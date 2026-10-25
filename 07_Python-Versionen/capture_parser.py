"""Deutsche Schnelleingabe ohne Tk (G01).

Erkennt in einer Eingabezeile Bearbeitungstag, Fälligkeit, Uhrzeit, Aufwand,
Wichtigkeit, Wiederholung und vorhandene Labels. Die Bedeutung folgt D01/D10:
Ein Datum ohne Zusatz setzt den Bearbeitungstag, „fällig“ oder „bis“ davor die
Fälligkeit – auch in „/“-Befehlen. Eine Wiederholung setzt die Fälligkeit auf
ihren ersten Termin, damit sie im Kalender steht (Entscheidung 02.10.2026). Jede Erkennung kommt mit ihrer Textstelle zurück, damit
die Oberfläche sie vor dem Speichern zeigen und einzeln zurücknehmen kann.
Text in Anführungszeichen bleibt wörtlich und behält seine Zeichen.

Seit 3.33.20 (KO03) erkennt die Eingabe auch eine Erinnerung: „erinnere 9 Uhr“,
„Erinnerung morgen 14:30“, „erinnern 30 min vorher“, „/erinnern bei Fälligkeit“.
Was nach dem Auslösewort steht, gehört zur Erinnerung und setzt weder
Bearbeitungstag noch Fälligkeit. Ein Vorlauf braucht eine Fälligkeit; fehlt sie,
bleibt der Text stehen und der Chip sagt warum. Erinnerungen werden nur bei
laufender Glide zugestellt (Produktgrenze); der Chip nennt das.
"""
import re
import repeat_rules as repeat_logic
from datetime import date, datetime, timedelta
from typing import NamedTuple

WEEKDAYS = ("montag", "dienstag", "mittwoch", "donnerstag", "freitag", "samstag", "sonntag")
WEEKDAY_SHORT = ("Mo", "Di", "Mi", "Do", "Fr", "Sa", "So")
OFFSETS = {"heute": 0, "morgen": 1, "übermorgen": 2, "uebermorgen": 2}
IMPORTANCE = {"wichtig": 3, "hoch": 3, "mittel": 2, "niedrig": 1}
IMPORTANCE_NAMES = {3: "hoch", 2: "mittel", 1: "niedrig"}
MAX_ESTIMATE_MINUTES = 24 * 60
# Wiederholungsregeln wie in der Eingabemaske (app.pyw, REPEAT_*).
REPEAT_DAILY, REPEAT_EVERY_N_DAYS, REPEAT_WEEKDAYS = "taeglich", "tage", "wochentage"
REPEAT_WEEKLY, REPEAT_MONTHLY, REPEAT_YEARLY = "woechentlich", "monatlich", "jaehrlich"
REPEAT_MAX_INTERVAL = 365
NUMBER_WORDS = {"zwei": 2, "drei": 3, "vier": 4, "fünf": 5, "fuenf": 5, "sechs": 6, "sieben": 7,
                "acht": 8, "neun": 9, "zehn": 10}
WEEKDAY_PLURAL = tuple(f"{name}s" for name in WEEKDAYS)

# „/“-Befehle beim Anlegen eines Punkts (27.09.2026): „Einkauf /morgen /wichtig“.
# Seit D10 (3.33.3) setzt ein Datum auch hier den Bearbeitungstag; die
# Fälligkeit setzen „/bis“ und „/fällig“ vor einem Datum.
SLASH_COMMANDS = (
    ("heute", "Bearbeitungstag heute"), ("morgen", "Bearbeitungstag morgen"),
    ("übermorgen", "Bearbeitungstag übermorgen"),
    ("montag", "Bearbeitungstag Montag"), ("dienstag", "Bearbeitungstag Dienstag"),
    ("mittwoch", "Bearbeitungstag Mittwoch"), ("donnerstag", "Bearbeitungstag Donnerstag"),
    ("freitag", "Bearbeitungstag Freitag"), ("samstag", "Bearbeitungstag Samstag"),
    ("sonntag", "Bearbeitungstag Sonntag"),
    ("bis", "Fälligkeit, z. B. /bis Freitag"), ("fällig", "Fälligkeit, z. B. /fällig morgen"),
    ("wichtig", "Wichtigkeit hoch"), ("hoch", "Wichtigkeit hoch"), ("mittel", "Wichtigkeit mittel"),
    ("niedrig", "Wichtigkeit niedrig"),
    ("meintag", "für heute einplanen (Ansicht „Heute“)"),
    ("erinnern", "Erinnerung, z. B. /erinnern 9:00 oder /erinnern 30 min vorher"),
)
SLASH_IMPORTANCE = {"wichtig": 3, "hoch": 3, "mittel": 2, "niedrig": 1}
# Auslösewörter einer Erinnerung (KO03). „Erinnerung an …“ ohne Zeitangabe
# bleibt gewöhnlicher Text.
REMINDER_WORDS = ("erinnern", "erinnere", "erinnerung", "erinner")
REMINDER_NOTE = "nur bei laufender Glide"
REMINDER_MAX_MINUTES = 525600


