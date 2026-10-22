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
import ics_recurrence

DAILY = "taeglich"
EVERY_N_DAYS = "tage"
WEEKDAYS = "wochentage"
WEEKLY = "woechentlich"
MONTHLY = "monatlich"
YEARLY = "jaehrlich"
SERIES = "serie"
KINDS = (DAILY, EVERY_N_DAYS, WEEKDAYS, WEEKLY, MONTHLY, YEARLY, SERIES)
SERIES_CHOICES = (
    ("alle N Wochen an Wochentagen", "serie_woche"),
    ("alle N Monate", "serie_monat"),
    ("alle N Jahre", "serie_jahr"),
    ("n-ter Wochentag im Monat", "serie_position"),
    ("letzter Tag im Monat", "serie_letzter"),
    ("letzter Werktag im Monat (Mo–Fr)", "serie_werktag"),
)
DAY_CODES = tuple(ics_recurrence.WEEKDAYS)


def series_rule(text):
    """Nur die editierbare FP-02/1-Teilmenge; unbekannte Teile nie annähern.

    COUNT, UNTIL, Pausen und Bezug auf Erledigung gehören zu Stufe 2.
    Das Serienende bleibt wie bisher das eigene inklusive Datumsfeld.
    """
    if not isinstance(text, str) or len(text) > 180:
        raise ValueError("Keine unterstützte Serienregel.")
    fields = {part.partition("=")[0] for part in text.upper().split(";")}
    if fields - {"FREQ", "INTERVAL", "BYDAY", "BYMONTHDAY", "BYSETPOS"}:
        raise ValueError("Nicht unterstützte Serienteile.")
    rule = ics_recurrence.parse_rule(text)
    if rule.interval > MAX_INTERVAL:
        raise ValueError("Serienabstand muss zwischen 1 und 365 liegen.")
    if rule.frequency == "WEEKLY":
        valid = bool(rule.weekdays) and all(n is None for n, _d in rule.weekdays)
    elif rule.frequency == "MONTHLY":
        valid = (not (rule.weekdays or rule.monthdays or rule.positions)
                 or (rule.monthdays == (-1,) and not (rule.weekdays or rule.positions))
                 or (len(rule.weekdays) == 1 and rule.weekdays[0][0] in (1, 2, 3, 4, 5, -1)
                     and not (rule.monthdays or rule.positions))
                 or (set(rule.weekdays) == {(None, d) for d in range(5)}
                     and rule.positions == (-1,) and not rule.monthdays))
    else:
        valid = rule.frequency == "YEARLY" and not (rule.weekdays or rule.monthdays or rule.positions)
    if not valid:
        raise ValueError("Keine unterstützte Serienform.")
    parts = ["FREQ=" + rule.frequency, "INTERVAL=" + str(rule.interval)]
    if rule.weekdays:
        parts.append("BYDAY=" + ",".join((str(n) if n is not None else "") + DAY_CODES[d]
                                        for n, d in sorted(rule.weekdays, key=lambda v: v[1])))
    if rule.monthdays:
        parts.append("BYMONTHDAY=" + ",".join(map(str, rule.monthdays)))
    if rule.positions:
        parts.append("BYSETPOS=" + ",".join(map(str, rule.positions)))
    return ";".join(parts)


