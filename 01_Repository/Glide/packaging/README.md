# Paketierung Glide

Stand 27.10.2026 · Glide 3.47.0 · Aufgabenformat 26 · Einstellungen 2 · Vorlagen 2

**Aktueller Quellkandidat 3.47.0:** Mehrfachplanung und Nebenansichtsverlauf ergänzen Tagessteuerung/Suche und die vorherigen Technik-/Startseitenpakete. Kopier-/Baulisten enthalten alle 88 Laufzeitdateien, auch `persistence.py` und `home_task_tiles.py`. Die bestehenden Windows-/Mac-Pakete bleiben beim eingefrorenen 3.45.0-Abschluss `d516ca67…`; neue Funktionen oder eine Versionszeile ersetzen keinen Paketneubau. [Gemeinsamer Quell-/Prüf-/Lieferstand](../tests/qa-3.46.0/zweierpaket_2026-10-27/README.md).

Die eigenständigen Entwicklungspakete für Windows x64 und macOS arm64 sind auf 3.45.0 neu gebaut und geprüft. Windows: 103 Dateien, Python 3.14.7/Tcl-Tk 9.0.4, kompilierter Quell-/PE-/Lizenzabgleich und lokale Startprobe grün. Mac: 333 Dateien und 29 interne Symlinks, Python 3.14.5/Tcl-Tk 9.0.3, nativer arm64-Bau, Mach-O-/Ad-hoc-Signaturprüfung und Prozesssandbox-Startprobe grün. Beim damaligen Abschluss war auch die Python-Lieferung bytegleich; alte aktive 3.42.0-Pakete liegen im jeweiligen `build/.../Archiv`. [Nachweise](../tests/qa-3.45.0/paketabschluss_2026-10-26/README.md). Windows bleibt unsigniert; öffentliche Signaturen, Installer und Menschenabnahme sind eigene Tore.

## Aktuelle Lieferartefakte

