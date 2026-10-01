from pathlib import Path
import re
import shutil
root = Path(__file__).resolve().parents[2]
paths = ['README.md', '00_Arbeitsvorbereitung/README.md',
         '00_Arbeitsvorbereitung/Glide_KI_Austauschformat_und_Zukunftsarchitektur.md',
         '05_Probelisten_Testdaten/README.md', '07_Python-Versionen/README.md',
         '10_Dokumentation/README.md', '20_Grafik_Master/README.md',
         '30_Release_Exports/README.md', '40_Store_Material/README.md',
         '40_Store_Material/Apple/Store_Angaben_Apple.md',
         '40_Store_Material/Microsoft/Store_Angaben_Microsoft.md',
         '50_Ablage/README.md', '50_Ablage/QA/Dokumentation/README.md',
         '50_Ablage/QA/Dokumentation/Renderlaeufe/README.md',
         '50_Ablage/Screenshots/README.md', '90_Testdaten_Extern/README.md']
for relative in paths:
    p = root / relative
    old = p.read_text(encoding='utf-8')
    archive = p.parent/'archiv'/f'{p.stem}_3.25.0_vor_Schema17.md'
    archive.parent.mkdir(exist_ok=True)
    if not archive.exists():
        shutil.copy2(p, archive)
    lines = old.splitlines()
    for i, line in enumerate(lines):
        if re.search(r'^(?:\*\*)?(?:Stand|Arbeitsstand|Aktueller|Aktuelle)', line):
            if relative == 'README.md' and 'Aktueller Entwicklungsstand' in line:
                lines[i] = ('Aktueller Entwicklungsstand: **3.26.0 vom 21.09.2026**, Datenformat 17. '
                    'Die Nachbesserung ergänzt Notizlisten, Verlauf, Pinnwand-Lasso, Zoom und Navigator sowie responsive Feldmasken. '
                    'Die Gesamtfreigabe richtet sich nach dem [QA-Bericht](01_Repository/Glide/docs/07_QA_BERICHT.md); '
                    'ein Entwicklungsstand ist kein signiertes Release.')
            else:
                lines[i] = line.replace('3.25.0','3.26.0').replace('19.09.2026','21.09.2026').replace('20.09.2026','21.09.2026')
                lines[i] = re.sub(r'([Ff]ormat\s+)16\b',r'\g<1>17',lines[i])
        elif relative == '90_Testdaten_Extern/README.md':
            lines[i] = line.replace('Formate 4 bis 16', 'Formate 4 bis 17')
    p.write_text('\n'.join(lines)+'\n', encoding='utf-8')
p = root/'00_Arbeitsvorbereitung/Fehlerprotokolle/README.md'
s = p.read_text(encoding='utf-8')
if 'Stand ' not in s:
    head, tail = s.split('\n', 1)
    p.write_text(head+'\n\nStand 21.09.2026 · Glide 3.26.0 · Datenformat 17\n'+tail, encoding='utf-8')
print(f'{len(paths)} Ablagedokumente mit Originalsicherung aktualisiert.')
