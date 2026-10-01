from pathlib import Path
from datetime import datetime
import json, shutil, re
R=Path.cwd(); B=Path(__file__).parent; REPO='01_Repository/Glide/'
result=json.loads((R/REPO/'tests/qa-3.21.4/abschluss/ergebnis.json').read_text())
assert result['exitcode']==0,result
assert len(result['schritte'])==39
assert sum(x['status']=='ausgeführt' for x in result['schritte'])==37
stamp=datetime.fromisoformat(result['zeitpunkt']); day=stamp.strftime('%d.%m.%Y'); hour=stamp.strftime('%H:%M')
summary=f'Der vollständige Abschlusslauf zu **3.21.4** bestand am **{day} um {hour}** auf macOS mit Python 3.14.5 und `TZ=Europe/Berlin`: **Exitcode 0**, **39 Schritte, davon 37 ausgeführt**. Alle **25 Testsuiten**, drei Analysen, Vorprüfungen sowie Beispiel- und Releaseabgleiche bestanden. Übersprungen blieben ausschließlich die plattformgebundene Screenshot-Erzeugung und die manuelle Sichtprüfung.'
changes={}; archives=[]
def read(rel):return changes.get(rel,(R/rel).read_text())
def settext(rel,text):changes[rel]=text

def replace(rel,old,new):
 text=read(rel)
 assert old in text,(rel,old)
 settext(rel,text.replace(old,new,1))

q=REPO+'docs/07_QA_BERICHT.md';t=read(q)
start=t.index('Für 3.21.4 sind alle');end=t.index('\n\n',start)
paragraph=t[start:end]
details=paragraph[paragraph.index('3.21.4 ändert keinen Anwendungscode'):]
details=details[:details.index(' Der maßgebliche macOS-Lauf steht aus:')]
t=t[:start]+summary+' [Prüfprotokoll](../tests/qa-3.21.4/abschluss/ergebnis.json).\n\n'+details+t[end:]
settext(q,t+'\n## Ergänzender Befund beim Ablageabschluss\n\nDer [erste vollständige Lauf](../tests/qa-3.21.4/vor_Korrektur_Erinnerungsabgleich/ergebnis.json) bestand alle 25 Suiten und drei Analysen, scheiterte aber am Beispielabgleich nach dem Tageswechsel. Ein fester Erinnerungstermin wurde absolut verglichen. Die Korrektur in `pruefen.py` erhält Tagesabstand und Ortszeit einschließlich Sommerzeitwechsel; abweichende Tage und Uhrzeiten bleiben Fehler. Die mitgelieferten Beispieldaten wurden nicht ersetzt. Der oben verlinkte Abschlusslauf prüft den korrigierten Stand.\n')

handoff='00_Arbeitsvorbereitung/Glide_Weitergabe_neuer_Chat_2026-09-11.md';t=read(handoff)
start=t.index('Für 3.21.4 sind alle');end=t.index(' Offen bleiben',start)
settext(handoff,t[:start]+summary+' [Prüfprotokoll](../01_Repository/Glide/tests/qa-3.21.4/abschluss/ergebnis.json).'+t[end:])

facts='00_Arbeitsvorbereitung/Notizen/Technische_Fakten_3.21.4.md';t=read(facts)
start=t.index('## Prüfstand\n');end=t.index('## Wissensstand',start)
settext(facts,t[:start]+'## Prüfstand\n\n'+summary+'\n\n[Prüfprotokoll](../../01_Repository/Glide/tests/qa-3.21.4/abschluss/ergebnis.json).\n\nDie Ablageprüfung korrigierte außerdem eine fehlende Wortgrenze in Regel R6: `Vorlagenformat 2` und `Einstellungsformat 2` dürfen nicht als Aufgabenformat gelesen werden. Positive und negative Gegenproben bestanden. Das Original des Prüfwerkzeugs liegt im lokalen Archiv; der Anwendungscode bleibt bis auf die Versionsnummer unverändert.\n\n'+t[end:])
replace(facts,'Der 3.21.3-Lauf ist entsprechend in QA-Bericht,\nWeitergabe und den Technischen Fakten zu 3.21.3 nachgetragen.', 'Der 3.21.3-Lauf ist im aktuellen QA-Bericht und in der Weitergabe nachgetragen.\nDie archivierten Technischen Fakten zu 3.21.3 behalten ihren ursprünglichen\nWortlaut; der abgeschlossene Prüflauf ist separat erhalten.')

