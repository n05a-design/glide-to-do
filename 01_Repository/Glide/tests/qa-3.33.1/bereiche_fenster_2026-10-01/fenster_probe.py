import os,sys,tempfile,importlib.machinery,importlib.util,time,json,cProfile,pstats,io,zipfile
from pathlib import Path
r=Path(__file__).resolve().parents[3]; out=Path(sys.argv[1]); src=Path(sys.argv[2]) if len(sys.argv)>2 else r/'src/glide/app.pyw'
with tempfile.TemporaryDirectory(prefix='glide-window-probe-') as d:
 os.environ['GLIDE_DATA_DIR']=d;os.environ['GLIDE_TEST_MODE']='1'
 with zipfile.ZipFile(r/'tests/fixtures/beispiele/glide_beispieldaten.glidebackup') as z:Path(d,'liste_speicher.json').write_bytes(z.read('data.json'))
 loader=importlib.machinery.SourceFileLoader('glide_probe',str(src));m=importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name,loader));loader.exec_module(m)
 root=m.tk.Tk();root.geometry('1400x950+20+20');errors=[];root.report_callback_exception=lambda *e:errors.append(str(e[1]));a=m.ListApp(root)
 a.show_info=a.show_warning=a.show_error=lambda *args,**kw:errors.append(str(args))
 for _ in range(3):root.update()
 a.set_active_list(max(a.lists,key=lambda e:a.count_items(e.get('items',[])))['id']);a.open_board_view()
 for _ in range(3):root.update()
 values=[];original=a.run_modal
 def modal(dialog,parent=None):
  mapped=[]
  def onmap(e):
   if e.widget is dialog and not mapped:mapped.append(time.perf_counter())
  dialog.bind('<Map>',onmap,add='+')
  def close():
   dialog.focus_set();t=time.perf_counter();dialog.event_generate('<Escape>');values[-1]['close_ms']=(time.perf_counter()-t)*1000
   if dialog.winfo_exists():errors.append('Escape failed '+dialog.title());dialog.destroy()
  dialog.after(150,close);original(dialog,parent);values[-1]['map_ms']=(mapped[0]-start)*1000 if mapped else None
 a.run_modal=modal
 profile=cProfile.Profile();profile.enable()
 for name in ['show_actions_dialog','show_settings_dialog','show_shortcuts_dialog','show_about_dialog','show_print_dialog','show_history_dialog']:
  start=time.perf_counter();values.append({'action':name});getattr(a,name)();values[-1]['total_ms']=(time.perf_counter()-start)*1000
  root.update()
 profile.disable();s=io.StringIO();pstats.Stats(profile,stream=s).sort_stats('cumulative').print_stats(35);out.with_suffix('.profile.txt').write_text(s.getvalue())
 out.write_text(json.dumps({'measurements':values,'errors':errors},indent=2));print(json.dumps(values));root.destroy();assert not errors,errors
