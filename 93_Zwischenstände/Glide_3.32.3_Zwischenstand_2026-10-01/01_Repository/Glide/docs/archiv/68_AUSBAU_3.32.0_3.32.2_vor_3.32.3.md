# Ausbau nach der Funktionsrecherche – Glide 3.32.0

Stand 30.09.2026 · Glide 3.32.2 · Aufgabenformat 20

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

### 1.5 Hänger nach „Über Glide“ (dringend, 30.09.2026)

- **Meldung des Inhabers:** Nach „Über Glide“ friert Glide ein und muss
  zwangsbeendet werden.
- **Beleg:** macOS-Berichte `glide-python_2026-09-29-231826` und
  `…_2026-09-30-071942` (8,5 s ohne Rückmeldung). Der Hauptthread steckt
  in dieser Kette:
  1. `NSMenuTrackingSession … _performPostTrackingDismissalActions`: macOS
     führt den Menüpunkt aus, die Menüverfolgung läuft noch.
  2. Darin Glides Befehl, der ein modales Fenster öffnet und mit
     `wait_window` wartet (`Tcl_DoOneEvent` → `mach_msg`).
  3. Die innere Warteschleife bekommt keine Ereignisse mehr, weil macOS erst
     nach der Rückkehr des Menübefehls weitermacht.
- **Warum R11 das nicht abfing:** Seit 29.09.2026 wurden nur Einträge mit „…“
  verschoben. Eine Probe über alle Menüpunkte fand 13 ohne „…“, die ein
  Fenster öffnen:
  - Neue Liste, Neuer Ordner, Seite aus Zwischenablage;
  - Wo liegen meine Daten?, Standardordner benutzen;
  - Kopieren (Hinweis), Einfügen, Erledigte Punkte löschen;
  - Als Reiter öffnen, Auf Pinnwand anheften;
  - Tastenkürzel anzeigen, Fehlerprotokoll öffnen, Über Glide.

  Dazu kommt „Beenden“ (`::tk::mac::Quit`) mit Rückfrage.
- **Behebung:** `defer_window_menu_commands` verschiebt jetzt **jeden**
  Menübefehl (`add_command`, `insert_command`) in den nächsten Leerlauf, in
  der Menüleiste wie in Kontextmenüs. Häkchen und Auswahlpunkte bleiben
  unmittelbar: Sie setzen nur Werte, und die Auswahlfelder der Dialoge
  (`tk.OptionMenu`) verlassen sich darauf. Ein erster Versuch, auch sie zu
  verschieben, ließ drei Suiten scheitern. `::tk::mac::Quit` ruft `on_close` ebenfalls im
  Leerlauf auf.
- **Prüfung:**
  - `test_befunde330` prüft, dass kein Befehl, auch „Über Glide“, innerhalb
    des Menüaufrufs läuft, alle danach folgen und ein Häkchen sofort wirkt.
  - `test_glide` und `test_ui_updates` warten nach `invoke` einen Leerlauf ab.
  - Nachstellen mit echten Mausklicks auf die Menüleiste gelang nicht
    zuverlässig (AppleScript drückt Menüpunkte ohne Menüverfolgung). Die
    Probe mit echter Maus bleibt Punkt A18 der manuellen Prüfliste.

### 1.6 Hänger beim Öffnen einer Seite mit Bildern (30.09.2026)

- **Meldung:** Glide hing beim Öffnen einer Seite mit Bildern; danach meldete es
  „Es ist ein Fehler aufgetreten“.
- **Protokoll:** Um 08:13:39 scheiterten binnen einer Sekunde flache Rückrufe
  (`sync_backdrop_surfaces`, `draw_icons`, `_recolor_tree`) mit
  `RecursionError`. Keiner ruft sich selbst auf – der Stapel war vorher schon
  voll.
- **Nachgestellt:** Seite mit zwei Bildern (Umfluss und mittig), öffnen,
  wechseln, Fenstergröße ändern, scrollen. Die Stapeltiefe erreichte 992 in
  `place_origin`. Der Kreis, 123-mal hintereinander:
  `place_images` → `place_at` → `place_origin` → `update_idletasks()` →
  `yscrollcommand` des Textfelds → `place_images` …
- **Ursache:** `place_origin` misst, wo `place` im Textfeld ansetzt, und merkte
  das Ergebnis erst nach der Messung, und zwar je Innenabstand. Die Lesespalte
  ändert ihren Innenabstand mit jeder Breite. So wurde beim Öffnen und
  Vergrößern ständig neu und verschachtelt gemessen.
- **Behebung:** Einmal je Programmlauf wird gemessen, *ob* Tk den Innenabstand
  mitzählt (`PageEditor._padding_counts`). Danach wird gerechnet. Während der
  Messung liefert eine erneute Anfrage sofort die Rechnung
  (`_measuring_origin`). Stapeltiefe im selben Ablauf: 16.
- **Geprüft:** Alle übrigen `update()`- und `update_idletasks()`-Aufrufe (28)
  stehen in Dialogaufbau, Seitenaufbau oder Knopfaktionen, nicht in einem
  Rückruf, der sich selbst wieder auslöst.