def from_series_fields(kind, interval, days=(), position=1, weekday=0):
    """Maskenwerte als kanonische RRULE; Zahlenbereiche auch außerhalb der UI prüfen."""
    if kind not in dict((key, label) for label, key in SERIES_CHOICES):
        raise ValueError("Unbekannte Serienform.")
    if isinstance(interval, bool) or not str(interval).isascii() or not str(interval).isdigit():
        raise ValueError("Bitte einen Abstand von 1 bis 365 eingeben.")
    interval = int(interval)
    if not 1 <= interval <= MAX_INTERVAL:
        raise ValueError("Bitte einen Abstand von 1 bis 365 eingeben.")
    frequency = {"serie_woche": "WEEKLY", "serie_jahr": "YEARLY"}.get(kind, "MONTHLY")
    text = f"FREQ={frequency};INTERVAL={interval}"
    if kind == "serie_woche":
        if not days or any(type(d) is not int or not 0 <= d <= 6 for d in days):
            raise ValueError("Bitte mindestens einen Wochentag auswählen.")
        text += ";BYDAY=" + ",".join(DAY_CODES[d] for d in sorted(set(days)))
    elif kind == "serie_position":
        if type(position) is not int or position not in (1, 2, 3, 4, 5, -1) or type(weekday) is not int or not 0 <= weekday <= 6:
            raise ValueError("Bitte eine Monatsposition und einen Wochentag auswählen.")
        text += f";BYDAY={position}{DAY_CODES[weekday]}"
    elif kind == "serie_letzter":
        text += ";BYMONTHDAY=-1"
    elif kind == "serie_werktag":
        text += ";BYDAY=MO,TU,WE,TH,FR;BYSETPOS=-1"
    return {"art": SERIES, "rrule": series_rule(text)}


def form_values(value):
    """Gespeicherte Regeln verlustfrei in die feste Maskenauswahl zurückübersetzen."""
    value = normalize(value) or {}
    result = dict(art=value.get("art"), abstand=value.get("abstand", 2),
                  tage=value.get("tage", []), position=1, wochentag=0)
    if value.get("art") != SERIES:
        return result
    rule = ics_recurrence.parse_rule(value["rrule"])
    result.update(abstand=rule.interval, tage=[d for _n, d in rule.weekdays])
    if rule.frequency == "WEEKLY":
        result["art"] = "serie_woche"
    elif rule.frequency == "YEARLY":
        result["art"] = "serie_jahr"
    elif rule.positions:
        result["art"] = "serie_werktag"
    elif rule.monthdays:
        result["art"] = "serie_letzter"
    elif rule.weekdays:
        result.update(art="serie_position", position=rule.weekdays[0][0], wochentag=rule.weekdays[0][1])
    else:
        result["art"] = "serie_monat"
    return result


def describe_series(value):
    """Feste deutsche Klartexte, auch verlustfrei für den TXT-Rundlauf."""
    fields = form_values(value)
    names = ("Mo", "Di", "Mi", "Do", "Fr", "Sa", "So")
    n, kind = fields["abstand"], fields["art"]
    if kind == "serie_woche":
        return ("jede Woche: " if n == 1 else f"alle {n} Wochen: ") + ", ".join(names[d] for d in fields["tage"])
    if kind in ("serie_monat", "serie_jahr"):
        base = ("jeden Monat" if kind == "serie_monat" else "jedes Jahr") if n == 1 else f"alle {n} " + ("Monate" if kind == "serie_monat" else "Jahre")
        return base + " (fehlende Tage entfallen)"
    if kind == "serie_position":
        position = "letzter" if fields["position"] == -1 else f"{fields['position']}."
        suffix = position + " " + names[fields["wochentag"]]
    elif kind == "serie_letzter":
        suffix = "letzter Tag"
    elif kind == "serie_werktag":
        suffix = "letzter Werktag (Mo–Fr)"
    else:
        return ""
    return ("jeden Monat: " if n == 1 else f"alle {n} Monate: ") + suffix


