# Glide – Einstieg in die Arbeitsablage

**Neu in 3.30** – die Modernisierung nach dem Aufgabenkatalog vom 25.09.2026:

- eine **Pixel-Werkstatt** mit Flächen von 16 bis 128 Zellen, sieben
  Werkzeugen, zwei Farben, Symmetrie, Mustern, Paletten, Rückgängig je Aktion
  und PNG-Export;
- **Pixelsymbole** für Listen und Ordner;
- eine **Startseite**, die man direkt auf der Seite ordnet, dazu angeheftete
  Seiten und Filter;
- **Seiten- und Befehlssuche** mit Strg/Cmd+O;
- ein **Spaltenboard**, das ein Feld setzt, sobald man eine Karte in eine
  andere Spalte zieht;
- **Pinnwand-Bereiche**, beschriftete Verbindungen und ein Präsentationsmodus;
- ein **Tagebuch** für alle Inhaltsarten;
- verknüpfte Punkte, Abhängigkeiten und Zeiterfassung;
- das **Archiv** statt Löschen;
- das Design **„Pixel“** mit der Pixelschrift „Pixelify Sans“;
- im Ausbau: Zeitblöcke ziehen, Folien als PDF, Rückgängig beim
  Kartenverschieben, ein Detailbereich mit allen Feldern und Gismo in
  Leerzuständen;
- im zweiten Ausbau (26.09.2026):
  - Anhänge direkt im Detailbereich;
  - Zeichnungen als Bild in Folien;
  - ein Stundenraster neben „Mein Tag“;
  - Gruppierung, die Überschriften und Nummern erhält.

**Nach dem Update Glide 3.29 nicht mehr starten:** Es überschreibt einen
Bestand im Format 20 bei der ersten Eingabe. Zurück nur über die Vorsicherung
`liste_vor_format20_*.json`.

Das Aufgabenformat ist jetzt 20.
[Modernisierung 3.30](01_Repository/Glide/docs/66_MODERNISIERUNG_3.30.0.md).

Neu in 3.29: **Zeichnungsseiten** als eigene Listenart. Die 128-×-128-Fläche
liegt direkt in der Seitenanzeige von Listen, Ordnern und Tagebüchern, speichert
automatisch und kann ein PNG als Referenz zeigen oder nachzeichnen.
[Zeichnungsseite 3.29](01_Repository/Glide/docs/65_ZEICHNUNGSSEITE_3.29.0.md).

Neu in 3.28: Tagebuchordner, datierte Notizseiten und vier Tagebuchvorlagen,
ein pflegbarer Gismo, eine informativere Pinnwandvorschau, kontinuierliches
Scrollen mit gedrücktem Mausrad und eine klar priorisierte Oberfläche für
schmale Fenster. Der nach dem Füttern sichtbare weiße Neuaufbau wurde behoben:
Gismo aktualisiert nur noch seine eigene Karte. [Tagebuch und UI](01_Repository/Glide/docs/59_TAGEBUCH_UND_UI_3.28.0.md) ·
[Flackern und Ablageprüfung](01_Repository/Glide/docs/60_FLACKERN_UND_ABLAGEPRUEFUNG_3.28.0.md).

Aktueller Entwicklungsstand: **3.30.0 vom 26.09.2026**, Datenformat 20. Die
Gesamtfreigabe richtet sich nach dem [QA-Bericht](01_Repository/Glide/docs/07_QA_BERICHT.md);
ein Entwicklungsstand ist kein signiertes Release.

Durchgehende Grundlage, unabhängig von der jeweils neuesten Funktion:
verschachtelte Listen, Standard- und Tagebuchordner, Aufgaben, Long-Tasks,
Gruppen, Überschriften, Notizen, Fälligkeit, Wichtigkeit, Wiederholungen,
Erinnerungen, Labels, lokale Anhänge, Kalender, Suche, Rückgängig, Papierkorb,
16 vollständige Praxisvorlagen plus vier Tagebuchvorlagen sowie lokale Backups.

[3.14-Bedienung: Bearbeitungstag und Aufwand](01_Repository/Glide/docs/archiv/37_PLANUNG_UND_AUFWAND_3.14.0.md) · [3.13-Bedienung: Tabellenansicht](01_Repository/Glide/docs/archiv/36_TABELLENANSICHT_3.13.0.md).

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

[Erinnerungen: Bedienung und Grenzen](01_Repository/Glide/docs/archiv/31_ERINNERUNGEN_3.8.0.md) ·
[Warum es keine Systembenachrichtigung gibt](01_Repository/Glide/docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md) ·
[Vorlagenanleitung](01_Repository/Glide/docs/27_VORLAGEN_PRAXISANLEITUNG.md) ·
[Ablageprotokoll](01_Repository/Glide/docs/archiv/28_ABLAGEPRUEFUNG_2026-09-11.md)

Die automatisierte Vollprüfung von 3.30.0 nach dem zweiten Ausbau vom
26.09.2026 ist vollständig grün (Exitcode 0, 52 Schritte). Eine Freigabe ist das nicht. Offen bleiben:

- die manuelle Prüfung unter echtem Windows und macOS,
- DPI-Skalierung und Bildschirmleser,
- Signatur, Markenprüfung und Store.

[Aktueller QA-Bericht](01_Repository/Glide/docs/07_QA_BERICHT.md).

Alte Arbeitsversionen wurden nachvollziehbar in lokale Archiv-Unterordner verschoben.
Es wurden keine Dateien endgültig gelöscht und keine echten Nutzdaten importiert.

[Zeichenflächen-Aufgabensammlung](00_Arbeitsvorbereitung/Glide_Aufgabensammlung_Zeichenflaeche_2026-09-23.md) ·
[Kalenderimport aus ICS 3.21](01_Repository/Glide/docs/45_KALENDERIMPORT_3.21.0.md) ·
[Kalenderausgabe als ICS 3.20](01_Repository/Glide/docs/archiv/44_KALENDERAUSGABE_3.20.0.md) ·
[Dauerhafter Änderungsverlauf 3.19](01_Repository/Glide/docs/archiv/43_AENDERUNGSVERLAUF_3.19.0.md) ·
[CSV-Import mit Spaltenzuordnung 3.18](01_Repository/Glide/docs/archiv/42_CSV_IMPORT_3.18.0.md) ·
[Druck- und PDF-Ausgabe 3.17](01_Repository/Glide/docs/archiv/41_DRUCK_UND_PDF_3.17.0.md) ·
[Dokumentationsindex](01_Repository/Glide/docs/00_INDEX.md)
