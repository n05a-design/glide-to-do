# SPDX-License-Identifier: MPL-2.0
"""Bearbeitungstage und Aufwandsbilanz ohne Tk oder Datenmutation (KO01/AU02)."""
from datetime import date, timedelta


CHOICES = (("today", "Heute"), ("tomorrow", "Morgen"),
           ("weekend", "Wochenende"), ("next_week", "Nächste Woche"),
           ("date", "Datum …"), ("unplan", "Ohne Tag"))


def target_day(choice, reference, week_start="monday"):
    """Relative Ziele beziehen sich auf heute; Wochenende ist Sa, am Sa/So heute."""
    if choice == "unplan":
        return None
    if choice == "today":
        return reference.isoformat()
    if choice == "tomorrow":
        return (reference + timedelta(days=1)).isoformat()
    if choice == "weekend":
        return (reference + timedelta(days=max(0, 5 - reference.weekday()))).isoformat()
    if choice == "next_week":
        first = 6 if week_start == "sunday" else 0
        return (reference + timedelta(days=(first - reference.weekday()) % 7 or 7)).isoformat()
    raise ValueError("Unbekanntes Planungsziel")


def capacity_for(settings, day=None, default=0, maximum=1440):
    value = settings.get("daily_capacity_minutes", default)
    if type(value) is not int:
        value = default
    value = max(0, min(maximum, value))
    if day:
        try:
            weekday = date.fromisoformat(str(day)).weekday()
        except ValueError:
            return value
        profile = settings.get("daily_capacity_by_weekday")
        if isinstance(profile, list) and len(profile) == 7 and type(profile[weekday]) is int:
            return max(0, min(maximum, profile[weekday]))
    return value


def summarize(items, capacity, schedulable):
    """Erledigte Schätzungen bleiben geplant; fehlender Aufwand wird nie geraten."""
    capacity = max(0, int(capacity))
    result = dict(items=0, minutes=0, done_minutes=0, estimated=0,
                  without_estimate=0, capacity=capacity, remaining=None)
    for item in items or ():
        if not isinstance(item, dict) or not schedulable(item):
            continue
        result["items"] += 1
        minutes = item.get("estimated_minutes")
        if type(minutes) is not int or minutes <= 0:
            result["without_estimate"] += 1
            continue
        result["estimated"] += 1
        result["minutes"] += minutes
        if item.get("done"):
            result["done_minutes"] += minutes
    if capacity:
        result["remaining"] = capacity - result["minutes"]
    return result


def projected_items(items, selected, day):
    """Zieltag nach der Auswahl: vorhandene Punkte nur einmal, keine Mutation."""
    if day is None:
        return []
    selected_ids = {item["id"] for item in selected}
    result = {item["id"]: item for item in items
              if item.get("planned_date") == day and item.get("id") not in selected_ids}
    result.update((item["id"], item) for item in selected)
    return list(result.values())


def changed_ids(items, day):
    if day is not None and (not isinstance(day, str) or date.fromisoformat(day).isoformat() != day):
        raise ValueError("Der Bearbeitungstag muss ein gültiges ISO-Datum sein.")
    return list(dict.fromkeys(item["id"] for item in items if item.get("planned_date") != day))


def duration(minutes):
    if minutes is None:
        return ""
    hours, rest = divmod(minutes, 60)
    return (f"{hours} h {rest} min" if rest else f"{hours} h") if hours else f"{rest} min"


