import os,sys,tempfile,json
from pathlib import Path
r=Path(__file__).resolve().parents[3];sys.path.insert(0,str(r/'tests/tools'));from rundgang import load_module,ruhe
with tempfile.TemporaryDirectory(prefix='glide-showcase-area-') as d:
 m=load_module(Path(d));root=m.tk.Tk();root.geometry('1400x960+20+20');a=m.ListApp(root)
 a.show_info=lambda *args,**kw:None
 assert a.restore_app_backup(path=str(r/'tests/fixtures/showcase/Glide-Showcase_App.glideapp'),sections={name:True for name in a.APP_BACKUP_SECTIONS},show_success=False)
 ruhe(root)
 for kind,values in [('folder',a.folders),('list',a.lists)]:
  for value in values:
   if value.get('archived') or a.is_inbox_list(value):continue
   print(kind,value['title'],a.sidebar_section_for(kind,value['id']),'parent',value.get('folder_id',value.get('parent_id')),'exists',[(a.sidebar_section_for_tree(t),t.parent(kind+':'+value['id'])) for t in a.sidebar_trees() if t.exists(kind+':'+value['id'])],flush=True)
 root.destroy()
