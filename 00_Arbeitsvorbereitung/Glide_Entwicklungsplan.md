# Glide – Entwicklungsplan und Aufgabenstand

Stand 14.10.2026 · Glide 3.42.0 · Aufgabenformat 25

Einziges Planungsdokument: alle Aufgaben mit Marke, Stufen, Ziele und was der Inhaber entscheidet. Erledigte Zwischenstände (Paketbeschreibungen, Messerzählungen, Aufgabenkarten) werden nach der Lieferung gelöscht; Ergebnisse stehen im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md) und im [CHANGELOG](../01_Repository/Glide/CHANGELOG.md), Verhalten in den [Funktionen](../01_Repository/Glide/docs/20_FUNKTIONEN.md), Vorfassungen in Git.

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

✅ heißt: umgesetzt, automatisch geprüft und geliefert – bis 3.33.18 auf Windows, ab 3.33.18 zusätzlich im eingefrorenen Volllauf auf dem Referenz-Mac, der alle früheren Funktionen mitprüft. Die menschliche Sicht- und Bedienabnahme steht für alle Versionen gesammelt unter I6 (§11) und wird nicht je Zeile wiederholt.

## 1. Leitsatz und Reihenfolge

*Glide ist der ruhige, lokale Arbeitsplatz für den eigenen Tag – planen, erledigen, festhalten; alles in einer eigenen Datei, ohne Konto. Die Pixel-Werkstatt ist die persönliche Signatur.*

Drei Säulen in dieser Rangfolge: **verlässlich und schnell** (Daten sicher, Aktionen unter 100 ms bei realistischen Beständen) → **klarer Alltag** (Heute, Demnächst, Listen, Seiten; Erfassen ohne Nachdenken) → **Wissen im Kontext** (Aufgaben in Seiten und Notizen, Verweise, Suche).

**Bewusst begrenzt:** kein allgemeiner Notion-Nachbau, kein Sync- oder Cloud-Dienst. Die Pixel-Werkstatt ist eine besondere Kombination, keine bewiesene Alleinstellung. Es liegen keine Nutzungsdaten vor; Prioritäten folgen Funktionslücke, Entscheidung, Aufwand und Regressionsrisiko.

Reihenfolge der Stufen (Antwort des Inhabers vom 30.09.2026, bestätigt am 01.10.2026): Fundament → Planen → Wissen → Pixel → Austausch und Verteilung.

| Stufe | Inhalt | Stand |
|---|---|---|
| 0 Fundament | Performance P01–P09, T2, CI | ◐ Ziele für Abhaken und Suche erreicht (3.33.19, 3.34.0); P03/E01 und Linux-Kalibrierung mit 3.36.0 geliefert; P05 im Sprint-Code fortsetzen |
| 1 Klarer Alltag | Bereiche, Startseite, Eingabe, Eisenhower, Heute/Demnächst, UX1, Fokus, Komfort, Tag, Oberfläche Welle 1 | ◐ geliefert bis 3.33.21; Welle 2 nach I7 in 3.38.0 geliefert, Mac/Linux/Windows automatisch grün; Menschenabnahme getrennt offen; AU03-Hinweise/AU07 mit 3.39.0 geliefert |
| 2 Wissen im Kontext | Suche, Verweise, Live-Liste, Titelbild, Kalender mit Wochenplanung, Bilder in Seiten, Filter erklären | ◐ geliefert 3.33.7–3.34.0; N05 in 3.38.0 geliefert, Mac/Linux/Windows automatisch grün; Menschenabnahme getrennt offen |
| 3 Pixel | Palettenbearbeitung, Symbolvorschau, Animation | ◐ G19, G-03 ✅ 3.35.0; G17 ✅ 3.40.0 geliefert |
| 4 Austausch und Verteilung | KI-Austausch Stufe 2, Import, Sicherungsvergleich, Paket mit eigenem Python | ◐ G24, F-03 ✅ 3.35.0; G21 ✅ 3.41.0 geliefert; G26/D27 ✅ 3.42.0 geliefert |
| 5 Zukunft (4.x) | Screenreader (Tk 9.1), Seitenversionen, SQLite nur nach D16-Neubewertung | ▶ N12 Aufgaben-Kernablauf durch D36/D44 für 4.0.0 beauftragt und vorbereitet; übrige Zukunftspunkte ◇ |

## 2. Erledigt seit 3.30

| Version | Inhalt |
|---|---|
| ✅ 3.30.0–3.31.0 | Modernisierung: Pinnwand-Board, Ordnertypen, Seiten und Galerie, Pixel-Werkstatt mit Größen 16–128, Format 20, Bilder in Seiten, Tk 9, Ziehen aus Finder/Explorer, Systemmitteilungen (Option), Logo, Sicherungen nur bei Änderung, Startprüfung, Notizbereich, gemeinsamer Editor, Inhaltsverzeichnis, Aufklapp- und Hinweisblöcke |
| ✅ 3.32.0–3.32.3 | Symbol-Export (ICO), Paletten aus Aseprite/Adobe, Platzhalter, Tagesabschluss; Klappkontrolle (D08); Ziehen in Bereichsbäumen (D04); Schriftcache; Bibliothekskarten erhalten; Showcase |
| ✅ 3.33.0–3.33.6 | Formatsicherung T2, P09a; vier Seitenleistenbereiche; Startseite „Ruhig“ (D12); Schnelleingabe mit Feldchips (D10) und Wiederholungen; Eisenhower als Gruppierung (D13); „Heute“ und „Demnächst“ (D14) |
| ✅ 3.33.7–3.33.12 | Inhaltssuche (G14), Windows-Formatsicherung; P08a, P09b, P08b; stabile Aktionskennungen, U03/U07; U10/U19, erste OB01-Übernahme |
| ✅ 3.33.13–3.33.18 | KO01/AU02 Einplanen mit verfügbarer Zeit; Tagespaket AU01/AU03-Weg/G05/H-02; Aufgaben im Wissen G29/G31/G32 (Format 21); Bedienkomfort U01/U02/U13/U14/U16/U22/U24; Wissen und Woche N04/AU04, G08/G30 (Format 22); Seiten im Alltag G28/G09/U08 (Format 23) |
| ✅ 3.33.19–3.35.0 | Sprint (§14): Tempo, Komfort, ruhige Oberfläche, Wissen und Seiten, Pixel und Austausch |
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
| U02 | Dauerhafte Hinweiszeilen (P1, P4) | „?“ klappt Hinweise ein/aus, Zustand gemerkt (D11) | ✅ 3.33.16 |
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
| LG01 | Logo-Rückfall unter Tk 8.6 geglättet (Weg B der [Funktionsnachweis](../01_Repository/Glide/tests/qa-3.37.0/logo_symbole_2026-10-10/README.md)) | ✅ 3.37.0 geliefert; Mac/Linux/Windows automatisch grün, Menschen-/DPI-Abnahme getrennt |
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
| G21 = F-02 | Begrenzter Import aus einer ersten Quelle mit Verlustbericht | ○ E-S4 |
| F-03 | Zwei Sicherungsstände lesbar vergleichen | ✅ 3.35.0 |
| G26 = H-03 = N11 | Paket mit eingebettetem Python 3.14 + Tk 9 je Plattform (D15) | ○ E-S5 |
| – | Windows-/Linux-Abnahme, Linux-App (AppImage/Flatpak später) | ○ Inhaber |
| H-01 | Kontrollmatrix echter Bedienwege fortführen | laufend |

## 7. Zukunft und bewusst nicht

| ID | Thema | Marke | Grund / Auslöser |
|---|---|---|---|
| N12 = U23 | Screenreader und beschriftete Canvas-Bedienung über Tk 9.1 `tk accessible` | ▶ | Aufgaben-Kernablauf als erste Stufe gewählt (D36); G26 und tatsächliche Readerabnahme erforderlich |
| N13 | Einzelne Seite aus vorhandener Sicherung wiederherstellen | ▶ | vollständig gewählt (D37); Text, Bilder/Anhänge, Aufgabenverweise, Live-Listen; kein fortlaufendes Versionssystem |
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
| N15–N20 | Spracherfassung, Cloud-KI, Teamfunktionen, freie Datenbankfelder, Web Clipper | ✕ | Produktgrenzen |

