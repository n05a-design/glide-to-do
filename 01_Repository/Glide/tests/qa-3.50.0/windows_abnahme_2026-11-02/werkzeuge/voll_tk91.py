"""Eingefrorener Windows-Volllauf mit eigener Tk 9.1 und nativer Zugangsprüfung.

Muster: 13_TK-Test-Umgebung/Macbook-M2/voll_tk91.py bzw. gesichert_pruefen.py.
Aufruf: python -B voll_tk91.py <Repo 01_Repository/Glide> <Laufordner> <python-extension>
Schreibt <Laufordner>/lauf.json (Pfade der eingefrorenen Kopie) und abschluss.json im Nachweisordner.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
ablage = Path(sys.argv[2]).resolve()
erweiterung = sys.argv[3]
sys.path.insert(0, str(repo / 'tests/tools'))
from pruefablauf import Pruefablauf, einfrieren  # noqa: E402

ablage.mkdir(parents=True, exist_ok=True)
frozen, root = einfrieren(repo, ablage)
guard = Pruefablauf(frozen, ablage)
(ablage / 'lauf.json').write_text(json.dumps({
    'eingefroren': str(frozen), 'nachweise': str(root), 'waechter': str(guard.root)},
    ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
command = [sys.executable, '-B', str(frozen / 'tests/tools/pruefen.py'), '--modus', 'voll', '--zugang-nativ',
           '--protokoll', str(root / 'protokoll'), '--timeout', '900', '--arbeitsablage', str(guard.root.parent)]
env = dict(os.environ, PYTHONPATH=erweiterung)
print(f'Eingefrorene Prüfkopie: {frozen}\nNachweise: {root}\nProzesswächter: {guard.root}', flush=True)
try:
    result = guard.command('voll', command, timeout=900 * 200, environment=env, cwd=frozen)
except (OSError, subprocess.TimeoutExpired):
    result = None
code = result.returncode if result is not None and not guard.stopped else 1
(root / 'abschluss.json').write_text(json.dumps({
    'exitcode': code, 'art': 'voll', 'tk': '9.1', 'zugang_nativ': True, 'plattform': 'windows-x64',
    'pruefablauf': str(guard.root / 'pruefablauf.json'), 'release_ready': False},
    ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Exitcode {code}', flush=True)
sys.exit(code)