- Windows: `build/windows/Glide-3.45.0/Glide.exe` und `build/windows/Glide-3.45.0-windows-x64.zip`.
- Mac: `build/macos/Glide-3.45.0-macos-arm64.tar.gz` nativ entpacken. Die lokale `build/macos/Glide.app` ist eine Windows-Inspektionskopie mit NT-Linkzielen; native Weitergabe über das unveränderte TAR.
- Wiederholbarer nativer Mac-Bau: `sh packaging/paket/baue_und_pruefe_macos.sh --python /Pfad/python3`; neuer Bauordner außerhalb OneDrive, exakte Originalruntime gemäß Lizenzmanifest. `.github/workflows/macos-paket.yml` führt denselben Weg auf einem nativen arm64-Runner aus. [Grüner nativer Lauf](https://github.com/n05a-design/glide-to-do/actions/runs/40328682255).

## Inhalt eines Pakets

`src/glide/app.pyw` mit allen Modulen daneben – `glide_start.py`, `drawing.py`, `drawing_image.py`, `backdrop.py`, `page_markdown.py`, `image_preview.py`, `image_conversion.py`, `logo.py`, `schema_backups.py`, `sidebar_policy.py`, `svg_geometry.py`, `home_tiles.py`, `home_dashboard.py`, `home_task_tiles.py`, `capture_parser.py`, `eisenhower.py`, `today_view.py`, `content_search.py`, `save_comparison.py`, `view_metrics.py`, `action_catalog.py`, `ui_design.py`, `planning.py`, `day_proposal.py`, `focus_timer.py`, `task_references.py`, `interaction_policy.py`, `object_references.py`, `week_planning.py`, `page_features.py`, `repeat_rules.py`, `repeat_ics.py`, `routines.py`, `runtime_check.py`, `release_notes.py`, `appearance.py`, `preview_tools.py`, `filter_explain.py`, `exchange_patch.py`, `exchange_recipes.py`, `markdown_tree.py`, `pinboard_pages.py`, `view_definition.py`, `action_menu.py`, `side_view.py`, `compact_mode.py`, `storage_health.py`, `backup_catalog.py`, `attachment_policy.py`, `backup_diff.py`, `render_retention.py`, `logo_raster.py`, `symbol_policy.py`, `motion.py`, `task_editing.py`, `daily_hints.py`, `ics_recurrence.py`, `occupied_time.py`, `ics_busy.py`, `ics_timezone.py`, `timezones.py`, `day_relief.py`, `busy_calendar.py`, `calendar_service.py`, `animation.py`, `animation_export.py`, `attachment_paths.py`, `backup_snapshot.py`, `notion_archive.py`, `notion_hierarchy.py`, `notion_import.py`, `notion_reimport.py`, `page_restore.py`, `restore_assets.py`, `source_metadata.py`, `accessibility.py`, `accessibility_bindings.py`, `core_accessibility.py`, `glyph_metrics.py`, `undo_history.py`, `structural_guard.py`, `load_phases.py`, `editor_flush.py`, `data_lock.py`, `item_index.py`, `save_result.py`, `persistence.py` (Aufgaben siehe [Modulübersicht](../src/glide/README.md)) –, der vollständige Ordner `resources` (Schriften mit Lizenztexten, Vorlagen, Logo) und `vendor/tkinterdnd2` nur mit den Bibliotheken der Zielplattform, samt Lizenzen. Die Bedienprobe `drawing_prototype.pyw` gehört nicht hinein. Daten werden nie in den Installationsordner geschrieben.

## Kennungen (26.09.2026, nie ändern)

- macOS: `de.shaye.glide` (`APP_BUNDLE_ID`)
- Windows: `Shaye.Glide` (`APP_USER_MODEL_ID`)

Eingetragen im [Produktregister](../docs/decisions/PRODUCT_IDENTITY.md).

## Werkzeuge

**Programmsymbole – [`baue_symbole.py`](baue_symbole.py):** erzeugt mit Tk 9 aus `src/glide/resources/logo/glide-app-icon.svg` (Kopie von `20_Grafik_Master/03_Fav-Icon/App-Icon-transparent-02.svg`) unter `assets/icons/` die Dateien `glide.ico` (Windows, 16–256 px), `glide_macos_1024.png` (macOS, mit Apples Rand) und `glide_512.png` (Linux, Stores).

**macOS-Vorstufe mit externem Python – [`macos/baue_app.py`](macos/baue_app.py):**

```
python3 -B packaging/baue_symbole.py
python3 -B packaging/macos/baue_app.py --ziel build/macos-vorstufe [--symbol anderes_1024.png]
```

Baut `Glide.app` mit Quellen und Modulen (Start über `glide_start.py`), Ressourcen, dem macOS-Teil von `vendor/tkinterdnd2`, einer Kopie des Python-Starters aus dem installierten python.org-Framework, `Glide.icns` und Ad-hoc-Signatur. macOS führt den Prozess als „Glide“ mit `de.shaye.glide`. Das Bundle braucht das installierte Python mit Tk und ist nicht zur Weitergabe gedacht.

**Windows-Verknüpfung – [`windows/verknuepfung_anlegen.ps1`](windows/verknuepfung_anlegen.ps1):** legt im Startmenü „Glide“ an (pythonw.exe mit `app.pyw`, Symbol `glide.ico`) mit der AppUserModelID; kein Adminrecht, keine Registry. Glide meldet sich beim Start mit derselben Kennung an (`set_windows_app_user_model_id`). Unter Windows noch nicht ausgeführt.

Die vorhandene Vorstufe bleibt durch `tests/integration/test_paketierung330.py` geprüft. Die eigenständigen Entwicklungsbauten stehen im folgenden Abschnitt; Developer-ID-Signatur, Notarisierung, Windows-Zertifikat und Installer bleiben nach D43 gesondert offen.

## Eigenständige Entwicklungspakete (Paket 7)

Die Bauwerkzeuge unter `packaging/paket` bündeln Python, Tcl/Tk, alle aktuellen
Glide-Module und die Ressourcen der gewählten Plattform. Gebaut wird nativ auf
macOS arm64 beziehungsweise Windows x64. PyInstaller 6.22.3 und die übrigen
Bauabhängigkeiten stehen in `requirements/build-*.txt`; sie sind keine
Laufzeitabhängigkeiten der Python-Fassung. Ein eigenständiges Linux-Paket ist
nicht gewählt.

Für jeden Bau einen neuen Ordner außerhalb von OneDrive verwenden. Folgende
Mac-Aufrufe erfolgen aus `01_Repository/Glide`; `BAU_GLIDE` bezeichnet ausschließlich
den eigenen Bauordner:

```sh
BAU_GLIDE="$TMPDIR/glide-paketbau"
mkdir "$BAU_GLIDE"
python3 -m venv "$BAU_GLIDE/venv"
"$BAU_GLIDE/venv/bin/python3" -m pip install -r requirements/build-macos.txt
"$BAU_GLIDE/venv/bin/python3" -B packaging/paket/lizenzen_vorbereiten_macos.py \
  --quelle src/glide --repo . --ziel "$BAU_GLIDE/lizenzen"
"$BAU_GLIDE/venv/bin/python3" -B packaging/paket/baue_paket.py \
  --quelle src/glide --version "$(cat VERSION)" --ziel "$BAU_GLIDE/bau" \
  --plattform macos-arm64 --lizenzen "$BAU_GLIDE/lizenzen"
PYTHON_GLIDE="$("$BAU_GLIDE/venv/bin/python3" -c 'import sys; print(sys.base_prefix)')"
"$BAU_GLIDE/venv/bin/python3" -B packaging/paket/pruefe_start_macos.py \
  --paket "$BAU_GLIDE/bau/dist/Glide.app" --bericht "$BAU_GLIDE/startprobe.json" \
  --sperren "$PYTHON_GLIDE" --sperren "$BAU_GLIDE/venv" \
  --sperren "$BAU_GLIDE/bau/quelle" --sperren "$PWD"
```

Der eingecheckte Mac-Lizenzbestand belegt Python 3.14.5/Tcl-Tk 9.0.3 und seine
konkreten Bibliotheken. Der Generator prüft Laufzeit, Bauabhängigkeiten und
Originaltexte vor der Übernahme. Eine andere Laufzeit benötigt passende neue
Originalbelege; der Generator verweigert eine bloße Umbenennung. Aktuelle
Projektlizenzhinweise werden aus genau dem anschließend gebauten Quellstand
übernommen.

Der native Windows-Bau läuft im Workflow `Glide-Prüfung` nach der vollständigen
Linux-/Windows-Matrix: eigene Bauumgebung, Lizenzbelege aus der tatsächlich
installierten Laufzeit, `baue_paket.py --plattform windows-x64` und anschließend
`pruefe_start_windows.py`. Dessen ACL-Sperre ist ausschließlich für den
vergänglichen GitHub-Hosted-Runner zugelassen. Originale Zugriffsregeln werden im
`finally`-Zweig wiederhergestellt und vollständig verglichen; nur der AI-Modellmarker
darf im vergänglichen Runner abweichen, der Rohvergleich bleibt separat sichtbar.
Das externe Python wird danach erneut gestartet.
Der Workflow sichert Paket und Belege als getrennte Artefakte.

Die native Startprobe legt ausschließlich künstliche Daten an und prüft sechs
Ansichten, Speichern und erneutes Dateilesen, Abhaken und Undo, den App-Sicherungs-
Rundlauf, gebündelte Schriften/Logo/DND, Ressourcen-
und Lizenzhashes sowie geladene Bibliotheken und Python-Suchpfade. Das externe
Python muss in einer Gegenprobe tatsächlich blockiert sein. `test_paket3420.py`
prüft zusätzlich die vollständigen realen Bauquellen beider Zielpakete; ein
nativer Startbericht kann mit `--startnachweis <Datei>` abgeglichen werden.
Bau, GUI-Proben und Vollprüfung nacheinander ausführen. Der genaue Abnahmestand
steht im [QA-Bericht](../docs/07_QA_BERICHT.md).

Mac-Pakete tragen eine geprüfte Ad-hoc-Signatur, Windows-Pakete bleiben ohne
Inhaberzertifikat unsignierte Entwicklungsartefakte. Öffentliche Signaturen,
Installer und Veröffentlichungstore sind weiterhin getrennt offen (D43).
