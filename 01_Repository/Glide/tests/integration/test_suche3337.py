"""G14: Inhaltstreffer, Originalziele, echte Eingabe/Enter, Änderungen/Neustart.

--app <Vorversion> erlaubt die Gegenprobe gegen den bisherigen Suchvertrag.
Alle Daten entstehen unter temporärem GLIDE_DATA_DIR.
"""
import argparse
import copy
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import tempfile

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--app', type=Path, default=REPO / 'src/glide/app.pyw')
args = parser.parse_args()
sys.path.insert(0, str(REPO / 'src/glide'))

with tempfile.TemporaryDirectory(prefix='glide-suche3337-') as folder:
    os.environ['GLIDE_DATA_DIR'] = folder
    os.environ['GLIDE_TEST_MODE'] = '1'
    loader = importlib.machinery.SourceFileLoader('glide_search_test', str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    errors = []

    def start():
        root = mod.tk.Tk()
        root.withdraw()
        root.report_callback_exception = lambda *error: errors.append(repr(error[1]))
        app = mod.ListApp(root)
        root.update()
        return root, app

    def stop(app):
        app.cancel_pending_callbacks()
        app.release_data_lock()
        # Tk-Aufträge der Editor-Kinder gehören zum gerade geprüften
        # Interpreter und dürfen nicht in den Neustartlauf hineinreichen.
        for job in app.root.tk.call('after', 'info'):
            app.root.tk.call('after', 'cancel', job)
        app.root.destroy()

    root, app = start()
    try:
        page = app.new_list_object(title='Bericht', list_kind='page',
                                   rich_note={'text': 'Die Umsatzprognose prüfen.', 'spans': [], 'links': {}})
        note = app.new_list_object(title='Besprechung', list_kind='note',
                                   rich_note={'text': 'Straße zum Kunden', 'spans': [], 'links': {}})
        tasks = app.new_list_object(title='Arbeit', note='Beschaffungsplanung')
        item = app.new_item('Angebot', description='Lieferkonditionen klären')
        tasks['items'].append(item)
        title_match = app.new_list_object(title='Umsatzprognose')
        archive = app.new_list_object(title='Archivbericht', archived=True,
                                      rich_note={'text': 'Umsatzprognose Altjahr'})
        archive['items'].append(app.new_item('Geheime Altaufgabe', description='Lieferkonditionen'))
        app.lists.extend([page, note, tasks, title_match, archive])
        app.save_items()
        before = copy.deepcopy(app.lists)

        def result(query, identity):
            return next(value for value in app.quick_open_results(query)
                        if identity in value['target'])

        hits = app.quick_open_results('umsatzprognose')
        assert hits[0]['target'] == ('list', title_match['id'])
        assert sum(value['target'] == ('list', page['id']) for value in hits) == 1
        assert 'Umsatzprognose' in result('umsatzprognose', page['id'])['path']
        assert 'im Archiv' in result('umsatzprognose', archive['id'])['path']
        assert result('strasse', note['id'])['target'] == ('list', note['id'])
        assert result('beschaffung', tasks['id'])['target'] == ('list', tasks['id'])
        item_hit = result('lieferkonditionen', item['id'])
        assert item_hit['target'] == ('item', tasks['id'], item['id'])
        assert not any(archive['items'][0]['id'] in value['target']
                       for value in app.quick_open_results('lieferkonditionen'))
        assert app.lists == before, 'Suche darf Bestand und IDs nicht ändern'

        # Mehr als 200 frühere Treffer dürfen einen späten Titeltreffer nicht verdrängen.
        tasks['items'].extend(app.new_item('Unterlage', description='Rankingprobe') for _ in range(205))
        late = app.new_item('Rankingprobe zuerst')
        tasks['items'].append(late)
        assert next(value for value in app.quick_open_results('rankingprobe')
                    if value['group'] == 'Punkte')['target'][-1] == late['id']

        # Neue Objekte nach Undo/Import werden nicht durch einen Suchcache verdeckt.
        page['rich_note']['text'] = 'Neue Nachtragsklausel'
        assert result('nachtragsklausel', page['id'])
        assert not any(page['id'] in value['target'] for value in app.quick_open_results('umsatzprognose'))
        app.lists = copy.deepcopy(app.lists)
        assert result('nachtragsklausel', page['id'])

        # Tatsächliche Suchbindung: Eingabe -> Ergebnis -> Enter -> Originalseite.
        root.deiconify()
        root.geometry('860x700')
        root.update()
        app.show_quick_open()
        field = app._quick_open['entry']
        field.insert(0, 'nachtragsklausel')
        root.update()
        field.focus_force()
        root.update()
        field.event_generate('<Return>')
        root.update()
        assert app._quick_open is None and app.active_list_id == page['id']
        app.open_quick_result(item_hit)
        root.update()
        assert app.active_list_id == tasks['id'] and app.get_selected_item_id() == item['id']
        app.save_items()
    finally:
        stop(app)

    root, app = start()
    try:
        assert result('nachtragsklausel', page['id'])
        assert result('lieferkonditionen', item['id'])
        assert not errors, errors
    finally:
        stop(app)
    print('test_suche3337: OK; Inhalt, Rangfolge, IDs, Archiv, Änderungen, Enter und Neustart.')
