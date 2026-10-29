"""WA-41: nur eigene Pruefprozesse auf einen logischen Prozessor begrenzen."""
import ctypes as c
from ctypes import wintypes as w
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
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
kernel=c.WinDLL('kernel32',use_last_error=True)
kernel.OpenProcess.argtypes=[w.DWORD,w.BOOL,w.DWORD]
kernel.OpenProcess.restype=w.HANDLE
kernel.CloseHandle.argtypes=[w.HANDLE]
kernel.CloseHandle.restype=w.BOOL
kernel.SetProcessAffinityMask.argtypes=[w.HANDLE,c.c_size_t]
kernel.SetProcessAffinityMask.restype=w.BOOL
kernel.GetProcessAffinityMask.argtypes=[w.HANDLE,c.POINTER(c.c_size_t),c.POINTER(c.c_size_t)]
kernel.GetProcessAffinityMask.restype=w.BOOL


def integrity(base):
    return [name for name,expected in proof['sha256'].items()
        if not (base/name).is_file() or hashlib.sha256((base/name).read_bytes()).hexdigest()!=expected]


def affinity(pid,pin):
    handle=kernel.OpenProcess(0x1200,False,pid)
    if not handle:
        raise c.WinError(c.get_last_error())
    process_mask=c.c_size_t()
    system_mask=c.c_size_t()
    try:
        if not kernel.GetProcessAffinityMask(handle,c.byref(process_mask),c.byref(system_mask)):
            raise c.WinError(c.get_last_error())
        before=process_mask.value
        if pin:
            assert before & 1, 'Logischer Prozessor 0 nicht erlaubt'
            if not kernel.SetProcessAffinityMask(handle,1):
                raise c.WinError(c.get_last_error())
        if not kernel.GetProcessAffinityMask(handle,c.byref(process_mask),c.byref(system_mask)):
            raise c.WinError(c.get_last_error())
        return dict(before=hex(before),after=hex(process_mask.value),system=hex(system_mask.value),
            verified=(process_mask.value==1) if pin else process_mask.value==before)
    finally:
        kernel.CloseHandle(handle)


report=dict(started=datetime.now(timezone.utc).isoformat(),source_before=integrity(ROOT),
    frozen_before=integrity(FROZEN),cases=[],completed=False,cause_confirmed=False,release_ready=False)


def save():
    (HERE/'ergebnis.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


save()
assert not report['source_before'] and not report['frozen_before']
env=os.environ.copy()
env.update(PYTHONHASHSEED='0',PYTHONUTF8='1',PYTHONFAULTHANDLER='1',PYTHONDONTWRITEBYTECODE='1')
for name in ('PYTHONMALLOC','PYTHONDEVMODE'):
    env.pop(name,None)
for name,pin in (('cpu0_1',True),('default_control',False),('cpu0_2',True)):
    print('START',name,flush=True)
    trace=HERE/f'{name}.trace.log'
    output=HERE/f'{name}.stdout.log'
    command=[sys.executable,'-B','-u','-X','faulthandler',str(QA/'wa41_2026-10-27/probe.py'),
        '--repo',str(REPO),'--output',str(trace),'--variant','normal']
    started=time.monotonic()
    timed_out=False
    with tempfile.TemporaryDirectory(prefix='glide-wa41-affinity-') as temporary,output.open('wb') as log:
        child=subprocess.Popen(command,cwd=REPO,env=dict(env,GLIDE_DATA_DIR=temporary,GLIDE_TEST_MODE='1'),
            stdout=log,stderr=subprocess.STDOUT)
        masks=affinity(child.pid,pin)
        assert masks['verified']
        try:
            code=child.wait(timeout=300)
        except subprocess.TimeoutExpired:
            timed_out=True
            subprocess.run(['taskkill','/PID',str(child.pid),'/T','/F'],capture_output=True,check=False)
            code=child.wait(timeout=30)
    events=[json.loads(line) for line in trace.read_text(encoding='utf-8').splitlines()]
    row=dict(case=name,pinned_to_logical_cpu0=pin,affinity=masks,exitcode=code,
        seconds=round(time.monotonic()-started,2),timed_out=timed_out,
        core_pass=any(event['event']=='core_pass' for event in events),
        stdout_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
        trace_sha256=hashlib.sha256(trace.read_bytes()).hexdigest(),
        last_events=events[-2:])
    report['cases'].append(row)
    save()
    print('END',name,'exit',code,'seconds',row['seconds'],flush=True)
report.update(completed=True,finished=datetime.now(timezone.utc).isoformat(),
    source_after=integrity(ROOT),frozen_after=integrity(FROZEN))
save()
print(json.dumps({r['case']:r['exitcode'] for r in report['cases']}),flush=True)
raise SystemExit(bool(report['source_after'] or report['frozen_after']))
