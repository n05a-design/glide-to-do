# Prüfungen für Glide

Stand 10.10.2026 · Glide 3.36.0 · Aufgabenformat 23 · 83 Suiten aus `pruefen.py` und fünf Analysen

Alle App-Tests setzen vor dem App-Import einen temporären `GLIDE_DATA_DIR`; echte Nutzerdaten sind ausgeschlossen. Was wann läuft, welche Regeln gelten und welche Suite welchen Bereich abdeckt, steht im [Prüfplan](../docs/05_QA_TESTPLAN.md); Ergebnisse im [QA-Bericht](../docs/07_QA_BERICHT.md).

## Aufrufe (aus `01_Repository/Glide`)

| Zweck | Aufruf |
|---|---|
| Vollprüfung (Referenz-Mac) | `python3 -B tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.36.0/<Name> --timeout 900` |
| Schnellprüfung | `python3 -B tests/tools/pruefen.py` |
| CI-Grundstufe (wie GitHub) | `python3 -B tests/tools/ci_grundstufe.py --protokoll <Ordner>` |
| Windows | `tests/tools/windows_vollpruefung.cmd` (Anleitung in der [manuellen Prüfliste](../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md)) |
| Einzelsuite | `python3 -B tests/integration/<suite>.py`, unter macOS im Hintergrund mit `GLIDE_QA_HINTERGRUND=1 PYTHONPATH=tests/tools/hintergrund` |
| Fachlogik ohne Tk | `python3 -B -m unittest discover -s tests/unit -v` |
| Werkzeugtests | `python3 -B -m unittest discover -s tests/tools -p "test_*.py"` |
| Nur Stand und Links | `python3 -B tests/tools/standpruefung.py` |

Unter Windows die geprüfte Python-3.14-/Tk-9-Laufzeit oder `windows_vollpruefung.ps1 -PythonExecutable <Pfad>` verwenden; `--timeout 900` ist dort mit Virenschutz und synchronisiertem Ordner realistischer als die Vorgabe von 300 Sekunden je Suite. Kein `pytest`: Die Suiten sind ausführbare Skripte, die beim Import ein Tk-Fenster öffnen.

## Aufbau

| Ordner | Inhalt |
|---|---|
| `integration/` | 83 Integrationssuiten; Liste in `SUITEN` von `tools/pruefen.py` |
| `unit/` | Unit-Tests der Tk-freien Fachmodule (D17) |
| `tools/` | Prüfstand, Analysen, Erzeuger für Beispiel-, Release-, Rundgang- und Showcase-Daten, CI-Grundstufe, Ablagegröße ([Übersicht](tools/README.md)) |
| `fixtures/` | Referenzformate 2 und 4–23, Beispiel- und Releasedaten, Rundgang, Showcase ([Übersicht](fixtures/README.md)) |
| `qa-<Version>/` | Nachweise der sieben neuesten Versionen: README, `ergebnis.json`, Quellstand, Lieferabgleich, Messwerte; Fensterbilder nur der drei neuesten; Rohprotokolle bleiben lokal und werden nicht versioniert |

Regeln für die Prüfumgebung (Zeitzone, Termine in Suiten, Hintergrundmodus, Last): [Prüfplan](../docs/05_QA_TESTPLAN.md#regeln).
