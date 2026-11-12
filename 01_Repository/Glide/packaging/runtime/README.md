# Eigene Tcl/Tk-9.1-Runtime

Stand 12.11.2026 · Glide 3.55.1 · eigene Tcl/Tk 9.1 · Reader bis Bedarf zurückgestellt

`baue_runtime.py` exportiert saubere Git-Originale aus den Pins in `runtime_contract.py` und baut Tcl, Tk und die dazu passende CPython-3.14-Erweiterung `_tkinter` in einem neuen Ziel außerhalb von OneDrive. Installierte Python-Header und Quellheader müssen bis auf die Zeilenenden bytegleich sein (der python.org-Installer für Windows liefert CRLF, der Git-Export LF). Native Ziele: macOS arm64, Windows x64 mit MSVC, Linux x64 mit verpflichtendem ATK/AT-SPI. Es gibt keine Systeminstallation.

`runtime_patches.py` wendet ausschließlich die in `patches.json` dokumentierten Korrekturen auf die exportierte Baukopie an. Quellpin, Originalbytes, Diffbytes und Ergebnisbytes müssen passen. Originalquellen bleiben unverändert. Die Mac-Korrektur betrifft bestätigte native Verträge bei Aktionswarteschlange, deaktivierten Inhalten, Fokus, Verfügbarkeit, Kennungen, Hilfe und Aufgabengruppen. Jede vorgemerkte Aktion besitzt Interpreter und Kommandodaten; entfernte, versteckte, deaktivierte oder ersetzte Ziele werden verworfen. Interpreterlöschung entfernt ausstehende Aktionen.

`hole_runtimequellen.py` lädt die offiziellen festen Git-Pins ausschließlich in ein neues Hosted-CI-Ziel unter `RUNNER_TEMP`. Der vorhandene Workflow `Glide-Prüfung` mit manuellem Bereich `zugang400` baut Linux und anschließend Windows; Linux prüft die reale externe AT-SPI-Textschnittstelle, Windows den Aufgaben-Kernablauf und danach tatsächliche NVDA-Sprache mit isoliertem Profil. Die nativen Vollprüfungen je Lieferung bleiben zusätzlich erforderlich.

