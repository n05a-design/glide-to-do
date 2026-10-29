"""WA-37/38/40: Dialoggrenzen, Speicherergebnis und genau ein Undo."""
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


def seed(run):
    app = run.app
    done, opened = app.new_item('Erledigt'), app.new_item('Offen')
    done['done'] = True
    entry = app.new_list_object('Mutationsprüfung', [done, opened])
    app.lists.append(entry)
    assert app.save_items()
    app.set_active_list(entry['id'])
    run.idle()
    app.undo_stack.clear()
    return entry, done, opened


def label_dialog(app, color=None):
    app.themed_input_dialog = lambda *a, **kw: 'NeuLabel'
    app.choose_label_color = color or (lambda **kw: 'blue')


def fall_label_fehler(run):
    seed(run)
    app = run.app
    label_dialog(app)
    before = run.datei()
    with patch.object(app, 'write_json_atomic', side_effect=OSError('künstlicher Schreibfehler')):
        result = app.create_label_interactively()
    assert result is None, 'Nicht gespeichertes Label als erfolgreicher Rückgabewert'
    assert run.datei() == before
    assert app.get_label_by_name('NeuLabel') and len(app.undo_stack) == 1
    assert app.dirty, 'Nicht gespeicherte Änderung muss sichtbar ungespeichert bleiben'
    app.undo_last_change()
    assert app.get_label_by_name('NeuLabel') is None
    return {'kein_erfolgswert': True, 'ram_undo_erhalten': True, 'datei_unveraendert': True}


def fall_label_dialoggrenze(run):
    seed(run)
    app = run.app
    def color(**kw):
        app.labels.append(app.new_label_object('NeuLabel', None, 'red'))
        return 'blue'
    label_dialog(app, color)
    assert app.create_label_interactively() is None
    assert len([v for v in app.labels if v.get('name') == 'NeuLabel']) == 1
    assert not app.undo_stack
    return {'duplikat_nach_farbabfrage_abgewehrt': True}


def fall_schreibschutz(run):
    entry, done, opened = seed(run)
    app = run.app
    label_dialog(app)
    before = copy.deepcopy((app.lists, app.labels))
    disk = run.datei()
    app._data_read_only = True
    try:
        assert app.create_label_interactively() is None
        app.remove_done_items(entry['id'])
        app.apply_sidebar_rename(('list', entry['id']), 'Verboten')
        assert (app.lists, app.labels) == before, 'Schreibschutz erst nach RAM-Mutation geprüft'
        assert run.datei() == disk and not app.undo_stack
    finally:
        app._data_read_only = False
    return {'drei_einstiege_ohne_mutation': True}


def fall_entfernen_frische_ids(run):
    entry, done, opened = seed(run)
    app = run.app
    extra = app.new_item('Während des Dialogs ergänzt')
    def confirm(*a, **kw):
        app.lists = copy.deepcopy(app.lists)
        fresh = next(v for v in app.lists if v['id'] == entry['id'])
        fresh['items'].append(extra)
        app.items = fresh['items']
        return True
    app.ask_yes_no = confirm
    app.remove_done_items(entry['id'])
    fresh = next(v for v in app.lists if v['id'] == entry['id'])
    assert {v['id'] for v in fresh['items']} == {opened['id'], extra['id']}, 'Gehaltenes Objekt überschreibt frischen Dialogstand'
    assert done['id'] in app.data_item_ids() and extra['id'] in run.datei_ids()
    assert len(app.undo_stack) == 1
    app.undo_last_change()
    fresh = next(v for v in app.lists if v['id'] == entry['id'])
    assert {v['id'] for v in fresh['items']} == {done['id'], opened['id'], extra['id']}
    return {'frischer_dialogstand': True, 'papierkorb_und_ein_undo': True}


def fall_entfernen_sperrwechsel(run):
    entry, done, opened = seed(run)
    app = run.app
    before, disk = copy.deepcopy(app.lists), run.datei()
    def confirm(*a, **kw):
        app._data_read_only = True
        return True
    app.ask_yes_no = confirm
    try:
        app.remove_done_items(entry['id'])
        assert app.lists == before and run.datei() == disk and not app.undo_stack
    finally:
        app._data_read_only = False
    return {'sperre_nach_bestaetigung': True}


def fall_entfernen_fehler(run):
    entry, done, opened = seed(run)
    app = run.app
    disk = run.datei()
    with patch.object(app, 'show_undo_toast') as toast, patch.object(
            app, 'write_json_atomic', side_effect=OSError('künstlicher Schreibfehler')):
        app.remove_done_items(entry['id'])
        assert not toast.called, 'Erfolgstoast trotz fehlgeschlagenem Schreiben'
    assert run.datei() == disk and len(app.undo_stack) == 1 and app.dirty
    assert done['id'] in app.data_item_ids()
    app.undo_last_change()
    assert {v['id'] for v in app.current_list()['items']} == {done['id'], opened['id']}
    return {'kein_erfolgstoast': True, 'ram_undo_und_papierkorb_erhalten': True}


