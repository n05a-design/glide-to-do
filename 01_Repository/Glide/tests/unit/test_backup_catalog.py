"""Sicherungen inventarisieren, filtern und eindeutig auswählen, ohne Inhalte zu öffnen."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
import backup_catalog as catalog


class Catalog(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='glide-katalog-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def file(self, name, stamp=10, content=b'kein gueltiges JSON'):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        os.utime(path, (stamp, stamp))
        return path

    def test_scan_newest_limit_filter_and_deduplication(self):
        first = self.file('alt.json', 10)
        self.file('neu.glideapp', 20)
        self.file('unpassend.txt', 30)
        rows, errors = catalog.scan(self.root, [first], limit=1)
        self.assertEqual([r.name for r in rows], ['neu.glideapp'])
        self.assertEqual(len(errors), 1)
        rows, _ = catalog.scan(self.root, [first])
        self.assertEqual(len(rows), 2)

    def test_no_content_read_during_inventory(self):
        self.file('defekt.glidebackup')
        with patch.object(Path, 'open', side_effect=AssertionError('Inhalt gelesen')):
            rows, errors = catalog.scan(self.root)
        self.assertEqual(rows[0].kind, 'Aufgabensicherung')
        self.assertFalse(errors)

    def test_missing_directory_and_disappeared_external_file(self):
        self.assertEqual(catalog.scan(self.root / 'fehlend'), ([], []))
        rows, errors = catalog.scan(self.root, [self.root / 'verschwunden.json'])
        self.assertFalse(rows)
        self.assertEqual(len(errors), 1)

    def test_directory_error_is_visible(self):
        with patch.object(catalog.os, 'scandir', side_effect=PermissionError):
            rows, errors = catalog.scan(self.root)
        self.assertFalse(rows)
        self.assertTrue(errors)

    def test_filter_is_case_insensitive_and_requires_all_terms(self):
        self.file('Urlaub-Änderung.glideapp')
        self.file('Arbeit.json')
        rows, _ = catalog.scan(self.root)
        self.assertEqual(len(catalog.filtered(rows, 'URLAUB app')), 1)
        self.assertEqual(catalog.filtered(rows, 'Urlaub Aufgaben'), [])

    def test_selection_names_distinguish_same_basename(self):
        a = self.file('a/stand.json')
        b = self.file('b/stand.json')
        label = catalog.choice_label([], a)
        sources = [(label, str(a))]
        second = catalog.choice_label(sources, b)
        self.assertNotEqual(label, second)
        self.assertEqual(catalog.choice_label(sources, a), label)

    def test_metadata_sizes_and_directory_rejected(self):
        row = catalog.inspect(self.file('gross.JSON', content=b'x' * 2048))
        self.assertEqual(row.size_text, '2,0 KiB')
        with self.assertRaises(ValueError):
            catalog.inspect(self.root)

    def test_description_handles_nested_items_without_mutation(self):
        data = {'version': 26, 'lists': [{'items': [
            {'done': True, 'children': [{'text': 'Kind'}]}]}, {'items': None}]}
        self.assertEqual(catalog.describe(data), '2 Listen · 2 Punkte · 1 erledigt · Speicherstufe 26')
        self.assertNotIn('done', data['lists'][0]['items'][0]['children'][0])


if __name__ == '__main__':
    unittest.main()