def parse_series_text(text):
    """Erkennt ausschließlich die eigenen eindeutigen Serien-Klartexte."""
    import re
    names = ("Mo", "Di", "Mi", "Do", "Fr", "Sa", "So")
    for original, replacement in (("jede Woche", "alle 1 Wochen"), ("jeden Monat", "alle 1 Monate"), ("jedes Jahr", "alle 1 Jahre")):
        if text.startswith(original):
            text = replacement + text[len(original):]
            break
    match = re.fullmatch(r"alle ([0-9]{1,3}) (Wochen|Monate|Jahre)(.*)", text)
    if not match:
        return None
    interval, unit, suffix = match.groups()
    try:
        if unit == "Wochen" and suffix.startswith(": "):
            return from_series_fields("serie_woche", interval, [names.index(v) for v in suffix[2:].split(", ")])
        if unit in ("Monate", "Jahre") and suffix == " (fehlende Tage entfallen)":
            return from_series_fields("serie_monat" if unit == "Monate" else "serie_jahr", interval)
        if unit == "Monate":
            if suffix == ": letzter Tag":
                return from_series_fields("serie_letzter", interval)
            if suffix == ": letzter Werktag (Mo–Fr)":
                return from_series_fields("serie_werktag", interval)
            position = re.fullmatch(r": (letzter|[1-5]\.) (Mo|Di|Mi|Do|Fr|Sa|So)", suffix)
            if position:
                return from_series_fields("serie_position", interval,
                    position=-1 if position[1] == "letzter" else int(position[1][0]), weekday=names.index(position[2]))
    except ValueError:
        pass
    return None
# Obergrenze für „alle N Tage“; darüber ist „jährlich“ die richtige Wahl.
MAX_INTERVAL = 365
# Sicherung gegen eine Regel, die nie einen Termin trifft.
MAX_LOOKAHEAD_DAYS = 800
# Verpasste Termine überspringen: höchstens so viele Schritte bis heute.
# Täglich über mehr als zehn Jahre verpasst ist kein Alltag mehr.
MAX_SKIP_STEPS = 4000


def check_stored_series(data, version):
    """Format-26-Regeln auch in Papierkorb/Kindpunkten vor Normalisierung prüfen."""
    pending = [data]
    while pending:
        value = pending.pop()
        if isinstance(value, list):
            pending.extend(value)
        elif isinstance(value, dict):
            repeat = value.get("repeat")
            if isinstance(repeat, dict) and (repeat.get("art") == SERIES
                    or any(key in repeat for key in ("bezug", "pausiert", "rest"))):
                if type(version) is not int or version < 26:
                    raise ValueError("Erweiterte Wiederholungsregeln brauchen Datenformat 26.")
                if normalize(repeat) is None:
                    raise ValueError("Ungültige erweiterte Wiederholungsregel; Datei bleibt erhalten.")
            pending.extend(v for v in value.values() if isinstance(v, (dict, list)))


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
    if art == SERIES:
        if set(value) - {"art", "rrule", "start", "ende", "bezug", "pausiert", "rest"}:
            return None
        try:
            regel["rrule"] = series_rule(value.get("rrule"))
        except ValueError:
            return None
    elif art == EVERY_N_DAYS:
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
    if value.get("bezug", "faellig") not in ("faellig", "erledigt"):
        return None
    if value.get("bezug") == "erledigt":
        regel["bezug"] = "erledigt"
    if "pausiert" in value and type(value["pausiert"]) is not bool:
        return None
    if value.get("pausiert"):
        regel["pausiert"] = True
    if "rest" in value:
        if type(value["rest"]) is not int or not 1 <= value["rest"] <= 10000:
            return None
        regel["rest"] = value["rest"]
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
    if art == SERIES:
        anker = anchor_date(regel) or anker
        if letzter == date.max:
            return None
        upper = date.fromisoformat(regel["ende"]) if regel.get("ende") else date.max
        return next(ics_recurrence.dates(anker, regel["rrule"], upper,
                                        after=letzter + timedelta(days=1)), None)
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


def apply_options(rule, basis="faellig", paused=False, remaining=""):
    """Gemeinsame Zusatzwerte, ohne eine alte Regel ungefragt umzuschreiben."""
    if basis not in ("faellig", "erledigt") or type(paused) is not bool:
        raise ValueError("Ungültiger Serienbezug oder Pausenzustand.")
    value = dict(rule)
    for key in ("bezug", "pausiert", "rest"):
        value.pop(key, None)
    if basis == "erledigt":
        value["bezug"] = basis
    if paused:
        value["pausiert"] = True
    text = str(remaining).strip()
    if text:
        if not text.isascii() or not text.isdigit() or not 1 <= int(text) <= 10000:
            raise ValueError("Bitte 1 bis 10.000 verbleibende Termine eingeben oder das Feld leer lassen.")
        value["rest"] = int(text)
    result = normalize(value)
    if result is None:
        raise ValueError("Ungültige Wiederholung.")
    return result


