"""Gemeinsame Gestaltungsskalen und reine Regeln für Titel und Herkunft.

Vier Inhaltsstufen: Seitentitel, Abschnitt, Inhalt und Zusatzangabe.
Bestehende Symbol- und Bediengrößen bleiben unabhängig davon.
"""
from types import MappingProxyType

SPACING = MappingProxyType({value: value for value in
                           (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 22, 24, 28, 30)})
RADII = MappingProxyType({"card": 18, "field": 16})
FONT_SIZES = MappingProxyType({"caption": 9, "source": 9, "body": 12, "section": 16, "title": 22})
ROW_HEIGHTS = MappingProxyType({"task": 36})
TITLE_MAX_CHARS = 40
BUTTON_TEXT_MAX_CHARS = 24


def clip_title(text, limit=TITLE_MAX_CHARS, ellipsis="..."):
    """Zeichengrenze einschließlich Auslassung; keine Änderung am Quellobjekt."""
    text = str(text or "")
    if len(text) <= limit:
        return text
    if limit < len(ellipsis):
        return ""
    return text[:limit - len(ellipsis)].rstrip() + ellipsis


def edited_title(text, previous):
    """Alttitel bei reinen Metadatenänderungen bewahren, geänderte Titel begrenzen."""
    return text if text == previous else clip_title(text)


def task_title(text, description="", *, preserve=False):
    """Neue Titel begrenzen und ihr Original sichern; Altdaten vollständig bewahren."""
    clipped = text if preserve else clip_title(text)
    if clipped != text:
        description = (str(description or "").rstrip() + "\n\nOriginaltitel:\n" + text).lstrip()
    return clipped, description


def display_title(text, measure, width, limit=TITLE_MAX_CHARS):
    """Zeichen- und Pixelgrenze gemeinsam; vollständiger Titel bleibt beim Aufrufer."""
    return fit_text(clip_title(" ".join(str(text or "").split()), limit), measure, width, ellipsis="...")


def page_icon_layout(left_padding, line_height, preferred_scale, cell_size=16, gap=8):
    """Symbol im linken Leserand halten; die Textkante bleibt bei x=0."""
    scale = min(max(1, int(preferred_scale)), int((left_padding - gap) // cell_size),
                int(line_height // cell_size))
    if scale < 1:
        return None
    size = cell_size * scale
    return scale, -size - gap, (int(line_height) - size) // 2


def fit_text(text, measure, width, ellipsis="…"):
    """Einzeilig kürzen; vollständiger Text bleibt beim Aufrufer erhalten."""
    if not text or width <= 0:
        return ""
    if measure(text) <= width:
        return text
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
    # B11: Der Titel bleibt zusätzlich die breiteste Spalte. Seit der breiteren
    # Standardschrift Roboto Mono (D59) war die Fälligkeit mit Bearbeitungstag
    # sonst breiter als der Titel.
    if width - source - due - labels - 24 - edge < max(260, due + 1, labels + 1):
        labels = 0
    if width - source - due - 24 - edge < max(260, due + 1):
        due = 0
    gap = 24 if due or labels else 0
    return max(260, width - source - due - labels - gap - edge), due, labels, source, gap
