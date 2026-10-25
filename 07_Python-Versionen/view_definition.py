"""Bedingungen und Darstellung gespeicherter Ansichten, ohne Tk (FP-03).

Der eigene oberste Einstellungsschlüssel überlebt den bisherigen Altleser.
Unverstandene Definitionen bleiben gespeichert und werden sichtbar ungültig.
"""
from collections import Counter
import copy
from datetime import date, timedelta

KEY = 'saved_view_conditions_v1'
LAYOUT_KEY = 'saved_view_layouts_v1'
COLUMNS = ('title', 'source', 'type', 'due', 'planned_date', 'estimated_minutes',
           'importance', 'labels', 'checklist', 'status')
GROUPS = ('none', 'list', 'done', 'importance', 'due', 'planned', 'label', 'eisenhower')
LAYOUT_DEFAULT = dict(display='list', group='none', sort='due', direction='asc',
                      columns=['title', 'source', 'due', 'importance', 'status'],
                      widths={}, collapsed=[], hide_empty=True, only_open=False)


def layout_errors(value):
    if not isinstance(value, dict):
        return ['Die Darstellung ist kein gültiges Objekt.']
    problems = []
    if set(value) - set(LAYOUT_DEFAULT):
        problems.append('Die Darstellung enthält unbekannte Felder.')
    for key, choices in (('display', ('list', 'table', 'columns')), ('group', GROUPS),
                         ('sort', ('manual',) + COLUMNS), ('direction', ('asc', 'desc'))):
        option = value.get(key, LAYOUT_DEFAULT[key])
        if not isinstance(option, str) or option not in choices:
            problems.append('Ungültige Darstellung: ' + key)
    columns = value.get('columns', LAYOUT_DEFAULT['columns'])
    if (not isinstance(columns, list) or not columns or len(columns) > len(COLUMNS)
            or any(not isinstance(v, str) or v not in COLUMNS for v in columns)
            or len(set(columns)) != len(columns) or 'title' not in columns):
        problems.append('Die Tabellenspalten benötigen eine eindeutige Auswahl mit Aufgabe.')
    widths = value.get('widths', {})
    if not isinstance(widths, dict) or any(
            k not in COLUMNS or type(v) is not int or not 60 <= v <= 1200 for k, v in widths.items()):
        problems.append('Ungültige Tabellenspaltenbreiten.')
    collapsed = value.get('collapsed', [])
    if not isinstance(collapsed, list) or len(collapsed) > 1000 or any(
            not isinstance(v, str) or len(v) > 160 for v in collapsed):
        problems.append('Ungültige eingeklappte Gruppen.')
    if any(type(value.get(k, LAYOUT_DEFAULT[k])) is not bool for k in ('hide_empty', 'only_open')):
        problems.append('Ungültige Darstellungsoption.')
    return problems


def layout(value):
    """Fehlende/ungültige Darstellung lesbar öffnen; Rohwert bleibt erhalten."""
    return copy.deepcopy(LAYOUT_DEFAULT if layout_errors(value) else {**LAYOUT_DEFAULT, **value})


def ordered(entries, definition, value):
    """Stabil sortieren, fehlende Werte auch absteigend zuletzt; Originale bewahren.

    Der Adapter liefert je Eintrag (Vergleichswert, fehlt). Keine Modellmutation.
    """
    result = list(entries)
    if definition['sort'] != 'manual':
        decorated = [(entry, value(entry, definition['sort'])) for entry in result]
        decorated.sort(key=lambda pair: pair[1][0], reverse=definition['direction'] == 'desc')
        decorated.sort(key=lambda pair: bool(pair[1][1]))
        result = [entry for entry, _key in decorated]
    return result


def grouped(entries, columns, keys):
    """Vorbereitete Gruppen in fester Folge; Labels dürfen Mehrfachtreffer haben."""
    buckets = {column['key']: [] for column in columns}
    for entry in entries:
        for key in dict.fromkeys(keys(entry)):
            if key in buckets:
                buckets[key].append(entry)
    return [(column, buckets[column['key']]) for column in columns]
