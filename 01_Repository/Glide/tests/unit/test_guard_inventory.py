import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]/'src/glide'))
from structural_guard import data_item_ids, item_ids, trash_item_ids


class GuardInventory(unittest.TestCase):
    def test_current_list_and_item_trash_include_all_descendants(self):
        lists = [{'id': 'live-list', 'items': [{'id': 'live', 'children': [{'id': 'live-child'}]}]}]
        trash = [{'kind': 'list', 'list': {'id': 'deleted-list', 'items': [
            {'id': 'deleted', 'children': [{'id': 'deleted-child'}]}]}},
            {'kind': 'item', 'item': {'id': 'point', 'children': [{'id': 'point-child'}]}},
            {'kind': 'folder', 'folder': {'id': 'folder'}}]
        before = copy.deepcopy((lists, trash))
        self.assertEqual(data_item_ids(lists, trash), {
            'live', 'live-child', 'deleted', 'deleted-child', 'point', 'point-child'})
        self.assertEqual((lists, trash), before)

    def test_legacy_payload_forms_remain_supported(self):
        records = [{'payload': {'id': 'p'}}, {'payload': [{'id': 'q'}]},
                   {'items': [{'id': 'r'}]}, {'items': {'id': 's'}},
                   {'payload': {'id': 'container', 'items': [{'id': 't'}]}}]
        self.assertEqual(trash_item_ids(records), {'p', 'q', 'r', 's', 't'})

    def test_typed_task_unknown_items_field_is_not_reinterpreted_as_list(self):
        record = {'kind': 'item', 'item': {'id': 'task', 'items': [{'id': 'future-field'}]}}
        self.assertEqual(trash_item_ids([record]), {'task'})

    def test_invalid_records_and_existing_into_set(self):
        self.assertEqual(trash_item_ids([None, 7, {}, {'list': None}, {'item': []}]), set())
        into = {'before'}
        self.assertIs(item_ids([None, {'id': 'after'}], into), into)
        self.assertEqual(into, {'before', 'after'})


if __name__ == '__main__':
    unittest.main()
