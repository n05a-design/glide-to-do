# Aktuelle startbare Python-Fassung

Stand 27.10.2026 · Glide 3.47.0 · Speicherstufe 26 · Vorlagenformat 2

**Liefergrenze:** Die Python-Fassung 3.47.0 enthält Mehrfachplanung und Nebenansichtsverlauf samt den vorherigen Tagessteuerungs-/Suchfunktionen. Eigenständige Windows-/Mac-Pakete bleiben separat bei 3.45.0. Gezielte Paketprüfung und strenger Lieferabgleich sind von vollständiger Endmatrix und menschlicher Abnahme getrennt. [Aktueller Prüf-/Liefernachweis](../01_Repository/Glide/tests/qa-3.47.0/folgepakete_2026-10-27/README.md).

Die startbare Python-Fassung `Glide-Aufgaben-und-Listen_v3.47.0.pyw` enthält den aktuellen Quellstand: Tagesaufgaben gemeinsam auswählen/planen und Inhalte im flüchtigen Nebenansichtsverlauf nachschlagen, einschließlich der früheren Startseiten-/Speicherverbesserungen. Aufgabenformat 26; 88 Code-Dateien und 147 Ressourcen-/Vendor-Dateien sind nach SHA-256 bytegleich zur eingefrorenen Quelle. Lieferprobe, endgültige Prüfergebnisse und offene Plattformtore stehen im [aktuellen Nachweis](../01_Repository/Glide/tests/qa-3.47.0/folgepakete_2026-10-27/README.md). In denselben Ordner gehören:

- die Module `drawing.py`, `drawing_image.py`, `backdrop.py`, `page_markdown.py`, `image_preview.py`, `image_conversion.py`, `logo.py`, `schema_backups.py`, `sidebar_policy.py`, `svg_geometry.py`, `home_tiles.py`, `home_dashboard.py`, `home_task_tiles.py`, `capture_parser.py`, `eisenhower.py`, `today_view.py`, `content_search.py`, `save_comparison.py`, `view_metrics.py`, `action_catalog.py`, `ui_design.py`, `planning.py`, `day_proposal.py`, `focus_timer.py`, `task_references.py`, `interaction_policy.py`, `object_references.py`, `week_planning.py`, `page_features.py`, `repeat_rules.py`, `repeat_ics.py`, `routines.py`, `runtime_check.py`, `release_notes.py`, `appearance.py`, `preview_tools.py`, `filter_explain.py`, `exchange_patch.py`, `backup_diff.py`, `render_retention.py`, `logo_raster.py`, `symbol_policy.py`, `motion.py`, `task_editing.py`, `daily_hints.py`, `ics_recurrence.py`, `occupied_time.py`, `ics_busy.py`, `ics_timezone.py`, `timezones.py`, `day_relief.py`, `busy_calendar.py`, `calendar_service.py`, `animation.py`, `animation_export.py`, `attachment_paths.py`, `backup_snapshot.py`, `notion_archive.py`, `notion_hierarchy.py`, `notion_import.py`, `notion_reimport.py`, `page_restore.py`, `restore_assets.py`, `source_metadata.py`, `accessibility.py`, `accessibility_bindings.py`, `core_accessibility.py`, `glyph_metrics.py`, `exchange_recipes.py`, `markdown_tree.py`, `pinboard_pages.py`, `view_definition.py`, `undo_history.py`, `structural_guard.py`, `load_phases.py`, `editor_flush.py`, `data_lock.py`, `item_index.py`, `save_result.py`, `persistence.py`, `action_menu.py`, `side_view.py`, `compact_mode.py`, `storage_health.py`, `backup_catalog.py`, `attachment_policy.py` – ohne sie startet Glide nicht;
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

Die native Windows-Prüfung und das eigenständige Paket verwenden Python 3.14.7/Tk 9.0.4. Das lokal bereitgestellte Paket unter `01_Repository/Glide/build/windows/Glide-3.45.0/Glide.exe` benötigt keine externe Python-Installation; der folgende Python-Startweg ist weiterhin zusätzlich verfügbar. Die separate Python-3.14.8-/Tk-9.0.4-Prüflaufzeit aus dem Nachweis der 3.33.8 ist in dieser Sitzung nicht vorhanden. Wer sie separat anlegen möchte, folgt der [Prüfliste, B0](../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md#b-windows-pc-nach-der-vollprüfung). Herkunft und Herstellerhash dieser optionalen Laufzeit: [Prüflaufzeit](https://github.com/n05a-design/glide-to-do/blob/254541aeae4577c0529d1ef768846a5c4546e59f/01_Repository/Glide/tests/qa-3.33.8/windows_2026-10-05/prueflaufzeit.json).

## Bytecode

Python legt den übersetzten Stand im Cacheordner des Systems ab, nie hier: macOS `~/Library/Caches/Glide/bytecode`, Windows `%LOCALAPPDATA%\Glide\Cache\bytecode`, Linux `~/.cache/glide/bytecode`. `Schnellstart.pyw` startet die versionierte Datei als Modul; ab dem zweiten Start öffnet Glide damit rund eine halbe Sekunde schneller.

## Datenformat und frühere Fassungen

Aufgabenformat 26 (seit 3.44.0) speichert die erweiterten Wiederholungsrhythmen samt Erledigungsbezug, Pause und Restanzahl; die frühere 3.43.1 verwendet Format 25. Vor der Umstellung entsteht die bytegleiche Vorsicherung `liste_vor_format26_<Zeitstempel>.json`; schlägt sie fehl, bleibt die alte Datei unverändert. Die unveränderte 3.43.1 (im Archiv) und die früheren, jetzt archivierten Pakete 3.42.0 öffnen Format 26 schreibgeschützt; die aktuellen Pakete 3.45.0 verarbeiten Format 26. Format 25 (seit 3.41.0) bewahrt Notion-Quellenzuordnungen an Seiten und Ordnern.

**Ältere Fassungen nie mit dem umgestellten Bestand starten.** Glide 3.29 hält ihn für beschädigt, beginnt leer und überschreibt ihn bei der ersten Eingabe. Zurück geht es nur mit der Vorsicherung in einer getrennten Ablage (`GLIDE_DATA_DIR`). Eine Fassung öffnet einen Bestand aus einer neueren Version nur schreibgeschützt.

[Archiv](Archiv/README.md) enthält frühere ausgelieferte Hauptdateien. Zusammen mit der aktuellen bleiben höchstens sieben Versionen erhalten; ältere Fassungen und Nachweise wurden nach der Aufbewahrungsregel gekürzt. Sie brauchen die Module dieses Ordners und starten nur, solange sich deren Schnittstellen nicht geändert haben; ältere Stände trägt Git.

Benachrichtigungen funktionieren nur bei laufender App. Was sich je Version geändert hat: [Änderungsverlauf](../01_Repository/Glide/CHANGELOG.md) · Prüfstand: [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md).
