"""WA-37/38/40: Dialoggrenzen, Speicherergebnis und genau ein Undo."""
import argparse
from datetime import date
import copy
from contextlib import contextmanager
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


@contextmanager
def hauptdateifehler(run):
    """Hauptdatei gezielt sperren; die echte Sperrerneuerung muss durchlaufen."""
    app = run.app
    writer, writes = app.write_json_atomic, []
    def fail(path, payload):
        writes.append(Path(path).resolve())
        if Path(path).resolve() == Path(run.mod.SAVE_FILE).resolve():
            raise OSError('künstlicher Schreibfehler')
        return writer(path, payload)
    app._lock_token = dict(app._lock_token, refreshed_at='')
    with patch.object(app, 'write_json_atomic', side_effect=fail):
        yield writes
    assert Path(run.mod.LOCK_FILE).resolve() in writes, 'Sperrerneuerung nicht erreicht'
    assert Path(run.mod.SAVE_FILE).resolve() in writes, 'Hauptdateifehler nicht erreicht'


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
    with hauptdateifehler(run):
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
    with patch.object(app, 'show_undo_toast') as toast, hauptdateifehler(run):
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
    with hauptdateifehler(run):
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



def capture(app, text='Neu angelegt'):
    app.entry.delete(0, 'end')
    app.entry_placeholder_active = False
    app.entry.insert(0, text)


def fall_anlage_schreibschutz(run):
    entry, done, opened = seed(run)
    app = run.app
    capture(app)
    before, disk = copy.deepcopy(app.lists), run.datei()
    app._data_read_only = True
    try:
        app.add_item()
        assert app.lists == before and run.datei() == disk and not app.undo_stack
        assert app.get_entry_text() == 'Neu angelegt'
        with patch.object(app, 'new_item_dialog') as dialog:
            app.add_item_advanced()
            assert not dialog.called, 'Eingabedialog trotz Schreibschutz geöffnet'
    finally:
        app._data_read_only = False
    return {'beide_einstiege_ohne_mutation': True}


def fall_anlage_fehler(run):
    for advanced in (False, True):
        entry, done, opened = seed(run)
        app = run.app
        capture(app)
        app.new_item_dialog = lambda *a, **k: {'text':'Neu angelegt', 'list_id':entry['id']}
        disk = run.datei()
        with patch.object(app, 'feedback') as feedback, hauptdateifehler(run):
            app.add_item_advanced() if advanced else app.add_item()
        assert not feedback.called, 'Erfolg trotz Hauptdateifehler'
        assert run.datei() == disk and app.dirty and len(app.undo_stack) == 1
        assert len(app.current_list()['items']) == 3
        app.undo_last_change()
        assert {i['id'] for i in app.current_list()['items']} == {done['id'],opened['id']}
    return {'beide_dateifehler_ohne_erfolg_undo_erhalten': True}


def fall_anlage_dialog_sperre(run):
    entry, done, opened = seed(run)
    app = run.app
    capture(app)
    def dialog(*a, **k):
        app._data_read_only = True
        return {'text':'Darf nicht entstehen', 'list_id':entry['id']}
    app.new_item_dialog = dialog
    before, disk = copy.deepcopy(app.lists), run.datei()
    try:
        app.add_item_advanced()
        assert app.lists == before and run.datei() == disk and not app.undo_stack
        assert app.get_entry_text() == 'Neu angelegt'
    finally:
        app._data_read_only = False
    return {'sperrwechsel_nach_dialog_abgewehrt': True}


def fall_anlage_dialogziel(run):
    entry, done, opened = seed(run)
    app = run.app
    target = app.new_list_object('Ziel', [])
    app.lists.append(target)
    assert app.save_items()
    app.undo_stack.clear()
    def dialog(*a, **k):
        app.lists = [v for v in app.lists if v['id'] != target['id']]
        return {'text':'Kein Ersatz-Ziel', 'list_id':target['id']}
    app.new_item_dialog = dialog
    app.add_item_advanced()
    assert len(app.current_list()['items']) == 2 and not app.undo_stack
    return {'fehlendes_dialogziel_kein_fallback': True}


