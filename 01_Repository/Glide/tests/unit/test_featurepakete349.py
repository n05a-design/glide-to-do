"""Funktionaler Ausbau der drei bestehenden D57-Pakete ohne Tk."""
import copy
from dataclasses import replace
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
import home_task_tiles as tiles
import side_view
from task_editing import batch_plan
from test_home_task_tiles import Recorder


class WeekChoicesTests(unittest.TestCase):
    def test_monday_to_sunday_and_adjacent_weeks(self):
        self.assertEqual([value for value, label in tiles.week_choices('2026-12-31')],
                         ['2026-12-28', '2026-12-29', '2026-12-30', '2026-12-31',
                          '2027-01-01', '2027-01-02', '2027-01-03'])
        self.assertEqual(tiles.week_choices('2026-12-31', 1)[0], ('2027-01-04', 'Mo · 04.01.2027'))
        self.assertEqual(tiles.week_choices('2028-02-29')[1][0], '2028-02-29')

    def test_calendar_extremes_never_overflow(self):
        self.assertEqual(tiles.week_choices('0001-01-01', -1), ())
        self.assertEqual(tiles.week_choices('9999-12-31', 1), ())
        self.assertEqual(tiles.week_choices('9999-12-31')[-1][0], '9999-12-31')

    def test_week_button_uses_explicit_existing_port(self):
        record = Recorder()
        renderer = record.renderer()
        renderer = replace(renderer, commands=replace(renderer.commands,
                            day_shift=lambda step: None, day_week=record.today))
        content = tiles.TodayContent(0, 0, '', (), None, False, 0, (), True)
        renderer.render_today(None, content)
        next(command for title, command, color in record.actions if title == 'Woche …')()
        self.assertEqual(record.calls, [('today',)])


class BatchDatesAndEffortTests(unittest.TestCase):
    def setUp(self):
        self.items = [dict(id='a', due='2026-10-28', due_time='09:30', planned_date='2026-10-27',
                           estimated_minutes=15), dict(id='b', due=None, planned_date='2026-10-27')]

    def test_due_changes_only_requested_field(self):
        before = copy.deepcopy(self.items)
        plan = batch_plan(self.items, 'due', '2026-11-01')
        self.assertEqual(plan, {'a': {'due': '2026-11-01'}, 'b': {'due': '2026-11-01'}})
        self.assertEqual(self.items, before)

    def test_clear_due_also_clears_time(self):
        self.assertEqual(batch_plan(self.items, 'due', None), {'a': {'due': None, 'due_time': None}})

    def test_due_validation(self):
        for value in ('2026-02-30', '20261028', '', 123, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                batch_plan(self.items, 'due', value)

    def test_series_rejects_entire_plan_without_mutation(self):
        self.items[1].update(repeat={'art': 'taeglich'}, due='2026-10-28')
        before = copy.deepcopy(self.items)
        with self.assertRaises(ValueError):
            batch_plan(self.items, 'due', '2026-11-01')
        self.assertEqual(before, self.items)
        self.assertEqual(batch_plan(self.items, 'due', '2026-10-28'), {})

    def test_effort_set_clear_idempotence(self):
        self.assertEqual(batch_plan(self.items, 'estimated_minutes', 15), {'b': {'estimated_minutes': 15}})
        self.assertEqual(batch_plan(self.items, 'estimated_minutes', None), {'a': {'estimated_minutes': None}})
        self.assertEqual(batch_plan(self.items, 'estimated_minutes', 60000),
                         {'a': {'estimated_minutes': 60000}, 'b': {'estimated_minutes': 60000}})

    def test_effort_limits(self):
        for value in (0, -1, 60001, True, 1.5, '30'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                batch_plan(self.items, 'estimated_minutes', value)


class ReferenceActionsTests(unittest.TestCase):
    def test_live_target_can_open_and_copy(self):
        row = dict(value='glide://list/abc', state='active', enabled=True)
        self.assertTrue(all(enabled for _, _, enabled in side_view.reference_actions(row)))

    def test_missing_and_trash_only_allow_copy(self):
        for state in ('missing', 'trash'):
            row = dict(value='glide://list/abc', state=state, enabled=False)
            self.assertEqual([key for key, _, enabled in side_view.reference_actions(row) if enabled], ['copy'])

    def test_main_only_target_and_invalid_values(self):
        row = dict(value='glide://list/abc', state='active', enabled=False)
        self.assertEqual([key for key, _, enabled in side_view.reference_actions(row) if enabled], ['main', 'copy'])
        self.assertFalse(any(enabled for _, _, enabled in side_view.reference_actions({'value': 'https://invalid.test'})))


if __name__ == '__main__':
    unittest.main()
