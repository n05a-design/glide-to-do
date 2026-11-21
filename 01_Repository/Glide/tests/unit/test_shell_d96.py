# SPDX-License-Identifier: MPL-2.0
"""Shell-Bausteine aus D96 allein: `window_geometry`, `system_appearance`, `redo_history`.

Prüft die drei Module ohne Glide-Werte und belegt, dass `compact_mode`,
`appearance` und `undo_history` dieselben Objekte weiterreichen (keine
zweite Fassung). Ohne Tk.

Aufruf: python3 -B -m unittest tests/unit/test_shell_d96.py
"""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src" / "glide"))

from glide_shell import redo_history, system_appearance, window_geometry  # noqa: E402
import appearance  # noqa: E402
import compact_mode  # noqa: E402
import undo_history  # noqa: E402


class Fenstergeometrie(unittest.TestCase):
    def test_lesen_und_schreiben(self):
        self.assertEqual(window_geometry.parse("800x600+-1700+20"), (800, 600, -1700, 20))
        self.assertEqual(window_geometry.parse("800x600-10+20"), (800, 600, None, None))
        self.assertIsNone(window_geometry.parse("0x600"))
        self.assertEqual(window_geometry.format_geometry(800, 600, -1700, 20), "800x600+-1700+20")

    def test_mindestmass_ist_pflicht_und_kommt_vom_host(self):
        with self.assertRaises(TypeError):
            window_geometry.clamp(100, 100, 0, 0, 1000, 800)  # pylint: disable=no-value-for-parameter
        self.assertEqual(window_geometry.clamp(100, 100, None, None, 1000, 800, (300, 200)), (300, 200, None, None))
        breite, hoehe, x, y = window_geometry.clamp(900, 900, 5000, 5000, 1000, 800, (300, 200), origin=(-1000, 0))
        self.assertEqual((breite, hoehe), (900, 800 - window_geometry.SCREEN_RESERVE))
        self.assertEqual((x, y), (-1000 + 1000 - window_geometry.VISIBLE_MARGIN, 800 - window_geometry.VISIBLE_MARGIN))

    def test_sichtbar_halten(self):
        self.assertEqual(window_geometry.keep_visible(-5000, -10, 800, (0, 0, 1440, 900)),
                         (-(800 - window_geometry.VISIBLE_MARGIN), 0))


class Systemmodus(unittest.TestCase):
    def test_erkennung_scheitert_ohne_ausnahme(self):
        def kaputt():
            raise OSError("no registry")
        self.assertIsNone(system_appearance.windows_is_dark(kaputt))
        self.assertTrue(system_appearance.windows_is_dark(lambda: 0))
        self.assertTrue(system_appearance.linux_is_dark("'prefer-dark'"))
        self.assertTrue(system_appearance.linux_is_dark(None, "Adwaita-dark"))
        self.assertIsNone(system_appearance.linux_is_dark())
        self.assertFalse(system_appearance.tk_is_dark("0"))
        self.assertIsNone(system_appearance.tk_is_dark("?"))

    def test_resolve_mit_beliebigen_designnamen(self):
        paar = {"light": "paper", "dark": "night"}
        self.assertEqual(system_appearance.resolve(paar, True, "paper"), "night")
        self.assertEqual(system_appearance.resolve(paar, None, "paper"), "paper")
        self.assertEqual(system_appearance.resolve(None, True, "paper"), "paper")


class Wiederholen(unittest.TestCase):
    def test_gilt_bis_zur_naechsten_aenderung(self):
        verlauf, undo = redo_history.RedoHistory(limit=2), ["a"]
        verlauf.push("x", undo)
        self.assertTrue(verlauf.validate(undo))
        verlauf.note_write()
        self.assertFalse(verlauf.validate(undo))

    def test_hoechstzahl_und_zuruecklegen(self):
        verlauf, undo = redo_history.RedoHistory(limit=2), []
        for eintrag in "abc":
            verlauf.push(eintrag, undo)
        self.assertEqual(len(verlauf), 2)
        eintrag = verlauf.pop()
        verlauf.restore(eintrag)
        self.assertEqual(verlauf.peek(), "c")
        self.assertTrue(verlauf.validate(undo))


class Weiterleitung(unittest.TestCase):
    def test_glide_module_reichen_dieselben_objekte_weiter(self):
        for host, shell, namen in (
                (compact_mode, window_geometry, ("parse", "format_geometry", "keep_visible", "VISIBLE_MARGIN")),
                (appearance, system_appearance, ("resolve", "windows_is_dark", "linux_is_dark", "tk_is_dark")),
                (undo_history, redo_history, ("RedoHistory", "DEFAULT_LIMIT"))):
            for name in namen:
                with self.subTest(host=host.__name__, name=name):
                    self.assertIs(getattr(host, name), getattr(shell, name))

    def test_kompaktmodus_behaelt_seine_vorgabe(self):
        self.assertEqual(compact_mode.clamp(10, 10, None, None, 2000, 2000)[:2], compact_mode.COMPACT_MIN)


if __name__ == "__main__":
    unittest.main()
