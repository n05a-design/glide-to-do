"""Kontrollierte verzögerte Ereignisverarbeitung; Originalassertions unverändert."""
import argparse
import json
from pathlib import Path
import sys
import tempfile
import traceback

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[2]
sys.path.insert(0, str(REPO/'tests/integration'))
import test_arbeitsmodi as suite

parser = argparse.ArgumentParser()
parser.add_argument('--name', required=True)
args = parser.parse_args()
target = OUT/(args.name+'.json')
if target.exists():
    raise FileExistsError('Vorhandenen Beleg erhalten; neuen Namen wählen.')
result = {'event_delay_ms':450, 'delay_executed':False, 'writes_with_open_draft':[]}
with tempfile.TemporaryDirectory(prefix='side-timer-', dir=Path.home()/'GlidePruefung') as folder:
    run = suite.Lauf(REPO/'src/glide/app.pyw',folder)
    run.capture = None
    original_save = run.app.save_items
    original_idle = suite.idle
    def has_draft():
        editor = getattr(run.app,'rich_note_editor',None)
        return editor is not None and 'Unveränderter Hauptentwurf' in editor.text.get('1.0','end-1c')
    def save(*a,**kw):
        if has_draft():
            result['writes_with_open_draft'].append([{'function':r.name,'line':r.lineno}
                                                   for r in traceback.extract_stack()[-9:]])
        return original_save(*a,**kw)
    def delayed_idle(lauf,runden=4):
        original_idle(lauf,runden)
        if has_draft() and not result['delay_executed']:
            result['delay_executed'] = True
            ready = run.mod.tk.BooleanVar(master=run.root,value=False)
            run.root.after(450,lambda:ready.set(True))
            run.root.wait_variable(ready)
    run.app.save_items = save
    suite.idle = delayed_idle
    try:
        result['result'] = suite.fall_side_verweisnavigation(run)
        result['passed'] = True
    except Exception:
        result['passed'] = False
        result['error'] = traceback.format_exc().replace(str(Path.home()),'%USERPROFILE%')[-2000:]
    finally:
        suite.idle = original_idle
        run.app.save_items = original_save
        suite.abbauen(run)
target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
raise SystemExit(0 if result['passed'] else 1)
