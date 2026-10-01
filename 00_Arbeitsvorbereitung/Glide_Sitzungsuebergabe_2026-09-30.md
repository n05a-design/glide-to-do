# Glide – Übergabe an eine neue Sitzung

Stand 01.10.2026 · Glide 3.32.3 · Aufgabenformat 20 · für den nächsten Chat oder Bearbeiter

**Analyse und Planung 01.10.2026 (App unverändert 3.32.3):**
- **Neue Einstiege:**
  - [Entwicklungsplan ab 3.33](Glide_Entwicklungsplan_3.33ff_2026-10-01.md) mit Stufen 0–5 und Abgleich mit dem Auftrag
  - [Entscheidungsvorlage D09–D17](Glide_Entscheidungsvorlage_2026-10-01.md) (offen)
  - [Bestandsaufnahme Code/Doku](Glide_Bestandsaufnahme_Code_und_Dokumentation_2026-10-01.md)
  - [Konkurrenz- und Featurematrix](Glide_Konkurrenz_und_Featurematrix_2026-10-01.md)
  - [Produktprinzipien und UX-Prüfung](Glide_Produktprinzipien_und_UX-Pruefung_2026-10-01.md)
  - Nachweise: [analyse_planung_2026-10-01](../01_Repository/Glide/tests/qa-3.32.3/analyse_planung_2026-10-01/README.md)
- **Neu gemessen** (Linux, künstliche Daten, [`messung_speicherweg.py`](../01_Repository/Glide/scripts/pflege/messung_speicherweg.py)):
  - Jede Aktion kostet linear mit dem Bestand (Abhaken 56 ms bei 1.000, 446 ms bei 10.000 Punkten).
  - Das erste Speichern parst die Datei neunmal.
  - Vorschläge: P08 und T2; T2 ist der kleinste nächste Schnitt.
- **Repository `n05a-design/glide-to-do`:**
  - Enthält seit 01.10.2026 die Projektablage. Die Wurzel des Repositorys ist der Projektordner; `01_Repository/Glide` ist der Quellbaum.
  - Uploads immer in diese Struktur. Ein Upload in einen Unterordner bricht alle Querverweise.
  - Ob Git die Arbeitsgrundlage wird, entscheidet D09.
- **Hinweis zur Claude-Übergabe:** Für Claude Code ist das Paket `Glide_3.32.3_Python_Codebasis.zip` vorgesehen (`Archiv/Glide_3.32.3_Claude_Code_2026-10-01`); in der Sitzung vom 01.10. wurde stattdessen `07_Python-Versionen` übergeben (Laufzeit bytegleich).
- **Weiterhin gültig:** D01–D08 und der beauftragte Performance-Anschluss.
- **Vorfassung:** [Archiv](Archiv/Glide_Sitzungsuebergabe_2026-09-30_3.32.3_vor_Analyse_2026-10-01.md).


**Aktiver Showcase:** [Vertrag und Prüfgrenzen](../01_Repository/Glide/docs/72_SHOWCASE_3.32.3.md), [Nutzeranleitung](../05_Probelisten_Testdaten/Showcase/README.md). Eigenständiger, dauerhaft bearbeitbarer Arbeitsstand mit allen fünf Dokumentarten und den Bildern aus `20_Grafik_Master/06_Beispielbilder`; normale Glide-Nutzerdaten bleiben getrennt. Die Funktionsvorschau wurde auf den 01.10.2026 aktualisiert. Showcase-Prüfung ist zusätzlich zu 58 Suiten verpflichtend. Bestehende Feature-/Performancefolge und offene Auswahl bleiben gültig.

**Fortlaufende Arbeitsgrundlage:** [Arbeitsrichtung und Abnahme](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md) ist in AGENTS.md verankert. Der [Dokumentations-/Prüfwerkzeugnachlauf](../01_Repository/Glide/tests/qa-3.32.3/dokumentationsabgleich_2026-10-01/ergebnis.json) aktualisiert lokale Regeln und Einstiege bei unveränderter App 3.32.3.


