"""Originalreferenzen und Suchsemantik der kurzlebigen ID-Projektion."""
import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
from item_index import ItemIndex


def recursive(identity, siblings, parent=None):
    for position, item in enumerate(siblings):
        if item.get('id') == identity:
            return item, siblings, position, parent
        found = recursive(identity, item.get('children', ()), item)
        if found:
            return found


class IndexTests(unittest.TestCase):
    def setUp(self):
        self.items = [dict(id='a', children=[dict(id='b'), dict(id='c', children=[dict(id='d')])]),
                      dict(id='c', text='doppelt'), dict(text='ohne ID')]

    def test_matches_recursive_and_keeps_original_references(self):
        index = ItemIndex(self.items)
        for identity in ['a', 'b', 'c', 'd', 'fehlt']:
            found, expected = index.get(identity), recursive(identity, self.items)
            self.assertEqual(found, expected)
            if found:
                self.assertIs(found[0], expected[0])
                self.assertIs(found[1], expected[1])
                self.assertIs(found[3], expected[3])

    def test_list_context_and_selection_order(self):
        lists = [dict(id='l1', items=self.items), dict(id='l2', items=[dict(id='e')])]
        index = ItemIndex(lists=lists)
        self.assertIs(index.in_list('d')[3], lists[0])
        self.assertIs(index.in_list('e')[3], lists[1])
        self.assertEqual(list(index.selected(['e', 'b', 'e', 'fehlt'])), ['e', 'b'])
        self.assertIsNone(index.in_list('fehlt'))

    def test_rebuild_after_replacement_move_and_delete(self):
        previous = ItemIndex(self.items)
        fresh = copy.deepcopy(self.items)
        fresh[0]['children'][0]['text'] = 'nach Undo'
        fresh.append(fresh[0]['children'].pop(0))
        index = ItemIndex(fresh)
        self.assertIsNot(index.get('b')[0], previous.get('b')[0])
        self.assertIsNone(index.get('b')[3])
        self.assertEqual(index.get('b')[2], len(fresh) - 1)
        fresh.pop()
        self.assertIsNone(ItemIndex(fresh).get('b'))

    def test_deep_tree_uses_no_python_recursion(self):
        roots = []; children = roots
        for number in range(1500):
            row = dict(id=str(number), children=[]); children.append(row); children = row['children']
        self.assertEqual(ItemIndex(roots).get('1499')[0]['id'], '1499')
