"""Stilzuordnung, Vorgabe und Kompatibilität ohne Tk oder Nutzdaten."""
import unittest

from font_catalog import DEFAULT, LABELS, STYLES, style_for


class CatalogTests(unittest.TestCase):
    def test_requested_classifications_and_default_are_stable(self):
        self.assertEqual(LABELS, ("Modern: Rubik", "Technisch: Roboto Mono",
                                  "Klassisch: Playfair Display", "Kreativ: Fraunces"))
        self.assertEqual(DEFAULT.key, "rubik")
        self.assertEqual(len({style.key for style in STYLES}), 4)

    def test_display_keys_and_native_families_resolve_to_same_style(self):
        for style in STYLES:
            for alias in (style.key, style.label, style.family, style.tk_family):
                with self.subTest(alias=alias):
                    self.assertIs(style_for("  " + alias.upper() + "  "), style)
        self.assertEqual(style_for("Fraunces").tk_family, "Fraunces 72pt")
        self.assertEqual(style_for("Roboto Mono").key, "roboto_mono")

    def test_empty_legacy_and_invalid_choices_use_current_default(self):
        for value in ("", None, "DejaVu Sans", "Glide Sans", "Unbekannt"):
            with self.subTest(value=value):
                self.assertIs(style_for(value), DEFAULT)


if __name__ == "__main__":
    unittest.main()
