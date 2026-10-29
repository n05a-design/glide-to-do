# WA-41: Wiederholung auf dem AMD-PC

Stand 27.10.2026 · Glide 3.48.0 · Aufgabenformat 26

Auftrag: die auf PC 2 mit Intel-CPU auffälligen Prüfungen auf dem aktuellen AMD-PC wiederholen. Keine Produktionsänderung, Änderung der CPU-/BIOS-Einstellungen, Lieferung oder Gitaktion.

## Ergebnis

**Abgeschlossen: zehn von zehn ausgewerteten Prüfprozessen grün.** Neun unter Python 3.14.7, einer zusätzlich unter 3.15.1. Keine unerwarteten Interpreterabbrüche, Typfehler oder Abweichungen zwischen gespeichertem und geladenem Bestand. Nach jedem Prozess und abschließend alle 470 Dateien der Prüfkopie unverändert. [Geprüfte Gesamtbilanz](auswertung.json), [acht geplante Prozesse](fester_pruefordner/ergebnis.json), [zwei Zusatzproben mit Intel-Originalbytes](originalbestand/ergebnis.json).

| Prüfung | Laufzeit | Ergebnis | Dauer |
|---|---|---|---|
| Kernprobe 1, 26.420 Punkte / 40 Runden | 3.14.7 | grün | 149,96 s |
| Originalvollsuite 1 | 3.14.7 | grün | 221,33 s |
| Reiner Datenkern, 20 Runden ohne Appimport/Tk | 3.14.7 | grün | 25,47 s |
| Originalvollsuite 2 | 3.14.7 | grün | 204,82 s |
| Datenkern nach Appimport, 20 Runden ohne Fenster/Schreiber | 3.14.7 | grün | 30,90 s |
| Kernprobe 2, 26.420 Punkte / 40 Runden | 3.14.7 | grün | 138,28 s |
| Originalvollsuite 3 | 3.14.7 | grün | 201,48 s |
| Ergänzende Originalvollsuite | 3.15.1 | grün | 160,69 s |
| Intel-Originalbestand, reiner Datenkern / 20 Runden | 3.14.7 | grün | 26,15 s |
| Intel-Originalbestand nach Appimport / 20 Runden | 3.14.7 | grün | 28,69 s |

Die vier Vollsuiten bestanden jeweils auch sechs harte Schreiberabbrüche sowie Parallelität, Sperren, Sicherungsrotation und Startmigrationen. Zusammen mit den zwei Kernproben **240 Änderungs-/Speicher-/Laderunden**, dazu **80 Daten-/Importdurchgänge** und **24 beabsichtigte Schreiberabbrüche**. Der Umfang und sämtliche Datenvergleichskriterien blieben unverändert. Die damals auf Intel ebenfalls betroffene Pythonversion 3.14.7 zeigt hier keinen WA-41A-/WA-41B-Befund; der Systemunterschied ist damit besser gestützt, die Ursache noch nicht isoliert.

**Integritätswächter und Dokumentänderung:** Während der Folge traf der zusätzliche Dokumentationsaudit ein und änderte in der Arbeitskopie ausschließlich `tests/fixtures/showcase/README.md` aus dem alten 470-Dateien-Manifest. Der streng auf alle 470 Arbeitskopiedateien prüfende Orchestrator endet deshalb mit Exitcode 1, obwohl alle acht Testprozesse selbst Exitcode 0 und gültige Abschlussmarker haben. Der eingefrorene ausführbare Prüfstand blieb vollständig bytegleich. Die unabhängige Schlussauswertung prüft Log-/Trace-/Helferhashes, beide Eingangsdateien und alle 470 eingefrorenen Dateien; nur diese dokumentierte README-Abweichung in der Arbeitskopie ist zugelassen. Kein ausführbarer Quell-, Test-, Daten- oder Ressourcenunterschied. Keine Rohdaten umgeschrieben oder aus einem roten Einzeltest ein grüner gemacht.

