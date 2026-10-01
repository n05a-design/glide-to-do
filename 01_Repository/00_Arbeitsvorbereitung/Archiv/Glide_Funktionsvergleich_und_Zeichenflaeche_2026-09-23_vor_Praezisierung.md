# Glide – Funktionsvergleich und Konzept für eine Pixel-Zeichenfläche

Stand 23.09.2026 · Recherche- und Planungsstand · Glide 3.28.0 · Aufgabenformat 18

> **Status dieses Dokuments:** Recherche und fachliche Planung. Die
> Zeichenfläche, die Dateiformate und alle daraus abgeleiteten Erweiterungen
> sind **geplant, nicht umgesetzt**. Dieses Dokument ändert weder App-Version
> noch Datenformat und ist kein Nachweis einer bereits vorhandenen Funktion.

## 1. Auftrag, Quellen und Bewertungsregeln

Diese Untersuchung vergleicht den dokumentierten Funktionsumfang von Glide mit
Todoist, Notion, Microsoft Planner, OneNote, Figma Design, FigJam und Microsoft
Paint. Daraus wird ein belastbares Konzept für eine neue Seitenart
**Zeichenfläche** abgeleitet. Die sechs beigefügten Bilder dienen als visuelle
Inspiration für sichtbare Raster, klare Zellkanten, Pixelmotive, Farbflächen und
Muster. Sie enthalten keine auszuführenden Anweisungen und sind keine technische
Spezifikation.

Für Aussagen über Glide wurden ausschließlich die im Projekt abgelegten
Dokumente ausgewertet. Der Quellcode wurde für diese Untersuchung nicht als
Funktionsnachweis verwendet und die App wurde nicht erneut vollständig geprüft.
Für Wettbewerber wurden aktuelle Hersteller- und Standardquellen verwendet;
Abrufdatum aller Webquellen ist der **23.09.2026**. Preise werden nicht
verglichen. Tarif- oder Plattformgrenzen erscheinen nur, wenn sie die
Funktionsbewertung verändern.

Die folgenden Kennzeichnungen gelten im gesamten Dokument:

| Kennzeichnung | Bedeutung |
|---|---|
| **Dokumentiert vorhanden** | Ein aktueller Glide-Vertrag beschreibt die Funktion. |
| **Eingeschränkt vorhanden** | Die Grundfunktion existiert, aber mit dokumentierten Grenzen. |
| **Widersprüchlich dokumentiert** | Ein älteres Dokument widerspricht einem neueren, spezifischeren Vertrag. |
| **Geplant, nicht umgesetzt** | Fachliche Empfehlung oder künftige Schnittstelle dieses Dokuments. |
| **Nicht belegt** | Die ausgewerteten Quellen reichen für eine belastbare Aussage nicht aus. |

## 2. Dokumentierter Glide-Iststand

### 2.1 Aufgaben, Planung und Ansichten

Glide 3.28.0 ist als deutschsprachige lokale Desktop-Anwendung ohne
Benutzerkonto, eigenen Cloudservice oder notwendige Internetverbindung
dokumentiert. Der aktuelle Bestand umfasst:

- verschachtelte Ordner, Aufgaben, Unterpunkte, Gruppen, Long-Tasks und
  Überschriften;
- Fälligkeit mit Uhrzeit, Wiederholungen, lokale Benachrichtigungen bei
  laufender App, Wichtigkeit, Labels, Checklisten und lokale Anhänge;
- Schnellerfassung, gespeicherte Filter, „Mein Tag“, einen von der Fälligkeit
  getrennten Bearbeitungstag, Aufwandsschätzung und Tageskapazität;
- Listen-, Tabellen-, Reiter-, Kalender-, Label- und Pinnwandansichten auf
  demselben Aufgabenbestand;
- Suche, Papierkorb, Rückgängig, dauerhaften begrenzten Änderungsverlauf,
  Vorlagen und Druckausgabe über eigenständiges HTML.

Benachrichtigungen werden nur verarbeitet, solange die Anwendung läuft.
Glide synchronisiert einen extern gewählten Datenordner nicht selbst. Die
Belegungsdatei hilft gegen erkannte gleichzeitige Nutzung, löst aber keine
Konflikte zwischen noch nicht synchronisierten Kopien.

