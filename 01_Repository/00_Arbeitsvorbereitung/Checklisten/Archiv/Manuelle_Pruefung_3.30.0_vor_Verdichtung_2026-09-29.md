# Manuelle Prüfung – Glide 3.30.0

Stand 27.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · ergänzt um drei Ausbauten (26.09.2026), das Aufräumen, die Kompression sowie Tk 9, Bilder in Seiten und feste Bestandteile (27.09.2026) · noch nicht ausgeführt

## Rahmen

- Diese Prüfung ergänzt die weiterhin offenen Prüflisten
  [3.29](Manuelle_Pruefung_3.29.0.md) und [3.28](Manuelle_Pruefung_3.28.0.md).
  Einige Punkte der 3.29-Liste sind überholt: Rückgängig gilt jetzt je Aktion,
  und es gibt mehr als eine Flächengröße.
- Geprüft wird mit einer Kopie oder einem isolierten `GLIDE_DATA_DIR`, nicht
  mit dem einzigen echten Datenbestand.
- Beim ersten Start über einem 3.29-Bestand prüfen, dass im Ordner `backups`
  die Datei `liste_vor_format20_<Zeitstempel>.json` entsteht.
- Seit dem 27.09.2026 nimmt der Agent Bildschirmfotos nur vom eigenen
  Glide-Fenster auf (mit künstlichen Daten). Sie ersetzen die Prüfung am
  echten Gerät nicht: Maus, Trackpad, DPI, Windows und Bildschirmleser
  bleiben hier offen
  ([Vertrag 3.30](../../01_Repository/Glide/docs/66_MODERNISIERUNG_3.30.0.md)).

## Migration und Rückfall

- [x] Ein echter Format-19-Bestand öffnet ohne Fehlermeldung. Listen,
      Notizen, Zeichnungen, Notizbücher, Papierkorb und Pinnwände sind
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

## Liste, Tabelle, Notizbuch, Planung

- [ ] Liste und Tabelle gruppieren. Zwischen Abschnitten ziehen; Abschnitte
      zuklappen und neu starten.
- [ ] Tabelle verschachtelt mit Suche: Elternpunkte bleiben abgeschwächt
      stehen.
- [ ] Notizbuch: Notiz, Liste, Zeichnung und Pinnwand anlegen, Momentdatum
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

## Kleine Fenster vom 26.09.2026

- [ ] Fenster ganz zusammenschieben (860 × 700): In Liste, Tabelle, „Mein
      Tag“, Pinnwand und „Listen und Ordner“ ist nichts angeschnitten oder
      gequetscht. Mit markierten Punkten stehen unten mindestens Wichtigkeit,
      Fällig und Löschen; alles Weitere über „⋯“, Kontextmenü und Kürzel.
- [ ] Fenster breiter ziehen: Die Auswahlleiste zeigt dann alle fünf Knöpfe
      und die Anzahl. (Die festen Aktionsreihen und „Liste importieren“ unter
      dem Baum gibt es seit dem 27.09.2026 nicht mehr.)
- [ ] Dasselbe mit Schriftgröße „groß“ und im Design „Pixel“.
- [ ] Gruppierte Tabelle nach einer Spalte sortieren: Die Überschriften
      bleiben, sortiert wird darunter.

## Dialoge, Kontrast, Raster, Paketierung vom 26.09.2026

- [ ] Kalender (Monat) bei kleinem Fenster: Einträge enden mit „…“, volle
      Tage zeigen „+N“ neben der Zahl, der Hinweis oben bricht um.
- [ ] „In Liste verschieben …“ öffnet die Auswahl mit farbigen Listen.
- [ ] Punktmaske schmal ziehen: Der Kalenderknopf neben dem Datum bleibt
      vollständig.
- [ ] Design „Hell“ und „Glas hell“: Grün, Orange und Türkis wirken tiefer,
      bleiben aber erkennbar dieselben Farben. In „Pixel“, „Dopamin“ und den
      dunklen Designs beim Überfahren der Knöpfe dunkle statt weißer Schrift
      auf hellen Flächen.
- [ ] „Mein Tag“ mit Raster in einem Fenster unter 900 Pixeln: Das Raster
      steht statt der Liste, „Raster“ schaltet zurück.
- [ ] Einen Punkt aus einer normalen Liste auf „Mein Tag“ in der
      Seitenleiste ziehen: Er bleibt in seiner Liste und erscheint in „Mein
      Tag“; Strg/Cmd+Z nimmt das zurück.
