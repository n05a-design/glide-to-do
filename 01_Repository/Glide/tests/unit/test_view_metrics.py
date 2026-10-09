"""P09b: Datumssemantik, Tageswechsel und strukturierte Kennzahlen ohne Tk."""
from datetime import date, datetime, timedelta
import random
import sys
from pathlib import Path
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import view_metrics as metrics


def walk(items):
    for item in items:
        yield item
        yield from walk(item.get("children", []))


def normalize(value):
    if not value or not isinstance(value, str):
        return None
    parsed = metrics.parsed_date(value.strip())
    return parsed.strftime("%Y-%m-%d") if parsed else None


def summary(items, today=None):
    return metrics.summarize(items, walk=walk, schedulable=lambda i: i.get("kind") != "group",
                             normalize_due=normalize, regular_labels=["own"], today=today)


class MetricsTest(unittest.TestCase):
    def test_date_compatibility(self):
        values = ["2026-1-2", "2024-02-29", "2026-02-29", "2026-13-01", "garbage",
                  "2026-01-01 ", "0001-01-01", "9999-12-31", ""]
        for value in values:
            try:
                expected = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                expected = None
            self.assertEqual(metrics.parsed_date(value), expected)
            self.assertEqual(metrics.display_date(value), expected.strftime("%d.%m.%Y") if expected else "")

    def test_date_cache_bounded_and_shared(self):
        metrics.parsed_date.cache_clear()
        with patch.object(metrics, "datetime", wraps=datetime) as parser:
            for _ in range(10):
                metrics.parsed_date("2026-10-05")
                metrics.display_date("2026-10-05")
                metrics.due_status({"due": "2026-10-05"}, date(2026, 10, 5))
            self.assertEqual(parser.strptime.call_count, 1)
        for number in range(4100):
            metrics.parsed_date(f"invalid-{number}")
        self.assertEqual(metrics.parsed_date.cache_info().currsize, 4096)

    def test_status_boundaries_and_day_change(self):
        today = date(2026, 10, 5)
        for delta, expected in [(-1, "overdue"), (0, "today"), (1, "soon"), (2, "soon"), (3, "future")]:
            item = {"due": (today + timedelta(days=delta)).isoformat()}
            self.assertEqual(metrics.due_status(item, today), expected)
            item["done"] = True
            self.assertEqual(metrics.due_status(item, today), "future")
        item = {"due": today.isoformat()}
        self.assertEqual(metrics.due_status(item, today + timedelta(days=1)), "overdue")
        self.assertEqual(metrics.due_status({"due": "bad", "done": True}, today), "")

    def test_summary_container_children_labels_and_nearest(self):
        children = [{"due": "2026-10-04", "labels": ["own", "system"]},
                    {"due": "2026-10-06"}, {"due": "2026-10-05", "done": True}]
        value = summary([{"kind": "group", "due": "2026-10-03", "children": children}], date(2026, 10, 5))
        self.assertEqual(value.stats, (3, 1, 1))
        self.assertEqual(value.next_due, "2026-10-06")
        self.assertEqual(value.labels, frozenset(["own"]))

    def test_fresh_after_object_replacement(self):
        self.assertEqual(summary([{"done": True}]).stats, (1, 1, 0))
        self.assertEqual(summary([{"done": False}]).stats, (1, 0, 0))

    def test_one_visit_and_read_only(self):
        import copy
        items = [{"due": "2026-10-05", "children": [{"done": True}]}]
        before = copy.deepcopy(items)
        calls = []
        def counted(values):
            for item in walk(values):
                calls.append(item)
                yield item
        metrics.summarize(items, walk=counted, schedulable=lambda i: True, normalize_due=normalize)
        self.assertEqual(len(calls), 2)
        self.assertEqual(items, before)

    def test_differential(self):
        randomizer = random.Random(33310)
        today = date(2026, 10, 5)
        for _ in range(200):
            items = [{"kind": randomizer.choice(["task", "group"]),
                      "done": randomizer.choice([True, False]),
                      "due": randomizer.choice([None, "bad", "2026-10-04", "2026-10-06"])} for _ in range(30)]
            tasks = [item for item in items if item["kind"] != "group"]
            total = len(tasks)
            done = sum(bool(i["done"]) for i in tasks)
            overdue = sum(not i["done"] and i["due"] == "2026-10-04" for i in tasks)
            self.assertEqual(summary(items, today).stats, (total, done, overdue))

    def test_progress_only_skips_details(self):
        with patch.object(metrics, "parsed_date", wraps=metrics.parsed_date):
            value = metrics.summarize([{"done": True, "labels": ["own"]}], walk=walk,
                                     schedulable=lambda i: True,
                                     normalize_due=lambda v: self.fail("unneeded normalization"),
                                     include_details=False)
            self.assertEqual(value.stats, (1, 1, 0))
            self.assertFalse(value.labels)

    def test_line_height_current_padding(self):
        self.assertEqual(metrics.line_height(2, 18, "3.0", 2), 46)
        self.assertEqual(metrics.line_height(1, 20, "", 2), 24)


if __name__ == "__main__":
    unittest.main()
