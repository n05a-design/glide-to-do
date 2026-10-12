"""Übliche eingebettete VTIMEZONE-Regeln ohne externe Laufzeitbibliothek.

STANDARD/DAYLIGHT mit DTSTART, jährlicher RRULE und RDATE. Unbekannte
Regeln werden abgewiesen; ein fremder Zonenname wird nie still geraten.
RFC 5545 §3.6.5: https://datatracker.ietf.org/doc/html/rfc5545#section-3.6.5
"""
from bisect import bisect_right
from dataclasses import dataclass
from datetime import datetime, date, timedelta, tzinfo
from functools import lru_cache
import re
import ics_recurrence as recurrence

ZERO = timedelta(0)


@dataclass(frozen=True)
class Observance:
    start: datetime
    before: timedelta
    after: timedelta
    daylight: bool
    name: str
    rule: object = None
    extra: tuple = ()


def offset(value):
    match=re.fullmatch(r'([+-])(\d{2})(\d{2})(\d{2})?',value)
    if not match:
        raise ValueError('Ungültiger Zeitzonenversatz.')
    sign,hour,minute,second=match.groups()
    hour,minute,second=int(hour),int(minute),int(second or 0)
    if hour>23 or minute>59 or second>59 or (sign=='-' and not any((hour,minute,second))):
        raise ValueError('Ungültiger Zeitzonenversatz.')
    return timedelta(seconds=(hour*3600+minute*60+second)*(1 if sign=='+' else -1))


def local_time(value):
    if not re.fullmatch(r'\d{8}T\d{6}',value):
        raise ValueError('Zeitzonenübergang braucht eine lokale Uhrzeit ohne Z oder TZID.')
    return datetime.strptime(value,'%Y%m%dT%H%M%S')


class CalendarZone(tzinfo):
    def __init__(self,name,observances):
        self.key=name
        self.observances=tuple(observances)
        if not name or not self.observances:
            raise ValueError('Zeitzonenkennung oder STANDARD/DAYLIGHT fehlt.')
        self.offsets=tuple(set(o.before for o in self.observances)|set(o.after for o in self.observances))

    @lru_cache(maxsize=64)
    def _timeline(self,year):
        through=date(min(9999,year+2),12,31)
        changes={}
        for obs in self.observances:
            starts={obs.start} if obs.start.date()<=through else set()
            starts.update(value for value in obs.extra if value.date()<=through)
            if obs.rule:
                for day in recurrence.dates(obs.start.date(),obs.rule,through):
                    moment=obs.start.replace(year=day.year,month=day.month,day=day.day)
                    if obs.rule.until:
                        until=datetime.strptime(obs.rule.until,'%Y%m%dT%H%M%SZ')
                        if moment-obs.before>until:
                            continue
                    starts.add(moment)
            for moment in starts:
                instant=moment-obs.before
                entry=(instant,obs.before,obs.after,obs.daylight,obs.name)
                if instant in changes and changes[instant]!=entry:
                    raise ValueError('Widersprüchliche Zeitzonenübergänge.')
                changes[instant]=entry
        entries=tuple(sorted(changes.values()))
        if not entries:
            obs=min(self.observances,key=lambda o:o.start-o.before)
            entries=((obs.start-obs.before,obs.before,obs.after,obs.daylight,obs.name),)
        for previous,current in zip(entries,entries[1:]):
            if previous[2]!=current[1]:
                raise ValueError('Zeitzonenübergänge schließen nicht aneinander an.')
        return tuple(entry[0] for entry in entries),entries

    def _at_utc(self,instant):
        moments,entries=self._timeline(instant.year)
        index=bisect_right(moments,instant)-1
        if index<0:
            first=entries[0]
            return first[1],not first[3],self.key,index,entries
        entry=entries[index]
        return entry[2],entry[3],entry[4] or self.key,index,entries

    def _local_info(self,dt):
        local=dt.replace(tzinfo=None)
        candidates=[]
        for candidate in self.offsets:
            instant=local-candidate
            info=self._at_utc(instant)
            if info[0]==candidate:
                candidates.append((instant,info))
        if candidates:
            candidates.sort(key=lambda pair:pair[0])
            return candidates[-1 if dt.fold else 0][1]
        # In einer Frühlingslücke gilt vorwärts fold=0 der bisherige Versatz;
        # Roundtrip über fromutc erkennt diese nicht existierende Uhrzeit.
        _moments,entries=self._timeline(local.year)
        for index,entry in enumerate(entries):
            instant,before,after,daylight,name=entry
            if after>before and instant+before<=local<instant+after:
                chosen=after if dt.fold else before
                phase=daylight if dt.fold else not daylight
                return chosen,phase,name or self.key,index if dt.fold else index-1,entries
        raise ValueError('Lokale Uhrzeit lässt sich keiner Zeitzonenphase zuordnen.')

    def utcoffset(self,dt):
        return None if dt is None else self._local_info(dt)[0]

    def dst(self,dt):
        if dt is None:
            return None
        chosen,daylight,_name,index,entries=self._local_info(dt)
        if not daylight:
            return ZERO
        standard=[entry[2] for entry in entries[:index+1] if not entry[3]]
        if not standard:
            standard=[entry[2] for entry in entries[index+1:] if not entry[3]]
        if not standard:
            return ZERO
        previous_standard=any(not entry[3] for entry in entries[:index+1])
        return chosen-(standard[-1] if previous_standard else standard[0])

    def tzname(self,dt):
        return self.key if dt is None else self._local_info(dt)[2]

    def fromutc(self,dt):
        if dt.tzinfo is not self:
            raise ValueError('fromutc braucht dieselbe Zeitzone.')
        instant=dt.replace(tzinfo=None)
        chosen,_daylight,_name,index,entries=self._at_utc(instant)
        fold=0
        if index>=0:
            transition,before,after,_daylight,_name=entries[index]
            fold=int(before>after and transition<=instant<transition+(before-after))
        return (instant+chosen).replace(tzinfo=self,fold=fold)


