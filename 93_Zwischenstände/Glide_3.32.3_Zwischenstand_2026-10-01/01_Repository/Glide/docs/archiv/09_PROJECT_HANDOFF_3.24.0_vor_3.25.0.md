# Projektübergabe – Glide 3.23.0

Stand 19.09.2026 · Glide 3.24.0 · Aufgabenformat 16 · Einstellungen 2 · Vorlagen 2

Kanonisch: `src/glide/app.pyw`. Startbare Kopie im äußeren Ordner `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.23.0.pyw`, mit vollständigen Ressourcen. Kein Git-Checkout, unveröffentlichter Entwicklungsstand.

## Prüf- und Ablagestand

Der letzte vollständige Abschlusslauf auf Zielhardware gehört zu **3.21.4**: **15.09.2026 um 10:23** auf macOS mit Python 3.14.5 und `TZ=Europe/Berlin`, **Exitcode 0**, **39 Schritte, davon 37 ausgeführt**, alle Testsuiten und Analysen bestanden. [Prüfprotokoll](../tests/qa-3.21.4/abschluss/ergebnis.json).

Für **3.23.0** umfasst der Prüfstand **27 Testsuiten** und **vier Analysen** – statische Analyse, Erreichbarkeit, Standprüfung der Dokumente und neu die Attributprüfung. Der Stand ist in der Entwicklungsumgebung grün; die plattformgebundenen Schritte (Screenshot-Erzeugung, manuelle Sichtprüfung) und der Abgleich gegen das vollständige Dokumentarchiv sind dort nicht ausführbar und stehen auf Zielhardware noch aus. Details: [QA-Bericht](07_QA_BERICHT.md).

Die Übernahme ist abgeschlossen. In `07_Python-Versionen` liegt nur die aktuelle startbare Fassung; ältere Arbeitsstände und das unveränderte Übertragungspaket sind archiviert. Eine Wortgrenze in `standpruefung.py` verhindert Fehlalarme bei Vorlagenformat 2. `pruefen.py` vergleicht feste Erinnerungen im Beispielbestand relativ zum Erzeugungstag und unter Erhaltung der Ortszeit; Gegenproben einschließlich Sommerzeitwechsel bestanden.

## Funktionsbestand

Umgesetzt sind Kalenderimport und Kalenderausgabe als ICS, der dauerhafte Änderungsverlauf, der CSV-Import mit Spaltenzuordnung, die Druck- und PDF-Ausgabe, das vollständige App-Backup mit Inhaltsvorschau, die Tagesplanung mit Tageskapazität, Bearbeitungstag und geschätzter Aufwand, die Tabellenansicht mit listenspezifischen Spalten, „Mein Tag“, die Schnellerfassung mit deutscher Fristvorschau, gespeicherte Filter sowie Reiter und Pinnwände.

Durchgehende Grundlage, unabhängig von der jeweils neuesten Funktion: verschachtelte Listen und Ordner, Aufgaben, Long-Tasks, Gruppen, Überschriften und Unterpunkte, Notizen, Fälligkeit mit Uhrzeit, Wichtigkeit, sechs Wiederholungsarten, Erinnerungen innerhalb der laufenden App, Labels, Farben, Beschreibungen und lokale Anhänge an Punkten, Listen und Ordnern, Kalenderansicht, Suche und Offen-Filter, Mehrfachauswahl, Ziehen, Rückgängig und Papierkorb, 16 Praxisvorlagen mit eigenem Katalog zum Bearbeiten, Importieren und Exportieren, TXT-, CSV- und Markdown-Austausch, portable Aufgabenbackups sowie Hell- und Dunkelmodus mit Akzentfarbe und drei Schriftgrößen.

Alle Ansichten bearbeiten dieselben Aufgabenobjekte. Tabellenspalten, „Mein Tag“, Reiter, Pinnwand, gespeicherte Filter und Tageskapazität sind persönliche Einstellungen und stehen nicht in einem Aufgabenbackup.

