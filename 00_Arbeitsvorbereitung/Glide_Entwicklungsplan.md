# Glide – Entwicklungsplan und Aufgabenstand

Stand 18.10.2026 · Glide 3.43.1 · Aufgabenformat 25

Einziges Planungsdokument: Aufgaben, Pakete, Reihenfolge und Entscheidungsvorlagen. Nach der Standanalyse vom 18.10.2026 wurde die beauftragte Schutzrunde auf FP-01 integriert und gezielt geprüft. Der anschließende Auftrag umfasst globale Ablageprüfung, Zusammenführung, Bereinigung, erneute Validierung sowie Commit und GitHub-Pull-Request. Weitere Features, Versionswechsel, Lieferung nach 07 und automatische Zusammenführung sind damit nicht freigegeben. Ergebnisse stehen im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md), Verhalten in den [Funktionen](../01_Repository/Glide/docs/20_FUNKTIONEN.md), Produktentscheidungen in der [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md). Historische Paketbelege sind keine aktuelle Abnahme.

**Lesefolge:** aktueller Auftrag und Statusachsen hier → konsolidiertes [Funktionsinventar §18](#18-konsolidiertes-funktions--und-aufgabeninventar) → [Paketvertiefung §19](#19-paketgrenzen-ausbaustufen-und-aufwand) → [Entscheidungsregister §20](#20-vollständiges-entscheidungsregister). §§3–8 ordnen bestehende Kennungen fachlich; §§14–15 erhalten die ausgewählten Sprints als Vorgeschichte; §16 trägt weiterhin die FP-/WA-Aufgaben. Es entsteht kein zweiter Backlog.

Verbindliche Entscheidungen stehen in der [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md), Produktgrenzen und Prinzipien in den [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md). D07 ist durch D18 entschieden; Importquelle und Bauwerkzeug sind durch D26/D27 gewählt; Inhaberfreigaben bleiben eigene Entscheidungen (§11).

## Statusmarken

| Marke | Bedeutung |
|---|---|
| ✅ | erledigt, mit Version |
| ◐ | teilweise erledigt; der offene Rest steht dabei |
| ▶ | beauftragt, als Nächstes |
| ○ | offen, braucht Auftrag oder Entscheidung |
| ◇ | Zukunft, wartet auf einen Auslöser |
| ✕ | bewusst nicht (Produktgrenze oder Entscheidung) |

Die Marken sind Navigationshilfen aus den früheren Runden. Ein früheres ✅ bezeichnet den damaligen Paketabschluss; es beweist weder eine heutige Vollprüfung noch eine menschliche Abnahme. **Verbindlich ist die getrennte Angabe A/B im aktuellen Inventar (§18):** A = Auftrag/Entscheidung/Auslegung/Vorschlag/zurückgestellt/ausgeschlossen; B = Implementierung, tatsächlich ausgeführte Prüfung, Lieferung und menschliche/plattformspezifische Abnahme. Bei 3.43.x fehlen Teile des Mac-/Paketabschlusses; deshalb wird die ältere pauschale Gleichsetzung von ✅ und vollständig geliefert hier ausdrücklich aufgehoben.

**Untersuchte Ausgangsstände:** Die Analyse verglich die lokale Wurzel `c0252ba` mit `origin/main` bei `9ec474b9dcbd502efce8cb221e53e24c322f9a78` und dem Planungszweig `19c7df5` (D51). Inzwischen sind der Upstream und die Schutzrunde in `codex/ablageaudit-schutzrunde-2026-10-18` integriert: App-Hash `f74af723e3fe1fc18aae5beafcef3d026a3a9c39d8eb16c90b68fb3ae7ddec26`, 72 eigene Laufzeitdateien und 94 Integrationssuiten. 07 bleibt unverändert auf dem früheren 3.43.1-Stand; Pakete bleiben 3.42.0. Die historische [Analyse §9](Glide_Analyse.md#9-gesamtanalyse-vom-18102026) bleibt erhalten; die aktuelle Standmatrix steht im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md).

## 1. Leitsatz und Reihenfolge

*Glide ist der ruhige, lokale Arbeitsplatz für den eigenen Tag – planen, erledigen, festhalten; alles in einer eigenen Datei, ohne Konto. Die Pixel-Werkstatt ist die persönliche Signatur.*

Drei Säulen in dieser Rangfolge: **verlässlich und schnell** (Daten sicher, Aktionen unter 100 ms bei realistischen Beständen) → **klarer Alltag** (Heute, Demnächst, Listen, Seiten; Erfassen ohne Nachdenken) → **Wissen im Kontext** (Aufgaben in Seiten und Notizen, Verweise, Suche).

**Bewusst begrenzt:** kein allgemeiner Notion-Nachbau, kein Sync- oder Cloud-Dienst. Die Pixel-Werkstatt ist eine besondere Kombination, keine bewiesene Alleinstellung. Es liegen keine Nutzungsdaten vor; Prioritäten folgen Funktionslücke, Entscheidung, Aufwand und Regressionsrisiko.

Reihenfolge der Stufen (Antwort des Inhabers vom 30.09.2026, bestätigt am 01.10.2026): Fundament → Planen → Wissen → Pixel → Austausch und Verteilung.

| Stufe | Inhalt | Stand |
|---|---|---|
| 0 Fundament | Performance P01–P09, T2, CI | ◐ Ziele für Abhaken und Suche erreicht (3.33.19, 3.34.0); P03/E01 und Linux-Kalibrierung mit 3.36.0 geliefert; P05 nur bei künftig tatsächlich angefasstem Code; aktuelle Schutzpunkte §18 |
| 1 Klarer Alltag | Bereiche, Startseite, Eingabe, Eisenhower, Heute/Demnächst, UX1, Fokus, Komfort, Tag, Oberfläche Welle 1 | ◐ geliefert bis 3.33.21; Welle 2 nach I7 in 3.38.0 geliefert, Mac/Linux/Windows automatisch grün; Menschenabnahme getrennt offen; AU03-Hinweise/AU07 mit 3.39.0 geliefert; UI-/UX-Paket aus Nutzerbeobachtungen (§17) mit 3.43.0 |
| 2 Wissen im Kontext | Suche, Verweise, Live-Liste, Titelbild, Kalender mit Wochenplanung, Bilder in Seiten, Filter erklären | ◐ geliefert 3.33.7–3.34.0; N05 in 3.38.0 geliefert, Mac/Linux/Windows automatisch grün; Menschenabnahme getrennt offen |
| 3 Pixel | Palettenbearbeitung, Symbolvorschau, Animation | ◐ G19, G-03 ✅ 3.35.0; G17 ✅ 3.40.0 geliefert |
| 4 Austausch und Verteilung | KI-Austausch Stufe 2, Import, Sicherungsvergleich, Paket mit eigenem Python | ◐ G24, F-03 ✅ 3.35.0; G21 ✅ 3.41.0 geliefert; G26/D27 ✅ 3.42.0 geliefert |
| 5 Zukunft (4.x) | Screenreader (Tk 9.1), Seitenversionen, SQLite nur nach D16-Neubewertung | ◐ N12 Aufgaben-Kernablauf durch D36/D44 für 4.0.0 beauftragt und vorbereitet, seit D50 hinter dem UI-/UX-Paket pausiert; übrige Zukunftspunkte ◇ |

## 2. Erledigt seit 3.30

| Version | Inhalt |
|---|---|
| ✅ 3.30.0–3.31.0 | Modernisierung: Pinnwand-Board, Ordnertypen, Seiten und Galerie, Pixel-Werkstatt mit Größen 16–128, Format 20, Bilder in Seiten, Tk 9, Ziehen aus Finder/Explorer, Systemmitteilungen (Option), Logo, Sicherungen nur bei Änderung, Startprüfung, Notizbereich, gemeinsamer Editor, Inhaltsverzeichnis, Aufklapp- und Hinweisblöcke |
| ✅ 3.32.0–3.32.3 | Symbol-Export (ICO), Paletten aus Aseprite/Adobe, Platzhalter, Tagesabschluss; Klappkontrolle (D08); Ziehen in Bereichsbäumen (D04); Schriftcache; Bibliothekskarten erhalten; Showcase |
| ✅ 3.33.0–3.33.6 | Formatsicherung T2, P09a; vier Seitenleistenbereiche; Startseite „Ruhig“ (D12); Schnelleingabe mit Feldchips (D10) und Wiederholungen; Eisenhower als Gruppierung (D13); „Heute“ und „Demnächst“ (D14) |
| ✅ 3.33.7–3.33.12 | Inhaltssuche (G14), Windows-Formatsicherung; P08a, P09b, P08b; stabile Aktionskennungen, U03/U07; U10/U19, erste OB01-Übernahme |
| ✅ 3.33.13–3.33.18 | KO01/AU02 Einplanen mit verfügbarer Zeit; Tagespaket AU01/AU03-Weg/G05/H-02; Aufgaben im Wissen G29/G31/G32 (Format 21); Bedienkomfort U01/U02/U13/U14/U16/U22/U24; Wissen und Woche N04/AU04, G08/G30 (Format 22); Seiten im Alltag G28/G09/U08 (Format 23) |
| ✅ 3.33.19–3.35.0 | Sprint (§14): Tempo, Komfort, ruhige Oberfläche, Wissen und Seiten, Pixel und Austausch |
| ◐ 3.43.0 | UI-/UX-Paket aus Nutzerbeobachtungen (§17, D50): B01–B20; automatisch geprüft und nach 07/05 geliefert, Mac-Vollprüfung und Bundle offen |
| ✅ 01.–03.10.2026 | D09 Repository als Ablage, CI-Grundstufe, Ablagegröße, Bereinigung der Ablage und Dokumentation |

## 3. Performance (Stufe 0, beauftragt)

Fortlaufender Auftrag des Inhabers: „Ich habe Performance Probleme mit Glide, hilf mir die Code-Basis zu optimieren, mit Variabeln für die gleichen Funktionen, Streamlinen und optimieren.“ Gleiche Funktionen und Werte nur bei gleicher Bedeutung bündeln, Aufbau- und Schreibaufwand messbar senken, Daten-, Undo- und Fokusverhalten erhalten. Keine pauschale Ersetzung von Datenschlüsseln durch Variablen.

| ID | Arbeit | Stand |
|---|---|---|
| P01 | Messbasis: unprofilierte Serien mit 100/1.000/10.000 Punkten, Notiz, Bildseite, Verlaufvarianten, Speicherentwicklung | ✅ 3.33.19 (P01r) |
| P02 | Schriftcache je Tk-Interpreter | ✅ 3.32.2 |
| P03 | Aufbau und Layout | ✅ 3.36.0: geänderte Karten und Startseite abgeglichen, viele Karten geprüft; Tempoausnahmen D46 und Messnachweis in §15.7 |
| P04 = A-02 | Bildlayout nur bei geänderter Geometrie, Platzieren beim Scrollen | ✅ 3.33.19 |
| P05 | Gemeinsame Helfer | ◐ Hover 3.32.2; gezielt gleiche Texte/Abläufe im Sprint-Code gewählt (D40 A/1) |
| P06r = A-03 | Doppelte Refresh-/Schreibanforderungen je Aktion | ✅ 3.33.19 |
| P07 | Volltextsuche als ersetzbarer FTS5-Cache | ✕ nach Messung 3.34.0: 66,6 ms Median bei 10.000 Punkten (Regel: unter 100 ms kein Index) |
| P08a/P08b | Ein Vergleichsdurchlauf für Verlauf und Aktivität; nur geänderte Listen vergleichen, Vollvergleich im Autosave | ✅ 3.33.9 / 3.33.11 |
| P08c | Abhaken bei 5.000 Punkten ≤ 120 ms | ✅ gemessen 3.33.19: 61 ms |
| P09a/P09b | Tabelle ohne Listenspaltenmessung; Kennzahlen, Datum und Schriftmaße einmal je Aufbau | ✅ 3.33.0 / 3.33.10 |
| T2 | Gemeinsame Formatsicherung | ✅ 3.33.0; Windows-Signatur 3.33.7, Inhaltsvergleich 3.33.8 |
| E01 | Einblendung des Einstellungsfensters | ✅ 3.36.0: erste Anzeige ≤ 250 ms, erneut Median ≤ 150/p95 ≤ 190 ms nach D48; sichere Wiederverwendung |
| CI | CI-Grundstufe (Linux/Xvfb) | ✅ 01.10.2026; gesamte ausführbare Linux-Matrix seit 3.36.0 verpflichtend und nativ grün (D35/S26-15) |

Messwerte je Version: [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md). Verbindlich ist die Messung auf dem Referenz-Mac mit Aufwärmen, Median und p95; Linux-Werte gelten als Trend.

## 4. Klarer Alltag (Stufe 1)

### 4.1 UX1 „Weniger Oberfläche“

| ID | Befund (Prinzip) | Empfehlung | Stand |
|---|---|---|---|
| U01 = N03 | Kopfzeile mit acht Symbolknöpfen, zwei Suchen (P3, P5) | eine Befehlspalette (`Strg/Cmd+O`), Verlauf und Drucken ins Menü, Glocke nur bei Bedarf, ≤ 4 Symbolknöpfe | ✅ 3.33.16 |
| U02 | Dauerhafte Hinweiszeilen (P1, P4) | „?“ klappt Hinweise ein/aus, Zustand gemerkt (D11); seit B06 ein Schalter in den Einstellungen statt „?“ | ✅ 3.33.16; Fortschreibung §17 |
| U03 | „Suche löschen“ auch bei leerer Suche | Löschkreuz nur bei Inhalt, `Esc` leert | ✅ 3.33.11 |
| U04 | „Erweitert“/„Hinzufügen“ als Textknöpfe | Feldchips, „+“-Knopf, Umschalt+Enter | ✅ 3.33.3 / 3.33.20 |
| U05 | Startseite überladen | sieben Kacheln (D12); Gismo-Pflege bei Bedarf | ✅ 3.33.2 / 3.33.21 |
| U06 | Überlappende Ansichten | Heute und Demnächst (D14) | ✅ 3.33.6 |
| U07 = N02 | Eingang nicht in der Seitenleiste | Zeile „Eingang (n)“ nur solange er Einträge hat | ✅ 3.33.11 |
| U10 | Kopfzeile kürzt den Titel zugunsten der Kennzahlen | Titel hat Vorrang, Kennzahlen in der Unterzeile | ✅ 3.33.12 |
| U13 | Bibliothek mit doppelten Wegen | Kachelklick öffnet; eine Fußleiste | ✅ 3.33.16 |
| U14 | Menüeinträge am falschen Ort, drei Sicherungsbegriffe | Einträge umsortiert, ein Sicherungsbegriff | ✅ 3.33.16 |
| U16 | Begriffe uneinheitlich | Glossar: Aufgabe, Langtext, Zwischenüberschrift, Gruppe | ✅ 3.33.16 |
| U17/N01 | Kein „wie System“ | „Automatisch hell/dunkel“, Signaturdesign vorn | ✅ 3.33.21 |
| U19 | Quellliste und Nummer vor jedem Titel in „Heute“ | Titel zuerst, Quelle gedämpft rechts | ✅ 3.33.12 |
| U22 | Bearbeitungstag in Listenzeilen unsichtbar | Symbol ◉ + Tag in der Datumsspalte | ✅ 3.33.16 |
| U24 | Symbole mit mehreren Bedeutungen | eigene Zeichen, Doppelungsregel in der Symbolprüfung | ✅ 3.33.16 |

**Fertig, wenn:** Kopfzeile ≤ 4 Symbolknöpfe ✅; kein Symbol mit zwei Bedeutungen ✅ (Bewegungspfeile ausgenommen); Bedienfläche über dem Inhalt ≤ 15 % bei 1280 × 800 – mit 3.38.0 an sechs Inhaltswidgets 14,125–14,625 % gemessen und Mac/Linux/Windows automatisch grün; menschliche Abnahme getrennt offen.

### 4.2 Weitere Arbeiten der Stufe 1

| ID | Arbeit | Stand |
|---|---|---|
| G05 = B-02 | Fokus mit Timer an der vorhandenen Zeiterfassung, Zeit genau einmal gebucht | ✅ 3.33.14 |
| H-02 | Tastaturwege für alles, was sich ziehen lässt, mit sichtbarem Ziel und einem Undo-Schritt | ✅ Zeitblöcke 3.33.14, Pinnwand und Bereichsbäume 3.34.0 (H-02r) |
| G29/G31/G32 = C-01–C-03 | Aufgaben im Notiztext mit gleicher ID, Seitenaufgabe in eine Liste, Filter „aus Seiten“ | ✅ 3.33.15 |
| N07 = U21 | Einmalige Karte „Neu in …“ nach einem Update | ✅ 3.33.20 |
| N08 | JPEG-Vorschau unter Linux über ein Systemwerkzeug | ✅ 3.34.0; Linux-Sichtprüfung offen |
| U20 | Leerzustand ohne doppelten Anlegen-Knopf | ✅ 3.33.20 |
| DOK2 | Kommentar AB06, Mindestversion Python/Tk (AB08) | ✅ 3.33.9 / 3.33.20 |
| LG01 | Logo-Rückfall unter Tk 8.6 geglättet (Weg B der [Funktionsnachweis](https://github.com/n05a-design/glide-to-do/blob/0e7b3583a9d7a53925e0b67053895718bbd1c6b6/01_Repository/Glide/tests/qa-3.37.0/logo_symbole_2026-10-10/README.md)) | ✅ 3.37.0 geliefert; Mac/Linux/Windows automatisch grün, Menschen-/DPI-Abnahme getrennt |
| LG02 | App-Symbol in 16, 32, 64 und 256 px vorrechnen, unter Tk 8.6 direkt laden; `glide-logo.png` und Modulkopf von `logo.py` berichtigen (Wege C und F) | ✅ 3.37.0 geliefert; Mac/Linux/Windows automatisch grün, Menschen-/DPI-Abnahme getrennt |
| LG03 | `test_logo330` verlangt Zwischentöne an der Logokante (Weg D) | ✅ 3.37.0 geliefert; Mac/Linux/Windows automatisch grün, Menschen-/DPI-Abnahme getrennt |
| LG04 | Logo-Master überarbeiten (Weg E; [Befunde](../20_Grafik_Master/README.md#freigegebene-master-und-laufzeit-3370)) | ✅ 3.37.0 geliefert; Mac/Linux/Windows automatisch grün, Menschen-/DPI-Abnahme getrennt |
| W01 | Seitenleistentitel unter Windows/Tk 9 rechts um etwa ein Zeichen angeschnitten; `sidebar_available_text_width` mit dem gezeichneten Platz abgleichen | ○ Sichtprüfung B1, dann Produktionsschnitt |
| W02 | Dunkeltests über `set_design` statt `theme_name` | ✅ umgestellt 08.10.2026; Mac und native Windows-Vollprüfung 3.36.0 grün, menschliche Sichtprüfung offen |
| W06 | Auf Fotos von „Neue Liste“/„Neuer Ordner“ fehlen Überschrift und Feldbeschriftungen | ○ Sichtprüfung B1a; bei Bestätigung Produktionsschnitt, sonst Fotozeitpunkt in `test_fenster330` |
| W07 | „PNG auf 128 × 128 einpassen“ nach „Ganzes Bild zeigen“: Hinweistext doppelt | ◇ auf dem Mac nicht nachstellbar; Sichtprüfung B1a |
| W08 | „Pixelsymbol“: Raster nur rund 60 px groß | ◇ auf dem Mac nicht nachstellbar; Sichtprüfung B1a |
| W09 | Einmaliger Absturz von Python 3.14.8 unter Windows in `attributpruefung` (0 von 30 Wiederholungen) | ◇ beobachten; bei Wiederholung an CPython melden |
| W03, W04, W05, W10–W15 | Zeilenenden, Synchronisationswächter, Dialogbreite, Aufbewahrung, Kommentare, Lieferabsatz, Standprüfung, Vorversionen, Sperrzählung | ✅ 08./09.10.2026 bzw. 3.33.21 (W05; Bestätigung in der Windows-Sichtprüfung B1a) |

### 4.3 Ausbauprogramm Alltag, Komfort und Oberfläche

Auftrag des Inhabers vom 05.10.2026 (Wortlaut): „Mehr Features, Mehr Quality of Life Updates, Mehr Unterstützung im Alltag und eine modernere Oberfläche genau wie in der Konkurrenz Analyse beschrieben“. Grundlage sind [Markt und Vorbilder](Glide_Markt_und_Vorbilder.md) (fertiger Tagesablauf; zu viel dauerhaft sichtbar; Vorbilder TickTick, Things, Apple, Super Productivity, Sunsama).

**Regeln für jedes Paket:** Prinzipien-Check der [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md) bestehen – vorhandenen Weg erweitern statt einen zweiten bauen und benennen, was dafür verschwindet; D01/D02 gelten; Fachlogik als Tk-freies Modul mit Unit-Tests (D17); keine neue Laufzeitabhängigkeit; kein Formatwechsel, außer er ist genannt. Aufwand: S bis 1 Arbeitstag, M 2–4, L mehr als 4.

#### A. Moderne, ruhige Oberfläche

| ID | Paket | Abnahme (Auszug) | Aufwand | Stand |
|---|---|---|---|---|
| OB01 | Gestaltungsskala für Abstände, Radien, Schriftgrößen und Zeilenhöhen (`ui_design.py`) | ohne sichtbare Änderung; Abstandswerte je Ansicht gemessen | M | ✅ 3.33.12 / 3.33.21 (Startseite, Bibliothek, Einstellungen, Schnellerfassung: direkte Zahlen 134 → 3); weitere Ansichten bei Gelegenheit |
| OB02 | Vier Textstufen; Kopf von „Heute“ zeigt nächste Aufgabe, verfügbare Zeit und Fortschritt als stärkstes Element | 860 × 700, große Schrift; jede Angabe genau einmal | M | ✅ 3.38.0 geliefert; Mac/Linux/Windows automatisch grün, Menschen-/DPI-Abnahme getrennt offen |
| OB03 | Zeilenaktionen nur bei Bedarf (Einplanen, Termin, „…“ beim Überfahren und bei Auswahl) | jede Aktion auch über Tastatur, Kontextmenü, Palette; Bedienfläche ≤ 15 % | M | ✅ 3.38.0 geliefert; Mac/Linux/Windows automatisch grün, Menschen-/DPI-Abnahme getrennt offen |
| OB04 | Dezente Bewegung beim Abhaken, Klappen und Bereichswechsel (≤ 150 ms), nur mit Animationen | keine messbare Verschlechterung der Ziele aus §10 | M | ✅ 3.38.0 geliefert; Mac/Linux/Windows automatisch grün, Menschen-/DPI-Abnahme getrennt offen |
| OB05 | Schmale Seitenleiste mit Symbolen | Zustand gemerkt; Tastatur; 860 × 700 | M | ✅ 3.33.21 |
| OB06 | Gestaltungsabnahme je Paket: Vorher-/Nachher-Fensterbilder, vom Inhaber bewertet; Bilder lokal und unversioniert | Entscheidung im QA-Bericht vermerkt | S je Paket | ◐ Bewertung durch den Inhaber offen |

#### B. Komfort im täglichen Gebrauch

| ID | Paket | Abnahme (Auszug) | Aufwand | Stand |
|---|---|---|---|---|
| KO01 | Ein Menü „Einplanen“ (Heute, Morgen, Wochenende, Nächste Woche, Datum …, Ohne Tag) für die Mehrfachauswahl | ein Undo-Schritt; Fälligkeit bleibt | S–M | ✅ 3.33.13 |
| KO02 | Wiederholungen: Termin überspringen, verpasste Termine überspringen | Serie bleibt; ein Undo-Schritt | S | ✅ 3.33.20 |
| KO03 | Erinnerungen in der Schnelleingabe als Chip | Chip nennt „nur bei laufender App“ | S | ✅ 3.33.20 |
| KO04 | Felder am Objekt: Klick auf Termin, Wichtigkeit oder Label öffnet die kleine Auswahl dort | ein Undo-Schritt; einheitlich mit N05 | M | ✅ 3.38.0 geliefert; Mac/Linux/Windows automatisch grün, Menschen-/DPI-Abnahme getrennt offen |
| KO05 | Mehrzeiliges Einfügen in die Eingabezeile nach Rückfrage | ein Undo-Schritt | S | ✅ 3.33.20 |
| KO06 | Zuletzt benutzte Ziele zuerst bei „Verschieben nach …“ und Labels | keine neue Einstellung | S | ✅ 3.33.20 |

#### C. Unterstützung im Alltag

| ID | Paket | Abnahme (Auszug) | Aufwand | Stand |
|---|---|---|---|---|
| AU01 | Tagesvorschlag „Was passt heute?“ mit Grund je Zeile | deterministisch; nichts ohne Bestätigung; ein Undo-Schritt | M | ✅ 3.33.14 |
| AU02 | Verfügbare Zeit in allen Planungswegen | eine Rechenstelle (`planning_summary`) | S–M | ✅ 3.33.13 |
| AU03 | Geführter Tagesbeginn (Rückblick → Vorschlag → Zeitblöcke) und optionaler Hinweis zu Tagesbeginn/-abschluss | Hinweise nach D20 | M | ✅ 3.39.0 geliefert; Mac/Linux/Windows automatisch grün, Menschen-/DPI-Abnahme getrennt offen |
| AU04 | Wochenplanung im eingebetteten Kalender mit Kapazitätsbalken | Teil von N04 | M | ✅ 3.33.17 |
| AU05 | Fokussitzung mit nächster Aufgabe (= G05) | Zeit genau einmal gebucht | M | ✅ 3.33.14 |
| AU06 | Routinen als Abschnitt in „Heute“ | kein Formatwechsel | M | ✅ 3.33.20 |
| AU07 | Termine aus einer ICS-Datei als belegte Zeit im Stundenraster | berührt die Produktgrenze „ICS ist Dateiaustausch“ | M–L | ✅ 3.39.0 geliefert; Mac/Linux/Windows automatisch grün, Menschen-/DPI-Abnahme getrennt offen |

**Fertig (Programm), wenn:** Ein Tag lässt sich aus „Heute“ in höchstens drei Schritten planen ✅ (3.33.14); die verfügbare Zeit ist überall sichtbar, wo geplant wird ✅ (3.33.13); die Bedienfläche aus §10 ist mit 3.38.0 automatisch auf Mac/Linux/Windows geprüft und erreicht; übrige Messgrenzen/Abnahmen siehe §10; der Inhaber hat jede Welle gestalterisch abgenommen (OB06) – offen.

### 4.4 Größere Umsetzungspakete (Auftrag 07.10.2026)

Der Inhaber beauftragt mehrere zusammengehörige Features je Umsetzung, abgeleitet aus Analyse, Recherche und Konkurrenzdokumenten; innerhalb dieses Auftrags braucht es keine erneute Freigabe jeder Teilfunktion. Offene Produktentscheidungen bleiben offen. Geliefert als 3.33.14–3.33.18 und im Sprint 3.33.19–3.35.0 (§14).

**Prüfstrategie pro Paket:** gezielte Baselines der betroffenen Bereiche vor Produktionsänderungen; Unit-Tests und echte Bedienwege je Teilfunktion; eine Pflichtsuite mit Gegenprobe gegen die Vorversion; ein gemeinsamer eingefrorener Volllauf mit vollständiger Regression, Interaktions-/Fehler-/Undo-/Neustartprüfung, Mindestgröße, großer Schrift, hell und dunkel sowie Messung. Erst danach Python, Showcase und Bundle liefern. Weitere Vollläufe nur nach ausführbaren Änderungen oder einem Fehlerbefund; keine künstlichen Zwischenversionen. Native und menschliche Abnahme getrennt ausweisen.

## 5. Wissen im Kontext (Stufe 2)

| ID | Arbeit | Stand |
|---|---|---|
| N05 = U12 | Ein Inspektor statt Maske + Detailbereich | ✅ 3.38.0 geliefert; Mac/Linux/Windows automatisch grün, Menschen-/DPI-Abnahme getrennt offen |
| G14 = D-01 | Inhaltssuche, gemeinsame Befehlspalette, Treffer im Dokument hervorheben | ✅ 3.33.7 / 3.33.16 / 3.34.0; FTS5 nach Messung nicht nötig (P07) |
| D-03 | Erklären, warum ein Filter einen Punkt zeigt oder ausblendet | ✅ 3.34.0 (gespeicherte Filter) |
| G08/G30 = D-02 | Seiten-, Listen- und Aufgabenverweise mit Rückverweisen (Format 22) | ✅ 3.33.17 |
| G28 = E-01 | Live-Liste in einer Seite (Originalaufgaben) | ✅ 3.33.18 |
| G09 = E-02 | Titelbild für Seiten und Bibliothekskarten, auch als Pixelzeichnung | ✅ 3.33.18 |
| U08 = E-03 | Vorlagen im Anlegen-Weg mit gefüllter Vorschau | ✅ 3.33.18 |
| N04 = U11 + B-03 | Kalender als eingebettete Ansicht, Ziehen auf Tage, freie Zeitfenster | ✅ 3.33.17 |
| U09, U15, U18 | Kompakte Pinnwandleiste, Lila nur für Hinzufügen, Seitentitel im Dokument | ✅ 3.33.21 |
| B4 | Bilder in Seiten: keine Überlappung, Bilder in Druck/PDF und Markdown | ✅ 3.34.0 |

## 6. Pixel, Austausch, Verteilung (Stufen 3–4)

| ID | Arbeit | Stand |
|---|---|---|
| G19 = G-01 | Paletteneintrag ändern färbt die Zeichnung um, mit Vorschau und Undo | ✅ 3.35.0 |
| G-03 | Symbolvorschau in 16/32/48 px vor dem Export | ✅ 3.35.0 |
| G17 = G-02 | Animation: Frames, Dauer, Vorschau | ✅ E-S1 A/V durch D18; 3.40.0 geliefert |
| G24 = F-01 | KI-Austausch Stufe 2: Kontextpaket, Änderungsvorschläge mit Feldvergleich (Q3) | ✅ 3.35.0 |
| G21 = F-02 | Begrenzter Notion-Import mit Verlustbericht und Wiedererkennung | ✅ 3.41.0 im damaligen Lieferumfang; D26/D39, I6 offen |
| F-03 | Zwei Sicherungsstände lesbar vergleichen | ✅ 3.35.0 |
| G26 = H-03 = N11 | Paket mit eingebettetem Python 3.14 + Tk 9 je Plattform (D15) | ✅ 3.42.0; neuere Python-Fassung und vorhandene Pakete getrennt, aktueller Lieferabgleich §18 |
| – | Windows-/Linux-Abnahme, Linux-App (AppImage/Flatpak später) | ○ Inhaber |
| H-01 | Kontrollmatrix echter Bedienwege fortführen | laufend |

## 7. Zukunft und bewusst nicht

| ID | Thema | Marke | Grund / Auslöser |
|---|---|---|---|
| N12 = U23 | Screenreader und beschriftete Canvas-Bedienung über Tk 9.1 `tk accessible` | ▶ | Aufgaben-Kernablauf als erste Stufe gewählt (D36); G26 und tatsächliche Readerabnahme erforderlich |
| N13 | Einzelne Seite aus vorhandener Sicherung wiederherstellen | ✅ 3.41.0 | vollständig gewählt (D37); Text, Bilder/Anhänge, Aufgabenverweise, Live-Listen; kein fortlaufendes Versionssystem; I6 offen |
| – | SQLite als Hauptspeicher | ◇ | nur bei realen Beständen über 20.000 Punkten (D16) |
| G25, Mobile | Toolkit-Probe, iPhone/iPad | ◇ | D03 aufheben |
| G18, G15, G10 | Kachelsatz, Filter in Alltagssprache, Registerkarten-Block | ◇ | Vorrat |
| G06 | Gewohnheiten | ◇ | vorerst nicht; Routinen in „Heute“ (AU06) seit 3.33.20 decken den Alltagsbedarf ohne Statistik |
| B1 | Seitenleiste als Ganzes scrollen | ◇ | wenn die kleinen Bereiche im Alltag stören |
| B7 | Tk-Fehler (Rahmen einer ausgeblendeten Leinwand) an Tcl/Tk melden | ○ | braucht ein Konto bei core.tcl-lang.org |
| N09 | Erinnerungen bei geschlossener App (Stufe C) | ✕ | Produktgrenze |
| N10 | Lokaler MCP-Server | ✕ | Q3: Dokumente statt Schnittstelle |
| N14 = G07 | Systemweiter Erfassungs-Hotkey | ✕ | nur plattformeigen lösbar (Q2) |
| N06 | „Erste Schritte“-Seite, Einstieg für neue Nutzer | ✕ | bewusst nicht gewählt; Rundgang und Showcase vorhanden |
| G23 | Gleichzeitige Bearbeitung auf zwei Geräten | ✕ | Produktgrenze |
| G22 | Verschlüsselte Ablage | ✕ | keine Priorität |
| G12, G13 | Spalten in Seiten, Graph | ✕ | Entscheidungen 29./30.09.2026 |
| ZF-200 | Eigene Felder je Liste | ✕ | am 25.09.2026 nicht gewählt |
| N15–N20 | N15 Sprache, N16 Gewohnheitsstatistik (=G06, vorerst), N17 Team, N18 freie Felder, N19 Unterseiten/Graph, N20 Web Clipper | ✕ bzw. zurückgestellt N16 | konkrete Produktgrenzen; Cloud-KI separat durch Q3 ausgeschlossen |

## 8. Abhängigkeiten und Regeln

- **Referenz- und Löschregeln:** Eine Aufgabe hat genau einen Heimatort (Liste, Seite oder Notiz), andere Orte zeigen einen Verweis. Entfernt man eine Verweiszeile, entfällt nur der Verweis. Entfernt man die Zeile am Heimatort, wandert die Aufgabe in den Papierkorb; Verweise zeigen „im Papierkorb“ bzw. nach endgültigem Löschen „Ziel fehlt“. Undo stellt beides zusammen her.
- **Datenformat-Tore:** Format 21 (Aufgabenverweise), 22 (allgemeine Verweise), 23 (Live-Listen/Titelbild), 24 (Animation) und 25 (Importquellen) sind vergeben. FP-02 benötigt bei seinem tatsächlichen Formatschnitt die nächste freie Nummer, Vorsicherung, Migration und schreibgeschützten Altleser; keine Nummer vorab vergeben.
- **Erfüllte Voraussetzungen:** D07/D18 → G17, D26 → G21, D15/D27 → G26 und I7/D21 → OB02/OB03/N05/KO04 sind umgesetzt. Offen bleiben N12-Abschluss auf dem aktuellen UI-Stand, WA-09 vor FP-04 und die neue Ablaufplanung nach dem Abschlussauftrag vom 15.10.; aktuelle Folge §19.

## 9. Risiken

| Nr. | Risiko | Gegenmaßnahme |
|---|---|---|
| R1 | Regressionen in der Klasse `ListApp` (46.929 Zeilen allein in `ListApp` am lokalen c0252ba (AST-Abgrenzung; Gesamtdatei separat)) | kleine Schnitte, echte Bedienproben, Vollprüfung je Paket, Fachlogik als Tk-freies Modul (D17) |
| R2 | Beschriftungs- oder Positionswechsel löst die falsche Aktion aus | stabile Aktionskennungen seit 3.33.11; Suchtreffer über ID neu auflösen |
| R3 | Neue Dokumentinhalte gehen in älteren Fassungen verloren | Datenformat-Tore (§8) |
| R4 | P08b übersieht einen Änderungsweg | Vollvergleich im Autosave, Differenztest |
| R5 | Plattform- und Menschenabnahme fehlen | neuer Sprint: Mac-Vollprüfung, ausführbare Linux-Matrix und native Windows-Vollprüfung je Paket (D35/D42); tatsächliche Bedien-/Readerabnahme getrennt (I6) |
| R7 | Umfang wächst | Klassifizierung, Prinzipien-Check mit Vorgeschichte |
| R9 | Gewohnheitsbruch durch D10/D12/D14 | Bestandseinstellungen bleiben; Karte „Neu in Glide“ (N07) |
| R10 | Namenskollision „Glide“ | Markenprüfung durch den Inhaber (I4) |
| R11 | Linux-Messungen nicht auf den Mac übertragbar | Abnahme auf dem Referenz-Mac |
| R12 | Gestaltungsumbau ohne Referenzentwurf erzeugt Nacharbeit | I7 vor OB02/OB03; Gestaltungsabnahme OB06 |
| R13 | Tagesvorschläge wirken bevormundend | AU01 schlägt nur vor, nennt den Grund, ändert nichts ohne Bestätigung |
| R14 | Mehr Funktionen in der großen `ListApp` | neue Fachlogik nur als Tk-freies Modul (D17); je Paket „was verschwindet dafür“ |
| R15 | Uneingecheckter Arbeitsstand: die Aufbewahrung entfernt planmäßig Nachweise, die nie in Git waren (3.33.13–3.33.16) | nach jeder Lieferung committen |

## 10. Messbare Ziele

| Bereich | Ziel | Stand (Beleg) |
|---|---|---|
| Abhaken 1.000 / 5.000 / 10.000 Punkte | ≤ 50 / 120 / 200 ms | ✅ 17 / 61 / 118 ms (Referenz-Mac, 3.33.19) |
| Suche bis zur gezeichneten Trefferliste, 10.000 Punkte | ≤ 100 ms | ✅ 66,6 ms Median, p95 73,1 ms (Referenz-Mac, 3.34.0) |
| Erstes Speichern, 10 MB | ≤ Folgespeichern + 50 ms | ✅ ohne Zusatz-Parse seit 3.33.0 |
| Startseite aufbauen | warm ≤ 150 ms; kalt direkt ≤ 300/Kindprozess ≤ 500 ms (D46) | ✅ 3.36.0: direkt kalt 266/282 ms, warm 75/88; Kindprozess 483/493 und 75/90 (Median/p95) |
| Tabellenansicht öffnen, 5.000 Punkte | ≤ 400 ms | 292 ms (Linux, Messung zu T8); seit P09a nicht als Ganzes neu gemessen |
| Kopfzeilen-Symbolknöpfe | ≤ 4 | ✅ seit 3.33.16 |
| Bedienfläche über Inhalt (1280 × 800; 840 zusätzlich) | ≤ 15 % | ✅ 3.38.0: sechs Ansichten 14,125–14,625 %, Mac/Linux/Windows automatisch grün; Menschenabnahme getrennt offen |
| Startseitenkacheln im Standard | 8 (D12 fortgeschrieben durch B04/D50) | Code seit 3.43.0; eigene Auswahl bleibt, menschliche Abnahme I6 |
| Symbole mit mehreren Bedeutungen | 0 (Bewegungspfeile ausgenommen) | ✅ seit 3.33.16 |
| Tag aus „Heute“ planen (Tagesbeginn → Vorschlag → Zeitblöcke) | ≤ 3 Schritte | ✅ 3.33.14 (automatisch geprüft; menschliche Abnahme I6) |
| Verfügbare Zeit beim Einplanen sichtbar | in allen Planungswegen | ✅ 3.33.13 |
| Abstandswerte in den Hauptansichten | nur Werte der Skala aus OB01 | ◐ Startseite, Bibliothek, Einstellungen, Schnellerfassung 134 → 3 direkte Zahlen (3.33.21) |

## 11. Nur durch den Inhaber

| Nr. | Aufgabe | Stand |
|---|---|---|
| I1 | Inhaberangaben bestätigen | ○ Vorschläge in [Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md#inhaberangaben) |
| I2 | Lizenzbedingungen veröffentlichen | ○ Entwurf: kostenlos für private, nicht kommerzielle Nutzung |
| I3 | Apple-Developer-Konto, Windows-Code-Signing-Zertifikat | ○ |
| I4 | Markenprüfung „Glide“ | ○ Fachanwalt für Markenrecht |
| I5 | Aktuelles Python auf dem Mac installieren | ◐ Referenz-Mac mit Python 3.14.5/Tk 9.0.3 trägt die Volläufe; python.org führt 3.14.8 (Windows-Absturz W09 beobachten); Installation braucht das Passwort des Inhabers |
| I6 | Windows-Vollprüfung des aktuellen Stands und manuelle Prüfsitzungen | ▶ Windows je neuer Lieferung gewählt (D42); native Vollprüfungen 3.36.0–3.38.0 grün; Folgepakete jeweils erneut prüfen. Tatsächliche Sicht-/Bedien-/Readerabnahme getrennt nach der [Prüfliste](Glide_Manuelle_Pruefung.md) |
| I7 | Referenzentwürfe für „Heute“, Liste, Seite und Inspektor | ✅ Bild 1 gewählt (D19/D21); vier Funktionen D22–D25 vollständig mit 3.38.0 geliefert, Mac/Linux/Windows automatisch grün; Menschen-/DPI-Abnahme getrennt offen |
| I8 | Lösungsweg für das Logo unter Tk 8.6 (LG01–LG04) | ✅ technische Wege D28 und Master/Kleingrößen D41/D45 in 3.37.0 geliefert; Menschen-/DPI-Abnahme getrennt |
| I9 | Rechte an Fremdbildern im öffentlichen Repository (`20_Grafik_Master/05_Inspiration`, `06_Beispielbilder`, die sechs Showcase-Motive) | ○ behalten mit Rechtenachweis oder entfernen und den Showcase mit eigenen Motiven neu erzeugen; Empfehlung: ohne Nachweis entfernen |
| I10 | Git-Historie bereinigen (gelöschte Protokolle mit Benutzerpfaden, frühere Archivkopien) | ○ eigener Auftrag; ändert alle Commit-Kennungen ([Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md#github-auftritt)) |
| I11 | GitHub-Auftritt: Beschreibung, Tags, Wiki, Issues, KI-Codeprüfung | ○ Empfehlungen in der [Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md#github-auftritt) |
| A–H | Bearbeitungstiefe der Auswahl vom 30.09.2026 (A Tempo · B Planen und Fokus · C Aufgaben im Text · D Suchen und Wissen · E Projektseiten · F Austausch und Sicherungen · G Pixel-Werkstatt · H Bedienkontrolle und Auslieferung) | beauftragte Teile umgesetzt (Aufgaben A-01 bis H-03 mit Status oben); weitere Tiefe je Richtung entscheidet der Inhaber |

**Entscheidungen und Auswahlstand** (Stand 12.10.2026; Empfehlungen sind keine Entscheidungen):

| Nr. | Frage | Blockiert | Empfehlung |
|---|---|---|---|
| E-S1 | D07: Animationsexport | G17 | entschieden 10.10.2026: A/V, D18; 3.40.0 geliefert |
| E-S2 | I7: Referenzweg und Auswahl der vier Oberflächenfunktionen | OB02, OB03-Rest, N05, KO04 | Referenzweg und Bild 1 entschieden (D19/D21); vier Funktionen D22–D25 in 3.38.0 geliefert, automatisch Mac/Linux/Windows grün |
| E-S3 | AU03: Vorgabe und Tiefe automatischer Tageshinweise | AU03-Rest | entschieden 10.10.2026: A/V, D20; in 3.39.0 geliefert |
| E-S4 | G21: erste Importquelle | G21 | entschieden 10.10.2026: Notion A/V, D26; 3.41.0 geliefert; Mac/Linux/Windows automatisch grün |
| E-S5 | D15/G26: Bauwerkzeug | G26, N12 | entschieden 10.10.2026: PyInstaller 6.22.3, beide Zielsysteme A/V, D27 |
| E-S6 | I8: Logo-Rückfall unter Tk 8.6 | LG01–LG04 | D28/D41 gewählt, Gestaltung D45 freigegeben; 3.37.0 geliefert |
| E-S7 | A14: Symbolschrift | einheitliche Symbolgröße | Systemzeichen, gesamte Tabelle D29 in 3.37.0 geliefert |
| E-S8 | AU07, OB04 | AU07, OB04 | D30/D31 vollständig gewählt; OB04 in 3.38.0 geliefert, AU07 in 3.39.0 geliefert |

## 12. Pflege

- Bei jeder Produktionsrunde Statusmarken, Abschnitt 2 und die Ziele nachführen; nach der Lieferung Zwischenstände löschen (Git trägt sie). Keine datierte Kopie.
- Neue Ideen erst nach dem [Prinzipien-Check](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md#prinzipien-check-für-neue-funktionen) und mit Marke aufnehmen.
- Neue Entscheidungen gehören in die [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md), nicht hierher.

## 13. Abgleich mit dem ursprünglichen Zukunftsdokument

Original vollständig aus der Git-Historie gelesen: „Glide – KI-Austauschformat und Zukunftsarchitektur“, frühere Datei `00_Arbeitsvorbereitung/Archiv/Glide_KI_Austauschformat_und_Zukunftsarchitektur_Dublette_2026-09-18.md`, Commit `569020ef65880b28a50408e229a8027ba2a65898`. Die späteren namensähnlichen Fassungen waren nur Verweise. Die ursprünglichen Beispiele beziehen sich auf Format 15 und sind keine aktuellen Formatverträge. [Original in Git](https://github.com/n05a-design/glide-to-do/blob/569020ef65880b28a50408e229a8027ba2a65898/00_Arbeitsvorbereitung/Archiv/Glide_KI_Austauschformat_und_Zukunftsarchitektur_Dublette_2026-09-18.md).

| Ursprüngliche Idee | Heutiger Code / Entscheidung | Konsequenz |
|---|---|---|
| Internes Format, Exchange und KI-Beschreibung trennen | `DATA_SCHEMA_VERSION = 25`, `EXCHANGE_FORMAT_VERSION = 1` (Änderungsvorschläge 2), `exchange_manifest`, erzeugte Spezifikation vorhanden | ✅ Grundlage erhalten; neue Funktionen nicht automatisch zum Exchange-Vertrag erklären |
| Create mit freien Schlüsseln statt erfundener UUIDs | `parse_exchange_document`, Preview und Import; echte IDs werden von Glide vergeben | ✅ kein neuer Importweg nötig |
| Capability Registry, unbekannte Felder sichtbar | `exchange_capabilities`, Feldlisten, Importbericht; Anhänge/Repeat/Reminder bewusst Stufe 0, `patch_mode` 1 seit 3.35.0 | ✅ Registry, Spezifikation und Verlustbericht mit G24 weitergeführt |
| `.glidecontext` plus geprüfte Patch-Operationen | Kontextpaket und Änderungsvorschlag seit 3.35.0 (`exchange_patch.py`) | ✅ G24: Auswahlumfang, Prüfsummen, Ausgangsstand, Feldvergleich, Vorsicherung, ein Undo-Schritt; Konflikte nie still überschrieben |
| Echte Notizen je Aufgabe, getrennt von Beschreibung | Eigenständige Notizlisten/Seiten vorhanden; kein datiertes `item.notes[]`-Modell | ◇ ZF-NOTES: optionaler Wissensausbau nach G29/Verweisen; erst konkreten Bediennutzen, Migration, Lösch- und Exchange-Regeln definieren. Keine zweite Beschreibung ergänzen |
| Unteraufgaben mit `children`, keine zweite `subtasks`-Struktur | rekursive Aufgaben, Klappkontrolle und Strukturmutationen vorhanden | ✅ Datenstruktur behalten; H-02 prüft die verbleibenden Tastaturwege |
| Dynamische Pinnwand statt Aufgabenkopien | vorhandenes Board nutzt echte Aufgaben, Quellen/Filter/Gruppierung | ◐ ursprüngliches Ziel weitgehend erreicht; kein zweiter Board-Inhaltstyp |
| Allgemeines ViewDefinition-Modell | vorhandene Ansichten/Filter, D17 verbietet Großumbau | ◇ nur gleiche Quellen-, Filter- und Sortierlogik schrittweise extrahieren; kein Architekturprojekt ohne gemessenen Nutzen |
| Tabellenbreiten und gemeinsame UI-Bausteine | `table_column_widths`, `table_sort`, `ThemedAutoScrollbar`, `DropdownPopup` vorhanden | ◐ vorhandene Bausteine weiterverwenden; Fokus/Trackpad/Kontrast über echte Bedienwege prüfen |
| Labelbeschreibungen und eigene Felder | Label-Felder derzeit key/name/color; eigene Felder je Liste später bewusst nicht gewählt | ◇ ZF-LABEL: Beschreibungen nur mit belegtem Bedarf; ✕ eigene Datenbankfelder gemäß Produktgrenze. Historische Vorschläge überschreiben keine spätere Entscheidung |
| Eigener KI-Bereich, Plugins/API und Systemintegration | Dateimenü enthält die Austauschwege; Q3 entscheidet Dokumente statt Schnittstelle | Kein neuer Hauptbereich nötig; Kontextpaket/Änderungsvorschlag im vorhandenen Dateiaustausch, kein MCP-/Cloud-/API-Auftrag daraus ableiten |

## 14. Sprint ab 08.10.2026: Aufgabenkatalog

**Auftrag des Inhabers vom 08.10.2026** (Kern im Wortlaut): „Führe auf dieser Grundlage anschließend einen langfristigen, umfangreichen Feature-Sprint durch.“ Verlangt waren Analyse ([Analyse](Glide_Analyse.md)), Recherche ([Markt und Vorbilder §7](Glide_Markt_und_Vorbilder.md#7-alltagsabläufe-und-konsequenzen-für-glide)), dieses Aufgabendokument und die vollständige Umsetzung mit Prüfung. Umfang: alle offenen Aufgaben der Stufen 0–4 ohne offene Inhaberentscheidung, dazu die Analysebefunde. **Umgesetzt und geliefert 3.33.19–3.35.0 am 09.10.2026.** Die Aufgabenkarten (Ausgangslage, Nutzen, Umfang, Akzeptanz, Prüfung) sind nach der Lieferung gelöscht; sie stehen in Git (Commit `6098877`).

### 14.1 Übersicht

| Phase / Version | ID | Titel | Prio | Abhängig von | Status |
|---|---|---|---|---|---|
| 0 ohne App-Version | A01 | Dokumentinhalte aus `main` (PR #15) in den Arbeitsstand übernehmen | P1 | – | ✅ 08.10.2026 |
| 0 | PR01 | Native Mac-Vollprüfung 3.33.18 und Bundle 3.33.18 | P1 | – | ✅ 09.10.2026 Exitcode 0 (93/95, 2 übersprungen), Bundle 3.33.18 signiert und SHA-256-gleich; menschliche Abnahme I6 offen |
| 0 | W10 | Aufbewahrungswerkzeug: Verknüpfungsprüfung nur innerhalb der Ablage | P1 | – | ✅ 08.10.2026 |
| 0 | W11 | Kommentare zur Tastaturabschirmung in `pruefen.py`/`sitecustomize.py` berichtigen | P3 | – | ✅ 08.10.2026 |
| 0 | W02 | Tests auf `set_design` umstellen (Dunkelfälle wirklich dunkel) | P2 | – | ✅ Mac und native Windows-Vollprüfung 3.36.0 grün; Dunkelfall mit Luminanzprüfung, menschliche Sicht offen |
| 0 | W03 | Zeilenenden für die ganze Ablage festlegen | P3 | – | ✅ 08.10.2026 |
| 0 | W04 | CI-Wächter gegen Synchronisationskopien und geschrumpfte Hauptdokumente | P2 | – | ✅ 08.10.2026 |
| 0 | W12 | Lieferabsatz in `07_Python-Versionen/README.md` nicht vergessen (Befund A15) | P3 | – | ✅ 09.10.2026: `abgleich_07.py` bricht ab, solange die README die gelieferte Hauptdatei nicht nennt; Reihenfolge in `scripts/pflege/README.md` |
| 0 | W13 | Standprüfung R10: die README in `07_Python-Versionen` folgt den Modulen dieses Ordners, nicht dem Quellbaum (CI zwischen zwei Lieferungen sonst rot) | P2 | – | ✅ 09.10.2026, Werkzeugtest ergänzt |
| 0 | W14 | Altleser-Proben mit Vorversionen außerhalb der Aufbewahrung (Befund A18) | P1 | – | ✅ 09.10.2026 `tests/integration/vorversion.py` |
| 0 | W15 | Sperrdatei-Zählung in `test_tempo33319` unabhängig vom Sekundenwechsel (Befund A19) | P2 | – | ✅ 09.10.2026 |
| 0 | DOK3 | Dokumentation inhaltlich nachführen (Analyse A02–A13) | P2 | A01 | ✅ 09.10.2026 (A02–A13 erledigt, laufend mit A15–A22; A14 in 3.37.0 umgesetzt, native Menschen-/DPI-Sichtprüfung getrennt) |
| 1 → 3.33.19 Tempo | P04 | Bildlayout nur bei geänderter Geometrie, Platzieren beim Scrollen | P1 | PR01 | ✅ 09.10.2026 3.33.19: 30 Bilder, Tippen fern 267–273 → 2,5–3,9 ms, im Umfluss 275 → 22–43 ms |
| 1 | P06r | Doppelte Aktualisierungs-/Schreibanforderungen je Aktion beseitigen | P1 | PR01 | ✅ 09.10.2026 3.33.19: je Aktion ein Seitenleistenaufbau und ein Einstellungsschreiben (Duplizieren zwei) |
| 1 | P03r | Unveränderte Startseitenkacheln behalten statt neu bauen | P2 | PR01 | ✅ 09.10.2026 3.33.19: ohne Änderung 502–517 → 0,2–0,3 ms, Wechsel 543–561 → 273–297 ms |
| 1 | E01 | Einstellungsfenster schneller einblenden (heute ≈ 2,1 s) | P2 | PR01 | ✅ 09.10.2026 3.33.19: Mac 677 → ≈ 560 ms; Rest Tk-Zeichnen, als Grenze dokumentiert |
| 1 | P08c | Abhaken bei 5.000 Punkten messen und dem Ziel 120 ms nähern | P2 | PR01 | ✅ 09.10.2026 gemessen: 61 ms (Sprint) bzw. 112–119 ms (Akku, Hintergrund); Ziel erreicht, keine Änderung nötig |
| 1 | P01r | Messbasis um Verlaufsvarianten und Speicherentwicklung ergänzen | P3 | – | ✅ 09.10.2026: Verlauf an/aus, Arbeitsspeicher, 1.000/5.000/10.000 Punkte im Nachweis 3.33.19 |
| 2 → 3.33.20 Komfort und Alltag | KO02 | Wiederholungen: Termin überspringen, verpasste Termine überspringen, frühes Erledigen | P2 | – | ✅ 09.10.2026 3.33.20 (Kontextmenü, Detailbereich, Menü, Palette; Befund „Als erledigt markieren“ in Übersichten behoben) |
| 2 | KO03 | Erinnerung in der Schnelleingabe als Chip | P2 | – | ✅ 09.10.2026 3.33.20 |
| 2 | KO05 | Mehrzeiliges Einfügen in die Eingabezeile mit Rückfrage | P2 | – | ✅ 09.10.2026 3.33.20 |
| 2 | KO06 | Zuletzt benutzte Ziele zuerst (Verschieben, Labels) | P3 | – | ✅ 09.10.2026 3.33.20 |
| 2 | U04 | „+“-Knopf und Umschalt+Enter statt zweier Textknöpfe | P3 | – | ✅ 09.10.2026 3.33.20 (Menüweg „Neuer Punkt mit allen Angaben …“ neu (fehlte bisher)) |
| 2 | U20 | Leerzustand ohne doppelten Anlegen-Knopf | P3 | – | ✅ 09.10.2026 3.33.20 |
| 2 | N07 | Einmalige Karte „Neu in …“ nach einem Update | P3 | – | ✅ 09.10.2026 3.33.20 |
| 2 | AB08 | Mindestversion Python/Tk beim Start prüfen | P2 | – | ✅ 09.10.2026 3.33.20 (Startprobe mit Python 3.9 grün) |
| 2 | AU06 | Routinen als Abschnitt in „Heute“ | P2 | G05 ✅ | ✅ 09.10.2026 3.33.20 |
| 3 → 3.33.21 Ruhige Oberfläche | N01 | „Automatisch (hell/dunkel)“ nach System, Signaturdesign vorn | P2 | – (A04) | ✅ 09.10.2026 3.33.21 (Paar aus dem gewählten Design, Erkennung je System, Pixel vorn) |
| 3 | U15 | Lila nur für Hinzufügen, aktiver Zustand neutral | P3 | – | ✅ 09.10.2026 3.33.21 (neutrale Rolle `active`) |
| 3 | U05r | Gismo-Kachel kompakter, Pflegeknöpfe bei Bedarf | P3 | – | ✅ 09.10.2026 3.33.21 |
| 3 | U09 | Kompakte Pinnwandleiste | P3 | – | ✅ 09.10.2026 3.33.21 (eine Werkzeugzeile, Menü „…“) |
| 3 | U18 | Seitentitel im Dokument, Schreibhinweis in leerer Seite | P3 | – | ✅ 09.10.2026 3.33.21 |
| 3 | OB05 | Schmale Seitenleiste mit Symbolen | P3 | UX1 | ✅ 09.10.2026 3.33.21 |
| 3 | OB01r | Gestaltungsskala in weiteren Ansichten | P3 | OB01 | ✅ 09.10.2026 3.33.21 (Startseite, Bibliothek, Einstellungen, Schnellerfassung wertgleich auf `SPACING`, direkte Zahlen 134 → 3) |
| 3 | W05 | Breite Dialoge, Knopfreihe rechts | P3 | – | ✅ 09.10.2026 3.33.21 (auf dem Mac bestätigt mit 1251/1504 px, jetzt 520/620 px, Knöpfe rechts) |
| 3 | W07 | Doppelter Hinweis nach „Ganzes Bild zeigen“ | P3 | – | ◇ auf dem Mac nicht nachstellbar (ein Hinweis); bleibt für die Windows-Sichtprüfung B1a |
| 3 | W08 | Pixelsymbol-Raster füllt den Dialog | P3 | – | ◇ auf dem Mac nicht nachstellbar (Raster füllt den Dialog, Zoom 32×); bleibt für die Windows-Sichtprüfung B1a |
| 4 → 3.34.0 Wissen und Seiten | B4 | Bilder in Seiten: keine Überlappung, Bilder in Druck/PDF und Markdown | P2 | – | ✅ 09.10.2026 3.34.0 (Bilder weichen vorigen aus; Druckseite mit Daten-URL; Markdown mit Bildverweisen und Rückweg als Seitenbilder) |
| 4 | G14h | Suchtreffer im Dokument hervorheben | P2 | G14 | ✅ 09.10.2026 3.34.0 (alle Fundstellen markiert, Esc/Tippen hebt auf, nie gespeichert) |
| 4 | P07 | FTS5-Cache nur nach gemessener Suchlatenz | P3 | G14h | ✕ 09.10.2026 nach Messung: Median 66,6 ms, p95 73,1 ms (3.33.21: 100,8 ms); kein FTS5-Index |
| 4 | D-03 | Erklären, warum ein Filter einen Punkt zeigt oder ausblendet | P3 | – | ✅ 09.10.2026 3.34.0 („Warum steht das hier?“, „Ausgeblendet: N“, „Filter erklären …“; einfache Listensuche ohne Erklärdialog) |
| 4 | H-02r | Tastaturwege für Pinnwand und Seitenbäume | P2 | – | ✅ 09.10.2026 3.34.0 (Bereichsbäume wie Listenbaum, lose Seiten in den Ordner darunter; Hinweis mit Rückgängig. Abweichung von der Karte: Wirkung erscheint beim Ausführen statt vorher, und Pfeile ohne Alt wählen weiter Karten – Alt+Pfeile bewegen) |
| 4 | N08 | JPEG-Vorschau unter Linux über ein Systemwerkzeug | P4 | – | ✅ 09.10.2026 3.34.0 (Mac mit erzwungenem Linux-Weg; Linux-Sichtprüfung offen) |
| 5 → 3.35.0 Pixel | G19 | Palettenfarbe ändern färbt die Zeichnung um | P3 | – | ✅ 09.10.2026 3.35.0 (Doppelklick oder Umschalt+Klick, Vorschau vor dem Bestätigen, Ablehnen ohne Spur; Dreifachklick abgefangen) |
| 5 | G-03 | Symbolvorschau 16/32/48 px vor dem Export | P3 | – | ✅ 09.10.2026 3.35.0 (hell/dunkel, Original und doppelt, pixelgleich zur ICO-Datei) |
| 6 → 3.35.0 Austausch (mit Paket 5) | G24 | KI-Austausch Stufe 2: Kontextpaket und geprüfte Änderungsvorschläge | P2 | – | ✅ 09.10.2026 3.35.0 (Kontextpaket auch der Auswahl, Prüfdialog mit Konflikten, Vorsicherung, ein Undo; Spezifikation im Datenvertrag) |
| 6 | F-03 | Zwei Sicherungsstände lesbar vergleichen | P3 | – | ✅ 09.10.2026 3.35.0 (Bestand, automatische Sicherungen, Dateien; nur lesend) |
| Abschluss | ABS | Abgleich Aufgabendokument ↔ Code ↔ Prüfergebnisse | P1 | alle | ✅ 09.10.2026 (§14.2: Abweichungen benannt, Offenes aufgelistet) |

### 14.2 Abschlussabgleich ABS (09.10.2026)

Jede Zeile aus 14.1 gegen Code, Prüfung und Nachweis abgeglichen. Quelle der Prüfzahlen sind die eingefrorenen Mac-Volläufe (Referenz-Mac, Python 3.14.5, Tk 9.0.3, künstliche Daten); Nachweise unter `01_Repository/Glide/tests/qa-<Version>/`.

| Version | Aufgaben | Einstieg im Code (Auswahl) | Pflichtsuite, Gegenprobe | Volllauf, Lieferung |
|---|---|---|---|---|
| 3.33.19 Tempo | P04, P06r, P03r, E01, P08c, P01r | `layout_images` (inkrementell), `settings_write_batch`, Startseitenkacheln behalten | `test_tempo33319`, gegen 3.33.18 rot | Exit 0, 94 ausgeführt; 07, Showcase, Bundle SHA-256-gleich |
| 3.33.20 Komfort | KO02, KO03, KO05, KO06, U04, U20, N07, AB08, AU06 | `repeat_rules.py`, `capture_parser.py`, `routines.py`, `release_notes.py`, `runtime_check.py` | `test_komfort33320`, gegen 3.33.19 rot | Exit 0, 95 ausgeführt; gleich geliefert |
| 3.33.21 Ruhige Oberfläche | N01, U15, U05r, U09, U18, OB05, OB01r, W05 | `appearance.py`, `with_active_role`, `board_controls`, `PageEditor.title_label`, `sidebar_rail` | `test_oberflaeche33321`, gegen 3.33.20 rot | Exit 0, 96 ausgeführt (nach W14/W15); gleich geliefert |
| 3.34.0 Wissen und Seiten | B4, G14h, D-03, H-02r, N08; P07 ✕ | `image_push`, `build_page_print_html`, `page_document_from_markdown`, `highlight_matches`, `filter_explain.py`, `keyboard_sidebar_move`, `preview_tools.py`, `content_search._original_index` | `test_wissen3340`, gegen 3.33.21 rot | Exit 0, 97 ausgeführt; gleich geliefert |
| 3.35.0 Pixel und Austausch | G19, G-03, G24, F-03 | `drawing_replace_color` + `DrawingModel.discard_open_action`, `drawing_icon_preview`, `exchange_patch.py` + `show_exchange_patch_dialog`, `backup_diff.py` + `show_backup_compare_dialog` | `test_pixel3350`, `test_austausch3350`, beide gegen 3.34.0 rot | Exit 0, 99 ausgeführt; 07 (37 Code-Dateien), Showcase, Bundle SHA-256-gleich |

**Abweichungen von den Aufgabenkarten (benannt, nicht stillschweigend; die Karten stehen in Git, Commit `6098877`):**

- **H-02r:** Ziel und Wirkung erscheinen beim Ausführen als Hinweis mit „Rückgängig“, nicht vorher – eine Vorabfrage je Tastendruck würde die Tastaturbedienung bremsen. Pfeile ohne Alt wählen auf der Pinnwand weiter Karten (wie in Liste und Seitenleiste); Alt+Pfeile bewegen. Wer eine Vorabanzeige will, entscheidet das als Inhaber.
- **D-03:** „Warum?“ und „Ausgeblendet: N“ gelten für gespeicherte Filter; die einfache Listensuche mit Statusschalter hat nur zwei sichtbare Bedingungen und bekam keinen Erklärdialog.
- **P07:** kein FTS5-Index – nach der Regel der Karte belegt (3.33.21 100,8 ms → 3.34.0 66,6 ms Median).
- **B4:** zusätzlich der Rückweg (Markdown mit Bildern wird wieder Seite mit Seitenbildern), weil die Abnahme „Markdown-Rundlauf erhält Bilder“ sonst nicht erfüllbar war.
- **N08, W07, W08:** Linux- bzw. Windows-Sichtprüfung steht aus (◇/offen); auf dem Mac sind N08 mit erzwungenem Linux-Weg und W05 belegt, W07/W08 nicht nachstellbar.
- **Pakete 5 und 6:** gemeinsam als 3.35.0 in einem eingefrorenen Volllauf geliefert, weil Paket 5 klein war (zwei Dialogergänzungen) und beide gleichzeitig fertig vorlagen; jedes behielt Pflichtsuite und Gegenprobe. Die geplante 3.36.0 entfällt (technische Lieferentscheidung, kein Inhaberentscheid).
- **Bundle:** `codesign --verify` scheitert direkt im OneDrive-Ordner am Dateianbieter; geprüft im Bauordner und auf einer Rückkopie, Inhalt gleich.
- **Nachweise 3.33.13–3.33.16:** waren nie eingecheckt und fielen planmäßig aus der Aufbewahrung; ihre Werte stehen nur im QA-Bericht.

**Befunde des Sprints** (Analyse A15–A23): Lieferabsatz nach Werkzeuglauf, fehlender Menüweg zur vollständigen Eingabemaske, „Als erledigt markieren“ in Übersichten, zwei zeitabhängige Prüfwerkzeuge, Alt+→ bei losen Listen, Suchengpass, Bilder in Seiten – alle behoben und in der jeweiligen Version geprüft. Beim Prüfen von 3.35.0 kam ein Dreifachklick auf der Farbleiste hinzu (öffnete den Dialog erneut), behoben.

**Abschlussstand des letzten Sprints, 09.10.2026:** W02 und alle Lieferungen ab 3.33.19 auf Windows nachprüfen; W07/W08 (Windows-Sichtprüfung B1a); N08 unter Linux ansehen; menschliche Abnahme I6; Inhaberentscheidungen E-S1–E-S8 und I1–I11 (§11). Eingecheckt am 09.10.2026. Die inzwischen entschiedenen Auswahlen und der neue Prüfrahmen stehen in §11/§15; dieser Absatz beschreibt den damaligen Abschlussstand.

## 15. Neuer Feature-Sprint ab 09.10.2026: gemeinsame Planung

**Status: Phase 1, Auswahlrunden 1 bis 6 am 10.10.2026 festgelegt (D18–D43), Gesamtplan am 10.10.2026 mit „ja“ bestätigt (D44), Phase 2 begonnen.** Alle angebotenen Funktionskandidaten sind entschieden. §15.7 legt acht bestätigte Produktionsversionen mit Reihenfolge und Prüfungen fest; §15.8 benennt die verbleibenden Abnahmetore. D44 beschreibt den gewählten Umfang; D50 und der Abschlussauftrag 15.10. ändern die Folge. Der aktuelle Auftrag erlaubt Analyse und Planung, keine Produktion. Keine Auswahl aus Empfehlungen oder Schweigen ableiten.

Grundlagen vollständig gelesen: `CLAUDE.md` → `01_Repository/Glide/AGENTS.md` → Übergabe → Arbeitsrichtung; danach §11, §4.3, §5–§7, §14.2 sowie Analyse und Markt/Vorbilder; ergänzend Produktgrenzen und Dokumentenpflege. Ausgangspunkt: 3.35.0, Format 23, sauberes `main` mit PR #16 (`b5f5c22`). Arbeitszweig: `claude/glide-sprint-2026-10-09`. Q1–Q5, D01–D17 und die bewussten Ausschlüsse werden nicht neu zur Wahl gestellt. E-S8 wird in ICS-Belegzeiten und Oberflächenbewegung getrennt; bei E-S2 sind Referenzweg und vier Funktionsumfänge eigene Antworten.

### 15.1 Ausgewählte Aufgaben

Die Karten tragen den vom Inhaber gewählten Umfang. Nur N12 und P05 sind erste Stufe; alle anderen Funktionskandidaten vollständig im jeweils angebotenen Rahmen. Die Antworten stehen mit Datum und Wortlaut als D18–D43 in der Arbeitsrichtung. Aufwand S bis 1, M 2–4, L mehr als 4 Arbeitstage als Größenordnung einschließlich gezielter Prüfung, keine Terminzusage. Gemeinsame Lieferprüfung zusätzlich je Produktionspaket (§15.3).

| ID / Herkunft | Ausgangslage → Ziel / Nutzen | Gewählter Umfang | Abhängigkeiten | Akzeptanzkriterien | Prüfung | Status |
|---|---|---|---|---|---|---|
| S26-01 / OB02, E-S2 | Heute ohne ausgeprägte Hierarchie → nächste Aufgabe, Zeit und Fortschritt schnell erfassen | vollständig nach D22: Heute-Kopf und vier Textstufen in Heute, Listen, Seiten und Inspektor; M–L | Bild 1 (D21); N05 für Inspektor | jede Angabe einmal, feste Kanten; 860 × 700 und große Schrift; alle gewählten Ansichten erfasst | echte Bedienwege, Geometrie, Kontrast, Vorher/Nachher; Gegenprobe gegen Vorversion | ✅ 3.38.0 geliefert; Mac/Linux/Windows automatisch grün, Tempo D46/D48 erfüllt; Menschen-/DPI-Abnahme getrennt offen |
| S26-02 / OB03, E-S2 | nur Einplanen bedarfsabhängig → weitere Zeilenaktionen erreichbar und ruhig | vollständig nach D23: Einplanen, Fälligkeit und „…“ bei Hover/Auswahl in Liste, Tabelle, Heute und Demnächst; M–L | Bild 1; S26-13 gemeinsam ausgewählt | Tastatur, Kontextmenü und Palette gleichwertig; keine Fokusverluste; alle vier Ansichten | Hover/Auswahl/Fokus, Aktion über stabile ID, Flächenmessung; Gegenprobe gegen Vorversion | ✅ 3.38.0 geliefert; Mac/Linux/Windows automatisch grün, Tempo D46/D48 erfüllt; Menschen-/DPI-Abnahme getrennt offen |
| S26-03 / N05, E-S2 | Maske und Detailbereich doppelt → eine verlässliche Bearbeitungsfläche | vollständig nach D24: gemeinsamer Inspektor in Liste, Tabelle, Heute, Demnächst, Pinnwand und Dokumentverweisen; bei schmalem Fenster in Inhaltsfläche; L | Bild 1; Grundlage für KO04 | alle bisherigen Felder und Einstiege erhalten; ein primärer Editor; Undo, Abbruch, Auswahl und Schreibschutz konsistent | Feld-/Einstiegsmatrix aller Kontexte, Fokus, Neustart, große Schrift; Gegenprobe gegen Vorversion | ✅ 3.38.0 geliefert; Mac/Linux/Windows automatisch grün, Tempo D46/D48 erfüllt; Menschen-/DPI-Abnahme getrennt offen |
| S26-04 / KO04, E-S2 | häufige Felder erfordern Umweg → direkt am Objekt bearbeiten | vollständig nach D25: Bearbeitungstag, Fälligkeit, Wichtigkeit und Labels im Inspektor und an sichtbaren Aufgabenfeldern in Liste, Tabelle, Heute, Demnächst, Pinnwand und Dokumentverweisen; L | S26-03 (D24) | identische Fachlogik; D01/D02; je Änderung ein Undo; Positionierung, Fokus und Abbruch konsistent | Maus/Tastatur, alle Kontexte und Felder, Abbruch, Neustart; Gegenprobe gegen Vorversion | ✅ 3.38.0 geliefert; Mac/Linux/Windows automatisch grün, Tempo D46/D48 erfüllt; Menschen-/DPI-Abnahme getrennt offen |
| S26-05 / AU03, E-S3 | Tagesbeginn/-abschluss nur manuell → optional rechtzeitig erinnern | A/V nach D20: Vorgabe aus, 08:30/17:30; Uhrzeiten/Wochentage, später erinnern, heute überspringen, gesammelte verpasste Hinweise; M | D20 entschieden; Gesamtplan D44 bestätigt | nur bei laufender App; kein Zwangswechsel, keine Mehrfachzustellung je Termin; Einstellungen und Zustellzustand bleiben über Neustart erhalten | Tk-freie Zeit-/Zustelltests mit künstlicher Uhr; Tageswechsel, Neustart, modaler Zustand; echte Bindungen; Gegenprobe gegen Vorversion | ✅ 3.39.0 geliefert; Mac/Linux/Windows automatisch grün, Menschen-/DPI-Abnahme getrennt offen |
| S26-06 / AU07, E-S8a | freie Fenster berücksichtigen nur Glide → lokale Termine als Belegzeiten berücksichtigen | A/V nach D30: gewählte ICS-Datei lesend; Einzel-/ganztägige Termine, übliche tägliche/wöchentliche/monatliche/jährliche Serien und Ausnahmen, Zeitzonen/Sommerzeit, transparent/storniert; L | begrenzte ICS-Erweiterung durch D30; planning_summary | Überlappungen nicht doppelt zählen; keine Aufgaben/Synchronisation; nicht unterstützte Regeln sichtbar melden; alle Planungswege verwenden gleiche Bilanz | Tk-freie ICS-/Serien-/Zeitzonentests; Fixtures, Randtage, Sommerzeit, Überlappung, Ausnahmen; echte Planungswege; Gegenprobe gegen Vorversion | ✅ 3.39.0 geliefert; Mac/Linux/Windows automatisch grün, Menschen-/DPI-Abnahme getrennt offen |
| S26-07 / OB04, E-S8b | Zustandswechsel abrupt → dezente optionale Rückmeldung | A/V nach D31: Abhaken, Klappen, Bereichswechsel bis 150 ms, unterbrechbar; M–L | D31; Tempoziel vor/nach | Animationsoption beachten; keine zurückbleibenden after-Aufträge; schnelle Folgen sauber abbrechen; keine Zielverschlechterung | Zeit-/Abbruchlogik Tk-frei; echte schnelle Folgeaktionen, Fokus, Messen, Animationen aus; Gegenprobe gegen Vorversion | ✅ 3.38.0 geliefert; Mac/Linux/Windows automatisch grün, Tempo D46/D48 erfüllt; Menschen-/DPI-Abnahme getrennt offen |
| S26-08 / G17, E-S1/D07 | statische Zeichnungen → begrenzte Pixelanimation | A/V nach D18: Frames anlegen/duplizieren/löschen/umordnen, gemeinsame und einzelne Dauer, Vorschau, PNG-Spritesheet und Einzelbildfolge; kein GIF; L | D18 entschieden; nächstes Datenformat-Tor; Gesamtplan D44 bestätigt | Altzeichnungen erhalten; Vorsicherung/Migration/Altleser; Vorschau und Exporte entsprechen den Frames; jede Bearbeitung rücknehmbar; Reihenfolge und Dauer über Neustart erhalten | Tk-freie Frame-/Exporttests; echte Werkzeuge, Exportdateien, Undo, Altleser; Gegenprobe gegen Vorversion | ✅ 3.40.0 geliefert |
| S26-09 / G21, E-S4 | generischer Dateiimport → erste Fremdquelle kontrolliert übernehmen | Notion A/V nach D26: ZIP, Text/Überschriften/Listen, lokale Bilder/Anhänge, Aufgaben-Kästchen und interne Seitenverweise; Vorschau und Verlustbericht; L | D26; vorhandener Markdown-Import und lokale Verweise | nichts still verlieren oder überschreiben; keine Notion-Datenbank; Unterseiten in bestehende Ordner/Seiten; sichere Größen-/Pfadgrenzen; ein Undo und Vorsicherung | Tk-freie Parser-/Archivtests; künstliche Exportpakete, fehlerhafte Archive, Quellverluste, Abbruch, Undo, Neustart; Gegenprobe gegen Vorversion | ✅ 3.41.0 geliefert; Mac/Linux/Windows automatisch grün |
| S26-10 / G26, E-S5/D15 | installiertes Python nötig → eigenständig startende Pakete | A/V nach D27: PyInstaller 6.22.3 nur zum Bauen; Python 3.14/Tk 9; macOS arm64 und Windows x64, vollständige Ressourcen, Lizenzbelege und Bauanweisungen; L | native Mac-/Windows-Bau- und Prüfumgebung; I3 für öffentliche Signatur | Start ohne externes Python; Daten außerhalb Paket; Ressourcen/vendor vollständig; Version/Architektur nachvollziehbar; Signaturstatus ehrlich ausgewiesen | native isolierte Start-/Ressourcen-/Datenproben, Hash und Signatur; Gegenprobe: Vorversion benötigt externes Python | ✅ 3.42.0 geliefert; beide native Pakete/isolierte Starts und Vollprüfungen grün; Menschenabnahme getrennt |
| S26-11 / LG01–LG03, E-S6/I8 | Tk-8.6-Logo treppig und großes PNG → geglätteter Rückfall und richtige Symbolgrößen | A/V nach D28: Wege B+C+D+F; Glättung, App-Symbole 16/32/64/256, Tests und Dokumentation; M–L | D28; Master LG04 nach D41, Gestaltungsabnahme D45 erfüllt | Zwischentöne und korrekte Größen bei wechselndem DPI/Akzent; Tk 9 bleibt erhalten; kein großes PNG im Startweg | Tk-freie Raster-/PNGtests; Bildwerte, Tk 8.6/9, Startmessung, native Sichtprüfung; Gegenprobe gegen Vorversion | ✅ 3.37.0 geliefert; Mac/Linux/Windows automatisch grün; Menschen-/DPI-Sichtprüfung getrennt offen |
| S26-12 / A14, E-S7 | Ersatzschriften für einige Symbole → einheitliche und eindeutige Zeichen | A/V nach D29: gesamte ICONS-Tabelle mit Zeichen aus tatsächlich verwendeter UI-Schrift; Größe/Ausrichtung/Bedeutung; M | D29; native Plattformprüfung | nur ICONS; keine zusätzliche Symbolschrift; keine Mehrfachbedeutung; Beschriftung und Tastaturwege erhalten | Symbolprüfung je Plattform, Schrift-/DPI-Wechsel, Kontrast und Sichtabnahme; Gegenprobe für belegte Ersatzschriftfehler | ✅ 3.37.0 geliefert; Mac/Linux/Windows automatisch grün; Menschen-/DPI-Sichtprüfung getrennt offen |
| S26-13 / Bedienfläche ≤ 15 % | zuletzt ≈ 27 %, seit U09/OB05 ungemessen → Inhalt gewinnt Fläche | A/V nach D32: Liste, Heute, Tabelle, Demnächst, Seiten, Pinnwand messen und dauerhafte Bedienfläche über Inhalt reduzieren; M–L | OB02/OB03/N05; D32 | ≤ 15 % bei 1280 × 800 nach P4; 840 zusätzlich berichten; alle Wege erhalten; 860 × 700/große Schrift erreichbar und lesbar | nachvollziehbare Geometriemessung je Ansicht; große Schrift, Tastatur und Auffindbarkeit; Gegenprobe gegen Vorversion | ✅ 3.38.0 geliefert; Mac/Linux/Windows automatisch grün, Tempo D46/D48 erfüllt; Menschen-/DPI-Abnahme getrennt offen |
| S26-14 / P03-Rest | geänderte Karten teuer, Startseite 270–300 ms → weniger Aufbau | A/V nach D33: Teilaktualisierung geänderter Karten, viele Karten und Startseiten-Neuaufbau; L | gemessene Baseline; D33 | unveränderte Widgets erhalten; Auswahl/Fokus/Scrollen stabil; Startseite warm ≤ 150 ms; Kalt-Ausnahme D46 ≤ 300 ms direkt/≤ 500 ms Kindprozess, Messbeleg | warm/kalt, Median/p95, 1.000/10.000 Punkte, Widget-/Speicherentwicklung; Gegenprobe gegen Vorversion | ✅ 3.36.0 geliefert; D46/D47 eingehalten, Mac/Linux/Windows automatisch grün, Menschenabnahme getrennt |
| S26-14b / E01-Rest | Einstellungen ≈ 560 ms → schnellerer erster/wiederholter Zugang | A/V nach D34: sichtbare Bereiche zuerst, wiederverwendbare Bereiche erhalten; M–L | eigene Baseline; D34 | erste Anzeige ≤ 250 ms, erneut Median ≤ 150 ms/p95 ≤ 190 ms nach D48 (12.10.2026; ersetzt die bisherige p95-Grenze 170 ms aus D47); Werte aktuell; keine Rückrufe nach Schließen; Abweichungen ausdrücklich klären | getrennte Erst-/Folgeserien, Median/p95, Themen-/Schriftwechsel, Schließen/Öffnen, Fokus und Lebensdauer; Gegenprobe gegen Vorversion | ✅ 3.36.0 geliefert; D46/D47 eingehalten, Mac/Linux/Windows automatisch grün, Menschenabnahme getrennt |
| S26-15 / Linux-CI | nur Grundstufe verpflichtend → kalibrierte Integrationssuiten | A/V nach D35: gesamte sachlich ausführbare Linux-Matrix verpflichtend; L | Linux mit tkinter/Xvfb; native CI-Ausführung | echte Befunde nicht wegkalibrieren; Plattformfälle ausdrücklich benennen; neue Sprintwege eingeschlossen | native Linux-Läufe, absichtlich fehlerhafte Gegenfälle, CI-Nachweis und rote Vorversion für neue Pflichtsuiten | ✅ 3.36.0: gesamte ausführbare Matrix und sieben passende Defektgegenproben an `3f267a2` grün; neue Sprint-Suiten je Folgepaket ergänzen |
| S26-16 / N12 | Screenreader-Kernabläufe fehlen → Tk-9.1-Zugänglichkeit | A/1 nach D36: Aufgaben erfassen, suchen, Heute planen, Inspektor; L | S26-10; eigens geprüfte Tk-9.1-Laufzeit; native Screenreader | Rollen/Namen/Werte/Zustände; Auswahl/Fokus; kompletter gewählter Kernablauf tatsächlich bedienbar; übrige Arbeitsbereiche ausdrücklich außerhalb | Tk-9.1-Proben plus VoiceOver/NVDA/Linux-Screenreader-Abnahme; Tastatur/Undo/Neustart; Gegenprobe gegen Vorversion | ▶ erste Stufe ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-17 / N13 | Sicherungen nur insgesamt vergleichbar → einzelne Seite wiederherstellen | A/V nach D37: bestehender Sicherungsvergleich mit Vorschau; Text, Bilder/Anhänge, Aufgabenverweise, Live-Listen; L | Sicherungs-/Verweis-/Anhangsregeln; D37 | andere Seiten unverändert; IDs/Verweise konsistent; fehlende Ziele vorab; Vorsicherung und ein Undo; kein neues fortlaufendes Versionssystem | Tk-freie Wiederherstellungsplanung; Sicherungs-Fixtures mit Bildern/Live-Listen, fehlende Ziele, Neustart/Undo; Gegenprobe gegen Vorversion | ✅ 3.41.0 geliefert; Mac/Linux/Windows automatisch grün |
| S26-18 / V01, neuer Vorschlag | Überplanung nur angezeigt → ausgewählte Aufgaben direkt entlastend umplanen | A/V nach D38: Heute, Woche, Tagesvorschlag; Auswahl, anderer Tag/Vorrat, Vorher-/Nachher-Bilanz mit ICS-Belegzeiten; M–L | planning_summary; S26-06; D38 | Nutzer wählt Aufgaben und Ziel; keine automatische Verteilung; Fälligkeiten bleiben; ein Undo | Tk-freie Bilanz-/Umplanungsregeln; Kapazität, ungeschätzte Aufgaben, Mehrfachauswahl, alle drei Kontexte, D02; Gegenprobe gegen Vorversion | ✅ 3.39.0 geliefert; Mac/Linux/Windows automatisch grün, Menschen-/DPI-Abnahme getrennt offen |
| S26-19 / V02, neuer Vorschlag | erneuter Fremdimport kann Dubletten schaffen → Quellen wiedererkennen | A/V nach D39: unverändert/geändert/neu, eigene Änderungen als Konflikt, ausdrücklich gewählte Übernahme; L | S26-09; Datenformat-Tor für Quellenmetadaten; D39 | keine stillen Dubletten oder Überschreibungen; Verlustbericht; keine Live-Synchronisation; Zustände über Neustart erhalten | Tk-freie Zuordnungs-/Konflikttests; gleiche/geänderte Exporte, umbenannte Quellen, Konflikt/Abbruch/Undo, Migration/Altleser | ✅ 3.41.0 geliefert; Mac/Linux/Windows automatisch grün |
| S26-20 / I6, W01/W02/W06–W08/N08 | Windows seit 3.33.18, Linux-Sicht und Menschenabnahme offen → belegter Plattformstand | A/V nach D42: native Windows-Vollprüfung je Lieferung; vorhandene Windows-/Linux-Sichtfälle nachführen; L + getrennte Abnahme | native Windows-/Linux-Runner; GitHub Actions aktiviert; Inhaber für Menschenabnahme | Mac/Linux/Windows-Ergebnisse getrennt; kein automatischer Lauf ersetzt Menschenbedienung/DPI/Screenreader; keine unbelegten Plattformfreigaben | native Vollprüfungen je Lieferung, vorhandene manuelle Prüfliste; konkrete Lauf-/Artefaktverweise; echte Readerproben getrennt von Attributtests | ◐ Gelieferte Pakete bis 3.42.0 einschließlich 3.39.1 nativ Windows/Linux grün; weitere Lieferungen und Menschenabnahme bleiben Pflicht |
| S26-21 / P05 | gemeinsame Helfer nur teilweise → gezielte Vereinheitlichung | A/1 nach D40: nur nachweislich gleiche UI-Texte/Abläufe im angefassten Sprint-Code; S–M | kein Großumbau, D17; D40 | gleiche Bedeutung, keine stillen Aktions-/Begriffsänderungen; kein Gesamtabgleich | betroffene Aufrufer, Bindungen und bestehende Suites; Gegenprobe für jeweiliges Paketverhalten | ▶ erste Stufe ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-22 / LG04 | Knicke an Rundungsübergängen und enger Innenraum klein → sauberer Master | A/V nach D41: tangentiale Anschlüsse/Kurzsegment, zusätzliche Kleingrößenfassung 16/32; M–L | Vorher-/Nachher-Abnahme vor Übernahme; D28 unabhängig | Silhouette/Farbe erhalten; keine stille Masteränderung; Exporte nachvollziehbar | Vektor-/Rastervergleich, 16/32/54/512 px, Gestaltungsabnahme, App-Symbole/Lieferabgleich; Gegenprobe gegen Vorversion | ✅ 3.37.0 geliefert; Mac/Linux/Windows automatisch grün; Menschen-/DPI-Sichtprüfung getrennt offen |

Quellen: [Analyse](Glide_Analyse.md), §3–§7/§14.2 dieses Plans und [Markt/Vorbilder §8](Glide_Markt_und_Vorbilder.md#8-daten-offline-und-ki). V01/V02 sind eigene Ableitungen, keine behaupteten Herstellermerkmale. N13 stammt bereits aus §7. Jede Karte ist ausdrücklich ausgewählt; §15.7 ordnet alle 23 Aufgabenkennungen einer Lieferung oder einer durchgehenden Aufgabe zu.

### 15.2 Entscheidungsrunden und Gesprächsstand

- **Runde 1 entschieden am 10.10.2026:** E-S1 A/V (D18), E-S2 B/V (D19), E-S3 A/V (D20). Vollständiger Antwortwortlaut und verbindlicher Umfang in der Arbeitsrichtung. Drei Referenztafeln für alle vier Bereiche sind vorgelegt; Bild 1 und OB02/OB03/N05/KO04 anschließend durch D21–D25 gewählt.
- **Runde 2 entschieden am 10.10.2026:** Bild 1 (D21); OB02, OB03, N05 und KO04 jeweils B – vollständig (D22–D25). Antworten im Wortlaut in der Arbeitsrichtung, Umfang in den Aufgabenkarten und §15.4.

- **Runde 3 entschieden am 10.10.2026:** E-S4 Notion A/V (D26), E-S5 PyInstaller 6.22.3 für Mac/Windows A/V (D27), E-S6 Logo B+C+D+F A/V (D28), E-S7 Systemzeichen/gesamte ICONS-Tabelle A/V (D29).

- **Runde 4 entschieden am 10.10.2026:** ICS-Belegzeiten (D30), Bewegung (D31), Bedienfläche (D32), P03 (D33), E01 (D34) und Linux-Matrix (D35), jeweils A/V.

- **Runde 5 entschieden am 10.10.2026:** N12 A/1 (D36), N13 A/V (D37), V01 A/V (D38), V02 A/V (D39), P05 A/1 (D40), LG04 A/V (D41).

- **Runde 6 entschieden am 10.10.2026:** Windows je Lieferung A/V (D42); Veröffentlichungstore I1–I5/I9–I11 ausdrücklich gesondert offen halten (D43). Damit alle Funktionskandidaten entschieden; Gesamtplan als D44 bestätigt; Logoentwürfe als D45 freigegeben.

### 15.3 Verbindlicher Lieferrahmen nach Bestätigung

Je Paket eine Produktionsversion nach Übergabe §5: isolierte Baseline → Umsetzung mit Tk-freier Fachlogik/Unit-Tests (D17) und echten Bedienwegen → Pflichtsuite mit roter Gegenprobe gegen die Vorversion → CHANGELOG → Versionswechsel → 07-README → Nachweisrahmen/Standprüfung → eingefrorene Kopie außerhalb OneDrive → Vollprüfung → Abgleich 07 und Showcase in der Kopie → 07/05 zurück → Bundle und Signatur im Bauordner sowie auf Rückkopie → Nachweise/QA/Plan/Funktionen/Übergabe → CI-Grundstufe → sofortiger Commit. Neue 07-Hauptdatei beim Vormerken ausführbar setzen. Erster Versionswechsel: Nachweisverweise 3.33.17 auf Commit `6098877` festsetzen.

Commits mit `Claude <noreply@anthropic.com>` auf dem genannten `claude/`-Zweig; PR nur als Merge-Commit. Stash, `codex/`-Zweig und Windows-Worktrees unangetastet lassen. Keine UI-Prüfungen parallel zu Vollprüfungen oder Messungen; keine Konsolenumleitung nach OneDrive. Neue Produktfragen vorlegen und unabhängig weiterarbeiten; Umfang nicht still reduzieren. Externe Prüfungen und benötigte Inhaberhandlungen vor Bestätigung als konkrete Tore vereinbaren. Zum Abschluss Plan ↔ Code ↔ Prüfergebnisse mit allen Abweichungen abgleichen.

### 15.4 Referenzentwürfe und zweite Auswahlrunde (10.10.2026)

Bild 1 und die vollständigen angebotenen Umfänge OB02/OB03/N05/KO04 wurden als D21–D25 gewählt und in3.38.0 geliefert. Referenztafeln und Herkunft bleiben im Grafik-Master; die ursprünglichen Wahlalternativen stehen in Git. Sie werden nicht erneut als offene Auswahl geführt.

### 15.5 Dritte Auswahlrunde und Quellenbindung (10.10.2026)

D26/D27 begrenzen Notion-Import und Bauwerkzeug, D28/D29 Logo/Symbole, D30/D31 ICS/Bewegung, D32–D35 Fläche/Tempo/Prüfmatrix. Die vollständig gewählten Umfänge stehen in der Arbeitsrichtung und §15.1; Lieferstände in §15.7. Keine offene Produktentscheidung aus dieser Runde.

### 15.6 Fünfte Auswahlrunde (10.10.2026)

N12 A/1, N13 A/V, V01 A/V, V02 A/V, P05 A/1 und LG04 A/V sind D36–D41; Windows je Lieferung und gesonderte Veröffentlichungstore D42/D43. D44 bestätigte den damaligen Gesamtplan, D45 den Logoentwurf. Nicht erneut entscheiden; offene Abnahmen bleiben eigene Tore.

### 15.7 Bestätigter Gesamtplan: acht Produktionsversionen

**Historischer Umfang nach D44 vom 10.10.2026.** Die folgende Tabelle bewahrt die bestätigten Aufgaben und ihre Reihenfolge. Der aktuelle Fortgang steht in §18–§20.

| Folge / Version | Inhalt und Aufgaben | Warum in dieser Reihenfolge | Status |
|---|---|---|---|
| 1 / **3.36.0** | Fundament und Tempo: P03-Rest S26-14, E01-Rest S26-14b, gesamte ausführbare Linux-Matrix S26-15; native Windows-Vollprüfung S26-20 ab dieser Lieferung | belastbare Prüfstände und Tempo vor dem breiten Oberflächenumbau | ✅ 10.10.2026 geliefert; Mac/Linux/Windows automatisch grün |
| 2 / **3.37.0** | Logo und Symbole: Tk-8.6-Rückfall/App-Symbole S26-11, gesamte ICONS-Tabelle S26-12, Logo-Master und Kleingrößen S26-22 | Grafikgrundlagen vor neuen Oberflächenaufnahmen; Gestaltungsabnahme vor Masterübernahme | ✅ geliefert 11.10.2026: Mac/Linux/Windows automatisch grün, 07/05/Bundle bytegleich, Signaturen grün; Menschenabnahme getrennt |
| 3 / **3.38.0** | Aufgabenoberfläche nach Bild 1: OB02 S26-01, OB03 S26-02, gemeinsamer Inspektor S26-03, direkte Felder S26-04, Bewegung S26-07, Bedienfläche S26-13 | einheitliche Bearbeitungsfläche als Grundlage für folgende Planungs- und Zugänglichkeitswege | ✅ 12.10.2026 geliefert; Hash bcdbc4da, Mac/Linux/Windows-Vollprüfung und 18 Defektgegenproben grün; Tempo D46/D48 erfüllt, Lieferdateien/Signaturen erneut geprüft; Menschen-/DPI-Abnahme getrennt offen |
| 4 / **3.39.0** | Tagesplanung: Tageshinweise S26-05, ICS-Belegzeiten S26-06, Tag entlasten S26-18 | alle Kapazitätswege teilen dieselbe Bilanz; Entlasten berücksichtigt die neuen Belegzeiten | ✅ 3.39.0 geliefert; Mac/Linux/Windows automatisch grün, Menschen-/DPI-Abnahme getrennt offen |
| 5 / **3.40.0** | Pixelanimation S26-08 vollständig mit PNG-Spritesheet/Einzelbildfolge | eigenes Datenformat- und Exportpaket, getrennt vom folgenden Import | ✅ 3.40.0 geliefert |
| 6 / **3.41.0** | Notion-Import S26-09, Wiedererkennung/Konfliktvergleich S26-19, einzelne Seite aus Sicherung S26-17 | Quellenzuordnung und Wiederherstellung gemeinsam gegen Verweis-/Anhangsregeln prüfen | ✅ 3.41.0 geliefert; Mac/Linux/Windows automatisch grün |
| 7 / **3.42.0** | Eigenständige Pakete S26-10: PyInstaller 6.22.3, macOS arm64 und Windows x64, Python 3.14/Tk 9 | vollständigen Funktionsstand samt Ressourcen bündeln; Bauweg vor Tk-9.1-Wechsel festigen | ✅ 3.42.0 geliefert; Mac/Linux/Windows automatisch grün, Menschen-/Releaseabnahme getrennt |
| 8 / **4.0.0** | Zugänglicher Aufgaben-Kernablauf S26-16 A/1 mit eigener geprüfter Tk-9.1-Laufzeit und tatsächlichen Readerproben | baut auf gemeinsamem Inspektor und eigenständigen Paketen auf; nach D50 auf aktuellen UI-Stand abgleichen | ◐ separate Vorbereitung, keine Lieferung: gezielte automatische Verträge vorhanden; vollständige native Readerabläufe, eingefrorene Endmatrix und Pakete offen (§18/§19) |

Pakete 1–7 wurden als 3.36.0–3.42.0 geliefert; FP-00 lag als 3.39.1 vor Paket 5. Das nach D50 vorgezogene UI-/UX-Paket folgte als Python-Lieferung 3.43.0/3.43.1. Paket 8 ist weiterhin nicht geliefert. Seine Vorbereitung einschließlich GUI10 und SIG11 bleibt im [historischen Nachweis](../01_Repository/Glide/tests/qa-3.42.0/zugang400_vorbereitung_2026-10-14/README.md) nachvollziehbar.

Die wiederholten Liefergeschichten sind hier zusammengeführt; Einzelwerte und damalige Grenzen bleiben in den QA-Nachweisen und der Git-Historie erhalten. FP-01 und WA-27–WA-30 sind inzwischen im lokalen Prüfkandidaten integriert (§18.3). Das ist keine neue Lieferung nach 07 und kein Abschluss der offenen Phasenentscheidungen.

### 15.8 Gemeinsame Prüfungen, Abnahmetore und Abschluss

D44, D50 und D51 bestimmen den Fortgang: gezielte Prüfungen während einer Phase, eingefrorene Vollprüfung und Lieferung am bestätigten Phasenende. Die vorgeschlagenen Gesamtphasen bleiben entscheidungspflichtig. D17/P05, D35/D42 und die Datenformat-Tore gelten weiter; Format 24/25 erfordern Altleser- und Sicherungsprüfungen. D45 ist erfüllt.

I6 und N12 bleiben menschliche Abnahmen. D43 sowie I1–I5/I9–I11 werden mit ihren eigenen Nachweisen geprüft. Automatisierte Prüfungen ersetzen weder native Sicht-/Screenreaderabnahme noch Freigabe einer neuen Lieferung.

Vor jedem Commit läuft die CI-Grundstufe. Der Auftrag vom 18.10. umfasst Bestandsprüfung, Zusammenführung, Bereinigung, Validierung sowie Commit und Pull Request; der Pull Request wird nicht automatisch zusammengeführt. Temporäre Arbeitskopien dürfen nach Sicherung und Abgleich entfallen, ihre Branches und Sicherungen bleiben erhalten.

## 16. Vorschläge aus Wettbewerbs- und Open-Source-Analyse (13.10.2026)

**A-Verbindlichkeit seit D49:** Auslegung der Fortsetzungsantwort vom 13.10.2026, **keine einzeln bestätigte Auswahl** E-W1–E-W7; jederzeit durch den Inhaber korrigierbar. D50 gab dem UI-/UX-Paket Vorrang, der Abschlussauftrag 15.10. verlangt danach eine Neuordnung. Diese ersetzt die früher hier als automatisch auszuführend formulierte Folge. Der Auftrag vom 18.10. umfasst nur Analyse/Planung. **FP-00 ist geliefert; FP-01 ist inzwischen upstream als Kandidat implementiert und gezielt geprüft, lokal/07 nicht übernommen oder geliefert; FP-02–FP-07 sind vorbereitet.** P3-Einträge mit Auslöser bleiben zurückgestellt. Grundlagen: [Analyse](Glide_Analyse.md), [Markt und Vorbilder](Glide_Markt_und_Vorbilder.md); aktuelle Statusachsen §18, Auswahlstand §20.

### 16.1 Priorisierung

- **P0 – Kritisch:** Fehler, Datenintegrität, Stabilität, bestehende Kernfunktionen. Die erste Durchsicht fand keinen P0-Fehler; die Vorprüfung für FP-02 (§16.10) belegte **zwei reproduzierbare Fehler** im Lieferstand: Teilerkennung von Wiederholungsangaben in der Schnelleingabe (A29, WA-18) und abweichende Monats-/Jahresserien im ICS-Austausch (A28, WA-17), gebündelt als FP-00 und mit A30 (Zeitzonen im Aufgabenimport) als 3.39.1 geliefert. W01/W06–W09 sind unterschiedlich gesicherte Sicht-/Beobachtungsfälle (§4.2), keine pauschal bestätigten kritischen Fehler; ihre Priorität folgt einer Reproduktion. 3.39.0 ist seit 13.10.2026 geliefert, der Dokumentabgleich WA-13 erledigt.
- **P1 – Hoch:** deutlich spürbar im Alltag bei beherrschbarem Risiko.
- **P2 – Mittel:** wertvolle Erweiterung oder Optimierung.
- **P3 – Optional:** experimentell, größere Architektur, langfristig.

Bewertung je Eintrag: Nutzen, Aufwand (S bis 1, M 2–4, L mehr als 4 Arbeitstage, wie §4.3), technisches Risiko, Wartbarkeit. Geringer Aufwand mit hohem Nutzen geht vor; Prestige-Funktionen ohne belegten Alltagsnutzen sind ausgeschlossen. Der Umfang einer Lieferung folgt dem zusammenhängenden Nutzen und den Abnahmetoren; nicht jeder Backlogeintrag braucht eine eigene Version.

### 16.2 Feature-Backlog

| ID | Titel | Problem (Fakt, Beleg) | Herkunft | Nutzen | Aufwand | Risiko | Wartbarkeit | Prio | Marke | Paket |
|---|---|---|---|---|---|---|---|---|---|---|
| WA-01 | Wiederholen nach Rückgängig | lokal kein Redo in `ListApp`; upstream Stufe 1+2 als Kandidat, noch nicht geliefert (PR #36) | Systemkonvention (P1); alle Vergleichsprodukte | hoch | M | mittel | gut | P1 | ▶ D49 | FP-01 |
| WA-02 | Erweiterte Wiederholungsregeln | sechs Arten ohne Intervall für Woche/Monat/Jahr, ohne n-ten Wochentag, nicht ab Erledigung [Code `repeat_rules.py`]; zweiter Rechner `ics_recurrence.py` kann mehr (A26) | Super Productivity, Todoist, RFC 5545 | hoch | M–L | mittel (Formattor) | besser als heute (ein Rechner) | P1 | ▶ D49 | FP-02 |
| WA-03 | Gespeicherte Ansichten | Filter ohne Bearbeitungstag, Aufwand, „wartet auf“, Ausschluss; Darstellung nicht gespeichert [Code `SavedFilters`] | AFFiNE, Vikunja, Obsidian Bases | mittel–hoch | M–L | mittel | gut (eine Auswertung) | P2 | ▶ D49 | FP-03 |
| WA-04 | Seiten und Notizen als Pinnwandkarten | nur Zeichnungen als Seitenkarte [Code `valid_pages`] | AFFiNE, Milanote, FigJam | mittel–hoch | M | gering–mittel | gut | P2 | ▶ D49 | FP-04 |
| WA-05 | Unverknüpfte Erwähnungen | Rückverweise nur für echte Verweise [Code] | Obsidian; Buildin (Dritte) | mittel | S–M | gering | gut | P2 | ▶ D49 | FP-05 |
| WA-06 | Wiederverwendbare KI-Aufträge | Kontextpaket ohne mitgelieferte Anweisungen [Code `exchange_patch.py`] | Notion, AFFiNE, Buildin (Bedienidee); Q3 | mittel–hoch | S–M | gering | gut | P2 | ▶ D49 | FP-06 |
| WA-07 | Offene Ausgabeformate | Ausgabe nur je Liste/Ordner; Pinnwand nur als PDF [Code] | Obsidian, JSON Canvas | mittel | M | gering | gut | P2/P3 | ▶ D49 | FP-07 |
| WA-08 | Zeitauswertung je Tag, Liste, Label | Zeit nur als Summe je Aufgabe; Wochenrückblick summiert erledigte Aufgaben [Code `week_review_data`] | Super Productivity (Arbeitsprotokoll) | mittel | M–L | mittel (Formattor) | mittel | P3 | ◇ Auslöser: Bedarf an Zeitnachweis | – |
| WA-09 | Vorwärtsverträgliche Einstellungen | innerhalb bekannter Strukturen verwerfen Normalisierer Unbekanntes, `prune` entfernt unbekannte Seitenkarten; oberste Ebene bleibt erhalten (A27) [Code] | Lehre 3.29/3.30 (Übergabe §4) | Schutz, keine sichtbare Funktion | S–M | gering | besser | P1 als Vorarbeit | ▶ D49 | vor FP-04 |
| WA-10 | Optionaler lokaler KI-Endpunkt | Q3 erlaubt nur Dokumente | AppFlowy (Ollama), AFFiNE (BYOK) | unbelegt | M | mittel | mittel | P3 | ✕ E-W3 A (D49) | – |
| WA-11 | Seitenvorschau für Verweise | Verweis navigiert, Kontext geht verloren [Code] | AFFiNE „Peek“ | mittel | M | gering | gut | P3 | ◇ | – |
| WA-12 | Tagesvorschlag: Grund „gibt andere frei“ | Vorschlag kennt blockierte, nicht blockierende Aufgaben [Code `day_proposal.py`] | Taskwarrior (Gewicht 8) | gering–mittel | S | gering | gut | P3 | ○ | – |
| WA-13 | Dokumentabgleich A24/A25 | veraltete Plattform- und Statusangaben [Dok] | eigene Prüfung | Verlässlichkeit | S | – | – | P0 | ✅ 13.10.2026 | – |
| WA-14 | Wiederkehrende Vorlagen | Vorlagen nur von Hand [Code] | Notion-Wiederholvorlagen | mittel | M | mittel | mittel | P3 | ◇ nach FP-02 | – |
| WA-15 | Rangfolge der Inhaltstreffer | Titelrang, keine Relevanzformel [Code `content_search.py`] | AFFiNE BM25+ | gering | S | gering | gut | P3 | ◇ nur nach belegter schlechter Rangfolge | – |
| WA-16 | Wartbarkeitskennzahl je Lieferung | Größe von `ListApp` am lokalen c0252ba 46.929 Zeilen/1.634 Methoden; kein Verlauf dieser Kennzahl [Code] | eigene Analyse | indirekt | S | – | besser | P3 | ○ | – |
| WA-17 | ICS-Austausch von Monats- und Jahresserien am Monatsende | Ausgabe `FREQ=MONTHLY`/`FREQ=YEARLY` für Termine am 29.–31. bzw. 29.02. ergibt in Kalenderprogrammen andere Termine als in Glide; Import einer Monatsserie am 31. legt zusätzliche Termine auf Monatsenden (A28) [Code][Probe] | eigene Vorprüfung | Korrektheit des Austauschs | S | gering | gut | P0 (Fehler, Randfall) | ✅ 3.39.1 geliefert | FP-00 |
| WA-18 | Wiederholungsangaben in der Schnelleingabe vollständig oder gar nicht erkennen | „monatlich am 15.“, „wöchentlich montags“, „alle 2 Wochen montags“ u. a. ergeben Serien ab heute, der Rest bleibt Titeltext; „jeden zweiten Dienstag“ ergibt nur einen Bearbeitungstag (A29) [Code][Probe] | eigene Vorprüfung | Korrektheit einer Kernfunktion | S–M | gering | gut | P0 (Fehler) | ✅ 3.39.1 geliefert | FP-00 |

**Geprüft und nicht vorgeschlagen:** vollständiger Block-Editor (Neubau des Seitenmodells, L+, Nutzen gezielt erreichbar), Whiteboard-Engine mit Formen/Freihand (Tk-Leinwand ohne Glättung; Produktgrenze), Datenbank-Baukasten und freie Felder (N15–N20), neue Beziehungsarten wie bei Vikunja (`links`/`blocked_by`/Unterpunkte genügen), Synchronisation/CRDT (G23), eingebaute Cloud-KI und BYOK (Produktgrenze), semantische Suche (Nutzen unbelegt, native Abhängigkeit), Daueralarm wie TickTick (widerspricht ruhiger Tagesführung), bezahlte Veröffentlichung wie Buildin (kein Ziel), Toolkit-Wechsel (§16.6).

### 16.3 Feature-Pakete

**Prinzipien-Check in Kurzform** ([Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md#prinzipien-check-für-neue-funktionen)); vor Umsetzung je Paket ausführlich in Funktionen und Plan eintragen.

| Paket | Vorgeschichte (0) | Ort (2) | Doppelung, was entfällt (3) | Dauerfläche bei 1280 × 800 (4) | Rücknahme (8) | Daten (9) | Tempo (10) |
|---|---|---|---|---|---|---|---|
| FP-00 | Fehlerbehebung, keine Produktentscheidung | Schnelleingabe, ICS-Ausgabe/-Import | keine | 0 px; Chip nennt zusätzlich den Ankertag | ein Undo wie bisher | nein (nur bestehende Arten) | – |
| FP-01 | D49-Auslegung; upstream Kandidat | Bearbeiten-Menü, Palette, Kürzel, Rückgängig-Hinweis | keine; ergänzt Rückgängig | 0 px (Hinweis zeigt nur bei Bedarf „Wiederholen“) | ist selbst Rücknahme | nein | Speicher messen |
| FP-02 | Wiederholungen bestehen; Erweiterung D49-Auslegung | Inspektor, Schnelleingabe | zweiter Rechner entfällt intern (A26) | 0 px | ein Undo je Änderung | Formattor | Budget im Rechner |
| FP-03 | gespeicherte Filter bestehen; eigene Felder ✕ bleibt | Filterdialog, Kachel, Palette | Bedingungen in einem Modul | 0 px | ein Undo je Ziehen | Einstellungen additiv, eigener Schlüssel auf oberster Ebene | ≤ 100 ms bei 10.000 |
| FP-04 | Zeichnungskarten bestehen (ZF-100); freie Zettel ✕ bleibt | Pinnwand, Seitenleisten-Kontextmenü | keine neue Art | 0 px | Flächenstapel | Einstellungen additiv (WA-09) | Auszug je Aufbau gecacht |
| FP-05 | D49-Auslegung | Rückverweisbereich der Seite, eingeklappt | keine | 0 px (eingeklappt) | ein Undo | nein | nur beim Aufklappen |
| FP-06 | Q3 entschieden; bleibt gewahrt | Dialog „Für KI bereitstellen …“ | keine | 0 px | Import mit bestehendem Undo | nein | – |
| FP-07 | Ausgabe je Liste/Ordner besteht | Datei › Ausgabe | keine; ergänzt Einzel-Ausgaben | 0 px | schreibt nur außerhalb des Datenordners | nein | Fortschritt bei großen Beständen |

#### FP-00 Wiederholungen richtig erfassen und austauschen (WA-17, WA-18)

| Bestandteil | Beschreibung |
|---|---|
| Paket-ID | FP-00 |
| Titel | Fehlerbehebung: Wiederholungsangaben in der Schnelleingabe und Monatsende-Serien im ICS-Austausch |
| Zielsetzung | Eine erkannte Wiederholung entspricht dem Eingegebenen oder wird gar nicht gedeutet; exportierte Serien zeigen in Kalenderprogrammen dieselben Termine wie in Glide. |
| Ausgangssituation | [Code][Probe `probe_wiederholung.py`] A29: `capture_parser._wiederholung` erkennt Intervall bzw. „monatlich/wöchentlich“, aber nicht den folgenden Ankertag oder die Wochentage; die Serie beginnt heute, der Rest bleibt Titeltext. Ordinale wie „jeden zweiten Dienstag“ ergeben nur einen Bearbeitungstag. A28: `ics_repeat_rule` gibt „monatlich“/„jährlich“ als `FREQ=MONTHLY`/`FREQ=YEARLY` aus; `ics_repeat_from_rule` bildet `FREQ=MONTHLY` unabhängig vom Starttag auf „monatlich“ ab. |
| Geplante Funktionen | (1) Ankertag und Wochentage im bestehenden Datenformat übernehmen: „monatlich am 15.“/„jeden Monat am Ersten“ → `monatlich` mit Start am nächsten 15./1.; „wöchentlich montags“ → `woechentlich` ab nächstem Montag; „alle 2 Wochen montags“/„… am Montag“ → `tage` 14 ab nächstem Montag; „jeden zweiten Dienstag“ → `tage` 14 ab nächstem Dienstag. (2) Was das heutige Format nicht abbilden kann („alle 2 Wochen montags und donnerstags“, „jeden ersten Montag im Monat“, „jeden dritten Freitag“), bleibt vollständig Titeltext mit einem Hinweischip „Wiederholung nicht erkannt“ statt Teilerkennung. (3) Der Wiederholungschip nennt den Ankertag. (4) ICS-Ausgabe für Starttage 29–31 mit `BYMONTHDAY=…;BYSETPOS=-1`, jährlich am 29.02. mit `BYMONTH=2;BYMONTHDAY=28,29;BYSETPOS=-1`; ICS-Import erkennt genau diese Formen als „monatlich“/„jährlich“ und verwirft `FREQ=MONTHLY` mit Starttag 29–31 bzw. `FREQ=YEARLY` am 29.02. sichtbar, statt die Folge still zu ändern. |
| Nutzermehrwert | Keine unbemerkt falschen Fälligkeiten bei Routinen; Kalenderausgabe vertrauenswürdig. |
| Betroffene Komponenten | `capture_parser.py` (Tk-frei), Chiptexte der Schnelleingabe, `ListApp.ics_repeat_rule`, `ics_repeat_from_rule` und ihr Aufrufer im ICS-Import (Starttag). |
| Technische Umsetzung | Erkennung als Muster über die vorhandenen Wort- und Datumsfunktionen; Teilerkennung verhindern, indem eine Wiederholungsangabe mit nicht abbildbarem Rest als Ganzes verworfen wird. RRULE-Ausgabe und -Rückweg als reine Funktionen in einem Tk-freien Modul (D17), geprüft gegen `ics_recurrence.dates`. |
| Abhängigkeiten | keine; unabhängig von FP-02, das später die nicht abbildbaren Formen ergänzt. |
| Kompatibilität | kein Formatwechsel: nur bestehende Arten und Startdaten. Bereits gespeicherte Serien bleiben unverändert; nur neue Eingaben und neue Ausgaben ändern sich. Re-Import früherer Glide-ICS-Dateien bleibt möglich. |
| Risiken | Mehrdeutigkeit der Sprache („jeden 2. Dienstag“ als zweiter Dienstag im Monat oder alle zwei Wochen) – Vorschlag: Ordinal ohne „im Monat“ gilt als „jede zweite Woche“, mit „im Monat“ erst in FP-02; geänderte Erwartungen bestehender Unit-Tests der Schnelleingabe; Kalenderprogramme mit unvollständiger BYSETPOS-Unterstützung (manuelle Probe). |
| Aufwand | S–M |
| Priorität | P0 (Fehlerbehebung nach Auftragsdefinition; Häufigkeit gering bis mittel) |
| Akzeptanzkriterien | (1) Jede Eingabe aus `probe_wiederholung.py` ergibt entweder die gemeinte Serie oder keine Wiederholung mit vollständigem Titeltext; keine Teilerkennung. (2) Chip nennt Art und Ankertag. (3) Für alle Starttage 1–31 und den 29.02. stimmt die Folge aus der ausgegebenen RRULE (gerechnet mit `ics_recurrence`) über 24 Termine mit `repeat_rules.next_date` überein. (4) Rundlauf Ausgabe → Import ergibt dieselbe Glide-Regel. (5) Importierte `FREQ=MONTHLY` am 31. wird sichtbar abgewiesen. |
| Tests | Unit-Tests für Parser-Muster (positiv und Teilerkennungsfallen) und RRULE-Abbildung über alle Starttage; Gegenprobe: dieselben Fälle gegen 3.39.0 rot; Regression bestehende Schnelleingabe-, ICS- und Wiederholungssuiten (`test_features320`, `test_features321`, `test_komfort33320`). |
| Dokumentation | Funktionen §3 (Erfassen) und §11 (ICS), Analyse A28/A29 erledigt, CHANGELOG, QA-Bericht, Prüfliste (Kalenderprogramm öffnet die Ausgabe). |
| Umsetzungsstand | ✅ 3.39.1 geliefert: `repeat_ics.py`, Erkennung in `capture_parser.py`, Import-Zeitzonen über `timezones` (A30); 19 Unit-Tests, `test_wiederholung3391`, getrennte Gegenprobe gegen 3.39.0 ([Nachweise](../01_Repository/Glide/tests/qa-3.39.1/wiederholung_2026-10-13/README.md)). |

#### FP-01 Wiederholen nach Rückgängig (WA-01)

| Bestandteil | Beschreibung |
|---|---|
| Paket-ID | FP-01 |
| Titel | Wiederholen für Aufgaben-, Listen- und Strukturänderungen |
| Zielsetzung | Ein versehentliches Rückgängig lässt sich zurücknehmen; Cmd/Strg+Umschalt+Z (Windows zusätzlich Strg+Y) wirkt überall wie erwartet (P1). |
| Ausgangssituation | [Code] `snapshot_undo` legt Schnappschüsse (Listen, Ordner, Labels, Papierkorb als `PackedState`, Ansicht) auf `undo_stack` (`MAX_UNDO_STEPS = 20`); `undo_last_change` stellt über `apply_snapshot` her; eigener Flächenstapel der Pinnwand (`workspace.view_undo_pending`), der sich die Tiefe von `undo_stack` merkt; offene Fokusbuchung sperrt (`recover_time_booking`); Bestandswächter nimmt über `rollback_to_undo_depth` zurück. Vorprüfung 13.10.2026: 38 Aufrufe von `snapshot_undo` und 32 direkte Stapeleingriffe (`pop`, `del`, Rücksetzen) in 31 Methoden, meist zum Zurücknehmen wirkungsloser oder gescheiterter Aktionen; `item_change(background=True)` speichert Zustellbelege ohne Rückgängig-Punkt. Wiederholen gibt es nur in `RichNoteEditor`, `PageEditor` und `DrawingEditor`. |
| Geplante Funktionen | **Stufe 1:** Wiederholen für alle Wege, die über `undo_stack` rückgängig gehen; Bearbeiten › Wiederholen mit stabiler Aktionskennung, Palette, Kürzel; der Rückgängig-Hinweis bietet danach „Wiederholen“; Text- und Zeichenfokus behalten ihre Editorstapel. **Stufe 2:** Wiederholen auch für Pinnwand-Flächenänderungen; der Änderungsverlauf verweist für ältere Stände auf „Sicherungen vergleichen“. |
| Nutzermehrwert | Fehlbedienung folgenlos korrigierbar; Mut zu Strukturaktionen; erwartetes Desktopverhalten. |
| Betroffene Komponenten | `ListApp.snapshot_undo`, `undo_last_change`, `rollback_to_undo_depth`, `trim_undo_stack`, Rückgängig-Hinweis, `build_menu`/`action_catalog.py`, Tastaturbindungen; neues Tk-freies `undo_history.py`. |
| Technische Umsetzung | Schnappschuss-Stapel wie Rückgängig (AE-3): Rückgängig legt den aktuellen Stand auf „Wiederholen“, Wiederholen legt ihn zurück auf „Rückgängig“. **Gültigkeitsregel statt Eingriffen an 32 Stellen:** Ein Wiederholen-Eintrag merkt sich Tiefe und oberstes Objekt von `undo_stack` sowie einen Schreibzähler, den `save_items` bei jedem erfolgreichen Schreiben erhöht (auch für Zustellbelege). Wiederholen ist nur erlaubt, solange alle drei unverändert sind; sonst wird der Stapel verworfen. Wirkungslose Aktionen, die einen Punkt anlegen und wieder entfernen, lassen ihn gültig; jede gespeicherte Änderung macht ihn ungültig. Der Flächenstapel der Pinnwand vergleicht weiterhin Tiefen und wird in Stufe 2 einbezogen. Gleiche Grenze 20. Regeln im Tk-freien Modul, `ListApp` bleibt Adapter (D17). Scheitert das Speichern, bleiben beide Stapel unverändert. |
| Abhängigkeiten | keine; sinnvoll vor weiteren neuen Mutationsarten (FP-02 ff.), damit diese von Beginn an mitgeprüft werden. |
| Kompatibilität | kein Daten- oder Einstellungsformat; Stapel nur im Arbeitsspeicher wie heute. |
| Risiken | Reihenfolge gegenüber dem Flächenstapel; Zeichen-Editor-Flush; Fokusbuchung; Speicher bis 2 × 20 Schnappschüsse; Strg+Y in Windows-Textfeldern. |
| Aufwand | Stufe 1 M, Stufe 2 S |
| Priorität | P1 |
| Akzeptanzkriterien | (1) Jede rücknehmbare Aktion der Einstiegsmatrix (anlegen, löschen, verschieben, einrücken, gruppieren, abhaken mit Wiederholung, einplanen, entlasten, importieren) ist nach Rückgängig mit genau einem Wiederholen wiederhergestellt; Bestand nach JSON-Vergleich gleich dem Zustand vor Rückgängig. (2) Neue Änderung, Laden und Wächterabbruch leeren „Wiederholen“. (3) Text- und Zeicheneditor unverändert. (4) Abhaken 5.000 Punkte weiter ≤ 120 ms (§10); Zusatzspeicher bei 10.000 Punkten gemessen und benannt. (5) Menü, Palette, Kürzel und Hinweis lösen dieselbe Kennung aus. |
| Tests | Unit `test_undo_history.py` (Stapelregeln, Grenze, Leeren); Pflichtsuite über echte Bindungen mit Bytevergleich, Schreibfehler/Retry, Fokusbuchung, Flächenstapel, Neustart; rote Gegenprobe gegen die Vorversion; Regression `test_datenintegritaet` und bestehende Rückgängig-Suiten, Mindestgröße. |
| Dokumentation | Funktionen (Bedienung, Kürzel), Architektur §2 „Rückgängig“, Kürzelübersicht der App, CHANGELOG, QA-Bericht, Plan-Marke, manuelle Prüfliste (Kürzel je Plattform). |
| Umsetzungsstand | **Lokaler Prüfkandidat auf FP-01-Stand:** PR #36 / `9ec474b` ist integriert; Version 3.43.1, Format 25. Wiederholen mit neun Fällen einschließlich 10.001 Aufgaben sowie A33 erneut grün. Die früheren Messwerte und 57 Bereichssuiten bleiben im [FP-01-Nachweis](../01_Repository/Glide/tests/qa-3.43.1/fp01_wiederholen_2026-10-17/README.md) historisch erhalten. 07 und Pakete enthalten den Kandidaten noch nicht; eingefrorener Phasenabschluss und native Abnahmen bleiben offen. |

#### FP-02 Erweiterte Wiederholungsregeln (WA-02)

| Bestandteil | Beschreibung |
|---|---|
| Paket-ID | FP-02 |
| Titel | Wiederholungen mit Intervall, n-tem Wochentag und Bezug auf Erledigung |
| Zielsetzung | Übliche Rhythmen ohne Hilfskonstruktion: „alle zwei Wochen montags und donnerstags“, „am zweiten Dienstag im Monat“, „letzter Werktag im Monat“, „alle 3 Monate am 15.“, „drei Tage nach Erledigung“. |
| Ausgangssituation | [Code] `repeat_rules.py`: Arten `taeglich`, `tage` (1–365), `wochentage`, `woechentlich`, `monatlich`, `jaehrlich`; Start/Ende, Monatsende-Anker (31.01. → 28.02. → 31.03.), Termin und verpasste Termine überspringen (KO02); Folgetermin stets ab Fälligkeit. Schnelleingabe kennt „täglich“, „werktags“, „jeden <Wochentag>“, Wochentagslisten, „alle N Tage/Wochen“ (als N·7 Tage), „monatlich“, „jährlich“ (`capture_parser._wiederholung`; Fehler A29 → FP-00). `ics_recurrence.py` (3.39.0) rechnet RFC-5545-Serien mit INTERVAL, COUNT, UNTIL, BYDAY samt Ordinal, BYMONTHDAY, BYSETPOS und Budget; Vorprüfung: 11.192 Kombinationen ohne Abweichung von einer unabhängigen Referenz (§16.10). |
| Geplante Funktionen | **Stufe 1:** Intervall für Monat/Jahr und für Wochen mit mehreren Wochentagen; n-ter und letzter Wochentag im Monat; letzter Tag bzw. letzter Werktag im Monat (Werktag = Montag bis Freitag, ohne Feiertage); Vorschau der nächsten fünf Termine im Inspektor. **Stufe 2:** Folgetermin ab Erledigung; Serie pausieren; Anzahl Termine mit sichtbarem Rest; Schnelleingabe für die geprüften Formen der Beispieltabelle in §16.10 als Chip mit Ankertag; Ordinal mit Wochentag nur zusammen mit „im Monat“ als Monatsposition (ohne „im Monat“ gilt „jeden zweiten Dienstag“ als „alle 2 Wochen“, siehe FP-00); ICS-Ausgabe als RRULE. |
| Nutzermehrwert | Verlässliche Routinen für Beruf und Alltag; Gleichstand mit Todoist, TickTick, Super Productivity. |
| Betroffene Komponenten | `repeat_rules.py` (Fassade), `ics_recurrence.py` (Rechner), `capture_parser.py`, Wiederholungsfeld im Inspektor (`read_repeat_rule`), `build_ics_document`, Datenformat/Migration; Austauschformat bleibt Stufe 0 für Wiederholungen. |
| Technische Umsetzung | Neue Regeln intern als normalisierte RRULE-Teilmenge plus Bezug (`faellig`/`erledigt`) und Pausenmarke; alle Berechnungen über `ics_recurrence` (AE-2). Die sechs alten Arten bleiben gespeichert, wie sie sind, und rechnen unverändert. Semantik nach RFC 5545 und Super Productivity (MIT) portiert, kein Fremdcode. Fachlogik Tk-frei mit Unit-Tests (D17). |
| Abhängigkeiten | Datenformat-Tor mit der nächsten freien Nummer nach den Paketen 5 und 6 (Vergabe beim Formatschnitt); FP-00 und FP-01 empfohlen vorher. |
| Kompatibilität | **Formatwechsel zwingend:** `repeat_rules.normalize` älterer Fassungen gibt für unbekannte Arten `None` zurück; ohne Tor verlöre eine ältere Fassung die Regel beim nächsten Speichern. Vorsicherung, Migration (Formatnummer; alte Regeln unverändert), schreibgeschützter Altleser. |
| Risiken | Monatsenden, Schaltjahre, Sommerzeit; Bezug auf Erledigung mit Rückgängig/Wiederholen; Verständlichkeit der Eingabesprache; CSV- und Austauschgrenzen benennen. |
| Aufwand | Stufe 1 M, Stufe 2 M (zusammen M–L) |
| Priorität | P1 |
| Akzeptanzkriterien | (1) 30 Referenzregeln: die nächsten 24 Termine gleich einer unabhängig erstellten Tabelle (Monatsende, Schaltjahr, Sommerzeit). (2) Alle sechs alten Arten liefern dieselben Folgetermine wie 3.39.0. (3) Ältere Fassung öffnet den neuen Bestand schreibgeschützt, Vorsicherung vorhanden. (4) Jede erkannte Eingabe erscheint als rücknehmbarer Chip (D01/D10). (5) Überspringen, verpasste überspringen und frühes Erledigen gelten auch für neue Regeln. (6) Ausgegebene RRULE liest `ics_recurrence` mit identischer Terminfolge wieder ein. |
| Tests | Unit für Normalisierung, Terminfolgen und Parser; Altleser- und Migrations-Kindprozess über `tests/integration/vorversion.py`; Pflichtsuite mit Inspektor, Schnelleingabe, Abhaken, Überspringen, Undo, Neustart; rote Gegenprobe; Regression Erinnerungen relativ zur Fälligkeit, Heute/Demnächst, Wochenplanung. |
| Dokumentation | Funktionen §3/§4, Daten und Migration (Format, Regelvertrag), Produktgrenzen (Planung), CHANGELOG, QA-Bericht, Prüfliste. |

#### FP-03 Gespeicherte Ansichten (WA-03, Vorarbeit WA-09)

| Bestandteil | Beschreibung |
|---|---|
| Paket-ID | FP-03 |
| Titel | Gespeicherte Ansichten: vollständige Bedingungen und gespeicherte Darstellung |
| Zielsetzung | Wiederkehrende Sichten wie „diese Woche geplant, ohne Label Warten, nach Liste gruppiert, als Tabelle“ einmal festlegen und mit einem Klick öffnen. |
| Ausgangssituation | [Code] `SavedFilters` (≤ 100) mit Liste, Quelle, Status, Wichtigkeit (genau), Labels (beliebig/alle), festen Fälligkeitsstufen und Text; immer nach Fälligkeit sortiert; Erklärung über `filter_explain.py` (D-03); bis zu vier als Startseitenkachel. Gruppierung und Tabellenspalten werden je Liste gespeichert. |
| Geplante Funktionen | **Stufe 1:** Bedingungen Bearbeitungstag (heute, liegen geblieben, diese/nächste Woche, ohne, Zeitraum), Aufwand (ohne Schätzung, höchstens/mindestens), „wartet auf“ (blockiert/frei), Wichtigkeit „mindestens“, Labels ausschließen; Verknüpfung „alle“ oder „mindestens eine“ (eine Ebene). **Stufe 2:** Darstellung je Ansicht – Liste, Tabelle oder Spaltenboard, Gruppierung, Sortierung, Tabellenspalten; „Als Ansicht speichern“ aus der aktuellen Darstellung. „Warum steht das hier?“ deckt alle Bedingungen ab. |
| Nutzermehrwert | Wiederkehrende Auswertungen ohne Nachbauen; keine doppelte Pflege, weil Ansichten Ableitungen bleiben. |
| Betroffene Komponenten | `SavedFilters`, `filter_explain.py`, neues Tk-freies `view_definition.py`, Filterdialog, `group_columns`/`set_group_value`, Tabellenspalten, Startseitenkacheln, Palette. |
| Technische Umsetzung | Ansichtsdefinition als JSON nach dem Muster AFFiNE/Vikunja (Markt §9.3, T01–T04), ausschließlich über festen Glide-Feldern (AE-1). Reine Auswertung über die vorhandenen Punktfakten; unbekannte Bedingungen sichtbar ungültig, nie still erfüllt. **Speicherort:** neue Bedingungen und Darstellung in einem eigenen Einstellungsschlüssel auf oberster Ebene, je Filterkennung (A27: oberste Ebene überlebt ältere Fassungen); `saved_filters` behält seine bisherigen Felder unverändert, verwaiste Erweiterungen räumt die neue Fassung auf. Treffer bleiben Originale. Ziehen zwischen Gruppen über `set_group_value` (D02). |
| Abhängigkeiten | keine (WA-09 entfällt durch den eigenen Schlüssel; Alternative: Erweiterung innerhalb `saved_filters` nur nach WA-09). |
| Kompatibilität | Datenformat unverändert; Einstellungen additiv. Eine ältere Fassung zeigt einen erweiterten Filter nur mit seinen bisherigen Bedingungen (mehr Treffer, kein Datenverlust) und lässt den Erweiterungsschlüssel unberührt. Bestehende Filter liefern unverändert dieselben Treffer. |
| Risiken | Bedienkomplexität (P5/P6): Standarddialog bleibt kurz, weitere Bedingungen über „Bedingung hinzufügen“; Tempo; verständliche Erklärtexte. |
| Aufwand | Stufe 1 M, Stufe 2 M |
| Priorität | P2 |
| Akzeptanzkriterien | (1) Jede neue Bedingung erscheint in der Erklärung mit ✓/✗ und dem Wert des Punkts. (2) Auswertung bei 10.000 Punkten Median ≤ 100 ms. (3) Gespeicherte Darstellung nach Neustart identisch. (4) Ziehen zwischen Gruppen setzt genau das sichtbare Feld, ein Undo. (5) Alte Filter: gleiche Treffer wie 3.39.0. (6) Dialog bei 860 × 700 und großer Schrift vollständig bedienbar. |
| Tests | Unit `test_view_definition.py` (Normalisierung, Auswertung, Erklärung, Unbekanntes); Pflichtsuite mit Dialog, Kachel, Palette, Gruppieren/Ziehen, Neustart; Messung; rote Gegenprobe; Regression `test_wissen3340` (D-03). |
| Dokumentation | Funktionen §5, Daten und Migration (Einstellungen), CHANGELOG, QA-Bericht, Prüfliste. |

#### FP-04 Seiten und Notizen als Pinnwandkarten (WA-04, Vorarbeit WA-09)

| Bestandteil | Beschreibung |
|---|---|
| Paket-ID | FP-04 |
| Titel | Seiten und Notizen als Karten auf der Pinnwand |
| Zielsetzung | Projektwand mit Wissen und Aufgaben auf einer Fläche, ohne neue Inhaltsart und ohne freie Zettel. |
| Ausgangssituation | [Code] Karten sind Aufgaben/Langtexte und Zeichnungen; Zeichnungskarten tragen `page:<Kennung>` (`ItemWorkspace.PAGE_CARD_PREFIX`), `valid_pages` lässt nur `is_drawing_list` zu; Verbindungen laufen über Kartenkennungen; Vorschau über `page_card_blocks`. |
| Geplante Funktionen | Seite oder Notiz anheften (Seitenleisten-Kontextmenü, Pinnwand „Anheften …“, Ziehen aus der Seitenleiste). Karte zeigt Titel, Pixelsymbol oder Titelbild, die ersten Zeilen (≤ 160 Zeichen) und die Zahl offener Aufgaben; Doppelklick öffnet die Seite; Verbindungen zu Aufgabenkarten; Präsentation und PDF berücksichtigen Seitenkarten; archivierte oder gelöschte Seiten fallen wie Zeichnungen weg. |
| Nutzermehrwert | Projektkontext ohne Wechsel zwischen Seite und Pinnwand. |
| Betroffene Komponenten | `ItemWorkspace.valid_pages`, `page_card_pseudo`, `page_card_blocks`, `prune`, Druck (`board_region_lines`), Seitenleisten-Kontextmenü, `page_features.py`. |
| Technische Umsetzung | `valid_pages` auf nicht archivierte Seiten und Notizen erweitern; Auszug und Aufgabenzahl als Tk-freie Funktion in `page_features.py`, je Aufbau über `render_cached`; Vorschau nur lesend, keine Kopie von Inhalten. |
| Abhängigkeiten | WA-09 (ältere Fassungen entfernen sonst beim `prune` die neuen Seitenkarten aus `settings.json`). |
| Kompatibilität | Datenformat unverändert; Einstellungen additiv. |
| Risiken | Tempo bei vielen Textauszügen; Erwartung „freie Notizzettel“ – Produktgrenze bleibt: jede Karte zeigt ein bestehendes Objekt. |
| Aufwand | M |
| Priorität | P2 |
| Akzeptanzkriterien | (1) Anheften, Verschieben, Verbinden, Entfernen je ein Undo-Schritt im Flächenstapel. (2) Kartentext folgt einer Seitenänderung ohne Neustart. (3) Archivieren/Löschen der Seite entfernt die Karte; Undo stellt beides her. (4) 200 Karten, davon 50 Seitenkarten: Aufbau höchstens 10 % über der bisherigen Pinnwandmessung. (5) Eine ältere Fassung mit WA-09 behält die Seitenkarten. |
| Tests | Unit (Auszug, Aufgabenzahl); Pflichtsuite mit Anheften, Ziehen, Tastatur (H-02), Präsentation, Druck, Undo, Neustart; Altleser mit Vorversion; rote Gegenprobe. |
| Dokumentation | Funktionen §6, Daten und Migration (`pinboards`), Produktgrenzen (Karten nur für Objekte), CHANGELOG, QA-Bericht. |

#### FP-05 Unverknüpfte Erwähnungen (WA-05)

| Bestandteil | Beschreibung |
|---|---|
| Paket-ID | FP-05 |
| Titel | Erwähnungen ohne Verweis finden und verknüpfen |
| Zielsetzung | Bezüge, die nur als Text bestehen, mit einem Schritt zu echten Verweisen machen – deterministisch statt KI-Vorschlag. |
| Ausgangssituation | [Code] typisierte Verweise mit abgeleiteten Rückverweisen (`object_references.py`, Format 22); Inhaltssuche mit Umlautnormalisierung ohne Index (`content_search.py`). |
| Geplante Funktionen | Im Rückverweisbereich einer Seite oder Liste ein eingeklappter Abschnitt „Erwähnt ohne Verweis (n)“: Fundstellen des Titels als ganzes Wort (Mindestlänge 4 Zeichen, Umlautregeln der Suche) in Seiten, Notizen und Beschreibungen; je Fundstelle markierter Ausschnitt mit „Verknüpfen“ (ersetzt die Textstelle durch einen Verweis) und „Öffnen“. |
| Nutzermehrwert | Wissen vernetzt sich ohne zusätzliche Pflege. |
| Betroffene Komponenten | `object_references.py`, `content_search.py` (Normalisierung), Rückverweisbereich im `PageEditor`, vorhandene Verweiserstellung. |
| Technische Umsetzung | Tk-freie Funktion für Fundstellen mit Wortgrenzen; Berechnung erst beim Aufklappen, Ergebnis je Aufbau gehalten; Verknüpfen über den bestehenden Verweisweg. |
| Abhängigkeiten | keine |
| Kompatibilität | kein neues Format (Verweise aus Format 22). |
| Risiken | Fehltreffer bei kurzen oder allgemeinen Titeln (Mindestlänge, bereits verknüpfte Stellen ausnehmen); Tempo bei großen Seiten. |
| Aufwand | S–M |
| Priorität | P2 |
| Akzeptanzkriterien | (1) Fixture mit 20 erwarteten Treffern und 10 Fehltrefferfallen: alle Treffer, keine Falle. (2) „Verknüpfen“ erzeugt denselben Verweis wie der bestehende Weg, ein Undo, Rückverweis sofort sichtbar. (3) 500 Seiten/10.000 Punkte: Aufklappen Median ≤ 150 ms. |
| Tests | Unit; Pflichtsuite mit Aufklappen, Verknüpfen, Undo, Neustart; Messung; rote Gegenprobe. |
| Dokumentation | Funktionen §8 und Abschnitt Verweise, CHANGELOG, QA-Bericht. |

#### FP-06 Wiederverwendbare KI-Aufträge im Austauschformat (WA-06)

| Bestandteil | Beschreibung |
|---|---|
| Paket-ID | FP-06 |
| Titel | KI-Aufträge für das Kontextpaket |
| Zielsetzung | Häufige KI-Aufgaben – Notiz in Aufgaben zerlegen, Projekt mit Aufwand planen, Beschreibung zusammenfassen, Priorisierung mit Begründung vorschlagen, Labels vorschlagen – ohne selbst formulierte Anweisung; Q3-konform, ohne Netz und ohne Abhängigkeit. |
| Ausgangssituation | [Code] „Für KI bereitstellen …“ schreibt `.glidecontext` mit Zweck, Auswahl und Prüfsummen; eine Antwort als Änderungsvorschlag wird mit Feldvergleich, Konflikten, Vorsicherung und einem Undo übernommen (`exchange_patch.py`, G24). |
| Geplante Funktionen | Auswahl „Auftrag“ im Bereitstellen-Dialog mit fünf mitgelieferten Aufträgen; jeder ergänzt das Kontextpaket um eine deutsche Anweisung, das erwartete Antwortschema und die erlaubten Felder; „In Zwischenablage kopieren“ für Chatwerkzeuge; eigene Aufträge als lokale Textvorlagen; Übernahme unverändert über den Prüfdialog. |
| Nutzermehrwert | KI-Hilfe für Strukturierung und Planung mit einem frei gewählten Werkzeug (lokal oder Cloud nach Entscheidung des Nutzers); Datenhoheit und Prüfung bleiben. |
| Betroffene Komponenten | Austauschdialog, Kontextpaket (`build_exchange_payload`), neues Tk-freies `exchange_recipes.py`, versionierte Ressource mit Aufträgen, Spezifikation in Daten und Migration. |
| Technische Umsetzung | Aufträge als Ressource (Kennung, Titel, Zweck, Anweisung, erlaubte Felder). Vorprüfung 13.10.2026 [Code `exchange_patch.build_context`, `EXCHANGE_ROOT_FIELDS`]: Das Kontextpaket trägt bereits ein Feld `instructions`; der Auftrag ergänzt dessen Text, ein neues Feld ist nicht nötig. Änderungsvorschläge (Stufe 2) überarbeiten nur die neun Felder vorhandener Aufgaben – passend für Zusammenfassen, Priorisieren, Aufwand schätzen, Labels. Neue Aufgaben (Notiz zerlegen, Projekt planen) entstehen nur über Stufe 1 (`mode: "create"`); deren Import meldet unbekannte Wurzelfelder, deshalb dort keine zusätzlichen Wurzelfelder verlangen. „Zusammenfassen“ schreibt die Zusammenfassung vor den unveränderten Originaltext der Beschreibung, damit die Übernahme nichts verliert. Kein Formatwechsel. |
| Abhängigkeiten | G24 (✅ 3.35.0) |
| Kompatibilität | Kontextpaket additiv; Antwortformat und Importweg unverändert. |
| Risiken | Antwortqualität fremder KI ist nicht steuerbar – Prüfdialog bleibt Pflicht; Missverständnis „Glide hat eingebaute KI“ – Texte klarstellen; Pflege der Anweisungen. |
| Aufwand | S–M |
| Priorität | P2 |
| Akzeptanzkriterien | (1) Für jeden Auftrag besteht eine Musterantwort den bestehenden Import ohne Fehler. (2) Ohne Auftragswahl bleibt das Kontextpaket bis auf Zeit und Prüfsumme gleich 3.39.0. (3) Kein neues Modul enthält Netzwerkfunktionen (statische Prüfung). (4) Eigene Aufträge überstehen Neustart und App-Backup. |
| Tests | Unit (Auftragsnormalisierung, Paketerweiterung); Rundlauf mit fünf Musterantworten; Pflichtsuite für Dialog und Zwischenablage; rote Gegenprobe; statischer Test ohne `urllib`/`socket`. |
| Dokumentation | Funktionen §11, Daten und Migration (Austauschformat), Produktgrenzen (KI nur über Dokumente), CHANGELOG, QA-Bericht. |

#### FP-07 Offene Ausgabeformate (WA-07)

| Bestandteil | Beschreibung |
|---|---|
| Paket-ID | FP-07 |
| Titel | Gesamtausgabe als Markdown-Ordner und Pinnwand als JSON Canvas |
| Zielsetzung | Datensouveränität und Ausstiegsfähigkeit: gesamter Bestand in einem Schritt als lesbarer Dateibaum; Pinnwand in einem offenen Leinwandformat. |
| Ausgangssituation | [Code] Ausgabe je Liste (TXT/MD/CSV) und je Ordner (TXT/MD), Seiten als Markdown mit Bildern, Druck/PDF, ICS; Bestand ohnehin als lesbares JSON; Pinnwand nur als Druckseite; Pinnwandlayout nur im App-Backup [Dok 06]. |
| Geplante Funktionen | **Stufe 1 „Alles als Markdown-Ordner …“:** Ordnerbaum wie die Seitenleiste; je Seite, Notiz und Liste eine `.md` mit Kopfdaten (Kennung, Art, Labels, Termine); Aufgaben als `- [ ]`/`- [x]` mit Feldern; interne Verweise als relative Links; Anhänge und Bilder kopiert; Tabellen zusätzlich als CSV; `INDEX.md` mit Zählung und Verlustbericht (Wiederholungsdetails, Erinnerungen, Pinnwandlayout). **Stufe 2 „Pinnwand als JSON Canvas …“:** Karten als `text`-Knoten, Seiten- und Zeichnungskarten als `file`-Knoten auf die Dateien aus Stufe 1, Bereiche als `group`, Verbindungen als Kanten mit Pfeilenden nach Richtung, Beschriftung und Farbe. |
| Nutzermehrwert | Vertrauen und Weiterverwendung in Obsidian, AFFiNE, Notion (Markdown-Import) und jeder Textsuche. |
| Betroffene Komponenten | Datei › Ausgabe, `page_markdown.py`, `export_list_as`/`export_folder_as`, neue Tk-freie Module für Ordnerausgabe und Canvas, Anhangspfade. |
| Technische Umsetzung | In temporären Zielordner schreiben und erst am Ende umbenennen; Dateinamen bereinigen (Windows-Zeichen, Länge, Kollisionen); eigener JSON-Canvas-Schreiber nach Spezifikation 1.0 (MIT) in der Standardbibliothek; keine Netz- oder Fremdbibliothek. |
| Abhängigkeiten | Paket 6 vorher empfohlen (gemeinsame Markdown- und Verweisregeln mit dem Notion-Import). |
| Kompatibilität | reine Ausgabe, kein Format. |
| Risiken | lange Windows-Pfade, große Anhänge, Namenskollisionen; Erwartung eines Wiederimports – ausdrücklich nicht Ziel der Stufe 1. |
| Aufwand | Stufe 1 M, Stufe 2 S–M |
| Priorität | Stufe 1 P2, Stufe 2 P3 |
| Akzeptanzkriterien | (1) Showcase vollständig ausgegeben: Zahl der Seiten, Aufgaben und Anhänge gleich dem Bestand; der Verlustbericht nennt jede nicht abgebildete Eigenschaft. (2) Alle internen Links im Ausgabeordner lösen auf. (3) Datenordner nach der Ausgabe bytegleich. (4) `.canvas` erfüllt die Spezifikation (Pflichtattribute, eindeutige Kennungen, gültige Kantenenden) und öffnet in einem Referenzleser (manuelle Probe). (5) Pfade unter Windows ≤ 240 Zeichen. |
| Tests | Unit (Dateinamen, Kopfdaten, Linkauflösung, Canvas-Schema); Pflichtsuite mit Showcase, Abbruch und Schreibfehler; Windows-Pfade in der nativen Matrix; rote Gegenprobe. |
| Dokumentation | Funktionen §11, Daten und Migration (Ausgabe, Verlustbericht), Repository-README (Daten), CHANGELOG, QA-Bericht, Prüfliste. |

### 16.4 Übrige Backlogpunkte

- **WA-08 Zeitauswertung:** Zeiteinträge je Tag aus Fokus- und Handbuchungen (Formattor), Auswertung je Woche/Monat nach Liste und Label mit CSV-Ausgabe im Wochenrückblick; Vorbild Arbeitsprotokoll von Super Productivity. Erst bei belegtem Bedarf.
- **WA-09 Vorwärtsverträgliche Einstellungen:** Unbekannte Schlüssel auf oberster Ebene überleben schon heute (A27). `ItemWorkspace.prune` und die Normalisierer innerhalb von `pinboards` und `saved_filters` erhalten künftig unbekannte Karten und Schlüssel bis zu ihren Grenzen unverändert; eine gemeinsame Regel mit Test „ältere Fassung schreibt Zukunftsfelder verlustfrei zurück“. Zwingend eine Lieferung vor FP-04 (AE-4); für FP-03 nicht nötig.
- **WA-10 Optionaler lokaler KI-Endpunkt:** nur über Entscheidungsvorlage E-W3.
- **WA-11 Seitenvorschau für Verweise:** „Vorschau“ im Kontextmenü eines Verweises zeigt die Zielseite lesend im Inspektorbereich.
- **WA-12 Tagesvorschlag „gibt andere frei“:** Aufgaben, auf die andere warten, erhalten einen eigenen erklärten Grund vor „wichtig“ (`day_proposal.REASONS`); Tk-frei, kein Format.
- **WA-14 Wiederkehrende Vorlagen:** Vorlage plus Regel aus FP-02 legt zum Termin eine Liste oder Seite an.
- **WA-15 Rangfolge der Inhaltstreffer:** BM25-Formel über den vorhandenen Treffern, ohne Index; nur nach belegter schlechter Rangfolge.
- **WA-16 Wartbarkeitskennzahl:** Pflegewerkzeug schreibt je Lieferung Zeilen von `ListApp`, Zahl der Tk-freien Module und Unit-Tests in den Nachweis.

### 16.5 Entscheidungsvorlagen für den Inhaber

Nummeriert nach dem bewährten Muster (Übergabe §4); Kurzantwort etwa „E-W7 A, E-W1 A/V, E-W2 A/1“. Die Empfehlungen gelten als D49-Auslegung mit Korrekturvorbehalt; keine erneute Zustimmung wird fingiert. D50 hat die Folge geändert. D51 ist auf dem separaten Planungszweig belegt; neue tatsächlich ausgewählte Produktentscheidungen beginnen bei D52. Aktuelle Entscheidungsvorlagen ausschließlich §20.

| Nr. | Frage | A/1 – erste Stufe | A/V – vollständig | B / C | Empfehlung |
|---|---|---|---|---|---|
| E-W1 | FP-01 Wiederholen | Aufgaben- und Strukturänderungen; M | zusätzlich Pinnwandfläche und Verlaufshinweis; M+S | B auslassen | A/V |
| E-W2 | FP-02 Wiederholungsregeln | Intervalle, n-ter/letzter Wochentag, letzter (Werk-)Tag, Terminvorschau; M; Formattor | zusätzlich ab Erledigung, Pause, Anzahl, deutsche Schnelleingabe, RRULE-Ausgabe; M–L; ein Formattor | B auslassen | A/V (das Formattor fällt nur einmal an) |
| E-W3 | KI-Richtung | – | – | A: Q3 bleibt, nur FP-06 · B: zusätzlich WA-10 lokaler Endpunkt (nur `localhost`, Vorgabe aus, Prüfdialog Pflicht) als Ergänzung von Q3 · C: weder noch | A; WA-10 nach Nutzungserfahrung mit FP-06 neu bewerten |
| E-W4 | FP-03 | neue Bedingungen; M | zusätzlich gespeicherte Darstellung; M+M | B auslassen | A/V mit eigenem Einstellungsschlüssel (ohne WA-09) |
| E-W5 | FP-04, FP-05, FP-07 je einzeln | FP-07 nur Markdown-Ordner | jeweils vollständig | B auslassen | FP-05 A/V, FP-04 A/V nach WA-09, FP-07 A/1 |
| E-W6 | Einordnung | – | – | A: neuer Sprint nach 4.0.0 · B: FP-01 zwischen 3.40.0 und 3.41.0 einschieben (ändert die durch D44 bestätigte Reihenfolge) | A – bestätigten Plan nicht unterbrechen |
| E-W7 | FP-00 Fehlerbehebung | – | – | A: kleine eigene Fehlerbehebungslieferung direkt nach dem Lieferabschluss von 3.39.0, vor Paket 5 (ändert die durch D44 bestätigte Folge um eine Zwischenlieferung) · B: nach 4.0.0 mit W1 · C: als bekannte Grenze dokumentieren | A – Fehler in einer Kernfunktion, klein, ohne Formatwechsel |

### 16.6 Architekturentscheidungen: geprüfte Alternativen

| Nr. | Thema | Geprüfte Alternativen | Empfehlung | Begründung |
|---|---|---|---|---|
| AE-1 | Ansichtsmodell | (a) neue Ansichtsart mit eigener Datenhaltung · (b) Datenbankblock wie AFFiNE/AppFlowy · (c) gespeicherte Filter erweitern | (c) | keine Parallelstruktur; feste Felder (N15–N20); vorhandene Erklärung D-03 weiterverwendbar |
| AE-2 | Wiederholungsrechner | (a) `repeat_rules.py` erweitern · (b) `ics_recurrence.py` als einziger Rechner hinter der bestehenden Fassade · (c) `dateutil.rrule` | (b) | Rechner vorhanden und geprüft; (c) wäre neue Laufzeitabhängigkeit; (a) verdoppelt Logik weiter (A26) |
| AE-3 | Wiederholen | (a) Befehlsmuster mit inversen Operationen · (b) Schnappschuss-Stapel wie Rückgängig | (b) | gleicher Weg wie Rückgängig und Bestandswächter; (a) verlangte Umbau aller Mutationswege |
| AE-4 | Vorwärtsverträglichkeit der Einstellungen | (a) Einstellungs-Formattor mit Schreibschutz · (b) unbekannte Schlüssel erhalten | zuerst (b), (a) nur bei Bedeutungswechsel | billig, wirkt rückwirkend für alle künftigen Erweiterungen; Lehre 3.29/3.30 |
| AE-5 | Lokale KI | (a) eingebettetes Modell über native Bindung · (b) externer Dienst über HTTP auf `localhost` · (c) Dateiaustausch | jetzt (c); (b) nur nach E-W3; (a) ✕ | (a) native Abhängigkeit und GB-große Modelle im Paket; (b) berührt Q3 |
| AE-6 | Toolkit-/Framework-Wechsel | Qt (PySide6), Web (Electron/Tauri), Flutter | kein Wechsel | Nutzen (Kantenglättung, reichere Editoren, Zugänglichkeit) teils über Tk 9/9.1 erreichbar (SVG/PNG, Paket 8); Kosten: Neubau der Tk-gebundenen Oberfläche (lokale AST-Zählung in Analyse §9), die überwiegend an Tk gebunden sind, Verlust der geprüften Tk-Lösungen und Suiten, neue Abhängigkeiten. D03/Q4 bleiben; Neubewertung nur, wenn Paket 8 scheitert oder D03 aufgehoben wird |
| AE-7 | Speicher | JSON (D16) · SQLite · CRDT (Yjs/yrs) | JSON | CRDT dient bei AFFiNE/AppFlowy der Synchronisation (G23 ✕); Logseq-Beta zeigt das Risiko eines Speicherwechsels |

### 16.7 Empfohlene Reihenfolge

Diese Tabelle dokumentiert die bisherige Empfehlung vom 13.10.2026, **keine aktuelle Startfolge**. FP-01 begann upstream bereits am 17.10. außerhalb der lokalen Wurzel. Die konsolidierte Empfehlung unter Berücksichtigung D50 und Abschlussauftrag 15.10. steht in §19. Versions-/Formatnummern entstehen erst im späteren Umsetzungsauftrag.

| Folge | Inhalt | Prio | Abhängig von | Warum hier |
|---|---|---|---|---|
| W0 (ohne App-Version) | WA-13 Dokumentabgleich ✅; Vorprüfungen §16.10 ✅; Entscheidungsvorlagen E-W1–E-W7 | P0/– | – | erledigt bzw. Voraussetzung jeder Auswahl |
| W0b | FP-00 Fehlerbehebung Wiederholungen | P0 | – | ✅ 3.39.1 geliefert; ohne Formatwechsel, mit A30 |
| W1 | FP-01 Wiederholen und WA-09 Vorwärtsverträglichkeit | P1 | – | beide klein, ohne Formatwechsel; sichern alle folgenden Pakete ab |
| W2 | FP-02 Wiederholungsregeln | P1 | Formattor, FP-01 | größter Alltagsnutzen; ein Formatschnitt |
| W3 | FP-05 und FP-04 (Seiten im Kontext) | P2 | WA-09 für FP-04 | beide verbinden Seiten mit ihrem Umfeld; kein Format |
| W4 | FP-03 Gespeicherte Ansichten | P2 | – | eigener Einstellungsschlüssel; Bedienentwurf Stufe 2 vorher |
| W5 | FP-06 KI-Aufträge und FP-07 Stufe 1 | P2 | G24, Paket 6 | beide im Bereich Datei › Austausch/Ausgabe |
| später | WA-12, FP-07 Stufe 2, WA-11, WA-16, WA-14, WA-08, WA-15; WA-10 nur nach E-W3 | P3 | je Eintrag | nach Bedarf |

### 16.8 Umsetzungsreife

| Paket | Spezifikation | Vorbereitendes Refactoring | Entscheidung / verbleibendes Tor | Datenmigration | Erforderliche Testabdeckung |
|---|---|---|---|---|---|
| FP-00 | ausreichend; Beispiel- und Fallenliste liegt als Probe vor | – | E-W7 A durch D49; geliefert 3.39.1 | nein | Parser-Positiv-/Fallenfälle, RRULE über alle Starttage |
| FP-01 | upstream Kandidat Stufe 1+2 und gezielte Prüfungen vorhanden | Extrakt upstream vorhanden, lokal fehlt er | D49-Auslegung; vollständiger Liefer-/Plattformabschluss offen | nein | Vollmatrix, reale Tastenwege und Baseline-Zoomfall vor Abschluss klären |
| FP-02 | ausreichend; Beispieltabelle der Eingabesprache gegen `ics_recurrence` geprüft (§16.10) | `repeat_rules.py` als Fassade über `ics_recurrence.py`; alte Arten rechnen weiter selbst (Monatsende-Anker weicht von RFC ab) | E-W2 A/V durch D49; Formatnummer beim Schnitt | ja | Referenztermine aus unabhängiger Rechnung (Werkzeug liegt vor), Altleser-Kindprozess |
| FP-03 | Stufe 1 ausreichend; Stufe 2 braucht Bedienentwurf des Dialogs | – (eigener Einstellungsschlüssel) | E-W4 A/V durch D49 | Einstellungen additiv | Referenzbestand für Filtertreffer, Messung |
| FP-04 | ausreichend | WA-09 | E-W5 durch D49 gemäß §16.5 | nein | Pinnwand-Altleser, Messung mit 200 Karten |
| FP-05 | ausreichend | – | E-W5 durch D49 gemäß §16.5 | nein | Treffer-/Fallen-Fixture |
| FP-06 | ausreichend; Austauschweg geprüft (`instructions` vorhanden, Erstellen nur über Stufe 1) | – | E-W3 A durch D49; kein lokaler KI-Endpunkt | nein | Musterantworten je Auftrag, beide Stufen |
| FP-07 | Stufe 1 ausreichend | gemeinsame Markdown-Regeln mit Paket 6 | E-W5 durch D49 gemäß §16.5 | nein | Showcase-Rundlauf, Linkauflösung, Canvas-Schema |

**Aktuelle Umsetzungsreife:** FP-00 geliefert. FP-01 und Schutzrunde sind im lokalen Prüfkandidaten integriert und gezielt geprüft; der Lieferabschluss fehlt. FP-05/FP-06/WA-12 besitzen einen umsetzbaren Entwurf; FP-03 Stufe 2 braucht noch den Bedienentwurf. D49 bleibt Auslegung, die durch D50 und den Abschlussauftrag 15.10. überholte Folge ist keine automatische Startanweisung. Neuplanung und Abhängigkeiten §19, offene echte Produktfragen §20.

### 16.9 QA-Strategie für die Vorschläge

Es gelten Prüfplan, §15.3 und §15.8 unverändert: Tk-freie Unit-Tests (D17), Pflichtsuite mit roter Gegenprobe gegen die Vorversion, eingefrorene Mac-Vollprüfung, native Linux-/Windows-Matrix (D35/D42), Mindestgröße, große Schrift, hell und dunkel, Tempo nach §10, Altleser-Kindprozess bei jedem Formatschnitt, Menschenabnahme getrennt (I6). Zusätzlich aus dieser Analyse:

1. **Vorwärtsverträglichkeit** als fester Test ab WA-09: Die Vorversion öffnet einen Einstellungsstand mit Zukunftsfeldern und schreibt ihn verlustfrei zurück.
2. **Unabhängige Referenzwerte** für Wiederholungstermine (Tabelle aus getrennter Rechnung, nicht aus dem Code unter Test).
3. **Bytevergleich im Rundlauf** Rückgängig → Wiederholen.
4. **Statischer Netzwerktest** für KI-nahe Module (keine `urllib`-/`socket`-Nutzung ohne Entscheidung).
5. **Ausgabevalidierung:** Linkauflösung im Markdown-Ordner, JSON-Canvas-Schema, unveränderter Datenordner.
6. **Fallenlisten für die Schnelleingabe:** Jede Eingabe wird ganz oder gar nicht gedeutet; die Proben aus `probe_wiederholung.py` sind Ausgangsbestand.
7. **Gegenrechnung statt Selbstbestätigung:** Terminfolgen und RRULE-Abbildungen gegen `gegenprobe_rrule.py` bzw. eine Referenztabelle prüfen.

### 16.10 Vorprüfungen zur Umsetzungsreife (13.10.2026)

Nur lesend, ohne Tk-Fenster, am Lieferstand `7995ecbc…`; Werkzeuge und Ergebnisse im [Nachweis](../01_Repository/Glide/tests/qa-3.39.0/wettbewerbsanalyse_2026-10-13/README.md).

| Prüfung | Ergebnis | Folge |
|---|---|---|
| Unabhängige Gegenrechnung von `ics_recurrence.dates` (`gegenprobe_rrule.py`, eigenständige Tag-für-Tag-Abtastung nach RFC 5545) | 11.192 zufällige Regel-/Startkombinationen aus drei Reihen ohne Abweichung; Randfall UNTIL vor DTSTART liefert keinen Termin (Auslegungsfrage) | Rechner ist tragfähige Grundlage für FP-02 (AE-2); 3.39.0-Belegzeiten zusätzlich bestätigt |
| Wiederholungsangaben der Schnelleingabe (`probe_wiederholung.py`) | Teilerkennung oder Fehldeutung in 10 von 14 Proben, Details A29 | Fehler → FP-00 (WA-18) |
| Glide-Folge gegen ICS-Ausgabe | 4 von 5 Monatsende-/Schaltjahrproben weichen ab, der Korrekturvorschlag stimmt in 5 von 5 | Fehler → FP-00 (WA-17) |
| Rückgängig-Inventar für FP-01 | 38 Aufrufe `snapshot_undo`, 32 direkte Stapeleingriffe in 31 Methoden, Zustellbelege ohne Rückgängig-Punkt | Gültigkeitsregel mit Schreibzähler statt Einzeleingriffen |
| Einstellungsnormalisierung für FP-03/FP-04 | oberste Ebene bleibt erhalten, innerhalb bekannter Strukturen nicht (A27) | FP-03 ohne WA-09; WA-09 nur vor FP-04 |
| Austauschweg für FP-06 | `instructions` vorhanden; Stufe 2 nur Überarbeiten; Stufe 1 meldet unbekannte Wurzelfelder | kein Formatwechsel; Aufträge nach Stufe getrennt |

**Geprüfte Beispieltabelle der Eingabesprache für FP-02** (Regel mit `ics_recurrence.parse_rule` akzeptiert, erste Termine ab Dienstag 13.10.2026 gerechnet):

| Eingabe | Regel | Erste Termine |
|---|---|---|
| alle 2 Monate | `FREQ=MONTHLY;INTERVAL=2` | 13.10., 13.12.2026, 13.02.2027 |
| alle 3 Monate am 15. | `FREQ=MONTHLY;INTERVAL=3;BYMONTHDAY=15` | 15.10.2026, 15.01., 15.04.2027 |
| jedes Quartal | `FREQ=MONTHLY;INTERVAL=3` | 13.10.2026, 13.01., 13.04.2027 |
| alle 2 Jahre | `FREQ=YEARLY;INTERVAL=2` | 13.10.2026, 13.10.2028 |
| alle 2 Wochen montags und donnerstags | `FREQ=WEEKLY;INTERVAL=2;BYDAY=MO,TH` | 15.10., 26.10., 29.10.2026 |
| am zweiten Dienstag im Monat | `FREQ=MONTHLY;BYDAY=2TU` | 13.10., 10.11., 08.12.2026 |
| jeden ersten Montag im Monat | `FREQ=MONTHLY;BYDAY=1MO` | 02.11., 07.12.2026, 04.01.2027 |
| letzten Freitag im Monat | `FREQ=MONTHLY;BYDAY=-1FR` | 30.10., 27.11., 25.12.2026 |
| am Monatsende | `FREQ=MONTHLY;BYMONTHDAY=-1` | 31.10., 30.11., 31.12.2026 |
| letzter Werktag im Monat | `FREQ=MONTHLY;BYDAY=MO,TU,WE,TH,FR;BYSETPOS=-1` | 30.10., 30.11., 31.12.2026 |
| erster Werktag im Monat | `FREQ=MONTHLY;BYDAY=MO,TU,WE,TH,FR;BYSETPOS=1` | 02.11., 01.12.2026, 01.01.2027 (Feiertag; Werktag = Mo–Fr) |
| wöchentlich, 10 Termine | `FREQ=WEEKLY;COUNT=10` | 13.10., 20.10., 27.10.2026 |

„Ab Erledigung“ und „pausieren“ sind keine RRULE-Teile; sie werden als eigene Felder neben der Regel geführt (FP-02 Stufe 2).


**Abschlussauftrag 15.10.2026 (vormittags; Priorität seit D50 geändert, §17):** Der Inhaber möchte die nächsten Schritte und Pakete neu strukturieren. Zunächst die laufenden 4.0-Arbeiten samt notwendigen Korrekturen, Prüfungen und umsetzbaren Kernfunktionen zum gesicherten Abschluss bringen. Danach Übergabe mit tatsächlichem Lieferstand, umgesetztem Umfang, Prüfbelegen und ausdrücklich offenen Abnahmen; weitere Folgepakete erst aus der neuen Planung starten. D49-Auswahlinhalte bleiben erhalten, ihre Ausführungsfolge wird anschließend neu geordnet.

## 17. UI-/UX-Feature-Paket aus Nutzerbeobachtungen (15.10.2026)

**Ausgangsreferenz:** Glide 3.42.0, 15.10.2026, 13:42 Uhr. **Auftrag:** am 15.10.2026 als vorrangig vor Paket 8 beauftragt (D50). Umgesetzt auf `claude/ui-ux-paket` (Basis `origin/main` `27bac83` mit der P8-Vorbereitung bis PR #26; deren additive Zugänglichkeitsanbindungen bleiben unverändert und reisen mit 3.43.0 mit, ohne Paket 8 zu liefern). **Geliefert als 3.43.0 am 16.10.2026** nach `07_Python-Versionen` und `05_Probelisten_Testdaten`; eingefrorene Windows-Vollprüfung und Punkt-für-Punkt-Matrix im [Nachweis](../01_Repository/Glide/tests/qa-3.43.0/ui_ux_paket_2026-10-16/README.md). Offen: Mac-Vollprüfung und Mac-Bundle (nur auf dem Referenz-Mac), eigenständige Pakete 3.43.0, Menschenabnahme, Produktentscheidungen E-U1–E-U3.

[Vollständiger Ausführungsprompt](Featurepaket_UI_UX/PROMPT.md) · [unveränderter Originalauftrag](Featurepaket_UI_UX/AUFTRAG.md) · [Bildreferenzen S01–S28](Featurepaket_UI_UX/BILDREFERENZEN.md) · [Design Richtlinien](../01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md) · [Prüfnachweis](../01_Repository/Glide/tests/qa-3.43.0/ui_ux_paket_2026-10-16/README.md).

Die Kennungen bilden die Originalnummerierung ab (A01 = A.1, B01 = B.1 …). **Belege:** Pflichtsuite `tests/integration/test_uiux_paket.py` (17 Fälle, alle grün; dieselben 17 Fälle gegen den 3.42.0-Quellbaum alle rot mit dem jeweiligen Ursprungsfehler), 711 Unit-Tests, Vorher-/Nachher-Fensteraufnahmen desselben Kontexts (künstliche Showcase-Daten, Windows 11/Tk 9.0.4). Menschliche Sicht-, DPI- und Screenreaderabnahme bleibt für alle Punkte getrennt offen.

| ID | Gegenstand | Status | Umsetzung / Beleg | Rest |
|---|---|---|---|---|
| A01 | Kompaktmodus, kleinere Mindestgröße | ◐ untersucht, Auswahl offen | Ursachen der Grenze 860 × 700 und Entwurf unten; Probe an echten Inhalten | Produktentscheidung E-U1 |
| A02 | Zweitfenster oder geteilte Ansicht | ◐ untersucht, Auswahl offen | Optionen, Konflikt mit „eingebettet“, Aufwand unten | Produktentscheidung E-U2 |
| A03 | Notion-Muster | ◐ untersucht, Auswahl offen | priorisierte Tabelle in [Markt und Vorbilder §10](Glide_Markt_und_Vorbilder.md#10-notion-muster-für-glide-a03-15102026) | Produktentscheidung E-U3 |
| B01 | Startseite nach „Gelesen“ an den Anfang | ✅ 3.43.0 | `_refresh_home` setzt nach „Gelesen“ die Lage 0; Suite b01 (vorher 0,27) | Mac-Abnahme, Menschenabnahme |
| B02 | „Startseite anpassen“ links | ✅ 3.43.0 | linke Rasterkante bei 860/1280/1600 px; b02 | Mac-Abnahme, Menschenabnahme |
| B03 | Gismo fest, Spielereien aktiv | ✅ 3.43.0 | `home_tiles.retire_mascot_settings`, Sichtbarkeit nur über die Kachel; b03, Unit-Tests | Mac-Abnahme, Menschenabnahme |
| B04 | Galeriebilder auf der Startseite | ✅ 3.43.0 | Kachel „Galeriebilder“ (Standard, eigene Auswahl bleibt), Vorschau im Leerlauf, Klick öffnet Bild; b04 | Mac-Abnahme, Menschenabnahme |
| B05 | Logohöhe | ✅ 3.43.0 | Großbuchstabenhöhe bis Grundlinie der Unterzeile; b05 (vorher 6 px darunter) | Mac-Abnahme, DPI-Sichtprüfung |
| B06 | Datum/„?“ weg, Hinweisschalter | ✅ 3.43.0 | Einstellung `show_hints`, Übernahme alter Wahl; Bedienwege in Textzeilen (Kopfnotiz, Werkzeugzeile, Kartenfuß, Papierkorb, Spaltenboard) folgen dem Schalter; Handbucheintrag; b06_b15, Unit-Tests; D11 fortgeschrieben | Mac-Abnahme, Menschenabnahme |
| B07 | Menüs und Kopfsymbole ausgerichtet | ✅ 3.43.0 | eine Titelzeile, `HEADER_CONTROL_HEIGHT`; b07 (vorher 10 px Versatz) | Mac-Abnahme, DPI-Sichtprüfung |
| B08 | Linke Flucht Fehlerprotokoll | ✅ 3.43.0 | Dialogüberschrift ohne Labelrand; b08 (vorher 3 px) | Mac-Abnahme, Menschenabnahme |
| B09 | Pfeile/Papierkorb optisch zentriert | ✅ 3.43.0 | `glyph_metrics.py`: Bereichspfeile −0,3 px, Papierkorbsymbol +2 px auf Bezugsform; Pfadtrenner „›“ in Startseitenknöpfen (Kachel „Pinnwände“) einzeln auf die Großbuchstabenmitte (−0,05 statt +0,95 px), Schreibweise unverändert; b09 | Mac-Abnahme, DPI-Sichtprüfung |
| B10 | Lupe statt „Su“ | ✅ 3.43.0 | ⌕ aus Segoe UI Symbol (Windows) nach `SYMBOL_FONT_FALLBACKS`; b10; D29 präzisiert | macOS/Linux nativ prüfen |
| B11 | Informationspriorität, Titelbreite | ✅ 3.43.0 | Matrix je Ansicht in Design Richtlinien; Metadaten auf Inhaltsbreite (Labels 177 statt 281 px), bei Enge ganz ausgeblendet statt abgeschnitten; b11 prüft Labels, Heute und Liste | Sichtprüfung bei großer Schrift |
| B12 | Eindeutige Pfeile in Heute | ✅ 3.43.0 | kein ▶/△ neben dem Aufklapppfeil; b12_b13 | Mac-Abnahme, Menschenabnahme |
| B13 | Nächste Aufgabe nur Titel fett | ✅ 3.43.0 | Zelltag `today_next_title` in Zeilengröße; b12_b13; D22 präzisiert | Mac-Abnahme, Menschenabnahme |
| B14 | Kein Kästchen vor „Aufgabe“ | ✅ 3.43.0 | Blockleiste; b14 | Mac-Abnahme, Menschenabnahme |
| B15 | Papierkorbtext, Buttonschutz | ✅ 3.43.0 | kurzer Text, `_follow_empty_text`; 12 Kombinationen ohne Überdeckung (b06_b15); appweit jeder sichtbare Knopf in 7 Ansichten und 5 Dialogen (b15_appweit, gegen 3.42.0 rot mit S21); dabei „Nur offene“ im Spaltenboard behoben (Zeile bricht um); unter Tk 9.1 (GitHub, Linux und Windows) Leertextüberdeckung gefunden und behoben (platzierter statt gemappter Leertext, Map/Configure ziehen nach); Regel in Design Richtlinien | Sichtprüfung seltener Dialoge, DPI |
| B16 | Scrollsprung über Bildern | ✅ 3.43.0 | Rad über Bild pixelweise wie Text; größter Schritt 30 statt 389 px (b16) | Trackpad/macOS nativ |
| B17 | Hintergrundkästen oberer Aktionen | ✅ 3.43.0 | Trägerfläche statt Fensterfarbe, konturlose Knöpfe in Ruhe durchsichtig; b17_b19 | alle Designs sichten |
| B18 | Neuerungen unter „Über Glide“ | ✅ 3.43.0 | „Neuerungen …“ aus `release_notes.history_text`; b18; Pflegeverfahren in Veröffentlichung | Katalogeintrag der neuen Version beim Versionswechsel |
| B19 | Hintergrundkästen Punktbearbeitung | ✅ 3.43.0 | `DueField.surface`, Kalenderknopf in `blend_embedded_editor`; b17_b19 | alle Designs sichten |
| B20 | Skills neutral als Design Richtlinien | ✅ 3.43.0 | Skill `design-richtlinien`, Fremdtext mit Lizenz unter `referenzen/`; alle 15 Skills aus `skills-main/` begründet übernommen oder ausgeschlossen (Design Richtlinien); Prüfung `test_design_richtlinien.py` | – |
| B21 | Verständliche Übergabe | ✅ 3.43.0 | über Übergabe, Arbeitsvorbereitungsindex und Plan auffindbar; Originalauftrag und Bilder getrennt von Regeln (Design Richtlinien) und Status (§17); Prüfmatrix im [Nachweis](../01_Repository/Glide/tests/qa-3.43.0/ui_ux_paket_2026-10-16/README.md#prüfung-aller-punkte-des-originalauftrags) | fortlaufende Pflege mit jeder Nutzeranweisung |
| B22 | Dokumentation/Ablage/Projektauftritt zuletzt | ✅ 3.43.0 | Stand-, Versions-, Entscheidungs- und Archivangaben abgeglichen (u. a. D01–D50, Archiv-README, Showcase-README), Projekt-README aktualisiert; Ablage auf sieben Versionen gekürzt; Push und Merge über PR #27 (`fe9366c`) | GitHub nach PR #32 (`eb5658c`, [Lauf 38979558948](https://github.com/n05a-design/glide-to-do/actions/runs/38979558948)) vollständig grün: Grundstufe, Linux- und Windows-Vollprüfung mit eigener Tk 9.1 einschließlich der drei Linux-Suiten aus PR #26, eigenständiger Windows-Paketlauf mit der ACL-Restaurierung aus dem [Nachlauf 16.10.](../01_Repository/Glide/tests/qa-3.43.0/acl_symlinks_2026-10-16/README.md) |

**Status „✅ 3.43.0“** heißt hier: umgesetzt, automatisch geprüft (Windows lokal eingefroren, 110 Schritte ohne roten Schritt) und nach 07/05 geliefert. Die native Linux-/Windows-Matrix der GitHub-Prüfung ist seit PR #32 (3.43.1) vollständig grün. Abweichend von §Statusmarken fehlen noch die eingefrorene Mac-Vollprüfung und das Mac-Bundle; beide werden auf dem Referenz-Mac nachgeholt.

**3.43.1 – Kürzel in Listen unter Linux/Tk 9.1 (✅ 3.43.1, 16.10.2026, Produktionsrunde auf Wunsch des Inhabers):** Die seit PR #26 roten Linux-Suiten ausgewertet (Lauf 38930140166). `test_tempo330` und `test_oberflaeche33321` erzeugten Tk-9.1-/Xvfb-Ereignisse falsch bzw. isolierten die Systemerkennung zu spät – Prüfwerkzeuge korrigiert. `test_planen33313` zeigte einen Glide-Fehler: Unter X11 lösen Strg-Buchstaben-Kürzel auch Tks Emacs-Navigation aus, auf die die Treeview seit Tk 9.1 reagiert; die Auswahl sprang vor „Einplanen“. Behoben mit `guard_x11_emacs_navigation` und Tk-freier Regel in `interaction_policy.py`; eingefrorene Windows-Vollprüfung 111 Schritte, 108 grün (91 von 92 Suiten, 714 Units); `test_tag3390` dabei rot, unter 3.43.0 gleich rot (Fokus/Sichtbarkeit, nicht durch 3.43.1) – Ursache im [Prüfwerkzeugnachlauf 17.10.2026](../01_Repository/Glide/tests/qa-3.43.1/wackelsuiten_windows_2026-10-17/README.md) belegt und behoben, App unverändert. GitHub nach PR #32 (`eb5658c`, [Lauf 38979558948](https://github.com/n05a-design/glide-to-do/actions/runs/38979558948)) vollständig grün einschließlich Windows-Paketlauf. Offen: Mac-Vollprüfung/Bundle, Linux-Tastaturabnahme D5 der [Prüfliste](Glide_Manuelle_Pruefung.md). [Nachweis](../01_Repository/Glide/tests/qa-3.43.1/kuerzel_linux_tk91_2026-10-16/README.md).

**Beobachtung außerhalb des Pakets:** `test_ui_followup36.py` bleibt auf diesem Windows-Rechner in `root.update()` hängen – identisch am unveränderten Stand `27bac83` (Gegenprobe). Kein Befund dieses Pakets; vor dem Volllauf auf dem Referenz-Mac bzw. in der nativen CI prüfen. `test_template_workflows` und `test_tag3390` wackelten am 16./17.10.2026 unter 3.43.1 und 3.43.0 gleich; im [Prüfwerkzeugnachlauf 17.10.2026](../01_Repository/Glide/tests/qa-3.43.1/wackelsuiten_windows_2026-10-17/README.md) belegt und behoben: Das Auswahl-Popup schloss richtig, sobald der Desktop einem anderen Programm den Vordergrund gab, `test_tag3390` setzte denselben Vordergrund voraus und bediente Dialoge nach festen 80 ms vor Tks Layout. Kein Produktbefund. Ebenso unverändert vorhanden: In der Showcase-Liste „Vermarktung · Umsetzung“ steht über der Pinnwand der Inhalt der Seite „Parkquartier · Briefing und Freigabe“ (gleiches Bild am Ausgangsstand).

### 17.1 A01 – Kompaktmodus und kleinere Mindestgröße

**Befund (Code):** Die Grenze 860 × 700 setzt `ListApp.__init__` fest (`root.minsize`). Was sie trägt: Seitenleiste rund 250 px (schmal 64 px, ausblendbar), Kopfzeile mit Titel ≥ 140 px, unter Windows vier Menüs (rund 300 px) und vier Kopfsymbole (rund 200 px), Aktionsreihen (`ACTION_DENSITY_MIN_WIDTH` 700 px) und Höhenstufen (`HEIGHT_DENSITY_*` 850/780 px). Darunter weichen bereits heute schrittweise Labelspalte (Baum < 636 px), Fälligkeit (< 400 px), Inspektor (Fenster < 980 px → Maske) und Druck/Einstellungen (Überlaufmenü). Die Grenze ist also keine einzelne Ansicht, sondern die Summe aus Seitenleiste, Kopf und Aktionsreihen.

**Vergleich:** *Allgemeine Verkleinerung* des Normalfensters würde jede Ansicht unter 860 px testpflichtig machen (über 90 Suiten mit Mindestgrößenfällen) und Kernfunktionen in Überlaufmenüs drängen. *Ausdrücklich aktivierter Kompaktmodus* (Vorbild Microsoft To Do, S10/S11) blendet nur in diesem Zustand Seitenleiste, Menüband und Aktionsreihen aus und erlaubt eine kleinere Mindestgröße; der Normalmodus bleibt unverändert.

**Entwurf:** Ansicht › „Kompaktmodus“ (Kürzel, Befehlspalette, Knopf im Kopf). Gezeigt werden nur Titel des geöffneten Inhalts, Lupe (Inhalt wechseln über die vorhandene Suche Strg/Cmd+O), Schnellerfassung und Rückweg („Kompaktmodus beenden“, auch Esc/Kürzel). Eingabezeile bleibt, Aktionsreihen weichen ins „…“-Menü, der Inspektor öffnet als vorhandene Maske, Hinweise folgen dem Schalter aus B06. Fensterlage und -größe beider Modi werden getrennt gemerkt. **Zielgröße:** Vorschlag 480 × 560 px als Untergrenze im Kompaktmodus; vor einer Festlegung mit echten Inhalten (Liste, Heute, Seite, Notiz, große Schrift, lange Titel) messen – die Mindestgröße wird erst nach Auswahl verbindlich.

**Probe an echten Inhalten (15.10.2026, Windows 11/Tk 9.0.4, Showcase-Daten, Seitenleiste ausgeblendet, Mindestgröße nur für die Messung aufgehoben):** Bei 860 × 700, 640 × 620, 560 × 600, 480 × 560 und 420 × 520 blieben Liste, Heute und Seite ohne überlappende Knöpfe bedienbar; Inhalt und Eingabezeile bleiben sichtbar, die Metadatenspalten weichen planmäßig. Ab 560 px Breite wird jedoch der Kopf zum Engpass: Unter 560 px verschwinden Titel sowie die Windows-Menüs „Ansicht“ und „Hilfe“ (nur „Datei“ und „Bearbeiten“ bleiben), das Suchfeld wird auf wenige Zeichen gekürzt. Ergebnis: Eine allgemeine Verkleinerung würde Kernfunktionen verdecken (Regel B15); ein Kompaktmodus braucht einen eigenen, reduzierten Kopf (Menüs gebündelt in einem Knopf, Titel bleibt). Die Seite mit Blockleiste ist bei 480 × 560 vollständig nutzbar (Leiste bricht in zwei Zeilen um).

**Grenzen/Aufwand:** Pinnwand und Pixel-Werkstatt bleiben im Kompaktmodus eingeschränkt nutzbar (Fläche zu klein) und öffnen auf Wunsch den Normalmodus. Aufwand M–L (Zustand, Kopfvariante, Größenstufen, Tests je Ansicht), Risiko mittel. **Empfehlung:** Kompaktmodus als eigenes Folgepaket statt allgemeiner Verkleinerung.

### 17.2 A02 – Zwei Inhalte gleichzeitig

**Befund (Code):** `ListApp` führt genau einen Ansichtszustand (`view_mode`, aktive Liste, ein Baum `self.tree`, ein Seiteneditor, eine Pinnwand). Alle Mutationen laufen über `item_change`/`sidebar_change`, Undo ist ein gemeinsamer Stapel, die Speichersperre gilt je Prozess. Funktionen leben nach den Produktgrenzen „eingebettet in der Ansicht, nicht in Zusatzfenstern“.

| Option | Beschreibung | Nutzen | Aufwand/Risiko | Konflikt |
|---|---|---|---|---|
| A | Zweites Fenster derselben Sitzung mit gemeinsamem Datenmodell | zwei Bildschirme, freie Anordnung | L+: Ansichtsschicht muss mehrfach instanziierbar werden (Baum, Editor, Fokus, Undo-Ziel, Schließen eines Fensters); hohes Regressionsrisiko | widerspricht „keine Zusatzfenster“ |
| B | Geteilte Inhaltsfläche in einem Fenster (verschiebbarer Trenner wie im Inspektor, S09) | zwei Listen/Seiten nebeneinander, ein Fenster | L: dieselbe Mehrfachinstanz der Inhaltsansicht, aber ein Fenster, ein Fokus-/Undo-Rahmen | passt zu „eingebettet“ |
| C | Nebenansicht im vorhandenen Inspektorbereich: zweiter Inhalt lesend mit direkten Aktionen (abhaken, öffnen), bearbeitet wird im Hauptbereich | Nachschlagen und Abhaken nebenbei | M: baut auf Inspektor und Live-Liste auf; geringes Risiko | passt; deckt WA-11 (Seitenvorschau) mit ab |
| D | Zweite unabhängige App-Instanz | – | ausgeschlossen: zweiter schreibender Prozess auf derselben Ablage | Speichersperre |

**Abnahmekriterien für B/C:** gemeinsamer Bestand, sofortige Aktualisierung in beiden Bereichen, stabile IDs, getrennte Auswahl/Scrolllage, keine verlorenen Eingaben beim Wechsel, ein Undo-Stapel mit Zielhinweis, eindeutiger Fokus, Schließen eines Bereichs ohne Datenverlust, Speichersperre unverändert. **Empfehlung:** C als erste Stufe (geringes Risiko, deckt Nachschlagen/Abhaken), B als spätere Ausbaustufe nach Erfahrung; A und D nicht.

### 17.3 Entscheidungsvorlagen für den Inhaber

A01–A03 sind Untersuchungsaufträge, keine Umsetzungsentscheidungen. Die vollständig ausgearbeiteten, knapp beantwortbaren Vorlagen **E-U1–E-U3 stehen allein in §20**; keine zweite Auswahlkopie. Neue Auswahl wird erst nach tatsächlicher Antwort als D52+ in der Arbeitsrichtung erfasst.

Originalbilder sind unverändert und lokal vom Git-Upload ausgeschlossen; für einen anderen Dienst das Paket einschließlich `bilder/` mitgeben. Anforderungsdetails und Abnahmekriterien nur im Prompt pflegen, Gestaltungsvorgaben nur in Design Richtlinien, Ergebnisse im QA-Bericht. Die Dokumentationsprüfung der Vorbereitungsrunde steht im [Vorbereitungsnachweis](../01_Repository/Glide/tests/qa-3.42.0/ui_ux_prompt_2026-10-15/README.md).

## 18. Konsolidiertes Funktions- und Aufgabeninventar

**Abschließender Remote-Abgleich 18.10.2026:** Lauf 39075284901 am unveränderten Upstream 9ec474b ist inzwischen erfolgreich: Grundstufe, Linux-/Windows-Vollprüfung mit eigener Tk 9.1 und Windows-Paketjob. Spezielle Orca-/NVDA-Läufe sind ausgelassen; Mac-/Menschenabnahmen und die lokale 07-/Paketlieferung des FP-01-Kandidaten bleiben offen. Der frühere laufende Snapshot bleibt historisch erhalten; [Abschluss-Snapshot](../01_Repository/Glide/tests/qa-3.43.1/standanalyse_2026-10-18/remote_abschluss.json).



### 18.1 Statusachsen, Quellen und Abdeckung

**A – Verbindlichkeit:** `Auftrag` = direkter Nutzerauftrag; `Entscheidung` = ausdrücklich bestätigte D-/Q-Festlegung; `Auslegung D49` = dokumentierte Interpretation mit Korrekturvorbehalt; `Vorschlag` = zur Auswahl oder technischen Planung vorgelegt; `zurückgestellt` = erst bei Auslöser; `ausgeschlossen` = geltende Produktgrenze. Die Analyse beauftragt das Untersuchen sämtlicher Zeilen, nicht deren Umsetzung.

**B – Bearbeitung:** je Zeile separat **I** Implementierung · **P** tatsächlich ausgeführte Prüfung · **L** Lieferung · **M** menschliche/native Abnahme. „P historisch“ bezieht sich auf die benannte damalige Version; der heutige Quellstand erbt daraus keine frische Vollprüfung. Die [aktuelle QA-Matrix](../01_Repository/Glide/docs/07_QA_BERICHT.md) führt die tatsächlichen Läufe, Plattformen, Hashes und Lücken. **L Python** umfasst die bereitgestellte Python-Fassung; **L Paket** verlangt einen eigenständigen Paketbeleg und darf daraus nicht abgeleitet werden. Ein beobachteter oder injizierter Fehler hat seinen Wirkungsnachweis; seine Häufigkeit im Alltag bleibt ohne entsprechende Messung unbekannt.

Die Inventargruppen unten bilden alle vorhandenen Funktionskennungen ab. Unterzeilen behalten ihre IDs und den konkreten ursprünglichen Umfang in §§3–7, §14, §15.1, §16 und §17. Das ist eine Zuordnung innerhalb dieses einen Backlogs. Befunde A01–A36 sind Diagnosekennungen der [Analyse](Glide_Analyse.md); sie erzeugen keine zusätzlichen Aufgaben neben den hier genannten Ziel-IDs. Die bisherige pauschale Aussage „N01–N20/G01–G32 stehen im Plan“ wurde durch Rekonstruktion der fehlenden historischen Kennungen präzisiert.

| Bereich | Untersuchungsstand | Ergebnis / Grenze | Zuständiger Ort |
|---|---|---|---|
| Vorhandene G01–G32, N01–N20, U01–U24 | untersucht | ursprüngliche Bedeutung, spätere Begrenzung und heute offener Rest zugeordnet; historische IDs aus Git rekonstruiert | §18.2/§18.4, §§3–7 |
| P01–P09/T2/E01/CI und A–H | untersucht | Messbeleg von Ziel/Annahme getrennt; neue Schutzprobleme vor Erweiterungen | §3/§10/§18.3 |
| S26-01–S26-22 einschließlich 14b | untersucht | acht Pakete plus durchgehende P05/I6-Prüfaufgaben; P8 bleibt unvollendet | §15.1/§15.7/§19 |
| WA-01–WA-18 / FP-00–FP-07 | untersucht | FP-00 geliefert, FP-01 upstream Kandidat, übrige Entwürfe; D49 als Auslegung gekennzeichnet | §16/§19 |
| UI A01–A03 / B01–B22 | untersucht | Analyse-/Auswahlaufgaben von Code-/Prüf-/Lieferabschluss getrennt; vollständige Bildabnahme nicht neu behauptet | §17/§19/§20 |
| Kleine Restarbeiten W01–W15, B1/B4/B7, AB/DOK, I1–I11 | untersucht | Reproduktion, Beobachtung, erledigter Werkzeugstand und Inhaberentscheidung getrennt | §18.3/§20 |
| Neue Befunde A31–A36 | untersucht | Risiko und reproduzierte Schutzfehler; technische Ableitungen WA-26–WA-30, A33 im FP-01-Abschluss. Gegenprüfung 18.10.: A36 Datensperre neu; am Upstream-Stand `9ec474b` ist A33 behoben, A32/A34/A35/A27 unverändert | §18.3, Analyse §9/§11.4 |
| Vollständige native Reader-/DPI-/Menschenabnahme | durch fehlende Ausführung blockiert | mit Attribut-/GUI-Verträgen nicht nachgewiesen; konkrete Plattform-/Bedienproben fehlen | I6/N12, QA/Prüfliste |
| Künftige Produktwahl A01–A03 | zur Entscheidung vorbereitet | Untersuchungsauftrag erfüllt; keine Wahl des Inhabers erfunden | §20 E-U1–E-U3 |

### 18.2 Bestehende Funktionen und ihre Restumfänge

Für alle gelieferten Bestandsgruppen bleibt **M offen gemäß I6**, soweit der QA-Bericht keine konkrete menschliche Freigabe nennt. Der frühere Designentscheid D45 ist eine Freigabe des Logoentwurfs, keine appweite DPI-/Bedienabnahme. Funktionsvertrag, Tests und Modulnamen sind die jeweils primären Belege; diese Tabelle verdoppelt den Vertrag nicht.

| Vorhandene IDs / Nutzerbedarf | Herkunft A und präziser Umfang | B: I / P / L / M | Module, offene Arbeit, Abhängigkeit und Paket |
|---|---|---|---|
| **G01=B-01**, U04/KO03/KO05: Gedanken schnell und nachvollziehbar erfassen | Entscheidung D01/D10, Auftrag Alltag; deutsche Chips für Bearbeitungstag, Fälligkeit, Aufwand, Labels, Wiederholung; keine unsichtbare Teildeutung | I vorhanden; P `test_eingabe3333`, `test_komfort33320`, `test_wiederholung3391` historisch; L Python bis 3.43.1; M offen | `capture_parser.py`, App-Eingabe; Parserkorrektur FP-00 geliefert, erweiterte Grammatik FP-02, lange/mehrzeilige Eingaben bleiben Regression |
| **G02**, U06/U19, AU01–AU07, KO01/KO02/KO06: realistisch planen | D02/D13/D14/D20/D30/D38; Eisenhower, Heute/Demnächst, Einplanen, Zeitbilanz, Vorschlag, Rituale/Routinen, Erinnern und Entlasten | I vorhanden; P Planen/Tages-/Wochensuiten historisch, Linux-Kürzelfix 3.43.1; L Python 3.43.1, historisch Paket 3.42.0; M offen | `planning.py`, `day_proposal.py`, `week_planning.py`, `routines.py`, `daily_hints.py`, `ics_busy.py`/`ics_recurrence.py`; neue Regeln FP-02, optionaler Grund WA-12; Fälligkeit bleibt immer eigener Vertrag |
| **G03/G04**, B-03=N04=U11/AU04: Tagesabschluss und Stundenraster | G03 schon 3.32.0; G04 als Bestandsfunktion bestätigt, durch eingebettete Woche weitergeführt; historische Fassung begründet kein zweites Raster | I vorhanden; P Tages-/Wochen-/Tagesplanungssuiten historisch; L Bestand; M offen | App-Zeitraster und `week_planning.py`; kein neues Paket für schon vorhandene Zeitleiste; Überplanung über V01/S26-18 |
| **G05=B-02=AU05**, H-02/H-02r: fokussieren und ohne Ziehen arbeiten | D02; Timer auf vorhandener Zeitbuchung, genau einmal; Tastaturwege für Blöcke/Pinnwand/Bereichsbäume | I vorhanden; P `test_tag33314`, `test_wissen3340` historisch; L Bestand; M Tastatur/Reader offen | App-Fokusbuchung/Strukturwege, `interaction_policy.py`; P8 prüft zugänglichen Kernablauf, WA-08 erst bei Zeitnachweisbedarf; H-02r-Zielhinweis erst nach Aktion ist benannte Abweichung, keine neue Auswahlpflicht |
| **G29=C-01/G31=C-02/G32=C-03**, G08/G30=D-02: Aufgaben und Wissen verbunden halten | D05/Q5, Format 21/22; ein Heimatobjekt und echte IDs, Verschieben lässt Verweis, Rückverweise/Filter aus Seiten | I vorhanden; P Wissen-/Wochensuiten historisch; L Bestand; M offen | `task_references.py`, `object_references.py`, Page-/Note-Editor; FP-05 ergänzt unverbundene Erwähnungen; WA-28/WA-29 schützen Laden/Flush, P8 deckt nur Aufgabeninspektor und Kernablauf |
| **G28=E-01/G09=E-02/U08=E-03**, U18/B4: Wissen lesen und weiterverwenden | Format 23; Live-Liste mit Originalen, lokale Titelbilder, Vorlagenvorschau, Seitentitel, Bilder und Markdown-Rückweg | I vorhanden; P `test_seiten33318`, `test_wissen3340` historisch; L Bestand; M lange/enge Inhalte offen | `page_features.py`, `page_markdown.py`, Editoren, Bildkonversion; FP-04 verknüpft Seitenkarten, FP-07 gesamter lesbarer Export, A03 bestehende Funktionen ruhiger zugänglich machen |
| **G11**: Tagesnotizen ohne wiederholtes Tippen | historischer Auftrag 30.09.; Platzhalter `{{Datum}}`/`{{Wochentag}}`/`{{KW}}`, später Vorlagenvorschau | I vorhanden; P Ausbau-/Vorlagenprüfungen historisch; L 3.32.0 und Bestand; M offen | App-Vorlagen/`template_helpers.py`; WA-14 ist automatische Wiederholung einer Vorlage und damit eigener zurückgestellter Umfang, nicht fehlender Platzhalter |
| **G14=D-01/G14h**, U01=N03/U03/U07=N02, D-03: Inhalte finden und Wege verstehen | D17, Produktprinzipien; Inhaltssuche, gemeinsame Palette, hervorgehobene Treffer, Eingang und Filtererklärung; FTS5 nur nach belegter Notwendigkeit | I vorhanden; P Suche/Wissen historisch; L Bestand; M offen | `content_search.py`, `action_catalog.py`, `filter_explain.py`; FP-03 neue Bedingungen/Darstellung; WA-15 erst Rangfolgeproblem; P07 ist bewusst nicht umgesetzt nach Messung, keine offene Suchindexlieferung |
| **N05=U12**, KO04, OB02/OB03/OB04: Aufgaben verständlich bearbeiten | ausdrücklich D22–D25/D31/D32; ein Aufgabeneditor, direkte Felder, vier Textstufen, bedarfsabhängige Aktionen und begrenzte Übergänge | I vorhanden; P `test_aufgaben3380` und damalige Mac/Linux/Windows-Matrix; L 3.38.0 im Bestand; M DPI/Design offen | App-Inspektor, `ui_design.py`, Inspektor in `app.pyw`/Interaktionsadapter; B13 präzisiert nächste Aufgabe; A02 darf keinen zweiten unkoordinierten Editorkontext schaffen |
| **U02/U05/U09/U10/U13/U14/U15/U16/U17=N01/U20/U21=N07/U22/U24**, OB01/OB05/OB06 | bestätigte UX1-/Alltagsaufträge; ruhige Kopfzeile/Bibliothek/Begriffe, Systemdesign, bedarfsgerechte Hinweise, schmale Leiste | I weitgehend vorhanden; P Komfort/Oberfläche/UIUX historisch; L Bestand; M OB06 weiterhin offen | `appearance.py`, `ui_design.py`, `home_tiles.py`, `release_notes.py`; OB01 weitere direkte Werte nur bei angefassten Ansichten, keine neue Gesamterneuerung; UI-B06/B04/B13 ersetzen ältere Detailvorgaben |
| **G16/G20/G19=G-01/G-03**: eigene Pixelwerke und Paletten nutzen | Auftrag 30.09./Sprint 08.10.; ICO/Favicon, Aseprite-/Adobe-Paletten, indizierte Umfärbung mit Vorschau/Undo, Symbolvorschau | I vorhanden; P Ausbau-/Pixel-/Exportsuiten historisch; L 3.32.0/3.35.0 und Bestand; M Nischeneignung/Sicht offen | `drawing.py`, `drawing_import.py`, `drawing_palette.py`; WA-26 betrifft Bildvorschauen, kein Auftrag für Ebenen/Transparenz/Allzweckgrafik |
| **G17=G-02=S26-08**: kleine lokale Animation | ausdrücklich D18 statt alter unverbindlicher GIF-/Zwiebelhautideen; Frames, Dauer, Vorschau, PNG-Spritesheet und Einzelbilder | I vorhanden; P `test_animation3400` + Migration historisch; L 3.40.0, Schema 24; M offen | `drawing_animation.py`, `drawing.py`; GIF/Zwiebelhaut sind kein stiller Rest des gewählten D18-Rahmens; G18 erst bei Kachelsatzbedarf |
| **G24=F-01**, F-03, G21=F-02/V02/N13 | D26/D37/D39 und Q3; KI-Dateien mit geprüftem Diff, Sicherungsvergleich, begrenzter Notion-Import mit Konfliktwiedererkennung, einzelne Seite wiederherstellen | I vorhanden; P Austausch-/Import-/Restoreprüfungen historisch; L 3.35.0/3.41.0, Schema 25; M reale Import-/Restoreabläufe offen | `exchange_patch.py`, `backup_diff.py`, `notion_import.py`, `notion_reimport.py`, `page_restore.py`; FP-06/07 für Bedienung/Ausstieg; frühere zweite Quelle Todoist ist nach D26 nicht mitbeauftragt |
| **G26=H-03=N11=S26-10**, H-01/CI/T2: sichere Weitergabe und Regressionskontrolle | D15/D27/D35/D42; eigene Laufzeit für Mac arm64/Windows x64, native Vollmatrix, Formatsicherung und echte Bindungstests | I Bau-/Prüfwege vorhanden; P historische Lieferbelege 3.42.0 und spätere CI getrennt; L Python/Paketstände in QA; M Veröffentlichung offen | `packaging/`, `schema_backups.py`, `tests/tools`; P8 mit eigener Tk 9.1 noch kein Lieferabschluss, Linux-App nicht gewählt; I1–I5/I9–I11 bleiben eigene Tore |
| **LG01–LG04/S26-11/S26-12/S26-22**, A14/I8 | D28/D29/D41/D45; technische Tk-8.6-Glättung, vorgefertigte Größen und freigegebener Master | I vorhanden; P Logo-/Glyphentests historisch; L 3.37.0; M appweite native Sicht/DPI offen | `logo.py`, `glyph_metrics.py`, Grafik-Master; B05/B09/B10 präzisieren Darstellung, kein neuer Logoentscheid |
| **P01/P01r–P09** einschließlich P03r/P04=A-02/P06r=A-03/P08c, **E01/T2/G27** | Performanceauftrag, D16/D17/D33/D34/D40/D46–48; Messungen, gezielter Aufbau, gemeinsame Fachlogik statt Großumbau | I ausgewählte Optimierungen vorhanden; P Messungen jeweils datiert; L bis 3.36.0/Bestand; M aktuelles Referenzgerät nicht neu geprüft | §3/§10; neue Risiken WA-26–WA-29; P05 bleibt kontinuierlicher begrenzter Auftrag, G27 wird durch D17 schrittweise erfüllt und nicht als pauschal abgeschlossen geführt |

**Historische Quellrekonstruktion:** G03/G04/G11/G16/G20/G27 und die genaue N15–N20-Aufteilung aus [Funktionsrecherche vor Konsolidierung](https://github.com/n05a-design/glide-to-do/blob/3e943ab%5E/00_Arbeitsvorbereitung/Glide_Funktionsrecherche_Ausbau_2026-09-30.md) bzw. [Featurematrix vor Konsolidierung](https://github.com/n05a-design/glide-to-do/blob/3e943ab%5E/00_Arbeitsvorbereitung/Glide_Konkurrenz_und_Featurematrix_2026-10-01.md), im lokalen Git lesend geprüft. Die späteren Entscheidungen haben Vorrang; alte Versionserwartungen/Dateiverweise werden nicht reaktiviert.

### 18.3 Offene Aufgaben, Schutzmaßnahmen und kleine Reste

| ID / Bedarf | A | B: I / P / L / M | Rest, Module und Abhängigkeit | Zielpaket / Entscheidung |
|---|---|---|---|---|
| **N12=U23=S26-16** Aufgaben ohne visuelle Navigation bedienen | ausdrücklich D36/D44; D50 ändert Folge | I additive Vorbereitung im lokalen Quellbaum, P gezielte Semantik-/Runtime-/GUI-Verträge; L keine 4.0; M vollständige VoiceOver/NVDA/Orca-Abläufe offen | aktuellen 3.43.x-UI-Stand mit Vorbereitung abgleichen; Orca-Absturzkorrektur nativ nachweisen, Fokus/Abschnittsauswahl, beide Pakete, finale Vollmatrix; Attributprobe genügt nicht | P8 zuerst gesichert abschließen; bestehender Rahmen gewählt, keine neue Stufenfrage |
| **FP-01/WA-01** Fehlbedienung wiederholen | D49-Auslegung; upstream Start 17.10. im dortigen Nachweis | I upstream Stufen 1+2, lokal fehlt; P 9/9 und 12 Units, kein kompletter Endabschluss; L offen; M offen | A33 dort mitbehoben; am 18.10. durch Ausführung der Fehlerprobe gegen `9ec474b` bestätigt (Schritt bleibt, Arbeitsspeicher zurück, keine Erfolgsmeldung). Lieferabgleich muss genau diesen Pfad und Schreibfehler prüfen; der grüne GitHub-Lauf 39075284901 ersetzt keine lokale Lieferung | vorhandenen Kandidaten prüfen/abschließen, nicht erneut implementieren; Integration erst mit Umsetzungsauftrag |
| **WA-26 / A31**, P04/P05: UI bei Bildvorschauen bedienbar halten | technischer Vorschlag aus Codeanalyse 18.10. | I Korrektur nicht begonnen; P synchroner Aufrufpfad belegt; L nein; M nein | `PreviewCache.convert` ruft `subprocess.run(timeout=45)` aus Tk-after/Renderwegen; begründetes Blockierungsrisiko, kein gemessener normaler Engpass. Titelbild-Thread als vorhandene Lösung vergleichen. Begrenzter Worker, Host/Generation, Abbruch und Fehlversuchszustand | Schutz-/Reaktionsrunde nach Datenkorrekturen; kein Format/keine neue Abhängigkeit |
| **WA-27 / A32** Bestandswächter auch bei 20 Undo-Schritten | Prüfkandidat umgesetzt | I integriert; P gezielte Fehlerfälle grün; L noch nicht nach 07 geliefert; M native Abnahme offen | `structural_guard.py` sichert den Vorzustand unabhängig von der Stapeltiefe; fehlende IDs werden vor dem Schreiben erkannt. Später Abbruch stellt Originalbytes wieder her; Speicherfehler führen zu einer zutreffenden Fehlermeldung. | Voller Stapel, Savefehler, bytegleiche Datei nach Abbruch und Undo/Redo geprüft; [Schutznachweis](../01_Repository/Glide/tests/qa-3.43.1/schutzrunde_2026-10-18/README.md). |
| **WA-28 / A34** gültige Datei bei Darstellungsfehler behalten | Prüfkandidat umgesetzt | I integriert; P gezielte Fehlerfälle grün; L noch nicht nach 07 geliefert; M native Abnahme offen | `load_phases.py` trennt Lesen/Normalisierung vom UI-Aufbau. Ein Darstellungsfehler klassifiziert gültiges JSON nicht als beschädigte Datei; Schreibschutz und Bestand bleiben geschützt. | Gültige Datei mit UI-Fehler, ungültiges JSON und zukünftiges Format geprüft; [Schutznachweis](../01_Repository/Glide/tests/qa-3.43.1/schutzrunde_2026-10-18/README.md). |
| **WA-29 / A35** vor Kontextwechsel zuverlässig speichern | Prüfkandidat umgesetzt | I integriert; P echte Aufrufer und Fehlerfälle grün; L noch nicht nach 07 geliefert; M native Abnahme offen | `editor_flush.py` vereinheitlicht den True/False-Vertrag. Kontextwechsel und Ausgaben warten auf tatsächliche Übernahme; ein Dirty-Kennzeichen allein reicht nicht. Unveränderte übernommene Inhalte bleiben schreibgeschützt exportierbar. | Navigation, Anlegen, Ausgabe, Notion/Restore und beide Editoren geprüft; [Schutznachweis](../01_Repository/Glide/tests/qa-3.43.1/schutzrunde_2026-10-18/README.md). |
| **WA-30 / A36** Datensperre ohne Fail-open | Prüfkandidat umgesetzt | I integriert; P L1/L2/L3/L4/L5 und Prozessproben grün; L noch nicht nach 07 geliefert; M Cloud-Abgleich offen | `data_lock.py` nutzt exklusive Anlage und einen lokalen OS-Mutex für Übernahmen alter Sperren. Beschädigte Sperren bleiben schreibgeschützt bis zur bewussten Übernahme; alle Schreibwege einschließlich Einstellungen und Beenden verwenden die gemeinsame Schranke. Kein verteiltes Cloud-Lock. | Fehlende/verdrängte Sperre, Einstellungen, Beenden und sechs synchronisierte Prozesspaare geprüft; [Schutznachweis](../01_Repository/Glide/tests/qa-3.43.1/schutzrunde_2026-10-18/README.md). |
| **WA-09 / A27** Zukunftsfelder nicht still kürzen | D49-Auslegung, technische Voraussetzung FP-04 | I bisher nur oberste Ebene tolerant; P Vorprobe 13.10.; L Schutz fehlt | WA-09 schützt neue Leser, ändert alte ausgelieferte Normalisierer nicht. Neue Seitenkartendaten brauchen neuen obersten Namespace oder echtes Einstellungs-Schreibschutztor; siehe §19 | vor FP-04, kein Pseudobeleg „ältere Fassung mit WA-09“ ohne Mindestversion; AE-4 präzisiert |
| **FP-02/WA-02/A26** Sonderrhythmen verlässlich | D49-Auslegung A/V | I nicht begonnen; P historische Referenzprobe mit 11192 Kombinationen am ICS-Rechner; L nein | alte sechs Regeln exakt behalten, neue Regeln in eindeutiger Fassade, Formattor; Fehler des alten Parsers bereits FP-00, kein offener Doppelauftrag | nach Schutz/FP-01; voller Schnitt wirtschaftlicher als zwei Migrationen |
| **FP-03/WA-03** wiederkehrende Sicht einmal speichern | D49-Auslegung A/V | I vorbereitet; P nur bestehende Filter, neuer Umfang ungeprüft; L nein | feste Felder, Bedingungen+Darstellung+Erklärung, eigener Namespace; ältere Fassung zeigt sonst mehr Treffer, ohne Datenschutzproblem aber mit Planungsrisiko | nach Bedienentwurf; keine freien Felder; E-U3 ergänzt Wege statt neuen Filterbaukasten |
| **FP-04/WA-04, FP-05/WA-05** Projektkontext verbinden | D49-Auslegung vollständig | I vorbereitet; P neue Umfänge ungeprüft; L nein | Seitenkarten brauchen WA-09/altlesersichere Ablage; Erwähnungen Titelkollisionen/Umbenennung/keine Selbstverweise; bestehende Objekte und Verweiswege verwenden | zwei unabhängige Teile, zusammen nur nach belegtem gemeinsamen Nutzen; §19 |
| **FP-06/WA-06, FP-07/WA-07** KI-Ergebnisse kontrollieren/Ausstieg | D49-Auslegung FP-06 voll/FP-07 erste Stufe | I vorbereitet; P bestehende Exchangewege, keine Musterantwort; neue Funktion; L nein | `instructions` vorhanden, Erstellen/Patch getrennt; Gesamtausgabe Inventar/Manifest/relative Links/Anhänge und Verlustbericht; kein Wiederimportversprechen | gemeinsame Dateidialoge, separate Prüfbelege; Canvas als zweite Stufe von FP-07 bleibt optional |
| **WA-12** Vorschlag gibt andere frei; **WA-16** Wartbarkeitsverlauf | Vorschlag, keine klare Einzelwahl | I nicht begonnen; P keine; L nein | WA-12 nur zusätzlicher deterministischer Grund ohne Aufgabenautomatik; WA-16 Zählung zur Orientierung, keine Qualitätszahl | technisch unabhängig S; keine Produktentscheidung nötig bis Umsetzungsumfang gewählt |
| **W01/W06** Windows-Titel/fehlende Dialogbeschriftung | beauftragte Nachprüfung, Produktionsbedarf unbestätigt | I unbekannt; P alte Aufnahme, keine frische Reproduktion; L kein behaupteter Fix; M offen | Schrift/DPI/Mapzeitpunkt mit künstlichem Datensatz prüfen; erst bestätigten Produktionsfehler korrigieren, sonst Testaufnahme anpassen | I6/B1/B1a-Prüfsitzung, keine pauschale P0-Einstufung |
| **W07/W08/W09/N08** Doppelhinweis/Pixelraster/Absturz/Linux-Bilder | Nachprüfung/Beobachtung | W07/08 Mac nicht nachstellbar; W09 0/30 Wiederholungen; N08 implementiert, native Sicht offen | Windows-DPI/Originalablauf, Linux-Systemkonverter; W09 nur mit neuem Crashbeleg an CPython, keine unbelegte Ursachenkorrektur | I6; konkrete auslösende Umgebung nennen |
| **W02–W05/W10–W15, DOK2/DOK3, AB03–AB08** Prüf-/Ablagekonsistenz | frühere Aufträge; historische Einzelkorrekturen | I damals erledigt; P Werkzeug-/Bestandsprüfungen jeweiliger Runde; L keine App-Funktion je Zeile; M W05 Sicht offen | Zeilenenden, Wächter, Dialogbreite, Retention, Kommentare, Liefer-README, Altleser, Sperrzeit; AB06 Kommentar/AB08 Mindestversion. Historische AB01/AB02 nicht als neue offene Anforderung erfinden | laufende Pflege; aktuelle Werkzeugänderungen upstream separat, lokale Routineprüfung QA |
| **B01–B20**, **B21/B22** UI-/UX-Abschluss | direkter Auftrag 15.10./D50 | I B01–20 lokal vorhanden, B21 Dokumentation; P Suite 17/17 historisch Windows, spätere CI im QA; L Python 3.43.1, vollständiger Mac-/Paketabschluss fehlt; M offen | §17 Einzelmatrix; B22 ist Liefer-/Pflegeabschluss, keine vollständige Freigabe. E-U1–3 Auswahl getrennt; 23 bzw. 25 IDs bleiben nachweisbar | Abschluss bestehender Lieferung, keine erneute Umsetzung aller B-Punkte |

### 18.4 Zurückstellungen und bewusste Ausschlüsse

**Zusätzliche bereits vorhandene Planung vom 17.10.2026:** Bei der Prüfung anderer lokaler Git-Stände wurde `claude/ausbauprogramm-phasen` (`19c7df5`, Planungsinhalt ursprünglich `7527e87`) gefunden. Dessen §18 war in der untersuchten Wurzel nicht enthalten. Die folgenden IDs bleiben unverändert erhalten. Der direkte Auftrag zu größeren Paketen und phasenweiser Prüfung ist als **D51** belegt; **E-P1–E-P5 und die neuen Funktionsumfänge sind dort Vorschläge, keine ausgewählten Entscheidungen**. Herkunft: [festgeschriebener Phasenplan](https://github.com/n05a-design/glide-to-do/blob/19c7df5/00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#18-ausbauprogramm-in-phasen-vorschlag-17102026). Die Einordnung hier übernimmt gültige Inhalte als Dokumentation, keinen Code und keinen Git-Merge.

| Bereits vergebene ID | Bedarf / ursprünglicher Vorschlag | A / B heute | Vertiefter Rest, Modul, Abhängigkeit und Ziel |
|---|---|---|---|
| **WA-19** | weitere Importquellen Todoist-/TickTick-CSV, Markdown-/Obsidian-Ordner | Vorschlag E-P3; vorbereitet, nicht implementiert/geprüft/geliefert | zuerst Exportvarianten/IDs/Datumssemantik/Anhänge/Verweisauflösung mit echten künstlichen Fixtures spezifizieren; Quellenmetadaten aus `notion_reimport.py` sind kein allgemeiner Importvertrag. FP-07-Ausgabe ist nicht automatisch verlustfrei rückimportierbar. Phase 4, je Quelle klar begrenzen |
| **WA-20** | Wochenbeginn/-abschluss, bis zu drei Ziele und Kapazitätsbilanz | Vorschlag E-P3; Entwurf, nicht implementiert/geprüft/geliefert | vorhandenen Wochenrückblick erweitern; Ziele entweder referenzierte Aufgaben oder Notizbuchinhalt, keine zweite Aufgabe. `week_planning.py`, `planning.py`, `daily_hints.py`; Zielpersistenz/Löschverhalten vor Umsetzung festlegen. Phase 4, optional neben Dateiaustausch |
| **WA-21** | Fundorte einer Aufgabe im Inspektor zeigen | Vorschlag E-P3; nicht implementiert/geprüft/geliefert | Heimatliste/-seite von Live-Listen/Verweisen/Pinnwandvorkommen unterscheiden; aus stabilen IDs ableiten, keine persistente Fundortkopie; `object_references.py`, Inspektor in `app.pyw`, App-Pinnwände. Phase 3, passend zu FP-04/05; ein eingeklappter Bereich |
| **WA-22** | Pinnwandlayout in Komplettbackup und Tagesständen erhalten | Vorschlag E-P3; nicht implementiert/geprüft/geliefert | Backupbegriff und Restorevertrag erweitern, vorhandene Archive weiter lesen; Quelldaten und Layout gemeinsam konsistent, Vorsicherung/Undo/fehlende Ziele. `backup_diff.py`, App-Backup/Restore. **Nicht pauschal ohne Datenwirkung:** Backupformat und Wiederherstellung verändern sich, Schutzschema explizit versionieren. Phase 4 nach Schutzrunde |
| **WA-23** | einen einzelnen Serientermin verschieben/auslassen | Vorschlag E-P3; nicht implementiert/geprüft/geliefert | reine Fortschreibung einer Aufgabe reicht für künftige Ausnahme nicht; Instanzidentität, Ausnahmedatum, Nachfolgetermin, Abhaken/Undo/ICS definieren. Eng mit FP-02, gemeinsames Formattor nur nach fertiger Modellprüfung. Phase 2, nicht als bereits genehmigter Teil von D49 behandeln |
| **WA-24** | erledigte Serientermine in Datumsansichten behalten | Vorschlag E-P3; nicht implementiert/geprüft/geliefert | ursprüngliche Annahme „nur Ableitung, kein Format“ **nicht belegt**: dauerhafte einzelne Vorkommen benötigen belastbare Abschluss-/Instanzdaten. Vorhandenen begrenzten Aktivitätsverlauf nicht zum dauerhaften Serienarchiv erklären. Mit WA-23/FP-02 Modell/Retention/Export klären, sonst nur vorhandene letzte Abschlüsse zeigen und Grenze nennen. Phase 2 |
| **WA-25** | relative Bearbeitungszeit für Seiten | Vorschlag E-P3 bzw. E-U3 B, nicht implementiert/geprüft/geliefert | Notion-Rang 4; aus vorhandenem Änderungsdatum berechnen, ohne jede Minute alle Seiten neu aufzubauen; exakte Zeit zugänglich. `page_features.py`, Seitenkopf; kein eigener Auftrag neben E-U3. Phase 1 optional |
| **TK9-RAD** | Rad-/Zoombindungen für Tk 9 vereinheitlichen | technischer Vorschlag, nicht implementiert/geprüft/geliefert | Tk 9 behandelt Button-4/5 anders, Tk 8 braucht den Linux-Weg; echte Rad-/Seitentasten getrennt nach Laufzeit prüfen, nicht einfach Bindungen löschen. `interaction_policy.py`, App-/Editor-Radadapter. Phase 1 bzw. WA-26 |
| **PS-01** | wackelige Windows-Prüfsuiten stabilisieren | Prüfauftrag 17.10.; upstream Werkzeugkorrektur teilweise vorhanden, lokal veraltet | `test_tag3390`/`test_template_workflows` upstream 17.10. korrigiert, `test_ui_followup36` und Features330-Zoom nur bei belegter Ursache. Gegenproben und Plattformstände erhalten. Phase 0, keine Produktkorrektur aus einem Fokus-/Dialogtest allein ableiten |
| **PS-02** | fremder Seiteninhalt oberhalb Showcase-Pinnwand | Untersuchungsauftrag 17.10.; Ursache offen, keine bestätigte Korrektur | künstliche isolierte Fixture; Hostwechsel/Widgetabbau/Ansichtsmodus prüfen, Datenreferenz gegen UI-Rest unterscheiden. App-Ansichtswechsel, `ItemWorkspace`; nur im Fehlerfall produktiv korrigieren, keine echten Showcase-Nutzerdaten ersetzen. Phase 0/Schutzrunde |

Die übrigen Auslöser bleiben erhalten:

| IDs | A / B | Nutzerbedarf und Auslöser | Planerische Behandlung |
|---|---|---|---|
| G06=N16, WA-08 | vorerst zurückgestellt, nicht begonnen | Routinen schon AU06; Statistik bzw. tageweise Zeiteinträge erst bei echtem Zeitnachweisbedarf | WA-08 Formattor/Protokoll; keine Bewertung des Menschen, keine voreilige Statistiklieferung |
| G10/G15/G18 | Vorrat, nicht begonnen | Registerkartenblock nur bei Nichtausreichen Gliederung; natürliche Filter erst nach FP-03-Bedarf; Kachelsatz nach konkretem Pixelworkflow | keine neue Ansicht/Parser-/Zeichnungsart ohne Bedarf; G17 ist allein kein Auslöser |
| WA-11 | zurückgestellt bzw. Teiloption A02 | Zielkontext nachlesen ohne den Hauptinhalt zu verlieren | lesende Vorschau in E-U2 A integriert, niemals doppeltes Paket; derzeit keine Implementierung |
| WA-14/WA-15, ZF-NOTES/ZF-LABEL | zurückgestellt, nicht begonnen | wiederkehrende Vorlagen nach FP-02; Suchrang erst bei Fehlreihung; datierte Aufgabennotizen/Labelbeschreibungen erst bei Bedarf | alte Vision, keine Ausführungsfreigabe; Lösch-/Exchange-/Migrationsregeln vor späterem Schnitt |
| P07, SQLite als Hauptspeicher | bedarfsgebunden nicht gewählt | Suche historisch unter 100 ms, D16-Neubewertung des Hauptspeichers erst über 20.000 echte Punkte | keine Index-/Datenbankmigration auf Verdacht; erst aktuelle Messung und Bedarf |
| G25/Mobile | zurückgestellt D03/Q4 | eigentliche Mobile Nutzung oder reproduzierbare Grenze gewählter Zugänglichkeit | keine Toolkitprobe als heimliche Lösung für einzelne Tk-Fehler |
| G07=N14, N09/N10, WA-10 | ausgeschlossen Q2/Q3/Produktgrenze | externe Erfassung, Zustellung beendet, MCP/KI-Endpunkt | zusätzliche Plattform-/Prozess-/Netzabhängigkeiten zurzeit nicht gewählt; E-W3 durch D49 mit Dateiaustausch ausgelegt |
| G12/G13=N19, N18=ZF-200, N17/G23, N15/N20, G22 | ausgeschlossen bzw. G22 keine Priorität | Seitenspalten/Graph/Unterseiten, freie Felder/Datenbanken, Team/Sync, Sprache/Web Clipper, Verschlüsselung | aktuelle Recherche liefert keinen Anlass zum erneuten Öffnen; vorhandene Rückverweise/Ordner/Export decken Teile ab |
| N06, freie Klebezettel/Freihand, Cloud-KI | ausgeschlossen | Einstieg/Rundgang besteht; bestehende Objektkarten; Q3 Dateien | keine weiteren impliziten Pakete aus Notion-Bildern ableiten |
| B1/B7 | B1 zurückgestellt, B7 Drittmeldung offen | ganze Seitenleiste scrollen erst bei konkreter Störung; Tk-Rahmenfehler umgangen | B7 braucht Tcl-Konto und expliziten Meldeauftrag; Kontoanlage/Versand gehören nicht in Analyse |

**Namensräume:** `A01` im alten Sprint §14 ist der Dokumentabgleich 08.10., `A01` im UI-Paket §17 ist Kompaktmodus, `A01` in der Analyse ist ein historischer Befund. Ebenso sind `B4`, `B04` und `B-03` verschieden. Alle Verweise nennen deshalb den fachlichen Abschnitt. Keine Kennung wird neu vergeben oder still umbenannt.

## 19. Paketgrenzen, Ausbaustufen und Aufwand

### 19.1 Prüfmaßstab für sämtliche vorhandenen Pakete

Die Prüfung umfasst die historischen Umsetzungspakete A–H/§14, die acht D44-Pakete, FP-00–FP-07, das UI-/UX-Paket und den gefundenen Phasenentwurf vom 17.10. Bereits gelieferte Inhalte werden nicht erneut als offenes Paket angeboten. Die Kennungen der ursprünglichen Pakete bleiben; die Phasen sind Lieferbündel dieser Aufgaben. Es werden keine neuen Versionsnummern oder Termine festgelegt.

| Dimension aus dem Analyseauftrag | Nachweis und verbindliche Ergänzung für die Paketplanung |
|---|---|
| 1 Ziel/Nutzerbedarf | §§18.2–18.4 und jeweilige FP-Karte §16; jede Phase braucht einen im Alltag abgeschlossenen Ablauf |
| 2 Auftrag/spätere Änderung | A-Status §18, D44→D49 Auslegung→D50 Vorrang→Abschluss 15.10.→D51 Prüfrhythmus; aktuelle Analyse startet keine Produktion |
| 3 Implementiert/geliefert | B-Status §18 und QA-Matrix; FP-01 upstream Kandidat und lokale Lieferung gesondert; P8-Bestand ist Vorbereitung |
| 4 Fehlender Umfang | Restspalten §18, konkrete Ausbaustufen §19.3; keine schon vorhandenen Raster/Verweise/Paletten nochmals bauen |
| 5 Konkurrenzumfang | [Markt](Glide_Markt_und_Vorbilder.md), mit Abruf/Belegstufe; Ableitung: Wiederholungssemantik, Findbarkeit, Kontext und Ausstieg statt Zahl sichtbarer Funktionen |
| 6 Sonderfälle/Alltag | je Paket Fehler/Abbruch/Undo/Redo/Neustart, Bestand leer/groß, lange Titel, fehlende Ziele; zusätzliche Spezialfälle unten |
| 7 Oberfläche/Wege | bestehender Ort, Maus/Tastatur/Palette, Fokus und Reader; Hover allein ist kein Zugang; B15 appweiter Buttonschutz |
| 8 Fachlogik/Daten | D17-Tk-freie Planung, UI-Adapter, stabile IDs, `item_change`/`sidebar_change`; Format- und Einstellungsablage ausdrücklich unterscheiden |
| 9 Migration/Rückweg | echte Vorversion plus neue Dateien prüfen; WA-09 allein kann bereits ausgelieferte alte Leser nicht reparieren; kein stiller Verlust/kein falsches Rückimportversprechen |
| 10 Abhängigkeiten | §19.4; Schutz vor zusätzlichen Mutationen, FP-01 vor neuen Mutationen empfohlen, WA-09/Namespace vor FP-04, Modellvorprüfung vor FP-02/WA-23/24 |
| 11 Prüfung/Abnahme | D51 gezielte Prüfungen je Teilpaket, ein eingefrorener Endlauf je zusammenhängender Phase; D35/D42-Plattform-/Menschen-/Reader-Tore bleiben |
| 12 Aufwand/Unsicherheit/Risiko | Bandbreiten §19.3/4; Entwicklungsaufwand einschließlich gezielter Tests, gemeinsame Endprüfung extra, native Reader-/Kontowartezeit nicht schätzbar |
| 13 Produktentscheidungen | ausschließlich §20; technische Details innerhalb bestehender Grenzen selbst lösen, bestätigte D01–D51 nicht neu öffnen |
| 14 Paketgrenze | zusammenfassen bei gemeinsamer Fachlogik und eigenem Nutzennachweis; trennen bei unabhängigem Datenformat/Reader-/Dateisystemrisiko. Keine Großphase allein zur Verringerung der Zahl der Vollläufe |

**Schätzgrundlage:** ein Entwickler mit vorhandener Codekenntnis, funktionierende künstliche Fixtures und verfügbare lokale Laufzeit. `S` ungefähr 0,5–2 Arbeitstage, `M` ungefähr 2–5, `L` ungefähr 5–10; größere Spannen ausdrücklich genannt. Das ersetzt die früher uneinheitlichen S/M/L-Zahlen für neue Planung, nicht historische Zusagen. Bandbreiten sind Schätzungen, keine empirische Arbeitszeitmessung und keine Veröffentlichungstermine. Gemeinsame Prüfung/Lieferung typischerweise zusätzlich 2–5 Tage je breiter Phase; Paketstarts, echte Reader und Fehlerbefunde können die Spanne erweitern.

### 19.2 Bestehende Pakete: Abschluss und Zuschnitt

| Paket / ausgewählte IDs | Beibehaltener Nutzen und heutiger Umfang | Rest / 14-Dimensionen-Folge / angemessene Grenze |
|---|---|---|
| A–H / Sprint 3.33.19–3.35.0 | Tempo, Komfort, ruhigere Oberfläche, Wissen, Pixel und Austausch im damaligen Umfang umgesetzt; Karten nach Lieferung aus Git nachvollziehbar | kein neuer offener Komplettsprint. H-02r-Zielhinweis nach Aktion und D-03 nur gespeicherte Filter sind dokumentierte Grenzen; neue Befunde in WA-26–29 statt Wiederöffnung aller alten Karten |
| D44 Paket 1 Fundament, Paket 2 Logo | technische Grundlagen und damalige Mess-/Lieferbelege vorhanden | D46/D48-Grenzen bleiben. Keine neue Logoentscheidung, kein Index ohne Latenzbeleg. Native Sicht-/DPI und Referenzmessung nur für tatsächlich geänderte Wege; PS-01 ist Werkzeugpflege |
| D44 Paket 3 Aufgabenoberfläche | gemeinsamer Inspektor/direkte Felder, Fläche/Hierarchie/Übergänge geliefert; UI-B13 präzisiert Titelgewicht | A02 muss auf Ein-Editor-Annahme Rücksicht nehmen; keine zwei kopierten Inspektoren. Nebenansicht lesend als begrenzte erste Stufe; editierbare Doppelfläche erst eigener geprüfter Hostzustand |
| D44 Paket 4 Tagesplanung | Hinweise, lokale ICS-Belegung, Kapazität/Entlastung vorhanden | PS-01-Prüfisolation und 3.43.1-Kürzelfix von Produktstand trennen. WA-20 nicht mit Tagesritual doppeln; Wochenziel muss auf bestehende Aufgaben/Notiz zeigen. WA-24 braucht vorher Vorkommensmodell |
| D44 Paket 5 Animation | D18 Frames/Dauer/Vorschau/PNG-Ausgaben mit Format 24 | vollständig gewählten Rahmen beibehalten; GIF/Zwiebelhaut/Kachelsatz optionale spätere Entscheidungen, keine unerledigten Abnahmekriterien. Exportkollision/Teilfehler/Timerabbau bleiben Regression |
| D44 Paket 6 Import/Wiederherstellung | Notion, Konfliktvergleich und einzelne Seite, Format 25 | frühere gekoppelte Grenze fachlich sinnvoll (IDs/Anhänge). Vor zusätzlichen Quellen WA-28/29 korrigieren. WA-19 je Quelle mit Verlustbericht spezifizieren; Notion-Datenbanken/Unterseitenhierarchie nicht nachbauen |
| D44 Paket 7 eigenständige Pakete | Python/Tk, Ressourcen und isolierte Starts historisch 3.42.0 | neuere Pythonfassung macht Pakete nicht aktuell. Mac-Bundle/Windows-Job/Arbeitspakete/Lieferhash getrennt; D43 Veröffentlichung bleibt offen. Kein Linux-Paket aus Pflicht-Linux-Tests ableiten |
| **D44 Paket 8 N12** | ausgewählter Aufgaben-Kernablauf; additive Semantik-/Runtimearbeit vorhanden | alltagstaugliche erste Stufe ist **vollständiger gewählter Kernablauf**, kein Attributdemo. Aktuellen UI-Stand einbeziehen, Orca-Lebensdauerfix nativ, VoiceOver/NVDA/Orca, Fokus, Paketläufe und Endmatrix. Breiter Seiten-/Pixel-/Kalenderzugang bleibt außerhalb. Aufwand für belegte Codekorrekturen 3–8 Tage mit hoher Unsicherheit; Readerdauer separat. Der alte P8-Schnitt bleibt, bis Inhaber anders entscheidet |
| **FP-00** | Monatsende-/Parser-/Zeitzonenfehler als 3.39.1 geliefert | historische Karte als Beleg/Regression, keine erneute Lieferung. Ganz-oder-gar-nicht-Regel des Parsers und Monatsendfolge in FP-02 übernehmen |
| **UI A01–A03/B01–B22** | B01–B20 implementiert/automatisch gezielt geprüft, Python 3.43.1; Originalauftrag und 28 Referenzen erhalten | B21 Pflege fortlaufend; B22 vollständiger Lieferabschluss offen. A Untersuchungsergebnis ≠ Umsetzung. Layoutnachweise decken nicht alle Designs/DPI/Dialoge/Maus/Trackpads; E-U1–3 eigenes Auswahlregister. Kein nochmaliger Großumbau aller B-Punkte |
| **Phasenentwurf 17.10. / D51** | große zusammenhängende Pakete und phasenweise Endprüfung ausdrücklich gewünscht | D51 ändert Prüfrhythmus, bestätigt keine E-P-Option und keine fiktiven 3.44–3.47 Termine/Versionen. Ursprüngliche 16–24/12–18/15–21/15–20 Tage ohne Endprüfung waren Vorschlagsgrößen; neue Risiken/WA-23/24 machen Summen nicht belastbar. Sinnvolle Zuschnitte §19.4, Auswahl §20 |

**Schutzrunde WA-27/28/29 und WA-30:** im lokalen Prüfkandidaten auf FP-01 integriert. Zehn Schutzfälle sind grün; dieselben zehn Gegenproben sind auf der ursprünglichen FP-01-Basis rot. Kein neues Datenformat, keine Lieferung nach 07. D51-Phasenabschluss und native/menschliche Abnahmen bleiben eigene offene Tore.

### 19.3 Erste nützliche Stufe, vollständiges Ziel und Option

Die detaillierten Funktions-/Testkarten FP-01–FP-07 in §16 bleiben zuständig. Diese Tabelle schließt deren Paketgrenzenprüfung ab und verändert ausgewählten Umfang nicht.

| Vorhaben | Erste bereits nützliche Stufe | Sinnvoll vollständiges Ziel / Zusatzfälle | Langfristig optional / Aufwand und Unsicherheit |
|---|---|---|---|
| FP-01 | Wiederholen für alle Bestandsschnappschüsse über denselben Menü-/Kürzelweg, Schreibfehlerzustand sicher | zusätzlich Pinnwandstapel, Verlaufshinweis, korrekter Editorfokus; upstream ist beides bereits Kandidat | persistente Undo-Historie nicht vorgeschlagen. Rest 2–5 Tage Übernahme-/Regressions-/Lieferarbeit plus Plattformprüfung; nicht erneut 2–5 Tage Neubau zählen. Bereichsprüfung erneut grün; Phasenabschluss und Lieferung offen |
| FP-02 | Intervalle, n-ter/letzter Wochentag, Vorschau, alte Regeln exakt gleich | D49 A/V zusätzlich ab Erledigung/Pause/Anzahl/Parser/RRULE; Pause/Reaktivierung/Ende/Erledigen früh/spät mit Undo/Redo | WA-23/24 und WA-14 sind separate, noch ungewählte Erweiterungen. FP-02 voll 6–12 Tage; ein gemeinsames Formattor ist vollständig wirtschaftlicher als eine zweite Migration. Mit Ausnahmen/Historie zusätzlich 5–10 Tage + Modellrisiko, kein „S“-Anhängsel |
| FP-03 | zusätzliche feste Bedingungen mit wahrer Erklärung und klarer Ungültigmeldung | gespeicherte Liste/Tabelle/Board, Gruppierung/Sortierung/Spalten und „Als Ansicht speichern“, gleiche Originalaufgaben | keine freien Felder/Datenbank. 5–10 Tage gesamt; Stufe 1 allein 2–4. Warnung „ältere Fassung zeigt mehr Treffer“, Ablage und Test gegen wirklichen Altleser; Bedienentwurf Stufe 2 fehlt |
| FP-04 | eine vorhandene Seite/Notiz anheften, lesen/öffnen/entfernen, Titeländerung folgt | Anheften über alle gewählten Wege, Deckbild/Auszug/Offenzahl, Verbindungen, PDF/Präsentation, Archivieren/Löschen/Undo | Bearbeiten innerhalb der Karte kein Auftrag. 3–6 Tage plus WA-09; größte Unsicherheit ist die Altleserablage, nicht der Auszug. Erste Stufe bei Zweifeln nur lesend ohne Titelbild, aber Namespaceprüfung immer Pflicht |
| FP-05 | unverknüpfte Titelstellen im eingeklappten Rückverweisbereich finden/öffnen | gezielt verknüpfen mit gleichem Objektvertrag; doppelte Titel, Wortgrenzen, Umlaut, bereits verlinkt/Quellobjekt/Umbenennung/Archivierte ausschließen | semantische KI-Ähnlichkeit kein Bedarf. 2–4 Tage; Zielambiguität sichtbar, niemals automatisch verknüpfen. Messung beim Aufklappen statt Dauerindex |
| FP-06 | fünf Aufträge mit passenden Musterantworten/erlaubten Feldern, gemeinsamer Datei-/Prüfweg | eigene Vorlagen lokal, Versions-/Capability-Angabe, `create` vs. `patch` klar, Originalbeschreibung bei Zusammenfassung behalten, exportierter Kontext nur im gewählten Umfang | KI-Endpunkt bleibt ausgeschlossen. 2–4 Tage; Vorlageninhalt und fremde Antwortqualität als unverbindlich. Kein Netz, kein API-Key, keine zweite Patch-Engine |
| FP-07 | gesamter lesbarer Markdownbaum mit Bildern/Anhängen/relativen Links plus Inventar, Manifest und Erhalt-/Verlustbericht | erste Stufe vollständig: Namenskollisionen, Windows-Pfadlänge, Symlinks, Schreibfehler/Abbruch, atomarer Zielabschluss, unveränderte Quelldaten, fehlende Anhänge/IDs genau zugeordnet | Canvas als zweite Stufe nach E-P5, unabhängig von der Lesbarkeit des ersten Exports. Markdown 4–8 Tage, Canvas zusätzlich 2–4; **kein garantierter Glide-Wiederimport**. Volles JSON-Backup bleibt Restaurierungsweg |
| A01 / E-U1 | reduzierter Modus für Heute/Liste/Seite/Notiz, Suche/Eingabe/Rückweg immer erreichbar | getestete Grenzen bei Schrift/DPI, gespeicherte Modusgrößen, Moduswechsel/Inspektor/Blockleiste; Buchinhalte im gleichen Host | Pixel/Pinnwand: Öffnen im Normalmodus klar anzeigen. 4–8 Tage; 480×560 ist Kandidat, kein Beschluss; native Mac-Menüleiste gegen Windows-Menübündelung prüfen |
| A02 / E-U2 | lesende Vorschau im Inspektorbereich, „Öffnen“ und ggf. Abhaken über gemeinsame IDs | echte editierbare Zweifläche mit zwei View-Hosts/Scroll-/Auswahlzuständen, einem Modell/Undo, aktivem Ziel und Flushvertrag | Zweitfenster nur als begrenzte Änderung von „eingebettet“, keine zweite App-Instanz. Lesend 3–6 Tage; Zweifläche 10–20; Zweitfenster 15–30 mit größter Unsicherheit. WA-28/29 vor Bearbeitung/Navigation |
| A03 / E-U3 | durchsuchbare Seiten-/Blockaktionen, Fokus-/Tastaturgriff und ruhiger Seitenkopf | dieselben Aktionen statt Parallelmenü, Menüzustände/Kürzel/Fokus/Abbruch/Reader; optional relative Seitenzeit WA-25 | Blockziehen langfristig 5–10 Tage zusätzlich/Modellprüfung, kein notwendiger Rest. Rang 1–3 gesamt 4–8 Tage, Zeitangabe zusätzlich 0,5–1,5; Hover ohne Fokus wäre keine Abnahme |
| WA-19 | eine zusätzliche Quelle vollständig begrenzt, Vorschau/Verlustbericht | weitere Quellen je Fixtures/Manifest/Quellenzuordnung, kein Überschreiben von Papierkorb/IDs | 3–6 Tage je CSV-Quelle, Ordner 4–8; Werte vor Exportfixtures nur Schätzung. Quellenwahl E-P3 nicht als drei Importer auf einmal schätzen |
| WA-20/21/22 | Wochenritual auf bestehenden Aufgaben; Fundorte lesend; vollständiges Layout-Backup/-Restore, jeweils eigenständig | keine zweite Zielaufgabe, alle Fundorte über IDs, abwärtslesbares Backup mit Layout und fehlenden Zielen vor Restore | grob 2–5/1–3/2–5 Tage; WA-22 ursprünglich S war ohne Restoreprüfung zu optimistisch. Unabhängige Teilpakete, keine automatische Pflichtkopplung |
| WA-26 | Bildkonversion aus dem Tk-Thread verlagern, mit Fehler-/Timeout-Rückmeldung | begrenzter Worker/Queue, Generation/Hostabbau, gemeinsame Pipeline für Galerie/Startseite/Seiten/Cover, negative Ergebnisse und Retry | Durch Cache/Index ersparte Kosten erst messen. 3–6 Tage, synthetischer langsamer Konverter und Hostwechsel belegen die UI-Reaktion; kein neues Format |

**Präzisierte Altlesergrenze WA-09/FP-04:** Unbekannte Schlüssel künftig zu erhalten ist sinnvoll, schützt aber nur Fassungen, die diesen Code besitzen. Eine bereits veröffentlichte 3.43.1 wird dadurch nicht nachträglich tolerant. Tragfähige Optionen sind (a) neue Seitenkarten unter eigenem obersten Namespace, den alte Leser unangetastet lassen, und neue Fassung führt bekannte Zeichnungskarten zusammen; (b) Einstellungsformat-Tor, das bereits gelesenen Schutzmechanismus voraussetzt und notfalls Mindestversion verbindlich macht. Empfohlen (a), nachdem ein realer Altleser-Rundlauf verlustfrei belegt wurde. Ein bloßer „eine Version früher schützen“-Plan ohne Mindestversion schützt ältere Exemplare nicht. Das ist technische Vertragsklärung innerhalb vorhandener Grenzen, keine erneute Produktwahl.

### 19.4 Konsolidierte Phasenfolge und Abhängigkeiten

**Prioritätsmaßstab:** zuerst nachgewiesener Bestandsschutz und korrekte Fehlerrückmeldung, dann ausstehender Abschluss beauftragter Umfänge, danach häufige Alltagsabläufe, dann Kontext/Ausstieg, erst danach optionale Breite. Unbekannte Fehlerhäufigkeit mindert nicht die Pflicht, einen reproduzierten Rollback-/Ladefehler zu korrigieren; ungemessene Performancevermutung rechtfertigt keinen Großumbau. Die Empfehlungen sind keine neue Produktentscheidung.

| Folge / bestehende Phase | Zusammenhängender Inhalt | Abhängigkeit / bereits unabhängig mögliche Arbeit | Aufwand und Regressionsrisiko |
|---|---|---|---|
| **0 Bestands-/Prüfabschluss** | PS-01/PS-02/W-Sichtfälle, Quell-/07-/Paketstand einfrieren, aktive Upstream-CI abschließend lesen, Referenz-Mac-Abschluss konkret benennen | Quellintegration und Ablageabgleich erfolgt; Liefer-/Paketabschluss und native Tore bleiben offen. CI-Erfolg gehört immer zum Hash | 1–3 Tage gezielte Ursachenarbeit, Mac-/Readerzeit extern. Testwartung nicht mit Produktfix verwechseln |
| **Schutzrunde vor Breitphase: Kandidat umgesetzt** | WA-27/28/29 und A33/FP-01-Kandidat mit transaktionalem Fehlervertrag, dazu WA-30 Datensperre; bei Reproduktion PS-02 | neue Import-/View-/Serienmutationen warten bis Schutzpfade bestehen; P8-Readerdiagnose und Bedienentwürfe unabhängig | Implementierung und gezielte Gegenproben abgeschlossen; frühere Schätzung 3–7 Tage ist kein heutiger Restaufwand. Offen bleiben Phasenendprüfung und Lieferung; zentrale Adapter benötigen native Regression |
| **P8-/UI-Lieferabschluss** | D36 gewählten Kernablauf auf aktuellen UI-Stand bringen, fehlende Mac-/Paketbelege und echte Reader prüfen; keine zusätzlichen Arbeitsbereiche | D50 Vorrang der B-Änderungen sachlich erfüllt, Abschluss 15.10. bleibt; E-P2 entscheidet Abweichung. Bei Readerblockade konkreten Rest übergeben | 3–8 Tage Code/Prüfvorbereitung + externe Reader/Paketzeit; kein angebliches Vollpaket bei abgebrochenem Orca-Lauf |
| **1 Bedienung und sicherer Kontextwechsel** | verbleibender FP-01-Lieferabschluss, WA-09; E-U3 Rang 1–3; E-U1 Kompakt nur gewählt; WA-12/TK9-RAD nach Befund, WA-25 nur gewählt | FP-01 nicht neu implementieren; Kompaktmodus und Menüfilter können als Entwürfe parallel laufen, abschließend ein Zustands-/Fokusabgleich | Kern 6–12 Tage, mit Kompakt zusätzlich 4–8; Bandbreiten nicht blind addieren. Weniger Dauerfläche, fehlender Fokus ist Blocker |
| **2 Rhythmen und Routinen** | FP-02 voll; WA-23/24/14 nur gewählt und mit fertigem Modell, WA-08 nur E-P4 | FP-01 und Schutzrunde; vor Formatschnitt Ausnahmen-/Historie/Zeiteinträge klären. Nicht jede Option muss ins gleiche Formattor gezwungen werden | FP-02 Kern 6–12 Tage, breite Phase 12–25 + Endprüfung, hohe Daten-/Regressionsunsicherheit |
| **3 Ansichten und Wissen** | FP-03/04/05, WA-21; E-U2 A/WA-11 nur gewählt; OB01 nur im angefassten Code, Tabellenmessung T8 | WA-09/neuer Namespace vor FP-04; FP-05/WA-21 vorab unabhängig; zwei Editoren brauchen Host-/Flushschutz | Kern 10–18 Tage, lesende Nebenansicht zusätzlich 3–6; mittlere bis größere Fokus-/Cachekosten. FP-03 und 04 nicht in ein gemeinsames Formattor zwingen |
| **4 Austausch und Wochenführung** | FP-06/FP-07 erste Stufe; WA-19/22/20 nur gewählt; Canvas E-P5 optional | Schutzrunde und Verweis-/Exportverträge; Wochenritual ist fachlich unabhängig von Importeranzahl, darf bei verzögertem Importer abgeschlossen werden | Kern 6–12 Tage, mit neuen Quellen/Backup/Canvas insgesamt 15–30; größtes Risiko Datei-/Verlustbericht, kein Datenschutz-Netzauftrag |
| **Auslöser statt Anschlusszwang** | WA-08/14/15, G18/G15/G10, ZF-NOTES/LABEL, weitere Zugänglichkeit, Toolkit-/Speicherneubewertung | jeweiliger Bedarf; D03/D16/Q3/Produktgrenzen gelten | kein Budget/Termin, keine ungefragte Roadmapverlängerung |

**Sinnvolle Parallelität:** P8-Readerdiagnose, Importfixtureinventar, A01/A03 Bedienentwürfe und Exportmanifest können unabhängig untersucht werden. Gemeinsame UI-Messungen/Vollprüfungen laufen seriell. Produktion an Undo/Load/Flush mutiert denselben Kern und braucht eine klare Zuständigkeit. Lesender Fundort/Erwähnungssuche lässt sich getrennt von Serienregeländerung entwickeln, wenn ID-/Löschregressionsfälle vereinbart werden.

### 19.5 D51: phasenweise prüfen, Belege nicht vermischen

Der Inhaber hat größere Pakete und phasenweise Prüfung gewünscht. Daraus folgt: während der Entwicklung Tk-freie Units und gezielte Suiten der berührten Wege; bei abgeschlossenem Teilpaket seine Pflichtsuite. Ein gemeinsamer Versionswechsel und eingefrorener Endlauf pro fachlich zusammenhängender Phase. Rote Vorversionsgegenproben, Linux-Defektfälle, native Windows-/Linux-Matrix, Referenz-Mac-Vollprüfung, relevante Messungen, Altleser/Migration, `abgleich_07`, Showcase und Pakete bleiben Endtore. Nach ausführbarer Korrektur oder einem tatsächlichen Befund betroffene Prüfungen und begründeten Endlauf wiederholen; kein Zwischenversionsritual je Kleinänderung. Menschliche Sicht-/DPI-/Readerabnahme wird je Phase gesammelt und getrennt ausgewiesen.

Zu große Phasen können Fehler spät lokalisierbar machen und lange ohne bereitgestellte Fassung bleiben. Deshalb Teilpakete mit eigenen Nutzens-/Fehlerbelegen und nur eine gemeinsame finale Matrix. Ein reproduzierter Schutzfehler darf als begrenzte Korrekturlieferung vorgezogen werden; eine offene optionale Nebenansicht oder Importquelle soll einen fertigen Kernablauf nicht unbefristet blockieren. Weder D51 noch der Phasenentwurf erteilen in diesem Analyseauftrag Commit-/Push-/Produktionsfreigabe.

## 20. Vollständiges Entscheidungsregister

### 20.1 Was bereits feststeht

Die ausdrücklich bestätigten **D01–D48**, der konkrete UI-/UX-Auftrag **D50** und die auf dem separaten Planungszweig belegte Prüfregel **D51** werden nicht erneut zur Wahl gestellt. **D49 ist eine Auslegung mit Korrekturvorbehalt**, keine einzeln beantwortete Auswahl. Der Abschlussauftrag 15.10. und der aktuelle Analyseauftrag bleiben bei der Reihenfolge maßgeblich. Neue tatsächliche Auswahlentscheidungen beginnen bei **D52**. Das Register hier bereitet Fragen vor; die Arbeitsrichtung dokumentiert erst eine eingegangene Antwort als verbindlich.

| Vorhandene Kennung | Ergebnis / verbleibender Entscheidungsbedarf |
|---|---|
| E-S1/D07 → D18 | Animation im angebotenen PNG-Rahmen gewählt, geliefert; GIF nicht erneut fragen |
| E-S2/I7 → D19/D21–D25 | Bild 1 und vier Oberflächenfunktionen vollständig gewählt; Lieferung 3.38.0, menschliche Abnahme getrennt |
| E-S3 → D20 | optionale Tageshinweise vollständig gewählt; keine erneute Vorgabenfrage |
| E-S4 → D26, E-S5 → D27 | Notion als erste Quelle und PyInstaller für beide Zielsysteme gewählt; weitere Quellen sind WA-19/E-P3, keine Änderung der ersten Quelle |
| E-S6/I8 → D28/D41/D45, E-S7 → D29 | Logo-/Systemzeichenweg und Master freigegeben; B10/D50 präzisiert gezielte Systemschrift für Lupe; kein neuer Fontauftrag |
| E-S8 → D30/D31 | lokale ICS-Belegung und die drei UI-Übergänge gewählt und geliefert |
| E-W1/E-W2/E-W4/E-W5 | D49 legt A/V für FP-01/02/03/04/05 und FP-07 A/1 aus; **keine neue Frage zur gleichen Funktion**. Produktinhalt bei ausdrücklicher Korrektur ändern, sonst Status als Auslegung erhalten |
| E-W3 | D49 A folgt Q3: FP-06 über Dateien, WA-10 kein lokaler Endpunkt. Kein neuer KI-Anbieter oder Schlüssel notwendig |
| E-W6/E-W7 | FP-00 vor Paket 5 geliefert, ursprüngliche Reihenfolge nach 4.0 durch D50/Abschluss 15.10. überholt; heutige Neuordnung über E-P1/P2 statt rückwirkend dieselben Varianten anbieten |
| I7/I8, A–H | Auswahl der beauftragten historischen Schnitte erledigt; weitere Tiefe nur über konkrete offene Kandidaten, nicht pauschal über alle acht Richtungen |
| AE-1–AE-7 | technische Alternativen, keine offenen Inhaberabstimmungen: feste Filter erweitern, Snapshot-Redo, RRULE-Fassade, echte Altleserablage, Datei-KI, Tk und JSON. Nur ein nachgewiesener Grenzkonflikt würde eine neue Produktentscheidung erzeugen |

**Größte Freigabewirkung:** E-P1 (Zuschnitt der nächsten Umsetzung) und E-P2 (Reihenfolge des P8-Abschlusses) bestimmen, welcher Arbeitsblock zuerst konkretisiert wird. E-U1/E-U3 verändern die Breite der Bedienphase. E-U2 ist vor der Wissensphase nötig. E-P3–P5 betreffen zusätzliche Optionen; deren Vertagung blockiert die bestehenden FP-Kerne nicht. Keine Antwort ist für den Abschluss dieser Analyse erforderlich.

### 20.2 E-P1–E-P5: Phasen und zusätzliche Funktionen

Die Kennungen und ihre ursprünglichen Optionen stammen aus dem Planungszweig vom 17.10. Die Empfehlungen unten sind anhand des neu belegten Schutzbedarfs und der bereits begonnenen FP-01-Arbeit aktualisiert. **D51 selbst steht nicht zur Abstimmung.** Die Optionen lassen sich knapp beantworten; eine abweichende Zusammenstellung kann der Inhaber ausdrücklich nennen.

| ID / Frage / Bedarfszeitpunkt | Anlass, Stand und bisherige Festlegung | Konkrete Optionen und Empfehlung | Folgen für Aufwand, Daten, Gestaltung, Tests / Vertagung |
|---|---|---|---|
| **E-P1 – Welchen Zuschnitt soll der nächste Umsetzungsauftrag haben?** Vor Beginn neuer Produktion | Nutzer 17.10. möchte größere Pakete, D51 bestätigt phasenweise Prüfung. Gefundener Plan war noch Vorschlag; jetzt liegen zentrale Schutzfehler und upstream FP-01 vor. D44/D50/Abschluss 15.10. bleiben | **A**: §19.4 als Rahmen, zuerst begrenzte Schutzrunde und vorhandene Abschlüsse, danach ausgewählte Phasen 1–4; jede Phase einzeln mit konkret eingefrorenem Umfang starten. **B**: die gleichen Inhalte in kleineren Lieferpaketen, phasenweise Endprüfung je solchem abgeschlossenen Paket. **C**: eigene Zusammenstellung. **Empfehlung A**, mit ausdrücklich begrenzten Schutz-/Abschlussarbeiten zuerst | Keine pauschale Wahl aller E-P3-Funktionen durch A. D51-Zwischenprüfungen bleiben, D42/D43 ebenso. Bandbreiten §19, keine festen Versionen. Vertagen lässt konkrete Schutzspezifikation/Fixtures/Entwürfe zu, startet aber keinen neuen Produktionsauftrag. Quelle: §18.4/§19, Original 17.10., Analyse A31–35 |
| **E-P2 – Wann wird der gewählte P8-Kernablauf abgeschlossen?** Vor einer Änderung der bisherigen Folge | D36/D44 wählen A/1; D50 UI-Priorität, Abschluss 15.10. verlangt gesicherten Abschluss vor Folgepaketen. Entwurf vom 17.10. empfahl parallel, Antwort nicht belegt. Additive Vorbereitung ist lokal vorhanden, echte Reader-/Endpaketbelege fehlen | **A**: eigener paralleler Strang, neue Funktionsphasen dürfen vor P8-Lieferung weiterlaufen; P8 nach jeder Phase abgleichen. **B**: bestehende Schutz-/UI/P8-Abschlüsse zuerst, danach neue Phasen. **C**: P8 nach den Funktionsphasen. **Empfehlung B** aufgrund des Abschlussauftrags und der Gefahr erneuter UI-/Runtime-Abweichung. Falls eine konkrete Readerplattform blockiert, Rest transparent übergeben und dann gezielt über unabhängige Weiterarbeit entscheiden | A/C ändern die bisherige Folge ausdrücklich und verursachen zusätzliche Integrations-/Readerregressionen. B wahrt den Auftrag, kann an realen Readerzugängen warten; Wartezeit nicht als Entwicklungsaufwand schätzen. Vertagen: bisheriger Abschlussauftrag gilt weiter, kein automatischer Wechsel auf A. Quellen D36/D44/D50, Abschluss 15.10., QA und §19 |
| **E-P3 – Welche zusätzlichen WA-19–WA-25 sollen aufgenommen werden?** Vor Umfangsfestlegung der betreffenden Phase | Vorschläge vom 17.10., keine bestätigte Auswahl. Marktprüfung vom 18.10. vertieft vorhandene Bedürfnisse, beweist keinen Bedarf an allen Zusatzfunktionen. WA-22/24 sind anders als früher angenommen datenwirksam bzw. unklar | Ursprüngliche Optionen bleiben: **A** alle sieben; **B** damalige Teilmenge WA-21/22/24/25/TK9-RAD; **C** keine. **Aktualisierte Empfehlung: einzeln wählen**, zunächst **WA-21 Fundorte**, **WA-22 Backup nur nach Restorevertrag**, **WA-25 nur zusammen E-U3 B**. WA-19 pro Importquelle, WA-20 Wochenritual sowie WA-23/24 erst nach Modellprobe entscheiden. Kurzantwort z.B. „E-P3 WA-21, WA-22; Rest vertagen“ | Die alte Begründung von B „ohne Datenwirkung“ ist nicht tragfähig: Backupvertrag/Serienhistorie brauchen Prüfung. A breitet Import-/Serien-/UI-Prüfmatrix erheblich aus. C lässt bestehende FP-Pakete vollständig möglich. Aufwand je Zeile §19.3. Vertagen verhindert keine Schutzkorrektur/FP-Kernarbeit. Quellen §18.4, Markt, Datenvertrag |
| **E-P4 – WA-08 Zeitauswertung jetzt oder bedarfsgebunden?** Vor Modellabschluss der Serienphase | derzeit nur Summe je Aufgabe; Nutzerbedarf an Zeitnachweis nicht belegt. D49 ließ P3-Auslöser offen; ein ohnehin anstehendes Formattor ist kein Nutzennachweis | **A**: tageweise Zeitprotokolle und Wochen-/Monatsauswertung nach Liste/Label einschließlich CSV mitplanen. **B**: weiter zurückstellen bis belegter Zeitnachweisbedarf. **Empfehlung B**; bei regelmäßigem eigenen Nachweisbedarf A | A verlangt Einträge mit stabiler Aufgabe, Datum/Dauer/Korrektur, Fokus-/Handbuchung, Migration alter Summen ohne erfundene Tagesdaten und Retention. Grob 5–10 Tage plus Prüfung, höheres Datenrisiko. B vermeidet zweite Zeitdarstellung und schränkt vorhandenen Fokustimer nicht ein. Vertagen hält WA-08 als ◇; FP-02 läuft unabhängig. Quellen WA-08, `week_review_data`, Markt Super Productivity |
| **E-P5 – FP-07 zusätzlich JSON Canvas?** Vor Exportphasenabschluss | D49 enthält FP-07 nur die erste Stufe. Canvas ist offene zusätzliche Option im 17.10.-Entwurf, nicht durch Recherche genehmigt | **A**: Canvas zusammen mit lesbarer Gesamtausgabe; **B**: zunächst vollständige erste Stufe, Canvas weiter P3. **Empfehlung B**, sofern Übernahme in ein anderes Canvas-Werkzeug nicht konkret geplant; bei diesem Bedarf A | A zusätzlich 2–4 Tage, Layout/Verbindungen/Dateireferenzen und Referenzleser prüfen; Seitenkartenablage FP-04 berücksichtigen. B sichert früheren Datenausstieg ohne Wiederimportversprechen. Vertagen blockiert Markdownbaum und Manifest von FP-07 nicht. Quellen FP-07, JSON Canvas Primärquelle im Markt, §19.3 |

### 20.3 E-U1–E-U3: konkreter Arbeitsmodus und Seitenbedienung

| ID / Entscheidungsfrage | Anlass, heutiger Stand, frühere Festlegung | Varianten, Vor-/Nachteile und Empfehlung | Auswirkungen, Vertagung und Zeitpunkt |
|---|---|---|---|
| **E-U1 – Kompaktmodus oder allgemeine kleinere Mindestgröße?** | A01 direkter Untersuchungsauftrag; Heute/Liste/Seite können Inhalte schon schmal darstellen, Kopf/Menüs werden in der historischen Probe unter 560 px verdrängt. Aktuelle Mindestgröße 860×700, B15 schützt jeden Button; kein konkretes neues Minimum gewählt | **A** eigener expliziter Kompaktmodus; normaler Modus bleibt, reduzierter Kopf mit Suche/Eingabe/Rückweg, erste Zielprobe 480×560. **B** allgemeine Mindestgröße senken, alle Ansichten/Dialoge unter neuer Grenze adaptieren. **C** unverändert. **Empfehlung A**: abgeschlossener Nutzen für schmales Nebenfenster bei überschaubarer Zustandszahl; Nachteil: zusätzlicher Modus und eingeschränkte Pixel/Pinnwandfläche | A: 4–8 Tage, B: 8–16 mit größerer Matrix; Einstellungen für Modusgröße und Lage additiv, kein Aufgabenformat. Maus/Tastatur/Reader/OS-Menüs/Schrift/DPI/Neustart prüfen; 480×560 erst nach erfolgreichen Proben festlegen. Vertagen behält 860×700, blockiert keine bestehenden UI-Korrekturen. Auswahl vor Bedienphase. Quellen §17.1, Prompt A01, S10/S11, Markt Microsoft To Do |
| **E-U2 – Zweiten Kontext lesen oder zwei Inhalte bearbeiten?** | A02 Untersuchungsauftrag; ein Ansichtszustand/ein Modell. Eingebettete Funktionen Hausregel, D17 schrittweise Extraktion, WA-28/29 schützen Wechsel. WA-11 Vorschau ist dieselbe Absicht, keine zweite Aufgabe | **A** lesende Nebenansicht im Inspektor mit „Öffnen“/gezielten Originalaktionen; **B** vollständig editierbare geteilte Inhaltsfläche; **C** zweites Fenster derselben Sitzung mit gemeinsamem Modell; **D** vertagen. **Empfehlung A**: konkreter Nutzen beim Nachschlagen, geringeres Fokus-/Datenrisiko; deckt freie Bearbeitung nebeneinander nicht ab. B: voller Zielumfang ohne Zusatzfenster, aber hoher Hostumbau. C: nützlich für zwei Monitore und verändert die Fensterregel begrenzt | A: 3–6 / B: 10–20 / C: 15–30 Tage, keine zweite schreibende App-Instanz. Stabile IDs, zwei Scroll-/Auswahlzustände, aktives Ziel/ein Undo/Flush/Abbruch/Hostabbau prüfen; Desktoplayout klein/groß, Reader/Design. Vertagen lässt Navigation wie heute und FP-03/04/05 unabhängig. Auswahl vor Wissensphase, B/C erst nach Schutzrunde. Quellen §17.2, Prompt A02/S09, Markt AFFiNE Peek |
| **E-U3 – Welche Notion-Muster kommen als eigenes Bedienpaket?** | A03 Untersuchungsauftrag; bestehende Blockaktionen/Palette/Titelbild sind vorhanden. S12–S17 belegen Anordnung, keine Geschwindigkeit. D50 fordert Analyse, nicht ungefragte Übernahme | **A** Rang 1–3: durchsuchbare Seiten-/Blockaktionen, dezenter fokus-/tastaturerreichbarer Griff als Einstieg in dieselben Aktionen, ruhiger Seitenkopf. **B** zusätzlich Rang 4/WA-25 relative Bearbeitungszeit. **C** nichts übernehmen. **Empfehlung A**; B nur bei wiederkehrendem Bedarf an Zeitinformation. Größter Nutzen durch schnelleres Auffinden bestehender Aktionen, Nachteil Pflege eigener zugänglicher Auswahl | A: 4–8 Tage, B zusätzlich 0,5–1,5; bestehende Aktions-IDs/Blockmodell, keine Datenmigration. Keine Hoverpflicht, Tab/Esc/Filter/Screenreader/Abbruch/Umwandlung/Undo/Hostwechsel prüfen. Blockziehen ist spätere Option, kein Pflichtteil dieser Wahl. Vertagen lässt bestehende Menüs, verhindert keinen P8-Abschluss. Auswahl vor Bedienphase. Quellen Markt §10/Notion-Primärquellen, Prompt A03/S12–17 |

**Kurze mögliche Antwort:** „E-P1 A, E-P2 B; E-U1 A, E-U2 A, E-U3 A; E-P3 WA-21/WA-22, Rest vertagen; E-P4 B, E-P5 B.“ Das ist eine Antwortvorlage mit Empfehlungen, keine bereits erteilte Zustimmung.

### 20.4 Veröffentlichungstore, Menschenabnahme und bewusst keine neue Frage

Die Veröffentlichungstore nach D43 stehen hier der Vollständigkeit halber. Sie blockieren keine Recherche, technische Schutzspezifikation oder Entwicklung eines unsignierten Entwicklungsartefakts. Öffentliche Veröffentlichung, Kauf, Kontoanlage, externe Meldung und Historienumschreibung benötigen ihren konkreten Auftrag. Detailunterlagen stehen allein in der [Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md); dieses Register bereitet die Auswahl und ihren Zeitpunkt vor.

| ID / Frage | Realistische Optionen / Empfehlung | Ursache, heutiger Stand, Folgen und Zeitpunkt |
|---|---|---|
| **I1 Inhaberangaben** | **A** vorhandenen Entwurf bestätigen/gezielt korrigieren; **B** öffentliche Veröffentlichung vertagen. Empfehlung A erst vor konkretem Release | Namen/Kontaktveröffentlichung ist Inhaberentscheidung. Daten/Code: kein Umbau; Pflichtangaben anschließend in Lizenz/README/Paket konsistent. Vertagen blockiert öffentlichen Release, keine Entwicklung |
| **I2 endgültige Glide-Lizenz** | **A** vorhandenes privat-nichtkommerzielles Modell abschließend prüfen und freigeben; **B** anderes explizit benanntes Lizenzmodell vorbereiten; **C** vertagen. Keine automatische Lizenzwahl | Entwurfs-/Fremdcode-Lizenzbelege vorhanden, eigener Nutzungsrahmen offen. Jede Variante ändert Nutzungsrechte und Pakettexte, nicht Datenmodell; Aufwand für Inhaberprüfung nicht geschätzt. Vor öffentlichem Release |
| **I3 Signierung/Konten** | **A** Developer-ID/Windows-Zertifikat in separatem Auftrag beschaffen; **B** Entwicklungsartefakte weiter unsigniert bzw. ad hoc mit Hash kennzeichnen. Jetzt B, vor Vertrieb A prüfen | Kauf/Registrierung/Secrets außerhalb Analyse; Integrität/isolierter Start bleiben prüfbar. Release-Tor auf beiden Zielsystemen, keine Suite ersetzt Zertifikat. Vertagen behält Warnungen/Vertrauensgrenze |
| **I4 Markenprüfung** | **A** gewählten Namen fachkundig prüfen lassen; **B** vor Veröffentlichung anderen Namen festlegen; **C** vertagen. Empfehlung A vor breiter Außenkommunikation | Keine erneute Produktidentitätsdiskussion ohne Befund. Namenswechsel hätte Paket-/Dokumentfolgen, stabile IDs `de.shaye.glide`/`Shaye.Glide` bleiben nach bisheriger Festlegung. Vertagen blockiert Namensfreigabe |
| **I5 systemweite Mac-Laufzeit** | **A** vorhandenen Referenz-Mac gezielt aktualisieren, wenn Prüfmatrix dies braucht; **B** mit reproduzierbarer gewählter Paketlaufzeit arbeiten und Systeminstallation vertagen. Empfehlung B bis Abweichung belegt | Historische 3.14.5/9.0.3 ist Messumgebung, keine aktuelle Versionsgarantie. Installation ist gesonderter Vorgang; keine unbelegte „neuestes Python“-Anforderung. Native Mac-Vollprüfung bleibt Abschlusstor |
| **I6 / OB06 Menschen-/Plattformabnahme** | **A** gebündelte Sitzung mit Prüfliste je nach verfügbarem Windows/Mac/Linux/DPI/Reader; **B** fehlende Konstellationen einzeln vertagen und Grenzen klar benennen. Empfehlung A für den gewählten P8-Kern, übrige Sichten priorisieren | Automatik ist kein Geschmacks-/DPI-/Readerentscheid. Praktisch zu prüfen: kleine Fenster/große Schrift, W-Sichtfälle, Trackpad, Gismo/Galerie, Inspektor/Kürzel, kompletter P8-Ablauf. Vor Behauptung voller Plattform-/Menschenabnahme, nicht zum Abschluss dieser Analyse |
| **I9 Fremdbildrechte** | **A** je Motiv Rechtebeleg bereitstellen; **B** ohne diesen Beleg durch nachweislich eigene Motive ersetzen und Showcase gezielt erneuern; **C** Veröffentlichung dieser Bilder vertagen. Empfehlung B falls Belege fehlen | Keine Stilllöschung im Analyseauftrag. Betroffene Grafik-/Showcasereferenzen und Bildvergleiche müssen weiter auflösen; aktuelle Rechteentscheidung nur Inhaber. Vor Veröffentlichung der betroffenen Bilder |
| **I10 Git-Historie** | **A** eigener begründeter Bereinigungsauftrag mit Backup/Abstimmung, **B** bestehende Historie vorerst behalten. Jetzt B bis Risiko-/Zielklärung | Umschreiben kann alle Commit-/Prüfbeleglinks ändern; hohe Koordinationswirkung, kein routinemäßiger Dokumentfix. Getrennte autorisierte Aktion mit verifiziertem Ziel, niemals aus Retentionsregeln ableiten |
| **I11 öffentlicher Auftritt** | **A** lokal vorbereitete Beschreibung/Tags/Wiki/Issues nach konkreter Auswahl veröffentlichen, **B** vorerst nur Dokumentationsstand pflegen. Jetzt B | Ein aktuelles README nennt keine öffentliche Releasefreigabe; CI-Prüfung und PR-Merge beweisen keinen fertigen Release. Details in Veröffentlichung; vor bewusstem öffentlichem Auftritt/Kontoaktion |
| **B7 Drittmeldung** | **A** reproduzierbaren Tk-Fehler in eigenem Auftrag melden, **B** bekannten Glide-Workaround behalten. Jetzt B | Kontozugang und Autorisierung zum Versand fehlen; technische Analyse unabhängig. Keine weitere Produktentscheidung oder Toolkitprobe erforderlich |

Keine neue Inhaberentscheidung ist für WA-26–WA-30 innerhalb der bestehenden Produktgrenzen nötig; die Lösung ist technische Korrekturarbeit eines folgenden Umsetzungsauftrags. Neue Abhängigkeiten, externe KI, Toolkitwechsel, SQLite-Hauptspeicher, Sync, freie Felder oder zusätzliche Arbeitsbereiche werden aus diesem Analyseauftrag nicht abgeleitet. Ihre bestehenden Grenzen bleiben bis zu einer ausdrücklichen Änderung gültig.

### 20.5 Zweiter Abgleich gegen Auftrag und Eingangsquellen

Das konsolidierte Inventar wurde gegen Entwicklungsplan, Arbeitsrichtung einschließlich des separaten D51-Quellstands, historische G-/N-Kataloge, Analyse, Markt, Funktionsvertrag, QA, UI-Prompt und Originalauftrag geprüft. Ergebnis: fehlende historische IDs wiederzugeordnet; aktive Stände G21/G26/N13/Startkacheln korrigiert; D49 von ausdrücklicher Auswahl getrennt; FP-01-Kandidat vom lokalen Lieferstand getrennt; Phasen-/WA-/E-P-Inhalte des separaten Zweigs mit unveränderten IDs erhalten; neue Befunde erst ab WA-26 eingeordnet; alle 25 UI-IDs und alle S26-/FP-Pakete behalten ihren Ablageort.

Offen bleiben die **ausdrücklich benannten** Produktions-/Menschen-/Reader-/Lieferprüfungen, die hier vorbereiteten Produktoptionen und nicht praktisch ausgeführte Konkurrenzabläufe. Der Plan ist als Analyse-/Planungsergebnis abschließbar; diese offenen Umsetzungen/Abnahmen werden dadurch nicht als erledigt erklärt. Ergebnisse tatsächlicher Dokument-/Linkprüfungen und der Quell-/Lieferhashvergleich stehen im QA-Nachweis dieser Runde.

**Gegenprüfung 18.10.2026:** Gegen den erweiterten Claude-Auftrag nachgetragen wurden die Datensperre A36/WA-30, die Upstream-Gegenprobe (A33 behoben, übrige Befunde unverändert), die A32-Präzisierung sowie die Quellen- und Rekonstruktionsbilanz ([Analyse §12.2](Glide_Analyse.md#122-quellen-und-rekonstruktionsbilanz-der-gegenprüfung)). Eine neue Inhaberentscheidung ist dafür nicht nötig: WA-30 ist eine Schutzkorrektur innerhalb bestehender Verträge.
