"""Durchsuchbare Seiten- und Blockaktionen ohne Tk (E-U3 A, D55, 23.10.2026).

Seite und Block behalten ihre bisherigen Menüs. Die eingebettete Auswahl liest
dieselben Einträge (Beschriftung, Pfad, Zustand) aus dem fertigen Menü und
führt beim Wählen genau diesen Menüeintrag aus. So gibt es keine zweite
Befehlsliste, die auseinanderlaufen könnte. Dieses Modul ordnet, filtert und
erklärt gesperrte Einträge; den Menübaum liest die Oberfläche.

Eine Zeile aus der Oberfläche ist ein Tupel
``(schluessel, beschriftung, pfad, aktiv, gruppe, art)``:

- ``schluessel``: Menüindizes vom Wurzelmenü bis zum Eintrag,
- ``pfad``: Beschriftungen der Untermenüs davor,
- ``gruppe``: Nummer des durch Trennlinien gebildeten Abschnitts der obersten Ebene,
- ``art``: ``"command"`` oder ``"submenu"`` (Untermenü, das sich erst beim
  Öffnen füllt und deshalb als Ganzes gewählt wird).
"""

from dataclasses import dataclass

import content_search

CHECK_MARK = "✓"
PATH_SEPARATOR = " › "
FALLBACK_SECTION = "Weitere"
MAX_ENTRIES = 240

# Gründe für gesperrte Einträge. Die Menüs kennen nur „gesperrt“; die Auswahl
# sagt zusätzlich, warum (Design Richtlinien: deaktiviert mit Grund).
READ_ONLY_REASON = "Schreibgeschützter Bestand · nur ansehen"
SELECTION_REASON = "Zuerst Text markieren"
LINE_REASON = "Bild- und Tabellenzeilen bleiben an ihrem Platz; ein Bild über sein eigenes Menü verschieben"
OWN_TASK_REASON = "Nur für eine Aufgabe dieser Seite an der Schreibmarke"
NO_COVER_REASON = "Die Seite hat kein Titelbild"
NO_HEADINGS_REASON = "Die Seite hat noch keine Überschriften"
EMPTY_REASON = "Keine Einträge vorhanden"
DEFAULT_REASON = "Gerade nicht verfügbar"

# Reine Platzhalter eines leeren Untermenüs sind keine Aktion und entfallen.
PLACEHOLDER_LABELS = frozenset({"Keine", "Kein Objekt ausgewählt"})
_SELECTION_LABELS = frozenset({"Ausschneiden", "Kopieren"})
_LINE_LABELS = frozenset({"Zeile nach oben", "Zeile nach unten", "Zeile duplizieren", "Zeile löschen"})
_WRITE_LABELS = frozenset({"Aufgabe verknüpfen …", "In Liste übernehmen …"})


@dataclass(frozen=True)
class Entry:
    """Ein wählbarer Menüeintrag mit Anzeige- und Ausführungsangaben."""

    key: tuple
    label: str
    path: tuple = ()
    enabled: bool = True
    checked: bool = False
    reason: str = ""
    section: str = ""
    kind: str = "command"

    @property
    def location(self):
        """Pfad unterhalb des Abschnitts, etwa „Gliederung“ in einer flachen Trefferliste."""
        return PATH_SEPARATOR.join(self.path)


def clean_label(raw):
    """Beschriftung ohne Häkchen und Ausrichtungsleerzeichen; dazu, ob ein Häkchen stand."""
    text = str(raw or "")
    stripped = text.lstrip()
    checked = stripped.startswith(CHECK_MARK)
    if checked:
        stripped = stripped[len(CHECK_MARK):]
    return " ".join(stripped.split()), checked


def reason_for(label, path, context=None):
    """Verständlicher Grund für einen gesperrten Eintrag."""
    context = context or {}
    path = tuple(path or ())
    if label in ("Keine", "Kein Objekt ausgewählt"):
        return EMPTY_REASON
    if context.get("read_only") and (label in _WRITE_LABELS or label in _LINE_LABELS or
                                      label == "Titelbild entfernen"):
        return READ_ONLY_REASON
    if label in _SELECTION_LABELS or (path and path[0] == "Formatieren"):
        return SELECTION_REASON
    if label in _LINE_LABELS:
        return LINE_REASON
    if label == "In Liste übernehmen …":
        return OWN_TASK_REASON
    if label == "Titelbild entfernen":
        return NO_COVER_REASON
    if label == "Gliederung":
        return NO_HEADINGS_REASON
    if context.get("read_only"):
        return READ_ONLY_REASON
    return DEFAULT_REASON


