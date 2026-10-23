"""E-U3 A: Einträge, Filter, Abschnitte und Sperrgründe der durchsuchbaren Aktionen."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
import action_menu


def rows():
    """Nachbau des Blockkontextmenüs: Abschnitte über Trennlinien, Untermenüs mit Pfad."""
    return [
        ((0,), 'Ausschneiden', (), False, 0, 'command'),
        ((1,), 'Kopieren', (), False, 0, 'command'),
        ((2,), 'Einfügen', (), True, 0, 'command'),
        ((4,), 'Aufgabe verknüpfen …', (), True, 1, 'command'),
        ((5,), 'In Liste übernehmen …', (), False, 1, 'command'),
        ((7, 0), 'Fett', ('Formatieren',), False, 2, 'command'),
        ((8, 0), '   Text', ('Umwandeln in',), True, 2, 'command'),
        ((8, 1), '✓ Überschrift 1', ('Umwandeln in',), True, 2, 'command'),
        ((8, 5), '   Aufzählung', ('Umwandeln in',), True, 2, 'command'),
        ((10,), 'Zeile nach oben', (), False, 3, 'command'),
        ((11,), 'Zeile löschen', (), False, 3, 'command'),
        ((12,), 'Blockaktionen suchen …', (), True, 3, 'command'),
    ]


SECTIONS = ('Bearbeiten', 'Aufgabe', 'Formatieren', 'Block')


class EntryTests(unittest.TestCase):
    def test_sections_checks_and_reasons(self):
        values = action_menu.entries(rows(), SECTIONS, skip={'Blockaktionen suchen …'})
        by_label = {entry.label: entry for entry in values}
        self.assertNotIn('Blockaktionen suchen …', by_label)
        self.assertEqual(by_label['Einfügen'].section, 'Bearbeiten')
        self.assertEqual(by_label['Aufgabe verknüpfen …'].section, 'Aufgabe')
        self.assertEqual(by_label['Überschrift 1'].section, 'Umwandeln in')
        self.assertTrue(by_label['Überschrift 1'].checked)
        self.assertFalse(by_label['Text'].checked)
        self.assertEqual(by_label['Text'].label, 'Text')
        self.assertEqual(by_label['Zeile löschen'].section, 'Block')
        self.assertEqual(by_label['Kopieren'].reason, action_menu.SELECTION_REASON)
        self.assertEqual(by_label['Fett'].reason, action_menu.SELECTION_REASON)
        self.assertEqual(by_label['Zeile nach oben'].reason, action_menu.LINE_REASON)
        self.assertEqual(by_label['In Liste übernehmen …'].reason, action_menu.OWN_TASK_REASON)
        self.assertEqual(by_label['Einfügen'].reason, '')
        self.assertEqual(by_label['Überschrift 1'].key, (8, 1))
        self.assertEqual(by_label['Überschrift 1'].location, 'Umwandeln in')

    def test_read_only_reason_for_mutations(self):
        values = action_menu.entries(rows(), SECTIONS, context={'read_only': True})
        by_label = {entry.label: entry for entry in values}
        self.assertEqual(by_label['Zeile löschen'].reason, action_menu.READ_ONLY_REASON)
        self.assertEqual(by_label['In Liste übernehmen …'].reason, action_menu.READ_ONLY_REASON)
        # Fehlende Markierung bleibt der eigentliche Grund.
        self.assertEqual(by_label['Kopieren'].reason, action_menu.SELECTION_REASON)

    def test_unknown_group_and_kind_fall_back(self):
        values = action_menu.entries([((0,), 'Etwas', (), True, 9, 'cascade'),
                                      ((1,), '', (), True, 0, 'command')], ('Eins',))
        self.assertEqual(len(values), 1)
        self.assertEqual(values[0].section, action_menu.FALLBACK_SECTION)
        self.assertEqual(values[0].kind, 'command')

    def test_entry_limit(self):
        many = [((index,), f'Eintrag {index}', (), True, 0, 'command') for index in range(500)]
        self.assertEqual(len(action_menu.entries(many)), action_menu.MAX_ENTRIES)

    def test_empty_and_heading_reasons(self):
        self.assertEqual(action_menu.reason_for('Keine', ('Verweise (0)',)), action_menu.EMPTY_REASON)
        self.assertEqual(action_menu.reason_for('Gliederung', ()), action_menu.NO_HEADINGS_REASON)
        self.assertEqual(action_menu.reason_for('Titelbild entfernen', ('Titelbild',)), action_menu.NO_COVER_REASON)
        self.assertEqual(action_menu.reason_for('Irgendwas', ()), action_menu.DEFAULT_REASON)


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.values = action_menu.entries(rows(), SECTIONS)

    def test_empty_query_keeps_menu_order(self):
        self.assertEqual(action_menu.search(self.values, '  '), self.values)

    def test_rank_title_start_word_then_path(self):
        labels = [entry.label for entry in action_menu.search(self.values, 'ue')]
        # „Überschrift 1“ beginnt mit ü = ue; „In Liste übernehmen“ hat ein Wort mit ue.
        self.assertEqual(labels[0], 'Überschrift 1')
        self.assertIn('In Liste übernehmen …', labels)
        self.assertLess(labels.index('Überschrift 1'), labels.index('In Liste übernehmen …'))

    def test_path_and_section_match(self):
        labels = [entry.label for entry in action_menu.search(self.values, 'umwandeln')]
        self.assertEqual(labels, ['Text', 'Überschrift 1', 'Aufzählung'])
        labels = [entry.label for entry in action_menu.search(self.values, 'block')]
        self.assertIn('Zeile löschen', labels)

    def test_no_hit(self):
        self.assertEqual(action_menu.search(self.values, 'xyz'), [])
        self.assertEqual(action_menu.summary([], 'xyz'), 'Keine passende Aktion')
        self.assertEqual(action_menu.summary([], ''), 'Keine Aktionen')

    def test_grouped_order_and_first_enabled(self):
        groups = action_menu.grouped(self.values, order=('Umwandeln in', 'Block', 'Fehlt'))
        self.assertEqual([name for name, _ in groups][:2], ['Umwandeln in', 'Block'])
        self.assertEqual({name for name, _ in groups},
                         {'Umwandeln in', 'Block', 'Bearbeiten', 'Aufgabe', 'Formatieren'})
        self.assertEqual(action_menu.first_enabled(self.values).label, 'Einfügen')
        self.assertIsNone(action_menu.first_enabled([v for v in self.values if not v.enabled]))

    def test_summary_counts(self):
        text = action_menu.summary(self.values, '')
        self.assertIn('von', text)
        enabled = [value for value in self.values if value.enabled]
        self.assertEqual(action_menu.summary(enabled[:1], ''), '1 Aktion')


class HeaderTests(unittest.TestCase):
    def test_header_affordances(self):
        self.assertEqual(action_menu.header_affordances({'id': 'p'}), ('icon', 'cover'))
        self.assertEqual(action_menu.header_affordances({'icon': {'rows': []}}), ('cover',))
        self.assertEqual(action_menu.header_affordances({'cover': {'kind': 'image'}}), ('icon',))
        self.assertEqual(action_menu.header_affordances({'icon': {}, 'cover': {'kind': 'drawing'}}), ())
        self.assertEqual(action_menu.header_affordances({'id': 'p'}, read_only=True), ())
        self.assertEqual(action_menu.header_affordances({'id': 'p', 'archived': True}), ())
        self.assertEqual(action_menu.header_affordances(None), ())


if __name__ == '__main__':
    unittest.main()
