"""G28/G09/U08: Originalaufgaben, Bilder, echte Vorschau, Undo/Import/Neustart."""
import argparse
import copy
from datetime import date, timedelta
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
parser.add_argument('--app', type=Path, default=REPO/'src/glide/app.pyw')
parser.add_argument('--previous', type=Path)
parser.add_argument('--report', type=Path)
parser.add_argument('--capture', type=Path)
parser.add_argument('--counterprobe', action='store_true')
args = parser.parse_args()
sys.path.insert(0, str(Path(__file__).resolve().parent))
import vorversion
args.previous = vorversion.finden(REPO.parents[1], '3.33.17', REPO/'CHANGELOG.md', args.previous)
checks, observations = [], []

with tempfile.TemporaryDirectory(prefix='glide-seiten18-') as directory:
    os.environ['GLIDE_DATA_DIR'] = directory; os.environ['GLIDE_TEST_MODE'] = '1'
    original = (REPO/'tests/fixtures/current_v22/reference_v22.json').read_bytes()
    Path(directory,'liste_speicher.json').write_bytes(original)
    loader = importlib.machinery.SourceFileLoader('glide_seiten18', str(args.app.resolve()))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod; loader.exec_module(mod)
    if args.counterprobe:
        available = all(hasattr(mod.ListApp, name) for name in ('choose_live_list', 'choose_page_cover', 'confirm_template_preview'))
        result = dict(version=mod.APP_VERSION, available=available, exitcode=0 if available else 1,
                      app_sha256=hashlib.sha256(args.app.read_bytes()).hexdigest())
        if args.report:
            args.report.parent.mkdir(parents=True,exist_ok=True)
            args.report.write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(result); raise SystemExit(result['exitcode'])
    root = mod.tk.Tk(); root.geometry('1280x800+20+20')
    errors = []; root.report_callback_exception = lambda *exc: errors.append(repr(exc[1]))
    mod.ListApp.show_info = mod.ListApp.show_warning = lambda *a, **kw: None
    app = mod.ListApp(root); app.show_error = lambda *a, **kw: errors.append(repr(a))
    def idle():
        for _ in range(3): root.update_idletasks(); root.update()
    def entry(identity): return next(e for e in app.lists if e['id'] == identity)
    def item(identity): return app.find_item_in_lists(identity)[0]
    def stop():
        app.cancel_pending_callbacks(); app.release_data_lock()
        for job in root.tk.call('after','info'): root.tk.call('after','cancel',job)
        root.destroy()
    try:
        assert app.DATA_SCHEMA_VERSION == 23
        assert json.loads(Path(mod.SAVE_FILE).read_text())['version'] == 23
        backups = list(Path(mod.BACKUP_DIR).glob('liste_vor_format23_*.json'))
        assert len(backups) == 1 and backups[0].read_bytes() == original
        checks.append('Format 22 → 23, bytegenaue Vorsicherung')
        child = app.new_item('Unteraufgabe – Rückmeldung einholen')
        task = app.new_item('Angebot prüfen – ä, emoji 😀', children=[child], due='2026-10-12')
        source = app.new_list_object('Kundenprojekt', [task, app.new_item('Erledigt', done=True)])
        page = app.new_list_object('Projekt im Kontext', [], list_kind='page',
                                  rich_note={'text':'Besprechungsnotizen und Entscheidungen.','spans':[],'links':{}})
        drawing = app.new_list_object('Eigenes Titelbild', [], list_kind='drawing',
                    drawing=mod.glide_drawing.DrawingModel(size=16).to_document())
        app.lists.extend([source, page, drawing]); app.save_items()
        sid, pid, tid, cid, did = source['id'], page['id'], task['id'], child['id'], drawing['id']
        target = mod.glide_objects.uri('list', sid)
        app.set_active_list(pid); idle(); depth = len(app.undo_stack)
        assert app.choose_live_list(pid, target); idle()
        assert len(app.undo_stack) == depth+1 and entry(pid)['items'] == []
        ed = app.rich_note_editor
        assert ed.live_tree.get_children() == (tid,cid,source['items'][1]['id'])
        assert ('list',pid) in app.object_graph()[2][('list',sid)]
        ed.live_tree.selection_set(tid); ed.live_tree.focus(tid); root.focus_force(); ed.live_tree.focus_set(); idle()
        depth = len(app.undo_stack); ed.live_tree.event_generate('<KeyPress-space>'); idle()
        assert item(tid)['done'] and len(app.undo_stack) == depth+1
        app.undo_last_change(); idle(); assert not item(tid)['done'] and entry(pid)['items'] == []
        app.set_active_list(pid); idle()
        with patch.object(app,'edit_page_task') as opening:
            ed = app.rich_note_editor; ed.live_tree.selection_set(cid); ed.live_tree.focus_set(); idle()
            ed.live_tree.event_generate('<Return>'); idle()
            opening.assert_called_once_with(cid)
        assert app.remove_live_list(pid,target); idle()
        assert app.find_item_in_lists(tid) and app.rich_note_editor.live_tree is None
        app.undo_last_change(); idle(); assert entry(pid)['live_lists'] == [target]
        before = copy.deepcopy(app.lists); depth = len(app.undo_stack)
        with patch.object(app,'save_items',return_value=False): assert not app.remove_live_list(pid,target)
        assert app.lists == before and len(app.undo_stack) == depth
        with patch.object(app,'save_items',return_value=False): assert not app.toggle_live_task(pid,target,tid)
        assert app.lists == before and len(app.undo_stack) == depth
        app._data_read_only = True
        assert not app.remove_live_list(pid,target) and not app.toggle_live_task(pid,target,tid)
        app._data_read_only = False
        empty = app.new_list_object('Leere Quelle', [])
        app.lists.append(empty); app.save_items()
        empty_target = mod.glide_objects.uri('list',empty['id'])
        assert app.choose_live_list(pid,empty_target); idle()
        with patch.object(app,'themed_choice_dialog',return_value=empty_target): app.rich_note_editor.choose_live_target()
        assert app.rich_note_editor.live_tree.get_children() == ('_empty',)
        depth = len(app.undo_stack); assert not app.toggle_live_task(pid,empty_target,'_empty')
        assert len(app.undo_stack) == depth and app.remove_live_list(pid,empty_target)
        idle()
        checks.append('Live-Liste: Original-ID, Unteraufgabe, Tastatur-Abhaken/Details, ein Undo; Lösen erhält Quelle; Speicherfehler/Schreibschutz')
        with app.sidebar_change(refresh_tree=True) as change:
            entry(sid)['title'] = 'Projekt umbenannt'; item(tid)['text'] = 'Neuer Titel'; change.mark()
        assert 'Neuer Titel' in app.rich_note_editor.live_tree.item(tid,'text')
        app.set_archived('list',sid,True); idle()
        assert mod.glide_pages.live_rows(target,app.lists,app.trash)[0] == 'archived'
        assert not app.toggle_live_task(pid,target,tid)
        app.set_archived('list',sid,False); idle()
        with patch.object(app,'ask_yes_no',return_value=True): app.delete_list_by_id(sid)
        idle(); assert mod.glide_pages.live_rows(target,app.lists,app.trash)[0] == 'trash'
        assert entry(pid)['live_lists'] == [target] and not app.toggle_live_task(pid,target,tid)
        app.undo_last_change(); idle(); assert mod.glide_pages.live_rows(target,app.lists,app.trash)[0] == 'active'
        assert app.choose_live_list(pid,'glide://list/missing') is False
        checks.append('Frische Titel und Zustände nach Umbenennen, Archiv, Papierkorb und Undo; fehlende Ziele')
        image = Path(directory,'titel.png'); model = mod.glide_drawing.DrawingModel(size=16)
        model.fill(0, 0, '#5264A8')
        model.paint_cells(((x,y) for x in range(3,13) for y in range(4,12)), '#D9DFFF')
        image.write_bytes(model.to_png(scale=4)); image_bytes = image.read_bytes()
        depth = len(app.undo_stack); assert app.choose_page_cover(pid,path=str(image)); idle()
        assert len(app.undo_stack) == depth+1 and entry(pid)['cover']['kind'] == 'image'
        attachment_id = entry(pid)['cover']['attachment']
        attachment = next(a for a in entry(pid)['attachments'] if a['id'] == attachment_id)
        assert Path(app.resolve_attachment_path(attachment)).read_bytes() == image_bytes
        assert app.rich_note_editor._cover_host.winfo_children()[0]._photo is not None
        old = copy.deepcopy(app.lists); files = sorted(Path(mod.ATTACHMENTS_DIR).iterdir()); depth = len(app.undo_stack)
        with patch.object(app,'save_items',return_value=False): assert not app.choose_page_cover(pid,path=str(image))
        assert app.lists == old and sorted(Path(mod.ATTACHMENTS_DIR).iterdir()) == files and len(app.undo_stack) == depth
        assert app.choose_page_cover(pid,drawing=True,drawing_id=did); idle()
        snapshot = copy.deepcopy(entry(pid)['cover'])
        assert snapshot['document'] == entry(did)['drawing']
        changed_drawing = mod.glide_drawing.DrawingModel.from_document(entry(did)['drawing'])
        changed_drawing.set_cell(0, 0, '#FF0000')
        entry(did)['drawing'] = changed_drawing.to_document()
        assert entry(pid)['cover'] == snapshot
        app.undo_last_change(); idle(); assert entry(pid)['cover']['kind'] == 'image'
        checks.append('Bilddatei bytegleich, native Vorschau, Pixelzeichnung als unabhängiges Titelbild, Undo und Speicherfehler ohne Dateireste')
        app.duplicate_list(pid); idle(); duplicate = app.current_list()
        assert duplicate['cover'] == entry(pid)['cover'] and duplicate['live_lists'] == [target]
        assert duplicate['items'] == []
        app.undo_last_change(); idle()
        copied = copy.deepcopy([entry(sid),entry(pid)])
        app.prepare_additive_import(copied,[],[]); mapping = app._additive_import_maps
        copy_page = next(e for e in copied if e['id'] == mapping['containers'][pid])
        assert copy_page['live_lists'] == [mod.glide_objects.uri('list',mapping['containers'][sid])]
        app.remap_import_attachments(copied)
        assert copy_page['cover']['attachment'] != attachment_id
        assert any(a['id'] == copy_page['cover']['attachment'] for a in copy_page['attachments'])
        backup = Path(directory,'projekt.glidebackup')
        app.write_complete_backup(str(backup),app.complete_backup_payload())
        assert app.import_full_backup(additive=True,path=str(backup),show_success=False), errors
        idle()
        imported = next(e for e in app.lists if e['title'] == entry(pid)['title'] and e['id'] != pid)
        assert imported['live_lists'] != [target] and mod.glide_pages.live_rows(imported['live_lists'][0],app.lists)[0] == 'active'
        imported_attachment = next(a for a in imported['attachments'] if a['id'] == imported['cover']['attachment'])
        assert Path(app.resolve_attachment_path(imported_attachment)).read_bytes() == image_bytes
        app.undo_last_change(); idle()
        app.set_active_list(pid); idle()
        with patch.object(app,'ask_yes_no',return_value=True): app.delete_list_by_id(pid)
        trash_id = next(t['id'] for t in app.trash if (t.get('list') or {}).get('id') == pid)
        app.set_trash_view(); idle(); app.tree.selection_set('trash:'+trash_id); app.restore_selected_trash_entries(); idle()
        assert entry(pid)['cover']['attachment'] == attachment_id and entry(pid)['live_lists'] == [target]
        checks.append('Kopie/echtes Backup mit Anhängen/additiver Import remappen gemeinsam; Papierkorb-Wiederherstellung erhält Bild und Live-Liste')
        # Actual modal preview: inspect filled text, cancel, then accept with Return.
        template = copy.deepcopy(next(t for t in app.templates if t.get('kind') == 'list' and 'payload' in t))
        template.update(id='preview18',title='Projekt {{Projekt}}',schedule_anchor=(date.today()-timedelta(days=7)).isoformat())
        template['payload']['lists'] = [copy.deepcopy(entry(pid))]
        template['payload']['active_list_id'] = pid
        template['payload']['active_folder_id'] = None
        template['payload']['lists'][0]['items'] = [copy.deepcopy(item(tid))]
        template['payload']['lists'][0]['items'][0].update(due=(date.today()-timedelta(days=5)).isoformat(),done=True)
        # Capture the actual attachment bytes in the template format.
        import base64
        template['files'] = {a['storage']:base64.b64encode(Path(app.resolve_attachment_path(a)).read_bytes()).decode('ascii')
                             for a in template['payload']['lists'][0]['attachments']}
        app.templates.append(template)
        app.ask_template_fields = lambda fields,title='': {'Projekt':'Alpha'}
        before = copy.deepcopy((app.lists,app.folders,app.settings)); data = Path(mod.SAVE_FILE).read_bytes(); depth = len(app.undo_stack)
        seen = []
        def modal(dialog,parent=None):
            idle(); text = app._template_preview_text.get('1.0','end-1c'); seen.append(text)
            assert 'Projekt Alpha' in text and 'Unteraufgabe' in text and 'Originalaufgaben' not in text
            assert (date.today()+timedelta(days=2)).isoformat() in text
            dialog.deiconify(); dialog.focus_force(); idle(); dialog.event_generate('<Escape>'); idle()
        with patch.object(app,'run_modal',side_effect=modal): assert app.create_list_from_template('preview18') is None
        assert (app.lists,app.folders,app.settings) == before and Path(mod.SAVE_FILE).read_bytes() == data and len(app.undo_stack) == depth
        def accept(dialog,parent=None):
            dialog.deiconify(); dialog.focus_force(); idle()
            assert app._template_preview_text.cget('state') == 'disabled'
            dialog.event_generate('<Return>'); idle()
        destination = app.new_folder_object('Vorlagenziel'); app.folders.append(destination); assert app.save_items()
        depth = len(app.undo_stack); writes = []; real_write = app.write_json_atomic
        def record_write(path,data,*args,**kwargs):
            if Path(path) == Path(mod.SAVE_FILE): writes.append(copy.deepcopy(data))
            return real_write(path,data,*args,**kwargs)
        with patch.object(app,'run_modal',side_effect=accept), patch.object(app,'themed_choice_dialog',return_value='preview18'), patch.object(app,'write_json_atomic',side_effect=record_write):
            created = app.choose_creation_template(destination['id'],'lists')
        assert created['folder_id'] == destination['id'] and len(app.undo_stack) == depth + 1
        persisted = [e for data in writes for e in data.get('lists',[]) if e['id'] == created['id']]
        assert persisted and all(e['folder_id'] == destination['id'] for e in persisted),persisted

        assert created and created['title'] == 'Projekt Alpha', (created, errors)
        assert created['items'][0]['due'] == (date.today()+timedelta(days=2)).isoformat() and not created['items'][0]['done']
        app.undo_last_change(); idle()
        # Built-in pages also pass through a real preview, and cancellation has no effects.
        with patch.object(app,'confirm_template_preview',return_value=False) as confirmation:
            before = copy.deepcopy(app.lists); assert app.create_page_from_template('besprechung') is None
            assert app.lists == before and confirmation.called
        with patch.object(app,'confirm_template_preview',return_value=True), patch.object(app,'save_items',return_value=False):
            before = copy.deepcopy(app.lists); assert app.create_page_from_template('besprechung') is None
            assert app.lists == before
        with patch.object(app,'confirm_template_preview',return_value=True), patch.object(app,'save_items',return_value=False):
            before = copy.deepcopy(app.lists); assert app.create_list_from_template('preview18') is None
            assert app.lists == before
        before = copy.deepcopy((app.lists,app.folders,app.settings)); data = Path(mod.SAVE_FILE).read_bytes(); depth = len(app.undo_stack)
        ids = {e['id'] for e in app.lists}; files_before = {p.name for p in Path(mod.ATTACHMENTS_DIR).iterdir() if p.is_file()}
        def fail_new_payload(path,value,*args,**kwargs):
            if Path(path) == Path(mod.SAVE_FILE) and any(e['id'] not in ids for e in value.get('lists',[])):
                raise OSError('synthetic template commit failure')
            return real_write(path,value,*args,**kwargs)
        with patch.object(app,'confirm_template_preview',return_value=True), patch.object(app,'themed_choice_dialog',return_value='preview18'), patch.object(app,'write_json_atomic',side_effect=fail_new_payload), patch.object(app,'show_error') as reported:
            assert app.choose_creation_template(destination['id'],'lists') is None and reported.called
        assert (app.lists,app.folders,app.settings) == before and Path(mod.SAVE_FILE).read_bytes() == data and len(app.undo_stack) == depth
        assert {p.name for p in Path(mod.ATTACHMENTS_DIR).iterdir() if p.is_file()} == files_before
        checks.append('Echte gefüllte Vorschau: Unteraufgaben/gleiche Termine, Escape/Abbruch ohne Mutation, Return erzeugt geprüfte Werte im gewählten Ordner vor erstem Commit; ein Undo, atomarer Schreibfehler ohne Anhänge, Markdown-Vorlage')

        if args.capture: args.capture.mkdir(parents=True,exist_ok=True)
        sys.path.insert(0,str(REPO/'tests/tools')); from releasedaten import save_windows_screenshot
        for size in ('mittel','gross'):
            app.settings['ui_font_size'] = size; app.apply_ui_font()
            for theme in ('light','dark'):
                app.set_design(theme,apply_now=False); app.apply_theme()
                for width,height in ((1280,800),(860,700)):
                    root.geometry(f'{width}x{height}+20+20'); app.set_active_list(pid); idle(); ed = app.rich_note_editor
                    assert ed.text.winfo_height() >= 65, (size,theme,width,ed.text.winfo_height())
                    assert ed.live_tree.winfo_ismapped() and ed._cover_host.winfo_height() >= 110
                    live_style = ed.live_tree.cget('style')
                    for field, role in (('background','card'),('fieldbackground','card'),('foreground','text')):
                        assert app.style.lookup(live_style,field) == app.theme[role], (theme,field,app.style.lookup(live_style,field))
                    assert app.style.lookup(live_style,'foreground',('selected',)) == app.theme['selection_text']
                    assert app.style.lookup(live_style,'background',('selected',)) == app.theme['selection']
                    observations.append(dict(size=size,theme=theme,width=width,text_height=ed.text.winfo_height(),live_height=ed._live_host.winfo_height()))
                    if args.capture and size == 'mittel': save_windows_screenshot(root,args.capture/f'page-{theme}-{width}.png')
                    app.set_library_view(); idle()
                    surface = next(v[1] for k,v in app._library_card_cache['cards'].items() if k == ('list',pid))
                    canvas = next(c for c in surface.inner.winfo_children() if isinstance(c,mod.tk.Canvas) and hasattr(c,'_photo'))
                    assert canvas._photo is not None
                    top = surface.winfo_rooty() - app.home_content.winfo_rooty()
                    app.home_canvas.yview_moveto(max(0,top-8)/max(1,app.home_content.winfo_reqheight())); idle()
                    assert canvas.winfo_rooty() < app.home_canvas.winfo_rooty() + app.home_canvas.winfo_height()
                    assert canvas.winfo_rooty() + canvas.winfo_height() > app.home_canvas.winfo_rooty()
                    if args.capture and size == 'mittel': save_windows_screenshot(root,args.capture/f'library-{theme}-{width}.png')
        checks.append('Mindestfenster/große Schrift/hell-dunkel: Seitentext, Live-Liste und Titelbild sichtbar; Bibliotheksbilder ohne Änderung am Bestand')
        assert app.save_items(); saved_page = copy.deepcopy(entry(pid)); stop()
        root = mod.tk.Tk(); root.geometry('1280x800+20+20'); app = mod.ListApp(root)
        app.show_error = lambda *a, **kw: errors.append(repr(a)); app.show_info = lambda *a, **kw: None
        assert entry(pid)['live_lists'] == saved_page['live_lists'] and entry(pid)['cover'] == saved_page['cover']
        app.set_active_list(pid); idle(); assert app.rich_note_editor.live_tree.get_children()
        checks.append('Neustart aus gespeicherten Bytes erhält Original-IDs, Cover und Live-Liste')
        assert not errors, errors
    finally:
        if root.winfo_exists(): stop()
    with tempfile.TemporaryDirectory(prefix='glide-format23-failure-') as failed_directory:
        Path(failed_directory,'liste_speicher.json').write_bytes(original)
        failure_script = """import importlib.machinery,importlib.util,sys,pathlib
from unittest.mock import patch
l=importlib.machinery.SourceFileLoader('gate23',sys.argv[1]);m=importlib.util.module_from_spec(importlib.util.spec_from_loader(l.name,l));sys.modules[l.name]=m;l.exec_module(m)
m.ListApp.show_error=m.ListApp.show_warning=m.ListApp.show_info=lambda *a,**kw:None
r=m.tk.Tk();r.withdraw();before=pathlib.Path(m.SAVE_FILE).read_bytes()
with patch.object(m.shutil,'copy2',side_effect=OSError('synthetic backup failure')):
 a=m.ListApp(r);assert not a.save_items(show_error=False);assert pathlib.Path(m.SAVE_FILE).read_bytes()==before
a.dirty=False;a.cancel_pending_callbacks();a.release_data_lock();r.destroy()
"""
        result = subprocess.run([sys.executable,'-B','-c',failure_script,str(args.app.resolve())],
            env=dict(os.environ,GLIDE_DATA_DIR=failed_directory),capture_output=True,text=True,timeout=90)
        assert result.returncode == 0, result.stdout+result.stderr
        checks.append('Fehlgeschlagene Format-23-Vorsicherung verhindert Startmigration und Überschreiben')
    if args.previous is None:
        checks.append(vorversion.hinweis('3.33.17'))
    else:
        script = """import os,sys,hashlib,importlib.machinery,importlib.util
from pathlib import Path
os.environ['GLIDE_DATA_DIR']=sys.argv[2]
sys.path.insert(0,str(Path(sys.argv[1]).parent.parent if Path(sys.argv[1]).parent.name=='Archiv' else Path(sys.argv[1]).parent))
p=Path(sys.argv[2])/'liste_speicher.json';before=p.read_bytes()
l=importlib.machinery.SourceFileLoader('previous18',sys.argv[1]);m=importlib.util.module_from_spec(importlib.util.spec_from_loader(l.name,l));l.exec_module(m)
m.ListApp.show_error=m.ListApp.show_warning=m.ListApp.show_info=lambda *a,**kw:None
r=m.tk.Tk();r.withdraw();a=m.ListApp(r)
assert a.DATA_SCHEMA_VERSION==22 and a._data_read_only
assert not a.save_items() and p.read_bytes()==before
a.cancel_pending_callbacks();a.release_data_lock();r.destroy()
print('Unveraenderte 3.33.17: Format 23 schreibgeschuetzt; Datei bytegleich')
"""
        result = subprocess.run([sys.executable,'-B','-c',script,str(args.previous.resolve()),directory],capture_output=True,text=True,timeout=90)
        assert result.returncode == 0, result.stdout+result.stderr
        checks.append('Unveränderte 3.33.17 erkennt Format 23; Start und Speicherprobe erhalten Datei bytegenau')
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(dict(version=mod.APP_VERSION,format=23,exitcode=0,checks=checks,layouts=observations,
            app_sha256=hashlib.sha256(args.app.read_bytes()).hexdigest()),indent=2,ensure_ascii=False),encoding='utf-8')
    print(f'OK: Seiten im Alltag, {len(checks)} Pruefabschnitte, {len(observations)} Layouts')