product='40_Store_Material/Produktdatenblatt_3.21.4.md'
replace(product,'Der maßgebliche macOS-Abschlusslauf zu 3.21.4 steht bis zum dokumentierten\nPrüfergebnis aus. Der Nachweis je Stand steht im QA-Bericht.', summary+' Der Nachweis je Stand steht im QA-Bericht.')

checklist='00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.21.4.md';t=read(checklist)
for old in (
 '- [ ] `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.21.4/abschluss`',
 '- [ ] Ergebnis danach in QA-Bericht, Weitergabe und Technische Fakten **dieses**',
 '- [ ] `Claude outputs` ist leer;',
 '- [ ] `05_Probelisten_Testdaten` enthält aktiv nur die drei 3.21.4-Dateien und',
 '- [ ] `00_Arbeitsvorbereitung/Notizen`, `Checklisten` und `Entscheidungen`',
 '- [ ] `tests/fixtures/beispiele` enthält weiterhin **alle** versionierten',
 '- [ ] `50_Ablage/Archiv/Werkzeuge_3.21.4` enthält Ablage- und',
):
 assert old in t,old;t=t.replace(old,old.replace('- [ ]','- [x]'),1)
t+='\n## Nachweis der Ablageprüfung am '+day+'\n\n'+summary+'\n\nDie markierten Punkte wurden ausgeführt. Weitere Kontrollkästchen bleiben als\nmanuelle Prüfwege bestehen. Der [Ablagenachweis](../../50_Ablage/Archiv/Werkzeuge_3.21.4/Ablageprotokoll_2026-09-15.md) dokumentiert Archivierung, Prüfsummen und die ergänzenden Korrekturen.\n'
settext(checklist,t)

project=REPO+'docs/09_PROJECT_HANDOFF.md'
replace(project,'## Funktionsbestand', '## Prüf- und Ablagestand\n\n'+summary+' [Prüfprotokoll](../tests/qa-3.21.4/abschluss/ergebnis.json).\n\nDie Übernahme ist abgeschlossen. In `07_Python-Versionen` liegt nur die aktuelle startbare Fassung; ältere Arbeitsstände und das unveränderte Übertragungspaket sind archiviert. Eine Wortgrenze in `standpruefung.py` verhindert Fehlalarme bei Vorlagenformat 2. `pruefen.py` vergleicht feste Erinnerungen im Beispielbestand relativ zum Erzeugungstag und unter Erhaltung der Ortszeit; Gegenproben einschließlich Sommerzeitwechsel bestanden.\n\n## Funktionsbestand')
replace(REPO+'docs/03_STARTKONTEXT.md','Aufgabenformat ist jetzt 14.', 'Diese Ansichten wurden in Aufgabenformat 13 eingeführt. Aktuell gilt Aufgabenformat 15; Format 14 ergänzte in 3.14 Bearbeitungstag und Aufwand.')

# The source audit lists ten individual code assertions. Avoid carrying its
# unsupported headline count of twelve into the current handoff documents.
for rel in (q,handoff,facts,checklist,project,'00_Arbeitsvorbereitung/Entscheidungen/Offene_Entscheidungen_3.21.4.md'):
 t=read(rel)
 for old,new in [('zwölf sachlich falsche Aussagen','zehn aufgeführte falsche Aussagen'),('Zwölf davon sind sachlich falsche Aussagen','Zehn aufgeführte Befunde betreffen falsche Aussagen'),('Zwölf falsche Aussagen','Zehn aufgeführte falsche Aussagen'),('zwölf Aussagen über den Anwendungscode','zehn aufgeführte Aussagen über den Anwendungscode'),('Die zwölf Codeaussagen','Die aufgeführten Codeaussagen'),('die zwölf falschen','die aufgeführten falschen'),('Zwölf falsche Codeaussagen','Falsche Codeaussagen'),('Alle zwölf stehen','Die aufgeführten Aussagen stehen')]:t=t.replace(old,new)
 settext(rel,t)
