# Vollständige Projektbestandsaufnahme & Technisches Audit – Glide (`glide-to-do`)

Stand: 10.11.2026 · Glide 3.53.0 · Aufgabenformat 26 · Glide-System V1.15 · Git-Referenz `main` (`9e767bea`)

> **Zweck dieses Dokuments:** Eigenständige, verifizierbare Projektbestandsaufnahme und technische/dokumentarische Analyse des Glide-Repositories als Referenz für zukünftige Chats, Entwicklerinnen/Entwickler und KI-Agenten. Kanonische Aufgabenquelle bleibt [`Glide_Entwicklungsplan.md`](Glide_Entwicklungsplan.md); kanonische Fachanalyse bleibt [`Glide_Analyse.md`](Glide_Analyse.md).

---

## 1. Projektziel und aktueller Entwicklungsstand

### 1.1 Projektidentität & Produktziel
**Glide – Aufgaben und Listen** (`APP_BUNDLE_ID = "de.shaye.glide"`, `APP_USER_MODEL_ID = "Shaye.Glide"`) ist eine deutschsprachige, rein lokale („Local-First“) Desktop-Anwendung für persönliche Projekt-, Aufgaben-, Wissens- und Kreativorganisation ohne Kontozwang, Cloud-Sync, Teamfunktionen oder Netzwerk-Telemetrie ([`README.md`](../README.md), [`01_PRODUCT_CONSTRAINTS.md`](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md)).
- **Lizenz:** **MPL-2.0** (Mozilla Public License 2.0, entschieden in D72; [`LICENSE`](../LICENSE), [`01_Repository/Glide/LICENSE.md`](../01_Repository/Glide/LICENSE.md)).
- **Versionsstand im Code:**
  - **Anwendungsversion:** `3.53.0` ([`VERSION`](../01_Repository/Glide/VERSION), `APP_VERSION` in [`app.pyw`](../01_Repository/Glide/src/glide/app.pyw)).
  - **Glide-System-Version (Wiederverwendungskatalog für Folgeprojekt „Steps“):** `1.15` ([`GLIDE_SYSTEM_VERSION`](../01_Repository/Glide/GLIDE_SYSTEM_VERSION), [`src/glide/README.md`](../01_Repository/Glide/src/glide/README.md)).
  - **Datenformat (`DATA_SCHEMA_VERSION`):** `26` (`liste_speicher.json`), Einstellungen Schema `2` (`settings.json`), Vorlagen Schema `2` (`vorlagen.json`), Austauschpaket Schema `2` (`.glideexchange`) ([`06_DATA_BACKUP_MIGRATION.md`](../01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md)).

### 1.2 Abgrenzung: Implementiert vs. Geplant vs. Verworfen

