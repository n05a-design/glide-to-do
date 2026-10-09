"""Tk-freie Datums- und Bestandsauswertung für bestehende Ansichten (P09b).

Nur das Lesen identischer Datumszeichenketten wird dauerhaft gemerkt.
Kennzahlen entstehen frisch; die Oberfläche hält sie höchstens einen Aufbau.
"""
from dataclasses import dataclass
from datetime import date, datetime
from functools import lru_cache


@lru_cache(maxsize=4096)
def parsed_date(value):
    """Bisherige strptime-Semantik, einschließlich nicht aufgefüllter Monate."""
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def due_status(item, today=None):
    value = item.get("due")
    if not value:
        return ""
    parsed = parsed_date(value)
    if parsed is None:
        return ""
    if item.get("done"):
        return "future"
    delta = (parsed - (today or date.today())).days
    return "overdue" if delta < 0 else "today" if delta == 0 else "soon" if delta <= 2 else "future"


@lru_cache(maxsize=4096)
def display_date(value):
    parsed = parsed_date(value)
    return parsed.strftime("%d.%m.%Y") if parsed is not None else ""


@dataclass(frozen=True)
class ItemMetrics:
    total: int = 0
    done: int = 0
    overdue: int = 0
    next_due: str | None = None
    labels: frozenset = frozenset()

    @property
    def stats(self):
        return self.total, self.done, self.overdue


def summarize(items, *, walk, schedulable, normalize_due, regular_labels=(), today=None,
              include_details=True):
    """Ein Durchlauf: Fortschritt, nächste offene Fälligkeit und eigene Labels."""
    today = today or date.today()
    iso_today = today.isoformat()
    regular_labels = frozenset(regular_labels)
    total = done = overdue = 0
    next_due = None
    labels = set()
    for item in walk(items):
        if not schedulable(item):
            continue
        total += 1
        if include_details:
            labels.update(value for value in item.get("labels", []) or [] if value in regular_labels)
        if item.get("done"):
            done += 1
            continue
        if due_status(item, today) == "overdue":
            overdue += 1
        due = normalize_due(item.get("due")) if include_details else None
        if due and due >= iso_today and (next_due is None or due < next_due):
            next_due = due
    return ItemMetrics(total, done, overdue, next_due, frozenset(labels))


def line_height(lines, linespace, pady, inset):
    """Zeilenraum plus aktueller Labelrand; Rand selbst wird nicht gecacht."""
    return lines * linespace + 2 * (int(float(pady or 0)) + inset)
