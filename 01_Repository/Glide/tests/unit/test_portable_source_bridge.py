"""Quellenbindung durch tatsächliche portable Sicherungen/Restore, ohne Tk."""
import copy
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import zipfile
import test_page_restore_bridge as bridge
m=bridge.m


class PortableSourceBridgeTests(unittest.TestCase):
    def setUp(self):
        self.fixture=bridge.PageRestoreBridgeTests();self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.a=self.fixture.app;self.base=self.fixture.base
        self.operations=[]
        self.a.record_data_operation=lambda *args:self.operations.append(args)
        def select(identity,refresh=True):
            self.a.active_list_id=identity
            entry=next(v for v in self.a.lists if v['id']==identity)
            self.a.items=entry['items'];self.a.app_title=entry['title']
        self.a.set_active_list=select

    def state(self):
        return copy.deepcopy(self.a.data_payload()),Path(m.SAVE_FILE).read_bytes(),list(self.a.undo_stack),self.files()

    def files(self):
        return {p.name:p.read_bytes() for p in (self.base/'attachments').iterdir()}

    def assert_preserved(self,before):
        data,disk,undo,files=before
        self.assertEqual(self.a.data_payload(),data)
        self.assertEqual(Path(m.SAVE_FILE).read_bytes(),disk)
        self.assertEqual(self.a.undo_stack,undo)
        self.assertEqual(self.files(),files)

    def current_hashes(self):
        hashes,files,issues=m.glide_notion_import.current_sources(self.a.lists,self.a.resolve_attachment_path,
                                                                max_bytes=self.a.MAX_BACKUP_TOTAL_BYTES)
        self.assertEqual(issues,())
        return hashes

    def test_actual_portable_restore_reanchors_clean_images_cover_and_reimport_state(self):
        before=copy.deepcopy(self.a.data_payload());raw=self.fixture.archive.read_bytes()
        self.assertTrue(self.a.import_full_backup(path=self.fixture.archive,confirm=False,show_success=False),
                        self.fixture.errors)
        self.assertEqual(self.fixture.archive.read_bytes(),raw)
        page=self.a.page_entry('seite');asset=page['attachments'][0]
        self.assertNotEqual(asset['id'],'bild');self.assertNotEqual(asset['storage'],'attachments/quelle.png')
        self.assertEqual(Path(self.a.resolve_attachment_path(asset)).read_bytes(),self.fixture.png)
        self.assertEqual(page['rich_note']['images']['img:'+'a'*16]['attachment'],asset['id'])
        self.assertEqual(page['cover']['attachment'],asset['id'])
        self.assertEqual(page['live_lists'],self.fixture.saved['live_lists'])
        self.assertEqual(self.current_hashes()['seite'],page['notion_source']['local_hash'])
        self.assertEqual(len(self.a.undo_stack),1)
        self.assertEqual(len(list((self.base/'backups').glob('vor_import_*.glidebackup'))),1)
        stored=json.loads(Path(m.SAVE_FILE).read_text())
        self.assertEqual(stored['lists'],self.a.lists)
        pages,_=self.a.normalize_lists_data(stored)
        hashes,_files,issues=m.glide_notion_import.current_sources(pages,self.a.resolve_attachment_path,
                                                                 max_bytes=self.a.MAX_BACKUP_TOTAL_BYTES)
        self.assertEqual(issues,());self.assertEqual(hashes['seite'],page['notion_source']['local_hash'])
        self.a.undo_last_change()
        self.assertEqual(self.a.lists,before['lists']);self.assertEqual(self.a.trash,before['trash'])
        self.assertEqual(json.loads(Path(m.SAVE_FILE).read_text())['lists'],before['lists'])
        self.assertEqual((self.base/'attachments/quelle.png').read_bytes(),self.fixture.png)

    def test_local_edits_in_saved_source_remain_conflicts_after_actual_file_relocation(self):
        archive=self.base/'lokal-bearbeitet.glidebackup'
        self.a.write_complete_backup(archive,self.a.complete_backup_payload())
        baseline=self.a.page_entry('seite')['notion_source']['local_hash']
        self.assertNotEqual(self.current_hashes()['seite'],baseline)
        self.assertTrue(self.a.import_full_backup(path=archive,confirm=False,show_success=False),self.fixture.errors)
        page=self.a.page_entry('seite')
        self.assertIn('Heute verändert',page['rich_note']['text'])
        self.assertEqual(page['notion_source']['local_hash'],baseline)
        self.assertNotEqual(self.current_hashes()['seite'],baseline)
        self.assertNotEqual(page['attachments'][0]['id'],'bild')

    def test_additive_import_keeps_live_binding_and_makes_independent_copies(self):
        before=copy.deepcopy(self.a.lists)
        self.assertTrue(self.a.import_full_backup(path=self.fixture.archive,additive=True,
                                               confirm=False,show_success=False),self.fixture.errors)
        for original in before:self.assertEqual(next(v for v in self.a.lists if v['id']==original['id']),original)
        copies=[v for v in self.a.lists if v['id'] not in {p['id']for p in before}]
        self.assertTrue(copies)
        self.assertTrue(all('notion_source' not in p for p in copies))
        self.assertEqual(len(m.glide_source_metadata.records(self.a.lists)),1)
        page=next(v for v in copies if v['list_kind']=='page')
        self.assertEqual(Path(self.a.resolve_attachment_path(page['attachments'][0])).read_bytes(),self.fixture.png)
        self.assertEqual(len(self.a.undo_stack),1)
        self.a.undo_last_change();self.assertEqual(self.a.lists,before)

    def test_incomplete_archive_aborts_before_prebackup_and_preserves_everything(self):
        before=self.state();broken=self.base/'unvollstaendig.glidebackup'
        with zipfile.ZipFile(self.fixture.archive)as old,zipfile.ZipFile(broken,'w')as new:
            new.writestr('data.json',old.read('data.json'))
        with patch.object(self.a,'write_complete_backup')as writer:
            self.assertFalse(self.a.import_full_backup(path=broken,confirm=False,show_success=False))
            writer.assert_not_called()
        self.assert_preserved(before)
        self.assertTrue(any('unvollständig' in str(e)for e in self.fixture.errors))

    def test_failed_final_atomic_write_removes_new_files_and_restores_undo(self):
        before=self.state();write=self.a.write_json_atomic;calls=[]
        def fail_final(path,data):
            if str(path)==str(m.SAVE_FILE):
                calls.append(copy.deepcopy(data))
                if len(calls)==2:raise OSError('synthetischer finaler Restore-Schreibfehler')
            return write(path,data)
        with patch.object(self.a,'write_json_atomic',side_effect=fail_final):
            self.assertFalse(self.a.import_full_backup(path=self.fixture.archive,confirm=False,show_success=False))
        self.assertEqual(len(calls),2)
        self.assert_preserved(before)
        self.assertTrue(any('finaler Restore-Schreibfehler' in str(e)for e in self.fixture.errors))

    def test_refused_prebackup_never_installs_staged_files_or_changes_bindings(self):
        before=self.state()
        with patch.object(self.a,'write_complete_backup',side_effect=OSError('Vorsicherung verweigert')):
            self.assertFalse(self.a.import_full_backup(path=self.fixture.archive,confirm=False,show_success=False))
        self.assert_preserved(before)
        self.assertFalse(list(self.base.glob('.glide-import-*')))


if __name__=='__main__':unittest.main()
