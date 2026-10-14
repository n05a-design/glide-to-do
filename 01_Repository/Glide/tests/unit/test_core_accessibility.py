import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src' / 'glide'))

import unittest
from types import SimpleNamespace
from core_accessibility import control_name, button_attributes, entry_attributes, selected_task_attributes
import core_accessibility as core
import test_accessibility_bindings as fixtures


class Control:
    def __init__(self, value='', state='normal'):
        self.value, self.state, self.text = value, state, value
    def cget(self, name):
        assert name == 'state'
        return self.state
    def get(self, *args):
        return self.value


class CoreValues(unittest.TestCase):
    def test_compact_actions_have_words_and_text_does_not_lose_umlauts(self):
        self.assertEqual(control_name('+'), 'Hinzufügen')
        self.assertEqual(control_name('×'), 'Entfernen')
        self.assertEqual(control_name('✓ Erledigt'), 'Erledigt')
        self.assertEqual(control_name('  Änderungen speichern … '), 'Änderungen speichern')
        self.assertEqual(control_name('…'), 'Weitere Aktionen')

    def test_button_uses_current_name_command_state_and_explicit_symbol_meaning(self):
        button = Control('+')
        button._accessible_name = 'Aufgabe hinzufügen'
        self.assertEqual(button_attributes(button).name, 'Aufgabe hinzufügen')
        button.state = 'disabled'
        self.assertEqual(button_attributes(button).state, 'disabled')

    def test_symbol_button_uses_current_tooltip_and_preserves_explicit_name(self):
        button = Control('⚑')
        caption = ['Heute öffnen']
        button._glide_tooltip = {'source': lambda: caption[0]}
        self.assertEqual(button_attributes(button).name, 'Heute öffnen')
        caption[0] = 'Morgen öffnen'
        self.assertEqual(button_attributes(button).name, 'Morgen öffnen')
        button._accessible_name = 'Auswahl einplanen'
        self.assertEqual(button_attributes(button).name, 'Auswahl einplanen')

    def test_fields_read_current_text_and_preserve_readonly_state(self):
        field = Control('Eins\nZwei', 'readonly')
        result = entry_attributes(field, 'Beschreibung', text=True)
        self.assertEqual((result.role, result.value, result.state), ('Text', 'Eins\nZwei', 'readonly'))
        field.value = 'Neu'
        self.assertEqual(entry_attributes(field, 'Beschreibung', text=True).value, 'Neu')

    def test_editable_values_preserve_line_breaks_spaces_and_unicode_positions(self):
        for text, value in ((False, '  Angebot  prüfen 🏠'), (True, 'Erste Zeile\n\n  Zweite\tZeile 🏠')):
            field = Control(value)
            result = entry_attributes(field, 'Aufgabentext', text=text)
            self.assertEqual(result.value, value)
            self.assertEqual(len(result.value), len(value))
            self.assertEqual(field.value, value)

    def app(self):
        self.items = {'t': {'id': 't', 'text': 'Anrufen', 'planned_date': '2026-10-13',
                            'due': '2026-10-14', 'blocked_by': ['b', 'missing'], 'labels': ['l']},
                      'b': {'id': 'b', 'text': 'Antwort erhalten'}}
        self.selected = ['t']
        return SimpleNamespace(get_selected_item_id=lambda:self.selected[0] if self.selected else None,
            get_selected_item_ids=lambda:list(self.selected),
            find_item_in_lists=lambda key:(self.items[key],) if key in self.items else None,
            item_labels=lambda item:[{'name':'Privat'}], view_mode='planday', PLAN_DAY_VIEW='planday')

    def test_task_distinguishes_planning_due_and_named_relations_without_ids(self):
        app = self.app();result = selected_task_attributes(app)
        self.assertEqual(result.name, 'Mein Tag: Aufgaben')
        for value in ('Bearbeitungstag 13.10.2026', 'Fällig 14.10.2026', 'Wartet auf Antwort erhalten', 'Labels Privat'):
            self.assertIn(value, result.value)
        self.assertNotIn('missing', result.value)

    def test_undo_object_replacement_and_completed_blocker_are_resolved_fresh(self):
        app = self.app();first = selected_task_attributes(app)
        self.items['t'] = {'id':'t','text':'Ersetzt','done':True}
        self.items['b']['done'] = True
        result = selected_task_attributes(app)
        self.assertNotEqual(first.value, result.value)
        self.assertIn('Ersetzt. Erledigt.', result.value)
        self.assertNotIn('Antwort erhalten', result.value)

    def test_removed_selection_multiple_selection_and_readonly_remain_explainable(self):
        app = self.app();self.selected.append('b')
        self.assertIn('2 Aufgaben ausgewählt.', selected_task_attributes(app).value)
        app._data_read_only = True
        self.assertEqual(selected_task_attributes(app).description, 'Schreibgeschützter Bestand.')
        self.items.pop('t')
        self.assertEqual(selected_task_attributes(app).value, 'Keine Aufgabe ausgewählt.')
        self.selected.clear()
        self.assertEqual(selected_task_attributes(app).state, 'normal')

    def test_placeholder_is_not_announced_as_entered_content(self):
        field = Control('Aufgabe eingeben')
        self.assertEqual(entry_attributes(field, 'Neue Aufgabe', placeholder=lambda:True).value, '')
        self.assertEqual(entry_attributes(field, 'Neue Aufgabe', placeholder=lambda:False).value, 'Aufgabe eingeben')


