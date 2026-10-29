"""Derselbe künstliche Großbestand in den verdächtigen Fachmodulen, ohne App/Tk."""
import argparse
import ast
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, required=True)
parser.add_argument('--payload', type=Path, required=True)
parser.add_argument('--iterations', type=int, default=20)
parser.add_argument('--bootstrap', choices=('none', 'import', 'tk', 'app', 'compile', 'imports', 'prefix'), default='none')
parser.add_argument('--source-mode', choices=('loader', 'compiled', 'cached_main_fresh_deps'), default='loader')
args = parser.parse_args()
sys.path.insert(0, str(args.repo/'src/glide'))
import drawing
import repeat_rules
import save_comparison

source = ast.parse((args.repo/'src/glide/app.pyw').read_text(encoding='utf-8'))
owner = next(node for node in source.body if isinstance(node, ast.ClassDef) and node.name == 'ListApp')
assignment = next(node for node in owner.body if isinstance(node, ast.Assign)
                  and any(isinstance(n, ast.Name) and n.id == 'HISTORY_ITEM_FIELDS' for n in node.targets))
fields = ast.literal_eval(assignment.value)
del source, owner, assignment
temporary = root = app = None
if args.bootstrap != 'none':
    temporary = tempfile.TemporaryDirectory(prefix='glide-wa41-pure-')
    os.environ['GLIDE_DATA_DIR'] = temporary.name
    os.environ['GLIDE_TEST_MODE'] = '1'
    if args.bootstrap in ('compile', 'imports', 'prefix'):
        path = args.repo/'src/glide/app.pyw'
        tree = ast.parse(path.read_text(encoding='utf-8'))
        if args.bootstrap == 'imports':
            tree.body = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
        elif args.bootstrap == 'prefix':
            position = next(i for i,n in enumerate(tree.body) if isinstance(n,ast.ClassDef) and n.name=='ListApp')
            tree.body = tree.body[:position]
        compiled_app = compile(tree, str(path), 'exec')
        if args.bootstrap != 'compile':
            reduced_scope = dict(__file__=str(path), __name__='wa41_reduced')
            exec(compiled_app, reduced_scope)
    if args.bootstrap in ('import', 'app'):
        with zipfile.ZipFile(args.repo/'tests/fixtures/beispiele/glide_beispieldaten.glidebackup') as archive:
            Path(temporary.name, 'liste_speicher.json').write_bytes(archive.read('data.json'))
        loader = importlib.machinery.SourceFileLoader('wa41_bootstrap', str(args.repo/'src/glide/app.pyw'))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        sys.modules[loader.name] = module
        if args.source_mode == 'compiled':
            exec(compile((args.repo/'src/glide/app.pyw').read_bytes(), str(args.repo/'src/glide/app.pyw'), 'exec'), module.__dict__)
        elif args.source_mode == 'cached_main_fresh_deps':
            original_code = loader.get_code(loader.name)
            sys.pycache_prefix = str(Path(temporary.name)/'empty-cache')
            exec(original_code, module.__dict__)
        else:
            loader.exec_module(module)
    if args.bootstrap in ('tk', 'app'):
        import tkinter
        root = tkinter.Tk()
        root.withdraw()
        if args.bootstrap == 'app':
            app = module.ListApp(root)
            app.process_reminders = lambda *a, **kw: False
        root.update()


def drawing_hash(entry):
    if not isinstance(entry.get('drawing'), dict):
        return None
    fields = dict(drawing=entry['drawing'], animation=entry.get('animation'))
    return hashlib.sha256(drawing.canonical_json(fields).encode('utf-8')).hexdigest()


raw = args.payload.read_bytes()
reference = None
for iteration in range(args.iterations):
    data = json.loads(raw)
    repeat_rules.check_stored_series(data, data['version'])
    result = save_comparison.compare_lists(data['lists'], item_fields=fields,
        schedulable=lambda item: item.get('kind', 'task') in ('task', 'long'), drawing_hash=drawing_hash)
    digest = hashlib.sha256(repr(result).encode('utf-8')).hexdigest()
    # repr enthält nur Werte/Digests; gleiche Einlesereihenfolge und feste Eingangsdaten.
    if reference is None:
        reference = digest
    assert digest == reference, (iteration, digest, reference)
    if args.bootstrap == 'none':
        assert 'tkinter' not in sys.modules and '_tkinter' not in sys.modules
    if root is not None:
        root.update()
    print('round', iteration, 'items', len(result.items), flush=True)
print('PASS pure', sys.version.split()[0], args.iterations, flush=True)
if app is not None:
    app.cancel_pending_callbacks()
    app.release_data_lock()
if root is not None:
    root.destroy()
if temporary is not None:
    temporary.cleanup()
