# Glide – Aufgaben und Listen

Aktueller interner Entwicklungsstand: **3.12.0** · 13.09.2026

Lokale deutschsprachige Desktop-App mit Python/Tk. Ohne Konto oder neue Laufzeitabhängigkeiten. Nutzdaten liegen außerhalb des Programmordners.

Neu: „Mein Tag“ für eine bewusste Tagesauswahl aus mehreren Listen, Schnellerfassung mit deutscher Fristvorschau und gespeicherte Filter über Listen, Labels, Status, Wichtigkeit, Fälligkeit und Suchtext. Einzelne Aufgaben und Gruppen lassen sich als Reiter öffnen; vorhandene Punkte können auf Pinnwänden für Listen und Ordner angeheftet, gefiltert und angeordnet werden. Alle Ansichten bearbeiten dieselben Objekte.

Start: `python3 src/glide/app.pyw` mit Tk-fähigem Python. Eine laufende ältere Instanz vorher schließen. Die startbare Kopie liegt im äußeren Ordner `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.12.0.pyw`; der vollständige Nachbarordner `resources` gehört dazu.

Aufgabenformat 13, Einstellungen 2 und Vorlagen 2 bleiben erhalten. Reiter/Pinnwände liegen in Einstellungen und sind kein Bestandteil eines Aufgabenbackups. Benachrichtigungen werden bei laufender App verarbeitet.

Prüfung: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.12.0/abschluss`. Alle Tests verwenden isolierte Datenordner. Keine Veröffentlichung oder Signatur durch diesen Quellstand.

[Bedienung 3.12](docs/35_MEIN_TAG_3.12.0.md) · [Bedienung 3.11](docs/34_SCHNELLERFASSUNG_UND_FILTER_3.11.0.md) · [QA](docs/07_QA_BERICHT.md) · [Daten und Backups](docs/06_DATA_BACKUP_MIGRATION.md) · [Dokumentationsindex](docs/00_INDEX.md).