FIELDS = {'mode', 'planned', 'start', 'end', 'effort', 'minutes',
          'blocked', 'importance_min', 'exclude_labels'}
PLANNED = {'any', 'none', 'today', 'overdue', 'this_week', 'next_week', 'range'}


def day(value):
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            parsed = date.fromisoformat(value)
            return parsed if parsed.isoformat() == value else None
        except ValueError:
            pass
    return None


def errors(value):
    if not isinstance(value, dict):
        return ['Die Ansichtsbedingungen sind kein gültiges Objekt.']
    problems = []
    if set(value) - FIELDS:
        problems.append('Die Ansicht enthält unbekannte Bedingungen.')
    for field, choices, default in (
            ('mode', {'all', 'any'}, 'all'), ('planned', PLANNED, 'any'),
            ('effort', {'any', 'none', 'at_most', 'at_least'}, 'any'),
            ('blocked', {'any', 'yes', 'no'}, 'any'),
            ('importance_min', {'all', '0', '1', '2', '3'}, 'all')):
        option = value.get(field, default)
        if not isinstance(option, str) or option not in choices:
            problems.append('Ungültige Bedingung: ' + field)
    if value.get('planned') == 'range':
        start, end = day(value.get('start')), day(value.get('end'))
        if start is None or end is None or start > end:
            problems.append('Zeitraum: gültiges Von-/Bis-Datum im Format JJJJ-MM-TT erforderlich.')
    if value.get('effort') in ('at_most', 'at_least'):
        minutes = value.get('minutes')
        if type(minutes) is not int or not 1 <= minutes <= 525600:
            problems.append('Aufwand: 1 bis 525600 Minuten erforderlich.')
    labels = value.get('exclude_labels', [])
    if not isinstance(labels, list) or len(labels) > 1000 or any(
            not isinstance(label, str) or not label or len(label) > 120 for label in labels):
        problems.append('Ungültige ausgeschlossene Labels.')
    return problems


def prune(settings, identities):
    """Nur verwaiste Ansichten löschen; unbekannte Felder bestehender bewahren."""
    result = dict(settings)
    for namespace in (KEY, LAYOUT_KEY):
        raw = result.get(namespace, {})
        result[namespace] = ({key: copy.deepcopy(value) for key, value in raw.items() if key in identities}
                             if isinstance(raw, dict) else {key: raw for key in identities})
    return result


def compact(value):
    """Neutrale Eingabefelder weglassen; nur für bereits geprüfte Definitionen."""
    result = {key: copy.deepcopy(value[key]) for key, default in (
        ('mode', 'all'), ('planned', 'any'), ('effort', 'any'),
        ('blocked', 'any'), ('importance_min', 'all'), ('exclude_labels', []))
        if key in value and value[key] != default}
    if result.get('planned') == 'range':
        result.update(start=value['start'], end=value['end'])
    if result.get('effort') in ('at_most', 'at_least'):
        result['minutes'] = value['minutes']
    return result


