"""WA-36: gezielte synchrone Mutationsmessung, weiterentwickelt aus Paket 1.

Keine Tk-Ereignispumpe zwischen den gemessenen toggle_done-Aufrufen. Auswahl
setzen liegt außerhalb der Uhr; Snapshot, Speichern und synchroner Refresh
liegen darin. Der getrennte cProfile-Aufruf erklärt Kosten, misst keinen Gewinn.
"""
from pathlib import Path
import argparse
import ast
import cProfile
from datetime import datetime, timezone
import faulthandler
import hashlib
import json
import platform
import pstats
import statistics
import sys
import tempfile
import time


REPO = Path(__file__).resolve().parents[3]


def source_info(path):
    raw = path.read_bytes()
    source = raw.decode('utf-8-sig')
    tree = ast.parse(source)
    locations = {}
    toggle_hash = None
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name in ('ListApp', 'PackedState'):
            for method in node.body:
                if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    locations[(method.name, method.lineno)] = node.name + '.' + method.name
                    for decorator in method.decorator_list:
                        locations[(method.name, decorator.lineno)] = node.name + '.' + method.name
                    if node.name == 'ListApp' and method.name == 'toggle_done':
                        body = ast.get_source_segment(source, method)
                        toggle_hash = hashlib.sha256(body.encode('utf-8')).hexdigest()
    return dict(app_sha256=hashlib.sha256(raw).hexdigest(), toggle_done_source_sha256=toggle_hash), locations


def profile_result(profiler, locations, app_path):
    stats = pstats.Stats(profiler)
    rows = []
    for (filename, line, function), (primitive, total, own, cumulative, _callers) in stats.stats.items():
        is_app = filename not in ('~', '<string>') and Path(filename).resolve() == app_path
        qualified = locations.get((function, line), function) if is_app else function
        rows.append(dict(file=Path(filename).name, line=line, function=qualified,
                         primitive_calls=primitive, total_calls=total,
                         self_s=round(own, 6), cumulative_s=round(cumulative, 6)))
    rows.sort(key=lambda row: -row['cumulative_s'])
    categories = {
        'snapshot': lambda row: row['function'] in ('ListApp.snapshot_undo', 'ListApp.undo_state', 'PackedState.__init__'),
        'json': lambda row: row['file'] in ('encoder.py', '__init__.py') and row['function'] in ('dumps', 'encode', 'iterencode'),
        'zlib': lambda row: 'zlib' in row['function'] or row['function'] in ('compress', 'decompress'),
        'backup': lambda row: row['function'] == 'ListApp.write_backup_copy',
        'atomic_write': lambda row: row['function'] in ('ListApp.write_json_atomic', 'ListApp.replace_with_retry', 'ListApp.settings_json_text') or 'fsync' in row['function'],
        'render': lambda row: row['function'] in ('ListApp.refresh_tree', 'ListApp._refresh_tree', 'ListApp._refresh_tree_contents', 'ListApp.update_sidebar_list'),
        'comparison_history': lambda row: row['function'] in ('ListApp.list_comparison', 'ListApp.update_history'),
    }
    return dict(total_profiled_self_s=round(stats.total_tt, 6), top_functions=rows[:40],
                cost_categories={name: [row for row in rows if predicate(row)]
                                 for name, predicate in categories.items()},
                interpretation=(
                    'cProfile-Kosten eines zusätzlichen Aufrufs mit 100 ausgewählten Aufgaben bei 10.000. '
                    'Snapshot enthält JSON und zlib; atomarer Schreibweg enthält JSON/Dateisystem; '
                    'Refresh kann Teilaufbauten enthalten. Kumulative Werte überlappen und sind nicht '
                    'addierbar. self_s schließt Unteraufrufe aus. Backupkosten bedeuten die ausgeführte '
                    'Prüfung bzw. Sicherung, nicht zwingend eine neu erzeugte Backupdatei. '
                    'Profiling verursacht Zusatzlast und ist kein Latenz- oder Gewinnbeleg.'))


