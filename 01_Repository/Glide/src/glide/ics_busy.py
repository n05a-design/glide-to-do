"""Lokale ICS-Belegzeiten ohne Aufgabenimport, Tk oder Datenmutation.

RFC 5545 §§3.3.5/3.3.6/3.6.1/3.8.5: halb offene Enden, nominale
Tagesdauern, echte Zeitdauern, Serienvereinigung und einzelne Ausnahmen.
Quelle: https://datatracker.ietf.org/doc/html/rfc5545
Zeitzonen lassen sich durch einen geprüften lokalen Resolver ergänzen.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import re
from zoneinfo import ZoneInfoNotFoundError
import ics_recurrence as recurrence
import ics_timezone
import timezones
from occupied_time import Block, utc

UTC = timezone.utc


@dataclass(frozen=True)
class Property:
    name: str
    params: dict
    value: str


@dataclass(frozen=True)
class Span:
    days: int = 0
    seconds: int = 0

    def end(self, start):
        nominal = start + timedelta(days=self.days)
        return (utc(nominal) + timedelta(seconds=self.seconds)).astimezone(start.tzinfo)


@dataclass(frozen=True)
class Event:
    uid: str
    title: str
    start: datetime | None
    span: Span
    all_day: bool
    rule: object = None
    until: datetime | None = None
    extra: tuple = ()
    excluded: frozenset = frozenset()
    identity: datetime | None = None
    cancelled: bool = False
    transparent: bool = False
    sequence: int = 0
    stamp: str = ""
    identity_all_day: bool | None = None


@dataclass(frozen=True)
class Calendar:
    events: tuple
    issues: tuple


@dataclass(frozen=True)
class Expansion:
    blocks: tuple
    issues: tuple


def _split(text, separator):
    result, current, quoted = [], [], False
    for character in text:
        if character == '"':
            quoted = not quoted
        if character == separator and not quoted:
            result.append(''.join(current)); current = []
        else:
            current.append(character)
    if quoted:
        raise ValueError("Nicht geschlossenes Anführungszeichen in ICS-Eigenschaft.")
    result.append(''.join(current))
    return result


def property_line(line):
    pieces = _split(line, ':')
    if len(pieces) < 2:
        raise ValueError("ICS-Eigenschaft ohne Doppelpunkt.")
    head, value = pieces[0], ':'.join(pieces[1:])
    pieces = _split(head, ';')
    params = {}
    for piece in pieces[1:]:
        name, separator, content = piece.partition('=')
        name = name.upper()
        if not separator or name in params:
            raise ValueError("Ungültige oder doppelte ICS-Parameter.")
        params[name] = content.strip('"')
    return Property(pieces[0].upper(), params, value)


def components(text):
    lines = []
    for line in str(text).lstrip('\ufeff').splitlines():
        if line.startswith((' ', '\t')):
            if not lines:
                raise ValueError("ICS-Faltung ohne vorherige Zeile.")
            lines[-1] += line[1:]
        elif line:
            lines.append(line)
    stack, events, zones, calendar_seen = [], [], [], False
    for line in lines:
        prop = property_line(line)
        if prop.name == 'BEGIN':
            name = prop.value.upper()
            if not stack:
                if name != 'VCALENDAR' or calendar_seen:
                    raise ValueError("Genau ein VCALENDAR-Kalender wird benötigt.")
                calendar_seen = True
            stack.append((name, [], []))
        elif prop.name == 'END':
            if not stack or stack[-1][0] != prop.value.upper():
                raise ValueError("Nicht zusammenpassende ICS-Komponenten.")
            name, properties, children = stack.pop()
            if stack:
                stack[-1][2].append((name,tuple(properties),tuple(children)))
            if name == 'VEVENT':
                events.append(tuple(properties))
            elif name == 'VTIMEZONE':
                zones.append((tuple(properties),tuple(children)))
        elif not stack:
            raise ValueError("ICS-Eigenschaft außerhalb des Kalenders.")
        else:
            stack[-1][1].append(prop)
    if stack or not calendar_seen:
        raise ValueError("Unvollständiger ICS-Kalender.")
    return events, zones


def text_value(value):
    return re.sub(r'\\([nN,;\\])', lambda m: '\n' if m[1].lower() == 'n' else m[1], value)


def valid_local(moment):
    return utc(moment).astimezone(moment.tzinfo).replace(tzinfo=None) == moment.replace(tzinfo=None)


def moment(prop, zone, resolver, date_zone=None):
    value = prop.value
    date_only = prop.params.get('VALUE', '').upper() == 'DATE'
    if date_only:
        if prop.params.get('TZID') or not re.fullmatch(r'\d{8}', value):
            raise ValueError("Ganztägiges Datum muss ohne TZID als JJJJMMTT vorliegen.")
        return datetime.strptime(value, '%Y%m%d').replace(tzinfo=date_zone or zone), True
    if prop.params.get('VALUE', 'DATE-TIME').upper() != 'DATE-TIME':
        raise ValueError("Nicht unterstützter Zeitwert: " + prop.params['VALUE'])
    if not re.fullmatch(r'\d{8}T\d{6}Z?', value):
        raise ValueError("Zeitpunkt muss als JJJJMMTTTHHMMSS mit optionalem Z vorliegen.")
    if value.endswith('Z'):
        if prop.params.get('TZID'):
            raise ValueError("UTC-Zeitpunkt darf keine zusätzliche TZID haben.")
        tz = UTC
    else:
        tzid = prop.params.get('TZID')
        try:
            tz = resolver(tzid) if tzid else zone
        except (ValueError, ZoneInfoNotFoundError):
            raise ValueError("Zeitzone nicht verfügbar: " + tzid) from None
    value = value.removesuffix('Z')
    found = datetime.strptime(value, '%Y%m%dT%H%M%S').replace(tzinfo=tz, fold=0)
    utc(found)
    return found, False


def duration(text, all_day):
    match = re.fullmatch(r'\+?P(?:(\d+)W|(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?)', text)
    if not match or text.endswith('T') or not any(value is not None for value in match.groups()):
        raise ValueError("Nicht unterstützte oder negative ICS-Dauer.")
    week, day, hour, minute, second = (int(value or 0) for value in match.groups())
    if all_day and any((hour, minute, second)):
        raise ValueError("Ganztägige Dauer muss aus Tagen oder Wochen bestehen.")
    return Span(week * 7 + day, hour * 3600 + minute * 60 + second)


def parse_calendar(text, zone, resolver=None, date_zone=None):
    resolver = timezones.Resolver() if resolver is None else resolver
    utc(datetime(2026, 1, 1, tzinfo=zone))
    events, issues = [], []
    raw_events, raw_zones = components(text)
    embedded, invalid_zones = {}, set()
    for properties, children in raw_zones:
        name = next((p.value for p in properties if p.name == 'TZID'), '')
        try:
            if name in embedded or name in invalid_zones:
                raise ValueError('Zeitzonenkennung ist mehrfach definiert: ' + name)
            embedded[name] = ics_timezone.parse_zone(properties, children)
        except ValueError as exc:
            invalid_zones.add(name)
            embedded.pop(name, None)
            issues.append((name, str(exc)))
    original_resolver = resolver
    def resolver(name):
        if name in invalid_zones:
            raise ValueError('Ungültige eingebettete Zeitzone: ' + name)
        return embedded[name] if name in embedded else original_resolver(name)
    for properties in raw_events:
        lookup = {}
        for prop in properties:
            lookup.setdefault(prop.name, []).append(prop)
        uid = lookup.get('UID', [Property('UID', {}, '')])[0].value
        try:
            def one(name, required=False):
                found = lookup.get(name, ())
                if len(found) > 1 or (required and not found):
                    raise ValueError("ICS-Eigenschaft fehlt oder ist mehrfach vorhanden: " + name)
                return found[0] if found else None
            uid = one('UID', True).value
            if not uid:
                raise ValueError("Leere Ereigniskennung.")
            cancelled = (one('STATUS').value.upper() == 'CANCELLED') if one('STATUS') else False
            transparent = (one('TRANSP').value.upper() == 'TRANSPARENT') if one('TRANSP') else False
            identity = one('RECURRENCE-ID')
            if identity and identity.params.get('RANGE'):
                raise ValueError("Serienausnahme mit RANGE wird nicht unterstützt.")
            identity, identity_all_day = moment(identity, zone, resolver, date_zone) if identity else (None,None)
            start_prop = one('DTSTART', not cancelled)
            start, all_day = moment(start_prop, zone, resolver, date_zone) if start_prop else (None, False)
            span = Span()
            end, length = one('DTEND'), one('DURATION')
            if end and length:
                raise ValueError("DTEND und DURATION dürfen nicht gemeinsam vorkommen.")
            if start:
                if end:
                    finish, end_all_day = moment(end, zone, resolver, date_zone)
                    if end_all_day != all_day or utc(finish) <= utc(start):
                        raise ValueError("Ereignisende passt nicht zum Beginn.")
                    span = Span((finish.date()-start.date()).days) if all_day else Span(seconds=int((utc(finish)-utc(start)).total_seconds()))
                elif length:
                    span = duration(length.value, all_day)
                elif all_day:
                    span = Span(days=1)
                span.end(start)
            rule, until = None, None
            if one('RRULE') and start:
                try:
                    rule = recurrence.parse_rule(one('RRULE').value)
                    if not recurrence.matches_start(start.date(),rule):
                        raise ValueError('DTSTART stimmt nicht mit dem Serienfilter überein; die Folge ist laut RFC nicht definiert.')
                    if rule.until:
                        if not all_day and not start_prop.params.get('TZID') and not start_prop.value.endswith('Z') and rule.until.endswith('Z'):
                            raise ValueError('UNTIL einer lokalen Serie ohne TZID muss ebenfalls lokal vorliegen.')
                        if not all_day and (start_prop.params.get('TZID') or start_prop.value.endswith('Z')) and not rule.until.endswith('Z'):
                            raise ValueError('UNTIL einer zonierten Serie muss in UTC vorliegen.')
                        until_prop = Property('UNTIL', {'VALUE':'DATE'} if all_day else {}, rule.until)
                        until = moment(until_prop, start.tzinfo, resolver, date_zone)[0]
                        if all_day:
                            until += timedelta(days=1, microseconds=-1)
                except (ValueError, recurrence.RuleError) as exc:
                    rule = None
                    issues.append((uid, str(exc) + ' Weitere Serienvorkommen wurden nicht berücksichtigt.'))
            def moments(name):
                result = []
                for prop in lookup.get(name, ()):
                    for value in prop.value.split(','):
                        found, date_only = moment(Property(prop.name, prop.params, value), zone, resolver, date_zone)
                        if date_only != all_day:
                            raise ValueError(name + ' hat einen anderen Datumstyp als DTSTART.')
                        result.append(found)
                return tuple(result)
            extra = moments('RDATE')
            excluded = frozenset(utc(value) for value in moments('EXDATE'))
            sequence = int(one('SEQUENCE').value) if one('SEQUENCE') else 0
            if sequence < 0:
                raise ValueError("Negative Serienrevision.")
            stamp = one('DTSTAMP').value if one('DTSTAMP') else ''
            if stamp:
                stamp_moment,stamp_date = moment(one('DTSTAMP'),zone,resolver,date_zone)
                if stamp_date or not stamp.endswith('Z'):
                    raise ValueError('DTSTAMP muss eine UTC-Uhrzeit enthalten.')
            title = text_value(one('SUMMARY').value) if one('SUMMARY') else 'Belegte Zeit'
            events.append(Event(uid, title, start, span, all_day, rule, until, extra, excluded,
                                identity, cancelled, transparent, sequence, stamp, identity_all_day))
        except (ValueError, OverflowError) as exc:
            issues.append((uid, str(exc)))
    return Calendar(tuple(events), tuple(issues))


def expand(calendar, start, end, *, max_periods=200000, max_blocks=100000):
    lower, upper = utc(start), utc(end)
    if upper <= lower:
        raise ValueError("Betrachtungszeitraum muss positiv sein.")
    groups, issues, blocks = {}, list(calendar.issues), []
    budget = recurrence.Budget(max_periods)
    for event in calendar.events:
        group = groups.setdefault(event.uid, {})
        key = utc(event.identity) if event.identity else None
        if key in group:
            issues.append((event.uid, 'Mehrere Revisionen: neueste SEQUENCE/DTSTAMP berücksichtigt.'))
            if (event.sequence, event.stamp) < (group[key].sequence, group[key].stamp):
                continue
        group[key] = event
    def add(event, occurrence):
        if event.cancelled or event.transparent or occurrence is None:
            return
        finish = event.span.end(occurrence)
        if utc(finish) > utc(occurrence) and utc(occurrence) < upper and utc(finish) > lower:
            if len(blocks) >= max_blocks:
                raise recurrence.ExpansionLimitError(
                    "Zu viele Kalenderintervalle; bitte den Kalenderzeitraum begrenzen.")
            blocks.append(Block(occurrence, finish, event.title, event.all_day))
    for uid, group in groups.items():
        before = len(blocks)
        try:
            master = group.pop(None, None)
            if master and master.cancelled:
                continue
            if master and master.start:
                for key,event in tuple(group.items()):
                    if event.identity_all_day != master.all_day or (event.start is not None and event.all_day != master.all_day):
                        issues.append((uid,'Serienausnahme hat einen anderen Datumstyp als der Basistermin; Ausnahme nicht berücksichtigt.'))
                        del group[key]
                occurrences = {utc(master.start):master.start}
                if master.rule:
                    # Beginn früherer mehrtägiger Blöcke einschließen; COUNT wird
                    # im Serienmodul vor dem Suchfenster gezählt.
                    lookback = master.span.days + master.span.seconds // 86400 + 2
                    after = max(master.start.date(), datetime.fromordinal(max(1,
                        lower.astimezone(master.start.tzinfo).date().toordinal()-lookback)).date())
                    through = upper.astimezone(master.start.tzinfo).date()
                    def at(day):
                        return master.start.replace(year=day.year, month=day.month, day=day.day)
                    for day in recurrence.dates(master.start.date(), master.rule, through,
                                                after=after, valid=lambda day: valid_local(at(day)), budget=budget):
                        occurrence = at(day)
                        if master.until is None or utc(occurrence) <= utc(master.until):
                            occurrences[utc(occurrence)] = occurrence
                occurrences.update((utc(value),value) for value in master.extra)
                for identity, occurrence in occurrences.items():
                    if identity not in master.excluded and identity not in group:
                        add(master, occurrence)
            elif group:
                issues.append((uid, 'Serienausnahme ohne Basistermin; einzelner Termin berücksichtigt.'))
            for event in group.values():
                add(event, event.start)
        except (ValueError, OverflowError) as exc:
            del blocks[before:]
            issues.append((uid, str(exc)))
    return Expansion(tuple(sorted(blocks,key=lambda block:(utc(block.start),utc(block.end),block.title))),tuple(issues))