def fall_anlage_dialog_frisch(run):
    entry, done, opened = seed(run)
    app = run.app
    added = app.new_item('Während Dialog hinzugekommen')
    def dialog(*a, **k):
        app.lists = copy.deepcopy(app.lists)
        fresh = next(v for v in app.lists if v['id'] == entry['id'])
        fresh['items'].append(added)
        return {'text':'Aus Dialog', 'list_id':entry['id']}
    app.new_item_dialog = dialog
    app.add_item_advanced()
    saved = next(v for v in json.loads(run.datei().decode())['lists'] if v['id'] == entry['id'])
    assert {done['id'],opened['id'],added['id']} <= {i['id'] for i in saved['items']}
    assert sum(i['text']=='Aus Dialog' for i in saved['items']) == 1
    assert len(app.undo_stack) == 1
    app.undo_last_change()
    assert {i['id'] for i in app.current_list()['items']} == {done['id'],opened['id'],added['id']}
    return {'frische_liste_kein_dialogverlust': True}


def fall_anlage_dialog_art(run):
    entry, done, opened = seed(run)
    app = run.app
    target = app.new_list_object('Ziel', [])
    app.lists.append(target)
    assert app.save_items()
    app.undo_stack.clear()
    def dialog(*a, **k):
        target['list_kind'] = app.LIST_KIND_DRAWING
        return {'text':'Kein Punkt in Zeichnung', 'list_id':target['id']}
    app.new_item_dialog = dialog
    app.add_item_advanced()
    assert target['items'] == [] and not app.undo_stack
    return {'gewechselte_zielart_abgewehrt': True}


def fall_anlage_regulaer(run):
    for advanced in (False, True):
        entry, done, opened = seed(run)
        app = run.app
        capture(app)
        app.new_item_dialog = lambda *a, **k: {'text':'Neu angelegt','list_id':entry['id']}
        with patch.object(app, 'feedback') as feedback:
            app.add_item_advanced() if advanced else app.add_item()
        created = [i for i in app.current_list()['items'] if i['text']=='Neu angelegt']
        assert len(created)==1 and len(app.undo_stack)==1 and not app.dirty
        feedback.assert_called_once_with('item_created')
        identity = created[0]['id']
        app.undo_last_change();assert app.find_item(identity) is None
        app.redo_last_change();assert app.find_item(identity)
        run.neustart();assert run.app.find_item(identity)
    return {'beide_einstiege_undo_redo_neustart': True}


def fall_anlage_nachlauf(run):
    entry, done, opened = seed(run)
    app = run.app
    capture(app)
    with patch.object(app, 'refresh_tree', side_effect=run.mod.tk.TclError('Nachlauf')):
        app.add_item()
    stored = next(v for v in json.loads(run.datei().decode())['lists'] if v['id']==entry['id'])
    assert sum(i['text']=='Neu angelegt' for i in stored['items'])==1
    assert len(app.undo_stack)==1 and app._last_save_result.data_written
    assert app._last_save_result.followup_errors
    return {'commit_bei_ui_fehler_erhalten': True}


def fall_anlage_abbruch(run):
    entry, done, opened = seed(run)
    app = run.app
    capture(app)
    app.new_item_dialog = lambda *a, **k: None
    disk = run.datei()
    app.add_item_advanced()
    assert run.datei()==disk and not app.undo_stack and app.get_entry_text()=='Neu angelegt'
    return {'dialogabbruch_ohne_mutation': True}


def fall_anlage_ordner(run):
    entry, done, opened = seed(run)
    app = run.app
    folder = app.new_folder_object('Erfassungsordner')
    app.folders.append(folder)
    assert app.save_items()
    app.view_mode = 'folder'
    app.active_folder_id = folder['id']
    capture(app,'Neue Liste')
    app.undo_stack.clear()
    with patch.object(app, 'refresh_folder_overview'):
        app.add_item()
    created=[v for v in app.lists if v['title']=='Neue Liste' and v['folder_id']==folder['id']]
    assert len(created)==1 and len(app.undo_stack)==1
    app.undo_last_change();assert not any(v['id']==created[0]['id'] for v in app.lists)
    app.redo_last_change();assert any(v['id']==created[0]['id'] for v in app.lists)
    return {'listenanlage_im_ordner_undo_redo': True}


