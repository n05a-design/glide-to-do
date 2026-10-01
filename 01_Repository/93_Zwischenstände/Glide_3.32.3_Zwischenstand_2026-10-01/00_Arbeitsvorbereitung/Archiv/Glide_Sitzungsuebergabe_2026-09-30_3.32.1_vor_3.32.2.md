# Glide – Übergabe an eine neue Sitzung

Stand 30.09.2026 · Glide 3.32.1 · Aufgabenformat 20 · für den nächsten Chat oder Bearbeiter

Dieses Dokument ist der Einstieg für jede neue Sitzung. Es ersetzt nicht die
Verträge; es sagt, wo was steht, was gilt und was als Nächstes ansteht.

**Neu nach den Antworten D01–D08:**
[Arbeits- und Featureplanung](Glide_Arbeits_und_Featureplanung_2026-09-30.md)
führt D01–D06 als entschieden, D07 nach Erklärung als offen. D08 ist die
Klappkorrektur 3.32.1 mit neuer Pflichtsuite und
[Kontrollmatrix](../01_Repository/Glide/docs/69_KLAPPKONTROLLE_3.32.1.md).
Mobile/Toolkit-Probe zurückgestellt; Hinweise unverändert; bestehende Bereiche
um Ziehen erweitern; einzelne Aufgaben in Notizen/Seiten. Die Performance-
Pakete und Bild-/Formatleistenbefunde bleiben zur nächsten Umsetzung offen.

## 1. In fünf Sätzen

- Glide ist eine lokale Aufgaben-, Notiz- und Seiten-App in Python mit Tk 9
  (eine Datei `src/glide/app.pyw` mit rund 54.000 Zeilen, dazu sieben Module).
- Der aktuelle Stand ist **3.32.1**:
  - Etappe 1 der Funktionsrecherche: Symbol-Export, Paletten, Platzhalter,
    Tagesabschluss;
  - zwei behobene Hänger: Menüleiste und Seite mit Bildern;
  - Klappzustände, Label-Pfeilklick und verschachtelte Bibliothek korrigiert;
  - Pflichtsuite mit echten Bedienwegen und Callbackfehler-Erfassung;
  - Prüfungen laufen im Hintergrund.
- Der Inhaber startet Glide **nur** aus `07_Python-Versionen` oder aus
  `01_Repository/Glide/build/macos/Glide.app`. Eine Änderung ist erst bei ihm,
  wenn beide abgeglichen sind.
- Entscheidungen trifft der Inhaber über datierte Dokumente in
  `00_Arbeitsvorbereitung`, mit Nummern und je einer Empfehlung.
- Antworten und Dokumente sind auf Deutsch.

## 2. Wo was liegt

| Was | Wo |
|---|---|
| Code | `01_Repository/Glide/src/glide/` (`app.pyw`, `drawing.py`, `drawing_image.py`, `backdrop.py`, `page_markdown.py`, `image_preview.py`, `logo.py`, `glide_start.py`) |
| Startbare Fassung des Inhabers | `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.32.1.pyw` plus Module, `resources`, `vendor` |
| macOS-Bundle | `01_Repository/Glide/build/macos/Glide.app` (Kennung `de.shaye.glide`, nie ändern; Windows `Shaye.Glide`) |
| Verträge | `docs/66_MODERNISIERUNG_3.30.0.md` (3.30, 3.31: Abschnitte 2.17, 2.18), `docs/68_AUSBAU_3.32.0.md` (ab 3.32) |
| Entscheidungen | `00_Arbeitsvorbereitung/Glide_Funktionsrecherche_Ausbau_2026-09-30.md` (G01–G32, Q1–Q5), `Glide_Rueckmeldung_und_Entscheidungen_2026-09-29.md` (R1–R11), `Glide_Uebersicht_und_Entscheidungen_2026-09-29.md` (B, E, F, I) |
| Prüfstand | `docs/07_QA_BERICHT.md`, `tests/qa-verlauf.md`, Protokolle unter `tests/qa-<Version>/` |
| Manuelle Prüfliste | `00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.30.0.md` (gilt auch für 3.32.1; zusätzliche Klappkontrolle im Vertrag 69) |
| Projektübergabe (technisch) | `docs/09_PROJECT_HANDOFF.md`, Entwicklungsnotizen `docs/DEV_NOTES.md` |
| Pflegewerkzeuge | `scripts/pflege/` (Versionswechsel, Abgleich nach 07, Messung, Codeanalyse; siehe README dort) |
| Fehlerprotokoll des Inhabers | `~/Library/Application Support/Glide/fehlerprotokoll.txt` – nur mit Erlaubnis lesen, nur Fehlereinträge |

