#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Glide-Importdateien prüfen und Pixelzeichnungen kodieren – Hilfsskript des Skills `glide-to-do`.

Nur Standardbibliothek, Python 3.9 oder neuer. Das Skript liest die genannten
Dateien und schreibt ausschließlich die ausdrücklich angegebene Ausgabedatei;
es fasst weder den Glide-Datenordner noch Sicherungen an und braucht kein Netz.

    python3 glide_datei.py pruefen DATEI [DATEI …] [--kontext PAKET.glidecontext] [--streng]
    python3 glide_datei.py zeichnung EINGABE.json AUSGABE [--nur-zeichnung]

`pruefen` kennt drei Dateiarten:
  * `.glideexchange`/`.json` mit `mode: "create"` – neue Ordner, Listen, Punkte, Notizen, Zeichnungen
  * `.glideexchange`/`.json` mit `mode: "patch"` – Änderungsvorschlag zu einem Kontextpaket
  * `.md` – Seite für „Datei › Importieren › Seite aus Datei …“

Meldungen: FEHLER (Glide lehnt ab oder verliert Inhalt), WARNUNG (Glide kürzt,
übergeht oder ändert etwas), HINWEIS (zulässig, aber besser anders). Exitcode 1
bei Fehlern, mit `--streng` auch bei Warnungen.

Die Regeln bilden die Prüfung von Glide 1.0.2 (Austauschformat 2) nach.
`tests/tools/test_agenten_skill.py` vergleicht sie mit dem Glide-Code; ändert
sich der Austauschweg, muss dieses Skript im selben Schnitt mitgehen.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
import zipfile

GLIDE_VERSION = "1.0.2"
FORMAT = "glide.exchange"
FORMAT_VERSION = 2
CONTEXT_FORMAT = "glide.context"
SUFFIX = ".glideexchange"

# Feldmengen wie `ListApp.EXCHANGE_*_FIELDS`; `capabilities` darf zusätzlich an der Wurzel stehen.
ROOT_FIELDS = frozenset({"format", "format_version", "generator", "created_for", "mode",
                         "labels", "folders", "lists", "notes"})
LABEL_FIELDS = frozenset({"key", "name", "color"})
FOLDER_FIELDS = frozenset({"key", "title", "description", "parent", "labels", "folder_kind", "attachments"})
LIST_FIELDS = frozenset({"key", "title", "description", "folder", "labels", "items", "list_kind",
                         "rich_note", "markdown", "drawing", "animation", "attachments", "cover"})
ITEM_FIELDS = frozenset({"key", "type", "title", "text", "description", "done", "importance", "due",
                         "due_time", "planned_date", "estimated_minutes", "labels", "checklist",
                         "children", "repeat", "reminder", "attachments"})
ITEM_TYPES = ("task", "long", "group", "heading")
STRUCTURAL_TYPES = ("group", "heading")
LIST_KINDS = ("tasks", "note", "drawing", "page", "gallery")
FOLDER_KINDS = ("standard", "library", "journal")

MAX_BYTES = 12 * 1024 * 1024
MAX_ITEMS = 5000
MAX_DEPTH = 12
MAX_CHECKLIST_ENTRIES = 50
MAX_CHECKLIST_TEXT = 200
MAX_ESTIMATED_MINUTES = 60000
TITLE_MAX = 40
MAX_LABEL_NAME = 40
MAX_LABELS = 80
MAX_LABELS_PER_ITEM = 20
LABEL_COLORS = ("accent", "clear", "due_action", "export", "flag", "delete", "import")

# Änderungsvorschlag wie `exchange_patch.py`.
PATCH_FIELDS = ("title", "description", "importance", "due", "due_time", "planned_date",
                "estimated_minutes", "done", "labels")
PATCH_MAX_CHANGES = 5000
PATCH_MAX_MINUTES = 10080
PATCH_MAX_DESCRIPTION = 20000

# Seitentext wie `RichNoteEditor`.
RICH_NOTE_FORMATS = ("bold", "italic", "underline", "strike", "h1", "h2", "h3", "bullet", "number",
                     "quote", "code", "codeblock", "highlight", "table", "divider", "task",
                     "indent1", "indent2", "indent3", "h4", "callout", "toggle", "toggle_closed")
RICH_NOTE_MAX_TEXT = 1_000_000
RICH_NOTE_MAX_SPANS = 10000
MARKDOWN_MAX_CHARS = 5_000_000

# Zeichenmodell wie `drawing.py`.
DRAWING_FORMAT = "glide.drawing"
DRAWING_SIZES = (16, 32, 64, 128)
DRAWING_BACKGROUND = "#FFFFFF"
DRAWING_OPAQUE_WHITE = "#FEFEFE"
DRAWING_MAX_COLORS = 256
DRAWING_ENCODING = "hex8-row-v1"
DRAWING_COLOR_SPACE = "srgb"
DRAWING_PALETTE_ID = "glide-drawing-default"
DRAWING_FIELDS = frozenset({"format", "format_version", "width", "height", "color_space",
                            "palette_id", "palette_version", "palette", "encoding", "rows"})

_DATUM = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_UHRZEIT = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")
_FARBE = re.compile(r"^#[0-9A-Fa-f]{6}$")
_REF = re.compile(r"^r-[0-9a-f]{16}$")
_BASE = re.compile(r"^[0-9a-f]{16}$")
_PALETTEN_ID = re.compile(r"^[A-Za-z0-9._-]{1,64}$")
_LINK = re.compile(r"^(https?://|mailto:)\S+$")


