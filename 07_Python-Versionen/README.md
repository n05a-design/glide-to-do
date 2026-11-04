# Aktuelle startbare Python-Fassung

Stand 04.11.2026 · Glide 3.50.2 · Erster öffentlicher Stand · Aufgabenformat 26 · Vorlagenformat 2

Die startbare Python-Fassung `Glide-Aufgaben-und-Listen_v3.50.2.pyw` und alle Begleitmodule/Ressourcen entsprechen dem Quellstand 3.50.2 (öffentliche erste Beta). Hintergrundfarben, volle Seitenleiste, Blockziehen, Nebenansicht und Fokusfunktionen sind enthalten. Der [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md) nennt die tatsächlichen Prüfungen und Paketlieferungen. Die menschliche Prüfung folgt nach der technischen Fertigstellung; Screenreader-Abnahme ist bis Bedarf zurückgestellt.

[Prüfung, SHA-256 und Liefergrenzen](../01_Repository/Glide/tests/qa-3.50.2/ci247_2026-11-03/README.md): Themenflächenkorrektur und die vier Schriftstile mit Rubik als Vorgabe sind enthalten; Python-Abgleich bytegleich zur Quelle. Native Pakete sind getrennte Lieferstände. Ältere Absätze unten bewahren ihre datierten Prüfstände. In denselben Ordner gehören:

- die Module `drawing.py`, `drawing_image.py`, `backdrop.py`, `page_markdown.py`, `image_preview.py`, `image_conversion.py`, `logo.py`, `schema_backups.py`, `sidebar_policy.py`, `svg_geometry.py`, `home_tiles.py`, `home_dashboard.py`, `home_task_tiles.py`, `capture_parser.py`, `eisenhower.py`, `today_view.py`, `content_search.py`, `save_comparison.py`, `view_metrics.py`, `action_catalog.py`, `ui_design.py`, `font_catalog.py`, `planning.py`, `day_proposal.py`, `focus_timer.py`, `task_references.py`, `interaction_policy.py`, `object_references.py`, `week_planning.py`, `page_features.py`, `repeat_rules.py`, `repeat_ics.py`, `routines.py`, `runtime_check.py`, `release_notes.py`, `appearance.py`, `preview_tools.py`, `filter_explain.py`, `exchange_patch.py`, `backup_diff.py`, `render_retention.py`, `logo_raster.py`, `symbol_policy.py`, `motion.py`, `task_editing.py`, `daily_hints.py`, `ics_recurrence.py`, `occupied_time.py`, `ics_busy.py`, `ics_timezone.py`, `timezones.py`, `day_relief.py`, `busy_calendar.py`, `calendar_service.py`, `animation.py`, `animation_export.py`, `attachment_paths.py`, `backup_snapshot.py`, `notion_archive.py`, `notion_hierarchy.py`, `notion_import.py`, `notion_reimport.py`, `page_restore.py`, `restore_assets.py`, `source_metadata.py`, `accessibility.py`, `accessibility_bindings.py`, `core_accessibility.py`, `glyph_metrics.py`, `exchange_recipes.py`, `markdown_tree.py`, `pinboard_pages.py`, `view_definition.py`, `undo_history.py`, `structural_guard.py`, `load_phases.py`, `editor_flush.py`, `data_lock.py`, `item_index.py`, `save_result.py`, `persistence.py`, `action_menu.py`, `side_view.py`, `compact_mode.py`, `storage_health.py`, `backup_catalog.py`, `attachment_policy.py`, `settings_compat.py`, `session_guard.py`, `runtime_diagnostics.py` – ohne sie startet Glide nicht;
- `Schnellstart.pyw` (im Repository `glide_start.py`);
- die Ordner `resources` (Schriften, Vorlagen, Logo, IANA-/CLDR-Zeitzonen samt Lizenzbelegen) und `vendor` (tkinterdnd2 für das Ziehen aus Finder und Explorer; fehlt er, startet Glide ohne diese Funktion), beide samt Lizenz- und Herkunftsnachweisen.