## Zuletzt umgesetztes Funktionspaket: 3.23, Designsystem, Leistung, Austauschformat und Arbeitsfläche

3.23.0 ist kein einzelnes Feature, sondern ein gebündelter Umbau ohne Formatsprung. Vier Bereiche tragen ihn:

**Designsystem.** Grunddesign, Farbmodus und Dopamin-Modus sind zu einer Auswahl zusammengeführt; `DESIGNS` beschreibt jedes Design deklarativ, Liquid-Glass liegt als zwei Einträge darin. Bei Änderungen besonders prüfen: dass `active_theme` seine Werte ausschließlich aus `design_info` ableitet, dass die Migration aus `theme`/`color_mode`/`glass_mode` weiterhin läuft **und** die abgeleiteten Spiegelwerte zurückschreibt (sonst verliert ein Rückwechsel auf 3.22 den Dopamin-Modus), und dass jede Auswahl- und Hover-Fläche ihre Textfarbe über `ensure_contrast` bekommt statt fest verdrahtet. [Designsystem](50_DESIGNSYSTEM_3.23.0.md).

**Leistung und Oberfläche.** Der Ansichtswechsel wurde profiliert, nicht überdeckt: drei Ursachen – mehrfach berechnete Bestandszählungen, wiederholte Textvermessung in der Spaltenbreite und doppelte Aufbauten der Seitenleiste – ergaben gemessen **336 ms → 129 ms** bei 1.584 Punkten. Bei Änderungen besonders prüfen: dass jede neue teure Auswertung durch `render_cached` läuft und dass `save_items` den Zwischenspeicher leert – ein vergessener Aufruf zeigt alte Zahlen, ohne dass ein Test zwangsläufig anschlägt. [Leistung und Oberfläche](51_LEISTUNG_UND_OBERFLAECHE_3.23.0.md).

**Austauschformat.** `.glideexchange` trägt Struktur, Reihenfolge, Checklisten, Metadaten und stabile IDs verlustfrei durch den Rundlauf KI → Glide → Bearbeitung → Export → KI. Bei Änderungen besonders prüfen: dass stabile IDs beim Export erhalten und beim Import wiedergefunden werden (sonst dupliziert der zweite Rundlauf den Bestand), dass die drei Grenzen **vor** jeder Bestandsänderung greifen und dass die Markdown-Ebene nur liest, was die maschinenlesbare Ebene auch schreiben kann. [Austauschformat](52_AUSTAUSCHFORMAT_3.23.0.md).

**Arbeitsfläche.** Die Pinnwand kennt Verbindungen zwischen Karten, einen Fokusmodus innerhalb des Fensters und eine Flächenausgabe als PDF. Bei Änderungen besonders prüfen: dass `normalize_settings` Verbindungen zu entfernten Karten verwirft, dass `unpin` die zugehörigen Verbindungen mit abräumt und dass die Druckgeometrie aus der belegten Fläche kommt, nicht aus dem sichtbaren Ausschnitt. [Pinnwand](53_PINNWAND_ARBEITSFLAECHE_3.23.0.md) · [Anzeigemodi](54_ANZEIGEMODI_3.23.0.md).

## Vorgängerpaket: 3.21, Kalenderimport aus ICS

Bei Änderungen besonders prüfen: dass `unfold_ics_lines` gefaltete Zeilen vor dem Zerlegen zusammenfügt, dass `parse_ics_property` Doppelpunkte in Anführungszeichen überliest, dass `ics_repeat_from_rule` streng bleibt und Unabbildbares verwirft statt vereinfacht, dass eigene UIDs weiterhin als Duplikat gelten und dass ein fehlgeschlagener Import Labelbestand und Rückgängig-Stapel exakt zurücksetzt. [Bedienung 3.21](45_KALENDERIMPORT_3.21.0.md).

