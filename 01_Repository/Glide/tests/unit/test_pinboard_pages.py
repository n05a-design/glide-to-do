import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[2]/'src/glide'))
import pinboard_pages as pages
from page_features import card_summary


class PageCardTests(unittest.TestCase):
    def test_excerpt_and_task_count_nested(self):
        entry = {'rich_note': {'text': '  A\n B '+('Wort '*80)+'\ufffc'}, 'items': [
            {'id': 'i', 'kind': 'group', 'children': [{'id':'j'}, {'id':'k', 'done':True}]}]}
        text, count = card_summary(entry)
        self.assertLessEqual(len(text), 160)
        self.assertTrue(text.startswith('A B '))
        self.assertEqual(count, 1)

    def test_legacy_namespace_and_cross_edge_roundtrip_without_mutation(self):
        data = {'pinboards': {'global': {'cards': [
            {'item_id': 'page:p', 'list_id': 'p', 'x': 70},
            {'item_id': 'page:d', 'list_id': 'd', 'x': 1},
            {'item_id': 't', 'list_id': 'l', 'x': 3}],
            'connections': [{'from':'page:p','to':'t','label':'Kontext'}], 'zoom':125}}}
        before = copy.deepcopy(data)
        stored = pages.persist(data, [{'id':'p','list_kind':'page'}, {'id':'d','list_kind':'drawing'}])
        self.assertEqual(data, before)
        self.assertNotIn('page:p', str(stored['pinboards']))
        self.assertIn('page:d', str(stored['pinboards']))
        self.assertEqual(pages.restore(stored), data)

    def test_remove_does_not_resurrect_card(self):
        stored = pages.persist({'pinboards': {'global': {'cards':[{'item_id':'page:p','list_id':'p'}], 'connections':[]}}}, [{'id':'p','list_kind':'page'}])
        data = pages.restore(stored)
        data['pinboards']['global']['cards'].clear()
        saved = pages.persist(data, [{'id':'p','list_kind':'page'}])
        self.assertNotIn(pages.KEY, saved)
        self.assertFalse(pages.restore(saved)['pinboards']['global']['cards'])

    def test_roundtrip_preserves_more_than_one_thousand_scopes(self):
        page_id = 'f' * 32
        data = {'pinboards': {
            'list:' + format(index, '032x'): {
                'cards': [{'item_id': 'page:' + page_id, 'list_id': page_id,
                           'x': index, 'y': 70}],
                'connections': [], 'zoom': 125}
            for index in range(1001)}}
        before = copy.deepcopy(data)
        stored = pages.persist(data, [{'id': page_id, 'list_kind': 'page'}])
        stored_before = copy.deepcopy(stored)
        self.assertEqual(len(stored[pages.KEY]), 1001)
        restored = pages.restore(stored)
        self.assertEqual(restored, data)
        self.assertEqual(data, before)
        self.assertEqual(stored, stored_before)

    def test_malformed_extension_is_bounded(self):
        for value in (None, 7, [], 'falsch', {'global':{'cards':7,'connections':'x'}}):
            result = pages.restore({pages.KEY:value, 'pinboards':{}})
            self.assertIsInstance(result['pinboards'], dict)


if __name__ == '__main__':unittest.main()