## Prüfaufbau

- AMD Ryzen 7 5800X3D, acht Kerne/16 logische Prozessoren, MSI B550M PRO-VDH WIFI, BIOS 2.L0. Windows 11 Pro, Build 26300. Hersteller-/Modell-/Laufzeitinformationen und Binärhashes stehen im Nachweis. Keine Affinitätsbindung oder Leistungs-/Firmwareänderung.
- Hauptvergleich mit Python **3.14.7**, Build `823f032`, MSC 1944, Tk/Tcl 9.0.4. Diese Version war auch auf PC 2 betroffen: Die [damalige Bilanz](../wa41_2026-10-27/auswertung.json) enthält eine grüne und eine mit `0xC0000005` abgebrochene Kernprobe sowie eine grüne Originalsuite.
- Ein zusätzlicher Originalvolltest mit der hier vorhandenen Python-Version **3.15.1**, Build `c37e74c`, Tk/Tcl 9.0.4. Er ist eine ergänzende Gegenprobe; der spätere Intel-Versionsvergleich verwendete **3.15.2** bzw. **3.14.8**. Diese Laufzeiten werden hier nicht installiert oder als bytegleich behauptet. GIL aktiv, JIT aus.
- Alle **470** Dateien des [maßgeblichen Manifests](../dreierpaket_2026-10-27/quellstand.json) stimmen vor Beginn bytegenau mit dem damaligen Quell-/Test-/Ressourcen-/Fixturestand überein. Kopie außerhalb OneDrive in `%USERPROFILE%\GlidePruefung\amd-wa41-*`; SHA-256 vor/nach jedem Fall sowie abschließend für Arbeitskopie und Prüfkopie kontrolliert.
- Jeder Prozess verwendet eigene künstliche Daten unter einem separaten `GLIDE_DATA_DIR`. Für diese Kindprozesse zeigen auch `TMP`/`TEMP` in den festen Prüfordner. `PYTHONHASHSEED=0`, `PYTHONUTF8=1`, `PYTHONFAULTHANDLER=1`, kein Bytecodeschreiben, normaler Allokator. Fälle nacheinander, Zeitlimit jeweils 300 Sekunden.
- Drei unveränderte Originalvollsuiten unter 3.14.7; zwei normale instrumentierte Kernproben mit denselben 40 Änderungs-/Speicher-/Laderunden; je eine reine Fachmodul- und Appimportprobe mit 20 Runden; eine zusätzliche Originalvollsuite unter 3.15.1. Originalsuite und Produktionsquellen unverändert, Helfer zusätzlich gehasht. Eine Null als Orchestrator-Exitcode allein ist kein Erfolgskriterium: Exitcode, Abschlussmarker und Konsistenz-/Integritätsbefunde werden einzeln ausgewertet.

## Daten- und Vergleichsgrenzen

Die ursprüngliche temporäre Eingangsdatei auf PC 2 ist hier nicht unter dem alten Benutzer-/Temp-Pfad verfügbar. Beim späteren Dokumentabgleich wurde jedoch die zusätzliche geschützte Projektkopie unter `lokale_belege/eingang/initial.json` vorgefunden und ihr SHA-256 `a3b8c0cac4c72e1820e71730ad78e312f2a30338678fbcfe2a2b6d91dae081f4` sowie ihr Umfang von 28.548.872 Bytes bestätigt. Dieser inzwischen verfügbare Originalbestand wird deshalb in zwei zusätzlichen, getrennten Datenkern-/Importproben verwendet; [Zusatznachweis](originalbestand/ergebnis.json). `original_intel_payload_available=false` im Hauptnachweis beschreibt dessen ursprünglichen Aufbau, nicht den abschließenden Übernahmestand. Der [zwischenzeitliche Dokumentationsaudit](../dokumentationsaudit_2026-10-27/README.md) dokumentiert die zusätzliche Belegsicherung.

