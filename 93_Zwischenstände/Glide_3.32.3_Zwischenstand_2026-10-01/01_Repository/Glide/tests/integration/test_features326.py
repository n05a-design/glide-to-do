"""Regressionen aus der 3.26-Nachprüfung; ausschließlich isolierte Testdaten."""
import copy
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import tempfile

REPO = Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory(prefix='glide326-') as isolated:
    os.environ['GLIDE_DATA_DIR'] = isolated
    os.environ['GLIDE_TEST_MODE'] = '1'
    loader = importlib.machinery.SourceFileLoader('glide326', str(REPO/'src/glide/app.pyw'))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.withdraw()
    errors = []
    root.report_callback_exception = lambda *args: errors.append(args)
    app = mod.ListApp(root)
    app.show_info = app.show_warning = app.show_error = lambda *a, **k: None
    try:
        root.update()
        original_refresh = app.refresh_tree
        refreshes = []
        app.refresh_tree = lambda *a, **k: refreshes.append(1)
        for index in range(10):
            app.search_var.set(str(index))
        assert not refreshes
        root.update()
        assert len(refreshes) == 1, refreshes
        app.refresh_tree = original_refresh
        app.search_var.set('')
        root.update()
        manual = app.MANUAL_SECTIONS
        app.MANUAL_SECTIONS = (('<Probe>', (('A & B', '<script>', 'Lokal'),)),)
        exported = app.manual_html()
        assert '&lt;Probe&gt;' in exported and '<script>' not in exported
        app.MANUAL_SECTIONS = manual
        original_events, original_feedback = app.history_events, app.feedback
        original_level, original_animations = app.action_feedback_level, app.animations_enabled
        signals = []
        app.feedback = lambda key, count=1: signals.append((key, count))
        app.action_feedback_level = lambda: 'all'
        app.animations_enabled = lambda: True
        for field, key in [('labels', 'labelled'), ('due', 'due_set'), ('planned_date', 'planned')]:
            app.history_events = lambda *a, field=field: [{'action':'updated', 'fields':[app.HISTORY_FIELD_NAMES[field]]}]
            app.feedback_for_changes({})
            assert signals[-1] == (key, 1)
        app.animations_enabled = lambda: False
        count = len(signals)
        app.feedback_for_changes({})
        assert len(signals) == count
        app.history_events, app.feedback = original_events, original_feedback
        app.action_feedback_level, app.animations_enabled = original_level, original_animations
        assert app.mascot_name() == 'Gismo'
        app.settings['mascot_name'] = 'Mika'
        assert app.mascot_name() == 'Mika'
        for design in ('minimal_light', 'minimal_dark'):
            app.set_design(design, apply_now=False)
            app.settings['accent_color'] = 'muted'
            theme = app.active_theme()
            assert theme['ui_accent'] == theme['text']
            assert mod.contrast_ratio(theme['selection'], theme['selection_text']) >= 4.5
            assert app.normalize_personal_settings(app.settings)['accent_color'] == 'muted'
            app.settings['accent_color'] = 'clear'
            assert app.active_theme()['ui_accent'] != theme['ui_accent']
        for raw, expected in [('Reiter …', 'Reiter'), ('Punkte anheften ...', 'Anheften'),
                              ('Weitere Aktionen …', 'Aktionen'), ('…', 'Mehr')]:
            assert mod.RoundedButton.action_text(raw) == expected
        preview = mod.BoardPreview(root, '#000000', '#222222', '#aaaaaa', '#ffffff')
        preview.set_content([], [])
        assert not preview.find_all()
        cards = [{'item_id': str(i), 'x': (i%3)*316, 'y': (i//3)*268} for i in range(205)]
        app.settings['pinboards']['global'] = {'cards': cards, 'connections': [], 'layout': 'free'}
        original = copy.deepcopy(app.settings['pinboards']['global'])
        boxes, links, total = app.global_board_preview()
        assert total == 205 and len(boxes) == app.HOME_BOARD_PREVIEW_CARDS
        assert app._home_preview_condensed and original == app.settings['pinboards']['global']
        preview.set_content(boxes, links)
        fit = preview._fitted(425, 140)
        assert min(b[2] for b in fit) > 25 and min(b[3] for b in fit) > 12
        assert all(preview.type(i) == 'rectangle' for i in preview.find_all())
        a, b, c = [app.new_item(t) for t in ('A', 'B', 'C')]
        entry = app.new_list_object('Verbindungen', [a,b,c]);app.lists.append(entry)
        app.set_active_list(entry['id'])
        ws = app.workspace
        ws.pin([a['id'],b['id'],c['id']]);ws.set_mode('board');root.update()
        ws.configure_board('connection_style', 'forward')
        ws.toggle_connection(a['id'], b['id']);ws.toggle_connection(b['id'], c['id'])
        ws.selected_ids = [a['id'],b['id']];ws.selected_id = b['id']
        ws.configure_board('connection_style','backward')
        edges = ws.board()['connections']
        assert edges[0]['style'] == 'backward' and edges[1]['style'] == 'forward', edges
        assert len(ws.canvas.find_withtag('connection')) == 2
        # Lasso selects fully enclosed cards; partial overlap alone is excluded.
        from types import SimpleNamespace
        ws.store_position(a['id'], 100, 100)
        ws.store_position(b['id'], 700, 100)
        ws.store_position(c['id'], 700, 700)
        root.update()
        ws.canvas.xview_moveto(0);ws.canvas.yview_moveto(0)
        def event(x, y, state=0):
            return SimpleNamespace(x=x-ws.canvas.canvasx(0), y=y-ws.canvas.canvasy(0), state=state)
        ax, ay, aw, ah = ws.card_boxes[a['id']]
        ws.card_press(event(70,70))
        ws.card_motion(event(ax+aw+5, ay+ah+5))
        assert ws.canvas.find_withtag('layer:interaction')
        ws.card_release(event(ax+aw+5, ay+ah+5))
        assert ws.selection() == [a['id']], ws.selection()
        assert not ws.canvas.find_withtag('layer:interaction')
        ws.configure_board('object_snap', True)
        assert app.normalize_personal_settings(app.settings)['pinboards'][ws.context()]['object_snap']
        assert ws.canvas.find_withtag('layer:cards') and ws.canvas.find_withtag('layer:labels')
        original_positions = copy.deepcopy(ws.board()['cards'])
        ws.configure_board('zoom',100);root.update()
        base_box = ws.card_boxes[a['id']]
        base_print_geometry = ws.board_print_geometry()
        for percent in (50,75,100,125,150,200):
            ws.configure_board('zoom', percent);root.update()
            factor = percent/100
            assert ws.board()['cards'] == original_positions
            assert all(abs(actual-expected*factor)<0.01 for actual, expected in zip(ws.card_boxes[a['id']], base_box))
            assert ws.canvas.find_withtag('connection')
            assert ws.board_print_geometry() == base_print_geometry
            assert '<html lang="de">' in ws.build_board_print_html()
            assert app.normalize_personal_settings(app.settings)['pinboards'][ws.context()]['zoom'] == percent
        ws.configure_board('zoom',100)
        ws.configure_board('navigator', True);root.update()
        assert ws.navigator.find_withtag('map:viewport')
        assert len(ws.navigator.find_withtag('map:card')) == len(ws.card_boxes)
        ws.navigate_board(SimpleNamespace(x=155, y=95))
        assert ws.board()['cards'] == original_positions
        ws.configure_board('navigator', False);root.update()
        assert not ws.navigator.winfo_manager()
        # Defense at the mutation boundary: even a faulty form cannot create a foreign task.
        folder = app.new_folder_object('Ordner')
        app.folders.append(folder)
        inside = app.new_list_object('Innen', [], folder_id=folder['id']);app.lists.append(inside)
        outside = app.new_list_object('Außen', []);app.lists.append(outside)
        app.set_active_folder(folder['id']);ws.set_mode('board');root.update()
        captured = {}
        def form(*args, **kwargs):
            captured.update(kwargs)
            return {'text':'Falsch', 'kind':'task','list_id':outside['id']}
        app.new_item_dialog = form
        ws.create_card_item(20,20)
        assert captured['allowed_list_ids'] == {inside['id']}
        assert outside['items'] == [] and inside['items'] == []
        def valid(*args, **kwargs):
            return {'text':'Richtig', 'kind':'task', 'list_id':inside['id']}
        app.new_item_dialog = valid
        ws.create_card_item(20,20)
        assert [i['text'] for i in inside['items']] == ['Richtig']
        assert len(ws.board()['cards']) == 1
        # Hybrid note list: formatting, Unicode positions, local undo and saved data.
        note = app.new_list_object('Notizprobe', [app.new_item('Aufgabe oben')], list_kind='note')
        app.lists.append(note); app.set_active_list(note['id']);root.update()
        editor = app.rich_note_editor
        editor.text.insert('1.0', 'Hallo Welt\nZweite Zeile 😀 Ende')
        editor.flush()
        editor.text.tag_add('sel', '1.0', '1.5');editor.format('bold')
        assert any(span['tag'] == 'bold' for span in note['rich_note']['spans'])
        formatted = copy.deepcopy(note['rich_note'])
        editor.undo();assert note['rich_note']['spans'] == []
        editor.redo();assert note['rich_note'] == formatted
        editor.text.tag_remove('sel', '1.0', 'end')
        editor.text.tag_add('sel', '2.0', '2.6');editor.format('italic')
        expected = copy.deepcopy(note['rich_note'])
        editor.load(expected);assert editor.document() == expected
        assert app.list_text_matches_query(note, 'zweite zeile')
        assert not app.list_text_matches_query(note, 'italic')
        # A failed write is retried even when the user has not typed again.
        callback = editor.on_change
        attempts = []
        editor.on_change = lambda value: attempts.append(copy.deepcopy(value)) or len(attempts) > 1
        editor.text.insert('end-1c', '!')
        assert editor.flush() is False
        assert editor.flush() is True and len(attempts) == 2
        editor.on_change = callback
        editor.load(expected);editor._last = copy.deepcopy(expected)
        app.save_items()
        import json
        stored = json.loads(Path(mod.SAVE_FILE).read_text(encoding='utf-8'))
        restored, _ = app.normalize_lists_data(copy.deepcopy(stored))
        assert next(v for v in restored if v['id'] == note['id'])['rich_note'] == expected
        app.duplicate_list(note['id'])
        duplicate = app.current_list()
        assert duplicate['rich_note'] == expected and duplicate['rich_note'] is not note['rich_note']
        assert duplicate['list_kind'] == 'note'
        scratch = mod.RichNoteEditor(root, app, on_change=lambda document: True)
        plain = {'text':'Übung 😀\nZweite Zeile', 'spans':[], 'links':{}}
        for tag in mod.RichNoteEditor.FORMATS:
            scratch.load(plain);scratch._last = copy.deepcopy(plain)
            scratch._undo.clear();scratch._redo.clear()
            scratch.text.tag_add('sel', '1.0', '1.end')
            scratch.format(tag)
            value = scratch.document()
            assert any(span['tag'] == tag for span in value['spans']), tag
            scratch.load(value);assert scratch.document() == value, tag
            scratch.undo();assert scratch.document() == plain, tag
            scratch.redo();assert scratch.document() == value, tag
        scratch.load(plain);scratch._last = copy.deepcopy(plain)
        scratch.text.tag_add('sel', '1.0', 'end-1c');scratch.format('bullet')
        scratch.text.tag_add('sel', '1.0', 'end-1c');scratch.format('number')
        assert scratch.document()['text'] == '1. Übung 😀\n2. Zweite Zeile'
        scratch.text.tag_add('sel', '1.0', 'end-1c');scratch.format('number')
        assert scratch.document()['text'] == plain['text']
        scratch.destroy()
        # Structured interchange and templates must retain every semantic span.
        payload = app.build_exchange_payload(lists=[note])
        parsed, report = app.parse_exchange_document(json.dumps(payload, ensure_ascii=False))
        assert parsed is not None and not report.errors, report.errors
        imported = app.apply_exchange_payload(parsed)
        assert imported[0]['rich_note'] == expected and imported[0]['list_kind'] == 'note'
        template = app.capture_template(list_id=note['id'])
        assert template['payload']['lists'][0]['rich_note'] == expected
        app.create_list_from_template(template['id'])
        assert app.current_list()['rich_note'] == expected
        # Migration backup contains exactly the old bytes before the first format-17 save.
        old = copy.deepcopy(stored);old['version'] = 16
        original_bytes = json.dumps(old, ensure_ascii=False).encode('utf-8')
        Path(mod.SAVE_FILE).write_bytes(original_bytes)
        app._schema17_backup_checked = False
        assert app.save_items()
        backups = list(Path(mod.BACKUP_DIR).glob('liste_vor_format17_*.json'))
        assert backups and backups[-1].read_bytes() == original_bytes
        assert json.loads(Path(mod.SAVE_FILE).read_text(encoding='utf-8'))['version'] == 20
        from datetime import datetime, timedelta
        now = datetime.now()
        history = [{'id': str(i), 'at': (now-timedelta(minutes=i)).isoformat(),
                    'kind':'item', 'action':'created', 'target':str(i)} for i in range(30)]
        history.append({'id':'old','at':(now-timedelta(days=16)).isoformat(),
                        'kind':'item','action':'created','target':'expired'})
        normalized = app.normalize_history_entries(history)
        assert len(normalized) == 15 and normalized[-1]['id'] == '0'
        assert 'old' not in {v['id'] for v in normalized}
        app._activate_system_view(app.HISTORY_VIEW);root.update()
        assert app.get_display_title() == 'Änderungsverlauf'
        assert app.get_active_page() is None
        assert 'Änderungen' in app.stats_label.cget('text')
        # Seit 27.09.2026 steht der Untertitel in der Kennzahlenzeile unter dem Titel.
        assert 'letzten Änderungen' in app.header_note_text()
        assert not app.system_listbox.exists('smart:history')  # seit 26.09.2026 Kopfzeilenknopf
        assert app.home_content.winfo_children()
        assert not errors, errors
        print('OK 3.26: Vorschau, Verbindungen, Ordnergrenze, Lasso, Zoom, Navigator, Akzente, Gismo, Notizformate/Undo/Speichern/Austausch/Vorlagen, Migration und Verlauf')
    finally:
        app.dirty = False
        app.on_close()
