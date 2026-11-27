# SPDX-License-Identifier: MPL-2.0
"""Unit-Tests für den ruhigen Umgang mit verstrichenen Fristen (WA-53, Tk-frei nach D17)."""
from datetime import date
from pathlib import Path
import sys
import unittest

SRC = Path(__file__).resolve().parents[2] / "src" / "glide"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import i18n  # noqa: E402
import overdue_review as ov  # noqa: E402

HEUTE = date(2026, 11, 26)


def punkt(pid, due=None, **felder):
    return {"id": pid, "text": pid, "due": due, "done": False, "kind": "task", **felder}


class OverdueReviewTests(unittest.TestCase):
    def setUp(self):
        self.items = [
            punkt("a", "2026-11-20"),
            punkt("b", "2026-11-25", planned_date="2026-11-26"),
            punkt("c", "2026-11-01", repeat={"art": "woechentlich", "start": "2026-11-01", "ende": None}),
            punkt("d", "2026-11-26"),                     # heute fällig – nicht verstrichen
            punkt("e", "2026-11-10", done=True),          # erledigt
            punkt("f", "2026-11-10", kind="heading"),     # keine Aufgabe
            punkt("g", None),
            punkt("h", "2026-11-24T09:00"),
            punkt("i", "kaputt"),
        ]

    def tearDown(self):
        i18n.set_language("de")

    def test_zusammenfassung_neutral(self):
        s = ov.summarize(self.items, HEUTE)
        self.assertEqual((s.count, s.oldest_days, s.planned_today, s.recurring, s.to_plan), (4, 25, 1, 1, 3))
        self.assertEqual(ov.banner_text(s), "4 Aufgaben mit verstrichener Frist · älteste seit 25 Tagen · 1 schon für heute eingeplant")
        self.assertEqual(ov.banner_text(ov.summarize([], HEUTE)), "")
        self.assertEqual(ov.banner_text(ov.summarize([punkt("x", "2026-11-25")], HEUTE)), "1 Aufgabe mit verstrichener Frist")

    def test_heute_einplanen_aendert_nur_bearbeitungstag_kandidaten(self):
        self.assertEqual(ov.plan_today_ids(self.items, HEUTE), ("a", "c", "h"))
        # Funktion ist rein: nichts an den Punkten verändert
        self.assertEqual(self.items[0]["due"], "2026-11-20")
        self.assertNotIn("planned_date", self.items[0])

    def test_fristen_neu_setzen_ueberspringt_serien(self):
        plan = ov.due_shift(self.items, "2026-11-28", HEUTE)
        self.assertEqual(plan.new_due, "2026-11-28")
        self.assertEqual(plan.change_ids, ("a", "b", "h"))
        self.assertEqual(plan.skipped_recurring, ("c",))
        self.assertEqual(ov.due_shift(self.items, "2026-11-26", HEUTE).change_ids, ("a", "b", "h"))

    def test_fristen_nicht_in_vergangenheit_oder_ungueltig(self):
        for wert in ("2026-11-25", "2026-13-01", "", None, "morgen"):
            with self.assertRaises(ValueError, msg=wert):
                ov.due_shift(self.items, wert, HEUTE)

    def test_rueckfrage_nennt_serien_und_undo(self):
        plan = ov.due_shift(self.items, "2026-11-28", HEUTE)
        text = ov.shift_confirmation(plan, "Samstag", "Cmd+Z")
        self.assertIn("3 Fristen auf Samstag setzen?", text)
        self.assertIn("1 Serienaufgaben", text)
        self.assertIn("Cmd+Z", text)

    def test_englisch(self):
        i18n.set_language("en")
        s = ov.summarize(self.items, HEUTE)
        self.assertEqual(ov.banner_text(s), "4 tasks past their due date · oldest for 25 days · 1 already planned for today")
        with self.assertRaises(ValueError) as ctx:
            ov.due_shift(self.items, "2026-11-01", HEUTE)
        self.assertEqual(str(ctx.exception), "The new due date cannot be before today.")


if __name__ == "__main__":
    unittest.main()
