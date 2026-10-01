# Manuelle Prüfung – Glide 3.29.0

Stand 24.09.2026 · Glide 3.29.0 · Aufgabenformat 19 · noch nicht ausgeführt

Diese Prüfung ergänzt die weiterhin offene
[manuelle Prüfung 3.28](Manuelle_Pruefung_3.28.0.md). Sie erfolgt mit einer
Kopie oder einem isolierten `GLIDE_DATA_DIR`, nicht mit dem einzigen echten
Datenbestand. Beim ersten Start mit echten Daten prüfen, dass im Ordner
`backups` die Datei `liste_vor_format19_<Zeitstempel>.json` entsteht.

In der Agentenumgebung waren keine Bildschirmaufnahmen möglich. Die Darstellung
wurde nur über Fenster- und Widgetgeometrie sowie automatisierte Tests geprüft.

## Anlage und Einbettung

- [ ] „Datei → Neu anlegen → Neue Zeichnung“ öffnet die Fläche **im
      Inhaltsbereich**, ohne zusätzliches Fenster.
- [ ] „Neue Liste …“ mit Listenart „Zeichnung“ in einem normalen Ordner und in
      einem Tagebuchordner anlegen; im Tagebuch erscheinen Datum, Favorit,
      Stimmung und Ort über der Fläche.
- [ ] Ordner- und Tagebuchübersicht zeigen die Zeichnung mit ▩ und „Zellen
      bemalt“ bzw. Momentdatum.
- [ ] Beim Wechsel zu einer Aufgabenliste stehen Eingabezeile, Suche, Baum und
      Fußleisten wieder in gewohnter Reihenfolge.

## Zeichnen mit Maus oder Trackpad

- [ ] Schnelle diagonale und kreisförmige Züge mit allen vier Pinselgrößen:
      keine Lücken, rote Vorschau entspricht den gefärbten Zellen.
- [ ] Erster Zug direkt nach dem Öffnen der Seite zeichnet vollständig.
- [ ] Zug über den Flächenrand hinaus und Loslassen außerhalb: kein hängender
      Pinsel.
- [ ] Füllen trennt diagonal berührende Flächen; Pipette übernimmt Farben der
      Zeichnung und – bei eingeblendeter Referenz – der Referenz.
- [ ] Strg/Cmd+Z nimmt Zellen einzeln zurück, höchstens 20.

## Tastatur und Zugänglichkeit

- [ ] Tab bis zur Fläche; der gestrichelte Zellcursor ist sichtbar.
- [ ] Pfeiltasten, Umschalt+Pfeil, Leertaste, B/F/I, 1/2/4/8, +/−/0, G, R, C.
- [ ] Die Statuszeile nennt Werkzeug, Farbe, Zelle, Zoom und Speicherzustand;
      Screenreader-Ansage unter Windows (Sprachausgabe) und macOS (VoiceOver)
      notieren.

## Speichern und Fehlerfall

- [ ] Nach einigen Strichen wechselt der Status kurz auf „Ungespeichert“ und
      danach auf „Gespeichert“; Glide beenden und neu starten: Bild identisch.
- [ ] Unmittelbar nach einem Strich die Seite wechseln oder Glide schließen:
      der letzte Strich ist nach dem Neustart vorhanden.
- [ ] Datenordner schreibgeschützt setzen: Status „Speichern fehlgeschlagen“,
      keine Dialogflut, keine beschädigte Datei.

## Referenz und Nachzeichnung

- [ ] „Mehr → PNG-Referenz laden …“ mit einem großen Foto und einem kleinen
      Symbolbild; Rahmen füllen/einpassen, Größe, Versatz.
- [ ] „Nur als Referenz“: blasse Hilfsebene, Zeichnung unverändert, R blendet
      aus und ein.
- [ ] „Nachzeichnen …“: Weißtoleranz und Rastervorschau; Übernahme ersetzt die
      Zeichnung; „Rückgängig“ bzw. „Nachzeichnung zurücksetzen“ holt sie zurück.
- [ ] Referenz-PNG erscheint in den Anhängen der Seite; nach Komplettbackup und
      Wiederherstellung in leerem Datenordner ist die Referenz wieder sichtbar.

## Austausch und Darstellung

- [ ] „Mehr → Als SVG exportieren …“ im Browser, in Adobe Illustrator und
      Affinity Designer öffnen: weißer Hintergrund, quadratische Zellen,
      richtige Farben.
- [ ] Die Datei in Illustrator/Affinity erneut speichern und in Glide
      importieren: Ablehnung mit verständlicher Meldung oder verlustfreie
      Übernahme; der Bestand bleibt unverändert, wenn abgelehnt wird.
- [ ] Alle Designs (Standard hell/dunkel, Glas, Dopamin, Kontrast, Minimal)
      sowie 860 × 700, 1280 × 860 und Vollbild sichten; Hoch-DPI und zweiter
      Monitor unter Windows und macOS.

## Geänderte Bestandsfunktion

- [ ] Der Bearbeiten-Dialog zeigt Listen- und Ordnerart nur noch an. Prüfen,
      ob der frühere Wechsel Aufgaben ↔ Notiz im Alltag fehlt; falls ja, als
      eigene Produktentscheidung neu aufnehmen.
