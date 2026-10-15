"""Reader-Diagnose vor dem ersten Inspektor und bei späteren Fehlern, ohne Tk."""
from types import SimpleNamespace
import unittest
from reader_app400 import diagnostic_state


class ReaderAppState(unittest.TestCase):
    def test_initial_empty_list_does_not_require_an_inspector_host(self):
        app = SimpleNamespace(view_mode='list', lists=[{'items':[]}], walk_items=iter)
        self.assertEqual(diagnostic_state(app, 123, []), dict(pid=123,view='list',tasks=[],
                                                            inspector=None,callback_errors=[]))

    def test_current_tasks_inspector_and_errors_are_reported_without_mutation(self):
        tasks = [{'id':'t', 'text':'Künstliche Aufgabe'}]
        app = SimpleNamespace(view_mode='planday', lists=[{'items':tasks}],walk_items=iter,
                              _detail_state={'item_id':'t'})
        errors = ['künstlicher Callbackfehler']
        result = diagnostic_state(app, 123, errors)
        self.assertEqual(result['tasks'], tasks)
        self.assertEqual(result['inspector'], 't')
        errors.append('später')
        self.assertEqual(result['callback_errors'], ['künstlicher Callbackfehler'])
        self.assertEqual(tasks, [{'id':'t', 'text':'Künstliche Aufgabe'}])


if __name__ == '__main__':
    unittest.main()