def rest_schreibschutz(run, operation):
    entry, done, opened = seed(run)
    app = run.app
    label = app.new_label_object('Fachlabel')
    app.labels.append(label)
    entry['labels'] = [label['id']] if operation == 'page_clear' else []
    assert app.save_items()
    app.undo_stack.clear()
    app.get_selected_item_id = lambda: opened['id']
    app.current_focus_widget = lambda: None
    app.root.clipboard_get = lambda: 'Erster neuer Punkt\nZweiter neuer Punkt'
    app.new_item_dialog = lambda *a, **k: {'text':'Zusätzlich','list_id':entry['id']}
    app.themed_choice_dialog = lambda *a, **k: 'einzeln'
    before, disk = copy.deepcopy((app.lists,app.labels)), run.datei()
    calls = {
        'calendar':lambda:app.add_task_with_due(date.today()),
        'child':lambda:app.add_child_item(opened['id']),
        'sibling':lambda:app.add_sibling_item(reference_id=opened['id']),
        'field':lambda:app.update_in_progress_item(opened['id'],'importance',3),
        'label':lambda:app.toggle_in_progress_label(opened['id'],label['id']),
        'page_label':lambda:app.toggle_page_label('list',entry['id'],label['id']),
        'page_clear':lambda:app.clear_page_labels('list',entry['id']),
        'paste':app.paste_items_from_clipboard,
        'multiline':app.paste_into_entry,
        'sort':app.sort_current_list,
    }
    app._data_read_only = True
    try:
        calls[operation]()
        assert (app.lists,app.labels)==before and run.datei()==disk and not app.undo_stack, operation
    finally:
        app._data_read_only = False
    return {'operation':operation,'modell_datei_undo_unveraendert':True}


def fall_kalender_dialogziel(run):
    entry, done, opened = seed(run)
    app = run.app
    app.new_item_dialog = lambda *a, **k: {'text':'Verlorenes Ziel','list_id':'nicht-mehr-da'}
    disk = run.datei()
    assert app.add_task_with_due(date.today()) is False
    assert run.datei()==disk and len(app.current_list()['items'])==2 and not app.undo_stack
    return {'kein_kalender_fallback_auf_falsche_liste':True}


def fall_kalender_fehler(run):
    entry, done, opened = seed(run)
    app = run.app
    app.new_item_dialog = lambda *a, **k: {'text':'Aus Kalender','list_id':entry['id']}
    disk = run.datei()
    with hauptdateifehler(run):
        assert app.add_task_with_due(date.today()) is False
    assert run.datei()==disk and app.dirty and len(app.undo_stack)==1
    app.undo_last_change()
    assert len(app.current_list()['items'])==2
    return {'falscher_kalendererfolg_abgewehrt':True}


def fall_unterpunkt_frisch(run):
    entry, done, opened = seed(run)
    app = run.app
    existing = app.new_item('Zwischenzeitlicher Unterpunkt')
    def dialog(*a, **k):
        app.lists = copy.deepcopy(app.lists)
        parent = next(i for v in app.lists for i in v['items'] if i['id']==opened['id'])
        parent['children']=[existing]
        return {'text':'Frischer Unterpunkt','list_id':entry['id']}
    app.new_item_dialog = dialog
    app.add_child_item(opened['id'])
    parent = app.find_item_in_lists(opened['id'])[0]
    assert {i['text'] for i in parent['children']}=={'Zwischenzeitlicher Unterpunkt','Frischer Unterpunkt'}
    assert len(app.undo_stack)==1
    app.undo_last_change()
    assert [i['id'] for i in app.find_item_in_lists(opened['id'])[0]['children']]==[existing['id']]
    return {'frischer_elternpunkt_nach_dialog':True}


def fall_sortierung_noop(run):
    entry, done, opened = seed(run)
    app = run.app
    app.sort_current_list('alpha')
    assert not app.undo_stack, 'Identische Sortierung erzeugt Undo'
    app.sort_current_list('due')
    assert len(app.undo_stack)==1
    app.sort_current_list('due')
    assert len(app.undo_stack)==1
    app.undo_last_change()
    assert [i['id'] for i in app.current_list()['items']]==[done['id'],opened['id']]
    return {'sortierung_nur_bei_tatsaechlicher_aenderung':True}


