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

Die Probe kann ein lokales PNG mit genau 128 × 128 Pixeln laden, hinter der
Zeichnung einblenden und mit der Pipette abtasten. Die Einschränkung ist ein
bewusster Prototypstand. Kopieren in Glides Anhangsordner, beliebige
Skalierung, Deckkraft, Backup und Wiederherstellung folgen erst bei der
produktiven Integration.

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

Der schnelle Repository-Lauf nach der Änderung bestätigt Syntax,
Versionskonsistenz, Dokumentverweise, Tk-Voraussetzung, Zeitzone, den neuen
Zeichnungstest sowie die unveränderten Kern-, Datenintegritäts-, Audit- und
aktuellen Funktionssuiten. Das Gesamtergebnis bleibt wegen bereits im
Ausgangslauf vorhandener Fehler rot: ein altes Release-Backup mit unerwartetem
Schema, nicht reproduzierbare Vorlagendaten, drei ältere UI-Erwartungen und
sieben überholte Standangaben. Der Dokumentationsindexfehler des Ausgangslaufs
wurde bei der ohnehin notwendigen Indexfortschreibung behoben. Protokoll:
`tests/qa-3.28.0/nach_zeichenflaechenkern_2026-09-24/ergebnis.json`.

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