def parse_capture_due(value, today=None):
    """Bewusst begrenzte deutsche Datumseingabe für ein Feld mit fester Bedeutung."""
    today = today or date.today()
    text = " ".join(str(value or "").strip().lower().split())
    if not text:
        return None, None
    due_time = None
    clock = re.search(r"(?:\s+(?:um\s+)?)(\d{1,2}):(\d{2})(?:\s+uhr)?$", text)
    if clock:
        hour, minute = int(clock[1]), int(clock[2])
        if hour > 23 or minute > 59:
            raise ValueError("Bitte eine Uhrzeit zwischen 00:00 und 23:59 eingeben.")
        due_time = f"{hour:02d}:{minute:02d}"
        text = text[:clock.start()].strip()
    try:
        if text in OFFSETS:
            day = today + timedelta(days=OFFSETS[text])
        elif text in WEEKDAYS:
            day = today + timedelta(days=(WEEKDAYS.index(text) - today.weekday()) % 7)
        elif (relative := re.fullmatch(r"in (\d{1,4}) (tag(?:en)?|woche(?:n)?)", text)):
            days = int(relative[1]) * (7 if relative[2].startswith("woche") else 1)
            if days > 3650:
                raise ValueError
            day = today + timedelta(days=days)
        elif re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{4}", text):
            day = datetime.strptime(text, "%d.%m.%Y").date()
        elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
            day = date.fromisoformat(text)
        else:
            raise ValueError
    except (ValueError, OverflowError):
        raise ValueError("Datum nicht erkannt: z. B. morgen, Montag, in 3 Tagen oder 24.09.2026; optional um 14:30.") from None
    return day.isoformat(), due_time


def slash_suggestions(teil, labels=()):
    """Befehle, die zum angefangenen Wort „/mo…“ passen – für die Vorschlagszeile."""
    teil = str(teil or "").lower()
    treffer = [befehl for befehl, _text in SLASH_COMMANDS if befehl.startswith(teil)]
    treffer += [str(label.get("name")) for label in labels or ()
                if isinstance(label, dict) and str(label.get("name") or "").lower().startswith(teil)]
    return treffer[:8]


class Teil(NamedTuple):
    """Eine erkannte Stelle: Textbereich, Schlüssel zum Zurücknehmen, Felder und Chiptext."""
    start: int
    ende: int
    schluessel: str
    felder: dict
    text: str


class Erfassung(NamedTuple):
    titel: str
    felder: dict
    teile: tuple


class _Wort(NamedTuple):
    start: int
    ende: int        # ohne Satzzeichen und Punkt
    ende_datum: int  # ohne Satzzeichen, Punkt bleibt (24.12.)
    wort: str
    datum: str
    roh: str


def format_day(iso):
    tag = date.fromisoformat(iso)
    return f"{WEEKDAY_SHORT[tag.weekday()]} {tag:%d.%m.%Y}"


def format_minutes(minutes):
    stunden, rest = divmod(int(minutes), 60)
    if stunden and rest:
        return f"{stunden} Std. {rest} Min."
    return f"{stunden} Std." if stunden else f"{rest} Min."


def _woerter(text, geschuetzt):
    result = []
    for treffer in re.finditer(r"\S+", text):
        if any(a <= treffer.start() < b for a, b in geschuetzt):
            continue
        roh = treffer.group()
        klein = roh.lower()
        datum = re.sub(r"[,;:!?)]+$", "", klein)
        wort = datum.rstrip(".")
        result.append(_Wort(treffer.start(), treffer.start() + len(wort),
                            treffer.start() + len(datum), wort, datum, roh))
    return result


def _geschuetzt(text):
    """Bereiche in „…“ oder "…" werden nicht gedeutet."""
    return [(m.start(), m.end()) for m in re.finditer(r'"[^"]*"|„[^“”]*[“”]', text)]


def _tag(wort, today):
    """Datum aus einem Wort oder None."""
    if wort.datum in OFFSETS or wort.wort in OFFSETS:
        return today + timedelta(days=OFFSETS.get(wort.wort, OFFSETS.get(wort.datum, 0)))
    if wort.wort in WEEKDAYS:
        return today + timedelta(days=(WEEKDAYS.index(wort.wort) - today.weekday()) % 7)
    if (teile := re.fullmatch(r"(\d{1,2})\.(\d{1,2})\.(\d{4}|\d{2})?", wort.datum)):
        tag, monat, jahr = int(teile[1]), int(teile[2]), teile[3]
        try:
            if jahr:
                return date(int(jahr) + (2000 if len(jahr) == 2 else 0), monat, tag)
            kandidat = date(today.year, monat, tag)
            return kandidat if kandidat >= today else date(today.year + 1, monat, tag)
        except ValueError:
            return None
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", wort.datum):
        try:
            return date.fromisoformat(wort.datum)
        except ValueError:
            return None
    return None


def _zeit(woerter, i):
    """Uhrzeit ab Wort i: (Anzahl Wörter, „HH:MM“) oder None."""
    n = 0
    if i < len(woerter) and woerter[i].wort == "um":
        n = 1
    if i + n >= len(woerter):
        return None
    wort = woerter[i + n].wort
    folgt_uhr = i + n + 1 < len(woerter) and woerter[i + n + 1].wort == "uhr"
    if (teile := re.fullmatch(r"(\d{1,2}):(\d{2})(?:uhr)?", wort)):
        stunde, minute = int(teile[1]), int(teile[2])
        n += 1 + (1 if folgt_uhr else 0)
    elif re.fullmatch(r"\d{1,2}", wort) and folgt_uhr:
        stunde, minute = int(wort), 0
        n += 2
    elif (teile := re.fullmatch(r"(\d{1,2})uhr", wort)):
        stunde, minute = int(teile[1]), 0
        n += 1
    else:
        return None
    if stunde > 23 or minute > 59:
        return None
    return n, f"{stunde:02d}:{minute:02d}"


