"""Semantik des Aufgaben-Kernablaufs; Widgetadapter ohne Tk-Import."""
from accessibility import Attributes, plain, task_value
from accessibility_bindings import Binding, available


def control_name(text):
    text = plain(text)
    special = {'+': 'Hinzufügen', '×': 'Entfernen', '…': 'Weitere Aktionen',
               '...': 'Weitere Aktionen', '←': 'Zurück', '→': 'Weiter'}
    if text in special:
        return special[text]
    while text and not (text[0].isalnum() or text[0] in 'ÄÖÜäöü'):
        text = text[1:].lstrip()
    return text.rstrip(' …') or 'Aktion'


def bind_control(widget, attributes, *, action=None):
    old = getattr(widget, '_glide_accessibility', None)
    if old is not None and not old.closed:
        old.attributes = attributes
        old.action = action
        if action is not None and old.command is None and old.supported:
            old.command = widget.register(old.invoke)
        old.refresh()
        return old
    root = widget._root()
    supported = getattr(root, '_glide_accessibility_supported', None)
    if supported is None:
        supported = root._glide_accessibility_supported = available(widget.tk.call)
    binding = Binding(widget, attributes, action=action, supported=supported)
    widget._glide_accessibility = binding
    return binding


def refresh(widget, *, selection=False):
    binding = getattr(widget, '_glide_accessibility', None)
    if binding is not None:
        binding.refresh(selection=selection)


def button_attributes(widget):
    state = str(widget.cget('state'))
    if getattr(widget, '_accessible_disabled', False) or not callable(getattr(widget, 'command', None)):
        state = 'disabled'
    name = getattr(widget, '_accessible_name', None)
    if not name:
        tooltip = getattr(widget, '_glide_tooltip', {}).get('source')
        tooltip = tooltip() if callable(tooltip) else tooltip
        name = plain(tooltip) if tooltip and not any(char.isalnum() for char in widget.text) else control_name(widget.text)
    value = getattr(widget, '_accessible_value', lambda: '')()
    return Attributes(getattr(widget, '_accessible_role', 'Button'), name, state=state, value=value,
                      help='Mit Leertaste oder Enter ausführen.')


def bind_button(widget):
    return bind_control(widget, lambda: button_attributes(widget), action=lambda: widget.command())


def bind_checkbox(widget, variable, name):
    return bind_control(widget, lambda: Attributes('Checkbutton', name,
        value='1' if variable.get() else '0', state=str(widget.cget('state')),
        description='Ausgewählt' if variable.get() else 'Nicht ausgewählt',
        help='Mit Leertaste umschalten.'), action=widget.invoke)


def attachment_attributes(app, identity, index):
    state = getattr(app, '_detail_state', {})
    attachments = state.get('fields', {}).get('attachments', ())
    if (state.get('item_id') != identity or app.find_item_in_lists(identity) is None or
            not 0 <= index < len(attachments)):
        return None
    return Attributes('Button', 'Anhang öffnen: '+plain(attachments[index].get('name') or 'Anhang'),
                      help='Mit Leertaste oder Enter öffnen.')


def bind_attachment(widget, app, identity, index):
    binding = bind_control(widget, lambda: attachment_attributes(app, identity, index),
                           action=lambda: app.open_detail_pane_attachment(index))
    widget.configure(takefocus=True)
    for sequence in ('<Return>', '<space>'):
        if sequence not in binding.bindings:
            binding.bindings[sequence] = widget.bind(sequence, lambda _event: binding.invoke(), add='+')
    return binding


def entry_attributes(widget, name, *, text=False, help='', placeholder=None):
    value = '' if placeholder is not None and placeholder() else (
        widget.get('1.0', 'end-1c') if text else widget.get())
    return Attributes('Text' if text else 'Entry', name, value=str(value or ''),
                      state=str(widget.cget('state')), help=help or 'Mit den normalen Texttasten bearbeiten.')


def bind_entry(widget, name, *, text=False, help='', placeholder=None):
    binding = bind_control(widget, lambda: entry_attributes(widget, name, text=text, help=help, placeholder=placeholder))
    if binding.supported and not getattr(widget, '_accessible_entry_keys', False):
        identity = widget.bind('<KeyRelease>', lambda _event: binding.refresh(selection=True), add='+')
        binding.bindings['<KeyRelease>'] = identity
        widget._accessible_entry_keys = True
    return binding


def choice_disabled(widget):
    predicate = getattr(widget, '_inspector_readonly', None)
    target = getattr(widget, 'summary_label', widget)
    state = target.cget('state') if hasattr(target, 'cget') else 'normal'
    return str(state) == 'disabled' or bool(predicate() if callable(predicate) else predicate)


def choice_attributes(widget):
    return Attributes('Combobox', getattr(widget, '_accessible_name', 'Auswahl'),
                      value=plain(widget.variable.get()), state='disabled' if choice_disabled(widget) else 'normal',
                      help='Mit Enter öffnen, Pfeiltasten wählen, Enter übernehmen, Escape abbrechen.')


