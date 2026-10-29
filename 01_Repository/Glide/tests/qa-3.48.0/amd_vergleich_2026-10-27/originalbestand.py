"""Zusatzprobe mit der inzwischen vorgefundenen bytegleichen Intel-Eingangsdatei."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
QA = HERE.parent
OUTPUT = HERE / 'originalbestand'
OUTPUT.mkdir(exist_ok=True)
if (OUTPUT / 'ergebnis.json').exists():
    raise SystemExit('Vorhandenen Nachweis nicht ueberschreiben.')
main = json.loads((HERE / 'fester_pruefordner/ergebnis.json').read_text(encoding='utf-8'))
assert main['completed'] and all(row['passed'] for row in main['cases'])
frozen = Path(main['frozen_root'])
repo = frozen / '01_Repository/Glide'
original = QA / 'lokale_belege/eingang/initial.json'
proof = json.loads((QA / 'dreierpaket_2026-10-27/quellstand.json').read_text(encoding='utf-8'))
helper = QA / 'wa41_2026-10-27/pure_probe.py'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def integrity(base):
    return [name for name, expected in proof['sha256'].items()
            if not (base / name).is_file() or digest(base / name) != expected]


expected = 'a3b8c0cac4c72e1820e71730ad78e312f2a30338678fbcfe2a2b6d91dae081f4'
assert digest(original) == expected and original.stat().st_size == 28548872
payload = frozen.parent / 'initial_intel.json'
shutil.copy2(original, payload)
assert digest(payload) == expected
assert not integrity(frozen)
data_root = frozen.parent / 'testdaten'
env = dict(os.environ, PYTHONHASHSEED='0', PYTHONUTF8='1', PYTHONFAULTHANDLER='1',
           PYTHONDONTWRITEBYTECODE='1', TMP=str(data_root), TEMP=str(data_root))
for key in ('PYTHONMALLOC', 'PYTHONPYCACHEPREFIX', 'PYTHONPATH', 'PYTHONHOME'):
    env.pop(key, None)
report = dict(started=datetime.now(timezone.utc).isoformat(), source_files=470,
              frozen_before=integrity(frozen), source_before=integrity(ROOT),
              original_path=str(original), payload_path=str(payload),
              payload_sha256=expected, payload_bytes=payload.stat().st_size,
              input_byte_identical_to_intel=True, execution='sequential',
              runtime=main['runtime_info']['3147'], cases=[], completed=False,
              helper_sha256={p.name: digest(p) for p in (Path(__file__), helper)})


def save():
    (OUTPUT / 'ergebnis.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


save()
for name, bootstrap in [('original_pure', 'none'), ('original_import', 'import')]:
    assert not integrity(frozen) and digest(payload) == expected
    log_path = OUTPUT / f'{name}.stdout.log'
    command = [main['runtime_info']['3147']['executable'], '-B', '-u', '-X', 'faulthandler',
               str(helper), '--repo', str(repo), '--payload', str(payload),
               '--bootstrap', bootstrap, '--iterations', '20']
    print('START', name, flush=True)
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='glide-amd-original-', dir=data_root) as temporary:
        with log_path.open('wb') as log:
            process = subprocess.Popen(command, cwd=repo, env=dict(env, GLIDE_DATA_DIR=temporary, GLIDE_TEST_MODE='1'),
                                       stdout=log, stderr=subprocess.STDOUT)
            timed_out = False
            try:
                code = process.wait(timeout=300)
            except subprocess.TimeoutExpired:
                timed_out = True
                subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True, check=False)
                code = process.wait(timeout=30)
    raw = log_path.read_text(encoding='utf-8', errors='replace')
    rounds = len(re.findall(r'^round \d+ items 26420$', raw, re.M))
    row = dict(case=name, bootstrap=bootstrap, pid=process.pid, exitcode=code,
               seconds=round(time.monotonic() - started, 2), rounds_completed=rounds,
               timed_out=timed_out, frozen_after=integrity(frozen),
               payload_sha256_after=digest(payload), stdout_sha256=digest(log_path))
    row['passed'] = (code == 0 and not timed_out and rounds == 20 and not row['frozen_after']
                     and row['payload_sha256_after'] == expected and 'PASS pure 3.14.7 20' in raw)
    report['cases'].append(row)
    save()
    print('END', name, 'passed=', row['passed'], flush=True)
report.update(completed=True, finished=datetime.now(timezone.utc).isoformat(),
              frozen_after=integrity(frozen), source_after=integrity(ROOT),
              original_sha256_after=digest(original))
save()
raise SystemExit(not all(row['passed'] for row in report['cases']))
