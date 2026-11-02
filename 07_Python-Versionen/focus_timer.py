"""Eine Zeiterfassung mit pausierbarer Fokussitzung und Buchungsjournal, ohne Tk."""
from datetime import datetime
import math


# Wählbare Fokusdauern in Minuten (D57, 31.10.2026); Vorgabe wie bisher 25.
FOCUS_MINUTES = (15, 25, 50)
DEFAULT_FOCUS_MINUTES = 25


def normalize_minutes(value):
    """Gespeicherte oder gewählte Fokusdauer; Unbekanntes ergibt die Vorgabe."""
    return value if type(value) is int and value in FOCUS_MINUTES else DEFAULT_FOCUS_MINUTES


# Sitzung nach geschätztem Aufwand: ganze Minuten in diesem Bereich, ohne Vorgabe zu werden.
SESSION_MINUTES = (5, 180)


def session_minutes(value):
    """Erlaubte Sitzungsdauer in Minuten (Vorgabe oder Aufwand), sonst None."""
    return value if type(value) is int and SESSION_MINUTES[0] <= value <= SESSION_MINUTES[1] else None


def estimate_option(estimate):
    """Zusätzliche Fokusdauer aus dem Aufwand, wenn sie keine der Vorgaben ist; sonst None."""
    minutes = session_minutes(estimate)
    return minutes if minutes is not None and minutes not in FOCUS_MINUTES else None


def interval_minutes(timer):
    """Dauer einer laufenden Sitzung in Minuten (ältere Sitzungen: Vorgabe)."""
    seconds = (timer or {}).get("interval_seconds") if isinstance(timer, dict) else None
    minutes = seconds // 60 if type(seconds) is int and seconds % 60 == 0 else None
    return session_minutes(minutes) or DEFAULT_FOCUS_MINUTES


# „Wechseln zu …“ im Fokusfeld (D57, 01.11.2026): so viele nächste Aufgaben zur Wahl.
SWITCH_LIMIT = 5
SWITCH_TITLE_LIMIT = 48


def next_candidates(rows, limit=None):
    """Nächste Fokusaufgaben aus (Rang, ID, Wert): aufsteigend nach Rang, dann ID.

    Der erste Wert ist derselbe, den „Nächste Aufgabe“ wählt; `limit` kürzt die Wahl.
    """
    order = sorted(rows, key=lambda row: (row[0], row[1]))
    return [row[2] for row in (order if limit is None else order[:max(0, limit)])]


def more_label(count):
    """Gesperrter Schlusseintrag von „Wechseln zu …“ für Aufgaben jenseits der Grenze; leer ohne Rest."""
    if not isinstance(count, int) or count <= 0:
        return ""
    return f"… und {count} weitere für heute"


def switch_label(title, limit=SWITCH_TITLE_LIMIT):
    """Einzeiliger Menütitel; lange Titel enden an der Grenze mit „…“."""
    clean = " ".join(str(title or "").split()) or "Ohne Titel"
    return clean if len(clean) <= limit else clean[:limit - 1].rstrip() + "…"


def next_label(title, remaining=0):
    """Zeile „Als Nächstes“ im Fokusfeld; `None` heißt: keine weitere Aufgabe für heute.

    `remaining` zählt die Tagesaufgaben nach der genannten (3.50.0).
    """
    if title is None:
        return "Danach keine weitere Aufgabe für heute"
    rest = remaining if isinstance(remaining, int) and remaining > 0 else 0
    suffix = "" if not rest else f" · danach noch {rest} Aufgabe{'' if rest == 1 else 'n'}"
    return "Als Nächstes: " + switch_label(title) + suffix


class PendingBookingError(RuntimeError):
    """Eine vorbereitete Buchung muss vor einer weiteren Mutation geklärt sein."""


def parsed(value):
    try:
        result = datetime.fromisoformat(value)
        return result if result.utcoffset() is not None else result.astimezone()
    except (TypeError, ValueError):
        return None


