"""Commitgrenze: ein Schreibweg, vorbereitende Fehler und unabhängiger Nachlauf."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
from persistence import PersistenceCoordinator, PersistencePlan


class PersistenceTests(unittest.TestCase):
    def plan(self, failure=None, warning=None):
        calls = []

        def operation(name, value=None):
            def run(*args):
                calls.append(name)
                if name == failure:
                    raise OSError(name)
                return value
            return run

        comparison = object()

        def followups(value):
            self.assertIs(value, comparison)
            return [('Aktivität', operation('activity')), ('Anzeige', operation('display'))]

        plan = PersistencePlan(prepare=operation('prepare', comparison),
                               backup=operation('backup', warning), write=operation('write'),
                               accept=operation('accept'), reject=operation('reject'),
                               followups=followups, settings=operation('settings', (False, True)))
        return plan, calls

    def test_success_orders_all_stages_and_writes_once(self):
        plan, calls = self.plan()
        result = PersistenceCoordinator.save(plan)
        self.assertEqual(calls, ['prepare', 'backup', 'write', 'accept', 'activity', 'display', 'settings'])
        self.assertTrue(result.data_written and result.history_updated and result.lock_verified)
        self.assertEqual(result.followup_errors, ())

    def test_failure_before_commit_never_runs_followups(self):
        for stage in ('prepare', 'backup', 'write'):
            with self.subTest(stage=stage):
                plan, calls = self.plan(failure=stage)
                result = PersistenceCoordinator.save(plan)
                self.assertFalse(result.data_written)
                self.assertEqual(calls[-1], 'reject')
                self.assertNotIn('accept', calls)
                self.assertNotIn('activity', calls)
                self.assertEqual(result.backup_checked, stage == 'write')

    def test_backup_warning_preserves_success_and_failed_write_preserves_warning(self):
        for stage in (None, 'write'):
            plan, calls = self.plan(failure=stage, warning='Sicherung voll')
            result = PersistenceCoordinator.save(plan)
            self.assertEqual(result.data_written, stage is None)
            self.assertEqual(result.backup_warning, 'Sicherung voll')
            self.assertTrue(result.backup_checked)

    def test_post_commit_failures_do_not_reject_and_other_followups_run(self):
        for stage in ('accept', 'activity', 'display', 'settings'):
            with self.subTest(stage=stage):
                plan, calls = self.plan(failure=stage)
                result = PersistenceCoordinator.save(plan)
                self.assertTrue(result.data_written)
                self.assertNotIn('reject', calls)
                self.assertIn('display', calls)
                self.assertIn('settings', calls)
                self.assertEqual(len(result.followup_errors), 1)

    def test_followup_construction_failure_is_also_after_commit(self):
        plan, calls = self.plan()

        def broken(comparison):
            raise RuntimeError('Nachlauf')

        result = PersistenceCoordinator.save(replace(plan, followups=broken))
        self.assertTrue(result.data_written)
        self.assertEqual(result.followup_errors, ('Folgeaktionen: Nachlauf',))
        self.assertNotIn('reject', calls)

    def test_deferred_settings_keep_their_result_contract(self):
        plan, calls = self.plan()
        result = PersistenceCoordinator.save(replace(plan, settings=lambda: (True, None)))
        self.assertTrue(result.settings_pending)
        self.assertIsNone(result.settings_saved)
        self.assertFalse(result.finish_settings(False).settings_saved)


if __name__ == '__main__':
    unittest.main()
