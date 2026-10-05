# Paketierung

Stand 05.10.2026 · Glide 3.33.8 laut VERSION · Aufgabenformat 20

Ein Paket enthält die Anwendung, alle Module aus der
[Architekturtabelle](../docs/02_ARCHITECTURE.md), Ressourcen und die passenden
tkdnd-Plattformbibliotheken samt Lizenzen. Die Zeichenprobe gehört nicht ins
Paket. Keine Nutzerdaten im Installationsordner.

| Werkzeug | Vorhandene Funktion |
|---|---|
| [baue_symbole.py](baue_symbole.py) | ICO und Plattform-PNGs aus resources/logo/glide-app-icon.svg; Master in 20_Grafik_Master/02_App-Icon |
| [macos/baue_app.py](macos/baue_app.py) | Lokales Glide.app mit installiertem Python und Ad-hoc-Signatur |
| [windows/verknuepfung_anlegen.ps1](windows/verknuepfung_anlegen.ps1) | Startmenü-Verknüpfung mit fester AppUserModelID |

Aus dem Quellbaum: `python -B packaging/baue_symbole.py` und
`python -B packaging/macos/baue_app.py --ziel build/macos`.
Bundlebau braucht macOS, Symbolrendering Tk 9. Das Entwicklungsbundle braucht
die installierte Laufzeit; Windows-Verknüpfung und echte Releaseverteilung
sind noch manuell abzuklären. Identitäten: [Produktregister](../docs/decisions/PRODUCT_IDENTITY.md).
Geprüfter Quell-/Lieferstand ist aktuell offen. Veröffentlichungsfreigaben
und Signierungsablauf stehen ausschließlich in der [Releasecheckliste](../docs/10_VEROEFFENTLICHUNG.md).

Mitgelieferter Code: `drawing.py`, `drawing_image.py`, `backdrop.py`, `page_markdown.py`, `image_preview.py`, `logo.py`, `glide_start.py`, `schema_backups.py`, `sidebar_policy.py`, `svg_geometry.py`, `home_tiles.py`, `capture_parser.py`, `eisenhower.py`, `today_view.py`, `content_search.py`.
