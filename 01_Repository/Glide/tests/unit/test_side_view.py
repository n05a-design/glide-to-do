"""E-U2 A: Ziel, Lesbarkeit und Projektion der lesenden Nebenansicht."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
import page_markdown
import side_view


class NavigationTests(unittest.TestCase):
    def test_unicode_offsets_refer_to_original_text(self):
        text = '🎵 Straße und STRASSE, Straße.'
        matches, more = side_view.literal_matches(text, 'strasse')
        self.assertEqual([text[a:b] for a,b in matches], ['Straße', 'STRASSE', 'Straße'])
        self.assertFalse(more)
        self.assertEqual(side_view.literal_matches('ß', 's'), ([(0, 1)], False))

    def test_literal_query_and_budget(self):
        self.assertEqual(side_view.literal_matches('[x] a.b [x]', '[x]'), ([(0, 3), (8, 11)], False))
        self.assertEqual(side_view.literal_matches('aaaa', 'a', 2), ([(0, 1), (1, 2)], True))
        self.assertEqual(side_view.literal_matches('abc', ''), ([], False))
        self.assertEqual(side_view.literal_matches('abc', 'z'), ([], False))

    def test_matching_rows_preserve_ids_and_order(self):
        rows = [('one', 'Straße'), ('two', 'Straße Straße'), ('three', 'Anders')]
        self.assertEqual(side_view.matching_rows(rows, 'STRASSE'), (['one', 'two'], False))
        self.assertEqual(side_view.matching_rows(rows, 'STRASSE', 1), (['one'], True))

    def test_match_navigation_wraps_both_directions(self):
        self.assertEqual(side_view.match_index(-1, 3), 0)
        self.assertEqual(side_view.match_index(-1, 3, -1), 2)
        self.assertEqual(side_view.match_index(2, 3), 0)
        self.assertEqual(side_view.match_index(0, 3, -1), 2)
        self.assertEqual(side_view.match_index(0, 0), -1)

    def test_page_sections_are_projection_headings(self):
        entry = {'list_kind': 'page', 'rich_note': page_markdown.markdown_to_page('# Start\n\nText\n\n## Weiter\n')}
        before = repr(entry)
        sections = side_view.sections(entry)
        self.assertEqual([section['title'] for section in sections], ['Start', 'Weiter'])
        self.assertEqual([section['depth'] for section in sections], [0, 1])
        self.assertEqual(repr(entry), before)

    def test_list_sections_use_real_group_ids(self):
        entry = {'items': [{'id': 'g', 'kind': 'group', 'text': 'Abschnitt', 'children': [
            {'id': 'h', 'kind': 'heading', 'text': 'Unterabschnitt'}, {'id': 'a', 'text': 'Aufgabe'}]}]}
        self.assertEqual(side_view.sections(entry), [dict(key='g', title='Abschnitt', depth=0),
                                                     dict(key='h', title='Unterabschnitt', depth=1)])


def page_document():
    document = page_markdown.markdown_to_page(
        '# Wochenplan\n\nAbsatz mit **fett** und *kursiv*.\n\n- Grundriss prüfen\n- Muster bestellen\n\n'
        '> Zitat zum Schluss\n\n---\n\n## Nächste Schritte\n')
    text = document['text'] + '\nAngebot vergleichen\n￼\nNach dem Bild'
    start = text.index('Angebot vergleichen')
    spans = list(document['spans']) + [
        {'tag': 'item:a1', 'start': start, 'end': start + len('Angebot vergleichen')},
        {'tag': 'indent1', 'start': start, 'end': start + len('Angebot vergleichen') + 1},
    ]
    return {'text': text, 'spans': spans, 'links': {}}


class AvailabilityTests(unittest.TestCase):
    def test_reference_target_uses_typed_ids_and_owning_container(self):
        entry = {'id': 'same', 'list_kind': 'page'}
        task = {'id': 'same', 'text': 'Aufgabe'}
        index = {('list', 'same'): ('active', entry, entry),
                 ('item', 'same'): ('active', task, entry)}
        self.assertEqual(side_view.reference_target(('list', 'same'), index),
                         {'list_id': 'same', 'item_id': None})
        self.assertEqual(side_view.reference_target(('item', 'same'), index),
                         {'list_id': 'same', 'item_id': 'same'})

    def test_reference_target_accepts_archive_but_not_deleted_or_unsupported(self):
        for state in ('active', 'archived'):
            entry = {'id': 'l', 'list_kind': 'note'}
            self.assertEqual(side_view.reference_target(('list', 'l'), {('list', 'l'): (state, entry, entry)}),
                             {'list_id': 'l', 'item_id': None})
        for state, kind in (('trash', 'page'), ('missing', 'tasks'), ('active', 'drawing'), ('active', 'gallery')):
            entry = {'id': 'l', 'list_kind': kind}
            self.assertIsNone(side_view.reference_target(('list', 'l'), {('list', 'l'): (state, entry, entry)}))
        self.assertIsNone(side_view.reference_target(None, {}))
        self.assertIsNone(side_view.reference_target(('item', 'gone'), {}))

    def test_reference_target_is_fresh_and_does_not_mutate(self):
        old = {'id': 'old', 'list_kind': 'tasks'}
        new = {'id': 'new', 'list_kind': 'tasks'}
        task = {'id': 'task'}
        self.assertEqual(side_view.reference_target(('item', 'task'), {('item', 'task'): ('active', task, old)})['list_id'], 'old')
        self.assertEqual(side_view.reference_target(('item', 'task'), {('item', 'task'): ('active', task, new)})['list_id'], 'new')
        self.assertEqual(task, {'id': 'task'})

    def test_states(self):
        self.assertEqual(side_view.availability({'id': 'l', 'list_kind': 'tasks'}), ('ok', ''))
        self.assertEqual(side_view.availability({'id': 'p', 'list_kind': 'page'})[0], 'ok')
        self.assertEqual(side_view.availability({'id': 'p', 'list_kind': 'page', 'archived': True})[0], 'archived')
        state, text = side_view.availability({'id': 'z', 'list_kind': 'drawing'})
        self.assertEqual(state, 'unsupported')
        self.assertIn('Zeichnungen', text)
        self.assertEqual(side_view.availability({'id': 'g', 'list_kind': 'gallery'})[0], 'unsupported')
        self.assertEqual(side_view.availability(None, 'weg')[0], 'missing')
        trash = [{'kind': 'list', 'list': {'id': 'weg'}}]
        self.assertEqual(side_view.availability(None, 'weg', trash)[0], 'trash')
        folder = [{'kind': 'folder', 'folder': {'id': 'f', 'lists': [{'id': 'innen'}]}}]
        self.assertEqual(side_view.availability(None, 'innen', folder)[0], 'trash')

    def test_targets(self):
        self.assertEqual(side_view.target_for({'id': 'x'}), {'kind': 'list', 'id': 'x'})
        self.assertIsNone(side_view.target_for({'id': ''}))
        self.assertIsNone(side_view.target_for(None))
        self.assertEqual(side_view.normalize_target({'kind': 'list', 'id': 'x'}), {'kind': 'list', 'id': 'x'})
        self.assertIsNone(side_view.normalize_target({'kind': 'folder', 'id': 'x'}))
        self.assertIsNone(side_view.normalize_target({'kind': 'list', 'id': 'x' * 201}))

    def test_content_kind(self):
        self.assertEqual(side_view.content_kind({'list_kind': 'page'}), 'page')
        self.assertEqual(side_view.content_kind({'list_kind': 'note'}), 'note')
        self.assertEqual(side_view.content_kind({}), 'tasks')


class RowTests(unittest.TestCase):
    def test_list_rows_and_summary(self):
        items = [dict(id='g', text='Bauabschnitt  Nord', kind='group', children=[
                     dict(id='a', text='Statik prüfen', done=True, due='2026-10-30'),
                     dict(id='b', text='Gerüst\nbestellen', kind='long')]),
                 dict(id='h', text='Später', kind='heading'), 'kaputt', dict(id='c', text='Abnahme')]
        rows = side_view.list_rows(items)
        self.assertEqual([row['id'] for row in rows], ['g', 'a', 'b', 'h', 'c'])
        self.assertEqual(rows[0]['text'], 'Bauabschnitt Nord')
        self.assertEqual(rows[1]['depth'], 1)
        self.assertEqual(rows[2]['text'], 'Gerüst bestellen')
        self.assertEqual([row['toggle'] for row in rows], [False, True, True, False, True])
        self.assertEqual(rows[1]['due'], '2026-10-30')
        self.assertEqual(side_view.list_summary(rows), '2 offen · 1 erledigt')
        self.assertEqual(side_view.list_summary([]), 'Keine Aufgaben')
        self.assertEqual(side_view.list_summary(side_view.list_rows([dict(id='x', done=True)])), '1 erledigt')

    def test_row_limit(self):
        items = [dict(id=str(n), text=str(n)) for n in range(50)]
        self.assertEqual(len(side_view.list_rows(items, limit=10)), 10)


class ProjectionTests(unittest.TestCase):
    def test_styles_tasks_images_and_inline(self):
        projection = side_view.page_projection(page_document())
        lines = {line['line']: line for line in projection['lines']}
        texts = projection['text'].split('\n')
        style = {texts[number - 1]: line['style'] for number, line in lines.items()}
        self.assertEqual(style['Wochenplan'], 'h1')
        self.assertEqual(style['Nächste Schritte'], 'h2')
        self.assertEqual(style['• Grundriss prüfen'], 'bullet')
        self.assertEqual(style['Zitat zum Schluss'], 'quote')
        self.assertEqual(style['Absatz mit fett und kursiv.'], 'body')
        self.assertEqual(style['Angebot vergleichen'], 'task')
        self.assertEqual(style['￼'], 'image')
        task_line = next(line for line in projection['lines'] if line['task'])
        self.assertEqual((task_line['task'], task_line['reference'], task_line['indent']), ('a1', False, 1))
        self.assertEqual(side_view.page_tasks(projection), ['a1'])
        self.assertEqual(len(projection['images']), 1)
        formats = {tag for _start, _end, tag in projection['inline']}
        self.assertEqual(formats, {'bold', 'italic'})
        start, end, _ = next(value for value in projection['inline'] if value[2] == 'bold')
        self.assertEqual(projection['text'][start:end], 'fett')
        self.assertFalse(projection['truncated'])

    def test_truncation_and_invalid_input(self):
        document = {'text': '\n'.join(f'Zeile {n}' for n in range(20)),
                    'spans': [{'tag': 'h1', 'start': 0, 'end': 7}, {'tag': 'bold', 'start': 'x', 'end': 2},
                              'kaputt', {'tag': 'unbekannt', 'start': 0, 'end': 3}]}
        projection = side_view.page_projection(document, limit=5)
        self.assertTrue(projection['truncated'])
        self.assertEqual(len(projection['lines']), 5)
        self.assertEqual(projection['lines'][0]['style'], 'h1')
        self.assertEqual(side_view.page_projection(None)['lines'], [{'line': 1, 'style': 'body', 'indent': 0,
                                                                      'task': None, 'reference': False}])

    def test_reference_task(self):
        document = {'text': 'Fremde Aufgabe', 'spans': [{'tag': 'taskref:z9', 'start': 0, 'end': 14}]}
        line = side_view.page_projection(document)['lines'][0]
        self.assertEqual((line['style'], line['task'], line['reference']), ('task', 'z9', True))


class SignatureTests(unittest.TestCase):
    def test_signature_changes_with_visible_content(self):
        entry = {'id': 'p', 'title': 'Plan', 'list_kind': 'page', 'rich_note': page_document(),
                 'items': [dict(id='a1', text='Angebot vergleichen')]}
        base = side_view.signature(entry, ('a1', False))
        self.assertEqual(base, side_view.signature(dict(entry), ('a1', False)))
        self.assertNotEqual(base, side_view.signature(dict(entry, title='Neu'), ('a1', False)))
        self.assertNotEqual(base, side_view.signature(entry, ('a1', True)))
        changed = dict(entry, items=[dict(id='a1', text='Angebot vergleichen', done=True)])
        self.assertNotEqual(base, side_view.signature(changed, ('a1', False)))
        self.assertEqual(side_view.signature(None, extra=('x',)), ('none', 'x'))


if __name__ == '__main__':
    unittest.main()
