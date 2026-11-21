# SPDX-License-Identifier: MPL-2.0
"""Durchsuchbare Seiten- und Blockaktionen ohne Tk (E-U3 A, D55, 23.10.2026).

Seite und Block behalten ihre bisherigen Menüs. Die eingebettete Auswahl liest
dieselben Einträge (Beschriftung, Pfad, Zustand) aus dem fertigen Menü und
führt beim Wählen genau diesen Menüeintrag aus. So gibt es keine zweite
Befehlsliste, die auseinanderlaufen könnte. Dieses Modul ordnet, filtert und
erklärt gesperrte Einträge; den Menübaum liest die Oberfläche. Seit V1.69
liegen Eintragsmodell, Ordnen, Suchen und Gruppieren in
`glide_shell.action_picker` (D98); hier bleiben Sperrgründe, Platzhalter,
Zustandstexte, Kopfverweise und die Glide-Suchsemantik aus `content_search`.

Eine Zeile aus der Oberfläche ist ein Tupel
``(schluessel, beschriftung, pfad, aktiv, gruppe, art)``:

- ``schluessel``: Menüindizes vom Wurzelmenü bis zum Eintrag,
- ``pfad``: Beschriftungen der Untermenüs davor,
- ``gruppe``: Nummer des durch Trennlinien gebildeten Abschnitts der obersten Ebene,
- ``art``: ``"command"`` oder ``"submenu"`` (Untermenü, das sich erst beim
  Öffnen füllt und deshalb als Ganzes gewählt wird).
"""

import content_search
from glide_shell import action_picker as _menu
from glide_shell.action_picker import (CHECK_MARK, CHECK_PAD, MAX_ENTRIES, PATH_SEPARATOR, Entry,  # noqa: F401
                                       check_label, clean_label, first_enabled, grouped)

FALLBACK_SECTION = "Weitere"

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
SIDE_VIEW_REASON = "Zuerst eine Nebenansicht öffnen"
SIDE_LOOKUP_LABEL = "Markierung in Nebenansicht suchen"

# Reine Platzhalter eines leeren Untermenüs sind keine Aktion und entfallen.
PLACEHOLDER_LABELS = frozenset({"Keine", "Kein Objekt ausgewählt"})
_SELECTION_LABELS = frozenset({"Ausschneiden", "Kopieren"})
_LINE_LABELS = frozenset({"Zeile nach oben", "Zeile nach unten", "Zeile duplizieren", "Zeile löschen"})
_WRITE_LABELS = frozenset({"Aufgabe verknüpfen …", "In Liste übernehmen …"})


def reason_for(label, path, context=None):
    """Verständlicher Grund für einen gesperrten Eintrag."""
    context = context or {}
    path = tuple(path or ())
    if label in ("Keine", "Kein Objekt ausgewählt"):
        return EMPTY_REASON
    if label == SIDE_LOOKUP_LABEL:
        # Lesend, deshalb auch im Schreibschutz; gesperrt nur ohne Nebenansicht oder Markierung.
        return SELECTION_REASON if context.get("side_view") else SIDE_VIEW_REASON
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
    return _menu.entries(rows, sections, skip=skip, placeholders=PLACEHOLDER_LABELS,
                         reason=lambda label, path: reason_for(label, path, context),
                         fallback_section=FALLBACK_SECTION)


def search(values, query):
    """Treffer zur Eingabe: Beschriftung zuerst, dann Pfad und Abschnitt.

    Reihenfolge wie die Befehlspalette (Titel beginnt mit der Eingabe, ein Wort
    beginnt damit, irgendwo enthalten) und innerhalb gleicher Güte die
    Menüreihenfolge. Umlaute zählen gleich ae/oe/ue/ss.
    """
    return _menu.search(values, query, content_search.search_key)


def summary(values, query):
    """Kurze Zustandszeile unter der Liste."""
    if not values:
        return "Keine passende Aktion" if str(query or "").strip() else "Keine Aktionen"
    usable, total = _menu.counts(values)
    if usable == total:
        return f"{usable} Aktionen" if usable != 1 else "1 Aktion"
    return f"{usable} von {total} Aktionen verfügbar"


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