- **Suite:** `test_etappe1_332` wiederholt den Ablauf und verlangt eine
  Stapeltiefe unter 80.

### 1.7 Prüfungen im Hintergrund (30.09.2026)

- **Wunsch des Inhabers:** Prüfläufe sollen nicht jedes Mal Fokus und Maus
  nehmen.
- **Umsetzung:** `tests/tools/hintergrund/sitecustomize.py` kennzeichnet unter
  macOS jedes Tk-Hauptfenster der Suiten als „Zubehör“ (kein Dock-Symbol,
  keine Menüleiste) und gibt den Vordergrund zurück (`deactivate`).
  `focus_force` wird zu `focus_set`. Glide selbst bleibt unverändert.
- **Anbindung:** `pruefen.py` setzt das unter macOS als Standard
  (`GLIDE_QA_HINTERGRUND=1`, PYTHONPATH); `--vordergrund` schaltet es ab.
- **Probe:** Mit dem Modus blieb das vorn arbeitende Programm vorn, ohne ihn
  kam Python nach vorn. Fenster werden gezeichnet und lassen sich
  fotografieren; sie können über anderen Fenstern erscheinen, nehmen aber
  weder Tastatur noch Maus.
- **Vollprüfung vom 30.09.2026 im Modus:** Keine Suite scheiterte am
  fehlenden Vordergrund.

### 1.8 Prüfung

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
| vorab | D08 Klappkorrektur 3.32.1; D04 Drag-and-drop in bestehenden Seiten-/Notizbereichen; Stabilität der Bildseite/Formatleiste gezielt reproduzieren; P01–P07 aus der Arbeits- und Featureplanung: messen, Schriften/Helfer bündeln, besonders Bibliotheksaufbau und Layout-Rückrufe reduzieren | – |
| 2 – Planen | G01 Alltagssprache in der Eingabezeile, G02 Eisenhower-Matrix nach D02, G05 Fokus mit vorhandener Zeiterfassung, G29 Einzelaufgaben im Notiz-/Seitentext bei getrennten Inhaltstypen (D05), G31 Seitenaufgabe über IDs verschieben; G32 nur Filter „aus Seiten“ und Aktualisierung ergänzen (Kopfzähler existieren) | 3.33.0 |
| 3 – Wissen | G08 Seitenverweise mit G30 (Verweise auf Listen und Aufgaben), G14 Volltextindex, G09 Titelbild und Galerie, G28 Liste in Seite einbetten | 3.34.0 |
| 4 – Pixel | G19 Palettenbearbeitung und Undo (indizierter Kern existiert), G17 Animation; Mehrbild-GIF nachweisen, D07 beachten; Schema beim ersten inkompatiblen Inhalt anheben | 3.35.0 |
| danach | G24 KI-Austausch Stufe 2 über Dokumente; Import aus Notion und Todoist | – |
| zurückgestellt | G25 Toolkit-/Mobile-Probe: D03 setzt den Fokus auf die vorhandene Desktop-Anwendung | – |

**Planungsnachtrag 30.09.2026:**
[Recherche, Codebefunde, Entscheidungen und Arbeitsablauf](../../../00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md).
G04 (Stundenraster mit Ziehen) ist bereits vorhanden. Unbekannte interne
Links/Einbettungsblöcke können alte Leser verwerfen; G08/G28/G30 prüfen daher
das Datenformat vor der Umsetzung. Format 21 ist nicht ausschließlich für
Animation reserviert. Zielversionen und Aufwände sind Planung, keine Freigabe.
Die Performance-Abschlussaufgabe steht wörtlich am Ende der Arbeitsplanung.

## 3. Stabilitätskorrektur 3.32.1 – Klappmechanismen (D08)

[Vertrag und Kontrollmatrix](69_KLAPPKONTROLLE_3.32.1.md): Label-Pfeilklicks,
native Öffnungsreihenfolge, globale Zustände, Auswahl in geschlossenen
Vorfahren, Tastatur der Bereichspfeile und verschachtelte Bibliotheken.
Datenformat bleibt 20. D01–D06 gelten nach den aktuellen Inhaberantworten;
D07 bleibt nach Begriffserklärung offen. Mobile/Toolkit-Probe zurückgestellt,
Hinweisgestaltung unverändert. D04 ist in 3.32.2 umgesetzt; Einzelaufgaben im Notiztext folgen gemäß Arbeitsplanung.

## 4. Drag-and-drop und erster Performance-Schnitt 3.32.2

[Drag-and-drop und Performance 3.32.2](70_DRAG_UND_PERFORMANCE_3.32.2.md) dokumentiert D04, Schriften-/Layoutcache, gemeinsamen Hover, echte Bedienproben und unprofilierte Vorher-/Nachher-Werte. P02 umgesetzt, P01/P03/P05 teilweise; Karten-Neuerzeugung, Bildlayout und Speicheraktualisierung bleiben nächste Performance-Schritte. Zielversion 3.33 bleibt die Planungsfeatureetappe, ohne Inhaltstypen allgemein zu konvertieren.
