"""Inventur und Dokumentationsindex aus dem finalen lokalen Bestand erzeugen."""
from pathlib import Path
import csv
import hashlib
import json
import re
import zipfile
from dokumente_abgleichen import ROOT, save

WORKSPACE = ROOT.parents[1]
QA = Path(__file__).resolve().parent

def archives():
    for folder in sorted(p for p in ROOT.rglob('archiv') if p.is_dir()):
        target = folder / 'README.md'
        if target.exists():
            continue
        body = '''# Archiv

Hier bleiben Vorgängerfassungen des unmittelbar übergeordneten Bereichs erhalten.
Dateinamen enthalten den beschriebenen Versionsstand; `vor_Bestandsanalyse_2026-09-04`
kennzeichnet den unveränderten Eingangsstand der aktuellen Konsolidierung.
Archivgrund: durch eine inhaltlich abgeglichene Fassung zu Glide 3.2.0 ersetzt.
Vorhandene historische Versionen und ihre Aussagen wurden nicht umetikettiert.
Verweise innerhalb dieser Originale können frühere Speicherorte beschreiben und
sind keine aktuellen Einstiegspunkte. Aktive Dokumente stehen außerhalb des Archivs.

'''
        body += '\n'.join('- `' + p.name + '`' for p in sorted(folder.iterdir()) if p.is_file()) + '\n'
        target.write_text(body, encoding='utf-8')

def index():
    target = ROOT / 'docs/00_INDEX.md'
    if not (target.parent / 'archiv/00_INDEX_3.2.0_vor_Bestandsanalyse_2026-09-04.md').exists():
        save('docs/00_INDEX.md', target.read_text(encoding='utf-8'))
    entries = sorted((ROOT / 'docs').rglob('*.md'))
    groups = {'Aktuelle Quellen': [], 'Ausführungspläne – historische Entscheidungen': [], 'Archiv – unveränderte Vorgänger': []}
    for path in entries:
        relative = path.relative_to(ROOT / 'docs').as_posix()
        if relative == '00_INDEX.md':
            continue
        title = next((line.lstrip('# ').strip() for line in path.read_text(encoding='utf-8-sig').splitlines() if line.startswith('#')), path.stem)
        label = f'`{relative}` – {title}'
        row = f'- [{relative}](<{relative}>) – {title}'
        key = 'Archiv – unveränderte Vorgänger' if 'archiv' in path.parts else 'Ausführungspläne – historische Entscheidungen' if 'exec-plans' in path.parts else 'Aktuelle Quellen'
        groups[key].append(row)
    body = '''# Dokumentationsindex

Stand: 04.09.2026 · App-Version 3.2.0 · Datenformat 10

Der Index erfasst jede Markdown-Datei unter `docs/`, einschließlich der
Vorgängerfassungen. Diese Datei ist selbst der Einstiegspunkt. Historische
Versionsangaben in Archiven und Ausführungsplänen bleiben bewusst erhalten.
Die Nummern 03 und 04 sind im verfügbaren Bestand nicht belegt; ohne
Git-Historie lässt sich eine frühere Belegung nicht feststellen.

'''
    for key, rows in groups.items():
        body += '## ' + key + '\n\n' + '\n'.join(rows) + '\n\n'
    body += '''## Quellen außerhalb von docs

- [Arbeitsregeln](../AGENTS.md)
- [Projektüberblick](../README.md)
- [Testaufrufe](../tests/README.md)
- [Werkzeuge](../tests/tools/README.md)
- [Referenz- und Arbeitsdaten](../tests/fixtures/README.md)
- [Äußere Arbeitsvorbereitung](../../../00_Arbeitsvorbereitung/README.md)
- [Aktuelles Produktdatenblatt](../../../40_Store_Material/Produktdatenblatt_3.2.0.md)
- [Release-Ablage](../../../30_Release_Exports/README.md)

Die ausführliche Word-Arbeitsgrundlage liegt im äußeren `10_Dokumentation/`.
Die Markdown-Dateien im Repository bleiben die knappen, code-nahen Quellen.
'''
    target.write_text(body, encoding='utf-8')