Die Originalsuite erzeugt ihre 26.420 Punkte weiterhin selbst mit unverändertem Zufallsseed und unveränderten Assertions. UUIDs und Zeitstempel sind deshalb nicht bytegleich zu Intel oder zwischen den Vollsuiten. Kein streng bytegleicher Volltest-Replay; die Zusatzproben mit Originalbytes sind reine Daten-/Importproben.

Die erste Kernprobe sichert zusätzlich einen neuen künstlichen AMD-Anfangsbestand für die ersten beiden reinen Daten-/Importproben. SHA-256 `6b6979ab5b9a3288720fd42dfbcd326caa6c964346bee67d2c547c870eec5e68`, ebenfalls 28.548.872 Bytes; lokaler Pfad im Hauptnachweis. Dieser Bestand wird nicht mit dem Intel-Original gleichgesetzt. Keine echten Nutzerdaten verwendet.

Die vollständige Suite prüft zusätzlich zu den 40 Runden sechs harte Schreiberabbrüche, parallele Schreiber, Sperren, Sicherungsrotation und Startmigrationen. Ihre Prüfung entzogener POSIX-Schreibrechte ist unter Windows bedingt übersprungen; eine Windows-ACL-Prüfung wird daraus nicht abgeleitet. Die Kern- und Importproben ersetzen die Originalsuite nicht.

## Unvollständiger Temp-Vorlauf

Der [erste Versuch](ergebnis.json) bleibt unverändert erhalten. Vorher stimmten alle 470 Dateien; eine Kernprobe endete grün nach 40 Runden. Die folgende Originalsuite passierte die Datenrunden, scheiterte aber beim Start des ersten Schreibers in Phase 3 an `ModuleNotFoundError: drawing`. Danach fehlten in der Temp-Prüfkopie 340 Manifestdateien, darunter die Originalsuite; weitere Fälle waren dadurch reine Startfehler. Die Arbeitskopie blieb vollständig unverändert. Eine Ursache oder ein verursachender Prozess für diese Dateilöschungen ist nicht nachgewiesen.

Dieser Vorlauf wird weder als reproduzierter nativer WA-41-Absturz noch als vollständig grüner Lastvergleich gezählt. Die feste Folge verwendet eine neue Kopie außerhalb des System-Temp-Verzeichnisses und prüft die Integrität nach jedem Prozess. Keine Originalprotokolle gelöscht oder frühere rote Intel-Ergebnisse nachträglich umgewertet.

## Fortsetzung und Grenzen

WA-41A bezeichnet unerwartete Interpreter-/Prozessfehler, WA-41B den früheren Unterschied zwischen gespeichertem und geladenem Bestand. Beide Fehlerbilder wurden im AMD-Nachlauf nicht reproduziert. Wiederholt grüne AMD-Läufe stärken den Hinweis auf einen Unterschied der beiden Systeme, sind aber kein isolierter Beweis für einen CPU-Defekt oder einen bestimmten Firmwarefehler. CPU, Mainboard, Firmware und Prozessumgebung sind kein kontrollierter Einzelfaktorversuch. Frühere rote Intel-Belege und die offene Ursachenfrage bleiben erhalten; WA-41 wird nicht pauschal als repariert geschlossen.

Betroffene Last-/Diagnosefälle, keine erneute gesamte Integrationsmatrix, keine native Plattform-/Reader-/DPI-/Menschenabnahme und kein Liefer-/Releaseabschluss. Python-Lieferung bleibt 3.47.0, eigenständige Pakete 3.45.0; Quelle 3.48.0 bleibt Prüfkandidat.

Reproduktion: `python.exe -B -u pruefen.py --bericht <neuer leerer Nachweisordner>`. Das Skript verwendet die beiden ausdrücklich erfassten installierten Laufzeiten, legt eine neue feste lokale Prüfkopie an und verweigert das Überschreiben vorhandener Ergebnisse. Rohlogs, künstlicher Großbestand und lokale Prüfkopie bleiben lokal.
