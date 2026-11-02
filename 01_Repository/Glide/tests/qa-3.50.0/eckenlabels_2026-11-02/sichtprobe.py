import sys,os,json,tempfile,subprocess,importlib.util,importlib.machinery
from pathlib import Path
repo=Path(sys.argv[1]).resolve();src=repo/'src/glide/app.pyw'
sys.path.insert(0,str(repo/'tests/integration'));sys.path.insert(0,str(src.parent))
out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
d=tempfile.mkdtemp(prefix='gtag-')
os.environ['GLIDE_DATA_DIR']=d;os.environ['GLIDE_TEST_MODE']='1'
loader=importlib.machinery.SourceFileLoader('glide_font_setup',str(src));m0=importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name,loader));sys.modules[loader.name]=m0;loader.exec_module(m0);m0.register_private_fonts()
from test_uiux_paket import Lauf
from test_arbeitsmodi import seite_anlegen
l=Lauf(src,d);a=l.app;res={'checks':[]}
def rect(w):return (w.winfo_rootx(),w.winfo_rooty(),w.winfo_rootx()+w.winfo_width(),w.winfo_rooty()+w.winfo_height())
def inter(r,s):return not (r[2]<=s[0] or s[2]<=r[0] or r[3]<=s[1] or s[3]<=r[1])
def cap(name):
    l.root.after(250,l.root.quit);l.root.mainloop();l.idle()
    subprocess.run(['/usr/sbin/screencapture','-x','-R'+','.join(map(str,(l.root.winfo_rootx(),l.root.winfo_rooty(),l.root.winfo_width(),l.root.winfo_height()))),str(out/(name+'.png'))],check=True)
def check(name,shot=False):
    l.idle();f=a.page_labels_frame;inner=a.list_frame_outer.inner
    c={'name':name,'placed':f.winfo_manager()=='place','chips':[w.chip_text for w in a.page_label_widgets]}
    if c['placed']:
        r=rect(f);ir=rect(inner);c['chip']=r
        c['inside']=r[0]>=ir[0] and r[2]<=ir[2] and r[1]>=ir[1]
        e=a.page_title_editor()
        if e is not None:
            t=rect(e.title_label);c['title']=t;c['overlap']=inter(r,t);c['dbg']=(e._corner_reserve,e._title_right_pad,e._read_pad,str(e.title_label.pack_info().get('padx')) if e.title_label.winfo_manager() else None)
            hr=getattr(e,'_head_row',None)
            if hr is not None and hr.winfo_ismapped():c['head_overlap']=inter(r,rect(hr))
        else:
            tv=a.tree
            kids=tv.get_children()
            if tv.winfo_ismapped() and kids:
                bb=tv.bbox(kids[0])
                if bb:
                    rr=(tv.winfo_rootx()+bb[0],tv.winfo_rooty()+bb[1],tv.winfo_rootx()+bb[0]+bb[2],tv.winfo_rooty()+bb[1]+bb[3]);c['row']=rr;c['overlap']=inter(r,rr)
            wsb=getattr(a.workspace,'bar',None)
            if wsb is not None and wsb.winfo_ismapped():c['bar_overlap']=inter(r,rect(wsb))
    res['checks'].append(c)
    if shot:cap(name)
labs=[{'id':'lab-text','name':'Text','color':'export'},{'id':'lab-k','name':'Kunde','color':'clear'},{'id':'lab-x','name':'Freigabe extern','color':'flag'},{'id':'lab-y','name':'Q4','color':'delete'}]
a.labels.extend(labs)
t=a.new_item('Unterlagen zur Freigabe prüfen');t['due']='2026-11-05';t['labels']=['lab-k'];t2=a.new_item('Angebot schicken')
folder=a.new_folder_object('Kundenordner',labels=['lab-text']);a.folders.append(folder)
listing=a.new_list_object('Projekt',[t,t2],folder_id=folder['id'],labels=['lab-text','lab-k']);a.lists.append(listing)
plain=a.new_list_object('Ohne Labels',[a.new_item('Eins')]);a.lists.append(plain);a.save_items()
page,e=seite_anlegen(l,'# Wochenplanung mit einem sehr langen Seitentitel, der bis in die Ecke reichen würde\n\nEin Absatz Fließtext, der bis an den rechten Rand reichen darf.\n\nZweiter Absatz')
page['labels']=['lab-text','lab-k','lab-x','lab-y']
for theme in ('light','dark'):
    a.set_design(theme)
    for w in (1280,860):
        l.root.geometry(f'{w}x800+20+20');l.idle()
        tag=f'{theme}-{w}'
        a.set_active_list(listing['id']);a.open_list_view();check('liste-'+tag,shot=True)
        a.set_table_view();check('tabelle-'+tag,shot=(w==1280 and theme=='light'))
        a.open_board_view();check('pinnwand-'+tag,shot=(w==1280 and theme=='light'))
        a.open_list_view()
        a.set_active_folder(folder['id']);check('ordner-'+tag,shot=(theme=='light'))
        a.set_active_list(plain['id']);check('ohne-'+tag)
        res['checks'][-1]['spacer']=a.page_labels_spacer.winfo_manager()
        a.set_active_list(page['id']);check('seite-'+tag,shot=True)
        for full in (True,False):
            a.settings['page_full_width']=full;a.set_active_list(listing['id']);a.set_active_list(page['id']);check(f'seite-voll{int(full)}-'+tag,shot=(full and theme=='light' and w==1280))
res['errors']=l.errors
bad=[c for c in res['checks'] if c.get('overlap') or c.get('head_overlap') or c.get('bar_overlap') or (c['placed'] and not c.get('inside'))]
res['bad']=bad
(out/'ergebnis.json').write_text(json.dumps(res,ensure_ascii=False,indent=1))
print(json.dumps({'n':len(res['checks']),'bad':[(b['name'],b.get('overlap'),b.get('inside')) for b in bad],'errors':l.errors,'unplaced':[c['name'] for c in res['checks'] if not c['placed']]},ensure_ascii=False))
l.ende()
