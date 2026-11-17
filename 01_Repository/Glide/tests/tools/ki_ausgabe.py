#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Zentrale Prüfung von KI-Ausgaben: Zeigt Glide, was die Datei beschreibt? (WA-61)

    python3 -B tests/tools/ki_ausgabe.py DATEI [DATEI …] [--kontext PAKET.glidecontext]
                                         [--oberflaeche] [--json BERICHT.json]

Für Dateien, die ein KI-Agent mit dem Skill `glide-to-do` oder auf anderem Weg
angelegt hat: `.glideexchange`/`.json` (neue Inhalte oder Änderungsvorschlag)
und `.md` (Seite). Je Datei vier Stufen:

1. Skill: das Hilfsskript des Skills (`skills/glide-to-do/scripts/glide_datei.py`).
2. Glide-Prüfung: `parse_exchange_document` bzw. die Prüfung des Änderungsvorschlags.
3. Übernahme mit dem echten Glide-Code in einem künstlichen Datenordner.
   Ohne Schalter fensterlos und ohne Speichern; mit `--oberflaeche` in einer
   echten Glide-Instanz, gespeichert und nach einem Neustart neu geladen.
4. Vergleich jeder Angabe der Datei mit dem angelegten Glide-Objekt; mit
   `--oberflaeche` zusätzlich mit der Anzeige: Zeilen der Liste, Text und
   Aufgabenkästchen der Seite oder Notiz, Zellen der Zeichnung.

Befunde: FEHLER (Datei unbrauchbar), ABWEICHUNG (Glide zeigt etwas anderes,
als die Datei beschreibt), GRENZE (bekannte Lücke laut `abdeckung.json` des
Skills), HINWEIS. Exitcode 1 bei FEHLER oder ABWEICHUNG.

Nie mit echten Nutzerdaten: Das Werkzeug legt immer einen eigenen temporären
Datenordner an und setzt `GLIDE_DATA_DIR`, bevor es Glide lädt.
Änderungsvorschläge lassen sich ohne den Bestand, aus dem ihr Kontextpaket
stammt, nur gegen das Paket prüfen; die Übernahme prüft Glide beim Nutzer.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.machinery
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SOURCE = REPO / "src" / "glide"
SKILL = REPO / "skills" / "glide-to-do"

FEHLER, ABWEICHUNG, GRENZE, HINWEIS = "FEHLER", "ABWEICHUNG", "GRENZE", "HINWEIS"
OBJEKTARTEN = ("punkt", "liste", "ordner", "label")


@dataclass
class Befund:
    art: str
    ort: str
    text: str


@dataclass
class Ergebnis:
    datei: str
    befunde: list = field(default_factory=list)
    angelegt: dict = field(default_factory=dict)

    def melden(self, art: str, ort: str, text: str) -> None:
        self.befunde.append(Befund(art, ort, text))

    @property
    def bestanden(self) -> bool:
        return not any(b.art in (FEHLER, ABWEICHUNG) for b in self.befunde)

    def arten(self, art: str) -> list:
        return [b for b in self.befunde if b.art == art]


# ----------------------------------------------------------------------
# Laden
# ----------------------------------------------------------------------
def lade_modul(name: str, pfad: Path):
    if name in sys.modules:
        return sys.modules[name]
    loader = importlib.machinery.SourceFileLoader(name, str(pfad))
    modul = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = modul
    loader.exec_module(modul)
    return modul


def hilfsskript():
    return lade_modul("glide_ki_ausgabe_hilfsskript", SKILL / "scripts" / "glide_datei.py")


def abdeckung() -> dict:
    return json.loads((SKILL / "abdeckung.json").read_text(encoding="utf-8"))


def grenzen(daten: dict | None = None) -> dict:
    """Je Objektart: Austauschname eines noch nicht übernommenen Felds → (Paket, Hinweis)."""
    daten = daten or abdeckung()
    ergebnis = {art: {} for art in OBJEKTARTEN}
    for art, felder in daten["felder"].items():
        for name, eintrag in felder.items():
            if eintrag.get("status") == "offen" and eintrag.get("austausch"):
                ergebnis[art][eintrag["austausch"]] = (eintrag.get("paket", "?"), eintrag.get("hinweis") or name)
    return ergebnis


def glide_laden():
    """Glide mit einem eigenen künstlichen Datenordner laden; nie den Nutzerbestand.

    Jeder Aufruf lädt `app.pyw` neu, weil Glide seine Ablagepfade beim Import festlegt.
    """
    ordner = tempfile.mkdtemp(prefix="glide-ki-ausgabe-")
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    if str(SOURCE) not in sys.path:
        sys.path.insert(0, str(SOURCE))
    name = f"glide_ki_ausgabe_app_{Path(ordner).name.replace('-', '_')}"
    return lade_modul(name, SOURCE / "app.pyw"), ordner