def fall_umbenennen_nachlauf(run):
    entry, done, opened = seed(run)
    app = run.app
    with patch.object(app, 'refresh_tree', side_effect=run.mod.tk.TclError('künstlicher UI-Nachlauffehler')):
        assert app.apply_sidebar_rename(('list', entry['id']), 'Gespeicherter Titel') is True
    stored = json.loads(run.datei().decode('utf-8'))
    assert next(v for v in stored['lists'] if v['id'] == entry['id'])['title'] == 'Gespeicherter Titel'
    assert len(app.undo_stack) == 1
    assert app._last_save_result is not None and app._last_save_result.followup_errors
    app.undo_last_change()
    assert app.current_list()['title'] == 'Mutationsprüfung'
    return {'commit_bleibt_erfolgreich': True, 'nachlauffehler_gemeldet': True, 'undo': True}


def fall_umbenennen_fehler_noop(run):
    entry, done, opened = seed(run)
    app = run.app
    app.apply_sidebar_rename(('list', entry['id']), entry['title'])
    assert not app.undo_stack
    before = run.datei()
    with patch.object(app, 'write_json_atomic', side_effect=OSError('künstlicher Schreibfehler')):
        assert app.apply_sidebar_rename(('list', entry['id']), 'Noch ungespeichert') is False
    assert run.datei() == before and len(app.undo_stack) == 1 and app.dirty
    app.undo_last_change()
    assert app.current_list()['title'] == 'Mutationsprüfung'
    return {'noop_ohne_undo': True, 'expliziter_schreibfehler': True, 'ruecknehmbar': True}


def fall_label_abbruch(run):
    seed(run)
    app = run.app
    label_dialog(app, lambda **kw: None)
    before, disk = copy.deepcopy(app.labels), run.datei()
    assert app.create_label_interactively() is None
    assert app.labels == before and run.datei() == disk and not app.undo_stack
    return {'farbabbruch_ohne_mutation': True}


def fall_entfernen_verschachtelt(run):
    entry, done, opened = seed(run)
    app = run.app
    child = app.new_item('Erledigter Unterpunkt')
    child['done'] = True
    done['children'] = [child]
    assert app.save_items()
    app.undo_stack.clear()
    app.remove_done_items(entry['id'])
    payload_ids = [v['id'] for record in app.trash if record.get('kind') == app.TRASH_KIND_ITEM
                   for v in app.walk_items([record['item']])]
    assert payload_ids.count(child['id']) == 1 and payload_ids.count(done['id']) == 1, 'Doppelte IDs in Eltern-/Kindpapierkorb'
    run.neustart()
    payload_ids = [v['id'] for record in run.app.trash if record.get('kind') == run.app.TRASH_KIND_ITEM
                   for v in run.app.walk_items([record['item']])]
    assert payload_ids.count(child['id']) == 1 and payload_ids.count(done['id']) == 1
    app = run.app
    for record in list(app.trash):
        if record.get('kind') == app.TRASH_KIND_ITEM and record['item']['id'] in {done['id'], child['id']}:
            assert app.restore_trash_entry(record['id'])
    parent = app.find_item_in_lists(done['id'])[0]
    assert [v['id'] for v in parent['children']] == [child['id']]
    return {'keine_doppelten_ids_im_papierkorb': True, 'neustart': True, 'hierarchie_wiederhergestellt': True}


def fall_label_regulaer(run):
    seed(run)
    app = run.app
    label_dialog(app)
    created = app.create_label_interactively()
    assert created and app.get_label_by_name('NeuLabel')['id'] == created['id']
    assert len(app.undo_stack) == 1
    app.undo_last_change()
    assert app.get_label_by_name('NeuLabel') is None
    app.redo_last_change()
    assert app.get_label_by_name('NeuLabel')['id'] == created['id']
    run.neustart()
    assert run.app.get_label_by_name('NeuLabel')['id'] == created['id']
    return {'anlegen_undo_redo_neustart': True}


def fall_label_sperre_limit(run):
    seed(run)
    app = run.app
    before, disk = copy.deepcopy(app.labels), run.datei()
    def color(**kw):
        app._data_read_only = True
        return 'blue'
    label_dialog(app, color)
    try:
        assert app.create_label_interactively() is None
        assert app.labels == before and run.datei() == disk and not app.undo_stack
    finally:
        app._data_read_only = False
    original_limit = app.MAX_LABELS
    def limit(**kw):
        app.MAX_LABELS = len(app.labels)
        return 'blue'
    label_dialog(app, limit)
    try:
        assert app.create_label_interactively() is None
        assert app.labels == before and run.datei() == disk and not app.undo_stack
    finally:
        app.MAX_LABELS = original_limit
    return {'sperre_und_limit_nach_dialog': True}


def fall_entfernen_veraendert(run):
    entry, done, opened = seed(run)
    app = run.app
    disk = run.datei()
    def confirm(*a, **kw):
        done['done'] = False
        return True
    app.ask_yes_no = confirm
    app.remove_done_items(entry['id'])
    assert done in entry['items'] and run.datei() == disk and not app.undo_stack
    assert any('inzwischen verändert' in str(v) for v in run.meldungen)
    return {'veraenderte_bestaetigte_auswahl_abgebrochen': True}