- [ ] macOS: im Ordner `01_Repository/Glide` den Befehl
      `python3 packaging/macos/baue_app.py --ziel build/macos` ausführen und
      `build/macos/Glide.app` starten. Im Dock steht „Glide“ mit Symbol, nicht
      „Python“. Achtung: Das Bundle nutzt die echten Daten.

## Hintergrundverläufe vom 26.09.2026

- [ ] Einstellungen › Hintergrund: In „Liquid Glass“ (hell und dunkel) und
      „Pixel“ je zwei Verläufe wählen. Der Verlauf liegt hinter Kopfzeile,
      Rand und Zwischenräumen, Karten bleiben ruhig, der Titel gut lesbar.
- [ ] Fenster vergrößern und verkleinern, Seitenleiste ein- und ausblenden,
      auf der Startseite scrollen: keine Kanten, Versätze oder alten
      Bildreste.
- [ ] Schriftgröße „groß“ und das Kontrastdesign mit Verlauf.
- [ ] Unter Windows: dieselben Punkte – dort ist die Darstellung noch
      ungeprüft.

## Rückmeldung vom 26.09.2026

- [ ] Hell, Liquid Glass und Verlauf bei schmalem Fenster: Glide startet
      (war der Absturz).
- [ ] Milchglas: Kacheln, Liste und Seitenleiste tragen die Farbe des
      Verlaufs dahinter, keine Kästen hinter Texten. Einen Dialog öffnen –
      etwa den Kalender – und prüfen, dass er sich mittönt.
- [ ] Hinweistexte (über der Knopfleiste, unter dem Titel) ohne Kasten und
      gut lesbar.
- [ ] Kopfzeile: ◷ öffnet den Verlauf. Das Zahnrad bleibt nach dem
      Verkleinern und Vergrößern ganz rechts.
- [ ] „Mein Tag“: „In Bearbeitung“ steht unter den Aufgaben des Tages; ein
      Doppelklick auf die Überschrift öffnet die ganze Ansicht.
- [ ] Zeichenfläche: Raster, Vorschau und Werkzeuge umschalten – die Fläche
      bleibt stehen. Mit „Auswahl“ neben die Auswahl klicken hebt sie auf;
      über der Auswahl zeigt der Zeiger das Verschieben.
- [ ] Unterkanten: Seitenleiste und rechter Bereich enden in jeder Ansicht
      auf einer Linie.

## Zweite Rückmeldung vom 26.09.2026

- [ ] Mit Verlauf: Punktdetails (F2) und „Erweitert“ öffnen in voller Größe,
      alle Felder sind bedienbar.
- [ ] Dialoge (Schnellerfassung, Aktionen, Neue Liste) haben einen ruhigen,
      einheitlichen Grund, ohne Streifen.
- [ ] Farben: Grün nur bei Hinzufügen, Speichern, Anlegen und Erledigt; Rot
      bei Löschen und Leeren; alles andere grau.
- [ ] Papierkorb und „Mein Tag“ ohne Eingabezeile; der Leertext bricht um.
- [ ] „Erledigte Punkte löschen“ im Menü „Bearbeiten“; die Punkte stehen
      danach im Papierkorb.
- [ ] Startseite mit Verlauf flüssig scrollen; keine Knöpfe verschwinden.
- [ ] `07_Python-Versionen/Schnellstart.pyw` zweimal starten: Der zweite Start
      ist spürbar schneller.

## Seiten und Ordnertypen vom 26.09.2026

- [ ] Einen KI-Bericht (Markdown) kopieren und in „Seiten“ auf „Aus
      Zwischenablage“ klicken: Überschriften, Listen, Tabelle, Zitat, Code
      und Links stehen sauber da, „- [ ]“ ist ein Kästchen.
- [ ] Lange Seite endlos scrollen: flüssig, gut lesbar.
- [ ] Tippen: „## “, „- “, „1. “, „[] “, „> “; „/“ am Zeilenanfang; Enter in
      Listen und Aufgaben.
- [ ] Aufgabe abhaken; per Doppelklick Fälligkeit setzen; sie erscheint in
      „Mein Tag“. Aufgabenzeile löschen, dann Befehl+Z.
- [ ] „Mehr › Als Markdown speichern …“ und in einem anderen Programm öffnen.
- [ ] Neuer Ordner: Ordnerart „Bibliothek“ wählen und darin einen Eintrag
      anlegen – er wird eine Seite.

