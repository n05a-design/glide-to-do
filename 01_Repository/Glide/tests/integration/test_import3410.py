"""Notion und Einzelrestore: echte Vorschauen, Auswahl, Speicherung und Altleser."""
import argparse
import copy
import hashlib
import importlib.machinery
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from unittest.mock import patch
from urllib.parse import quote
import zipfile

CASES = ('import', 'vergleich', 'restore', 'fehler', 'geometrie', 'migration')


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def run(app_path, cases, report=None, previous=None):
    results, callbacks, notices = [], [], []
    with tempfile.TemporaryDirectory(prefix='glide-import3410-') as temporary:
        os.environ.update(GLIDE_DATA_DIR=temporary, GLIDE_TEST_MODE='1')
        sys.path.insert(0, str(app_path.parent))
        loader = importlib.machinery.SourceFileLoader('glide_import3410', str(app_path))
        mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
        sys.modules[loader.name] = mod
        loader.exec_module(mod)
        assert callable(getattr(mod.ListApp, 'import_notion_archive', None)), 'Notion-Import fehlt'
        assert callable(getattr(mod.ListApp, 'restore_page_from_backup', None)), 'Einzelrestore fehlt'
        mod.ListApp.show_error = mod.ListApp.show_warning = mod.ListApp.show_info = lambda *a, **k: notices.append(a)
        root = mod.tk.Tk()
        root.geometry('1280x800+20+20')
        root.report_callback_exception = lambda *exc: callbacks.append(repr(exc[1]))
        app = mod.ListApp(root)
        app.ask_yes_no = lambda *a, **k: True
        directory = Path(temporary)
        disk = Path(mod.SAVE_FILE)
        source = directory/'Notion.zip'
        primary_name = 'Projekt '+'a'*32+'.md'
        child_name = 'Projekt '+'a'*32+'/Unterseite '+'b'*32+'.md'
        png = mod.glide_drawing.DrawingModel.blank(16).to_png()
        click_time = [1000]

        def pump(seconds=.10):
            deadline = time.monotonic()+seconds
            while time.monotonic() < deadline:
                root.update()
                time.sleep(.005)

        def button(parent, label):
            matches = [w for w in descendants(parent) if getattr(w, 'text', None) == label]
            assert len(matches) == 1, (label, len(matches))
            return matches[0]

        def activate(widget):
            # Wie in test_animation3400: Knopfzeilen ordnen sich nach dem ersten
            # Größenereignis an; unter Xvfb höchstens 3 s darauf warten.
            deadline = time.monotonic()+3
            while not (widget.winfo_exists() and widget.winfo_ismapped()) and time.monotonic() < deadline:
                pump(.05)
            assert widget.winfo_ismapped(), 'Aktionsknopf nicht sichtbar'
            widget.focus_set()
            pump(.03)
            click_time[0] += 1000
            x, y = widget.winfo_width()//2, widget.winfo_height()//2
            widget.event_generate('<ButtonPress-1>', x=x, y=y, time=click_time[0])
            widget.event_generate('<ButtonRelease-1>', x=x, y=y, time=click_time[0]+10)
            pump()

        def modal(title, opener, action):
            observed, failures, jobs = [], [], []
            deadline = time.monotonic()+15
            def inspect():
                matches = [w for w in descendants(root)
                           if isinstance(w, mod.tk.Toplevel) and w.title() == title]
                if not matches:
                    if time.monotonic() >= deadline:
                        failures.append(AssertionError(title+' wurde nicht geöffnet'))
                        for w in list(root.winfo_children()):
                            if isinstance(w, mod.tk.Toplevel):
                                w.destroy()
                        return
                    jobs.append(root.after(20, inspect))
                    return
                dialog = matches[0]
                observed.append(dialog)
                try:
                    action(dialog)
                except BaseException as exc:
                    failures.append(exc)
                finally:
                    if dialog.winfo_exists():
                        dialog.destroy()
            jobs.append(root.after(60, inspect))
            try:
                outcome = opener()
            finally:
                for job in jobs:
                    try:
                        root.after_cancel(job)
                    except mod.tk.TclError:
                        pass
            if failures:
                raise failures[0]
            assert observed, title+' wurde nicht geöffnet'
            pump()
            return outcome

        def export_file(changed=False):
            stream = io.BytesIO()
            with zipfile.ZipFile(stream, 'w') as archive:
                archive.writestr(primary_name,
                    '# '+('Neue Quelle' if changed else 'Projekt')+'\n\n'
                    '- [ ] Importierte Aufgabe\n\n![Foto](foto.png)\n\n'
                    '[Unterseite]('+quote(child_name)+')\n\n[Anlage](anlage.txt)')
                archive.writestr(child_name, '# Unterseite\n\nGesicherter Unterseitentext')
                archive.writestr('foto.png', png)
                archive.writestr('anlage.txt', 'Lokale Anlage')
                archive.writestr('Daten.csv', 'Name,Wert\nBeispiel,1')
            source.write_bytes(stream.getvalue())
            return stream.getvalue()

        def select(dialog, statuses=None):
            state = dialog._glide_notion_preview
            tree, plan = state['tree'], state['plan']
            ids = [str(i) for i, row in enumerate(plan.rows)
                   if statuses is None or row.status in statuses]
            assert ids, 'Keine passende Quelle in der Vorschau'
            tree.selection_set(ids)
            tree.focus(ids[0])
            tree.event_generate('<<TreeviewSelect>>')
            pump()
            return state

        def import_all():
            return modal('Notion-Export übernehmen', lambda: app.import_notion_archive(path=source),
                         lambda dialog: (select(dialog, {'new', 'changed', 'conflict', 'missing-target'}),
                                         activate(button(dialog, 'Ausgewählte übernehmen'))))

        def primary():
            return next(p for p in app.lists if (p.get('notion_source') or {}).get('key') == 'notion:'+'a'*32)

        def assets():
            folder = Path(mod.ATTACHMENTS_DIR)
            return {p.name: p.read_bytes() for p in folder.iterdir()} if folder.exists() else {}

        try:
            pump(.25)
            original = app.new_list_object('Unbeteiligte Seite', [app.new_item('Bestehende Aufgabe')],
                                           list_kind='page', rich_note={'text': 'Bestehender Text'})
            app.lists.append(original)
            app.refresh_tree()
            assert app.save_items()
            unrelated = copy.deepcopy(original)
            initial = copy.deepcopy(app.data_payload())
            raw = export_file()
            if 'import' in cases:
                def cancellation(dialog):
                    state = dialog._glide_notion_preview
                    assert not state['tree'].selection(), 'Import darf keine Seiten vorwählen'
                    activate(button(dialog, 'Ausgewählte übernehmen'))
                    assert dialog.winfo_exists(), 'Leere Auswahl darf nicht übernommen werden'
                    select(dialog, {'new'})
                    text = state['details'].get('1.0', 'end')
                    assert 'CSV-Datenbank' in text and 'Text aus dem Export:' in text
                    activate(button(dialog, 'Abbrechen'))
                depth, files = len(app.undo_stack), assets()
                assert not modal('Notion-Export übernehmen', lambda: app.import_notion_archive(path=source), cancellation)
                assert app.lists == initial['lists'] and len(app.undo_stack) == depth and assets() == files
                assert import_all(), notices
                page = primary()
                identity = page['id']
                assert len(page['items']) == 1 and page['items'][0]['text'] == 'Importierte Aufgabe'
                assert page['rich_note']['images'] and page['rich_note']['links']
                assert any(Path(app.resolve_attachment_path(a)).read_bytes() == png for a in page['attachments'])
                child = next(p for p in app.lists if p['title'] == 'Unterseite')
                assert child.get('folder_id') and app.sidebar_section_for('list', child['id']) == 'pages'
                report_page = next(p for p in app.lists if p['title'] == 'Notion-Importbericht')
                assert 'CSV-Datenbank' in report_page['rich_note']['text']
                assert Path(app.resolve_attachment_path(report_page['attachments'][0])).read_bytes() == raw
                assert next(p for p in app.lists if p['id'] == unrelated['id']) == unrelated
                assert len(app.undo_stack) == depth+1
                assert list(Path(mod.BACKUP_DIR).glob('vor_notion_import_*.glidebackup'))
                app.load_items()
                assert primary()['id'] == identity and primary()['notion_source'] == page['notion_source']
                app.undo_last_change()
                pump()
                assert app.lists == initial['lists'] and len(app.undo_stack) == depth
                assert import_all()
                results.append('Erstimport mit ausdrücklicher Auswahl/Abbruch, Vorschau/Verlustbericht, Original-ZIP, Bilder/Anhänge/Aufgaben/Seitenverweise/Unterordner; Neustart und ein echtes Undo')
            if any(case in cases for case in ('vergleich', 'restore', 'fehler', 'migration')) and not any(p.get('notion_source') for p in app.lists):
                assert import_all(), notices
            if 'vergleich' in cases:
                before, depth, files = copy.deepcopy(app.data_payload()), len(app.undo_stack), assets()
                def unchanged(dialog):
                    state = select(dialog, {'unchanged'})
                    activate(button(dialog, 'Ausgewählte übernehmen'))
                    assert dialog.winfo_exists()
                    assert all(row.status == 'unchanged' for row in state['plan'].rows)
                    activate(button(dialog, 'Abbrechen'))
                assert not modal('Notion-Export übernehmen', lambda: app.import_notion_archive(path=source), unchanged)
                assert app.lists == before['lists'] and len(app.undo_stack) == depth and assets() == files
                page = primary()
                page['rich_note']['text'] += '\nEigene Änderung'
                assert app.save_items()
                local, identity = copy.deepcopy(page), page['id']
                export_file(True)
                asked = []
                def decline(*args, **kwargs):
                    asked.append(args)
                    return False
                def conflict_decline(dialog):
                    state = select(dialog, {'conflict'})
                    text = state['details'].get('1.0', 'end')
                    assert 'Heutiger Text in Glide:' in text and 'Eigene Änderung' in text and 'Neue Quelle' in text
                    activate(button(dialog, 'Ausgewählte übernehmen'))
                    assert asked and dialog.winfo_exists()
                    activate(button(dialog, 'Abbrechen'))
                with patch.object(app, 'ask_yes_no', side_effect=decline):
                    assert not modal('Notion-Export übernehmen', lambda: app.import_notion_archive(path=source), conflict_decline)
                assert primary() == local and len(app.undo_stack) == depth
                assert import_all(), notices
                assert primary()['id'] == identity and primary()['title'] == 'Neue Quelle'
                assert len(app.undo_stack) == depth+1
                app.undo_last_change();pump()
                assert primary() == local
                results.append('Wiederimport unverändert ohne Bericht/Undo; tatsächliche Quell-/Lokalvorschau; Konfliktablehnung erhält eigenen Stand, Freigabe erhält Identität und ist rückgängig')
            if 'restore' in cases:
                page = primary()
                identity = page['id']
                page['live_lists'] = [mod.glide_objects.uri('list', unrelated['id'])]
                image_asset = next(a for a in page['attachments'] if Path(app.resolve_attachment_path(a)).read_bytes() == png)
                page['cover'] = {'kind': 'image', 'attachment': image_asset['id']}
                assert app.save_items()
                archive = directory/'Seite.glidebackup'
                saved = copy.deepcopy(page)
                app.write_complete_backup(archive, app.complete_backup_payload())
                archive_bytes = archive.read_bytes()
                page['rich_note']['text'] += '\nHeute zusätzlich'
                page['items'].append(app.new_item('Heute zusätzlich erfasst'))
                assert app.save_items()
                current, depth = copy.deepcopy(page), len(app.undo_stack)
                def restore_preview(dialog):
                    state = dialog._glide_restore_preview
                    text = state['preview'].get('1.0', 'end')
                    assert state['plan'].ready and 'Heute zusätzlich' in text and 'Sicherungsstand:' in text
                    activate(button(dialog, 'Seite wiederherstellen'))
                assert modal('Einzelne Seite wiederherstellen',
                             lambda: app.restore_page_from_backup(path=archive, page_id=identity), restore_preview), notices
                restored = app.page_entry(identity)
                assert restored['rich_note']['text'] == saved['rich_note']['text']
                assert restored['live_lists'] == saved['live_lists']
                assert any(Path(app.resolve_attachment_path(a)).read_bytes() == png for a in restored['attachments'])
                assert restored['cover']['attachment'] in {a['id'] for a in restored['attachments']}
                assert next(p for p in app.lists if p['id'] == unrelated['id']) == unrelated
                assert len(app.undo_stack) == depth+1 and archive.read_bytes() == archive_bytes
                assert list(Path(mod.BACKUP_DIR).glob('vor_seitenrestore_*.glidebackup'))
                app.undo_last_change();pump()
                assert app.page_entry(identity) == current and len(app.undo_stack) == depth
                results.append('Echter selektiver Archivrestore mit Vergleich, Bild/Cover/Aufgaben/Live-Liste, unveränderter anderer Seite/Quelle, Vorsicherung und einem Undo')
            if 'fehler' in cases:
                export_file(True)
                before, depth, files = copy.deepcopy(app.data_payload()), len(app.undo_stack), assets()
                def choose_and_fail(dialog):
                    select(dialog, {'changed', 'conflict'})
                    activate(button(dialog, 'Ausgewählte übernehmen'))
                with patch.object(app, 'write_complete_backup', side_effect=OSError('synthetische Vorsicherung verweigert')):
                    assert not modal('Notion-Export übernehmen', lambda: app.import_notion_archive(path=source), choose_and_fail)
                assert app.lists == before['lists'] and len(app.undo_stack) == depth and assets() == files
                assert any('Vorsicherung verweigert' in str(v) for v in notices)
                after_preview = [False]
                writer = app.write_json_atomic
                def fail_writer(path, payload):
                    if after_preview[0] and Path(path) == disk:
                        raise OSError('synthetischer Schreibfehler nach Vorschau')
                    return writer(path, payload)
                disk_bytes = disk.read_bytes()
                def choose_then_fail(dialog):
                    select(dialog, {'changed', 'conflict'})
                    after_preview[0] = True
                    activate(button(dialog, 'Ausgewählte übernehmen'))
                with patch.object(app, 'write_json_atomic', side_effect=fail_writer):
                    assert not modal('Notion-Export übernehmen', lambda: app.import_notion_archive(path=source), choose_then_fail)
                assert app.lists == before['lists'] and len(app.undo_stack) == depth and assets() == files
                assert disk.read_bytes() == disk_bytes
                app._data_read_only = True
                assert not app.import_notion_archive(path=source)
                assert not app.restore_page_from_backup(path=directory/'nicht-vorhanden.glidebackup')
                app._data_read_only = False
                assert app.lists == before['lists'] and assets() == files
                results.append('Vorsicherungsfehler und echter atomarer Schreibfehler nach GUI-Vorschau rollen Daten/Dateien/Undo zurück; Schreibschutz sperrt beide Einstiege')
            if 'geometrie' in cases:
                export = mod.glide_notion_archive.inspect_export(source)
                hashes, _assets, _issues = mod.glide_notion_import.current_sources(app.lists, app.resolve_attachment_path,
                                                                                  max_bytes=app.MAX_BACKUP_TOTAL_BYTES)
                records = mod.glide_source_metadata.records(app.lists)
                comparison = mod.glide_notion_reimport.compare(export, records, hashes)
                source_page = app.new_list_object('Sichtprobe', [], list_kind='page',
                                                 rich_note={'text': 'Gesicherter Text\n'*80})
                backup = dict(app.data_payload(), lists=[source_page]+copy.deepcopy(app.lists))
                plan = mod.glide_page_restore.prepare(copy.deepcopy(app.data_payload()), backup, source_page['id'], set())
                for design in ('light', 'dark'):
                    app.set_design(design, apply_now=False)
                    for size in ('mittel', 'gross'):
                        app.settings['ui_font_size'] = size
                        app.apply_ui_font();app.apply_theme()
                        root.geometry('860x700+20+20');pump(.15)
                        def geometry(dialog):
                            dialog.geometry('860x700');pump(.15)
                            footer = dialog._daily_footer
                            assert footer.winfo_ismapped()
                            for target in descendants(footer):
                                if getattr(target, 'command', None):
                                    assert target.winfo_ismapped()
                                    assert target.winfo_rootx() >= dialog.winfo_rootx()
                                    assert target.winfo_rootx()+target.winfo_width() <= dialog.winfo_rootx()+dialog.winfo_width()
                                    assert target.winfo_rooty()+target.winfo_height() <= dialog.winfo_rooty()+dialog.winfo_height()
                                    assert mod.tkfont.Font(font=target.font).measure(target.text)+24 <= target.winfo_width()
                            canvas = dialog._daily_scroll_canvas
                            canvas.yview_moveto(1);pump()
                            assert canvas.yview()[1] > .99
                            activate(button(dialog, 'Abbrechen'))
                        modal('Notion-Export übernehmen', lambda: app.notion_import_preview(export, comparison,
                              {r.key: r.target_id for r in records}), geometry)
                        modal('Einzelne Seite wiederherstellen', lambda: app.page_restore_preview(plan, backup), geometry)
                results.append('Beide Vorschauen in Hell/Dunkel, mittlerer/großer Schrift bei 860 × 700: scrollbarer Inhalt, vollständige feste Fußaktionen')
            if 'migration' in cases:
                if previous is None:
                    repo = app_path.parents[2]
                    sys.path.insert(0, str(repo/'tests/integration'))
                    import vorversion
                    previous = vorversion.finden(repo.parent.parent, '3.40.0', repo/'CHANGELOG.md')
                assert app.save_items()
                data = disk.read_bytes()
                app.cancel_pending_callbacks();app.release_data_lock();root.destroy()
                child = '''import importlib.machinery,importlib.util,json,os,pathlib,sys
from unittest.mock import patch
p=pathlib.Path(os.environ['GLIDE_DATA_DIR'])/'liste_speicher.json';before=p.read_bytes()
app_path=pathlib.Path(sys.argv[1])
sys.path.insert(0,str(app_path.parent.parent if app_path.parent.name=='Archiv' else app_path.parent))
l=importlib.machinery.SourceFileLoader('format3410',sys.argv[1]);m=importlib.util.module_from_spec(importlib.util.spec_from_loader(l.name,l));l.exec_module(m)
m.ListApp.show_error=m.ListApp.show_warning=m.ListApp.show_info=lambda *a,**kw:None
r=m.tk.Tk();r.withdraw()
if sys.argv[2]=='old':
 a=m.ListApp(r);assert a.DATA_SCHEMA_VERSION==24 and a._data_read_only
 assert not a.save_items() and p.read_bytes()==before
elif sys.argv[2]=='failure':
 with patch.object(m.shutil,'copy2',side_effect=OSError('synthetische Vorsicherung gesperrt')):
  a=m.ListApp(r);assert not a.save_items(show_error=False);assert p.read_bytes()==before
else:
 a=m.ListApp(r);assert a.DATA_SCHEMA_VERSION==25 and json.loads(p.read_text())['version']==25
 backups=list(pathlib.Path(m.BACKUP_DIR).glob('liste_vor_format25_*.json'))
 assert len(backups)==1 and backups[0].read_bytes()==before
 assert [v['id'] for v in json.loads(before)['lists']]==[v['id'] for v in a.lists]
a.dirty=False;a.cancel_pending_callbacks();a.release_data_lock();r.destroy()
'''
                if previous is not None:
                    outcome = subprocess.run([sys.executable, '-B', '-c', child, str(previous), 'old'],
                                             capture_output=True, text=True, timeout=90)
                    assert outcome.returncode == 0, outcome.stdout+outcome.stderr
                    assert disk.read_bytes() == data
                else:
                    results.append(vorversion.hinweis('3.40.0'))
                legacy = json.loads(data)
                legacy['version'] = 24
                # Ein echter Format-24-Bestand kennt weder Seiten- noch Ordnerzuordnungen.
                for page in legacy['lists']:
                    page.pop('notion_source', None)
                for folder in legacy.get('folders', []):
                    folder.pop('notion_source_key', None)
                legacy_bytes = (json.dumps(legacy, ensure_ascii=False)+'\n').encode()
                for mode in ('failure', 'success'):
                    with tempfile.TemporaryDirectory(prefix='glide-format25-'+mode+'-') as old_dir:
                        Path(old_dir, 'liste_speicher.json').write_bytes(legacy_bytes)
                        outcome = subprocess.run([sys.executable, '-B', '-c', child, str(app_path), mode],
                                                 env=dict(os.environ, GLIDE_DATA_DIR=old_dir),
                                                 capture_output=True, text=True, timeout=90)
                        assert outcome.returncode == 0, outcome.stdout+outcome.stderr
                root = mod.tk.Tk();root.geometry('1280x800+20+20')
                root.report_callback_exception = lambda *exc: callbacks.append(repr(exc[1]))
                app = mod.ListApp(root);pump()
                assert any(p.get('notion_source') for p in app.lists)
                results.append('Echter Neustart mit Quellenmetadaten; Format 24 → 25 mit bytegenauer Vorsicherung und verweigertem Kopieren; echte Vorversion schreibgeschützt gemäß Aufbewahrung')
            assert not callbacks, callbacks
        finally:
            try:
                app.dirty = False
                app.cancel_pending_callbacks();app.release_data_lock();root.destroy()
            except mod.tk.TclError:
                pass
        payload = dict(app_sha256=hashlib.sha256(app_path.read_bytes()).hexdigest(), faelle=cases,
                       pruefungen=results, callbackfehler=callbacks, exitcode=0)
        if report:
            report.parent.mkdir(parents=True, exist_ok=True)
            report.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n')
        print('Notion und Einzelrestore: '+str(len(results))+' Gruppen grün; '+', '.join(cases))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--app', type=Path, default=Path(__file__).resolve().parents[2]/'src/glide/app.pyw')
    parser.add_argument('--previous', type=Path)
    parser.add_argument('--fall', choices=CASES)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    run(args.app.resolve(), [args.fall] if args.fall else list(CASES), args.report,
        args.previous.resolve() if args.previous else None)
