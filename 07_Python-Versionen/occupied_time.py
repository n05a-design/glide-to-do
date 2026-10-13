"""Überlappungsfreie Belegzeit und Tageskapazität, ohne Tk oder Datenmutation."""
from dataclasses import dataclass
from datetime import datetime, time, timedelta, timezone
from math import ceil

UTC = timezone.utc


def utc(moment):
    if not isinstance(moment, datetime) or moment.tzinfo is None or moment.utcoffset() is None:
        raise ValueError("Belegzeiten brauchen eine eindeutige Zeitzone.")
    return moment.astimezone(UTC)


@dataclass(frozen=True)
class Block:
    start: datetime
    end: datetime
    title: str = ""
    all_day: bool = False

    def __post_init__(self):
        if utc(self.end) <= utc(self.start):
            raise ValueError("Das Ende muss nach dem Beginn liegen.")


def merged_intervals(blocks, start, end):
    """UTC-Intervalle schneiden und vereinigen; angrenzende Blöcke zusammenfassen."""
    lower, upper = utc(start), utc(end)
    if upper <= lower:
        raise ValueError("Der Betrachtungszeitraum muss positiv sein.")
    clipped = sorted((max(lower, utc(block.start)), min(upper, utc(block.end)))
                     for block in blocks if utc(block.start) < upper and utc(block.end) > lower)
    result = []
    for left, right in clipped:
        if result and left <= result[-1][1]:
            result[-1] = result[-1][0], max(right, result[-1][1])
        else:
            result.append((left, right))
    return tuple(result)

@dataclass(frozen=True)
class BlockIndex:
    blocks: tuple
    starts: tuple
    prefix_ends: tuple

    @classmethod
    def build(cls, blocks):
        ordered = tuple(sorted(blocks, key=lambda block: utc(block.start)))
        starts, ends, latest = [], [], None
        for block in ordered:
            starts.append(utc(block.start))
            latest = max(latest, utc(block.end)) if latest is not None else utc(block.end)
            ends.append(latest)
        return cls(ordered, tuple(starts), tuple(ends))

    def between(self, start, end):
        from bisect import bisect_left, bisect_right
        lower, upper = utc(start), utc(end)
        if upper <= lower:
            raise ValueError("Der Betrachtungszeitraum muss positiv sein.")
        first = bisect_right(self.prefix_ends, lower)
        last = bisect_left(self.starts, upper)
        return tuple(block for block in self.blocks[first:last] if utc(block.end) > lower)


def local_interval(day, clock, minutes, zone):
    """Aufgabenuhrzeit: erste doppelte Stunde; fehlende Uhrzeit sichtbar abweisen."""
    import re
    if not isinstance(clock, str) or not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", clock):
        raise ValueError("Ungültige Aufgabenzeit.")
    if type(minutes) is not int or not 1 <= minutes <= 1440:
        raise ValueError("Ungültige Aufgabendauer.")
    hour, minute = map(int, clock.split(":"))
    local = datetime.combine(day, time(hour, minute), zone)
    start = utc(local)
    if start.astimezone(zone).replace(tzinfo=None) != local.replace(tzinfo=None):
        raise ValueError("Diese Aufgabenzeit existiert am Tag der Zeitumstellung nicht.")
    return start, start + timedelta(minutes=minutes)