class Bericht:
    """Gesammelte Meldungen zu einer Datei."""

    def __init__(self, name: str):
        self.name = name
        self.fehler: list[str] = []
        self.warnungen: list[str] = []
        self.hinweise: list[str] = []

    def f(self, text: str) -> None:
        self.fehler.append(text)

    def w(self, text: str) -> None:
        self.warnungen.append(text)

    def h(self, text: str) -> None:
        self.hinweise.append(text)

    def zeilen(self) -> list[str]:
        return ([f"FEHLER: {t}" for t in self.fehler] + [f"WARNUNG: {t}" for t in self.warnungen]
                + [f"HINWEIS: {t}" for t in self.hinweise])


def _ist_ganzzahl(wert) -> bool:
    return isinstance(wert, int) and not isinstance(wert, bool)


def _datum_ok(wert) -> bool:
    if not isinstance(wert, str) or not _DATUM.fullmatch(wert):
        return False
    try:
        _dt.date.fromisoformat(wert)
    except ValueError:
        return False
    return True


def _titel(bericht: Bericht, wo: str, titel: str) -> None:
    if len(titel) > TITLE_MAX:
        bericht.w(f"{wo}: Titel hat {len(titel)} Zeichen; Glide kürzt neue Titel auf {TITLE_MAX} "
                  "und schiebt das Original in die Beschreibung. Kürzer fassen, Details in description.")


# ----------------------------------------------------------------------
# Zeichnung
# ----------------------------------------------------------------------
def pruefe_zeichnung(bericht: Bericht, wo: str, dokument) -> None:
    """Prüft ein `glide.drawing`-Dokument wie `DrawingModel.from_document`."""
    if not isinstance(dokument, dict):
        bericht.f(f"{wo}: drawing muss ein Objekt sein.")
        return
    fremd = set(dokument) - DRAWING_FIELDS
    fehlt = DRAWING_FIELDS - set(dokument)
    if fremd:
        bericht.f(f"{wo}: unbekannte Zeichnungsfelder {', '.join(sorted(fremd))}.")
    if fehlt:
        bericht.f(f"{wo}: fehlende Zeichnungsfelder {', '.join(sorted(fehlt))}.")
        return
    for feld, soll in (("format", DRAWING_FORMAT), ("color_space", DRAWING_COLOR_SPACE),
                       ("encoding", DRAWING_ENCODING)):
        if dokument.get(feld) != soll:
            bericht.f(f"{wo}: {feld} muss „{soll}“ sein.")
    breite, hoehe = dokument.get("width"), dokument.get("height")
    if not _ist_ganzzahl(breite) or breite != hoehe or breite not in DRAWING_SIZES:
        bericht.f(f"{wo}: width und height müssen gleich und eine von {DRAWING_SIZES} sein.")
        return
    version = 1 if breite == 128 else 2
    if dokument.get("format_version") != version:
        bericht.f(f"{wo}: format_version muss bei {breite} Zellen {version} sein.")
    if not isinstance(dokument.get("palette_id"), str) or not _PALETTEN_ID.fullmatch(dokument["palette_id"]):
        bericht.f(f"{wo}: palette_id ist ungültig.")
    pv = dokument.get("palette_version")
    if not _ist_ganzzahl(pv) or not 1 <= pv <= 1_000_000:
        bericht.f(f"{wo}: palette_version muss eine Ganzzahl 1–1.000.000 sein.")
    palette = dokument.get("palette")
    if not isinstance(palette, list) or not palette:
        bericht.f(f"{wo}: palette muss eine nicht leere Liste sein.")
        return
    farben = []
    for farbe in palette:
        if not isinstance(farbe, str) or not _FARBE.fullmatch(farbe):
            bericht.f(f"{wo}: Palettenfarbe {farbe!r} ist kein #RRGGBB.")
            return
        farben.append(farbe.upper())
    if farben[0] != DRAWING_BACKGROUND:
        bericht.f(f"{wo}: palette[0] muss {DRAWING_BACKGROUND} sein (Grund, im Symbol durchsichtig).")
    if len(farben) > DRAWING_MAX_COLORS or len(set(farben)) != len(farben):
        bericht.f(f"{wo}: höchstens {DRAWING_MAX_COLORS} Farben, jede nur einmal.")
    zeilen = dokument.get("rows")
    if not isinstance(zeilen, list) or len(zeilen) != hoehe:
        bericht.f(f"{wo}: rows muss genau {hoehe} Zeilen enthalten.")
        return
    muster = re.compile(r"[0-9A-F]{%d}" % (2 * breite))
    for nummer, zeile in enumerate(zeilen, 1):
        if not isinstance(zeile, str) or not muster.fullmatch(zeile):
            bericht.f(f"{wo}: Zeile {nummer} braucht {2 * breite} große Hexzeichen.")
            return
        if max(bytes.fromhex(zeile)) >= len(farben):
            bericht.f(f"{wo}: Zeile {nummer} verweist außerhalb der Palette.")
            return


