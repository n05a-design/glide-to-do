#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Agenten-Skill `glide-to-do` (WA-61, Paket K1): Standardkopf, Regelabgleich und echte Glide-Prüfung.

Der Skill erzeugt Importdateien für Glide. Bis der Austauschvertrag Tk-frei
vorliegt (Paket K2), bildet sein Hilfsskript die Glide-Prüfung von Hand nach.
Diese Prüfung hält beide zusammen: Feldmengen und Grenzen des Skripts müssen den
Glide-Konstanten entsprechen, und jedes Beispiel muss die echte Glide-Prüfung,
die echte Übernahme ohne Speichern und den echten Seitenimport bestehen.

Nur künstliche Daten. `GLIDE_DATA_DIR` zeigt vor dem App-Import auf einen
temporären Ordner; es entsteht kein Tk-Fenster, nichts wird gespeichert.
"""
from __future__ import annotations

import ast
import contextlib
import copy
import importlib.machinery
import importlib.util
import io
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "src" / "glide"
SKILL = ROOT / "skills" / "glide-to-do"
BEISPIELE = SKILL / "assets" / "beispiele"
CREATE_BEISPIELE = ("einkaufsliste.glideexchange", "projekt.glideexchange",
                    "notiz.glideexchange", "zeichnung.glideexchange")
KOPF_FELDER = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}

# Feste künstliche Aufgaben, aus denen das Beispiel-Kontextpaket entsteht.
BEISPIEL_LISTE = {"id": "beispiel-liste-planung", "title": "Planung",
                  "note": "Alles, was vor dem Umzugstag entschieden oder bestellt sein muss."}
BEISPIEL_AUFGABEN = [
    {"id": "beispiel-aufgabe-1", "text": "Angebote Umzugsfirma einholen",
     "description": "Drei Angebote mit Festpreis.", "importance": 2, "due": "2026-11-27",
     "planned_date": "2026-11-23", "estimated_minutes": 60, "labels": ["label-extern"]},
    {"id": "beispiel-aufgabe-2", "text": "Sitzplan festlegen", "importance": 1,
     "due": "2026-12-01", "estimated_minutes": 90},
]
BEISPIEL_LABELS = {"label-extern": "Extern"}


def lade(name: str, pfad: Path):
    loader = importlib.machinery.SourceFileLoader(name, str(pfad))
    modul = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = modul
    loader.exec_module(modul)
    return modul


def kopf(text: str) -> dict:
    """Kleiner Leser für den YAML-Kopf von SKILL.md: Schlüssel, Werte, `metadata`-Block."""
    teile = text.split("\n")
    if teile[0] != "---" or "---" not in teile[1:]:
        raise ValueError("SKILL.md beginnt nicht mit einem Kopf zwischen ---")
    ende = teile.index("---", 1)
    ergebnis, block = {}, None
    for zeile in teile[1:ende]:
        if not zeile.strip():
            continue
        eingerueckt = re.match(r"^  ([A-Za-z0-9_-]+):\s*(.*)$", zeile)
        if eingerueckt and block is not None:
            wert = eingerueckt.group(2).strip()
            if not (len(wert) >= 2 and wert[0] == wert[-1] == '"'):
                raise ValueError(f"metadata.{eingerueckt.group(1)} muss ein Text in Anführungszeichen sein")
            ergebnis[block][eingerueckt.group(1)] = wert[1:-1]
            continue
        oben = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", zeile)
        if not oben:
            raise ValueError(f"Kopfzeile nicht lesbar: {zeile!r}")
        schluessel, wert = oben.group(1), oben.group(2).strip()
        if schluessel in ergebnis:
            raise ValueError(f"Kopffeld {schluessel} doppelt")
        if wert:
            ergebnis[schluessel], block = wert, None
        else:
            ergebnis[schluessel], block = {}, schluessel
    return ergebnis


class AgentenSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._daten = tempfile.TemporaryDirectory(prefix="glide-agenten-skill-")
        cls._umgebung = {name: os.environ.get(name) for name in ("GLIDE_DATA_DIR", "GLIDE_TEST_MODE")}
        os.environ.update(GLIDE_DATA_DIR=cls._daten.name, GLIDE_TEST_MODE="1")
        sys.path.insert(0, str(SOURCE))
        cls.app = lade("glide_agenten_skill_app", SOURCE / "app.pyw")
        cls.hilfe = lade("glide_agenten_skill_hilfsskript", SKILL / "scripts" / "glide_datei.py")
        import exchange_patch
        import page_markdown
        import drawing
        cls.patch, cls.markdown, cls.drawing = exchange_patch, page_markdown, drawing

    @classmethod
    def tearDownClass(cls):
        for name, wert in cls._umgebung.items():
            if wert is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = wert
        cls._daten.cleanup()

    def kopfloses_glide(self):
        """`ListApp` ohne Fenster und ohne Speichern, mit leerem künstlichem Bestand."""
        app = self.app.ListApp.__new__(self.app.ListApp)
        app.labels, app.lists, app.folders, app.trash = [], [], [], []
        app.settings, app.undo_stack, app.dirty = {}, [], False
        app._data_read_only = False
        app.refresh_data_lock = lambda: True
        app.prepare_inspector_switch = lambda: True
        app.snapshot_undo = lambda trim=True: app.undo_stack.append("vorher")
        app.restore_import_checkpoint = lambda *args: self.fail("Import rollte zurück")
        app.trim_undo_stack = lambda: None
        app.finish_import_ui = lambda *args: None
        app.save_items = lambda: True
        return app

    @staticmethod
    def lies(name: str) -> str:
        return (BEISPIELE / name).read_text(encoding="utf-8")

    # ------------------------------------------------------------------
    def test_kopf_folgt_dem_skill_standard(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        werte = kopf(text)
        self.assertLessEqual(set(werte), KOPF_FELDER)
        self.assertEqual(werte["name"], SKILL.name)
        self.assertRegex(werte["name"], r"^[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertLessEqual(len(werte["name"]), 64)
        self.assertTrue(0 < len(werte["description"]) <= 1024, len(werte["description"]))
        self.assertLessEqual(len(werte.get("compatibility", "")), 500)
        self.assertEqual(werte["license"], "MPL-2.0")
        metadaten = werte["metadata"]
        self.assertRegex(metadaten["version"], r"^\d+\.\d+$")
        self.assertEqual(metadaten["glide-version"], self.hilfe.GLIDE_VERSION)
        self.assertEqual(metadaten["exchange-format"], str(self.app.ListApp.EXCHANGE_FORMAT_VERSION))
        geprueft = tuple(int(t) for t in self.hilfe.GLIDE_VERSION.split("."))
        aktuell = tuple(int(t) for t in (ROOT / "VERSION").read_text(encoding="utf-8").strip().split("."))
        self.assertLessEqual(geprueft, aktuell, "Skill nennt eine neuere Glide-Fassung als VERSION")
        self.assertLess(len(text.splitlines()), 500, "SKILL.md unter 500 Zeilen halten")

    def test_verweise_und_genannte_beispiele_existieren(self):
        for pfad in [SKILL / "SKILL.md", SKILL / "README.md", *sorted((SKILL / "references").glob("*.md"))]:
            # Codeblöcke und Codespannen zeigen Markdown-Beispiele, keine Verweise.
            text = re.sub(r"`[^`\n]*`", "", re.sub(r"```.*?```", "", pfad.read_text(encoding="utf-8"), flags=re.S))
            for ziel in re.findall(r"\]\(([^)\s]+)\)", text):
                if re.match(r"^[a-z]+:", ziel) or ziel.startswith("#"):
                    continue
                with self.subTest(datei=pfad.name, ziel=ziel):
                    self.assertTrue((pfad.parent / ziel.split("#", 1)[0]).exists())
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        genannt = set(re.findall(r"`([\w-]+\.(?:glideexchange|glidecontext|json|md))`",
                                 skill.split("## Beispiele", 1)[1]))
        self.assertEqual(genannt, {p.name for p in BEISPIELE.iterdir() if p.is_file()})

    def test_regeln_des_hilfsskripts_entsprechen_glide(self):
        glide, hilfe = self.app.ListApp, self.hilfe
        self.assertEqual(hilfe.FORMAT, glide.EXCHANGE_FORMAT_NAME)
        self.assertEqual(hilfe.FORMAT_VERSION, glide.EXCHANGE_FORMAT_VERSION)
        self.assertEqual(hilfe.SUFFIX, glide.EXCHANGE_SUFFIX)
        self.assertEqual(hilfe.ROOT_FIELDS, glide.EXCHANGE_ROOT_FIELDS)
        self.assertEqual(hilfe.LABEL_FIELDS, glide.EXCHANGE_LABEL_FIELDS)
        self.assertEqual(hilfe.FOLDER_FIELDS, glide.EXCHANGE_FOLDER_FIELDS)
        self.assertEqual(hilfe.LIST_FIELDS, glide.EXCHANGE_LIST_FIELDS)
        self.assertEqual(hilfe.ITEM_FIELDS, glide.EXCHANGE_ITEM_FIELDS)
        self.assertEqual(set(hilfe.ITEM_TYPES), set(glide.EXCHANGE_ITEM_TYPES))
        self.assertEqual(set(hilfe.LIST_KINDS), set(glide.LIST_KINDS))
        for ihr, unser in ((glide.MAX_EXCHANGE_BYTES, hilfe.MAX_BYTES), (glide.MAX_EXCHANGE_ITEMS, hilfe.MAX_ITEMS),
                           (glide.MAX_EXCHANGE_DEPTH, hilfe.MAX_DEPTH),
                           (glide.MAX_CHECKLIST_ENTRIES, hilfe.MAX_CHECKLIST_ENTRIES),
                           (glide.MAX_CHECKLIST_TEXT, hilfe.MAX_CHECKLIST_TEXT),
                           (glide.MAX_ESTIMATED_MINUTES, hilfe.MAX_ESTIMATED_MINUTES),
                           (glide.CONTAINER_TITLE_MAX, hilfe.TITLE_MAX),
                           (glide.MAX_LABEL_NAME_LENGTH, hilfe.MAX_LABEL_NAME),
                           (glide.MAX_LABELS, hilfe.MAX_LABELS),
                           (glide.MAX_LABELS_PER_ITEM, hilfe.MAX_LABELS_PER_ITEM)):
            self.assertEqual(ihr, unser)
        self.assertEqual(hilfe.CONTEXT_FORMAT, self.patch.CONTEXT_FORMAT)
        self.assertEqual(hilfe.PATCH_FIELDS, self.patch.FIELDS)
        self.assertEqual(hilfe.PATCH_MAX_CHANGES, self.patch.MAX_CHANGES)
        rich = self.app.RichNoteEditor
        self.assertEqual(hilfe.RICH_NOTE_FORMATS, rich.FORMATS)
        self.assertEqual((hilfe.RICH_NOTE_MAX_TEXT, hilfe.RICH_NOTE_MAX_SPANS), (rich.MAX_TEXT, rich.MAX_SPANS))
        zeichnung = self.drawing
        self.assertEqual(hilfe.DRAWING_FORMAT, zeichnung.FORMAT_NAME)
        self.assertEqual(hilfe.DRAWING_SIZES, zeichnung.SIZES)
        self.assertEqual(hilfe.DRAWING_BACKGROUND, zeichnung.BACKGROUND)
        self.assertEqual(hilfe.DRAWING_OPAQUE_WHITE, zeichnung.OPAQUE_WHITE)
        self.assertEqual(hilfe.DRAWING_MAX_COLORS, zeichnung.MAX_COLORS)
        self.assertEqual(hilfe.DRAWING_ENCODING, zeichnung.ENCODING)
        self.assertEqual(hilfe.DRAWING_COLOR_SPACE, zeichnung.COLOR_SPACE)
        self.assertEqual(hilfe.DRAWING_PALETTE_ID, zeichnung.DEFAULT_PALETTE_ID)
        self.assertEqual(set(hilfe.DRAWING_FIELDS), zeichnung._MODEL_FIELDS)

    def test_beispiele_bestehen_das_hilfsskript_streng(self):
        for name in (*CREATE_BEISPIELE, "recherchebericht.md"):
            with self.subTest(beispiel=name):
                bericht = self.hilfe.pruefe_datei(str(BEISPIELE / name))
                self.assertEqual((bericht.fehler, bericht.warnungen), ([], []))
        kontext = json.loads(self.lies("kontextpaket.glidecontext"))
        bericht = self.hilfe.pruefe_datei(str(BEISPIELE / "aenderungsvorschlag.glideexchange"), kontext)
        self.assertEqual((bericht.fehler, bericht.warnungen, bericht.hinweise), ([], [], []))

    def test_beispiele_bestehen_die_glide_pruefung(self):
        app = self.kopfloses_glide()
        for name in CREATE_BEISPIELE:
            with self.subTest(beispiel=name):
                nutzlast, bericht = app.parse_exchange_document(self.lies(name))
                self.assertIsNotNone(nutzlast, bericht.errors)
                self.assertEqual((bericht.errors, bericht.warnings, bericht.unknown_fields), ([], [], []))
        zeichnung = json.loads(self.lies("zeichnung.glideexchange"))["lists"][0]["drawing"]
        modell = self.drawing.DrawingModel.from_document(zeichnung)
        self.assertEqual(modell.to_document(), zeichnung)

    def test_beispiele_entstehen_in_glide_unverkuerzt(self):
        for name in CREATE_BEISPIELE:
            with self.subTest(beispiel=name):
                app = self.kopfloses_glide()
                nutzlast, bericht = app.parse_exchange_document(self.lies(name))
                listen = app.apply_exchange_payload(nutzlast)
                self.assertIsNotNone(listen)
                self.assertEqual(len(listen), len(nutzlast["lists"]))
                self.assertEqual(len(app.folders), len(nutzlast.get("folders") or []))
                quelle = {liste["title"]: liste for liste in nutzlast["lists"]}
                angelegt = 0
                for liste in listen:
                    vorlage = quelle[liste["title"]]
                    self.assertEqual(liste["list_kind"], vorlage.get("list_kind", "tasks"))
                    self.assertEqual(liste["note"], vorlage.get("description", ""))
                    angelegt += self.vergleiche_punkte(app, liste["items"], vorlage.get("items") or [])
                    if vorlage.get("rich_note"):
                        self.assertEqual(liste["rich_note"]["text"], vorlage["rich_note"]["text"])
                    if vorlage.get("drawing"):
                        self.assertEqual(liste["drawing"], vorlage["drawing"])
                self.assertEqual(angelegt, bericht.total_items)
                self.assertEqual(sorted(l["name"] for l in app.labels),
                                 sorted(l["name"] for l in nutzlast.get("labels") or []))
        projekt = self.kopfloses_glide()
        projekt.apply_exchange_payload(projekt.parse_exchange_document(self.lies("projekt.glideexchange"))[0])
        ordner = {o["title"]: o for o in projekt.folders}
        self.assertEqual(ordner["Unterlagen"]["parent_id"], ordner["Büroumzug"]["id"])

    def vergleiche_punkte(self, app, punkte, vorlagen) -> int:
        """Titel, Beschreibung und Planungsfelder kommen unverändert an; liefert die Punktzahl."""
        self.assertEqual(len(punkte), len(vorlagen))
        namen = {label["id"]: label["name"] for label in app.labels}
        schluessel = {}
        anzahl = 0
        for punkt, vorlage in zip(punkte, vorlagen):
            anzahl += 1
            self.assertEqual(punkt["text"], vorlage["title"], "Titel gekürzt")
            self.assertEqual(punkt["description"], vorlage.get("description", ""))
            self.assertEqual(punkt["kind"], app.EXCHANGE_ITEM_TYPES[vorlage.get("type", "task")])
            for feld in ("due", "due_time", "planned_date", "estimated_minutes"):
                self.assertEqual(punkt.get(feld), vorlage.get(feld), feld)
            self.assertEqual(punkt["importance"], vorlage.get("importance", 0))
            self.assertEqual(punkt["done"], vorlage.get("done", False))
            self.assertEqual([s["text"] for s in punkt["checklist"]],
                             [s["text"] for s in vorlage.get("checklist") or []])
            schluessel.update({k: k for k in vorlage.get("labels") or []})
            self.assertEqual(len(punkt["labels"]), len(vorlage.get("labels") or []))
            self.assertTrue(all(kennung in namen for kennung in punkt["labels"]))
            anzahl += self.vergleiche_punkte(app, punkt["children"], vorlage.get("children") or [])
        return anzahl

    def test_markdown_beispiel_wird_eine_seite(self):
        text = self.lies("recherchebericht.md")
        erste = next(zeile for zeile in text.splitlines() if zeile.strip())
        self.assertEqual(erste, "# Recherche: Teamausflug im Frühjahr")
        rumpf = text.split(erste, 1)[1]
        dokument = self.markdown.markdown_to_page(rumpf)
        self.assertEqual([(a["text"], a["done"]) for a in dokument["tasks"]],
                         [("Drei Terminvorschläge abstimmen", False), ("Angebot Kochschule anfragen", False),
                          ("Budget mit der Leitung klären", False), ("Ideen sammeln", True)])
        tags = {span["tag"] for span in dokument["spans"]}
        self.assertLessEqual({"h2", "h3", "table", "quote", "bullet", "bold", "italic", "task"}, tags)
        dokument.pop("tasks")
        self.app.RichNoteEditor.normalize(dokument)

    def test_zeichnung_entsteht_aus_der_eingabe(self):
        eingabe = json.loads(self.lies("zeichnung-eingabe.json"))
        self.assertEqual(self.hilfe.zeichnung_als_austausch(eingabe), json.loads(self.lies("zeichnung.glideexchange")))
        dokument = self.hilfe.baue_zeichnung(eingabe)
        modell = self.drawing.DrawingModel.from_document(dokument)
        self.assertEqual(modell.palette[0], self.drawing.BACKGROUND)
        self.assertIn(self.drawing.OPAQUE_WHITE, modell.palette)
        for groesse in self.drawing.SIZES:
            leer = {"size": groesse, "legend": {".": "#ffffff", "x": "#1e88e5"},
                    "pixels": ["x" + "." * (groesse - 1)] * groesse}
            self.assertEqual(self.drawing.DrawingModel.from_document(self.hilfe.baue_zeichnung(leer)).to_document(),
                             self.hilfe.baue_zeichnung(leer))
        with self.assertRaisesRegex(ValueError, "fehlt in legend"):
            self.hilfe.baue_zeichnung({"size": 16, "legend": {".": "#FFFFFF"}, "pixels": ["?" * 16] * 16})

    def test_kontextpaket_und_vorschlag_entsprechen_glide(self):
        kontext = self.patch.build_context([(BEISPIEL_LISTE, aufgabe, None) for aufgabe in BEISPIEL_AUFGABEN],
                                           BEISPIEL_LABELS, created_at="2026-11-16T10:00:00+01:00",
                                           application_version=self.hilfe.GLIDE_VERSION)
        self.assertEqual(json.loads(self.lies("kontextpaket.glidecontext")), kontext)
        vorschlag = json.loads(self.lies("aenderungsvorschlag.glideexchange"))
        aenderungen = self.patch.parse_patch(vorschlag)
        je_verweis = {self.patch.ref(a["id"]): (a, BEISPIEL_LABELS) for a in BEISPIEL_AUFGABEN}
        vorschau = self.patch.check_patch(aenderungen, je_verweis.get, BEISPIEL_LABELS.values())
        self.assertEqual([e["status"] for e in vorschau], ["ok"] * len(aenderungen), vorschau)

    def test_hilfsskript_meldet_typische_fehler(self):
        schlecht = {
            "format": "glide.exchange", "format_version": 2, "mode": "create", "extra": 1,
            "labels": [{"key": "l1", "name": "Team", "color": "accent"}],
            "folders": [{"key": "f2", "title": "Kind", "parent": "f1"}, {"key": "f1", "title": "Eltern"}],
            "lists": [
                {"key": "a", "title": "Liste", "folder": "f1", "labels": ["l1"], "items": [
                    {"type": "task", "title": "x" * 50, "due": "27.11.2026", "estimated_minutes": "60"},
                    {"type": "heading", "title": "Abschnitt", "due": "2026-11-27"},
                    {"type": "task", "title": "Uhrzeit", "due_time": "09:00", "repeat": "weekly"},
                ]},
                {"key": "b", "title": "Bild", "list_kind": "drawing", "items": [{"title": "nein"}]},
            ],
        }
        bericht = self.hilfe.Bericht("probe")
        self.hilfe.pruefe_create(bericht, schlecht)
        fehler, warnungen, hinweise = " | ".join(bericht.fehler), " | ".join(bericht.warnungen), " | ".join(bericht.hinweise)
        for erwartet in ("unbekanntes Feld „extra“", "kein Datum JJJJ-MM-TT", "estimated_minutes",
                         "unbekanntes Punktfeld „repeat“", "keine Punkte enthalten"):
            self.assertIn(erwartet, fehler)
        for erwartet in ("Titel hat 50 Zeichen", "kein weiter oben beschriebener Ordner",
                         "Labels an Listen", "heading trägt keine due", "due_time ohne due"):
            self.assertIn(erwartet, warnungen)
        self.assertIn("Labelfarbe", hinweise)
        # Dieselben Fälle weist auch Glide ab oder meldet sie.
        nutzlast, glide_bericht = self.kopfloses_glide().parse_exchange_document(json.dumps(schlecht))
        self.assertIsNone(nutzlast)
        self.assertIn("extra", glide_bericht.unknown_fields)

        kontext = json.loads(self.lies("kontextpaket.glidecontext"))
        vorschlag = json.loads(self.lies("aenderungsvorschlag.glideexchange"))
        vorschlag["changes"][0]["base"] = "0" * 16
        vorschlag["changes"][1]["set"] = {"title": "y" * 41, "importance": 7}
        bericht = self.hilfe.Bericht("vorschlag")
        self.hilfe.pruefe_patch(bericht, vorschlag, kontext)
        fehler = " | ".join(bericht.fehler)
        for erwartet in ("base passt nicht", "1 bis 40 Zeichen", "Wichtigkeit muss 0 bis 3"):
            self.assertIn(erwartet, fehler)

        with tempfile.TemporaryDirectory() as ordner:
            seite = Path(ordner) / "seite.md"
            seite.write_text("Ohne Überschrift\n\n![Logo](https://example.org/logo.png)\n\n<details>x</details>\n",
                             encoding="utf-8")
            bericht = self.hilfe.pruefe_datei(str(seite))
        warnungen = " | ".join(bericht.warnungen)
        for erwartet in ("mit „# Titel“ beginnen", "lädt nie aus dem Netz", "HTML"):
            self.assertIn(erwartet, warnungen)

    def test_kommandozeile_schreibt_nur_neue_dateien(self):
        with tempfile.TemporaryDirectory() as ordner:
            ziel = Path(ordner) / "tasse.glideexchange"
            argumente = ["zeichnung", str(BEISPIELE / "zeichnung-eingabe.json"), str(ziel)]
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(self.hilfe.main(argumente), 0)
            inhalt = ziel.read_bytes()
            with contextlib.redirect_stderr(io.StringIO()) as fehler:
                self.assertEqual(self.hilfe.main(argumente), 1)
            self.assertIn("nichts überschrieben", fehler.getvalue())
            self.assertEqual(ziel.read_bytes(), inhalt)
            with contextlib.redirect_stdout(io.StringIO()) as ausgabe:
                self.assertEqual(self.hilfe.main(["pruefen", str(ziel), "--streng"]), 0)
            self.assertIn("0 Fehler, 0 Warnungen", ausgabe.getvalue())

    def test_hilfsskript_braucht_nur_die_standardbibliothek(self):
        if not hasattr(sys, "stdlib_module_names"):
            self.skipTest("sys.stdlib_module_names erst ab Python 3.10")
        baum = ast.parse((SKILL / "scripts" / "glide_datei.py").read_text(encoding="utf-8"))
        module = set()
        for knoten in ast.walk(baum):
            if isinstance(knoten, ast.Import):
                module.update(alias.name.split(".")[0] for alias in knoten.names)
            elif isinstance(knoten, ast.ImportFrom) and knoten.module:
                module.add(knoten.module.split(".")[0])
        self.assertLessEqual(module - {"__future__"}, set(sys.stdlib_module_names))


if __name__ == "__main__":
    unittest.main()