class Prepared:
    """Einmal geprüfte Regeln; Treffer und Erklärung verwenden dieselben Prädikate."""
    def __init__(self, value, today):
        self.problems = errors(value)
        self.rules = []
        self.any = isinstance(value, dict) and value.get('mode') == 'any'
        if self.problems:
            return

        def add(key, title, predicate, requested, actual):
            self.rules.append((key, title, predicate, requested, actual))

        def planned_text(facts, names):
            planned = day(facts.get('planned_date'))
            return planned.strftime('%d.%m.%Y') if planned else 'ohne Bearbeitungstag'

        mode = value.get('planned', 'any')
        if mode == 'none':
            add('planned', 'Bearbeitungstag', lambda f: day(f.get('planned_date')) is None,
                lambda n: 'ohne Bearbeitungstag', planned_text)
        elif mode == 'overdue':
            def overdue(f):
                planned = day(f.get('planned_date'))
                return planned is not None and planned < today and not f.get('done')
            add('planned', 'Bearbeitungstag', overdue, lambda n: 'liegen geblieben (offen vor heute)', planned_text)
        elif mode in ('today', 'this_week', 'next_week', 'range'):
            start = end = today
            if mode in ('this_week', 'next_week'):
                start = today - timedelta(days=today.weekday()) + timedelta(days=7 if mode == 'next_week' else 0)
                end = start + timedelta(days=6)
            elif mode == 'range':
                start, end = day(value['start']), day(value['end'])
            def in_window(f):
                planned = day(f.get('planned_date'))
                return planned is not None and start <= planned <= end
            requested = f'{start:%d.%m.%Y} bis {end:%d.%m.%Y}'
            add('planned', 'Bearbeitungstag', in_window, lambda n: requested, planned_text)
        effort = value.get('effort', 'any')
        if effort != 'any':
            limit = value.get('minutes')
            def effort_matches(f):
                minutes = f.get('estimated_minutes')
                estimated = type(minutes) is int and minutes > 0
                if effort == 'none':
                    return not estimated
                return estimated and (minutes <= limit if effort == 'at_most' else minutes >= limit)
            def effort_text(f, n):
                minutes = f.get('estimated_minutes')
                return f'{minutes} Minuten' if type(minutes) is int and minutes > 0 else 'ohne Schätzung'
            effort_request = ('ohne Schätzung' if effort == 'none' else
                              ('höchstens ' if effort == 'at_most' else 'mindestens ') + f'{limit} Minuten')
            add('effort', 'Aufwand', effort_matches, lambda n: effort_request, effort_text)
        blocked = value.get('blocked', 'any')
        if blocked != 'any':
            add('blocked', 'Wartet auf', lambda f: bool(f.get('blocked')) == (blocked == 'yes'),
                lambda n: 'blockiert' if blocked == 'yes' else 'frei',
                lambda f, n: 'blockiert' if f.get('blocked') else 'frei')
        minimum = value.get('importance_min', 'all')
        if minimum != 'all':
            level = int(minimum)
            add('importance_min', 'Mindestwichtigkeit', lambda f: f.get('importance', 0) >= level,
                lambda n: f'mindestens {minimum}', lambda f, n: f.get('importance', 0))
        excluded = tuple(value.get('exclude_labels', []))
        if excluded:
            excluded_set = frozenset(excluded)
            def excluded_text(f, n):
                overlap = excluded_set.intersection(f.get('labels') or ())
                return ', '.join(n.get(label, label) for label in sorted(overlap)) if overlap else 'keines der ausgeschlossenen Labels'
            add('exclude_labels', 'Labels ausschließen', lambda f: not excluded_set.intersection(f.get('labels') or ()),
                lambda n: ', '.join(n.get(label, label) for label in excluded), excluded_text)

    def matches(self, facts, legacy=()):
        if self.problems:
            return False
        if not legacy and not self.rules:
            return True
        values = (predicate(facts) for _, _, predicate, _, _ in self.rules)
        if self.any:
            return any(v['ok'] for v in legacy) or any(values)
        return all(v['ok'] for v in legacy) and all(values)

    def conditions(self, facts, names=None):
        if self.problems:
            return [dict(key='view_invalid', title='Ansicht ungültig', ok=False, detail=' '.join(self.problems))]
        names = names or {}
        return [dict(key=key, title=title, ok=bool(predicate(facts)),
                     detail=f'verlangt: {requested(names)} · Punkt: {actual(facts, names)}')
                for key, title, predicate, requested, actual in self.rules]


def conditions(value, facts, today, names=None):
    return Prepared(value, today).conditions(facts, names)


def matches(conditions, definition):
    if any(value['key'] == 'view_invalid' for value in conditions):
        return False
    if not conditions:
        return True
    return (any if definition.get('mode') == 'any' else all)(value['ok'] for value in conditions)


def hidden_reasons(groups):
    counts, titles = Counter(), {}
    for conditions in groups:
        for value in conditions:
            if not value['ok']:
                counts[value['key']] += 1
                titles[value['key']] = value['title']
                break
    return [(titles[key], count) for key, count in counts.items()]