Dieses Dokument ist der Einstieg für jede neue Sitzung. Es ersetzt nicht die
Verträge; es sagt, wo was steht, was gilt und was als Nächstes ansteht.

**Neu nach den Antworten D01–D08:**
[Arbeits- und Featureplanung](Glide_Arbeits_und_Featureplanung_2026-09-30.md)
führt D01–D06 als entschieden, D07 nach Erklärung als offen. D08 ist die
Klappkorrektur 3.32.1 mit neuer Pflichtsuite und
[Kontrollmatrix](../01_Repository/Glide/docs/69_KLAPPKONTROLLE_3.32.1.md).
Mobile/Toolkit-Probe zurückgestellt; Hinweise unverändert; bestehende Bereiche
um Ziehen erweitern: D04 ist jetzt 3.32.2. [Drag-/Performance-Vertrag 3.32.2](../01_Repository/Glide/docs/70_DRAG_UND_PERFORMANCE_3.32.2.md) enthält die gemeinsamen Drag-Bindungen, Schriftcache, gebündelte Layouts, Hoverhelfer und unprofilierte Messungen. 3.32.3 erhält Bibliothekskarten und gemeinsame Aktionsleisten im selben lebenden Host; Archiv-Zurückholen aktualisiert einmal. [Vertrag 71](../01_Repository/Glide/docs/71_KARTEN_PERFORMANCE_3.32.3.md). Einzelaufgaben im Notiztext sowie verbleibende Performance-Pakete folgen. Originalfoto-Befunde sind ohne konkreten Ablauf weiterhin nicht pauschal als behoben markiert.

## 1. In fünf Sätzen

- Glide ist eine lokale Aufgaben-, Notiz- und Seiten-App in Python mit Tk 9
  (eine Datei `src/glide/app.pyw` mit rund 54.000 Zeilen, dazu sieben Module).
- Der aktuelle Stand ist **3.32.3**:
  - Etappe 1 der Funktionsrecherche: Symbol-Export, Paletten, Platzhalter,
    Tagesabschluss;
  - zwei behobene Hänger: Menüleiste und Seite mit Bildern;
  - Klappzustände, Label-Pfeilklick und verschachtelte Bibliothek korrigiert;
  - Pflichtsuite mit echten Bedienwegen und Callbackfehler-Erfassung;
  - Prüfungen laufen im Hintergrund;
  - Drag-and-drop in bestehenden Seiten-/Notizbereichen;
  - Schriftcache, gebündelte Formatleistenlayouts und gemeinsamer Hover, mit Vorher-/Nachher-Messungen;
  - erhaltene Bibliothekskarten/Aktionsleisten im selben Host und einmaliges Archiv-Zurückholen.
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
| Startbare Fassung des Inhabers | `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.32.3.pyw` plus Module, `resources`, `vendor` |
| macOS-Bundle | `01_Repository/Glide/build/macos/Glide.app` (Kennung `de.shaye.glide`, nie ändern; Windows `Shaye.Glide`) |
| Verträge | `docs/66_MODERNISIERUNG_3.30.0.md` (3.30, 3.31: Abschnitte 2.17, 2.18), `docs/68_AUSBAU_3.32.0.md` (ab 3.32) |
| Entscheidungen | `00_Arbeitsvorbereitung/Glide_Funktionsrecherche_Ausbau_2026-09-30.md` (G01–G32, Q1–Q5), `Glide_Rueckmeldung_und_Entscheidungen_2026-09-29.md` (R1–R11), `Glide_Uebersicht_und_Entscheidungen_2026-09-29.md` (B, E, F, I) |
| Prüfstand | `docs/07_QA_BERICHT.md`, `tests/qa-verlauf.md`, Protokolle unter `tests/qa-<Version>/` |
| Manuelle Prüfliste | `00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.30.0.md` (gilt auch für 3.32.3; zusätzliche Bedienproben in Verträgen 69/70/71) |
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
- **Plattformunabhängig:** Mac, Linux, Windows. Mobile/iPhone/iPad und Toolkit-Probe sind nach D03 zurückgestellt; keine
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
- **Jede Produktionsrunde bekommt eine Version** (Werkzeug `scripts/pflege/versionswechsel.py`). Reine Dokumentations-/Prüfwerkzeugnachläufe werden zur unveränderten App-Version datiert belegt; [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md).
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
- **Historischer Tempobefund auf 3.32.0:** Die Vergleichsliste kostete im erneuten `test_tempo330` rund
  50,7 ms je Scroll-/Zeichendurchlauf, die Glide-Tabelle 25,9 ms. Das ist
  keine allgemeine Tk-Untergrenze. Der Bibliotheksaufbau und wiederholte
  Layout-Aufrufe sind teure Pfade; zuerst messen und diese reduzieren.
  G25/Mobile ist gemäß D03 zurückgestellt. Zunächst Tk/Desktop verbessern.

