# Glide Produktdatenblatt 3.16.0

Neu in 3.16: Ein vollständiges App-Backup sichert Aufgaben, Anhänge, persönliche Einstellungen, Vorlagenkatalog und Aktivitätsdaten in einem Archiv. Vor dem Wiederherstellen zeigt eine Inhaltsvorschau, was darin steckt; jeder Bereich ist einzeln zuschaltbar. [Bedienung und Datenregeln](../01_Repository/Glide/docs/40_APP_BACKUP_3.16.0.md).

Stand: 13.09.2026 · lokaler Entwicklungsstand · Aufgabenformat 14 ·
Einstellungen 2 · Vorlagenformat 2

Glide ist eine deutschsprachige lokale Desktop-App für Aufgaben, Listen,
verschachtelte Ordner und Notizen. Python/Tk und die Standardbibliothek bilden
die Laufzeitbasis; Konto, Server und Synchronisationsdienst sind nicht nötig.

## Funktionsumfang

| Bereich | Vorhandene Leistung |
|---|---|
| Struktur | Listen, Ordner, Aufgaben, Long-Tasks, Gruppen, Überschriften und Unterpunkte |
| Planung | Fälligkeit mit Uhrzeit, Wichtigkeit, Wiederholungen, Kalender, lokale Benachrichtigungsübersicht sowie freiwilliger Bearbeitungstag und geschätzter Aufwand |
| Ansichten | Liste, kompakte Tabellenansicht mit wählbaren Spalten, „Mein Tag“, Tagesplanung mit Aufwandssumme und Tageskapazität, Reiter und Pinnwand |
| Inhalt | Beschreibungen, Farben, Labels und lokale Anhänge an Punkten, Listen und Ordnern |
| Bedienung | Suche, Offen-Filter, gespeicherte Filter, Mehrfachauswahl, Ziehen, Rückgängig und Papierkorb |
| Vorlagen | 16 Praxisvorlagen, eigener Katalog, Bearbeiten, Speichern, Import und Export |
| Austausch | TXT-/Markdown-/CSV-Export, portable Backups, vollständiges App-Backup mit Inhaltsvorschau und ergänzender Listen-/Ordnerimport |
| Darstellung | Hell/Dunkel, Akzentfarbe, drei Schriftgrößen und mitgelieferte DejaVu-Sans-Schrift |

Alle Ansichten bearbeiten dieselben Aufgabenobjekte. Tabellen-Spalten,
„Mein Tag“, Reiter, Pinnwand, gespeicherte Filter und die Tageskapazität sind
persönliche Einstellungen und werden nicht in Aufgabenbackups geschrieben. Die
Tagesplanung rechnet aus vorhandenen Feldern; sie ist keine Zeiterfassung und
verteilt keine Termine automatisch.

## Daten und Grenzen

Der Datenordner ist frei wählbar. Fremdsperren führen zum Schreibschutz.
Aufgabenbackups bleiben portabel und enthalten verwaltete Anhänge. Ein vollständiges
App-Backup nimmt zusätzlich persönliche Einstellungen, Vorlagenkatalog und
Aktivitätsdaten auf und stellt sie nach einer Inhaltsvorschau bereichsweise wieder her;
Cloudziel, Zeitplan und Verschlüsselung sind nicht Bestandteil. Benachrichtigungen
werden innerhalb der laufenden App verarbeitet. Bei beendetem Programm erfolgt
keine Systemzustellung.

Der 3.16-Stand ist lokal geprüft: 20 Testsuiten, statische Analysen sowie
Beispiel- und Releaseabgleiche sind erfolgreich; der abschließende macOS-Lauf
ist im QA-Bericht nachgewiesen. Native Windows-Sichtprüfung,
weitere DPI-/Monitorprofile, Accessibility, Langzeitbetrieb, Installer,
Signierung und Storefreigabe bleiben vor einer Veröffentlichung abzunehmen.

[Aktuelle Bedienung](../01_Repository/Glide/docs/40_APP_BACKUP_3.16.0.md) ·
[QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md) ·
[Dokumentationsindex](../01_Repository/Glide/docs/00_INDEX.md)