## 3. Regeln, die immer gelten

- **Nichts löschen.**
  - Überholtes bekommt die Endung `_Z`; der Inhaber löscht selbst.
  - Vor jeder Änderung eines bestehenden Dokuments eine Kopie im
    benachbarten `archiv/` anlegen (`<Name>_<Version>_vor_<Anlass>.md`) und im
    Index `docs/00_INDEX.md` nachweisen.
- **Echte Daten nur als Kopie und nur mit Erlaubnis.**
  - Tests und Messungen immer mit temporärem `GLIDE_DATA_DIR`.
  - Originale nie verändern.
- **Fotos nur vom eigenen Glide-Fenster** (`screencapture -l <Fensternummer>`),
  nie vom Bildschirm.
- **Plattformunabhängig:** Mac, Linux, Windows, später iPhone/iPad; keine
  Funktion nur für eine Plattform; keine neue Laufzeitabhängigkeit ohne
  Entscheidung.
- **Form folgt Funktion:**
  - keine Fläche ohne Aufgabe, keine doppelten Wege oder Symbole;
  - Kanten fluchten;
  - Funktionen leben eingebettet in der Seitenansicht, nicht in
    Zusatzfenstern;
  - Seitenleiste, Kopf und Inhaltsfläche springen nie.
- **Farben nach Bedeutung:**
  - Rot nur Löschen, Grün nur Bestätigen, festes Lila für Hinzufügen und Neu,
    Gelb für Hinweise, sonst neutral;
  - die Regeln stehen in `BUTTON_ROLE_RULES`; Knöpfe nie von Hand einfärben.
- **Jede Runde bekommt eine Version** (Werkzeug `scripts/pflege/versionswechsel.py`).
  **Erst nach Abgleich** (`abgleich_07.py`, `baue_app.py`, SHA-256) gilt etwas
  als erledigt.

## 4. Technische Stolperfallen (teuer gelernt)

- **Menübefehle unter macOS:**
  - Jeder `add_command`/`insert_command` läuft über
    `defer_window_menu_commands` erst im nächsten Leerlauf.
  - Ein modales Fenster direkt aus dem Menübefehl friert die App ein (Hänger
    29./30.09.).
  - Tests, die `menu.invoke()` rufen, müssen danach `update()` ausführen.
  - Häkchen und Auswahlpunkte bleiben unmittelbar.
- **Kein `update()` oder `update_idletasks()` in Rückrufen, die sich selbst
  wieder auslösen können** (Scroll-, Configure- oder Leerlauf-Rückrufe).
  - Die Bildplatzierung in Seiten lief so in einen Kreislauf bis zum
    `RecursionError` (Vertrag 68, 1.6).
  - Ein `RecursionError` in flachen Rückrufen im Fehlerprotokoll heißt: Der
    Stapel war vorher voll; nach verschachteltem `update` suchen.
- **Tk 9:**
  - `place` im Textfeld zählt den Innenabstand (`place_at`, `place_origin`);
  - `<TouchpadScroll>` packt X und Y in ein Wort;
  - ausgepackte Rahmen malt macOS nicht immer neu (`repaint_sidebar`).
- **Tempo:** Die Vergleichsliste kostet im erneuten `test_tempo330` rund
  50,7 ms je Scroll-/Zeichendurchlauf, die Glide-Tabelle 25,9 ms. Das ist
  keine allgemeine Tk-Untergrenze. Der Bibliotheksaufbau und wiederholte
  Layout-Aufrufe sind teure Pfade; zuerst messen und diese reduzieren.
  G25/Mobile ist gemäß D03 zurückgestellt. Zunächst Tk/Desktop verbessern.

## 5. Prüfen

