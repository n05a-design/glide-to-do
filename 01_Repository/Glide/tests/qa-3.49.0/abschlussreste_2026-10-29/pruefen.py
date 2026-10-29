"""Eingefrorene Bereichsprüfung zum Abarbeiten offener Abnahmereste."""
import argparse
import json
import os
from pathlib import Path
import sys

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[2]
sys.path.insert(0, str(REPO / 'tests/tools'))
from pruefablauf import einfrieren, Pruefablauf, dateien, sha256


def clean(value):
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items()}
    if isinstance(value, list):
        return [clean(v) for v in value]
    if isinstance(value, str):
        return value.replace(str(Path.home()), '%USERPROFILE%').replace(Path.home().as_posix(), '%USERPROFILE%')
    return value


def write(name, value):
    (OUT / name).write_text(json.dumps(clean(value), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--suite', action='append', required=True)
    parser.add_argument('--fall')
    parser.add_argument('--capture', type=Path)
    args = parser.parse_args()
    if (OUT/(args.name+'.json')).exists():
        raise FileExistsError('Vorhandenen Prüfbeleg erhalten; neuen --name wählen.')
    original = dateien(REPO)
    frozen, directory = einfrieren(REPO)
    guard = Pruefablauf(frozen)
    result = {'scope': args.name, 'frozen': str(directory), 'source_sha256': original,
              'app_sha256': sha256(REPO/'src/glide/app.pyw'), 'cases': [], 'complete': False,
              'global_acceptance': False}
    for index, name in enumerate(args.suite):
        report = directory / (name+'.json')
        command = [sys.executable, '-B', 'tests/integration/test_'+name+'.py', '--report', str(report)]
        if args.fall:
            command += ['--fall', args.fall]
        if args.capture:
            command += ['--capture', str(args.capture.resolve())]
        print('START '+name, flush=True)
        run = guard.command(name, command, timeout=420, environment=os.environ, cwd=frozen)
        row = {'suite': name, 'returncode': None if run is None else run.returncode,
               'ok': run is not None and run.returncode == 0 and not guard.stopped}
        if run is not None:
            (OUT/(args.name+'_'+name+'.log')).write_text(clean(run.stdout+'\n'+run.stderr), encoding='utf-8')
        if report.is_file():
            write(args.name+'_'+name+'.json', json.loads(report.read_text(encoding='utf-8-sig')))
            row['report'] = args.name+'_'+name+'.json'
        result['cases'].append(row)
        print(('OK ' if row['ok'] else 'ROT ')+name, flush=True)
        write(args.name+'.json', result)
        if not row['ok']:
            result['not_executed'] = args.suite[index+1:]
            break
    result['complete'] = True
    result['all_executed_green'] = len(result['cases']) == len(args.suite) and all(r['ok'] for r in result['cases'])
    result['source_unchanged'] = dateien(REPO) == original
    result['frozen_integrity'] = guard.integrity()
    result['guard'] = str(guard.root)
    write(args.name+'.json', result)
    print(json.dumps(clean({k:v for k,v in result.items() if k!='source_sha256'}), ensure_ascii=False), flush=True)
    return 0 if result['all_executed_green'] and result['source_unchanged'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
