# Release-Checkliste – Glide 3.13.0

Stand 13.09.2026 · interner Entwicklungsstand · Aufgabenformat 13

## Quellstand

- Version, App-Konstante, Hauptsuite, Changelog und aktuelle Release-Fixtures auf 3.13.0 abstimmen.
- Sechzehn Suiten plus Syntax, Dokumentverweise, Daten-Fixtures, zwei Analysen und Reproduktion vollständig prüfen.
- Startbare Kopie und Ressourcen mit kanonischem Stand per SHA-256 vergleichen.
- Prüfergebnis und offene Fälle im [QA-Bericht](07_QA_BERICHT.md) festhalten.
- [3.13-Bedienvertrag](36_TABELLENANSICHT_3.13.0.md), [3.12-Bedienvertrag](35_MEIN_TAG_3.12.0.md), [3.11-Bedienvertrag](34_SCHNELLERFASSUNG_UND_FILTER_3.11.0.md) und den weitergeführten [3.9-Bestand](32_UI_UND_BEDIENUNG_3.9.0.md) mit der Oberfläche abgleichen.

## Noch erforderliche Plattformabnahme

- Native Windows-Prüfung der einheitlichen Auswahlfelder und des Benachrichtigungsbaums.
- Reale macOS-/Windows-Bedienung mit Trackpad/Maus, App-Wechsel und verschachtelten Dialogen.
- DPI/Monitore, Screenreader, lange Namen, kleine Bildschirme, Hochkontrast/RDP.
- Dock-/Taskleistenaufmerksamkeit und physisches Schlafen/Aufwachen.
- Dauerlauf und sequenzieller Wechsel real synchronisierter Datenordner.

## Veröffentlichung

Publisher, stabile Plattformidentitäten, Lizenzmodell und Markenprüfung bleiben gesondert festzulegen. Installer/App-Bundle, Signatur, Notarisierung/Gatekeeper, Clean-Machine-Prüfung und Storematerial sind weiterhin offen. Grüne Quelltests bedeuten kein signiertes Binärpaket oder öffentliches Stable-Release.

Die UI-Bezeichnung Benachrichtigungen darf nicht als Systemzustellung bei beendetem Programm beworben werden. [Systemintegrationsentscheidung](decisions/SYSTEMBENACHRICHTIGUNGEN.md).

3.11 ergänzt Schnellerfassung und gespeicherte Filter; 3.12 ergänzt „Mein Tag“; 3.13 ergänzt die Tabellenansicht. Die neuen Einstellungen sind additiv; Aufgabenformat 13 und Backups bleiben unverändert. [Bedienung und Grenzen](36_TABELLENANSICHT_3.13.0.md).
