import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / 'packaging/paket'))
from pathlib import Path
import tempfile
import unittest
from runtime_paths import script_library, tk_providers


class EmbeddedScriptContract(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.package = Path(self.tmp.name)/'Glide.app'
        self.library = self.package/'Resources/_tcl_data';self.library.mkdir(parents=True)
        self.provider = self.package/'Frameworks/libtcl9.1.dylib';self.provider.parent.mkdir()
        self.provider.write_bytes(b'native-testprovider')

    def test_actual_internal_directory_remains_valid(self):
        self.assertEqual(script_library(self.library, 'tcl', self.package),
                         {'modus': 'dateien', 'ort': 'Resources/_tcl_data'})

    def test_embedded_library_needs_actual_loaded_internal_provider(self):
        path = '//zipfs:/lib/tcl/tcl_library'
        self.assertEqual(script_library(path, 'tcl', self.package, provider=self.provider)['modus'], 'eingebettetes-zip')
        with self.assertRaises(ValueError):
            script_library(path, 'tcl', self.package)
        outside = Path(self.tmp.name)/'extern.dylib';outside.write_bytes(b'external')
        with self.assertRaises(ValueError):
            script_library(path, 'tcl', self.package, provider=outside)

    def test_arbitrary_zip_mount_and_missing_or_external_directory_are_rejected(self):
        for value in ('//zipfs:/tmp/fremd', self.package/'fehlt', Path(self.tmp.name)):
            with self.assertRaises(ValueError):
                script_library(value, 'tcl', self.package, provider=self.provider)

    def test_symlinked_external_provider_is_rejected(self):
        outside = Path(self.tmp.name)/'extern.dylib';outside.write_bytes(b'external')
        link = self.package/'Frameworks/extern.dylib';link.symlink_to(outside)
        with self.assertRaises(ValueError):
            script_library('//zipfs:/lib/tk/tk_library', 'tk', self.package, provider=link)

    def test_tk_filename_with_tcl_prefix_is_never_mistaken_for_tcl_provider(self):
        providers = tk_providers(['/bundle/libtcl9.1.dylib', '/bundle/libtcl9tk9.1.dylib', '/bundle/_tkinter.so'])
        self.assertEqual(providers, {'tcl': '/bundle/libtcl9.1.dylib', 'tk': '/bundle/libtcl9tk9.1.dylib'})

    def test_extensions_and_platform_names_are_not_confused(self):
        mac = ['/b/Contents/Frameworks/Tcl', '/b/Contents/Frameworks/Tk',
               '/b/Contents/Frameworks/tkinterdnd2/tkdnd/osx-arm64-tcl9/libtcl9tkdnd2.10.2.dylib']
        self.assertEqual(tk_providers(mac), {'tcl': mac[0], 'tk': mac[1]})
        win = ['C:/p/_internal/tcl90.dll', 'C:/p/_internal/tcl9tk90.dll', 'C:/p/_internal/libtkdnd2.10.2.dll']
        self.assertEqual(tk_providers(win), {'tcl': win[0], 'tk': win[1]})

    def test_duplicate_native_providers_are_rejected(self):
        with self.assertRaises(ValueError):
            tk_providers(['/internal/tcl91.dll', '/external/tcl91.dll'])


if __name__ == '__main__':
    unittest.main()
