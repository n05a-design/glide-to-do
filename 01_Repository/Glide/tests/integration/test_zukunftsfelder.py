"""WA-09: echte Einstellungsrundläufe, unbekannte Karten und gültige Grenzen."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import traceback
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO/'tests/integration'))
from test_schutzrunde import Lauf

FUTURE = {'nested': [1, False, None, {'text': 'Unbekanntes bewahren'}]}


def seed(run):
    app = run.app
    task = app.new_item('Bekannte Aufgabe')
    entry = app.new_list_object('WA-09', [task])
    app.lists.append(entry)
    assert app.save_items()
    app.set_active_list(entry['id'])
    raw = {'saved_filters': [{'id': 'f', 'name': 'Eigene Ansicht', 'future': copy.deepcopy(FUTURE)}],
           'open_tabs': [{'item_id': task['id'], 'list_id': entry['id'], 'future': copy.deepcopy(FUTURE)}],
           'pinboards': {scope: {'future': copy.deepcopy(FUTURE), 'cards': [
               {'item_id': task['id'], 'list_id': entry['id'], 'future': copy.deepcopy(FUTURE),
                'show': {'description': True, 'future': copy.deepcopy(FUTURE)}},
               {'item_id': 'embed:future', 'list_id': entry['id'], 'kind': 'future',
                'payload': copy.deepcopy(FUTURE)},
               {'item_id': 'deleted', 'list_id': entry['id']},
               {'item_id': 'page:deleted', 'list_id': entry['id']}],
               'connections': [{'from': task['id'], 'to': 'embed:future', 'future': copy.deepcopy(FUTURE)},
                               {'from': task['id'], 'to': 'deleted'}],
               'areas': [{'id': 'area', 'future': copy.deepcopy(FUTURE)}]}
               for scope in ('global', 'list:'+entry['id'])}}
    app.settings = app.normalize_personal_settings({**app.settings, **raw})
    return task['id'], entry['id'], raw


def verify(app, task_id):
    assert app.settings['saved_filters'][0]['future'] == FUTURE
    assert app.settings['open_tabs'][0]['future'] == FUTURE
    for board in app.settings['pinboards'].values():
        assert board['future'] == FUTURE and board['areas'][0]['future'] == FUTURE
        cards = {c['item_id']: c for c in board['cards']}
        assert set(cards) == {task_id, 'embed:future'}
        assert cards[task_id]['future'] == FUTURE
        assert cards[task_id]['show']['future'] == FUTURE
        assert cards['embed:future']['payload'] == FUTURE
        assert len(board['connections']) == 1 and board['connections'][0]['future'] == FUTURE


def fall_normalisierung(run):
    task_id, list_id, raw = seed(run)
    original = copy.deepcopy(raw)
    result = run.app.normalize_personal_settings(raw)
    assert raw == original
    assert result['pinboards']['global']['cards'][0]['future'] == FUTURE
    result['pinboards']['global']['cards'][0]['future']['nested'].append(999)
    assert raw == original
    run.app.workspace.prune()
    verify(run.app, task_id)
    return {'kontexte': 2, 'fremde_karte_erhalten': True, 'bekannte_geloeschte_entfernt': True}


def fall_persistenz(run):
    task_id, list_id, raw = seed(run)
    app = run.app
    app.workspace.prune()
    assert app.save_settings()
    verify(app, task_id)
    stored = json.loads(Path(run.mod.SETTINGS_FILE).read_text(encoding='utf-8'))
    assert stored['pinboards']['global']['future'] == FUTURE
    backup = Path(run.data).parent/'zukunft.glideapp'
    app.write_complete_backup(str(backup), app.app_backup_payload())
    run.neustart()
    app = run.app
    verify(app, task_id)
    app.set_active_list(list_id)
    app.workspace.set_mode('board')
    run.idle(3)
    assert 'embed:future' not in app.workspace.card_ids
    assert task_id in app.workspace.card_ids
    with app.item_change([task_id]) as change:
        app.find_item_in_lists(task_id)[0]['text'] = 'Bearbeitet'
        change.mark(task_id)
    app.undo_last_change()
    verify(app, task_id)
    app.settings['pinboards']['global']['future'] = {'changed': True}
    assert app.save_settings()
    assert app.restore_app_backup(str(backup), sections={
        'tasks': True, 'settings': True, 'templates': True, 'activity': True}, show_success=False)
    verify(app, task_id)
    run.neustart()
    verify(run.app, task_id)
    return {'neustarts': 2, 'app_sicherung_restore': True, 'undo': True, 'fremde_karte_nicht_gerendert': True}


def fall_bearbeitung(run):
    task_id, list_id, raw = seed(run)
    app = run.app
    app.workspace.prune()
    criteria = {key: value for key, value in app.settings['saved_filters'][0].items() if key != 'future'}
    criteria.update(name='Umbenannt', query='Bekannte')
    assert app.saved_filters.save(criteria)
    assert app.settings['saved_filters'][0]['name'] == 'Umbenannt'
    assert app.settings['saved_filters'][0]['future'] == FUTURE
    assert '_view' not in app.settings['saved_filters'][0] and '_layout' not in app.settings['saved_filters'][0]
    verify(app, task_id)
    before = copy.deepcopy(app.settings)
    disk = Path(run.mod.SETTINGS_FILE).read_bytes()
    with patch.object(app, 'write_json_atomic', side_effect=OSError('WA-09 künstlicher Fehler')):
        assert not app.saved_filters.save(dict(criteria, name='Nicht gespeichert'))
    assert app.settings == before and Path(run.mod.SETTINGS_FILE).read_bytes() == disk
    app._data_read_only = True
    try:
        assert not app.saved_filters.save(dict(criteria, name='Gesperrt'))
        assert app.settings == before and Path(run.mod.SETTINGS_FILE).read_bytes() == disk
    finally:
        app._data_read_only = False
    assert app.saved_filters.delete('f')
    run.neustart()
    assert not run.app.settings['saved_filters']
    return {'bearbeiten_ohne_zukunftsfeldverlust': True, 'schreibfehler_und_sperre': True, 'loeschen_bleibt_wirksam': True}


def fall_grenzen(run):
    mod = run.mod
    data = {'saved_filters': [{'id': str(i), 'name': 'F', '_view': {'transient': True}, 'future': FUTURE}
                              for i in range(mod.SavedFilters.MAX_FILTERS+2)],
            'pinboards': {'global': {'cards': [
                {'item_id': 'embed:'+str(i), 'list_id': 'l', 'x': -99, 'scale': 'invalid',
                 'show': {key: 'invalid' for key in mod.ItemWorkspace.CARD_SHOW_KEYS}, 'future': FUTURE}
                for i in range(mod.ItemWorkspace.MAX_CARDS+2)],
                'connections': [{'from': 'embed:0', 'to': 'embed:1', 'dash': 'invalid', 'label': 4}],
                'areas': [{'id': 'a', 'w': False}], 'layout': 'invalid'}}}
    result = mod.ListApp.normalize_personal_settings(data)
    assert len(result['saved_filters']) == mod.SavedFilters.MAX_FILTERS
    assert all('_view' not in v and v['future'] == FUTURE for v in result['saved_filters'])
    board = result['pinboards']['global']
    assert len(board['cards']) == mod.ItemWorkspace.MAX_CARDS and board['layout'] == 'free'
    assert board['cards'][0]['x'] == 0
    assert board['cards'][0]['scale'] == mod.ItemWorkspace.CARD_SCALE_DEFAULT
    assert 'show' not in board['cards'][0]
    assert 'dash' not in board['connections'][0] and 'label' not in board['connections'][0]
    assert board['areas'][0]['w'] == 480
    return {'kartenlimit': len(board['cards']), 'filterlimit': len(result['saved_filters']),
            'bekannte_felder_streng': True, 'keine_neue_semantik': True}


def fall_seitennamespace(run):
    task_id, list_id, raw = seed(run)
    app = run.app
    page = app.new_list_object('Zukunftsfelder der Seite', [], list_kind='page')
    page['rich_note'] = {'text': 'Unveränderter Seiteninhalt', 'spans': [], 'links': {}}
    app.lists.append(page)
    assert app.save_items()
    identity = 'page:'+page['id']
    board = app.settings['pinboards']['global']
    board['cards'].append({'item_id': identity, 'list_id': page['id'], 'future': copy.deepcopy(FUTURE)})
    board['connections'].append({'from': identity, 'to': 'embed:future', 'future': copy.deepcopy(FUTURE)})
    app.workspace.prune()
    assert app.save_settings()
    stored = json.loads(Path(run.mod.SETTINGS_FILE).read_text(encoding='utf-8'))
    extra = stored[run.mod.glide_pinboard_pages.KEY]['global']
    assert extra['cards'][0]['future'] == FUTURE and extra['connections'][0]['future'] == FUTURE
    run.neustart()
    app = run.app

    def verify_page():
        board = app.settings['pinboards']['global']
        card = next(c for c in board['cards'] if c['item_id'] == identity)
        assert card['future'] == FUTURE
        assert next(e for e in board['connections'] if e['from'] == identity)['future'] == FUTURE
        assert any(c['item_id'] == 'embed:future' for c in board['cards'])

    verify_page()
    app.ask_yes_no = lambda *args, **kwargs: True
    app.delete_list_by_id(page['id'])
    assert not any(c['item_id'] == identity for c in app.settings['pinboards']['global']['cards'])
    app.undo_last_change()
    verify_page()
    run.neustart()
    app = run.app
    verify_page()
    return {'seitennamespace_felder_und_kanten': True, 'loeschen_undo': True, 'neustarts': 2}


CASES = ('normalisierung', 'persistenz', 'bearbeitung', 'grenzen', 'seitennamespace')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--app', type=Path, default=REPO/'src/glide/app.pyw')
    parser.add_argument('--report', type=Path)
    parser.add_argument('--fall', choices=CASES)
    args = parser.parse_args()
    report = {'app_sha256': hashlib.sha256(args.app.read_bytes()).hexdigest(), 'faelle': {}, 'fehler': []}
    for name in ([args.fall] if args.fall else CASES):
        run = None
        with tempfile.TemporaryDirectory(prefix='glide-zukunft-') as directory:
            try:
                run = Lauf(args.app, str(Path(directory)/'daten'))
                evidence = globals()['fall_'+name](run)
                assert not run.errors, run.errors
                report['faelle'][name] = {'ok': True, 'messung': evidence}
                print('OK', name, flush=True)
            except Exception:
                error = traceback.format_exc().replace(str(Path.home()), '%USERPROFILE%')[-2500:]
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
