"""Routinen in „Heute“ (AU06) ohne Oberfläche."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import routines as r


def liste(identity, items, **werte):
    eintrag = dict(id=identity, title=f"Liste {identity}", list_kind="tasks", recurring_checklist=True, items=items)
    eintrag.update(werte)
    return eintrag


def punkt(identity, done=False, kind="task", children=None):
    return dict(id=identity, done=done, kind=kind, children=children or [])


class Routinen(unittest.TestCase):
    def test_only_recurring_task_lists_count(self):
        self.assertTrue(r.is_candidate(liste("a", [])))
        self.assertFalse(r.is_candidate(liste("a", [], recurring_checklist=False)))
        self.assertFalse(r.is_candidate(liste("a", [], list_kind="note")))
        self.assertFalse(r.is_candidate(liste("a", [], archived=True)))
        self.assertFalse(r.is_candidate(liste("a", [], system_role="inbox")))

    def test_selected_keeps_order_and_drops_missing_or_archived(self):
        lists = [liste("a", []), liste("b", [], folder_id="arch"), liste("c", [])]
        auswahl = r.selected(lists, ["c", "fehlt", "b", "a"], archived_folder=lambda f: f == "arch")
        self.assertEqual([e["id"] for e in auswahl], ["c", "a"])

    def test_section_counts_tasks_with_children_not_groups(self):
        morgen = liste("m", [punkt("1", True), punkt("g", kind="group", children=[punkt("2"), punkt("3", True)]),
                             punkt("h", kind="heading")])
        leer = liste("l", [punkt("h", kind="heading")])
        zeilen = r.section([morgen, leer], {}, "2026-10-09")
        self.assertEqual(len(zeilen), 1)
        self.assertEqual((zeilen[0]["done"], zeilen[0]["total"], zeilen[0]["open"]), (2, 3, ["2"]))
        self.assertFalse(zeilen[0]["completed_today"])
        self.assertEqual(r.summary(zeilen[0]), "Liste m · 2/3")

    def test_completion_today_is_remembered_and_shown(self):
        tage = r.remember_completion({"alt": "2026-10-01", "weg": "2026-10-02", 5: "x"}, "m", "2026-10-09",
                                     valid_ids={"alt", "m"})
        self.assertEqual(tage, {"alt": "2026-10-01", "m": "2026-10-09"})
        offen = r.section([liste("m", [punkt("1"), punkt("2")])], tage, "2026-10-09")[0]
        self.assertTrue(offen["completed_today"])
        self.assertIn("heute schon einmal erledigt", r.summary(offen))
        fertig = r.section([liste("m", [punkt("1", True)])], tage, "2026-10-09")[0]
        self.assertEqual(r.summary(fertig), "Liste m · heute erledigt")
        self.assertFalse(r.section([liste("m", [punkt("1")])], tage, "2026-10-10")[0]["completed_today"])

    def test_normalize_stored_values(self):
        self.assertEqual(r.normalize_selection(["a", "", 5, "a", "b"]), ["a", "b"])
        self.assertEqual(r.normalize_selection("a"), [])
        self.assertEqual(len(r.normalize_selection([f"l{i}" for i in range(40)])), r.MAX_ROUTINES)
        self.assertEqual(r.normalize_done_days({"a": "2026-10-09", "b": "gestern", 3: "2026-10-09", "c": 5}),
                         {"a": "2026-10-09"})
        self.assertEqual(r.normalize_done_days(["a"]), {})

    def test_toggled(self):
        self.assertEqual(r.toggled(["a"], "b"), ["a", "b"])
        self.assertEqual(r.toggled(["a", "b"], "a"), ["b"])
        self.assertEqual(r.toggled(None, "a"), ["a"])


if __name__ == "__main__":
    unittest.main()
