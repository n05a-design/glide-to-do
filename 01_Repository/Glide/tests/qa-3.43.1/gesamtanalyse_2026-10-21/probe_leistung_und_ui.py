"""Unprofilierte Windows-Messungen und eigene Testfenster; keine Nutzerdaten.

Messung und Profiling sind getrennt. Die sieben warmen Werte je Szenario
ergeben nur einen lokalen Trend; ihr p95 ist bei dieser Stichprobe der Maximalwert.
"""
import argparse
import cProfile
import gc
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import pstats
import statistics
import sys
import tempfile
import time
import traceback
import tracemalloc


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--app',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--wait-for',type=Path)
    args=parser.parse_args();out=args.out;out.mkdir(parents=True,exist_ok=True)
    if args.wait_for:
        deadline=time.monotonic()+900
        while True:
            try:
                if len(json.loads(args.wait_for.read_text(encoding='utf-8')))>=8:break
            except (OSError,ValueError):pass
            if time.monotonic()>deadline:raise TimeoutError('Bereichspruefungen nicht abgeschlossen')
            time.sleep(.2)
        time.sleep(1)
    appdir=args.app.parents[2]
    sys.path.insert(0,str(appdir/'tests/integration'))
    sys.path.insert(0,str(appdir/'tests/tools'))
    from test_schutzrunde import Lauf
    from test_ansichten import criterion
    from releasedaten import save_windows_screenshot
    report=dict(app_sha256=hashlib.sha256(args.app.read_bytes()).hexdigest(),python=platform.python_version(),
        platform=platform.system()+' '+platform.release(),processes=[],screens=[],errors=[],
        limits='Windows-Trend, drei frische Tk-Interpreter und Datenordner nacheinander in einem Python-Prozess; sieben warme Werte. Importcache bleibt erhalten. Keine Mac-Abnahme, kein Langzeit-/RSS-/DPI-/Readernachweis. Tracemalloc erfasst keine vollstaendigen nativen Tk-Allokationen.')
    def persist():
        (out/'leistung_und_ui.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    def series(run,name,fn,repeats=7):
        begin=time.perf_counter();result=fn();run.idle()
        cold=(time.perf_counter()-begin)*1000
        values=[]
        for _ in range(repeats):
            begin=time.perf_counter();result=fn();run.root.update_idletasks()
            values.append((time.perf_counter()-begin)*1000);run.idle(1)
        return dict(name=name,first_ms=round(cold,3),warm_ms=[round(v,3) for v in values],
            median_ms=round(statistics.median(values),3),p95_ms=round(sorted(values)[math.ceil(.95*len(values))-1],3))
    for process_index in range(3):
        run=None
        with tempfile.TemporaryDirectory(prefix='glide-analysis-measure-') as td:
            try:
                begin=time.perf_counter();run=Lauf(args.app,str(Path(td)/'data'))
                entry=dict(index=process_index+1,startup_with_import_ms=round((time.perf_counter()-begin)*1000,3),scenarios=[])
                report['processes'].append(entry)
                app=run.app
                report.update(tk=str(run.root.tk.call('info','patchlevel')),scaling=float(run.root.tk.call('tk','scaling')))
                for count in (100,1000,10000):
                    tasks=[app.new_item('Aufgabe '+str(i).zfill(5)) for i in range(count)]
                    source=app.new_list_object('Messbestand '+str(count),tasks)
                    app.lists.append(source);assert app.save_items(show_error=False)
                    app.set_active_list(source['id']);run.idle(3)
                    fns=[('render',app.refresh_tree),('search',lambda:app.quick_open_results('Aufgabe 09')),
                         ('filter',lambda:app.saved_filters.entries(criterion(query='Aufgabe'))),
                         ('save',lambda:app.save_items(show_error=False))]
                    for name,fn in fns:
                        row=series(run,name,fn);row['items']=count;entry['scenarios'].append(row)
                    identity=tasks[0]['id']
                    def toggle():
                        app.tree.selection_set(identity);app.tree.focus(identity);app.toggle_done()
                    row=series(run,'toggle_real_adapter',toggle);row['items']=count;entry['scenarios'].append(row)
                    if count==10000 and process_index==0:
                        profiler=cProfile.Profile();profiler.enable()
                        for _ in range(5):app.quick_open_results('Aufgabe 09')
                        profiler.disable();stats=pstats.Stats(profiler)
                        top=sorted(stats.stats.items(),key=lambda p:p[1][3],reverse=True)[:15]
                        report['profile_search']=[dict(file=Path(k[0]).name,line=k[1],function=k[2],calls=v[1],cumulative_s=round(v[3],6)) for k,v in top]
                    app.lists.remove(source);app.set_home_view();assert app.save_items(show_error=False)
                    run.idle(2);persist()
                # Python-Allokationen bei wiederholtem Ansichtswechsel, separat vom Timing.
                if process_index==0:
                    tracemalloc.start();gc.collect();before=tracemalloc.get_traced_memory()[0]
                    for _ in range(20):app.set_today_view();run.idle(1);app.set_home_view();run.idle(1)
                    gc.collect();current,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
                    report['python_memory_switches']=dict(switches=40,before=before,after=current,peak=peak,
                        interpretation='Momentaufnahme; Wachstum allein beweist kein Leck und enthaelt initiale Caches.')
                print('Messprozess abgeschlossen',process_index+1,flush=True)
            except Exception:
                report['errors'].append(traceback.format_exc().replace(str(Path.home()),'~')[-2500:]);persist()
            finally:
                if run:run.app.previews.close();run.ende()
    # Visueller Audit am selben eingefrorenen App-Stand und synthetischer Showcase.
    from test_uiux_paket import Lauf as UILauf
    run=None
    with tempfile.TemporaryDirectory(prefix='glide-analysis-ui-') as td:
        try:
            run=UILauf(args.app,str(Path(td)/'data'));run.showcase();app=run.app
            page=next(e for e in app.lists if app.is_page_list(e))
            listing=max((e for e in app.lists if not app.is_page_list(e) and e.get('items')),key=lambda e:len(e['items']))
            views=[('startseite',app.set_home_view),('heute',app.set_today_view),('labels',app.set_labels_view),
                ('vorlagen',app.set_template_view),('papierkorb',app.set_trash_view),
                ('liste',lambda:app.set_active_list(listing['id'])),('seite',lambda:app.set_active_list(page['id'])),
                ('pinnwand',app.open_global_board),('kalender',app.open_calendar_view)]
            index=0
            for label,geometry,font in [('normal','1280x800+20+20','mittel'),('eng_gross','860x700+20+20','gross')]:
                app.settings['ui_font_size']=font;app.apply_ui_font();run.root.geometry(geometry);run.idle(4)
                for name,opener in views:
                    opener();run.idle(5);index+=1
                    target=out/(str(index).zfill(2)+'_'+name+'_'+label+'.png')
                    save_windows_screenshot(run.root,target)
                    report['screens'].append(dict(step=index,view=name,configuration=label,file=target.name,
                        requested_geometry=geometry,font=font,captured=True,visually_reviewed=False))
            app.run_modal=lambda dialog,*a,**k:(run.idle(4),save_windows_screenshot(dialog,out/'19_einstellungen.png'),dialog.destroy())
            app.show_settings_dialog();report['screens'].append(dict(step=19,view='einstellungen',file='19_einstellungen.png',captured=True,visually_reviewed=False))
            report['callback_errors']=run.errors
        except Exception:
            report['errors'].append(traceback.format_exc().replace(str(Path.home()),'~')[-2500:])
        finally:
            if run:run.ende()
    persist();print(json.dumps(dict(processes=len(report['processes']),screens=len(report['screens']),errors=report['errors']),ensure_ascii=False),flush=True)


if __name__=='__main__':main()
