"""Tk-Bildfunktionen der Glide-Zeichenfläche.

Gemeinsam genutzt von der eingebetteten Zeichenseite in ``app.pyw`` und der
isolierten Bedienprobe ``drawing_prototype.pyw``. Das Modul benötigt Tk nur für
``PhotoImage``; das gespeicherte Zellmodell bleibt ausschließlich Sache von
``drawing.py``.
"""

from __future__ import annotations

import re
import tkinter as tk

from drawing import BACKGROUND, HEIGHT, WIDTH, DrawingFormatError, DrawingModel

# Referenzbilder werden vor dem Einlesen begrenzt. Tk hält ein PhotoImage
# unkomprimiert im Speicher; 4096 × 4096 Pixel sind rund 64 MiB.
MAX_REFERENCE_BYTES = 32 * 1024 * 1024
MAX_REFERENCE_DIMENSION = 4096
# Die Nachzeichnung verwendet höchstens 64 Farben einschließlich Weiß.
TRACE_MAX_COLORS = 64
TRACE_WHITE_DEFAULT = 245


_SHORT_HEX_RE = re.compile(r"#?([0-9A-Fa-f]{3})\Z")
_LONG_HEX_RE = re.compile(r"#?([0-9A-Fa-f]{6})\Z")


def normalize_ui_color(value: str, widget: tk.Misc) -> str:
    """Accept common color input while keeping the drawing format canonical."""
    text = value.strip()
    match = _LONG_HEX_RE.fullmatch(text)
    if match:
        return f"#{match.group(1).upper()}"
    match = _SHORT_HEX_RE.fullmatch(text)
    if match:
        digits = match.group(1).upper()
        return "#" + "".join(character * 2 for character in digits)
    try:
        red, green, blue = widget.winfo_rgb(text)
    except tk.TclError as exc:
        raise DrawingFormatError(
            "Ungültige Farbe. Bitte Farbspektrum oder #RRGGBB verwenden."
        ) from exc
    return f"#{red // 257:02X}{green // 257:02X}{blue // 257:02X}"


def render_framed_reference(
    source: tk.PhotoImage,
    mode: str = "fill",
    zoom_percent: float = 100.0,
    offset_x: float = 0.0,
    offset_y: float = 0.0,
) -> tk.PhotoImage:
    """Render a local PNG into the fixed 128 x 128 reference plane.

    The nearest-neighbour sampling is deliberate: the reference remains crisp
    and every displayed reference color can be picked deterministically.
    """
    source_width, source_height = source.width(), source.height()
    if source_width < 1 or source_height < 1:
        raise DrawingFormatError("Das Referenzbild hat keine gültigen Abmessungen")
    if mode not in {"fit", "fill"}:
        raise DrawingFormatError("Unbekannter Bildrahmen-Modus")
    base_scale = (
        min(WIDTH / source_width, HEIGHT / source_height)
        if mode == "fit"
        else max(WIDTH / source_width, HEIGHT / source_height)
    )
    scale = base_scale * max(0.01, float(zoom_percent) / 100.0)
    displayed_width = source_width * scale
    displayed_height = source_height * scale
    left = (WIDTH - displayed_width) / 2.0 + float(offset_x)
    top = (HEIGHT - displayed_height) / 2.0 + float(offset_y)

    rows = []
    transparency_get = getattr(source, "transparency_get", None)
    for y in range(HEIGHT):
        source_y = round((y + 0.5 - top) / scale - 0.5)
        row = []
        for x in range(WIDTH):
            source_x = round((x + 0.5 - left) / scale - 0.5)
            if not (0 <= source_x < source_width and 0 <= source_y < source_height):
                row.append("#FFFFFF")
                continue
            if transparency_get is not None and transparency_get(source_x, source_y):
                row.append("#FFFFFF")
                continue
            value = source.get(source_x, source_y)
            if isinstance(value, tuple):
                row.append("#{:02X}{:02X}{:02X}".format(*value[:3]))
            elif isinstance(value, str) and value.startswith("#"):
                row.append(value[:7].upper())
            else:
                row.append("#FFFFFF")
        rows.append("{" + " ".join(row) + "}")
    result = tk.PhotoImage(width=WIDTH, height=HEIGHT)
    result.put(" ".join(rows))
    return result


