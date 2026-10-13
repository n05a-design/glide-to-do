"""Portabler Aufruf und Bindung der Originalbelege an die Baulaufzeit."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[2] / 'packaging/paket'
sys.path.insert(0, str(TOOLS))
import lizenzen_vorbereiten_macos as licenses


class MacLicenseTests(unittest.TestCase):
    def test_repository_basis_preserves_original_license_bytes(self):
        basis = TOOLS / 'lizenzen/macos'
        document = json.loads((basis / 'manifest.json').read_text(encoding='utf-8'))
        components = {record['name']: record for record in document['components']}
        versions = {name: components[label]['version'] for name, label in licenses.BUILD.items()}
        self.assertEqual(len(licenses.verified_basis(basis, document['runtime'], versions)['components']),
                         len(document['components']))

    def test_cli_is_available_without_private_context_or_build_dependencies(self):
        with tempfile.TemporaryDirectory() as folder:
            result = subprocess.run([sys.executable, '-B', str(TOOLS / 'lizenzen_vorbereiten_macos.py'), '--help'],
                                    cwd=folder, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('--basis', result.stdout)

    def test_changed_runtime_and_tampered_original_license_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            basis = Path(folder)
            text = basis / 'Original.txt'
            text.write_bytes(b'Originaler Lizenzbeleg\n')
            runtime = {'python': '3.14.5'}
            versions = {name: 'pin' for name in licenses.BUILD}
            components = [dict(name=label, version='pin', source='gepruefte Quelle',
                               files={'Original.txt': hashlib.sha256(text.read_bytes()).hexdigest()})
                          for label in licenses.BUILD.values()]
            (basis / 'manifest.json').write_text(json.dumps(dict(runtime=runtime, components=components)))
            result = licenses.verified_basis(basis, runtime, versions)
            result['components'].clear()
            self.assertEqual(len(licenses.verified_basis(basis, runtime, versions)['components']), len(components))
            with self.assertRaisesRegex(ValueError, 'Baulaufzeit'):
                licenses.verified_basis(basis, {'python': '3.14.6'}, versions)
            changed = copy.deepcopy(versions)
            changed['pyinstaller'] = 'anderer Pin'
            with self.assertRaisesRegex(ValueError, 'Bauabhängigkeit'):
                licenses.verified_basis(basis, runtime, changed)
            text.write_bytes(b'Veraendert\n')
            with self.assertRaisesRegex(ValueError, 'Lizenzbeleg'):
                licenses.verified_basis(basis, runtime, versions)


if __name__ == '__main__':
    unittest.main()
