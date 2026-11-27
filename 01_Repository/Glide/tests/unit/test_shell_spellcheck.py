# SPDX-License-Identifier: MPL-2.0
"""Shell 0.8.0: Rechtschreibvertrag `glide_shell.spellcheck` (EDITOR-02, ohne eigene Engine)."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src" / "glide"))
from glide_shell import spellcheck as sp  # noqa: E402

WOERTER = {"de": ["Das", "Haus", "ist", "schön", "und", "Garten", "siehe"], "en": ["the", "house", "is", "nice"]}


class Woerter(unittest.TestCase):
    def test_ausgeschlossene_bereiche(self):
        text = "Haus https://x.example/Hauss www.hauss.de a@b.de C:\Pfad\Hauss /usr/hauss foo_bar API camelCase `Hauss` v2 Garten"
        gefunden = [w for _, _, w in sp.words(text)]
        self.assertEqual(gefunden, ["Haus", "Garten"])

    def test_positionen_stimmen(self):
        text = "Ein schöner Tag"
        for a, b, wort in sp.words(text):
            self.assertEqual(text[a:b], wort)


class Pruefen(unittest.TestCase):
    def setUp(self):
        self.gespeichert = []
        self.checker = sp.LayeredChecker(sp.WordListChecker(WOERTER), personal=["Glide"], on_add=self.gespeichert.append)

    def test_unbekannte_woerter_je_sprache(self):
        text = "Das Hauss ist schön und Glide"
        self.assertEqual([w for _, _, w in sp.misspelled(self.checker, text, "de")], ["Hauss"])
        self.assertEqual([w for _, _, w in sp.misspelled(self.checker, "the hous is nice", "en")], ["hous"])

    def test_vorschlaege_behalten_schreibweise(self):
        self.assertEqual(self.checker.suggest("Hauss", "de"), ["Haus"])

    def test_ignorieren_und_hinzufuegen(self):
        self.checker.ignore("Hauss")
        self.assertEqual(sp.misspelled(self.checker, "Hauss", "de"), [])
        self.checker.add("Bento")
        self.assertTrue(self.checker.check("bento", "de"))
        self.assertEqual(self.gespeichert[-1], ["bento", "glide"])

    def test_nur_geaenderte_bereiche(self):
        text = "Hauss und Gartn"
        self.assertEqual([w for _, _, w in sp.misspelled(self.checker, text, "de", ranges=[(10, 15)])], ["Gartn"])

    def test_basisklasse_und_probe(self):
        with self.assertRaises(NotImplementedError):
            sp.SpellChecker().check("x", "de")
        self.assertEqual(set(sp.probe_backends()), set(sp.OPTIONAL_BACKENDS))


if __name__ == "__main__":
    unittest.main()
