# Glide – Aufgabensammlung Pixel-Zeichenfläche

Stand 23.09.2026 · Planungsstand · Grundlage: Glide 3.28.0 · Aufgabenformat 18

> **Gesamtstatus: geplant, nicht umgesetzt.** Diese Sammlung ist eine
> umsetzbare Entwicklungsplanung. Kein Punkt in diesem Dokument belegt eine
> vorhandene Zeichenfunktion, eine erfolgte Datenmigration oder eine
> Plattformfreigabe.

Fachliche Grundlage ist der
[Funktionsvergleich und das Zeichenflächenkonzept](Glide_Funktionsvergleich_und_Zeichenflaeche_2026-09-23.md).
Die technische SVG- und Speicherprüfung steht in der
[SVG- und Zeichnungsdaten-Untersuchung](Glide_SVG_und_Zeichnungsdaten_Untersuchung_2026-09-23.md).
Die Reihenfolge richtet sich nach Datenintegrität und Abhängigkeiten, nicht nach
der Sichtbarkeit einer Funktion.

Die Kennungen bleiben als stabile Referenzen erhalten. Die Überschriften sind
bewusst als konkrete Fragen beziehungsweise Ergebnisse formuliert, damit die
Produktentscheidung ohne Kenntnis einer Kennung verständlich ist.

## 1. Festgelegter Zielumfang

- Neue unveränderliche Inhaltsart `drawing` neben `tasks` und `note`.
- Sichtbare Listenarten im Anlagedialog: **Notizen**, **Liste**,
  **Zeichnung**, **Pinnwand**.
  Liste und Pinnwand verwenden beide `tasks` und unterscheiden sich nur in der
  bevorzugten Ansicht.
- Feste Bildfläche mit **128 × 128 logischen, skalierbaren Zellen**.
- Genau eine editierbare Zeichenebene; eine Referenzabbildung ist höchstens eine
  getrennte Editorhilfe.
- Vier noch festzulegende Pinselgrößen, Pipette und Füllung mit
  4er-Nachbarschaft.
- Kein eigener Radierer in V1; der Hintergrund ist deckend weiß und Weiß dient
  als Rücksetzfarbe. Transparenz ist kein Zellzustand der ersten Formatversion.
- Eine Zelle wird bei mindestens einem Drittel geometrischer Abdeckung vom
  Pinsel getroffen.
- Lokaler Undo-/Redo-Ring für die letzten 20 Zellfarbänderungen.
- Vollständig bearbeitbarer Rundlauf eigener JSON- und Glide-SVG-Dateien.
- PNG-Ausgabe und allgemeiner Fremd-SVG-Import sind nachrangig.
- Lokale, atomare Speicherung; Backup, Migration, Duplizieren, Papierkorb und
  Wiederherstellung folgen den bestehenden Glide-Grundsätzen.
- Keine Umsetzung in diesem Dokumentationsauftrag.

## 2. Prioritäten, Aufwand und Abhängigkeiten

| Kennung | Priorität | Arbeitspaket | Aufwand | Abhängigkeiten | Status |
|---|---|---|---|---|---|
| ZF-000 | P0 | Dokumentationsstand konsolidieren | S | keine | geplant, nicht umgesetzt |
| ZF-010 | P0 | Welche Daten bilden genau eine Zeichnung? | M | ZF-000 | geplant, nicht umgesetzt |
| ZF-015 | P0 | Wo liegt die Zeichnung im Glide-Bestand? | M | ZF-010 | geplant, nicht umgesetzt |
| ZF-020 | P0 | Wann darf Glide „gespeichert“ anzeigen? | M | ZF-015 | geplant, nicht umgesetzt |
| ZF-030 | P0 | Welche Zelle trifft der Pinsel und was macht Undo? | M | ZF-010 | geplant, nicht umgesetzt |
| ZF-040 | P1 | Funktioniert das Modell schnell und zugänglich in Tk? | L | ZF-010, ZF-030 | geplant, nicht umgesetzt |
| ZF-050 | P1 | Kann das Zeilenmodell verlustfrei als Text reisen? | M | ZF-010, ZF-020 | geplant, nicht umgesetzt |
| ZF-060 | P1 | Kann Glide sein eigenes SVG sicher rundführen? | L | ZF-010, ZF-040, ZF-050 | geplant, nicht umgesetzt |
| ZF-070 | P1 | Editor-Bedienung und Barrierefreiheit | L | ZF-030, ZF-040 | geplant, nicht umgesetzt |
| ZF-080 | P1 | Integration als Glide-Seitenart | XL | ZF-015, ZF-020, ZF-040, ZF-070 | geplant, nicht umgesetzt |
| ZF-090 | P1 | Backup, Migration und Wiederherstellung | L | ZF-050, ZF-080 | geplant, nicht umgesetzt |
| ZF-100 | P2 | Pinnwand-Referenz und Vorschau | M | ZF-080, ZF-090 | geplant, nicht umgesetzt |
| ZF-110 | P1 | Dokumentation und Releaseprüfung des Kernumfangs | M | ZF-060, ZF-080, ZF-090 | geplant, nicht umgesetzt |
| ZF-200 | P2 | Weitere belegte Plattformverbesserungen | mehrere | unabhängig | geplant, nicht umgesetzt |
| ZF-300 | P3 | Erweiterte Zeichenfunktionen bewerten | mehrere | stabile erste Stufe | geplant, nicht umgesetzt |

Aufwandklassen: **S** = klein, **M** = mittel, **L** = groß, **XL** = sehr
groß. Sie dienen der Reihenfolge und sind keine Zeitschätzung.

## 3. Direkte Produktfragen mit Auswirkung

