import copy
from datetime import date
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
import view_definition as views


class ViewDefinitionTests(unittest.TestCase):
    today = date(2026, 10, 21)

    def check(self, definition, facts):
        conditions = views.conditions(definition, facts, self.today)
        return views.matches(conditions, definition)

    def test_planned_windows_and_week_boundaries(self):
        cases = {'today': ['2026-10-21'], 'this_week': ['2026-10-19', '2026-10-25'],
                 'next_week': ['2026-10-26', '2026-11-01'], 'overdue': ['2026-10-18']}
        for mode, days in cases.items():
            for day in days:
                with self.subTest(mode=mode, day=day):
                    self.assertTrue(self.check({'planned': mode}, {'planned_date': day}))
            self.assertFalse(self.check({'planned': mode}, {'planned_date': '2026-11-02'}))
        self.assertFalse(self.check({'planned': 'overdue'}, {'planned_date': '2026-10-20', 'done': True}))
        self.assertTrue(self.check({'planned': 'none'}, {}))
        self.assertFalse(self.check({'planned': 'none'}, {'planned_date': '2026-10-21'}))

    def test_range_inclusive_leap_day_and_invalid_ranges(self):
        definition = {'planned': 'range', 'start': '2024-02-28', 'end': '2024-03-01'}
        self.assertTrue(self.check(definition, {'planned_date': '2024-02-29'}))
        self.assertTrue(self.check(definition, {'planned_date': '2024-03-01'}))
        self.assertFalse(self.check(definition, {'planned_date': '2024-03-02'}))
        for start, end in [('2024-03-02', '2024-03-01'), ('2023-02-29', '2024-03-01'), ('20240228', '2024-03-01')]:
            self.assertTrue(views.errors(dict(definition, start=start, end=end)))

    def test_effort_unknown_and_exact_boundaries(self):
        for unknown in (None, 0, False, '30'):
            self.assertTrue(self.check({'effort': 'none'}, {'estimated_minutes': unknown}))
            self.assertFalse(self.check({'effort': 'at_most', 'minutes': 30}, {'estimated_minutes': unknown}))
        for mode in ('at_most', 'at_least'):
            self.assertTrue(self.check({'effort': mode, 'minutes': 30}, {'estimated_minutes': 30}))
        self.assertFalse(self.check({'effort': 'at_most', 'minutes': 30}, {'estimated_minutes': 31}))
        self.assertFalse(self.check({'effort': 'at_least', 'minutes': 30}, {'estimated_minutes': 29}))
        for bad in (True, 0, -1, '30', 525601):
            self.assertTrue(views.errors({'effort': 'at_most', 'minutes': bad}))

    def test_blocked_importance_and_excluded_labels(self):
        definition = {'blocked': 'no', 'importance_min': '2', 'exclude_labels': ['wait']}
        facts = {'blocked': False, 'importance': 2, 'labels': ['client']}
        self.assertTrue(self.check(definition, facts))
        for key, value in [('blocked', True), ('importance', 1), ('labels', ['wait'])]:
            self.assertFalse(self.check(definition, dict(facts, **{key: value})))
        explained = views.conditions(definition, dict(facts, labels=['wait']), self.today, {'wait': 'Warten'})
        self.assertIn('Warten', explained[-1]['detail'])

    def test_any_combines_legacy_conditions_but_never_accepts_invalid(self):
        legacy = [dict(key='status', title='Status', ok=True, detail='offen')]
        definition = {'mode': 'any', 'effort': 'none'}
        extra = views.conditions(definition, {'estimated_minutes': 30}, self.today)
        self.assertTrue(views.matches(legacy + extra, definition))
        self.assertFalse(views.matches(legacy + extra, dict(definition, mode='all')))
        for invalid in ({'mode': 'any', 'future': 1}, {'mode': []}, None, [], {'exclude_labels': [7]}):
            bad = views.conditions(invalid, {}, self.today)
            self.assertFalse(views.matches(legacy + bad, invalid))
        self.assertTrue(views.matches([], {}))

    def test_prune_retains_future_definition_without_mutation(self):
        data = {views.KEY: {'keep': {'future': ['x']}, 'deleted': {'planned': 'today'}}, 'other': 7}
        before = copy.deepcopy(data)
        result = views.prune(data, {'keep'})
        self.assertEqual(result[views.KEY], {'keep': {'future': ['x']}})
        self.assertEqual(data, before)
        result[views.KEY]['keep']['future'].append('y')
        self.assertEqual(data, before)
        self.assertTrue(views.errors(views.prune({views.KEY: 'broken'}, {'keep'})[views.KEY]['keep']))

    def test_explanation_and_hidden_reasons_use_same_conditions(self):
        definition = {'planned': 'today', 'effort': 'none'}
        conditions = views.conditions(definition, {'planned_date': '2026-10-20', 'estimated_minutes': 30}, self.today)
        self.assertEqual(views.hidden_reasons([conditions]), [('Bearbeitungstag', 1)])
        self.assertEqual([c['key'] for c in conditions], ['planned', 'effort'])
        self.assertTrue(all(c['detail'].startswith('verlangt:') for c in conditions))

    def test_prepared_matching_agrees_with_explanation(self):
        for mode in ('all', 'any'):
            definition = dict(mode=mode, planned='today', effort='at_most', minutes=30,
                              blocked='no', importance_min='2', exclude_labels=['wait'])
            prepared = views.Prepared(definition, self.today)
            for planned in (None, '2026-10-21', '2026-10-20'):
                for minutes in (None, 20, 60):
                    for blocked in (False, True):
                        facts = dict(planned_date=planned, estimated_minutes=minutes, blocked=blocked,
                                     importance=3, labels=['wait'] if blocked else [])
                        for legacy in ([], [dict(key='status', ok=False)], [dict(key='status', ok=True)]):
                            explained = legacy + prepared.conditions(facts)
                            self.assertEqual(prepared.matches(facts, legacy), views.matches(explained, definition))

    def test_compact_preserves_semantics_and_omits_neutral_fields(self):
        value = dict(mode='all', planned='any', start='', end='', effort='any', minutes=30,
                     blocked='any', importance_min='all', exclude_labels=[])
        self.assertEqual(views.compact(value), {})
        value.update(planned='range', start='2026-10-01', end='2026-10-21', effort='at_most')
        result = views.compact(value)
        self.assertEqual(result, dict(planned='range', start='2026-10-01', end='2026-10-21', effort='at_most', minutes=30))
        self.assertIn('mode', views.compact(dict(value, mode='any')))


