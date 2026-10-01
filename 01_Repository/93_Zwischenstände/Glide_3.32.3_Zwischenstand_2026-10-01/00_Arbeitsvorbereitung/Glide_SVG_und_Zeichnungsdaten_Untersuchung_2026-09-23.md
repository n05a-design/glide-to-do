# Glide – SVG- und Zeichnungsdaten-Untersuchung

Stand 23.09.2026 · ergänzt 24.09.2026 · Ergänzung zum Funktionsvergleich · Glide 3.28.0 ·
Aufgabenformat 18

> **Hinweis zum Abgleich vom 26.09.2026:** Die Aussagen zur festen Fläche mit
> 128 × 128 Zellen, zum 20er-Zell-Undo und zum begrenzten Werkzeugumfang
> beschreiben den Stand vor Glide 3.30. Seitdem gibt es die Größen 16 bis 128,
> Rückgängig je Aktion sowie Formen und Auswahl. JSON-Format `hex8-row-v1`
> und das Glide-SVG-Profil gelten unverändert. Maßgeblich ist der
> [Vertrag 3.30](../01_Repository/Glide/docs/66_MODERNISIERUNG_3.30.0.md).

> **Status:** Recherche, Formatentwurf und begonnene isolierte Umsetzung.
> Zellmodell, JSON-/Glide-SVG-Export und -Import sowie eine getrennte
> Tk-Bedienprobe sind seit 24.09.2026 implementiert und automatisiert geprüft.
> `ListApp`, produktives Datenformat und bestehende Nutzdaten wurden nicht
> verändert.

## 1. Ergebnis

Ein verlustfrei erneut bearbeitbares **Glide-SVG** ist mit der bestehenden
Python-/Tk-Architektur ohne neue Laufzeitabhängigkeit machbar, wenn Glide nur
ein enges eigenes SVG-Unterprofil akzeptiert.

Glide muss SVG dafür nicht selbst als Vektorgrafik rendern. Der Ablauf lautet:

1. Glide speichert und bearbeitet ein festes 128-×-128-Zellmodell.
2. Der Editor stellt dieses Modell mit Tk dar.
3. Der SVG-Export erzeugt daraus eine skalierbare Standardgrafik und bettet das
   vollständige Modell als Text in `metadata` ein.
4. Der Rückimport liest nur das streng geprüfte Glide-Modell und erzeugt die
   sichtbare Grafik erneut.

Ein allgemeiner Import beliebiger SVG-Dateien ist in der ersten Stufe nicht
vorgesehen. Pfade, Text, CSS, Transformationen, Filter und andere allgemeine
SVG-Konstrukte lassen sich ohne vollwertige SVG-Engine nicht verlässlich in
Zellen zurückwandeln.

## 2. Direkte Prüfung an Glide

### 2.1 Vorhandene Möglichkeiten

