# Design Richtlinien

Stand 22.10.2026 · Glide 3.44.0 · appweiter Gestaltungsvertrag; bestehendes UI-/UX-Paket und fortlaufende Übertragung

Dieses Dokument sammelt die belegten Gestaltungsvorgaben des Inhabers und ihre Konsequenzen für Glide. Es ist agentenunabhängig lesbar; der Claude-Code-Skill `design-richtlinien` (`.claude/skills/design-richtlinien/`) verweist nur hierher. Produktentscheidungen stehen weiterhin in [Arbeitsrichtung](ARBEITSRICHTUNG.md), Produktgrenzen in [Produktgrenzen](01_PRODUCT_CONSTRAINTS.md), technische Umsetzung in [Architektur](02_ARCHITECTURE.md), Funktionsverhalten in [Funktionen](20_FUNKTIONEN.md) und Aufgabenstatus im [Entwicklungsplan](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md). Diese Zuständigkeiten nicht durch Kopien ersetzen.

## Quellen und Geltung

| Quelle | Gegenstand | Geltung |
|---|---|---|
| [Leitgedanken und frühere Antworten](ARBEITSRICHTUNG.md) vom 25.09.–01.10.2026 | Vorbilder, klare Formen, geringe Komplexität, zuverlässiger lokaler Ablauf | Bestehende Entscheidungen bleiben maßgeblich, soweit neuere direkte Anweisungen sie nicht gezielt ändern |
| [Sechs Produktprinzipien und Hausregeln](01_PRODUCT_CONSTRAINTS.md) | Hierarchie, Rollenfarben, Fluchten, Inhalt vor Bedienung, Erreichbarkeit | Bestehende Quelle; technische Einzelregeln dort nachführen |
| [Nutzerauftrag vom 15.10.2026](../../../00_Arbeitsvorbereitung/Featurepaket_UI_UX/AUFTRAG.md) und [Ausführungsprompt](../../../00_Arbeitsvorbereitung/Featurepaket_UI_UX/PROMPT.md) | A01–A03 und B01–B22, 28 Bildreferenzen | Seit D50 (15.10.2026) beauftragt und vorrangig vor Paket 8; bei unvereinbaren älteren Vorgaben gilt dieses Paket |
| Fremdreferenz im Skill `design-richtlinien/referenzen/` | Bewegung, Material, Typografie, Gestaltungsgrundsätze (MIT, Emil Kowalski, `emilkowalski/skills`) | Hintergrund; nur die unten übersetzten Grundsätze gelten |

Die Projektbezeichnung lautet **Design Richtlinien**; der frühere markenbezogene Skillname ist seit B20 kein aktiver Projektname mehr. Quellnachweise und Lizenz-/Copyright-Angaben bleiben erhalten; die neutrale Benennung ist keine rechtliche Freigabe. Historische Zitate und Eingangsbelege werden nicht nachträglich umgeschrieben.

## Verbindliche Gestaltungsvorgaben

### Bedienelemente schützen (B15, 15.10.2026)

Jeder Button benötigt einen eindeutigen Zweck und eine Funktion. Er muss in den vorgesehenen Fenstergrößen sichtbar, lesbar und erreichbar bleiben. Texte, Hinweise, Bilder und andere Bereiche dürfen seine Fläche weder überdecken noch abschneiden. Reicht Platz nicht, müssen Layout, Umbruch oder Scrollbereich reagieren. Wirkungsloses Bedienelement ausblenden oder seinen tatsächlichen Zustand verständlich darstellen.

**Umsetzungsregeln:** Ein Element, das unter einem umbrechenden Text steht, folgt dessen tatsächlicher Höhe bei jedem Neuumbruch (Leerzustände: `_follow_empty_text`). Positionen nie nur beim ersten Aufbau berechnen. Knopfreihen, die bei der Mindestgröße nicht in eine Zeile passen, brechen um (`ButtonFlow`), statt den letzten Knopf zu quetschen – so die Optionszeile des Spaltenboards („Nur offene“ war bei 860 px abgeschnitten, gefunden mit der appweiten Prüfung am 16.10.2026).

