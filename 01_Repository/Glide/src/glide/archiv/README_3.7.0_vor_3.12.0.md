# Anwendungskern Glide 3.7.0

`app.pyw` ist die kanonische Anwendung. Python/Tk und die Standardbibliothek
bilden die Laufzeit. `resources/fonts` enthält vier DejaVu-Sans-TTF-Dateien,
Lizenz und Herkunftsnachweis. Ressourcen beim Kopieren oder Paketieren mitführen.

Datenformat 12, Einstellungen 2, Vorlagen 2. Datenpfad und weitere Details:
[Architektur](../../docs/02_ARCHITECTURE.md),
[Backups](../../docs/06_DATA_BACKUP_MIGRATION.md).
Tests dürfen die App erst nach gesetztem isolierten `GLIDE_DATA_DIR` importieren.

## Nachbesserung vom 11.09.2026

Mac-Trackpad unter Tk 9, vollständige isolierte Vorlagenbearbeitung, 16 Praxisvorlagen,
relative Termine mit Vorlagenformat 2 und verbesserte Aufgaben-Vorschauen.
Der aktuelle [Nachtrag mit Migration, Bedienung und Prüfgrenzen](../../docs/26_MAC_VORLAGEN_UND_ABLAGE_3.7.0.md)
hat für diese Punkte Vorrang vor dem Prüfstand vom 07.09.2026.
