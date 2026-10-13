"""Lokale Pixelbildfolgen, Zeitachse und PNG-Ausgabe ohne Tk.

Jeder Frame behält ein gewöhnliches DrawingModel samt seinem Zell-Undo.
Strukturaktionen und ihr Undo führt der aufrufende Bestandsrahmen aus.
Die aktive Bearbeitung und die Vorschau sind keine gespeicherten Daten.
"""
from dataclasses import dataclass
import hashlib
import json
import math
import re
import struct
from uuid import uuid4
import zlib

from drawing import DrawingFormatError, DrawingModel, canonical_json, check_size

FORMAT = "glide.animation"
FORMAT_VERSION = 1
DEFAULT_DURATION_MS = 150
MIN_DURATION_MS = 20
MAX_DURATION_MS = 60_000
MAX_FRAMES = 120
MAX_JSON_BYTES = 12 * 1024 * 1024
MAX_SHEET_EDGE = 8192
MAX_SHEET_PIXELS = 16_777_216
_ID = re.compile(r"[A-Za-z0-9_-]{1,64}\Z")


def duration(value):
    if type(value) is not int or not MIN_DURATION_MS <= value <= MAX_DURATION_MS:
        raise DrawingFormatError("Die Bilddauer muss 20 bis 60.000 Millisekunden betragen.")
    return value


def frame_id(value):
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise DrawingFormatError("Ungültige Frame-Kennung.")
    return value


