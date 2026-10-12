import unittest
from datetime import datetime,timedelta,timezone
from zoneinfo import ZoneInfo
from ics_timezone import CalendarZone,Observance,offset,parse_zone
import ics_recurrence as recurrence
import ics_busy as ics

UTC=timezone.utc
class TimezoneTests(unittest.TestCase):
    def setUp(self):
        self.zone=CalendarZone('Custom/Berlin',[
            Observance(datetime(1970,3,29,2),timedelta(hours=1),timedelta(hours=2),True,'CEST',
                recurrence.parse_rule('FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU')),
            Observance(datetime(1970,10,25,3),timedelta(hours=2),timedelta(hours=1),False,'CET',
                recurrence.parse_rule('FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU'))])
    def test_offsets_validation(self):
        self.assertEqual(offset('+053045'),timedelta(hours=5,minutes=30,seconds=45))
        self.assertEqual(offset('-0400'),timedelta(hours=-4))
        for value in ('-0000','+2400','+0060','+000060','0100'):
            with self.assertRaises(ValueError): offset(value)
    def test_all_2026_utc_instants_match_iana(self):
        reference=ZoneInfo('Europe/Berlin')
        instant=datetime(2026,1,1,tzinfo=UTC)
        while instant.year==2026:
            actual=instant.astimezone(self.zone);expected=instant.astimezone(reference)
            self.assertEqual(actual.replace(tzinfo=None),expected.replace(tzinfo=None))
            self.assertEqual((actual.utcoffset(),actual.dst(),actual.fold),(expected.utcoffset(),expected.dst(),expected.fold))
            instant+=timedelta(hours=6)
    def test_fold_both_hours_and_gap_roundtrip(self):
        for fold,offset_hours in ((0,2),(1,1)):
            moment=datetime(2026,10,25,2,30,tzinfo=self.zone,fold=fold)
            self.assertEqual(moment.utcoffset(),timedelta(hours=offset_hours))
            returned=moment.astimezone(UTC).astimezone(self.zone)
            self.assertEqual(returned.fold,fold)
            self.assertEqual(returned.replace(tzinfo=None),moment.replace(tzinfo=None))
        gap=datetime(2026,3,29,2,30,tzinfo=self.zone)
        self.assertEqual(gap.utcoffset(),timedelta(hours=1))
        self.assertFalse(ics.valid_local(gap))
        self.assertEqual(gap.astimezone(UTC).astimezone(self.zone).hour,3)
    def test_fixed_zone_before_and_after_first_transition(self):
        zone=CalendarZone('Fixed',[Observance(datetime(1970,1,1),timedelta(hours=5),timedelta(hours=5),False,'Fixed')])
        for year in (1960,2026):
            self.assertEqual(datetime(year,1,1,tzinfo=UTC).astimezone(zone).hour,5)
            self.assertEqual(datetime(year,1,1,tzinfo=zone).dst(),timedelta(0))
    def test_rdate_and_finite_rule(self):
        zone=CalendarZone('Finite',[
            Observance(datetime(2025,3,30,2),timedelta(hours=1),timedelta(hours=2),True,'Summer',extra=(datetime(2026,3,29,2),)),
            Observance(datetime(2025,10,26,3),timedelta(hours=2),timedelta(hours=1),False,'Winter',extra=(datetime(2026,10,25,3),))])
        self.assertEqual(datetime(2026,7,1,tzinfo=zone).utcoffset(),timedelta(hours=2))
        self.assertEqual(datetime(2028,7,1,tzinfo=zone).utcoffset(),timedelta(hours=1))
    def test_embedded_zone_without_system_database(self):
        text='''BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VTIMEZONE
TZID:Custom/Berlin
BEGIN:DAYLIGHT
DTSTART:19700329T020000
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
END:DAYLIGHT
BEGIN:STANDARD
DTSTART:19701025T030000
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD
END:VTIMEZONE
BEGIN:VEVENT
UID:embedded
DTSTART;TZID=Custom/Berlin:20260327T023000
DURATION:PT30M
RRULE:FREQ=DAILY;COUNT=3
END:VEVENT
END:VCALENDAR'''
        def unavailable(name): raise ValueError('Kein Systembestand')
        calendar=ics.parse_calendar(text,UTC,resolver=unavailable)
        result=ics.expand(calendar,datetime(2026,3,1,tzinfo=UTC),datetime(2026,4,1,tzinfo=UTC))
        self.assertFalse(result.issues)
        self.assertEqual([b.start.day for b in result.blocks],[27,28,30])
        invalid=text.replace('FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU','FREQ=HOURLY')
        calendar=ics.parse_calendar(invalid,UTC,resolver=unavailable)
        self.assertTrue(calendar.issues);self.assertFalse(calendar.events)
    def test_inconsistent_chain_rejected(self):
        zone=CalendarZone('Bad',[Observance(datetime(2026,3,1),timedelta(hours=1),timedelta(hours=2),True,'A'),
                                 Observance(datetime(2026,10,1),timedelta(hours=3),timedelta(hours=1),False,'B')])
        with self.assertRaises(ValueError): datetime(2026,5,1,tzinfo=zone).utcoffset()

if __name__=='__main__': unittest.main()
