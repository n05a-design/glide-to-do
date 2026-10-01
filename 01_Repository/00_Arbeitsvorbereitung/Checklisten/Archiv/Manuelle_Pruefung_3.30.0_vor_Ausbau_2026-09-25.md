# Manuelle Prüfung – Glide 3.30.0

Stand 25.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · noch nicht ausgeführt

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

- [ ] Ein echter Format-19-Bestand öffnet ohne Fehlermeldung. Listen, Notizen,
      Zeichnungen, Tagebuch, Papierkorb und Pinnwände sind vollständig.
- [ ] Die Vorsicherung liegt bytegleich zur alten Datei im Ordner `backups`.
- [ ] Glide 3.29 (Archivkopie) lehnt den neuen Bestand sichtbar ab und
      verändert ihn nicht.
- [ ] Die Startseite sieht nach dem Update aus wie vorher; die neuen Kacheln
      sind ausgeblendet und über „Startseite anpassen“ einblendbar.

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