| Kategorie | Umfang & Beleg |
|---|---|
| **Implementierte Funktionen (Stand 3.53.0 / Format 26)** | **147 katalogisierte System-/Produktfeatures (F001–F147)** in [`src/glide/README.md`](../01_Repository/Glide/src/glide/README.md) und [`20_FUNKTIONEN.md`](../01_Repository/Glide/docs/20_FUNKTIONEN.md):<br>• **Aufgaben & Projekte:** Hierarchische Aufgaben/Unteraufgaben, Checklisten, Beziehungen (`blocks`/`relates`), reichere Wiederholungen (FP-02), gespeicherte Filteransichten (FP-03), einheitlicher Inspektor (D24), Inline-Felder (D25), 40-Zeichen-Titelgrenze mit Live-Zähler (D63/D67).<br>• **Tages- & Wochensteuerung:** `Heute`/`Demnächst`, Zeitraster (06:00–22:00), ICS-Belegzeiten (rein lesend, D30), Tagesvorschlag (`day_proposal.py`), Tag entlasten (`day_relief.py`, D38), Fokus-Timer (`focus_timer.py`), optionale Tageshinweise (D20), Wochenplanung/-rückblick (`week_planning.py`).<br>• **Seiten, Notizen & Pinnwände:** Rich-Text-Seiten (`page`) mit Blockgriffen, Live-Aufgabenlisten, Aufgabenverweisen und unverknüpften Titelerwähnungen (`task_references.py`, FP-05), lesende Nebenansicht im Inspektor (`side_view.py`, D55/D57), Notizbücher/Tagebuch (`note`/`journal`), Spalten- & freie Pinnwände (`ItemWorkspace`), Bildgalerien (`gallery`).<br>• **Pixel-Werkstatt:** 16×16 bis 128×128 Pixelzeichnungen (`drawing.py`), eigener Pixel-Editor, mehrstufige Frame-Animationen + PNG-Spritesheet/Einzelbildexport (`animation.py`, `animation_export.py`, D18), Referenzbild/Nachzeichnen (`drawing_image.py`), transparente Pixelgründe (D59), eigene 16×16-Pixelsymbole.<br>• **Austausch & Sicherung:** Kontrollierter lokaler KI-Dateiaustausch über `.glideexchange` / JSON-Patch mit Prüfsummen (`exchange_patch.py`, `exchange_recipes.py`, FP-06), Notion-ZIP-Import inkl. Reimport-Konfliktprüfung (`notion_import.py`, `notion_reimport.py`, D26/D39), vollständiger Markdown-Baum-Export (`markdown_tree.py`, FP-07 Stufe 1), Seiten-Einzelwiederherstellung aus Backups (`page_restore.py`, D37), atomare Speicherung + Backup-Katalog (`persistence.py`, `backup_catalog.py`).<br>• **Design & Typografie:** 4 Schriftstile nach D77 (`Rubik`, `DM Mono`, `DM Serif Display`, `Charis SIL` + `DejaVu Sans` als interner Symbolbegleiter; [`font_catalog.py`](../01_Repository/Glide/src/glide/font_catalog.py)), Themenfarbe für Ansichtstitel (`view_title`, D68), gezeichnete Scrollleisten (`ThemedAutoScrollbar`, D66), Kompaktmodus (`compact_mode.py`, D55), bis zu 12 Reiter. |
| **Implementiert, aber mit offenen Abnahme-/Plattformtoren (`◐` / `▶`)** | • **Paket 8 / Barrierefreiheit (D36 / 4.0.0-Vorbereitung):** `core_accessibility.py` und gepatchte eigene Tk-9.1-Laufzeit sind im Code vorhanden; Screenreader-Gesamtabnahme nach **D58** bewusst bis Bedarf zurückgestellt.<br>• **SBOM / Lieferkette (WA-46):** CycloneDX-1.6-Generator in [`packaging/paket/sbom.py`](../01_Repository/Glide/packaging/paket/sbom.py) implementiert und schemageprüft, aber Status bewusst `pre-build`/`incomplete` bis zum Nachweis des vollständigen transitiven Abhängigkeitsgraphen am finalen nativen Paket ([`Glide_Entwicklungsplan.md`](Glide_Entwicklungsplan.md)).<br>• **Release-Entwurf-Workflow (D64):** [`.github/workflows/release.yml`](../.github/workflows/release.yml) ist implementiert, wurde aber noch nie über einen `v*`-Tag scharf ausgelöst. |
| **Geplante / offene Aufgaben (`○`, technische Restvorhaben)** | • **WA-21 (Paket A):** Vollständige Fundortübersicht („Wo wird dieses Element überall verwendet?“) mit Sprung/Rückkehr.<br>• **WA-32 / WA-39 / WA-49 / WA-50:** Schrittweise Entkopplung von `ListApp` (`_refresh_home`-Pilot), Initialisierung ohne Modulimport-Seiteneffekte (`RuntimePaths`/`RuntimeConfig`), Modulbudget.<br>• **WA-36 / WA-42:** Gezielte Performance-Optimierung (Speicher-/Refreshweg bei 1.000/10.000 Punkten, Untersuchung der Schwankungen in `test_tempo330` und `test_seitenkarten/druck_tempo`).<br>• **WA-41A / WA-41B:** Offene Ursachenanalyse historischer Intel-Mac-Crashes (`abort()` im Fontpanel / SIGILL in CoreGraphics) und einer leeren historischen Test-Sicherungsdatei. |
| **Ideen & unentschiedene Vorlagen (`◇`, ausdrücklich NICHT beauftragt)** | • **E-P1 bis E-P5:** Umfang und Reihenfolge späterer Ausbauphasen (u. a. WA-20 Wochenabsicht, WA-22 Arbeitskontext-Wiedereinstieg, WA-23/24 erweiterte Routinen, FP-07 Stufe 2 JSON Canvas / Reimport).<br>• **WA-52 bis WA-59:** Weitere Markt-/Mehrwertideen aus [`Glide_Markt_und_Vorbilder.md`](Glide_Markt_und_Vorbilder.md).<br>• Austausch des klassischen Tk-Restbestands (28 Kontrollkästchen, 2 Optionsknöpfe, 4 Listenfelder, 1 Regler) durch gezeichnete Widgets ([`Glide_Entwicklungsplan.md`](Glide_Entwicklungsplan.md)). |
| **Überholte / verworfene Konzepte (`✕`)** | • **Alte Schriftwahl D59/D60 (`Roboto Mono`, `Playfair Display`, `Fraunces`):** Durch **D77** (3.53.0) im gebündelten Ressourcenbestand abgelöst durch `DM Mono`, `DM Serif Display`, `Charis SIL` (alte Namen werden in [`font_catalog.py`](../01_Repository/Glide/src/glide/font_catalog.py) kompatibel auf die vier Stilklassen abgebildet).<br>• **Doppelter Seitentitel im Seiteninhalt (U18):** Durch **D71** abgeschafft (`PageEditor.TITLE_IN_CONTENT = False`).<br>• **Alte proprietäre Lizenzentwürfe:** Durch **D72 (MPL-2.0)** vollständig ersetzt.<br>• **Dauerhaft ausgeschlossen ([`01_PRODUCT_CONSTRAINTS.md`](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md)):** Cloud/Sync, Mehrbenutzer/Team/Kommentare, direkter KI-API-/Netzwerk-Client (Q3), systemweiter Global-Hotkey (G07), freie Datenbanktabellen à la Notion, Unterseiten-Hierarchien, SQLite als Primärspeicher (D16). |

---

## 2. Architektur und wesentliche Komponenten

### 2.1 Technologie-Stack & Laufzeitumgebung
- **Sprache & GUI:** **Python 3.14** + **Tcl/Tk 9.1** (regulärer Rückfall auf Tk 8.6 mit dokumentierten Einschränkungen bei SVG/Skalierung).
- **Laufzeit-Abhängigkeiten:** Ausschließlich Python-Standardbibliothek plus vendortes `tkinterdnd2` (MIT-Lizenz, unter [`src/glide/vendor/tkinterdnd2/`](../01_Repository/Glide/src/glide/vendor/tkinterdnd2)) für Datei-Drag-&-Drop aus Explorer/Finder. Keine externen Pip-Laufzeitpakete (kein Pillow, kein SQLite-ORM, kein HTTP-Framework).
- **Build & Packaging:** **PyInstaller 6.22.3** (fest gepinnt in [`requirements/build-windows.txt`](../01_Repository/Glide/requirements/build-windows.txt) und [`requirements/build-macos.txt`](../01_Repository/Glide/requirements/build-macos.txt)) + plattformspezifisch aus C-Quellen gebaute Tcl/Tk-9.1.0-Laufzeit inkl. Accessibility-Patches ([`packaging/runtime/`](../01_Repository/Glide/packaging/runtime)).

