# Weitergabe – Glide-Zeichenfläche, SVG, PNG-Referenz und Nachzeichner

Stand 24.09.2026 · Glide 3.28.0 · produktives Aufgabenformat 18 · Prototypformat `glide.drawing` 1

## 1. Zweck dieser Weitergabe

Dieses Dokument ist der kanonische Einstieg für einen neuen Bearbeiter oder
einen anderen Agenten. Es führt Produktentscheidungen, Implementierung,
Begründungen, behobene Probleme, Prüfbelege und offene Integrationsarbeit an
einer Stelle zusammen. Die ausführliche Wettbewerbsrecherche und die
Arbeitspakete bleiben eigenständige Quellen; diese Weitergabe ersetzt sie
nicht.

Vor Änderungen in dieser Reihenfolge lesen:

1. `AGENTS.md` im Repository;
2. dieses Dokument;
3. [isolierter Zeichenflächenkern](61_ZEICHENFLAECHE_ISOLIERTER_KERN_2026-09-24.md);
4. [Aufgabensammlung](../../../00_Arbeitsvorbereitung/Glide_Aufgabensammlung_Zeichenflaeche_2026-09-23.md);
5. [SVG- und Speicheruntersuchung](../../../00_Arbeitsvorbereitung/Glide_SVG_und_Zeichnungsdaten_Untersuchung_2026-09-23.md);
6. [Produktvergleich](../../../00_Arbeitsvorbereitung/Glide_Funktionsvergleich_und_Zeichenflaeche_2026-09-23.md);
7. [Daten, Backup und Migration](06_DATA_BACKUP_MIGRATION.md) vor jeder produktiven Integration.

## 2. Wahrer Projektstatus

Der Zeichenkern und die Tk-Bedienprobe sind implementiert und automatisiert
geprüft. Sie sind bewusst von der produktiven Anwendung getrennt.

**Umgesetzt:**

- festes 128-×-128-Zellmodell;
- Pinsel, Füllung und Pipette;
- vier Pinselgrößen;
- zellweises Undo/Redo;
- kanonischer JSON-Rundlauf;
- sichtbares Standard-SVG mit eingebettetem Glide-Modell;
- strenger, passiver SVG-Rückimport;
- eigenständig startbare Tk-Bedienprobe;
- PNG-Rahmung, Referenzebene und automatischer Nachzeichner;
- Farbwahl über Spektrum und robuste Texteingabe;
- automatisierte Kern- und UI-Regressionstests.

**Nicht umgesetzt:**

- `drawing` als produktive Glide-Listenart;
- Migration des produktiven Aufgabenformats 18;
- Autosave in `liste_speicher.json`;
- Ordner-, Tagebuch-, Suche-, Vorlage-, Papierkorb- und Pinnwandintegration;
- produktive Anhangsverwaltung der PNG-Referenz;
- Voll- und Teilbackup einschließlich Referenz;
- Windows-, DPI-, Mehrmonitor-, Screenreader- und Releasefreigabe.

Die App-Version bleibt 3.28.0 und das produktive Aufgabenformat bleibt 18. Es
darf nicht behauptet werden, die Zeichenfläche sei bereits eine freigegebene
Glide-Funktion.

Der äußere Projektordner ist kein Git-Checkout. Es gibt daher in diesem Stand
keinen Commit oder Branch als Übergabepunkt. Maßgeblich sind die hier genannten
Dateien und Prüfprotokolle im OneDrive-Projektordner.

## 3. Verbindliche Produktentscheidungen

