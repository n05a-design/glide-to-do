"""Gesamtausgabe: Inhalte, Grenzen, unveränderte Quellen und atomarer Abschluss."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[2]/'src/glide'))
import markdown_tree as export


class TreeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='glide-md-unit-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.data = self.root/'daten';(self.data/'attachments').mkdir(parents=True)
        (self.data/'attachments/a.png').write_bytes(b'PNG-Daten')
        self.snapshot = {'lists': [
            {'id': 'a', 'title': 'CON:* [Plan](alt)', 'list_kind': 'page', 'folder_id': 'f',
             'rich_note': {'text': 'Bild\n\ufffc\nLink', 'spans': [
                 {'start': 5, 'end': 6, 'tag': 'bild'}, {'start': 7, 'end': 11, 'tag': 'link'}],
                 'images': {'bild': {'attachment': 'att'}}, 'links': {'link': 'glide://item/i'}},
             'attachments': [{'id': 'att', 'name': 'a.png', 'storage': 'attachments/a.png'}],
             'items': [{'id': 'i', 'text': 'Task', 'done': False, 'repeat': {'type': 'daily'},
                        'children': [{'id': 'j', 'text': 'Fertig', 'done': True}]}]},
            {'id': 'b', 'title': 'con:*', 'references': ['glide://list/a'], 'items': []}],
            'folders': [{'id': 'f', 'title': 'Ordner'}], 'labels': []}

    def run_export(self, **kwargs):
        return export.write_tree(self.snapshot, self.root/'ausgabe', self.data, **kwargs)

    def test_complete_inventory_and_source_bytes(self):
        before = copy.deepcopy(self.snapshot)
        result = self.run_export()
        inv = json.loads((self.root/'ausgabe/INVENTAR.json').read_text(encoding='utf-8'))
        self.assertEqual(inv['bestand'], before)
        self.assertEqual(self.snapshot, before)
        self.assertEqual((self.data/'attachments/a.png').read_bytes(), b'PNG-Daten')
        self.assertEqual(result['zaehlung'], dict(listen_seiten=2, ordner=1, aufgaben=2,
                                                anhangverweise=1, anhangdateien=1))
        md = '\n'.join(p.read_text(encoding='utf-8') for p in (self.root/'ausgabe').rglob('*.md'))
        self.assertIn('- [x] Fertig', md)
        self.assertIn('- [ ] Task', md)
        self.assertNotIn('glide://', md)
        self.assertTrue(any(v['objekt']=='i' and v['feld']=='repeat' for v in inv['hinweise']))

    def test_manifest_and_every_relative_link(self):
        self.run_export()
        base = self.root/'ausgabe'
        manifest = json.loads((base/'MANIFEST.json').read_text(encoding='utf-8'))['sha256']
        for name, digest in manifest.items():
            self.assertEqual(hashlib.sha256((base/name).read_bytes()).hexdigest(), digest)
        import re
        for path in base.rglob('*.md'):
            for ref in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                relative, _, anchor = unquote(ref).partition('#')
                dest = path.parent/relative
                self.assertTrue(dest.is_file(), (path, ref))
                if anchor:self.assertIn(f'id="{anchor}"', dest.read_text(encoding='utf-8'))

    def test_task_refs_are_links_instead_of_duplicate_tasks(self):
        self.snapshot['lists'][0]['rich_note'] = {'text':'Task\nTask', 'spans':[
            {'start':0,'end':9,'tag':'task'}, {'start':0,'end':4,'tag':'item:i'},
            {'start':5,'end':9,'tag':'taskref:i'}], 'links':{}}
        result = self.run_export()
        import re
        md = '\n'.join(p.read_text(encoding='utf-8') for p in (self.root/'ausgabe').rglob('*.md') if p.name!='INDEX.md')
        self.assertEqual(len(re.findall(r'^\s*- \[[ x]\]',md,re.M)), result['zaehlung']['aufgaben'])
        self.assertGreaterEqual(md.count('#punkt-i'),2)

    def test_structural_rows_do_not_become_task_checkboxes(self):
        self.snapshot['lists'][0]['items'][0]['kind'] = 'group'
        result = self.run_export()
        import re
        md = '\n'.join(p.read_text(encoding='utf-8') for p in (self.root/'ausgabe').rglob('*.md'))
        self.assertEqual(result['zaehlung']['aufgaben'],1)
        self.assertEqual(len(re.findall(r'^\s*- \[[ x]\]',md,re.M)),1)

    def test_literal_code_uris_remain_text_and_real_references_resolve(self):
        self.snapshot['lists'][0]['note'] = '`glide://list/b`\n\n```text\nglide://list/b\n```'
        self.snapshot['lists'][0]['references'] = ['glide://list/b']
        self.run_export()
        inv = json.loads((self.root/'ausgabe/INVENTAR.json').read_text(encoding='utf-8'))
        name = next(o['datei'] for o in inv['objekte'] if o['art']=='list' and o['id']=='a')
        md = (self.root/'ausgabe'/name).read_text(encoding='utf-8')
        self.assertEqual(md.count('glide://list/b'),2)
        self.assertIn('[Verweis](',md)

    def test_existing_target_never_changed(self):
        target = self.root/'ausgabe';target.mkdir();(target/'behalten').write_bytes(b'alt')
        with self.assertRaises(FileExistsError):self.run_export()
        self.assertEqual((target/'behalten').read_bytes(), b'alt')

    def test_cancel_no_final_or_staging_folder(self):
        event = threading.Event();event.set()
        with self.assertRaises(export.ExportCancelled):self.run_export(cancel=event)
        self.assertFalse((self.root/'ausgabe').exists())
        self.assertFalse(list(self.root.glob('.glide-md-*')))

    def test_write_failure_no_partial_result(self):
        with patch.object(export.os, 'rename', side_effect=OSError('Schreibfehler')):
            with self.assertRaises(OSError):self.run_export()
        self.assertFalse((self.root/'ausgabe').exists())
        self.assertFalse(list(self.root.glob('.glide-md-*')))

    def test_cancel_during_attachment_copy_removes_partial_files(self):
        event = threading.Event()
        original = Path.open
        source = self.data/'attachments/a.png'
        class Reader:
            def __init__(self, stream):self.stream = stream
            def __enter__(self):return self
            def __exit__(self, *args):self.stream.close()
            def fileno(self):return self.stream.fileno()
            def read(self, size):
                value = self.stream.read(size)
                event.set()
                return value
        def opened(path, *args, **kwargs):
            stream = original(path, *args, **kwargs)
            return Reader(stream) if path == source and args == ('rb',) else stream
        with patch.object(Path, 'open', opened):
            with self.assertRaises(export.ExportCancelled):self.run_export(cancel=event)
        self.assertFalse((self.root/'ausgabe').exists())
        self.assertFalse(list(self.root.glob('.glide-md-*')))

    def test_target_created_during_export_is_preserved(self):
        target = self.root/'ausgabe'
        original = export.os.open
        def claim(path, *args, **kwargs):
            if str(path).endswith('.lock'):
                target.mkdir();(target/'fremd').write_bytes(b'neu')
            return original(path, *args, **kwargs)
        with patch.object(export.os, 'open', side_effect=claim):
            with self.assertRaises(FileExistsError):self.run_export()
        self.assertEqual((target/'fremd').read_bytes(), b'neu')

    def test_missing_attachment_and_reference_are_assigned(self):
        (self.data/'attachments/a.png').unlink()
        self.snapshot['lists'][1]['references'] = ['glide://list/weg']
        result = self.run_export()
        self.assertTrue(any(v['objekt']=='a' and v['feld']=='att' for v in result['hinweise']))
        self.assertTrue(any(v['objekt']=='b' and v['feld']=='references' for v in result['hinweise']))

    def test_unsafe_storage_never_read(self):
        self.snapshot['lists'][0]['attachments'][0]['storage'] = 'attachments/../geheim'
        result = self.run_export()
        self.assertEqual(result['zaehlung']['anhangdateien'], 0)

    def test_symlink_is_reported(self):
        source = self.data/'attachments/a.png';source.unlink()
        try:source.symlink_to(self.root/'extern')
        except OSError as e:self.skipTest(str(e))
        (self.root/'extern').write_bytes(b'extern')
        result = self.run_export()
        self.assertEqual(result['zaehlung']['anhangdateien'], 0)
        self.assertTrue(any('Symlink' in v['detail'] for v in result['hinweise']))

    def test_deep_paths_collisions_and_windows_limit(self):
        self.snapshot['folders'] = [{'id': str(i), 'title': 'Ordner'*20, 'parent_id': str(i-1) if i else None} for i in range(20)]
        self.snapshot['lists'][0]['folder_id'] = '19'
        self.run_export()
        self.assertTrue(all(len(str(p)) <= 240 for p in (self.root/'ausgabe').rglob('*')))
        names = [p.name.casefold() for p in (self.root/'ausgabe').rglob('*.md') if p.name != 'INDEX.md']
        self.assertEqual(len(names), len(set(names)))

    def test_duplicate_id_rejected_before_publication(self):
        self.snapshot['lists'][1]['id'] = 'a'
        with self.assertRaises(ValueError):self.run_export()
        self.assertFalse((self.root/'ausgabe').exists())

    def test_output_inside_data_rejected(self):
        with self.assertRaises(ValueError):export.write_tree(self.snapshot, self.data/'export', self.data)

    def test_table_csv_and_empty_folder(self):
        self.snapshot['lists'][0]['rich_note'] = {'text': '| A | B |\n|---|---|\n| 1 | 2 |', 'spans': []}
        self.snapshot['folders'].append({'id': 'empty', 'title': 'Leer'})
        self.run_export()
        self.assertEqual(len(list((self.root/'ausgabe').rglob('*.tabellen.csv'))), 1)
        self.assertGreaterEqual(len(list((self.root/'ausgabe').rglob('INDEX.md'))), 3)


if __name__ == '__main__':unittest.main()
