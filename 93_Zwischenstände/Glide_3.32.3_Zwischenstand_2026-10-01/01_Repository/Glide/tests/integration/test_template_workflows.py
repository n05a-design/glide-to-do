"""Trackpad, vollständige Vorlagen, Abbruch, Migration und portable Rundläufe."""
import base64
import copy
from datetime import date, timedelta
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]

def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)

with tempfile.TemporaryDirectory(prefix='glide-template-qa-') as tmp:
    os.environ['GLIDE_DATA_DIR'] = tmp
    loader = importlib.machinery.SourceFileLoader('glide_template_qa', str(ROOT/'src/glide/app.pyw'))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec); loader.exec_module(mod)
    root = mod.tk.Tk()
    root.withdraw()
    errors = []
    root.report_callback_exception = lambda *exc: errors.append(exc)
    app = mod.ListApp(root)
    app.show_error = lambda *args, **kw: errors.append(args)
    app.show_warning = lambda *args, **kw: errors.append(args)
    app.show_info = lambda *args, **kw: None
    app.ask_yes_no = lambda *args, **kw: True
    root.geometry('1280x850+30+30'); root.deiconify(); root.update()
    try:
        # Sämtliche ausgelieferten Vorlagen durch denselben Importvalidator.
        defaults = app.default_template_records()
        assert len(defaults) == 20
        assert {entry['id'] for entry in defaults if entry['id'].startswith('journal-')} == {
            'journal-note', 'journal-gratitude', 'journal-weekly', 'journal-folder'
        }
        for record in defaults:
            if 'payload' in record:
                app.validate_template_payload(record)
        import sys
        sys.path.insert(0, str(ROOT/'tests/tools'))
        import vorlagendaten
        assert vorlagendaten.build(mod) == json.loads(vorlagendaten.TARGET.read_text()), 'Erzeuger nicht reproduzierbar'

        # Format 1 bleibt lesbar; Originalbytes werden vor Format 2 gesichert.
        legacy = {'format_version': 1, 'templates': app.legacy_template_records()}
        original = json.dumps(legacy, ensure_ascii=False).encode('utf-8')
        Path(mod.TEMPLATES_FILE).write_bytes(original)
        app.templates = app.load_templates()
        assert len(app.templates) == 20
        assert all('payload' in entry for entry in app.templates
                   if not entry['id'].startswith('journal-'))
        assert app.save_templates()
        assert json.loads(Path(mod.TEMPLATES_FILE).read_text())['format_version'] == 2
        backups = list(Path(mod.BACKUP_DIR).glob('vorlagen_vor_format2_*.json'))
        assert len(backups) == 1 and backups[0].read_bytes() == original
        assert app.save_templates() and len(list(Path(mod.BACKUP_DIR).glob('vorlagen_vor_format2_*.json'))) == 1
        custom = copy.deepcopy(legacy); custom['templates'][0]['note'] = 'Eigener Tagesablauf'
        Path(mod.TEMPLATES_FILE).write_text(json.dumps(custom))
        assert app.load_templates()[0]['note'] == 'Eigener Tagesablauf'
        Path(mod.TEMPLATES_FILE).write_text('{"format_version": 1, "templates": []}')
        assert {entry['id'] for entry in app.load_templates()} == {
            'journal-note', 'journal-gratitude', 'journal-weekly', 'journal-folder'
        }
        Path(mod.TEMPLATES_FILE).write_bytes(original)
        saved_copy = mod.shutil.copy2
        mod.shutil.copy2 = lambda *a, **kw: (_ for _ in ()).throw(OSError('Test: kein Schreibrecht'))
        assert not app.save_templates() and Path(mod.TEMPLATES_FILE).read_bytes() == original
        mod.shutil.copy2 = saved_copy
        assert app.save_templates()
        try:
            app.normalize_template_records({'format_version': 999, 'templates': []})
            raise AssertionError('Neueres Format akzeptiert')
        except ValueError:
            pass

        template = next(t for t in defaults if t['id'] == 'real-estate')
        app.templates = [copy.deepcopy(template)]
        app.set_template_view(); app._templates_editing = True
        before = copy.deepcopy((app.lists, app.folders, app.labels, app.templates, app.settings))
        app.save_items()
        data_before = Path(mod.SAVE_FILE).read_bytes()
        files_before = {p.name for p in Path(mod.ATTACHMENTS_DIR).iterdir()}

        # Abbruch verwirft verschachtelte Änderungen, neue Labels und Anhangskopien.
        source = Path(tmp)/'entwurf.txt'; source.write_text('Nur im Entwurf, niemals im echten Anhangsordner.')
        with mod.TemplateDraft(app, template) as draft:
            draft.labels.append(draft.new_label_object('Nur im Entwurf', color='delete'))
            draft.lists[0]['items'][2]['children'].reverse()
            stored = draft.store_attachment(str(source))
            draft.holder['attachments'].append(stored)
            temporary = Path(draft._draft_dir)
            draft.run_modal = lambda dialog, parent=None: dialog.destroy()
            original_modal = app.run_modal
            app.run_modal = lambda dialog, parent=None: dialog.destroy()
            assert draft.edit() is None
            app.run_modal = original_modal
        assert not temporary.exists()
        assert (app.lists, app.folders, app.labels, app.templates, app.settings) == before
        assert Path(mod.SAVE_FILE).read_bytes() == data_before
        assert {p.name for p in Path(mod.ATTACHMENTS_DIR).iterdir()} == files_before

        # Der echte Editor und seine vorhandenen vollständigen Detailmasken.
        for theme in ('light', 'dark'):
            app.set_design(theme, apply_now=False); app.apply_theme(); root.update()
            # Beide Plattformpfade: Windows behält den ursprünglichen Widgettyp.
            owner = mod.tk.Toplevel(root)
            owner.geometry('700x400+50+50')
            variable = mod.tk.StringVar(value='Normal')
            choices = ['Normal', 'Wichtig'] + [f'Auswahl {i}' for i in range(20)]
            platform = mod.IS_MACOS
            for mac in (False, True):
                try:
                    mod.IS_MACOS = mac
                    border, field = app._make_option_menu(owner, variable, choices,
                                                         option_colors={'Wichtig': 'priority_high'})
                finally:
                    mod.IS_MACOS = platform
                border.pack(fill='x', padx=20, pady=15)
                owner.update()
                assert isinstance(field, mod.AppOptionMenu)
                variable.set('Wichtig')
                assert field.cget('fg') == app.theme['priority_high']
                field['menu'].invoke(0)
                owner.update()  # Menübefehle laufen seit 3.32.0 im nächsten Leerlauf
                assert variable.get() == 'Normal'
                if isinstance(field, mod.AppOptionMenu):
                    assert field.cget('bg') == app.theme['input']
                    owner.grab_set()
                    field._open_popup(); owner.update()
                    assert field._popup is not None
                    assert root.grab_current() is owner
                    assert field._choices.cget('bg') == app.theme['input']
                    assert field._choices.yview()[1] < 1, 'Lange Auswahlliste muss scrollbar sein'
                    field._move(1)
                    assert variable.get() == 'Normal', 'Navigation darf noch nicht übernehmen'
                    grabs = []
                    trace = variable.trace_add('write', lambda *args: grabs.append(root.grab_current()))
                    field._commit(); owner.update()
                    assert variable.get() == 'Wichtig' and grabs == [owner]
                    variable.trace_remove('write', trace)
                    assert root.grab_current() is owner
                    field._open_popup(); owner.update()
                    field._highlight(12)
                    field._cancel(); owner.update()
                    assert variable.get() == 'Wichtig' and root.grab_current() is owner
                    field._open_popup(); owner.update()
                    field._type_ahead(SimpleNamespace(char='N'))
                    box = field._choices.bbox(0)
                    field._choose_mouse(SimpleNamespace(x=10, y=box[1]+2)); owner.update()
                    assert variable.get() == 'Normal'
                    field._open_popup(); owner.update()
                    field._outside_click(SimpleNamespace(x_root=0, y_root=0))
                    assert field._popup is None and root.grab_current() is owner
                    # Zerstören eines offenen Feldes darf keinen Grab oder Trace zurücklassen.
                    field._open_popup(); owner.update()
                border.destroy(); owner.update()
                assert not variable.trace_info()
                if isinstance(field, mod.AppOptionMenu):
                    assert root.grab_current() is owner
            owner.grab_release(); owner.destroy()
            with mod.TemplateDraft(app, template) as draft:
                draft.ask_yes_no = lambda *args, **kw: True
                def details(dialog, parent=None):
                    dialog.update()
                    assert dialog.cget('bg') == app.theme['bg']
                    widgets = list(descendants(dialog))
                    labels = [w.cget('text') for w in widgets if isinstance(w, mod.tk.Label)]
                    dropdown = next(w for w in widgets if isinstance(w, mod.LabelDropdown))
                    assert 'Labels (Mehrfachauswahl)' in labels
                    assert any(isinstance(w, mod.tk.Listbox) for w in widgets), 'Anhangsauswahl fehlt'
                    dropdown.set_selected_ids([draft.labels[-1]['id']])
                    first = next(w for w in widgets if isinstance(w, mod.tk.Entry))
                    first.delete(0, 'end'); first.insert(0, 'Geprüfter Titel')
                    next(w for w in widgets if isinstance(w, mod.RoundedButton) and w.text == 'Speichern').command()
                draft.run_modal = details
                def main(dialog, parent=None):
                    dialog.update()
                    assert dialog.cget('bg') == app.theme['bg']
                    tree = draft.editor_tree
                    style = mod.ttk.Style(dialog)
                    tree_style = tree.cget('style')
                    assert style.lookup(tree_style, 'background') == app.theme['card']
                    assert style.lookup(tree_style, 'fieldbackground') == app.theme['card']
                    assert style.lookup(tree_style, 'foreground') == app.theme['text']
                    assert style.lookup(tree_style, 'background', ('selected',)) == app.theme['selection']
                    assert int(style.lookup(tree_style, 'rowheight')) >= 36
                    assert tuple(map(str, tree.tk.splitlist(tree.cget('show')))) == ('tree',), 'Keine ungestalteten Tabellenköpfe'
                    assert isinstance(draft.editor_scrollbar, mod.ThemedAutoScrollbar)
                    for size in ('800x640', '1050x780', '1500x950'):
                        dialog.geometry(size); dialog.update()
                        columns = [tree.column(key, 'width') for key in ('#0', 'kind', 'due', 'labels')]
                        assert sum(columns) <= tree.winfo_width() + 2, (size, columns, tree.winfo_width())
                        for button in [w for w in descendants(dialog) if isinstance(w, mod.RoundedButton)]:
                            assert button.winfo_ismapped(), (size, button.text)
                            assert button.winfo_rooty()+button.winfo_height() <= dialog.winfo_rooty()+dialog.winfo_height()
                    child_folder = draft.folders[-1]
                    tree.item(child_folder['id'], open=False)
                    draft.render_editor(draft.holder['id'])
                    assert not tree.item(child_folder['id'], 'open'), 'Zugeklappte Zweige beim Auffrischen erhalten'
                    draft.edit_holder()
                    assert draft.holder['title'] == 'Geprüfter Titel'
                    task = draft.lists[0]['items'][2]['children'][0]
                    original_children = copy.deepcopy(task['children'])
                    draft.edit_object('item', task)
                    assert task['text'] == 'Geprüfter Titel' and task['children'] == original_children
                    # Umsortieren erhält die Objekte einschließlich Metadaten.
                    peer = draft.lists[0]['items'][2]['children'][1]
                    original_task = copy.deepcopy(task)
                    draft.editor_tree.selection_set(task['id'])
                    draft.move_selected(1)
                    assert draft.lists[0]['items'][2]['children'][1] == original_task
                    assert draft.lists[0]['items'][2]['children'][0]['id'] == peer['id']
                    # Listen im verschachtelten Ordner per vorhandener Maske ergänzen.
                    child_folder = draft.folders[-1]
                    draft.editor_tree.selection_set(child_folder['id'])
                    draft.add_node('list')
                    assert draft.lists[-1]['folder_id'] == child_folder['id']
                    # Der bestehende Anhang ist lokal im temporären Entwurf lesbar.
                    attachment = draft.holder['attachments'][0]
                    assert Path(draft.resolve_attachment_path(attachment)).read_bytes() == base64.b64decode(template['files'][attachment['storage']])
                    draft.holder['attachments'].append(draft.store_attachment(str(source)))
                    draft.title_var.set('Geprüfte Immobilienvorlage')
                    draft.submit()
                app.run_modal = main
                updated = draft.edit()
                app.run_modal = original_modal
            assert updated['title'] == 'Geprüfte Immobilienvorlage'
            app.validate_template_payload(updated)
            assert (app.lists, app.folders, app.labels, app.templates) == before[:4]
            assert {p.name for p in Path(mod.ATTACHMENTS_DIR).iterdir()} == files_before
        app.templates = [updated]
        assert app.save_templates()
        app.templates = app.load_templates()
        assert app.templates[0] == updated
        assert {entry['id'] for entry in app.templates[1:]} == {
            'journal-note', 'journal-gratitude', 'journal-weekly', 'journal-folder'
        }

        # Verwendung: neue IDs, relative Daten inkl. Wiederholungsstart/-ende,
        # originale Anhangsbytes, kein bereits angelegter Bestand überschrieben.
        weekly = copy.deepcopy(next(t for t in defaults if t['id'] == 'household'))
        task = weekly['payload']['lists'][0]['items'][0]
        task['repeat']['ende'] = (date.fromisoformat(weekly['schedule_anchor'])+timedelta(days=42)).isoformat()
        app.templates += [weekly]
        current_ids = {page['id'] for page in app.lists}
        created = app.create_list_from_template('household')
        assert current_ids < {page['id'] for page in app.lists}
        assert created['items'][0]['due'] == (date.today()+timedelta(days=7)).isoformat()
        assert created['items'][0]['repeat']['ende'] == (date.today()+timedelta(days=42)).isoformat()
        absolute = copy.deepcopy(weekly); absolute['id'] = 'absolute'; absolute.pop('schedule_anchor')
        app.templates.append(absolute)
        assert app.create_list_from_template('absolute')['items'][0]['due'] == task['due']
        created = app.create_list_from_template(updated['id'])
        assert created['title'] == updated['title'] and len(created['attachments']) == 2
        assert Path(app.resolve_attachment_path(created['attachments'][1])).read_bytes() == source.read_bytes()
        assert app.validate_template_payload(updated)

        # Synthetische Mac-Trackpad-Ereignisse direkt über Diagramm, Beschriftung
        # und Schaltflächen, inklusive kleinem Delta und rein horizontaler Geste.
        # Punkt 32 (3.23.0): Bei 1000 Pixeln Fensterbreite steht die Startseite
        # seit 3.23 zweispaltig und wird dadurch kürzer als das Fenster – dann
        # gäbe es nichts zu scrollen. Geprüft wird hier das Scrollen, nicht das
        # Raster; die Spaltenzahl wird deshalb ausdrücklich auf eins gesetzt.
        app.settings['home_columns'] = '1'
        app.set_home_view(); root.geometry('1000x700+20+20'); root.update()
        app.refresh_home(); root.update()
        assert app.home_canvas.yview()[1] < 1
        # Nur sichtbare Flächen: Eine Schaltfläche, die die Schnellzugriffs-
        # zeile bei schmaler Kachel bewusst ausblendet (ButtonFlow.compact_keys),
        # kann kein Mausrad-Ereignis empfangen – sie ist nicht gezeichnet.
        surfaces = [app.home_canvas] + [w for w in descendants(app.home_content)
                                        if isinstance(w, (mod.tk.Label, mod.RoundedButton))
                                        and w.winfo_ismapped()][:8]
        precise_supported = bool(app.home_canvas.bind('<TouchpadScroll>'))
        for widget in surfaces:
            app.home_canvas.yview_moveto(0); root.update()
            before_scroll = app.home_canvas.yview()
            if precise_supported:
                widget.event_generate('<TouchpadScroll>', delta=65531)  # Y = -5 Pixel
                root.update()
                assert app.home_canvas.yview()[0] > before_scroll[0], (widget, app.home_canvas.yview())
                before_scroll = app.home_canvas.yview()
                widget.event_generate('<TouchpadScroll>', delta=5 << 16)  # nur X
                root.update()
                assert app.home_canvas.yview() == before_scroll
            widget.event_generate('<MouseWheel>', delta=-1)
            root.update()
            assert app.home_canvas.yview()[0] > 0, (widget.winfo_class(), getattr(widget, 'text', ''), app.home_canvas.yview())
        app.home_canvas.yview_moveto(0); root.update()
        app.home_canvas.event_generate('<MouseWheel>', delta=-120); root.update()
        assert 0 < app.home_canvas.canvasy(0) <= 24, 'Ein Mausradschritt darf nicht die ganze Seite überspringen'
        app.settings['home_columns'] = 'auto'
        app.set_library_view(); root.update()
        for surface in app.library_cards:
            assert surface.winfo_x()+surface.winfo_width() <= surface.master.winfo_width()
        assert not errors, errors
        print('OK: 16 vollständige Projekt-/Listen- plus 4 Tagebuchvorlagen, reproduzierbare Daten, Format-1-Sicherung/Migration, Abbruchisolierung, vollständige Dialoge in Hell/Dunkel, Struktur und Anhänge, relative/absolute Fristen, Trackpad und Übersicht.')
    finally:
        app.on_close()
