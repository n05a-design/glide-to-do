# Abschlussbericht – historischer Glide-3.8-Nachweis

Dieses Dokument ist ein abgeschlossener Nachweis und wird nicht nachgezogen. Der aktuelle Stand steht im [Dokumentationsindex](00_INDEX.md) und im [QA-Bericht](07_QA_BERICHT.md). Die folgenden Befunde gehören zum jeweils angegebenen älteren Stand.

Dieser Bericht dokumentiert den damaligen Erinnerungsstand. Der heutige
Prüfstand steht im [QA-Bericht](07_QA_BERICHT.md), die jüngste Bedienergänzung
in [Kalenderimport aus ICS](45_KALENDERIMPORT_3.21.0.md).

Stand: 12.09.2026 · unveröffentlichter Entwicklungsstand · Aufgabenformat 13

## Ergebnis

Die erste priorisierte Stufe der **lokalen Erinnerungen** ist umgesetzt. In den
Punktdetails stehen feste einmalige Zeitpunkte und Abstände zur Fälligkeit zur
Wahl; ohne Fälligkeitsuhrzeit gilt sichtbar 09:00 Uhr. Eine gemeinsame Übersicht
bündelt geplante, verschobene, offene/verpasste und bestätigte Hinweise und
trennt Aufgabe öffnen, Erinnerung verschieben, Aufgabe erledigen und Hinweis
bestätigen als eigene Aktionen. Ein Aufschub ändert keine Frist, eine Bestätigung
erledigt keine Aufgabe. „Aufgabe öffnen“ hebt eine aktive Suche auf und markiert
die Aufgabe in ihrer Quellliste.

Eine neu zugestellte Erinnerung hebt seit dem 12.09.2026 zusätzlich den Eintrag
in der Taskleiste beziehungsweise im Dock hervor – einmal je Prüflauf, erst nach
gespeichertem Zustellbeleg, ohne das Fenster nach vorn zu reißen, abschaltbar in
den persönlichen Einstellungen. Eine echte Systembenachrichtigung ist das
ausdrücklich nicht; sie setzt eine registrierte, installierte Anwendung voraus
([Entscheidung](decisions/SYSTEMBENACHRICHTIGUNGEN.md)).

Gespeicherte Zustellbelege verhindern Doppelzustellungen über Neustart,
Zeitumstellung und Zeitzonenwechsel hinweg. Relative Hinweise folgen der
bestehenden Serienlogik, feste einmalige Zeitpunkte werden beim Vorrücken der
Serie entfernt. Aufgabenformat 13 ergänzt pro Punkt eine Erinnerungskonfiguration;
vor dem ersten Überschreiben einer älteren Datei entsteht eine unrotierte
bytegleiche Originalkopie, und ohne diese Sicherung wird nicht gespeichert.
[Funktions- und Datenvertrag](31_ERINNERUNGEN_3.8.0.md).

Der 3.7-Bestand bleibt unverändert erhalten: isolierter Vorlageneditor mit 16
Praxisvorlagen, thematisierte Mac-Auswahlfelder und die dynamische Kachelübersicht.
[Funktionsübersicht](25_FEATURE_ABGLEICH_3.7.0.md) · [Kacheln](29_DYNAMISCHE_KACHELN_3.7.0.md).

## Nachweise und Grenzen

Der vollständige Lauf auf macOS/Python 3.14.5 bestand mit Exitcode 0: zwölf
Testsuiten einschließlich der neuen `test_reminders.py`, zwei statische Analysen,
Syntax-, Versions- und Dokumentationsprüfung sowie Beispiel- und Releaseabgleich.
Übersprungen blieben allein die plattformgebundene Screenshot-Erzeugung und die
manuelle Sichtprüfung. Die danach ergänzte Aufmerksamkeitsstufe hat einen eigenen
Abschlusslauf mit demselben Ergebnis; beide sind im [QA-Bericht](07_QA_BERICHT.md)
nachgewiesen. Automatisiert ist 3.8.0 damit vollständig abgenommen.

Hinweise sind Anzeigen innerhalb der laufenden App. Bei beendetem Programm,
Abmeldung, Ruhezustand oder ausgeschaltetem Gerät erfolgt keine Zustellung;
nach Rückkehr erscheinen vergangene Zeitpunkte gesammelt. Systembenachrichtigungen
sind nicht implementiert und dürfen nicht als vorhanden dargestellt werden.
Native Sichtabnahme beider Plattformen, reales Schlafen/Aufwachen, physisches
Trackpad, weitere DPI/Monitore, Screenreader, Langzeitbetrieb, ein echter
Windows-Systemlauf, Installer und Signierung bleiben offen. Es wurden keine
echten Nutzdaten für Prüfungen verwendet.

- [Vollständiger Abschlusslauf](../tests/qa-3.8.0/erinnerungen/abschluss/ergebnis.json)
- [Abschlusslauf der Aufmerksamkeitsstufe](../tests/qa-3.8.0/aufmerksamkeit/abschluss/ergebnis.json)
- [Code-/Arbeitskopie-Prüfsummen](../tests/qa-3.8.0/erinnerungen/gepruefter_quellstand_sha256.json)
- [Erster Gesamtlauf](../tests/qa-3.8.0/erinnerungen/erster_gesamtlauf/ergebnis.json)
- [QA-Bericht](07_QA_BERICHT.md) · [Projektübergabe](09_PROJECT_HANDOFF.md)
- Die jeweils aktuelle startbare Arbeitskopie benennt die [Projektübergabe](09_PROJECT_HANDOFF.md); ein fester Dateiname gehört nicht in einen abgeschlossenen Nachweis.

Nächste Schritte damals – Reiteransicht und Pinnwand sind seit 3.10.0 umgesetzt: native Abnahme der ersten Stufe, danach Entwurf der
Plattformintegration für Systembenachrichtigungen mit ausdrücklich festgelegten
Betriebszuständen, anschließend Reiteransicht und Pinnwand für dieselben
Aufgabenobjekte. Die bisherigen Word-Berichte liegen im äußeren
`10_Dokumentation/Archiv/` und bleiben historische Nachweise; verbindlicher
Einstieg sind die aktuellen Markdown-Dokumente im [Dokumentationsindex](00_INDEX.md).
