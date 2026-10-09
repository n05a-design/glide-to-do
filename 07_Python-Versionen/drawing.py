"""Datenkern der Glide-Pixelzeichnung.

Das Modul ist absichtlich unabhängig von Tk und vom produktiven Glide-Bestand.
Es enthält das versionierte Zellmodell, Rückgängig je Aktion, die Werkzeuge
(Pinsel, Füllen mit Mustern, Formen, Symmetrie, pixelgenaue Linie, Bereiche),
Palettendateien, PNG-Ausgabe und das enge, statische Glide-SVG-Profil. Die
Oberfläche verwendet diesen Kern, ohne Darstellungszustände in die Zeichnung zu
schreiben.

Formatversion 1 beschreibt die feste 128-×-128-Fläche aus Glide 3.29.
Formatversion 2 (seit 3.30) erlaubt die quadratischen Größen 16, 32, 64 und
128. Eine 128-×-128-Zeichnung wird weiterhin als Version 1 geschrieben, damit
ihre Exporte auch ältere Glide-Fassungen lesen.
"""

from __future__ import annotations

from collections import deque
from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import json
import math
import re
import struct
from typing import Iterable, Sequence
import xml.etree.ElementTree as ET
import zlib


FORMAT_NAME = "glide.drawing"
FORMAT_VERSION = 1
FORMAT_VERSION_SIZED = 2
ENCODING = "hex8-row-v1"
COLOR_SPACE = "srgb"
WIDTH = 128
HEIGHT = 128
CELL_COUNT = WIDTH * HEIGHT
SIZES = (16, 32, 64, 128)
MAX_COLORS = 256
BACKGROUND = "#FFFFFF"
DEFAULT_PALETTE_ID = "glide-drawing-default"
DEFAULT_PALETTE_VERSION = 1
BRUSH_SIZES = (1, 2, 4, 8)
# Rückgängig nimmt seit 3.30 ganze Aktionen zurück: einen Pinselzug, eine
# Füllung, eine Form. Begrenzt sind die Zahl der Aktionen und die Summe der
# darin gemerkten Zellen, damit auch viele Vollflächenfüllungen den Speicher
# nicht sprengen.
UNDO_LIMIT = 50
UNDO_CELL_BUDGET = 8 * CELL_COUNT
MAX_JSON_BYTES = 512 * 1024
MAX_SVG_BYTES = 4 * 1024 * 1024
MAX_PNG_EDGE = 2048
PNG_SCALES = (1, 2, 4, 8, 16)
SYMMETRY_MODES = ("none", "x", "y", "xy")
FILL_PATTERNS = ("solid", "checker", "dots25", "dots75")
SHAPES = ("line", "rect", "rect_filled", "ellipse", "ellipse_filled")

# Glide-Inhaltspalette (ZF-210): 32 eigene Farben, versioniert. Sie gilt für
# neue Farbauswahl; vorhandene Zeichnungen behalten ihre konkreten Farben.
# Kräftiges Blau, Gelb und Pink stammen aus der Markenanmutung, dazu Grautöne,
# Natur- und Hauttöne für Motive.
GLIDE_PALETTE_ID = "glide-content"
GLIDE_PALETTE_VERSION = 1
GLIDE_PALETTE_NAME = "Glide 32"
GLIDE_PALETTE = (
    "#000000", "#3B3B3B", "#7A7A7A", "#B8B8B8", "#FFFFFF",
    "#1E88E5", "#0D47A1", "#64B5F6", "#00ACC1",
    "#FFD000", "#FFF176", "#FF9800", "#E65100",
    "#FF4F9A", "#F8BBD0", "#C2185B", "#E53935", "#8E0000",
    "#43A047", "#1B5E20", "#AED581", "#00897B",
    "#7E57C2", "#311B92", "#D1C4E9",
    "#8D6E63", "#4E342E", "#D7B899", "#F2D2B6", "#A0522D",
    "#263238", "#90A4AE",
)

SVG_NS = "http://www.w3.org/2000/svg"
GLIDE_NS = "urn:glide:drawing:1"
SVG = f"{{{SVG_NS}}}"
GLIDE = f"{{{GLIDE_NS}}}"

_COLOR_RE = re.compile(r"#[0-9A-F]{6}\Z")
_PALETTE_ID_RE = re.compile(r"[A-Za-z0-9._-]{1,64}\Z")
_MODEL_FIELDS = {
    "format", "format_version", "width", "height", "color_space",
    "palette_id", "palette_version", "palette", "encoding", "rows",
}
# Geordnetes 4-×-4-Raster (Bayer). Ein Wert unter der Schwelle erhält die
# erste Farbe; so entstehen gleichmäßige 25-, 50- und 75-Prozent-Muster.
_BAYER = ((0, 8, 2, 10), (12, 4, 14, 6), (3, 11, 1, 9), (15, 7, 13, 5))


class DrawingFormatError(ValueError):
    """Eine Zeichnungs-, Paletten- oder SVG-Datei verletzt den Vertrag."""


@dataclass(frozen=True, slots=True)
class CellChange:
    index: int
    before: int
    after: int


@dataclass(frozen=True, slots=True)
class DrawingAction:
    """Eine rücknehmbare Einheit: alle Zellen eines Zugs, einer Füllung, einer Form."""

    label: str
    changes: tuple[CellChange, ...]

    @property
    def count(self) -> int:
        return len(self.changes)


@dataclass(frozen=True, slots=True)
class Region:
    """Ein kopierter Bereich mit konkreten Farben, zeilenweise von oben links."""

    width: int
    height: int
    colors: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SvgImportResult:
    model: "DrawingModel"
    repaired: bool
    warnings: tuple[str, ...]


def normalize_color(value: str) -> str:
    if not isinstance(value, str):
        raise DrawingFormatError("Farbe muss Text im Format #RRGGBB sein")
    color = value.strip().upper()
    if not _COLOR_RE.fullmatch(color):
        raise DrawingFormatError(f"Ungültige sRGB-Farbe: {value!r}")
    return color


def check_size(size) -> int:
    if type(size) is not int or size not in SIZES:
        raise DrawingFormatError("Die Fläche muss 16, 32, 64 oder 128 Zellen breit sein")
    return size


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DrawingFormatError(f"Doppelter JSON-Schlüssel: {key}")
        result[key] = value
    return result


