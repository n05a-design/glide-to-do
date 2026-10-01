# Glide – Aufgabenkatalog: Modernisierung, Pinnwand-Board, Ordner und Pixel-Werkstatt

Stand 25.09.2026 · umgesetzt mit Glide 3.30.0 · Aufgabenformat 20

> **Gesamtstatus: umgesetzt mit Glide 3.30.0 (25.09.2026).** Die Entscheidungen
> E-01 bis E-16 folgen der Empfehlung. Umfang, Datenvertrag und Abweichungen:
> [Vertrag Modernisierung 3.30](../01_Repository/Glide/docs/66_MODERNISIERUNG_3.30.0.md).
> AO-070 und MO-080 sind seit dem Ausbau am selben Tag auch in zweiter Stufe
> umgesetzt (Zeitblöcke ziehen, Folien als PDF). Dazu kamen Gismo in
> Leerzuständen (MO-050), die Pixelschrift (MO-060), Karten-Rückgängig und
> der vollständige Detailbereich (MO-030).
>
> Grundlage sind die
> [Wettbewerbsrecherche](Glide_Wettbewerbsrecherche_Modernisierung_2026-09-25.md)
> und die [Arbeitsvorbereitung](Glide_Arbeitsvorbereitung_Modernisierung_2026-09-25.md)
> vom 25.09.2026. Rahmenbedingungen, Datenklassen (D0–D3), Entscheidungen
> (E-01 bis E-16), Etappen und die Definition von „fertig“ stehen dort und
> werden hier nicht wiederholt.

Die Kennungen sind stabile Referenzen. Präfixe: **ST** Startseite, **MO**
allgemeine Modernisierung, **PW** Pinnwand, **AO** Aufgaben und Ordner, **ZD**
Zeichnen und Design. Die **Priorität** beschreibt den Nutzen (P1 hoch, P2
mittel, P3 beobachten). Die **Etappe** beschreibt die Reihenfolge nach
Abhängigkeiten. Aufwand: **S** klein, **M** mittel, **L** groß, **XL** sehr
groß – eine Reihenfolgehilfe, keine Zeitschätzung.

## 1. Übersicht

| Kennung | Prio | Arbeitspaket | Aufwand | Daten | Entscheidung | Abhängig von | Etappe | Status |
|---|---|---|---|---|---|---|---|---|
| MO-020 | P1 | Anklickbare Pfadzeile über dem Seitentitel | S | D0 | – | – | A | umgesetzt 3.30.0 |
| MO-040 | P1 | Rückgängig direkt in der Rückmeldung | S | D0 | – | – | A | umgesetzt 3.30.0 |
| MO-010 | P1 | Seiten- und Befehlssuche mit Tastenkürzel | M | D1 | E-03 | – | A | umgesetzt 3.30.0 |
| ZD-010 | P1 | Kontextleiste für den Zeichen-Editor | M | D0 | – | – | A | umgesetzt 3.30.0 |
| ZD-020 | P1 | Zwei Farben, Rechtsklick und Farbleiste | M | D1 | – | ZD-010 | A | umgesetzt 3.30.0 |
| ZD-030 | P1 | Zoom mit Mausrad und Verschieben | S | D0 | – | – | A | umgesetzt 3.30.0 |
| ZD-040 | P1 | Eingebettete Vorschau in Originalgröße | S | D0 | – | – | A | umgesetzt 3.30.0 |
| ZD-120 | P1 | PNG-Export in ganzzahligen Größen | S | D0 | E-13 | – | A | umgesetzt 3.30.0 |
| ST-030 | P1 | Kachel „Zeichnungen“ mit Miniaturen | S–M | D1 | – | – | A | umgesetzt 3.30.0 |
| ST-010 | P1 | Startseite direkt anpassen | M | D1 | – | – | B | umgesetzt 3.30.0 |
| ST-020 | P1 | Gespeicherten Filter als Kachel anheften | M | D1 | – | – | B | umgesetzt 3.30.0 |
| ST-040 | P1 | Angeheftete Seiten in Seitenleiste und Startseite | M | D1 | – | – | B | umgesetzt 3.30.0 |
| ST-050 | P2 | Zuletzt geöffnet neben zuletzt bearbeitet | S | D1 | – | – | B | umgesetzt 3.30.0 |
| AO-010 | P1 | Übersichten als Galerie mit Vorschau | M | D1 | – | ST-030; Tagebuchteil ZF-120 | B | umgesetzt 3.30.0 |
| AO-020 | P2 | Schnellaktionen und Abschnitte in der Seitenleiste | M | D1 | – | ST-040 | B | umgesetzt 3.30.0 |
| PW-010 | P1 | Spaltenboard nach Feld mit Ziehen | L | D2 | E-07, E-16 | AO-040 (gemeinsame Logik) | C | umgesetzt 3.30.0 |
| AO-040 | P2 | Liste und Tabelle nach Feld gruppieren | M | D1 | – | – | C | umgesetzt 3.30.0 |
| PW-020 | P1 | Karteninhalt und Kartenfarbe wählbar | M | D2 | – | ST-030 (Miniaturen) | C | umgesetzt 3.30.0 |
| ZF-100 | P1 | Zeichnung als Pinnwandkarte (bestehend) | M | D2 | – | PW-020 | C | umgesetzt 3.30.0 |
| PW-030 | P1 | Benannte Bereiche auf der Pinnwand | L | D2 | – | – | C | umgesetzt 3.30.0 |
| PW-040 | P2 | Auswahl aufräumen | S | D0 | – | – | C | umgesetzt 3.30.0 |
| PW-050 | P2 | Schnell weiterdenken: Nachbarkarte und Verbinden per Ziehen | M | D2 | E-08 | – | C | umgesetzt 3.30.0 |
| PW-060 | P2 | Verbindungen beschriften und gestalten | M | D2 | – | – | C | umgesetzt 3.30.0 |
| PW-070 | P2 | Flächenhintergrund Punkte, Linien, Karo | S | D2 | – | – | C | umgesetzt 3.30.0 |
| ZD-070 | P1 | Rückgängig je Aktion | M | D0 | E-11 | – | D | umgesetzt 3.30.0 |
| ZD-050 | P1 | Symmetrisch zeichnen | M | D1 | – | ZD-070 | D | umgesetzt 3.30.0 |
| ZD-060 | P2 | Linie, Rechteck und Ellipse | M | D0 | E-10 | ZD-070, ZD-010 | D | umgesetzt 3.30.0 |
| ZD-100 | P2 | Farbe in der ganzen Zeichnung ersetzen | S | D0 | – | ZD-020, ZD-070 | D | umgesetzt 3.30.0 |
| ZD-110 | P2 | Kachelmodus für Muster | M | D1 | – | ZD-040 | D | umgesetzt 3.30.0 |
| ZD-130 | P2 | Pixel-perfekte Linie | S–M | D1 | – | ZD-070 | D | umgesetzt 3.30.0 |
| ZD-150 | P2 | Graustufenansicht und Referenzdeckkraft | S | D1 | – | – | D | umgesetzt 3.30.0 |
| ZD-090 | P2 | Palettenbibliothek mit Import und Export | M | D1 | E-15 | ZD-020, ZF-210 | D | umgesetzt 3.30.0 |
| ZD-140 | P1* | Flächengrößen 16, 32, 64 und 128 | L | D3 | E-14, E-02 | – | E | umgesetzt 3.30.0 |
| AO-050 | P1* | Pixelsymbol für Listen, Ordner und Seiten | L | D3 | E-09, E-02 | ZD-140 | E | umgesetzt 3.30.0 |
| ZD-080 | P2 | Benannte Zwischenstände | M–L | D3 oder Anhang | E-12 | – | E | umgesetzt 3.30.0 |
| MO-070 | P3 | Archivieren statt Löschen | M–L | D3 | E-06, E-02 | – | E | umgesetzt 3.30.0 |
| MO-030 | P2 | Eingebetteter Detailbereich neben der Liste | XL | D1 | E-04 | – | später | umgesetzt 3.30.0 |
| MO-050 | P2 | Leerzustände mit nächstem Schritt | M | D0 | Arbeitsbegleiter Stufe 3 | – | später | umgesetzt 3.30.0 |
| MO-060 | P2 | Visuelle Richtung „Pixel“ | M | D1 | E-05 | ZF-210 | später | umgesetzt 3.30.0 |
| AO-030 | P2 | Tabelle mit verschachtelten Unterpunkten | M | D1 | – | – | später | umgesetzt 3.30.0 |
| AO-060 | P3 | Kompakte Eigenschaften im Seitenkopf | S | D0 | – | MO-020 | später | umgesetzt 3.30.0 |
| AO-070 | P3 | Tagesplan mit Zeitblöcken | L | D3 (`planned_time`) | – | – | später | umgesetzt 3.30.0 (zwei Stufen) |
| MO-080 | P3 | Präsentationsmodus | L | D0 | – | PW-030 | später | umgesetzt 3.30.0 (zwei Stufen) |
| ZD-160 | P3 | Auswahl, Verschieben und Kopieren von Bereichen | L | D0 | – | ZD-070 | später | umgesetzt 3.30.0 |
| ZD-170 | P3 | Dithering und Musterfüllung | M | D0 | – | ZD-090 | später | umgesetzt 3.30.0 |

