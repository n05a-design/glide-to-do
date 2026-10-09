"""Gemeinsame Gestaltungsskalen und reine Regeln für Titel und Herkunft.

OB01 beginnt mit bestehenden Werten. Die unregelmäßigen Zwischenstufen
bewahren die bisherige Darstellung; weitere Ansichten werden schrittweise
übernommen, bevor eine bewusst sichtbare Vereinheitlichung entschieden wird.
"""
from types import MappingProxyType

SPACING = MappingProxyType({value: value for value in
                           (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 22, 24, 28, 30)})
RADII = MappingProxyType({"card": 18, "field": 16})
FONT_SIZES = MappingProxyType({"caption": 8, "source": 9, "body": 12, "title": 24})
ROW_HEIGHTS = MappingProxyType({"task": 36})


def fit_text(text, measure, width):
    """Einzeilig kürzen; vollständiger Text bleibt beim Aufrufer erhalten."""
    if not text or width <= 0:
        return ""
    if measure(text) <= width:
        return text
    ellipsis = "…"
    if measure(ellipsis) > width:
        return ""
    low, high = 0, len(text)
    while low < high:
        mid = (low + high + 1) // 2
        if measure(text[:mid] + ellipsis) <= width:
            low = mid
        else:
            high = mid - 1
    return text[:low].rstrip() + ellipsis


def today_columns(width, due, labels):
    """Titel behält mindestens 260 px, Herkunft höchstens 180 px rechts.

    Labels und Fälligkeit weichen bei Enge wie bisher; die Herkunft bleibt
    sichtbar. Die Quelle wird im verbleibenden Raum mit Auslassung gekürzt.
    """
    source = min(180, max(100, int(width * .25)))
    edge = 6
    if width - source - due - labels - 24 - edge < 260:
        labels = 0
    if width - source - due - 24 - edge < 260:
        due = 0
    gap = 24 if due or labels else 0
    return max(260, width - source - due - labels - gap - edge), due, labels, source, gap
