# Manuelle Prüfung – Glide 3.30.0 (verdichtet)

Stand 29.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · ersetzt die bisherigen Listen 3.28, 3.29 und 3.30 · noch nicht ausgeführt

## Kurzantwort: Ist die manuelle Prüfung noch aktuell?

Nur zum kleineren Teil. Die drei alten Listen und der Auszug für Windows
hatten zusammen **201 offene Punkte**. Seitdem sind viele Suiten
dazugekommen:

- Mindestgröße, Kontrast, Hintergrund und Rückmeldungen;
- Seiten, Aufräumen, Kompression, Bilder und feste Bestandteile;
- seit dem 29.09.2026 Logo, Kartenfuß und der Belastungstest.

Sie beantworten die meisten Punkte automatisch. Die Zuordnung jedes alten
Punkts steht im [Anhang](#anhang-zuordnung-der-alten-punkte).

| Einordnung | Anzahl | Bedeutung |
|---|---|---|
| automatisch geprüft | 119 | Eine Suite prüft Verhalten, Daten und Lage. |
| automatisch geprüft, Handgefühl offen | 34 | Die Logik prüft eine Suite; wie es sich mit Maus, Trackpad oder am Bildschirm anfühlt, steckt in Teil A oder B. |
| überholt | 6 | Die Funktion hat sich geändert oder ist entfallen. |
| durch den Inhaber beantwortet | 1 | „Beim Scrollen verschwinden keine Knöpfe“ (Antwort vom 29.09.2026). |
| Frage an den Inhaber | 1 | Fehlt der Wechsel Aufgaben ↔ Notiz im Alltag? (Übersicht vom 29.09.2026) |
| bleibt von Hand | 40 | Nur am echten Gerät, mit echter Hand oder mit fremden Programmen prüfbar – zusammengefasst in 32 Schritten unten; dazu kommt A16 für die Seitenleiste vom 29.09.2026. |

**Was übrig bleibt**, sind fünf Sitzungen:

- A: am Mac, etwa 40 Minuten;
- B: am Windows-PC, nach der Vollprüfung;
- C: Bildschirmleser und Tastatur;
- D: Linux, falls vorhanden;
- E: was nur der Inhaber veranlassen kann.

## Rahmen

- Immer mit einer getrennten Ablage prüfen: `GLIDE_DATA_DIR` auf einen
  Testordner setzen und den
  [Rundgang](../../05_Probelisten_Testdaten/Glide-Rundgang_3.30.0.glidebackup)
  über Datei › Listen/Ordner hinzufügen … einlesen. Ausnahme ist B2, der
  erste Start mit dem echten Windows-Bestand.
- Befunde am besten mit einem Bildschirmfoto nur des Glide-Fensters
  festhalten.

## A. Mac (etwa 40 Minuten)

- [ ] **A1 Programmsymbol:** Glide über `Schnellstart.pyw` starten. Im Dock
      steht das Glide-Symbol (blaue Fläche, weißes „g“), nicht die
      Python-Rakete. Danach `python3 packaging/macos/baue_app.py --ziel
      build/macos` im Repository ausführen und `build/macos/Glide.app`
      starten. Im Dock steht „Glide“ mit Symbol. **Achtung:** Das Bundle nutzt
      die echten Daten.
- [ ] **A2 Logo:** Bei breitem Fenster steht das Logo links neben Titel und
      Unterzeile, auf der Flucht der Seitenleiste. Fenster schmal ziehen: Das
      Logo weicht, der Titel rückt an den Rand. Akzentfarbe wechseln
      (Einstellungen, ganz oben): Das Logo folgt. Auf dem Retina-Bildschirm
      ist es scharf. Klick auf das Logo öffnet „Über Glide“ mit Logo.
- [ ] **A3 Lupe:** ⌕ öffnet die Suche; sie wirkt so schwer wie ⌘ und ⚙.
- [ ] **A4 Arbeitsfläche:** Pinnwand (Spalten), Liste, Tabelle, Seite und
      Zeichnung reichen bis zur Unterkante der Seitenleiste. Der Hinweis
      unten in der Liste ist gut lesbar. Einen Punkt markieren: Die
      Auswahlleiste ersetzt den Hinweis, nichts springt.
- [ ] **A5 Pixel-Werkstatt mit Maus und Trackpad:**
  - Strg+Mausrad zoomt um den Zeiger, die mittlere Maustaste verschiebt.
  - Linie, Rechteck und Ellipse mit Umschalt und Alt ziehen.
  - Rechtsklick malt mit der zweiten Farbe.
  - Schnelle diagonale und kreisförmige Züge haben keine Lücken.
- [ ] **A6 Ziehen mit Maus und Trackpad:**
  - Pinnwandkarten zwischen Spalten ziehen;
  - Bereiche am Kopf ziehen und in der Größe ändern;
  - Zeitblöcke im Stundenraster ziehen;
  - in Seiten Bilder an der Ecke ziehen und in eine andere Spaltenhälfte
    ziehen;
  - Bilder aus dem Finder in Seite und Galerie ziehen;
  - Punkte auf „Mein Tag“ in der Seitenleiste ziehen;
  - den Detailbereich in der Breite ziehen.
- [ ] **A7 Gedrücktes Mausrad:** oben, unten, links und rechts außerhalb der
      Totzone halten; die Fläche läuft selbst und stoppt beim Loslassen.
- [ ] **A8 Systemmitteilungen:**
  - Ansicht › Systemmitteilung testen: macOS fragt einmal nach der
    Erlaubnis, danach erscheint die Probe.
  - Einschalten und eine Erinnerung in zwei Minuten setzen: genau eine
    Mitteilung.
  - Drei zur selben Zeit: eine Sammelmeldung.
  - Aus `Glide.app` gestartet erscheint sie unter „Glide“.
- [ ] **A9 Druck und PDF im Browser:** „Präsentation als PDF …“, „Folien als
      PDF …“ und „Drucken und PDF …“ öffnen, als PDF sichern und lesen. Eine
      Zeichnungskarte ist scharf.
- [ ] **A10 Fremde Programme:**
  - eine Palette `.gpl` in Aseprite oder Pixelorama öffnen und zurück
    importieren;
  - ein Zeichnungs-SVG im Browser und in Affinity oder Illustrator öffnen;
  - nach dem Speichern dort in Glide importieren: verlustfrei oder mit
    verständlicher Ablehnung;
  - eine Seite „Als Markdown speichern …“ und in einem Markdown-Programm
    mit Bildern öffnen.
- [ ] **A11 Tempo, gefühlt:**
  - Pinnwand mit 500 Karten und Galerie mit 100 Bildern: scrollen und ziehen
    bleiben flüssig.
  - Eine lange Seite scrollt endlos und ruhig.
  - Schnell hintereinander abhaken und umbenennen: keine Verzögerung.
  - `Schnellstart.pyw` zweimal starten: Der zweite Start ist spürbar
    schneller.
- [ ] **A12 Zwangsbeenden:** Einen Punkt ändern und Glide sofort hart beenden
      (Aktivitätsanzeige › Sofort beenden). Nach dem Neustart ist die
      Änderung da.
- [ ] **A13 Sichtprüfung der Designs:**
  - Hell, Dunkel, Liquid Glass hell und dunkel, Pixel und Kontrast, je mit
    und ohne Hintergrundverlauf.
  - Fenster vergrößern, verkleinern und die Seitenleiste umschalten: keine
    Kanten, Versätze oder Bildreste; Titel und Hinweise gut lesbar.
  - Gismo im Dopamin-Design zehnmal füttern, spielen, ruhen: nichts wird
    weiß.
- [ ] **A14 Kalender im kleinen Fenster:** Monatsansicht bei 860 × 700;
      Einträge enden mit „…“, volle Tage zeigen „+N“. Diese Texte liegen
      auf einer Zeichenfläche und werden nicht automatisch gemessen.
- [ ] **A15 Globale Suche:** in allen Designs über Startseite, Liste, Pinnwand
      und Seite öffnen. Ecken und Schatten liegen ohne Kasten auf der Fläche
      darunter.
- [ ] **A16 Seitenleiste mit Seiten, Listen und Notizen** (29.09.2026):
  - Reihenfolge Seiten, Listen, Notizen. Der Pfeil klappt seinen Bereich
    ein, der Titel öffnet die Übersicht, „+“ legt an.
  - Den Ordner mit der geöffneten Liste zuklappen, dann einen Punkt abhaken,
    umbenennen und die Ansicht wechseln: Der Ordner bleibt zu.
  - Über einer Bibliothek und einem Notizbuch erscheinen beim Überfahren „+“
    und „…“; „+ › Neuer Unterordner …“ legt einen Unterordner derselben Art
    an.
  - Bei 860 × 700 bleibt die Überschrift „Notizen“ sichtbar, und eine
    geöffnete Notiz zeigt mehrere Zeilen Text.

## B. Windows-PC (nach der Vollprüfung)

- [ ] **B1 Vollprüfung:** nach der
      [Windows-Anleitung](Windows_Pruefung_3.30.0.md) mit Python 3.14.
      Vorher „Immer auf diesem Gerät behalten“ für den Ordner „Glide ToDo“.
- [ ] **B2 Echter Windows-Bestand (Format 17):** Glide 3.30 aus
      `07_Python-Versionen` starten.
  - Der Hinweis „Bestand umgestellt“ erscheint.
  - Im Backup-Ordner liegen `liste_vor_format20_*.json`, gegebenenfalls
    `liste_vor_titelkuerzung_*.json`, und die Meldung „Titel gekürzt“.
  - Listen, Notizen, Papierkorb und Pinnwände sind vollständig.
- [ ] **B3 Design „Pixel“:** Seitentitel und Kachelköpfe in Pixelify Sans,
      Umlaute und ß korrekt.
- [ ] **B4 Skalierung:** 100, 150 und 200 % sowie zwei Monitore. Logo,
      Pixelsymbole und Zeichnungen sind scharf.
- [ ] **B5 Logo und Lupe:**
  - Mit Python 3.14 (Tk 9) ist das Logo glatt; mit 3.13 (Tk 8.6) ist es eine
    Fläche mit harten Kanten.
  - Die Lupe ⌕ ist lesbar; bitte notieren, aus welcher Schrift sie kommt
    (`tests/tools/symbolpruefung.py`).
- [ ] **B6 Startmenü-Verknüpfung:**
  `powershell -ExecutionPolicy Bypass -File packaging\windows\verknuepfung_anlegen.ps1`.
  - „Glide“ mit Glide-Symbol erscheint im Startmenü.
  - Glide startet ohne Konsolenfenster.
  - Das Fenster gruppiert sich in der Taskleiste unter der Verknüpfung.
- [ ] **B7 Hintergrundverläufe:** wie A13, besonders Größenänderung und
      Scrollen ohne Bildreste.
- [ ] **B8 Vorschauen:** JPEG, TIFF, BMP und SVG in der Galerie; HEIC und
      WebP nur mit den Microsoft-Erweiterungen.
- [ ] **B9 Ziehen aus dem Explorer** in Seite und Galerie.
- [ ] **B10 Systemmitteilung:** Mit der ersten Mitteilung erscheint das
      Glide-Symbol im Infobereich; ein Klick holt Glide nach vorn.
- [ ] **B11 Druck und PDF** wie A9.
- [ ] **B12 Beenden mit Alt+F4:** Der nächste Start öffnet in derselben
      Größe und Lage.

## C. Bildschirmleser und Tastatur (VoiceOver bzw. NVDA)

- [ ] **C1** Seitenleiste, Suche, Detailbereich und Anpassen-Modus der
      Startseite sind erreichbar und werden sinnvoll angesagt.
- [ ] **C2 Zeichenfläche:**
  - Mit Tab bis zur Fläche; der gestrichelte Zellcursor ist sichtbar.
  - Die Statuszeile wird angesagt.
  - Pfeiltasten, Leertaste und die Werkzeugtasten wirken.
- [ ] **C3** Bilder in Seiten sind als Fläche erreichbar; der Text liest sich
      ohne Ankerzeichen.

## D. Linux (falls vorhanden)

- [ ] **D1** Design „Pixel“ zeigt die Pixelschrift, ohne dass sie installiert
      ist (Fontconfig).
- [ ] **D2** Vorschauen PNG, GIF und SVG; Logo und Lupe erscheinen.

## E. Nur durch den Inhaber

- Signatur, Notarisierung und Installer.
- Markenprüfung.
- Store-Freigabe.

## Anhang: Zuordnung der alten Punkte

Legende:

- **auto** – automatisch geprüft, die Suite steht dahinter;
- **auto+A/B** – Logik automatisch, Gerätegefühl im genannten Schritt;
- **überholt** – mit Grund;
- **bleibt** – mit Schritt oben.

Die alten Listen liegen unverändert unter
`Checklisten/Archiv/*_vor_Verdichtung_2026-09-29.md`.

### Aus der Liste 3.30

| Bereich | Punkt | Einordnung |
|---|---|---|
| Migration | Format-19-Bestand öffnet, Vorsicherung bytegleich | bereits abgehakt (Kopie des echten Bestands, 25.09.) |
| Migration | Startseite nach dem Update, neue Kacheln aus | auto (`test_features330`) |
| Migration | Start in derselben Fenstergröße und -lage | auto (`test_bilder330`); Alt+F4 → B12 |
| Pixel-Werkstatt | Größen 16–128, Einpassen, Zoom | auto+A5 (`test_drawing330`, `test_features330`) |
| Pixel-Werkstatt | Linie, Rechteck, Ellipse mit Umschalt/Alt | auto+A5 |
| Pixel-Werkstatt | zweite Farbe, X, D, Farbleiste | auto+A5 |
| Pixel-Werkstatt | Symmetrie, Muster, Kachel, über den Rand | auto (`test_drawing330`) |
| Pixel-Werkstatt | Auswahl, Kopieren, Glide-JSON einfügen | auto (`test_drawing330`, `test_features330`) |
| Pixel-Werkstatt | Rückgängig je Aktion | auto (`test_drawing330`) |
| Pixel-Werkstatt | Palette in Aseprite/Pixelorama | bleibt → A10 |
| Pixel-Werkstatt | PNG-Export ohne Glättung | auto (`test_drawing330`) |
| Pixel-Werkstatt | Zwischenstand merken und wiederherstellen | auto (`test_features330`) |
| Pixel-Werkstatt | Pixelsymbol an Liste und Ordner, Skalierung | auto+B4 |
| Startseite | Anpassen, Alt+↑/↓, ganze Breite, Neustart | auto (`test_features330`) |
| Startseite | Seite und Filter anheften, Treffer abhaken | auto (`test_features330`) |
| Seitenleiste | Einklappen, „+“ und „…“, Ziehen | auto (`test_aufraeumen330`, `test_kompression330`, `test_glide`) |
| Suche | Strg/Cmd+O mit Umlauten und ae/oe/ue | auto (`test_features330`); seit 29.09. auch die Lupe (`test_logo330`) |
| Kopf | Pfadzeile anklicken | **überholt**: Die Pfadzeile entfiel am 27.09.2026 |
| Planung | Tagesbeginn und Wochenrückblick | auto (`test_features330`) |
| Pinnwand | Spaltenboard nach jedem Feld, Wirkung in Liste, Tabelle, Kalender | auto+A6 (`test_features330`) |
| Pinnwand | Alt+←/→, „Überfällig“ lehnt ab | auto |
| Pinnwand | 500 Karten flüssig | bleibt → A11 |
| Pinnwand | Karteninhalt, Kartenfarbe, Kontrast | auto (`test_features330`, `test_kontrast330`) |
| Pinnwand | Zeichnung als Karte, „Zurück zur Pinnwand“ | auto (`test_features330`, `test_festlayout330`) |
| Pinnwand | Bereiche ziehen, Größe, F2, entfernen, Rückgängig | auto+A6 |
| Pinnwand | Aufräumen, neue Karte, Verbinden, Verbindung gestalten | auto |
| Pinnwand | Hintergrund bei 50/200 % Zoom, Druck | auto+A11 |
| Pinnwand | Präsentation, blättern, Escape | auto |
| Liste | Gruppieren, zwischen Abschnitten ziehen, Neustart | auto |
| Tabelle | verschachtelt mit Suche | auto |
| Notizbuch | alle Inhaltsarten, Momentdatum, Filter | auto (`test_features330`) |
| Planung | Verknüpfen, „wartet auf“, Zeiterfassung über Neustart | auto |
| Planung | Zeitplan mit Überschneidungshinweis | auto |
| Vorlagen | Platzhalter `{{Projektname}}`, `{{Datum}}` | auto |
| Archiv | Liste und Ordner archivieren und zurückholen | auto |
| Ausbau 25.09. | Blöcke in „Mein Tag“ ziehen, Rückgängig | auto+A6 |
| Ausbau 25.09. | Präsentation als PDF im Browser | auto (Druckseite) + A9 |
| Ausbau 25.09. | Karte mit Maus und Alt+Pfeil, Rückgängig | auto+A6 |
| Ausbau 25.09. | Detailbereich alle Felder, Rückfrage bei „Gruppe“ | auto; Scrollgefühl → A5/A6 |
| Ausbau 25.09. | Gismo in Leerzuständen, „Spielereien aus“ | auto |
| Ausbau 25.09. | Pixelify Sans unter macOS und Windows, Skalierung | auto (Registrierung) + B3/B4 |
| Zweiter Ausbau | Anhänge im Detailbereich | auto |
| Zweiter Ausbau | Raster: Blöcke ziehen, nebeneinander, Doppelklick | auto+A6 |
| Zweiter Ausbau | Zeichnungskarte im PDF scharf | auto (PNG in der Druckseite) + A9 |
| Zweiter Ausbau | Zwischenüberschriften und Nummern | auto |
| Zweiter Ausbau | Windows-Vollprüfung | bleibt → B1 |
| Dritter Ausbau | aus „Ohne Uhrzeit“ und Eingang ins Raster ziehen | auto+A6 |
| Dritter Ausbau | gruppierte Tabelle mit Nummern, Sortierung | auto |
| Dritter Ausbau | „Pinnwand öffnen“ aus der Tabelle | auto |
| Dritter Ausbau | Pixelschrift unter Linux | bleibt → D1 |
| Kleine Fenster | 860 × 700 ohne Anschnitt, Auswahlleiste | auto (`test_mindestgroesse330`, `test_kartenfuss330`) |
| Kleine Fenster | breit: fünf Knöpfe und Anzahl | auto (`test_aufraeumen330`) |
| Kleine Fenster | Schriftgröße „groß“ und Design „Pixel“ | auto (`test_mindestgroesse330`) |
| Kleine Fenster | sortierte gruppierte Tabelle | auto |
| Dialoge | Kalender Monat im kleinen Fenster | bleibt → A14 (Zeichenfläche, nicht gemessen) |
| Dialoge | „In Liste verschieben …“ | auto (`test_mindestgroesse330`) |
| Dialoge | Punktmaske schmal | auto (`test_mindestgroesse330`) |
| Kontrast | Farbwirkung Hell und Glas hell, dunkle Schrift beim Überfahren | auto (`test_kontrast330`); Eindruck → A13 |
| Raster | unter 900 px statt Liste | auto |
| Raster | auf „Mein Tag“ in der Seitenleiste ziehen | auto+A6 |
| Paketierung | `Glide.app` im Dock | bleibt → A1 |
| Verläufe | Verlauf hinter Kopfzeile, Titel lesbar | auto (`test_hintergrund330`); Eindruck → A13 |
| Verläufe | Größenänderung und Scrollen ohne Bildreste | bleibt → A13 |
| Verläufe | Schrift „groß“ und Kontrastdesign | auto (`test_kontrast330`) |
| Verläufe | Windows | bleibt → B7 |
| Rückmeldung 26.09. | Start in hellem Glas mit Verlauf bei schmalem Fenster | auto (`test_hintergrund330`) |
| Rückmeldung 26.09. | Milchglas, Dialog tönt mit | auto (`test_hintergrund330`); Eindruck → A13 |
| Rückmeldung 26.09. | Hinweise ohne Kasten | auto (`test_kontrast330`, `test_rueckmeldung330`) |
| Rückmeldung 26.09. | ◷ und Zahnrad | auto (`test_rueckmeldung330`) |
| Rückmeldung 26.09. | „In Bearbeitung“ in „Mein Tag“ | auto |
| Rückmeldung 26.09. | ruhige Zeichenfläche, Auswahl | auto (`test_rueckmeldung330`) |
| Rückmeldung 26.09. | gleiche Unterkanten | auto (`test_rueckmeldung330`, `test_kartenfuss330`) |
| Zweite Rückmeldung | F2 und „Erweitert“ mit Verlauf | auto (`test_rueckmeldung330`) |
| Zweite Rückmeldung | ruhiger Grund der Dialoge | auto (`test_hintergrund330`) |
| Zweite Rückmeldung | Farben nach Bedeutung | auto (`test_rueckmeldung330`) |
| Zweite Rückmeldung | Papierkorb und „Mein Tag“ ohne Eingabezeile | auto (`test_rueckmeldung330`, `test_kartenfuss330`) |
| Zweite Rückmeldung | „Erledigte Punkte löschen“ | auto |
| Zweite Rückmeldung | Startseite scrollen, keine Knöpfe verschwinden | **beantwortet** vom Inhaber am 29.09.2026 |
| Zweite Rückmeldung | Schnellstart zweimal | bleibt → A11 |
| Seiten | KI-Bericht aus der Zwischenablage | auto (`test_seiten330`) |
| Seiten | lange Seite endlos scrollen | bleibt → A11 |
| Seiten | Tippen „## “, „- “, „/“, Enter | auto (`test_seiten330`) |
| Seiten | Aufgabe abhaken, Fälligkeit, „Mein Tag“, Rückgängig | auto |
| Seiten | als Markdown speichern, anderes Programm | auto (Export) + A10 |
| Seiten | Bibliothek: Eintrag wird Seite | auto |
| Aufräumen | Auswahlleiste erscheint und verschwindet | auto (`test_aufraeumen330`, `test_kartenfuss330`) |
| Aufräumen | ⌘, ↯, ⍾ | auto (`test_aufraeumen330`) |
| Aufräumen | „+“ neben „Listen“, „…“ | auto |
| Aufräumen | Umschalter hervorgehoben | auto |
| Aufräumen | Pinnwand in einer Zeile, Spalten ab 220 px | auto |
| Aufräumen | „Startseite anpassen“ ohne Kasten, Gismo ohne Rechteck | auto (`test_aufraeumen330`) |
| Aufräumen | „Erledigt!“ steigt unten auf | auto (`test_aufraeumen330`) |
| Aufräumen | Akzentfarbe oben, Textlogo folgt | auto (`test_aufraeumen330`) |
| Aufräumen | „Seiten +“, Vorlagen, Seite als Vorlage | auto |
| Aufräumen | Bibliothek exportieren und importieren | auto |
| Aufräumen | Galerie: Bilder, Größen, Großansicht, Rückgängig | auto; JPEG unter Windows → B8 |
| Kompression | erster Start: „Titel gekürzt“ und Sicherung | bleibt → B2 (am Mac seit 27.09. im Einsatz) |
| Kompression | höchstens 40 Zeichen, Zähler | auto (`test_kompression330`) |
| Kompression | keine Beschreibungszeile im Kopf | auto |
| Kompression | Klapppfeile | auto |
| Kompression | Bibliothekstabelle sortieren | auto |
| Kompression | „Notizbuch“ überall | auto |
| Kompression | Notizseite auf einer Linie | auto |
| Kompression | keine gestapelten Hinweise | auto (`test_kompression330`) |
| Tk 9 | Laufzeit Python 3.14 mit Tk 9 | auto (jeder QA-Lauf nennt Tk); Windows → B1 |
| Feste Bestandteile | nichts springt beim Wechseln | auto (`test_festlayout330`, `test_kartenfuss330`) |
| Feste Bestandteile | kein Ordnerpfad über dem Titel | auto |
| Feste Bestandteile | Unterkante, Hinweis darunter auf der Linie der Seitenleiste | **überholt**: seit 29.09. Karte bis unten, Hinweis im Kartenfuß (`test_kartenfuss330`) |
| Feste Bestandteile | Auswahlleiste statt Hinweis, Liste nicht kürzer | auto (`test_kartenfuss330`) |
| Feste Bestandteile | dasselbe schmal und mit großer Schrift | auto (`test_festlayout330`, `test_mindestgroesse330`) |
| Feste Bestandteile | „Mein Tag“: Kennzahlen höchstens zweizeilig | auto |
| Feste Bestandteile | „Zurück zur Pinnwand“ neben dem Titel | auto |
| Feste Bestandteile | Werkzeuge in der Leiste über der Fläche | auto |
| Feste Bestandteile | Designwechsel ohne Kästen | auto (`test_kontrast330`); Eindruck → A13 |
| Bilder in Seiten | PNG, JPEG, HEIC, SVG, breites Bild | auto (`test_bilder330`) |
| Bilder in Seiten | „/“ › Bild und Mehr › Bild | auto |
| Bilder in Seiten | aus dem Finder ziehen, PDF abgelehnt | auto (`test_bilder330`) + A6 |
| Bilder in Seiten | Rahmen, Griff, Ecke ziehen | auto+A6 |
| Bilder in Seiten | Umfluss links, mittig, rechts per Ziehen | auto+A6 |
| Bilder in Seiten | Rechtsklickmenü | auto |
| Bilder in Seiten | Entf, Rückgängig, Alt+Pfeile | auto |
| Bilder in Seiten | Text neben Bild, Umfluss passt sich an | auto |
| Bilder in Seiten | Scrollen ohne Versatz | bleibt → A11 (bekannte Grenze bis 18 px oben) |
| Bilder in Seiten | schmal, breit, Lesebreite | auto |
| Bilder in Seiten | Neustart: Bilder unverändert | auto |
| Bilder in Seiten | Markdown mit Bildordner | auto (Export) + A10 |
| Bilder in Seiten | als Glide-Seite exportieren und importieren | auto |
| Bilder in Seiten | duplizieren, Vorlage | auto |
| Bilder in Seiten | Komplettbackup in leere Ablage | auto |
| Bilder in Seiten | Bildschirmleser | bleibt → C3 |
| Vorschauen | alle Formate je System | auto (macOS, `test_bilder330`); Windows → B8, Linux → D2 |
| Vorschauen | Kachelgrößen scharf | bleibt → A13 |
| Vorschauen | aus Finder/Explorer in die Galerie | auto (macOS); Windows → B9 |
| Vorschauen | Pinnwandkarte mit JPEG-Anhang | auto (`test_bilder330`) |
| Vorschauen | Galerie mit 100 Bildern | bleibt → A11 |
| Systemmitteilungen | anfangs aus | auto (`test_bilder330`) |
| Systemmitteilungen | Probe mit Erlaubnis | bleibt → A8 |
| Systemmitteilungen | eine Mitteilung nach zwei Minuten | bleibt → A8 |
| Systemmitteilungen | Sammelmeldung | auto (Text) + A8 |
| Systemmitteilungen | Windows-Infobereich | bleibt → B10 |
| Systemmitteilungen | ausgeschaltet: nur Hervorheben | auto (`test_bilder330`) |
| Systemmitteilungen | aus `Glide.app` unter „Glide“ | bleibt → A8 |
| „/“-Befehle | Vorschlagszeile, Enter | auto (`test_bilder330`) |
| „/“-Befehle | Tab ergänzt, Escape | auto |
| „/“-Befehle | alle Befehle und Labels | auto |
| „/“-Befehle | „und/oder“, „/xyz“ bleiben Titel | auto |
| Checkliste | wiederkehrend: Häkchen, zurücksetzen, Rückgängig | auto |
| Checkliste | „Alle Punkte wieder öffnen“ | auto |
| Checkliste | Duplikat bleibt wiederkehrend | auto |
| Globale Suche | Lage, Rundung, Schatten | auto (Geometrie); Eindruck in allen Designs → A15 |
| Globale Suche | über allen Ansichten ohne Kasten | bleibt → A15 |
| Globale Suche | Pfeiltasten, Enter, Escape, Klick | auto (`test_features330`, `test_logo330`) |
| Leistung | Fenster erscheint sofort | auto (`test_bilder330`) |
| Leistung | schnell abhaken und umbenennen | bleibt → A11 (Speicherzeiten: `test_speicherlast330`) |
| Leistung | nach Zwangsbeenden gespeichert | bleibt → A12 (Schreibabbrüche: `test_speicherlast330`) |
| Oberfläche | Detailbereich, Auswahl wechseln, unter 980 px | auto+A6 |
| Oberfläche | Leerzustände | auto |
| Oberfläche | „Pixel“, Hell/Dunkel, Kontrast | auto (`test_kontrast330`) |
| Oberfläche | Bildschirmleser | bleibt → C1 |
| Oberfläche | Skalierung und zwei Monitore | bleibt → B4 |

### Aus der Liste 3.29

| Bereich | Punkt | Einordnung |
|---|---|---|
| Anlage | Zeichnung im Inhaltsbereich, im Notizbuch, in Übersichten | auto (`test_features329`, `test_features330`) |
| Anlage | Rückkehr zur Aufgabenliste in gewohnter Reihenfolge | auto (`test_kartenfuss330`) |
| Zeichnen | schnelle Züge ohne Lücken | bleibt → A5 |
| Zeichnen | erster Zug nach dem Öffnen | auto (`test_drawing_prototype`) |
| Zeichnen | über den Rand, Loslassen außerhalb | auto |
| Zeichnen | Füllen, Pipette mit Referenz | auto |
| Zeichnen | Rückgängig je Zelle, höchstens 20 | **überholt**: seit 3.30 je Aktion |
| Tastatur | Tab bis zur Fläche, Zellcursor | bleibt → C2 |
| Tastatur | Pfeile, Werkzeug- und Zoomtasten | auto (`test_features329`) |
| Tastatur | Statuszeile und Ansage | bleibt → C2 |
| Speichern | „Ungespeichert“ → „Gespeichert“, Neustart identisch | auto (`test_features329`) |
| Speichern | sofort wechseln oder schließen | auto |
| Speichern | schreibgeschützter Datenordner | auto (`test_features329`, `test_speicherlast330`) |
| Referenz | laden, einpassen, Größe, Versatz | auto |
| Referenz | nur als Referenz, R | auto |
| Referenz | Nachzeichnen, Rückgängig | auto |
| Referenz | als Anhang, im Komplettbackup | auto |
| Austausch | SVG in Browser, Illustrator, Affinity | bleibt → A10 |
| Austausch | dort gespeichert wieder importieren | bleibt → A10 |
| Darstellung | alle Designs und Größen, DPI, zweiter Monitor | auto (Designs, Größen) + B4 |
| Bestand | Wechsel Aufgaben ↔ Notiz fehlt im Alltag? | **Frage an den Inhaber**, steht in der [Übersicht vom 29.09.2026](../Glide_Uebersicht_und_Entscheidungen_2026-09-29.md) |
| (zwei Hinweise) | Vorsicherung Format 19 beim ersten Start | **überholt**: Format 20 ist umgestellt |
| (Rahmen) | keine Bildschirmaufnahmen möglich | **überholt**: seit 27.09. Aufnahmen des eigenen Fensters |

### Aus der Liste 3.28

| Bereich | Punkt | Einordnung |
|---|---|---|
| Gismo | zehnmal pflegen im Dopamin-Design, nichts wird weiß | bleibt → A13 |
| Gismo | Balken sofort, übrige Karten stehen | auto (`test_features328`) |
| Gismo | in vier weiteren Designs | bleibt → A13 |
| Gismo | Fehlerprotokoll ohne neuen Eintrag | auto (Suiten prüfen das Protokoll) |
| Notizbuch | Ordner, Eintrag, Favorit, Stimmung, Ort, Impuls | auto (`test_features328`, `test_features330`) |
| Notizbuch | Vorlagen Tagesnotiz, Dankbarkeit, Wochenrückblick, Jahr | auto |
| Notizbuch | Suche, Sortierung, Backup, Papierkorb | auto |
| Oberfläche | breit, mittel, minimal ohne Überdecken | auto (`test_vollpruefung325`, `test_mindestgroesse330`) |
| Oberfläche | Felder, Tabelle, Flucht, Kopfaktionen, Werkzeuge | auto |
| Oberfläche | gedrücktes Mausrad | bleibt → A7 |
| Abschluss | OneDrive-Dateien lokal | bleibt → B1 |
| Abschluss | Vollprüfung mit 900 s | bleibt → B1 |
| Abschluss | Ergebnis im QA-Bericht | bleibt → B1 |
| Abschluss | Windows, Python/Tk, DPI im Bericht | **überholt**: gehört zu B1 und B4 |

### Aus dem Windows-Auszug

| Punkt | Einordnung |
|---|---|
| Pixelify Sans | bleibt → B3 |
| Skalierung, zwei Monitore | bleibt → B4 |
| PDF im Browser | bleibt → B11 |
| NVDA | bleibt → C1 |
| Startmenü-Verknüpfung | bleibt → B6 |