Bei AO-070, MO-080, ZD-160 und ZD-170 stand die Datenklasse bei der Planung
noch offen; eingetragen ist die tatsächlich umgesetzte.

\* P1 unter der Voraussetzung, dass E-14 beziehungsweise E-09 zustimmend
entschieden wird.

## 2. Einordnung der bestehenden offenen Kennungen

Die [Aufgabensammlung Zeichenfläche](Glide_Aufgabensammlung_Zeichenflaeche_2026-09-23.md)
bleibt für ihre Kennungen maßgeblich. Dieser Katalog ersetzt keine davon,
sondern ordnet sie ein:

| Bestehend | Einordnung |
|---|---|
| ZF-100 Pinnwand-Referenz | Umgesetzt mit 3.30.0 (Zeichnungskarte `page:`, Miniatur, Rückweg). |
| ZF-120 Rest (alle Inhaltsarten im Tagebuch, Tages- und Zeitraumfilter) | Umgesetzt mit 3.30.0. |
| Anlageoption „Pinnwand“ (Rest ZF-015) | Umgesetzt mit 3.30.0: eine Aufgabenliste, die als Fläche startet. |
| ZF-050 Rest (Einfügen aus Text, Importvorschau) | Umgesetzt mit 3.30.0. |
| ZF-110 Dokumentation und Releaseprüfung | Unverändert; gilt für jede Etappe sinngemäß. |
| ZF-200 Plattformlücken | Bereiche → PW-030, Präsentation → MO-080. Verknüpfte Punkte, echte Abhängigkeiten, Tagesbeginn und Wochenrückblick sowie Vorlagen mit Eingabefeldern sind mit 3.30.0 umgesetzt (Auswahl vom 25.09.2026). Eigene Felder (nicht gewählt) und Systembenachrichtigungen bleiben in ZF-200. |
| ZF-210 Inhaltspalette | Umgesetzt mit 3.30.0 („Glide 32“). |
| ZF-300 erweiterte Zeichenfunktionen | PNG-Ausgabe → ZD-120, Gerade und Rechteck → ZD-060, Auswahl und Verschieben → ZD-160, Dithering und Musterfüllung → ZD-170. Text- und Vektorobjekte, Fremd-SVG, Stift und Touch, Großflächen, Ebenen und Animation bleiben in ZF-300 und werden nicht empfohlen. |
| Manuelle Prüfungen 3.28, 3.29 und 3.30 | Offen; vor einer Freigabe abarbeiten, zuerst die [Prüfliste 3.30](Checklisten/Manuelle_Pruefung_3.30.0.md). |

## 3. Etappe A – Schneller Zugriff und Zeichenkomfort

### MO-020 – Anklickbarer Pfad über dem Seitentitel

**Priorität:** P1 · **Aufwand:** S · **Daten:** D0 · **Entscheidung:** –
**Vorbild:** Notion-Brotkrumen. Glide zeigt Pfade bisher nur in Karten und
Auswahllisten; der Kopf zeigt allein den Titel.

**Ziel:** Jederzeit sehen und mit einem Klick erreichen, wo eine Seite liegt.

**Umfang**

- Über dem Titel von Listen, Notizen, Zeichnungen, Ordnern und Tagebüchern
  steht „Ordner › Unterordner“ in Nebentextfarbe; jedes Glied öffnet seinen
  Ordner.
- Reicht der Platz nicht, werden mittlere Glieder zu „…“; ein Klick darauf
  öffnet die ausgelassenen Glieder als eingebettete Auswahl.
- Systemansichten (Startseite, Mein Tag, Papierkorb …) zeigen keinen Pfad.
- Glieder sind per Tab erreichbar und mit Enter auslösbar.

**Abnahmekriterien**

1. Nach Verschieben oder Umbenennen eines Ordners stimmt der Pfad sofort.
2. Die bestehende Titelkürzung (`update_header_title`) bleibt wirksam; der
   Titel bricht nicht um.
3. Bei 860 px Fensterbreite überlappt nichts; die Kopfzeile wächst höchstens
   um eine Zeile.
4. Kein Pfadklick verändert Daten.

**Einstieg:** `update_header_title`, `get_display_title`, `folder_path_titles`.

### MO-040 – Rückgängig direkt in der Rückmeldung

**Priorität:** P1 · **Aufwand:** S · **Daten:** D0 · **Entscheidung:** –
**Vorbild:** verbreitetes „Rückgängig“ im Hinweis nach Löschen oder
Verschieben (Notion, Mail-Programme). Glide meldet jede Aktion seit 3.25, bietet
dort aber keinen Rückweg.

**Umfang**

- Rückmeldungen für Löschen, In-den-Papierkorb, Verschieben, Erledigen,
  Gruppieren und Von-Pinnwand-Entfernen tragen die Schaltfläche „Rückgängig“.
- Sichtbar etwa sechs Sekunden, beim Überfahren gehalten; Strg/Cmd+Z bleibt
  gleichwertig.
- Der Hinweis erscheint unabhängig von „Bewegte Rückmeldung“, weil er eine
  Bedienfunktion ist; ohne Animation erscheint er statisch.

**Abnahmekriterien**

1. Ein Klick nimmt genau die gemeldete Aktion zurück (Snapshot-Kennung).
2. Ist inzwischen eine weitere Änderung erfolgt, verschwindet die
   Schaltfläche, statt eine andere Aktion zurückzunehmen.
3. Die Schaltfläche ist per Tastatur erreichbar und für Screenreader
   beschriftet.
4. Zeichnungsstriche sind nicht betroffen; dort gilt das Editor-Undo.

**Einstieg:** `feedback()`, `ACTION_FEEDBACK_TEXTS`, `undo_last_change`,
`snapshot_undo`.

### MO-010 – Seiten- und Befehlssuche mit Tastenkürzel

**Priorität:** P1 · **Aufwand:** M · **Daten:** D1 · **Entscheidung:** E-03
**Vorbild:** Notion-Suche; Glides eigene Aktionssuche seit 3.22.

**Ziel:** Jede Seite und jede Aktion aus einem Feld erreichen.

**Umfang**

- Eine eingebettete Überlagerung im Hauptfenster (Technik wie
  `DropdownPopup`, kein Zusatzfenster) mit Suchfeld und zwei Ergebnisgruppen:
  **Seiten** und **Aktionen**.
- Seiten umfassen Listen, Notizen, Zeichnungen, Ordner, Tagebücher,
  gespeicherte Filter und Systemansichten; jeder Treffer zeigt Symbol und
  Pfad.
- Suche nach Teilwort, ohne Unterschied von Groß- und Kleinschreibung, Umlaute
  gleichwertig zu ae/oe/ue.
