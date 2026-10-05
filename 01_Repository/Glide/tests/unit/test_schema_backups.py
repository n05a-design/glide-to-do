"""Sicherungsvertrag: alte Bytes, Fehler und Dateiaustausch ohne Tk prüfen."""
from pathlib import Path
import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
from schema_backups import SchemaBackups, file_signature


class SchemaBackupTests(unittest.TestCase):
    def test_windows_stat_and_fstat_ctime_difference_does_not_invalidate(self):
        common = dict(st_dev=1, st_ino=2, st_size=40, st_mtime_ns=200, st_birthtime_ns=100)
        with patch('schema_backups.os.name', 'nt'):
            self.assertEqual(file_signature(SimpleNamespace(**common, st_ctime_ns=100)),
                             file_signature(SimpleNamespace(**common, st_ctime_ns=200)))

    def test_posix_change_time_still_invalidates(self):
        common = dict(st_dev=1, st_ino=2, st_size=40, st_mtime_ns=200)
        with patch('schema_backups.os.name', 'posix'):
            self.assertNotEqual(file_signature(SimpleNamespace(**common, st_ctime_ns=100)),
                                file_signature(SimpleNamespace(**common, st_ctime_ns=200)))

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.source = Path(self.temp.name) / 'data.json'
        self.backups = Path(self.temp.name) / 'backups'
        self.guard = SchemaBackups()

    def write(self, payload):
        self.source.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
        return self.source.read_bytes()

    def test_all_formats_preserve_exact_original_and_parse_once(self):
        for version in range(4, 21):
            with self.subTest(version=version):
                original = self.write({'version': version, 'text': 'ä\nAltbestand'})
                guard = SchemaBackups()
                load = json.load
                with patch('schema_backups.json.load', wraps=load) as calls:
                    for target in range(12, 21):
                        backup = guard.ensure(self.source, self.backups, target)
                        self.assertEqual(bool(backup), version < target)
                        if backup:
                            self.assertEqual(Path(backup).read_bytes(), original)
                    self.assertEqual(calls.call_count, 1)
                self.assertEqual(self.source.read_bytes(), original)

    def test_loading_supplies_version_without_additional_parse(self):
        payload = {'version': 11}
        self.write(payload)
        self.guard.observe(self.source, payload, self.source.stat())
        with patch('schema_backups.json.load', side_effect=AssertionError('Zusatz-Parse')):
            self.assertTrue(self.guard.ensure(self.source, self.backups, 20))

    def test_missing_file_needs_no_backup(self):
        self.assertIsNone(self.guard.ensure(self.source, self.backups, 20))

    def test_scalar_missing_string_and_bool_version_are_backed_up(self):
        for payload in [[], {}, {'version': '20'}, {'version': True}]:
            original = self.write(payload)
            backup = self.guard.ensure(self.source, self.backups, 20)
            self.assertEqual(Path(backup).read_bytes(), original)

    def test_file_replacement_invalidates_observed_version(self):
        self.write({'version': 20})
        self.assertIsNone(self.guard.ensure(self.source, self.backups, 20))
        replacement = self.source.with_suffix('.new')
        replacement.write_text('{"version": 19}', encoding='utf-8')
        os.replace(replacement, self.source)
        backup = self.guard.ensure(self.source, self.backups, 20)
        self.assertEqual(Path(backup).read_bytes(), self.source.read_bytes())

    def test_in_place_change_invalidates_version(self):
        self.write({'version': 20})
        self.assertIsNone(self.guard.ensure(self.source, self.backups, 20))
        self.write({'version': 18})
        self.assertTrue(self.guard.ensure(self.source, self.backups, 20))

    def test_windows_same_metadata_still_preserves_changed_format_bytes(self):
        # Windows kann innerhalb eines Ticks dieselben Zeiten zurückgeben.
        # Diese Gegenprobe erzwingt den Fall auch auf Linux/macOS.
        with patch('schema_backups.os.name', 'nt'), patch('schema_backups.file_signature', return_value=(1, 2, 15, 100, 100)):
            self.write({'version': 20})
            self.assertIsNone(self.guard.ensure(self.source, self.backups, 20))
            original = self.write({'version': 18})
            backup = self.guard.ensure(self.source, self.backups, 20)
            self.assertTrue(backup)
            with open(backup, 'rb') as saved:
                self.assertEqual(saved.read(), original)

    def test_windows_same_metadata_detects_version_after_large_content(self):
        # Ein bloßer Headervergleich würde den Formatwert hier übersehen.
        with patch('schema_backups.os.name', 'nt'), patch('schema_backups.file_signature', return_value=(1, 2, 300000, 100, 100)):
            self.write({'padding': 'x' * 300000, 'version': 20})
            self.assertIsNone(self.guard.ensure(self.source, self.backups, 20))
            original = self.write({'padding': 'x' * 300000, 'version': 18})
            backup = self.guard.ensure(self.source, self.backups, 20)
            self.assertTrue(backup)
            with open(backup, 'rb') as saved:
                self.assertEqual(saved.read(), original)

    def test_windows_unchanged_content_still_parses_only_once(self):
        self.write({'version': 18})
        load = json.load
        with patch('schema_backups.os.name', 'nt'), patch('schema_backups.json.load', wraps=load) as calls:
            for _ in range(5):
                self.assertTrue(self.guard.ensure(self.source, self.backups, 20))
            self.assertEqual(calls.call_count, 1)

    def test_failed_copy_propagates_and_retry_preserves_original(self):
        original = self.write({'version': 19})
        with patch('schema_backups.shutil.copy2', side_effect=OSError('kein Speicherplatz')):
            with self.assertRaises(OSError):
                self.guard.ensure(self.source, self.backups, 20)
        self.assertEqual(self.source.read_bytes(), original)
        backup = self.guard.ensure(self.source, self.backups, 20)
        self.assertEqual(Path(backup).read_bytes(), original)

    def test_invalid_json_does_not_become_a_writable_version(self):
        self.source.write_bytes(b'{invalid')
        with self.assertRaises(json.JSONDecodeError):
            self.guard.ensure(self.source, self.backups, 20)
        self.assertEqual(self.source.read_bytes(), b'{invalid')
        self.write({'version': 19})
        self.assertTrue(self.guard.ensure(self.source, self.backups, 20))


if __name__ == '__main__':
    unittest.main()
