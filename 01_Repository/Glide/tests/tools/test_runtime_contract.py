"""Bauziele, Header-ABI und echtes Linux-Backend ohne Compiler/GUI prüfen."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'packaging/runtime'))
from runtime_contract import build_destination, extension_command, python_pin, require_atk


class RuntimeContract(unittest.TestCase):
    def test_header_patch_and_regular_abi_are_required(self):
        self.assertEqual(python_pin('3.14.5', '#define PY_VERSION "3.14.5"')[:8], '5607950e')
        for version, header, options in (
                ('3.14.5', '#define PY_VERSION "3.14.7"', {}),
                ('3.14.9', '#define PY_VERSION "3.14.9"', {}),
                ('3.14.5', '#define PY_VERSION "3.14.5"', {'free_threaded': True}),
                ('3.14.5', '#define PY_VERSION "3.14.5"', {'debug': True})):
            with self.subTest(version=version, options=options), self.assertRaises(ValueError):
                python_pin(version, header, **options)

    def test_build_cannot_overlay_source_or_enter_sync_folder(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'source'
            self.assertEqual(build_destination(root / 'build', [source]), (root / 'build').resolve())
            for target in (source, source / 'build', root, root / 'OneDrive-Test/build'):
                with self.subTest(target=target.name), self.assertRaises(ValueError):
                    build_destination(target, [source])

    def test_linux_stub_build_is_rejected(self):
        require_atk('DEFS = -DHAVE_ATK=1 -DHAVE_X11=1\n')
        for makefile in ('ATK_LIBS =\n', 'DEFS = -DHAVE_ATK=0', 'DEFS = -DHAVE_ATK=10'):
            with self.assertRaises(ValueError):
                require_atk(makefile)

    def test_linker_uses_own_libraries_and_windows_import_library(self):
        arguments = dict(include=Path('headers'), prefix=Path('runtime'), modules=Path('modules'), output=Path('_tkinter.so'))
        mac = extension_command('darwin', 'arm64', **arguments)
        self.assertIn(str(Path('runtime/lib/libtcl9.1.dylib')), mac)
        self.assertIn('-Wl,-rpath,' + str(Path('runtime/lib')), mac)
        linux = extension_command('linux', 'x86_64', **arguments)
        self.assertIn(str(Path('runtime/lib/libtcl9tk9.1.so')), linux)
        windows = extension_command('win32', 'x86_64', python_library=Path('python314.lib'), **arguments)
        self.assertIn(str(Path('runtime/lib/tcl9tk91.lib')), windows)
        self.assertIn('python314.lib', windows)
        with self.assertRaises(ValueError):
            extension_command('win32', 'x86_64', **arguments)


if __name__ == '__main__':
    unittest.main()
