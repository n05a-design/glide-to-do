# Aktuelle startbare Python-Fassung

Glide 3.33.8 · Entwicklungsstand 05.10.2026 · Aufgabenformat 20 · Vorlagenformat 2

`Glide-Aufgaben-und-Listen_v3.33.8.pyw` (unter Windows mit Python 3.14.8/Tk 9.0.4 geprüft und am 05.10.2026 ausgeliefert; Referenz-Mac-Abnahme und Bundle stehen aus) ist die bytegleiche Arbeitskopie des kanonischen Codes (`01_Repository/Glide/src/glide/app.pyw`). Daneben gehören, ebenfalls bytegleich, in denselben Ordner:

- die Module `drawing.py`, `drawing_image.py`, `backdrop.py`, `page_markdown.py`, `image_preview.py`, `logo.py`, `schema_backups.py`, `sidebar_policy.py`, `svg_geometry.py`, `home_tiles.py`, `capture_parser.py`, `eisenhower.py`, `today_view.py`, `content_search.py` – ohne sie startet Glide nicht;
- `Schnellstart.pyw` (im Repository `glide_start.py`);
- die Ordner `resources` (Schriften, Vorlagen, Logo) und `vendor` (tkinterdnd2 für das Ziehen aus Finder und Explorer; fehlt er, startet Glide ohne diese Funktion), beide samt Lizenz- und Herkunftsnachweisen.

Verbindliche Modultabelle: [Architektur](../01_Repository/Glide/docs/02_ARCHITECTURE.md).

Abgleich und Prüfsummen: `scripts/pflege/abgleich_07.py` (SHA-256). Änderungen hier nur im Rahmen einer Produktionsrunde.

Mit Python 3.14 und Tk 9 starten. Mit Python 3.13 und Tk 8.6 startet Glide ebenfalls, nur ohne Systemmitteilung und SVG-Vorschau; das Logo erscheint dann als ungeglättete Fläche, Fenster- und Taskleistensymbol sind treppig ([Diagnose](../01_Repository/Glide/docs/diagnosen/LOGO_KANTENGLAETTUNG.md)). Eine laufende ältere Instanz vorher schließen.

## Windows mit der geprüften Laufzeit starten

Aus der Wurzel `glide-to-do` in PowerShell:

```powershell
& "$env:USERPROFILE\.cache\glide-qa\python-3.14.8\runtime\pythonw.exe" ".\07_Python-Versionen\Schnellstart.pyw"
```

Die separate Python-3.14.8-/Tk-9.0.4-Laufzeit ändert weder Standardinstallation noch Dateizuordnung; anlegen wie in der [Prüfliste, B0](../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md#b-windows-pc-nach-der-vollprüfung) beschrieben. Herkunft und Herstellerhash: [Prüflaufzeit](../01_Repository/Glide/tests/qa-3.33.8/windows_2026-10-05/prueflaufzeit.json).

## Bytecode

Python legt den übersetzten Stand im Cacheordner des Systems ab, nie hier: macOS `~/Library/Caches/Glide/bytecode`, Windows `%LOCALAPPDATA%\Glide\Cache\bytecode`, Linux `~/.cache/glide/bytecode`. `Schnellstart.pyw` startet die versionierte Datei als Modul; ab dem zweiten Start öffnet Glide damit rund eine halbe Sekunde schneller.

## Datenformat und frühere Fassungen

Aufgabenformat 20. Einen älteren Bestand stellt Glide beim Start um; vorher entsteht die unveränderte Sicherung `liste_vor_format20_<Zeitstempel>.json`.

**Ältere Fassungen nie mit dem umgestellten Bestand starten.** Glide 3.29 hält ihn für beschädigt, beginnt leer und überschreibt ihn bei der ersten Eingabe. Zurück geht es nur mit der Vorsicherung in einer getrennten Ablage (`GLIDE_DATA_DIR`). Eine Fassung öffnet einen Bestand aus einer neueren Version nur schreibgeschützt.

[Archiv](Archiv/README.md) enthält die Hauptdateien der früher ausgelieferten Versionen 3.33.2–3.33.6; 3.33.7 wurde nicht ausgeliefert. Zusammen mit der aktuellen bleiben höchstens sieben. Sie brauchen die Module dieses Ordners und starten nur, solange sich deren Schnittstellen nicht geändert haben; ältere Stände trägt Git.

Benachrichtigungen funktionieren nur bei laufender App. Was sich je Version geändert hat: [Änderungsverlauf](../01_Repository/Glide/CHANGELOG.md) · Prüfstand: [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md).