## 5. Prüfen

- **Vollprüfung:**
  `python3 -B tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.32.3/<Name> --timeout 900`
  - 58 Suiten einschließlich Klapp-, Drag-/Performance- und Bibliothekskarten-Kontrolle, bisher rund 25 Minuten.
  - Unter macOS laufen die Fenster im Hintergrund und nehmen weder Fokus noch
    Tastatur; `--vordergrund` schaltet das ab.
- **Einzelsuite:** `python3 -B tests/integration/<suite>.py`, im Hintergrund
  mit `GLIDE_QA_HINTERGRUND=1 PYTHONPATH=tests/tools/hintergrund`.
- **Überall fest:** Standprüfung und Linkprüfung laufen in der Vollprüfung mit
  (`tests/tools/standpruefung.py`). Neue Dokumente unter `docs/` müssen in
  `docs/00_INDEX.md` stehen.
- **Letztes Ergebnis:** 3.32.3, Exitcode 0, 73 Schritte/58 Suiten und fünf Analysen; Python-Fassung
  und Bundle SHA-256-bytegleich (139/53 Dateien). Siehe
  `docs/07_QA_BERICHT.md` und `tests/qa-verlauf.md`.

## 6. Was als Nächstes ansteht

**Performance-Fortsetzung 01.10.2026:** Bibliothekskarten und gemeinsame Aktionen in 3.32.3 umgesetzt; gezielte Prüfung und Messserien grün. [Vertrag 71](../01_Repository/Glide/docs/71_KARTEN_PERFORMANCE_3.32.3.md) enthält Lebensdauer/Invalidierung und Messgrenzen. Vollprüfung und Abgleich abgeschlossen: 73 Schritte/58 Suiten und fünf Analysen, 139 Python-/53 Bundle-Dateien bytegleich, Signatur gültig. Beide Startfassungen tragen 3.32.3. Der Inhaber hat die bestehende Performance-Arbeit ausdrücklich fortgesetzt, die zusätzliche Auswahl neuer Features bleibt offen.

**Neue Auswahl auf Wunsch des Inhabers:** [Weitere Aufgaben und Richtungsauswahl nach 3.32.2](Glide_Aufgabenauswahl_nach_3.32.2_2026-09-30.md) sammelt 24 Aufgaben. Erste Richtung und Bearbeitungstiefe sind noch offen; A-01 ist in 3.32.3 abgeschlossen. Rest P03 und A-02/A-03 folgen der beauftragten Performance-Arbeit; C-01 oder B-01 ist eine anschließende Empfehlung, kein neuer Beschluss. Die bisherige Folgeplanung unten bleibt Grundlage bis zur Auswahl.

