# Glide Produktdatenblatt 3.18.0

Neu in 3.18: CSV-Import mit Spaltenzuordnung. Trennzeichen und Kodierung werden erkannt und sind umstellbar, jede Spalte wird einem Glide-Feld zugeordnet, eine Vorschau zeigt das Ergebnis vor der Übernahme; eine mit „Als CSV“ geschriebene Liste ist vollständig zurücklesbar. [Bedienung und Datenregeln](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md).

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
| Austausch | TXT- und CSV-Import mit Spaltenzuordnung, TXT-/Markdown-/CSV-Export, Druckansicht für Papier und PDF, portable Backups, vollständiges App-Backup mit Inhaltsvorschau und ergänzender Listen-/Ordnerimport |
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

Der 3.18-Stand ist lokal geprüft: 22 Testsuiten, statische Analysen sowie
Beispiel- und Releaseabgleiche sind in einer Vorabumgebung erfolgreich; der
abschließende macOS-Lauf wird im QA-Bericht nachgewiesen. Native Windows-Sichtprüfung,
weitere DPI-/Monitorprofile, Accessibility, Langzeitbetrieb, Installer,
Signierung und Storefreigabe bleiben vor einer Veröffentlichung abzunehmen.

[Aktuelle Bedienung](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md) ·
[QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md) ·
[Dokumentationsindex](../01_Repository/Glide/docs/00_INDEX.md)
