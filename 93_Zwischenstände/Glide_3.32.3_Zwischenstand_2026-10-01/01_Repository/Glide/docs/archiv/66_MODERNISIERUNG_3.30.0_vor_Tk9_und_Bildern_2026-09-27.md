# Modernisierung 3.30.0 – Pixel-Werkstatt, Format 20, Startseite, Board

Stand 27.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

## 1. Status und Umfang

3.30.0 setzt den
[Aufgabenkatalog vom 25.09.2026](../../../00_Arbeitsvorbereitung/Glide_Aufgabenkatalog_Modernisierung_2026-09-25.md)
vollständig um: alle fünf Etappen (A bis E) und die Pakete unter „Später“.
Grundlage sind die
[Wettbewerbsrecherche](../../../00_Arbeitsvorbereitung/Glide_Wettbewerbsrecherche_Modernisierung_2026-09-25.md)
und die
[Arbeitsvorbereitung](../../../00_Arbeitsvorbereitung/Glide_Arbeitsvorbereitung_Modernisierung_2026-09-25.md).

**Entscheidungen vom 25.09.2026:**

- E-01 bis E-16: alle Empfehlungen.
- Das Archiv (MO-070, E-06) gehört dazu. Die Rückfrage nannte bei der
  Alternative „Ohne neues Datenformat“ ausdrücklich „kein Archiv“; mit
  „Alle Empfehlungen“ war es damit Teil des gebündelten Formats 20.
- Aus dem älteren Ideenvorrat gewählt: verknüpfte Punkte, Vorlagen mit
  Eingabefeldern, echte Abhängigkeiten, Tagesbeginn und Wochenrückblick,
  Kapazität je Wochentag, Zeiterfassung je Punkt.
- Visuelle Richtung: ein eigenes Design „Pixel“.
- Nicht gewählt: Einstieg für neue Nutzer, eigene Felder je Liste.

**Ausbau am selben Tag** (Rückfrage nach dem ersten Abschluss, alle
Empfehlungen gewählt):

- Zeitblöcke per Ziehen und Alt+↑/↓ (AO-070, zweite Stufe);
- Präsentation und Notizfolien als Druckseite bzw. PDF (MO-080, zweite Stufe);
- Rückgängig beim einfachen Kartenverschieben;
- Detailbereich mit allen Feldern außer Anhängen;
- Gismo still in Leerzuständen (Stufe 2 der Begleiter-Entscheidung);
- Pixelschrift „Pixelify Sans“ (SIL OFL 1.1) für Überschriften im Design
  „Pixel“;
- Umstellungstest mit einer Kopie des echten Bestands. Er deckte auf, dass
  Glide 3.29 einen Format-20-Bestand bei der ersten Eingabe überschreibt
  (Abschnitt 9).

**Zweiter Ausbau am 26.09.2026** (alle vorgeschlagenen Punkte gewählt):

- Anhänge im Detailbereich;
- Zeichnungen als Bild in Folien und Druckseite;
- Stundenraster in „Mein Tag“;
- Gruppierung mit Zwischenüberschriften und durchgehender Nummerierung;
- ein Lasttest der zeitempfindlichen Oberflächensuite;
- ein Windows-Prüfpaket;
- ein Entwurf des Produktdatenblatts 3.30.

**Dritter Ausbau am 26.09.2026** („weiter mit den nächsten Aufgaben“ – die
bekannten Grenzen aus Abschnitt 11):

- Punkte aus der Liste von „Mein Tag“ ins Stundenraster ziehen, auch ohne
  Uhrzeit und aus dem Eingang;
- die gruppierte Tabelle mit Zwischenüberschriften und Nummern;
- die Pixelschrift unter Linux über Fontconfig;
- mitbehoben: „Pinnwand öffnen“ aus der Tabelle (Abschnitt 9).

**Kleine Fenster am 26.09.2026** (Rückmeldung: bei Mindestgröße nur das
Wichtigste, ohne Überschneidungen, Quetschungen oder unbedienbare Teile):

- Höhenstufen für Aktionsreihen, Seitenleiste, Bibliothek und Pinnwand;
- ganze Chips und Unterzeilen statt Anschnitt;
- Knöpfe der Suchzeile nie mehr gequetscht;
- Tabellenspalten nach Priorität;
- die Kennzahlen weichen dem Titel;
- außerdem Überschriften auch in der sortierten gruppierten Tabelle;
- eine eigene Suite: `test_mindestgroesse330.py` (Abschnitt 2.5).

**Weitere Runde am 26.09.2026** (Rückfrage, alle vier Vorschläge gewählt):

- Dialoge bei Mindestgröße (Abschnitt 2.5);
- Kontrast aller Designs nach WCAG AA (Abschnitt 2.6);
- Stundenraster in schmalen Fenstern und Einplanen über die Seitenleiste
  (Abschnitt 2.4);
- Paketierung als Vorstufe mit festen Kennungen `de.shaye.glide` und
  `Shaye.Glide` (Abschnitt 2.7).

**Hintergrundverläufe am 26.09.2026** (Auftrag mit Beispielbildern: moderne
Mesh-, Aurora- und Grain-Verläufe, fünf je Design, Liquid-Glass-Wirkung im
Glasdesign):

- Details in Abschnitt 2.8.

**Rückmeldung am 26.09.2026** (Bildschirmfotos des Nutzers, Absturz im
hellen Glasdesign):

- Der Absturz beim Start ist behoben; Milchglas je Kachel und Fenster, Schrift
  statt Pille (Abschnitt 2.8).
- Oberfläche aufgeräumt nach „Form folgt Funktion“: Verlauf als Kopfzeilen-
  knopf, „In Bearbeitung“ in „Mein Tag“, kein Klapppfeil bei „Listen“, feste
  Knopfreihenfolge, gleiche Unterkanten, ruhige Zeichenfläche (Abschnitt 2.9).

**Zweite Rückmeldung am 26.09.2026** (zehn Bildschirmfotos, Leistungsprobleme,
Wunsch nach mehr Notion):

- Punktdialoge bedienbar, Farben nach Bedeutung, Aufräumen, deutlich
  schnellere Oberfläche (Abschnitt 2.10).
- Das Notion-Konzept liegt als Entscheidungsvorlage bereit:
  [Konzept Seiten wie Notion](../../../00_Arbeitsvorbereitung/Glide_Konzept_Seiten_wie_Notion_2026-09-26.md).

**Seiten und Ordnertypen am 26.09.2026** (Entscheidungen des Nutzers zum
Konzept): Die neue Seitenart „Seite“ ist für KI-Berichte gedacht, mit
Aufgaben als echten Punkten. Dazu kommen die Übersicht „Seiten“ und die
Ordnertypen Ordner, Bibliothek und Notizbuch (Abschnitt 2.11).

**Aufräumen, Seitenbereich und Galerie am 27.09.2026** (Auswahl des Nutzers
aus einer Rundgangsliste, dazu eine eigene Notizliste): Die Aktionsleiste
erscheint nur bei Auswahl, die Kopfzeile trägt nur Symbole. Die Knöpfe unter
dem Listenbaum entfallen, Liste · Tabelle · Pinnwand ist ein fester
Umschalter. Seiten haben einen eigenen Bereich „Seiten +“ mit Vorlagen und
eigenem Format `.glidepage`, und die neue Listenart „Galerie“ kommt hinzu
(Abschnitt 2.12).

**Kompression am 27.09.2026** (Antworten des Nutzers und Wunsch „die App
weiter komprimieren“, Abschnitt 2.13):

- Titel höchstens 40 Zeichen; die Beschreibung steht nur in der
  Kennzahlenzeile.
- Seiten- und Listenbereich klappen ein; die Bibliothek ist eine Tabelle.
- „Notizbuch“ statt „Tagebuch“, gleiche Innenränder.
- Hinweise stapeln sich nicht mehr.

Aus der
[Aufgabensammlung Zeichenfläche](../../../00_Arbeitsvorbereitung/Glide_Aufgabensammlung_Zeichenflaeche_2026-09-23.md)
sind außerdem erledigt:

- ZF-050 (Rest),
- ZF-100 (Zeichnung als Pinnwandkarte),
- ZF-120 (Tagebuch mit allen Inhaltsarten),
- ZF-210 (Glide-Palette),
- die Anlageoption „Pinnwand“,
- die Punkte aus ZF-200 und ZF-300, soweit sie im Katalog stehen.

**Nicht durch Agenten erledigbar und offen:**

- manuelle Prüfung unter echtem Windows und macOS,
- DPI-Skalierung und Bildschirmleser,
- Signatur und Notarisierung,
- Markenprüfung und Store-Freigabe.

Die [manuelle Prüfliste 3.30.0](../../../00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.30.0.md)
führt diese Punkte einzeln auf.

## 2. Bedienung nach Bereichen

### 2.1 Pixel-Werkstatt (ZD-010 bis ZD-170, AO-050)

- **Werkzeuge:** sieben Werkzeuge mit Kontextleiste: Pinsel (B), Füllen (F),
  Pipette (I), Linie (L), Rechteck (U), Ellipse (E), Auswahl (S).
  - Die Leiste zeigt nur, was zum Werkzeug passt: Größe 1/2/4/8, Umriss oder
    gefüllt, Symmetrie, Muster.
  - Umschalt beim Ziehen hält Linien bei 0/45/90 Grad und Formen quadratisch.
- **Farben:**
  - Links malt die Vorder-, rechts die Hintergrundfarbe; X tauscht, D setzt
    zurück.
  - Die Farbleiste zeigt Palette und zuletzt benutzte Farben. Umschalt+Klick
    ersetzt eine Farbe in der ganzen Zeichnung.
- **Ansicht:**
  - Strg+Mausrad zoomt um den Zeiger, die mittlere Maustaste verschiebt.
  - Eine eingebettete Vorschau zeigt die Originalgröße (P).
- **Muster und Hilfen:** Symmetrie (M, waagerecht/senkrecht/beide), Füllmuster
  (voll, Schachbrett, Punktraster 25/75 %), Kachelvorschau 3 × 3, Pinsel über
  den Rand, pixelgenaue 1×1-Linie, Graustufen, Deckkraft der Referenz.
- **Auswahl:** Rechteck aufziehen, dann verschieben, kopieren, ausschneiden und
  einfügen – auch zwischen Zeichnungen und aus Glide-JSON-/SVG-Text. Vor der
  Übernahme erscheint eine Importvorschau.
- **Rückgängig je Aktion:** Pinselzug, Form, Füllung, Ersetzen und Einfügen
  sind je ein Schritt, höchstens 50 (Budget 8 × Zellzahl).
- **Größen:** 16, 32, 64 oder 128 Zellen je Seite, beim Anlegen gewählt und
  danach fest.
- **Paletten:** „Glide 32“ ist mitgeliefert; eigene Paletten speichern,
  löschen, als `.gpl`/`.hex` ein- und ausgeben; unbenutzte Farben entfernen.
- **Zwischenstände:** benannte Stände als Anhang der Seite (MIME
  `application/vnd.glide.drawing-snapshot+json`, höchstens 10), wiederherstellbar.
- **PNG-Export:** ganzzahlig vergrößert, ohne Glättung, bis 2048 px
  Kantenlänge.
- **Pixelsymbol:** eine eigene 16×16-Zeichnung im Listen- bzw. Ordnerobjekt
  (E-09). Sie steht in Seitenleiste, Übersicht und Suche.

### 2.2 Startseite, Seitenleiste und Suche (Etappe B)

- **„Startseite anpassen“** schaltet die Startseite in einen eingebetteten
  Bearbeitungsmodus:
  - Kacheln am Griff ziehen oder mit Alt+↑/↓ verschieben;
  - „Ganze Breite“ umschalten;
  - ausblenden und wieder einblenden.
  - Neue Kacheln „Zeichnungen“ (Miniaturen), „Angeheftet“ und „Angeheftete
    Filter“ (höchstens 4, Treffer direkt abhakbar).
  - Eine Startseite, deren Reihenfolge schon gespeichert war, bekommt die neuen
    Kacheln ausgeblendet; sie sieht nach dem Update unverändert aus.