Prüfen: Mindestgröße, große Schrift, DPI, lange deutsche Texte, Hinweise an/aus, Inspektor offen, Größenwechsel, leere und gefüllte Zustände. Die Regel gilt appweit einschließlich Dialogen. Automatisch misst `test_uiux_paket.py` sie zweifach: Fall b06_b15 für den Papierkorb in zwölf Kombinationen, Fall b15_appweit für jeden sichtbaren Knopf in sieben Hauptansichten (Startseite, Heute, Labels, Vorlagen, Papierkorb, Liste, Seite) und fünf Dialogen (Über Glide, Neuerungen, Fehlerprotokoll, Tastenkürzel, Einstellungen) bei 860 × 700 und 1280 × 800, mittlerer und großer Schrift, Hinweisen an und aus: kein fremdes Text-, Eingabe- oder Knopfelement im sichtbaren Knopfbereich, außerhalb scrollbarer Flächen vollständig im Fenster, Beschriftung nicht breiter als der Knopf. Gegen 3.42.0 findet dieselbe Prüfung das gemeldete Überdecken von „Zur Startseite“ im Papierkorb (S21). Eine Geometrieprüfung ersetzt nicht die Sichtprüfung weiterer, seltener Dialoge.

### Informationshierarchie vor starrer Metadatenbreite (B11)

Für jede Ansicht gilt, welche Information die aktuelle Nutzerabsicht zuerst unterstützt. Titel und wesentlicher Inhalt dürfen nicht früh verschwinden, während nachrangige Metadaten ungenutzte Breite belegen. Datum und Uhrzeit können im Planungs-/Kalenderkontext selbst primär sein; deshalb keine globale Titel-vor-Datum-Regel ohne Kontext.

**Umsetzungsregel:** Metadatenspalten sind so breit wie ihr tatsächlicher Inhalt (gemessen), höchstens so breit wie das Muster des längsten möglichen Werts; den Rest bekommt der Titel. Bei Enge weichen Metadaten ganz (zuerst Labels, dann Fälligkeit; in „Heute“ behält der Titel mindestens 260 px), abgeschnitten werden sie nie. Bis 3.42.0 erzwang eine Uhrzeit irgendwo in der Ansicht die volle Musterbreite (in „Labels“ 281 statt 177 px). Kurze Leer- und Verweiszeilen in Textspalten tragen keine Angaben, die schon im Titel stehen. Automatisch geprüft je Aufgabenansicht (Labels, Heute, Liste; Fall b11): Titel ist die breiteste Spalte, Datum und Labels höchstens so breit wie ihr Inhalt und entweder vollständig oder ganz ausgeblendet.

Prioritätsmatrix, am 15.10.2026 an den realen Ansichten mit Showcase-Daten geprüft (Windows, 1280 × 800 und 860 × 700):

