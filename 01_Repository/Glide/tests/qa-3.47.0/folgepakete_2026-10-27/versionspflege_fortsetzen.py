"""Unterbrochene 3.46->3.47-Pflege fertigstellen; Showcase zunächst im Tempordner."""
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
ROOT=REPO.parents[1]
assert (REPO/'VERSION').read_text().strip()=='3.47.0'
os.environ['PYTHONUTF8']='1'


def module(name,path):
    loader=importlib.machinery.SourceFileLoader(name,str(path))
    mod=importlib.util.module_from_spec(importlib.util.spec_from_loader(name,loader))
    sys.modules[name]=mod
    loader.exec_module(mod)
    return mod


def run(name,args):
    result=subprocess.run([sys.executable,'-B',*map(str,args)],cwd=REPO,capture_output=True,
                          text=True,encoding='utf-8',timeout=900)
    (HERE/(name+'.log')).write_text(result.stdout+result.stderr,encoding='utf-8')
    if result.returncode:
        raise RuntimeError(name+': '+str(result.returncode)+'; siehe lokales Log')
    print(name+': grün',flush=True)
    return result.stdout


copy=module('glide_copy347',REPO/'scripts/pflege/showcase_abgleich.py').copy_atomic
with tempfile.TemporaryDirectory(prefix='glide-347-fixtures-') as folder:
    stage=Path(folder).resolve()
    assert stage.is_relative_to(Path(tempfile.gettempdir()).resolve())
    os.environ['GLIDE_DATA_DIR']=str(stage/'daten')
    run('showcase_temp',[REPO/'tests/tools/showcase.py','--ziel',stage/'showcase','--tag','2026-10-27'])
    for path in (stage/'showcase').iterdir():
        if path.is_file():
            copy(path,REPO/'tests/fixtures/showcase'/path.name)
    templates=module('glide_templates347',REPO/'tests/tools/vorlagendaten.py')
    app=module('glide_fixture347',REPO/'src/glide/app.pyw')
    payload=templates.build(app)
    target=stage/'vorlagen.glidetemplates'
    target.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    copy(target,templates.TARGET)
    print(str(len(payload['templates']))+' Vorlagen atomar übernommen',flush=True)
    run('releasedaten',[REPO/'tests/tools/releasedaten.py','--ziel',
                       REPO/'tests/fixtures/beispiele/glide_releaseplanung_3.47.0.glidebackup',
                       '--stichtag','2026-10-27'])

check=subprocess.run([sys.executable,'-B',str(REPO/'tests/tools/standpruefung.py')],
                     cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
paths={}
for line in check.stdout.splitlines():
    found=re.match(r'- (.+?\.md):(\d+): ',line)
    if found:
        paths.setdefault(found[1],set()).add(int(found[2]))
for filename,lines in paths.items():
    path=ROOT/filename
    values=path.read_text(encoding='utf-8').split('\n')
    for number in lines:
        values[number-1]=values[number-1].replace('3.46.0','3.47.0')
    temporary=path.with_name('.glide-347-stand-'+path.name)
    temporary.write_text('\n'.join(values),encoding='utf-8',newline='\n')
    os.replace(temporary,path)
pruning=run('aufbewahrung',[REPO/'scripts/pflege/ablage_kuerzen.py','--ohne-git-index'])
(HERE/'versionspflege.json').write_text(json.dumps(dict(version='3.47.0',
    resumed_after='Showcase-Zugriffsfehler',showcase_staged_outside_onedrive=True,
    templates=len(payload['templates']),updated_documents=len(paths),
    retention=pruning.strip().splitlines()[-1],git_index_changed=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Standpflege:',len(paths),'Dokumente;',pruning.strip().splitlines()[-1])
