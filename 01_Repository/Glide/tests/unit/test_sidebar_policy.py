import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src/glide'))
from sidebar_policy import SidebarPolicy,accepts,normalize_visibility,normalize_locations,template_allowed,sibling_ids

class PolicyTests(unittest.TestCase):
 def test_all_kinds(self):
  for kind,values in [('list',['tasks','page','note','drawing','gallery','future']),('folder',['standard','library','journal','future'])]:
   for value in values:
    self.assertTrue(accepts('lists',kind,value))
    allowed={'pages':{'list':{'page'},'folder':{'standard','library'}},'notes':{'list':{'note'},'folder':{'standard','journal'}},'drawings':{'list':{'drawing'},'folder':{'standard'}}}
    for section in allowed:self.assertEqual(accepts(section,kind,value),value in allowed[section][kind])
 def test_defaults_and_overrides(self):
  es=[{'id':k,'list_kind':k} for k in ['page','note','drawing','tasks','gallery']]
  p=SidebarPolicy(es,[],{'list:page':'lists'})
  self.assertEqual([p.section('list',e['id']) for e in es],['lists','notes','drawings','lists','lists'])
 def test_hidden_and_mandatory(self):
  self.assertTrue(normalize_visibility({'lists':False})['lists'])
  p=SidebarPolicy([{'id':'a','list_kind':'drawing'}],[],visibility={'drawings':False})
  self.assertEqual(p.section('list','a'),'lists')
 def test_nested_and_mixed_legacy(self):
  fs=[{'id':'a','folder_kind':'library'},{'id':'b','parent_id':'a','folder_kind':'standard'}]
  es=[{'id':'c','folder_id':'b','list_kind':'page'}]
  self.assertEqual(SidebarPolicy(es,fs).section('list','c'),'pages')
  es.append({'id':'d','folder_id':'b','list_kind':'drawing'})
  p=SidebarPolicy(es,fs)
  self.assertEqual(p.section('folder','a'),'lists');self.assertEqual(p.section('list','c'),'lists')
 def test_empty_standard_folder_assignment(self):
  p=SidebarPolicy([], [{'id':'a'}],{'folder:a':'drawings'})
  self.assertEqual(p.section('folder','a'),'drawings')
 def test_bad_settings_cycle_unknown(self):
  self.assertEqual(normalize_locations({'list:a':'bad','oops':'pages'}),{})
  p=SidebarPolicy([], [{'id':'a','parent_id':'b'},{'id':'b','parent_id':'a'}])
  self.assertEqual(p.section('folder','a'),'lists');self.assertFalse(p.subtree_accepts('a','pages'))
 def test_portable_template_payload(self):
  template={'kind':'folder','payload':{'folders':[{'folder_kind':'library'},{'folder_kind':'standard'}],'lists':[{'list_kind':'page'}]}}
  self.assertTrue(template_allowed(template,'pages'));self.assertFalse(template_allowed(template,'drawings'))
  template['payload']['lists'].append({'list_kind':'drawing'})
  self.assertFalse(template_allowed(template,'pages'));self.assertTrue(template_allowed(template,'lists'))
 def test_journal_takes_dated_drawings(self):
  self.assertTrue(accepts('notes','list','drawing','journal'))
  for container in (None,'standard','library'):self.assertFalse(accepts('notes','list','drawing',container))
  for kind in ('tasks','page','gallery'):self.assertFalse(accepts('notes','list',kind,'journal'))
  self.assertFalse(accepts('pages','list','drawing','journal'));self.assertFalse(accepts('notes','folder','drawing','journal'))
  fs=[{'id':'j','folder_kind':'journal'},{'id':'u','parent_id':'j','folder_kind':'journal'},{'id':'s','folder_kind':'standard'}]
  es=[{'id':'n','folder_id':'j','list_kind':'note'},{'id':'d','folder_id':'u','list_kind':'drawing'}]
  p=SidebarPolicy(es,fs)
  self.assertEqual([p.section('folder','j'),p.section('list','d')],['notes','notes'])
  es.append({'id':'t','folder_id':'j','list_kind':'tasks'})
  self.assertEqual(SidebarPolicy(es,fs).section('folder','j'),'lists')
  p=SidebarPolicy([{'id':'x','folder_id':'s','list_kind':'drawing'}],fs,{'folder:s':'notes'})
  self.assertEqual(p.section('folder','s'),'lists')
 def test_template_in_journal(self):
  self.assertTrue(template_allowed({'kind':'list','list_kind':'drawing'},'notes','journal'))
  self.assertFalse(template_allowed({'kind':'list','list_kind':'drawing'},'notes'))
  self.assertTrue(template_allowed({'kind':'folder','folder_kind':'journal','lists':[{'list_kind':'drawing'}]},'notes'))
  self.assertFalse(template_allowed({'kind':'folder','folder_kind':'standard','lists':[{'list_kind':'drawing'}]},'notes'))
  template={'kind':'folder','payload':{'folders':[{'id':'j','folder_kind':'journal'}],'lists':[{'list_kind':'drawing','folder_id':'j'}]}}
  self.assertTrue(template_allowed(template,'notes'))
  template['payload']['lists'].append({'list_kind':'drawing'})
  self.assertFalse(template_allowed(template,'notes'));self.assertTrue(template_allowed(template,'notes','journal'))
 def test_siblings_respect_area_and_parent(self):
  es=[{'id':'p','list_kind':'page'},{'id':'n','list_kind':'note'},{'id':'q','list_kind':'page'},{'id':'x','list_kind':'page','folder_id':'f'}]
  p=SidebarPolicy(es,[{'id':'f','folder_kind':'standard'}])
  self.assertEqual(sibling_ids(p,'list','p'),['p','q']);self.assertEqual(sibling_ids(p,'list','x'),['x'])
  self.assertEqual(sibling_ids(p,'list','unknown'),[])
if __name__=='__main__':unittest.main()
