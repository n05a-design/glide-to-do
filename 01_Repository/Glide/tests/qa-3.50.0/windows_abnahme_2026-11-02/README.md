# Windows-Abnahme auf PC-01: Tk-9.1-Volllauf und Paket 3.50.0

Stand 02.11.2026 · Glide 3.50.0 · Aufgabenformat 26 · PC-01 AMD Ryzen 7 5800X3D, Windows 11, Python 3.14.7 mit eigener Tcl/Tk 9.1.0 · künstliche Daten

**Auftrag 01.11.2026 (Inhaber):** Windows-Pakete und -Komponenten, Windows-Komplettprüfung und menschliche Prüfung nachholen, während auf dem MacBook noch Prüfungen laufen. Entscheidung: Prüfstand ist der neueste Mac-Stand nach seiner Übernahme, Paket mit eigener Tk 9.1 wie das Mac-Paket. Keine Lieferung nach `build/windows`, kein Versionswechsel; die menschliche Prüfung hat der Inhaber am 02.11. auf nach weiteren Änderungen verschoben.

## Werkzeugkette und eigene Tk-9.1-Laufzeit

Visual Studio 2022 Build Tools (C++) per winget installiert. Gepinnte Quellen nach [Runtime-Bauanleitung](../../../packaging/runtime/README.md#eigene-prüfgeräte--bau-und-auswahl-der-runtime): tcl `0c6bad08…`, tk `3f45110c…`, cpython `823f0323…` (3.14.7). [Baunachweis](runtime-bau.json): Tcl/Tk 9.1.0, `_tkinter` gegen Python 3.14.7, Windows-Patches `windows-accessibility-name`, `windows-accessibility-identity` und `common-accessibility-selection`, Backend MSAA; Probe lädt Tk 9.1.0 aus der eigenen Erweiterung ([Vorbereitung](runtime-vorbereitung.json)).

Erster Bauversuch rot an der vorhandenen Header-Sperre von `baue_runtime.py`: Die CPython-Quelle war mit LF exportiert, der python.org-Installer liefert `Include/patchlevel.h` mit CRLF (`9bf051c8…`). CPython legt keine Zeilenenden fest; nur diese Quellkopie wurde deshalb auf die Zeilenenden der Installation eingestellt und der Header vor dem Bau verglichen. Die Tk-Quellen erzwingen LF selbst, die Patch-Prüfsummen stimmen dafür (gegengeprüft). Keine Änderung an `baue_runtime.py` oder den Pins.

## Eingefrorener Volllauf

Frischer Klon von GitHub `main` `c24d2d42` (PR #48) außerhalb OneDrive, App `1582c600…` – derselbe Stand wie der Mac-Lauf `t1101-225816`. Klon mit `core.autocrlf=false`, `core.eol=lf`, `core.longpaths=true`, damit der Arbeitsbaum bytegleich zum Repository und zum Mac-Stand ist (App-Hash geprüft). Muster des Mac-Starters: `einfrieren`, `pruefen.py --modus voll --zugang-nativ --timeout 900` mit der eigenen Erweiterung.

**[Ergebnis](volllauf/ergebnis.json): 127 von 128 Schritten ausgeführt und grün, Exitcode 0** (00:13–01:16 Uhr). Darin Fachtests, alle Integrationssuiten, native Tcl-Zugangsbindungen ([Skript](volllauf/zugang-skript.json), [Kern](volllauf/zugang-kern.json)), Showcase, fünf Analysen, Beispiel- und Releasedaten-Abgleich und Windows-Aufnahme. Offen bleibt nur die Sichtprüfung der Fensterbilder durch eine Person. [Systemkontext](volllauf/systemkontext.json), [Abschluss](volllauf/abschluss.json), [Laufstatus](volllauf/status.json). Erster vollständig grüner Windows-Volllauf mit eigener Tk 9.1. Fensterbilder und Rohlogs bleiben lokal.

## Windows-Paket 3.50.0

Aus derselben eingefrorenen Kopie, venv mit `requirements/build-windows.txt`, `lizenzen_vorbereiten_windows.py` und `baue_paket.py --plattform windows-x64 --runtime-bau …`. Nach dem Merge von PR #49 (`a3506f3`, nur `setuptools` 84.0.0 → 84.1.0, App unverändert) neu gebaut; dieser Bau gilt:

- [Bau](paket/bau-ergebnis.json): 29 Lizenzkomponenten für Python 3.14.7 / Tcl 9.1.0, Quellvergleich, [PE-Nachprüfung](paket/pe-nachpruefung.json) Exitcode 0.
- [Startprobe](paket/start.json) des gebauten Pakets ohne Prüf-/Python-Umgebungsvariablen: Exitcode 0, App 3.50.0, Tcl/Tk 9.1.0, sechs Ansichten, Anlegen/Abhaken/Undo, Dateilesen, App-Sicherung im Rundlauf, Daten isoliert, 30 Ressourcen und 35 Lizenzdateien per SHA-256 bestätigt, tkdnd 2.10.2.
- `Glide.exe` SHA-256 `4d818e4e1cec3fe4935b60fa7dd8bb8499601611873ac8aa734a716d6998c835` ([Status](paket/status.json)); unsignierter Entwicklungsbau, lokal auf PC-01, nicht geliefert.

Der normale Paketstart ersetzt die Hosted-only-ACL-Isolationsprobe nicht.

## Werkzeuge

[`werkzeuge/`](werkzeuge/) enthält die verwendeten Starter: `vorbereiten.ps1` (Build Tools, gepinnte Quellen, Headerabgleich, Laufzeitbau, Probe) und `windows_abnahme.ps1` mit `voll_tk91.py`, `dateien_laden.py` und `belege.py` (optional frischer Klon von `main`, Volllauf, Paketbau, Startprobe, flache Belege nach `13_TK-Test-Umgebung/PC-01-AMD`). Aufruf auf PC-01 nach `C:\gq\…` kopiert:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File C:\gq\abnahme\windows_abnahme.ps1 -AusGitHub [-NurPaket] [-AppHash <Anfang>]
```

## Grenzen

- Menschliche Abnahme nach der [Prüfliste](../../../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md) offen, vom Inhaber verschoben; nach weiteren Codeänderungen Volllauf und Paket erneut.
- NVDA auf PC-01 nicht installiert; Readerkette Windows offen. Die übersprungenen Reader-Jobs der GitHub-Prüfung sind davon unabhängig.
- Keine Signatur, kein Installer, keine Lieferung nach `build/windows`; Windows-Lieferstand bleibt 3.45.0.
- WA-41A/B unberührt; PC-01 ist der stabile Prüfplatz.
