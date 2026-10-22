"""FP-05: echte Tk-Einstiege, ein Undo, Neustart, Fehler und Aufklapptempo."""
import argparse
import contextlib
import copy
import hashlib
import json
from pathlib import Path
import statistics
import sys
import tempfile
import time
import traceback
from unittest.mock import patch

from test_schutzrunde import Lauf

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'tests/unit'))
from test_unlinked_mentions import fixture


def seed(run):
    app = run.app
    target = app.new_list_object('Große Reise', [], list_kind='page')
    source = app.new_list_object('Reisebericht', [], list_kind='note')
    source['rich_note'] = dict(text='😀 Vorher: GROSSE\n  Reise. Danach.', spans=[], links={})
    item = app.new_item('Beschreibung prüfen', description='Die große Reise vorbereiten.')
    tasks = app.new_list_object('Arbeit', [item], note='Große Reise planen.')
    app.lists.extend([target, source, tasks])
    assert app.save_items()
    app.set_active_list(target['id']); run.idle()
    return ('list', target['id']), source['id'], tasks['id'], item['id']


def children(widget):
    for child in widget.winfo_children():
        yield child
        yield from children(child)


def fall_aufklappen(run):
    target, source, *_ = seed(run)
    app = run.app; editor = app.rich_note_editor
    run.root.geometry('860x700+20+20'); run.idle()
    with patch.object(run.mod.glide_objects, 'unlinked_mentions', wraps=run.mod.glide_objects.unlinked_mentions) as scan:
        app.refresh_tree(); run.idle()
        assert scan.call_count == 0, 'Suche beim normalen Aufbau'
        editor._mentions_button.command(); run.idle()
        assert scan.call_count == 1 and editor._mentions_open
        assert '(3)' in editor._mentions_button.text
        assert any(isinstance(w, run.mod.tk.Text) and w.tag_ranges('mention')
                   for w in children(editor._mentions_rows)), 'Keine markierte Fundstelle'
        if getattr(run, 'capture', None) and sys.platform == 'win32':
            sys.path.insert(0, str(REPO / 'tests/tools'))
            from releasedaten import save_windows_screenshot
            save_windows_screenshot(run.root, run.capture)
        editor._mentions_button.command(); run.idle()
        assert scan.call_count == 1 and not editor._mentions_open
    disk = run.datei()
    app._data_read_only = True
    editor.toggle_mentions(); run.idle()
    assert editor._mentions_open and run.datei() == disk
    assert not [w for w in children(editor._mentions_rows) if getattr(w, 'text', '') == 'Verknüpfen']
    app._data_read_only = False


def fall_link_undo_neustart(run):
    target, source, *_ = seed(run)
    app = run.app; editor = app.rich_note_editor
    editor.toggle_mentions(); run.idle()
    before = copy.deepcopy(app.lists)
    depth = len(app.undo_stack)
    buttons = [w for w in children(editor._mentions_rows) if getattr(w, 'text', '') == 'Verknüpfen']
    assert len(buttons) == 3
    buttons[0].command(); run.idle()
    assert len(app.undo_stack) == depth + 1
    assert ('list', source) in app.object_graph()[2][target]
    doc = app.object_graph()[0][('list', source)][1]['rich_note']
    assert list(doc['links'].values()) == [run.mod.glide_objects.uri(*target)]
    assert doc['text'] == '😀 Vorher: GROSSE\n  Reise. Danach.'
    assert 'Rückverweise: 1' in [w.cget('text') for w in children(editor._mentions_rows)
                                if isinstance(w, run.mod.tk.Label)]
    app.undo_last_change(); run.idle()
    assert app.lists == before
    hit = run.mod.glide_objects.unlinked_mentions(target, app.object_graph()[0])[0]
    assert app.link_unlinked_mention(target, hit)
    run.neustart()
    assert ('list', source) in run.app.object_graph()[2][target]
    doc = run.app.object_graph()[0][('list', source)][1]['rich_note']
    assert doc['text'][doc['spans'][0]['start']:doc['spans'][0]['end']] == 'GROSSE\n  Reise'


def fall_beschreibung_menu(run):
    target, source, tasks, item = seed(run)
    app = run.app
    menu = app.build_object_reference_menu(target)
    labels = [menu.entrycget(i, 'label') for i in range(menu.index('end') + 1) if menu.type(i) == 'cascade']
    assert 'Erwähnt ohne Verweis …' in labels
    sub = app._new_themed_popup_menu(menu)
    app.fill_mentions_menu(sub, target)
    hits = run.mod.glide_objects.unlinked_mentions(target, app.object_graph()[0])
    for hit in [h for h in hits if h.field != 'rich_note']:
        depth = len(app.undo_stack)
        assert app.link_unlinked_mention(target, hit)
        assert len(app.undo_stack) == depth + 1
        assert hit.source in app.object_graph()[2][target]
    assert app.object_graph()[0][('item', item)][1]['description'] == 'Die große Reise vorbereiten.'
    assert len(run.mod.glide_objects.unlinked_mentions(target, app.object_graph()[0])) == 1


