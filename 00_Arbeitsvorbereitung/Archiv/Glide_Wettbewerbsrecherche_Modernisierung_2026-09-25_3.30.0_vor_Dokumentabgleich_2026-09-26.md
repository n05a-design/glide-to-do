# Glide – Wettbewerbsrecherche: Startseite, Pinnwand, Ordner und Pixel-Design

Stand 25.09.2026 · Recherchestand · Glide 3.29.0 · Aufgabenformat 19

> **Status dieses Dokuments:** Recherche und Bewertung, keine Programmänderung.
> Die daraus abgeleitete Planung steht in der
> [Arbeitsvorbereitung](Glide_Arbeitsvorbereitung_Modernisierung_2026-09-25.md),
> die abarbeitbaren Pakete stehen im
> [Aufgabenkatalog](Glide_Aufgabenkatalog_Modernisierung_2026-09-25.md).
> Der [Funktionsvergleich vom 23.09.2026](Glide_Funktionsvergleich_und_Zeichenflaeche_2026-09-23.md)
> bleibt für das Zeichenflächenkonzept maßgeblich; dieses Dokument schreibt den
> Vergleich für Startseite, Pinnwand, Ordner und Zeichenablauf fort.

## 1. Auftrag und Vorgehen

Auftrag vom 25.09.2026: Glides Funktionsumfang online mit der Konkurrenz
vergleichen und daraus Recherche, Arbeitsvorbereitung und einen abarbeitbaren
Aufgabenkatalog erstellen. Vier Bereiche mit vorgegebenen Referenzen:

| Bereich | Referenz |
|---|---|
| Darstellung, besonders Startseite, und allgemeine Modernisierung | Notion |
| Pinnwand | Trello, OneNote, Figma/FigJam, Microsoft Planner |
| Aufgabenmanagement, Ordnerstruktur und Darstellung | Notion |
| Zeichnen und künstlerische Entfaltung | Affinity (früher Affinity Designer) |

Für das Zeichnen gilt eine Sonderregel: Glide will die **Pixel-Design-Nische**
besetzen. Affinity dient deshalb als Vorbild für Arbeitsablauf und Oberfläche,
nicht für den Funktionsumfang. Ergänzend wurden Aseprite, Pixelorama und das
Palettenverzeichnis Lospec als Referenzen genau dieser Nische herangezogen.

**Quellen.** Bevorzugt wurden Hilfeseiten und Versionshinweise der Hersteller,
abgerufen am 25.09.2026. Drittquellen erscheinen nur, wo der Hersteller keine
Seite liefert, und sind gekennzeichnet. Preise werden nicht verglichen;
Tarifgrenzen stehen nur dort, wo sie die Bewertung verändern.

**Glide-Iststand.** Aus den Verträgen 48 bis 59 und 65 sowie einem gezielten
Codeabgleich in `app.pyw` 3.29.0 (Startseitenkacheln, Übersicht, Kopfzeile,
Seitenleiste, Pinnwandanordnung, Zeichen-Editor, Tastenbindungen).

**Bewertungsskala.**

| Bewertung | Bedeutung |
|---|---|
| **Übernehmen** | Klarer Nutzen, passt ohne Bruch zu Glides Grenzen. |
| **Anpassen** | Das Prinzip passt, die Glide-Form muss anders sein. |
| **Beobachten** | Später oder erst nach einer Vorbedingung sinnvoll. |
| **Nicht übernehmen** | Widerspricht lokalem Betrieb, Datenmodell oder Produktfokus. |

Leitfrage jeder Bewertung: Ist das Bedienprinzip übertragbar, ohne Konto,
Cloud, neue Laufzeitabhängigkeit oder Zusatzfenster einzuführen und ohne den
Unterschied zwischen Inhalt und Ansicht aufzuweichen?

## 2. Glide-Iststand 3.29.0 in Kürze

