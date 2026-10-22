"""FP-05: erwartete Treffer/Fallen unabhängig von der Oberfläche."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
import object_references as refs


def fixture():
    target = dict(id='ziel', title='Größe', items=[])
    lists = [target]
    for i in range(20):
        text = ('Die Größe prüfen.', 'GROESSE!', 'Neue größe?')[i % 3]
        entry = dict(id=f'fund{i}', title=f'Quelle {i}', items=[])
        if i % 3 == 0:
            entry['rich_note'] = dict(text=text, spans=[], links={})
        elif i % 3 == 1:
            entry['note'] = text
        else:
            entry['items'] = [dict(id=f'punkt{i}', text='Aufgabe', description=text)]
        lists.append(entry)
    target['note'] = 'Größe'  # 1: eigene Seite
    for identity, text in [('wort', 'Groessenordnung'), ('unterstrich', 'x_Größe'),
                           ('url', 'https://beispiel.test/Größe')]:
        lists.append(dict(id=identity, title=identity, note=text, items=[]))  # 2–4
    for identity, tag in [('link', 'link:a'), ('code', 'codeblock')]:
        lists.append(dict(id=identity, title=identity, items=[], rich_note=dict(
            text='Größe', spans=[dict(tag=tag, start=0, end=5)], links={'link:a': 'glide://list/ziel'})))  # 5–6
    lists.extend([dict(id='archiv', title='Archiv', archived=True, note='Größe', items=[]),  # 7
                  dict(id='explizit', title='Bezug', note='Größe', items=[], references=['glide://list/ziel']),  # 8
                  dict(id='titel', title='Größe', items=[])])  # 9: Titel ist kein Inhalt
    trash = [dict(list=dict(id='papierkorb', title='Weg', note='Größe', items=[]))]  # 10
    return lists, trash


class MentionsTests(unittest.TestCase):
    def test_twenty_hits_ten_traps_and_no_mutation(self):
        lists, trash = fixture()
        before = copy.deepcopy((lists, trash))
        hits = refs.unlinked_mentions(('list', 'ziel'), refs.nodes(lists, trash))
        self.assertEqual(len(hits), 20)
        self.assertEqual({hit.source[1] for hit in hits},
                         {f'punkt{i}' if i % 3 == 2 else f'fund{i}' for i in range(20)})
        self.assertEqual((lists, trash), before)

    def test_whitespace_umlaut_and_original_offsets(self):
        target = dict(id='t', title='Große Reise', items=[])
        source = dict(id='s', title='Quelle', note='😀 Vorher: GROSSE\n  Reise; danach.', items=[])
        hit, = refs.unlinked_mentions(('list', 't'), refs.nodes([target, source]))
        self.assertEqual(hit.text[hit.start:hit.end], 'GROSSE\n  Reise')
        self.assertEqual(hit.excerpt()[1], 'GROSSE\n  Reise')

    def test_short_missing_archived_and_task_targets(self):
        target = dict(id='t', title='Plan', items=[])
        source = dict(id='s', note='Plan und Tee', items=[dict(id='i', text='Plan')])
        for title in ('Tee', ''):
            target['title'] = title
            self.assertFalse(refs.unlinked_mentions(('list', 't'), refs.nodes([target, source])))
        target.update(title='Plan', archived=True)
        index = refs.nodes([target, source])
        for key in [('list', 't'), ('list', 'weg'), ('item', 'i')]:
            self.assertFalse(refs.unlinked_mentions(key, index))

    def test_linked_occurrence_only_excluded_not_whole_document(self):
        target = dict(id='t', title='Plan', items=[])
        source = dict(id='s', items=[], rich_note=dict(text='Plan und Plan',
            spans=[dict(tag='link:a', start=0, end=4)], links={'link:a': 'https://example.test'}))
        hit, = refs.unlinked_mentions(('list', 't'), refs.nodes([target, source]))
        self.assertEqual((hit.start, hit.end), (9, 13))
        original = copy.deepcopy(source)
        doc = refs.linked_mention_document(source, hit, ('list', 't'), 'link:new')
        self.assertEqual(doc['text'], source['rich_note']['text'])
        self.assertEqual(doc['links']['link:new'], 'glide://list/t')
        self.assertEqual(doc['spans'][-1], dict(tag='link:new', start=9, end=13))
        self.assertEqual(source, original)
        source['rich_note']['text'] += '!'
        with self.assertRaises(ValueError):
            refs.linked_mention_document(source, hit, ('list', 't'), 'link:new')

    def test_more_than_search_default_limit_and_duplicate_plain_mirror(self):
        target = dict(id='t', title='Plan', items=[])
        text = 'Plan ' * 510
        source = dict(id='s', note=text, items=[], rich_note=dict(text=text, spans=[], links={}))
        self.assertEqual(len(refs.unlinked_mentions(('list', 't'), refs.nodes([target, source]))), 510)


if __name__ == '__main__':
    unittest.main()
