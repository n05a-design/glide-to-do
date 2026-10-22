"""Analyseprobe: realer Sperrerwerb gegen Freigabe/Erneuerung am Zeitlimit.

Nur künstliche temporäre Daten. Kein Produktionsfix. Ein instrumentierter
Leseaufruf hält den bereits gelesenen LockState zurück, bis ein echter zweiter
Prozess eine veraltete Sperre über den unveränderten App-Einstieg übernommen
hat. Das erzwingt die Reihenfolge; ihre natürliche Häufigkeit wird nicht gemessen.
"""
import argparse
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta
from unittest.mock import patch

CHILD = r'''
import importlib.machinery, importlib.util, json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]).parent))
loader=importlib.machinery.SourceFileLoader('lock_child', sys.argv[1])
mod=importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
loader.exec_module(mod)
app=mod.ListApp.__new__(mod.ListApp)
gate=Path(sys.argv[2]); end=gate.with_suffix('.end')
deadline=time.monotonic()+45
while not gate.exists():
    if time.monotonic()>deadline: raise TimeoutError('gate')
    time.sleep(.005)
app.acquire_data_lock()
print(json.dumps({'read_only':app._data_read_only,'token':app._lock_token.get('token')}),flush=True)
while not end.exists():
    if time.monotonic()>deadline: raise TimeoutError('end')
    time.sleep(.005)
'''


def load(path, directory):
    os.environ['GLIDE_DATA_DIR']=str(directory)
    os.environ['GLIDE_TEST_MODE']='1'
    sys.path.insert(0,str(path.parent))
    loader=importlib.machinery.SourceFileLoader('lock_probe',str(path))
    mod=importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name,loader))
    sys.modules[loader.name]=mod
    loader.exec_module(mod)
    return mod


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--app',type=Path,required=True)
    parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args()
    results=[]
    with tempfile.TemporaryDirectory(prefix='glide-lock-transition-') as td:
        directory=Path(td);mod=load(args.app,directory)
        for action in ('release','renew'):
            app=mod.ListApp.__new__(mod.ListApp)
            app.acquire_data_lock()
            assert not app._data_read_only and app._lock_token
            own_token=app._lock_token['token']
            old=(datetime.now().astimezone()-timedelta(hours=9)).isoformat()
            record=dict(app._lock_token,refreshed_at=old,started_at=old)
            app._lock_token=dict(record)
            lock=Path(mod.LOCK_FILE)
            lock.write_text(json.dumps(record),encoding='utf-8')
            gate=directory/(action+'.gate')
            child=subprocess.Popen([sys.executable,'-B','-c',CHILD,str(args.app),str(gate)],
                env=dict(os.environ,GLIDE_DATA_DIR=td,PYTHONUTF8='1'),stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,text=True,encoding='utf-8')
            original=mod.glide_lock.read
            acquired={}
            used=False
            def interleaved(path):
                nonlocal used
                state=original(path)
                if not used and Path(path)==lock:
                    used=True;gate.touch()
                    acquired.update(json.loads(child.stdout.readline()))
                    assert acquired['read_only'] is False
                    assert original(lock).record['token']==acquired['token']!=own_token
                return state
            try:
                with patch.object(mod.glide_lock,'read',side_effect=interleaved):
                    value=app.release_data_lock() if action=='release' else app.check_data_lock(renew=True)
                state=original(lock)
                results.append(dict(action=action,second_process_acquired=True,
                    second_process_alive=child.poll() is None,return_value=value,
                    file_missing=state.kind==mod.glide_lock.MISSING,
                    foreign_token_preserved=state.kind==mod.glide_lock.VALID and state.record['token']==acquired['token'],
                    original_owner_replaced_foreign_token=state.kind==mod.glide_lock.VALID and state.record['token']==own_token))
            finally:
                gate.with_suffix('.end').touch()
                child.wait(timeout=15)
                if lock.exists():lock.unlink()
        # Gegenfall: die fremde Kennung ist schon vor dem Lesen sichtbar.
        app=mod.ListApp.__new__(mod.ListApp);app.acquire_data_lock()
        foreign=dict(app._lock_token,token='synthetic-foreign')
        lock=Path(mod.LOCK_FILE);lock.write_text(json.dumps(foreign),encoding='utf-8')
        before=lock.read_bytes();app.release_data_lock()
        results.append(dict(action='control_foreign_before_read',bytes_preserved=lock.read_bytes()==before))
        lock.unlink()
        # Erneuerung scheitert, die vorherige eigene Sperre bleibt bestehen.
        app=mod.ListApp.__new__(mod.ListApp);app.acquire_data_lock()
        past=(datetime.now().astimezone()-timedelta(seconds=5)).isoformat()
        app._lock_token=dict(app._lock_token,refreshed_at=past)
        lock.write_text(json.dumps(app._lock_token),encoding='utf-8');before=lock.read_bytes()
        with patch.object(app,'write_json_atomic',side_effect=OSError('synthetic renewal error')):
            allowed=app.check_data_lock(renew=True)
        results.append(dict(action='renew_write_failure',write_allowed=allowed,read_only=app._data_read_only,
                            lock_bytes_preserved=lock.read_bytes()==before))
        app.release_data_lock()
    report=dict(method='controlled two-process interleaving',source=str(args.app.name),
        mock_boundary='Only the timing of glide_lock.read; lock acquisition and release/renew methods are original.',
        natural_frequency='not measured',cases=results)
    args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))
    return 0


if __name__=='__main__':raise SystemExit(main())
