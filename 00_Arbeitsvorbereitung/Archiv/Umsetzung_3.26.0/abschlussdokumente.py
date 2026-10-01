from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[2]
repo = root / '01_Repository/Glide'
docs = repo / 'docs'

def write(relative, content):
    path = docs / relative
    if path.exists():
        archive = path.parent / 'archiv' / (path.stem + '_3.26.0_vor_Abschlussabgleich.md')
        archive.parent.mkdir(exist_ok=True)
        if not archive.exists():
            shutil.copy2(path, archive)
    path.write_text(content.strip() + '\n', encoding='utf-8')

write('07_QA_BERICHT.md', '''
# QA-Bericht – Glide 3.26.0

Stand 21.09.2026 · App 3.26.0 · Datenformat 17 · Windows, Python 3.13.15

## Prüfstand

Die Nachbesserung ist implementiert; der abschließende Gesamtlauf steht noch aus. Dieser Bericht wird nach dem tatsächlichen Ergebnis ergänzt. Einzelne bestandene Tests ersetzen keine Gesamtfreigabe.

- [Ausgangslauf vor der Nachbesserung](../tests/qa-3.26.0/vor_umsetzung_2026-09-20/ergebnis.json): Exitcode 1. Bereits vorhanden waren Probleme mit Fixtures, Vorlagenreproduktion, Popup-Tests und Laufzeitgrenzen.
- [Zwischenlauf](../tests/qa-3.26.0/gesamtpruefung_2026-09-21/ergebnis.json): Exitcode 1. Veraltete Testannahmen zu Formulargeometrie, Verlauf und Auto-Beschriftung sowie Dokumentstände und ein verwaister Vorschau-Platzhalter wurden danach korrigiert. Die betroffenen Einzeltests bestanden anschließend.
- Neue Suite `tests/integration/test_features326.py`: Vorschau mit 205 Karten, Auswahlverbindungen, Ordnergrenzen, Lasso, Zoom/Printkoordinaten, Navigator, Akzente, Gismo, Rich-Text-Formate, Unicode, Undo/Redo, Speicherung, Duplikate, Vorlagen, Austausch, Migrationssicherung und Verlaufsgrenzen. Zusätzlich Suchaktualisierungen, Rückmeldungszuordnung und HTML-Escaping.
- Eigene Windows-Sichtproben liegen in `tests/qa-3.26.0/sichtpruefung`. Geprüft: breite und schmale Punktmaske, Notizliste mit sechs Aufgabenzeilen und nutzbarem Editor sowie Verlauf. Scrollbare Dialoginhalte bleiben über dem festen Fußbereich erreichbar.

Alle App-Importe und Tests verwenden temporäre GLIDE_DATA_DIR-Verzeichnisse mit künstlichen Daten. Nutzerdaten wurden nicht als Testbestand geöffnet.

## Grenzen

Automatisierte Tk-Ereignisse und Sichtprüfung ersetzen keinen vollständigen Bedienungstest durch einen Menschen. macOS, native Druckdialoge, reale Installer, Zertifikate und Notarisierung wurden hier nicht ausgeführt. Gismo-Bildmaterial bleibt ein separat vom Nutzer zu lieferndes Asset; die vorhandene zeichenbasierte Darstellung funktioniert weiterhin ohne neue Abhängigkeit. Offene Produktentscheidungen sind in der [Umsetzungsmatrix](decisions/Entscheidungen_3.26.0.md) getrennt aufgeführt.

Der historische [3.25-Abschluss](../tests/qa-3.25.0/abschluss/ergebnis.json) ist erhalten und wird nicht als Prüfnachweis für 3.26 ausgegeben.
''')
write('09_PROJECT_HANDOFF.md', '''
# Projektübergabe – Glide 3.26.0

Stand 21.09.2026 · App 3.26.0 · Aufgabenformat 17 · Einstellungen 2 · Vorlagen 2

Kanonisch ist `src/glide/app.pyw`. Die startbare Kopie wird unter `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.26.0.pyw` im äußeren Projektordner mit denselben Ressourcen bereitgestellt. Der Ordner ist kein Git-Checkout. Originalstände sind archiviert.

## Umgesetzter Stand

Mein-Tag-Aufklappen, lesbare Pinnwandvorschau, Verbindungsbearbeitung, Ordnergrenzen, responsive Buttons und Formulare sind nachgebessert. Pinnwand-Lasso, optionale Ausrichtung mit Guides/Abständen, sechs Zoomstufen und Navigator sind vorhanden. Gismo hat Kontexttexte, Füttern, Hover-Reaktion und einen Schalter für Spielereien. Notizlisten verbinden sechs Aufgabenzeilen mit Rich Text samt Formatierung, Unicode, lokalem Undo/Redo und strukturiertem Austausch. Schema 17 sichert vor der ersten Migration die bisherige Datei. Verlauf ist über die Seitenleiste erreichbar und begrenzt auf 15 Einträge beziehungsweise 15 Tage. Import-/Export-/Backup-Aktionen werden erfasst. Das Handbuch lässt sich als HTML speichern und zum Drucken öffnen.

## Weiterarbeit und Prüfung

Den [QA-Bericht](07_QA_BERICHT.md) und die [Umsetzungsmatrix](decisions/Entscheidungen_3.26.0.md) zuerst lesen. Bereits erledigte Punkte nicht erneut als offen behandeln. Bei Quelländerungen GLIDE_DATA_DIR vor dem Import isolieren und die betroffenen Regressionen ausführen. Vollprüfung aus dem Repository: `python tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.26.0/abschluss_2026-09-21 --timeout 900`.

Benannte Pinnwandbereiche, echte Aufgabenabhängigkeiten und Pinnwand-Reisen sind fachlich offen. Der Konkurrenz-Backlog ist kein vollständig beauftragtes 3.26-Paket. Es liegen Lizenzentwurf, Vertriebs-/Markenrecherche-Vorbereitung und Signierungsanleitung vor; keine abgeschlossene Markenfreigabe, keine Signierung und keine Veröffentlichung.
''')
write('decisions/Entscheidungen_3.26.0.md', '''
# Entscheidungen und Umsetzungsstand 3.26.0

Stand 21.09.2026 · App-Version 3.26.0 · Datenformat 17

Der Entwicklungsauftrag ist fachliche Referenz. Maßgeblich ist der ausdrückliche Nutzerauftrag zur Umsetzung und Nachprüfung. Alte Screenshots und frühere Agentenaussagen sind keine Nachweise für den aktuellen Quellstand.

| Anforderung | Umsetzung und Abgrenzung |
| --- | --- |
| Mein Tag | Redundanten Textpfeil entfernt; native Baum-Aufklappfunktion erhalten. |
| Startseite | Tatsächlicher Monatsname, Gismo-Kontexte und Interaktionen, höhere Standardposition. Individuelle Kachelreihenfolgen bleiben erhalten. |
| Vorschau | Leere Pinnwand bleibt leer; keine Innenlinien. Große/extreme Bestände zeigen eine ausdrücklich verdichtete Übersicht mit höchstens 40 Karten, Gesamtzählung und unveränderten Modellkoordinaten. |
| Buttons und schmale Fenster | Dialogellipsen entfernt, Aktionsleisten pro Zeile unabhängig, kompakte Kopfzeilen und Anzeigen, Minimaldesign-Akzente einschließlich Kontrastgrau. |
| Pinnwand-Bugfixes | Ausgewählte Verbindungen ändern, Alle auswählen, Ordner-Ziellisten an Dialog und Mutation begrenzen. Auto anheften benennt die vorhandene Funktion; es bedeutet nicht automatische Kartengröße. |
| Canvas | Logische Tags, Lasso mit vollständiger Einschließung und Strg/Cmd-Ergänzung, optionale Ausrichtung mit sechs Bildschirmpixeln Toleranz, Alt-Unterdrückung, Abstands-Guides, Zoom 50–200 Prozent in sechs Stufen, optionaler Navigator. Druck nutzt logische Koordinaten. |
| Punkteingabe | FieldPairGrid für die gesamte Maske, schmal einspaltig, scrollbarer Inhalt, feste Abschlussaktionen und umbrechende Checklistenaktionen. |
| Notizlisten | Sechs Aufgabenzeilen plus Rich-Text-Editor, 13 Formate, Links, Datum/Zeit, lokale Tastenkürzel und Undo/Redo, Suchmarkierung, Autosave, Schema-17-Migration, Backups, Austausch, Duplikate und Vorlagen. TXT/Markdown enthalten den Notiztext; CSV bleibt auf Aufgaben ausgerichtet. |
| Verlauf | Seitenleistenansicht, Filter/Suche/Export, höchstens 15 Einträge und 15 Tage; Import/Export/Backup enthalten. |
| Rückmeldungen | Gemeinsame Mutationswege ergänzen Bearbeiten, Verschieben, Wiederherstellen, Labels, Fälligkeit und Planung. Notiz-Autosave löst keine Animationsflut aus. |
| Handbuch | HTML-Datei speichern oder im Standardprogramm zum Drucken öffnen. |
| Wartbarkeit | Historische Punktmarker entfernt, technische Gründe erhalten; Suchänderungen je Ereigniszyklus zusammengefasst. Architektur- und Widget-Bewertung dokumentiert. |
| Ablage | Historische Dokumente und alte QA-Verzeichnisse nach festgelegten Altersgrenzen archiviert; keine historischen Daten gelöscht. |
| Produktvorbereitung | Publisher festgehalten, persönlicher nichtkommerzieller Lizenzentwurf, Vertrieb/Markenrecherche-Vorbereitung und Signierungsanleitung vorhanden. |

## Bewusste offene Punkte

Permanente benannte Bereiche, echte gerichtete Aufgabenabhängigkeiten und Pinnwand-Reisen benötigen gemäß Abschnitt 1 des Auftrags eine fachliche Entscheidung. Der Abschnitt 14 bleibt Backlog. Neue Gismo-Bildassets sind vom Nutzer separat vorgesehen; die vorhandene Darstellung bleibt nutzbar. Es wurden keine Vertriebskonten angelegt, Markenrechte bestätigt oder signierte Installer veröffentlicht.

Kein vollständiger ttk- oder Virtual-Event-Umbau: Die Bewertung und bestehende Abhängigkeiten stehen in [Architektur](../02_ARCHITECTURE.md). Der tatsächliche Prüfnachweis und Plattformgrenzen stehen im [QA-Bericht](../07_QA_BERICHT.md).
''')

