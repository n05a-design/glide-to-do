# Zeichenfläche – isolierter Datenkern und Bedienprobe

Stand 24.09.2026 · Glide 3.28.0 · produktives Aufgabenformat weiterhin 18

## Status und Grenze

Der erste Implementierungsschritt ist **isoliert umgesetzt und automatisiert
geprüft**. Er ändert weder `ListApp`, den produktiven Glide-Bestand noch dessen
Datenformat. Die Zeichenfläche ist damit noch keine freigegebene App-Funktion.

Umgesetzt sind:

- `src/glide/drawing.py`: UI-unabhängiges 128-×-128-Zellmodell;
- `src/glide/drawing_prototype.pyw`: eigenständig startbare Tk-Bedienprobe;
- `tests/integration/test_drawing.py`: Modell-, Werkzeug-, Undo-, JSON-, SVG-
  und Sicherheitsprüfungen;
- `tests/integration/test_drawing_prototype.py`: Regressionen für Referenzrahmen,
  Zentrierung, ersten Strich und Farbeingabe;
- Einbindung der neuen Testsuite in `tests/tools/pruefen.py`.

Die Bedienprobe startet mit:

```text
python3 src/glide/drawing_prototype.pyw
```

Sie liest oder schreibt nur Dateien, die ausdrücklich in einem Dateidialog
gewählt werden. `GLIDE_DATA_DIR`, `liste_speicher.json`, Einstellungen,
Anhänge und Backups werden nicht geöffnet.

## Implementierter Zeichenvertrag

- feste Fläche mit 128 × 128 logischen Zellen;
- deckend weißer Hintergrund und höchstens 256 konkrete sRGB-Farben;
- quadratische Pinselbreiten 1, 2, 4 und 8 logische Zellen;
- Ein-Drittel-Flächenregel mit sichtbarer Treffer-Vorschau;
- Interpolation mit acht Zwischenstufen je zurückgelegter logischer Zelle;
- iterative Füllung mit 4er-Nachbarschaft;
- Pipette;
- sichtbares HSV-Farbspektrum mit Helligkeitsregler; direkte Eingabe von
  `#RGB`, `RGB`, `#RRGGBB`, `RRGGBB` und Tk-Farbnamen wird vor dem Zeichnen
  auf `#RRGGBB` normalisiert;
- zellweiser Undo-/Redo-Ring mit 20 Änderungen;
- kanonisches `hex8-row-v1`-JSON mit genau 128 Zeilen;
- SHA-256 über kanonisches Modell und sichtbare Rechteckläufe;
- Standard-SVG aus weißem Hintergrund und maximalen horizontalen
  Rechteckläufen;
- vollständiges Zeichenmodell im Namespace `urn:glide:drawing:1` unter
  `metadata`.

Bei einer manuellen Änderung ausschließlich des eingebetteten JSON-Modells
meldet der Import, dass die sichtbare Grafik neu erzeugt wird. Eine Änderung
nur an der sichtbaren Grafik wird abgelehnt. Stimmen geändertes Modell und
geänderte Grafik überein, können beide nach Prüfung normalisiert werden.

## Sicherheitsgrenzen des SVG-Imports

Der Import akzeptiert ausschließlich das enge Glide-Profil. Abgelehnt werden
unter anderem Skripte, Ereignisattribute, Links, externe Ressourcen,
`foreignObject`, CSS, Pfade, Transformationen, Filter, Masken, Animationen,
DOCTYPE, Entitäten, CDATA, Kommentare und unbekannte Elemente. Vor dem Parser
gilt ein Limit von 4 MiB; Elementzahl, Tiefe, Attribute und Textlängen sind
zusätzlich begrenzt.

Die sichtbare SVG-Grafik verwendet nur standardisierte Grundelemente und kann
deshalb außerhalb von Glide angezeigt werden. Ein erneutes Speichern in einem
Fremdprogramm garantiert den bearbeitbaren Glide-Rückimport nur, wenn
Metadaten und erlaubte Rechteckstruktur erhalten bleiben.

## PNG-Referenz in der Bedienprobe

