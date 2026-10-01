"""Conservative OOXML revision of the retained Glide working document.

Only intended text slots, footer date, core metadata and TOC page caches change.
Styles, images, numbering, all relationships and opaque package parts are kept.
"""
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import shutil
from lxml import etree as ET

ROOT = Path(r'%USERPROFILE%\OneDrive\Glide ToDo').resolve()
QA = Path(__file__).resolve().parent
original = ROOT / '10_Dokumentation/2.6.0 – Glide_Arbeitsvorbereitung_Codex_Build_Release_Plan.docx'
reference = original.parent / 'Archiv' / original.name
out = original.with_name(original.name.replace('2.6.0', '3.2.0'))
if original.exists():
    assert ROOT in original.resolve().parents and ROOT in reference.resolve().parents
    if reference.exists():
        assert reference.read_bytes() == original.read_bytes()
    else:
        shutil.copy2(original, reference)
    # Retain the baseline at a stable archive path; no original is deleted.
    preserved = reference.with_name(reference.stem + '_Original_verschoben_2026-09-04.docx')
    assert not preserved.exists()
    shutil.move(original, preserved)
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = '{' + ns['w'] + '}'
with ZipFile(reference) as z:
    parts = {i.filename: z.read(i.filename) for i in z.infolist()}
    infos = z.infolist()
root = ET.fromstring(parts['word/document.xml'])
ps = root.findall('.//w:p', ns)

def para_text(p):
    return ''.join(('\n' if e.tag == W+'br' else '\t' if e.tag == W+'tab' else e.text or '') for e in p.iter() if e.tag in (W+'t',W+'br',W+'tab'))

def replace(index, text):
    p = ps[index]
    rpr = p.find('.//w:rPr',ns)
    for c in list(p):
        if c.tag not in {W+'pPr', W+'bookmarkStart', W+'bookmarkEnd'}:
            p.remove(c)
    r = ET.SubElement(p, W+'r')
    if rpr is not None:
        r.append(deepcopy(rpr))
    for n, line in enumerate(text.split('\n')):
        if n:
            ET.SubElement(r,W+'br')
        t=ET.SubElement(r,W+'t');t.text=line;t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')

