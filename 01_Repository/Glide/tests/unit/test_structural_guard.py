"""Bestandswächter-Transaktion ohne Tk (WA-27, Befund A32)."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import structural_guard as sg


class Record:
    saved = True


class GuardTransactionRules(unittest.TestCase):
    def setUp(self):
        self.guard = sg.GuardTransaction("Gruppieren", {"a", "b", "c"}, depth_before=20, writes_before=7)

    def test_missing_and_complete(self):
        self.assertEqual(self.guard.missing({"a", "b", "c", "neu"}), set())
        self.assertEqual(self.guard.missing({"a"}), {"b", "c"})

    def test_check_save_blocks_loss_and_remembers_count(self):
        self.assertFalse(self.guard.check_save({"a"}))
        self.assertTrue(self.guard.blocked_save)
        self.assertEqual(self.guard.blocked_missing, 2)
        # Ein späterer vollständiger Stand darf wieder schreiben.
        self.assertTrue(self.guard.check_save({"a", "b", "c"}))
        self.assertFalse(self.guard.blocked_save)
        self.assertEqual(self.guard.blocked_missing, 2)

    def test_file_written_compares_write_counter(self):
        self.assertFalse(self.guard.file_written(7))
        self.assertTrue(self.guard.file_written(8))

    def test_needs_abort(self):
        self.assertFalse(self.guard.needs_abort(set()))
        self.assertTrue(self.guard.needs_abort({"b"}))
        self.assertTrue(self.guard.needs_abort(set(), crashed=True))
        self.assertTrue(self.guard.needs_abort(set(), reported=True))
        self.guard.check_save({"a"})
        self.assertTrue(self.guard.needs_abort(set()), "abgewehrtes Speichern ist ein Abbruch")

    def test_abort_marks_change_records_unsaved(self):
        first, second = Record(), Record()
        self.guard.records.extend([first, second])
        self.guard.abort()
        self.assertTrue(self.guard.aborted)
        self.assertEqual((first.saved, second.saved), (False, False))


class OutcomeAndMessage(unittest.TestCase):
    def test_outcome(self):
        self.assertEqual(sg.outcome(0, False, None), sg.RESTORED)
        self.assertEqual(sg.outcome(0, False, True), sg.RESTORED)
        self.assertEqual(sg.outcome(0, True, True), sg.RESTORED)
        self.assertEqual(sg.outcome(0, True, False), sg.UNSAVED)
        self.assertEqual(sg.outcome(0, True, None), sg.UNSAVED)
        self.assertEqual(sg.outcome(1, False, True), sg.INCOMPLETE)
        self.assertEqual(sg.outcome(2, True, True), sg.INCOMPLETE)
        self.assertEqual(sg.outcome(0, False, True, dirty_before=True), sg.UNSAVED)

    def test_byte_exact_restoration_and_failed_replace(self):
        with tempfile.TemporaryDirectory(prefix="glide-guard-bytes-") as folder:
            path = Path(folder) / "bestand.json"
            path.write_bytes(b'{"neu": true}')
            original = b'{ "alt": 1 }\r\n'
            sg.restore_bytes(path, original)
            self.assertEqual(path.read_bytes(), original)
            def denied(*args):
                raise OSError("Schreibfehler")
            with self.assertRaises(OSError):
                sg.restore_bytes(path, b"anderer Inhalt", denied)
            self.assertEqual(path.read_bytes(), original)
            self.assertEqual([p.name for p in Path(folder).iterdir()], ["bestand.json"])

    def test_only_restored_claims_full_restoration(self):
        title, text = sg.stop_message("Gruppieren", 1, sg.RESTORED)
        self.assertEqual(title, "Abgebrochen – keine Daten verloren")
        self.assertIn("vollständig wiederhergestellt", text)
        self.assertIn("1 Punkt(e)", text)
        for result in (sg.UNSAVED, sg.INCOMPLETE):
            title, text = sg.stop_message("Gruppieren", 1, result, missing_after=1)
            self.assertNotIn("keine Daten verloren", title)
            self.assertNotIn("vollständig wiederhergestellt", text)
        title, text = sg.stop_message("Gruppieren", 1, sg.UNSAVED)
        self.assertIn("ließ sich aber nicht speichern", text)
        title, text = sg.stop_message("Gruppieren", 3, sg.INCOMPLETE, missing_after=2)
        self.assertIn("2 Punkt(e) fehlen noch", text)
        self.assertIn("Strg/Cmd+Z", text)

    def test_crash_and_unknown_count(self):
        self.assertIn("abgebrochen", sg.stop_message("X", 0, crashed=True)[1])
        text = sg.stop_message("X", 0)[1]
        self.assertNotIn("0 Punkt", text)


if __name__ == "__main__":
    unittest.main()
