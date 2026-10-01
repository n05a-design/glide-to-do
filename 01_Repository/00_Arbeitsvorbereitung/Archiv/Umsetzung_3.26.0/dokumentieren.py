from pathlib import Path
import shutil,json
root=Path('01_Repository/Glide')
def archive(path,version='3.25.0'):
 path=root/path
 if path.exists():
  target=path.parent/'archiv'/f'{path.stem}_{version}_vor_Vervollstaendigung_3.26.0{path.suffix}'
  target.parent.mkdir(exist_ok=True)
  if not target.exists():shutil.copy2(path,target)
 return path
p=archive(Path('CHANGELOG.md'),'3.26.0');s=p.read_text(encoding='utf-8');pos=s.index('## 3.25.0');s=s[:s.index('## 3.26.0')]+'''## 3.26.0 – Arbeitsstand 20.09.2026

Noch kein freigegebener Abschlussstand. Der Audit vom 20.09. hat erhebliche Lücken im bisherigen 3.26-Stand bestätigt. Die Nachbesserung läuft schrittweise mit isolierten Regressionstests.

- Doppeltes Eingangssymbol in Mein Tag entfernt; die native Aufklappfunktion bleibt bestehen.
- Große oder extrem lange Pinnwände erhalten eine beschriftete verdichtete Vorschau; keine erfundenen Karten bei leerer Pinnwand und keine inneren Trennlinien.
- Vorhandene Verbindungen zwischen ausgewählten Karten übernehmen die gewählte Verbindungsart. Die Ziellistenauswahl einer Ordnerpinnwand und die Mutation selbst sind auf deren Listen begrenzt.
- Auswahlrechteck mit vollständiger Einschließung; optionales Ausrichten an Kartenkanten und Mittellinien, sichtbare Hilfslinien.
- Gismo als Standardname, höhere Standardposition, kontextbezogene Sätze, Füttern, Hover-Reaktion und eigener Schalter für Spielereien.
- Tatsächlicher Monatsname in der Kalenderkachel; normale Aktionsbuttons ohne Dialogellipsen. Kompakte Symbole für Aktionen, Anzeige und Erweitert; Fortschritt im kleinsten Kopfzeilenmodus ausgeblendet.
- Minimaldesigns mit wählbarem Akzent und Kontrastgrau; aktive und berührte Buttonflächen mit passender Outline.
- Neue Listenart Notiz mit Aufgabenbereich und Rich-Text-Editor, Formatspannen, Links, Zeitstempeln und lokalem Undo/Redo. Formatierte Inhalte werden gespeichert, dupliziert und in Backups/Austauschdateien übernommen.
- Aufgabenformat **17** mit unveränderter Originalsicherung vor der ersten Migration. Persönliche Einstellungen bleiben Format 2.
- Verlauf als Seitenleistenansicht; höchstens 15 Einträge und höchstens 15 Tage, auch beim Laden und Speichern geprüft.

Prüfstand und offene Anforderungen: [Entscheidungen und Umsetzungsstand](docs/decisions/Entscheidungen_3.26.0.md).

'''+s[pos:];p.write_text(s,encoding='utf-8')
d=root/'docs/decisions/Entscheidungen_3.26.0.md';d.write_text('''# Entscheidungen und Umsetzungsstand 3.26.0

Stand 20.09.2026 · App-Version 3.26.0 · Datenformat 17 · in Arbeit

Der Entwicklungsauftrag ist fachliche Referenz. Ausgeführt wird der ausdrückliche Nutzerauftrag, fehlende Änderungen umzusetzen und vorhandene zu überprüfen. Die alten Screenshots und frühere Agentenaussagen sind keine Nachweise für den aktuellen Quellstand.

## Festlegungen

- Bestehende Daten, Funktionen und persönliche Einstellungen bleiben erhalten; Tests verwenden ausschließlich GLIDE_DATA_DIR in temporären Ordnern.
- „Auto“ ist im bestehenden Produkt automatisches Anheften neuer Punkte, keine automatische Kartengröße. Die Funktion bleibt erhalten und heißt Auto anheften. Die abweichende Beschreibung im Auftrag wird nicht als Anlass verwendet, die bestehende Funktion umzudeuten.
- Lasso: vollständige Einschließung; mit Strg/Cmd ergänzend. Ein leerer Klick hebt die Auswahl auf.
- Ausrichtung an anderen Karten ist optional und zunächst aus. Toleranz sechs Canvas-Pixel, Alt unterdrückt sie während des Ziehens. Das bestehende Raster bleibt separat schaltbar.
- Sehr große Pinnwandvorschauen sind ausdrücklich als verdichtete Übersicht gekennzeichnet. Sie zeigen höchstens 40 Karten; Gesamtzahl und tatsächliche Anzahl der dargestellten Karten werden genannt. Koordinaten werden dadurch nicht verändert.
- Verlauf wird im Bestand gespeichert und auf 15 Einträge beziehungsweise 15 Tage begrenzt. Die erste Schema-17-Speicherung sichert die Originaldatei vor der Übernahme.
- Die Listenart kann zwischen Aufgaben und Notiz wechseln. Notizinhalt bleibt beim Zurückschalten erhalten. Rich Text verwendet Standard-Tk, keinen HTML-Renderer und keine neue Laufzeitabhängigkeit.
- Gerichtete Aufgabenabhängigkeiten, Reisen von Pinnwänden und dauerhaft benannte Bereiche bleiben offene Produktentscheidungen. Verbindungsrichtungen stellen keine Aufgabenabhängigkeit dar.
- Kein Big-Bang-Umbau auf ttk oder ein neues Ereignissystem. PanedWindow, Navigator und weitere Architekturänderungen werden nach Nutzen und Prüfbarkeit bewertet.

## Nachgewiesener Zwischenstand

Neue Regressionen in tests/integration/test_features326.py prüfen Vorschaugeometrie mit 205 Karten, unveränderte gespeicherte Positionen, Verbindungsstil bei Mehrfachauswahl, Ordnergrenzen auch gegen fehlerhafte Dialogdaten, Lasso, optionale Ausrichtungseinstellung, Akzente, Notizformatierung/Undo/Redo, Speicher- und Duplikatrundlauf, bytegenaue Migrationssicherung und Verlaufsgrenzen. Die Attributprüfung meldet derzeit keine Befunde.

## Noch nicht vollständig abgenommen

Zoom auf allen Elementen und allen sechs Stufen; vollständiges FieldPairGrid in der Punktmaske; Mini-Map-Bewertung; sämtliche Notizformate, Vorlagen, Exporte und fehlgeschlagene Schreibvorgänge; Verlauf für Import/Export/Backup-Aktionen; vollständiger Dopamin-Abgleich; Kommentarbereinigung und Dokumentationsabgleich; Handbuch-Druck/Export; Produkt-, Lizenz-, Branding- und Signierungsunterlagen; Release-Dateien; vollständiger QA-Abschluss und Sichtprüfung.

Diese Liste wird erst nach tatsächlicher Umsetzung und Prüfung reduziert. Eine bestandene Teilprüfung ist keine Freigabe der Gesamtversion.
''',encoding='utf-8')
p=archive(Path('docs/07_QA_BERICHT.md'));s=p.read_text(encoding='utf-8');s=s.replace(s.splitlines()[0],s.splitlines()[0]+'''

## Nachbesserung 3.26.0 – 20.09.2026

Der vollständige Abschlusslauf 3.25.0 ist mit Exitcode 0 belegt: [Originalprotokoll vom 19.09.2026](../tests/qa-3.25.0/abschluss/ergebnis.json). Er verwendete Python 3.13.15 unter Windows.

Der vollständige Ausgangslauf vor der jetzigen Nachbesserung endete mit Exitcode 1: [Ausgangsprotokoll](../tests/qa-3.26.0/vor_umsetzung_2026-09-20/ergebnis.json). Unter anderem fehlten aktuelle Release-Fixtures, der Vorlagenkatalog war nicht reproduzierbar, test_ui39 scheiterte am Popup und test_vollpruefung325 überschritt 900 Sekunden. Diese Fehler bestanden bereits vor den jetzigen Quelländerungen.

Die jetzige Umsetzung verwendet Datenformat 17 und ist noch nicht vollständig freigegeben. [Entscheidungen und offene Abnahme](decisions/Entscheidungen_3.26.0.md). Weitere Ergebnisse werden unter tests/qa-3.26.0/nachbesserung_2026-09-20 abgelegt.

## Vorheriger dokumentierter Prüfstand
''',1);p.write_text(s,encoding='utf-8')
p=archive(Path('docs/09_PROJECT_HANDOFF.md'));s=p.read_text(encoding='utf-8');s=s.replace(s.splitlines()[0],s.splitlines()[0]+'''

## Aktueller Arbeitsstand 20.09.2026

App-Version 3.26.0, Datenformat 17, Nachbesserung in Arbeit. Verbindlicher Quellstand: src/glide/app.pyw. Die äußere Python-Datei mit Versionsnummer 3.25 ist weiterhin ein älterer Stand. Den aktuellen Stand nicht mit einer fertigen Release-Abnahme verwechseln.

Der vollständige Abschlusslauf 3.25.0 vom 19.09.2026 ist mit Exitcode 0 belegt. Der neue 3.26-Ausgangslauf scheiterte bereits vor Änderungen an Fixtures, Vorlagen, einem Popup-Test und einem Timeout. Aktuelle Anforderungen, Festlegungen und offene Punkte: [Umsetzungsstand 3.26](decisions/Entscheidungen_3.26.0.md).

Fortsetzung: Ergebnisse unter tests/qa-3.26.0/nachbesserung_2026-09-20 auswerten, betroffene Regressionen beheben; dann offene Anforderungspunkte abarbeiten und erst anschließend vollständige Releaseprüfung ausführen. Immer GLIDE_DATA_DIR vor dem Import isolieren. Bereits umgesetzte Teile durch Tests erhalten, nicht nochmals neu erfinden.

## Historische Übergabe
''',1);p.write_text(s,encoding='utf-8')
(root/'tests/qa-verlauf.md').write_text('''# Langfristiger Prüfverlauf

| Datum | Stand | Ergebnis | Nachweis |
|---|---|---|---|
| 19.09.2026 | 3.25.0 Abschluss, Windows/Python 3.13.15 | Exitcode 0 | [Protokoll](qa-3.25.0/abschluss/ergebnis.json) |
| 20.09.2026 | 3.26.0 vor Nachbesserung | Exitcode 1, einschließlich Timeout im Breitentest | [Protokoll](qa-3.26.0/vor_umsetzung_2026-09-20/ergebnis.json) |
| 20.09.2026 | 3.26.0 Nachbesserung, Schema 17 | In Arbeit; einzelne Regressionen bestanden, keine Gesamtfreigabe | [Suiten-Zwischenstand](qa-3.26.0/nachbesserung_2026-09-20/zwischenstand.json) |
''',encoding='utf-8')
(root/'docs/decisions/DOKUMENTENPFLEGE.md').write_text('''# Dokumentenpflege

Aktuelle Dokumente nennen Version, Datenformat und Prüfstand. Vor Überarbeitung wird die bisherige Datei im benachbarten archiv-Ordner mit ihrer bisherigen Versionsnummer gesichert. Historische Aufträge und Testergebnisse bleiben unverändert. Neue Archive werden im Dokumentationsindex aufgenommen.

Kommentare im Quellcode erklären Verhalten, Invarianten und technische Gründe. Historische Arbeitsauftragsnummern und lange Entwicklungserzählungen gehören in Changelog, Entscheidungen oder DEV_NOTES. Bereinigung darf keinen ausführbaren Code verändern.

Prüfergebnisse werden pro Lauf in einem eigenen Ordner abgelegt und im Prüfverlauf referenziert. Ein fehlgeschlagener Lauf wird nicht durch Wiederverwendung desselben Ordners verdeckt. Archive werden nicht automatisch gelöscht. Eine spätere Aufbewahrungsregel benötigt eine ausdrückliche Festlegung.
''',encoding='utf-8')
(root/'docs/DEV_NOTES.md').write_text('''# Entwicklungsnotizen 3.26.0

Standard-Tk bleibt die Laufzeitbasis. Der neue RichNoteEditor speichert Text und semantische Spannen statt HTML; die Positionen im Dateiformat sind Python-Zeichenindizes. Tk-Indizes werden beim Laden aus Zeilen und nativen Tcl-Spalten erzeugt. Ein lokaler Undo-Stapel umfasst Text und Formatierung gemeinsam.

Pinnwand-Vorschau und echte Pinnwandpositionen sind getrennt. Eine verdichtete Vorschau darf niemals die Modellkoordinaten zurückschreiben. Verbindungen werden über Punktkennungen gespeichert; Änderungen an ausgewählten Verbindungen ändern beide Endpunkte gemeinsam, nicht fremde Kanten.

Migrationen sichern unveränderte Originaldateien, bevor der neue Aufgabenstand geschrieben wird. Der Verlaufszeitraum wird beim Normalisieren sowie vor dem Speichern begrenzt. Benutzerdefinierte Startseitenanordnungen werden nicht durch die neue Standardreihenfolge überschrieben.
''',encoding='utf-8')
err=Path('00_Arbeitsvorbereitung/Fehlerprotokolle');err.mkdir(exist_ok=True,parents=True)
(err/'README.md').write_text('''# Gesammelte Fehlerprotokolle

Dieser Ordner dient der Entwicklungsdiagnose. Laufzeitprotokolle entstehen weiterhin im jeweils gewählten Glide-Datenordner, damit die App portabel bleibt. Hier abgelegte Kopien müssen mit Datum und Version bezeichnet werden. Echte Nutzerdaten werden nicht zu Testdaten gemacht.

Aktuelle automatisierte Ergebnisse: 01_Repository/Glide/tests/qa-3.26.0/.
''',encoding='utf-8')
p=archive(Path('docs/00_INDEX.md'));s=p.read_text(encoding='utf-8');s+='\n## Nachbesserung 3.26 und neue Archive\n\n';
for doc in sorted((root/'docs').rglob('*.md')):
 rel=doc.relative_to(root/'docs').as_posix()
 if rel!='00_INDEX.md' and rel not in s:s+=f'- [{doc.stem}]({rel})\n'
p.write_text(s,encoding='utf-8')
print('Arbeitsstand, Archive und Prüfverlauf dokumentiert')
