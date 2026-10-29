# WA-41: gezielte Ursachenanalyse

Stand 27.10.2026 · Glide 3.48.0 · Aufgabenformat 26

**Späterer Ablage-/Dumpnachtrag:** Die folgende Phase samt `auswertung.json` bleibt ein historischer Zwischenbefund. Ihre damalige Aussage „keine nativen Speicherabbilder“ ist inzwischen überholt: acht ältere Minidumps wurden bestätigt und zusätzlich lokal gesichert; noch kein FullMemory-Dump und keine symbolisierte Auswertung. [Aktuelle Übergabe](../../../../../00_Arbeitsvorbereitung/Glide_Uebergabe.md#0-sofortübergabe-wa-41--zuerst-lesen), [Sicherungsmanifest](../dokumentationsaudit_2026-10-27/beweissicherung_lokal.json). BIOS/CPU vorerst unverändert; kein weiterer Lastlauf aus dem Dokumentationsauftrag.

**Vorrangiger späterer Befund:** [Internet-/Last-/CPU-Nachdiagnose](../last_fenster_2026-10-27/README.md) findet 25 historische WHEA-Prozessorkern-Paritätsfehler bei i9-14900K/F19/0x12B und zwei grüne CPU-0-Kernläufe gegenüber roter normaler Affinitätsgegenprobe. Lokale CPU-/Firmwarestabilität ist jetzt die stärkste konkrete Ursachenspur; kein bewiesener Zusammenhang oder CPU-Defekt. Die folgende 24er-Diagnose ist die vorangegangene Phase, ihr Hardwareverdacht war damals noch nicht geprüft.

**Neuer Befund mit Python 3.15.2:** Im [anschließenden Versionsvergleich](../python315_vergleich_2026-10-27/README.md) vier von acht 3.15-Prozessen rot, darunter zwei originale vollständige Lastläufe. Gleiche Zugriffsverletzung am Generator in `repeat_rules.py:196` und erneut interner Cacheabbruch. WA-41 ist nicht auf 3.14 begrenzt; Update auf 3.15 behebt ihn nicht. Die folgenden 24 Gegenproben bleiben die vorherige Diagnosephase.

## Ergebnis

**Die genaue Ursache bleibt offen. Die neuen Befunde sprechen am stärksten für einen ungültigen Ausführungszustand im Python-Prozess.** Ein normaler fachlicher Speicher-/JSON-Fehler erklärt die Kombination aus Zugriffsverletzungen, internem Interpreterabbruch und wechselnden Typfehlern nicht ausreichend. Ob CPython selbst, eine native Bibliothek oder eine Besonderheit dieses Rechners den Zustand auslöst, ist noch nicht entschieden. Der Stack des Absturzes zeigt nicht zwingend den vorherigen Verursacher.

Die Fehlerbilder werden vorläufig unter WA-41 untersucht. Dass alle denselben Ursprung haben, ist ebenfalls noch eine Hypothese.

24 zusätzliche, getrennte Diagnoseprozesse: 15 grün, neun rot; darunter vier native Abbrüche und fünf Python-Fehler. Das sind unterschiedliche, schrittweise gewählte Gegenproben, **keine statistische Ausfallrate**. [Auswertung](auswertung.json), Rohbilanzen [1](matrix.json), [2](matrix2.json), [3](matrix3.json), [4](matrix4.json), [5](matrix5.json), [6](matrix6.json). Die ursprüngliche rote Vollprüfung und alle vorherigen grünen/roten Gegenproben bleiben im [Dreierpaketnachweis](../dreierpaket_2026-10-27/README.md) erhalten.

## Kleinster beobachteter Auslöser

In `pure_import_app` genügte diese Folge: unverändertes Appmodul importieren, danach den künstlichen Großbestand wiederholt als JSON lesen, Serien prüfen und den echten Speichervergleich bilden. Zwei Runden waren grün, die dritte scheiterte in `repeat_rules.check_stored_series` mit `TypeError: 'tuple' object is not an iterator` innerhalb eines Generatorausdrucks über `dict.values()`.

Dabei wurden **kein Tk-Fenster, keine ListApp-Instanz und kein produktiver Speicherweg** ausgeführt. Geschrieben wurden nur die isolierte kleine Startfixture und Diagnoseausgaben, nicht der verglichene Großbestand. Das grenzt Fensterdarstellung, Windows-Titelleiste und Dateischreiben als notwendige Auslöser dieses Fehlerbilds aus. Der Import lädt allerdings weiterhin Appabhängigkeiten, darunter native Erweiterungen; er ist kein Nachweis eines Prozesses ohne nativen Code. Spätere Importwiederholungen waren grün: noch kein stabiler Minimalreproducer.

## Gegenproben und Aussagegrenzen

| Gegenprobe | Ergebnis | Belastbare Aussage |
| --- | --- | --- |
| Python 3.14.8, normale Kernprobe | nativer Abbruch `0xC0000409`, „Executing a cache“, ungültiger Frame | Fehler innerhalb der Interpreterausführung beobachtet |
| Python 3.14.7, gleiche Kernprobe | einmal grün, einmal `0xC0000005` | Nicht auf 3.14.8 beschränkt |
| Python 3.14.7, originale vollständige Lastsuite | grün, 102 Sekunden | Fehler tritt intermittierend auf; Kernprobe ersetzt diesen Gesamttest nicht |
| Python 3.15, Kernprobe | einmal 40 Runden grün | Vergleichskandidat; kein belegter Fix und kein Versionswechsel |
| Windows-Chrome-/Titelleistenbehandlung vor Appstart deaktiviert | weiterhin `0xC0000005` | Diese Aufrufe sind keine notwendige Voraussetzung |
| Große UI-Aktualisierungen nach Appstart deaktiviert | Fehler bereits in Runde 1: `'cell' object is not an iterator` | Laufende UI-Neudarstellung ist keine notwendige Voraussetzung; Initialisierung bleibt enthalten |
| Zyklische Garbage Collection vor Import deaktiviert | `name 'isinstance' is not defined` | Abschalten der GC behebt den Fehler nicht; Referenzzählung bleibt aktiv |
| `PYTHONMALLOC=debug` | `'bool' object is not an iterator` | Kein Debug-Allocator-Befund in diesem Lauf; keine Entwarnung für alle nativen Speicherfehler |
| `PYTHONMALLOC=malloc` | `'tuple' object is not an iterator` | Nicht ausschließlich an den Standard-Kleinobjektallocator gebunden |
| Großbestand nur mit Tk-freien Fachmodulen | 20 Runden grün | Diese Eingabedaten allein reproduzierten den Fehler in dieser Probe nicht |
| Minimaler Tk-Root ohne Appimport | 20 Runden grün | Tk allein nicht als Auslöser nachgewiesen |
| Vollständige Appinitialisierung, anschließend reiner Datenvergleich | 20 Runden grün | Auch vorhandene App/Tk-Instanz erzwingt den Fehler nicht |
| Nur App kompilieren / nur Imports / Modulkopf vor ListApp ausführen | je 20 Runden grün | Große Quellkompilierung und diese Imports allein nicht als Ursache belegt |
| Bereinigter Kindprozess-PATH ohne Codex-Poppler-Laufzeiten | weiterhin `0xC0000005` | Zusätzlich geladenes Poppler-ICU 78 ist keine notwendige Voraussetzung |
| Frischer Bytecodecache / frische Kompilierung / bestehender Cache | alle letzten Wiederholungen grün | Beschädigter oder veralteter Dateicache nicht belegt |

Beide 3.14-Laufzeiten verwenden den GIL, der optionale JIT war aus; Python-Trace-/Profile-Hooks und registrierte Monitoring-Tools waren nicht aktiv. Die vorhandenen `_tkinter`-/Python-DLL-Versionen passen jeweils zusammen, Tk ist 9.0.4. Das widerlegt keine beliebigen ABI-/Bibliotheksfehler, liefert aber keinen Beleg für einen simplen 3.14.7/3.14.8-Dateimix. Eine eigene ausführbare Tk-9.1-Gegenprobe war lokal nicht vorhanden.

## Bedeutung des internen Cachefehlers

`Executing a cache` bezieht sich auf den `CACHE`-Opcode im Interpreter. Im [exakten CPython-3.14.8-Quellstand](https://github.com/python/cpython/blob/v3.14.8/Python/generated_cases.c.h) führt dessen Ausführung im Block `TARGET(CACHE)` absichtlich zu `Py_FatalError`. Das ist **kein Dateicachefehler**. Wie der Interpreter dort landete, geht aus dem Abbruchtext nicht hervor.

Die aus `.pyc` geladenen Codeobjekte für App, `repeat_rules` und `save_comparison` wurden rekursiv mit frisch kompiliertem Quellcode verglichen: keine strukturellen Unterschiede in Codeattributen/Konstanten; Headerzeit und Quellgröße passen. Unterschiedliche `marshal.dumps`-Bytes allein wären wegen Internierungs-/Referenzflags kein Korruptionsnachweis. Frische Cachepfade und frische Hauptdateikompilierung waren grün, ebenso die letzten Wiederholungen mit bestehendem Cache. Cachelöschen ist damit kein begründeter produktiver Fix.

## Native Befunde und verworfene Verdachtsmomente

[Windows-Ereignisse](native_events.json) bestätigen drei neue Zugriffsverletzungen in `python314.dll` und den internen Abbruch über `ucrtbase.dll`; zusätzlich ist der ursprüngliche Vollprüfungsabsturz enthalten. Der Offset `0x497ab` in Python 3.14.8 tritt beim ursprünglichen Volltest und bei der Probe ohne Windows-Chrome auf. Ohne native Stacks mit Symbolen lässt sich daraus kein schuldiger Aufruf ableiten. Für die neuen Abbrüche wurde kein lokales Python-Speicherabbild gefunden; cdb/WinDbg waren nicht verfügbar. Keine globalen Windows-Debug-/Dump-Einstellungen geändert.

Ein älterer Lieferbericht enthielt einen Hinweis auf `tv_x64.dll`. Diese DLL wurde in den aktuellen Appstartinventaren nicht gefunden. Die normale Umgebung lädt über PATH zusätzliche ICU-78-Bibliotheken aus der Codex-Poppler-Umgebung. Eine Gegenprobe ohne diese PATH-Einträge verwendet stattdessen System-ICU und stürzt ebenfalls ab. Beide Beobachtungen rechtfertigen aktuell keine Schuldzuweisung an TeamViewer, Codex oder ICU.

Die produktiven `ctypes`-Einstiege für GDI-Schriften, DWM/Windows-Chrome und Prozess-/Dateisperren wurden gelesen. Kein belegter Signaturfehler oder absichtlicher Codeobjekt-/Speichereingriff gefunden. GDI-Schriften werden erst bei ListApp-Initialisierung registriert und erklären den beobachteten Importfall daher nicht unmittelbar. Das ersetzt keine native Speicherprüfung.

## Bewertung der Ursachen

1. **Stärkste Arbeitshypothese:** Fehler im Ausführungs-/Objektzustand des Python-Prozesses unter dieser Kombination aus Appimport und hoher Objektlast, eventuell durch native Erweiterung oder lokale Prozessumgebung ausgelöst. Der interne Cacheabbruch und die wechselnden, für den jeweiligen Ausdruck unplausiblen Objekttypen sind die Hauptbelege. Der Nachlauf reproduziert den Fehler auch unter 3.15.2; eine Beschränkung auf 3.14 ist widerlegt. Ein CPython-Bug ist damit noch nicht bestätigt.
2. **Weiter offen:** Appimport-Nebenwirkung oder native Bibliothek, die früher einen fehlerhaften Zustand erzeugt. Das große ListApp-Klassenobjekt ist ein sinnvoller nächster Reduktionsschnitt, aber dessen Umfang wurde nicht als Ursache belegt. Reine Python-Modullogik, Dekoratoren/Globals und native Imports müssen dabei getrennt werden.
3. **Schwächer gestützt:** deterministischer Fehler der Speicherfachlogik oder bestimmter JSON-Daten. Dagegen sprechen identische grüne Durchläufe und die internen Fehler; der frühere Ladevergleichsfehler bleibt trotzdem ein realer, bisher nicht bis zum konkreten Feld aufgeklärter Befund.
4. **Nicht belegt:** reale Nutzerdatenkorruption, Hardwaredefekt, OneDrive, die neuen drei Features, Dateicachedefekt oder ein ausschließliches 3.14.8-Problem. Die eingefrorene Quelle und alle Testdaten liegen außerhalb OneDrive; Hardware wurde nicht untersucht. Ein grüner 3.47.0-Basislauf schließt eine Regression nicht aus; WA-41 ist bereits seit 3.44.0 dokumentiert.

## Nächster entscheidender Untersuchungsschritt

Priorität hat dieselbe eingefrorene Quelle mit diesem künstlichen Bestand auf einem sauberen zweiten Windows-System: wiederholte originale Vollsuite plus Importkern, dazu eine getrennte 3.14-/3.15-Laufzeit-/Tk-Matrix. Beim ersten nativen Fehler einen Speicherabzug mit passenden CPython-Symbolen erfassen. Das trennt Code-/Laufzeiteffekt von diesem Rechner und identifiziert möglicherweise den ersten ungültigen Zugriff. Keine blinde Änderung von Speichervergleich oder atomarem Schreiber.

Wenn der reine Importkern zuverlässig rot wird, den Import bis zur kleinsten notwendigen Klasse/Modulnebenwirkung reduzieren und erst dann einen reproduzierbaren CPython-/Tk-Bericht ableiten. Der anschließende wiederholte 3.15-Vergleich ist ebenfalls rot und rechtfertigt keine Schließung von WA-41. Keine bestehende Fernprüfung gestartet, keine globale Laufzeit, Nutzerdatei oder Windows-Einstellung verändert.

## Reproduktion und Grenzen

`probe.py` führt auf der eingefrorenen Kopie nur Phasen 1/2 der vorhandenen Lastsuite mit 26.420 künstlichen Punkten und 40 Änderungs-/Laderunden aus; Originalassertionen bleiben erhalten, zusätzliche Felddiagnose vor dem unveränderten Fehlerkriterium. Nach Runde 40 Ende statt der übrigen Schreiber-/Sperr-/Migrationsprüfungen. Die Varianten ändern ausschließlich den jeweiligen Prüfprozess. `pure_probe.py` liest denselben künstlichen Anfangsbestand und verwendet echte Fachmodule; die Startkontexte und Cachewege werden getrennt ausgewählt. Beide Helfer wurden während der Eingrenzung erweitert; alte Trace-Zeilennummern können deshalb vom aktuellen Helfer abweichen.

Beispiel für einen isolierten Prozess, mit Variablen für vorhandene Laufzeit, eingefrorene Kopie und temporäre künstliche Payload:

```powershell
$env:PYTHONHASHSEED = '0'
$env:PYTHONUTF8 = '1'
$env:PYTHONFAULTHANDLER = '1'
& $taskPython -B .\pure_probe.py --repo $taskFrozenRepo --payload $taskSyntheticJson --bootstrap import --iterations 20
& $taskPython -B .\probe.py --repo $taskFrozenRepo --output $taskTraceLog --variant normal
```

`payload_ort.log` hier und `freeze_ort.log` im benachbarten Dreierpaketnachweis enthalten die lokalen temporären Orte. Logs mit absoluten Rechnerpfaden bleiben lokal; keine echte Nutzerdatenquelle. `auswertung.py` aggregiert nur vorhandene Ergebnisse und kontrolliert die 470 eingefrorenen Quell-/Prüf-/Ressourcen-/Fixturedateien. Ihre Prüfung ergibt unveränderte Bytes. Neue Diagnosehelfer sind zusätzlich, Produktionscode und Lastsuite bleiben unverändert. **WA-41 bleibt offen und das Release-Tor bleibt geschlossen.**

Methodenquelle: [Python-Dokumentation zu Faulthandler und PYTHONMALLOC](https://docs.python.org/3.14/using/cmdline.html#envvar-PYTHONMALLOC). Debugallocator und alternative Allokatoren sind Gegenproben, kein vollständiger Speicherfehlerausschluss. Fremde Fehlermeldungen aus Issue-Trackern wurden mangels passender Voraussetzungen nicht als identische Ursache übernommen.