- **Anheften** (höchstens 20 Seiten) über das Kontextmenü von Liste und Ordner.
  Der Block „Angeheftet“ steht unter den Systemzeilen.
- **Seitenleiste:**
  - Die Abschnitte Ansichten, Angeheftet sowie Listen und Ordner sind
    einklappbar.
  - Ansichten klappt man über das Kontextmenü einer Systemzeile ein, Listen
    über den Pfeil neben „+“.
  - Über Ordnerzeilen erscheinen „+“ (Liste, Notiz, Pinnwand, Zeichnung,
    Unterordner) und „…“ (Kontextmenü) als Überlagerung. Jede Aktion steht auch
    im Kontextmenü.
- **Suche Strg/Cmd+O:** Seiten, Punkte und Aktionen in einem eingebetteten
  Feld; ohne Eingabe die zuletzt geöffneten Seiten. Umlaute gelten wie
  ae/oe/ue/ss.
- **Seitenkopf:** anklickbarer Ordnerpfad, darunter eine Chipzeile, zum
  Beispiel „2 offen · 1 überfällig · nächste Fälligkeit morgen · 1 Label“.
- **Rückgängig im Hinweis** nach Abhaken, Löschen und Lösen von Karten. Der
  Hinweis nimmt nur zurück, was er meldet.
- **„Listen und Ordner“** als Galerie:
  - Kartengröße wählbar;
  - Zeichnungsminiaturen und Notizanfang;
  - Schalter „Archiv“ mit „Zurückholen“.
- **Tagesbeginn und Wochenrückblick** sind Unterseiten der Startseite.
  - Der Tagesbeginn geht Überfälliges, Verschlepptes und den Eingang durch:
    heute, morgen, nächste Woche, ohne Tag, erledigt, überspringen.
  - Der Wochenrückblick zeigt Erledigtes, Weitergewandertes, geschätzte gegen
    erfasste Zeit und die Kapazität je Tag.

### 2.3 Pinnwand als Board (Etappe C)

- **Spaltenboard** (PW-010): dritte Anordnung neben „Geordnete Karten“ und
  „Frei anordnen“.
  - Es zeigt alle Aufgaben und Long-Tasks des Bereichs (E-16), nicht nur
    angeheftete Karten.
  - Gruppieren nach Fälligkeit, Bearbeitungstag, Wichtigkeit, Label, Erledigt
    und – auf Ordner- und globaler Pinnwand – Liste.
  - Ziehen oder Alt+←/→ setzt genau dieses Feld, als ein Rückgängig-Schritt.
  - Regeln:
    - Beim Datum bleibt die Uhrzeit.
    - Eine Wiederholung bleibt Serie.
    - Beim Label ersetzt das Ziel das Quelllabel; „Ohne Label“ entfernt die
      eigenen Labels.
    - „Überfällig“ nimmt nichts an und sagt warum.
  - Spalten lassen sich einklappen; „Leere Spalten ausblenden“ und „Nur offene“
    sind Schalter.
  - Doppelklick in eine Spalte legt einen Punkt mit ihrem Wert an.
- **Gruppieren in Liste und Tabelle** (AO-040): „Ansicht › Liste ›
  Gruppieren nach“ oder das Listenmenü.
  - Die Abschnitte sind aufklappbar, und ihr Zustand bleibt erhalten.
  - Ziehen zwischen Abschnitten setzt das Feld.
  - Seit dem zweiten Ausbau bleiben Zwischenüberschriften als Trennzeilen im
    Abschnitt stehen (synthetische Zeilen `…::ghead…`, nicht auswählbar).
  - Jeder Punkt trägt seine Nummer aus der ungruppierten Liste
    (`list_view_number_paths`).
  - Die Tabelle zeigt Unterpunkte auf Wunsch verschachtelt (AO-030).
    Elternpunkte eines Treffers bleiben dabei abgeschwächt stehen.
  - Seit dem dritten Ausbau zeigt auch die Tabelle beides:
    - Gruppiert oder verschachtelt steht in der schmalen Baumspalte
      (jetzt 76 px) die Nummer aus der Liste. Vorher erschien dort der
      abgeschnittene Titel ein zweites Mal.
    - Gruppiert stehen die Zwischenüberschriften als Trennzeilen im
      Abschnitt. Eine Spaltensortierung gilt innerhalb jeder Überschrift;
      die Überschriften selbst behalten die Reihenfolge der Liste.
- **Karteninhalt und Kartenfarbe** (PW-020):
  - Inhalt: Beschreibung (160 Zeichen), Checkliste (fünf Schritte, abhakbar),
    Bild. Einzelne Karten übersteuern das.
  - Farbe als Streifen, Kopf oder ganze Karte, aus Punktfarbe oder erstem
    Label. Im Kontrastdesign kommt zusätzlich eine Form je Farbe dazu.
- **Zeichnung als Karte** (ZF-100): Verweis `page:<Seitenkennung>` mit
  Miniatur (höchstens 160 px, Revisionsschlüssel). Doppelklick öffnet das
  Original, die Pfadzeile bietet „Zurück zur Pinnwand“.
- **Bereiche** (PW-030): Rechteck mit Name und Farbe, höchstens 50.
  - Karten, deren Mittelpunkt darin liegt, wandern beim Verschieben mit.
  - Der Griff unten rechts ändert die Größe.
  - F2 benennt, Entfernen löscht nur den Bereich.
  - „Zu Bereich springen“; Bereiche erscheinen im Navigator und im Druck.
  - Sichtbar nur bei „Frei anordnen“.
- **Aufräumen** (PW-040): Die Auswahl kommt in ein Raster mit ungefähr √n
  Spalten, in der Reihenfolge Zeilen von oben, dann von links. Der Fang bleibt
  beachtet.
- **Weiterdenken** (PW-050): Strg/Cmd+Enter öffnet rechts neben der Karte ein
  Titelfeld (E-08).
  - Enter legt einen normalen Punkt der Liste an; Escape hinterlässt nichts.
  - Auf Wunsch wird die neue Karte automatisch verbunden.
  - Der Ziehpunkt am Kartenrand verbindet durch Ziehen.
- **Verbindungen** (PW-060): Beschriftung bis 40 Zeichen, gestrichelt, Farbe,
  Richtung – per Rechtsklick auf die Linie.
- **Hintergrund** (PW-070): Punkte, Linien oder Karo im Rasterabstand.
  Gezeichnet wird nur der sichtbare Ausschnitt, höchstens 2500 Marken. Das
  Mitdrucken ist wählbar.
- **Präsentieren** (MO-080): Bereiche als Folien im Vollbild.
  Pfeiltasten, Leertaste und Bild auf/ab blättern, Escape endet; der Zoom wird
  nur geliehen.
  - „Präsentation als PDF …“ (zweite Stufe) öffnet eine Druckseite: je
    Bereich eine A4-Seite quer mit Karten und Verbindungen, eingepasst und mit
    mitwachsender Schrift. Gedruckt oder als PDF gesichert wird im Browser –
    ohne eigene PDF-Bibliothek.
  - Die Druckseite der Pinnwand und die Folien teilen den Kartenbaustein
    `board_region_lines`.
  - Seit dem zweiten Ausbau zeigen Druckseite und Folien Zeichnungskarten als
    pixelscharfes PNG (`drawing_data_uri`, `image-rendering: pixelated`).
- **Kartenverschieben** mit Maus oder Alt+Pfeil ist seit dem Ausbau ein
  Rückgängig-Schritt mit Rückmeldung (`board_view_change`, Beschriftung
  „Karte verschoben“).
- **Anlageoption „Pinnwand“:** eine Aufgabenliste, die als Fläche startet.

### 2.4 Tagebuch, Planung, Oberfläche

- **Tagebuch** (ZF-120):
  - Notiz, Liste, Zeichnung und Pinnwand; die Anlage fragt das Momentdatum ab.
  - Jede Zeile nennt Datum und Art.
  - Sortierung nach Momentdatum, Erstellung und Kennung.
  - Knopf „Zeitraum“ für einen Tag oder Von-bis; beide Grenztage zählen mit,
    die Volltextsuche wirkt zusätzlich.
  - Verschieben ins Tagebuch bewahrt das Datum, sonst gilt der
    Erstellungstag; ist der unlesbar, fragt Glide.
  - „Momentdatum …“ im Listenmenü.
- **Mein Tag** (AO-070):
  - Punkte mit Uhrzeit stehen als „Zeitplan“ vorn. Die Dauer kommt aus der
    Schätzung, sonst gelten 30 Minuten für die Überschneidungsprüfung.
  - Überschneidungen werden benannt, nicht verschoben.
  - Die Kapazität bleibt minutenbasiert.
  - Zweite Stufe – Ziehen setzt die Uhrzeit, wie beim Umordnen entscheidet
    die Zeilenhälfte:
    - obere Hälfte eines Blocks: der Punkt endet, wo der Block beginnt;
    - untere Hälfte: er beginnt am Blockende;
    - Kopfzeile „Zeitplan“: vor den ersten Block;
    - „Ohne Uhrzeit“: die Uhrzeit fällt weg.
  - Mehrere Punkte folgen lückenlos aufeinander; Alt+↑/↓ verschiebt die
    Auswahl um 15 Minuten. Jede Änderung ist ein Rückgängig-Schritt.
  - **Stundenraster** (zweiter Ausbau): Der Knopf „Raster“ oder
    „Mein Tag: Stundenraster ein/aus“ blendet ab 900 px Fensterbreite rechts
    neben dem Zeitplan ein Raster ein, darunter statt der Liste.
    - Es reicht von 6 bis 22 Uhr und erweitert sich bei Bedarf.
    - Überschneidende Blöcke stehen nebeneinander, eine rote Linie markiert
      die aktuelle Uhrzeit.
    - Ziehen verschiebt einen Block im 15-Minuten-Raster, ein Doppelklick
      öffnet den Punkt.
    - Seit dem dritten Ausbau lässt sich jede Punktzeile der Liste ins Raster
      ziehen, auch aus „Ohne Uhrzeit“ und dem Eingang.
      - Eine gestrichelte Linie zeigt die Startzeit.
      - Der Punkt erhält diese Uhrzeit und den angezeigten Tag als
        Bearbeitungstag.
      - Mehrere Punkte folgen lückenlos aufeinander.
      - Ein Rückgängig-Schritt macht alles zurück.
    - Unter 900 px Fensterbreite steht das Raster statt der Liste;
      „Raster“ schaltet dann zwischen beiden um. Vorher verschwand es dort
      ganz.
    - Aus jeder Liste oder Tabelle auf „Mein Tag“ in der Seitenleiste
      gezogen, wird ein Punkt für den angezeigten Tag eingeplant, statt in
      eine andere Liste verschoben zu werden. Er bleibt in seiner Liste und
      erscheint im Zeitplan. Auch das ist ein Rückgängig-Schritt.
- **Vorlagen mit Eingabefeldern:** `{{Name}}` in Titel, Punkten,
  Beschreibungen, Checklisten und Notiztext.
  - Beim Verwenden gibt es einen Dialog für alle Namen (höchstens 12).
  - `{{Datum}}`, `{{Heute}}` und `{{Tag}}` sind mit heute vorbelegt, `{{Jahr}}`
    mit dem Jahr.
  - Formatierungen im Notiztext verschieben sich mit.
