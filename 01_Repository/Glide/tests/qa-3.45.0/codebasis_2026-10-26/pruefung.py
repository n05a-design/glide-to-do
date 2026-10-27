"""Reproduzierbarer Quellabgleich und semantische Gegenprobe zum Revieweingang.

Keine App-Imports; nur künstliche Daten. Laufzeitwerte betreffen ausschließlich
Zeitstempel/Vergleich, weder Speichern noch Rendern oder native Ereignisse.
"""
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import statistics
import subprocess
import sys
import tempfile
import time
import unittest

REPO = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SOURCE = REPO / 'src/glide'
BASELINE = '089ae83'
sys.path.insert(0, str(SOURCE))
import save_comparison as current


def git_source(name):
    return subprocess.check_output(['git', 'show', f'{BASELINE}:01_Repository/Glide/src/glide/{name}'], cwd=REPO)


def inventory(source):
    tree = ast.parse(source)
    app = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'ListApp')
    attrs = {node.attr for node in ast.walk(app) if isinstance(node, ast.Attribute)
             and isinstance(node.value, ast.Name) and node.value.id == 'self'}
    assigned = {node.attr for node in ast.walk(app) if isinstance(node, ast.Attribute)
                and isinstance(node.ctx, ast.Store) and isinstance(node.value, ast.Name)
                and node.value.id == 'self'}
    direct_assigned = {target.attr for node in ast.walk(app) if isinstance(node, ast.Assign)
                       for target in node.targets if isinstance(target, ast.Attribute)
                       and isinstance(target.value, ast.Name) and target.value.id == 'self'}
    calls = {}
    for node in ast.walk(app):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == 'self':
                calls[node.func.attr] = calls.get(node.func.attr, 0) + 1
    methods = [node for node in app.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    return {'lines': len(source.splitlines()), 'functions': sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                                                             for n in ast.walk(tree)),
            'listapp_lines': app.end_lineno - app.lineno + 1, 'listapp_methods': len(methods),
            'self_attributes': len(attrs), 'self_stored_attributes': len(assigned),
            'self_direct_assigned_attributes': len(direct_assigned),
            'largest_methods': sorted([{'name': n.name, 'line': n.lineno, 'lines': n.end_lineno-n.lineno+1}
                                       for n in methods], key=lambda n:n['lines'], reverse=True)[:12],
            'direct_call_sites': dict(sorted(calls.items(), key=lambda n:n[1], reverse=True)[:12])}


def fixture(count):
    return [{'id': f'l{n}', 'title': f'Liste {n}', 'items': [
        {'id': f'i{n}-{i}', 'text': f'Punkt {i}', 'done': i % 3 == 0,
         'done_at': '2026-01-01' if i % 5 == 0 else None, 'children': []}
        for i in range(count // 4)]} for n in range(4)]


def values(result):
    return tuple(getattr(result, key) for key in ('items', 'lists', 'list_signatures', 'item_signatures'))


def main():
    result = {'baseline_commit': BASELINE, 'python': sys.version, 'platform': sys.platform,
              'baseline_app': inventory(git_source('app.pyw').decode('utf-8-sig')),
              'candidate_app': inventory((SOURCE/'app.pyw').read_text(encoding='utf-8-sig'))}
    own = [p for p in SOURCE.iterdir() if p.suffix in ('.py', '.pyw') and p.name != 'drawing_prototype.pyw']
    result['runtime_files'] = len(own)
    all_python = [p for p in SOURCE.rglob('*') if p.suffix in ('.py', '.pyw')]
    result['python_sources_including_vendor_and_prototype'] = len(all_python)
    result['main_share_source_bytes'] = ((SOURCE/'app.pyw').stat().st_size
                                         / sum(p.stat().st_size for p in all_python))
    result['source_manifest'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(own)}
    with tempfile.TemporaryDirectory(prefix='glide-comparison-reference-') as temporary:
        path = Path(temporary)/'reference.py'
        path.write_bytes(git_source('save_comparison.py'))
        spec = importlib.util.spec_from_file_location('comparison_reference', path)
        old = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = old
        spec.loader.exec_module(old)
        options = dict(item_fields=('text', 'done', 'done_at'),
                       schedulable=lambda item: item.get('kind', 'task') == 'task', drawing_hash=lambda entry: None)
        randomizer = random.Random(345026)
        for case in range(240):
            original = fixture(80)
            baseline = {'items': old.compare_lists(original, **options).items}
            previous_old = old.prepare_comparison(original, **options)
            previous_new = current.prepare_comparison(original, **options)
            original = copy.deepcopy(original)
            for entry in original:
                for item in entry['items']:
                    item['done'] = randomizer.choice((True, False))
                    if randomizer.choice((True, False)):
                        item['done_at'] = None
                    item['children'] = [{'id': item['id']+'c', 'done': True, 'text': 'Kind'}]
            if case % 5 == 0:
                original[1]['id'] = original[0]['id']
            if case % 7 == 0:
                original[0]['items'][0]['kind'] = 'group'
            scope = None if case % 2 else {'l0', 'l1'}
            before, after = copy.deepcopy(original), copy.deepcopy(original)
            left = old.prepare_comparison(before, baseline=baseline, completed_at='2026-10-26T20:00:00+01:00',
                                          previous_parts=previous_old.parts, changed_ids=scope, **options)
            right = current.prepare_save_comparison(after, baseline=baseline, completed_at='2026-10-26T20:00:00+01:00',
                                                    previous_parts=previous_new.parts, changed_ids=scope, **options)
            assert json.dumps(before, ensure_ascii=False).encode() == json.dumps(after, ensure_ascii=False).encode(), case
            assert values(left) == values(right), case
        result['comparison_differential_cases'] = 240
        result['comparison_only_ms'] = {}
        for count in (100, 1000, 5000, 10000):
            times = {'before': [], 'after': []}
            for trial in range(7):
                for kind in (('before', 'after') if trial % 2 else ('after', 'before')):
                    data = fixture(count)
                    start = time.perf_counter()
                    if kind == 'before':
                        old.prepare_comparison(data, completed_at='2026-10-26', **options)
                    else:
                        current.prepare_save_comparison(data, baseline=None, completed_at='2026-10-26', **options)
                    times[kind].append((time.perf_counter()-start)*1000)
            result['comparison_only_ms'][str(count)] = {
                kind: {'median': statistics.median(samples), 'p95': sorted(samples)[-1], 'samples': samples}
                for kind, samples in times.items()}

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    for pattern in ('test_persistence.py', 'test_save_result.py', 'test_save_comparison.py',
                    'test_incremental_comparison.py', 'test_compact_mode.py', 'test_image_conversion.py'):
        suite.addTests(loader.discover(str(REPO/'tests/unit'), pattern=pattern))
    check = unittest.TextTestRunner(verbosity=1).run(suite)
    result['unit_tests'] = {'run': check.testsRun, 'failures': len(check.failures),
                            'errors': len(check.errors), 'skipped': len(check.skipped)}
    for path in own:
        compile(path.read_text(encoding='utf-8-sig'), str(path), 'exec')
    result['syntax_runtime_files'] = len(own)
    (HERE/'pruefung.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key: result[key] for key in ('comparison_differential_cases', 'unit_tests', 'syntax_runtime_files')}))
    return int(not check.wasSuccessful())


if __name__ == '__main__':
    raise SystemExit(main())
