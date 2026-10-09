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
