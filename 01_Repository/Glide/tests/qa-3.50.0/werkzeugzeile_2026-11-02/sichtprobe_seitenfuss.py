import sys,os,json,tempfile,subprocess,importlib.util,importlib.machinery
from pathlib import Path
repo=Path(sys.argv[1]).resolve();src=Path(sys.argv[2]).resolve();out=Path(sys.argv[3]);out.mkdir(parents=True,exist_ok=True);tag=sys.argv[4]
sys.path.insert(0,str(repo/'tests/integration'));sys.path.insert(0,str(src.parent))
d=tempfile.mkdtemp(prefix='gfuss-');os.environ['GLIDE_DATA_DIR']=d;os.environ['GLIDE_TEST_MODE']='1'
loader=importlib.machinery.SourceFileLoader('glide_font_setup',str(src));m0=importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name,loader));sys.modules[loader.name]=m0;loader.exec_module(m0);m0.register_private_fonts()
from test_uiux_paket import Lauf
from test_arbeitsmodi import seite_anlegen
l=Lauf(src,d);a=l.app
a.set_design('dark');l.idle()
page,e=seite_anlegen(l)
l.root.geometry('1280x800+20+20');l.idle(6)
e=a.rich_note_editor
e.status.configure(text='Schreibgeschützter Bestand');l.idle()
b=e._mentions_button;st=e.status
res={'knopf':(b.winfo_rootx(),b.winfo_rooty(),b.winfo_width(),b.winfo_height()),'status':(st.winfo_rootx(),st.winfo_rooty(),st.winfo_width(),st.winfo_height())}
res['eine_zeile']=abs((b.winfo_rooty()+b.winfo_height()/2)-(st.winfo_rooty()+st.winfo_height()/2))<=2 and st.winfo_rootx()>=b.winfo_rootx()+b.winfo_width()
l.root.after(250,l.root.quit);l.root.mainloop();l.idle()
x=e.winfo_rootx();y=b.winfo_rooty()-40
subprocess.run(['/usr/sbin/screencapture','-x','-R'+','.join(map(str,(x,y,900,90))),str(out/f'fuss-{tag}.png')],check=True)
print(json.dumps(res));l.ende()
