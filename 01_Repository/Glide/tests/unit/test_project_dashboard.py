# SPDX-License-Identifier: MPL-2.0
"""Projektübersicht (Ecosystem E04): Kennzahlen nur aus belastbaren Feldern (T380)."""
import datetime as dt
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src" / "glide"))
import project_dashboard as pd

HEUTE = dt.date(2026, 11, 28)


def punkt(i, done=False, done_at=None, due=None, importance=None):
    return {"id": f"p{i}", "text": f"Punkt {i}", "done": done, "done_at": done_at, "due": due, "importance": importance}


class Uebersicht(unittest.TestCase):
    def setUp(self):
        self.folders = [{"id": "a", "title": "Alpha", "parent_id": None}, {"id": "a1", "title": "Teil", "parent_id": "a"},
                        {"id": "b", "title": "Beta", "parent_id": None}]
        self.lists = [
            {"id": "l1", "list_kind": "tasks", "folder_id": "a", "items": [
                punkt(1, True, "2026-11-27T10:00"), punkt(2, True, "2026-11-18"), punkt(3, due="2026-11-20", importance="high"),
                punkt(4, due="2026-12-05")]},
            {"id": "l2", "list_kind": "tasks", "folder_id": "a1", "items": [punkt(5, importance="low"), punkt(6, True, None)]},
            {"id": "l3", "list_kind": "page", "folder_id": "b", "items": [punkt(7)]},
            {"id": "l4", "list_kind": "tasks", "folder_id": None, "items": [punkt(8, due="kaputt")]},
            {"id": "l5", "list_kind": "tasks", "folder_id": "b", "archived": True, "items": [punkt(9)]},
        ]

    def test_projekte_mit_unterordnern_ohne_seiten_und_archiv(self):
        s = pd.summary(self.lists, self.folders, HEUTE, no_project_title="Ohne")
        projekte = {p["id"]: p for p in s["projects"]}
        self.assertEqual(set(projekte), {"a", pd.NO_PROJECT})
        a = projekte["a"]
        self.assertEqual((a["open"], a["done"], a["overdue"], a["next_due"]), (3, 3, 1, "2026-12-05"))
        self.assertEqual(s["totals"], {"open": 4, "done": 3, "overdue": 1})
        self.assertEqual(s["projects"][-1]["title"], "Ohne")

    def test_erledigungen_und_woche_nur_mit_datum(self):
        s = pd.summary(self.lists, self.folders, HEUTE)
        self.assertEqual(s["completions"], {"2026-11-27": 1, "2026-11-18": 1})
        self.assertEqual(s["week"], {"last_7": 1, "previous_7": 1})

    def test_fristen_und_wichtigkeit(self):
        s = pd.summary(self.lists, self.folders, HEUTE)
        self.assertEqual([(x[1], x[3]) for x in s["due_soon"]], [("p4", 7)])
        self.assertEqual(s["importance"], {"high": 1, "none": 2, "low": 1})

    def test_zyklischer_ordnerbaum_haengt_nicht(self):
        ordner = [{"id": "x", "parent_id": "y", "title": "X"}, {"id": "y", "parent_id": "x", "title": "Y"}]
        s = pd.summary([{"id": "l", "list_kind": "tasks", "folder_id": "x", "items": [punkt(1)]}], ordner, HEUTE)
        self.assertEqual(s["totals"]["open"], 1)

    def test_leerer_bestand(self):
        s = pd.summary([], [], HEUTE)
        self.assertEqual((s["projects"], s["totals"], s["completions"]), ([], {"open": 0, "done": 0, "overdue": 0}, {}))


if __name__ == "__main__":
    unittest.main()
