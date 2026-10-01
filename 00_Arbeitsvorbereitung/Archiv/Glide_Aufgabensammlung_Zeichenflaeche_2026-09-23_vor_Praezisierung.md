# Glide – Aufgabensammlung Pixel-Zeichenfläche

Stand 23.09.2026 · Planungsstand · Grundlage: Glide 3.28.0 · Aufgabenformat 18

> **Gesamtstatus: geplant, nicht umgesetzt.** Diese Sammlung ist eine
> umsetzbare Entwicklungsplanung. Kein Punkt in diesem Dokument belegt eine
> vorhandene Zeichenfunktion, eine erfolgte Datenmigration oder eine
> Plattformfreigabe.

Fachliche Grundlage ist der
[Funktionsvergleich und das Zeichenflächenkonzept](Glide_Funktionsvergleich_und_Zeichenflaeche_2026-09-23.md).
Die Reihenfolge richtet sich nach Datenintegrität und Abhängigkeiten, nicht nach
der Sichtbarkeit einer Funktion.

## 1. Festgelegter Zielumfang

- Neue Seitenart `drawing` neben Aufgaben- und Notizseiten.
- Pixel zuerst, begrenzte Bildfläche, Standard 128 × 128 Zellen;
  Startvorgaben 64 × 64 und 256 × 256.
- Einfache Pixelebenen mit Reihenfolge, Sichtbarkeit und Sperre.
- Pixelstift, Radierer, Füllen, Pipette, Linie, Rechteck und
  Rechteckauswahl.
- Vollständig bearbeitbarer Rundlauf eigener JSON- und Glide-SVG-Dateien.
- PNG als Bildausgabe ohne Zusage einer editierbaren Ebenenstruktur.
- Lokale, atomare Speicherung; Backup, Migration, Duplizieren, Papierkorb und
  Wiederherstellung folgen den bestehenden Glide-Grundsätzen.
- Keine Umsetzung in diesem Dokumentationsauftrag.

## 2. Prioritäten, Aufwand und Abhängigkeiten

| Kennung | Priorität | Arbeitspaket | Aufwand | Abhängigkeiten | Status |
|---|---|---|---|---|---|
| ZF-000 | P0 | Dokumentationsstand konsolidieren | S | keine | geplant, nicht umgesetzt |
| ZF-010 | P0 | Zeichenmodell und Formatvertrag | M | ZF-000 | geplant, nicht umgesetzt |
| ZF-020 | P0 | Speicher- und Wiederherstellungsvertrag | M | ZF-010 | geplant, nicht umgesetzt |
| ZF-030 | P0 | Eingabe-, Transaktions- und Undo-Vertrag | M | ZF-010 | geplant, nicht umgesetzt |
| ZF-040 | P1 | Isolierter Modell- und Leistungsprototyp | L | ZF-010, ZF-030 | geplant, nicht umgesetzt |
| ZF-050 | P1 | JSON-Import und -Export | M | ZF-010, ZF-020 | geplant, nicht umgesetzt |
| ZF-060 | P1 | Glide-SVG und PNG | L | ZF-010, ZF-050 | geplant, nicht umgesetzt |
| ZF-070 | P1 | Editor-Bedienung und Barrierefreiheit | L | ZF-030, ZF-040 | geplant, nicht umgesetzt |
| ZF-080 | P1 | Integration als Glide-Seitenart | XL | ZF-020, ZF-040, ZF-070 | geplant, nicht umgesetzt |
| ZF-090 | P1 | Backup, Migration und Wiederherstellung | L | ZF-050, ZF-080 | geplant, nicht umgesetzt |
| ZF-100 | P2 | Pinnwand-Referenz und Vorschau | M | ZF-080, ZF-090 | geplant, nicht umgesetzt |
| ZF-110 | P2 | Dokumentation, Vorlagen und Releaseprüfung | M | ZF-080, ZF-090, ZF-100 | geplant, nicht umgesetzt |
| ZF-200 | P2 | Weitere belegte Plattformverbesserungen | mehrere | unabhängig | geplant, nicht umgesetzt |
| ZF-300 | P3 | Erweiterte Zeichenfunktionen bewerten | mehrere | stabile erste Stufe | geplant, nicht umgesetzt |

