# Release-Checkliste – Glide 3.16.0

Stand 13.09.2026 · interner Entwicklungsstand · Aufgabenformat 14

## Quellstand

- Version, App-Konstante, Hauptsuite, Changelog und aktuelle Release-Fixtures auf 3.16.0 abstimmen.
- Zwanzig Suiten plus Syntax, Dokumentverweise, Daten-Fixtures, zwei Analysen und Reproduktion vollständig prüfen.
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

3.11 ergänzt Schnellerfassung und gespeicherte Filter; 3.12 ergänzt „Mein Tag“; 3.13 ergänzt die Tabellenansicht. Die neuen Einstellungen sind additiv; Aufgabenformat 14 und Backups führen seit 3.14 zusätzlich Bearbeitungstag und Aufwand mit. [Bedienung und Grenzen](36_TABELLENANSICHT_3.13.0.md).

Für 3.14 zusätzlich alte Daten in isolierter Ablage auf Format 14 migrieren; Rückfallkopie vergleichen, Mehrfachbearbeitung und Undo prüfen, Planungsfelder in Vorlagen/Backup/Export abgleichen. Ältere Apps dürfen Format 14 nicht öffnen. [Bedienung 3.14](37_PLANUNG_UND_AUFWAND_3.14.0.md).

Für 3.16 zusätzlich das App-Backup abnehmen: Archiv schreiben und in einer isolierten Ablage wiederherstellen, Inhaltsvorschau gegen den tatsächlichen Inhalt prüfen, jeden Bereich einzeln übernehmen, Abbruch und leere Auswahl testen, die drei Rückfallsicherungen im Backup-Ordner kontrollieren und ein `.glideapp` gegenprüfen, das als Aufgabenbackup geladen wird. [Bedienung 3.16](40_APP_BACKUP_3.16.0.md).

Für 3.15 zusätzlich Tagesplanung und Tageskapazität abnehmen: Tageswechsel und Zähler, Summen in Tagesplanung, „Mein Tag", Tabelle und Startseite, Kapazität 0/1/1440 und ungültige Eingaben, Kontextmenü zum Verschieben und Entfernen des Bearbeitungstags, Sichtbarkeit der Tagesschalter nur in dieser Ansicht. Das Datenformat bleibt 14; ein Downgrade auf 3.14 verliert nur die Kapazitätseinstellung. [Bedienung 3.15](39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md).
