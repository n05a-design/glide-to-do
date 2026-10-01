# Anwendungskern

Stand 25.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

`app.pyw` ist die kanonische Anwendung. Seit 3.29.0 gehören `drawing.py`
(UI-unabhängiger Zellvertrag, JSON und Glide-SVG) und `drawing_image.py`
(Tk-Bildfunktionen für PNG-Referenz und Nachzeichnung) als Module daneben;
sie werden beim Start aus demselben Ordner geladen.

Seit 3.30.0 enthalten die Module außerdem:

- `drawing.py`: Aktionspuffer, Flächengrößen 16–128, Formen, Symmetrie,
  Muster, Bereiche, PNG-Kodierung und Paletten (`.gpl`/`.hex`, Glide 32);
- `drawing_image.py`: Miniaturen für Galerie, Startseite und Pinnwand.

Die Archivkopien des Stands vor 3.30 liegen in `archiv/`. `drawing_prototype.pyw`
bleibt die isolierte Bedienprobe. Python/Tk und die Standardbibliothek
bilden die Laufzeit. `resources/fonts` enthält vier DejaVu-Sans-TTF-Dateien,
Lizenz und Herkunftsnachweis. Ressourcen beim Kopieren oder Paketieren
mitführen. Die Schriften werden nur **prozesslokal** registriert – unter
Windows über `FR_PRIVATE`, unter macOS im Prozessumfang; sie werden nicht im
System installiert und stehen anderen Programmen deshalb nicht zur Verfügung.

Der Funktionsbestand entspricht dem Repository-README: Designsystem mit
sieben Designs, fünf Anzeigemodi der Listenansicht, Glide-Austauschformat,
Pinnwand als Arbeitsfläche, Kalenderimport und
Kalenderausgabe als ICS, Zeichnungsseiten mit 128 × 128 Zellen, dauerhafter Änderungsverlauf, CSV-Import mit
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
