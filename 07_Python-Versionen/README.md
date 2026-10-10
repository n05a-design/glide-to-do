# Aktuelle startbare Python-Fassung

Glide 3.36.0 · Entwicklungsstand 10.10.2026 · Aufgabenformat 23 · Vorlagenformat 2

Geliefert wird `Glide-Aufgaben-und-Listen_v3.36.0.pyw`: gezielter Abgleich geänderter Bibliothekskarten und der Startseite, schnellerer erster und wiederholter Zugang zu Einstellungen. Aufgabenformat 23 unverändert. Eingefrorene Mac-Vollprüfung grün; 07, Showcase und Bundle werden mit SHA-256 abgeglichen. Native Linux-/Windows-Abnahme folgt am unveränderten Kandidatcommit. [Liefernachweis](../01_Repository/Glide/tests/qa-3.36.0/fundament_2026-10-10/README.md). In denselben Ordner gehören:

- die Module `drawing.py`, `drawing_image.py`, `backdrop.py`, `page_markdown.py`, `image_preview.py`, `logo.py`, `schema_backups.py`, `sidebar_policy.py`, `svg_geometry.py`, `home_tiles.py`, `capture_parser.py`, `eisenhower.py`, `today_view.py`, `content_search.py`, `save_comparison.py`, `view_metrics.py`, `action_catalog.py`, `ui_design.py`, `planning.py`, `day_proposal.py`, `focus_timer.py`, `task_references.py`, `interaction_policy.py`, `object_references.py`, `week_planning.py`, `page_features.py`, `repeat_rules.py`, `routines.py`, `runtime_check.py`, `release_notes.py`, `appearance.py`, `preview_tools.py`, `filter_explain.py`, `exchange_patch.py`, `backup_diff.py`, `render_retention.py` – ohne sie startet Glide nicht;
- `Schnellstart.pyw` (im Repository `glide_start.py`);
- die Ordner `resources` (Schriften, Vorlagen, Logo) und `vendor` (tkinterdnd2 für das Ziehen aus Finder und Explorer; fehlt er, startet Glide ohne diese Funktion), beide samt Lizenz- und Herkunftsnachweisen.

Verbindliche Modultabelle: [Architektur](../01_Repository/Glide/docs/02_ARCHITECTURE.md).

Abgleich und Prüfsummen: `scripts/pflege/abgleich_07.py` (SHA-256). Änderungen hier nur im Rahmen einer Produktionsrunde.

Mit Python 3.14 und Tk 9 starten; ein Python vor 3.12 oder ein Tk vor 8.6 weist Glide mit einer Meldung ab, bevor es Daten öffnet. Mit Python 3.13 und Tk 8.6 startet Glide ebenfalls, nur ohne Systemmitteilung und SVG-Vorschau; das Logo erscheint dann als ungeglättete Fläche, Fenster- und Taskleistensymbol sind treppig ([Diagnose](../01_Repository/Glide/docs/diagnosen/LOGO_KANTENGLAETTUNG.md)). Eine laufende ältere Instanz vorher schließen.

## Windows mit der geprüften Laufzeit starten

Aus der Wurzel `glide-to-do` in PowerShell:

```powershell
py -3.14 ".\07_Python-Versionen\Schnellstart.pyw"
```

Die aktuelle Windows-Prüfung nutzt die vorhandene Python-3.14.7-/Tk-9.0.4-Installation; der Launcher wählt sie ausdrücklich. Die separate Python-3.14.8-/Tk-9.0.4-Prüflaufzeit aus dem Nachweis der 3.33.8 ist in dieser Sitzung nicht vorhanden. Wer sie separat anlegen möchte, folgt der [Prüfliste, B0](../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md#b-windows-pc-nach-der-vollprüfung). Herkunft und Herstellerhash dieser optionalen Laufzeit: [Prüflaufzeit](https://github.com/n05a-design/glide-to-do/blob/254541aeae4577c0529d1ef768846a5c4546e59f/01_Repository/Glide/tests/qa-3.33.8/windows_2026-10-05/prueflaufzeit.json).

## Bytecode

Python legt den übersetzten Stand im Cacheordner des Systems ab, nie hier: macOS `~/Library/Caches/Glide/bytecode`, Windows `%LOCALAPPDATA%\Glide\Cache\bytecode`, Linux `~/.cache/glide/bytecode`. `Schnellstart.pyw` startet die versionierte Datei als Modul; ab dem zweiten Start öffnet Glide damit rund eine halbe Sekunde schneller.

## Datenformat und frühere Fassungen

Aufgabenformat 23 schützt Live-Listen und Titelbilder; die frühere 3.33.17 verwendet Format 22. Vor der Umstellung entsteht die bytegleiche Vorsicherung `liste_vor_format23_<Zeitstempel>.json`; schlägt sie fehl, bleibt die alte Datei unverändert. Die unveränderte 3.33.17 öffnet Format 23 nachweislich schreibgeschützt.

**Ältere Fassungen nie mit dem umgestellten Bestand starten.** Glide 3.29 hält ihn für beschädigt, beginnt leer und überschreibt ihn bei der ersten Eingabe. Zurück geht es nur mit der Vorsicherung in einer getrennten Ablage (`GLIDE_DATA_DIR`). Eine Fassung öffnet einen Bestand aus einer neueren Version nur schreibgeschützt.

[Archiv](Archiv/README.md) enthält frühere ausgelieferte Hauptdateien. Zusammen mit der aktuellen bleiben höchstens sieben Versionen erhalten; ältere Fassungen und Nachweise wurden nach der Aufbewahrungsregel gekürzt. Sie brauchen die Module dieses Ordners und starten nur, solange sich deren Schnittstellen nicht geändert haben; ältere Stände trägt Git.

Benachrichtigungen funktionieren nur bei laufender App. Was sich je Version geändert hat: [Änderungsverlauf](../01_Repository/Glide/CHANGELOG.md) · Prüfstand: [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md).
