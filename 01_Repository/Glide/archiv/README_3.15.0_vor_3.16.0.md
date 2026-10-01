# Glide – Aufgaben und Listen

Neu in 3.15: Die Ansicht „Tagesplanung“ zeigt alle Aufgaben mit Bearbeitungstag an einem wählbaren Tag und stellt ihren geschätzten Aufwand einer selbst gesetzten Tageskapazität gegenüber. Summen erscheinen auch in „Mein Tag“, in der Tabelle und auf der Startseite. Keine Zeiterfassung und keine automatische Terminverteilung. [Bedienung und Datenregeln](docs/39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md).

Aktueller interner Entwicklungsstand: **3.15.0** · 13.09.2026

Lokale deutschsprachige Desktop-App mit Python/Tk. Ohne Konto oder neue Laufzeitabhängigkeiten. Nutzdaten liegen außerhalb des Programmordners.

Neu: Die Tabellenansicht zeigt Aufgaben einer Liste kompakt in wählbaren Spalten; Such-, Offen- und Bearbeitungsaktionen bleiben mit der Listenansicht verbunden. Dazu kommen „Mein Tag“, Schnellerfassung mit deutscher Fristvorschau und gespeicherte Filter. Alle Ansichten bearbeiten dieselben Objekte.

Start: `python3 src/glide/app.pyw` mit Tk-fähigem Python. Eine laufende ältere Instanz vorher schließen. Die startbare Kopie liegt im äußeren Ordner `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.15.0.pyw`; der vollständige Nachbarordner `resources` gehört dazu.

Aufgabenformat 14, Einstellungen 2 und Vorlagen 2 bleiben erhalten. Reiter/Pinnwände liegen in Einstellungen und sind kein Bestandteil eines Aufgabenbackups. Benachrichtigungen werden bei laufender App verarbeitet.

Prüfung: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.15.0/abschluss`. Alle Tests verwenden isolierte Datenordner. Keine Veröffentlichung oder Signatur durch diesen Quellstand.

[Bedienung 3.15](docs/39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md) · [Bedienung 3.14](docs/37_PLANUNG_UND_AUFWAND_3.14.0.md) · [Bedienung 3.13](docs/36_TABELLENANSICHT_3.13.0.md) · [QA](docs/07_QA_BERICHT.md) · [Daten und Backups](docs/06_DATA_BACKUP_MIGRATION.md) · [Dokumentationsindex](docs/00_INDEX.md).
