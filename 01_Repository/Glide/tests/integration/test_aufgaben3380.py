"""Gemeinsamer Inspektor, echte Feldklicks, Bewegung und tatsächliche Inhaltsfläche.

Alle Fälle verwenden ausschließlich künstliche Daten und echte Tk-Widgets.
--app/--fall ermöglichen rote Gegenproben gegen die unmittelbare Vorversion.
--tempo prüft zusätzlich die Wandzeit auf dem Referenz-Mac. CI prüft Dauervertrag,
sofortige Bedienbarkeit, Abbruch und Rückstände; ihre Laufzeiten werden berichtet.
Die getrennte menschliche Sicht-/DPI-/Screenreader-Abnahme bleibt offen.
"""
import argparse
import json
from pathlib import Path
import tempfile

def inspektor(app_path, report, *, gross=False, tempo=False):
    from types import SimpleNamespace
    args = SimpleNamespace(app=app_path, report=report, gross=gross, tempo=tempo)
    'Reale Inspektor-/Feldpickerprobe im lokalen Entwurf; keine Produktabnahme.'
    import copy, importlib.machinery, importlib.util, json, os, sys, tempfile
    from pathlib import Path
    from datetime import date, timedelta
    sys.path.insert(0, str(args.app.parent))
    checks = []
    errors = []
    with tempfile.TemporaryDirectory(prefix='glide-inspektor3380-') as data:
        os.environ['GLIDE_DATA_DIR'] = data
        os.environ['GLIDE_TEST_MODE'] = '1'
        loader = importlib.machinery.SourceFileLoader('glide_inspektor3380_entwurf', str(args.app))
        m = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
        sys.modules[loader.name] = m
        loader.exec_module(m)
        assert hasattr(m.ListApp, "open_task_inspector"), "Gemeinsamer Aufgabeninspektor fehlt"
        root = m.tk.Tk()
        root.geometry('1280x800+20+20')
        root.report_callback_exception = lambda *e: errors.append(repr(e[1]))
        app = m.ListApp(root)
        app.show_info = app.show_warning = lambda *a, **k: None
        app.show_error = lambda *a, **k: errors.append(str(a))

        def idle():
            for _ in range(3):
                root.update_idletasks()
                root.update()

        def item():
            return app.find_item_in_lists(tid)[0]
        task = app.new_item('Inspektorprobe', due=(date.today() + timedelta(days=2)).isoformat(), planned_date=date.today().isoformat(), importance=2, description='Beschreibung bleibt', estimated_minutes=30, repeat={'art': 'tage', 'abstand': 3}, reminder={'mode': 'relative', 'minutes': 30, 'delivered_key': 'probe', 'delivered_at': '2026-10-01T08:00:00Z'})
        second = app.new_item('Auswahlziel')
        source = app.new_list_object('Gemeinsame Aufgabe', [task, second])
        page = app.new_list_object('Dokumentverweis', [], list_kind='page', rich_note={'text': 'Kontext', 'spans': [], 'links': {}})
        app.lists.extend([source, page])
        app.save_items()
        tid = task['id']
        sid = source['id']
        pid = page['id']
        contexts = [('Liste', lambda: app.set_active_list(sid)), ('Tabelle', lambda: (app.set_active_list(sid), app.set_table_view())), ('Heute', app.set_today_view), ('Demnächst', app.set_in_progress_view), ('Pinnwand', lambda: (app.set_active_list(sid), app.workspace.pin([tid]), app.workspace.set_mode('board'))), ('Dokument', lambda: app.set_active_list(pid))]
        try:
            for name, open_view in contexts:
                open_view()
                idle()
                assert app.open_task_inspector(tid)
                idle()
                assert app.detail_pane.winfo_ismapped(), (name, 'Inspektor unsichtbar')
                assert app._detail_state['item_id'] == tid, (name, 'falsches Ziel')
                fields = app._detail_state['fields']
                assert {'text', 'due', 'planned', 'importance', 'labels', 'description', 'estimated_minutes', 'repeat', 'reminder'} <= set(fields), (name, set(fields))
                before = copy.deepcopy(item())
                depth = len(app.undo_stack)
                title = fields['text']
                title.delete(0, 'end')
                title.insert(0, name + ' bearbeitet')
                app.commit_detail_pane()
                idle()
                assert item()['text'] == name + ' bearbeitet' and len(app.undo_stack) == depth + 1, (name, 'Speichern/Undo')
                assert item()['description'] == before['description'] and item()['planned_date'] == before['planned_date'], name
                app.undo_last_change()
                idle()
                assert item()['text'] == before['text'], name
                fields = app._detail_state['fields']
                fields['text'].delete(0, 'end')
                fields['text'].insert(0, 'Verwerfen')
                app.close_task_inspector(discard=True)
                idle()
                assert item()['text'] == before['text'], name
                checks.append(name + ': gleicher Inspektor, Felder, Speichern/ein Undo/Verwerfen')
            app.set_active_list(sid)
            app.workspace.set_mode('list')
            idle()
            root.geometry('860x700+20+20')
            idle()
            assert app.open_task_inspector(tid)
            idle()
            pane = app.detail_pane
            host = app.content_frame
            assert pane.winfo_ismapped() and app._inspector_narrow
            assert pane.winfo_x() >= 0 and pane.winfo_x() + pane.winfo_width() <= host.winfo_width() + 1
            assert pane.winfo_y() >= 0 and pane.winfo_y() + pane.winfo_height() <= host.winfo_height() + 1
            assert app.sidebar_listbox.winfo_ismapped()
            app.close_task_inspector()
            idle()
            assert app.tree.winfo_ismapped()
            checks.append('860×700: Inhaltsinspektor, Navigation bleibt bedienbar, Schließen stellt Inhalt her')
            root.geometry('1280x800+20+20')
            idle()
            assert app.open_task_inspector(tid)
            idle()
            title = app._detail_state['fields']['text']
            title.delete(0, 'end')
            before = copy.deepcopy(item())
            old_context = app.inspector_context()
            app.set_today_view()
            idle()
            assert app.inspector_context() == old_context and app.detail_pane.winfo_ismapped()
            assert app._detail_commit_error and item() == before
            app.on_close()
            assert root.winfo_exists() and (not app._closing)
            app.close_task_inspector(discard=True)
            idle()
            assert item() == before
            checks.append('Leerer Titel: Navigation und Beenden halten an, Eingabe verwerfbar')
            assert app.open_task_inspector(tid)
            idle()
            title = app._detail_state['fields']['text']
            title.delete(0, 'end')
            title.insert(0, 'Schreibschutz-Eingabe')
            app._data_read_only = True
            try:
                app.set_today_view()
                idle()
                assert app.inspector_context() == old_context and app._detail_commit_error and (item() == before)
            finally:
                app._data_read_only = False
            app.close_task_inspector(discard=True)
            idle()
            checks.append('Neu eingetretener Schreibschutz: Eingabe bleibt, kein Ansichtswechsel')
            assert app.open_task_inspector(tid)
            idle()
            title = app._detail_state['fields']['text']
            title.delete(0, 'end')
            title.insert(0, 'Nach Schreibfehler erneut gespeichert')
            disk = Path(m.SAVE_FILE).read_bytes()
            depth = len(app.undo_stack)
            history = copy.deepcopy(app.history)
            dirty = app.dirty
            original_write = app.write_json_atomic
            original_error = app.show_error
            expected = []

            def fail_write(path, payload):
                if str(path) == str(m.SAVE_FILE):
                    raise OSError('Absichtlicher Schreibfehler in synthetischen Daten')
                return original_write(path, payload)
            app.write_json_atomic = fail_write
            app.show_error = lambda *a, **k: expected.append(a)
            try:
                assert app.commit_detail_pane() is False and app._detail_commit_error
                assert item() == before and Path(m.SAVE_FILE).read_bytes() == disk and (len(app.undo_stack) == depth)
                assert app.history == history and app.dirty == dirty and (title.get() == 'Nach Schreibfehler erneut gespeichert')
                app.set_today_view()
                assert app.inspector_context() == old_context
            finally:
                app.write_json_atomic = original_write
                app.show_error = original_error
            assert expected
            assert app.commit_detail_pane() is True
            idle()
            assert item()['text'] == 'Nach Schreibfehler erneut gespeichert' and len(app.undo_stack) == depth + 1
            app.undo_last_change()
            idle()
            assert item() == before
            app.close_task_inspector()
            idle()
            checks.append('Echter Dateischreibfehler: Modell/Undo/Verlauf/Datei bleiben, erneutes Speichern ist ein Undo')
            assert app.open_task_inspector(tid)
            idle()
            app.tree.selection_set(second['id'])
            app.tree.focus(second['id'])
            idle()
            assert app._detail_state['item_id'] == second['id']
            app._detail_state['fields']['text'].delete(0, 'end')
            app.tree.selection_set(tid)
            app.tree.focus(tid)
            idle()
            assert app._detail_state['item_id'] == second['id'] and app.tree.focus() == second['id'] and app._detail_commit_error
            app.close_task_inspector(discard=True)
            idle()
            checks.append('Echte Zeilenauswahl wechselt den Inspektor; fehlerhafte Eingabe hält Ziel und Auswahl fest')
            app.set_active_list(sid)
            app.workspace.set_mode('list')
            idle()
            assert app.open_task_inspector(tid)
            idle()
            before = copy.deepcopy(item())
            depth = len(app.undo_stack)
            title = app._detail_state['fields']['text']
            title.focus_force()
            idle()
            title.delete(0, 'end')
            title.insert(0, 'Per Tastatur gespeichert')
            title.event_generate('<Command-s>' if m.IS_MACOS else '<Control-s>')
            idle()
            assert item()['text'] == 'Per Tastatur gespeichert' and len(app.undo_stack) == depth + 1
            assert app.detail_status.cget('fg') == app.theme['confirm']
            title.delete(0, 'end')
            app.save_task_inspector()
            assert app._detail_commit_error and app.detail_status.cget('fg') == app.theme['delete']
            title.insert(0, 'Per Tastatur gespeichert')
            app.save_task_inspector()
            assert not app._detail_commit_error and len(app.undo_stack) == depth + 1
            title.event_generate('<Escape>')
            idle()
            assert not app.detail_pane.winfo_ismapped()
            app.undo_last_change()
            idle()
            assert item() == before
            checks.append('Speichern per Cmd/Ctrl+S aus dem echten Titelfeld; Escape schließt, ein Undo stellt den Titel her')
            assert app.open_task_inspector(tid)
            idle()
            for name, action in (('Anfügen', lambda: app.add_detail_pane_step(tid, 'Schreibfehler-Schritt')),):
                before = copy.deepcopy(item())
                disk = Path(m.SAVE_FILE).read_bytes()
                depth = len(app.undo_stack)
                history = copy.deepcopy(app.history)
                dirty = app.dirty
                expected = []
                app.write_json_atomic = fail_write
                app.show_error = lambda *a, **k: expected.append(a)
                try:
                    assert action() is False and app._detail_commit_error
                    assert item() == before and Path(m.SAVE_FILE).read_bytes() == disk and (len(app.undo_stack) == depth)
                    assert app.history == history and app.dirty == dirty
                finally:
                    app.write_json_atomic = original_write
                    app.show_error = original_error
                assert expected and action() is True
                idle()
                assert len(app.undo_stack) == depth + 1
                assert len(item()['checklist']) == len(before['checklist']) + 1
                checks.append('Checkliste ' + name + ': Schreibfehler lässt Modell/Datei/Undo/Verlauf unverändert; Wiederholen fügt genau einen Schritt an')
            for name, action in (('Abhaken', lambda: app.toggle_detail_pane_step(tid, 0)), ('Entfernen', lambda: app.remove_detail_pane_step(tid, 0))):
                before = copy.deepcopy(item())
                disk = Path(m.SAVE_FILE).read_bytes()
                depth = len(app.undo_stack)
                history = copy.deepcopy(app.history)
                dirty = app.dirty
                expected = []
                app.write_json_atomic = fail_write
                app.show_error = lambda *a, **k: expected.append(a)
                try:
                    action()
                    assert app._detail_commit_error and item() == before and (Path(m.SAVE_FILE).read_bytes() == disk)
                    assert len(app.undo_stack) == depth and app.history == history and (app.dirty == dirty)
                finally:
                    app.write_json_atomic = original_write
                    app.show_error = original_error
                assert expected
                action()
                idle()
                assert len(app.undo_stack) == depth + 1 and item()['checklist'] != before['checklist']
                app.undo_last_change()
                idle()
                assert item() == before
                checks.append('Checkliste ' + name + ': echter Schreibfehler und erfolgreicher Wiederholungsversuch, ein Undo')
            app.close_task_inspector()
            idle()
            app.workspace.pin([tid, second['id']])
            app.workspace.set_mode('board')
            idle()
            app.workspace.focus_card(tid)
            assert app.open_task_inspector(tid)
            idle()
            app.workspace.next_card(1)
            idle()
            assert app._detail_state['item_id'] == second['id']
            app._detail_state['fields']['text'].delete(0, 'end')
            app.workspace.next_card(1)
            idle()
            assert app._detail_state['item_id'] == second['id'] and app.workspace.selected_id == second['id'] and app._detail_commit_error
            app.close_task_inspector(discard=True)
            app.workspace.set_mode('list')
            idle()
            checks.append('Pinnwand-Tastaturauswahl wechselt den Inspektor; ungültige Eingabe hält die Auswahl fest')
            assert app.open_task_inspector(tid)
            idle()
            before = copy.deepcopy(item())
            depth = len(app.undo_stack)
            assert app.commit_detail_pane() is False and (not app._detail_commit_error) and (item() == before) and (len(app.undo_stack) == depth)
            app.skip_detail_pane_repeat(tid)
            idle()
            assert item()['due'] == (date.fromisoformat(before['due']) + timedelta(days=3)).isoformat()
            assert len(app.undo_stack) == depth + 1 and (not app._detail_commit_error)
            app.undo_last_change()
            idle()
            assert item() == before and len(app.undo_stack) == depth
            app.close_task_inspector()
            idle()
            checks.append('Wiederholungsanker und Zustellbeleg sind keine Eingabeänderung; Überspringen und Undo bleiben genau ein Schritt')
            for field in ('planned', 'due', 'importance', 'labels'):
                before = copy.deepcopy(item())
                depth = len(app.undo_stack)
                observed = {}

                def act():
                    dialogs = [w for w in root.winfo_children() if hasattr(w, '_glide_task_field')]
                    if not dialogs:
                        observed['missing'] = True
                        return
                    dialog = dialogs[0]
                    state = dialog._glide_task_field
                    observed['identity'] = state['item_id']
                    observed['field'] = state['field']
                    if field in ('planned', 'due'):
                        state['picker'].set_due((date.today() + timedelta(days=3)).isoformat())
                    elif field == 'importance':
                        state['variable'].set(app.importance_choice_text(3))
                    state['submit']() if field != 'labels' else state['cancel']()
                drive = root.after(80, act)

                def timeout():
                    observed['timeout'] = True
                    for w in root.winfo_children():
                        if hasattr(w, '_glide_task_field'):
                            w.destroy()
                guard = root.after(10000, timeout)
                app.edit_task_field(tid, field, app.title_label)
                for job in (drive, guard):
                    try:
                        root.after_cancel(job)
                    except m.tk.TclError:
                        pass
                idle()
                assert observed.get('identity') == tid and observed.get('field') == field and (not observed.get('timeout')), observed
                assert len(app.undo_stack) == depth + (field != 'labels'), (field, 'Undo')
                if field == 'labels':
                    assert item() == before
                else:
                    app.undo_last_change()
                    idle()
                    assert item() == before, (field, 'Rücknahme')
                checks.append(field + ': realer Modalweg, Speichern/Abbrechen und Undo')
            expected_model = copy.deepcopy(item())
            assert app.save_items()
            app.cancel_pending_callbacks()
            app.release_data_lock()
            for job in root.tk.call('after', 'info'):
                root.tk.call('after', 'cancel', job)
            root.destroy()
            root = m.tk.Tk()
            root.geometry('1280x800+20+20')
            root.report_callback_exception = lambda *e: errors.append(repr(e[1]))
            app = m.ListApp(root)
            app.show_info = app.show_warning = lambda *a, **k: None
            app.show_error = lambda *a, **k: errors.append(str(a))
            idle()
            assert item() == expected_model
            checks.append('Tatsächlicher Neustart bewahrt die vollständige Aufgabe einschließlich Planung, Wiederholung und Zustellbeleg')
            assert not errors, errors
        finally:
            app.cancel_pending_callbacks()
            app.release_data_lock()
            for job in root.tk.call('after', 'info'):
                root.tk.call('after', 'cancel', job)
            root.destroy()
    args.report.write_text(json.dumps({'produktionstest': True, 'pruefungen': checks, 'fehler': errors}, ensure_ascii=False, indent=2) + '\n')
    print('\n'.join(checks))

