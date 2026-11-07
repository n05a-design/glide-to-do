# Paketierung Glide

Stand 07.11.2026 · Glide 3.50.6 · Erster öffentlicher Stand (intern: öffentliche erste Beta) · Aufgabenformat 26

**Windows-Abnahmekandidat 3.50.3, 05.11.2026:** `build/windows/Kandidaten/Glide-3.50.3-abnahme-20261105` enthält den lokal gebauten und isoliert gestarteten 3.50.3-Stand mit eigener Tcl/Tk 9.1.0. 132 Lieferdateien bytegleich zum Bau; Quell-/PE-/Lizenzprüfung grün. [Nachweis und genaue Matrix-/Menschen-/Mac-Grenzen](../tests/qa-3.50.3/abnahmekorrekturen_2026-11-05/README.md). Die regulären 3.50.0-Pakete unten bleiben datierte andere Lieferstände. Kein öffentlicher Release aus dem Kandidaten abgeleitet.

**Lieferabgleich 03.11.2026:** Quelle/Python 3.50.2 mit vier korrigierten Schriftklassen und SemiBold-Schnitten; reguläre lokale Windows-/Mac-Pakete weiterhin 3.50.0 auf Apphash `067e683b…`. Windows-Paket: 104 Dateien bytegleich zu seinem ZIP; Mac-TAR unverändert zum datierten Lieferhash. Auf diesem Windows-Checkout liegt kein aktuelles `build/macos/Glide.app`. [Aktueller Abgleich und Grenzen](../tests/qa-3.50.2/ablageabgleich_2026-11-03/README.md). Kein nativer Neubau oder Release aus der Versionsnummer abgeleitet.


