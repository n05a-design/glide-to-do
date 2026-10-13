"""Archivübernahme durch tatsächliche App-Speicher-/Undo-Wege, ohne Tk."""
import copy
import hashlib
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import zipfile
import test_page_restore_bridge as restore_bridge
m=restore_bridge.m


class NotionBridgeTests(unittest.TestCase):
    def setUp(self):
        self.fixture=restore_bridge.PageRestoreBridgeTests();self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.a=self.fixture.app;self.base=self.fixture.base
        stream=io.BytesIO()
        with zipfile.ZipFile(stream,'w')as archive:
            archive.writestr('Neu '+'c'*32+'.md','# Neu\n\n- [ ] Importierte Aufgabe\n\n![Foto](foto.png)')
            archive.writestr('foto.png',self.fixture.png)
            archive.writestr('Daten.csv','Name,Wert\nBeispiel,1')
        self.raw=stream.getvalue();self.path=self.base/'Notion.zip';self.path.write_bytes(self.raw)
        def choose(export,comparison,page_ids):
            rows=[row for row in comparison.rows if row.status not in ('unchanged','local-only')]
            if not rows:return None
            return tuple(row.page.key for row in rows),tuple(row.page.key for row in rows if row.status=='conflict')
        self.a.notion_import_preview=choose

    def test_real_archive_import_files_source_state_restart_and_actual_undo(self):
        a=self.a;before=copy.deepcopy(a.data_payload())
        self.assertTrue(a.import_notion_archive(path=self.path),self.fixture.errors)
        imported=next(p for p in a.lists if p['title']=='Neu')
        self.assertEqual(len(imported['items']),1);self.assertEqual(len(imported['rich_note']['images']),1)
        report=next(p for p in a.lists if p['title']=='Notion-Importbericht')
        self.assertIn('CSV-Datenbank',report['rich_note']['text'])
        self.assertEqual(Path(a.resolve_attachment_path(report['attachments'][0])).read_bytes(),self.raw)
        self.assertEqual(Path(a.resolve_attachment_path(imported['attachments'][0])).read_bytes(),self.fixture.png)
        for original in before['lists']:
            self.assertEqual(next(p for p in a.lists if p['id']==original['id']),original)
        saved=json.loads(Path(m.SAVE_FILE).read_text());pages,_active=a.normalize_lists_data(saved)
        hashes,files,issues=m.glide_notion_import.current_sources(pages,a.resolve_attachment_path,max_bytes=a.MAX_BACKUP_TOTAL_BYTES)
        self.assertEqual(issues,())
        self.assertEqual(hashes[imported['id']],imported['notion_source']['local_hash'])
        self.assertEqual(len(a.undo_stack),1)
        self.assertEqual(len(list((self.base/'backups').glob('vor_notion_import_*.glidebackup'))),1)
        a.undo_last_change()
        self.assertEqual(a.lists,before['lists']);self.assertEqual(a.trash,before['trash'])
        self.assertEqual(a.undo_stack,[])
        self.assertEqual(json.loads(Path(m.SAVE_FILE).read_text())['lists'],before['lists'])

    def test_repeated_archive_is_unchanged_and_never_adds_a_report_or_undo(self):
        a=self.a;self.assertTrue(a.import_notion_archive(path=self.path))
        before=copy.deepcopy(a.data_payload());depth=len(a.undo_stack)
        observed=[];a.notion_import_preview=lambda export,comparison,ids:observed.extend(comparison.rows)
        self.assertFalse(a.import_notion_archive(path=self.path))
        self.assertEqual([row.status for row in observed],['unchanged'])
        self.assertEqual(a.lists,before['lists']);self.assertEqual(len(a.undo_stack),depth)

    def test_write_failure_and_prebackup_failure_preserve_current_files_and_undo(self):
        a=self.a;before=copy.deepcopy(a.data_payload());disk=Path(m.SAVE_FILE).read_bytes()
        files={p.name:p.read_bytes()for p in (self.base/'attachments').iterdir()}
        chooser=a.notion_import_preview;after_preview=[False]
        def choose_then_fail(*args):
            result=chooser(*args);after_preview[0]=True;return result
        a.notion_import_preview=choose_then_fail
        original_replace=a.replace_with_retry
        def failing_replace(*args,**kwargs):
            if after_preview[0]:raise OSError('synthetischer Schreibfehler nach Vorschau')
            return original_replace(*args,**kwargs)
        with patch.object(m.ListApp,'replace_with_retry',side_effect=failing_replace):
            self.assertFalse(a.import_notion_archive(path=self.path))
        self.assertTrue(after_preview[0])
        self.assertEqual(a.lists,before['lists']);self.assertEqual(a.undo_stack,[])
        self.assertEqual(Path(m.SAVE_FILE).read_bytes(),disk)
        self.assertEqual({p.name:p.read_bytes()for p in (self.base/'attachments').iterdir()},files)
        with patch.object(a,'write_complete_backup',side_effect=OSError('Vorsicherung verweigert')):
            self.assertFalse(a.import_notion_archive(path=self.path))
        self.assertEqual({p.name:p.read_bytes()for p in (self.base/'attachments').iterdir()},files)
        self.assertEqual(a.undo_stack,[])

    def test_changed_local_file_during_preview_blocks_before_backup(self):
        a=self.a;before=copy.deepcopy(a.lists)
        chooser=a.notion_import_preview
        def change(export,comparison,page_ids):
            (self.base/'attachments/quelle.png').write_bytes(b'Jetzt veraendert')
            return chooser(export,comparison,page_ids)
        a.notion_import_preview=change
        with patch.object(a,'write_complete_backup')as writer:
            self.assertFalse(a.import_notion_archive(path=self.path))
            writer.assert_not_called()
        self.assertEqual(a.lists,before);self.assertEqual(a.undo_stack,[])
        self.assertTrue(any('Anhangsdatei' in str(error)for error in self.fixture.errors))

    def test_changed_source_conflict_keeps_page_identity_and_preserves_previous_tasks(self):
        a=self.a;self.assertTrue(a.import_notion_archive(path=self.path))
        original=next(p for p in a.lists if p['title']=='Neu');identity=original['id']
        original['rich_note']['text']+='\nEigene Änderung'
        a.save_items();before=copy.deepcopy(original);old_task=copy.deepcopy(original['items'][0])
        stream=io.BytesIO()
        with zipfile.ZipFile(stream,'w')as archive:
            archive.writestr('Neu '+'c'*32+'.md','# Neue Quelle\n\n- [x] Erledigt')
        self.path.write_bytes(stream.getvalue())
        chooser=a.notion_import_preview;observed=[]
        def choose(export,cmp,ids):
            observed.extend(cmp.rows);return chooser(export,cmp,ids)
        a.notion_import_preview=choose
        self.assertTrue(a.import_notion_archive(path=self.path),self.fixture.errors)
        self.assertEqual([r.status for r in observed],['conflict'])
        page=next(p for p in a.lists if p['id']==identity)
        self.assertEqual(page['title'],'Neue Quelle');self.assertTrue(page['items'][0]['done'])
        self.assertIn(old_task,[entry['item']for entry in a.trash if entry['kind']=='item'])
        self.assertEqual(len(a.undo_stack),2)
        a.undo_last_change()
        self.assertEqual(next(p for p in a.lists if p['id']==identity),before)

    def test_original_archive_is_immutable_and_cancellation_or_readonly_creates_nothing(self):
        a=self.a;chooser=a.notion_import_preview
        def replaced(export,comparison,ids):
            self.path.write_bytes(b'Zwischenzeitlich ersetzt')
            return chooser(export,comparison,ids)
        a.notion_import_preview=replaced
        self.assertTrue(a.import_notion_archive(path=self.path),self.fixture.errors)
        report=next(p for p in a.lists if p['title']=='Notion-Importbericht')
        self.assertEqual(Path(a.resolve_attachment_path(report['attachments'][0])).read_bytes(),self.raw)
        before=copy.deepcopy(a.lists);files=set((self.base/'attachments').iterdir());depth=len(a.undo_stack)
        a._data_read_only=True
        self.assertFalse(a.import_notion_archive(path=self.path))
        a._data_read_only=False;self.path.write_bytes(self.raw);a.notion_import_preview=lambda *_:None
        self.assertFalse(a.import_notion_archive(path=self.path))
        self.assertEqual(a.lists,before);self.assertEqual(len(a.undo_stack),depth)
        self.assertEqual(set((self.base/'attachments').iterdir()),files)

    def test_local_file_change_while_staging_aborts_and_removes_staged_files(self):
        a=self.a;before=copy.deepcopy(a.lists);stage=m.glide_restore_assets.stage
        files={p.name:p.read_bytes()for p in (self.base/'attachments').iterdir()}
        def change_after_stage(*args,**kwargs):
            result=stage(*args,**kwargs)
            (self.base/'attachments/quelle.png').write_bytes(b'Extern waehrend der Vorbereitung geaendert')
            return result
        with patch.object(m.glide_restore_assets,'stage',side_effect=change_after_stage):
            self.assertFalse(a.import_notion_archive(path=self.path))
        self.assertEqual(a.lists,before);self.assertEqual(a.undo_stack,[])
        self.assertEqual({p.name for p in (self.base/'attachments').iterdir()},set(files))
        self.assertEqual((self.base/'attachments/quelle.png').read_bytes(),b'Extern waehrend der Vorbereitung geaendert')
        self.assertTrue(any('Vorbereiten geändert' in str(error)for error in self.fixture.errors))

    def test_subpages_appear_under_pages_and_undo_restores_sidebar_locations(self):
        a=self.a;before=copy.deepcopy(a.settings.get('sidebar_locations',{}))
        stream=io.BytesIO()
        with zipfile.ZipFile(stream,'w')as archive:
            archive.writestr('Projekt '+'d'*32+'/Unterseite '+'e'*32+'.md','# Unterseite')
        self.path.write_bytes(stream.getvalue())
        self.assertTrue(a.import_notion_archive(path=self.path),self.fixture.errors)
        page=next(p for p in a.lists if p['title']=='Unterseite')
        self.assertIsNotNone(page['folder_id'])
        self.assertEqual(a.sidebar_section_for('list',page['id']),'pages')
        self.assertEqual(a.sidebar_section_for('folder',page['folder_id']),'pages')
        a.undo_last_change()
        self.assertEqual(a.settings.get('sidebar_locations'),before)


if __name__=='__main__':unittest.main()
