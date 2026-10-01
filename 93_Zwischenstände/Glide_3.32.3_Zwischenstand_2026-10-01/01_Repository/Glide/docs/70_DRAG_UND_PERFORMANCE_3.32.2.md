# Drag-and-drop und Performance – Glide 3.32.2

Stand 30.09.2026 · Glide 3.32.2 · Aufgabenformat 20

Fortsetzung des Feature-/Performance-Auftrags: D04 und erster gemessener
Schnitt von P01/P02/P03/P05. Keine neue Laufzeitabhängigkeit, kein neues
Datenformat. Die nächste Featureetappe bleibt „Planen“ (3.33).

## Bedienvertrag D04

- Alle drei bestehenden Seitenleistenbäume verwenden dieselben Drag-Bindungen.
  Seiten und Notizen lassen sich umordnen, in Ordner verschieben und wieder
  auf die Hauptebene ziehen. Bibliotheken und Notizbücher lassen sich ebenfalls
  sortieren und verschachteln.
- Auf Inhaltszeilen entscheidet die obere/untere Hälfte über davor/danach.
  Auf Ordnern bleibt die Mitte das Ziel „hinein“; bei gezogenen Ordnern
  sortieren oberes und unteres Viertel davor/danach.
- Bei einem Wechsel zwischen Bereichen bleibt das Mausereignis am Quellbaum.
  Die Zielzone wird deshalb aus Bildschirmkoordinaten in Zielkoordinaten
  umgerechnet. Die Bewegungsgrenze berücksichtigt beide Richtungen.
- Ein neutraler Ordner-/Listenwechsel verändert weder Bearbeitungstag noch
  Fälligkeit. Im Notizbuch gilt weiterhin der bestehende Momentdatum-Vertrag:
  vorhandenes Datum erhalten, sonst Erstellungsdatum verwenden.
- Inhaltsarten bleiben erhalten. Ein unvereinbarer freier Typbereich oder
  ein Sortierziel auf dessen Hauptebene löst keine Konvertierung aus.
  Ordner dürfen weiterhin verschiedene Inhaltsarten aufnehmen.
- Ein Zug erzeugt einen gemeinsamen Undo-Schritt und nutzt `sidebar_change`
  sowie `guarded_structural_change`. Zyklen und zu tiefe Verschachtelung
  bleiben gesperrt. Klicks ohne Zug laufen weiterhin durch die native
  Treeview-Bedienung, insbesondere die Klapppfeile.

## Gemeinsame Bausteine und tatsächlicher Aufwand

1. `app_font`: Familie und Größenaufschlag werden je Tk-Interpreter
   zwischengespeichert. `apply_ui_font` invalidiert vor dem Umstellen.
   Getrennte Tk-Interpreter teilen keine Werte; ohne Tk wird kein Fenster
   implizit erzeugt. Schwache Schlüssel halten geschlossene Rootfenster nicht
   allein wegen des Caches am Leben. Stile und Schriftgrößen bleiben erhalten.
2. `ButtonFlow`: mehrere `add`-/Configure-Meldungen ergeben einen Layoutlauf
   im Leerlauf. Unveränderte Breite, Knöpfe, angeforderte Größen, Auswahl,
   Hintergrundfarbe und Abstände lösen keine erneuten Grid-Schreibvorgänge
   aus. Explizites `reflow` bleibt synchron. Zerstören bricht ausstehende
   Layouts ab. Umbruch und kompakte Werkzeugauswahl bleiben bestehen.
3. Datums- und Labelauswahl benutzen `bind_theme_hover`; bestehende
   Methoden und Signaturen bleiben als Wrapper erhalten. Die Hoverfarbe
   wird aus dem aktuellen Theme gelesen. Das verbessert Wartbarkeit,
   ohne dafür einen separaten Laufzeitgewinn zu behaupten.
4. Drop-Markierungen werden in allen drei Bereichen entfernt; unveränderte
   Zeilentags werden dabei nicht erneut geschrieben.

**Sofort lesende Layoutstellen:** Die Zeichenwerkzeuge messen die reservierte Kontextleistenhöhe innerhalb desselben Aufrufs. `build_context_row` schließt daher nach dem Hinzufügen synchron mit `row.reflow()` ab. Ohne diesen Abschluss sprang die Zeichenfläche beim Werkzeugwechsel; die Vollprüfung fand den Befund. Bestehende Rückmeldungssuite und neue Probe über drei Breiten verlangen weiterhin eine feste Flächenhöhe.

Keine pauschale Ersetzung von Datenschlüsseln oder Designwerten durch
Variablen. Der vorhandene Bildcache, atomare Speicherweg, Backups und Undo
bleiben maßgeblich. Hinweisgestaltung gemäß D06 unverändert.

## Messung

[Messwerkzeug](../scripts/pflege/messung_performance.py): isoliertes
`GLIDE_DATA_DIR`, ohne cProfile; feste Inhalte mit 12 Aufgabenlisten, einer
Notiz und einer Seite mit 50 Absätzen und zwei Bildern. 1400 × 950 Pixel,
drei Tk-Zeichendurchläufe je Wechsel. Erster Wechsel getrennt von 6–8
warmen Stichproben; Median, p95 und Einzelwerte im JSON. Vergleich auf
macOS/Python 3.14.5/Tk 9.0.3 mit gesichertem 3.32.1 und
[Quellstand 3.32.2](../tests/qa-3.32.2/drag_performance_2026-09-30/quellstand.json).

Bei 1.000 Aufgaben im Gesamtbestand:

