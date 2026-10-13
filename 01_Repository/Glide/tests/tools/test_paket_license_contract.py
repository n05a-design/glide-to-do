import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / 'packaging/paket'))
from pathlib import Path
import tempfile
import unittest

from license_contract import macos_native_components, windows_native_components, pure_components, resource_components, validate_components


class LicenseContractTests(unittest.TestCase):
    def test_vendor_and_site_packages_never_inherit_python_license(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            options = dict(stage=root/'source', stdlib=root/'python', pyinstaller=root/'builder/PyInstaller')
            records = [('glide_app', str(root/'source/glide_app.py'), 'PYMODULE'),
                       ('json', str(root/'python/json/__init__.py'), 'PYMODULE'),
                       ('tkinterdnd2', str(root/'source/vendor/tkinterdnd2/__init__.py'), 'PYMODULE')]
            self.assertEqual(pure_components(records, **options),
                             {'glide_app':['Glide'], 'json':['Python'], 'tkinterdnd2':['tkinterdnd2']})
            for path in ('source/vendor/alien/__init__.py', 'python/site-packages/alien.py',
                         'source/untracked/nested.py', 'foreign/alien.py'):
                with self.subTest(path=path), self.assertRaisesRegex(ValueError, 'belegte Herkunft'):
                    pure_components([('alien', str(root/path), 'PYMODULE')], **options)

    def test_multiple_embedded_components_and_unknown_native_files(self):
        prefix = 'Contents/Frameworks/python3__dot__14/lib-dynload/'
        names = ['Contents/Frameworks/Tk', prefix+'_lzma.cpython-314-darwin.so',
                 prefix+'_decimal.cpython-314-darwin.so', prefix+'pyexpat.cpython-314-darwin.so']
        result = macos_native_components(names)
        self.assertEqual(result[names[0]], ['Tk', 'NanoSVG'])
        self.assertEqual(result[names[1]], ['Python', 'liblzma'])
        self.assertEqual(result[names[2]], ['Python', 'libmpdec'])
        self.assertEqual(result[names[3]], ['Python'])
        for path in ('Contents/Frameworks/libalien.dylib', prefix+'alien.cpython-314-darwin.so',
                     'Contents/Frameworks/../libssl.3.dylib'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                macos_native_components([path])

    def test_absent_embedded_license_and_duplicate_record_block_delivery(self):
        matrix = macos_native_components(['Contents/Frameworks/Tk'])
        tk = dict(name='Tk', version='9.0.3', source='official pin', files={'Tk-LICENSE':'digest'})
        with self.assertRaisesRegex(ValueError, 'NanoSVG'):
            validate_components(matrix, [tk])
        nano = dict(name='NanoSVG', version='pin', source='official pin', files={'NanoSVG-LICENSE':'digest'})
        self.assertEqual(set(validate_components(matrix, [tk, nano])), {'Tk', 'NanoSVG'})
        with self.assertRaisesRegex(ValueError, 'doppelter'):
            validate_components(matrix, [tk, nano, tk])


    def test_tcl_requires_its_embedded_arithmetic_and_regex_licenses(self):
        matrix = macos_native_components(['Contents/Frameworks/Tcl'])
        def record(name):
            return dict(name=name, version='Tcl 9.0.3 pin', source='official pinned source',
                        files={name+'-LICENSE':'digest'})
        with self.assertRaisesRegex(ValueError, 'Henry-Spencer-Regex.*libtommath'):
            validate_components(matrix, [record('Tcl')])
        complete = [record(name) for name in ('Tcl', 'libtommath', 'Henry-Spencer-Regex')]
        self.assertEqual(set(validate_components(matrix, complete)),
                         {'Tcl', 'libtommath', 'Henry-Spencer-Regex'})

    def test_timezone_resource_licenses_cannot_hide_behind_application_license(self):
        names = ['resources/timezones/iana-2026e.zip','resources/timezones/windowsZones.xml',
                 'resources/timezones/provenance.json']
        matrix = resource_components(names)
        self.assertEqual(matrix[names[0]],['IANA-Zeitzonen'])
        self.assertEqual(matrix[names[1]],['Unicode-CLDR'])
        self.assertEqual(matrix[names[2]],['IANA-Zeitzonen','Unicode-CLDR'])
        glide = dict(name='Glide', version='dev', source='LICENSE.md', files={'license':'digest'})
        with self.assertRaisesRegex(ValueError,'IANA-Zeitzonen.*Unicode-CLDR'):
            validate_components(matrix,[glide])

    def test_unknown_or_ambiguous_resources_block_the_build(self):
        self.assertEqual(resource_components(['resources/fonts/DejaVuSans.ttf']),
                         {'resources/fonts/DejaVuSans.ttf':['Glide-Schriften']})
        for names in (['resources/unknown/image.png'],['resources/timezones/iana-2027a.zip'],
                      ['resources/../outside'],['resources/logo/icon.png','resources/logo/icon.png']):
            with self.subTest(names=names),self.assertRaises(ValueError):resource_components(names)

    def test_cpython_queue_is_attributed_to_python_and_not_unknown_extensions(self):
        name='Contents/Frameworks/python3__dot__14/lib-dynload/_queue.cpython-314-darwin.so'
        self.assertEqual(macos_native_components([name]),{name:['Python']})
        with self.assertRaisesRegex(ValueError,'belegte Lizenzzuordnung'):
            macos_native_components([name.replace('_queue','_unknown_queue')])

    def test_windows_tcl_external_arithmetic_and_runtime_have_separate_licenses(self):
        names = ['Glide.exe', '_internal/tcl90.dll', '_internal/tcl9tk90.dll',
                 '_internal/libtommath.dll', '_internal/libffi-8.dll', '_internal/VCRUNTIME140.dll',
                 '_internal/_ctypes.pyd', '_internal/_lzma.pyd']
        matrix = windows_native_components(names)
        self.assertEqual(matrix['_internal/tcl90.dll'], ['Tcl', 'Henry-Spencer-Regex'])
        self.assertEqual(matrix['_internal/tcl9tk90.dll'], ['Tk', 'NanoSVG'])
        self.assertEqual(matrix['_internal/libtommath.dll'], ['libtommath'])
        self.assertEqual(matrix['_internal/libffi-8.dll'], ['libffi'])
        self.assertEqual(matrix['_internal/_lzma.pyd'], ['Python', 'liblzma'])
        records = [dict(name=name,version='native pin',source='official source',files={'license':'digest'})
                   for name in {v for values in matrix.values() for v in values} - {'Microsoft-VC-Runtime'}]
        with self.assertRaisesRegex(ValueError, 'Microsoft-VC-Runtime'):
            validate_components(matrix, records)

    def test_windows_new_dlls_extensions_and_duplicate_names_refuse_the_build(self):
        for names in (['_internal/alien.dll'], ['_internal/_unknown.pyd'],
                      ['_internal/python315.dll'], ['_internal/../outside.dll'],
                      ['_internal/python314.dll', '_internal/PYTHON314.DLL'],
                      ['_internal/tcl86t.dll'], []):
            with self.subTest(names=names), self.assertRaises(ValueError):
                windows_native_components(names)


if __name__ == '__main__':
    unittest.main()