def baue_zeichnung(eingabe: dict) -> dict:
    """Aus Legende und Zeichenreihen ein `glide.drawing`-Dokument bauen."""
    if not isinstance(eingabe, dict):
        raise ValueError("Die Eingabe muss ein JSON-Objekt sein.")
    groesse = eingabe.get("size")
    if groesse not in DRAWING_SIZES:
        raise ValueError(f"size muss eine von {DRAWING_SIZES} sein.")
    legende = eingabe.get("legend")
    pixel = eingabe.get("pixels")
    if not isinstance(legende, dict) or not legende:
        raise ValueError("legend ordnet jedem Zeichen eine Farbe #RRGGBB zu.")
    if not isinstance(pixel, list) or len(pixel) != groesse:
        raise ValueError(f"pixels braucht genau {groesse} Zeilen.")
    farbe_je_zeichen = {}
    for zeichen, farbe in legende.items():
        if not isinstance(zeichen, str) or len(zeichen) != 1:
            raise ValueError(f"Legendeneintrag {zeichen!r}: genau ein Zeichen je Farbe.")
        if not isinstance(farbe, str) or not _FARBE.fullmatch(farbe):
            raise ValueError(f"Legendeneintrag {zeichen!r}: {farbe!r} ist kein #RRGGBB.")
        farbe_je_zeichen[zeichen] = farbe.upper()
    palette = [DRAWING_BACKGROUND]
    zeilen = []
    for nummer, zeile in enumerate(pixel, 1):
        if not isinstance(zeile, str) or len(zeile) != groesse:
            raise ValueError(f"pixels Zeile {nummer}: genau {groesse} Zeichen.")
        indizes = []
        for zeichen in zeile:
            if zeichen not in farbe_je_zeichen:
                raise ValueError(f"pixels Zeile {nummer}: Zeichen {zeichen!r} fehlt in legend.")
            farbe = farbe_je_zeichen[zeichen]
            if farbe not in palette:
                palette.append(farbe)
            indizes.append(palette.index(farbe))
        zeilen.append(bytes(indizes).hex().upper())
    if len(palette) > DRAWING_MAX_COLORS:
        raise ValueError(f"Höchstens {DRAWING_MAX_COLORS} Farben.")
    return {
        "format": DRAWING_FORMAT,
        "format_version": 1 if groesse == 128 else 2,
        "width": groesse,
        "height": groesse,
        "color_space": DRAWING_COLOR_SPACE,
        "palette_id": DRAWING_PALETTE_ID,
        "palette_version": 1,
        "palette": palette,
        "encoding": DRAWING_ENCODING,
        "rows": zeilen,
    }


def zeichnung_als_austausch(eingabe: dict) -> dict:
    """Austauschdatei mit einer Zeichnungsseite, wahlweise in einem neuen Ordner."""
    titel = " ".join(str(eingabe.get("title") or "").split())
    if not titel:
        raise ValueError("title fehlt.")
    liste = {"key": "list-1", "title": titel, "list_kind": "drawing",
             "drawing": baue_zeichnung(eingabe)}
    beschreibung = str(eingabe.get("description") or "").strip()
    if beschreibung:
        liste["description"] = beschreibung
    nutzlast = {"format": FORMAT, "format_version": FORMAT_VERSION, "mode": "create",
                "generator": {"type": "ai", "name": "glide-to-do"}}
    ordner = " ".join(str(eingabe.get("folder") or "").split())
    if ordner:
        nutzlast["folders"] = [{"key": "folder-1", "title": ordner}]
        liste["folder"] = "folder-1"
    nutzlast["lists"] = [liste]
    return nutzlast


# ----------------------------------------------------------------------
# Neue Inhalte (mode "create")
# ----------------------------------------------------------------------
def _pruefe_rich_note(bericht: Bericht, wo: str, dokument, art: str) -> None:
    if not isinstance(dokument, dict) or not isinstance(dokument.get("text", ""), str):
        bericht.f(f"{wo}: rich_note braucht {{\"text\": …, \"spans\": [], \"links\": {{}}}}.")
        return
    text = dokument.get("text", "")
    if len(text) > RICH_NOTE_MAX_TEXT:
        bericht.f(f"{wo}: Text länger als {RICH_NOTE_MAX_TEXT} Zeichen.")
    spans = dokument.get("spans", [])
    links = dokument.get("links", {})
    if not isinstance(spans, list) or len(spans) > RICH_NOTE_MAX_SPANS:
        bericht.f(f"{wo}: spans muss eine Liste mit höchstens {RICH_NOTE_MAX_SPANS} Einträgen sein.")
        return
    if not isinstance(links, dict):
        bericht.f(f"{wo}: links muss ein Objekt sein.")
        return
    for schluessel, ziel in links.items():
        if not (isinstance(schluessel, str) and schluessel.startswith("link:") and len(schluessel) <= 80
                and isinstance(ziel, str) and len(ziel) <= 2048 and _LINK.fullmatch(ziel)):
            bericht.w(f"{wo}: Link {schluessel!r} wird verworfen (nur http, https, mailto).")
    for span in spans:
        if not isinstance(span, dict) or not isinstance(span.get("tag"), str):
            bericht.f(f"{wo}: ungültiger Formatbereich {span!r}.")
            return
        start, ende, tag = span.get("start"), span.get("end"), span["tag"]
        if not (_ist_ganzzahl(start) and _ist_ganzzahl(ende) and 0 <= start < ende <= len(text)):
            bericht.f(f"{wo}: Formatbereich {tag} liegt außerhalb des Texts (Python-Zeichenpositionen).")
            return
        if tag not in RICH_NOTE_FORMATS and tag not in links:
            bericht.w(f"{wo}: Formatbereich {tag!r} kennt Glide nicht und verwirft ihn.")
    if "images" in dokument:
        bericht.w(f"{wo}: Seitenbilder brauchen Anhänge; das Austauschformat trägt sie nicht.")
    if spans:
        bericht.h(f"{wo}: Formatierte Seiten sicherer als Markdown-Datei anlegen (Seite aus Datei …).")
    elif art == "page" and re.search(r"(?m)^(#{1,4} |\s*[-*] \[[ xX]\] |\|.*\|\s*$)", text):
        bericht.w(f"{wo}: Der Text sieht nach Markdown aus, wird hier aber nicht umgewandelt. "
                  "Als .md-Datei über „Seite aus Datei …“ importieren.")