- **Vollprüfung:**
  `python3 -B tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.32.1/<Name> --timeout 900`
  - 56 Suiten einschließlich Klappkontrolle, bisher rund 25 Minuten.
  - Unter macOS laufen die Fenster im Hintergrund und nehmen weder Fokus noch
    Tastatur; `--vordergrund` schaltet das ab.
- **Einzelsuite:** `python3 -B tests/integration/<suite>.py`, im Hintergrund
  mit `GLIDE_QA_HINTERGRUND=1 PYTHONPATH=tests/tools/hintergrund`.
- **Überall fest:** Standprüfung und Linkprüfung laufen in der Vollprüfung mit
  (`tests/tools/standpruefung.py`). Neue Dokumente unter `docs/` müssen in
  `docs/00_INDEX.md` stehen.
- **Letztes Ergebnis:** 3.32.1, Exitcode 0, 71 Schritte/56 Suiten; Python-Fassung
  und Bundle SHA-256-bytegleich (139/53 Dateien). Siehe
  `docs/07_QA_BERICHT.md` und `tests/qa-verlauf.md`.

## 6. Was als Nächstes ansteht

In dieser Reihenfolge; D08 wurde als Stabilitätskorrektur 3.32.1 vorgezogen.
D01–D06 sind gemäß Abschnitt 7 verbindliche Umsetzungsvorgaben.

1. **Drag-and-drop der bestehenden Seiten-/Notizbereiche (D04), dann
   Code-Durchsicht für Tempo und Einheitlichkeit** (Auftrag vom 30.09.2026,
   recherchiert und gemessen, Optimierung noch offen):
   - Statische Befunde (`scripts/pflege/analyse_codebasis.py`):
     - `app_font()` fragt bei jedem Aufruf dreimal Tk ab (404 Aufrufstellen).
       Ein Zwischenspeicher, geleert in `apply_ui_font`, ist der erste
       Schritt.
     - Beschriftungen wiederholen sich: „Abbrechen“ 29-mal, „Alle Dateien“
       26-mal, „Übernehmen“ 13-mal. Eine gemeinsame Texttabelle ist
       empfohlen.
     - `DueField._add_hover` und `LabelDropdown._hover` sind identisch; zu
       einer Hilfsfunktion zusammenlegen.
     - Datenschlüssel wie `'planned_date'` **nicht** in Variablen legen: kein
       Nutzen, tausende Änderungen.
   - Laufzeit: `scripts/pflege/messung_ansichtswechsel.py` ausgeführt;
     `refresh_library_page` und `ButtonFlow.reflow` sind Kostenstellen.
     Profilierte Wechsel sind keine unverfälschten Produktlatenzen. P01–P07
     mit unprofilierter Messbasis, gezielten UI-Aktualisierungen und
     Vorher/Nachher-Protokoll umsetzen (Arbeitsplanung, Abschnitt 5).
   - Davor die Bild-/Formatleistenbefunde der fünf neuen Fotos isoliert
     reproduzieren. Die Fotos beweisen keine konkrete Fehlerursache.
   - Längste Funktionen: `_refresh_home` (824 Zeilen), `item_form_dialog`
     (724), `create_ui` (680). Aufteilen erst mit Versionsverwaltung (E1).
2. **Etappe 2 „Planen“ → 3.33.0:**
   - G01 Alltagssprache: allgemeines Datum setzt Bearbeitungstag (D01);
   - G02 Eisenhower-Matrix mit erwartbarer Wirkung im sichtbaren Zielkontext
     (D02); Bearbeitungstag und Fälligkeit bleiben getrennte Felder;
   - G05 Fokus mit Timer;
   - dazu G31 (Seitenaufgabe über IDs in eine Liste schicken), G32 (Filter
     „aus Seiten“, Kopfzähler sind vorhanden) und G29 (Aufgabenzeilen im Notiztext; die Liste darüber
     zeigt genau diese Punkte – Antwort Q5 vom 30.09.2026).
3. **Etappe 3 „Wissen“ → 3.34.0:**
   - G08 Seitenverweise, zusammen mit G30 (Verweise auf Listen und Aufgaben);
   - G14 Volltextindex (SQLite FTS5);
   - G09 Titelbild;
   - G28 Liste in Seite einbetten.
