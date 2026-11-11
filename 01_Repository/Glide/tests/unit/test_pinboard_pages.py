# SPDX-License-Identifier: MPL-2.0
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

    def test_zoomed_image_by_type(self):
        # macOS lädt Vorschauen als nsimage: kein zoom/subsample, sondern neu in Zielgröße.
        self.assertEqual(pages.zoomed_image('photo', 120, 80, 1.5), ('photo', 6, 4))
        self.assertEqual(pages.zoomed_image('photo', 120, 80, 0.75), ('photo', 3, 4))
        self.assertEqual(pages.zoomed_image('nsimage', 120, 80, 1.5), ('nsimage', 180, 120))
        self.assertEqual(pages.zoomed_image('nsimage', 3, 1, 0.25), ('nsimage', 1, 1))
        self.assertIsNone(pages.zoomed_image('bitmap', 10, 10, 2))

    def test_export_json_canvas_nodes_edges_and_loss_report(self):
        board = {
            'layout': 'free',
            'width': 300,
            'areas': [
                {'id': 'a1', 'name': 'Sprint-Ziele', 'color': 'clear', 'x': 10, 'y': 20, 'w': 600, 'h': 400},
            ],
            'cards': [
                {'item_id': 't1', 'list_id': 'l1', 'x': 40, 'y': 60},
                {'item_id': 'page:p1', 'list_id': 'p1', 'x': 400, 'y': 60},
                {'item_id': 'hidden', 'list_id': 'l1', 'x': 800, 'y': 60},
            ],
            'connections': [
                {'from': 't1', 'to': 'page:p1', 'style': 'forward', 'label': 'belegt', 'color': 'export', 'dash': True},
                {'from': 't1', 'to': 'hidden', 'style': 'line'},
            ],
        }
        cards_info = [
            {
                'id': 't1',
                'x': 40,
                'y': 60,
                'width': 300,
                'height': 180,
                'title': 'Architektur prüfen',
                'done': False,
                'importance_label': 'Hohe Priorität',
                'due': '12.11.2026',
                'source_title': 'Kernliste',
                'description': 'Schnittstellen abgleichen',
                'checklist': [{'text': 'Schema lesen', 'done': True}, {'text': 'Tests ergänzen', 'done': False}],
                'labels': ['Wichtig', 'Kern'],
                'attachments_count': 2,
                'color': 'priority_high',
            },
            {
                'id': 'page:p1',
                'x': 400,
                'y': 60,
                'width': 300,
                'height': 150,
                'title': 'Spezifikation',
                'is_page': True,
                'kind_label': 'Seite',
                'description': 'Auszug der Seite · 3 offene Aufgaben',
                'color': 'accent',
            },
        ]
        doc, report = pages.export_json_canvas(board, cards_info, scope_title='Globale Pinnwand')
        self.assertEqual(set(doc.keys()), {'nodes', 'edges'})
        self.assertEqual(report.areas_count, 1)
        self.assertEqual(report.cards_count, 2)
        self.assertEqual(report.edges_count, 1)

        group_nodes = [n for n in doc['nodes'] if n['type'] == 'group']
        text_nodes = [n for n in doc['nodes'] if n['type'] == 'text']
        self.assertEqual(len(group_nodes), 1)
        self.assertEqual(group_nodes[0]['label'], 'Sprint-Ziele')
        self.assertEqual(group_nodes[0]['color'], '5')
        self.assertEqual(len(text_nodes), 2)
        t1_node = next(n for n in text_nodes if n['id'] == 't1')
        self.assertIn('### [ ] Architektur prüfen', t1_node['text'])
        self.assertIn('- [x] Schema lesen', t1_node['text'])
        self.assertIn('`glide://item/t1`', t1_node['text'])
        p1_node = next(n for n in text_nodes if n['id'] == 'page:p1')
        self.assertIn('### Spezifikation (Seite)', p1_node['text'])
        self.assertIn('`glide://list/p1`', p1_node['text'])

        edge = doc['edges'][0]
        self.assertEqual(edge['fromNode'], 't1')
        self.assertEqual(edge['toNode'], 'page:p1')
        self.assertEqual(edge['fromSide'], 'right')
        self.assertEqual(edge['toSide'], 'left')
        self.assertEqual(edge['fromEnd'], 'none')
        self.assertEqual(edge['toEnd'], 'arrow')
        self.assertEqual(edge['label'], 'belegt')
        self.assertEqual(edge['color'], '4')

        summary = report.summary_text()
        self.assertIn('Globale Pinnwand', summary)
        self.assertIn('gestrichelte Verbindung', summary)
        self.assertIn('Checklisten', summary)
        self.assertIn('Dateianhänge', summary)
        self.assertIn('ausgeblendete oder nicht mehr vorhandene Karte', summary)


if __name__ == '__main__':unittest.main()
