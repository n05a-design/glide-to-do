# WA-41: Prozessdiagnose im gemeinsamen Prüfungsstarter

Stand 28.10.2026 · Glide 3.48.0 · Aufgabenformat 26

Nutzerauftrag: Den nach dem AMD-Vergleich plausiblen Intel-/Systemeinfluss als mögliche Ursache bei den zuvor fehlgeschlagenen Tests berücksichtigen. Zehn ausgewertete AMD-Prozesse waren grün; dies ist kein isolierter Nachweis eines Intel-CPU-Defekts. [Vorhandener Vergleich](../amd_vergleich_2026-10-27/README.md).

## Umsetzung und Grenze

`tests/tools/prozessdiagnose.py` wird durch `Prueflauf` in `pruefen.py` genutzt, damit auch die CI-Grundstufe denselben Baustein verwendet. Lesender CPU-/BIOS-/Python-Kontext und App-SHA-256, unverändertes Rohlog, ursprünglicher Exitcode und gezielte Diagnose-JSON mit Zeitfenster. Möglicher Software-/Systemeinfluss bei passenden Prozess-/Interpretersignaturen; konkrete Save/Reload-Abweichung eigenständig WA-41B. Fehler bleiben rot; keine Hersteller-Skips, Wiederholungen, Mengengrenzen oder Systemänderungen. Dieser Nachlauf verändert keine Produktionsquellen und keine Assertions der Originalsuite.

[Vertrag und konkrete Signaturen](../../../docs/05_QA_TESTPLAN.md#prozessabstürze-und-möglicher-prüfplatzfehler-wa-41). Direkte Originalsuite-/historische Helferaufrufe ohne gemeinsamen Starter erhalten keine neue Elternprozessdiagnose. Die zusätzlichen Prüfwerkzeuge gehören nicht zum historischen 470-Dateien-Manifest; dieses bleibt eine Referenz des damaligen Standes.

## Prüfung

16 gezielte Werkzeuggegenproben grün, darunter native signed/unsigned Statuswerte, Intel/AMD, Cacheabbruch, Datenabweichung, gewöhnliche Ausnahme, Timeout, bewusster Schreiberabbruch bei erfolgreicher Suite, unveränderter Fehlerstatus, Log-/JSON-Nachweis und ein echter kurzer Kindprozess mit kontrolliertem Exitcode 7. Kein echter Interpretercrash oder Großlasttest ausgelöst. Zusätzlich besteht die Diagnose-Gegenprobe am parallel ergänzten Integritätswächter. Alle fünf roten historischen Prozesse des Python-Versionsvergleichs werden erkannt; fünf grüne bleiben ohne Fehlalarm ([Signaturgegenprobe](signaturgegenprobe.json), ausschließlich vorhandene Logs gelesen). Ergebnis der ergänzenden Grundstufe und abschließender Hashabgleich in [ergebnis.json](ergebnis.json).

Die bestehenden roten Intel-Belege werden nicht umgeschrieben. Appweiter Wiederanlauf, komplette Vereinheitlichung/Integritätswächter, symbolisierte Dumpanalyse, WA-41-Ursache und Release-/Lieferabnahme bleiben offen. Ausgangsstand dieses Werkzeugnachlaufs: Quelle 3.48.0-Kandidat, Python/Showcase 3.47.0, native Pakete 3.45.0. Die unabhängige parallele Produktionsrunde hat die Quelle inzwischen auf 3.49.0 angehoben; deren Abnahme ist nicht Bestandteil dieses Nachweises.

Technische Referenzen: [Microsoft NTSTATUS-Werte](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-erref/596a1078-e883-4972-9bbc-49e60bebca55), [Python subprocess: Prozessstatus und Signale](https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess.returncode). Exit-/Fehlersignatur beschreibt einen Abbruch, nicht seine Ursache.

**Paralleler Arbeitsstand:** Während der Grundprüfung trafen unabhängige Änderungen am Prüfungsstarter und an Produktionsdateien ein. Diese Änderungen werden erhalten, gehören aber nicht zu diesem Diagnoseauftrag. Der begleitende CI-Lauf ist deshalb keine Abnahme eines durchgehend eingefrorenen aktuellen Gesamtstands. Die gezielten Diagnosegegenproben wurden auch gegen die neue Wächter-Schnittstelle ausgeführt.

Die begleitende Grundprüfung wurde wegen dieses Quell-/Versionswechsels gezielt beendet. Zuvor 208 Werkzeugtests ohne Fehler (ein Skip), Fachlogik mit und ohne Systemzeitzonen jeweils grün. Keine vollständige CI-Abnahme; die abschließenden 16 gezielten Diagnosefälle und der rein lesende historische Signaturabgleich sind davon getrennte Nachweise.
