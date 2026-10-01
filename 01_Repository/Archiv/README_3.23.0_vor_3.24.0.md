# Glide – Einstieg in die Arbeitsablage

Neu in 3.23: eine Designauswahl statt dreier Schalter, fünf Anzeigemodi der Listenansicht, ein eigenes Austauschformat für den Weg zu und von einer KI, die Pinnwand als Arbeitsfläche mit Verbindungen und Druck sowie ein messbar schnellerer Ansichtswechsel. [Designsystem](01_Repository/Glide/docs/50_DESIGNSYSTEM_3.23.0.md) · [Anzeigemodi](01_Repository/Glide/docs/54_ANZEIGEMODI_3.23.0.md) · [Austauschformat](01_Repository/Glide/docs/52_AUSTAUSCHFORMAT_3.23.0.md) · [Pinnwand](01_Repository/Glide/docs/53_PINNWAND_ARBEITSFLAECHE_3.23.0.md).

Aktueller Entwicklungsstand: **3.23.0 vom 18.09.2026**: Designsystem mit sieben Designs, Anzeigemodi der Listenansicht mit abhakbaren Checklistenschritten, Glide-Austauschformat, Pinnwand als Arbeitsfläche und ein Ansichtswechsel, der statt 336 nur noch 129 Millisekunden braucht. Davor: zusammengeführte Tagesansicht „Mein Tag“ mit Eingangsblock, Checkliste je Aufgabe, einstellbares Kachelraster auf der Startseite, sortier- und verstellbare Tabelle, ausgebaute Pinnwand, gruppierte App-Aktionen, die Farbmodi „Kontrast“ und „Dopamin“, Kalenderimport aus ICS, Kalenderausgabe als ICS, dauerhafter Änderungsverlauf, CSV-Import mit Spaltenzuordnung, Druck- und PDF-Ausgabe, vollständiges App-Backup, Tagesplanung und Tageskapazität, Bearbeitungstag und Aufwand, Tabellenansicht mit listenspezifischer Spaltenauswahl sowie „Mein Tag“, Schnellerfassung, gespeicherte Filter, Reiter und Pinnwände. Der mitgelieferte Beispielbestand deckt diese Funktionen seit 3.21.2 testbar ab: [Probedaten und Prüfwege](05_Probelisten_Testdaten/README.md).

Durchgehende Grundlage, unabhängig von der jeweils neuesten Funktion: verschachtelte Listen und Ordner, Aufgaben, Long-Tasks, Gruppen, Überschriften und Unterpunkte, Notizen, Fälligkeit mit Uhrzeit, Wichtigkeit, sechs Wiederholungsarten, Erinnerungen innerhalb der laufenden App, Labels, Farben, Beschreibungen und lokale Anhänge an Punkten, Listen und Ordnern, Kalenderansicht, Suche und Offen-Filter, Mehrfachauswahl, Ziehen, Rückgängig und Papierkorb, 16 Praxisvorlagen mit eigenem Katalog zum Bearbeiten, Importieren und Exportieren, TXT-, CSV- und Markdown-Austausch, portable Aufgabenbackups sowie Hell- und Dunkelmodus mit Akzentfarbe und drei Schriftgrößen.

[3.14-Bedienung: Bearbeitungstag und Aufwand](01_Repository/Glide/docs/37_PLANUNG_UND_AUFWAND_3.14.0.md) · [3.13-Bedienung: Tabellenansicht](01_Repository/Glide/docs/36_TABELLENANSICHT_3.13.0.md).

| Ordner | Aktueller Zweck |
|---|---|
| [01_Repository/Glide](01_Repository/Glide/README.md) | Kanonischer Quellcode, Tests und technische Dokumentation |
| [07_Python-Versionen](07_Python-Versionen/README.md) | Startbare, synchron gehaltene Python-Arbeitskopie mit Ressourcen |
| [05_Probelisten_Testdaten](05_Probelisten_Testdaten/README.md) | 16 Praxisvorlagen und zwei aktuelle Beispielbackups |
| [10_Dokumentation](10_Dokumentation/README.md) | Bedienanleitung und aktuelle Nachweise |
| [00_Arbeitsvorbereitung](00_Arbeitsvorbereitung/README.md) | Offene Entscheidungen und manuelle Prüfungen |
| [20_Grafik_Master](20_Grafik_Master/README.md) | Bestehende Grafikquellen |
| [30_Release_Exports](30_Release_Exports/README.md) | Paketierungsablage; kein neues signiertes Release erzeugt |
| [40_Store_Material](40_Store_Material/README.md) | Entwürfe für die Veröffentlichung |
| [50_Ablage](50_Ablage/README.md) | Historische QA, Screenshots und Rückfallstände |
| [90_Testdaten_Extern](90_Testdaten_Extern/README.md) | Bewusst erhaltene ältere Importbeispiele |

[Erinnerungen: Bedienung und Grenzen](01_Repository/Glide/docs/31_ERINNERUNGEN_3.8.0.md) ·
[Warum es keine Systembenachrichtigung gibt](01_Repository/Glide/docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md) ·
[Vorlagenanleitung](01_Repository/Glide/docs/27_VORLAGEN_PRAXISANLEITUNG.md) ·
[Ablageprotokoll](01_Repository/Glide/docs/28_ABLAGEPRUEFUNG_2026-09-11.md)

Der letzte vollständige Abschlusslauf auf Zielhardware gehört zu 3.21.4 und ist am 15.09.2026 abgeschlossen; der Stand 3.23.0 wird gerade nativ abgenommen. [Ablage- und Prüfnachweis](50_Ablage/Archiv/Werkzeuge_3.21.4/Ablageprotokoll_2026-09-15.md).

Alte Arbeitsversionen wurden nachvollziehbar in lokale Archiv-Unterordner verschoben.
Es wurden keine Dateien endgültig gelöscht und keine echten Nutzdaten importiert.

[Funktionsvorschläge und Prioritäten](00_Arbeitsvorbereitung/Glide_Funktionsvorschlaege_2026-09-16.md) ·
[Kalenderimport aus ICS 3.21](01_Repository/Glide/docs/45_KALENDERIMPORT_3.21.0.md) ·
[Kalenderausgabe als ICS 3.20](01_Repository/Glide/docs/44_KALENDERAUSGABE_3.20.0.md) ·
[Dauerhafter Änderungsverlauf 3.19](01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md) ·
[CSV-Import mit Spaltenzuordnung 3.18](01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md) ·
[Druck- und PDF-Ausgabe 3.17](01_Repository/Glide/docs/41_DRUCK_UND_PDF_3.17.0.md) ·
[Dokumentationsindex](01_Repository/Glide/docs/00_INDEX.md)