| Ansicht/Kontext | Vorrangige Information | Danach | Layoutkonsequenz | Prüfstand |
|---|---|---|---|---|
| Startseite | Gewählte Inhalte, nächste sinnvolle Handlung | Fortschritt, Kontext und Vorschauen | Zusammenhängendes Raster, Anpassungsaktion an der linken Rasterkante | umgesetzt (B02, B04) |
| Heute/Demnächst | Aufgabentitel und relevante zeitliche Lage | Liste, Label, weitere Metadaten | Eindeutige Zustände, nur Titel der nächsten Aufgabe fett; kurze Leerzeile | umgesetzt (B12, B13); Herkunftsspalte bleibt rechts |
| Liste/Labels/Suchergebnisse | Titel und Treffer-/Aufgabenkontext | Erforderliche Fälligkeit, Label, Herkunft | Titel flexibel, Metadaten auf Inhaltsbreite | umgesetzt (B11); Herkunft hängt in „Labels“ am Titelende und wird zuerst gekürzt |
| Tabelle | Gewählte Spalten und deren Feldwerte | Zusätzlicher Kontext | Eigene, ziehbare Spaltenbreiten bleiben | unverändert |
| Kalender/Zeitplanung | Termin-/Zeitposition und Aufgabe | Dauer, Fälligkeit, Herkunft | Zeitinformation darf hier Vorrang haben | unverändert |
| Pinnwand/Board | Karteninhalt und räumlicher Zusammenhang | Status, Label, Verbindungen | Einheitliche Symbole, keine störenden Aktionsflächen | unverändert |
| Seite/Notiz/Notizbuch | Lesbarer bzw. bearbeitbarer Inhalt | Titel, Momentdatum, Kontextaktionen | Natürlich scrollen, Bild und Folgetext erreichen | umgesetzt (B16, B17) |
| Buch/Ordner | Erkennbare enthaltene Objekte | Typ und Status | Klare Navigation ohne unnötige Metadaten | unverändert |
| Galerie/Zeichnung | Bild bzw. Werk und seine Identität | Zugehörigkeit und Aktionen | Seitenverhältnis bewahren, fehlende Vorschau verständlich | umgesetzt für die Startseitenvorschau (B04) |
| Vorlagen | Name und Verwendungszweck | Struktur-/Anwendungskontext | Auswahl verständlich, Hauptaktion geschützt | unverändert |
| Papierkorb | Leerzustand oder wiederherstellbare Objekte | Ergänzender Hinweis | Kurzer Standardtext, Aktionen niemals überdecken | umgesetzt (B15) |
| Inspektor/Dialog | Aktuelle Bearbeitung und Bestätigung | Felder nach Bedarf | Eindeutige Eingabeflächen und geschützte Aktionen | umgesetzt (B08, B19) |

### Fluchten und optische Zentrierung (B02, B05, B07–B09)

Zusammengehörige Texte und Aktionen teilen erkennbare Kanten, Abstände und Höhen. Menü, Kopfaktionen, Dialogüberschrift und Fließtext dürfen nicht zufällig versetzt wirken. Gemeinsame Layout-/Symbolregeln gegenüber isolierten Einzelversätzen bevorzugen.

- **Kopfzeile (B07):** Windows-Menüs und Kopfsymbole stehen in derselben Titelzeile, haben dieselbe Höhe (`HEADER_CONTROL_HEIGHT`, 38 px = Höhe der Titelzeile) und damit dieselbe Mittellinie; der Kopf wird dadurch nicht höher (Bedienfläche ≤ 15 % bei 1280 × 800 bleibt erfüllt). Die Unterzeile behält die volle Breite.
- **Logo (B05):** vom oberen Rand der Großbuchstaben des Titels bis zur Grundlinie der Unterzeile; Seitenverhältnis unverändert.
- **Texte in Dialogen (B08):** Überschrift und Meldungstext beginnen an derselben Pixelkante; Labels dafür ohne Standardrand und -innenabstand.
- **Startseite (B02):** „Startseite anpassen“ steht an der linken Kante des Kachelrasters im Kachelabstand darunter.
- **Symbolmitte (B09):** Die sichtbare Mitte eines Symbols liegt auf der Mitte der Großbuchstabenhöhe seines Textes; in Baumzeilen auf der Mitte der geometrischen Bezugsformen (▣ ◉ ◈ ▤). Gerechnet wird aus den Glyphenrahmen der mitgelieferten Schrift (`glyph_metrics.py`), nicht mit festen Pixelversätzen. Gemessen nach der Umsetzung: Bereichspfeile −0,3 px, Papierkorbsymbol im selben Abstand zum Text wie die übrigen Systemsymbole. Gleiche Widgetkoordinaten garantieren bei verschiedenen Glyphen keine gleiche wahrgenommene Höhe.
- **Pfadtrenner (B09, 16.10.2026):** „›“ sitzt typografisch auf der x-Höhe und stand in Knöpfen mit Pfaden – etwa der Startseitenkachel „Pinnwände“ – rund 1 px unter der Großbuchstabenmitte. Knöpfe (`RoundedButton`) setzen jeden Trenner einzeln auf die Großbuchstabenmitte (gemessen −0,05 px); Schreibweise, Umbruch und Lage der übrigen Zeichen bleiben pixelgleich. In nativ gesetzten Texten (Baumzeilen, Fenstertitel, Exporte) bleibt „›“ unverändert.

