import copy
from types import SimpleNamespace
import unittest
from notion_hierarchy import prepare, restored_source_key

K='notion:'+'a'*32
J='notion:'+'b'*32
P='notion:'+'c'*32
Q='notion:'+'d'*32

def page(key=P,folders=((K,'Projekt'),(J,'Unterseiten'))):
    return SimpleNamespace(key=key,folders=folders)


class HierarchyTests(unittest.TestCase):
    def test_shared_ancestors_are_created_once_without_mutating_existing_data(self):
        folders=[{'id':'ziel','title':'Ziel','parent_id':None}];before=copy.deepcopy(folders)
        ids=iter(('projekt','unterseiten'))
        plan=prepare([page(),page(Q)],folders,target_folder_id='ziel',new_id=lambda:next(ids))
        self.assertEqual([f.parent_id for f in plan.folders],['ziel','projekt'])
        self.assertEqual(plan.page_folders,((P,'unterseiten'),(Q,'unterseiten')))
        self.assertEqual(folders,before)

    def test_bound_folder_keeps_local_title_and_parent(self):
        folders=[{'id':'manuell','parent_id':None},{'id':'projekt','title':'Eigener Titel','parent_id':'manuell','notion_source_key':K}]
        plan=prepare([page(folders=((K,'Quelltitel'),))],folders)
        self.assertEqual(plan.folders,())
        self.assertEqual(plan.page_folders,((P,'projekt'),))
        self.assertEqual(folders[1]['title'],'Eigener Titel')

    def test_existing_page_keeps_current_folder(self):
        existing=[{'id':'seite','folder_id':'manuell','notion_source':{'key':P}}]
        plan=prepare([page()],[{'id':'manuell','parent_id':None}],existing)
        self.assertEqual(plan.folders,())
        self.assertEqual(plan.page_folders,((P,'manuell'),))

    def test_depth_limit_applies_to_real_target_chain(self):
        folders=[{'id':'ziel','parent_id':'a'},{'id':'a','parent_id':None}]
        with self.assertRaisesRegex(ValueError,'Ordnertiefe'):
            prepare([page()],folders,target_folder_id='ziel',max_depth=3)

    def test_archived_missing_and_cyclic_targets_are_rejected(self):
        for folders,target in (([], 'fehlt'),([{'id':'a','parent_id':None,'archived':True}],'a'),([{'id':'a','parent_id':'a'}],'a')):
            with self.assertRaises(ValueError):prepare([page()],folders,target_folder_id=target)

    def test_ambiguous_folder_binding_and_export_ancestry_are_rejected(self):
        with self.assertRaisesRegex(ValueError,'Mehrdeutige Notion'):
            prepare([page()],[{'id':'a','notion_source_key':K},{'id':'b','notion_source_key':K}])
        with self.assertRaisesRegex(ValueError,'nicht eindeutig'):
            prepare([page(),page(Q,((J,'Unterseiten'),))],[])

    def test_duplicate_pages_and_exhausted_ids_are_rejected(self):
        with self.assertRaisesRegex(ValueError,'mehrfach'):
            prepare([page(),page()],[])
        with self.assertRaisesRegex(ValueError,'freie Ordnerkennung'):
            prepare([page()],[{'id':'belegt','parent_id':None}],new_id=lambda:'belegt')

    def test_folder_ids_cannot_collide_with_existing_or_prepared_pages(self):
        for kwargs in ({"current_pages":[{"id":"belegt"}]},{"occupied_ids":["belegt"]}):
            with self.assertRaisesRegex(ValueError,"freie Ordnerkennung"):
                prepare([page()],[],new_id=lambda:'belegt',**kwargs)

    def test_root_page_needs_no_new_folder(self):
        plan=prepare([page(folders=())],[])
        self.assertEqual(plan.folders,())
        self.assertEqual(plan.page_folders,((P,None),))

    def test_trash_folder_source_is_preserved_unless_it_already_has_a_live_target(self):
        folder={'id':'alt','notion_source_key':K}
        self.assertEqual(restored_source_key(folder,[]),K)
        self.assertIsNone(restored_source_key(folder,[{'id':'neu','notion_source_key':K}]))
        self.assertEqual(restored_source_key(folder,[{'id':'anderer','notion_source_key':J}]),K)
        self.assertIsNone(restored_source_key({'id':'ohne'},[]))

    def test_trash_folder_rejects_ambiguous_live_targets(self):
        with self.assertRaisesRegex(ValueError,'nicht eindeutig'):
            restored_source_key({'notion_source_key':K},[{'notion_source_key':J},{'notion_source_key':J}])


if __name__=='__main__':unittest.main()
