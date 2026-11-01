# Prüfungen für Glide

Stand 31.10.2026 · Glide 3.50.0 · Aufgabenformat 26 · 108 Suiten aus `pruefen.py` und fünf Analysen

**Mutationsabschluss 31.10.2026:** 56 Fälle einschließlich frischer Gruppendialoge, direkter Anlege-/Feld-/Labelwege, aktuellem Schreibbesitz, vollem Undo-Stapel und CSV-/ICS-Rollback/Nachlauf. Fehlerinjektion weist Sperrdateierneuerung und anschließenden Hauptdateifehler getrennt nach. CI-Folgestopp mit echten roten Kindprozessen geprüft. [Prüf- und Liefernachweis](qa-3.49.0/gesamtabschluss_2026-10-31/README.md).

**Aktueller Gesamtprüfstand 31.10.2026:** Native Mac-Tk-9.1-Matrix `t1031-164116`: 126 Schritte grün, einschließlich aller 108 Integrationssuiten, Showcase, fünf Analysen und Reproduktionen. Programm-, Test- und Ressourcenstand bytegleich, spätere Anleitungspflege gesondert geprüft. 1.082 Fachtests (ein Skip); neue Grundstufe zusätzlich 235 Werkzeugtests (drei Skips), Fachtests auch ohne Systemzeitzonen. Quelle/Python/Showcase/macOS 3.49.0; Windows-Lieferung und aktuelle Windows-/Linux-Endmatrix sowie echte Reader-/Menschenabnahme bleiben getrennt offen. [Prüf- und Liefernachweis](qa-3.49.0/gesamtabschluss_2026-10-31/README.md).

**Neuester Bereichsnachlauf:** „Liste leeren“ mit 7 neuen Fällen plus 17 Mutations- und 16 Schutzfällen auf `39499ab3…` grün, Quellen/Prüfkopie unverändert. Apple-Silicon-/Rosetta-Profil ergänzt: 231 Werkzeugtests grün (ein Skip), einschließlich Apple-Profil und Zählvertrag, Darwin-Zweig simuliert. Neuer Lauf ist ein Bereichsbeleg. Vorheriger Mutationsschnitt: `test_mutationsreste.py` mit 17 Fällen plus Schutzrunde 16/16 grün; sechs reine Entnahme-/Label-/Retentionsfälle und vier Wächterinventarfälle neu. Intel-CI am Mutationsstand rot: erster Fachlauf 1.074 grün, zweiter ohne Systemzeitzonen nativer Abbruch `0xC0000409` / „Executing a cache“. Originalbelege gesichert; keine neue grüne Vollprüfung. [Belege](qa-3.49.0/abschlussreste_2026-10-29/README.md). Frühere CI-/Fallzahlen unten bleiben ihren Quellständen zugeordnet.

**Robustheit 3.49.0:** `tests/unit/test_session_guard.py`, `tests/unit/test_runtime_diagnostics.py`, `tests/tools/test_pruefablauf.py` und `tests/integration/test_wiederanlauf.py` prüfen die neuen Grenzen mit künstlichen Daten. Breite Last-/Vollprüfung und native Abnahme bleiben getrennt. [Tatsächlicher Stand](qa-3.49.0/robustheit_2026-10-28/README.md).

**Datierter Bereichsnachlauf 29.10.2026:** [Abschlussnachlauf](qa-3.49.0/abschlussreste_2026-10-29/README.md): ursprüngliche A01-Pflichtfolge nach dokumentierten Adapter-/Prüfplatzkorrekturen in 13 Suiten/136 Fällen grün. Danach WA-09 mit fünf neuen Appfällen und 21 Ansichts-/Seitenkartenregressionen grün; 1.064 Fachtests und 224 Werkzeugtests (ein Skip) grün. `test_zukunftsfelder.py` ist in der Vollmatrix registriert. Die nun 108 registrierten Suiten sind kein neuer bestandener Volllauf; die folgende grüne CI gehört zum früheren WA-09-Stand. Historischer [Abnahmebericht](qa-3.49.0/abnahme_2026-10-28/README.md) und seine Rotbelege bleiben unverändert. Neue eingefrorene CI-Grundstufe grün: 19 Schritte, 18 ausgeführt und der zulässige Lieferhinweis; zweimal 1.064 Fachtests. Abschließende Statusmeldungen danach separat auf Stand/Links geprüft. Python/Showcase 3.47.0, native Pakete 3.45.0.