def fensterloses_glide(mod):
    """`ListApp` mit leerem Bestand, ohne Tk-Fenster und ohne Speichern."""
    app = mod.ListApp.__new__(mod.ListApp)
    app.labels, app.lists, app.folders, app.trash = [], [], [], []
    app.settings, app.undo_stack, app.dirty = {}, [], False
    app._data_read_only = False
    app.refresh_data_lock = lambda: True
    app.prepare_inspector_switch = lambda: True
    app.snapshot_undo = lambda trim=True: app.undo_stack.append(None)
    app.restore_import_checkpoint = lambda *args: None
    app.trim_undo_stack = lambda: None
    app.finish_import_ui = lambda *args: None
    app.save_items = lambda: True
    return app


# ----------------------------------------------------------------------
# Vergleich (ohne Tk)
# ----------------------------------------------------------------------
def _norm(text) -> str:
    return " ".join(str(text or "").split())


def _titel(ergebnis: Ergebnis, ort: str, erwartet: str, angezeigt: str, grenze: int) -> None:
    if angezeigt == erwartet:
        return
    if len(erwartet) > grenze and erwartet.startswith(angezeigt.rstrip("…").rstrip()):
        ergebnis.melden(ABWEICHUNG, ort, f"Titel auf {grenze} Zeichen gekürzt („{angezeigt}“); "
                                         "das Original steht in der Beschreibung")
    else:
        ergebnis.melden(ABWEICHUNG, ort, f"Titel „{angezeigt}“ statt „{erwartet}“")


def _unbekannt(ergebnis: Ergebnis, ort: str, quelle: dict, bekannte: set, offen: dict) -> None:
    for feld in quelle:
        if feld in offen:
            paket, hinweis = offen[feld]
            ergebnis.melden(GRENZE, ort, f"„{feld}“ übernimmt Glide noch nicht (Paket {paket}; {hinweis})")
        elif feld not in bekannte:
            ergebnis.melden(ABWEICHUNG, ort, f"Angabe „{feld}“ kennt Glide nicht; sie wird nicht übernommen")


def vergleiche_punkte(app, ergebnis: Ergebnis, ort: str, quellen, punkte, tiefe: int, kontext: dict) -> int:
    """Vergleicht Austauschpunkte mit den angelegten Punkten; liefert die Zahl verglichener Punkte."""
    gueltig = [q for q in quellen or [] if isinstance(q, dict) and _norm(q.get("title") or q.get("text"))]
    if len(gueltig) < len(quellen or []):
        ergebnis.melden(ABWEICHUNG, ort, f"{len(quellen) - len(gueltig)} Punkte ohne Titel oder ohne Objektform "
                                         "lässt Glide aus")
    if gueltig and tiefe >= app.MAX_EXCHANGE_DEPTH:
        ergebnis.melden(ABWEICHUNG, ort, f"{len(gueltig)} Unterpunkte jenseits von Ebene "
                                         f"{app.MAX_EXCHANGE_DEPTH} fehlen in Glide")
        return 0
    if len(gueltig) != len(punkte):
        ergebnis.melden(ABWEICHUNG, ort, f"{len(gueltig)} Punkte beschrieben, {len(punkte)} in Glide")
    anzahl = 0
    for quelle, punkt in zip(gueltig, punkte):
        anzahl += 1
        art_name = str(quelle.get("type") or "task")
        art = app.EXCHANGE_ITEM_TYPES.get(art_name, app.ITEM_KIND_TASK)
        roh = str(quelle.get("title") or quelle.get("text") or "").strip()
        erwartet = app.normalize_item_text(roh, art)
        hier = f"{ort} › „{erwartet[:30]}“"
        _titel(ergebnis, hier, erwartet, punkt["text"], app.CONTAINER_TITLE_MAX)
        if art_name not in app.EXCHANGE_ITEM_TYPES:
            ergebnis.melden(ABWEICHUNG, hier, f"Punktart „{art_name}“ unbekannt; Glide zeigt eine Aufgabe")
        if punkt["kind"] != art:
            ergebnis.melden(ABWEICHUNG, hier, f"Art „{punkt['kind']}“ statt „{art}“")
        if punkt["text"] == erwartet and str(quelle.get("description") or "") != punkt["description"]:
            ergebnis.melden(ABWEICHUNG, hier, "Beschreibung weicht ab")
        gliederung = art in (app.ITEM_KIND_GROUP, app.ITEM_KIND_HEADING)
        for feld in ("done", "importance", "due", "due_time", "planned_date", "estimated_minutes"):
            if feld not in quelle or quelle[feld] in (None, False, 0, ""):
                continue
            wert = punkt.get(feld)
            if gliederung:
                ergebnis.melden(ABWEICHUNG, hier, f"{feld} an einer Gliederung ({art_name}) verwirft Glide")
            elif feld == "due_time" and not punkt.get("due"):
                ergebnis.melden(ABWEICHUNG, hier, "Uhrzeit ohne Fälligkeitsdatum verwirft Glide")
            elif wert != quelle[feld]:
                ergebnis.melden(ABWEICHUNG, hier, f"{feld}: Datei {quelle[feld]!r}, Glide {wert!r}")
        erwartete_labels = {kontext["label_namen"].get(str(k), _norm(k)).casefold()
                            for k in quelle.get("labels") or [] if _norm(k)}
        eigene = {kontext["labels"][i]["name"].casefold() for i in punkt.get("labels") or []
                  if i in kontext["labels"] and not kontext["labels"][i].get("system")}
        if erwartete_labels != eigene:
            ergebnis.melden(ABWEICHUNG, hier, f"Labels {sorted(eigene)} statt {sorted(erwartete_labels)}")
        schritte = [s for s in quelle.get("checklist") or [] if isinstance(s, dict)]
        if not gliederung:
            soll = [(_norm(s.get("text")), bool(s.get("done"))) for s in schritte][:app.MAX_CHECKLIST_ENTRIES]
            ist = [(_norm(s.get("text")), bool(s.get("done"))) for s in punkt.get("checklist") or []]
            if len(schritte) > app.MAX_CHECKLIST_ENTRIES:
                ergebnis.melden(ABWEICHUNG, hier, f"nur {app.MAX_CHECKLIST_ENTRIES} von {len(schritte)} "
                                                  "Checklistenschritten übernommen")
            if soll != ist:
                ergebnis.melden(ABWEICHUNG, hier, "Checkliste weicht ab")
        elif schritte:
            ergebnis.melden(ABWEICHUNG, hier, "Checkliste an einer Gliederung verwirft Glide")
        _unbekannt(ergebnis, hier, quelle, app.EXCHANGE_ITEM_FIELDS, kontext["grenzen"]["punkt"])
        anzahl += vergleiche_punkte(app, ergebnis, hier, quelle.get("children"), punkt.get("children") or [],
                                    tiefe + 1, kontext)
    return anzahl


