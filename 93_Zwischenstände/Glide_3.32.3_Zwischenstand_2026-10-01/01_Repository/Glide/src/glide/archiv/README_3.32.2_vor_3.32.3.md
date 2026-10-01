# Anwendungskern

Stand 30.09.2026 · Glide 3.32.2 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

`app.pyw` ist die kanonische Anwendung. Seit 3.29.0 gehören `drawing.py`
(UI-unabhängiger Zellvertrag, JSON und Glide-SVG) und `drawing_image.py`
(Tk-Bildfunktionen für PNG-Referenz und Nachzeichnung) als Module daneben;
sie werden beim Start aus demselben Ordner geladen.

Seit 3.30.0 enthalten die Module außerdem:

- `drawing.py`: Aktionspuffer, Flächengrößen 16–128, Formen, Symmetrie,
  Muster, Bereiche, PNG-Kodierung und Paletten (`.gpl`/`.hex`, Glide 32);
- `drawing_image.py`: Miniaturen für Galerie, Startseite und Pinnwand.

Weitere Module neben `app.pyw` (alle beim Kopieren mitnehmen):

- `backdrop.py`: Hintergrundverläufe (26.09.2026);
- `page_markdown.py`: Markdown ↔ Seitendokument (26.09.2026), seit dem
  27.09.2026 mit Bildzeilen;
- `image_preview.py`: Bildvorschauen mit den Mitteln von Tk 9 (27.09.2026);
- `logo.py`: Logo und App-Symbol aus den SVG-Mastern unter
  `resources/logo`, eingefärbt in der Akzentfarbe (29.09.2026);
- `glide_start.py`: Schnellstart mit Bytecode-Cache (in `07_Python-Versionen`
  als `Schnellstart.pyw`).

`vendor/tkinterdnd2` (seit 27.09.2026) bringt tkDnD für das Ziehen aus Finder
und Explorer mit – optional, MIT-Lizenz, Herkunft in `vendor/provenance.json`,
[Entscheidung](../../docs/decisions/ABHAENGIGKEIT_TKDND.md). Fehlt der Ordner,
startet Glide ohne diese Funktion.

`resources/logo` (seit 29.09.2026) enthält unveränderte Kopien der Master aus
`20_Grafik_Master`: das Logo und das App-Symbol je als SVG und PNG. Beim
Start setzt `app.pyw` den Bytecode-Cache auf den Cacheordner des Systems
(`bytecode_cache_dir`); neben den Modulen entsteht kein `__pycache__`.

Die Archivkopien des Stands vor 3.30 liegen in `archiv/`. `drawing_prototype.pyw`
bleibt die isolierte Bedienprobe. Python 3.14 mit Tk 9 und die
Standardbibliothek bilden die Laufzeit (Tk 8.6 bleibt lauffähig). `resources/fonts` enthält vier DejaVu-Sans-TTF-Dateien und
seit 3.30 Pixelify Sans (Regular, Bold; SIL OFL 1.1, nur Überschriften im
Design „Pixel“), jeweils mit Lizenztext; Herkunft und Prüfsummen stehen in
`provenance.json`. Ressourcen beim Kopieren oder Paketieren
mitführen. Die Schriften werden nur **prozesslokal** registriert – unter
Windows über `FR_PRIVATE`, unter macOS im Prozessumfang über CoreText, unter Linux
über Fontconfig (`FcConfigAppFontAddDir`); sie werden nicht im
System installiert und stehen anderen Programmen deshalb nicht zur Verfügung.

Der Funktionsbestand entspricht dem Repository-README: Designsystem mit
zehn Designs (einschließlich „Pixel“), fünf Anzeigemodi der Listenansicht,
Glide-Austauschformat, Pinnwand als Arbeitsfläche mit Spaltenboard, Bereichen
und Präsentation, Kalenderimport und Kalenderausgabe als ICS, Zeichnungsseiten
mit 16 bis 128 Zellen (Pixel-Werkstatt), dauerhafter Änderungsverlauf, CSV-Import mit
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
geprüften Quellstand synchronisiert und über SHA-256 abgeglichen. Ein
macOS-Entwicklungsbundle baut `packaging/macos/baue_app.py` aus diesem Ordner.

Seit dem 26.09.2026 gehört `backdrop.py` dazu: Es enthält die Hintergrundverläufe
(Entwürfe, Lesezone, PNG), nutzt nur die Standardbibliothek und muss wie die
übrigen Module neben `app.pyw` liegen.

`page_markdown.py` übersetzt Markdown in Seiten und zurück (Seitenart „Seite“,
Standardbibliothek) und muss neben `app.pyw` liegen.

Die Galerie (seit 27.09.2026, Klasse `GalleryView` in `app.pyw`) braucht kein
weiteres Modul: PNG und GIF liest Tk, andere Bildformate wandelt unter macOS
das Systemwerkzeug `sips` in Vorschauen im Cache.

`glide_start.py` ist der Schnellstart.

- Es lädt `app.pyw` als Modul und legt den übersetzten Stand im Cache des
  Systems ab (macOS `~/Library/Caches/Glide/bytecode`).
- Ab dem zweiten Start lädt Glide dadurch rund eine halbe Sekunde schneller.
- `python3 src/glide/glide_start.py` startet Glide wie `app.pyw`.
