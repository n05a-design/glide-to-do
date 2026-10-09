"""Semantische Grenzen: Heimat, Referenz, Archiv, Papierkorb, ID-Neuvergabe."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
import task_references as refs


class TaskReferencesTests(unittest.TestCase):
    def test_tags(self):
        for tag in ('item:a', 'taskref:b-2_c'):
            self.assertEqual(refs.task_id(tag), tag.split(':')[1])
        for tag in (None, 'taskref:', 'item:a b', 'taskref:' + 'a' * 65, 'item:a\n'):
            self.assertIsNone(refs.task_id(tag))

    def test_owned_ids(self):
        doc = dict(spans=[dict(tag='item:a'), dict(tag='taskref:b'), dict(tag='bold')])
        self.assertEqual(refs.document_ids(doc), {'a', 'b'})
        self.assertEqual(refs.document_ids(doc, owned=True), {'a'})

    def test_owned_tag_ignores_same_id_reference(self):
        self.assertEqual(refs.task_id('item:a', owned=True), 'a')
        self.assertIsNone(refs.task_id('taskref:a', owned=True))
        both = dict(spans=[dict(tag='item:a'), dict(tag='taskref:a')])
        reference = dict(spans=[dict(tag='taskref:a')])
        self.assertEqual(refs.document_ids(both, owned=True), {'a'})
        self.assertEqual(refs.document_ids(reference), {'a'})
        self.assertEqual(refs.document_ids(reference, owned=True), set())

    def test_move_preserves_other_content(self):
        doc = dict(text='a😀b', images={'img:x': {}}, links={'link:x': 'url'},
                   spans=[dict(tag='item:a', start=0, end=1), dict(tag='bold', start=1, end=2)])
        old = copy.deepcopy(doc)
        moved = refs.reference_document(doc, ['a'])
        self.assertEqual(doc, old)
        self.assertEqual(moved['spans'][0]['tag'], 'taskref:a')
        for key in ('text', 'images', 'links'):
            self.assertEqual(moved[key], doc[key])

    def test_sources_and_archives(self):
        page = dict(id='p', list_kind='page', items=[dict(id='a', children=[dict(id='child')])],
                    rich_note=dict(spans=[dict(tag='taskref:b'), dict(tag='taskref:b')]))
        note = dict(id='n', list_kind='note', items=[dict(id='c')])
        archived = dict(id='old', list_kind='page', archived=True, items=[dict(id='d')])
        self.assertEqual(refs.sources([page, note, archived]), {'a': ['p'], 'child': ['p'], 'b': ['p'], 'c': ['n']})
        self.assertNotIn('c', refs.sources([page, note], pages_only=True))

    def test_remap_roles_and_external_targets(self):
        doc = dict(spans=[dict(tag='item:a'), dict(tag='taskref:b'), dict(tag='taskref:outside')])
        refs.remap(doc, {'a': 'new-a', 'b': 'new-b'})
        self.assertEqual([s['tag'] for s in doc['spans']], ['item:new-a', 'taskref:new-b', 'taskref:outside'])

    def test_status_never_restores_or_duplicates(self):
        child = dict(id='child', text='Kind')
        page = dict(id='p', items=[dict(id='a', children=[child])])
        trash = [dict(payload=dict(id='folder', lists=[page]))]
        before = copy.deepcopy(trash)
        self.assertEqual(refs.status('child', [], trash), ('trash', child, None))
        self.assertEqual(refs.status('gone', [], trash), ('missing', None, None))
        self.assertEqual(refs.status('child', [page], trash), ('active', child, page))
        self.assertEqual(trash, before)

    def test_edited_reference_title(self):
        old = dict(text='Alt\nAlt', spans=[dict(tag='taskref:a', start=0, end=7)])
        new = dict(text='Neu 😀\nAlt', spans=[dict(tag='taskref:a', start=0, end=9)])
        self.assertEqual(refs.edited_titles(old, new), {'a': 'Neu 😀'})
        self.assertEqual(refs.edited_titles(old, old), {})

    def test_reference_removal_does_not_rename(self):
        old = dict(text='Alt\nAlt', spans=[dict(tag='taskref:a', start=0, end=7)])
        new = dict(text='Alt', spans=[dict(tag='taskref:a', start=0, end=3)])
        self.assertEqual(refs.edited_titles(old, new), {})

    def test_title_undo_and_redo(self):
        old = dict(text='Alt', spans=[dict(tag='taskref:a', start=0, end=3)])
        new = dict(text='Neu', spans=[dict(tag='taskref:a', start=0, end=3)])
        self.assertEqual(refs.undo_titles(new, old, {'a': ('active', dict(text='Neu'), None)}), {'a': 'Alt'})
        self.assertEqual(refs.undo_titles(old, new, {'a': ('active', dict(text='Alt'), None)}), {'a': 'Neu'})

    def test_title_undo_preserves_external_change(self):
        old = dict(text='Alt', spans=[dict(tag='taskref:a', start=0, end=3)])
        new = dict(text='Neu', spans=[dict(tag='taskref:a', start=0, end=3)])
        self.assertEqual(refs.undo_titles(new, old, {'a': ('active', dict(text='Anderswo'), None)}), {})

    def test_title_undo_keeps_missing_target(self):
        old = dict(text='Alt', spans=[dict(tag='taskref:a', start=0, end=3)])
        new = dict(text='Neu', spans=[dict(tag='taskref:a', start=0, end=3)])
        self.assertEqual(refs.undo_titles(new, old, {}), {})

    def test_title_undo_preserves_external_change_after_view_refresh(self):
        old = dict(text='Alt', spans=[dict(tag='taskref:a', start=0, end=3)])
        new = dict(text='Neu', spans=[dict(tag='taskref:a', start=0, end=3)])
        live = dict(text='Extern', spans=[dict(tag='taskref:a', start=0, end=6)])
        self.assertEqual(refs.undo_titles(live, old, {'a': ('active', dict(text='Extern'), None)},
                         prior_document=new, prior_titles={'a': 'Extern'}), {})


if __name__ == '__main__':
    unittest.main()
