# Aktuelle startbare Python-Fassung

Glide 3.32.2 · Entwicklungsstand 30.09.2026 · Aufgabenformat 20 · Vorlagenformat 2

[Glide-Aufgaben-und-Listen_v3.32.2.pyw](Glide-Aufgaben-und-Listen_v3.32.2.pyw)
ist die bytegleiche Arbeitskopie des kanonischen Codes
(`01_Repository/Glide/src/glide/app.pyw`). Daneben gehören, ebenfalls
bytegleich, in denselben Ordner:

- die Module `drawing.py`, `drawing_image.py`, `backdrop.py`,
  `page_markdown.py`, `image_preview.py` und `logo.py` – ohne sie startet
  Glide nicht;
- `Schnellstart.pyw` (im Repository `glide_start.py`);
- die Ordner `resources` (Schriften, Vorlagen, seit 29.09.2026 das Logo) und
  `vendor` (tkinterdnd2 für das Ziehen aus Finder und Explorer; fehlt er,
  startet Glide ohne diese Funktion).

Mit Python 3.14 und Tk 9 starten. Mit Python 3.13 und Tk 8.6 startet Glide
ebenfalls, nur ohne Systemmitteilung und SVG-Vorschau; das Logo erscheint
dann als gezeichnete Fläche. Eine laufende ältere Instanz vorher schließen.

## Bytecode

Python übersetzt die Module beim ersten Start und legt den übersetzten Stand
ab. Seit dem 29.09.2026 landet er auch beim direkten Start der `.pyw` im
Cacheordner des Systems, nie mehr hier:

- macOS: `~/Library/Caches/Glide/bytecode`;
- Windows: `%LOCALAPPDATA%\Glide\Cache\bytecode`;
- Linux: `~/.cache/glide/bytecode`.

`Schnellstart.pyw` startet die versionierte Datei als Modul und tat das schon
vorher; ab dem zweiten Start öffnet Glide damit rund eine halbe Sekunde
schneller. Der frühere Ordner `__pycache___Z` stammt aus direkten Starts vor
dieser Änderung und ist zum Löschen markiert.

## Neu in 3.30 (Auszug)

- **29.09.2026:** Logo in der Akzentfarbe links neben dem Titel, in „Über
  Glide“ und als Programmsymbol; Lupe ⌕ für die Suche; Startseite ohne
  Eingabeleiste; Inhaltskarten bis ganz unten; Sicherungen nur bei Änderung
  mit Tagesständen; Startprüfung des Bestands; Bereich „Notizen +“ in der
  Seitenleiste, zugeklappte Ordner bleiben zu.
- **27.09.2026:** Tk 9, Bilder in Seiten, Ziehen aus Finder/Explorer,
  Systemmitteilungen (Option), „/“-Befehle, wiederkehrende Checklisten,
  feste Bestandteile; Seitenbereich, Galerie, Bibliothekstabelle,
  „Notizbuch“ statt „Tagebuch“.
- **26.09.2026:** Seiten und Ordnertypen, Hintergrundverläufe, kleine
  Fenster, Kontrast nach WCAG AA, drei Ausbauten.
- **25.09.2026:** Pixel-Werkstatt, Startseite zum Anpassen, Pinnwand als
  Board, Notizbuch, Planung mit Beziehungen und Zeiterfassung, Design
  „Pixel“.

Vollständig: [Modernisierung 3.30](../01_Repository/Glide/docs/66_MODERNISIERUNG_3.30.0.md).

## Datenformat und frühere Fassungen

Aufgabenformat 20. Einen älteren Bestand stellt Glide seit dem 29.09.2026
gleich beim Start um; vorher entsteht die unveränderte Sicherung
`liste_vor_format20_<Zeitstempel>.json`.

**Ältere Fassungen nie mit dem umgestellten Bestand starten.** Glide 3.29
hält ihn für beschädigt, beginnt leer und überschreibt ihn bei der ersten
Eingabe. Dasselbe gilt für die Zwischenstände von 3.30 vor dem 26. bzw.
27.09.2026: Sie kennen die Listenarten „Seite“ und „Galerie“ nicht. Zurück
geht es nur mit der Vorsicherung in einer getrennten Ablage
(`GLIDE_DATA_DIR`). 3.30 selbst öffnet einen Bestand aus einer neueren
Version nur schreibgeschützt.

Frühere startbare Fassungen liegen zum Vergleich im Unterordner `Archiv`:

| Fassung | Ordner in `Archiv` |
|---|---|
| 3.29.0 | `Glide-Aufgaben-und-Listen_v3.29.0` |
| 3.30.0 vor dem Ausbau (25.09.) | `Glide-Aufgaben-und-Listen_v3.30.0_vor_Ausbau_2026-09-25` |
| vor dem zweiten Ausbau (26.09.) | `…_v3.30.0_vor_Ausbau2_2026-09-26` |
| vor dem dritten Ausbau | `…_v3.30.0_vor_Ausbau3_2026-09-26` |
| vor den kleinen Fenstern | `…_v3.30.0_vor_Mindestgroesse_2026-09-26` |
| vor Kontrast und Paketierung | `…_v3.30.0_vor_Kontrast_und_Paketierung_2026-09-26` |
| vor den Hintergrundverläufen | `…_v3.30.0_vor_Hintergrund_2026-09-26` |
| vor der Rückmeldung | `…_v3.30.0_vor_Rueckmeldung_2026-09-26` |
| vor der zweiten Rückmeldung | `…_v3.30.0_vor_Rueckmeldung2_2026-09-26` |
| vor den Seiten | `…_v3.30.0_vor_Seiten_2026-09-26` |
| vor dem Aufräumen (27.09.) | `…_v3.30.0_vor_Aufraeumen_2026-09-27` |
| vor der Kompression | `…_v3.30.0_vor_Kompression_2026-09-27` |
| vor Tk 9 und Bildern | `…_v3.30.0_vor_Tk9_und_Bildern_2026-09-27` |
| vor Logo und Sicherungen (29.09.) | `…_v3.30.0_vor_Logo_und_Sicherungen_2026-09-29` |
| vor der Rückmeldung vom Abend (29.09.), zugleich Endstand 3.30.0 | `…_v3.30.0_vor_Rueckmeldung_Abend_2026-09-29` |
| Endstand 3.31.0 (30.09.) | `…_v3.31.0_Endstand_2026-09-30` |

Abgelöste Hauptdateien liegen als `Archiv/Glide-Aufgaben-und-Listen_v<Version>_Z.pyw`
zum Löschen durch den Inhaber bereit (seit 30.09.2026: 3.30.0 und 3.31.0);
die vollständigen Stände stecken in den Ordnern darüber.

3.28.0 und älter liegen direkt im Archiv; sie brauchen keine Module. 3.27.0
ist als undokumentierter UI-/UX-Zwischenstand erhalten. Nur mit getrennter
Ablage starten.

Benachrichtigungen funktionieren weiterhin nur bei laufender App.

[Modernisierung 3.30](../01_Repository/Glide/docs/66_MODERNISIERUNG_3.30.0.md) ·
[Zeichnungsseite 3.29](../01_Repository/Glide/docs/65_ZEICHNUNGSSEITE_3.29.0.md) ·
[Prüfstand](../01_Repository/Glide/docs/07_QA_BERICHT.md) ·
[Dokumentationsindex](../01_Repository/Glide/docs/00_INDEX.md)
