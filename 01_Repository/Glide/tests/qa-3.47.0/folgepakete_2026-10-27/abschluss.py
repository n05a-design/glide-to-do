"""Dokumentregister, eingefrorene Quelle, gezielte Nachläufe und Lieferung prüfen."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
ROOT=REPO.parents[1]
sys.path.insert(0,str(REPO/'tests/tools'))
import standpruefung as stand


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name): return json.loads((HERE/name).read_text(encoding='utf-8'))


result={'version':'3.47.0','schema':26,'errors':[],'full_104_suite_run':False,
        'native_packages':'3.45.0','links_checked':0,'anchors_checked':0}
(HERE/'abschluss.json').write_text('{}\n',encoding='utf-8')
frozen=read('quellstand.json')
for name,expected in frozen['runtime'].items():
    if sha(REPO/'src/glide'/name)!=expected:result['errors'].append('Quelltext geändert: '+name)
test_changes=[name for name,expected in frozen['tests'].items() if sha(REPO/name)!=expected]
result['test_changes_after_freeze']=test_changes
if test_changes!=['tests/integration/test_arbeitsmodi.py']:
    result['errors'].append('Unerwartete Prüfcodeänderung nach Einfrieren')
result['source_files']=len(frozen['runtime'])
result['prototype_not_delivered']='drawing_prototype.pyw'
delivery=ROOT/'07_Python-Versionen'
result['delivery_differences']=[]
for name,expected in frozen['runtime'].items():
    if name=='drawing_prototype.pyw':continue
    target=delivery/({'app.pyw':'Glide-Aufgaben-und-Listen_v3.47.0.pyw','glide_start.py':'Schnellstart.pyw'}.get(name,name))
    if not target.exists() or sha(target)!=expected:result['delivery_differences'].append(name)
for name,expected in frozen['resources'].items():
    if sha(REPO/'src/glide'/name)!=expected or sha(delivery/name)!=expected:
        result['delivery_differences'].append(name)
result['runtime_files']=len(frozen['runtime'])-1
result['resource_files']=len(frozen['resources'])
if result['delivery_differences']:result['errors'].append('Python-Lieferstand weicht ab')
work=read('arbeitsmodi_eingefroren.json')
follow=read('nebenansicht_nachlauf.json')
if work['fehler']!=['nebenansicht_liste']:result['errors'].append('Ungeklärte eingefrorene Arbeitsmodifälle')
cases={**work['faelle'],**follow['faelle']}
result['focused_cases']={'total':len(cases),'failed':[name for name,value in cases.items() if not value['ok']],
                         'retained_original_failure':work['fehler']}
if len(cases)!=22 or result['focused_cases']['failed']:result['errors'].append('Gezielte Fälle unvollständig')
probe=read('python_lieferprobe.json')
if probe['fehler'] or len(probe['faelle'])!=2:result['errors'].append('Python-Lieferprobe nicht grün')
for report in (work,follow,probe):
    if report['app_sha256']!=frozen['runtime']['app.pyw']:result['errors'].append('Prüfung an anderer Appquelle')
result['geometry']=cases['folgepaket_gestaltung']['befund']
result['showcase_sha256']={}
for name in ('Glide-Showcase.glidebackup','Glide-Showcase_App.glideapp','Glide-Showcase.glidetemplates',
             'manifest.json','Showcase_starten.pyw','README.md'):
    source=REPO/'tests/fixtures/showcase'/name
    result['showcase_sha256'][name]=sha(source)
    if sha(ROOT/'05_Probelisten_Testdaten/Showcase'/name)!=sha(source):
        result['errors'].append('Showcase-Lieferung weicht ab: '+name)
ci=read('ci_streng/ergebnis.json')
result['ci']={'exitcode':ci['exitcode'],'steps':len(ci['schritte']),
              'passed':sum(value['status']=='ausgeführt' for value in ci['schritte'])}
if ci['exitcode']:result['errors'].append('CI-Grundstufe nicht grün')


def headings(path):
    text=re.sub(r'```.*?```','',path.read_text(encoding='utf-8-sig'),flags=re.S)
    values,counts=set(),{}
    for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*$',text,flags=re.M):
        slug=re.sub(r'[^\w\- ]','',title.lower()).replace(' ','-')
        number=counts.get(slug,0);counts[slug]=number+1
        values.add(slug+(f'-{number}' if number else ''))
    values.update(re.findall(r'<a\s+(?:name|id)=["\']([^"\']+)',text))
    return values


documents=list(stand.dokumente(ROOT))
checked=stand.lauf([ROOT],'3.47.0')
result['document_register']={'total':len(documents),'current':checked.fortgeschrieben,
    'frozen':checked.festgeschrieben,'without_status':checked.ohne_stand,
    'files':[path.relative_to(ROOT).as_posix() for path in documents]}
result['errors'].extend(checked.fehler)
documents=[path for path in documents if not any(part.startswith('qa-') for part in path.parts)]
documents.append(HERE/'README.md')
for path in documents:
    content=re.sub(r'```.*?```','',path.read_text(encoding='utf-8-sig'),flags=re.S)
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',content):
        target=target.strip().strip('<>').split(' "',1)[0]
        if not target or urlsplit(target).scheme:continue
        filename,_,anchor=unquote(target).partition('#')
        destination=(path.parent/filename).resolve() if filename else path
        result['links_checked']+=1
        if not destination.exists():result['errors'].append(f'{path.relative_to(ROOT)}: fehlendes Ziel {target}')
        elif anchor and destination.suffix=='.md':
            result['anchors_checked']+=1
            if anchor not in headings(destination):result['errors'].append(f'{path.relative_to(ROOT)}: fehlender Anker {target}')
for args in (['git','diff','--check'],['git','diff','--cached','--check']):
    check=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
    if check.returncode:result['errors'].append(check.stdout+check.stderr)
result['ok']=not result['errors']
(HERE/'abschluss.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({key:value for key,value in result.items() if key!='document_register'},ensure_ascii=False,indent=2))
print('Dokumentregister:',len(result['document_register']['files']))
raise SystemExit(int(not result['ok']))
