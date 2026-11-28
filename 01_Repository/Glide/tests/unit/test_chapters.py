# SPDX-License-Identifier: MPL-2.0
"""Unit-Tests für `chapters` (PAGE-02): Projektion, Baum, Umbenennen, Auflösen, Ebenen, Verschieben."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src" / "glide"))
import chapters  # noqa: E402


def dokument(zeilen):
    """[(Ebene oder None, Text)] → Seitendokument mit Überschriftenbereichen und einem Fettbereich."""
    text, spans = "", []
    for stufe, zeile in zeilen:
        start = len(text)
        text += zeile + "\n"
        if stufe:
            spans.append({"tag": f"h{stufe}", "start": start, "end": start + len(zeile)})
    text = text[:-1]
    return {"text": text, "spans": spans, "links": {}}


BEISPIEL = [(1, "Projektentwicklung"), (None, "Einleitung"), (2, "Grundlagen"), (None, "A"), (2, "Architektur"),
            (3, "Datenmodell"), (None, "B **fett**"), (3, "Schnittstellen"), (None, "C"), (2, "Architektur"),
            (None, "Doppelt")]


class Projektion(unittest.TestCase):
    def test_kapitel_ebenen_abschnitte_und_eltern(self):
        doc = dokument(BEISPIEL)
        k = chapters.outline(doc)
        self.assertEqual([c.title for c in k], ["Projektentwicklung", "Grundlagen", "Architektur", "Datenmodell",
                                                 "Schnittstellen", "Architektur"])
        self.assertEqual(k[2].section_end, k[5].start, "Abschnitt endet vor der nächsten gleichrangigen Überschrift")
        self.assertEqual(k[3].parent, 2)
        self.assertEqual(k[0].section_end, len(doc["text"]))
        self.assertEqual([c.key for c in k if c.title == "Architektur"], ["2:Architektur#1", "2:Architektur#2"])
        baum = chapters.tree(k)
        self.assertEqual(len(baum), 1)
        self.assertEqual([kind[0].title for kind in baum[0][1]], ["Grundlagen", "Architektur", "Architektur"])
        self.assertEqual(chapters.current(k, doc["text"].index("B **")).title, "Datenmodell")

    def test_aufklapp_praefix_und_leere_ueberschrift(self):
        doc = dokument([(2, "▾ Offen"), (2, "   ")])
        self.assertEqual([c.title for c in chapters.outline(doc)], ["Offen"])


class Aenderungen(unittest.TestCase):
    def test_umbenennen_verschiebt_folgende_bereiche(self):
        doc = dokument(BEISPIEL)
        k = chapters.outline(doc)
        neu = chapters.rename(doc, k[1], "Basis und Ziele")
        self.assertEqual(chapters.outline(neu)[1].title, "Basis und Ziele")
        self.assertEqual([c.title for c in chapters.outline(neu)][2:], ["Architektur", "Datenmodell", "Schnittstellen", "Architektur"])
        self.assertEqual(chapters.validate(neu), [])
        with self.assertRaises(ValueError):
            chapters.rename(doc, k[1], "  ")

    def test_aufloesen_behaelt_text(self):
        doc = dokument(BEISPIEL)
        k = chapters.outline(doc)
        neu = chapters.dissolve(doc, k[3])
        self.assertEqual(neu["text"], doc["text"])
        self.assertNotIn("Datenmodell", [c.title for c in chapters.outline(neu)])

    def test_ebene_aendern(self):
        doc = dokument(BEISPIEL)
        neu = chapters.set_level(doc, chapters.outline(doc)[3], 2)
        self.assertEqual(chapters.outline(neu)[3].level, 2)
        self.assertEqual(neu["text"], doc["text"])

    def test_abschnitt_mit_unterkapiteln_verschieben_und_zurueck(self):
        doc = dokument(BEISPIEL)
        k = chapters.outline(doc)
        hoch = chapters.move(doc, k, k[2], -1)
        titel = [c.title for c in chapters.outline(hoch)]
        self.assertEqual(titel, ["Projektentwicklung", "Architektur", "Datenmodell", "Schnittstellen", "Grundlagen", "Architektur"])
        self.assertEqual(sorted(hoch["text"].split("\n")), sorted(doc["text"].split("\n")), "kein Text verloren")
        self.assertEqual(chapters.validate(hoch), [])
        zurueck = chapters.move(hoch, chapters.outline(hoch), chapters.outline(hoch)[1], +1)
        self.assertEqual(zurueck["text"], doc["text"])
        self.assertEqual(sorted((s["tag"], s["start"], s["end"]) for s in zurueck["spans"]),
                         sorted((s["tag"], s["start"], s["end"]) for s in doc["spans"]))

    def test_letzter_abschnitt_ohne_zeilenende_und_grenzen(self):
        doc = dokument(BEISPIEL)
        k = chapters.outline(doc)
        runter = chapters.move(doc, k, k[2], +1)
        self.assertTrue(runter["text"].endswith("Schnittstellen\nC"))
        self.assertFalse(runter["text"].endswith("\n"))
        self.assertIsNone(chapters.move(doc, k, k[0], -1), "kein Geschwister")
        self.assertIsNone(chapters.move(doc, k, k[3], -1), "Unterkapitel bleiben im Elternkapitel")

    def test_bereiche_wandern_mit_ihrem_abschnitt(self):
        doc = dokument(BEISPIEL)
        start = doc["text"].index("fett")
        doc["spans"].append({"tag": "bold", "start": start, "end": start + 4})
        k = chapters.outline(doc)
        neu = chapters.move(doc, k, k[2], -1)
        fett = next(s for s in neu["spans"] if s["tag"] == "bold")
        self.assertEqual(neu["text"][fett["start"]:fett["end"]], "fett")


if __name__ == "__main__":
    unittest.main()
