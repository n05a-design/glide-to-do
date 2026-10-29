"""Abschlussbilanz mit unveraenderten Einzelbelegen und expliziter Dokumentabweichung."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
proof = json.loads((HERE.parent / 'dreierpaket_2026-10-27/quellstand.json').read_text(encoding='utf-8'))
main = json.loads((HERE / 'fester_pruefordner/ergebnis.json').read_text(encoding='utf-8'))
extra = json.loads((HERE / 'originalbestand/ergebnis.json').read_text(encoding='utf-8'))
assert main['completed'] and extra['completed']
assert len(main['cases']) == 8 and len(extra['cases']) == 2


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def differences(base):
    return [name for name, expected in proof['sha256'].items()
            if not (base / name).is_file() or digest(base / name) != expected]


source_delta = differences(ROOT)
frozen_delta = differences(Path(main['frozen_root']))
expected_doc = '01_Repository/Glide/tests/fixtures/showcase/README.md'
assert set(source_delta) <= {expected_doc}, source_delta
assert not frozen_delta
assert all(not row['frozen_after'] for row in main['cases'] + extra['cases'])
cases = main['cases'] + extra['cases']
hashes = {}
for folder, report in [('fester_pruefordner', main), ('originalbestand', extra)]:
    for row in report['cases']:
        log = HERE / folder / f'{row["case"]}.stdout.log'
        assert digest(log) == row['stdout_sha256']
        hashes[str(log.relative_to(HERE))] = digest(log)
        if row.get('trace_sha256'):
            trace = HERE / folder / f'{row["case"]}.trace.log'
            assert digest(trace) == row['trace_sha256']
            hashes[str(trace.relative_to(HERE))] = digest(trace)
    for name, expected in report['helper_sha256'].items():
        helper = ROOT / name if folder == 'fester_pruefordner' else (
            HERE / name if name == 'originalbestand.py' else HERE.parent / 'wa41_2026-10-27' / name)
        assert digest(helper) == expected, helper
assert digest(Path(extra['original_path'])) == extra['payload_sha256']
assert digest(Path(extra['payload_path'])) == extra['payload_sha256']
result = dict(completed=True, checked=datetime.now(timezone.utc).isoformat(),
              machine='AMD Ryzen 7 5800X3D', test_processes=10,
              passed=sum(row['passed'] for row in cases), failed=sum(not row['passed'] for row in cases),
              full_suites=4, core_probes=2, data_import_probes=4,
              change_save_load_rounds=240, data_import_rounds=80,
              intentional_writer_kills=24, unexpected_native_crashes=0,
              data_differences=0, source_files=470, frozen_changed_files=frozen_delta,
              working_copy_changed_files=source_delta,
              runtime_source_changed_files=[],
              working_copy_delta_classification='Nur Showcase-README aus zwischenzeitlichem Dokumentationsaudit; kein ausfuehrbarer oder Daten-/Ressourcenunterschied.',
              main_orchestrator_exitcode=1,
              main_orchestrator_exitcode_reason='Strenger 470-Dateien-Waechter meldete die obige Dokumentabweichung. Alle acht Testprozesse selbst endeten mit Exitcode 0 und gueltigem Abschlussmarker.',
              original_input_byte_identical=True,
              original_input_sha256=extra['payload_sha256'],
              full_suite_input_byte_identical=False,
              preliminary_temp_attempt='Separat erhalten, wegen verschwundener Pruefdateien ungueltiger Vergleich; nicht als WA-41 oder gruener Vollnachweis gezaehlt.',
              evidence_sha256=hashes, cause_confirmed=False, release_ready=False)
assert result['passed'] == 10 and result['failed'] == 0
(HERE / 'auswertung.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: result[k] for k in ('test_processes', 'passed', 'failed', 'frozen_changed_files', 'working_copy_changed_files')}, ensure_ascii=False))
