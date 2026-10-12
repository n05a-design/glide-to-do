from datetime import date, datetime, timedelta, timezone
import unittest
import ics_busy as ics
from ics_recurrence import dates, matches_start
import timezones

# Mitgelieferte IANA-Daten statt Systemdatenbank: Windows bringt keine mit,
# Glide selbst löst Zonen ebenfalls über timezones.Resolver auf.
IANA = timezones.Resolver()

UTC=timezone.utc


def parse(*events, zones="", zone=UTC):
    return ics.parse_calendar("BEGIN:VCALENDAR\nVERSION:2.0\n"+zones+"".join(
        "BEGIN:VEVENT\n"+event+"\nEND:VEVENT\n" for event in events)+"END:VCALENDAR\n",zone)


def expand(*events):
    return ics.expand(parse(*events),datetime(2026,1,1,tzinfo=UTC),datetime(2027,1,1,tzinfo=UTC))


class EdgeTests(unittest.TestCase):
    def test_weekly_series_at_both_date_limits_keeps_valid_days(self):
        self.assertEqual(list(dates(date.min,"FREQ=WEEKLY;BYDAY=MO,SU;WKST=SU;COUNT=3",date(1,1,8))),
            [date(1,1,1),date(1,1,7),date(1,1,8)])
        self.assertEqual(list(dates(date(9999,12,27),"FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR,SA,SU;COUNT=8",date.max)),
            [date(9999,12,day) for day in range(27,32)])

    def test_inconsistent_start_is_visible_and_only_start_is_kept(self):
        self.assertFalse(matches_start(date(2026,10,10),"FREQ=WEEKLY;BYDAY=MO"))
        self.assertFalse(matches_start(date(2026,10,20),"FREQ=MONTHLY;BYDAY=TU;BYSETPOS=1"))
        self.assertTrue(matches_start(date(2026,10,6),"FREQ=MONTHLY;BYDAY=TU;BYSETPOS=1"))
        result=expand("UID:bad-filter\nDTSTART:20261010T090000Z\nDURATION:PT1H\nRRULE:FREQ=WEEKLY;BYDAY=MO")
        self.assertEqual(len(result.blocks),1)
        self.assertIn("nicht definiert",result.issues[0][1])

    def test_floating_until_needs_floating_time(self):
        bad=expand("UID:floating\nDTSTART:20261010T090000\nDURATION:PT1H\nRRULE:FREQ=DAILY;UNTIL=20261012T090000Z")
        self.assertEqual(len(bad.blocks),1);self.assertTrue(bad.issues)
        good=expand("UID:floating\nDTSTART:20261010T090000\nDURATION:PT1H\nRRULE:FREQ=DAILY;UNTIL=20261012T090000")
        self.assertEqual([block.start.day for block in good.blocks],[10,11,12]);self.assertFalse(good.issues)

    def test_wrong_exception_date_type_does_not_cancel_master_occurrence(self):
        result=expand("UID:typed\nDTSTART;VALUE=DATE:20261010\nRRULE:FREQ=DAILY;COUNT=2",
            "UID:typed\nRECURRENCE-ID:20261011T000000Z\nSTATUS:CANCELLED")
        self.assertEqual([block.start.day for block in result.blocks],[10,11]);self.assertTrue(result.issues)
        result=expand("UID:typed\nDTSTART;VALUE=DATE:20261010\nRRULE:FREQ=DAILY;COUNT=2",
            "UID:typed\nRECURRENCE-ID;VALUE=DATE:20261011\nSTATUS:CANCELLED")
        self.assertEqual([block.start.day for block in result.blocks],[10]);self.assertFalse(result.issues)

    def test_revision_timestamp_is_validated_before_choosing_newest(self):
        base="UID:revision\nDTSTART:20261010T090000Z\nDURATION:PT1H\nSEQUENCE:1\nDTSTAMP:20261001T120000Z"
        result=expand(base,base.replace("T090000Z","T100000Z").replace("20261001T120000Z","20261002T120000Z"))
        self.assertEqual(result.blocks[0].start.hour,10)
        for stamp in ("20261301T120000Z","20261001T120000","nichts"):
            result=expand(base,base.replace("SEQUENCE:1","SEQUENCE:2").replace("20261001T120000Z",stamp))
            self.assertEqual(result.blocks[0].start.hour,9);self.assertTrue(result.issues)

    def test_lookback_at_first_date_does_not_drop_first_year_series(self):
        result=ics.expand(parse("UID:first\nDTSTART:00010101T090000Z\nDURATION:PT1H\nRRULE:FREQ=DAILY;COUNT=2"),
            datetime(1,1,1,tzinfo=UTC),datetime(1,1,3,tzinfo=UTC))
        self.assertEqual([block.start.day for block in result.blocks],[1,2]);self.assertFalse(result.issues)

    def test_southern_half_hour_embedded_zone_matches_iana(self):
        zones="""BEGIN:VTIMEZONE
TZID:Local/LordHowe
BEGIN:DAYLIGHT
DTSTART:20251005T020000
TZOFFSETFROM:+1030
TZOFFSETTO:+1100
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=1SU
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:20260405T020000
TZOFFSETFROM:+1100
TZOFFSETTO:+1030
RRULE:FREQ=YEARLY;BYMONTH=4;BYDAY=1SU
END:STANDARD
END:VTIMEZONE
"""
        calendar=parse("UID:half\nDTSTART;TZID=Local/LordHowe:20260101T120000\nDURATION:PT1H",zones=zones)
        self.assertFalse(calendar.issues)
        embedded=calendar.events[0].start.tzinfo;actual=IANA("Australia/Lord_Howe")
        moment=datetime(2026,1,1,tzinfo=UTC)
        while moment.year==2026:
            left,right=moment.astimezone(embedded),moment.astimezone(actual)
            self.assertEqual((left.replace(tzinfo=None),left.utcoffset(),left.dst(),left.fold),
                (right.replace(tzinfo=None),right.utcoffset(),right.dst(),right.fold),moment)
            moment+=timedelta(hours=6)
        local=datetime(2026,4,5,1,45,tzinfo=embedded)
        self.assertEqual(local.utcoffset(),timedelta(hours=11))
        self.assertEqual(local.replace(fold=1).utcoffset(),timedelta(hours=10,minutes=30))


if __name__=="__main__":unittest.main()
