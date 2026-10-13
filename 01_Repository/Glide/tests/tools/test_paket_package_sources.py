import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / 'packaging/paket'))
import hashlib
from pathlib import Path
import tempfile
import unittest
from package_sources import identity,in_onedrive,included,manifest,TARGETS

SOURCE='APP_NAME="Glide"\nAPP_VERSION="3.42.0"\nAPP_BUNDLE_ID="de.shaye.glide"\nAPP_USER_MODEL_ID="Shaye.Glide"\n'

class SourcesTest(unittest.TestCase):
    def test_onedrive_build_folders_are_recognized_precisely(self):
        for path in ("/QA/Library/CloudStorage/OneDrive-Persönlich/bau", "C:/QA/OneDrive/bau",
                     "C:/QA/OneDrive - Firma/bau"):
            self.assertTrue(in_onedrive(path), path)
        for path in ("/private/tmp/-Users-x-Library-CloudStorage-OneDrive-Pers-nlich-Github/bau", "/tmp/onedrivebau"):
            self.assertFalse(in_onedrive(path), path)

    def test_identity_without_import(self):
        values=identity(SOURCE+'raise RuntimeError("nicht importieren")\n','3.42.0')
        self.assertEqual(values['APP_USER_MODEL_ID'],'Shaye.Glide')
        self.assertEqual(values['APP_BUNDLE_ID'],'de.shaye.glide')
        for source,version in ((SOURCE,'3.41.0'),(SOURCE,'3.42'),(SOURCE+'APP_NAME="Anders"\n','3.42.0'),
                               (SOURCE.replace('APP_USER_MODEL_ID','ANDERES'),'3.42.0'),
                               (SOURCE.replace('"Glide"','__import__("does_not_exist")'),'3.42.0')):
            with self.subTest(source=source,version=version),self.assertRaises(ValueError):identity(source,version)

    def test_platform_files_and_omissions(self):
        for target,(_system,_arch,dnd)in TARGETS.items():
            self.assertTrue(included('app.pyw',target))
            self.assertTrue(included('new_logic.py',target))
            self.assertTrue(included('resources/fonts/UI.ttf',target))
            self.assertTrue(included('vendor/tkinterdnd2/LICENSE',target))
            self.assertTrue(included('vendor/tkinterdnd2/tkdnd/'+dnd+'/pkgIndex.tcl',target))
            for other in ('win-x86-tcl9','linux-x64-tcl9','osx-x64-tcl9',dnd.removesuffix('-tcl9')):
                self.assertFalse(included('vendor/tkinterdnd2/tkdnd/'+other+'/file',target))
            for p in ('drawing_prototype.py','README.md','tests/fixture','resources/__pycache__/x.pyc',
                      'resources/archiv/alt.svg','resources/.DS_Store'):
                self.assertFalse(included(p,target))
        with self.assertRaises(ValueError):included('app.pyw','windows-arm64')
        for p in ('/app.pyw','../app.pyw','resources/../x','resources\\x','resources/./x'):
            with self.subTest(path=p),self.assertRaises(ValueError):included(p,'macos-arm64')

    def fixture(self,root):
        files=['app.pyw','vendor/tkinterdnd2/__init__.py','vendor/tkinterdnd2/TkinterDnD.py',
               'vendor/tkinterdnd2/LICENSE','vendor/provenance.json','resources/fonts/LICENSE',
               'resources/logo/a.svg']
        files += ['vendor/tkinterdnd2/tkdnd/'+v[2]+'/pkgIndex.tcl'for v in TARGETS.values()]
        files += ['vendor/tkinterdnd2/tkdnd/linux-x64-tcl9/x.so','drawing_prototype.py']
        for p in files:
            f=root/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(p)

    def test_manifest_hashes_and_complete_native_resources(self):
        with tempfile.TemporaryDirectory()as folder:
            root=Path(folder);self.fixture(root)
            values=manifest(root,'macos-arm64')
            self.assertEqual(values['app.pyw'],hashlib.sha256(b'app.pyw').hexdigest())
            self.assertFalse(any('windows' in p or 'win-' in p or 'linux-' in p for p in values))
            self.assertNotIn('drawing_prototype.py',values)
            (root/'vendor/tkinterdnd2/tkdnd/osx-arm64-tcl9/pkgIndex.tcl').unlink()
            with self.assertRaises(ValueError):manifest(root,'macos-arm64')
            self.assertTrue(manifest(root,'windows-x64'))

    def test_symlink_not_silently_bundled(self):
        with tempfile.TemporaryDirectory()as folder:
            root=Path(folder);self.fixture(root)
            (root/'resources/logo/link.svg').symlink_to(root/'app.pyw')
            with self.assertRaisesRegex(ValueError,'Symlink'):manifest(root,'macos-arm64')

if __name__=='__main__':unittest.main()
