from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
import interaction_policy as policy


class InteractionTests(unittest.TestCase):
    def test_action_scope_and_content_query_are_distinct(self):
        self.assertEqual(policy.palette_query(' > Kopieren '), ('Kopieren', True))
        self.assertEqual(policy.palette_query('Kopieren'), ('Kopieren', False))
        self.assertEqual(policy.palette_query('>'), ('', True))

    def test_hints_are_opt_in_per_view_and_invalid_settings_are_rejected(self):
        settings = {'view_hints': policy.normalize_hints({'list': True, 'table': False, 'bad': 1})}
        self.assertTrue(policy.hints_visible(settings, 'list'))
        self.assertFalse(policy.hints_visible(settings, 'table'))
        self.assertFalse(policy.hints_visible(settings, 'today'))
        self.assertNotIn('bad', settings['view_hints'])

    def test_planning_does_not_hide_or_relabel_due_dates(self):
        self.assertEqual(policy.date_text('7.10.', '7.10.', 'F', 'P'), 'F 7.10. · P 7.10.')
        self.assertEqual(policy.date_text('', '7.10.', 'F', 'P'), 'P 7.10.')
        self.assertEqual(policy.date_text('', '', 'F', 'P'), '')