### 2.2 Modularchitektur (`01_Repository/Glide/src/glide/`)
Das Quellverzeichnis umfasst **94 Python-Dateien** (93 produktive Module + `drawing_prototype.pyw`):
1. **Zentraler Monolith / Orchestrator ([`app.pyw`](../01_Repository/Glide/src/glide/app.pyw)):**
   - **69.015 Zeilen Code**, zentrale Klasse `ListApp` mit **~1.863 direkten Methoden**.
   - Verantwortlich für Anwendungsstart, Tk-Root-Lebensdauer, Theme-Anwendung, sämtliche Hauptansichten (Startseite, Heute, Demnächst, Liste, Tabelle, Pinnwand, Kalender, Seiten, Notizen, Zeichnungen, Papierkorb, Einstellungen), modale Dialoge und Event-Routing.
   - Führt beim **Modulimport** bereits Seiteneffekte aus (WA-49): Pfadmanipulation (`sys.path`), Monkey-Patching von `tk.Menu.add_command`/`insert_command` via `defer_window_menu_commands()`, Setzen von `sys.pycache_prefix` (`bytecode_cache_dir()`), Stream-Ersatz unter `pythonw.exe` (`_ensure_streams()`) sowie Auflösung und Anlage von Datenverzeichnissen.
2. **Tk-freie Fach- und Regelmodule (88 von 94 Dateien ohne direkten `tkinter`-Import, gemäß D17):**
   - **Domäne & Planung:** `planning.py`, `day_proposal.py`, `day_relief.py`, `today_view.py`, `week_planning.py`, `week_review_data.py`, `eisenhower.py`, `focus_timer.py`, `routines.py`, `repeat_rules.py`, `repeat_ics.py`, `ics_busy.py`, `ics_recurrence.py`, `ics_timezone.py`, `occupied_time.py`, `busy_calendar.py`, `calendar_service.py`, `daily_hints.py`, `capture_parser.py`.
   - **Seiten, Verweise & Suche:** `page_features.py`, `page_markdown.py`, `page_restore.py`, `task_references.py`, `object_references.py`, `side_view.py`, `content_search.py`, `filter_explain.py`, `view_definition.py`, `item_index.py`, `relation_index.py`.
   - **Persistenz, Sicherheit & Sperren:** `persistence.py` (`PersistenceCoordinator`), `save_result.py`, `save_comparison.py`, `storage_health.py` (32-MiB-Grenze), `data_lock.py`, `session_guard.py`, `structural_guard.py`, `undo_history.py` (zlib-komprimierte JSON-Snapshots `PackedState`), `backup_catalog.py`, `backup_diff.py`, `backup_snapshot.py`, `schema_backups.py`, `restore_assets.py`, `attachment_policy.py`, `attachment_paths.py`.
   - **Import / Export / KI-Austausch:** `exchange_patch.py`, `exchange_recipes.py`, `markdown_tree.py`, `notion_archive.py`, `notion_import.py`, `notion_hierarchy.py`, `notion_reimport.py`, `source_metadata.py`.
   - **Design, Typografie & Grafik:** `ui_design.py`, `appearance.py`, `font_catalog.py`, `glyph_metrics.py`, `symbol_policy.py`, `brand.py`, `logo.py`, `logo_raster.py`, `drawing.py`, `animation.py`, `animation_export.py`, `sidebar_policy.py`, `compact_mode.py`, `view_metrics.py`, `home_dashboard.py`, `home_tiles.py`, `home_task_tiles.py`.
3. **Tk-Adaptermodule (5 Dateien neben `app.pyw`):**
   - `backdrop.py`, `drawing_image.py`, `image_preview.py`, `pinboard_pages.py`, `drawing_prototype.pyw`.

### 2.3 Lieferkopie-Architektur (`07_Python-Versionen/`)
- Das Verzeichnis [`07_Python-Versionen/`](../07_Python-Versionen) enthält eine direkt ausführbare Spiegelkopie aller 93 Laufzeitmodule und 171 Ressourcendateien (`app.pyw` heißt dort [`Glide-Aufgaben-und-Listen_v3.53.0.pyw`](../07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.53.0.pyw), gestartet über [`Schnellstart.pyw`](../07_Python-Versionen/Schnellstart.pyw)).
- Bytegleichheit zwischen `01_Repository/Glide/src/glide/` und `07_Python-Versionen/` ist zwingendes CI-Tor und wird über [`scripts/pflege/abgleich_07.py`](../01_Repository/Glide/scripts/pflege/abgleich_07.py) geprüft.

### 2.4 Datenmodelle & Persistenz ([`06_DATA_BACKUP_MIGRATION.md`](../01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md))
- Alle Nutzerdaten liegen lokal im Betriebssystem-Datenordner (überschreibbar per `GLIDE_DATA_DIR`):
  - **`liste_speicher.json` (Schema-Version 26):** Enthält alle Listen/Dokumente (`kind`: `todo`, `page`, `note`, `journal`, `drawing`, `gallery`), Ordner/Bücher/Notizbücher, hierarchische Items (`TaskItem`), Beziehungen, Wiederholungsregeln, Quellenmetadaten und Papierkorb.
  - **`settings.json` (Schema-Version 2):** UI-Konfiguration, Design/Theme, gewählter Schriftstil (`Rubik`, `DM Mono`, `DM Serif Display`, `Charis SIL`), gespeicherte Ansichten (`saved_views`), Pinnwand-Arbeitsbereiche (`pinboard_pages`), Seiten-/Notizkarten (`page_cards`).
  - **`vorlagen.json` (Schema-Version 2):** Aufgaben-, Listen-, Seiten- und Ordner-Vorlagen.
  - **`.glideexchange` (Schema-Version 2):** Kontrolliertes JSON-Austauschformat für KI-Aufträge und Patch-Vorschläge.
- **Schutzmechanismen:**
  - Exklusives Lockfile (`glide.lock` via `msvcrt.locking` / `fcntl.flock` + Sitzungs-Token in `data_lock.py` / `session_guard.py`).
  - Schreibschutz (Read-Only-Modus) bei unbekannter/höherer `DATA_SCHEMA_VERSION` (`NewerDataError`), fremder Sperre oder unaufgelöstem Speicherkonflikt.
  - Atomares Schreiben über temporäre Datei + `flush()` + `os.fsync()` + `os.replace()`.
  - Automatische Vorsicherungen vor Formatmigrationen (`SchemaBackups`), destruktiven Operationen und Anhangsumbenennungen (D67).

