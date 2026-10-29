"""Originale rote Bedienfälle beobachten; nur künstliche eigene Tk-Fenster."""
import hashlib
import argparse
import json
import os
from pathlib import Path
import sys
import tempfile
import traceback

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[2]
sys.path.insert(0, str(REPO/'tests/integration'))
sys.path.insert(0, str(REPO/'tests/tools'))
import test_arbeitsmodi as suite
from releasedaten import save_windows_screenshot

parser = argparse.ArgumentParser()
parser.add_argument('--name', default='ui_diagnose')
parser.add_argument('--capture-all', action='store_true')
args = parser.parse_args()
report_path = OUT/(args.name+'.json')
if report_path.exists():
    raise FileExistsError('Vorhandenen Diagnosebeleg erhalten; neuen --name wählen.')
CAPTURE = OUT/(args.name+'_bilder')
CAPTURE.mkdir(exist_ok=True)
rows = []
original_check = suite.befunde_b15
active = {}


def observe_buttons(run, context):
    count, findings = original_check(run, context)
    if findings:
        active.setdefault('button_findings',[]).append({'context':context,'findings':findings})
        if os.name == 'nt':
            save_windows_screenshot(run.root,CAPTURE/(active['case']+'-'+str(len(active['button_findings']))+'.png'))
    return count, findings


suite.befunde_b15 = observe_buttons
for name in ['kopfverweise','nebenansicht_seite','kompakt','gestaltung']:
    print('START',name,flush=True)
    active = {'case':name,'app_sha256':hashlib.sha256((REPO/'src/glide/app.pyw').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='ui-rest-diagnose-',dir=Path.home()/'GlidePruefung') as folder:
        run = suite.Lauf(REPO/'src/glide/app.pyw',folder)
        run.capture = CAPTURE if args.capture_all else None
        root_geometry = run.root.geometry
        calls = []
        def geometry(spec=None):
            result = root_geometry() if spec is None else root_geometry(spec)
            calls.append({'requested':spec,'returned':result})
            return result
        run.root.geometry = geometry
        try:
            active['result'] = getattr(suite,'fall_'+name)(run)
            active['passed'] = True
        except Exception:
            active['passed'] = False
            active['error'] = traceback.format_exc().replace(str(Path.home()),'%USERPROFILE%')[-1900:]
            active['geometry'] = root_geometry()
            active['geometry_calls'] = calls[-12:]
            active['screen'] = [run.root.winfo_screenwidth(),run.root.winfo_screenheight()]
            if os.name == 'nt':
                save_windows_screenshot(run.root,CAPTURE/(name+'.png'))
            if name == 'kopfverweise':
                editor = run.app.rich_note_editor
                active['head'] = {'title':str(editor.title_label.cget('text')),
                    'title_pixels':run.mod.tkfont.Font(font=editor.title_label.cget('font')).measure(editor.title_label.cget('text')),
                    'text_width':editor.text.winfo_width(),'read_pad':editor._read_pad,
                    'actions_width':editor.page_head_width(),'gap':editor.HEAD_ACTION_GAP,
                    'fits':editor._head_fits}
            if name == 'nebenansicht_seite':
                text = suite.seitenbaum(run.app)
                marks = [w for w in text.winfo_children() if isinstance(w,run.mod.tk.Label)
                         and w.cget('text') in (run.app.ICONS['task_open'],run.app.ICONS['check'])]
                active['marks'] = [{'mapped':bool(w.winfo_ismapped()),'index':text.index(w._w)} for w in marks]
                before = len(run.app.undo_stack)
                for mark in marks:
                    text.see(mark._w);run.idle(5)
                    active['visible_after_see'] = bool(mark.winfo_ismapped())
                    mark.event_generate('<Button-1>');run.idle(5)
                active['undo_delta_after_visible_click'] = len(run.app.undo_stack)-before
        finally:
            suite.abbauen(run)
    rows.append(active)
    report_path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(name,active.get('passed'),active.get('head',active.get('marks',active.get('geometry'))),flush=True)
