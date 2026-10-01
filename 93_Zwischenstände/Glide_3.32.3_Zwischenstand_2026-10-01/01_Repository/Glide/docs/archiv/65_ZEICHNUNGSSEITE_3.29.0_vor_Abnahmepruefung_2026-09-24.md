# Zeichnungsseite 3.29.0 – produktive Integration, Etappe 1

Stand 24.09.2026 · Glide 3.29.0 · Aufgabenformat 19 · Einstellungen 2 · Vorlagen 2

## 1. Status und Grenze

Mit 3.29.0 ist die Zeichnung eine **eigene, unveränderliche Listenart** im
normalen Glide-Bestand. Umgesetzt ist die mit dem Auftraggeber am 24.09.2026
vereinbarte **Etappe 1**: ZF-015, ZF-020, ZF-080 und ZF-090 aus der
[Aufgabensammlung](../../../00_Arbeitsvorbereitung/Glide_Aufgabensammlung_Zeichenflaeche_2026-09-23.md)
einschließlich PNG-Referenz als Anhang, Vorher-Snapshot für die Nachzeichnung
und der Tastaturbedienung aus ZF-070.

Ausdrücklich **nicht** Teil dieser Etappe und weiterhin offen:

- ZF-120 vollständig: Aufgabenlisten und Pinnwände im Tagebuch, Tages- und
  Zeitraumfilter. Tagebuchordner nehmen jetzt Notizen **und Zeichnungen** auf;
  beide sortieren nach Momentdatum.
- die Anlageoption „Pinnwand“ als `tasks/board` (`preferred_view`);
- ZF-100 Pinnwandvorschau einer Zeichnung, ZF-210 app-weite Palette;
- Plattform-, DPI-, Mehrmonitor- und Screenreader-Abnahme (ZF-110);
- Öffnen und erneutes Speichern des Exports in Illustrator und Affinity.

Eine erfolgreich geprüfte Python-Fassung ist kein signiertes Release.

## 2. Bedienung

**Anlegen.** „Neue Liste …“ mit Listenart *Zeichnung*, „Datei › Neu anlegen ›
Neue Zeichnung“ oder das Kontextmenü einer Liste oder eines Ordners („Neue
Zeichnung in diesem Ordner“). In einem Tagebuchordner entsteht
„Zeichnung · TT.MM.JJJJ“ mit heutigem Momentdatum; der Kopf mit Datum, Favorit,
Stimmung und Ort erscheint wie bei Tagebuchnotizen.

**Eingebettete Fläche statt Extrafenster.** Die Zeichnung erscheint im
Inhaltsbereich der Seite, an der Stelle des Aufgabenbaums. Eingabezeile, Suche,
Ansichtsumschalter sowie Hinweis-, Aktions- und Fußleisten werden auf einer
Zeichnungsseite ausgeblendet und beim Seitenwechsel in ursprünglicher
Reihenfolge zurückgeholt. Titel, Beschreibung, Labels und Anhänge bleiben im
Seitenkopf bzw. im Bearbeiten-Dialog.

| Bereich | Bedienung |
|---|---|
| Werkzeuge | Pinsel, Füllen (4er-Nachbarschaft), Pipette |
| Pinselgrößen | 1×1, 2×2, 4×4, 8×8; rote Vorschau zeigt exakt die nach der Ein-Drittel-Regel getroffenen Zellen |
| Farbe | Farbfeld oder „Farbe“: Spektrum mit Helligkeit, Direkteingabe `#RGB`, `#RRGGBB` oder Tk-Farbname, Farben der Zeichnung als Schnellwahl |
| Rückgängig | ↶/↷ bzw. Strg+Z, Strg+Y, Strg+Umschalt+Z auf der Fläche: letzte 20 Zelländerungen einzeln |
| Ansicht | −/+ zoomt (2–12 Bildschirmpixel je Zelle); bis zum ersten manuellen Zoom passt sich die Fläche dem Fenster an; „Raster“ ab Zoom 3 |
| Tastatur | Pfeile bewegen den Zellcursor, Umschalt+Pfeil acht Zellen; Leertaste/Enter wendet das Werkzeug an; B/F/I, 1/2/4/8, +/−/0, G (Raster), R (Referenz), C (Farbe), Escape beendet einen Zug |
| Status | eine Textzeile: Werkzeug, Größe, Farbe, Cursorzelle mit Farbe, Zoom, Undo-Stand, Speicherzustand – ohne Farbcodierung verständlich |
| „Mehr“ | PNG-Referenz laden, neu rahmen, nachzeichnen, entfernen; Nachzeichnung zurücksetzen; Export SVG/JSON; Import ersetzen; Jetzt speichern; Zeichnung leeren |

