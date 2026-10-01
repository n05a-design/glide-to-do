"""One reviewed, non-destructive consolidation of external Glide 3.2 documents."""
from pathlib import Path
import hashlib
import json
import re
import shutil

ROOT = Path(r'C:\Users\vontrostorff\OneDrive\Glide ToDo').resolve()
QA = Path(__file__).resolve().parent
ledger_path = QA / 'external_archive_manifest.json'
ledger = json.loads(ledger_path.read_text(encoding='utf-8')) if ledger_path.exists() else []

def checked(p):
    p = Path(p).resolve()
    if p != ROOT and ROOT not in p.parents:
        raise ValueError(p)
    return p

def preserve(p, move=False):
    p = checked(p)
    dest = checked(p.parent / 'Archiv' / (p.stem + '_vor_Konsolidierung_2026-09-04' + p.suffix))
    dest.parent.mkdir(exist_ok=True)
    if dest.exists():
        if any(x['source'] == str(p.relative_to(ROOT)) for x in ledger):
            return
        raise FileExistsError(dest)
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    if move:
        shutil.move(p, dest)
    else:
        shutil.copy2(p, dest)
    assert hashlib.sha256(dest.read_bytes()).hexdigest() == digest
    ledger.append({'source': str(p.relative_to(ROOT)), 'archive': str(dest.relative_to(ROOT)), 'sha256': digest, 'action': 'move' if move else 'copy', 'reason': 'Vorgänger vor sachlicher Konsolidierung auf App 3.2.0 und Datenformat 10 erhalten'})
    (QA / 'external_archive_manifest.json').write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding='utf-8')