## Aufräumen, Seitenbereich und Galerie vom 27.09.2026

- [ ] Liste öffnen, einen Punkt markieren: Die Auswahlleiste erscheint unten
      (Anzahl, Wichtigkeit, Fällig, Einplanen, Labels, Löschen) und
      verschwindet ohne Auswahl wieder.
- [ ] Kopfzeile: ⌘ öffnet die Aktionen, ↯ die Schnellerfassung, ⍾ zeigt die
      Zahl offener Hinweise. Kennzahlen stehen nur unter dem Titel.
- [ ] „+“ neben „Listen“: Anlegen-Menü samt „Listen importieren …“. Über
      einer Listenzeile erscheint „…“ mit Bearbeiten und Löschen.
- [ ] Liste · Tabelle · Pinnwand umschalten; die offene Ansicht ist
      hervorgehoben.
- [ ] Pinnwand im breiten Fenster: Aktionen und Schalter in einer Zeile. In
      der Spaltenansicht passen alle Spalten, solange sie mindestens 220
      Pixel breit bleiben.
- [ ] „Startseite anpassen“ mit Verlauf: kein Kasten hinter Überschrift,
      Hinweis und „AUSGEBLENDET“. Gismo auf einer Akzentkachel anklicken:
      kein Rechteck um ihn.
- [ ] Punkt abhaken: „Erledigt!“ steigt unten auf, das Suchfeld bleibt frei.
- [ ] Einstellungen öffnen: Die Akzentfarbe steht oben neben dem Textlogo;
      das Logo übernimmt sie.
- [ ] „Seiten +“: neue Seite, Seite aus Vorlage (Bericht, Besprechung,
      Projektseite), neue Bibliothek. Eine Seite als Vorlage speichern und
      daraus eine neue anlegen – die Aufgaben sind abhakbar.
- [ ] Eine Bibliothek als Glide-Seiten exportieren und wieder importieren.
- [ ] Neue Galerie: PNG- und JPEG-Bilder hinzufügen; Kachelgrößen; Doppelklick
      für die Großansicht, Titel und Notiz eintragen, ◀ ▶; ein Bild entfernen
      und „Rückgängig“.

## Kompression vom 27.09.2026

- [ ] Beim ersten Start mit dem echten Bestand: Die Meldung „Titel gekürzt“
      nennt zu lange Titel (etwa „2. ✓ Objektdaten …“), und im Ordner
      `backups` liegt `liste_vor_titelkuerzung_…json`.
- [ ] Liste umbenennen: Mehr als 40 Zeichen lassen sich nicht eingeben, der
      Zähler zeigt „n / 40“.
- [ ] Kopf: keine Zeile „Beschreibungstext hinzufügen …“ mehr; eine kurze
      Beschreibung steht hinter den Kennzahlen.
- [ ] Pfeile vor „Seiten“ und „Listen“ klappen ein und aus; der Abstand
      zwischen beiden ist klein.
- [ ] Bibliothek öffnen: Tabelle mit Titel, Beschreibung, Farbe, Labels,
      Aufgaben, Erstellt; Spaltenköpfe sortieren.
- [ ] Menüs und Vorlagen sagen „Notizbuch“; ein neuer Tageseintrag heißt
      „Tagesnotiz · Datum“.
- [ ] Notizseite: Text, Werkzeugleiste und Knöpfe darüber stehen auf einer
      Linie.
- [ ] „Anzeige“ und andere Knöpfe mehrmals überfahren und anklicken: immer
      nur ein Hinweis, kein gestapelter Schatten, nichts fliegt durchs
      Fenster.

## Tk 9, Bilder in Seiten und feste Bestandteile vom 27.09.2026

Am einfachsten mit dem Rundgang: `05_Probelisten_Testdaten/Glide-Rundgang_3.30.0.glidebackup`
über Datei › Listen/Ordner hinzufügen … einlesen.

### Laufzeit

- [ ] Hilfe › Über Glide bzw. ein Python-Aufruf: Glide läuft mit Python 3.14
      und Tk 9. Unter Windows nach der Installation von Python 3.14 erneut
      starten; mit Python 3.13 (Tk 8.6) startet Glide ebenfalls, nur ohne
      Systemmitteilung und SVG-Vorschau.

### Feste Bestandteile