- Glide verwendet Python, Tk und die Standardbibliothek.
- Die Anwendung erzeugt bereits heute SVG-Text für Verbindungen in der
  Pinnwand-Druckausgabe, rendert SVG aber nicht innerhalb von Tk:
  [Pinnwand-Druckausgabe](../01_Repository/Glide/src/glide/app.pyw#L4827).
- `json`, `hashlib` und `xml.etree.ElementTree` reichen aus, um das enge Profil
  zu schreiben, zu lesen und zu validieren.
- Eine isolierte Probe mit Python 3.12 erzeugte ein SVG aus einem
  128-×-128-Modell, las es wieder ein, prüfte den Modellhash und rekonstruierte
  alle 16.384 Zellen identisch. Die Probe war kein App-Test und keine
  Releasefreigabe. Sie war eine einmalige Forschungsprobe; ZF-060 muss daraus
  vor der Umsetzung ein dauerhaftes, reproduzierbares Rundlauf-Testprogramm
  mit Testdateien machen.

### 2.2 Relevante Grenze von Tk

Die für Glide dokumentierte Tk-8.6-Laufzeit kann SVG nicht mit `PhotoImage`
anzeigen. Sie unterstützt PNG, GIF und PPM/PGM. Die lokale Architektur hält
diese Grenze ebenfalls fest:
[Arbeitsbegleiter-Entscheidung](../01_Repository/Glide/docs/decisions/ARBEITSBEGLEITER.md#empfohlenes-ausgangsmaterial).

Das blockiert den vorgeschlagenen Rundlauf nicht: Der Editor zeichnet das
Zellmodell selbst. Es blockiert nur den beliebigen Fremd-SVG-Import und die
Verwendung eines SVG als ungeprüftes Referenzbild.

Quellen: [Python 3.12: Tk-Bilder](https://docs.python.org/3.12/library/tkinter.html#images),
[Tk 8.6: Photo image](https://www.tcl-lang.org/man/tcl8.6/TkCmd/photo.htm).

## 3. Bewertung der beiden Speicherideen

Gemessen wurde eine feste Zeichenfläche mit 128 × 128 Zellen und einer
Ebene. Die Werte sind unkomprimierte Näherungswerte; sie dienen der
Formatentscheidung und sind keine Laufzeitmessung der fertigen App.

| Darstellung | Leer | Einfarbig | Schachbrett | Zufällige Farben | Pixelmotiv |
|---|---:|---:|---:|---:|---:|
| XML-Element je Zelle | ca. 325 KB | ca. 325 KB | ca. 325 KB | ca. 325 KB | ca. 325 KB |
| Nach Farbe gruppierte Koordinaten | ca. 0,1 KB | ca. 101 KB | ca. 101 KB | ca. 88 KB | ca. 48 KB |
| Dichte Zahlenmatrix, kompakt | ca. 32 KB | ca. 32 KB | ca. 32 KB | ca. 32 KB | ca. 32 KB |
| 128 Zeilen mit je zweistelligen Hex-Indizes | ca. 32,5 KB | ca. 32,5 KB | ca. 32,5 KB | ca. 32,5 KB | ca. 32,5 KB |
| Zeilenweise Lauflängen | ca. 1,4 KB | ca. 1,4 KB | ca. 96 KB | ca. 85 KB | ca. 4,3 KB |

### 3.1 Konzept 1: zeilenweise speichern

**Bewertung: geeignete Grundlage mit geänderter Codierung.**

Ein eigenes Element für jede Zelle erzeugt hauptsächlich XML-Strukturtext.
Stattdessen erhält jede der 128 Zeilen eine feste Folge von Palettenindizes.
Bei zwei Hexzeichen pro Zelle sind bis zu 256 Farben möglich und jede Zeile
hat exakt 256 Zeichen.

Vorteile:

- feste und vorab bekannte Maximalgröße;
- unmittelbare Entsprechung zwischen Datei und Zeichenfläche;
- keine doppelten oder fehlenden Koordinaten;
- strenge und einfache Validierung;
- eine Farbänderung betrifft genau eine Zeile;
- geeignete Grundlage für Pipette und 4er-Füllung.

### 3.2 Konzept 2: Koordinaten nach Farbe gruppieren

**Bewertung: für sichtbare SVG-Geometrie brauchbar, als internes
Bearbeitungsformat nicht empfohlen.**

Vorteilhaft ist das Konzept nur bei fast leeren Bildern. Bei dichten Bildern
wiederholen sich Koordinaten, und eine Farbänderung muss einen Punkt aus einer
Farbgruppe entfernen und einer anderen hinzufügen. Doppelte Koordinaten,
Überlappungen und Sortierung erzeugen zusätzliche Fehlerfälle. Vor Füllen,
Pipette oder Zeichnen müsste ohnehin wieder eine vollständige Matrix aufgebaut
werden.

### 3.3 Empfohlenes Modell im Glide-Bestand

```json
{
  "format": "glide.drawing",
  "format_version": 1,
  "width": 128,
  "height": 128,
  "color_space": "srgb",
  "palette_id": "glide-drawing-default",
  "palette_version": 1,
  "palette": ["#FFFFFF", "#000000", "#2B7DE9"],
  "encoding": "hex8-row-v1",
  "rows": [
    "0000000000000000000000000000000000000000000000000000000000000000...",
    "0000000000000000000000000202020202000000000000000000000000000000..."
  ]
}
```

Verbindliche Eigenschaften des Entwurfs:

- genau 128 Zeilen;
- genau 128 Palettenindizes je Zeile;
- zwei Hexzeichen je Index;
- höchstens 256 Farben in Version 1;
- stabile `palette_id` und `palette_version`; konkrete Farben reisen trotzdem
  im Dokument mit und werden durch spätere Katalogänderungen nicht ersetzt;
- `palette[0]` ist verbindlich `#FFFFFF`; alle Farben sind deckende,
  sechsstellige sRGB-Hexwerte in Großbuchstaben;
- keine Transparenz und keine Alphawerte in Version 1;
- im Arbeitsspeicher genau 16.384 Palettenindizes;
- eine editierbare Zeichenebene;
- Werkzeug, Zoom, sichtbares Raster und aktuelle Farbe sind kein
  Zeichnungsinhalt.

Im derzeit eingerückten Glide-JSON belegt diese Codierung ungefähr 34 KB je
Zeichnung. Das vorhandene 32-MiB-Limit ist bei einer einzelnen oder einigen
hundert Zeichnungen daher kein unmittelbarer Blocker. Die Zahl ist keine
Zusicherung für beliebig viele Zeichnungen; Gesamtbestand und Verlauf müssen
weiterhin begrenzt und getestet werden.

## 4. Empfohlenes Glide-SVG-Profil

### 4.1 Grundstruktur

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:glide="urn:glide:drawing:1"
     version="1.1"
     width="128"
     height="128"
     viewBox="0 0 128 128"
     preserveAspectRatio="xMidYMid meet">
  <title>Glide-Zeichnung</title>
  <desc>128 × 128 logische Zellen</desc>
  <metadata>
    <glide:drawing version="1">
      <glide:manifest model-sha256="…" artwork-sha256="…"/>
      <glide:model media-type="application/json">
        {"encoding":"hex8-row-v1","format":"glide.drawing",…}
      </glide:model>
    </glide:drawing>
  </metadata>
  <rect x="0" y="0" width="128" height="128" fill="#FFFFFF"/>
  <g id="glide-artwork" shape-rendering="crispEdges">
    <rect x="14" y="8" width="9" height="1" fill="#3366FF"/>
  </g>
</svg>
```

Jede logische Zelle entspricht einer Einheit im SVG-Koordinatensystem. Sie ist
kein physischer Bildschirmpixel. `viewBox="0 0 128 128"` skaliert den logischen
Raum, während `preserveAspectRatio` die Zellen quadratisch hält.

`shape-rendering="crispEdges"` ist sinnvoll, aber laut Standard nur ein
Hinweis an den Renderer. Bei gebrochenen Skalierungsfaktoren kann keine
vollständig identische Abbildung auf physische Displaypixel garantiert werden.

Quellen: [W3C: viewBox](https://www.w3.org/TR/SVG2/coords.html#ViewBoxAttribute),
[W3C: shape-rendering](https://www.w3.org/TR/SVG2/painting.html#ShapeRendering).

### 4.2 Sichtbare Zellen

Die sichtbare Grafik verwendet horizontale Rechteckläufe. Ein Rechteck steht
für unmittelbar benachbarte Zellen derselben Farbe in genau einer Zeile:

```xml
<rect x="14" y="8" width="9" height="1" fill="#3366FF"/>
```

Das ist eine SVG-gültige Weiterentwicklung der zeilenweisen Speicheridee.
`path` wird in Version 1 ausgeschlossen, weil dessen Befehlssprache und
Transformationen deutlich schwerer eindeutig zu prüfen sind. Bei 128 × 128
Zellen ist die zusätzliche Kompression nicht erforderlich.

Quelle: [W3C: rect](https://www.w3.org/TR/SVG2/shapes.html#RectElement).

### 4.3 Bearbeitungsmodell in `metadata`

SVG erlaubt fremde Namensräume und Anwendungsdaten in `metadata`. Das
vollständige, kanonische Glide-Modell kann deshalb im Dokument mitreisen,
ohne gerendert zu werden. Der Inhalt ist weiterhin Text und kann gezielt
kopiert oder bearbeitet werden.

Quellen: [W3C: SVG-Metadaten](https://www.w3.org/TR/SVG/struct.html#MetadataElement),
[W3C: private Daten und Roundtrip](https://www.w3.org/TR/SVG11/extend.html).

### 4.4 Browser, Illustrator und Affinity Designer

Der sichtbare Teil des Glide-SVG besteht ausschließlich aus standardisierten
SVG-Grundelementen und konkreten Farben. Dadurch kann die Datei unabhängig von
Glide:

- in einem modernen Browser angezeigt werden;
- in Adobe Illustrator geöffnet und weiterverarbeitet werden;
- in Affinity Designer geöffnet und weiterverarbeitet werden.

Adobe führt SVG in den unterstützten Illustrator-Formaten. Die Affinity-Hilfe
dokumentiert SVG-Import und -Export. `viewBox` ist browserübergreifend etabliert
und trennt die 128 logischen Zellen von der Ausgabegröße.

Diese Kompatibilität garantiert die **sichtbare Grafik**, nicht den
verlustfreien Rückimport nach einer externen Bearbeitung. Illustrator oder
Affinity dürfen beim Speichern Glides fremden Namensraum entfernen,
Rechteckläufe umformen oder zusätzliche Elemente schreiben. Glide akzeptiert
eine extern gespeicherte Datei deshalb nur dann wieder als bearbeitbares
Projekt, wenn Metadaten, Positivliste, Hashes und semantischer Grafikvergleich
weiterhin vollständig bestehen. Andernfalls bleibt sie eine normale
SVG-Grafik außerhalb des Glide-Projektrundlaufs.

Quellen: [Adobe Illustrator: unterstützte Formate](https://helpx.adobe.com/in/illustrator/desktop/get-started/learn-the-basics/supported-file-formats.html),
[Adobe: SVG-Export](https://helpx.adobe.com/illustrator/using/exporting-artwork.html),
[Affinity Designer 2: Import- und Exportformate](https://affinity.help/designer2/English.lproj/pages/Appendix/fileformat.html),
[MDN: `viewBox`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/viewBox).

## 5. Import und Konfliktbehandlung

Dateiimport und das Einfügen von SVG-Text verwenden dieselbe Prüfroutine:

1. höchstens 4 MiB unkomprimiertes UTF-8-XML;
2. kein SVGZ und kein UTF-16 in Version 1;
3. `DOCTYPE`, `ENTITY` und fremde Verarbeitungsanweisungen vor dem Parser
   ablehnen;
4. Elementzahl, Tiefe, Attribut- und Textlängen begrenzen;
5. jedes Element und Attribut gegen eine Positivliste prüfen;
6. JSON ohne doppelte Schlüssel lesen;
7. Format, Version, 128 Zeilen, Zeilenlänge, Palette und Indizes prüfen;
8. Modell- und Grafikprüfsumme kontrollieren;
9. Vorschau aus dem Modell erzeugen;
10. erst nach Bestätigung eine neue Zeichnung anlegen oder eine vorhandene
    ersetzen.

`ElementTree` lädt keine externe DTD und expandiert externe Entitäten nicht.
Die Python-Dokumentation warnt dennoch vor böswillig großen oder komplexen
XML-Daten. Größen- und Laufzeitgrenzen bleiben deshalb verpflichtend.

Quelle: [Python 3.12: XML-Sicherheit](https://docs.python.org/3.12/library/xml.html).

### 5.1 Erlaubte SVG-Elemente

- `svg`;
- optional einmal `title` und `desc`;
- genau einmal `metadata`;
- die festgelegten Glide-Elemente im Namespace `urn:glide:drawing:1`;
- ein Hintergrundrechteck;
- genau eine Gruppe `g` mit `id="glide-artwork"`;
- darin ausschließlich achsenparallele `rect`-Elemente mit ganzzahligen
  Zellkoordinaten.

### 5.2 Verbotene Inhalte

- `script` und Ereignisattribute wie `onclick`;
- Animationen und Interaktion;
- `foreignObject`, `image`, `audio`, `video`, `iframe` und `a`;
- `use`, `href`, `xlink:href` und URL-Werte einschließlich `data:`;
- CSS, `style`, `class` und XML-Stylesheets;
- `defs`, Filter, Masken, Muster, Verläufe und Marker;
- `transform`, verschachtelte SVGs und unbekannte Elemente;
- allgemeine `path`-Geometrie.

Glide orientiert sich damit am sicheren statischen Verarbeitungsmodus, verlässt
sich aber nicht darauf, dass ein fremder Renderer die Einschränkungen korrekt
durchsetzt.

Quellen: [W3C: Secure Static Mode](https://www.w3.org/TR/SVG/conform.html#processing-modes),
[W3C: SVG-Verweise](https://www.w3.org/TR/SVG/linking.html),
[W3C: SVG-Styling](https://www.w3.org/TR/SVG2/styling.html).

### 5.3 Prüfsummen und Textänderungen

Nicht die gesamte XML-Datei wird als rohe Bytefolge verglichen. Leerraum,
Attributreihenfolge und Namespacepräfixe können sich ohne Inhaltsänderung
ändern.

- `model-sha256` gilt für das normalisierte JSON-Modell.
- `artwork-sha256` gilt für die normalisierte sichtbare Grafik einschließlich
  des weißen Hintergrunds.

Das **kanonische Modell** verwendet diese verbindlichen Bytes:

1. alle Objektschlüssel auf jeder Ebene lexikografisch nach ihren
   ASCII-Namen sortieren;
2. UTF-8 ohne BOM und ohne abschließenden Zeilenumbruch schreiben;
3. zwischen Werten nur `,` und `:` verwenden, ohne zusätzlichen Leerraum;
4. ausschließlich Ganzzahlen in Dezimalschreibweise, Zeichenketten, Arrays
   und Objekte zulassen; keine Gleitkommazahlen und keine doppelten Schlüssel;
5. Farben als eindeutige Großbuchstabenwerte `#RRGGBB`,
   `palette[0] = #FFFFFF`, Zeilenindizes als Großbuchstaben-Hexwerte;
6. den SHA-256-Hash über genau diese UTF-8-Bytes bilden.

Das JSON wird mit einem XML-Schreiber als Textknoten eingesetzt. Zeichen wie
`&` oder `<` werden dabei erst **nach** der Hashbildung XML-escaped. Beim Import
wird zuerst XML-decodiert, dann JSON geparst und anschließend erneut
kanonisiert; XML-Einrückung ist daher kein Bestandteil des Modellhashs.

Für die **kanonische Grafik** erzeugt Glide zuerst genau den Datensatz
`B,0,0,128,128,#FFFFFF` für den Hintergrund. Danach folgen maximal lange,
nichtweiße Rechteckläufe als
`R,<y>,<x>,<breite>,#RRGGBB`, sortiert nach `y` und `x`, jeweils mit `\n`
abgeschlossen. Auch der Hintergrunddatensatz endet mit `\n`. Direkt
benachbarte Läufe derselben Farbe werden vereinigt;
Überlappungen, weiße Läufe im Artwork, zusätzliche Rechtecke und Koordinaten
außerhalb der Fläche sind ungültig. Der Hash entsteht über die UTF-8-Bytes
dieser Zeilenfolge. Beim Import wird die sichtbare SVG-Geometrie in genau
diese Form normalisiert und mit der aus dem Modell erzeugten Folge verglichen.

In der folgenden Tabelle bedeutet „geändert“, dass der aus dem tatsächlichen
Inhalt berechnete Hash vom gleichnamigen Wert im Manifest abweicht. Zusätzlich
erzeugt Glide aus dem eingelesenen Modell die erwartete Grafikfolge und
vergleicht sie semantisch mit den sichtbaren Rechtecken.

| Modell | sichtbare Grafik | Behandlung |
|---|---|---|
| unverändert | unverändert | normaler verlustfreier Import |
| geändert | unverändert | Textänderung als Vorschau zeigen; Grafik aus Modell neu erzeugen |
| unverändert | geändert | Import als Zeichnung ablehnen; vorhandenen Bestand unverändert lassen |
| beide geändert und Grafik entspricht dem neuen Modell | Vorschau aus dem Modell zeigen; nach Bestätigung normalisieren und beide Hashes neu schreiben |
| beide geändert und widersprüchlich | Import abbrechen; vorhandenen Bestand unverändert lassen |
| Metadaten fehlen oder sind ungültig | Import als Zeichnung ablehnen |

Die Hashes erkennen Widersprüche, sind aber keine digitale Signatur und kein
Urhebernachweis. Für wiederholbare JSON-Hashes dient kanonische, kompakte
UTF-8-Ausgabe; [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html) beschreibt
den allgemeinen Ansatz.

## 6. Bezug zum Glide-Datenmodell

Die vier sichtbaren Anlageoptionen sollten intern nicht vier inkompatible
`list_kind`-Werte erzeugen:

| sichtbare Auswahl | gespeicherter Inhaltstyp | bevorzugte Ansicht |
|---|---|---|
| Notizen | `note` | Notizeditor |
| Liste | `tasks` | `list` |
| Zeichnung | `drawing` | Zeichenfläche |
| Pinnwand | `tasks` | `board` |

Damit bleibt **Liste ↔ Pinnwand** ein Ansichtswechsel desselben
Aufgabenbestands. Notiz und Zeichnung sind nach der Anlage nicht konvertierbar.
Neue künftige Inhaltstypen erhalten eine zentrale Fähigkeitstabelle, statt
stillschweigend zu Aufgabenlisten umgedeutet zu werden.

Für `drawing` wird das Zellmodell als typbezogenes Feld im Listenobjekt
geplant. Das passt in den bestehenden Daten-, Ordner-, Papierkorb- und
Backupbestand. SVG bleibt in der ersten Stufe bewusst Austauschformat und wird
nicht zur physischen Primärdatei. Autosave und Backup arbeiten mit dem
Zeilenmodell; SVG entsteht auf ausdrücklichen Export und wird beim Import auf
das validierte Modell zurückgeführt.

Ordner und Tagebuch sind unveränderliche `folder_kind`-Werte. Ein Tagebuch darf
alle registrierten Inhaltsarten enthalten. Jede direkte Seite erhält ein
`journal.moment_date`; die gemeinsame Ansicht sortiert unabhängig vom
Inhaltstyp absteigend danach und bietet Tages- und Zeitraumfilter.

Der dauerhafte Änderungsverlauf speichert keine Zeichnungs-Snapshots. Sein
Listenvergleich erhält nur den SHA-256-Wert des kanonischen Zeichenmodells. Ein
erfolgreicher gebündelter Speichervorgang kann damit einen Eintrag
**„Zeichnung geändert“** erzeugen, ohne 16.384 Zellen oder alte Bildstände in
den Verlauf zu kopieren. Wiederherstellung bleibt Aufgabe von Backup und den
Sicherungen vor einem ersetzenden Import.

## 7. Referenzbild als zweite Anzeigeebene

Eine zweite **editierbare** Ebene ist nicht erforderlich. Bestätigt ist eine
getrennte, nicht editierbare Referenzanzeige:

- PNG wird in Glides Anhangsordner kopiert und über eine stabile Anhangskennung
  mit der Zeichnung verknüpft;
- Anzeige unter oder über dem Zellraster, ein-/ausblendbar;
- Pipette darf aus der Referenzfarbe lesen;
- Referenz wird nicht Teil der gezeichneten SVG-Grafik;
- Duplizieren, Papierkorb sowie vollständiges und passendes Teilbackup führen
  Datei und Verweis gemeinsam;
- allgemeines SVG als Referenz ist mit Tk 8.6 ohne neue Bibliothek nicht
  darstellbar;
- beliebige Skalierung und regelbare Deckkraft des Referenzbilds brauchen
  einen eigenen Prototyp. Tk 8.6 bietet dafür nur begrenzte Bildoperationen.

Der isolierte Tk-Prototyp muss die zulässigen PNG-Abmessungen und die Abbildung
auf das 128-×-128-Raster bestimmen. Falls beliebige Skalierung ohne neue
Abhängigkeit nicht zuverlässig gelingt, darf V1 die Referenzabmessungen
einschränken; die Originaldatei bleibt dabei unverändert im Anhang.

## 8. Bestätigte Produktentscheidungen vom 24.09.2026

1. Quadratische Pinselgrößen: 1 × 1, 2 × 2, 4 × 4 und 8 × 8 logische Zellen.
2. V1-Werkzeuge: Pinsel, 4er-Füllung und Pipette.
3. Höchstens 256 Farben je Zeichnung; eine app-weite Inhaltspalette mit
   möglicherweise 128 Farben wird später versioniert untersucht.
4. Referenzabbildung als lokaler PNG-Anhang einschließlich Backups.
5. Tagebuchordner dürfen alle Inhaltsarten enthalten und erhalten
   Datumssortierung sowie Tages-/Zeitraumsuche.
6. `standard` und `journal` sind nach Anlage nicht konvertierbar.
7. Das Zeilenmodell bleibt Primärspeicher; SVG ist Export- und Rückimportformat
   und muss sich im Browser, in Illustrator sowie Affinity Designer öffnen
   lassen.

## 9. Verbindliche V1-Grenze nach aktuellem Stand

- 128 × 128 logische, beliebig skalierbare Zellen;
- eine editierbare Ebene;
- quadratische Pinselgrößen 1 × 1, 2 × 2, 4 × 4 und 8 × 8;
- 4er-Nachbarschaft beim Füllen;
- Pipette;
- Ein-Drittel-Abdeckung als Trefferregel;
- deckend weißer Hintergrund ohne Transparenz;
- lokaler Editor-Undo-Puffer mit 20 Zelländerungen, auch bei Füllungen;
- automatisches, gebündeltes Speichern im Glide-Bestand;
- eigenes verlustfrei reimportierbares Glide-SVG;
- Anzeige und Sicherung eines lokalen PNG-Referenzanhangs;
- sichtbare SVG-Kompatibilität mit Browser, Illustrator und Affinity Designer;
- PNG-Ausgabe und allgemeiner Fremd-SVG-Import nachrangig;
- Maus und Tastatur zuerst;
- Status: isolierter Datenkern und Bedienprobe **in Umsetzung**; produktive
  Glide-Integration, Migration, Backup und Plattformfreigabe **geplant, nicht
  umgesetzt**.
