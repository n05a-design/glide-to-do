"""Echte lokale Quellen, unveränderliche Ergebnisse und begrenzte Rechenarbeit."""
from dataclasses import FrozenInstanceError
from datetime import date, timezone
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import busy_calendar as busy
import ics_recurrence as recurrence


def calendar(*events):
    return ("BEGIN:VCALENDAR\r\nVERSION:2.0\r\n" + "".join(events) + "END:VCALENDAR\r\n").encode()


def event(uid="e", rule="", start="20261011T080000Z"):
    return ("BEGIN:VEVENT\r\nUID:" + uid + "\r\nDTSTART:" + start +
            "\r\nDURATION:PT1H\r\nSUMMARY:Unverändert\r\n" +
            ("RRULE:" + rule + "\r\n" if rule else "") + "END:VEVENT\r\n")


class CalendarSourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="glide-busy-source-")
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "belegt.ics"
        self.content = calendar(event())
        self.path.write_bytes(self.content)

    def source(self):
        return busy.read_source(self.path, timezone.utc)

    def test_additive_config_preserves_metadata_and_exact_file_name(self):
        import copy
        value={"path":"/lokal/mit Leerzeichen .ics", "zone":"Europe/Berlin", "sha256":"a"*64,
               "loaded_at":"2026-10-11T18:00:00+02:00", "future":{"keep":True}}
        before=copy.deepcopy(value)
        self.assertEqual(busy.normalize_config(value),value)
        self.assertEqual(value,before)
        self.assertEqual(busy.normalize_config(None),{})
        self.assertEqual(busy.normalize_config({})["path"],"")

    def test_corrupt_selected_config_is_never_silently_disabled(self):
        for value in (False, [], {"path":3}, {"path":"/bad\x00path"}, {"path":"x"*4097},
                      {"path":"chosen.ics", "zone":"../zone"}, {"zone":None}, {"sha256":"wrong"}):
            with self.subTest(value=value), self.assertRaises(busy.SourceError):
                busy.normalize_config(value)

    def test_original_readonly_and_window_never_reloads(self):
        original = self.path.stat()
        source = self.source()
        self.assertEqual(source.sha256, hashlib.sha256(self.content).hexdigest())
        self.assertEqual(source.size, len(self.content))
        self.assertEqual(self.path.stat().st_mtime_ns, original.st_mtime_ns)
        self.path.unlink()
        with patch.object(Path, "open", side_effect=AssertionError("Keine Dateizugriffe in der Bilanz")):
            window = busy.expand_window(source, date(2026, 10, 11), date(2026, 10, 11))
        self.assertEqual(len(window.blocks), 1)
        self.assertEqual(window.sha256, source.sha256)
        self.assertTrue(window.contains(date(2026, 10, 11)))
        self.assertFalse(window.contains(date(2026, 10, 12)))
        with self.assertRaises(FrozenInstanceError):
            window.blocks = ()

    def test_missing_directory_and_invalid_utf8_fail_visibly(self):
        for source in (self.path.parent, self.path.parent / "fehlt.ics"):
            with self.subTest(source=source), self.assertRaises(busy.SourceError):
                busy.read_source(source, timezone.utc)
        self.path.write_bytes(b"\xff")
        with self.assertRaisesRegex(busy.SourceError, "UTF-8"):
            self.source()

    def test_size_and_folded_property_limits(self):
        with patch.object(busy, "MAX_BYTES", len(self.content) - 1):
            with self.assertRaisesRegex(busy.SourceError, "12 MiB"):
                self.source()
        self.path.write_bytes(calendar("SUMMARY:abc\r\n defgh\r\n"))
        with patch.object(busy, "MAX_LINE_BYTES", 12):
            with self.assertRaisesRegex(busy.SourceError, "zu lang"):
                self.source()

    def test_component_limits_apply_after_unfolding(self):
        self.path.write_bytes(calendar(event("a"), event("b")).replace(b"BEGIN:VEVENT", b"BEGIN:VE\r\n VENT"))
        with patch.object(busy, "MAX_EVENTS", 1):
            with self.assertRaisesRegex(busy.SourceError, "zu viele"):
                self.source()
        self.path.write_bytes(calendar("BEGIN:X\r\nBEGIN:Y\r\nEND:Y\r\nEND:X\r\n"))
        with patch.object(busy, "MAX_DEPTH", 2):
            with self.assertRaisesRegex(busy.SourceError, "verschachtelte"):
                self.source()

    def test_file_changed_while_reading_rejected(self):
        original = Path.stat
        calls = []
        def stat_changed(path, *args, **kwargs):
            if path == self.path:
                calls.append(True)
                if len(calls) == 2:
                    self.path.write_bytes(self.content + b" ")
            return original(path, *args, **kwargs)
        with patch.object(Path, "stat", stat_changed):
            with self.assertRaisesRegex(busy.SourceError, "beim Lesen geändert"):
                self.source()

    def test_reloading_changes_source_hash_and_blocks(self):
        before = self.source()
        self.path.write_bytes(calendar(event(start="20261012T080000Z")))
        after = self.source()
        self.assertNotEqual(before.sha256, after.sha256)
        self.assertEqual(len(busy.expand_window(before, date(2026, 10, 11), date(2026, 10, 11)).blocks), 1)
        self.assertEqual(busy.expand_window(after, date(2026, 10, 11), date(2026, 10, 11)).blocks, ())

    def test_unsupported_series_remains_reported(self):
        self.path.write_bytes(calendar(event(rule="FREQ=HOURLY")))
        result = busy.expand_window(self.source(), date(2026, 10, 11), date(2026, 10, 11))
        self.assertEqual(len(result.blocks), 1)
        self.assertIn("nicht berücksichtigt", result.issues[0][1])

    def test_old_counted_series_has_shared_work_limit(self):
        self.path.write_bytes(calendar(event(rule="FREQ=DAILY;COUNT=1000000", start="19000101T080000Z")))
        with self.assertRaisesRegex(busy.SourceError, "Prüfgrenze"):
            busy.expand_window(self.source(), date(2026, 10, 11), date(2026, 10, 11), max_steps=10)
        self.path.write_bytes(calendar(event("a", "FREQ=DAILY"), event("b", "FREQ=DAILY")))
        with self.assertRaisesRegex(busy.SourceError, "Prüfgrenze"):
            busy.expand_window(self.source(), date(2026, 10, 11), date(2026, 10, 13), max_steps=5)

    def test_interval_limit_fails_instead_of_partial_success(self):
        self.path.write_bytes(calendar(event("a"), event("b")))
        with self.assertRaisesRegex(busy.SourceError, "Zu viele Kalenderintervalle"):
            busy.expand_window(self.source(), date(2026, 10, 11), date(2026, 10, 11), max_blocks=1)

    def test_window_boundaries_and_empty_calendar(self):
        for first, last in ((date(2026, 10, 12), date(2026, 10, 11)),
                            (date(2026, 1, 1), date(2028, 1, 1)), (date.max, date.max)):
            with self.subTest(first=first, last=last), self.assertRaises(busy.SourceError):
                busy.expand_window(self.source(), first, last)
        self.path.write_bytes(calendar())
        self.assertEqual(busy.expand_window(self.source(), date(2026, 10, 11), date(2026, 10, 11)).blocks, ())

    def test_recurrence_budget_charges_days_in_monthly_and_yearly_periods(self):
        for frequency in ("MONTHLY", "YEARLY"):
            with self.subTest(frequency=frequency), self.assertRaises(recurrence.ExpansionLimitError):
                list(recurrence.dates(date(2026, 1, 1), "FREQ="+frequency,
                                      date(2027, 12, 31), budget=recurrence.Budget(10)))


    def test_date_values_keep_local_calendar_day_with_foreign_floating_zone(self):
        import timezones
        from occupied_time import day_occupancy
        resolver=timezones.Resolver()
        berlin,tokyo=resolver("Europe/Berlin"),resolver("Asia/Tokyo")
        self.path.write_text("BEGIN:VCALENDAR\nBEGIN:VEVENT\nUID:date\nDTSTART;VALUE=DATE:20261011\nEND:VEVENT\nBEGIN:VEVENT\nUID:floating\nDTSTART:20261011T090000\nDURATION:PT1H\nEND:VEVENT\nEND:VCALENDAR\n")
        source=busy.read_source(self.path,tokyo,resolver,berlin)
        window=busy.expand_window(source,date(2026,1,1),date(2026,12,31),2)
        self.assertFalse(day_occupancy(window.day_blocks(date(2026,10,10),berlin),date(2026,10,10),berlin,480)["all_day"])
        self.assertTrue(day_occupancy(window.day_blocks(date(2026,10,11),berlin),date(2026,10,11),berlin,480)["all_day"])
        self.assertFalse(day_occupancy(window.day_blocks(date(2026,10,12),berlin),date(2026,10,12),berlin,480)["all_day"])
        floating=next(block for block in window.blocks if not block.all_day)
        self.assertEqual(floating.start.astimezone(berlin).strftime("%H:%M"),"02:00")

    def test_all_day_rules_exclusions_and_dst_use_date_zone(self):
        import timezones
        from occupied_time import day_occupancy
        resolver=timezones.Resolver();berlin=resolver("Europe/Berlin")
        self.path.write_text("BEGIN:VCALENDAR\nBEGIN:VEVENT\nUID:date-series\nDTSTART;VALUE=DATE:20261024\nRRULE:FREQ=DAILY;COUNT=3\nEXDATE;VALUE=DATE:20261026\nRDATE;VALUE=DATE:20261029\nEND:VEVENT\nEND:VCALENDAR\n")
        source=busy.read_source(self.path,timezone.utc,resolver,berlin)
        window=busy.expand_window(source,date(2026,1,1),date(2026,12,31),2)
        self.assertFalse(window.issues)
        self.assertEqual([block.start.date().isoformat()for block in window.blocks],["2026-10-24","2026-10-25","2026-10-29"])
        value=day_occupancy(window.day_blocks(date(2026,10,25),berlin),date(2026,10,25),berlin,480)
        self.assertEqual((value["minutes"],value["day_minutes"],value["capacity"]),(1500,1500,0))
        self.assertFalse(window.day_blocks(date(2026,10,26),berlin))

    def test_all_day_source_default_remains_backward_compatible(self):
        self.path.write_text("BEGIN:VCALENDAR\nBEGIN:VEVENT\nUID:date\nDTSTART;VALUE=DATE:20261011\nEND:VEVENT\nEND:VCALENDAR\n")
        source=busy.read_source(self.path,timezone.utc)
        self.assertEqual(source.calendar.events[0].start.tzinfo,timezone.utc)

if __name__ == "__main__":
    unittest.main()
