"""Begrenzter AMD-Gegenlauf zu WA-41, ohne Produktions- oder Systemeingriffe.

Die Originalsuite bleibt unverändert. Vorhandene Kern-/Importhelfer werden
gesondert ausgewiesen. Alle Prozesse laufen nacheinander mit Testdaten.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
QA = HERE.parent
PROOF = QA / 'dreierpaket_2026-10-27/quellstand.json'
DIAG = QA / 'wa41_2026-10-27'
RUNTIMES = {
    '3147': Path.home() / 'AppData/Local/Programs/Python/Python314/python.exe',
    '3151': Path.home() / 'AppData/Local/Python/pythoncore-3.15-64/python.exe',
}
PLAN = [
    ('3147_core_1', '3147', 'core'),
    ('3147_full_1', '3147', 'full'),
    ('3147_pure_1', '3147', 'pure'),
    ('3147_full_2', '3147', 'full'),
    ('3147_import_1', '3147', 'import'),
    ('3147_core_2', '3147', 'core'),
    ('3147_full_3', '3147', 'full'),
    ('3151_full_1', '3151', 'full'),
]
parser = argparse.ArgumentParser()
parser.add_argument('--bericht', type=Path, default=HERE / 'fester_pruefordner')
args = parser.parse_args()
OUTPUT = args.bericht.resolve()
OUTPUT.mkdir(parents=True, exist_ok=True)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


proof = json.loads(PROOF.read_text(encoding='utf-8'))


def integrity(base):
    return [name for name, expected in proof['sha256'].items()
            if not (base / name).is_file() or digest(base / name) != expected]


def powershell(code):
    result = subprocess.run(['pwsh', '-NoProfile', '-Command', code],
                            capture_output=True, text=True, encoding='utf-8',
                            errors='replace', timeout=30, check=True)
    return json.loads(result.stdout.lstrip('\ufeff'))


if (OUTPUT / 'ergebnis.json').exists():
    raise SystemExit('Dieser Nachweis existiert bereits; nicht ueberschreiben.')
before = integrity(ROOT)
if before:
    raise SystemExit(f'Quellmanifest weicht ab: {before}')
workspace = Path.home() / 'GlidePruefung'
workspace.mkdir(parents=True, exist_ok=True)
frozen = Path(tempfile.mkdtemp(prefix='amd-wa41-', dir=workspace)) / 'projekt'
for name in proof['sha256']:
    target = frozen / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / name, target)
repo = frozen / '01_Repository/Glide'
payload = frozen.parent / 'initial_amd.json'
data_root = frozen.parent / 'testdaten'
data_root.mkdir()
env = dict(os.environ, PYTHONHASHSEED='0', PYTHONUTF8='1',
           PYTHONFAULTHANDLER='1', PYTHONDONTWRITEBYTECODE='1',
           TMP=str(data_root), TEMP=str(data_root))
for key in ('PYTHONMALLOC', 'PYTHONPYCACHEPREFIX', 'PYTHONPATH', 'PYTHONHOME'):
    env.pop(key, None)
report = dict(started=datetime.now(timezone.utc).isoformat(),
              version='3.48.0', schema=26, source_files=len(proof['sha256']),
              source_before=before, frozen_before=integrity(frozen),
              frozen_root=str(frozen), execution='sequential',
              workspace_policy='Feste lokale Pruefablage ausserhalb OneDrive und System-TEMP; TMP/TEMP nur fuer Kinder umgeleitet.',
              plan=[dict(case=n, runtime=r, kind=k) for n, r, k in PLAN],
              original_intel_payload_available=False,
              original_intel_payload_sha256='a3b8c0cac4c72e1820e71730ad78e312f2a30338678fbcfe2a2b6d91dae081f4',
              full_suite_input='Original erzeugt selbst; UUIDs/Zeitstempel nicht bytegleich zu Intel.',
              runtime_info={}, cases=[], completed=False, cause_confirmed=False,
              release_ready=False, production_changed=False,
              helper_sha256={str(p.relative_to(ROOT)): digest(p) for p in
                             (Path(__file__), DIAG / 'probe.py', DIAG / 'pure_probe.py')})
report['machine'] = powershell(
    '[ordered]@{cpu=@(Get-CimInstance Win32_Processor | Select-Object Name,Manufacturer,NumberOfCores,NumberOfLogicalProcessors);'
    'os=Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber,TotalVisibleMemorySize,FreePhysicalMemory;'
    'board=Get-CimInstance Win32_BaseBoard | Select-Object Manufacturer,Product,Version;'
    'bios=Get-CimInstance Win32_BIOS | Select-Object SMBIOSBIOSVersion,ReleaseDate} | ConvertTo-Json -Depth 5')


def save():
    (OUTPUT / 'ergebnis.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


save()
assert not report['frozen_before']
runtime_code = '''
import hashlib,importlib.metadata,json,os,platform,sys,sysconfig,tkinter
from pathlib import Path
root=tkinter.Tk(); root.withdraw()
base=Path(sys.base_prefix)
files=[Path(sys.executable),*base.glob('python3*.dll'),base/'DLLs/_tkinter.pyd',*base.glob('DLLs/tcl*.dll'),*base.glob('DLLs/tk*.dll')]
print(json.dumps(dict(python=sys.version,executable=sys.executable,platform=platform.platform(),
    tk=str(root.tk.call('package','provide','Tk')),tcl=str(root.tk.call('info','patchlevel')),
    gil_disabled=sysconfig.get_config_var('Py_GIL_DISABLED'),
    jit_enabled=getattr(getattr(sys,'_jit',None),'is_enabled',lambda:None)(),
    packages={d.metadata['Name']:d.version for d in importlib.metadata.distributions() if d.metadata['Name']},
    binaries={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files if f.is_file()})))
root.destroy()
'''
for tag, runtime in RUNTIMES.items():
    with tempfile.TemporaryDirectory(prefix='glide-amd-runtime-', dir=data_root) as temp:
        info = subprocess.run([str(runtime), '-B', '-c', runtime_code], env=dict(env, GLIDE_DATA_DIR=temp),
                              capture_output=True, text=True, encoding='utf-8', timeout=30, check=True)
    report['runtime_info'][tag] = json.loads(info.stdout)
    assert report['runtime_info'][tag]['python'].split()[0] == {'3147': '3.14.7', '3151': '3.15.1'}[tag]
save()

for number, (name, tag, kind) in enumerate(PLAN, 1):
    changed = integrity(frozen)
    if changed:
        report['aborted_source_integrity'] = dict(before_case=name, changed=changed)
        save()
        raise SystemExit('Pruefkopie veraendert; keine weiteren Faelle gestartet.')
    print(f'START {number}/{len(PLAN)} {name}', flush=True)
    command = [str(RUNTIMES[tag]), '-B', '-u', '-X', 'faulthandler']
    trace = OUTPUT / f'{name}.trace.log'
    if kind == 'full':
        command += [str(repo / 'tests/integration/test_speicherlast330.py')]
    elif kind == 'core':
        command += [str(DIAG / 'probe.py'), '--repo', str(repo), '--output', str(trace), '--variant', 'normal',
                    '--payload', str(payload)]
    else:
        command += [str(DIAG / 'pure_probe.py'), '--repo', str(repo), '--payload', str(payload),
                    '--bootstrap', 'none' if kind == 'pure' else 'import', '--iterations', '20']
    output = OUTPUT / f'{name}.stdout.log'
    started = time.monotonic()
    timed_out = False
    temporary = tempfile.mkdtemp(prefix='glide-amd-case-', dir=data_root)
    with output.open('wb') as log:
        process = subprocess.Popen(command, cwd=repo, env=dict(env, GLIDE_DATA_DIR=temporary, GLIDE_TEST_MODE='1'),
                                   stdout=log, stderr=subprocess.STDOUT)
        report['running'] = dict(case=name, pid=process.pid, started=datetime.now(timezone.utc).isoformat())
        save()
        try:
            exitcode = process.wait(timeout=300)
        except subprocess.TimeoutExpired:
            timed_out = True
            subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True, check=False)
            exitcode = process.wait(timeout=30)
    raw = output.read_text(encoding='utf-8', errors='replace')
    row = dict(case=name, runtime=tag, kind=kind, pid=process.pid, exitcode=exitcode,
               seconds=round(time.monotonic() - started, 2), timed_out=timed_out,
               stdout_sha256=digest(output),
               error_messages=re.findall(r'^(?:AssertionError|TypeError|NameError|RuntimeError|PermissionError|Fatal Python error)[^\r\n]*', raw, re.M))
    row['frozen_after'] = integrity(frozen)
    if trace.exists():
        events = [json.loads(line) for line in trace.read_text(encoding='utf-8').splitlines()]
        row.update(core_pass=any(e['event'] == 'core_pass' for e in events),
                   last_started_iteration=max((e['iteration'] for e in events if e['event'] == 'round'), default=None),
                   data_differences=[e for e in events if e['event'] == 'data_difference'], trace_sha256=digest(trace))
    expected_marker = (r'^test_speicherlast330: OK; 26420 Punkte.*40 Änderungsrunden verlustfrei'
                       if kind == 'full' else r'^PASS pure .* 20$')
    row['passed'] = (exitcode == 0 and not timed_out and
                     (row.get('core_pass', False) if kind == 'core' else bool(re.search(expected_marker, raw, re.M))))
    if kind in ('pure', 'import'):
        row['rounds_completed'] = len(re.findall(r'^round \d+ items 26420$', raw, re.M))
    row['summary'] = raw.strip().splitlines()[-1] if raw.strip() else 'core_pass im Trace'
    try:
        shutil.rmtree(temporary)
    except OSError as error:
        row['cleanup_error'] = str(error)
    report['cases'].append(row)
    report.pop('running', None)
    if payload.exists():
        report.update(payload_path=str(payload), payload_sha256=digest(payload), payload_bytes=payload.stat().st_size)
    save()
    print(f'END {name} passed={row["passed"]} exit={exitcode} seconds={row["seconds"]}', flush=True)
    if row['frozen_after']:
        report['aborted_source_integrity'] = dict(after_case=name, changed=row['frozen_after'])
        save()
        raise SystemExit('Pruefkopie veraendert; keine weiteren Faelle gestartet.')

report.update(completed=True, finished=datetime.now(timezone.utc).isoformat(),
              source_after=integrity(ROOT), frozen_after=integrity(frozen))
report['summary'] = {tag: dict(passed=sum(r['runtime'] == tag and r['passed'] for r in report['cases']),
                            failed=sum(r['runtime'] == tag and not r['passed'] for r in report['cases'])) for tag in RUNTIMES}
save()
print(json.dumps(report['summary']), flush=True)
raise SystemExit(bool(report['source_after'] or report['frozen_after'] or any(not r['passed'] for r in report['cases'])))