def klicks(app_path, report, *, gross=False, tempo=False):
    from types import SimpleNamespace
    a = SimpleNamespace(app=app_path, report=report, gross=gross, tempo=tempo)
    import copy, importlib.machinery, importlib.util, json, os, sys, tempfile, time, types
    from pathlib import Path
    from datetime import date, timedelta
    sys.path.insert(0, str(a.app.parent))
    checks = []
    errors = []
    with tempfile.TemporaryDirectory(prefix='glide-klick3380-') as data:
        os.environ['GLIDE_DATA_DIR'] = data
        os.environ['GLIDE_TEST_MODE'] = '1'
        loader = importlib.machinery.SourceFileLoader('glide_klickprobe', str(a.app))
        m = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
        sys.modules[loader.name] = m
        loader.exec_module(m)
        assert hasattr(m.ListApp, "edit_task_field"), "Direkte Aufgabenfeldbearbeitung fehlt"
        root = m.tk.Tk()
        root.report_callback_exception = lambda *e: errors.append(repr(e[1]))
        app = m.ListApp(root)
        root.geometry('1280x800+20+20')
        app.show_info = app.show_warning = lambda *a, **k: None
        app.show_error = lambda *a, **k: errors.append(repr(a))

        def idle():
            for _ in range(3):
                root.update_idletasks()
                root.update()
        stamp = 1000

        def click(w, x, y, state=0):
            nonlocal stamp
            stamp += 1000
            w.event_generate('<ButtonPress-1>', x=round(x), y=round(y), state=state, time=stamp)
            idle()
            w.event_generate('<ButtonRelease-1>', x=round(x), y=round(y), state=state, time=stamp + 50)
            idle()
        label = app.new_label_object('Kunde')
        app.labels.append(label)
        task = app.new_item('Exposé abschließend prüfen', due=(date.today() + timedelta(days=2)).isoformat(), planned_date=date.today().isoformat(), importance=2, labels=[label['id']])
        other = app.new_item('Zweite Karte', due=date.today().isoformat(), planned_date=date.today().isoformat())
        source = app.new_list_object('Projekt', [task, other])
        page = app.new_list_object('Dokument', [], list_kind='page', rich_note={'text': 'Bezug\n', 'spans': [], 'links': {}}, live_lists=['glide://list/' + source['id']])
        app.lists.extend([source, page])
        app.save_items()
        tid = task['id']
        sid = source['id']
        pid = page['id']
        calls = []
        original = app.edit_task_field
        app.edit_task_field = lambda identity, field, anchor=None: calls.append((identity, field)) or 'break'
        try:
            views = [('Liste', lambda: (app.set_active_list(sid), app.workspace.set_mode('list'))), ('Tabelle', lambda: (app.set_active_list(sid), app.set_table_view())), ('Heute', app.set_today_view), ('Demnächst', app.set_in_progress_view)]
            for name, open_view in views:
                print('Ansicht', name, flush=True)
                open_view()
                idle()
                if name == 'Tabelle':
                    app.settings['table_columns'][sid] = ['title', 'importance', 'planned_date', 'due', 'labels']
                    app.settings['table_column_widths'][sid] = {'title': 280, 'importance': 70, 'planned_date': 120, 'due': 120, 'labels': 120}
                    app.refresh_tree()
                    idle()
                row = next((r for r in app.iter_tree_ids() if app.in_progress_item_sources.get(r, (None, r))[1] == tid))
                app.tree.see(row)
                idle()
                app.tree.selection_set(row)
                app.tree.focus(row)
                idle()
                app.show_quick_plan_row()
                idle()
                for key in ('quick_plan_row_button', 'row_due_button', 'row_overflow_button'):
                    button = getattr(app, key)
                    assert button.winfo_ismapped(), (name, key)
                    assert button.winfo_x() >= app.tree.winfo_x() + app.tree.winfo_width(), (name, 'Feld überdeckt')
                for col, field in [('importance', 'importance'), ('planned_date', 'planned'), ('due', 'due'), ('labels', 'labels')] if name == 'Tabelle' else [('due', 'due'), ('due', 'planned'), ('labels', 'labels'), ('#0', 'importance')]:
                    box = app.tree.bbox(row, col)
                    if name == 'Tabelle' and box and (box[0] >= app.tree.winfo_width()):
                        app.tree.xview_moveto(1)
                        idle()
                        box = app.tree.bbox(row, col)
                    assert box and box[2] > 0 and (box[0] < app.tree.winfo_width()), (name, field, 'Pflichtfeld fehlt')
                    x = box[0] + 12
                    y = box[1] + box[3] // 2
                    if col == 'due' and field == 'planned' and (name != 'Tabelle'):
                        # B13: nur die Titelzelle der nächsten Aufgabe ist fett, in Zeilengröße.
                        font = app.tree_cell_font(row, 'due')
                        prefix = m.glide_interaction.date_text(app.format_due_column(task['due']), '', app.DUE_COLUMN_ICON, app.ICONS['today']) + ' · '
                        x = box[0] + 8 + font.measure(prefix) + 12
                    if col == '#0':
                        display = app.tree.item(row, 'text')
                        body = app.item_display_text(task)
                        marker = app.IMPORTANCE_MARKERS[2]
                        idx = display.rfind(marker, 0, display.rfind(body))
                        assert idx >= 0, (name, display)
                        start = next((x for x in range(box[0], box[0] + box[2]) if app.tree.identify_element(x, y) == 'text'))
                        font = app.tree_cell_font(row, '#0')
                        x = start + font.measure(display[:idx]) + font.measure(marker.rstrip()) / 2
                    assert x < box[0] + box[2] and x < app.tree.winfo_width(), (name, field, 'Pflichtfeld abgeschnitten')
                    print('Klick', name, field, x, y, flush=True)
                    before = len(calls)
                    click(app.tree, x, y)
                    assert calls[before:] == [(tid, field)], (name, field, x, y, calls[before:], app.tree.identify_region(x, y), app.tree.identify_column(x))
                    checks.append(name + ': echter Feldklick ' + field)
                app.tree.xview_moveto(0)
                idle()
                box = app.tree.bbox(row, 'title' if name == 'Tabelle' else '#0')
                before = len(calls)
                click(app.tree, min(app.tree.winfo_width() - 5, box[0] + box[2] - 20), box[1] + box[3] // 2, state=8 if m.IS_MACOS else 4)
                assert len(calls) == before
                checks.append(name + ': Zusatztaste bleibt Auswahl')
            long_task = app.new_item('Ausführlicher Langtext mit mehreren sichtbaren Zeilen ' * 35,
                kind=app.ITEM_KIND_LONG, importance=2)
            source['items'].append(long_task)
            app.save_items()
            app.set_active_list(sid)
            app.workspace.set_mode('list')
            idle()
            row = long_task['id']
            app.tree.see(row)
            idle()
            box = app.tree.bbox(row, '#0')
            y = box[1] + box[3] / 2
            display = app.tree.item(row, 'text')
            assert app.item_display_text(long_task) not in display
            number = m.re.match(r'^\d+(?:\.\d+)*\. ', display)
            assert number
            start = next(x for x in range(box[0], box[0] + box[2])
                         if app.tree.identify_element(x, round(y)) == 'text')
            font = app.task_row_font()
            x = start + font.measure(display[:number.end()]) + font.measure(app.IMPORTANCE_MARKERS[2].rstrip()) / 2
            before = len(calls)
            click(app.tree, x, y)
            assert calls[before:] == [(long_task['id'], 'importance')]
            checks.append('Umgebrochener Langtext: sichtbarer Wichtigkeitsmarker trifft die Kopfaufgabe')
            app.set_active_list(sid)
            app.workspace.pin([tid, other['id']])
            app.workspace.set_mode('board')
            idle()
            print('Pinnwand', flush=True)
            for layout in ('free', 'grid', 'columns'):
                print('Layout', layout, flush=True)
                app.workspace.configure_board('layout', layout)
                idle()
                for zoom in (75, 150):
                    app.workspace.configure_board('zoom', zoom)
                    idle()
                    # Spalten können breiter als der sichtbare Canvas sein.
                    # Die vorhandene Kartennavigation muss die Karte erreichbar
                    # machen; danach jeden Feldtreffer wirklich anklicken.
                    app.workspace.focus_card(tid)
                    idle()
                    hits = list(app.workspace._field_hits)
                    available = {field for _box, identity, field in hits if identity == tid}
                    assert {'due', 'planned', 'importance', 'labels'} <= available, (layout, zoom, 'Feld fehlt', available)
                    fields = set()
                    for box, identity, field in hits:
                        if identity != tid:
                            continue
                        x = box[0] + box[2] / 2
                        y = box[1] + box[3] / 2
                        c = app.workspace.canvas
                        region = tuple(map(float, root.tk.splitlist(c.cget('scrollregion'))))
                        assert len(region) == 4, (layout, zoom, region)
                        c.xview_moveto(max(0, x-region[0]-c.winfo_width()/2) / max(1, region[2]-region[0]))
                        c.yview_moveto(max(0, y-region[1]-c.winfo_height()/2) / max(1, region[3]-region[1]))
                        idle()
                        px = x - c.canvasx(0)
                        py = y - c.canvasy(0)
                        assert 0 <= px < c.winfo_width() and 0 <= py < c.winfo_height(), (
                            layout, zoom, field, 'Feld nicht erreichbar', box, region, c.xview(), c.yview())
                        before = len(calls)
                        click(c, px, py)
                        assert calls[before:] == [(tid, field)], (layout, zoom, field, calls[before:])
                        fields.add(field)
                    assert {'due', 'planned', 'importance', 'labels'} <= fields, (layout, zoom, fields)
                    checks.append(f'Pinnwand {layout}/{zoom}%: vier echte Feldklicks')
            app.workspace.configure_board('zoom', 100)
            app.workspace.configure_board('layout', 'free')
            idle()
            assert app.open_task_inspector(tid)
            idle()
            app.workspace.select_card(other['id'])
            idle()
            assert app._detail_state['item_id'] == other['id']
            app._detail_state['fields']['text'].delete(0, 'end')
            old = list(app.workspace.selected_ids)
            assert app.workspace.select_card(tid) is False
            assert app._detail_state['item_id'] == other['id'] and app.workspace.selected_ids == old
            app.close_task_inspector(discard=True)
            checks.append('Pinnwandauswahl folgt Inspektor, fehlerhafte Eingabe hält Auswahl')
            app.set_active_list(pid)
            idle()
            editor = app.rich_note_editor
            tree = editor.live_tree
            assert tree is not None and tree.winfo_ismapped()
            box = tree.bbox(tid, 'due')
            before = len(calls)
            click(tree, box[0] + 12, box[1] + box[3] / 2)
            assert calls[before:] == [(tid, 'due')], calls[before:]
            checks.append('Dokument-Live-Liste: echter Fälligkeitsklick auf Quellaufgabe')
            editor.text.mark_set('insert', '1.0')
            editor.insert_task_reference(tid)
            idle()
            start, _end = editor.task_ranges(tid)[0]
            editor.text.see(start)
            idle()
            box = editor.text.bbox(f'{start}+3c')
            assert box
            stamp += 1000
            for offset in (0, 100):
                editor.text.event_generate('<ButtonPress-1>', x=box[0]+2, y=box[1]+box[3]//2, time=stamp+offset)
                editor.text.event_generate('<ButtonRelease-1>', x=box[0]+2, y=box[1]+box[3]//2, time=stamp+offset+40)
                idle()
            assert app._detail_state['item_id'] == tid and app.current_list()['id'] == pid
            assert app.detail_pane.winfo_ismapped()
            app.close_task_inspector()
            checks.append('Dokument-Aufgabenverweis: echter Doppelklick öffnet denselben Inspektor und erhält die Seite')
            assert not errors, errors
        finally:
            app.edit_task_field = original
            app.cancel_pending_callbacks()
            app.release_data_lock()
            for job in root.tk.call('after', 'info'):
                root.tk.call('after', 'cancel', job)
            root.destroy()
    a.report.write_text(json.dumps({'produktionstest': True, 'pruefungen': checks, 'fehler': errors}, ensure_ascii=False, indent=2) + '\n')
    print('\n'.join(checks))

def bewegung(app_path, report, *, gross=False, tempo=False):
    from types import SimpleNamespace
    args = SimpleNamespace(app=app_path, report=report, gross=gross, tempo=tempo)
    'Reale Tk-Übergänge: Zustand sofort, abbrechbar, keine blockierten Eingaben.'
    import importlib.machinery, importlib.util, json, os, sys, tempfile, time
    from pathlib import Path
    from datetime import date, timedelta
    sys.path.insert(0, str(args.app.parent))
    checks = []
    errors = []
    durations = []
    with tempfile.TemporaryDirectory(prefix='glide-motion3380-') as data:
        os.environ['GLIDE_DATA_DIR'] = data
        os.environ['GLIDE_TEST_MODE'] = '1'
        loader = importlib.machinery.SourceFileLoader('glide_motion3380_entwurf', str(args.app))
        m = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
        sys.modules[loader.name] = m
        loader.exec_module(m)
        root = m.tk.Tk()
        root.geometry('1280x800+20+20')
        root.report_callback_exception = lambda *e: errors.append(repr(e[1]))
        app = m.ListApp(root)
        assert hasattr(app, "_ui_transitions"), "Unterbrechbare Aufgabenübergänge fehlen"
        app.show_info = app.show_warning = lambda *a, **k: None
        app.show_error = lambda *a, **k: errors.append(str(a))

        def pump(seconds=0.2):
            until = time.monotonic() + seconds
            while time.monotonic() < until:
                root.update()
                time.sleep(0.002)

        def finish():
            start = time.monotonic()
            while app._ui_transitions.active and time.monotonic() - start < 1:
                root.update()
                time.sleep(0.001)
            elapsed = 1000 * (time.monotonic() - start)
            durations.append(elapsed)
            assert not app._ui_transitions.active
            if args.tempo:
                assert all((v <= 150 for v in finished_durations)), finished_durations

        def normal_coords():
            return [float(app.list_frame_outer.inner_pad_x), float(app.list_frame_outer.inner_pad_y)]
        task = app.new_item('Bewegungsprobe', due=(date.today() + timedelta(days=2)).isoformat(), planned_date=date.today().isoformat())
        child = app.new_item('Unteraufgabe')
        group = app.new_item('Gliederung', kind=app.ITEM_KIND_GROUP, children=[child])
        source = app.new_list_object('Übergänge', [task, group])
        app.lists.append(source)
        app.save_items()
        tid = task['id']
        sid = source['id']
        gid = group['id']
        try:
            app.set_active_list(sid)
            pump()
            app.entry.focus_force()
            root.update()
            host = app.list_frame_outer
            window = host._window_id
            controller = app._ui_transitions
            finished_durations = []
            started = []
            original_start = controller.start

            def record_start(key, update, finish_callback=lambda: None, **kwargs):
                t = time.monotonic()

                def record_finish():
                    finished_durations.append(1000 * (time.monotonic() - t))
                    finish_callback()
                assert kwargs.get('duration_ms', 120) <= 150
                result = original_start(key, update, record_finish, **kwargs)
                started.append(key)
                return result
            controller.start = record_start
            for _ in range(5):
                app.animate_area_change()
                assert 'area' in controller.active
                assert app._area_feedback.winfo_manager() == 'place' and app._area_feedback.find_withtag('area-transition')
                assert host.coords(window) == normal_coords()
                assert root.grab_current() is None and root.focus_get() == app.entry
                app.entry.insert('end', 'x')
                assert app.entry.get().endswith('x')
                finish()
                assert host.coords(window) == normal_coords()
            checks.append('Bereich: sichtbare Akzentkante bei fester Inhaltsposition, Eingabe/Fokus sofort nutzbar, fünf Abschlüsse ohne Rückstände; Referenzzeit separat prüfbar')
            app.set_today_view()
            assert 'area' in controller.active
            finish()
            assert host.coords(window) == normal_coords()
            app.set_active_list(sid)
            finish()
            checks.append('Ansichtswechsel löst den Übergang tatsächlich aus')
            app.tree.selection_set(tid)
            app.tree.focus(tid)
            app.toggle_done()
            assert app.find_item_in_lists(tid)[0]['done']
            assert 'rows' in controller.active and host.find_withtag('task-transition')
            finish()
            assert not host.find_withtag('task-transition')
            app.undo_last_change()
            pump()
            checks.append('Abhaken: gespeicherter Zustand sofort, sichtbare Rückmeldung, danach keine Zeichenreste')
            app.toggle_tree_row_open(gid)
            assert not app.tree.item(gid, 'open')
            assert 'rows' in controller.active and host.find_withtag('task-transition')
            finish()
            app.toggle_tree_row_open(gid)
            finish()
            assert app.tree.item(gid, 'open')
            app.tree.focus(gid)
            count = started.count('rows')
            app.tree.event_generate('<<TreeviewClose>>')
            root.update()
            assert started.count('rows') == count + 1
            finish()
            checks.append('Auf-/Zuklappen: direkter und nativer Ereignisweg, Zustand sofort, Zeichen entfernt')
            for i in range(100):
                app.animate_area_change()
                app.animate_task_rows('fold', row=gid)
                assert len(controller.active) <= 2
                if i % 10 == 0:
                    root.update()
            pending = {flight.job for flight in controller.active.values() if flight.job}
            finish()
            assert not pending.intersection(root.tk.call('after', 'info'))
            assert host.coords(window) == normal_coords() and (not host.find_withtag('task-transition'))
            checks.append('100 schnelle Folgeaktionen: höchstens zwei Übergänge, keine alten Rückrufe oder Versätze')
            app.animate_area_change()
            app.animate_task_rows('fold', row=gid)
            app.settings['animations_enabled'] = False
            app.apply_theme()
            root.update()
            assert not controller.active and host.coords(window) == normal_coords() and (not host.find_withtag('task-transition'))
            app.animate_area_change()
            app.animate_task_rows('fold', row=gid)
            assert not controller.active and host.coords(window) == normal_coords()
            app.tree.selection_set(tid)
            app.tree.focus(tid)
            app.toggle_done()
            root.update()
            assert app.find_item_in_lists(tid)[0]['done'] and (not controller.active)
            checks.append('Abschalten beendet laufende Übergänge; alle drei Zustandsänderungen bleiben ohne Bewegung bedienbar')
            app.settings['animations_enabled'] = True
            app.animate_area_change()
            app.animate_task_rows('fold', row=gid)
            pending = {flight.job for flight in controller.active.values() if flight.job}
            app.cancel_pending_callbacks()
            assert controller.closed and (not controller.active) and (not pending.intersection(root.tk.call('after', 'info')))
            assert not errors, errors
            checks.append('Schließen entfernt alle Übergangsrückrufe')
        finally:
            app.cancel_pending_callbacks()
            app.release_data_lock()
            for job in root.tk.call('after', 'info'):
                root.tk.call('after', 'cancel', job)
            root.destroy()
    args.report.write_text(json.dumps({'produktionstest': True, 'pruefungen': checks, 'restlauf_ms': durations, 'tatsaechliche_dauer_ms': finished_durations, 'fehler': errors}, ensure_ascii=False, indent=2) + '\n')
    print('\n'.join(checks))
    print('Restlaufzeiten:', [round(v, 2) for v in durations])
    print('Tatsächliche Übergangsabschlüsse:', [round(v, 2) for v in finished_durations])

def flaeche(app_path, report, *, gross=False, tempo=False):
    from types import SimpleNamespace
    args = SimpleNamespace(app=app_path, report=report, gross=gross, tempo=tempo)
    import importlib.machinery, importlib.util, json, os, sys, tempfile, time
    from pathlib import Path
    from datetime import date, timedelta
    sys.path.insert(0, str(args.app.parent))
    out = []
    errors = []
    with tempfile.TemporaryDirectory(prefix='glide-flaechen3380-') as data:
        os.environ['GLIDE_DATA_DIR'] = data
        os.environ['GLIDE_TEST_MODE'] = '1'
        loader = importlib.machinery.SourceFileLoader('glide_flaeche3380', str(args.app))
        m = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
        sys.modules[loader.name] = m
        loader.exec_module(m)
        if args.gross:
            Path(m.SETTINGS_FILE).write_text(json.dumps({'ui_font_size': 'gross'}))
        root = m.tk.Tk()
        root.report_callback_exception = lambda *e: errors.append(repr(e[1]))
        app = m.ListApp(root)
        app.show_info = app.show_warning = lambda *a, **k: None
        app.show_error = lambda *a, **k: errors.append(str(a))
        app.set_design('light')

        def idle():
            until = time.monotonic() + 0.18
            while time.monotonic() < until:
                root.update_idletasks()
                root.update()
                time.sleep(0.01)
        label = app.new_label_object('Kundenprojekt')
        app.labels.append(label)
        tasks = [app.new_item('Exposé abschließend prüfen', due=(date.today() + timedelta(days=2)).isoformat(), planned_date=date.today().isoformat(), importance=2, estimated_minutes=30, labels=[label['id']]), app.new_item('Besichtigung vorbereiten', due=(date.today() + timedelta(days=4)).isoformat(), planned_date=date.today().isoformat(), estimated_minutes=45)]
        source = app.new_list_object('Projektübersicht', tasks)
        page = app.new_list_object('Projektwissen', [], list_kind='page', rich_note={'text': 'Vermarktung\nDie vereinbarten Schritte sind hier zusammengefasst.\nNächster Termin am Mittwoch.', 'spans': [{'start': 0, 'end': 11, 'tag': 'h1'}], 'links': {}})
        app.lists.extend([source, page])
        app.save_items()
        sid = source['id']
        pid = page['id']
        contexts = [('Liste', lambda: (app.set_active_list(sid), app.workspace.set_mode('list'))), ('Tabelle', lambda: (app.set_active_list(sid), app.set_table_view())), ('Heute', app.set_today_view), ('Demnaechst', app.set_in_progress_view), ('Seiten', lambda: app.set_active_list(pid)), ('Pinnwand', lambda: (app.set_active_list(sid), app.workspace.pin([t['id'] for t in tasks]), app.workspace.set_mode('board')))]
        try:
            for width, height in ((1280, 800), (1280, 840), (860, 700)):
                root.geometry(f'{width}x{height}+20+20')
                idle()
                for name, open_view in contexts:
                    open_view()
                    idle()
                    menu_row = getattr(app, 'custom_menubar', None)
                    if menu_row is not None:
                        assert menu_row.master is app.title_row, 'Windows-Menüs belegen eine zusätzliche Zeile oder verengen die Statuszeile'
                        assert menu_row.winfo_ismapped(), 'Windows-Menüs verschwunden'
                        expected = [title for title, _menu in app.action_menus]
                        assert [button.text for button in app.custom_menu_buttons] == expected
                        for button in app.custom_menu_buttons:
                            assert button.winfo_ismapped(), ('Menüknopf verborgen', button.text)
                            assert button.winfo_rootx() >= app.header_frame.winfo_rootx()
                            assert button.winfo_rootx()+button.winfo_width() <= app.header_frame.winfo_rootx()+app.header_frame.winfo_width()
                            assert button.winfo_width() >= button.winfo_reqwidth(), ('Menüknopf abgeschnitten', button.text)
                        for mnemonic in ('d', 'b', 'a', 'h'):
                            assert root.bind('<Alt-'+mnemonic+'>'), ('Menükürzel fehlt', mnemonic)
                    widgets = {}
                    for key in ('header_frame', 'content_toolbar', 'main_area', 'content_frame', 'input_frame', 'search_frame', 'tool_band', 'list_frame_outer', 'tree', 'home_frame', 'sidebar_shell', 'add_button', 'advanced_add_button', 'list_view_button', 'table_button', 'board_button', 'search_entry', 'entry', 'title_row', 'subtitle_row', 'page_chip_row', 'header_controls', 'title_block'):
                        w = getattr(app, key, None)
                        if w is not None and w.winfo_exists():
                            widgets[key] = {'sichtbar': bool(w.winfo_ismapped()), 'manager': w.winfo_manager(), 'x': w.winfo_rootx() - root.winfo_rootx(), 'y': w.winfo_rooty() - root.winfo_rooty(), 'breite': w.winfo_width(), 'hoehe': w.winfo_height(), 'wunschbreite': w.winfo_reqwidth(), 'wunschhoehe': w.winfo_reqheight()}
                    surface = app.rich_note_editor.title_label if name == 'Seiten' else app.workspace.canvas if name == 'Pinnwand' else app.tree
                    content_y = surface.winfo_rooty() - root.winfo_rooty()
                    assert surface.winfo_ismapped(), (name, 'Inhalt unsichtbar')
                    if name in ('Liste', 'Tabelle'):
                        assert app.input_frame.winfo_ismapped(), (name, 'Eingabe verloren')
                    record = {'tatsaechlicher_inhalt': content_y, 'anteil_tatsaechlich': content_y / root.winfo_height(), 'ansicht': name, 'fenster': [root.winfo_width(), root.winfo_height()], 'schrift': app.settings.get('ui_font_size'), 'widgets': widgets, 'inhalt_oberkante': widgets['list_frame_outer']['y'], 'anteil_bis_inhalt': widgets['list_frame_outer']['y'] / root.winfo_height()}
                    print("Geometrie-Einzelmessung:", json.dumps(
                        dict(record, tk_scaling=float(root.tk.call("tk", "scaling")),
                             standardfont=root.tk.call("font", "actual", "TkDefaultFont")),
                        ensure_ascii=False, sort_keys=True), flush=True)
                    if width == 1280 and (not args.gross):
                        assert content_y <= 120, (name, content_y, '15 Prozent überschritten')
                    out.append(record)
            assert not errors, errors
        finally:
            app.cancel_pending_callbacks()
            app.release_data_lock()
            for job in root.tk.call('after', 'info'):
                root.tk.call('after', 'cancel', job)
            root.destroy()
    args.report.write_text(json.dumps({'produktionstest': True, 'messungen': out, 'fehler': errors}, ensure_ascii=False, indent=2) + '\n')
    for r in out:
        print(r['ansicht'], r['fenster'], r['tatsaechlicher_inhalt'], round(r['anteil_tatsaechlich'] * 100, 1), '%')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app",type=Path,default=Path(__file__).resolve().parents[2]/"src/glide/app.pyw")
    parser.add_argument("--fall",choices=("inspektor","klicks","bewegung","flaeche","alle"),default="alle")
    parser.add_argument("--tempo",action="store_true")
    args=parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="glide-aufgaben3380-nachweise-") as folder:
        for name,probe in (("inspektor",inspektor),("klicks",klicks),("bewegung",bewegung),("flaeche",flaeche)):
            if args.fall not in (name,"alle"):
                continue
            for gross in ((False,True) if name=="flaeche" else (False,)):
                report=Path(folder)/(name+("-gross" if gross else "")+".json")
                probe(args.app,report,gross=gross,tempo=args.tempo)
                evidence=json.loads(report.read_text())
                assert not evidence["fehler"],evidence["fehler"]
                print("OK",name,"große Schrift" if gross else "",len(evidence.get("pruefungen",evidence.get("messungen",[]))))
                if name=="bewegung":
                    print("Tatsächliche Übergangsdauer ms:",evidence["tatsaechliche_dauer_ms"])
                if name=="flaeche":
                    print("Geometrie-Nachweis:",json.dumps(evidence,ensure_ascii=False,sort_keys=True))
    print("test_aufgaben3380: OK")

if __name__=="__main__":
    main()
