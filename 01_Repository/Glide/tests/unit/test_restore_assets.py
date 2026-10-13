from pathlib import Path
import copy
import io
import tempfile
import unittest
from unittest.mock import patch
import restore_assets


def attachment(identity='old',raw=b'PNG'):
    return dict(id=identity,storage='attachments/'+identity+'.png',size=len(raw),name='Foto.png',
                mime='image/png',title='Titel',note='Notiz',added_at='früher')

class AssetsTest(unittest.TestCase):
    def test_copy_metadata_keep_and_original_unchanged(self):
        original=attachment();before=copy.deepcopy(original)
        with tempfile.TemporaryDirectory()as folder:
            directory=Path(folder);(directory/'old.png').write_bytes(b'Bestehend')
            with restore_assets.stage([original],directory,lambda _p:io.BytesIO(b'PNG'),max_bytes=10,
                                      new_id=lambda:'new',now='heute')as result:
                self.assertEqual((directory/'new.png').read_bytes(),b'PNG')
                self.assertEqual(result.metadata['old'],dict(original,id='new',storage='attachments/new.png'))
                result.keep()
            self.assertEqual((directory/'old.png').read_bytes(),b'Bestehend')
            self.assertTrue((directory/'new.png').is_file())
        self.assertEqual(original,before)

    def test_missing_historical_timestamp_uses_supplied_fallback(self):
        original=attachment();original.pop('added_at')
        with tempfile.TemporaryDirectory() as folder:
            with restore_assets.stage([original],folder,lambda _p:io.BytesIO(b'PNG'),max_bytes=10,
                                      new_id=lambda:'new',now='heute') as result:
                self.assertEqual(result.metadata['old']['added_at'],'heute')
        self.assertNotIn('added_at',original)

    def test_aborted_preview_or_backup_leaves_no_new_files(self):
        with tempfile.TemporaryDirectory()as folder:
            directory=Path(folder)
            with restore_assets.stage([attachment()],directory,lambda _p:io.BytesIO(b'PNG'),max_bytes=10,
                                      new_id=lambda:'new'):
                self.assertTrue((directory/'new.png').exists())
            self.assertEqual(list(directory.iterdir()),[])

    def test_partial_failure_removes_only_owned_files(self):
        for raw in (b'XX',b'XXXX'):
            with self.subTest(raw=raw),tempfile.TemporaryDirectory()as folder:
                directory=Path(folder);existing=directory/'bestehend';existing.write_bytes(b'Erhalten')
                ids=iter(('new1','new2'))
                def source(storage):return io.BytesIO(b'PNG'if'old1'in storage else raw)
                with self.assertRaises(ValueError):
                    restore_assets.stage([attachment('old1'),attachment('old2')],directory,source,
                                         max_bytes=10,new_id=lambda:next(ids))
                self.assertEqual([p.name for p in directory.iterdir()],['bestehend'])
                self.assertEqual(existing.read_bytes(),b'Erhalten')

    def test_collision_is_retried_without_overwriting(self):
        with tempfile.TemporaryDirectory()as folder:
            directory=Path(folder);existing=directory/'NEW.png';existing.write_bytes(b'Behalten')
            ids=iter((None,'../unsafe','old','new','ok'))
            with restore_assets.stage([attachment()],directory,lambda _p:io.BytesIO(b'PNG'),max_bytes=10,
                                      new_id=lambda:next(ids))as result:
                self.assertEqual(result.metadata['old']['id'],'ok')
                result.keep()
            self.assertEqual(existing.read_bytes(),b'Behalten')
            with self.assertRaises(OSError):
                restore_assets.stage([attachment()],directory,lambda _p:io.BytesIO(b'PNG'),max_bytes=10,
                                     new_id=lambda:'old')

    def test_unrelated_names_and_replaced_path_are_never_removed(self):
        with tempfile.TemporaryDirectory()as folder:
            directory=Path(folder);(directory/'unbekannt-fremd.bin').write_bytes(b'Fremd')
            result=restore_assets.stage([attachment()],directory,lambda _p:io.BytesIO(b'PNG'),max_bytes=10,new_id=lambda:'new')
            created=directory/'new.png';created.unlink();created.symlink_to(directory/'unbekannt-fremd.bin')
            result.cleanup()
            self.assertTrue(created.is_symlink())
            self.assertEqual(created.read_bytes(),b'Fremd')
            self.assertEqual((directory/'unbekannt-fremd.bin').read_bytes(),b'Fremd')

    def test_read_and_fsync_errors_roll_back(self):
        with tempfile.TemporaryDirectory()as folder:
            directory=Path(folder)
            with patch.object(restore_assets.os,'fsync',side_effect=OSError('Datenträger voll')):
                with self.assertRaises(OSError):
                    restore_assets.stage([attachment()],directory,lambda _p:io.BytesIO(b'PNG'),max_bytes=10,new_id=lambda:'new')
            self.assertEqual(list(directory.iterdir()),[])
            def failure(_p):raise OSError('Archiv unlesbar')
            with self.assertRaises(OSError):restore_assets.stage([attachment()],directory,failure,max_bytes=10,new_id=lambda:'new')
            self.assertEqual(list(directory.iterdir()),[])

if __name__=='__main__':unittest.main()
