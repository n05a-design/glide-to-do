"""WA-36: weitere echte Änderungswege (Abhaken, Anlegen, Löschen, Verschieben einzeln/mehrfach) messen.

Muster wie tests/qa-3.49.0/gesamtabschluss_2026-10-31/messung_mutationen.py: gleicher Bestand,
eigener Prozess je Größe, Phasen Snapshot/Speichern/Rendern und Tk-Nachlauf getrennt. Keine Codeänderung.
"""
import hashlib, json, math, platform, statistics, sys, tempfile, time
from pathlib import Path
repo = Path(sys.argv[1]).resolve(); size = int(sys.argv[2]); output = Path(sys.argv[3])
# Optional: anderer App-Stand (etwa die gelieferte Fassung in 07) für vorher/nachher.
app_pfad = Path(sys.argv[4]).resolve() if len(sys.argv) > 4 else repo/'src/glide/app.pyw'
sys.path.insert(0, str(repo/'tests/integration'))
from test_schutzrunde import Lauf

def stats(v):
    o = sorted(v); return {'median_ms': round(statistics.median(v), 2), 'p95_ms': round(o[math.ceil(.95*len(o))-1], 2), 'n': len(v)}

with tempfile.TemporaryDirectory(prefix='glide-wege-') as d:
    run = Lauf(app_pfad, str(Path(d)/'daten'))
    try:
        app = run.app; inbox = app.ensure_inbox_list(); inbox['id'] = 'perf-inbox'; inbox['items'] = []
        app.lists = [inbox]; app.active_list_id = inbox['id']; app.items = inbox['items']; app.folders = []; app.labels = []; app.trash = []
        for k in range(12):
            items = [app.new_item('Aufgabe '+str(i), item_id='point-'+str(i), description='Prüfbeschreibung '*8) for i in range(k, size, 12)]
            for item in items: item['created_at'] = '2026-10-31T10:00:00'
            app.lists.append(app.new_list_object('Messliste '+str(k), items, list_id='list-'+str(k), created_at='2026-10-31T10:00:00'))
        assert app.save_items(); app.update_sidebar_list(); app.set_active_list('list-0'); run.idle()
        fixture = hashlib.sha256(json.dumps(app.lists, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        # Gleicher Bestand trotz Erzeugungszeit: Zeitstempel (*_at) für den Vergleich ausblenden.
        def ohne_zeit(wert):
            if isinstance(wert, dict): return {k: ohne_zeit(v) for k, v in wert.items() if not k.endswith('_at')}
            if isinstance(wert, list): return [ohne_zeit(v) for v in wert]
            return wert
        fixture_ohne_zeit = hashlib.sha256(json.dumps(ohne_zeit(app.lists), sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        phasen = {n: [] for n in ('snapshot', 'save', 'render')}
        for name, method in [('snapshot', 'snapshot_undo'), ('save', 'save_items'), ('render', 'refresh_tree')]:
            original = getattr(app, method)
            def timed(*a, _n=name, _o=original, **kw):
                t = time.perf_counter()
                try: return _o(*a, **kw)
                finally: phasen[_n].append((time.perf_counter()-t)*1000)
            setattr(app, method, timed)
        liste0 = lambda: [i['id'] for i in next(e for e in app.lists if e['id'] == 'list-0')['items']]
        bulk = max(1, min(50, len(liste0())//4))
        zaehler = {'n': 0}
        def abhaken():
            assert app.toggle_item_done_anywhere('point-0')
        def anlegen():
            zaehler['n'] += 1; app.entry.delete(0, 'end'); app.entry.insert(0, f'Neu {zaehler["n"]}')
            app.entry_placeholder_active = False; vorher = len(liste0()); app.add_item(); assert len(liste0()) == vorher+1
        def loeschen():
            ziel = liste0()[-1]; app.tree.selection_set(ziel); app.tree.focus(ziel); app.delete_item(); assert ziel not in liste0()
        def verschieben_einzeln():
            ziel = liste0()[-1]; assert app.move_items_to_list([ziel], 'list-1') is not False; assert ziel not in liste0()
        def verschieben_mehrfach():
            ids = liste0()[-bulk:]; assert app.move_items_to_list(ids, 'list-1') is not False; assert not set(ids) & set(liste0())
        ergebnis = {'size': size, 'fixture_sha256': fixture, 'fixture_ohne_zeit_sha256': fixture_ohne_zeit,
                    'app_sha256': hashlib.sha256(app_pfad.read_bytes()).hexdigest(),
                    'python': platform.python_version(), 'tk': str(run.root.tk.call('info', 'patchlevel')), 'platform': platform.platform(),
                    'bulk': bulk, 'wege': {}}
        for name, aktion, runden in [('abhaken', abhaken, 11), ('anlegen', anlegen, 11), ('loeschen', loeschen, 11),
                                     ('verschieben_einzeln', verschieben_einzeln, 11), ('verschieben_mehrfach', verschieben_mehrfach, 11)]:
            app.set_active_list('list-0'); run.idle()
            gesamt, nach = [], []; ph = {n: [] for n in phasen}
            for r in range(runden):
                vor = {k: len(v) for k, v in phasen.items()}
                t = time.perf_counter(); aktion(); dauer = (time.perf_counter()-t)*1000
                t = time.perf_counter(); run.idle(); folge = (time.perf_counter()-t)*1000
                nach_aktion = {k: len(v) for k, v in phasen.items()}
                assert not app.dirty and not run.errors, (name, run.errors[-1:] if run.errors else 'dirty')
                if name != 'abhaken':
                    # Bestand je Runde gleich halten; die Rücknahme selbst wird nicht gemessen.
                    vorher_ids = liste0(); app.undo_last_change(); run.idle()
                    assert not app.dirty and not run.errors and liste0() != vorher_ids, (name, 'Undo')
                if r >= 2 or runden < 11:
                    gesamt.append(dauer); nach.append(folge)
                    for k, v in phasen.items(): ph[k].append(sum(v[vor[k]:nach_aktion[k]]))
            ergebnis['wege'][name] = {'gesamt': stats(gesamt), 'tk_nachlauf': stats(nach), 'phasen': {k: stats(v) for k, v in ph.items()}}
            print(size, name, ergebnis['wege'][name]['gesamt'], 'Nachlauf', ergebnis['wege'][name]['tk_nachlauf']['median_ms'], flush=True)
        output.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2)+'\n')
    finally:
        run.ende()
