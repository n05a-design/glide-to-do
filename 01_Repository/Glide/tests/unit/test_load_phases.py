"""Ladeweg in zwei Phasen ohne Tk (WA-28, Befund A34)."""
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import load_phases as lp


class NewerData(ValueError):
    pass


class ReadFailure(unittest.TestCase):
    def test_kinds_and_wording(self):
        try:
            json.loads("{kaputt")
        except ValueError as exc:
            message, newer = lp.read_failure(exc, NewerData)
        self.assertFalse(newer)
        self.assertTrue(message.startswith("Die Speicherdatei ist beschädigt oder ungültig:"))
        message, newer = lp.read_failure(PermissionError("gesperrt"), NewerData)
        self.assertFalse(newer)
        self.assertTrue(message.startswith("Die Speicherdatei konnte nicht gelesen werden:"))
        message, newer = lp.read_failure(NewerData("Unbekannte Listenart"), NewerData)
        self.assertTrue(newer)
        self.assertEqual(message, "Unbekannte Listenart")
        self.assertFalse(lp.read_failure(RecursionError("tief"))[1])

    def test_error_classes(self):
        for error in (json.JSONDecodeError("x", "", 0), UnicodeDecodeError("utf-8", b"\xff", 0, 1, "x"),
                      RecursionError(), OSError(), NewerData()):
            self.assertIsInstance(error, lp.READ_ERRORS)
        self.assertNotIsInstance(KeyError("x"), lp.READ_ERRORS)

    def test_display_failure_never_calls_the_file_damaged(self):
        title, text = lp.display_failure(RuntimeError("Zeichnen"))
        self.assertEqual(title, lp.DISPLAY_TITLE)
        self.assertNotIn("beschädigt", text)
        self.assertIn("vollständig geladen", text)
        self.assertIn("Zeichnen", text)


class ActiveList(unittest.TestCase):
    def test_choose(self):
        ids, inbox = ["eingang", "a", "b"], ["eingang"]
        self.assertEqual(lp.choose_active_list(ids, inbox, current="b", from_file="a"), "b")
        self.assertEqual(lp.choose_active_list(ids, inbox, current=None, from_file="a"), "a")
        self.assertEqual(lp.choose_active_list(ids, inbox, current="weg", from_file="a"), "a")
        self.assertEqual(lp.choose_active_list(ids, inbox, current="weg", from_file="auch-weg"), "a")
        self.assertEqual(lp.choose_active_list(["eingang"], inbox), "eingang")
        self.assertIsNone(lp.choose_active_list([], []))


if __name__ == "__main__":
    unittest.main()
