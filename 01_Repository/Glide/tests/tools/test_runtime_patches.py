"""Echter Patchlauf und verweigerte fremde/veränderte Eingaben ohne GUI."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'packaging/runtime'))
from runtime_contract import PINS
from runtime_patches import apply_patches


class RuntimePatches(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.base = Path(self.folder.name)
        self.source = self.base / 'export'
        self.source.mkdir()
        self.target = self.source / 'provider.c'
        self.target.write_text('first\nold\nlast\n')
        self.patch = self.base / 'provider.patch'
        self.patch.write_text('--- a/provider.c\n+++ b/provider.c\n@@ -1,3 +1,3 @@\n first\n-old\n+new\n last\n')
        sha = lambda value: hashlib.sha256(value).hexdigest()
        self.entry = dict(id='fixture', platform='darwin', file='provider.c', patch='provider.patch',
                          before_sha256=sha(self.target.read_bytes()),
                          after_sha256=sha(b'first\nnew\nlast\n'), patch_sha256=sha(self.patch.read_bytes()))
        self.manifest = dict(tk_pin=PINS['tk'], patches=[self.entry])
        self.definitions = self.base / 'patches.json'

    def run_patch(self, system='darwin'):
        self.definitions.write_text(json.dumps(self.manifest))
        return apply_patches(self.source, system, definitions=self.definitions)

    def test_real_patch_is_bounded_and_duplicate_application_is_rejected(self):
        self.assertEqual(self.run_patch(), [self.entry])
        self.assertEqual(self.target.read_bytes(), b'first\nnew\nlast\n')
        with self.assertRaises(ValueError):
            self.run_patch()

    def test_other_platform_never_applies_patch(self):
        self.assertEqual(self.run_patch('linux'), [])
        self.assertEqual(self.target.read_bytes(), b'first\nold\nlast\n')

    def test_wrong_pin_source_or_diff_cannot_modify_export(self):
        original = self.target.read_bytes()
        for key in ('tk_pin', 'before_sha256', 'patch_sha256'):
            record = self.manifest if key == 'tk_pin' else self.entry
            correct = record[key]
            record[key] = '0' * len(correct)
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.run_patch()
            self.assertEqual(self.target.read_bytes(), original)
            record[key] = correct

    def test_parent_escape_is_rejected_before_git(self):
        for key, value in (('file', '../outside.c'), ('patch', '../outside.patch')):
            correct = self.entry[key]
            self.entry[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.run_patch()
            self.entry[key] = correct


if __name__ == '__main__':
    unittest.main()
