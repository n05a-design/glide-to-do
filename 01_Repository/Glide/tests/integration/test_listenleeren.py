"""Liste leeren: frische Bestätigung, Schreibbesitz, Speicherfehler und Undo."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import traceback
from unittest.mock import patch

from test_mutationsreste import REPO, Lauf, seed


def leeren(app, entry, active):
    return app.clear_list() if active else app.clear_list_by_id(entry['id'])


def fall_schreibschutz(run):
    entry, done, opened = seed(run)
    app = run.app
    before, disk = copy.deepcopy(app.lists), run.datei()
    app._data_read_only = True
    try:
        for active in (False, True):
            leeren(app, entry, active)
            assert app.lists == before and run.datei() == disk and not app.undo_stack, 'Liste trotz Schreibschutz im RAM geleert'
    finally:
        app._data_read_only = False
    return {'beide_einstiege_ohne_ram_mutation': True}


def fall_frischer_bestand(run):
    for active in (False, True):
        entry, done, opened = seed(run)
        app = run.app
        def confirm(*a, **kw):
            app.lists = copy.deepcopy(app.lists)
            fresh = next(v for v in app.lists if v['id'] == entry['id'])
            fresh['items'][0]['text'] = 'Frischer Text'
            fresh['items'].reverse()
            app.items = fresh['items']
            return True
        app.ask_yes_no = confirm
        leeren(app, entry, active)
        assert not app.current_list()['items'], 'Veraltetes Listenobjekt statt frischem Bestand geleert'
        assert len(app.undo_stack) == 1
        app.undo_last_change()
        assert [v['id'] for v in app.current_list()['items']] == [opened['id'], done['id']]
        assert app.current_list()['items'][1]['text'] == 'Frischer Text'
    return {'beide_einstiege_frisch': True, 'umordnung_und_undo_erhalten': True}


def fall_auswahl_veraendert(run):
    for active in (False, True):
        entry, done, opened = seed(run)
        app = run.app
        extra = app.new_item('Nicht bestätigter neuer Punkt')
        disk = run.datei()
        def confirm(*a, **kw):
            entry['items'].append(extra)
            return True
        app.ask_yes_no = confirm
        leeren(app, entry, active)
        assert {v['id'] for v in app.current_list()['items']} == {done['id'], opened['id'], extra['id']}, 'Neue unbestätigte Punkte mit gelöscht'
        assert not app.undo_stack and run.datei() == disk
        assert app.save_items()
    return {'neue_ids_nicht_mit_geloescht': True, 'kein_neuer_undo_oder_schreibversuch': True}


def fall_dialogsperre(run):
    for active in (False, True):
        for gate in ('readonly', 'editor'):
            entry, done, opened = seed(run)
            app = run.app
            before, disk = copy.deepcopy(app.lists), run.datei()
            def confirm(*a, **kw):
                if gate == 'readonly':
                    app._data_read_only = True
                return True
            app.ask_yes_no = confirm
            try:
                with patch.object(app, 'prepare_inspector_switch', return_value=(gate != 'editor')):
                    leeren(app, entry, active)
                assert app.lists == before and run.datei() == disk and not app.undo_stack, 'Dialog-Sperrwechsel oder fehlgeschlagene Editorübernahme übergangen'
            finally:
                app._data_read_only = False
    return {'beide_einstiege_sperrwechsel_und_editorabbruch': True}


def fall_nachlauf(run):
    for active in (False, True):
        entry, done, opened = seed(run)
        app = run.app
        with patch.object(app, 'refresh_tree', side_effect=run.mod.tk.TclError('künstlicher UI-Nachlauffehler')):
            leeren(app, entry, active)
        stored = json.loads(run.datei().decode('utf-8'))
        assert next(v for v in stored['lists'] if v['id'] == entry['id'])['items'] == []
        assert len(app.undo_stack) == 1 and app._last_save_result.followup_errors
        app.undo_last_change()
        assert {v['id'] for v in app.current_list()['items']} == {done['id'], opened['id']}
    return {'beide_einstiege_commit_erhalten': True, 'ui_fehler_gemeldet_und_undo': True}


def fall_speicherfehler(run):
    for active in (False, True):
        entry, done, opened = seed(run)
        app = run.app
        disk = run.datei()
        with patch.object(app, 'write_json_atomic', side_effect=OSError('künstlicher Schreibfehler')):
            leeren(app, entry, active)
        assert run.datei() == disk and app.dirty and len(app.undo_stack) == 1, {
            'active': active, 'file_equal': run.datei() == disk, 'dirty': app.dirty,
            'undo': len(app.undo_stack), 'remaining': len(app.current_list()['items']),
            'messages': run.meldungen[-3:]}
        app.undo_last_change()
        assert {v['id'] for v in app.current_list()['items']} == {done['id'], opened['id']}
    return {'beide_einstiege_datei_erhalten_und_undo': True}


def fall_regulaer(run):
    entry, done, opened = seed(run)
    app = run.app
    child = app.new_item('Unterpunkt mit Zusatzfeld')
    child['zukunft'] = {'behalten': [1, 2]}
    done['children'] = [child]
    other = app.new_list_object('Hintergrund', [app.new_item('Hintergrundpunkt')])
    app.lists.append(other)
    assert app.save_items()
    app.undo_stack.clear()
    active_ids = {done['id'], opened['id'], child['id']}
    trash = copy.deepcopy(app.trash)
    app.clear_list_by_id(other['id'])
    assert app.active_list_id == entry['id'] and active_ids <= app.data_item_ids()
    assert not other['items'] and len(app.undo_stack) == 1 and app.trash == trash
    app.undo_last_change()
    assert next(v for v in app.lists if v['id'] == other['id'])['items']
    app.undo_stack.clear()
    app.clear_list()
    assert not app.current_list()['items'] and len(app.undo_stack) == 1 and app.trash == trash
    app.undo_last_change()
    assert app.find_item(child['id'])[0]['zukunft'] == {'behalten': [1, 2]}
    app.redo_last_change()
    app.undo_stack.clear()
    with patch.object(app, 'ask_yes_no') as confirm:
        app.clear_list()
        app.clear_list_by_id(entry['id'])
        assert not confirm.called and not app.undo_stack, 'Leere Liste erzeugt Bestätigung und Undo'
    run.neustart()
    assert not run.app.current_list()['items']
    assert next(v for v in run.app.lists if v['id'] == other['id'])['items']
    return {'hintergrund_ohne_ansichtswechsel': True, 'verschachtelt_undo_redo_neustart': True,
            'direktloeschen_ohne_papierkorb': True, 'leerer_noop': True}


CASES = ('schreibschutz', 'frischer_bestand', 'auswahl_veraendert', 'dialogsperre',
         'nachlauf', 'speicherfehler', 'regulaer')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--app', type=Path, default=REPO/'src/glide/app.pyw')
    parser.add_argument('--report', type=Path)
    parser.add_argument('--fall', choices=CASES)
    args = parser.parse_args()
    report = {'app_sha256': hashlib.sha256(args.app.read_bytes()).hexdigest(), 'faelle': {}, 'fehler': []}
    for name in ([args.fall] if args.fall else CASES):
        run = None
        with tempfile.TemporaryDirectory(prefix='glide-leeren-') as directory:
            try:
                run = Lauf(args.app, str(Path(directory)/'daten'))
                evidence = globals()['fall_'+name](run)
                assert not run.errors, run.errors
                report['faelle'][name] = {'ok': True, 'messung': evidence}
                print('OK', name, flush=True)
            except Exception:
                error = traceback.format_exc().replace(str(Path.home()), '%USERPROFILE%')[-2000:]
                report['faelle'][name] = {'ok': False, 'fehler': error}
                report['fehler'].append(name)
                print('ROT', name, error, flush=True)
            finally:
                if run is not None:
                    run.app.previews.close()
                    run.ende()
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return int(bool(report['fehler']))


if __name__ == '__main__':
    raise SystemExit(main())