Aufwandklassen: **S** = klein, **M** = mittel, **L** = groß, **XL** = sehr
groß. Sie dienen der Reihenfolge und sind keine Zeitschätzung.

## 3. P0 – Verträge vor Implementierung

### ZF-000 – Dokumentationsstand konsolidieren

**Status:** geplant, nicht umgesetzt  
**Ziel:** Eine widerspruchsfreie Grundlage schaffen, bevor Schema oder UI
geändert werden.  
**Nutzen:** Verhindert doppelte Arbeit an bereits vorhandenen Funktionen und
falsche Annahmen über Backup oder Rich-Text.  
**Aufwand:** S  
**Abhängigkeiten:** keine

**Umfang**

- Den allgemeinen Produktvertrag an Notizlisten, Tagebuch und aktuelle
  Pinnwandtransporte angleichen.
- Historische Aussagen zu fehlendem Zoom, Navigator, Rich-Text und
  Pinnwandtransport als überholt markieren, ohne historische Dokumente
  rückwirkend umzuschreiben.
- Die Begriffe Aufgabenboard, Pinnwand, Notizseite und Zeichenfläche im
  Dokumentationsindex eindeutig abgrenzen.
- „Dokumentiert vorhanden“ und „vollständig releasefreigegeben“ konsequent
  getrennt halten.

**Abnahmekriterien**

1. Kein aktuelles Einstiegsdokument behauptet mehr, Rich-Text sei generell
   ausgeschlossen oder Pinnwände reisten nie in Backups.
2. Zoom, Navigator, Lasso und Snap werden nicht mehr als neue
   Zeichenflächenaufgaben geführt, sondern als wiederverwendbare Bedienideen.
3. Alle geänderten aktuellen Dokumente besitzen gemäß Repository-Regel eine
   nachvollziehbare Archivfassung.

**Quellen:** lokale Produktgrenzen, Datenvertrag, Pinnwandvertrag 3.24,
Entscheidungen 3.26, Tagebuchvertrag 3.28 und QA-Bericht 3.28.

### ZF-010 – Zeichenmodell und Formatvertrag

**Status:** geplant, nicht umgesetzt  
**Ziel:** Das vollständige, UI-unabhängige Modell `glide.drawing` Version 1
festlegen.  
**Nutzen:** Bearbeitbarkeit und Zukunftsfähigkeit hängen nicht von Tk,
Bildschirmauflösung oder einem Exportformat ab.  
**Aufwand:** M  
**Abhängigkeiten:** ZF-000

**Umfang**

- Dokumentfelder für Formatkennung, Version, Breite, Höhe, Farbraum,
  Palette und Ebenen festlegen.
- Zellkoordinaten ganzzahlig und nullbasiert definieren; transparent bedeutet
  fehlende Zelle, nicht eine besondere Hintergrundfarbe.
- Ebene mit stabiler Kennung, Name, Sichtbarkeit, Sperre und Zellmenge
  definieren.
- Normalisierung und kanonische Schreibreihenfolge festlegen, damit ein
  Export-Import-Export ohne inhaltliche Änderung stabil vergleichbar ist.
- Harte Grenzen festlegen: Bildmaße, Ebenen, Palette, belegte Zellen,
  Dateigröße, Textlängen und Verschachtelung.
- Verhalten für unbekannte optionale und unbekannte verpflichtende Felder
  definieren.
- Beispiel für leeres, kleines und mehrschichtiges Dokument liefern.

**Abnahmekriterien**

1. Der Vertrag kann ein 128-×-128-Bild mit Transparenz und mehreren Ebenen
   ohne Kenntnis der UI vollständig beschreiben.
2. Zwei Implementierungen könnten anhand des Dokuments denselben kanonischen
   JSON-Inhalt erzeugen.
3. Ungültige Farben, Koordinaten außerhalb der Fläche, doppelte
   Ebenenkennungen und Grenzüberschreitungen haben jeweils eine eindeutige
   Fehlerfolge.
4. Zoom, Pan, Navigator, Rasteranzeige und aktives Werkzeug sind ausdrücklich
   kein Bestandteil des fachlichen Bildmodells.

