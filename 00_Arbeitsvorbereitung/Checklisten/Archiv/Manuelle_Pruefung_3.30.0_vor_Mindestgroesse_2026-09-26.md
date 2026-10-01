# Manuelle Prüfung – Glide 3.30.0

Stand 25.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · ergänzt um drei Ausbauten (Stand 26.09.2026) · noch nicht ausgeführt

## Rahmen

- Diese Prüfung ergänzt die weiterhin offenen Prüflisten
  [3.29](Manuelle_Pruefung_3.29.0.md) und [3.28](Manuelle_Pruefung_3.28.0.md).
  Einige Punkte der 3.29-Liste sind überholt: Rückgängig gilt jetzt je Aktion,
  und es gibt mehr als eine Flächengröße.
- Geprüft wird mit einer Kopie oder einem isolierten `GLIDE_DATA_DIR`, nicht
  mit dem einzigen echten Datenbestand.
- Beim ersten Start über einem 3.29-Bestand prüfen, dass im Ordner `backups`
  die Datei `liste_vor_format20_<Zeitstempel>.json` entsteht.
- In der Agentenumgebung waren keine Bildschirmaufnahmen möglich. Die
  Darstellung wurde nur über Widgetgeometrie und automatisierte Tests geprüft
  ([Vertrag 3.30](../../01_Repository/Glide/docs/66_MODERNISIERUNG_3.30.0.md)).

## Migration und Rückfall

- [x] Ein echter Format-19-Bestand öffnet ohne Fehlermeldung. Listen,
      Notizen, Zeichnungen, Tagebuch, Papierkorb und Pinnwände sind
      vollständig. *Automatisch geprüft am 25.09.2026 mit einer Kopie des
      echten Bestands: 6 Seiten, 138 Punkte, 2 Pinnwände, Inhalt unverändert.*
- [x] Die Vorsicherung liegt bytegleich zur alten Datei im Ordner `backups`.
      *Automatisch geprüft, ebenfalls mit der Kopie.*
- **Warnung:** Glide 3.29 nach der Umstellung **nicht** mehr starten. Es hält
  Format 20 für beschädigt, beginnt leer und überschreibt den Bestand bei der
  ersten Eingabe (mit der Kopie nachgewiesen). Zurück nur über
  `liste_vor_format20_*.json` in einer getrennten Ablage.
- [ ] Die Startseite sieht nach dem Update aus wie vorher; die neuen Kacheln
      sind ausgeblendet und über „Startseite anpassen“ einblendbar.
- [ ] Nach dem Beenden mit Cmd+Q bzw. Alt+F4 öffnet der nächste Start in
      derselben Fenstergröße und -position.

## Pixel-Werkstatt mit Maus, Trackpad und Tastatur

- [ ] Je eine Zeichnung mit 16, 32, 64 und 128 Zellen anlegen. Die Fläche
      passt sich ein; Strg+Mausrad zoomt um den Zeiger, die mittlere Maustaste
      verschiebt.
- [ ] Linie, Rechteck und Ellipse ziehen, auch mit Umschalt (gerade bzw.
      quadratisch) und Alt (vom Mittelpunkt). Die Vorschau stimmt mit dem
      Ergebnis überein.
- [ ] Rechtsklick malt mit der zweiten Farbe; X tauscht, D setzt zurück. Die
      Farbleiste übernimmt zuletzt benutzte Farben.
- [ ] Symmetrie in allen drei Arten; Muster Schachbrett und Punktraster;
      Kachelvorschau; Pinsel über den Rand.
- [ ] Auswahl aufziehen, verschieben, kopieren, in eine andere Zeichnung
      einfügen. Glide-JSON aus der Zwischenablage einfügen, mit Vorschau.
- [ ] Strg/Cmd+Z nimmt je Aktion zurück (ein Pinselzug, eine Form, eine
      Füllung).
- [ ] Palette als .gpl exportieren, in Aseprite oder Pixelorama öffnen und
      zurück importieren.