Bereits entschieden sind: 128 × 128 logische Zellen, eine editierbare Ebene,
deckend weißer Hintergrund ohne Transparenz, vier Pinsel,
Ein-Drittel-Trefferregel, 4er-Füllung, Pipette, auch bei Füllungen höchstens 20
zellweise Undo-Schritte, automatisches Speichern und SVG vor PNG.

Vor einer Implementierung fehlen nur noch folgende Produktantworten:

| Frage | Warum die Antwort benötigt wird | Empfohlener Startwert |
|---|---|---|
| **Welche vier Pinselgrößen und Formen gelten?** | Die Ein-Drittel-Trefferregel benötigt einen geometrischen Fußabdruck. | Quadratisch 1×1, 2×2, 3×3 und 4×4 Zellen. |
| **Braucht V1 zusätzlich Gerade, Rechteck oder Auswahl?** | Der beschriebene Bedienweg nennt freies Ziehen mit vier Pinseln, nicht zwingend eigene Formwerkzeuge. | V1 zunächst nur Pinsel, Füllung und Pipette. |
| **Reichen 256 Farben pro Zeichnung?** | Zwei Hexzeichen je Zelle halten das Modell fest bei ungefähr 34 KB. | Ja; mehr Farben erst mit neuer Formatversion. |
| **Soll ein Referenz-PNG im Backup enthalten sein?** | Eine Referenz ist Editorhilfe, kann aber für späteres Weiterzeichnen wichtig sein. | Als lokaler Glide-Anhang sichern, nicht ins SVG-Bild exportieren. |
| **Darf ein Tagebuchordner nur Notizseiten enthalten?** | Die Antwort steuert Anlageoptionen und Vorlagen im Ordner. | Nur Notizseiten; Zeichnungen in normalen Ordnern. |
| **Ist auch die Ordnerart nach Anlage unveränderlich?** | Verhindert verdeckte Inhalts- und Darstellungswechsel. | Ja. |
| **Bleibt SVG Austauschformat oder wird es später Primärdatei?** | Eine Primärdatei braucht Mehrdatei-Transaktionen, Papierkorb- und Backupregeln. | V1: internes Zeilenmodell; SVG für Export und Rückimport. |

