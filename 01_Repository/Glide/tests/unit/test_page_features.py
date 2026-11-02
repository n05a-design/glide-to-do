import copy
from datetime import date
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
import drawing
import object_references as refs
import page_features as pages


class PageFeaturesTests(unittest.TestCase):
    def test_block_move_preserves_formats_references_images_and_unicode(self):
        doc = {'text': '😀 Erst\nBild\nAufgabe', 'links': {'link:1': 'glide://list/a'},
               'images': {'img:1': {'attachment': 'a', 'width': 320, 'mode': 'center'}},
               'spans': [{'tag': 'bold', 'start': 0, 'end': 11},
                         {'tag': 'link:1', 'start': 2, 'end': 6},
                         {'tag': 'img:1', 'start': 7, 'end': 11},
                         {'tag': 'item:task1', 'start': 12, 'end': 19}]}
        prior = copy.deepcopy(doc)
        result, caret = pages.move_document_block(doc, 2, 3, 0)
        self.assertEqual(result['text'], 'Aufgabe\n😀 Erst\nBild')
        self.assertEqual(caret, 0)
        self.assertEqual(doc, prior)
        self.assertEqual(result['images'], doc['images'])
        self.assertEqual(result['links'], doc['links'])
        task = next(s for s in result['spans'] if s['tag'] == 'item:task1')
        self.assertEqual(result['text'][task['start']:task['end']], 'Aufgabe')
        link = next(s for s in result['spans'] if s['tag'] == 'link:1')
        self.assertEqual(result['text'][link['start']:link['end']], 'Erst')

    def test_block_move_boundaries_empty_lines_and_no_op(self):
        for text in ('A\nB\nC', 'A\nB\n', 'A\n\nB', '😀\nö\n三'):
            doc = {'text': text, 'spans': [], 'links': {}}
            rows = text.split('\n')
            result, _ = pages.move_document_block(doc, 0, 1, len(rows))
            self.assertEqual(result['text'], '\n'.join(rows[1:] + rows[:1]))
            self.assertEqual(pages.move_document_block(doc, 0, 1, 1)[0], doc)
        with self.assertRaises(ValueError):
            pages.move_document_block({'text': 'A'}, 1, 2, 0)

    def test_whole_code_table_and_toggle_blocks(self):
        doc = {'text': 'Kopf\nKind\nCode\nMehr\nEnde', 'spans': [
            {'tag': 'toggle', 'start': 0, 'end': 5},
            {'tag': 'indent1', 'start': 5, 'end': 10},
            {'tag': 'codeblock', 'start': 10, 'end': 20}]}
        self.assertEqual(pages.block_lines(doc, 0), (0, 2))
        self.assertEqual(pages.block_lines(doc, 3), (2, 4))
        doc['spans'][-1]['tag'] = 'table'
        self.assertEqual(pages.block_lines(doc, 2), (2, 4))

    def test_indented_children_follow_a_plain_parent_block(self):
        doc = {'text': 'Elternblock\nKind\nEnkel\nDanach', 'spans': [
            {'tag': 'indent1', 'start': 12, 'end': 17},
            {'tag': 'indent2', 'start': 17, 'end': 23}]}
        self.assertEqual(pages.block_lines(doc, 0), (0, 3))
        self.assertEqual(pages.block_lines(doc, 1), (1, 3))
        moved, _ = pages.move_document_block(doc, *pages.block_lines(doc, 0), 4)
        self.assertEqual(moved['text'], 'Danach\nElternblock\nKind\nEnkel')

    def test_live_validation_and_real_home_states(self):
        self.assertEqual(pages.live_lists(['glide://list/a'] * 2), ['glide://list/a'])
        for value in (['glide://item/a'], ['glide://list/a?x'], ['glide://list/a'] * 21, {}):
            with self.assertRaises(ValueError): pages.live_lists(value)
        source = {'id': 'a', 'title': 'Quelle', 'items': [{'id': 'x', 'text': 'Aufgabe', 'kind': 'task',
                  'done': False, 'children': [{'id': 'y', 'text': 'Kind', 'done': True}]}]}
        prior = copy.deepcopy(source)
        self.assertEqual([r[0] for r in pages.live_rows('glide://list/a', [source])[2]], ['x', 'y'])
        self.assertEqual(source, prior)
        source['folder_id'] = 'child'
        self.assertEqual(pages.live_rows('glide://list/a', [source], folders=[
            {'id':'child','parent_id':'root'}, {'id':'root','archived':True}])[0], 'archived')
        source['title'] = 'Umbenannt'; source['archived'] = True
        self.assertEqual(pages.live_rows('glide://list/a', [source])[:2], ('archived', 'Umbenannt'))
        self.assertEqual(pages.live_rows('glide://list/a', [], [{'kind':'list','payload':source}])[0], 'trash')
        self.assertEqual(pages.live_rows('glide://list/a', [])[0], 'missing')

    def test_live_graph_and_single_remap_preserve_external_sources(self):
        holder = {'id': 'p', 'title': 'Seite', 'live_lists': ['glide://list/a', 'glide://list/external'], 'items': []}
        self.assertEqual(refs.graph([holder])[2][('list', 'a')], {('list', 'p')})
        refs.remap_holder(holder, {'a': 'b', 'b': 'c'}, {})
        self.assertEqual(holder['live_lists'], ['glide://list/b', 'glide://list/external'])

    def test_cover_validation_and_drawing_snapshot(self):
        self.assertEqual(pages.cover({'kind': 'image', 'attachment': 'abc'}), {'kind':'image','attachment':'abc'})
        for value in ({'kind':'image','attachment':'../x'}, {'kind':'url','url':'https://x'}, 'x'):
            with self.assertRaises(ValueError): pages.cover(value)
        model = drawing.DrawingModel(size=16)
        original = {'kind':'drawing','document':model.to_document()}
        normalized = pages.cover(original)
        self.assertEqual(normalized, original)
        self.assertIsNot(normalized['document'], original['document'])

    def test_filled_preview_uses_same_dates_nested_content_and_no_mutation(self):
        record = {'title':'Projekt Alpha','kind':'list','schedule_anchor':'2026-10-01','payload':{'lists':[
            {'title':'Alt','rich_note':{'text':'Notiz Alpha'},'live_lists':['glide://list/ext'],
             'cover':{'kind':'image','attachment':'a'}, 'items':[{'id':'a','text':'Erledigt vorher','done':True,
             'due':'2026-10-03','planned_date':'2026-10-02','repeat':{'start':'2026-10-03'},
             'children':[{'id':'b','text':'Unteraufgabe','description':'Details'}]}]}]}}
        before = copy.deepcopy(record)
        prepared = pages.prepare_template(record, date(2026,10,8))
        self.assertEqual(record, before)
        task = prepared['payload']['lists'][0]['items'][0]
        self.assertFalse(task['done']); self.assertEqual(task['due'], '2026-10-10')
        self.assertEqual(task['planned_date'],'2026-10-09'); self.assertEqual(task['repeat']['start'],'2026-10-10')
        self.assertEqual(pages.prepare_template(prepared,date(2026,10,8)),prepared)
        preview = pages.template_preview(prepared)
        for value in ('Projekt Alpha','Notiz Alpha','Unteraufgabe','Details','2026-10-10','Live-Liste','Titelbild'):
            self.assertIn(value, preview)


    def test_template_destination_preserves_subfolders_and_original_ids(self):
        folders = [{'id':'root','parent_id':None},{'id':'child','parent_id':'root'}]
        lists = [{'id':'inside','folder_id':'child','live_lists':['glide://list/standalone']},
                 {'id':'standalone','folder_id':None}]
        before = copy.deepcopy((lists,folders))
        pages.place_roots(lists,folders,None)
        self.assertEqual((lists,folders),before)
        pages.place_roots(lists,folders,'existing')
        self.assertEqual(folders[0]['parent_id'],'existing')
        self.assertEqual(folders[1]['parent_id'],'root')
        self.assertEqual(lists[0],before[0][0])
        self.assertEqual(lists[1],{'id':'standalone','folder_id':'existing'})
        after=copy.deepcopy((lists,folders));pages.place_roots(lists,folders,'existing')
        self.assertEqual((lists,folders),after)


if __name__ == '__main__': unittest.main()
