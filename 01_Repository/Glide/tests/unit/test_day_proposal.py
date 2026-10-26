"""Auswahlbudget, stabile Reihenfolge und unveränderliche Vorschläge."""
import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import day_proposal as p


def row(identity, **fields):
    item = dict(id=identity, text=identity, importance=0, due=None, planned_date=None,
                estimated_minutes=30, done=False)
    item.update(fields)
    return dict(list_id="list", item=item, blocked=False)


def summary(remaining=90, unknown=0):
    return dict(capacity=120, remaining=remaining, without_estimate=unknown, minutes=30)


class ProposalTest(unittest.TestCase):
    def test_last_open_prerequisite_is_a_new_reason_before_importance(self):
        data = [row("important", importance=3), row("release"), row("waiting", blocked_by=["release"])]
        data[-1]["blocked"] = True
        result = p.propose(data, "2026-10-07", summary(30))
        self.assertEqual([r["item_id"] for r in result["rows"]], ["release", "important"])
        first = result["rows"][0]
        self.assertEqual((first["reason"], first["unblocks"], first["selected"]), ("unblocks", 1, True))
        self.assertEqual(p.reason_text(first), "gibt 1 weitere Aufgabe frei")

    def test_only_last_open_direct_prerequisite_counts(self):
        data = [row("a"), row("b"), row("done", done=True),
                row("one", blocked_by=["a", "done", "missing", "a"]),
                row("two", blocked_by=["a", "b"]),
                row("finished", blocked_by=["a"], done=True),
                row("self", blocked_by=["self"])]
        self.assertEqual(p.release_counts(data), {"a": 1})
        self.assertEqual(p.release_counts(data + [data[3]]), {"a": 1})

    def test_more_releases_first_but_urgent_order_is_preserved(self):
        data = [row("a"), row("b"), row("urgent", due="2026-10-01"),
                row("w1", blocked_by=["a"]), row("w2", blocked_by=["b"]),
                row("w3", blocked_by=["b"]), row("w4", blocked_by=["urgent"])]
        for record in data[3:]:
            record["blocked"] = True
        result = p.propose(data, "2026-10-07", summary(60))
        self.assertEqual([r["item_id"] for r in result["rows"]], ["urgent", "b", "a"])
        self.assertEqual(p.reason_text(result["rows"][0]), "überfällig · gibt 1 weitere Aufgabe frei")
        self.assertEqual(p.reason_text(result["rows"][1]), "gibt 2 weitere Aufgaben frei")
        self.assertEqual([r["selected"] for r in result["rows"]], [True, True, False])

    def test_archived_prerequisite_status_is_resolved_and_invalidates_preview(self):
        data = [row("a"), row("waiting", blocked_by=["a", "archived"])]
        data[1]["blocked"] = True
        open_context = {"a": False, "waiting": False, "archived": False}
        before = p.propose(data, "2026-10-07", summary(), dependency_done=open_context)
        after = p.propose(data, "2026-10-07", summary(), dependency_done={**open_context, "archived": True})
        self.assertEqual(before["rows"], [])
        self.assertEqual(after["rows"][0]["unblocks"], 1)
        self.assertNotEqual(before["signature"], after["signature"])

    def test_release_counts_do_not_mutate_or_override_exclusions(self):
        data = [row("future", planned_date="2026-10-08"), row("today", planned_date="2026-10-07"),
                row("blocked"), row("w1", blocked_by=["future"]),
                row("w2", blocked_by=["today"]), row("w3", blocked_by=["blocked"])]
        for record in data[2:]:
            record["blocked"] = True
        old = copy.deepcopy(data)
        self.assertEqual(p.propose(data, "2026-10-07", summary())["rows"], [])
        self.assertEqual(data, old)

    def test_direct_chain_is_not_a_transitive_release_and_cycles_stay_blocked(self):
        data = [row("a"), row("b", blocked_by=["a"]), row("c", blocked_by=["b"]),
                row("cycle_a", blocked_by=["cycle_b"]), row("cycle_b", blocked_by=["cycle_a"])]
        for record in data[1:]:
            record["blocked"] = True
        result = p.propose(data, "2026-10-07", summary())
        self.assertEqual([(r["item_id"], r["unblocks"]) for r in result["rows"]], [("a", 1)])

    def test_reasons_order_and_exact_fit(self):
        data = [row("important", importance=3), row("soon", due="2026-10-09"),
                row("carried", planned_date="2026-10-06"), row("today", due="2026-10-07"),
                row("overdue", due="2026-10-01")]
        proposal = p.propose(data, "2026-10-07", summary())
        self.assertEqual([r["item_id"] for r in proposal["rows"]],
                         ["overdue", "today", "carried", "soon", "important"])
        self.assertEqual([r["selected"] for r in proposal["rows"]], [True, True, True, False, False])
        self.assertEqual(proposal["remaining"], 0)

    def test_large_task_does_not_hide_small_fit(self):
        result = p.propose([row("large", due="2026-10-01", estimated_minutes=100),
                            row("small", importance=1, estimated_minutes=20)], "2026-10-07", summary(20))
        self.assertEqual([r["selected"] for r in result["rows"]], [False, True])

    def test_missing_estimates_reserve_budget_without_mutation(self):
        data = [row("unknown", importance=1, estimated_minutes=None), row("known", importance=1)]
        old = copy.deepcopy(data)
        result = p.propose(data, "2026-10-07", summary(60, 1))
        self.assertEqual(result["budget"], 30)
        self.assertEqual(sum(r["minutes"] for r in result["rows"] if r["selected"]), 30)
        self.assertEqual(data, old)
        self.assertTrue(next(r for r in result["rows"] if r["item_id"] == "unknown")["assumed"])

    def test_no_choice_for_full_overplanned_or_unknown_day(self):
        for remaining in (0, -30, None):
            result = p.propose([row("a", importance=1)], "2026-10-07", summary(remaining))
            self.assertFalse(result["rows"][0]["selected"])
            with self.assertRaises(ValueError):
                p.selected_rows(result, [("list", "a")])

    def test_future_plan_completed_blocked_and_already_today_excluded(self):
        data = [row("future", importance=3, planned_date="2026-10-08"),
                row("done", importance=3, done=True), row("today", importance=3, planned_date="2026-10-07"),
                row("blocked", importance=3)]
        data[-1]["blocked"] = True
        self.assertEqual(p.propose(data, "2026-10-07", summary())["rows"], [])

    def test_duplicate_identity_and_input_order_are_deterministic(self):
        data = [row("b", importance=1), row("a", importance=1)]
        first = p.propose(data, "2026-10-07", summary())
        second = p.propose(list(reversed(data)), "2026-10-07", summary())
        self.assertEqual(first, second)
        self.assertEqual(len(p.propose(data + [data[0]], "2026-10-07", summary())["rows"]), 2)

    def test_preview_signatures_detect_changes_and_capacity(self):
        data = [row("a", importance=1)]
        original = p.propose(data, "2026-10-07", summary())["signature"]
        data[0]["item"]["text"] = "changed"
        self.assertNotEqual(original, p.propose(data, "2026-10-07", summary())["signature"])
        self.assertNotEqual(original, p.propose([row("a", importance=1)], "2026-10-07", summary(30))["signature"])

    def test_unknown_selection_and_empty_selection(self):
        result = p.propose([row("a", importance=1)], "2026-10-07", summary())
        self.assertEqual(p.selected_rows(result, []), [])
        with self.assertRaises(ValueError):
            p.selected_rows(result, [("other", "a")])


if __name__ == "__main__":
    unittest.main()
