"""Kurzlebige Bestandsprojektion der Startseite, ohne Tk und ohne Mutation.

Die Aufrufer liefern bereits nach Archivstatus gefilterte Listen und dieselben
Fachregeln wie die übrige App. Originalobjekte bleiben für Öffnen/Aktionen
erhalten; die Projektion gehört ausschließlich zu einem synchronen Aufbau.
"""
from dataclasses import dataclass, field
from datetime import date, timedelta


PROJECTIONS = frozenset(("summary", "focus", "week", "labels", "scheduled"))


def planned_preview(entries, limit=5):
    """Die ersten offenen Planeinträge, in Originalreihenfolge und mit Originalen.

    Erledigte verbrauchen keinen Vorschauplatz. Die Zeit-/Archiv-/Planregeln
    bleiben Sache des bestehenden plan_day_entries-Aufrufers.
    """
    result = []
    if limit <= 0:
        return result
    for entry in entries:
        if not entry[-1].get("done"):
            result.append(entry)
            if len(result) >= limit:
                break
    return result


@dataclass
class Dashboard:
    day: date
    projections: frozenset
    total: int = 0
    done: int = 0
    overdue: int = 0
    due_today: int = 0
    due_lists: list = field(default_factory=list)
    due_counts: dict = field(default_factory=dict)
    label_counts: dict = field(default_factory=dict)
    _focus: tuple = None
    _scheduled: tuple = None
    _day_iso: str = field(init=False)
    _needs_due: bool = field(init=False)

    def __post_init__(self):
        self._day_iso = self.day.isoformat()
        self._needs_due = bool(self.projections & {"summary", "week", "scheduled"})

    @property
    def focus(self):
        return self._focus[1:] if self._focus else (None, None)

    @property
    def next_scheduled(self):
        return self._scheduled[1:] if self._scheduled else (None, None)

    def summary(self, lists, recent):
        """Listenanzahl und Verlauf umfassen absichtlich auch Archive."""
        lookup = {entry["id"]: entry for entry in lists}
        return dict(total=self.total, done=self.done, open=self.total - self.done,
                    overdue=self.overdue, due_today=self.due_today, lists=len(lists),
                    due_lists=list(self.due_lists),
                    recent=[(lookup[value["id"]], value["edited_at"])
                            for value in recent if value["id"] in lookup])

    def week_overview(self, days=7):
        return [((self.day + timedelta(days=offset)).isoformat(),
                 self.due_counts.get((self.day + timedelta(days=offset)).isoformat(), 0))
                for offset in range(days)]

    def label_overview(self, get_label, limit=6):
        matches = []
        for identity, count in self.label_counts.items():
            label = get_label(identity)
            if label is not None:
                matches.append((label, count))
        matches.sort(key=lambda value: (-value[1], str(value[0].get("name", "")).lower()))
        return matches[:limit]


def _best(previous, key, item, entry):
    """Bei gleichen Schlüsseln bleibt wie bisher das erste Original erhalten."""
    return (key, item, entry) if previous is None or key < previous[0] else previous


def _count_due(dashboard, due, today):
    if due == today:
        dashboard.due_today += 1
        return 1
    if due and due < today:
        dashboard.overdue += 1
    return 0


def _count_labels(counts, item):
    # Doppelte IDs werden wie im vorhandenen Bestandsvertrag mehrfach gezählt.
    for identity in item.get("labels", []) or ():
        counts[identity] = counts.get(identity, 0) + 1


def _record_open(result, entry, item, *, normalize_due, normalize_time,
                 urgency_rank, max_focus_rank):
    projections = result.projections
    day = result._day_iso
    due = normalize_due(item.get("due")) if result._needs_due else None
    matching = _count_due(result, due, day) if "summary" in projections else 0
    if "week" in projections and due:
        result.due_counts[due] = result.due_counts.get(due, 0) + 1
    if "labels" in projections:
        _count_labels(result.label_counts, item)
    if "focus" in projections:
        rank = urgency_rank(item)
        if rank[0] <= max_focus_rank:
            result._focus = _best(result._focus, rank, item, entry)
    if "scheduled" in projections and due and due >= day:
        key = (due, normalize_time(item.get("due_time")) or "99:99")
        result._scheduled = _best(result._scheduled, key, item, entry)
    return matching