def vergleiche_austausch(app, ergebnis: Ergebnis, nutzlast: dict, listen: list, neue_ordner: list,
                         offen: dict | None = None) -> None:
    """Vergleicht eine Austauschdatei (mode „create“) mit dem, was Glide angelegt hat."""
    offen = offen or grenzen()
    labels = {l["id"]: l for l in app.labels}
    label_namen = {}
    for nummer, label in enumerate(nutzlast.get("labels") or [], 1):
        if not isinstance(label, dict) or not _norm(label.get("name")):
            continue
        if label.get("key"):
            label_namen[str(label["key"])] = _norm(label["name"])
        _unbekannt(ergebnis, f"Label „{_norm(label['name'])}“", label, app.EXCHANGE_LABEL_FIELDS, offen["label"])
        if "color" in label and label.get("color"):
            zugeordnet = next((l for l in app.labels if _norm(l.get("name") or "").casefold() == _norm(label["name"]).casefold()), None)
            if zugeordnet and label["color"] in app.LABEL_COLOR_KEYS and zugeordnet.get("color") != label["color"]:
                ergebnis.melden(ABWEICHUNG, f"Label „{_norm(label['name'])}“", f"Farbe {zugeordnet.get('color')!r} statt {label['color']!r}")
    kontext = {"labels": labels, "label_namen": label_namen, "grenzen": offen}

    ordner_quelle = [o for o in nutzlast.get("folders") or [] if isinstance(o, dict) and _norm(o.get("title"))]
    ordner_id = {}
    if len(ordner_quelle) != len(neue_ordner):
        ergebnis.melden(ABWEICHUNG, "Ordner", f"{len(ordner_quelle)} beschrieben, {len(neue_ordner)} angelegt")
    for quelle, ordner in zip(ordner_quelle, neue_ordner):
        ort = f"Ordner „{_norm(quelle['title'])}“"
        _titel(ergebnis, ort, _norm(quelle["title"]), ordner["title"], app.CONTAINER_TITLE_MAX)
        if ordner["title"] == _norm(quelle["title"]) and str(quelle.get("description") or "") != ordner.get("note", ""):
            ergebnis.melden(ABWEICHUNG, ort, "Beschreibung weicht ab")
        if "labels" in quelle:
            erwartete_labels = {kontext["label_namen"].get(str(k), _norm(k)).casefold()
                                for k in quelle.get("labels") or [] if _norm(k)}
            eigene = {kontext["labels"][i]["name"].casefold() for i in ordner.get("labels") or []
                      if i in kontext["labels"] and not kontext["labels"][i].get("system")}
            if erwartete_labels != eigene:
                ergebnis.melden(ABWEICHUNG, ort, f"Labels {sorted(eigene)} statt {sorted(erwartete_labels)}")
        eltern = quelle.get("parent")
        erwartet = ordner_id.get(str(eltern)) if eltern else None
        if eltern and erwartet is None:
            ergebnis.melden(ABWEICHUNG, ort, f"liegt auf oberster Ebene: Elternordner „{eltern}“ ist nicht "
                                             "weiter oben beschrieben")
        elif ordner.get("parent_id") != erwartet:
            ergebnis.melden(ABWEICHUNG, ort, "liegt in einem anderen Ordner als beschrieben")
        _unbekannt(ergebnis, ort, quelle, app.EXCHANGE_FOLDER_FIELDS, offen["ordner"])
        if quelle.get("key"):
            ordner_id[str(quelle["key"])] = ordner["id"]

    listen_quelle = [l for l in nutzlast.get("lists") or [] if isinstance(l, dict) and _norm(l.get("title"))]
    if len(listen_quelle) < len(nutzlast.get("lists") or []):
        ergebnis.melden(ABWEICHUNG, "Listen", "Listen ohne Titel lässt Glide samt Inhalt aus")
    if len(listen_quelle) != len(listen):
        ergebnis.melden(ABWEICHUNG, "Listen", f"{len(listen_quelle)} beschrieben, {len(listen)} angelegt")
    punkte = 0
    for quelle, liste in zip(listen_quelle, listen):
        titel = _norm(quelle["title"])
        ort = f"Liste „{titel}“"
        _titel(ergebnis, ort, titel, liste["title"], app.CONTAINER_TITLE_MAX)
        if liste["title"] == titel and str(quelle.get("description") or "") != liste.get("note", ""):
            ergebnis.melden(ABWEICHUNG, ort, "Beschreibung weicht ab")
        if "labels" in quelle:
            erwartete_labels = {kontext["label_namen"].get(str(k), _norm(k)).casefold()
                                for k in quelle.get("labels") or [] if _norm(k)}
            eigene = {kontext["labels"][i]["name"].casefold() for i in liste.get("labels") or []
                      if i in kontext["labels"] and not kontext["labels"][i].get("system")}
            if erwartete_labels != eigene:
                ergebnis.melden(ABWEICHUNG, ort, f"Labels {sorted(eigene)} statt {sorted(erwartete_labels)}")
        art = quelle.get("list_kind") or app.LIST_KIND_TASKS
        if liste["list_kind"] != art:
            ergebnis.melden(ABWEICHUNG, ort, f"Listenart „{liste['list_kind']}“ statt „{art}“")
        if quelle.get("folder"):
            erwartet = ordner_id.get(str(quelle["folder"]))
            if erwartet is None:
                ergebnis.melden(ABWEICHUNG, ort, f"Ordner „{quelle['folder']}“ ist nicht beschrieben; "
                                                 "die Liste liegt ohne Ordner")
            elif liste.get("folder_id") != erwartet:
                ergebnis.melden(ABWEICHUNG, ort, "liegt in einem anderen Ordner als beschrieben")
        _unbekannt(ergebnis, ort, quelle, app.EXCHANGE_LIST_FIELDS, offen["liste"])
        if isinstance(quelle.get("rich_note"), dict):
            soll = quelle["rich_note"]
            ist = liste.get("rich_note") or {}
            if str(soll.get("text") or "") != ist.get("text", ""):
                ergebnis.melden(ABWEICHUNG, ort, "Notiz- oder Seitentext weicht ab")
            if len(soll.get("spans") or []) != len(ist.get("spans") or []):
                ergebnis.melden(ABWEICHUNG, ort, f"{len(soll.get('spans') or [])} Formatbereiche beschrieben, "
                                                 f"{len(ist.get('spans') or [])} in Glide")
        if quelle.get("drawing") is not None and liste.get("drawing") != quelle["drawing"]:
            ergebnis.melden(ABWEICHUNG, ort, "Zeichnung weicht ab")
        punkte += vergleiche_punkte(app, ergebnis, ort, quelle.get("items"), liste.get("items") or [], 0, kontext)
    ergebnis.angelegt.update(ordner=len(neue_ordner), listen=len(listen), punkte=punkte)