| Vorgang | Vorher, Median ms | Nachher, Median ms | Änderung |
|---|---:|---:|---:|
| Startseite | 962,5 | 763,8 | -20,6 % |
| Bibliothek | 1409,3 | 962,3 | -31,7 % |
| Liste | 154,1 | 146,7 | -4,8 % |
| Tabelle | 127,7 | 127,0 | -0,5 % |
| Seite mit zwei Bildern | 369,1 | 207,6 | -43,8 % |
| Notiz | 375,1 | 259,9 | -30,7 % |
| 3.000 Schriftabfragen | 25,1 | 1,0 | -96,1 % |
| Erzeugung von 30 neuen Knöpfen | 410,6 | 443,5 | +8,0 % |

[Vorher 100](../tests/qa-3.32.2/drag_performance_2026-09-30/messung_vorher_100.json),
[nachher 100](../tests/qa-3.32.2/drag_performance_2026-09-30/messung_nachher_100.json),
[vorher 1.000](../tests/qa-3.32.2/drag_performance_2026-09-30/messung_vorher_1000.json),
[Abschlussnachmessung 1.000](../tests/qa-3.32.2/drag_performance_2026-09-30/messung_nachher_1000_final.json).

Die Abschlussnachmessung verwendet den finalen Anwendungshash einschließlich der Zeichenleistenkorrektur. Die 100-/10.000-Serien wurden davor im selben Performance-Schnitt gemessen; sie enthalten keine Zeichenwerkzeuge. Der vorherige Messquellstand bleibt archiviert.

Die Verbesserungen betreffen vor allem den Aufbau von Ansichten mit vielen
Werkzeugen. Liste/Tabelle sind weitgehend unverändert. Das Neuerzeugen von
Widgets bleibt teuer; weniger Layoutaufrufe bedeutet nicht automatisch
eine schnellere Erzeugung von 30 Knöpfen. Lokale Stichproben sind keine
allgemeinen Produktlatenzen und kein Nachweis für 60 FPS. Die Punktzahl
betrifft den Gesamtbestand, auf 12 Listen verteilt; keine Ansicht zeigt
10.000 Punkte gleichzeitig. Messvarianten mit Verlauf und Speicherverlauf
bleiben für P01 offen.

Zusätzlich [vorher 10.000](../tests/qa-3.32.2/drag_performance_2026-09-30/messung_vorher_10000.json) und [nachher 10.000](../tests/qa-3.32.2/drag_performance_2026-09-30/messung_nachher_10000.json): Bibliothek 1.426,4 → 987,2 ms, Bildseite 381,6 → 222,8 ms, Notiz 387,5 → 274,6 ms (Median). Liste/Tabelle bleiben weitgehend unverändert.

[Layoutaufwand ohne Zeitmessung](../tests/qa-3.32.2/drag_performance_2026-09-30/layout_aufwand.json) zählt getrennt von den Latenzserien die tatsächlichen Aufrufe beim Aufbau von 30 Knöpfen: Reflow 32 → 3, Grid-Schreibvorgänge für Knöpfe 525 → 60. Kein Profileraufwand in den Zeitwerten.

## Regression und verbleibende Arbeit

Neue Pflichtsuite
[`test_drag_performance3322.py`](../tests/integration/test_drag_performance3322.py):
echte Press-/Motion-/Release-Bindungen aller drei Bäume, unterschiedliche
Zielkoordinaten, Reihenfolge, Inhalte/IDs/Termine, Rückgängig, Notizbuchdatum,
Zyklenabwehr, Rückweg zur Hauptebene, keine Typkonvertierung und native
Klapppfeile. Dazu Schriftwechsel/Interpreter, Formatleistenumbruch,
kompakte Auswahl, längere Beschriftung, Fokusbeibehaltung und Zerstören vor
dem Leerlauf. Tk-Callbackfehler führen zum Fehlschlag.

`test_bilder330` und `test_befunde330` sind gezielt erneut grün: Bilder
einfügen, umfließen, Größe ziehen, verschieben, zurücknehmen und laden;
Rechtsklick/Formatierung und Seiten-/Notizblöcke. Die fünf Fotos belegen
weiterhin nicht den konkreten ursprünglichen Fehlerablauf. Kein neuer
Bildcache und keine unbelegte Behauptung, alle Foto-Befunde seien behoben.
Die vollständige Klappkontrolle bleibt Pflichtbestandteil.

Die [Vollprüfung](../tests/qa-3.32.2/drag_performance_2026-09-30/vollpruefung/ergebnis.json) ist mit Exitcode 0 abgeschlossen: 72 automatisierte Schritte,
57 Suiten und fünf Analysen. Der [Auslieferungsabgleich](../tests/qa-3.32.2/drag_performance_2026-09-30/abgleich.json) bestätigt 139 Python-Dateien und 53 Bundle-Dateien
per SHA-256 sowie die gültige Ad-hoc-Signatur. Ergebnis, Zeichnungsleistenkorrektur
und manuelle Grenzen stehen im [QA-Bericht](07_QA_BERICHT.md).
Physische Trackpad-/Mauswege, DPI, Screenreader und Windows/Linux bleiben
zur Plattformabnahme offen.

**Nächster Performance-Schnitt:** P03 unveränderte Karten erhalten und
gezielt aktualisieren, danach P04 Bildlayout/Platzierung und P06 redundante
Speicher-/Refresh-Anforderungen. Gemeinsame UI-Texte (Rest P05) nur nach
gleicher Bedeutung bündeln. P07 folgt zusammen mit G14.

**Nächste Features:** G01 Alltagssprache → G05 Fokus → G29 einzelne Aufgaben
in Notizen → G31/G32 Aufgabenwege/Filter → G02 mit ausdrücklich benanntem
Terminkontext. D01–D06 entschieden, D07 GIF-Umfang weiterhin offen.
