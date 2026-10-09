"""Darstellungsregeln ohne Tk: Platz, Auslassung und unveränderte Skalen."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import ui_design as design


class DesignTest(unittest.TestCase):
    def test_scales_keep_existing_values_and_are_immutable(self):
        self.assertEqual(design.RADII["card"], 18)
        self.assertEqual(design.FONT_SIZES["title"], 24)
        self.assertEqual(design.ROW_HEIGHTS["task"], 36)
        with self.assertRaises(TypeError):
            design.SPACING[12] = 14

    def test_fit_text_at_edges(self):
        for text in ("", "Heute", "äöüß", "Aufgabe   mit Rand", "x" * 10000):
            for width in range(30):
                shown = design.fit_text(text, len, width)
                self.assertLessEqual(len(shown), width)
                if len(text) <= width:
                    self.assertEqual(shown, text)
                elif shown:
                    self.assertTrue(shown.endswith("…"))
                    self.assertTrue(text.startswith(shown[:-1]))

    def test_fit_text_measures_glyphs_and_bounds_calls(self):
        calls = []
        def measure(text):
            calls.append(text)
            return sum(3 if c == "W" else 1 for c in text)
        self.assertEqual(design.fit_text("WWWabc", measure, 7), "WW…")
        calls.clear()
        self.assertEqual(design.fit_text("W" * 10000, measure, 20), "W" * 6 + "…")
        self.assertLess(len(calls), 20)
        self.assertEqual(design.fit_text("W", measure, 0), "")

    def test_today_title_and_source_fit_at_supported_widths(self):
        for width in range(400, 1800):
            title, due, labels, source, gap = design.today_columns(width, 132, 160)
            self.assertGreaterEqual(title, 260)
            self.assertGreaterEqual(source, 100)
            self.assertLessEqual(source, 180)
            self.assertLessEqual(title + due + labels + source + gap + 6, width)
        self.assertEqual(design.today_columns(480, 132, 160)[1:3], (0, 0))
        self.assertEqual(design.today_columns(1200, 132, 160)[1:3], (132, 160))


if __name__ == "__main__":
    unittest.main()
