import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]/'src/glide'))
import settings_compat as compat


class CompatibilityTests(unittest.TestCase):
    def test_unknown_nested_fields_survive_without_aliases(self):
        raw = {'name': ' unbereinigt ', 'future': {'nested': [1, False, None]}}
        before = copy.deepcopy(raw)
        result = compat.preserve(raw, {'name': 'bereinigt'}, {'name'})
        self.assertEqual(result['future'], raw['future'])
        self.assertEqual(result['name'], 'bereinigt')
        result['future']['nested'].append(3)
        self.assertEqual(raw, before)

    def test_invalid_known_and_ephemeral_fields_are_not_resurrected(self):
        result = compat.preserve({'id': 'f', '_view': {'x': 1}, '_layout': {},
                                  'query': 7, 'future': False}, {'id': 'f'}, compat.FILTER_FIELDS)
        self.assertEqual(result, {'id': 'f', 'future': False})
        self.assertEqual(compat.preserve({'dash': 'bad', 'future': []}, {}, compat.EDGE_FIELDS),
                         {'future': []})

    def test_opaque_card_has_explicit_type_or_namespace_and_bounded_identity(self):
        for value in ({'item_id': 'embed:x'}, {'item_id': 'x', 'kind': 'future'}):
            self.assertTrue(compat.opaque_card(value))
        for value in ({}, {'item_id': False}, {'item_id': 'x'*201, 'kind': 'future'},
                      {'item_id': 'task'}, {'item_id': 'page:deleted'},
                      {'item_id': 'x', 'kind': 'task'}, {'item_id': 'x', 'kind': False}):
            self.assertFalse(compat.opaque_card(value), value)

    def test_prune_keeps_unknown_edges_but_removes_known_deleted_objects(self):
        board = {'future': 5, 'cards': [
            {'item_id': 't', 'list_id': 'old'},
            {'item_id': 'embed:x', 'list_id': 'old', 'payload': {'nested': [False]}},
            {'item_id': 'deleted', 'list_id': 'old'},
            {'item_id': 'page:deleted', 'list_id': 'p'}],
            'connections': [{'from': 't', 'to': 'embed:x', 'future': {'x': 1}},
                            {'from': 't', 'to': 'deleted'}]}
        before = copy.deepcopy(board)
        cards, edges = compat.prune_cards(board, {'t': ({'id': 'new'}, {})})
        self.assertEqual([c['item_id'] for c in cards], ['t', 'embed:x'])
        self.assertEqual(cards[0]['list_id'], 'new')
        self.assertEqual(cards[1], board['cards'][1])
        self.assertEqual(edges, board['connections'][:1])
        cards[1]['payload']['nested'].append(9)
        self.assertEqual(board, before)


if __name__ == '__main__':
    unittest.main()
