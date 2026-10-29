# WA-41: wiederholter Vergleich mit Python 3.15.2

Stand 27.10.2026 · Glide 3.48.0 · Aufgabenformat 26

**Späterer Diagnosenachtrag:** [Last-/Fenster-/CPU-Gegenproben](../last_fenster_2026-10-27/README.md) liefern einen konkreten CPU-/Firmwareverdacht mit WHEA-Ereignissen und Affinitätsvergleich. Der vorliegende Versionsvergleich und seine roten Befunde bleiben unverändert gültig; keine Ursache oder Reparatur dadurch bestätigt.

**Ergebnis: WA-41 tritt auch mit Python 3.15.2 auf.** Vier von acht neuen 3.15-Prozessen scheitern, darunter zwei originale vollständige Lastläufe. Derselbe native Fehlercode und derselbe Generatorausdruck wie unter 3.14 sind belegt. Der Versionswechsel ist kein Fix; die genaue Ursache bleibt offen.

Auftrag: die installierte Python-3.15-Version gezielt verwenden und prüfen, ob der bekannte Lastfehler dort ebenfalls auftritt. Die Systemvorgabe, Produktionsquellen und vorhandenen Lieferungen werden nicht geändert. Dieser Nachweis ergänzt die [vorherige Ursachenanalyse](../wa41_2026-10-27/README.md); deren 24 Gegenproben und ursprüngliche rote Befunde bleiben erhalten.

## Prüfaufbau

Maßgeblich ist dieselbe eingefrorene Quelle außerhalb OneDrive. Vor dem Start werden alle 470 Quell-/Prüf-/Ressourcen-/Fixturedateien sowohl in der Arbeitskopie als auch in der eingefrorenen Kopie gegen das vorhandene SHA-256-Manifest geprüft. Der künstliche Anfangsbestand hat 26.420 Punkte und 28.548.872 Bytes. Alle Appimporte verwenden temporäre `GLIDE_DATA_DIR`-Ordner; keine echten Nutzerdaten.

Zehn neue Prozesse, feste Reihenfolge, nacheinander:

1. Python 3.15.2: originale vollständige Speicherlastsuite, Lauf 1.
2. Python 3.14.8: bestehende normale Kernprobe, Gegenprobe 1.
3. Python 3.15.2: dieselbe normale Kernprobe, Lauf 1.
4. Python 3.15.2: Importprobe mit 20 reinen Datenrunden, Lauf 1.
5. Python 3.15.2: originale vollständige Speicherlastsuite, Lauf 2.
6. Python 3.14.8: normale Kernprobe, Gegenprobe 2.
7. Python 3.15.2: normale Kernprobe, Lauf 2.
8. Python 3.15.2: Importprobe mit 20 reinen Datenrunden, Lauf 2.
9. Python 3.15.2: originale vollständige Speicherlastsuite, Lauf 3.
10. Python 3.15.2: Importprobe mit 20 reinen Datenrunden, Lauf 3.

Die vollständige Suite ist unverändert und umfasst 40 Änderungs-/Speicher-/Laderunden, sechs harte Schreiberabbrüche, parallele Schreiber, Sperren, Sicherungen, Startmigrationen und Schreibrechte. Die bestehende Kernprobe enthält nur die ersten beiden Phasen mit 40 Runden; sie ist kein Ersatz für die vollständige Suite. Die Importprobe erzeugt weder Tk-Root noch ListApp und schreibt den verglichenen Großbestand nicht. Sie umfasst JSON-Lesen, Serienprüfung und echten Speichervergleich.

Beide Laufzeiten melden GIL aktiv, JIT aus und Tk 9.0.4. Python, Compiler, Standardbibliothek, `_tkinter` sowie Tcl-/Tk-Binärdateien unterscheiden sich jedoch. Ein Unterschied zwischen den Ergebnissen ist deshalb ein Befund zum jeweiligen Laufzeitpaket und beweist noch keinen isolierten CPython-Kernfehler. Die Binärhashes werden erfasst; vorhandene Dateien sind keine Liste tatsächlich geladener DLLs.

Kindprozesse erhalten `PYTHONHASHSEED=0`, `PYTHONUTF8=1`, `PYTHONFAULTHANDLER=1` und deaktiviertes Bytecodeschreiben. Kein alternativer Allokator, kein expliziter Cachewechsel und keine Deaktivierung produktiver Funktionen in den normalen Kernproben. Jeder Prozess hat ein Zeitlimit von 300 Sekunden; ein Timeout würde ausdrücklich ausgewiesen und nur der eigene Prüfprozess samt seinen Schreibern beendet.

