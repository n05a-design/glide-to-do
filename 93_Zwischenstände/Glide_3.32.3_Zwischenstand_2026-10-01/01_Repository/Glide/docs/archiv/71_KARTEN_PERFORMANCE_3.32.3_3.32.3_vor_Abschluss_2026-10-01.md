# Bibliothekskarten und gemeinsame Aktionen – Glide 3.32.3

Stand 01.10.2026 · Glide 3.32.3 · Aufgabenformat 20

Fortsetzung des bereits beauftragten Performance-Pakets P03 (A-01), mit einem belegten Doppel-Refresh aus P06 (A-03). Die zusätzliche Feature-Richtungsauswahl bleibt offen. Hinweisgestaltung, Datenformat und bestehende Speicherwege bleiben erhalten.

## Verhalten und Lebensdauer

`refresh_library_page` erhält Karten über `(Art, ID)` innerhalb desselben Bibliotheksrasters. Gleiche Vorschau: gleiche Karte, derselbe Öffnen-Button und gehaltene PhotoImages. Andere Reihenfolge: vorhandene Karten umordnen. Entfernte Einträge: zugehörige Karte zerstören. Geänderte Einträge: betroffene Karte ersetzen, übrige erhalten. Befehle verwenden stabile IDs, damit Undo oder neu geladene Python-Objekte keine veralteten Einträge öffnen.

Der gemeinsame Host `home_content` gehört jeweils der sichtbaren Ansicht. Beim Wechsel zur Startseite oder einer anderen Ansicht zerstört der bestehende Weg das Raster. Dessen Destroy-Bindung gibt `_library_card_cache` und gehaltene Vorschaubilder frei. Es gibt keine Wiederverwendung über zerstörte Ansichtshosts und kein Umparenten von Tk-Widgets.

Kartengröße, Archivansicht, vollständiges Theme, Schrift, Designname und Skalierung der Pixelsymbole bilden den Rasterkontext. Eine Änderung baut das Raster neu auf. Breitenänderungen verteilen vorhandene Karten auf die bestehenden Spalten. Die Configure-Bindung wird einmal pro Raster angelegt.

## Invalidierung

`library_card_preview` berechnet Aufgaben-/Ordnerdaten bei jeder Aktualisierung frisch. Gespeichert werden Widgets, keine dauerhaften Aufgaben- oder Terminzähler. Der vorhandene Durchgangscache und dessen Invalidierung bleiben erhalten.

Die Kartensignatur enthält Titel, Inhaltsart, Farbrolle, Ordnerpfad, Symbol, Zeichnungsinhalt, Notizvorschau, Labelnamen, sichtbare Aufgaben mit Termin/Wichtigkeit, restliche Einträge und Aufgabenstatistik. Ein Tageswechsel verändert Überfälligkeitszähler. Wenn sich ein Kind ändert, erhält auch die übergeordnete Ordnerkarte eine neue Vorschau, soweit ihre Anzeige betroffen ist.

Bei unverändertem Inhalt bleiben der vorhandene Tk-Fokusknopf und die Scrollposition erhalten. Eine geänderte Karte wird ersetzt; Fokusübernahme innerhalb ersetzter Karten bleibt ein eigener weiterer Schnitt. Die Hintergrundsuite prüft Tk-Fokuszustand und vorhandene Ziele, sie erzwingt keinen physischen macOS-Fokus.

## Gemeinsame Aktionsleiste und Archiv

`refresh_page_actions` überspringt den Aufbau nur bei identischen sichtbaren Specs (Text, Befehl, Farbrolle, Breite), Theme, Schrift und Design sowie denselben lebenden Kindern. Die bisherige Filterung der Importaktionen nach Höhenstufe erfolgt davor. Gleicher Text mit anderem Callable ersetzt die Knöpfe; wechselnde Ansichten mit neuen Lambdas dürfen neu aufbauen.

Beim tatsächlichen Neuaufbau wird die vorher registrierte Configure-Funktion abgemeldet. Die Leiste sammelt deshalb bei wechselnden Aktionen keine alten Tcl-Befehle an. Geometrie und Aktionswege bleiben erhalten.

„Zurückholen“ ruft `set_archived` auf. Dessen `sidebar_change(refresh_tree=True)` aktualisiert bereits zentral. Der zweite explizite `refresh_library_page` entfällt. Die native Knopfprobe zählt genau eine Aktualisierung. Atomare Speicherung, Backups, Sperre, Fehlerpfade und Undo werden nicht verzögert oder ersetzt.

## Messung

Identische temporäre Daten: 12 Aufgabenlisten mit insgesamt 100, 1.000 oder 10.000 Aufgaben, ein Ordner, eine Notiz, eine kleine Zeichnung. Fensteranforderung 1.400 × 950. Beide Fassungen laufen mit Python 3.14.5/Tk 9.0.3, ohne cProfile. Pro Aktion ein separat protokollierter Aufwärmdurchlauf, anschließend acht Rohwerte mit Median und empirischem p95.

