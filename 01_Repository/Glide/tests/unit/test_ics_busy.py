import unittest
from datetime import datetime, timedelta, timezone
import ics_busy as ics
from occupied_time import utc
import timezones

# Mitgelieferte IANA-Daten statt Systemdatenbank: Windows bringt keine mit,
# Glide selbst löst Zonen ebenfalls über timezones.Resolver auf.
IANA = timezones.Resolver()

class CalendarTests(unittest.TestCase):
    def setUp(self):
        self.zone=IANA('Europe/Berlin')
        self.start=datetime(2026,3,1,tzinfo=self.zone)
        self.end=datetime(2026,4,2,tzinfo=self.zone)
    def parse(self,*events,resolver=IANA):
        text='BEGIN:VCALENDAR\r\nVERSION:2.0\r\n'+''.join('BEGIN:VEVENT\r\n'+event.replace('\n','\r\n')+'\r\nEND:VEVENT\r\n' for event in events)+'END:VCALENDAR\r\n'
        return ics.parse_calendar(text,self.zone,resolver)
    def expand(self,*events):
        return ics.expand(self.parse(*events),self.start,self.end)
    def test_timezone_utc_and_floating(self):
        result=self.expand('UID:one\nDTSTART;TZID=Europe/Berlin:20260310T090000\nDTEND:20260310T090000Z\nSUMMARY:Besprechung',
            'UID:two\nDTSTART:20260310T100000\nDURATION:PT30M')
        self.assertFalse(result.issues)
        self.assertEqual([int((utc(b.end)-utc(b.start)).total_seconds()/60) for b in result.blocks],[60,30])
    def test_unfolding_quoted_params_and_text(self):
        result=self.expand('UID:one\nDTSTART;TZID="Europe/Berlin":20260310T090000\nDURATION:PT30M\nSUMMARY:Text\\, mit\\;\n Fortsetzung\\nZweite Zeile')
        self.assertEqual(result.blocks[0].title,'Text, mit;Fortsetzung\nZweite Zeile')
        prop=ics.property_line('ATTENDEE;CN="Name: mit; Zeichen":mailto:x@example.test')
        self.assertEqual(prop.params['CN'],'Name: mit; Zeichen')
        self.assertEqual(prop.value,'mailto:x@example.test')
    def test_date_end_exclusive_and_default_day(self):
        result=self.expand('UID:one\nDTSTART;VALUE=DATE:20260328\nDTEND;VALUE=DATE:20260330',
            'UID:two\nDTSTART;VALUE=DATE:20260310')
        self.assertEqual([b.all_day for b in result.blocks],[True,True])
        self.assertEqual([int((utc(b.end)-utc(b.start)).total_seconds()/3600) for b in result.blocks],[24,47])
    def test_nominal_days_and_exact_hours(self):
        result=self.expand('UID:days\nDTSTART;TZID=Europe/Berlin:20260328T120000\nDURATION:P1D',
            'UID:hours\nDTSTART;TZID=Europe/Berlin:20260329T013000\nDURATION:PT2H')
        self.assertEqual(result.blocks[0].end.hour,12)
        self.assertEqual(int((utc(result.blocks[0].end)-utc(result.blocks[0].start)).total_seconds()/3600),23)
        self.assertEqual(result.blocks[1].end.hour,4)
        self.assertEqual(int((utc(result.blocks[1].end)-utc(result.blocks[1].start)).total_seconds()/3600),2)
    def test_exact_dtend_duration_repeats_physically(self):
        result=self.expand('UID:exact\nDTSTART;TZID=Europe/Berlin:20260328T120000\nDTEND;TZID=Europe/Berlin:20260329T120000\nRRULE:FREQ=DAILY;COUNT=2')
        self.assertEqual([b.end.hour for b in result.blocks],[12,11])
    def test_daily_count_skips_nonexistent_clock(self):
        result=self.expand('UID:dst\nDTSTART;TZID=Europe/Berlin:20260327T023000\nDURATION:PT30M\nRRULE:FREQ=DAILY;COUNT=3')
        self.assertFalse(result.issues)
        self.assertEqual([b.start.day for b in result.blocks],[27,28,30])
    def test_rule_rdate_union_and_exdate(self):
        result=self.expand('UID:union\nDTSTART:20260310T090000Z\nDURATION:PT30M\nRRULE:FREQ=DAILY;COUNT=3\nRDATE:20260312T090000Z,20260315T090000Z\nEXDATE:20260311T090000Z')
        self.assertEqual([b.start.day for b in result.blocks],[10,12,15])
    def test_until_inclusive_utc(self):
        result=self.expand('UID:until\nDTSTART;TZID=Europe/Berlin:20260310T090000\nDURATION:PT30M\nRRULE:FREQ=DAILY;UNTIL=20260312T080000Z')
        self.assertEqual([b.start.day for b in result.blocks],[10,11,12])
    def test_moved_cancelled_and_transparent_exceptions(self):
        result=self.expand('UID:series\nDTSTART:20260310T090000Z\nDURATION:PT30M\nRRULE:FREQ=DAILY;COUNT=4',
            'UID:series\nRECURRENCE-ID:20260311T090000Z\nDTSTART:20260311T120000Z\nDURATION:PT1H\nSUMMARY:Verschoben',
            'UID:series\nRECURRENCE-ID:20260312T090000Z\nSTATUS:CANCELLED',
            'UID:series\nRECURRENCE-ID:20260313T090000Z\nDTSTART:20260313T090000Z\nDURATION:PT30M\nTRANSP:TRANSPARENT')
        self.assertFalse(result.issues)
        self.assertEqual([(b.start.day,b.start.hour) for b in result.blocks],[(10,9),(11,12)])
    def test_moved_into_window_from_old_instance(self):
        result=self.expand('UID:move\nDTSTART:20260101T090000Z\nDURATION:PT1H\nRRULE:FREQ=DAILY;COUNT=2',
            'UID:move\nRECURRENCE-ID:20260102T090000Z\nDTSTART:20260315T090000Z\nDURATION:PT1H')
        self.assertEqual([b.start.day for b in result.blocks],[15])
    def test_revision_and_master_cancellation(self):
        result=self.expand('UID:revision\nDTSTART:20260310T090000Z\nDURATION:PT1H\nSEQUENCE:1',
            'UID:revision\nDTSTART:20260310T110000Z\nDURATION:PT1H\nSEQUENCE:2')
        self.assertEqual(result.blocks[0].start.hour,11)
        self.assertTrue(result.issues)
        cancelled=self.expand('UID:revision\nDTSTART:20260310T090000Z\nDURATION:PT1H\nSEQUENCE:1',
            'UID:revision\nSEQUENCE:2\nSTATUS:CANCELLED')
        self.assertFalse(cancelled.blocks)
    def test_transparent_and_zero_duration(self):
        result=self.expand('UID:free\nDTSTART:20260310T090000Z\nDURATION:PT1H\nTRANSP:TRANSPARENT',
            'UID:instant\nDTSTART:20260310T090000Z')
        self.assertFalse(result.blocks)
    def test_clipping_query_keeps_spanning_blocks(self):
        result=self.expand('UID:long\nDTSTART:20260228T090000Z\nDURATION:P3D\nRRULE:FREQ=WEEKLY;COUNT=1')
        self.assertEqual(len(result.blocks),1)
        # Identische Zeitzonenobjekte dürfen UTC-Vergleich nicht umgehen.
        with self.assertRaises(ValueError): ics.expand(self.parse(),self.end,self.start)
    def test_unsupported_visible_other_events_survive(self):
        result=self.expand('UID:unsupported\nDTSTART:20260310T090000Z\nDURATION:PT1H\nRRULE:FREQ=HOURLY',
            'UID:badzone\nDTSTART;TZID=Unavailable/Zone:20260310T090000\nDURATION:PT1H',
            'UID:good\nDTSTART:20260311T090000Z\nDURATION:PT1H')
        self.assertEqual([b.start.day for b in result.blocks],[10,11])
        self.assertEqual(len(result.issues),2)
        self.assertIn('Weitere Serienvorkommen',result.issues[0][1])
    def test_invalid_event_and_file(self):
        result=self.expand('UID:bad\nDTSTART:20260310T090000Z\nDTEND:20260310T080000Z',
            'UID:both\nDTSTART:20260310T090000Z\nDTEND:20260310T100000Z\nDURATION:PT1H',
            'UID:range\nRECURRENCE-ID;RANGE=THISANDFUTURE:20260310T090000Z\nDTSTART:20260310T090000Z\nDURATION:PT1H')
        self.assertFalse(result.blocks);self.assertEqual(len(result.issues),3)
        for text in ('','BEGIN:VEVENT\nEND:VEVENT','BEGIN:VCALENDAR\nEND:VEVENT','BEGIN:VCALENDAR'):
            with self.assertRaises(ValueError): ics.parse_calendar(text,self.zone)
    def test_resolver_injection_and_no_mutation(self):
        calls=[]
        def resolver(name): calls.append(name);return self.zone
        calendar=self.parse('UID:custom\nDTSTART;TZID=Custom:20260310T090000\nDURATION:PT1H',resolver=resolver)
        before=calendar
        first=ics.expand(calendar,self.start,self.end);second=ics.expand(calendar,self.start,self.end)
        self.assertEqual(first,second);self.assertEqual(calendar,before);self.assertEqual(calls,['Custom'])

    def test_all_day_weekly_monthly_and_yearly(self):
        result=self.expand('UID:all\nDTSTART;VALUE=DATE:20260302\nRRULE:FREQ=WEEKLY;COUNT=3;BYDAY=MO',
            'UID:month\nDTSTART:20260131T090000Z\nDURATION:PT1H\nRRULE:FREQ=MONTHLY;COUNT=3',
            'UID:year\nDTSTART:20240310T090000Z\nDURATION:PT1H\nRRULE:FREQ=YEARLY')
        self.assertFalse(result.issues)
        self.assertEqual([b.start.day for b in result.blocks],[2,9,10,16,31])
    def test_fold_uses_first_occurrence(self):
        calendar=self.parse('UID:fold\nDTSTART;TZID=Europe/Berlin:20261025T023000\nDURATION:PT1H')
        result=ics.expand(calendar,datetime(2026,10,25,tzinfo=self.zone),datetime(2026,10,26,tzinfo=self.zone))
        self.assertEqual(result.blocks[0].start.fold,0)
        self.assertEqual(result.blocks[0].start.utcoffset(),timedelta(hours=2))
        self.assertEqual(result.blocks[0].end.fold,1)
    def test_invalid_until_and_unbounded_duration_visible(self):
        result=self.expand('UID:until\nDTSTART;TZID=Europe/Berlin:20260310T090000\nDURATION:PT1H\nRRULE:FREQ=DAILY;UNTIL=20260312T090000',
            'UID:huge\nDTSTART:20260310T090000Z\nDURATION:P999999999999D')
        self.assertEqual(len(result.issues),2)
        self.assertEqual(len(result.blocks),1)
        for value in ('P','PT','P1DT','-P1D','P1W1D'):
            with self.assertRaises(ValueError): ics.duration(value,False)

if __name__=='__main__': unittest.main()
