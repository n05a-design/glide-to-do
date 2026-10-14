"""Windows-Lizenzherkunft: echte native Version statt bloßer Wortsuche."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'packaging/paket'))
from windows_license_sources import dependency_version, static_sources


class WindowsLicenseSources(unittest.TestCase):
    externals = 'set libraries=%libraries% mpdecimal-4.0.0\nset libraries=%libraries% zlib-ng-2.2.4\n'

    def test_static_components_have_their_own_complete_original_terms(self):
        records = static_sources(self.externals, '4.0.0', '2.2.4')
        self.assertEqual([record['name'] for record in records], ['libmpdec', 'zlib-ng'])
        self.assertTrue(records[0]['url'].endswith('/mpdecimal-4.0.0/COPYRIGHT.txt'))
        self.assertTrue(records[1]['url'].endswith('/zlib-ng-2.2.4/LICENSE.md'))
        self.assertNotEqual(records[0]['file'], records[1]['file'])

    def test_missing_ambiguous_or_changed_native_versions_refuse_the_build(self):
        for externals, decimal, zlib in (('', '4.0.0', '2.2.4'),
                (self.externals + ' mpdecimal-4.0.1', '4.0.0', '2.2.4'),
                (self.externals, '4.0.1', '2.2.4'), (self.externals, '4.0.0', None)):
            with self.subTest(externals=externals, decimal=decimal, zlib=zlib), self.assertRaises(ValueError):
                static_sources(externals, decimal, zlib)

    def test_version_parser_does_not_truncate_a_four_component_version(self):
        with self.assertRaises(ValueError):
            dependency_version('mpdecimal-4.0.0.1', 'mpdecimal')


if __name__ == '__main__':
    unittest.main()