| Bereich | Entscheidung | Folge |
|---|---|---|
| Inhaltsarten | Listenarten: Notizen, Liste, Zeichnung und Pinnwand; Ordnerarten: Ordner und Tagebuch | `drawing` wird später eine eigene, unveränderliche Inhaltsart. Liste und Pinnwand dürfen Ansichten desselben Aufgabenbestands sein. Andere Typen werden nicht pauschal konvertierbar. |
| Tagebuch | Darf Listen, Notizen, Zeichnungen, Pinnwände und künftige Formate enthalten | Sortierung nach Momentdatum sowie Tages- und Zeitraumssuche müssen typübergreifend funktionieren. Tagebuch und normaler Ordner bleiben unveränderliche Ordnerarten. |
| Fläche | 128 × 128 logische Zellen | Bildschirmgröße und Zoom verändern niemals die gespeicherten Koordinaten. Ein logischer Pixel ist kein Displaypixel. |
| Hintergrund | Deckend weiß | Weiß dient zugleich zum Zurücksetzen. Transparenz und eigener Radierer gehören nicht zu V1. |
| Werkzeuge | Pinsel, 4er-Füllung, Pipette | Gerade, Rechteck, Auswahl, Text und Vektorobjekte gehören nicht zum V1-Kern. |
| Pinsel | 1 × 1, 2 × 2, 4 × 4 und 8 × 8 | Eine Zelle zählt ab mindestens einem Drittel geometrischer Überdeckung. |
| Undo | Letzte 20 Zellfarbänderungen | Keine Zusammenfassung eines Strichs zu einer einzigen Undo-Aktion. Automatische Nachzeichnung ersetzt das Modell erst nach Vorschau und Bestätigung. |
| Farben | Modell höchstens 256 konkrete sRGB-Farben | Eine spätere app-weite Palette mit eventuell 128 Farben ist ein eigener Vertrag. Der Nachzeichner verwendet höchstens 64 Farben einschließlich Weiß. |
| Ebenen | Eine editierbare Ebene | Eine PNG-Referenz ist eine getrennte, nicht bemalbare Editorhilfe. Keine Effekte oder Mischmodi. |
| Austausch | Internes Zeilen-JSON plus Glide-SVG | PNG-Ausgabe ist nachrangig. Allgemeiner Fremd-SVG-Import ist nicht Teil des engen Glide-Profils. |
| Referenz | Lokales PNG; später als verwalteter Anhang | In der Probe bleibt es nur im Arbeitsspeicher. Produktiv muss es mit Duplizieren, Papierkorb und passenden Backups reisen. |
| Nachzeichner | Wahl zwischen „Nur als Referenz“ und „Nachzeichnen“ | Der Referenzweg verändert das Zeichenmodell nicht. Nachzeichnung wird erst nach einer zweiten Vorschau übernommen. |

## 4. Ausgeführte Schritte und Gründe

| Schritt | Umsetzung | Grund |
|---|---|---|
| 1. Dokumentations- und Wettbewerbsabgleich | Glide nur anhand abgelegter Dokumentation bewertet; Todoist, Notion, Planner, OneNote, Figma/FigJam und Paint über Herstellerquellen verglichen | Bestehende Glide-Funktionen sollten nicht erneut als fehlend geplant werden. |
| 2. Formatentscheidung | Offenes, kanonisches JSON als Bearbeitungsmodell; SVG als sichtbares Austauschformat mit eingebettetem Modell | Reines SVG garantiert bei Fremdbearbeitung keine vollständige Glide-Semantik. Das JSON bleibt die eindeutige Bearbeitungsquelle. |
| 3. Isolierter Kern | `drawing.py` ohne Tk- oder App-Abhängigkeit angelegt | Modell, Speicherung und UI sollen getrennt testbar bleiben. |
| 4. Werkzeuge | Ein-Drittel-Pinsel, interpolierte Mauspfade, iterative 4er-Füllung und Pipettenbasis umgesetzt | Schnelle Mausbewegungen dürfen keine Zelllücken erzeugen; diagonale Flächen dürfen beim Füllen getrennt bleiben. |
| 5. Undo | Ring aus 20 einzelnen Zelländerungen | Entspricht der bestätigten, einfachen Rücknahmeidee. Große Füllungen behalten bewusst nur ihre letzten 20 Zelländerungen. |
| 6. JSON/SVG | Kanonisches `hex8-row-v1`, Modell- und Grafikhash, horizontale Rechteckläufe | Stabile Textdiffs, kleine Dateien, Browserdarstellung und prüfbarer Rückimport. |
| 7. SVG-Härtung | Enges Element- und Attributprofil; aktive und externe Inhalte abgelehnt | SVG ist XML und kann Skripte, Links oder externe Ressourcen enthalten. Glide importiert deshalb nur sein eigenes passives Profil. |
| 8. Tk-Probe | Separates `drawing_prototype.pyw` | Bedienung und Leistung konnten erprobt werden, ohne echte Glide-Daten oder Schema 18 zu verändern. |
| 9. Große PNGs | Starre 128-×-128-Prüfung durch Rahmenvorschau ersetzt | Das 400-×-400-Pikachu-Beispiel war klein, wurde aber allein wegen der exakten Maßprüfung abgewiesen. |
| 10. Zentrierung | Scrollbereich erhält symmetrische Außenränder | Die endliche Fläche soll in breiten und hohen Fenstern nicht links oben kleben. |
| 11. Erster Strich | `FocusOut` vom Hauptfenster auf die Zeichenfläche begrenzt | `focus_set()` beim ersten Ansetzen löste zuvor einen allgemeinen Fokusverlust aus und brach den Strich nach dem ersten Punkt ab. |
| 12. Farben | HSV-Spektrum, Helligkeit und flexible Normalisierung | Nicht jede Texteingabe war gültiges `#RRGGBB`; Fehler wirkten zuvor wie „Farbe existiert nicht“ und verhinderten das Zeichnen ohne klare Hilfe. |
| 13. Nachzeichner | 64-Farben-Median-Cut, Weißtoleranz und Vorschau | Referenzen sollen wahlweise nur sichtbar oder in ein editierbares Zellmodell überführt werden. |
| 14. Konturerhalt | 4 × 4 Teilflächen je Zielzelle; ab 6 dunklen Treffern wird die Konturfarbe verwendet | Eine reine Mittelpunktprobe konnte eine ausreichend breite, seitlich liegende Kontur übersehen. Sechs von 16 Treffern erfüllen mindestens ein Drittel Abdeckung. |
| 15. Rastervorschau | Aus, jede Zelle oder 8er-Gruppen | Die Wirkung der 128er-Zellstruktur muss vor dem Ersetzen einer Zeichnung beurteilt werden können. |
| 16. Dokumentation und QA | Changelog, Index, Fachbericht, Tests und archivierte Vorstände ergänzt | Jeder Stand soll nachvollziehbar und ohne Rückgriff auf Chatverlauf übernehmbar sein. |

