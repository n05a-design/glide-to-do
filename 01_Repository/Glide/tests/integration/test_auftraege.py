"""FP-06: fünf lokale Aufträge über Dialog, Datei, Kopierweg und alte Importer."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import traceback
from unittest.mock import patch

from test_schutzrunde import Lauf

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'src/glide'))


def widgets(widget):
    for child in widget.winfo_children():
        yield child
        yield from widgets(child)


def button(dialog, label):
    return next(w for w in widgets(dialog) if getattr(w, 'text', None) == label)


def choice(run, dialog, part):
    return next(w for w in widgets(dialog) if isinstance(w, run.mod.AppOptionMenu)
                and any(part in v for v in w.options))


def seed(run):
    app = run.app
    item = app.new_item('Reise vorbereiten', description='Originalbeschreibung.')
    done = app.new_item('Schon erledigt', done=True)
    source = app.new_list_object('Planung', [item, done], note='Tickets kaufen und Hotel wählen.')
    other = app.new_list_object('Privat', [app.new_item('Nicht mitgeben')])
    app.lists.extend([source, other]); assert app.save_items()
    app.set_active_list(source['id']); run.idle()
    return source['id'], item['id'], done['id']


def fall_dateien(run):
    source, *_ = seed(run); app = run.app
    presets = app.exchange_recipe_catalog()
    before = copy.deepcopy(app.lists)
    for recipe in presets:
        target = Path(run.data).parent / (recipe['id'] + '.json')
        def modal(dialog, *args, **kwargs):
            dialog.geometry('660x620+20+20'); dialog.update_idletasks(); dialog.update()
            menu = choice(run, dialog, 'Mitgeliefert')
            menu.variable.set(next(v for v in menu.options if v.endswith(' · ' + recipe['title'])))
            purpose = choice(run, dialog, 'Kontextpaket')
            assert ('Kontextpaket' in purpose.variable.get()) == (recipe['mode'] == 'patch')
            dialog.update_idletasks(); dialog.update()
            for field in (menu, purpose):
                host = field.master
                while not isinstance(host, run.mod.tk.Canvas):
                    host = host.master
                assert field.arrow.winfo_rootx() + field.arrow.winfo_width() <= host.winfo_rootx() + host.winfo_width(), 'Auswahlpfeil außerhalb des sichtbaren Bereichs'
            for label in ('Abbrechen', 'In Zwischenablage kopieren', 'Speichern'):
                w = button(dialog, label)
                assert w.winfo_rooty() + w.winfo_height() <= dialog.winfo_rooty() + dialog.winfo_height()
            if recipe['id'] == 'summarize' and getattr(run, 'capture', None):
                dialog.update_idletasks(); dialog.update()
                if sys.platform == 'win32':
                    sys.path.insert(0, str(REPO / 'tests/tools'))
                    from releasedaten import save_windows_screenshot
                    save_windows_screenshot(dialog, run.capture)
            button(dialog, 'Speichern').command()
        app.run_modal = modal
        with patch.object(run.mod.filedialog, 'asksaveasfilename', return_value=str(target)):
            app.show_exchange_export_dialog()
        payload = json.loads(target.read_text(encoding='utf-8'))
        text = payload['instructions' if recipe['mode'] == 'patch' else 'notes']
        assert recipe['instruction'] in text
        assert 'Nicht mitgeben' not in json.dumps(payload, ensure_ascii=False)
        if recipe['mode'] == 'create':
            _, report = app.parse_exchange_document(json.dumps(payload))
            assert not report.errors and not report.unknown_fields, (report.errors, report.unknown_fields)
        else:
            assert len(payload['items']) == 2 and payload['items'][0]['base']
    assert app.lists == before, 'Bereitstellen verändert Listen/Punkte'


def fall_kopieren_ohne_auftrag(run):
    source, item, _ = seed(run); app = run.app
    captured = []
    def modal(dialog, *args, **kwargs):
        menu = choice(run, dialog, 'Mitgeliefert')
        assert menu.variable.get() == 'Ohne Auftrag'
        button(dialog, 'In Zwischenablage kopieren').command()
        plain = json.loads(captured[-1])
        expected = app.build_exchange_payload(lists=[app.current_list()], folders=[])
        assert plain == expected
        menu.variable.set(next(v for v in menu.options if v.endswith(' · Beschreibung zusammenfassen')))
        button(dialog, 'In Zwischenablage kopieren').command()
        packaged = json.loads(captured[-1]); expected = app.build_exchange_context([app.current_list()])
        assert packaged['items'] == expected['items']
        assert packaged['instructions'].startswith(expected['instructions'])
        purpose = choice(run, dialog, 'Kontextpaket')
        purpose.variable.set(purpose.options[0])
        assert menu.variable.get() == 'Ohne Auftrag'
        dialog.destroy()
    app.run_modal = modal
    with patch.object(app.root, 'clipboard_clear') as clear, patch.object(app.root, 'clipboard_append', side_effect=captured.append):
        app.show_exchange_export_dialog()
    assert clear.call_count == 2 and len(captured) == 2


def fall_eigener_neustart_backup(run):
    seed(run); app = run.app
    def modal(dialog, *args, **kwargs):
        if dialog.title() == 'Eigener Auftrag':
            entry = next(w for w in widgets(dialog) if isinstance(w, run.mod.tk.Entry))
            entry.insert(0, 'Meine Zusammenfassung')
            text = next(w for w in widgets(dialog) if isinstance(w, run.mod.tk.Text))
            text.insert('1.0', 'Kürze nur die Zusammenfassung und erhalte den Originaltext.')
            button(dialog, 'Speichern').command()
            assert app.settings.get('exchange_recipes'), (
                'Eigener Auftrag nicht gespeichert', getattr(app, '_data_read_only', None),
                [w.cget('text') for w in widgets(dialog) if isinstance(w, run.mod.tk.Label)] if dialog.winfo_exists() else 'geschlossen')
        else:
            button(dialog, 'Eigenen Auftrag bearbeiten').command()
            menu = choice(run, dialog, 'Mitgeliefert')
            assert 'Eigener · Meine Zusammenfassung' == menu.variable.get(), (menu.variable.get(), app.settings.get('exchange_recipes'), run.meldungen)
            dialog.destroy()
    app.run_modal = modal
    app.show_exchange_export_dialog()
    own = copy.deepcopy(app.settings['exchange_recipes'])
    assert len(own) == 1
    run.neustart(); app = run.app
    assert app.settings['exchange_recipes'] == own
    backup = app.app_backup_payload()
    section = app.app_backup_section(json.loads(json.dumps(backup)))
    assert section['settings']['exchange_recipes'] == own
    assert app.save_exchange_recipe(own[0], remove=True)
    assert not app.settings['exchange_recipes']
    app.restore_app_backup_extras(section, settings=True)
    assert app.settings['exchange_recipes'] == own
    app.run_modal = lambda dialog, *a, **k: button(dialog, 'Löschen').command()
    assert app.edit_exchange_recipe(own[0]) == {}
    assert not app.settings['exchange_recipes']


def fall_musterantworten(run):
    source, item_id, done_id = seed(run); app = run.app
    samples = {
        'split-note': dict(format='glide.exchange', format_version=2, mode='create', lists=[dict(key='note', title='Aus Notiz', items=[dict(type='task', title='Tickets kaufen')])]),
        'plan-project': dict(format='glide.exchange', format_version=2, mode='create', lists=[dict(key='plan', title='Projektplan', items=[dict(type='task', title='Hotel wählen', estimated_minutes=30)])]),
        'summarize': {'description': 'Zusammenfassung.\n\nOriginaltext:\nOriginalbeschreibung.'},
        'prioritize': {'importance': 3, 'description': 'Begründung: Vorbereitung.\n\nOriginalbeschreibung.'},
        'suggest-labels': {'labels': ['Reise']},
    }
    label = app.ensure_label_by_name('Reise')
    app.find_item_in_lists(item_id)[0]['labels'] = [label['id']]; assert app.save_items()
    for recipe in app.exchange_recipe_catalog():
        before = copy.deepcopy(app.lists); depth = len(app.undo_stack)
        if recipe['mode'] == 'create':
            payload, report = app.parse_exchange_document(json.dumps(samples[recipe['id']]))
            assert not report.errors and not report.unknown_fields
            app.apply_exchange_payload(payload)
            assert len(app.lists) == len(before) + 1
        else:
            # Ein Labelvorschlag braucht tatsächlich eine andere erlaubte Auswahl.
            if recipe['id'] == 'suggest-labels':
                app.find_item_in_lists(item_id)[0]['labels'] = []; assert app.save_items()
                app.find_item_in_lists(done_id)[0]['labels'] = [label['id']]; assert app.save_items()
                before = copy.deepcopy(app.lists)
            context_ids = {item_id, done_id} if recipe['id'] == 'suggest-labels' else {item_id}
            context = app.build_recipe_exchange([app.current_list()], mode='patch', recipe=recipe, item_ids=context_ids)
            if recipe['id'] == 'suggest-labels':
                assert any('Reise' in row['fields']['labels'] for row in context['items'])
            row = context['items'][0]
            reply = dict(format='glide.exchange', format_version=2, mode='patch', changes=[dict(ref=row['ref'], base=row['base'], set=samples[recipe['id']])])
            preview, index = app.check_exchange_patch(reply)
            assert all(v['status'] == 'ok' for v in preview), preview
            app.apply_exchange_patch(preview, index)
            if recipe['id'] == 'summarize':
                assert app.find_item_in_lists(item_id)[0]['description'].endswith('Originalbeschreibung.')
        assert len(app.undo_stack) == depth + 1
        app.undo_last_change(); run.idle()
        assert app.lists == before


def fall_fehler_scope(run):
    source, item, done = seed(run); app = run.app
    recipe = app.exchange_recipe_catalog()[2]
    payload = app.build_recipe_exchange([app.current_list()], mode='patch', recipe=recipe, item_ids={item})
    assert len(payload['items']) == 1
    payload = app.build_recipe_exchange([app.current_list()], mode='patch', include_done=False)
    assert len(payload['items']) == 1 and payload['items'][0]['fields']['title'] == 'Reise vorbereiten'
    own = {**recipe, 'id': 'own-test', 'title': 'Mein Auftrag'}
    before = copy.deepcopy(app.settings)
    disk = Path(run.mod.SETTINGS_FILE).read_bytes()
    with patch.object(app, 'write_json_atomic', side_effect=OSError('Prüffehler')):
        assert not app.save_exchange_recipe(own)
    assert app.settings == before and Path(run.mod.SETTINGS_FILE).read_bytes() == disk
    app._data_read_only = True
    with patch.object(app, 'refresh_data_lock'):
        assert not app.save_exchange_recipe(own)
    app._data_read_only = False
    cancelled = Path(run.data).parent / 'nicht-geschrieben.json'
    app.run_modal = lambda d, *a, **k: (button(d, 'Speichern').command(), d.destroy())
    with patch.object(app, 'output_editor_ready', return_value=False), patch.object(run.mod.filedialog, 'asksaveasfilename', return_value=str(cancelled)):
        app.show_exchange_export_dialog()
    assert not cancelled.exists()


def fall_vorschau(run):
    source, item, done = seed(run); app = run.app
    instruction = ('Lange Anweisung mit Umlauten und genauem Kontext. ' * 40) + 'ENDE-DER-ANWEISUNG'
    before = copy.deepcopy(app.lists)
    previews = []
    for mode in ('create', 'patch'):
        recipe = dict(id='preview-' + mode, title='Vorschau ' + mode, mode=mode, instruction=instruction)
        assert app.save_exchange_recipe(recipe)
        def modal(dialog, *args, **kwargs):
            if dialog.title() == 'Vorschau für KI':
                dialog.geometry('860x700+20+20'); dialog.update_idletasks(); dialog.update()
                text = next(w for w in widgets(dialog) if w.winfo_name() == 'exchange_preview')
                assert text.cget('state') == 'disabled'
                shown = text.get('1.0', 'end-1c')
                instructions, context = shown.split('\n\nKontext und Paketdaten\n\n', 1)
                payload = json.loads(context)
                assert instruction in instructions and 'ENDE-DER-ANWEISUNG' in instructions
                assert 'Nicht mitgeben' not in text.get('1.0', 'end-1c')
                if mode == 'patch':
                    assert {row['ref'] for row in payload['items']} == {
                        row['ref'] for row in app.build_recipe_exchange([app.current_list()], mode='patch', recipe=recipe)['items']}
                close = button(dialog, 'Schließen')
                assert close.winfo_rooty() + close.winfo_height() <= dialog.winfo_rooty() + dialog.winfo_height()
                text.yview_moveto(1); dialog.update_idletasks()
                assert text.yview()[1] > .99, 'vollständiges Paket nicht bis zum Ende scrollbar'
                if getattr(run, 'capture', None) and mode == 'patch' and sys.platform == 'win32':
                    sys.path.insert(0, str(REPO / 'tests/tools'))
                    from releasedaten import save_windows_screenshot
                    save_windows_screenshot(dialog, run.capture)
                previews.append(payload); dialog.destroy(); return
            menu = choice(run, dialog, 'Mitgeliefert')
            menu.variable.set(next(v for v in menu.options if v.endswith(' · ' + recipe['title'])))
            dialog.update_idletasks(); dialog.update()
            button(dialog, 'Vorschau').command()
            dialog.destroy()
        app.run_modal = modal
        with patch.object(run.mod.filedialog, 'asksaveasfilename') as picker, patch.object(run.root, 'clipboard_clear') as clipboard:
            app.show_exchange_export_dialog()
            picker.assert_not_called(); clipboard.assert_not_called()
    assert len(previews) == 2 and app.lists == before


CASES = ('dateien', 'kopieren_ohne_auftrag', 'eigener_neustart_backup', 'musterantworten', 'fehler_scope', 'vorschau')


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--app', type=Path, default=REPO / 'src/glide/app.pyw')
    parser.add_argument('--report', type=Path); parser.add_argument('--capture', type=Path); parser.add_argument('--fall', choices=CASES)
    args = parser.parse_args(); report = dict(app_sha256=hashlib.sha256(args.app.read_bytes()).hexdigest(), faelle={})
    for name in ([args.fall] if args.fall else CASES):
        run = None
        with tempfile.TemporaryDirectory(prefix='glide-fp06-') as directory:
            try:
                run = Lauf(args.app, str(Path(directory) / 'daten')); run.capture = args.capture
                globals()['fall_' + name](run)
                assert not run.errors, run.errors
                report['faelle'][name] = dict(ok=True); print('OK', name, flush=True)
            except Exception:
                error = traceback.format_exc().replace(str(Path.home()), '~')[-2000:]
                report['faelle'][name] = dict(ok=False, fehler=error); print('ROT', name, error, flush=True)
            finally:
                if run: run.ende()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return int(any(not v['ok'] for v in report['faelle'].values()))


if __name__ == '__main__':
    raise SystemExit(main())
