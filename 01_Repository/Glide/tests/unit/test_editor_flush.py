"""Ergebnisvertrag der Editorübernahme ohne Tk (WA-29, Befund A35)."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import editor_flush as ef


class Combine(unittest.TestCase):
    def test_every_combination(self):
        self.assertTrue(ef.combine())
        self.assertTrue(ef.combine(True, True))
        self.assertTrue(ef.combine(None, True), "nichts offen zählt als Erfolg")
        self.assertFalse(ef.combine(False, True))
        self.assertFalse(ef.combine(True, False))
        self.assertFalse(ef.combine(False, False))
        self.assertIs(ef.combine(True, True), True)


class SwitchAllowed(unittest.TestCase):
    def test_only_unadopted_content_of_this_dataset_blocks(self):
        calls = []

        def belongs():
            calls.append(1)
            return True

        self.assertTrue(ef.switch_allowed(True, read_only=False, adopted=False, editor_in_dataset=belongs))
        self.assertEqual(calls, [], "bei Erfolg wird nichts weiter geprüft")
        self.assertFalse(ef.switch_allowed(False, read_only=False, adopted=False, editor_in_dataset=belongs))
        self.assertTrue(ef.switch_allowed(False, read_only=True, adopted=False, editor_in_dataset=True))
        self.assertTrue(ef.switch_allowed(False, read_only=False, adopted=True, editor_in_dataset=True),
                        "Schreibfehler: Uebernahme wurde am Inhalt geprueft")
        self.assertTrue(ef.switch_allowed(False, read_only=False, adopted=False, editor_in_dataset=False),
                        "Editor eines vorher geladenen Bestands")

    def test_message(self):
        title, text = ef.NOT_ADOPTED
        self.assertTrue(title and "nichts verloren" in text)


if __name__ == "__main__":
    unittest.main()
