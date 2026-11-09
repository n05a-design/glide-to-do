# SPDX-License-Identifier: MPL-2.0
"""Keine verlorenen, doppelten oder optional gewordenen Arbeitsmodifälle."""
from pathlib import Path
import unittest
from arbeitsmodi_gruppen import GRUPPEN, fallbestand, gruppen


class ArbeitsmodigruppenTests(unittest.TestCase):
    def test_all_implemented_cases_are_mandatory_exactly_once_in_original_order(self):
        cases = fallbestand(Path(__file__).resolve().parents[1] / 'integration/test_arbeitsmodi.py')
        groups = gruppen(cases)
        self.assertEqual(tuple(groups), GRUPPEN)
        self.assertTrue(all(groups.values()))
        self.assertEqual(tuple(case for group in groups.values() for case in group), cases)
        self.assertEqual(len(cases), len(set(cases)))

    def test_missing_duplicate_or_reordered_boundary_fails_instead_of_skipping(self):
        cases = fallbestand(Path(__file__).resolve().parents[1] / 'integration/test_arbeitsmodi.py')
        for broken in (cases[1:], cases + (cases[0],), tuple(reversed(cases))):
            with self.subTest(cases=broken[:2]):
                with self.assertRaises(ValueError):
                    gruppen(broken)


if __name__ == '__main__':
    unittest.main()
