"""FP-02/1: unabhängige Referenztabellen, Formularvertrag und Vorschau."""
import copy
from datetime import date
import json
from pathlib import Path
import sys
import unittest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'src/glide'))
import repeat_rules as r


class Serien(unittest.TestCase):
    def test_30_reference_rules_24_dates_each(self):
        table = json.loads((REPO / 'tests/fixtures/wiederholungsregeln_fp02.json').read_text(encoding='utf-8'))
        self.assertEqual(len(table['regeln']), 30)
        for example in table['regeln']:
            with self.subTest(rule=example['rrule'], start=example['start']):
                rule = r.normalize(dict(art=r.SERIES, rrule=example['rrule'], start=example['start']))
                self.assertIsNotNone(rule)
                current = date.fromisoformat(example['start'])
                actual = []
                for _ in range(24):
                    current = r.next_date(rule, current)
                    actual.append(current.isoformat())
                self.assertEqual(actual, example['expected'])

    def test_form_and_plain_text_roundtrip(self):
        for _label, kind in r.SERIES_CHOICES:
            for interval in (1, 3, 365):
                for position in (1, 5, -1):
                    rule = r.from_series_fields(kind, interval, [0, 3], position, 1)
                    fields = r.form_values(rule)
                    self.assertEqual(r.from_series_fields(fields['art'], fields['abstand'],
                        fields['tage'], fields['position'], fields['wochentag']), rule)
                    self.assertEqual(r.parse_series_text(r.describe_series(rule)), rule)

    def test_unknown_parts_do_not_degrade(self):
        for text in ('FREQ=DAILY', 'FREQ=WEEKLY', 'FREQ=WEEKLY;BYDAY=2MO',
                     'FREQ=MONTHLY;BYDAY=-2MO', 'FREQ=MONTHLY;COUNT=3',
                     'FREQ=YEARLY;UNTIL=20300101', 'FREQ=MONTHLY;INTERVAL=366',
                     'FREQ=MONTHLY;BYMONTHDAY=15', 'FREQ=MONTHLY;BYSETPOS=-1',
                     'FREQ=MONTHLY;FREQ=YEARLY', 'FREQ=MONTHLY;WKST=SU'):
            self.assertIsNone(r.normalize(dict(art=r.SERIES, rrule=text)), text)
        self.assertIsNone(r.normalize(dict(art=r.SERIES, rrule='FREQ=MONTHLY', future=True)))

    def test_invalid_form_fields(self):
        for interval in (True, 0, 366, '1.5', '-2', '²', '1' * 300):
            with self.assertRaises(ValueError):
                r.from_series_fields('serie_monat', interval)
        for days in ([], [True], [7], ['0']):
            with self.assertRaises(ValueError):
                r.from_series_fields('serie_woche', 2, days)
        for position in (True, 0, -2, 6):
            with self.assertRaises(ValueError):
                r.from_series_fields('serie_position', 1, position=position)

    def test_preview_is_bounded_pure_and_end_inclusive(self):
        rule = dict(art=r.SERIES, rrule='FREQ=MONTHLY;BYMONTHDAY=-1', start='2026-01-31', ende='2026-03-31')
        before = copy.deepcopy(rule)
        self.assertEqual(r.preview(rule, '2026-01-31'), ['2026-02-28', '2026-03-31'])
        self.assertEqual(rule, before)
        self.assertEqual(r.preview(rule, None), [])
        for count in (0, 6, True):
            with self.assertRaises(ValueError):
                r.preview(rule, '2026-01-31', count)
        self.assertEqual(r.preview(rule, '9999-12-31'), [])

    def test_month_end_and_leap_year_are_explicit(self):
        self.assertEqual(r.preview({'art':r.MONTHLY}, '2026-01-31', 2), ['2026-02-28','2026-03-31'])
        self.assertEqual(r.preview(r.from_series_fields('serie_monat',1), '2026-01-31',2), ['2026-03-31','2026-05-31'])
        self.assertEqual(r.preview(r.from_series_fields('serie_jahr',1), '2028-02-29',2), ['2032-02-29','2036-02-29'])

    def test_last_workday_is_monday_to_friday_without_holidays(self):
        rule = r.from_series_fields('serie_werktag', 1)
        self.assertEqual(r.preview(rule, '2026-12-01', 2), ['2026-12-31','2027-01-29'])

    def test_week_anchor_and_dst_date_boundaries(self):
        rule = dict(art=r.SERIES,rrule='FREQ=WEEKLY;INTERVAL=2;BYDAY=MO,TH',start='2026-03-16')
        self.assertEqual(r.preview(rule,'2026-03-19'),
                         ['2026-03-30','2026-04-02','2026-04-13','2026-04-16','2026-04-27'])
        rule['start']='2026-10-12'
        self.assertEqual(r.preview(rule,'2026-10-15',2), ['2026-10-26','2026-10-29'])

    def test_stored_series_gate_in_nested_and_trashed_items(self):
        for field in ('lists','trash'):
            data={field:[{'items':[{'children':[{'repeat':r.from_series_fields('serie_monat',3)}]}]}]}
            with self.assertRaises(ValueError):
                r.check_stored_series(data,25)
            r.check_stored_series(data,26)
            data[field][0]['items'][0]['children'][0]['repeat']['future']=1
            with self.assertRaises(ValueError):
                r.check_stored_series(data,26)


if __name__ == '__main__':
    unittest.main()
