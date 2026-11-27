# SPDX-License-Identifier: MPL-2.0
"""PAGE-06 (27.11.2026): Speicher der zuletzt gesehenen Stelle je Ansicht."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import view_positions as vp


class ViewPositionsTests(unittest.TestCase):
    def test_remember_recall_and_copy(self):
        stellen = vp.ViewPositions()
        stellen.remember(("page", "a"), top=10, insert=12)
        gelesen = stellen.recall(("page", "a"))
        self.assertEqual(gelesen, {"top": 10, "insert": 12})
        gelesen["top"] = 99
        self.assertEqual(stellen.recall(("page", "a"))["top"], 10, "Rückgabe ist eine Kopie")
        self.assertIsNone(stellen.recall(("page", "b")))
        stellen.remember(None, top=1)
        self.assertEqual(len(stellen), 1)
        stellen.forget(("page", "a"))
        self.assertIsNone(stellen.recall(("page", "a")))

    def test_limit_drops_oldest_and_refreshes_on_use(self):
        stellen = vp.ViewPositions(limit=2)
        stellen.remember("a", top=1)
        stellen.remember("b", top=2)
        stellen.remember("a", top=3)
        stellen.remember("c", top=4)
        self.assertIsNone(stellen.recall("b"))
        self.assertEqual(stellen.recall("a"), {"top": 3})
        self.assertEqual(len(stellen), 2)

    def test_clamping(self):
        self.assertEqual(vp.clamp_offset(50, 20), 20)
        self.assertEqual(vp.clamp_offset(5, 20), 5)
        for falsch in (-1, 2.5, None, "3", True):
            self.assertIsNone(vp.clamp_offset(falsch, 20), falsch)
        self.assertEqual(vp.clamp_fraction(1.4), 1.0)
        self.assertEqual(vp.clamp_fraction(-0.2), 0.0)
        self.assertEqual(vp.clamp_fraction("0.25"), 0.25)
        self.assertIsNone(vp.clamp_fraction(float("nan")))
        self.assertIsNone(vp.clamp_fraction(None))

    def test_row_target_prefers_existing_row(self):
        self.assertEqual(vp.row_target("x", ["a", "x"], 0.7), ("x", None))
        self.assertEqual(vp.row_target("weg", ["a"], 0.7), (None, 0.7))
        self.assertEqual(vp.row_target(None, [], None), (None, None))


if __name__ == "__main__":
    unittest.main()
