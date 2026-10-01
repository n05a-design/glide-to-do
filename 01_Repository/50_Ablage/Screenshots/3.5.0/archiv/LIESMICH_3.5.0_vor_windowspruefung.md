# Bildnachweise 3.5.0 – Vorprüfung unter Linux

**Diese Aufnahmen entstanden unter Linux mit Tcl/Tk 8.6 und DejaVu Sans, nicht
unter Windows.** Sie belegen Aufbau, Abstände, Farben und Zustände der
Oberfläche – nicht das Aussehen der Schriftzeichen auf einem Windows-Rechner.
Symbolformen sehen dort anders aus, weil für einen Teil der Zeichen eine
Ersatzschrift einspringt; welche das sind, beantwortet
`01_Repository/Glide/tests/tools/symbolpruefung.py` auf dem jeweiligen Rechner.

Die maßgeblichen Windows-Aufnahmen entstehen im Vollmodus des Prüflaufs und
gehören anschließend ebenfalls hierher.

| Datei | Zeigt |
|---|---|
| 01_startseite_oben_hell.png | Kopfzeile mit Uhr, Willkommenskachel, Tagesziel, Schnellzugriffe |
| 02_startseite_unten_hell.png | Zuletzt bearbeitet, Vorlagen, Bestand mit 7-Tage-Diagramm |
| 06_startseite_oben_dunkel.png | dieselbe Ansicht im dunklen Theme |
| 07_startseite_unten_dunkel.png | unterer Teil im dunklen Theme |
| 08_einstellungen_dunkel.png | Textlogo mit Farbwahl und Vorschau, tägliche Herausforderung |
| 09_eingabe_wiederholung_dunkel.png | Wiederholung mit Wochentagen und Enddatum |
| 10_liste_faelligkeit_dunkel.png | Fälligkeitsspalte mit Datum und Uhrzeit, vollständig |
| 11_liste_schmal_860_dunkel.png | schmales Fenster: Labels und Fälligkeit weichen |

Die Testdaten sind erfunden; es wurden keine echten Nutzerdaten verwendet.
`GLIDE_DATA_DIR` war für jeden Lauf auf ein isoliertes Verzeichnis gesetzt.

Das Prüfprotokoll dieses Laufs liegt unter
`01_Repository/Glide/tests/qa-3.5.0/linux-vorpruefung/`.
