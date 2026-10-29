"""Vorhandene WA-41-Belege lokal sichern, ohne neue Appausfuehrung.

Nur bekannte Minidumps und der bereits gehashte kuenstliche Anfangsbestand.
Originale bleiben erhalten; bestehende abweichende Ziele werden nie ersetzt.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
QA = HERE.parent
DEST = QA / 'lokale_belege'
DEST.mkdir(exist_ok=True)
ignore = DEST / '.gitignore'
expected_ignore = '*\n!.gitignore\n'
if ignore.exists():
    assert ignore.read_text(encoding='utf-8') == expected_ignore
else:
    ignore.write_text(expected_ignore, encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


sources = []
for row in json.loads((QA / 'last_fenster_2026-10-27/dump_bestand.json').read_text(encoding='utf-8')):
    source = Path(os.environ['LOCALAPPDATA']) / 'CrashDumps' / row['Name']
    sources.append((source, Path('minidumps') / row['Name'], row['SHA256']))
sources.append((Path(os.environ['TEMP']) / 'glide-wa41-payload-x1yjbvw8/initial.json',
    Path('eingang/initial.json'), 'a3b8c0cac4c72e1820e71730ad78e312f2a30338678fbcfe2a2b6d91dae081f4'))

result = dict(date='2026-10-27', application_tests_started=False, originals_unchanged=True,
    private_local_only=True, full_memory_dumps=0, files=[])
for source, relative, expected in sources:
    assert source.is_file(), str(source)
    assert digest(source) == expected, str(source)
    target = DEST / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        assert digest(target) == expected, str(target)
    else:
        shutil.copy2(source, target)
    assert digest(target) == expected
    result['files'].append(dict(path=target.relative_to(QA).as_posix(), bytes=target.stat().st_size,
        sha256=expected, source='%LOCALAPPDATA%/CrashDumps/' + source.name
        if relative.parts[0] == 'minidumps' else '%TEMP%/glide-wa41-payload-x1yjbvw8/initial.json'))
result['bytes'] = sum(r['bytes'] for r in result['files'])
(HERE / 'beweissicherung_lokal.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(files=len(result['files']), bytes=result['bytes'], originals_unchanged=True)))
