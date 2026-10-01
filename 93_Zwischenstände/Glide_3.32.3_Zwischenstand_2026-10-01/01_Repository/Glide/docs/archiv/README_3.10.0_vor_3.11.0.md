# Glide – Aufgaben und Listen

Aktueller interner Entwicklungsstand: **3.10.0** · 13.09.2026

Lokale deutschsprachige Desktop-App mit Python/Tk. Ohne Konto oder neue Laufzeitabhängigkeiten. Nutzdaten liegen außerhalb des Programmordners.

Neu: einzelne Aufgaben und Gruppen als Reiter öffnen; vorhandene Punkte auf Pinnwänden für Listen und Ordner anheften, filtern und anordnen. Beide Ansichten bearbeiten dieselben Objekte. Reiter schließen und Karten abheften löschen keine Aufgaben. Die 3.9-Oberfläche bleibt erhalten.

Start: `python3 src/glide/app.pyw` mit Tk-fähigem Python. Eine laufende ältere Instanz vorher schließen. Die startbare Kopie liegt im äußeren Ordner `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.10.0.pyw`; der vollständige Nachbarordner `resources` gehört dazu.

Aufgabenformat 13, Einstellungen 2 und Vorlagen 2 bleiben erhalten. Reiter/Pinnwände liegen in Einstellungen und sind kein Bestandteil eines Aufgabenbackups. Benachrichtigungen werden bei laufender App verarbeitet.

Prüfung: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.10.0/abschluss`. Alle Tests verwenden isolierte Datenordner. Keine Veröffentlichung oder Signatur durch diesen Quellstand.

[Bedienung 3.10](docs/33_REITER_UND_PINNWAND_3.10.0.md) · [QA](docs/07_QA_BERICHT.md) · [Daten und Backups](docs/06_DATA_BACKUP_MIGRATION.md) · [Dokumentationsindex](docs/00_INDEX.md).