- [ ] PNG-Export in 1×, 8× und der größten Stufe prüfen: harte Kanten, keine
      Glättung.
- [ ] Zwischenstand merken, weiterzeichnen, wiederherstellen.
- [ ] Pixelsymbol an Liste und Ordner zeichnen. Es erscheint in Seitenleiste,
      Übersicht und Suche und ist bei 100 %, 150 % und 200 % Skalierung scharf.

## Startseite, Seitenleiste, Suche

- [ ] „Startseite anpassen“: Kacheln ziehen, Alt+↑/↓, ganze Breite,
      ausblenden, wieder einblenden. Das Ergebnis überlebt einen Neustart.
- [ ] Seite und gespeicherten Filter anheften. Ein Filtertreffer lässt sich
      in der Kachel abhaken.
- [ ] Seitenleiste: Ansichten, Angeheftet sowie Listen und Ordner einklappen.
      „+“ und „…“ erscheinen beim Überfahren eines Ordners ohne Springen der
      Zeilen; Ziehen in der Seitenleiste funktioniert unverändert.
- [ ] Strg/Cmd+O: Seite, Punkt und Aktion finden, mit Umlauten und
      ae/oe/ue-Schreibweise.
- [ ] Pfadzeile anklicken; die Chipzeile stimmt mit dem Inhalt überein.
- [ ] Tagesbeginn einmal vollständig durchgehen, Wochenrückblick vor und
      zurück blättern.

## Pinnwand als Board

- [ ] Spaltenboard nach jedem Feld. Karten mit der Maus in andere Spalten
      ziehen und die Wirkung in Liste, Tabelle und Kalender prüfen (Datum,
      Uhrzeit, Wiederholung, Labels).
- [ ] Alt+←/→ verschiebt per Tastatur; „Überfällig“ lehnt ab.
- [ ] 500 Karten: Scrollen und Ziehen bleiben flüssig.
- [ ] Karteninhalt und Kartenfarbe umschalten, auch im Kontrastdesign
      (Formen je Farbe).
- [ ] Zeichnung als Karte anheften; Doppelklick öffnet sie, „Zurück zur
      Pinnwand“ kehrt zurück.
- [ ] Bereich anlegen, am Kopf ziehen (Karten wandern mit), Größe ändern,
      umbenennen (F2), entfernen – und jeweils Strg/Cmd+Z.
- [ ] Aufräumen, Strg/Cmd+Enter für eine neue Karte, Ziehpunkt verbinden;
      Verbindung beschriften, stricheln, einfärben.
- [ ] Hintergrund Punkte, Linien und Karo bei 50 % und 200 % Zoom: kein
      Ruckeln, lesbarer Kontrast. Druck mit und ohne Hintergrund.
- [ ] Präsentation: Bereiche als Folien, blättern, Escape.

## Liste, Tabelle, Tagebuch, Planung

- [ ] Liste und Tabelle gruppieren. Zwischen Abschnitten ziehen; Abschnitte
      zuklappen und neu starten.
- [ ] Tabelle verschachtelt mit Suche: Elternpunkte bleiben abgeschwächt
      stehen.
- [ ] Tagebuch: Notiz, Liste, Zeichnung und Pinnwand anlegen, Momentdatum
      wählen. Tag- und Von-bis-Filter zusammen mit der Suche verwenden.
- [ ] Verknüpfen, „wartet auf“ und Abhaken eines wartenden Punkts;
      Zeiterfassung starten, Glide beenden, neu starten, stoppen.
- [ ] Mein Tag mit Uhrzeiten: Zeitplan und Überschneidungshinweis.
- [ ] Vorlage mit `{{Projektname}}` und `{{Datum}}` speichern und verwenden.
- [ ] Archivieren und Zurückholen einer Liste und eines Ordners.

## Ausbau vom 25.09.2026

- [ ] „Mein Tag“: einen Block auf die obere bzw. untere Hälfte eines anderen
      ziehen, einen Punkt aus „Ohne Uhrzeit“ auf die Kopfzeile „Zeitplan“
      ziehen, einen Block nach „Ohne Uhrzeit“ ziehen; Alt+↑/↓; jeweils
      Strg/Cmd+Z.
