"""U01/U02/U13/U14/U16/U22/U24: gemeinsame echte Bedienwege und Neustart."""
import argparse
import copy
from datetime import date
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--app', type=Path, default=REPO / 'src/glide/app.pyw')
parser.add_argument('--report', type=Path)
parser.add_argument('--capture', type=Path)
parser.add_argument('--observe', action='store_true')
parser.add_argument('--counterprobe', action='store_true')
args = parser.parse_args()
sys.path.insert(0, str(REPO / 'tests/tools'))

with tempfile.TemporaryDirectory(prefix='glide-bedienung-') as data:
    os.environ['GLIDE_DATA_DIR'] = data
    os.environ['GLIDE_TEST_MODE'] = '1'
    loader = importlib.machinery.SourceFileLoader('glide_bedienung', str(args.app.resolve()))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    if args.counterprobe:
        available = hasattr(mod.ListApp, 'toggle_view_hints')
        result = dict(version=mod.APP_VERSION, exitcode=0 if available else 1,
                      remembered_hints=available, app_sha256=hashlib.sha256(args.app.read_bytes()).hexdigest())
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(result, indent=2), encoding='utf-8')
        print(result)
        raise SystemExit(result['exitcode'])
    errors, observations, checks = [], [], []
    root = mod.tk.Tk()
    root.geometry('1280x800+20+20')
    root.report_callback_exception = lambda *exc: errors.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_warning = app.show_error = lambda *a, **kw: errors.append(repr(a))
    def idle():
        for _ in range(3):
            root.update_idletasks(); root.update()
    def stop():
        app.cancel_pending_callbacks(); app.release_data_lock()
        for job in root.tk.call('after', 'info'):
            root.tk.call('after', 'cancel', job)
        root.destroy()
    try:
        point = app.new_item('Kundenangebot prüfen', due='2026-10-12', planned_date='2026-10-09')
        entry = app.new_list_object('Planung und tägliche Arbeit', [point])
        app.lists.append(entry); app.save_items(); app.set_active_list(entry['id']); idle()
        original = copy.deepcopy(app.lists)
        for size in ('mittel', 'gross'):
            for design in ('light', 'dark'):
                app.set_design(design, apply_now=False)
                app.settings['ui_font_size'] = size
                app.apply_ui_font(); app.apply_theme()
                for width, height in ((1280, 800), (860, 700)):
                    root.geometry(f'{width}x{height}+20+20')
                    for view in ('list', 'library'):
                        app.set_active_list(entry['id']) if view == 'list' else app.set_library_view()
                        idle()
                        observations.append(dict(width=width, height=height, size=size, design=design,
                            view=view, header_height=app.header_frame.winfo_height(),
                            visible_buttons=len(app.header_controls.pack_slaves())))
                        if not args.observe:
                            assert len(app.header_controls.pack_slaves()) <= 4
                            if view == "library":
                                assert app.header_note_text() == ""
                                assert not any(getattr(w, "_header_note", None) for w in app.page_chip_row.winfo_children())
                            assert not app.print_button.winfo_manager() and not app.history_button.winfo_manager()
                            if view == 'list':
                                value = app.tree.set(point['id'], 'due')
                                assert app.format_due_column(point['planned_date']) in value, value
                                assert app.format_due_column(point['due']) in value, value
                                assert 'due' in app.tree.cget('displaycolumns'), 'Datum bleibt bei Mindestgröße sichtbar'
                                assert not app.hint_label.winfo_ismapped()
                            else:
                                button = app.library_open_buttons[('list', entry['id'])]
                                root.focus_force(); button.focus_set(); idle()
                                button.event_generate('<Return>'); idle()
                                assert app.active_list_id == entry['id'] and app.view_mode == 'list'
                                app.set_library_view(); idle()
                        if args.capture and size == 'gross':
                            from releasedaten import save_windows_screenshot
                            args.capture.mkdir(parents=True, exist_ok=True)
                            save_windows_screenshot(root, args.capture / f'{view}_{width}_{design}.png')
        if not args.observe:
            app.set_active_list(entry['id']); idle()
            undo_count = len(app.undo_stack)
            app.hints_button.command(); idle()
            assert app.hint_label.winfo_ismapped()
            assert len(app.undo_stack) == undo_count and app.lists == original
            app.hints_button.command(); idle()
            assert not app.hint_label.winfo_ismapped()
            with patch.object(app, 'save_settings', return_value=False):
                app.toggle_view_hints()
            assert not app.settings['view_hints']['list']
            app.toggle_view_hints(); idle()
            checks.append('Hinweise: echte Schaltfläche, keine Aufgabenänderung, Schreibfehler rücknehmbar')
            # Dieselbe Palette mit einem Editor als ursprünglichem Fokus.
            editor = mod.tk.Text(root, undo=True)
            editor.pack(); editor.insert('1.0', 'Auswahl'); editor.tag_add('sel', '1.0', 'end-1c')
            editor.focus_set(); root.focus_force(); idle()
            app._actions_source_focus = editor
            app.show_actions_dialog(); idle()
            assert not root.grab_current(), 'Palette ist eingebettet und nicht modal'
            state = app._quick_open
            state['entry'].delete(0, 'end'); state['entry'].insert(0, '> Kopieren'); idle()
            hits = state['results']
            index = next(i for i, hit in enumerate(hits) if hit['target'][1]['id'] == 'copy_selected_to_clipboard')
            state['tree'].selection_set(str(index))
            state['entry'].event_generate('<Return>'); idle()
            assert root.clipboard_get() == 'Auswahl'
            editor.destroy()
            checks.append('Gemeinsame Palette: Aktion über echte Eingabe/Enter mit Editorfokus')
            menus = app.menubar_structure()
            assert any(row and row[0] == 'Papierkorb leeren' for row in dict(menus)['Bearbeiten'])
            assert not any(row and row[0] in ('Papierkorb leeren', 'Systemmitteilung testen')
                           for row in dict(menus)['Ansicht'])
            assert app.ITEM_KIND_LABELS[app.ITEM_KIND_LONG] == 'Langtext'
            assert app.ICONS['inbox'] != app.ICONS['move_down']
            assert app.ICONS['overdue'] != app.ICONS['move_up']
            assert app.ICONS['timer'] != app.ICONS['history']
            symbols = {}
            for key, value in app.ICONS.items():
                symbols.setdefault(value, set()).add(key)
            duplicate_roles = {frozenset(keys) for keys in symbols.values() if len(keys) > 1}
            assert duplicate_roles <= {frozenset(('move_up','sort_ascending')), frozenset(('move_down','sort_descending'))}
            actions = app.app_action_entries()
            assert not [a for a in actions if a['group'] == 'Weitere Aktionen']
            app.apply_reminder_badge(1); idle()
            assert app.notifications_button.winfo_ismapped() and len(app.header_controls.pack_slaves()) <= 4
            app.apply_reminder_badge(0); idle()
            assert not app.notifications_button.winfo_ismapped()
            app.save_settings()
        assert not errors, errors
        result = dict(version=mod.APP_VERSION, app_sha256=hashlib.sha256(args.app.read_bytes()).hexdigest(),
                      observations=observations, checks=checks, callback_errors=errors, exitcode=0)
    finally:
        stop()
    if not args.observe:
        root = mod.tk.Tk(); root.withdraw(); app = mod.ListApp(root)
        try:
            assert app.settings['view_hints']['list'] is True, 'Hinweise bleiben nach Neustart gespeichert'
            assert app.find_item_in_lists(point['id'])[0]['due'] == point['due']
            assert app.find_item_in_lists(point['id'])[0]['planned_date'] == point['planned_date']
            result['checks'].append('Neustart: gemerkte Hinweise und getrennte Datumsfelder')
        finally:
            stop()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print('OK: Bedienkomfort, 16 Layoutkombinationen, Palette/Editorfokus, Hinweise/Neustart, Bibliothek, Datum und Menüs')