def _load_json(text: str) -> dict:
    if not isinstance(text, str):
        raise DrawingFormatError("Zeichnungsdaten müssen UTF-8-Text sein")
    if len(text.encode("utf-8")) > MAX_JSON_BYTES:
        raise DrawingFormatError("Zeichnungsdaten überschreiten 512 KiB")
    try:
        value = json.loads(text, object_pairs_hook=_unique_object)
    except DrawingFormatError:
        raise
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise DrawingFormatError(f"Ungültiges JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise DrawingFormatError("Das Zeichenmodell muss ein JSON-Objekt sein")
    return value


def canonical_json(document: dict) -> str:
    """Stabile UTF-8-Repräsentation für Export und SHA-256."""
    return json.dumps(
        document, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    )


# --- Geometrie ---------------------------------------------------------------

def brush_hits(u: float, v: float, size: int, width: int = WIDTH, height: int = HEIGHT,
               wrap: bool = False) -> tuple[tuple[int, int], ...]:
    """Zellen, die ein quadratischer Pinsel nach der Ein-Drittel-Regel trifft.

    Mit ``wrap`` erscheinen Treffer jenseits des Rands auf der Gegenseite –
    der Kachelmodus für nahtlose Muster.
    """
    if size not in BRUSH_SIZES:
        raise DrawingFormatError("Pinselgröße muss 1, 2, 4 oder 8 sein")
    if not all(isinstance(value, (int, float)) and math.isfinite(value) for value in (u, v)):
        raise DrawingFormatError("Pinselposition muss endlich sein")
    half = size / 2.0
    left, right = u - half, u + half
    top, bottom = v - half, v + half
    first_x, last_x = math.floor(left), math.ceil(right) - 1
    first_y, last_y = math.floor(top), math.ceil(bottom) - 1
    if not wrap:
        first_x, last_x = max(0, first_x), min(width - 1, last_x)
        first_y, last_y = max(0, first_y), min(height - 1, last_y)
    hits = []
    seen = set()
    for y in range(first_y, last_y + 1):
        overlap_y = max(0.0, min(bottom, y + 1.0) - max(top, float(y)))
        for x in range(first_x, last_x + 1):
            overlap_x = max(0.0, min(right, x + 1.0) - max(left, float(x)))
            if overlap_x * overlap_y + 1e-12 >= (1.0 / 3.0):
                cell = (x % width, y % height) if wrap else (x, y)
                if cell not in seen:
                    seen.add(cell)
                    hits.append(cell)
    if wrap:
        hits.sort(key=lambda cell: (cell[1], cell[0]))
    return tuple(hits)


def line_cells(x0: int, y0: int, x1: int, y1: int) -> list[tuple[int, int]]:
    """Lückenlose Zellfolge nach Bresenham, beide Endpunkte eingeschlossen."""
    cells = []
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    step_x = 1 if x0 < x1 else -1
    step_y = 1 if y0 < y1 else -1
    error = dx + dy
    x, y = x0, y0
    while True:
        cells.append((x, y))
        if x == x1 and y == y1:
            return cells
        double = 2 * error
        if double >= dy:
            error += dy
            x += step_x
        if double <= dx:
            error += dx
            y += step_y


def constrain_end(x0: int, y0: int, x1: int, y1: int, shape: str) -> tuple[int, int]:
    """Umschalt beim Aufziehen: Linie auf 0/45/90 Grad, Rechteck und Ellipse quadratisch."""
    dx, dy = x1 - x0, y1 - y0
    if shape == "line":
        if abs(dx) > 2 * abs(dy):
            return x1, y0
        if abs(dy) > 2 * abs(dx):
            return x0, y1
        length = max(abs(dx), abs(dy))
        return x0 + (length if dx >= 0 else -length), y0 + (length if dy >= 0 else -length)
    length = max(abs(dx), abs(dy))
    return x0 + (length if dx >= 0 else -length), y0 + (length if dy >= 0 else -length)


def _box(x0: int, y0: int, x1: int, y1: int) -> tuple[int, int, int, int]:
    return min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)


def rect_cells(x0: int, y0: int, x1: int, y1: int, filled: bool = False) -> list[tuple[int, int]]:
    left, top, right, bottom = _box(x0, y0, x1, y1)
    if filled:
        return [(x, y) for y in range(top, bottom + 1) for x in range(left, right + 1)]
    cells = []
    for x in range(left, right + 1):
        cells.append((x, top))
        if bottom != top:
            cells.append((x, bottom))
    for y in range(top + 1, bottom):
        cells.append((left, y))
        if right != left:
            cells.append((right, y))
    return cells


