# SPDX-License-Identifier: MPL-2.0
"""Shell-Bausteine aus D98 allein: `text_fit`, `action_picker`, `runtime_paths`.

Prüft die drei Module ohne Glide-Werte und belegt, dass `ui_design`,
`action_menu` und `runtime_config` dieselben Objekte weiterreichen oder auf
sie zurückgreifen, ohne ihr Verhalten zu ändern. Ohne Tk.

Aufruf: python3 -B -m unittest tests/unit/test_shell_d98.py
"""
import json
import ntpath
import os
import pathlib
import posixpath
import sys
import tempfile
import types
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src" / "glide"))

from glide_shell import action_picker, runtime_paths, text_fit  # noqa: E402
import action_menu as glide_menu  # noqa: E402
import runtime_config  # noqa: E402
import ui_design  # noqa: E402


def breite(text):
    return len(text) * 7


class Textbreite(unittest.TestCase):
    def test_kuerzen_nach_zeichen_und_pixeln(self):
        self.assertEqual(text_fit.clip("abcdefghij", 6), "abc...")
        self.assertEqual(text_fit.clip("abc", 2), "")
        self.assertEqual(text_fit.clip("kurz", 10), "kurz")
        self.assertEqual(text_fit.fit("Ein langer Titel", breite, 70), "Ein lange…")
        self.assertEqual(text_fit.fit("abc", breite, 3), "")
        self.assertEqual(text_fit.fit("", breite, 300), "")

    def test_ruhige_umbruchbreite_und_markerausgleich(self):
        gesehen = set()
        self.assertEqual([text_fit.settled_wrap_width(w, gesehen) for w in (300, 280, 300, 290)], [300, 280, 280, 290])
        masse = {"✓": 10, "□": 14}
        messen = lambda text: sum(masse.get(z, 1) for z in text)
        ausgleich = text_fit.aligned_markers(("✓", "□", "✓"), messen)
        self.assertEqual(list(ausgleich), ["✓", "□"])
        self.assertEqual(messen(ausgleich["✓"]), 14)

    def test_glide_reicht_weiter_und_behaelt_grenze(self):
        for name in ("HAIR_SPACE", "aligned_markers", "pad_to_width", "settled_wrap_width"):
            self.assertIs(getattr(ui_design, name), getattr(text_fit, name), name)
        self.assertIs(ui_design.fit_text, text_fit.fit)
        lang = "x" * (ui_design.TITLE_MAX_CHARS + 5)
        self.assertEqual(ui_design.clip_title(lang), text_fit.clip(lang, ui_design.TITLE_MAX_CHARS))


ZEILEN = [((0,), "Öffnen", (), True, 0, "command"), ((1,), "✓ Umbrechen", (), True, 0, "command"),
          ((2, 0), "Umbenennen", ("Bearbeiten",), False, 1, "command"),
          ((3,), "Keine", (), False, 1, "command"), ((4,), "Mehr", (), True, 7, "submenu")]


class Aktionsauswahl(unittest.TestCase):
    def test_eintraege_ohne_glide_werte(self):
        gefunden = action_picker.entries(ZEILEN, ("Datei",), placeholders=("Keine",),
                                       reason=lambda label, path: f"{label}@{'/'.join(path)}")
        self.assertEqual([e.label for e in gefunden], ["Öffnen", "Umbrechen", "Umbenennen", "Mehr"])
        self.assertEqual([e.section for e in gefunden], ["Datei", "Datei", "Bearbeiten", action_picker.FALLBACK_SECTION])
        self.assertTrue(gefunden[1].checked)
        self.assertEqual(gefunden[2].reason, "Umbenennen@Bearbeiten")
        self.assertEqual(gefunden[3].kind, "submenu")
        self.assertEqual(len(action_picker.entries(ZEILEN * 100, limit=5)), 5)
        self.assertEqual(action_picker.counts(gefunden), (3, 4))

    def test_suche_mit_einfachem_und_eigenem_schluessel(self):
        gefunden = action_picker.entries(ZEILEN, ("Datei",))
        self.assertEqual([e.label for e in action_picker.search(gefunden, "um")], ["Umbrechen", "Umbenennen"])
        self.assertEqual([e.label for e in action_picker.search(gefunden, "bearb")], ["Umbenennen"])
        self.assertEqual(action_picker.search(gefunden, "oeffnen"), [])
        glide = [e.label for e in action_picker.search(gefunden, "oeffnen", glide_menu.content_search.search_key)]
        self.assertEqual(glide, ["Öffnen"])

    def test_glide_reicht_weiter_und_behaelt_texte(self):
        for name in ("Entry", "check_label", "clean_label", "grouped", "first_enabled", "CHECK_MARK", "PATH_SEPARATOR"):
            self.assertIs(getattr(glide_menu, name), getattr(action_picker, name), name)
        gefunden = glide_menu.entries(ZEILEN, ("Datei",))
        self.assertEqual(gefunden[-1].section, "Weitere")
        self.assertNotIn("Keine", [e.label for e in gefunden])
        self.assertEqual(gefunden[2].reason, glide_menu.DEFAULT_REASON)
        self.assertEqual(glide_menu.summary(gefunden, ""), "3 von 4 Aktionen verfügbar")


