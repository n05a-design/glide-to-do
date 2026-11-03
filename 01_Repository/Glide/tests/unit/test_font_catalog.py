"""Stilzuordnung, Vorgabe und Kompatibilität ohne Tk oder Nutzdaten."""
import unittest

from font_catalog import DEFAULT, LABELS, STYLES, style_for, family_for_weight


class CatalogTests(unittest.TestCase):
    def test_requested_classifications_and_default_are_stable(self):
        self.assertEqual(LABELS, ("Modern: Rubik", "Technisch: Roboto Mono",
                                  "Kreativ: Playfair Display", "Klassisch: Fraunces"))
        self.assertEqual(DEFAULT.key, "rubik")
        self.assertEqual(len({style.key for style in STYLES}), 4)

    def test_display_keys_and_native_families_resolve_to_same_style(self):
        for style in STYLES:
            for alias in (style.key, style.label, style.family, style.tk_family, style.default_family):
                with self.subTest(alias=alias):
                    self.assertIs(style_for("  " + alias.upper() + "  "), style)
        self.assertEqual(style_for("Fraunces").tk_family, "Fraunces 72pt")
        self.assertEqual(style_for("Roboto Mono").key, "roboto_mono")

    def test_semibold_body_preserves_real_bold_and_other_families(self):
        for style in STYLES:
            self.assertEqual(family_for_weight(style.default_family), style.default_family)
            self.assertEqual(family_for_weight(style.default_family, True), style.tk_family)
            self.assertEqual(family_for_weight(style.tk_family), style.default_family)
        for family in ("DejaVu Sans", "Pixelify Sans", "Eigene Schrift"):
            self.assertEqual(family_for_weight(family), family)
            self.assertEqual(family_for_weight(family, True), family)
        for key in ("playfair_display", "fraunces"):
            style = style_for(key)
            self.assertTrue(style.default_family.endswith(" SemiBold"))
            self.assertTrue(style.body_regular.endswith("-SemiBold.ttf"))

    def test_empty_legacy_and_invalid_choices_use_current_default(self):
        for value in ("", None, "DejaVu Sans", "Glide Sans", "Unbekannt"):
            with self.subTest(value=value):
                self.assertIs(style_for(value), DEFAULT)


if __name__ == "__main__":
    unittest.main()