def _pruefe_punkt(bericht: Bericht, wo: str, punkt, tiefe: int, zaehler: dict, label_keys: set) -> None:
    if zaehler["punkte"] >= MAX_ITEMS:
        return
    if not isinstance(punkt, dict):
        bericht.f(f"{wo}: Punkt ist kein Objekt.")
        return
    for feld in punkt:
        if feld not in ITEM_FIELDS:
            bericht.f(f"{wo}: unbekanntes Punktfeld „{feld}“ (Glide übernimmt es nicht).")
    art = punkt.get("type", "task")
    if art not in ITEM_TYPES:
        bericht.w(f"{wo}: Punktart {art!r} unbekannt; Glide macht eine Aufgabe daraus.")
        art = "task"
    titel = " ".join(str(punkt.get("title") or punkt.get("text") or "").split())
    if not titel:
        bericht.f(f"{wo}: Punkt ohne Titel wird übersprungen.")
        return
    zaehler["punkte"] += 1
    wo = f"{wo} „{titel[:30]}“"
    _titel(bericht, wo, titel)
    if "description" in punkt and not isinstance(punkt["description"], str):
        bericht.f(f"{wo}: description muss Text sein.")
    if art in STRUCTURAL_TYPES:
        planung = [f for f in ("done", "importance", "due", "due_time", "planned_date",
                               "estimated_minutes", "checklist") if punkt.get(f) not in (None, False, 0, [])]
        if planung:
            bericht.w(f"{wo}: {art} trägt keine {', '.join(planung)}; Glide verwirft diese Angaben.")
    if "done" in punkt and not isinstance(punkt["done"], bool):
        bericht.f(f"{wo}: done muss true oder false sein.")
    if "importance" in punkt:
        wert = punkt["importance"]
        if not _ist_ganzzahl(wert) or not 0 <= wert <= 3:
            bericht.f(f"{wo}: importance muss 0, 1, 2 oder 3 sein.")
    for feld in ("due", "planned_date"):
        if punkt.get(feld) is not None and not _datum_ok(punkt[feld]):
            bericht.f(f"{wo}: {feld} {punkt[feld]!r} ist kein Datum JJJJ-MM-TT; Glide lässt es leer.")
    if punkt.get("due_time") is not None:
        if not isinstance(punkt["due_time"], str) or not _UHRZEIT.fullmatch(punkt["due_time"]):
            bericht.f(f"{wo}: due_time {punkt['due_time']!r} ist keine Uhrzeit HH:MM.")
        elif not punkt.get("due"):
            bericht.w(f"{wo}: due_time ohne due – Glide verwirft die Uhrzeit.")
    if punkt.get("estimated_minutes") is not None:
        wert = punkt["estimated_minutes"]
        if not _ist_ganzzahl(wert) or not 1 <= wert <= MAX_ESTIMATED_MINUTES:
            bericht.f(f"{wo}: estimated_minutes muss eine Ganzzahl 1–{MAX_ESTIMATED_MINUTES} sein; "
                      "Glide lässt den Aufwand sonst still leer.")
    schritte = punkt.get("checklist")
    if schritte is not None:
        if not isinstance(schritte, list):
            bericht.f(f"{wo}: checklist muss eine Liste sein.")
        else:
            if len(schritte) > MAX_CHECKLIST_ENTRIES:
                bericht.f(f"{wo}: {len(schritte)} Checklistenschritte; Glide übernimmt nur {MAX_CHECKLIST_ENTRIES}.")
            for schritt in schritte:
                if (not isinstance(schritt, dict) or not isinstance(schritt.get("text"), str)
                        or not schritt["text"].strip()):
                    bericht.f(f"{wo}: Checklistenschritt braucht {{\"text\": …, \"done\": false}}.")
                    break
                if len(schritt["text"]) > MAX_CHECKLIST_TEXT:
                    bericht.w(f"{wo}: Checklistenschritt länger als {MAX_CHECKLIST_TEXT} Zeichen.")
                if "done" in schritt and not isinstance(schritt["done"], bool):
                    bericht.f(f"{wo}: Checklistenschritt done muss true oder false sein.")
    labels = punkt.get("labels")
    if labels is not None:
        if not isinstance(labels, list) or not all(isinstance(l, str) and l.strip() for l in labels):
            bericht.f(f"{wo}: labels ist eine Liste von Label-Schlüsseln oder -Namen.")
        else:
            if len(labels) > MAX_LABELS_PER_ITEM:
                bericht.w(f"{wo}: mehr als {MAX_LABELS_PER_ITEM} Labels an einem Punkt.")
            if label_keys:
                fremd = [l for l in labels if l not in label_keys]
                if fremd:
                    bericht.w(f"{wo}: Labels {', '.join(fremd)} stehen nicht unter labels; "
                              "Glide legt sie über ihren Namen an.")
    if "repeat" in punkt and punkt.get("repeat") is not None:
        if not isinstance(punkt["repeat"], dict):
            bericht.f(f"{wo}: repeat muss ein Objekt sein.")
        elif not punkt.get("due"):
            bericht.w(f"{wo}: repeat ohne due – Glide verwirft die Wiederholung.")
    if "reminder" in punkt and punkt.get("reminder") is not None:
        if not isinstance(punkt["reminder"], dict):
            bericht.f(f"{wo}: reminder muss ein Objekt sein.")
        elif punkt["reminder"].get("mode") not in ("relative", "fixed"):
            bericht.f(f"{wo}: reminder mode muss 'relative' oder 'fixed' sein.")
    kinder = punkt.get("children")
    if kinder is not None:
        if not isinstance(kinder, list):
            bericht.f(f"{wo}: children muss eine Liste sein.")
        elif kinder and tiefe + 1 >= MAX_DEPTH:
            bericht.f(f"{wo}: Unterpunkte jenseits von Ebene {MAX_DEPTH} übernimmt Glide nicht.")
        else:
            for nummer, kind in enumerate(kinder, 1):
                _pruefe_punkt(bericht, f"{wo} › {nummer}", kind, tiefe + 1, zaehler, label_keys)