def offset_boundaries(start, end, zone):
    """Offsetwechsel auf Sekundengrenzen innerhalb des betrachteten Intervalls."""
    left, upper = utc(start), utc(end)
    points = [left]
    while left < upper:
        right = min(upper, left + timedelta(hours=1))
        offset = left.astimezone(zone).utcoffset()
        if right.astimezone(zone).utcoffset() != offset:
            low, high = left, right
            while (high-low).total_seconds() > 1:
                middle = low + timedelta(seconds=int((high-low).total_seconds()) // 2)
                if middle.astimezone(zone).utcoffset() == offset:
                    low = middle
                else:
                    high = middle
            if high < upper:
                points.append(high)
            left = high
        else:
            left = right
    return tuple(points + [upper])


@dataclass(frozen=True)
class GridSegment:
    block: Block
    start: datetime
    end: datetime
    minutes: tuple
    zone_label: str


def grid_segments(blocks, day, zone):
    """Lokale Rasterteile; doppelte Stunden bleiben getrennte, benannte Segmente."""
    day_start, day_end = day_bounds(day, zone)
    lower, upper = utc(day_start), utc(day_end)
    midnight = datetime.combine(day, time.min)
    result = []
    for block in blocks:
        if block.all_day:
            continue
        left, right = max(lower, utc(block.start)), min(upper, utc(block.end))
        if right <= left:
            continue
        points = offset_boundaries(left, right, zone)
        for start, end in zip(points, points[1:]):
            offset = start.astimezone(zone).utcoffset()
            first = ((start.replace(tzinfo=None) + offset) - midnight).total_seconds() / 60
            last = ((end.replace(tzinfo=None) + offset) - midnight).total_seconds() / 60
            result.append(GridSegment(block, start, end, (max(0, first), min(1440, last)),
                                      start.astimezone(zone).strftime("%Z %z")))
    return tuple(sorted(result, key=lambda part: (part.minutes[0], part.minutes[1], utc(part.start))))

def planning_slots(items, day, duration, blocks, zone, start=8*60, end=18*60):
    """Freie lokale Bereiche aus bekannten Kalender- und geschätzten Glide-Blöcken."""
    if type(duration) is not int or not 1 <= duration <= 1440:
        return []
    if not (type(start) is int and type(end) is int and 0 <= start < end < 1440):
        raise ValueError("Ungültiger Zeitraum für freie Zeitfenster.")
    lower, _ = local_interval(day, f"{start//60:02d}:{start%60:02d}", 1, zone)
    upper, _ = local_interval(day, f"{end//60:02d}:{end%60:02d}", 1, zone)
    busy = list(blocks)
    for item in items:
        if item.get("planned_date") != day.isoformat() or not item.get("planned_time"):
            continue
        effort = item.get("estimated_minutes")
        if type(effort) is not int or not 1 <= effort <= 1440:
            continue
        begin, finish = local_interval(day, item["planned_time"], effort, zone)
        busy.append(Block(begin, finish))
    return [(begin.astimezone(zone).strftime("%H:%M"), finish.astimezone(zone).strftime("%H:%M"))
            for begin, finish in free_intervals(busy, lower, upper)
            if finish-begin >= timedelta(minutes=duration)]




def day_bounds(day, zone):
    """Kalendertage haben an Zeitumstellungen 23 oder 25 tatsächliche Stunden."""
    start = datetime.combine(day, time.min, zone)
    end = datetime.combine(day + timedelta(days=1), time.min, zone)
    utc(start); utc(end)
    return start, end


def day_occupancy(blocks, day, zone, capacity):
    if type(capacity) is not int or not 0 <= capacity <= 1440:
        raise ValueError("Die Tageskapazität muss zwischen 0 und 1440 Minuten liegen.")
    blocks = tuple(blocks)
    start, end = day_bounds(day, zone)
    intervals = merged_intervals(blocks, start, end)
    seconds = sum((right - left).total_seconds() for left, right in intervals)
    all_day = any(block.all_day and utc(block.start) < utc(end) and utc(block.end) > utc(start)
                  for block in blocks)
    minutes = ceil(seconds / 60)
    return {"minutes": minutes, "all_day": all_day, "capacity_before": capacity,
            "capacity": 0 if all_day else max(0, capacity - minutes),
            "day_minutes": int((utc(end) - utc(start)).total_seconds() / 60),
            "intervals": intervals}


def overlaps(blocks, start, end):
    """Grenzkontakt ist frei; Anfang und Ende sind halb offene Intervalle."""
    return bool(merged_intervals(blocks, start, end))


def free_intervals(blocks, start, end):
    cursor, upper = utc(start), utc(end)
    result = []
    for left, right in merged_intervals(blocks, start, end):
        if left > cursor:
            result.append((cursor, left))
        cursor = right
    if cursor < upper:
        result.append((cursor, upper))
    return tuple(result)
