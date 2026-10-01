# Anwendungskern

Stand 23.09.2026 · Glide 3.28.0 · Aufgabenformat 18 · Einstellungen 2 · Vorlagen 2

`app.pyw` ist die kanonische Anwendung. Python/Tk und die Standardbibliothek
bilden die Laufzeit. `resources/fonts` enthält vier DejaVu-Sans-TTF-Dateien,
Lizenz und Herkunftsnachweis. Ressourcen beim Kopieren oder Paketieren
mitführen. Die Schriften werden nur **prozesslokal** registriert – unter
Windows über `FR_PRIVATE`, unter macOS im Prozessumfang; sie werden nicht im
System installiert und stehen anderen Programmen deshalb nicht zur Verfügung.

Der Funktionsbestand entspricht dem Repository-README: Designsystem mit
sieben Designs, fünf Anzeigemodi der Listenansicht, Glide-Austauschformat,
Pinnwand als Arbeitsfläche, Kalenderimport und
Kalenderausgabe als ICS, dauerhafter Änderungsverlauf, CSV-Import mit
Spaltenzuordnung, Druck- und PDF-Ausgabe, vollständiges App-Backup mit
Inhaltsvorschau, Tagesplanung mit Tageskapazität, Bearbeitungstag und
geschätzter Aufwand, Tabellenansicht mit listenspezifischen Spalten, „Mein
Tag“, Schnellerfassung, gespeicherte Filter, Reiter und Pinnwände. Alle
Ansichten bearbeiten dieselben Objekte; Spaltenauswahl und Tagesauswahl liegen
als persönliche Einstellungen vor.

Datenpfad und weitere Details: [Architektur](../../docs/02_ARCHITECTURE.md),
[Backups](../../docs/06_DATA_BACKUP_MIGRATION.md).
Tests dürfen die App erst nach gesetztem isolierten `GLIDE_DATA_DIR`
importieren.

Die startbare Kopie im äußeren Ordner `07_Python-Versionen` wird nach jedem
geprüften Quellstand synchronisiert und über SHA-256 abgeglichen.
