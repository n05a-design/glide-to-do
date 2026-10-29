"""Prueft abgeschlossene Vergleichsbelege und extrahiert pfadfreie Absturzsignaturen."""
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
report = json.loads((HERE/'ergebnis.json').read_text(encoding='utf-8'))
assert report['completed'], 'Vergleich noch nicht abgeschlossen'
assert not any(report[key] for key in ('source_before','frozen_before','source_after','frozen_after'))
rows=[]
for case in report['cases']:
    output=HERE/f'{case["case"]}.stdout.log'
    assert hashlib.sha256(output.read_bytes()).hexdigest()==case['stdout_sha256']
    if 'trace_sha256' in case:
        trace=HERE/f'{case["case"]}.trace.log'
        assert hashlib.sha256(trace.read_bytes()).hexdigest()==case['trace_sha256']
    raw=output.read_text(encoding='utf-8',errors='replace')
    frames=[]
    for name,line,function in re.findall(r'File "([^"]+)", line (\d+) in ([^\r\n]+)',raw):
        frames.append(dict(file=Path(name).name,line=int(line),function=function))
    row=dict(case=case['case'],runtime=case['runtime'],kind=case['kind'],
             exitcode=case['exitcode'],seconds=case['seconds'],
             native_access_violation=case['exitcode']==0xC0000005,frames=frames)
    if frames:
        row['signature']=f'{case["exitcode"]:08x}|{frames[0]["file"]}:{frames[0]["line"]}:{frames[0]["function"]}'
    rows.append(row)
signatures={tag:{r['signature'] for r in rows if r['runtime']==tag and 'signature' in r} for tag in ('314','315')}
result=dict(completed=True,summary=report['summary'],cases=rows,
    common_fault_signatures=sorted(signatures['314'] & signatures['315']),
    wa41_reproduced_on_315=any(r['runtime']=='315' and r['native_access_violation'] for r in rows),
    production_files_unchanged=report['source_files'],frozen_files_unchanged=report['source_files'],
    errors=[],cause_confirmed=False,release_ready=False)
assert len(rows)==10 and sum(r['runtime']=='315' for r in rows)==8
(HERE/'auswertung.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='cases'},ensure_ascii=False))