def _datum(woerter, i, today):
    """Datumsausdruck ab Wort i: (Anzahl Wörter, Tag) oder None."""
    n = 0
    if i < len(woerter) and woerter[i].wort in ("am", "zum"):
        n = 1
    nur_kuenftig = False
    if i + n < len(woerter) and woerter[i + n].wort in ("nächsten", "naechsten", "kommenden"):
        nur_kuenftig = True
        n += 1
    if i + n >= len(woerter):
        return None
    wort = woerter[i + n]
    if wort.wort == "in" and i + n + 2 < len(woerter):
        zahl = woerter[i + n + 1].wort
        einheit = woerter[i + n + 2].wort
        menge = 1 if zahl in ("einem", "einer") else int(zahl) if re.fullmatch(r"\d{1,3}", zahl) else None
        if menge is not None and re.fullmatch(r"tag(?:en)?|woche(?:n)?", einheit):
            return n + 3, today + timedelta(days=menge * (7 if einheit.startswith("woche") else 1))
        return None
    tag = _tag(wort, today)
    if tag is None:
        return None
    if nur_kuenftig:
        if wort.wort not in WEEKDAYS:
            return None
        if tag <= today:
            tag += timedelta(days=7)
    return n + 1, tag


def _aufwand(woerter, i):
    """Aufwand ab Wort i: (Anzahl Wörter, Minuten) oder None."""
    def menge(wort):
        if (teile := re.fullmatch(r"(\d{1,3})(?:[,.](\d))?", wort)):
            return int(teile[1]) + (int(teile[2]) / 10 if teile[2] else 0)
        return None

    def einheit(wort):
        if re.fullmatch(r"min|minute|minuten", wort):
            return 1
        if re.fullmatch(r"h|std|stunde|stunden", wort):
            return 60
        return None

    if i >= len(woerter):
        return None
    zusammen = re.fullmatch(r"(\d{1,3}(?:[,.]\d)?)(min|h|std)", woerter[i].wort)
    if zusammen:
        n, minuten = 1, menge(zusammen[1]) * einheit(zusammen[2])
    elif i + 1 < len(woerter) and menge(woerter[i].wort) is not None and einheit(woerter[i + 1].wort):
        n, minuten = 2, menge(woerter[i].wort) * einheit(woerter[i + 1].wort)
    else:
        return None
    # „1 Std. 30 Min.“ gehört zusammen.
    if einheit(woerter[i + n - 1].wort if not zusammen else zusammen[2]) == 60 and i + n + 1 < len(woerter):
        rest = menge(woerter[i + n].wort)
        if rest is not None and einheit(woerter[i + n + 1].wort) == 1:
            n, minuten = n + 2, minuten + rest
    minuten = round(minuten)
    if not 0 < minuten <= MAX_ESTIMATE_MINUTES:
        return None
    return n, minuten


ORDINAL_WORDS = {"ersten": 1, "zweiten": 2, "dritten": 3, "vierten": 4, "fünften": 5, "fuenften": 5,
                 "letzten": -1}
ORDINAL_FEMININE = {"zweite": 2, "dritte": 3, "vierte": 4}
UNSUPPORTED_REPEAT = "wird noch nicht unterstützt – bleibt Text"


def _extended_wiederholung(words, i, today):
    tokens = words[i:i + 18]
    w = [v.wort for v in tokens]
    if not w:
        return None

    def number(word):
        return NUMBER_WORDS.get(word) or (int(word) if re.fullmatch(r"[0-9]{1,3}", word) else None)

    def first(rule):
        if repeat_logic.ics_recurrence.matches_start(today, rule["rrule"]):
            return today
        return repeat_logic.next_date(rule, today, today)

    def result(n, rule, day=None):
        day = day or first(rule)
        if day is None:
            return None
        return n, rule, day, repeat_logic.describe_series(rule)

    def day_index(word):
        name = word[:-1] if word.endswith("s") else word
        return WEEKDAYS.index(name) if name in WEEKDAYS else None

    def month_suffix(k):
        return 2 if w[k:k+2] in (["im", "monat"], ["des", "monats"], ["jedes", "monats"]) else 0

    # Ausdrückliche Monatsposition: ohne „im Monat“ bleibt „jeden zweiten
    # Dienstag“ die bisherige Zweiwochenregel (FP-00).
    k = 1 if w[0] in ("jeden", "am") else 2 if w[:2] == ["monatlich", "am"] else -1
    if k >= 0 and k + 1 < len(w):
        position = ORDINAL_WORDS.get(w[k])
        if position is None and re.fullmatch(r"[1-5]", w[k]) and tokens[k].datum.endswith("."):
            position = int(w[k])
        end = k + 2
        suffix = month_suffix(end)
        monthly = bool(suffix or k == 2)
        if position in (1, 2, 3, 4, 5, -1) and monthly:
            weekday = day_index(w[k+1])
            if weekday is not None:
                return result(end+suffix, repeat_logic.from_series_fields("serie_position", 1,
                              position=position, weekday=weekday))
            if position == -1 and w[k+1] in ("tag", "werktag"):
                return result(end+suffix, repeat_logic.from_series_fields(
                    "serie_werktag" if w[k+1] == "werktag" else "serie_letzter", 1))

    if len(w) >= 3 and w[0] in ("alle", "jede"):
        n = number(w[1]) if w[0] == "alle" else ORDINAL_FEMININE.get(w[1])
        if n is None or not 1 <= n <= 365:
            return None
        unit = w[2]
        if unit in ("monat", "monate", "monaten", "jahr", "jahre", "jahren"):
            kind = "serie_jahr" if unit.startswith("jahr") else "serie_monat"
            end = 3; day = today
            if len(w) > end and w[end] in ("am", "zum"):
                end += 1
                if end >= len(w):return None
                if kind == "serie_monat" and re.fullmatch(r"[0-9]{1,2}", w[end]):
                    target = int(w[end])
                    if not 1 <= target <= 31:return None
                    while day.day != target:day += timedelta(days=1)
                elif kind == "serie_jahr":
                    day = _tag(tokens[end], today)
                    if day is None:return None
                else:return None
                end += 1
            return result(end, repeat_logic.from_series_fields(kind, n), day)
        if unit in ("woche", "wochen"):
            end = 3
            if len(w) > end and w[end] in ("am", "immer"):end += 1
            days = []
            while end < len(w):
                day = day_index(w[end])
                if day is None:break
                days.append(day);end += 1
                if end < len(w) and w[end] == "und":end += 1
            if len(set(days)) > 1 and n > 1:
                return result(end, repeat_logic.from_series_fields("serie_woche", n, sorted(set(days))))
    if len(w) >= 4 and number(w[0]) and w[1] in ("tag", "tage", "tagen") and w[2:4] == ["nach", "erledigung"]:
        n = number(w[0])
        return 2, {"art": REPEAT_EVERY_N_DAYS, "abstand": n}, today, f"alle {n} Tage"
    if w[:2] == ["jedes", "quartal"]:
        return result(2, repeat_logic.from_series_fields("serie_monat", 3), today)
    return None