- **Detailbereich** (MO-030, E-04): zuschaltbar über „Ansicht › Liste ›
  Detailbereich ein-/ausblenden“.
  - Er steht rechts neben Liste oder Tabelle, erscheint ab 980 px
    Fensterbreite und ist ziehbar breit (280 bis 640 px).
  - Übernommen wird beim Verlassen eines Felds, mit Enter oder vor dem
    Auswahlwechsel, je Übernahme ein Rückgängig-Schritt.
  - Seit dem zweiten Ausbau auch die **Anhänge**: anfügen („+ Datei …“,
    lokale Kopie wie in der Maske), öffnen per Klick, entfernen mit „×“. Die
    Datei bleibt für Rückgängig liegen; dieselbe Datei (Name und Größe) kommt
    nicht doppelt.
  - Seit dem ersten Ausbau alle übrigen Felder: Titel (Long-Task
    mehrzeilig), Erledigt, Wichtigkeit, Art, Farbe, Fälligkeit, Wiederholung,
    Erinnerung, Bearbeitungstag mit Uhrzeit, Aufwand, erfasste Zeit, Labels,
    Beschreibung, Checkliste (anfügen, abhaken, entfernen), „Verknüpft mit“
    und „Wartet auf“ mit Kreisprüfung. Der Bereich scrollt.
  - Ein Wechsel zu Gruppe oder Überschrift fragt nach, wenn der Punkt
    Planungsfelder trägt – in der Maske sieht man deren Wegfall vor dem
    Bestätigen, hier wirkt die Wahl sofort.
  - Maske und Bereich teilen `read_repeat_rule` und `add_relation_targets`;
    den Erinnerungseditor übernimmt der Bereich aus der Maske.
  - „Alle Felder …“ öffnet weiterhin die Punktmaske.
- **Leerzustände** (MO-050): Unter der Leerzeile steht eine Hauptaktion:
  - „Ersten Punkt anlegen“,
  - „Suche zurücksetzen“,
  - „Neue Liste anlegen“,
  - „Ersten Eintrag anlegen“,
  - „Alle Tage zeigen“,
  - „Zur Startseite“,
  - auf der Pinnwand „Punkte anheften“ bzw. „Filter aufheben“.
  - Seit dem Ausbau steht Gismo klein (56 px) und still daneben – ohne
    Sprechblase, ohne Blinzeln, ohne Führung. „Spielereien aus“ blendet ihn
    aus (Stufe 2 der Begleiter-Entscheidung).
- **Design „Pixel“** (MO-060): Blau, Gelb und Pink auf Schwarz,
  Farbflächen-Kachelköpfe, blockige Akzentbalken auf Karten, harte
  Pixelrahmen um Miniaturen. Es gibt keine Texturen.
  - Seit dem Ausbau tragen Seitentitel und Kachelköpfe die Pixelschrift
    „Pixelify Sans“ (Regular und Bold, SIL OFL 1.1). Fließtext bleibt in der
    Oberflächenschrift.
  - Herkunft, Commit und Prüfsummen stehen in
    `resources/fonts/provenance.json`, der Lizenztext in
    `OFL-PixelifySans.txt`.
  - Registriert wird nur für den laufenden Prozess:
    - Windows: `FR_PRIVATE`;
    - macOS: CoreText;
    - Linux (seit dem dritten Ausbau): `FcConfigAppFontAddDir` von
      Fontconfig. Damit ändert Glide weder `~/.fonts` noch den Schriftcache.

    Findet Tk die Schrift trotzdem nicht – etwa ein Tk ohne Xft –, bleibt
    die Oberflächenschrift.
- **Verknüpfungen, Abhängigkeiten, Zeit:** in der Maske im Abschnitt
  „Beziehungen und Zeit“ und im Kontextmenü „Beziehungen und Zeit“.
  - Ein wartender Punkt fragt vor dem Abhaken nach und steht in der
    Dringlichkeit auf Rang 4.
  - Die laufende Zeiterfassung zeigt der Kopf.

### 2.5 Kleine Fenster (Mindestgröße 860 × 700)

Regel: Bei Mindestgröße bleiben die wichtigsten Bestandteile. Was weicht,
weicht ganz und bleibt über „⋯“, Kontextmenü, Menüleiste oder Kürzel
erreichbar. Nichts wird gequetscht oder angeschnitten.

- **Höhenstufen** (`height_density`, gemessen an der Fensterhöhe):
  - ab 850 px (also auch in der Standardgröße 1280 × 860): alles;
  - 780–849 px: je Aktionsrahmen eine Reihe, wenn nur zwei Spalten passen.
    „Liste importieren“ weicht aus der Seitenleiste und von der Seite
    „Listen und Ordner“ (bleibt im Menü „Datei“). Die Pinnwand zeigt eine
    einzeilige Hilfe;
  - unter 780 px: nur die erste Aktionsreihe (Liste leeren, Löschen,
    Wichtigkeit, Fällig). „Ordner“, „Bearbeiten“ und „–“ stehen in einer
    Zeile.

  Bei 860 × 700 zeigt die Aufgabenliste damit rund 8 statt 6 Zeilen, der
  Listenbaum der Seitenleiste 5 bis 6 statt 2 bis 3.
- **Kopfbereich:**
  - Die Kennzahlen unter dem Titel zeigen nur ganze Chips.
  - Die Unterzeile verliert zuerst ganze Abschnitte hinter „ · “, dann
    folgt „…“.
  - Die Kennzahlen rechts oben weichen dem Titel: Sie brechen im
    verbleibenden Platz um und bleiben vollständig.
- **Suchzeile:** Die Knöpfe „Liste“, „Tabelle“, „Pinnwand“ und die
  Tagesschalter werden vor das dehnbare Suchfeld gepackt
  (`search_row_anchor`). Vorher wurden sie bei schmalem Fenster gequetscht.
- **Pinnwandleiste:** Die Breite wird gemessen statt geschätzt.
  - Zuerst weichen die Nebenschalter, dann „Reiter“.
  - Zuletzt wird „Übersicht“ zum Pfeil.
- **Bibliothek und Vorlagen:** Die Knöpfe fließen in so viele Spalten, wie
  passen. Vorher standen sie bei Enge einzeln untereinander.
- **Tabelle:** Der Titel behält mindestens 220 px, ganze Spalten weichen nach
  `TABLE_COLUMN_PRIORITY` (zuerst „Art“, dann Aufwand, Checkliste …). Die
  gewählte Spaltenfolge bleibt.
- **Prüfung:** `test_mindestgroesse330.py` misst jede Ansicht in fünf
  Kombinationen aus Design, Schriftgröße und Fenstergröße (unter anderem große Schrift, Pixel, Glas, 1400 × 700).
  - Die Befundarten sind: über den Fensterrand, über den Elternrand,
    gequetschte Knöpfe, abgeschnittener Labeltext und seitlicher Überstand
    auf Scrollflächen.
  - Die Suite läuft ohne Bildschirmaufnahme und damit auch bei gesperrtem
    Bildschirm.
  - Gegen den Stand davor fand sie 24 Befunde.

- **Dialoge:** Jeder Dialog der Menüleiste wird bei seiner eigenen
  Mindestgröße gemessen, in mittlerer und großer Schrift.
  - `run_modal` hebt die Mindestbreite eines Dialogs auf die Breite seines
    Inhalts an, begrenzt durch den Bildschirm (`ensure_dialog_min_width`).
    Feste Mindestgrößen stammen aus der mittleren Schrift.
  - Im Kalender kürzen die Tageszellen nach Pixeln statt nach Zeichen.
    Was in der Höhe nicht passt, weicht ganz und erscheint als „+N“ neben
    dem Tag; der Hinweis bricht um.
  - Datumsfelder verlangen 10 statt 20 Zeichen Breite, damit der
    Kalenderknopf daneben Platz behält. Kalenderknöpfe werden vor dem
    dehnbaren Feld gepackt.
  - Aufklapppfeile sind genau so hoch wie ihr Feld.

### 2.6 Kontrast (WCAG 2.2 AA)

Jeder dargestellte Text erreicht in allen zehn Designs mindestens 4,5:1,
große Schrift 3:1.

- **Grundpalette:** Die Schriftfarben von „Hell“ und „Dunkel“ sind in
  `PALETTE` selbst vertieft beziehungsweise aufgehellt, jeweils knapp über
  4,5:1.
  - Hell: Grün `#34C759` → `#22813A`, Orange `#FF9500` → `#A35F00`, Türkis
    `#30B0C7` → `#227B8B`, Blau → `#086FD6`, Lila → `#9E4AC8`, Rot →
    `#D43128`, Platzhalter und schwache Priorität → `#707074`.
  - Dunkel: Platzhalter → `#939398`, Lila → `#C66CF3`, Rot → `#FF5950`, Blau
    → `#2C95FF` (eigener Ton `dark_blue`).

  Vorher lagen sie im hellen Design bei 2,0 bis 3,8:1.
- **Sicherheitsnetz:** `legible_text_roles` prüft in jedem Design die
  Schriftrollen gegen Hintergrund, Karte und Eingabefeld (`TEXT_ROLE_KEYS`,
  `legible_on`). Wo nötig, zieht es sie im eigenen Farbton nach, vor allem in
  den gemischten Glasdesigns. Hell und Dunkel ändert es nicht mehr.
- **Knöpfe:** `RoundedButton.legible_text` sichert jeden Zustand, auch beim
  Überfahren und aktiv.
  - Vorher stand in dunklen und bunten Designs weiße Schrift auf hellen
    Füllungen, bis hinunter zu 1,3:1.
  - Neutrale Schrift wechselt zur lesbaren Gegenfarbe, farbige wird im
    eigenen Ton nachgezogen.
- **Prüfung:** `test_kontrast330.py` misst an den dargestellten Elementen in
  neun Ansichten: Labels, Eingaben, farbige Zeilen und jeden Knopf in drei
  Zuständen. Das sind rund 13.700 Paare aus Schrift und Fläche.

### 2.7 Paketierung (Vorstufe)

- Kennungen (Inhaberentscheidung 26.09.2026): `APP_BUNDLE_ID =
  "de.shaye.glide"`, `APP_USER_MODEL_ID = "Shaye.Glide"`; im Produktregister
  eingetragen.
- Windows: Glide meldet sich vor dem ersten Fenster mit der Kennung an.
  `packaging/windows/verknuepfung_anlegen.ps1` legt die Startmenü-Verknüpfung
  mit derselben Kennung an; unter Windows noch nicht ausgeführt.
- macOS: `packaging/macos/baue_app.py` baut ein Entwicklungsbundle mit
  Quellen, Ressourcen, einer Kopie des Python-Starters und Ad-hoc-Signatur.
  - macOS führt den Prozess als „Glide“ mit der Kennung `de.shaye.glide`,
    geprüft mit getrenntem Datenordner.
  - Ohne übergebenes Logo entsteht ein Platzhaltersymbol im Build-Ordner.
- Keine neue Abhängigkeit. Die Werkzeuge `iconutil`, `sips` und `codesign`
  bringt macOS mit.
- Offen bleiben der Release-Build mit eingebettetem Python, Signatur,
  Notarisierung, Installer und die Mitteilungen selbst (Stufe B).

### 2.8 Hintergrundverläufe

- **Auswahl:** Je Design gibt es „Aus“ (Voreinstellung) und fünf Verläufe.
  - Gewählt wird in den Einstellungen unter „Design“ mit Vorschaubildern
    oder über „Ansicht › Oberfläche › Hintergrund“.
  - Gespeichert wird je Design in `backdrops` (additiv, Einstellungsformat 2).
- **Entwürfe** (`src/glide/backdrop.py`, reine Standardbibliothek):
  - Hell: Pastell, Herbstlicht, Morgenrot, Salbei, Perlmutt;
  - Dunkel: Aurora, Mitternacht, Ozean, Glut, Nebel;
  - Glas hell: Iris, Pfirsich, Lavendel, Minze, Himmel;
  - Glas dunkel: Nordlicht, Lagune, Amethyst, Sonnenwind, Polarnacht;
  - Minimal: Papier-, Graphit- und Körnungsvarianten ohne Farbe;
  - Dopamin: Neon, Synthwave, Lava, Tropen, Candy;
  - Pixel: Pixel-Aurora, 8-Bit-Abend, Sternenhimmel, Plasma, Rasterlinien –
    grob gerechnet, mit schwachem geordnetem Dithering auf gedämpfte
    Palettenstufen, blockweise vergrößert;
  - Kontrast: fünf kaum sichtbare Tönungen je Richtung.