### 2.2 Notizen und Tagebuch

Seit Aufgabenformat 17 gibt es eigene Notizlisten mit `list_kind: "note"` und
strukturiertem `rich_note`-Inhalt. Der dokumentierte Editor umfasst Rich-Text,
13 Formatierungen, Links, Datum und Zeit, lokale Tastenkürzel, Suche,
Undo/Redo und Autosave. Notizinhalt bleibt bei einem Wechsel des Listentyps
erhalten. Aufgabenbackups und das Glide-Austauschformat bewahren die
strukturierte Notiz; TXT und Markdown enthalten den Text, jedoch nicht alle
Formatierungen.

Aufgabenformat 18 ergänzt Tagebuchordner und datierte Notizseiten. Eintrag und
Ordner können Momentdatum, Favorit, Stimmung, Ortsnotiz und Schreibimpuls
tragen; Rich-Text, Labels und lokale Anhänge verwenden die bestehende
Notizinfrastruktur.

### 2.3 Pinnwand

Die Pinnwand ist eine zusätzliche Ansicht vorhandener Punkte und kein
eigenständiger Aufgabenspeicher. Eine Karte referenziert einen echten Punkt;
Bearbeitungen erscheinen deshalb auch in Liste, Tabelle, Suche und Backup.
Dokumentiert vorhanden sind:

- Listen-, Ordner- und globale Pinnwände;
- freie Kartenpositionen, geordnete Ansicht, drei Kartengrößen, Filter,
  Vollbild und Druck der belegten Fläche;
- Mehrfachauswahl, Lasso, optionale Ausrichtung, Abstands-Guides und
  vorübergehende Unterdrückung des Einrastens mit Alt;
- Zoom von 50 bis 200 Prozent in sechs Stufen und optionaler Navigator;
- Verbindungen als Linie oder mit einer beziehungsweise zwei Pfeilrichtungen;
- höchstens 500 Karten und 200 Verbindungen je Pinnwand;
- Transport zugehöriger Pinnwände in Komplettbackups sowie beim Hinzufügen
  exportierter Listen und Ordner, einschließlich Neuzuordnung der Kennungen.

Pfeile sind eine visuelle Beziehung und keine fachliche Aufgabenabhängigkeit.
Permanente benannte Bereiche, echte gerichtete Abhängigkeiten,
Pinnwand-Reisen und freie Zeichnungsdaten sind weiterhin offen.

### 2.4 Import, Export und Wiederherstellung

Glide dokumentiert TXT-, CSV- und Markdown-Austausch, CSV-Import mit
Spaltenzuordnung, ICS-Import und -Export, ein versioniertes
`.glideexchange`-Format, portable Aufgabenbackups und vollständige
App-Backups. Wichtige Trennlinien:

- `.glideexchange` ist ein Transportformat und ersetzt kein Backup.
- ICS ist Dateiimport beziehungsweise Dateiausgabe, keine
  Kalendersynchronisierung.
- Ein `.glidebackup` ist ein geprüftes ZIP mit Daten und referenzierten
  Anhängen. Vollrestore ersetzt erst nach Validierung und Sicherung.
- Zoom, Werkzeugauswahl und andere reine Arbeitszustände gehören nicht in den
  fachlichen Inhalt einer künftigen Zeichnung.

## 3. Dokumentationskonflikte und verbindlicher Lesestand

Die älteren Analysen bleiben historische Nachweise, sind aber keine aktuelle
Funktionsliste. Für diese Untersuchung gilt bei einem Widerspruch der neuere,
spezifischere Funktions- oder Datenvertrag.