def import_rollback_case(run, kind, append):
    entry, done, opened = seed(run)
    app = run.app
    for _ in range(app.MAX_UNDO_STEPS):
        app.snapshot_undo()
    stack_before = tuple(app.undo_stack)
    before, disk, dirty = copy.deepcopy((app.lists,app.labels)), run.datei(), app.dirty
    def parse(*a, **k):
        app.labels.append(app.new_label_object('Importlabel'))
        return [app.new_item('Darf nicht bleiben')], {'count':1}
    app.csv_rows_to_items = parse
    app.ics_events_to_items = parse
    with hauptdateifehler(run):
        try:
            if kind=='csv':
                app.import_csv_table({'path':'Import.csv'},{'text':0},append_to_current=append)
            else:
                app.import_ics_events({'name':'Import'},[],append_to_current=append)
        except ValueError:
            pass
        else:
            raise AssertionError('Fehlgeschlagener Import meldet keinen Fehler')
    assert (app.lists,app.labels)==before and run.datei()==disk, 'Import nach Schreibfehler nur teilweise zurückgenommen'
    assert tuple(app.undo_stack)==stack_before, 'Voller Undo-Stapel nach fehlgeschlagenem Import gekürzt'
    assert app.dirty==dirty
    return {'quelle':kind,'anhaengen':append,'daten_labels_undo_datei_vollstaendig_erhalten':True}


IMPORT_ROLLBACKS = ('csv_new','csv_append','ics_new','ics_append')
for _case in IMPORT_ROLLBACKS:
    _kind,_mode = _case.split('_')
    globals()['fall_import_'+_case] = lambda run,kind=_kind,append=_mode=='append': import_rollback_case(run,kind,append)


def import_followup_case(run, kind):
    seed(run)
    app = run.app
    app.undo_stack.clear()
    created = app.new_item('Gespeicherter Import')
    def parse(*a, **k):
        return [created], {'items':1}
    app.csv_rows_to_items = app.ics_events_to_items = parse
    with patch.object(app,'set_active_list',side_effect=RuntimeError('Darstellung kaputt')):
        if kind=='csv':
            target, report = app.import_csv_table({'path':'Import.csv'},{'text':0})
        else:
            target, report = app.import_ics_events({'name':'Import'},[])
    assert created in target['items'] and report['items']==1
    assert created['id'].encode() in run.datei(), 'Erfolg ohne gespeicherten Import'
    assert len(app.undo_stack)==1 and not app.dirty
    app.undo_last_change()
    assert not app.find_item_in_lists(created['id']), 'Import nicht vollständig rücknehmbar'
    return {'quelle':kind,'commit_und_ein_undo_trotz_ui_fehler':True}


for _kind in ('csv','ics'):
    globals()['fall_import_'+_kind+'_nachlauf'] = lambda run,kind=_kind: import_followup_case(run,kind)


def detail_dialog_case(run, method, readonly):
    entry, _, _ = seed(run)
    app = run.app
    group = app.new_item('Gruppe',kind=app.ITEM_KIND_GROUP,description='Alter Kontext')
    entry['items'].append(group)
    assert app.save_items()
    app.refresh_tree()
    app.get_selected_item_id = lambda: group['id']
    app.undo_stack.clear()
    before, disk = copy.deepcopy(app.lists), run.datei()
    def dialog(item):
        details=app.item_details_snapshot(item)
        details['text']='Bearbeitete Gruppe'
        if not readonly:
            app.lists=copy.deepcopy(app.lists)
            app.find_item_in_lists(group['id'])[0]['description']='Frischer Kontext'
        return details
    with patch.object(app,'themed_item_details_dialog',side_effect=dialog):
        app._data_read_only=readonly
        try:
            if method=='edit_item':app.edit_item()
            else:getattr(app,method)(group['id'])
        finally:app._data_read_only=False
    if readonly:
        assert app.lists==before and run.datei()==disk and not app.undo_stack,'Detaildialog mutiert im Schreibschutz'
    else:
        fresh=app.find_item_in_lists(group['id'])[0]
        assert fresh['text']=='Bearbeitete Gruppe' and fresh['description']=='Frischer Kontext','Staler Dialog verliert eigene oder zwischenzeitliche Änderung'
        assert len(app.undo_stack)==1
        app.undo_last_change()
        fresh=app.find_item_in_lists(group['id'])[0]
        assert fresh['text']=='Gruppe' and fresh['description']=='Frischer Kontext'
    return {'einstieg':method,'schreibschutz':readonly,'frischer_dreiwege_abgleich':not readonly}


DETAIL_DIALOGS = ('edit_item','edit_in_progress_item','edit_page_task')
for _method in DETAIL_DIALOGS:
    for _readonly in (False,True):
        globals()['fall_details_'+_method+('_schutz' if _readonly else '_frisch')] = lambda run,method=_method,readonly=_readonly: detail_dialog_case(run,method,readonly)


