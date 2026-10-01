from pathlib import Path
import re
import shutil

root = Path(__file__).resolve().parents[2] / '01_Repository/Glide'
names = ['assets/README.md', 'docs/00_INDEX.md', 'docs/01_PRODUCT_CONSTRAINTS.md',
         'docs/02_ARCHITECTURE.md', 'docs/03_STARTKONTEXT.md', 'docs/05_QA_TESTPLAN.md',
         'docs/06_DATA_BACKUP_MIGRATION.md', 'docs/07_QA_BERICHT.md',
         'docs/09_PROJECT_HANDOFF.md', 'docs/10_RELEASE_CHECKLIST.md',
         'docs/27_VORLAGEN_PRAXISANLEITUNG.md', 'docs/decisions/ARBEITSBEGLEITER.md',
         'docs/decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md', 'docs/decisions/PRODUCT_IDENTITY.md',
         'docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md', 'packaging/README.md',
         'README.md', 'SECURITY.md', 'src/glide/README.md', 'tests/fixtures/README.md',
         'tests/README.md', 'tests/tools/README.md']
for name in names:
    path = root / name
    content = path.read_text(encoding='utf-8')
    backup = path.parent / 'archiv' / f'{path.stem}_3.25.0_vor_Schema17{path.suffix}'
    backup.parent.mkdir(exist_ok=True)
    if not backup.exists():
        shutil.copy2(path, backup)
    lines = content.splitlines()
    for index, line in enumerate(lines):
        if re.match(r'^(?:\*\*)?Stand\b', line):
            lines[index] = (line.replace('3.25.0', '3.26.0').replace('19.09.2026', '20.09.2026')
                           .replace('Datenformat 16', 'Datenformat 17').replace('Aufgabenformat 16', 'Aufgabenformat 17'))
    content = '\n'.join(lines) + '\n'
    content = content.replace('Formate 4 bis 16', 'Formate 4 bis 17').replace('Formate 4–16', 'Formate 4–17')
    path.write_text(content, encoding='utf-8')
for name in ['docs/DEV_NOTES.md', 'docs/decisions/DOKUMENTENPFLEGE.md', 'tests/qa-verlauf.md']:
    path = root / name
    lines = path.read_text(encoding='utf-8').splitlines()
    if not any(line.startswith('Stand ') for line in lines):
        lines.insert(1, '\nStand 20.09.2026 · Glide 3.26.0 · Datenformat 17\n')
        path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
index = root / 'docs/00_INDEX.md'
content = index.read_text(encoding='utf-8')
for path in sorted((root/'docs').rglob('*.md')):
    relative = path.relative_to(root/'docs').as_posix()
    if relative != '00_INDEX.md' and relative not in content:
        content += f'- [{path.stem}]({relative})\n'
index.write_text(content, encoding='utf-8')
print('Standzeilen und Archivindex aktualisiert.')
