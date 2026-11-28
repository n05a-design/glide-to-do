# SPDX-License-Identifier: MPL-2.0
"""Kapitel einer Seite als Projektion ihrer Überschriften (PAGE-02, Master-Serie Teil 03).

Tk-frei nach D17. Eine Seite speichert ihren Inhalt als Dokument
`{"text", "spans", "links", "images"}`; Überschriften sind Zeilen mit einem
Bereich `h1`–`h4`. Ein **Kapitel** ist eine solche Überschrift mit ihrem
**Abschnitt**: von der Überschriftenzeile bis vor die nächste Überschrift
gleicher oder höherer Ebene. Kapitel bleiben Teil derselben Seite; es entsteht
keine Unterseite und keine zweite Inhaltsstruktur.

Regeln:
1. Kennung im Format 26: `key` aus Ebene, Titel und laufender Nummer gleicher
   Titel (`"2:Architektur#1"`). Sie ist innerhalb einer Sitzung eindeutig, aber
   nicht stabil gegen Umbenennen; eine dauerhafte Kennung braucht einen
   persistenten Anker (`anchor:<hex>`, Aufgabenformat 27, siehe `ensure_anchors`).
2. Jede Änderung ist eine reine Funktion Dokument → neues Dokument; alle Bereiche
   (Format, Links, Bilder, Aufgaben) wandern mit ihrem Text.
3. „Auflösen“ entfernt nur die Überschriftenauszeichnung; der Text bleibt.
   Löschen eines ganzen Abschnitts bietet dieses Modul bewusst nicht an.
4. Verschieben bewegt immer den ganzen Abschnitt mit allen Unterkapiteln und
   nur innerhalb derselben Ebene unter demselben Elternkapitel.
"""
from __future__ import annotations

import copy
import re
import uuid
from collections import namedtuple

HEADING_LEVELS = {"h1": 1, "h2": 2, "h3": 3, "h4": 4}
TOGGLE_PREFIXES = ("▾ ", "▸ ")
SIDEBAR_MAX_LEVEL = 3
SIDEBAR_MAX_CHAPTERS = 60

Chapter = namedtuple("Chapter", "index key level title line start end section_end parent anchor",
                     defaults=(None,))

# Stabiler Kapitelanker (Aufgabenformat 27, Inhaberfreigabe 27.11.2026, Teil 05):
# ein Bereich `{"tag": "anchor:<32 hex>", "start": s, "end": e}` über der ganzen
# Überschriftenzeile. Er wandert wie jeder Bereich mit dem Text (Umbenennen,
# Verschieben, Ebene), verschwindet beim Auflösen und wird beim Duplizieren neu
# vergeben. Ältere Fassungen öffnen Format 27 nur lesend und verlieren ihn nicht.
ANCHOR_PREFIX = "anchor:"
ANCHOR_TAG = re.compile(r"^anchor:[0-9a-f]{32}$")


def anchor_id(tag):
    return tag[len(ANCHOR_PREFIX):] if isinstance(tag, str) and ANCHOR_TAG.match(tag) else None


def _lines(text):
    """(Zeilennummer ab 1, Start, Ende ohne Zeilenumbruch)."""
    start = 0
    for nummer, zeile in enumerate(text.split("\n"), 1):
        yield nummer, start, start + len(zeile)
        start += len(zeile) + 1


def _heading_level(spans, start, end):
    beste = None
    for span in spans:
        stufe = HEADING_LEVELS.get(span.get("tag"))
        if stufe and span["start"] <= start < max(span["end"], start + 1) and span["end"] > start:
            beste = stufe if beste is None else min(beste, stufe)
    return beste


def clean_title(text):
    text = text.strip()
    for praefix in TOGGLE_PREFIXES:
        if text.startswith(praefix.strip()):
            text = text[len(praefix.strip()):].strip()
    return text


def outline(document):
    """Alle Kapitel des Dokuments in Textreihenfolge."""
    text = (document or {}).get("text") or ""
    spans = (document or {}).get("spans") or []
    roh = []
    for nummer, start, ende in _lines(text):
        if start == ende:
            continue
        stufe = _heading_level(spans, start, ende)
        titel = clean_title(text[start:ende])
        if stufe and titel:
            anker = next((anchor_id(s.get("tag")) for s in spans
                          if anchor_id(s.get("tag")) and _on_line(s, start, ende)), None)
            roh.append((stufe, titel, nummer, start, ende, anker))
    kapitel, gesehen, stapel, vergeben = [], {}, [], set()
    for index, (stufe, titel, nummer, start, ende, anker) in enumerate(roh):
        abschnitt_ende = next((r[3] for r in roh[index + 1:] if r[0] <= stufe), len(text))
        while stapel and kapitel[stapel[-1]].level >= stufe:
            stapel.pop()
        eltern = stapel[-1] if stapel else None
        zaehler = gesehen.get((stufe, titel), 0) + 1
        gesehen[(stufe, titel)] = zaehler
        if anker in vergeben:
            anker = None  # doppelte Kennung: nur die erste gilt (ensure_anchors erneuert)
        if anker:
            vergeben.add(anker)
        schluessel = anker or f"{stufe}:{titel}#{zaehler}"
        kapitel.append(Chapter(index, schluessel, stufe, titel, nummer, start, ende,
                               abschnitt_ende, eltern, anker))
        stapel.append(index)
    return kapitel