## Ergebnisse

Die Folge ist vollständig abgeschlossen: zehn Prozesse, fünf grün/fünf rot. Unter **3.15.2 vier grün/vier rot**, unter 3.14.8 eine grüne/eine rote Kernprobe. Unterschiedliche Prüfarten und begrenzte Wiederholungszahl: daraus keine allgemeine Ausfallwahrscheinlichkeit ableiten.

| Fall | Laufzeit | Ergebnis | Dauer |
| --- | --- | --- | --- |
| Vollsuite 1 | 3.15.2 | grün, alle acht Prüfbereiche | 96,55 s |
| Kernprobe, Gegenprobe 1 | 3.14.8 | `0xC0000005`, Serienprüfung in Runde 18 | 39,33 s |
| Kernprobe 1 | 3.15.2 | `0xC0000005`, derselbe Generator in Runde 37 | 66,18 s |
| Importprobe 1 | 3.15.2 | grün, 20 Runden | 12,52 s |
| Vollsuite 2 | 3.15.2 | `0xC0000005`, derselbe Generator beim Laden | 11,40 s |
| Kernprobe, Gegenprobe 2 | 3.14.8 | grün, 40 Runden | 75,12 s |
| Kernprobe 2 | 3.15.2 | Speicherfehler in Runde 13, danach nativer Abbruch bei Fehlerausgabe | 26,70 s |
| Importprobe 2 | 3.15.2 | grün, 20 Runden | 12,44 s |
| Vollsuite 3 | 3.15.2 | `0xC0000409`, `_TAIL_CALL_CACHE: Executing a cache`, ungültiger Frame | 31,74 s |
| Importprobe 3 | 3.15.2 | grün, 20 Runden | 12,43 s |

In Kernprobe 1 und Vollsuite 2 unter 3.15 steht wie in der roten 3.14-Gegenprobe `repeat_rules.py:196` im obersten Frame: Generatorausdruck in `check_stored_series`, aufgerufen über Normalisierung/Lesen/Laden. Das ist eine gemeinsame **Absturzsignatur**, kein Beweis, dass die Python-Zeile den Zustand verursacht hat. Kernprobe 2 meldet vorher beim Speichern `catching classes that do not inherit from BaseException is not allowed`; nach der protokollierten Assertion stürzt der Prozess zusätzlich beim Formatieren des Tracebacks in `_safe_can_colorize`/Importkompilierung ab. Diesen sekundären Absturz nicht mit einem primären Appimportfehler verwechseln.

Die Windows-Ereignisse bestätigen die nativen Abbrüche in `python315.dll`, beim internen Cacheabbruch in `ucrtbase.dll`. Der rote originale Volltest zeigt, dass der 3.15-Befund nicht nur vom verkürzten Diagnosehelfer abhängt. Die grünen Voll-/Importläufe belegen zugleich weiter das sporadische Auftreten. Die erste grüne 3.15-Kernprobe aus der früheren 24er-Diagnose war keine Entwarnung.

Maschinenlesbare [Bilanz](ergebnis.json), geprüfte [Absturzsignaturen](auswertung.json) und [Windows-Ereignisse](native_events.json). `completed` ist wahr; sämtliche Loghashes wurden nachgeprüft. Exitcode null des Orchestrators allein bedeutet keine grünen Einzelfälle. Rohlogs mit absoluten lokalen Pfaden bleiben lokal.

**Quelltreue:** Vor und nach der Folge alle 470 Dateien in Arbeitskopie und eingefrorener Quelle unverändert. Keine Produktionsreparatur, kein Lieferabgleich, keine Versions-/Formatänderung und keine Releasefreigabe. WA-41 bleibt offen. Die Untersuchung muss nun versionsübergreifend fortgesetzt werden; ein sauberes zweites Windows-System und native Speicherabbilder sind weiterhin die entscheidenden Gegenbelege für Laufzeitkern, gemeinsame native Komponenten oder lokale Prozessumgebung.

## Reproduktion

`pruefen.py --python315 <Pfad zu python.exe 3.15.2> --control314 <Pfad zu python.exe 3.14.8>` mit einer dieser Laufzeiten starten. Die bestehenden lokalen `freeze_ort.log`-/`payload_ort.log`-Hinweise müssen noch auf die unveränderten temporären Prüfkopien zeigen. Das Skript prüft Hashes vor und nach der Folge und protokolliert Versionen, Fallfolge, Laufzeiten, Fehler und Ergebnisartefakthashes. Es installiert nichts, ändert keine Standardlaufzeit und startet keine Fernprüfung.
