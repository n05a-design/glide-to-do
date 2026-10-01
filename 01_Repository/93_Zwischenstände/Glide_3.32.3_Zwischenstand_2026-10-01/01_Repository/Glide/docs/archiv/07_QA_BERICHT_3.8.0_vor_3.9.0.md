# QA-Bericht – Glide 3.8.0

Stand 12.09.2026 · macOS · Python 3.14.5

Der vollständige unveränderte 3.7-Ausgangslauf war erfolgreich: elf Suiten,
Syntax/Versionen/Dokumentation, zwei Analysen und Beispiel-/Releaseabgleich.
[Ausgangsprotokoll](../tests/qa-3.7.0/erinnerungen/ausgang/ergebnis.json).

Die Suite `test_reminders.py` ist erfolgreich: Migration/Originalkopie,
persistente einmalige Zustellung, Aufschub, Serien, Papierkorb, Restore, 25
verpasste Hinweise, Speicherfehler, Schreibschutz, lokale Zeitumstellung,
Zeitzonenwechsel, Hell-/Dunkeldialoge, Aktionsgeometrie, Suchaufhebung beim
Öffnen einer Aufgabe, die Aufmerksamkeit bei fälliger Erinnerung und echter
App-Neustart.

Der erste Gesamtlauf liegt unter `tests/qa-3.8.0/erinnerungen/erster_gesamtlauf`.
Der darauf folgende Lauf wurde während der manuellen Bedienwegprüfung von der
Korrektur an `open_task` eingeholt: acht Suiten liefen vor, vier nach der
Änderung. Er ist als Teillauf unter
`tests/qa-3.8.0/erinnerungen/abschluss_teillauf_vor_suchrandfall` erhalten und
gilt nicht als Abschluss.

**Der maßgebliche Abschlusslauf über den finalen Stand war erfolgreich**
(12.09.2026, 08:47–08:53 Uhr, Exitcode 0): 23 von 25 Schritten ausgeführt –
Syntax über 26 Quelldateien, Versionskonsistenz 3.8.0/Format 13, Dokumentation
mit 264 geprüften Dateiverweisen, Fixtures, Tk-Voraussetzung, alle zwölf Suiten,
beide Analysen sowie Beispiel- und Releaseabgleich. Übersprungen blieben allein
die plattformgebundene Screenshot-Erzeugung und die manuelle Sichtprüfung.
Er liegt vollständig nach der letzten Änderung des damaligen Stands.
[Protokoll](../tests/qa-3.8.0/erinnerungen/abschluss/ergebnis.json).

## Abschluss der Aufmerksamkeitsstufe

Die am 12.09.2026 ergänzte Aufmerksamkeit bei fälligen Erinnerungen (Stufe A)
entstand nach jenem Lauf und hat einen eigenen bekommen.

Ein erster Versuch schlug fehl – an einer falschen Erwartung in der neuen
Prüfung, nicht am Programm: Sie unterstellte, ein Speicherfehler bei der
Hintergrundzustellung erzeuge eine modale Fehlermeldung. `item_change` mit
`background=True` ruft `save_items(show_error=False)` und meldet bewusst über
die Statuszeile. Die Prüfung deckt nun genau das ab: keine modale Meldung,
Statuszeile meldet „nicht gespeichert", ein geglückter Folgelauf räumt sie weg.
Das Protokoll bleibt unter
`tests/qa-3.8.0/aufmerksamkeit/abschluss_testfehler_statuszeile`; elf Suiten,
beide Analysen und alle übrigen Schritte waren dort bereits erfolgreich.

**Der Abschlusslauf über den korrigierten Stand war erfolgreich**
(12.09.2026, 10:00–10:06 Uhr, Exitcode 0): dieselben 23 von 25 Schritten,
zwölf Suiten, beide Analysen, Beispiel- und Releaseabgleich. Er liegt
vollständig nach der letzten Änderung. Der geprüfte Quellstand ist über
[Prüfsummen](../tests/qa-3.8.0/erinnerungen/gepruefter_quellstand_sha256.json)
belegt; Code und startbare Arbeitskopie sind bytegleich.
[Protokoll](../tests/qa-3.8.0/aufmerksamkeit/abschluss/ergebnis.json).

Offen: native Sichtabnahme beider Plattformen – für die Aufmerksamkeitsstufe
insbesondere, ob das Dock unter macOS tatsächlich reagiert und die Taskleiste
unter Windows blinkt; die Suite belegt nur, dass die Plattformermittlung nicht
wirft. Ebenso offen: reales Schlafen/Aufwachen, Trackpad, weitere DPI/Monitore,
Screenreader, Installer und Signierung. Für den Langzeitbetrieb steht seit
12.09.2026 `tests/tools/dauerlauf.py` bereit; ein Ergebnis liegt noch nicht vor
und wird nach dem ersten vollen Lauf hier vermerkt. Tk-Widgettests und simulierte Zeitwechsel ersetzen diese Abnahmen
nicht. Systembenachrichtigungen bei geschlossenem Programm sind nicht implementiert.

[Funktions- und Datenvertrag](31_ERINNERUNGEN_3.8.0.md).