| Bereich | Vorhanden | Nicht vorhanden |
|---|---|---|
| **Startseite** | 16 Kacheln (Uhr, Begrüßung, Gismo, Heute, Nächste Aufgabe, sieben Tage, Labels, Zuletzt bearbeitet, Vorlagen, Impuls, Kalendervorschau, Verspätet, Fortschritt, Pinnwände, Pinnwand-Vorschau, Bestand); Raster mit 1–3 Spalten automatisch oder fest; „Startseite einrichten“ schaltet Kacheln ein/aus und ordnet sie; Kalendervorschau Monat/Woche/Nächste; Ausführlichkeit normal/kompakt; acht Startansichten; Begrüßungsbereich mit vier Flächen und „Weitere …“; neun Designs | Anordnen direkt auf der Startseite, Kachelbreite, angeheftete Seiten, Filterergebnis als Kachel, Bildvorschau von Zeichnungen |
| **Allgemeine Bedienung** | Menüs nach Zweck, Handbuch (F1), durchsuchbare App-Aktionen über die Schaltfläche „Aktionen“ und das Menü, Rückmeldung je Aktion, Seitenleiste als `ttk.Treeview` mit Ziehen, Punktmaske als Dialog | Seitensuche („Gehe zu …“), eigenes Kürzel für die Aktionssuche (Strg/Cmd+K öffnet den Kalender), anklickbarer Pfad im Kopf (der Kopf zeigt nur den Titel), Rückgängig direkt in der Rückmeldung |
| **Pinnwand** | Listen-, Ordner- und globale Pinnwand; freie oder geordnete Anordnung; drei Kartengrößen; Verbindungen als Linie oder Pfeil; Mehrfachauswahl, Lasso, Fang und Hilfslinien; Zoom 50–200 %; Navigator; Vollbild; Druck; 500 Karten/200 Verbindungen; Transport im Backup | Spalten nach Feld (Kanban) mit Ziehen, wählbarer Karteninhalt, Bereiche, beschriftete Verbindungen, Flächenhintergrund, Auswahl aufräumen, Zeichnung als Karte (ZF-100) |
| **Aufgaben und Ordner** | Ordner bis 5 Ebenen, Listen, Punkte mit Unterpunkten, Gruppen, Long-Tasks, Überschriften; Labels, Wichtigkeit, Fälligkeit mit Uhrzeit, Wiederholung, Erinnerung, Bearbeitungstag, Aufwand, Checkliste, Anhänge; Liste, flache Tabelle, Kalender, Labels, Pinnwand, Reiter; fünf Anzeigemodi; Mein Tag, In Bearbeitung, Verspätet; gespeicherte Filter; Listen- und Ordnerübersicht als Karten mit Pfad und Textvorschau; Tagebuchordner; Vorlagen, Papierkorb, Verlauf | Galerie mit Bildvorschau, Gruppieren einer Liste nach Feld, verschachtelte Tabelle, Seitensymbole, Schnellaktionen in der Seitenleiste |
| **Zeichnen** | 128 × 128 Zellen, eine Ebene, ≤ 256 Farben; Pinsel 1/2/4/8, Füllen (4er-Nachbarschaft), Pipette; Farbdialog mit Spektrum, Helligkeit und Hex; Zell-Undo/Redo (20); Zoom 2–12 mit automatischem Einpassen; Raster; PNG-Referenz und Nachzeichner (≤ 64 Farben); Tastaturcursor; Autosave; SVG/JSON-Rundlauf | zweite Farbe und Rechtsklick-Malen, Farbleiste im Editor, zuletzt verwendete Farben, Palettenbibliothek, Symmetrie, Formen, Vorschau in Originalgröße, Mausrad-Zoom, PNG-Export, andere Flächengrößen, benannte Zwischenstände |

## 3. Startseite und allgemeine Modernisierung – Notion

### 3.1 Befund

- **Notion Home** ist ein fester Startbereich aus Widgets: Begrüßung, zuletzt
  besuchte Seiten (bis 20), anstehende Termine, „Meine Aufgaben“ aus mehreren
  Aufgabendatenbanken, eine angeheftete Datenbankansicht, Vorschläge, Trends,
  Lernen und Vorlagen. Widgets lassen sich ein- und ausblenden; die Reihenfolge
  ist fest. Als Startseite wählbar sind Home, die zuletzt besuchte oder die
  oberste Seite der Seitenleiste. *(Drittquelle: Thomas Frank.)*
- **Dashboard-Ansicht** (Notion 3.4, 26.03.2026; nur Business/Enterprise): ein
  Container für bis zu 12 Widgets, höchstens 4 je Zeile. Breiten werden am
  Rand gezogen, Zeilenhöhen an der Zeilengrenze; Widgets lassen sich zwischen
  Zeilen verschieben. Globale Filter wirken auf mehrere Widgets zugleich. Es
  gibt einen Ansichts- und einen Bearbeitungsmodus sowie ein reines
  Zahlen-Widget.
- **Neue Seitenleiste** (3.4): vier Reiter (Home, KI-Chats, Meetings,
  Posteingang), ein- und ausschaltbare Abschnitte. Favoriten, Privat, Geteilt
  und Teamspaces; unbegrenzte Verschachtelung. Überfahren zeigt „+“ für eine
  Unterseite und „•••“ für das Menü. Einstellbar sind die Zahl der Seiten vor
  „Mehr“ und die Sortierung (manuell oder nach Bearbeitung).
- **Seitengestaltung:** jede Seite mit Symbol (Emoji oder eigenes Bild) und
  Titelbild; Schrift Standard/Serif/Mono, kleine Schrift, volle Breite.
  Neu in 3.4 sind ein Reiter-Block als Alternative zu verschachtelten
  Unterseiten, Seitenarchivierung und ein Präsentationsmodus (Beta).
- **Seitenblick:** Datenbankeinträge öffnen rechts neben der Ansicht, in der
  Mitte oder als Vollseite; Tabelle, Board, Liste und Zeitleiste öffnen
  standardmäßig rechts, die übrige Ansicht bleibt bedienbar.

### 3.2 Vergleich und Bewertung

