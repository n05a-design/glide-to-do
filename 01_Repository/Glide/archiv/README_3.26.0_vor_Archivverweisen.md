# Glide – Aufgaben und Listen

Neu im aktuellen Stand 3.26: Die App und die Dokumentationsfassung wurden auf den konsolidierten 3.26.0-Stand gebracht. Die aktuellen Abgleichungen betreffen vor allem die Menü-/Produktbezeichnungen, den Release-Status und die Beschreibung des aktuellen Arbeitsstands. Die Detaildokumentation der 3.25-Serie bleibt als fachlicher Nachweis erhalten. [Übersichtlichkeit und Hierarchie](docs/57_UEBERSICHT_UND_HIERARCHIE_3.25.0.md) · [Startseite und Begleiter](docs/58_STARTSEITE_UND_BEGLEITER_3.25.0.md) · [Navigation und Pinnwand](docs/55_NAVIGATION_UND_PINNWAND_3.24.0.md) · [Designsystem](docs/50_DESIGNSYSTEM_3.23.0.md) · [Austauschformat](docs/52_AUSTAUSCHFORMAT_3.23.0.md) · [Anzeigemodi](docs/54_ANZEIGEMODI_3.23.0.md).

Aktueller interner Entwicklungsstand: **3.26.0** · 20.09.2026 · Aufgabenformat 17 · Einstellungen 2 · Vorlagen 2

Lokale deutschsprachige Desktop-App mit Python/Tk. Ohne Konto oder neue Laufzeitabhängigkeiten. Nutzdaten liegen außerhalb des Programmordners.

Funktionsbestand: Designsystem mit neun Designs, Anzeigemodi der Listenansicht, Glide-Austauschformat, Pinnwand als Arbeitsfläche, Kalenderimport und Kalenderausgabe als ICS, dauerhafter Änderungsverlauf, CSV-Import mit Spaltenzuordnung, Druck- und PDF-Ausgabe, vollständiges App-Backup mit Inhaltsvorschau, Tagesplanung mit Tageskapazität, Bearbeitungstag und geschätzter Aufwand, Tabellenansicht mit listenspezifischen Spalten, „Mein Tag“, Schnellerfassung mit deutscher Fristvorschau, gespeicherte Filter, Reiter und Pinnwände. Alle Ansichten bearbeiten dieselben Objekte.

Durchgehende Grundlage, unabhängig von der jeweils neuesten Funktion: verschachtelte Listen und Ordner, Aufgaben, Long-Tasks, Gruppen, Überschriften und Unterpunkte, Notizen, Fälligkeit mit Uhrzeit, Wichtigkeit, sechs Wiederholungsarten, Erinnerungen innerhalb der laufenden App, Labels, Farben, Beschreibungen und lokale Anhänge an Punkten, Listen und Ordnern, Kalenderansicht, Suche und Offen-Filter, Mehrfachauswahl, Ziehen, Rückgängig und Papierkorb, 16 Praxisvorlagen mit eigenem Katalog zum Bearbeiten, Importieren und Exportieren, TXT-, CSV- und Markdown-Austausch, portable Aufgabenbackups sowie Hell- und Dunkelmodus mit Akzentfarbe und drei Schriftgrößen.

Start: `python3 src/glide/app.pyw` mit Tk-fähigem Python. Eine laufende ältere Instanz vorher schließen. Die startbare Kopie liegt im äußeren Ordner `07_Python-Versionen` und trägt die Nummer aus `VERSION`; der vollständige Nachbarordner `resources` gehört dazu.

Aufgabenformat 16 (seit 3.22, davor 15 seit 3.19 und 14 seit 3.14), Einstellungen 2 und Vorlagen 2 bleiben erhalten. Reiter/Pinnwände liegen in Einstellungen und sind kein Bestandteil eines Aufgabenbackups. Benachrichtigungen werden bei laufender App verarbeitet.

Prüfung: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.23.0/abschluss` – alle Suiten und Analysen aus `tests/tools/pruefen.py`, Beispiel- und Releaseabgleich. Alle Tests verwenden isolierte Datenordner. Keine Veröffentlichung oder Signatur durch diesen Quellstand.

[Bedienung 3.21](docs/45_KALENDERIMPORT_3.21.0.md) · [Bedienung 3.20](docs/44_KALENDERAUSGABE_3.20.0.md) · [Bedienung 3.19](docs/43_AENDERUNGSVERLAUF_3.19.0.md) · [Bedienung 3.18](docs/42_CSV_IMPORT_3.18.0.md) · [Bedienung 3.17](docs/41_DRUCK_UND_PDF_3.17.0.md) · [QA](docs/07_QA_BERICHT.md) · [Daten und Backups](docs/06_DATA_BACKUP_MIGRATION.md) · [Dokumentationsindex](docs/00_INDEX.md).
