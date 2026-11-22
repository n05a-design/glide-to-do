# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 13: durchsuchbare Aktionsauswahl aus einem fertigen Menü, ohne Tk (D98).

Eine eingebettete Auswahl liest dieselben Einträge (Beschriftung, Pfad,
Zustand) aus dem fertigen Tk-Menü und führt beim Wählen genau diesen
Menüeintrag aus. So gibt es keine zweite Befehlsliste. Dieses Modul ordnet,
filtert und gruppiert; den Menübaum liest die Oberfläche.

Eine Zeile der Oberfläche ist ein Tupel
``(schluessel, beschriftung, pfad, aktiv, gruppe, art)``:

- ``schluessel``: Menüindizes vom Wurzelmenü bis zum Eintrag,
- ``pfad``: Beschriftungen der Untermenüs davor,
- ``gruppe``: Nummer des durch Trennlinien gebildeten Abschnitts der obersten Ebene,
- ``art``: ``"command"`` oder ``"submenu"``.

Sperrgründe, Platzhalter, Abschnittsnamen und Zustandstexte liefert der
Host; die Suche nimmt optional seinen Suchschlüssel (Glide: Umlaute wie
ae/oe/ue/ss). Vertrag: `tests/unit/test_shell_d98.py`.
"""

from dataclasses import dataclass
import unicodedata

CHECK_MARK = "✓"
# Vier Leerzeichen sind in der macOS-Menüschrift genau so breit wie „✓ “
# (15 px), in DejaVu Sans 1 px schmaler; so beginnen alle Beschriftungen an einer Kante.
CHECK_PAD = "    "
PATH_SEPARATOR = " › "
MAX_ENTRIES = 240
FALLBACK_SECTION = "More"


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


def check_label(label, checked):
    """Menübeschriftung mit Häkchenspalte: „✓ “ oder gleich breite Leerstelle davor."""
    return (CHECK_MARK + " " if checked else CHECK_PAD) + label


def clean_label(raw):
    """Beschriftung ohne Häkchen und Ausrichtungsleerzeichen; dazu, ob ein Häkchen stand."""
    text = str(raw or "")
    stripped = text.lstrip()
    checked = stripped.startswith(CHECK_MARK)
    if checked:
        stripped = stripped[len(CHECK_MARK):]
    return " ".join(stripped.split()), checked


def entries(rows, sections=(), skip=(), placeholders=(), reason=None, fallback_section=FALLBACK_SECTION,
            limit=MAX_ENTRIES):
    """Zeilen der Oberfläche in Einträge mit Abschnitt, Häkchen und Sperrgrund.

    ``sections`` benennt die Abschnitte der obersten Ebene; Einträge in
    Untermenüs gehören zum Abschnitt ihres ersten Untermenüs. Gesperrte
    ``placeholders`` (etwa „Keine“) entfallen. ``reason(label, path)``
    erklärt einen gesperrten Eintrag.
    """
    result = []
    skip, placeholders = set(skip), set(placeholders)
    for row in rows:
        key, raw, path, enabled, group, kind = row
        label, checked = clean_label(raw)
        path = tuple(clean_label(part)[0] for part in (path or ()))
        if not label or label in skip or (not enabled and label in placeholders):
            continue
        if path:
            section = path[0]
        elif 0 <= int(group) < len(sections):
            section = sections[int(group)]
        else:
            section = fallback_section
        why = "" if enabled or reason is None else reason(label, path)
        result.append(Entry(key=tuple(key), label=label, path=path, enabled=bool(enabled), checked=checked,
                            reason=why, section=section, kind=kind if kind in ("command", "submenu") else "command"))
        if len(result) >= limit:
            break
    return result


def plain_key(text):
    """Einfacher Suchschlüssel: NFC, Groß/Klein egal, Leerraum zusammengefasst."""
    return unicodedata.normalize("NFC", " ".join(str(text or "").split())).casefold()


def label_rank(text, key, search_key=plain_key):
    """0: beginnt mit der Eingabe, 1: ein Wort beginnt damit, 2: enthalten, None: kein Treffer."""
    value = search_key(text)
    if not key or value.startswith(key):
        return 0
    if any(word.startswith(key) for word in value.split()):
        return 1
    return 2 if key in value else None


def search(values, query, search_key=plain_key):
    """Treffer zur Eingabe: Beschriftung zuerst, dann Pfad und Abschnitt.

    Innerhalb gleicher Güte bleibt die Menüreihenfolge.
    """
    key = search_key(query)
    values = list(values)
    if not key:
        return values
    ranked = []
    for position, entry in enumerate(values):
        rank = label_rank(entry.label, key, search_key)
        if rank is None and key in search_key(" ".join((entry.section,) + entry.path)):
            rank = 3
        if rank is not None:
            ranked.append((rank, position, entry))
    ranked.sort(key=lambda value: (value[0], value[1]))
    return [entry for _rank, _position, entry in ranked]


def grouped(values, order=()):
    """Einträge je Abschnitt; ``order`` stellt gewünschte Abschnitte nach vorn."""
    groups = {}
    for entry in values:
        groups.setdefault(entry.section, []).append(entry)
    first = [name for name in order if name in groups]
    rest = [name for name in groups if name not in first]
    return [(name, groups[name]) for name in first + rest]


def first_enabled(values):
    """Erster wählbarer Eintrag oder None (Startauswahl der Liste)."""
    return next((entry for entry in values if entry.enabled), None)


def counts(values):
    """(wählbar, gesamt) für die Zustandszeile des Hosts."""
    values = list(values)
    return sum(1 for entry in values if entry.enabled), len(values)