def pruefe_create(bericht: Bericht, nutzlast: dict) -> None:
    for feld in nutzlast:
        if feld not in ROOT_FIELDS and feld != "capabilities":
            bericht.f(f"Wurzel: unbekanntes Feld „{feld}“.")
    label_keys: set = set()
    label_namen: set = set()
    labels = nutzlast.get("labels") or []
    if not isinstance(labels, list):
        bericht.f("labels muss eine Liste sein.")
        labels = []
    for nummer, label in enumerate(labels, 1):
        wo = f"Label {nummer}"
        if not isinstance(label, dict) or not str(label.get("name") or "").strip():
            bericht.f(f"{wo}: Label ohne Namen wird übersprungen.")
            continue
        for feld in label:
            if feld not in LABEL_FIELDS:
                bericht.f(f"{wo}: unbekanntes Labelfeld „{feld}“.")
        name = " ".join(str(label["name"]).split())
        if len(name) > MAX_LABEL_NAME:
            bericht.w(f"{wo}: Name länger als {MAX_LABEL_NAME} Zeichen; Glide kürzt ihn.")
        if label.get("key"):
            if str(label["key"]) in label_keys:
                bericht.f(f"{wo}: Schlüssel {label['key']!r} doppelt.")
            label_keys.add(str(label["key"]))
        label_namen.add(name.casefold())
        if "color" in label:
            farbe = label.get("color")
            if farbe not in LABEL_COLORS:
                bericht.w(f"{wo}: Farbe {farbe!r} unbekannt (erlaubt: {', '.join(LABEL_COLORS)}); Glide vergibt eine eigene Farbe.")
    if len(label_namen) > 12:
        bericht.h(f"{len(label_namen)} Labels in einer Datei; wenige, wiederverwendete Labels sind übersichtlicher "
                  f"(Glide hält insgesamt höchstens {MAX_LABELS}).")

    ordner_keys: set = set()
    ordner = nutzlast.get("folders") or []
    if not isinstance(ordner, list):
        bericht.f("folders muss eine Liste sein.")
        ordner = []
    for nummer, eintrag in enumerate(ordner, 1):
        wo = f"Ordner {nummer}"
        if not isinstance(eintrag, dict):
            bericht.f(f"{wo}: kein Objekt.")
            continue
        for feld in eintrag:
            if feld not in FOLDER_FIELDS:
                bericht.f(f"{wo}: unbekanntes Ordnerfeld „{feld}“.")
        titel = " ".join(str(eintrag.get("title") or "").split())
        if not titel:
            bericht.f(f"{wo}: Ordner ohne Titel wird übersprungen.")
            continue
        _titel(bericht, f"{wo} „{titel}“", titel)
        eltern = eintrag.get("parent")
        if eltern and str(eltern) not in ordner_keys:
            bericht.w(f"{wo} „{titel}“: parent {eltern!r} ist kein weiter oben beschriebener Ordner; "
                      "Glide legt den Ordner dann auf oberster Ebene an.")
        labels = eintrag.get("labels")
        if labels is not None:
            if not isinstance(labels, list) or not all(isinstance(l, str) and l.strip() for l in labels):
                bericht.f(f"{wo} „{titel}“: labels muss eine Liste von Label-Schlüsseln oder -Namen sein.")
        if "folder_kind" in eintrag:
            art = eintrag.get("folder_kind")
            if art not in FOLDER_KINDS:
                bericht.w(f"{wo} „{titel}“: Ordnerart {art!r} unbekannt (erlaubt: {', '.join(FOLDER_KINDS)}); "
                          "Glide verwendet standard.")
        if eintrag.get("key"):
            if str(eintrag["key"]) in ordner_keys:
                bericht.f(f"{wo}: Schlüssel {eintrag['key']!r} doppelt.")
            ordner_keys.add(str(eintrag["key"]))

    listen = nutzlast.get("lists")
    if not isinstance(listen, list) or not listen:
        bericht.f("Die Datei enthält keine Listen (lists).")
        return
    zaehler = {"punkte": 0}
    listen_keys: set = set()
    for nummer, liste in enumerate(listen, 1):
        wo = f"Liste {nummer}"
        if not isinstance(liste, dict):
            bericht.f(f"{wo}: kein Objekt.")
            continue
        for feld in liste:
            if feld not in LIST_FIELDS:
                bericht.f(f"{wo}: unbekanntes Listenfeld „{feld}“.")
        titel = " ".join(str(liste.get("title") or "").split())
        if not titel:
            bericht.f(f"{wo}: Liste ohne Titel wird übersprungen.")
            continue
        wo = f"{wo} „{titel}“"
        _titel(bericht, wo, titel)
        if liste.get("key"):
            if str(liste["key"]) in listen_keys:
                bericht.f(f"{wo}: Schlüssel {liste['key']!r} doppelt.")
            listen_keys.add(str(liste["key"]))
        art = liste.get("list_kind", "tasks")
        if art not in LIST_KINDS:
            bericht.f(f"{wo}: Listenart {art!r} unbekannt (erlaubt: {', '.join(LIST_KINDS)}).")
            continue
        if liste.get("folder") and str(liste["folder"]) not in ordner_keys:
            bericht.w(f"{wo}: Ordner {liste['folder']!r} ist nicht beschrieben; die Liste entsteht ohne Ordner.")
        labels = liste.get("labels")
        if labels is not None:
            if not isinstance(labels, list) or not all(isinstance(l, str) and l.strip() for l in labels):
                bericht.f(f"{wo}: labels muss eine Liste von Label-Schlüsseln oder -Namen sein.")
        if "rich_note" in liste:
            _pruefe_rich_note(bericht, wo, liste["rich_note"], art)
        if "markdown" in liste and not isinstance(liste["markdown"], str):
            bericht.f(f"{wo}: markdown muss Text sein.")
        if liste.get("animation") is not None:
            if art != "drawing":
                bericht.f(f"{wo}: Eine Bildfolge gehört in eine Zeichnung (list_kind „drawing“).")
            else:
                bericht.h(f"{wo}: Bildfolgen prüft erst Glide beim Import.")
        if art == "drawing":
            if liste.get("items"):
                bericht.f(f"{wo}: Eine Zeichnung kann keine Punkte enthalten.")
            if "drawing" in liste:
                pruefe_zeichnung(bericht, wo, liste["drawing"])
            else:
                bericht.w(f"{wo}: Zeichnung ohne drawing – Glide legt eine leere Fläche an.")
            continue
        if "drawing" in liste:
            bericht.f(f"{wo}: drawing gehört nur in eine Zeichnung (list_kind „drawing“).")
        if art == "gallery":
            bericht.w(f"{wo}: Galerien bestehen aus Bildern, die das Austauschformat noch nicht trägt.")
        punkte = liste.get("items") or []
        if not isinstance(punkte, list):
            bericht.f(f"{wo}: items muss eine Liste sein.")
            continue
        for index, punkt in enumerate(punkte, 1):
            _pruefe_punkt(bericht, f"{wo} › {index}", punkt, 0, zaehler, label_keys)
    if zaehler["punkte"] >= MAX_ITEMS:
        bericht.f(f"Mehr als {MAX_ITEMS} Punkte in einer Datei.")


