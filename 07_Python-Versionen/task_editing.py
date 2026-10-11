"""Feldweises Zusammenführen einer Inspektoreingabe, ohne Tk oder Mutation.

Eine gehaltene Eingabefläche darf während einer Änderung nicht neu gebaut
werden. Unberührte Felder bewahren deshalb den frischen Bestandswert.
"""
import copy
from dataclasses import dataclass

FIELDS = frozenset(("text", "kind", "importance", "color", "due", "due_time", "repeat", "labels",
                    "description", "attachments", "reminder", "planned_date", "estimated_minutes",
                    "checklist", "links", "blocked_by", "planned_time", "time_spent_minutes"))


FIELD_NAMES = {
    "text": "Titel", "kind": "Art", "importance": "Wichtigkeit", "color": "Farbe",
    "due": "Fälligkeit", "due_time": "Uhrzeit zur Fälligkeit", "repeat": "Wiederholung",
    "labels": "Labels", "description": "Beschreibung", "attachments": "Anhänge",
    "reminder": "Benachrichtigung", "planned_date": "Bearbeitungstag", "estimated_minutes": "Aufwand",
    "checklist": "Checkliste", "links": "Verknüpfungen", "blocked_by": "Voraussetzungen",
    "planned_time": "Geplante Uhrzeit", "time_spent_minutes": "Erfasste Zeit",
}


# Ein Datum und seine Uhrzeit sind eine gemeinsame Eingabe. Wiederholungen
# hängen an der Fälligkeit; getrennte zeitgleiche Änderungen nicht kombinieren.
GROUPS = (frozenset(("due", "due_time", "repeat")),
          frozenset(("planned_date", "planned_time")))


class Conflict(ValueError):
    def __init__(self, fields):
        self.fields = tuple(sorted(fields))
        super().__init__("Zwischenzeitlich geänderte Felder: " + ", ".join(FIELD_NAMES[key] for key in self.fields))


@dataclass(frozen=True)
class Edit:
    details: dict
    changed: tuple
    baseline: dict


def merge(baseline, entered, current):
    """Drei vollständige Details-Snapshots, identischer Feldvertrag.

    Rückgabe baseline ist der tatsächlich in der UI stehende Eingabestand;
    sie darf nicht durch unsichtbare fremde Änderungen ersetzt werden.
    Geänderte gemeinsame Werte sind bereits aufgelöst und kein Konflikt.
    """
    for values in (baseline, entered, current):
        if not isinstance(values, dict) or set(values) != FIELDS:
            raise ValueError("Unvollständiger Feldvertrag des Aufgabeneditors.")
    changed = tuple(sorted(key for key in FIELDS if baseline[key] != entered[key]))
    conflicts = {key for key in changed if current[key] != baseline[key] and current[key] != entered[key]}
    for group in GROUPS:
        edits = group.intersection(changed)
        concurrent = {key for key in group if current[key] != baseline[key] and current[key] != entered[key]}
        pending = {key for key in edits if current[key] != entered[key]}
        if concurrent and pending:
            conflicts.update(concurrent | pending)
    if conflicts:
        raise Conflict(conflicts)
    details = copy.deepcopy(current)
    details.update({key:copy.deepcopy(entered[key]) for key in changed})
    return Edit(details, changed, copy.deepcopy(entered))