- **Rechnen:** Weiche Farbwolken (Gauß) über der Grundfarbe, eine sanfte
  Sinusverzerrung für Nordlichtbänder, feine Körnung.
  - Glide rechnet in halber Bildschirmauflösung in einem Hintergrund-Thread
    (rund 1 s) und vergrößert ganzzahlig.
  - Das Ergebnis liegt als PNG im Cache des Systems (macOS
    `~/Library/Caches/Glide`, Windows `%LOCALAPPDATA%\Glide\Cache`, Linux
    `~/.cache/glide`), in Prüfläufen im Testordner. Die letzten sechs Bilder
    bleiben, der Nutzerdatenordner bleibt unberührt.
- **Lesbarkeit:** Oben, wo Titel und Unterzeile direkt auf dem Verlauf
  stehen (Lesezone), dämpft `fit_intensity` ihn, bis beide Schriftfarben auf
  jedem Punkt 4,5:1 erreichen.
  - Darunter leuchtet er voll, mit weichem Übergang.
  - Andere Texte auf dem Verlauf, etwa der Hinweis über den Aktionsknöpfen,
    messen den hellsten und dunkelsten Punkt darunter (`backdrop_extremes`).
    Reicht der Kontrast nicht, weicht zuerst die Schrift im eigenen Farbton
    aus (`fit_label_to_backdrop`, `legible_on`). Die Milchglas-Pille bleibt
    der letzte Ausweg. Bis zur Rückmeldung stand jeder Hinweis als dunkler
    Kasten auf dem Verlauf.
- **Anzeige ohne Transparenz:** Tk kennt keine durchscheinenden Flächen.
  - Rahmen in der Grundfarbe bekommen einen passgenauen Bildausschnitt als
    unterstes Kind, das Hauptfenster für seinen Rand ebenso.
  - Canvas-Flächen zeichnen das gemeinsame Bild als unterstes Element:
    Knöpfe, Karten, Scrollleisten, Startseite.
  - Titel, Unterzeile, Kennzahlen, Pfad und Hinweis sind `CanvasLabel`: Text
    ohne eigenes Rechteck.
  - Karten, Listen, Tabellen und Eingaben bleiben deckend. Der Verlauf ist
    Atmosphäre, nicht Arbeitsfläche.
- **Liquid Glass:** In den Glasdesigns nehmen Karten einen Hauch der
  mittleren Verlaufsfarbe an (16 %), ihr oberer Lichtverlauf mehr (45 %),
  die Innenkante wird heller.
  - Der Lichtverlauf bleibt seit der Rückmeldung im oberen Innenrand. Vorher
    reichte er über ein Drittel der Karte, hinter die deckenden
    Beschriftungen, die dadurch als helle Kästen erschienen.
- **Milchglas je Kachel und Fenster** (Entscheidung des Nutzers vom
  26.09.2026: „Tönung je Kachel“):
  - Jede Kachel nimmt den Mittelwert des Verlaufs hinter ihr an, mit der
    Kartenfarbe gemischt: 38 % im Glasdesign, 22 % in den übrigen, die
    Kontrastdesigns bleiben deckend (`sync_frosted_cards`, `frosted_color`).
  - Der Anteil sinkt, bis Schrift, Nebenschrift und Akzent 4,5:1 halten; die
    Farbe ist auf Dreierstufen gerundet, damit Scrollen nicht flackert.
  - Beschriftungen, Knöpfe, Scrollleisten und Listen der Kachel übernehmen
    dieselbe Farbe; Listen über einen abgeleiteten ttk-Stil
    (`Frost<Farbe>.<Stil>`). So gibt es keine Kästen.
  - Dialogfenster tönen sich nach der Stelle des Hauptfensters, über der sie
    liegen (60 % der Stärke, `frost_window`).
  - Neu gezeigte Widgets erfasst eine `<Map>`-Bindung und bündelt die Arbeit
    im nächsten Leerlauf (`_on_widget_map`).
  - Echte Durchsicht bleibt unmöglich: Listen, Felder und Seitenleiste sind
    native Widgets. Der Nutzer hat diese Grenze vor der Umsetzung bestätigt.
- **Absturz beim Start behoben:** Mit Verlauf, Startseite und schmalem
  Fenster (860 Pixel) stürzte Tk beim Start ab (`XMoveResizeWindow`).
  - Ursache: Die Hintergrundbilder trugen das Bindtag ihres Rahmens, damit
    Klicks durchgehen. Der Rahmen bekam dadurch auch ihre
    `<Configure>`-Meldungen und rechnete sein Layout mit den Bildmaßen neu.
    Das schaukelte sich auf.
  - Jetzt tragen sie ein eigenes Bindtag, das nur Mausereignisse an den
    Rahmen weitergibt (`install_backdrop_forwarding`).
  - Nachgestellt mit einer Kopie der Einstellungs- und Fensterdatei des
    Nutzers (mit Zustimmung), Originale per Prüfsumme unverändert.

### 2.9 Aufgeräumte Oberfläche (Rückmeldung vom 26.09.2026)

- **Gleiche Unterkanten:** Pinnwand, Zeichenfläche und Verlauf reichten
  14 Pixel tiefer als die Seitenleiste, die Startseite 4 Pixel weniger tief.
  Den unteren Rand trägt jetzt der Inhaltsbereich selbst (`PAGE_BOTTOM_GAP`).
- **Kopfzeile:** Die Knöpfe stehen in fester Reihenfolge
  (`pack_header_controls`). Vorher packte der Wechsel der Breitenstufe
  einzelne Knöpfe neu, und Tk hängte sie links an. Das Zahnrad stand danach
  ganz links, im Minimalzustand der Überlauf.
- **Änderungsverlauf:** Er ist ein Knopf ◷ neben „Drucken“ statt einer
  Seitenleistenzeile. Strg+H und das Menü öffnen dieselbe Seite.
  - Die Seite steht auf einer Karte und füllt die Höhe.
  - Das Symbol ist nicht mehr ↶, weil das zugleich „Rückgängig“ bedeutet.
- **„In Bearbeitung“ in „Mein Tag“:** Das ist jetzt ein aufklappbarer
  Abschnitt unter den Aufgaben des Tages (`plan_in_progress_entries`).
  - Er enthält alles Fällige, das nicht für den Tag eingeplant ist und nicht
    im Eingang steht.
  - Die Seitenleistenzeile ist entfallen. Die volle Ansicht öffnet ein
    Doppelklick auf die Abschnittsüberschrift; erreichbar ist sie außerdem
    über Startseite, Ansichtsmenü und App-Aktionen.
- **Kein Klapppfeil bei „Listen“:** „Listen und Ordner“ lässt sich nicht mehr
  einklappen. Ein gespeicherter Zustand „zu“ wird verworfen.
- **Zeichenfläche:**
  - Die Statuszeile hat immer zwei Zeilen: oben der Zustand, darunter
    Meldung und Referenzhinweis.
  - Die Kontextleiste reserviert für die aktuelle Breite die Zeilen des
    längsten Werkzeugs.
  - Beides zusammen hält die Fläche beim Umschalten ruhig; vorher sprang sie
    um bis zu 13 Pixel.
  - Mit dem Auswahlwerkzeug hebt ein Klick ohne Ziehen die Auswahl auf, statt
    ein blaues 1×1-Feld stehen zu lassen. Dazu kommen der Knopf „Aufheben“
    und Esc.
  - Über der Auswahl zeigt der Zeiger das Verschieben an (`fleur`).

### 2.10 Zweite Rückmeldung: Bedienbarkeit, Farben, Tempo (26.09.2026)

- **Punktdetails und erweiterte Eingabe:** Mit Verlauf ließ Tk den Dialog
  endlos neu anordnen. Er blieb klein, und nichts war anklickbar.
  - Ursache war das nachträgliche Umfärben der Dialoge (`frost_window`).
  - Neu: Mit Verlauf nimmt das ganze Design Grund- und Kartenfarbe aus
    dessen Mittelwert auf (`glass_backdrop_tint`). Dialoge entstehen gleich
    darin, mit statischem, passendem Grund.
  - Ein Designwechsel zieht dabei auch nicht eingetragene Widgets nach
    (`apply_theme`).
- **Kein Kasten mehr hinter Text:** Die Kennzahlen unter dem Titel
  („20 offen · 5 überfällig · 3 Labels“) sind Canvas-Text mit Trennpunkt.
  Eine Suche über alle Ansichten fand keine weiteren Kästen auf dem Verlauf.
- **„Startseite anpassen“** steht unter den Kacheln.
- **Farbe nur mit Bedeutung** (`button_color_key`):
  - Grün für die bestätigende Hauptaktion (Hinzufügen, Speichern, Anlegen,
    Erledigt).
  - Rot für Löschen und Leeren.
  - Die Benachrichtigungen als Statusanzeige.
  - Alles andere neutral: Hellgrau im dunklen, Dunkelgrau im hellen Design.
  - Aktive Zustände, Listen- und Labelfarben bleiben.
- **Form folgt Funktion:**
  - Die Eingabezeile fehlt in den abgeleiteten Ansichten (Mein Tag, In
    Bearbeitung, Labels, Filter, Verspätet) und im Papierkorb; dort meldete
    sie nur „geht hier nicht“.
  - Im Papierkorb fehlen auch die Knopfleisten (`sync_view_chrome`).
  - Leertexte brechen um statt abgeschnitten zu werden.
  - In der Notizseite steht unter der Eingabe nicht mehr „Notiz“.
- **Pinnwand:** Die Zeile mit Raster, Vorschau und den übrigen Schaltern ist
  linksbündig. Die Auswahlfelder sind so breit wie ihr längster Eintrag.
- **Zeichenfläche:** Um die Zeichnung herum steht die Kartenfarbe; vorher war
  links und rechts ein grauer Streifen.
- **„Erledigte Punkte löschen“:**
  - im Menü „Bearbeiten“, im Kontextmenü der Liste, im Überlaufmenü und in
    der Aktionssuche; vorher nur per Rechtsklick in der Seitenleiste;
  - die Punkte wandern in den Papierkorb, Rückgängig holt sie zurück.
- **Tempo** (Messungen auf dem Entwicklungs-Mac, Beispieldaten, 1280 × 860):

  | Messung | vorher | nachher |
  |---|---|---|
  | 20 Scrollschritte Startseite ohne Verlauf | 2,8 s | 1,45 s |
  | 20 Scrollschritte Startseite mit Verlauf | 10,5 s | rund 2,9 s |
  | Startseite öffnen mit Verlauf | 2,0 s | 0,8 s |
  | Liste öffnen mit Verlauf | 0,61 s | 0,25 s |
  | Modul laden ab dem zweiten Start (Schnellstart) | 0,87 s | 0,06 s |

  - `bind_resize`: Knöpfe, Karten, Scrollleisten und Umbruchzeilen zeichnen
    nur bei echter Größenänderung neu, nicht bei jeder Verschiebung.
  - Verlauf nur, wo er sichtbar ist (`_exposed_rects`): Fläche minus Kinder,
    beschnitten auf den sichtbaren Ausschnitt; Karten nur an den Ecken. Die
    gezeichnete Bildfläche sank auf der Startseite von 8,2 auf rund 0,3
    Megapixel.
  - Der Abgleich beim Scrollen läuft höchstens alle 80 ms.
  - Das Verlaufsbild liegt nur in Rechenauflösung im Speicher; die Stücke
    werden beim Kopieren vergrößert. Das spart bei 2560 × 1720 rund 17 MB.
  - Rückgängig-Schritte liegen als komprimiertes JSON (`PackedState`), rund
    10 % der bisherigen Tiefenkopien.
  - `glide_start.py` (im Bundle, in `07_Python-Versionen` als
    `Schnellstart.pyw`) lädt Glide als Modul. Der übersetzte Stand liegt im
    Cache des Systems; das spart ab dem zweiten Start rund eine halbe
    Sekunde.