- [ ] Nacheinander Aufgabenliste, Liste in einem Unterordner, Notiz,
      Zeichnung, Seite, Galerie, Ordner, Pinnwand, Tabelle und „Mein Tag“
      öffnen: Seitenleiste, Kopfzeile, Kopfknöpfe und die Oberkante der
      Inhaltsfläche stehen still, nichts springt.
- [ ] Über dem Titel steht nie ein Ordnerpfad.
- [ ] Die Unterkante der Inhaltsfläche steht in allen Ansichten gleich.
      Darunter steht der Hinweis bzw. in Pinnwand, Seite, Zeichnung und
      Galerie ein eigener kurzer Hinweis, auf der Linie der Seitenleiste.
- [ ] In einer Liste einen Punkt markieren: Die Auswahlleiste erscheint an
      der Stelle des Hinweises, die Liste wird nicht kürzer. Auswahl
      aufheben: Der Hinweis ist zurück.
- [ ] Dasselbe im schmalen Fenster (860 × 700) und mit Schriftgröße „groß“.
- [ ] „Mein Tag“: Die Kennzahlen rechts oben haben höchstens zwei Zeilen,
      die Kopfzeile wird nicht höher. Der volle Text steht im Tooltip.
- [ ] Eine Zeichnung von einer Pinnwandkarte aus öffnen: „Zurück zur
      Pinnwand“ steht rechts neben dem Titel, der Titel bleibt, wo er ist.
- [ ] Seite, Zeichnung und Galerie: Ihre Werkzeuge stehen in der Leiste über
      der Fläche; die Fläche beginnt auf derselben Höhe wie bei einer Liste.
- [ ] Design wechseln (Hell, Dunkel, Glas, Pixel, Kontrast), jeweils mit und
      ohne Hintergrundverlauf: Werkzeugleiste und Fußbereich tragen keine
      Kästen, die Überschrift „Seiten“ bleibt lesbar.

### Bilder in Seiten

- [ ] „Bild“ in der Werkzeugleiste: ein PNG, ein JPEG, ein HEIC (macOS), ein
      SVG und ein sehr breites Bild einfügen. Kleine stehen links mit Text
      daneben, große füllen die Spalte.
- [ ] „/“ am Anfang einer leeren Zeile › Bild … und Mehr › Bild einfügen …
      führen zum selben Dialog.
- [ ] Ein Bild aus dem Finder bzw. Explorer auf eine Stelle der Seite ziehen:
      Es landet vor der Zeile unter dem Zeiger. Eine PDF-Datei wird mit
      Hinweis abgelehnt.
- [ ] Bild anklicken: Rahmen und Griff erscheinen. Ecke ziehen: Das Bild
      wächst und schrumpft im Seitenverhältnis; der Text fließt neu.
- [ ] Bild in die linke, mittlere und rechte Spaltenhälfte ziehen: Die
      Markierung zeigt Zeile und Seite; danach umfließt der Text links, steht
      das Bild in eigener Zeile bzw. umfließt rechts.
- [ ] Rechtsklick: Umfluss wechseln, Spaltenbreite, halbe Breite,
      Originalgröße, Im System öffnen, Bild entfernen.
- [ ] Entf auf dem markierten Bild entfernt es; Strg/Cmd+Z holt es zurück.
      Alt+←/→/↑ wechselt den Umfluss.
- [ ] Text neben einem Bild tippen, löschen, Überschriften setzen: Der
      Umfluss passt sich an, nichts überlappt.
- [ ] Seite scrollen (Mausrad, Trackpad, auch über einem Bild): Die Bilder
      wandern ohne Versatz mit.
- [ ] Fenster schmaler und breiter ziehen, Lesebreite ↔ volle Breite: Bilder
      bleiben in der Spalte, nie breiter als die Spalte.
- [ ] Seite schließen, Glide neu starten: Bilder, Größen und Umfluss sind
      unverändert.
- [ ] Mehr › Als Markdown speichern …: Neben der Datei liegt „<Name> Bilder“
      mit den Dateien; in einem Markdown-Programm erscheinen die Bilder.
- [ ] Als Glide-Seite exportieren und wieder importieren: Die Kopie zeigt
      alle Bilder.
- [ ] Seite duplizieren und als Vorlage speichern, daraus eine neue Seite
      anlegen: Die Bilder sind da (sonst steht „Bild fehlt“).
- [ ] Komplettbackup speichern und in eine leere Ablage laden: Bilder da.
- [ ] Bildschirmleser: Das Bild ist als Fläche erreichbar; der Text liest
      sich ohne Ankerzeichen.

