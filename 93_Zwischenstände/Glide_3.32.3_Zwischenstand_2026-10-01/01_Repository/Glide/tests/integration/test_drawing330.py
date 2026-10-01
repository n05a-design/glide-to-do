"""Glide 3.30.0: Werkzeuge und Formate des Zeichenkerns ohne Tk."""

from __future__ import annotations

import json
from pathlib import Path
import random
import struct
import sys
import zlib


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src/glide"))

import drawing  # noqa: E402
from drawing import (  # noqa: E402
    BACKGROUND,
    BRUSH_SIZES,
    DrawingFormatError,
    DrawingModel,
    PixelPerfectStroke,
    brush_hits,
    constrain_end,
    ellipse_cells,
    import_glide_svg,
    line_cells,
    mirror_cells,
    mirror_points,
    palette_to_gpl,
    palette_to_hex,
    parse_palette,
    rect_cells,
)


def rejected(action, message):
    try:
        action()
    except DrawingFormatError:
        return
    raise AssertionError(message)


def png_indices(data):
    """Minimaler Leser für die eigenen indizierten PNGs."""
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    position = 8
    chunks = {}
    idat = b""
    while position < len(data):
        length = struct.unpack(">I", data[position:position + 4])[0]
        kind = data[position + 4:position + 8]
        body = data[position + 8:position + 8 + length]
        crc = struct.unpack(">I", data[position + 8 + length:position + 12 + length])[0]
        assert crc == zlib.crc32(kind + body) & 0xFFFFFFFF
        if kind == b"IDAT":
            idat += body
        else:
            chunks[kind] = body
        position += 12 + length
    width, height, depth, color_type = struct.unpack(">IIBB", chunks[b"IHDR"][:10])
    assert depth == 8 and color_type == 3
    raw = zlib.decompress(idat)
    rows = [raw[y * (width + 1) + 1:(y + 1) * (width + 1)] for y in range(height)]
    assert all(raw[y * (width + 1)] == 0 for y in range(height))
    palette = [chunks[b"PLTE"][index:index + 3].hex().upper() for index in range(0, len(chunks[b"PLTE"]), 3)]
    return width, height, rows, palette


# ---------------------------------------------------------------------------
# Flächengrößen: Version 2 für 16, 32, 64; 128 bleibt Version 1
# ---------------------------------------------------------------------------
for size in drawing.SIZES:
    model = DrawingModel.blank(size)
    document = model.to_document()
    assert document["width"] == document["height"] == size
    assert len(document["rows"]) == size and all(len(row) == 2 * size for row in document["rows"])
    assert document["format_version"] == (1 if size == 128 else 2)
    model.set_cell(size - 1, size - 1, "#112233")
    again = DrawingModel.from_json(model.to_json())
    assert again.width == size and again.color_at(size - 1, size - 1) == "#112233"
    svg = model.to_svg("Größe")
    assert f'viewBox="0 0 {size} {size}"' in svg
    imported = import_glide_svg(svg)
    assert imported.model.to_json() == model.to_json() and not imported.warnings
rejected(lambda: DrawingModel.blank(48), "Größe 48 wurde angenommen")
v1_small = DrawingModel.blank(16).to_document()
v1_small["format_version"] = 1
rejected(lambda: DrawingModel.from_document(v1_small), "Version 1 mit 16 Zellen wurde angenommen")
non_square = DrawingModel.blank(32).to_document()
non_square["height"] = 16
rejected(lambda: DrawingModel.from_document(non_square), "Nicht quadratische Fläche wurde angenommen")
v2_full = DrawingModel.blank(128).to_document()
v2_full["format_version"] = 2
assert DrawingModel.from_document(v2_full).width == 128
small_svg = DrawingModel.blank(32).to_svg("x")
rejected(lambda: import_glide_svg(small_svg.replace('version="2"', 'version="1"')),
         "Kleines SVG mit Profilversion 1 wurde angenommen")

# ---------------------------------------------------------------------------
# Formen, Einschränkung mit Umschalt
# ---------------------------------------------------------------------------
line = line_cells(0, 0, 9, 4)
assert line[0] == (0, 0) and line[-1] == (9, 4)
assert all(max(abs(a[0] - b[0]), abs(a[1] - b[1])) == 1 for a, b in zip(line, line[1:]))
assert line_cells(3, 3, 3, 3) == [(3, 3)]
assert constrain_end(0, 0, 10, 2, "line") == (10, 0)
assert constrain_end(0, 0, 2, 10, "line") == (0, 10)
assert constrain_end(0, 0, 7, 5, "line") == (7, 7)
assert constrain_end(5, 5, 1, 9, "rect") == (1, 9)
assert len(rect_cells(2, 2, 6, 5)) == 2 * 5 + 2 * 2
assert len(rect_cells(2, 2, 6, 5, filled=True)) == 5 * 4
assert rect_cells(4, 4, 4, 4) == [(4, 4)]
circle = set(ellipse_cells(10, 10, 25, 25))
assert circle == {(35 - x, y) for x, y in circle} == {(x, 35 - y) for x, y in circle}
filled_circle = set(ellipse_cells(10, 10, 25, 25, filled=True))
assert circle <= filled_circle and len(filled_circle) > len(circle)
shapes = DrawingModel([BACKGROUND, "#000000"])
with shapes.action("Form"):
    shapes.paint_shape("rect_filled", 0, 0, 3, 3, 1, 1)
