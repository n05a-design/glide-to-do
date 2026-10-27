"""Quellmanifest, neue Modulregistrierung und geänderte Dokumentverweise prüfen."""
import ast
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess
import sys
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ROOT = REPO.parents[1]
SOURCE = REPO/'src/glide'
proof = json.loads((HERE/'pruefung.json').read_text(encoding='utf-8'))
result = {'source_manifest_matches': True, 'links_checked': 0, 'anchors_checked': 0, 'errors': []}
(HERE/'abschluss.json').write_text('{"status": "running"}\n', encoding='utf-8')


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


for name, expected in proof['source_manifest'].items():
    if hashlib.sha256((SOURCE/name).read_bytes()).hexdigest() != expected:
        result['errors'].append(f'Geänderte Quelle seit Fachprüfung: {name}')
        result['source_manifest_matches'] = False

delivery = ROOT/'07_Python-Versionen'
differences = []
for name, expected in proof['source_manifest'].items():
    target = delivery/({'app.pyw': 'Glide-Aufgaben-und-Listen_v3.45.0.pyw',
                        'glide_start.py': 'Schnellstart.pyw'}.get(name, name))
    if not target.exists() or hashlib.sha256(target.read_bytes()).hexdigest() != expected:
        differences.append(name)
result['delivery_differences'] = differences
expected_differences = {'app.pyw', 'compact_mode.py', 'image_conversion.py', 'image_preview.py',
                        'save_comparison.py', 'persistence.py'}
if set(differences) != expected_differences:
    result['errors'].append('Unerwartete Laufzeitunterschiede zur Lieferung')

documents = [ROOT/name for name in subprocess.check_output(['git', 'diff', '--name-only'], cwd=ROOT,
                                                          text=True, encoding='utf-8').splitlines()
             if name.endswith('.md')]
documents.append(HERE/'README.md')
for path in documents:
    if not path.exists():
        continue
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

tree = ast.parse((SOURCE/'persistence.py').read_text(encoding='utf-8'))
result['coordinator_functions'] = {node.name: node.end_lineno-node.lineno+1 for node in ast.walk(tree)
                                   if isinstance(node, ast.FunctionDef)}
imports = [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
assert not any(name and 'tkinter' in name for name in imports)
assert max(result['coordinator_functions'].values()) <= 50
for name in ('packaging/macos/baue_app.py', 'scripts/pflege/abgleich_07.py'):
    namespace = ast.parse((REPO/name).read_text(encoding='utf-8'))
    assert any(isinstance(node, ast.Constant) and node.value == 'persistence.py' for node in ast.walk(namespace))

sys.path.insert(0, str(REPO/'tests/tools'))
namespace = runpy.run_path(str(REPO/'tests/tools/pruefen.py'), run_name='documentation_check')
result['documentation_check'] = namespace['dokumentation_pruefen']()
diff = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
result['git_diff_check_exitcode'] = diff.returncode
if diff.returncode:
    result['errors'].append(diff.stdout + diff.stderr)
result['ok'] = not result['errors']
(HERE/'abschluss.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(int(not result['ok']))
