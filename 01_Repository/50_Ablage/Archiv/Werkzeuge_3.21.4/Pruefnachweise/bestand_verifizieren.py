from pathlib import Path
import json,hashlib,importlib.util,difflib
R=Path.cwd();B=Path(__file__).parent
S=json.loads((B/'ausgangsbestand.json').read_text());checks=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for rel,info in S.items():
 p=R/rel
 if p.exists() and sha(p)==info['sha256']:continue
 folder=next((x for x in p.parent.iterdir() if x.is_dir() and x.name.lower()=='archiv'),None) if p.parent.exists() else None
 candidates=[] if folder is None else [x for x in folder.iterdir() if x.is_file() and x.stat().st_size==info['bytes']]
 if rel.startswith('Claude outputs/'):candidates=[R/'50_Ablage/Archiv/Uebertragungspakete'/p.name]
 hits=[x.relative_to(R).as_posix() for x in candidates if x.exists() and sha(x)==info['sha256']]
 assert hits,'Original nicht archiviert: '+rel
 checks.append({'vorher':rel,'sha256_vorher':info['sha256'],'archiv':hits,'gesichert':True})
(B/'archivpruefung.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
q=R/'50_Ablage/Archiv/Werkzeuge_3.21.4/quellstand';s=importlib.util.spec_from_file_location('a',q.parent/'ablegen_3214.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
items=[];expected={'standpruefung.py','pruefen.py'}
for source,rel in m.ZIELE:
 p=R/'01_Repository/Glide'/rel;equal=sha(q/source)==sha(p)
 assert equal or source in expected,rel
 items.append({'paket':source,'ziel':p.relative_to(R).as_posix(),'paketidentisch':equal})
 if not equal:
  diff=''.join(difflib.unified_diff((q/source).read_text().splitlines(True),p.read_text().splitlines(True),fromfile='Paket/'+source,tofile=rel))
  (B/(source+'.diff')).write_text(diff)
assert {x['paket'] for x in items if not x['paketidentisch']}==expected
(B/'paketabgleich.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
assert (R/'01_Repository/Glide/src/glide/app.pyw').read_bytes()==(B/'vorher/01_Repository/Glide/src/glide/app.pyw').read_bytes().replace(b'APP_VERSION = "3.21.3"',b'APP_VERSION = "3.21.4"',1)
print(f'{len(checks)} Ausgangsdateien unverändert archiviert; 15 Paketziele geprüft, ausschließlich zwei dokumentierte Werkzeugkorrekturen.')