def entries(rows, sections=(), context=None, skip=()):
    """Zeilen der Oberfläche in Einträge mit Abschnitt, Häkchen und Sperrgrund.

    ``sections`` benennt die durch Trennlinien gebildeten Abschnitte der
    obersten Ebene; Einträge in Untermenüs gehören zum Abschnitt ihres ersten
    Untermenüs („Umwandeln in“, „Formatieren“, „Gliederung“).
    """
    result = []
    skip = set(skip)
    for row in rows:
        key, raw, path, enabled, group, kind = row
        label, checked = clean_label(raw)
        path = tuple(clean_label(part)[0] for part in (path or ()))
        if not label or label in skip or (not enabled and label in PLACEHOLDER_LABELS):
            continue
        if path:
            section = path[0]
        elif 0 <= int(group) < len(sections):
            section = sections[int(group)]
        else:
            section = FALLBACK_SECTION
        result.append(Entry(key=tuple(key), label=label, path=path, enabled=bool(enabled), checked=checked,
                            reason="" if enabled else reason_for(label, path, context),
                            section=section, kind=kind if kind in ("command", "submenu") else "command"))
        if len(result) >= MAX_ENTRIES:
            break
    return result


def search(values, query):
    """Treffer zur Eingabe: Beschriftung zuerst, dann Pfad und Abschnitt.

    Reihenfolge wie die Befehlspalette (Titel beginnt mit der Eingabe, ein Wort
    beginnt damit, irgendwo enthalten) und innerhalb gleicher Güte die
    Menüreihenfolge. Umlaute zählen gleich ae/oe/ue/ss.
    """
    key = content_search.search_key(query)
    values = list(values)
    if not key:
        return values
    ranked = []
    for position, entry in enumerate(values):
        rank = content_search.title_rank(entry.label, key)
        if rank is None and key in content_search.search_key(" ".join((entry.section,) + entry.path)):
            rank = 3
        if rank is not None:
            ranked.append((rank, position, entry))
    ranked.sort(key=lambda value: (value[0], value[1]))
    return [entry for _rank, _position, entry in ranked]


def grouped(values, order=()):
    """Einträge je Abschnitt; ``order`` stellt gewünschte Abschnitte nach vorn.

    Innerhalb eines Abschnitts bleibt die Reihenfolge erhalten. Abschnitte, die
    ``order`` nicht nennt, folgen in der Reihenfolge ihres ersten Eintrags.
    """
    groups = {}
    for entry in values:
        groups.setdefault(entry.section, []).append(entry)
    first = [name for name in order if name in groups]
    rest = [name for name in groups if name not in first]
    return [(name, groups[name]) for name in first + rest]


def first_enabled(values):
    """Erster wählbarer Eintrag oder None (Startauswahl der Liste)."""
    return next((entry for entry in values if entry.enabled), None)


def summary(values, query):
    """Kurze Zustandszeile unter der Liste."""
    if not values:
        return "Keine passende Aktion" if str(query or "").strip() else "Keine Aktionen"
    usable = sum(1 for entry in values if entry.enabled)
    if usable == len(values):
        return f"{usable} Aktionen" if usable != 1 else "1 Aktion"
    return f"{usable} von {len(values)} Aktionen verfügbar"


def header_affordances(entry, read_only=False):
    """Welche zurückhaltenden Kopfverweise eine Seite über dem Titel zeigt (Rang 3).

    Nur, was fehlt und änderbar ist: ``("icon", "cover")`` in fester Reihenfolge.
    Archivierte Seiten und schreibgeschützte Bestände zeigen keine.
    """
    if not isinstance(entry, dict) or read_only or entry.get("archived"):
        return ()
    result = []
    if not isinstance(entry.get("icon"), dict):
        result.append("icon")
    if not entry.get("cover"):
        result.append("cover")
    return tuple(result)