| Dimension | Notion | Glide 3.29 | Bewertung | Katalog |
|---|---|---|---|---|
| Startbereich anordnen | Home fest; Dashboard per Ziehen mit Breiten | Reihenfolge und Sichtbarkeit nur im Dialog; Spaltenzahl global | **Anpassen:** Bearbeitungsmodus direkt auf der Startseite, Kachelbreite | ST-010 |
| Persönliche Ansicht als Widget | „Meine Aufgaben“, Datenbankansicht | Gespeicherte Filter nur als eigene Ansicht | **Übernehmen:** Filter als Kachel anheften | ST-020 |
| Bilder statt Text | Titelbilder, Galerie | Pinnwand-Vorschau als Bild; keine Zeichnungsvorschau | **Übernehmen:** Kachel „Zeichnungen“ | ST-030 |
| Favoriten | Abschnitt in Seitenleiste und Home | fehlt; „Favorit“ ist im Tagebuch schon ein Eintragsmerkmal | **Anpassen:** „Angeheftet“ | ST-040 |
| Zuletzt besucht | 20 Seiten | „Zuletzt bearbeitet“ | **Anpassen:** Umschalter geöffnet/bearbeitet | ST-050 |
| Suche und Sprung zu Seiten | zentrale Suche | Aktionssuche ohne Seiten und ohne Kürzel | **Übernehmen:** Seiten- und Befehlssuche | MO-010 |
| Pfad | Brotkrumen über der Seite | Pfad nur in Karten und Auswahllisten | **Übernehmen:** anklickbare Pfadzeile | MO-020 |
| Details ohne Kontextverlust | Seitenblick rechts | Punktmaske als Dialog | **Anpassen:** eingebetteter Detailbereich | MO-030 |
| Rückmeldung | – | Rückmeldung je Aktion, ohne Rückweg | **Übernehmen:** „Rückgängig“ im Hinweis | MO-040 |
| Seitensymbol | Emoji oder Bild | Farbe und ICONS-Zeichen | **Anpassen:** Pixelsymbol aus Glides Zeichenfläche | AO-050 |
| Archivieren | seit 3.4 | nur Papierkorb (200 Einträge) | **Beobachten** | MO-070 |
| Präsentationsmodus | seit 3.4 (Beta) | Pinnwand-Stufe 3 offen | **Beobachten** | MO-080 |
| KI-Agenten, Meeting-Notizen, Personenverzeichnis, Konnektoren | vorhanden | – | **Nicht übernehmen** (Konto, Netz, Team) | – |

### 3.3 Ergebnis

Glides Startseite ist in der Anordnung bereits flexibler als Notion Home. Es
fehlt die direkte Handhabung: Kacheln ordnen, verbreitern und ergänzen, wo man
sie sieht. Außerdem fehlen persönliche Ausschnitte (Filterkacheln) und mehr
Bild statt Text, etwa Zeichnungen als Miniaturen. Allgemein bringen drei
kleine Bausteine den größten Modernisierungsgewinn: Seitensuche mit Kürzel,
anklickbarer Pfad und Rückgängig direkt in der Rückmeldung.

Zwei Katalogpunkte stammen nicht aus dem Wettbewerb, sondern aus Glides
eigenen Vorgaben: Leerzustände mit nächstem Schritt (MO-050) setzen die
offene Stufe 3 des Arbeitsbegleiters um. Die visuelle Richtung „Pixel“
(MO-060) greift das Inspirationsbild im Projektordner auf: kräftige,
abgerundete Blockformen in Blau, Gelb und Pink auf Schwarz.

## 4. Pinnwand – Trello, OneNote, FigJam und Microsoft Planner

### 4.1 Befund

**Trello.** Das neue Trello (angekündigt 22.05.2025) bringt:

- **Posteingang:** Erfassung aus Mail, Slack und Teams.
- **Planer:** Kalender verbinden und Karten als Zeitblöcke hineinziehen.
- **Navigation:** Posteingang, Planer und Board auch nebeneinander.
- **Kartenrückseite:** kompakter, mit Hinzufügen-Menü unter dem Titel und
  Aktionsmenü oben rechts.

Weitere Merkmale:

- **Kartencover:** Farbe oder Bild, halb oder voll. Ein Modus für
  Farbfehlsichtige legt Muster auf farbige Cover.
- **Kartentypen:** Vorlagen-, Board-, Trenn- (`---`), Spiegel- und Link-Karte.
- **Listen:** Listen lassen sich einklappen, Name und Kartenzahl bleiben dabei
  sichtbar. Listenfarben gibt es ab Standard.
- **Ansichten:** Kalender; ab Premium zusätzlich Zeitleiste, Tabelle,
  Dashboard und Karte.

**OneNote.**

- **Seite:** eine freie Seite, Inhalte an beliebiger Stelle.
- **Zeichnen:** Stifte, Textmarker, Radierer, Lineal mit Winkel, Formen,
  Lasso, Umwandlung von Freihand in Text oder Form, Wiedergabe.
- **Seitenhintergrund:** Farbe sowie Linien oder Karo; auf Wunsch für jede
  neue Seite.
- **Tags:** „Aufgabe“ als Kontrollkästchen (Strg+1). Eine Tag-Zusammenfassung
  gruppiert nach Tag, Abschnitt, Titel oder Datum.