class LayoutTests(unittest.TestCase):
    def test_layout_defaults_are_independent_and_unknown_fields_stay_visible(self):
        first = views.layout({})
        first['columns'].append('type')
        self.assertNotIn('type', views.layout({})['columns'])
        unknown = {'display': 'future', 'future_option': 3}
        self.assertTrue(views.layout_errors(unknown))
        self.assertEqual(views.layout(unknown)['display'], 'list')
        self.assertEqual(unknown, {'display': 'future', 'future_option': 3})

    def test_layout_validation_and_pruning(self):
        for bad in ({'columns': ['source']}, {'columns': ['title', 'title']},
                    {'columns': ['title', {}]}, {'widths': {'title': True}},
                    {'widths': {'title': 59}}, {'group': []}, {'sort': 'future'},
                    {'only_open': 1}, {'collapsed': [3]}, None):
            self.assertTrue(views.layout_errors(bad), bad)
        self.assertFalse(views.layout_errors({'display': 'columns', 'group': 'list',
                                            'columns': ['title', 'source'], 'widths': {'title': 600}}))
        settings = {views.KEY: {'a': {}}, views.LAYOUT_KEY: {'a': {'future': 7}, 'removed': {}}}
        result = views.prune(settings, {'a'})
        self.assertEqual(result[views.LAYOUT_KEY], {'a': {'future': 7}})
        self.assertIn('removed', settings[views.LAYOUT_KEY])

    def test_ordering_keeps_originals_ties_and_missing_values_last(self):
        rows = [{'value': 2}, {'value': None}, {'value': 1}, {'value': 2}]
        value = lambda row, key: (row['value'] or 0, row['value'] is None)
        desc = views.ordered(rows, dict(sort='importance', direction='desc'), value)
        self.assertEqual(desc, [rows[0], rows[3], rows[2], rows[1]])
        self.assertIs(desc[0], rows[0])
        self.assertEqual(views.ordered(rows, dict(sort='manual'), value), rows)

    def test_groups_allow_multiple_labels_without_duplicate_keys(self):
        first, second = {'labels': ['a', 'b', 'a']}, {'labels': ['b']}
        columns = [{'key': 'b'}, {'key': 'a'}, {'key': 'empty'}]
        result = views.grouped([first, second], columns, lambda row: row['labels'])
        self.assertEqual(result, [(columns[0], [first, second]), (columns[1], [first]), (columns[2], [])])
        self.assertIs(result[0][1][0], first)


if __name__ == '__main__':
    unittest.main()