Die Probe kann lokale PNG-Dateien bis 32 MiB und bis 4096 × 4096 Pixel laden.
Vor der Übernahme zeigt ein Rahmenfenster die feste 128-×-128-Zielgröße. Dort
kann das Bild wahlweise vollständig eingepasst oder flächenfüllend
zugeschnitten, zwischen 25 und 400 Prozent skaliert sowie horizontal und
vertikal verschoben werden. Die Abtastung verwendet bewusst den nächsten
Bildpunkt, damit Referenzfarben deterministisch mit der Pipette übernommen
werden können. Transparente oder außerhalb des Bildes liegende Bereiche werden
in der Referenz weiß dargestellt.

Die gerahmte Referenz bleibt eine zweite, nicht bemalbare Hilfsebene im
Arbeitsspeicher. Sie wird noch nicht mit JSON oder SVG exportiert. Kopieren in
Glides Anhangsordner, Deckkraft, Backup und Wiederherstellung folgen erst bei
der produktiven Integration.

Nach dem Rahmen stehen zwei ausdrücklich getrennte Wege bereit:

- **Nur als Referenz** übernimmt das gerahmte PNG als ein- und ausblendbare
  Hilfsebene und verändert die Zeichnung nicht.
- **Nachzeichnen** erzeugt zunächst eine zweite Vorschau und erst nach der
  ausdrücklichen Übernahme ein neues, vollständig bearbeitbares Zellmodell.

Der Nachzeichner verwendet das feste 128-×-128-Raster und höchstens 64 Farben
einschließlich des weißen Hintergrunds. Ein gewichteter Median-Cut fasst die
Farben ohne externe Bibliothek zusammen. Bildpunkte, deren drei RGB-Kanäle
mindestens die einstellbare Weißtoleranz erreichen, werden zu Hintergrund.
Damit verschwinden leichte Unterschiede eines weißen Bildgrunds, während
ausreichend breite dunkle Konturen als eigene Zellen erhalten bleiben. Dafür
wird jede Zielzelle an 16 gleichmäßig verteilten Teilflächen abgetastet. Sind
mindestens sechs davon dunkel, verwendet die Nachzeichnung gezielt deren
Konturfarbe. Das entspricht mindestens einem Drittel der logischen Zelle und
verhindert, dass eine seitlich liegende Kontur allein wegen einer verfehlten
Mittelpunktprobe verschwindet.

Die Nachzeichnungsvorschau kann ohne Raster, mit jeder einzelnen Zelle oder
mit 8er-Gruppen angezeigt werden. Bei einer bereits begonnenen Zeichnung weist
sie vor der Übernahme darauf hin, dass der aktuelle Inhalt ersetzt wird. Der
reine Referenzweg bleibt davon unberührt.

## Bedienkorrekturen der Probe

- Die Zeichenfläche wird bei jeder Fenster- und Zoomänderung horizontal und
  vertikal zentriert, solange sie vollständig in die Ansicht passt.
- Der Fokusverlust wird nur noch an der Zeichenfläche behandelt. Der erste
  Fokuswechsel beim ersten Ansetzen bricht den laufenden Strich deshalb nicht
  mehr nach dem Anfangspunkt ab.
- Ungültige Farbeingaben erzeugen eine sichtbare Statusmeldung und verändern
  keine Zelle. Das Farbspektrum umgeht die fehleranfällige Handeingabe.

## Geprüfte Anwenderexporte

Die bereitgestellten Dateien `Test.json` und `Test.svg` wurden mit dem
implementierten Importer gegengeprüft. Beide enthalten dasselbe vollständige
128-×-128-Zeichenmodell mit zwei Farben und 757 schwarzen Zellen. Der
kanonische Modellhash ist in beiden Dateien identisch
(`b09580b9b76685cb1081b8167284c86629aa598ca078d6d5c85fe4a2b85d3462`).
Das SVG enthält 321 zusammengefasste sichtbare Rechteckläufe; Modell,
Grafikhash und sichtbare Grafik stimmen überein. Der Import benötigt keine
Reparatur und meldet keine Warnung. Das JSON ist kanonisch und lässt sich
verlustfrei erneut serialisieren.

## Gemessener Stand

Median aus neun lokalen Durchläufen mit Python 3.14.5 auf dem
Entwicklungs-Mac:

| Vorgang | Messwert |
|---|---:|
| Vollfüllung aller 16.384 Zellen | 13,47 ms |
| SVG-Export eines vollständig gefüllten Bildes | 2,04 ms |
| Prüfung und Rückimport desselben SVG | 3,97 ms |
| SVG-Dateigröße in diesem ungünstigen Vollbildfall | 41.638 Byte |