Genau ein Abschnitt dieses Dokuments bezeichnet ein Funktionspaket als das zuletzt umgesetzte; alle älteren stehen als Vorgängerpakete darunter. Bis 3.21.2 stand derselbe Satz dreimal darin – bei 3.15, 3.16 und 3.21 –, was den Einstieg in die Technik irreführend machte.

## Folgestände zu 3.21

**3.21.1** behob zwei Zeitzonenfehler im ICS-Rundlauf und einen Fehler im Prüfstand. `UNTIL` trägt in der Ausgabe dieselbe Zeitform wie `DTSTART` – ohne „Z“ beim Uhrzeittermin, als reines Datum beim Ganztagstermin; beim Lesen nimmt `parse_ics_until` den Kalendertag **ohne** Zeitzonenumrechnung, weil `UNTIL` eine Datumsgrenze ist und kein Zeitpunkt. Im Prüfstand bleiben die Verlaufszeiten (`history[].at`) aus dem Fixture-Abgleich heraus, genauso wie `exported_at`; Suiten laufen ohne eigene Vorgabe unter `TZ=Europe/Berlin`. Bei Änderungen besonders prüfen: dass keine Ausgabe ein `UNTIL` mit „Z“ schreibt und dass der Fixture-Abgleich keine beim Speichern entstehenden Zeiten vergleicht.

**3.21.2** erweiterte den mitgelieferten Beispielbestand und den Vorlagenkatalog auf die Funktionen seit 3.14: beide Erinnerungsarten, alle sechs Wiederholungsarten, sieben Bearbeitungstage, sechs Aufwandsangaben, 166 Punkte in 12 Listen. `tests/tools/releasedaten.py` bindet seine Standangaben an `APP_VERSION` und `DATA_SCHEMA_VERSION`. Anwendungscode unverändert.

**3.21.3** ergänzt `tests/tools/standpruefung.py` als dritte Analyse: Sie vergleicht jede aktive Standangabe der Ablage mit `VERSION` und verlangt, dass festgeschriebene Dokumente – Version oder Datum im Dateinamen, Versionsordner im Pfad oder „historisch“ im Titel – keinen aktuellen Stand behaupten. Anlass waren sieben Dokumente, die zwei Versionssprünge lang auf 3.21.0 standen, ohne dass eine Prüfung das finden konnte. Bei Änderungen besonders prüfen: dass Zitate und Codespannen weiterhin aus der Bewertung fallen, sonst meldet die Prüfung den Satz, der einen Fehler dokumentiert. Anwendungscode unverändert. [Prüfungen und Umfang](../tests/README.md).

**3.21.4** ist ein Korrekturstand aus einem vollständigen Durchgang durch alle 93 aktiven Dokumente: zehn aufgeführte falsche Aussagen über den Anwendungscode, fünf überholte Formatstufen, acht falsche Verweise und sieben Gegenwartsbehauptungen in historischen Dokumenten. Für die Technik am wichtigsten: Die Kalenderausgabe erzeugt aus einem Bearbeitungstag **auch ohne Fälligkeit** einen Planungstermin – der Bedienvertrag schloss das aus –, und `SEQUENCE` steht fest auf `0`, die Termin-Identität trägt allein die stabile `UID`. `standpruefung.py` prüft seit diesem Stand auch Formatstufen gegen `DATA_SCHEMA_VERSION`. Bei Änderungen besonders prüfen: dass eine Formatstufe nicht als Literal in Prosa wandert, sondern aus dem Code kommt. Anwendungscode unverändert. [Prüfungen und Umfang](../tests/README.md).

## Bestand aus den Vorgängerständen

