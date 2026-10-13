"""Übliche Serien und ausdrücklich abgewiesene Regelteile, ohne Tk."""
from datetime import date
import unittest
from ics_recurrence import dates, parse_rule, RuleError


def series(start, rule, through="2027-12-31", after=None, **kw):
    return [d.isoformat() for d in dates(date.fromisoformat(start), rule, date.fromisoformat(through),
                                      after=date.fromisoformat(after) if after else None, **kw)]


class RecurrenceTests(unittest.TestCase):
    def test_daily_count_interval_and_inclusive_until(self):
        self.assertEqual(series("2026-10-10", "FREQ=DAILY;INTERVAL=2;COUNT=3"),
                         ["2026-10-10", "2026-10-12", "2026-10-14"])
        self.assertEqual(series("2026-10-10", "FREQ=DAILY;UNTIL=20261012"),
                         ["2026-10-10", "2026-10-11", "2026-10-12"])

    def test_weekly_multiple_days_and_week_start_interval(self):
        self.assertEqual(series("1997-08-05", "FREQ=WEEKLY;INTERVAL=2;COUNT=4;BYDAY=TU,SU;WKST=MO"),
                         ["1997-08-05", "1997-08-10", "1997-08-19", "1997-08-24"])
        self.assertEqual(series("1997-08-05", "FREQ=WEEKLY;INTERVAL=2;COUNT=4;BYDAY=TU,SU;WKST=SU"),
                         ["1997-08-05", "1997-08-17", "1997-08-19", "1997-08-31"])

    def test_month_end_skips_invalid_dates_without_consuming_count(self):
        self.assertEqual(series("2026-01-31", "FREQ=MONTHLY;COUNT=4"),
                         ["2026-01-31", "2026-03-31", "2026-05-31", "2026-07-31"])
        self.assertEqual(series("2026-01-31", "FREQ=MONTHLY;BYMONTHDAY=-1;COUNT=3"),
                         ["2026-01-31", "2026-02-28", "2026-03-31"])

    def test_monthly_first_monday_last_friday_and_last_workday(self):
        self.assertEqual(series("2026-10-05", "FREQ=MONTHLY;BYDAY=1MO;COUNT=3"),
                         ["2026-10-05", "2026-11-02", "2026-12-07"])
        self.assertEqual(series("2026-10-30", "FREQ=MONTHLY;BYDAY=-1FR;COUNT=3"),
                         ["2026-10-30", "2026-11-27", "2026-12-25"])
        self.assertEqual(series("2026-10-30", "FREQ=MONTHLY;BYDAY=MO,TU,WE,TH,FR;BYSETPOS=-1;COUNT=3"),
                         ["2026-10-30", "2026-11-30", "2026-12-31"])

    def test_leap_day_yearly_and_multiple_months(self):
        self.assertEqual(series("2024-02-29", "FREQ=YEARLY;COUNT=3", "2035-01-01"),
                         ["2024-02-29", "2028-02-29", "2032-02-29"])
        self.assertEqual(series("2026-01-10", "FREQ=YEARLY;BYMONTH=1,6;COUNT=4"),
                         ["2026-01-10", "2026-06-10", "2027-01-10", "2027-06-10"])

    def test_yearly_ordinal_with_and_without_month(self):
        self.assertEqual(series("2026-03-29", "FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU;COUNT=2"),
                         ["2026-03-29", "2027-03-28"])
        self.assertEqual(series("2026-01-05", "FREQ=YEARLY;BYDAY=1MO;COUNT=2"),
                         ["2026-01-05", "2027-01-04"])

    def test_filters_intersect_and_positions_apply_within_period(self):
        self.assertEqual(series("2026-10-13", "FREQ=MONTHLY;BYDAY=TU;BYMONTHDAY=10,11,12,13,14;COUNT=3"),
                         ["2026-10-13", "2026-11-10", "2027-01-12"])
        self.assertEqual(series("2026-10-06", "FREQ=MONTHLY;BYDAY=TU;BYSETPOS=1,-1;COUNT=4"),
                         ["2026-10-06", "2026-10-27", "2026-11-03", "2026-11-24"])

    def test_count_includes_previous_dates_but_invalid_local_time_does_not(self):
        self.assertEqual(series("2026-03-27", "FREQ=DAILY;COUNT=4", after="2026-03-29",
                                valid=lambda d: d != date(2026, 3, 29)),
                         ["2026-03-30", "2026-03-31"])
        self.assertEqual(series("2026-10-10", "FREQ=DAILY;COUNT=3", after="2026-10-12"), ["2026-10-12"])

    def test_no_count_can_seek_to_modern_window(self):
        self.assertEqual(series("1900-01-01", "FREQ=DAILY", "2026-10-12", "2026-10-10"),
                         ["2026-10-10", "2026-10-11", "2026-10-12"])
        self.assertEqual(series("1900-01-31", "FREQ=MONTHLY", "2026-12-31", "2026-10-01"),
                         ["2026-10-31", "2026-12-31"])

    def test_unhandled_parts_and_invalid_combinations_raise_visible_reason(self):
        for text in ("FREQ=HOURLY", "FREQ=DAILY;BYHOUR=8", "FREQ=DAILY;COUNT=0", "FREQ=DAILY;INTERVAL=0",
                     "FREQ=DAILY;COUNT=2;UNTIL=20261012", "FREQ=MONTHLY;BYDAY=0MO", "FREQ=WEEKLY;BYDAY=1MO",
                     "FREQ=WEEKLY;BYMONTHDAY=1", "FREQ=MONTHLY;BYSETPOS=-1", "FREQ=MONTHLY;BYMONTH=13",
                     "FREQ=DAILY;FREQ=DAILY", "FREQ=DAILY;UNTIL=20260230", "FREQ=DAILY;UNTIL=20261010T250000Z"):
            with self.subTest(text=text):
                with self.assertRaises(RuleError): parse_rule(text)


if __name__ == "__main__":
    unittest.main()
