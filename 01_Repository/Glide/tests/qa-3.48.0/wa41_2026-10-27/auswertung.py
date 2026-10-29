"""Wertet vorhandene WA-41-Gegenproben aus; startet keine App oder Lastsuite."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
proof = json.loads((HERE.parent / 'dreierpaket_2026-10-27/quellstand.json').read_text(encoding='utf-8'))
rows = []
for name in ('matrix.json', 'matrix2.json', 'matrix3.json', 'matrix4.json', 'matrix5.json', 'matrix6.json'):
    for row in json.loads((HERE / name).read_text(encoding='utf-8-sig')):
        rows.append(dict(matrix=name, **row))
assert len(rows) == 24 and len({row['case'] for row in rows}) == 24
native_codes = {0xC0000005, 0xC0000409}
changed = [name for name, expected in proof['sha256'].items()
           if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected]
events = json.loads((HERE / 'native_events.json').read_text(encoding='utf-8-sig'))
result = dict(
    version='3.48.0', schema=26, cause_confirmed=False, release_ready=False,
    diagnostic_processes=len(rows),
    passed=sum(row['exitcode'] == 0 for row in rows),
    failed=sum(row['exitcode'] != 0 for row in rows),
    native_failures=sum(row['exitcode'] in native_codes for row in rows),
    python_failures=sum(row['exitcode'] != 0 and row['exitcode'] not in native_codes for row in rows),
    source_files_verified=len(proof['sha256']), changed_source_files=changed,
    cases=rows, native_events=events,
    limitations=[
        'Adaptive Gegenproben unterschiedlicher Umfaenge; keine statistische Ausfallrate.',
        'Kernprobe prueft Phasen 1/2; kein Ersatz fuer die originale Gesamtsuite.',
        'Nur ein gruener Python-3.15-Kernlauf; kein Freigabe- oder Reparaturnachweis.',
        'Importfehler einmal aufgetreten, Folgewiederholungen gruen; kein stabiler Minimalreproducer.',
        'Keine nativen Speicherabbilder oder symbolisierte Absturzstacks vorhanden.',
    ],
)
result['evidence_sha256'] = {
    file.name: hashlib.sha256(file.read_bytes()).hexdigest()
    for file in sorted(HERE.iterdir())
    if file.is_file() and file.suffix in ('.json', '.log', '.py', '.md')
    and file.name not in ('auswertung.json', 'payload_ort.log')
}
(HERE / 'auswertung.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({key: result[key] for key in (
    'diagnostic_processes', 'passed', 'failed', 'native_failures', 'python_failures',
    'source_files_verified', 'changed_source_files', 'cause_confirmed', 'release_ready')}, ensure_ascii=False))
raise SystemExit(bool(changed))