- [ ] Pinnwand › Aktionen › „Präsentation als PDF …“: Die Druckseite öffnet im
      Browser, je Bereich eine Seite quer; als PDF sichern und lesen. Dasselbe
      mit „Folien als PDF …“ im Notizmenü.
- [ ] Eine Karte mit der Maus und mit Alt+Pfeil verschieben, dann Strg/Cmd+Z.
- [ ] Detailbereich: Art, Farbe, Wiederholung (auch Wochentage), Erinnerung,
      erfasste Zeit, Checkliste und Beziehungen ändern; mit Mausrad und
      Trackpad scrollen; Wechsel zu „Gruppe“ fragt nach.
- [ ] Gismo steht neben leerer Liste, leerem Ordner und leerer Pinnwand; nach
      „Spielereien aus“ ist er überall weg.
- [ ] Design „Pixel“: Seitentitel und Kachelköpfe in „Pixelify Sans“, Umlaute
      und ß korrekt, scharf bei 100, 150 und 200 % – unter macOS und Windows.

## Zweiter Ausbau vom 26.09.2026

- [ ] Detailbereich: Datei anhängen, per Klick öffnen, mit „×“ entfernen,
      Strg/Cmd+Z.
- [ ] „Mein Tag“ › „Raster“: Blöcke mit Maus und Trackpad ziehen,
      Überschneidungen nebeneinander, Doppelklick öffnet den Punkt, Rückgängig.
- [ ] Pinnwand mit Zeichnungskarte als PDF drucken und als Folien ausgeben:
      Die Zeichnung ist scharf, nicht verwaschen.
- [ ] Liste mit Zwischenüberschriften gruppieren: Überschriften stehen im
      Abschnitt, die Nummern stimmen mit der ungruppierten Liste überein.
- [ ] Windows-Vollprüfung nach [Windows-Prüfung 3.30](Windows_Pruefung_3.30.0.md).

## Dritter Ausbau vom 26.09.2026

- [ ] „Mein Tag“ mit Raster: einen Punkt aus „Ohne Uhrzeit“ und einen aus
      dem Eingang ins Raster ziehen. Die gestrichelte Linie zeigt die Zeit,
      der Punkt landet dort, Strg/Cmd+Z nimmt es zurück.
- [ ] Tabelle einer Liste mit Zwischenüberschriften gruppieren: Nummern in
      der schmalen linken Spalte wie in der Liste, Überschriften als
      Trennzeilen; nach einer Spalte sortiert verschwinden die Überschriften.
- [ ] In der Tabelle „Ansicht › Pinnwand › Pinnwand öffnen“: Die Pinnwand der
      Liste öffnet sich ohne Hinweis.
- [ ] Unter Linux (falls verfügbar): Design „Pixel“ zeigt den Seitentitel in
      „Pixelify Sans“, ohne dass die Schrift installiert ist.

## Oberfläche und Zugänglichkeit

- [ ] Detailbereich einschalten: Felder bearbeiten, die Auswahl wechseln
      (keine Eingabe geht verloren), Breite ziehen, Fenster unter 980 px.
- [ ] Leerzustände: leere Liste, leerer Ordner, leeres Tagebuch, leere Suche,
      leerer Papierkorb, leere Pinnwand – je eine sinnvolle Hauptaktion.
- [ ] Design „Pixel“ auf allen Seiten, Hell/Dunkel-Schalter, Kontrastdesigns.
- [ ] Bildschirmleser (NVDA oder VoiceOver): Seitenleiste, Suche,
      Detailbereich, Anpassen-Modus der Startseite.
- [ ] Windows 11 und macOS mit 100 %, 150 % und 200 % Skalierung sowie zwei
      Monitoren.

## Nicht durch Agenten prüfbar

- Signatur, Notarisierung und Installer.
- Markenprüfung.
- Store-Freigabe.
