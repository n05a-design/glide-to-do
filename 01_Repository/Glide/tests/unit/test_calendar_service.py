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
        from zoneinfo import ZoneInfo
        zone = ZoneInfo("Europe/Berlin")
        self.assertEqual(self.service.view(DAY, zone).blocks, ())
        self.assertEqual(len(self.service.view(date(2026, 10, 12), zone).blocks), 1)
        self.assertEqual(len(self.service.windows[DAY.year].blocks), 1)
        self.assertEqual(len(self.service.view(DAY, timezone.utc).blocks), 1)

    def test_year_margin_keeps_foreign_floating_zone_and_local_day_distinct(self):
        self.path.write_text("BEGIN:VCALENDAR\nBEGIN:VEVENT\nUID:probe\nDTSTART:20251231T230000Z\nDURATION:PT1H\nEND:VEVENT\nEND:VCALENDAR\n")
        self.service.load(self.path, timezone.utc, date(2026, 1, 1))
        self.finish()
        from zoneinfo import ZoneInfo
        self.assertEqual(len(self.service.view(date(2026, 1, 1), ZoneInfo("Europe/Berlin")).blocks), 1)
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

    def test_old_load_result_is_ignored_after_source_change(self):
        started, release = Event(), Event()
        old_reader = self.service.reader
        def reader(*args):
            started.set()
            self.assertTrue(release.wait(3))
            return old_reader(*args)
        self.service.reader = reader
        token = self.service.load(self.path, timezone.utc, DAY)
        self.assertTrue(started.wait(3))
        self.service.disable()
        release.set()
        self.assertTrue(self.finished.wait(3))
        result = self.service._results.get(timeout=3)
        self.service._results.put(result)
        self.assertFalse(self.service.poll())
        self.assertGreater(self.service.generation, token)
        self.assertEqual(self.service.view(DAY).status, "disabled")

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

if __name__ == "__main__":
    unittest.main()
