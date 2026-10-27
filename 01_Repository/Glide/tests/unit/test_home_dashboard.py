"""Startseitenprojektion: Originale, Fachgrenzen und begrenzter Aufwand."""
import copy
from datetime import date, datetime
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import home_dashboard as dashboard


TODAY = date(2026, 10, 26)


class PlannedPreviewTests(unittest.TestCase):
    def test_done_entries_do_not_use_any_of_the_five_slots(self):
        entries = [(None, 0, n, {'id': 'source'}, {'id': str(n), 'done': n < 6}) for n in range(14)]
        before = copy.deepcopy(entries)
        preview = dashboard.planned_preview(entries)
        self.assertEqual([row[-1]['id'] for row in preview], ['6', '7', '8', '9', '10'])
        self.assertIs(preview[0], entries[6])
        self.assertEqual(entries, before)

    def test_empty_done_only_and_explicit_limit(self):
        self.assertEqual(dashboard.planned_preview([]), [])
        self.assertEqual(dashboard.planned_preview([(None, 0, 0, {}, {'done': True})]), [])
        entries = [(None, 0, n, {}, {'done': False}) for n in range(4)]
        self.assertEqual(dashboard.planned_preview(iter(entries), 2), entries[:2])
        self.assertEqual(dashboard.planned_preview(entries, 0), [])


def walk(items):
    for item in items:
        yield item
        yield from walk(item.get("children", []))


def normalize_day(value):
    try:
        return date.fromisoformat(value.strip()).isoformat()
    except (AttributeError, TypeError, ValueError):
        return None


def normalize_time(value):
    try:
        return datetime.strptime(value.strip(), "%H:%M").strftime("%H:%M")
    except (AttributeError, TypeError, ValueError):
        return None


def build(entries, today=TODAY, **options):
    settings = dict(walk_items=walk, is_schedulable=lambda item: item.get("kind", "task") == "task",
                    normalize_due=normalize_day, normalize_time=normalize_time,
                    urgency_rank=lambda item: item.get("rank", (3,)), max_focus_rank=2)
    settings.update(options)
    return dashboard.build(entries, today, **settings)


