"""Echter Einzelrestore mit Archiv, Writer, Änderungsrahmen und Undo; ohne Tk."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from test_source_schema_bridge import m


class PageRestoreBridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='glide-seitenrestore-bruecke-')
        self.addCleanup(self.temp.cleanup);self.base=Path(self.temp.name)
        for name,value in {'BASE_DIR':str(self.base),'BACKUP_DIR':str(self.base/'backups'),
                           'ATTACHMENTS_DIR':str(self.base/'attachments'),
                           'SAVE_FILE':str(self.base/'liste.json'),
                           'SETTINGS_FILE':str(self.base/'settings.json')}.items():
            p=patch.object(m,name,value);p.start();self.addCleanup(p.stop)
        (self.base/'attachments').mkdir()
        self.app=m.ListApp.__new__(m.ListApp);a=self.app
        a.settings={};a.labels=[];a.folders=[];a.trash=[];a.history=[];a.undo_stack=[]
        a.dirty=False;a._data_read_only=False;a.active_folder_id=None;a.view_mode='list'
        self.errors=[]
        for name in ('clear_render_cache','refresh_data_lock','flush_drawing_editor',
                     'save_settings','refresh_reminder_status','remember_written_data_format',
                     'record_recent_list_edits','update_sidebar_list','refresh_tree',
                     'show_undo_toast','update_history','finish_page_switch',
                     'feedback','note_page_opened'):
            setattr(a,name,lambda *args,**kw:None)
        a.show_error=lambda *args,**kw:self.errors.append(args)
        a.show_warning=a.show_info=lambda *args,**kw:None
        a.current_drawing_editor=lambda:None
        a.prepare_inspector_switch=lambda:True;a.flush_rich_note=lambda:True
        a.list_comparison=lambda **kw:SimpleNamespace(parts={})
        a.write_backup_copy=lambda **kw:None
        for version in (12,13,14,15,16,17,18,19,20,21):
            setattr(a,'ensure_schema'+str(version)+'_backup',lambda:None)
        a.ensure_schema_backup=lambda _v:None
        self.png=m.glide_drawing.DrawingModel.blank(16).to_png()
        self.stored=a.normalize_attachments([dict(id='bild',storage='attachments/quelle.png',
            name='Quelle.png',size=len(self.png),mime='image/png',added_at='2026-10-10T10:00:00')])[0]
        (self.base/'attachments/quelle.png').write_bytes(self.png)
        self.saved=a.new_list_object('Quellseite',[a.new_item('Gesicherte Aufgabe')],list_id='seite',
                    list_kind='page',rich_note={'text':'Gesicherter Text','spans':[],'links':{}},
                    attachments=[self.stored],live_lists=[m.glide_objects.uri('list','andere')])
        self.saved['rich_note']=m.glide_page_markdown.markdown_to_page('Gesicherter Text\n\n![Foto](quelle.png)',
            lambda *_:('img:'+'a'*16,dict(attachment='bild',mode='left',width=360)))
        self.saved['rich_note']=m.RichNoteEditor.normalize(self.saved['rich_note'])
        self.saved['cover']=dict(kind='image',attachment='bild')
        self.saved['notion_source']=m.glide_notion_reimport.SourceRecord('notion:'+'a'*32,'seite','b'*64,
            m.glide_notion_reimport.content_fingerprint(self.saved,{'bild':hashlib.sha256(self.png).hexdigest()}),
            'Projekt.md').to_document()
        self.other=a.new_list_object('Andere Seite',[a.new_item('Andere Aufgabe')],list_id='andere')
        current=copy.deepcopy(self.saved);current['rich_note']['text']+='\nHeute verändert'
        current['items'].append(a.new_item('Zusätzlich heute erfasst'))
        self.inbox=a.new_list_object('Eingang',[],list_id='inbox',system_role='inbox')
        a.lists=[current,self.other,self.inbox];a.active_list_id='seite';a.items=current['items'];a.app_title=current['title']
        a.ensure_inbox_list()
        self.archive=self.base/'sicherung.glidebackup'
        payload=dict(a.complete_backup_payload(),lists=[self.saved,self.other,self.inbox])
        a.write_complete_backup(self.archive,payload)
        self.assertTrue(a.save_items())
        self.snapshot=a.read_page_restore_backup(self.archive)
        self.plan=m.glide_page_restore.prepare(copy.deepcopy(a.data_payload()),self.snapshot.data,'seite',
                                               self.snapshot.available())
        self.assets=self.snapshot.capture_assets((v['storage']for v in self.plan.attachments),
                           max_member_bytes=a.MAX_BACKUP_ATTACHMENT_BYTES,max_total_bytes=a.MAX_BACKUP_TOTAL_BYTES)

    def test_real_restore_preserves_other_page_and_has_one_undo(self):
        a=self.app;before_other=copy.deepcopy(self.other);before_page=copy.deepcopy(a.page_entry('seite'))
        self.archive.write_bytes(b'Nach der Vorschau ersetzt')
        self.assertTrue(a.apply_page_restore(self.plan,self.snapshot,self.assets))
        self.assertEqual(next(v for v in a.lists if v['id']=='andere'),before_other)
        self.assertEqual(a.page_entry('seite')['rich_note']['text'],self.saved['rich_note']['text'])
        self.assertEqual(len(a.undo_stack),1)
        self.assertEqual(next(v for v in m.unpack_state(a.undo_stack[0]['lists']) if v['id']=='seite'),before_page)
        self.assertEqual(a.data_item_ids(),set(a.data_item_ids())|{before_page['items'][-1]['id']})
        restored=a.page_entry('seite');asset=restored['attachments'][0]
        self.assertNotEqual(asset['id'],'bild')
        self.assertEqual(Path(a.resolve_attachment_path(asset)).read_bytes(),self.png)
        self.assertEqual(restored['rich_note']['images']['img:'+'a'*16]['attachment'],asset['id'])
        self.assertEqual(restored['cover']['attachment'],asset['id'])
        self.assertEqual(restored['live_lists'],self.saved['live_lists'])
        self.assertEqual(restored['notion_source']['local_hash'],m.glide_notion_reimport.content_fingerprint(
            restored,{asset['id']:hashlib.sha256(self.png).hexdigest()}))
        self.assertEqual(json.loads(Path(m.SAVE_FILE).read_text())['lists'],a.lists)
        self.assertEqual(len(list((self.base/'backups').glob('vor_seitenrestore_*.glidebackup'))),1)

    def test_actual_undo_restores_all_original_pages_and_disk_bytes(self):
        a=self.app;before=copy.deepcopy(a.data_payload())
        self.assertTrue(a.apply_page_restore(self.plan,self.snapshot,self.assets))
        self.assertEqual(len(a.undo_stack),1)
        a.undo_last_change()
        self.assertEqual(a.lists,before['lists']);self.assertEqual(a.trash,before['trash'])
        self.assertEqual(a.labels,before['labels']);self.assertEqual(a.undo_stack,[])
        self.assertEqual(json.loads(Path(m.SAVE_FILE).read_text())['lists'],before['lists'])
        self.assertEqual((self.base/'attachments/quelle.png').read_bytes(),self.png)

    def test_real_atomic_writer_failure_rolls_back_memory_files_and_undo(self):
        a=self.app;before=copy.deepcopy(a.data_payload());original=Path(m.SAVE_FILE).read_bytes()
        undo=[dict(older='erhalten')];a.undo_stack[:]=undo
        with patch.object(m.ListApp,'replace_with_retry',side_effect=OSError('synthetischer Datenträgerfehler')):
            self.assertFalse(a.apply_page_restore(self.plan,self.snapshot,self.assets))
        self.assertEqual(a.data_payload(),before);self.assertEqual(a.undo_stack,undo)
        self.assertEqual(Path(m.SAVE_FILE).read_bytes(),original)
        self.assertEqual(list((self.base/'attachments').iterdir()),[self.base/'attachments/quelle.png'])
        self.assertEqual((self.base/'attachments/quelle.png').read_bytes(),self.png)

    def test_integrity_guard_rollback_never_keeps_new_files_or_reports_success(self):
        a=self.app;before=copy.deepcopy(a.data_payload());probe=a.data_item_ids;calls=[0]
        missing=before['lists'][1]['items'][0]['id']
        def inconsistent_once():
            calls[0]+=1
            found=probe()
            return found-{missing} if calls[0]==2 else found
        with patch.object(a,'data_item_ids',side_effect=inconsistent_once):
            self.assertFalse(a.apply_page_restore(self.plan,self.snapshot,self.assets))
        self.assertEqual(a.lists,before['lists']);self.assertEqual(a.trash,before['trash'])
        self.assertEqual(a.undo_stack,[])
        self.assertEqual(json.loads(Path(m.SAVE_FILE).read_text())['lists'],before['lists'])
        self.assertEqual(list((self.base/'attachments').iterdir()),[self.base/'attachments/quelle.png'])

    def test_prebackup_failure_creates_no_new_attachment_or_undo(self):
        before=copy.deepcopy(self.app.data_payload())
        with patch.object(self.app,'write_complete_backup',side_effect=OSError('Vorsicherung gesperrt')):
            with self.assertRaisesRegex(OSError,'Vorsicherung'):
                self.app.apply_page_restore(self.plan,self.snapshot,self.assets)
        self.assertEqual(self.app.data_payload(),before);self.assertEqual(self.app.undo_stack,[])
        self.assertEqual(len(list((self.base/'attachments').iterdir())),1)

    def test_changed_live_data_after_preview_aborts_before_prebackup(self):
        next(v for v in self.app.lists if v['id']=='andere')['title']='Zwischenzeitliche Änderung'
        with patch.object(self.app,'write_complete_backup') as writer:
            with self.assertRaisesRegex(ValueError,'Bestand hat sich geändert'):
                self.app.apply_page_restore(self.plan,self.snapshot,self.assets)
            writer.assert_not_called()
        self.assertEqual(next(v for v in self.app.lists if v['id']=='andere')['title'],'Zwischenzeitliche Änderung')

    def test_readonly_aborts_without_files_and_cancelled_preview_keeps_page(self):
        self.app._data_read_only=True
        self.assertFalse(self.app.apply_page_restore(self.plan,self.snapshot,self.assets))
        self.app._data_read_only=False;self.app.page_restore_preview=lambda *_:False
        before=copy.deepcopy(self.app.data_payload())
        self.assertFalse(self.app.restore_page_from_backup(path=self.archive,page_id='seite'))
        self.assertEqual(self.app.data_payload(),before);self.assertEqual(self.app.undo_stack,[])
        self.assertFalse((self.base/'backups').exists())

    def test_backup_normalization_never_replaces_current_collections(self):
        folders,labels,trash=self.app.folders,self.app.labels,self.app.trash
        self.app._loaded_history=['eigener temporärer Lesestand']
        snapshot=self.app.read_page_restore_backup(self.archive)
        self.assertIs(self.app.folders,folders);self.assertIs(self.app.labels,labels);self.assertIs(self.app.trash,trash)
        self.assertEqual(self.app._loaded_history,['eigener temporärer Lesestand'])
        self.assertEqual(snapshot.data['lists'][0]['list_kind'],'page')


if __name__=='__main__':unittest.main()