def seitentitel(markdown: str) -> tuple[str, str]:
    """Titel und Rumpf wie „Seite aus Datei …“: erste Zeile, eine Überschrift entfällt im Text."""
    erste = next((zeile for zeile in markdown.splitlines() if zeile.strip()), "")
    stripped = erste.strip()
    if stripped.startswith("#") and stripped.lstrip("#")[:1] == " ":
        return stripped.lstrip("#").strip()[:120], markdown.split(erste, 1)[1]
    return stripped[:120], markdown


def vergleiche_seite(app, ergebnis: Ergebnis, markdown: str, seite: dict, page_markdown) -> None:
    """Vergleicht eine Markdown-Seite mit der angelegten Glide-Seite."""
    titel, rumpf = seitentitel(markdown)
    ort = f"Seite „{titel[:40]}“"
    _titel(ergebnis, ort, titel, seite["title"], app.CONTAINER_TITLE_MAX)
    if seite.get("list_kind") != app.LIST_KIND_PAGE:
        ergebnis.melden(ABWEICHUNG, ort, "ist keine Seite")
    erwartet = page_markdown.markdown_to_page(rumpf)
    aufgaben = [(_norm(a["text"]), bool(a["done"])) for a in erwartet["tasks"]]
    angelegt = [(_norm(i.get("text")), bool(i.get("done"))) for i in seite.get("items") or []]
    for (soll_text, soll_erledigt), (ist_text, ist_erledigt) in zip(aufgaben, angelegt):
        _titel(ergebnis, f"{ort} › Aufgabe", soll_text, ist_text, app.CONTAINER_TITLE_MAX)
        if soll_erledigt != ist_erledigt:
            ergebnis.melden(ABWEICHUNG, f"{ort} › „{soll_text[:30]}“", "Erledigt-Zustand weicht ab")
    if len(aufgaben) != len(angelegt):
        ergebnis.melden(ABWEICHUNG, ort, f"{len(aufgaben)} Aufgaben beschrieben, {len(angelegt)} in Glide")
    text = (seite.get("rich_note") or {}).get("text", "")
    if text != erwartet["text"]:
        ergebnis.melden(ABWEICHUNG, ort, "Seitentext weicht von der Markdown-Umwandlung ab")
    bilder_md = rumpf.count("![")
    bilder = len((seite.get("rich_note") or {}).get("images") or {})
    if bilder_md > bilder:
        ergebnis.melden(GRENZE, ort, f"{bilder_md - bilder} Bildverweise ohne lokale Datei bleiben Text")
    ergebnis.angelegt.update(seiten=1, punkte=len(angelegt))