**3.20** brachte die Kalenderausgabe als ICS. Bei Änderungen besonders prüfen: dass jede Ausgabezeile durch `fold_ics_line` läuft (die Faltung zählt Oktette, nicht Zeichen), dass jeder Textwert durch `escape_ics_text` geht, dass Ganztagstermine ihr `DTEND` am Folgetag tragen, dass die UID je Punkt stabil bleibt und Bearbeitungstage eine eigene tragen, und dass die Ausgabe weder Bestand noch Änderungsverlauf berührt. [Bedienung 3.20](44_KALENDERAUSGABE_3.20.0.md).

**3.19** brachte den dauerhaften Änderungsverlauf mit Aufgabenformat 15. Bei Änderungen besonders prüfen: dass `update_history` in jedem Speicherweg läuft und den Vergleichsstand nachführt (auch bei abgeschalteter Protokollierung), dass `normalize_lists_data` den gelesenen Verlauf nur in `_loaded_history` ablegt – sonst überschreibt ein fremdes Archiv das laufende Protokoll –, dass gelöschte Container ihre Punkte nicht einzeln melden, dass Sammeleinträge und Obergrenze greifen und dass ein defektes `history`-Feld verworfen wird, ohne die Aufgaben zu berühren. [Bedienung 3.19](43_AENDERUNGSVERLAUF_3.19.0.md).

**3.18** brachte den CSV-Import mit Spaltenzuordnung. Bei Änderungen besonders prüfen: dass `read_csv_table` die Zeilenenden mit `keepends` erhält (sonst verliert ein mehrzeiliger Aufgabentext den Rundlauf), dass jede Zelle durch `clean_csv_cell` läuft, dass Gruppen und Überschriften keine Status- und Fristangaben übernehmen, dass die drei Grenzen vor jeder Bestandsänderung greifen und dass ein fehlgeschlagener Import Labelbestand und Rückgängig-Stapel exakt zurücksetzt. [Bedienung 3.18](42_CSV_IMPORT_3.18.0.md).

**3.17** brachte die Druck- und PDF-Ausgabe über eine eigenständige HTML-Druckansicht. Bei Änderungen dort besonders prüfen: dass die Datei keine externen Verweise erhält, dass jeder ausgegebene Text durch `escape_print_text` läuft, dass die Obergrenze greift und dass Nutzdatendateien als Ziel abgewiesen bleiben. [Bedienung 3.17](41_DRUCK_UND_PDF_3.17.0.md).

**3.16** brachte das vollständige App-Backup mit Inhaltsvorschau. Bei Änderungen besonders prüfen: dass der Zusatzabschnitt neben den Aufgabenfeldern bleibt, dass die Aufgaben weiter durch `import_full_backup` laufen, dass vor jedem Ersetzen die drei Sicherungen entstehen und dass Ansichtsverweise ohne die zugehörigen Aufgaben verworfen werden. [Bedienung 3.16](40_APP_BACKUP_3.16.0.md).

**3.15** brachte die Systemansicht „Tagesplanung“ über `planned_date`, die Einstellung `daily_capacity_minutes` und eine gemeinsame Rechenstelle für alle Aufwandssummen. Bei Änderungen besonders prüfen: dass `planning_summary` die einzige Rechenstelle bleibt, dass die Tagesmenge nur `planned_date` auswertet, dass Serien beim Vorrücken keinen künftigen Tag erzeugen und dass die Tagesschalter nur in dieser Ansicht sichtbar sind. Datenformat und Backups bleiben unverändert. [Bedienung 3.15](39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md).

**3.14** brachte Bearbeitungstag und Aufwand mit gemeinsamem Editor, Mehrfachbearbeitung, Tabelle und Punktreitern; Datenformat 14 ergänzte die Felder und sicherte ältere Originaldateien. [Bedienung 3.14](37_PLANUNG_UND_AUFWAND_3.14.0.md).

