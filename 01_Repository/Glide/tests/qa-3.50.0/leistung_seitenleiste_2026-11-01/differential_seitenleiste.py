"""Differential: Seitenleistenzahlen und Heute-Pools für zwei App-Stände auf demselben Zufallsbestand.

Aufruf je Stand: python3 -B differential_seitenleiste.py <Glide-Repo> <app.pyw> <Keim> <ausgabe.json>
Die Ausgaben zweier Stände mit gleichem Keim müssen bytegleich sein: alle Zeilen der
Seitenleistenbäume (Text, Zähler), Heute-Zähler, Labelzähler, Ordner-/Listenzähler, Pool
und Tagespläne dreier Tage, Abschnitte von „Heute“ und Baumdurchlauf – im Anfangszustand
und nach sechs zufälligen Abhakwechseln. Bestand mit Unterpunkten bis Tiefe 4, allen
Arten, ungültigen Datumswerten, unbekannten/System-/leeren Labels, Ordnern und Archiv.
"""
import json, random, sys, tempfile
from datetime import date, timedelta
from pathlib import Path
repo = Path(sys.argv[1]).resolve(); app_pfad = Path(sys.argv[2]).resolve(); seed = int(sys.argv[3]); out = Path(sys.argv[4])
sys.path.insert(0, str(repo/'tests/integration'))
from test_schutzrunde import Lauf
rnd = random.Random(seed)
heute = date.today()
def datum():
    w = rnd.random()
    if w < .35: return None
    if w < .4: return rnd.choice(['', '  ', 'kein Datum', '2026-13-40'])
    return (heute + timedelta(days=rnd.randint(-6, 6))).isoformat() + rnd.choice(['', '', ' '])
with tempfile.TemporaryDirectory(prefix='glide-diff-') as d:
    run = Lauf(app_pfad, str(Path(d)/'daten'))
    try:
        app = run.app
        nutzer = [app.new_label_object('L'+str(i), label_id='lab-'+str(i)) for i in range(4)]
        app.labels = [l for l in app.labels if app.is_system_label(l)] + nutzer
        label_ids = [l['id'] for l in app.labels] + ['unbekannt']
        zaehler = [0]
        def punkt(tiefe):
            zaehler[0] += 1
            it = app.new_item('P'+str(zaehler[0]), item_id='p-'+str(zaehler[0]))
            it['kind'] = rnd.choice(app.ITEM_KINDS + ('task', 'task', 'fremd'))
            it['done'] = rnd.random() < .25
            it['due'] = datum(); it['planned_date'] = datum()
            if rnd.random() < .4: it['labels'] = rnd.sample(label_ids, rnd.randint(0, 3))
            if rnd.random() < .1: it['labels'] = None
            it['children'] = [punkt(tiefe+1) for _ in range(rnd.randint(0, 3))] if tiefe < 3 and rnd.random() < .3 else []
            return it
        folders = [app.new_folder_object('O1', folder_id='f1'), app.new_folder_object('O2', folder_id='f2', parent_id='f1'),
                   app.new_folder_object('O3', folder_id='f3', archived=rnd.random() < .5)]
        app.folders = folders
        inbox = app.ensure_inbox_list(); inbox['id'] = 'inbox-fix'; inbox['items'] = [punkt(0) for _ in range(rnd.randint(0, 15))]
        lists = [inbox]
        for k in range(10):
            lists.append(app.new_list_object('Liste '+str(k), [punkt(0) for _ in range(rnd.randint(0, 40))], list_id='l-'+str(k),
                         folder_id=rnd.choice([None, None, 'f1', 'f2', 'f3']), archived=rnd.random() < .15))
        app.lists = lists; app.active_list_id = 'l-0'; app.items = lists[1]['items']; app.trash = []
        assert app.save_items(); app.update_sidebar_list(); app.set_active_list('l-0'); run.idle()
        def bild():
            b = {}
            for baum in [app.system_listbox] + app.sidebar_trees():
                rows = []
                def walk(parent):
                    for iid in baum.get_children(parent):
                        rows.append([iid, baum.item(iid, 'text'), list(baum.item(iid, 'values'))]); walk(iid)
                walk('')
                b[str(baum)] = rows
            with app.render_pass():
                teile = app.plan_day_sections(apply_filters=False, day=heute.isoformat())
                b['zahlen'] = [app.count_today_view(), app.count_labelled_items(),
                               [app.folder_task_count(f['id']) for f in app.folders],
                               [app.count_items(e.get('items', [])) for e in app.lists]]
                b['pool'] = [[t[0], t[1], t[2], t[4]['id']] for t in app.today_view_pool(apply_filters=False)]
                for tag in (heute - timedelta(days=2), heute, heute + timedelta(days=3)):
                    b['plan '+tag.isoformat()] = [[t[0], t[1], t[2], t[4]['id']] for t in app.plan_day_entries(apply_filters=False, day=tag.isoformat())]
                b['teile'] = {k: [x[-1]['id'] if isinstance(x, tuple) else str(x) for x in (getattr(teile, k) or [])] for k in ('plan', 'verspaetet', 'liegen', 'faellig')}
                b['walk'] = [i['id'] for e in app.lists for i in app.walk_items(e.get('items', []))]
            return b
        bilder = [bild()]
        ids = [i['id'] for e in app.lists for i in app.walk_items(e['items'])]
        for _ in range(6):
            app.toggle_item_done_anywhere(rnd.choice(ids)); run.idle(); bilder.append(bild())
        out.write_text(json.dumps(bilder, ensure_ascii=False, default=str, indent=0))
        print(seed, 'Punkte', len(ids), 'heute', bilder[0]['zahlen'][0], 'labels', bilder[0]['zahlen'][1], 'fehler', len(run.errors))
    finally:
        run.ende()
