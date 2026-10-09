"""Wiederholungsregeln ohne Tk (Fachlogik nach D17, KO02 seit 3.33.20).

Bis 3.33.19 lagen Prüfen und Weiterrechnen als Klassenmethoden in `ListApp`;
sie delegieren seitdem hierher und behalten ihr Verhalten. Neu sind das
Überspringen eines Termins und das Überspringen verpasster Termine: Beide
rücken die Reihe vor, ohne eine Erledigung zu buchen (Things 3.23 erlaubt
frühes Erledigen mit genau einem Folgetermin; Glide ergänzt den ausdrücklichen
Weg, Termine auszulassen).
"""
import calendar
from datetime import date, datetime, timedelta

DAILY = "taeglich"
EVERY_N_DAYS = "tage"
WEEKDAYS = "wochentage"
WEEKLY = "woechentlich"
MONTHLY = "monatlich"
YEARLY = "jaehrlich"
KINDS = (DAILY, EVERY_N_DAYS, WEEKDAYS, WEEKLY, MONTHLY, YEARLY)
# Obergrenze für „alle N Tage“; darüber ist „jährlich“ die richtige Wahl.
MAX_INTERVAL = 365
# Sicherung gegen eine Regel, die nie einen Termin trifft.
MAX_LOOKAHEAD_DAYS = 800
# Verpasste Termine überspringen: höchstens so viele Schritte bis heute.
# Täglich über mehr als zehn Jahre verpasst ist kein Alltag mehr.
MAX_SKIP_STEPS = 4000


def normalize(value, default_start=None):
    """Prüft eine Wiederholungsregel und liefert sie in fester Form.

    Alles Unbekannte fällt auf None zurück – ein Punkt ohne gültige Regel
    wiederholt sich nicht. `default_start` setzt den Ursprungstermin, wenn die
    Regel noch keinen trägt; daran hängen Monats- und Jahresabstände.
    """
    if not isinstance(value, dict):
        return None
    art = value.get("art")
    if art not in KINDS:
        return None
    regel = {"art": art}
    if art == EVERY_N_DAYS:
        abstand = value.get("abstand")
        if isinstance(abstand, bool) or not isinstance(abstand, int):
            return None
        if not 1 <= abstand <= MAX_INTERVAL:
            return None
        regel["abstand"] = abstand
    elif art == WEEKDAYS:
        roh = value.get("tage")
        if not isinstance(roh, list):
            return None
        tage = sorted({tag for tag in roh
                       if isinstance(tag, int) and not isinstance(tag, bool) and 0 <= tag <= 6})
        # Ohne einen einzigen Wochentag träfe die Regel nie zu.
        if not tage:
            return None
        regel["tage"] = tage
    for feld, ersatz in (("start", default_start), ("ende", None)):
        roh = value.get(feld) or (ersatz if feld == "start" else None)
        if isinstance(roh, str) and roh:
            try:
                datetime.strptime(roh, "%Y-%m-%d")
            except ValueError:
                if feld == "ende":
                    return None
                roh = None
            regel[feld] = roh
        else:
            regel[feld] = None
    return regel


def add_months(start, months):
    """Verschiebt ein Datum um Monate und behält den Monatsletzten bei."""
    monat_gesamt = (start.year * 12 + start.month - 1) + months
    jahr, monat = divmod(monat_gesamt, 12)
    monat += 1
    letzter = calendar.monthrange(jahr, monat)[1]
    return date(jahr, monat, min(start.day, letzter))


def next_date(regel, letzter, anker=None):
    """Nächster Termin einer Regel nach `letzter`; None, wenn die Reihe endet."""
    regel = normalize(regel)
    if regel is None or letzter is None:
        return None
    anker = anker or letzter
    art = regel["art"]
    if art == DAILY:
        naechster = letzter + timedelta(days=1)
    elif art == EVERY_N_DAYS:
        naechster = letzter + timedelta(days=regel["abstand"])
    elif art == WEEKLY:
        naechster = letzter + timedelta(days=7)
    elif art == WEEKDAYS:
        naechster = None
        for schritt in range(1, 8):
            kandidat = letzter + timedelta(days=schritt)
            if kandidat.weekday() in regel["tage"]:
                naechster = kandidat
                break
        if naechster is None:
            return None
    elif art == MONTHLY:
        # Vom Anker aus zählen, nicht vom letzten Termin: Sonst schrumpfte
        # der 31. über einen Februar hinweg dauerhaft auf den 28.
        schritte = max(1, (letzter.year - anker.year) * 12 + (letzter.month - anker.month))
        naechster = add_months(anker, schritte)
        wache = 0
        while naechster <= letzter and wache < 120:
            schritte += 1
            naechster = add_months(anker, schritte)
            wache += 1
    elif art == YEARLY:
        schritte = max(1, letzter.year - anker.year)
        naechster = add_months(anker, schritte * 12)
        wache = 0
        while naechster <= letzter and wache < 20:
            schritte += 1
            naechster = add_months(anker, schritte * 12)
            wache += 1
    else:
        return None
    if naechster is None or naechster <= letzter:
        return None
    if (naechster - letzter).days > MAX_LOOKAHEAD_DAYS:
        return None
    ende = regel.get("ende")
    if ende and naechster.isoformat() > ende:
        return None
    return naechster


def anchor_date(regel):
    """Ursprungstermin einer Reihe (`start`), sonst None."""
    anker = regel.get("start") if isinstance(regel, dict) else None
    if isinstance(anker, str) and anker:
        try:
            return datetime.strptime(anker, "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


def _due(item):
    roh = item.get("due") if isinstance(item, dict) else None
    try:
        return datetime.strptime(roh, "%Y-%m-%d").date() if isinstance(roh, str) and roh else None
    except ValueError:
        return None


def first_on_or_after(regel, letzter, anker, stichtag):
    """Erster Termin der Reihe am oder nach `stichtag`, gezählt ab `letzter`.

    None, wenn die Reihe vorher endet oder die Schrittgrenze erreicht ist.
    """
    termin = letzter
    for _ in range(MAX_SKIP_STEPS):
        termin = next_date(regel, termin, anker)
        if termin is None:
            return None
        if termin >= stichtag:
            return termin
    return None


def skip_plan(items, stichtag, missed=False):
    """Neue Fälligkeit je Aufgabe beim Überspringen, ohne Daten zu ändern.

    `missed=False`: genau den aktuellen Termin auslassen (nächster nach der
    Fälligkeit). `missed=True`: alle verpassten Termine auslassen, also auf den
    ersten Termin am oder nach `stichtag`; nur für überfällige Reihen.
    Liefert (Plan, Gründe): Plan ordnet Kennung → ISO-Datum zu; Gründe nennt
    für jede nicht anwendbare Aufgabe, warum.
    """
    plan, gruende = {}, {}
    for item in items:
        kennung = item.get("id")
        regel = normalize(item.get("repeat"))
        faellig = _due(item)
        if regel is None:
            gruende[kennung] = "keine Wiederholung"
            continue
        if item.get("done"):
            gruende[kennung] = "bereits erledigt"
            continue
        if faellig is None:
            gruende[kennung] = "ohne Fälligkeit"
            continue
        anker = anchor_date(regel) or faellig
        if missed:
            if faellig >= stichtag:
                gruende[kennung] = "nicht überfällig"
                continue
            neu = first_on_or_after(regel, faellig, anker, stichtag)
        else:
            neu = next_date(regel, faellig, anker)
        if neu is None:
            gruende[kennung] = "die Reihe hat keinen weiteren Termin"
            continue
        plan[kennung] = neu.isoformat()
    return plan, gruende
