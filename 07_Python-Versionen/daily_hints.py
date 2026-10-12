"""Optionale Tageshinweise mit dauerhaften Zustellkennungen, ohne Tk.

Der Aufrufer sammelt fällige Hinweise nur bei laufender Anwendung, speichert
mark_presented vor der Anzeige und öffnet einen Tagesmodus erst nach Auswahl.
Ein Neustart erzeugt keine zweite Zustellung bereits vorgemerkter Hinweise.
"""
from copy import deepcopy
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
import re

KINDS = ("start", "close")
DEFAULT_CLOCKS = {"start": "08:30", "close": "17:30"}


def normalize(config):
    source = config if isinstance(config, dict) else {}
    result = {"enabled": source.get("enabled") is True, **DEFAULT_CLOCKS}
    for kind in KINDS:
        value = source.get(kind)
        if isinstance(value, str) and re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", value):
            result[kind] = value
    weekdays = source.get("weekdays", list(range(7)))
    result["weekdays"] = sorted({day for day in weekdays if type(day) is int and 0 <= day < 7}) if isinstance(weekdays, list) else list(range(7))
    return result


def _moment(value):
    try:
        parsed = datetime.fromisoformat(value)
        return parsed if parsed.tzinfo is not None else None
    except (TypeError, ValueError):
        return None


def _now(now):
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("Tageshinweise brauchen eine Uhrzeit mit Zeitzone.")
    return now


def key(day, kind):
    if kind not in KINDS:
        raise ValueError("Unbekannter Tageshinweis")
    if isinstance(day, str):
        day = date.fromisoformat(day)
    if type(day) is not date:
        raise ValueError("Ungültiger Hinweistag")
    return f"{day.isoformat()}/{kind}"


def _state(state):
    if state is not None and not isinstance(state, dict):
        raise ValueError("Gespeicherter Tageshinweiszustand ist beschädigt.")
    result = deepcopy(state) if isinstance(state, dict) else {}
    if "receipts" in result and not isinstance(result["receipts"], dict):
        raise ValueError("Gespeicherte Tageshinweisbelege sind beschädigt.")
    result.setdefault("receipts", {})
    if result.get("last_check") and _moment(result["last_check"]) is None:
        raise ValueError("Gespeicherter Prüfzeitpunkt der Tageshinweise ist ungültig.")
    for identity, receipt in result["receipts"].items():
        try:
            stamp, kind = identity.split("/")
            valid = key(stamp,kind) == identity
        except (AttributeError,ValueError,TypeError):
            continue
        if valid and (not isinstance(receipt,dict) or receipt.get("status") not in
                      ("presented","completed","skipped","snoozed")):
            raise ValueError("Unbekannter gespeicherter Zustand eines Tageshinweises: " + identity)
        if valid and receipt.get("status") == "snoozed" and _moment(receipt.get("wake_at")) is None:
            raise ValueError("Gespeicherte Später-Uhrzeit eines Tageshinweises ist ungültig: " + identity)
    return result


@dataclass(frozen=True)
class Hint:
    identity: str
    kind: str
    day: str
    due: datetime
    missed: bool
    snoozed: bool = False


def collect_due(config, state, now):
    """Reine Vorschau; erst mark_presented vermerkt die Zustellung.

    Ohne früheren Prüfzeitpunkt beginnt die Sammlung am heutigen Tag. Nach
    Abwesenheit werden alle seit der letzten Prüfung fälligen Hinweise als
    eine vom Aufrufer zusammen darzustellende Auswahl zurückgegeben.
    """
    now = _now(now)
    config = normalize(config)
    if not config["enabled"]:
        return ()
    state = _state(state)
    previous = _moment(state.get("last_check"))
    first = previous.astimezone(now.tzinfo).date() if previous else now.date()
    if (now.date()-first).days > 3660:
        raise ValueError("Der gespeicherte Prüfzeitpunkt liegt mehr als zehn Jahre zurück. Bitte die Tageshinweise ab heute neu beginnen.")
    receipts, offers = state["receipts"], {}
    day = first
    while day <= now.date():
        if day.weekday() in config["weekdays"]:
            for kind in KINDS:
                identity = key(day, kind)
                due = datetime.combine(day, time.fromisoformat(config[kind]), tzinfo=now.tzinfo)
                due = due.astimezone(timezone.utc).astimezone(now.tzinfo)
                if due.astimezone(timezone.utc) <= now.astimezone(timezone.utc) and identity not in receipts:
                    offers[identity] = Hint(identity, kind, day.isoformat(), due, day < now.date())
        if day == now.date():
            break
        day += timedelta(days=1)
    for identity, receipt in receipts.items():
        if not isinstance(receipt, dict) or receipt.get("status") != "snoozed":
            continue
        wake = _moment(receipt.get("wake_at"))
        if wake is None or wake.astimezone(timezone.utc) > now.astimezone(timezone.utc):
            continue
        try:
            if not isinstance(identity, str):
                continue
            stamp, kind = identity.split("/")
            day = date.fromisoformat(stamp)
            if key(day, kind) != identity:
                continue
        except (ValueError, TypeError):
            continue
        offers[identity] = Hint(identity, kind, stamp, wake, day < now.date(), True)
    return tuple(sorted(offers.values(), key=lambda hint: (hint.due.astimezone(timezone.utc), hint.identity)))


