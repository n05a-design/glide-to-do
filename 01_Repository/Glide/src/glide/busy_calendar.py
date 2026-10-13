"""Begrenzte, ausdrücklich geladene ICS-Quelle und unveränderliche Zeitfenster.

Dateizugriff erfolgt nur in read_source. expand_window eignet sich für einen
Arbeiter ohne Tk; die Oberfläche übernimmt ausschließlich passende Quellhashes.
Fehler ergeben niemals eine scheinbar leere, erfolgreiche Kalenderauswertung.
"""
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
import hashlib
from pathlib import Path
import stat
import ics_busy
import ics_recurrence
from occupied_time import BlockIndex, day_bounds

MAX_BYTES = 12 * 1024 * 1024
MAX_EVENTS = 5000
MAX_LINES = 200000
MAX_LINE_BYTES = 65536
MAX_DEPTH = 32
MAX_ZONES = 128
MAX_WINDOW_DAYS = 370


class SourceError(ValueError):
    pass


@dataclass(frozen=True)
class Source:
    path: str
    sha256: str
    size: int
    calendar: object
    zone: object


@dataclass(frozen=True)
class Window:
    sha256: str
    first: date
    last: date
    blocks: tuple
    issues: tuple
    index: BlockIndex = field(init=False, compare=False, repr=False)

    def __post_init__(self):
        object.__setattr__(self, "index", BlockIndex.build(self.blocks))

    def day_blocks(self, day, zone):
        if not self.contains(day):
            raise ValueError("Tag liegt außerhalb des geprüften Kalenderfensters.")
        return self.index.between(*day_bounds(day, zone))

    def contains(self, day):
        return type(day) is date and self.first <= day <= self.last


def validate_content(content):
    if len(content) > MAX_BYTES:
        raise SourceError("Kalenderdatei ist größer als 12 MiB.")
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise SourceError("Kalenderdatei ist nicht gültig UTF-8-kodiert.") from None
    lines = text.splitlines()
    if len(lines) > MAX_LINES:
        raise SourceError("Kalenderdatei enthält zu viele Zeilen.")
    unfolded = []
    folded_bytes = 0
    for line in lines:
        continuation = line.startswith((" ", "\t"))
        size = len((line[1:] if continuation else line).encode("utf-8"))
        folded_bytes = folded_bytes + size if continuation else size
        if folded_bytes > MAX_LINE_BYTES:
            raise SourceError("Eine Kalendereigenschaft ist zu lang.")
        if continuation:
            if not unfolded:
                raise SourceError("ICS-Faltung ohne vorherige Eigenschaft.")
            unfolded[-1] += line[1:]
        elif line:
            unfolded.append(line)
    depth = events = zones = 0
    for line in unfolded:
        upper = line.upper()
        if upper.startswith("BEGIN:"):
            depth += 1
            events += upper == "BEGIN:VEVENT"
            zones += upper == "BEGIN:VTIMEZONE"
            if depth > MAX_DEPTH or events > MAX_EVENTS or zones > MAX_ZONES:
                raise SourceError("Kalender enthält zu viele Termine, Zeitzonen oder verschachtelte Komponenten.")
        elif upper.startswith("END:"):
            depth -= 1
    return text


def read_source(path, zone, resolver=None, date_zone=None):
    """Lokale Datei einmal vollständig lesen; Original weder ändern noch kopieren."""
    try:
        source = Path(path).expanduser().absolute()
        before = source.stat()
        if not stat.S_ISREG(before.st_mode):
            raise SourceError("Bitte eine gewöhnliche lokale Kalenderdatei wählen.")
        if before.st_size > MAX_BYTES:
            raise SourceError("Kalenderdatei ist größer als 12 MiB.")
        with source.open("rb") as stream:
            content = stream.read(MAX_BYTES + 1)
            after = source.stat()
        signature = lambda value: (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns)
        if signature(before) != signature(after):
            raise SourceError("Kalenderdatei wurde beim Lesen geändert; bitte erneut laden.")
        text = validate_content(content)
        calendar = ics_busy.parse_calendar(text, zone, resolver, date_zone)
        return Source(str(source), hashlib.sha256(content).hexdigest(), len(content), calendar, zone)
    except SourceError:
        raise
    except (OSError, ValueError, OverflowError) as exc:
        raise SourceError("Kalenderdatei konnte nicht gelesen werden: " + str(exc)) from exc


def expand_window(source, first, last, margin_days=0, *, max_steps=200000, max_blocks=100000):
    """Beide Datumsgrenzen inklusive; maximal 370 Tage, keine Dateizugriffe."""
    if type(first) is not date or type(last) is not date or last < first:
        raise SourceError("Bitte einen gültigen Kalenderzeitraum wählen.")
    if (last - first).days >= MAX_WINDOW_DAYS or last == date.max:
        raise SourceError("Kalenderzeitraum muss kürzer als 371 Tage sein und vor dem letzten Datum enden.")
    if type(margin_days) is not int or not 0 <= margin_days <= 2:
        raise SourceError("Ungültiger Zeitzonenrand des Kalenderfensters.")
    expanded_first = max(date.min, first - timedelta(days=min(margin_days, (first-date.min).days)))
    expanded_last = last + timedelta(days=min(margin_days, (date.max-last).days-1))
    if (expanded_last-expanded_first).days >= MAX_WINDOW_DAYS:
        raise SourceError("Kalenderfenster einschließlich Zeitzonenrand ist zu groß.")
    lower = datetime.combine(expanded_first, time(), source.zone)
    upper = datetime.combine(expanded_last + timedelta(days=1), time(), source.zone)
    try:
        result = ics_busy.expand(source.calendar, lower, upper,
                                 max_periods=max_steps, max_blocks=max_blocks)
    except (ValueError, OverflowError, ics_recurrence.ExpansionLimitError) as exc:
        raise SourceError("Kalenderzeitraum konnte nicht ausgewertet werden: " + str(exc)) from exc
    return Window(source.sha256, first, last, result.blocks, result.issues)


def normalize_config(value):
    """Additive lokale Einstellungen; beschädigte gewählte Quellen bleiben Fehler."""
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise SourceError("Gespeicherte Kalenderauswahl ist beschädigt.")
    result = dict(value)
    path = result.get("path", "")
    if path is None:
        path = ""
    if not isinstance(path, str) or len(path) > 4096 or any(ord(c) < 32 for c in path):
        raise SourceError("Gespeicherter Kalenderpfad ist ungültig.")
    result["path"] = path
    zone = result.get("zone", "local")
    import timezones
    if zone != "local" and not timezones.valid_key(zone):
        raise SourceError("Gespeicherte Kalenderzeitzone ist ungültig.")
    result["zone"] = zone
    digest = result.get("sha256")
    if digest is not None:
        import re
        if not isinstance(digest, str) or not re.fullmatch("[0-9a-f]{64}", digest):
            raise SourceError("Gespeicherter Kalenderhash ist ungültig.")
    return result