In dieser Reihenfolge; D08 wurde als Stabilitätskorrektur 3.32.1 vorgezogen.
D01–D06 sind gemäß Abschnitt 7 verbindliche Umsetzungsvorgaben.

1. **Nächster Performance-Schnitt: restliches P03, P04/P06:**
   - D04 ist umgesetzt. P02 Schriftcache, gebündelte ButtonFlow-Layouts
     (Teil P03) und Hoverhelfer (Teil P05) sind im Vertrag 70 dokumentiert.
   - Unprofilierte Messserien mit 100/1.000/10.000 Aufgaben sowie Notiz und
     Bildseite liegen im QA-Ordner 3.32.2. Rest P01: Verlaufvarianten und
     Speicherentwicklung; keine allgemeinen Latenzversprechen.
   - Bibliothekskarten bleiben seit 3.32.3 innerhalb derselben Ansicht erhalten; [Vertrag 71](../01_Repository/Glide/docs/71_KARTEN_PERFORMANCE_3.32.3.md). Startseitenkarten/geänderte Kartenelemente und viele Karten weiter prüfen. Neue Pflichtsuite für Invalidierung, Scrollen, Größen/Design, Undo und Lebensdauer; physische Fokusprobe offen.
   - Danach Bildlayout von Platzierung trennen und identische Speicher-/
     Refresh-Anforderungen reduzieren. Vorhandene Caches, Undo und atomare
     Datenwege bewahren. Keine verzögerte ungesicherte Datenspeicherung.
   - Die Bild-/Formatierungssuiten sind erneut grün. Originalfoto-Ablauf
     nicht exakt reproduziert; keine pauschale Erledigtbehauptung.
   - Rest P05: gleiche UI-Texte nur nach gleicher Bedeutung zentralisieren.
     Große Monolith-Aufteilung bleibt mit vertagtem Git zurückgestellt.
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

- A17–A21 der fortgeschriebenen manuellen Prüfliste:
  - Hänger über die echte Menüleiste;
  - Tagesabschluss, Symbol-Export, Paletten, Platzhalter;
  - Rechtsklick und Formatleiste;
  - sämtliche Klappzustände, Drag-Ziele und Fokus/Scrollen bei Kartenaktualisierung.
- Die Windows-Vollprüfung (`Checklisten/Windows_Pruefung_3.30.0.md`).

## 9. Zum Löschen markiert (`_Z`)

- Die `_Z`-Ordner hat der Inhaber am 30.09.2026 gelöscht.
- Übrig sind `07_Python-Versionen/Archiv/Glide-Aufgaben-und-Listen_v3.30.0_Z.pyw`
  und `…_v3.31.0_Z.pyw`. Beide Stände liegen vollständig in den Ordnern
  `…_vor_Rueckmeldung_Abend_2026-09-29` bzw. `…_v3.31.0_Endstand_2026-09-30`.
- Neu: `Glide-Aufgaben-und-Listen_v3.32.0_Z.pyw` im Python-Archiv; vorheriger
  Vollstand in `Glide_v3.32.0_vor_Klappkontrolle_2026-09-30`, vorheriges Bundle
  in `build/macos/archiv/Glide_v3.32.0_vor_Klappkontrolle_2026-09-30_Z.app`.
- Neu nach 3.32.2: `Glide-Aufgaben-und-Listen_v3.32.1_Z.pyw`; vollständige
  Python-/Bundle-Vorsicherungen stehen in Abschnitt 11.
- Neu nach 3.32.3: `Glide-Aufgaben-und-Listen_v3.32.2_Z.pyw` und vollständige Vorsicherungen gemäß Abschnitt 12.
- Neues Überholtes weiter mit `_Z` markieren, nie selbst löschen.

## 10. Abschlussaufgabe für die nächste Implementierungsrunde

> Ich habe Performance Probleme mit Glide, hilf mir die Code-Basis zu optimieren, mit Variabeln für die gleichen Funktionen, Streamlinen und optimieren.