Der Paketstarter begleitet den Appprozess für lokale technische Diagnose und den tatsächlichen Exitstatus; `--paket-pruefen` bleibt der direkte isolierte Prüfweg. Alle 92 Laufzeitdateien einschließlich Sitzungs-/Diagnoseschutz und Ressourcen gehören zum Paket. Die aktuelle Lieferung wird ausschließlich dem unten verlinkten 3.50-Nachweis zugeordnet. Frühere Bauwerte bleiben in den datierten [3.45-Paketbelegen](https://github.com/n05a-design/glide-to-do/blob/1ba516a8acfb6ef73b807131f8365bfae8f64816/01_Repository/Glide/tests/qa-3.45.0/paketabschluss_2026-10-26/README.md) und dem [3.49-Abschluss](https://github.com/n05a-design/glide-to-do/blob/f1a5b5b6e0f97f2b5eab1ac552999c33c6416e69/01_Repository/Glide/tests/qa-3.49.0/gesamtabschluss_2026-10-31/README.md) erhalten.

**Schriftstile D60:** Quelle/Python enthalten Rubik als Vorgabe, Roboto Mono, Playfair Display und Fraunces; DejaVu bleibt interner Symbolbegleiter, Pixelify für das Pixel-Design. Lizenzbestand, beide Lizenzvorbereiter und Paketstartprobe erfassen die neuen Originalschriften. Diese Quelländerung ist noch kein Neubau des vorhandenen Windows-/Mac-Pakets. [Prüfung und Grenzen](../tests/qa-3.50.0/schriftstile_2026-11-03/README.md).

## Aktuelle Lieferartefakte

Der erste öffentliche Stand heißt auf allen Ausgaben 3.50.0. Tatsächlich geprüfte Dateien, Laufzeiten und SHA-256 stehen im [QA-Bericht](../docs/07_QA_BERICHT.md) und im aktuellen Releaseaudit. `build/windows/Glide-3.50.0`, das reguläre Windows-ZIP und `build/macos/Glide-3.50.0-macos-arm64.tar.gz` enthalten den damals geprüften Code `067e683b…`; sie enthalten die spätere 3.50.2-Pflege nicht; frühere lokale Ausgaben sind im jeweiligen `Archiv` erhalten. Mac-TAR-Dateien bewahren POSIX-Verknüpfungen und Dateimodi. Unter `build/macos/Glide.app` darf ausschließlich ein eigenständiges geprüftes Bundle liegen; eine Vorstufe darf es niemals ersetzen. Auf dem Mac kann der Pfad auf die native geprüfte Installation außerhalb des Syncordners verweisen, etwa `~/Applications/Glide.app`; auf Windows ist diese externe Mac-Verknüpfung kein vorhandenes ausführbares Bundle. OneDrive kann Framework-Bundlemarker verändern und die strenge Signaturprüfung beanstanden. Deshalb das unveränderte aktuelle TAR nativ auf dem Mac entpacken und dort erneut prüfen. Audit-/UI-Kandidaten liegen zusätzlich unter `build/<Plattform>/Kandidaten`; eine gerätespezifische Verknüpfung ersetzt kein plattformübergreifendes Paket.

Wiederholbarer nativer Mac-Bau mit eigener 9.1-Runtime: `PYTHONPATH=/Pfad/runtime91/python-extension sh packaging/paket/baue_und_pruefe_macos.sh --python /Pfad/python3 --basis /Pfad/lizenzen91 --runtime-bau /Pfad/runtime91/runtime-bau.json --ziel /neuer/Bauordner`. Originalquellen und Lizenzbasis gemäß [Runtime-Anleitung](runtime/README.md) vorbereiten. Ohne optionale Runtime-/Basisargumente bleibt der geprüfte Originalruntime-Bau möglich. `.github/workflows/macos-paket.yml` baut auf macOS arm64 die eigene Tk-9.1-Runtime und das eigenständige Paket; der Windows-Bau folgt seiner vollständigen Matrix im Hauptworkflow. Beide installieren Bauabhängigkeiten ausschließlich mit Originalhashes.

## Inhalt eines Pakets

`src/glide/app.pyw` mit allen Modulen daneben – `glide_start.py`, `drawing.py`, `drawing_image.py`, `backdrop.py`, `page_markdown.py`, `image_preview.py`, `image_conversion.py`, `logo.py`, `brand.py`, `schema_backups.py`, `sidebar_policy.py`, `svg_geometry.py`, `home_tiles.py`, `home_dashboard.py`, `home_task_tiles.py`, `capture_parser.py`, `eisenhower.py`, `today_view.py`, `content_search.py`, `save_comparison.py`, `view_metrics.py`, `action_catalog.py`, `ui_design.py`, `font_catalog.py`, `planning.py`, `day_proposal.py`, `focus_timer.py`, `task_references.py`, `interaction_policy.py`, `object_references.py`, `week_planning.py`, `page_features.py`, `repeat_rules.py`, `repeat_ics.py`, `routines.py`, `runtime_check.py`, `release_notes.py`, `appearance.py`, `preview_tools.py`, `filter_explain.py`, `exchange_patch.py`, `exchange_recipes.py`, `markdown_tree.py`, `pinboard_pages.py`, `settings_compat.py`, `view_definition.py`, `action_menu.py`, `side_view.py`, `compact_mode.py`, `storage_health.py`, `session_guard.py`, `runtime_diagnostics.py`, `backup_catalog.py`, `attachment_policy.py`, `backup_diff.py`, `render_retention.py`, `logo_raster.py`, `symbol_policy.py`, `motion.py`, `task_editing.py`, `daily_hints.py`, `ics_recurrence.py`, `occupied_time.py`, `ics_busy.py`, `ics_timezone.py`, `timezones.py`, `day_relief.py`, `busy_calendar.py`, `calendar_service.py`, `animation.py`, `animation_export.py`, `attachment_paths.py`, `backup_snapshot.py`, `notion_archive.py`, `notion_hierarchy.py`, `notion_import.py`, `notion_reimport.py`, `page_restore.py`, `restore_assets.py`, `source_metadata.py`, `accessibility.py`, `accessibility_bindings.py`, `core_accessibility.py`, `glyph_metrics.py`, `undo_history.py`, `structural_guard.py`, `load_phases.py`, `editor_flush.py`, `data_lock.py`, `item_index.py`, `save_result.py`, `persistence.py` (Aufgaben siehe [Modulübersicht](../src/glide/README.md)) –, der vollständige Ordner `resources` (Schriften mit Lizenztexten, Vorlagen, Logo) und `vendor/tkinterdnd2` nur mit den Bibliotheken der Zielplattform, samt Lizenzen. Die Bedienprobe `drawing_prototype.pyw` gehört nicht hinein. Daten werden nie in den Installationsordner geschrieben.

## Kennungen (26.09.2026, nie ändern)

- macOS: `de.shaye.glide` (`APP_BUNDLE_ID`)
- Windows: `Shaye.Glide` (`APP_USER_MODEL_ID`)

Eingetragen im [Produktregister](../docs/decisions/PRODUCT_IDENTITY.md).

## Werkzeuge

**Programmsymbole – [`baue_symbole.py`](baue_symbole.py):** erzeugt mit Tk 9 aus `src/glide/resources/logo/glide-app-icon.svg` (Kopie von `20_Grafik_Master/01_Logo/2026-Glide-Logo-App-und-Fav-Icon.svg`) unter `assets/icons/` die Dateien `glide.ico` (Windows, 16–256 px), `glide_macos_1024.png` (macOS, mit Apples Rand) und `glide_512.png` (Linux, Stores).

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

Der native Windows-Bau steht in `.github/workflows/windows-paket.yml` und läuft im
Workflow `Glide-Prüfung` nach der vollständigen Linux-/Windows-Matrix: eigene Bauumgebung, Lizenzbelege aus der tatsächlich
installierten Laufzeit, `baue_paket.py --plattform windows-x64` und anschließend
`pruefe_start_windows.py`. Dessen ACL-Sperre ist ausschließlich für den
vergänglichen GitHub-Hosted-Runner zugelassen. Originale Zugriffsregeln werden im
`finally`-Zweig wiederhergestellt und vollständig verglichen; nur der AI-Modellmarker
darf im vergänglichen Runner abweichen, der Rohvergleich bleibt separat sichtbar.
Das externe Python wird danach erneut gestartet.
Der Workflow sichert Paket und Belege als getrennte Artefakte.

Der Mac-Workflow (`macos-paket.yml`) erzeugt nach Archiv- und Startprüfung zusätzlich
`Glide-<Version>-macos-arm64.dmg`: Inhalt ausschließlich aus dem geprüften TAR,
`/Applications`-Verknüpfung zum Hineinziehen, nach `hdiutil verify` schreibgeschützt
eingehängt, Datei- und Linkbestand gegen das Archiv verglichen und Ad-hoc-Signatur
erneut geprüft. Ein Tag `v<VERSION>` auf einem `main`-Commit startet `release.yml`:
beide Paketworkflows bauen neu, danach entsteht ein GitHub-Release-**Entwurf** als
Vorabversion mit Windows-ZIP, DMG, TAR und `.sha256`-Dateien. Den Stand der Vollmatrix
für denselben Commit schreibt der Workflow in die Versionshinweise; veröffentlicht wird
nur von Hand ([Veröffentlichung](../docs/10_VEROEFFENTLICHUNG.md#github-auftritt)).

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