def _collect_summary(result, entries, walk_items, is_schedulable, **policies):
    normalize_due = policies["normalize_due"]
    day = result._day_iso
    for entry in entries:
        matching = 0
        for item in walk_items(entry.get("items", [])):
            if not is_schedulable(item):
                continue
            result.total += 1
            if item.get("done"):
                result.done += 1
                continue
            due = normalize_due(item.get("due"))
            if due == day:
                result.due_today += 1
                matching += 1
            elif due and due < day:
                result.overdue += 1
        if matching:
            result.due_lists.append((entry, matching))


def _collect_focus(result, entries, walk_items, is_schedulable, **policies):
    urgency_rank = policies["urgency_rank"]
    max_rank = policies["max_focus_rank"]
    best = None
    for entry in entries:
        for item in walk_items(entry.get("items", [])):
            if not is_schedulable(item) or item.get("done"):
                continue
            rank = urgency_rank(item)
            if rank[0] <= max_rank and (best is None or rank < best[0]):
                best = (rank, item, entry)
    result._focus = best


def _collect_week(result, entries, walk_items, is_schedulable, **policies):
    normalize_due = policies["normalize_due"]
    counts = result.due_counts
    for entry in entries:
        for item in walk_items(entry.get("items", [])):
            if not is_schedulable(item) or item.get("done"):
                continue
            due = normalize_due(item.get("due"))
            if due:
                counts[due] = counts.get(due, 0) + 1


def _collect_labels(result, entries, walk_items, is_schedulable, **policies):
    counts = result.label_counts
    for entry in entries:
        for item in walk_items(entry.get("items", [])):
            if not is_schedulable(item) or item.get("done"):
                continue
            for identity in item.get("labels", []) or ():
                counts[identity] = counts.get(identity, 0) + 1


def _collect_scheduled(result, entries, walk_items, is_schedulable, **policies):
    normalize_due = policies["normalize_due"]
    normalize_time = policies["normalize_time"]
    day, best = result._day_iso, None
    for entry in entries:
        for item in walk_items(entry.get("items", [])):
            if item.get("done") or not is_schedulable(item):
                continue
            due = normalize_due(item.get("due"))
            if not due or due < day:
                continue
            key = (due, normalize_time(item.get("due_time")) or "99:99")
            if best is None or key < best[0]:
                best = (key, item, entry)
    result._scheduled = best


_SINGLE_COLLECTORS = {"summary": _collect_summary, "focus": _collect_focus,
                      "week": _collect_week, "labels": _collect_labels,
                      "scheduled": _collect_scheduled}


def build(entries, today, *, walk_items, is_schedulable, normalize_due,
          normalize_time, urgency_rank, max_focus_rank, projections=PROJECTIONS):
    """Berechnet nur angeforderte Projektionen in einem Bestandsdurchlauf.

    Einzelne Fassadenabfragen müssen insbesondere keine Dringlichkeit oder
    Abhängigkeiten auswerten, wenn sie nur Zähler oder Kalenderdaten benötigen.
    """
    projections = frozenset(projections)
    if not projections <= PROJECTIONS:
        raise ValueError("Unbekannte Startseitenprojektion")
    result = Dashboard(today, projections)
    if len(projections) == 1:
        _SINGLE_COLLECTORS[next(iter(projections))](
            result, entries, walk_items, is_schedulable, normalize_due=normalize_due,
            normalize_time=normalize_time, urgency_rank=urgency_rank, max_focus_rank=max_focus_rank)
        return result
    for entry in entries:
        matching = 0
        for item in walk_items(entry.get("items", [])):
            if not is_schedulable(item):
                continue
            if "summary" in projections:
                result.total += 1
                result.done += bool(item.get("done"))
            if item.get("done"):
                continue
            matching += _record_open(result, entry, item, normalize_due=normalize_due,
                                     normalize_time=normalize_time, urgency_rank=urgency_rank,
                                     max_focus_rank=max_focus_rank)
        if matching:
            result.due_lists.append((entry, matching))
    return result
