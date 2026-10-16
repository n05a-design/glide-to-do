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

    def test_legacy_view_hints_are_still_normalized(self):
        self.assertEqual(policy.normalize_hints({'list': True, 'table': False, 'bad': 1}),
                         {'list': True, 'table': False})
        self.assertEqual(policy.normalize_hints('kaputt'), {})

    def test_hints_follow_one_saved_switch_default_off(self):
        # B06 (15.10.2026): ein Schalter für alle Ansichten, Vorgabe aus.
        self.assertFalse(policy.hints_visible({}))
        self.assertFalse(policy.hints_visible({'show_hints': False}, 'list'))
        self.assertTrue(policy.hints_visible({'show_hints': True}, 'today'))
        self.assertFalse(policy.hints_visible({'show_hints': 'ja'}))
        self.assertFalse(policy.hints_visible(None))

    def test_former_choice_per_view_is_taken_over(self):
        alt = {'view_hints': {'list': True, 'table': False}}
        neu = policy.migrate_hint_setting(alt)
        self.assertIs(neu['show_hints'], True)
        self.assertNotIn('view_hints', neu)
        self.assertIn('view_hints', alt, 'Original bleibt unverändert')
        self.assertIs(policy.migrate_hint_setting({'view_hints': {'list': False}})['show_hints'], False)
        self.assertIs(policy.migrate_hint_setting({})['show_hints'], False)
        # Ein gespeicherter Schalter hat Vorrang vor Altwerten; Unlesbares fällt auf die Vorgabe.
        self.assertIs(policy.migrate_hint_setting({'show_hints': False, 'view_hints': {'list': True}})['show_hints'], False)
        self.assertIs(policy.migrate_hint_setting({'show_hints': 1})['show_hints'], False)

    def test_trash_empty_text_is_short_without_hints(self):
        # B15: exakt dieser Wortlaut.
        self.assertEqual(policy.trash_empty_text(False), 'Der Papierkorb ist leer.')
        self.assertEqual(policy.trash_empty_text(True),
                         'Der Papierkorb ist leer. Gelöschte Punkte, Listen und Ordner landen hier '
                         'und bleiben wiederherstellbar.')

    def test_planning_does_not_hide_or_relabel_due_dates(self):
        self.assertEqual(policy.date_text('7.10.', '7.10.', 'F', 'P'), 'F 7.10. · P 7.10.')
        self.assertEqual(policy.date_text('', '7.10.', 'F', 'P'), 'P 7.10.')
        self.assertEqual(policy.date_text('', '', 'F', 'P'), '')