# ----------------------------------------------------------------------
# Änderungsvorschlag (mode "patch")
# ----------------------------------------------------------------------
def _patch_wert(feld: str, wert) -> str | None:
    """Fehlermeldung oder None, wie `exchange_patch.validate_value`."""
    if feld == "title":
        if not isinstance(wert, str) or not wert.strip() or len(wert) > TITLE_MAX:
            return f"Titel muss Text mit 1 bis {TITLE_MAX} Zeichen sein"
    elif feld == "description":
        if not isinstance(wert, str) or len(wert) > PATCH_MAX_DESCRIPTION:
            return f"Beschreibung muss Text bis {PATCH_MAX_DESCRIPTION} Zeichen sein"
    elif feld == "importance":
        if not _ist_ganzzahl(wert) or not 0 <= wert <= 3:
            return "Wichtigkeit muss 0 bis 3 sein"
    elif feld in ("due", "planned_date"):
        if wert is not None and not _datum_ok(wert):
            return "Datum im Format JJJJ-MM-TT oder null"
    elif feld == "due_time":
        if wert is not None and (not isinstance(wert, str) or not _UHRZEIT.fullmatch(wert)):
            return "Uhrzeit im Format HH:MM oder null"
    elif feld == "estimated_minutes":
        if wert is not None and (not _ist_ganzzahl(wert) or not 1 <= wert <= PATCH_MAX_MINUTES):
            return f"Aufwand in Minuten (1 bis {PATCH_MAX_MINUTES}) oder null"
    elif feld == "done":
        if not isinstance(wert, bool):
            return "Erledigt muss true oder false sein"
    elif feld == "labels":
        if not isinstance(wert, list) or not all(isinstance(n, str) and n.strip() for n in wert):
            return "Labels als Liste von Namen"
    else:
        return f"unbekanntes Feld „{feld}“"
    return None


