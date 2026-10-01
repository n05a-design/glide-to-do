# Projektübergabe – Glide 3.9.0

Stand 12.09.2026 · Aufgabenformat 13 · Einstellungen 2 · Vorlagen 2

Kanonisch: `src/glide/app.pyw`. Startbare Kopie im äußeren Ordner `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.9.0.pyw` mit vollständigen Ressourcen. Kein Git-Checkout, unveröffentlichter Entwicklungsstand.

3.9 vereinheitlicht Benachrichtigungsbenennung und Dropdowns, verdichtet die Kopfzeile, verschiebt Light/Dark Mode in die Einstellungen, ergänzt durchsuchbare App-Aktionen und eine ausblendbare Seitenleiste. Neue Listen/Ordner nutzen ihre Inhaltshöhe bzw. zwei Spalten. [Vollständiger Vertrag](32_UI_UND_BEDIENUNG_3.9.0.md).

Wichtig für Weiterarbeit: Popups sind jetzt `DropdownPopup`-Frames innerhalb des Elternfensters. Sie dürfen keinen eigenen modalen Grab erhalten. Temporäre Bindtags müssen beim Schließen entfernt bleiben. Alle App-Aktionen werden aus dem tatsächlichen Menübaum gelesen; keine zweite unabhängige Befehlsliste pflegen.

Daten-, Backup-, Vorlagen- und Zustellverträge bleiben erhalten. `reminder` heißt technisch weiterhin so. Benachrichtigungen funktionieren bei laufender App; geschlossene App/Systemzustellung bleibt offen. Neue Einstellungen werden additiv normalisiert. [Datenvertrag](06_DATA_BACKUP_MIGRATION.md).

Vor Änderungen `AGENTS.md` lesen, Ausgangstest durchführen und ausschließlich temporäre `GLIDE_DATA_DIR` verwenden. Aufgaben über `item_change`, Listen/Ordner über `sidebar_change`, modale Dialoge über `run_modal`. Historische Dokumente vor Ersetzung im gleichnamigen Unterarchiv sichern.

[Aktueller QA-Bericht](07_QA_BERICHT.md) · [Freigabegrenzen](10_RELEASE_CHECKLIST.md).
