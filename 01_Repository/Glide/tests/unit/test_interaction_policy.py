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

    def test_emacs_trigger_is_control_with_one_letter(self):
        # 3.43.1: Tks X11-Emacs-Sequenzen aus ::tk::EventMotifBindings.
        for sequenz in ('<Control-P>', '<Control-Lock-p>', '<Control-Key-p>', '<Control-Shift-P>', '<Control-a>'):
            self.assertTrue(policy.is_emacs_trigger(sequenz), sequenz)
        for sequenz in ('<Up>', '<Shift-Up>', '<Control-Left>', '<Control-Shift-Home>', '<Meta-w>',
                        '<Alt-Control-p>', '<Control-F10>', '<<PrevLine>>', 'Control-p', '', None):
            self.assertFalse(policy.is_emacs_trigger(sequenz), sequenz)

    def test_only_navigation_events_with_emacs_trigger_are_guarded(self):
        # Ausschnitt aus Tk 9.1 unter X11: Treeview-Klasse und `event info`.
        klasse = ['<<PrevLine>>', '<<SelectPrevLine>>', '<<PrevWord>>', '<<Copy>>', '<Prior>', '<<LineStart>>']
        folgen = {'<<PrevLine>>': ['<Up>', '<Control-p>', '<Control-Lock-P>'],
                  '<<SelectPrevLine>>': ['<Shift-Up>', '<Control-P>', '<Control-Lock-p>'],
                  '<<PrevWord>>': ['<Control-Left>'],
                  '<<Copy>>': ['<Control-c>', '<F16>'],  # Kopieren ist keine Emacs-Navigation
                  '<<LineStart>>': ['<Home>']}       # tk_strictMotif: ohne Strg+A
        self.assertEqual(policy.emacs_guarded_events(klasse, folgen), ['<<PrevLine>>', '<<SelectPrevLine>>'])
        # Windows/macOS und Tk bis 9.0: keine Navigation über Strg-Buchstaben.
        self.assertEqual(policy.emacs_guarded_events(klasse, {'<<SelectPrevLine>>': ['<Shift-Up>']}), [])
        self.assertEqual(policy.emacs_guarded_events([], folgen), [])

    def test_guarded_script_skips_letters_and_is_idempotent(self):
        original = '::ttk::treeview::KeyNav %W up extend'
        geschuetzt = policy.guard_emacs_script(original)
        self.assertTrue(geschuetzt.startswith(policy.EMACS_GUARD_MARK))
        self.assertIn('if {[string length %K] != 1} {\n' + original + '\n}', geschuetzt)
        self.assertNotIn('break', geschuetzt)  # Fenster- und Anwendungskürzel laufen weiter
        self.assertEqual(geschuetzt.count('{'), geschuetzt.count('}'))
        self.assertEqual(policy.guard_emacs_script(geschuetzt), geschuetzt)
        self.assertEqual(policy.guard_emacs_script(''), '')