### 2.11 Seiten und Ordnertypen (26.09.2026)

**Entscheidungen des Nutzers:**

- Seite und Notiz bleiben getrennt.
- Seiten dienen vor allem KI-erzeugten Berichten: endlos scrollend, leicht zu
  lesen, einfach zu bedienen.
- Aufgaben darin sind voll integriert.
- Favoriten und Zuletzt gelten nur für Seiten.
- Felder sollen später Glide-weit gelten, nicht je Liste.
- Ordnertypen: Ordner, Bibliothek, Notizbuch.

**Seitenart „Seite“** (`list_kind: "page"`, Klasse `PageEditor`):

- **Dokumentmodell:** wie die Notiz (`rich_note`: Text, Formatbereiche,
  Links), erweitert um `table`, `divider`, `task`, `indent1`–`indent3` und
  Aufgabenmarken `item:<id>`.
  - Dadurch funktionieren Papierkorb, Sicherungen, Vorlagen, Duplizieren und
    Austausch ohne neue Wege.
- **Lesen:** Lesespalte bis 760 Pixel mittig (umschaltbar auf volle
  Breite), Text 13 pt mit Zeilenabstand, Überschriften 24/19/15 pt, Code und
  Tabellen in Festbreitenschrift, endlos scrollend.
- **Schreiben:**
  - Markdown-Kürzel beim Tippen;
  - „/“ am Zeilenanfang öffnet die Blockauswahl;
  - Enter setzt Listen und Aufgaben fort, eine leere Zeile beendet sie;
  - Werkzeugleiste: Überschrift, Liste, Nummeriert, Aufgabe, Zitat, Code,
    Mehr.
- **Aufgaben:** Jede Aufgabenzeile ist ein echter Punkt der Seite (`items`).
  - Das Kästchen hakt über `toggle_item_done_anywhere` ab.
  - Ein Doppelklick auf den Titel öffnet die vollen Punktdetails
    (`edit_page_task`).
  - Titeländerungen im Text übernimmt der Punkt, und umgekehrt.
  - Eine gelöschte Zeile legt den Punkt in den Papierkorb. Rückgängig im
    Editor holt ihn zurück (`restore_page_task`).
  - Punkte, die ohne Zeile in die Seite kommen (etwa verschoben), erscheinen
    am Ende (`append_unlisted_page_tasks`).
- **Markdown** (`src/glide/page_markdown.py`, Standardbibliothek):
  - Überschriften, Absätze, verschachtelte Listen, Aufgaben, Zitate, Code,
    Trennlinien, Tabellen (als ausgerichtete Markdown-Tabelle), fett,
    kursiv, durchgestrichen, Code und Links;
  - der Rundlauf ist stabil;
  - Wege hinein: „Aus Zwischenablage“, Datei › Importieren › Markdown als
    Seite …, Einfügen in eine Seite;
  - Wege hinaus: Mehr › Als Markdown speichern oder kopieren.
  - Das bestehende „KI-Ergebnis importieren …“ bleibt der Weg für Gliederungen,
    die zu Listen werden.
- **Übersicht „Seiten“** (Seitenleiste, `PAGES_VIEW`): Neue Seite, Aus
  Zwischenablage, Markdown-Datei; Favoriten, Zuletzt geöffnet (höchstens 12)
  und alle Seiten – keine Listen. Ohne Eingabezeile und ohne Punktliste.
- **Ordnertypen** (`FOLDER_KINDS`, gespeichert in `folder_kind`):
  - `standard` heißt jetzt „Ordner“;
  - `journal` heißt „Notizbuch“ (bisher „Tagebuch“), das Verhalten bleibt;
  - `library` („Bibliothek“) ist neu: Neue Einträge darin sind Seiten.
  - Unbekannte Werte werden zu „Ordner“.

### 2.12 Aufräumen, Seitenbereich und Galerie (27.09.2026)

Grundsatz: Form folgt Funktion – keine Form ohne Funktion, kein zweiter Weg
zur selben Aktion, der wie ein eigener aussieht.

**Entscheidungen des Nutzers** (Auswahl aus einem Rundgang durch alle
Ansichten):

- Aktionsleiste nur bei Auswahl.
- In der Kopfzeile wird „+“ nicht doppelt belegt, zwischen den Symbolen
  steht kein Text, und die Kennzahlen erscheinen nur einmal.
- Alle vier Knöpfe unter dem Listenbaum entfallen.
- Liste · Tabelle · Pinnwand als Umschalter.
- Nicht gewählt: lange Hinweiszeilen entfernen, „Suche löschen“ als ×,
  Startseite entschlacken.

**Aus der Notizliste des Nutzers:**

- die Pinnwand in einer Zeile, mehr Platz für die Spalten;
- keine Kästen hinter Text (Startseite anpassen);
- Textlogo in der Akzentfarbe, Akzentfarbe oben in den Einstellungen;
- „Erledigt!“-Anzeige und Gismos Rechteck;
- ein Seitenbereich „Seiten +“ mit Funktionen wie bei Listen;
- die Galerie.

**Aktionsleiste:**

- Statt zwölf fester Knöpfe gibt es eine Reihe, die nur mit markierten
  Punkten erscheint (`selection_bar`, `sync_selection_bar`).
- Sie zeigt die Anzahl, Wichtigkeit, Fällig, Einplanen (Bearbeitungstag und
  Aufwand), Labels (Zuweisen als Menü) und Löschen.
- Labelverwaltung, Kalender, Rückgängig, Kopieren, Einfügen, Auf- und
  Zuklappen und „Liste leeren“ bleiben im Menü, in der Aktionssuche, im
  Rechtsklick und als Kürzel.
- Bei schmaler Spalte weicht zuerst die Anzahl. Bei Mindestbreite bleiben
  Wichtigkeit, Fällig und Löschen.

**Kopfzeile:**

- Nur Symbole: ⌘ Aktionen, ↯ Schnellerfassung (bisher „+“, dasselbe Zeichen
  wie „Neue Liste“) und ⍾ Benachrichtigungen mit der Zahl daneben.
- ◐ („In Bearbeitung“) stand im schmalen Kopf für die Benachrichtigungen und
  ist dort ersetzt.
- ✎ bleibt „Bearbeiten“.
- Die Kennzahlen rechts neben dem Titel entfallen, wo die Zeile unter dem
  Titel sie zeigt. Diese Zeile nennt jetzt auch „N erledigt“.
- Die Zeichnung meldete dort „Noch keine Aufgaben in dieser Liste.“ – das
  entfällt damit.

**Seitenleiste:**

- „Liste importieren“, „+ Neuer Ordner“, „Bearbeiten“ und „–“ unter dem
  Baum entfallen; der Baum bekommt die volle Höhe.
- „+“ neben „Listen“ öffnet dasselbe Menü wie das „+“ einer Ordnerzeile
  (`folder_quick_add_menu`). Es enthält jetzt auch Neue Seite und Neue
  Galerie, oben zusätzlich „Listen importieren …“.
- Listenzeilen zeigen beim Überfahren „…“ mit Bearbeiten und Löschen.

**Ansichtsumschalter:**

- Liste · Tabelle · Pinnwand stehen fest nebeneinander (`view_switch`).
- Die offene Ansicht trägt die Auswahlfarbe. Vorher wechselten je zwei Knöpfe
  zu den jeweils anderen Ansichten.

**Pinnwand:**

- Aktionen (Anheften, Neue Aufgabe, Bearbeiten, Verbinden, Aktionen) und
  Schalter stehen in einer Zeile (`board_action_buttons`). Erst wenn die
  Breite nicht reicht, rücken die Schalter in eine zweite Zeile. Bei
  Mindestbreite weichen Bearbeiten und Verbinden (beide unter „Aktionen“).
- Eingeschaltete Schalter tragen die Auswahlfarbe statt Grün.
- Spalten teilen sich die sichtbare Breite: breiter bis 1,5 × Kartenbreite,
  schmaler bis 220 Pixel (`COLUMN_STRETCH_MAX`, `COLUMN_MIN_WIDTH`). Erst
  darunter wird quer gescrollt.

**Einzelkorrekturen:**

- **Kästen hinter Text:** „Startseite anpassen“, der Hinweis und
  „AUSGEBLENDET“ sind `CanvasLabel`.
  - Die Suche über 18 Ansichten und Zustände in Dunkel und Hell findet
    danach keine Beschriftung mehr, die als Kasten auf dem Verlauf steht.
  - Gismos Sprechzeile hat keinen Rahmen mehr.
- **Gismo:** Er zeichnet seinen Grund in der Farbe der Fläche darunter statt
  in der Themenfarbe. Auf getönten Kacheln entstand sonst bei jeder
  Animation ein Rechteck.
- **„Erledigt!“:** Die Fahne steigt vom unteren Rand über dem
  Rückgängig-Hinweis auf. Oben lag sie über dem Suchfeld, und macOS zeichnete
  Feld und Schreibmarke darüber.
- **Textlogo:** Es trägt die Akzentfarbe der Oberfläche (`monogram_colors`
  aus `ui_accent`). Die Akzentfarbe steht in den Einstellungen oben neben der
  Logovorschau; die eigene Logofarbe entfällt. `profile_logo_color` bleibt
  lesbar, wirkt aber nicht mehr.
- **Seite ohne Eingabe und Suche:**
  - Die Suchzeile ist auf Seiten ausgeblendet.
  - Nach einer Zeichnung packte `restore_drawing_chrome` die Eingabezeile
    wieder ein, nachdem schon feststand, dass die Seite keine braucht.
    `sync_view_chrome` läuft jetzt auch am Ende jedes Neuaufbaus.

**Seitenbereich „Seiten +“** (`create_pages_sidebar`):

- **Aufbau:**
  - Zwischen Papierkorb und „Listen +“ steht ein eigener Baum
    (`pages_listbox`) mit Seiten ohne Ordner und Bibliotheken samt Inhalt.
  - Seiten in gewöhnlichen Ordnern bleiben bei ihrem Ordner.
  - Die Systemzeile „Seiten“ entfällt; die Überschrift öffnet die Übersicht
    mit Favoriten und Zuletzt.
  - Der Baum ist so hoch wie seine Zeilen (höchstens 8) und verschwindet ohne
    Seiten.
  - Kontextmenü, Doppelklick, Entf und Markierung der offenen Seite arbeiten
    wie im Listenbaum.
- **„+“:** Neue Seite, Aus Vorlage, Neue Bibliothek, Seite aus
  Zwischenablage, Markdown als Seite, Glide-Seiten importieren.
- **Vorlagen:**
  - Bericht, Besprechung und Projektseite sind als Markdown mitgeliefert
    (`PAGE_TEMPLATES`, `{Datum}` wird ersetzt).
  - Eigene Seiten speichert „Als Vorlage speichern“. Der Vorlagensatz trägt
    dafür `list_kind`.
- **Eigenes Format `.glidepage`:**
  - Aufbau wie ein Teilbackup (`data.json` und Anhänge), aber nur Seiten und
    Bibliotheken, gekennzeichnet mit `"content": "pages"`.
  - Export: Seite › Mehr, Kontextmenü von Seite und Bibliothek, Datei ›
    Exportieren › Als Glide-Seite.
  - Import: Datei › Importieren oder „+“.
  - Labels werden zusammengeführt, Kennungen neu vergeben. Eine Datei mit
    Listen weist der Seitenimport ab.