- Ohne Eingabe erscheinen die zuletzt geöffneten Seiten (ST-050, sonst die
  zuletzt bearbeiteten).
- Pfeiltasten, Enter und Escape; Kürzel nach E-03 (Vorschlag Strg/Cmd+O).
  Die bisherigen Wege („Aktionen“, Menü) öffnen dieselbe Überlagerung.

**Abnahmekriterien**

1. Jede Seite ist mit Kürzel, höchstens drei Zeichen und Enter erreichbar,
   sofern der Name eindeutig beginnt.
2. Die Aktionsliste ist identisch mit `ACTION_GROUPS`; „Weitere Aktionen“
   bleibt leer.
3. Seiten im Papierkorb erscheinen nicht.
4. Handbuch und Tastenkürzelübersicht nennen das Kürzel; kein bestehendes
   Kürzel ändert seine Bedeutung.
5. Bei 5.000 Punkten und 300 Seiten reagiert die Suche ohne spürbare
   Verzögerung; Grenzwert in `leistungspruefung.py` festlegen.

**Einstieg:** `show_actions_dialog`, `ACTION_GROUPS`, `MANUAL_SECTIONS`,
Tastenbindungen, `list_path_title`.

### ZD-010 – Kontextleiste für den Zeichen-Editor

**Priorität:** P1 · **Aufwand:** M · **Daten:** D0 · **Entscheidung:** –
**Vorbild:** Affinity-Kontextleiste: nur Optionen des aktiven Werkzeugs.
Glide zeigt heute zwei Zeilen Textschaltflächen, alle immer sichtbar.

**Umfang**

- **Zeile 1:** Werkzeuge (Pinsel, Füllen, Pipette, später Formen) als
  kompakte Schaltflächen aus ICONS-Glyphe und Kurzname mit deutlichem
  Aktivzustand. Daneben die Farbfelder (ZD-020); rechts Rückgängig und
  Wiederholen.
- **Zeile 2 (Kontext):**
  - Pinsel: Größen 1/2/4/8, später Symmetrie (ZD-050) und pixel-perfekt
    (ZD-130);
  - Füllen: Hinweis „füllt waagerecht und senkrecht verbundene Zellen“;
  - Pipette: Quelle Zeichnung oder Referenz.
- **Ansichtsgruppe rechts:** Zoomanzeige mit Stufenwahl, Raster, Referenz,
  Vorschau (ZD-040), „Mehr“.
- Tooltips nennen jedes Tastenkürzel. Bei schmalem Fenster bricht die Leiste
  über `ButtonFlow` um.

**Abnahmekriterien**

1. Alle bisherigen Funktionen und Tastenkürzel bleiben erreichbar und
   unverändert.
2. Bei 860 × 700 wird nichts abgeschnitten; die Fläche verliert höchstens die
   Höhe einer Zeile gegenüber 3.29.
3. Neue Glyphen stehen in `ICONS` und bestehen die Symbolprüfung und die
   Schriftabdeckung.
4. Die Geometrietests aus `test_features329.py` sind angepasst und grün.

**Einstieg:** `DrawingEditor._build`, `TOOLS`, `ButtonFlow`.

### ZD-020 – Zwei Farben, Rechtsklick und Farbleiste

**Priorität:** P1 · **Aufwand:** M · **Daten:** D1 (Ansichtszustand) ·
**Entscheidung:** – · **Abhängig von:** ZD-010
**Vorbild:**

- Aseprite: Linksklick malt mit der Vordergrund-, Rechtsklick mit der
  Hintergrundfarbe.
- Affinity: X tauscht, D setzt zurück, zehn zuletzt verwendete Farben.

**Ziel:** Farbe wechseln und Weiß auftragen, ohne Dialog. Weiß als zweite
Farbe ersetzt den bewusst nicht vorhandenen Radierer.

**Umfang**

- **Zwei Farben:** Vordergrund- und Hintergrundfarbe, Vorgabe Schwarz und
  Weiß.
  - Linksklick malt mit der Vordergrundfarbe, Rechtsklick mit der
    Hintergrundfarbe.
  - X tauscht die beiden, D setzt Schwarz/Weiß.
  - Tastatur: Leertaste malt Vordergrund, Umschalt+Leertaste Hintergrund.
- **Farbleiste:**
  - „In dieser Zeichnung“ zeigt alle verwendeten Palettenfarben,
    scrollbar, höchstens 256.
  - „Zuletzt“ zeigt zehn Farben, programmweit.
  - Klick setzt die Vordergrund-, Rechtsklick die Hintergrundfarbe.
- **Pipette:** Links übernimmt in die Vordergrund-, rechts in die
  Hintergrundfarbe.
- **Status:** Die Statuszeile nennt beide Farben.

**Abnahmekriterien**

1. Rechtsklick ist plattformgerecht gebunden (macOS `<Button-2>`, sonst
   `<Button-3>`) und öffnet kein Kontextmenü auf der Fläche.
2. Eine neue Farbe jenseits von 256 wird mit verständlicher Meldung
   abgelehnt; die Zeichnung bleibt unverändert.
3. Zuletzt verwendete Farben und Hintergrundfarbe überstehen einen Neustart
   (Ansichtszustand); die gespeicherte Zeichnung enthält sie nicht.
4. X und D kollidieren mit keinem bestehenden Kürzel der Fläche.

**Einstieg:** `DrawingEditor` (Bindungen, `choose_color`, `set_tool`),
`drawing_view_state`, `drawing_color_dialog`.

### ZD-030 – Zoom mit Mausrad und Verschieben

**Priorität:** P1 · **Aufwand:** S · **Daten:** D0 · **Entscheidung:** –
**Vorbild:** Grafikprogramme allgemein (Affinity, Aseprite). Glide zoomt heute
über Schaltflächen, Tasten und automatisches Einpassen; im Editor ist kein
Mausrad gebunden.

**Umfang**

- Strg/Cmd+Mausrad zoomt um die Zeigerposition; die Stufen `ZOOM_LEVELS`
  werden um 16, 20 und 24 erweitert.
- Mausrad und Umschalt+Mausrad scrollen nur, wenn die Fläche größer als die
  Anzeige ist (Regel aus der 3.29-Nachbesserung bleibt).
- Ziehen mit der mittleren Maustaste verschiebt bei scrollbarer Fläche.
- Die Zoomanzeige nennt den Faktor („8×“); die Taste 0 passt weiter ein.

**Abnahmekriterien**

1. Die Zelle unter dem Zeiger bleibt beim Zoomen auf ±1 Zelle an ihrer
   Bildschirmstelle.
2. Passt die Fläche, lässt sie sich weder scrollen noch verschieben.
3. Mausrad unter Windows, macOS und Linux (`<Button-4/5>`) über eine
   gemeinsame Hilfsfunktion; Tests für alle drei Ereignisarten.
4. Manueller Zoom beendet das automatische Einpassen wie bisher.

**Einstieg:** `change_zoom`, `fit_zoom`, `_center_surface`, `_visible_size`.

### ZD-040 – Eingebettete Vorschau in Originalgröße

**Priorität:** P1 · **Aufwand:** S · **Daten:** D0 · **Entscheidung:** –
**Vorbild:** Aseprite-Vorschaufenster (F7), Affinity-Pixelansicht. Glide
bettet die Vorschau ein, statt ein Fenster zu öffnen.

**Umfang**

- Schalter „Vorschau“ (Taste P) blendet ein kleines Feld neben
  beziehungsweise bei schmalem Fenster unter der Fläche ein.
- Das Feld zeigt die Zeichnung in 1× und 2× auf Weiß, ohne Raster.
- Aktualisierung gebündelt mit dem Neuzeichnen der geänderten Zellen.

**Abnahmekriterien**

1. Kein Zusatzfenster; der Schalterzustand ist Ansichtszustand.
2. Nach einem Strich zeigt die Vorschau den neuen Stand spätestens mit dem
   nächsten Bildaufbau.
3. Die Hauptfläche behält ihre Scroll- und Zoomregeln.

