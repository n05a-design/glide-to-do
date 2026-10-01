"""Einmalige, ausdrücklich beauftragte Bereinigung von Markdown-Versionskopien."""
from pathlib import Path
import re, os, json, hashlib, collections
R=Path(__file__).resolve().parents[3]; B=R.parents[1]; Q=Path(__file__).resolve().parent
roots=[B/x for x in ('00_Arbeitsvorbereitung','01_Repository/Glide/docs','01_Repository/Glide/archiv','20_Grafik_Master','40_Store_Material','90_Testdaten_Extern','05_Probelisten_Testdaten','07_Python-Versionen/Archiv','01_Repository/Glide/assets','01_Repository/Glide/packaging','01_Repository/Glide/src/glide','01_Repository/Glide/tests/archiv','01_Repository/Glide/tests/fixtures/archiv','01_Repository/Glide/tests/tools/archiv')]
files=sorted(set(p for root in roots if root.exists() for p in root.rglob('*.md') if not any(x in p.parts for x in ('vorher','vendor','qa-3.33.1'))))
archived=lambda p:any(part.lower()=='archiv' for part in p.relative_to(B).parts)
active=[p for p in files if not archived(p)]
# README files next to an archived directory are the canonical source too.
for root in roots:
 if root.name.lower()=='archiv' and (root.parent/'README.md').is_file():active.append(root.parent/'README.md')
canonical=active+[p for p in files if archived(p) and '_vor_' not in p.stem and not p.name.startswith('README_')]
def normalized(name):return re.sub(r'_\d+\.\d+(?:\.\d+)?(?=_|$)','',name)
def distance(a,p):return len(a.parts)+len(p.parts)-2*len(Path(os.path.commonpath((a,p))).parts)
rows=[]
for p in files:
 if not archived(p) or '_vor_' not in p.stem:continue
 prefix=p.stem.split('_vor_')[0]
 matches=[a for a in canonical if p.stem.startswith(a.stem+'_') or normalized(a.stem)==normalized(prefix)]
 if not matches:continue
 a=min(matches,key=lambda a:(distance(a.parent,p.parent),-len(a.stem),archived(a)))
 rows.append((p,a,'Überholte Versionskopie; gepflegte Quelle bzw. einzelner fachlicher Vertrag bleibt'))
# Exact duplicate proposal; source stays. Obsolete marked checklists are superseded.
a=B/'00_Arbeitsvorbereitung/Archiv/Glide_KI_Austauschformat_Vorschlag_2026-09-16.md'
p=B/'00_Arbeitsvorbereitung/Archiv/Glide_KI_Austauschformat_und_Zukunftsarchitektur_Dublette_2026-09-18.md'
if p.exists() and a.exists() and p.read_bytes()==a.read_bytes():rows.append((p,a,'Bytegleiche Dublette'))
for name in ('Manuelle_Pruefung_3.28.0_Z.md','Manuelle_Pruefung_3.29.0_Z.md'):
 p=B/'00_Arbeitsvorbereitung/Checklisten/Archiv'/name
 if p.exists():rows.append((p,B/'00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.30.0.md','Bereits als überholt markiert; aktuelle fortgeschriebene Prüfliste ersetzt diese'))
rows=list({p:(p,a,why) for p,a,why in rows}.values())
deleted={p.resolve():a.resolve() for p,a,_why in rows}
assert not any(a in deleted for a in deleted.values()),'Canonical destination must survive'
manifest={'authorization':'Nutzerauftrag 01.10.2026: doppelte und überholte Dokumente löschen; Wissen zusammenfassen','deleted':[{'path':str(p.relative_to(B)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'canonical':str(a.relative_to(B)),'reason':why} for p,a,why in rows]}
manifest['count']=len(rows);manifest['bytes']=sum(x['bytes'] for x in manifest['deleted'])
Q.joinpath('archiv_bereinigung.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
# Rewrite existing file links throughout current project documentation; delete obsolete index rows.
links=re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
changed=[]
for path in B.rglob('*.md'):
 if any(part in ('.git','vendor','build','vorher') or part.startswith('qa-') for part in path.relative_to(B).parts) or path.resolve() in deleted:continue
 original=path.read_text(encoding='utf-8-sig');text=original
 if path==R/'docs/00_INDEX.md':
  text='\n'.join(line for line in text.split('\n') if not any(str(p.relative_to(R/'docs')) in line for p,_a,_w in rows if p.is_relative_to(R/'docs')))
 def replace(match):
  label,target=match.groups();clean=target.strip().strip('<>')
  if ':' in clean or clean.startswith('#'):return match.group(0)
  base,_,anchor=clean.partition('#');dest=(path.parent/base).resolve()
  if dest not in deleted:return match.group(0)
  new=os.path.relpath(deleted[dest],path.parent)
  # Old section anchors belong to snapshots; canonical entry is sufficient.
  return f'[{label}]({new})'
 text=links.sub(replace,text)
 if text!=original:path.write_text(text);changed.append(str(path.relative_to(B)))
for p,a,why in rows:p.unlink()
# Empty archive directories only; never remove files of other kinds.
for root in roots:
 if root.exists():
  for directory in sorted((p for p in root.rglob('*') if p.is_dir()),key=lambda p:len(p.parts),reverse=True):
   if archived(directory):
    try:directory.rmdir()
    except OSError:pass
manifest['updated_link_documents']=changed
Q.joinpath('archiv_bereinigung.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(json.dumps({'deleted':len(rows),'bytes':manifest['bytes'],'changed_links':len(changed),'folders':dict(collections.Counter(str(p.parent.relative_to(B)) for p,_a,_w in rows))},ensure_ascii=False))
