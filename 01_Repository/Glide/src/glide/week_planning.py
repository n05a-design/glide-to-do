"""Wochenbilanz und freie Zeitfenster aus derselben Tagesbilanz, ohne Tk."""
from datetime import date, timedelta
import planning


def days(reference, week_start='monday'):
    first = 6 if week_start == 'sunday' else 0
    start = reference - timedelta(days=(reference.weekday() - first) % 7)
    return [start + timedelta(days=offset) for offset in range(7)]


def summarize(items, dates, settings, schedulable):
    buckets = {day.isoformat(): [] for day in dates}
    for item in items:
        if schedulable(item) and item.get('planned_date') in buckets:
            buckets[item['planned_date']].append(item)
    return {day: planning.summarize(values, planning.capacity_for(settings, day), schedulable)
            for day, values in buckets.items()}


def free_slots(items, day, duration, start=8*60, end=18*60):
    """Vorschläge ohne Buchung; Fälligkeiten und externe Termine belegen keine Zeit."""
    if type(duration) is not int or duration <= 0:
        return []
    blocks = []
    for item in items:
        clock = item.get('planned_time')
        effort = item.get('estimated_minutes')
        if item.get('planned_date') != day or not isinstance(clock, str) or type(effort) is not int or effort <= 0:
            continue
        try:
            hour, minute = map(int, clock.split(':'))
        except (ValueError, TypeError):
            continue
        if not (0 <= hour < 24 and 0 <= minute < 60):
            continue
        begin = max(start, hour*60 + minute)
        finish = min(end, hour*60 + minute + effort)
        if finish > begin:
            blocks.append((begin, finish))
    result, cursor = [], start
    for begin, finish in sorted(blocks):
        if begin - cursor >= duration:
            result.append((cursor, begin))
        cursor = max(cursor, finish)
    if end - cursor >= duration:
        result.append((cursor, end))
    return [(f'{a//60:02d}:{a%60:02d}', f'{b//60:02d}:{b%60:02d}') for a,b in result]


def calendar_buckets(entries, dates, normalize_due):
    buckets = {day.isoformat(): [] for day in dates}
    for entry, item in entries:
        for day in {item.get('planned_date'), normalize_due(item.get('due'))}:
            if day in buckets:
                buckets[day].append((entry, item))
    return buckets
