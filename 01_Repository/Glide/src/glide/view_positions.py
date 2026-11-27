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
