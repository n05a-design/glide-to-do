from types import SimpleNamespace
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src' / 'glide'))

import unittest
from accessibility import Attributes
from accessibility_bindings import Binding, available


class Native:
    def __init__(self):
        self.calls, self.values = [], {}
        self.supported = self.reader = True

    def call(self, *args):
        self.calls.append(args)
        if args[0] == 'info':
            return args[-1] if self.supported else ''
        if args[0].endswith('check_screenreader'):
            return int(self.reader)
        if args[0].startswith('::tk::accessible::set_acc_'):
            self.values[args[0].split('set_acc_')[1]] = args[2]
        return ''


class Widget:
    def __init__(self):
        self.tk = Native()
        self.jobs, self.handlers, self.commands = {}, {}, {}
        self.exists = self.mapped = True
        self.sequence = 0
        self.original_key_binding = object()
        self.handlers['<Return>'] = {'original': self.original_key_binding}

    def __str__(self):
        return '.aufgabe'

    def after_idle(self, callback):
        self.sequence += 1
        identity = str(self.sequence)
        self.jobs[identity] = callback
        return identity

    def after_cancel(self, identity):
        self.jobs.pop(identity, None)

    def flush(self):
        pending = list(self.jobs.values())
        self.jobs.clear()
        for callback in pending:
            callback()

    def bind(self, event, handler, add):
        assert add == '+'
        identity = str(len(self.handlers)+1)
        self.handlers.setdefault(event, {})[identity] = handler
        return identity

    def unbind(self, event, identity):
        self.handlers[event].pop(identity)

    def register(self, command):
        self.commands['py_action'] = command
        return 'py_action'

    def deletecommand(self, command):
        del self.commands[command]

    def winfo_exists(self):
        return self.exists

    def winfo_ismapped(self):
        return self.mapped


class BindingLifecycle(unittest.TestCase):
    def test_native_backend_is_required_and_old_runtime_has_no_callbacks(self):
        widget = Widget();widget.tk.supported = False
        self.assertFalse(available(widget.tk.call))
        binding = Binding(widget, lambda: Attributes('Button', 'Einplanen'), action=lambda: None)
        self.assertFalse(binding.supported)
        self.assertFalse(widget.jobs or widget.commands)
        binding.close()
        self.assertIn('original', widget.handlers['<Return>'])

    def test_class_map_reset_is_replaced_with_current_model_after_idle(self):
        widget = Widget();current = [Attributes('Button', 'Einplanen', value='Nicht eingeplant')]
        binding = Binding(widget, lambda: current[0])
        widget.tk.values.update(name='Canvas', value='Alter Klassenwert')
        current[0] = Attributes('Button', 'Einplanen', value='Heute')
        binding.refresh();widget.flush()
        self.assertEqual(widget.tk.values['name'], 'Einplanen')
        self.assertEqual(widget.tk.values['value'], 'Heute')
        role_position = next(i for i, call in enumerate(widget.tk.calls) if call[0].endswith('set_acc_role'))
        name_position = next(i for i, call in enumerate(widget.tk.calls) if call[0].endswith('set_acc_name'))
        self.assertLess(role_position, name_position)

    def test_rapid_focus_selection_coalesce_and_keep_existing_key_bindings(self):
        widget = Widget();binding = Binding(widget, lambda: Attributes('Tree', 'Heute'))
        for _ in range(20):
            binding.refresh(selection=True);binding.refresh(focus=True)
        self.assertEqual(len(widget.jobs), 1)
        widget.flush()
        notifications = [c[0] for c in widget.tk.calls if '::tk::accessible::emit_' in c[0]]
        self.assertEqual(notifications, ['::tk::accessible::emit_focus_change'])
        self.assertIs(widget.handlers['<Return>']['original'], widget.original_key_binding)

    def test_destroy_cancels_job_removes_owned_commands_and_late_callback_is_inert(self):
        widget = Widget();binding = Binding(widget, lambda: Attributes('Button', 'Speichern'), action=lambda: True)
        late = next(iter(widget.jobs.values()))
        binding.close();binding.close();late()
        self.assertFalse(widget.jobs or widget.commands)
        self.assertFalse(any(c[0].endswith('set_acc_role') for c in widget.tk.calls))
        self.assertIs(widget.handlers['<Return>']['original'], widget.original_key_binding)

    def test_removed_or_disabled_target_never_invokes_stale_action(self):
        widget = Widget();current = [Attributes('Button', 'Öffnen')];calls = []
        binding = Binding(widget, lambda: current[0], action=lambda: calls.append('aktiviert'))
        widget.flush();self.assertEqual(widget.tk.values['action'], ('py_action',))
        binding.invoke();self.assertEqual(calls, ['aktiviert'])
        current[0] = None;binding.refresh();widget.flush();binding.invoke()
        self.assertEqual(calls, ['aktiviert'])
        self.assertEqual(widget.tk.values['name'], 'Nicht verfügbar')
        self.assertEqual(widget.tk.values['action'], ())
        current[0] = Attributes('Button', 'Öffnen', state='disabled');binding.invoke()
        self.assertEqual(calls, ['aktiviert'])

    def test_unmapped_widget_waits_and_inactive_reader_is_not_notified(self):
        widget = Widget();widget.mapped = False;widget.tk.reader = False
        binding = Binding(widget, lambda: Attributes('Entry', 'Aufgabe erfassen'))
        widget.flush()
        self.assertFalse(widget.tk.values)
        widget.mapped = True
        for handler in widget.handlers['<Map>'].values():
            handler(SimpleNamespace(widget=widget))
        binding.refresh(focus=True);widget.flush()
        self.assertEqual(widget.tk.values['name'], 'Aufgabe erfassen')
        self.assertFalse(any('::tk::accessible::emit_' in c[0] for c in widget.tk.calls))


class NativeSupportContracts(unittest.TestCase):
    def test_same_named_atk_stubs_are_rejected_and_inactive_real_backend_is_supported(self):
        for value, expected in ((0, True), ('0', True), (1, True), ('1', True),
                                ('', False), (None, False),
                                ('Warning: Tk accessibility support not available in this build.', False)):
            def native(*args):
                return args[-1] if args[0] == 'info' else value
            with self.subTest(value=value):
                self.assertEqual(available(native), expected)


class HiddenControlActions(unittest.TestCase):
    def test_retained_native_action_cannot_execute_hidden_or_removed_widget(self):
        widget = Widget(); calls = []
        binding = Binding(widget, lambda: Attributes('Button', 'Speichern'), action=lambda: calls.append('save'))
        widget.mapped = False; binding.invoke()
        self.assertEqual(calls, [])
        widget.mapped = True; binding.invoke()
        self.assertEqual(calls, ['save'])
        widget.exists = False; binding.invoke()
        self.assertEqual(calls, ['save'])


if __name__ == '__main__':
    unittest.main()
