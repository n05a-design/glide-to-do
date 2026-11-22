# SPDX-License-Identifier: MPL-2.0
"""Explizites Entlasten mit gemeinsamer Belegzeitbilanz; ohne Tk/Mutation."""
from dataclasses import dataclass
from datetime import date
import json
import planning
from occupied_time import day_occupancy
import i18n as glide_i18n


def iso_day(value):
    if not isinstance(value, str) or date.fromisoformat(value).isoformat() != value:
        raise ValueError(glide_i18n.t("mod.day_relief.iso_day.please_choose_a_valid", "Bitte einen gültigen Bearbeitungstag wählen."))
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
        text = glide_i18n.t("mod.day_relief.available_text.free_time_unknown", 'Freie Zeit unbekannt · {get}', get=value.get("calendar_message", "Kalender nicht verfügbar"))
        if value.get("without_estimate"):
            text += glide_i18n.t("mod.day_relief.available_text.without_estimate", ' · {without_estimate} ohne Schätzung', without_estimate=value['without_estimate'])
        return text
    text = planning.available_text(value)
    if value.get("occupied_all_day"):
        text += glide_i18n.t("ui.calendar_grid_caption.busy_all_day", " · ganztägig belegt")
    elif value.get("occupied_minutes"):
        text += glide_i18n.t("mod.day_relief.available_text.calendar_time", ' · {duration} Kalenderzeit', duration=planning.duration(value["occupied_minutes"]))
    if value.get("calendar_issues"):
        text += glide_i18n.t("ui.show_comparison.note_the_calendar_hints", " · Kalenderhinweise beachten")
    return text


def capacity_analysis(value):
    """Fachliche Kapazitätsanalyse des Tagesstands (WA-12 / D57)."""
    return planning.capacity_analysis(value)


def relief_summary_text(value):
    """Präzise Vorher/Nachher-Bilanzzeile für die Tagesentlastung (WA-12 / D57)."""
    items_count = value.get("items", 0)
    items_label = f"{items_count} {glide_i18n.t("mod.day_proposal.reason_text.task", 'Aufgabe') if items_count == 1 else glide_i18n.t("mod.day_proposal.reason_text.tasks", 'Aufgaben')}"
    if value.get("calendar_state") in ("loading", "error", "closed"):
        text = glide_i18n.t("mod.day_relief.relief_summary_text.free_time_unknown", '{items_label} · Freie Zeit unbekannt · {get}', items_label=items_label, get=value.get("calendar_message", "Kalender nicht verfügbar"))
        if value.get("without_estimate"):
            text += glide_i18n.t("mod.day_relief.relief_summary_text.without_estimate", ' · {without_estimate} ohne Schätzung', without_estimate=value['without_estimate'])
        return text
    analysis = planning.capacity_analysis(value)
    return f"{items_label} · {analysis['summary_text']}"


def _overload_reasons(value):
    if value.get("calendar_state") in ("loading", "error", "closed"):
        return ()
    analysis = planning.capacity_analysis(value)
    return analysis["overload_reasons"] if analysis["is_overloaded"] else ()


def overload_lines(before, after, day_label, limit=4):
    """Erklärende Zeilen unter der Vorher/Nachher-Bilanz der Tagesentlastung.

    Je Tag, der nachher überplant ist, die Gründe danach; je Tag, den das
    Umplanen entlastet, die Gründe davor und dass er danach frei ist. Mehr als
    `limit` Tage werden nur gezählt, damit der feste Dialogfuß sichtbar bleibt.
    """
    lines = []
    for old, new in zip(before, after):
        now = _overload_reasons(new)
        if now:
            lines.append(glide_i18n.t("mod.day_relief.overload_lines.after", '{day_label}, nachher: {join}', day_label=day_label(new['day']), join="; ".join(now)))
            continue
        was = _overload_reasons(old)
        if was:
            lines.append(glide_i18n.t("mod.day_relief.overload_lines.before_after_no_longer", '{day_label}, vorher: {join} · nachher nicht mehr überplant', day_label=day_label(old['day']), join="; ".join(was)))
    if len(lines) > limit:
        rest = len(lines) - limit
        lines = lines[:limit] + [glide_i18n.t("mod.day_relief.overload_lines.and_one_more_day", "… und ein weiterer Tag") if rest == 1 else glide_i18n.t("mod.day_relief.overload_lines.and_more_days", '… und {rest} weitere Tage', rest=rest)]
    return lines


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
        raise ValueError(glide_i18n.t("mod.day_relief.propose.ambiguous_task_ids", "Mehrdeutige Aufgabenkennungen."))
    index = dict(zip(identities, items))
    selected = tuple(dict.fromkeys(selected))
    if not selected:
        raise ValueError(glide_i18n.t("mod.day_relief.propose.please_choose_at_least", "Bitte mindestens eine Aufgabe wählen."))
    moves = []
    for identity in selected:
        item = index.get(identity)
        if item is None or not schedulable(item) or item.get("done"):
            raise ValueError(glide_i18n.t("mod.day_relief.propose.the_selected_task_is", "Ausgewählte Aufgabe ist nicht mehr offen verfügbar."))
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
        raise ValueError(glide_i18n.t("mod.day_relief.validate.ambiguous_task_ids", "Mehrdeutige Aufgabenkennungen."))
    if fingerprint(items, schedulable) != plan.snapshot:
        raise ValueError(glide_i18n.t("mod.day_relief.validate.the_planning_has_changed", "Die Planung hat sich inzwischen geändert; bitte neu vergleichen."))
    if any(value is not None for value in (capacity, blocks, zone)):
        if any(value is None for value in (capacity, blocks, zone)):
            raise ValueError(glide_i18n.t("mod.day_relief.validate.capacity_busy_times_and", "Kapazität, Belegzeiten und Zeitzone werden gemeinsam benötigt."))
        fresh = propose(items, [move.identity for move in plan.moves],
                        plan.moves[0].target if plan.moves else None,
                        capacity=capacity, blocks=blocks, zone=zone, schedulable=schedulable) if plan.moves else plan
        if fresh.before != plan.before or fresh.after != plan.after:
            raise ValueError(glide_i18n.t("mod.day_relief.validate.the_capacity_has_changed", "Die Kapazität hat sich inzwischen geändert; bitte neu vergleichen."))
    for move in plan.moves:
        item = index.get(move.identity)
        if (item is None or not schedulable(item) or item.get("done")
                or item.get("planned_date") != move.source or item.get("planned_time") != move.clock):
            raise ValueError(glide_i18n.t("mod.day_relief.validate.the_planning_has_changed", "Die Planung hat sich inzwischen geändert; bitte neu vergleichen."))
    return tuple((move.identity, move.target, move.clock if move.target else None) for move in plan.moves)