4. **Etappe 4 „Pixel“ → 3.35.0:** G19 Palettenbearbeitung und Undo
   (indizierter Kern vorhanden), G17 Animation. Das nächste Datenformat
   wird beim ersten inkompatiblen Inhalt angehoben; das kann bereits die
   Wissensetappe betreffen. Mehrbild-GIF nachweisen, D07 beachten.
5. **Danach:** G24 KI-Austausch Stufe 2 über Dokumente (`.glidecontext`,
   Seiten als Markdown, Felder aus Format 20, Änderungsvorschläge), Import
   aus Notion und Todoist.

## 7. Entscheidungen und offene Punkte des Inhabers

[Arbeitsplanung, Abschnitt 6](Glide_Arbeits_und_Featureplanung_2026-09-30.md#6-entscheidungen-des-inhabers-und-offene-punkte)
ist maßgeblich: D01 Bearbeitungstag; D02 erwartbare Kontextwirkung; D03
Mobile vertagt; D04 Ziehen in bestehenden Bereichen; D05 einzelne Aufgaben in
Notizen/Seiten bei getrennten Typen; D06 Hinweise unverändert. F11 ist damit
beantwortet. D08 fordert Kontrolle aller Klappmechanismen und bessere QA;
Korrekturen und Nachweise stehen in Vertrag 69.

- **D07:** Muss die erste Animationsetappe bereits ein abspielbares GIF liefern,
  oder reichen Frames, Vorschau und Spritesheet? GIF ist eine abspielbare
  Bildfolge; Spritesheet ist eine PNG-Datei mit Frames nebeneinander.
- **Inhaber-/Store-/Plattformangaben:** I1–I6 gemäß Übersicht vom 29.09.;
  Git bleibt nach bestehendem Beschluss vertagt. Keine erneute Anfrage zu
  D01–D06 oder Hinweisvarianten/Mobile.
- **Store-Material:** Produktdatenblatt beschreibt noch 3.30.0; erst bei
  konkretem Bedarf archivieren und nachführen.

## 8. Manuell zu prüfen (nur der Inhaber)

- A17 und A18 der manuellen Prüfliste:
  - Hänger über die echte Menüleiste;
  - Tagesabschluss, Symbol-Export, Paletten, Platzhalter;
  - Rechtsklick und Formatleiste.
- Die Windows-Vollprüfung (`Checklisten/Windows_Pruefung_3.30.0.md`).

## 9. Zum Löschen markiert (`_Z`)

- Die `_Z`-Ordner hat der Inhaber am 30.09.2026 gelöscht.
- Übrig sind `07_Python-Versionen/Archiv/Glide-Aufgaben-und-Listen_v3.30.0_Z.pyw`
  und `…_v3.31.0_Z.pyw`. Beide Stände liegen vollständig in den Ordnern
  `…_vor_Rueckmeldung_Abend_2026-09-29` bzw. `…_v3.31.0_Endstand_2026-09-30`.
- Neu: `Glide-Aufgaben-und-Listen_v3.32.0_Z.pyw` im Python-Archiv; vorheriger
  Vollstand in `Glide_v3.32.0_vor_Klappkontrolle_2026-09-30`, vorheriges Bundle
  in `build/macos/archiv/Glide_v3.32.0_vor_Klappkontrolle_2026-09-30_Z.app`.
- Neues Überholtes weiter mit `_Z` markieren, nie selbst löschen.

## 10. Abschlussaufgabe für die nächste Implementierungsrunde

> Ich habe Performance Probleme mit Glide, hilf mir die Code-Basis zu optimieren, mit Variabeln für die gleichen Funktionen, Streamlinen und optimieren.

Aufgenommen, noch nicht umgesetzt. Konkreter Umfang und Abnahme: P01–P07
in der [Arbeits- und Featureplanung](Glide_Arbeits_und_Featureplanung_2026-09-30.md),
Abschnitte 5, 8 und 9. Gleiche Funktionen/Werte bündeln, UI-Aufrufe und
Neuaufbauten reduzieren, Gewinn messen, Daten-/Undo-/Fokusverhalten erhalten.