## 5. Implementierungsstruktur

### `src/glide/drawing.py`

UI-unabhängiger Vertrag:

- `FORMAT_NAME = "glide.drawing"`;
- `FORMAT_VERSION = 1`;
- `ENCODING = "hex8-row-v1"`;
- 128 × 128 Zellen, also 16.384 Werte;
- Palette mit Weiß an Index 0 und höchstens 256 eindeutigen `#RRGGBB`-Werten;
- exakt 128 Hexzeilen mit je 256 Großbuchstaben-Hexzeichen;
- Pinselgrößen 1, 2, 4 und 8;
- Undo-Limit 20;
- JSON-Limit 512 KiB;
- SVG-Limit 4 MiB.

Jede Zelle speichert einen Ein-Byte-Palettenindex. Darum reichen zwei
Hexzeichen je Zelle und darum darf die Palette höchstens 256 Einträge haben.
Zoom, Werkzeug, Rasteranzeige, Scrollposition und Referenzsichtbarkeit sind
Ansichtszustände und gehören nicht in dieses Modell.

Der Pinsel berechnet die geometrische Überdeckung jeder berührten Zelle und
übernimmt sie ab `1/3`. Zwischen zwei Mausereignissen werden pro
zurückgelegter logischer Zelle acht Zwischenpositionen berechnet. Dadurch
bleibt die Spur auch bei schnellen Mausbewegungen zusammenhängend. Die
Füllung arbeitet iterativ mit einer Warteschlange und ausschließlich mit
linkem, rechtem, oberem und unterem Nachbarn; diagonale Berührung verbindet
keine Flächen.

### `src/glide/drawing_prototype.pyw`

Eigenständige Tk-Oberfläche. Sie kennt weder `ListApp` noch `GLIDE_DATA_DIR`
noch `liste_speicher.json`. Hauptbereiche:

- flexible Farbeingabe und Farbspektrum;
- Rahmenberechnung für PNG;
- konturbewusste Nachzeichnungsabtastung;
- 64-Farben-Verdichtung;
- Rahmen-, Nachzeichnungs- und Haupteditor-Dialoge;
- Canvas-Rendering, Zentrierung, Zoom und Raster;
- explizite JSON-/SVG-Dateidialoge.

Start im Repository:

```text
python3 src/glide/drawing_prototype.pyw
```

### Tests

- `tests/integration/test_drawing.py`: Modell, Pinselgeometrie, schnelle
  Pfade, 4er-Füllung, 20-Zell-Undo, JSON, SVG-Rundlauf und verbotene Inhalte.
- `tests/integration/test_drawing_prototype.py`: Farbnormalisierung,
  Bildrahmung, Konturerhalt außerhalb der Mittelpunktprobe, 64-Farben-Grenze,
  Weißhintergrund, Zentrierung, erster Strich sowie getrennte Referenz- und
  Nachzeichnungswege.
- Beide sind als eigene Suiten in `tests/tools/pruefen.py` eingebunden. Der
  Prüfstand umfasst dadurch 34 Suiten.

## 6. Bedienablauf der Probe

### Zeichnen

