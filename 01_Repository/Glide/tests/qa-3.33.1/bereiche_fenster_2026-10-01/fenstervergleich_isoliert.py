"""Unprofilierte, alternierende Messung realer Button- und Modalwege, nur temporäre Daten."""
import subprocess,os,sys,time,tempfile,importlib.util,importlib.machinery,json,zipfile,statistics,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[3];Q=Path(__file__).resolve().parent
raw=[]
if '--sample' in sys.argv:
 iteration=int(sys.argv[3]);variant=sys.argv[2]
 src=Q/'vorher/quelle/app.pyw' if variant=='alt' else R/'src/glide/app.pyw'
 with tempfile.TemporaryDirectory(prefix='glide-window-compare-') as d:
  os.environ['GLIDE_DATA_DIR']=d;os.environ['GLIDE_TEST_MODE']='1'
  with zipfile.ZipFile(R/'tests/fixtures/beispiele/glide_beispieldaten.glidebackup') as z:Path(d,'liste_speicher.json').write_bytes(z.read('data.json'))
  loader=importlib.machinery.SourceFileLoader('glide_compare_'+variant,str(src));m=importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name,loader));loader.exec_module(m)
  root=m.tk.Tk();root.geometry('1400x950+20+20');errors=[];root.report_callback_exception=lambda *e:errors.append(str(e[1]));a=m.ListApp(root)
  for _ in range(3):root.update()
  a.set_active_list(max(a.lists,key=lambda e:a.count_items(e.get('items',[])))['id']);a.open_board_view()
  for _ in range(3):root.update()
  original=a.run_modal;ready=[];closing=[]
  def modal(dialog,parent=None):
   # Existing production foreground entry remains real; record when mapping/lifting finishes.
   old_bring=a.bring_dialog_to_front
   def bring(target):
    old_bring(target);ready.append(time.perf_counter())
   a.bring_dialog_to_front=bring
   def close():
    t=time.perf_counter();dialog.focus_set();dialog.event_generate('<Escape>');closing.append((time.perf_counter()-t)*1000)
    assert not dialog.winfo_exists(),dialog.title()
   dialog.after(100,close)
   try:original(dialog,parent)
   finally:a.bring_dialog_to_front=old_bring
  a.run_modal=modal
  for button in ['actions_button','settings_button','print_button']:
   w=getattr(a,button);ready.clear();closing.clear();t=time.perf_counter()
   w.event_generate('<ButtonPress-1>',x=8,y=8);w.event_generate('<ButtonRelease-1>',x=8,y=8)
   assert ready and closing,(variant,button)
   if iteration:raw.append({'variant':variant,'round':iteration,'button':button,'ready_ms':(ready[0]-t)*1000,'close_ms':closing[0]})
   root.update()
  for section in ['pages','lists','notes']:
   arrow=getattr(a,'sidebar_heading_icon' if section=='lists' else section+'_heading_icon');t=time.perf_counter()
   arrow.event_generate('<Button-1>',x=6,y=6);root.update()
   if iteration:raw.append({'variant':variant,'round':iteration,'section':section,'toggle_ms':(time.perf_counter()-t)*1000})
  assert not errors,errors;root.destroy()
 print(iteration,variant,flush=True)
 Path(sys.argv[4]).write_text(json.dumps(raw));sys.exit(0)
with tempfile.TemporaryDirectory(prefix='glide-window-samples-') as folder:
 for iteration in range(6):
  for variant in (['alt','neu'] if iteration%2==0 else ['neu','alt']):
   destination=Path(folder)/f'{iteration}-{variant}.json'
   result=subprocess.run([sys.executable,'-B',__file__,'--sample',variant,str(iteration),str(destination)],capture_output=True,text=True,timeout=180)
   assert result.returncode==0,(iteration,variant,result.stdout,result.stderr)
   raw.extend(json.loads(destination.read_text()))
   print(iteration,variant,flush=True)
def stats(values):
 values=sorted(values);return {'median_ms':statistics.median(values),'p95_ms':values[min(len(values)-1, int(len(values)*.95))],'raw_ms':values}
summary={}
for variant in ['alt','neu']:
 summary[variant]={}
 for key in ['actions_button','settings_button','print_button','pages','lists','notes']:
  rows=[v for v in raw if v['variant']==variant and (v.get('button')==key or v.get('section')==key)]
  summary[variant][key]={metric:stats([v[metric] for v in rows]) for metric in ['ready_ms','close_ms','toggle_ms'] if rows and metric in rows[0]}
(Path(sys.argv[1]) if len(sys.argv)>1 else Q/'fenstervergleich.json').write_text(json.dumps({'method':'Same host/runtime, each sample in a NEW Python process (no shared imported helpers/resources), alternating source per round, first iteration warmup excluded, synthetic real Tk bindings, no profiler; ready after native bring_dialog_to_front, close Escape','sources':{v:hashlib.sha256((Q/'vorher/quelle/app.pyw' if v=='alt' else R/'src/glide/app.pyw').read_bytes()).hexdigest() for v in ['alt','neu']},'summary':summary,'raw':raw},indent=2))
print(json.dumps(summary))
