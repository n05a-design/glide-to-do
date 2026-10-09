"""Planungsinvarianten, Datumsgrenzen und Vorschau ohne Oberfläche."""
import copy
from datetime import date
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import planning as p


def task(identity, **values):
    return dict(id=identity, kind="task", planned_date=None, **values)


class PlanningTest(unittest.TestCase):
    def test_relative_days_at_week_and_year_boundaries(self):
        self.assertEqual(p.target_day("tomorrow", date(2026, 12, 31)), "2027-01-01")
        self.assertEqual(p.target_day("next_week", date(2026, 12, 28)), "2027-01-04")
        self.assertEqual(p.target_day("next_week", date(2026, 12, 27), "sunday"), "2027-01-03")
        self.assertEqual(p.target_day("next_week", date(2026, 12, 26), "sunday"), "2026-12-27")
        with self.assertRaises(ValueError):
            p.target_day("typo", date(2026, 10, 6))

    def test_weekend_is_saturday_and_stays_today_on_weekend(self):
        self.assertEqual(p.target_day("weekend", date(2026, 10, 6)), "2026-10-10")
        for day in (10, 11):
            self.assertEqual(p.target_day("weekend", date(2026, 10, day)), f"2026-10-{day}")
        self.assertIsNone(p.target_day("unplan", date(2026, 10, 6)))

    def test_day_profile_fallback_and_zero_are_distinct(self):
        settings = dict(daily_capacity_minutes=240, daily_capacity_by_weekday=[0, 90, None, True, -10, 99999, 60])
        self.assertEqual(p.capacity_for(settings, "2026-10-05"), 0)
        self.assertEqual(p.capacity_for(settings, "2026-10-06"), 90)
        self.assertEqual(p.capacity_for(settings, "2026-10-07"), 240)
        self.assertEqual(p.capacity_for(settings, "2026-10-08"), 240)
        self.assertEqual(p.capacity_for(settings, "2026-10-09"), 0)
        self.assertEqual(p.capacity_for(settings, "2026-10-10"), 1440)
        self.assertEqual(p.capacity_for(settings, "invalid"), 240)

    def test_completed_estimates_stay_in_balance(self):
        items = [task("a", estimated_minutes=60), task("b", estimated_minutes=90, done=True),
                 dict(id="group", kind="group", estimated_minutes=900), None]
        summary = p.summarize(items, 120, lambda x: x.get("kind") == "task")
        self.assertEqual((summary["items"], summary["minutes"], summary["done_minutes"], summary["remaining"]),
                         (2, 150, 90, -30))
        self.assertEqual(p.available_text(summary), "30 min überplant")

    def test_missing_estimates_and_unknown_capacity_are_never_guessed(self):
        items = [task(str(i), estimated_minutes=value) for i, value in enumerate((None, True, 0, -1, "30", 30))]
        summary = p.summarize(items, 0, lambda x: True)
        self.assertEqual(summary["minutes"], 30)
        self.assertEqual(summary["without_estimate"], 5)
        self.assertIsNone(summary["remaining"])
        self.assertEqual(p.available_text(summary), "Kapazität nicht festgelegt · 5 ohne Schätzung")

    def test_projection_deduplicates_and_preserves_every_field(self):
        a, b = task("a", estimated_minutes=30, due="2026-10-01", planned_time="09:00"), task("b", estimated_minutes=60)
        a["planned_date"] = "2026-10-06"
        old = copy.deepcopy([a, b])
        projected = p.projected_items([a, b], [a, b, b], "2026-10-06")
        self.assertEqual(len(projected), 2)
        self.assertEqual(p.summarize(projected, 120, lambda x: True)["remaining"], 30)
        self.assertEqual([a, b], old)

    def test_noop_invalid_date_and_unplan(self):
        item = task("a", due="2026-10-01", planned_time="09:00")
        self.assertEqual(p.changed_ids([item, item], "2026-10-06"), ["a"])
        self.assertEqual(p.changed_ids([item], None), [])
        for invalid in ("2026-02-30", "20261006", "bad", 123):
            with self.assertRaises(ValueError):
                p.changed_ids([item], invalid)

    def test_empty_day_can_still_have_available_time(self):
        self.assertEqual(p.available_text(p.summarize([], 80, lambda x: True)), "frei 1 h 20 min")
        self.assertEqual(p.available_text(p.summarize([], 0, lambda x: True)), "Kapazität nicht festgelegt")

    def test_sequential_clock_targets_and_missing_estimate(self):
        items = [task("a", estimated_minutes=40), task("b", estimated_minutes=None)]
        before = copy.deepcopy(items)
        self.assertEqual(p.time_assignments(items, "2026-10-07", "09:30"),
                         [("a", "2026-10-07", "09:30"), ("b", "2026-10-07", "10:10")])
        self.assertEqual(items, before)

    def test_clock_clear_preserves_day_for_caller(self):
        self.assertEqual(p.time_assignments([task("a")], "2026-10-07", None), [("a", None, None)])

    def test_clock_rejects_invalid_or_overflowing_assignments(self):
        for clock in ("24:00", "9:00", "10:70", "bad"):
            with self.assertRaises(ValueError):
                p.time_assignments([task("a")], "2026-10-07", clock)
        with self.assertRaises(ValueError):
            p.time_assignments([task("a", estimated_minutes=60)], "2026-10-07", "23:30")

    def test_block_can_end_at_midnight_without_truncation(self):
        self.assertEqual(p.time_assignments([task("a", estimated_minutes=30)], "2026-10-07", "23:30"),
                         [("a", "2026-10-07", "23:30")])


if __name__ == "__main__":
    unittest.main()