**PNG-Referenz.** Das gewählte PNG (höchstens 32 MB und 4096 × 4096 Pixel,
Signaturprüfung) wird wie jeder Anhang als lokale Kopie in `attachments/`
abgelegt und mit der Seite verknüpft. Der Rahmen-Dialog bietet „Fläche füllen“
oder „Ganzes Bild zeigen“, Größe 25–400 % und Versatz ±128 Zellen. Danach:

- **Nur als Referenz**: blasse, nicht bemalbare Hilfsebene hinter weißen Zellen.
  Die Pipette liest die unverblasste Originalfarbe. Das Zellmodell bleibt
  unverändert.
- **Nachzeichnen …**: zweite Vorschau mit Weißtoleranz 220–255 und
  Rasteranzeige; erst „Nachzeichnung übernehmen“ ersetzt das Modell (höchstens
  64 Farben einschließlich Weiß).

Fehlt die Referenzdatei (etwa nach Kopie eines Datenordners ohne Anhänge),
meldet die Statuszeile das; die Zeichnung bleibt unverändert.

**Austausch.** Export als Glide-SVG oder kanonisches JSON über einen atomaren
Schreibweg; Nutzdatendateien sind als Ziel ausgeschlossen. „Datei ›
Importieren › Zeichnung (SVG/JSON)“ legt standardmäßig eine **neue** Seite an.
„Mehr › importieren und ersetzen“ ersetzt nach Rückfrage und ist rückgängig
machbar. Eine abgelehnte Datei verändert keinen Bestand.

## 3. Datenvertrag Format 19

Neue Felder am Listenobjekt, ausschließlich bei `list_kind == "drawing"`:

| Feld | Inhalt |
|---|---|
| `drawing` | kanonisches Zellmodell `glide.drawing` Version 1 (`hex8-row-v1`, 128 Zeilen, Palette mit Weiß an Index 0, höchstens 256 Farben) aus [`drawing.py`](../src/glide/drawing.py) |
| `drawing_reference` | `null` oder `{attachment_id, mode, zoom_percent, offset_x, offset_y}`; `attachment_id` zeigt auf einen Eintrag in `attachments` derselben Liste |

Regeln:

- Zentrale Typregistrierung `LIST_KINDS` (`tasks`, `note`, `drawing`) mit
  Fähigkeit `accepts_items`. Zeichnungen nehmen keine Punkte auf; eine Datei mit
  Punkten in einer Zeichnung wird abgelehnt statt still bereinigt.
- Eine **unbekannte Listenart in einem Format-19-Bestand** wird sichtbar
  abgelehnt (`check_list_kind`). Format 18 und älter werden wie bisher gelesen;
  deren Schreiber kannten nur `tasks` und `note`.
- Ungültige Zellmodelle werden beim Laden, Import, Austausch und aus dem
  Papierkorb mit Titel der Seite abgelehnt.
- Ein entfernter Referenz-Anhang löscht den Verweis; eine nur fehlende Datei
  lässt den Verweis bestehen.
- Zoom, Werkzeug, Farbe, Raster, Tastaturcursor, Referenzsichtbarkeit und der
  Vorher-Stand einer Nachzeichnung sind **Sitzungsansichtszustand** und werden
  nicht gespeichert.
- Listen- und Ordnerart sind nach der Anlage fest. Der Bearbeiten-Dialog zeigt
  die Art nur an; `_apply_page_details` schreibt sie nicht mehr. Das entspricht
  der bestätigten Produktentscheidung und entfernt den bis 3.28 möglichen
  Wechsel Aufgaben ↔ Notiz sowie Ordner ↔ Tagebuch.
- Der Eingang bleibt immer eine Aufgabenliste.

**Migration.** Vor dem ersten Speichern einer älteren Datei entsteht
unrotiert und bytegleich `backups/liste_vor_format19_<Zeitstempel>.json`.
Scheitert die Sicherung, wird nicht gespeichert. Glide 3.28 und älter lesen
Format 19 nicht. Referenz: `tests/fixtures/current_v19/reference_v19.json`.

## 4. Speichern (ZF-020)

