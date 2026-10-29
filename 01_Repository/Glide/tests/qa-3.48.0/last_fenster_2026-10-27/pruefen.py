"""Last-/Fensterfolge und saubere venv, alle Prozesse nacheinander."""
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
import venv
from ressourcen import Monitor

HERE=Path(__file__).resolve().parent
QA=HERE.parent
ROOT=HERE.parents[4]
FROZEN=Path((QA/'dreierpaket_2026-10-27/freeze_ort.log').read_text(encoding='utf-8').strip())
REPO=FROZEN/'01_Repository/Glide'
proof=json.loads((QA/'dreierpaket_2026-10-27/quellstand.json').read_text(encoding='utf-8'))


def integrity(base):
    return [name for name,expected in proof['sha256'].items()
        if not (base/name).is_file() or hashlib.sha256((base/name).read_bytes()).hexdigest()!=expected]


report=dict(started=datetime.now(timezone.utc).isoformat(),source_files=len(proof['sha256']),
    source_before=integrity(ROOT),frozen_before=integrity(FROZEN),cases=[],completed=False,
    cause_confirmed=False,release_ready=False)


def save():
    (HERE/'ergebnis.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


save()
assert not report['source_before'] and not report['frozen_before']
plan=[('small_visible_1',1,'visible','original'),('small_hidden_1',1,'hidden','original'),
      ('small_visible_2',1,'visible','original'),('small_hidden_2',1,'hidden','original'),
      ('small_pump',1,'visible','pump'),('medium_visible',15,'visible','original'),
      ('large_visible',150,'visible','original'),('large_hidden',150,'hidden','original'),
      ('clean_venv_full',None,None,None)]
env=os.environ.copy()
env.update(PYTHONHASHSEED='0',PYTHONUTF8='1',PYTHONFAULTHANDLER='1',PYTHONDONTWRITEBYTECODE='1')
for name in ('PYTHONPATH','PYTHONMALLOC','PYTHONDEVMODE'):
    env.pop(name,None)
with tempfile.TemporaryDirectory(prefix='glide-wa41-clean-venv-') as temporary:
    venv.EnvBuilder(with_pip=False,system_site_packages=False).create(Path(temporary)/'venv')
    clean_python=Path(temporary)/'venv/Scripts/python.exe'
    info=subprocess.run([str(clean_python),'-B','-s','-c',
        'import json,sys; print(json.dumps(dict(version=sys.version,isolated_environment=sys.prefix!=sys.base_prefix)))'],
        env=env,capture_output=True,text=True,encoding='utf-8',check=True)
    report['venv']=json.loads(info.stdout)
    save()
    for name,count,window,events_mode in plan:
        print('START',name,flush=True)
        trace=HERE/f'{name}.trace.log'
        output=HERE/f'{name}.stdout.log'
        command=[str(clean_python) if count is None else sys.executable,'-B','-u','-s','-X','faulthandler']
        if count is None:
            command.append(str(REPO/'tests/integration/test_speicherlast330.py'))
        else:
            command += [str(HERE/'probe.py'),'--repo',str(REPO),'--trace',str(trace),
                '--lists',str(count),'--window',window,'--events',events_mode]
        started=time.monotonic()
        samples=[]
        timed_out=False
        with tempfile.TemporaryDirectory(prefix='glide-wa41-scale-env-') as isolated:
            with output.open('wb') as log,(HERE/f'{name}.resources.log').open('w',encoding='utf-8') as resource_log:
                process=subprocess.Popen(command,cwd=REPO,env=dict(env,GLIDE_DATA_DIR=isolated,GLIDE_TEST_MODE='1'),
                    stdout=log,stderr=subprocess.STDOUT)
                monitor=Monitor(process.pid)
                try:
                    while process.poll() is None:
                        sample=dict(seconds=round(time.monotonic()-started,3),**monitor.sample())
                        samples.append(sample)
                        resource_log.write(json.dumps(sample)+'\n')
                        resource_log.flush()
                        if time.monotonic()-started>300:
                            timed_out=True
                            subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],capture_output=True,check=False)
                            break
                        time.sleep(0.5)
                    code=process.wait(timeout=30)
                finally:
                    monitor.close()
        raw=output.read_text(encoding='utf-8',errors='replace')
        row=dict(case=name,list_count=count,window=window,events=events_mode,exitcode=code,
            seconds=round(time.monotonic()-started,2),timed_out=timed_out,samples=len(samples),
            foreground_samples=sum(s['foreground'] for s in samples),
            peaks={key:max((s.get(key,0) for s in samples),default=0) for key in
                ('working_set','working_set_peak','private_bytes','handles','gdi_peak','user_peak')},
            minimum_available_physical=min((s['available_physical'] for s in samples if 'available_physical' in s),default=None),
            errors=re.findall(r'^(?:Fatal Python error|Windows fatal exception|AssertionError|TypeError|NameError)[^\r\n]*',raw,re.M),
            stdout_sha256=hashlib.sha256(output.read_bytes()).hexdigest())
        if trace.exists():
            rows=[json.loads(line) for line in trace.read_text(encoding='utf-8').splitlines()]
            row['trace_events']=rows
        report['cases'].append(row)
        save()
        print('END',name,'exit',code,'seconds',row['seconds'],flush=True)
report.update(completed=True,finished=datetime.now(timezone.utc).isoformat(),
    source_after=integrity(ROOT),frozen_after=integrity(FROZEN))
save()
print(json.dumps({row['case']:row['exitcode'] for row in report['cases']}),flush=True)
raise SystemExit(bool(report['source_after'] or report['frozen_after']))
