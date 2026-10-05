# Anwendungskern

Stand 05.10.2026 · Glide 3.33.8 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

`app.pyw` ist die kanonische Anwendung (Klasse `ListApp`). Daneben liegen Module, die beim Start aus demselben Ordner geladen werden und beim Kopieren oder Paketieren immer mitgehen:

| Modul | Aufgabe |
|---|---|
| `glide_start.py` | Schnellstart mit Bytecode-Cache im Systemcache (in `07_Python-Versionen` als `Schnellstart.pyw`) |
| `drawing.py` | Zellmodell der Pixel-Werkstatt, JSON, Glide-SVG, PNG/ICO, Paletten |
| `drawing_image.py` | Tk-Bildfunktionen und Miniaturen der Zeichnung |
| `backdrop.py` | Hintergrundverläufe |
| `page_markdown.py` | Markdown ↔ Seitendokument |
| `image_preview.py` | Bildvorschauen mit den Mitteln von Tk 9 |
| `logo.py` | Logo und App-Symbol aus den SVG-Mastern in der Akzentfarbe |
| `schema_backups.py` | Formatsicherung vor Migrationen (Tk-frei) |
| `sidebar_policy.py` | Regeln der vier Seitenleistenbereiche (Tk-frei) |
| `svg_geometry.py` | SVG-Pfade und Farben für den Logo-Rückfall (Tk-frei) |
| `home_tiles.py` | Startseitenkacheln und Standard D12 (Tk-frei) |
| `capture_parser.py` | Deutsche Schnelleingabe mit Feldchips (Tk-frei) |
| `eisenhower.py` | Quadranten „Dringlichkeit × Wichtigkeit“ (Tk-frei) |
| `today_view.py` | Aufteilung der Ansicht „Heute“ (Tk-frei) |
| `content_search.py` | Inhaltssuche und Trefferausschnitte (Tk-frei) |

Die Tk-freien Fachmodule entstehen nach D17 und haben Unit-Tests unter `tests/unit`. `drawing_prototype.pyw` ist die isolierte Bedienprobe der Zeichenfläche und gehört nicht zur App.

- **Ressourcen:** `resources/fonts` (DejaVu Sans, Pixelify Sans unter SIL OFL 1.1, Lizenztexte, `provenance.json`; prozesslokal registriert), `resources/templates` (Vorlagenkatalog), `resources/logo` (unveränderte Kopien aus `20_Grafik_Master`).
- **`vendor/tkinterdnd2`:** optional für das Ziehen aus Finder und Explorer, MIT, Herkunft in `vendor/provenance.json` ([Entscheidung](../../docs/decisions/ABHAENGIGKEIT_TKDND.md)). Fehlt der Ordner, startet Glide ohne diese Funktion.
- **Laufzeit:** Python 3.14 mit Tk 9 und Standardbibliothek; Tk 8.6 bleibt lauffähig. Beim Start setzt `app.pyw` den Bytecode-Cache auf den Cacheordner des Systems; neben den Modulen entsteht kein `__pycache__`.
- **Tests** importieren die App erst nach gesetztem isoliertem `GLIDE_DATA_DIR`.
- **Lieferung:** `scripts/pflege/abgleich_07.py` spielt diesen Stand nach `07_Python-Versionen` (SHA-256), `packaging/macos/baue_app.py` baut daraus das Entwicklungsbundle. Änderungen hier nur im Rahmen einer Produktionsrunde.

Aufbau und Datenwege: [Architektur](../../docs/02_ARCHITECTURE.md). Verhalten: [Funktionen](../../docs/20_FUNKTIONEN.md). Datenformat: [Daten und Migration](../../docs/06_DATA_BACKUP_MIGRATION.md).
