"""Isolierte Vertragstests für das Zeichenmodell und Glide-SVG."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src/glide"))

from drawing import (  # noqa: E402
    BACKGROUND,
    CELL_COUNT,
    GLIDE,
    SVG,
    UNDO_CELL_BUDGET,
    UNDO_LIMIT,
    DrawingFormatError,
    DrawingModel,
    import_glide_svg,
)


def rejected(action, message):
    try:
        action()
    except DrawingFormatError:
        return
    raise AssertionError(message)


# Das feste Zeilenmodell bleibt unabhängig von Zoom, Tk und SVG.
blank = DrawingModel.blank()
document = blank.to_document()
assert len(document["rows"]) == 128
assert all(len(row) == 256 for row in document["rows"])
assert len(blank.cells) == CELL_COUNT and set(blank.cells) == {0}
assert DrawingModel.from_json(blank.to_json()).to_json() == blank.to_json()

with_duplicate = blank.to_json().replace('"width":128', '"width":128,"width":128')
rejected(lambda: DrawingModel.from_json(with_duplicate), "Doppelte JSON-Schlüssel wurden angenommen")
broken = dict(document)
broken["rows"] = document["rows"][:-1]
rejected(lambda: DrawingModel.from_document(broken), "127 Zeilen wurden angenommen")
broken = dict(document)
broken["future"] = True
rejected(lambda: DrawingModel.from_document(broken), "Unbekanntes Pflichtfeld wurde still verworfen")

# Farben sind konkret, eindeutig und auf 256 Einträge begrenzt.
black = blank.ensure_color("#000000")
assert black == blank.ensure_color("#000000") == 1
assert blank.palette == [BACKGROUND, "#000000"]
rejected(
    lambda: DrawingModel([BACKGROUND] + [f"#{number:06X}" for number in range(1, 257)]),
    "Mehr als 256 Farben wurden angenommen",
)

# Die Ein-Drittel-Regel bleibt bei Zentren, Grenzen und Ecken deterministisch.
assert DrawingModel.brush_cells(0.5, 0.5, 1) == ((0, 0),)
assert DrawingModel.brush_cells(1.0, 0.5, 1) == ((0, 0), (1, 0))
assert DrawingModel.brush_cells(1.0, 1.0, 1) == ()
left = set(DrawingModel.brush_cells(31.0, 40.5, 4))
right = {(60 - x, y) for x, y in DrawingModel.brush_cells(30.0, 40.5, 4)}
assert left == right

# Schnelle Mausbewegungen erzeugen eine lückenlose Spur in logischen Zellen.
stroke = DrawingModel([BACKGROUND, "#000000"])
assert stroke.paint_path([(0.5, 10.5), (127.5, 10.5)], 1, 1) == 128
assert all(stroke.color_index_at(x, 10) == 1 for x in range(128))

# Füllen verwendet nur links, rechts, oben und unten.
fill = DrawingModel([BACKGROUND, "#AA0000", "#0000AA"])
fill.set_cell(4, 4, 1)
fill.set_cell(5, 5, 1)
fill._undo.clear()
assert fill.fill(4, 4, 2) == 1
assert fill.color_index_at(4, 4) == 2
assert fill.color_index_at(5, 5) == 1

# Seit 3.30 nimmt Rückgängig ganze Aktionen zurück (Entscheidung E-11 vom
# 25.09.2026): einen Zug, eine Füllung, eine Form. Einzelne set_cell-Aufrufe
# außerhalb einer Aktion bleiben je eine eigene Aktion.
undo = DrawingModel([BACKGROUND, "#000000"])
for x in range(25):
    undo.set_cell(x, 0, 1)
assert undo.undo_count == 25
for _ in range(25):
    assert undo.undo() is not None
assert undo.undo() is None
assert [undo.color_index_at(x, 0) for x in range(25)] == [0] * 25
for _ in range(25):
    assert undo.redo() is not None
undo.undo()
undo.set_cell(127, 127, 1)
assert undo.redo() is None

stroke_undo = DrawingModel([BACKGROUND, "#000000"])
with stroke_undo.action("Pinselzug"):
    stroke_undo.paint_path([(0.5, 3.5), (60.5, 3.5)], 8, 1)
assert stroke_undo.undo_count == 1 and stroke_undo.peek_undo().label == "Pinselzug"
painted_cells = sum(value == 1 for value in stroke_undo.cells)
assert painted_cells == stroke_undo.peek_undo().count > 64
assert stroke_undo.undo().count == painted_cells
assert set(stroke_undo.cells) == {0}
assert stroke_undo.redo() is not None and sum(value == 1 for value in stroke_undo.cells) == painted_cells

# Eine Vollfüllung ist in einem Schritt vollständig rücknehmbar.
large_fill = DrawingModel([BACKGROUND, "#123456"])
with large_fill.action("Füllen"):
    assert large_fill.fill(0, 0, 1) == CELL_COUNT
assert large_fill.undo_count == 1
large_fill.undo()
assert set(large_fill.cells) == {0}

# Zelle, die innerhalb einer Aktion hin- und zurückgesetzt wird, ist kein Schritt.
neutral = DrawingModel([BACKGROUND, "#000000"])
with neutral.action("Hin und zurück"):
    neutral.set_cell(1, 1, 1)
    neutral.set_cell(1, 1, 0)
assert neutral.undo_count == 0

# Die Zahl der Aktionen und die Summe der Zellen sind begrenzt.
many = DrawingModel([BACKGROUND, "#000000"])
for index in range(UNDO_LIMIT + 5):
    many.set_cell(index % 128, index // 128, 1)
assert many.undo_count == UNDO_LIMIT
budget = DrawingModel([BACKGROUND, "#000000", "#FF0000"])
for round_number in range(12):
    with budget.action("Füllen"):
        budget.fill(0, 0, 1 + round_number % 2)
assert sum(action.count for action in budget._undo) <= UNDO_CELL_BUDGET
assert budget.undo_count >= 1

# Eigenes SVG bleibt Standard-SVG und führt sämtliche Zellfarben rund.
image = DrawingModel([BACKGROUND, "#000000", "#2B7DE9"])
image.paint_path([(5.5, 8.5), (20.5, 8.5)], 1, 2)
image.set_cell(100, 100, 1)
svg = image.to_svg("Rundlauf & Prüfung")
assert svg.startswith('<?xml version="1.0" encoding="UTF-8"?>')
assert "<script" not in svg and "<path" not in svg and "viewBox=\"0 0 128 128\"" in svg
result = import_glide_svg(svg)
assert result.repaired is False and result.warnings == ()
assert result.model.to_json() == image.to_json()
assert result.model.to_svg("Rundlauf & Prüfung") == svg

# Das eingebettete Modell darf als Text geändert werden. Die sichtbare Grafik
# gilt dann als alte Vorschau und wird nach bestätigtem Import neu erzeugt.
root = ET.fromstring(svg)
drawing = root.find(f"{SVG}metadata/{GLIDE}drawing")
model_element = drawing.find(f"{GLIDE}model")
edited = json.loads(model_element.text)
row = edited["rows"][12]
edited["rows"][12] = row[:24] + "01" + row[26:]
model_element.text = json.dumps(edited, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
edited_svg = ET.tostring(root, encoding="unicode")
repaired = import_glide_svg(edited_svg)
assert repaired.repaired and repaired.model.color_index_at(12, 12) == 1
assert "sichtbare Grafik wird neu erzeugt" in repaired.warnings[0]

# Änderungen nur an der Grafik und aktive beziehungsweise externe Inhalte
# werden vor einer Bestandsänderung abgelehnt.
graphic_only = svg.replace('x="100" y="100"', 'x="101" y="100"')
rejected(lambda: import_glide_svg(graphic_only), "Grafikänderung ohne Modell wurde angenommen")
with_script = svg.replace("<metadata>", "<script>alert(1)</script><metadata>")
rejected(lambda: import_glide_svg(with_script), "SVG-Skript wurde angenommen")
nested_script = svg.replace("<title>Rundlauf &amp; Prüfung</title>",
                            "<title>Rundlauf<script>alert(1)</script></title>")
rejected(lambda: import_glide_svg(nested_script), "Verschachteltes SVG-Skript wurde angenommen")
with_image = svg.replace("<metadata>", '<image href="https://example.invalid/a.png"/><metadata>')
rejected(lambda: import_glide_svg(with_image), "Externe SVG-Ressource wurde angenommen")
with_doctype = svg.replace("<svg ", '<!DOCTYPE svg [<!ENTITY x "y">]><svg ', 1)
rejected(lambda: import_glide_svg(with_doctype), "DOCTYPE wurde angenommen")

print("test_drawing: OK")
