"""Echte Format-25-Bestandsbrücke ohne Tk-Fenster, ausschließlich künstliche Daten."""
import copy
from contextlib import nullcontext
import hashlib
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest

W=Path(__file__).resolve().parents[1]
DATA=tempfile.TemporaryDirectory(prefix='glide-source-bruecke-')
os.environ.update(GLIDE_DATA_DIR=DATA.name,GLIDE_TEST_MODE='1')
SRC=W.parent/'src/glide'
sys.path.insert(0,str(SRC))
loader=importlib.machinery.SourceFileLoader('glide_schema3410',str(SRC/'app.pyw'))
m=importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name,loader))
sys.modules[loader.name]=m;loader.exec_module(m)


class SourceSchemaBridge(unittest.TestCase):
    def setUp(self):
        self.app=m.ListApp.__new__(m.ListApp)
        self.app.labels=[];self.app.settings={};self.app.lists=[];self.app.folders=[];self.app.trash=[]
        self.app.flush_rich_note=lambda:True

    def page(self,identity='seite'):
        page=self.app.new_list_object('Projekt',list_id=identity,list_kind='page',rich_note={'text':'Quelltext','spans':[],'links':{}})
        page['notion_source']=m.glide_notion_reimport.SourceRecord('notion:'+'a'*32,identity,'b'*64,
                m.glide_notion_reimport.content_fingerprint(page,{}),'Projekt.md').to_document()
        return page

    def test_constructor_owns_independent_mapping_and_keeps_old_features(self):
        original=self.page();before=copy.deepcopy(original)
        page=self.app.new_list_object('Projekt',list_id='seite',list_kind='page',notion_source=original['notion_source'])
        self.assertEqual(page['notion_source'],original['notion_source'])
        page['notion_source']['source_path']='anders.md';self.assertEqual(original,before)
        self.assertTrue(hasattr(m.ListApp,'process_daily_hints'))
        animation=m.glide_animation.Animation.from_legacy(m.glide_drawing.DrawingModel.blank(16).to_document())
        animation.duplicate('frame-1',new_identity='zweites-bild')
        drawing=self.app.new_list_object('Bildfolge',list_kind='drawing',**m.glide_animation.entry_fields(animation))
        self.assertEqual(len(drawing['animation']['frames']),2)

    def test_live_and_trashed_pages_keep_mapping_without_mutating_input(self):
        page=self.page();data={'version':25,'lists':[page],'trash':[{'id':'geloescht','kind':'list','list':page}]};before=copy.deepcopy(data)
        lists,_=self.app.normalize_lists_data(data)
        self.assertEqual(lists[0]['notion_source'],page['notion_source'])
        self.assertEqual(self.app.trash[0]['list']['notion_source'],page['notion_source'])
        self.assertEqual(data,before)

    def test_source_mapping_requires_format25_and_page_owner(self):
        page=self.page()
        with self.assertRaisesRegex(ValueError,'Datenformat 25'):
            self.app.normalize_lists_data({'version':24,'lists':[page]})
        for identity,kind in (('andere','page'),('seite','tasks')):
            with self.assertRaisesRegex(ValueError,'Quellenzuordnung'):
                self.app.new_list_object('Projekt',list_id=identity,list_kind=kind,notion_source=page['notion_source'])

    def test_live_source_duplicates_are_rejected(self):
        a=self.page();b=self.page('andere')
        with self.assertRaisesRegex(ValueError,'nicht eindeutig'):
            self.app.normalize_lists_data({'version':25,'lists':[a,b]})

    def test_folder_mapping_survives_live_and_trash_normalization(self):
        key='notion:'+'c'*32
        folder=self.app.new_folder_object('Mein lokaler Name',folder_id='ordner',notion_source_key=key)
        data={'version':25,'lists':[self.page()],'folders':[folder],
              'trash':[{'id':'geloeschter-ordner','kind':'folder','folder':folder}]}
        before=copy.deepcopy(data)
        self.app.normalize_lists_data(data)
        self.assertEqual(self.app.folders[0]['notion_source_key'],key)
        self.assertEqual(self.app.folders[0]['title'],'Mein lokaler Name')
        self.assertEqual(self.app.trash[0]['folder']['notion_source_key'],key)
        self.assertEqual(data,before)
        self.assertNotIn('notion_source_key',self.app.new_folder_object('Neue unabhängige Kopie'))

    def test_folder_mapping_format_duplicates_and_invalid_paths_are_rejected(self):
        key='notion:'+'c'*32
        folder=self.app.new_folder_object('Quelle',folder_id='ordner',notion_source_key=key)
        for field,value in (('folders',[folder]),('trash',[{'kind':'folder','folder':folder}])):
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'Datenformat 25'):
                self.app.check_stored_list_kinds({field:value},24)
        other=dict(folder,id='zweiter')
        with self.assertRaisesRegex(ValueError,'nicht eindeutig'):
            self.app.check_stored_list_kinds({'folders':[folder,other]},25)
        with self.assertRaisesRegex(ValueError,'Ordnerzuordnung'):
            self.app.new_folder_object('Defekt',notion_source_key='../Quelle.md')

    def test_real_trash_restore_keeps_source_without_duplicating_a_live_mapping(self):
        self.app.prune_unknown_item_labels=lambda:None
        original=self.page()
        self.app.trash=[{'id':'weg','kind':'list','list':original}]
        self.assertTrue(self.app.restore_trash_entry('weg',save=False))
        self.assertEqual(self.app.lists[-1]['notion_source'],original['notion_source'])
        self.app.trash=[{'id':'zweite-kopie','kind':'list','list':original}]
        self.assertTrue(self.app.restore_trash_entry('zweite-kopie',save=False))
        self.assertNotIn('notion_source',self.app.lists[-1])
        self.assertNotEqual(self.app.lists[-1]['id'],original['id'])

    def test_real_folder_trash_restore_preserves_only_a_unique_live_source(self):
        self.app.prune_unknown_item_labels=lambda:None
        original=self.app.new_folder_object('Quelle',folder_id='quellordner',notion_source_key='notion:'+'e'*32)
        for number in range(2):
            self.app.trash=[{'id':'weg','kind':'folder','folder':original}]
            self.assertTrue(self.app.restore_trash_entry('weg',save=False,cascade=False))
            if number==0:
                self.assertEqual(self.app.folders[-1]['notion_source_key'],original['notion_source_key'])
            else:
                self.assertNotIn('notion_source_key',self.app.folders[-1])

    def test_real_page_copy_is_an_independent_source_target(self):
        original=self.page();before=copy.deepcopy(original)
        self.app.lists=[original]
        self.app.guarded_structural_change=lambda *_:nullcontext(SimpleNamespace(aborted=False))
        self.app.sidebar_change=lambda **_:nullcontext(SimpleNamespace(saved=True,mark=lambda:None))
        self.app.sync_current_list_reference=lambda:None
        self.app.set_active_list=lambda *_:None
        self.assertEqual(self.app.duplicate_list(original['id']),'break')
        self.assertEqual(original,before)
        self.assertNotIn('notion_source',self.app.lists[-1])
        self.assertEqual(len(m.glide_source_metadata.records(self.app.lists)),1)

    def test_additive_backup_remaps_independent_copies_and_keeps_source_input(self):
        page=self.page();folder=self.app.new_folder_object('Quelle',folder_id='ordner',notion_source_key='notion:'+'e'*32)
        page['folder_id']=folder['id'];before=copy.deepcopy((page,folder))
        pages,folders,_=self.app.prepare_additive_import([page],[folder],[])
        self.assertEqual((page,folder),before)
        self.assertNotIn('notion_source',pages[0]);self.assertNotIn('notion_source_key',folders[0])
        self.assertNotEqual(pages[0]['id'],page['id'])
        self.assertEqual(pages[0]['folder_id'],folders[0]['id'])

    def test_actual_backup_asset_remap_reanchors_clean_source_and_image_targets(self):
        page=self.page();png=m.glide_drawing.DrawingModel.blank(16).to_png();digest=hashlib.sha256(png).hexdigest()
        page['attachments']=self.app.normalize_attachments([{'id':'foto','name':'Quelle.png',
            'storage':'attachments/quelle.png','size':len(png),'mime':'image/png'}])
        page['rich_note']['images']={'bild':{'attachment':'foto','mode':'left','width':360}}
        page['cover']={'kind':'image','attachment':'foto','position':50}
        page['notion_source']['local_hash']=m.glide_notion_reimport.content_fingerprint(page,{'foto':digest})
        before=copy.deepcopy(([page],[]))
        storage_map=self.app.remap_import_attachments([page],[],[])
        attachment=page['attachments'][0]
        self.assertNotEqual(attachment['id'],'foto')
        self.assertEqual(page['rich_note']['images']['bild']['attachment'],attachment['id'])
        self.assertEqual(page['cover']['attachment'],attachment['id'])
        with tempfile.TemporaryDirectory(prefix='glide-dateiumzug-bruecke-') as directory:
            staged=Path(directory)/'quelle.png';staged.write_bytes(png)
            after_hashes=m.glide_source_metadata.staged_source_hashes(([page],[]),
                {attachment['storage']:staged},max_bytes=len(png))
            old_hashes={old:after_hashes[new]for old,new in storage_map.items()}
            actual=m.glide_source_metadata.relocated_collections(before,([page],[]),old_hashes,after_hashes)[0][0]
        self.assertEqual(actual['notion_source']['local_hash'],
            m.glide_notion_reimport.content_fingerprint(actual,{attachment['id']:digest}))

    def test_backup_validator_rejects_misdeclared_source_metadata(self):
        page=self.page()
        data={'app':m.APP_NAME,'version':25,'lists':[page],'folders':[],'labels':[],'trash':[]}
        self.assertEqual(self.app.validate_backup_schema(data,portable=True),set())
        with self.assertRaisesRegex(ValueError,'Datenformat 25'):
            self.app.validate_backup_schema(dict(data,version=24),portable=True)

    def test_format25_backup_failure_precedes_history_and_write(self):
        calls=[];writes=[]
        self.app.clear_render_cache=self.app.refresh_data_lock=self.app.sync_current_list_reference=lambda:None
        for version in (12,13,14,15,16,17,18,19,20,21):
            setattr(self.app,'ensure_schema'+str(version)+'_backup',lambda:None)
        def guard(version):
            calls.append(version)
            if version==25:raise OSError('synthetisch verweigerte Format-25-Vorsicherung')
        self.app.ensure_schema_backup=guard
        self.app.list_comparison=lambda **kw:writes.append('history')
        self.app.write_json_atomic=lambda *args:writes.append('file')
        self.assertFalse(self.app.save_items(show_error=False))
        self.assertEqual(calls,[22,23,24,25]);self.assertEqual(writes,[])


if __name__=='__main__':unittest.main()