def _wiederholung(words, i, today):
    value = _extended_wiederholung(words, i, today) or _base_wiederholung(words, i, today)
    if value is None or value[1] is None:
        return value
    n, rule, first, text = value
    w = [word.wort for word in words[i:]]
    options = {}
    if w[n:n+2] in (["nach", "erledigung"], ["ab", "erledigung"]):
        options["bezug"] = "erledigt"; n += 2; text += " ab Erledigung"
    if w[n:n+1] == ["pausiert"]:
        options["pausiert"] = True; n += 1; text += " pausiert"
    if n+2 < len(w) and w[n] == "insgesamt" and re.fullmatch(r"[0-9]{1,5}", w[n+1]) and w[n+2] in ("termin", "termine", "terminen"):
        remaining = int(w[n+1])
        if not 1 <= remaining <= 10000:
            return n+3, None, None, "Wiederholung: Anzahl muss zwischen 1 und 10.000 liegen – bleibt Text"
        options["rest"] = remaining;n += 3;text += f" · noch {remaining} Termine"
    if options:
        rule = dict(rule, **options)
    if options or rule.get("art") == repeat_logic.SERIES:
        text += f" · erster Termin {first:%d.%m.%Y}"
    return n, rule, first, text


def _base_wiederholung(woerter, i, today):
    """Wiederholung ab Wort i: (Anzahl Wörter, Regel ohne Start, erster Termin, Text) oder None.

    Eine Angabe wird ganz oder gar nicht gedeutet (A29): Folgt einem Rhythmus
    ein Ankertag oder Wochentag, gehört er dazu. Was das Datenformat nicht
    abbilden kann, liefert die Regel None und einen Hinweistext – die Wörter
    bleiben dann vollständig Titel und werden nicht teilweise als Datum gelesen.
    """
    if i >= len(woerter):
        return None
    w = [wort.wort for wort in woerter[i:i + 10]]
    d = [wort.datum for wort in woerter[i:i + 10]]

    def naechster(tage):
        return min(today + timedelta(days=(tag - today.weekday()) % 7) for tag in tage)

    def wochentag(wort):
        """Wochentag aus „Montag“ oder „montags“, sonst None."""
        name = wort[:-1] if wort.endswith("s") and wort[:-1] in WEEKDAYS else wort
        return WEEKDAYS.index(name) if name in WEEKDAYS else None

    def wochentage(start):
        """„Montag“, „Montag und Donnerstag“, „Montag, Mittwoch und Freitag“ ab Position start."""
        tage, n = [], start
        while n < len(w):
            tag = wochentag(w[n])
            if tag is None:
                break
            tage.append(tag)
            n += 1
            if n + 1 < len(w) and w[n] == "und" and wochentag(w[n + 1]) is not None:
                n += 1
            elif not (n < len(w) and woerter[i + n - 1].roh.endswith(",") and wochentag(w[n]) is not None):
                break
        return sorted(set(tage)), n - start

    def tage_text(tage):
        namen = [WEEKDAYS[tag] + "s" for tag in tage]
        return namen[0] if len(namen) == 1 else ", ".join(namen[:-1]) + " und " + namen[-1]

    def ordinal(k):
        """Ordnungszahl an Position k: (Wert, Wörter) oder None; „2.“ oder „zweiten“."""
        if k >= len(w):
            return None
        if re.fullmatch(r"\d{1,2}", w[k]) and d[k].endswith("."):
            return int(w[k]), 1
        if w[k] in ORDINAL_WORDS:
            return ORDINAL_WORDS[w[k]], 1
        return None

    def im_monat(k):
        """Länge von „im Monat“, „des Monats“ oder „jedes Monats“ an Position k, sonst 0."""
        if w[k:k + 2] in (["im", "monat"], ["des", "monats"], ["jedes", "monats"]):
            return 2
        return 0

    def nach_tagen(k):
        """Optionale Wochentage nach einem Rhythmus: (Tage, Wörter) – „am Montag“, „montags“."""
        n = 1 if k < len(w) and w[k] in ("am", "immer") else 0
        tage, laenge = wochentage(k + n)
        return (tage, n + laenge) if tage else ([], 0)

    def hinweis(n, was):
        return n, None, None, f"Wiederholung „{was}“ {UNSUPPORTED_REPEAT}"

    if w[0] in ("täglich", "taeglich") or w[:2] == ["jeden", "tag"]:
        n = 1 if w[0] != "jeden" else 2
        return n, {"art": REPEAT_DAILY}, today, "täglich"
    if w[0] == "werktags" or w[:2] == ["jeden", "werktag"] or w[:2] == ["an", "werktagen"]:
        n = 1 if w[0] == "werktags" else 2
        return n, {"art": REPEAT_WEEKDAYS, "tage": [0, 1, 2, 3, 4]}, naechster(range(5)), "werktags"
    if w[0] in ("wöchentlich", "woechentlich") or w[:2] == ["jede", "woche"]:
        n = 1 if w[0] != "jede" else 2
        tage, laenge = nach_tagen(n)
        if not tage:
            return n, {"art": REPEAT_WEEKLY}, today, "wöchentlich"
        if len(tage) == 1:
            return n + laenge, {"art": REPEAT_WEEKLY}, naechster(tage), "wöchentlich " + tage_text(tage)
        return n + laenge, {"art": REPEAT_WEEKDAYS, "tage": tage}, naechster(tage), tage_text(tage)
    if w[0] == "monatlich" or w[:2] == ["jeden", "monat"]:
        n = 1 if w[0] == "monatlich" else 2
        k = n + (1 if n < len(w) and w[n] in ("am", "zum") else 0)
        tag = None
        if k < len(w) and re.fullmatch(r"\d{1,2}", w[k]) and (d[k].endswith(".") or k > n):
            tag = int(w[k])
        elif k < len(w) and w[k] == "ersten":
            tag = 1
        elif k < len(w) and w[k] == "letzten":
            laenge = k + 1 + (1 if k + 1 < len(w) and w[k + 1] in ("tag", "werktag") else 0)
            return hinweis(laenge, " ".join(woerter[i + x].roh for x in range(laenge)))
        if tag is None:
            return n, {"art": REPEAT_MONTHLY}, today, "monatlich"
        if not 1 <= tag <= 31:
            return None
        erster = today
        while erster.day != tag:
            erster += timedelta(days=1)
        return k + 1, {"art": REPEAT_MONTHLY}, erster, f"monatlich am {tag}."
    if w[0] in ("jährlich", "jaehrlich") or w[:2] == ["jedes", "jahr"]:
        n = 1 if w[0] != "jedes" else 2
        k = n + (1 if n < len(w) and w[n] in ("am", "zum") else 0)
        if k < len(w) and re.fullmatch(r"\d{1,2}\.\d{1,2}\.", d[k]):
            erster = _tag(woerter[i + k], today)
            if erster is not None:
                return k + 1, {"art": REPEAT_YEARLY}, erster, f"jährlich am {erster:%d.%m.}"
        return n, {"art": REPEAT_YEARLY}, today, "jährlich"
    if w[0] == "jede" and len(w) >= 3 and w[2] == "woche" and (
            w[1] in ORDINAL_FEMININE or (re.fullmatch(r"\d", w[1]) and d[1].endswith("."))):
        menge = ORDINAL_FEMININE.get(w[1]) or int(w[1])
        tage, laenge = nach_tagen(3)
        if len(tage) > 1:
            return hinweis(3 + laenge, " ".join(woerter[i + x].roh for x in range(3 + laenge)))
        erster = naechster(tage) if tage else today
        text = f"alle {menge} Wochen" + (" " + tage_text(tage) if tage else "")
        return 3 + laenge, {"art": REPEAT_EVERY_N_DAYS, "abstand": menge * 7}, erster, text
    if w[0] == "jeden" and (stelle := ordinal(1)):
        wert, laenge = stelle
        tag = wochentag(w[1 + laenge]) if 1 + laenge < len(w) else None
        if tag is None and 1 + laenge < len(w) and w[1 + laenge] == "tag" and 2 <= wert <= REPEAT_MAX_INTERVAL:
            return 2 + laenge, {"art": REPEAT_EVERY_N_DAYS, "abstand": wert}, today, f"alle {wert} Tage"
        if tag is None:
            # „jeden 15.“ ist ein Monatstag; „jeden 2. und 4. …“ bleibt Text.
            if wert > 0 and 1 + laenge < len(w) and w[1 + laenge] in ("und", "oder"):
                return hinweis(1 + laenge, " ".join(woerter[i + x].roh for x in range(1 + laenge)))
            if wert < 1 or wert > 31 or not d[1].endswith("."):
                return None
            erster = today
            while erster.day != wert:
                erster += timedelta(days=1)
            ende = 2 + im_monat(2)
            return ende, {"art": REPEAT_MONTHLY}, erster, f"monatlich am {wert}."
        ende = 2 + laenge
        monat = im_monat(ende)
        if monat or wert in (1, -1):
            # Position im Monat („zweiter Dienstag im Monat“, „erster Montag“, „letzter Freitag“)
            # kennt das heutige Format nicht.
            ende += monat
            return hinweis(ende, " ".join(woerter[i + x].roh for x in range(ende)))
        if not 2 <= wert <= 5:
            return None
        return ende, {"art": REPEAT_EVERY_N_DAYS, "abstand": wert * 7}, naechster([tag]), \
            f"alle {wert} Wochen {tage_text([tag])}"
    if w[0] == "jeden" or wochentag(w[0]) is not None and w[0].endswith("s"):
        start = 1 if w[0] == "jeden" else 0
        if start and (len(w) < 2 or w[1] not in WEEKDAYS):
            return None
        tage, laenge = wochentage(start)
        if not tage:
            return None
        text = ("jeden " + WEEKDAYS[tage[0]].capitalize()) if len(tage) == 1 else tage_text(tage)
        regel = {"art": REPEAT_WEEKLY} if len(tage) == 1 else {"art": REPEAT_WEEKDAYS, "tage": tage}
        return start + laenge, regel, naechster(tage), text
    if w[0] == "alle" and len(w) >= 3:
        menge = NUMBER_WORDS.get(w[1]) or (int(w[1]) if re.fullmatch(r"\d{1,3}", w[1]) else None)
        if menge is None:
            return None
        if re.fullmatch(r"monate?n?|jahre?n?|quartale?n?", w[2]):
            return hinweis(3, " ".join(woerter[i + x].roh for x in range(3)))
        if re.fullmatch(r"tage?n?", w[2]):
            tage_abstand, wochen = menge, False
        elif re.fullmatch(r"wochen?", w[2]):
            tage_abstand, wochen = menge * 7, True
        else:
            return None
        if not 1 <= tage_abstand <= REPEAT_MAX_INTERVAL:
            return None
        tage, laenge = nach_tagen(3) if wochen else ([], 0)
        if len(tage) > 1 and menge > 1:
            return hinweis(3 + laenge, " ".join(woerter[i + x].roh for x in range(3 + laenge)))
        if tage and menge == 1:
            regel = {"art": REPEAT_WEEKLY} if len(tage) == 1 else {"art": REPEAT_WEEKDAYS, "tage": tage}
            return 3 + laenge, regel, naechster(tage), "wöchentlich " + tage_text(tage)
        if tage_abstand == 1:
            return 3, {"art": REPEAT_DAILY}, today, "täglich"
        text = f"alle {menge} Wochen" if wochen else f"alle {menge} Tage"
        if tage:
            return 3 + laenge, {"art": REPEAT_EVERY_N_DAYS, "abstand": tage_abstand}, naechster(tage), \
                text + " " + tage_text(tage)
        return 3, {"art": REPEAT_EVERY_N_DAYS, "abstand": tage_abstand}, today, text
    if w[0] == "jedes" and len(w) >= 2 and w[1] == "quartal":
        return hinweis(2, " ".join(woerter[i + x].roh for x in range(2)))
    return None


