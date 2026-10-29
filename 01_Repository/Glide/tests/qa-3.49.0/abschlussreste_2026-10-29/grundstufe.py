"""CI-Grundstufe am eingefrorenen Abschlussrest-Stand, ohne Originaldaten."""
import argparse
import json
from pathlib import Path
import sys

from pruefen import OUT, REPO, clean

sys.path.insert(0, str(REPO/'tests/tools'))
from pruefablauf import einfrieren, Pruefablauf, dateien, sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    args = parser.parse_args()
    target = OUT/(args.name+'.json')
    if target.exists():
        raise FileExistsError('Vorhandenen Beleg erhalten; neuen Namen wählen.')
    original = dateien(REPO)
    frozen, directory = einfrieren(REPO)
    guard = Pruefablauf(frozen)
    logs = directory/'ci-grundstufe'
    result = guard.command('ci-grundstufe', [sys.executable, '-B',
        'tests/tools/ci_grundstufe.py', '--protokoll', str(logs)], cwd=frozen, timeout=1800)
    report = {'source_sha256': original, 'app_sha256': sha256(REPO/'src/glide/app.pyw'),
              'returncode': None if result is None else result.returncode,
              'guard_stopped': guard.stopped, 'frozen_integrity': guard.integrity(),
              'source_unchanged': dateien(REPO) == original,
              'global_acceptance': False, 'guard': str(guard.root)}
    if result is not None:
        (OUT/(args.name+'.log')).write_text(clean(result.stdout+'\n'+result.stderr), encoding='utf-8')
    if (logs/'ergebnis.json').is_file():
        report['ci'] = json.loads((logs/'ergebnis.json').read_text(encoding='utf-8'))
    target.write_text(json.dumps(clean(report), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(clean({k:v for k,v in report.items() if k not in ('source_sha256', 'ci')})), flush=True)
    if 'ci' in report:
        print(json.dumps(clean(report['ci']), ensure_ascii=False), flush=True)
    return 0 if (result is not None and result.returncode == 0 and not guard.stopped
                 and report['source_unchanged']) else 1


if __name__ == '__main__':
    raise SystemExit(main())