def format_je_zeichen(dokument: dict) -> list:
    """Formatierung je Zeichen außer Zeilenumbrüchen.

    Der Seiteneditor fasst beim Speichern benachbarte gleiche Bereiche zusammen
    und nimmt den Zeilenumbruch in Zeilenformate auf; das ändert weder Text noch
    Darstellung. Verglichen wird deshalb, welche Formate jedes Zeichen trägt.
    """
    text = str((dokument or {}).get("text") or "")
    ereignisse = {}
    for span in (dokument or {}).get("spans") or []:
        ereignisse.setdefault(span["start"], []).append((1, span["tag"]))
        ereignisse.setdefault(span["end"], []).append((-1, span["tag"]))
    aktiv, ergebnis = {}, []
    for index, zeichen in enumerate(text):
        for richtung, tag in ereignisse.get(index, ()):
            aktiv[tag] = aktiv.get(tag, 0) + richtung
        if zeichen != "\n":
            ergebnis.append(frozenset(tag for tag, zahl in aktiv.items() if zahl > 0))
    return ergebnis


def gleichwertig(vorher: dict, nachher: dict) -> bool:
    """Gleicher Listenstand; Seitentext mit gleicher Formatierung je Zeichen."""
    a, b = dict(vorher), dict(nachher)
    notiz_a, notiz_b = a.pop("rich_note", None) or {}, b.pop("rich_note", None) or {}
    if a != b:
        return False
    if notiz_a.get("text", "") != notiz_b.get("text", "") or notiz_a.get("links") != notiz_b.get("links"):
        return False
    if notiz_a.get("images") != notiz_b.get("images"):
        return False
    return format_je_zeichen(notiz_a) == format_je_zeichen(notiz_b)


# ----------------------------------------------------------------------
# Anzeige (Tk)
# ----------------------------------------------------------------------
def _alle(punkte):
    for punkt in punkte or []:
        yield punkt
        yield from _alle(punkt.get("children"))


def ruhe(root, runden: int = 6) -> None:
    for _ in range(runden):
        root.update_idletasks()
        root.update()


def oeffnen(app, root, liste: dict) -> None:
    """Öffnet die Liste oder Seite in der echten Oberfläche."""
    app.set_active_list(liste["id"])
    ruhe(root)


def verfaelschen(app, liste: dict) -> bool:
    """Gegenprobe: verändert nur die Anzeige der geöffneten Liste, nicht den Bestand."""
    art = liste["list_kind"]
    if art in (app.LIST_KIND_NOTE, app.LIST_KIND_PAGE) and getattr(app, "rich_note_editor", None):
        app.rich_note_editor.text.insert("1.0", "Fremdtext ")
        return True
    if art == app.LIST_KIND_DRAWING and getattr(app, "drawing_editor", None):
        modell = app.drawing_editor.model
        modell.cells[0] = 1 if modell.cells[0] == 0 and len(modell.palette) > 1 else 0
        return True
    erster = next(_alle(liste.get("items")), None)
    if erster and app.tree.exists(erster["id"]):
        app.tree.delete(erster["id"])
        return True
    return False


def lies_anzeige(app, ergebnis: Ergebnis, liste: dict) -> None:
    """Liest ab, was Glide für die geöffnete Liste zeigt, und vergleicht mit dem Bestand."""
    ort = f"Anzeige „{liste['title']}“"
    art = liste["list_kind"]
    if art in (app.LIST_KIND_TASKS, app.LIST_KIND_NOTE):
        zeilen = set(app.iter_tree_ids())
        for punkt in _alle(liste.get("items")):
            if punkt["id"] not in zeilen:
                ergebnis.melden(ABWEICHUNG, ort, f"„{punkt['text'][:30]}“ erscheint nicht in der Liste")
                continue
            anzeige = str(app.tree.item(punkt["id"], "text"))
            kurz = app.item_display_text(punkt).split("\n", 1)[0][:30]
            if kurz and kurz not in anzeige:
                ergebnis.melden(ABWEICHUNG, ort, f"Zeile zeigt „{anzeige[:40]}“ statt „{kurz}“")
    if art in (app.LIST_KIND_NOTE, app.LIST_KIND_PAGE):
        editor = getattr(app, "rich_note_editor", None)
        if editor is None:
            ergebnis.melden(ABWEICHUNG, ort, "kein Texteditor sichtbar")
        else:
            gezeigt = editor.text.get("1.0", "end-1c")
            gespeichert = (liste.get("rich_note") or {}).get("text", "")
            if gezeigt.strip() != gespeichert.strip():
                ergebnis.melden(ABWEICHUNG, ort, "der Editor zeigt einen anderen Text als gespeichert")
            if art == app.LIST_KIND_PAGE and len(editor.task_boxes()) != len(liste.get("items") or []):
                ergebnis.melden(ABWEICHUNG, ort, f"{len(editor.task_boxes())} Aufgabenkästchen, "
                                                 f"{len(liste.get('items') or [])} Aufgaben")
    if art == app.LIST_KIND_DRAWING:
        editor = getattr(app, "drawing_editor", None)
        if editor is None or editor.model.to_document() != liste.get("drawing"):
            ergebnis.melden(ABWEICHUNG, ort, "die Zeichenfläche zeigt nicht die gespeicherte Zeichnung")


