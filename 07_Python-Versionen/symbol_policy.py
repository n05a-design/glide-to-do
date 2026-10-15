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
# Die Auswahl bleibt semantisch: Druck kurz beschriftet, Meldung als
# Ausrufezeichen, Papierkorb als Wiederverwertung mit lesbarem Text-Rückfall.
# Die Suche zeigt seit B10 (15.10.2026) wieder die Lupe ⌕ (U+2315); „Su“ ist
# nur noch der letzte Rückfall.
PREFERRED = {"search": ("⌕", "Su"), "notifications": ("!",), "trash": ("♲", "Pk"), "print": ("Dr",)}

# B10 (15.10.2026, D50 präzisiert D29): Die mitgelieferte UI-Schrift (DejaVu
# Sans) kennt keine Lupe. Nur für sie darf das Zeichen aus einer einfarbigen
# Systemschrift des Betriebssystems kommen – unter Windows Segoe UI Symbol,
# unter macOS Apple Symbols, unter Linux Noto Sans Symbols bzw. DejaVu Sans
# Mono. Das ist keine mitgelieferte Symbol- oder Iconschrift; fehlt jede, bleibt
# es beim lesbaren Text „Su“. Emoji-Schriften sind ausgeschlossen.
SYMBOL_FONT_FALLBACKS = {"search": ("Segoe UI Symbol", "Apple Symbols", "Noto Sans Symbols",
                                    "Noto Sans Symbols2", "DejaVu Sans Mono")}
SYMBOL_FONT_FAMILIES = frozenset(name for names in SYMBOL_FONT_FALLBACKS.values() for name in names)


def resolve(icons, covers):
    """Vollständige Tabelle und nachvollziehbare Änderungen zurückgeben.

    `covers` prüft eine ganze Zeichenfolge. Ein fehlender Tabellenvertrag
    oder eine UI-Schrift ohne lesbare ASCII-Zeichen ist ein sichtbarer Fehler.
    """
    resolved, changes, _fonts = resolve_with_fonts(icons, covers)
    return resolved, changes


def resolve_with_fonts(icons, covers, covers_in=None):
    """Wie `resolve`, zusätzlich mit der Schrift je Zeichen außerhalb der UI-Schrift.

    `covers_in(familie, text)` prüft eine Systemschrift aus
    `SYMBOL_FONT_FALLBACKS`. Liefert ``(tabelle, änderungen, schriften)``;
    `schriften` nennt nur Schlüssel, deren Zeichen nicht aus der UI-Schrift stammt.
    """
    if set(icons) != set(TEXT_FALLBACKS):
        raise ValueError("Symbolvertrag und ICONS-Tabelle unterscheiden sich")
    resolved, changes, fonts = {}, {}, {}
    for key, original in icons.items():
        choices = (*PREFERRED.get(key, (original,)), TEXT_FALLBACKS[key])
        chosen = family = None
        for value in dict.fromkeys(choices):
            if covers(value):
                chosen = value
                break
            if covers_in is not None and not value.isascii():
                family = next((name for name in SYMBOL_FONT_FALLBACKS.get(key, ()) if covers_in(name, value)), None)
                if family is not None:
                    chosen = value
                    break
        if chosen is None:
            raise ValueError(f"UI-Schrift enthält kein lesbares Zeichen für {key}")
        resolved[key] = chosen
        if family is not None:
            fonts[key] = family
        if chosen != original:
            changes[key] = {"vorher": original, "nachher": chosen}
    return resolved, changes, fonts


def split_heading(text, icons):
    """Symbol und Beschriftung dürfen in verschiedenen Schriften stehen."""
    first, separator, caption = str(text).partition("  ")
    return (first, caption) if separator and first in icons.values() else ("", str(text))