revisions = {
5: 'Diese Revision beschreibt Glide 3.2.0 mit Datenformat 10 und den noch offenen Weg zu einem öffentlichen Release. Code, Dokumentation und Beispiele sind konsolidiert; Build, Signing, Produktidentität und manuelle Plattformfreigabe bleiben offen. Historische Screenshots und Ticketvorlagen sind Referenzen.',
6: 'Dokumentversion 3.2.0 · Stand 04.09.2026',
7: 'Arbeitsstatus: Source 3.2.0 · Datenformat 10 · interne Vorabversion ohne freigegebenen Release-Build',
36: 'Gesamtbewertung. Glide 3.2.0 ist eine lokale Aufgaben- und Listen-App mit vier Punktarten, verschachtelten Ordnern, Labels, Papierkorb, Kalender und optionaler Uhrzeit. Der Code bleibt ein Python-/Tk-Monolith. Datenformat 10 und portable Backups der Formate 4 bis 10 werden unterstützt. Für die Veröffentlichung fehlen insbesondere reale Plattformfreigabe, Produktidentität, Branding, Build und Signing.',
38: 'Kernaussage 3.2.0',
39: 'Seit 3.1.0 bündeln item_change und sidebar_change die Änderungen, run_modal die modalen Dialoge. 3.2.0 entfernt die automatische Datenübernahme aus früheren Programmnamen und zentralisiert viele Symbole in ICONS. Gruppen-, Wichtigkeits- und Beschreibungsmarker enthalten weiterhin Emoji-Ausnahmen. Das gemeldete Einfrieren bleibt mangels Reproduktion NICHT VERIFIZIERT.',
60: 'Die Build- und Release-Abfolge ist eine Planung. Im Bestand fehlen noch PyInstaller-Spec, Installer-Skript, macOS-Bundle-Konfiguration und freigegebene Branding-Assets. Dieses Dokument trennt deshalb vorhandene Software von künftig herzustellenden Release-Artefakten.',
62: 'Glide arbeitet lokal, einsprachig Deutsch und ohne Konto, Netzwerkkommunikation oder Telemetrie. Die Laufzeit verwendet nur die Python-Standardbibliothek und Tk. Cloud-Synchronisierung, Mehrbenutzerbetrieb, Konten und Lizenzserver sind bewusste Nicht-Ziele gemäß docs/01_PRODUCT_CONSTRAINTS.md.',
69: '2.4 Umgesetzter Arbeitsstand 3.2.0',
70: 'Kanonischer Source ist 01_Repository/Glide/src/glide/app.pyw. Die aktuelle Einzeldatei unter 07_Python-Versionen ist bytegleich; ältere Stände bleiben unverändert im dortigen Archiv. Arbeitsdokumente werden vor Fortschreibung im Archiv ihres jeweiligen Ordners erhalten.',
71: '''Glide ToDo/
├─ 00_Arbeitsvorbereitung/          aktuelle Vorbereitung 3.2.0
├─ 01_Repository/Glide/
│  ├─ src/glide/app.pyw             kanonischer Monolith
│  ├─ tests/integration/            drei ausführbare Suiten
│  ├─ tests/tools/                  Prüf- und Datenwerkzeuge
│  ├─ tests/fixtures/               Formate 4–10, Legacy 2, Beispiele
│  ├─ docs/                         aktuelle technische Dokumentation
│  └─ assets/, packaging/           Release-Arbeit noch offen
├─ 05_Probelisten_Testdaten/        aktuelle Glide-Beispiele
├─ 07_Python-Versionen/            aktuelle Kopie und Archiv
├─ 10_Dokumentation/               Word-Arbeitsgrundlage 3.2.0
├─ 20_Grafik_Master/               noch keine freigegebenen Assets
├─ 30_Release_Exports/             noch kein freigegebener Build
├─ 40_Store_Material/               Texte, Anforderungen, Quellen
├─ 50_Ablage/                      Prüfberichte und Renderläufe
└─ 90_Testdaten_Extern/             historische Migrationseingaben
Archive liegen dezentral im jeweiligen Ausgangsordner.''',
72: 'Drei Suiten prüfen Hauptfunktionen, Datenintegrität und appweite Pfade. Dazu kommen statische Analyse, Erreichbarkeitsanalyse und Sichtaufnahmen. Die Testisolierung setzt GLIDE_DATA_DIR vor dem App-Import. Einzelne Testpfade wurden an tatsächliche Windows-Fenstergeometrie und Tk-Schriftmetrik angepasst; der App-Code blieb unverändert.',
73: '2.5 Historischer Abbruchpunkt und Dokumentprüfung',
75: 'Historischer Befund aus der Revision 2.5.2: Die damaligen 21 Seiten wurden auf Inhaltsverlust, Tabellenumbrüche, Navigation und Schriften geprüft. Seitdem enthält die Vorlage wiederholte Tabellenköpfe, interne Sprungziele sowie explizite Arial-/Consolas-Schriften. Die aktuelle Revision verwendet diese Gestaltung weiter.',
76: '2.6 Entwicklungsschritte seit 2.6.0',
77: 'Die ältere Entwicklung bis 2.6.0 bleibt im archivierten Word-Dokument und im CHANGELOG erhalten. Die folgenden Schritte erklären den heutigen Funktionsstand; historische Versionsnummern werden dabei bewusst nicht umetikettiert.',
78: '2.7 bis 2.9 – Papierkorb, Labels und Kalender; Long-Task und Zwischenüberschrift; verschachtelte Ordner mit Kreis- und Tiefenschutz. Die Datenformate wurden schrittweise bis 9 erweitert.',
79: '2.10 bis 2.11 – TXT-Rundlauf der vier Punktarten, Labeldarstellung, Papierkorb für einzelne Punkte, Bestandswächter und optionale Uhrzeit. Seit 2.11.0 gilt Datenformat 10.',
80: '2.12 bis 3.0.2 – kompaktere Eingabemaske, Label-Aufklappfeld, Kalenderknopf, Umbenennen in der Seitenleiste, Symbole sowie Drag & Drop in Gruppen. 3.1.0 vereinheitlicht Änderungen und modale Dialoge; wirkungslose Aktionen kosten keinen Rückgängig-Schritt mehr.',
81: '3.2.0 – automatische Übernahme aus früheren Programmnamen entfernt, ICONS-Tabelle bereinigt, reproduzierbarer Beispielbestand ergänzt. Datenformat 10 bleibt unverändert. Windows-/macOS-Freigaben und Release-Builds folgen als eigene Arbeit.',
82: 'Datenformat 10 ergänzt unter anderem Papierkorbeinträge für einzelne Punkte und optionale Uhrzeit. Die aktuelle App kann portable Backups 4 bis 10 lesen. Alte App-Versionen sind kein sicherer Bearbeitungsweg für neue Bestände; für einen Wechsel zuerst ein Komplettbackup erstellen. TXT überträgt keine Anhangsbinaries und ersetzt kein Komplettbackup.',
88: 'geplant; Build fehlt',90: 'geplant; Konfiguration fehlt',92:'geplant; Build fehlt',94:'geplant; Build fehlt',96:'Anforderungen bekannt; Asset fehlt',98:'Anforderungen bekannt; Asset fehlt',102:'Planungsoption; Spec fehlt',104:'offen',106:'offen',108:'offen',110:'im Code umgesetzt',112:'3.2.0 konsistent',114:'Datenmigration vorhanden; Installer ungeprüft',116:'offen',118:'Anforderungen recherchiert',120:'Sandbox und Build offen',
125: 'PyInstaller OneDir ist die vorgesehene Packaging-Basis, noch kein implementierter Buildprozess. Die spätere Build-Konfiguration muss Python und Tk bundeln, Ressourcen auflösen sowie auf beiden Zielplattformen reproduzierbar geprüft werden.',
154: 'Die Namens- und Markenlage zu Glide ist nicht freigegeben. Vor öffentlichem Branding sind Markenregister, Store-Verfügbarkeit und Domains fachlich zu prüfen. Aus einem Namensfund allein folgt keine Aussage über Zulässigkeit oder Rechte.',
187: 'Windows Win32-ICO: mindestens 16, 24, 32, 48 und 256 px gemäß Microsoft. Weitere Größen der Tabelle dienen der optischen Prüfung. Klassisches macOS-iconset: 16, 32, 128, 256 und 512 Punkte jeweils 1x/2x, also bis 1024 px; daraus entsteht .icns. Aktuelle Apple-Gestaltung und Icon Composer separat berücksichtigen. Quellen mit Abruf 04.09.2026: Store-Dokumente.',
191: 'Die Zweiteilung bleibt in 3.2.0 bestehen: persönlicher Workspace für Arbeitsmaterial und ein kanonischer Repository-Bereich. Die folgende Struktur nennt vorhandene zentrale Dateien. Die frühere Modul- und CI-Struktur war ein Zielbild und ist nicht implementiert.',
192: '''01_Repository/Glide/
├─ AGENTS.md, README.md, CHANGELOG.md, VERSION
├─ LICENSE.md, SECURITY.md
├─ src/glide/app.pyw
├─ tests/integration/
│  ├─ test_glide.py
│  ├─ test_datenintegritaet.py
│  └─ audit_app.py
├─ tests/tools/
│  ├─ screenshots.py
│  ├─ analyse_statisch.py
│  ├─ analyse_erreichbarkeit.py
│  ├─ beispieldaten.py
│  ├─ pruefen.py
│  └─ releasedaten.py
├─ tests/fixtures/
│  ├─ current_v4/ bis current_v10/
│  ├─ legacy_v2/
│  └─ beispiele/
├─ docs/
│  ├─ 00_INDEX.md
│  ├─ 01_PRODUCT_CONSTRAINTS.md
│  ├─ 02_ARCHITECTURE.md
│  ├─ 05_QA_TESTPLAN.md
│  ├─ 06_DATA_BACKUP_MIGRATION.md
│  ├─ 07_QA_BERICHT.md
│  ├─ 08_CODE_BEFUND.md
│  ├─ 09_PROJECT_HANDOFF.md
│  ├─ 09_STARTKONTEXT.md
│  ├─ 09_ARBEITSAUFTRAG_BESTANDSANALYSE.md
│  ├─ 10_RELEASE_CHECKLIST.md
│  ├─ 11_BESTANDSANALYSE.md
│  ├─ decisions/
│  ├─ exec-plans/                  Historie
│  └─ archiv/                     frühere Dokumentstände
├─ assets/                        Branding noch zu liefern
├─ packaging/                     Build-Konfiguration fehlt
├─ scripts/                       vorbereitete Prozessbereiche
└─ requirements/                  getrennte Laufzeit-/Buildbereiche

Keine Modulzerlegung und keine neue CI-Konfiguration beauftragt.
Finale Binärartefakte gehören nach 30_Release_Exports/<Version>/.
Historische Dateien bleiben in dezentralen Archiv-Unterordnern.''',
200:'generierter Cache, kein Source; historische Funde bleiben archiviert',202:'aktuelle 3.2.0-Beispielbackups; ältere TXT-/JSON-Dateien im Archiv',207:'Dezentrale Archive',208:'im jeweiligen Ordner; 100_Archiv ist kein aktiver Bereich',212:'Der Monolith bleibt erhalten. Source 3.2.0 und die aktuelle Einzeldatei sind bytegleich. Eine Modulzerlegung ist nicht beauftragt; das nächste Arbeitspaket richtet sich auf reale Plattform-QA und reproduzierbares Packaging.',
325:'C01–C08 bleiben wiederverwendbare Ticketvorlagen. Sie sind Dokumentinhalt und führen keine Arbeit automatisch aus. C01 ist in docs/11_BESTANDSANALYSE.md für 3.2.0 nachgeführt; C02/C03 sind teilweise umgesetzt. Asset-, Build- und Signing-Arbeiten benötigen die jeweiligen Produktentscheidungen und Arbeitsaufträge.',
326:'C01 – Repository Audit (Stand 3.2.0 dokumentiert)',
338:'C07 – QA (drei Suiten vorhanden; Release-QA offen)',
343:'Verbindlich ist 01_Repository/Glide/AGENTS.md. Der folgende Auszug fasst die aktuellen Regeln zusammen. Er ersetzt die Quelldatei nicht und enthält keine zusätzlichen Arbeitsaufträge.',
344:'''# Glide – Arbeitsregeln für den aktuellen Bestand

Produkt: lokale Desktop-App, ohne Konto, Cloud oder Telemetrie.
Kanonischer Source: src/glide/app.pyw; Version 3.2.0, Schema 10.

Verbindliche Dokumente
- docs/01_PRODUCT_CONSTRAINTS.md
- docs/02_ARCHITECTURE.md
- docs/05_QA_TESTPLAN.md
- docs/06_DATA_BACKUP_MIGRATION.md
- docs/07_QA_BERICHT.md
- docs/10_RELEASE_CHECKLIST.md
- docs/decisions/PRODUCT_IDENTITY.md

Entwicklungsregeln
1. Vor Änderungen aktuellen Teststand und Datenpfade prüfen.
2. GLIDE_DATA_DIR vor jedem Testimport auf isolierten Ordner setzen.
3. Bestehende Funktionen, Nutzerdaten und Migrationen bewahren.
4. Keine neue Laufzeitabhängigkeit ohne dokumentierte Entscheidung.
5. Keine Datenformatänderung ohne eigene Migration, Sicherung und Tests.
6. Punkte über item_change, Listen und Ordner über sidebar_change ändern.
7. Umbauaktionen zusätzlich unter guarded_structural_change ausführen.
8. Modale Dialoge ausschließlich über run_modal führen.
9. Oberflächensymbole in ICONS zentralisieren; Rest-Ausnahmen dokumentieren.
10. Überholte Dokumente vor dem Ändern versionsbezogen archivieren.
11. Änderungen in CHANGELOG und betroffenen Dokumenten nachführen.
12. Keine Secrets, Zertifikate oder Schlüssel ins Repository.

Abschluss
Syntaxprüfung und passende automatisierte Tests müssen bestehen.
Versionen müssen übereinstimmen.
Verbleibende manuelle Prüfungen ausdrücklich nennen.

Aktueller Auftrag
Keine Datei löschen. Keine automatische Versionserhöhung oder Commits.
Den Monolithen und die drei linearen Testsuiten nicht umstrukturieren.
Inhaberentscheidungen und vermutete Fehler nicht als erledigt ausgeben.''',
354:'Monolith, Datenmodell und Datenfluss',355:'07_QA_BERICHT.md',356:'aktueller Laufstand und verbleibende Prüfungen',357:'08_CODE_BEFUND.md',358:'statische Befunde und Maßnahmen',363:'09_PROJECT_HANDOFF.md',364:'Einstieg, Architektur und Übergabe',365:'09_STARTKONTEXT.md',366:'kompakter Startkontext',367:'11_BESTANDSANALYSE.md',368:'Befund, Maßnahmen, Prozesse und Grenzen',
379:'''# Produktgrenzen

Glide ist eine lokale Desktop-App für Windows und macOS.
Deutsch ist die einzige Oberflächensprache.
Die Kernfunktionen benötigen kein Internet und kein Benutzerkonto.
Glide selbst überträgt keine Nutzerdaten.

Laufzeit: Python-Standardbibliothek und Tk.
Neue Laufzeitabhängigkeiten benötigen eine dokumentierte Entscheidung.
Buildtools zählen nicht zur Laufzeit der Anwendung.

Bewusste Nicht-Ziele
- Cloud-Synchronisierung und Mehrbenutzerbetrieb
- Benutzerkonten, Lizenzserver und Telemetrie
- Push-Infrastruktur und externe Kalender-/Mailanbindung
- Mehrsprachigkeit und Rich-Text-Editor

Datenkompatibilität hat Vorrang vor internem Refactoring.
Maßgeblich ist docs/01_PRODUCT_CONSTRAINTS.md.''',
381:'Die verbindlichen Stammdaten werden zentral im Repository geführt. Die externe Liste Offene_Entscheidungen_3.2.0.md ist eine Arbeitsansicht desselben Registers, kein zweiter Ort für verbindliche Identitäten.',
382:'01_Repository/Glide/docs/decisions/PRODUCT_IDENTITY.md',
383:'''Produktname: Glide
Langname: Glide – Aufgaben und Listen
App-Version: 3.2.0
Datenformat: 10
Lesbare portable Backups: 4 bis 10
Status: interne Vorabversion, kein öffentliches Release

Offen: Publisher, Copyright, Supportkontakt, Website,
Datenschutz-URL, Lizenzmodell und Preis.
Windows: Architektur, Mindestversion, AppUserModelID, AppId.
macOS: Bundle Identifier, Mindestversion, Architektur, Vertriebsweg.
Kennungen erst nach Inhaberentscheidung dauerhaft festlegen.''',
391:'Drei lineare Python-Suiten prüfen Glide mit isolierten temporären Daten. Hauptsuite, Datenintegritätssuite und appweiter Audit bleiben einzeln aufrufbar. Das Prüfwerkzeug tests/tools/pruefen.py bündelt Syntax, Versionen, Suiten und Analysen. Der aktuelle QA-Bericht dokumentiert konkrete Laufzeit, Ergebnisse und übersprungene Schritte; manuelle Plattform- und Buildtests bleiben separat.',
392:'''tests/
├─ integration/test_glide.py
├─ integration/test_datenintegritaet.py
├─ integration/audit_app.py
├─ tools/pruefen.py               Schnell- und Vollprüfung
├─ tools/screenshots.py           visuelle Nachweise
├─ tools/analyse_statisch.py
├─ tools/analyse_erreichbarkeit.py
└─ fixtures/                     Schema 4–10, Legacy 2, Beispiele''',
393:'Nachweis 04.09.2026: Windows-Prüfung mit Python 3.12.12 und Tk 8.6.17. Die drei bestehenden Suiten bestanden nach begrenzten Anpassungen im Testcode für aktuelle Widgets und native Geometrie. App-Code und Datenformat blieben unverändert. Endgültiger Gesamtlauf einschließlich Release-Fixture: siehe docs/07_QA_BERICHT.md.',
463:'Referenzdaten liegen für die Formate 4 bis 10 sowie Legacy 2 vor und werden vom Integrationstest geladen und normalisiert. Das Beispiel-Komplettbackup und die Release-Arbeitslisten sind über Werkzeuge reproduzierbar. Ein Komplettbackup ersetzt beim Laden den gesamten Bestand; ein TXT-Listenimport ergänzt eine einzelne Liste.',
464:'''tests/fixtures/
├─ current_v4/ bis current_v10/   ein Referenzbestand je Schema
├─ legacy_v2/                    historischer Aufgabenbestand
└─ beispiele/                    portable .glidebackup-Beispiele

tests/tools/beispieldaten.py      erzeugt Funktionsbeispiele
tests/tools/releasedaten.py       erzeugt drei Release-Arbeitslisten
90_Testdaten_Extern/              unveränderte historische TXT-Eingaben''',
465:'Format 10 umfasst vier Punktarten, Labels, verschachtelte Ordner, Papierkorb und Uhrzeit. Zwei isoliert belegte Release-Blocker bleiben offen: Ein Systemlabel kann die Grenze auf 21 Labels überschreiten; make_subitem kann Tiefe 101 erzeugen, die später beim Laden abgewiesen wird. App-Code unverändert; gezielte Behebung und Regression erforderlich. Alte Fixtures bleiben historische Schemareferenzen.',
467:'Finale Veröffentlichungen gehören nach 30_Release_Exports/<VERSION>/. Für Source 3.2.0 existiert noch kein freigegebener EXE-, Installer-, App- oder DMG-Build. Ältere Ablagepläne bleiben historische Vorbereitung. Das folgende Ablageschema ist ein Zielbild, kein vorhandenes Release-Manifest.',
490:'Der Source 3.2.0 ist im kanonischen Repository-Pfad vorhanden und bytegleich zur aktuellen Einzeldatei unter 07_Python-Versionen. Ältere Source-Fassungen, Word-Dokumente und Checklisten bleiben unverändert archiviert. Die Archivzuordnung dieser Revision steht in der Bestandsanalyse.',
491:'Glide 3.2.0 · Source-SHA-256: 6309f2669f549077…2e3cd4bfc01715',
506:'Datenformat 10 ist bereits festgelegt; keine offene Geschäftsentscheidung',
511:'Vorhandene Referenzen decken alte Schemata und typische Grenzfälle ab. Beispiele werden aus lesbarem Quelltext erzeugt und als .glidebackup validiert. Bei Änderung des Erzeugers die Datei neu bauen und testen; Fälligkeiten werden am Erzeugungstag berechnet.',
513:'''AGENTS.md und docs/00_INDEX.md       verbindliche Einstiege
docs/02_ARCHITECTURE.md             Version 3.2.0 / Schema 10
docs/05_QA_TESTPLAN.md               Prüfprozess
docs/06_DATA_BACKUP_MIGRATION.md     Formate, Speicherung, Import
docs/07_QA_BERICHT.md                aktueller Nachweis
docs/08_CODE_BEFUND.md               bekannte Befunde
docs/09_PROJECT_HANDOFF.md           Übergabe
docs/10_RELEASE_CHECKLIST.md         offene Release-Gates
docs/11_BESTANDSANALYSE.md           Konsolidierung und Ergebnisse
docs/decisions/PRODUCT_IDENTITY.md   Identitäten und offene Entscheidungen
docs/exec-plans/ und docs/archiv/    unveränderte Historie''',
515:'Store-Screenshots erst vom Release-Kandidaten auf dem jeweiligen Zielsystem erstellen. Mac: 1–10 PNG/JPEG ohne Alpha, 1280×800, 1440×900, 2560×1600 oder 2880×1800. Microsoft MSI/EXE: 1–10, mindestens vier empfohlen; Pixelvorgaben dieser Route sind in der aktuellen Quelle nicht genannt. Quellen und Abrufdatum 04.09.2026 in 40_Store_Material.',
522:'Source 3.2.0, Beispiele und Dokumentation vorhanden; Identität und Branding offen',
525:'Bestandsanalyse 3.2.0 vorhanden; Grenzen und Nachtests getrennt dokumentiert',
528:'Struktur, Regeln, Doku und drei Suiten vorhanden; keine Modulzerlegung beauftragt',
540:'automatisierte Windows-Prüfung vorhanden; Geräte-, DPI-, macOS- und Clean-Machine-Freigabe offen',
549:'Vertriebsweg durch Inhaber festlegen; Store-Vorgaben und Sandbox anhand des Builds prüfen',
552:'Prüfprozess gebündelt; Build, Signing und Veröffentlichung noch nicht automatisiert',
563:'Glide 3.2.0 ist als Source und Dokumentation konsolidiert. Die App enthält vier Punktarten, Labels, Papierkorb, Kalender und Datenformat 10. Drei automatisierte Suiten und reproduzierbare Beispiele unterstützen die Prüfung. Ein öffentlicher Release ist weiterhin von Plattformfreigabe, Produktidentität, Branding, Packaging und Signing abhängig.',
564:'Empfohlene Reihenfolge für die nächsten Arbeiten:',
565:'1. Den Stand 3.2.0 mit einer Kopie realer Daten in GLIDE_DATA_DIR prüfen; Originaldaten unverändert lassen.',
566:'2. Windows-/macOS-Dialoge, Mehrfachauswahl, DPI, Symbole und die gemeldete Einfrierstörung gezielt manuell prüfen.',
573:'9. Den Bestandswächter und Rückgängig-Rahmen bei weiteren Änderungen beibehalten; keine unbeauftragte Modulzerlegung.',
575:'Nach der Bestandsanalyse zuerst die manuelle Plattformprüfung durchführen und Produktidentitäten festlegen. Danach einen reproduzierbaren unsigned Build samt Smoke-Test erstellen. Signing, Stores und Veröffentlichung bleiben weitere Arbeitsschritte mit eigenen Nachweisen.',
578:'Arbeitskontext und Bestandsanalyse-Auftrag vom 04.09.2026; historische Screenshots und Tickettexte bleiben als solche erkennbar.',
579:'Kanonischer Source src/glide/app.pyw, Version 3.2.0 und Datenformat 10; frühere Releases anhand des unveränderten CHANGELOG und der Archive.',
580:'Lokaler Workspace und drei Testsuiten unter tests/integration; Prüfprozess und abschließende Ergebnisse in docs/07_QA_BERICHT.md und docs/11_BESTANDSANALYSE.md.',
583:'Externe Referenzen aus der Vorlage bleiben erhalten. Aktuell recherchierte Store-Spezifikationen mit Abruf 04.09.2026 stehen in 40_Store_Material/Microsoft/Store_Angaben_Microsoft.md und Apple/Store_Angaben_Apple.md. Die nachfolgenden allgemeinen Links sind historische Quellen, keine Freigaben.',
601:'Prüfstand 04.09.2026: App 3.2.0, Datenformat 10, portable Backups 4 bis 10. Der aktuelle Gesamtlauf ist im QA-Bericht belegt. Manuelle Plattformprüfung, Einfrier-Reproduktion, Installer, Signing, Store-Einreichung und Clean-Machine-Prüfung bleiben offen. Die ältere Dokumentfassung 2.6.0 ist unverändert archiviert.',
}
for i,t in revisions.items(): replace(i,t)

