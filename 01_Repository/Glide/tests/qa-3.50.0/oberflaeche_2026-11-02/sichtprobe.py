import sys,json,tempfile,os,subprocess,importlib.util,importlib.machinery
from pathlib import Path
repo=Path(sys.argv[1]).resolve();src=repo/'src/glide/app.pyw';sys.path.insert(0,str(repo/'tests/integration'));sys.path.insert(0,str(src.parent))
from test_uiux_paket import Lauf
from test_arbeitsmodi import seite_anlegen,zeile_mit
out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True);result={'measurements':[],'glyphs':{}}
def capture(l,name):
 l.root.after(180,l.root.quit);l.root.mainloop();l.idle();a=l.app
 if a.view_mode=='list':a.show_quick_plan_row();l.idle()
 subprocess.run(['/usr/sbin/screencapture','-x','-R'+','.join(map(str,(l.root.winfo_rootx(),l.root.winfo_rooty(),l.root.winfo_width(),l.root.winfo_height()))),str(out/(name+'.png'))],check=True)
with tempfile.TemporaryDirectory(prefix='glide-five-matrix-') as d:
 os.environ['GLIDE_DATA_DIR']=d;os.environ['GLIDE_TEST_MODE']='1'
 loader=importlib.machinery.SourceFileLoader('glide_font_setup',str(src));mod=importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name,loader));sys.modules[loader.name]=mod;loader.exec_module(mod);mod.register_private_fonts()
 l=Lauf(src,d)
 try:
  a=l.app;result['runtime']=dict(python=sys.version.split()[0],tk=str(l.root.tk.call('package','provide','Tk')))
  for key in ('list','table','board','calendar','overdue','overflow'):
   f=l.mod.tkfont.Font(root=l.root,font=a.symbol_font(key,12));result['glyphs'][key]=dict(text=a.ICONS[key],font=f.actual('family'),actual=[str(l.root.tk.call('font','actual',f.name,'-family',c)) for c in a.ICONS[key]])
  task=a.new_item('Unterlagen zur Freigabe prüfen');listing=a.new_list_object('Projekt',[task]);a.lists.append(listing);a.save_items();a.set_active_list(listing['id']);l.idle();a.tree.selection_set(task['id']);a.tree.focus(task['id']);l.idle();capture(l,'liste-hell-1280')
  page,e=seite_anlegen(l,'# Wochenplanung\n\nQuellabsatz\n\nZielabsatz\n\nDanach')
  pid=page['id']
  for theme in ('light','dark'):
   a.set_design(theme);l.idle();assert a.design_name()==theme
   for size in ('mittel','gross'):
    a.settings['ui_font_size']=size;a.apply_ui_font();a.apply_theme()
    for w in (860,1280):
     l.root.geometry(f'{w}x800+20+20');l.idle()
     for full in (False,True):
      a.settings['page_full_width']=full;a.set_active_list(pid);l.idle();e=a.rich_note_editor;t=e.text;source=zeile_mit(t,'Quellabsatz');dest=zeile_mit(t,'Zielabsatz');e.show_block_handle(f'{source}.0');l.idle();h=e._block_handle;b=t.dlineinfo(f'{dest}.0');px=t.winfo_rootx()+b[0]+20;py=t.winfo_rooty()+b[1]+1
      h.event_generate('<ButtonPress-1>',x=3,y=3);h.event_generate('<B1-Motion>',x=px-h.winfo_rootx(),y=py-h.winfo_rooty(),rootx=px,rooty=py);l.idle();m=e._block_drop_marker;target=t.dlineinfo(str(e._block_drag['target']+1)+'.0');dx=m.winfo_rootx()-(t.winfo_rootx()+b[0]);dy=m.winfo_rooty()-(t.winfo_rooty()+target[1]);f=l.mod.tkfont.Font(root=l.root,font=e.title_label.cget('font'));result['measurements'].append(dict(theme=theme,font_size=size,width=w,full_width=full,dx=dx,dy=dy,title_size=f.actual('size'),main_title_size=a.header_title_font()[1]));assert abs(dx)<=1 and abs(dy)<=1
      if theme=='light' and size=='mittel' and w==1280 and not full:capture(l,'seite-hell-1280')
      if theme=='dark' and size=='gross' and w==860 and not full:capture(l,'seite-dunkel-860')
      e.cancel_block_drag()
  result['callback_errors']=l.errors;assert not l.errors
 finally:l.ende()
(out/'geometrie.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(dict(measurements=len(result['measurements']),runtime=result['runtime'],glyphs=result['glyphs'],errors=result['callback_errors']),ensure_ascii=False))
