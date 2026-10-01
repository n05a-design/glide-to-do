"""Gezielte Dokumentkorrekturen; sichert jede Ausgangsfassung vor dem Schreiben."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[3] / "01_Repository" / "Glide"

def save(name, text):
    path = ROOT / name
    if path.exists():
        backup = path.parent / "archiv" / (path.stem + "_3.2.0_vor_Bestandsanalyse_2026-09-04" + path.suffix)
        backup.parent.mkdir(parents=True, exist_ok=True)
        if not backup.exists():
            shutil.copy2(path, backup)
    path.write_text(text, encoding="utf-8")

def edit(name, replacements):
    text = (ROOT / name).read_text(encoding="utf-8")
    for old, new in replacements:
        if old not in text:
            raise ValueError(f"Text nicht gefunden: {name}: {old[:70]}")
        text = text.replace(old, new)
    save(name, text)

if __name__ == '__main__':
    EXCEPTION_ROW = '| `description_suffix` (zwei Ansichten) | 📝 (U+1F4DD) | Beschreibungsmarker in Aufgabenbaum und Aufgabenübersicht |'
    for name in ("docs/01_PRODUCT_CONSTRAINTS.md", "docs/02_ARCHITECTURE.md"):
        edit(name, [
            ('Zwei Marker außerhalb von `ICONS`', 'Drei Symbolarten außerhalb von `ICONS`'),
            ('| `GROUP_MARKER` | 📁 (U+1F4C1) | Aufgabenbaum vor Gruppentiteln **und** im TXT-Export |', '| `GROUP_MARKER` | 📁 (U+1F4C1) | Aufgabenbaum vor Gruppentiteln **und** im TXT-Export |\n' + EXCEPTION_ROW),
        ])
    
    edit("docs/01_PRODUCT_CONSTRAINTS.md", [
        ('Jedes Symbol der Oberfläche ist ein **Textzeichen** und steht in einer zentralen\nTabelle (`ICONS`). Farbige Emoji sind seit 3.2.0 ausgeschlossen:', 'Zielvorgabe: Jedes Symbol der Oberfläche ist ein **Textzeichen** und steht in einer zentralen\nTabelle (`ICONS`). Die Umstellung in 3.2.0 ist noch unvollständig (siehe Ausnahmen):'),
        ('Nicht vorgesehen sind: Labels als Filterkriterium mit eigener Ansicht,\nhierarchische Labels und automatisch vergebene Labels.', 'Nicht vorgesehen sind: Labels als Filterkriterium mit eigener Ansicht und\nhierarchische Labels. Frei definierte Labels werden nicht automatisch vergeben;\ndie festen Systemlabels „Long-Task“ und „Überschrift“ werden mit der Punktart synchronisiert.'),
    ])
    
    arch = (ROOT / 'docs/02_ARCHITECTURE.md').read_text(encoding='utf-8')
    start = arch.rindex('## Symbole\n')
    end = arch.index('## Umbenennen in der Seitenleiste', start)
    arch = arch[:start] + arch[end:]
    arch = arch.replace('Jedes Symbol der Oberfläche steht in der Tabelle `ICONS` und ist ein\nTextzeichen.', 'Die zentrale Symboltabelle `ICONS` enthält Textzeichen. Die angestrebte\nvollständige Zentralisierung ist wegen der unten genannten Ausnahmen noch offen.')
    arch = arch.replace('**Aufgabe und Long-Task** verhalten sich im Datenmodell identisch; sie unterscheiden sich ausschließlich in der Darstellung.', '**Aufgabe und Long-Task** teilen Status- und Terminlogik; Long-Tasks erlauben zusätzlich gespeicherte Zeilenumbrüche und erhalten ein festes Artlabel.')
    arch = arch.replace('Ein **Punkttext ist einzeilig**. Die Mehrzeiligkeit eines Long-Tasks entsteht erst bei der Darstellung; die Normalisierung führt Zeilenumbrüche und Mehrfachleerzeichen auf ein Leerzeichen zurück.', 'Ein **Punkttext ist einzeilig**, außer beim Long-Task: `normalize_item_text` bewahrt dort bis zu 40 Textzeilen. Die Liste stellt davon höchstens fünf Zeilen dar; die vollständige Fassung bleibt in den Punktdetails zugänglich.')
    arch = arch.replace('6 Pixel Radius', '9 Pixel Radius (`LabelChip.RADIUS`)')
    arch = arch.replace('die Kopfzeile einer geöffneten Liste oder eines Ordners besteht aus einzelnen\n  `tk.Label`-Widgets, von denen jedes seine eigene Farbe trägt.', 'die Kopfzeile einer geöffneten Liste oder eines Ordners verwendet\n  `LabelChip`-Widgets mit eigener Flächenfarbe.')
    arch = arch.replace('## Bewusste Übergangsentscheidung', '## Bewusste Architekturentscheidung')
    start = arch.index('Eine Aufteilung in `version.py`')
    end = arch.index('## Eine Eingabemaske', start)
    arch = arch[:start] + 'Der Monolith bleibt erhalten. Eine Modulzerlegung ist weder Voraussetzung der\nStabilisierung noch Teil des aktuellen Auftrags. `VERSION` und `APP_VERSION`\nwerden gemeinsam geprüft. Das Datenformat bleibt 10; fehlende Felder älterer\nunterstützter Formate werden durch die bestehende Normalisierung ergänzt.\n\n' + arch[end:]
    arch = arch.replace('je nach Monat fünf oder\nsechs Zeilen', 'je nach Monat vier, fünf oder\nsechs Zeilen')
    arch = arch.replace('auch `docs/` seit 3.2.0', 'im Repository als `archiv/`, im äußeren Workspace als `Archiv/`')
    arch = arch.replace('bis zu 14 Aufgaben je Tag', 'eine begrenzte Zahl sichtbarer Aufgaben je Tag')
    save('docs/02_ARCHITECTURE.md', arch)
    
    edit('docs/06_DATA_BACKUP_MIGRATION.md', [
        ('# Daten, Backup und Migration', '# Daten, Backup und Migration\n\nStand: 04.09.2026 · App-Version 3.2.0 · Datenformat 10'),
        ('Wer einen solchen Altbestand hat, öffnet ihn über\n„Datei → Komplettbackup laden …“', 'Wer bereits ein portables Komplettbackup eines solchen Altbestands hat, öffnet es über\n„Datei → Komplettbackup laden …“; eine rohe Speicherdatei mit separaten Anhängen\nist kein solches ZIP-Backup'),
        ('Ein Punkttext wird beim Laden auf eine Zeile normalisiert (Zeilenumbrüche und\nMehrfachleerzeichen werden zu einem Leerzeichen). Die Mehrzeiligkeit eines\nLong-Tasks entsteht ausschließlich bei der Darstellung; dadurch bleiben TXT-,\nCSV- und Markdown-Export zeilentreu und der TXT-Import eindeutig.', 'Historisch in Format 8 war der Text einzeilig. Im aktuellen Stand 3.2.0\nbewahrt `normalize_item_text` bei Long-Tasks bis zu 40 eigene Textzeilen; alle\nanderen Punktarten bleiben einzeilig. Der TXT-Rundlauf nutzt `Text:`-Fortsetzungen.'),
        ('Farbschlüssel (`label_red`, `label_blue` …) werden beim Laden auf die\nListenfarbpalette abgebildet.', 'Farbschlüssel (`label_red`, `label_blue` …) wurden früher auf die\nListenfarbpalette abgebildet. Seit 3.2.0 ist diese Abbildung entfernt: Die lokale\nNormalisierung setzt unbekannte Farben auf `DEFAULT_LABEL_COLOR`; ein portables\nBackup mit unbekannter Labelfarbe wird durch die strikte Schemaprüfung abgelehnt.'),
        ('Vollständige `.glidebackup`-Archive der Datenformate 4 bis 9 werden akzeptiert.', 'Vollständige `.glidebackup`-Archive der Datenformate 4 bis 10 werden akzeptiert.'),
        ('`tests/fixtures/current_v7/`, `current_v6/`, `current_v5/`, `current_v4/` und `legacy_v2/`', '`tests/fixtures/current_v10/`, `current_v9/`, `current_v8/`, `current_v7/`, `current_v6/`, `current_v5/`, `current_v4/` und `legacy_v2/`'),
        ('alle fünf Bestände', 'alle acht Bestände'), ('alle fünf durch', 'alle acht durch'),
    ])
    
    edit('docs/05_QA_TESTPLAN.md', [
        ('# QA-Testplan', '# QA-Testplan\n\nStand: 04.09.2026 · App-Version 3.2.0 · Datenformat 10\n\nDie Versionsüberschriften beschreiben, wann eine Prüfung hinzukam. Der aktuelle\nPrüfstand steht in `07_QA_BERICHT.md`, der gemeinsame Aufruf in `../tests/README.md`.\nWindows und macOS benötigen kein Xvfb; Linux benötigt für Tk ein Display.\n'),
        ('Ein versehentlich\n  eingefügtes Emoji fällt damit im Testlauf auf, nicht erst auf einem fremden\n  Rechner.', 'Der Test gilt nur für\n  diese Tabelle; die drei Emoji-Ausnahmen außerhalb von `ICONS` sind in\n  `01_PRODUCT_CONSTRAINTS.md` dokumentiert.'),
        ('Maße (Radius 6,', 'Maße (aktuell Radius 9,'),
        ('Referenzbestände der Formate 9, 8, 7, 6, 5, 4 und 2', 'Referenzbestände der Formate 10, 9, 8, 7, 6, 5, 4 und 2'),
        ('Systemblock der Seitenleiste: Eingang, „In Bearbeitung“ und Papierkorb stehen\n  in einem dreizeiligen Feld, der Listenbaum darunter.', 'Systemblock der Seitenleiste: Eingang, „In Bearbeitung“, „Verspätet“ und\n  Papierkorb stehen aktuell in einem vierzeiligen Feld, der Listenbaum darunter.'),
        ('Kalender: Wochenstart am Montag, fünf Wochen ab der laufenden Woche, Sammeln', 'Kalender: Wochenstart am Montag, aktuelles Wochen- oder Monatsraster, Sammeln'),
        ('Themenschalter-Wechsel 🌙/☀', 'Themenschalter-Wechsel ☾/☀'),
    ])
    
    edit('docs/decisions/PRODUCT_IDENTITY.md', [
        ('| Oberflächensymbole | ausschließlich Textzeichen, keine Emoji | `ICONS`, im Integrationstest erzwungen (< U+1F000) |', '| Oberflächensymbole | `ICONS` nutzt Textzeichen; drei Emoji-Ausnahmen außerhalb der Tabelle sind offen | `ICONS`, `GROUP_MARKER`, `IMPORTANCE_MARKERS[3]`, `description_suffix`; siehe Produktgrenzen |'),
        ('| Max. Anhangsgröße | 512 MB je Datei |', '| Größenlimit je Anhang | 512 MiB je Datei |'),
        ('| Max. Backupgröße | 2 GB gesamt, 32 MB Daten-JSON |', '| Entpackte Backup-Grenzen | 2 GiB gesamt, 32 MiB Daten-JSON |'),
        ('| Max. Aufgabenzahl je Bestand | 200.000 |', '| Technisches Validierungslimit | 200.000 Punkte; keine Performancezusage |'),
        ('| Getestete Laufzeit | Python 3.12 / Tk 8.6 | Integrationstestlauf |', '| Prüflaufzeit | Windows: Python 3.12.12 / Tk 8.6.17; zuvor dokumentiert Linux/Xvfb | aktuelles Ergebnis in `../07_QA_BERICHT.md` |'),
        ('| macOS Mindestversion | offen, Empfehlung macOS 12 | folgt aus Testgeräten |', '| macOS Mindestversion | offen | folgt aus Build-Laufzeit und Tests auf Zielgeräten |'),
        ('| macOS Architektur | offen, Empfehlung Universal 2 | Inhaber |', '| macOS Architektur | offen; Universal 2 erst nach Machbarkeits- und Buildprüfung | Inhaber |'),
        ('Bis 3.1.0 stand hier **Datenformat 9**, während der Code seit 2.11.0 auf\n**10** lief – über drei Versionen unbemerkt.', 'Der übergebene Kontext meldete einen veralteten Wert 9. Beim aktuellen\nAbgleich enthielt diese Datei bereits korrekt **10**. Der tatsächliche Dateistand\nhat Vorrang vor älteren Übergaben.'),
    ])
    
    edit('README.md', [
        ('**Nur noch Textzeichen als Symbole.**', '**Textzeichen in der zentralen Symboltabelle.**'),
        ('alle\n  Oberflächensymbole stehen in einer Tabelle und sind keine Emoji mehr.', 'die\n  zentralen Symbole stehen in `ICONS`. Gruppenmarker, hohe Wichtigkeit und\n  Beschreibungsmarker sind noch Emoji-Ausnahmen (siehe Produktgrenzen).'),
        ('**Kein Datenverlust mehr.**', '**Absicherung gegen Datenverlust.**'),
        ('Daneben liegen unter `tests/tools/` vier Werkzeuge, die kein Ja/Nein liefern,\nsondern Material zum Hinsehen:', 'Daneben liegen unter `tests/tools/` Werkzeuge für Prüfung und Arbeitsdaten,\nunter anderem:'),
    ])
    
    edit('src/glide/README.md', [
        ('Eine spätere Aufteilung in UI, Datenmodell, Persistenz, Pfade und Versionierung benötigt ein eigenes Refactoring mit Regressionstests.', 'Eine Modulaufteilung ist nicht beauftragt.'),
    ])
    
    print('Dokumente gezielt abgeglichen; Ausgangsfassungen archiviert.')
    