- **Mitbehoben:** Aufgabenmarken `item:<id>` folgen jetzt neuen
  Punktkennungen (`remap_rich_note_items`) – bei Import, Vorlage und
  Duplikat. Vorher waren die Aufgaben einer kopierten Seite von ihren Punkten
  getrennt.

**Galerie** (`list_kind: "gallery"`, Klasse `GalleryView`):

- **Bilder:** Sie sind Anhänge der Liste. Sicherung, Export, Papierkorb und
  Import behandeln sie wie jeden Anhang. Titel und Notiz stehen am Anhang
  (`title`, `note`).
- **Ansicht:**
  - Kachelraster in drei Größen, Anzahl in der Kopfzeile.
  - Doppelklick oder Enter zeigt ein Bild groß in der Fläche selbst, mit
    Titel und Notiz; ◀ ▶ und die Pfeiltasten blättern.
  - Rechtsklick: Groß ansehen, Im System öffnen, Aus der Galerie entfernen
    (mit Rückgängig).
- **Formate:**
  - Tk zeigt PNG und GIF selbst.
  - JPEG, HEIC, WebP, TIFF und BMP wandelt unter macOS das Systemwerkzeug
    `sips` in eine Vorschau (Cache `~/Library/Caches/Glide/galerie`, nicht im
    Datenordner), eine nach der anderen, damit die Oberfläche bedienbar
    bleibt.
  - Anderswo zeigt die Kachel die Dateiendung, und „Im System öffnen“ zeigt
    das Bild.
  - Eine Bildbibliothek wie Pillow bleibt außerhalb der Produktgrenzen.
- **Anlegen:** „+“ neben „Listen“ › Neue Galerie, Datei › Neu anlegen oder
  Listenart Galerie. Die Galerie nimmt keine Punkte auf und hat weder Tabelle
  noch Pinnwand (`is_surface_list`). Die Seitenleiste zählt ihre Bilder.

### 2.13 Kompression, Bibliothekstabelle und Notizbuch (27.09.2026)

**Entscheidungen des Nutzers:**

- **Felder einer Seite:** Titel, Beschreibung, Farbe, Labels, Checkliste
  (die Aufgaben der Seite) und Erstellungsdatum.
- Die Bibliothek erscheint als Tabelle.
- „Tagebuch“ heißt überall „Notizbuch“.
- Titel von Listen, Seiten und Ordnern sind auf 40 Zeichen begrenzt;
  längere werden beim nächsten Start gekürzt.
- Die Beschreibung steht nur unter 50 Zeichen im Kopf, neben den
  Kennzahlen.
- Seiten und Listen klappen mit Pfeilen ein, statt Symbole zu tragen, und
  stehen enger beieinander.
- Die Akzentfarbe heißt in den Einstellungen nur noch „Akzentfarbe der
  Oberfläche“.

**Titelgrenze** (`CONTAINER_TITLE_MAX = 40`):

- `new_list_object` und `new_folder_object` kürzen mit „…“
  (`clip_container_title`); ebenso Umbenennen und der Bearbeiten-Dialog.
- Die Titelfelder nehmen nicht mehr als 40 Zeichen an und zeigen einen
  Zähler (`limit_title_entry`). Eingefügter Text wird bis zur Grenze
  übernommen.
- Beim Laden kürzt die Normalisierung. Vor dem ersten Speichern sichert
  `back_up_before_title_clipping` die Originaldatei als
  `backups/liste_vor_titelkuerzung_<Zeitstempel>.json`, speichert und meldet
  die gekürzten Titel.
  - Scheitert die Sicherung, bekommen die Titel ihren Wortlaut zurück.
- Aufgabentitel bleiben frei.

**Kopf:**

- Die eigene Zeile „Beschreibungstext hinzufügen …“ entfällt. Kennzahlen,
  eine kurze Beschreibung (unter 50 Zeichen, `HEADER_NOTE_MAX`) und der
  Untertitel einer Systemansicht teilen sich die Zeile `page_chip_row`.
- Ein Klick auf die Beschreibung öffnet den Bearbeiten-Dialog.
- Bei Platzmangel kürzt sich zuerst der Untertitel, abschnittsweise hinter
  „ · “ (`shorten_to_width`).

**Seitenleiste:**

- Vor „Seiten“ und „Listen“ steht ein Klapppfeil (▽/▷) statt ▢ und ☷. Der
  Pfeil klappt den Bereich ein; die Überschrift öffnet die Übersicht.
- Der Zustand liegt in `sidebar_sections_closed` (`pages`, `lists`).
- Der Abstand zwischen beiden Bereichen beträgt 10 statt 30 Pixel
  (`SIDEBAR_LISTS_GAP`).

**Bibliothek als Tabelle** (`refresh_library_table`):

- Spalten: Titel, Beschreibung, Farbe, Labels, Aufgaben („1 von 2“),
  Erstellt. Sortieren über die Überschrift, Unterordner stehen oben.
- Die Zeilen tragen dieselben Kennungen wie in der Ordneransicht; Öffnen,
  Kontextmenü und Ziehen bleiben gleich.
- Ansichtsumschalter und „Anzeige“ entfallen dort. Der Hinweis nennt Seiten
  statt Listen.

**Notizbuch:**

- Menüs, Handbuch, Dialoge, Leertexte und die mitgelieferten Vorlagen heißen
  „Notizbuch“.
  - Die Vorlagennamen ziehen auch in bestehenden Vorlagendateien nach.
  - Ein neuer Tageseintrag heißt „Tagesnotiz · Datum“, ein neuer
    Jahresordner „Notizbuch <Jahr>“.
  - Eigene Titel bleiben unverändert.
- Datenschlüssel (`folder_kind: "journal"`, `journal`) bleiben.

**Raster:**

- Notiz, Seite, Zeichnung und Galerie stehen links, rechts und unten im
  selben Abstand zur Karte wie die Aufgabenliste (`CONTENT_INSET`).
- Vorher lagen Werkzeugleiste und Text der Notiz 10 Pixel vom Rand, Datum,
  Knöpfe und Liste darüber 24 Pixel.

**Hinweise** (`add_tooltip`):

- Je Element gibt es eine Anmeldung; ein zweiter Aufruf tauscht nur den
  Text. Knöpfe, die ihren Hinweis bei jeder Aktualisierung neu setzen,
  stapelten vorher mehrere Hinweisfenster übereinander.
- Höchstens ein Hinweis ist sichtbar; jeder Klick, jede Taste und das
  Mausrad schließen ihn.
- Das Fenster steht an seiner Stelle, bevor es erscheint. Vorher wanderte es
  sichtbar von oben links heran.

**Mitbehoben:** Der Leertext der Liste stand über einer Notiz doppelt und
versetzt. Die Beschriftung folgt jetzt der Zeile, solange sie angezeigt wird
(`_place_empty_text`).

## 3. Datenvertrag Format 20

Ein gebündelter Schritt (E-02), mit eigener Migration, Vorsicherung und
Tests.

| Objekt | Feld | Inhalt |
|---|---|---|
| Punkt | `links` | bis 50 Punktkennungen; beidseitig angezeigt, nicht beidseitig gespeichert |
| Punkt | `blocked_by` | bis 50 Kennungen, kreisfrei; Kreise werden beim Laden aufgelöst |
| Punkt | `planned_time` | `HH:MM`, nur zusammen mit `planned_date` |
| Punkt | `time_spent_minutes` | 0 bis 1 000 000 oder `null` |
| Punkt | `done_at` | Zeitpunkt des Abhakens; beim Wiederöffnen `null` |
| Liste, Ordner | `icon` | Zeichendokument 16 × 16 oder `null` |
| Liste | `list_kind: "page"` | Seitenart „Seite“ (26.09.2026, vor der Veröffentlichung additiv ergänzt) |
| Liste | `rich_note.spans` | zusätzlich `table`, `divider`, `task`, `indent1`–`indent3`, `item:<id>` |
| Ordner | `folder_kind: "library"` | Ordnertyp „Bibliothek“ (26.09.2026, additiv) |
| Liste | `list_kind: "gallery"` | Listenart „Galerie“; Bilder in `attachments` (27.09.2026, additiv) |
| Anhang | `title`, `note` | Titel (bis 200 Zeichen) und Notiz (bis 4000) eines Galeriebilds (27.09.2026, additiv) |
| Vorlage | `list_kind` | Listenart der Vorlagenliste; `page` für Seitenvorlagen (27.09.2026) |
| Datei `.glidepage` | `content: "pages"` | Teilbackup nur mit Seiten und Bibliotheken (27.09.2026) |
| Liste, Ordner | `title` | höchstens 40 Zeichen; längere werden beim Laden gekürzt, vorher Sicherung `liste_vor_titelkuerzung_*.json` (27.09.2026) |
| Liste, Ordner | `archived`, `archived_at` | Archivstatus und Zeitpunkt |
| Zeichnung | `drawing.format_version` | 2 für 16/32/64; 128 bleibt 1 |

- `DATA_SCHEMA_VERSION = 20`; lesbare Backups: Formate 4 bis 20.
- Vor dem ersten Schreiben über einem älteren Bestand entsteht
  `liste_vor_format20_<Zeitstempel>.json`.
- **Glide 3.29 nach der Umstellung nicht mehr starten.** 3.29 meldet
  „Speicherdatei beschädigt oder ungültig“, beginnt mit einem leeren Bestand
  und überschreibt die Format-20-Datei bei der ersten Eingabe (Echtdatenprobe,
  Abschnitt 9). Zurück zu 3.29 führt nur die Vorsicherung.
- Seit 3.30 selbst: Ein Bestand aus einer neueren Version öffnet schreibgeschützt
  (`_read_only_reason = "newer_format"`); eine unlesbare Datei wird vor jedem
  Überschreiben als `backups/liste_unlesbar_<Zeitstempel>.json` gesichert.
- Nach dem ersten Speichern mit echtem Inhalt merkt sich Glide
  `data_format_written` in den Einstellungen. Ein frisch angelegter, leerer
  Bestand setzt die Markierung nicht, damit ein danach hineinkopierter
  Altbestand keine Warnung auslöst.
- Findet ein späterer Start eine ältere Datei vor, als hier schon geschrieben
  wurde, warnt er: Eine ältere Version hat gespeichert oder jemand hat eine
  ältere Datei hineinkopiert. Die Warnung nennt den Weg zu den Sicherungen.
- Kopieren, Duplizieren und additiver Import vergeben neue Kennungen und
  ziehen `links`/`blocked_by` nach (`remap_item_references`).
- Der Änderungsverlauf kennt die neuen Felder. Das Erledigt-Datum setzt
  `stamp_done_times` beim Speichern.
- Referenz: `tests/fixtures/current_v20/reference_v20.json`. Die Datei ist ein
  Fixpunkt der Normalisierung.

## 4. Einstellungen (additiv, Einstellungsformat bleibt 2)

Fehlende Werte ergeben das Verhalten von 3.29:

- **Zeichnen, Zeit, Übersicht:** `drawing_tools`, `time_tracking`,
  `library_card_size`, `recent_pages`, `daily_capacity_by_weekday`.
- **Startseite und Angeheftetes:**
  - `home_tile_span` (`wide`),
  - `home_filter_tiles` (höchstens 4),
  - `pinned_pages` (höchstens 20),
  - `home_tiles_330` – Übergangsmerker: neue Kacheln bei gespeicherter
    Reihenfolge einmalig aus.
- **Seitenleiste:** `sidebar_sections_closed` (`views`, `pinned`, `folders`).
- **Gruppierung:** `list_group_by` (je Liste, ohne `list`), `table_nesting`,
  `group_sections_closed`.
- **Detailbereich:** `detail_pane`, `detail_pane_width`.
- **Rückfallerkennung:** `data_format_written` – das zuletzt hier geschriebene
  Aufgabenformat (Ausbau, siehe Abschnitt 3).
