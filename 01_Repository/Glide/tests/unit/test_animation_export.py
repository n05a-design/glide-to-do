import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from animation_export import ExportRecoveryError, write_files


class AnimationExportTests(unittest.TestCase):
    def test_complete_new_output_and_explicit_replacement(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            files = {'bild.png': b'png', 'folge.json': b'json'}
            output = write_files(root, files)
            self.assertEqual({p.name: p.read_bytes() for p in output}, files)
            self.assertEqual(sorted(p.name for p in root.iterdir()), sorted(files))
            with self.assertRaises(FileExistsError):
                write_files(root, {'bild.png': b'neu'})
            write_files(root, {'bild.png': b'neu'}, replace=True)
            self.assertEqual((root / 'bild.png').read_bytes(), b'neu')
            self.assertEqual((root / 'folge.json').read_bytes(), b'json')

    def test_staging_error_preserves_existing_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'bild.png').write_bytes(b'vorher')
            with patch('animation_export.os.fsync', side_effect=OSError('voll')):
                with self.assertRaisesRegex(OSError, 'voll'):
                    write_files(root, {'bild.png': b'neu', 'folge.json': b'json'}, replace=True)
            self.assertEqual({p.name: p.read_bytes() for p in root.iterdir()}, {'bild.png': b'vorher'})

    def test_each_replace_failure_restores_all_previous_files(self):
        actual = os.replace
        for fail_at in (1, 2, 3, 4):
            with self.subTest(fail_at=fail_at), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                original = {'bild.png': b'vorher-png', 'folge.json': b'vorher-json'}
                for name, content in original.items():
                    (root / name).write_bytes(content)
                count = [0]
                def replace(*args):
                    count[0] += 1
                    if count[0] == fail_at:
                        raise OSError('absichtlicher Austauschfehler')
                    return actual(*args)
                with patch('animation_export.os.replace', side_effect=replace):
                    with self.assertRaisesRegex(OSError, 'Austauschfehler'):
                        write_files(root, {'bild.png': b'neu', 'folge.json': b'json'}, replace=True)
                self.assertEqual({p.name: p.read_bytes() for p in root.iterdir()}, original)

    def test_failed_new_output_leaves_no_reserved_or_partial_files(self):
        actual = os.replace
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            count = [0]
            def replace(*args):
                count[0] += 1
                if count[0] == 2:
                    raise OSError('zweite Datei')
                return actual(*args)
            with patch('animation_export.os.replace', side_effect=replace):
                with self.assertRaisesRegex(OSError, 'zweite Datei'):
                    write_files(root, {'bild.png': b'png', 'folge.json': b'json'})
            self.assertEqual(list(root.iterdir()), [])

    def test_failed_rollback_retains_backup_and_reports_location(self):
        actual = os.replace
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'bild.png').write_bytes(b'vorher')
            def replace(source, target):
                if Path(source).parent.name in ('neu', 'vorher'):
                    raise OSError('gesperrt')
                return actual(source, target)
            with patch('animation_export.os.replace', side_effect=replace):
                with self.assertRaises(ExportRecoveryError) as caught:
                    write_files(root, {'bild.png': b'neu'}, replace=True)
            staging = next(root.glob('.glide-animation-*'))
            self.assertIn(str(staging), str(caught.exception))
            self.assertEqual((staging / 'vorher/bild.png').read_bytes(), b'vorher')

    def test_invalid_names_and_symlinks_are_rejected_before_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ('../bild.png', 'a/b.png', 'a\\b.png', '.', '..', ''):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    write_files(root, {name: b'daten'})
            (root / 'extern').write_bytes(b'vorher')
            (root / 'bild.png').symlink_to(root / 'extern')
            with self.assertRaises(ValueError):
                write_files(root, {'bild.png': b'neu'}, replace=True)
            self.assertEqual((root / 'extern').read_bytes(), b'vorher')
            self.assertEqual(sorted(p.name for p in root.iterdir()), ['bild.png', 'extern'])


if __name__ == '__main__':
    unittest.main()