def _json_document(text):
    if isinstance(text, bytes):
        try:
            text = text.decode("utf-8")
        except UnicodeError as exc:
            raise DrawingFormatError("Die Bildfolge braucht gültiges UTF-8.") from exc
    if not isinstance(text, str) or len(text.encode("utf-8")) > MAX_JSON_BYTES:
        raise DrawingFormatError("Die Bildfolge darf höchstens 12 MiB belegen.")
    def unique(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise DrawingFormatError("Doppelter JSON-Schlüssel: " + key)
            value[key] = item
        return value
    try:
        document = json.loads(text, object_pairs_hook=unique)
    except (ValueError, RecursionError) as exc:
        raise DrawingFormatError("Ungültige Animationsdaten: " + str(exc)) from exc
    return document


@dataclass(slots=True)
class Frame:
    id: str
    model: DrawingModel
    duration_ms: int | None = None


@dataclass(frozen=True, slots=True)
class Playback:
    index: int
    frame_id: str
    remaining_ms: int
    finished: bool


class Animation:
    def __init__(self, frames, duration_ms=DEFAULT_DURATION_MS):
        frames = list(frames)
        self.duration_ms = duration(duration_ms)
        if not 1 <= len(frames) <= MAX_FRAMES:
            raise DrawingFormatError("Eine Bildfolge braucht 1 bis 120 Frames.")
        identities = set()
        size = None
        for frame in frames:
            if not isinstance(frame, Frame) or not isinstance(frame.model, DrawingModel):
                raise DrawingFormatError("Ein Frame braucht ein gültiges Pixelmodell.")
            frame_id(frame.id)
            if frame.id in identities:
                raise DrawingFormatError("Doppelte Frame-Kennung.")
            identities.add(frame.id)
            if frame.duration_ms is not None:
                duration(frame.duration_ms)
            if size is not None and frame.model.width != size:
                raise DrawingFormatError("Alle Frames müssen dieselbe Fläche haben.")
            size = frame.model.width
        self.frames = frames

    @property
    def size(self):
        return self.frames[0].model.width

    @classmethod
    def from_legacy(cls, document):
        return cls([Frame("frame-1", DrawingModel.from_document(document))])

    @classmethod
    def from_document(cls, raw):
        fields = {"format", "format_version", "width", "height", "duration_ms", "frames"}
        if not isinstance(raw, dict) or set(raw) != fields:
            raise DrawingFormatError("Die Bildfolge enthält fehlende oder unbekannte Felder.")
        if raw["format"] != FORMAT or type(raw["format_version"]) is not int or raw["format_version"] != FORMAT_VERSION:
            raise DrawingFormatError("Unbekanntes Animationsformat.")
        size = check_size(raw["width"])
        if type(raw["height"]) is not int or raw["height"] != size:
            raise DrawingFormatError("Die Bildfolge muss quadratisch sein.")
        if not isinstance(raw["frames"], list) or not 1 <= len(raw["frames"]) <= MAX_FRAMES:
            raise DrawingFormatError("Eine Bildfolge braucht 1 bis 120 Frames.")
        frames = []
        for value in raw["frames"]:
            if not isinstance(value, dict) or set(value) != {"id", "drawing", "duration_ms"}:
                raise DrawingFormatError("Ein Frame enthält fehlende oder unbekannte Felder.")
            model = DrawingModel.from_document(value["drawing"])
            if model.width != size:
                raise DrawingFormatError("Framefläche und Animationsfläche unterscheiden sich.")
            frames.append(Frame(value["id"], model, value["duration_ms"]))
        return cls(frames, raw["duration_ms"])

    @classmethod
    def from_json(cls, text):
        return cls.from_document(_json_document(text))

    def to_document(self):
        return {"format": FORMAT, "format_version": FORMAT_VERSION,
                "width": self.size, "height": self.size, "duration_ms": self.duration_ms,
                "frames": [{"id": frame.id, "drawing": frame.model.to_document(),
                            "duration_ms": frame.duration_ms} for frame in self.frames]}

    def to_json(self):
        return canonical_json(self.to_document())

    def model_hash(self):
        return hashlib.sha256(self.to_json().encode("utf-8")).hexdigest()

    def index(self, identity):
        for index, frame in enumerate(self.frames):
            if frame.id == identity:
                return index
        raise DrawingFormatError("Der Frame ist nicht mehr vorhanden.")

    def _new_id(self, value):
        identity = frame_id(value if value is not None else uuid4().hex)
        if any(frame.id == identity for frame in self.frames):
            raise DrawingFormatError("Doppelte Frame-Kennung.")
        return identity

    def add(self, after=None, *, identity=None):
        if len(self.frames) >= MAX_FRAMES:
            raise DrawingFormatError("Eine Bildfolge darf höchstens 120 Frames enthalten.")
        index = len(self.frames) if after is None else self.index(after) + 1
        frame = Frame(self._new_id(identity), DrawingModel.blank(self.size))
        self.frames.insert(index, frame)
        return frame.id

    def duplicate(self, identity, *, new_identity=None):
        if len(self.frames) >= MAX_FRAMES:
            raise DrawingFormatError("Eine Bildfolge darf höchstens 120 Frames enthalten.")
        index = self.index(identity)
        source = self.frames[index]
        frame = Frame(self._new_id(new_identity), source.model.copy(), source.duration_ms)
        self.frames.insert(index + 1, frame)
        return frame.id

    def remove(self, identity):
        index = self.index(identity)
        if len(self.frames) == 1:
            raise DrawingFormatError("Der letzte Frame bleibt erhalten.")
        self.frames.pop(index)
        return self.frames[min(index, len(self.frames) - 1)].id

    def move(self, identity, target):
        index = self.index(identity)
        if type(target) is not int or not 0 <= target < len(self.frames):
            raise DrawingFormatError("Ungültige Frameposition.")
        if target == index:
            return False
        self.frames.insert(target, self.frames.pop(index))
        return True

    def replace_model(self, identity, model):
        """Ein Bild ersetzen, weitere Bilder und Zeitachse erhalten."""
        index = self.index(identity)
        if not isinstance(model, DrawingModel):
            raise DrawingFormatError("Kein gültiges Pixelmodell.")
        if len(self.frames) > 1 and model.width != self.size:
            raise DrawingFormatError("Ein Bild einer Folge braucht dieselbe Fläche; eine andere Größe als neue Zeichnung anlegen.")
        checked = DrawingModel.from_document(model.to_document())
        self.frames[index].model = checked

    def set_duration(self, value, identity=None):
        if identity is None:
            value = duration(value)
            changed = self.duration_ms != value
            self.duration_ms = value
        else:
            frame = self.frames[self.index(identity)]
            value = None if value is None else duration(value)
            changed = frame.duration_ms != value
            frame.duration_ms = value
        return changed

    def durations(self):
        return tuple(frame.duration_ms if frame.duration_ms is not None else self.duration_ms
                     for frame in self.frames)

    def playback(self, elapsed_ms, *, loop=True):
        if (isinstance(elapsed_ms, bool) or not isinstance(elapsed_ms, (int, float))
                or (isinstance(elapsed_ms, float) and not math.isfinite(elapsed_ms)) or elapsed_ms < 0):
            raise DrawingFormatError("Ungültiger Zeitpunkt für die Vorschau.")
        times = self.durations()
        total = sum(times)
        if not loop and elapsed_ms >= total:
            return Playback(len(times) - 1, self.frames[-1].id, 0, True)
        position = elapsed_ms % total
        for index, milliseconds in enumerate(times):
            if position < milliseconds:
                return Playback(index, self.frames[index].id,
                                max(1, math.ceil(milliseconds - position)), False)
            position -= milliseconds
        raise AssertionError("Zeitachse ohne Frame")

    def export_manifest(self):
        return {"format": "glide.animation.export", "format_version": 1,
                "width": self.size, "height": self.size, "frames": [
                    {"id": frame.id, "duration_ms": milliseconds}
                    for frame, milliseconds in zip(self.frames, self.durations())]}

    def png_sequence(self, scale=1):
        files = {f"bild-{index:03d}.png": frame.model.to_png(scale)
                 for index, frame in enumerate(self.frames, 1)}
        manifest = self.export_manifest()
        manifest["scale"] = scale
        for index, item in enumerate(manifest["frames"], 1):
            item["file"] = f"bild-{index:03d}.png"
        files["animation.json"] = (canonical_json(manifest) + "\n").encode("utf-8")
        return files

    def png_spritesheet(self, *, columns=None, scale=1):
        if type(scale) is not int or not 1 <= scale <= 16:
            raise DrawingFormatError("Der Exportmaßstab muss 1 bis 16 sein.")
        count = len(self.frames)
        columns = math.ceil(math.sqrt(count)) if columns is None else columns
        if type(columns) is not int or not 1 <= columns <= count:
            raise DrawingFormatError("Ungültige Spaltenzahl für das Spritesheet.")
        rows = math.ceil(count / columns)
        edge = self.size * scale
        width, height = columns * edge, rows * edge
        if max(width, height) > MAX_SHEET_EDGE or width * height > MAX_SHEET_PIXELS:
            raise DrawingFormatError("Das Spritesheet ist zu groß; einen kleineren Maßstab wählen.")
        # Framepaletten dürfen zusammen mehr als 256 Farben enthalten.
        # RGBA bewahrt jede konkrete Farbe und leere Rasterplätze transparent.
        palettes = [[bytes.fromhex(color[1:]) + b"\xff" for color in frame.model.palette]
                    for frame in self.frames]
        data = bytearray()
        for y in range(height):
            data.append(0)
            frame_row, cell_y = divmod(y, edge)
            for column in range(columns):
                frame_index = frame_row * columns + column
                if frame_index >= count:
                    data.extend(bytes(edge * 4))
                    continue
                frame, palette = self.frames[frame_index], palettes[frame_index]
                start = (cell_y // scale) * self.size
                for cell in frame.model.cells[start:start + self.size]:
                    data.extend(palette[cell] * scale)
        def chunk(kind, payload):
            return (struct.pack(">I", len(payload)) + kind + payload
                    + struct.pack(">I", zlib.crc32(kind + payload)))
        png = (b"\x89PNG\r\n\x1a\n"
               + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
               + chunk(b"IDAT", zlib.compress(data, 9)) + chunk(b"IEND", b""))
        manifest = self.export_manifest()
        manifest.update(columns=columns, rows=rows, scale=scale,
                        sheet_width=width, sheet_height=height)
        for index, item in enumerate(manifest["frames"]):
            item.update(x=index % columns * edge, y=index // columns * edge,
                        width=edge, height=edge)
        return png, manifest


def from_entry(entry):
    """Bildfolge lesen; das erste Bild bleibt die statische Vorschau der Seite.

    Ungültige Bildfolgen dürfen niemals auf das erste Bild reduziert werden.
    Die beiden Darstellungen müssen denselben ersten Frame beschreiben.
    """
    if not isinstance(entry, dict):
        raise DrawingFormatError("Eine Zeichnungsseite braucht ein gültiges Objekt.")
    legacy = DrawingModel.from_document(entry.get("drawing"))
    raw = entry.get("animation")
    if raw is None:
        return Animation.from_legacy(legacy.to_document())
    result = Animation.from_document(raw)
    if result.frames[0].model.to_document() != legacy.to_document():
        raise DrawingFormatError("Die statische Vorschau und das erste Bild der Bildfolge unterscheiden sich.")
    return result


def entry_fields(value):
    """Kanonische gespeicherte Felder, unabhängig vom aktiv bearbeiteten Frame."""
    if not isinstance(value, Animation):
        raise DrawingFormatError("Keine gültige Bildfolge.")
    document = value.to_document()
    # Erneut validieren: UI-Änderungen könnten das Modell seit dem letzten
    # Lesen verändert haben. Es gelangt nur ein vollständiger Stand zur Datei.
    checked = Animation.from_document(document)
    return {"drawing": checked.frames[0].model.to_document(),
            "animation": checked.to_document()}


def from_snapshot(text):
    """Alte statische Zwischenstände und vollständige Bildfolgen lesen."""
    document = _json_document(text)
    if isinstance(document, dict) and document.get("format") == FORMAT:
        return Animation.from_document(document)
    return Animation.from_legacy(document)