class CoreBindingContracts(unittest.TestCase):
    def test_inspector_readonly_predicate_controls_choice_and_label_semantics(self):
        readonly = [False]
        field = Control('Wichtigkeit')
        field.variable = SimpleNamespace(get=lambda: 'Normal')
        field._inspector_readonly = lambda: readonly[0]
        dropdown = SimpleNamespace(labels=[], selected_ids=[], summary_label=Control(),
                                   _inspector_readonly=field._inspector_readonly)
        self.assertEqual(core.choice_attributes(field).state, 'normal')
        self.assertEqual(core.label_selection_attributes(dropdown).state, 'normal')
        readonly[0] = True
        self.assertTrue(core.choice_disabled(field))
        self.assertEqual(core.choice_attributes(field).state, 'disabled')
        self.assertEqual(core.label_selection_attributes(dropdown, popup=True).state, 'disabled')

    def widget(self, root=None):
        widget = fixtures.Widget()
        widget._root = lambda: root or widget
        return widget

    def test_attachment_is_named_from_current_fields_and_keyboard_respects_inspector_target(self):
        widget=self.widget();widget.configure=lambda **options:None
        calls=[]
        app=SimpleNamespace(_detail_state={'item_id':'t','fields':{'attachments':[{'name':'Angebot.pdf'}]}},
            find_item_in_lists=lambda identity:({'id':identity},),
            open_detail_pane_attachment=lambda index:calls.append(index),_data_read_only=True)
        binding=core.bind_attachment(widget,app,'t',0)
        keyboard=next(value for key,value in widget.handlers['<Return>'].items() if key!='original')
        self.assertEqual(binding.attributes().name,'Anhang öffnen: Angebot.pdf')
        keyboard(None);self.assertEqual(calls,[0])  # Read-only still permits reading attachments.
        app._detail_state['fields']['attachments'][0]={'name':'Neue Fassung.pdf'}
        self.assertEqual(binding.attributes().name,'Anhang öffnen: Neue Fassung.pdf')
        app._detail_state['item_id']='other'
        keyboard(None);binding.invoke();self.assertEqual(calls,[0])
        app._detail_state['item_id']='t';app._detail_state['fields']['attachments'].clear()
        self.assertIsNone(binding.attributes())
        keyboard(None);self.assertEqual(calls,[0])

    def test_attachment_keyboard_works_without_native_backend_and_refuses_removed_item(self):
        widget=self.widget();widget.tk.supported=False;widget.configure=lambda **options:None
        exists=[True];calls=[]
        app=SimpleNamespace(_detail_state={'item_id':'t','fields':{'attachments':[{'name':'Datei'}]}},
            find_item_in_lists=lambda identity:({},) if exists[0] else None,
            open_detail_pane_attachment=lambda index:calls.append(index))
        binding=core.bind_attachment(widget,app,'t',0)
        keyboard=next(value for key,value in widget.handlers['<space>'].items() if key!='original')
        keyboard(None);self.assertEqual(calls,[0])
        exists[0]=False;keyboard(None);self.assertEqual(calls,[0])
        self.assertFalse(binding.supported)

    def test_native_weekday_checkbox_reads_current_variable_and_disabled_state(self):
        widget=self.widget();state=['normal'];value=[False];calls=[]
        widget.cget=lambda name:state[0]
        widget.invoke=lambda:calls.append('toggle')
        variable=SimpleNamespace(get=lambda:value[0])
        binding=core.bind_checkbox(widget,variable,'Wiederholung: Montag')
        self.assertEqual(binding.attributes().value,'0')
        value[0]=True
        self.assertEqual((binding.attributes().name,binding.attributes().value),('Wiederholung: Montag','1'))
        binding.invoke();self.assertEqual(calls,['toggle'])
        state[0]='disabled';binding.invoke();self.assertEqual(calls,['toggle'])

    def test_readonly_inspector_button_reports_disabled_even_with_noop_callback(self):
        widget=Control('Entfernen');widget.command=lambda:'break'
        widget._accessible_disabled=True
        self.assertEqual(core.button_attributes(widget).state,'disabled')

    def test_rebinding_replaces_action_and_never_duplicates_callbacks(self):
        widget = self.widget();calls=[]
        binding = core.bind_control(widget, lambda:core.Attributes('Button','Alt'), action=lambda:calls.append('alt'))
        original=dict(widget.handlers)
        self.assertIs(core.bind_control(widget, lambda:core.Attributes('Button','Neu'), action=lambda:calls.append('neu')),binding)
        widget.flush();binding.invoke()
        self.assertEqual(calls,['neu'])
        self.assertEqual(widget.tk.values['name'],'Neu')
        self.assertEqual(widget.handlers,original)
        self.assertEqual(len(widget.commands),1)
        core.bind_control(widget, lambda:core.Attributes('Label','Jetzt lesend'))
        widget.flush();binding.invoke()
        self.assertEqual(widget.tk.values['action'],())
        self.assertEqual(calls,['neu'])

    def test_backend_detection_is_per_interpreter_and_old_backend_remains_inert(self):
        root = self.widget();root.tk.supported = False
        first = core.bind_control(root, lambda:core.Attributes('Button','Erfassen'), action=lambda:None)
        inquiries = len([call for call in root.tk.calls if call[0]=='info'])
        self.assertGreater(inquiries,0)
        second = self.widget(root);second.tk=root.tk
        core.bind_control(second, lambda:core.Attributes('Entry','Suchen'))
        self.assertEqual(len([call for call in root.tk.calls if call[0]=='info']),inquiries)
        self.assertFalse(first.supported or root.jobs or second.jobs or root.commands)
        native = self.widget();binding = core.bind_control(native, lambda:core.Attributes('Button','Erfassen'))
        self.assertTrue(binding.supported)

    def test_entry_keys_keep_existing_activation_and_close_owned_registration(self):
        widget=self.widget();widget.get=lambda *a:'Aufgabe';widget.cget=lambda name:'normal'
        binding=core.bind_entry(widget,'Neue Aufgabe')
        again=core.bind_entry(widget,'Aufgabentitel')
        self.assertIs(again,binding)
        self.assertEqual(len(widget.handlers['<KeyRelease>']),1)
        widget.flush();self.assertEqual(widget.tk.values['name'],'Aufgabentitel')
        binding.close()
        self.assertFalse(widget.handlers['<KeyRelease>'])
        self.assertIs(widget.handlers['<Return>']['original'],widget.original_key_binding)

    def test_label_values_follow_full_selection_and_current_keyboard_target(self):
        dropdown=SimpleNamespace(labels=[{'id':'a','name':'Arbeit'},{'id':'b','name':'Privat'}],selected_ids=['b'],_focus_index=0)
        self.assertEqual(core.label_selection_attributes(dropdown).value,'Privat')
        self.assertEqual(core.label_selection_attributes(dropdown,popup=True).value,'Arbeit. Nicht ausgewählt.')
        dropdown._focus_index=1
        self.assertEqual(core.label_selection_attributes(dropdown,popup=True).value,'Privat. Ausgewählt.')
        dropdown.labels=[]
        self.assertEqual(core.label_selection_attributes(dropdown,popup=True).value,'Keine Labels vorhanden.')

    def test_checklist_current_target_and_readonly_state_do_not_use_removed_steps(self):
        item={'checklist':[{'text':'Anlage prüfen','done':False}]}
        app=SimpleNamespace(find_item_in_lists=lambda identity:(item,))
        result=core.checklist_attributes(app,'t',0)
        self.assertEqual((result.role,result.name,result.value,result.description),
                         ('Checkbutton','Anlage prüfen','0','Offen'))
        item['checklist'][0]={'text':'Anlage neu prüfen','done':True};app._data_read_only=True
        result=core.checklist_attributes(app,'t',0)
        self.assertEqual((result.name,result.value,result.state,result.description),
                         ('Anlage neu prüfen','1','disabled','Erledigt'))
        item['checklist'].clear()
        self.assertIsNone(core.checklist_attributes(app,'t',0))

    def test_checklist_keyboard_and_native_actions_respect_removed_or_readonly_target(self):
        widget=self.widget();widget.configure=lambda **kw:None
        item={'checklist':[{'text':'Prüfen'}]};calls=[]
        app=SimpleNamespace(find_item_in_lists=lambda identity:(item,),
            toggle_detail_pane_step=lambda *args:calls.append(args),_detail_state={},
            _data_read_only=True)
        binding=core.bind_checklist(widget,app,'t',0)
        keyboard=next(v for k,v in widget.handlers['<Return>'].items()if k!='original')
        keyboard(None);binding.invoke()
        self.assertEqual(calls,[])
        app._data_read_only=False
        keyboard(None);self.assertEqual(calls,[('t',0)])
        item['checklist'].clear()
        keyboard(None);binding.invoke()
        self.assertEqual(calls,[('t',0)])