def pruefe_patch(bericht: Bericht, nutzlast: dict, kontext: dict | None) -> None:
    if nutzlast.get("format_version") != FORMAT_VERSION:
        bericht.f(f"Ein Änderungsvorschlag braucht format_version {FORMAT_VERSION}.")
    for feld in nutzlast:
        if feld not in ("format", "format_version", "mode", "changes", "generator", "notes"):
            bericht.w(f"Wurzel: Feld „{feld}“ wertet der Änderungsvorschlag nicht aus.")
    aenderungen = nutzlast.get("changes")
    if not isinstance(aenderungen, list) or not aenderungen:
        bericht.f("Der Vorschlag enthält keine Änderungen (changes).")
        return
    if len(aenderungen) > PATCH_MAX_CHANGES:
        bericht.f(f"Höchstens {PATCH_MAX_CHANGES} Änderungen je Datei.")
    bekannt = {}
    if kontext is not None:
        bekannt = {p.get("ref"): p for p in kontext.get("items") or [] if isinstance(p, dict)}
    gesehen = set()
    for nummer, aenderung in enumerate(aenderungen, 1):
        wo = f"Änderung {nummer}"
        if (not isinstance(aenderung, dict) or not isinstance(aenderung.get("ref"), str)
                or not isinstance(aenderung.get("base"), str) or not isinstance(aenderung.get("set"), dict)):
            bericht.f(f"{wo}: ref, base und set fehlen oder haben die falsche Form.")
            continue
        ref, base, setze = aenderung["ref"], aenderung["base"], aenderung["set"]
        if not _REF.fullmatch(ref) or not _BASE.fullmatch(base):
            bericht.f(f"{wo}: ref und base unverändert aus dem Kontextpaket kopieren.")
        if ref in gesehen:
            bericht.f(f"{wo}: dieselbe Aufgabe kommt mehrfach vor.")
        gesehen.add(ref)
        if kontext is not None:
            quelle = bekannt.get(ref)
            if quelle is None:
                bericht.f(f"{wo}: ref {ref} steht nicht im Kontextpaket.")
            elif quelle.get("base") != base:
                bericht.f(f"{wo}: base passt nicht zum Kontextpaket; Glide meldet einen Konflikt.")
        if not setze:
            bericht.w(f"{wo}: set ist leer.")
        for feld, wert in setze.items():
            meldung = _patch_wert(feld, wert)
            if meldung:
                bericht.f(f"{wo}: {meldung}.")
        if kontext is not None and ref in bekannt and isinstance(bekannt[ref].get("fields"), dict):
            alt = bekannt[ref]["fields"]
            if all(alt.get(feld) == wert for feld, wert in setze.items() if feld != "labels"):
                if "labels" not in setze or sorted(setze["labels"]) == sorted(alt.get("labels") or []):
                    bericht.h(f"{wo}: ändert nichts gegenüber dem Kontextpaket.")


# ----------------------------------------------------------------------
# Markdown-Seite
# ----------------------------------------------------------------------
_MD_TASK = re.compile(r"^\s*[-*+]\s+\[([ xX])\]\s+(.*)$")
_MD_IMAGE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)[^)]*\)")


def pruefe_markdown(bericht: Bericht, text: str, basis: str) -> None:
    if len(text) > MARKDOWN_MAX_CHARS:
        bericht.f(f"Glide liest höchstens {MARKDOWN_MAX_CHARS} Zeichen einer Seite.")
    zeilen = text.splitlines()
    erste = next((z.strip() for z in zeilen if z.strip()), "")
    if not erste:
        bericht.f("Die Datei ist leer.")
        return
    treffer = re.match(r"^#{1,6}\s+(.*)$", erste)
    if not treffer:
        bericht.w("Die erste Zeile wird zum Seitentitel; mit „# Titel“ beginnen.")
        titel = erste
    else:
        titel = treffer.group(1).strip()
    _titel(bericht, "Seitentitel", titel)
    im_code = False
    aufgaben = 0
    for nummer, zeile in enumerate(zeilen, 1):
        if re.match(r"^\s*(```|~~~)", zeile):
            im_code = not im_code
            continue
        if im_code:
            continue
        aufgabe = _MD_TASK.match(zeile)
        if aufgabe:
            aufgaben += 1
            _titel(bericht, f"Zeile {nummer} (Aufgabe)", aufgabe.group(2).strip())
        for ziel in _MD_IMAGE.findall(zeile):
            if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", ziel) and not ziel.lower().startswith("file:"):
                bericht.w(f"Zeile {nummer}: Bild {ziel} – Glide lädt nie aus dem Netz; es bleibt ein Verweis.")
            elif not ziel.lower().startswith("file:") and not os.path.isfile(os.path.join(basis, ziel)):
                bericht.w(f"Zeile {nummer}: Bilddatei {ziel} liegt nicht neben der Seite.")
        if re.search(r"<(details|summary|u|mark|span|div|br)\b", zeile, re.I):
            bericht.w(f"Zeile {nummer}: HTML übernimmt Glide nicht als Format; Markdown verwenden.")
        if re.match(r"^\s*>\s*\[!\w+\]", zeile):
            bericht.h(f"Zeile {nummer}: Hinweisblöcke werden ein Zitat.")
        if re.match(r"^#{5,6}\s", zeile):
            bericht.h(f"Zeile {nummer}: Glide kennt Überschriften bis Ebene 4.")
    if im_code:
        bericht.w("Ein Codeblock wird nicht geschlossen.")
    if aufgaben > 200:
        bericht.h(f"{aufgaben} Aufgaben in einer Seite; für reine Aufgabenlisten eine .glideexchange-Datei nehmen.")