def fall_einfuegen_voller_undo_fehler(run):
    seed(run)
    app=run.app
    for _ in range(app.MAX_UNDO_STEPS):app.snapshot_undo()
    stack, dirty, before, disk = tuple(app.undo_stack), app.dirty, copy.deepcopy(app.lists), run.datei()
    with patch.object(app.root,'clipboard_get',return_value='Erste Aufgabe\nZweite Aufgabe'), \
            patch.object(app,'themed_choice_dialog',return_value='einzeln'),hauptdateifehler(run):
        app.paste_into_entry()
    assert app.lists==before and run.datei()==disk
    assert tuple(app.undo_stack)==stack and app.dirty==dirty,'Mehrzeiliges Einfügen verliert ältesten Undo-Schritt oder Dirty-Zustand'
    return {'voller_undo_stapel_bei_schreibfehler_erhalten':True}


def label_manager_action(run, operation, callback=None):
    app = run.app
    actions = {}
    original = app._make_dialog_button
    def button(parent, text, command, *a, **k):
        actions[text] = command
        return original(parent,text,command,*a,**k)
    def modal(dialog, *a, **k):
        try:
            run.idle()
            actions[operation]()
            if callback:
                callback()
        finally:
            dialog.destroy()
    with patch.object(app,'_make_dialog_button',side_effect=button), patch.object(app,'run_modal',side_effect=modal):
        app.open_label_manager()


def fall_labelmanager_schreibschutz(run):
    seed(run)
    app = run.app
    label = app.new_label_object('Prüflabel')
    app.labels.insert(0,label)
    assert app.save_items()
    app.undo_stack.clear()
    app.themed_input_dialog = lambda *a, **k: 'Anderer Name'
    app.choose_label_color = lambda *a, **k: 'blue'
    before,disk = copy.deepcopy((app.lists,app.labels)),run.datei()
    app._data_read_only = True
    try:
        for operation in ('Umbenennen','Farbe','Entfernen'):
            label_manager_action(run,operation)
            assert (app.lists,app.labels)==before and run.datei()==disk and not app.undo_stack,operation
    finally:
        app._data_read_only = False
    return {'drei_echte_dialogbefehle_ohne_mutation':True}


def fall_labelmanager_frisch(run):
    seed(run)
    app = run.app
    label = app.new_label_object('Prüflabel')
    app.labels.insert(0,label)
    assert app.save_items()
    app.undo_stack.clear()
    def rename(*a, **k):
        app.labels=copy.deepcopy(app.labels)
        return 'Frischer Name'
    app.themed_input_dialog = rename
    label_manager_action(run,'Umbenennen')
    assert app.get_label(label['id'])['name']=='Frischer Name' and len(app.undo_stack)==1
    app.undo_last_change()
    assert app.get_label(label['id'])['name']=='Prüflabel'
    return {'aktuelles_label_nach_dialog_ein_undo':True}


REST_READONLY = ('calendar','child','sibling','field','label','page_label','page_clear','paste','multiline','sort')
for _operation in REST_READONLY:
    globals()['fall_rest_'+_operation] = lambda run, operation=_operation: rest_schreibschutz(run,operation)


CASES = ('einfuegen_voller_undo_fehler',) + tuple('details_'+method+suffix for method in DETAIL_DIALOGS for suffix in ('_frisch','_schutz')) + ('import_csv_nachlauf', 'import_ics_nachlauf', 'label_fehler', 'label_dialoggrenze', 'schreibschutz', 'entfernen_frische_ids',
         'entfernen_sperrwechsel', 'entfernen_fehler', 'umbenennen_nachlauf', 'umbenennen_fehler_noop', 'label_abbruch', 'entfernen_verschachtelt', 'label_regulaer', 'label_sperre_limit',
         'entfernen_veraendert', 'entfernen_papierkorbgrenze', 'umbenennen_ordner', 'waechter_papierkorbliste', 'entfernen_umgeordnet', 'anlage_schreibschutz', 'anlage_fehler', 'anlage_dialog_sperre', 'anlage_dialogziel', 'anlage_dialog_frisch', 'anlage_dialog_art', 'anlage_regulaer', 'anlage_nachlauf', 'anlage_abbruch', 'anlage_ordner', 'kalender_dialogziel', 'kalender_fehler', 'unterpunkt_frisch', 'sortierung_noop', 'labelmanager_schreibschutz', 'labelmanager_frisch') + tuple('rest_'+operation for operation in REST_READONLY) + tuple('import_'+case for case in IMPORT_ROLLBACKS)


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