p = docs/'02_ARCHITECTURE.md'
s = p.read_text(encoding='utf-8')
s = s.replace('Glide 3.23.0', 'Glide 3.26.0', 1)
write('02_ARCHITECTURE.md', s + '''

## Bewertung 3.26: Widgets und Ereignisse

Die Notizansicht verwendet eine feste Höhe von sechs Aufgabenzeilen mit eigenem Scrollen und einen wachsenden Editor. Ein PanedWindow würde die vereinbarte 5–7-Zeilen-Vorgabe ohne zusätzlichen Nutzen aufweichen. Pinnwand-Eigenschaften und eine ständig sichtbare Detailansicht sind derzeit keine unabhängigen Paneele; deshalb dort kein Splitter.

Comboboxen, kompakte Zoomauswahl und bestehende Fortschrittskomponenten bleiben erhalten. Spinbox, Scale und Notebook liefern für die vorhandenen Eingaben keinen belegten Bedienvorteil und werden nicht parallel eingeführt.

Die direkten Abhängigkeiten sind: item_change -> Speichern/Verlauf/Statistik und aktuelle Aufgabenansicht; sidebar_change -> Speichern/Sidebar und Listenansicht; guarded_structural_change schützt Strukturumbauten. Theme-Wechsel aktualisieren zentrale Styles und sichtbare Views; Import/Restore normalisiert vollständig vor dem Neuaufbau. Auswahl bleibt lokal im Workspace, Pinnwandänderungen in dessen Refresh-Pfad. Verlauf wird aus dem gespeicherten Modellzustand abgeleitet.

Damit sind TaskChanged, ListChanged und StructureChanged mögliche spätere Signale an den Mutationsgrenzen; SelectionChanged/BoardChanged bleiben lokal; ThemeChanged/SettingsChanged gehören an die zentralen Einstellungswege; HistoryChanged an den Verlaufsschreibpunkt; DataReloaded erst hinter die vollständige Normalisierung. 3.26 führt keine zweite Benachrichtigungsschicht neben diesen Aufrufen ein: Das würde sonst doppelte Refreshes und unklare Reihenfolge riskieren. Eine spätere Migration muss pro Grenze den direkten Aufruf ersetzen und Reentranz testen.

Live-Suchänderungen werden mit after_idle je Ereigniszyklus zusammengefasst; ein expliziter Refresh verwirft den geplanten Doppelaufruf. Rich-Text-Autosave wartet 400 ms, Flushing vor Seitenwechsel und Datenausgabe schließt ausstehende Änderungen ab. Resize-, Scrollbar- und Canvas-Aktualisierungen verwenden ihre vorhandenen Scheduler weiter.
''')
p = docs/'DEV_NOTES.md'
write('DEV_NOTES.md', p.read_text(encoding='utf-8') + '''

## Geometrie und Ereignisse 3.26

ButtonFlow verwendet je Umbruchzeile einen eigenen Frame. Gemeinsame Grid-Spalten über mehrere Zeilen würden sonst die jeweils größte Spaltenbreite erzwingen und trotz passender Summen Buttons abschneiden. Im übergeordneten Frame angelegte Buttons müssen über den Zeilenframes angehoben werden.

Die Aufgaben-Scrollbar einer Notizliste hat Anforderungshöhe 1; sonst vergrößert ihre Standardhöhe den auf sechs Zeilen begrenzten Treeview. FieldPairGrid entfernt bei einspaltigem Layout die gemeinsame Spaltenuniformität. Zoom verändert ausschließlich die Darstellung; Druck und gespeicherte Kartenpositionen verwenden logische Koordinaten.
''')
p = repo/'CHANGELOG.md'
s = p.read_text(encoding='utf-8').replace('Arbeitsstand 20.09.2026', '21.09.2026', 1)
s = s.replace('Noch kein freigegebener Abschlussstand. Der Audit vom 20.09. hat erhebliche Lücken im bisherigen 3.26-Stand bestätigt. Die Nachbesserung läuft schrittweise mit isolierten Regressionstests.', 'Die Nachbesserung des zuvor unvollständigen Standes ergänzt die folgenden Funktionen. Prüfergebnisse und Plattformgrenzen sind im QA-Bericht dokumentiert.')
anchor = 'Prüfstand und offene Anforderungen:'
s = s.replace(anchor, '- Sechs Zoomstufen, optionale Mini-Map, Abstands-Guides und zoomunabhängige Druckgeometrie.\n- Vollständig responsive Punktmaske, unabhängige Buttonzeilen und nutzbarer Notizeditor unter sechs Aufgabenzeilen.\n- Handbuch als HTML speichern/drucken; Import-, Export- und Backup-Ereignisse im Verlauf; ergänzte Aktionsrückmeldungen.\n- Dokumentarchivierung, Schema-17-Referenzdaten und reproduzierbare Vorlagen; Lizenzentwurf und Signierungs-/Vertriebsvorbereitung.\n\n'+anchor, 1)
p.write_text(s, encoding='utf-8')

# Alle neu hinzugekommenen Dokumente einschließlich Originalsicherungen aufführen.
p = docs/'00_INDEX.md'
s = p.read_text(encoding='utf-8')
for entry in sorted(docs.rglob('*.md')):
    relative = entry.relative_to(docs).as_posix()
    if entry != p and relative not in s:
        s += f'\n- [{entry.stem}]({relative})\n'
p.write_text(s, encoding='utf-8')
print('Abschlussdokumente vorbereitet und archiviert.')