def simuliert(plattform, heim):
    flavour = ntpath if plattform == "win32" else posixpath
    return types.SimpleNamespace(join=flavour.join, abspath=flavour.abspath,
                                 expanduser=lambda wert: heim + wert[1:] if wert.startswith("~") else wert)


class Laufzeitpfade(unittest.TestCase):
    def test_plattformordner(self):
        mac, win, lin = "/Users/nutzer", "C:\\Users\\nutzer", "/home/nutzer"
        faelle = (
            ("darwin", mac, {}, mac + "/Library/Application Support/App", mac + "/Library/Caches/App"),
            ("win32", win, {"APPDATA": win + "\\R", "LOCALAPPDATA": win + "\\L"}, win + "\\R\\App", win + "\\L\\App\\Cache"),
            ("win32", win, {}, win + "\\App", win + "\\App\\Cache"),
            ("linux", lin, {}, lin + "/.local/share/App", lin + "/.cache/app"),
            ("linux", lin, {"XDG_DATA_HOME": "/d", "XDG_CACHE_HOME": "/c"}, "/d/App", "/c/app"),
        )
        for plattform, heim, umgebung, daten, cache in faelle:
            with self.subTest(plattform=plattform, umgebung=umgebung):
                pfad = simuliert(plattform, heim)
                self.assertEqual(runtime_paths.platform_data_dir("App", plattform, umgebung, pfad), daten)
                self.assertEqual(runtime_paths.platform_cache_dir("App", plattform, umgebung, pfad), cache)

    def test_reihenfolge_ohne_seiteneffekt(self):
        with tempfile.TemporaryDirectory(prefix="glide-d98-") as ordner:
            standard, zeiger = os.path.join(ordner, "standard"), os.path.join(ordner, "zeiger.json")
            self.assertEqual(runtime_paths.resolve_base(None, {}, "X_DIR", standard, zeiger), (standard, False))
            with open(zeiger, "w", encoding="utf-8-sig") as datei:
                json.dump({"path": os.path.join(ordner, "gewaehlt")}, datei)
            self.assertEqual(runtime_paths.resolve_base(None, {}, "X_DIR", standard, zeiger),
                             (os.path.join(ordner, "gewaehlt"), False))
            self.assertEqual(runtime_paths.resolve_base(None, {"X_DIR": ordner}, "X_DIR", standard, zeiger), (ordner, True))
            self.assertEqual(runtime_paths.resolve_base(ordner + "/a", {"X_DIR": "/b"}, "X_DIR", standard, zeiger),
                             (os.path.abspath(ordner + "/a"), True))
            with open(zeiger, "w", encoding="utf-8") as datei:
                datei.write("{kaputt")
            self.assertIsNone(runtime_paths.read_pointer(zeiger))
            self.assertEqual(sorted(os.listdir(ordner)), ["zeiger.json"])
        self.assertIsNone(runtime_paths.env_dir({"X_DIR": ""}, "X_DIR"))

    def test_glide_nutzt_die_mechanik_mit_eigenen_namen(self):
        with tempfile.TemporaryDirectory(prefix="glide-d98-") as ordner:
            pfade = runtime_config.resolve_paths(env={"GLIDE_DATA_DIR": ordner, "GLIDE_CACHE_DIR": ordner + "/c"})
            self.assertEqual((pfade.base_dir, pfade.is_overridden), (os.path.abspath(ordner), True))
            self.assertEqual(pfade.cache_dir, os.path.abspath(ordner + "/c"))
            self.assertEqual(os.path.basename(pfade.pointer_file), "datenordner.json")
            self.assertEqual(os.listdir(ordner), [])


if __name__ == "__main__":
    unittest.main()
