# Prüfungen für Glide

Stand 23.10.2026 · Glide 3.44.0 · Aufgabenformat 26 · 102 Suiten aus `pruefen.py` und fünf Analysen

D55 (lokaler Kandidat auf 3.44.0): `test_arbeitsmodi.py` prüft zwölf Fälle über echte Tk-Wege – Seiten-, Block- und Notizaktionen mit Filter, Sperrgrund, Esc/Fokus und einem Undo; Blockgriff an Schreibmarke und Mauszeiger; Seitenkopf ohne Zusatzzeile; Nebenansicht mit Abhaken/Undo/Redo, Umbenennen, Papierkorb, Inspektorwechsel und schmalem Fenster; Kompaktmodus mit Kürzel, 480 × 560, getrennten Fensterlagen und Neustart; Knopfschutz B15 in fünf Gestaltungskonfigurationen. `--fall` wählt einzelne Fälle, `--capture ORDNER` speichert Sichtbelege lokal. Die 102 registrierten Suiten sind kein neuer Volllauf.

FP-02, beide Stufen: `test_wiederholungsregeln.py` ergänzt zwölf Fälle einschließlich Masken normal/groß, Formatmigration, Kopierfehler und Altleser. 30 unabhängige Referenzregeln mit 720 Folgeterminen; [aktueller Nachweis](qa-3.43.1/wiederholungsregeln_2026-10-21/README.md). Registriert heißt nicht neu vollständig gelaufen. Erledigungsbezug, Pause, Restanzahl, Chips und Kalender-Rundweg gehören jetzt zum selben Paket.

FP-03 Stufe 1: `test_ansichten.py` prüft neun Fälle einschließlich normaler/großer Schrift, Altleser, 30 alter Filterkombinationen, Schreibfehler und 10.000 Aufgaben. [Aktueller Nachweis](qa-3.43.1/ansichten_2026-10-21/README.md); 100 registriert bedeutet keinen neuen vollständigen 100-Suiten-Lauf.
Alle App-Tests setzen vor dem App-Import einen temporären `GLIDE_DATA_DIR`; echte Nutzerdaten sind ausgeschlossen. Was wann läuft, welche Regeln gelten und welche Suite welchen Bereich abdeckt, steht im [Prüfplan](../docs/05_QA_TESTPLAN.md); Ergebnisse im [QA-Bericht](../docs/07_QA_BERICHT.md).

## Aufrufe (aus `01_Repository/Glide`)

| Zweck | Aufruf |
|---|---|
| Vollprüfung (Referenz-Mac) | `python3 -B tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.44.0/<Name> --timeout 900` |
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
| `integration/` | 99 lokale Integrationssuiten; Liste in `SUITEN` von `tools/pruefen.py` |
| `unit/` | Unit-Tests der Tk-freien Fachmodule (D17) |
| `tools/` | Prüfstand, Analysen, Erzeuger für Beispiel-, Release-, Rundgang- und Showcase-Daten, CI-Grundstufe, Ablagegröße ([Übersicht](tools/README.md)) |
| `fixtures/` | Referenzformate 2 und 4–25, Beispiel- und Releasedaten, Rundgang, Showcase ([Übersicht](fixtures/README.md)) |
| `qa-<Version>/` | Nachweise der sieben neuesten Versionen: README, `ergebnis.json`, Quellstand, Lieferabgleich, Messwerte; Fensterbilder nur der drei neuesten; Rohprotokolle bleiben lokal und werden nicht versioniert |

Regeln für die Prüfumgebung (Zeitzone, Termine in Suiten, Hintergrundmodus, Last): [Prüfplan](../docs/05_QA_TESTPLAN.md#regeln).
