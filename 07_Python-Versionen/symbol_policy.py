"""Lesbare Oberflächenzeichen aus der tatsächlichen UI-Schrift, ohne Tk.

Die UI liefert eine Abdeckungsprüfung für normale und fette Schnitte.
Beschriftungen, Aktionskennungen und Tastaturwege bleiben beim Aufrufer.
"""

# Kurze deutsche Beschriftungen sind der letzte Rückfall. Kein Symbolfont,
# keine Emoji und keine unlesbaren Ersatzkästchen.
TEXT_FALLBACKS = {
    "move_up": "^", "move_down": "v", "history": "V", "bullet": "*",
    "actions": "Ak", "search": "Su", "details": "Dt", "home": "St",
    "today": "H", "pages": "Se", "planday": "Pl", "settings": "Ei",
    "capture": "+", "notifications": "!", "sidebar": "Sl", "check": "OK",
    "task_open": "[]", "templates": "Vo", "inbox": "E", "in_progress": "De",
    "overdue": "Vs", "trash": "Pk", "theme_to_dark": "Du", "theme_to_light": "He",
    "labels": "La", "calendar": "Ka", "attachment": "An", "repeat": "W",
    "group": ">", "back": "<", "next": ">", "board": "Pi", "folder": "Or",
    "list": "Li", "drawing": "Ze", "gallery": "Ga", "undo": "Zu", "redo": "No",
    "swap": "<>", "link": "Ve", "blocked": "Wa", "timer": "Zt", "archive": "Ar",
    "pinned": "Fa", "symmetry_x": "X" , "symmetry_y": "Y", "edit": "Be",
    "dropdown_closed": "v", "dropdown_open": "^", "moon_new": "N", "moon_first": ")",
    "moon_full": "O", "moon_last": "(", "description": "Bs", "priority_low": "1",
    "priority_medium": "2", "priority_high": "3", "checklist": "[x]",
    "sort_ascending": "^", "sort_descending": "v", "print": "Dr", "overflow": "...",
    "remove": "x",
}

# Einige ältere Zeichen fehlen auch in der mitgelieferten UI-Schrift.
# Die Auswahl bleibt semantisch: Suche/Druck kurz beschriftet, Meldung als
# Ausrufezeichen, Papierkorb als Wiederverwertung mit lesbarem Text-Rückfall.
PREFERRED = {"search": ("Su",), "notifications": ("!",), "trash": ("♲", "Pk"), "print": ("Dr",)}


def resolve(icons, covers):
    """Vollständige Tabelle und nachvollziehbare Änderungen zurückgeben.

    `covers` prüft eine ganze Zeichenfolge. Ein fehlender Tabellenvertrag
    oder eine UI-Schrift ohne lesbare ASCII-Zeichen ist ein sichtbarer Fehler.
    """
    if set(icons) != set(TEXT_FALLBACKS):
        raise ValueError("Symbolvertrag und ICONS-Tabelle unterscheiden sich")
    resolved, changes = {}, {}
    for key, original in icons.items():
        choices = (*PREFERRED.get(key, (original,)), TEXT_FALLBACKS[key])
        chosen = next((value for value in dict.fromkeys(choices) if covers(value)), None)
        if chosen is None:
            raise ValueError(f"UI-Schrift enthält kein lesbares Zeichen für {key}")
        resolved[key] = chosen
        if chosen != original:
            changes[key] = {"vorher": original, "nachher": chosen}
    return resolved, changes


def split_heading(text, icons):
    """Symbol und Beschriftung dürfen in verschiedenen Schriften stehen."""
    first, separator, caption = str(text).partition("  ")
    return (first, caption) if separator and first in icons.values() else ("", str(text))
