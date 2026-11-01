"""WA-36 Seitenleiste: Neuaufbau nach dem Speichern und Abhaken messen.

Aufruf: python3 -B messung_seitenleiste.py <Glide-Repo> <Größe> <app.pyw> gemischt|leer
„leer“: Aufgaben ohne Termin/Label (Bestfall der Vorprüfung); „gemischt“: 40 % Fälligkeit,
30 % Bearbeitungstag, 30 % Label, 20 % erledigt (fester Zufallskeim). Künstliche Daten.
"""
import json, random, statistics, sys, tempfile, time
from datetime import date, timedelta
from pathlib import Path
repo = Path(sys.argv[1]).resolve(); size = int(sys.argv[2]); app_pfad = Path(sys.argv[3]).resolve(); gemischt = sys.argv[4] == 'gemischt'
sys.path.insert(0, str(repo/'tests/integration'))
from test_schutzrunde import Lauf
rnd = random.Random(7); heute = date.today()
with tempfile.TemporaryDirectory(prefix='glide-bench-') as d:
    run = Lauf(app_pfad, str(Path(d)/'daten'))
    try:
        app = run.app; inbox = app.ensure_inbox_list(); inbox['id'] = 'perf-inbox'; inbox['items'] = []
        nutzer = [app.new_label_object('L'+str(i), label_id='lab-'+str(i)) for i in range(6)]
        app.labels = [l for l in app.labels if app.is_system_label(l)] + nutzer
        app.lists = [inbox]; app.active_list_id = inbox['id']; app.items = inbox['items']; app.folders = []; app.trash = []
        for k in range(12):
            items = []
            for i in range(k, size, 12):
                it = app.new_item('Aufgabe '+str(i), item_id='point-'+str(i), description='Prüfbeschreibung '*8)
                if gemischt:
                    if rnd.random() < .4: it['due'] = (heute + timedelta(days=rnd.randint(-20, 40))).isoformat()
                    if rnd.random() < .3: it['planned_date'] = (heute + timedelta(days=rnd.randint(-3, 5))).isoformat()
                    if rnd.random() < .3: it['labels'] = ['lab-'+str(rnd.randint(0, 5))]
                    if rnd.random() < .2: it['done'] = True
                items.append(it)
            app.lists.append(app.new_list_object('Messliste '+str(k), items, list_id='list-'+str(k)))
        assert app.save_items(); app.update_sidebar_list(); app.set_active_list('list-0'); run.idle()
        def messen(name, ziel):
            orig = getattr(app, name)
            def timed(*a, **kw):
                t = time.perf_counter()
                try: return orig(*a, **kw)
                finally: ziel.append((time.perf_counter()-t)*1000)
            setattr(app, name, timed)
        zeiten, erinnerung = [], []
        messen('update_sidebar_list', zeiten); messen('refresh_reminder_status', erinnerung)
        gesamt = []
        for r in range(13):
            t = time.perf_counter(); app.toggle_item_done_anywhere('point-0'); gesamt.append((time.perf_counter()-t)*1000); run.idle()
        print(json.dumps({'groesse': size, 'gemischt': gemischt, 'sidebar_median_ms': round(statistics.median(zeiten[2:]), 1),
                          'erinnerungsstatus_median_ms': round(statistics.median(erinnerung[2:]), 1),
                          'abhaken_median_ms': round(statistics.median(gesamt[2:]), 1), 'n': len(zeiten[2:])}))
    finally:
        run.ende()