assert shapes.undo_count == 1 and sum(shapes.cells) == 16
thick = DrawingModel([BACKGROUND, "#000000"])
thick.paint_shape("line", 10, 10, 30, 10, 4, 1)
assert all(thick.color_index_at(x, 9) == 1 for x in range(12, 29))

# ---------------------------------------------------------------------------
# Symmetrie: Das Spiegelbild des Zeigers trifft genau die gespiegelten Zellen
# ---------------------------------------------------------------------------
generator = random.Random(330)
for _ in range(300):
    size = generator.choice(BRUSH_SIZES)
    u, v = generator.uniform(0, 128), generator.uniform(0, 128)
    original = set(brush_hits(u, v, size))
    (mu, mv) = mirror_points(u, v, "x")[1]
    assert set(brush_hits(mu, mv, size)) == {(127 - x, y) for x, y in original}
    (mu, mv) = mirror_points(u, v, "y")[1]
    assert set(brush_hits(mu, mv, size)) == {(x, 127 - y) for x, y in original}
assert len(mirror_points(5, 5, "xy")) == 4 and mirror_points(5, 5, "none") == [(5, 5)]
assert set(mirror_cells([(0, 0)], "xy", 16, 16)) == {(0, 0), (15, 0), (0, 15), (15, 15)}
rejected(lambda: mirror_points(1, 1, "diagonal"), "Unbekannte Symmetrie wurde angenommen")

# ---------------------------------------------------------------------------
# Kachelmodus: Treffer jenseits des Rands erscheinen auf der Gegenseite
# ---------------------------------------------------------------------------
assert set(brush_hits(0.0, 0.0, 2, 16, 16, wrap=True)) == {(15, 15), (0, 15), (15, 0), (0, 0)}
assert set(brush_hits(0.0, 0.0, 2, 16, 16)) == {(0, 0)}

# ---------------------------------------------------------------------------
# Pixel-perfekte Linie entfernt L-Ecken, aber keine früher bemalten Zellen
# ---------------------------------------------------------------------------
tracker = PixelPerfectStroke()
removed = [tracker.add(cell) for cell in [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)]]
assert removed == [None, None, (1, 0), None, (2, 1)]
assert tracker.cells == [(0, 0), (1, 1), (2, 2)]
straight = PixelPerfectStroke()
assert [straight.add(cell) for cell in [(0, 0), (1, 0), (2, 0)]] == [None, None, None]
revisit = PixelPerfectStroke()
for cell in [(5, 5), (6, 5), (6, 6), (6, 5)]:
    revisit.add(cell)
assert revisit.add((7, 4)) is None  # (6, 5) wurde zweimal bemalt und bleibt
perfect = DrawingModel([BACKGROUND, "#000000"])
with perfect.action("Pinselzug"):
    perfect.set_cell(1, 0, 1)
    perfect.set_cell(0, 0, 1)
    assert perfect.restore_in_action(1, 0) is True
    assert perfect.restore_in_action(9, 9) is False
assert perfect.color_index_at(1, 0) == 0 and perfect.peek_undo().count == 1

# ---------------------------------------------------------------------------
# Füllmuster und Farbersetzung
# ---------------------------------------------------------------------------
checker = DrawingModel.blank(16)
assert checker.fill(0, 0, "#000000", "checker", "#FFFFFF") == 128
assert checker.color_index_at(0, 0) == 1 and checker.color_index_at(1, 0) == 0
for pattern, share in (("dots25", 0.25), ("dots75", 0.75)):
    dotted = DrawingModel.blank(16)
    dotted.fill(3, 3, "#FF0000", pattern, "#00FF00")
    red = sum(1 for value in dotted.cells if dotted.palette[value] == "#FF0000")
    assert red == int(256 * share), (pattern, red)
walled = DrawingModel.blank(16)
for y in range(16):
    walled.set_cell(8, y, "#000000")
