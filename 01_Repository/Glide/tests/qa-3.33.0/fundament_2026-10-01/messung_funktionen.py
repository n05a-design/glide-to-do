"""Alternierender Alt/Neu-Vergleich im selben Prozess; isoliert die Ursachen."""
import ast
import importlib.machinery
import importlib.util
import json
import math
import os
from pathlib import Path
import statistics
import tempfile
import time
from unittest.mock import patch

repo = Path(__file__).resolve().parents[3]
qa = Path(__file__).resolve().parent
old_source = qa / 'vorher/quellstand/app.pyw'
with tempfile.TemporaryDirectory(prefix='glide-paarmessung-') as directory:
    os.environ['GLIDE_DATA_DIR'] = directory
    os.environ['GLIDE_TEST_MODE'] = '1'
    loader = importlib.machinery.SourceFileLoader('glide_pair', str(repo / 'src/glide/app.pyw'))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(mod)
    root = mod.tk.Tk()
    app = mod.ListApp(root)
    errors = []
    root.report_callback_exception = lambda *exc: errors.append(str(exc[1]))
    try:
        app.items.extend(app.new_item(f'Aufgabe {i}', due='2026-12-24', description='Text '*150) for i in range(5000))
        app.save_items()
        root.update()
        cls = next(n for n in ast.parse(old_source.read_text()).body if isinstance(n, ast.ClassDef) and n.name == 'ListApp')
        old = {}
        for n in cls.body:
            if isinstance(n, ast.FunctionDef) and (n.name == 'content_column_widths' or n.name.startswith('ensure_schema') and n.name.endswith('_backup')):
                namespace = dict(vars(mod))
                exec(compile(ast.Module(body=[n], type_ignores=[]), str(old_source), 'exec'), namespace)
                old[n.name] = namespace[n.name]
        methods = [old[f'ensure_schema{target}_backup'] for target in range(12, 21)]
        def reset():
            for target in range(12, 21):
                setattr(app, f'_schema{target}_backup_checked', False)
        def old_backup():
            reset()
            for method in methods:
                method(app)
        def new_backup():
            reset()
            app._schema_backup_guard = mod.SchemaBackups()
            for target in range(12, 21):
                app.ensure_schema_backup(target)
        def loaded_backup():
            reset()
            app._schema_backup_guard = mod.SchemaBackups()
            app._schema_backup_guard.observe(mod.SAVE_FILE, {'version': 20}, Path(mod.SAVE_FILE).stat())
            for target in range(12, 21):
                app.ensure_schema_backup(target)
        def series(functions):
            result = {name: [] for name in functions}
            for fn in functions.values():
                fn()
            for turn in range(12):
                names = list(functions)
                if turn % 2:
                    names.reverse()
                for name in names:
                    start = time.perf_counter()
                    functions[name]()
                    result[name].append((time.perf_counter() - start)*1000)
            return {name: {'median_ms':statistics.median(values), 'p95_ms':sorted(values)[math.ceil(.95*len(values))-1], 'roh_ms':values} for name, values in result.items()}
        result = {'python':mod.sys.version, 'tk':root.tk.call('info','patchlevel'), 'punkte':5000, 'methode':'abwechselnd im selben Prozess, Aufwärmen + 12 Runden', 'grenze':'Funktionskosten, keine Gesamtlatenz einer Aktion'}
        result['formatsicherung'] = series({'alt':old_backup,'neu_kalt':new_backup,'neu_nach_laden':loaded_backup})
        load = mod.json.load
        reads = {}
        for name,fn in {'alt':old_backup,'neu_kalt':new_backup,'neu_nach_laden':loaded_backup}.items():
            count = [0]
            def counted(file,*a,**k):
                if Path(file.name) == Path(mod.SAVE_FILE):
                    count[0] += 1
                return load(file,*a,**k)
            with patch.object(mod.json,'load',side_effect=counted):
                fn()
            reads[name] = count[0]
        result['json_leselaeufe'] = reads
        expected = old['content_column_widths'](app)
        assert expected == app.content_column_widths()
        app.set_table_view()
        root.update()
        result['tabellen_spaltenmessung'] = series({'alt':lambda:old['content_column_widths'](app),'neu':app.content_column_widths})
        assert not errors, errors
        (qa/'funktionsmessung.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
        print({key: {name:round(value['median_ms'],3) for name,value in result[key].items()} for key in ['formatsicherung','tabellen_spaltenmessung']}, reads)
    finally:
        root.destroy()
