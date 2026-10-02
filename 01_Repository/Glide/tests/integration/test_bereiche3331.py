"""Vier Bereiche: echte Bindungen, Erstellen, Regeln, Undo, Einstellungen, Neustart."""
import importlib.machinery,importlib.util,json,os,tempfile
from pathlib import Path
from unittest.mock import patch
R=Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory(prefix='glide-bereiche-') as d:
 os.environ['GLIDE_DATA_DIR']=d;os.environ['GLIDE_TEST_MODE']='1'
 loader=importlib.machinery.SourceFileLoader('glide_bereiche',str(R/'src/glide/app.pyw'))
 mod=importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name,loader));loader.exec_module(mod)
 root=mod.tk.Tk();root.geometry('1280x900+20+20');errors=[];root.report_callback_exception=lambda *e:errors.append(str(e[1]));a=mod.ListApp(root)
 def idle():
  for _ in range(3):root.update()
 def descendants(w):
  result=[];stack=[w]
  while stack:
   w=stack.pop();result.append(w);stack.extend(w.winfo_children())
  return result
 def click(w):
  w.event_generate('<ButtonPress-1>',x=6,y=6);w.event_generate('<ButtonRelease-1>',x=6,y=6)
 def labels(menu):
  return [menu.entrycget(i,'label') for i in range(menu.index('end')+1) if menu.type(i) in ('command','cascade')]
 original_modal=a.run_modal
 def form_modal(dialog,parent=None):
  def submit():
   fields=[w for w in descendants(dialog) if isinstance(w,mod.tk.Entry)]
   assert fields;fields[-1].delete(0,'end');fields[-1].insert(0,'Testordner')
   button=next(w for w in descendants(dialog) if isinstance(w,mod.RoundedButton) and w.text=='Anlegen');click(button)
  dialog.after(100,submit);original_modal(dialog,parent)
 try:
  idle();inbox=next(e for e in a.lists if a.is_inbox_list(e))
  entries={kind:a.new_list_object('Beispiel '+kind,[],list_kind=kind) for kind in ('tasks','page','note','drawing','gallery')}
  a.lists.extend(entries.values());a.update_sidebar_list();idle()
  for kind,section in [('page','pages'),('note','notes'),('drawing','drawings'),('tasks','lists'),('gallery','lists')]:
   assert a.sidebar_section_for('list',entries[kind]['id'])==section
  assert len(a.sidebar_trees())==4
  # Folder creation uses the actual form and persists placement for empty ordinary folders.
  a.run_modal=form_modal
  folders={}
  for section in ('pages','notes','drawings','lists'):
   before={f['id'] for f in a.folders};a.create_container_dialog('folder',sidebar_section=section);idle()
   folder=next(f for f in a.folders if f['id'] not in before);folders[section]=folder
   assert folder['folder_kind']=='standard' and a.sidebar_section_for('folder',folder['id'])==section
  a.run_modal=original_modal
  # All accepted kinds in Lists; typed sections expose only their own kinds and allowed folders.
  for section,expected,forbidden in [('pages',['Neue Seite','Neuer Unterordner …'],['Neue Zeichnung','Neue Liste …','Neue Notiz …']),
                                    ('notes',['Neue Notiz …','Neuer Unterordner …'],['Neue Seite','Neue Zeichnung','Neue Liste …']),
                                    ('drawings',['Neue Zeichnung','Neuer Unterordner …'],['Neue Seite','Neue Liste …','Neue Notiz …']),
                                    ('lists',['Neue Seite','Neue Zeichnung','Neue Galerie','Neue Liste …','Neue Notiz …'],[])]:
   menu=a.folder_quick_add_menu(folders[section]['id']);names=labels(menu);assert all(x in names for x in expected),(section,names)
   assert not any(x in names for x in forbidden),(section,names);menu.destroy()
  with a.sidebar_change() as change:
   assert a.move_sidebar_list_into_folder(entries['drawing']['id'],folders['drawings']['id']);change.mark()
  assert not a.move_sidebar_list_into_folder(entries['page']['id'],folders['drawings']['id'])
  # A notebook in Notes keeps dated drawings (owner decision 01.10.2026); task lists stay a case for Lists.
  journal=a.new_folder_object('Notizbuch',folder_kind='journal');a.folders.append(journal);a.update_sidebar_list();idle()
  menu=a.folder_quick_add_menu(journal['id']);names=labels(menu);menu.destroy()
  assert names[0]=='Neue Tagesnotiz' and 'Neue Zeichnung' in names and 'Neue Liste …' not in names,names
  a.create_in_sidebar_section('drawing',journal['id'],'notes');idle();sketch=a.current_list()
  assert sketch['folder_id']==journal['id'] and sketch['journal']['moment_date'] and sketch['title'].startswith('Zeichnung · ')
  assert a.sidebar_section_for('folder',journal['id'])=='notes' and a.get_sidebar_tree_for_iid('list:'+sketch['id']) is a.notes_listbox
  loose=a.new_list_object('Lose Skizze',[],list_kind='drawing');a.lists.append(loose);a.update_sidebar_list();idle()
  src,dst=a.drawings_listbox,a.notes_listbox;siid,diid='list:'+loose['id'],'folder:'+journal['id'];src.see(siid);dst.see(diid);idle()
  x,y,w,h=src.bbox(siid);sx,sy=x+40,y+h//2;dx,dy,dw,dh=dst.bbox(diid);tx,ty=dst.winfo_rootx()+dx+40,dst.winfo_rooty()+dy+dh//2
  src.event_generate('<ButtonPress-1>',x=sx,y=sy,rootx=src.winfo_rootx()+sx,rooty=src.winfo_rooty()+sy)
  src.event_generate('<B1-Motion>',x=tx-src.winfo_rootx(),y=ty-src.winfo_rooty(),rootx=tx,rooty=ty)
  src.event_generate('<ButtonRelease-1>',x=tx-src.winfo_rootx(),y=ty-src.winfo_rooty(),rootx=tx,rooty=ty);idle()
  moved=next(e for e in a.lists if e['id']==loose['id'])
  assert moved['folder_id']==journal['id'] and moved['journal']['moment_date'] and a.sidebar_section_for('folder',journal['id'])=='notes'
  a.undo_last_change();idle();assert not next(e for e in a.lists if e['id']==loose['id']).get('folder_id')
  assert not a.move_sidebar_list_into_folder(loose['id'],folders['notes']['id'])
  assert not a.move_sidebar_list_into_folder(entries['tasks']['id'],journal['id'])
  assert a.sidebar_section_for('folder',journal['id'])=='notes'
  nested=a.new_folder_object('Unterordner',parent_id=folders['lists']['id']);a.folders.append(nested)
  mixed=a.new_list_object('Gemischt',[],folder_id=nested['id'],list_kind='tasks');a.lists.append(mixed)
  assert not a.can_move_folder_into(folders['lists']['id'],folders['pages']['id'])
  # Compatible root cross-section moves use real press/motion/release bindings on the heading.
  a.set_active_list(entries['page']['id']);idle();tree=a.pages_listbox;iid='list:'+entries['page']['id'];tree.see(iid);idle()
  x,y,w,h=tree.bbox(iid);sx,sy=x+40,y+h//2;target=a.sidebar_title_row
  tx,ty=target.winfo_rootx()+40,target.winfo_rooty()+target.winfo_height()//2
  tree.event_generate('<ButtonPress-1>',x=sx,y=sy,rootx=tree.winfo_rootx()+sx,rooty=tree.winfo_rooty()+sy)
  tree.event_generate('<B1-Motion>',x=tx-tree.winfo_rootx(),y=ty-tree.winfo_rooty(),rootx=tx,rooty=ty)
  tree.event_generate('<ButtonRelease-1>',x=tx-tree.winfo_rootx(),y=ty-tree.winfo_rooty(),rootx=tx,rooty=ty);idle()
  page_id=entries['page']['id'];assert a.sidebar_section_for('list',page_id)=='lists'
  a.undo_last_change();idle();assert a.sidebar_section_for('list',page_id)=='pages'
  a.locate_sidebar_root('list',page_id,'lists')
  with a.sidebar_change() as change:
   assert a.move_sidebar_list_into_folder(page_id,folders['pages']['id']);change.mark()
  a.set_active_list(page_id);idle();a.pages_listbox.selection_set('list:'+page_id)
  a.outdent_selected_sidebar_list();idle()
  assert a.sidebar_section_for('list',page_id)=='pages'
  assert a.get_sidebar_tree_for_iid('list:'+page_id) is a.pages_listbox
  a.undo_last_change();idle()
  assert next(e for e in a.lists if e['id']==page_id)['folder_id']==folders['pages']['id']
  # Every fold: actual pointer/keyboard, state across rebuilding, no orphan quick controls.
  a.set_drawings_view();idle();assert a.get_display_title()=='Zeichnungen'
  for section in ('pages','lists','notes','drawings'):
   arrow=getattr(a,'sidebar_heading_icon' if section=='lists' else section+'_heading_icon')
   click(arrow);idle();assert not a.sidebar_section_open(section)
   a.update_sidebar_list();idle();assert not a.sidebar_section_open(section)
   arrow.focus_set();arrow.event_generate('<Return>');idle();assert a.sidebar_section_open(section)
  # Settings are exercised through the real modal loop and the actual Save button.
  def settings_modal(dialog,parent=None):
   def submit():
    nodes=descendants(dialog)
    for section in ('pages','notes','drawings'):
     check=next(w for w in nodes if w.winfo_name()=='setting_sidebar_'+section);check.invoke()
    click(next(w for w in nodes if isinstance(w,mod.RoundedButton) and w.text=='Speichern'))
   dialog.after(100,submit);original_modal(dialog,parent)
  a.run_modal=settings_modal;click(a.settings_button);idle();a.run_modal=original_modal
  assert a.sidebar_section_visible('lists')
  for section in ('pages','notes','drawings'):
   assert not getattr(a,section+'_title_row').winfo_manager()
  assert all(a.get_sidebar_tree_for_iid('list:'+e['id']) is a.sidebar_listbox for e in a.lists if not a.is_inbox_list(e))
  saved=json.loads(Path(mod.SETTINGS_FILE).read_text());assert saved['sidebar_sections_visible']=={'pages':False,'lists':True,'notes':False,'drawings':False}
  a.settings['sidebar_sections_visible']={};a.save_settings();a.update_sidebar_list();idle()
  order=[str(w) for w in a.sidebar_frame.pack_slaves()]
  rows=[a.pages_title_row,a.sidebar_title_row,a.notes_title_row,a.drawings_title_row];assert [order.index(str(w)) for w in rows]==sorted(order.index(str(w)) for w in rows)
  # Heights and logo at small/large font and narrow window; theme changes keep logo aligned.
  for size in ['klein','mittel','gross']:
   a.settings['ui_font_size']=size;a._header_cap_font=None;a._header_subtitle_font=None;a.apply_ui_font();idle();a.sync_header_logo();idle()
   assert a.header_logo.winfo_rooty()>=a.title_label.winfo_rooty()+2
   assert a.header_logo.winfo_height()==a.header_logo_height()
  root.geometry('860x700');idle()
  assert a.drawings_title_row.winfo_rooty()+a.drawings_title_row.winfo_height() <= a.sidebar_frame.winfo_rooty()+a.sidebar_frame.winfo_height()+2
  # Unchanged logo geometry must not re-enter Tk's pack layout on every refresh.
  a.sync_header_logo();idle()
  with patch.object(a.header_logo,'pack_configure',wraps=a.header_logo.pack_configure) as repack:
   for _ in range(5):a.sync_header_logo()
   assert repack.call_count==0
  # Explicit non-library ordinary folders retain locations across load/restart settings.
  a.save_items();locations=dict(a.settings['sidebar_locations']);a.load_items();a.settings=a.load_settings();a.update_sidebar_list();idle()
  assert a.settings['sidebar_locations']==locations
  assert a.sidebar_section_for('folder',folders['drawings']['id'])=='drawings'
  assert not errors,errors
  print('Vier Bereiche, Formular/Menüs, Inhaltsgrenzen, Drag/Undo, Klappen, Settings, Logo, Reload: ok')
 finally:root.destroy()