def classification(path):
    relative = path.relative_to(ROOT).as_posix()
    archived = 'archiv' in path.parts
    version = next(iter(re.findall(r'\d+\.\d+\.\d+', path.name)), '3.2.0 abgeglichen')
    if '__pycache__' in path.parts or path.suffix == '.pyc':
        return 'Python-Cache', 'temporär / Artefakt', 'laufzeitabhängig', 'nicht zur Laufzeit erforderlich'
    if archived:
        category = 'Dokumentation, historisch' if path.suffix.lower() == '.md' else 'Test' if path.name.startswith('test_') else 'Werkzeug'
        return 'Vorgängerfassung/Archivnachweis', category, version if version != '3.2.0 abgeglichen' else 'Archivkonzept 3.2.0', 'bewusst unverändert; nicht aktive Quelle'
    if 'exec-plans' in path.parts:
        return 'Historischer Ausführungsplan', 'Dokumentation, historisch', version, 'Entscheidungsverlauf, nicht heutiger Prüfnachweis'
    if relative == 'src/glide/app.pyw':
        return 'Gesamte Anwendung', 'produktiv', '3.2.0 / Schema 10', 'unveränderter Monolith; SHA-256 geprüft'
    if relative == 'VERSION':
        return 'App-Version', 'produktiv', '3.2.0', 'mit App/Test/Changelog abgeglichen'
    if 'fixtures' in path.parts and path.suffix != '.md':
        if path.suffix == '.glidebackup':
            return 'Importierbarer Beispiel-/Arbeitsbestand', 'Fixture', '3.2.0 / Schema 10', 'generiert; Erzeuger unter tests/tools; Schema-/Importprüfung'
        schema = re.search(r'(?:current_v|legacy_v)(\d+)', relative)
        return 'Kompatibilitätsreferenz', 'Fixture', 'Schema ' + (schema.group(1) if schema else 'unbekannt'), 'historische Daten bewusst erhalten und aktuell geladen'
    if 'integration' in path.parts:
        return 'Automatisierte Funktions-/Integritätsprüfung', 'Test', '3.2.0', 'lineares Skript; isolierte Daten'
    if path.suffix == '.md':
        if path.name in ('08_CODE_BEFUND.md', '09_ARBEITSAUFTRAG_BESTANDSANALYSE.md'):
            return 'Aktuell eingeordnete historische Referenz', 'Dokumentation, aktuell', '3.2.0 mit gekennzeichneter Historie', 'ursprüngliche Inhalte erhalten; aktuelle Abweichungen vorangestellt'
        return 'Projekt-/Prozessdokumentation', 'Dokumentation, aktuell', version, 'Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden'
    if 'scripts/release' in relative and 'v252' in path.name or path.name == 'update_release_plan_docx.py':
        return 'Historisches Word-Fortschreibungswerkzeug', 'Werkzeug', '2.5.x', 'nicht für aktuelle App-/Dokumentversion aufrufen; als Historie erhalten'
    if 'requirements' in path.parts:
        return 'Laufzeit-/Builddeklaration', 'Werkzeug', '3.2.0 abgeglichen', 'keine externe App-Laufzeitabhängigkeit; Buildpins noch offen'
    if path.suffix in ('.py', '.ps1'):
        return 'Prüf-/Erzeugungswerkzeug', 'Werkzeug', '3.2.0', 'CLI/Voraussetzungen im zugehörigen README'
    if path.name in ('.editorconfig', '.gitattributes', '.gitignore'):
        return 'Entwicklungs-/Dateiformatregeln', 'Werkzeug', 'versionsneutral, für 3.2.0 gültig', 'vorhanden; Git-Historie fehlt in dieser Kopie'
    return 'Nicht sicher zugeordnet', 'Status unklar', 'STATUS UNKLAR', 'gesondert prüfen'