def ellipse_cells(x0: int, y0: int, x1: int, y1: int, filled: bool = False) -> list[tuple[int, int]]:
    """Ellipse im Rechteck der beiden Eckzellen, deckungsgleich spiegelbar."""
    left, top, right, bottom = _box(x0, y0, x1, y1)
    center_x, center_y = (left + right + 1) / 2.0, (top + bottom + 1) / 2.0
    radius_x, radius_y = (right - left + 1) / 2.0, (bottom - top + 1) / 2.0
    inside = set()
    for y in range(top, bottom + 1):
        ny = (y + 0.5 - center_y) / radius_y
        for x in range(left, right + 1):
            nx = (x + 0.5 - center_x) / radius_x
            if nx * nx + ny * ny <= 1.0 + 1e-9:
                inside.add((x, y))
    if not inside:
        inside = {(left, top)}
    if filled:
        return sorted(inside, key=lambda cell: (cell[1], cell[0]))
    outline = [
        (x, y) for x, y in inside
        if any((x + dx, y + dy) not in inside for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    ]
    return sorted(outline, key=lambda cell: (cell[1], cell[0]))


def shape_cells(shape: str, x0: int, y0: int, x1: int, y1: int) -> list[tuple[int, int]]:
    if shape == "line":
        return line_cells(x0, y0, x1, y1)
    if shape in ("rect", "rect_filled"):
        return rect_cells(x0, y0, x1, y1, filled=shape == "rect_filled")
    if shape in ("ellipse", "ellipse_filled"):
        return ellipse_cells(x0, y0, x1, y1, filled=shape == "ellipse_filled")
    raise DrawingFormatError(f"Unbekannte Form: {shape!r}")


def mirror_points(u: float, v: float, mode: str, width: int = WIDTH,
                  height: int = HEIGHT) -> list[tuple[float, float]]:
    """Zeigerposition und ihre Spiegelbilder an den Mittelachsen der Fläche.

    Die Achsen liegen auf Zellgrenzen. Weil die Ein-Drittel-Regel
    achsensymmetrisch ist, trifft das Spiegelbild genau die gespiegelten Zellen.
    """
    if mode not in SYMMETRY_MODES:
        raise DrawingFormatError("Unbekannte Symmetrie")
    points = [(u, v)]
    if mode in ("x", "xy"):
        points.append((width - u, v))
    if mode in ("y", "xy"):
        points.append((u, height - v))
    if mode == "xy":
        points.append((width - u, height - v))
    return points


def mirror_cells(cells: Iterable[tuple[int, int]], mode: str, width: int = WIDTH,
                 height: int = HEIGHT) -> list[tuple[int, int]]:
    if mode not in SYMMETRY_MODES:
        raise DrawingFormatError("Unbekannte Symmetrie")
    result = []
    seen = set()
    for x, y in cells:
        variants = [(x, y)]
        if mode in ("x", "xy"):
            variants.append((width - 1 - x, y))
        if mode in ("y", "xy"):
            variants.append((x, height - 1 - y))
        if mode == "xy":
            variants.append((width - 1 - x, height - 1 - y))
        for cell in variants:
            if cell not in seen:
                seen.add(cell)
                result.append(cell)
    return result


def pattern_primary(pattern: str, x: int, y: int) -> bool:
    """True, wenn eine Musterzelle die erste Farbe erhält."""
    if pattern == "solid":
        return True
    if pattern == "checker":
        return (x + y) % 2 == 0
    if pattern == "dots25":
        return _BAYER[y % 4][x % 4] < 4
    if pattern == "dots75":
        return _BAYER[y % 4][x % 4] < 12
    raise DrawingFormatError(f"Unbekanntes Füllmuster: {pattern!r}")


class PixelPerfectStroke:
    """Entfernt L-Ecken aus einer Freihandlinie mit 1-×-1-Pinsel.

    Eine Zelle, die mit ihrem Vorgänger und Nachfolger eine L-Ecke bildet,
    wird wieder zurückgesetzt – sofern der Zug sie nicht schon vorher bemalt
    hat. So entstehen die dünnen Linien, die Pixelgrafik ausmachen.
    """

    def __init__(self):
        self.cells: list[tuple[int, int]] = []
        self.visits: dict[tuple[int, int], int] = {}

    def add(self, cell: tuple[int, int]) -> tuple[int, int] | None:
        if self.cells and self.cells[-1] == cell:
            return None
        self.cells.append(cell)
        self.visits[cell] = self.visits.get(cell, 0) + 1
        if len(self.cells) < 3:
            return None
        (ax, ay), (bx, by), (cx, cy) = self.cells[-3:]
        corner = (abs(ax - cx) == 1 and abs(ay - cy) == 1
                  and abs(ax - bx) + abs(ay - by) == 1 and abs(cx - bx) + abs(cy - by) == 1)
        if not corner or self.visits.get((bx, by), 0) != 1:
            return None
        middle = self.cells.pop(-2)
        self.visits[middle] -= 1
        return middle


# --- Palettendateien ---------------------------------------------------------

def parse_palette(text: str, name_hint: str = "") -> tuple[str, list[str]]:
    """Liest eine GIMP-Palette (.gpl) oder eine Hex-Liste (.hex).

    Rückgabe: Name und eindeutige Farben in Dateireihenfolge. Eine fehlerhafte
    Datei wird vollständig abgelehnt; es gibt keine halbe Übernahme.
    """
    if not isinstance(text, str):
        raise DrawingFormatError("Palettendatei muss Text sein")
    if len(text) > 256 * 1024:
        raise DrawingFormatError("Palettendatei ist zu groß")
    lines = [line.strip() for line in text.replace("\r\n", "\n").split("\n")]
    name = " ".join(str(name_hint or "Palette").split())[:60] or "Palette"
    colors: list[str] = []
    if lines and lines[0].lower().startswith("gimp palette"):
        for number, line in enumerate(lines[1:], 2):
            if not line or line.startswith("#"):
                continue
            if line.lower().startswith("name:"):
                name = " ".join(line[5:].split())[:60] or name
                continue
            if line.lower().startswith("columns:"):
                continue
            parts = line.split()
            if len(parts) < 3 or not all(part.isdigit() for part in parts[:3]):
                raise DrawingFormatError(f"Zeile {number} ist keine Farbe (R G B Name)")
            red, green, blue = (int(part) for part in parts[:3])
            if max(red, green, blue) > 255:
                raise DrawingFormatError(f"Zeile {number}: Farbwerte müssen 0 bis 255 sein")
            colors.append(f"#{red:02X}{green:02X}{blue:02X}")
    else:
        for number, line in enumerate(lines, 1):
            if not line or line.startswith(";"):
                continue
            value = line if line.startswith("#") else "#" + line
            try:
                colors.append(normalize_color(value))
            except DrawingFormatError as exc:
                raise DrawingFormatError(f"Zeile {number} ist keine Hex-Farbe") from exc
    unique = list(dict.fromkeys(colors))
    if not unique:
        raise DrawingFormatError("Die Palette enthält keine Farbe")
    if len(unique) > MAX_COLORS:
        raise DrawingFormatError("Eine Palette darf höchstens 256 Farben enthalten")
    return name, unique


MAX_BINARY_PALETTE_BYTES = 16 * 1024 * 1024


def parse_binary_palette(data: bytes, name_hint: str = "") -> tuple[str, list[str]]:
    """Palette aus einer Aseprite-Datei oder aus Adobe-Farbfeldern (G20, 30.09.2026).

    Beide nutzen die Endung `.ase`; unterschieden wird am Dateianfang:
    Adobe Swatch Exchange beginnt mit `ASEF`, Aseprite trägt im Kopf die
    Kennung 0xA5E0. Gelesen wird nur die Palette, nie die Bilddaten. Wie bei
    Textpaletten gilt: alles oder nichts.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise DrawingFormatError("Palettendatei muss Binärdaten enthalten")
    if len(data) > MAX_BINARY_PALETTE_BYTES:
        raise DrawingFormatError("Palettendatei ist zu groß")
    name = " ".join(str(name_hint or "Palette").split())[:60] or "Palette"
    try:
        if data[:4] == b"ASEF":
            colors = _adobe_swatches(bytes(data))
        elif len(data) >= 128 and struct.unpack_from("<H", data, 4)[0] == 0xA5E0:
            colors = _aseprite_palette(bytes(data))
        else:
            raise DrawingFormatError("Weder Aseprite-Datei noch Adobe-Farbfelder")
    except struct.error as exc:
        raise DrawingFormatError("Die Datei ist unvollständig") from exc
    unique = list(dict.fromkeys(colors))
    if not unique:
        raise DrawingFormatError("Die Palette enthält keine Farbe")
    if len(unique) > MAX_COLORS:
        raise DrawingFormatError("Eine Palette darf höchstens 256 Farben enthalten")
    return name, unique


def _hex(red: float, green: float, blue: float) -> str:
    clamp = lambda value: max(0, min(255, int(round(value))))
    return f"#{clamp(red):02X}{clamp(green):02X}{clamp(blue):02X}"


def _adobe_swatches(data: bytes) -> list[str]:
    count = struct.unpack_from(">I", data, 8)[0]
    position, colors = 12, []
    for _ in range(count):
        kind, length = struct.unpack_from(">HI", data, position)
        body = position + 6
        position = body + length
        if kind != 0x0001:  # Gruppenanfang und -ende tragen keine Farbe
            continue
        name_chars = struct.unpack_from(">H", data, body)[0]
        model_at = body + 2 + 2 * name_chars
        model = data[model_at:model_at + 4]
        values_at = model_at + 4
        if model == b"RGB ":
            red, green, blue = struct.unpack_from(">fff", data, values_at)
            colors.append(_hex(red * 255, green * 255, blue * 255))
        elif model == b"Gray":
            (gray,) = struct.unpack_from(">f", data, values_at)
            colors.append(_hex(gray * 255, gray * 255, gray * 255))
        elif model == b"CMYK":
            cyan, magenta, yellow, key = struct.unpack_from(">ffff", data, values_at)
            colors.append(_hex(255 * (1 - cyan) * (1 - key), 255 * (1 - magenta) * (1 - key),
                               255 * (1 - yellow) * (1 - key)))
        else:
            raise DrawingFormatError("Farbfelder im Lab-Farbraum werden nicht unterstützt")
    return colors


def _aseprite_palette(data: bytes) -> list[str]:
    frames = struct.unpack_from("<H", data, 6)[0]
    position = 128
    for _ in range(max(1, frames)):
        frame_bytes, magic, old_chunks = struct.unpack_from("<IHH", data, position)
        if magic != 0xF1FA:
            raise DrawingFormatError("Aseprite-Datei ist beschädigt")
        new_chunks = struct.unpack_from("<I", data, position + 12)[0]
        chunk_count = new_chunks or old_chunks
        chunk = position + 16
        old_palette: list[str] = []
        for _chunk in range(chunk_count):
            size, kind = struct.unpack_from("<IH", data, chunk)
            body = chunk + 6
            if kind == 0x2019:  # neue Palette, mit Deckkraft und Namen
                entries, first, last = struct.unpack_from("<III", data, body)
                entry = body + 20
                colors = []
                for _index in range(first, last + 1):
                    flags, red, green, blue, alpha = struct.unpack_from("<HBBBB", data, entry)
                    entry += 6
                    if flags & 1:
                        entry += 2 + struct.unpack_from("<H", data, entry)[0]
                    if alpha:
                        colors.append(_hex(red, green, blue))
                return colors
            if kind in (0x0004, 0x0011):  # alte Palette (0..255 bzw. 0..63)
                packets = struct.unpack_from("<H", data, body)[0]
                entry = body + 2
                factor = 255 / 63 if kind == 0x0011 else 1
                for _packet in range(packets):
                    count = data[entry + 1] or 256
                    entry += 2
                    for _color in range(count):
                        red, green, blue = data[entry:entry + 3]
                        old_palette.append(_hex(red * factor, green * factor, blue * factor))
                        entry += 3
            chunk += size
        if old_palette:
            return old_palette
        position += frame_bytes
    raise DrawingFormatError("Die Aseprite-Datei enthält keine Palette")


def palette_to_gpl(name: str, colors: Sequence[str]) -> str:
    clean = " ".join(str(name or "Palette").split())[:60] or "Palette"
    lines = ["GIMP Palette", f"Name: {clean}", "#"]
    for color in colors:
        value = normalize_color(color)
        red, green, blue = (int(value[index:index + 2], 16) for index in (1, 3, 5))
        lines.append(f"{red:3d} {green:3d} {blue:3d}\t{value}")
    return "\n".join(lines) + "\n"


def palette_to_hex(colors: Sequence[str]) -> str:
    return "\n".join(normalize_color(color)[1:] for color in colors) + "\n"


# --- PNG ---------------------------------------------------------------------

def _png_chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def encode_indexed_png(width: int, height: int, palette: Sequence[str], cells: Sequence[int],
                       scale: int = 1) -> bytes:
    """Indiziertes PNG ohne Glättung; jede Zelle wird ein Quadrat aus scale Pixeln."""
    if type(scale) is not int or scale < 1 or max(width, height) * scale > MAX_PNG_EDGE:
        raise DrawingFormatError(f"Das PNG darf höchstens {MAX_PNG_EDGE} Pixel breit sein")
    plte = b"".join(bytes.fromhex(normalize_color(color)[1:]) for color in palette)
    raw = bytearray()
    for y in range(height):
        row = bytes(cells[y * width:(y + 1) * width])
        line = b"\x00" + (row if scale == 1 else bytes(value for value in row for _ in range(scale)))
        raw.extend(line * scale)
    header = struct.pack(">IIBBBBB", width * scale, height * scale, 8, 3, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + _png_chunk(b"IHDR", header) + _png_chunk(b"PLTE", plte)
            + _png_chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + _png_chunk(b"IEND", b""))


# --- Symbole (ICO, G16 vom 30.09.2026) ------------------------------------------

ICON_SIZES = (16, 32, 48, 256)


def resample_cells(width: int, cells: Sequence[int], target: int) -> list[int]:
    """Quadratische Zellen auf `target` Kantenlänge, ohne Glättung.

    Ganzzahlige Vergrößerung wiederholt jede Zelle; sonst nimmt jedes Zielpixel
    die Zelle unter seiner Mitte (nächster Nachbar). So bleiben harte
    Pixelkanten erhalten; Mischfarben entstehen nie.
    """
    if target < 1:
        raise DrawingFormatError("Symbolgröße muss positiv sein")
    result = []
    for y in range(target):
        source_y = min(width - 1, (2 * y + 1) * width // (2 * target))
        row = source_y * width
        for x in range(target):
            result.append(cells[row + min(width - 1, (2 * x + 1) * width // (2 * target))])
    return result


def encode_rgba_png(size: int, pixels: Sequence[tuple[int, int, int, int]]) -> bytes:
    """Quadratisches RGBA-PNG (Farbtyp 6); so erwartet Windows PNG-Bilder in ICO-Dateien."""
    raw = bytearray()
    for y in range(size):
        raw.append(0)
        for red, green, blue, alpha in pixels[y * size:(y + 1) * size]:
            raw.extend((red, green, blue, alpha))
    header = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + _png_chunk(b"IHDR", header)
            + _png_chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + _png_chunk(b"IEND", b""))


def icon_rgba(width: int, palette: Sequence[str], cells: Sequence[int], size: int,
              transparent_background: bool = True) -> list[tuple[int, int, int, int]]:
    """RGBA-Pixel eines Symbolbilds – dieselbe Rechnung für Export und Vorschau (G-03)."""
    rgba = []
    for index, color in enumerate(palette):
        value = normalize_color(color)
        alpha = 0 if (index == 0 and transparent_background) else 255
        rgba.append((int(value[1:3], 16), int(value[3:5], 16), int(value[5:7], 16), alpha))
    return [rgba[value] for value in resample_cells(width, cells, size)]


def icon_preview_rows(width: int, palette: Sequence[str], cells: Sequence[int], size: int,
                      background: str = BACKGROUND, transparent_background: bool = True) -> list[list[str]]:
    """Zeilen aus Hexfarben für die Symbolvorschau auf einem Grund (G-03 seit 3.35.0).

    Durchsichtige Pixel zeigen den Grund; sonst genau die Exportfarbe – die
    Vorschau ist damit pixelgleich zum ICO-Bild derselben Größe.
    """
    grund = normalize_color(background)
    pixel = icon_rgba(width, palette, cells, size, transparent_background)
    zeilen = []
    for y in range(size):
        zeile = []
        for red, green, blue, alpha in pixel[y * size:(y + 1) * size]:
            zeile.append(grund if alpha == 0 else f"#{red:02X}{green:02X}{blue:02X}")
        zeilen.append(zeile)
    return zeilen


def encode_ico(width: int, palette: Sequence[str], cells: Sequence[int],
               sizes: Sequence[int] = ICON_SIZES, transparent_background: bool = True) -> bytes:
    """ICO mit je einem PNG-Bild pro Größe (Windows ab Vista, alle Browser als Favicon).

    Der unbemalte Grund (Farbindex 0) wird auf Wunsch durchsichtig. Auch
    macOS und Linux lesen ICO; für Websites ist es die übliche `favicon.ico`.
    """
    sizes = tuple(dict.fromkeys(int(size) for size in sizes))
    if not sizes or any(size < 1 or size > 256 for size in sizes):
        raise DrawingFormatError("Symbolgrößen müssen zwischen 1 und 256 Pixel liegen")
    images = [encode_rgba_png(size, icon_rgba(width, palette, cells, size, transparent_background))
              for size in sizes]
    header = struct.pack("<HHH", 0, 1, len(images))
    offset = 6 + 16 * len(images)
    entries = bytearray()
    for size, data in zip(sizes, images):
        edge = 0 if size == 256 else size
        entries.extend(struct.pack("<BBBBHHII", edge, edge, 0, 0, 1, 32, len(data), offset))
        offset += len(data)
    return header + bytes(entries) + b"".join(images)


# --- Modell ------------------------------------------------------------------

class DrawingModel:
    """Eine Zeichnung mit fester quadratischer Fläche, Palette und Aktions-Undo."""

    def __init__(
        self,
        palette: Sequence[str] | None = None,
        cells: Sequence[int] | bytes | bytearray | None = None,
        *,
        palette_id: str = DEFAULT_PALETTE_ID,
        palette_version: int = DEFAULT_PALETTE_VERSION,
        undo_limit: int = UNDO_LIMIT,
        size: int = WIDTH,
    ):
        size = check_size(size)
        normalized = [normalize_color(color) for color in (palette or [BACKGROUND])]
        if not normalized or normalized[0] != BACKGROUND:
            raise DrawingFormatError("palette[0] muss #FFFFFF sein")
        if len(normalized) > MAX_COLORS:
            raise DrawingFormatError("Eine Zeichnung darf höchstens 256 Farben enthalten")
        if len(set(normalized)) != len(normalized):
            raise DrawingFormatError("Palettenfarben müssen eindeutig sein")
        if not isinstance(palette_id, str) or not _PALETTE_ID_RE.fullmatch(palette_id):
            raise DrawingFormatError("Ungültige Palettenkennung")
        if type(palette_version) is not int or not 1 <= palette_version <= 1_000_000:
            raise DrawingFormatError("Ungültige Palettenversion")
        if type(undo_limit) is not int or undo_limit < 1:
            raise DrawingFormatError("Undo-Limit muss eine positive Ganzzahl sein")

        count = size * size
        raw_cells = bytearray(count) if cells is None else bytearray(cells)
        if len(raw_cells) != count:
            raise DrawingFormatError(f"Eine Zeichnung benötigt genau {count} Zellen")
        if raw_cells and max(raw_cells) >= len(normalized):
            raise DrawingFormatError("Eine Zelle verweist außerhalb der Palette")

        self.width = size
        self.height = size
        self.palette = normalized
        self.palette_id = palette_id
        self.palette_version = palette_version
        self.cells = raw_cells
        self.undo_limit = undo_limit
        self._undo: deque[DrawingAction] = deque(maxlen=undo_limit)
        self._redo: list[DrawingAction] = []
        self._open: dict[int, list[int]] | None = None
        self._open_label = ""
        self._open_depth = 0

    @property
    def size(self) -> int:
        return self.width

    @property
    def cell_count(self) -> int:
        return self.width * self.height

    @classmethod
    def blank(cls, size: int = WIDTH) -> "DrawingModel":
        return cls(size=size)

    @classmethod
    def from_document(cls, raw: dict) -> "DrawingModel":
        if not isinstance(raw, dict):
            raise DrawingFormatError("Das Zeichenmodell muss ein Objekt sein")
        unknown = set(raw) - _MODEL_FIELDS
        missing = _MODEL_FIELDS - set(raw)
        if unknown:
            raise DrawingFormatError("Unbekannte Modellfelder: " + ", ".join(sorted(unknown)))
        if missing:
            raise DrawingFormatError("Fehlende Modellfelder: " + ", ".join(sorted(missing)))
        version = raw.get("format_version")
        if type(version) is not int or version not in (FORMAT_VERSION, FORMAT_VERSION_SIZED):
            raise DrawingFormatError("Ungültiger Wert für format_version")
        width, height = raw.get("width"), raw.get("height")
        if type(width) is not int or type(height) is not int or width != height:
            raise DrawingFormatError("Ungültiger Wert für width")
        if version == FORMAT_VERSION and width != WIDTH:
            raise DrawingFormatError("Ungültiger Wert für width")
        if width not in SIZES:
            raise DrawingFormatError("Ungültiger Wert für width")
        for key, value in (("format", FORMAT_NAME), ("color_space", COLOR_SPACE), ("encoding", ENCODING)):
            if raw.get(key) != value:
                raise DrawingFormatError(f"Ungültiger Wert für {key}")

        palette = raw.get("palette")
        if not isinstance(palette, list):
            raise DrawingFormatError("palette muss eine Liste sein")
        model = cls(
            palette,
            palette_id=raw.get("palette_id"),
            palette_version=raw.get("palette_version"),
            size=width,
        )
        rows = raw.get("rows")
        if not isinstance(rows, list) or len(rows) != height:
            raise DrawingFormatError(f"rows muss genau {height} Zeilen enthalten")
        row_re = re.compile(r"[0-9A-F]{%d}\Z" % (2 * width))
        cells = bytearray()
        for number, row in enumerate(rows, 1):
            if not isinstance(row, str) or not row_re.fullmatch(row):
                raise DrawingFormatError(f"Zeile {number} muss {2 * width} große Hexzeichen enthalten")
            decoded = bytes.fromhex(row)
            if decoded and max(decoded) >= len(model.palette):
                raise DrawingFormatError(f"Zeile {number} enthält einen ungültigen Palettenindex")
            cells.extend(decoded)
        model.cells = cells
        return model

    @classmethod
    def from_json(cls, value: str | bytes) -> "DrawingModel":
        if isinstance(value, bytes):
            try:
                value = value.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise DrawingFormatError("Zeichnungsdatei ist kein gültiges UTF-8") from exc
        return cls.from_document(_load_json(value))

    def to_document(self) -> dict:
        rows = []
        for y in range(self.height):
            start = y * self.width
            rows.append(bytes(self.cells[start:start + self.width]).hex().upper())
        return {
            "format": FORMAT_NAME,
            "format_version": FORMAT_VERSION if self.width == WIDTH else FORMAT_VERSION_SIZED,
            "width": self.width,
            "height": self.height,
            "color_space": COLOR_SPACE,
            "palette_id": self.palette_id,
            "palette_version": self.palette_version,
            "palette": list(self.palette),
            "encoding": ENCODING,
            "rows": rows,
        }

    def to_json(self) -> str:
        return canonical_json(self.to_document())

    def model_hash(self) -> str:
        return hashlib.sha256(self.to_json().encode("utf-8")).hexdigest()

    def copy(self) -> "DrawingModel":
        return DrawingModel(self.palette, self.cells, palette_id=self.palette_id,
                            palette_version=self.palette_version, size=self.width)

    def _index(self, x: int, y: int) -> int:
        if type(x) is not int or type(y) is not int or not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Zellkoordinate liegt außerhalb der Zeichenfläche")
        return y * self.width + x

    def contains(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def color_index_at(self, x: int, y: int) -> int:
        return self.cells[self._index(x, y)]

    def color_at(self, x: int, y: int) -> str:
        return self.palette[self.color_index_at(x, y)]

    def ensure_color(self, color: str) -> int:
        normalized = normalize_color(color)
        try:
            return self.palette.index(normalized)
        except ValueError:
            if len(self.palette) >= MAX_COLORS:
                raise DrawingFormatError("Die Palette enthält bereits 256 Farben")
            self.palette.append(normalized)
            return len(self.palette) - 1

    def _color_index(self, color: str | int) -> int:
        index = self.ensure_color(color) if isinstance(color, str) else color
        if type(index) is not int or not 0 <= index < len(self.palette):
            raise DrawingFormatError("Ungültiger Palettenindex")
        return index

    def used_colors(self) -> list[str]:
        """Farben, die tatsächlich in Zellen vorkommen, nach Häufigkeit."""
        counts: dict[int, int] = {}
        for value in self.cells:
            counts[value] = counts.get(value, 0) + 1
        ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        return [self.palette[index] for index, _count in ordered]

    # --- Rückgängig je Aktion ------------------------------------------------
    def begin_action(self, label: str = "Änderung") -> None:
        """Öffnet eine Aktion; verschachtelte Aufrufe gehören zur äußeren."""
        if self._open is not None:
            self._open_depth += 1
            return
        self._open = {}
        self._open_label = str(label or "Änderung")[:60]
        self._open_depth = 1

    def end_action(self) -> DrawingAction | None:
        if self._open is None:
            return None
        self._open_depth -= 1
        if self._open_depth > 0:
            return None
        changes = tuple(CellChange(index, values[0], values[1])
                        for index, values in self._open.items() if values[0] != values[1])
        label = self._open_label
        self._open = None
        self._open_label = ""
        self._open_depth = 0
        if not changes:
            return None
        action = DrawingAction(label, changes)
        self._push(action)
        return action

    @contextmanager
    def action(self, label: str = "Änderung"):
        self.begin_action(label)
        try:
            yield self
        finally:
            self.end_action()

    @property
    def action_open(self) -> bool:
        return self._open is not None

    def _push(self, action: DrawingAction) -> None:
        self._undo.append(action)
        self._redo.clear()
        total = sum(entry.count for entry in self._undo)
        while len(self._undo) > 1 and total > UNDO_CELL_BUDGET:
            total -= self._undo.popleft().count

    def _set_index(self, index: int, color_index: int, *, record: bool = True) -> bool:
        if type(color_index) is not int or not 0 <= color_index < len(self.palette):
            raise DrawingFormatError("Ungültiger Palettenindex")
        before = self.cells[index]
        if before == color_index:
            return False
        self.cells[index] = color_index
        if record:
            if self._open is not None:
                entry = self._open.get(index)
                if entry is None:
                    self._open[index] = [before, color_index]
                else:
                    entry[1] = color_index
            else:
                self._push(DrawingAction("Zelle", (CellChange(index, before, color_index),)))
        return True

    def revert_open_action(self) -> int:
        """Setzt alle Zellen der offenen Aktion auf ihren Anfangswert (Formvorschau)."""
        if self._open is None:
            return 0
        count = 0
        for index, values in self._open.items():
            if self.cells[index] != values[0]:
                self.cells[index] = values[0]
                count += 1
            values[1] = values[0]
        return count

    def discard_open_action(self, palette_length: int | None = None) -> int:
        """Verwirft die offene Aktion ohne Verlaufseintrag – etwa eine abgelehnte Vorschau (G19).

        Farben, die erst in dieser Aktion hinten an die Palette kamen und danach
        unbenutzt sind, fallen wieder weg; `palette_length` ist die Länge davor.
        Liefert die Zahl zurückgesetzter Zellen.
        """
        count = self.revert_open_action()
        self._open = None
        self._open_label = ""
        self._open_depth = 0
        if palette_length is not None and 0 < palette_length < len(self.palette):
            used = set(self.cells)
            if not any(index in used for index in range(palette_length, len(self.palette))):
                del self.palette[palette_length:]
        return count

    def restore_in_action(self, x: int, y: int) -> bool:
        """Setzt eine in der offenen Aktion geänderte Zelle auf ihren Anfangswert."""
        if self._open is None:
            return False
        index = self._index(x, y)
        entry = self._open.get(index)
        if entry is None or self.cells[index] == entry[0]:
            return False
        self.cells[index] = entry[0]
        entry[1] = entry[0]
        return True

    def set_cell(self, x: int, y: int, color: str | int) -> bool:
        return self._set_index(self._index(x, y), self._color_index(color))

    @property
    def undo_count(self) -> int:
        return len(self._undo)

    @property
    def redo_count(self) -> int:
        return len(self._redo)

    def peek_undo(self) -> DrawingAction | None:
        return self._undo[-1] if self._undo else None

    def peek_redo(self) -> DrawingAction | None:
        return self._redo[-1] if self._redo else None

    def clear_history(self) -> None:
        self._undo.clear()
        self._redo.clear()

    def undo(self) -> DrawingAction | None:
        if self._open is not None:
            self._open_depth = 1
            self.end_action()
        if not self._undo:
            return None
        action = self._undo.pop()
        for change in reversed(action.changes):
            self.cells[change.index] = change.before
        self._redo.append(action)
        return action

    def redo(self) -> DrawingAction | None:
        if not self._redo:
            return None
        action = self._redo.pop()
        for change in action.changes:
            self.cells[change.index] = change.after
        self._undo.append(action)
        return action

    # --- Werkzeuge -------------------------------------------------------------
    @staticmethod
    def brush_cells(u: float, v: float, size: int) -> tuple[tuple[int, int], ...]:
        """Treffer auf der Standardfläche 128 × 128 (Schnittstelle aus 3.29)."""
        return brush_hits(u, v, size)

    def hits(self, u: float, v: float, size: int, wrap: bool = False) -> tuple[tuple[int, int], ...]:
        return brush_hits(u, v, size, self.width, self.height, wrap)

    def paint_cells(self, cells: Iterable[tuple[int, int]], color: str | int) -> int:
        color_index = self._color_index(color)
        changed = 0
        for x, y in cells:
            if self.contains(x, y):
                changed += self._set_index(y * self.width + x, color_index)
        return changed

    def paint_brush(self, u: float, v: float, size: int, color: str | int, wrap: bool = False) -> int:
        return self.paint_cells(self.hits(u, v, size, wrap), self._color_index(color))

    def paint_path(
        self,
        points: Iterable[tuple[float, float]],
        size: int,
        color: str | int,
        wrap: bool = False,
    ) -> int:
        points = list(points)
        if not points:
            return 0
        color_index = self._color_index(color)
        changed = 0
        previous = points[0]
        changed += self.paint_brush(*previous, size, color_index, wrap)
        for current in points[1:]:
            if len(current) != 2:
                raise DrawingFormatError("Ein Pfadpunkt benötigt x und y")
            dx, dy = current[0] - previous[0], current[1] - previous[1]
            steps = max(1, math.ceil(max(abs(dx), abs(dy)) * 8.0))
            for step in range(1, steps + 1):
                ratio = step / steps
                changed += self.paint_brush(
                    previous[0] + dx * ratio,
                    previous[1] + dy * ratio,
                    size,
                    color_index,
                    wrap,
                )
            previous = current
        return changed

    def paint_shape(self, shape: str, x0: int, y0: int, x1: int, y1: int, size: int,
                    color: str | int, symmetry: str = "none") -> int:
        """Linie, Rechteck oder Ellipse; Umrisse in Pinselstärke."""
        color_index = self._color_index(color)
        cells = shape_cells(shape, x0, y0, x1, y1)
        cells = mirror_cells(cells, symmetry, self.width, self.height)
        if size == 1 or shape.endswith("_filled"):
            return self.paint_cells(cells, color_index)
        changed = 0
        for x, y in cells:
            changed += self.paint_brush(x + 0.5, y + 0.5, size, color_index)
        return changed

    def flood_region(self, x: int, y: int) -> list[int]:
        """Zusammenhängende gleichfarbige Zellen (links, rechts, oben, unten)."""
        start = self._index(x, y)
        target = self.cells[start]
        region = []
        seen = bytearray(self.cell_count)
        seen[start] = 1
        queue = deque([start])
        width, height = self.width, self.height
        while queue:
            index = queue.popleft()
            region.append(index)
            cx, cy = index % width, index // width
            for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                if 0 <= nx < width and 0 <= ny < height:
                    neighbor = ny * width + nx
                    if not seen[neighbor] and self.cells[neighbor] == target:
                        seen[neighbor] = 1
                        queue.append(neighbor)
        return region

    def fill(self, x: int, y: int, color: str | int, pattern: str = "solid",
             secondary: str | int | None = None) -> int:
        replacement = self._color_index(color)
        if pattern not in FILL_PATTERNS:
            raise DrawingFormatError(f"Unbekanntes Füllmuster: {pattern!r}")
        other = replacement if pattern == "solid" or secondary is None else self._color_index(secondary)
        target = self.cells[self._index(x, y)]
        if pattern == "solid" and target == replacement:
            return 0
        changed = 0
        for index in self.flood_region(x, y):
            cx, cy = index % self.width, index // self.width
            value = replacement if pattern_primary(pattern, cx, cy) else other
            changed += self._set_index(index, value)
        return changed

    def replace_color(self, old: str | int, new: str | int) -> int:
        """Ersetzt eine Farbe in der ganzen Zeichnung."""
        old_index = self.palette.index(normalize_color(old)) if isinstance(old, str) else old
        if type(old_index) is not int or not 0 <= old_index < len(self.palette):
            raise DrawingFormatError("Unbekannte Farbe")
        new_index = self._color_index(new)
        if old_index == new_index:
            return 0
        changed = 0
        for index, value in enumerate(self.cells):
            if value == old_index:
                changed += self._set_index(index, new_index)
        return changed

    def unused_palette_count(self) -> int:
        used = set(self.cells) | {0}
        return len(self.palette) - len(used)

    def compact_palette(self) -> int:
        """Entfernt unbenutzte Palettenfarben. Leert das Rückgängig."""
        used = sorted(set(self.cells) | {0})
        if len(used) == len(self.palette):
            return 0
        mapping = {old: new for new, old in enumerate(used)}
        removed = len(self.palette) - len(used)
        self.palette = [self.palette[index] for index in used]
        self.cells = bytearray(mapping[value] for value in self.cells)
        self.clear_history()
        return removed

    # --- Bereiche --------------------------------------------------------------
    def clip_box(self, x0: int, y0: int, x1: int, y1: int) -> tuple[int, int, int, int] | None:
        left, top, right, bottom = _box(x0, y0, x1, y1)
        left, top = max(0, left), max(0, top)
        right, bottom = min(self.width - 1, right), min(self.height - 1, bottom)
        if left > right or top > bottom:
            return None
        return left, top, right, bottom

    def copy_region(self, x0: int, y0: int, x1: int, y1: int) -> Region | None:
        box = self.clip_box(x0, y0, x1, y1)
        if box is None:
            return None
        left, top, right, bottom = box
        colors = tuple(self.palette[self.cells[y * self.width + x]]
                       for y in range(top, bottom + 1) for x in range(left, right + 1))
        return Region(right - left + 1, bottom - top + 1, colors)

    def clear_region(self, x0: int, y0: int, x1: int, y1: int) -> int:
        box = self.clip_box(x0, y0, x1, y1)
        if box is None:
            return 0
        left, top, right, bottom = box
        return self.paint_cells(((x, y) for y in range(top, bottom + 1) for x in range(left, right + 1)), 0)

    def stamp_region(self, region: Region, x: int, y: int, skip_white: bool = False) -> int:
        """Setzt einen Bereich mit oberer linker Ecke bei (x, y); Ränder werden abgeschnitten."""
        needed = [color for color in dict.fromkeys(region.colors) if color not in self.palette]
        if len(self.palette) + len(needed) > MAX_COLORS:
            raise DrawingFormatError("Die Palette enthält bereits 256 Farben")
        changed = 0
        for row in range(region.height):
            for column in range(region.width):
                color = region.colors[row * region.width + column]
                if skip_white and color == BACKGROUND:
                    continue
                cx, cy = x + column, y + row
                if self.contains(cx, cy):
                    changed += self._set_index(cy * self.width + cx, self.ensure_color(color))
        return changed

    # --- Ausgabe ---------------------------------------------------------------
    def downscaled(self, size: int) -> "DrawingModel":
        """Verkleinerung nach Mehrheitsfarbe je Block, etwa für ein Seitensymbol."""
        size = check_size(size)
        if size > self.width:
            raise DrawingFormatError("Eine Zeichnung kann nur verkleinert werden")
        block = self.width // size
        result = DrawingModel(size=size)
        for by in range(size):
            for bx in range(size):
                counts: dict[int, int] = {}
                for y in range(by * block, (by + 1) * block):
                    start = y * self.width + bx * block
                    for value in self.cells[start:start + block]:
                        counts[value] = counts.get(value, 0) + 1
                best = max(counts.items(), key=lambda item: (item[1], item[0] != 0, -item[0]))[0]
                result.cells[by * size + bx] = result.ensure_color(self.palette[best])
        return result

    def to_png(self, scale: int = 1) -> bytes:
        return encode_indexed_png(self.width, self.height, self.palette, self.cells, scale)

    def to_ico(self, sizes: Sequence[int] = ICON_SIZES, transparent_background: bool = True) -> bytes:
        return encode_ico(self.width, self.palette, self.cells, sizes, transparent_background)

    def artwork_records(self) -> tuple[str, ...]:
        records = [f"B,0,0,{self.width},{self.height},{BACKGROUND}"]
        for y in range(self.height):
            x = 0
            while x < self.width:
                color_index = self.cells[y * self.width + x]
                start = x
                x += 1
                while x < self.width and self.cells[y * self.width + x] == color_index:
                    x += 1
                if color_index:
                    records.append(f"R,{y},{start},{x - start},{self.palette[color_index]}")
        return tuple(records)

    def artwork_bytes(self) -> bytes:
        return ("\n".join(self.artwork_records()) + "\n").encode("utf-8")

    def artwork_hash(self) -> str:
        return hashlib.sha256(self.artwork_bytes()).hexdigest()

    def to_svg(self, title: str = "Glide-Zeichnung") -> str:
        title = " ".join(str(title or "Glide-Zeichnung").split())[:200]
        ET.register_namespace("", SVG_NS)
        ET.register_namespace("glide", GLIDE_NS)
        size = str(self.width)
        root = ET.Element(SVG + "svg", {
            "version": "1.1", "width": size, "height": size,
            "viewBox": f"0 0 {size} {size}",
            "preserveAspectRatio": "xMidYMid meet",
        })
        ET.SubElement(root, SVG + "title").text = title
        ET.SubElement(root, SVG + "desc").text = f"{size} × {size} logische Zellen"
        metadata = ET.SubElement(root, SVG + "metadata")
        drawing = ET.SubElement(metadata, GLIDE + "drawing",
                                {"version": "1" if self.width == WIDTH else "2"})
        ET.SubElement(drawing, GLIDE + "manifest", {
            "model-sha256": self.model_hash(),
            "artwork-sha256": self.artwork_hash(),
        })
        ET.SubElement(drawing, GLIDE + "model", {
            "media-type": "application/json",
        }).text = self.to_json()
        ET.SubElement(root, SVG + "rect", {
            "x": "0", "y": "0", "width": size, "height": size,
            "fill": BACKGROUND,
        })
        group = ET.SubElement(root, SVG + "g", {
            "id": "glide-artwork", "shape-rendering": "crispEdges",
        })
        for record in self.artwork_records()[1:]:
            _kind, y, x, width, color = record.split(",")
            ET.SubElement(group, SVG + "rect", {
                "x": x, "y": y, "width": width, "height": "1", "fill": color,
            })
        xml = ET.tostring(root, encoding="unicode", short_empty_elements=True)
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + xml + "\n"


def _exact_attributes(element: ET.Element, expected: set[str], context: str):
    actual = set(element.attrib)
    if actual != expected:
        raise DrawingFormatError(
            f"{context}: Attribute müssen {sorted(expected)} sein; erhalten {sorted(actual)}"
        )


def _parse_int_attribute(element: ET.Element, name: str, *, minimum: int, maximum: int) -> int:
    value = element.get(name, "")
    if not re.fullmatch(r"0|[1-9][0-9]*", value):
        raise DrawingFormatError(f"SVG-Attribut {name} muss eine Ganzzahl sein")
    number = int(value)
    if not minimum <= number <= maximum:
        raise DrawingFormatError(f"SVG-Attribut {name} liegt außerhalb der Fläche")
    return number


def import_glide_svg(value: str | bytes) -> SvgImportResult:
    """Ein enges Glide-SVG prüfen und sein eingebettetes Zellmodell lesen.

    Geänderte Modellmetadaten dürfen als bewusste Textbearbeitung übernommen
    werden. Änderungen allein an der sichtbaren Grafik werden abgelehnt.
    """
    if isinstance(value, bytes):
        if len(value) > MAX_SVG_BYTES:
            raise DrawingFormatError("SVG überschreitet 4 MiB")
        try:
            text = value.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise DrawingFormatError("SVG ist kein gültiges UTF-8") from exc
    elif isinstance(value, str):
        text = value
        if len(text.encode("utf-8")) > MAX_SVG_BYTES:
            raise DrawingFormatError("SVG überschreitet 4 MiB")
    else:
        raise DrawingFormatError("SVG muss Text oder UTF-8-Bytes sein")

    lowered = text.lower()
    if any(token in lowered for token in ("<!doctype", "<!entity", "<![cdata[", "<!--")):
        raise DrawingFormatError("DOCTYPE, ENTITY, CDATA und Kommentare sind nicht erlaubt")
    without_declaration = re.sub(r"\A﻿?\s*<\?xml\s+[^?]*\?>", "", text, count=1, flags=re.I)
    if "<?" in without_declaration:
        raise DrawingFormatError("Verarbeitungsanweisungen sind nicht erlaubt")
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        raise DrawingFormatError(f"Ungültiges XML: {exc}") from exc

    count = 0
    stack = [(root, 1)]
    allowed_tags = {
        SVG + "svg", SVG + "title", SVG + "desc", SVG + "metadata",
        SVG + "rect", SVG + "g", GLIDE + "drawing", GLIDE + "manifest",
        GLIDE + "model",
    }
    while stack:
        element, depth = stack.pop()
        count += 1
        if count > 4096 or depth > 8:
            raise DrawingFormatError("SVG-Struktur ist zu groß oder zu tief")
        if element.tag not in allowed_tags:
            raise DrawingFormatError(f"Nicht erlaubtes SVG-Element: {element.tag}")
        if any(len(str(key)) > 80 or len(str(item)) > 512 for key, item in element.attrib.items()):
            raise DrawingFormatError("SVG-Attribut ist zu lang")
        if element.text and len(element.text) > MAX_JSON_BYTES:
            raise DrawingFormatError("SVG-Textknoten ist zu lang")
        if element.tail and element.tail.strip():
            raise DrawingFormatError("Text zwischen SVG-Elementen ist nicht erlaubt")
        stack.extend((child, depth + 1) for child in element)

    if root.tag != SVG + "svg":
        raise DrawingFormatError("Wurzelelement muss svg im SVG-Namensraum sein")
    _exact_attributes(root, {"version", "width", "height", "viewBox", "preserveAspectRatio"}, "svg")
    size_text = root.get("width", "")
    size = int(size_text) if size_text.isdigit() and str(int(size_text)) == size_text else 0
    if size not in SIZES:
        raise DrawingFormatError("SVG-Koordinatenraum entspricht nicht dem Glide-Profil")
    expected_root = {
        "version": "1.1", "width": str(size), "height": str(size),
        "viewBox": f"0 0 {size} {size}", "preserveAspectRatio": "xMidYMid meet",
    }
    if root.attrib != expected_root:
        raise DrawingFormatError("SVG-Koordinatenraum entspricht nicht dem Glide-Profil")
    children = list(root)
    expected_tags = [SVG + name for name in ("title", "desc", "metadata", "rect", "g")]
    if [child.tag for child in children] != expected_tags:
        raise DrawingFormatError("SVG benötigt title, desc, metadata, Hintergrund und glide-artwork")
    title, desc, metadata, background, group = children
    _exact_attributes(title, set(), "title")
    _exact_attributes(desc, set(), "desc")
    if len(title) or len(desc):
        raise DrawingFormatError("Titel und Beschreibung dürfen keine Unterelemente enthalten")
    if len(title.text or "") > 200 or len(desc.text or "") > 300:
        raise DrawingFormatError("Titel oder Beschreibung ist zu lang")

    _exact_attributes(metadata, set(), "metadata")
    if len(metadata) != 1 or metadata[0].tag != GLIDE + "drawing":
        raise DrawingFormatError("Glide-Metadaten fehlen")
    drawing = metadata[0]
    _exact_attributes(drawing, {"version"}, "glide:drawing")
    expected_version = "1" if size == WIDTH else "2"
    if drawing.get("version") != expected_version or len(drawing) != 2:
        raise DrawingFormatError("Unbekannte Glide-SVG-Version")
    manifest, model_element = drawing
    if manifest.tag != GLIDE + "manifest" or model_element.tag != GLIDE + "model":
        raise DrawingFormatError("Glide-Manifest oder Zeichenmodell fehlt")
    _exact_attributes(manifest, {"model-sha256", "artwork-sha256"}, "glide:manifest")
    _exact_attributes(model_element, {"media-type"}, "glide:model")
    if len(manifest) or (manifest.text or "").strip():
        raise DrawingFormatError("Glide-Manifest darf keine Inhalte enthalten")
    if model_element.get("media-type") != "application/json" or len(model_element):
        raise DrawingFormatError("Glide-Modell muss ein JSON-Textknoten sein")
    for name in ("model-sha256", "artwork-sha256"):
        if not re.fullmatch(r"[0-9a-f]{64}", manifest.get(name, "")):
            raise DrawingFormatError(f"Ungültige Prüfsumme {name}")
    model = DrawingModel.from_json(model_element.text or "")
    if model.width != size:
        raise DrawingFormatError("SVG-Größe und Zeichenmodell passen nicht zusammen")

    _exact_attributes(background, {"x", "y", "width", "height", "fill"}, "Hintergrund")
    if background.attrib != {
        "x": "0", "y": "0", "width": str(size), "height": str(size), "fill": BACKGROUND,
    } or len(background):
        raise DrawingFormatError("SVG-Hintergrund entspricht nicht dem Glide-Profil")
    _exact_attributes(group, {"id", "shape-rendering"}, "glide-artwork")
    if group.attrib != {"id": "glide-artwork", "shape-rendering": "crispEdges"}:
        raise DrawingFormatError("SVG-Grafikgruppe entspricht nicht dem Glide-Profil")

    visible = DrawingModel(
        model.palette,
        palette_id=model.palette_id,
        palette_version=model.palette_version,
        size=size,
    )
    source_records = [f"B,0,0,{size},{size},{BACKGROUND}"]
    occupied = bytearray(size * size)
    previous_key = (-1, -1)
    for element in group:
        if element.tag != SVG + "rect" or len(element) or (element.text or "").strip():
            raise DrawingFormatError("glide-artwork darf nur leere rect-Elemente enthalten")
        _exact_attributes(element, {"x", "y", "width", "height", "fill"}, "Artwork-Rechteck")
        x = _parse_int_attribute(element, "x", minimum=0, maximum=size - 1)
        y = _parse_int_attribute(element, "y", minimum=0, maximum=size - 1)
        width = _parse_int_attribute(element, "width", minimum=1, maximum=size)
        height = _parse_int_attribute(element, "height", minimum=1, maximum=1)
        if x + width > size or height != 1:
            raise DrawingFormatError("Artwork-Rechteck liegt außerhalb der Fläche")
        color = normalize_color(element.get("fill"))
        if color == BACKGROUND:
            raise DrawingFormatError("Weiße Läufe gehören nicht in glide-artwork")
        try:
            color_index = model.palette.index(color)
        except ValueError as exc:
            raise DrawingFormatError("Artwork-Farbe fehlt in der Palette") from exc
        if (y, x) <= previous_key:
            raise DrawingFormatError("Artwork-Rechtecke sind nicht nach y und x sortiert")
        previous_key = (y, x)
        for cell_x in range(x, x + width):
            index = y * size + cell_x
            if occupied[index]:
                raise DrawingFormatError("Artwork-Rechtecke überlappen sich")
            occupied[index] = 1
            visible.cells[index] = color_index
        source_records.append(f"R,{y},{x},{width},{color}")

    if tuple(source_records) != visible.artwork_records():
        raise DrawingFormatError("Artwork-Rechtecke sind nicht maximal zusammengefasst")
    visible_hash = visible.artwork_hash()
    actual_model_hash = model.model_hash()
    declared_model_hash = manifest.get("model-sha256")
    declared_artwork_hash = manifest.get("artwork-sha256")
    model_changed = declared_model_hash != actual_model_hash
    artwork_changed = declared_artwork_hash != visible_hash
    matches_model = visible.cells == model.cells

    if not model_changed and artwork_changed:
        raise DrawingFormatError("Die sichtbare Grafik wurde ohne passendes Modell verändert")
    if not matches_model and not model_changed:
        raise DrawingFormatError("Die sichtbare Grafik widerspricht dem unveränderten Modell")
    if not matches_model and model_changed and artwork_changed:
        raise DrawingFormatError("Modell und sichtbare Grafik wurden widersprüchlich verändert")

    warnings = []
    if model_changed and not artwork_changed and not matches_model:
        warnings.append("Zeichenmodell wurde als Text geändert; sichtbare Grafik wird neu erzeugt")
    elif model_changed and artwork_changed and matches_model:
        warnings.append("Modell und Grafik wurden geändert; Prüfsummen werden neu erzeugt")
    elif model_changed:
        warnings.append("Modellprüfsumme wird neu erzeugt")
    return SvgImportResult(model=model, repaired=bool(warnings), warnings=tuple(warnings))