Erster Schnitt in 3.32.2 und Bibliothekskarten/Aktionsleisten in 3.32.3 umgesetzt, gemessen und in beiden Startfassungen abgeglichen (73 Schritte/58 Suiten grün). Restliches P03, P04/P06 und weitere Optimierungen bleiben offen. Konkreter Umfang und Abnahme: P01–P07
in der [Arbeits- und Featureplanung](Glide_Arbeits_und_Featureplanung_2026-09-30.md),
Abschnitte 5, 8 und 9. Gleiche Funktionen/Werte bündeln, UI-Aufrufe und
Neuaufbauten reduzieren, Gewinn messen, Daten-/Undo-/Fokusverhalten erhalten.

## 11. Historischer Abschluss der Produktionsrunde 3.32.2

Python-Vollstand 3.32.1 in `07_Python-Versionen/Archiv/Glide_v3.32.1_vor_Drag_Performance_2026-09-30`, Bundle in `build/macos/archiv/Glide_v3.32.1_vor_Drag_Performance_2026-09-30_Z.app`. Quellstand/Messwerte und Hashes unter `tests/qa-3.32.2/drag_performance_2026-09-30`. Alte Hauptdatei ist als `Glide-Aufgaben-und-Listen_v3.32.1_Z.pyw` archiviert.

**Abschluss:** [Vollprotokoll](../01_Repository/Glide/tests/qa-3.32.2/drag_performance_2026-09-30/vollpruefung/ergebnis.json) und [Dateiabgleich](../01_Repository/Glide/tests/qa-3.32.2/drag_performance_2026-09-30/abgleich.json) bestätigen 72 Schritte/57 Suiten, fünf Analysen, 139 Python-/53 Bundle-Dateien bytegleich sowie gültige Ad-hoc-Signatur. Der Quellstand wurde während des finalen Volllaufs nicht geändert. Zeichnungs-Kontextleiste vor synchroner Höhenreservierung ausdrücklich layouten; die Pflichtsuite prüft stabile Höhe über Werkzeugwechsel und Fensterbreiten. Windows/Linux, physische Bedienung, DPI und Screenreader bleiben offen; keine echten Nutzdaten gelesen.

## 12. Abschluss 3.32.3, 01.10.2026

[Vertrag 71](../01_Repository/Glide/docs/71_KARTEN_PERFORMANCE_3.32.3.md), [Vollprotokoll](../01_Repository/Glide/tests/qa-3.32.3/karten_performance_2026-10-01/vollpruefung/ergebnis.json), [Abgleich](../01_Repository/Glide/tests/qa-3.32.3/karten_performance_2026-10-01/abgleich.json): 73 Schritte/58 Suiten/fünf Analysen grün, Quell-/Prüfstand unverändert; 139 Python-/53 Bundle-Dateien bytegleich, Signatur gültig. Bei 1.000 Aufgaben erneuter Bibliotheks-Refresh unverändert 776,2 → 4,9 ms, Status 785,3 → 388,3 ms. Keine Speicher-/Wechsellatenzbehauptung. Vollstand 3.32.2 in `07_Python-Versionen/Archiv/Glide_v3.32.2_vor_Karten_Performance_2026-10-01`, Bundle in `build/macos/archiv/Glide_v3.32.2_vor_Karten_Performance_2026-10-01_Z.app`; alte Hauptdatei `Glide-Aufgaben-und-Listen_v3.32.2_Z.pyw`. Anschluss P04/P06 in Arbeitsplanung und [statischem Codeabgleich](../01_Repository/Glide/tests/qa-3.32.3/karten_performance_2026-10-01/folgeschnitt_codebefunde.json). Mobile/Hinweisgestaltung/Git unverändert entschieden; neue Feature-Richtungsauswahl und D07 offen. Windows/Linux, physische Bedienung, DPI und Screenreader offen; keine echten Nutzdaten gelesen.