def bind_choice(widget, name=None):
    if name:
        widget._accessible_name = name
    return bind_control(widget, lambda: choice_attributes(widget), action=lambda: widget._open_popup())


def bind_options(widget, owner):
    return bind_control(widget, lambda: Attributes('Listbox', getattr(owner, '_accessible_name', 'Auswahl'),
        state='disabled' if choice_disabled(owner) else 'normal',
        value=plain(widget.options[widget._selected]) if widget.options else 'Keine Auswahl',
        help='Pfeiltasten wählen, Enter übernimmt, Escape bricht ab.'), action=owner._commit)


def label_selection_attributes(dropdown, *, popup=False):
    if popup:
        index = getattr(dropdown, '_focus_index', 0)
        label = dropdown.labels[index] if 0 <= index < len(dropdown.labels) else None
        value = (plain(label.get('name')) + ('. Ausgewählt.' if label.get('id') in dropdown.selected_ids
                                           else '. Nicht ausgewählt.')) if label else 'Keine Labels vorhanden.'
    else:
        value = ', '.join(plain(label.get('name')) for label in dropdown.labels
                          if label.get('id') in dropdown.selected_ids) or 'Keine Labels ausgewählt.'
    return Attributes('Listbox' if popup else 'Combobox', 'Labels', value=value,
                      state='disabled' if choice_disabled(dropdown) else 'normal',
                      help='Enter öffnet oder beendet die Auswahl. Pfeiltasten wählen ein Label, Leertaste schaltet es um.')


def bind_labels(dropdown, popup=None):
    widget = popup or dropdown.summary_label
    return bind_control(widget, lambda: label_selection_attributes(dropdown, popup=popup is not None),
                        action=dropdown._toggle_focused if popup is not None else dropdown._open_popup)


def navigation_attributes(tree, name):
    selected = tuple(tree.selection())
    focused = tree.focus()
    identity = focused if focused in selected and tree.exists(focused) else next(
        (value for value in selected if tree.exists(value)), None)
    title = plain(tree.item(identity, 'text')) if identity is not None else ''
    return Attributes('Tree', name + (': ' + title if title else ''),
                      value=title or 'Keine Auswahl.',
                      help='Mit Pfeil auf und ab den Bereich oder die Liste wählen.')


def bind_navigation(app):
    for key, name in (('system_listbox', 'Arbeitsbereiche'),
                      ('sidebar_listbox', 'Listen und Ordner'),
                      ('pages_listbox', 'Seiten'), ('notes_listbox', 'Notizbücher'),
                      ('drawings_listbox', 'Zeichnungen')):
        tree = getattr(app, key, None)
        if tree is not None:
            bind_control(tree, lambda target=tree, caption=name: navigation_attributes(target, caption))


def task_completion_attributes(widget, app, identity):
    found = app.find_item_in_lists(identity)
    if found is None:
        return None
    item = found[0]
    done = bool(item.get('done'))
    return Attributes('Button', 'Aufgabe wieder öffnen' if done else 'Aufgabe erledigen',
                      description=plain(item.get('text')), value='Erledigt' if done else 'Offen',
                      state='disabled' if getattr(app, '_data_read_only', False) else str(widget.cget('state')),
                      help='Mit Leertaste oder Enter ausführen.')


def bind_task_completion(widget, app, identity):
    return bind_control(widget, lambda: task_completion_attributes(widget, app, identity),
                        action=lambda: widget.command())


def bind_due(field):
    name = 'Bearbeitungstag' if field.purpose == 'planned' else 'Fälligkeit'
    bind_entry(field.date_entry, name, help='Datum als Tag, Monat und Jahr eingeben, zum Beispiel 13.10.2026.')
    time = getattr(field, 'time_entry', None)
    if time is not None:
        bind_entry(time, name + ': Uhrzeit', help='Freiwillige Uhrzeit als Stunde und Minute eingeben, zum Beispiel 09:30.')
    if field.calendar_button is not None:
        field.calendar_button._accessible_name = name + ' im Kalender wählen'
        refresh(field.calendar_button)


def checklist_attributes(app, identity, index):
    found = app.find_item_in_lists(identity)
    steps = found[0].get('checklist', ()) if found else ()
    if not 0 <= index < len(steps):
        return None
    step = steps[index]
    return Attributes('Checkbutton', plain(step.get('text')) or 'Checklistenpunkt',
        # Tk 9.1 leitet den nativen Checked-Zustand aus dem Wert "1" ab.
        value='1' if step.get('done') else '0',
        description='Erledigt' if step.get('done') else 'Offen',
        state='disabled' if getattr(app, '_data_read_only', False) else 'normal',
        help='Leertaste oder Enter schaltet den Checklistenpunkt um.')


