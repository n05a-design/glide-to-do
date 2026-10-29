"""Begrenzte Ursachenprobe: Originalfall gegen sauberen Test-Sitzungsabschluss.

Keine Quelldatei oder Testassertion wird geändert. Der rote Originalbefund
bleibt bestehen; der zweite Fall ist ausschließlich eine Diagnosevariation.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
import traceback

OUT = Path(__file__).resolve().parent
original = json.loads((OUT / 'eingefroren.json').read_text(encoding='utf-8'))
base = Path(original['copy'].replace('%USERPROFILE%', str(Path.home())))
repo = base / 'projekt/01_Repository/Glide'
sys.path.insert(0, str(repo / 'tests/integration'))
import test_wiederholen as suite


def main():
    rows = []
    for clean in (False, True):
        with tempfile.TemporaryDirectory(prefix='diagnose-gueltigkeit-', dir=base) as folder:
            lauf = suite.Lauf(repo / 'src/glide/app.pyw', folder)
            row = {'clean_teardown_in_memory': clean, 'observations': []}
            close = lauf.ende
            if clean:
                def clean_close():
                    lauf.app.finish_recovery_session()
                    close()
                lauf.ende = clean_close
            restart = lauf.neustart
            def observe_restart():
                row['observations'].append({'step': 'before_restart',
                    'readonly': bool(getattr(lauf.app, '_data_read_only', False))})
                restart()
                result = getattr(lauf.app, '_recovery_assessment', None)
                row['observations'].append({'step': 'after_restart',
                    'readonly': bool(getattr(lauf.app, '_data_read_only', False)),
                    'reason': getattr(lauf.app, '_read_only_reason', None),
                    'assessment': getattr(result, 'kind', None)})
            lauf.neustart = observe_restart
            try:
                row['result'] = suite.fall_gueltigkeit(lauf)
                row['passed'] = True
            except Exception:
                row['passed'] = False
                row['traceback'] = traceback.format_exc().replace(str(Path.home()), '%USERPROFILE%')
                row['readonly'] = bool(getattr(lauf.app, '_data_read_only', False))
                row['reason'] = getattr(lauf.app, '_read_only_reason', None)
            finally:
                lauf.ende()
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    current = hashlib.sha256((repo / 'src/glide/app.pyw').read_bytes()).hexdigest()
    assert current == original['app_sha256']
    (OUT / 'diagnose_wiederholen.json').write_text(json.dumps({
        'app_sha256': current, 'original_suite_unchanged': True,
        'assertions_unchanged': True, 'diagnosis_only': True, 'cases': rows},
        ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