def checkpoint(state, now):
    """Prüfzeitpunkt ohne Zustellung; bei Konfigurationswechsel ab heute sammeln.

    Der Aufrufer speichert auch eine deaktivierte Konfiguration mit diesem
    Zeitstempel. Aus der abgeschalteten Zeit entsteht so kein Tagesstapel.
    Bereits vorgemerkte Zustellungen behalten ihre feste Kennung.
    """
    now = _now(now)
    result = _state(state)
    previous = _moment(result.get("last_check"))
    result["last_check"] = (max((previous,now),key=lambda x:x.astimezone(timezone.utc))
                            if previous else now).isoformat()
    return result


def mark_presented(state, hints, now):
    """Vor der Anzeige atomar speichern; feste Kennung statt Sitzungstoken."""
    now = _now(now)
    result = _state(state)
    for hint in hints:
        if key(hint.day, hint.kind) != hint.identity:
            raise ValueError("Ungültige Zustellkennung")
        result["receipts"][hint.identity] = {"status": "presented", "at": now.isoformat()}
    return checkpoint(result,now)


def snooze(state, hint, now, minutes=15):
    now = _now(now)
    if type(minutes) is not int or not 1 <= minutes <= 1440:
        raise ValueError("Später erinnern braucht 1 bis 1440 Minuten.")
    result = mark_presented(state, (hint,), now)
    result["receipts"][hint.identity] = {"status": "snoozed", "wake_at": (now.astimezone(timezone.utc) + timedelta(minutes=minutes)).astimezone(now.tzinfo).isoformat()}
    return result


def skip_day(state, day, now):
    now = _now(now)
    result = _state(state)
    for kind in KINDS:
        result["receipts"][key(day, kind)] = {"status": "skipped", "at": now.isoformat()}
    return result


def complete(state, hint, now):
    result = mark_presented(state, (hint,), now)
    result["receipts"][hint.identity]["status"] = "completed"
    return result


def pending(config, state, now):
    """Bereits zugestellte offene Hinweise manuell lesen, ohne erneut zuzustellen.

    Später-Hinweise bleiben auch vor ihrer nächsten Fälligkeit im Hinweiskorb;
    deren wake_at ist eine reale Uhrzeit. Erledigte/übersprungene Belege bleiben
    für die Deduplizierung gespeichert, erscheinen aber nicht in der Auswahl.
    """
    now = _now(now)
    config = normalize(config)
    state = _state(state)
    result = []
    for identity, receipt in state["receipts"].items():
        try:
            stamp, kind = identity.split("/")
            day = date.fromisoformat(stamp)
            if key(day, kind) != identity:
                continue
        except (AttributeError, TypeError, ValueError):
            continue
        if receipt["status"] not in ("presented", "snoozed"):
            continue
        delayed = receipt["status"] == "snoozed"
        due = (_moment(receipt["wake_at"]).astimezone(now.tzinfo) if delayed else
               datetime.combine(day, time.fromisoformat(config[kind]), tzinfo=now.tzinfo))
        due = due.astimezone(timezone.utc).astimezone(now.tzinfo)
        result.append(Hint(identity, kind, stamp, due, day < now.date(), delayed))
    return tuple(sorted(result, key=lambda hint: (hint.due.astimezone(timezone.utc), hint.identity)))


def prepare_delivery(config, state, now):
    """Fällige Hinweise und ihren vor Anzeige zu speichernden Zustand liefern.

    Ohne neue Zustellung genügt ein Prüfbeleg je lokalem Tag. So schreibt die
    laufende App nicht alle 30 Sekunden unveränderte Hinweishistorien auf Platte.
    """
    now = _now(now)
    original = _state(state)
    if not normalize(config)["enabled"]:
        return (), original
    due = collect_due(config, original, now)
    if due:
        return due, mark_presented(original, due, now)
    previous = _moment(original.get("last_check"))
    if previous and previous.astimezone(now.tzinfo).date() == now.date():
        return (), original
    return (), checkpoint(original, now)
