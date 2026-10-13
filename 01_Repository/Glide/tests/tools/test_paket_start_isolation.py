import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / 'packaging/paket'))
from pathlib import Path
import tempfile
import unittest
from pruefe_start_macos import profile_for, quoted_path


class ProcessIsolationContract(unittest.TestCase):
    def test_forbidden_sources_must_never_cover_or_enter_the_package(self):
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary)/'Bau/Glide.app'
            for forbidden in ([package], [package.parent], [package/'Contents']):
                with self.assertRaises(ValueError):
                    profile_for(package, forbidden)
            with self.assertRaises(ValueError):
                profile_for(package, [])

    def test_local_paths_cannot_inject_an_additional_sandbox_rule(self):
        with self.assertRaises(ValueError):
            quoted_path('/tmp/Falscher\nPfad')
        value = quoted_path('/tmp/Glide "Probe" \\ Rückfall')
        self.assertIn('\\"Probe\\"', value)
        self.assertIn('\\\\', value)

    def test_profile_blocks_external_sources_without_global_mutations(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            profile = profile_for(base/'Bau/Glide.app', [base/'Python', base/'Quellen', base/'Python'])
            self.assertEqual(profile.count('(deny file-read*'), 2)
            self.assertIn('(allow default)', profile)
            self.assertNotIn('(deny process', profile)
            self.assertFalse((base/'Python').exists())


if __name__ == '__main__':
    unittest.main()
