"""WA-41-Vergleich: originale Lastsuite und vorhandene isolierte Kernproben.

Nur eingefrorene Quellen und kuenstliche Testdaten. Keine globale Laufzeitwahl.
Die Fallfolge steht vor dem Start fest und laeuft absichtlich nacheinander.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent
QA = HERE.parent
ROOT = HERE.parents[4]
parser = argparse.ArgumentParser()
parser.add_argument('--python315', type=Path, required=True)
parser.add_argument('--control314', type=Path, required=True)
args = parser.parse_args()
frozen_root = Path((QA / 'dreierpaket_2026-10-27/freeze_ort.log').read_text(encoding='utf-8').strip())
frozen_repo = frozen_root / '01_Repository/Glide'
diagnostics = QA / 'wa41_2026-10-27'
payload = Path((diagnostics / 'payload_ort.log').read_text(encoding='utf-8').strip())
proof = json.loads((QA / 'dreierpaket_2026-10-27/quellstand.json').read_text(encoding='utf-8'))
plan = [
    ('315_full_1', '315', 'full'),
    ('314_core_1', '314', 'core'),
    ('315_core_1', '315', 'core'),
    ('315_import_1', '315', 'import'),
    ('315_full_2', '315', 'full'),
    ('314_core_2', '314', 'core'),
    ('315_core_2', '315', 'core'),
    ('315_import_2', '315', 'import'),
    ('315_full_3', '315', 'full'),
    ('315_import_3', '315', 'import'),
]
runtimes = {'315': args.python315.resolve(), '314': args.control314.resolve()}


def digest(file):
    return hashlib.sha256(file.read_bytes()).hexdigest()


def integrity(base):
    return [name for name, expected in proof['sha256'].items()
            if not (base / name).is_file() or digest(base / name) != expected]


report = dict(started=datetime.now(timezone.utc).isoformat(), version='3.48.0', schema=26,
    execution='sequential', plan=[dict(case=name, runtime=runtime, kind=kind) for name,runtime,kind in plan],
    runtime_info={}, cases=[], source_files=len(proof['sha256']),
    source_before=integrity(ROOT), frozen_before=integrity(frozen_root),
    payload_sha256=digest(payload), payload_bytes=payload.stat().st_size,
    script_sha256={file.name: digest(file) for file in (Path(__file__), diagnostics/'probe.py', diagnostics/'pure_probe.py')},
    cause_confirmed=False, release_ready=False, completed=False)


def save():
    (HERE / 'ergebnis.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


save()
if report['source_before'] or report['frozen_before']:
    raise SystemExit('Quellmanifest passt nicht; keine Pruefung gestartet')

env = os.environ.copy()
env.update(PYTHONHASHSEED='0', PYTHONUTF8='1', PYTHONFAULTHANDLER='1', PYTHONDONTWRITEBYTECODE='1')
env.pop('PYTHONMALLOC', None)
runtime_code = '''
import hashlib,json,sys,sysconfig,tkinter
from pathlib import Path
root=tkinter.Tk(); root.withdraw()
base=Path(sys.base_prefix)
files=[*base.glob('python3*.dll'),base/'DLLs/_tkinter.pyd',*base.glob('DLLs/tcl*.dll'),*base.glob('DLLs/tk*.dll')]
print(json.dumps(dict(python=sys.version,tk=str(root.tk.call('package','provide','Tk')),
    gil_disabled=sysconfig.get_config_var('Py_GIL_DISABLED'),
    jit_enabled=getattr(getattr(sys,'_jit',None),'is_enabled',lambda:None)(),
    binaries={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files if f.is_file()})))
root.destroy()
'''
for tag, runtime in runtimes.items():
    info = subprocess.run([str(runtime),'-B','-c',runtime_code],env=env,capture_output=True,text=True,encoding='utf-8',timeout=30,check=True)
    report['runtime_info'][tag]=json.loads(info.stdout)
save()

for number,(name,tag,kind) in enumerate(plan,1):
    print(f'START {number}/{len(plan)} {name}',flush=True)
    command=[str(runtimes[tag]),'-B','-u','-X','faulthandler']
    trace=HERE/f'{name}.trace.log'
    if kind=='full':
        command += [str(frozen_repo/'tests/integration/test_speicherlast330.py')]
    elif kind=='core':
        command += [str(diagnostics/'probe.py'),'--repo',str(frozen_repo),'--output',str(trace),'--variant','normal']
    else:
        command += [str(diagnostics/'pure_probe.py'),'--repo',str(frozen_repo),'--payload',str(payload),'--bootstrap','import','--iterations','20']
    output=HERE/f'{name}.stdout.log'
    started=time.monotonic()
    timed_out=False
    with tempfile.TemporaryDirectory(prefix='glide-wa41-315-env-') as temporary:
        case_env=dict(env,GLIDE_DATA_DIR=temporary,GLIDE_TEST_MODE='1')
        with output.open('wb') as log:
            process=subprocess.Popen(command,cwd=frozen_repo,env=case_env,stdout=log,stderr=subprocess.STDOUT)
            try:
                exitcode=process.wait(timeout=300)
            except subprocess.TimeoutExpired:
                timed_out=True
                # Nur diesen eigenen Pruefprozess und seine Schreiber beenden.
                subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],capture_output=True,check=False)
                exitcode=process.wait(timeout=30)
    raw=output.read_text(encoding='utf-8',errors='replace')
    errors=re.findall(r'^(?:AssertionError|TypeError|NameError|RuntimeError|Fatal Python error)[^\r\n]*',raw,re.M)
    row=dict(case=name,runtime=tag,kind=kind,exitcode=exitcode,seconds=round(time.monotonic()-started,2),
             timed_out=timed_out,stdout_sha256=digest(output),error_messages=errors)
    if trace.exists():
        events=[json.loads(line) for line in trace.read_text(encoding='utf-8').splitlines()]
        row['core_pass']=any(event['event']=='core_pass' for event in events)
        row['last_started_iteration']=max((event['iteration'] for event in events if event['event']=='round'),default=None)
        row['trace_sha256']=digest(trace)
    if kind=='import':
        row['rounds_completed']=len(re.findall(r'^round \d+ items 26420$',raw,re.M))
    if exitcode==0:
        row['summary']=raw.strip().splitlines()[-1] if raw.strip() else 'core_pass im Trace'
    report['cases'].append(row)
    save()
    print(f'END {name} exit={exitcode} seconds={row["seconds"]}',flush=True)

report.update(completed=True,finished=datetime.now(timezone.utc).isoformat(),
    source_after=integrity(ROOT),frozen_after=integrity(frozen_root))
report['summary']={tag:dict(passed=sum(r['runtime']==tag and r['exitcode']==0 for r in report['cases']),
    failed=sum(r['runtime']==tag and r['exitcode']!=0 for r in report['cases'])) for tag in runtimes}
save()
print(json.dumps(report['summary']),flush=True)
raise SystemExit(bool(report['source_after'] or report['frozen_after']))
