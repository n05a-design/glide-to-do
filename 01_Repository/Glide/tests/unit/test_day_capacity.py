# SPDX-License-Identifier: MPL-2.0
"""Prüfungen für die erweiterte Tageskapazitäts- und Belastungsanalyse (WA-12 / D57)."""
import copy
from datetime import datetime, timezone
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import planning as p
import day_relief as relief
from occupied_time import Block

UTC = timezone.utc
DAY = "2026-11-12"
NEXT = "2026-11-13"


def task(identity, minutes=60, day=DAY, due="2026-11-20", done=False):
    return dict(id=identity, text=identity, planned_date=day, planned_time="09:00",
                estimated_minutes=minutes, due=due, done=done, kind="task")


class DayCapacityAnalysisTest(unittest.TestCase):
    def test_planned_effort_and_free_capacity(self):
        items = [task("t1", 90), task("t2", 60)]
        summary = p.summarize(items, 240, lambda item: True)
        analysis = p.capacity_analysis(summary)

        self.assertEqual(analysis["task_minutes"], 150)
        self.assertEqual(analysis["estimated_count"], 2)
        self.assertEqual(analysis["without_estimate_count"], 0)
        self.assertEqual(analysis["capacity_minutes"], 240)
        self.assertTrue(analysis["has_capacity"])
        self.assertFalse(analysis["is_overloaded"])
        self.assertEqual(analysis["overload_minutes"], 0)
        self.assertEqual(analysis["remaining_minutes"], 90)
        self.assertEqual(analysis["free_minutes"], 90)
        self.assertIn("Aufwand 2 h 30 min", analysis["summary_text"])
        self.assertIn("frei 1 h 30 min", analysis["summary_text"])

    def test_overload_reasons_and_calculation(self):
        # 300 Minuten Aufgaben bei 180 Minuten Kapazität -> 120 Minuten überplant
        items = [task("t1", 180), task("t2", 120)]
        summary = p.summarize(items, 180, lambda item: True)
        analysis = p.capacity_analysis(summary)

        self.assertEqual(analysis["task_minutes"], 300)
        self.assertTrue(analysis["is_overloaded"])
        self.assertEqual(analysis["overload_minutes"], 120)
        self.assertEqual(analysis["remaining_minutes"], -120)
        self.assertGreater(len(analysis["overload_reasons"]), 0)
        self.assertTrue(any("übersteigt nutzbare Kapazität" in r for r in analysis["overload_reasons"]))
        self.assertIn("2 h überplant", analysis["summary_text"])

    def test_unknown_estimates_are_never_treated_as_zero(self):
        items = [task("t1", 60), task("t2", None), task("t3", 0), task("t4", -30), task("t5", "invalid")]
        summary = p.summarize(items, 120, lambda item: True)
        analysis = p.capacity_analysis(summary)

        self.assertEqual(analysis["task_minutes"], 60)
        self.assertEqual(analysis["estimated_count"], 1)
        self.assertEqual(analysis["without_estimate_count"], 4)
        # 4 Aufgaben ohne Schätzung müssen ausdrücklich ausgewiesen werden
        self.assertIn("4 ohne Schätzung", analysis["summary_text"])
        self.assertTrue(any("4 Aufgaben ohne Aufwandsschätzung" in r for r in analysis["overload_reasons"]))

    def test_no_fictitious_capacity_when_undefined(self):
        # Wenn keine Kapazität festgelegt ist, darf keine freie Zeit erfunden werden
        items = [task("t1", 120)]
        summary = p.summarize(items, 0, lambda item: True)
        analysis = p.capacity_analysis(summary)

        self.assertFalse(analysis["has_capacity"])
        self.assertIsNone(analysis["remaining_minutes"])
        self.assertIsNone(analysis["free_minutes"])
        self.assertFalse(analysis["is_overloaded"])
        self.assertIn("Kapazität nicht festgelegt", analysis["summary_text"])
        self.assertNotIn("frei", analysis["summary_text"])

    def test_calendar_occupancy_impact_on_net_capacity(self):
        items = [task("t1", 120)]
        busy_blocks = (
            Block(datetime(2026, 11, 12, 10, 0, tzinfo=UTC), datetime(2026, 11, 12, 12, 0, tzinfo=UTC)),  # 120 min
        )
        summary = relief.day_summary(items, DAY, 300, busy_blocks, UTC, lambda item: True)
        analysis = relief.capacity_analysis(summary)

        self.assertEqual(analysis["capacity_minutes"], 300)
        self.assertEqual(analysis["occupied_minutes"], 120)
        self.assertEqual(analysis["net_capacity"], 180)
        self.assertEqual(analysis["task_minutes"], 120)
        self.assertEqual(analysis["remaining_minutes"], 60)
        self.assertFalse(analysis["is_overloaded"])
        self.assertIn("Kalender 2 h", analysis["summary_text"])
        self.assertIn("frei 1 h", analysis["summary_text"])

    def test_all_day_calendar_occupancy(self):
        items = [task("t1", 30)]
        all_day_block = (
            Block(datetime(2026, 11, 12, tzinfo=UTC), datetime(2026, 11, 13, tzinfo=UTC), all_day=True),
        )
        summary = relief.day_summary(items, DAY, 240, all_day_block, UTC, lambda item: True)
        analysis = relief.capacity_analysis(summary)

        self.assertTrue(analysis["occupied_all_day"])
        self.assertEqual(analysis["net_capacity"], 0)
        self.assertTrue(analysis["is_overloaded"])
        self.assertEqual(analysis["overload_minutes"], 30)
        self.assertTrue(any("ganztägig" in r for r in analysis["overload_reasons"]))
        self.assertIn("ganztägig belegt", analysis["summary_text"])

    def test_relief_summary_text_formatting(self):
        items = [task("t1", 90), task("t2", None)]
        summary = relief.day_summary(items, DAY, 180, (), UTC, lambda item: True)
        text = relief.relief_summary_text(summary)

        self.assertTrue(text.startswith("2 Aufgaben"))
        self.assertIn("Aufwand 1 h 30 min", text)
        self.assertIn("frei 1 h 30 min", text)
        self.assertIn("1 ohne Schätzung", text)

    def test_due_date_preservation_in_relief_plan(self):
        items = [task("t1", 60, due="2026-11-25"), task("t2", 90, due="2026-11-30")]
        original = copy.deepcopy(items)
        options = dict(capacity=lambda day: 240, blocks=lambda day: (), zone=UTC, schedulable=lambda i: True)
        plan = relief.propose(items, ["t1"], NEXT, **options)

        # Fälligkeiten dürfen unter keinen Umständen mutiert werden
        self.assertEqual(items, original)
        self.assertEqual(plan.moves[0].identity, "t1")
        self.assertEqual(plan.moves[0].source, DAY)
        self.assertEqual(plan.moves[0].target, NEXT)

        # Validierung liefert genaue Zielzuordnung
        valid_moves = relief.validate(plan, items, lambda i: True)
        self.assertEqual(valid_moves, (("t1", NEXT, "09:00"),))

    def test_overlapping_calendar_blocks_deduplication(self):
        # Zwei überlappende Blöcke: 10:00-11:30 (90 min) und 11:00-12:00 (60 min)
        # Gesamte belegte Zeit darf nur 120 min sein, nicht 150 min!
        items = [task("t1", 60)]
        busy_blocks = (
            Block(datetime(2026, 11, 12, 10, 0, tzinfo=UTC), datetime(2026, 11, 12, 11, 30, tzinfo=UTC)),
            Block(datetime(2026, 11, 12, 11, 0, tzinfo=UTC), datetime(2026, 11, 12, 12, 0, tzinfo=UTC)),
        )
        summary = relief.day_summary(items, DAY, 240, busy_blocks, UTC, lambda item: True)
        analysis = relief.capacity_analysis(summary)

        self.assertEqual(analysis["occupied_minutes"], 120)
        self.assertEqual(analysis["net_capacity"], 120)  # 240 - 120
        self.assertEqual(analysis["remaining_minutes"], 60)  # 120 - 60
        self.assertFalse(analysis["is_overloaded"])

    def test_calendar_error_or_loading_state(self):
        items = [task("t1", 60)]
        error_summary = {
            "items": 1,
            "minutes": 60,
            "without_estimate": 0,
            "calendar_state": "error",
            "calendar_message": "Kalenderdatei nicht lesbar",
        }
        text = relief.relief_summary_text(error_summary)
        self.assertIn("Freie Zeit unbekannt", text)
        self.assertIn("Kalenderdatei nicht lesbar", text)

    def test_relief_validation_rejects_modified_state(self):
        # Wenn sich der Aufgabenbestand zwischen Planung und Übernahme ändert,
        # muss die Validierung veraltete Züge sicher abweisen.
        items = [task("t1", 60), task("t2", 90)]
        options = dict(capacity=lambda day: 240, blocks=lambda day: (), zone=UTC, schedulable=lambda i: True)
        plan = relief.propose(items, ["t1"], NEXT, **options)

        # Simuliere geänderten Bestand: t1 wurde zwischenzeitlich erledigt oder gelöscht
        modified_items = [task("t2", 90)]
        with self.assertRaises(ValueError):
            relief.validate(plan, modified_items, lambda i: True)

    def test_multiple_tasks_with_same_due_date(self):
        # Mehrere Aufgaben mit exakt gleicher Fälligkeit
        items = [task("t1", 30, due="2026-11-20"), task("t2", 45, due="2026-11-20"), task("t3", 60, due="2026-11-20")]
        summary = p.summarize(items, 180, lambda item: True)
        analysis = p.capacity_analysis(summary)

        self.assertEqual(analysis["task_minutes"], 135)
        self.assertEqual(analysis["estimated_count"], 3)
        self.assertEqual(analysis["remaining_minutes"], 45)

        # Entlastung einer Aufgabe lässt Fälligkeiten aller Aufgaben intakt
        options = dict(capacity=lambda day: 180, blocks=lambda day: (), zone=UTC, schedulable=lambda i: True)
        plan = relief.propose(items, ["t1", "t2"], NEXT, **options)
        valid = relief.validate(plan, items, lambda i: True)
        self.assertEqual(len(valid), 2)
        # Ursprüngliche Fälligkeiten in items unverändert
        self.assertTrue(all(item["due"] == "2026-11-20" for item in items))


if __name__ == "__main__":
    unittest.main()