**3.10 bis 3.13** ergänzten `ItemWorkspace`, `SavedFilters` und die Schnellerfassung, `today_plan` sowie `table_columns` und die Tabellenansicht. Filter-, Tages- und Tabellenreferenzen werden beim Öffnen aus dem aktuellen Bestand erzeugt. Fachliche Änderungen verwenden vorhandene Dialoge und `item_change`; neue Ansichtsstatus liegen additiv in den Einstellungen. [Bedienvertrag 3.13](36_TABELLENANSICHT_3.13.0.md).

**3.9** bleibt mit eingebetteten `DropdownPopup`-Frames ohne eigenen Grab erhalten. Temporäre Bindtags müssen sauber verschwinden. App-Aktionen leiten sich weiterhin aus dem tatsächlichen Menübaum ab. `reminder` bleibt die technische Bezeichnung; keine Systemzustellung bei beendetem Programm.

## Architektur und Randbedingungen

`refresh_tree` baut weiterhin den normalen Aufgabenbaum und aktualisiert danach den Workspace. Beim Laden wird `_workspace_ready` erst nach vollständigem Datenladen gesetzt, damit gespeicherte Referenzen nicht vorzeitig bereinigt werden. Die ursprüngliche Pack-Reihenfolge wird vor der bestehenden Startseitenlogik wiederhergestellt. Einstellungen enthalten `open_tabs`, `active_tab` und `pinboards`; keine Punktkopien oder neuen Statusfelder. Pruning entfernt fehlende oder ungeeignete IDs. LRU begrenzt Punktreiter global auf zwölf; je Pinnwand höchstens 500 Karten.

Bei Änderungen besonders prüfen: Quellenwechsel, Papierkorb und Rückgängig, Wiederholung und Tageszählung, Dialogfokus, Pack-Reihenfolge nach Startseite, schmale Fenster, Tastaturbewegung und Wiederherstellung der Einstellungen. Aufgabenbackups bleiben ohne Sichtzustände.

## Änderungsdisziplin

Vor Änderungen `AGENTS.md` lesen, Ausgangstests prüfen, nur temporäre `GLIDE_DATA_DIR` verwenden. Änderungen an Punkten über `item_change`, an Listen und Ordnern über `sidebar_change`, Struktur über `guarded_structural_change`, Dialoge über `run_modal`. Dokumente vor dem Ersetzen im gleichnamigen Unterarchiv sichern.

Zwei Prüfstandsregeln, die sich nicht aus dem Code ergeben: Prüfläufe nicht in UTC – bei Versatz null ist jeder Zeitzonenfehler unsichtbar, `pruefen.py` setzt darum `TZ=Europe/Berlin`, wenn der Aufrufer keine Zone vorgibt. Und: Ein Abgleich gegen die eigene Neuerzeugung findet keinen Textfehler, weil Fixture und Neuerzeugung denselben überholten Text tragen; Standangaben und Farben gehören deshalb an Konstanten gebunden und gegen die App geprüft.

[Aktueller QA-Bericht](07_QA_BERICHT.md) · [Freigabegrenzen](10_RELEASE_CHECKLIST.md) · [Prüfungen und Umfang](../tests/README.md).

## Offene Ideen

Offen sind benutzerdefinierte Felder je Liste – das wäre der nächste Formatsprung – und darauf aufbauende eigene Ansichten. Eine echte Kalendersynchronisierung mit Konfliktregeln, Löschweitergabe und Abonnements bleibt bewusst außen vor; der Import legt an und erkennt eigene Punkte über die `UID` wieder, aktualisiert aber keine vorhandenen. Die Arbeitsfläche ist mit 3.23.0 um Verbindungen, Fokusmodus und Flächenausgabe erweitert; freies Zeichnen und ein eigenständiges Markenmaskottchen bleiben offen und sind separat zu planen. Keine zusätzliche Projektmappe und keine parallele Statusablage. [Offene Entscheidungen](../../../00_Arbeitsvorbereitung/Entscheidungen/Offene_Entscheidungen_3.23.0.md) · [Arbeitsbegleiter](decisions/ARBEITSBEGLEITER.md).
