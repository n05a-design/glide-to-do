# Python-Codebasis Glide 3.32.3

Einmalige unveränderte Laufzeitkopie vom 01.10.2026. Diese Ablage und `CLAUDE.md` werden künftig nicht gepflegt. Die beigefügte `CLAUDE.md` ist dieselbe kompakte Übergabe wie die separate Markdown-Datei.

Die acht Python-Dateien sowie `resources` und `vendor` müssen zusammenbleiben. `app.pyw` ist die kanonische Hauptdatei, `glide_start.py` der Schnellstarter. Die 139 Laufzeitdateien stimmen per SHA-256 mit dem geprüften Auslieferungsstand überein. Schriften, Vorlagen, Logo und die optionale Drag-and-drop-Bibliothek samt Lizenzen sind vollständig enthalten.

Start im entpackten Codeordner mit Python/Tk. Für eine getrennte Testablage unter macOS/Linux:

```sh
GLIDE_DATA_DIR="$PWD/Testdaten" python3 glide_start.py
```

Unter Windows in PowerShell:

```powershell
$env:GLIDE_DATA_DIR = Join-Path $PWD "Testdaten"
py -3 glide_start.py
```

Ohne `GLIDE_DATA_DIR` verwendet die App ihren normalen persönlichen Datenordner. In dieser Übergabe liegen keine echten Nutzerdaten. Eine Umgebung ohne Tk/Anzeige unterstützt keine GUI-Abnahme.

`Pruefnachweise` enthält vorhandene Ergebnis-/Hash-/Messdateien aus dem vollständigen Projekt. Deren ursprüngliche Repositorypfade sind historische Belegangaben. Tests und große Dokumentationsarchive sind nicht Bestandteil dieses kompakten Laufzeitpakets. Der bestehende Volltest wurde hier nicht erneut ausgeführt. Das Paket enthält keine Python-/Tk-Installation und keinen Installer.

`DATEIEN_SHA256.json` beschreibt die 139 Original-Laufzeitdateien; `SHA256SUMS.txt` prüft alle Paketdateien außer sich selbst. Syntax wurde ohne App-Import und ohne Zugriff auf Nutzerdaten geprüft.