def render_trace_reference(
    source: tk.PhotoImage,
    mode: str = "fill",
    zoom_percent: float = 100.0,
    offset_x: float = 0.0,
    offset_y: float = 0.0,
) -> tk.PhotoImage:
    """Render a contour-aware 128 x 128 source for automatic tracing."""
    source_width, source_height = source.width(), source.height()
    if source_width < 1 or source_height < 1:
        raise DrawingFormatError("Das Referenzbild hat keine gültigen Abmessungen")
    if mode not in {"fit", "fill"}:
        raise DrawingFormatError("Unbekannter Bildrahmen-Modus")
    base_scale = (
        min(WIDTH / source_width, HEIGHT / source_height)
        if mode == "fit"
        else max(WIDTH / source_width, HEIGHT / source_height)
    )
    scale = base_scale * max(0.01, float(zoom_percent) / 100.0)
    left = (WIDTH - source_width * scale) / 2.0 + float(offset_x)
    top = (HEIGHT - source_height * scale) / 2.0 + float(offset_y)
    transparency_get = getattr(source, "transparency_get", None)
    sample_positions = (0.125, 0.375, 0.625, 0.875)
    contour_samples = 6  # mindestens ein Drittel der 16 Teilflächen
    rows = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            samples = []
            dark = []
            for sub_y in sample_positions:
                source_y = round((y + sub_y - top) / scale - 0.5)
                for sub_x in sample_positions:
                    source_x = round((x + sub_x - left) / scale - 0.5)
                    if not (0 <= source_x < source_width and 0 <= source_y < source_height):
                        color = (255, 255, 255)
                    elif transparency_get is not None and transparency_get(source_x, source_y):
                        color = (255, 255, 255)
                    else:
                        color = _image_rgb(source, source_x, source_y)
                    samples.append(color)
                    luminance = (299 * color[0] + 587 * color[1] + 114 * color[2]) // 1000
                    if luminance <= 96:
                        dark.append(color)
            selected = dark if len(dark) >= contour_samples else samples
            average = tuple(
                round(sum(color[channel] for color in selected) / len(selected))
                for channel in range(3)
            )
            row.append("#{:02X}{:02X}{:02X}".format(*average))
        rows.append("{" + " ".join(row) + "}")
    result = tk.PhotoImage(width=WIDTH, height=HEIGHT)
    result.put(" ".join(rows))
    return result


def _image_rgb(image: tk.PhotoImage, x: int, y: int) -> tuple[int, int, int]:
    value = image.get(x, y)
    if isinstance(value, tuple):
        return tuple(value[:3])
    if isinstance(value, str) and value.startswith("#") and len(value) >= 7:
        return tuple(int(value[index:index + 2], 16) for index in (1, 3, 5))
    return (255, 255, 255)


def quantize_reference(
    image: tk.PhotoImage,
    *,
    max_colors: int = 64,
    white_threshold: int = 245,
) -> DrawingModel:
    """Convert a framed reference into an editable, white-backed cell model."""
    if image.width() != WIDTH or image.height() != HEIGHT:
        raise DrawingFormatError("Die Nachzeichnung benötigt eine gerahmte 128-×-128-Referenz")
    if not 2 <= max_colors <= 64:
        raise DrawingFormatError("Die Nachzeichnung erlaubt 2 bis 64 Farben")
    if not 0 <= white_threshold <= 255:
        raise DrawingFormatError("Die Weißtoleranz muss zwischen 0 und 255 liegen")

    raw_cells: list[tuple[int, int, int] | None] = []
    histogram: dict[tuple[int, int, int], int] = {}
    transparency_get = getattr(image, "transparency_get", None)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            transparent = transparency_get is not None and transparency_get(x, y)
            color = _image_rgb(image, x, y)
            if transparent or min(color) >= white_threshold:
                raw_cells.append(None)
                continue
            raw_cells.append(color)
            histogram[color] = histogram.get(color, 0) + 1

    if not histogram:
        return DrawingModel.blank()

    boxes: list[list[tuple[tuple[int, int, int], int]]] = [
        sorted(histogram.items())
    ]
    while len(boxes) < max_colors - 1:
        candidates = []
        for index, entries in enumerate(boxes):
            if len(entries) < 2:
                continue
            ranges = tuple(
                max(color[channel] for color, _count in entries)
                - min(color[channel] for color, _count in entries)
                for channel in range(3)
            )
            population = sum(count for _color, count in entries)
            channel = max(range(3), key=lambda value: (ranges[value], -value))
            candidates.append((ranges[channel] * population, population, index, channel))
        if not candidates:
            break
        _spread, _population, box_index, channel = max(candidates)
        entries = sorted(boxes.pop(box_index), key=lambda item: (item[0][channel], item[0]))
        total = sum(count for _color, count in entries)
        cumulative = 0
        split_at = 1
        for split_at, (_color, count) in enumerate(entries, 1):
            cumulative += count
            if cumulative * 2 >= total:
                break
        split_at = min(len(entries) - 1, max(1, split_at))
        boxes.extend((entries[:split_at], entries[split_at:]))

    palette = [BACKGROUND]
    color_to_index: dict[tuple[int, int, int], int] = {}
    for entries in boxes:
        population = sum(count for _color, count in entries)
        representative = tuple(
            round(sum(color[channel] * count for color, count in entries) / population)
            for channel in range(3)
        )
        value = "#{:02X}{:02X}{:02X}".format(*representative)
        if value == BACKGROUND:
            representative = max(entries, key=lambda item: (item[1], item[0]))[0]
            value = "#{:02X}{:02X}{:02X}".format(*representative)
        try:
            palette_index = palette.index(value)
        except ValueError:
            palette.append(value)
            palette_index = len(palette) - 1
        for color, _count in entries:
            color_to_index[color] = palette_index

    cells = bytearray(
        0 if color is None else color_to_index[color]
        for color in raw_cells
    )
    return DrawingModel(palette, cells)


def model_to_photo(model: DrawingModel) -> tk.PhotoImage:
    rows = []
    for y in range(HEIGHT):
        start = y * WIDTH
        rows.append("{" + " ".join(
            model.palette[index] for index in model.cells[start:start + WIDTH]
        ) + "}")
    image = tk.PhotoImage(width=WIDTH, height=HEIGHT)
    image.put(" ".join(rows))
    return image
