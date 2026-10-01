# Glide – Aufgaben und Listen

Aktueller interner Entwicklungsstand: **3.9.0** · 12.09.2026

Lokale deutschsprachige Desktop-App mit Python/Tk. Ohne Konto, Internet oder neue Laufzeitabhängigkeiten. Nutzdaten liegen außerhalb des Programmordners.

Neu: einheitliche Benachrichtigungsoberfläche, kompakte Kopfzeile mit Einstellungszahnrad, Light/Dark Mode in Einstellungen, durchsuchbare App-Aktionen, ausblendbare Seitenleiste und grafische Dropdowns ohne separate Popup-Fenster. Neue Listen nutzen die verfügbare Höhe oder zwei Spalten.

Start: `python3 src/glide/app.pyw` mit einer Tk-fähigen Python-Installation. Eine laufende ältere Instanz vorher schließen. Die startbare Arbeitskopie liegt im äußeren Ordner `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.9.0.pyw`; ihr `resources`-Ordner gehört dazu.

Aufgabenformat 13, Einstellungen 2 und Vorlagen 2 bleiben erhalten. Vor der ersten Format-13-Speicherung älterer Daten wird eine unveränderte Originalkopie angelegt. Benachrichtigungen werden bei laufender App verarbeitet; keine Systemzustellung bei beendetem Programm.

Prüfung: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.9.0/oberflaeche/abschluss`. Alle Tests verwenden isolierte Datenordner. Keine Veröffentlichung oder Signatur durch diesen Quellstand.

[Änderungen 3.9](docs/32_UI_UND_BEDIENUNG_3.9.0.md) · [QA](docs/07_QA_BERICHT.md) · [Daten und Backups](docs/06_DATA_BACKUP_MIGRATION.md) · [Dokumentationsindex](docs/00_INDEX.md).
