"""Atomarer Versionsschreibweg und begrenzte Aufbewahrung ohne Git-Indexänderung."""
import ast
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]


class Pflege(unittest.TestCase):
    def showcase_module(self):
        spec = importlib.util.spec_from_file_location('pflege_showcase_test', REPO / 'scripts/pflege/showcase_abgleich.py')
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_showcase_replace_failure_preserves_delivery(self):
        mod = self.showcase_module()
        with tempfile.TemporaryDirectory(prefix='glide-showcase-copy-') as folder:
            source, target = Path(folder) / 'quelle', Path(folder) / 'lieferung'
            source.write_bytes(b'Neue Sicherung\x00\xff')
            target.write_bytes(b'Bisherige Sicherung')
            with patch.object(mod.os, 'replace', side_effect=OSError('Dateisperre')):
                with self.assertRaises(OSError):
                    mod.copy_atomic(source, target)
            self.assertEqual(target.read_bytes(), b'Bisherige Sicherung')
            self.assertEqual(set(Path(folder).iterdir()), {source, target})
            mod.copy_atomic(source, target)
            self.assertEqual(target.read_bytes(), source.read_bytes())

    def test_showcase_copy_failure_preserves_delivery(self):
        mod = self.showcase_module()
        with tempfile.TemporaryDirectory(prefix='glide-showcase-copy-') as folder:
            source, target = Path(folder) / 'quelle', Path(folder) / 'lieferung'
            source.write_bytes(b'Neue Sicherung')
            target.write_bytes(b'Bisherige Sicherung')
            def incomplete_copy(_source, temporary):
                Path(temporary).write_bytes(b'Unvollstaendig')
                raise OSError('Kopie unterbrochen')
            with patch.object(mod.shutil, 'copy2', side_effect=incomplete_copy):
                with self.assertRaises(OSError):
                    mod.copy_atomic(source, target)
            self.assertEqual(target.read_bytes(), b'Bisherige Sicherung')
            self.assertEqual(set(Path(folder).iterdir()), {source, target})

    def test_failed_atomic_replace_preserves_target(self):
        tree = ast.parse((REPO / 'scripts/pflege/versionswechsel.py').read_text('utf-8'))
        fn = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'schreibe')
        namespace = {'os': os, 'tempfile': tempfile}
        exec(compile(ast.Module(body=[fn], type_ignores=[]), '<Versionsschreibweg>', 'exec'), namespace)
        with tempfile.TemporaryDirectory(prefix='glide-version-test-') as folder:
            path = Path(folder) / 'app.pyw'
            path.write_bytes(b'Original\r\n')
            with patch.object(os, 'replace', side_effect=OSError('Schreibprobe')):
                with self.assertRaises(OSError):
                    namespace['schreibe'](path, 'Neu\n')
            self.assertEqual(path.read_bytes(), b'Original\r\n')
            self.assertEqual(list(Path(folder).iterdir()), [path])
            namespace['schreibe'](path, 'Neu\n')
            self.assertEqual(path.read_bytes(), b'Neu\n')

    def retention_module(self):
        spec = importlib.util.spec_from_file_location('pflege_retention_test', REPO / 'scripts/pflege/ablage_kuerzen.py')
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_explicit_working_file_mode_never_calls_git(self):
        mod = self.retention_module()
        with tempfile.TemporaryDirectory(prefix='glide-retention-test-') as folder:
            root = Path(folder)
            path = root / 'alt' / 'beleg.json'
            path.parent.mkdir()
            path.write_text('{}', encoding='utf-8')
            with patch.object(mod.ablagegroesse, 'ABLAGE', root), patch.object(
                    mod, 'kandidaten', return_value=['alt/beleg.json']), patch.object(
                    sys, 'argv', ['ablage_kuerzen', '--ohne-git-index']), patch.object(
                    mod.subprocess, 'run', side_effect=AssertionError('Git-Index verändert')):
                self.assertEqual(mod.main(), 0)
            self.assertFalse(path.exists())

    def test_preview_keeps_files_and_never_calls_git(self):
        mod = self.retention_module()
        with patch.object(mod, 'kandidaten', return_value=['alt/beleg.json']), patch.object(
                sys, 'argv', ['ablage_kuerzen', '--anzeigen', '--ohne-git-index']), patch.object(
                mod.subprocess, 'run', side_effect=AssertionError('Git-Index verändert')):
            self.assertEqual(mod.main(), 0)

    def test_working_file_mode_rejects_path_outside_root(self):
        mod = self.retention_module()
        with tempfile.TemporaryDirectory(prefix='glide-retention-grenze-') as folder:
            root = Path(folder) / 'wurzel'
            root.mkdir()
            protected = Path(folder) / 'fremd.json'
            protected.write_text('{}', encoding='utf-8')
            with patch.object(mod.ablagegroesse, 'ABLAGE', root), patch.object(
                    mod, 'kandidaten', return_value=['../fremd.json']), patch.object(
                    sys, 'argv', ['ablage_kuerzen', '--ohne-git-index']):
                with self.assertRaises(ValueError):
                    mod.main()
            self.assertTrue(protected.exists())


if __name__ == '__main__':
    unittest.main()
