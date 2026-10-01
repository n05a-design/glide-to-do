"""Datenkern für Glides geplante 128-x-128-Pixel-Zeichenfläche.

Das Modul ist absichtlich unabhängig von Tk und vom produktiven Glide-Bestand.
Es enthält das versionierte Zellmodell, zellweises Undo/Redo, die drei
Kernwerkzeuge und das enge, statische Glide-SVG-Profil. Die spätere Oberfläche
kann diesen Kern verwenden, ohne Darstellungszustände in die Zeichnung zu
schreiben.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import hashlib
import json
import math
import re
from typing import Iterable, Sequence
import xml.etree.ElementTree as ET


FORMAT_NAME = "glide.drawing"
FORMAT_VERSION = 1
ENCODING = "hex8-row-v1"
COLOR_SPACE = "srgb"
WIDTH = 128
HEIGHT = 128
CELL_COUNT = WIDTH * HEIGHT
MAX_COLORS = 256
BACKGROUND = "#FFFFFF"
DEFAULT_PALETTE_ID = "glide-drawing-default"
DEFAULT_PALETTE_VERSION = 1
BRUSH_SIZES = (1, 2, 4, 8)
UNDO_LIMIT = 20
MAX_JSON_BYTES = 512 * 1024
MAX_SVG_BYTES = 4 * 1024 * 1024

SVG_NS = "http://www.w3.org/2000/svg"
GLIDE_NS = "urn:glide:drawing:1"
SVG = f"{{{SVG_NS}}}"
GLIDE = f"{{{GLIDE_NS}}}"

_COLOR_RE = re.compile(r"#[0-9A-F]{6}\Z")
_PALETTE_ID_RE = re.compile(r"[A-Za-z0-9._-]{1,64}\Z")
_HEX_ROW_RE = re.compile(r"[0-9A-F]{256}\Z")
_MODEL_FIELDS = {
    "format", "format_version", "width", "height", "color_space",
    "palette_id", "palette_version", "palette", "encoding", "rows",
}


class DrawingFormatError(ValueError):
    """Eine Zeichnungs- oder SVG-Datei verletzt den festgelegten Vertrag."""


@dataclass(frozen=True, slots=True)
class CellChange:
    index: int
    before: int
    after: int


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


class DrawingModel:
    """Eine Zeichnung mit fester Fläche, Palette und kleinem Zell-Undo."""

    def __init__(
        self,
        palette: Sequence[str] | None = None,
        cells: Sequence[int] | bytes | bytearray | None = None,
        *,
        palette_id: str = DEFAULT_PALETTE_ID,
        palette_version: int = DEFAULT_PALETTE_VERSION,
        undo_limit: int = UNDO_LIMIT,
    ):
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

        raw_cells = bytearray(CELL_COUNT) if cells is None else bytearray(cells)
        if len(raw_cells) != CELL_COUNT:
            raise DrawingFormatError(f"Eine Zeichnung benötigt genau {CELL_COUNT} Zellen")
        if raw_cells and max(raw_cells) >= len(normalized):
            raise DrawingFormatError("Eine Zelle verweist außerhalb der Palette")

        self.palette = normalized
        self.palette_id = palette_id
        self.palette_version = palette_version
        self.cells = raw_cells
        self.undo_limit = undo_limit
        self._undo: deque[CellChange] = deque(maxlen=undo_limit)
        self._redo: list[CellChange] = []

    @classmethod
    def blank(cls) -> "DrawingModel":
        return cls()

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
        expected = {
            "format": FORMAT_NAME,
            "format_version": FORMAT_VERSION,
            "width": WIDTH,
            "height": HEIGHT,
            "color_space": COLOR_SPACE,
            "encoding": ENCODING,
        }
        for key, value in expected.items():
            if raw.get(key) != value or (type(value) is int and type(raw.get(key)) is not int):
                raise DrawingFormatError(f"Ungültiger Wert für {key}")

        palette = raw.get("palette")
        if not isinstance(palette, list):
            raise DrawingFormatError("palette muss eine Liste sein")
        model = cls(
            palette,
            palette_id=raw.get("palette_id"),
            palette_version=raw.get("palette_version"),
        )
        rows = raw.get("rows")
        if not isinstance(rows, list) or len(rows) != HEIGHT:
            raise DrawingFormatError("rows muss genau 128 Zeilen enthalten")
        cells = bytearray()
        for number, row in enumerate(rows, 1):
            if not isinstance(row, str) or not _HEX_ROW_RE.fullmatch(row):
                raise DrawingFormatError(f"Zeile {number} muss 256 große Hexzeichen enthalten")
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
        for y in range(HEIGHT):
            start = y * WIDTH
            rows.append(bytes(self.cells[start:start + WIDTH]).hex().upper())
        return {
            "format": FORMAT_NAME,
            "format_version": FORMAT_VERSION,
            "width": WIDTH,
            "height": HEIGHT,
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

    @staticmethod
    def _index(x: int, y: int) -> int:
        if type(x) is not int or type(y) is not int or not (0 <= x < WIDTH and 0 <= y < HEIGHT):
            raise IndexError("Zellkoordinate liegt außerhalb der Zeichenfläche")
        return y * WIDTH + x

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

    def _set_index(self, index: int, color_index: int, *, record: bool = True) -> bool:
        if type(color_index) is not int or not 0 <= color_index < len(self.palette):
            raise DrawingFormatError("Ungültiger Palettenindex")
        before = self.cells[index]
        if before == color_index:
            return False
        self.cells[index] = color_index
        if record:
            self._undo.append(CellChange(index, before, color_index))
            self._redo.clear()
        return True

    def set_cell(self, x: int, y: int, color: str | int) -> bool:
        color_index = self.ensure_color(color) if isinstance(color, str) else color
        return self._set_index(self._index(x, y), color_index)

    @property
    def undo_count(self) -> int:
        return len(self._undo)

    @property
    def redo_count(self) -> int:
        return len(self._redo)

    def undo(self) -> CellChange | None:
        if not self._undo:
            return None
        change = self._undo.pop()
        self.cells[change.index] = change.before
        self._redo.append(change)
        return change

    def redo(self) -> CellChange | None:
        if not self._redo:
            return None
        change = self._redo.pop()
        self.cells[change.index] = change.after
        self._undo.append(change)
        return change

    @staticmethod
    def brush_cells(u: float, v: float, size: int) -> tuple[tuple[int, int], ...]:
        if size not in BRUSH_SIZES:
            raise DrawingFormatError("Pinselgröße muss 1, 2, 4 oder 8 sein")
        if not all(isinstance(value, (int, float)) and math.isfinite(value) for value in (u, v)):
            raise DrawingFormatError("Pinselposition muss endlich sein")
        half = size / 2.0
        left, right = u - half, u + half
        top, bottom = v - half, v + half
        first_x = max(0, math.floor(left))
        last_x = min(WIDTH - 1, math.ceil(right) - 1)
        first_y = max(0, math.floor(top))
        last_y = min(HEIGHT - 1, math.ceil(bottom) - 1)
        hits = []
        for y in range(first_y, last_y + 1):
            overlap_y = max(0.0, min(bottom, y + 1.0) - max(top, float(y)))
            for x in range(first_x, last_x + 1):
                overlap_x = max(0.0, min(right, x + 1.0) - max(left, float(x)))
                if overlap_x * overlap_y + 1e-12 >= (1.0 / 3.0):
                    hits.append((x, y))
        return tuple(hits)

    def paint_brush(self, u: float, v: float, size: int, color: str | int) -> int:
        color_index = self.ensure_color(color) if isinstance(color, str) else color
        changed = 0
        for x, y in self.brush_cells(u, v, size):
            changed += self._set_index(self._index(x, y), color_index)
        return changed

    def paint_path(
        self,
        points: Iterable[tuple[float, float]],
        size: int,
        color: str | int,
    ) -> int:
        points = list(points)
        if not points:
            return 0
        color_index = self.ensure_color(color) if isinstance(color, str) else color
        changed = 0
        previous = points[0]
        changed += self.paint_brush(*previous, size, color_index)
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
                )
            previous = current
        return changed

    def fill(self, x: int, y: int, color: str | int) -> int:
        start = self._index(x, y)
        replacement = self.ensure_color(color) if isinstance(color, str) else color
        if type(replacement) is not int or not 0 <= replacement < len(self.palette):
            raise DrawingFormatError("Ungültiger Palettenindex")
        target = self.cells[start]
        if target == replacement:
            return 0
        queue = deque([start])
        seen = bytearray(CELL_COUNT)
        seen[start] = 1
        changed = 0
        while queue:
            index = queue.popleft()
            if self.cells[index] != target:
                continue
            changed += self._set_index(index, replacement)
            cx, cy = index % WIDTH, index // WIDTH
            for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                    neighbor = ny * WIDTH + nx
                    if not seen[neighbor] and self.cells[neighbor] == target:
                        seen[neighbor] = 1
                        queue.append(neighbor)
        return changed

    def artwork_records(self) -> tuple[str, ...]:
        records = [f"B,0,0,{WIDTH},{HEIGHT},{BACKGROUND}"]
        for y in range(HEIGHT):
            x = 0
            while x < WIDTH:
                color_index = self.cells[y * WIDTH + x]
                start = x
                x += 1
                while x < WIDTH and self.cells[y * WIDTH + x] == color_index:
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
        root = ET.Element(SVG + "svg", {
            "version": "1.1", "width": str(WIDTH), "height": str(HEIGHT),
            "viewBox": f"0 0 {WIDTH} {HEIGHT}",
            "preserveAspectRatio": "xMidYMid meet",
        })
        ET.SubElement(root, SVG + "title").text = title
        ET.SubElement(root, SVG + "desc").text = "128 × 128 logische Zellen"
        metadata = ET.SubElement(root, SVG + "metadata")
        drawing = ET.SubElement(metadata, GLIDE + "drawing", {"version": "1"})
        ET.SubElement(drawing, GLIDE + "manifest", {
            "model-sha256": self.model_hash(),
            "artwork-sha256": self.artwork_hash(),
        })
        ET.SubElement(drawing, GLIDE + "model", {
            "media-type": "application/json",
        }).text = self.to_json()
        ET.SubElement(root, SVG + "rect", {
            "x": "0", "y": "0", "width": str(WIDTH), "height": str(HEIGHT),
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
    without_declaration = re.sub(r"\A\ufeff?\s*<\?xml\s+[^?]*\?>", "", text, count=1, flags=re.I)
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
    expected_root = {
        "version": "1.1", "width": "128", "height": "128",
        "viewBox": "0 0 128 128", "preserveAspectRatio": "xMidYMid meet",
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
    if drawing.get("version") != "1" or len(drawing) != 2:
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

    _exact_attributes(background, {"x", "y", "width", "height", "fill"}, "Hintergrund")
    if background.attrib != {
        "x": "0", "y": "0", "width": "128", "height": "128", "fill": BACKGROUND,
    } or len(background):
        raise DrawingFormatError("SVG-Hintergrund entspricht nicht dem Glide-Profil")
    _exact_attributes(group, {"id", "shape-rendering"}, "glide-artwork")
    if group.attrib != {"id": "glide-artwork", "shape-rendering": "crispEdges"}:
        raise DrawingFormatError("SVG-Grafikgruppe entspricht nicht dem Glide-Profil")

    visible = DrawingModel(
        model.palette,
        palette_id=model.palette_id,
        palette_version=model.palette_version,
    )
    source_records = [f"B,0,0,{WIDTH},{HEIGHT},{BACKGROUND}"]
    occupied = bytearray(CELL_COUNT)
    previous_key = (-1, -1)
    for element in group:
        if element.tag != SVG + "rect" or len(element) or (element.text or "").strip():
            raise DrawingFormatError("glide-artwork darf nur leere rect-Elemente enthalten")
        _exact_attributes(element, {"x", "y", "width", "height", "fill"}, "Artwork-Rechteck")
        x = _parse_int_attribute(element, "x", minimum=0, maximum=WIDTH - 1)
        y = _parse_int_attribute(element, "y", minimum=0, maximum=HEIGHT - 1)
        width = _parse_int_attribute(element, "width", minimum=1, maximum=WIDTH)
        height = _parse_int_attribute(element, "height", minimum=1, maximum=1)
        if x + width > WIDTH or height != 1:
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
            index = y * WIDTH + cell_x
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