---

## 3. Dokumentations- und Quellenverzeichnis

Das Repository umfasst aktuell **~1.610 Dateien** im Haupt-Arbeitsbaum (ohne `.git/` und ohne den sekundären Worktree unter `.claude/worktrees/`).

| Pfadbereich | Typ & Inhalt | Umfang / Status |
|---|---|---|
| [`CLAUDE.md`](../CLAUDE.md), [`01_Repository/Glide/AGENTS.md`](../01_Repository/Glide/AGENTS.md) | **Agent- & Governance-Regeln:** Verbindliche Arbeitsregeln, Lesereihenfolge, Pfadlängengrenzen (OneDrive 400 Zeichen, `markdown_tree` 130 Zeichen), Teststufen und Verbote. | Vollständig gelesen |
| [`README.md`](../README.md), [`01_Repository/Glide/README.md`](../01_Repository/Glide/README.md), [`LICENSE`](../LICENSE), [`SECURITY.md`](../SECURITY.md) | **Öffentlicher Projekt- & Lizenzrahmen:** Produktbeschreibung, Startwege, MPL-2.0-Lizenz, Sicherheitsrichtlinie. | Vollständig gelesen |
| [`.github/workflows/`](../.github/workflows) | **CI/CD-Pipelines (5 Workflows):** `python-app.yml` (Pflichtmatrix PR/Main: Grundstufe, Linux/Windows-UI & Vollmodus, Windows-Paketbau), `release.yml` (Tag-basierter Entwurf für Win/Mac), `macos-paket.yml`, `windows-paket.yml`, `codeql.yml`. | Inventarisiert & Kernworkflows geprüft |
| [`00_Arbeitsvorbereitung/`](.) | **Projektsteuerung, Übergabe, Analyse & Roadmap:**<br>• [`Glide_Uebergabe.md`](Glide_Uebergabe.md) (Operativer Einstieg)<br>• [`Glide_Entwicklungsplan.md`](Glide_Entwicklungsplan.md) (2.647 Zeilen, alleinige Aufgabenquelle bis §21.83/§21.84)<br>• [`Glide_Analyse.md`](Glide_Analyse.md) (1.027 Zeilen, technische Analysen bis §13.31/§13.32)<br>• [`Glide_Manuelle_Pruefung.md`](Glide_Manuelle_Pruefung.md) (550 Zeilen, menschliche Abnahmeprotokolle)<br>• [`Glide_Markt_und_Vorbilder.md`](Glide_Markt_und_Vorbilder.md) (Wettbewerbs-/Mehrwertanalyse + PPTX-Anhang)<br>• [`Featurepaket_UI_UX/`](Featurepaket_UI_UX) (Prompt + 5 Referenzbilder zu D50) | Kerndokumente gelesen |
| [`01_Repository/Glide/docs/`](../01_Repository/Glide/docs) | **Kanonische Fachdokumentation (16 Markdown-Dateien inkl. `decisions/`):**<br>• [`00_INDEX.md`](../01_Repository/Glide/docs/00_INDEX.md), [`ARBEITSRICHTUNG.md`](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md) (Entscheidungen D01–D77)<br>• [`01_PRODUCT_CONSTRAINTS.md`](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md), [`02_ARCHITECTURE.md`](../01_Repository/Glide/docs/02_ARCHITECTURE.md), [`27_VORLAGEN_PRAXISANLEITUNG.md`](../01_Repository/Glide/docs/27_VORLAGEN_PRAXISANLEITUNG.md)<br>• [`05_QA_TESTPLAN.md`](../01_Repository/Glide/docs/05_QA_TESTPLAN.md), [`06_DATA_BACKUP_MIGRATION.md`](../01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md), [`07_QA_BERICHT.md`](../01_Repository/Glide/docs/07_QA_BERICHT.md)<br>• [`10_VEROEFFENTLICHUNG.md`](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md), [`20_FUNKTIONEN.md`](../01_Repository/Glide/docs/20_FUNKTIONEN.md), [`DESIGN_RICHTLINIEN.md`](../01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md), [`DOKUMENTENPFLEGE.md`](../01_Repository/Glide/docs/DOKUMENTENPFLEGE.md), [`decisions/PRODUCT_IDENTITY.md`](../01_Repository/Glide/docs/decisions/PRODUCT_IDENTITY.md) | Systematisch ausgewertet |
| [`01_Repository/Glide/src/glide/`](../01_Repository/Glide/src/glide) | **Produktiver Quellcode & Ressourcen:**<br>• 94 Python-Dateien (`app.pyw` + 92 Module + `drawing_prototype.pyw`)<br>• [`src/glide/README.md`](../01_Repository/Glide/src/glide/README.md) (Glide-System V1.15: 967 Zeilen Katalog aller 94 Module, 147 Features, 25 Steps-Bestandspakete)<br>• `resources/` (Fonts: `Rubik`, `DM Mono`, `DM Serif Display`, `Charis SIL`, `Pixelify Sans`, `DejaVu Sans`; Icons/Logos; Paletten)<br>• `vendor/tkinterdnd2/` (Drag-&-Drop-Bibliothek inkl. Binärbibliotheken für Win/Mac/Linux) | Struktur & Katalog vollständig, Code stichprobenartig |
| [`01_Repository/Glide/packaging/`](../01_Repository/Glide/packaging) & [`scripts/pflege/`](../01_Repository/Glide/scripts/pflege) | **Bau-, Pflege- & Messwerkzeuge:**<br>• `packaging/`: `build_macos.py`, `build_windows.py`, `bundle_common.py`, `sbom.py`, `verify_bundle.py`, `runtime/` (Tcl/Tk 9.1 Patches & Build-Skripte)<br>• `scripts/pflege/`: 20 Dateien (`abgleich_07.py`, `versionswechsel.py`, `logo_abgleich.py`, `showcase_abgleich.py`, Performance-Messskripte) | Inventarisiert |
| [`01_Repository/Glide/tests/`](../01_Repository/Glide/tests) | **Testlandschaft & QA-Nachweise:**<br>• `unit/`: **112 Unit-Test-Dateien** (~1.163 Einzeltests)<br>• `integration/`: **111 Integrations-Testsuiten** (Tk-GUI-, Design-, Arbeitsmodi-, Tempo- und Dauerlauftests)<br>• `tools/`: **88 Prüf- und Diagnosewerkzeuge** (u. a. `pruefen.py`, `standpruefung.py`, `altbestandteile.py`, `hintergrund/`)<br>• `fixtures/` & `qa-3.36.0/` bis `qa-3.53.0/`: Historische und aktuelle eingefrorene Prüfprotokolle (`ergebnis.json`, `README.md`) | Inventarisiert, aktuelle QA-Nachweise gelesen |
| [`05_Probelisten_Testdaten/`](../05_Probelisten_Testdaten) | **Synthetische Showcase- & Testdaten:**<br>• `Glide_Showcase_Parkquartier/` (Synthetischer 11-Dokumente-Bestand für 3.53.0 + Exportbeispiele + 56 Anhangsdateien) | Inventarisiert (keine unnötigen Binärreads) |
| [`07_Python-Versionen/`](../07_Python-Versionen) | **Startfertige Python-Lieferkopie:**<br>• `Schnellstart.pyw`, `Glide-Aufgaben-und-Listen_v3.53.0.pyw`, gespiegelte Module & Ressourcen (266 Dateien). | Inventarisiert |
| [`20_Grafik_Master/`](../20_Grafik_Master) | **Grafik-, Icon-, Font- & Screenshot-Archiv:**<br>• `01_Logo/`, `02_App_Icon/`, `03_Favicon/`, `04_Vorschau/`, `05_Inspiration/`, `06_Archiv/`, `07_Fonts/` (alle 7 Schriftfamilien inkl. historischer `Roboto Mono`, `Playfair Display`, `Fraunces`), `08_Screenshots/`, sowie unversioniert `09_Inspiration/`. | Inventarisiert (Binärdateien nicht eingelesen) |
| `GLIDE_GESAMTAUDIT_V2_2026-11-10/` | **Unversioniertes externes Audit-Paket (`??` im Root):**<br>• Enthält ein tiefgehendes Vergleichsaudit zwischen Glide (`9e767bea`) und dem separaten Folgeprojekt-Repository „Steps“ (`75329fef`) mit 14 Berichtsdateien, JSON/CSV-Inventaren und Metriken. | Kerndokumente gelesen |
| `.claude/worktrees/glide-audit-final-check-46b42f/` | **Sekundärer lokaler Git-Worktree:**<br>• Ausgecheckter Branch `claude/glide-audit-final-check-46b42f`. Vollständige zweite Arbeitskopie des Repositories. | Als duplizierter Worktree identifiziert & übersprungen |