1. Pinsel, Füllung oder Pipette wählen.
2. Beim Pinsel 1 × 1, 2 × 2, 4 × 4 oder 8 × 8 wählen.
3. Farbe über „Farbspektrum…“ oder Texteingabe setzen.
4. Gültig sind `#RGB`, `RGB`, `#RRGGBB`, `RRGGBB` und von Tk bekannte
   Farbnamen. Intern wird immer `#RRGGBB` gespeichert.
5. Ungültige Farben verändern keine Zelle und erzeugen eine Statusmeldung.
6. Rasteranzeige und Zoom verändern die Zeichnungsdaten nicht.

### PNG laden und rahmen

1. „PNG-Referenz laden“ wählen.
2. Zulässig sind lokale PNGs bis 32 MiB und höchstens 4096 × 4096 Pixel.
3. Zwischen „Fläche füllen (Zuschneiden)“ und „Ganzes Bild zeigen“ wählen.
4. Größe zwischen 25 und 400 Prozent einstellen.
5. Bild horizontal und vertikal um jeweils bis zu 128 logische Zellen
   verschieben.
6. Danach entweder „Nur als Referenz“ oder „Nachzeichnen…“ wählen.

### Nur als Referenz

- Das gerahmte Bild liegt hinter der Zeichnung.
- Weiße Modellzellen lassen die Referenz sichtbar.
- Die Pipette kann Referenzfarben aufnehmen.
- Das Zeichenmodell bleibt unverändert; dieser Umstand ist automatisiert
  geprüft.
- Die Referenz ist in der Probe flüchtig und wird nicht in JSON oder SVG
  geschrieben.

### Nachzeichnen

1. Die Rahmeneinstellungen werden auf eine konturbewusste Abtastung angewandt.
2. Jede Zielzelle erhält 16 Teilproben.
3. Sind mindestens sechs Proben dunkel, wird die dunkle Kontur repräsentiert.
4. Sonst wird die mittlere Zellfarbe verwendet.
5. Nahezu weiße Farben werden nach einstellbarer RGB-Schwelle Hintergrund.
6. Ein gewichteter Median-Cut verdichtet auf höchstens 63 Nichtweißfarben;
   Weiß bleibt Palettenindex 0. Damit gibt es höchstens 64 Farben insgesamt.
7. Die Vorschau bietet Raster aus, jede Zelle oder 8er-Gruppen.
8. Bei vorhandenem Inhalt erscheint ein Hinweis, dass die Übernahme die
   Zeichnung ersetzt.
9. Erst „Nachzeichnung übernehmen“ ersetzt das Modell. Anschließend ist das
   Ergebnis mit Pinsel, Füllung und Pipette normal bearbeitbar sowie als JSON
   oder SVG exportierbar.

Die Weißtoleranz ist in der UI von 220 bis 255 einstellbar und startet bei
245. Ein Bildpunkt wird Hintergrund, wenn Rot, Grün und Blau jeweils
mindestens diesen Wert erreichen. Eine Teilprobe gilt bei einer gewichteten
Helligkeit von höchstens 96 als dunkel. Diese beiden Konstanten sind
Prototypentscheidungen und müssen bei einer späteren Produktoption versioniert
oder weiterhin nur als Importparameter behandelt werden; sie gehören nicht in
das gespeicherte Zellmodell.

## 7. JSON- und SVG-Vertrag

JSON ist die kanonische Bearbeitungsform. Pflichtfelder sind Format,
Formatversion, Maße, Farbraum, Palettenkennung, Palettenversion, Palette,
Codierung und Zeilen. Unbekannte Pflichtfelder, doppelte JSON-Schlüssel,
falsche Maße, falsche Zeilenlängen und ungültige Palettenindizes werden
abgelehnt.

Das SVG bleibt normales SVG 1.1 mit `viewBox="0 0 128 128"`, weißem Hintergrund
und horizontal maximal zusammengefassten Rechtecken. Unter `metadata` liegt
das vollständige JSON-Modell im Namensraum `urn:glide:drawing:1`. Das Manifest
enthält SHA-256 für Modell und sichtbare Grafik.

Importregeln:

- unverändertes eigenes SVG wird verlustfrei geladen;
- nur im Modell geänderte Daten dürfen nach Warnung die sichtbare Vorschau neu
  erzeugen;
- nur sichtbare Grafik geändert: Ablehnung;
- widersprüchlich geändertes Modell und Grafik: Ablehnung;
- Skript, Eventattribute, Links, externe Ressourcen, `foreignObject`, CSS,
  Pfade, Transformationen, Filter, Masken, Animationen, DOCTYPE, ENTITY,
  CDATA, Kommentare und unbekannte Elemente: Ablehnung.