### Klare Formen und stabile Symbolbedeutung (B10, B12, B14)

Ein Symbol hat eine nachvollziehbare Bedeutung. Abschnittsköpfe mit Aufklapppfeil tragen kein zweites Dreieck oder Pfeilzeichen; ▶/◀ blättern, ▿/▷ klappen. Die Lupe ⌕ kennzeichnet die Suche. Die Seiten-Blockleiste trägt keine Symbole vor einzelnen Beschriftungen. Plattformweite Glyphenabdeckung, zugängliche Benennung und Fokus mitprüfen. Zentrale `ICONS`- und Rollenfarbregeln an ihrer Quelle pflegen.

**Symbolschrift (B10, präzisiert D29):** Zeichen kommen aus der tatsächlich verwendeten UI-Schrift (mitgelieferte DejaVu Sans). Fehlt ein bedeutungstragendes Zeichen dort, darf es gezielt aus einer einfarbigen Systemschrift des Betriebssystems kommen, wenn diese das Zeichen nachweislich selbst enthält (`SYMBOL_FONT_FALLBACKS` in `symbol_policy.py`, derzeit nur die Lupe: Segoe UI Symbol, Apple Symbols, Noto Sans Symbols, DejaVu Sans Mono). Keine Emoji-, Icon- oder mitgelieferte Zusatzschrift. Fehlt jede, bleibt der lesbare Textrückfall („Su“).

### Typografie gezielt einsetzen (B13)

Hervorhebung folgt der Information. In „Nächste Aufgabe“ ist nur die Titelzelle fett, in normaler Zeilengröße; Datum, Label und Herkunft bleiben nachgeordnet. Das ändert nicht pauschal alle vorhandenen Überschriftenstufen (D22 bleibt für Heute-Kopf, Listen, Seiten und Inspektor bestehen).

### Ruhige, zusammenhängende Flächen (B17, B19)

Unbeabsichtigte Hintergrundrechtecke um Aktionsgruppen und Editorfelder vermeiden. Echte Eingabeflächen, Konturen, Fokus, Auswahl, Hover und deaktivierter Zustand bleiben verständlich. Alle Designs und Verläufe prüfen.

**Umsetzungsregel „Trägerfläche“:** Ein Element übernimmt die Farbe der Fläche, auf der es tatsächlich liegt (`surface_key`, `DueField.surface`, `blend_embedded_editor`) – nicht pauschal die Fensterfarbe. Mit Hintergrundverlauf zeichnet Glide den Verlauf in jede Fläche in Fensterfarbe; ein falsch eingefärbtes Element erschien deshalb als Verlaufsstück. Ein Knopf ohne Kontur ist in Ruhe durchsichtig; Überfahren, Fokus und aktiver Zustand bleiben sichtbar.

### Hinweise bei Bedarf (B06, B15)

Ergänzende Bedienhinweise schaltet **Einstellungen › Darstellung und Bedienung › „Ergänzende Bedienhinweise in den Ansichten anzeigen“** für alle Ansichten gemeinsam; Vorgabe aus. Eine frühere Wahl je Ansicht („?“) wird übernommen: War irgendwo aufgeklappt, bleiben Hinweise sichtbar. Datum und „?“ stehen nicht mehr im Kopf. Notwendige Zustands-/Fehlermeldungen, Feldbezeichnungen und vom Benutzer geschriebene Hinweisblöcke innerhalb von Seiten (D06) sind davon getrennt. Der Papierkorb zeigt standardmäßig „Der Papierkorb ist leer.“; bei aktivierten Hinweisen zusätzlich „Gelöschte Punkte, Listen und Ordner landen hier und bleiben wiederherstellbar.“ Bedienwege in Textzeilen („Doppelklick öffnet“) zählen zu den ergänzenden Hinweisen.

