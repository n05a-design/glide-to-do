"""Glide-Wiederholungen ↔ iCalendar-RRULE ohne Tk (FP-00, A28).

Glide klemmt Monats- und Jahresreihen am Monatsende: Eine Reihe ab dem 31.01.
trifft den 28.02. und danach wieder den 31.03. (`repeat_rules.add_months`).
Ein Kalenderprogramm liest `FREQ=MONTHLY` nach RFC 5545 dagegen so, dass es
Monate ohne diesen Tag auslässt. Deshalb nennt die Ausgabe für Anker vom 29.
an alle in Frage kommenden Tage und wählt mit BYSETPOS den letzten vorhandenen:
genau das Klemmen. Der Rückweg erkennt nur Formen, die Glide genauso
wiederholen kann, und lehnt alles andere ab, statt die Folge still zu ändern.
Quelle: https://www.rfc-editor.org/rfc/rfc5545#section-3.3.10
"""
from datetime import date

DAILY, EVERY_N_DAYS, WEEKDAYS = "taeglich", "tage", "wochentage"
WEEKLY, MONTHLY, YEARLY = "woechentlich", "monatlich", "jaehrlich"
ICS_WEEKDAYS = ("MO", "TU", "WE", "TH", "FR", "SA", "SU")


def _monatsende_tage(tag):
    """BYMONTHDAY-Liste, deren letzter vorhandener Wert das Klemmen auf `tag` nachbildet."""
    return ",".join(str(wert) for wert in range(28, tag + 1))


def rule_parts(regel, anker):
    """RRULE-Teile ohne UNTIL für eine normalisierte Glide-Regel; None, wenn nicht abbildbar.

    `anker` ist der Ursprungstermin der Reihe (date): der Start der Regel oder,
    wenn sie keinen trägt, die Fälligkeit.
    """
    if not isinstance(regel, dict):
        return None
    art = regel.get("art")
    if art == DAILY:
        return ["FREQ=DAILY"]
    if art == EVERY_N_DAYS:
        abstand = regel.get("abstand")
        if isinstance(abstand, bool) or not isinstance(abstand, int) or abstand < 1:
            return None
        return ["FREQ=DAILY", f"INTERVAL={abstand}"]
    if art == WEEKDAYS:
        tage = [ICS_WEEKDAYS[tag] for tag in regel.get("tage") or ()
                if isinstance(tag, int) and not isinstance(tag, bool) and 0 <= tag <= 6]
        return ["FREQ=WEEKLY", "BYDAY=" + ",".join(tage)] if tage else None
    if art == WEEKLY:
        return ["FREQ=WEEKLY"]
    if art == MONTHLY:
        if isinstance(anker, date) and anker.day >= 29:
            return ["FREQ=MONTHLY", "BYMONTHDAY=" + _monatsende_tage(anker.day), "BYSETPOS=-1"]
        return ["FREQ=MONTHLY"]
    if art == YEARLY:
        if isinstance(anker, date) and (anker.month, anker.day) == (2, 29):
            return ["FREQ=YEARLY", "BYMONTH=2", "BYMONTHDAY=28,29", "BYSETPOS=-1"]
        return ["FREQ=YEARLY"]
    return None


def parse_parts(wert):
    """RRULE-Text in ein Wörterbuch großgeschriebener Teile; leere Teile entfallen."""
    teile = {}
    for stueck in str(wert or "").split(";"):
        if "=" in stueck:
            schluessel, roh = stueck.split("=", 1)
            teile[schluessel.strip().upper()] = roh.strip().upper()
    return teile


def from_parts(teile, start):
    """Glide-Regel (ohne Start und Ende) aus RRULE-Teilen oder None.

    `start` ist der erste Termin (date) der Kalenderreihe. Erkannt werden nur
    Formen, die Glide mit derselben Terminfolge wiederholt; UNTIL wertet der
    Aufrufer aus. Monatsreihen ab dem 29. ohne die Klemmform und Jahresreihen
    am 29.02. lassen in RFC 5545 Monate bzw. Jahre aus und werden abgelehnt.
    """
    freq = teile.get("FREQ")
    erlaubt = {"FREQ", "INTERVAL", "UNTIL", "BYDAY", "WKST"}
    if freq == "MONTHLY":
        erlaubt |= {"BYMONTHDAY", "BYSETPOS"}
    if freq == "YEARLY":
        erlaubt |= {"BYMONTH", "BYMONTHDAY", "BYSETPOS"}
    if not freq or set(teile) - erlaubt:
        return None
    intervall = teile.get("INTERVAL", "1")
    if not intervall.isdigit() or int(intervall) < 1:
        return None
    intervall = int(intervall)
    roh_tage = [kuerzel for kuerzel in teile.get("BYDAY", "").split(",") if kuerzel]
    if any(kuerzel not in ICS_WEEKDAYS for kuerzel in roh_tage):
        return None  # etwa „2MO“ – eine Position im Monat kennt Glide nicht
    tage = sorted({ICS_WEEKDAYS.index(kuerzel) for kuerzel in roh_tage})
    klemmform = {key: teile.get(key) for key in ("BYMONTH", "BYMONTHDAY", "BYSETPOS") if key in teile}
    if freq == "DAILY" and not tage:
        return {"art": DAILY} if intervall == 1 else {"art": EVERY_N_DAYS, "abstand": intervall}
    if freq == "WEEKLY" and intervall == 1:
        return {"art": WEEKDAYS, "tage": tage} if tage else {"art": WEEKLY}
    if tage or intervall != 1:
        return None
    # Ohne bekannten Starttag (ältere Aufrufer) gilt die bisherige Abbildung.
    tag = (start.month, start.day) if isinstance(start, date) else None
    if freq == "MONTHLY":
        if not klemmform:
            return {"art": MONTHLY} if tag is None or tag[1] < 29 else None
        if tag and tag[1] >= 29 and klemmform == {"BYMONTHDAY": _monatsende_tage(tag[1]), "BYSETPOS": "-1"}:
            return {"art": MONTHLY}
        if tag and tag[1] == 31 and klemmform == {"BYMONTHDAY": "-1"}:
            return {"art": MONTHLY}
        return None
    if freq == "YEARLY":
        if not klemmform:
            return {"art": YEARLY} if tag != (2, 29) else None
        if tag == (2, 29) and klemmform == {"BYMONTH": "2", "BYMONTHDAY": "28,29", "BYSETPOS": "-1"}:
            return {"art": YEARLY}
        return None
    return None
