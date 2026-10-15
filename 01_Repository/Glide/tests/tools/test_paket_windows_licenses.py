"""Windows-Lizenzherkunft: echte native Version statt bloßer Wortsuche."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'packaging/paket'))
from windows_license_sources import dependency_version, static_sources, toolkit_references, utf8proc_version


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

    def test_own_toolkit_uses_exact_source_pins_and_old_toolkit_keeps_its_tag(self):
        refs = toolkit_references('9.1.0', '9.1', pins={'tcl':'a'*40, 'tk':'b'*40})
        self.assertTrue(refs['tcl']['raw'].endswith('/'+'a'*40))
        self.assertTrue(refs['tk']['source'].endswith('/'+'b'*40))
        self.assertNotIn('core-', refs['tcl']['source'])
        old = toolkit_references('9.0.3', '9.0')
        self.assertTrue(old['tcl']['raw'].endswith('/core-9-0-3'))

    def test_mixed_toolkit_or_missing_original_pins_are_rejected(self):
        for tcl, tk, pins in (('9.1.0','9.1',None), ('9.1.0','9.0',{'tcl':'a'*40,'tk':'b'*40}),
                ('9.0.3','9.0',{'tcl':'a'*40,'tk':'b'*40}), ('9.1.0','9.1',{'tcl':'main','tk':'b'*40}),
                ('9.1.0','9.1',{}), ('9.1.1','9.1',{'tcl':'a'*40,'tk':'b'*40})):
            with self.subTest(tcl=tcl, tk=tk, pins=pins), self.assertRaises(ValueError):
                toolkit_references(tcl, tk, pins=pins)

    def test_utf8proc_version_is_complete_and_unambiguous(self):
        header = '#define UTF8PROC_VERSION_MAJOR 2\n#define UTF8PROC_VERSION_MINOR 12\n#define UTF8PROC_VERSION_PATCH 0\n'
        self.assertEqual(utf8proc_version(header), '2.12.0')
        for invalid in ('', header.replace('PATCH', 'UNKNOWN'), header+'#define UTF8PROC_VERSION_MAJOR 3\n'):
            with self.subTest(header=invalid), self.assertRaises(ValueError):
                utf8proc_version(invalid)

    def test_version_parser_does_not_truncate_a_four_component_version(self):
        with self.assertRaises(ValueError):
            dependency_version('mpdecimal-4.0.0.1', 'mpdecimal')


if __name__ == '__main__':
    unittest.main()
