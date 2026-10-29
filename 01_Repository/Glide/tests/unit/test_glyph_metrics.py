"""Optische Symbolmitte aus den Glyphenrahmen der mitgelieferten Schrift (B09)."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import glyph_metrics as gm

SCHRIFTEN = Path(__file__).resolve().parents[2] / "src/glide/resources/fonts"


class GlyphMetrics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.normal = gm.load(SCHRIFTEN / "DejaVuSans.ttf")
        cls.fett = gm.load(SCHRIFTEN / "DejaVuSans-Bold.ttf")

    def test_reads_units_cap_height_and_known_boxes(self):
        self.assertEqual(self.normal.units_per_em, 2048)
        self.assertEqual(self.normal.cap_height, self.normal.bbox("H")[3])
        self.assertEqual(self.normal.bbox("H")[1], 0)
        self.assertTrue(self.normal.covers("▽") and self.normal.covers("♲"))
        self.assertFalse(self.normal.covers("\u2315"), "Die Lupe fehlt der UI-Schrift (Grund für B10)")
        self.assertIsNone(self.normal.bbox(" "))

    def test_triangle_sits_below_and_recycling_sign_near_cap_center(self):
        kappe = self.normal.cap_center()
        self.assertLess(self.normal.ink_center("▽"), kappe - 0.08)
        self.assertAlmostEqual(self.normal.ink_center("♲"), kappe, delta=0.02)
        self.assertAlmostEqual(self.normal.ink_center("▣"), self.normal.ink_center("◉"), delta=0.01)

    def test_relative_shift_moves_odd_glyph_to_reference_family(self):
        self.assertEqual(gm.relative_shift(self.fett, "▣", "▣", 16), 0)
        self.assertEqual(gm.relative_shift(self.fett, "◉", "▣", 16), 0)
        self.assertEqual(gm.relative_shift(self.fett, "♲", "▣", 16), 2)
        self.assertEqual(gm.relative_shift(None, "♲", "▣", 16), 0)
        self.assertEqual(gm.relative_shift(self.fett, "\u2315", "▣", 16), 0)

    def test_multi_character_symbols_use_their_common_height(self):
        # ICONS["priority_high"] ist "⚑⚑"; bbox() allein verlangt ein Zeichen.
        self.assertEqual(self.fett.ink_center("⚑⚑"), self.fett.ink_center("⚑"))
        self.assertEqual(self.fett.ink_center("⚑ "), self.fett.ink_center("⚑"))
        self.assertEqual(gm.relative_shift(self.fett, "⚑⚑", "▣", 16), gm.relative_shift(self.fett, "⚑", "▣", 16))
        hoch, tief = self.normal.bbox("♲"), self.normal.bbox("▽")
        erwartet = (min(hoch[1], tief[1]) + max(hoch[3], tief[3])) / 2 / self.normal.units_per_em
        self.assertAlmostEqual(self.normal.ink_center("♲▽"), erwartet, places=9)
        self.assertIsNone(self.normal.ink_center(""))
        self.assertIsNone(self.normal.ink_center("  "))

    def test_label_center_puts_symbol_center_on_cap_center(self):
        grundlinie, text_px, symbol_px = 23.0, 16.0, 12.0
        mitte = gm.label_center_for_cap(grundlinie, self.fett, text_px, self.normal, "▽", symbol_px, 11, 14)
        symbol_grundlinie = mitte - 14 / 2 + 11
        symbol_mitte = symbol_grundlinie - self.normal.ink_center("▽") * symbol_px
        self.assertAlmostEqual(symbol_mitte, grundlinie - self.fett.cap_center() * text_px, places=6)
        self.assertIsNone(gm.label_center_for_cap(grundlinie, self.fett, text_px, self.normal, "\u2315", 12, 11, 14))

    def test_broken_font_file_is_a_value_error(self):
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".ttf", delete=False) as datei:
            datei.write(b"\x00\x01\x00\x00\x00\x00")
        try:
            with self.assertRaises(ValueError):
                gm.load(datei.name)
        finally:
            Path(datei.name).unlink()


if __name__ == "__main__":
    unittest.main()
