"""Quellwechsel, veraltete Ergebnisse und echte Arbeit ohne Tk-Hauptthread."""
from datetime import date, timezone, timedelta
from pathlib import Path
from threading import Event, get_ident
import tempfile
import unittest
from unittest.mock import patch
import busy_calendar
from calendar_service import CalendarService

DAY = date(2026, 10, 11)


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="glide-calendar-worker-")
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "test.ics"
        self.path.write_text("BEGIN:VCALENDAR\nBEGIN:VEVENT\nUID:probe\nDTSTART:20261011T080000Z\nDURATION:PT1H\nEND:VEVENT\nEND:VCALENDAR\n")
        self.finished = Event()
        self.worker_ids = []
        def expand(*args):
            self.worker_ids.append(get_ident())
            try:
                return busy_calendar.expand_window(*args)
            finally:
                self.finished.set()
        self.service = CalendarService(expander=expand, cache_size=1)
        self.addCleanup(self.service.close)

    def finish(self):
        self.assertTrue(self.finished.wait(3), "Arbeiter beendet sich nicht")
        # Das Ereignis liegt unmittelbar vor der Ergebnisübergabe. Ein Queue-
        # Marker wartet auf genau dieses Ergebnis, ohne Zeit-/Sleep-Annahme.
        result = self.service._results.get(timeout=3)
        self.service._results.put(result)
        self.assertTrue(self.service.poll())
        self.finished.clear()

    def load(self):
        self.service.load(self.path, timezone.utc, DAY)
        self.finish()

    def test_load_runs_off_caller_thread_and_ready_never_reads_file(self):
        self.assertEqual(self.service.view(DAY).status, "disabled")
        self.load()
        self.assertNotIn(get_ident(), self.worker_ids)
        self.path.unlink()
        with patch.object(Path, "open", side_effect=AssertionError("Kein IO")):
            view = self.service.view(DAY)
        self.assertEqual((view.status, len(view.blocks)), ("ready", 1))
        self.assertFalse(self.service.poll())

    def test_day_index_returns_local_day_only_without_losing_year_preview(self):
        self.path.write_text("BEGIN:VCALENDAR\nBEGIN:VEVENT\nUID:probe\nDTSTART:20261011T230000Z\nDURATION:PT1H\nEND:VEVENT\nEND:VCALENDAR\n")
        self.load()
        import timezones
        zone = timezones.Resolver()("Europe/Berlin")  # mitgelieferte IANA-Daten (Windows ohne Systemdatenbank)
        self.assertEqual(self.service.view(DAY, zone).blocks, ())
        self.assertEqual(len(self.service.view(date(2026, 10, 12), zone).blocks), 1)
        self.assertEqual(len(self.service.windows[DAY.year].blocks), 1)
        self.assertEqual(len(self.service.view(DAY, timezone.utc).blocks), 1)

    def test_year_margin_keeps_foreign_floating_zone_and_local_day_distinct(self):
        self.path.write_text("BEGIN:VCALENDAR\nBEGIN:VEVENT\nUID:probe\nDTSTART:20251231T230000Z\nDURATION:PT1H\nEND:VEVENT\nEND:VCALENDAR\n")
        self.service.load(self.path, timezone.utc, date(2026, 1, 1))
        self.finish()
        import timezones
        self.assertEqual(len(self.service.view(date(2026, 1, 1), timezones.Resolver()("Europe/Berlin")).blocks), 1)
        self.assertEqual(self.service.view(date(2026, 1, 1), timezone.utc).blocks, ())
        self.assertEqual(self.service.windows[2026].first, date(2026, 1, 1))

    def test_leap_year_margin_stays_within_shared_window_bound(self):
        self.service.load(self.path, timezone.utc, date(2028, 1, 1))
        self.finish()
        self.assertEqual(self.service.view(date(2028, 1, 1)).status, "ready")

    def test_load_and_expansion_failures_are_unknown_not_free(self):
        self.service.load(self.path.parent / "fehlt", timezone.utc, DAY)
        result = self.service._results.get(timeout=3)
        self.service._results.put(result)
        self.service.poll()
        self.assertEqual(self.service.view(DAY).status, "error")
        self.assertIsNone(self.service.source)
        self.load()
        def fail(*args):
            self.finished.set()
            raise ValueError("keine vollständige Serie")
        self.service.expander = fail
        next_year = date(2027, 1, 1)
        self.assertEqual(self.service.view(next_year).status, "loading")
        self.finish()
        self.assertEqual(self.service.view(next_year).status, "error")
        self.assertIn("keine vollständige", self.service.view(next_year).message)
        self.assertEqual(self.service.view(DAY).status, "ready")

    def test_year_cache_eviction_and_requests_are_deduplicated(self):
        self.load()
        other = date(2027, 1, 1)
        for _ in range(10):
            self.assertEqual(self.service.view(other).status, "loading")
        self.assertEqual(self.service.pending, {2027})
        self.finish()
        self.assertEqual(list(self.service.windows), [2027])
        self.assertEqual(self.service.view(other).status, "ready")
        self.assertEqual(self.service.view(DAY).status, "loading")
        self.finish()
        self.assertEqual(list(self.service.windows), [2026])
        self.assertEqual(len(self.worker_ids), 3)

    def test_adopt_only_matching_hash_and_closed_service_stays_closed(self):
        source = busy_calendar.read_source(self.path, timezone.utc)
        window = busy_calendar.expand_window(source, date(2026, 1, 1), date(2026, 12, 31))
        self.service.adopt(source, window)
        self.assertEqual(self.service.view(DAY).status, "ready")
        from dataclasses import replace
        with self.assertRaises(ValueError):
            self.service.adopt(source, replace(window, sha256="anderer Stand"))
        with self.assertRaises(ValueError):
            self.service.adopt(source, busy_calendar.expand_window(source, DAY, DAY))
        self.service.close()
        self.assertEqual(self.service.view(DAY).status, "closed")
        with self.assertRaises(RuntimeError):
            self.service.load(self.path, timezone.utc, DAY)
        with self.assertRaises(RuntimeError):
            self.service.adopt(source, window)

    def test_earliest_day_with_positive_zone_is_visible_error_without_poisoning_utc(self):
        self.service.load(self.path, timezone.utc, date.min)
        self.finish()
        view = self.service.view(date.min, timezone(timedelta(hours=14)))
        self.assertEqual(view.status, "error")
        self.assertIn("Tagesgrenzen", view.message)
        self.assertEqual(self.service.view(date.min, timezone.utc).status, "ready")

    def test_date_limit_is_visible_without_worker_job(self):
        self.load()
        self.assertEqual(self.service.view(date.max).status, "error")
        self.assertEqual(self.service.view("2026-10-11").status, "error")
        self.assertEqual(self.service.pending, set())


    def test_worker_carries_local_date_zone_separately_from_floating_times(self):
        import timezones
        resolver=timezones.Resolver();berlin=resolver("Europe/Berlin");tokyo=resolver("Asia/Tokyo")
        self.path.write_text("BEGIN:VCALENDAR\nBEGIN:VEVENT\nUID:date\nDTSTART;VALUE=DATE:20261011\nEND:VEVENT\nEND:VCALENDAR\n")
        self.service.load(self.path,tokyo,DAY,resolver,berlin)
        self.finish()
        self.assertFalse(self.service.view(date(2026,10,10),berlin).blocks)
        current=self.service.view(DAY,berlin)
        self.assertEqual((current.status,len(current.blocks)),("ready",1))
        self.assertEqual(current.blocks[0].start.tzinfo,berlin)
        self.assertFalse(self.service.view(date(2026,10,12),berlin).blocks)


