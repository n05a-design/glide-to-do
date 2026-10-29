"""Originale Lastphasen mit explizit variierter Datenmenge und Fensterbehandlung."""
import argparse
import faulthandler
import hashlib
import json
import os
from pathlib import Path
import sys
import time

parser=argparse.ArgumentParser()
parser.add_argument('--repo',type=Path,required=True)
parser.add_argument('--trace',type=Path,required=True)
parser.add_argument('--lists',type=int,choices=(1,15,150),required=True)
parser.add_argument('--window',choices=('visible','hidden'),required=True)
parser.add_argument('--events',choices=('original','pump'),default='original')
args=parser.parse_args()
log=args.trace.open('w',encoding='utf-8',buffering=1)
started=time.monotonic()
faulthandler.enable()


def record(event,**values):
    log.write(json.dumps(dict(event=event,seconds=round(time.monotonic()-started,3),**values),ensure_ascii=False)+'\n')


def configure(root):
    if args.window=='hidden':
        root.withdraw()


def install(mod):
    original=mod.ListApp.__init__
    def initialize(self,*a,**kw):
        original(self,*a,**kw)
        if args.window=='visible':
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
        record('app_ready',state=self.root.state(),viewable=bool(self.root.winfo_viewable()))
    mod.ListApp.__init__=initialize


def files(folder):
    return sum(len(names) for _,_,names in os.walk(folder))


test=args.repo/'tests/integration/test_speicherlast330.py'
source=test.read_text(encoding='utf-8')
record('start',python=sys.version,hashseed=os.environ.get('PYTHONHASHSEED'),list_count=args.lists,
    window=args.window,events=args.events,test_sha256=hashlib.sha256(test.read_bytes()).hexdigest())
for original,replacement in (
    ('    loader.exec_module(mod)','    loader.exec_module(mod)\n    install(mod)'),
    ('    root = mod.tk.Tk()','    root = mod.tk.Tk()\n    configure(root)'),
    ('        for index in range(150):',f'        for index in range({args.lists}):'),
    ('        assert anzahl >= 20000, anzahl','        assert anzahl > 0, anzahl'),
    ('        groesse_mb = SPEICHER.stat().st_size / 1e6',
     '        groesse_mb = SPEICHER.stat().st_size / 1e6\n        record("bulk",items=anzahl,bytes=SPEICHER.stat().st_size,files=files(ordner),state=root.state())'),
    ('        for runde in range(40):',
     '        for runde in range(40):\n            record("round",iteration=runde,files=files(ordner),pending_callbacks=len(root.tk.call("after","info")),state=root.state())'),
):
    assert source.count(original)==1,original
    source=source.replace(original,replacement)
if args.events=='pump':
    original='            assert len(alle_punkte()) == erwartet, (runde, len(alle_punkte()), erwartet)'
    assert source.count(original)==1
    source=source.replace(original,original+'\n            ruhe(1)')
marker='        # Endgültiges Entfernen'
assert source.count(marker)==1
source=source[:source.index(marker)]+(
    '        assert not fehler, fehler\n'
    '        record("pass",iterations=40,items=anzahl,files=files(ordner))\n'
    '    finally:\n'
    '        app.cancel_pending_callbacks()\n'
    '        app.release_data_lock()\n'
    '        root.destroy()\n')
scope=dict(__file__=str(test),__name__='__main__',install=install,configure=configure,record=record,files=files)
try:
    exec(compile(source,str(test),'exec'),scope)
except BaseException as error:
    record('exception',type=type(error).__name__,message=str(error))
    raise
finally:
    log.close()