- **Stundenraster:** `plan_day_grid` (zweiter Ausbau).
- **Seiten:** `page_favorites` (bis 200 Kennungen), `page_recent` (bis 12),
  `page_full_width` (Lesebreite oder volle Breite).
- **Galerie:** `gallery_tile_size` – je Galerie `small`, `medium` oder
  `large`; andere Werte fallen weg.
- **Seitenleiste:** `sidebar_sections_closed` kennt zusätzlich `pages` und
  `lists` (27.09.2026).
- **Textlogo:** `profile_logo_color` wird seit dem 27.09.2026 nicht mehr
  geschrieben; das Logo folgt `accent_color`.
- **Hintergrund:** `backdrops` – je Design der gewählte Verlauf; unbekannte
  Werte fallen beim Laden weg.
- **Neue Abschnittskennungen in `overview_sections_closed`:**
  `section:timeplan`, `section:untimed`.

## 5. Pinnwandabschnitt (`pinboards`, additiv)

- **Pinnwand:**
  - `layout` um `columns` erweitert;
  - `group_by`, `collapsed`, `hide_empty`, `only_open`;
  - `show_description`, `show_checklist`, `color_mode`
    (`stripe`/`header`/`fill`), `color_source` (`item`/`label`);
  - `areas` (`id`, `name`, `color`, `x`, `y`, `w`, `h`);
  - `auto_connect`, `background`, `print_background`.
- **Karte:** optional `show` mit `description`/`checklist`/`image`.
  Zeichnungskarten tragen `item_id = "page:<Seitenkennung>"`.
- **Verbindung:** optional `label`, `dash`, `color`.
  - Abweichung vom Katalog: Die Strichart heißt `dash`, weil `style` seit 3.24
    die Richtung trägt.
  - Pfeile bleiben Darstellung, keine Aufgabenabhängigkeit.
- **Ältere Fassungen:**
  - Sie lesen `columns` als „Frei anordnen“ und zeichnen einfache Linien.
  - Unbekannte Schlüssel verwerfen sie beim nächsten Speichern.
  - Zeichnungskarten verschwinden dort beim Aufräumen der Karten.
- **Additiver Import:**
  - Bereiche bekommen neue Kennungen.
  - Zeichnungskarten, eingeklappte Listenspalten und Verbindungen folgen den
    neuen Kennungen.
  - Ein Spaltenboard und eine Pinnwand mit Bereichen reisen auch ohne
    angeheftete Karten.

## 6. Rückgängig

- **Zeichenfläche:** eigener Aktionspuffer (siehe 2.1). Strukturaktionen
  (Nachzeichnen, Ersetzen, Leeren, Referenzwechsel) bleiben globale Schritte.
- **Punktänderungen:** Spaltenboard, Gruppen-Ziehen, Detailbereich, Karten-
  Checkliste und Weiterdenken laufen über `item_change` – je ein Schritt.
- **Flächenänderungen der Pinnwand:** Aufräumen, Bereich anlegen, verschieben,
  vergrößern und entfernen legen einen Ansichtsschritt an
  (`board_view_change`). Er ist über den Hinweis und über Strg/Cmd+Z
  zurücknehmbar, solange danach keine Punktänderung kam.
- **Kartenpositionen** beim einfachen Ziehen bleiben wie bisher ohne
  Rückgängig.

## 7. Architektur

- **`drawing.py`:**
  - `DrawingModel` mit Aktionspuffer (`begin_action`/`end_action`/`action()`)
    und Größen 16–128;
  - Formen, Symmetrie, Muster, Bereiche, PNG-Kodierung, Paletten-Ein- und
    -Ausgabe.
- **`drawing_image.py`:** Miniaturen (`thumbnail_photo`) und Graustufen.
- **`DrawingEditor`:** Kontextleiste, Farbleiste, Vorschau und Auswahl, in der
  Seitenanzeige eingebettet.
- **Gruppierung** an einer Stelle:
  - `group_columns`, `item_group_keys` und `set_group_value` für Spaltenboard,
    Liste und Tabelle;
  - `date_group_target` bestimmt den gesetzten Tag.
- **`ItemWorkspace`:**
  - Spaltenboard (`draw_columns`, `column_*`), Bereiche (`area_*`),
    Ansichts-Undo, Weiterdenken, Verbindungsgestaltung, Hintergrund,
    Präsentation;
  - `valid_cards` = Punkte plus Zeichnungsseiten.
- **Leistengrenzen:** Zeichnung, Startseite und Pinnwand blenden Leisten
  unabhängig aus.
  - `_refresh_tree` gibt die Leisten einer Zeichnung jetzt zurück, bevor die
    Pinnwand sie ordnet.
  - Bei ausgeblendeter Listenoberfläche wandern sie in die Merkliste der
    Startseite (siehe 9).
- **Eingebettet statt Zusatzfenster:**
  - Startseitenbearbeitung, Suche, Detailbereich, Tagesbeginn, Wochenrückblick
    und Präsentation liegen in der Seitenanzeige.
  - Kleine modale Dialoge (Platzhalter, Zeitraum, Momentdatum) laufen über
    `run_modal`.

## 8. Abweichungen vom Katalog

1. ST-010: Breite „normal“ oder „ganze Breite“ statt 1–3 Rasterspalten.
2. MO-010: Der Dialog „Aktionen“ bleibt; die Suche Strg/Cmd+O kommt dazu.
3. Tagesbeginn und Wochenrückblick sind Unterseiten der Startseite.
4. ZD-080: Zwischenstände als Anhang (E-12), ohne Formatänderung.
5. ZD-130: pixelgenau über die Zelle unter dem Zeiger plus Bresenham.
6. PW-010: Reihenfolge der Anordnungen Geordnet · Spalten · Frei (Frei bleibt
   der letzte Eintrag wie bis 3.29). Zeichnungskarten erscheinen nicht im
   Spaltenboard.
7. PW-060: Strichart-Schlüssel `dash` (siehe 5).
8. AO-040: In Liste und Tabelle steht ein Punkt mit mehreren Labels unter
   seinem ersten Label; eine Baumzeile gibt es nur einmal. Das Spaltenboard
   zeigt ihn in jeder Labelspalte.
9. MO-030: In der Liste behält Enter seine Bedeutung (abhaken); der Bereich
   folgt der Auswahl. In der Tabelle öffnet Enter den Bereich.
10. MO-050: Gismo nur als stiller Auftritt (Stufe 2 der Reihenfolge). Ein
    führender Begleiter mit Hinweisen setzt ein Endnutzer-Onboarding voraus,
    das nicht gewählt ist.
11. MO-060: die Pixelschrift nur für Seitentitel und Kachelköpfe; Fließtext
    bleibt in der Oberflächenschrift.
12. AO-070 und MO-080 in zweiter Stufe: Zeitblöcke werden in der Zeitplanliste
    gezogen (die Zeilenhälfte entscheidet) und seit dem zweiten Ausbau auch
    im Stundenraster, seit dem dritten Ausbau auch aus der Liste ins Raster.
    Folien entstehen als Druckseite; das PDF erzeugt der Druckdialog des
    Browsers.

## 9. Mitbehobene Befunde

- Verbindungslinien stapelten sich beim Ziehen einer Karte, weil
  `draw_connections` die alten Linien nicht entfernte.
- Startseite → neue Zeichnung → Startseite ließ die Eingabezeile bis zum
  Neustart verschwinden (Tk-Fehler „isn't packed“ beim Wiedereinblenden, still
  abgefangen). Zeichnung → Pinnwand-Liste ließ sie über der Fläche stehen.
  Beides war schon in 3.29.0 vorhanden.
- „Ansicht › Liste › Zur Listenansicht“ meldete aus der Tabelle „keine Liste
  geöffnet“.
- Beim Schließen liefen Kopfzeilen-Aktualisierung und Zuletzt-geöffnet-Speicherung
  in bereits zerstörte Widgets.

Beim Ausbau gefunden und behoben:

- **Datenverlust beim Öffnen mit einer älteren Version.** Konnte Glide die
  Speicherdatei nicht lesen – beschädigt oder aus einer neueren Version –,
  begann es leer und überschrieb die Datei beim ersten Speichern. So verliert
  Glide 3.29 einen Format-20-Bestand (Echtdatenprobe mit einer Kopie). In 3.30
  gilt:
  - ein neueres Format öffnet schreibgeschützt;
  - eine unlesbare Datei wird zuerst gesichert;
  - die Rückfallerkennung warnt, wenn eine ältere Version zwischendurch
    geschrieben hat.

  3.29 selbst lässt sich nicht mehr ändern; die Übergabe und die Prüfliste
  warnen davor.
- **Kaputtes JSON verhinderte jedes Speichern.** Die Formatsicherungen lasen
  die Datei bei jedem Speichern erneut und scheiterten daran. Nach der Kopie
  nach `liste_unlesbar_*` entfallen sie für diese Sitzung.
- **Leere `window.conf`.** Ein zweites Beenden – Cmd+Q während der
  Speicherabfrage oder ein von macOS nachgereichtes Beenden – öffnete die
  Datei zum Schreiben, bevor die Fenstergröße am zerstörten Fenster scheiterte.
  Der nächste Start verlor die Position. Gefunden als leere Datei im echten
  Datenordner. `on_close` läuft jetzt nur einmal, und `save_window_geometry`
  schreibt atomar.

Beim dritten Ausbau gefunden und behoben:

- **„Pinnwand öffnen“ aus der Tabelle.** Der Befehl im Menü „Ansicht ›
  Pinnwand“ und im Kontextmenü des leeren Listenbereichs rief die Pinnwand
  direkt auf. In der Tabellenansicht meldete er deshalb „Zuerst eine Liste
  oder einen Ordner öffnen“, obwohl eine Liste offen war. Beide nutzen jetzt
  `open_board_view`, das den Fall schon kannte.
- **Doppelter Titel in der Baumspalte der Tabelle.** Gruppiert oder
  verschachtelt zeigte die 40 px schmale Spalte den abgeschnittenen Titel
  neben der Titelspalte; dort steht jetzt die Nummer.

Bei der Überarbeitung für kleine Fenster gefunden und behoben:

- **Titel nach Schriftwechsel zu lang.** Die Messschrift für das Kürzen des
  Seitentitels blieb nach einem Wechsel der Schriftgröße auf dem alten Stand.
  Bei „groß“ ragte der Titel deshalb über seinen Platz.
- **Titel nach Größenwechsel falsch gekürzt.** Die Kürzung las die
  Wunschbreite der Kennzahlen, die Tk erst im Leerlauf nachrechnet
  (`packed_width` misst jetzt die Kinder).
- **„Raster“ bei großer Schrift gequetscht.** Die Pinnwandleiste nutzte eine
  feste Schwelle von 620 px.
- **Kurze Höhenmeldung beim Neuaufbau.** Tk meldet beim Seitenwechsel kurz
  1 px Höhe; die Höhenstufe ignoriert das.

In der Runde mit Dialogen, Kontrast, Raster und Paketierung gefunden und
behoben:

- **„In Liste verschieben …“ stürzte ab.** Der Aufruf übergab die
  Listenfarben als Wörterbuch nach Kennung, der Auswahldialog griff mit der
  Position zu (`KeyError: 0`); der Dialog erschien nie.
  `themed_choice_dialog` nimmt jetzt beides.
- **Kalender, Punktmaske, Aufklapppfelder, „Über Glide“ bei großer
  Schrift:** siehe Abschnitt 2.5, Dialoge.
- **Kontrast:** siehe Abschnitt 2.6.

## 10. Prüfung

- Neue Suiten: `tests/integration/test_drawing330.py` (Kern) und
  `test_features330.py` (Oberfläche und Datenwege aller Pakete, einschließlich
  Regressionen der mitbehobenen Befunde).