- **2026:** Bildzuschnitt, neue Stiftarten, Freihand-Wiedergabe,
  Laserpointer; Copilot teils nur mit Lizenz.

**FigJam.**

- **Klebezettel:** zwei Formen, Farbe wählbar, Autorname ein-/ausblendbar.
  Strg/Cmd+Enter legt direkt daneben einen neuen Zettel an, das Textfeld ist
  sofort aktiv.
- **Verbinder:** geknickt, gebogen oder gerade. Sie tragen Text mit
  Hintergrund, haben fünf Endpunktarten, sind gestrichelt oder durchgezogen,
  frei gefärbt und rasten an Objektkanten ein.
- **Abschnitte:** Umschalt+S; sie fassen Objekte zusammen und bewegen sie
  gemeinsam.
- **Aufräumen:** ordnet eine Auswahl in ein gleichmäßiges Raster, laut Figma
  auch zugunsten von Screenreadern.
- **Weiteres:** Stempel, Emotes, Abstimmung, Timer, Vorlagen und Widgets.
- **KI** (bezahlt): sortiert Zettel nach Thema, Farbe oder Autor.

**Microsoft Planner.**

- **Board:** Gruppieren nach Bucket, Zugewiesen, Fortschritt, Fälligkeit,
  Labels oder Priorität. Bei Gruppierung nach Fälligkeit ändert Ziehen in eine
  andere Spalte die Fälligkeit.
- **Kartenvorschau:** „Auf Karte anzeigen“ wählt ein Foto, eine Datei, einen
  Link, die Checkliste oder die Beschreibung; das erste Foto wird automatisch
  Vorschau.
- **Premium:** Zeitachse (Gantt), Personen, Ziele, Sprints, bis zu zehn eigene
  Felder, Abhängigkeiten, Meilensteine, Aufgabenverlauf und bedingte Färbung.

### 4.2 Vergleich und Bewertung

| Dimension | Vorbild | Glide 3.29 | Bewertung | Katalog |
|---|---|---|---|---|
| Spalten nach Feld | Planner, Notion-Board, Trello-Listen | frei oder geordnet, keine Feldspalten | **Übernehmen** | PW-010 |
| Ziehen ändert Feld | Planner (Fälligkeit), Notion (jede Gruppierung) | – | **Übernehmen** über `item_change` | PW-010 |
| Spalten einklappen, Anzahl, Farbe | Trello, Notion | – | **Übernehmen** | PW-010 |
| Karteninhalt wählbar | Planner „Auf Karte anzeigen“, Notion-Kartenvorschau | fester Inhalt mit Bildvorschau | **Übernehmen** | PW-020 |
| Farbcover mit Muster | Trello | Kontrastdesigns | **Anpassen** | PW-020 |
| Bereiche | FigJam-Abschnitte | Stufe 2 offen | **Übernehmen** | PW-030 |
| Auswahl aufräumen | FigJam | nur globale geordnete Anordnung | **Übernehmen** | PW-040 |
| Schnell weiterdenken | FigJam: Strg/Cmd+Enter, Verbinden per Ziehen | Modus „Verbinden …“; Doppelklick öffnet Maske | **Anpassen** | PW-050 |
| Verbindungen beschriften | FigJam | Richtung, kein Text | **Übernehmen** | PW-060 |
| Flächenhintergrund | OneNote Linien/Karo, FigJam-Raster | – | **Übernehmen** als Darstellung | PW-070 |
| Zeichnung auf der Fläche | OneNote-Stifte, FigJam-Marker | bewusst getrennt | **Anpassen:** Zeichnungsseite als Karte | ZF-100 |
| Zettel ohne Aufgabe | FigJam, OneNote | jede Karte ist ein echter Punkt | **Nicht übernehmen** (zweiter Bestand) | – |
| Spiegelkarten | Trello (kostenpflichtig) | derselbe Punkt auf mehreren Pinnwänden ist Grundprinzip | bereits vorhanden | – |
| Tags mit Zusammenfassung | OneNote | Labels, Labelansicht, Filter | bereits vorhanden | – |
| Eingang und Tagesplanung | Trello Inbox/Planner | Eingang, Mein Tag, Kalender | vorhanden; Zeitblöcke **beobachten** | AO-070 |
| Gantt, Sprints, Abhängigkeiten | Planner Premium, Notion | offen (ZF-200) | **Beobachten** | ZF-200 |
| Echtzeit, Stempel, Abstimmung, Timer, KI | FigJam, Trello | – | **Nicht übernehmen** | – |

### 4.3 Ergebnis

Alle vier Vorbilder trennen zwei Board-Formen, die Glide bisher in einer
Pinnwand vereint: die **freie Denkfläche** (FigJam, OneNote) und das
**Spaltenboard für den Arbeitsfluss** (Planner, Trello, Notion). Glide hat die
freie Fläche weit ausgebaut. Die größte Einzellücke ist ein Spaltenboard, in dem
Ziehen ein Feld ändert. Beide Formen bleiben Ansichten auf dieselben Punkte;
genau das unterscheidet Glide von Trello, wo Spiegelkarten eine
Zusatzfunktion sind.