def _beenden(app, root) -> None:
    """Wie beim Schließen des Fensters: speichern und die Datensperre freigeben."""
    try:
        app.on_close()
    finally:
        with contextlib.suppress(Exception):
            root.destroy()


def _starten(mod):
    root = mod.tk.Tk()
    root.withdraw()
    root.geometry("1400x900+0+0")
    fehler = []
    root.report_callback_exception = lambda *args: fehler.append(args)
    app = mod.ListApp(root)
    meldungen = []
    app.show_warning = app.show_error = lambda *args, **kwargs: meldungen.append(args)
    app.show_info = lambda *args, **kwargs: None
    app.ask_yes_no = lambda *args, **kwargs: True
    return root, app, fehler, meldungen


# ----------------------------------------------------------------------
# Ablauf
# ----------------------------------------------------------------------
def _lies(pfad: Path) -> str:
    return pfad.read_text(encoding="utf-8-sig")


def _stufen_1_2(mod, app, pfad: Path, ergebnis: Ergebnis, kontext_paket):
    """Skill- und Glide-Prüfung; liefert (Art, Nutzlast oder Markdown) oder None."""
    hilfe = hilfsskript()
    bericht = hilfe.pruefe_datei(str(pfad), kontext_paket)
    for text in bericht.fehler:
        ergebnis.melden(FEHLER, "Skill", text)
    for text in bericht.warnungen:
        ergebnis.melden(HINWEIS, "Skill", text)
    text = _lies(pfad)
    if pfad.suffix.lower() in (".md", ".markdown", ".txt"):
        return "seite", text
    try:
        roh = json.loads(text)
    except ValueError:
        return None
    if isinstance(roh, dict) and roh.get("mode") == "patch":
        import exchange_patch
        try:
            exchange_patch.parse_patch(roh)
        except exchange_patch.PatchError as fehler:
            ergebnis.melden(FEHLER, "Glide", str(fehler))
            return None
        ergebnis.melden(HINWEIS, "Glide", "Änderungsvorschlag: Glide prüft ihn beim Import gegen den eigenen "
                                          "Bestand; hier nur gegen das Kontextpaket" if kontext_paket else
                        "Änderungsvorschlag: ohne --kontext nur die Form geprüft")
        return "patch", roh
    nutzlast, glide_bericht = app.parse_exchange_document(text)
    for meldung in glide_bericht.errors:
        ergebnis.melden(FEHLER, "Glide", meldung)
    for meldung in glide_bericht.warnings:
        # Folgen dieser Hinweise erfasst der Feldvergleich als ABWEICHUNG.
        ergebnis.melden(HINWEIS, "Glide-Vorschau", meldung)
    if nutzlast is None:
        return None
    return "austausch", nutzlast


def pruefe_fensterlos(mod, pfade, kontext_paket=None) -> list:
    """Stufen 1–4 mit dem echten Glide-Code, ohne Fenster und ohne Speichern."""
    import page_markdown
    ergebnisse = []
    for pfad in map(Path, pfade):
        ergebnis = Ergebnis(str(pfad))
        ergebnisse.append(ergebnis)
        app = fensterloses_glide(mod)
        stufe = _stufen_1_2(mod, app, pfad, ergebnis, kontext_paket)
        if stufe is None or stufe[0] == "patch":
            continue
        art, inhalt = stufe
        if art == "seite":
            titel, rumpf = seitentitel(inhalt)
            seite = app.new_list_object(titel or "Neue Seite", [], list_kind=app.LIST_KIND_PAGE)
            dokument = page_markdown.markdown_to_page(rumpf)
            seite["items"] = [app.new_item(a["text"], done=a["done"]) for a in dokument.pop("tasks")]
            seite["rich_note"] = dokument
            vergleiche_seite(app, ergebnis, inhalt, seite, page_markdown)
            continue
        vorher = len(app.folders)
        listen = app.apply_exchange_payload(inhalt)
        if not listen:
            ergebnis.melden(FEHLER, "Übernahme", "Glide hat nichts angelegt")
            continue
        vergleiche_austausch(app, ergebnis, inhalt, listen, app.folders[vorher:])
    return ergebnisse