def parse_zone(properties,children):
    def single(props,name,required=True):
        found=[p for p in props if p.name==name]
        if len(found)>1 or (required and not found):
            raise ValueError('Zeitzoneneigenschaft fehlt oder ist mehrfach vorhanden: '+name)
        return found[0] if found else None
    name=single(properties,'TZID').value
    observances=[]
    for kind,props,_children in children:
        if kind not in ('STANDARD','DAYLIGHT'):
            raise ValueError('Unbekannte Zeitzonenkomponente: '+kind)
        first=single(props,'DTSTART')
        if first.params:
            raise ValueError('Zeitzonen-DTSTART muss lokal ohne Parameter vorliegen.')
        rule_prop=single(props,'RRULE',False)
        rule=recurrence.parse_rule(rule_prop.value) if rule_prop else None
        if rule and rule.frequency!='YEARLY':
            raise ValueError('Eingebettete Zeitzonen unterstützen nur jährliche Regeln.')
        if rule and rule.until and not re.fullmatch(r'\d{8}T\d{6}Z',rule.until):
            raise ValueError('Zeitzonen-UNTIL muss in UTC vorliegen.')
        extras=[]
        for prop in props:
            if prop.name=='RDATE':
                if prop.params:
                    raise ValueError('Zeitzonen-RDATE muss lokal ohne Parameter vorliegen.')
                extras.extend(local_time(value) for value in prop.value.split(','))
            if prop.name=='EXDATE':
                raise ValueError('EXDATE innerhalb VTIMEZONE wird nicht unterstützt.')
        label=single(props,'TZNAME',False)
        observances.append(Observance(local_time(first.value),offset(single(props,'TZOFFSETFROM').value),
            offset(single(props,'TZOFFSETTO').value),kind=='DAYLIGHT',label.value if label else name,rule,tuple(extras)))
    return CalendarZone(name,observances)