def write(rel, text):
    p = checked(ROOT / rel)
    if p.exists():
        if p.read_text(encoding='utf-8-sig') == text:
            return
        preserve(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')

def edit(rel, pairs):
    s = (ROOT / rel).read_text(encoding='utf-8-sig')
    for old, new in pairs:
        if old not in s:
            if new in s:
                continue
            raise ValueError(f'Missing replacement {rel}: {old}')
        s = s.replace(old, new)
    write(rel, s)

# Historical version-labelled files move intact into each direct parent's archive.
for rel in [
    '00_Arbeitsvorbereitung/Entscheidungen/Offene_Entscheidungen_2.6.0.md',
    '00_Arbeitsvorbereitung/Entscheidungen/Offene_Entscheidungen_2.11.0.md',
    '00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_2.6.0.md',
    '00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_2.11.0.md',
    '00_Arbeitsvorbereitung/Notizen/Technische_Fakten_2.6.0.md',
    '00_Arbeitsvorbereitung/Notizen/Technische_Fakten_2.11.0.md',
    '40_Store_Material/Produktdatenblatt_2.6.0.md',
]:
    preserve(ROOT / rel, move=True)

write('00_Arbeitsvorbereitung/Entscheidungen/Offene_Entscheidungen_3.2.0.md', '''# Offene Entscheidungen für Glide 3.2.0

Stand: 04.09.2026 · App-Version 3.2.0 · Datenformat 10

Verbindliches Register: `../../01_Repository/Glide/docs/decisions/PRODUCT_IDENTITY.md`.
Die Angaben unten sind offen; ein Vorschlag ist keine Freigabe. Build, Signing,
manuelle Plattformprüfung und Store-Unterlagen fehlen zusätzlich als Arbeitsleistung.

| Entscheidung | Konkret festzulegen |
|---|---|
| Windows-Zielarchitektur | x64, ARM64 oder mehrere; an Testgeräten und gewählter Python-/Build-Kette prüfen |
| Windows-Mindestversion | Zielsysteme verbindlich nach realem Buildtest festlegen |
| Inno Setup AppId | dauerhafte Installationsidentität, sobald Inno Setup verbindlich gewählt ist |
| Windows AppUserModelID | dauerhafte Shell-Identität auf Basis der Produkt- und Publisherentscheidung |
| macOS Bundle Identifier | dauerhaft eindeutiger Reverse-DNS-Bezeichner |
| macOS Mindestversion und Architektur | Intel, Apple Silicon oder Universal 2 an Laufzeit und Testgeräten prüfen |
| macOS Vertriebsweg | Direktverteilung, Mac App Store oder beides; Sandbox und Datenpfade separat testen |
| Windows Vertriebsweg | Direktdownload, Microsoft Store oder beides; MSI/EXE und MSIX haben unterschiedliche Anforderungen |
| Publisher und Copyright | rechtlich verantwortliche, öffentlich sichtbare Angaben |
| Support und Website | erreichbare Support-URL und Kontakt, eigener Webauftritt |
| Datenschutz-URL | öffentlich erreichbare Erklärung zur lokalen Verarbeitung und fehlenden Übertragung |
| Preis und Lizenzmodell | kostenlos, Einmalkauf oder anderes Modell; Auswirkungen auf Vertrieb und Pflege bewerten |
| Sicherheitskontakt | Adresse für Meldungen in `SECURITY.md` |
| Marke und Name Glide | Namens-/Markenlage fachlich prüfen und Produktname freigeben |
| Lizenztext | Platzhalter in `LICENSE.md` durch freigegebene Bedingungen ersetzen |

## Bereits aus dem Code bekannt

Lokale Desktop-App, Deutsch, Python-Standardbibliothek plus Tk, kein Konto und
keine Netzwerkkommunikation durch Glide. Datenformat 10; portable Backups der
Formate 4 bis 10 werden unterstützt. `GLIDE_DATA_DIR` isoliert Tests auf allen
Plattformen. Automatische Übernahme aus früheren Programmnamen entfällt seit 3.2.0.

## Weiterhin zu prüfen

Die automatisierte Prüfung ersetzt keine Gerätefreigabe. Den aktuellen Laufstand
enthält `../../01_Repository/Glide/docs/07_QA_BERICHT.md`; manuelle Aufgaben stehen
in `../Checklisten/Manuelle_Pruefung_3.2.0.md`. Das gemeldete Einfrieren wurde nie
reproduziert; die überarbeitete Dialog-Griffrückgabe ist deshalb noch kein Beleg
für eine vollständige Fehlerbehebung. Altersfreigabe, Barrierefreiheit und
Systemanforderungen werden erst anhand der tatsächlichen Fragebögen bzw. Builds freigegeben.

Aktuelle Texte und recherchierte Plattformanforderungen:
`../../40_Store_Material/Produktdatenblatt_3.2.0.md`,
`../../40_Store_Material/Microsoft/Store_Angaben_Microsoft.md`,
`../../40_Store_Material/Apple/Store_Angaben_Apple.md`.
''')

edit('00_Arbeitsvorbereitung/Notizen/Technische_Fakten_3.2.0.md', [
('Jede Zeile\nist aus dem Quellcode belegt; nichts hier ist geschätzt.', 'Codefakten und Prüfgrenzen sind getrennt. Der aktuelle Testlauf steht im\nRepository unter `docs/07_QA_BERICHT.md`.'),
('| Getestet mit | Python 3.12, Tk 8.6 |', '| Referenzlaufzeit | Python 3.12, Tk 8.6; aktueller Plattformlauf siehe QA-Bericht |'),
('Austausch, **verlustfrei reimportierbar**', 'struktureller Austausch; keine Anhangsbinaries, kein vollständiges Backup'),
('Seit 2.10.0 überstehen alle vier Arten den TXT-Rundlauf, einschließlich', 'Seit 2.10.0 überstehen alle vier Arten den getesteten TXT-Rundlauf, einschließlich'),
('`run_modal` gibt den Tastatur- und Mausgriff an das\naufrufende Fenster zurück. Das war die Ursache eines gemeldeten Einfrierens –\n**auf Windows noch nicht bestätigt.**', '`run_modal` gibt den Tastatur- und Mausgriff an das\naufrufende Fenster zurück. Damit wurde ein plausibler Fehlerpfad entschärft.\nDas gemeldete Einfrieren wurde nie reproduziert; eine vollständige Behebung ist\n**NICHT VERIFIZIERT**.'),
('Belegt: vollständige Tastaturbedienung, Kontrast der Label-Chips über 4,5:1', 'Implementiert: zahlreiche Tastenkürzel. Automatisiert geprüft: Kontrast der Label-Chips über 4,5:1'),
('**Nicht belegt:** Screenreader-Unterstützung – ungeprüft.', '**Nicht belegt:** vollständige Bedienbarkeit ohne Maus und Screenreader-Unterstützung; manuelle Prüfung offen.'),
('- „Alle Daten bleiben auf dem Gerät.“', '- „Glide speichert lokal und überträgt selbst keine Daten.“'),
('- „Vollständig mit der Tastatur bedienbar.“', '- „Mit zahlreichen Tastenkürzeln bedienbar.“'),
('- „Keine Umbauaktion kann einen Punkt verlieren; die App prüft das nach jedem Schritt selbst.“', '- „Ein Bestandswächter prüft Umbauaktionen auf verlorene Punkt-IDs und stellt bei erkanntem Verlust den Vorzustand her.“'),
])
edit('00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.2.0.md', [
('### Das gemeldete Einfrieren (3.0.1, Ursache in 3.1.0 behoben)', '### Das gemeldete Einfrieren (3.0.1, Griffrückgabe seit 3.1.0 überarbeitet)'),
('**Der wichtigste Punkt dieser Runde.** Die Ursache ist gefunden und beseitigt –\nmodale Unterdialoge gaben den Tastatur- und Mausgriff nicht an das aufrufende\nFenster zurück. **Reproduzieren ließ sich der Fehler nie**, deshalb kann nur die\nBenutzung auf Windows bestätigen, dass es die einzige Ursache war.', '**Der wichtigste Punkt dieser Runde.** Die Griffrückgabe modaler Dialoge wurde\nüberarbeitet. Das ist eine Maßnahme gegen einen plausiblen Fehlerpfad.\n**Reproduzieren ließ sich die gemeldete Störung nie**; die vollständige Behebung\nist NICHT VERIFIZIERT. Erforderlich sind reproduzierbare Dialogfolgen und Dauerbenutzung.'),
('Hell und Dunkel folgen der Systemeinstellung', 'Hell und Dunkel über den Themenschalter wechseln; automatisches Folgen der Systemeinstellung nicht als zugesicherte Funktion voraussetzen'),
('**Diese beiden sind noch Emoji**', '**Gruppenmarker und höchste Wichtigkeitsstufe verwenden noch Emoji**'),
])

edit('40_Store_Material/Produktdatenblatt_3.2.0.md', [
('Alle Angaben in diesem Dokument sind aus dem Quellcode belegt. Sie sind die', 'Der Funktionskatalog ist aus dem Quellcode abgeleitet. Entwürfe, Vorschläge und\nnoch offene Prüfungen sind gekennzeichnet. Die Angaben sind die'),
('verschachtelte Listen', 'Listen mit verschachtelten Aufgaben'),
('beliebig viele Dateianhänge', 'mehrere Dateianhänge innerhalb der technischen Grenzen'),
('| Betriebssystem | Windows 10 oder 11 | *offen, Empfehlung macOS 12 oder neuer* |', '| Betriebssystem | Mindestversion nach Buildtest festzulegen | Mindestversion nach Buildtest festzulegen |'),
('| Architektur | *offen, Empfehlung x64* | *offen, Empfehlung Universal 2* |', '| Architektur | offen; x64/ARM64 zu entscheiden | offen; Intel/Apple Silicon/Universal 2 zu entscheiden |'),
('| Laufzeit | in der App enthalten | in der App enthalten |', '| Laufzeit | Source benötigt Python und Tk; gebündelter Build geplant | Source benötigt Python und Tk; gebündelter Build geplant |'),
('**Noch nicht bestätigt:** Alle automatisierten Prüfungen liefen unter Linux mit\nTk 8.6.', '**Prüfgrenze:** Der frühere Referenzlauf erfolgte unter Linux mit Tk 8.6.\nDen aktuellen Windows-Prüflauf dokumentiert `../01_Repository/Glide/docs/07_QA_BERICHT.md`.'),
('| Erhebt die App personenbezogene Daten? | Nein |', '| Übermittelt Glide personenbezogene Daten an den Anbieter? | Nein; eingegebene Inhalte werden lokal verarbeitet |'),
('| Zugriff auf Dateien | Nur auf Dateien, die der Nutzer über den Dateidialog selbst auswählt |', '| Zugriff auf Dateien | Eigene Nutzdaten automatisch; externe Anhänge, Importe und Exporte nach Nutzeraktion |'),
('| Datenlöschung | Löschen des App-Datenordners entfernt alle Daten |', '| Datenlöschung | App-Datenordner enthält den internen Bestand; separat exportierte Backups und Dateien bleiben erhalten |'),
('Dateizugriffe erfolgen ausschließlich über den\nSystem-Dateidialog nach Nutzeraktion.', 'Glide liest und schreibt seinen Datenordner selbstständig, etwa beim Start,\nSpeichern und Autosave. Externe Dateien werden nach Nutzeraktion verarbeitet.\nEin vom Nutzer gewählter synchronisierter Ordner kann Daten außerhalb von Glide übertragen.'),
('| Altersfreigabe | ohne Altersbeschränkung | kein nutzergenerierter Austausch, kein Netzwerk, keine Werbung, keine Käufe |', '| Altersfreigabe | offen bis Plattformfragebogen | Einstufung wird vom jeweiligen Verfahren ermittelt |'),
('| Barrierefreiheit | Tastaturbedienung vollständig, Kontraste in beiden Modi geprüft | Screenreader-Unterstützung nicht geprüft |', '| Barrierefreiheit | Tastenkürzel vorhanden, Labelkontraste automatisiert geprüft | vollständiger Tastaturweg und Screenreader ungeprüft |'),
('Auflösungen richten sich nach den Store-Vorgaben; die App liefert bei\n1000 × 800 Pixeln eine vollständige Ansicht.', 'Recherchierte Anforderungen einschließlich Abrufdatum stehen in den\nMicrosoft- und Apple-Dokumenten dieses Ordners. Die Standardfenstergröße der\nApp ist kein Nachweis eines gültigen Store-Screenshots.'),
])

write('00_Arbeitsvorbereitung/README.md', '''# Arbeitsvorbereitung

Stand: 04.09.2026 · Glide 3.2.0 · Datenformat 10

Vorbereitung für Entscheidungen, Recherche, Checklisten und Notizen. Der
kanonische Source liegt unter `../01_Repository/Glide/`; diese Unterlagen
ersetzen weder Code noch den aktuellen QA-Bericht.

| Inhalt | Aktuelle Datei |
|---|---|
| Inhaberentscheidungen | [Offene Entscheidungen](Entscheidungen/Offene_Entscheidungen_3.2.0.md) |
| Manuelle Tests | [Prüfliste](Checklisten/Manuelle_Pruefung_3.2.0.md) |
| Importierbare Zusatzliste | [Veröffentlichungscheckliste](Checklisten/Glide_Veroeffentlichung_Checkliste.txt) |
| Codefakten und Grenzen | [Technische Fakten](Notizen/Technische_Fakten_3.2.0.md) |
| Arbeitsgrundlage als Word | [Dokumentation](../10_Dokumentation/README.md) |

Die früheren Fassungen 2.6.0 und 2.11.0 liegen unverändert im `Archiv/` ihres
jeweiligen direkten Ordners. Jede Fortschreibung erhält vorab eine Archivkopie.

Glide 3.2.0 enthält vier Punktarten, verschachtelte Ordner, Labels, Papierkorb,
Kalender, optionale Uhrzeiten und den Bestandswächter. Seit 3.1.0 bündeln
`item_change`, `sidebar_change` und `run_modal` Änderungen und Dialoge. Seit
3.2.0 entfällt die automatische Übernahme aus früheren Programmnamen.

Release-Hürden bleiben Branding, Build/Installer, Signaturen, Identitäten,
Lizenz und reale Plattformtests. Die Griffrückgabe modaler Dialoge wurde
überarbeitet; das gemeldete Einfrieren ist mangels Reproduktion weiterhin
NICHT VERIFIZIERT. Emoji-Ausnahmen für Gruppe und höchste Wichtigkeit bleiben
für Windows-/macOS-Schriftprüfung relevant.

Aktuelle Nachweise: [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md),
[Release-Checkliste](../01_Repository/Glide/docs/10_RELEASE_CHECKLIST.md),
[Produktidentität](../01_Repository/Glide/docs/decisions/PRODUCT_IDENTITY.md),
[Bestandsanalyse](../01_Repository/Glide/docs/11_BESTANDSANALYSE.md).
''')
write('40_Store_Material/README.md', '''# Store-Material

Stand: 04.09.2026 · Glide 3.2.0 · Datenformat 10

- [Produktdatenblatt](Produktdatenblatt_3.2.0.md): tatsächlicher Funktionsumfang,
  Datenpfade, Grenzen und redaktionelle Textentwürfe.
- [Microsoft](Microsoft/Store_Angaben_Microsoft.md): Win32-Einreichung als MSI/EXE,
  Pflichtmaterial und recherchierte Quellen.
- [Apple](Apple/Store_Angaben_Apple.md): App Store Connect sowie getrennte
  Anforderungen an Direktverteilung und Mac App Store.

Alle Texte sind Entwürfe. Mindestbetriebssysteme und gebündelte Laufzeit sind
ohne Release-Build nicht zugesichert. Altersfreigabe und Barrierefreiheit sind
keine allein aus dem Code ableitbaren Freigaben. Die Store-Dokumente nennen
Quellen und Abrufdatum; vor Einreichung erneut prüfen.

Offene Inhaberentscheidungen stehen in
[Offene Entscheidungen 3.2.0](../00_Arbeitsvorbereitung/Entscheidungen/Offene_Entscheidungen_3.2.0.md).
Vorgänger liegen unverändert in den jeweiligen `Archiv/`-Unterordnern.
''')
edit('20_Grafik_Master/README.md', [('## Stand 01.09.2026', '## Stand 04.09.2026 · Glide 3.2.0'), ('Kapitel 5.', 'Kapitel 5. Aktuelle Plattformquellen stehen außerdem unter\n`../40_Store_Material/Microsoft/Store_Angaben_Microsoft.md` und\n`../40_Store_Material/Apple/Store_Angaben_Apple.md`.')])
edit('90_Testdaten_Extern/README.md', [('aktuell für die Datenformate 6, 5, 4\n  und 2.', 'für die Datenformate 4 bis 10 sowie Legacy 2.'), ('und trägt `2.6.0` im Namen.', 'als `Glide-Funktionsvorschau_3.2.0.glidebackup`.'), ('## Stand 01.09.2026', '## Stand 04.09.2026 · aktueller App-Stand 3.2.0')])
edit('50_Ablage/README.md', [('enthält freigegebene Word-/PDF-Dokumentation.', 'enthält die aktuelle Word-Arbeitsgrundlage und ihre historischen Fassungen.'), ('## Stand 01.09.2026', '## Historischer QA-Bestand und Stand 04.09.2026'), ('Nach einer Verschiebung muss es neu erzeugt werden, sonst\nverweist es auf Pfade, die es nicht mehr gibt.', 'Nach einer Verschiebung muss es neu erzeugt werden, sonst\nverweist es auf Pfade, die es nicht mehr gibt. Der neue Dokumentlauf liegt unter\n`QA/Dokumentation/Renderlaeufe/3.2.0_2026-09-04/`; alte Renderläufe bleiben\nunverändert als historische Nachweise erhalten.')])
write('10_Dokumentation/README.md', '''# Dokumentation

Stand: 04.09.2026 · Glide 3.2.0 · Datenformat 10

Aktuelle Arbeitsgrundlage:
[Glide Arbeitsvorbereitung Build und Release 3.2.0](<3.2.0 – Glide_Arbeitsvorbereitung_Codex_Build_Release_Plan.docx>).
Sie führt die bestehende Word-Struktur fort und trennt erreichten Code-Stand,
historische Referenzen, offene Arbeit und Inhaberentscheidungen.

Vorgänger sind in `Archiv/` erhalten. Der aktuelle Änderungsverlauf wird
zentral in [CHANGELOG.md](../01_Repository/Glide/CHANGELOG.md) gepflegt;
Versionsprotokolle im Archiv sind historische Einzeldokumente.

Codefakten: [Dokumentationsindex](../01_Repository/Glide/docs/00_INDEX.md).
Prüfstand: [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md).
''')

# The TXT remains a non-destructive additional-list import. Dates in its old
# one-off planning example are removed; current generated release data uses relative dates.
rel = '00_Arbeitsvorbereitung/Checklisten/Glide_Veroeffentlichung_Checkliste.txt'
s = (ROOT / rel).read_text(encoding='utf-8-sig')
s = re.sub(r'^\s+Fällig: .*\n', '', s, flags=re.M)
s = s.replace('2.11.0', '3.2.0').replace('Datenformat 9, Backups der Formate 4 bis 9 lesbar', 'Datenformat 10, Backups der Formate 4 bis 10 lesbar')
s = s.replace('✓ Kategorie Produktivität, ohne Altersbeschränkung', 'Altersfreigabe im aktuellen Plattformfragebogen ermitteln')
s = s.replace('✓ Integrationstest und app-weiter Durchlauf grün', 'Aktuellen Lauf aller drei Testsuiten anhand des QA-Berichts prüfen')
s = s.replace('✓ Store-Texte vollständig entworfen', 'Store-Texte anhand des Produktdatenblatts 3.2.0 freigeben')
s = s.replace('Der Name wird von mehreren Softwareanbietern genutzt.', 'Die Verfügbarkeit des Namens ist noch nicht freigegeben.')
s = s.replace('Ein Abo widerspricht der Produktphilosophie – kein Konto, kein Server, keine Lizenzprüfung – und würde Infrastruktur erzwingen, die es bewusst nicht gibt. Bleiben kostenlos oder einmaliger Kaufpreis.', 'Kostenlos, Einmalkauf und andere Vertriebsmodelle abwägen. In Glide gibt es derzeit kein Konto, keinen Lizenzserver und keine integrierte Kaufabwicklung; daraus folgt noch keine Preisentscheidung.')
s = s.replace('Pflichtfeld in beiden Stores, auch ohne Datenerhebung.', 'Öffentliche Datenschutzinformation vorbereiten und Anforderungen des gewählten Stores prüfen.')
s = s.replace('Eine E-Mail genügt zunächst;', 'Support-URL und erreichbaren Kontakt bereitstellen;')
s = s.replace('Vertriebsweg je Plattform festlegen: Direktdownload zuerst, Store danach.', 'Vertriebsweg je Plattform entscheiden: Direktdownload, Store oder beides.')
s = s.replace('weil der Mac App Store die Sandbox erzwingt und der Datenordner dann im App-Container liegt – ein Store-Build und ein Direkt-Build teilen ihre Daten dann nicht.', 'weil der Mac App Store Sandbox-Anforderungen stellt. Den tatsächlichen Containerpfad sowie Export und Migration anhand des späteren Store-Builds prüfen.')
s = s.replace('die genauen Werte stehen in den Store-Angaben.', 'die belegten Werte und offene Anforderungen stehen in den Store-Angaben mit Quellen und Abrufdatum.')
s = s.replace('Der Integrationstest und der app-weite Durchlauf decken die Logik ab.', 'Drei automatisierte Suiten prüfen ausgewählte Logik- und UI-Pfade.')
s = s.replace('der Funktion ist', 'der Funktion ist')
write(rel, s)

(QA / 'external_archive_manifest.json').write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'{len(ledger)} Vorgänger archiviert; Dateien konsolidiert.')