| Ältere Aussage | Aktueller dokumentierter Stand | Konsequenz |
|---|---|---|
| Rich-Text liege außerhalb des Produkts. | Notizlisten mit Rich-Text sind seit Format 17 dokumentiert; Tagebuchseiten verwenden sie in Format 18. | Rich-Text wird nicht erneut als Lücke geplant. Der allgemeine Produktvertrag muss später redaktionell bereinigt werden. |
| Pinnwände seien grundsätzlich kein Aufgabenbackup. | Seit 3.24 reisen zugehörige Pinnwände in Komplettbackups und beim Listen-/Ordnerimport mit. | Die neue Zeichenfläche erhält einen eigenen eindeutigen Backupvertrag. |
| Zoom und Navigator fehlten. | Der 3.26-Entscheidungsstand dokumentiert Zoom 50–200 Prozent und Navigator. | Vorhandene Bedienbausteine werden wiederverwendet statt neu ausgeschrieben. |
| Pinnwandverbindungen seien nur ungerichtet. | Seit 3.24 gibt es `line`, `forward`, `backward` und `both`. | Eine echte Abhängigkeitslogik bleibt trotzdem eine gesonderte Funktion. |
| Ordner- und globale Pinnwände könnten keine neuen Punkte anlegen. | Seit 3.24 wählt die vollständige Punktmaske dort eine Zielliste. | Kein neues Arbeitspaket erforderlich. |
| Freies Zeichnen müsse Teil der Pinnwanddaten werden. | Die geplante Zeichnung hat ein eigenes dauerhaftes Inhaltsmodell. | Sie wird als neue Seitenart geplant und kann später auf Pinnwänden referenziert werden. |

Der QA-Bericht zu 3.28 bezeichnet den Stand als gezielt geprüft, aber nicht
als vollständig releasefreigegeben. OneDrive-Platzhalter, zwei Zeitgrenzen und
offene manuelle Prüfungen verhindern eine weitergehende Aussage. In diesem
Dokument bedeutet „dokumentiert vorhanden“ deshalb nicht automatisch „auf
allen Zielplattformen abschließend abgenommen“.

## 4. Wettbewerbsvergleich

### 4.1 Aufgaben- und Seitenmodelle

