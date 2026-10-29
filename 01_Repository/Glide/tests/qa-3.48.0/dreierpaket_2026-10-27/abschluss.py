"""Quelltreue, Featureprüfung, Dokumente und tatsächliche Python-Lieferung."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ROOT = REPO.parents[1]
sys.path.insert(0, str(REPO / 'tests/tools'))
import ci_grundstufe as ci
import pruefen
import standpruefung as stand


def read(name):
    return json.loads((HERE / name).read_text(encoding='utf-8'))


result = dict(version='3.48.0', schema=26, errors=[], release_ready=False,
              python_delivery='3.47.0', native_packages='3.45.0')
proof = read('quellstand.json')
result['changed_after_freeze'] = [name for name, digest in proof['sha256'].items()
    if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest]
if result['changed_after_freeze']:
    result['errors'].append('Ausführbare Quelle/Prüfung/Ressource nach dem Einfrieren verändert')
result['delivery_differences'] = ci.lieferstand_abweichungen()
expected_delivery = {'Glide-Aufgaben-und-Listen_v3.48.0.pyw', 'home_task_tiles.py', 'release_notes.py',
                     'side_view.py', 'task_editing.py', 'resources/templates/glide_vorlagen.glidetemplates'}
if {name.replace('\\', '/') for name in result['delivery_differences']} != expected_delivery:
    result['errors'].append('Unerwarteter Abstand zwischen Quellkandidat und unveränderter Lieferung')
old_proof = json.loads((REPO / 'tests/qa-3.47.0/folgepakete_2026-10-27/quellstand.json').read_text(encoding='utf-8'))
result['old_delivery_files_verified'] = 0
old_files = {**old_proof['runtime'], **old_proof['resources']}
for name, expected in old_files.items():
    if name == 'drawing_prototype.pyw':
        continue
    target = {'app.pyw': 'Glide-Aufgaben-und-Listen_v3.47.0.pyw', 'glide_start.py': 'Schnellstart.pyw'}.get(name, name)
    data = (ROOT / '07_Python-Versionen' / target).read_bytes()
    # Tatsächliche Lieferbytes statt Git-Textblobs (dort können LF-Filter wirken).
    if hashlib.sha256(data).hexdigest() != expected:
        result['errors'].append('Bestehende Lieferung verändert: ' + name)
    result['old_delivery_files_verified'] += 1
for name, expected in [('arbeitsmodi_vorlauf.json', 26)]:
    report = read(name)
    if (report['fehler'] or len(report['faelle']) != expected
            or report['app_sha256'] != proof['app_sha256']):
        result['errors'].append('Fehlende/abweichende Featureprüfung: ' + name)
full = read('windows_vollpruefung/ergebnis.json')
suites = {Path(name).stem for name in pruefen.SUITEN}
steps = {row['schritt']: row for row in full['schritte']}
result['broad_suites'] = {'expected': len(suites),
    'passed': sorted(name for name in suites if steps.get(name, {}).get('status') == 'ausgeführt'),
    'failed': sorted(name for name in suites if steps.get(name, {}).get('status') != 'ausgeführt')}
result['original_full_failures'] = [row['schritt'] for row in full['schritte']
                                  if row['status'] == 'fehlgeschlagen']
result['original_full_exitcode'] = full['exitcode']
result['known_open_risk'] = 'WA-41: nativer Windows-Speicherlastabsturz, Ursache offen'
follow = read('nachpruefung.json')
historical = {'test_seitenkarten', 'test_ansichten', 'test_wiederholungsregeln'}
result['historical_followups'] = follow['altleser']
result['load_followups'] = follow['wa41']
historical_passed = {row['suite'] for row in follow['altleser'] if row['exitcode'] == 0}
if historical_passed != historical:
    result['errors'].append('Historische Gegenproben nicht vollständig grün')
allowed = {'Dokumentation', 'standpruefung', 'test_speicherlast330'} | historical_passed
if set(result['original_full_failures']) - allowed:
    result['errors'].append('Zusätzliche ungeklärte Fehler in der breiten Prüfung')
if set(result['broad_suites']['failed']) - ({'test_speicherlast330'} | historical_passed):
    result['errors'].append('Weitere Integrationssuiten fehlen/sind fehlgeschlagen')
checked = stand.lauf([ROOT], '3.48.0')
result['errors'].extend(checked.fehler)
result['documents'] = checked.fortgeschrieben + checked.festgeschrieben + checked.ohne_stand
result['documentation'] = pruefen.dokumentation_pruefen()
result['ci_exitcode'] = read('ci_abschluss/ergebnis.json')['exitcode']
if result['ci_exitcode']:
    result['errors'].append('Aktuelle CI-Grundstufe fehlgeschlagen')
for args in (['git', 'diff', '--check'], ['git', 'diff', '--cached', '--check']):
    check = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    if check.returncode:
        result['errors'].append(check.stdout + check.stderr)
result['local_feature_candidate_verified'] = not result['errors']
result['new_delivery_performed'] = False
(HERE / 'abschluss.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(int(bool(result['errors'])))
