import unittest
from datetime import datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path
import tempfile
from zipfile import ZipFile
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import timezones
import ics_busy

UTC = timezone.utc


def unavailable(key):
    raise ZoneInfoNotFoundError(key)


class Zones(unittest.TestCase):
    def setUp(self):
        self.resolver = timezones.Resolver(system=unavailable)

    def test_no_system_database_and_future_dst(self):
        zone = self.resolver("Europe/Berlin")
        self.assertEqual(datetime(2050, 1, 1, tzinfo=zone).utcoffset(), timedelta(hours=1))
        self.assertEqual(datetime(2050, 7, 1, tzinfo=zone).utcoffset(), timedelta(hours=2))
        self.assertIs(zone, self.resolver("Europe/Berlin"))

    def test_fold_and_gap(self):
        zone = self.resolver("Europe/Berlin")
        before = datetime(2026, 10, 25, 0, 30, tzinfo=UTC).astimezone(zone)
        after = datetime(2026, 10, 25, 1, 30, tzinfo=UTC).astimezone(zone)
        self.assertEqual((before.hour, before.fold, after.hour, after.fold), (2, 0, 2, 1))
        self.assertFalse(ics_busy.valid_local(datetime(2026, 3, 29, 2, 30, tzinfo=zone)))

    def test_southern_and_half_hour(self):
        zone = self.resolver("Australia/Lord_Howe")
        self.assertEqual(datetime(2026, 1, 1, tzinfo=zone).utcoffset(), timedelta(hours=11))
        self.assertEqual(datetime(2026, 7, 1, tzinfo=zone).utcoffset(), timedelta(hours=10, minutes=30))
        zone = self.resolver("Asia/Kathmandu")
        self.assertEqual(datetime(2026, 7, 1, tzinfo=zone).utcoffset(), timedelta(hours=5, minutes=45))

    def test_latest_canadian_change(self):
        zone = self.resolver("America/Winnipeg")
        self.assertEqual(datetime(2026, 12, 1, tzinfo=zone).utcoffset(), timedelta(hours=-5))

    def test_every_packaged_zone_readable(self):
        with ZipFile(timezones.RESOURCES / "iana-2026e.zip") as archive:
            self.assertGreater(len(archive.namelist()), 590)
            for key in archive.namelist():
                with self.subTest(key=key):
                    zone = self.resolver(key)
                    self.assertIsNotNone(datetime(2026, 10, 10, tzinfo=zone).utcoffset())

    def test_unknown_and_unsafe_key(self):
        with self.assertRaises(ZoneInfoNotFoundError): self.resolver("Unknown/Here")
        for key in ("/etc/passwd", "../UTC", "Etc//UTC", "Etc/./UTC", "C:/UTC", "Etc\\UTC", "UTC\x00", ""):
            with self.subTest(key=key), self.assertRaises(ValueError): self.resolver(key)

    def test_system_fallback_without_packaged_file(self):
        with tempfile.TemporaryDirectory() as folder:
            resolver = timezones.Resolver(folder, system=lambda key: UTC)
            self.assertIs(resolver("New/Zone"), UTC)

    def test_broken_packaged_file_visible(self):
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, "iana-2026e.zip").write_bytes(b"kaputt")
            with self.assertRaises(Exception): timezones.Resolver(folder)("UTC")

    def test_windows_mapping_and_territory(self):
        self.assertEqual(self.resolver.windows_key("W. Europe Standard Time"), "Europe/Berlin")
        self.assertEqual(self.resolver.windows_key("W. Europe Standard Time", "AT"), "Europe/Vienna")
        with self.assertRaises(ZoneInfoNotFoundError): self.resolver.windows_key("Unknown")

    def test_windows_local_keeps_future_dst(self):
        zone = timezones.local_zone(self.resolver, environment={}, platform="win32",
                                  windows_reader=lambda: ("W. Europe Standard Time", False))
        self.assertEqual(datetime(2026, 7, 1, tzinfo=zone).utcoffset(), timedelta(hours=2))
        self.assertEqual(datetime(2026, 12, 1, tzinfo=zone).utcoffset(), timedelta(hours=1))

    def test_windows_disabled_dst(self):
        fixed = timezone(timedelta(hours=1))
        zone = timezones.local_zone(self.resolver, environment={}, platform="win32",
                                  windows_reader=lambda: ("W. Europe Standard Time", True), fixed_local=fixed)
        self.assertIs(zone, fixed)

    def test_local_tzif_and_explicit_environment(self):
        with tempfile.TemporaryDirectory() as folder, ZipFile(timezones.RESOURCES / "iana-2026e.zip") as archive:
            path = Path(folder, "localtime"); path.write_bytes(archive.read("Europe/Berlin"))
            zone = timezones.local_zone(self.resolver, environment={}, platform="darwin", localtime=path)
            self.assertEqual(datetime(2026, 7, 1, tzinfo=zone).utcoffset(), timedelta(hours=2))
            self.assertEqual(timezones.local_zone(self.resolver, environment={"TZ": "Asia/Tokyo"}).key, "Asia/Tokyo")
            self.assertEqual(datetime(2026, 7, 1, tzinfo=timezones.local_zone(self.resolver, environment={"TZ": ":"+str(path)})).utcoffset(), timedelta(hours=2))

    def test_timezone_file_and_unavailable_local(self):
        with tempfile.TemporaryDirectory() as folder:
            missing = Path(folder, "missing"); text = Path(folder, "timezone");text.write_text("Europe/Berlin\n")
            self.assertEqual(timezones.local_zone(self.resolver, environment={}, platform="linux", localtime=missing, timezone_file=text).key, "Europe/Berlin")
            with self.assertRaises(ZoneInfoNotFoundError):
                timezones.local_zone(self.resolver, environment={}, platform="linux", localtime=missing, timezone_file=missing)

    def test_ics_without_system_zones(self):
        text = "BEGIN:VCALENDAR\nBEGIN:VEVENT\nUID:z\nDTSTART;TZID=Europe/Berlin:20260328T100000\nDURATION:PT1H\nRRULE:FREQ=DAILY;COUNT=3\nEND:VEVENT\nEND:VCALENDAR"
        calendar = ics_busy.parse_calendar(text, UTC, resolver=self.resolver)
        expanded = ics_busy.expand(calendar, datetime(2026,3,28,tzinfo=UTC), datetime(2026,4,1,tzinfo=UTC))
        self.assertFalse(expanded.issues)
        self.assertEqual([block.start.astimezone(UTC).hour for block in expanded.blocks], [9,8,8])


if __name__ == "__main__": unittest.main()