def tree(chapters, max_level=SIDEBAR_MAX_LEVEL, limit=SIDEBAR_MAX_CHAPTERS):
    """[(Kapitel, Kinder)] bis `max_level`, höchstens `limit` Kapitel insgesamt."""
    sichtbar = [k for k in chapters if k.level <= max_level][:limit]
    knoten = {k.index: (k, []) for k in sichtbar}
    wurzeln = []
    for k in sichtbar:
        eltern = k.parent
        while eltern is not None and eltern not in knoten:
            eltern = chapters[eltern].parent
        (knoten[eltern][1] if eltern is not None else wurzeln).append(knoten[k.index])
    return wurzeln


def find(chapters, key):
    return next((k for k in chapters if k.key == key), None)


def current(chapters, offset):
    """Kapitel, in dessen Abschnitt `offset` liegt (tiefstes zuerst), sonst None."""
    treffer = None
    for k in chapters:
        if k.start <= offset < k.section_end and (treffer is None or k.level >= treffer.level):
            treffer = k
    return treffer


def _clone(document):
    neu = copy.deepcopy(document or {})
    neu.setdefault("text", "")
    neu.setdefault("spans", [])
    return neu


def _replace(document, start, end, text):
    """Ersetzt text[start:end]; Bereiche danach verschieben sich, Bereiche darin werden geklemmt."""
    neu = _clone(document)
    alt = neu["text"]
    delta = len(text) - (end - start)
    neu["text"] = alt[:start] + text + alt[end:]
    spans = []
    for span in neu["spans"]:
        a, b = span["start"], span["end"]
        if a >= end:
            a, b = a + delta, b + delta
        elif b > start:
            a = min(a, start + len(text)) if a > start else a
            b = b + delta if b >= end else min(b, start + len(text))
        if b > a:
            spans.append(dict(span, start=a, end=b))
    neu["spans"] = spans
    return neu


def rename(document, chapter, title):
    title = " ".join(str(title).split())
    if not title:
        raise ValueError("Kapitelname darf nicht leer sein")
    zeile = document["text"][chapter.start:chapter.end]
    praefix = next((p for p in TOGGLE_PREFIXES if zeile.startswith(p)), "")
    return _replace(document, chapter.start + len(praefix), chapter.end, title)


def dissolve(document, chapter):
    """Überschrift wird Text; Inhalt und übrige Formate bleiben."""
    neu = _clone(document)
    neu["spans"] = [s for s in neu["spans"]
                    if not (s.get("tag") in HEADING_LEVELS and s["start"] <= chapter.start < s["end"])]
    return neu


def set_level(document, chapter, level):
    if level not in (1, 2, 3, 4):
        raise ValueError("Ebene 1 bis 4")
    neu = dissolve(document, chapter)
    neu["spans"].append({"tag": f"h{level}", "start": chapter.start, "end": chapter.end})
    neu["spans"].sort(key=lambda s: (s["start"], s["end"], s["tag"]))
    return neu


def sibling(chapters, chapter, direction):
    """Nachbarkapitel gleicher Ebene unter demselben Elternkapitel oder None."""
    geschwister = [k for k in chapters if k.parent == chapter.parent and k.level == chapter.level]
    stelle = geschwister.index(chapter) + direction
    return geschwister[stelle] if 0 <= stelle < len(geschwister) else None


