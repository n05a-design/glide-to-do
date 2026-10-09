"""Erscheinungsbild „Automatisch (hell/dunkel)“ (N01) ohne Oberfläche."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import appearance as a

DESIGNS = {
    "light": {"base": "light", "partner": "dark"},
    "dark": {"base": "dark", "partner": "light"},
    "glass_light": {"base": "light", "partner": "glass_dark"},
    "glass_dark": {"base": "dark", "partner": "glass_light"},
    "pixel": {"base": "dark", "partner": "pixel"},
    "dopamine": {"base": "dark", "partner": "dopamine"},
}


class Paare(unittest.TestCase):
    def test_pair_from_either_side(self):
        self.assertEqual(a.pair_for("glass_dark", DESIGNS), {"light": "glass_light", "dark": "glass_dark"})
        self.assertEqual(a.pair_for("glass_light", DESIGNS), {"light": "glass_light", "dark": "glass_dark"})
        self.assertEqual(a.pair_for("light", DESIGNS), {"light": "light", "dark": "dark"})

    def test_dark_only_design_uses_light_by_day(self):
        self.assertEqual(a.pair_for("pixel", DESIGNS), {"light": "light", "dark": "pixel"})
        self.assertEqual(a.pair_for("dopamine", DESIGNS), {"light": "light", "dark": "dopamine"})
        self.assertIsNone(a.pair_for("unbekannt", DESIGNS))

    def test_normalize(self):
        self.assertEqual(a.normalize_auto({"light": "light", "dark": "pixel", "x": 1}, DESIGNS),
                         {"light": "light", "dark": "pixel"})
        for kaputt in (None, True, [], {"light": "light"}, {"light": "weg", "dark": "dark"}):
            self.assertIsNone(a.normalize_auto(kaputt, DESIGNS), kaputt)

    def test_resolve(self):
        paar = {"light": "light", "dark": "pixel"}
        self.assertEqual(a.resolve(paar, True, "light"), "pixel")
        self.assertEqual(a.resolve(paar, False, "pixel"), "light")
        self.assertEqual(a.resolve(paar, None, "pixel"), "pixel")  # Erkennung gescheitert
        self.assertEqual(a.resolve(None, True, "glass_light"), "glass_light")  # aus


class Erkennung(unittest.TestCase):
    def test_windows(self):
        self.assertTrue(a.windows_is_dark(lambda: 0))
        self.assertFalse(a.windows_is_dark(lambda: 1))

        def fehlt():
            raise OSError("kein Schlüssel")
        self.assertIsNone(a.windows_is_dark(fehlt))
        self.assertIsNone(a.windows_is_dark(lambda: "0"))
        self.assertIsNone(a.windows_is_dark(lambda: True))

    def test_linux(self):
        self.assertTrue(a.linux_is_dark("'prefer-dark'"))
        self.assertFalse(a.linux_is_dark("'default'"))
        self.assertTrue(a.linux_is_dark("'default'", "'Adwaita-dark'"))
        self.assertFalse(a.linux_is_dark(None, "'Adwaita'"))
        self.assertIsNone(a.linux_is_dark(None, None))

    def test_tk(self):
        self.assertTrue(a.tk_is_dark(1))
        self.assertFalse(a.tk_is_dark("0"))
        self.assertIsNone(a.tk_is_dark("vielleicht"))


if __name__ == "__main__":
    unittest.main()
