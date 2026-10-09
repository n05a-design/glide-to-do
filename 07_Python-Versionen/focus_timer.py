"""Eine Zeiterfassung mit pausierbarer Fokussitzung und Buchungsjournal, ohne Tk."""
from datetime import datetime
import math


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
    return dict(item_id=identity, started_at=started, focus=True,
                elapsed_seconds=min(elapsed, 86400 * 365),
                goal_seconds=min(max(goal, elapsed), 86400 * 365))


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
        result["goal_seconds"] = result["elapsed_seconds"] + 1500
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
