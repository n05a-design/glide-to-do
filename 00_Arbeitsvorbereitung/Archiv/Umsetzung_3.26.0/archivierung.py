"""Reversible Archivierung mit Linknachführung und Manifest."""
from pathlib import Path
import json
import os
import re
import shutil
from urllib.parse import unquote

root = Path(__file__).resolve().parents[2]
repo = root / '01_Repository/Glide'
docs = repo/'docs'
moves = {}
for path in docs.glob('*.md'):
    version = re.search(r'3\.(\d+)\.\d+', path.stem)
    if version and int(version[1]) < 21:
        moves[path.resolve()] = (docs/'archiv'/path.name).resolve()
for path in (repo/'tests').glob('qa-*'):
    version = re.search(r'3\.(\d+)\.\d+', path.name)
    if path.is_dir() and version and int(version[1]) <= 23:
        moves[path.resolve()] = (root/'50_Ablage/QA'/path.name).resolve()

for old, new in moves.items():
    old.relative_to(root); new.relative_to(root)
    assert old != root and new != root and not new.exists(), (old, new)

def translated(path):
    for old, new in moves.items():
        try:
            return new/path.relative_to(old)
        except ValueError:
            pass
    return path

pattern = re.compile(r'(\[[^\]\n]*\]\()([^\)\n]+)(\))')
rewrites = {}
for path in root.rglob('*.md'):
    if any(part.lower().startswith('archiv') or part.endswith('Änderungen-Prompt') for part in path.parts):
        continue
    if any(part.startswith('qa-') for part in path.parts):
        continue
    original = path.read_text(encoding='utf-8-sig')
    new_path = translated(path.resolve())
    def rewrite(match):
        raw = match[2]
        target = raw.strip('<>')
        if '://' in target or target.startswith(('#', 'mailto:')):
            return match[0]
        link, separator, fragment = target.partition('#')
        old_target = (path.parent/unquote(link)).resolve()
        new_target = translated(old_target)
        if new_target == old_target and new_path == path.resolve():
            return match[0]
        relative = Path(os.path.relpath(new_target, new_path.parent)).as_posix()
        if separator: relative += '#'+fragment
        if ' ' in relative: relative = '<'+relative+'>'
        return match[1]+relative+match[3]
    updated = pattern.sub(rewrite, original)
    if updated != original:
        rewrites[path.resolve()] = updated

for old, new in moves.items():
    new.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(old), str(new))
for old, content in rewrites.items():
    target = translated(old)
    if target == old:
        backup = old.parent/'archiv'/f'{old.stem}_3.26.0_vor_Archivverweisen.md'
        backup.parent.mkdir(exist_ok=True)
        if not backup.exists(): shutil.copy2(old, backup)
    target.write_text(content, encoding='utf-8')
manifest = {'moves': {str(old.relative_to(root)): str(new.relative_to(root)) for old,new in moves.items()},
            'links_updated': [str(translated(old).relative_to(root)) for old in rewrites]}
(Path(__file__).parent/'archivierung_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(moves)} Dokumente/QA-Ordner archiviert, {len(rewrites)} Linkdateien nachgeführt; nichts gelöscht.')
