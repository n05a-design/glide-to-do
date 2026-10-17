"""Wiederholen nach Rückgängig: Stapelregeln ohne Tk (FP-01)."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import undo_history as uh


def undo_once(history, undo_stack, current):
    """So wie die App ein Rückgängig ausführt: prüfen, entnehmen, merken."""
    history.validate(undo_stack)
    undone = undo_stack.pop()
    history.note_write()
    history.push(current, undo_stack)
    return undone


class RedoRules(unittest.TestCase):
    def setUp(self):
        self.history = uh.RedoHistory()
        self.undo = [{"stand": n} for n in range(3)]

    def test_undo_then_redo_restores_in_reverse_order(self):
        undo_once(self.history, self.undo, "C")
        undo_once(self.history, self.undo, "B")
        self.assertTrue(self.history.validate(self.undo))
        self.assertEqual(self.history.pop(), "B")
        self.undo.append({"stand": "vor B"})
        self.history.note_write()
        self.history.mark(self.undo)
        self.assertTrue(self.history.validate(self.undo))
        self.assertEqual(self.history.pop(), "C")
        self.assertFalse(self.history.validate(self.undo))

    def test_new_step_discards_redo(self):
        undo_once(self.history, self.undo, "C")
        self.undo.append({"stand": "neu"})
        self.assertFalse(self.history.validate(self.undo))
        self.assertEqual(len(self.history), 0)

    def test_new_step_with_equal_content_is_still_new(self):
        undo_once(self.history, self.undo, "C")
        kopie = dict(self.undo[-1])
        self.undo[-1] = kopie
        self.assertFalse(self.history.validate(self.undo))

    def test_ineffective_action_keeps_redo(self):
        undo_once(self.history, self.undo, "C")
        self.undo.append({"stand": "wirkungslos"})
        self.undo.pop()
        self.assertTrue(self.history.validate(self.undo))
        # Auch das Zurücksetzen über eine Listenkopie (`undo_stack[:] = vorher`).
        vorher = list(self.undo)
        self.undo.append({"stand": "gescheitert"})
        self.undo[:] = vorher
        self.assertTrue(self.history.validate(self.undo))

    def test_any_saved_change_discards_redo(self):
        undo_once(self.history, self.undo, "C")
        self.history.note_write()
        self.assertFalse(self.history.validate(self.undo))

    def test_trimmed_bottom_keeps_redo_but_removed_top_does_not(self):
        undo_once(self.history, self.undo, "C")
        self.undo.pop(0)
        self.assertFalse(self.history.validate(self.undo), "Tiefe geändert")
        undo_once(self.history, self.undo, "B")
        self.undo.insert(0, {"stand": "unten"})
        self.undo.pop(0)
        self.assertTrue(self.history.validate(self.undo))

    def test_undo_to_empty_stack_and_clear_on_load(self):
        for stand in ("C", "B", "A"):
            undo_once(self.history, self.undo, stand)
        self.assertEqual(self.undo, [])
        self.assertTrue(self.history.validate(self.undo))
        self.history.clear()
        self.assertFalse(self.history.validate(self.undo))

    def test_limit_drops_oldest_entries(self):
        history = uh.RedoHistory(limit=3)
        undo = [{"stand": n} for n in range(5)]
        for name in "EDCBA":
            undo_once(history, undo, name)
        self.assertEqual(len(history), 3)
        self.assertEqual([history.pop() for _ in range(3)], ["A", "B", "C"])
        self.assertEqual(uh.RedoHistory().limit, uh.DEFAULT_LIMIT)
        self.assertEqual(uh.RedoHistory(limit=0).limit, 1)

    def test_failed_redo_restores_entry_and_keeps_mark(self):
        undo_once(self.history, self.undo, "C")
        self.assertTrue(self.history.validate(self.undo))
        eintrag = self.history.pop()
        # Die App legt den Stand vor dem Wiederholen ab, das Speichern scheitert
        # (kein Schreibvorgang), sie nimmt den Schritt wieder herunter.
        self.undo.append({"stand": "vor C"})
        self.undo.pop()
        self.history.restore(eintrag)
        self.assertTrue(self.history.validate(self.undo))
        self.assertEqual(self.history.pop(), "C")

    def test_push_never_mixes_with_stale_rest(self):
        undo_once(self.history, self.undo, "C")
        self.history.note_write()
        undo_once(self.history, self.undo, "B")
        self.assertEqual(len(self.history), 1)
        self.assertEqual(self.history.pop(), "B")

    def test_peek_shows_next_step_without_taking_it(self):
        self.assertIsNone(self.history.peek())
        undo_once(self.history, self.undo, "C")
        undo_once(self.history, self.undo, "B")
        self.assertEqual(self.history.peek(), "B")
        self.assertEqual(len(self.history), 2)
        self.assertEqual(self.history.pop(), "B")

    def test_board_entries_are_marked(self):
        eintrag = uh.board_redo_entry("liste:a", {"cards": []}, {"cards": [1]}, "Aufgeräumt")
        self.assertTrue(uh.is_board_entry(eintrag))
        self.assertEqual((eintrag["restored"], eintrag["board"]), ({"cards": []}, {"cards": [1]}))
        self.assertFalse(uh.is_board_entry({"lists": None}))
        self.assertFalse(uh.is_board_entry("C"))


if __name__ == "__main__":
    unittest.main()
