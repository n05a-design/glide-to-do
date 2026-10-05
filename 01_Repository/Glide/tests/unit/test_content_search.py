"""Suchvertrag: echte Inhalte, Rangfolge, Umlaute und begrenzte Ausschnitte."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
from content_search import content_excerpt, list_content, match_content, search_key, title_rank


class ContentSearchTests(unittest.TestCase):
    def test_existing_normalization(self):
        self.assertEqual(search_key('  ÄÖÜ\nStraße  '), 'aeoeue strasse')
        self.assertEqual(search_key(None), '')

    def test_title_ranking(self):
        for text, expected in [('Planung', 0), ('Meine Planung', 1), ('Vorplanung', 2), ('Bericht', None)]:
            self.assertEqual(title_rank(text, 'plan'), expected)

    def test_title_wins_and_is_not_duplicated(self):
        self.assertEqual(match_content('Budget', ['Budget im Inhalt'], 'budget'), (0, ''))

    def test_page_and_note_text_only(self):
        entry = {'note': 'Listenbeschreibung', 'rich_note': {
            'text': 'Quartalsbericht', 'spans': [{'tag': 'Geheimkennung'}],
            'links': {'x': 'https://versteckt.example'}, 'images': ['Bildbytes']}}
        texts = list_content(entry)
        self.assertEqual(texts, ('Listenbeschreibung', 'Quartalsbericht'))
        self.assertEqual(match_content('Seite', texts, 'quartal')[0], 3)
        for query in ('geheimkennung', 'versteckt', 'bildbytes'):
            self.assertEqual(match_content('Seite', texts, query), (None, ''))

    def test_old_or_malformed_document(self):
        for document in (None, '', [], {'text': 42}):
            self.assertEqual(list_content({'note': 'Alttext', 'rich_note': document}), ('Alttext',))

    def test_short_and_empty_queries_do_not_search_contents(self):
        for query in ('', 'x'):
            self.assertNotEqual(match_content('Bericht', ['xxx'], query)[0], 3)

    def test_description_and_multiline_phrase(self):
        score, excerpt = match_content('Aufgabe', ['Kosten\n  prüfen'], 'kosten pruefen')
        self.assertEqual(score, 3)
        self.assertEqual(excerpt, 'Kosten prüfen')

    def test_excerpt_uses_original_unicode_positions(self):
        for query in ('strasse', 'straße', 'pruefen', 'prüfen'):
            text = 'ä ' * 40 + 'Straße prüfen' + ' z' * 80
            excerpt = content_excerpt(text, search_key(query))
            self.assertIn('Straße prüfen', excerpt)
            self.assertLessEqual(len(excerpt), 100)

    def test_excerpt_at_edges_and_long_query(self):
        for text, query in [('Treffer ' + 'x' * 150, 'treffer'), ('x' * 150 + ' Treffer', 'treffer'),
                            ('x' * 200, 'x' * 120)]:
            excerpt = content_excerpt(text, query)
            self.assertTrue(excerpt)
            self.assertLessEqual(len(excerpt), 100)
        self.assertEqual(content_excerpt('Text', 'fehlt'), '')


if __name__ == '__main__':
    unittest.main()
