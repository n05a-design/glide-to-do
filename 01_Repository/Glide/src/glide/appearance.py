# SPDX-License-Identifier: MPL-2.0
"""Erscheinungsbild „Automatisch (hell/dunkel)“ ohne Tk (N01 seit 3.33.21).

Glide kennt Designpaare (Hell/Dunkel, Liquid Glass, Minimal, Kontrast) und
zwei Designs nur auf dunklem Grund (Pixel, Dopamin). Folgt Glide dem System,
merkt es sich ein Paar: das helle und das dunkle Design. Für ein Design ohne
helles Gegenstück gilt bei hellem System „Hell“ – neue Farben entstehen nicht.

Erkannt wird der Systemmodus über Tk (macOS), die Registrierung (Windows) oder
die Desktop-Einstellung (Linux). Jede Erkennung darf scheitern; dann bleibt
das zuletzt gewählte Design stehen. Die Erkennung und `resolve` liegen seit
V1.67 in `glide_shell.system_appearance` (D96); hier bleiben Designpaare und
Hintergrundwahl.
"""

from glide_shell.system_appearance import (  # noqa: F401 – bisherige Aufrufstellen
    linux_is_dark, resolve, tk_is_dark, windows_is_dark)

LIGHT_FALLBACK = "light"


def pair_for(design, designs):
    """{"light": …, "dark": …} für ein Design aus der Designtabelle."""
    eintrag = designs.get(design)
    if eintrag is None:
        return None
    partner = eintrag.get("partner") or design
    if partner == design or partner not in designs:
        if eintrag.get("base") == "light":
            return {"light": design, "dark": design}
        return {"light": LIGHT_FALLBACK if LIGHT_FALLBACK in designs else design, "dark": design}
    if eintrag.get("base") == "light":
        return {"light": design, "dark": partner}
    return {"light": partner, "dark": design}


def normalize_auto(value, designs):
    """Gespeichertes Paar prüfen; Unlesbares oder Unbekanntes ergibt None (aus)."""
    if not isinstance(value, dict):
        return None
    hell, dunkel = value.get("light"), value.get("dark")
    if hell not in designs or dunkel not in designs:
        return None
    return {"light": hell, "dark": dunkel}


BACKGROUND_CHOICES = (
    ('Designvorgabe', 'default'), ('Wie die Fensterfläche · ohne Schatten', 'surface'),
    ('Lila', 'accent'), ('Blau', 'clear'), ('Türkis', 'due_action'),
    ('Grün', 'export'), ('Gelb', 'flag'), ('Rot', 'delete'),
    ('Braun', 'import'), ('Kontrastgrau', 'muted'),
)
BACKGROUND_KEYS = frozenset(key for _label, key in BACKGROUND_CHOICES)


def background_choice(value):
    return value if isinstance(value, str) and value in BACKGROUND_KEYS else 'default'


def with_background(theme, choice, palette=None):
    """Nur den Hintergrund färben; Arbeitsflächen und Rollen bleiben erhalten."""
    from backdrop import hex_rgb, rgb_hex, mix, luminance
    result = dict(theme)
    choice = background_choice(choice)
    if choice == 'surface':
        result['bg'] = result['card']
        result['glass_shadow'] = result['card']
        result['glass_gradient'] = ''
    elif choice != 'default':
        # Ruhige Töne derselben festen Palette erhalten den Schriftkontrast.
        base = hex_rgb(result['bg'])
        share = 0.16 if luminance(base) < 0.2 else 0.08
        result['bg'] = rgb_hex(mix(base, hex_rgb((palette or theme)[choice]), share))
    return result