- Zellstriche verändern zunächst nur das Modell des Editors. 700 ms nach dem
  letzten Strich überträgt `DrawingEditor.flush` das kanonische Dokument über
  `store_drawing` in den Bestand; `save_items` schreibt wie jede Glide-Änderung
  über temporäre Datei, `fsync` und atomaren Austausch.
- Offene Striche werden außerdem vor jedem globalen Rückgängig-Punkt
  (`snapshot_undo`), vor Seitenwechsel, Export, Backup, Vorlagenaufnahme,
  Austausch und Programmende (`flush_rich_note`) übertragen und beim
  Fokusverlust der Fläche gesichert.
- Zustände: *Ungespeichert*, *Speichert …*, *Gespeichert*, *Speichern
  fehlgeschlagen – Änderungen bleiben erhalten* (in der Gefahrenfarbe und im
  Text). Ein Schreibfehler zeigt keinen modalen Dialog je Autosave; der letzte
  gültige Dateistand bleibt unverändert, der nächste Strich oder „Mehr › Jetzt
  speichern“ versucht erneut. Fehler landen im Fehlerprotokoll.
- Zwanzig schnelle Zelländerungen erzeugen genau einen Schreibvorgang
  (automatisiert geprüft).
- Der Änderungsverlauf speichert nur den SHA-256 des kanonischen Modells und
  meldet „Zeichnung · geändert“. Aufeinanderfolgende Änderungen derselben Seite
  innerhalb von zehn Minuten bilden einen Eintrag, dessen Zeit nachgeführt
  wird. Diese Zusammenfassung gilt ebenso für wiederholte Notizspeicherungen.

## 5. Rückgängig

- Zellstriche verwenden ausschließlich den 20er-Zellpuffer des Editors.
- Strukturaktionen – Nachzeichnen, Referenz laden/entfernen, Ersetzen durch
  Import, Nachzeichnung zurücksetzen, Leeren – laufen durch
  `apply_drawing_change` und legen einen vollständigen globalen Vorher-Snapshot
  mit Markierung `drawing_restore` an. Rückgängig stellt dann Modell, Referenz
  und Anhangsliste zurück.
- Ein globales Rückgängig einer **anderen** Aktion übernimmt das aktuelle
  Zellmodell aller Zeichnungen (`snapshot_keeping_drawings`). Ohne das hätte ein
  älterer Stand spätere Striche still verworfen.
- Strg+Z auf der fokussierten Fläche ist immer Zell-Undo.

## 6. Architektur

| Baustein | Rolle |
|---|---|
| `src/glide/drawing.py` | unveränderter UI-unabhängiger Vertrag aus dem isolierten Kern |
| `src/glide/drawing_image.py` | neu: aus der Bedienprobe ausgelagerte Tk-Bildfunktionen (`render_framed_reference`, `render_trace_reference`, `quantize_reference`, `model_to_photo`, `normalize_ui_color`) samt Grenzwerten |
| `DrawingEditor` in `app.pyw` | eingebettetes Widget im Glide-Stil; Darstellung als **ein** vergrößertes `PhotoImage`, Änderungen schreiben nur ihre Zellausschnitte |
| `sync_drawing_view` | Gegenstück zu `sync_rich_note_view`; läuft am Ende jedes `_refresh_tree` |
| `hide_drawing_chrome` / `restore_drawing_chrome` | idempotentes Aus- und Einblenden der Leisten mit gemerkter Packreihenfolge |
| `store_drawing`, `apply_drawing_change`, `snapshot_keeping_drawings` | Autosave, Strukturaktionen, Rückgängig-Semantik |
| `drawing_reference_frame_dialog`, `drawing_trace_preview_dialog`, `drawing_color_dialog` | themed Dialoge über `run_modal` |

`app.pyw` legt seinen eigenen Ordner an den Anfang von `sys.path` und
importiert `drawing` und `drawing_image`. Die startbare Kopie in
`07_Python-Versionen` enthält deshalb beide Module neben der `.pyw`-Datei.
Neue Laufzeitabhängigkeiten gibt es nicht.

Die Pinnwand-Arbeitsfläche kennt Zeichnungen nicht: `Workspace.context()` liefert
für Zeichnungsseiten keinen Bereich, `eligible_lists` schließt Zeichnungen aus.
Schnellerfassung, Punktmaske, „In Liste verschieben“, Ablegen auf Ordner und
CSV-/ICS-Anhängen schließen Zeichnungen als Ziel aus; `require_list_view`
blockiert Punktaktionen auf einer Zeichnungsseite.

