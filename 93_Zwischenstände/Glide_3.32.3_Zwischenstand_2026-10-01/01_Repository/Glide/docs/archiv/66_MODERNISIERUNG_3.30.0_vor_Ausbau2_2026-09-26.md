# Modernisierung 3.30.0 – Pixel-Werkstatt, Format 20, Startseite, Board

Stand 25.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

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
  - Die Tabelle zeigt Unterpunkte auf Wunsch verschachtelt (AO-030).
    Elternpunkte eines Treffers bleiben dabei abgeschwächt stehen.
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
  - Seit dem Ausbau alle Felder außer den Anhängen: Titel (Long-Task
    mehrzeilig), Erledigt, Wichtigkeit, Art, Farbe, Fälligkeit, Wiederholung,
    Erinnerung, Bearbeitungstag mit Uhrzeit, Aufwand, erfasste Zeit, Labels,
    Beschreibung, Checkliste (anfügen, abhaken, entfernen), „Verknüpft mit“
    und „Wartet auf“ mit Kreisprüfung. Der Bereich scrollt.
  - Ein Wechsel zu Gruppe oder Überschrift fragt nach, wenn der Punkt
    Planungsfelder trägt – in der Maske sieht man deren Wegfall vor dem
    Bestätigen, hier wirkt die Wahl sofort.
  - Maske und Bereich teilen `read_repeat_rule` und `add_relation_targets`;
    den Erinnerungseditor übernimmt der Bereich aus der Maske.
  - „Alle Felder …“ öffnet die Punktmaske – für Anhänge.
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
  - Ist die Schrift nicht registriert (etwa unter Linux), bleibt die
    Oberflächenschrift.
- **Verknüpfungen, Abhängigkeiten, Zeit:** in der Maske im Abschnitt
  „Beziehungen und Zeit“ und im Kontextmenü „Beziehungen und Zeit“.
  - Ein wartender Punkt fragt vor dem Abhaken nach und steht in der
    Dringlichkeit auf Rang 4.
  - Die laufende Zeiterfassung zeigt der Kopf.

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
    gezogen (die Zeilenhälfte entscheidet), nicht in einem Stundenraster.
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
  - doppeltes Beenden.
- Abschlusslauf nach dem Ausbau am 26.09.2026
  ([Protokoll](../tests/qa-3.30.0/ausbau_abschluss_2026-09-26/ergebnis.json)):
  **Exitcode 0**, alle 52 Schritte. Die Zwischenläufe und ihre Korrekturen
  stehen im [QA-Bericht](07_QA_BERICHT.md).
- **Echtdatenprobe** (mit Zustimmung, nur mit einer Kopie in einem
  temporären Ordner):
  - 6 Seiten und 138 Punkte, nach der Umstellung inhaltlich gleich;
  - Vorsicherung bytegleich, keine Meldung, kein Tk-Fehler;
  - das Original unverändert (SHA-256 vorher und nachher).

## 11. Bekannte Grenzen

- **Detailbereich:** Anhänge bleiben in der Maske („Alle Felder …“).
- **Zeitplan:** kein Stundenraster; freie Uhrzeiten setzt das Feld
  „Bearbeitungstag“ in Bereich oder Maske.
- **Folien:** Zeichnungskarten erscheinen als beschriftete Karte ohne
  Miniatur.
- **Pixelschrift:** unter Linux nur, wenn „Pixelify Sans“ systemweit
  installiert ist; sonst gilt die Oberflächenschrift.
- **Gruppierung in der Liste:**
  - Zwischenüberschriften lösen sich auf.
  - Die Nummerierung beginnt je Abschnitt neu.
- **Importvorschau in Tests:** Seit 3.30 zeigt der Zeichnungsimport eine
  Vorschau (ZF-050). Tests, die den Import aufrufen, müssen sie bestätigen.
  `test_features329` wartete deshalb zunächst auf eine Eingabe und ist
  entsprechend angepasst.
