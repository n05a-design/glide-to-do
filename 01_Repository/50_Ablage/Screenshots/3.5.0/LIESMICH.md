# Bildnachweise Glide 3.5.0

Stand: 05.09.2026

- `windows-abschluss/`: 16 Aufnahmen der UI-Suite, sechs der erweiterten
  Wiederholungsmaske bei 760 × 700 Pixeln, zwei der Releaseplanung. Alle 24
  wurden angesehen. Eigene Windows-Testfenster, Python 3.12.7, Tk 8.6.13.
- `windows-ausgang/`: zwei Bilder des Ausgangslaufs vor der redaktionellen Korrektur.
- `archiv/startseite_vorfassung_dunkel.png`: zusätzlich erhaltene Vorfassung,
  die entgegen dem Übergabebericht keine identische Dublette war.
- Die acht direkt hier liegenden PNG-Dateien bleiben Linux-Vorprüfungen.

Reale Maus-/Langzeitbedienung und weitere DPI/Monitore bleiben offen.
Details: [QA-Bericht](../../../01_Repository/Glide/docs/07_QA_BERICHT.md).

## Historische Beschreibung der Linux-Aufnahmen


**Diese Aufnahmen entstanden unter Linux mit Tcl/Tk 8.6 und DejaVu Sans, nicht
unter Windows.** Sie belegen Aufbau, Abstände, Farben und Zustände der
Oberfläche – nicht das Aussehen der Schriftzeichen auf einem Windows-Rechner.
Symbolformen sehen dort anders aus, weil für einen Teil der Zeichen eine
Ersatzschrift einspringt; welche das sind, beantwortet
`01_Repository/Glide/tests/tools/symbolpruefung.py` auf dem jeweiligen Rechner.

Die Windows-Abschlussaufnahmen liegen inzwischen unter `windows-abschluss/`.

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