Technische Abbruchgrenzen des Profils:

| Grenze | Wert |
|---|---:|
| JSON-Datei beziehungsweise eingebettetes Modell | 512 KiB |
| SVG-Datei | 4 MiB |
| XML-Elemente | 4096 |
| XML-Tiefe | 8 |
| Attributname | 80 Zeichen |
| Attributwert | 512 Zeichen |
| Titel | 200 Zeichen |
| Beschreibung | 300 Zeichen |

Ein Browser, Illustrator oder Affinity kann die sichtbare SVG-Grafik öffnen.
Ein Fremdprogramm darf Metadaten oder die genaue Rechteckstruktur verändern;
dann ist der verlustfreie Glide-Rückimport nicht garantiert. Allgemeines SVG
wird nicht als angeblich verlustfreies Glide-SVG behandelt.

## 8. Geprüfte Anwenderdateien

### `Test.json` und `Test.svg`

Beide Dateien wurden mit dem implementierten Importer gelesen:

- identisches vollständiges 128-×-128-Modell;
- Palette `[#FFFFFF, #000000]`;
- 757 nichtweiße Zellen;
- Dateigrößen: JSON 33.367 Byte, SVG 52.619 Byte;
- identischer Modellhash
  `b09580b9b76685cb1081b8167284c86629aa598ca078d6d5c85fe4a2b85d3462`;
- SVG-Grafikhash
  `128f5f8f5af6d0444c4ddb802d672350f67f1a97a3d8d57f0f7d43e1cf793a9b`;
- SVG mit 321 zusammengefassten Rechteckläufen;
- keine Reparatur und keine Importwarnung;
- JSON bereits kanonisch.

Die Dateien lagen während der Prüfung unter `/Users/shaye/Downloads/`. Sie
sind Benutzeraustauschdateien und wurden nicht in den Repository-Bestand
kopiert.

### `pikachu.png`

- Quelle: 400 × 400 Pixel, 14.935 Byte;
- wird nach Aufhebung der alten Exaktmaßprüfung akzeptiert;
- Nachzeichnung verwendet 64 Farben einschließlich Weiß;
- konturbewusste Abtastung plus Farbverdichtung benötigten lokal etwa 0,7 s;
- visuell geprüfte 4×-Vorschau:
  `tests/qa-3.28.0/nach_nachzeichner_2026-09-24/pikachu_nachzeichnung_4x.png`.

## 9. Behobene Probleme

| Problem | Ursache | Korrektur | Regression |
|---|---|---|---|
| Erstes Ziehen erzeugte nur einen Punkt | Allgemeines `root`-`FocusOut` brach den Strich ab, als die Canvas beim ersten Klick Fokus erhielt | Fokusabbruch nur noch an Canvas binden | Test prüft Bindung, erstes Ansetzen und mehrzellige erste Spur |
| 400-×-400-PNG wurde abgelehnt | Prototyp verlangte exakt 128 × 128 Pixel | Rahmenvorschau mit Fit/Fill, Skalierung und Versatz | Unterschiedliche Seitenverhältnisse und Zielgröße geprüft |
| Fläche klebte links oben | Scrollregion entsprach nur der Bildfläche | Symmetrische Scrollränder bei passender Ansichtsgröße | Erwartete negative Randkoordinaten geprüft |
| Manche Farbe zeichnete nicht | Freitext akzeptierte nur exaktes `#RRGGBB`; Fehler war schwer verständlich | Farbspektrum und Normalisierung mehrerer Eingabeformen | gültige Kurzformen, Namen und ungültiger Wert geprüft |
| Mittelpunktprobe verlor seitliche Kontur | Nur eine Probe pro Zielzelle | 16 Teilproben; Kontur ab sechs dunklen Treffern | künstliche Kontur verfehlt Mittelpunkt und bleibt trotzdem erhalten |
| Referenz und Nachzeichnung konnten verwechselt werden | Nur ein Übernahmepfad war vorgesehen | getrennte Abschlussaktionen und zweite Nachzeichnungsvorschau | Referenz verändert Modell nicht; Nachzeichnung ersetzt es gezielt |
| Dokumentationsindex war im ersten Ausgangslauf rot | neue beziehungsweise vorhandene Dokumente waren nicht vollständig verlinkt | Index fortgeschrieben | spätere Dokumentationsprüfung grün |

## 10. Bekannte Grenzen und Risiken

