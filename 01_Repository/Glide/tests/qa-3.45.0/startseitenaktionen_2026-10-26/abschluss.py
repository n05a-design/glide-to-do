"""Quell-/Syntax-/Verweisabschluss nach der gezielten Startseitenprüfung."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ROOT = REPO.parents[1]
SOURCE = REPO/'src/glide'
result = {'errors': [], 'source_manifest': {}, 'links_checked': 0, 'anchors_checked': 0}
(HERE/'abschluss.json').write_text('{"status":"running"}\n', encoding='utf-8')


def headings(path):
    text = re.sub(r'```.*?```', '', path.read_text(encoding='utf-8-sig'), flags=re.S)
    found, counts = set(), {}
    for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, flags=re.M):
        slug = re.sub(r'[^\w\- ]', '', title.lower()).replace(' ', '-')
        number = counts.get(slug, 0)
        found.add(slug + (f'-{number}' if number else ''))
        counts[slug] = number+1
    found.update(re.findall(r'<a\s+(?:name|id)=["\']([^"\']+)', text))
    return found


sources = sorted(path for path in SOURCE.iterdir() if path.suffix in ('.py', '.pyw')
                 and path.name != 'drawing_prototype.pyw')
result['runtime_files'] = len(sources)
result['delivery_differences'] = []
for path in sources:
    compile(path.read_text(encoding='utf-8-sig'), str(path), 'exec')
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    result['source_manifest'][path.name] = digest
    name = {'app.pyw': 'Glide-Aufgaben-und-Listen_v3.45.0.pyw', 'glide_start.py': 'Schnellstart.pyw'}.get(path.name, path.name)
    delivered = ROOT/'07_Python-Versionen'/name
    if not delivered.exists() or hashlib.sha256(delivered.read_bytes()).hexdigest() != digest:
        result['delivery_differences'].append(path.name)

tree = ast.parse((SOURCE/'home_task_tiles.py').read_text(encoding='utf-8'))
imports = [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
assert not any(name and ('tkinter' in name or name == 'app') for name in imports)
result['renderer_functions'] = {node.name: node.end_lineno-node.lineno+1 for node in ast.walk(tree)
                                if isinstance(node, ast.FunctionDef)}
assert max(result['renderer_functions'].values()) <= 50
for name in ('packaging/macos/baue_app.py', 'scripts/pflege/abgleich_07.py'):
    copy_tree = ast.parse((REPO/name).read_text(encoding='utf-8'))
    assert any(isinstance(node, ast.Constant) and node.value == 'home_task_tiles.py' for node in ast.walk(copy_tree))

result['interaction'] = json.loads((HERE/'bedienung.json').read_text(encoding='utf-8'))
assert result['interaction']['button_checks'] == 300
assert all(result['interaction'][key] for key in ('undo_redo', 'stale_callback', 'write_failure', 'read_only'))
for name in ('b01', 'b02', 'b04'):
    check = json.loads((HERE/(name+'.json')).read_text(encoding='utf-8'))
    assert not check['fehler'] and check['faelle'][name]['ok']

documents = [ROOT/name for name in subprocess.check_output(['git', 'diff', '--name-only'], cwd=ROOT,
                                                          text=True, encoding='utf-8').splitlines() if name.endswith('.md')]
documents += [HERE/'README.md', HERE.parent/'codebasis_2026-10-26/README.md']
for path in documents:
    content = re.sub(r'```.*?```', '', path.read_text(encoding='utf-8-sig'), flags=re.S)
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', content):
        target = target.strip().strip('<>').split(' "', 1)[0]
        if not target or urlsplit(target).scheme:
            continue
        filename, _, anchor = unquote(target).partition('#')
        destination = (path.parent/filename).resolve() if filename else path
        result['links_checked'] += 1
        if not destination.exists():
            result['errors'].append(f'{path.relative_to(ROOT)}: fehlendes Ziel {target}')
        elif anchor and destination.suffix == '.md':
            result['anchors_checked'] += 1
            if anchor not in headings(destination):
                result['errors'].append(f'{path.relative_to(ROOT)}: fehlender Anker {target}')
diff = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
result['git_diff_check_exitcode'] = diff.returncode
if diff.returncode:
    result['errors'].append(diff.stdout+diff.stderr)
result['ok'] = not result['errors']
(HERE/'abschluss.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({key:value for key,value in result.items() if key != 'source_manifest'}, ensure_ascii=False, indent=2))
raise SystemExit(int(not result['ok']))
