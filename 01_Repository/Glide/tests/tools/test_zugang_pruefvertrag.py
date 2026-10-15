import unittest

from zugang_pruefvertrag import native_zugangspruefung


class ZugangsPruefvertrag(unittest.TestCase):
    def test_four_and_later_cannot_silently_pass_on_fallback(self):
        for version in ('4.0.0', '4.0.1', '4.10.0', '10.0.0'):
            with self.subTest(version=version):
                self.assertTrue(native_zugangspruefung(version))

    def test_preparation_can_require_native_without_changing_delivered_version(self):
        self.assertFalse(native_zugangspruefung('3.42.0'))
        self.assertTrue(native_zugangspruefung('3.42.0', angefordert=True))

    def test_ambiguous_versions_fail_instead_of_skipping_native_checks(self):
        for version in ('4', '4.0.0-beta', 'v4.0.0', '', '4.0.0\n'):
            with self.subTest(version=version), self.assertRaises(ValueError):
                native_zugangspruefung(version)


if __name__ == '__main__':
    unittest.main()