1. Die PNG-Referenz lebt nur im Arbeitsspeicher. Schließen der Probe verwirft
   sie; JSON und SVG enthalten sie nicht.
2. Die Nachzeichnung ersetzt nach Vorschau das aktuelle Modell. Der normale
   20-Zell-Undo kann eine komplette Nachzeichnung nicht zurücknehmen. Für die
   produktive Integration ist ein eigener Vorher-Snapshot oder eine atomare
   Strukturaktion erforderlich.
3. Der Nachzeichner unterscheidet dunkle Konturen über eine feste
   Helligkeitsschwelle. Bei dunklen Farbflächen kann diese Regel ebenfalls
   deren Farbe bevorzugen. Die Vorschau ist deshalb verpflichtend.
4. Median-Cut erhält höchstens 64 repräsentative Farben, garantiert aber keine
   semantische Markenpalette. Eine app-weite 128-Farben-Palette bleibt offen.
5. Weiß ist Hintergrund und Löschfarbe. Weiß gemalte Inhalte sind daher nicht
   von unbemaltem Hintergrund unterscheidbar; das ist für V1 bewusst so.
6. Das Zell-Undo enthält einzelne Pixeländerungen. Große Füllungen und breite
   Pinsel können mehr als 20 Änderungen erzeugen.
7. PNG-Import ist absichtlich auf 32 MiB und 4096 Pixel je Achse begrenzt, um
   den Tk-Prototyp vor unkontrolliertem Speicherbedarf zu schützen.
8. Allgemeiner Fremd-SVG-Import, Fremd-PNG-zu-Modell ohne Vorschau,
   Handschrift, Touch, Stiftdruck, Texte, Vektorobjekte und mehrere editierbare
   Ebenen sind nicht implementiert.
9. Browserdarstellung wurde lokal sichtbar geprüft. Ein echter Speichern-und-
   Wiederöffnen-Rundlauf in Illustrator und Affinity steht aus.
10. Die visuelle Bedienprüfung ist bisher macOS-zentriert. Windows, DPI,
    Mehrmonitor, Tastaturvollständigkeit und Screenreader bleiben manuell.
11. Der produktive Datenbestand wurde absichtlich nicht geöffnet oder
    verändert. Für die spätere Integration fehlen Migrations- und
    Wiederherstellungstests.

## 11. Prüfergebnisse

### Gezielte Prüfungen des finalen isolierten Stands

```text
python3 tests/integration/test_drawing.py
python3 tests/integration/test_drawing_prototype.py
```

Beide sind grün. Zusätzlich sind Syntax, Versionskonsistenz und
Dokumentationsindex grün.

### Repository-Schnellläufe

| Protokoll | Bedeutung |
|---|---|
| `tests/qa-3.28.0/vor_zeichenflaeche_2026-09-24/ergebnis.json` | Ausgangszustand vor dem Kern; enthält bereits die später wiederkehrenden Altfehler und zusätzlich den damals offenen Dokumentationsindex. |
| `tests/qa-3.28.0/nach_zeichenflaechenkern_2026-09-24/ergebnis.json` | Kern, JSON/SVG und erste Bedienprobe. |
| `tests/qa-3.28.0/nach_referenzrahmen_2026-09-24/ergebnis.json` | große PNGs, Zentrierung, erster Strich und Farbspektrum. |
| `tests/qa-3.28.0/nach_nachzeichner_2026-09-24/ergebnis.json` | Referenz-/Nachzeichnungsablauf und 64-Farben-Vorschau. |

Die Gesamtläufe enden mit Exitcode 1, weil folgende Befunde bereits im
Ausgangszustand vorhanden waren und außerhalb dieser isolierten Änderung
liegen:

- historisches Fixture `glide_releaseplanung_3.26.0.glidebackup` passt nicht
  zur angegebenen Erzeugerversion;
- `test_template_workflows`: Vorlagenerzeuger nicht reproduzierbar;
- `test_features313`, `test_features322`, `test_features328`: ältere
  UI-Erwartungen widersprechen dem aktuellen 3.28-Stand;
- `standpruefung`: sieben überholte oder fehlende Standangaben in älteren
  Dokumenten.

Die sieben Standbefunde sind konkret:

1. `00_Arbeitsvorbereitung/Glide_KI_Austauschformat_und_Zukunftsarchitektur.md`
   nennt Format 17 statt 18;
