"""Begrenzte übliche iCalendar-Serien nach RFC 5545 §3.3.10, ohne Tk.

Tägliche, wöchentliche, monatliche und jährliche Datumsfolgen. Der Aufrufer
prüft lokale Uhrzeiten über valid, bevor sie COUNT verbrauchen; fehlende
Sommerzeit-Uhrzeiten werden dadurch übersprungen. Unbekannte Regelteile
werden ausdrücklich abgewiesen, niemals still angenähert.
Quelle: https://www.rfc-editor.org/rfc/rfc5545#section-3.3.10
"""
import calendar
from dataclasses import dataclass
from datetime import date, timedelta
import re

WEEKDAYS = {name: index for index, name in enumerate(("MO", "TU", "WE", "TH", "FR", "SA", "SU"))}
SUPPORTED = {"FREQ", "INTERVAL", "COUNT", "UNTIL", "BYDAY", "BYMONTH", "BYMONTHDAY", "BYSETPOS", "WKST"}


class RuleError(ValueError):
    pass


class ExpansionLimitError(RuntimeError):
    """Ein Kalender ist für eine interaktive lokale Vorschau zu aufwendig."""


@dataclass
class Budget:
    remaining: int = 200000

    def take(self, amount=1):
        self.remaining -= amount
        if self.remaining < 0:
            raise ExpansionLimitError(
                "Serienberechnung überschreitet die lokale Prüfgrenze; bitte den Kalenderzeitraum begrenzen.")


@dataclass(frozen=True)
class Rule:
    frequency: str
    interval: int = 1
    count: int | None = None
    until: str | None = None
    weekdays: tuple = ()
    months: tuple = ()
    monthdays: tuple = ()
    positions: tuple = ()
    week_start: int = 0


def _integer(value, minimum, maximum, zero=False):
    if not re.fullmatch(r"[+-]?\d+", value):
        raise RuleError("Serienregel enthält keine gültige ganze Zahl.")
    number = int(value)
    if not minimum <= number <= maximum or (number == 0 and not zero):
        raise RuleError("Zahl der Serienregel liegt außerhalb des erlaubten Bereichs.")
    return number


def parse_rule(text):
    fields = {}
    for part in str(text).upper().split(";"):
        name, separator, value = part.partition("=")
        if not separator or not value or name in fields:
            raise RuleError("Serienregel ist unvollständig oder enthält doppelte Teile.")
        fields[name] = value
    if set(fields) - SUPPORTED:
        raise RuleError("Nicht unterstützte Serienteile: " + ", ".join(sorted(set(fields) - SUPPORTED)))
    frequency = fields.get("FREQ")
    if frequency not in ("DAILY", "WEEKLY", "MONTHLY", "YEARLY"):
        raise RuleError("Nur tägliche, wöchentliche, monatliche und jährliche Serien werden unterstützt.")
    if "COUNT" in fields and "UNTIL" in fields:
        raise RuleError("COUNT und UNTIL dürfen nicht gemeinsam stehen.")
    interval = _integer(fields.get("INTERVAL", "1"), 1, 2147483647)
    count = _integer(fields["COUNT"], 1, 2147483647) if "COUNT" in fields else None
    until = fields.get("UNTIL")
    if until:
        if not re.fullmatch(r"\d{8}(?:T\d{6}Z?)?", until):
            raise RuleError("UNTIL enthält kein unterstütztes Enddatum.")
        try:
            date(int(until[:4]), int(until[4:6]), int(until[6:8]))
            if len(until) > 8 and not (int(until[9:11]) < 24 and int(until[11:13]) < 60 and int(until[13:15]) < 60):
                raise ValueError
        except ValueError:
            raise RuleError("UNTIL enthält kein gültiges Enddatum.") from None
    weekdays = []
    for token in fields.get("BYDAY", "").split(",") if "BYDAY" in fields else ():
        match = re.fullmatch(r"([+-]?\d+)?(MO|TU|WE|TH|FR|SA|SU)", token)
        if not match:
            raise RuleError("BYDAY enthält keinen gültigen Wochentag.")
        ordinal = _integer(match[1], -53, 53) if match[1] else None
        if ordinal is not None and frequency not in ("MONTHLY", "YEARLY"):
            raise RuleError("Nummerierte Wochentage brauchen eine Monats- oder Jahresserie.")
        if ordinal is not None and frequency == "MONTHLY" and abs(ordinal) > 5:
            raise RuleError("Monatlicher Wochentag muss zwischen -5 und 5 liegen.")
        weekdays.append((ordinal, WEEKDAYS[match[2]]))
    def numbers(name, minimum, maximum):
        return tuple(sorted({_integer(value, minimum, maximum) for value in fields[name].split(",")})) if name in fields else ()
    months = numbers("BYMONTH", 1, 12)
    monthdays = numbers("BYMONTHDAY", -31, 31)
    positions = numbers("BYSETPOS", -366, 366)
    if monthdays and frequency == "WEEKLY":
        raise RuleError("BYMONTHDAY darf nicht in einer Wochenserie stehen.")
    if positions and not (weekdays or months or monthdays):
        raise RuleError("BYSETPOS braucht einen weiteren BY-Teil.")
    week_start = fields.get("WKST", "MO")
    if week_start not in WEEKDAYS:
        raise RuleError("WKST enthält keinen gültigen Wochentag.")
    return Rule(frequency, interval, count, until, tuple(dict.fromkeys(weekdays)), months,
                monthdays, positions, WEEKDAYS[week_start])


