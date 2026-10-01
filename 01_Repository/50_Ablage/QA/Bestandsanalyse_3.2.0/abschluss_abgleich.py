from dokumente_abgleichen import ROOT, save

for path in ROOT.rglob('*.md'):
    if 'archiv' in path.parts or 'exec-plans' in path.parts:
        continue
    old = path.read_text(encoding='utf-8')
    new = old.replace('Glide_Releaseplanung_3.2.0.glidebackup', 'glide_releaseplanung_3.2.0.glidebackup')
    if new != old:
        path.write_text(new, encoding='utf-8')

runner = ROOT / 'tests/tools/pruefen.py'
text = runner.read_text(encoding='utf-8').replace('Glide_Releaseplanung_{version}.glidebackup', 'glide_releaseplanung_{version}.glidebackup')
runner.write_text(text, encoding='utf-8')

for name in ('bestandsbericht.py','statusdokumente.py','uebergabe_abgleichen.py'):
    path = __import__('pathlib').Path(__file__).with_name(name)
    path.write_text(path.read_text(encoding='utf-8').replace('Glide_Releaseplanung_3.2.0.glidebackup', 'glide_releaseplanung_3.2.0.glidebackup'), encoding='utf-8')

text = (ROOT / '.gitignore').read_text(encoding='utf-8')
text = text.replace('*.glidebackup\n', '*.glidebackup\n# Generierte Referenz-/Arbeitsbestände gehören mit ihrem Erzeuger ins Repository.\n!tests/fixtures/beispiele/*.glidebackup\n')
save('.gitignore', text)

path = ROOT / 'README.md'
text = path.read_text(encoding='utf-8')
marker = '## Noch offen vor einer öffentlichen Veröffentlichung'
section = '''## Dokumentation und Release-Arbeitslisten

Aktueller Einstieg: [Dokumentationsindex](docs/00_INDEX.md),
[Bestandsanalyse](docs/11_BESTANDSANALYSE.md),
[QA-Bericht](docs/07_QA_BERICHT.md) und [Testaufrufe](tests/README.md).
Die [Word-Arbeitsgrundlage](<../../10_Dokumentation/3.2.0 – Glide_Arbeitsvorbereitung_Codex_Build_Release_Plan.docx>)
führt den bisherigen Plan mit seiner Gliederung auf Stand 3.2.0 fort.

Eine [gemeinsame Backupdatei](tests/fixtures/beispiele/glide_releaseplanung_3.2.0.glidebackup)
enthält drei editierbare Arbeitslisten: Unterlagen & Assets, Vermarktungsstrategie
und Feature-Übersicht. Quelle und Recherchezeitpunkt stehen in den Beschreibungen.
**Der Import ersetzt den gesamten Bestand**; zuerst eine isolierte Testablage
verwenden oder eigene Daten vollständig sichern.

'''
if section not in text:
    text = text.replace(marker, section + marker)
path.write_text(text, encoding='utf-8')

path = ROOT / 'docs/10_RELEASE_CHECKLIST.md'
text = path.read_text(encoding='utf-8').replace('- [ ] Große Bestände auf Zielgeräten vermessen.', '- [ ] Große Bestände auf Zielgeräten vermessen.\n- [ ] Tiefenschutz vor sämtlichen tiefenerhöhenden Punktänderungen absichern.\n- [ ] Labelgrenze bei Wechsel der Punktart inklusive festem Artlabel einhalten.\n  Beide Lücken sind in `11_BESTANDSANALYSE.md` reproduziert dokumentiert.')
path.write_text(text, encoding='utf-8')
print('Dateischreibung, Einstieg und Releasegates konsistent.')