**Quellen:** Glide-Austauschformat 1, Datenvertrag Format 17/18,
[W3C-SVG-Erweiterbarkeit](https://www.w3.org/TR/SVG11/extend.html).

### ZF-020 – Speicher- und Wiederherstellungsvertrag

**Status:** geplant, nicht umgesetzt  
**Ziel:** Verlustarme Speicherung bei normaler Nutzung, Schreibfehlern und
Programmneustart verbindlich definieren.  
**Nutzen:** „Gespeichert“ wird eine prüfbare Zusage und kein bloßer UI-Zustand.  
**Aufwand:** M  
**Abhängigkeiten:** ZF-010

**Umfang**

- Autosave-Bündelung, erzwungenes Flush vor Navigation, Export, Backup und
  Programmende definieren.
- Schreiben über temporäre Datei, Validierung und atomaren Ersatz planen;
  der letzte gültige Stand bleibt bis zum erfolgreichen Ersatz erhalten.
- Zustände `ungespeichert`, `speichert`, `gespeichert` und `Fehler` samt
  zugänglicher Statusmeldung definieren.
- Wiederanlauf nach Prozessabbruch sowie Umgang mit verwaisten temporären
  Dateien festlegen.
- Entscheiden und dokumentieren, dass die fachliche Zeichnung lokal dauerhaft
  ist und keine Synchronisierung benötigt.
- Maximale Autosave-Verzögerung und Obergrenze für im Speicher gehaltene
  Änderungen nach dem Prototyp festschreiben.

**Abnahmekriterien**

1. Nach angezeigtem Zustand `gespeichert` enthält ein Neustart ohne Netzwerk
   exakt den bestätigten Inhalt.
2. Ein simulierter Fehler vor dem atomaren Ersatz beschädigt den vorherigen
   Stand nicht.
3. Seitenwechsel, Backup und Programmende warten auf ein ausstehendes Save
   oder melden nachvollziehbar, warum sie nicht fortfahren.
4. Ein Speicherfehler bleibt sichtbar; weitere Bearbeitung vernichtet weder
   den letzten gültigen Stand noch die ungespeicherten Änderungen still.

**Quellen:** Glide-Daten- und Migrationsvertrag; als Vergleich die offizielle
[Todoist-Offlinedokumentation](https://www.todoist.com/help/todoist/features/use-todoist-while-offline-4rbaZw).

### ZF-030 – Eingabe-, Transaktions- und Undo-Vertrag

**Status:** geplant, nicht umgesetzt  
**Ziel:** Jede Benutzerhandlung besitzt einen eindeutigen Anfang, Abschluss,
Abbruch und Undo-Schritt.  
**Nutzen:** Verhindert Lücken, hängende Werkzeuge und schwer erklärbare
Teiländerungen.  
**Aufwand:** M  
**Abhängigkeiten:** ZF-010

**Umfang**

- Zustandsautomaten für Strich, Linie, Rechteck, Auswahl und Verschieben
  spezifizieren.
- Schnelle Bewegungen durch Zellinterpolation zwischen zwei erfassten
  logischen Positionen schließen.
- Ein Strich, eine Füllung, eine Form, eine Auswahlstransformation und eine
  Ebenenaktion jeweils als eine Transaktion festlegen.
- `Escape`, Fokusverlust, Fensterwechsel und Loslassen außerhalb der Fläche
  einheitlich behandeln.
- Redo-Zweig nach neuer Bearbeitung und Umgang mit speicherintensiven
  Füllungen festlegen.
- Entscheidung über Undo nach Neustart vorbereiten; V1 darf den Undo-Stapel
  beim Neustart bewusst beenden, wenn dieser Zustand sichtbar dokumentiert ist.

**Abnahmekriterien**

1. Ein schneller diagonaler Strich enthält keine unbeabsichtigten Lücken.
2. Ein Undo entfernt genau den letzten zusammenhängenden Strich und nicht nur
   dessen letzten Bewegungspunkt.
3. Abgebrochene Vorschauen ändern das Modell und den Speicherstand nicht.
4. Fokusverlust und Loslassen außerhalb hinterlassen keinen aktiven
   Dauerzustand.
5. Undo/Redo stellt Pixel, Ebenenreihenfolge, Sichtbarkeit und Sperre exakt
   wieder her.

**Quellen:** bestehende Glide-Mutationswege und die im Konzept ausgewerteten
Bedienmuster von Paint, OneNote und Figma.

## 4. P1 – Isolierte Entwicklung und Austausch

### ZF-040 – Isolierter Modell- und Leistungsprototyp

**Status:** geplant, nicht umgesetzt  
**Ziel:** Modell, Rendering und Eingabeverhalten außerhalb des produktiven
App-Flusses messen, bevor das Hauptdatenformat geändert wird.  
**Nutzen:** Technische Risiken werden sichtbar, ohne bestehende Nutzerdaten zu
berühren.  
**Aufwand:** L  
**Abhängigkeiten:** ZF-010, ZF-030

**Umfang**

- Reines Zeichenmodell ohne Tk-Abhängigkeit implementieren und testen.
- Mindestens bildbasierte, gekachelte und selektiv aktualisierte Darstellung
  für 64 × 64, 128 × 128 und 256 × 256 vergleichen.
- Zoom, Pan, sichtbares Raster und Koordinatenabbildung isoliert erproben.
- Leistung bei Strichen, großer Füllung, Ebenenwechsel, Undo/Redo und
  Vollrendering messen.
- Abbruchschwellen und Renderstrategie dokumentieren. Keine neue Abhängigkeit
  allein aus Bequemlichkeit einführen.

**Abnahmekriterien**

1. Der Prototyp verwendet ausschließlich einen temporären, isolierten
   Datenordner und kann keinen echten Glide-Bestand öffnen.
2. Dieselbe Modellkoordinate wird bei allen geprüften Zoomstufen und
   Display-Skalierungen getroffen.
3. 256 × 256 Zellen mit mehreren Ebenen bleiben innerhalb vorher definierter
   Reaktionsziele; Messwerte und Testrechner werden dokumentiert.
4. Die gewählte Renderstrategie ist austauschbar, ohne den Formatvertrag zu
   ändern.

### ZF-050 – JSON-Import und -Export

**Status:** geplant, nicht umgesetzt  
**Ziel:** Verlustfreier Text-Rundlauf des kanonischen Zeichenmodells.  
**Nutzen:** Zukunftssichere, offene und prüfbare Bearbeitbarkeit.  
**Aufwand:** M  
**Abhängigkeiten:** ZF-010, ZF-020

**Umfang**

- Dateiimport und Einfügen aus Text auf denselben Parser und dieselbe
  Validierung führen.
- Importvorschau mit Maßen, Ebenen, belegten Zellen, Farben, Warnungen und
  unbekannten Angaben bereitstellen.
- Import standardmäßig als neue Zeichnung; Ersetzen einer offenen Zeichnung
  nur als ausdrückliche Aktion mit Sicherung.
- Kanonischen Export mit stabiler Feld- und Ebenenreihenfolge erzeugen.
- Den gesamten Import als einen Undo-Schritt behandeln, sofern er innerhalb
  eines bestehenden Dokuments erfolgt.

**Abnahmekriterien**

1. Export → Import → Export ergibt semantisch und kanonisch denselben
   Zeicheninhalt.
2. Beschädigte, übergroße oder unbekannte Pflichtangaben verändern keinen
   vorhandenen Bestand.
3. Dateiimport und Textimport melden dieselben Fehler an denselben Feldern.
4. Umlaute, Zeichen außerhalb der BMP und Ebenennamen bleiben erhalten.

### ZF-060 – Glide-SVG und PNG

**Status:** geplant, nicht umgesetzt  
**Ziel:** Sichtbare Standardausgabe und kontrollierter Rückimport eigener SVGs.  
**Nutzen:** Zeichnungen lassen sich außerhalb von Glide verwenden, ohne den
Glide-Rundlauf eigener Dateien aufzugeben.  
**Aufwand:** L  
**Abhängigkeiten:** ZF-010, ZF-050

**Umfang**

- SVG aus sichtbaren Pixelebenen erzeugen; zusammenhängende gleichfarbige
  Bereiche dürfen zur Dateigröße zusammengefasst werden, solange die
  Darstellung zellgenau bleibt.
- Vollständiges JSON-Modell, Formatversion und Prüfsumme in `metadata`
  einbetten.
- Eigenes SVG-Profil definieren und nur dieses als verlustfrei reimportierbar
  zusagen.
- Abweichungen zwischen Metadaten und sichtbarer SVG-Darstellung erkennen und
  als Konflikt behandeln.
- Strikten Parser ohne Skriptausführung, Netzwerk, externe Ressourcen,
  Entitätserweiterung oder `foreignObject` festlegen.
- PNG mit wählbarer Skalierung und Transparenz exportieren; PNG-Import als
  flache Ebene kennzeichnen.

**Abnahmekriterien**

1. Eigenes Glide-SVG durchläuft Export → Import → Export ohne Verlust von
   Zellen, Farben, Ebenenreihenfolge, Sichtbarkeit oder Sperre.
2. Ein SVG ohne Glide-Metadaten wird niemals als garantiert vollständig
   bearbeitbares Projekt bezeichnet.
3. SVG mit Skript, externen Referenzen, übergroßer Struktur oder verbotenen
   Elementen wird vor jeder Modelländerung abgewiesen.
4. PNG entspricht der sichtbaren Komposition bei 1× und ganzzahligen
   Skalierungen pixelgenau.

**Quellen:** [W3C: SVG-Erweiterbarkeit](https://www.w3.org/TR/SVG11/extend.html),
[Python: XML-Sicherheit](https://docs.python.org/3/library/xml.html),
[Figma: SVG-Austausch](https://help.figma.com/hc/en-us/articles/360040030374-Copy-assets-between-design-tools).

### ZF-070 – Editor-Bedienung und Barrierefreiheit

**Status:** geplant, nicht umgesetzt  
**Ziel:** Zuverlässige Bedienung mit Maus und Tastatur in breiten und schmalen
Fenstern.  
**Nutzen:** Die Zeichenfläche bleibt im Unternehmensalltag auffindbar und
beherrschbar.  
**Aufwand:** L  
**Abhängigkeiten:** ZF-030, ZF-040

**Umfang**

- Werkzeugleiste mit sichtbarem aktivem Werkzeug, Vorderfarbe, aktiver Ebene,
  Zoom und Speicherstatus planen.
- Seltene Aktionen in ein beschriftetes Menü verschieben; Kernwerkzeuge
  bleiben direkt erreichbar.
- Tastaturpfade für Werkzeugwechsel, Zoom, Pan, Auswahl, Löschen, Kopieren,
  Einfügen, Undo und Redo definieren.
- Fokusrahmen, Statusmeldungen und Fehlerhinweise ohne alleinige
  Farbcodierung gestalten.
- Verhalten bei schmalen Fenstern, hoher DPI, Mehrmonitorbetrieb und
  horizontalem/vertikalem Scrollen prüfen.
- Maus bildet die erste Eingabestufe. Touch, Stiftdruck und Handschrift bleiben
  außerhalb dieses Pakets.

**Abnahmekriterien**

1. Alle Grundwerkzeuge sind ohne Maus erreichbar und ihr aktiver Zustand ist
   mit Fokus und Screenreader-tauglichem Text erkennbar.
2. Zoom verändert nicht die logische Auswahl oder das Ergebnis eines
   Tastatur-Pixelschritts.
3. Bei Minimalbreite bleiben Zeichenfläche, Speicherstatus und Abschlusswege
   erreichbar.
4. Ein manueller Prüfplan deckt Windows und macOS, DPI, Mehrmonitor,
   Fokuswechsel und Screenreader ab.

## 5. P1 und P2 – Integration in Glide

### ZF-080 – Integration als Glide-Seitenart

**Status:** geplant, nicht umgesetzt  
**Ziel:** Den isoliert bestätigten Editor als dritte Seitenart in den
bestehenden Lebenszyklus integrieren.  
**Nutzen:** Zeichnungen nutzen dieselbe Navigation, Datenhoheit und
Schutzmechanismen wie Aufgaben und Notizen.  
**Aufwand:** XL  
**Abhängigkeiten:** ZF-020, ZF-040, ZF-070

**Umfang**

- `list_kind` beziehungsweise den künftigen Seitentyp um `drawing` erweitern;
  die genaue Schemaform vor Implementierung in einer Datenentscheidung
  festhalten.
- Erstellung aus Neu-Menü, Ordnerkontext und geeigneten Vorlagen anbieten.
- Titel, Beschreibung, Labels, lokale Anhänge und Seitenmetadaten mit
  bestehenden Regeln verbinden.
- Suche indexiert Titel und Metadaten; eine Pixel-Inhaltssuche ist nicht Teil
  der ersten Stufe.
- Duplizieren, Verschieben, Umbenennen, Papierkorb, Wiederherstellen und
  endgültiges Entfernen definieren.
- Wechsel zwischen Aufgaben-, Notiz- und Zeichnungsart nur nach explizitem
  Vertrag; kein stilles Verwerfen eines Zeichnungsdokuments.
- Bestehende Mutations-, Modal- und Speicherpfade verwenden; keine parallele
  zweite Datenbank einführen.

**Abnahmekriterien**

1. Eine Zeichnungsseite lässt sich erstellen, benennen, verschieben,
   duplizieren, löschen und wiederherstellen, ohne Aufgaben oder Notizen zu
   verändern.
2. Navigation mit ungespeicherten Änderungen folgt ZF-020.
3. Alte Format-18-Bestände werden unverändert geladen und erst nach Sicherung
   migriert.
4. Eine ältere Glide-Fassung darf den neuen Bestand nicht unbemerkt
   schreibend verändern.

### ZF-090 – Backup, Migration und Wiederherstellung

**Status:** geplant, nicht umgesetzt  
**Ziel:** Vollständige Portabilität und sichere Schemaanhebung.  
**Nutzen:** Die Zeichenfläche ist kein Sonderbestand, der bei Backup oder
Gerätewechsel verloren geht.  
**Aufwand:** L  
**Abhängigkeiten:** ZF-050, ZF-080

**Umfang**

- Neue Formatnummer, additive Normalisierung und unveränderte Vorsicherung
  nach bestehendem Glide-Muster planen.
- Komplettbackup, Teilbackup eines Ordners/einer Liste, App-Backup und
  Datenordnerkopie um Zeichnungsseiten ergänzen.
- Vollrestore und additives Hinzufügen mit neuen Kennungen prüfen.
- Zeichnungen im Papierkorb, leere Zeichnungen, große Zeichnungen und
  Anhänge abdecken.
- Backupgrenzen und Vorschau um Zeichnungsanzahl, Abmessungen und Gesamtgröße
  erweitern.
- Wiederherstellung in einen leeren, isolierten Datenordner als verpflichtenden
  Release-Test festlegen.

**Abnahmekriterien**

1. Vollbackup → Wiederherstellung in leerem Datenordner erhält Dokumente,
   Ebenen, Zellen, Metadaten, Anhänge und Verknüpfungen.
2. Teilbackup transportiert alle Zeichnungen im gewählten Zweig und keine
   fremden Seiten.
3. Ein beschädigtes Archiv verändert den bestehenden Bestand nicht.
4. Migration scheitert sicher, wenn die unveränderte Vorsicherung nicht
   geschrieben werden kann.
5. Bestehende Aufgaben, Notizen, Tagebücher und Pinnwände sind nach Migration
   byte- beziehungsweise semantisch unverändert, soweit die Normalisierung
   keine dokumentierte Ergänzung verlangt.

### ZF-100 – Pinnwand-Referenz und Vorschau

**Status:** geplant, nicht umgesetzt  
**Ziel:** Eine Zeichnungsseite auf einer Pinnwand zeigen, ohne ihren Inhalt zu
duplizieren.  
**Nutzen:** Visuelle Notizen lassen sich mit Aufgaben und Long-Tasks in einem
Arbeitskontext verbinden.  
**Aufwand:** M  
**Abhängigkeiten:** ZF-080, ZF-090

**Umfang**

- Pinnwandkarte referenziert die stabile Seitenkennung und erzeugt eine
  begrenzte Vorschau aus dem Original.
- Doppelklick beziehungsweise Bearbeiten öffnet die Original-Zeichenfläche;
  Rückkehr erhält den Pinnwandkontext.
- Kartenposition, Kartengröße und Verbindung bleiben
  Pinnwandeinstellungen; Pixel und Ebenen bleiben Seiteninhalt.
- Aktualisierung der Vorschau bündeln und mit Dokumentrevision kennzeichnen,
  damit kein unnötiger Vollrender entsteht.
- Verhalten beim Papierkorb, Wiederherstellen, Löschen und Import mit neuen
  Kennungen festlegen.

**Abnahmekriterien**

1. Bearbeitung der Originalzeichnung aktualisiert alle sichtbaren
   Pinnwandvorschauen, ohne Kopien des Zeichenmodells anzulegen.
2. Entfernen der Karte löscht die Zeichnungsseite nicht; Löschen der Seite
   entfernt oder kennzeichnet alle ungültigen Referenzen nachvollziehbar.
3. Backup und additiver Import ordnen Pinnwandreferenzen auf neue Kennungen um.
4. Eine große Zeichnung blockiert die Pinnwand nicht; die Vorschau besitzt
   feste Grenzen.

### ZF-110 – Dokumentation, Vorlagen und Releaseprüfung

**Status:** geplant, nicht umgesetzt  
**Ziel:** Die erste Stufe vollständig erklären, prüfen und als eigenen
Releaseumfang abnehmen.  
**Nutzen:** Funktionsversprechen, Datenvertrag und tatsächlicher Prüfstand
bleiben deckungsgleich.  
**Aufwand:** M  
**Abhängigkeiten:** ZF-080, ZF-090, ZF-100

**Umfang**

- Bedienvertrag, Daten-/Migrationsvertrag, Architektur, QA-Plan, Changelog,
  Projektübergabe und Dokumentationsindex aktualisieren.
- Mindestens drei Vorlagen anbieten: leer 64 × 64, leer 128 × 128 und
  einfaches Musterraster. Vorlagen enthalten keine urheberrechtlich fremden
  Motive aus den Referenzbildern.
- Automatisierte Modell-, Import-, Export-, Migrations-, Backup- und
  Regressionstests ausführen.
- Manuelle Windows-/macOS-Prüfung für Maus, Tastatur, DPI, Mehrmonitor,
  schmale Fenster, Dateidialoge und Screenreader dokumentieren.
- Leistungswerte und nicht geprüfte Plattformen offen nennen.

**Abnahmekriterien**

1. Alle in Abschnitt 7 genannten Szenarien besitzen grüne automatisierte
   Tests oder einen ausdrücklich offenen manuellen Prüfpunkt.
2. Versionsangaben und Datenformat sind in allen aktuellen Dokumenten
   konsistent.
3. Eine startbare Entwicklungsfassung ist nicht automatisch als signiertes
   Release bezeichnet.
4. Die Dokumentation kennzeichnet Fremd-SVG, Stift und Vektorobjekte weiterhin
   als außerhalb der ersten Stufe.

## 6. P2 und P3 – Getrennter Folgevorrat

### ZF-200 – Weitere belegte Plattformverbesserungen

**Status:** geplant, nicht umgesetzt  
**Ziel:** Andere sinnvolle Lücken erhalten, ohne sie mit der Zeichenfläche zu
vermischen.  
**Aufwand:** mehrere eigenständige Pakete  
**Abhängigkeiten:** unabhängig von der Zeichenfläche

Als getrennte Entscheidungen weiterführen:

- permanente benannte Pinnwandbereiche;
- echte gerichtete Aufgabenabhängigkeiten mit Kreisprüfung;
- Pinnwand-Reisen oder Präsentationsabläufe;
- verknüpfte Punkte mit Rückverweisen;
- geführter Tagesbeginn und Wochenrückblick;
- Vorlagen mit Eingabefeldern;
- benutzerdefinierte Felder und darauf aufbauende Ansichten;
- Systembenachrichtigungen nach erfolgreicher Paketierung.

Jeder Punkt benötigt einen eigenen Daten- und Bedienvertrag. Pinnwandpfeile
werden nicht still zu Abhängigkeiten umgedeutet.

### ZF-300 – Erweiterte Zeichenfunktionen bewerten

**Status:** geplant, nicht umgesetzt  
**Ziel:** Optionen nach einer stabilen Pixelstufe anhand echter Nutzung
bewerten.  
**Aufwand:** mehrere eigenständige Pakete  
**Abhängigkeiten:** abgenommene erste Zeichenstufe

Mögliche spätere Untersuchungen:

- Text- und Vektorobjekte mit dauerhaft editierbaren Eigenschaften;
- allgemeiner Fremd-SVG-Import mit klar definierter Teilmenge;
- Stiftdruck, Touch, Handschrift und plattformspezifische Gesten;
- unbeschränkt wachsende oder gekachelte Großflächen;
- komplexe Ebenenmischung, Masken, Filter und Animation;
- Palettenverwaltung, Dithering und musterbasiertes Füllen;
- Export für weitere Bild- oder Projektformate.

Keiner dieser Punkte darf den Formatvertrag der ersten Stufe rückwirkend
brechen. Neue Eigenschaften werden additiv versioniert oder erhalten eine
explizite Migration.

## 7. Verbindliche Gesamttests der späteren Umsetzung

### Daten und Rundlauf

1. Leere, vollständig gefüllte, transparente und mehrschichtige Bilder für
   64 × 64, 128 × 128 und 256 × 256 speichern und neu laden.
2. JSON → Import → JSON sowie Glide-SVG → Import → Glide-SVG erhalten
   alle zugesagten Eigenschaften.
3. PNG-Ausgabe stimmt bei 1× und ganzzahligen Skalierungen mit der sichtbaren
   Komposition überein.
4. Unbekannte zukünftige optionale Felder folgen dem Formatvertrag;
   unbekannte Pflichtfelder stoppen vor dem Schreiben.

### Eingabe und Undo

1. Langsame und schnelle Striche treffen dieselben durchlaufenen Zellen.
2. Ziehen über Fensterrand, Fokuswechsel und Escape hinterlassen keinen
   halbfertigen Modellzustand.
3. Undo/Redo deckt Strich, Füllung, Form, Auswahl, Ebenenaktionen und
   Flächengröße ab.
4. Werkzeugvorschau ist niemals bereits gespeicherter Bildinhalt.

### Darstellung und Bedienung

1. Unterschiedliche Zoomstufen und Display-Skalierungen treffen dieselben
   logischen Zellen.
2. Raster ein/aus verändert keinen Export und keine Zellkoordinate.
3. Tastaturbedienung, Fokus, Kontrast und Statusmeldungen sind ohne
   Farberkennung verständlich.
4. Schmale Fenster verbergen keine notwendigen Abschluss- oder Speicherwege.

### Sicherheit und Fehlerfälle

1. Fehlerhafte, übergroße und tief verschachtelte Dateien verändern keinen
   bestehenden Inhalt.
2. SVG-Skripte, externe Ressourcen, Entitäten und `foreignObject` werden
   nicht ausgeführt oder nachgeladen.
3. Schreibabbruch vor dem atomaren Ersatz erhält den letzten gültigen Stand.
4. Speicherfehler, fehlender Platz und schreibgeschützte Ziele werden sichtbar
   und reproduzierbar behandelt.

### Migration und Regression

1. Format-18-Bestand wird vor der ersten neuen Speicherung unverändert
   gesichert.
2. Voll- und Teilbackup werden in einem leeren Testdatenordner wiederhergestellt.
3. Aufgaben, Notizen, Tagebücher, Erinnerungen, Vorlagen, Anhänge und
   Pinnwände bleiben erhalten.
4. Import mit neuen Kennungen erhält interne Zeichen- und Pinnwandreferenzen.
5. Tests verwenden ausschließlich einen isolierten `GLIDE_DATA_DIR`.

## 8. Definition of Done für die erste Zeichenstufe

Die erste Stufe ist erst abgeschlossen, wenn:

- ZF-000 bis ZF-110 umgesetzt und ihre Abnahmekriterien erfüllt sind;
- kein offener P0-Datenverlust- oder Importbefund besteht;
- eigene JSON- und Glide-SVG-Dateien verlustfrei wieder bearbeitet werden;
- Backups auf leerem Bestand erfolgreich wiederhergestellt wurden;
- bestehende Glide-Inhalte die Regressionstests bestehen;
- manuelle Zielplattformprüfungen oder ausdrücklich dokumentierte offene
  Grenzen vorliegen;
- Dokumentation, Version und Datenformat konsistent sind.

„Absolut zuverlässig“ wird in dieser Planung nicht als unbeweisbare Garantie
verwendet. Gemeint sind konkrete, reproduzierbare Speicher-, Rundlauf-,
Fehler- und Wiederherstellungstests mit offen dokumentierten Grenzen.
