import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / 'packaging/paket'))
import copy
import unittest
from windows_native import validate_graph, validate_loaded


def record(path, imports=(), *, machine=0x8664, sha256='a'*64):
    return dict(path=path, imports=list(imports), machine=machine, sha256=sha256)


class WindowsNativeContract(unittest.TestCase):
    def test_internal_python_tcl_and_system_imports_resolve_without_mutation(self):
        records = [record('Glide.exe', ['KERNEL32.dll', 'python314.dll']),
                   record('_internal/python314.dll', ['api-ms-win-core-file-l1-1-0.dll']),
                   record('_internal/_tkinter.pyd', ['TCL91.dll', 'tk91.dll', 'python314.dll']),
                   record('_internal/tcl91.dll'), record('_internal/tk91.dll', ['user32.dll'])]
        before = copy.deepcopy(records)
        self.assertEqual(validate_graph(records)['exitcode'], 0)
        self.assertEqual(records, before)

    def test_missing_external_runtime_and_delayed_import_are_errors(self):
        result = validate_graph([record('Glide.exe', ['python314.dll', 'libcrypto-3.dll'])])
        self.assertEqual(result['exitcode'], 1)
        self.assertEqual({v['abhaengigkeit'] for v in result['fehler']}, {'python314.dll', 'libcrypto-3.dll'})

    def test_wrong_architecture_and_system_shadowing_are_errors(self):
        result = validate_graph([record('Glide.exe', machine=0x14c), record('_internal/kernel32.dll')])
        self.assertEqual(len(result['fehler']), 2)

    def test_different_duplicates_and_absolute_dll_import_are_errors(self):
        records = [record('Glide.exe', ['C:\\Python\\python314.dll']), record('a/same.dll'),
                   record('b/SAME.dll', sha256='b'*64)]
        self.assertEqual(len(validate_graph(records)['fehler']), 2)

    def test_paths_cannot_escape_the_native_package(self):
        for path in ('../Glide.exe', '/tmp/Glide.exe', 'C:/Python/Glide.exe', 'a\\Glide.exe'):
            with self.assertRaises(ValueError):
                validate_graph([record(path)])

    def test_loaded_library_contract_rejects_external_python_even_if_other_paths_are_valid(self):
        result = validate_loaded('C:\\Paket\\Glide', 'C:\\Windows', [
            'c:\\paket\\glide\\Glide.exe', 'C:\\Paket\\Glide\\_internal\\python314.dll',
            'C:\\Windows\\System32\\kernel32.dll', 'C:\\Python314\\tcl91.dll'])
        self.assertEqual(result['exitcode'], 1)
        self.assertEqual(len(result['bibliotheken']), 3)
        self.assertIn('tcl91.dll', result['fehler'][0])
        self.assertNotIn('C:\\Python314', str(result))

    def test_windows_temp_is_not_a_system_library_directory(self):
        result = validate_loaded('C:\\Paket\\Glide', 'C:\\Windows', ['C:\\Windows\\Temp\\python314.dll'])
        self.assertEqual(result['exitcode'], 1)
        with self.assertRaises(ValueError):
            validate_loaded('relatives-paket', 'C:\\Windows', [])


if __name__ == '__main__':
    unittest.main()