## 5. Aufgaben, Ordnerstruktur und Darstellung – Notion

### 5.1 Befund

- Seiten lassen sich unbegrenzt ineinander verschachteln.
- **Datenbankansichten:** Tabelle, Board, Zeitleiste, Kalender, Liste, Galerie,
  Diagramm, Formular und seit 3.4 Dashboard.
- **Ordnen:** Gruppierung mit Untergruppen; einfache und erweiterte Filter
  (UND/ODER, drei Ebenen); mehrstufige Sortierung.
- **Board:** Gruppen nach Status, Auswahl, Person oder Relation. Spaltenfarbe,
  Kartengröße S/M/L, Bild einpassen oder zuschneiden; Kartenvorschau aus
  Titelbild, Inhalt oder Dateien. Ziehen ändert die Eigenschaft. Je Spalte eine
  Berechnung; Spalten lassen sich ausblenden.
- **Unterpunkte und Abhängigkeiten:** Unterpunkte verschachtelt (aufklappbar)
  oder als flache Liste. Abhängigkeiten gibt es nur in der Zeitleiste, mit drei
  Regeln zum Verschieben von Terminen.
- **Layouts:** Seitenkopf mit angehefteten Eigenschaften, Eigenschaftsgruppen,
  rechtes Seitenpanel und Reiter-Layout.

### 5.2 Vergleich und Bewertung

| Dimension | Notion | Glide 3.29 | Bewertung | Katalog |
|---|---|---|---|---|
| Tiefe der Hierarchie | unbegrenzt | 5 Ordnerebenen, Listen, Punkte bis Tiefe 100 | Glides Begrenzung **behalten** | – |
| Galerie mit Vorschau | Galerie, Kartenvorschau | Übersichtskarten mit Text | **Übernehmen** | AO-010 |
| Schnellaktionen in der Seitenleiste | „+“ und „•••“ beim Überfahren, einklappbare Abschnitte | Kontextmenü und Ziehen | **Anpassen** | AO-020 |
| Unterpunkte in der Tabelle | verschachtelt oder flach | nur flach | **Übernehmen** | AO-030 |
| Gruppieren nach Feld | Gruppe und Untergruppe | strukturelle Gruppen, Labelansicht | **Übernehmen** als Ansicht, gemeinsame Logik mit PW-010 | AO-040 |
| Seitensymbol | Emoji/Bild | ICONS und Farbe | **Anpassen:** Pixelsymbol | AO-050 |
| Eigenschaften im Seitenkopf | Layouts | Titel und Metazeile | **Beobachten** | AO-060 |
| Abhängigkeiten, Vorlagen mit Feldern | vorhanden | offen (ZF-200) | **Beobachten** | ZF-200 |
| Formulare, Personen, Datenbank-Baukasten | vorhanden | – | **Nicht übernehmen** (Baukasten, Team) | – |

### 5.3 Ergebnis

Glide soll Notion nicht als Baukasten nachbauen; die feste, verständliche
Struktur aus Ordner, Liste und Punkt ist eine Stärke. Übertragbar sind die
**Darstellungswerkzeuge**: Galerie mit Vorschau, Gruppieren einer Ansicht nach
Feld, verschachtelte Tabelle und schnelle Aktionen direkt in der Seitenleiste.
Das Seitensymbol wird in Glide zum Brückenstück in die Pixel-Nische.

## 6. Zeichnen und Design – Affinity, ergänzt um Pixel-Werkzeuge

### 6.1 Befund Affinity

- **Neue App:** Seit 30./31.10.2025 gibt es eine kostenlose App „Affinity“ von
  Canva. Sie vereint Vector-, Pixel- und Layout-Studio; Werkzeuge lassen sich
  mischen, Arbeitsbereiche anpassen und als Studio teilen. Ein Canva-Konto ist
  Pflicht; KI-Werkzeuge gibt es nur mit Canva Premium. Die App läuft auf Mac
  und Windows; eine iPad-Fassung ist angekündigt.
- **Kontextleiste:** Sie zeigt immer nur die Optionen des aktiven Werkzeugs,
  abhängig von Auswahl und Studio.
- **Farbfelder:** Dokument-, Programm- und Systempaletten; die zehn zuletzt
  verwendeten Farben; eine Palette aus den Farben des Dokuments; Import und
  Export als `.afpalette` und `.ase`; globale Farben. X tauscht Füllung und
  Kontur, D setzt sie zurück.
- **Farbwahl:** Farbrad (HSL), Schieberegler für RGB, HSL, CMYK und LAB, Box,
  Hex-Eingabe, Pipette auch außerhalb der App, zuletzt verwendete Farben.
- **Verlauf und Schnappschüsse:** benannte Zwischenstände, mit dem Dokument
  gespeichert, wiederherstellbar oder als neues Dokument.