### Vorhersehbar reagieren und scrollen (B01, B16)

Kleine Scrollbewegungen dürfen nicht Bild und erste Textzeile unkontrolliert überspringen: Über einem Seitenbild scrollt das Rad genauso pixelweise wie über dem Text (Tk-Klassenbindung), keine doppelte Ereignisverarbeitung oder künstliche Verzögerung. Nach dem Lesen der Neuerungen steht die Startseite unmittelbar am Anfang; normale Aktualisierungen bewahren ihren Scrollzustand.

### Gismo und Vorschauen (B03, B04, B18)

Gismo heißt fest Gismo und behält seine spielerischen Funktionen (Füttern, Spielen, Ruhen, Reaktionen), solange seine Kachel sichtbar ist. Wer ihn nicht möchte, blendet die Kachel unter „Startseite anpassen“ aus; dann erscheint er auch nicht neben Leerzuständen. Umbenennen und „Spielereien aus“ entfallen; frühere Werte werden beim Laden entfernt. Bewegungsreduktion nimmt nur die Bewegung, nicht die Funktionen. Die Zeichnungsvorschau bleibt; Galeriebilder haben eine eigene Kachel „Galeriebilder“. Neuerungen bleiben unter Hilfe › Über Glide › „Neuerungen …“ nachlesbar.

## Übernommene Grundsätze aus den Skillquellen, übersetzt nach Tk (B20)

Ausgewählt aus dem Fremdtext unter `referenzen/` (Bewegung, Material, Typografie, Gestaltungsgrundsätze) und aus den übrigen Skills von `emilkowalski/skills` (MIT); nur, was zu einer lokalen Tk-Desktop-App passt. Web-Beispiele (CSS, JavaScript, Federanimationen) gelten nicht.

| Grundsatz der Quelle | Übersetzung für Glide (Tk) | Bezug |
|---|---|---|
| Sofortige Rückmeldung, keine Latenz | Rückmeldung im selben Ereignis; Aufbau-/Scrollwege messen (D46/D48), keine künstlichen Wartezeiten | B16, Performance-Auftrag |
| Unterbrechbare Übergänge | Bewegung ≤ 150 ms, abbrechbar, keine zurückbleibenden `after`-Aufträge (bestehende Regel aus Paket 3) | D22-Umfeld, Architektur |
| Bewegungsreduktion statt Funktionsverlust | „Bewegte Rückmeldung“ aus: Zustände wechseln ohne Bewegung, Funktionen bleiben | B03 |
| Material und Tiefe ordnen Hierarchie | Getönte Karten (Milchglas) und Verläufe nur als Fläche; Elemente übernehmen die Trägerfläche | B17, B19 |
| Typografie: Hierarchie aus Gewicht, Größe und Abstand; Gewicht vor Größe | Hervorhebung zuerst durch Gewicht; vorhandene Textstufen (D22) statt neuer Größen | B13 |
| Konsistenz: Gleiches sieht gleich aus und verhält sich gleich | Ein Symbol, eine Bedeutung; Aufklappen und Blättern getrennt | B12, B14 |
| Gruppierung und Zuordnung | Steuerelement nah an dem, was es betrifft, an gemeinsamer Kante | B02, B07 |
| Einfachheit statt Minimalismus | Ergänzende Hinweise abschaltbar, notwendige Meldungen bleiben | B06 |
| Handwerk: nichts ist zufällig | Fluchten und optische Mitte nach Regel und Messung, nicht nach Augenmaß einzelner Pixel | B05, B08, B09 |
| Worst-Case-Daten prüfen (Skill „break-ui“) | Lange Titel, fehlende/lange Metadaten, leere und volle Zustände, große Schrift, kleine Fenster in jede Sichtprüfung; künstliche Daten | B11, B15, QA |

