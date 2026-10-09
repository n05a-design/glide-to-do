"""Aufbewahrung: neue Dateien, fehlende Indexeinträge und Pfadgrenzen."""
import importlib.util
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tests/tools'))
spec=importlib.util.spec_from_file_location('retention',ROOT/'scripts/pflege/ablage_kuerzen.py')
retention=importlib.util.module_from_spec(spec);spec.loader.exec_module(retention)

class RetentionTests(unittest.TestCase):
    def test_inventory_includes_new_and_ignores_missing_index_entry(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            names=['old/tracked.json','old/new.json','old/missing.json']
            for name in names[:2]:
                p=root/name;p.parent.mkdir(exist_ok=True);p.write_text('test')
            output=('\0'.join(names+names[:1])+'\0').encode()
            with patch.object(retention.ablagegroesse,'ABLAGE',root), patch.object(retention.ablagegroesse,'aktuelle_version',return_value='3.33.16'), patch.object(retention.subprocess,'run',return_value=SimpleNamespace(returncode=0,stdout=output)) as run, patch.object(retention.ablagegroesse,'befunde',return_value=[('Archivalter',names[0],''),('Archivalter',names[1],'')]) as rules:
                self.assertEqual(retention.kandidaten(),sorted(names[:2]))
                self.assertIn('--others',run.call_args.args[0])
                self.assertEqual({name for name,size in rules.call_args.args[0]},set(names[:2]))

    def test_escaping_path_is_rejected_before_git_or_deletion(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'workspace';root.mkdir()
            outside=Path(directory)/'outside.json';outside.write_text('preserve')
            with patch.object(retention.ablagegroesse,'ABLAGE',root), patch.object(retention,'kandidaten',return_value=['../outside.json']), patch.object(sys,'argv',['retention']), patch.object(retention.subprocess,'run') as run:
                with self.assertRaises(ValueError):retention.main()
                run.assert_not_called()
                self.assertEqual(outside.read_text(),'preserve')

    def test_tracked_and_new_paths_removed_unrelated_files_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for name in ['old/tracked.json','old/new.json','keep.json']:
                p=root/name;p.parent.mkdir(exist_ok=True);p.write_text('test')
            with patch.object(retention.ablagegroesse,'ABLAGE',root), patch.object(retention,'kandidaten',return_value=['old/tracked.json','old/new.json']), patch.object(sys,'argv',['retention']), patch.object(retention.subprocess,'run') as run:
                self.assertEqual(retention.main(),0)
                self.assertIn('--ignore-unmatch',run.call_args.args[0])
            self.assertFalse((root/'old').exists())
            self.assertEqual((root/'keep.json').read_text(),'test')

    def test_symlink_inside_workspace_is_rejected(self):
        # Gegenprobe zur Korrektur vom 08.10.2026: Verknüpfungen oberhalb der
        # Ablage sind erlaubt, innerhalb bleiben sie verboten.
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'workspace';root.mkdir()
            # Ziel innerhalb der Ablage: Die Pfadgrenze allein hielte das nicht auf.
            target=root/'elsewhere';target.mkdir()
            (target/'data.json').write_text('preserve')
            (root/'link').symlink_to(target,target_is_directory=True)
            with patch.object(retention.ablagegroesse,'ABLAGE',root), patch.object(retention,'kandidaten',return_value=['link/data.json']), patch.object(sys,'argv',['retention']), patch.object(retention.subprocess,'run') as run:
                with self.assertRaises(ValueError):retention.main()
                run.assert_not_called()
            self.assertEqual((target/'data.json').read_text(),'preserve')

    def test_symlinked_parent_above_workspace_is_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            real=Path(directory)/'real';(real/'old').mkdir(parents=True)
            (real/'old/x.json').write_text('test')
            alias=Path(directory)/'alias';alias.symlink_to(real,target_is_directory=True)
            with patch.object(retention.ablagegroesse,'ABLAGE',alias), patch.object(retention,'kandidaten',return_value=['old/x.json']), patch.object(sys,'argv',['retention']), patch.object(retention.subprocess,'run'):
                self.assertEqual(retention.main(),0)
            self.assertFalse((real/'old/x.json').exists())

if __name__=='__main__':unittest.main()
