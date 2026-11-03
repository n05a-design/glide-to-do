"""Stilzuordnung, Vorgabe und Kompatibilität ohne Tk oder Nutzdaten."""
import unittest
from pathlib import Path
import struct

from font_catalog import DEFAULT, LABELS, STYLES, style_for, family_for_weight, actual_family, face_options


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
            self.assertTrue(style.body_family.endswith(" SemiBold"))
            self.assertTrue(style.body_regular.endswith("-SemiBold.ttf"))

    def test_macos_selects_original_semibold_postscript_faces(self):
        expected = {"playfair_display": "PlayfairDisplay-SemiBold", "fraunces": "Fraunces72pt-SemiBold"}
        for key, postscript in expected.items():
            style = style_for(key)
            self.assertEqual(style.family_for_platform("darwin"), postscript)
            for alias in (style.tk_family, style.body_family, postscript, postscript + "Italic"):
                self.assertIs(style_for(alias), style)
                self.assertEqual(family_for_weight(alias, platform="darwin"), postscript)
                self.assertEqual(family_for_weight(alias, italic=True, platform="darwin"), postscript + "Italic")
                self.assertEqual(family_for_weight(alias, bold=True, platform="darwin"), style.tk_family)
            self.assertEqual(actual_family(postscript, "darwin"), style.tk_family)
            self.assertEqual(actual_family(postscript + "Italic", "darwin"), style.tk_family)
            for platform in ("win32", "linux"):
                self.assertEqual(style.family_for_platform(platform), style.body_family)
                self.assertEqual(family_for_weight(style.tk_family, italic=True, platform=platform), style.body_family)
                self.assertEqual(actual_family(style.body_family, platform), style.body_family)

    def test_postscript_names_belong_to_bundled_original_faces(self):
        fonts = Path(__file__).resolve().parents[2] / "src/glide/resources/fonts"
        for style in STYLES:
            if not style.body_postscript:
                continue
            for italic in (False, True):
                filename = style.body_regular.replace("-SemiBold.ttf", "-SemiBoldItalic.ttf") if italic else style.body_regular
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
                self.assertIn(style.body_postscript + ("Italic" if italic else ""), names)

    def test_copying_macos_face_keeps_requested_size_and_styles(self):
        face = "Fraunces72pt-SemiBoldItalic"
        self.assertEqual(face_options((face, -16, "italic underline"), "darwin"),
                         {"family": face, "size": -16, "weight": "normal", "slant": "italic",
                          "underline": 1, "overstrike": 0})
        self.assertIsNone(face_options((face, 12), "win32"))
        self.assertIsNone(face_options(("Rubik", 12), "darwin"))
        self.assertIsNone(face_options(("TkDefaultFont",), "darwin"))

    def test_empty_legacy_and_invalid_choices_use_current_default(self):
        for value in ("", None, "DejaVu Sans", "Glide Sans", "Unbekannt"):
            with self.subTest(value=value):
                self.assertIs(style_for(value), DEFAULT)


if __name__ == "__main__":
    unittest.main()
