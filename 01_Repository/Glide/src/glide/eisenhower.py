"""Eisenhower-Einordnung ohne Tk (G02, Entscheidung D13).

Keine eigene Ansicht, sondern eine Gruppierung „Dringlichkeit × Wichtigkeit“
im vorhandenen Board, in Liste und Tabelle. Wichtig ist eine Aufgabe ab
Wichtigkeit „mittel“; dringend, wenn Fälligkeit oder Bearbeitungstag in den
nächsten zwei Tagen liegen oder schon vorbei sind. Ziehen ändert nach D02 nur,
was der Zielquadrant verlangt: die Wichtigkeit oder den Bearbeitungstag.
Eine Fälligkeit wird nie gelöscht oder verschoben.
"""
from datetime import date, timedelta

WICHTIG_AB = 2
DRINGEND_TAGE = 2
WICHTIG_SETZEN = 2
UNWICHTIG_SETZEN = 1
# (Schlüssel, Titel, wichtig, dringend)
QUADRANTEN = (
    ("q1", "Sofort · wichtig und dringend", True, True),
    ("q2", "Einplanen · wichtig, nicht dringend", True, False),
    ("q3", "Kurz halten · dringend, nicht wichtig", False, True),
    ("q4", "Später · weder wichtig noch dringend", False, False),
)
KEYS = tuple(key for key, _titel, _w, _d in QUADRANTEN)


def _tag(value):
    try:
        return date.fromisoformat(str(value)[:10]) if value else None
    except ValueError:
        return None


def grenze(today=None, tage=DRINGEND_TAGE):
    """Letzter Tag, der noch als dringend gilt."""
    return (today or date.today()) + timedelta(days=tage)


def ist_wichtig(item):
    wert = item.get("importance", 0)
    return isinstance(wert, int) and not isinstance(wert, bool) and wert >= WICHTIG_AB


def faellig_dringend(item, today=None, tage=DRINGEND_TAGE):
    tag = _tag(item.get("due"))
    return tag is not None and tag <= grenze(today, tage)


def ist_dringend(item, today=None, tage=DRINGEND_TAGE):
    tag = _tag(item.get("planned_date"))
    return faellig_dringend(item, today, tage) or (tag is not None and tag <= grenze(today, tage))


def quadrant(item, today=None, tage=DRINGEND_TAGE):
    wichtig, dringend = ist_wichtig(item), ist_dringend(item, today, tage)
    return next(key for key, _t, w, d in QUADRANTEN if w == wichtig and d == dringend)


def aenderung(item, ziel, today=None, tage=DRINGEND_TAGE):
    """Was Ablegen im Quadranten ``ziel`` ändert: (Felder, Grund).

    Felder ist ein Wörterbuch der neuen Werte (leer, wenn nichts zu tun ist);
    Grund erklärt, warum ein Ablegen nicht geht – dann ist Felder None.
    """
    today = today or date.today()
    soll = next(((w, d) for key, _t, w, d in QUADRANTEN if key == ziel), None)
    if soll is None:
        return None, "Unbekannter Quadrant."
    wichtig_soll, dringend_soll = soll
    felder = {}
    if wichtig_soll and not ist_wichtig(item):
        felder["importance"] = WICHTIG_SETZEN
    elif not wichtig_soll and ist_wichtig(item):
        felder["importance"] = UNWICHTIG_SETZEN
    if dringend_soll and not ist_dringend(item, today, tage):
        felder["planned_date"] = today.isoformat()
    elif not dringend_soll and ist_dringend(item, today, tage):
        if faellig_dringend(item, today, tage):
            return None, ("Die Fälligkeit liegt in den nächsten zwei Tagen und macht die Aufgabe dringend. "
                          "Glide ändert keine Fälligkeit durch Ziehen.")
        felder["planned_date"] = (grenze(today, tage) + timedelta(days=1)).isoformat()
    return felder, None
