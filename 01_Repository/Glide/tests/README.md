# Prüfungen für Glide

Stand 02.11.2026 · Glide 3.50.0 · Erster öffentlicher Stand · Aufgabenformat 26 · 108 Integrationssuiten und fünf Analysen

Die aktuelle vollständige Prüf- und Lieferbilanz steht im [QA-Bericht](../docs/07_QA_BERICHT.md) und im [Betanachweis](qa-3.50.0/oeffentliche_beta_2026-11-02/README.md). Historische Ergebnisse werden dort ihren tatsächlichen Quellständen zugeordnet, statt hier eine zweite Statusliste zu pflegen. Am 02.11.2026 gekürzt und zusammengeführt.

3.50 ergänzt Hintergrundfarben, volle Seitenleiste und Blockziehen. `test_arbeitsmodi.py` prüft insgesamt 39 Fälle; der neue Betafall deckt zehn Designs, alle Hintergrundoptionen, drei Größen, echte Aufgaben und Bildanhänge, Speicherung/Neustart, Undo/Redo, Abbruch und Schreibschutz ab. Der Knopfschutz prüft zusätzlich sieben Ansichten und fünf Dialoge.

D58: Commit/Push und verfügbare Hosted-Plattformprüfungen sind für den Abschluss autorisiert. Menschliche Prüfung anschließend. Screenreader-Abnahme einschließlich VoiceOver/NVDA/Orca ist bis Bedarf zurückgestellt; die optionalen Anleitungen unten bleiben erhalten. Keine Tests mit echten Nutzerdaten, Hardwareänderungen oder Eingriffe in persönliche Installationen.

## Aufrufe (aus `01_Repository/Glide`)

| Zweck | Aufruf |
|---|---|
| Vollprüfung (Referenz-Mac) | `python3 -B tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.50.0/<Name> --timeout 900` |
| Schnellprüfung | `python3 -B tests/tools/pruefen.py` |
| CI-Grundstufe (wie GitHub) | `python3 -B tests/tools/ci_grundstufe.py --protokoll <Ordner>` |
| Windows | `tests/tools/windows_vollpruefung.cmd` (Anleitung in der [manuellen Prüfliste](../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md)) |
| Windows, nebenher arbeiten | `tests/tools/windows_sandbox.cmd` bzw. `py -3.14 -B tests/tools/windows_sandbox.py --warten`: dieselbe Vollprüfung in der Windows-Sandbox, Fenster auf dem zweiten Bildschirm |
| Einzelsuite | `python3 -B tests/integration/<suite>.py`, unter macOS im Hintergrund mit `GLIDE_QA_HINTERGRUND=1 PYTHONPATH=tests/tools/hintergrund` |
| Fachlogik ohne Tk | `python3 -B -m unittest discover -s tests/unit -v` |
| Werkzeugtests | `python3 -B -m unittest discover -s tests/tools -p "test_*.py"` |
| Nur Stand und Links | `python3 -B tests/tools/standpruefung.py` |

Unter Windows die geprüfte Python-3.14-/Tk-9-Laufzeit oder `windows_vollpruefung.ps1 -PythonExecutable <Pfad>` verwenden; `--timeout 900` ist dort mit Virenschutz und synchronisiertem Ordner realistischer als die Vorgabe von 300 Sekunden je Suite. Kein `pytest`: Die Suiten sind ausführbare Skripte, die beim Import ein Tk-Fenster öffnen.

## Aufbau

| Ordner | Inhalt |
|---|---|
| `integration/` | 108 registrierte Integrationssuiten; Liste in `SUITEN` von `tools/pruefen.py` |
| `unit/` | Unit-Tests der Tk-freien Fachmodule (D17) |
| `tools/` | Prüfstand, Analysen, Erzeuger für Beispiel-, Release-, Rundgang- und Showcase-Daten, CI-Grundstufe, Ablagegröße ([Übersicht](tools/README.md)) |
| `fixtures/` | Referenzformate 2 und 4–26, Beispiel- und Releasedaten, Rundgang, Showcase ([Übersicht](fixtures/README.md)) |
| `qa-<Version>/` | Nachweise der sieben neuesten Versionen: README, `ergebnis.json`, Quellstand, Lieferabgleich, Messwerte; Fensterbilder nur der drei neuesten; Rohprotokolle bleiben lokal und werden nicht versioniert |