def normalize(timer):
    if not isinstance(timer, dict):
        return None
    identity = timer.get("item_id")
    if not isinstance(identity, str) or not 0 < len(identity) <= 64:
        return None
    started = timer.get("started_at")
    if not timer.get("focus"):
        return dict(item_id=identity, started_at=started) if parsed(started) else None
    elapsed, goal = timer.get("elapsed_seconds", 0), timer.get("goal_seconds", 1500)
    if (type(elapsed) not in (int, float) or not math.isfinite(elapsed) or elapsed < 0 or
            type(goal) not in (int, float) or not math.isfinite(goal) or goal < 1 or
            (started is not None and parsed(started) is None)):
        return None
    result = dict(item_id=identity, started_at=started, focus=True,
                  elapsed_seconds=min(elapsed, 86400 * 365),
                  goal_seconds=min(max(goal, elapsed), 86400 * 365))
    # Gewählte Sitzungsdauer: nur bekannte Werte; ältere Leser verwerfen das Feld und nutzen 25 min.
    interval = timer.get("interval_seconds")
    if type(interval) is int and interval % 60 == 0 and session_minutes(interval // 60):
        result["interval_seconds"] = interval
    return result


def elapsed(timer, now):
    timer = normalize(timer)
    if not timer:
        return 0.0
    total = timer.get("elapsed_seconds", 0)
    started = parsed(timer["started_at"])
    if started:
        total += max(0.0, (now.astimezone() - started).total_seconds())
    return min(total, timer["goal_seconds"]) if timer.get("focus") else total


def minutes(timer, now):
    seconds = elapsed(timer, now)
    return math.ceil(seconds / 60) if seconds >= 1 else 0


def pause(timer, now):
    result = normalize(timer)
    if not result or not result.get("focus"):
        raise ValueError("Keine Fokussitzung.")
    result.update(elapsed_seconds=elapsed(result, now), started_at=None)
    return result


def resume(timer, now):
    result = normalize(timer)
    if not result or not result.get("focus"):
        raise ValueError("Keine Fokussitzung.")
    if result["started_at"] is not None:
        return result
    if result["elapsed_seconds"] >= result["goal_seconds"]:
        result["goal_seconds"] = result["elapsed_seconds"] + result.get("interval_seconds", DEFAULT_FOCUS_MINUTES * 60)
    result["started_at"] = now.astimezone().isoformat(timespec="microseconds")
    return result


def extend(timer, now, seconds=300):
    """Fokusintervall ab der verstrichenen Zeit verlängern (3.50.0).

    Stand die Sitzung am Intervallende still, läuft sie weiter; eine bewusste
    Pause mitten im Intervall wird nur verlängert, nicht aufgehoben.
    """
    result = normalize(timer)
    if not result or not result.get("focus"):
        raise ValueError("Keine Fokussitzung.")
    bisher = elapsed(result, now)
    am_ende = result["started_at"] is None and bisher >= result["goal_seconds"]
    result["goal_seconds"] = min(max(result["goal_seconds"], bisher) + seconds, 86400 * 365)
    if am_ende:
        result["elapsed_seconds"] = bisher
        result["started_at"] = now.astimezone().isoformat(timespec="microseconds")
    return result


def normalize_booking(value):
    if not isinstance(value, dict):
        return None
    identity, before, after = value.get("item_id"), value.get("before"), value.get("after")
    if (not isinstance(identity, str) or not 0 < len(identity) <= 64 or
            type(before) is not int or type(after) is not int or not 0 <= before <= after):
        return None
    return dict(item_id=identity, before=before, after=after, minutes=after-before)


def booking_action(booking, current):
    """Ein vorbereitetes Journal wird nach Absturz höchstens einmal angewendet."""
    if current == booking["after"]:
        return "committed"
    if current == booking["before"]:
        return "apply"
    return "conflict"
