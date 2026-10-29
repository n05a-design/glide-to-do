"""Begrenzte WA-41-Diagnose an eingefrorener Quelle, ausschließlich Testdaten.

Die ursprünglichen Phasen 1/2 und ihre Assertions bleiben erhalten; danach
endet die Kernprobe. Varianten sind ausschließlich Änderungen im Prüfprozess.
"""
import argparse
import faulthandler
import gc
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import sysconfig
import threading
import time

parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--variant', choices=('normal', 'no_chrome', 'no_ui', 'nogc'), default='normal')
parser.add_argument('--payload', type=Path)
args = parser.parse_args()
args.output.parent.mkdir(parents=True, exist_ok=True)
log = args.output.open('w', encoding='utf-8', buffering=1)
faulthandler.enable()
started = time.monotonic()


def record(event, **values):
    row = dict(event=event, seconds=round(time.monotonic()-started, 3), **values)
    log.write(json.dumps(row, ensure_ascii=False, default=str)+'\n')


def native_libraries():
    current_repo = Path(__file__).resolve().parents[3]
    path = current_repo/'packaging/paket/start_glide.py'
    spec = importlib.util.spec_from_file_location('wa41_native_probe', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.loaded_libraries()


def install(mod):
    if args.variant == 'no_chrome':
        mod.ListApp._schedule_windows_chrome_theme = lambda *a, **k: None
        mod.ListApp._apply_windows_chrome_theme = lambda *a, **k: True
    original = mod.ListApp.__init__

    def initialize(self, *a, **kw):
        original(self, *a, **kw)
        record('app_ready', tk=str(self.root.tk.call('package', 'provide', 'Tk')),
               native_libraries=native_libraries(), threads=[t.name for t in threading.enumerate()])
        if args.variant == 'no_ui':
            for name in ('refresh_tree', 'refresh_home', 'update_sidebar_list', 'update_window_title',
                         'update_header_title', 'refresh_library_page'):
                setattr(self, name, lambda *a, **kw: None)
    mod.ListApp.__init__ = initialize


def difference(saved, loaded, iteration):
    before, after = json.loads(saved), json.loads(loaded)
    found = []

    def compare(left, right, path=''):
        if len(found) >= 16 or left == right:
            return
        if type(left) is type(right) is dict:
            for key in sorted(set(left) | set(right)):
                compare(left.get(key, '<fehlt>'), right.get(key, '<fehlt>'), path+'/'+key)
        elif type(left) is type(right) is list and len(left) == len(right):
            for index, (lvalue, rvalue) in enumerate(zip(left, right)):
                compare(lvalue, rvalue, path+'/'+str(index))
        else:
            found.append(dict(path=path, saved=repr(left)[:250], loaded=repr(right)[:250]))
    compare(before, after)
    record('data_difference', iteration=iteration, differences=found)


def snapshot(path):
    if args.payload and not args.payload.exists():
        args.payload.parent.mkdir(parents=True, exist_ok=True)
        args.payload.write_bytes(path.read_bytes())
        record('payload', bytes=args.payload.stat().st_size)


if args.variant == 'nogc':
    gc.disable()
test = args.repo/'tests/integration/test_speicherlast330.py'
source = test.read_text(encoding='utf-8')
record('start', python=sys.version, executable=sys.executable, test_sha256=hashlib.sha256(test.read_bytes()).hexdigest(),
       variant=args.variant, allocator=os.environ.get('PYTHONMALLOC', 'default'),
       hashseed=os.environ.get('PYTHONHASHSEED'), gc_enabled=gc.isenabled(),
       gil_disabled=sysconfig.get_config_var('Py_GIL_DISABLED'),
       jit_enabled=getattr(getattr(sys, '_jit', None), 'is_enabled', lambda: None)())
assert source.count('    loader.exec_module(mod)') == 1
source = source.replace('    loader.exec_module(mod)', '    loader.exec_module(mod)\n    install(mod)')
source = source.replace('        groesse_mb = SPEICHER.stat().st_size / 1e6',
                        '        snapshot(SPEICHER)\n        groesse_mb = SPEICHER.stat().st_size / 1e6')
source = source.replace('        for runde in range(40):',
                        '        for runde in range(40):\n            record("round", iteration=runde)')
assertion = '            assert bestand() == auf_platte, f"Runde {runde}: geladen ≠ gespeichert"'
assert source.count(assertion) == 1
source = source.replace(assertion,
    '            observed = bestand()\n'
    '            if observed != auf_platte:\n'
    '                difference(auf_platte, observed, runde)\n'
    '                raise AssertionError(f"Runde {runde}: geladen ≠ gespeichert")')
marker = '        # Endgültiges Entfernen'
assert source.count(marker) == 1
source = source[:source.index(marker)] + (
    '        record("core_pass", tasks=anzahl, iterations=40)\n'
    '    finally:\n'
    '        app.cancel_pending_callbacks()\n'
    '        app.release_data_lock()\n'
    '        root.destroy()\n')
scope = dict(__file__=str(test), __name__='__main__', install=install, record=record,
             difference=difference, snapshot=snapshot)
try:
    exec(compile(source, str(test), 'exec'), scope)
except BaseException as error:
    record('exception', error_type=type(error).__name__, message=str(error))
    raise
finally:
    log.close()
