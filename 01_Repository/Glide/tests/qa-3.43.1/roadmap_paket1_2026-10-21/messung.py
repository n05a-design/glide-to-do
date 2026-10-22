from pathlib import Path
import argparse
import cProfile
import hashlib
import faulthandler
import json
import pstats
import statistics
import sys
import tempfile
import time

parser = argparse.ArgumentParser()
parser.add_argument('--app', type=Path, required=True)
parser.add_argument('--report', type=Path, required=True)
parser.add_argument('--profile', action='store_true')
args = parser.parse_args()
repo = Path.cwd()
sys.path.insert(0, str(repo / 'tests/integration'))
from test_schutzrunde import Lauf

result = dict(app_sha256=hashlib.sha256(args.app.read_bytes()).hexdigest(),
              sizes=[], repetitions=5, warmups=1, isolated_python_process=True,
              scope='Synchroner toggle_done-Weg einschließlich Undo, sofortigem Speichern und Refresh; unprofiliert, Desktoplast. Nachlaufende Tk-Ereignisse nicht im Zeitwert enthalten.')
faulthandler.dump_traceback_later(45, exit=True)
for size in (100, 1000, 10000):
    with tempfile.TemporaryDirectory(prefix='glide-roadmap-messung-') as td:
        run = Lauf(args.app, str(Path(td) / 'data'))
        app = run.app
        try:
            result['tk'] = str(run.root.tk.call('info', 'patchlevel'))
            tasks = [app.new_item('Messaufgabe ' + str(i).zfill(5)) for i in range(size)]
            entry = app.new_list_object('Messbestand', tasks)
            app.lists.append(entry); assert app.save_items(show_error=False)
            app.set_active_list(entry['id']); run.idle()
            row = dict(items=size, operations=[])
            for count in (1, min(100, size)):
                identities = [item['id'] for item in tasks[-count:]]
                values = []
                for iteration in range(6):
                    app.tree.selection_set(identities)
                    begin = time.perf_counter(); app.toggle_done(); elapsed = (time.perf_counter() - begin) * 1000
                    if iteration: values.append(round(elapsed, 3))
                    else: first = round(elapsed, 3)
                row['operations'].append(dict(selected=count, first_ms=first, values_ms=values,
                                              median_ms=round(statistics.median(values), 3)))
            if args.profile and size == 10000:
                app.tree.selection_set([item['id'] for item in tasks[-100:]])
                profiler = cProfile.Profile(); profiler.enable(); app.toggle_done(); profiler.disable()
                stats = pstats.Stats(profiler)
                result['profile'] = [dict(file=Path(k[0]).name, function=k[2], primitive_calls=v[0],
                                          total_calls=v[1], cumulative_s=round(v[3], 6))
                                     for k, v in sorted(stats.stats.items(), key=lambda p: -p[1][3])[:20]]
            result['sizes'].append(row)
            print(json.dumps(row), flush=True)
            assert not run.errors, run.errors
        finally:
            run.ende()
    faulthandler.cancel_dump_traceback_later()
    faulthandler.dump_traceback_later(45, exit=True)
faulthandler.cancel_dump_traceback_later()
args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
