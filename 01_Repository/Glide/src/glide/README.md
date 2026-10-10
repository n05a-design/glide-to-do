# Anwendungskern

Stand 10.10.2026 · Glide 3.36.0 · Aufgabenformat 23 · Einstellungen 2 · Vorlagen 2

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
| `save_comparison.py` | Gemeinsamer Vergleich für Verlauf, Listenänderung und Aktivität (Tk-frei, P08a) |
| `view_metrics.py` | Datumslesen, Fälligkeitsstatus, Fortschritt und Kennzahlen sowie Zeilenhöhenformel (Tk-frei, P09b) |
| `action_catalog.py` | Stabile Aktionskennungen, Gruppen und virtuelle Editorbefehle (Tk-frei) |
| `ui_design.py` | Gemeinsame Abstände, Radien, Schriftgrößen und Zeilenhöhen; Titel-/Herkunftsbreiten (Tk-frei, OB01/U10/U19) |
| `planning.py` | Bearbeitungstagsziele, Wochentagskapazität, Bilanz und Vorschau (Tk-frei, KO01/AU02) |
| `day_proposal.py` | Erklärbare Tagesauswahl, Budget und Prüfung veralteter Vorschläge (Tk-frei, AU01) |
| `focus_timer.py` | Pausierbarer Fokus und genau einmal gebuchte Zeit (Tk-frei, G05/AU05) |
| `task_references.py` | Heimat und Textverweise, Quellenindex, Zielzustand, ID-Neuvergabe und bearbeitete Zeilentitel ohne Tk |
| `interaction_policy.py` | Palettensuche, gemerkte Hinweise und getrennte Datumsanzeige (Tk-frei) |
| `object_references.py` | Typisierte lokale Verweise, abgeleitete Rückverweise und Import-/Kopierregeln (Tk-frei) |
| `week_planning.py` | Gemeinsame Wochenbilanz und Zeitfenster aus vorhandenen Glide-Blöcken (Tk-frei) |
| `page_features.py` | Live-Listen, Titelbilder und gefüllte Vorlagenvorschau (Tk-frei) |
| `repeat_rules.py` | Wiederholungsregeln, Termin überspringen, verpasste Termine überspringen (Tk-frei, KO02) |
| `routines.py` | Routinen in „Heute“: Auswahl, Fortschritt, heute erledigt (Tk-frei, AU06) |
| `runtime_check.py` | Mindestversion Python/Tk vor dem Start, in einfacher Syntax (AB08) |
| `release_notes.py` | Katalog und Regeln der Karte „Neu in …“ (Tk-frei, N07) |
| `appearance.py` | Designpaar und Erkennung des Systemmodus für „Automatisch hell/dunkel“ (Tk-frei, N01) |
| `preview_tools.py` | Systemwerkzeuge für Bildvorschauen unter Linux, JPEG-Größe (Tk-frei, N08) |
| `filter_explain.py` | Bedingungen gespeicherter Filter prüfen und erklären (Tk-frei, D-03) |
| `exchange_patch.py` | KI-Austausch Stufe 2: Kontextpaket, Änderungsvorschlag prüfen, Konflikte (Tk-frei, G24) |
| `backup_diff.py` | Zwei Datenstände vergleichen, nur lesend (Tk-frei, F-03) |
| `render_retention.py` | Inhaltsabgleich und Lebensdauer wiederverwendbarer Ansichtsbausteine (Tk-frei) |

Die Tk-freien Fachmodule entstehen nach D17 und haben Unit-Tests unter `tests/unit`. `drawing_prototype.pyw` ist die isolierte Bedienprobe der Zeichenfläche und gehört nicht zur App.

- **Ressourcen:** `resources/fonts` (DejaVu Sans, Pixelify Sans unter SIL OFL 1.1, Lizenztexte, `provenance.json`; prozesslokal registriert), `resources/templates` (Vorlagenkatalog), `resources/logo` (unveränderte Kopien aus `20_Grafik_Master`).
- **`vendor/tkinterdnd2`:** optional für das Ziehen aus Finder und Explorer, MIT, Herkunft in `vendor/provenance.json` ([Entscheidung](../../docs/decisions/ABHAENGIGKEIT_TKDND.md)). Fehlt der Ordner, startet Glide ohne diese Funktion.
- **Laufzeit:** Python 3.14 mit Tk 9 und Standardbibliothek; Tk 8.6 bleibt lauffähig. Beim Start setzt `app.pyw` den Bytecode-Cache auf den Cacheordner des Systems; neben den Modulen entsteht kein `__pycache__`.
- **Tests** importieren die App erst nach gesetztem isoliertem `GLIDE_DATA_DIR`.
- **Lieferung:** `scripts/pflege/abgleich_07.py` spielt diesen Stand nach `07_Python-Versionen` (SHA-256), `packaging/macos/baue_app.py` baut daraus das Entwicklungsbundle. Änderungen hier nur im Rahmen einer Produktionsrunde.

Aufbau und Datenwege: [Architektur](../../docs/02_ARCHITECTURE.md). Verhalten: [Funktionen](../../docs/20_FUNKTIONEN.md). Datenformat: [Daten und Migration](../../docs/06_DATA_BACKUP_MIGRATION.md).
