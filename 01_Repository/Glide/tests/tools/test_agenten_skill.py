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
        cls.zentral = lade("glide_agenten_skill_ki_ausgabe", Path(__file__).resolve().parent / "ki_ausgabe.py")
        cls.abdeckung = json.loads((SKILL / "abdeckung.json").read_text(encoding="utf-8"))
        import exchange_patch
        import page_markdown
        import drawing
        import animation
        cls.patch, cls.markdown, cls.drawing, cls.animation = exchange_patch, page_markdown, drawing, animation

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
        beispiele = skill.split("## Beispiele", 1)[1]
        if "\n## " in beispiele:
            beispiele = beispiele.split("\n## ", 1)[0]
        genannt = set(re.findall(r"`([\w-]+\.(?:glideexchange|glidecontext|json|md))`", beispiele))
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
        self.assertEqual(set(hilfe.LABEL_COLORS), set(glide.LABEL_COLOR_KEYS))
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

    def test_beispiele_bestehen_die_zentrale_pruefung(self):
        """Dieselbe Prüfung wie `ki_ausgabe.py`: jede Angabe kommt unverändert in Glide an."""
        dateien = [str(BEISPIELE / name) for name in (*CREATE_BEISPIELE, "recherchebericht.md")]
        with contextlib.redirect_stdout(io.StringIO()):
            ergebnisse = self.zentral.pruefe_fensterlos(self.app, dateien)
        for ergebnis in ergebnisse:
            with self.subTest(beispiel=Path(ergebnis.datei).name):
                self.assertTrue(ergebnis.bestanden, self.zentral.bericht_text([ergebnis]))
                self.assertEqual(ergebnis.arten(self.zentral.GRENZE), [])
        gesamt = {Path(e.datei).name: e.angelegt for e in ergebnisse}
        self.assertEqual(gesamt["projekt.glideexchange"], {"ordner": 2, "listen": 3, "punkte": 12})
        self.assertEqual(gesamt["recherchebericht.md"], {"seiten": 1, "punkte": 4})

    # ------------------------------------------------------------------
    # Kopplung an das Datenformat: Ändert sich der Datensatz, muss der Skill mit.
    # ------------------------------------------------------------------
    def datenfelder(self) -> dict:
        """Felder, die Glide tatsächlich speichert: Konstruktoren plus Referenzbestand des Formats."""
        glide = self.app.ListApp
        app = self.kopfloses_glide()
        felder = {"punkt": set(app.new_item("Probe", references=[])),
                  "liste": set(), "ordner": set(app.new_folder_object("Probe")),
                  "label": set(app.new_label_object("Probe", None, glide.LABEL_COLOR_KEYS[0]))}
        for art in glide.LIST_KINDS:
            felder["liste"] |= set(app.new_list_object("Probe", list_kind=art, references=[]))
        felder["liste"] |= set(app.new_list_object("Probe", recurring_checklist=True))
        felder["liste"] |= set(app.new_list_object("Probe", list_kind=glide.LIST_KIND_PAGE, live_lists=[]))
        format_nr = glide.DATA_SCHEMA_VERSION
        referenz = ROOT / "tests" / "fixtures" / f"current_v{format_nr}" / f"reference_v{format_nr}.json"
        self.assertTrue(referenz.is_file(), f"Datenformat {format_nr} ohne Referenzbestand {referenz.name}")
        bestand = json.loads(referenz.read_text(encoding="utf-8"))

        def punkte(liste):
            for punkt in liste or []:
                felder["punkt"].update(punkt)
                punkte(punkt.get("children"))

        for liste in bestand.get("lists") or []:
            felder["liste"].update(liste)
            punkte(liste.get("items"))
        for ordner in bestand.get("folders") or []:
            felder["ordner"].update(ordner)
        for label in bestand.get("labels") or []:
            felder["label"].update(label)
        return felder

    def austauschfelder(self) -> dict:
        glide = self.app.ListApp
        return {"punkt": glide.EXCHANGE_ITEM_FIELDS, "liste": glide.EXCHANGE_LIST_FIELDS,
                "ordner": glide.EXCHANGE_FOLDER_FIELDS, "label": glide.EXCHANGE_LABEL_FIELDS}

    def test_abdeckung_folgt_dem_datenformat(self):
        glide, abdeckung = self.app.ListApp, self.abdeckung
        hinweis = ("Skill glide-to-do nachziehen: abdeckung.json, Referenzen, Hilfsskript und Beispiele "
                   "(Pflegematrix, Zeile Agenten-Skill)")
        self.assertEqual(abdeckung["datenformat"], glide.DATA_SCHEMA_VERSION, "Datenformat geändert. " + hinweis)
        self.assertEqual(abdeckung["austauschformat"], glide.EXCHANGE_FORMAT_VERSION, "Austauschformat geändert. " + hinweis)
        self.assertEqual(abdeckung["faehigkeiten"], sorted(glide.exchange_capabilities()),
                         "Fähigkeiten des Austauschformats geändert. " + hinweis)
        self.assertEqual(set(abdeckung["listenarten"]), set(glide.LIST_KINDS), "Listenarten geändert. " + hinweis)
        self.assertEqual(set(abdeckung["ordnerarten"]), set(glide.FOLDER_KINDS), "Ordnerarten geändert. " + hinweis)
        self.assertEqual(set(abdeckung["punktarten"]), set(glide.ITEM_KINDS), "Punktarten geändert. " + hinweis)
        self.assertEqual(set(abdeckung["punktarten"]), set(glide.EXCHANGE_ITEM_TYPES))
        for art, felder in self.datenfelder().items():
            with self.subTest(objektart=art):
                eingetragen = set(abdeckung["felder"][art])
                self.assertEqual(sorted(felder - eingetragen), [], f"Neue Datenfelder ({art}). " + hinweis)
                self.assertEqual(sorted(eingetragen - felder), [], f"Entfallene Datenfelder ({art}). " + hinweis)
        self.assertEqual(abdeckung["glide_version"], self.hilfe.GLIDE_VERSION)

    def test_abdeckung_stimmt_mit_dem_austauschweg(self):
        """„ja“ kommt nachweislich an; „offen“ kommt nachweislich noch nicht an."""
        app = self.kopfloses_glide()
        drawing = self.drawing.DrawingModel.blank(16).to_document()
        folge = self.animation.Animation.from_legacy(drawing)
        folge.duplicate("frame-1", new_identity="zweites")
        bild = self.animation.entry_fields(folge)
        proben = {  # Austauschfeld → Probewert; das Ergebnis muss vom leeren Objekt abweichen
            "punkt": {"title": "Probe", "type": "long", "description": "Text", "done": True, "importance": 2,
                      "due": "2026-12-01", "due_time": "09:30", "planned_date": "2026-11-30",
                      "estimated_minutes": 45, "labels": ["Probe-Label"],
                      "checklist": [{"text": "Schritt", "done": False}], "children": [{"title": "Kind"}]},
            "liste": {"title": "Probeliste", "description": "Wozu", "folder": "o1", "list_kind": "note",
                      "items": [{"title": "Eins"}], "rich_note": {"text": "Notiz", "spans": [], "links": {}},
                      "labels": ["Probe-Label"]},
            "ordner": {"title": "Probeordner", "description": "Wozu", "parent": "o0", "labels": ["Probe-Label"]},
            "label": {"name": "Probe-Label", "color": "flag"},
        }
        nutzlast = {"format": "glide.exchange", "format_version": 2, "mode": "create",
                    "labels": [dict(proben["label"], key="Probe-Label")],
                    "folders": [{"key": "o0", "title": "Oben"}, dict(proben["ordner"], key="o1")],
                    "lists": [dict(proben["liste"], items=[proben["punkt"]]),
                              {"title": "Bild", "list_kind": "drawing", **bild}]}
        geprueft, bericht = app.parse_exchange_document(json.dumps(nutzlast))
        self.assertIsNotNone(geprueft, bericht.errors)
        listen = app.apply_exchange_payload(geprueft)
        objekte = {"punkt": listen[0]["items"][0], "liste": listen[0], "ordner": app.folders[-1],
                   "label": next(l for l in app.labels if l["name"] == "Probe-Label")}
        leer = {"punkt": app.new_item("Leer"), "liste": app.new_list_object("Leer"),
                "ordner": app.new_folder_object("Leer"), "label": app.new_label_object("Leer", None, None)}
        felder_im_austausch = self.austauschfelder()
        for art, felder in self.abdeckung["felder"].items():
            for name, eintrag in felder.items():
                with self.subTest(objektart=art, feld=name):
                    status, schluessel = eintrag["status"], eintrag.get("austausch")
                    self.assertIn(status, ("ja", "offen", "intern"))
                    if status == "intern":
                        self.assertNotIn("austausch", eintrag)
                        continue
                    if status == "offen":
                        self.assertRegex(eintrag.get("paket", ""), r"^K[1-6]$")
                    if (art, name) in (("liste", "drawing"), ("liste", "animation")):
                        self.assertEqual(listen[1][name], bild[name])
                        continue
                    angekommen = objekte[art].get(name) != leer[art].get(name)
                    if status == "ja":
                        self.assertIn(schluessel, felder_im_austausch[art])
                        self.assertIn(schluessel, proben[art], "Probewert für ein neues Austauschfeld ergänzen")
                        self.assertTrue(angekommen, f"{art}.{name} kommt über „{schluessel}“ nicht an")
                    elif schluessel in felder_im_austausch[art]:
                        self.assertFalse(angekommen, f"Glide übernimmt jetzt {art}.{name}: in abdeckung.json "
                                                     "auf „ja“ setzen und den Skill nachziehen")
                    else:
                        self.assertNotIn(schluessel, felder_im_austausch[art])

    def test_referenz_nennt_jedes_uebernommene_feld(self):
        referenz = (SKILL / "references" / "austauschformat.md").read_text(encoding="utf-8")
        for art, felder in self.abdeckung["felder"].items():
            for name, eintrag in felder.items():
                if eintrag["status"] == "ja" and art != "label":
                    with self.subTest(objektart=art, feld=name):
                        self.assertIn(f"`{eintrag['austausch']}`", referenz)

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
            "labels": [{"key": "l1", "name": "Team", "color": "neon"}],
            "folders": [{"key": "f2", "title": "Kind", "parent": "f1"}, {"key": "f1", "title": "Eltern"}],
            "lists": [
                {"key": "a", "title": "Liste", "folder": "f1", "labels": ["l1"], "items": [
                    {"type": "task", "title": "x" * 50, "due": "27.11.2026", "estimated_minutes": "60"},
                    {"type": "heading", "title": "Abschnitt", "due": "2026-11-27"},
                    {"type": "task", "title": "Uhrzeit", "due_time": "09:00", "repeat": "weekly"},
                ]},
                {"key": "b", "title": "Bild", "list_kind": "drawing", "animation": {"frames": []}, "items": [{"title": "nein"}]},
            ],
        }
        bericht = self.hilfe.Bericht("probe")
        self.hilfe.pruefe_create(bericht, schlecht)
        fehler, warnungen, hinweise = " | ".join(bericht.fehler), " | ".join(bericht.warnungen), " | ".join(bericht.hinweise)
        for erwartet in ("unbekanntes Feld „extra“", "kein Datum JJJJ-MM-TT", "estimated_minutes",
                         "unbekanntes Punktfeld „repeat“", "keine Punkte enthalten"):
            self.assertIn(erwartet, fehler)
        for erwartet in ("Titel hat 50 Zeichen", "kein weiter oben beschriebener Ordner",
                         "Farbe 'neon' unbekannt", "heading trägt keine due", "due_time ohne due"):
            self.assertIn(erwartet, warnungen)
        self.assertIn("Bildfolgen", hinweise)
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
