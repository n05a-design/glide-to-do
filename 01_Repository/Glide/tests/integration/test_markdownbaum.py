"""FP-07/1: echter Menü-/Dialogweg, Showcase, Abbruch und Flush-Schranke."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import threading
import time
import traceback
from unittest.mock import patch
from urllib.parse import unquote

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO/'tests/integration'))
from test_schutzrunde import Lauf


# Sperrdateien sind keine Nutzdaten: Seit WA-31 hält die Sitzung die
# OS-Sperre auf glide.lock.acquire, unter Windows ist sie dann nicht lesbar.
# Die App nimmt beide beim Kopieren eines Datenordners ebenso aus.
SPERRDATEIEN = {'glide.lock', 'glide.lock.acquire'}


def filehashes(directory):
    return {str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in Path(directory).rglob('*') if p.is_file() and p.name not in SPERRDATEIEN}


def modal(run, dialog):
    deadline = time.monotonic()+30
    while dialog.winfo_exists() and time.monotonic()<deadline:
        run.idle(1);time.sleep(.005)
    assert not dialog.winfo_exists(), 'Exportdialog blieb offen'


def export(run, target):
    with patch.object(run.app, 'run_modal', side_effect=lambda d:modal(run,d)):
        run.app.export_all_markdown(str(target))


def fall_showcase(run, directory):
    # Vorschauen sind ein unabhängiger schreibender Cache-Dienst und haben eine
    # eigene Pflichtsuite. Für den Bytevergleich des Exportwegs pausieren wir
    # ihre Anforderung bereits vor dem Laden der künstlichen Showcase-Daten.
    with patch.object(run.app.previews,'request_conversion',return_value='test-paused'):
        return showcase_export(run,directory)


def showcase_export(run, directory):
    app=run.app
    fixture=REPO/'tests/fixtures/showcase/Glide-Showcase_App.glideapp'
    assert app.restore_app_backup(str(fixture), sections={
        'tasks':True,'settings':True,'templates':True,'activity':True}, show_success=False)
    run.idle()
    assert app.output_editor_ready()
    before=filehashes(Path(run.data))
    original=copy.deepcopy(app.data_payload())
    target=directory/'ausgabe'
    export(run,target)
    assert target.is_dir(),run.meldungen
    inv=json.loads((target/'INVENTAR.json').read_text(encoding='utf-8'))
    assert inv['bestand']['lists']==original['lists']
    assert len([v for v in inv['objekte'] if v['art']=='list'])==len(app.lists)
    assert inv['zaehlung']['aufgaben']==sum(i.get('kind','task')=='task' for e in app.lists for i in app.walk_items(e.get('items',[])))
    expected=sum(len(h.get('attachments') or []) for h in [*app.folders,*app.lists,
        *(i for e in app.lists for i in app.walk_items(e.get('items',[])))])
    assert inv['zaehlung']['anhangverweise']==expected,(inv['zaehlung'],expected)
    assert all(a['status']=='kopiert' for a in inv['anhaenge']),inv['hinweise']
    links=0;checkboxes=0
    for path in target.rglob('*.md'):
        checkboxes+=len(re.findall(r'^\s*- \[[ x]\]',path.read_text(encoding='utf-8'),re.M))
        for ref in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
            if re.match(r'^[A-Za-z]+:',ref):continue
            relative,_,anchor=unquote(ref).partition('#')
            dest=path.parent/relative
            assert dest.is_file(),(path.name,ref)
            if anchor:assert f'id="{anchor}"' in dest.read_text(encoding='utf-8'),anchor
            links+=1
    manifest=json.loads((target/'MANIFEST.json').read_text(encoding='utf-8'))['sha256']
    assert all(hashlib.sha256((target/n).read_bytes()).hexdigest()==h for n,h in manifest.items())
    assert all(len(str(p))<=240 for p in target.rglob('*'))
    assert checkboxes==inv['zaehlung']['aufgaben'],(checkboxes,inv['zaehlung']['aufgaben'])
    after=filehashes(Path(run.data))
    assert after==before,('Quelldateien durch Ausgabe verändert',[n for n in sorted(set(before)|set(after)) if before.get(n)!=after.get(n)])
    return dict(**inv['zaehlung'], dateien=len(manifest)+1, relative_links=links,checkboxen=checkboxes)


def fall_abbruch_fehler(run,directory):
    app=run.app;target=directory/'abbruch'
    import markdown_tree
    entered=threading.Event();tick=[]
    original=markdown_tree.write_tree
    def delayed(*args,cancel=None,**kwargs):
        entered.set()
        assert cancel.wait(5),'Abbruch nicht beim Worker angekommen'
        return original(*args,cancel=cancel,**kwargs)
    def abort(dialog):
        deadline=time.monotonic()+5
        while not entered.is_set() and time.monotonic()<deadline:run.idle(1);time.sleep(.005)
        run.root.after(1,lambda:tick.append(True))
        dialog.event_generate('<Escape>')
        # Event hat auch bei fehlendem WM-Fokus denselben gebundenen Rückruf.
        dialog.tk.call(dialog.protocol('WM_DELETE_WINDOW'))
        modal(run,dialog)
    with patch.object(markdown_tree,'write_tree',side_effect=delayed),patch.object(app,'run_modal',side_effect=abort):
        app.export_all_markdown(str(target))
    assert tick and not target.exists()
    assert not list(directory.glob('.glide-md-*'))
    target.mkdir();(target/'behalten').write_bytes(b'vorher')
    export(run,target)
    assert (target/'behalten').read_bytes()==b'vorher'
    assert any(m[0]=='show_error' for m in run.meldungen)


def fall_flush_dialog(run,directory):
    app=run.app
    with patch.object(app,'output_editor_ready',return_value=False),patch.object(run.mod.filedialog,'askdirectory') as dialog:
        app.export_all_markdown()
        dialog.assert_not_called()
    with patch.object(run.mod.filedialog,'askdirectory',return_value=''):
        app.export_all_markdown()
    assert not list(directory.glob('ausgabe*'))
    # Sichtbares Menü und Palette verwenden dieselbe klassifizierte Aktion.
    entries=[entry for entry in app.app_action_entries() if entry['id']=='export_all_markdown']
    assert len(entries)==1 and entries[0]['label']=='Alles als Markdown-Ordner …'
    assert entries[0]['group']=='Export'
    assert app.app_action_group(entries[0]['label'])=='Export'


CASES=('showcase','abbruch_fehler','flush_dialog')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--app',type=Path,default=REPO/'src/glide/app.pyw')
    parser.add_argument('--report',type=Path);parser.add_argument('--fall',choices=CASES)
    args=parser.parse_args();report={'app_sha256':hashlib.sha256(args.app.read_bytes()).hexdigest(),'faelle':{}}
    for name in ([args.fall] if args.fall else CASES):
        run=None
        with tempfile.TemporaryDirectory(prefix='glide-fp07-') as directory:
            try:
                run=Lauf(args.app,str(Path(directory)/'daten'))
                evidence=globals()['fall_'+name](run,Path(directory))
                assert not run.errors,run.errors
                report['faelle'][name]={'ok':True,'messung':evidence};print('OK',name,evidence or '',flush=True)
            except Exception:
                error=traceback.format_exc().replace(str(Path.home()),'~')[-2500:]
                report['faelle'][name]={'ok':False,'fehler':error};print('ROT',name,error,flush=True)
            finally:
                if run is not None:run.app.previews.close();run.ende()
    if args.report:args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return int(any(not v['ok'] for v in report['faelle'].values()))


if __name__=='__main__':raise SystemExit(main())
