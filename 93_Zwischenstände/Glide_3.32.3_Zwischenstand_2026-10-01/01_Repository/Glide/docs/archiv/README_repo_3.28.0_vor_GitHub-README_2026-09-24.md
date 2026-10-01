# Glide – Aufgaben und Listen

Neu in 3.28: Tagebuch-Ordner und datierte Notizseiten mit Favorit, Stimmung,
Ort, Schreibimpulsen, Suche und Vorlagen; ein pflegbarer Gismo; eine
aussagekräftigere Pinnwandvorschau; automatische Mausradnavigation sowie eine
klar priorisierte Oberfläche für schmale Fenster. [Tagebuch und UI 3.28](docs/59_TAGEBUCH_UND_UI_3.28.0.md) · [Übersichtlichkeit und Hierarchie](docs/57_UEBERSICHT_UND_HIERARCHIE_3.25.0.md) · [Navigation und Pinnwand](docs/55_NAVIGATION_UND_PINNWAND_3.24.0.md).

Nach der Gismo-Pflege wird nur noch die vorhandene Karte aktualisiert. Der
vorherige vollständige Startseiten-Neuaufbau und damit der besonders im
Dopamin-Design sichtbare weiße Blitz entfallen. [Ursache, Recherche und
Regressionstest](docs/60_FLACKERN_UND_ABLAGEPRUEFUNG_3.28.0.md).

Aktueller interner Entwicklungsstand: **3.28.0** · 23.09.2026 · Aufgabenformat 18 · Einstellungen 2 · Vorlagen 2

Lokale deutschsprachige Desktop-App mit Python/Tk. Ohne Konto oder neue Laufzeitabhängigkeiten. Nutzdaten liegen außerhalb des Programmordners.

Funktionsbestand: Designsystem mit neun Designs, Anzeigemodi der Listenansicht, Glide-Austauschformat, Pinnwand als Arbeitsfläche, Kalenderimport und Kalenderausgabe als ICS, dauerhafter Änderungsverlauf, CSV-Import mit Spaltenzuordnung, Druck- und PDF-Ausgabe, vollständiges App-Backup mit Inhaltsvorschau, Tagesplanung mit Tageskapazität, Bearbeitungstag und geschätzter Aufwand, Tabellenansicht mit listenspezifischen Spalten, „Mein Tag“, Schnellerfassung mit deutscher Fristvorschau, gespeicherte Filter, Reiter und Pinnwände. Alle Ansichten bearbeiten dieselben Objekte.

Durchgehende Grundlage, unabhängig von der jeweils neuesten Funktion: verschachtelte Listen und Ordner, Aufgaben, Long-Tasks, Gruppen, Überschriften und Unterpunkte, Notizen und Tagebücher, Fälligkeit mit Uhrzeit, Wichtigkeit, sechs Wiederholungsarten, Erinnerungen innerhalb der laufenden App, Labels, Farben, Beschreibungen und lokale Anhänge an Punkten, Listen und Ordnern, Kalenderansicht, Suche und Offen-Filter, Mehrfachauswahl, Ziehen, Rückgängig und Papierkorb, Praxisvorlagen mit eigenem Katalog zum Bearbeiten, Importieren und Exportieren, TXT-, CSV- und Markdown-Austausch, portable Aufgabenbackups sowie Hell- und Dunkelmodus mit Akzentfarbe und drei Schriftgrößen.

Start: `python3 src/glide/app.pyw` mit Tk-fähigem Python. Eine laufende ältere Instanz vorher schließen. Die startbare Kopie liegt im äußeren Ordner `07_Python-Versionen` und trägt die Nummer aus `VERSION`; der vollständige Nachbarordner `resources` gehört dazu.

Aufgabenformat 18 ergänzt Tagebuch-Metadaten; davor kamen Notizseiten in Format 17, Checklisten in Format 16, Verlauf in Format 15 und Planung in Format 14. Einstellungen 2 und Vorlagen 2 bleiben erhalten. Reiter/Pinnwände liegen in Einstellungen und sind kein Bestandteil eines Aufgabenbackups. Benachrichtigungen werden bei laufender App verarbeitet.

Prüfung: `python tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.28.0/abschluss` – alle Suiten und Analysen aus `tests/tools/pruefen.py`, Beispiel- und Releaseabgleich. Alle Tests verwenden isolierte Datenordner. Keine Veröffentlichung oder Signatur durch diesen Quellstand.

[Bedienung 3.21](docs/45_KALENDERIMPORT_3.21.0.md) · [Bedienung 3.20](docs/archiv/44_KALENDERAUSGABE_3.20.0.md) · [Bedienung 3.19](docs/archiv/43_AENDERUNGSVERLAUF_3.19.0.md) · [Bedienung 3.18](docs/archiv/42_CSV_IMPORT_3.18.0.md) · [Bedienung 3.17](docs/archiv/41_DRUCK_UND_PDF_3.17.0.md) · [QA](docs/07_QA_BERICHT.md) · [Daten und Backups](docs/06_DATA_BACKUP_MIGRATION.md) · [Dokumentationsindex](docs/00_INDEX.md).