def _period(start, rule, index):
    if rule.frequency == "DAILY":
        first = start + timedelta(days=index * rule.interval)
        return first, (first,)
    if rule.frequency == "WEEKLY":
        ordinal = start.toordinal() - (start.weekday() - rule.week_start) % 7 + 7 * index * rule.interval
        first = date.fromordinal(max(1, ordinal))
        return first, tuple(date.fromordinal(value) for value in range(
            max(1, ordinal), min(date.max.toordinal(), ordinal + 6) + 1))
    if rule.frequency == "MONTHLY":
        year, month = divmod(start.year * 12 + start.month - 1 + index * rule.interval, 12)
        month += 1
        first = date(year, month, 1)
        return first, tuple(date(year, month, i) for i in range(1, calendar.monthrange(year, month)[1] + 1))
    year = start.year + index * rule.interval
    first = date(year, 1, 1)
    days = 366 if calendar.isleap(year) else 365
    return first, tuple(first + timedelta(days=i) for i in range(days))


def _matches(day, start, rule):
    if rule.months and day.month not in rule.months:
        return False
    if rule.monthdays:
        days = calendar.monthrange(day.year, day.month)[1]
        if day.day not in {value if value > 0 else days + value + 1 for value in rule.monthdays}:
            return False
    if rule.weekdays:
        matches = False
        for ordinal, weekday in rule.weekdays:
            if day.weekday() != weekday:
                continue
            if ordinal is None:
                matches = True
                break
            if rule.frequency == "YEARLY" and not rule.months:
                position = (day - date(day.year, 1, 1)).days
                remaining = (date(day.year, 12, 31) - day).days
            else:
                position = day.day - 1
                remaining = calendar.monthrange(day.year, day.month)[1] - day.day
            actual = position // 7 + 1 if ordinal > 0 else -(remaining // 7 + 1)
            if actual == ordinal:
                matches = True
                break
        if not matches:
            return False
    if rule.frequency == "WEEKLY" and not rule.weekdays:
        return day.weekday() == start.weekday()
    if rule.frequency == "MONTHLY" and not (rule.monthdays or rule.weekdays):
        return day.day == start.day
    if rule.frequency == "YEARLY":
        if not (rule.monthdays or rule.weekdays) and day.day != start.day:
            return False
        if not (rule.months or rule.monthdays or rule.weekdays) and day.month != start.month:
            return False
    return True


def matches_start(start, rule):
    """RFC: DTSTART außerhalb seines Regelfilters hat keine definierte Serie."""
    if isinstance(rule,str):
        rule = parse_rule(rule)
    _first,candidates = _period(start,rule,0)
    matching = [day for day in candidates if _matches(day,start,rule)]
    if rule.positions:
        matching = {matching[position-1 if position>0 else position]
                    for position in rule.positions if abs(position)<=len(matching)}
    return start in matching


def dates(start, rule, through, *, after=None, valid=lambda day: True, budget=None):
    """Inklusive Datumsgrenzen; COUNT zählt auch Vorkommen vor after.

    UNTIL-Zeit/Zeitzone prüft der Kalender-Aufrufer zusätzlich an der fertigen
    Uhrzeit. Die UTC-Datumskante bleibt hier um einen Tag weit, damit Termine
    jenseits des UTC-Tageswechsels nicht vorzeitig abgeschnitten werden.
    """
    if isinstance(rule, str):
        rule = parse_rule(rule)
    if type(start) is not date or type(through) is not date or (after is not None and type(after) is not date):
        raise RuleError("Serie braucht reine Datumswerte.")
    lower = after or start
    upper = through
    if rule.until:
        until_day = date(int(rule.until[:4]), int(rule.until[4:6]), int(rule.until[6:8]))
        if len(rule.until) > 8 and until_day < date.max:
            until_day += timedelta(days=1)
        upper = min(upper, until_day)
    if upper < start or lower > upper:
        return
    seen = 1
    if lower <= start <= upper:
        yield start
    if rule.count == 1:
        return
    budget = budget if budget is not None else Budget()
    index = 0
    if rule.count is None and lower > start:
        if rule.frequency == "DAILY":
            index = max(0, (lower - start).days // rule.interval - 1)
        elif rule.frequency == "WEEKLY":
            index = max(0, (lower - start).days // (7 * rule.interval) - 1)
        elif rule.frequency == "MONTHLY":
            index = max(0, ((lower.year - start.year) * 12 + lower.month - start.month) // rule.interval - 1)
        else:
            index = max(0, (lower.year - start.year) // rule.interval - 1)
    while True:
        try:
            first, candidates = _period(start, rule, index)
        except (OverflowError, ValueError):
            return
        if first > upper:
            return
        budget.take(len(candidates))
        matching = [day for day in candidates if _matches(day, start, rule)]
        if rule.positions:
            matching = sorted({matching[position - 1 if position > 0 else position]
                               for position in rule.positions if abs(position) <= len(matching)})
        for day in matching:
            if day <= start or day > upper or not valid(day):
                continue
            seen += 1
            if rule.count is not None and seen > rule.count:
                return
            if day >= lower:
                yield day
        index += 1