### Vorschauen (Tk 9)

- [ ] Galerie mit PNG, GIF, JPEG, HEIC, WebP, TIFF, BMP und SVG füllen:
      macOS zeigt alle als Vorschau; Windows JPEG, TIFF, BMP und SVG (HEIC und
      WebP nur mit den Microsoft-Erweiterungen); Linux PNG, GIF und SVG.
- [ ] Kachelgrößen Klein, Mittel, Groß und die Großansicht: Bilder sind
      scharf, ohne Treppen (macOS) bzw. akzeptabel (Windows).
- [ ] Bilder aus dem Finder bzw. Explorer in die Galerie ziehen.
- [ ] Pinnwandkarte eines Punkts mit JPEG-Anhang: Die Karte zeigt die
      Vorschau (macOS).
- [ ] Galerie mit 100 Bildern: Scrollen bleibt flüssig.

### Systemmitteilungen

- [ ] Einstellungen › Persönlich › „Fällige Benachrichtigungen auch als
      Systemmitteilung zeigen“ ist anfangs aus.
- [ ] Ansicht › Systemmitteilung testen: macOS fragt einmal nach der
      Erlaubnis; danach erscheint die Probe. Ohne Erlaubnis nennt Glide den
      Grund.
- [ ] Einschalten, eine Erinnerung in zwei Minuten setzen, Glide in den
      Hintergrund: Genau eine Mitteilung mit dem Titel des Punkts erscheint.
- [ ] Drei Erinnerungen zur selben Zeit: eine Sammelmeldung „3 Erinnerungen
      fällig“.
- [ ] Windows: Mit der ersten Mitteilung erscheint das Symbol im
      Infobereich; ein Klick darauf holt Glide nach vorn.
- [ ] Ausgeschaltet: keine Mitteilung, nur das Hervorheben in Dock bzw.
      Taskleiste.
- [ ] Im Entwicklungsbundle (`Glide.app`) statt aus Python gestartet:
      Die Mitteilung erscheint unter „Glide“.

### „/“-Befehle und wiederkehrende Checkliste

- [ ] In einer Liste „Milch /morgen /wichtig“ eintippen: Unter der Eingabe
      steht „→ fällig morgen · Wichtigkeit hoch“; Enter legt „Milch“ so an.
- [ ] „/mo“ und Tab: wird zu „/morgen “. Escape blendet den Hinweis aus.
- [ ] /heute, /übermorgen, /freitag, /24.12.2026, /hoch, /mittel, /niedrig,
      /meintag und ein vorhandenes Label wie /Kunde ausprobieren.
- [ ] „und/oder“ und „/xyz“ bleiben Teil des Titels.
- [ ] Rechtsklick auf eine Aufgabenliste › Wiederkehrende Checkliste: Häkchen
      erscheint. Alle Punkte abhaken: Nach einem Augenblick sind alle wieder
      offen, samt Checklistenschritten; Rückgängig zeigt den erledigten
      Stand.
- [ ] „Alle Punkte wieder öffnen“ in einer normalen Liste.
- [ ] Liste duplizieren: Die Kopie ist ebenfalls wiederkehrend.

### Globale Suche

- [ ] Strg/Cmd+O: Die Suche erscheint unter der Kopfzeile mit runden Ecken
      und weichem Schatten; die Kopfknöpfe bleiben ganz sichtbar.
- [ ] In allen Designs und über Startseite, Liste, Pinnwand und Seite
      öffnen: Ecken und Schatten liegen ohne Kasten auf der Fläche darunter.
- [ ] Pfeiltasten, Enter und Escape; Klick auf einen Treffer.

### Leistung und Start

- [ ] Glide mit einem großen Bestand starten: Das Fenster erscheint sofort
      in der zuletzt benutzten Größe und Lage und füllt sich dann.
- [ ] Schnell hintereinander Punkte abhaken und umbenennen: keine spürbare
      Verzögerung beim Speichern.
- [ ] Nach einem Absturz oder Zwangsbeenden: Die letzte Änderung ist
      gespeichert (Glide schreibt weiterhin sofort).

## Oberfläche und Zugänglichkeit

- [ ] Detailbereich einschalten: Felder bearbeiten, die Auswahl wechseln
      (keine Eingabe geht verloren), Breite ziehen, Fenster unter 980 px.
- [ ] Leerzustände: leere Liste, leerer Ordner, leeres Notizbuch, leere Suche,
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