class ChecklistVariableContracts(unittest.TestCase):
    def setUp(self):
        self.widget = fixtures.Widget()
        self.widget._root = lambda: self.widget
        self.options = {}
        self.widget.configure = lambda **options: self.options.update(options)
        self.variable = SimpleNamespace(value=False)
        self.variable.get = lambda: self.variable.value
        self.variable.set = lambda value: setattr(self.variable, 'value', value)
        self.widget._accessible_variable = self.variable
        self.item = {'checklist': [{'text': 'Unterlagen prüfen', 'done': False}]}
        self.calls = []
        self.app = SimpleNamespace(find_item_in_lists=lambda identity: (self.item,),
            _detail_state={}, toggle_detail_pane_step=lambda *args: self.calls.append(args))
        self.binding = core.bind_checklist(self.widget, self.app, 't', 0)

    def test_mouse_toggle_is_reverted_when_write_fails_or_readonly_changes(self):
        self.variable.value = True  # Tk toggles before invoking the command.
        self.options['command']()
        self.assertEqual(self.calls, [('t', 0)])
        self.assertFalse(self.variable.value)
        self.app._data_read_only = True
        self.variable.value = True
        self.options['command']()
        self.assertEqual(self.calls, [('t', 0)])
        self.assertFalse(self.variable.value)

    def test_native_action_does_not_pretoggle_and_resolves_replaced_item(self):
        def toggle(*args):
            self.assertFalse(self.variable.value)
            self.item = {'checklist': [{'text': 'Neu', 'done': True}]}
        self.app.toggle_detail_pane_step = toggle
        self.binding.invoke()
        self.assertTrue(self.variable.value)
        self.assertEqual(self.binding.attributes().name, 'Neu')

    def test_destroyed_old_widget_during_render_is_not_touched(self):
        def toggle(*args):
            self.item['checklist'][0]['done'] = True
            self.widget.exists = False
        self.app.toggle_detail_pane_step = toggle
        self.variable.set = lambda value: self.fail('Destroyed old widget must not be updated')
        self.binding.invoke()
        self.assertTrue(self.item['checklist'][0]['done'])

    def test_focused_checkbox_resyncs_after_undo_replaces_model(self):
        self.variable.value = True
        self.item = {'checklist': [{'text': 'Unterlagen prüfen', 'done': False}]}
        self.app.detail_pane = object()
        self.app.iter_descendants = lambda _pane: [self.widget]
        core.refresh_inspector(self.app)
        self.assertFalse(self.variable.value)
        self.widget.flush()
        self.assertEqual(self.widget.tk.values['value'], '0')

    def test_retained_action_refuses_replaced_step_at_same_index(self):
        self.item['checklist'][0]['id'] = 'original-step'
        binding = core.bind_checklist(self.widget, self.app, 't', 0)
        self.item['checklist'][0] = {'id': 'other-step', 'text': 'Andere Aufgabe', 'done': False}
        binding.invoke()
        self.assertEqual(self.calls, [])
        self.assertIsNone(binding.attributes())

    def test_inspector_keeps_focus_only_while_checklist_structure_matches(self):
        app = SimpleNamespace(_detail_state={'baseline': {'checklist': [{'id': 'a', 'done': True}]}})
        self.assertTrue(core.inspector_structure_matches(app, {'checklist': [{'id': 'a', 'done': False}]}))
        self.assertFalse(core.inspector_structure_matches(app, {'checklist': []}))
        self.assertFalse(core.inspector_structure_matches(app, {'checklist': [{'id': 'b'}]}))