---

## 4. Aktueller Git-Arbeitsstand (zum Prüfzeitpunkt 10.11.2026)

- **Aktiver Branch:** `main` (verfolgt `origin/main`, synchron auf Commit `9e767bea6c182442c4c6cd4e36dd0795efcc8ab9`: *„Merge pull request #75 from n05a-design/codex/glide-3.53.0-release“*).
- **Weitere lokale Branches:**
  - `codex/glide-3.53.0-release` (Stand vor dem Merge-Commit von PR #75)
  - `claude/glide-audit-final-check-46b42f` (ausgecheckt im lokalen Worktree `.claude/worktrees/glide-audit-final-check-46b42f`)
- **Letzte 5 Commits auf `main`:**
  1. `9e767be` – Merge pull request #75 from `n05a-design/codex/glide-3.53.0-release`
  2. `294fc4a` – D77: Schriften DM Mono, DM Serif Display und Charis SIL (3.53.0)
  3. `b7e9192` – Merge pull request #74 from `n05a-design/codex/glide-3.52.0-qa-release`
  4. `33f21eb` – 3.52.0: QA-Abschluss und D76-Nachführung
  5. `1258ee2` – Merge pull request #73 from `n05a-design/codex/glide-3.52.0-schriftgroessen`

### 4.1 Uncommittete Änderungen an verfolgten Dateien (7 Dateien `M`)
Alle 7 geänderten Dateien sind reine Dokumentations-Nachführungen nach dem Merge von PR #75 (`9e767bea`), um Versions-, Entscheidungs- und Abschnittsverweise auf `3.53.0` / `D77` / `§21.84` / `§13.32` zu aktualisieren:
1. [`README.md`](../README.md) (Zeile 172: Hinweis ergänzt, dass `main` seit PR #75 `9e767bea` die Quelle und Python-Lieferung `3.53.0` enthält).
2. [`00_Arbeitsvorbereitung/README.md`](README.md) (Entscheidungszähler `D01–D76` → `D01–D77`, Planverweis `§21.82` → `§21.84`, Analyseverweis `§13.31` → `§13.32`).
3. [`01_Repository/Glide/AGENTS.md`](../01_Repository/Glide/AGENTS.md) (`D01–D76` → `D01–D77`, `§21.82` → `§21.84`, `§13.31` → `§13.32`).
4. [`01_Repository/Glide/README.md`](../01_Repository/Glide/README.md) (Zeile 67: `main` auf PR #75 `9e767bea` / `3.53.0` aktualisiert).
5. [`01_Repository/Glide/docs/00_INDEX.md`](../01_Repository/Glide/docs/00_INDEX.md) (Standzeile auf `main` `9e767bea` / `3.53.0`, `D01–D77`, `§21.84`, `§13.32` aktualisiert).
6. [`01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md`](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md) (Zeile 7: `main` auf PR #75 `9e767bea` / `3.53.0` aktualisiert).
7. [`01_Repository/Glide/docs/20_FUNKTIONEN.md`](../01_Repository/Glide/docs/20_FUNKTIONEN.md) (Standzeile auf `main` `9e767bea` / `3.53.0` aktualisiert).

### 4.2 Unversionierte Pfade im Root (vor Anlage dieses Berichts)
1. `20_Grafik_Master/09_Inspiration/`: 21 PNG-Referenzbilder in 6 Unterordnern (`Buttons/`, `Dashboard/`, `Hintergründe/`, `Menüs/`, `Oberflächen/`, `Onboarding/`, `Punktdetails/`).
2. `GLIDE_GESAMTAUDIT_V2_2026-11-10/`: Externes Gesamtaudit-Paket (Glide vs. Steps).

---

## 5. Bestehende Probleme und technische Risiken

1. **Monolithische Konzentration in [`app.pyw`](../01_Repository/Glide/src/glide/app.pyw) (WA-32 / WA-39 / WA-50):**
   - Mit **69.015 Zeilen** und **~1.863 Methoden** in `ListApp` ist die Kopplung zwischen UI-Zustand, Tk-Layout und Anwendungssteuerung extrem hoch. Obwohl 88 Fachmodule Tk-frei ausgelagert wurden (D17), erfordern Querschnittsänderungen (Schriften, Fokus, Restflächen, DPI) regelmäßige Eingriffe direkt im Monolithen.
2. **Prozessweite Seiteneffekte beim Modulimport (WA-49):**
   - Das bloße Importieren von [`app.pyw`](../01_Repository/Glide/src/glide/app.pyw) verändert `sys.path`, setzt `sys.pycache_prefix`, überschreibt `sys.stdout`/`sys.stderr`, patcht global `tk.Menu` und legt bei der Konstanteninitialisierung Datenordner an. Dies erschwert isolierte Modultests und die geplante Wiederverwendung in Steps.
3. **OneDrive-Pfadlängenrisiko & enge Dateinamensbudgets ([`CLAUDE.md`](../CLAUDE.md), D67):**
   - Das Repository liegt unter `%USERPROFILE%\OneDrive\Github\glide-to-do`. OneDrive begrenzt Gesamtpfade hart auf 400 Zeichen; der `markdown_tree`-Testvertrag prüft auf **≤ 130 Zeichen** relativen Exportpfad. Zudem erzeugt der sekundäre Worktree unter `.claude/worktrees/glide-audit-final-check-46b42f/` zusätzliche tiefe Pfade im selben OneDrive-Baum.
4. **Performance-Schwankungen & offene Messbefunde (WA-36 / WA-42):**
   - Beim eingefrorenen Windows-Volltest zu `3.53.0` ([`Glide_Entwicklungsplan.md §21.83`](Glide_Entwicklungsplan.md#2183-schriftwechsel-d77-und-vollständige-testzuordnung-10112026)) traten intermittierende Überschreitungen in `test_tempo330` (66,35 ms/Bild statt ≤ 57,97 ms/Bild im ersten Lauf) und `test_seitenkarten/druck_tempo` (Quotient 1,174 statt ≤ 1,10 im zweiten Lauf) auf, bevor der dritte Gesamtlauf mit Exitcode 0 (130/131 Schritte) durchlief. Bei 10.000 Aufgaben sind Wechsel in lange Listen-/Bibliotheksansichten und Undo-Snapshots (`PackedState`) spürbar teuer.
5. **Offene native Plattform- und Paketlücken für `3.53.0`:**
   - Für `3.53.0` liegt ein grüner eingefrorener Windows-Volltest und eine visuelle Inhaber-Stichprobe („passt alles“) vor ([`07_QA_BERICHT.md`](../01_Repository/Glide/docs/07_QA_BERICHT.md)), jedoch **noch keine vollständige native macOS-/Linux-Gesamtmatrix auf Commit `9e767bea`** und **keine neu gebauten, signierten/notarisierten nativen Pakete (`.exe`/`.dmg`) für `3.53.0`**.
6. **Ungeklärte Altdiagnosen (WA-41A/B) & unvollständige SBOM (WA-46):**
   - Historische native Intel-Mac-Abstürze (`abort()` im macOS-Fontpanel / `SIGILL` in `CGBlit`) und eine 0-Byte-Sicherungsdatei aus älteren Läufen sind weiterhin als offene Diagnosespuren geführt.
   - Die CycloneDX-1.6-SBOM (`packaging/sbom.py`) deklariert sich korrekt als `incomplete`, solange C-Laufzeit- und transitive PyInstaller-Abhängigkeiten nicht vollständig im gebauten Endpaket verifiziert sind.
7. **Groß-/Kleinschreibungs-Divergenz im Showcase (Windows/macOS Case-Insensitivity):**
   - Im Showcase existieren zwei Anhangspfade mit reiner Groß-/Kleinschreibungsabweichung zwischen JSON-Referenz und Dateisystem, die unter Windows/macOS (case-insensitive) funktionieren, unter Linux (ext4, case-sensitive) jedoch fehlschlagen können.

---

## 6. Widersprüche zwischen Dokumentation und Code / Git-Realität

Beim Abgleich der Dokumentation gegen den tatsächlichen Quellcode und Git-Stand (`main` @ `9e767bea`) wurden **fünf konkrete Inkonsistenzen** festgestellt:

1. **Unvollständige Nachführung von PR #75 (`3.53.0` auf `main`) sowie tote Verweise auf `§21.84` und `§13.32`:**
   - **Befund:** Die 7 uncommitteten Arbeitsbaum-Änderungen (z. B. in [`01_Repository/Glide/AGENTS.md`](../01_Repository/Glide/AGENTS.md), [`01_Repository/Glide/docs/00_INDEX.md`](../01_Repository/Glide/docs/00_INDEX.md) und [`00_Arbeitsvorbereitung/README.md`](README.md)) verweisen bereits auf **`Plan §21.84`** und **`Analyse §13.32`** und erklären `3.53.0` (`9e767bea`) zum Stand von `main`.
   - **Widerspruch:**
     - In [`00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md`](Glide_Entwicklungsplan.md) endet das Dokument jedoch bei **`§21.83`** (ein `§21.84` existiert noch nicht), und Zeile 38 führt `main` noch auf dem Vorstand vor PR #75.
     - In [`00_Arbeitsvorbereitung/Glide_Analyse.md`](Glide_Analyse.md) endet das Dokument bei **`§13.31`** (ein `§13.32` existiert noch nicht).
     - Auch [`00_Arbeitsvorbereitung/Glide_Uebergabe.md`](Glide_Uebergabe.md) und [`01_Repository/Glide/docs/07_QA_BERICHT.md`](../01_Repository/Glide/docs/07_QA_BERICHT.md) führen `3.53.0` in ihren Kopfzeilen noch als unveröffentlichten Branch-Kandidaten vor Merge von PR #75.

2. **Veraltete Schriftdokumentation (D60 statt D77) in Produktgrenzen und Veröffentlichungsdoku:**
   - **Code-Realität (D77 / 3.53.0):** [`font_catalog.py`](../01_Repository/Glide/src/glide/font_catalog.py) und [`src/glide/resources/fonts/`](../01_Repository/Glide/src/glide/resources/fonts) liefern `Rubik`, `DM Mono`, `DM Serif Display`, `Charis SIL`, `Pixelify Sans` und `DejaVu Sans` aus. `Roboto Mono`, `Playfair Display` und `Fraunces` wurden aus den App-Ressourcen entfernt.
   - **Dokumentations-Widerspruch:**
     - [`01_PRODUCT_CONSTRAINTS.md`](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md) (Zeile 11) nennt unter „Mitgeliefert“ weiterhin die alten D60-Schriften (`Roboto Mono`, `Playfair Display`, `Fraunces`).
     - [`10_VEROEFFENTLICHUNG.md`](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md) (Zeilen 178–188) führt in der Lizenztabelle der mitgelieferten Schriften ebenfalls noch `Roboto Mono`, `Playfair Display` und `Fraunces` statt `DM Mono`, `DM Serif Display` und `Charis SIL`.

3. **Fehlender Eintrag für Entscheidung `D77` (und `D74`–`D76`) in `ARBEITSRICHTUNG.md`:**
   - **Befund:** Während [`00_INDEX.md`](../01_Repository/Glide/docs/00_INDEX.md) und [`AGENTS.md`](../01_Repository/Glide/AGENTS.md) auf `Entscheidungen D01–D77` in `ARBEITSRICHTUNG.md` verweisen, endet die Entscheidungstabelle in [`ARBEITSRICHTUNG.md`](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md) bei **`D73`** (Zeile 218). Die Entscheidungen `D74` (Steps-Systemkatalog), `D75`, `D76` (Schriftgrößen 3.52.0) und `D77` (Schriftwechsel 3.53.0) stehen zwar im Entwicklungsplan (§21.79–§21.83), fehlen aber in der Tabelle von `ARBEITSRICHTUNG.md`.

4. **Abweichung zwischen `CLAUDE.md` und `AGENTS.md`:**
   - [`CLAUDE.md`](../CLAUDE.md) (Zeilen 21–22) verweist noch auf `D01–D76`, `§21.82` und `§13.31`, während [`01_Repository/Glide/AGENTS.md`](../01_Repository/Glide/AGENTS.md) im Arbeitsbaum bereits auf `D01–D77`, `§21.84` und `§13.32` geändert wurde.

5. **Existenz des Folgeprojekts „Steps“:**
   - [`AGENTS.md`](../01_Repository/Glide/AGENTS.md), [`src/glide/README.md`](../01_Repository/Glide/src/glide/README.md) und [`Glide_Uebergabe.md`](Glide_Uebergabe.md) formulieren noch, dass für Steps *„bisher kein Repository angelegt“* wurde. Das im Arbeitsbaum abgelegte Gesamtaudit `GLIDE_GESAMTAUDIT_V2_2026-11-10/` belegt jedoch, dass parallel bereits ein Steps-Repository (`VERSION=0.0.0-dev`, Commit `75329fef`, 1.931 Dateien) existiert.

---

## 7. Offene Entscheidungen und Informationslücken

1. **Veröffentlichungs- und Inhabertore (D43 / [`10_VEROEFFENTLICHUNG.md`](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md)):**
   - **I1:** Endgültige Impressums-/Inhaber- und Kontaktangaben für öffentliche Pakete.
   - **I3:** Code-Signing-Zertifikate (Apple Developer ID + Notarisierung für macOS; Authenticode-Zertifikat für Windows).
   - **I4:** Professionelle Markenrechtsprüfung für den Namen „Glide“.
   - **I6:** Menschliche Gesamtabnahme (DPI-/Mehrmonitor-Matrix, physische macOS-/Windows-Paketabnahme auf `3.53.0`).
   - **I11:** Entscheidung über die öffentliche Schaltung eines GitHub-Release-Entwurfs (`v3.53.0`).
2. **Disposition der unversionierten Arbeitsbaum-Inhalte:**
   - Soll `20_Grafik_Master/09_Inspiration/` (21 PNGs) in Git aufgenommen und in [`20_Grafik_Master/README.md`](../20_Grafik_Master/README.md) inventarisiert werden?
   - Soll `GLIDE_GESAMTAUDIT_V2_2026-11-10/` außerhalb des Glide-Repos archiviert oder wieder entfernt werden (da es laut [`DOKUMENTENPFLEGE.md`](../01_Repository/Glide/docs/DOKUMENTENPFLEGE.md) keine zweite Wahrheitsquelle neben `docs/` und `00_Arbeitsvorbereitung/` geben darf)?
   - Kann der sekundäre Worktree `.claude/worktrees/glide-audit-final-check-46b42f/` bereinigt werden?
3. **Fachliche Roadmap-Auswahl durch den Inhaber:**
   - Reihenfolge und Freigabe der offenen Aufgaben (`WA-21` Fundortübersicht vs. technische Entkopplung `WA-32/39/49/50` vs. Performance `WA-36` vs. Ausbauphasen `E-P1–E-P5` / `WA-52–WA-59`).
   - Offene Detailfrage aus **D68**: Sollen aktive Umschalter neben dem Ansichtstitel ebenfalls die Themenfarbe tragen, oder bleibt U15 (aktive Umschalter neutral, Lila für Hinzufügen) bestehen?
4. **Architekturentscheidung Glide ↔ Steps (O1–O10 aus dem Gesamtaudit):**
   - Sollen die Tk-freien Kernmodule (`persistence`, `undo_history`, `data_lock`, `ui_design`, `font_catalog` etc.) als echtes geteiltes Paket gepflegt werden, oder bleiben Glide und Steps getrennte Codebasen mit dokumentiertem Übernahmevertrag?

---

## 8. Priorisierte Empfehlungen für die weitere Bearbeitung

1. **Priorität 1 – Dokumentations-Nachführung zu PR #75 (`3.53.0`) konsistent abschließen:**
   - Fehlende Abschnitte `§21.84` in [`Glide_Entwicklungsplan.md`](Glide_Entwicklungsplan.md) und `§13.32` in [`Glide_Analyse.md`](Glide_Analyse.md) ergänzen (oder die Verweise in den 7 geänderten Dateien auf `§21.83` / `§13.31` belassen).
   - Standzeilen in [`Glide_Uebergabe.md`](Glide_Uebergabe.md), [`07_QA_BERICHT.md`](../01_Repository/Glide/docs/07_QA_BERICHT.md), [`Glide_Entwicklungsplan.md`](Glide_Entwicklungsplan.md) und [`CLAUDE.md`](../CLAUDE.md) auf `main` @ `9e767bea` (`3.53.0`, `D77`) synchronisieren.
   - Entscheidungen `D74`–`D77` in [`ARBEITSRICHTUNG.md`](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md) nachtragen.
   - Schrifttabellen in [`01_PRODUCT_CONSTRAINTS.md`](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md) und [`10_VEROEFFENTLICHUNG.md`](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md) auf die D77-Schriften (`DM Mono`, `DM Serif Display`, `Charis SIL`) aktualisieren.
2. **Priorität 2 – Arbeitsbaum bereinigen & CI-Grundstufe verifizieren:**
   - Entscheidung über den Verbleib von `GLIDE_GESAMTAUDIT_V2_2026-11-10/`, `20_Grafik_Master/09_Inspiration/` und `.claude/worktrees/glide-audit-final-check-46b42f/` treffen.
   - Anschließend die strenge CI-Grundstufe ([`tests/tools/pruefen.py`](../01_Repository/Glide/tests/tools/pruefen.py) / [`tests/tools/standpruefung.py`](../01_Repository/Glide/tests/tools/standpruefung.py)) ausführen, um Link-, Stand- und Liefergleichheit (`07_Python-Versionen`) formal grün nachzuweisen.
3. **Priorität 3 – Case-Sensitivity-Korrektur im Showcase & Plattform-/Paketabschluss 3.53.0:**
   - Die zwei Groß-/Kleinschreibungs-Abweichungen in [`05_Probelisten_Testdaten/Showcase/`](../05_Probelisten_Testdaten/Showcase) beheben.
   - Native Linux-/macOS-Prüfläufe und Paketbauten für `3.53.0` auswerten bzw. anstoßen.
4. **Priorität 4 – Technische Entkopplung (`WA-49` / `WA-32`) vor weiterer Steps-Extraktion:**
   - Zuerst die Import-Seiteneffekte in [`app.pyw`](../01_Repository/Glide/src/glide/app.pyw) über eine explizite `RuntimeConfig`/`RuntimePaths`-Initialisierung kapseln (`WA-49`), bevor weitere Module in Richtung Steps geteilt oder umgebaut werden.

---

## 9. Prüfstatus dieser Bestandsaufnahme

| Prüfbereich | Status | Details |
|---|---|---|
| **Vollständig geprüft** | ✅ | • Git-Status, Branches, letzte Commits und sämtliche 7 Diffs im Arbeitsbaum<br>• Vollständiges Dateibaum-Inventar des Repositories (~1.610 Dateien)<br>• Governance- & Einstiegsdokumente (`CLAUDE.md`, `AGENTS.md`, beide `README.md`, `VERSION`, `GLIDE_SYSTEM_VERSION`, `00_INDEX.md`, `01_PRODUCT_CONSTRAINTS.md`, `10_VEROEFFENTLICHUNG.md`, `DOKUMENTENPFLEGE.md`, `00_Arbeitsvorbereitung/README.md`, `Glide_Uebergabe.md`, `standpruefung.py`)<br>• Kernergebnisse aus `GLIDE_GESAMTAUDIT_V2_2026-11-10` |
| **Teilweise / schwerpunktmäßig geprüft** | ◐ | • Große Referenzdokumente (jeweils Kopf, relevante Hauptabschnitte und aktuelle Schlusskapitel bis 10.11.2026 gelesen): `src/glide/README.md` (Glide-System V1.15), `02_ARCHITECTURE.md`, `06_DATA_BACKUP_MIGRATION.md`, `07_QA_BERICHT.md`, `ARBEITSRICHTUNG.md`, `DESIGN_RICHTLINIEN.md`, `Glide_Entwicklungsplan.md` (§1 & §§21.75–21.83), `Glide_Analyse.md` (§1, §2 & §§13.25–13.31), `Glide_Manuelle_Pruefung.md`<br>• Quellcode-Einstieg von [`app.pyw`](../01_Repository/Glide/src/glide/app.pyw) (Zeilen 1–350: Imports, Startup-Hooks, Branding-Konstanten, Font-Auflösung) |
| **Noch offen (bewusst nicht eingelesen / nicht ausgeführt)** | ○ | • Vollständiger Methodenkörper von `app.pyw` (Zeilen 351–69.015) sowie der Einzelcode der 93 weiteren Module und 311 Testdateien (über den Systemkatalog V1.15 hinaus)<br>• Ausführung von Tests oder Pflegeskripten<br>• Binärdateien, Font-Binaries, Bilder und `.claude/worktrees/` |
