"""Tagesnavigation, explizite Mehrfachfelder und lesende Verweisdaten."""
import copy
from datetime import date
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
import home_task_tiles as tiles
import object_references as objects
import side_view
from task_editing import batch_plan
from test_home_task_tiles import Recorder


class DayNavigationTests(unittest.TestCase):
    def test_calendar_boundaries_and_leap_day(self):
        self.assertEqual(tiles.shift_day('2028-02-28', 1), '2028-02-29')
        self.assertEqual(tiles.shift_day('2026-12-31', 1), '2027-01-01')
        self.assertEqual(tiles.shift_day('9999-12-31', 1), '9999-12-31')
        self.assertEqual(tiles.shift_day('0001-01-01', -1), '0001-01-01')

    def test_relative_titles_have_unambiguous_date(self):
        today = date(2026, 10, 27)
        self.assertEqual(tiles.day_title('2026-10-27', today), 'Heute')
        self.assertEqual(tiles.day_title('2026-10-28', today), 'Morgen · 28.10.2026')
        self.assertEqual(tiles.day_title('2026-10-26', today), 'Gestern · 26.10.2026')
        self.assertEqual(tiles.day_title('2026-11-10', today), '10.11.2026')

    def test_other_day_uses_own_due_labels_and_no_today_proposal(self):
        from dataclasses import replace
        recorder = Recorder()
        renderer = recorder.renderer()
        renderer = replace(renderer, commands=replace(renderer.commands, proposal=recorder.today))
        content = tiles.TodayContent(planned_total=0, open_total=0, planning='60 min frei', tasks=(),
            next_task=None, show_goal=False, inbox_total=0, due_lists=(), writable=True,
            is_today=False, day_title='Morgen · 28.10.2026')
        renderer.render_today(None, content)
        self.assertIn('An diesem Tag fällig', recorder.labels)
        self.assertIn('Für diesen Tag ist noch nichts eingeplant.', recorder.labels)
        self.assertIn('Für diesen Tag sind keine offenen Aufgaben fällig.', recorder.labels)
        self.assertFalse(any(title == 'Was passt heute?' for title, *_ in recorder.actions))


class BatchFieldsTests(unittest.TestCase):
    def setUp(self):
        self.items = [dict(id='a', importance=1, labels=['one']), dict(id='b', importance=3, labels=['two'])]

    def test_importance_plan_and_no_mutation(self):
        before = copy.deepcopy(self.items)
        self.assertEqual(batch_plan(self.items, 'importance', 3), {'a': {'importance': 3}})
        self.assertEqual(self.items, before)

    def test_add_preserves_different_labels_and_is_idempotent(self):
        self.assertEqual(batch_plan(self.items, 'label_add', 'one'), {'b': {'labels': ['two', 'one']}})
        self.assertEqual(batch_plan([self.items[0]], 'label_add', 'one'), {})

    def test_remove_preserves_other_labels(self):
        self.assertEqual(batch_plan(self.items, 'label_remove', 'one'), {'a': {'labels': []}})
        self.assertEqual(batch_plan(self.items, 'label_remove', 'missing'), {})

    def test_capacity_failure_is_all_or_nothing(self):
        before = copy.deepcopy(self.items)
        with self.assertRaisesRegex(ValueError, 'maximale Anzahl'):
            batch_plan(self.items, 'label_add', 'three', max_labels=1)
        self.assertEqual(self.items, before)

    def test_done_or_missing_identity_rejects_entire_selection(self):
        for invalid in (dict(id='z', done=True), dict(id=''), dict(id=False)):
            with self.assertRaises(ValueError):
                batch_plan(self.items + [invalid], 'importance', 2)

    def test_unknown_operation_and_invalid_values_fail(self):
        for operation, value in [('done', True), ('importance', True), ('importance', 4), ('label_add', ''),
                                 ('label_remove', None)]:
            with self.assertRaises(ValueError):
                batch_plan(self.items, operation, value)


class SideReferencesTests(unittest.TestCase):
    def test_only_local_links_and_visible_spans(self):
        value = objects.uri('list', 'target')
        document = dict(links={'link:a': value, 'link:external': 'https://example.com'}, spans=[
            dict(tag='link:a', start=2, end=20), dict(tag='link:external', start=0, end=3),
            dict(tag='link:a', start=True, end=3), dict(tag='link:a', start=8, end=10),
            dict(tag='bold', start=0, end=3), dict(tag='link:a', start=-1, end=2)])
        before = copy.deepcopy(document)
        self.assertEqual(side_view.page_links(document, 7), ((2, 7, value),))
        self.assertEqual(document, before)

    def test_broken_document_does_not_create_navigation(self):
        for document in (None, {}, {'links': []}, {'links': False}, {'spans': [None, 42]}):
            self.assertEqual(side_view.page_links(document, 20), ())

    def graph(self):
        target = dict(id='target', title='Ziel', list_kind='page', items=[])
        task = dict(id='task', text='Aufgabe', links=[], references=[objects.uri('list', 'target')])
        source = dict(id='source', title='Quelle', items=[task], references=[objects.uri('list', 'target'),
                                                                                  objects.uri('list', 'missing')])
        other = dict(id='other', title='Rückverweis', items=[], references=[objects.uri('list', 'source')])
        return objects.graph([source, target, other])

    def test_incoming_outgoing_and_selected_task_are_separate(self):
        index, outgoing, incoming = self.graph()
        groups = dict(side_view.reference_groups('source', 'task', index, outgoing, incoming))
        self.assertEqual(len(groups), 4)
        self.assertEqual(len(groups['Inhalt · Verweise']), 2)
        self.assertEqual(groups['Inhalt · Rückverweise'][0]['title'], 'Rückverweis')
        self.assertEqual(groups['Ausgewählte Aufgabe · Verweise'][0]['title'], 'Ziel')
        missing = next(row for row in groups['Inhalt · Verweise'] if not row['enabled'])
        self.assertEqual(missing['reason'], 'Ziel fehlt')

    def test_foreign_selected_task_is_not_exposed(self):
        self.assertEqual(len(side_view.reference_groups('target', 'task', *self.graph())), 2)

    def test_archived_is_readable_and_unsupported_is_explained(self):
        values = [dict(id='source', title='Quelle', items=[], references=[objects.uri('list', value)
                  for value in ('archived', 'drawing')]),
                  dict(id='archived', title='Archiv', items=[], archived=True),
                  dict(id='drawing', title='Bild', items=[], list_kind='drawing')]
        rows = dict(side_view.reference_groups('source', None, *objects.graph(values)))['Inhalt · Verweise']
        self.assertTrue(next(row for row in rows if 'Archiv' in row['title'])['enabled'])
        self.assertEqual(next(row for row in rows if 'Bild' in row['title'])['reason'],
                         'Nur im Hauptbereich darstellbar')


if __name__ == '__main__':
    unittest.main()