Startseitenmodell WA-39/WA-36 (26.10.2026): zwölf Fachfälle in `test_home_dashboard.py`; `test_startseite3332.py` ergänzt Archiv-/Datums-/Gleichstandsprüfung, genau einen Modellaufbau für die Bestandskacheln, echte Erledigen-/Undo-Aktion, aktuelle Objektauflösung und Renderfehler. Bestehende Standard-/Anpassungs-/Designprüfungen bleiben. [Nachweis und Leistung](qa-3.45.0/startseitenmodell_2026-10-26/README.md). Keine zusätzliche Suite und kein neuer Volllauf.

WA-40/WA-56 (lokaler Kandidat 25.10.2026): `test_speicherstatus.py` prüft vier echte Bereiche – Autosave-Fehler/Retry-Dialog, getrennte Nebenwege, geschützte Größenüberschreitungen und Reserve/Importabbruch. `storage_health.py` hat acht Tk-freie Tests; Formatvorsicherungen bleiben bytegenau und parse-zwischengespeichert. [Paketnachweis](qa-3.44.0/speicherstatus_2026-10-25/README.md).

D55 (historischer Einführungsnachweis mit 13 Fällen; seit 3.45.0 geliefert): `test_arbeitsmodi.py` prüft 13 Fälle über echte Tk-Wege – Seiten-, Block- und Notizaktionen mit Filter, Sperrgrund, Esc/Fokus und einem Undo; Blockgriff an Schreibmarke und Mauszeiger; Seitenkopf ohne Zusatzzeile; Nebenansicht mit Abhaken/Undo/Redo, Umbenennen, Papierkorb, Inspektorwechsel und schmalem Fenster; Rechtsklick in allen Seitenleistenbereichen ohne Öffnen des Hauptinhalts, mit weiter wirksamem Linksklick, Tastaturnavigation und Mehrfachauswahl; Kompaktmodus als erster Befehl im Menü „Ansicht“, mit Kürzel einschließlich KeyRelease-Ersatzweg, 480 × 560, getrennten Fensterlagen und Neustart; Knopfschutz B15 in fünf Gestaltungskonfigurationen. Im Kontextmenüfall wird nur die native Menüdarstellung ersetzt, die echten Mausbindungen und zeitversetzten Auswahlereignisse laufen weiter. `--fall` wählt einzelne Fälle, `--capture ORDNER` speichert Sichtbelege lokal. Die 103 registrierten Suiten sind kein neuer Volllauf.

