"""Ausgelagerte Kacheln: nur Modell/Ports, stabile IDs und bestehende Aktionen."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
from home_task_tiles import HomeTaskTiles, TaskLink, TodayContent, FocusContent, TileUI, TileCommands
from render_retention import snapshot


class Recorder:
    def __init__(self):
        self.labels, self.actions, self.rows, self.calls, self.goals = [], [], [], [], []

    def card(self, parent, title):
        return title

    def label(self, parent, text, *args, **options):
        self.labels.append(text)

    def action(self, parent, text, command, color, **options):
        self.actions.append((text, command, color))

    def flow(self, parent, **options):
        return parent

    def goal(self, parent):
        self.goals.append(parent)

    def task_row(self, parent, task, open_command, complete_command):
        self.rows.append((task, open_command, complete_command))

    def open_task(self, list_id, item_id):
        self.calls.append(('open', list_id, item_id))

    def complete(self, item_id):
        self.calls.append(('complete', item_id))

    def open_list(self, list_id):
        self.calls.append(('list', list_id))

    def today(self):
        self.calls.append(('today',))

    def upcoming(self):
        self.calls.append(('upcoming',))

    def next_task(self):
        self.calls.append(('next',))

    def renderer(self):
        return HomeTaskTiles(TileUI(self.card, self.label, self.action, self.flow, self.goal, self.task_row),
                             TileCommands(self.open_task, self.complete, self.open_list, self.today,
                                          self.upcoming, self.next_task),
                             dict(today='Heute', next='Weiter', check='Haken', in_progress='Später'), tuple(range(20)))


class HomeTaskTilesTests(unittest.TestCase):
    def test_optional_day_controls_use_existing_ports(self):
        from dataclasses import replace
        record = Recorder()
        renderer = record.renderer()
        renderer = replace(renderer, commands=replace(renderer.commands, focus=record.complete,
                            plan=record.open_list, proposal=record.today))
        renderer.render_focus(None, FocusContent(TaskLink('Aufgabe', 'l', 'x', 'accent')))
        next(command for title, command, color in record.actions if title == 'Fokus starten')()
        next(command for title, command, color in record.actions if title == 'Einplanen …')()
        self.assertEqual(record.calls, [('complete', 'x'), ('list', 'x')])
        record.actions.clear()
        renderer.render_today(None, self.content())
        next(command for title, command, color in record.actions if title == 'Was passt heute?')()
        self.assertEqual(record.calls[-1], ('today',))

    def content(self, **changes):
        options = dict(planned_total=8, open_total=2, planning='30 min geplant',
                       tasks=(TaskLink('Erste', 'l1', 'a', 'accent'), TaskLink('Zweite', 'l2', 'b', 'confirm')),
                       next_task=None, show_goal=False, inbox_total=3,
                       due_lists=(('Quelle · 2 offen', 'due-list', 'accent'),), writable=True)
        options.update(changes)
        return TodayContent(**options)

    def test_today_keeps_planning_and_due_separate_and_binds_each_id(self):
        record = Recorder()
        record.renderer().render_today('parent', self.content())
        self.assertIn('8 eingeplant · 2 offen\n30 min geplant', record.labels)
        self.assertIn('Heute fällig', record.labels)
        self.assertEqual(len(record.rows), 2)
        for task, open_command, complete_command in record.rows:
            open_command()
            complete_command()
        self.assertEqual(record.calls, [('open', 'l1', 'a'), ('complete', 'a'),
                                        ('open', 'l2', 'b'), ('complete', 'b')])
        for text, command, color in record.actions:
            command()
        self.assertEqual(record.calls[-2:], [('list', 'due-list'), ('today',)])

    def test_read_only_rows_keep_open_but_no_mutation(self):
        record = Recorder()
        record.renderer().render_today(None, self.content(writable=False))
        self.assertTrue(all(row[2] is None for row in record.rows))
        self.assertIn('Schreibgeschützt · Aufgaben lassen sich öffnen.', record.labels)
        record.rows[0][1]()
        self.assertEqual(record.calls, [('open', 'l1', 'a')])

    def test_empty_planning_and_due_keep_their_own_messages(self):
        record = Recorder()
        record.renderer().render_today(None, self.content(planned_total=0, open_total=0, tasks=(), due_lists=()))
        self.assertIn('Für heute ist noch nichts eingeplant.', record.labels)
        self.assertIn('Für heute sind keine offenen Aufgaben fällig.', record.labels)
        self.assertEqual(record.rows, [])

    def test_goal_and_next_only_when_requested(self):
        record = Recorder()
        task = TaskLink('Als Nächstes', 'l', 'next', 'accent')
        record.renderer().render_today(None, self.content(next_task=task, show_goal=True))
        self.assertEqual(len(record.goals), 1)
        next(command for text, command, color in record.actions if text == task.title)()
        self.assertEqual(record.calls, [('open', 'l', 'next')])

    def test_focus_and_empty_focus_keep_all_existing_actions(self):
        record = Recorder()
        task = TaskLink('Aufgabe', 'l', 'x', 'accent')
        record.renderer().render_focus(None, FocusContent(task, 'Fällig morgen · Quelle'))
        for text, command, color in record.actions:
            command()
        self.assertEqual(record.calls, [('open', 'l', 'x'), ('complete', 'x'), ('next',)])
        record = Recorder()
        record.renderer().render_focus(None, FocusContent(None))
        record.actions[0][1]()
        self.assertEqual(record.calls, [('upcoming',)])

    def test_focus_read_only_and_recreated_renderer_keep_stable_commands(self):
        record = Recorder()
        content = FocusContent(TaskLink('Aufgabe', 'l', 'x', 'accent'), writable=False)
        record.renderer().render_focus(None, content)
        commands = [snapshot(action[1]) for action in record.actions]
        self.assertEqual(len(commands), 2)
        record.actions.clear()
        record.renderer().render_focus(None, content)
        self.assertEqual(commands, [snapshot(action[1]) for action in record.actions])


if __name__ == '__main__':
    unittest.main()
