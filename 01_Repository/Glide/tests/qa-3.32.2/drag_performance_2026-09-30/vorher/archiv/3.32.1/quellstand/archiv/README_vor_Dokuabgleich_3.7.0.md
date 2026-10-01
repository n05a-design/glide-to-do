# Anwendungskern Glide 3.6.0

`app.pyw` ist die kanonische Anwendung. Python/Tk und die Standardbibliothek
bilden die Laufzeit. `resources/fonts` enthält vier DejaVu-Sans-TTF-Dateien,
Lizenz und Herkunftsnachweis. Ressourcen beim Kopieren oder Paketieren mitführen.

Datenformat 11, Einstellungen 2, Vorlagen 1. Datenpfad und weitere Details:
[Architektur](../../docs/02_ARCHITECTURE.md),
[Backups](../../docs/06_DATA_BACKUP_MIGRATION.md).
Tests dürfen die App erst nach gesetztem isolierten `GLIDE_DATA_DIR` importieren.
