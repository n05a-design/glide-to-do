# Ausbau nach der Funktionsrecherche – Glide 3.32.0

Stand 30.09.2026 · Glide 3.32.0 · Aufgabenformat 20

Grundlage: [Funktionsrecherche vom 30.09.2026](../../../00_Arbeitsvorbereitung/Glide_Funktionsrecherche_Ausbau_2026-09-30.md),
Antwort des Inhabers vom selben Tag:

- Reihenfolge: schnelle Gewinne, Planen, Wissen, Pixel;
- nichts nur für eine Plattform (Mac, Linux, Windows, später iPhone/iPad);
- verschlüsselte Ablage keine Priorität.

Dieser Vertrag wächst mit jeder Etappe um einen Abschnitt. Vertrag 66 bleibt
für 3.30 und 3.31 maßgeblich.

## 1. Etappe 1 – schnelle Gewinne (3.32.0)

### 1.1 Symbol-Export (G16)

- **Wo:** Zeichenfläche › Mehr › „Als Symbol exportieren (ICO)“ › „Grund
  durchsichtig …“ oder „Grund weiß …“.
- **Datei:** ICO mit vier PNG-Bildern (RGBA) in 16, 32, 48 und 256 Pixeln
  (`drawing.ICON_SIZES`, `encode_ico`). So erwartet Windows seit Vista
  PNG-Bilder in ICO-Dateien. macOS, Linux und alle Browser lesen die Datei
  ebenfalls, als `favicon.ico` auch Websites.
- **Grund:** Farbindex 0 (der unbemalte weiße Grund) wird wahlweise
  durchsichtig. Weiß gemalte Zellen gehören dazu, weil die Zeichnung beides
  nicht unterscheidet.
- **Skalieren:** `resample_cells` wiederholt Zellen bei ganzzahliger
  Vergrößerung und nimmt sonst die Zelle unter der Pixelmitte (nächster
  Nachbar). Es entstehen nie Mischfarben.
  - Zeichnungen in 16 oder 32 Zellen passen ohne Verlust.
  - Bei 64 und 128 meldet die Statuszeile „verkleinert ohne Glättung“.
- **Ohne neue Abhängigkeit:** geschrieben mit `struct` und `zlib` aus der
  Standardbibliothek.

### 1.2 Paletten aus Aseprite und Adobe (G20)

- **Wo:** Zeichenfläche › Palette › „Palette importieren (.gpl, .hex, .ase) …“.
- **Formate:** `drawing.parse_binary_palette` unterscheidet am Dateianfang.
  - **Adobe Swatch Exchange** (`ASEF`): Farbfelder in RGB, Grau und CMYK
    (CMYK einfach umgerechnet); Gruppen werden übergangen; Lab wird mit
    Meldung abgelehnt.
  - **Aseprite** (Kennung 0xA5E0): neue Palette (Chunk 0x2019, Farben mit
    Deckkraft 0 fallen weg) oder alte Paletten (0x0004 mit 0–255, 0x0011 mit
    0–63).
  - Gelesen wird nur die Palette, nie Bilddaten.
- **Regeln wie bei Textpaletten:** höchstens 256 Farben, doppelte Farben
  einmal, alles oder nichts. Eine abgeschnittene oder fremde Datei wird mit
  Meldung abgelehnt.

### 1.3 Selbstfüllende Platzhalter (G11)

- **Neu:** Datum und Zeit füllen sich beim Anlegen aus einer Vorlage
  (`template_auto_value`), ohne Dialog. Bisher waren sie nur vorbelegt und
  wurden abgefragt.
- **Namen**, Groß- und Kleinschreibung beliebig:

| Platzhalter | Beispiel am 30.09.2026, 18:05 |
|---|---|
| `{{Datum}}`, `{{Heute}}`, `{{Tag}}` | 30.09.2026 |
| `{{Wochentag}}` | Mittwoch |
| `{{KW}}`, `{{Kalenderwoche}}` | 40 |
| `{{Monat}}` | September |
| `{{Jahr}}` | 2026 |
| `{{Uhrzeit}}` | 18:05 |
| `{{Morgen}}` / `{{Gestern}}` | 01.10.2026 / 29.09.2026 |

- **Abfrage:** Der Dialog erscheint nur noch für die übrigen Platzhalter, etwa
  `{{Projektname}}`. Enthält eine Vorlage nur Datumsfelder, gibt es keinen
  Dialog.
- **Seitenvorlagen** kennen dieselben Platzhalter.
- **Format:** Das Vorlagenformat ändert sich nicht.

### 1.4 Tagesabschluss (G03)

- **Wo:** Ansicht › Ansichten › „Tagesabschluss …“ und in der Suche.
- **Umsetzung:** dritter Modus der Startseite (`day_close`) neben Tagesbeginn
  und Wochenrückblick. Eingebettet, kein Zusatzfenster.
- **Ablauf:**
  1. Offene Punkte, die für heute eingeplant oder heute fällig sind
     (`day_close_queue`), kommen einzeln: Morgen, Nächste Woche, Ohne Tag,
     Erledigt oder Überspringen. „Heute“ entfällt am Abend.
  2. Danach steht, was heute erledigt wurde (`done_at` von heute), mit
     Zählern für weitergegeben und jetzt abgehakt.
  3. „In die Tagesnotiz übernehmen“ hängt den Rückblick an die heutige
     Tagesnotiz (`moment_date` heute); fehlt sie, legt Glide sie an.
     Mehrfacher Abschluss hängt an dieselbe Notiz an.
- **Mitbehoben:**
  - Bei nur zwei Seitenaktionen baute `refresh_page_actions` eine leere,
    gerahmte zweite Leiste.
  - Am Ende des Tagesbeginns standen „Mein Tag öffnen“ und „Zur Startseite“
    doppelt, in der Karte und in der Leiste. Beide Abschlüsse nutzen jetzt
    nur die Leiste.

### 1.5 Prüfung

`tests/integration/test_etappe1_332.py` (55 Suiten) prüft:

- **ICO:** Aufbau, Größen, RGBA, durchsichtiger Grund, keine Mischfarben,
  Skalierung;
- **Paletten:** Aseprite (neue und beide alten Paletten), Adobe (RGB, Grau,
  CMYK, Gruppe) und Ablehnung von Lab, fremden und abgeschnittenen Dateien;
- **Oberfläche:** Export und Import über die Menüs;
- **Platzhalter:** Abfrage nur des Rests; kein Dialog bei reinen
  Datumsfeldern;
- **Tagesabschluss:** Schlange, Entscheidung, Rückblick in derselben
  Tagesnotiz.

## 2. Nächste Etappen

| Etappe | Inhalt | Version |
|---|---|---|
| 2 – Planen | G01 Alltagssprache in der Eingabezeile, G02 Eisenhower-Matrix, G05 Fokus mit Timer | 3.33.0 |
| 3 – Wissen | G08 Seitenverweise, G14 Volltextindex, G09 Titelbild und Galerie | 3.34.0 |
| 4 – Pixel | G19 indizierte Farben, G17 Animation (Format 21) | 3.35.0 |
| danach | G24 KI-Austausch Stufe 2 über Dokumente; Import aus Notion und Todoist | – |