class NavigationAndCompletionContracts(unittest.TestCase):
    def test_navigation_reads_visible_title_instead_of_icon_count_or_id(self):
        rows = {'today-id': 'Heute (3)', 'work-id': 'Arbeit'}
        selected = ['today-id']
        def item(identity, column):
            self.assertEqual(column, 'text')
            return rows[identity]
        tree = SimpleNamespace(selection=lambda: selected, focus=lambda: 'today-id',
                               exists=lambda identity: identity in rows, item=item)
        result = core.navigation_attributes(tree, 'Arbeitsbereiche')
        self.assertEqual((result.name, result.value), ('Arbeitsbereiche: Heute (3)', 'Heute (3)'))
        self.assertNotIn('today-id', result.name + result.value)
        rows['today-id'] = 'Heute (4)'
        self.assertEqual(core.navigation_attributes(tree, 'Arbeitsbereiche').value, 'Heute (4)')

    def test_navigation_handles_removed_focus_and_empty_selection(self):
        selected = ['gone-id', 'work-id']
        tree = SimpleNamespace(selection=lambda: selected, focus=lambda: 'gone-id',
            exists=lambda identity: identity == 'work-id', item=lambda identity, column: 'Arbeit')
        self.assertEqual(core.navigation_attributes(tree, 'Listen').name, 'Listen: Arbeit')
        selected.clear()
        self.assertEqual(core.navigation_attributes(tree, 'Listen').value, 'Keine Auswahl.')

    def test_completion_action_resolves_current_object_name_state_and_readonly(self):
        items = {'t': {'text': 'Angebot prüfen', 'done': False}}
        app = SimpleNamespace(find_item_in_lists=lambda identity: (items[identity],) if identity in items else None)
        widget = Control(state='normal')
        result = core.task_completion_attributes(widget, app, 't')
        self.assertEqual((result.role, result.name, result.value), ('Button', 'Aufgabe erledigen', 'Offen'))
        items['t'] = {'text': 'Ersetztes Angebot', 'done': True}
        app._data_read_only = True
        result = core.task_completion_attributes(widget, app, 't')
        self.assertEqual((result.name, result.description, result.value, result.state),
                         ('Aufgabe wieder öffnen', 'Ersetztes Angebot', 'Erledigt', 'disabled'))
        items.clear()
        self.assertIsNone(core.task_completion_attributes(widget, app, 't'))

    def test_native_button_action_tracks_removed_and_later_replaced_callback(self):
        widget = fixtures.Widget(); widget._root = lambda: widget
        widget.cget = lambda key: 'normal'; widget.text = 'Ausführen'
        calls = []; widget.command = lambda: calls.append('first')
        binding = core.bind_button(widget)
        binding.invoke(); self.assertEqual(calls, ['first'])
        widget.command = None
        self.assertEqual(core.button_attributes(widget).state, 'disabled')
        binding.invoke(); self.assertEqual(calls, ['first'])
        widget.command = lambda: calls.append('second')
        self.assertEqual(core.button_attributes(widget).state, 'normal')
        binding.invoke(); self.assertEqual(calls, ['first', 'second'])
        self.assertEqual(len(widget.commands), 1)

    def test_completion_rebinding_keeps_command_and_refuses_removed_or_readonly_target(self):
        widget = fixtures.Widget(); widget._root = lambda: widget
        widget.cget = lambda key: 'normal'
        calls = []; widget.command = lambda: calls.append('done')
        item = {'text': 'Prüfen'}
        app = SimpleNamespace(find_item_in_lists=lambda identity: (item,) if item else None)
        binding = core.bind_task_completion(widget, app, 't')
        self.assertIs(core.bind_task_completion(widget, app, 't'), binding)
        self.assertEqual(len(widget.commands), 1)
        binding.invoke(); self.assertEqual(calls, ['done'])
        app._data_read_only = True
        binding.invoke(); self.assertEqual(calls, ['done'])
        app._data_read_only = False; item.clear()
        binding.invoke(); self.assertEqual(calls, ['done'])


if __name__ == '__main__':
    unittest.main()
