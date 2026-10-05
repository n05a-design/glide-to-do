# QA-Bericht

Stand 05.10.2026 · Glide 3.33.8 laut VERSION · Datenformat 20

## Aktueller Prüfstatus

Beim Einstieg am 05.10.2026 waren VERSION, APP_VERSION, Hauptsuite und CHANGELOG konsistent mit 3.33.6; Hauptdatei und capture_parser.py waren in der Python-Lieferung vorhanden. Die abweichenden Aussagen der lokalen Übergabekopie sind widerlegt. Die unveränderte Unit-Baseline hatte 61 Tests mit 16 fehlgeschlagenen Format-Subtests (wiederholter JSON-Parse unter Windows). Die bestehende Seitensuite war grün. Ein CI-Vorlauf während der Umsetzung scheiterte an den vorhandenen Dokumentverweisen/Modullisten; er ist keine eingefrorene Baseline und wird nicht als grüner Nachweis ausgegeben.

**3.33.8, Windows / Python 3.14.8 / Tk 9.0.4:** Vollständige Nachprüfung **Exitcode 0: 84 automatische Schritte**, darunter 66 Integrationssuiten, 75 Unit-Tests, Showcase, fünf Analysen, Beispiel-/Release-Reproduktion und Windows-Bildaufnahme. [Grünes Originalergebnis](../tests/qa-3.33.8/windows_2026-10-05/voll_2/ergebnis.json). Titelbreiten, Mindesthöhen, Editor-Timerabbau und Windows-Formatcache korrigiert. Der erste Gesamtbericht hatte 66 grüne Integrationssuiten und einen fehlgeschlagenen Unit-Test; [erhaltenes Original](../tests/qa-3.33.8/windows_2026-10-05/voll/ergebnis.json). Der Inhaltsvergleich verhindert übersehene gleich große Formatwechsel bei identischen Dateizeiten. Alle 75 Unit-Tests bestehen zusätzlich mit Python 3.12.10.

**Python-Lieferung 3.33.8:** 16 Code-Dateien und 131 Ressourcen nach `07_Python-Versionen` SHA-256-abgeglichen; die Hauptdatei 3.33.6 liegt unverändert im Archiv. Showcase nach `05_Probelisten_Testdaten/Showcase` abgeglichen. Direkte Such-/Editor-Lieferproben und die CI-Grundstufe mit `--lieferstand-streng` sind grün. [CI-Ergebnis](../tests/qa-3.33.8/windows_2026-10-05/ci/ergebnis.json). [Nachweis](../tests/qa-3.33.8/windows_2026-10-05/README.md). Referenz-Mac, nativer Bundlebau und menschliche Abnahme bleiben offen.

**3.33.7, Windows / Python 3.12.10 / Tk 8.6:** Inhaltssuche und Formatsicherung implementiert; 72 Unit-Tests, Suchsuite und CI grün. Gegenprobe gegen Git-Stand 3.33.6 scheiterte erwartungsgemäß am fehlenden Seiteninhaltstreffer. Der zuerst diagnostisch beendete Volllauf hatte zwei überholte UI-/Font-Assertions. Nach deren Korrektur wurde ein vollständiges diagnostisches Ergebnis erzeugt: 56 von 65 Integrationssuiten grün, neun fehlgeschlagen; [Originalergebnis](../tests/qa-3.33.7/abnahme_windows_2026-10-05/ergebnis.json). Tk 8.6 erklärt SVG-/Touchpad-Befunde, weitere Testannahmen betrafen Windows-Menüs, Zeilenenden und noch nicht abgeschlossene Größenwechsel; echte Titel-/Höhenbefunde führten zu 3.33.8. Keine Lieferung von 3.33.7. Ursprung der Funktion und Fachmessung: [Nachweis](../tests/qa-3.33.7/suche_2026-10-05/README.md).

## Erhaltene Originalnachweise

| Version | Ergebnis | Automatische Schritte | Übersprungen | Original |
|---|---|---|---|---|
| 3.33.0 | Exitcode 0 (darwin, 2026-10-01T15:42:14) | 76 | 2 | Ergebnis (3.33.0: in der Git-Historie; außerhalb des Aufbewahrungsfensters) |
| 3.33.1 | Exitcode 0 (darwin, 2026-10-02T01:17:45) | 77 | 2 | [Ergebnis](https://github.com/n05a-design/glide-to-do/blob/267baab914c5dee5bdd85e8556288e82a711b0ea/01_Repository/Glide/tests/qa-3.33.1/abschluss_2026-10-01/vollpruefung_3/ergebnis.json) |
| 3.33.2 | Exitcode 0 (darwin, 2026-10-02T11:24:04) | 78 | 2 | [Ergebnis](../tests/qa-3.33.2/startseite_2026-10-02/vollpruefung/ergebnis.json) |
| 3.33.3 | Exitcode 0 (darwin, 2026-10-02T12:22:47) | 79 | 2 | [Ergebnis](../tests/qa-3.33.3/eingabe_2026-10-02/vollpruefung/ergebnis.json) |

Aktueller Windows-Originalbericht: 3.33.8, 05.10.2026, Exitcode 0, 84 automatische Schritte und eine offene Sichtprüfung (Link oben).

## Grenzen und Aufbewahrung

Ältere Prüfungen, Screenshots und doppelte Quellvorsicherungen wurden nach
dem Auftrag vom 03.10.2026 entfernt. Erhaltene Original-JSONs, Rohwerte und
Hashmanifeste bleiben unverändert; ihre früheren Dateipfade können entfernte
Artefakte benennen. Rohprotokolle bleiben lokal und sind nicht in Git.

Physische macOS-Bedienung, aktueller Referenz-Mac-/Linux-Volllauf, DPI/Mehrmonitor,
Tastatur/Screenreader, Installer/Signatur und echte Releaseverteilung bleiben
offen. Übersprungene Sichtprüfungen sind keine menschliche Freigabe.
Entwicklungsbundles mit Ad-hoc-Signatur sind keine öffentlichen Releases.

Die Projektbereinigung hat eigene Werkzeug-, Stand-/Link-, Dateibestand- und
Hashprüfungen; ihr Ergebnis steht im [Pflegestatus](DOKUMENTENPFLEGE.md).
Aufrufe und Kontrollmatrix: [Testplan](05_QA_TESTPLAN.md).