assert walled.fill(0, 0, "#00AA00") == 8 * 16
assert walled.color_at(9, 0) == BACKGROUND
rejected(lambda: walled.fill(0, 0, "#00AA00", "stripes"), "Unbekanntes Muster wurde angenommen")
recolor = DrawingModel.blank(16)
for x in range(5):
    recolor.set_cell(x, 2, "#AA0000")
with recolor.action("Farbe ersetzen"):
    assert recolor.replace_color("#AA0000", "#0000AA") == 5
assert recolor.color_at(4, 2) == "#0000AA" and recolor.peek_undo().count == 5
assert recolor.unused_palette_count() == 1
assert recolor.compact_palette() == 1 and recolor.palette == [BACKGROUND, "#0000AA"]
assert recolor.undo_count == 0 and recolor.color_at(0, 2) == "#0000AA"

# ---------------------------------------------------------------------------
# Bereiche kopieren, leeren und einsetzen
# ---------------------------------------------------------------------------
source = DrawingModel.blank(32)
source.paint_shape("rect_filled", 2, 2, 5, 4, 1, "#123456")
region = source.copy_region(5, 4, 2, 2)
assert (region.width, region.height) == (4, 3) and set(region.colors) == {"#123456"}
assert source.clear_region(2, 2, 5, 4) == 12
target = DrawingModel.blank(32)
assert target.stamp_region(region, 30, 30) == 4  # am Rand abgeschnitten
assert target.color_at(31, 31) == "#123456"
holes = drawing.Region(2, 1, ("#FFFFFF", "#654321"))
target.set_cell(0, 0, "#000000")
target.stamp_region(holes, 0, 0, skip_white=True)
assert target.color_at(0, 0) == "#000000" and target.color_at(1, 0) == "#654321"
full = DrawingModel([BACKGROUND] + [f"#{number:06X}" for number in range(1, 256)], size=16)
rejected(lambda: full.stamp_region(drawing.Region(1, 1, ("#ABCDEF",)), 0, 0),
         "257. Farbe über Einsetzen wurde angenommen")
assert source.copy_region(40, 40, 50, 50) is None

# ---------------------------------------------------------------------------
# Palettendateien
# ---------------------------------------------------------------------------
gpl = "GIMP Palette\nName: Meer\nColumns: 4\n#\n  0  64 128\tTief\n255 255 255 Weiß\n0 64 128 doppelt\n"
assert parse_palette(gpl) == ("Meer", ["#004080", "#FFFFFF"])
assert parse_palette("ff0000\n#00ff00\n; Kommentar\n", "Grundfarben") == ("Grundfarben", ["#FF0000", "#00FF00"])
rejected(lambda: parse_palette("GIMP Palette\n300 0 0 zu hell\n"), "Farbwert über 255 wurde angenommen")
rejected(lambda: parse_palette("zzzzzz\n"), "Ungültige Hexzeile wurde angenommen")
rejected(lambda: parse_palette(""), "Leere Palette wurde angenommen")
rejected(lambda: parse_palette("\n".join(f"{number:06X}" for number in range(300))), "300 Farben wurden angenommen")
assert parse_palette(palette_to_gpl("Meer", ["#004080", "#FFFFFF"]))[1] == ["#004080", "#FFFFFF"]
assert parse_palette(palette_to_hex(["#004080"]))[1] == ["#004080"]

# ---------------------------------------------------------------------------
# PNG: indiziert, ganzzahlig vergrößert, pixelgenau
# ---------------------------------------------------------------------------
art = DrawingModel.blank(16)
art.set_cell(0, 0, "#FF0000")
art.set_cell(15, 15, "#0000FF")
for scale in drawing.PNG_SCALES:
    width, height, rows, palette = png_indices(art.to_png(scale))
    assert width == height == 16 * scale
    assert palette[rows[0][0]] == "FF0000" and palette[rows[-1][-1]] == "0000FF"
    assert palette[rows[0][scale]] == "FFFFFF"
rejected(lambda: DrawingModel.blank(128).to_png(32), "PNG über 2048 Pixel wurde angenommen")

# ---------------------------------------------------------------------------
# Verkleinerung für Seitensymbole: Mehrheitsfarbe je Block
# ---------------------------------------------------------------------------
big = DrawingModel.blank(128)
big.paint_shape("rect_filled", 0, 0, 63, 63, 1, "#00AA00")
big.set_cell(70, 70, "#000000")
icon = big.downscaled(16)
assert icon.width == 16 and icon.color_at(0, 0) == "#00AA00" and icon.color_at(15, 15) == BACKGROUND
assert icon.color_at(8, 8) == BACKGROUND  # eine einzelne Zelle bleibt Minderheit
rejected(lambda: DrawingModel.blank(16).downscaled(32), "Vergrößerung über downscaled wurde angenommen")

print("test_drawing330: OK")
