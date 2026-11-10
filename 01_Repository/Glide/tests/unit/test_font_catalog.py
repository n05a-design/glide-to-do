# SPDX-License-Identifier: MPL-2.0
"""Stilzuordnung, Vorgabe und Kompatibilität ohne Tk oder Nutzdaten."""
import unittest
from pathlib import Path
import struct

from font_catalog import DEFAULT, LABELS, STYLES, style_for, family_for_weight, actual_family, face_options


class CatalogTests(unittest.TestCase):
    def test_requested_classifications_and_default_are_stable(self):
        self.assertEqual(LABELS, ("Modern: Rubik", "Technisch: DM Mono",
                                  "Kreativ: DM Serif Display", "Klassisch: Charis SIL"))
        self.assertEqual(DEFAULT.key, "rubik")
        self.assertEqual(len({style.key for style in STYLES}), 4)

    def test_display_keys_and_native_families_resolve_to_same_style(self):
        for style in STYLES:
            for alias in (style.key, style.label, style.family, style.tk_family, style.default_family):
                with self.subTest(alias=alias):
                    self.assertIs(style_for("  " + alias.upper() + "  "), style)
            for alias in style.aliases:
                with self.subTest(legacy_alias=alias):
                    self.assertIs(style_for(alias), style)
                    self.assertEqual(family_for_weight(alias, True), style.tk_family)
        self.assertEqual(style_for("DM Serif Display").key, "dm_serif_display")
        self.assertEqual(style_for("Charis SIL").key, "charis_sil")

    def test_weight_mapping_preserves_other_families_and_automatic_emphasis(self):
        for style in STYLES:
            self.assertEqual(family_for_weight(style.default_family), style.default_family)
            self.assertEqual(family_for_weight(style.default_family, True), style.tk_family)
            self.assertEqual(family_for_weight(style.tk_family), style.default_family)
        for family in ("DejaVu Sans", "Pixelify Sans", "Eigene Schrift"):
            self.assertEqual(family_for_weight(family), family)
            self.assertEqual(family_for_weight(family, True), family)
        self.assertFalse(style_for("dm_mono").automatic_bold)
        self.assertTrue(style_for("dm_serif_display").automatic_bold)
        self.assertTrue(style_for("charis_sil").automatic_bold)

    def test_platform_families_resolve_to_the_selected_static_fonts(self):
        for style in STYLES:
            for platform in ("win32", "darwin", "linux"):
                with self.subTest(style=style.key, platform=platform):
                    self.assertEqual(style.family_for_platform(platform), style.tk_family)
                    self.assertEqual(family_for_weight(style.tk_family, True, platform=platform), style.tk_family)
                    self.assertEqual(actual_family(style.tk_family, platform), style.tk_family)

    def test_bundled_font_files_and_postscript_names_match_the_catalog(self):
        fonts = Path(__file__).resolve().parents[2] / "src/glide/resources/fonts"
        expected = {
            "DMMono-Regular.ttf": "DMMono-Regular",
            "DMMono-Medium.ttf": "DMMono-Medium",
            "DMMono-Italic.ttf": "DMMono-Italic",
            "DMMono-MediumItalic.ttf": "DMMono-MediumItalic",
            "DMSerifDisplay-Regular.ttf": "DMSerifDisplay-Regular",
            "DMSerifDisplay-Italic.ttf": "DMSerifDisplay-Italic",
            "CharisSIL-Regular.ttf": "CharisSIL",
            "CharisSIL-Bold.ttf": "CharisSIL-Bold",
            "CharisSIL-Italic.ttf": "CharisSIL-Italic",
            "CharisSIL-BoldItalic.ttf": "CharisSIL-BoldItalic",
        }
        for filename, postscript in expected.items():
            with self.subTest(filename=filename):
                data = (fonts / filename).read_bytes()
                tables = {struct.unpack_from(">4sIII", data, 12 + i * 16)[0]:
                          struct.unpack_from(">4sIII", data, 12 + i * 16)[2]
                          for i in range(struct.unpack_from(">H", data, 4)[0])}
                offset = tables[b"name"]
                _, count, start = struct.unpack_from(">HHH", data, offset)
                names = set()
                for index in range(count):
                    platform, _, _, key, length, position = struct.unpack_from(">HHHHHH", data, offset + 6 + index * 12)
                    if platform in (0, 3) and key == 6:
                        names.add(data[offset + start + position:offset + start + position + length].decode("utf-16-be"))
                self.assertIn(postscript, names)
        for style in STYLES:
            self.assertTrue((fonts / style.regular).is_file(), style.regular)
            self.assertTrue((fonts / style.bold).is_file(), style.bold)

    def test_unaliased_font_families_use_the_native_tk_resolution(self):
        self.assertIsNone(face_options(("DM Serif Display", 12), "darwin"))
        self.assertIsNone(face_options(("Rubik", 12), "darwin"))
        self.assertIsNone(face_options(("TkDefaultFont",), "darwin"))

    def test_fontconfig_resolves_current_and_legacy_family_names(self):
        for style in STYLES:
            self.assertEqual(actual_family(style.family, "linux"), style.tk_family)
            for alias in style.aliases:
                self.assertEqual(actual_family(alias, "linux"), style.tk_family)

    def test_empty_legacy_and_invalid_choices_use_current_default(self):
        for value in ("", None, "DejaVu Sans", "Glide Sans", "Unbekannt"):
            with self.subTest(value=value):
                self.assertIs(style_for(value), DEFAULT)


if __name__ == "__main__":
    unittest.main()
