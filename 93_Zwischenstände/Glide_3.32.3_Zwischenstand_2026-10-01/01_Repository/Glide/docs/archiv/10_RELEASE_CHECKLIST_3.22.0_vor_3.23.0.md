# Release-Checkliste – Glide 3.22.0

Stand 17.09.2026 · Glide 3.22.0 · interner Entwicklungsstand · Aufgabenformat 16

## Quellstand

- Version, App-Konstante, Hauptsuite, Changelog und aktuelle Release-Fixtures auf die Version aus `VERSION` abstimmen – keine Nummer in diese Zeile schreiben, sie veraltet sonst bei jedem Stand.
- Formatsprung beachten: Aufgabenformat 16, Referenz-Fixture `current_v16`, Formatstufen in der Fixtureprüfung.
- Fünfundzwanzig Suiten plus Syntax, Versions- und Dokumentprüfung, Daten-Fixtures, die drei Analysen und die Reproduktion vollständig prüfen: neununddreißig Schritte im Vollmodus, von denen regelmäßig nur Screenshot-Erzeugung und Sichtprüfung übersprungen bleiben.
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

Für 3.21 zusätzlich den Kalenderimport abnehmen: je eine Datei aus Apple Kalender, Outlook und einem Webkalender einlesen, eine Einladung mit Teilnehmern (die Angaben fehlen erwartungsgemäß), eine Serie und einen Termin mit Alarm; den Rundlauf mit der eigenen Ausgabe prüfen (keine Kopien) und den Bericht mit den Übersprungsgründen gegen die Datei halten. [Bedienung 3.21](45_KALENDERIMPORT_3.21.0.md).

Für 3.20 zusätzlich die Kalenderausgabe abnehmen: je eine Datei in Apple Kalender, Outlook und Thunderbird einlesen, Ganztags- und Uhrzeittermine, Dauer, Priorität, Kategorien und Alarme im Kalender prüfen, eine Serie über mehrere Wochen ansehen, dieselbe Datei ein zweites Mal einlesen und das tatsächliche Verhalten des Zielkalenders dokumentieren (Ersetzen, Überspringen oder Kopie); Glide liefert stabile UIDs, aber keine erhöhte SEQUENCE. [Bedienung 3.20](44_KALENDERAUSGABE_3.20.0.md).

Für 3.19 zusätzlich den Änderungsverlauf abnehmen: vor der ersten Nutzung eine Sicherung anlegen und nach dem ersten Speichern die Datei `liste_vor_format15_*.json` im Backup-Ordner prüfen, einen Arbeitstag protokollieren lassen und die Einträge gegen das tatsächliche Vorgehen halten, Massenvorgänge auf Sammeleinträge prüfen, Filter und TXT-Ausgabe durchgehen, Protokollierung ab- und wieder einschalten, Verlauf leeren und den Bestand danach kontrollieren. [Bedienung 3.19](43_AENDERUNGSVERLAUF_3.19.0.md).

Für 3.18 zusätzlich den CSV-Import abnehmen: eine mit „Als CSV“ geschriebene Liste zurücklesen und mit dem Original vergleichen, eine aus Excel und eine aus Numbers gespeicherte Datei einlesen (Semikolon und Komma, mit und ohne BOM), Umlaute im Ergebnis prüfen, Zuordnung von Hand ändern, Vorschau gegen das Ergebnis halten, beide Importziele und Rückgängig ausprobieren. [Bedienung 3.18](42_CSV_IMPORT_3.18.0.md).

Für 3.17 zusätzlich die Druckausgabe abnehmen: alle vier Formate öffnen und tatsächlich drucken beziehungsweise als PDF speichern, Optionen durchschalten, Umlaute und Sonderzeichen im Ausdruck prüfen, Seitenumbrüche bei langen Listen ansehen und den HTML-Export in einem zweiten Browser öffnen. [Bedienung 3.17](41_DRUCK_UND_PDF_3.17.0.md).

Für 3.16 zusätzlich das App-Backup abnehmen: Archiv schreiben und in einer isolierten Ablage wiederherstellen, Inhaltsvorschau gegen den tatsächlichen Inhalt prüfen, jeden Bereich einzeln übernehmen, Abbruch und leere Auswahl testen, die drei Rückfallsicherungen im Backup-Ordner kontrollieren und ein `.glideapp` gegenprüfen, das als Aufgabenbackup geladen wird. [Bedienung 3.16](40_APP_BACKUP_3.16.0.md).

Für 3.15 zusätzlich Tagesplanung und Tageskapazität abnehmen: Tageswechsel und Zähler, Summen in Tagesplanung, „Mein Tag", Tabelle und Startseite, Kapazität 0/1/1440 und ungültige Eingaben, Kontextmenü zum Verschieben und Entfernen des Bearbeitungstags, Sichtbarkeit der Tagesschalter nur in dieser Ansicht. Das Datenformat bleibt 14; ein Downgrade auf 3.14 verliert nur die Kapazitätseinstellung. [Bedienung 3.15](39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md).