Verbindliche Modultabelle: [Architektur](../01_Repository/Glide/docs/02_ARCHITECTURE.md).

Abgleich und Prüfsummen: `scripts/pflege/abgleich_07.py` (SHA-256). Änderungen hier nur im Rahmen einer Produktionsrunde.

Mit Python 3.14 und Tk 9 starten; ein Python vor 3.12 oder ein Tk vor 8.6 weist Glide vor dem Öffnen von Daten ab. Mit Python 3.13/Tk 8.6 startet Glide ebenfalls, ohne Systemmitteilung und SVG-Vorschau; Logo und App-Symbole nutzen dort geglättete Bilder in exakter Zielgröße. Eine laufende ältere Instanz vorher schließen.

## Windows mit der geprüften Laufzeit starten

Aus der Wurzel `glide-to-do` in PowerShell:

```powershell
py -3.14 ".\07_Python-Versionen\Schnellstart.pyw"
```

Die native Windows-Prüfung und das eigenständige Paket verwenden Python 3.14.7 mit eigener Tcl/Tk-9.1-Laufzeit. Das Paket unter `01_Repository/Glide/build/windows/Glide-3.50.0/Glide.exe` benötigt keine externe Python-Installation. Der Python-Startweg oben bleibt zusätzlich verfügbar; für eine eigene geprüfte Laufzeit gilt die [Prüfliste, B0](../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md#b-windows-pc-nach-der-vollprüfung). Aktuelle Paketdateien und Quellhashes stehen im [Gesamtvalidierungsnachweis](../01_Repository/Glide/tests/qa-3.50.0/gesamtvalidierung_2026-11-02/README.md); ursprüngliche öffentliche Archive und spätere Kandidaten desselben Versionsnamens unterscheiden.

## Bytecode

Python legt den übersetzten Stand im Cacheordner des Systems ab, nie hier: macOS `~/Library/Caches/Glide/bytecode`, Windows `%LOCALAPPDATA%\Glide\Cache\bytecode`, Linux `~/.cache/glide/bytecode`. `Schnellstart.pyw` startet die versionierte Datei als Modul; ab dem zweiten Start öffnet Glide damit rund eine halbe Sekunde schneller.

## Datenformat und frühere Fassungen

Aufgabenformat 26 (seit 3.44.0) speichert die erweiterten Wiederholungsrhythmen samt Erledigungsbezug, Pause und Restanzahl; die frühere 3.43.1 verwendet Format 25. Vor der Umstellung entsteht die bytegleiche Vorsicherung `liste_vor_format26_<Zeitstempel>.json`; schlägt sie fehl, bleibt die alte Datei unverändert. Die unveränderte 3.43.1 (aus der Git-Historie) und die früheren, jetzt archivierten Pakete 3.42.0 öffnen Format 26 schreibgeschützt; die vorhandenen Pakete 3.50.0 sowie Quelle/Python 3.50.2 verarbeiten Format 26. Format 25 (seit 3.41.0) bewahrt Notion-Quellenzuordnungen an Seiten und Ordnern.

**Ältere Fassungen nie mit dem umgestellten Bestand starten.** Glide 3.29 hält ihn für beschädigt, beginnt leer und überschreibt ihn bei der ersten Eingabe. Zurück geht es nur mit der Vorsicherung in einer getrennten Ablage (`GLIDE_DATA_DIR`). Eine Fassung öffnet einen Bestand aus einer neueren Version nur schreibgeschützt.

[Archiv](Archiv/README.md) enthält frühere ausgelieferte Hauptdateien. Zusammen mit der aktuellen bleiben höchstens sieben Versionen erhalten; ältere Fassungen und Nachweise wurden nach der Aufbewahrungsregel gekürzt. Sie brauchen die Module dieses Ordners und starten nur, solange sich deren Schnittstellen nicht geändert haben; ältere Stände trägt Git.

Benachrichtigungen funktionieren nur bei laufender App. Was sich je Version geändert hat: [Änderungsverlauf](../01_Repository/Glide/CHANGELOG.md) · Prüfstand: [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md).