**Einstieg:** `drawing_image.model_to_photo`, Teilneuzeichnung im Editor.

### ZD-120 – PNG-Export in ganzzahligen Größen

**Priorität:** P1 · **Aufwand:** S · **Daten:** D0 · **Entscheidung:** E-13
**Vorbild:** Affinity-Export in 1×, 2× und 3×. Tk 8.6 schreibt PNG selbst;
keine neue Abhängigkeit.

**Umfang**

- „Mehr → Als PNG exportieren …“ mit Maßstab 1×, 2×, 4×, 8× oder 16×
  (höchstens 2048 px).
- Nächster-Nachbar-Skalierung, weißer Hintergrund (V1 kennt keine
  Transparenz).
- Dateiname vorgeschlagen aus dem Titel; atomar geschrieben wie die übrigen
  Exporte.

**Abnahmekriterien**

1. Zurückgelesen über `PhotoImage` stimmt jede Zelle pixelgenau in jedem
   Maßstab.
2. Ein Schreibfehler lässt keine halbe Datei zurück und meldet sich
   verständlich.
3. SVG- und JSON-Export bleiben unverändert; PNG wird nicht importiert.

**Einstieg:** `drawing_export`, `write_text_atomic` (binäres Gegenstück),
`show_drawing_menu`.

### ST-030 – Kachel „Zeichnungen“ mit Miniaturen

**Priorität:** P1 · **Aufwand:** S–M · **Daten:** D1 · **Entscheidung:** –
**Vorbild:** Notion-Galerie und Titelbilder; Glides eigene
Pinnwand-Vorschau („Bild statt Zeile“).

**Umfang**

- Neue Kachel zeigt bis zu sechs zuletzt geänderte Zeichnungen als
  Miniaturen (ganzzahlig skaliert, Pixelrahmen), Titel darunter, Pfad als
  Tooltip; Klick öffnet die Zeichnung.
- Ohne Zeichnungen erscheint eine Einladung „Neue Zeichnung“.
- Gemeinsamer **Miniaturcache** nach Zeichnungsprüfsumme
  (`drawing_history_hash`). AO-010, PW-020 und ZF-100 nutzen ihn später
  mit.

**Abnahmekriterien**

1. Das Ändern einer Zeichnung erneuert nur deren Miniatur.
2. Zeichnungen im Papierkorb erscheinen nicht.
3. Weiße Zeichnungen sind in dunklen Designs durch Rahmen klar abgegrenzt.
4. Für bestehende Startseiten ist die Kachel zunächst aus (Regel seit 3.22).
5. Bei 40 Zeichnungen bleibt der Startseitenaufbau innerhalb des vorher
   festgelegten Grenzwerts.

**Einstieg:** `HOME_TILE_DEFINITIONS`, Startseitenaufbau, `model_to_photo`.

## 4. Etappe B – Startseite und Übersichten

### ST-010 – Startseite direkt anpassen

**Priorität:** P1 · **Aufwand:** M · **Daten:** D1 · **Entscheidung:** –
**Vorbild:** Notion-Dashboard mit Bearbeitungsmodus, Breiten am Rand ziehen und
Verschieben zwischen Zeilen. Notion Home selbst ist nicht umsortierbar; Glide
kann das bereits, aber nur im Dialog.

**Umfang**

- Schaltfläche „Anpassen“ im Begrüßungsbereich schaltet den
  Bearbeitungsmodus ein; „Fertig“ und Escape beenden ihn.
- Im Bearbeitungsmodus trägt jede Kachel eine Griffleiste mit Titel,
  „Ausblenden“ und Breite (1, 2 oder 3 Spalten, höchstens die aktuelle
  Spaltenzahl).
- Ziehen verschiebt, eine Einfügemarke zeigt das Ziel; Alt+Pfeiltasten
  verschieben die fokussierte Kachel.
- Eine Platzhalterkachel „Kachel hinzufügen …“ listet ausgeblendete Kacheln.
- Kachelinhalte sind im Bearbeitungsmodus nicht anklickbar.
- „Startseite einrichten“ bleibt als gleichwertiger Weg.

**Abnahmekriterien**

1. Reihenfolge, Sichtbarkeit und Breite (`home_tile_span`, additiv)
   überstehen Neustart und App-Backup; die Normalisierung entfernt unbekannte
   Schlüssel.
2. Eine bestehende Startseite sieht nach dem Update unverändert aus.
3. Ziehen baut nicht je Mausbewegung neu auf; im Dopamin-Design kein
   Aufblitzen.
4. Jede Ziehaktion hat einen Tastaturweg; der Fokus bleibt sichtbar.
5. Bei einer Spalte (unter 980 px) wird die Breite ignoriert, aber
   gespeichert.

**Einstieg:** `HOME_TILE_DEFINITIONS`, Normalisierung der
Startseiteneinstellungen, Dialog „Startseite einrichten“.

### ST-020 – Gespeicherten Filter als Kachel anheften

**Priorität:** P1 · **Aufwand:** M · **Daten:** D1 · **Entscheidung:** –
**Vorbild:** Notion Home „Meine Aufgaben“ und angeheftete Datenbankansicht.

**Umfang**

- „Gespeicherten Filter anheften …“ im Bearbeitungsmodus und im
  Einrichten-Dialog; bis zu vier Filterkacheln.
- Die Kachel zeigt Name, Trefferzahl und die ersten fünf (kompakt drei)
  Treffer mit Abhaken und Öffnen; „Alle anzeigen“ führt in die Filteransicht.
- Wird ein Filter gelöscht, verschwindet seine Kachel mit Hinweis.

**Abnahmekriterien**

1. Die Treffer stammen aus derselben Funktion wie die Filteransicht, keine
   zweite Filterlogik.
2. Abhaken läuft über `item_change` und ist rückgängig machbar.
3. Umbenennen des Filters ändert den Kacheltitel.
4. `home_filter_tiles` ist additiv und übersteht Neustart und App-Backup.

**Einstieg:** `SavedFilters`, Ansicht `saved_filter`, Startseitenkacheln.

### ST-040 – Angeheftete Seiten

**Priorität:** P1 · **Aufwand:** M · **Daten:** D1 · **Entscheidung:** –
**Vorbild:** Notion-Favoriten. Glide nennt es **„Angeheftet“**, weil
„Favorit“ im Tagebuch bereits ein Eintragsmerkmal ist.

**Umfang**

- Kontextmenü „Anheften“/„Lösen“ für Liste, Notiz, Zeichnung, Ordner und
  Tagebuch.
- Abschnitt „Angeheftet“ oben in der Seitenleiste, einklappbar; Reihenfolge
  per Ziehen; höchstens 20 Einträge.
- Startseitenkachel „Angeheftet“ (für bestehende Startseiten zunächst aus).
- Seiten im Papierkorb sind ausgeblendet und kehren beim Wiederherstellen
  zurück.

**Abnahmekriterien**

1. Anheften verändert keine Liste und keinen Ordner und erzeugt keinen
   Verlaufseintrag.
2. Ohne angeheftete Seiten erscheint kein leerer Abschnitt.
3. `pinned_pages` ist additiv; beim Hinzufügen fremder Daten werden die
   Anheftungen des Gebers nicht übernommen (wie bei der globalen Pinnwand).
4. Tastaturweg über Kontextmenütaste beziehungsweise Umschalt+F10.

**Einstieg:** `sidebar_listbox`, Kontextmenüs der Seitenleiste,
Startseitenkacheln.

### ST-050 – Zuletzt geöffnet neben zuletzt bearbeitet

**Priorität:** P2 · **Aufwand:** S · **Daten:** D1 · **Entscheidung:** –
**Vorbild:** Notion „Zuletzt besucht“ (20 Seiten).

**Umfang**

- Die Kachel „Zuletzt bearbeitet“ erhält den Umschalter
  „geöffnet | bearbeitet“.
- `recent_pages` hält höchstens 20 Kennungen, auch Notizen und Zeichnungen.
- „Verlauf leeren“ löscht die Liste; sie bleibt rein lokal.

