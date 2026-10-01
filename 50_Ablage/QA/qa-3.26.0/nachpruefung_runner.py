from pathlib import Path
import subprocess, sys, os, json, time
sys.path.insert(0,str(Path('tests/tools').resolve()))
import pruefen
out=Path('tests/qa-3.26.0/nachbesserung_2026-09-20');out.mkdir(exist_ok=True,parents=True)
results=[]
for name in pruefen.SUITEN:
 if name == 'test_vollpruefung325.py':continue
 started=time.monotonic()
 try:
  result=subprocess.run([sys.executable,str(Path('tests/integration')/name)],capture_output=True,timeout=150,env={**os.environ,'PYTHONIOENCODING':'utf-8','PYTHONDONTWRITEBYTECODE':'1'})
  output=result.stdout+result.stderr;code=result.returncode
 except subprocess.TimeoutExpired as error:
  output=(error.stdout or b'')+(error.stderr or b'');code='timeout'
 (out/(name+'.log')).write_bytes(output)
 results.append({'suite':name,'exitcode':code,'seconds':round(time.monotonic()-started,2)})
 (out/'zwischenstand.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
 print(name,code,flush=True)