Zusätzlich liefen 50 zufällig erzeugte JSON-/SVG-Rundläufe ohne Abweichung.
Diese Werte belegen den isolierten Kern auf diesem System. Sie sind noch keine
Freigabe für Windows, weitere macOS-Versionen oder die spätere integrierte UI.

Der schnelle Repository-Lauf nach der ersten Kernänderung bestätigt Syntax,
Versionskonsistenz, Dokumentverweise, Tk-Voraussetzung, Zeitzone, den neuen
Zeichnungstest sowie die unveränderten Kern-, Datenintegritäts-, Audit- und
aktuellen Funktionssuiten. Das Gesamtergebnis bleibt wegen bereits im
Ausgangslauf vorhandener Fehler rot: ein altes Release-Backup mit unerwartetem
Schema, nicht reproduzierbare Vorlagendaten, drei ältere UI-Erwartungen und
sieben überholte Standangaben. Der Dokumentationsindexfehler des Ausgangslaufs
wurde bei der ohnehin notwendigen Indexfortschreibung behoben. Protokoll:
`tests/qa-3.28.0/nach_zeichenflaechenkern_2026-09-24/ergebnis.json`.

Der erneute Schnelllauf nach Referenzrahmen, Zentrierung, Fokuskorrektur und
Farbspektrum führt 34 statt zuvor 33 Suiten aus. Beide isolierten
Zeichensuiten, Syntax, Versionskonsistenz, Dokumentation, Tk-Voraussetzung,
Kern, Datenintegrität und die unveränderten aktuellen Funktionsprüfungen sind
grün. Rot bleiben ausschließlich dieselben Ausgangsbefunde: historisches
Fixture, Vorlagenreproduktion, `test_features313`, `test_features322`,
`test_features328` und sieben Standangaben. Protokoll:
`tests/qa-3.28.0/nach_referenzrahmen_2026-09-24/ergebnis.json`.

Am bereitgestellten 400-×-400-Pikachu-PNG erzeugt der Nachzeichner eine
64-Farben-Zeichnung einschließlich weißem Hintergrund. Die mehrfache
Teilflächenabtastung und anschließende Farbverdichtung benötigen auf dem
Entwicklungs-Mac zusammen rund 0,7 Sekunden. Das ist ein Importvorgang und
liegt nicht im zeitkritischen Zeichenpfad. Die visuell geprüfte
Vierfachvergrößerung liegt unter
`tests/qa-3.28.0/nach_nachzeichner_2026-09-24/pikachu_nachzeichnung_4x.png`.

Der erneute Repository-Schnelllauf nach Einführung des Nachzeichners bestätigt
erneut beide Zeichensuiten sowie alle zuvor grünen Glide-Bereiche. Die
anschließend präzisierte Ein-Drittel-Konturabtastung und die getrennten Wege
„Nur als Referenz“ und „Nachzeichnen“ wurden nochmals gezielt grün geprüft.
Die bekannten Ausgangsbefunde bleiben unverändert. Protokoll:
`tests/qa-3.28.0/nach_nachzeichner_2026-09-24/ergebnis.json`.

## Noch nicht umgesetzt

- `list_kind: drawing` im produktiven Schema und die Migration von Format 18;
- automatisches Speichern in `liste_speicher.json`;
- Duplizieren, Papierkorb, Suche, Vorlagen, Teil- und Vollbackup;
- gemischte Inhaltstypen im Tagebuch;
- Öffnen und Speichern der exportierten Datei in Illustrator und Affinity;
- produktive Anhangsverwaltung für PNG-Referenzen;
- app-weite Inhaltspalette mit möglicherweise 128 Farben;
- vollständige Windows-, macOS-, DPI-, Fokus- und Screenreader-Prüfung.

Fachliche Grundlage:
[Funktionsvergleich](../../../00_Arbeitsvorbereitung/Glide_Funktionsvergleich_und_Zeichenflaeche_2026-09-23.md),
[SVG-Untersuchung](../../../00_Arbeitsvorbereitung/Glide_SVG_und_Zeichnungsdaten_Untersuchung_2026-09-23.md) und
[Aufgabensammlung](../../../00_Arbeitsvorbereitung/Glide_Aufgabensammlung_Zeichenflaeche_2026-09-23.md).
