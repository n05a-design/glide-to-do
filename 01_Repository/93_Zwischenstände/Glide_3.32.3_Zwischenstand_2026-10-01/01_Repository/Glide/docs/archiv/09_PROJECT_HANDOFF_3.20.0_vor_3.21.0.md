# Projektübergabe – Glide 3.20.0

Stand 13.09.2026 · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2

Kanonisch: `src/glide/app.pyw`. Startbare Kopie im äußeren Ordner `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.20.0.pyw`, mit vollständigen Ressourcen. Kein Git-Checkout, unveröffentlichter Entwicklungsstand.

3.10 ergänzt `ItemWorkspace`; 3.11 ergänzt `SavedFilters` und die Schnellerfassung; 3.12 ergänzt `today_plan`; 3.13 ergänzt `table_columns` und die Tabellenansicht. Filter-, Tages- und Tabellenreferenzen werden beim Öffnen aus dem aktuellen Bestand erzeugt. Fachliche Änderungen verwenden vorhandene Dialoge und `item_change`; neue Ansichtsstatus liegen additiv in den Einstellungen. [Bedienvertrag 3.13](36_TABELLENANSICHT_3.13.0.md).

`refresh_tree` baut weiterhin den normalen Aufgabenbaum und aktualisiert danach den Workspace. Beim Laden wird `_workspace_ready` erst nach vollständigem Datenladen gesetzt, damit gespeicherte Referenzen nicht vorzeitig bereinigt werden. Die ursprüngliche Pack-Reihenfolge wird vor der bestehenden Startseitenlogik wiederhergestellt. Einstellungen enthalten `open_tabs`, `active_tab` und `pinboards`; keine Punktkopien oder neuen Statusfelder. Pruning entfernt fehlende/ungeeignete IDs. LRU begrenzt Punktreiter global auf zwölf; je Pinnwand höchstens 500 Karten.

Bei Änderungen besonders prüfen: Quellenwechsel, Papierkorb/Undo, Wiederholung und Tageszählung, Dialogfokus, Pack-Reihenfolge nach Startseite, schmale Fenster, Tastaturbewegung und Wiederherstellung der Einstellungen. Aufgabenbackups bleiben ohne Sichtzustände.

3.9-Popups bleiben eingebettete `DropdownPopup`-Frames ohne eigenen Grab. Temporäre Bindtags müssen sauber verschwinden. App-Aktionen leiten sich weiterhin aus dem tatsächlichen Menübaum ab. `reminder` bleibt die technische Bezeichnung; keine Systemzustellung bei beendetem Programm.

Vor Änderungen `AGENTS.md` lesen, Ausgangstests prüfen, nur temporäre `GLIDE_DATA_DIR` verwenden. Änderungen an Punkten über `item_change`, an Listen/Ordnern über `sidebar_change`, Struktur über `guarded_structural_change`, Dialoge über `run_modal`. Dokumente vor Ersetzen im gleichnamigen Unterarchiv sichern.

[Aktueller QA-Bericht](07_QA_BERICHT.md) · [Freigabegrenzen](10_RELEASE_CHECKLIST.md).

3.14 brachte Bearbeitungstag und Aufwand mit gemeinsamem Editor, Mehrfachbearbeitung, Tabelle und Punktreitern; Datenformat 14 ergänzt die Felder und sichert ältere Originaldateien. [Bedienung 3.14](37_PLANUNG_UND_AUFWAND_3.14.0.md).

3.15 ist das zuletzt umgesetzte Funktionspaket: die Systemansicht „Tagesplanung" über `planned_date`, die Einstellung `daily_capacity_minutes` und eine gemeinsame Rechenstelle für alle Aufwandssummen. Bei Änderungen besonders prüfen: dass `planning_summary` die einzige Rechenstelle bleibt, dass die Tagesmenge nur `planned_date` auswertet, dass Serien beim Vorrücken keinen künftigen Tag erzeugen und dass die Tagesschalter nur in dieser Ansicht sichtbar sind. Datenformat und Backups bleiben unverändert. [Bedienung 3.15](39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md).

3.16 ist das zuletzt umgesetzte Funktionspaket: das vollständige App-Backup mit Inhaltsvorschau. Bei Änderungen besonders prüfen: dass der Zusatzabschnitt neben den Aufgabenfeldern bleibt, dass die Aufgaben weiter durch `import_full_backup` laufen, dass vor jedem Ersetzen die drei Sicherungen entstehen und dass Ansichtsverweise ohne die zugehörigen Aufgaben verworfen werden. [Bedienung 3.16](40_APP_BACKUP_3.16.0.md).

3.20 ist das zuletzt umgesetzte Funktionspaket: die Kalenderausgabe als ICS. Bei Änderungen besonders prüfen: dass jede Ausgabezeile durch `fold_ics_line` läuft (die Faltung zählt Oktette, nicht Zeichen), dass jeder Textwert durch `escape_ics_text` geht, dass Ganztagstermine ihr `DTEND` am Folgetag tragen, dass die UID je Punkt stabil bleibt und Bearbeitungstage eine eigene tragen, und dass die Ausgabe weder Bestand noch Änderungsverlauf berührt. [Bedienung 3.20](44_KALENDERAUSGABE_3.20.0.md).

3.19 brachte den dauerhaften Änderungsverlauf mit Aufgabenformat 15. Bei Änderungen besonders prüfen: dass `update_history` in jedem Speicherweg läuft und den Vergleichsstand nachführt (auch bei abgeschalteter Protokollierung), dass `normalize_lists_data` den gelesenen Verlauf nur in `_loaded_history` ablegt – sonst überschreibt ein fremdes Archiv das laufende Protokoll –, dass gelöschte Container ihre Punkte nicht einzeln melden, dass Sammeleinträge und Obergrenze greifen und dass ein defektes `history`-Feld verworfen wird, ohne die Aufgaben zu berühren. [Bedienung 3.19](43_AENDERUNGSVERLAUF_3.19.0.md).

3.18 brachte den CSV-Import mit Spaltenzuordnung. Bei Änderungen besonders prüfen: dass `read_csv_table` die Zeilenenden mit `keepends` erhält (sonst verliert ein mehrzeiliger Aufgabentext den Rundlauf), dass jede Zelle durch `clean_csv_cell` läuft, dass Gruppen und Überschriften keine Status- und Fristangaben übernehmen, dass die drei Grenzen vor jeder Bestandsänderung greifen und dass ein fehlgeschlagener Import Labelbestand und Rückgängig-Stapel exakt zurücksetzt. [Bedienung 3.18](42_CSV_IMPORT_3.18.0.md).

3.17 brachte die Druck- und PDF-Ausgabe über eine eigenständige HTML-Druckansicht. Bei Änderungen dort besonders prüfen: dass die Datei keine externen Verweise erhält, dass jeder ausgegebene Text durch `escape_print_text` läuft, dass die Obergrenze greift und dass Nutzdatendateien als Ziel abgewiesen bleiben. [Bedienung 3.17](41_DRUCK_UND_PDF_3.17.0.md).

Die nächsten offenen Ideen sind ein dauerhafter Änderungsverlauf, ein CSV-Import mit Spaltenzuordnung und benutzerdefinierte Felder.