- **Symbole und Assets:** verknüpfte Instanzen; eine Änderung wirkt überall.
- **Ansicht:** Pixel- und Retina-Pixelansicht, Umriss- und Röntgenansicht,
  geteilte Vergleichsansicht, Graustufenansicht, zweite Ansicht mit eigenem
  Zoom.
- **Hilfen:** Raster, auch isometrisch; Fang; erzwungene Pixelausrichtung.
- **Export-Persona:** Exportbereiche (Slices) in 1×, 2× und 3×, mehrere Formate
  je Bereich, Dateipfade mit Ordnern.
- **Pinsel:** Stabilisator mit Seil- oder Fenstermodus.

### 6.2 Befund Pixel-Werkzeuge (Nische)

- **Aseprite:**
  - Werkzeuge Stift, Linie, Kurve, Rechteck, Ellipse, Kontur und Polygon.
  - Linksklick malt mit der Vordergrund-, Rechtsklick mit der
    Hintergrundfarbe.
  - Symmetrie horizontal und vertikal; die Achse lässt sich verschieben, auch
    auf eine Pixelmitte.
  - Kachelmodus für Muster; Vorschaufenster (F7); indizierte Farben bis 256;
    Tilemaps; Animation mit Zwiebelschicht.
- **Pixelorama:**
  - Werkzeuge frei auf linke und rechte Maustaste legbar.
  - Pixel-perfekte Linien, Spiegelung auch diagonal, Kachelmodus.
  - Paletten importieren oder selbst anlegen, auch aus Lospec.
  - Ebenen mit Schnittmasken, Animation; Export als PNG, GIF und Spritesheet.
  - Anpassbare Oberfläche, automatische Sicherung.
- **Lospec:** großes Verzeichnis von Pixel-Art-Paletten, etwa PICO-8 mit 16
  oder Endesga mit 32 Farben. Die Nutzungsbedingungen sind je Palette vor einer
  Auslieferung zu prüfen.

### 6.3 Vergleich und Bewertung

| Dimension | Affinity | Pixel-Werkzeuge | Glide 3.29 | Bewertung | Katalog |
|---|---|---|---|---|---|
| Kontextleiste | ja | ja | zwei Zeilen, alles immer sichtbar | **Übernehmen** | ZD-010 |
| Zwei Farben, Rechtsklick | X/D | links/rechts | eine Farbe; Rechtsklick ungenutzt | **Übernehmen:** Weiß als zweite Farbe ersetzt den bewusst fehlenden Radierer | ZD-020 |
| Farben der Zeichnung, zuletzt verwendet | Dokumentpalette, 10 zuletzt | Palettenleiste | nur Dialog | **Übernehmen** | ZD-020 |
| Zoom und Verschieben | Zoomwerkzeug, zweite Ansicht | Mausrad | Schaltflächen, Tasten, Einpassen | **Übernehmen** | ZD-030 |
| Vorschau in Originalgröße | Pixelansicht, zweite Ansicht | Vorschaufenster | – | **Übernehmen** eingebettet | ZD-040 |
| Symmetrie | – | ja | – | **Übernehmen** | ZD-050 |
| Linie, Rechteck, Ellipse | ja | ja | ausgeschlossen (Entscheidung 24.09.2026) | **Entscheidung** | ZD-060 |
| Rückgängig | je Aktion mit Verlauf | je Aktion | 20 Zelländerungen | **Entscheidung** | ZD-070 |
| Zwischenstände | Schnappschüsse | automatische Sicherung | Vorher-Stand nur bei Nachzeichnen, Import, Leeren | **Anpassen** | ZD-080 |
| Palettenbibliothek | `.afpalette`, `.ase` | Lospec, `.gpl` | ≤ 256 je Zeichnung, keine Bibliothek | **Anpassen** mit Textformaten | ZD-090 |
| Farbe ersetzen | globale Farben | indizierter Modus | – | **Übernehmen** | ZD-100 |
| Kachelmodus | – | ja | – | **Übernehmen** | ZD-110 |
| Export in Größen | 1×/2×/3× | PNG, GIF | SVG, JSON | **Übernehmen:** PNG ganzzahlig, Tk 8.6 schreibt PNG selbst | ZD-120 |
| Pixel-perfekte Linie | Pixelausrichtung | ja | Ein-Drittel-Regel | **Übernehmen** als Option | ZD-130 |
| Flächengröße | frei | frei | fest 128 × 128 | **Entscheidung** | ZD-140 |
| Graustufen, Referenzdeckkraft | Graustufenansicht, Deckkraft | – | feste Blässe | **Übernehmen** | ZD-150 |
| Auswahl, Verschieben | ja | ja | – | **Beobachten** | ZD-160 |
| Dithering, Muster | – | ja | – | **Beobachten** | ZD-170 |
| Ebenen, Animation, Vektorpfade, Verläufe, Effekte, KI | ja | teils | bewusst nicht | **Nicht übernehmen** | – |
| Anpassbare Arbeitsbereiche und Kürzel | Studios | anpassbar | fest | **Nicht jetzt** (Pflege, Handbuchtreue) | – |

### 6.4 Ergebnis und Positionierung

Keine der untersuchten Anwendungen verbindet Organisation mit einem echten
Pixelraster:

- Notion, Trello und Planner zeichnen nicht.
- OneNote und FigJam zeichnen frei, ohne Raster und ohne Palette.
- Affinity, Aseprite und Pixelorama organisieren keine Aufgaben, Notizen oder
  Tagebücher.

Glides Nische ist deshalb **„Aufgaben, Notizen und Pixel an einem Ort – lokal,
ohne Konto“**. Sie wird stärker, je sichtbarer Pixelbilder in der Organisation
werden. Brückenstücke dafür sind Pixelsymbole für Seiten (AO-050), die Kachel
„Zeichnungen“ (ST-030), die Galerie-Übersicht (AO-010) und Zeichnungen als
Pinnwandkarte (ZF-100).

Im Editor selbst sind die übertragbaren Arbeitsabläufe klein und
pixelspezifisch: zwei Farben mit Rechtsklick, eine sichtbare Farbleiste,
Symmetrie, Vorschau in Originalgröße, Zoom mit dem Mausrad und PNG in
ganzzahligen Größen. Vektor-, Ebenen- und KI-Funktionen würden die Nische
verwässern.

## 7. Was Glide bewusst nicht übernimmt

| Funktion | Vorbild | Grund |
|---|---|---|
| Echtzeitmitarbeit, Kommentare, Zuweisung, Personenverzeichnis | alle | Glide ist lokal und persönlich; Konten und Server sind Produktgrenze. |
| KI-Agenten, KI-Sortierung, generative Bildfunktionen | Notion, FigJam, Planner, Affinity | Netz, Konto und Datenschutz; widerspricht „keine Telemetrie, kein Cloudzwang“. |
| Bildarchive aus dem Netz (Unsplash-Cover) | Trello | automatischer Netzzugriff |
| Freie Klebezettel ohne Aufgabe | FigJam, OneNote | zweiter Datenbestand neben den Punkten |
| Freihand-Tinte auf der Pinnwand | OneNote, FigJam | Zeichnung ist eine eigene Seitenart; sie erscheint als Karte (ZF-100). |
| Datenbank-Baukasten, Formulare, eigene Feldtypen | Notion, Planner Premium | aus einem Planer würde ein Baukasten; eigene Felder bleiben in ZF-200. |
| Vektorpfade, Verläufe, Ebeneneffekte, Animation | Affinity, Aseprite | verwässert die Pixel-Nische; ZF-300 hält sie nur als Forschungsvorrat. |
| Arbeitsbereiche und Kürzel frei belegen | Affinity, Pixelorama | Pflegeaufwand; Handbuch und Tastenkürzelübersicht müssen stimmen. |

## 8. Quellen

Abrufdatum aller Webquellen: 25.09.2026.

**Notion**

