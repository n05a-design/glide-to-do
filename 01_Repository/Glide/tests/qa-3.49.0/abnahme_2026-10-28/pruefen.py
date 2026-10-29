"""Quellengebundene Abnahmeprüfung; keine produktiven Daten, Builds oder Codeänderungen."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

REPO = Path(__file__).resolve().parents[3]
ROOT = REPO.parents[1]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / 'tests/tools'))
from pruefablauf import einfrieren, Pruefablauf, dateien


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    original = dateien(REPO)
    frozen, directory = einfrieren(REPO)
    write('eingefroren.json', {'copy': str(directory).replace(str(Path.home()), '%USERPROFILE%'),
                              'runtime': sys.version, 'head': subprocess.check_output(
                                  ['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                              'source_sha256': original,
                              'app_sha256': digest(frozen / 'src/glide/app.pyw')})
    guard = Pruefablauf(frozen)
    cases = [('CI-Grundstufe', [sys.executable, '-B', 'tests/tools/ci_grundstufe.py',
                              '--protokoll', str(directory / 'grundstufe')], 600)]
    for name in ('wiederholen', 'wiederholungsregeln', 'ansichten', 'seitenkarten',
                 'erwaehnungen', 'auftraege', 'markdownbaum', 'arbeitsmodi',
                 'wiederanlauf', 'speicherstatus', 'sicherungszentrale', 'schutzrunde',
                 'bildkonversion'):
        report = directory / (name + '.json')
        cases.append((name, [sys.executable, '-B', 'tests/integration/test_' + name + '.py',
                            '--report', str(report)], 240))
    result = {'scope': 'Abnahmeaudit 3.49.0; ausgewählte breite Funktionsregression, keine Voll-/Native-Matrix',
              'app_sha256': digest(REPO / 'src/glide/app.pyw'),
              'source': original, 'cases': [], 'completed': False,
              'excluded': ['test_speicherlast330: bestehende WA-41-/Intel-Grenze',
                           'Dauer-/Leistungsstress', 'native fremde Plattformen', 'menschliche Abnahme'],
              'global_acceptance': False}
    write('testergebnis.json', result)
    for index, (name, command, timeout) in enumerate(cases):
        print(f'START {index+1}/{len(cases)} {name}', flush=True)
        try:
            run = guard.command(name, command, timeout=timeout, environment=os.environ, cwd=frozen)
            code = None if run is None else run.returncode
            row = {'case': name, 'returncode': code,
                   'ok': code == 0 and not guard.stopped,
                   'guard': str(guard.root).replace(str(Path.home()), '%USERPROFILE%')}
            if name == 'CI-Grundstufe':
                report = directory / 'grundstufe/ergebnis.json'
            else:
                report = directory / (name + '.json')
            if report.is_file():
                document = json.loads(report.read_text(encoding='utf-8-sig'))
                # Öffentlich prüfbare Daten enthalten keine lokalen Benutzerpfade.
                clean = json.dumps(document, ensure_ascii=False).replace(str(Path.home()), '%USERPROFILE%')
                write('lauf_' + name + '.json', json.loads(clean))
                row['report'] = 'lauf_' + name + '.json'
                row['report_sha256'] = digest(OUT / row['report'])
            result['cases'].append(row)
            print(('OK ' if row['ok'] else 'ROT ') + name, flush=True)
        except Exception as error:
            result['cases'].append({'case': name, 'ok': False, 'error': type(error).__name__})
            print(traceback.format_exc()[-1600:], flush=True)
        write('testergebnis.json', result)
        if guard.stopped or not result['cases'][-1]['ok']:
            result['not_executed'] = [item[0] for item in cases[index+1:]]
            break
    result['completed'] = True
    result['source_after_equal'] = dateien(REPO) == original
    result['frozen_integrity'] = guard.integrity()
    result['guard_report'] = str(guard.root / 'pruefablauf.json').replace(str(Path.home()), '%USERPROFILE%')
    result['all_executed_checks_green'] = len(result['cases']) == len(cases) and all(row['ok'] for row in result['cases'])
    write('testergebnis.json', result)
    return int(not result['all_executed_checks_green'])


if __name__ == '__main__':
    raise SystemExit(main())
