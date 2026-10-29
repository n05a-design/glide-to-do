import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]/'src/glide'))
from task_editing import new_label_name, completed_ids, remove_planned, displaced_payloads


def task(identity, done=False, children=None, kind='task'):
    return {'id': identity, 'kind': kind, 'done': done, 'children': children or [],
            'future': {'nested': [False, None]}}


class BulkChanges(unittest.TestCase):
    def test_label_name_uses_current_count_casefold_and_length(self):
        self.assertEqual(new_label_name([], ' Neu ', max_labels=2, max_length=3), 'Neu')
        for labels, name in (([{'name': 'NEU'}], 'neu'), ([{}, {}], 'x'), ([], ''), ([], 'vier')):
            with self.assertRaises(ValueError):
                new_label_name(labels, name, max_labels=2, max_length=3)

    def test_selection_is_postorder_and_preserves_open_descendants_and_groups(self):
        data = [task('p', True, [task('c', True)]), task('keep', True, [task('open')]),
                task('group', True, kind='group')]
        original = copy.deepcopy(data)
        self.assertEqual(completed_ids(data, lambda i: i['kind'] == 'task'), ('c', 'p'))
        self.assertEqual(data, original)

    def test_payloads_do_not_duplicate_nested_ids_and_keep_origins(self):
        data = [task('p', True, [task('c', True)]), task('open')]
        original = copy.deepcopy(data)
        kept, removed = remove_planned(data, ('c', 'p'))
        self.assertEqual([i['id'] for i in kept], ['open'])
        self.assertEqual([(i['id'], parent, index) for i, parent, index in removed],
                         [('c', 'p', 0), ('p', None, 0)])
        self.assertTrue(all(not i['children'] for i, _, _ in removed))
        kept[0]['future']['nested'].append(9)
        removed[0][0]['future']['nested'].append(8)
        self.assertEqual(data, original)

    def test_nonselected_parent_keeps_open_children_and_unknown_fields(self):
        data = [task('p', True, [task('closed', True), task('open')])]
        kept, removed = remove_planned(data, ('closed',))
        self.assertEqual([i['id'] for i in kept[0]['children']], ['open'])
        self.assertEqual(kept[0]['future'], data[0]['future'])
        self.assertEqual(removed[0][1:], ('p', 0))

    def test_existing_retention_loss_is_precise_including_large_incoming_batch(self):
        old, incoming = ['a', 'b', 'c'], ['x', 'y']
        self.assertEqual(displaced_payloads(old, incoming, 3), ['b', 'c'])
        self.assertEqual(displaced_payloads(old, ['w', 'x', 'y', 'z'], 3), ['w', 'a', 'b', 'c'])
        self.assertEqual(displaced_payloads(old, [], 3), [])
        self.assertEqual((old, incoming), (['a', 'b', 'c'], ['x', 'y']))

    def test_invalid_retention_limit(self):
        for limit in (0, -1, False, 1.5):
            with self.assertRaises(ValueError):
                displaced_payloads([], [], limit)


if __name__ == '__main__':
    unittest.main()