## 8. Abhängigkeiten und Regeln

- **Referenz- und Löschregeln:** Eine Aufgabe hat genau einen Heimatort (Liste, Seite oder Notiz), andere Orte zeigen einen Verweis. Entfernt man eine Verweiszeile, entfällt nur der Verweis. Entfernt man die Zeile am Heimatort, wandert die Aufgabe in den Papierkorb; Verweise zeigen „im Papierkorb“ bzw. nach endgültigem Löschen „Ziel fehlt“. Undo stellt beides zusammen her.
- **Datenformat-Tore:** Format 21 (Aufgabenverweise, 3.33.15), 22 (allgemeine Verweise, 3.33.17) und 23 (Live-Listen/Titelbild, 3.33.18) sind vergeben. Der nächste inkompatible Inhalt (etwa Animation G17) bekommt die nächste freie Nummer, mit Vorsicherung, Migration und schreibgeschütztem Altleser.
- **Reihenfolge:** D07 vor G17; Importquelle (E-S4) vor G21; D15/E-S5 vor G26 vor N12; I7 (E-S2) vor OB02, OB03-Rest, N05 und KO04.

## 9. Risiken

| Nr. | Risiko | Gegenmaßnahme |
|---|---|---|
| R1 | Regressionen in der Klasse `ListApp` (rund 57.400 Zeilen in `app.pyw`) | kleine Schnitte, echte Bedienproben, Vollprüfung je Paket, Fachlogik als Tk-freies Modul (D17) |
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
| Startseitenkacheln im Standard | 7 (D12) | ✅ seit 3.33.2 |
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