def move(document, chapters, chapter, direction):
    """Vertauscht den Abschnitt mit dem vorigen (-1) oder nächsten (+1) Geschwisterabschnitt."""
    nachbar = sibling(chapters, chapter, direction)
    if nachbar is None:
        return None
    erster, zweiter = (nachbar, chapter) if direction < 0 else (chapter, nachbar)
    neu = _clone(document)
    text = neu["text"]
    ergaenzt = not text.endswith("\n")
    if ergaenzt:
        text += "\n"
    a0, a1 = erster.start, erster.section_end + (1 if ergaenzt and erster.section_end == len(neu["text"]) else 0)
    b0, b1 = zweiter.start, zweiter.section_end + (1 if ergaenzt and zweiter.section_end == len(neu["text"]) else 0)
    if a1 != b0:
        raise ValueError("Abschnitte liegen nicht nebeneinander")
    teil_a, teil_b = text[a0:a1], text[b0:b1]
    text = text[:a0] + teil_b + teil_a + text[b1:]
    spans = []
    for span in neu["spans"]:
        for s, e, verschiebung in ((max(span["start"], a0), min(span["end"], a1), len(teil_b)),
                                   (max(span["start"], b0), min(span["end"], b1), -len(teil_a))):
            if s < e:
                spans.append(dict(span, start=s + verschiebung, end=e + verschiebung))
        if span["end"] <= a0 or span["start"] >= b1:
            spans.append(dict(span))
        else:
            if span["start"] < a0:
                spans.append(dict(span, end=a0))
            if span["end"] > b1:
                spans.append(dict(span, start=b1))
    if ergaenzt:
        text = text[:-1]
        spans = [dict(s, end=min(s["end"], len(text))) for s in spans if s["start"] < len(text)]
    neu["text"] = text
    neu["spans"] = sorted((s for s in spans if s["end"] > s["start"]), key=lambda s: (s["start"], s["end"], s["tag"]))
    return neu


def validate(document):
    """Strukturbefunde (leere Kapitelnamen gibt es durch `outline` nicht): Bereiche im Text und geordnet."""
    befunde = []
    laenge = len((document or {}).get("text") or "")
    for span in (document or {}).get("spans") or []:
        if not (0 <= span["start"] < span["end"] <= laenge):
            befunde.append(f"Bereich außerhalb des Textes: {span}")
    return befunde


def _on_line(span, start, ende):
    """Berührt der Bereich die Zeile einschließlich ihres Zeilenumbruchs?"""
    return span["start"] <= ende and span["end"] > start


def ensure_anchors(document, new_id=lambda: uuid.uuid4().hex):
    """Genau ein gültiger Anker je Überschriftenzeile; (Dokument, geändert).

    Anker außerhalb von Überschriftenzeilen fallen weg (aufgelöste Kapitel),
    doppelte Kennungen behalten nur ihr erstes Vorkommen. Bestehende
    Kennungen bleiben erhalten; reine Funktion.
    """
    if not isinstance(document, dict):
        return document, False
    text = document.get("text") or ""
    spans = [s for s in (document.get("spans") or []) if isinstance(s, dict)]
    andere = [s for s in spans if not str(s.get("tag", "")).startswith(ANCHOR_PREFIX)]
    anker = [s for s in spans if anchor_id(s.get("tag"))]
    neu, vergeben = [], set()
    for _nummer, start, ende in _lines(text):
        if start == ende or not _heading_level(andere, start, ende) or not clean_title(text[start:ende]):
            continue
        vorhanden = next((anchor_id(s["tag"]) for s in anker
                          if _on_line(s, start, ende) and anchor_id(s["tag"]) not in vergeben), None)
        kennung = vorhanden or new_id()
        while kennung in vergeben or not re.fullmatch(r"[0-9a-f]{32}", kennung):
            kennung = uuid.uuid4().hex
        vergeben.add(kennung)
        # Wie die Zeilenformate schließt der Anker den Zeilenumbruch ein: Wer die
        # Überschrift ganz neu tippt, behält ihre Kennung.
        neu.append({"tag": ANCHOR_PREFIX + kennung, "start": start, "end": min(ende + 1, len(text))})
    alt = sorted(({"tag": s["tag"], "start": s["start"], "end": s["end"]} for s in anker),
                 key=lambda s: (s["start"], s["end"], s["tag"]))
    if alt == neu and len(anker) == len(neu):
        return document, False
    result = dict(document)
    result["spans"] = sorted(andere + neu, key=lambda s: (s["start"], s["end"], s["tag"]))
    return result, True


def renew_anchors(document):
    """Neue Kennungen für eine Kopie (Duplizieren); Rückgabe (Dokument, alt → neu)."""
    if not isinstance(document, dict):
        return document, {}
    zuordnung = {}
    spans = []
    for span in document.get("spans") or []:
        alt = anchor_id(span.get("tag")) if isinstance(span, dict) else None
        if alt:
            zuordnung.setdefault(alt, uuid.uuid4().hex)
            span = dict(span, tag=ANCHOR_PREFIX + zuordnung[alt])
        spans.append(span)
    return dict(document, spans=spans), zuordnung


def find_anchor(chapters, anchor):
    return next((k for k in chapters if anchor and k.anchor == anchor), None)
