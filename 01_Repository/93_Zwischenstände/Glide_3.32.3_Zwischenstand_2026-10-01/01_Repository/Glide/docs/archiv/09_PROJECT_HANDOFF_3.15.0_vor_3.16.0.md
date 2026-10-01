# Projektübergabe – Glide 3.15.0

Stand 13.09.2026 · Aufgabenformat 14 · Einstellungen 2 · Vorlagen 2

Kanonisch: `src/glide/app.pyw`. Startbare Kopie im äußeren Ordner `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.15.0.pyw`, mit vollständigen Ressourcen. Kein Git-Checkout, unveröffentlichter Entwicklungsstand.

3.10 ergänzt `ItemWorkspace`; 3.11 ergänzt `SavedFilters` und die Schnellerfassung; 3.12 ergänzt `today_plan`; 3.13 ergänzt `table_columns` und die Tabellenansicht. Filter-, Tages- und Tabellenreferenzen werden beim Öffnen aus dem aktuellen Bestand erzeugt. Fachliche Änderungen verwenden vorhandene Dialoge und `item_change`; neue Ansichtsstatus liegen additiv in den Einstellungen. [Bedienvertrag 3.13](36_TABELLENANSICHT_3.13.0.md).

`refresh_tree` baut weiterhin den normalen Aufgabenbaum und aktualisiert danach den Workspace. Beim Laden wird `_workspace_ready` erst nach vollständigem Datenladen gesetzt, damit gespeicherte Referenzen nicht vorzeitig bereinigt werden. Die ursprüngliche Pack-Reihenfolge wird vor der bestehenden Startseitenlogik wiederhergestellt. Einstellungen enthalten `open_tabs`, `active_tab` und `pinboards`; keine Punktkopien oder neuen Statusfelder. Pruning entfernt fehlende/ungeeignete IDs. LRU begrenzt Punktreiter global auf zwölf; je Pinnwand höchstens 500 Karten.

Bei Änderungen besonders prüfen: Quellenwechsel, Papierkorb/Undo, Wiederholung und Tageszählung, Dialogfokus, Pack-Reihenfolge nach Startseite, schmale Fenster, Tastaturbewegung und Wiederherstellung der Einstellungen. Aufgabenbackups bleiben ohne Sichtzustände.

3.9-Popups bleiben eingebettete `DropdownPopup`-Frames ohne eigenen Grab. Temporäre Bindtags müssen sauber verschwinden. App-Aktionen leiten sich weiterhin aus dem tatsächlichen Menübaum ab. `reminder` bleibt die technische Bezeichnung; keine Systemzustellung bei beendetem Programm.

Vor Änderungen `AGENTS.md` lesen, Ausgangstests prüfen, nur temporäre `GLIDE_DATA_DIR` verwenden. Änderungen an Punkten über `item_change`, an Listen/Ordnern über `sidebar_change`, Struktur über `guarded_structural_change`, Dialoge über `run_modal`. Dokumente vor Ersetzen im gleichnamigen Unterarchiv sichern.

[Aktueller QA-Bericht](07_QA_BERICHT.md) · [Freigabegrenzen](10_RELEASE_CHECKLIST.md).

3.14 brachte Bearbeitungstag und Aufwand mit gemeinsamem Editor, Mehrfachbearbeitung, Tabelle und Punktreitern; Datenformat 14 ergänzt die Felder und sichert ältere Originaldateien. [Bedienung 3.14](37_PLANUNG_UND_AUFWAND_3.14.0.md).

3.15 ist das zuletzt umgesetzte Funktionspaket: die Systemansicht „Tagesplanung" über `planned_date`, die Einstellung `daily_capacity_minutes` und eine gemeinsame Rechenstelle für alle Aufwandssummen. Bei Änderungen besonders prüfen: dass `planning_summary` die einzige Rechenstelle bleibt, dass die Tagesmenge nur `planned_date` auswertet, dass Serien beim Vorrücken keinen künftigen Tag erzeugen und dass die Tagesschalter nur in dieser Ansicht sichtbar sind. Datenformat und Backups bleiben unverändert. [Bedienung 3.15](39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md).

Die nächste offene Idee ist ein vollständiges App-Backup mit Vorschau, einschließlich Einstellungen und Vorlagenkatalog; der vorhandene Aufgabenbackup ist weiterhin enger gefasst.