| Funktion | Glide-Iststand | Wettbewerberbefund | Praktische Bedeutung | Empfehlung für Glide | Quelle |
|---|---|---|---|---|---|
| Schnellerfassung | Deutsche Fristvorschau und Eingang sind dokumentiert. | Todoist hebt Schnelleingabe, natürliche Datumserkennung, Wiederholungen und Erinnerungen hervor. | Eine Aufgabe muss ohne langen Dialog erfassbar bleiben. | Vorhandene Schnellerfassung bewahren; Zeichenfläche direkt aus dem Neu-Menü erreichbar machen, ohne die Aufgabenerfassung zu überladen. | [Todoist: Funktionen](https://www.todoist.com/de/features) |
| Mehrere Ansichten | Liste, Tabelle, Reiter, Kalender und Pinnwand zeigen denselben Aufgabenbestand. | Todoist wechselt je Projekt zwischen Liste, Kalender und Board; Notion-Datenbanken bieten Tabelle, Board, Timeline, Kalender, Liste, Galerie und Diagramm mit ansichtseigenen Filtern. | Eine neue Ansicht darf keine unbemerkte Inhaltskopie anlegen. | Eine Zeichnung wird eine eigene Seite. Ihre Pinnwandkarte bleibt eine Referenz auf diese Seite. | [Todoist: Funktionen](https://www.todoist.com/de/features), [Notion: Ansichten](https://www.notion.com/help/views-filters-and-sorts) |
| Strukturierte Aufgabenboards | Pinnwandkarten sind frei positionierbare Referenzen auf Punkte. | Planner zeigt Aufgaben unter anderem in Raster-, Board-, Diagramm- und Kalenderansicht; Boardkarten werden nach Feldern gruppiert. | Ein Statusboard und eine freie Zeichenfläche lösen unterschiedliche Probleme. | Aufgabenboard, freie Pinnwand und Rasterzeichnung begrifflich und technisch getrennt halten. | [Microsoft Planner: Plan erstellen](https://support.microsoft.com/en-us/planner/create-a-plan-in-microsoft-planner) |
| Lokale Verfügbarkeit | Kernfunktionen laufen ohne Konto und Internet; Speicherung liegt lokal. | Notion stellt ausgewählte Seiten in Desktop-/Mobilapps offline bereit; Datenbanken sind zunächst begrenzt geladen. Todoist erlaubt Offlineänderungen, warnt aber vor dem Schließen vor abgeschlossener Synchronisierung. | Eine lokal bestätigte Zeichnung muss einen Neustart ohne Netz überstehen. | Sichtbaren Speicherstatus und atomare lokale Speicherung als P0 behandeln. | [Notion: Offline](https://www.notion.com/help/use-pages-offline), [Todoist: Offline](https://www.todoist.com/help/todoist/features/use-todoist-while-offline-4rbaZw) |
| Textbasierter Austausch | Glide besitzt CSV, Markdown und `.glideexchange` mit Vorschau und Grenzen. | Todoist beschreibt CSV-Projektaustausch; Notion exportiert strukturierte Inhalte, aber ein Export ist nicht automatisch eine vollständige Workspace-Wiederherstellung. | Austausch und vollständige Sicherung sind verschiedene Zusagen. | Zeichenprojekt, SVG-Austausch und App-Backup getrennt dokumentieren und testen. | [Todoist: CSV](https://www.todoist.com/help/account-and-billing/security/import-or-export-a-project-as-a-csv-file-in-todoist-YC8YvN), [Notion: Datensicherung](https://www.notion.com/help/back-up-your-data) |

### 4.2 Pinnwand, Zeichnen und Raster

| Funktion | Glide-Iststand | Wettbewerberbefund | Praktische Bedeutung | Empfehlung für Glide | Quelle |
|---|---|---|---|---|---|
| Freie Notizfläche | Pinnwand mit Karten, Beziehungen, Zoom, Navigator, Lasso und Ausrichtungshilfen. | FigJam kombiniert Haftnotizen, Text, Formen, Verbinder, Zeichnung, Bereiche und Seiten. Es ist ein Whiteboard; Figma Design ist ein präziser Objekteditor. | Whiteboard- und Grafikeditor-Bedienung dürfen nicht vermischt werden. | Pinnwand für Beziehungen behalten; Pixelbearbeitung auf einer eigenen Seite anbieten. | [FigJam-Leitfaden](https://help.figma.com/hc/en-us/articles/1500004362321-Guide-to-FigJam) |
| Freihand und Formen | Auf der Pinnwand nicht als Zeichnungsbestand dokumentiert. | OneNote bietet Stifte, Farben, Stärken, Formen, Auswahl, Verschieben, Skalieren, Radierer und Lineal. | Freihandstriche sind kontinuierliche Vektoren; Pixelkunst besteht aus diskreten Zellen. | Erste Stufe zellgenau halten. Stiftdruck und Handschrift später gesondert bewerten. | [OneNote: Zeichnen](https://support.microsoft.com/en-us/onenote/onenote-help-and-learning/draw-and-sketch-notes-in-onenote) |
| Sichtbares Raster | Pinnwand besitzt Ausrichtungshilfen, aber kein Pixelbildmodell. | OneNote kann karierte Hilfslinien zeigen; die Quelle belegt kein zellgenaues Einrasten. Figma Design kann auf das Pixelraster einrasten und zeigt das Pixelraster bei starker Vergrößerung. | Rasteranzeige, Rasterfang und gespeicherte Pixel sind drei verschiedene Dinge. | Diese drei Ebenen separat modellieren und testen. | [Figma: Zoom und Pixelraster](https://help.figma.com/hc/en-us/articles/360041065034-Adjust-your-zoom-and-view-options), [OneNote: Zeichnen](https://support.microsoft.com/en-us/onenote/onenote-help-and-learning/draw-and-sketch-notes-in-onenote) |
| Grundwerkzeuge | Noch kein Pixel-Editor. | Paint dokumentiert Stift, Pinsel, Füllen, Pipette, Text, Formen, Radierer, Auswahl, Zoom und Ebenen. | Ein kleiner, eindeutiger Werkzeugsatz ist für die erste Stufe belastbarer als ein Universal-Editor. | Pixelstift, Radierer, Füllen, Pipette, Linie, Rechteck und Rechteckauswahl zuerst umsetzen. | [Microsoft Paint](https://www.microsoft.com/en-us/windows/paint) |
| Dauerhaft bearbeitbares Projekt | Noch keine Zeichnungsdatei. | Paint unterstützt inzwischen `.paint`-Projektdateien mit editierbarem Projektzustand; die Offenheit des Formats ist nicht belegt. | Eine flache Bilddatei ersetzt kein Projektformat. | Offenes, versioniertes JSON als kanonisches Zeichenmodell festlegen. | [Windows Experience Blog: Paint-Projekte](https://blogs.windows.com/windowsexperience/2025/10/16/new-experiences-currently-rolling-out-for-windows-11/) |
| SVG-Austausch | Noch nicht vorhanden. | Figma kann SVG zwischen Designwerkzeugen austauschen, dokumentiert aber nicht unterstützte SVG-Konstrukte und transformationsbedingte Strukturverluste. | Visuelle Gleichheit beweist keine vollständige Editierbarkeit. | Nur eigene Glide-SVGs mit intakten Projektdaten als verlustfreien Rundlauf zusagen. | [Figma: SVG-Austausch](https://help.figma.com/hc/en-us/articles/360040030374-Copy-assets-between-design-tools), [Figma: Exportformate](https://help.figma.com/hc/en-us/articles/13402894554519-Export-formats-and-settings-for-static-designs) |

### 4.3 Ergebnis des Vergleichs

Glide soll weder Notion als Baukastensystem noch FigJam als kollaboratives
Whiteboard nachbauen. Sein sinnvoller Weg ist eine lokale, klar begrenzte
Pixel-Zeichenfläche mit demselben Anspruch an Backups, Migration und
Wiederherstellung wie Aufgaben und Notizen. Drei Prinzipien folgen direkt aus
dem Vergleich:

1. **Eine fachliche Quelle je Inhalt.** Pinnwandkarten und andere Ansichten
   referenzieren die Zeichenfläche; sie kopieren sie nicht.
2. **Gespeicherte Zellen statt Bildschirmkoordinaten.** Zoom, Fenstergröße
   und Display-Skalierung verändern keine Bilddaten.
3. **Projektformat und Bildausgabe trennen.** JSON sichert Bearbeitbarkeit,
   SVG und PNG dienen dem Austausch beziehungsweise der Darstellung.

## 5. Festgelegtes Konzept der Zeichenfläche

### 5.1 Produktrolle

Die Zeichenfläche wird als dritte Seitenart neben Aufgaben- und Notizseiten
geplant. Der künftige Seitentyp heißt in der technischen Planung `drawing`.
Er ist **keine** freie Dekoration in `settings.json` und **keine** Ansammlung
von Pinnwandlinien. Eine Zeichnung gehört zum portablen Inhaltsbestand und kann
später als referenzierte Vorschau auf einer Pinnwand erscheinen.

### 5.2 Raster und Bildfläche

- Standardgröße: **128 × 128 logische Zellen**.
- Weitere Startvorgaben: 64 × 64 und 256 × 256.
- Jede Zelle ist transparent oder verweist auf eine Farbe der Dokumentpalette.
- Koordinaten beginnen oben links bei `(0, 0)` und sind ganzzahlig.
- Rasterlinien sind reine Darstellung. Das Ausschalten der Linien verändert
  weder Zellen noch Zellfang.
- Pixelwerkzeuge schreiben immer auf logische Zellen. Bei Zwischenpositionen
  werden die übersprungenen Zellen zwischen zwei Eingabepunkten geschlossen,
  damit schnelle Bewegungen keine Lücken erzeugen.
- Vergrößern der Fläche ergänzt transparente Randbereiche. Vor einer
  Verkleinerung zeigt eine Vorschau, ob nichttransparente Zellen abgeschnitten
  würden. Ein bestätigtes Abschneiden ist ein einzelner Undo-Schritt.
- Zoom, Pan, Navigator, sichtbare Rasterlinien und aktive Werkzeugauswahl sind
  Ansichtszustand, nicht Zeichnungsinhalt.

### 5.3 Werkzeuge der ersten Stufe

| Werkzeug | Verbindliches Verhalten der ersten Stufe |
|---|---|
| Pixelstift | Setzt die gewählte Farbe zellgenau; ein gedrückter Zug ist eine Aktion. |
| Radierer | Setzt Zellen auf transparent; kein eigener Hintergrundfarbtrick. |
| Füllen | Füllt einen zusammenhängenden Bereich derselben Ausgangsfarbe innerhalb der aktiven Ebene. |
| Pipette | Übernimmt die sichtbare Farbe einer Zelle; bei Transparenz bleibt die bisherige Farbe erhalten und Transparenz wird gemeldet. |
| Linie | Vorschau während des Ziehens, Rasterung beim Abschließen; danach Pixelbestand. |
| Rechteck | Kontur, optional gefüllt; danach Pixelbestand. |
| Rechteckauswahl | Auswählen, verschieben, kopieren und löschen; Vorschau vor dem Festschreiben. |

Formen werden beim Abschluss in Pixel der aktiven Ebene umgewandelt.
Separat editierbare Vektorobjekte, Textobjekte, Filter, komplexe Mischmodi,
Stiftdruck, Touchgesten und Handschrifterkennung sind **geplant, nicht
umgesetzt** und gehören nicht zur ersten Ausbaustufe.

### 5.4 Ebenen und Farben

Die erste Stufe verwendet einfache Pixelebenen mit stabiler Kennung, Name,
Reihenfolge, Sichtbarkeit und Sperrstatus. Gesperrte Ebenen können ausgewählt,
aber nicht verändert werden. Mindestens eine Ebene bleibt erhalten. Eine
Löschung mit Inhalt verlangt Bestätigung und ist rückgängig zu machen.

Farben werden als normalisierte sRGB-Werte mit Alpha gespeichert. Eine
Dokumentpalette erleichtert Wiederverwendung, begrenzt aber nicht die Anzahl
darstellbarer Farben. Die Hintergrunddarstellung für Transparenz ist eine
Ansichtseinstellung und wird nicht als Pixel gespeichert.

### 5.5 Undo, Autosave und Eingabesicherheit

- Ein zusammenhängender Strich, eine Füllung, ein abgeschlossener Formzug,
  eine Auswahlstransformation oder eine Ebenenaktion bildet genau einen
  Undo-Schritt.
- `Escape` verwirft eine noch nicht abgeschlossene Vorschau. Fokusverlust und
  Loslassen außerhalb der Fläche schließen oder verwerfen die Aktion nach
  einer einheitlichen, getesteten Regel; sie dürfen keinen Dauer-Zeichenmodus
  hinterlassen.
- Autosave wird gebündelt, aber vor Seitenwechsel, Export, Backup und
  Programmende synchron abgeschlossen.
- „Gespeichert“ darf erst erscheinen, wenn die lokale Datei erfolgreich
  ersetzt wurde. Fehler lassen den letzten gültigen Stand bestehen und bleiben
  sichtbar, bis Speicherung erneut gelingt oder bewusst verworfen wird.
- Der dauerhafte Glide-Änderungsverlauf ersetzt den Editor-Undo-Stapel nicht.
  Eine spätere Entscheidung legt fest, ob Undo nach Neustart bewusst endet
  oder als begrenztes Journal fortgeführt wird.

## 6. Daten- und Austauschkonzept

### 6.1 Kanonisches JSON-Zeichenmodell

Das offene, versionierte JSON ist die kanonische Darstellung für
Bearbeitbarkeit. Der folgende Entwurf ist ein **Planungsbeispiel, nicht das
aktuelle Glide-Schema**:

```json
{
  "format": "glide.drawing",
  "format_version": 1,
  "width": 128,
  "height": 128,
  "color_space": "srgb",
  "palette": ["#000000FF", "#FFFFFFFF", "#2B7DE9FF"],
  "layers": [
    {
      "id": "layer-1",
      "name": "Ebene 1",
      "visible": true,
      "locked": false,
      "cells": [
        {"x": 12, "y": 8, "color": 2},
        {"x": 13, "y": 8, "color": 2}
      ]
    }
  ]
}
```

Leere Zellen werden nicht geschrieben. `color` verweist auf einen
Paletteintrag; dadurch bleibt ein typisches Pixelbild kompakt und als Text
diffbar. Vor einer Umsetzung sind Grenzen für Breite, Höhe, Ebenenzahl,
Zellzahl, Palettengröße und Dateigröße festzulegen. Unbekannte Pflichtfelder,
duplizierte Ebenenkennungen, außerhalb liegende Koordinaten und ungültige
Farben müssen den Import vor jeder Bestandsänderung abbrechen.

### 6.2 Glide-SVG

SVG ist XML-basierter Text und kann jede belegte Zelle als Rechteck ausgeben.
Der SVG-Standard erlaubt fremde Namensräume und anwendungsspezifische Daten
ausdrücklich für verlustfreie Rundläufe eines Autorenprogramms. Ein Glide-SVG
kann deshalb gleichzeitig enthalten:

1. eine standardkonforme sichtbare Grafik für Browser und Grafikprogramme;
2. ein versioniertes Glide-Zeichenmodell innerhalb von `metadata`;
3. eine Prüfsumme des eingebetteten Modells und eine Generatorangabe.

Der verlustfreie Import gilt nur, wenn Formatkennung, Version, Prüfsumme,
Abmessungen und sichtbare Darstellung zum eingebetteten Modell passen. Entfernt
ein fremdes Programm die Metadaten oder verändert es die Grafik, wird die Datei
nicht still als vollständig bearbeitbares Glide-Projekt geöffnet. Angeboten
werden dann nur ein klar bezeichneter eingeschränkter Bildimport oder Abbruch.

Der SVG-Parser darf keine Skripte ausführen, keine externen Ressourcen laden,
keine Netzwerkzugriffe auslösen und keine allgemeinen `foreignObject`-Inhalte
rendern. Python weist für nicht vertrauenswürdige XML-Daten ausdrücklich auf
Sicherheitsrisiken hin; Dateigröße, Elementzahl, Verschachtelung und
Textlängen werden deshalb vor der Übernahme begrenzt.

Quellen: [W3C: SVG-Erweiterbarkeit und Roundtrip-Daten](https://www.w3.org/TR/SVG11/extend.html),
[W3C: Metadaten in SVG](https://www.w3.org/TR/SVG11/metadata.html),
[Python: XML-Sicherheit](https://docs.python.org/3/library/xml.html).

### 6.3 PNG

PNG ist eine Bildausgabe für Webseiten, Dokumente und andere Anwendungen.
Transparenz und sichtbare Pixel bleiben erhalten; Ebenen, Sperrstatus,
Palettenreferenzen und andere Projektinformationen sind nicht als vollständiger
Bearbeitungsvertrag zugesagt. PNG-Import erzeugt daher ein neues flaches
Pixelbild oder eine neue Ebene und ersetzt niemals ungefragt ein vorhandenes
Projekt.

### 6.4 Speicherung, Backup und Migration

Das spätere Glide-Datenmodell erhält eine zusätzliche Seitenart `drawing` mit
einem versionierten `drawing`-Dokument. Der Inhalt reist in Komplett- und
geeigneten Teilbackups, beim Duplizieren, im Papierkorb und bei einer
Wiederherstellung mit. Ansichtszustände können separat in Einstellungen liegen,
dürfen aber für die Rekonstruktion des Bildes nicht erforderlich sein.

Vor der ersten schreibenden Migration muss Glide wie bei bisherigen
Formatsprüngen eine unveränderte, unrotierte Sicherung erzeugen. Scheitert die
Sicherung oder Validierung, wird der alte Bestand nicht überschrieben. Ein
Rückwechsel auf eine ältere Glide-Fassung erfolgt nur mit einer getrennten
Originalsicherung; die neue Datei darf nicht von einer alten Version
schreibend geöffnet werden.

## 7. Technische Machbarkeit in der bestehenden Architektur

Die dokumentierte Anwendung verwendet Python, Tk und die Standardbibliothek.
Tk stellt Canvas und Bildobjekte bereit; die Machbarkeit eines Pixel-Editors ist
damit grundsätzlich gegeben. Für eine produktionsnahe Umsetzung sind jedoch
drei Schichten zu trennen:

- **Modell:** logische Zellen, Ebenen, Palette, Validierung und Serialisierung;
- **Editor:** Werkzeuge, Eingabezustand, Auswahl, Undo/Redo und Autosave;
- **Darstellung:** sichtbares Raster, Zoom, Pan, Navigator und Vorschau.

Eine einzelne Canvas-Form pro Zelle wäre bei 256 × 256 Zellen und mehreren
Ebenen unnötig teuer. Der spätere Prototyp soll daher gekachelte oder
bildbasierte Darstellung gegen selektives Neuzeichnen messen. Das fachliche
Modell bleibt unabhängig von dieser Darstellungsentscheidung. Eine neue
Laufzeitabhängigkeit wird erst vorgeschlagen, wenn ein isolierter Prototyp einen
konkreten Nutzen gegenüber Tk/Standardbibliothek nachweist.

## 8. Risiken und bewusste Grenzen

| Risiko | Gegenmaßnahme |
|---|---|
| Fremdprogramm entfernt SVG-Metadaten. | JSON bleibt kanonisch; beim Import Integrität prüfen und Verlust klar melden. |
| Sehr große Bilder oder Füllungen blockieren die Oberfläche. | Harte Dokumentgrenzen, iterative Algorithmen und Leistungstests mit 256 × 256. |
| Schnelle Eingabe lässt Zellen aus. | Linieninterpolation zwischen aufeinanderfolgenden logischen Zellpositionen. |
| Autosave meldet zu früh Erfolg. | Erst nach atomarem Ersetzen als gespeichert markieren; Fehlerzustand persistent anzeigen. |
| Zoom oder DPI verändert das Bild. | Speicherung ausschließlich in logischen Zellkoordinaten; Rundung an einer zentralen Stelle. |
| Aufgaben-, Notiz- und Zeichnungslogik wachsen auseinander. | Gemeinsame Seiten-Lebenszyklen für Duplizieren, Papierkorb, Backup und Wiederherstellung definieren. |
| Unvertrauenswürdiges SVG greift auf externe Inhalte zu. | Strikte Teilmenge parsen; Skript, externe Referenzen und `foreignObject` ablehnen. |
| Barrierefreiheit wird auf Mausbedienung reduziert. | Tastaturweg, sichtbarer Fokus, Statusmeldungen und nichtfarbliche Ebenen-/Werkzeugzustände als Abnahmekriterien. |

## 9. Forschungsfazit

Eine textbasierte, erneut bearbeitbare Speicherung ist umsetzbar. Die stabile
Lösung besteht aus einem offenen JSON-Projektmodell und einem davon abgeleiteten
Glide-SVG mit eingebetteten Projektdaten. SVG allein ist kein verlässlicher
Projektvertrag, sobald die Datei durch fremde Programme gelaufen ist.

Die geplante Zeichenfläche passt zu Glide, wenn sie als lokale, begrenzte und
versionierte Seitenart entsteht. Sie soll die bestehende Pinnwand ergänzen,
nicht deren Aufgabenmodell ersetzen. Die konkrete Umsetzung ist in der
zugehörigen [Aufgabensammlung](Glide_Aufgabensammlung_Zeichenflaeche_2026-09-23.md)
in abhängige, prüfbare Arbeitspakete zerlegt.

## 10. Lokale Quellen

- [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md)
- [Architektur](../01_Repository/Glide/docs/02_ARCHITECTURE.md)
- [Daten, Backups und Migration](../01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md)
- [QA-Bericht 3.28.0](../01_Repository/Glide/docs/07_QA_BERICHT.md)
- [Glide-Austauschformat](../01_Repository/Glide/docs/52_AUSTAUSCHFORMAT_3.23.0.md)
- [Pinnwand als Arbeitsfläche 3.23](../01_Repository/Glide/docs/53_PINNWAND_ARBEITSFLAECHE_3.23.0.md)
- [Navigation und Pinnwand 3.24](../01_Repository/Glide/docs/55_NAVIGATION_UND_PINNWAND_3.24.0.md)
- [Tagebuch und UI 3.28](../01_Repository/Glide/docs/59_TAGEBUCH_UND_UI_3.28.0.md)
- [Entscheidungen und Umsetzungsstand 3.26](../01_Repository/Glide/docs/decisions/Entscheidungen_3.26.0.md)
- [Historische Konkurrenzanalyse 17.09.2026](Glide_Konkurrenzanalyse_2026-09-17.md)
- [Historische Feature-Gap-Analyse 18.09.2026](Glide_Feature_Gap_Analyse_2026-09-18.md)

