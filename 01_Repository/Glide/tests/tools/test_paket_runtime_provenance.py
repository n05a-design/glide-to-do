"""Veränderte Runtimeeingaben und falsche Anbieter beim Paketbau verweigern."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'packaging/paket'))
from runtime_provenance import validate_runtime_proof
from license_contract import macos_native_components, validate_components


class RuntimeProvenance(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.extension = self.root / 'python-extension/_tkinter.so'
        self.library = self.root / 'runtime/lib/libtcl9.1.dylib'
        for path in (self.extension, self.library):
            path.parent.mkdir(parents=True)
            path.write_bytes(b'Owned native fixture')
        self.runtime = dict(python='3.14.5', platform='darwin', machine='arm64', tcl='9.1.0', tk_compiled='9.1')
        self.pins = dict(tcl='tcl-pin', tk='tk-pin', python='python-pin')
        self.patches = [dict(platform='darwin', id='fixture')]
        self.proof = dict(self.runtime, quellpins=self.pins, runtime_patches=self.patches,
                          extension=str(self.extension), runtime=str(self.root / 'runtime'),
                          sha256={p.relative_to(self.root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (self.extension, self.library)})
        self.manifest = self.root / 'runtime-bau.json'

    def validate(self, extension=None):
        self.manifest.write_text(json.dumps(self.proof))
        return validate_runtime_proof(self.manifest, self.runtime, extension or self.extension,
                                      pins=self.pins, patches=self.patches)

    def test_exact_runtime_files_pins_and_patches_are_accepted(self):
        self.assertEqual(self.validate()['dateien'], 2)

    def test_wrong_loaded_extension_or_source_pins_are_rejected(self):
        with self.assertRaises(ValueError):
            self.validate(self.root / 'external/_tkinter.so')
        self.proof['quellpins'] = dict(self.pins, tk='other-pin')
        with self.assertRaises(ValueError):
            self.validate()

    def test_modified_or_added_runtime_files_are_rejected(self):
        self.library.write_bytes(b'Modified provider')
        with self.assertRaises(ValueError):
            self.validate()
        self.library.write_bytes(b'Owned native fixture')
        (self.library.parent / 'foreign.dylib').write_bytes(b'Extra provider')
        with self.assertRaises(ValueError):
            self.validate()

    def test_parent_escape_and_missing_extension_hash_are_rejected(self):
        self.proof['sha256']['../outside'] = '0' * 64
        with self.assertRaises(ValueError):
            self.validate()
        self.proof['sha256'].pop('../outside')
        self.proof['sha256'].pop('python-extension/_tkinter.so')
        with self.assertRaises(ValueError):
            self.validate()

    def test_tcl91_requires_utf8proc_license_and_unknown_provider_stays_red(self):
        matrix = macos_native_components(['Contents/Frameworks/libtcl9.1.dylib'])
        record = lambda name: dict(name=name, version='pin', source='original', files={'terms':'digest'})
        records = [record(name) for name in ('Tcl', 'libtommath', 'Henry-Spencer-Regex')]
        with self.assertRaisesRegex(ValueError, 'utf8proc'):
            validate_components(matrix, records)
        validate_components(matrix, records+[record('utf8proc')])
        with self.assertRaises(ValueError):
            macos_native_components(['Contents/Frameworks/libtcl9.2.dylib'])


if __name__ == '__main__':
    unittest.main()
