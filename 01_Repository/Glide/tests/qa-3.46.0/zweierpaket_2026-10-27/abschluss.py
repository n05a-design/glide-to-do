"""Endgültige Prüf-/Liefer-/Dokumentgrenzen des Zweierpakets nachvollziehen."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ROOT = REPO.parents[1]
frozen = json.loads((HERE/'vollpruefung_quellstand.json').read_text(encoding='utf-8'))
result = {'version': '3.46.0', 'errors': [], 'links_checked': 0, 'anchors_checked': 0}
(HERE/'abschluss.json').write_text('{"status":"running"}\n', encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summarize(path):
    report = json.loads(path.read_text(encoding='utf-8'))
    steps = report['schritte']
    return dict(exitcode=report['exitcode'], steps=len(steps),
                passed=sum(step['status'] == 'ausgeführt' for step in steps),
                skipped=[step['schritt'] for step in steps if step['status'] == 'übersprungen'],
                failed=[step['schritt'] for step in steps if step['status'] == 'fehlgeschlagen'])


for name, expected in frozen['source_manifest'].items():
    if digest(REPO/'src/glide'/name) != expected:
        result['errors'].append('Quelle nach Einfrieren geändert: '+name)
for name, expected in frozen['test_manifest'].items():
    if digest(REPO/name) != expected:
        result['errors'].append('Prüfcode nach Einfrieren geändert: '+name)
result['runtime_files'] = len(frozen['source_manifest'])
result['interrupted_full'] = json.loads((HERE/'vollpruefung_unterbrochen.json').read_text(encoding='utf-8'))
result['remaining_full'] = summarize(HERE/'windows_restlauf/ergebnis.json')
if result['remaining_full']['exitcode']:
    result['errors'].append('Fortsetzung des eingefrorenen Prüflaufs nicht grün')
result['single_complete_full_run'] = False
result['ci'] = summarize(HERE/'ci_streng/ergebnis.json')
if result['ci']['exitcode']:
    result['errors'].append('Strenge CI-Grundstufe nicht grün')
delivery = ROOT/'07_Python-Versionen'
differences = []
for name, expected in frozen['source_manifest'].items():
    target = delivery/({'app.pyw':'Glide-Aufgaben-und-Listen_v3.46.0.pyw',
                        'glide_start.py':'Schnellstart.pyw'}.get(name, name))
    if not target.exists() or digest(target) != expected:
        differences.append(name)
result['python_delivery_differences'] = differences
if differences:
    result['errors'].append('Python-Lieferung weicht von der eingefrorenen Quelle ab')
result['native_package_version'] = '3.45.0'
result['showcase_sha256'] = {}
for name in ('Glide-Showcase.glidebackup', 'Glide-Showcase_App.glideapp',
             'Glide-Showcase.glidetemplates', 'manifest.json', 'Showcase_starten.pyw', 'README.md'):
    source, target = REPO/'tests/fixtures/showcase'/name, ROOT/'05_Probelisten_Testdaten/Showcase'/name
    expected = digest(source)
    result['showcase_sha256'][name] = expected
    if digest(target) != expected:
        result['errors'].append('Showcase-Lieferung weicht ab: '+name)
work = json.loads((HERE/'windows_restlauf/arbeitsmodi.json').read_text(encoding='utf-8'))
result['work_modes'] = {'cases': len(work['faelle']), 'failed': work['fehler'], 'app_sha256': work['app_sha256']}
if work['fehler'] or not all(case['ok'] for case in work['faelle'].values()):
    result['errors'].append('Arbeitsmodifälle nicht alle grün')
if work['app_sha256'] != frozen['source_manifest']['app.pyw']:
    result['errors'].append('Arbeitsmodi nicht am eingefrorenen Apphash')
repeat_log = (HERE/'windows_voll/test_wiederholen.log').read_text(encoding='utf-8')
result['repeat_invalid_command_errors'] = repeat_log.count('invalid command name')
result['delivery_probe'] = json.loads((HERE/'python_lieferprobe.json').read_text(encoding='utf-8'))
if result['delivery_probe']['exitcode'] or result['delivery_probe']['callback_errors']:
    result['errors'].append('Python-Lieferprobe nicht grün')
geometry = json.loads((HERE/'gestaltung_final.json').read_text(encoding='utf-8'))
result['geometry'] = geometry['faelle']
if geometry['fehler'] or geometry['app_sha256'] != frozen['source_manifest']['app.pyw']:
    result['errors'].append('Gestaltungsnachweis nicht am eingefrorenen grünen Stand')


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


documents = [ROOT/name for name in subprocess.check_output(['git','diff','--name-only'], cwd=ROOT,
                                                          text=True, encoding='utf-8').splitlines()
             if name.endswith('.md') and (ROOT/name).exists()]
documents.append(HERE/'README.md')
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
diff = subprocess.run(['git','diff','--check'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
result['git_diff_check_exitcode'] = diff.returncode
if diff.returncode:
    result['errors'].append(diff.stdout+diff.stderr)
result['ok'] = not result['errors']
(HERE/'abschluss.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(int(not result['ok']))
