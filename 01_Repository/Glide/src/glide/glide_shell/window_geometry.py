# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 8: Fenstergeometrie ohne Tk – Geometrietexte lesen, schreiben und sichtbar halten.

Rechnet mit Tk-Geometrietexten („BxH+X+Y“) und Arbeitsflächen, auch mit
negativen Koordinaten links oder über dem Hauptbildschirm. Mindestmaße und
gemerkte Lagen liefert der Host; das Modul importiert kein `tkinter`.
"""

import re

MAX_SIDE = 10000
VISIBLE_MARGIN = 120
SCREEN_RESERVE = 80

_GEOMETRY = re.compile(r"^(\d{2,5})x(\d{2,5})(?:([+-])(-?\d{1,5})([+-])(-?\d{1,5}))?$")


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


def clamp(width, height, x, y, screen_width, screen_height, minimum, origin=(0, 0)):
    """Mindestgröße einhalten und einen sichtbaren Streifen auf der Arbeitsfläche lassen.

    Die Arbeitsfläche ist das Rechteck aus `origin` und Breite/Höhe – unter
    Windows die virtuelle Fläche über alle Bildschirme. Ein Bildschirm links
    oder über dem Hauptbildschirm hat negative Koordinaten. `minimum` ist
    (Breite, Höhe) des Hosts; die Höhe hält `SCREEN_RESERVE` für Menü- und
    Taskleisten frei.
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


def keep_visible(x, y, width, bounds, margin=VISIBLE_MARGIN):
    """Lage der Normalansicht: ein sichtbarer Streifen bleibt auf der Arbeitsfläche.

    `bounds` ist (links, oben, Breite, Höhe) der Arbeitsfläche. Die Maße des
    Fensters bleiben unberührt, seine Höhe geht in die Regel nicht ein: Die
    Oberkante bleibt auf der Fläche, seitlich genügt der Streifen. Anders als
    `clamp` gilt die Regel für jede gemeldete Fläche, auch für 0 × 0 – so
    rechnete die Fensterlage beim Start schon vor dieser Auslagerung.
    """
    left, top, screen_width, screen_height = bounds
    x = max(left - (width - margin), min(x, left + screen_width - margin))
    y = max(top, min(y, top + screen_height - margin))
    return x, y
