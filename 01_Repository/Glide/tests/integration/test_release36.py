"""3.6-Rundläufe mit echten Tk-Widgets und ausschließlich temporären Nutzdaten."""
import argparse
import copy
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import tempfile
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--screenshots', type=Path)
args = parser.parse_args()

def children(widget):
    for child in widget.winfo_children():
        yield child
        yield from children(child)

with tempfile.TemporaryDirectory(prefix='glide-release36-') as tmp, tempfile.TemporaryDirectory(prefix='glide-destination36-') as target:
    os.environ['GLIDE_DATA_DIR'] = tmp
    loader = importlib.machinery.SourceFileLoader('glide_release36', str(ROOT/'src/glide/app.pyw'))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.withdraw()
    app = mod.ListApp(root)
    app.confirm_template_preview = lambda template: True
    errors = []
    callback_errors = []
    root.report_callback_exception = lambda *error: callback_errors.append(error)
    app.show_error = lambda *error, **kwargs: errors.append(error)
    app.show_info = lambda *a, **kw: None
    app.show_warning = lambda *a, **kw: None
    app.ask_yes_no = lambda *a, **kw: True
    root.geometry('1280x960+20+20')
    root.deiconify()
    root.update()
    if os.name == 'nt':
        # Seit 3.30 gehören auch die beiden Pixelify-Schnitte zum Paket.
        # Jede ausgelieferte Schrift muss tatsächlich registriert sein;
        # Lizenz- und Herkunftsdateien zählen nicht als Schriftressource.
        font_dir = ROOT / 'src/glide/resources/fonts'
        expected_fonts = {path.resolve() for path in font_dir.iterdir()
                          if path.suffix.lower() in ('.ttf', '.otf')}
        registered_fonts = {Path(path).resolve() for path in app._registered_fonts}
        assert expected_fonts and registered_fonts == expected_fonts, (registered_fonts, expected_fonts)
        assert app.ui_font_family() == 'DejaVu Sans', app.ui_font_family()
        assert 'Pixelify Sans' in app.available_font_families()

    def capture(widget, name):
        if args.screenshots and os.name == 'nt':
            import sys
            sys.path.insert(0, str(ROOT/'tests/tools'))
            from releasedaten import save_windows_screenshot
            widget.update()
            save_windows_screenshot(widget, args.screenshots.resolve()/f'{name}.png')

    folder = app.new_folder_object('Projekt', color='accent')
    empty = app.new_folder_object('Leerer Unterordner', parent_id=folder['id'])
    app.folders.extend([folder, empty])
    label = app.new_label_object('Abnahme', None, 'clear')
    app.labels.append(label)
    item = app.new_item('Prüfen', due='2026-09-10', labels=[label['id']])
    item['description'] = 'Beschreibung bleibt erhalten.'
    item['repeat'] = {'art': mod.ListApp.REPEAT_DAILY, 'start': '2026-09-10', 'ende': None}
    child = app.new_item('Unterpunkt')
    item['children'] = [child]
    source_file = Path(tmp)/'original.txt'
    source_file.write_text('Anhang aus dem Teilbackup', encoding='utf-8')
    # Die Datei wird wie ein bereits gespeicherter lokaler Anhang angelegt.
    storage = 'attachments/release36.txt'
    (Path(tmp)/storage).write_bytes(source_file.read_bytes())
    item['attachments'] = [{'id': 'attachment36', 'name': 'original.txt', 'storage': storage}]
    entry = app.new_list_object('Abnahme', [item], folder_id=folder['id'], color='clear', labels=[label['id']])
    app.lists.append(entry)
    app.set_active_list(entry['id'])
    assert app.save_items()
    payload = app.partial_backup_payload(folder_ids=[folder['id']])
    assert {x['id'] for x in payload['folders']} == {folder['id'], empty['id']}
    assert [x['id'] for x in payload['lists']] == [entry['id']]
    partial = Path(tmp)/'teil.glidebackup'
    app.write_complete_backup(str(partial), payload)
    before_ids = {x['id'] for x in app.lists}
    app.import_full_backup(additive=True, path=str(partial))
    assert not errors, errors
    added = [x for x in app.lists if x['id'] not in before_ids]
    assert len(added) == 1
    restored = added[0]['items'][0]
    assert restored['description'] == item['description']
    assert restored['children'][0]['text'] == child['text']
    assert restored['repeat'] and restored['labels']
    restored_path = app.resolve_attachment_path(restored['attachments'][0])
    assert Path(restored_path).read_bytes() == source_file.read_bytes()
    assert restored['id'] != item['id']
    assert restored['attachments'][0]['storage'] != storage
    assert len([f for f in app.folders if f['title'] == 'Leerer Unterordner']) == 2
    assert before_ids <= {x['id'] for x in app.lists}

    template = app.capture_template(folder_id=folder['id'])
    assert template['payload']['lists'][0]['items'][0]['children']
    original_count = len(app.lists)
    app.create_list_from_template(template['id'])
    assert len(app.lists) == original_count + 1 and not errors, errors
    app.set_template_view()
    app.toggle_template_editing()
    def edit_dialog(dialog, parent=None):
        widgets = list(children(dialog))
        first = next(w for w in widgets if isinstance(w, mod.tk.Entry))
        first.delete(0, 'end'); first.insert(0, 'Geänderte Vorlage')
        next(w for w in widgets if isinstance(w, mod.RoundedButton) and w.text == 'Übernehmen').command()
    app.run_modal = edit_dialog
    app.edit_template(template['id'])
    assert app.template_by_id(template['id'])['title'] == 'Geänderte Vorlage'
    app.toggle_template_editing()
    saved = json.loads(Path(mod.TEMPLATES_FILE).read_text(encoding='utf-8'))
    assert any(t['title'] == 'Geänderte Vorlage' for t in saved['templates'])
    assert not app._templates_editing
    capture(root, 'vorlagen')

    def create_dialog(dialog, parent=None):
        dialog.update()
        widgets = list(children(dialog))
        entries = [w for w in widgets if isinstance(w, mod.tk.Entry)]
        entries[0].insert(0, 'Neue Maske')
        label = app.ensure_label_by_name('Freigabe')
        dropdown = next(w for w in widgets if isinstance(w, mod.LabelDropdown))
        dropdown.labels.append(label) if label not in dropdown.labels else None
        dropdown.set_selected_ids([label['id']])
        next(w for w in widgets if isinstance(w, mod.tk.Text)).insert('1.0', 'Notiz bei Anlage')
        capture(dialog, 'neue-liste')
        next(w for w in widgets if isinstance(w, mod.RoundedButton) and w.text == 'Anlegen').command()
    app.run_modal = create_dialog
    app.create_container_dialog('list', parent_id=folder['id'])
    created = app.current_list()
    assert created['title'] == 'Neue Maske' and created['note'] == 'Notiz bei Anlage'
    assert created['folder_id'] == folder['id'] and created['labels']

    app.settings['week_start'] = 'sunday'
    assert app.calendar_week_start(mod.date(2026,9,9)) == mod.date(2026,9,6)
    app.settings['week_start'] = 'monday'
    assert app.calendar_week_start(mod.date(2026,9,9)) == mod.date(2026,9,7)
    # Punkt 3 (3.23.0): Die Materialoptik ist kein eigener Schalter mehr,
    # sondern Bestandteil des Designs. Geprüft wird deshalb über set_design.
    vorheriges_design = app.design_name()
    app.set_design(app.theme_name, apply_now=False)
    app.settings['accent_color'] = 'clear'
    assert app.glass_enabled() is False
    assert app.active_theme()['selection'] == mod.ensure_contrast(
        app.THEMES[app.theme_name]['clear'], app.active_theme()['selection_text'])
    assert app.active_theme()['accent'] == app.THEMES[app.theme_name]['accent']
    app.set_design(vorheriges_design, apply_now=False)
    app.apply_theme()
    # Umbenennen speichert den Text; Long-Tasks bleiben in der Detailmaske.
    app.set_active_list(entry['id']); app.refresh_tree(); root.update()
    app.tree.selection_set(item['id'])
    app.begin_item_rename(item['id'])
    editor = app._item_rename_entry
    assert editor is not None
    editor.delete(0, 'end'); editor.insert(0, 'Umbenannt')
    root.focus_force(); editor.focus_set(); root.update()
    editor.event_generate('<Return>'); root.update()
    assert app.find_item(item['id'])[0]['text'] == 'Umbenannt'
    # An der Labelgrenze darf ein Artwechsel keine 21. Zuordnung erzeugen.
    boundary_labels = [app.new_label_object(f'Grenze {n}') for n in range(20)]
    app.labels.extend(boundary_labels)
    boundary = app.new_item('Grenzpunkt', labels=[label['id'] for label in boundary_labels])
    original_boundary = copy.deepcopy(boundary)
    assert not app.set_item_kind(boundary, app.ITEM_KIND_LONG)
    assert boundary == original_boundary
    # Ein gültiger 100-Ebenen-Baum darf nicht auf 101 Ebenen eingerückt werden.
    chain = app.new_item('Tiefe 0'); last = chain
    for n in range(1, app.MAX_ITEM_DEPTH):
        node = app.new_item(f'Tiefe {n}'); last['children'] = [node]; last = node
    loose = app.new_item('Außerhalb')
    prior_items = app.items
    app.items = [chain, loose]
    assert app.normalize_items(app.items)
    assert not app.make_subitem(loose['id'], last['id'])
    assert app.items == [chain, loose]
    app.items = prior_items
    # Fehlende oder beschädigte Vorlagenanhänge werden vor dem Import abgelehnt.
    damaged = copy.deepcopy(template); damaged['files'] = {}
    try:
        app.validate_template_payload(damaged)
    except ValueError:
        pass
    else:
        raise AssertionError('Fehlender Vorlagenanhang wurde akzeptiert.')
    saved_templates = app.templates
    app.templates = []
    assert app.home_template_keys() == []
    app.templates = saved_templates
    for theme in ('light','dark'):
        app.set_design(theme, apply_now=False); app.apply_theme(); app.set_home_view(); root.update()
        capture(root, f'startseite-{theme}')
        app.home_canvas.yview_moveto(1); root.update()
        capture(root, f'jahresanzeige-{theme}')
        app.home_canvas.yview_moveto(0)
    def settings_dialog(dialog, parent=None):
        dialog.update()
        widgets = list(children(dialog))
        canvases = [w for w in widgets if isinstance(w, mod.tk.Canvas) and not isinstance(w, mod.RoundedButton)]
        assert canvases
        capture(dialog, 'einstellungen')
        canvases[0].yview_moveto(1); dialog.update()
        capture(dialog, 'einstellungen-unten')
        next(w for w in widgets if isinstance(w, mod.RoundedButton) and w.text == 'Speichern').command()
    app.run_modal = settings_dialog
    app.show_settings_dialog()
    assert not errors and not callback_errors, (errors, callback_errors)

    # Ein fremder Host bleibt auch dann erkennbar, wenn dessen PID hier nicht existiert.
    foreign_path = Path(target)/'foreign.lock'
    foreign = {'host':'ANDERER-RECHNER', 'pid':99999999, 'started_at':datetime.now().astimezone().isoformat()}
    foreign_path.write_text(json.dumps(foreign),encoding='utf-8')
    assert app.read_foreign_lock(str(foreign_path)) == foreign
    foreign['started_at'] = (datetime.now().astimezone()-timedelta(days=3)).isoformat()
    foreign_path.write_text(json.dumps(foreign),encoding='utf-8')
    assert app.read_foreign_lock(str(foreign_path)) is None
    try:
        app.change_data_folder(target, move_existing=True)
    except ValueError:
        pass
    else:
        raise AssertionError('Nichtleerer Zielordner wurde überschrieben.')
    empty_target = Path(target)/'leer'
    expected = [(x['title'],len(x['items'])) for x in app.lists]
    assert app.change_data_folder(str(empty_target), move_existing=True)
    assert [(x['title'],len(x['items'])) for x in app.lists] == expected
    assert Path(tmp,'liste_speicher.json').exists()
    app.release_data_lock()
    app.cancel_pending_callbacks()
    root.destroy()
    print('Glide 3.6 End-to-End: Teilbackup mit Anhängen/Labels/leeren Ordnern, Vorlagen bearbeiten und speichern, Anlage, Fonts, Themes, Wochenbeginn und Datenordner: OK')