# ----------------------------------------------------------------------
# Einstieg
# ----------------------------------------------------------------------
def pruefe_datei(pfad: str, kontext: dict | None = None) -> Bericht:
    bericht = Bericht(pfad)
    try:
        groesse = os.path.getsize(pfad)
    except OSError as fehler:
        bericht.f(f"Datei nicht lesbar: {fehler}")
        return bericht
    if groesse > MAX_BYTES:
        bericht.f(f"Die Datei ist größer als {MAX_BYTES // (1024 * 1024)} MB.")
        return bericht
    if zipfile.is_zipfile(pfad):
        try:
            with zipfile.ZipFile(pfad, "r") as archive:
                namelist = archive.namelist()
                target_json = "exchange.json" if "exchange.json" in namelist else ("data.json" if "data.json" in namelist else None)
                if not target_json:
                    bericht.f("Im Austauschpaket fehlt exchange.json.")
                    return bericht
                with archive.open(target_json, "r") as f:
                    text = f.read().decode("utf-8-sig")
        except Exception as fehler:
            bericht.f(f"Austauschpaket konnte nicht gelesen werden: {fehler}")
            return bericht
    else:
        try:
            with open(pfad, "r", encoding="utf-8-sig") as datei:
                text = datei.read()
        except (OSError, UnicodeDecodeError) as fehler:
            bericht.f(f"Die Datei ist kein lesbares UTF-8: {fehler}")
            return bericht
    if pfad.lower().endswith((".md", ".markdown", ".txt")):
        pruefe_markdown(bericht, text, os.path.dirname(os.path.abspath(pfad)))
        return bericht
    try:
        nutzlast = json.loads(text)
    except ValueError as fehler:
        bericht.f(f"Kein gültiges JSON: {fehler}")
        return bericht
    if not isinstance(nutzlast, dict):
        bericht.f("Die Datei enthält kein JSON-Objekt.")
        return bericht
    if nutzlast.get("format") == CONTEXT_FORMAT:
        bericht.f("Das ist ein Kontextpaket von Glide; die Antwort ist ein Änderungsvorschlag (mode „patch“).")
        return bericht
    if nutzlast.get("format") != FORMAT:
        bericht.f(f"format muss „{FORMAT}“ sein.")
        return bericht
    version = nutzlast.get("format_version")
    if not _ist_ganzzahl(version) or version < 1 or version > FORMAT_VERSION:
        bericht.f(f"format_version muss 1 oder {FORMAT_VERSION} sein.")
        return bericht
    modus = nutzlast.get("mode", "create")
    if modus == "patch":
        pruefe_patch(bericht, nutzlast, kontext)
    elif modus == "create":
        if kontext is not None:
            bericht.h("--kontext gilt nur für Änderungsvorschläge.")
        pruefe_create(bericht, nutzlast)
    else:
        bericht.f(f"mode {modus!r} unbekannt (create oder patch).")
    if not pfad.lower().endswith((SUFFIX, ".json", ".zip")):
        bericht.h(f"Glide bietet im Importdialog die Endung {SUFFIX} an.")
    return bericht


def _lies_kontext(pfad: str) -> dict:
    with open(pfad, "r", encoding="utf-8-sig") as datei:
        kontext = json.load(datei)
    if not isinstance(kontext, dict) or kontext.get("format") != CONTEXT_FORMAT:
        raise ValueError(f"{pfad} ist kein Kontextpaket ({CONTEXT_FORMAT}).")
    return kontext


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="glide_datei.py", description=__doc__.split("\n\n")[0])
    unter = parser.add_subparsers(dest="befehl", required=True)
    p = unter.add_parser("pruefen", help="Importdateien prüfen")
    p.add_argument("dateien", nargs="+")
    p.add_argument("--kontext", help="Kontextpaket (.glidecontext) für einen Änderungsvorschlag")
    p.add_argument("--streng", action="store_true", help="Warnungen wie Fehler werten")
    z = unter.add_parser("zeichnung", help="Pixelzeichnung aus Legende und Zeichenreihen erzeugen")
    z.add_argument("eingabe")
    z.add_argument("ausgabe")
    z.add_argument("--nur-zeichnung", action="store_true",
                   help="nur das glide.drawing-Dokument schreiben (Zeichnung (SVG/JSON) importieren …)")
    args = parser.parse_args(argv)

    if args.befehl == "zeichnung":
        try:
            with open(args.eingabe, "r", encoding="utf-8-sig") as datei:
                eingabe = json.load(datei)
            ergebnis = baue_zeichnung(eingabe) if args.nur_zeichnung else zeichnung_als_austausch(eingabe)
        except (OSError, ValueError) as fehler:
            print(f"FEHLER: {fehler}", file=sys.stderr)
            return 1
        if os.path.exists(args.ausgabe):
            print(f"FEHLER: {args.ausgabe} gibt es schon; nichts überschrieben.", file=sys.stderr)
            return 1
        with open(args.ausgabe, "w", encoding="utf-8", newline="\n") as datei:
            json.dump(ergebnis, datei, ensure_ascii=False, indent=2)
            datei.write("\n")
        print(f"Geschrieben: {args.ausgabe}")
        return 0

    kontext = None
    if args.kontext:
        try:
            kontext = _lies_kontext(args.kontext)
        except (OSError, ValueError) as fehler:
            print(f"FEHLER: {fehler}", file=sys.stderr)
            return 1
    status = 0
    for pfad in args.dateien:
        bericht = pruefe_datei(pfad, kontext)
        print(f"== {pfad}")
        for zeile in bericht.zeilen():
            print(zeile)
        print(f"Ergebnis: {len(bericht.fehler)} Fehler, {len(bericht.warnungen)} Warnungen, "
              f"{len(bericht.hinweise)} Hinweise")
        if bericht.fehler or (args.streng and bericht.warnungen):
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main())