FP-02, beide Stufen: `test_wiederholungsregeln.py` ergänzt zwölf Fälle einschließlich Masken normal/groß, Formatmigration, Kopierfehler und Altleser. 30 unabhängige Referenzregeln mit 720 Folgeterminen; [aktueller Nachweis](https://github.com/n05a-design/glide-to-do/blob/2b1ee0fedc32acb3ae1feff26d8848c26a457be6/01_Repository/Glide/tests/qa-3.43.1/wiederholungsregeln_2026-10-21/README.md). Registriert heißt nicht neu vollständig gelaufen. Erledigungsbezug, Pause, Restanzahl, Chips und Kalender-Rundweg gehören jetzt zum selben Paket.

FP-03, beide Stufen: `test_ansichten.py` enthält 15 Appfälle einschließlich normaler/großer Schrift, Altleser, 30 alter Filterkombinationen, Schreibfehler, 10.000 Aufgaben sowie gespeicherter Darstellung, Spaltenbreiten und Gruppierungswechsel. [Einführungsnachweis Stufe 1 mit neun Fällen](https://github.com/n05a-design/glide-to-do/blob/2b1ee0fedc32acb3ae1feff26d8848c26a457be6/01_Repository/Glide/tests/qa-3.43.1/ansichten_2026-10-21/README.md), [gemeinsamer Stufe-2-Phasenabschluss 3.44.0](qa-3.44.0/phasenabschluss_2026-10-22/README.md); der aktuelle Gesamtprüfstand bleibt im QA-Bericht getrennt.
Alle App-Tests setzen vor dem App-Import einen temporären `GLIDE_DATA_DIR`; echte Nutzerdaten sind ausgeschlossen. Was wann läuft, welche Regeln gelten und welche Suite welchen Bereich abdeckt, steht im [Prüfplan](../docs/05_QA_TESTPLAN.md); Ergebnisse im [QA-Bericht](../docs/07_QA_BERICHT.md).

Die neue Pflichtsuite `test_sicherungszentrale.py` prüft Übersicht/Filter, externe und defekte Dateien, Auswahlvergleich mit gleichen Dateinamen, Wiederherstellungsabbruch, Anhangsrückfrage sowie kleine Dialoge/große Schrift. Die registrierte Suitezahl ist kein bestandener Volllauf.

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

Der Inhaber führt Windows-/Linux-/Readerprüfungen und menschliche Abnahmen selbst aus; kein Git-Push oder Hosted-Workflow beauftragt. Ausgangs-App 3.49.0: SHA-256 `1fabf883d14ff7bb576803b90ac565fc18d5fcf32b79a53a9f8ce036de7bbbeb`. Quell-/Test-/Fixture-/Ressourcenhashes und [Plattformmatrix](qa-3.49.0/gesamtabschluss_2026-10-31/plattformmatrix.json) zum Ergebnis mitgeben. `07_Python-Versionen` und die geprüfte Mac-App tragen bereits diesen Stand. Andere Sitzungen während des Einfrierens nicht ändern lassen; nach rotem Schritt stoppen, Befund erhalten.

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

**Native P8-Matrix mit Tk 9.1:** Die eigene geprüfte Runtime vor der Prüfung über `PYTHONPATH=<Runtime>/python-extension` wählen. Ein Standardlauf mit Tk 8.6/9.0 ersetzt P8 nicht. Um bei Quelle 3.49.0 die native Tcl-/Kernprüfung im gesamten eingefrorenen Volllauf zu erzwingen, zuerst nur einfrieren (unter Windows `python`, unter Linux `python3`; Ablage gegebenenfalls `C:/gq`):

```sh
python3 -B -c "import sys; from pathlib import Path; sys.path.insert(0, 'tests/tools'); from pruefablauf import einfrieren; p,r=einfrieren(Path.cwd(), Path.home()/'gq'); print('Repository:',p); print('Nachweise:',r)"
```

In den ausgegebenen Repositorypfad wechseln. `PYTHONPATH` muss weiter auf die passende native Erweiterung zeigen; für jeden Lauf einen neuen Protokollordner verwenden:

```sh
python3 -B tests/tools/pruefen.py --modus voll --zugang-nativ --timeout 900 --arbeitsablage "$HOME/gq" --protokoll "$HOME/gq/native-neuer-lauf"
```

Unter Windows entsprechend `python` und kurze `C:/gq/...`-Pfade verwenden; unter Linux den oben gezeigten DBus-/DISPLAY-Präfix ergänzen. Die Runtime muss tatsächlich Tk 9.1 und den nativen Anbieter liefern, sonst ist das kein grüner P8-Nachweis.

**Reader und menschliche Bedienung:** Nach der automatischen Prüfung auf dem realen Desktop den tatsächlich verwendeten VoiceOver/NVDA/Orca starten und die [manuelle Abschlussrunde](../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md#abschlussrunde-31102026--noch-menschlich-zu-bestätigen) durchführen. `tests/tools/reader_app400.py --app src/glide/app.pyw --diagnose <neuer-leerer-Ordner>` startet mit der gewählten Tk-9.1-Runtime eine eigene App mit ausschließlich synthetischen Daten; `bereit.json`, `zustand.json` und Callbackbefunde dokumentieren diese Instanz. Die reale Sprachausgabe und Bedienbeobachtung selbst protokollieren.

Die automatischen NVDA-/Orca-Profilhelfer sowie die Windows-ACL-Isolationsprobe sind absichtlich ausschließlich für vergängliche Hosted-Runner zugelassen. Auf eigenen Geräten keine Hosted-Umgebungsmarker vortäuschen und keine Inhaberinstallationen sperren. Manuelle Readerprüfung ist möglich; die gesonderte ACL-Isolationsabnahme bleibt mit dieser Geräteentscheidung offen. Ein normaler Paketstart wird nicht als ACL-Isolation bezeichnet.

Rückgabe: Plattform/Gerät, Python-/Tk-/Reader-Version, Apphash, eingefrorenes Quellmanifest, vollständiger Ergebnisordner und ausgefüllte menschliche Prüfliste. Bei Fehlern den ersten Befund mitsamt Kontext erhalten; keine Erfolgsauswahl aus Wiederholungen. Die Einordnung und Gesamtabnahme erfolgen erst anhand dieser tatsächlichen Ergebnisse.