def _erinnerung(woerter, i, today):
    """Erinnerung ab Wort i (nach dem Auslösewort).

    Liefert (Anzahl Wörter, Felder) oder None. Fest: {"mode": "fixed", "day":
    ISO oder None, "time": "HH:MM"}; der Tag fehlt, wenn keiner genannt ist –
    dann gilt der Bearbeitungstag, sonst die Fälligkeit, sonst heute. Vorlauf:
    {"mode": "relative", "minutes": N}.
    """
    if i >= len(woerter):
        return None
    w = [wort.wort for wort in woerter[i:i + 6]]
    if w[:2] in (["bei", "fälligkeit"], ["bei", "faelligkeit"], ["zur", "fälligkeit"], ["zur", "faelligkeit"]):
        return 2, {"mode": "relative", "minutes": 0}
    # Vorlauf: „30 min vorher“, „1 Std. vorher“, „2h vorher“, „einen Tag vorher“.
    menge, n = None, 0
    if (teile := re.fullmatch(r"(\d{1,4})(min|h|std)", w[0])):
        menge, einheit, n = int(teile[1]), teile[2], 1
    elif len(w) > 1:
        zahl = 1 if w[0] in ("einen", "eine", "einer") else int(w[0]) if re.fullmatch(r"\d{1,4}", w[0]) else None
        if zahl is not None:
            menge, einheit, n = zahl, w[1], 2
    if menge is not None and n < len(w) and w[n] == "vorher":
        faktor = (1 if re.fullmatch(r"min|minute|minuten", einheit) else
                  60 if re.fullmatch(r"h|std|stunde|stunden", einheit) else
                  1440 if re.fullmatch(r"tag|tage|tagen", einheit) else None)
        if faktor and 0 <= menge * faktor <= REMINDER_MAX_MINUTES:
            return n + 1, {"mode": "relative", "minutes": menge * faktor}
        return None
    # Fester Zeitpunkt: optional ein Tag, dann eine Uhrzeit („um 9“ genügt hier).
    n, tag = 0, None
    if (datum := _datum(woerter, i, today)):
        n, tag = datum[0], datum[1]
    if (zeit := _zeit(woerter, i + n)):
        return n + zeit[0], {"mode": "fixed", "day": tag.isoformat() if tag else None, "time": zeit[1]}
    if (i + n + 1 < len(woerter) and woerter[i + n].wort == "um"
            and re.fullmatch(r"\d{1,2}", woerter[i + n + 1].wort) and int(woerter[i + n + 1].wort) <= 23):
        return n + 2, {"mode": "fixed", "day": tag.isoformat() if tag else None,
                       "time": f"{int(woerter[i + n + 1].wort):02d}:00"}
    return None


