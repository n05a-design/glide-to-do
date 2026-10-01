"""Zusätzliche Startprobe der ausgelieferten Demo; ausschließlich temporäre Daten."""
import hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
repo=Path(__file__).resolve().parents[3]
base=repo.parents[1]
source=base/'05_Probelisten_Testdaten/Showcase'
checks=[]
with tempfile.TemporaryDirectory(prefix='launcher-',dir=Path(__file__).parent) as folder:
    target=Path(folder)
    for name in ['Showcase_starten.pyw','Glide-Showcase_App.glideapp']:
        shutil.copy2(source/name,target/name)
    launcher=target/'Showcase_starten.pyw'
    code="import runpy,sys,tkinter as tk; old=tk.Tk.mainloop; tk.Tk.mainloop=lambda self,*a,**k: (self.after(900,self.destroy),old(self,*a,**k))[1]; runpy.run_path(sys.argv[1],run_name='__main__')"
    env=dict(os.environ)
    env['GLIDE_QA_HINTERGRUND']='1'
    env['PYTHONPATH']=str(repo/'tests/tools/hintergrund')
    for first in [True,False]:
        run=subprocess.run([sys.executable,'-B','-c',code,str(launcher)],cwd=repo,env=env,capture_output=True,text=True,timeout=90)
        assert run.returncode==0,(run.stdout,run.stderr)
        datafile=target/'Arbeitsstand/liste_speicher.json'
        data=json.loads(datafile.read_text())
        assert len(data['lists'])==11
        note=next(e for e in data['lists'] if e['title']=='Abstimmung · Entwurf 02')
        if first:
            note['note']='Persistenzmarke ausschließlich im temporären Prüfdatenordner'
            datafile.write_text(json.dumps(data,ensure_ascii=False))
        else:
            assert note['note']=='Persistenzmarke ausschließlich im temporären Prüfdatenordner'
        checks.append({'erststart':first,'exitcode':run.returncode,'dokumente':len(data['lists'])})
    assert not (source/'Arbeitsstand').exists(), 'Die Probe darf den Arbeitsstand des Inhabers nicht anlegen.'
Path(__file__).with_suffix('.json').write_text(json.dumps({'starter_sha256':hashlib.sha256((source/'Showcase_starten.pyw').read_bytes()).hexdigest(),'runtime':'07_Python-Versionen','pruefungen':checks,'persoenliche_daten_unberuehrt':True},ensure_ascii=False,indent=2)+'\n')
print('Ausgelieferter Starter: Erststart, getrennter Datenpfad und Erhalt einer Bearbeitung beim zweiten Start: ok')
