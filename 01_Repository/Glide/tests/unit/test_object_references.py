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

if __name__=='__main__':
    unittest.main()