**Abnahmekriterien**

1. Gelöschte Seiten fallen heraus.
2. MO-010 zeigt ohne Eingabe diese Liste.
3. Kein Eintrag im Änderungsverlauf.

### AO-010 – Übersichten als Galerie mit Vorschau

**Priorität:** P1 · **Aufwand:** M · **Daten:** D1 · **Entscheidung:** –
**Abhängig von:** ST-030 (Miniaturcache); Tagebuchteil von ZF-120
**Vorbild:** Notion-Galerie mit Titelbild, Kartengrößen S/M/L und „Bild
einpassen“.

**Umfang**

- Die Listen- und Ordnerübersicht und die Ordneransicht zeigen je Karte eine
  Vorschau:
  - Zeichnung: Miniatur;
  - Notiz: die ersten zwei Zeilen;
  - Aufgabenliste: offene Punkte, Fortschrittsbalken, nächste Fälligkeit.
- Kartengröße S/M/L (`library_card_size`).
- Im Tagebuch steht das Momentdatum groß; Filter nach Tag und Zeitraum kommen
  aus ZF-120.

**Abnahmekriterien**

1. Auswahl und Reihenfolge der Karten entsprechen 3.29.
2. Die Abstandsprüfung in `test_ui_followup36.py` bleibt grün.
3. Bei 200 Karten bleibt der Aufbau im festgelegten Grenzwert.
4. Karten sind per Tastatur erreichbar; der Fokus scrollt in Sicht (wie
   heute).

**Einstieg:** `refresh_library_page`, `library_entries`.

### AO-020 – Schnellaktionen und Abschnitte in der Seitenleiste

**Priorität:** P2 · **Aufwand:** M · **Daten:** D1 · **Entscheidung:** –
**Abhängig von:** ST-040
**Vorbild:** Notion: „+“ und „•••“ beim Überfahren, einklappbare Abschnitte.

**Umfang**

- Beim Überfahren einer Ordnerzeile erscheinen am rechten Rand „+“ und „…“
  als eingebettete Schaltflächen an der Zeilen-Bbox.
  - „+“ legt im Ordner Liste, Notiz, Zeichnung oder Unterordner an.
  - „…“ öffnet das Kontextmenü.
- Die Abschnitte Angeheftet, Ansichten und Ordner sind einklappbar
  (`sidebar_sections_closed`).

**Abnahmekriterien**

1. Kein Springen der Zeilen beim Ein- und Ausblenden der Schaltflächen.
2. Ziehen in der Seitenleiste funktioniert unverändert.
3. Jede Schnellaktion ist auch über das Kontextmenü per Tastatur erreichbar.

**Einstieg:** `sidebar_listbox`, `on_sidebar_drag_*`,
`show_sidebar_context_menu`.

## 5. Etappe C – Pinnwand als Board

### PW-010 – Spaltenboard nach Feld mit Ziehen

**Priorität:** P1 · **Aufwand:** L · **Daten:** D2 · **Entscheidung:**
E-07, E-16 · **Abhängig von:** AO-040 (gemeinsame Gruppierungslogik)
**Vorbild:**

- Planner: Gruppieren nach Bucket, Fortschritt, Fälligkeit, Labels und
  Priorität; Ziehen ändert die Fälligkeit.
- Notion-Board: Ziehen ändert die Eigenschaft; Spaltenfarbe, Anzahl, leere
  Gruppen ausblenden.
- Trello: Listen einklappen, Name und Anzahl bleiben sichtbar.

**Ziel:** Die größte Pinnwand-Lücke schließen: Umplanen durch Ziehen zwischen
Spalten. Das Spaltenboard bleibt eine Ansicht auf dieselben Punkte.

**Umfang**

- Dritte Anordnung **„Spalten“** neben „Frei anordnen“ und „Geordnete
  Karten“ für Listen-, Ordner- und globale Pinnwand.
- **Gruppieren nach:**

  | Feld | Spalten |
  |---|---|
  | Wichtigkeit | je Stufe |
  | Fälligkeit | Überfällig, Heute, Morgen, Diese Woche, Später, Ohne Termin |
  | Bearbeitungstag | wie Fälligkeit |
  | Label | je Label, dazu „Ohne Label“ |
  | Erledigt | Offen, Erledigt |
  | Liste | nur auf Ordner- und globaler Pinnwand |

- Ziehen in eine andere Spalte setzt das Feld über `item_change`, ein
  Rückgängig-Schritt.
- Nicht setzbare Spalten wie „Überfällig“ nehmen keine Karte an und sagen
  warum.
- **Feldregeln:**
  - Datum: Die Uhrzeit bleibt, nur das Datum wechselt.
  - Wiederholung: Die Serie bleibt; verschoben wird das aktuelle Vorkommen.
  - Label: Eine Karte mit mehreren Labels erscheint in jeder Labelspalte;
    Ziehen ersetzt das Quelllabel durch das Ziellabel.
- **Spaltenkopf:** Name, Anzahl, Einklappen, Farbe aus Label oder
  Wichtigkeit. „Leere Spalten ausblenden“ als Schalter.
- **Reihenfolge** innerhalb einer Spalte folgt der Listenreihenfolge; keine
  zweite Ordnung.
- **Tastatur:** Karte fokussieren, Alt+Links/Rechts verschiebt in die
  Nachbarspalte.
- Welche Punkte erscheinen, regelt E-16 (Empfehlung: alle Punkte des
  Bereichs, „Nur offene“ als Filter).

**Abnahmekriterien**

1. Ziehen ändert genau das Gruppierungsfeld; Liste, Tabelle und Kalender
   zeigen die Änderung sofort.
2. Datums-, Wiederholungs- und Labelregeln sind je Fall getestet.
3. Gruppierung, eingeklappte Spalten und „Leere ausblenden“ überstehen
   Neustart, Komplett- und App-Backup (`pinboards`); ältere Fassungen fallen
   auf „Frei anordnen“ zurück.
4. 500 Karten in sechs Spalten bleiben im festgelegten Grenzwert.
5. Jede Ziehaktion hat einen Tastaturweg.

**Einstieg:** Pinnwand-Normalisierung (`layout`), Anordnungsauswahl,
Kartenaufbau, Ziehen, `item_change`.

### AO-040 – Liste und Tabelle nach Feld gruppieren

**Priorität:** P2 · **Aufwand:** M · **Daten:** D1 · **Entscheidung:** –
**Vorbild:** Notion Gruppe und Untergruppe; Planner „Gruppieren nach“.

**Umfang**

- Ansichtsoption „Gruppieren nach“ für Liste und Tabelle, mit denselben
  Feldern und Regeln wie PW-010. Eine gemeinsame Funktion liefert Gruppen und
  setzt Felder.
- Abschnittsköpfe wie in den Übersichten seit 3.25 (aufklappbar); Ziehen
  zwischen Abschnitten setzt das Feld.
- Die Gruppierung ist Ansicht: Strukturelle Gruppen bleiben unberührt. Die
  Entscheidung
  [Gruppe, Ordner, Überschrift](../01_Repository/Glide/docs/decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md)
  wird um diese Abgrenzung ergänzt.

**Abnahmekriterien**

1. Ohne Gruppierung sieht jede Liste aus wie in 3.29.
2. Abschnittsköpfe zählen in keiner Statistik und werden nicht exportiert.
3. `group_by` je Liste ist additiv.

### PW-020 – Karteninhalt und Kartenfarbe wählbar

**Priorität:** P1 · **Aufwand:** M · **Daten:** D2 · **Entscheidung:** –
**Abhängig von:** ST-030
**Vorbild:**

- Planner „Auf Karte anzeigen“;
- Notion-Kartenvorschau;
- Trello-Cover in Farbe, halb oder voll, mit Mustern für Farbfehlsichtige.

**Umfang**

- Je Pinnwand „Auf Karten zeigen“: Beschreibung (160 Zeichen), Checkliste
  (bis fünf Schritte, abhakbar), erstes Bild oder Zeichnungsminiatur. Einzelne
  Karten können das übersteuern.