def parse_capture(text, labels=(), today=None, ignore=()):
    """Zerlegt eine Eingabezeile in Titel, Felder und erkannte Teile.

    ``ignore`` enthält Schlüssel zurückgenommener Teile; ihr Text bleibt im
    Titel und wird auch nicht teilweise neu gedeutet.
    """
    today = today or date.today()
    text = str(text or "")
    ignore = set(ignore or ())
    namen = {str(label.get("name") or "").strip().lower(): (label.get("id"), str(label.get("name")))
             for label in labels or () if isinstance(label, dict) and label.get("id") and label.get("name")}
    geschuetzt = _geschuetzt(text)
    woerter = _woerter(text, geschuetzt)
    teile, zeiten = [], []
    belegt = set()
    wiederholung_hinweise = []

    def neu(i, n, felder, beschreibung, art, datum_ende=False):
        """Hält eine Stelle fest; eine zurückgenommene bleibt mit allen Wörtern Text."""
        ende = woerter[i + n - 1].ende_datum if datum_ende else woerter[i + n - 1].ende
        schluessel = " ".join(text[woerter[i].start:ende].lower().split())
        if schluessel not in ignore:
            teile.append((Teil(woerter[i].start, ende, schluessel, felder, beschreibung), art))
            belegt.add(art)
        return n

    i = 0
    while i < len(woerter):
        wort = woerter[i].wort
        verbraucht = None
        if (wort in REMINDER_WORDS or wort == "/erinnern") and "erinnerung" not in belegt:
            if (erinnerung := _erinnerung(woerter, i + 1, today)):
                verbraucht = neu(i, 1 + erinnerung[0], {"reminder": erinnerung[1]}, "Erinnerung", "erinnerung",
                                 datum_ende=True)
        if verbraucht is not None:
            pass
        elif wort.startswith("/") and len(wort) > 1:
            befehl = wort[1:]
            if befehl in ("bis", "fällig", "faellig") and "faellig" not in belegt:
                if (datum := _datum(woerter, i + 1, today)):
                    n, tag = 1 + datum[0], datum[1]
                    felder = {"due": tag.isoformat()}
                    if (zeit := _zeit(woerter, i + n)):
                        n += zeit[0]
                        felder["due_time"] = zeit[1]
                    verbraucht = neu(i, n, felder, _beschreibung("Fällig", felder["due"], felder.get("due_time")),
                                     "faellig", datum_ende=True)
            elif befehl == "meintag" and "plan" not in belegt:
                verbraucht = neu(i, 1, {"planned_date": today.isoformat()}, "Bearbeitungstag heute", "plan")
            elif befehl in SLASH_IMPORTANCE and "wichtig" not in belegt:
                stufe = SLASH_IMPORTANCE[befehl]
                verbraucht = neu(i, 1, {"importance": stufe}, f"Wichtigkeit {IMPORTANCE_NAMES[stufe]}", "wichtig")
            elif "plan" not in belegt and (tag := _tag(woerter[i]._replace(wort=befehl, datum=woerter[i].datum[1:]), today)):
                verbraucht = neu(i, 1, {"planned_date": tag.isoformat()},
                                 _beschreibung("Bearbeitungstag", tag.isoformat()), "plan", datum_ende=True)
            elif befehl in namen:
                kennung, name = namen[befehl]
                verbraucht = neu(i, 1, {"labels": [kennung]}, f"Label {name}", "label")
        elif wort.startswith("!") and wort[1:] in IMPORTANCE and "wichtig" not in belegt:
            stufe = IMPORTANCE[wort[1:]]
            verbraucht = neu(i, 1, {"importance": stufe}, f"Wichtigkeit {IMPORTANCE_NAMES[stufe]}", "wichtig")
        elif wort.startswith("#") and wort[1:] in namen:
            kennung, name = namen[wort[1:]]
            verbraucht = neu(i, 1, {"labels": [kennung]}, f"Label {name}", "label")
        elif wort in ("bis", "fällig", "faellig") and "faellig" not in belegt:
            n = 1
            if wort != "bis" and i + 1 < len(woerter) and woerter[i + 1].wort in ("bis", "am"):
                n = 2
            felder = None
            if (datum := _datum(woerter, i + n, today)):
                n += datum[0]
                felder = {"due": datum[1].isoformat()}
                if (zeit := _zeit(woerter, i + n)):
                    n += zeit[0]
                    felder["due_time"] = zeit[1]
            elif (zeit := _zeit(woerter, i + n)):
                n += zeit[0]
                felder = {"due": today.isoformat(), "due_time": zeit[1]}
            if felder:
                ende_datum = "due_time" not in felder
                verbraucht = neu(i, n, felder, _beschreibung("Fällig", felder["due"], felder.get("due_time")),
                                 "faellig", datum_ende=ende_datum)
        if verbraucht is None and "wiederholung" not in belegt and (regel := _wiederholung(woerter, i, today)):
            n, wiederholung, erster, beschreibung = regel
        else:
            wiederholung = False
        if wiederholung is None:
            # Nicht abbildbar: ein Hinweis ohne Wirkung, die Wörter bleiben
            # vollständig Titel und werden nicht teilweise gedeutet (A29).
            ende = woerter[i + n - 1].ende_datum
            wiederholung_hinweise.append(Teil(woerter[i].start, ende, " ".join(text[woerter[i].start:ende].lower().split()),
                                              {}, beschreibung))
            belegt.add("wiederholung")
            verbraucht = n
        elif wiederholung:
            felder = {"repeat": wiederholung, "due": erster.isoformat()}
            if (zeit := _zeit(woerter, i + n)):
                n += zeit[0]
                felder["due_time"] = zeit[1]
            verbraucht = neu(i, n, felder, f"Wiederholung {beschreibung}", "wiederholung",
                             datum_ende="due_time" not in felder)
        if verbraucht is None and "plan" not in belegt and (datum := _datum(woerter, i, today)):
            n, felder = datum[0], {"planned_date": datum[1].isoformat()}
            if (zeit := _zeit(woerter, i + n)):
                n += zeit[0]
                felder["planned_time"] = zeit[1]
            verbraucht = neu(i, n, felder, _beschreibung("Bearbeitungstag", felder["planned_date"],
                                                         felder.get("planned_time")),
                             "plan", datum_ende="planned_time" not in felder)
        if verbraucht is None and "zeit" not in belegt and (zeit := _zeit(woerter, i)):
            verbraucht = neu(i, zeit[0], {"planned_time": zeit[1]}, f"Uhrzeit {zeit[1]}", "zeit")
        if verbraucht is None and "aufwand" not in belegt and (aufwand := _aufwand(woerter, i)):
            verbraucht = neu(i, aufwand[0], {"estimated_minutes": aufwand[1]},
                             f"Aufwand {format_minutes(aufwand[1])}", "aufwand", datum_ende=True)
        i += verbraucht or 1

    # Eine ausdrückliche Fälligkeit („bis Freitag“) hat Vorrang: Die Reihe
    # beginnt dann dort. Sonst ist der erste Termin der Reihe die Fälligkeit.
    ausdruecklich = next((t for t, a in teile if a == "faellig"), None)
    zusammen = []
    for teil, art in teile:
        if art == "wiederholung":
            regel = dict(teil.felder["repeat"])
            if ausdruecklich is not None:
                regel["start"] = ausdruecklich.felder["due"]
                teil = teil._replace(felder={"repeat": regel}, text=teil.text + " ab der Fälligkeit")
            else:
                regel["start"] = teil.felder["due"]
                felder_neu = dict(teil.felder, repeat=regel)
                teil = teil._replace(felder=felder_neu, text=teil.text + " · " + _beschreibung(
                    "fällig ab", teil.felder["due"], teil.felder.get("due_time")))
        zusammen.append((teil, art))
    teile = zusammen
    felder = {}
    for teil, art in teile:
        for key, value in teil.felder.items():
            if key == "labels":
                felder.setdefault("labels", [])
                felder["labels"] += [v for v in value if v not in felder["labels"]]
            else:
                felder.setdefault(key, value)
    # Erinnerung (KO03): fester Tag aus Bearbeitungstag, Fälligkeit oder heute;
    # ein Vorlauf ohne Fälligkeit wirkt nicht und bleibt deshalb Text.
    hinweise = list(wiederholung_hinweise)
    if "reminder" in felder:
        erinnerung = dict(felder["reminder"])
        teil = next(t for t, a in teile if a == "erinnerung")
        if erinnerung["mode"] == "fixed":
            erinnerung["day"] = erinnerung["day"] or felder.get("planned_date") or felder.get("due") or today.isoformat()
            text_chip = f"Erinnerung {format_day(erinnerung['day'])} {erinnerung['time']} · {REMINDER_NOTE}"
            felder["reminder"] = erinnerung
            teile = [((t._replace(felder={"reminder": erinnerung}, text=text_chip)) if a == "erinnerung" else t, a)
                     for t, a in teile]
        elif "due" not in felder:
            del felder["reminder"]
            hinweis = teil._replace(felder={}, text="Erinnerung mit Vorlauf braucht eine Fälligkeit – bleibt Text")
            hinweise.append(hinweis)
            teile = [(t, a) for t, a in teile if a != "erinnerung"]
        else:
            minuten = erinnerung["minutes"]
            vorlauf = ("bei Fälligkeit" if not minuten else
                       f"{minuten // 1440} Tag(e) vor Fälligkeit" if minuten % 1440 == 0 else
                       f"{format_minutes(minuten)} vor Fälligkeit")
            teile = [((t._replace(text=f"Erinnerung {vorlauf} · {REMINDER_NOTE}")) if a == "erinnerung" else t, a)
                     for t, a in teile]
    # Eine Uhrzeit ohne eigenes Datum hängt am Bearbeitungstag – ohne ihn gilt heute.
    ergebnis_teile = []
    for teil, art in teile:
        if art == "zeit":
            if "planned_time" in felder and teil.felder["planned_time"] != felder["planned_time"]:
                continue
            if not any(a == "plan" for _t, a in teile):
                felder["planned_date"] = today.isoformat()
                teil = teil._replace(text=f"{teil.text} (heute)")
        ergebnis_teile.append(teil)
    titel = _titel(text, [t for t in ergebnis_teile])
    # Hinweise sind Chips ohne Wirkung: Ihr Text bleibt im Titel.
    return Erfassung(titel, felder, tuple(sorted(ergebnis_teile + hinweise, key=lambda t: t.start)))


