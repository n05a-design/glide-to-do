# SPDX-License-Identifier: MPL-2.0
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src/glide'))
import copy
import unittest
import object_references as refs

class ObjectReferencesTests(unittest.TestCase):
    def test_typed_ids_validation_and_dedup(self):
        self.assertEqual(refs.parse('glide://list/same'),('list','same'))
        self.assertEqual(refs.parse('glide://item/same'),('item','same'))
        self.assertEqual(refs.parse(refs.uri('item','Altbestand / ä')),('item','Altbestand / ä'))
        self.assertIsNone(refs.parse('glide://item/%00'))
        for value in ['file:///etc/passwd','https://test','glide://folder/a','glide://item/','glide://item/a?x=1']:
            self.assertIsNone(refs.parse(value))
        self.assertEqual(refs.normalize(['glide://list/a']*2),['glide://list/a'])
        with self.assertRaises(ValueError):refs.normalize(['bad'])
        with self.assertRaises(ValueError):refs.normalize(['glide://list/a']*201)

    def test_graph_backlinks_use_ids_and_current_state(self):
        a={'id':'same','title':'Seite','references':['glide://list/b'],
           'rich_note':{'links':{'link:a':'glide://item/same','link:unused':'glide://list/missing'},
                        'spans':[{'tag':'link:a','start':0,'end':1}]},'items':[]}
        b={'id':'b','title':'Liste','items':[{'id':'same','text':'Aufgabe','references':['glide://list/same'],'children':[]}]}
        lists=[a,b];previous=copy.deepcopy(lists)
        index,outgoing,incoming=refs.graph(lists)
        self.assertEqual(outgoing[('list','same')],{('list','b'),('item','same')})
        self.assertEqual(incoming[('list','same')],{('item','same')})
        self.assertEqual(lists,previous)
        b['title']='Neuer Titel';b['archived']=True
        index,_,_=refs.graph(lists)
        self.assertIn('Neuer Titel',refs.caption(('item','same'),index)[1])
        self.assertEqual(refs.caption(('item','same'),index)[0],'archived')
        self.assertEqual(refs.caption(('list','missing'),index),('missing','Ziel fehlt'))
        b['items'][0]['text']='Erste Zeile\nZweite Zeile'
        self.assertNotIn('\n',refs.caption(('item','same'),refs.nodes(lists))[1])
        index,_,incoming=refs.graph([a],[{'list':b}])
        self.assertEqual(refs.caption(('item','same'),index)[0],'trash')
        self.assertIn(('list','same'),incoming[('item','same')])

    def test_remap_all_typed_links_external_target_preserved(self):
        holder={'references':['glide://list/a','glide://item/a','glide://list/external'],
                'rich_note':{'links':{'link:1':'glide://list/a','link:2':'https://example.test'}}}
        refs.remap_holder(holder,{'a':'newlist'},{'a':'newtask'})
        self.assertEqual(holder['references'],['glide://list/newlist','glide://item/newtask','glide://list/external'])
        self.assertEqual(holder['rich_note']['links']['link:1'],'glide://list/newlist')
        self.assertEqual(holder['rich_note']['links']['link:2'],'https://example.test')

    def test_usage_locations_covers_home_references_rich_links_live_lists_relations_pinboards_and_mentions(self):
        folders=[{'id':'f1','title':'Projektordner','parent_id':None}]
        page={'id':'p1','title':'Architekturseite','list_kind':'page','folder_id':'f1',
              'live_lists':['glide://list/l1'],
              'rich_note':{'text':'Siehe Arbeitsliste\nEingebettete Aufgabe\nVerweis auf Zielaufgabe',
                           'links':{'link:1':'glide://item/t1'},
                           'spans':[{'tag':'item:t_owned','start':19,'end':39},
                                    {'tag':'taskref:t1','start':40,'end':63},
                                    {'tag':'link:1','start':40,'end':63}]},
              'items':[{'id':'t_owned','text':'Eingebettete Aufgabe','children':[]}]}
        task_list={'id':'l1','title':'Arbeitsliste','folder_id':'f1',
                   'references':['glide://list/p1'],
                   'items':[{'id':'t1','text':'Zielaufgabe',
                             'references':['glide://list/p1'],
                             'links':['t2'],'blocked_by':['t2'],
                             'children':[{'id':'t_sub','text':'Unteraufgabe','children':[]}]},
                            {'id':'t2','text':'Nachbaraufgabe','links':['t1'],'blocked_by':['t1'],'children':[]}]}
        pinboards={
            'global':{'cards':[{'item_id':'t1','list_id':'l1','x':48,'y':96},
                               {'item_id':'page:p1','list_id':'p1','x':320,'y':96}],
                      'connections':[{'from':'t1','to':'page:p1','style':'forward'}]},
            'folder:f1':{'cards':[{'item_id':'t1','list_id':'l1','x':24,'y':24}],'connections':[]},
        }
        lists=[page,task_list]

        task_locs=refs.usage_locations(('item','t1'),lists,folders=folders,pinboards=pinboards)
        kinds=[loc.kind for loc in task_locs]
        self.assertIn('home',kinds)
        self.assertIn('rich_link',kinds)
        self.assertIn('task_line',kinds)
        self.assertIn('relation',kinds)
        self.assertIn('pinboard',kinds)
        self.assertTrue(any(loc.kind=='pinboard' and loc.scope=='global' and '1 Verbindung' in loc.detail for loc in task_locs))

        sub_locs=refs.usage_locations(('item','t_sub'),lists,folders=folders,pinboards=pinboards)
        self.assertTrue(any(loc.kind=='home' and 'Unterpunkt von „Zielaufgabe“' in loc.detail for loc in sub_locs))

        owned_locs=refs.usage_locations(('item','t_owned'),lists,folders=folders,pinboards=pinboards)
        self.assertTrue(any(loc.kind=='home' and loc.line==2 and 'Heimatzeile 2' in loc.detail for loc in owned_locs))

        list_locs=refs.usage_locations(('list','l1'),lists,folders=folders,pinboards=pinboards)
        list_kinds=[loc.kind for loc in list_locs]
        self.assertIn('home',list_kinds)
        self.assertIn('live_list',list_kinds)
        self.assertIn('mention',list_kinds)

        page_locs=refs.usage_locations(('list','p1'),lists,folders=folders,pinboards=pinboards)
        page_kinds=[loc.kind for loc in page_locs]
        self.assertIn('home',page_kinds)
        self.assertIn('reference',page_kinds)
        self.assertIn('pinboard',page_kinds)

if __name__=='__main__':
    unittest.main()
