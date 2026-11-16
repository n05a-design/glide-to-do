#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Zentrale Prüfung von KI-Ausgaben (`ki_ausgabe.py`) ohne Tk-Fenster: erkennt sie, was Glide anders zeigt?

Die Oberflächenstufe mit Speichern, Neustart und Anzeige prüft die Integrationssuite
`test_ki_ausgabe_darstellung.py` in der Vollprüfung. Nur künstliche Daten.
"""
from __future__ import annotations

import contextlib
import importlib.machinery
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

WERKZEUGE = Path(__file__).resolve().parent
ROOT = WERKZEUGE.parents[1]
BEISPIELE = ROOT / "skills" / "glide-to-do" / "assets" / "beispiele"

FEHLERHAFT = {
    "format": "glide.exchange", "format_version": 2, "mode": "create",
    "labels": [{"key": "l1", "name": "Team", "color": "accent"}],
    "folders": [{"key": "f2", "title": "Kind", "parent": "f1"}, {"key": "f1", "title": "Eltern", "labels": ["l1"]}],
    "lists": [{"key": "a", "title": "Planung für das große Sommerfest im Garten", "folder": "f1", "labels": ["l1"],
               "items": [
                   {"type": "task", "title": "Getränke", "due": "27.11.2026", "estimated_minutes": "60",
                    "repeat": "weekly", "farbe": "rot"},
                   {"type": "heading", "title": "Abschnitt", "due": "2026-11-27"},
                   {"type": "task", "title": "Uhrzeit allein", "due_time": "09:00", "labels": ["l1", "Neu"]},
                   {"type": "aufgabe", "title": "Falsche Art"},
                   {"description": "ohne Titel"},
               ]}],
}


def lade(name, pfad):
    loader = importlib.machinery.SourceFileLoader(name, str(pfad))
    modul = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = modul
    loader.exec_module(modul)
    return modul


class KiAusgabeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._daten = tempfile.TemporaryDirectory(prefix="glide-ki-ausgabe-test-")
        cls._umgebung = {name: os.environ.get(name) for name in ("GLIDE_DATA_DIR", "GLIDE_TEST_MODE")}
        os.environ.update(GLIDE_DATA_DIR=cls._daten.name, GLIDE_TEST_MODE="1")
        sys.path.insert(0, str(ROOT / "src" / "glide"))
        cls.app = lade("glide_ki_ausgabe_test_app", ROOT / "src" / "glide" / "app.pyw")
        cls.ki = lade("glide_ki_ausgabe_test_werkzeug", WERKZEUGE / "ki_ausgabe.py")

    @classmethod
    def tearDownClass(cls):
        for name, wert in cls._umgebung.items():
            if wert is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = wert
        cls._daten.cleanup()

    def pruefe(self, *pfade, **optionen):
        with contextlib.redirect_stdout(io.StringIO()):
            return self.ki.pruefe_fensterlos(self.app, [str(p) for p in pfade], **optionen)

    def test_beispiele_des_skills_bestehen(self):
        namen = ("einkaufsliste.glideexchange", "projekt.glideexchange", "notiz.glideexchange",
                 "zeichnung.glideexchange", "recherchebericht.md")
        for ergebnis in self.pruefe(*(BEISPIELE / n for n in namen)):
            with self.subTest(datei=Path(ergebnis.datei).name):
                self.assertTrue(ergebnis.bestanden, self.ki.bericht_text([ergebnis]))
        vorschlag = self.pruefe(BEISPIELE / "aenderungsvorschlag.glideexchange",
                                kontext_paket=json.loads((BEISPIELE / "kontextpaket.glidecontext").read_text("utf-8")))
        self.assertTrue(vorschlag[0].bestanden)
        self.assertTrue(vorschlag[0].arten(self.ki.HINWEIS))

    def test_fehlerhafte_ausgabe_wird_feld_fuer_feld_erkannt(self):
        with tempfile.TemporaryDirectory() as ordner:
            datei = Path(ordner) / "ki.glideexchange"
            datei.write_text(json.dumps(FEHLERHAFT, ensure_ascii=False), encoding="utf-8")
            ergebnis = self.pruefe(datei)[0]
        self.assertFalse(ergebnis.bestanden)
        abweichungen = " | ".join(b.text for b in ergebnis.arten(self.ki.ABWEICHUNG))
        for erwartet in ("liegt auf oberster Ebene", "Titel auf 40 Zeichen gekürzt", "Punkte ohne Titel",
                         "due: Datei '27.11.2026', Glide None", "estimated_minutes: Datei '60'",
                         "an einer Gliederung (heading)", "Uhrzeit ohne Fälligkeitsdatum",
                         "Punktart „aufgabe“ unbekannt", "Angabe „farbe“ kennt Glide nicht"):
            self.assertIn(erwartet, abweichungen)
        grenzen = " | ".join(b.text for b in ergebnis.arten(self.ki.GRENZE))
        for erwartet in ("„repeat“ übernimmt Glide noch nicht (Paket K3", "„color“", "„labels“"):
            self.assertIn(erwartet, grenzen)
        # Grenzen stammen aus der Abdeckung des Skills, nicht aus einer zweiten Liste.
        offen = self.ki.grenzen()
        self.assertIn("repeat", offen["punkt"])
        self.assertEqual(offen["liste"]["labels"][0], "K2")

    def test_zeichnung_und_seite_werden_inhaltlich_verglichen(self):
        nutzlast = json.loads((BEISPIELE / "zeichnung.glideexchange").read_text("utf-8"))
        app = self.ki.fensterloses_glide(self.app)
        listen = app.apply_exchange_payload(app.parse_exchange_document(json.dumps(nutzlast))[0])
        listen[0]["drawing"] = dict(listen[0]["drawing"], rows=["00" * 16] * 16)
        ergebnis = self.ki.Ergebnis("zeichnung")
        self.ki.vergleiche_austausch(app, ergebnis, nutzlast, listen, app.folders)
        self.assertIn("Zeichnung weicht ab", " ".join(b.text for b in ergebnis.befunde))

        import page_markdown
        markdown = (BEISPIELE / "recherchebericht.md").read_text("utf-8")
        titel, rumpf = self.ki.seitentitel(markdown)
        self.assertEqual(titel, "Recherche: Teamausflug im Frühjahr")
        dokument = page_markdown.markdown_to_page(rumpf)
        seite = {"title": titel, "list_kind": "page", "rich_note": dict(dokument, text=dokument["text"] + "x"),
                 "items": [{"text": a["text"], "done": not a["done"]} for a in dokument["tasks"]]}
        ergebnis = self.ki.Ergebnis("seite")
        self.ki.vergleiche_seite(app, ergebnis, markdown, seite, page_markdown)
        texte = " | ".join(b.text for b in ergebnis.befunde)
        self.assertIn("Seitentext weicht", texte)
        self.assertIn("Erledigt-Zustand weicht ab", texte)
        self.assertEqual(self.ki.seitentitel("Ohne Überschrift\nText"), ("Ohne Überschrift", "Ohne Überschrift\nText"))

    def test_gleichwertig_vergleicht_formatierung_je_zeichen(self):
        text = "Eins\nZwei\nDrei"
        zerlegt = {"text": text, "links": {}, "spans": [{"tag": "bullet", "start": 0, "end": 4},
                                                         {"tag": "bullet", "start": 5, "end": 9}]}
        zusammen = {"text": text, "links": {}, "spans": [{"tag": "bullet", "start": 0, "end": 10}]}
        anders = {"text": text, "links": {}, "spans": [{"tag": "quote", "start": 0, "end": 10}]}
        self.assertTrue(self.ki.gleichwertig({"id": 1, "rich_note": zerlegt}, {"id": 1, "rich_note": zusammen}))
        self.assertFalse(self.ki.gleichwertig({"id": 1, "rich_note": zerlegt}, {"id": 1, "rich_note": anders}))
        self.assertFalse(self.ki.gleichwertig({"id": 1, "rich_note": zerlegt}, {"id": 2, "rich_note": zerlegt}))

    def test_kommandozeile_meldet_und_schreibt_bericht(self):
        with tempfile.TemporaryDirectory() as ordner:
            datei = Path(ordner) / "ki.glideexchange"
            datei.write_text(json.dumps(FEHLERHAFT, ensure_ascii=False), encoding="utf-8")
            bericht = Path(ordner) / "bericht.json"
            with contextlib.redirect_stdout(io.StringIO()) as ausgabe:
                self.assertEqual(self.ki.main([str(BEISPIELE / "einkaufsliste.glideexchange")]), 0)
                self.assertEqual(self.ki.main([str(datei), "--json", str(bericht)]), 1)
            self.assertIn("nicht bestanden", ausgabe.getvalue())
            daten = json.loads(bericht.read_text("utf-8"))
            self.assertFalse(daten[0]["bestanden"])
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(self.ki.main([str(datei), "--json", str(bericht)]), 1)
            self.assertEqual(json.loads(bericht.read_text("utf-8")), daten)

    def test_eigener_datenordner_statt_nutzerbestand(self):
        vorher = os.environ.get("GLIDE_DATA_DIR")
        try:
            with tempfile.TemporaryDirectory() as fremd:
                os.environ["GLIDE_DATA_DIR"] = fremd
                _, ordner = self.ki.glide_laden()
                self.assertNotEqual(Path(ordner).resolve(), Path(fremd).resolve())
                self.assertEqual(os.environ["GLIDE_DATA_DIR"], ordner)
                os.rmdir(ordner)
        finally:
            os.environ["GLIDE_DATA_DIR"] = vorher


if __name__ == "__main__":
    unittest.main()