Mac-Runtime4: zwölf native Anbieterfälle, vier installierte Tcl-Fälle, zehn GUI-Gruppen und isolierter privater Paket-Kernablauf grün. Neunter Linux-Lauf: Unicode/Caret, ACTIVE und deaktivierte Zustände sowie Tcl/GUI grün. Orca spricht Erfassung/Suche, meldet beim Wechsel jedoch fälschlich fokussierte Container; vollständiger Ablauf offen. Windows-Signaturgegenprobe und isolierter Paketprozess/Kernablauf im neunten Lauf grün; Gesamtnachweis wegen zweier abweichend restaurierter geschützter CI-Dateien rot. NVDA erreicht Heute, danach unknown; vollständiger Ablauf offen. [Nachweise und rote Vorläufe](https://github.com/n05a-design/glide-to-do/blob/2b1ee0fedc32acb3ae1feff26d8848c26a457be6/01_Repository/Glide/tests/qa-3.42.0/zugang400_vorbereitung_2026-10-14/README.md).

| Patch | Zweck |
|---|---|
| macos-accessibility-core | Native Aqua-Verträge für Namen/Werte, Kennungen, Hilfe, Fokus, Zustände und abgesicherte Aktionslebensdauer |
| common-accessibility-selection | Frühe Auswahl vor Map, entfernte Widgets und Bäume ohne Zusatzspalten ohne Tcl-Callbackfehler |
| linux-accessibility-text | Aktueller Text, Unicode-Zeichenoffsets, Zeichenzahl und Caret über AtkText |
| linux-accessibility-window | ACTIVE am gemappten Fenster mit tatsächlichem Tk-Eingabefokus |
| linux-accessibility-state | ENABLED/SENSITIVE/EDITABLE aus disabled/readonly; deaktivierter Text bleibt lesbar |
| linux-accessibility-focus | Virtuelle Vorfahrenereignisse sind kein Eingabefokus; Fokuswechsel sind keine neuen Kinder. Nach Orca-Befund vorbereitet, native Wiederholung offen |
| linux-accessibility-lifetime | Typgerechte native Callbackdaten, GObject-Referenzlebensdauer und DEFUNCT nach tatsächlichem SIG11; externer Lebensdauertest offen |
| windows-accessibility-name | get_accName liest den Namen; Beschreibung bleibt separat |
| windows-accessibility-identity | Stabile MSAA-Kindkennungen, Widget-/Root-Lebensdauer und gültige Fokus-Tabelle nach NVDA-unknown; COM-Gegenprobe offen |

Mac baut mit `--disable-framework --disable-zipfs --enable-aqua=yes`: getrennte Tcl-/Tk-Skriptdaten vermeiden den belegten PyInstaller-/Mach-O-Konflikt angehängter Archive. Windows erhält `manifest.uuid` aus Originalpräfix und verifiziertem Pin. `_tkinter` verwendet `TCL_WITH_EXTERNAL_TOMMATH` und `tommath.lib`; Tcl/Tk, zlib und TomMath liegen neben der eigenen pyd. Linux benötigt HarfBuzz sowie ATK/Bridge/X11.

Patchprozesse erzwingen LF lokal und verändern keine globale Git-Konfiguration. Elf Runtimeverträge samt tatsächlichem Git-Gegenfall sind grün. Plattformgemeinsame Patches gehören zur verpflichtenden Runtimeherkunft. `baue_paket.py --runtime-bau <runtime-bau.json>` verlangt Interpreter, Pins, Patchsatz und vollständige unveränderte Runtime-Dateihashes. Lizenzwerkzeuge verwenden Originalbelege einschließlich utf8proc; Reader-Testhelfer werden niemals mitpaketiert.

Standard-Vollmatrix und Windows-Paketjob sind auf eigene 9.1-Runtimes vorbereitet, Python-Pins Linux 3.14.8 / Windows 3.14.7. Der damalige P8-Prüfstand enthielt 92 Integrationssuiten; die damalige 3.50.0-Matrix umfasste 108. Aktuelle Läufe stehen commitbezogen im [QA-Bericht](../../docs/07_QA_BERICHT.md#plattformprüfung-und-pakete-auf-main-12112026). `--zugang-nativ` erzwingt die native Kernprüfung in der Vorstufe; ab Version 4 ist sie ohne Option Pflicht. Native Tcl-Bindungen gehören dazu. Linux-Defektgegenproben bleiben erhalten. Gezielter Mac-Hintergrundpfad und drei Versionsvertragsfälle grün; aktuelle Ergebnisse aller drei Plattformen stehen im [3.50-Nachweis](https://github.com/n05a-design/glide-to-do/blob/13bcb66a7ba2007c3d8828ba1e0e082cb8918c91/01_Repository/Glide/tests/qa-3.50.0/oeffentliche_beta_2026-11-02/README.md).

D58 (02.11.2026) stellt die Reader-Abnahme bis Bedarf zurück. Wird sie später aktiviert, bleiben vollständige tatsächliche VoiceOver-/NVDA-/Orca-Abläufe nach D36 Pflichtnachweise. Attribute, künstlich gesetzter Readerstatus im eigenen Tcl-Interpreter und direkte Tk-/spd-say-Ausgabe zählen dafür nicht. Menschen-/DPI-Abnahme nach D42 bleibt zusätzlich getrennt. Die hier genannten P8-Prototypen tragen historisch Basisversion 3.42.0. Der erste öffentliche Stand ist 3.50.0 auf Python/Showcase und beiden eigenständigen Paketen; tatsächliche Artefakte und Prüfungen im [aktuellen Liefernachweis](https://github.com/n05a-design/glide-to-do/blob/13bcb66a7ba2007c3d8828ba1e0e082cb8918c91/01_Repository/Glide/tests/qa-3.50.0/oeffentliche_beta_2026-11-02/README.md). Mac Ad-hoc-signiert, Windows unsigniert; öffentliche Signatur und Notarisierung sind gesonderte Vertriebsentscheidungen.

Letzter hier dokumentierter nativer Nachlauf vom 14.10.2026: [Native10](https://github.com/n05a-design/glide-to-do/blob/2b1ee0fedc32acb3ae1feff26d8848c26a457be6/01_Repository/Glide/tests/qa-3.42.0/zugang400_vorbereitung_2026-10-14/native_vorlauf10.json), exklusiver Linux-Fokus grün, danach Orca-SIG11; Linux-Lebensdauer und native Probe vorbereitet. NVDA-Heute-Fokus repariert, weitere Readernavigation/MSAA-Prüfer und Reparse-ACL korrigiert; Native11 offen. Kein4.0-Liefernachweis.

## Eigene Prüfgeräte – Bau und Auswahl der Runtime

Die technischen Prüfungen verwenden den nativen Mac und die nativen Linux-/Windows-Runner; der Inhaber übernimmt anschließend die menschliche Prüfung auf seinen Geräten (Auftrag 02.11.2026). Readerabläufe sind bis Bedarf zurückgestellt. [Aktuelle Matrix und Pakete](https://github.com/n05a-design/glide-to-do/blob/13bcb66a7ba2007c3d8828ba1e0e082cb8918c91/01_Repository/Glide/tests/qa-3.50.0/oeffentliche_beta_2026-11-02/README.md).

Benötigt werden reguläres CPython 3.14.5, 3.14.7 oder 3.14.8 einschließlich unveränderter Header, Git und die native Bauumgebung. Windows x64: MSVC-x64-Entwicklungsumgebung/SDK bereits in dieser Konsole aktiv. Linux x64: C-Bauwerkzeuge/pkg-config, X11/Xft/Xss, HarfBuzz sowie ATK/AT-SPI-Bridge; für die Matrix zusätzlich DBus/Xvfb. `baue_runtime.py` installiert nichts systemweit und lehnt unpassende ABI, Quellpins, Header, Plattform und Zielpfade ab.

Die drei sauberen lokalen Git-Quellen müssen exakt zu `runtime_contract.py` passen. Pins aus der gewählten Python-Laufzeit anzeigen (unter Windows `python`):

```sh
python3 -B -c "import sys,platform,json; sys.path.insert(0,'packaging/runtime'); from runtime_contract import PINS,PYTHON_PINS; print(json.dumps(dict(PINS,python=PYTHON_PINS[platform.python_version()]),indent=2))"
```

Je Quelle einen neuen leeren Ordner außerhalb OneDrive anlegen, dort `git init`, `git fetch --depth=1 <offizielles-Repository> <angezeigter-Pin>` und `git checkout --detach FETCH_HEAD` ausführen. Offizielle Repositories: `https://github.com/tcltk/tcl.git`, `https://github.com/tcltk/tk.git`, `https://github.com/python/cpython.git`. Danach sind die Quellen `tcl`, `tk`, `python` unverändert zu halten; der Baumeister exportiert und patcht ausschließlich seine eigene Kopie. `hole_runtimequellen.py` ist der Hosted-CI-Abrufhelfer und wird auf persönlichen Geräten nicht verwendet.

Beispiel Linux, aus dem Repository (Windows: `python`, Pfade etwa `C:/gq/quellen91/...` und `C:/gq/runtime91`):

```sh
python3 -B packaging/runtime/baue_runtime.py --tcl-quelle "$HOME/gq/quellen91/tcl" --tk-quelle "$HOME/gq/quellen91/tk" --python-quelle "$HOME/gq/quellen91/python" --ziel "$HOME/gq/runtime91"
```

Das Ziel muss neu/leer sein. `runtime-bau.json`, komplette Bauprotokolle und Pins erhalten. Danach nur für diesen Konsolenprozess `PYTHONPATH` setzen:

```powershell
$env:PYTHONPATH = 'C:\gq\runtime91\python-extension'
python -B -c "import tkinter as t; r=t.Tk(); print(r.tk.call('package','provide','Tk')); r.destroy()"
```

```sh
export PYTHONPATH="$HOME/gq/runtime91/python-extension"
python3 -B -c "import tkinter as t; r=t.Tk(); print(r.tk.call('package','provide','Tk')); r.destroy()"
```

Erwartet ist tatsächlich `9.1.0`. Für Matrix/Reader die [Prüfaufrufe auf eigenen Geräten](../../tests/README.md#abschlussprüfung-auf-eigenen-geräten-entscheidung-31102026) verwenden. Normaler Appbetrieb erzeugt eine Tk-Instanz je Prozess; keine spekulativen Fontcaches ergänzen. Echte Reader-Sprachausgabe und Menschenabnahme bleiben eigenständige Nachweise.