def fall_entfernen_papierkorbgrenze(run):
    entry, done, opened = seed(run)
    app = run.app
    other = app.new_item('Auch erledigt')
    other['done'] = True
    entry['items'].append(other)
    old = app.new_item('Alter Papierkorbeintrag')
    app.trash = [app.new_trash_entry(app.TRASH_KIND_ITEM, old)]
    assert app.save_items()
    app.undo_stack.clear()
    limit = app.MAX_TRASH_ENTRIES
    app.MAX_TRASH_ENTRIES = 1
    def confirm(title, message, **kw):
        assert 'höchstens 1 Einträge' in message
        return True
    app.ask_yes_no = confirm
    try:
        app.remove_done_items(entry['id'])
        assert len(app.trash) == 1 and app.trash[0]['item']['id'] == other['id']
        assert {v['id'] for v in app.current_list()['items']} == {opened['id']}
        assert len(app.undo_stack) == 1
        app.undo_last_change()
        assert {v['id'] for v in app.current_list()['items']} == {done['id'], opened['id'], other['id']}
        assert app.trash[0]['item']['id'] == old['id']
    finally:
        app.MAX_TRASH_ENTRIES = limit
    return {'bestehende_verdrängung_erlaubt': True, 'ueberlauf_vorher_benannt': True, 'ein_undo_erhaelt_original': True}


def fall_umbenennen_ordner(run):
    seed(run)
    app = run.app
    folder = app.new_folder_object('Alter Ordner')
    app.folders.append(folder)
    assert app.save_items()
    app.set_active_folder(folder['id'])
    app.undo_stack.clear()
    assert app.apply_sidebar_rename(('folder', folder['id']), 'Neuer Ordner') is True
    assert app.get_folder(folder['id'])['title'] == 'Neuer Ordner' and len(app.undo_stack) == 1
    app.undo_last_change()
    assert app.get_folder(folder['id'])['title'] == 'Alter Ordner'
    app.redo_last_change()
    run.neustart()
    assert run.app.get_folder(folder['id'])['title'] == 'Neuer Ordner'
    return {'ordner_undo_redo_neustart': True}


def fall_waechter_papierkorbliste(run):
    seed(run)
    app = run.app
    child = app.new_item('Kind im Papierkorb')
    point = app.new_item('Punkt im Papierkorb')
    point['children'] = [child]
    deleted = app.new_list_object('Gelöschte Liste', [point])
    app.trash.append(app.new_trash_entry(app.TRASH_KIND_LIST, deleted))
    assert app.save_items()
    app.undo_stack.clear()
    expected = {point['id'], child['id']}
    assert expected <= app.data_item_ids()
    disk = run.datei()
    with app.guarded_structural_change('Papierkorb-Listenprobe') as guard:
        with app.sidebar_change() as change:
            app.trash[-1]['list']['items'] = []
            change.mark()
    assert guard.aborted and change.saved is False
    assert expected <= app.data_item_ids() and run.datei() == disk
    return {'listen_und_kind_ids_erfasst': True, 'verlust_vor_schreiben_abgewehrt': True}


def fall_entfernen_umgeordnet(run):
    entry, done, opened = seed(run)
    app = run.app
    second = app.new_item('Zweite erledigte Aufgabe')
    second['done'] = True
    entry['items'].append(second)
    assert app.save_items()
    app.undo_stack.clear()
    def confirm(*a, **kw):
        entry['items'].reverse()
        return True
    app.ask_yes_no = confirm
    app.remove_done_items(entry['id'])
    assert [v['id'] for v in app.current_list()['items']] == [opened['id']], 'Reine Umordnung derselben bestätigten Auswahl darf nicht abbrechen'
    assert len(app.undo_stack) == 1
    app.undo_last_change()
    assert [v['id'] for v in app.current_list()['items']] == [second['id'], opened['id'], done['id']]
    return {'gleiche_ids_neue_reihenfolge_erlaubt': True, 'undo_haelt_frische_reihenfolge': True}


CASES = ('label_fehler', 'label_dialoggrenze', 'schreibschutz', 'entfernen_frische_ids',
         'entfernen_sperrwechsel', 'entfernen_fehler', 'umbenennen_nachlauf', 'umbenennen_fehler_noop', 'label_abbruch', 'entfernen_verschachtelt', 'label_regulaer', 'label_sperre_limit',
         'entfernen_veraendert', 'entfernen_papierkorbgrenze', 'umbenennen_ordner', 'waechter_papierkorbliste', 'entfernen_umgeordnet')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--app', type=Path, default=REPO/'src/glide/app.pyw')
    parser.add_argument('--report', type=Path)
    parser.add_argument('--fall', choices=CASES)
    args = parser.parse_args()
    report = {'app_sha256': hashlib.sha256(args.app.read_bytes()).hexdigest(), 'faelle': {}, 'fehler': []}
    for name in ([args.fall] if args.fall else CASES):
        run = None
        with tempfile.TemporaryDirectory(prefix='glide-mutationen-') as directory:
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