def capacity_analysis(summary):
    """Fachliche Kapazitäts- und Belastungsanalyse ohne Tk (WA-12 / D57).

    Ermittelt aus den Zusammenfassungsdaten:
    - task_minutes: Geplanter Aufgabenaufwand in Minuten (nur geschätzte Aufgaben)
    - estimated_count: Anzahl Aufgaben mit Schätzung
    - without_estimate_count: Anzahl Aufgaben ohne Schätzung (nie als 0 min gerechnet)
    - done_minutes: Davon bereits erledigte Schätzungen
    - capacity_minutes: Gesetzte Tageskapazität vor Belegzeiten
    - has_capacity: Ob eine Kapazität festgelegt oder ganztägig belegt ist
    - occupied_minutes: Belegte Kalenderzeit (sofern vorhanden)
    - occupied_all_day: Ob der Tag ganztägig belegt ist
    - net_capacity: Tatsächlich für Aufgaben verbleibende Gesamtkapazität
    - remaining_minutes: Verbleibende freie Minuten (oder negativ bei Überlastung, None ohne Kapazität)
    - is_overloaded: True, wenn verbleibende Zeit negativ ist
    - overload_minutes: Betrag der Überplanung
    - overload_reasons: Liste nachvollziehbarer Gründe für Überlastung
    - summary_text: Kompakte Textdarstellung für UI und Berichte
    """
    summary = summary or {}
    task_minutes = summary.get("minutes", 0)
    estimated_count = summary.get("estimated", 0)
    without_estimate_count = summary.get("without_estimate", 0)
    done_minutes = summary.get("done_minutes", 0)

    cap_before = summary.get("capacity_before")
    if cap_before is None:
        cap_before = summary.get("capacity", 0)
    capacity_minutes = max(0, int(cap_before)) if cap_before else 0

    occupied_minutes = max(0, int(summary.get("occupied_minutes", 0)))
    occupied_all_day = bool(summary.get("occupied_all_day", False))

    has_capacity = bool(capacity_minutes > 0 or occupied_all_day)
    net_capacity = 0 if occupied_all_day else max(0, capacity_minutes - occupied_minutes)

    if has_capacity:
        remaining_minutes = net_capacity - task_minutes
        is_overloaded = remaining_minutes < 0
        overload_minutes = -remaining_minutes if is_overloaded else 0
        free_minutes = remaining_minutes if remaining_minutes >= 0 else 0
    else:
        remaining_minutes = None
        is_overloaded = False
        overload_minutes = 0
        free_minutes = None

    reasons = []
    if is_overloaded:
        if occupied_all_day:
            reasons.append("Tag ist ganztägig durch Kalendertermine belegt")
        elif occupied_minutes > 0:
            reasons.append(
                f"Kalenderzeit belegt {duration(occupied_minutes)} der Kapazität ({duration(capacity_minutes)})"
            )
        if task_minutes > net_capacity:
            reasons.append(
                f"Geplanter Aufgabenaufwand ({duration(task_minutes)}) übersteigt nutzbare Kapazität ({duration(net_capacity)}) um {duration(overload_minutes)}"
            )
    if without_estimate_count > 0:
        label, verb = ("Aufgabe", "kann") if without_estimate_count == 1 else ("Aufgaben", "können")
        reasons.append(f"{without_estimate_count} {label} ohne Aufwandsschätzung {verb} den Tag zusätzlich belasten")

    parts = []
    if task_minutes > 0 or estimated_count > 0:
        parts.append(f"Aufwand {duration(task_minutes)}")
    if occupied_all_day:
        parts.append("ganztägig belegt")
    elif occupied_minutes > 0:
        parts.append(f"Kalender {duration(occupied_minutes)}")

    if not has_capacity:
        parts.append("Kapazität nicht festgelegt")
    elif is_overloaded:
        parts.append(f"{duration(overload_minutes)} überplant")
    else:
        parts.append(f"frei {duration(free_minutes)}")

    if without_estimate_count > 0:
        parts.append(f"{without_estimate_count} ohne Schätzung")

    summary_text = " · ".join(parts) if parts else "0 min geplant"

    return {
        "task_minutes": task_minutes,
        "estimated_count": estimated_count,
        "without_estimate_count": without_estimate_count,
        "done_minutes": done_minutes,
        "capacity_minutes": capacity_minutes,
        "has_capacity": has_capacity,
        "occupied_minutes": occupied_minutes,
        "occupied_all_day": occupied_all_day,
        "net_capacity": net_capacity,
        "remaining_minutes": remaining_minutes,
        "free_minutes": free_minutes,
        "is_overloaded": is_overloaded,
        "overload_minutes": overload_minutes,
        "overload_reasons": tuple(reasons),
        "summary_text": summary_text,
    }


def available_text(summary):
    remaining = summary["remaining"]
    if remaining is None:
        text = "Kapazität nicht festgelegt"
    elif remaining >= 0:
        text = f"frei {duration(remaining)}"
    else:
        text = f"{duration(-remaining)} überplant"
    if summary["without_estimate"]:
        text += f" · {summary['without_estimate']} ohne Schätzung"
    return text


def time_assignments(items, day, clock):
    """Aufeinanderfolgende Zeitblöcke; niemals am Tagesende still abschneiden."""
    if day is None or clock is None:
        return [(item["id"], None, None) for item in items]
    date.fromisoformat(day)
    try:
        hour, minute = map(int, clock.split(":"))
        if len(clock) != 5 or not 0 <= hour < 24 or not 0 <= minute < 60:
            raise ValueError
    except (AttributeError, TypeError, ValueError):
        raise ValueError("Bitte eine gültige Uhrzeit wählen.") from None
    start, result = hour * 60 + minute, []
    for item in items:
        estimate = item.get("estimated_minutes")
        duration = estimate if type(estimate) is int and estimate > 0 else 30
        if start + duration > 1440:
            raise ValueError("Die Zeitblöcke reichen über das Tagesende hinaus.")
        result.append((item["id"], day, f"{start // 60:02d}:{start % 60:02d}"))
        start += duration
    return result
