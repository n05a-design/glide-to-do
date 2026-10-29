"""Zwei gezielte WA-41-Proben mit -X dev; keine Produktionsaenderung."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time

HERE=Path(__file__).resolve().parent
QA=HERE.parent
ROOT=HERE.parents[4]
FROZEN=Path((QA/'dreierpaket_2026-10-27/freeze_ort.log').read_text(encoding='utf-8').strip())
REPO=FROZEN/'01_Repository/Glide'
proof=json.loads((QA/'dreierpaket_2026-10-27/quellstand.json').read_text(encoding='utf-8'))


def integrity(base):
    return [name for name,expected in proof['sha256'].items()
        if not (base/name).is_file() or hashlib.sha256((base/name).read_bytes()).hexdigest()!=expected]


report=dict(started=datetime.now(timezone.utc).isoformat(),version='3.48.0',schema=26,
    source_before=integrity(ROOT),frozen_before=integrity(FROZEN),cases=[],completed=False,
    cause_confirmed=False,release_ready=False)


def save():
    (HERE/'ergebnis.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


save()
assert not report['source_before'] and not report['frozen_before']
plan=[('315_dev_core',QA/'wa41_2026-10-27/probe.py',
       ['--repo',str(REPO),'--output',str(HERE/'315_dev_core.trace.log'),'--variant','normal']),
      ('315_dev_full',REPO/'tests/integration/test_speicherlast330.py',[])]
env=os.environ.copy()
env.update(PYTHONHASHSEED='0',PYTHONUTF8='1',PYTHONFAULTHANDLER='1',PYTHONDONTWRITEBYTECODE='1')
env.pop('PYTHONMALLOC',None)
env.pop('PYTHONDEVMODE',None)
for name,script,arguments in plan:
    print('START',name,flush=True)
    metadata=HERE/f'{name}.context.json'
    command=[sys.executable,'-B','-u','-X','dev','-X','faulthandler',str(HERE/'lauf.py'),
             '--metadata',str(metadata),'--script',str(script),*arguments]
    output=HERE/f'{name}.stdout.log'
    started=time.monotonic()
    timed_out=False
    with tempfile.TemporaryDirectory(prefix='glide-wa41-dev-') as temporary:
        child_env=dict(env,GLIDE_DATA_DIR=temporary,GLIDE_TEST_MODE='1')
        with output.open('wb') as log:
            process=subprocess.Popen(command,cwd=REPO,env=child_env,stdout=log,stderr=subprocess.STDOUT)
            try:
                code=process.wait(timeout=450)
            except subprocess.TimeoutExpired:
                timed_out=True
                subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],capture_output=True,check=False)
                code=process.wait(timeout=30)
    raw=output.read_text(encoding='utf-8',errors='replace')
    context=json.loads(metadata.read_text(encoding='utf-8'))
    assert context['before']['dev_mode'] and context['before']['faulthandler']
    row=dict(case=name,exitcode=code,seconds=round(time.monotonic()-started,2),timed_out=timed_out,
        context=context,stdout_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
        warning_counts={kind:len(re.findall(r'\b'+kind+r':',raw)) for kind in
            ('ResourceWarning','DeprecationWarning','RuntimeWarning','ImportWarning')},
        fatal_messages=re.findall(r'^(?:Fatal Python error|Windows fatal exception|AssertionError|TypeError|NameError)[^\r\n]*',raw,re.M))
    if code==0:
        row['summary']=raw.strip().splitlines()[-1] if raw.strip() else 'Kernprobe bestanden'
    report['cases'].append(row)
    save()
    print('END',name,'exit',code,'seconds',row['seconds'],flush=True)
report.update(completed=True,finished=datetime.now(timezone.utc).isoformat(),
    source_after=integrity(ROOT),frozen_after=integrity(FROZEN))
save()
print(json.dumps({row['case']:row['exitcode'] for row in report['cases']}),flush=True)
raise SystemExit(bool(report['source_after'] or report['frozen_after']))
