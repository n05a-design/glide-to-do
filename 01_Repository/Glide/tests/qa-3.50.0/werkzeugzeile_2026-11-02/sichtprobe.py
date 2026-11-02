import sys,os,json,tempfile,subprocess,importlib.util,importlib.machinery
from pathlib import Path
repo=Path(sys.argv[1]).resolve();src=Path(sys.argv[2]).resolve();out=Path(sys.argv[3]);out.mkdir(parents=True,exist_ok=True);tag=sys.argv[4]
sys.path.insert(0,str(repo/'tests/integration'));sys.path.insert(0,str(src.parent))
d=tempfile.mkdtemp(prefix='gabst-');os.environ['GLIDE_DATA_DIR']=d;os.environ['GLIDE_TEST_MODE']='1'
loader=importlib.machinery.SourceFileLoader('glide_font_setup',str(src));m0=importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name,loader));sys.modules[loader.name]=m0;loader.exec_module(m0);m0.register_private_fonts()
from test_uiux_paket import Lauf
from test_arbeitsmodi import seite_anlegen
l=Lauf(src,d);a=l.app
def cap(name):
    l.root.after(250,l.root.quit);l.root.mainloop();l.idle()
    subprocess.run(['/usr/sbin/screencapture','-x','-R'+','.join(map(str,(l.root.winfo_rootx(),l.root.winfo_rooty(),l.root.winfo_width(),l.root.winfo_height()))),str(out/f'{name}-{tag}.png')],check=True)
keys=[k for _l,k in a.mod.glide_appearance.BACKGROUND_CHOICES] if hasattr(a,'mod') else None
mod=l.mod
bgkeys=[k for _l,k in mod.glide_appearance.BACKGROUND_CHOICES]
a.set_design('dark');l.idle()
warm=[k for k in bgkeys if k not in ('default','surface')]
if warm: a.set_background_color(warm[-1]);l.idle()
pts=[mod.ListApp.new_item(a,'Unterlagen prüfen'),a.new_item('Angebot schicken'),a.new_item('Termin abstimmen')]
li=a.new_list_object('Projekt',pts);a.lists.append(li);a.save_items()
page,e=seite_anlegen(l)
res={'bg':a.settings.get('background_color')}
l.root.geometry('1280x800+20+20');l.idle(6)
def gap():
    sb=a.search_border if a.search_border.winfo_ismapped() else None
    lo=a.list_frame_outer
    r={}
    if sb is not None: r['suchfeld_unten_zu_karte']=lo.winfo_rooty()-(sb.winfo_rooty()+sb.winfo_height())
    sw=a.view_switch
    if sw.winfo_ismapped():
        rechts=[w for w in a.search_frame.pack_slaves() if w.winfo_ismapped() and w is not sw and w.winfo_rootx()>sw.winfo_rootx()]
        r['rechts_vom_umschalter']=[str(w) for w in rechts]
        r['umschalter_rechtskante']=sw.winfo_rootx()+sw.winfo_width()-(a.search_frame.winfo_rootx()+a.search_frame.winfo_width())
    return r
a.set_active_list(li['id']);a.open_list_view();l.idle();res['liste']=gap();cap('liste')
a.set_table_view();l.idle();res['tabelle']=gap();cap('tabelle')
a.open_board_view();a.workspace.pin([p['id'] for p in pts]);l.idle();res['pinnwand']=gap();res['pinnwand_grund']=(a.workspace.canvas.cget('bg'),a.theme['card'],a.theme['bg']);cap('pinnwand')
a.open_list_view();a.set_active_list(page['id']);l.idle()
tb=a.tool_band;res['seite_werkzeug_zu_karte']=a.list_frame_outer.winfo_rooty()-(tb.winfo_rooty()+tb.winfo_height()) if tb.winfo_ismapped() else None;cap('seite')
res['errors']=l.errors
print(json.dumps(res,ensure_ascii=False,indent=1));(out/f'messung-{tag}.json').write_text(json.dumps(res,ensure_ascii=False,indent=1))
l.ende()
