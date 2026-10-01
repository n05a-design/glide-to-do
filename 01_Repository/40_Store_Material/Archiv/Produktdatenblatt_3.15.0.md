# Glide Produktdatenblatt 3.15.0

Neu in 3.15: Die Ansicht „Tagesplanung“ zeigt alle Aufgaben mit Bearbeitungstag an einem wählbaren Tag und stellt ihren geschätzten Aufwand einer selbst gesetzten Tageskapazität gegenüber. Summen erscheinen auch in „Mein Tag“, in der Tabelle und auf der Startseite. Keine Zeiterfassung und keine automatische Terminverteilung. [Bedienung und Datenregeln](../01_Repository/Glide/docs/39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md).

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
| Austausch | TXT-/Markdown-/CSV-Export, portable Backups und ergänzender Listen-/Ordnerimport |
| Darstellung | Hell/Dunkel, Akzentfarbe, drei Schriftgrößen und mitgelieferte DejaVu-Sans-Schrift |

Alle Ansichten bearbeiten dieselben Aufgabenobjekte. Tabellen-Spalten,
„Mein Tag“, Reiter, Pinnwand, gespeicherte Filter und die Tageskapazität sind
persönliche Einstellungen und werden nicht in Aufgabenbackups geschrieben. Die
Tagesplanung rechnet aus vorhandenen Feldern; sie ist keine Zeiterfassung und
verteilt keine Termine automatisch.

## Daten und Grenzen

Der Datenordner ist frei wählbar. Fremdsperren führen zum Schreibschutz.
Aufgabenbackups bleiben portabel und enthalten verwaltete Anhänge; persönliche
Einstellungen und der Vorlagenkatalog werden separat gespeichert. Benachrichtigungen
werden innerhalb der laufenden App verarbeitet. Bei beendetem Programm erfolgt
keine Systemzustellung.

Der 3.15-Stand ist lokal geprüft: 19 Testsuiten, statische Analysen sowie
Beispiel- und Releaseabgleiche sind erfolgreich; der abschließende macOS-Lauf
ist im QA-Bericht nachgewiesen. Native Windows-Sichtprüfung,
weitere DPI-/Monitorprofile, Accessibility, Langzeitbetrieb, Installer,
Signierung und Storefreigabe bleiben vor einer Veröffentlichung abzunehmen.

[Aktuelle Bedienung](../01_Repository/Glide/docs/39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md) ·
[QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md) ·
[Dokumentationsindex](../01_Repository/Glide/docs/00_INDEX.md)