Regeln für die Prüfumgebung (Zeitzone, Termine in Suiten, Hintergrundmodus, Last): [Prüfplan](../docs/05_QA_TESTPLAN.md#regeln).

## Abschlussprüfung auf eigenen Geräten (Entscheidung 31.10.2026)

Der Auftrag vom 02.11.2026 ergänzt die ursprüngliche Entscheidung vom 31.10.: Technische Prüfungen und Paketbau werden auf verfügbaren nativen Geräten bzw. Hosted-Runnern abgeschlossen. Die menschliche Prüfung führt anschließend der Inhaber durch; Reader bleiben bis Bedarf zurückgestellt. Aktuelle Plattform-/Quellhashes und Lieferungen ausschließlich dem QA-Nachweis entnehmen.

**Windows-Vollprüfung:** PC-01/AMD bzw. einen stabilen Windows-x64-Prüfplatz verwenden; keine weitere Großlastserie auf dem instabilen PC-02/Intel. Im Projektordner `01_Repository/Glide` den bestehenden Starter ausführen:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tests\tools\windows_vollpruefung.ps1 -Arbeitsablage C:\gq
```

Der Starter wählt bevorzugt die lokale QA-Laufzeit 3.14.8, sonst `py -3.14`; `-PythonExecutable` kann die gewünschte reguläre x64-Laufzeit explizit setzen. Er prüft Online-Platzhalter, friert den vollständigen Stand mit eigener Git-Historie außerhalb OneDrive ein und isoliert alle Nutzdaten. Python-/Tk-Version, Quellhashes, `ergebnis.json`, `pruefablauf.json` und Rohlogs im ausgegebenen Prüfpfad erhalten. Kein getesteter Windows-Neubau entsteht allein durch die Vollprüfung.

**Linux-Vollprüfung:** Reguläres CPython 3.14 mit Headern sowie Xvfb/DBus und die [native Laufzeitvoraussetzungen](../packaging/runtime/README.md) verwenden. Aus `01_Repository/Glide`:

```sh
env -u DISPLAY dbus-run-session -- python3 -B tests/tools/gesichert_pruefen.py --art voll --timeout 900 --arbeitsablage "$HOME/gq"
```

Ohne DISPLAY verwendet `pruefen.py` Xvfb. Danach aus genau der ausgegebenen eingefrorenen Repositorykopie die kalibrierten Defektgegenproben ausführen; `<PROTOKOLL>` durch den dortigen Protokollordner ersetzen:

```sh
env -u DISPLAY dbus-run-session -- python3 -B tests/tools/linux_gegenproben.py --protokoll "<PROTOKOLL>/defektgegenproben" --basis-ergebnis "<PROTOKOLL>/ergebnis.json"
```

**Native P8-Matrix mit Tk 9.1:** Die eigene geprüfte Runtime vor der Prüfung über `PYTHONPATH=<Runtime>/python-extension` wählen. Ein Standardlauf mit Tk 8.6/9.0 ersetzt P8 nicht. Um bei Quelle 3.50.0 die native Tcl-/Kernprüfung im gesamten eingefrorenen Volllauf zu erzwingen, zuerst nur einfrieren (unter Windows `python`, unter Linux `python3`; Ablage gegebenenfalls `C:/gq`):

```sh
python3 -B -c "import sys; from pathlib import Path; sys.path.insert(0, 'tests/tools'); from pruefablauf import einfrieren; p,r=einfrieren(Path.cwd(), Path.home()/'gq'); print('Repository:',p); print('Nachweise:',r)"
```

In den ausgegebenen Repositorypfad wechseln. `PYTHONPATH` muss weiter auf die passende native Erweiterung zeigen; für jeden Lauf einen neuen Protokollordner verwenden:

```sh
python3 -B tests/tools/pruefen.py --modus voll --zugang-nativ --timeout 900 --arbeitsablage "$HOME/gq" --protokoll "$HOME/gq/native-neuer-lauf"
```

Unter Windows entsprechend `python` und kurze `C:/gq/...`-Pfade verwenden; unter Linux den oben gezeigten DBus-/DISPLAY-Präfix ergänzen. Die Runtime muss tatsächlich Tk 9.1 und den nativen Anbieter liefern, sonst ist das kein grüner P8-Nachweis.

**Optionale Readerprüfung (bis Bedarf zurückgestellt):** Nach der automatischen Prüfung auf dem realen Desktop den tatsächlich verwendeten VoiceOver/NVDA/Orca starten und die [manuelle Abschlussrunde](../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md#abschlussrunde-31102026--noch-menschlich-zu-bestätigen) durchführen. `tests/tools/reader_app400.py --app src/glide/app.pyw --diagnose <neuer-leerer-Ordner>` startet mit der gewählten Tk-9.1-Runtime eine eigene App mit ausschließlich synthetischen Daten; `bereit.json`, `zustand.json` und Callbackbefunde dokumentieren diese Instanz. Die reale Sprachausgabe und Bedienbeobachtung selbst protokollieren.

Die automatischen NVDA-/Orca-Profilhelfer sowie die Windows-ACL-Isolationsprobe sind absichtlich ausschließlich für vergängliche Hosted-Runner zugelassen. Auf eigenen Geräten keine Hosted-Umgebungsmarker vortäuschen und keine Inhaberinstallationen sperren. Manuelle Readerprüfung ist möglich; die gesonderte ACL-Isolationsabnahme bleibt mit dieser Geräteentscheidung offen. Ein normaler Paketstart wird nicht als ACL-Isolation bezeichnet.

Rückgabe: Plattform/Gerät, Python-/Tk-/Reader-Version, Apphash, eingefrorenes Quellmanifest, vollständiger Ergebnisordner und ausgefüllte menschliche Prüfliste. Bei Fehlern den ersten Befund mitsamt Kontext erhalten; keine Erfolgsauswahl aus Wiederholungen. Die Einordnung und Gesamtabnahme erfolgen erst anhand dieser tatsächlichen Ergebnisse.
