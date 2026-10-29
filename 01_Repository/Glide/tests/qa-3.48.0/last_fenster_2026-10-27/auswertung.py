"""Abgeschlossene Nachdiagnose auswerten, Belegbytes und unveraenderte Quelle pruefen."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
QA=HERE.parent
ROOT=HERE.parents[4]


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


scale=read(HERE/'ergebnis.json')
dev=read(QA/'entwicklermodus_2026-10-27/ergebnis.json')
capture=read(QA/'entwicklermodus_2026-10-27/exception_context.json')
affinity=read(QA/'affinitaet_2026-10-27/ergebnis.json')
assert scale['completed'] and dev['completed'] and affinity['completed'] and capture['completed']
assert len(scale['cases'])==9 and len(dev['cases'])==2 and len(affinity['cases'])==3
assert all(not data[key] for data in (scale,dev,affinity)
    for key in ('source_before','frozen_before','source_after','frozen_after'))
errors=[]
for folder,data in ((HERE,scale),(QA/'entwicklermodus_2026-10-27',dev),(QA/'affinitaet_2026-10-27',affinity)):
    for case in data['cases']:
        file=folder/f'{case["case"]}.stdout.log'
        if hashlib.sha256(file.read_bytes()).hexdigest()!=case['stdout_sha256']:
            errors.append('Log veraendert: '+case['case'])
app_cases=[r for r in scale['cases'] if r['list_count'] is not None]
generator=next(r for r in capture['frames'] if r['file']=='repeat_rules.py' and r['function']=='<genexpr>')
assert generator['matches_fresh_source'] and all(v['resolved_is_original'] for v in generator['bindings'].values())
for case in dev['cases']:
    for point in ('before','after'):
        context=case['context'][point]
        assert context['dev_mode'] and context['faulthandler']
        assert context['trace_hook'] is None and context['profile_hook'] is None
        assert not context['debugger_modules'] and not any(context['monitoring_tools'].values())
proof=read(QA/'dreierpaket_2026-10-27/quellstand.json')
changed=[name for name,expected in proof['sha256'].items()
    if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=expected]
result=dict(completed=True,source_files_verified=len(proof['sha256']),changed_source_files=changed,
    diagnostic_processes=15,
    scale_passed=sum(r['exitcode']==0 for r in app_cases),scale_total=len(app_cases),
    dev_failures=[r['fatal_messages'] for r in dev['cases']],
    exception_capture=capture['exception'],builtins_intact=True,code_matches_source=True,
    venv_full=dict(exitcode=scale['cases'][-1]['exitcode'],classification='PermissionError in Phase 3, kein WA-41-Nachweis',
        resource_counters='Nur Launcher erfasst; vom Appvergleich ausgeschlossen'),
    affinity=[{k:r[k] for k in ('case','affinity','exitcode','seconds')} for r in affinity['cases']],
    peak_private_mib=round(max(r['peaks']['private_bytes'] for r in app_cases)/2**20,1),
    peak_working_set_mib=round(max(r['peaks']['working_set_peak'] for r in app_cases)/2**20,1),
    minimum_available_gib=round(min(r['minimum_available_physical'] for r in app_cases)/2**30,1),
    peak_handles=max(r['peaks']['handles'] for r in app_cases),
    peak_gdi=max(r['peaks']['gdi_peak'] for r in app_cases),peak_user=max(r['peaks']['user_peak'] for r in app_cases),
    files_observed=max(e.get('files',0) for r in app_cases for e in r['trace_events']),
    scheduled_callbacks_observed=max(e.get('pending_callbacks',0) for r in app_cases for e in r['trace_events']),
    foreground_samples=sum(r['foreground_samples'] for r in app_cases),
    whea=read(HERE/'whea.json'),cpu_update_revision=read(HERE/'cpu_update_revision.json'),
    cause_confirmed=False,release_ready=False,errors=errors)
(HERE/'auswertung.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('whea','affinity','dev_failures')},ensure_ascii=False))
raise SystemExit(bool(errors or changed))
