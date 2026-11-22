# SPDX-License-Identifier: MPL-2.0
"""Kompaktmodus ohne Tk (E-U1 A, D55, 23.10.2026).

Ein ausdrücklich eingeschalteter Arbeitsmodus für ein schmales Glide-Fenster
neben einer anderen Anwendung: reduzierter Kopf, keine Seitenleiste und nur
in diesem Modus eine kleinere Mindestgröße. Der normale Modus bleibt
unverändert. Beide Modi merken sich ihre Fensterlage getrennt – der normale
wie bisher in `window.conf`, der kompakte additiv in den Einstellungen.

Dieses Modul rechnet nur mit Geometrietexten („BxH+X+Y“) und Bildschirmmaßen.
Die neutrale Geometrie (`parse`, `format_geometry`, `clamp`, `keep_visible`)
liegt seit V1.67 in `glide_shell.window_geometry` (D96); hier bleiben die
Glide-Mindestmaße, der Einstellungsname und die Regeln des Kompaktmodus.
"""

from glide_shell import window_geometry as _geometry
from glide_shell.window_geometry import (  # noqa: F401 – bisherige Aufrufstellen
    MAX_SIDE, SCREEN_RESERVE, VISIBLE_MARGIN, format_geometry, keep_visible, parse)

NORMAL_MIN = (860, 700)
COMPACT_MIN = (480, 560)
COMPACT_DEFAULT_WIDTH = 480
COMPACT_DEFAULT_HEIGHT = 760
SETTING = "compact_window"


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


def normalize_saved(value):
    """Gespeicherte Kompaktlage prüfen: gültiger Text mit Mindestgröße, sonst leer."""
    parsed = parse(value)
    if parsed is None or parsed[0] < COMPACT_MIN[0] or parsed[1] < COMPACT_MIN[1]:
        return ""
    return format_geometry(*parsed)


def clamp(width, height, x, y, screen_width, screen_height, minimum=COMPACT_MIN, origin=(0, 0)):
    """`window_geometry.clamp` mit der Kompakt-Mindestgröße als Vorgabe."""
    return _geometry.clamp(width, height, x, y, screen_width, screen_height, minimum, origin)


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