def _beschreibung(art, iso, zeit=None):
    return f"{art} {format_day(iso)}" + (f" {zeit}" if zeit else "")


def _titel(text, teile):
    """Text ohne erkannte Stellen. Aufgeräumt wird nur, wo etwas herausgenommen wurde."""
    if not teile:
        return " ".join(text.split())
    stellen = sorted((t.start, t.ende) for t in teile)
    rest, pos = [], 0
    for start, ende in stellen:
        # Satzzeichen, die nur die herausgenommene Stelle abtrennten, fallen mit.
        rest.append(re.sub(r"[,;]\s*$", " ", text[pos:start]) if start > 0 else "")
        pos = max(pos, ende)
        while pos < len(text) and text[pos] in ",;":
            pos += 1
    rest.append(text[pos:])
    titel = " ".join("".join(rest).split())
    return titel.strip(" ,;:-")


# --- Mehrzeiliges Einfügen in die Eingabezeile (KO05 seit 3.33.20) ---------
MAX_PASTE_LINES = 200
_AUFZAEHLUNG = re.compile(r"^(?:[-*•–—+]|\d{1,3}[.)]|[a-zA-Z][)])\s+")
_KAESTCHEN = re.compile(r"^\[\s*([xX✓])?\s*\]\s*")


def split_capture_lines(text, limit=MAX_PASTE_LINES):
    """Zerlegt eingefügten Text in Aufgabenzeilen.

    Aufzählungszeichen, Nummern und Kästchen (`- [ ]`, `[x]`) am Zeilenanfang
    entfallen; ein abgehaktes Kästchen markiert die Zeile als erledigt. Leere
    Zeilen werden übersprungen, Leerraum zusammengezogen. Liefert (Zeilen,
    abgeschnitten); jede Zeile ist {"text": …, "done": bool}.
    """
    zeilen = []
    for roh in str(text or "").splitlines():
        zeile = " ".join(roh.split())
        if not zeile:
            continue
        zeile = _AUFZAEHLUNG.sub("", zeile, count=1)
        erledigt = False
        if (kaestchen := _KAESTCHEN.match(zeile)):
            erledigt = bool(kaestchen.group(1))
            zeile = zeile[kaestchen.end():]
        zeile = zeile.strip()
        if zeile:
            zeilen.append({"text": zeile, "done": erledigt})
    return zeilen[:limit], len(zeilen) > limit
