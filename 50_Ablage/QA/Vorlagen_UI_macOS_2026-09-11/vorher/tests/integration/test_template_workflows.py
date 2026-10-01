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
        assert len(defaults) == 16
        for record in defaults:
            assert 'payload' in record
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
        assert len(app.templates) == 16 and all('payload' in entry for entry in app.templates)
        assert app.save_templates()
        assert json.loads(Path(mod.TEMPLATES_FILE).read_text())['format_version'] == 2
        backups = list(Path(mod.BACKUP_DIR).glob('vorlagen_vor_format2_*.json'))
        assert len(backups) == 1 and backups[0].read_bytes() == original
        assert app.save_templates() and len(list(Path(mod.BACKUP_DIR).glob('vorlagen_vor_format2_*.json'))) == 1
        custom = copy.deepcopy(legacy); custom['templates'][0]['note'] = 'Eigener Tagesablauf'
        Path(mod.TEMPLATES_FILE).write_text(json.dumps(custom))
        assert app.load_templates()[0]['note'] == 'Eigener Tagesablauf'
        Path(mod.TEMPLATES_FILE).write_text('{"format_version": 1, "templates": []}')
        assert app.load_templates() == []
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
            app.theme_name = theme; app.apply_theme(); root.update()
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
        assert app.templates == [updated]

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
        app.set_home_view(); root.geometry('1000x700+20+20'); root.update()
        assert app.home_canvas.yview()[1] < 1
        surfaces = [app.home_canvas] + [w for w in descendants(app.home_content) if isinstance(w, (mod.tk.Label, mod.RoundedButton))][:8]
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
            assert app.home_canvas.yview()[0] > 0
        app.home_canvas.yview_moveto(0); root.update()
        app.home_canvas.event_generate('<MouseWheel>', delta=-120); root.update()
        assert 0 < app.home_canvas.canvasy(0) <= 24, 'Ein Mausradschritt darf nicht die ganze Seite überspringen'
        app.set_library_view(); root.update()
        for surface in app.library_cards:
            assert surface.winfo_x()+surface.winfo_width() <= surface.master.winfo_width()
        assert not errors, errors
        print('OK: 16 Vorlagen, reproduzierbare Daten, Format-1-Sicherung/Migration, Abbruchisolierung, vollständige Dialoge in Hell/Dunkel, Struktur und Anhänge, relative/absolute Fristen, Trackpad und Übersicht.')
    finally:
        app.on_close()
