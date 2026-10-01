"""Reproduzierbare Tk-Messung mit synthetischen Daten; keine Nutzerdaten."""
import argparse
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import platform
import statistics
import tempfile
import time

parser = argparse.ArgumentParser()
parser.add_argument('--ziel', type=Path, required=True)
args = parser.parse_args()
repo = Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory(prefix='glide-performance-') as temp:
    os.environ['GLIDE_DATA_DIR'] = temp
    loader = importlib.machinery.SourceFileLoader('glide_performance', str(repo/'src/glide/app.pyw'))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    start = time.perf_counter()
    root = mod.tk.Tk()
    root.withdraw()
    app = mod.ListApp(root)
    app.show_info = app.show_warning = lambda *a, **kw: None
    root.geometry('1280x960+20+20')
    root.deiconify()
    root.update()
    report = {'version':mod.APP_VERSION, 'python':platform.python_version(),
              'platform':platform.platform(), 'tk':root.tk.call('info','patchlevel'),
              'scaling':float(root.tk.call('tk','scaling')), 'font':app.ui_font_family(),
              'startup_ms':round((time.perf_counter()-start)*1000,2), 'scenarios':[],
              'limits':'Synthetische flache Aufgaben ohne Anhänge; drei Wiederholungen; lokale Messung ohne Referenzgerät. Kein Langzeit-, Speicher- oder Mehrmonitorbenchmark.'}
    for count in (100,1000,5000):
        entry = app.new_list_object(f'Messung {count}', [app.new_item(f'Aufgabe {i:05}') for i in range(count)])
        app.lists.append(entry)
        app.set_active_list(entry['id'])
        for material in (False,True):
            app.settings['glass_mode'] = material
            app.apply_theme()
            root.update()
            values=[]
            for _ in range(3):
                start=time.perf_counter(); app.refresh_tree(); root.update_idletasks()
                values.append(round((time.perf_counter()-start)*1000,2))
            start=time.perf_counter(); assert app.save_items(); save_ms=(time.perf_counter()-start)*1000
            report['scenarios'].append({'items':count,'glass_mode':material,'render_ms':values,
                                        'render_median_ms':statistics.median(values),'save_ms':round(save_ms,2)})
        app.lists.remove(entry)
    app.release_data_lock(); app.cancel_pending_callbacks(); root.destroy()
args.ziel.parent.mkdir(parents=True,exist_ok=True)
args.ziel.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