- Angepasst:
  - `test_features322` – Übergangsmerker der Startseite im Normalisierungstest;
  - `test_features323` – fünfte Farbschicht;
  - `test_datenintegritaet` – neue Maskenfelder;
  - `test_features329` – bestätigt die neue Importvorschau;
  - Versionsliterale in `test_glide`, `test_glide_36`, `test_features329`.
- Neu erzeugt:
  - `current_v20`;
  - `glide_beispieldaten.glidebackup` mit einer Format-20-Liste und einer
    archivierten Liste;
  - `glide_releaseplanung_3.30.0.glidebackup`;
  - die Praxisvorlagen.
- Vollprüfung am 25.09.2026
  ([Protokoll](../tests/qa-3.30.0/abschluss_2026-09-25/ergebnis.json)):
  **Exitcode 0**, alle 52 automatisierten Schritte bestanden. Einzelheiten und
  die offenen manuellen Prüfungen stehen im [QA-Bericht](07_QA_BERICHT.md).
- Ausbau: `test_features330.py` prüft zusätzlich:
  - Zeitblöcke per Ziehen und Alt+↑/↓;
  - Karten-Rückgängig;
  - Folien- und Notizfolien-Druckseite;
  - den vollständigen Detailbereich;
  - Gismo im Leerzustand;
  - Pixelschrift samt Prüfsummen;
  - neuere und unlesbare Speicherdatei;
  - die Rückfallerkennung;
  - doppeltes Beenden;
  - aus dem zweiten Ausbau: Anhänge im Detailbereich, Zeichnungs-PNG in der
    Druckseite, Gruppierung mit Überschriften und durchgehender Nummerierung,
    Stundenraster einschließlich Ziehen und Rückgängig;
  - aus dem dritten Ausbau:
    - Ziehen eines Punkts ohne Uhrzeit aus der Liste ins Raster, mit
      Vorschaulinie und Rückgängig;
    - Nummern und Überschriften der gruppierten Tabelle, auch ohne
      Überschriften bei Spaltensortierung;
    - „Pinnwand öffnen“ aus der Tabelle;
    - die Linux-Registrierung mit nachgebildetem Fontconfig, samt Rückfall
      ohne Bibliothek;
  - aus der Überarbeitung für kleine Fenster: die sortierte gruppierte
    Tabelle mit Überschriften.
- `test_mindestgroesse330.py`: 75 Ansichten und 43 Dialogaufrufe ohne Befund
  bei Mindestgröße, dazu Höhenstufen und Tabellenspalten (Abschnitt 2.5).
- `test_kontrast330.py`: rund 13.700 Paare aus Schrift und Fläche in zehn
  Designs, keines unter WCAG AA (Abschnitt 2.6).
- `test_paketierung330.py`: Kennungen, Windows-Skript, und unter macOS das
  gebaute, gültig signierte Bundle (Abschnitt 2.7).
- `test_hintergrund330.py`: 50 Entwürfe, Lesezone, Einbau in drei Designs,
  Glas, Menü, Zwischenspeicher, Abschalten und die Auswahl in den
  Einstellungen (Abschnitt 2.8).
  - Seit der Rückmeldung auch: Schrift statt Pille, Milchglas für Kacheln,
    Listen und Fenster, Glanz im Innenrand, Bindtags der Hintergrundbilder.
  - Der Start im schmalen Fenster läuft als eigener Prozess. Mit dem alten
    Bindtag endet er mit Signal −10, der Test erkennt das.
- `test_rueckmeldung330.py`: Unterkanten in sieben Ansichten,
  Kopfzeilenreihenfolge über Dichtewechsel, Verlauf als Knopf und Karte,
  Seitenleiste, „In Bearbeitung“ in „Mein Tag“, ruhige Zeichenfläche und
  Auswahl (Abschnitt 2.9).
  - Seit der zweiten Rückmeldung zusätzlich (Abschnitt 2.10):
    - Farbregel, Kennzahlen als Text, „Startseite anpassen“ unten;
    - Eingabe und Leisten je Ansicht;
    - „Erledigte Punkte löschen“ samt Rückgängig, gepackter Rückgängig-
      Speicher;
    - Punktdialog mit Verlauf ohne Endlosschleife;
    - kein Neuzeichnen beim Verschieben.
- `test_seiten330.py`:
  - Markdown-Rundlauf;
  - Seite aus Markdown mit echten Aufgaben, einplanbar in „Mein Tag“;
  - Editor: Abhaken, Titel, Enter, Löschen und Rückgängig, Kürzel, Einfügen;
  - Export, Seitenübersicht, Ordnertypen, Speichern (Abschnitt 2.11).
- `test_features330.py` zusätzlich: Raster statt Liste im schmalen Fenster,
  Einplanen über „Mein Tag“ in der Seitenleiste.
- `test_ui_followup36` scrollt seit dem Lasttest vom 26.09.2026 vor jeder
  Messung erneut zur Karte; die Wiederholung unter vierfacher Last war 4/4
  grün (Abschnitt „Prüfläufe“ im QA-Bericht).
- Windows-Prüfpaket: `tests/tools/windows_vollpruefung.cmd` und `.ps1`,
  Anleitung in `00_Arbeitsvorbereitung/Checklisten/Windows_Pruefung_3.30.0.md`.
- Abschlusslauf nach dem Ausbau am 26.09.2026
  ([Protokoll](../tests/qa-3.30.0/ausbau_abschluss_2026-09-26/ergebnis.json)):
  **Exitcode 0**, alle 52 Schritte. Die Zwischenläufe und ihre Korrekturen
  stehen im [QA-Bericht](07_QA_BERICHT.md).
- Vollmodus nach dem zweiten Ausbau am 26.09.2026
  ([Protokoll](../tests/qa-3.30.0/ausbau2_2026-09-26/ergebnis.json)):
  **Exitcode 0**, alle 52 Schritte ohne parallele Last.
- Vollmodus nach dem dritten Ausbau am 26.09.2026
  ([Protokoll](../tests/qa-3.30.0/ausbau3_2026-09-26/ergebnis.json)):
  **Exitcode 0**, alle 52 Schritte.
- Vollmodus nach der Überarbeitung für kleine Fenster am 26.09.2026
  ([Protokoll](../tests/qa-3.30.0/mindestgroesse_2026-09-26/ergebnis.json)):
  **Exitcode 0**, alle 53 Schritte mit 38 Suiten.
- Vollmodus nach Dialogen, Kontrast, Raster und Paketierung am 26.09.2026
  ([Protokoll](../tests/qa-3.30.0/kontrast_paketierung_2026-09-26/ergebnis.json)):
  **Exitcode 0**, alle 55 Schritte mit 40 Suiten.
- Vollmodus nach den Hintergrundverläufen am 26.09.2026
  ([Protokoll](../tests/qa-3.30.0/hintergrund_2026-09-26/ergebnis.json)):
  **Exitcode 0**, alle 56 Schritte mit 41 Suiten.
- Vollmodus nach der Rückmeldung am 26.09.2026
  ([Protokoll](../tests/qa-3.30.0/rueckmeldung_2026-09-26/ergebnis.json)):
  **Exitcode 0**, alle 57 Schritte mit 42 Suiten.
- Vollmodus nach der zweiten Rückmeldung am 26.09.2026
  ([Protokoll](../tests/qa-3.30.0/rueckmeldung2_2026-09-26/ergebnis.json)):
  **Exitcode 0**, alle 57 Schritte mit 42 Suiten.
- Vollmodus nach Seiten und Ordnertypen am 27.09.2026
  ([Protokoll](../tests/qa-3.30.0/seiten_2026-09-27/ergebnis.json)):
  **Exitcode 0**, alle 58 Schritte mit 43 Suiten.
- Vollmodus nach Aufräumen, Seitenbereich und Galerie am 27.09.2026
  ([Protokoll](../tests/qa-3.30.0/aufraeumen_2026-09-27/ergebnis.json)):
  **Exitcode 0**, alle 59 Schritte mit 44 Suiten. Ein erster Lauf
  ([Protokoll](../tests/qa-3.30.0/aufraeumen_erster_lauf_2026-09-27/ergebnis.json))
  scheiterte einmal in `test_glide`; vier Einzelläufe blieben grün.
- Vollmodus nach der Kompression am 27.09.2026
  ([Protokoll](../tests/qa-3.30.0/kompression_2026-09-27/ergebnis.json)):
  **Exitcode 0** im ersten Lauf, alle 60 Schritte mit 45 Suiten – maßgeblicher
  automatisierter Nachweis.
- **Echtdatenprobe** (mit Zustimmung, nur mit einer Kopie in einem
  temporären Ordner):
  - 6 Seiten und 138 Punkte, nach der Umstellung inhaltlich gleich;
  - Vorsicherung bytegleich, keine Meldung, kein Tk-Fehler;
  - das Original unverändert (SHA-256 vorher und nachher).

## 11. Bekannte Grenzen

- **Pixelschrift unter Linux:** Die Registrierung über Fontconfig ist nur
  mit nachgebildeter Bibliothek geprüft, nicht auf einem echten
  Linux-Desktop.
- **Mindestgröße und Kontrast:** Die Messungen decken Überstand,
  Quetschung, Anschnitt und den Kontrast von Widgets ab. Nicht gemessen
  werden Texte auf Zeichenflächen (Pinnwandkarten, Kalenderzellen im
  Kalender-Canvas, Startseiten-Grafiken) und die Wirkung auf dem echten
  Bildschirm; das bleibt Teil der manuellen Prüfung.
- **Stundenraster:** Aus anderen Listen wird über „Mein Tag“ in der
  Seitenleiste eingeplant, nicht direkt auf eine Uhrzeit; die Uhrzeit folgt
  im Raster.
- **Hintergrundverläufe:**
  - Die Kacheln sind nicht wirklich durchscheinend; Tk kann das nicht. Das
    Milchglas ist eine flache Tönung je Kachel. Eine sehr große Kachel wie
    die Liste zeigt deshalb nur eine Farbe, keinen Verlauf.
  - In den hellen Designs fällt die Tönung schwach aus, weil die graue
    Nebenschrift auf der Kachel 4,5:1 halten muss.
  - In den hellen Designs bleibt die Lesezone fast farblos, weil die graue
    Unterzeile dort schon knapp über 4,5:1 liegt.
  - Unter Windows ist die Darstellung noch nicht am Gerät geprüft.
- **Seiten:**
  - Blöcke lassen sich nicht einzeln mit der Maus ziehen (Weg A); Ordnen
    geht über Ausschneiden und Einfügen.
  - Tabellen sind ausgerichteter Text in Festbreitenschrift und keine
    Zellen.
  - Titelbild, Unterseiten und Glide-weite Felder folgen in der nächsten
    Stufe.
  - Ein Titel mit mehreren Zeilen wird in der Seite einzeilig.
  - Seiten lassen sich im Seitenbereich nicht mit der Maus in eine
    Bibliothek ziehen; Verschieben geht über das Kontextmenü.
- **Galerie:**
  - Ohne Bildbibliothek zeigt Glide JPEG, HEIC und WebP nur unter macOS als
    Vorschau (über `sips`). Unter Windows und Linux steht dort die
    Dateiendung, und das Bild öffnet im Systembetrachter.
  - Bilder kommen über „Bilder hinzufügen …“. Ziehen aus dem Finder oder
    Explorer bräuchte eine zusätzliche Tk-Erweiterung.
  - Die Großansicht verkleinert in ganzzahligen Stufen; sie vergrößert kleine
    Bilder nicht.
- **Paketierung:** Das Entwicklungsbundle braucht das installierte Python
  von python.org und ist nur ad hoc signiert. Das Windows-Skript ist
  ungeprüft.
- **Importvorschau in Tests:** Seit 3.30 zeigt der Zeichnungsimport eine
  Vorschau (ZF-050). Tests, die den Import aufrufen, müssen sie bestätigen.
  `test_features329` wartete deshalb zunächst auf eine Eingabe und ist
  entsprechend angepasst.
