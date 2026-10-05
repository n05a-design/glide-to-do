# Python-Lieferung

Stand 05.10.2026 · Glide 3.33.8 laut VERSION · Aufgabenformat 20

Dieser Ordner ist die startbare Lieferung des kanonischen Quellstands.
**3.33.8 ist hier ausgeliefert:** Hauptdatei, Schnellstart, vierzehn Module und 131 Ressourcen sind SHA-256-abgeglichen. Die Windows-Vollprüfung mit Python 3.14.8/Tk 9.0.4 ist grün. Schnellstart verwendet 3.33.8; die frühere Hauptdatei 3.33.6 liegt unverändert im Archiv. Nativer Mac-Bundlebau und Referenz-Mac-/manuelle Abnahme bleiben offen. Den Nachweis nennt der QA-Bericht.
Schnellstart und Module dürfen erst nach konsistentem Quell-/Versionsstand,
passender Prüfung und SHA-256-Abgleich als ausgeliefert gelten.
Details: [Projektübergabe](../01_Repository/Glide/docs/09_PROJECT_HANDOFF.md).

Verbindliche Modultabelle: [Architektur](../01_Repository/Glide/docs/02_ARCHITECTURE.md).
`Schnellstart.pyw` entspricht `src/glide/glide_start.py`; `resources` und
`vendor` sind benötigte Lieferkopien samt Lizenz-/Herkunftsnachweisen.
Abgleich über `scripts/pflege/abgleich_07.py`. Rückfallstände liegen gesammelt
in `07_Python-Versionen/Archiv`, höchstens sieben Versionen, ohne `_Z`.
Alte Fassungen nur mit getrenntem GLIDE_DATA_DIR starten.

Mitgelieferter Code: `drawing.py`, `drawing_image.py`, `backdrop.py`, `page_markdown.py`, `image_preview.py`, `logo.py`, `glide_start.py`, `schema_backups.py`, `sidebar_policy.py`, `svg_geometry.py`, `home_tiles.py`, `capture_parser.py`, `eisenhower.py`, `today_view.py`, `content_search.py`.

## Windows mit der geprüften Laufzeit starten

Aus der Wurzel `glide-to-do` in PowerShell:

```powershell
& "$env:USERPROFILE\.cache\glide-qa\python-3.14.8\runtime\pythonw.exe" ".\07_Python-Versionen\Schnellstart.pyw"
```

Der lokale QA-Cache enthält die separate Python-3.14.8-/Tk-9.0.4-Laufzeit. Die Standardinstallation und Dateizuordnung wurden nicht geändert. Außerhalb dieses Rechners Python 3.14 mit Tk 9 bereitstellen. Herkunft/Herstellerhash und Prüfergebnisse stehen im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md).