Gemessen wird erneutes Rendern innerhalb einer bestehenden Bibliotheksansicht einschließlich drei Tk-Ereignisdurchläufen. „Aufgabenstatus“ ändert synthetische Daten unmittelbar; „Reihenfolge“ dreht die Listenfolge um. Das misst weder Dateischreiben noch Wechsel aus einer anderen Ansicht. Zusätzlich wird die Zahl neuer gerundeter Karten-/Aktionscontainer erfasst; deren Anzahl ist kein Zähler aller Tk-Kindwidgets.

| Aufgaben | Unverändert, Median/p95 ms vor → nach | Aufgabenstatus, Median/p95 ms vor → nach | Reihenfolge, Median/p95 ms vor → nach |
|---|---|---|---|
| 100 | 853,9/858,5 → 1,4/1,6 | 856,8/887,0 → 384,2/389,7 | 853,9/884,3 → 84,6/86,2 |
| 1.000 | 776,2/801,1 → 4,9/5,5 | 785,3/800,8 → 388,3/393,7 | 795,1/823,2 → 85,8/86,2 |
| 10.000 | 889,4/896,1 → 36,2/37,4 | 889,9/929,4 → 414,4/426,6 | 894,8/906,1 → 117,6/119,6 |

Neue Karten-/Aktionscontainer je warmem Durchlauf: vorher stets **17**, nachher unverändert **0**, Status **2** (Liste und Ordner), Reihenfolge **0**. Höhere Aufgabenanzahl bei gleicher Kartenzahl untersucht Berechnungskosten, keine Skalierung auf Tausende Karten.

Rohwerte und Quellhashes: [100 vorher](../tests/qa-3.32.3/karten_performance_2026-10-01/messung_vorher_100.json), [100 nachher](../tests/qa-3.32.3/karten_performance_2026-10-01/messung_nachher_100.json), [1.000 vorher](../tests/qa-3.32.3/karten_performance_2026-10-01/messung_vorher_1000.json), [1.000 nachher](../tests/qa-3.32.3/karten_performance_2026-10-01/messung_nachher_1000.json), [10.000 vorher](../tests/qa-3.32.3/karten_performance_2026-10-01/messung_vorher_10000.json), [10.000 nachher](../tests/qa-3.32.3/karten_performance_2026-10-01/messung_nachher_10000.json). Der erste Vorlauf ohne eigenen Aufwärmdurchlauf bleibt als `messung_vorher_1000_erstes_Z.json` erhalten und wird nicht mit der finalen Serie vermischt.

Keine festen Zeitassertions und kein allgemeines FPS-Versprechen. Datenberechnung bleibt abhängig vom Aufgabenbestand; Neuaufbau beim Ansichtswechsel und Startseitenkarten bleiben weitere Arbeit. Die Serien werden nacheinander ausgeführt; Hostlast und macOS-Geometrie beeinflussen Zeitwerte.

## Pflichtprüfung und Grenzen

`tests/integration/test_library_performance3323.py` ist im Vollmodus fest aufgenommen. Die gezielte Suite besteht: identische Karten/Knöpfe, betroffene Status-/Titel-/Label-/Notiz-/Bildkarten, Reihenfolge, neue Python-Objekte mit gleichen IDs, native Öffnen-/Zurückholen-Bedienung, Undo, Tageswechsel, Rasterbreiten, Kartengröße, Schrift, Design, leeres Archiv, neue/entfernte Inhalte und zerstörter Host. Zusätzlich gleiche Aktion mit geändertem Befehl, niedrige Höhenstufe und konstante Tcl-Callbackzahl. Alle Tk-Callbackfehler werden gesammelt und als Fehler gewertet.

**Vollprüfung und Auslieferung:** noch ausstehend. Der vorherige ausgelieferte Stand ist 3.32.2. Nach Vollprüfung folgen Abgleich der Python-Fassung, neues macOS-Bundle, SHA-256 und Signaturprüfung; [QA-Bericht](07_QA_BERICHT.md).

Windows/Linux, physische Maus-/Trackpadbedienung, DPI und Screenreader bleiben manuelle Abnahmen. Alle App-Tests und Messungen verwenden `GLIDE_DATA_DIR` vor dem Import. Echte Nutzerdaten und das persönliche Fehlerprotokoll wurden nicht gelesen. Die fünf Originalfotos sind ohne konkreten Ablauf weiterhin nicht pauschal als behoben markiert.

## Anschluss

P03 bleibt für Startseite, Aktualisierung einzelner Elemente geänderter Karten und große Kartenbestände offen. P04 trennt Bildgeometrie von Platzierung; P06 erfasst weitere doppelte Speicher-/Refresh-Anforderungen pro konkreter Aktion. Anschließend folgt die bestehende Featureplanung. Die zusätzliche Richtungsauswahl A–H und D07 bleiben offen; Empfehlungen ersetzen keine Entscheidung des Inhabers.