def report():
    path = ROOT / 'docs/11_BESTANDSANALYSE.md'
    if not path.exists():
        path.write_text('# Bestandsanalyse 3.2.0\n', encoding='utf-8')
    files = sorted(p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts)
    body = '''# Bestandsanalyse 3.2.0

Stand: 04.09.2026 · App-Version 3.2.0 · Datenformat 10

## Fakt: Umfang und Ausgangslage

Geprüft wurden die lokale Repository-Kopie `01_Repository/Glide` und die
erreichbaren äußeren Arbeits-, Dokumentations-, Versions- und Store-Ordner.
Der zuerst übergebene Kontext wurde vor dem Arbeitsauftrag gelesen. Der
genannte Pfad `Claude outputs/09_ARBEITSAUFTRAG_BESTANDSANALYSE.md` existiert
nicht; das Dokument liegt unter `docs/09_ARBEITSAUFTRAG_BESTANDSANALYSE.md`.
Der Text ist eine Referenz des Auftrags, kein Ersatz für geprüfte Dateifakten.

`git status` meldet, dass diese Kopie kein Git-Repository ist. Aussagen über
verlorene frühere Dateien, „Phase 11“ oder die unbelegten Dokumentnummern 03/04
lassen sich deshalb nicht über `git log` absichern. Es wurden keine Dokumente
nur zur Füllung dieser Nummernlücken erfunden.

`VERSION`, `APP_VERSION`, die explizite Testprüfung und der oberste
Changelog-Eintrag nennen 3.2.0. `DATA_SCHEMA_VERSION` ist 10; portable Backups
werden von 4 bis 10 unterstützt. Die acht JSON-Fixtures bleiben unverändert.
Die kanonische App und `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.2.0.pyw`
sind bytegleich und wurden nicht verändert.

App-SHA-256: `6309f2669f5490777d342138e9fe304b27a4e728404d0359952e3cd4bfc01715`.

## Befund und Maßnahme: Inkonsistenzen

Fundstellen nennen Abschnitt und eindeutigen Suchtext; der unveränderte
Ausgangswortlaut bleibt jeweils in der versionierten Archivkopie erhalten.

| Schwere | Fundstelle im Ausgangsbestand | Befund | Maßnahme / Ergebnis |
|---|---|---|---|
| wichtig | Handoff, Dokumentationstabelle; Startkontext, bekannte Fehler | Register/QA/Release angeblich 2.11.0; Dateien waren bereits auf 3.2.0, Register bereits Schema 10 | Kontext gegen echte Dateien fortgeschrieben |
| wichtig | Architektur, Datenmodell „Mehrzeiligkeit … erst bei Darstellung“ | widerspricht gespeicherten Long-Task-Zeilen in `normalize_item_text` | 40 gespeicherte / höchstens fünf dargestellte Zeilen korrekt beschrieben |
| wichtig | Architektur, zweiter Abschnitt „Symbole“ | erlaubte Emoji außerhalb Aufgabenliste, widersprach Zielvorgabe | doppelte widersprüchliche Passage entfernt; drei tatsächliche Ausnahmen transparent dokumentiert |
| wichtig | README/Changelog/QA/Register „alle Symbole“, „0 Emoji“ | 📁, 🚩 und 📝 außerhalb ICONS vorhanden | Aussage korrigiert, keine gestalterische Eigenentscheidung |
| wichtig | Backup-Dokument, „Backup-Kompatibilität“ | Formate nur 4 bis 9; zwei Fixturelisten nur fünf statt acht Bestände | Formate 4 bis 10 und alle acht Referenzen nachgeführt |
| wichtig | Backup-Dokument, Datenformat 7 | entfernte `LEGACY_LABEL_COLOR_MAP` als aktiv beschrieben | lokale Vorgabefarbe vs. portable strikte Ablehnung erklärt |
| wichtig | Architektur, „Bewusste Übergangsentscheidung“; Word-Plan | Modulaufteilung als nächster Schritt | Monolith als aktuelle Entscheidung erhalten |
| wichtig | QA-Bericht/Startkontext „alle Tests grün“, „nur Linux“ | erste aktuelle Windows-Prüfung fand zwei Testabbrüche | Ausgangslauf protokolliert, Testannahmen gezielt korrigiert, alle drei Suiten erneut bestanden |
| wichtig | `test_glide.py`, Windows-Layoutblock | Zugriff auf entferntes `system_box` | aktuelles `system_listbox` und Fehlen des Rahmens geprüft |
| kosmetisch | `test_glide.py`, Kopfmetrik | Windows reqheight 43 vs. Button 42 | explizite max. 1 px Fonttoleranz; Labelwechselhöhe weiterhin exakt gleich |
| wichtig | `test_datenintegritaet.py`, Start/Drag | leere bbox vor nativer Fensterereignisverarbeitung | `root.update()` nach Aufbau; Assertions unverändert |
| wichtig | Index/Releasecheckliste, Produktdatenabschnitt | angeblich letztes Datenblatt 2.6.0, obwohl 3.2.0 vorhanden | aktive 3.2-Quelle verlinkt und inhaltlich korrigiert |
| wichtig | Store-/Word-Unterlagen | geplante Laufzeit, Plattformabnahme, Sandbox oder Pflichtfelder teils als fertig dargestellt | belegte App-Fakten, recherchierte Vorgaben und offene Freigaben getrennt |
| kosmetisch | QA-Testplan/Architektur, LabelChip | Radius6 statt tatsächlichem9 | gegen `LabelChip.RADIUS` korrigiert |
| kosmetisch | Handoff, Quellzeilen / Werkzeuge |14.590 statt Werkzeugzählung 14.591; tools-README angeblich nur Screenshot | aktuelle Zählweise festgehalten; bereits vorhandene vier Werkzeuge anerkannt und neue ergänzt |
| wichtig | `scripts/test/run_core_tests.ps1` | startete nur Hauptsuite | Aufruf des gemeinsamen Prüfskripts statt unvollständiger Testfolge |
| kosmetisch | `requirements/runtime.txt` | Kommentar noch Glide 2.9.0 | auf 3.2.0 nachgeführt, keine neue Abhängigkeit |

Keine festgestellte Versionsinkonsistenz von `VERSION`/App/Test musste durch
eine Versionserhöhung kaschiert werden. Historische Versionsnummern in
Ausführungsplänen, Changelog und Schema-Fixtures sind fachlich richtig und
wurden nicht pauschal ersetzt.

## Maßnahme: Dateistruktur und Archiv

Es bestanden bereits dezentrale Archive. Dieses Konzept wurde fortgeführt:
`archiv/` innerhalb des Repositorys, `Archiv/` in den äußeren Bereichen.
Vor dem Überschreiben wurden alte Dokumentstände mit Version und bei mehreren
3.2-Fassungen zusätzlich Datum/Anlass kopiert. Das jeweilige Archiv-README
erklärt Zweck, Benennung und Grund. Bestehende Projekt-/Nutzdateien wurden
nicht gelöscht; alte Codeversionen und alle Kompatibilitäts-Fixtures bleiben
erhalten. Historische interne Verweise sind Originaltext und können frühere
Speicherorte nennen; aktive Markdown-Links und der aktuelle Index werden geprüft.

Es wurde keine Verschiebung von produktiv gelesenen Fixtures oder App-Quellen
vorgenommen. Die äußeren historischen 2.6-/2.11-Unterlagen sind von den aktiven
3.2-Dateien getrennt. Die Word-Gliederung und Gestaltung wurden bei der
Fortschreibung erhalten. Sämtliche aktuellen Dokumente unter `docs/` sowie
die Archivdateien sind einzeln im `00_INDEX.md` verzeichnet.

'''
    audit = (QA / 'codeaudit.md').read_text(encoding='utf-8')
    audit = audit[audit.index('## Ausgangslage'):]
    audit = audit.replace('vor eventuellen Symbolkorrekturen', 'ohne Symbolkorrekturen')
    audit = audit.replace('durch Hauptbearbeitung klären', 'als drei Symbolarten dokumentiert; Änderung bleibt offen')
    audit = audit.replace('spätere\nProduktionsänderungen', 'abschließende Dokument- und Fixtureergänzungen')
    body += '## Codeprüfung und Prozessverbesserung\n\n' + audit + '\n'
    body += '''
### Ergänzender Architekturabgleich

Die gemeinsame Änderungslogik ist noch nicht lückenlos umgesetzt.
`indent_selected` (12905) und `outdent_selected` (12923) verwenden
`item_change` ohne zusätzlichen Bestandswächter. `add_child_item` (11803)
und `apply_sidebar_rename` (5532) nutzen noch direkte Snapshot-/Speicherfolgen.
Die Dokumentation hatte die verbindliche Zielregel als vollständig erreichten
Istzustand ausgegeben. Dieser Überanspruch ist korrigiert; eine strukturelle
Umstellung der verbleibenden Aufrufer wurde nicht eigenmächtig vorgenommen.
Status: **GEMELDET**, wichtiger Architekturrest, kein hier neu reproduzierter
Datenverlust. Vor weiterer Änderung gezielt mit Rückgängig-/Fehlerpfaden prüfen.

`audit_app.py` enthält nummerierte Abschnitte 1 bis 10. Die Behauptung, es
gebe keinerlei Phasenstruktur, war falsch; nur die frühere elfte Phase bleibt
ohne Originaldatei/Git-Historie unbelegt.

'''

    body += '''## Drei Arbeitslisten im nativen Glide-Format

`tests/tools/releasedaten.py` erzeugt genau ein gemeinsames Backup unter
`tests/fixtures/beispiele/glide_releaseplanung_3.2.0.glidebackup`. Es enthält
die Listen „Unterlagen & Assets“, „Vermarktungsstrategie“ und „Feature-Übersicht“
in einem Release-Ordner sowie den technisch erforderlichen geschützten Eingang.
„3.2.0“ bezeichnet den tatsächlichen App-Stand; ein erfundenes Release 1.0
wurde vermieden. Alle vier Punktarten und der kleine Labelsatz werden verwendet.

Store-, Icon-, Text- und Signaturvorgaben sowie Wettbewerbsangaben tragen
Quelle und Abrufdatum 04.09.2026 in den Beschreibungstexten. Recherchierte
Anforderungen werden nach Windows-Vertriebspfad bzw. macOS-Store/Direktvertrieb
getrennt. Zielgruppen-, Kanal- und Preisüberlegungen sind Vorschläge, keine
Inhaberentscheidung. Fristen sind relative Planungsvorschläge ab Erzeugung,
keine vereinbarten Termine. Eine erneute Erzeugung aktualisiert keine Webrecherche.

Archivprüfung, Schemaprüfung, Listen-/Papierkorbnormierung und Labelreferenzen
werden mit dem echten App-Code kontrolliert. Die Hauptsuite prüft das neue
Fixture dauerhaft. Der Generator prüft außerdem das tatsächliche Einlesen.

**Ein Komplettbackup ersetzt den gesamten Bestand.** Zum Testen ein isoliertes
`GLIDE_DATA_DIR` verwenden; vor Import in eine eigene Ablage vollständig sichern.
Es wurden keine Arbeitslisten in den echten Datenbestand des Nutzers importiert.

'''
    backup = ROOT / 'tests/fixtures/beispiele/glide_releaseplanung_3.2.0.glidebackup'
    if backup.exists():
        with zipfile.ZipFile(backup) as z:
            data = json.loads(z.read('data.json'))
        def items(entries):
            for entry in entries:
                yield entry
                yield from items(entry.get('children', []))
        points = [p for listing in data.get('lists', []) for p in items(listing.get('items', []))]
        counts = {kind: sum(p.get('kind', 'task') == kind for p in points) for kind in ('task','group','long','heading')}
        body += f"Erzeugter Inhalt: {len(data.get('folders', []))} Ordner, {len(data.get('lists', []))} Listen einschließlich Eingang, {len(points)} Punkte, {len(data.get('labels', []))} Labels einschließlich Systemlabels. Arten: {counts}.\n\n"
    final = QA / 'abschluss/ergebnis.json'
    if final.exists():
        result = json.loads(final.read_text(encoding='utf-8'))
        body += f"## Abschließender Prüflauf\n\nZeitpunkt: {result['zeitpunkt']}. Modus: {result['modus']}. Exitcode: {result['exitcode']}.\n\n"
        body += '| Schritt | Status | Ergebnis/Grund |\n|---|---|---|\n'
        for row in result['schritte']:
            body += '| ' + ' | '.join(str(row[k]).replace('|','/').replace('\n',' ') for k in ('schritt','status','grund')) + ' |\n'
        body += '\nDie separat angesehenen Windows-Aufnahmen und das Word-Renderprotokoll sind\nim äußeren QA-Ordner erhalten. Ein automatisiertes Werkzeug kann diese\nSichtabnahme selbst nicht bescheinigen.\n\n'
    else:
        body += '## Abschließender Prüflauf\n\nDer finale Gesamtlauf nach allen Ergänzungen wird unter `50_Ablage/QA/Bestandsanalyse_3.2.0/abschluss/` protokolliert. Vorherige erfolgreiche Läufe ersetzen diesen Abschluss nicht.\n\n'
    body += '''## Offen / nicht beurteilbar

- **Vor Release zu beheben:** fehlende Tiefenprüfung vor tiefenerhöhenden
  Mutationen und Überschreitung der Labelgrenze durch Artwechsel. Eine
  strukturell konsistente Behebung wurde nicht durch einen lokalen Sonderfall ersetzt.
- **NICHT VERIFIZIERT:** Behebung des gemeldeten Einfrierens; keine
  Reproduktion des ursprünglichen Anwendersymptoms.
- **NOCH ZU TESTEN:** vollständige manuelle Windows-/macOS-Matrix,
  mehrere Monitore/DPI, reale Eingabegeräte, Langzeitnutzung und echte Datenkopien.
- **STATUS UNKLAR:** frühere Git-Historie, Dokumentnummern 03/04, verlorene
  Auditphase und ehemalige Zufallslaufwerkzeuge. Keine Rekonstruktion erfunden.
- **Inhaberentscheidungen:** Publisher, Copyright, URLs/Kontakte, Lizenz,
  Preis, IDs, Zielarchitekturen, Betriebssystem-Mindestversionen, Markenfreigabe
  und Vertriebswege. Produktive Storeformulare wurden nicht eingereicht.
- **Noch nicht vorhanden:** freigegebener Branding-Master, reproduzierbare
  Installer/App-Bundles, Signing-/Notarisierungsnachweis und finale Storeassets.

## Vollständige Datei-Inventur des Repositorys

Jede vorhandene Datei wird genau einmal kategorisiert. „3.2.0 abgeglichen“
bezeichnet die geprüfte aktuelle Gültigkeit, nicht eine erfundene ursprüngliche
Entstehungsversion. Historische Werkzeuge und Metadaten tragen ihre eigene Rolle.
Externe Arbeitsartefakte sind oben beschrieben und über ihre Ordner-README erreichbar.

| Pfad | Rolle | Kategorie | Inhaltlicher Stand | Besonderheit |
|---|---|---|---|---|
'''
    unknown = []
    for file in files:
        row = classification(file)
        if row[1] == 'Status unklar':
            unknown.append(str(file))
        body += '| `' + file.relative_to(ROOT).as_posix() + '` | ' + ' | '.join(row) + ' |\n'
    body += f'\nInventur: **{len(files)} Dateien**, `.git/` ausgenommen; {len(unknown)} nicht sicher zugeordnet.\n'
    path.write_text(body, encoding='utf-8')
    with (QA / 'Repository_SHA256.csv').open('w', newline='', encoding='utf-8-sig') as out:
        writer = csv.writer(out, delimiter=';')
        writer.writerow(['Pfad', 'Bytes', 'SHA256'])
        for file in files:
            raw = file.read_bytes()
            writer.writerow([file.relative_to(ROOT).as_posix(), len(raw), hashlib.sha256(raw).hexdigest()])
    print(f'Inventur: {len(files)} Dateien; {len(unknown)} unklar.')

if __name__ == '__main__':
    archives()
    report()
    index()
    report()
