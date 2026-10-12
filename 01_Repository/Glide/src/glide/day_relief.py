"""Explizites Entlasten mit gemeinsamer Belegzeitbilanz; ohne Tk/Mutation."""
from dataclasses import dataclass
from datetime import date
import json
import planning
from occupied_time import day_occupancy


def iso_day(value):
    if not isinstance(value, str) or date.fromisoformat(value).isoformat() != value:
        raise ValueError("Bitte einen gültigen Bearbeitungstag wählen.")
    return value


def summary(items, day, capacity, blocks, zone, schedulable):
    """Bilanz einer bereits ausgewählten/projizierten Menge, ohne erneuten Datumsfilter."""
    day = iso_day(day)
    busy = day_occupancy(blocks, date.fromisoformat(day), zone, capacity)
    result = planning.summarize(items, busy["capacity"], schedulable)
    # Eine vollständig belegte Kapazität ist nicht dasselbe wie keine Vorgabe.
    if capacity > 0 or busy["all_day"]:
        result["remaining"] = busy["capacity"] - result["minutes"]
    result.update(day=day, capacity_before=capacity, occupied_minutes=busy["minutes"],
                  occupied_all_day=busy["all_day"], day_minutes=busy["day_minutes"])
    return result


def day_summary(items, day, capacity, blocks, zone, schedulable):
    return summary([item for item in items if item.get("planned_date") == day],
                   day, capacity, blocks, zone, schedulable)


def available_text(value):
    if value.get("calendar_state") in ("loading", "error", "closed"):
        text = "Freie Zeit unbekannt · " + value.get("calendar_message", "Kalender nicht verfügbar")
        if value.get("without_estimate"):
            text += f" · {value['without_estimate']} ohne Schätzung"
        return text
    text = planning.available_text(value)
    if value.get("occupied_all_day"):
        text += " · ganztägig belegt"
    elif value.get("occupied_minutes"):
        text += " · " + planning.duration(value["occupied_minutes"]) + " Kalenderzeit"
    if value.get("calendar_issues"):
        text += " · Kalenderhinweise beachten"
    return text


@dataclass(frozen=True)
class Move:
    identity: str
    source: str
    clock: str | None
    target: str | None


@dataclass(frozen=True)
class Plan:
    moves: tuple
    before: tuple
    after: tuple
    snapshot: str


def fingerprint(items, schedulable):
    return json.dumps(sorted((item["id"], item.get("planned_date"), item.get("planned_time"),
                             item.get("estimated_minutes"), bool(item.get("done")), bool(schedulable(item)))
                            for item in items), sort_keys=True, ensure_ascii=False)


def propose(items, selected, target, *, capacity, blocks, zone, schedulable):
    """Nutzer bestimmt IDs und Ziel; kein Verteilen oder Ändern von Fälligkeiten.

    capacity(day) liefert die Vorgabe vor Belegzeiten; blocks(day) alle lokalen
    Kalenderintervalle. Ein späterer Mutationsaufrufer prüft nochmals validate.
    """
    if target is not None:
        iso_day(target)
    items = tuple(items)
    identities = [item["id"] for item in items]
    if len(set(identities)) != len(identities):
        raise ValueError("Mehrdeutige Aufgabenkennungen.")
    index = dict(zip(identities, items))
    selected = tuple(dict.fromkeys(selected))
    if not selected:
        raise ValueError("Bitte mindestens eine Aufgabe wählen.")
    moves = []
    for identity in selected:
        item = index.get(identity)
        if item is None or not schedulable(item) or item.get("done"):
            raise ValueError("Ausgewählte Aufgabe ist nicht mehr offen verfügbar.")
        source = iso_day(item.get("planned_date"))
        if source != target:
            moves.append(Move(identity, source, item.get("planned_time"), target))
    days = sorted({move.source for move in moves} | ({target} if target else set()))
    moved = {move.identity:move for move in moves}
    projected = [dict(item, planned_date=moved[item["id"]].target,
                      planned_time=item.get("planned_time") if target else None)
                 if item["id"] in moved else item for item in items]
    before, after = [], []
    for day in days:
        cap, occupied = capacity(day), tuple(blocks(day))
        before.append(day_summary(items, day, cap, occupied, zone, schedulable))
        after.append(day_summary(projected, day, cap, occupied, zone, schedulable))
    return Plan(tuple(moves), tuple(before), tuple(after), fingerprint(items, schedulable))


def validate(plan, items, schedulable, *, capacity=None, blocks=None, zone=None):
    """Kein Teilanwenden bei inzwischen geänderter Auswahl/Planung."""
    items = tuple(items)
    index = {item["id"]:item for item in items}
    if len(index) != len(items):
        raise ValueError("Mehrdeutige Aufgabenkennungen.")
    if fingerprint(items, schedulable) != plan.snapshot:
        raise ValueError("Die Planung hat sich inzwischen geändert; bitte neu vergleichen.")
    if any(value is not None for value in (capacity, blocks, zone)):
        if any(value is None for value in (capacity, blocks, zone)):
            raise ValueError("Kapazität, Belegzeiten und Zeitzone werden gemeinsam benötigt.")
        fresh = propose(items, [move.identity for move in plan.moves],
                        plan.moves[0].target if plan.moves else None,
                        capacity=capacity, blocks=blocks, zone=zone, schedulable=schedulable) if plan.moves else plan
        if fresh.before != plan.before or fresh.after != plan.after:
            raise ValueError("Die Kapazität hat sich inzwischen geändert; bitte neu vergleichen.")
    for move in plan.moves:
        item = index.get(move.identity)
        if (item is None or not schedulable(item) or item.get("done")
                or item.get("planned_date") != move.source or item.get("planned_time") != move.clock):
            raise ValueError("Die Planung hat sich inzwischen geändert; bitte neu vergleichen.")
    return tuple((move.identity, move.target, move.clock if move.target else None) for move in plan.moves)