## 7. Transportwege

| Weg | Verhalten |
|---|---|
| Duplizieren | Modell und Referenzverweis werden kopiert; der Anhang wird wie bei jeder Liste mitgeführt |
| Papierkorb / Wiederherstellen | vollständiges Listenobjekt samt Zeichnung |
| Komplett-, Teil- und App-Backup | Zeichnung im `data.json`, Referenz-PNG als referenzierter Anhang |
| Additiver Import | neue Listen- und Anhangskennungen; `remap_import_attachments` führt `drawing_reference.attachment_id` nach |
| Vorlagen | eine aus einer Zeichnung aufgenommene Vorlage erzeugt wieder eine Zeichnung (Import über denselben Backupweg) |
| Austauschformat | optionales Feld `drawing`; unbekannte Listenarten und Punkte in Zeichnungen werden abgelehnt; die PNG-Referenz reist als Datei nicht mit |
| TXT, Markdown, Druck | eine Zeichnung hat keine Punkte und erscheint dort ohne Inhalt |

## 8. Behobene Ausgangsbefunde des Prüfstands

| Befund | Ursache | Korrektur |
|---|---|---|
| Fixture `glide_releaseplanung_3.26.0` | Zuordnung Version → Format kannte Format 17 (3.26/3.27) und 18 (3.28) nicht | Zuordnung in `pruefen.py` ergänzt |
| Vorlagenerzeuger nicht reproduzierbar | `journal.moment_date` wurde aus der Erzeugungszeit abgeleitet und nicht stabilisiert | Momentdatum auf den Anker 11.09.2026 gesetzt, Katalog neu erzeugt |
| `test_features313` | Schalter „Nur offene Punkte“ ist seit 3.27 entfernt | Test prüft jetzt, dass ein Restwert nicht filtert |
| `test_features322` | Ansichtsumschalter zeigt seit 3.27 nur Ziele, nicht die aktive Ansicht | Test erwartet „Liste“ und „Pinnwand“ in der Tabellenansicht |
| `test_features328` | eigene Menüzeile existiert nur unter Windows | Erwartung plattformabhängig |
| Reproduktion Beispiel-/Releasedaten (Vollmodus, seit 3.26 unentdeckt) | Abgleich wertete die Listenzeitpunkte `created_at`/`updated_at` als Inhalt | wie `exported_at` ausgenommen; Momentdatum relativ zum Exporttag verglichen |

## 9. Prüfung

Neue Suite `tests/integration/test_features329.py` (Details im
[Test-README](../tests/README.md)). Messungen auf dem Entwicklungs-Mac mit
Python 3.14.5: ein Pinselzug mit 50 Mausereignissen einschließlich
Teilneuzeichnung rund 76 ms; bei 1280 × 860 erhält die Fläche 922 × 616 Pixel,
beim Minimalfenster 860 × 700 noch 502 × 420 Pixel. Ergebnisse des Gesamtlaufs
stehen im [QA-Bericht](07_QA_BERICHT.md).

Manuell offen: echte Maus-/Trackpadbedienung auf macOS und Windows, Hoch-DPI und
Mehrmonitor, Screenreader-Ansage der Statuszeile, Sichtprüfung aller Designs
(Bildschirmaufnahmen waren in der Agentenumgebung nicht möglich) sowie der
Illustrator-/Affinity-Rundlauf.

## 10. Bekannte Grenzen

1. Der Vorher-Stand für „Nachzeichnung zurücksetzen“ lebt nur in der Sitzung;
   dauerhaft bleibt der globale Rückgängig-Schritt bis zum Programmende.
2. Beim Ersetzen einer Referenz verlässt der alte PNG-Anhang die Seite; die
   Datei bleibt bis zu einer Bereinigung im Anhangsordner.
3. Die Referenz wird bei jedem Öffnen der Seite neu gerahmt (einige
   Zehntelsekunden bei großen PNGs); ein Zwischenspeicher fehlt.
4. Suche findet Zeichnungen über Titel, Beschreibung, Labels und
   Tagebuchangaben, nicht über Bildinhalt.
5. Vorlagen für Zeichnungen erscheinen im Anlagedialog unter den Listenvorlagen;
   die gewählte Vorlage bestimmt dann die Art.