def fall_veraltet_schreibschutz_fehler(run):
    target, source, *_ = seed(run)
    app = run.app
    hit = run.mod.glide_objects.unlinked_mentions(target, app.object_graph()[0])[0]
    for cause in ('text', 'ziel', 'archiv', 'readonly', 'speichern'):
        before = copy.deepcopy(app.lists); depth = len(app.undo_stack); disk = run.datei()
        if cause == 'text':
            app.object_graph()[0][hit.source][1]['rich_note']['text'] += ' geändert'
        elif cause == 'ziel':
            app.object_graph()[0][target][1]['title'] = 'Anderer Titel'
        elif cause == 'archiv':
            app.object_graph()[0][hit.source][1]['archived'] = True
        elif cause == 'readonly':
            app._data_read_only = True
        expected = copy.deepcopy(app.lists)
        with patch.object(app, 'refresh_data_lock'), (patch.object(app, 'save_items', return_value=False)
                if cause == 'speichern' else contextlib.nullcontext()):
            assert not app.link_unlinked_mention(target, hit), cause
        assert app.lists == expected and len(app.undo_stack) == depth, f'{cause}: Bestand/Stapel geändert'
        assert run.datei() == disk, f'{cause}: Datei geändert'
        app._data_read_only = False; app.lists = before; app.dirty = False
        app.sync_current_list_reference(); app.refresh_tree(); run.idle()
    # Ein voller Stapel darf beim Schreibfehler keinen alten Schritt verlieren.
    app.undo_stack[:] = [app.undo_state() for _ in range(app.MAX_UNDO_STEPS)]
    old_stack = list(app.undo_stack)
    for current in run.mod.glide_objects.unlinked_mentions(target, app.object_graph()[0]):
        with patch.object(app, 'save_items', return_value=False):
            assert not app.link_unlinked_mention(target, current)
        assert len(app.undo_stack) == len(old_stack) and all(a is b for a, b in zip(app.undo_stack, old_stack))


def fall_oeffnen_fallen(run):
    target, source, *_ = seed(run)
    hit = run.mod.glide_objects.unlinked_mentions(target, run.app.object_graph()[0])[0]
    assert run.app.open_mention(hit)
    run.idle()
    editor = run.app.rich_note_editor
    assert editor.entry_id == source
    positions = editor.text.tag_ranges('search_hit')
    assert editor.text.get(*positions) == 'GROSSE\n  Reise'
    # Ein eingebettetes Aufgabenfenster zählt in Tk als Zeichen, im Dokument nicht.
    editor.text.window_create('1.0', window=run.mod.tk.Label(editor.text, text='□'))
    assert run.app.open_mention(hit)
    positions = editor.text.tag_ranges('search_hit')
    assert editor.text.get(*positions) == 'GROSSE\n  Reise'
    duplicate = run.app.new_list_object('Große Reise', [], list_kind='page')
    run.app.lists.append(duplicate)
    assert run.app.link_unlinked_mention(target, hit)
    assert target in run.app.object_graph()[1][hit.source]
    assert ('list', duplicate['id']) not in run.app.object_graph()[1][hit.source]
    lists, trash = fixture()
    assert len(run.mod.glide_objects.unlinked_mentions(('list', 'ziel'), run.mod.glide_objects.nodes(lists, trash))) == 20


def fall_tempo(run):
    target, *_ = seed(run)
    app = run.app
    for i in range(500):
        entry = app.new_list_object(f'Seite {i}', [app.new_item(f'Punkt {i}-{j}', description='Normaler Inhalt ohne Bezug.')
                                                  for j in range(20)], list_kind='page')
        entry['rich_note'] = dict(text='Ein normaler Absatz. ' * 20, spans=[], links={})
        app.lists.append(entry)
    editor = app.rich_note_editor
    times = []
    for _ in range(5):
        start = time.perf_counter(); editor.toggle_mentions()
        times.append((time.perf_counter() - start) * 1000)
        editor.toggle_mentions()
    median = statistics.median(times)
    assert median <= 150, f'Aufklappen Median {median:.1f} ms > 150 ms'
    return dict(seiten=500, punkte=10000, aufklappen_ms=times, median_ms=median)


CASES = ('aufklappen', 'link_undo_neustart', 'beschreibung_menu', 'veraltet_schreibschutz_fehler', 'oeffnen_fallen', 'tempo')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--app', type=Path, default=REPO / 'src/glide/app.pyw')
    parser.add_argument('--report', type=Path)
    parser.add_argument('--fall', choices=CASES)
    parser.add_argument('--capture', type=Path)
    args = parser.parse_args()
    report = dict(app_sha256=hashlib.sha256(args.app.read_bytes()).hexdigest(), faelle={})
    for name in ([args.fall] if args.fall else CASES):
        run = None
        with tempfile.TemporaryDirectory(prefix='glide-fp05-') as directory:
            try:
                run = Lauf(args.app, str(Path(directory) / 'daten'))
                run.capture = args.capture
                evidence = globals()['fall_' + name](run)
                assert not run.errors, run.errors
                report['faelle'][name] = dict(ok=True, messung=evidence)
                print('OK', name, evidence or '', flush=True)
            except Exception as exc:
                report['faelle'][name] = dict(ok=False, fehler=str(exc).replace(str(Path.home()), '~')[:900],
                    traceback=traceback.format_exc().replace(str(Path.home()), '~')[-1800:])
                print('ROT', name, report['faelle'][name]['traceback'], flush=True)
            finally:
                if run is not None:
                    run.ende()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return int(any(not case['ok'] for case in report['faelle'].values()))


if __name__ == '__main__':
    raise SystemExit(main())
