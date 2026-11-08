import sys,os,json,tempfile,subprocess,importlib.util,importlib.machinery
from pathlib import Path
repo=Path(sys.argv[1]).resolve();src=Path(sys.argv[2]).resolve();out=Path(sys.argv[3]);out.mkdir(parents=True,exist_ok=True);tag=sys.argv[4]
sys.path.insert(0,str(repo/'tests/integration'));sys.path.insert(0,str(src.parent))
d=tempfile.mkdtemp(prefix='ghint-');os.environ['GLIDE_DATA_DIR']=d;os.environ['GLIDE_TEST_MODE']='1'
loader=importlib.machinery.SourceFileLoader('glide_font_setup',str(src));m0=importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name,loader));sys.modules[loader.name]=m0;loader.exec_module(m0);m0.register_private_fonts()
from test_uiux_paket import Lauf
l=Lauf(src,d);a=l.app
def cap(name):
    l.root.after(250,l.root.quit);l.root.mainloop();l.idle()
    subprocess.run(['/usr/sbin/screencapture','-x','-R'+','.join(map(str,(l.root.winfo_rootx(),l.root.winfo_rooty(),l.root.winfo_width(),l.root.winfo_height()))),str(out/f'{name}-{tag}.png')],check=True)
pts=[a.new_item('Unterlagen prüfen'),a.new_item('Angebot schicken'),a.new_item('Termin abstimmen')]
li=a.new_list_object('Projekt',pts);a.lists.append(li);a.save_items()
res={}
for hints in (False,True):
    a.settings['show_hints']=hints;a.apply_hint_setting()
    for w,h in ((860,700),(1280,800)):
        l.root.geometry(f'{w}x{h}+20+20');l.idle(6)
        a.set_active_list(li['id']);a.open_list_view();l.idle()
        if hints: cap(f'liste-{w}-hinweise')
        a.open_board_view();a.workspace.pin([p['id'] for p in pts]);l.idle()
        n=a.workspace.notice
        res[f'pinnwand-{w}-{hints}']=n.cget('text') if n.winfo_manager() else ''
        res[f'liste-fuss-{w}-{hints}']=None
        if not hints: cap(f'pinnwand-{w}')
        a.open_list_view();l.idle()
        res[f'liste-fuss-{w}-{hints}']=a.card_foot.winfo_manager() and a.hint_label.cget('text')
print(json.dumps(res,ensure_ascii=False,indent=1));l.ende()