def write_report(path, result):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app', type=Path, default=REPO / 'src/glide/app.pyw')
    parser.add_argument('--report', type=Path, default=Path(__file__).with_suffix('.json'))
    parser.add_argument('--profile', action='store_true')
    args = parser.parse_args()
    args.app = args.app.resolve()
    before, locations = source_info(args.app)
    sys.path.insert(0, str(REPO / 'tests/integration'))
    from test_schutzrunde import Lauf

    result = dict(**before, source_before=before, sizes=[], repetitions=5, warmups=1,
                  python=platform.python_version(), platform=platform.system(),
                  started_utc=datetime.now(timezone.utc).isoformat(),
                  one_python_process=True, fresh_tk_interpreter_per_size=True,
                  sizes_planned=[100, 1000, 5000, 10000],
                  scope=('Synchroner echter toggle_done-Weg einschließlich Undo, Sofortspeicherung und '
                         'Refresh; unprofiliert auf diesem Desktop. Auswahlsetzen außerhalb der Uhr. '
                         'Nachlaufende Tk-Ereignisse sind nicht im Zeitwert enthalten.'),
                  sample_limit=('Je Aktion ein erster Aufruf und fünf warme Wiederholungen. Der erste '
                                'Aufruf ist kein kalter Appstart. Kein p95 aus fünf Beobachtungen und '
                                'keine allgemeine Leistungs-/Plattformzusage.'),
                  comparable_to='roadmap_paket1_2026-10-21/messung.py: gleicher Ablauf, zusätzlich 5.000',
                  complete=False)
    write_report(args.report, result)
    try:
        for size in result['sizes_planned']:
            faulthandler.dump_traceback_later(120, exit=True)
            with tempfile.TemporaryDirectory(prefix='glide-roadmap3-messung-') as td:
                loaded, _ = source_info(args.app)
                run = Lauf(args.app, str(Path(td) / 'data'))
                app = run.app
                try:
                    result['tk'] = str(run.root.tk.call('info', 'patchlevel'))
                    tasks = [app.new_item('Messaufgabe ' + str(i).zfill(5)) for i in range(size)]
                    entry = app.new_list_object('Messbestand', tasks)
                    app.lists.append(entry)
                    assert app.save_items(show_error=False)
                    app.set_active_list(entry['id'])
                    run.idle()
                    row = dict(items=size, loaded_source=loaded, operations=[])
                    for count in (1, min(100, size)):
                        identities = [item['id'] for item in tasks[-count:]]
                        values = []
                        for iteration in range(6):
                            app.tree.selection_set(identities)
                            begin = time.perf_counter()
                            app.toggle_done()
                            elapsed = round((time.perf_counter() - begin) * 1000, 3)
                            assert app._last_save_result.data_written and not app.dirty
                            if iteration:
                                values.append(elapsed)
                            else:
                                first = elapsed
                        row['operations'].append(dict(selected=count, first_ms=first, values_ms=values,
                                                      median_ms=round(statistics.median(values), 3),
                                                      minimum_ms=min(values), maximum_ms=max(values)))
                    if args.profile and size == 10000:
                        app.tree.selection_set([item['id'] for item in tasks[-100:]])
                        profiler = cProfile.Profile()
                        profiler.enable()
                        app.toggle_done()
                        profiler.disable()
                        result['profile'] = profile_result(profiler, locations, args.app)
                    result['sizes'].append(row)
                    print(json.dumps(row, ensure_ascii=False), flush=True)
                    assert not run.errors, run.errors
                finally:
                    run.ende()
            faulthandler.cancel_dump_traceback_later()
            write_report(args.report, result)
        result['complete'] = True
    except Exception as exc:
        result['error_type'] = type(exc).__name__
        result['error'] = str(exc)
        raise
    finally:
        faulthandler.cancel_dump_traceback_later()
        after, _ = source_info(args.app)
        result['source_after'] = after
        result['source_unchanged_during_measurement'] = before == after and all(
            row['loaded_source'] == before for row in result['sizes'])
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        write_report(args.report, result)


if __name__ == '__main__':
    main()