2. `SECURITY.md` nennt den lesbaren Bereich 4 bis 17 statt 4 bis 18;
3. `docs/06_DATA_BACKUP_MIGRATION.md` nennt denselben alten Bereich;
4. `docs/decisions/PRODUCT_IDENTITY.md` nennt in einer Zeile Format 17;
5. dasselbe Dokument nennt in einer weiteren Zeile 4 und 17 statt 18;
6. `3.25 Änderungen-Prompt/3.25 ursprüngliche Prompt-Formulierung.md`
   besitzt keine erwartete Standangabe;
7. `90_Testdaten_Extern/README.md` nennt den lesbaren Bereich 4 bis 17.

Alle neuen Zeichentests sowie Kern, Datenintegrität, Audit, aktuelle
Funktionssuiten, statische Analyse, Erreichbarkeitsanalyse,
Attributprüfung und Dublettenprüfung sind grün. Der finale Konturfall und die
getrennten Abschlusswege wurden nach dem letzten Gesamtlauf nochmals gezielt
grün ausgeführt.

### Archivkette der Arbeit

Vor jedem größeren Dokumentationsschritt wurden die damaligen Stände erhalten.
Besonders relevant sind:

- `00_Arbeitsvorbereitung/archiv/*vor_Implementierungsbeginn_2026-09-24.md`;
- `docs/archiv/*vor_Referenzrahmen*` und die entsprechenden Archive von
  Changelog und Test-README;
- `docs/archiv/*vor_Nachzeichner*` und die entsprechenden Archive;
- `docs/archiv/00_INDEX_3.28.0_vor_Zeichenflaechenuebergabe_2026-09-24.md`;
- `docs/archiv/09_PROJECT_HANDOFF_3.28.0_vor_Zeichenflaechenuebergabe_2026-09-24.md`;
- `00_Arbeitsvorbereitung/archiv/README_3.28.0_vor_Zeichenflaechenuebergabe_2026-09-24.md`.

Historische Aussagen dürfen bei künftigen Korrekturen nicht still
überschrieben werden. Zuerst erneut archivieren, danach den aktiven Stand
fortschreiben und das neue Archiv im zuständigen Index verlinken.

## 12. Sichere Fortsetzungsreihenfolge

1. Keine direkte UI-Integration beginnen, bevor Datenvertrag und atomare
   Speicherung für `drawing` schriftlich abgeschlossen sind.
2. `list_kind: drawing` als neue, nicht konvertierbare Inhaltsart entwerfen.
   `tasks` bleibt zwischen Liste und Pinnwand umschaltbar.
3. Format-18-Migration mit unveränderter Originalsicherung planen. Erst danach
   die Formatnummer anheben.
4. Zeichnungsmodell im normalen Glide-Bestand speichern; Zoom, Werkzeug,
   Raster und Referenzsichtbarkeit bleiben Ansichtszustände.
5. Automatisches Speichern atomar umsetzen: temporäre Datei, Flush/Fsync nach
   bestehendem Glide-Muster, atomarer Austausch, sichtbarer Fehlerstatus und
   Erhalt des letzten gültigen Stands.
6. Für eine automatische Nachzeichnung einen vollständigen Vorher-Snapshot
   vorsehen. Der 20-Zell-Ring reicht für diese Strukturaktion nicht.
7. PNG als verwalteten lokalen Anhang mit stabiler relativer Referenz
   integrieren. Duplizieren, Papierkorb und Wiederherstellung gemeinsam testen.
8. Voll- und passendes Teilbackup um Zeichnung und Referenz erweitern;
   Wiederherstellung in leerem isolierten Datenordner prüfen.
9. Navigation, Suche, Vorlagen, Tagebuchdatum und Pinnwandvorschau ergänzen.
10. Erst anschließend Plattform-, Leistungs-, Tastatur- und
    Barrierefreiheitsabnahme durchführen.
11. App-Version und Aufgabenformat nur mit Migration, Referenz-Fixture,
    Changelog, Dokumentenstand und Releaseprüfung erhöhen.

## 13. Abnahmekriterien für die nächste Stufe

- bestehende Aufgaben, Notizen, Tagebücher und Pinnwände bleiben byte- und
  funktionsseitig erhalten;
- eine Zeichnung bleibt nach bestätigtem Autosave und Neustart identisch;
- ein Schreibfehler überschreibt keinen letzten gültigen Stand;
- JSON- und eigenes SVG erhalten alle unterstützten Daten im Rundlauf;
- Referenz-PNG und Verweis überstehen Duplizieren, Papierkorb, Vollbackup,
  passendes Teilbackup und Wiederherstellung;
