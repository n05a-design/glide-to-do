# SPDX-License-Identifier: MPL-2.0
"""Zuletzt gesehene Stelle je Ansicht (PAGE-06, 27.11.2026).

Wer zwischen Seiten, Notizen und Listen wechselt, kommt an die Stelle zurück,
an der er zuletzt war. Gemerkt wird objektbezogen, nicht in Pixeln:

- Seiten und Notizen: Zeichenversatz der obersten sichtbaren Stelle und der
  Schreibmarke im Dokument. Das übersteht eine andere Fensterbreite und damit
  einen anderen Zeilenumbruch.
- Listen: Kennung der obersten sichtbaren Zeile, ersatzweise der Bruchteil
  der Bildlaufleiste.

Nur für die laufende Sitzung; nichts davon wird gespeichert. Ein
ausdrücklicher Sprung (Suche, Aufgabe öffnen) hat Vorrang – der Aufrufer
stellt die Stelle nur ohne solchen Sprung wieder her. Tk-frei.
"""

from collections import OrderedDict

LIMIT = 64


class ViewPositions:
    """Begrenzter Speicher Ansichtsschlüssel → Stelle; älteste fällt zuerst heraus."""

    def __init__(self, limit=LIMIT):
        self.limit = max(1, int(limit))
        self._stellen = OrderedDict()

    def remember(self, key, **stelle):
        if key is None:
            return
        self._stellen.pop(key, None)
        self._stellen[key] = dict(stelle)
        while len(self._stellen) > self.limit:
            self._stellen.popitem(last=False)

    def recall(self, key):
        stelle = self._stellen.get(key)
        return dict(stelle) if stelle is not None else None

    def forget(self, key):
        self._stellen.pop(key, None)

    def __len__(self):
        return len(self._stellen)


def clamp_offset(offset, length):
    """Zeichenversatz in einem Dokument der Länge `length`; ungültig → None."""
    if type(offset) is not int or offset < 0:
        return None
    return min(offset, max(0, int(length)))


def clamp_fraction(value):
    """Bruchteil der Bildlaufleiste zwischen 0 und 1; ungültig → None."""
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    if value != value:  # NaN
        return None
    return min(1.0, max(0.0, value))


def row_target(row_id, visible_rows, fraction=None):
    """Wohin eine Liste zurückscrollt: (Zeile oder None, Bruchteil oder None).

    Gibt es die gemerkte oberste Zeile noch, gilt sie; sonst der Bruchteil.
    """
    if row_id is not None and row_id in set(visible_rows or ()):
        return row_id, None
    return None, clamp_fraction(fraction)


# --- Teil 05B: Lesepositionen über Neustarts (eigene Begleitdatei) ----------
# Nicht im Aufgabenformat: `view_positions.json` neben den Einstellungen, je
# Speicherdatei getrennt. Seiten merken Kapitelanker und Abstand darin, damit
# eingefügter oder gelöschter Text davor die Stelle nicht verschiebt.
FILE_NAME = "view_positions.json"
FORMAT = "glide-view-positions"
VERSION = 1
_FELDER = {"top", "insert", "row", "fraction", "anchor", "anchor_delta", "insert_anchor", "insert_delta"}


def anchor_point(chapters, offset):
    """(Anker, Abstand) des Kapitels, in dem `offset` liegt; sonst (None, None)."""
    if type(offset) is not int:
        return None, None
    kapitel = None
    for k in chapters:
        if k.start <= offset and k.anchor:
            kapitel = k
    if kapitel is None:
        return None, None
    return kapitel.anchor, offset - kapitel.start


def resolve_point(chapters, anchor, delta, fallback, length):
    """Zeichenversatz: Anker vor gemerktem Versatz; der Abstand bleibt im Abschnitt."""
    kapitel = next((k for k in chapters if anchor and k.anchor == anchor), None)
    if kapitel is not None and type(delta) is int and delta >= 0:
        return min(kapitel.start + delta, max(kapitel.start, kapitel.section_end), max(0, int(length)))
    return clamp_offset(fallback, length)


def _sauber(stelle):
    ergebnis = {}
    for feld, wert in (stelle or {}).items():
        if feld not in _FELDER:
            continue
        if feld in ("anchor", "insert_anchor", "row"):
            if isinstance(wert, str) and 0 < len(wert) <= 256:
                ergebnis[feld] = wert
        elif feld == "fraction":
            if clamp_fraction(wert) is not None:
                ergebnis[feld] = clamp_fraction(wert)
        elif type(wert) is int and 0 <= wert <= 10_000_000:
            ergebnis[feld] = wert
    return ergebnis


def to_payload(positions, save_file, previous=None):
    """Datei-Nutzlast; Einträge anderer Speicherdateien aus `previous` bleiben."""
    andere = [e for e in ((previous or {}).get("entries") or [])
              if isinstance(e, dict) and e.get("save_file") != save_file][:LIMIT * 4]
    eigene = [{"save_file": save_file, "key": list(key), "position": _sauber(stelle)}
              for key, stelle in positions._stellen.items()
              if isinstance(key, tuple) and all(isinstance(t, str) for t in key)]
    return {"format": FORMAT, "version": VERSION, "entries": andere + eigene}


def load_payload(positions, payload, save_file):
    for eintrag in (payload or {}).get("entries") or []:
        if not isinstance(eintrag, dict) or eintrag.get("save_file") != save_file:
            continue
        key = eintrag.get("key")
        if (isinstance(key, list) and 1 < len(key) <= 3 and all(isinstance(t, str) and t for t in key)
                and key[0] in ("page", "list")):
            positions.remember(tuple(key), **_sauber(eintrag.get("position")))
