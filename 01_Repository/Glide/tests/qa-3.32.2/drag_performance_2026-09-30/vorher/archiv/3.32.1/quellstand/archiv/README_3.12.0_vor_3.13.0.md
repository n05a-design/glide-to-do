# Anwendungskern Glide 3.12.0

`app.pyw` ist die kanonische Anwendung. Python/Tk und die Standardbibliothek
bilden die Laufzeit. `resources/fonts` enthält vier DejaVu-Sans-TTF-Dateien,
Lizenz und Herkunftsnachweis. Ressourcen beim Kopieren oder Paketieren mitführen.

Datenformat 13, Einstellungen 2, Vorlagen 2. „Mein Tag“ ergänzt eine bewusste Tagesauswahl über mehrere Listen; die Auswahl liegt als persönliche Einstellung vor. Datenpfad und weitere Details:
[Architektur](../../docs/02_ARCHITECTURE.md),
[Backups](../../docs/06_DATA_BACKUP_MIGRATION.md).
Tests dürfen die App erst nach gesetztem isolierten `GLIDE_DATA_DIR` importieren.

Die aktuelle Arbeitskopie enthält die 3.9-Oberflächenangleichung, Reiter und Pinnwände
für dieselben Aufgabenobjekte, Schnellerfassung und gespeicherte Filter sowie „Mein Tag“.
Die startbare Kopie im äußeren Ordner wird nach jedem geprüften Quellstand synchronisiert.
