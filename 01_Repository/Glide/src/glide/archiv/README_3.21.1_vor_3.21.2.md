# Anwendungskern Glide 3.14.0

`app.pyw` ist die kanonische Anwendung. Python/Tk und die Standardbibliothek
bilden die Laufzeit. `resources/fonts` enthält vier DejaVu-Sans-TTF-Dateien,
Lizenz und Herkunftsnachweis. Ressourcen beim Kopieren oder Paketieren mitführen.

Datenformat 13, Einstellungen 2, Vorlagen 2. Die Tabellenansicht ergänzt eine flache Darstellung mit listenspezifisch wählbaren Spalten; die Auswahl liegt als persönliche Einstellung vor. „Mein Tag“ bleibt als bewusste Tagesauswahl über mehrere Listen erhalten. Datenpfad und weitere Details:
[Architektur](../../docs/02_ARCHITECTURE.md),
[Backups](../../docs/06_DATA_BACKUP_MIGRATION.md).
Tests dürfen die App erst nach gesetztem isolierten `GLIDE_DATA_DIR` importieren.

Die aktuelle Arbeitskopie enthält die 3.9-Oberflächenangleichung, Reiter und Pinnwände
für dieselben Aufgabenobjekte, Schnellerfassung, gespeicherte Filter, „Mein Tag“ und die Tabellenansicht.
Die startbare Kopie im äußeren Ordner wird nach jedem geprüften Quellstand synchronisiert.
