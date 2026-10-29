"""Feldweises Zusammenführen einer Inspektoreingabe, ohne Tk oder Mutation.

Eine gehaltene Eingabefläche darf während einer Änderung nicht neu gebaut
werden. Unberührte Felder bewahren deshalb den frischen Bestandswert.
"""
import copy
from datetime import date
from dataclasses import dataclass


class ChangeRecord:
    """Gemeinsamer Ergebniszustand vorhandener Punkt-/Seitenleistenmutationen."""

    __slots__ = ('changed', 'focus_id', 'selection', 'saved', 'save_result', 'changed_ids', 'changed_lists')

    def __init__(self, selection):
        self.changed = False
        self.saved = None
        self.save_result = None
        self.focus_id = None
        self.selection = list(selection)
        self.changed_ids = set()
        self.changed_lists = set()

    def mark(self, focus_id=None):
        self.changed = True
        if focus_id is not None:
            self.focus_id = focus_id
            self.changed_ids.add(focus_id)
        else:
            self.changed_ids.update(self.selection)

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


def new_label_name(labels, name, *, max_labels, max_length):
    """Nach jeder Dialoggrenze am aktuellen Bestand prüfen, ohne Mutation."""
    if len(labels) >= max_labels:
        raise ValueError(f"Es sind höchstens {max_labels} Labels möglich.")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Bitte einen Namen eingeben.")
    name = name.strip()
    if len(name) > max_length:
        raise ValueError(f"Labelnamen dürfen höchstens {max_length} Zeichen lang sein – "
                         "so viel zeigt die Labelspalte einer Liste.")
    if any(str(label.get('name') or '').strip().casefold() == name.casefold() for label in labels):
        raise ValueError("Es gibt bereits ein Label mit diesem Namen.")
    return name


def completed_ids(items, schedulable):
    """Erledigte Blätter zuerst; Gruppen und Eltern mit offenen Kindern bleiben."""
    removed = []

    def visit(values):
        kept = 0
        for item in values:
            children_kept = visit(item.get('children', []))
            if schedulable(item) and item.get('done') and not children_kept:
                removed.append(item['id'])
            else:
                kept += 1
        return kept

    visit(items)
    return tuple(removed)


def remove_planned(items, identities):
    """Eine tiefe Kopie; jeder entfernte Punkt genau einmal samt Herkunft.

    Kinder werden vor Eltern entnommen. Ein entfernter Elternpunkt darf seine
    bereits einzeln entnommenen Kinder nicht noch einmal im Payload enthalten.
    """
    selected, removed = set(identities), []

    def visit(values, parent_id=None):
        kept = []
        for index, item in enumerate(values):
            item['children'] = visit(item.get('children', []), item['id'])
            if item['id'] in selected:
                removed.append((item, parent_id, index))
            else:
                kept.append(item)
        return kept

    return visit(copy.deepcopy(items)), removed


def displaced_payloads(existing, incoming, limit):
    """Vom bestehenden Neueste-zuerst-Papierkorblimit verdrängte Payloads.

    `incoming` steht in Einfügereihenfolge, `existing` bereits neueste zuerst.
    Nur lesen; der Aufrufer ermittelt daraus erlaubte ID-Verluste des Wächters.
    """
    if type(limit) is not int or limit < 1:
        raise ValueError('Ungültige Papierkorbgrenze.')
    return list(incoming[:max(0, len(incoming)-limit)]) + list(existing[max(0, limit-len(incoming)):])


def batch_plan(items, operation, value=None, *, max_labels=50, max_estimated=60000):
    """Explizite Mehrfachänderung ohne Mutation; ein ungültiges Ziel stoppt alles.

    Hinzufügen/Entfernen sind idempotent. Unterschiedliche vorhandene Labels
    bleiben erhalten; der Aufrufer liefert ausschließlich reguläre Label-IDs.
    """
    if operation not in ('importance', 'label_add', 'label_remove', 'due', 'estimated_minutes'):
        raise ValueError('Unbekannte Mehrfachaktion.')
    if operation == 'importance' and (type(value) is not int or not 0 <= value <= 3):
        raise ValueError('Die Wichtigkeit muss zwischen 0 und 3 liegen.')
    if operation.startswith('label_') and (not isinstance(value, str) or not value):
        raise ValueError('Kein gültiges Label ausgewählt.')
    if operation == 'due' and value is not None:
        try:
            valid = isinstance(value, str) and date.fromisoformat(value).isoformat() == value
        except ValueError:
            valid = False
        if not valid:
            raise ValueError('Die Fälligkeit muss ein gültiges Datum im Format JJJJ-MM-TT sein.')
    if operation == 'estimated_minutes' and value is not None:
        if type(value) is not int or not 1 <= value <= max_estimated:
            raise ValueError(f'Der Aufwand muss zwischen 1 und {max_estimated} ganzen Minuten liegen.')
    result = {}
    for item in items:
        identity = item.get('id')
        if not isinstance(identity, str) or not identity or item.get('done'):
            raise ValueError('Die Auswahl enthält keine offene Aufgabe mehr.')
        if operation == 'importance':
            if item.get('importance', 0) != value:
                result[identity] = {'importance': value}
            continue
        if operation in ('due', 'estimated_minutes'):
            changes = {}
            if item.get(operation) != value:
                if operation == 'due' and item.get('repeat'):
                    raise ValueError('Die Fälligkeit von Serien bitte einzeln bearbeiten; die Auswahl bleibt unverändert.')
                changes[operation] = value
            if operation == 'due' and value is None and item.get('due_time'):
                changes['due_time'] = None
            if changes:
                result[identity] = changes
            continue
        labels = list(item.get('labels') or [])
        updated = [label for label in labels if label != value] if operation == 'label_remove' else labels[:]
        if operation == 'label_add' and value not in updated:
            if len(updated) >= max_labels:
                raise ValueError('Mindestens eine Aufgabe hat bereits die maximale Anzahl Labels.')
            updated.append(value)
        if labels != updated:
            result[identity] = {'labels': updated}
    return result


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