def option_suffix(rule):
    result = []
    if rule.get("bezug") == "erledigt":
        result.append("ab Erledigung")
    if rule.get("pausiert"):
        result.append("pausiert")
    if rule.get("rest"):
        result.append(f"noch {rule['rest']} Termine inkl. aktuell")
    return "".join(" · " + text for text in result)


def split_options_text(text):
    import re
    parts = text.split(" · ")
    options = dict(basis="faellig", paused=False, remaining="")
    for part in parts[1:]:
        if part == "ab Erledigung":
            options["basis"] = "erledigt"
        elif part == "pausiert":
            options["paused"] = True
        elif match := re.fullmatch(r"noch ([0-9]{1,5}) Termine inkl\. aktuell", part):
            options["remaining"] = match[1]
        else:
            raise ValueError("Unbekannter Serienzusatz.")
    return parts[0], options


def advance_rule(rule, due, completed_on=None):
    """Ein Vorkommen verbrauchen: (nächster Tag, neue Regel), ohne Mutation.

    rest zählt das aktuelle Vorkommen mit. Überspringen übergibt keine
    Erledigung und bleibt im Terminraster; eine pausierte Serie rückt nie vor.
    """
    value = normalize(rule)
    if value is None or value.get("pausiert") or value.get("rest") == 1:
        return None, value
    base = due
    value["start"] = value.get("start") or due.isoformat()
    if value.get("bezug") == "erledigt" and completed_on is not None:
        base = completed_on
        value["start"] = base.isoformat()
    try:
        following = next_date(value, base, anchor_date(value) or base)
    except (OverflowError, ValueError):
        following = None
    if following is not None and "rest" in value:
        value["rest"] -= 1
    return following, value


def preview(regel, due, count=5, completed_on=None):
    """Bis zu fünf echte Folgetermine, ohne den Bestand oder den Anker zu verändern.

    Datum statt lokaler Uhrzeit: Der Rhythmus verschiebt sich beim Wechsel
    zwischen Sommer- und Winterzeit nicht. Nicht vorhandene RFC-Monatstage
    werden ausgelassen; die sechs alten Arten behalten ihre Klemmregel.
    """
    if type(count) is not int or not 1 <= count <= 5:
        raise ValueError("Die Vorschau enthält ein bis fünf Folgetermine.")
    regel = normalize(regel)
    current = _due({"due": due})
    if not regel or current is None:
        return []
    result = []
    for index in range(count):
        try:
            current, regel = advance_rule(regel, current, completed_on if index == 0 else None)
        except (OverflowError, ValueError):
            break
        if current is None:
            break
        result.append(current.isoformat())
    return result


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


def skip_plan(items, stichtag, missed=False, with_rules=False):
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
        if regel.get("pausiert"):
            gruende[kennung] = "Serie pausiert"
            continue
        if faellig is None:
            gruende[kennung] = "ohne Fälligkeit"
            continue
        if missed:
            if faellig >= stichtag:
                gruende[kennung] = "nicht überfällig"
                continue
            neu = faellig
            for _ in range(MAX_SKIP_STEPS):
                neu, regel = advance_rule(regel, neu)
                if neu is None or neu >= stichtag:
                    break
            else:
                neu = None
        else:
            neu, regel = advance_rule(regel, faellig)
        if neu is None:
            gruende[kennung] = "die Reihe hat keinen weiteren Termin"
            continue
        plan[kennung] = {"due": neu.isoformat(), "repeat": regel} if with_rules else neu.isoformat()
    return plan, gruende