**Geprüft und bewusst nicht übernommen** (16.10.2026, Quelle `skills-main/` des Inhabers, lokal und nicht versioniert): `animate`, `animate-expo`, `improve-animations`, `review-animations`, `find-animation-opportunities` und `animation-vocabulary` beschreiben Web- bzw. React-Native-Bewegung (Kurven, CSS-Übergänge, Federn) – für Glide gilt daraus nur die Kurzregel oben (kurz, unterbrechbar, abschaltbar). `mobile-native` (Mobilbrowser), `pick-ui-library` und `ask-sonner` (JavaScript-Bibliotheken), `write-swift` (Swift) und `prototype` (Web-Variantenumschalter) passen nicht zu einer lokalen Tk-App. `emil-design-eng` deckt sich in den gestalterischen Punkten mit den übernommenen Grundsätzen. Installiert wird kein weiterer Skill; Glide-Regeln stehen nur hier.

## Offene Untersuchungen

A01 (Kompaktmodus), A02 (zwei Inhalte gleichzeitig) und A03 (Notion-Muster) sind untersucht; Optionen, Empfehlungen und Aufwand stehen im [Entwicklungsplan §17](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#17-ui-ux-feature-paket-aus-nutzerbeobachtungen-15102026) bzw. für A03 in [Markt und Vorbilder §10](../../../00_Arbeitsvorbereitung/Glide_Markt_und_Vorbilder.md). Bis zur Auswahl gilt die Mindestgröße 860 × 700, und Funktionen leben eingebettet in der Ansicht.

## Pflege und Prüfung

Neue direkte Nutzeranweisungen mit Datum, Quelle und betroffenem Kontext hier integrieren. Geänderte Regeln gezielt ersetzen, unveränderte bewahren, offene Empfehlungen als solche markieren. Keine personenbezogenen oder unbestätigten Vorlieben ergänzen.

Die passende Prüfung in [Prüfplan](05_QA_TESTPLAN.md) und [manueller Prüfliste](../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md) pflegen. Layoutattribute und automatische QA ergänzen die tatsächliche Sichtprüfung; sie ersetzen keine optische, Bedien-, DPI- oder Screenreaderabnahme. Ergebnisse gehören in den [QA-Bericht](07_QA_BERICHT.md). Die Namens- und Verweisprüfung des Skills läuft als `tests/tools/test_design_richtlinien.py` in der CI-Grundstufe.

Bei jedem Paketabschluss zuletzt Dokumentation, Ablage, aktive Referenzen und Projektauftritt abgleichen (B22). Originalauftrag und offene Bildreferenzen als Eingangsbelege erhalten; erledigte/überholte Arbeitsdokumente nach [Dokumentenpflege](DOKUMENTENPFLEGE.md) zusammenführen und bereinigen.

## Appweite Übertragung und zukünftige Entwicklung

Der neue Inhaberauftrag verlangt mehr Einfluss dieser Richtlinien auf die **gesamte App** und ihre künftige Entwicklung. Die Regeln gelten deshalb für neue und angefasste Oberflächen einschließlich Import/Export, Fehlermeldungen, Vorlagen, Zeichnungen, Einstellungen und optionaler Integrationen. Der dokumentierte Geltungsbereich ist verbindlich; die bestehenden Ansichten sind dadurch nicht pauschal neu abgenommen. Bestehende Abweichungen werden über WA-32 im einzigen Entwicklungsplan bearbeitet.

### Gemeinsame Komponenten und semantische Rollen

Gleiche Bedeutung verwendet dieselbe Rolle und denselben Baustein: Kontextkopf, Titel/Untertitel/Inhalt/Metadatum, Abschnitt, Feld mit Label/Hilfe/Fehler, primäre/sekundäre/destruktive Aktion, Aktionsüberlauf, Karte, Vorschau und Zustandsmeldung. `ui_design.py`, Rollenfarben, `ICONS`, Schriften und vorhandene `ButtonFlow`-/Feld-/Modalbausteine sind erste Anlaufstelle. Abstände, Radien und Schriftgrößen an semantischen Rollen ausrichten. Fachlich unterschiedliche Editor-/Zeichnungsrollen dürfen begründet abweichen; keine globale Zahlenersetzung und keine allein dekorative neue Komponente.

Ein Kontextkopf nennt die aktuelle Arbeit und ihre relevanten Zustände, ohne die eigentliche Dokumentüberschrift unnötig zu verdrängen. Wiederholung von Titeln ist je Kontext zu prüfen; D22 bleibt, bis eine konkrete Ergänzung ausgewählt ist. Eine gemeinsame Aktionsleiste priorisiert die häufige Handlung und führt weitere Aktionen in einen lesbaren Überlauf. Kürzel und Palette öffnen dieselbe Aktion. Der aktive Editor und das Ziel jeder Mutation bleiben eindeutig.

Feldzustände sind erkennbar: normal, Fokus, ungültig mit konkreter Korrektur, deaktiviert mit Grund, gespeichert bzw. fehlgeschlagen. Erfolg wird erst nach tatsächlicher Wirkung gemeldet. Leere Ansicht, keine Suchtreffer, Ladezustand, fehlendes Bild, Fehler, Schreibschutz und Offline-Cache sind verschiedene Zustände. Notwendige Rückmeldungen bleiben auch bei ausgeschalteten Bedienhinweisen sichtbar. Farbe unterstützt Bedeutung; Text, Symbol und Fokus dürfen sie nicht allein voraussetzen.

Vorschauen zu Import, KI, Restore und Export zeigen gewählten Umfang, wirksame Anweisung bzw. Änderungen, Verluste, Ziel und Abbruchweg vollständig lesbar. Kein abgeschnittener Text als einzige Kontrollmöglichkeit. Bei einem späteren Netzweg ist vor Übertragung sichtbar, welche Daten an welchen Dienst gehen. Der Dateiaustausch verwendet denselben verständlichen Kontrollpunkt.

### Kontextmatrix für die gesamte App

| Kontext | Gestaltungsauftrag / wiederverwendbarer Baustein | Nötige Bereichsprüfung |
|---|---|---|
| Kopf, Menü, Seitenleiste | ruhige Hierarchie, optisch ausgerichtete Symbole, lesbarer aktiver Kontext | lange Namen, schmale/ausgeblendete Leiste, große Schrift, Menü/Kürzel/Fokus |
| Startseite / Gismo / Kacheln | Inhalt vor Dauerbedienung, konsistentes Raster, Vorschau mit Status | leere/volle Kacheln, Umbruch, Anpassung, Bildfehler, Hinweise an/aus |
| Heute / Demnächst / Tagesplan | Titel und relevante Zeitlage, echte Feldsemantik | überfällig/leer, Tageswechsel, Uhrzeit, lange Titel, Metadaten bei Enge |
| Liste / Labels / Suche | Treffer und Originalidentität, Aktionen an Auswahl | Auswahl/Fokus/Scroll nach Mutation und Undo, Trefferlücke, große Bestände |
| Tabelle / gespeicherte Ansicht | gleiche Feldrollen, erklärbare Filter-/Sortierwirkung | viele Spalten, kein Treffer, ungültige Bedingung, Größenwechsel, Altleser |
| Kalender / Wochenrückblick | Zeitinformation vorrangig, Einplanen verändert benanntes Feld | Umbruch der Aktionsreihen, Wochen-/Tageswechsel, Kapazität, Belegzeiten |
| Pinnwand / Spaltenboard | Inhalt und Beziehungen, sparsame Werkzeuge, Original öffnen | kleine Kartenhöhe, leere Spalten, Verbindungen, Tastatur, Hostabbau |
| Seite / Blockeditor | Lesefluss, sichtbare Einfügestelle, Kontextaktionen | lange Titel, Bild-/Textscroll, Flushfehler, Aufgaben-/Verweisidentität |
| Notiz / Notizbuch / Buch / Ordner | zeitliche bzw. strukturelle Herkunft, Inhalt zuerst | leere Sammlungen, Datumswechsel, Umbenennung, Fokus-/Editorwechsel |
| Galerie / Cover / Anhänge | Seitenverhältnis und Original schützen; Laden/Fehler/Retry benennen | kalte/warme Vorschau, fehlende/ersetzte Datei, Größenwechsel, Abbruch |
| Pixel / Bildfolge / Palette | Werkfläche zuerst, kontextbezogene Werkzeuge und prüfbare Ausgabe | Zoom/Framewechsel, kleine Größe, Palette, Fokus, Undo, Exportvorschau |
| Inspektor / Punktmaske | gleiche Feld-/Fehler-/Rhythmusrollen, gesicherte Aktionen | große Schrift, scrollbarer Inhalt/fester Fuß, kleine Größe, Schreibfehler |
| Vorlagen / Auftragsdialog | Verwendungszweck vor technischem Detail, effektiven Inhalt lesen | lange eigene Vorlage, leere Auswahl, Musterantwort, Kopieren/Dateiausgabe |
| Import / Export / Restore / Vergleich | Vorschau, Umfang, Verlust und eindeutiger Rückweg | Abbruch, kaputte Quelle, fehlender Anhang, Pfadlänge, Schreibschutz |
| Einstellungen / Hilfe / Neuerungen | klare Abschnitte und Fluchten, erreichbarer Abschluss | Umfang/Scroll, große Schrift, Modal-/Tabfokus, Neustart, Hinweise |
| Papierkorb / Archiv / Fehlermeldungen | kurze Zustandsaussage, Wiederherstellen von Löschen unterscheiden | leer/voll, Umbruch, fehlerhafter Rückweg, keine überdeckten Knöpfe |
| P8 / Reader / Betrieb | semantischer Name/Zustand, sichtbarer Fokus und Tastaturalternative | echte Reader-/native Tests; Screenshot/Attribute ersetzen diese nicht |
| Optionale Integrationen | Quelle/Cachealter/Übertragung/Zustimmung verständlich | offline, fehlende Rechte, Ablauf/Retry/Abbruch, volle Datenvorschau |

### Verbindlicher Nachweis je neuem oder angefasstem UI-Paket

Vor der Umsetzung betroffene Zeilen dieser Matrix und bestehende B-/D-Regeln nennen. Danach tatsächliche Screenshots und Geometrie-/Funktionsprüfung mit künstlichen Daten: mindestens 860 × 700 und 1280 × 800, mittlere/große Schrift, betroffene helle/dunkle/Verlaufsdesigns, lange deutsche Inhalte, Hinweise an/aus und die relevanten Leer-/Fehler-/Schreibschutzzustände. Modal-/Tastaturfokus, Auswahl/Scroll, Undo/Redo und aktiver Host gehören zum Ablauf. Eine Abweichung braucht Grund und Entscheidung bzw. klar markierten Vorschlag; „sieht modern aus“ ist kein Abnahmekriterium.

Der [frische Audit 21.10.](../../../00_Arbeitsvorbereitung/Glide_Analyse.md#135-frische-designprüfung-und-vollständiger-geltungsbereich) hat Umbruch/Knopfschutz in konkreten Fenstern bestätigt und Verbesserungskandidaten bei Seitenhierarchie, Boardwerkzeughöhe und KI-Auftragsvorschau gezeigt. Er umfasst 19 gesichtete eigene Aufnahmen, weitere Bereiche nur strukturell bzw. über bestehende Funktionstests. Die volle Kontextmatrix ist daher Arbeitsvertrag und Prüfumfang für künftige Pakete, keine Behauptung einer bereits abgeschlossenen appweiten visuellen/native Abnahme.