# Correct two actual pagination defects found in final2: a one-item split at
# the start of chapter 4 and a stranded first line of the constraints block.
for index, tag in [(126,'pageBreakBefore'),(378,'keepNext'),(379,'keepLines')]:
    prop = ps[index].find(W+'pPr')
    if prop is None:
        prop=ET.Element(W+'pPr');ps[index].insert(0,prop)
    setting=prop.find(W+tag)
    if setting is None:setting=ET.SubElement(prop,W+tag)
    setting.set(W+'val','1')

# Keep reference visual vocabulary. The retained user document controls colors,
# callouts, page furniture and font sizes; no generic restyling is performed.
# Update footer dates only; all page fields and relationships stay intact.
changed = {'word/document.xml':ET.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)}
for name,raw in parts.items():
    if name.startswith('word/footer') and b'01.09.2026' in raw:
        changed[name]=raw.replace(b'01.09.2026',b'04.09.2026')
core = ET.fromstring(parts['docProps/core.xml'])
for e in core:
    if ET.QName(e).localname == 'modified': e.text='2026-09-04T12:00:00Z'
changed['docProps/core.xml']=ET.tostring(core,xml_declaration=True,encoding='UTF-8',standalone=True)

# Navigation page numbers are filled after Word exports the final layout.
pages_path=QA/'bookmark_pages.json'
if pages_path.exists():
    pages=json.loads(pages_path.read_text(encoding='utf-8-sig'))
    for h in root.findall('.//w:hyperlink',ns):
        anchor=h.get(W+'anchor')
        if anchor in pages:
            texts=h.findall('.//w:t',ns)
            if texts and (texts[-1].text or '').isdigit(): texts[-1].text=str(pages[anchor])
    changed['word/document.xml']=ET.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)

with ZipFile(out,'w') as z:
    for info in infos:z.writestr(info,changed.get(info.filename,parts[info.filename]))
with ZipFile(out) as z:
    assert set(z.namelist())==set(parts)
    for name,raw in parts.items():
        if name not in changed:assert z.read(name)==raw,name
manifest = {'reference':str(reference),'reference_sha256':hashlib.sha256(reference.read_bytes()).hexdigest(),'output':str(out),'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'changed_parts':list(changed),'preserved_parts':[n for n in parts if n not in changed],'edited_paragraphs':list(revisions)}
(QA/'docx_revision_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(out)