Die ausführliche technische Begründung steht im
[Fragenabschnitt der SVG-Untersuchung](Glide_SVG_und_Zeichnungsdaten_Untersuchung_2026-09-23.md#8-noch-zu-beantwortende-produktfragen).

## 4. P0 – Verträge vor Implementierung

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
- Den aktuellen Rich-Text-Widerspruch zwischen allgemeinem Produktgrenzen-
  Vertrag und spezifischem Format-17/18-Vertrag korrigieren. Historische
  Aussagen zu fehlendem Zoom, Navigator und früherem Pinnwandtransport als
  überholt markieren, ohne historische Dokumente rückwirkend umzuschreiben.
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

### Welche Daten bilden genau eine Zeichnung? (ZF-010)

**Status:** geplant, nicht umgesetzt  
**Ziel:** Das vollständige, UI-unabhängige Modell `glide.drawing` Version 1 für
genau 128 × 128 Zellen und eine editierbare Ebene festlegen.  
**Nutzen:** Bearbeitbarkeit und Zukunftsfähigkeit hängen nicht von Tk,
Bildschirmauflösung oder einem Exportformat ab.  
**Aufwand:** M  
**Abhängigkeiten:** ZF-000

**Umfang**

- Dokumentfelder für Formatkennung, Version, feste Breite/Höhe, Farbraum,
  Palette, Codierung und 128 Zeilen festlegen.
- Im Arbeitsspeicher ein Array aus genau 16.384 Palettenindizes verwenden.
- Im gespeicherten Modell `hex8-row-v1` verwenden: genau 128 Zeilen mit je
  128 zweistelligen Hex-Palettenindizes.
- Palette in V1 vorläufig auf 256 sRGB-Farben begrenzen.
- `palette[0]` verbindlich als `#FFFFFF` festlegen; Farbcodes und
  Hex-Palettenindizes werden in Großbuchstaben normalisiert. Transparenz und
  Alphawerte sind in Version 1 unzulässig.
- Eine editierbare Ebene festschreiben; Ebenenliste, Ebenen-ID, Sichtbarkeit,
  Sperre und Mischmodi entfallen.
- Kanonische Feldreihenfolge und kompakte JSON-Normalisierung für Prüfsummen
  festlegen.
- Harte Grenzen für Palette, Dateigröße, Textlängen und Verschachtelung
  festlegen.
- Verhalten für unbekannte optionale und unbekannte verpflichtende Felder
  definieren.
- Beispiel für ein leeres, ein kleines mehrfarbiges und ein vollständig
  gefülltes Dokument liefern.

**Abnahmekriterien**

1. Der Vertrag beschreibt genau 16.384 Zellen ohne Kenntnis von UI, Zoom oder
   Displayauflösung.
2. Zwei Implementierungen könnten anhand des Dokuments denselben kanonischen
   JSON-Inhalt erzeugen.
3. Fehlende Zeilen, falsche Zeilenlänge, ungültige Hexwerte, Farben und
   Palettenindizes haben jeweils eine eindeutige Fehlerfolge.
4. Zoom, Pan, Navigator, Rasteranzeige und aktives Werkzeug sind ausdrücklich
   kein Bestandteil des fachlichen Bildmodells.
5. Ein vollständig gefülltes Bild bleibt in der vorgesehenen Codierung klein
   und benötigt keine Einzelobjekte je Zelle.

**Quellen:** Glide-Austauschformat 1, Datenvertrag Format 17/18 und
[SVG- und Zeichnungsdaten-Untersuchung](Glide_SVG_und_Zeichnungsdaten_Untersuchung_2026-09-23.md#3-bewertung-der-beiden-speicherideen).

### Wo liegt die Zeichnung im Glide-Bestand? (ZF-015)

**Status:** geplant, nicht umgesetzt  
**Ziel:** Listentyp, Ansichtsmodell und physische Einbettung entscheiden, bevor
Autosave, Backup oder Import gebaut werden.  
**Nutzen:** Verhindert, dass Zeichnungen still zu Aufgabenlisten werden oder
bei Duplizieren, Papierkorb und Backup verloren gehen.  
**Aufwand:** M  
**Abhängigkeiten:** ZF-010

**Bereits festgelegt**

- `list_kind` erhält die Werte `tasks | note | drawing`.
- Liste und Pinnwand verwenden beide `tasks`. `preferred_view: list | board`
  speichert die bevorzugte Darstellung.
- Notiz und Zeichnung sind nach Anlage nicht konvertierbar.
- Ordner verwenden `folder_kind: standard | journal`.
- V1 speichert das kompakte `drawing`-Modell als typbezogenes Feld im
  Listenobjekt und damit zusammen mit den anderen Glide-Daten.
- SVG ist zunächst Austauschformat, nicht der normale Autosave-Speicher.

**Umfang**

- Stille Normalisierung unbekannter `list_kind`-Werte zu `tasks` durch eine
  zentrale, explizite Typregistrierung ersetzen.
- Pro Typ zulässige Ansichten und Aktionen definieren: Aufgaben erlauben
  Liste/Pinnwand/Tabelle, Notizen den Notizeditor und Zeichnungen den
  Zeicheneditor.
- Typwahl aus dem späteren Bearbeiten-Dialog entfernen oder nur lesbar zeigen.
- Anlageoption **Pinnwand** auf `tasks/board` abbilden; Liste ↔ Pinnwand ändert
  ausschließlich die Ansicht.
- `drawing` auf allen Containerwegen mitführen: Duplizieren, Papierkorb,
  Vorlagen, Teilbackup, Vollbackup, Wiederherstellung und Austausch.
- Unbekannte Typen in einem bekannten neuen Schema sichtbar ablehnen.

**Abnahmekriterien**

1. Eine als Pinnwand angelegte Aufgabenliste enthält denselben Aufgabenbestand
   wie ihre Listenansicht.
2. Notiz und Zeichnung bieten keine Typkonvertierung an.
3. Eine Zeichenliste kann keine Aufgabe über Tastenkürzel, Schnellanlage oder
   versteckte Ansicht aufnehmen.
4. Ein unbekannter Inhaltstyp wird nie still zu `tasks` umgedeutet.
5. Das eingebettete Zeichenmodell reist bei Duplizieren, Papierkorb und Backup
   vollständig mit.

**Quellen:** aktueller Glide-Code für `new_list_object`, Listenanlage,
Ansichtsumschaltung und Backup; lokale Pinnwandverträge 3.23/3.24;
[SVG- und Zeichnungsdaten-Untersuchung](Glide_SVG_und_Zeichnungsdaten_Untersuchung_2026-09-23.md#6-bezug-zum-glide-datenmodell).

### Wann darf Glide „gespeichert“ anzeigen? (ZF-020)

**Status:** geplant, nicht umgesetzt  
**Ziel:** Verlustarme Speicherung bei normaler Nutzung, Schreibfehlern und
Programmneustart verbindlich definieren.  
**Nutzen:** „Gespeichert“ wird eine prüfbare Zusage und kein bloßer UI-Zustand.  
**Aufwand:** M  
**Abhängigkeiten:** ZF-015

**Umfang**

- Autosave während eines Pinselzugs und für kurze Folgeschritte bündeln. Nicht
  nach jedem einzelnen Zelltreffer die gesamte Glide-Datei schreiben.
- Erzwungenes Flush vor Navigation, Export, Backup und Programmende definieren.
- Schreiben über temporäre Datei, Validierung und atomaren Ersatz planen;
  der letzte gültige Stand bleibt bis zum erfolgreichen Ersatz erhalten.
- Zustände `ungespeichert`, `speichert`, `gespeichert` und `Fehler` samt
  zugänglicher Statusmeldung definieren.
- Den dauerhaften Änderungsverlauf um einen Hash des kanonischen
  Zeichenmodells erweitern. Pro erfolgreichem gebündeltem Speichervorgang
  entsteht höchstens ein Eintrag **„Zeichnung geändert“**; er enthält keine
  Zellen und keinen wiederherstellbaren Bildstand.
- Wiederanlauf nach Prozessabbruch sowie Umgang mit verwaisten temporären
  Dateien festlegen.
- Dokumentieren, dass Glide selbst nicht synchronisiert, Zeichnungen aber die
  vorhandenen Regeln für extern gewählte beziehungsweise synchronisierte
  Datenordner einhalten.
- OneDrive-Platzhalter, Belegungsdatei, Revisionsprüfung, Konfliktkopien und
  Schreibfehler in synchronisierten Ordnern in die Fehlerprüfung aufnehmen.
- Vorläufige Autosave-Verzögerung im Prototyp messen und danach verbindlich
  festschreiben.

**Abnahmekriterien**

1. Nach angezeigtem Zustand `gespeichert` enthält ein Neustart ohne Netzwerk
   exakt den bestätigten Inhalt.
2. Ein simulierter Fehler vor dem atomaren Ersatz beschädigt den vorherigen
   Stand nicht.
3. Seitenwechsel, Backup und Programmende warten auf ein ausstehendes Save
   oder melden nachvollziehbar, warum sie nicht fortfahren.
4. Ein Speicherfehler bleibt sichtbar; weitere Bearbeitung vernichtet weder
   den letzten gültigen Stand noch die ungespeicherten Änderungen still.
5. Zwanzig schnelle Zelländerungen lösen nicht zwanzig vollständige
   Dateischreibvorgänge aus.
6. Eine gespeicherte Zeichenänderung ist im dauerhaften Verlauf als
   zusammengefasste Listenänderung erkennbar; der Verlauf wird nicht zum
   zweiten Zeichen-Undo oder zur Bildversionsablage.

**Quellen:** Glide-Daten- und Migrationsvertrag; als Vergleich die offizielle
[Todoist-Offlinedokumentation](https://www.todoist.com/help/todoist/features/use-todoist-while-offline-4rbaZw).

### Welche Zelle trifft der Pinsel und was macht Undo? (ZF-030)

**Status:** geplant, nicht umgesetzt  
**Ziel:** Trefferberechnung, 4er-Füllung und die letzten 20
Zellfarbänderungen eindeutig festlegen.  
**Nutzen:** Verhindert Lücken, hängende Werkzeuge und schwer erklärbare
Teiländerungen.  
**Aufwand:** M  
**Abhängigkeiten:** ZF-010

**Umfang**

- Vier Pinsel als geometrische Fußabdrücke in logischen Zellen definieren.
- Eine Zelle umfärben, sobald mindestens ein Drittel ihrer Fläche vom
  Pinselabdruck überdeckt wird.
- Schnelle Bewegungen durch ausreichend feine Interpolation zwischen zwei
  erfassten Positionen schließen.
- Füllen ausschließlich mit 4er-Nachbarschaft implementieren.
- Jede tatsächlich geänderte Zelle mit `index`, `vorher` und `nachher` in
  einen lokalen Ringpuffer eintragen; Kapazität 20.
- Interpolierte Pinselpositionen in Bewegungsrichtung verarbeiten; innerhalb
  einer Position gleichzeitig getroffene Zellen nach `y`, dann `x` schreiben.
- Editor-Undo/Redo vom globalen Glide-Snapshot trennen.
- Auch bei einer Füllung jede tatsächlich geänderte Zelle einzeln und in
  deterministischer Reihenfolge in den Ringpuffer schreiben. Nach mehr als 20
  Änderungen bleiben ausschließlich die letzten 20 rücknehmbar.
- Die 4er-Füllung iterativ als Breitensuche ausführen: Startzelle zuerst,
  Nachbarn in der Reihenfolge links, rechts, oben, unten; eine Zelle bereits
  beim Einreihen markieren.
- `Escape`, Fokusverlust, Fensterwechsel und Loslassen außerhalb der Fläche
  einheitlich behandeln.
- Redo-Zweig nach einer neuen Zelländerung verwerfen.
- Undo nach Neustart bewusst beenden; der gespeicherte Bildinhalt bleibt davon
  unberührt.

**Abnahmekriterien**

1. Ein schneller diagonaler oder gebogener Zug enthält nach der definierten
   Ein-Drittel-Regel keine ausgelassenen Treffer.
2. Diagonal berührende Farbflächen werden von der 4er-Füllung nicht verbunden.
3. Zwanzig Undo-Schritte stellen exakt die letzten 20 Zellfarben wieder her;
   der 21. Schritt ist nicht mehr verfügbar.
4. Mehrfaches Treffen derselben bereits gleichfarbigen Zelle verbraucht keinen
   Undo-Platz.
5. Abbruch, Fokusverlust und Loslassen außerhalb hinterlassen keinen aktiven
   Dauerzustand und keine halbe Zelländerung.
6. Eine Füllung von mehr als 20 Zellen lässt genau ihre letzten 20
   Zelländerungen einzeln zurücknehmen; ein weiterer Undo-Schritt ist nicht
   verfügbar.

**Quellen:** bestehende Glide-Mutations- und Undo-Wege,
[Microsoft Paint](https://www.microsoft.com/en-US/windows/paint) und
[SVG- und Zeichnungsdaten-Untersuchung](Glide_SVG_und_Zeichnungsdaten_Untersuchung_2026-09-23.md#8-noch-zu-beantwortende-produktfragen).

## 5. P1 – Isolierte Entwicklung und Austausch

### Funktioniert das Modell schnell und zugänglich in Tk? (ZF-040)

**Status:** geplant, nicht umgesetzt  
**Ziel:** Modell, Rendering und Eingabeverhalten außerhalb des produktiven
App-Flusses messen, bevor das Hauptdatenformat geändert wird.  
**Nutzen:** Technische Risiken werden sichtbar, ohne bestehende Nutzerdaten zu
berühren.  
**Aufwand:** L  
**Abhängigkeiten:** ZF-010, ZF-030

**Umfang**

- Reines Zeichenmodell ohne Tk-Abhängigkeit implementieren und testen.
- Canvas-Zellen, zeilenweise Aktualisierung und Bildpuffer für fest
  128 × 128 vergleichen.
- Zoom, Pan, sichtbares Raster und Koordinatenabbildung isoliert erproben.
- Leistung bei vier Pinselgrößen, vollständiger 4er-Füllung, Zell-Undo/Redo,
  Vollrendering sowie Zeilen-Codierung und -Decodierung messen.
- Vorläufige Ziele messen: sichtbare Eingabereaktion höchstens 50 ms im
  95. Perzentil, Vollrender und Vollfüllung jeweils höchstens 100 ms auf dem
  dokumentierten Referenzsystem. Abweichungen bewusst begründen statt die
  Messgrenze nachträglich still zu verschieben.
- Frühen Machbarkeitstest für Tastatur-Zellcursor, Koordinatenansage,
  Werkzeugstatus und Farbinformation vorsehen.
- Abbruchschwellen und Renderstrategie dokumentieren. Keine neue Abhängigkeit
  allein aus Bequemlichkeit einführen.

**Abnahmekriterien**

1. Der Prototyp verwendet ausschließlich einen temporären, isolierten
   Datenordner und kann keinen echten Glide-Bestand öffnen.
2. Dieselbe Modellkoordinate wird bei allen geprüften Zoomstufen und
   Display-Skalierungen getroffen.
3. 128 × 128 Zellen, größter Pinsel und vollständige Füllung werden gegen die
   vorläufigen Reaktionsziele gemessen; Messwerte und Testrechner sind
   dokumentiert.
4. Die gewählte Renderstrategie ist austauschbar, ohne den Formatvertrag zu
   ändern.
5. Der Prototyp zeigt, wie Tastaturfokus und textliche Statusinformation ohne
   semantische Canvas-Zellen zugänglich angeboten werden.

**Quellen:** lokale Glide-Architektur und Leistungsdokumentation,
[Python 3.12: Tkinter](https://docs.python.org/3.12/library/tkinter.html),
[Tk 8.6: Canvas](https://www.tcl-lang.org/man/tcl8.6/TkCmd/canvas.htm).

### Kann das Zeilenmodell verlustfrei als Text reisen? (ZF-050)

**Status:** geplant, nicht umgesetzt  
**Ziel:** Verlustfreier Text-Rundlauf des kanonischen Zeichenmodells.  
**Nutzen:** Zukunftssichere, offene und prüfbare Bearbeitbarkeit.  
**Aufwand:** M  
**Abhängigkeiten:** ZF-010, ZF-020

**Umfang**

- Dateiimport und Einfügen aus Text auf denselben Parser und dieselbe
  Validierung führen.
- Importvorschau mit festen Maßen, Palette, Farbverteilung, Warnungen und
  unbekannten Angaben bereitstellen.
- Import standardmäßig als neue Zeichnung; Ersetzen einer offenen Zeichnung
  nur als ausdrückliche Aktion mit Sicherung.
- Kanonischen Export mit stabiler Feldreihenfolge, genau 128 Zeilen und
  normalisierten Hex-Indizes erzeugen.
- Import standardmäßig als neue Zeichnung anlegen. Beim ausdrücklichen
  Ersetzen einer vorhandenen Zeichnung vorher eine wiederherstellbare Sicherung
  erzeugen; der 20-Zellen-Undo-Puffer ist dafür nicht ausreichend.

**Abnahmekriterien**

1. Export → Import → Export ergibt semantisch und kanonisch denselben
   Zeicheninhalt.
2. Beschädigte, übergroße oder unbekannte Pflichtangaben verändern keinen
   vorhandenen Bestand.
3. Dateiimport und Textimport melden dieselben Fehler an denselben Feldern.
4. Umlaute und Zeichen außerhalb der BMP in Titel und Metadaten bleiben
   erhalten.

**Quellen:** [RFC 8259: JSON](https://www.rfc-editor.org/rfc/rfc8259),
[RFC 8785: JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785.html)
und die lokale SVG-/Speicheruntersuchung.

### Kann Glide sein eigenes SVG sicher rundführen? (ZF-060)

**Status:** geplant, nicht umgesetzt  
**Ziel:** Skalierbare Standardausgabe und kontrollierter Rückimport des engen
Glide-SVG-Profils.  
**Nutzen:** Zeichnungen lassen sich außerhalb von Glide verwenden, ohne den
Glide-Rundlauf eigener Dateien aufzugeben.  
**Aufwand:** L  
**Abhängigkeiten:** ZF-010, ZF-040, ZF-050

**Umfang**

- `viewBox="0 0 128 128"`, quadratisches Seitenverhältnis und
  `shape-rendering="crispEdges"` festlegen.
- Sichtbare Grafik aus einem Hintergrundrechteck und horizontalen
  `rect`-Läufen mit ganzzahligen Koordinaten erzeugen.
- Vollständiges kanonisches Zeilenmodell im Namespace
  `urn:glide:drawing:1` unter `metadata` einbetten.
- `model-sha256` für das normalisierte Modell und `artwork-sha256` für die
  normalisierten sichtbaren Rechteckläufe berechnen.
- Das Modell vor dem Hash als kompaktes UTF-8-JSON ohne Gleitkommazahlen,
  mit sortierten ASCII-Schlüsseln, eindeutigen Palettenfarben,
  Großbuchstaben-Farbcodes und `palette[0] = #FFFFFF` serialisieren. XML-
  Escaping erfolgt erst beim Schreiben als Textknoten und gehört nicht zu den
  Hashbytes.
- Für die Grafik den weißen Hintergrund plus die aus dem Modell abgeleiteten
  maximalen, nichtweißen horizontalen Läufe normalisieren: nach `y`, dann `x`
  sortieren, gleichfarbige Nachbarläufe zusammenführen und jeden Lauf als
  ganzzahligen Datensatz hashen. Überlappungen und zusätzliche Rechtecke sind
  ungültig.
- Dateiimport und „SVG-Text einfügen“ auf denselben Parser und dieselben
  Fehlercodes führen.
- Höchstens 4 MiB unkomprimiertes UTF-8-XML akzeptieren; vor dem Parser
  `DOCTYPE`, `ENTITY` und fremde Verarbeitungsanweisungen ablehnen.
- Nur `svg`, `title`, `desc`, `metadata`, festgelegte Glide-Metadaten,
  Hintergrund-`rect`, `g#glide-artwork` und darin `rect` erlauben.
- Skript, Ereignisattribute, CSS, `path`, `transform`, Animation, `image`,
  `use`, Links, URL-Werte, `foreignObject`, Filter, Masken und unbekannte
  Elemente abweisen.
- Widersprüche zwischen Modell und sichtbarer Grafik vor jeder
  Bestandsänderung klassifizieren. Die Vorschau wird aus dem validierten
  Modell mit dem in ZF-040 gewählten Tk-Verfahren gezeichnet.
- PNG vollständig aus diesem Paket herauslassen; es erhält bei Bedarf später
  ein eigenes Arbeitspaket.

**Abnahmekriterien**

1. Eigenes Glide-SVG durchläuft Export → Import → Export ohne Verlust einer
   der 16.384 Zellfarben oder eines Palettenwerts.
2. Ein SVG ohne gültige Glide-Metadaten wird in V1 als Zeichnungsimport
   abgelehnt und verändert keinen Bestand.
3. SVG mit Skript, CSS, Pfad, Transformation, Referenz, übergroßer Struktur
   oder anderem verbotenen Inhalt wird vor jeder Modelländerung abgewiesen.
4. Eine erlaubte Textänderung des eingebetteten Modells wird als Vorschau
   gezeigt und erzeugt nach Bestätigung eine neue normalisierte Grafik.
5. Eine Änderung nur an der sichtbaren Grafik wird nicht als verlustfreier
   Glide-Rundlauf akzeptiert, sondern mit unverändertem Bestand abgelehnt.
6. Stimmen Modell und Grafik semantisch überein, erzeugt der normalisierte
   Export unabhängig von XML-Einrückung, Attributreihenfolge und
   Namespacepräfix denselben Modell- und Grafikhash.

**Quellen:** [SVG- und Zeichnungsdaten-Untersuchung](Glide_SVG_und_Zeichnungsdaten_Untersuchung_2026-09-23.md),
[W3C: SVG-Metadaten](https://www.w3.org/TR/SVG/struct.html#MetadataElement),
[W3C: Secure Static Mode](https://www.w3.org/TR/SVG/conform.html#processing-modes),
[Python 3.12: XML-Sicherheit](https://docs.python.org/3.12/library/xml.html),
[Figma: SVG-Austausch](https://help.figma.com/hc/en-us/articles/360040030374-Copy-assets-between-design-tools).

### Wie bleibt der Editor mit Maus und Tastatur zuverlässig? (ZF-070)

**Status:** geplant, nicht umgesetzt  
**Ziel:** Zuverlässige Bedienung mit Maus und Tastatur in breiten und schmalen
Fenstern.  
**Nutzen:** Die Zeichenfläche bleibt im Unternehmensalltag auffindbar und
beherrschbar.  
**Aufwand:** L  
**Abhängigkeiten:** ZF-030, ZF-040

**Umfang**

- Werkzeugleiste mit sichtbarer Pinselgröße, gewählter Farbe, Füllung,
  Pipette, Zoom und Speicherstatus planen.
- Seltene Aktionen in ein beschriftetes Menü verschieben; Kernwerkzeuge
  bleiben direkt erreichbar.
- Tastaturpfade für Pinselgröße, Farbe/Pipette, Füllung, Zoom, Pan, Undo
  und Redo definieren.
- Fokusrahmen, Statusmeldungen und Fehlerhinweise ohne alleinige
  Farbcodierung gestalten.
- Verhalten bei schmalen Fenstern, hoher DPI, Mehrmonitorbetrieb und
  horizontalem/vertikalem Scrollen prüfen.
- Maus bildet die erste Eingabestufe. Touch, Stiftdruck und Handschrift bleiben
  außerhalb dieses Pakets.

**Abnahmekriterien**

1. Alle bestätigten Grundwerkzeuge sind ohne Maus erreichbar und ihr aktiver Zustand ist
   mit Fokus und Screenreader-tauglichem Text erkennbar.
2. Zoom verändert weder die logische Cursorzelle noch das Ergebnis eines
   Tastatur-Pixelschritts.
3. Bei Minimalbreite bleiben Zeichenfläche, Speicherstatus und Abschlusswege
   erreichbar.
4. Ein manueller Prüfplan deckt Windows und macOS, DPI, Mehrmonitor,
   Fokuswechsel und Screenreader ab.

**Quellen:** lokales Glide-Designsystem und QA-Plan,
[OneNote: Organisation mit Screenreader](https://support.microsoft.com/en-us/accessibility/onenote/use-a-screen-reader-to-organize-notebooks-sections-and-pages-in-onenote).

## 6. P1 und P2 – Integration in Glide

### Wie wird die Zeichnung als Glide-Listenart integriert? (ZF-080)

**Status:** geplant, nicht umgesetzt  
**Ziel:** Den isoliert bestätigten Editor als dritte Seitenart in den
bestehenden Lebenszyklus integrieren.  
**Nutzen:** Zeichnungen nutzen dieselbe Navigation, Datenhoheit und
Schutzmechanismen wie Aufgaben und Notizen.  
**Aufwand:** XL  
**Abhängigkeiten:** ZF-015, ZF-020, ZF-040, ZF-070

**Umfang**

- `list_kind` explizit auf `tasks | note | drawing` erweitern.
- `preferred_view: list | board` für `tasks` einführen. Die sichtbare
  Anlageoption **Pinnwand** erzeugt `tasks/board`, keinen vierten Inhaltstyp.
- Zentrale Typ-/Fähigkeitstabelle für zulässige Ansichten, Inhaltsfeld,
  Schnellerfassung und Exporter einrichten.
- Erstellung aus Neu-Menü, Ordnerkontext und typgefilterten Vorlagen anbieten.
- Titel, Beschreibung, Labels, lokale Anhänge und Seitenmetadaten mit
  bestehenden Regeln verbinden.
- Suche indexiert Titel und Metadaten; eine Pixel-Inhaltssuche ist nicht Teil
  der ersten Stufe.
- Duplizieren, Verschieben, Umbenennen, Papierkorb, Wiederherstellen und
  endgültiges Entfernen definieren.
- Aufgaben-, Notiz- und Zeichnungsart nach Anlage nicht konvertieren. Nur
  Liste ↔ Pinnwand wechselt die Ansicht eines `tasks`-Bestands.
- Bestehende Mutations-, Modal- und Speicherpfade verwenden; keine parallele
  zweite Datenbank einführen.

**Abnahmekriterien**

1. Eine Zeichnungsseite lässt sich erstellen, benennen, verschieben,
   duplizieren, löschen und wiederherstellen, ohne Aufgaben oder Notizen zu
   verändern.
2. Eine Aufgabenliste wechselt verlustfrei zwischen Liste und Pinnwand; Notiz
   und Zeichnung bieten keinen Typwechsel.
3. Navigation mit ungespeicherten Änderungen folgt ZF-020.
4. Format-18-Bestände werden vor dem ersten Schreiben des neuen Formats
   gesichert und in den zukunftsorientierten neuen Vertrag überführt.
5. Eine ältere Glide-Fassung darf den neuen Bestand nicht unbemerkt
   schreibend verändern.
6. Ein unbekannter künftiger `list_kind` wird sichtbar abgelehnt und niemals zu
   `tasks` normalisiert.

**Quellen:** lokaler Datenvertrag, Pinnwandverträge 3.23/3.24 und die
[SVG- und Zeichnungsdaten-Untersuchung](Glide_SVG_und_Zeichnungsdaten_Untersuchung_2026-09-23.md#6-bezug-zum-glide-datenmodell).

### Wie reisen Zeichnungen durch Backup und Migration? (ZF-090)

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
- Bei einer als Pinnwand angelegten Aufgabenliste sowohl `preferred_view` als
  auch die zugehörige Kartenanordnung im Teilbackup transportieren und beim
  additiven Import neu zuordnen.
- Vollrestore und additives Hinzufügen mit neuen Kennungen prüfen.
- Zeichnungen im Papierkorb, leere Zeichnungen, große Zeichnungen und
  Anhänge abdecken.
- Backupgrenzen und Vorschau um Zeichnungsanzahl, Abmessungen und Gesamtgröße
  erweitern.
- Wiederherstellung in einen leeren, isolierten Datenordner als verpflichtenden
  Release-Test festlegen.

**Abnahmekriterien**

1. Vollbackup → Wiederherstellung in leerem Datenordner erhält Dokumente,
   alle 16.384 Zellwerte, Palette, Metadaten, Anhänge und Verknüpfungen.
2. Teilbackup transportiert alle Zeichnungen im gewählten Zweig und keine
   fremden Seiten.
3. Ein beschädigtes Archiv verändert den bestehenden Bestand nicht.
4. Migration scheitert sicher, wenn die unveränderte Vorsicherung nicht
   geschrieben werden kann.
5. Bestehende Aufgaben, Notizen, Tagebücher und Pinnwände sind nach Migration
   byte- beziehungsweise semantisch unverändert, soweit die Normalisierung
   keine dokumentierte Ergänzung verlangt.

Es gibt kein Versprechen, Zeichnungen in alte Glide-Formate zurückzukonvertieren.
Die neue Version muss den aktuellen Bestand sicher übernehmen und ältere
Schreiber am verändernden Öffnen hindern.

**Quellen:** lokaler Daten-/Migrationsvertrag, Backupvertrag und
Pinnwandtransport 3.24.

### Wie erscheint eine Zeichnung auf der Pinnwand? (ZF-100)

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
  Pinnwandeinstellungen; Zellmodell und Palette bleiben Seiteninhalt.
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

**Quellen:** lokale Pinnwandverträge 3.23/3.24,
[FigJam-Leitfaden](https://help.figma.com/hc/en-us/articles/1500004362321-Guide-to-FigJam),
[Trello-Boards](https://support.atlassian.com/trello/docs/creating-a-new-board/).

### Ist der Kernumfang dokumentiert und releasefähig? (ZF-110)

**Status:** geplant, nicht umgesetzt  
**Ziel:** Die erste Stufe vollständig erklären, prüfen und als eigenen
Releaseumfang abnehmen.  
**Nutzen:** Funktionsversprechen, Datenvertrag und tatsächlicher Prüfstand
bleiben deckungsgleich.  
**Aufwand:** M  
**Abhängigkeiten:** ZF-060, ZF-080, ZF-090

**Umfang**

- Bedienvertrag, Daten-/Migrationsvertrag, Architektur, QA-Plan, Changelog,
  Projektübergabe und Dokumentationsindex aktualisieren.
- Mindestens zwei Vorlagen anbieten: leer 128 × 128 und ein eigenes einfaches
  Musterraster. Vorlagen enthalten keine fremden oder wasserzeichenbehafteten
  Motive aus den Referenzbildern.
- Automatisierte Modell-, Import-, Export-, Migrations-, Backup- und
  Regressionstests ausführen.
- Manuelle Windows-/macOS-Prüfung für Maus, Tastatur, DPI, Mehrmonitor,
  schmale Fenster, Dateidialoge und Screenreader dokumentieren.
- Leistungswerte und nicht geprüfte Plattformen offen nennen.

**Abnahmekriterien**

1. Alle in Abschnitt 8 genannten Szenarien besitzen grüne automatisierte
   Tests oder einen ausdrücklich offenen manuellen Prüfpunkt.
2. Versionsangaben und Datenformat sind in allen aktuellen Dokumenten
   konsistent.
3. Eine startbare Entwicklungsfassung ist nicht automatisch als signiertes
   Release bezeichnet.
4. Die Dokumentation kennzeichnet Fremd-SVG, Stift und Vektorobjekte weiterhin
   als außerhalb der ersten Stufe.
5. Die optionale Pinnwandvorschau ZF-100 blockiert die Freigabe des
   Zeichen-Kernumfangs nicht und erhält bei Umsetzung eine eigene
   Integrationsprüfung.

**Quellen:** alle in ZF-000 bis ZF-090 genannten Verträge und Herstellerquellen.

## 7. P2 und P3 – Getrennter Folgevorrat

### Welche anderen Plattformlücken bleiben danach? (ZF-200)

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

**Einordnung und Quellen:** Dieses Paket ist ein Epic/Forschungsvorrat und noch
kein einzeln abnehmbares Arbeitspaket. Quellen und Wettbewerbsbelege stehen im
Funktionsvergleich; vor Umsetzung wird jeder Punkt in eine eigene Kennung mit
Abnahme zerlegt.

### Welche erweiterten Zeichenfunktionen werden später bewertet? (ZF-300)

**Status:** geplant, nicht umgesetzt  
**Ziel:** Optionen nach einer stabilen Pixelstufe anhand echter Nutzung
bewerten.  
**Aufwand:** mehrere eigenständige Pakete  
**Abhängigkeiten:** abgenommene erste Zeichenstufe

Mögliche spätere Untersuchungen:

- PNG-Ausgabe und optionaler PNG-Import als Referenzhilfe;
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

**Einordnung und Quellen:** Dieses Paket ist ein Epic/Forschungsvorrat. Die
Grundlagen stehen in der SVG-Untersuchung sowie in den Herstellerquellen zu
Paint, Figma und OneNote. Vor Umsetzung erhält jede Funktion eine eigene
Kennung, Quelle, Grenze und Abnahme.

## 8. Verbindliche Gesamttests der späteren Umsetzung

### Daten und Rundlauf

1. Leere, vollständig weiße, vollständig gefüllte, schachbrettartige,
   zufällige und typische Pixelmotive mit 128 × 128 Zellen speichern und neu
   laden.
2. JSON → Import → JSON sowie Glide-SVG → Import → Glide-SVG erhalten
   alle zugesagten Eigenschaften.
3. Jede gespeicherte Zeile besitzt exakt 128 gültige Palettenindizes; ein
   vollständig gefülltes Bild bleibt innerhalb der dokumentierten Größe.
4. Unbekannte zukünftige optionale Felder folgen dem Formatvertrag;
   unbekannte Pflichtfelder stoppen vor dem Schreiben.
5. Modell- und Grafikprüfsumme klassifizieren unveränderte, nur im Modell
   geänderte, nur grafisch geänderte und widersprüchliche SVGs eindeutig.

### Eingabe und Undo

1. Langsame und schnelle Pinselzüge treffen nach der Ein-Drittel-Regel dieselben
   logischen Zellen.
2. Ziehen über Fensterrand, Fokuswechsel und Escape hinterlassen keinen
   halbfertigen Modellzustand.
3. Der lokale Puffer nimmt exakt die letzten 20 tatsächlichen
   Zellfarbänderungen zurück; unverändertes Übermalen verbraucht keinen Platz.
4. Die 4er-Füllung verbindet keine nur diagonal angrenzenden Flächen.
5. Eine Füllung mit mehr als 20 geänderten Zellen lässt genau die letzten 20
   Zellen einzeln rückgängig machen; ältere Änderungen der Füllung bleiben
   bestehen.

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
3. SVG mit CSS, Pfad, Transformation, `use`, `image`, Link oder Daten-URL wird
   vom V1-Profil abgewiesen.
4. Schreibabbruch vor dem atomaren Ersatz erhält den letzten gültigen Stand.
5. Speicherfehler, fehlender Platz und schreibgeschützte Ziele werden sichtbar
   und reproduzierbar behandelt.

### Migration und Regression

1. Format-18-Bestand wird vor der ersten neuen Speicherung unverändert
   gesichert.
2. Voll- und Teilbackup werden in einem leeren Testdatenordner wiederhergestellt.
3. Aufgaben, Notizen, Tagebücher, Erinnerungen, Vorlagen, Anhänge und
   Pinnwände bleiben erhalten.
4. Import mit neuen Kennungen erhält interne Zeichen- und Pinnwandreferenzen.
5. Tests verwenden ausschließlich einen isolierten `GLIDE_DATA_DIR`.

## 9. Definition of Done für die erste Zeichenstufe

Der Zeichen-Kernumfang ist abgeschlossen, wenn:

- ZF-000, ZF-010, ZF-015, ZF-020 bis ZF-090 sowie ZF-110 umgesetzt und ihre
  Abnahmekriterien erfüllt sind;
- kein offener P0-Datenverlust- oder Importbefund besteht;
- eigene JSON- und Glide-SVG-Dateien verlustfrei wieder bearbeitet werden;
- Backups auf leerem Bestand erfolgreich wiederhergestellt wurden;
- bestehende Glide-Inhalte die Regressionstests bestehen;
- manuelle Zielplattformprüfungen oder ausdrücklich dokumentierte offene
  Grenzen vorliegen;
- Dokumentation, Version und Datenformat konsistent sind.

ZF-100, die Darstellung einer Zeichnung als Pinnwand-Vorschau, bleibt eine
gesonderte P2-Integration und blockiert den Zeichen-Kernumfang nicht.

„Absolut zuverlässig“ wird in dieser Planung nicht als unbeweisbare Garantie
verwendet. Gemeint sind konkrete, reproduzierbare Speicher-, Rundlauf-,
Fehler- und Wiederherstellungstests mit offen dokumentierten Grenzen.