cl=REPO+'CHANGELOG.md';t=read(cl)
t=t.replace('**Zwölf sachlich falsche Aussagen über den Anwendungscode**','**Zehn aufgeführte falsche Aussagen über den Anwendungscode**',1)
t=t.replace('ist im QA-Bericht, in der Weitergabe und in den Technischen Fakten zu 3.21.3 eingetragen.', 'ist im aktuellen QA-Bericht und in der Weitergabe eingetragen; die archivierten Technischen Fakten zu 3.21.3 behalten ihren ursprünglichen Wortlaut.',1)
anchor_line = '- Ablageprüfung am 15.09.2026:'
position = t.index('\n', t.index(anchor_line))
t = t[:position] + '\n- Der vollständige Ablagelauf fand außerdem einen tagesabhängigen Fehler beim Beispielabgleich: Feste Erinnerungen wurden als absolute UTC-Zeitpunkte verglichen, obwohl der Erzeuger sie relativ zum Erzeugungstag setzt. `pruefen.py` vergleicht jetzt ihren Tagesabstand und ihre Ortszeit; die absolute Releaseprüfung bleibt unverändert. Paket, Neuerzeugung, Sommerzeitwechsel und absichtlich falsche Zeiten wurden gegengeprüft. Der erste fehlgeschlagene Prüflauf bleibt als Nachweis erhalten.' + t[position:]
settext(cl,t)

replace('README.md','Alte Arbeitsversionen wurden nachvollziehbar',f'Ablage und automatisierter Abschlusslauf zu 3.21.4 sind am {day} abgeschlossen. [Ablage- und Prüfnachweis](50_Ablage/Archiv/Werkzeuge_3.21.4/Ablageprotokoll_2026-09-15.md).\n\nAlte Arbeitsversionen wurden nachvollziehbar')
settext('50_Ablage/README.md',read('50_Ablage/README.md')+'\n## Übernahme 3.21.4\n\n[Ablage- und Prüfnachweis](Archiv/Werkzeuge_3.21.4/Ablageprotokoll_2026-09-15.md) · [Originalpaket](Archiv/Uebertragungspakete/glide-3.21.4-ablagepaket.zip). Die Originalwerkzeuge, Nacharbeiten und Prüfsummen liegen zusammen im Werkzeugarchiv. Das QA-Dateimanifest wurde nach der Archivierung aktualisiert.\n')

for rel,text in changes.items():
 # Updated documentation date; the version's release date remains 14 September.
 text=re.sub(r'(?m)^(Stand:?) 14\.09\.2026',rf'\g<1> {day}',text,count=1)
 p=R/rel
 if text==p.read_text():continue
 folder=next((x for x in p.parent.iterdir() if x.is_dir() and x.name.lower()=='archiv'),p.parent/'archiv')
 archive=folder/f'{p.stem}_3.21.4_vor_Abschluss_2026-09-15{p.suffix}'
 if not archive.exists():folder.mkdir(exist_ok=True);shutil.copy2(p,archive)
 archives.append(archive)
 p.write_text(text)

# Add every new docs archive path before final link and index verification.
p=R/REPO/'docs/00_INDEX.md';text=p.read_text();missing=[]
for f in sorted((p.parent).rglob('*.md')):
 rel=f.relative_to(p.parent).as_posix()
 if f!=p and rel not in text:missing.append(rel)
if missing:
 archive=p.parent/'archiv/00_INDEX_3.21.4_vor_Abschluss_2026-09-15.md'
 if not archive.exists():shutil.copy2(p,archive)
 ar=archive.relative_to(p.parent).as_posix()
 if ar not in text:missing.append(ar)
 text+='\n## Archivnachweise der Abschlussprüfung am '+day+'\n\n'+'\n'.join(f'- [{rel}](<{rel}>)' for rel in sorted(set(missing)))+'\n'
 p.write_text(text)
(B/'abschluss-dokumente.json').write_text(json.dumps({'geändert':list(changes),'archiviert':[p.relative_to(R).as_posix() for p in archives]},ensure_ascii=False,indent=2))
print(f'Prüfergebnis vom {day} {hour} in {len(changes)} Dokumenten eingetragen; neue Archivnachweise ergänzt.')