def pruefe_mit_oberflaeche(mod, pfade, kontext_paket=None, gegenprobe=False) -> list:
    """Stufen 1–4 in einer echten Glide-Instanz: anlegen, speichern, neu starten, Anzeige ablesen.

    Mit `gegenprobe` verfälscht der zweite Prozess danach die Anzeige jeder Liste
    und verlangt, dass die Ablesung das bemerkt.
    """
    import page_markdown
    ergebnisse = []
    angelegt = []  # (Ergebnis, Listen-ID)
    root, app, fehler, meldungen = _starten(mod)
    try:
        for pfad in map(Path, pfade):
            ergebnis = Ergebnis(str(pfad))
            ergebnisse.append(ergebnis)
            stufe = _stufen_1_2(mod, app, pfad, ergebnis, kontext_paket)
            if stufe is None or stufe[0] == "patch":
                continue
            art, inhalt = stufe
            if art == "seite":
                seite = app.new_page_from_markdown(inhalt, base_dir=str(pfad.parent))
                ruhe(root)
                if seite is None:
                    ergebnis.melden(FEHLER, "Übernahme", "Glide hat keine Seite angelegt")
                    continue
                vergleiche_seite(app, ergebnis, inhalt, seite, page_markdown)
                angelegt.append((ergebnis, seite["id"]))
                continue
            vorher = len(app.folders)
            listen = app.apply_exchange_payload(inhalt)
            ruhe(root)
            if not listen:
                ergebnis.melden(FEHLER, "Übernahme", "Glide hat nichts angelegt oder nicht gespeichert")
                continue
            vergleiche_austausch(app, ergebnis, inhalt, listen, app.folders[vorher:])
            angelegt.extend((ergebnis, liste["id"]) for liste in listen)
        stand = {"gegenprobe": gegenprobe, "listen": [
            {"ergebnis": ergebnisse.index(ergebnis),
             "liste": json.loads(json.dumps(next(l for l in app.lists if l["id"] == kennung)))}
            for ergebnis, kennung in angelegt]}
        for ergebnis in ergebnisse:
            for meldung in meldungen:
                ergebnis.melden(HINWEIS, "Glide-Meldung", " ".join(str(teil) for teil in meldung)[:200])
            if fehler:
                ergebnis.melden(ABWEICHUNG, "Oberfläche", f"{len(fehler)} Fehler in Rückrufen beim Anlegen")
    finally:
        _beenden(app, root)
    if not angelegt:
        return ergebnisse
    # Neustart wie beim Nutzer: ein neuer Prozess liest denselben Datenordner.
    ordner = Path(os.environ["GLIDE_DATA_DIR"])
    stand_pfad = ordner / "ki_ausgabe_stand.json"
    stand_pfad.write_text(json.dumps(stand, ensure_ascii=False), encoding="utf-8")
    lauf = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()), "--anzeige", str(stand_pfad)],
                          env={**os.environ, "GLIDE_DATA_DIR": str(ordner), "GLIDE_TEST_MODE": "1"},
                          capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
    rueckmeldung = ordner / "ki_ausgabe_anzeige.json"
    if lauf.returncode != 0 or not rueckmeldung.is_file():
        for ergebnis in ergebnisse:
            ergebnis.melden(FEHLER, "Neustart", "Anzeigeprüfung im neuen Prozess gescheitert: "
                            + (lauf.stdout + lauf.stderr).strip()[-400:])
        return ergebnisse
    for eintrag in json.loads(rueckmeldung.read_text(encoding="utf-8")):
        ergebnis = ergebnisse[eintrag["ergebnis"]]
        for befund in eintrag["befunde"]:
            ergebnis.melden(befund["art"], befund["ort"], befund["text"])
        if gegenprobe and not eintrag.get("gegenprobe_erkannt"):
            ergebnis.melden(FEHLER, "Gegenprobe", f"verfälschte Anzeige von „{eintrag['titel']}“ blieb unbemerkt")
    if any(muster in lauf.stdout + lauf.stderr for muster in ("Exception in Tkinter callback", "invalid command name",
                                                               "bgerror failed")):
        for ergebnis in ergebnisse:
            ergebnis.melden(ABWEICHUNG, "Oberfläche", "Tk-/Tcl-Rückruffehler nach dem Neustart")
    return ergebnisse


