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

    def test_excerpt_matches_character_wise_reference(self):
        """P07 (3.34.0): Halbierungssuche statt Zeichenschleife – gleiche Ausschnitte wie vorher."""
        def referenz(text, key, limit=100):
            plain = ' '.join(str(text or '').split())
            if key not in search_key(plain):
                return ''
            offsets, normal = [], []
            for index, zeichen in enumerate(plain):
                teil = search_key(zeichen) if not zeichen.isspace() else ' '
                normal.append(teil)
                offsets.extend([index] * len(teil))
            position = ''.join(normal).find(key)
            first, last = offsets[position], offsets[position + len(key) - 1] + 1
            start = max(0, first - 24)
            end = min(len(plain), max(last, start + limit - 2))
            if end - start > limit - 2:
                start = first
                end = min(len(plain), start + limit - 2)
            return ('…' if start else '') + plain[start:end] + ('…' if end < len(plain) else '')

        import random
        zufall = random.Random(3340)
        zeichen = list('abcdeßäöüÄÖÜ İﬁ̈🎉xyz  \n') + ['Straße', 'GRÖSSE', 'Prüfung ']
        for _ in range(400):
            text = ''.join(zufall.choice(zeichen) for _ in range(zufall.randint(0, 260)))
            plain = search_key(text)
            if len(plain) > 4 and zufall.random() < 0.8:
                a = zufall.randrange(len(plain) - 3)
                key = plain[a:a + zufall.randint(2, 6)].strip() or 'ae'
            else:
                key = zufall.choice(['ae', 'strasse', 'groesse', 'fi', 'i', 'x'])
            self.assertEqual(content_excerpt(text, key), referenz(text, key), (text, key))



class TrefferImDokument(unittest.TestCase):
    """G14h: Positionen im Originaltext mit derselben Gleichheit wie die Suche."""

    def test_all_occurrences_with_umlauts_and_case(self):
        from content_search import match_spans
        text = "Größe prüfen. Die GROESSE zählt, auch groeße."
        self.assertEqual([text[a:b] for a, b in match_spans(text, search_key("größe"))],
                         ["Größe", "GROESSE", "groeße"])

    def test_whitespace_collapses_like_search(self):
        from content_search import match_spans
        text = "Erster   Absatz\nzweiter Absatz"
        self.assertEqual([text[a:b] for a, b in match_spans(text, search_key("absatz zweiter"))],
                         ["Absatz\nzweiter"])

    def test_empty_limit_and_wide_characters(self):
        from content_search import match_spans
        self.assertEqual(match_spans("abc", ""), [])
        self.assertEqual(len(match_spans("a" * 50, "a", limit=7)), 7)
        self.assertEqual(match_spans("Glide 🎉 Glide", "glide"), [(0, 5), (8, 13)])


if __name__ == '__main__':
    unittest.main()