- [Notion 3.4, Teil 1 (26.03.2026): Dashboard, Seitenleiste, Präsentation, Reiter-Block, Archivierung](https://www.notion.com/releases/2026-03-26)
- [Dashboard-Ansicht](https://www.notion.com/help/dashboards)
- [Seitenleiste](https://www.notion.com/help/navigate-with-the-sidebar)
- [Ansichten, Filter, Sortierung, Gruppen](https://www.notion.com/help/views-filters-and-sorts)
- [Board-Ansicht](https://www.notion.com/help/boards)
- [Unterpunkte und Abhängigkeiten](https://www.notion.com/help/tasks-and-dependencies)
- [Layouts von Datenbankseiten](https://www.notion.com/help/layouts)
- [Seitengestaltung: Symbol, Titelbild, Schrift](https://www.notion.com/help/customize-and-style-your-content)
- Drittquelle: [Thomas Frank: Notion Home](https://thomasjfrank.com/notion-home-everything-you-need-to-know/)

**Trello**

- [Das neue Trello (22.05.2025)](https://www.atlassian.com/blog/announcements/new-trello-is-here)
- [Kartencover](https://support.atlassian.com/trello/docs/what-is-a-card-cover/)
- [Kartentypen](https://support.atlassian.com/trello/docs/card-types/)
- [Neue Kartenrückseite](https://support.atlassian.com/trello/docs/new-card-back/)
- [Liste einklappen](https://support.atlassian.com/trello/docs/collapse-or-expand-a-list/)
- [Listenfarbe](https://support.atlassian.com/trello/docs/change-the-color-of-a-list/)
- [Spiegelkarten](https://support.atlassian.com/trello/docs/mirroring-cards/)
- [Ansichten](https://trello.com/views)

**Microsoft Planner**

- [Aufgaben ordnen, Gruppieren nach, Ziehen ändert Fälligkeit](https://support.microsoft.com/en-us/office/organize-your-team-s-tasks-in-microsoft-planner-c931a8a8-0cbb-4410-b66e-ae13233135fb)
- [Vorschau auf der Karte](https://support.microsoft.com/en-us/planner/set-a-preview-picture-for-a-task)
- [Premium-Funktionen](https://support.microsoft.com/en-us/planner/teams/advanced-capabilities-with-premium-plans-in-planner)
- [Diagramme](https://support.microsoft.com/en-us/planner/view-charts-of-your-plan-s-progress)

**OneNote**

- [Zeichnen und Skizzieren](https://support.microsoft.com/en-us/onenote/onenote-help-and-learning/draw-and-sketch-notes-in-onenote)
- [Seitenfarbe](https://support.microsoft.com/en-us/office/change-the-background-color-of-a-page-in-onenote-5938f6c0-f4f7-4c16-b2ac-5f694ea76e17)
- [Tags anwenden](https://support.microsoft.com/en-us/onenote/onenote-help-and-learning/apply-a-tag-to-a-note-in-onenote)
- [Getaggte Notizen suchen](https://support.microsoft.com/en-us/onenote/onenote-help-and-learning/search-for-tagged-notes-in-onenote)

**FigJam**

- [Leitfaden zu FigJam](https://help.figma.com/hc/en-us/articles/1500004362321-Guide-to-FigJam)
- [Barrierearme Boards: Abschnitte und Aufräumen](https://help.figma.com/hc/en-us/articles/14477101678359-Create-accessible-FigJam-boards)
- [Verbinder](https://help.figma.com/hc/en-us/articles/1500004414542-Create-diagrams-and-flows-with-connectors-in-FigJam)
- [Klebezettel](https://help.figma.com/hc/en-us/articles/1500004414322-Sticky-notes-in-FigJam)
- [Zettel mit KI sortieren](https://help.figma.com/hc/en-us/articles/18711926790423-Sort-and-summarize-stickies-with-FigJam-AI)

**Affinity**

- [Canva: das neue Affinity](https://www.canva.com/newsroom/news/all-new-affinity/)
- [MacRumors: Affinity als kostenlose All-in-one-App (31.10.2025)](https://www.macrumors.com/2025/10/31/canva-relaunches-affinity-free-app/)
- [Kontextleiste](https://affinity.help/designer2/English.lproj/pages/Workspace/contextBar.html)
- [Farbfelder](https://affinity.help/designer2/English.lproj/pages/Panels/swatchesPanel.html)
- [Farbpanel](https://affinity.help/designer2/English.lproj/pages/Panels/clrPanel.html)
- [Schnappschüsse](https://affinity.help/designer2/English.lproj/pages/DesignAids/snapshot.html)
- [Symbole](https://affinity.help/designer2/English.lproj/pages/SymbolsAssets/symbols.html)
- [Ansichtsmodi](https://affinity.help/designer2/English.lproj/pages/GetStarted/view.html)
- [Export-Persona](https://affinity.help/designer2/English.lproj/pages/ExportPersona/exportPersona.html)
- [Pixelpinsel](https://affinity.help/designer2/English.lproj/pages/Painting/pixel_painting.html)

**Pixel-Werkzeuge**

- [Aseprite: Zeichnen](https://www.aseprite.org/docs/drawing/)
- [Aseprite: Symmetrie](https://www.aseprite.org/docs/symmetry/)
- [Aseprite: Vorschaufenster](https://www.aseprite.org/docs/preview-window/)
- [Aseprite: Kachelmodus](https://www.aseprite.org/docs/tiled-mode/)
- [Aseprite: Farbe](https://www.aseprite.org/docs/color/)
- [Pixelorama](https://github.com/orama-interactive/pixelorama)
- [Lospec-Palettenverzeichnis](https://lospec.com/palette-list)

**Lokale Quellen**

- [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md)
- [Ansichten und Startseite 3.22](../01_Repository/Glide/docs/48_ANSICHTEN_UND_STARTSEITE_3.22.0.md)
- [Designsystem 3.23](../01_Repository/Glide/docs/50_DESIGNSYSTEM_3.23.0.md)
- [Pinnwand als Arbeitsfläche 3.23](../01_Repository/Glide/docs/53_PINNWAND_ARBEITSFLAECHE_3.23.0.md)
- [Navigation und Pinnwand 3.24](../01_Repository/Glide/docs/55_NAVIGATION_UND_PINNWAND_3.24.0.md)
- [Startseite und Rückmeldung 3.24](../01_Repository/Glide/docs/56_STARTSEITE_UND_RUECKMELDUNG_3.24.0.md)
- [Übersichtlichkeit und Hierarchie 3.25](../01_Repository/Glide/docs/57_UEBERSICHT_UND_HIERARCHIE_3.25.0.md)
- [Startseite und Begleiter 3.25](../01_Repository/Glide/docs/58_STARTSEITE_UND_BEGLEITER_3.25.0.md)
- [Zeichnungsseite 3.29](../01_Repository/Glide/docs/65_ZEICHNUNGSSEITE_3.29.0.md)
- [Funktionsvergleich und Zeichenflächenkonzept](Glide_Funktionsvergleich_und_Zeichenflaeche_2026-09-23.md)
- [Historische Konkurrenzanalyse 17.09.2026](Archiv/Glide_Konkurrenzanalyse_2026-09-17.md)
- [Historische Feature-Gap-Analyse 18.09.2026](Archiv/Glide_Feature_Gap_Analyse_2026-09-18.md)
