"""Kompaktmodus ohne Tk (E-U1 A, D55, 23.10.2026).

Ein ausdrücklich eingeschalteter Arbeitsmodus für ein schmales Glide-Fenster
neben einer anderen Anwendung: reduzierter Kopf, keine Seitenleiste und nur
in diesem Modus eine kleinere Mindestgröße. Der normale Modus bleibt
unverändert. Beide Modi merken sich ihre Fensterlage getrennt – der normale
wie bisher in `window.conf`, der kompakte additiv in den Einstellungen.

Dieses Modul rechnet nur mit Geometrietexten („BxH+X+Y“) und Bildschirmmaßen.
"""

import re

NORMAL_MIN = (860, 700)
COMPACT_MIN = (480, 560)
COMPACT_DEFAULT_WIDTH = 480
COMPACT_DEFAULT_HEIGHT = 760
MAX_SIDE = 10000
VISIBLE_MARGIN = 120
SCREEN_RESERVE = 80
SETTING = "compact_window"

_GEOMETRY = re.compile(r"^(\d{2,5})x(\d{2,5})(?:([+-])(-?\d{1,5})([+-])(-?\d{1,5}))?$")


def shortcut_transition(down, *, released, modifiers, macos=False):
    """(Tastenzustand, Aktion) für das Kürzel; keine Uhr- oder Tk-Abhängigkeit.

    Vollständiges Paar und Wiederholung des Drückens wirken einmal. Fehlt der
    Tastendruck, gilt Loslassen nur mit Umschalt plus Strg bzw. Cmd als Ersatz.
    Modifierloslassen/Fensterfokusverlust setzen den Zustand im UI-Adapter zurück.
    """
    if not released:
        return True, 'consume' if down else 'toggle'
    if down:
        return False, 'consume'
    modifier = 0x0004 | (0x0008 if macos else 0)
    valid = bool(modifiers & 0x0001 and modifiers & modifier)
    return False, 'toggle' if valid else 'pass'


def parse(geometry):
    """(Breite, Höhe, x, y) aus einem Tk-Geometrietext; x/y None ohne Lage. None bei Unsinn.

    Tk schreibt eine Lage links oder über dem Hauptbildschirm als „+-1700“.
    Ein einfaches „-1700“ meint dagegen den Abstand vom rechten bzw. unteren
    Rand; ohne Bildschirmmaß ist das keine Lage, sie entfällt.
    """
    match = _GEOMETRY.match(str(geometry or "").strip())
    if not match:
        return None
    width, height = int(match.group(1)), int(match.group(2))
    if not (0 < width <= MAX_SIDE and 0 < height <= MAX_SIDE):
        return None
    if match.group(3) is None or "-" in (match.group(3), match.group(5)):
        return width, height, None, None
    return width, height, int(match.group(4)), int(match.group(6))


def format_geometry(width, height, x=None, y=None):
    """Tk-Geometrietext; negative Koordinaten als „+-x“ (nicht „-x“: das wäre vom rechten Rand)."""
    if x is None or y is None:
        return f"{int(width)}x{int(height)}"
    return f"{int(width)}x{int(height)}+{int(x)}+{int(y)}"


def normalize_saved(value):
    """Gespeicherte Kompaktlage prüfen: gültiger Text mit Mindestgröße, sonst leer."""
    parsed = parse(value)
    if parsed is None or parsed[0] < COMPACT_MIN[0] or parsed[1] < COMPACT_MIN[1]:
        return ""
    return format_geometry(*parsed)


def clamp(width, height, x, y, screen_width, screen_height, minimum=COMPACT_MIN, origin=(0, 0)):
    """Mindestgröße einhalten und einen sichtbaren Streifen auf der Arbeitsfläche lassen.

    Die Arbeitsfläche ist das Rechteck aus `origin` und Breite/Höhe – unter
    Windows die virtuelle Fläche über alle Bildschirme. Ein Bildschirm links
    oder über dem Hauptbildschirm hat negative Koordinaten.
    """
    left, top = (int(origin[0]), int(origin[1])) if origin else (0, 0)
    width = max(minimum[0], int(width))
    height = max(minimum[1], int(height))
    if screen_width and screen_width > 0:
        width = min(width, max(minimum[0], int(screen_width)))
    if screen_height and screen_height > 0:
        height = min(height, max(minimum[1], int(screen_height) - SCREEN_RESERVE))
    if x is None or y is None:
        return width, height, None, None
    if screen_width and screen_width > 0:
        x = max(left - (width - VISIBLE_MARGIN), min(int(x), left + int(screen_width) - VISIBLE_MARGIN))
    if screen_height and screen_height > 0:
        y = max(top, min(int(y), top + int(screen_height) - VISIBLE_MARGIN))
    return width, height, x, y


def compact_geometry(normal, saved, screen_width, screen_height, origin=(0, 0)):
    """Fensterlage beim Eintritt in den Kompaktmodus.

    Eine gemerkte Kompaktlage gilt, solange sie auf der Arbeitsfläche liegt.
    Sonst entsteht ein schmales Fenster an der rechten Kante des bisherigen:
    Es bleibt dort, wo man gerade gearbeitet hat – auch auf einem zweiten
    Bildschirm –, und gibt links Platz frei.
    """
    remembered = parse(normalize_saved(saved))
    if remembered is not None:
        return format_geometry(*clamp(*remembered, screen_width, screen_height, origin=origin))
    current = parse(normal)
    if current is None:
        return format_geometry(*clamp(COMPACT_DEFAULT_WIDTH, COMPACT_DEFAULT_HEIGHT, None, None,
                                      screen_width, screen_height, origin=origin))
    width, height, x, y = current
    new_width = COMPACT_DEFAULT_WIDTH
    # Höhe bleibt: Das schmale Fenster steht in derselben Zeile wie vorher.
    new_height = max(COMPACT_MIN[1], height)
    new_x = None if x is None else x + width - new_width
    return format_geometry(*clamp(new_width, new_height, new_x, y, screen_width, screen_height, origin=origin))


def normal_geometry(remembered, current):
    """Fensterlage beim Verlassen: die vor dem Eintritt gemerkte, sonst die aktuelle mit Normalmindestmaß."""
    parsed = parse(remembered) or parse(current)
    if parsed is None:
        return format_geometry(1280, 860)
    width, height, x, y = parsed
    return format_geometry(max(NORMAL_MIN[0], width), max(NORMAL_MIN[1], height), x, y)