- Kartenfarbe als Streifen (heute), Kopf oder volle Fläche aus Punktfarbe
  oder erstem Label.
- In Kontrastdesigns zusätzlich Muster oder Zeichen je Farbe.

**Abnahmekriterien**

1. Vorschau ist Darstellung; Abhaken schreibt in die Checkliste des Punkts
   wie im Anzeigemodus „Checklisten“.
2. Kartenhöhe ist begrenzt; die Druckausgabe zeigt dieselbe Vorschau.
3. Einstellungen reisen im `pinboards`-Abschnitt und werden beim Import neu
   zugeordnet.

### ZF-100 – Zeichnung als Pinnwandkarte (bestehend)

Unverändert nach der
[Aufgabensammlung](Glide_Aufgabensammlung_Zeichenflaeche_2026-09-23.md#wie-erscheint-eine-zeichnung-auf-der-pinnwand-zf-100).
Ergänzung aus diesem Katalog: Die Vorschau nutzt den Miniaturcache aus
ST-030 und die Vorschauart „Zeichnungsminiatur“ aus PW-020.

### PW-030 – Benannte Bereiche auf der Pinnwand

**Priorität:** P1 · **Aufwand:** L · **Daten:** D2 · **Entscheidung:** –
**Vorbild:** FigJam-Abschnitte; Glides Stufenplan (Stufe 2) und ZF-200.

**Umfang**

- Rechteck mit Name und Farbe.
- Karten, deren Mittelpunkt im Bereich liegt, bewegen sich mit ihm; die
  Zugehörigkeit wird beim Loslassen neu bestimmt.
- Bereiche lassen sich verschieben, in der Größe ändern und löschen, ohne
  Karten zu löschen.
- Liste „Zu Bereich springen“; Bereiche erscheinen im Navigator und im Druck.
- Höchstens 50 Bereiche je Pinnwand; in den Anordnungen „Geordnet“ und
  „Spalten“ ausgeblendet.

**Abnahmekriterien**

1. Verschieben eines Bereichs verschiebt enthaltene Karten in einem
   Rückgängig-Schritt.
2. `areas` reisen im Backup; der additive Import vergibt neue Kennungen.
3. Bereiche sind per Tastatur auswählbar und benennbar.

### PW-040 – Auswahl aufräumen

**Priorität:** P2 · **Aufwand:** S · **Daten:** D0 · **Entscheidung:** –
**Vorbild:** FigJam „Aufräumen“.

**Umfang**

- „Aufräumen“ ordnet eine Mehrfachauswahl in ein Raster mit gleichen
  Abständen, Spaltenzahl etwa √n.
- Die Reihenfolge folgt der bisherigen Lage: Zeilen von oben, innerhalb von
  links.

**Abnahmekriterien**

1. Ein Rückgängig-Schritt.
2. Der Fang bleibt beachtet.
3. Nicht ausgewählte Karten bleiben unberührt.

### PW-050 – Schnell weiterdenken

**Priorität:** P2 · **Aufwand:** M · **Daten:** D2 · **Entscheidung:** E-08
**Vorbild:** FigJam: Strg/Cmd+Enter legt einen Zettel daneben an; Verbinder
entstehen durch Ziehen vom Objektrand.

**Umfang**

- Strg/Cmd+Enter auf einer ausgewählten Karte legt rechts daneben einen
  neuen Punkt an, in der Liste der Ausgangskarte beziehungsweise der Zielliste
  der Pinnwand.
- Der Titel wird direkt auf der Karte eingegeben: Enter bestätigt, Escape
  verwirft ohne Rest. Auf Wunsch wird die neue Karte automatisch verbunden.
- Ein Ziehpunkt am Kartenrand erzeugt eine Verbindung durch Ziehen auf die
  Zielkarte. Der Modus „Verbinden …“ bleibt.

**Abnahmekriterien**

1. Der neue Punkt ist ein normaler Punkt seiner Liste; ein
   Rückgängig-Schritt.
2. Escape hinterlässt keinen leeren Punkt.
3. Die Verbindungsart folgt der Vorgabe der Pinnwand.

### PW-060 – Verbindungen beschriften und gestalten

**Priorität:** P2 · **Aufwand:** M · **Daten:** D2 · **Entscheidung:** –
**Vorbild:** FigJam-Verbinder mit Text, Strichart und Farbe.

**Umfang**

- Beschriftung bis 40 Zeichen in der Linienmitte.
- Strichart durchgezogen oder gestrichelt; Farbe aus den Akzent-Tokens des
  Designs.
- Alles erscheint auch im Druck.

**Abnahmekriterien**

1. `label`, `style` und `color` sind additiv.
2. Eine ältere Fassung zeichnet die Verbindung weiter als einfache Linie.
3. Pfeile bleiben reine Darstellung; sie erzeugen keine
   Aufgabenabhängigkeit.

### PW-070 – Flächenhintergrund

**Priorität:** P2 · **Aufwand:** S · **Daten:** D2 · **Entscheidung:** –
**Vorbild:** OneNote-Linien und -Karo, Punktraster in Whiteboards.

**Umfang**

- Hintergrund leer, Punkte, Linien oder Karo; der Abstand entspricht dem
  Fangraster.
- Die Farbe folgt dem Design.
- Im Druck optional.

**Abnahmekriterien**

1. Kein spürbarer Leistungsverlust bei 200 % Zoom.
2. Kontrast zur Karte bleibt erhalten.

## 6. Etappe D – Pixel-Werkstatt

### ZD-070 – Rückgängig je Aktion

**Priorität:** P1 · **Aufwand:** M · **Daten:** D0 · **Entscheidung:** E-11
**Vorbild:** Affinity-Verlauf, Aseprite. Glide nimmt heute 20 einzelne
Zelländerungen zurück. Ein 8-×-8-Tupfer ändert bis zu 64 Zellen und ist damit
nicht vollständig rücknehmbar.

**Umfang**

- **Einheit:** Rückgängig nimmt einen Pinselzug, eine Füllung, eine Form oder
  eine Farbersetzung zurück, jeweils mit allen geänderten Zellen.
- **Speicher:** begrenzt, etwa 50 Aktionen oder eine feste Zahl von Zellen.
  Ist die Grenze erreicht, fallen die ältesten Aktionen weg.
- **Tooltip:** nennt die Aktion, etwa „Rückgängig: Pinselzug (37 Zellen)“.
- **Vorher-Stand:** Der markierte Vorher-Stand (`drawing_restore`) für
  Nachzeichnen, Import und Leeren bleibt unverändert.

**Abnahmekriterien**

1. Eine Füllung der ganzen Fläche ist in einem Schritt rücknehmbar.
2. Eine neue Aktion leert Wiederholen.
3. Autosave und Verlaufseintrag „Zeichnung geändert“ verhalten sich wie in
   3.29.
4. Der Vertrag 65 und die Tests in `test_drawing.py` werden bewusst
   fortgeschrieben; die Entscheidung vom 24.09.2026 ist als abgelöst
   dokumentiert.

**Einstieg:** Undo-Ring in `drawing.py`, `DrawingEditor.undo/redo`,
`_history_step`.

### ZD-050 – Symmetrisch zeichnen

**Priorität:** P1 · **Aufwand:** M · **Daten:** D1 (Ansichtszustand) ·
**Entscheidung:** – · **Abhängig von:** ZD-070
**Vorbild:** Aseprite und Pixelorama: horizontal, vertikal oder beides.

**Umfang**

- Schalter „Symmetrie: aus | ↔ | ↕ | beide“ in der Kontextleiste.
- Die Achse liegt auf der Zellgrenze in der Flächenmitte. Weil die
  Ein-Drittel-Trefferregel achsensymmetrisch ist, entsteht durch Spiegeln
  der Zeigerposition genau das gespiegelte Zellbild.
- Die Achse wird gestrichelt angezeigt; die Vorschau zeigt auch die
  gespiegelten Treffer.
- Wirkt auf Pinsel und später auf Formen (ZD-060).

**Abnahmekriterien**

1. Für alle vier Pinselgrößen ist das Ergebnis exakt spiegelgleich.
2. Gespiegelte Zellen gehören zur selben Rückgängig-Aktion.
3. Tastaturmalen spiegelt ebenfalls.

### ZD-060 – Linie, Rechteck und Ellipse

**Priorität:** P2 · **Aufwand:** M · **Daten:** D0 · **Entscheidung:** E-10
**Abhängig von:** ZD-070, ZD-010
**Vorbild:** Formwerkzeuge in Aseprite und Affinity.

**Umfang**

- **Werkzeuge:** Linie in Pinselgröße; Rechteck und Ellipse jeweils als
  Umriss oder gefüllt.
- **Maus:** Aufziehen mit Vorschau. Umschalt beschränkt auf 45°, Quadrat
  oder Kreis, Alt zieht vom Mittelpunkt, Escape bricht ab.
- **Tastatur:** Leertaste setzt den Anfang, Pfeiltasten führen, Enter
  bestätigt.

**Abnahmekriterien**

1. Linien sind lückenlos und deterministisch (Bresenham-Verfahren).
2. Jede Form ist eine Rückgängig-Aktion.
3. Die Symmetrie wirkt auf Formen.

### ZD-100 – Farbe in der ganzen Zeichnung ersetzen

**Priorität:** P2 · **Aufwand:** S · **Daten:** D0 · **Entscheidung:** –
**Abhängig von:** ZD-020, ZD-070
**Vorbild:** indizierte Paletten in Aseprite, globale Farben in Affinity.

**Umfang**

- Rechtsklick auf ein Farbfeld der Leiste → „Farbe in Zeichnung ersetzen …“.
- Eine Vorschau nennt die Zahl der Zellen.

**Abnahmekriterien**

1. Die Ersetzung ist ein Rückgängig-Schritt.
2. Die Palette bleibt bei höchstens 256 Farben.
3. Es entsteht genau ein Verlaufseintrag.

### ZD-110 – Kachelmodus für Muster

**Priorität:** P2 · **Aufwand:** M · **Daten:** D1 · **Entscheidung:** –
**Abhängig von:** ZD-040
**Vorbild:** Aseprite- und Pixelorama-Kachelmodus.

**Umfang**

- Schalter „Kachelvorschau“: Das Vorschaufeld zeigt die Zeichnung 3 × 3
  wiederholt.
- Optional „Über den Rand malen“: Pinseltreffer jenseits des Rands erscheinen
  auf der Gegenseite.

**Abnahmekriterien**

1. Die Vorschau ist reine Ansicht.
2. Das Umlaufmalen ist abschaltbar und getestet an allen vier Rändern und
   Ecken.

### ZD-130 – Pixel-perfekte Linie

**Priorität:** P2 · **Aufwand:** S–M · **Daten:** D1 · **Entscheidung:** –
**Abhängig von:** ZD-070
**Vorbild:** Aseprite und Pixelorama.

**Umfang**

- Option für den 1-×-1-Pinsel: Eine Zelle, die innerhalb desselben Zugs mit
  Vorgänger und Nachfolger eine L-Ecke bildet, erhält ihre vorherige Farbe
  zurück.

**Abnahmekriterien**

1. Deterministische Tests für Diagonalen und Kurven.
2. Das Zusammenspiel mit der Ein-Drittel-Regel ist im Vertrag beschrieben.
3. Rückgängig stellt den Zug vollständig her.

### ZD-150 – Graustufenansicht und Referenzdeckkraft

**Priorität:** P2 · **Aufwand:** S · **Daten:** D1 · **Entscheidung:** –
**Vorbild:** Affinity-Graustufenansicht zur Tonwertprüfung, Deckkraft von
Hilfsebenen.

**Umfang**

- Ansichtsschalter „Graustufen“ zeigt die Zeichnung nach Luminanz.
- Die Referenz erhält einen Deckkraftregler von 10 bis 90 %, vorberechnet als
  Mischung mit Weiß.

**Abnahmekriterien**

1. Beides verändert weder Zeichnung noch Export.
2. Die Pipette liest weiter die echte Farbe.

### ZD-090 – Palettenbibliothek mit Import und Export

**Priorität:** P2 · **Aufwand:** M · **Daten:** D1 · **Entscheidung:** E-15
**Abhängig von:** ZD-020, ZF-210
**Vorbild:** Affinity-Programm- und Dokumentpaletten; Lospec-Paletten als
`.hex` und `.gpl`.

**Umfang**

- **Paletten:** Programmpaletten (Glide-Standard, nach ZF-210 die
  Glide-Inhaltspalette), eigene Paletten, „Palette aus Zeichnung
  übernehmen“.
- **Austausch:** Import und Export als GIMP-Palette (`.gpl`) und Hex-Liste
  (`.hex`), beides Textformate der Standardbibliothek.
- **Anzeige:** Die Farbleiste aus ZD-020 zeigt die gewählte Palette.
- **Grundsatz:** Zeichnungen behalten ihre konkreten Farben; eine Palette
  färbt nie um.

**Abnahmekriterien**

1. Der Import validiert `#RRGGBB`, höchstens 256 Einträge und Namen; eine
   fehlerhafte Datei ändert nichts.
2. Export und erneuter Import ergeben dieselbe Palette.
3. Mitgelieferte Paletten haben eine geprüfte Lizenz.

## 7. Etappe E – Formatpaket 20

Alle Pakete dieser Etappe teilen die Migration nach Abschnitt 3 der
Arbeitsvorbereitung: Vorsicherung, Ablehnung in älteren Fassungen, Rundlauf
durch alle Transportwege.

### ZD-140 – Flächengrößen 16, 32, 64 und 128

**Priorität:** P1* · **Aufwand:** L · **Daten:** D3 · **Entscheidung:**
E-14, E-02
**Vorbild:** freie Leinwandgrößen in allen Pixel-Werkzeugen. Kleine Flächen
sind der Normalfall für Symbole und Sprites.

**Umfang**

- **Anlage:** Die Anlage fragt die Größe 16, 32, 64 oder 128 (Vorgabe 128).
  Die Größe ist danach fest; „Größe ändern“ bleibt P3.
- **Format:** `glide.drawing` Version 2 mit `width` und `height` aus
  {16, 32, 64, 128}. Version-1-Zeichnungen bleiben unverändert gültig.
- **SVG:** Glide-SVG mit `viewBox="0 0 w h"`; Import akzeptiert Version 1 und
  2.
- **Nachzeichner und Miniaturen:** arbeiten auf die Zielgröße; Zoom und
  Einpassen richten sich nach der Größe.

**Abnahmekriterien**

1. Jede Größe übersteht JSON- und SVG-Rundlauf, Backup und Import.
2. Die Validierung prüft Zeilenzahl = Höhe und Zeilenlänge = 2 × Breite.
3. Glide 3.30 öffnet einen Bestand aus einer neueren Version nur schreibgeschützt.
   *(Berichtigt am 26.09.2026: Die ursprüngliche Annahme „eine ältere Fassung lehnt Format 20
   sichtbar ab“ ist widerlegt – Glide 3.29 überschreibt einen Format-20-Bestand bei der ersten
   Eingabe. Siehe Vertrag 3.30, Abschnitt 9.)*

### AO-050 – Pixelsymbol für Listen, Ordner und Seiten

**Priorität:** P1* · **Aufwand:** L · **Daten:** D3 · **Entscheidung:**
E-09, E-02 · **Abhängig von:** ZD-140
**Vorbild:** Notion-Seitensymbole. In Glide wird daraus ein Brückenstück
zwischen Organisation und Pixel-Nische.

**Umfang**

- **Anlegen:** Jede Liste, Notiz, Zeichnung, jeder Ordner und jedes Tagebuch
  kann ein 16-×-16-Pixelsymbol tragen.
  - Anlage im eingebetteten Editor mit Fläche 16.
  - Oder „Aus Zeichnung übernehmen“: verkleinert per Mehrheitsfarbe je Block.
- **Anzeige:** Seitenleiste (`ttk.Treeview`-Bild), Reiter, Übersichtskarten,
  Pfadzeile und Seitensuche. Ohne Symbol erscheint das ICONS-Zeichen.
- **Symbolregel:** Pixelsymbole sind Nutzerinhalt. Die Symbolprüfung erhält
  eine dokumentierte Ausnahme.

**Abnahmekriterien**

1. Das Symbol reist durch Duplizieren, Papierkorb, Vorlagen, alle Backups
   und das Austauschformat.
2. Bei 200 % Skalierung erscheint es ganzzahlig vergrößert und scharf.
3. Der Verlust der Bildreferenz lässt kein leeres Feld in der Seitenleiste
   zurück.

### ZD-080 – Benannte Zwischenstände

**Priorität:** P2 · **Aufwand:** M–L · **Daten:** nach E-12 (Empfehlung:
Anhänge) · **Entscheidung:** E-12
**Vorbild:** Affinity-Schnappschüsse, mit dem Dokument gespeichert.

**Umfang**

- „Mehr → Zwischenstand merken …“ mit Name; Vorgabe Datum und Uhrzeit.
- Liste mit Miniatur, Name und Datum. Aktionen: „Wiederherstellen“ (mit
  Vorher-Stand und Rückgängig), „Als neue Zeichnung“, „Löschen“.
- Höchstens zehn Zwischenstände je Zeichnung.

**Abnahmekriterien**

1. Zwischenstände reisen mit Komplett- und passendem Teilbackup.
2. Autosave wird nicht langsamer (deshalb die Empfehlung Anhänge).
3. Wiederherstellen ist rücknehmbar.

### MO-070 – Archivieren statt Löschen

**Priorität:** P3 · **Aufwand:** M–L · **Daten:** D3 · **Entscheidung:**
E-06, E-02
**Vorbild:** Notion-Seitenarchivierung (3.4).

**Umfang**

- Listen und Ordner lassen sich archivieren. Archivierte Seiten sind aus
  Seitenleiste, Startseite und Standardsuche ausgeblendet.
- Eine Ansicht „Archiv“ zeigt sie; „Zurückholen“ stellt sie wieder her.
- Anders als der Papierkorb gibt es keine Obergrenze und kein Entfernen.

**Abnahmekriterien**

1. Archivierte Punkte zählen in keiner Tagesplanung.
2. Das Archiv reist mit allen Backups.

## 8. Später – Ergänzungen und Forschung

### MO-030 – Eingebetteter Detailbereich neben der Liste

**Priorität:** P2 · **Aufwand:** XL · **Daten:** D1 · **Entscheidung:** E-04
**Vorbild:** Notion-Seitenblick. Er passt zur Vorgabe „eingebettet statt
Zusatzfenster“.

**Umfang**

- Enter oder Doppelklick öffnet die Details rechts im Inhaltsbereich; die
  Liste bleibt bedienbar.
- Wechselt die Auswahl, wechselt der Inhalt.
- Unter 980 px bleibt die Punktmaske; die Breite des Bereichs ist ziehbar und
  wird gemerkt.

**Abnahmekriterien**

1. Jede Änderung läuft über `item_change` und ist rückgängig machbar.
2. Beim Auswahlwechsel geht keine Eingabe verloren.
3. Die Punktmaske bleibt vollständig erhalten.

### MO-050 – Leerzustände mit nächstem Schritt

**Priorität:** P2 · **Aufwand:** M · **Daten:** D0 · **Voraussetzung:**
Entscheidung zur Stufe 3 im
[Arbeitsbegleiter](../01_Repository/Glide/docs/decisions/ARBEITSBEGLEITER.md)

**Umfang:** Leere Liste, leerer Ordner, leere Pinnwand, leere Suche, leerer
Papierkorb und leeres Tagebuch zeigen je einen Satz und eine Hauptaktion; Gismo
nur nach der Entscheidung.

### MO-060 – Visuelle Richtung „Pixel“

**Priorität:** P2 · **Aufwand:** M · **Daten:** D1 · **Entscheidung:** E-05
**Abhängig von:** ZF-210
**Vorbild:** das Inspirationsbild im Projektordner: kräftige, abgerundete
Blockformen in Blau, Gelb und Pink auf Schwarz.

**Umfang**

- Eigenes Design „Pixel“:
  - Farbflächen-Kachelköpfe;
  - blockige Akzentbalken;
  - Pixelrahmen um Miniaturen.
- Semantische Tokens bleiben; Kontrast wird gemessen wie bei „Minimal“.
- Keine Texturen; eine Pixelschrift nur nach Lizenzprüfung als mitgelieferte
  Ressource.

### AO-030 – Tabelle mit verschachtelten Unterpunkten

**Priorität:** P2 · **Aufwand:** M · **Daten:** D1
**Vorbild:** Notion-Unterpunkte „verschachtelt“ oder „flach“.

**Umfang**

- Tabellenschalter „Unterpunkte: verschachtelt | flach“; verschachtelt mit
  Aufklapppfeilen und Einrückung.
- Sortierung wirkt je Ebene; Eltern von Filtertreffern erscheinen
  abgeschwächt.

### AO-060 – Kompakte Eigenschaften im Seitenkopf

**Priorität:** P3 · **Aufwand:** S · **Daten:** D0

**Umfang:** Unter Titel und Pfad eine Chipzeile, zum Beispiel „12 offen ·
nächste Fälligkeit morgen · 3 Labels“. Vorbild sind die angehefteten
Eigenschaften in Notion-Layouts.

### AO-070 – Tagesplan mit Zeitblöcken (Forschung)

**Priorität:** P3 · **Vorbild:** Trello-Planer mit Zeitblöcken.

**Offene Frage:** Braucht der Bearbeitungstag eine Uhrzeit, und wie verhält
sie sich zur Kapazität? Dafür ist ein eigener Vertrag nötig.

**Umgesetzt 3.30.0:** `planned_time` (Format 20), Zeitplan in „Mein Tag“ mit
Überschneidungshinweis; im Ausbau Ziehen und Alt+↑/↓. Die Kapazität bleibt
minutenbasiert.

### MO-080 – Präsentationsmodus (Forschung)

**Priorität:** P3 · **Abhängig von:** PW-030
**Vorbild:** Notion-Präsentationsmodus (3.4), Pinnwand-Stufe 3.

**Idee:** Überschriften einer Notiz beziehungsweise Bereiche einer Pinnwand
werden zu Folien, im Vollbild der Seitenanzeige.

**Umgesetzt 3.30.0:** beide Folienquellen im Vollbild; im Ausbau zusätzlich als
Druckseite, aus der der Browser ein PDF erzeugt.

### ZD-160 – Auswahl, Verschieben und Kopieren (Forschung)

**Priorität:** P3 · **Abhängig von:** ZD-070

**Umfang:** Rechteckauswahl, Verschieben, Kopieren und Einfügen innerhalb
einer Zeichnung und zwischen Zeichnungen. Aus ZF-300.

### ZD-170 – Dithering und Musterfüllung (Forschung)

**Priorität:** P3 · **Abhängig von:** ZD-090

**Umfang:** Schachbrett- und Bayer-Muster als Füllart mit zwei Farben. Aus
ZF-300.

## 9. Bewusst nicht im Katalog

Echtzeitmitarbeit, KI-Funktionen, Bildarchive aus dem Netz, freie
Klebezettel ohne Punkt, Freihand-Tinte auf der Pinnwand, Datenbank-Baukasten,
Vektorpfade, Verläufe, Ebeneneffekte, Animation sowie frei belegbare
Arbeitsbereiche und Kürzel. Begründung:
[Wettbewerbsrecherche, Abschnitt 7](Glide_Wettbewerbsrecherche_Modernisierung_2026-09-25.md#7-was-glide-bewusst-nicht-übernimmt).
