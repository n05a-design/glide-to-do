# Glide – Aufgaben und Listen

Neu in 3.21: Kalenderimport aus ICS. Termine einer Kalenderdatei werden Aufgaben mit Fälligkeit – mit Dauer als Aufwand, Kategorien als Labels, abbildbaren Wiederholungen und Erinnerungen, mit Vorschau vor der Übernahme und einem Rückgängig-Schritt. [Bedienung und Datenregeln](docs/45_KALENDERIMPORT_3.21.0.md).

Aktueller interner Entwicklungsstand: **3.21.3** · 14.09.2026 · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2

Lokale deutschsprachige Desktop-App mit Python/Tk. Ohne Konto oder neue Laufzeitabhängigkeiten. Nutzdaten liegen außerhalb des Programmordners.

Funktionsbestand: Kalenderimport und Kalenderausgabe als ICS, dauerhafter Änderungsverlauf, CSV-Import mit Spaltenzuordnung, Druck- und PDF-Ausgabe, vollständiges App-Backup mit Inhaltsvorschau, Tagesplanung mit Tageskapazität, Bearbeitungstag und geschätzter Aufwand, Tabellenansicht mit listenspezifischen Spalten, „Mein Tag“, Schnellerfassung mit deutscher Fristvorschau, gespeicherte Filter, Reiter und Pinnwände. Alle Ansichten bearbeiten dieselben Objekte.

Durchgehende Grundlage, unabhängig von der jeweils neuesten Funktion: verschachtelte Listen und Ordner, Aufgaben, Long-Tasks, Gruppen, Überschriften und Unterpunkte, Notizen, Fälligkeit mit Uhrzeit, Wichtigkeit, sechs Wiederholungsarten, Erinnerungen innerhalb der laufenden App, Labels, Farben, Beschreibungen und lokale Anhänge an Punkten, Listen und Ordnern, Kalenderansicht, Suche und Offen-Filter, Mehrfachauswahl, Ziehen, Rückgängig und Papierkorb, 16 Praxisvorlagen mit eigenem Katalog zum Bearbeiten, Importieren und Exportieren, TXT-, CSV- und Markdown-Austausch, portable Aufgabenbackups sowie Hell- und Dunkelmodus mit Akzentfarbe und drei Schriftgrößen.

Start: `python3 src/glide/app.pyw` mit Tk-fähigem Python. Eine laufende ältere Instanz vorher schließen. Die startbare Kopie liegt im äußeren Ordner `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.21.3.pyw`; der vollständige Nachbarordner `resources` gehört dazu.

Aufgabenformat 15 (seit 3.19, vorher 14 seit 3.14), Einstellungen 2 und Vorlagen 2 bleiben erhalten. Reiter/Pinnwände liegen in Einstellungen und sind kein Bestandteil eines Aufgabenbackups. Benachrichtigungen werden bei laufender App verarbeitet.

Prüfung: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.21.3/abschluss` – 25 Suiten, drei Analysen, Beispiel- und Releaseabgleich. Alle Tests verwenden isolierte Datenordner. Keine Veröffentlichung oder Signatur durch diesen Quellstand.

[Bedienung 3.21](docs/45_KALENDERIMPORT_3.21.0.md) · [Bedienung 3.20](docs/44_KALENDERAUSGABE_3.20.0.md) · [Bedienung 3.19](docs/43_AENDERUNGSVERLAUF_3.19.0.md) · [Bedienung 3.18](docs/42_CSV_IMPORT_3.18.0.md) · [Bedienung 3.17](docs/41_DRUCK_UND_PDF_3.17.0.md) · [QA](docs/07_QA_BERICHT.md) · [Daten und Backups](docs/06_DATA_BACKUP_MIGRATION.md) · [Dokumentationsindex](docs/00_INDEX.md).