def anzeige_phase(stand_pfad: Path) -> int:
    """Zweiter Prozess: Glide neu starten, Bestand vergleichen, Anzeige jeder Liste ablesen."""
    stand = json.loads(stand_pfad.read_text(encoding="utf-8"))
    if Path(os.environ.get("GLIDE_DATA_DIR", "")).resolve() != stand_pfad.parent.resolve():
        raise SystemExit("Die Anzeigeprüfung läuft nur im künstlichen Datenordner ihres Stands.")
    if str(SOURCE) not in sys.path:
        sys.path.insert(0, str(SOURCE))
    mod = lade_modul("glide_ki_ausgabe_app", SOURCE / "app.pyw")
    rueckmeldung = []
    root, app, fehler, meldungen = _starten(mod)
    try:
        # Bestand vor jeder Bedienung festhalten: Öffnen einer Seite kann ihren
        # Editor beim Wechseln speichern lassen.
        geladen = {l["id"]: json.loads(json.dumps(l)) for l in app.lists}
        gefunden = []
        for eintrag in stand["listen"]:
            erwartet = eintrag["liste"]
            ergebnis = Ergebnis("")
            zeile = {"ergebnis": eintrag["ergebnis"], "titel": erwartet["title"]}
            liste = next((l for l in app.lists if l["id"] == erwartet["id"]), None)
            if liste is None:
                ergebnis.melden(ABWEICHUNG, "Neustart", f"„{erwartet['title']}“ fehlt nach dem Neustart")
            else:
                if not gleichwertig(erwartet, geladen[liste["id"]]):
                    ergebnis.melden(ABWEICHUNG, "Neustart", f"„{liste['title']}“ ist nach dem Neustart verändert")
                oeffnen(app, root, liste)
                lies_anzeige(app, ergebnis, liste)
                gefunden.append((zeile, liste))
            if fehler:
                ergebnis.melden(ABWEICHUNG, "Oberfläche", f"{len(fehler)} Fehler in Rückrufen der Oberfläche")
                fehler.clear()
            zeile["befunde"] = [asdict(b) for b in ergebnis.befunde]
            rueckmeldung.append(zeile)
        if stand.get("gegenprobe"):
            # Erst nach allen Vergleichen und schreibgeschützt: Die Gegenprobe
            # verfälscht nur die Anzeige und darf nichts speichern.
            app._data_read_only = True
            for zeile, liste in gefunden:
                oeffnen(app, root, liste)
                if verfaelschen(app, liste):
                    probe = Ergebnis("")
                    lies_anzeige(app, probe, liste)
                    zeile["gegenprobe_erkannt"] = bool(probe.arten(ABWEICHUNG))
            fehler.clear()
    finally:
        _beenden(app, root)
    (stand_pfad.parent / "ki_ausgabe_anzeige.json").write_text(
        json.dumps(rueckmeldung, ensure_ascii=False), encoding="utf-8")
    return 0


def bericht_text(ergebnisse) -> str:
    zeilen = []
    for ergebnis in ergebnisse:
        zeilen.append(f"== {ergebnis.datei}")
        for befund in ergebnis.befunde:
            zeilen.append(f"{befund.art}: {befund.ort}: {befund.text}")
        zahlen = ", ".join(f"{wert} {name}" for name, wert in ergebnis.angelegt.items())
        zeilen.append(f"Ergebnis: {'bestanden' if ergebnis.bestanden else 'nicht bestanden'}"
                      + (f" · angelegt: {zahlen}" if zahlen else "")
                      + f" · {len(ergebnis.arten(ABWEICHUNG))} Abweichungen, {len(ergebnis.arten(GRENZE))} Grenzen")
    return "\n".join(zeilen)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("dateien", nargs="*", help="KI-Ausgaben: .glideexchange, .json oder .md")
    parser.add_argument("--kontext", help="Kontextpaket (.glidecontext) zu einem Änderungsvorschlag")
    parser.add_argument("--oberflaeche", action="store_true",
                        help="in einer echten Glide-Instanz anlegen, speichern, neu starten und die Anzeige ablesen")
    parser.add_argument("--gegenprobe", action="store_true",
                        help="mit --oberflaeche: verfälschte Anzeige muss als Abweichung erkannt werden")
    parser.add_argument("--json", help="Bericht zusätzlich als JSON schreiben (Datei darf noch nicht existieren)")
    parser.add_argument("--behalten", action="store_true", help="künstlichen Datenordner danach nicht löschen")
    parser.add_argument("--anzeige", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.anzeige:
        return anzeige_phase(Path(args.anzeige))
    if not args.dateien:
        parser.error("mindestens eine Datei angeben")
    kontext_paket = None
    if args.kontext:
        kontext_paket = json.loads(Path(args.kontext).read_text(encoding="utf-8-sig"))
    mod, ordner = glide_laden()
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            if args.oberflaeche:
                ergebnisse = pruefe_mit_oberflaeche(mod, args.dateien, kontext_paket, gegenprobe=args.gegenprobe)
            else:
                ergebnisse = pruefe_fensterlos(mod, args.dateien, kontext_paket)
    finally:
        if not args.behalten:
            shutil.rmtree(ordner, ignore_errors=True)
    print(bericht_text(ergebnisse))
    if args.behalten:
        print(f"Künstlicher Datenordner: {ordner}")
    if args.json:
        ziel = Path(args.json)
        if ziel.exists():
            print(f"FEHLER: {ziel} gibt es schon; nichts überschrieben.", file=sys.stderr)
            return 1
        ziel.write_text(json.dumps([{"datei": e.datei, "bestanden": e.bestanden, "angelegt": e.angelegt,
                                     "befunde": [asdict(b) for b in e.befunde]} for e in ergebnisse],
                                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if all(e.bestanden for e in ergebnisse) else 1


if __name__ == "__main__":
    sys.exit(main())