- fehlerhafte, übergroße oder unbekannte Dateien verändern keinen Bestand;
- SVG lädt keine externen Ressourcen und führt keine aktiven Inhalte aus;
- Zoom und Display-Skalierung treffen dieselben logischen Zellen;
- Nachzeichnung kann vor Übernahme verworfen und nach Übernahme vollständig
  über einen gesonderten Vorher-Snapshot zurückgesetzt werden;
- Tagebuchordner sortieren gemischte Inhalte nach Datum und können nach Tag
  beziehungsweise Zeitraum suchen;
- manuelle Abnahme nennt Plattformen und Messergebnisse, statt „absolut
  zuverlässig“ ohne Beleg zu behaupten.

## 14. Kurzanweisung für den übernehmenden Agenten

```text
Arbeite im Repository 01_Repository/Glide und lies zuerst AGENTS.md sowie
`docs/62_ZEICHENFLAECHE_WEITERGABE_2026-09-24.md`. Der isolierte Zeichenkern
und die Tk-Probe sind vorhanden; integriere sie nicht unbesehen in ListApp.
Bewahre Glide 3.28.0 und Aufgabenformat 18, bis ein eigener, gesicherter
Migrationsauftrag vorliegt. Führe vor Änderungen den Prüfstand mit isoliertem
GLIDE_DATA_DIR aus und archiviere jedes zu ändernde Dokument. Behandle
`drawing` als nicht konvertierbare Inhaltsart, während `tasks` zwischen Liste
und Pinnwand umschaltbar bleibt. Plane zuerst Datenvertrag, atomare Speicherung,
Nachzeichnungs-Snapshot, Anhangspfad und Backup-Wiederherstellung. Die bekannten
roten Altbefunde stehen in Abschnitt 11 und dürfen weder als neue Regression
noch als bestanden ausgegeben werden. Nach jeder Änderung müssen mindestens
`test_drawing.py`, `test_drawing_prototype.py`, Versionskonsistenz und
Dokumentationsindex grün sein.
```

## 15. Dateikarte

| Datei | Rolle |
|---|---|
| `src/glide/drawing.py` | kanonischer, UI-unabhängiger Zeichenvertrag |
| `src/glide/drawing_prototype.pyw` | isolierte Tk-Bedienprobe |
| `tests/integration/test_drawing.py` | Modell-, Austausch- und SVG-Sicherheitstest |
| `tests/integration/test_drawing_prototype.py` | UI-, Referenz- und Nachzeichnerregression |
| `tests/tools/pruefen.py` | zentraler Glide-Prüflauf mit 34 Suiten |
| `docs/61_ZEICHENFLAECHE_ISOLIERTER_KERN_2026-09-24.md` | technische Implementierungsdokumentation |
| `docs/62_ZEICHENFLAECHE_WEITERGABE_2026-09-24.md` | diese kanonische Übergabe |
| `00_Arbeitsvorbereitung/Glide_Funktionsvergleich_und_Zeichenflaeche_2026-09-23.md` | Recherche und Wettbewerbsvergleich |
| `00_Arbeitsvorbereitung/Glide_SVG_und_Zeichnungsdaten_Untersuchung_2026-09-23.md` | SVG-, Speicher- und Integrationsentscheidung |
| `00_Arbeitsvorbereitung/Glide_Aufgabensammlung_Zeichenflaeche_2026-09-23.md` | priorisierte Arbeitspakete und Abnahmekriterien |
| `tests/qa-3.28.0/nach_nachzeichner_2026-09-24/` | jüngstes Gesamtprotokoll und visuelle Nachzeichnerprobe |

## 16. Abschlusskontrolle dieser Dokumentation

Die Weitergabe wurde nach ihrer Verlinkung automatisiert geprüft:

- Versionskonsistenz: Glide 3.28.0 und Aufgabenformat 18 konsistent;
- Dokumentationsindex: alle aktiven und archivierten Repository-Dokumente
  verzeichnet, 842 lokale Markdown-Dateilinks geprüft;
- Inhaltsmatrix: Produktentscheidungen, Umsetzung und Gründe, behobene und
  offene Probleme, JSON/SVG, Referenz und Nachzeichner, Prüfbelege,
  Fortsetzungsreihenfolge und Agentenanweisung vorhanden;
- Standprüfung: kein neuer Befund durch diese Weitergabe; dieselben sieben in
  Abschnitt 11 dokumentierten Altbefunde bleiben offen.

Damit ist der Zeichenflächenstand ohne den Chatverlauf rekonstruierbar. Die
noch offenen Punkte sind bewusst als offen benannt und nicht als umgesetzt
oder freigegeben dargestellt.
