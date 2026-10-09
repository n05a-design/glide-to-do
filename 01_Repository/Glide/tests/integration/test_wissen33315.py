"""G29/G31/G32 zusammen: UI, Heimat, Referenzen, Formattor, Import und Neustart."""
import argparse
import copy
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--app', type=Path, default=REPO / 'src/glide/app.pyw')
parser.add_argument('--report', type=Path)
parser.add_argument('--capture', type=Path)
parser.add_argument('--counterprobe', action='store_true')
parser.add_argument('--previous', type=Path)
args = parser.parse_args()
sys.stdout.reconfigure(encoding='utf-8')

with tempfile.TemporaryDirectory(prefix='glide-wissen-') as directory:
    os.environ['GLIDE_DATA_DIR'] = directory
    os.environ['GLIDE_TEST_MODE'] = '1'
    if not args.counterprobe:
        original20 = (REPO / 'tests/fixtures/current_v20/reference_v20.json').read_bytes()
        Path(directory, 'liste_speicher.json').write_bytes(original20)
    loader = importlib.machinery.SourceFileLoader('glide_wissen', str(args.app.resolve()))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    available = {name: hasattr(mod.ListApp, name) for name in
                 ('transfer_document_task', 'show_tasks_from_pages', 'open_task_text_source')}
    if args.counterprobe:
        result = dict(version=mod.APP_VERSION, app_sha256=hashlib.sha256(args.app.read_bytes()).hexdigest(),
                      available=available, exitcode=0 if all(available.values()) else 1)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(result, indent=2), encoding='utf-8')
        print(result)
        raise SystemExit(result['exitcode'])
    assert all(available.values()), available
    root = mod.tk.Tk()
    root.geometry('1280x800+10+10')
    errors, checks = [], []
    destroyed = False
    root.report_callback_exception = lambda *exc: errors.append(str(exc[1]))
    app = mod.ListApp(root)
    app.show_info = app.show_error = app.show_warning = lambda *a, **kw: None
    backups21 = list(Path(mod.BACKUP_DIR).glob('liste_vor_format21_*.json'))
    assert len(backups21) == 1 and backups21[0].read_bytes() == original20
    backups22 = list(Path(mod.BACKUP_DIR).glob('liste_vor_format22_*.json'))
    assert len(backups22) == 1 and backups22[0].read_bytes() == original20
    assert json.loads(Path(mod.SAVE_FILE).read_text(encoding='utf-8'))['version'] == 23
    checks.append(f'Format 20 → {app.DATA_SCHEMA_VERSION}: Startmigration mit bytegenauen Vorsicherungen für Format 21 und 22')

    def idle():
        for _ in range(3):
            root.update_idletasks(); root.update()

    def entry(identity):
        return next(e for e in app.lists if e['id'] == identity)

    def editor(identity):
        app.set_active_list(identity); idle()
        return app.rich_note_editor

    def task(identity):
        return app.find_item_in_lists(identity)[0]

    def spans(document, prefix):
        return [s for s in document['spans'] if s['tag'].startswith(prefix)]

    try:
        note = app.new_list_object('Besprechung 😀', [], list_kind='note')
        target = app.new_list_object('Umsetzung', [])
        app.lists.extend([note, target]); app.save_items()
        note_id, target_id = note['id'], target['id']
        ed = editor(note_id)
        assert ed.ALLOW_TASKS and 'task' in dict((tag, name) for name, tag in ed.block_choices())
        ed.text.insert('1.0', 'Rückruf organisieren')
        undo_before = len(app.undo_stack)
        ed.set_block('task'); idle()
        item_id = entry(note_id)['items'][0]['id']
        assert len(app.undo_stack) == undo_before + 1, 'Aufgabe und Text sind ein Undo-Schritt'
        assert spans(entry(note_id)['rich_note'], 'item:')[0]['tag'] == 'item:' + item_id
        assert app.tree.exists(item_id), 'Notizliste zeigt denselben Punkt'
        assert len(ed.task_boxes()) == 1
        ed.toggle_task(ed.task_boxes()[0]); idle()
        assert task(item_id)['done'] is True
        ed.text.focus_force(); idle()
        ed.text.mark_set('insert', '1.0 lineend'); ed.text.insert('insert', ' morgen')
        ed.flush(); assert task(item_id)['text'].endswith('morgen')
        undo_before = len(app.undo_stack)
        ed.insert_markdown('\n- [ ] Protokoll versenden')
        assert len(app.undo_stack) == undo_before + 1, 'Markdown und Aufgaben als ein Schritt'
        assert len(entry(note_id)['items']) == 2
        second = entry(note_id)['items'][1]['id']
        ed = editor(note_id)
        ranges = ed.task_ranges(second)
        ed.text.delete(f'{ranges[0][0]} linestart', f'{ranges[0][0]} lineend +1c'); ed.flush()
        assert not app.find_item_in_lists(second)
        ed.undo(); idle(); assert app.find_item_in_lists(second)
        ed.redo(); idle(); assert not app.find_item_in_lists(second)
        ed.undo(); idle(); assert app.find_item_in_lists(second)
        checks.append('Notiz: echte Aufgabe, gemeinsame ID, ein Undo-Schritt, Checkbox, Titel, Markdown, Undo/Redo')

        # Ein Verweis auf einen bestehenden Punkt derselben Notiz besitzt ihn nicht.
        legacy = app.new_item('Vorhandener Notizpunkt')
        entry(note_id)['items'].append(legacy); app.save_items()
        ed = editor(note_id); ed.text.mark_set('insert', 'end-1c')
        ed.insert_task_reference(legacy['id']); idle()
        rr = ed.task_ranges(legacy['id'])[0]
        ed.text.delete(f'{rr[0]} linestart', f'{rr[0]} lineend +1c'); ed.flush(); idle()
        assert app.find_item_in_lists(legacy['id']), 'Eigener Notizverweis löscht nur die Zeile'
        ed.undo(); idle(); ed.redo(); idle()
        assert app.find_item_in_lists(legacy['id'])

        # Eine zweite Verweiszeile verdeckt nicht das Löschen der Heimatzeile.
        ed.text.mark_set('insert', 'end-1c'); ed.insert_task_reference(second); idle()
        assert len(ed.task_ranges(second)) == 2
        owned_start = ed.text.index(ed.text.tag_ranges('item:' + second)[0])
        ed.text.delete(f'{owned_start} linestart', f'{owned_start} lineend +1c'); ed.flush(); idle()
        assert not app.find_item_in_lists(second) and len(ed.task_ranges(second)) == 1
        assert ed._task_widgets[second][0]._target_state == 'trash'
        ed.undo(); idle()
        assert app.find_item_in_lists(second) and len(ed.task_ranges(second)) == 2
        assert sum(item['id'] == second for item in entry(note_id)['items']) == 1
        ed.redo(); idle(); assert not app.find_item_in_lists(second)
        ed.undo(); idle(); assert app.find_item_in_lists(second)
        ref_start = ed.text.index(ed.text.tag_ranges('taskref:' + second)[0])
        ed.text.delete(f'{ref_start} linestart', f'{ref_start} lineend +1c'); ed.flush(); idle()
        assert app.find_item_in_lists(second) and len(ed.task_ranges(second)) == 1
        checks.append('Heimat und Verweis derselben Notiz: Verweislöschen erhält Punkt; Heimatlöschen wirkt trotz zweitem Verweis; Undo/Redo ohne Duplikat')

        page = app.new_page_from_markdown('# Recherche\n\n- [ ] Angebot prüfen')
        page_id, page_task = page['id'], page['items'][0]['id']
        child = app.new_item('Anlage prüfen')
        task(page_task)['children'].append(child)
        app.save_items()
        ed = editor(note_id)
        ed.text.mark_set('insert', 'end-1c')
        with patch.object(app, 'themed_choice_dialog', return_value=page_task) as choice:
            ed.insert_task_reference()
            assert choice.called
        ed.text.mark_set('insert', 'end-1c'); ed.insert_task_reference(page_task)
        idle()
        assert len(ed.task_ranges(page_task)) == 2 and len(ed._task_widgets[page_task]) == 2, (ed.document(), ed.task_ranges(page_task), list(ed._task_widgets), [(b._item_id, ed.text.index(b)) for b in ed.task_boxes()])
        root.focus_set(); idle()
        ranges = ed.task_ranges(page_task)
        start = ed.text.index(f'{ranges[0][0]} +1c')
        ed.text.delete(start, f'{ranges[0][0]} lineend')
        ed.text.insert(start, 'Angebot prüfen dringend', ('task', 'taskref:' + page_task))
        ed.flush(); idle()
        assert task(page_task)['text'] == 'Angebot prüfen dringend'
        ed.text.focus_force(); idle(); ed.text.event_generate('<Control-z>'); idle()
        assert task(page_task)['text'] == 'Angebot prüfen', 'Text-Undo nimmt den echten Titel zurück'
        before_redo = (len(ed._redo), ed._last, ed.document())
        ed.text.event_generate('<Control-y>'); idle()
        assert task(page_task)['text'] == 'Angebot prüfen dringend', (task(page_task)['text'], len(ed._redo), before_redo, ed.document())
        task(page_task)['text'] = 'Anderswo geändert'
        app.save_items()
        ed.undo(); idle()
        assert task(page_task)['text'] == 'Anderswo geändert', 'Text-Undo bewahrt spätere externe Titeländerung'
        ed.redo(); idle()
        assert task(page_task)['text'] == 'Anderswo geändert', 'Text-Redo bewahrt spätere externe Titeländerung nach Undo'
        ed.undo(); idle()
        assert task(page_task)['text'] == 'Anderswo geändert', 'Wiederholte Rücknahme bewahrt externe Titeländerung'
        task(page_task)['text'] = 'Angebot prüfen dringend'; app.save_items(); ed.refresh_tasks(); ed.flush()
        ed.text.mark_set('insert', ed.task_ranges(page_task)[0][1])
        ed.text.clipboard_clear(); ed.text.clipboard_append('\nZusatz ohne Aufgabe')
        ed.paste_plain(); idle()
        assert len(ed.task_ranges(page_task)) == 2, 'Mehrzeiliger Klartext kopiert keine Aufgabenmarke'
        assert task(page_task)['text'] == 'Angebot prüfen dringend'
        first = ed.task_ranges(page_task)[0][0]
        ed.text.mark_set('insert', f'{first} +5c')
        ed.text.clipboard_clear(); ed.text.clipboard_append('\nEigener Absatz')
        ed.text.focus_force(); idle(); ed.text.event_generate('<<Paste>>'); idle(); ed.flush()
        assert len(ed.task_ranges(page_task)) == 2
        assert 'Eigener Absatz' in ed.document()['text']
        # Rücknahme stellt Aufgabe und Text wieder her, ohne einen Absatz zu verlieren.
        ed.text.event_generate('<Control-z>'); idle()
        assert task(page_task)['text'] == 'Angebot prüfen dringend'

        owned_before = len(entry(note_id)['items'])
        ed.toggle_task(ed._task_widgets[page_task][0]); idle()
        assert task(page_task)['done'] and len(entry(note_id)['items']) == owned_before
        assert all(box._target_state == 'active' for box in ed._task_widgets[page_task])
        task(page_task)['text'] = 'Angebot freigeben 😀'; app.save_items()
        ed.text.focus_clear() if hasattr(ed.text, 'focus_clear') else root.focus_set()
        ed.refresh_tasks(); ed.flush()
        assert task(page_task)['text'] == 'Angebot freigeben 😀', 'Verweis schreibt keinen alten Titel zurück'
        assert ed.document()['text'].count('Angebot freigeben 😀') == 2
        ranges = ed.task_ranges(page_task)
        ed.text.delete(f'{ranges[0][0]} linestart', f'{ranges[0][0]} lineend +1c'); ed.flush()
        assert app.find_item_in_lists(page_task) and len(ed.task_ranges(page_task)) == 1
        checks.append('Textverweise: zwei Zeilen derselben ID, gemeinsamer Zustand, Unicode-Titel, Löschen nur des Verweises')

        ed = editor(page_id)
        ed.text.mark_set('insert', ed.task_ranges(page_task)[0][0])
        with patch.object(app, 'themed_choice_dialog', return_value=target_id):
            ed.move_task_to_list()
        idle()
        assert app.find_item_in_lists(page_task)[3]['id'] == target_id
        assert task(page_task)['children'][0]['id'] == child['id']
        assert entry(page_id)['items'] == []
        assert spans(entry(page_id)['rich_note'], 'taskref:')[0]['tag'] == 'taskref:' + page_task
        assert '- [x] Angebot freigeben 😀' in app.page_markdown(page_id)
        app.undo_last_change(); idle()
        assert app.find_item_in_lists(page_task)[3]['id'] == page_id
        assert spans(entry(page_id)['rich_note'], 'item:')
        assert app.transfer_document_task(page_id, page_task, target_id)
        action = next(a for a in app.app_action_entries() if a['id'] == 'show_tasks_from_pages')
        app.invoke_app_action(action); idle()
        assert app.view_mode == 'saved_filter' and app.saved_filters.current()['source'] == 'pages'
        ids = [row[4]['id'] for row in app.saved_filters.entries()]
        assert page_task in ids and item_id not in ids and child['id'] in ids
        app.open_task_text_source(page_task) if len(app.task_text_sources(page_task)) == 1 else None
        entry(page_id)['archived'] = True; app.save_items(); app._render_cache = {}
        assert page_task not in [row[4]['id'] for row in app.saved_filters.entries()]
        entry(page_id)['archived'] = False; app.save_items(); app._render_cache = {}
        assert page_task in [row[4]['id'] for row in app.saved_filters.entries()]
        with patch.object(app, 'themed_choice_dialog', return_value=page_id):
            app.open_task_text_source(page_task)
        assert app.active_list_id == page_id
        checks.append('Seite → Liste: gleiche ID und Unteraufgabe, Text bleibt Verweis, Undo, Aus Seiten, Archiv, Textquelle')

        ed = editor(target_id)
        with app.item_change([page_task], restore=False) as change:
            assert app.move_item_to_trash(page_task); change.mark()
        trash_before = copy.deepcopy(app.trash)
        ed = editor(page_id)
        assert not app.find_item_in_lists(page_task) and app.trash == trash_before
        assert ed.task_boxes()[0]._target_state == 'trash'
        assert any(ed.task_boxes()[0].itemcget(shape, 'text') == 'Im Papierkorb'
                   for shape in ed.task_boxes()[0].find_all() if ed.task_boxes()[0].type(shape) == 'text')
        ed.toggle_task(ed.task_boxes()[0]); idle()
        assert not app.find_item_in_lists(page_task), 'Papierkorbziel bleibt im Papierkorb'
        trashed = next(t for t in app.trash if (app.trash_entry_payload(t) or {}).get('id') == page_task)
        app.restore_trash_entry(trashed['id']); idle()
        assert app.find_item_in_lists(page_task)[3]['id'] == target_id
        ed = editor(target_id)
        with app.item_change([page_task], restore=False) as change:
            app.move_item_to_trash(page_task); change.mark()
        app.trash[:] = [t for t in app.trash if (app.trash_entry_payload(t) or {}).get('id') != page_task]
        app.drop_dangling_references(); app.save_items()
        ed = editor(page_id); ed.flush(); idle()
        assert not app.find_item_in_lists(page_task) and ed.task_boxes()[0]._target_state == 'missing'
        assert any(ed.task_boxes()[0].itemcget(shape, 'text') == 'Ziel fehlt'
                   for shape in ed.task_boxes()[0].find_all() if ed.task_boxes()[0].type(shape) == 'text')
        assert spans(ed.document(), 'taskref:')[0]['tag'] == 'taskref:' + page_task
        checks.append('Papierkorb und endgültig fehlendes Ziel: Verweis bleibt, kein Wiederbeleben, keine Ersatzaufgabe')

        # Gemeinsame Import-ID-Neuvergabe über mehrere Dokumente.
        imported_lists = [copy.deepcopy(entry(note_id)), copy.deepcopy(entry(target_id)), copy.deepcopy(entry(page_id))]
        source_task = task(item_id)
        imported_lists[2]['rich_note'] = dict(text=source_task['text'], links={}, spans=[
            dict(tag='task', start=0, end=len(source_task['text'])),
            dict(tag='taskref:' + item_id, start=0, end=len(source_task['text']))])
        backup = app.complete_backup_payload()
        backup['lists'] = imported_lists
        backup['folders'] = []; backup['trash'] = []
        path = Path(directory) / 'import.json'
        path.write_text(json.dumps(backup), encoding='utf-8')
        assert app.import_full_backup(additive=True, path=str(path), show_success=False, confirm=False)
        mapping = app._additive_import_maps
        copied = entry(mapping['containers'][page_id])
        copied_task = mapping['items'][item_id]
        assert copied_task != item_id
        assert spans(copied['rich_note'], 'taskref:')[0]['tag'] == 'taskref:' + copied_task
        assert app.find_item_in_lists(copied_task)[3]['id'] == mapping['containers'][note_id]
        checks.append('Additiver Import: globale ID-Neuvergabe und Textverweis auf importierte Aufgabe')

        # Ein fehlgeschlagener Schreibvorgang darf keinen gespeicherten Erfolg melden.
        ed = editor(note_id)
        old_bytes = Path(mod.SAVE_FILE).read_bytes()
        with patch.object(app, 'write_json_atomic', side_effect=OSError('synthetischer Schreibfehler')):
            ed.text.mark_set('insert', 'end-1c'); ed.text.insert('insert', '\nSpeicherprobe', ())
            assert ed.flush() is False
            assert Path(mod.SAVE_FILE).read_bytes() == old_bytes
            assert ed._save_failed
        assert ed.flush() and not app.dirty
        app._data_read_only = True
        persisted = Path(mod.SAVE_FILE).read_bytes()
        assert app.transfer_document_task(note_id, item_id, target_id) is False
        assert ed.flush() is False and Path(mod.SAVE_FILE).read_bytes() == persisted
        app._data_read_only = False
        checks.append('Speicherfehler: unveränderte Datei, sichtbarer Fehler, Retry; schreibgeschützter Bestand')

        if args.capture:
            sys.path.insert(0, str(REPO / 'tests/tools'))
            from releasedaten import save_windows_screenshot
            args.capture.mkdir(parents=True, exist_ok=True)
            for width, height in ((860, 700), (1280, 800)):
                root.geometry(f'{width}x{height}+10+10')
                for font_size in ('mittel', 'gross'):
                    for design in ('hell', 'dunkel'):
                        app.settings['ui_font_size'] = font_size
                        app.set_design('light' if design == 'hell' else 'dark', apply_now=False); app.apply_ui_font(); app.apply_theme(); idle()
                        for source in (note_id, page_id):
                            ed = editor(source)
                            assert ed.text.winfo_height() > 80
                            save_windows_screenshot(root, args.capture / f'{entry(source)["list_kind"]}_{width}_{font_size}_{design}.png')
            checks.append('16 Fensterzustände: Notiz/Seite, Mindest-/Referenzgröße, mittel/groß, hell/dunkel')
        app.flush_rich_note(); app.save_items(); app.save_settings()
        assert not errors, errors
        app.cancel_pending_callbacks(); app.release_data_lock(); root.destroy(); destroyed = True
        # Frischer Prozess: keine importierten Objekt- oder Rendercaches.
        script = '''import importlib.machinery,importlib.util,json,sys
l=importlib.machinery.SourceFileLoader('restart',sys.argv[1]);m=importlib.util.module_from_spec(importlib.util.spec_from_loader(l.name,l));sys.modules[l.name]=m;l.exec_module(m)
r=m.tk.Tk();r.withdraw();a=m.ListApp(r);a.show_info=lambda *x:None
assert a.DATA_SCHEMA_VERSION== 23
assert a.find_item_in_lists(sys.argv[2])
page=next(e for e in a.lists if e['id']==sys.argv[3]);assert any(s['tag']=='taskref:'+sys.argv[2] for s in page['rich_note']['spans'])
assert a.settings['saved_filters'];a.cancel_pending_callbacks();a.release_data_lock();r.destroy();print('restart OK')'''
        run = subprocess.run([sys.executable, '-B', '-c', script, str(args.app.resolve()), copied_task, copied['id']],
                             capture_output=True, text=True, timeout=60)
        assert run.returncode == 0, run.stderr
        checks.append('Neustart: Kennungen, Heimat, Textverweise und Filter aus gespeicherten Dateien')
        # Backupfehler vor der Migration blockiert jedes Überschreiben.
        with tempfile.TemporaryDirectory(prefix='glide-format21-failure-') as failure_dir:
            Path(failure_dir, 'liste_speicher.json').write_bytes(original20)
            failure_script = '''import importlib.machinery,importlib.util,sys,pathlib
from unittest.mock import patch
l=importlib.machinery.SourceFileLoader('gate',sys.argv[1]);m=importlib.util.module_from_spec(importlib.util.spec_from_loader(l.name,l));sys.modules[l.name]=m;l.exec_module(m)
m.ListApp.show_error=m.ListApp.show_warning=m.ListApp.show_info=lambda *x,**kw:None
r=m.tk.Tk();r.withdraw();before=pathlib.Path(m.SAVE_FILE).read_bytes()
with patch.object(m.shutil,'copy2',side_effect=OSError('synthetic backup failure')):
 a=m.ListApp(r);assert not a.save_items(show_error=False);assert pathlib.Path(m.SAVE_FILE).read_bytes()==before
a.dirty=False;a.cancel_pending_callbacks();a.release_data_lock();r.destroy()'''
            env = dict(os.environ, GLIDE_DATA_DIR=failure_dir)
            failed = subprocess.run([sys.executable, '-B', '-c', failure_script, str(args.app.resolve())],
                                    env=env, capture_output=True, text=True, timeout=60)
            assert failed.returncode == 0, failed.stderr
        checks.append('Formattor: fehlgeschlagene Vorsicherung lässt Originaldatei unverändert')
        import vorversion
        previous = vorversion.finden(REPO.parent.parent, '3.33.14', REPO / 'CHANGELOG.md', args.previous)
        if previous is None:
            checks.append(vorversion.hinweis('3.33.14'))
        else:
            old_script = '''import importlib.machinery,importlib.util,sys,pathlib
sys.path.insert(0,sys.argv[2]);l=importlib.machinery.SourceFileLoader('older',sys.argv[1]);m=importlib.util.module_from_spec(importlib.util.spec_from_loader(l.name,l));sys.modules[l.name]=m;l.exec_module(m)
m.ListApp.show_error=m.ListApp.show_warning=m.ListApp.show_info=lambda *x,**kw:None
r=m.tk.Tk();r.withdraw();before=pathlib.Path(m.SAVE_FILE).read_bytes();a=m.ListApp(r)
assert m.ListApp.DATA_SCHEMA_VERSION==20 and a._data_read_only
assert not a.save_items(show_error=False) and pathlib.Path(m.SAVE_FILE).read_bytes()==before
a.cancel_pending_callbacks();a.release_data_lock();r.destroy()'''
            old_read = subprocess.run([sys.executable, '-B', '-c', old_script, str(previous.resolve()),
                                      str((REPO.parent.parent / '07_Python-Versionen').resolve())],
                                     capture_output=True, text=True, timeout=60)
            assert old_read.returncode == 0, old_read.stderr
            checks.append(f'Unveränderte 3.33.14: Format {app.DATA_SCHEMA_VERSION} öffnet schreibgeschützt, Datei bytegleich')
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(dict(version=mod.APP_VERSION, format=mod.ListApp.DATA_SCHEMA_VERSION, exitcode=0, checks=checks,
                app_sha256=hashlib.sha256(args.app.read_bytes()).hexdigest(), callback_errors=errors,
                data='synthetic; isolated GLIDE_DATA_DIR', manual_acceptance='open'), indent=2, ensure_ascii=False), encoding='utf-8')
        print('test_wissen33315: OK; ' + '; '.join(checks))
    finally:
        if not destroyed:
            app.cancel_pending_callbacks(); app.release_data_lock(); root.destroy()
