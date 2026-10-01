# Projektübergabe – Glide 3.11.0

Stand 13.09.2026 · Aufgabenformat 13 · Einstellungen 2 · Vorlagen 2

Kanonisch: `src/glide/app.pyw`. Startbare Kopie im äußeren Ordner `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.11.0.pyw`, mit vollständigen Ressourcen. Kein Git-Checkout, unveröffentlichter Entwicklungsstand.

3.10 ergänzt `ItemWorkspace`; 3.11 ergänzt `SavedFilters` und die Schnellerfassung. Filterreferenzen werden beim Öffnen aus dem aktuellen Bestand erzeugt, relative Fälligkeiten verwenden den aktuellen Tag. Fachliche Änderungen verwenden vorhandene Dialoge und `item_change`; `saved_filters` und `active_saved_filter` liegen additiv in den Einstellungen. [Bedienvertrag](34_SCHNELLERFASSUNG_UND_FILTER_3.11.0.md).

`refresh_tree` baut weiterhin den normalen Aufgabenbaum und aktualisiert danach den Workspace. Beim Laden wird `_workspace_ready` erst nach vollständigem Datenladen gesetzt, damit gespeicherte Referenzen nicht vorzeitig bereinigt werden. Die ursprüngliche Pack-Reihenfolge wird vor der bestehenden Startseitenlogik wiederhergestellt. Einstellungen enthalten `open_tabs`, `active_tab` und `pinboards`; keine Punktkopien oder neuen Statusfelder. Pruning entfernt fehlende/ungeeignete IDs. LRU begrenzt Punktreiter global auf zwölf; je Pinnwand höchstens 500 Karten.

Bei Änderungen besonders prüfen: Quellenwechsel, Papierkorb/Undo, Wiederholung und Tageszählung, Dialogfokus, Pack-Reihenfolge nach Startseite, schmale Fenster, Tastaturbewegung und Wiederherstellung der Einstellungen. Aufgabenbackups bleiben ohne Sichtzustände.

3.9-Popups bleiben eingebettete `DropdownPopup`-Frames ohne eigenen Grab. Temporäre Bindtags müssen sauber verschwinden. App-Aktionen leiten sich weiterhin aus dem tatsächlichen Menübaum ab. `reminder` bleibt die technische Bezeichnung; keine Systemzustellung bei beendetem Programm.

Vor Änderungen `AGENTS.md` lesen, Ausgangstests prüfen, nur temporäre `GLIDE_DATA_DIR` verwenden. Änderungen an Punkten über `item_change`, an Listen/Ordnern über `sidebar_change`, Struktur über `guarded_structural_change`, Dialoge über `run_modal`. Dokumente vor Ersetzen im gleichnamigen Unterarchiv sichern.

[Aktueller QA-Bericht](07_QA_BERICHT.md) · [Freigabegrenzen](10_RELEASE_CHECKLIST.md).