class DashboardTests(unittest.TestCase):
    def test_empty_inventory_and_ranges(self):
        model = build([])
        self.assertEqual(model.summary([], []), dict(total=0, done=0, open=0, overdue=0,
                                                   due_today=0, lists=0, due_lists=[], recent=[]))
        self.assertEqual(model.focus, (None, None))
        self.assertEqual(model.next_scheduled, (None, None))
        self.assertEqual(model.week_overview(0), [])
        self.assertEqual(model.week_overview(-1), [])
        self.assertEqual(len(model.week_overview(14)), 14)
        self.assertEqual(model.label_overview(lambda identity: None), [])

    def test_counts_keep_structure_children_and_exclude_done_from_due(self):
        child = dict(id="child", due="2026-10-26")
        entry = dict(id="list", items=[dict(id="group", kind="group", children=[child]),
                     dict(id="heading", kind="heading", due="2026-10-26"),
                     dict(id="done", done=True, due="2026-10-25"),
                     dict(id="past", due="2026-10-25"), dict(id="invalid", due="2026-02-30")])
        result = build([entry]).summary([entry], [])
        self.assertEqual({key: result[key] for key in ("total", "done", "open", "overdue", "due_today")},
                         dict(total=4, done=1, open=3, overdue=1, due_today=1))
        self.assertIs(result["due_lists"][0][0], entry)
        self.assertEqual(result["due_lists"][0][1], 1)

    def test_summary_keeps_all_lists_and_recent_originals(self):
        active = dict(id="active", items=[dict(id="task")])
        archived = dict(id="archive", archived=True, items=[dict(id="old")])
        recent = [dict(id="archive", edited_at="yesterday"), dict(id="missing", edited_at="today")]
        result = build([active]).summary([active, archived], recent)
        self.assertEqual((result["lists"], result["total"]), (2, 1))
        self.assertEqual(len(result["recent"]), 1)
        self.assertIs(result["recent"][0][0], archived)

    def test_focus_uses_rank_boundary_and_first_equal_original(self):
        first = dict(id="first", rank=(0, -2))
        second = dict(id="second", rank=(0, -2))
        blocked = dict(id="blocked", rank=(4, -5))
        done = dict(id="done", rank=(-1,), done=True)
        entry = dict(id="list", items=[blocked, first, second, done])
        model = build([entry])
        self.assertIs(model.focus[0], first)
        self.assertIs(model.focus[1], entry)
        self.assertEqual(build([dict(items=[dict(rank=(3,)), blocked])]).focus, (None, None))
        self.assertEqual(build([dict(items=[dict(rank=(2,))])]).focus[0]["rank"], (2,))

    def test_scheduled_order_due_time_and_first_equal(self):
        earliest = dict(id="first", due=" 2026-10-26 ", due_time="08:30", rank=(4,))
        entry = dict(id="list", items=[dict(id="past", due="2026-10-25", due_time="00:01"),
                     dict(id="later", due="2026-10-27", due_time="00:01"),
                     dict(id="invalid_time", due="2026-10-26", due_time="bad"), earliest,
                     dict(id="equal", due="2026-10-26", due_time="08:30"),
                     dict(id="done", done=True, due="2026-10-26", due_time="00:01")])
        model = build([entry])
        self.assertIs(model.next_scheduled[0], earliest)
        self.assertIs(model.next_scheduled[1], entry)

    def test_explicit_date_leap_day_and_long_week(self):
        entry = dict(id="list", items=[dict(due="2028-02-28"), dict(due="2028-02-29"),
                     dict(due="2028-03-01"), dict(due="2028-03-10")])
        model = build([entry], date(2028, 2, 29))
        self.assertEqual((model.overdue, model.due_today), (1, 1))
        self.assertEqual(model.week_overview(3), [("2028-02-29", 1), ("2028-03-01", 1), ("2028-03-02", 0)])
        self.assertEqual(dict(model.week_overview(14))["2028-03-10"], 1)
        self.assertEqual(model.next_scheduled[0]["due"], "2028-02-29")

    def test_labels_ignore_unknowns_and_keep_sort_and_slice_contract(self):
        labels = {key: dict(id=key, name=name) for key, name in (("a", "Zulu"), ("b", "alpha"), ("c", "Beta"))}
        entry = dict(items=[dict(labels=["a", "a", "missing", "b", "c"]),
                            dict(labels=["b", "missing"]), dict(done=True, labels=["c"])])
        model = build([entry])
        self.assertEqual([(label["id"], count) for label, count in model.label_overview(labels.get)],
                         [("b", 2), ("a", 2), ("c", 1)])
        self.assertEqual(len(model.label_overview(labels.get, -1)), 2)
        self.assertEqual(model.label_overview(labels.get, 0), [])

    def test_single_walk_for_all_projections_and_no_input_mutation(self):
        entries = [dict(id="list", items=[dict(id="a", due="2026-10-26", labels=["a"], rank=(1,))])]
        before = copy.deepcopy(entries)
        walked = []
        normalized = []
        def counting_walk(items):
            for item in walk(items):
                walked.append(item)
                yield item
        def counting_due(value):
            normalized.append(value)
            return normalize_day(value)
        model = build(iter(entries), walk_items=counting_walk, normalize_due=counting_due)
        self.assertEqual((len(walked), len(normalized)), (1, 1))
        self.assertEqual(entries, before)
        self.assertIs(model.focus[0], entries[0]["items"][0])

    def test_individual_queries_skip_unrelated_callbacks(self):
        def forbidden(value):
            self.fail("Unrelated projection evaluated")
        entries = [dict(items=[dict(due="2026-10-26", labels=["a"])])]
        for name in ("summary", "week", "labels", "scheduled"):
            with self.subTest(projection=name):
                model = build(entries, projections=(name,), urgency_rank=forbidden)
                self.assertEqual(model.projections, frozenset((name,)))
        build(entries, projections=("labels",), urgency_rank=forbidden,
              normalize_due=forbidden, normalize_time=forbidden)
        build(entries, projections=("focus",), normalize_due=forbidden, normalize_time=forbidden)

    def test_rebuild_keeps_replaced_objects_instead_of_previous_ids(self):
        first = dict(id="same", rank=(0,))
        previous = build([dict(id="list", items=[first])])
        second = dict(id="same", rank=(0,), text="after undo")
        fresh = build([dict(id="list", items=[second])])
        self.assertIs(previous.focus[0], first)
        self.assertIs(fresh.focus[0], second)

    def test_single_and_combined_queries_have_identical_results(self):
        entries = [dict(id="a", items=[dict(id="first", due="2026-10-26", rank=(1,), labels=["b", "b"]),
                    dict(id="done", done=True, due="2026-10-25", labels=["a"]),
                    dict(kind="heading", children=[dict(id="child", due="2026-10-27", rank=(2,))])]),
                   dict(id="b", items=[dict(id="equal", due="2026-10-26", rank=(1,), labels=["a"]),
                    dict(due="invalid", rank=(4,)), dict(due="2026-10-25", rank=(3,), labels=["missing"])])]
        labels = {"a": dict(id="a", name="Alpha"), "b": dict(id="b", name="Beta")}
        expected = build(entries)
        names = sorted(dashboard.PROJECTIONS)
        for mask in range(1, 1 << len(names)):
            projections = [name for offset, name in enumerate(names) if mask & (1 << offset)]
            with self.subTest(projections=projections):
                actual = build(entries, projections=projections)
                if "summary" in projections:
                    self.assertEqual(actual.summary(entries, []), expected.summary(entries, []))
                if "focus" in projections:
                    self.assertIs(actual.focus[0], expected.focus[0])
                if "scheduled" in projections:
                    self.assertIs(actual.next_scheduled[0], expected.next_scheduled[0])
                if "week" in projections:
                    self.assertEqual(actual.week_overview(14), expected.week_overview(14))
                if "labels" in projections:
                    self.assertEqual(actual.label_overview(labels.get), expected.label_overview(labels.get))

    def test_errors_are_not_hidden_or_converted_to_partial_success(self):
        with self.assertRaisesRegex(ValueError, "Unbekannte"):
            build([], projections=("unknown",))
        def broken(value):
            raise RuntimeError("ranking failed")
        with self.assertRaisesRegex(RuntimeError, "ranking failed"):
            build([dict(items=[dict()])], urgency_rank=broken)


if __name__ == "__main__":
    unittest.main()