def bind_checklist(widget, app, identity, index):
    widget._accessible_step_index = index
    found = app.find_item_in_lists(identity)
    steps = found[0].get('checklist', ()) if found else ()
    step_id = steps[index].get('id') if 0 <= index < len(steps) else None
    def current_attributes():
        found = app.find_item_in_lists(identity)
        steps = found[0].get('checklist', ()) if found else ()
        if step_id is not None and (not 0 <= index < len(steps) or steps[index].get('id') != step_id):
            return None
        current = checklist_attributes(app, identity, index)
        variable = getattr(widget, '_accessible_variable', None)
        if (variable is not None and current is not None and widget.winfo_exists()
                and bool(variable.get()) != (current.value == '1')):
            variable.set(current.value == '1')
        return current

    def sync_variable():
        current_attributes()

    def invoke():
        # Ein echter Checkbutton schaltet seine Variable vor dem Maus-Command.
        # Maßgeblich bleibt der Datensatz, auch bei Schreibschutz/Schreibfehler.
        try:
            current = current_attributes()
            if (current is None or current.state == 'disabled' or binding.closed or
                    not widget.winfo_exists() or not widget.winfo_ismapped()):
                return 'break'
            app.toggle_detail_pane_step(identity, index)
        finally:
            sync_variable()
            binding.refresh()
        if app._detail_state.get('item_id') == identity:
            for target in app.iter_descendants(app.detail_pane):
                if getattr(target, '_accessible_step_index', None) == index:
                    target.focus_set()
                    break
        return 'break'
    binding = bind_control(widget, current_attributes, action=invoke)
    widget.configure(takefocus=True, command=invoke)
    for sequence in ('<Return>', '<space>'):
        if sequence not in binding.bindings:
            binding.bindings[sequence] = widget.bind(sequence, lambda _event: binding.invoke(), add='+')
    return binding


def inspector_structure_matches(app, item):
    baseline = getattr(app, '_detail_state', {}).get('baseline') or {}
    return [step.get('id') for step in baseline.get('checklist', ())] == [
        step.get('id') for step in item.get('checklist', ())]


def refresh_inspector(app):
    for widget in app.iter_descendants(app.detail_pane):
        binding = getattr(widget, '_glide_accessibility', None)
        if binding is not None and not binding.closed:
            # Auch der ältere Tk-Startweg benötigt aktuelle echte Haken nach
            # Undo, während fokussierte Texteingaben erhalten bleiben.
            if hasattr(widget, '_accessible_step_index'):
                binding.attributes()
            binding.refresh()


def selected_task_attributes(app):
    identity = app.get_selected_item_id()
    found = app.find_item_in_lists(identity) if identity else None
    name = 'Mein Tag: Aufgaben' if app.view_mode == app.PLAN_DAY_VIEW else 'Aufgaben'
    count = len(app.get_selected_item_ids())
    if found is None:
        value = 'Keine Aufgabe ausgewählt.'
    else:
        item = found[0]
        blockers = [target[0].get('text', '') for key in item.get('blocked_by', ())
                    if (target := app.find_item_in_lists(key)) and not target[0].get('done')]
        value = task_value(item, label_names=[label.get('name', '') for label in app.item_labels(item)],
                           blocked_titles=blockers)
        if count > 1:
            value = f'{count} Aufgaben ausgewählt. Aktuelle Aufgabe: ' + value
    return Attributes('Tree', name, value=value,
                      description='Schreibgeschützter Bestand.' if getattr(app, '_data_read_only', False) else '',
                      help='Pfeil auf und ab wählen Aufgaben. Leertaste erledigt. F2 öffnet den Inspektor. '
                           'Strg oder Cmd plus Umschalt plus P plant die Auswahl. Escape schließt den Inspektor.')


def install_core(app):
    bind_navigation(app)
    bind_entry(app.entry, 'Neue Aufgabe', help='Aufgabe eintippen, Enter fügt sie hinzu. Umschalt plus Enter öffnet alle Felder.',
               placeholder=lambda: app.entry_placeholder_active)
    bind_entry(app.search_entry, 'Aufgaben suchen', help='Suchtext eingeben. Escape löscht die Suche. Die Ergebnisliste folgt darunter.',
               placeholder=lambda: app.search_placeholder_active)
    bind_control(app.tree, lambda: selected_task_attributes(app))
    app.add_button._accessible_name = 'Aufgabe hinzufügen'
    refresh(app.add_button)


def bind_inspector_fields(fields):
    names = {'text': 'Aufgabentitel', 'estimated_minutes': 'Aufwand in Minuten',
             'time_spent_minutes': 'Erfasste Zeit in Minuten', 'description': 'Beschreibung'}
    for key, name in names.items():
        widget = fields.get(key)
        if widget is not None:
            bind_entry(widget, name, text=key == 'description' or
                       (key == 'text' and widget.winfo_class() == 'Text'))