**Auftrag des Inhabers vom 08.10.2026** (Kern im Wortlaut): „Führe auf dieser Grundlage anschließend einen langfristigen, umfangreichen Feature-Sprint durch.“ Verlangt waren Analyse ([Analyse](Glide_Analyse.md)), Recherche ([Markt und Vorbilder §7](Glide_Markt_und_Vorbilder.md#7-recherche-08102026-für-den-sprint)), dieses Aufgabendokument und die vollständige Umsetzung mit Prüfung. Umfang: alle offenen Aufgaben der Stufen 0–4 ohne offene Inhaberentscheidung, dazu die Analysebefunde. **Umgesetzt und geliefert 3.33.19–3.35.0 am 09.10.2026.** Die Aufgabenkarten (Ausgangslage, Nutzen, Umfang, Akzeptanz, Prüfung) sind nach der Lieferung gelöscht; sie stehen in Git (Commit `6098877`).

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

**Status: Phase 1, Auswahlrunden 1 bis 6 am 10.10.2026 festgelegt (D18–D43), Gesamtplan am 10.10.2026 mit „ja“ bestätigt (D44), Phase 2 begonnen.** Alle angebotenen Funktionskandidaten sind entschieden. §15.7 legt acht bestätigte Produktionsversionen mit Reihenfolge und Prüfungen fest; §15.8 benennt die verbleibenden Abnahmetore. Die ausdrückliche Bestätigung D44 erlaubt die vollständige Umsetzung; weitere Abnahmetore bleiben bestehen. Keine Auswahl aus Empfehlungen oder Schweigen ableiten.

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
| S26-20 / I6, W01/W02/W06–W08/N08 | Windows seit 3.33.18, Linux-Sicht und Menschenabnahme offen → belegter Plattformstand | A/V nach D42: native Windows-Vollprüfung je Lieferung; vorhandene Windows-/Linux-Sichtfälle nachführen; L + getrennte Abnahme | native Windows-/Linux-Runner; GitHub Actions aktiviert; Inhaber für Menschenabnahme | Mac/Linux/Windows-Ergebnisse getrennt; kein automatischer Lauf ersetzt Menschenbedienung/DPI/Screenreader; keine unbelegten Plattformfreigaben | native Vollprüfungen je Lieferung, vorhandene manuelle Prüfliste; konkrete Lauf-/Artefaktverweise; echte Readerproben getrennt von Attributtests | ◐ 3.36.0, 3.37.0 und 3.38.0 nativ Windows/Linux grün; weitere Lieferungen und Menschenabnahme bleiben Pflicht |
| S26-21 / P05 | gemeinsame Helfer nur teilweise → gezielte Vereinheitlichung | A/1 nach D40: nur nachweislich gleiche UI-Texte/Abläufe im angefassten Sprint-Code; S–M | kein Großumbau, D17; D40 | gleiche Bedeutung, keine stillen Aktions-/Begriffsänderungen; kein Gesamtabgleich | betroffene Aufrufer, Bindungen und bestehende Suites; Gegenprobe für jeweiliges Paketverhalten | ▶ erste Stufe ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-22 / LG04 | Knicke an Rundungsübergängen und enger Innenraum klein → sauberer Master | A/V nach D41: tangentiale Anschlüsse/Kurzsegment, zusätzliche Kleingrößenfassung 16/32; M–L | Vorher-/Nachher-Abnahme vor Übernahme; D28 unabhängig | Silhouette/Farbe erhalten; keine stille Masteränderung; Exporte nachvollziehbar | Vektor-/Rastervergleich, 16/32/54/512 px, Gestaltungsabnahme, App-Symbole/Lieferabgleich; Gegenprobe gegen Vorversion | ✅ 3.37.0 geliefert; Mac/Linux/Windows automatisch grün; Menschen-/DPI-Sichtprüfung getrennt offen |

Quellen: [Analyse](Glide_Analyse.md), §3–§7/§14.2 dieses Plans und [Markt/Vorbilder §8](Glide_Markt_und_Vorbilder.md#8-quellenabgleich-für-die-neue-planung-09102026). V01/V02 sind eigene Ableitungen, keine behaupteten Herstellermerkmale. N13 stammt bereits aus §7. Jede Karte ist ausdrücklich ausgewählt; §15.7 ordnet alle 23 Aufgabenkennungen einer Lieferung oder einer durchgehenden Aufgabe zu.

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

Nach D19 drei Bildtafeln mit jeweils Heute, Liste, Seite und Inspektor erstellt und in dieser Reihenfolge im Chat gezeigt. Grundlage: vier neue Aufnahmen des eigenen Glide-3.35.0-Fensters, künstliche Daten im temporären `GLIDE_DATA_DIR`, Python 3.14.5/Tk 9.0.3, 1280 × 840; nur `screencapture -l` des eigenen Prozesses. Quellenbilder außerhalb von OneDrive. Erzeugung über das eingebaute Image-Gen-Werkzeug nach Product Design; Apple-Design-Grundsätze zu Hierarchie, Nähe und unmittelbarer Rückmeldung berücksichtigt, keine Webbibliothek oder Laufzeitabhängigkeit eingeführt.

Die Bildtafeln sind lokale Vorschauen, keine implementierten oder nativ abgenommenen Oberflächen. Ablagepräfix: `~/.codex/generated_images/01a12269-6761-77d1-af2d-28dc26d3041d/`. Bild 1 ist nach Auswahl im Grafik-Master gesichert; Varianten 2/3 bleiben unversionierte Vorschauen. Der ausgewählte Entwurf wird vor Umsetzung an die tatsächlichen Tk-Mittel und Regeln gebunden. Maßgeblich ist die sichtbare Reihenfolge, nicht eine gedachte Reihenfolge von Generierungsaufträgen.

| Sichtbare Auswahl | Datei im Vorschauordner | Bindung und Bildbefunde |
|---|---|---|
| Bild 1 | `exec-54aa307c-afd5-4865-8b4f-a9c8bf9834f3.png` | kompakte Hierarchie; Bildempfehlung. Die Listenoptik darf nicht die vorhandenen Ansichtsmodelle ändern; Tabellen-/Listenwahl bleibt erhalten. |
| Bild 2 | `exec-881c3be5-d725-4606-bd42-6945118d9c6d.png` | stärkere nächste Handlung; Bildfehler: „Nächste Aufgabe“ doppelt. Vor Umsetzung entfernen; Nutzer im Chat darauf hingewiesen. |
| Bild 3 | `exec-6cc1ed81-1e0e-4174-b6d0-cd7525d2f59f.png` | dokumentorientierte Hierarchie im vorhandenen dunklen Erscheinungsbild; kein neues Design und keine echte Unschärfe daraus ableiten. |

Für alle drei gelten unabhängig vom Bild: bestehende Symbole aus `ICONS`, Farben aus Rollen, jede Angabe einmal, keine erfundenen Feld-/Navigationsfunktionen, alle bisherigen Felder erhalten. Kontrast, große Schrift, 860 × 700 und das 15-%-Ziel sind erst in einer tatsächlichen Umsetzung messbar; die Bilder belegen sie nicht. Bei einer Bildwahl mit Änderungswunsch zunächst die gewählte Referenz gezielt überarbeiten, dann im Gesamtplan festlegen.

| Einzelentscheidung | A – erste Stufe | B – vollständig (Empfehlung) | C / Nutzen und Abwägung |
|---|---|---|---|
| OB02 / S26-01 | nur Heute-Kopf mit nächster Aufgabe, Zeit und Fortschritt; M | vier Textstufen in Heute, Listen, Seiten und Inspektor sowie Heute-Kopf; M–L | C: auslassen. Schnellere Orientierung; größere Tiefe berührt mehr Layouts. |
| OB03 / S26-02 | bedarfsabhängige Zeilenaktionen in der Aufgabenliste; M | Liste, Tabelle, Heute und Demnächst; M–L | C: auslassen. Weniger Dauerbedienung; Tastatur, Kontextmenü und Palette in beiden Stufen Pflicht. |
| N05 / S26-03 | gemeinsamer Inspektor für Liste/Tabelle, andere Bearbeitungswege zunächst erhalten; M–L | ein Aufgabeneditor über Liste, Tabelle, Heute, Demnächst, Pinnwand und Aufgabenverweise; schmal innerhalb der Inhaltsfläche; L | C: auslassen. Größter struktureller Nutzen, zugleich größtes Regressionsrisiko dieser Runde; alle Felder/Einstiege erhalten. |
| KO04 / S26-04 | Bearbeitungstag, Fälligkeit, Wichtigkeit und Labels direkt im Inspektor öffnen; M | außerdem an sichtbaren Aufgabenfeldern in Liste, Tabelle, Heute, Demnächst, Pinnwand und Dokumentverweisen; L | C: auslassen. Kürzere Wege; braucht ausgewähltes N05 und Prüfung von Positionierung, Fokus und Abbruch. |

Bildwahl und Funktionsauswahl wurden getrennt beantwortet: Bild 1 und jeweils B – vollständig für OB02, OB03, N05 und KO04 (D21–D25, 10.10.2026). D18–D43 werden nicht erneut zur Wahl gestellt. Ausgewählte Referenz: [Glide-Oberflaeche-Referenz.png](../20_Grafik_Master/05_Inspiration/Glide-Oberflaeche-Referenz.png), mit dem integrierten Image-Gen-Werkzeug aus den vier eigenen Aufnahmen erzeugt. Promptvorgaben: native Glide-/Tk-Desktopanwendung, vier Ansichten auf einer Tafel, kompakte Hierarchie und kürzere Wege; bestehende drei Zonen, deutsche Texte, Rollenfarben und vier Textstufen; künstliche Aufgaben vom 10.10.2026; keine neuen Felder, Cloudfunktionen oder Abhängigkeiten. Bild 2/3 bleiben verworfene lokale Varianten.

### 15.5 Dritte Auswahlrunde und Quellenbindung (10.10.2026)

Entschieden: E-S4 A/V (D26), E-S5 A/V (D27), E-S6 A/V (D28), E-S7 A/V (D29). Antworten im Wortlaut in der Arbeitsrichtung; Umfang, Nutzen, Abhängigkeiten, Akzeptanz und Prüfung in S26-09 bis S26-12. Erste Stufen/Alternativen wurden einzeln angeboten: Notion nur Text oder allgemeiner Markdown-Ordner; Paket zunächst Mac; Logo zunächst B+D+F oder nur vorhandener Tk-9-Weg; drei Problemzeichen statt gesamte ICONS-Tabelle bzw. Symbolschrift je System; jeweils Verschieben/Auslassen möglich. Gewählt wurde jeweils der vollständige angebotene Rahmen.

PyInstaller-Version, Lizenz, Tk-Hook, native Plattformbindung, Ordnerpaket und Tk-/macOS-Hinweise vor der Auswahl anhand der Primärquellen geprüft ([Markt §8](Glide_Markt_und_Vorbilder.md#8-quellenabgleich-für-die-neue-planung-09102026)). D27 enthält Bauwerkzeug und Bauwege, keine Freigabe für öffentliche Veröffentlichung, Konten oder neue Glide-Lizenz.

**Runde 4 entschieden (D30–D35):** 13 E-S8a ICS (Einzeltermine oder zusätzlich Serien/Ausnahmen), 14 E-S8b Bewegung (Abhaken/Klappen oder zusätzlich Bereichswechsel), 15 Bedienfläche (Liste/Heute oder alle betroffenen Hauptansichten; alternativ nur messen), 16 P03-Rest (Karten oder zusätzlich Startseiten-Neuaufbau), 17 E01-Rest (erste Anzeige oder zusätzlich Wiederverwendung), 18 Linux (Kernwege oder gesamte sachlich ausführbare Matrix). Jeweils A/1 erste Stufe, A/V vollständig oder B auslassen; bei Bedienfläche B nur messen/C auslassen. Gewählt jeweils A/V. Bedienflächen-Referenz 1280 × 800 folgt bereits dem verbindlichen P4; 840 ist nur Zusatzmessung. Ziele P03 ≤ 150 ms; E01 erste Anzeige ≤ 250 ms, erneutes Öffnen ≤ 150 ms. Abweichungen belegt vorlegen. E01 wird nach D34 getrennt als S26-14b geführt. Gesamtplan D44 bestätigt; nächste freie Entscheidung D50. P03/E01 und Linux-Matrix mit 3.36.0 geliefert, Bewegung/Bedienfläche mit 3.38.0 und grüner Mac-/Linux-/Windows-Vollprüfung geliefert; Menschenabnahme getrennt offen. Ziele nach D46/D47 und der Folgeentscheidung D48 präzisiert; übrige Umsetzungen gemäß §15.7.

### 15.6 Fünfte Auswahlrunde (10.10.2026)

Entschieden durch D36–D41; Schlussrunde anschließend D42/D43, Gesamtplan D44 bestätigt, Logoentwürfe D45 freigegeben; nächste freie Entscheidung D50. Aufwand S bis 1 Arbeitstag, M 2–4, L mehr als 4; N12 vollständig braucht mehrere Pakete. Empfehlungen sind keine Auswahl.

| Frage / Aufgabe | Erste Stufe A/1 | Vollständig A/V | Nutzen / Abwägung / Empfehlung |
|---|---|---|---|
| 19 / S26-16 N12 | zugänglicher Aufgaben-Kernablauf: Erfassen, Suchen, Heute planen, Inspektor; Rollen/Namen/Werte/Zustände und Fokus; L | zusätzlich Seiteneditor, Kalender, Pinnwand und Pixel-Werkstatt mit semantisch tastaturbedienbaren Alternativen für Canvas; mehrere Pakete | zugängliche Arbeit; eigene geprüfte Tk-9.1-Laufzeit und tatsächliche VoiceOver-/NVDA-/Linux-Screenreader-Abnahme nötig. Empfehlung A/1; B später. |
| 20 / S26-17 N13 | reine Textseiten aus vorhandener Sicherung; Vergleich/Vorschau, Vorsicherung, ein Undo; komplexe Seiten abweisen; M | zusätzlich Bilder/Anhänge, Aufgabenverweise und Live-Listen; fehlende Ziele vorab zeigen; L | gezielte Reparatur ohne gesamten Bestand zurücksetzen; anspruchsvolle ID-/Verweis-/Anhangsregeln. Empfehlung A/V; B später. Kein neues System fortlaufender Seitenversionen. |
| 21 / S26-18 V01 | in Heute ausgewählte Aufgaben ausdrücklich auf anderen Tag verschieben, Vorher-/Nachher-Bilanz; M | zusätzlich Woche/Tagesvorschlag und Rückgabe in Vorrat; ICS-Belegzeiten berücksichtigen; M–L | Warnung wird Handlung; Mehrfachauswahl/Kontexte prüfen. Empfehlung A/V; B auslassen. Keine automatische Verteilung, Fälligkeiten bleiben, ein Undo. |
| 22 / S26-19 V02 | exakt gleiche Notion-Quellen wiedererkennen; M | neue/geänderte Quellen vergleichen, eigene Bearbeitungen als Konflikt, nur gewählte Änderungen übernehmen; L | Export später nachziehen; dauerhafte Quellenmetadaten/Formatmigration. Empfehlung A/V; B auslassen. Keine Live-Synchronisation. |
| 23 / S26-21 P05 | nachweislich gleiche Texte/Abläufe im angefassten Sprint-Code; S–M | systematischer Gesamtabgleich bestehender UI-Helfer, nur gleichbedeutende Duplikate; L | weniger auseinanderlaufende Bedienung; Gesamtabgleich viel Regressionsfläche. Empfehlung A/1; B auslassen. Kein Großumbau, D17 gilt. |
| 24 / S26-22 LG04 | tangentiale Rundungsanschlüsse, bedeutungsloses Kurzsegment entfernen, Silhouette/Farbe erhalten; M | zusätzlich Kleingrößenfassung 16/32 px mit breiterem Innenraum, Entwürfe vor Übernahme beurteilen; M–L | sauberer Master, verändert aber Gestaltung. Empfehlung B unverändert, falls Form beabsichtigt. D28 bleibt unabhängig gewählt. |

Quellen für V01/V02 im Marktvergleich §8; eigene Ableitungen. N12 nach dem dort dokumentierten Tk-9.1-Quellenabgleich, N13 aus der Zukunftsstufe, P05 aus dem bestehenden Performance-Auftrag, LG04 aus den Befunden im Grafik-Master. Auswahl: 19 A/1, 20 A/V, 21 A/V, 22 A/V, 23 A/1, 24 A/V (D36–D41). Schlussrunde: Windows je Lieferung A/V (D42), Veröffentlichungstore gesondert offen (D43). A–H wird nur in ausdrücklich ausgewählten Funktionen vertieft; bereits Geliefertes bleibt bestehen, keine pauschale Zusatzfunktion.

### 15.7 Bestätigter Gesamtplan: acht Produktionsversionen

**Am 10.10.2026 durch D44 bestätigt, Wortlaut „ja“.** Jede Tabellenzeile ist eine vollständige Lieferung nach §15.3. Die Funktionsumfänge aus §15.1 und D18–D43 werden dadurch nicht verkleinert. Die Folgepaket-Suiten sind geplant; `test_fundament3360` ist inzwischen vorhanden und gezielt geprüft, ihre eingefrorene Mac-Vollprüfung und native Linux-/Windows-Matrix sind grün. Terminliche Zusagen werden aus der Aufwandsgröße nicht abgeleitet.

| Folge / Version | Inhalt und Aufgaben | Warum in dieser Reihenfolge | Status |
|---|---|---|---|
| 1 / **3.36.0** | Fundament und Tempo: P03-Rest S26-14, E01-Rest S26-14b, gesamte ausführbare Linux-Matrix S26-15; native Windows-Vollprüfung S26-20 ab dieser Lieferung | belastbare Prüfstände und Tempo vor dem breiten Oberflächenumbau | ✅ 10.10.2026 geliefert; Mac/Linux/Windows automatisch grün |
| 2 / **3.37.0** | Logo und Symbole: Tk-8.6-Rückfall/App-Symbole S26-11, gesamte ICONS-Tabelle S26-12, Logo-Master und Kleingrößen S26-22 | Grafikgrundlagen vor neuen Oberflächenaufnahmen; Gestaltungsabnahme vor Masterübernahme | ✅ geliefert 11.10.2026: Mac/Linux/Windows automatisch grün, 07/05/Bundle bytegleich, Signaturen grün; Menschenabnahme getrennt |
| 3 / **3.38.0** | Aufgabenoberfläche nach Bild 1: OB02 S26-01, OB03 S26-02, gemeinsamer Inspektor S26-03, direkte Felder S26-04, Bewegung S26-07, Bedienfläche S26-13 | einheitliche Bearbeitungsfläche als Grundlage für folgende Planungs- und Zugänglichkeitswege | ✅ 12.10.2026 geliefert; Hash bcdbc4da, Mac/Linux/Windows-Vollprüfung und 18 Defektgegenproben grün; Tempo D46/D48 erfüllt, Lieferdateien/Signaturen erneut geprüft; Menschen-/DPI-Abnahme getrennt offen |
| 4 / **3.39.0** | Tagesplanung: Tageshinweise S26-05, ICS-Belegzeiten S26-06, Tag entlasten S26-18 | alle Kapazitätswege teilen dieselbe Bilanz; Entlasten berücksichtigt die neuen Belegzeiten | ✅ 3.39.0 geliefert; Mac/Linux/Windows automatisch grün, Menschen-/DPI-Abnahme getrennt offen |
| 5 / **3.40.0** | Pixelanimation S26-08 vollständig mit PNG-Spritesheet/Einzelbildfolge | eigenes Datenformat- und Exportpaket, getrennt vom folgenden Import | ✅ 3.40.0 geliefert |
| 6 / **3.41.0** | Notion-Import S26-09, Wiedererkennung/Konfliktvergleich S26-19, einzelne Seite aus Sicherung S26-17 | Quellenzuordnung und Wiederherstellung gemeinsam gegen Verweis-/Anhangsregeln prüfen | ✅ 3.41.0 geliefert; Mac/Linux/Windows automatisch grün |
| 7 / **3.42.0** | Eigenständige Pakete S26-10: PyInstaller 6.22.3, macOS arm64 und Windows x64, Python 3.14/Tk 9 | vollständigen Funktionsstand samt Ressourcen bündeln; Bauweg vor Tk-9.1-Wechsel festigen | ✅ 3.42.0 geliefert; Mac/Linux/Windows automatisch grün, Menschen-/Releaseabnahme getrennt |
| 8 / **4.0.0** | Zugänglicher Aufgaben-Kernablauf S26-16 A/1 mit eigener geprüfter Tk-9.1-Laufzeit und tatsächlichen Readerproben | baut auf gemeinsamem Inspektor und eigenständigen Paketen auf; Stufe 5 des Plans beginnt mit dem gewählten Schnitt | ▶ in Vorbereitung: 46 Semantiktests grün, native GUI-/Paket-/Readerabnahme offen |

**Durchgehend:** S26-20 umfasst Windows-Vollprüfung je Lieferung sowie Nachführung der vorhandenen Windows-/Linux-Sichtfälle und der getrennten Menschenabnahme. S26-21/P05 A/1 wird nur im tatsächlich angefassten Sprint-Code umgesetzt; seine Aufrufer werden im jeweiligen Paket geprüft. S26-15 nimmt nach der Kalibrierung auch jede neue sachlich ausführbare Sprint-Suite in die verpflichtende Linux-Matrix auf. D19/D21 sind mit erstellten Referenzen und Bildwahl erledigte Planungsvoraussetzungen, keine zusätzliche Produktionsversion. Damit sind S26-01–S26-22 einschließlich S26-14b vollständig zugeordnet.

**Paket 1 – 3.36.0, Fundament und Tempo.** Ausgangslage: echter Startseiten-Neuaufbau 270–300 ms, Einstellungen etwa 560 ms; Linux-Integrationen bisher nicht vollständig verpflichtend, Windows zuletzt 3.33.18. Ziel/Nutzen: kürzere Wartezeit und belastbare Plattformregressionen. Umfang: gezielte Kartenaktualisierung und viele Karten, tatsächlicher Startseiten-Neuaufbau, zuerst sichtbare Einstellungsbereiche und sichere Wiederverwendung. Abnahme: Startseite ≤ 150 ms; erste Einstellungsanzeige ≤ 250 ms, wiederholt ≤ 150 ms auf Referenz-Mac. Warm/kalt und Median/p95 getrennt dokumentieren; Fokus, Scrollposition, Cache-Gültigkeit, aktuelle Werte, Widget-/Speicherentwicklung und freigegebene Rückrufe prüfen. Keine reine Cachetreffer-Messung als Neuaufbau ausgeben. Neue Pflichtsuite `test_fundament3360` mit Gegenprobe gegen 3.35.0; echte Defektfälle sichern die kalibrierten Linux-Erwartungen. Vollständige Matrix mit begründeten nativen Plattformfällen führen. Nachweis: Baseline-/Nachhermessung, Suite/Gegenprobe, Mac-/Linux-/Windows-Ergebnisse. Messbare Zielabweichungen dem Inhaber vorlegen; sie gelten erst nach einer ausdrücklichen Entscheidung als akzeptiert. **D46 (10.10.2026):** Kalt-Ausnahme ≤ 300 ms bei direktem Start und ≤ 500 ms im beobachteten Kindprozessverfahren angenommen; warmer tatsächlicher Builder bleibt ≤ 150 ms, alle Funktionsumfänge erhalten. **D47 (10.10.2026):** erneute Einstellungsanzeige Median ≤ 150 ms/p95 ≤ 170 ms angenommen; erste Anzeige bleibt ≤ 250 ms. [Messnachweis](https://github.com/n05a-design/glide-to-do/blob/3f75265429410ed186109626d4e0776d5dcc3438/01_Repository/Glide/tests/qa-3.36.0/fundament_vorher_nachher/README.md). **Geliefert am 10.10.2026:** endgültiger Quellstand `04a0597…` hält D46/D47 ein. Eingefrorene Mac-Vollprüfung Exit 0 (100 ausgeführt, 835 Dateien unverändert), native Linux-/Windows-Matrix auf `3f267a2` jeweils Exit 0 (101 ausgeführt; je 83 Suiten/264 Unit-Tests), sieben Linux-Defektgegenproben passend rot. Windows-Desktop 1920 × 1080/Tk 9.0.4 bestätigt, alle zehn Vorlaufbefunde im Wiederholungslauf grün. 07/Showcase bytegleich, Bundle 3.36.0 im Bauordner und auf Rückkopie signaturgeprüft; [Liefernachweis](https://github.com/n05a-design/glide-to-do/blob/3f75265429410ed186109626d4e0776d5dcc3438/01_Repository/Glide/tests/qa-3.36.0/fundament_2026-10-10/README.md). Drei passende rote Vorversionsproben, aktuelle Werte/Fokus/Scrollen/Undo und Lebensdauer belegt. Manuelle Sicht-/Bedien-/DPI-/Readerabnahme bleibt getrennt offen.

**Paket 2 – 3.37.0, Logo und Symbole.** Ausgangslage: belegte Tk-8.6-Treppenkanten, langsamer großer PNG-Weg, Ersatzschriftzeichen und Masterknicke. Ziel/Nutzen: saubere Darstellung beim Start und in kleinen Größen. Entwürfe im Vergleich alt/neu sowie 16/32/54/512 px am 10.10.2026 als D45 vom Inhaber freigegeben. Nun technische Glättung per Standardbibliothek, App-Symbole 16/32/64/256 px, freigegebene tangentiale Masterkurven und Kleingrößenfassung liefern. Gesamte ICONS-Tabelle in der UI-Systemschrift auf Abdeckung, Größe, Ausrichtung und Bedeutung prüfen; Beschriftungen/Tastaturwege erhalten. Abnahme: korrekte Rastergrößen/Zwischentöne, DPI-/Akzentwechsel, unveränderter Tk-9-Weg, kein großes PNG im Startweg; native Sichtprüfung gesondert ausweisen. `test_logo3370`, Tk-freie Raster-/PNGtests, Gegenprobe gegen 3.36.0 für die bekannten Darstellungsfehler; Vektor-/Rastervergleich und Ressourcenhashes im Nachweis. Die technische Korrektur D28 und die freigegebenen Master D45 werden gemeinsam umgesetzt.

**Paket-3-Lieferabschluss 12.10.2026:** Nach nativer Matrix am früheren Hash 49ca48aa Auswahlverlust beim Langtextumbruch und zusätzliche Windows-Menüzeile korrigiert. Vorgängerhash 8cda250c: Mac/Linux und 18 Defektkontrollen grün; Windows-Vollprüfung 38213392543 drei Kopftextbefunde rot. Aktueller Hash bcdbc4da: Windows-Menüs teilen nur die Titelzeile, Statuszeile behält Breite; Titelmessung berücksichtigt die Menüs. Gezielte native Wiederholung 38220307993 mit 36 Kombinationen und drei Textsuiten grün; Mac-Vollprüfung Exit 0 (102 ausgeführt/zwei übersprungen), alle 899 Dateien unverändert; vier Gegenproben passend rot und Übergänge max. 106,20 ms. 07/05/Bundle bytegleich, Signaturen grün; strenge Liefer-CI grün; Tempo D46/D48 grün. Vollständige native Matrix 38272561080 am Kandidat a0288b7: Linux/Windows je Exit 0, 103 ausgeführt/eine menschliche Sichtprüfung übersprungen, 85 Suiten/294 Units; alle 18 Defekte passend erkannt. 189 Liefer-/97 Bundle-Dateien erneut bytegleich, Bau- und frische Rückkopiesignatur grün. Automatisch geliefert; Menschen-/DPI-Abnahme bleibt getrennt offen. Frühere Belege am Hash 49ca48aa bleiben historisch. Kein Umfang oder Flächenziel gelockert.

**D48 (12.10.2026), Tempoabschluss Paket 3:** Einstellungen warm weiterhin Median ≤ 150 ms, künftig p95 ≤ 190 ms; erste Anzeige weiterhin ≤ 250 ms, alle Funktionen erhalten. Wortlaut „A – Median 150 ms / p95 190 ms akzeptieren (Empfehlung)“. Fünf frische direkte Prozesse × 40 Wiederholungen ohne parallele Prüfungen ergeben 146,85/179,59 ms, max. 189,45 ms; erste Anzeige p95 203,90 ms. Startseite kalt p95 272,71 ms, warm 73,52/79,67 ms. Damit sind D46/D48 erfüllt; keine weitere Tempoentscheidung offen. Historische D47-Grenze und damalige Messwerte bleiben erhalten.

**Paket 3 – 3.38.0, Aufgabenoberfläche.** Ausgangslage: doppelte Bearbeitungsflächen, dauerhafte Zeilenaktionen und ungemessene Bedienfläche. Ziel/Nutzen: nächste Handlung erkennen und Felder unmittelbar ändern. Umfang vollständig nach D22–D25/D31/D32: vier Textstufen, Heute-Kopf, kontextuelle Aktionen in vier Ansichten, ein Inspektor und direkte Planungsfelder in allen sechs gewählten Kontexten; schmal innerhalb der Inhaltsfläche. Die bestehenden Listen-/Tabellenmodelle, sämtliche Felder, Einstiege, stabilen IDs, Schreibschutz- und Undo-Wege bleiben erhalten. Abnahme: Feld-/Einstiegsmatrix Liste/Tabelle/Heute/Demnächst/Pinnwand/Dokumentverweise; Maus, Tastatur, Kontextmenü und Palette; Popoverposition, Fokus, Abbruch und Neustart. Bewegung ≤ 150 ms, schnelle Folgen abbrechbar, Abschaltoption wirksam und keine zurückbleibenden Rückrufe. Bedienfläche in Liste, Tabelle, Heute, Demnächst, Seiten und Pinnwand ≤ 15 % bei 1280 × 800; 1280 × 840 zusätzlich berichten; 860 × 700 und große Schrift lesbar/erreichbar. `test_aufgaben3380` mit Geometrie-/Bindungs-/Lebensdauerproben, Gegenprobe gegen 3.37.0; Tempo vor/nach und eigene Fensteraufnahmen. Der Entwurf allein ist kein Messbeleg.

**Paket 4 – 3.39.0, Tagesplanung.** Ausgangslage: manuelle Tagesrituale, freie Zeit ohne externe Termine, Überplanung nur als Hinweis. Ziel/Nutzen: rechtzeitig beginnen/abschließen und Überplanung ausdrücklich korrigieren. Umfang vollständig D20/D30/D38: optionale Tageshinweise mit Vorgabe aus, 08:30/17:30, Uhrzeiten/Wochentagen, später erinnern/heute überspringen und gesammelten verpassten Hinweisen; nur laufende App, kein Zwangswechsel und keine doppelte Zustellung über Neustarts. Gewählte lokale ICS-Datei lesend, Einzel-/ganztägige Termine, übliche tägliche/wöchentliche/monatliche/jährliche Serien, Ausnahmen, Zeitzonen/Sommerzeit, transparente/stornierte Termine; nicht unterstützte Regeln sichtbar melden. Überschneidungen als vereinigte Belegzeit zählen. Nutzer wählt Aufgaben und anderen Tag/Vorrat aus Heute, Woche oder Tagesvorschlag; Vorher-/Nachher-Bilanz einschließlich ICS, Fälligkeiten erhalten, eine Aktion ein Undo. Abnahme: dieselbe Bilanz in allen Planungswegen, keine Kalender-Synchronisation oder aus Terminen erzeugten Aufgaben. `test_tag3390`, Tk-freie Zeit-/Zustell-/ICS-/Bilanztests mit künstlicher Uhr und Archiv-Fixtures; Sommerzeit, Randtage, Ausnahmen, Mehrfachauswahl, ungeschätzte Aufgaben, Modalzustand, Neustart/Undo; Gegenprobe gegen 3.38.0.

**Paket 5 – 3.40.0, Pixelanimation.** Ausgangslage: Zeichnungen haben nur einen statischen Zustand. Ziel/Nutzen: kleine Animationen vollständig lokal erstellen/exportieren. Umfang D18: Frames anlegen, duplizieren, löschen, umordnen; gemeinsame und einzelne Dauer; unterbrechbare Vorschau; PNG-Spritesheet und PNG-Einzelbildfolge. Abnahme: alte Zeichnungen verlustfrei erhalten, Reihenfolge/Dauer nach Neustart identisch, Bearbeitungen rücknehmbar, Exporte pixelgenau zu Frames; kein GIF. Eigenes Datenformat-Tor mit Vorsicherung, Migration und schreibgeschütztem Altleser. `test_animation3400`, Tk-freie Frame-/Zeit-/Exporttests und echte Werkzeug-/Undo-/Neustartproben, Gegenprobe gegen 3.39.0; Exportdateien und Migrations-/Altlesernachweis.

**Paket 6 – 3.41.0, Notion und Seitenwiederherstellung.** Ausgangslage: keine kontrollierte Notion-Quellenzuordnung, Sicherungsvergleich bisher lesend. Ziel/Nutzen: Inhalte mit sichtbaren Verlusten übernehmen, spätere Exporte kontrolliert nachziehen und einzelne Fehländerungen reparieren. Umfang vollständig D26/D39/D37: ZIP „Markdown & CSV“, Texte/Überschriften/Listen, lokale Bilder/Anhänge, Aufgaben-Kästchen und interne Seitenverweise; Unterseiten in bestehende Ordner/Seiten. Vorschau, Verlustbericht, Größen-/Pfadgrenzen und Vorsicherung. CSV-Datenbanken und nicht unterstützte Exportbestandteile ausdrücklich ausweisen und Quellen erhalten; keine Notion-Datenbank nachbauen. Unveränderte/neue/geänderte Quellen und lokale Konflikte dauerhaft wiedererkennen; nur ausdrücklich ausgewählte Änderungen übernehmen. Einzelne Seite aus vorhandener Sicherung mit Text/Bildern/Anhängen/Aufgabenverweisen/Live-Listen vergleichen und wiederherstellen; fehlende Ziele vorab zeigen, IDs konsistent, andere Seiten unverändert, ein Undo. Keine Live-Synchronisation oder neues System fortlaufender Seitenversionen. `test_import3410`, Tk-freie Parser-/Archiv-/Zuordnungs-/Konflikt-/Wiederherstellungstests; gleiche/umbenannte/geänderte Quellen, ungültige Archive, fehlende Ziele, Abbruch, Undo/Neustart; Gegenprobe gegen 3.40.0. Quellenmetadaten mit eigenem Datenformat-Tor sichern.

**Paket 7 – 3.42.0, eigenständige Pakete.** Ausgangslage: vorhandener Starter/Bundle braucht installiertes Python. Ziel/Nutzen: geprüften Stand ohne externe Python-Installation starten. Umfang D27: PyInstaller 6.22.3 ausschließlich gepinnte Bauabhängigkeit, native Bauwege macOS arm64/Windows x64 mit Python 3.14/Tk 9, Ressourcen/vendor, Drittanbieter-Lizenzbelege und nachvollziehbare Bauanweisungen. Abnahme: Paketversion/Architektur vollständig belegt, Daten außerhalb Paket, tatsächlicher isolierter Start und Ressourcen-/Import-/Speicherprobe ohne externen Python-Bezug. Leeres PATH allein genügt wegen absoluter Interpreterpfade der Vorversion nicht als Nachweis; zusätzlich Laufzeit-/Bibliotheksabhängigkeiten und den nativen isolierten Prüfstand belegen. `test_paket3420`, native Paketproben und Gegenprobe gegen 3.41.0; Paket-/Quellhashes und Start-/Signaturergebnisse. macOS-Ad-hoc-Signatur im Bauordner und auf Rückkopie prüfen. Windows ohne Inhaberzertifikat als unsigniertes Entwicklungsartefakt kennzeichnen und Integrität nachweisen; öffentliche Signaturen bleiben I3. Linux-Matrix bleibt Pflicht, ein eigenständiges Linux-Paket ist nicht gewählt.

**Paket 8 – 4.0.0, zugänglicher Aufgaben-Kernablauf.** Ausgangslage: bisherige Tk-9.0-Oberfläche hat keine belegte Screenreader-Bedienbarkeit. Ziel/Nutzen: den ausgewählten Kernablauf tatsächlich zugänglich machen. Umfang ausdrücklich D36 A/1: Aufgaben erfassen, suchen, in Heute planen und im gemeinsamen Inspektor bearbeiten; eigens geprüfte Python-3.14-/Tk-9.1-Laufzeit, auch in beiden eigenständigen Paketen. Rollen, Namen, Werte, Zustände, Auswahl, Fokus und Bedienaktionen setzen; eigene Canvas-Flächen im gewählten Kernablauf erhalten semantische Tastaturalternativen. Abnahme: vollständiger Kernablauf mit VoiceOver, NVDA und Linux-Screenreader tatsächlich durchführbar; Tastatur, Undo, Neustart und bestehende Funktionen bleiben erhalten. `test_zugang400`, Tk-9.1-/Semantik-/Fokusproben, Gegenprobe gegen 3.42.0, native Paketstarts und getrennte reale Readerprotokolle. Seiteneditor, Kalender, Pinnwand und Pixel-Werkstatt sind außerhalb dieser ersten Stufe; 4.0.0 bedeutet keine Abnahme dieser übrigen Zukunftsstufe.

**Technische Vorprüfung zu Paket 8 (14.10.2026):** Drei Semantikmodule mit 46 grünen Tk-freien Fällen und additive Anbindungen in einer privaten Kopie des aktuellen 3.42-Stands; noch keine native GUI-/Readerabnahme. Eigener Runtimebuilder mit vier reinen Vertragsfällen, native Aqua-Getter-/Aktionsprobe, AT-SPI-Textverbraucher und gepinnte tatsächliche NVDA-SpeechSpy-Probe vorbereitet. Checkboxwerte 0/1, unter Aqua echte Checkboxvariable und Schaltflächentitel aus der Beschreibung, unter X11 Rollenname `Checkbox`; editierbare Feldtexte bleiben unverändert. Die [Linux-Text-/Selektionsschnittstelle des gepinnten Tk-9.1-Originals](https://github.com/tcltk/tk/blob/3f45110c0a568b70f2ebd5412f215e87d199bc7d/unix/tkUnixAccessibility.c#L896) enthält Platzhalter (`get_text` NULL, Caret −1, Zeichenzahl 0); unter Aqua sind Aktionswarteschlange und Lesbarkeit schreibgeschützter Felder nativ zu prüfen. Native Gegenprobe vor jeder gezielten Runtimekorrektur. Neue Tcl/Tk-9.1-Lizenzoriginale einschließlich utf8proc und tatsächliche Mac-Tcl-Konsole abgeglichen, GUI-/Paketnachweis offen. Der Inhaber hat keine zusätzlichen Windows-/NVDA- oder Linux-/Orca-Prüfplätze; automatisierte native Readerproben und tatsächliche Menschenabnahme getrennt führen.

### 15.8 Gemeinsame Prüfungen, Abnahmetore und Abschluss

- **Starttor erfüllt:** ausdrückliches „ja“ zum Gesamtplan §15.7/§15.8 am 10.10.2026 als D44 erfasst. Ausgangslieferung 3.35.0; Umsetzung beginnt mit isolierter Baseline für 3.36.0.
- **Je Lieferung:** Mac-Vollprüfung auf eingefrorener Kopie, kalibrierte sachlich ausführbare Linux-Matrix und native Windows-Vollprüfung (D35/D42), jeweils mit Version, Laufzeit und konkreten Ergebnis-/Artefaktverweisen. CI-Grundstufe vor jedem Commit. Für Remoteprüfungen darf ein vollständig lokal geprüfter Kandidat als Claude-Commit auf den Sprintzweig; nach grünen nativen Läufen sofortiger Liefercommit mit Nachweisen. Die geprüften Code-/Ressourcenhashes müssen dem Lieferstand entsprechen. UI-Prüfungen/Vollprüfungen/Messungen nacheinander ausführen. GitHub Actions ist für das Repository aktiviert und als nativer Windows-/Linux-Prüfstand verfügbar; damit ist noch kein Lauf bestanden.
- **Pflichtsuiten:** jede neue Pflichtsuite hat eine fachlich passende rote Gegenprobe gegen die unmittelbar vorausgehende Version aus §15.7. Zusätzlich absichtlich fehlerhafte Gegenfälle für kalibrierte Erwartungen; keine weicheren Erwartungen zur Verdeckung echter Fehler. Neue Fachlogik Tk-frei mit Unit-Tests (D17); echte UI-Einstiege ergänzend prüfen. Refactoring P05 wird über seine tatsächlichen Aufrufer und Paketregressionen geprüft.
- **Datenformat-Tore:** Ausgangsformat 23. Pixel-Frames und dauerhafte Importquellen brauchen Migration/Vorsicherung/Altleserschutz; die jeweils nächste Formatnummer wird beim tatsächlichen Formatschnitt vergeben. Vor Persistenz neuer Hinweis-/ICS-Einstellungen den Normalisierer und Altleser prüfen; bei verlustgefährdeten Feldern ebenfalls ein Format-Tor. Jede neue Fassung muss alte Bestände erhalten, die Vorversion den neuen Bestand schreibgeschützt öffnen und Originaldateien bytegleich lassen. Keine vorab erfundene Schemafolge als geprüft ausgeben.
- **Gestaltungstor erfüllt:** D41-Beurteilung der Logoentwürfe am 10.10.2026 als D45 erteilt: geglätteter Normalmaster plus breiterer Innenraum ausschließlich bei 16/32 px. Konkrete Vergleichstafeln im Grafik-Master; Übernahme in Paket 2. Keine erneute Auswahlfrage.
- **Menschenabnahme:** D42 trennt native Automatiken von tatsächlicher Bedienung, DPI/Mehrmonitor und Screenreaderproben. Die bestehende manuelle Prüfliste systematisch um neue Wege ergänzen; Termine/konkrete Prüffälle mit dem Inhaber abstimmen. Für N12 reichen Attributprüfungen und Screenshots nicht; tatsächliche VoiceOver-/NVDA-/Linux-Readerproben sind erforderlich. Fehlende Prüfstände oder nicht bestandene Proben präzise ausweisen, unabhängige Aufgaben weiterführen und betroffene Abnahme offen lassen.
- **Veröffentlichungstore:** nach D43 bleiben I1–I5/I9–I11 gesondert offen: Inhaberangaben, endgültige Glide-Lizenz, öffentliche Signaturen/Konten, Marke, systemweite Python-Installation, Fremdbildrechte, Historienumschreibung und öffentlicher GitHub-Auftritt. Der Sprint liefert Entwicklungsartefakte, keine öffentliche Releasefreigabe. Drittanbieter-Lizenzbelege für D27 gehören trotzdem zum Sprint. Keine Käufe, Historienumschreibung oder stillen Fremdbildlöschungen aus diesem Auftrag ableiten.
- **Abweichungen:** neue Produktfragen dem Inhaber vorlegen und unabhängig weiterarbeiten; technische Routineentscheidungen dokumentieren. Unerreichte Tempo-/Flächenziele mit Messbeleg vorlegen, Umfang nicht still verkleinern oder Punkte als erledigt markieren. Bei einem offenen Tor ist der betroffene Punkt offen, auch wenn andere Pakete geliefert sind.
- **Abschluss:** Plan ↔ Code ↔ Prüfergebnisse für jede S26-Kennung abgleichen; gewählte erste Stufen, alle Abweichungen, offene Menschen-/Veröffentlichungstore und native Nachweise ausdrücklich nennen. QA-Bericht, Funktionen und Übergabe fortschreiben; nach jeder Lieferung Claude-Commit. Reviewbarer Pull Request, Merge ausschließlich als Merge-Commit wegen der dokumentierten Commit-Verweise. Beim ersten Versionswechsel QA-Verweise 3.33.17 auf `6098877` festsetzen; 07-Hauptdatei ausführbar vormerken, Stash/`codex/`/Windows-Worktrees unangetastet lassen.

## 16. Vorschläge aus Wettbewerbs- und Open-Source-Analyse (13.10.2026)

**Status seit D49 (13.10.2026): beauftragt mit den empfohlenen Optionen.** Zunächst als Vorschläge vorgelegt; auf „bitte immer weiter machen bis alles umgesetzt ist“ legt D49 die Empfehlungen E-W1–E-W7 als Auftrag aus (Auslegung durch Claude, jederzeit korrigierbar). Reihenfolge: Abschluss 3.39.0 → FP-00 → Pakete 5–8 (§15.7) → übrige Pakete nach §16.7. Grundlagen: [Analyse §8](Glide_Analyse.md#8-bestandsaufnahme-und-gap-analyse-13102026) (Bestand, Gap), [Markt und Vorbilder §9](Glide_Markt_und_Vorbilder.md#9-wettbewerbs--und-open-source-analyse-13102026) (Wettbewerb, Codeanalyse, Featurematrix). Der Wunsch des Inhabers nach spürbarerem Produktnutzen (Arbeitsrichtung, 10.10.2026) ist Anlass; die empfohlenen Optionen sind seit D49 beauftragt; P3-Einträge mit Auslöser bleiben bis zu diesem offen.

### 16.1 Priorisierung

- **P0 – Kritisch:** Fehler, Datenintegrität, Stabilität, bestehende Kernfunktionen. Die erste Durchsicht fand keinen P0-Fehler; die Vorprüfung für FP-02 (§16.10) belegte **zwei reproduzierbare Fehler** im Lieferstand: Teilerkennung von Wiederholungsangaben in der Schnelleingabe (A29, WA-18) und abweichende Monats-/Jahresserien im ICS-Austausch (A28, WA-17), gebündelt als FP-00 und mit A30 (Zeitzonen im Aufgabenimport) als 3.39.1 geliefert. Daneben bleiben P0 die offenen Befunde W01/W06–W09 in §4.2; 3.39.0 ist seit 13.10.2026 geliefert, der Dokumentabgleich WA-13 erledigt.
- **P1 – Hoch:** deutlich spürbar im Alltag bei beherrschbarem Risiko.
- **P2 – Mittel:** wertvolle Erweiterung oder Optimierung.
- **P3 – Optional:** experimentell, größere Architektur, langfristig.

Bewertung je Eintrag: Nutzen, Aufwand (S bis 1, M 2–4, L mehr als 4 Arbeitstage, wie §4.3), technisches Risiko, Wartbarkeit. Geringer Aufwand mit hohem Nutzen geht vor; Prestige-Funktionen ohne belegten Alltagsnutzen sind ausgeschlossen. Jedes Paket wäre eine Produktionsversion nach §15.3.

### 16.2 Feature-Backlog

| ID | Titel | Problem (Fakt, Beleg) | Herkunft | Nutzen | Aufwand | Risiko | Wartbarkeit | Prio | Marke | Paket |
|---|---|---|---|---|---|---|---|---|---|---|
| WA-01 | Wiederholen nach Rückgängig | kein Redo in `ListApp`, nur in Text- und Zeicheneditor [Code] | Systemkonvention (P1); alle Vergleichsprodukte | hoch | M | mittel | gut | P1 | ▶ D49 | FP-01 |
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
| WA-16 | Wartbarkeitskennzahl je Lieferung | Größe von `ListApp` (rund 45.600 Zeilen) nirgends verfolgt [Code] | eigene Analyse | indirekt | S | – | besser | P3 | ○ | – |
| WA-17 | ICS-Austausch von Monats- und Jahresserien am Monatsende | Ausgabe `FREQ=MONTHLY`/`FREQ=YEARLY` für Termine am 29.–31. bzw. 29.02. ergibt in Kalenderprogrammen andere Termine als in Glide; Import einer Monatsserie am 31. legt zusätzliche Termine auf Monatsenden (A28) [Code][Probe] | eigene Vorprüfung | Korrektheit des Austauschs | S | gering | gut | P0 (Fehler, Randfall) | ✅ 3.39.1 geliefert | FP-00 |
| WA-18 | Wiederholungsangaben in der Schnelleingabe vollständig oder gar nicht erkennen | „monatlich am 15.“, „wöchentlich montags“, „alle 2 Wochen montags“ u. a. ergeben Serien ab heute, der Rest bleibt Titeltext; „jeden zweiten Dienstag“ ergibt nur einen Bearbeitungstag (A29) [Code][Probe] | eigene Vorprüfung | Korrektheit einer Kernfunktion | S–M | gering | gut | P0 (Fehler) | ✅ 3.39.1 geliefert | FP-00 |

**Geprüft und nicht vorgeschlagen:** vollständiger Block-Editor (Neubau des Seitenmodells, L+, Nutzen gezielt erreichbar), Whiteboard-Engine mit Formen/Freihand (Tk-Leinwand ohne Glättung; Produktgrenze), Datenbank-Baukasten und freie Felder (N15–N20), neue Beziehungsarten wie bei Vikunja (`links`/`blocked_by`/Unterpunkte genügen), Synchronisation/CRDT (G23), eingebaute Cloud-KI und BYOK (Produktgrenze), semantische Suche (Nutzen unbelegt, native Abhängigkeit), Daueralarm wie TickTick (widerspricht ruhiger Tagesführung), bezahlte Veröffentlichung wie Buildin (kein Ziel), Toolkit-Wechsel (§16.6).

### 16.3 Feature-Pakete

**Prinzipien-Check in Kurzform** ([Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md#prinzipien-check-für-neue-funktionen)); vor Umsetzung je Paket ausführlich in Funktionen und Plan eintragen.

| Paket | Vorgeschichte (0) | Ort (2) | Doppelung, was entfällt (3) | Dauerfläche bei 1280 × 800 (4) | Rücknahme (8) | Daten (9) | Tempo (10) |
|---|---|---|---|---|---|---|---|
| FP-00 | Fehlerbehebung, keine Produktentscheidung | Schnelleingabe, ICS-Ausgabe/-Import | keine | 0 px; Chip nennt zusätzlich den Ankertag | ein Undo wie bisher | nein (nur bestehende Arten) | – |
| FP-01 | nicht entschieden | Bearbeiten-Menü, Palette, Kürzel, Rückgängig-Hinweis | keine; ergänzt Rückgängig | 0 px (Hinweis zeigt nur bei Bedarf „Wiederholen“) | ist selbst Rücknahme | nein | Speicher messen |
| FP-02 | Wiederholungen bestehen; Erweiterung nicht entschieden | Inspektor, Schnelleingabe | zweiter Rechner entfällt intern (A26) | 0 px | ein Undo je Änderung | Formattor | Budget im Rechner |
| FP-03 | gespeicherte Filter bestehen; eigene Felder ✕ bleibt | Filterdialog, Kachel, Palette | Bedingungen in einem Modul | 0 px | ein Undo je Ziehen | Einstellungen additiv, eigener Schlüssel auf oberster Ebene | ≤ 100 ms bei 10.000 |
| FP-04 | Zeichnungskarten bestehen (ZF-100); freie Zettel ✕ bleibt | Pinnwand, Seitenleisten-Kontextmenü | keine neue Art | 0 px | Flächenstapel | Einstellungen additiv (WA-09) | Auszug je Aufbau gecacht |
| FP-05 | nicht entschieden | Rückverweisbereich der Seite, eingeklappt | keine | 0 px (eingeklappt) | ein Undo | nein | nur beim Aufklappen |
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

Nummeriert nach dem bewährten Muster (Übergabe §4); Kurzantwort etwa „E-W7 A, E-W1 A/V, E-W2 A/1“. Die empfohlenen Optionen sind durch D49 beauftragt; neue abweichende Entscheidungen werden ab D50 in der Arbeitsrichtung eingetragen.

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
| AE-6 | Toolkit-/Framework-Wechsel | Qt (PySide6), Web (Electron/Tauri), Flutter | kein Wechsel | Nutzen (Kantenglättung, reichere Editoren, Zugänglichkeit) teils über Tk 9/9.1 erreichbar (SVG/PNG, Paket 8); Kosten: Neubau der rund 59.500 Zeilen in `app.pyw`, die überwiegend an Tk gebunden sind, Verlust der geprüften Tk-Lösungen und Suiten, neue Abhängigkeiten. D03/Q4 bleiben; Neubewertung nur, wenn Paket 8 scheitert oder D03 aufgehoben wird |
| AE-7 | Speicher | JSON (D16) · SQLite · CRDT (Yjs/yrs) | JSON | CRDT dient bei AFFiNE/AppFlowy der Synchronisation (G23 ✕); Logseq-Beta zeigt das Risiko eines Speicherwechsels |

### 16.7 Empfohlene Reihenfolge

Nach Abschluss des bestätigten Sprints (4.0.0), je Zeile eine Produktionsversion; Versionsnummern und Formatnummern vergibt der jeweilige Lieferweg.

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
| FP-01 | ausreichend; Einstiegsinventar erstellt (38 + 32 Stellen), Gültigkeitsregel festgelegt | Stapelregeln in `undo_history.py` herauslösen, Schreibzähler in `save_items` | E-W1 A/V durch D49; Strg+Y gemäß Systemkonvention | nein | Einstiegsmatrix aller Rückgängig-Wege mit Bytevergleich |
| FP-02 | ausreichend; Beispieltabelle der Eingabesprache gegen `ics_recurrence` geprüft (§16.10) | `repeat_rules.py` als Fassade über `ics_recurrence.py`; alte Arten rechnen weiter selbst (Monatsende-Anker weicht von RFC ab) | E-W2 A/V durch D49; Formatnummer beim Schnitt | ja | Referenztermine aus unabhängiger Rechnung (Werkzeug liegt vor), Altleser-Kindprozess |
| FP-03 | Stufe 1 ausreichend; Stufe 2 braucht Bedienentwurf des Dialogs | – (eigener Einstellungsschlüssel) | E-W4 A/V durch D49 | Einstellungen additiv | Referenzbestand für Filtertreffer, Messung |
| FP-04 | ausreichend | WA-09 | E-W5 durch D49 gemäß §16.5 | nein | Pinnwand-Altleser, Messung mit 200 Karten |
| FP-05 | ausreichend | – | E-W5 durch D49 gemäß §16.5 | nein | Treffer-/Fallen-Fixture |
| FP-06 | ausreichend; Austauschweg geprüft (`instructions` vorhanden, Erstellen nur über Stufe 1) | – | E-W3 A durch D49; kein lokaler KI-Endpunkt | nein | Musterantworten je Auftrag, beide Stufen |
| FP-07 | Stufe 1 ausreichend | gemeinsame Markdown-Regeln mit Paket 6 | E-W5 durch D49 gemäß §16.5 | nein | Showcase-Rundlauf, Linkauflösung, Canvas-Schema |

**Umsetzungsfolge nach D49:** FP-00 ist als 3.39.1 geliefert. Die übrigen beauftragten Pakete folgen nach Abschluss 4.0.0 gemäß §16.7. FP-05, FP-06 und WA-12 sind ausreichend spezifiziert; FP-01 braucht einen kleinen Extrakt. Vor Stufe 2 von FP-03 ist der Bedienentwurf des Dialogs vollständig zu spezifizieren. Bereits durch D49 gewählte Optionen brauchen keine erneute Auswahl.

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
