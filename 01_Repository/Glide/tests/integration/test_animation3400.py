"""Pixelanimation: echte Editor-/Dialogwege, Schreibfehler und Altleserschutz."""
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
import time
from unittest.mock import patch

CASES = ('frames', 'speichern', 'vorschau', 'export', 'zwischenstand', 'geometrie', 'migration')


def children(widget):
    for child in widget.winfo_children():
        yield child
        yield from children(child)


def run(app_path, cases, report, previous):
    results, callbacks, notices = [], [], []
    with tempfile.TemporaryDirectory(prefix='glide-animation3400-') as directory:
        os.environ.update(GLIDE_DATA_DIR=directory, GLIDE_TEST_MODE='1')
        sys.path.insert(0, str(app_path.parent))
        loader = importlib.machinery.SourceFileLoader('glide_animation3400', str(app_path))
        mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
        sys.modules[loader.name] = mod
        loader.exec_module(mod)
        assert callable(getattr(mod.ListApp, 'change_animation_frames', None)), 'Bildfolgenaktionen fehlen'
        assert getattr(mod, 'glide_animation', None), 'Animationsmodell fehlt'
        mod.ListApp.show_error = mod.ListApp.show_warning = mod.ListApp.show_info = lambda *a, **k: notices.append(a)
        root = mod.tk.Tk()
        root.geometry('1280x800+20+20')
        root.report_callback_exception = lambda *exc: callbacks.append(repr(exc[1]))
        app = mod.ListApp(root)
        app.ask_yes_no = lambda *a, **k: True
        saved_path = Path(mod.SAVE_FILE)
        app.create_new_drawing(size=16)
        identity = app.active_list_id
        assert identity and app.current_list().get('list_kind') == 'drawing'
        app.set_active_list(identity)

        def pump(seconds=.10):
            until = time.monotonic()+seconds
            while time.monotonic()<until:
                root.update()
                time.sleep(.005)

        def editor():
            value = app.current_drawing_editor()
            assert value is not None and value.list_id == identity
            return value

        def entry():
            return next(value for value in app.lists if value['id'] == identity)

        def document():
            return copy.deepcopy(entry()['animation'])

        def paint(color, x=0, y=0):
            value = editor()
            value.model.paint_cells([(x, y)], color)
            value.render_changes()
            value.mark_unsaved()
            assert value.flush(), 'Zeichenänderung nicht gespeichert'
            pump()

        def choose(index):
            value = editor()
            value.frame_choice.current(index)
            value.frame_choice.event_generate('<<ComboboxSelected>>')
            pump()
            assert editor().frame_id == editor().animation.frames[index].id

        def button(parent, text):
            values = [w for w in children(parent) if getattr(w, 'text', None) == text]
            assert len(values) == 1, (text, len(values))
            return values[0]

        click_time = [1000]
        def activate(widget):
            assert widget.winfo_exists() and widget.winfo_ismapped(), 'Aktionsknopf nicht sichtbar'
            widget.focus_set()
            pump(.03)
            click_time[0] += 1000
            x, y = widget.winfo_width()//2, widget.winfo_height()//2
            widget.event_generate('<ButtonPress-1>', x=x, y=y, time=click_time[0])
            widget.event_generate('<ButtonRelease-1>', x=x, y=y, time=click_time[0]+10)
            pump()

        def modal(title, opener, action):
            observed, failures = [], []
            jobs = set()
            def schedule(callback, delay):
                job = root.after(delay, callback)
                jobs.add(job)
                return job
            def inspect():
                candidates = [w for w in children(root) if isinstance(w, mod.tk.Toplevel) and w.title() == title]
                if not candidates:
                    schedule(inspect, 20)
                    return
                dialog = candidates[0]
                observed.append(dialog)
                try:
                    action(dialog)
                except BaseException as exc:
                    failures.append(exc)
                finally:
                    if dialog.winfo_exists():
                        dialog.destroy()
            def expire():
                failures.append(AssertionError(title+' nach 15 Sekunden nicht vollständig bedienbar'))
                for widget in list(children(root)):
                    if isinstance(widget, mod.tk.Toplevel):
                        widget.destroy()
            schedule(expire, 15000)
            schedule(inspect, 60)
            try:
                opener()
            finally:
                for job in jobs:
                    try:
                        root.after_cancel(job)
                    except mod.tk.TclError:
                        pass
            assert observed, title+' wurde nicht geöffnet'
            if failures:
                raise failures[0]
            pump()

        try:
            pump(.25)
            first = editor().frame_id
            if 'frames' in cases:
                paint('#123456')
                def frame_actions(dialog):
                    activate(button(dialog, 'Duplizieren'))
                    second = editor().frame_id
                    assert second != first and len(editor().animation.frames) == 2
                    assert editor().model.color_at(0, 0) == '#123456'
                    activate(button(dialog, 'Neu'))
                    third = editor().frame_id
                    assert len(editor().animation.frames) == 3 and third not in (first, second)
                    assert editor().model.color_at(0, 0) == mod.glide_drawing.BACKGROUND
                    activate(button(dialog, 'Nach links'))
                    assert [f.id for f in editor().animation.frames] == [first, third, second]
                    common = next(w for w in children(dialog) if w.winfo_name() == 'animation_common_duration')
                    own = next(w for w in children(dialog) if w.winfo_name() == 'animation_frame_duration')
                    common.delete(0, 'end');common.insert(0, '250')
                    own.delete(0, 'end');own.insert(0, '90')
                    radio = next(w for w in children(dialog) if isinstance(w, mod.tk.Radiobutton) and w.cget('text') == 'Eigene Dauer')
                    radio.invoke()
                    activate(button(dialog, 'Dauer speichern'))
                    assert editor().animation.durations() == [250, 90, 250]
                    activate(button(dialog, 'Löschen'))
                    assert [f.id for f in editor().animation.frames] == [first, second]
                modal('Bildfolge bearbeiten', lambda: activate(editor().frames_button), frame_actions)
                assert len(document()['frames']) == 2
                app.undo_last_change();pump()
                assert len(document()['frames']) == 3 and editor().animation.durations() == [250, 90, 250]
                # Zell-Undo gehört zum ausgewählten Bild, globale Struktur-Undo bleibt getrennt.
                choose(0);paint('#ABCDEF', 1, 1)
                choose(1);paint('#F01234', 2, 2)
                editor().undo();assert editor().flush();pump()
                assert editor().model.color_at(2, 2) == mod.glide_drawing.BACKGROUND
                choose(0)
                assert editor().model.color_at(1, 1) == '#ABCDEF'
                editor().undo();assert editor().flush();pump()
                assert editor().model.color_at(1, 1) == mod.glide_drawing.BACKGROUND
                results.append('Frame-Dialog: Neu/Duplizieren/Umordnen/Dauer/Löschen; globales Undo und unabhängiges Zell-Undo')
            if 'speichern' in cases:
                if len(editor().animation.frames) < 2:
                    assert app.change_animation_frames(editor(), 'new')
                    pump()
                choose(1)
                old_bytes = saved_path.read_bytes()
                current = editor()
                current.model.paint_cells([(3, 3)], '#345678')
                current.mark_unsaved()
                writer = app.write_json_atomic
                def fail_save(path, payload):
                    if Path(path) == saved_path:
                        raise OSError('synthetischer Aufgaben-Dateischreibfehler')
                    return writer(path, payload)
                with patch.object(app, 'write_json_atomic', side_effect=fail_save):
                    assert current.flush() is False and current.save_state == 'error'
                    assert not current.select_frame(current.animation.frames[0].id), 'Fehlerhafter Frame darf nicht still verlassen werden'
                assert saved_path.read_bytes() == old_bytes
                assert current.flush() and current.save_state == 'saved'
                disk_entry = next(value for value in json.loads(saved_path.read_text())['lists'] if value['id'] == identity)
                assert disk_entry['animation'] == document() and saved_path.read_bytes() != old_bytes
                assert json.loads(saved_path.read_text())['version'] == 24
                choose(0);choose(1)
                assert editor().model.color_at(3, 3) == '#345678'
                before, depth = document(), len(app.undo_stack)
                with patch.object(app, 'write_json_atomic', side_effect=fail_save):
                    assert not app.change_animation_frames(editor(), 'duplicate')
                pump()
                assert document() == before and len(app.undo_stack) == depth
                assert editor().animation.to_document() == before
                app._data_read_only = True
                assert not app.change_animation_frames(editor(), 'new')
                app._data_read_only = False
                results.append('Autosavefehler erhält Dateibytes und aktiven Frame; Retry; Strukturfehler rollt Folge und Undo zurück; Schreibschutz')
            if 'vorschau' in cases:
                if len(editor().animation.frames) < 2:
                    assert app.change_animation_frames(editor(), 'new');pump()
                assert app.change_animation_frames(editor(), 'duration', (80, None));pump()
                before, depth = document(), len(app.undo_stack)
                tracked = set(app._after_ids)
                timer = []
                def preview(dialog):
                    state = dialog._animation_preview_state
                    assert dialog._animation_preview_source == before
                    activate(button(dialog, 'Abspielen'))
                    assert state['running'] and state['job'] in app._after_ids
                    timer.append(state['job'])
                    pump(.23)
                    assert len(state['images']) <= 4
                    activate(button(dialog, 'Pause'))
                    assert not state['running'] and state['job'] is None
                    elapsed = state['elapsed'];pump(.10)
                    assert state['elapsed'] == elapsed
                    activate(button(dialog, 'Von vorn'))
                    assert state['elapsed'] == 0 and dialog._animation_preview_frame == editor().animation.frames[0].id
                    activate(button(dialog, 'Abspielen'))
                    timer.append(state['job'])
                modal('Bildfolge abspielen', lambda: activate(editor().play_animation_button), preview)
                assert not any(job in app._after_ids for job in timer)
                assert editor()._animation_preview_dialog is None and not editor()._animation_windows
                assert document() == before and len(app.undo_stack) == depth
                assert set(app._after_ids).issubset(tracked | set(root.tk.splitlist(root.tk.call('after', 'info'))))
                results.append('Vorschau: Start/Pause/Fortsetzen/Neustart; begrenzter Bildcache; Timerabbau; keine Bestandsänderung')
            if 'export' in cases:
                if len(editor().animation.frames) < 2:
                    assert app.change_animation_frames(editor(), 'duplicate');pump()
                exports = Path(directory)/'ausgabe';exports.mkdir()
                png_path = exports/'Probe.png'
                with patch.object(mod.filedialog, 'asksaveasfilename', return_value=str(png_path)):
                    app.drawing_animation_export(editor())
                manifest_path = exports/'Probe.glideanimation.json'
                assert png_path.read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
                manifest = json.loads(manifest_path.read_text())
                expected_png, expected_manifest = editor().animation.png_spritesheet()
                expected_manifest['file'] = png_path.name
                assert png_path.read_bytes() == expected_png and manifest == expected_manifest
                prior = {p.name:p.read_bytes() for p in exports.iterdir()}
                with patch.object(mod.filedialog, 'asksaveasfilename', return_value=str(png_path)), patch.object(app, 'ask_yes_no', return_value=False):
                    app.drawing_animation_export(editor())
                assert {p.name:p.read_bytes() for p in exports.iterdir()} == prior
                before_notices = len(notices)
                with patch.object(mod.filedialog, 'asksaveasfilename', return_value=str(png_path)), patch.object(mod.glide_animation_export.os, 'fsync', side_effect=OSError('synthetischer Exportfehler')):
                    app.drawing_animation_export(editor())
                assert len(notices) > before_notices and {p.name:p.read_bytes() for p in exports.iterdir()} == prior
                with patch.object(mod.filedialog, 'askdirectory', return_value=str(exports)):
                    app.drawing_animation_export(editor(), sequence=True)
                target = next(p for p in exports.iterdir() if p.is_dir())
                assert target.name.endswith(' – Bildfolge'), target.name
                assert {p.name:p.read_bytes() for p in target.iterdir()} == editor().animation.png_sequence()
                first_sequence = {p.name:p.read_bytes() for p in target.iterdir()}
                with patch.object(mod.filedialog, 'askdirectory', return_value=str(exports)):
                    app.drawing_animation_export(editor(), sequence=True)
                second = exports/(target.name+' 2')
                assert second.is_dir() and {p.name:p.read_bytes() for p in target.iterdir()} == first_sequence
                assert {p.name:p.read_bytes() for p in second.iterdir()} == first_sequence
                results.append('PNG-Spritesheet und Zeitachse bytegenau; ausdrückliches Ersetzen/Abbruch; Exportfehler ohne Teilbestand; PNG-Einzelbildfolge in neuem, lesbar benanntem Ordner')
            if 'zwischenstand' in cases:
                if len(editor().animation.frames) < 2:
                    assert app.change_animation_frames(editor(), 'duplicate');pump()
                assert editor().flush()
                full = document()
                old_bytes, old_entry = saved_path.read_bytes(), copy.deepcopy(entry())
                depth = len(app.undo_stack)
                attachment_dir = Path(mod.ATTACHMENTS_DIR)
                old_files = {p.name:p.read_bytes() for p in attachment_dir.iterdir() if p.is_file()}
                writer = app.write_json_atomic
                def snapshot_failure(path, payload):
                    if Path(path) == saved_path:
                        raise OSError('synthetischer Zwischenstands-Dateischreibfehler')
                    return writer(path, payload)
                with patch.object(app, 'themed_input_dialog', return_value='Nicht gespeichert'), \
                     patch.object(app, 'write_json_atomic', side_effect=snapshot_failure):
                    assert app.drawing_snapshot_save(editor()) is False
                pump()
                assert saved_path.read_bytes() == old_bytes and entry() == old_entry
                assert len(app.undo_stack) == depth and document() == full
                assert {p.name:p.read_bytes() for p in attachment_dir.iterdir() if p.is_file()} == old_files
                app._data_read_only = True
                with patch.object(app, 'themed_input_dialog', side_effect=AssertionError('Schreibschutz öffnet Dialog')):
                    assert app.drawing_snapshot_save(editor()) is False
                app._data_read_only = False
                with patch.object(app, 'themed_input_dialog', return_value='Ganze Folge'):
                    assert app.drawing_snapshot_save(editor()) is True
                pump()
                attachments = app.drawing_snapshots(entry())
                assert len(attachments) == 1
                stored = attachments[0]
                assert app.read_drawing_animation_snapshot(stored).to_document() == full
                assert app.read_drawing_snapshot(stored).to_document() == full['frames'][0]['drawing']
                assert app.change_animation_frames(editor(), 'new');pump()
                changed = document()
                assert changed != full
                modal('Zwischenstände', lambda: app.drawing_snapshot_dialog(editor()),
                      lambda dialog: activate(button(dialog, 'Wiederherstellen')))
                assert document() == full and editor().animation.to_document() == full
                app.undo_last_change();pump()
                assert document() == changed and editor().animation.to_document() == changed
                # Als neue Zeichnung erhält dieselben Frames/Dauern und eine neue Seitenkennung.
                count = len(app.lists)
                modal('Zwischenstände', lambda: app.drawing_snapshot_dialog(editor()),
                      lambda dialog: activate(button(dialog, 'Als neue Zeichnung')))
                assert len(app.lists) == count+1 and app.active_list_id != identity
                created = app.current_list()
                assert created['animation'] == full
                app.set_active_list(identity);pump()
                results.append('Zwischenstand: echter Schreibfehler erhält Datei/Metadaten/Undo und räumt eigenen Anhang auf; Retry und Schreibschutz; volle Wiederherstellung/Undo und Als-neue-Zeichnung')
            if 'geometrie' in cases:
                for size in ('mittel', 'gross'):
                    app.settings['ui_font_size'] = size
                    app.apply_ui_font()
                    root.geometry('860x700+20+20')
                    app.refresh_tree();pump(.25)
                    current = editor()
                    for target in (current.frame_choice, current.frames_button, current.play_animation_button,
                                   current.animation_export_button):
                        assert target.winfo_ismapped(), ('Animationsbedienung nicht sichtbar', size)
                        assert target.winfo_rootx() >= current.winfo_rootx()
                        assert target.winfo_rootx()+target.winfo_width() <= current.winfo_rootx()+current.winfo_width()+2
                    def geometry(dialog):
                        dialog.geometry('860x700');pump(.15)
                        footer = dialog._daily_footer
                        assert footer.winfo_ismapped()
                        for target in children(footer):
                            if getattr(target, 'command', None):
                                assert target.winfo_ismapped()
                                assert target.winfo_rooty()+target.winfo_height() <= dialog.winfo_rooty()+dialog.winfo_height()
                                assert target.winfo_rootx()+target.winfo_width() <= dialog.winfo_rootx()+dialog.winfo_width()
                        fields = [w for w in children(dialog._daily_body) if isinstance(w, mod.tk.Entry)]
                        for field in fields:
                            field.focus_force();pump(.10)
                            canvas = dialog._daily_scroll_canvas
                            assert field.winfo_rooty() >= canvas.winfo_rooty()-1
                            assert field.winfo_rooty()+field.winfo_height() <= canvas.winfo_rooty()+canvas.winfo_height()+1
                    modal('Bildfolge bearbeiten', lambda: activate(editor().frames_button), geometry)
                    modal('Bildfolge abspielen', lambda: activate(editor().play_animation_button), geometry)
                results.append('860 × 700 mit mittlerer/großer Schrift: Editoraktionen erreichbar, beide Dialoge scrollen und feste Fußaktionen bleiben sichtbar')
            if 'migration' in cases:
                # Neuere Fassung wird von der echten Vorversion ausschließlich lesend geöffnet.
                if previous is None:
                    repo=app_path.parents[2]
                    sys.path.insert(0,str(repo/'tests/integration'))
                    import vorversion
                    previous=vorversion.finden(repo.parent.parent,'3.39.1',repo/'CHANGELOG.md')
                if len(editor().animation.frames) < 2:
                    assert app.change_animation_frames(editor(), 'duplicate');pump()
                assert editor().flush() and app.save_items()
                full = document()
                data = saved_path.read_bytes()
                app.cancel_pending_callbacks();app.release_data_lock();root.destroy()
                script = '''import hashlib,importlib.machinery,importlib.util,os,pathlib,sys
p=pathlib.Path(os.environ['GLIDE_DATA_DIR'])/'liste_speicher.json';before=p.read_bytes()
sys.path.insert(0,str(pathlib.Path(sys.argv[1]).parent))
sys.path.append(str(pathlib.Path(sys.argv[1]).parent.parent))  # archivierte Hauptdatei: Begleitmodule der Lieferung
l=importlib.machinery.SourceFileLoader('altleser3400',sys.argv[1]);m=importlib.util.module_from_spec(importlib.util.spec_from_loader(l.name,l));l.exec_module(m)
m.ListApp.show_error=m.ListApp.show_warning=m.ListApp.show_info=lambda *a,**kw:None
r=m.tk.Tk();r.withdraw();a=m.ListApp(r)
assert a.DATA_SCHEMA_VERSION==23 and a._data_read_only
assert not a.save_items() and p.read_bytes()==before
a.cancel_pending_callbacks();a.release_data_lock();r.destroy()
print('Format 24: unveraenderte Vorversion schreibgeschuetzt, Dateibytes unveraendert')
'''
                if previous is not None:
                    result = subprocess.run([sys.executable, '-B', '-c', script, str(previous)], env=dict(os.environ), capture_output=True, text=True, timeout=90)
                    assert result.returncode == 0, result.stdout+result.stderr
                else:
                    results.append(vorversion.hinweis('3.39.1'))
                assert saved_path.read_bytes() == data
                root = mod.tk.Tk();root.geometry('1280x800+20+20')
                root.report_callback_exception = lambda *exc: callbacks.append(repr(exc[1]))
                app = mod.ListApp(root);app.set_active_list(identity);pump()
                assert document() == full and editor().animation.to_document() == full
                # Echter Startmigrationsweg, einschließlich verweigerter Vorsicherung.
                legacy = json.loads(data)
                legacy['version'] = 23
                for value in legacy['lists']:
                    value.pop('animation', None)
                legacy_bytes = (json.dumps(legacy, ensure_ascii=False)+'\n').encode('utf-8')
                migration_script = '''import importlib.machinery,importlib.util,json,os,pathlib,sys
from unittest.mock import patch
p=pathlib.Path(os.environ['GLIDE_DATA_DIR'])/'liste_speicher.json';before=p.read_bytes()
sys.path.insert(0,str(pathlib.Path(sys.argv[1]).parent))
l=importlib.machinery.SourceFileLoader('migration3400',sys.argv[1]);m=importlib.util.module_from_spec(importlib.util.spec_from_loader(l.name,l));l.exec_module(m)
m.ListApp.show_error=m.ListApp.show_warning=m.ListApp.show_info=lambda *a,**kw:None
r=m.tk.Tk();r.withdraw()
if sys.argv[2]=='failure':
 with patch.object(m.shutil,'copy2',side_effect=OSError('synthetischer Vorsicherungsfehler')):
  a=m.ListApp(r);assert not a.save_items(show_error=False);assert p.read_bytes()==before
else:
 a=m.ListApp(r);assert a.DATA_SCHEMA_VERSION==24 and json.loads(p.read_text())['version']==24
 backups=list(pathlib.Path(m.BACKUP_DIR).glob('liste_vor_format24_*.json'))
 assert len(backups)==1 and backups[0].read_bytes()==before
 old=json.loads(before);old_drawings={v['id']:v['drawing'] for v in old['lists'] if v.get('list_kind')=='drawing'}
 for v in a.lists:
  if v.get('list_kind')=='drawing':
   assert len(v['animation']['frames'])==1 and v['drawing']==old_drawings[v['id']]
a.dirty=False;a.cancel_pending_callbacks();a.release_data_lock();r.destroy()
print('Format-24-Startmigration '+sys.argv[2]+': Dateivertrag gruen')
'''
                for mode in ('failure', 'success'):
                    with tempfile.TemporaryDirectory(prefix='glide-format24-'+mode+'-') as legacy_dir:
                        Path(legacy_dir, 'liste_speicher.json').write_bytes(legacy_bytes)
                        outcome = subprocess.run([sys.executable, '-B', '-c', migration_script, str(app_path), mode],
                            env=dict(os.environ, GLIDE_DATA_DIR=legacy_dir), capture_output=True, text=True, timeout=90)
                        assert outcome.returncode == 0, outcome.stdout+outcome.stderr
                results.append(('Echter Neustart/Altleser; ' if previous is not None else 'Echter Neustart; Altleser gemäß Aufbewahrung ausgenommen; ')+'Format 23 → 24 mit bytegenauer Vorsicherung; Kopierfehler verhindert Überschreiben; statische Bilder verlustfrei')
            assert not callbacks, callbacks
        finally:
            try:
                app.dirty = False
                app.cancel_pending_callbacks();app.release_data_lock();root.destroy()
            except mod.tk.TclError:
                pass
        if report:
            report.parent.mkdir(parents=True, exist_ok=True)
            report.write_text(json.dumps(dict(app_sha256=hashlib.sha256(app_path.read_bytes()).hexdigest(),
                faelle=cases, pruefungen=results, callbackfehler=callbacks, exitcode=0), ensure_ascii=False, indent=2)+'\n')
        print('Pixelanimation: '+str(len(results))+' Gruppen grün; '+', '.join(cases))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--app', type=Path, default=Path(__file__).resolve().parents[2]/'src/glide/app.pyw')
    parser.add_argument('--previous', type=Path)
    parser.add_argument('--fall', choices=CASES)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    run(args.app.resolve(), [args.fall] if args.fall else list(CASES), args.report, args.previous.resolve() if args.previous else None)
