# Glide – Aufgaben und Listen

Aktueller interner Entwicklungsstand: **3.13.0** · 13.09.2026

Lokale deutschsprachige Desktop-App mit Python/Tk. Ohne Konto oder neue Laufzeitabhängigkeiten. Nutzdaten liegen außerhalb des Programmordners.

Neu: Die Tabellenansicht zeigt Aufgaben einer Liste kompakt in wählbaren Spalten; Such-, Offen- und Bearbeitungsaktionen bleiben mit der Listenansicht verbunden. Dazu kommen „Mein Tag“, Schnellerfassung mit deutscher Fristvorschau und gespeicherte Filter. Alle Ansichten bearbeiten dieselben Objekte.

Start: `python3 src/glide/app.pyw` mit Tk-fähigem Python. Eine laufende ältere Instanz vorher schließen. Die startbare Kopie liegt im äußeren Ordner `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.13.0.pyw`; der vollständige Nachbarordner `resources` gehört dazu.

Aufgabenformat 13, Einstellungen 2 und Vorlagen 2 bleiben erhalten. Reiter/Pinnwände liegen in Einstellungen und sind kein Bestandteil eines Aufgabenbackups. Benachrichtigungen werden bei laufender App verarbeitet.

Prüfung: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.13.0/abschluss`. Alle Tests verwenden isolierte Datenordner. Keine Veröffentlichung oder Signatur durch diesen Quellstand.

[Bedienung 3.13](docs/36_TABELLENANSICHT_3.13.0.md) · [Bedienung 3.12](docs/35_MEIN_TAG_3.12.0.md) · [QA](docs/07_QA_BERICHT.md) · [Daten und Backups](docs/06_DATA_BACKUP_MIGRATION.md) · [Dokumentationsindex](docs/00_INDEX.md).
