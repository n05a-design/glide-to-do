"""Karte „Neu in …“ (N07) ohne Oberfläche."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import release_notes as rn

KATALOG = {"1.0.1": ("a",), "1.0.2": ("b", "c"), "1.0.3": (), "1.1.0": tuple(f"p{i}" for i in range(7))}


class Neuerungen(unittest.TestCase):
    def test_version_tuple(self):
        self.assertEqual(rn.version_tuple("3.33.20"), (3, 33, 20))
        self.assertEqual(rn.version_tuple(" 3.4 "), (3, 4))
        for unlesbar in (None, "", "3.x", "3..1", "v3.1"):
            self.assertIsNone(rn.version_tuple(unlesbar), unlesbar)

    def test_notes_between_versions_newest_first_and_capped(self):
        self.assertEqual(rn.notes_since("1.0.0", "1.0.2", KATALOG), [("1.0.2", ["b", "c"]), ("1.0.1", ["a"])])
        neu = rn.notes_since("1.0.1", "1.1.0", KATALOG)
        self.assertEqual([version for version, _ in neu], ["1.1.0", "1.0.2"])  # 1.0.3 ohne Eintrag
        self.assertEqual(len(neu[0][1]), 5)  # höchstens fünf Punkte je Version

    def test_nothing_on_first_start_same_or_older_version(self):
        self.assertEqual(rn.notes_since(None, "1.0.2", KATALOG), [])
        self.assertEqual(rn.notes_since("1.0.2", "1.0.2", KATALOG), [])
        self.assertEqual(rn.notes_since("1.1.0", "1.0.2", KATALOG), [])
        self.assertEqual(rn.notes_since("kaputt", "1.0.2", KATALOG), [])

    def test_last_seen_distinguishes_existing_install(self):
        self.assertEqual(rn.last_seen({"release_notes_seen": "3.33.20"}, False), "3.33.20")
        self.assertEqual(rn.last_seen({}, True), rn.BEFORE_CATALOG)
        self.assertIsNone(rn.last_seen({}, False))
        self.assertEqual(rn.last_seen({"release_notes_seen": 5}, True), rn.BEFORE_CATALOG)
        self.assertTrue(rn.should_show({}, "1.0.1", KATALOG, existing_install=False) is False)

    def test_normalize_seen(self):
        self.assertEqual(rn.normalize_seen(" 3.33.20 "), "3.33.20")
        for unlesbar in (None, 5, "", "neu", ["3.33.20"]):
            self.assertIsNone(rn.normalize_seen(unlesbar), unlesbar)

    def test_remember_seen_leaves_original(self):
        alt = {"x": 1}
        neu = rn.remember_seen(alt, "3.33.20")
        self.assertEqual(neu, {"x": 1, "release_notes_seen": "3.33.20"})
        self.assertEqual(alt, {"x": 1})
        self.assertFalse(rn.should_show(neu, "3.33.20"))

    def test_catalog_entries_are_short_and_versioned(self):
        for version, punkte in rn.CATALOG.items():
            self.assertIsNotNone(rn.version_tuple(version), version)
            self.assertLessEqual(len(punkte), 5, version)
            for punkt in punkte:
                self.assertTrue(punkt.endswith((".", "“")), punkt)
                self.assertLess(len(punkt), 140, punkt)
        self.assertLess(rn.version_tuple(rn.BEFORE_CATALOG), min(rn.version_tuple(v) for v in rn.CATALOG))


if __name__ == "__main__":
    unittest.main()