class ObsoleteReadTests(unittest.TestCase):
    """Ereignisse bestimmen die Reihenfolge, Zeitlimits erkennen nur Hänger."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="glide-calendar-obsolete-")
        self.addCleanup(self.temp.cleanup)
        self.paths, self.sources = {}, {}
        for name in ("old", "latest", "adopted"):
            path = Path(self.temp.name) / (name + ".ics")
            path.write_text("BEGIN:VCALENDAR\nBEGIN:VEVENT\nUID:" + name
                            + "\nDTSTART:20261011T080000Z\nDURATION:PT1H\nEND:VEVENT\nEND:VCALENDAR\n")
            self.paths[name] = path
            self.sources[name] = busy_calendar.read_source(path, timezone.utc)
        self.old_started, self.old_release = Event(), Event()
        self.latest_started, self.latest_release = Event(), Event()
        self.latest_release.set()
        self.expansion_started, self.expansion_release = Event(), Event()
        self.expansion_release.set()
        self.old_read_error = self.old_expansion_error = None
        self.block_old_expansion = False
        self.reads, self.expanded = [], []

        def reader(path, *args):
            name = next(name for name, candidate in self.paths.items() if candidate == path)
            self.reads.append(name)
            if name == "old":
                self.old_started.set()
                if not self.old_release.wait(3):
                    raise TimeoutError("Alter Leser wurde nicht freigegeben")
                if self.old_read_error is not None:
                    raise self.old_read_error
            else:
                self.latest_started.set()
                if not self.latest_release.wait(3):
                    raise TimeoutError("Neuer Leser wurde nicht freigegeben")
            return self.sources[name]

        def expander(source, *args):
            self.expanded.append(source.sha256)
            if source is self.sources["old"] and self.block_old_expansion:
                self.expansion_started.set()
                if not self.expansion_release.wait(3):
                    raise TimeoutError("Alte Expansion wurde nicht freigegeben")
                if self.old_expansion_error is not None:
                    raise self.old_expansion_error
            return busy_calendar.expand_window(source, *args)

        self.service = CalendarService(reader=reader, expander=expander)
        self.addCleanup(self.stop)

    def stop(self):
        self.old_release.set()
        self.latest_release.set()
        self.expansion_release.set()
        self.service.close()
        if self.service._thread is not None:
            self.service._thread.join(3)
            self.assertFalse(self.service._thread.is_alive(), "Kalenderarbeiter beendet sich nicht")

    def start_old_read(self):
        token = self.service.load(self.paths["old"], timezone.utc, DAY)
        self.assertTrue(self.old_started.wait(3), "Alter Leser startet nicht")
        return token

    def finish_worker(self):
        # Der vorhandene Endmarker steht hinter allen Testaufträgen. join()
        # belegt ihren Abschluss auch dann, wenn ein veralteter Auftrag weder
        # Expansion noch Ergebnis erzeugt. Kein Sleep und kein Pollingrennen.
        self.service._jobs.put(None)
        self.service._thread.join(3)
        self.assertFalse(self.service._thread.is_alive(), "Kalenderarbeiter beendet sich nicht")
        return self.service.poll()

    def test_source_change_skips_obsolete_expansion_and_runs_latest_on_same_worker(self):
        token = self.start_old_read()
        worker = self.service._thread
        self.service.load(self.paths["latest"], timezone.utc, DAY)
        self.old_release.set()
        self.assertTrue(self.finish_worker())
        self.assertEqual(self.reads, ["old", "latest"])
        self.assertEqual(self.expanded, [self.sources["latest"].sha256])
        self.assertIs(self.service._thread, worker)
        self.assertGreater(self.service.generation, token)
        self.assertIs(self.service.source, self.sources["latest"])
        self.assertEqual(self.service.view(DAY).status, "ready")
        self.assertEqual(self.service.pending, set())

    def test_disable_during_read_skips_expansion_and_keeps_disabled(self):
        self.start_old_read()
        self.service.disable()
        self.old_release.set()
        self.assertFalse(self.finish_worker())
        self.assertEqual(self.expanded, [])
        self.assertEqual(self.service.view(DAY).status, "disabled")
        self.assertEqual((self.service.pending, self.service.failures), (set(), {}))
        self.assertFalse(self.service.loading)

    def test_same_source_reload_skips_old_year_and_keeps_latest_generation(self):
        self.start_old_read()
        self.service.load(self.paths["old"], timezone.utc, date(2027, 1, 1))
        self.old_release.set()
        self.assertTrue(self.finish_worker())
        self.assertEqual(self.reads, ["old", "old"])
        self.assertEqual(self.expanded, [self.sources["old"].sha256])
        self.assertEqual(list(self.service.windows), [2027])
        self.assertEqual(self.service.pending, set())

    def test_queued_source_change_is_skipped_before_reading(self):
        self.start_old_read()
        self.service.load(self.paths["latest"], timezone.utc, DAY)
        self.service.load(self.paths["adopted"], timezone.utc, DAY)
        self.old_release.set()
        self.assertTrue(self.finish_worker())
        self.assertEqual(self.reads, ["old", "adopted"])
        self.assertEqual(self.expanded, [self.sources["adopted"].sha256])
        self.assertIs(self.service.source, self.sources["adopted"])

    def test_close_during_read_skips_expansion_and_keeps_closed(self):
        self.start_old_read()
        self.service.close()
        self.old_release.set()
        self.assertFalse(self.finish_worker())
        self.assertEqual(self.expanded, [])
        self.assertEqual(self.service.view(DAY).status, "closed")
        self.assertEqual(self.service.pending, set())

    def test_adopt_during_read_skips_expansion_and_preserves_adopted_window(self):
        source = self.sources["adopted"]
        window = busy_calendar.expand_window(source, date(2026, 1, 1), date(2026, 12, 31))
        self.start_old_read()
        self.service.adopt(source, window)
        self.old_release.set()
        self.assertFalse(self.finish_worker())
        self.assertEqual(self.expanded, [])
        self.assertIs(self.service.source, source)
        self.assertIs(self.service.windows[DAY.year], window)
        self.assertEqual(self.service.view(DAY).status, "ready")

    def assert_latest_waiting_after_old_completion(self):
        self.assertTrue(self.latest_started.wait(3), "Neuer Leser startet nicht")
        # Das alte Ergebnis liegt vor dem Start des nächsten Readers in _results.
        self.assertFalse(self.service.poll())
        self.assertTrue(self.service.loading)
        self.assertEqual(self.service.pending, {DAY.year})
        self.assertEqual((self.service.error, self.service.failures), ("", {}))
        self.assertEqual(self.service.view(DAY).status, "loading")
        self.latest_release.set()
        self.assertTrue(self.finish_worker())
        self.assertEqual(self.service.view(DAY).status, "ready")
        self.assertIs(self.service.source, self.sources["latest"])

    def test_obsolete_reader_error_does_not_clear_latest_loading_or_pending_state(self):
        self.old_read_error = ValueError("Veralteter Lesefehler")
        self.latest_release.clear()
        self.start_old_read()
        self.service.load(self.paths["latest"], timezone.utc, DAY)
        self.old_release.set()
        self.assert_latest_waiting_after_old_completion()
        self.assertEqual(self.expanded, [self.sources["latest"].sha256])

    def test_already_running_expansion_result_does_not_replace_latest_source(self):
        self.block_old_expansion = True
        self.expansion_release.clear()
        self.latest_release.clear()
        self.start_old_read()
        self.old_release.set()
        self.assertTrue(self.expansion_started.wait(3), "Alte Expansion startet nicht")
        self.service.load(self.paths["latest"], timezone.utc, DAY)
        self.expansion_release.set()
        self.assert_latest_waiting_after_old_completion()
        self.assertEqual(self.expanded, [self.sources["old"].sha256,
                                        self.sources["latest"].sha256])

    def test_already_running_expansion_finishes_and_its_old_error_stays_ignored(self):
        self.block_old_expansion = True
        self.old_expansion_error = ValueError("Veralteter Expansionsfehler")
        self.expansion_release.clear()
        self.latest_release.clear()
        self.start_old_read()
        self.old_release.set()
        self.assertTrue(self.expansion_started.wait(3), "Alte Expansion startet nicht")
        self.service.load(self.paths["latest"], timezone.utc, DAY)
        self.assertFalse(self.latest_started.is_set())
        self.expansion_release.set()
        self.assert_latest_waiting_after_old_completion()
        self.assertEqual(self.expanded, [self.sources["old"].sha256,
                                        self.sources["latest"].sha256])

if __name__ == "__main__":
    unittest.main()
