import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
from save_result import SaveResult
from task_editing import ChangeRecord
from exchange_recipes import preview_text
import json


class SaveResults(unittest.TestCase):
    def test_preview_retains_full_instruction_and_context(self):
        payload = dict(instructions='Anweisung ä ' * 1200, items=[dict(ref='a', title='Original')])
        preview = preview_text(payload)
        self.assertIn(payload['instructions'], preview)
        self.assertEqual(json.loads(preview.split('\n\nKontext und Paketdaten\n\n', 1)[1]),
                         dict(items=payload['items']))
    def test_commit_is_independent_from_backup_and_followup(self):
        result = SaveResult(data_written=True, lock_verified=True, backup_checked=True,
                            backup_warning='Sicherung voll', followup_errors=('Ansicht fehlt',))
        self.assertTrue(result.success)
        self.assertFalse(SaveResult(lock_verified=True, error='Datei gesperrt').success)
        with self.assertRaises(TypeError):
            bool(result)

    def test_result_is_immutable(self):
        with self.assertRaises(AttributeError):
            SaveResult().data_written = True

    def test_ui_followup_preserves_written_result_and_settings(self):
        before = SaveResult(data_written=True, lock_verified=True, settings_saved=True,
                            followup_errors=('Seitenleiste',))
        after = before.with_followup_error('Inhaltsansicht')
        self.assertTrue(after.success)
        self.assertTrue(after.lock_verified)
        self.assertIs(after.settings_saved, True)
        self.assertEqual(before.followup_errors, ('Seitenleiste',))
        self.assertEqual(after.followup_errors, ('Seitenleiste', 'Inhaltsansicht'))

    def test_deferred_settings_complete_without_reversing_commit(self):
        pending = SaveResult(data_written=True, settings_pending=True)
        result = pending.finish_settings(False)
        self.assertTrue(result.success)
        self.assertFalse(result.settings_pending)
        self.assertIs(result.settings_saved, False)
        self.assertEqual(len(result.followup_errors), 1)
        self.assertIs(result.finish_settings(True), result)

    def test_change_record_retains_boolean_contract_and_explicit_details(self):
        result = ChangeRecord(['a', 'b'])
        self.assertFalse(result.changed)
        self.assertIsNone(result.saved)
        self.assertIsNone(result.save_result)
        result.mark('b'); result.save_result = SaveResult(data_written=True); result.saved = True
        self.assertEqual(result.changed_ids, {'b'})
        self.assertEqual(result.focus_id, 'b')
        self.assertIs(result.saved, True)
