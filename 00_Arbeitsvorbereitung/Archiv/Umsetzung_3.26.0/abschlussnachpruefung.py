"""Ergänzende Nachprüfung; Originalprotokolle werden nicht überschrieben."""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from datetime import datetime

root = Path(__file__).resolve().parents[2]
repo = root / '01_Repository/Glide'
qa = repo / 'tests/qa-3.26.0'
original = qa / 'abschluss_2026-09-21/ergebnis.json'
if not original.exists():
    raise SystemExit('Vollständiges Ausgangsprotokoll fehlt noch.')
result = json.loads(original.read_text(encoding='utf-8'))
failed = {row['schritt'] for row in result['schritte'] if row['status'] == 'fehlgeschlagen'}
if failed - {'test_ui_polish36', 'test_ui39'}:
    raise SystemExit(f'Weitere Befunde zuerst bearbeiten: {failed}')
output = qa / 'abschluss_nachpruefung_2026-09-21'
output.mkdir(exist_ok=True)
env = dict(os.environ, PYTHONIOENCODING='utf-8')
checks = []
for name, path in [('test_ui_polish36', 'tests/integration/test_ui_polish36.py'),
                   ('test_ui39', 'tests/integration/test_ui39.py'),
                   ('test_features326', 'tests/integration/test_features326.py'),
                   ('sichtprobe326', 'tests/qa-3.26.0/sichtprobe326.py'),
                   ('standpruefung', 'tests/tools/standpruefung.py')]:
    process = subprocess.run([sys.executable, path], cwd=repo, env=env,
                             capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=300)
    (output / (name + '.log')).write_text(process.stdout + process.stderr, encoding='utf-8')
    checks.append({'schritt':name, 'exitcode':process.returncode})
    print(name, process.returncode, flush=True)
    if process.returncode:
        print(process.stdout + process.stderr, flush=True)
        break
spec = importlib.util.spec_from_file_location('qa_helpers', repo/'tests/tools/pruefen.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
for name, check in [('Syntax', helper.syntax_pruefen), ('Dokumentation', helper.dokumentation_pruefen)]:
    try:
        detail = check()
        checks.append({'schritt':name, 'exitcode':0, 'detail':detail})
    except Exception as error:
        checks.append({'schritt':name, 'exitcode':1, 'detail':str(error)})
source = repo/'src/glide/app.pyw'
copy = root/'07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.26.0.pyw'
digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
checks.append({'schritt':'Startkopie', 'exitcode':int(digest(source) != digest(copy)), 'sha256':digest(source)})
resources = repo/'src/glide/resources'
different = []
for item in resources.rglob('*'):
    if not item.is_file() or any(part.lower() in ('archiv','__pycache__') for part in item.relative_to(resources).parts):
        continue
    target = root/'07_Python-Versionen/resources'/item.relative_to(resources)
    if not target.exists() or digest(item) != digest(target):
        different.append(item.relative_to(resources).as_posix())
checks.append({'schritt':'Aktive Ressourcen', 'exitcode':int(bool(different)), 'abweichungen':different})
passed = not any(row['exitcode'] for row in checks) and not (failed - {row['schritt'] for row in checks if row['exitcode'] == 0})
summary = {'zeitpunkt':datetime.now().isoformat(), 'exitcode':0 if passed else 1,
           'original_vollpruefung':str(original.relative_to(repo)), 'original_exitcode':result['exitcode'],
           'hinweis':'Original bleibt erhalten. Ein archivierter Referenzpfad im Mondphasentest wurde durch eine dauerhafte Fixture ersetzt; die betroffene Suite wird vollständig wiederholt.',
           'programm_sha256':digest(source), 'schritte':checks}
(output/'ergebnis.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
raise SystemExit(summary['exitcode'])
