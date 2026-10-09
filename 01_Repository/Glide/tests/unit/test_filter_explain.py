"""Gespeicherte Filter prüfen und erklären (D-03) ohne Oberfläche."""
from datetime import date
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import filter_explain as fe

HEUTE = date(2026, 10, 9)


def fakten(**werte):
    basis = {"list_id": "L1", "from_pages": False, "done": False, "importance": 0, "labels": set(),
             "due": None, "query_match": True}
    basis.update(werte)
    return basis


def kriterien(**werte):
    basis = {"list_ids": [], "label_ids": [], "status": "all", "importance": "all", "due": "any",
             "label_mode": "any", "source": "all", "query": ""}
    basis.update(werte)
    return basis


class Bedingungen(unittest.TestCase):
    def test_unset_conditions_do_not_appear(self):
        self.assertEqual(fe.conditions(kriterien(), fakten(), HEUTE), [])
        self.assertTrue(fe.matches([]))

    def test_each_condition(self):
        fall = [
            (kriterien(list_ids=["L2"]), fakten(), "list", False),
            (kriterien(list_ids=["L1"]), fakten(), "list", True),
            (kriterien(source="pages"), fakten(from_pages=True), "source", True),
            (kriterien(status="open"), fakten(done=True), "status", False),
            (kriterien(status="done"), fakten(done=True), "status", True),
            (kriterien(importance="3"), fakten(importance=2), "importance", False),
            (kriterien(label_ids=["a", "b"], label_mode="all"), fakten(labels={"a"}), "labels", False),
            (kriterien(label_ids=["a", "b"]), fakten(labels={"a"}), "labels", True),
            (kriterien(due="none"), fakten(due=HEUTE), "due", False),
            (kriterien(due="overdue"), fakten(due=date(2026, 10, 1)), "due", True),
            (kriterien(due="overdue"), fakten(due=date(2026, 10, 1), done=True), "due", False),
            (kriterien(due="tomorrow"), fakten(due=date(2026, 10, 10)), "due", True),
            (kriterien(due="next7"), fakten(due=date(2026, 10, 15)), "due", True),
            (kriterien(due="next7"), fakten(due=date(2026, 10, 16)), "due", False),
            (kriterien(query="Bericht"), fakten(query_match=False), "query", False),
        ]
        for krit, fak, key, ok in fall:
            with self.subTest(key=key, ok=ok):
                ergebnis = fe.conditions(krit, fak, HEUTE)
                self.assertEqual([(e["key"], e["ok"]) for e in ergebnis], [(key, ok)])
                self.assertEqual(fe.matches(ergebnis), ok)

    def test_details_name_missing_labels_and_list(self):
        ergebnis = fe.conditions(kriterien(list_ids=["L2"], label_ids=["a", "b"], label_mode="all"),
                                 fakten(labels={"a"}), HEUTE, names={"L1": "Arbeit", "b": "Wichtig"})
        self.assertIn("„Arbeit“", ergebnis[0]["detail"])
        self.assertIn("fehlt: Wichtig", ergebnis[1]["detail"])

    def test_hidden_reasons_count_first_failure(self):
        krit = kriterien(status="open", due="today")
        listen = [fe.conditions(krit, fakten(done=True, due=None), HEUTE),
                  fe.conditions(krit, fakten(done=False, due=None), HEUTE),
                  fe.conditions(krit, fakten(done=False, due=HEUTE), HEUTE)]
        self.assertEqual(fe.hidden_reasons(listen), [("Status", 1), ("Fälligkeit", 1)])


if __name__ == "__main__":
    unittest.main()
