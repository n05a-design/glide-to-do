# Glide – Entwicklungsplan und Aufgabenstand

Stand 10.10.2026 · Glide 3.36.0 · Aufgabenformat 23

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
| 0 Fundament | Performance P01–P09, T2, CI | ◐ Ziele für Abhaken und Suche erreicht (3.33.19, 3.34.0); offen P03-Rest, P05, Linux-Kalibrierung der Integrationssuiten |
| 1 Klarer Alltag | Bereiche, Startseite, Eingabe, Eisenhower, Heute/Demnächst, UX1, Fokus, Komfort, Tag, Oberfläche Welle 1 | ◐ geliefert bis 3.33.21; offen Welle 2 nach I7 (OB02, OB03-Rest, N05 mit KO04), AU03-Hinweise, OB04, AU07 |
| 2 Wissen im Kontext | Suche, Verweise, Live-Liste, Titelbild, Kalender mit Wochenplanung, Bilder in Seiten, Filter erklären | ◐ geliefert 3.33.7–3.34.0; offen N05 (Inspektor) |
| 3 Pixel | Palettenbearbeitung, Symbolvorschau, Animation | ◐ G19, G-03 ✅ 3.35.0; G17 ausgewählt durch D18, Umsetzung im neuen Sprint offen |
| 4 Austausch und Verteilung | KI-Austausch Stufe 2, Import, Sicherungsvergleich, Paket mit eigenem Python | ◐ G24, F-03 ✅ 3.35.0; G21 und G26 durch D26/D27 ausgewählt; Umsetzung offen |
| 5 Zukunft (4.x) | Screenreader (Tk 9.1), Seitenversionen, SQLite nur nach D16-Neubewertung | ◇ |

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
| P03 | Aufbau und Layout | ◐ Bibliothekskarten 3.32.3, Startseite 3.33.2, unveränderte Kacheln bleiben 3.33.19 (P03r). Ausbau vollständig gewählt (D33/S26-14): Elemente geänderter Karten, sehr viele Karten, Neuaufbau der Startseite (270–300 ms) |
| P04 = A-02 | Bildlayout nur bei geänderter Geometrie, Platzieren beim Scrollen | ✅ 3.33.19 |
| P05 | Gemeinsame Helfer | ◐ Hover 3.32.2; gezielt gleiche Texte/Abläufe im Sprint-Code gewählt (D40 A/1) |
| P06r = A-03 | Doppelte Refresh-/Schreibanforderungen je Aktion | ✅ 3.33.19 |
| P07 | Volltextsuche als ersetzbarer FTS5-Cache | ✕ nach Messung 3.34.0: 66,6 ms Median bei 10.000 Punkten (Regel: unter 100 ms kein Index) |
| P08a/P08b | Ein Vergleichsdurchlauf für Verlauf und Aktivität; nur geänderte Listen vergleichen, Vollvergleich im Autosave | ✅ 3.33.9 / 3.33.11 |
| P08c | Abhaken bei 5.000 Punkten ≤ 120 ms | ✅ gemessen 3.33.19: 61 ms |
| P09a/P09b | Tabelle ohne Listenspaltenmessung; Kennzahlen, Datum und Schriftmaße einmal je Aufbau | ✅ 3.33.0 / 3.33.10 |
| T2 | Gemeinsame Formatsicherung | ✅ 3.33.0; Windows-Signatur 3.33.7, Inhaltsvergleich 3.33.8 |
| E01 | Einblendung des Einstellungsfensters | ◐ erster Ausbau 3.33.19 (≈ 560 ms); Erst-/Folgeaufbau vollständig gewählt (D34/S26-14b) |
| CI | CI-Grundstufe (Linux/Xvfb) | ✅ 01.10.2026; gesamte ausführbare Linux-Matrix gewählt (D35/S26-15), Umsetzung offen |

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

**Fertig, wenn:** Kopfzeile ≤ 4 Symbolknöpfe ✅; kein Symbol mit zwei Bedeutungen ✅ (Bewegungspfeile ausgenommen); Bedienfläche über dem Inhalt ≤ 15 % bei 1280 × 800 – offen (zuletzt ≈ 27 %, nach U09/OB05 nicht neu gemessen).

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
| LG01 | Logo-Rückfall unter Tk 8.6 geglättet (Weg B der [Diagnose](../01_Repository/Glide/docs/diagnosen/LOGO_KANTENGLAETTUNG.md)) | ○ E-S6 |
| LG02 | App-Symbol in 16, 32, 64 und 256 px vorrechnen, unter Tk 8.6 direkt laden; `glide-logo.png` und Modulkopf von `logo.py` berichtigen (Wege C und F) | ○ E-S6; nur in einer Produktionsrunde |
| LG03 | `test_logo330` verlangt Zwischentöne an der Logokante (Weg D) | ○ E-S6 |
| LG04 | Logo-Master überarbeiten (Weg E; [Befunde](../20_Grafik_Master/README.md#befunde-am-logo-master-05102026-entscheidung-beim-inhaber)) | ▶ vollständig ausgewählt D41; Entwürfe vor Übernahme beurteilen |
| W01 | Seitenleistentitel unter Windows/Tk 9 rechts um etwa ein Zeichen angeschnitten; `sidebar_available_text_width` mit dem gezeichneten Platz abgleichen | ○ Sichtprüfung B1, dann Produktionsschnitt |
| W02 | Dunkeltests über `set_design` statt `theme_name` | ◐ umgestellt 08.10.2026, auf dem Mac in den Volläufen 3.33.19–3.35.0 grün; Windows-Nachprüfung offen |
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
| OB02 | Vier Textstufen; Kopf von „Heute“ zeigt nächste Aufgabe, verfügbare Zeit und Fortschritt als stärkstes Element | 860 × 700, große Schrift; jede Angabe genau einmal | M | ▶ vollständig ausgewählt D22; Umsetzung offen |
| OB03 | Zeilenaktionen nur bei Bedarf (Einplanen, Termin, „…“ beim Überfahren und bei Auswahl) | jede Aktion auch über Tastatur, Kontextmenü, Palette; Bedienfläche ≤ 15 % | M | ◐ Kalenderaktion 3.33.13; Rest vollständig ausgewählt D23; Umsetzung offen |
| OB04 | Dezente Bewegung beim Abhaken, Klappen und Bereichswechsel (≤ 150 ms), nur mit Animationen | keine messbare Verschlechterung der Ziele aus §10 | M | ▶ vollständig ausgewählt D31; Umsetzung offen |
| OB05 | Schmale Seitenleiste mit Symbolen | Zustand gemerkt; Tastatur; 860 × 700 | M | ✅ 3.33.21 |
| OB06 | Gestaltungsabnahme je Paket: Vorher-/Nachher-Fensterbilder, vom Inhaber bewertet; Bilder lokal und unversioniert | Entscheidung im QA-Bericht vermerkt | S je Paket | ◐ Bewertung durch den Inhaber offen |

#### B. Komfort im täglichen Gebrauch

| ID | Paket | Abnahme (Auszug) | Aufwand | Stand |
|---|---|---|---|---|
| KO01 | Ein Menü „Einplanen“ (Heute, Morgen, Wochenende, Nächste Woche, Datum …, Ohne Tag) für die Mehrfachauswahl | ein Undo-Schritt; Fälligkeit bleibt | S–M | ✅ 3.33.13 |
| KO02 | Wiederholungen: Termin überspringen, verpasste Termine überspringen | Serie bleibt; ein Undo-Schritt | S | ✅ 3.33.20 |
| KO03 | Erinnerungen in der Schnelleingabe als Chip | Chip nennt „nur bei laufender App“ | S | ✅ 3.33.20 |
| KO04 | Felder am Objekt: Klick auf Termin, Wichtigkeit oder Label öffnet die kleine Auswahl dort | ein Undo-Schritt; einheitlich mit N05 | M | ▶ vollständig ausgewählt D25; Umsetzung mit N05 offen |
| KO05 | Mehrzeiliges Einfügen in die Eingabezeile nach Rückfrage | ein Undo-Schritt | S | ✅ 3.33.20 |
| KO06 | Zuletzt benutzte Ziele zuerst bei „Verschieben nach …“ und Labels | keine neue Einstellung | S | ✅ 3.33.20 |

#### C. Unterstützung im Alltag

| ID | Paket | Abnahme (Auszug) | Aufwand | Stand |
|---|---|---|---|---|
| AU01 | Tagesvorschlag „Was passt heute?“ mit Grund je Zeile | deterministisch; nichts ohne Bestätigung; ein Undo-Schritt | M | ✅ 3.33.14 |
| AU02 | Verfügbare Zeit in allen Planungswegen | eine Rechenstelle (`planning_summary`) | S–M | ✅ 3.33.13 |
| AU03 | Geführter Tagesbeginn (Rückblick → Vorschlag → Zeitblöcke) und optionaler Hinweis zu Tagesbeginn/-abschluss | Hinweise nach D20 | M | ◐ geführter Weg 3.33.14; Hinweise ausgewählt 10.10.2026, Umsetzung offen |
| AU04 | Wochenplanung im eingebetteten Kalender mit Kapazitätsbalken | Teil von N04 | M | ✅ 3.33.17 |
| AU05 | Fokussitzung mit nächster Aufgabe (= G05) | Zeit genau einmal gebucht | M | ✅ 3.33.14 |
| AU06 | Routinen als Abschnitt in „Heute“ | kein Formatwechsel | M | ✅ 3.33.20 |
| AU07 | Termine aus einer ICS-Datei als belegte Zeit im Stundenraster | berührt die Produktgrenze „ICS ist Dateiaustausch“ | M–L | ▶ vollständig ausgewählt D30; Umsetzung offen |

**Fertig (Programm), wenn:** Ein Tag lässt sich aus „Heute“ in höchstens drei Schritten planen ✅ (3.33.14); die verfügbare Zeit ist überall sichtbar, wo geplant wird ✅ (3.33.13); die Oberflächenziele aus §10 sind erreicht – offen (Bedienfläche); der Inhaber hat jede Welle gestalterisch abgenommen (OB06) – offen.

### 4.4 Größere Umsetzungspakete (Auftrag 07.10.2026)

Der Inhaber beauftragt mehrere zusammengehörige Features je Umsetzung, abgeleitet aus Analyse, Recherche und Konkurrenzdokumenten; innerhalb dieses Auftrags braucht es keine erneute Freigabe jeder Teilfunktion. Offene Produktentscheidungen bleiben offen. Geliefert als 3.33.14–3.33.18 und im Sprint 3.33.19–3.35.0 (§14).

**Prüfstrategie pro Paket:** gezielte Baselines der betroffenen Bereiche vor Produktionsänderungen; Unit-Tests und echte Bedienwege je Teilfunktion; eine Pflichtsuite mit Gegenprobe gegen die Vorversion; ein gemeinsamer eingefrorener Volllauf mit vollständiger Regression, Interaktions-/Fehler-/Undo-/Neustartprüfung, Mindestgröße, großer Schrift, hell und dunkel sowie Messung. Erst danach Python, Showcase und Bundle liefern. Weitere Vollläufe nur nach ausführbaren Änderungen oder einem Fehlerbefund; keine künstlichen Zwischenversionen. Native und menschliche Abnahme getrennt ausweisen.

## 5. Wissen im Kontext (Stufe 2)

| ID | Arbeit | Stand |
|---|---|---|
| N05 = U12 | Ein Inspektor statt Maske + Detailbereich | ▶ vollständig ausgewählt D22; Umsetzung offen |
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
| G17 = G-02 | Animation: Frames, Dauer, Vorschau | ▶ E-S1 A/V durch D18 entschieden 10.10.2026; Umsetzung offen |
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
| Startseite aufbauen | ≤ 150 ms | ◐ unverändert 0,3 ms, Neuaufbau 270–300 ms (Referenz-Mac, 3.33.19; Grenze Tk-Zeichnen) |
| Tabellenansicht öffnen, 5.000 Punkte | ≤ 400 ms | 292 ms (Linux, Messung zu T8); seit P09a nicht als Ganzes neu gemessen |
| Kopfzeilen-Symbolknöpfe | ≤ 4 | ✅ seit 3.33.16 |
| Bedienfläche über Inhalt (1280 × 800; 840 zusätzlich) | ≤ 15 % | ○ zuletzt ≈ 27 %; nach U09/OB05 neu messen |
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
| I6 | Windows-Vollprüfung des aktuellen Stands und manuelle Prüfsitzungen | ▶ Windows je neuer Lieferung gewählt (D42); zuletzt geprüft 3.33.18. Tatsächliche Sicht-/Bedien-/Readerabnahme getrennt nach der [Prüfliste](Glide_Manuelle_Pruefung.md) |
| I7 | Referenzentwürfe für „Heute“, Liste, Seite und Inspektor | ▶ drei Entwürfe vorbereitet; Bild 1 und vier Funktionen vollständig gewählt (D19, D21–D25) |
| I8 | Lösungsweg für das Logo unter Tk 8.6 (LG01–LG04) | ▶ technische Wege B+C+D+F vollständig (D28), Master/Kleingrößen vollständig (D41); Entwurfsbeurteilung vor Übernahme offen |
| I9 | Rechte an Fremdbildern im öffentlichen Repository (`20_Grafik_Master/05_Inspiration`, `06_Beispielbilder`, die sechs Showcase-Motive) | ○ behalten mit Rechtenachweis oder entfernen und den Showcase mit eigenen Motiven neu erzeugen; Empfehlung: ohne Nachweis entfernen |
| I10 | Git-Historie bereinigen (gelöschte Protokolle mit Benutzerpfaden, frühere Archivkopien) | ○ eigener Auftrag; ändert alle Commit-Kennungen ([Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md#github-auftritt)) |
| I11 | GitHub-Auftritt: Beschreibung, Tags, Wiki, Issues, KI-Codeprüfung | ○ Empfehlungen in der [Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md#github-auftritt) |
| A–H | Bearbeitungstiefe der Auswahl vom 30.09.2026 (A Tempo · B Planen und Fokus · C Aufgaben im Text · D Suchen und Wissen · E Projektseiten · F Austausch und Sicherungen · G Pixel-Werkstatt · H Bedienkontrolle und Auslieferung) | beauftragte Teile umgesetzt (Aufgaben A-01 bis H-03 mit Status oben); weitere Tiefe je Richtung entscheidet der Inhaber |

**Entscheidungen und Auswahlstand** (Stand 10.10.2026; Empfehlungen sind keine Entscheidungen):

| Nr. | Frage | Blockiert | Empfehlung |
|---|---|---|---|
| E-S1 | D07: Animationsexport | G17 | entschieden 10.10.2026: A/V, D18; Umsetzung offen |
| E-S2 | I7: Referenzweg und Auswahl der vier Oberflächenfunktionen | OB02, OB03-Rest, N05, KO04 | Referenzweg und Bild 1 entschieden (D19/D21); vier Funktionen vollständig gewählt (D22–D25) |
| E-S3 | AU03: Vorgabe und Tiefe automatischer Tageshinweise | AU03-Rest | entschieden 10.10.2026: A/V, D20; Umsetzung offen |
| E-S4 | G21: erste Importquelle | G21 | entschieden 10.10.2026: Notion A/V, D26; Umsetzung offen |
| E-S5 | D15/G26: Bauwerkzeug | G26, N12 | entschieden 10.10.2026: PyInstaller 6.22.3, beide Zielsysteme A/V, D27 |
| E-S6 | I8: Logo-Rückfall unter Tk 8.6 | LG01–LG04 | B+C+D+F vollständig gewählt (D28); Master LG04 vollständig gewählt (D41), Gestaltungsabnahme offen |
| E-S7 | A14: Symbolschrift | einheitliche Symbolgröße | Systemzeichen, gesamte Tabelle gewählt (D29) |
| E-S8 | AU07, OB04 | AU07, OB04 | beide A/V entschieden (D30/D31); Umsetzung offen |

## 12. Pflege

- Bei jeder Produktionsrunde Statusmarken, Abschnitt 2 und die Ziele nachführen; nach der Lieferung Zwischenstände löschen (Git trägt sie). Keine datierte Kopie.
- Neue Ideen erst nach dem [Prinzipien-Check](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md#prinzipien-check-für-neue-funktionen) und mit Marke aufnehmen.
- Neue Entscheidungen gehören in die [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md), nicht hierher.

## 13. Abgleich mit dem ursprünglichen Zukunftsdokument

Original vollständig aus der Git-Historie gelesen: „Glide – KI-Austauschformat und Zukunftsarchitektur“, frühere Datei `00_Arbeitsvorbereitung/Archiv/Glide_KI_Austauschformat_und_Zukunftsarchitektur_Dublette_2026-09-18.md`, Commit `569020ef65880b28a50408e229a8027ba2a65898`. Die späteren namensähnlichen Fassungen waren nur Verweise. Die ursprünglichen Beispiele beziehen sich auf Format 15 und sind keine aktuellen Formatverträge. [Original in Git](https://github.com/n05a-design/glide-to-do/blob/569020ef65880b28a50408e229a8027ba2a65898/00_Arbeitsvorbereitung/Archiv/Glide_KI_Austauschformat_und_Zukunftsarchitektur_Dublette_2026-09-18.md).

| Ursprüngliche Idee | Heutiger Code / Entscheidung | Konsequenz |
|---|---|---|
| Internes Format, Exchange und KI-Beschreibung trennen | `DATA_SCHEMA_VERSION = 23`, `EXCHANGE_FORMAT_VERSION = 1` (Änderungsvorschläge 2), `exchange_manifest`, erzeugte Spezifikation vorhanden | ✅ Grundlage erhalten; neue Funktionen nicht automatisch zum Exchange-Vertrag erklären |
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
| 0 | W02 | Tests auf `set_design` umstellen (Dunkelfälle wirklich dunkel) | P2 | – | ◐ Mac ✅ (Volläufe 3.33.19–3.35.0 grün, Dunkelfall mit Luminanzprüfung); Windows-Nachprüfung offen |
| 0 | W03 | Zeilenenden für die ganze Ablage festlegen | P3 | – | ✅ 08.10.2026 |
| 0 | W04 | CI-Wächter gegen Synchronisationskopien und geschrumpfte Hauptdokumente | P2 | – | ✅ 08.10.2026 |
| 0 | W12 | Lieferabsatz in `07_Python-Versionen/README.md` nicht vergessen (Befund A15) | P3 | – | ✅ 09.10.2026: `abgleich_07.py` bricht ab, solange die README die gelieferte Hauptdatei nicht nennt; Reihenfolge in `scripts/pflege/README.md` |
| 0 | W13 | Standprüfung R10: die README in `07_Python-Versionen` folgt den Modulen dieses Ordners, nicht dem Quellbaum (CI zwischen zwei Lieferungen sonst rot) | P2 | – | ✅ 09.10.2026, Werkzeugtest ergänzt |
| 0 | W14 | Altleser-Proben mit Vorversionen außerhalb der Aufbewahrung (Befund A18) | P1 | – | ✅ 09.10.2026 `tests/integration/vorversion.py` |
| 0 | W15 | Sperrdatei-Zählung in `test_tempo33319` unabhängig vom Sekundenwechsel (Befund A19) | P2 | – | ✅ 09.10.2026 |
| 0 | DOK3 | Dokumentation inhaltlich nachführen (Analyse A02–A13) | P2 | A01 | ✅ 09.10.2026 (A02–A13 erledigt, laufend mit A15–A22; A14 wartet auf E-S7, §11) |
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
| S26-01 / OB02, E-S2 | Heute ohne ausgeprägte Hierarchie → nächste Aufgabe, Zeit und Fortschritt schnell erfassen | vollständig nach D22: Heute-Kopf und vier Textstufen in Heute, Listen, Seiten und Inspektor; M–L | Bild 1 (D21); N05 für Inspektor | jede Angabe einmal, feste Kanten; 860 × 700 und große Schrift; alle gewählten Ansichten erfasst | echte Bedienwege, Geometrie, Kontrast, Vorher/Nachher; Gegenprobe gegen Vorversion | ▶ ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-02 / OB03, E-S2 | nur Einplanen bedarfsabhängig → weitere Zeilenaktionen erreichbar und ruhig | vollständig nach D23: Einplanen, Fälligkeit und „…“ bei Hover/Auswahl in Liste, Tabelle, Heute und Demnächst; M–L | Bild 1; S26-13 gemeinsam ausgewählt | Tastatur, Kontextmenü und Palette gleichwertig; keine Fokusverluste; alle vier Ansichten | Hover/Auswahl/Fokus, Aktion über stabile ID, Flächenmessung; Gegenprobe gegen Vorversion | ▶ ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-03 / N05, E-S2 | Maske und Detailbereich doppelt → eine verlässliche Bearbeitungsfläche | vollständig nach D24: gemeinsamer Inspektor in Liste, Tabelle, Heute, Demnächst, Pinnwand und Dokumentverweisen; bei schmalem Fenster in Inhaltsfläche; L | Bild 1; Grundlage für KO04 | alle bisherigen Felder und Einstiege erhalten; ein primärer Editor; Undo, Abbruch, Auswahl und Schreibschutz konsistent | Feld-/Einstiegsmatrix aller Kontexte, Fokus, Neustart, große Schrift; Gegenprobe gegen Vorversion | ▶ ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-04 / KO04, E-S2 | häufige Felder erfordern Umweg → direkt am Objekt bearbeiten | vollständig nach D25: Bearbeitungstag, Fälligkeit, Wichtigkeit und Labels im Inspektor und an sichtbaren Aufgabenfeldern in Liste, Tabelle, Heute, Demnächst, Pinnwand und Dokumentverweisen; L | S26-03 (D24) | identische Fachlogik; D01/D02; je Änderung ein Undo; Positionierung, Fokus und Abbruch konsistent | Maus/Tastatur, alle Kontexte und Felder, Abbruch, Neustart; Gegenprobe gegen Vorversion | ▶ ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-05 / AU03, E-S3 | Tagesbeginn/-abschluss nur manuell → optional rechtzeitig erinnern | A/V nach D20: Vorgabe aus, 08:30/17:30; Uhrzeiten/Wochentage, später erinnern, heute überspringen, gesammelte verpasste Hinweise; M | D20 entschieden; Gesamtplan offen | nur bei laufender App; kein Zwangswechsel, keine Mehrfachzustellung je Termin; Einstellungen und Zustellzustand bleiben über Neustart erhalten | Tk-freie Zeit-/Zustelltests mit künstlicher Uhr; Tageswechsel, Neustart, modaler Zustand; echte Bindungen; Gegenprobe gegen Vorversion | ▶ ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-06 / AU07, E-S8a | freie Fenster berücksichtigen nur Glide → lokale Termine als Belegzeiten berücksichtigen | A/V nach D30: gewählte ICS-Datei lesend; Einzel-/ganztägige Termine, übliche tägliche/wöchentliche/monatliche/jährliche Serien und Ausnahmen, Zeitzonen/Sommerzeit, transparent/storniert; L | begrenzte ICS-Erweiterung durch D30; planning_summary | Überlappungen nicht doppelt zählen; keine Aufgaben/Synchronisation; nicht unterstützte Regeln sichtbar melden; alle Planungswege verwenden gleiche Bilanz | Tk-freie ICS-/Serien-/Zeitzonentests; Fixtures, Randtage, Sommerzeit, Überlappung, Ausnahmen; echte Planungswege; Gegenprobe gegen Vorversion | ▶ ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-07 / OB04, E-S8b | Zustandswechsel abrupt → dezente optionale Rückmeldung | A/V nach D31: Abhaken, Klappen, Bereichswechsel bis 150 ms, unterbrechbar; M–L | D31; Tempoziel vor/nach | Animationsoption beachten; keine zurückbleibenden after-Aufträge; schnelle Folgen sauber abbrechen; keine Zielverschlechterung | Zeit-/Abbruchlogik Tk-frei; echte schnelle Folgeaktionen, Fokus, Messen, Animationen aus; Gegenprobe gegen Vorversion | ▶ ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-08 / G17, E-S1/D07 | statische Zeichnungen → begrenzte Pixelanimation | A/V nach D18: Frames anlegen/duplizieren/löschen/umordnen, gemeinsame und einzelne Dauer, Vorschau, PNG-Spritesheet und Einzelbildfolge; kein GIF; L | D18 entschieden; nächstes Datenformat-Tor; Gesamtplan offen | Altzeichnungen erhalten; Vorsicherung/Migration/Altleser; Vorschau und Exporte entsprechen den Frames; jede Bearbeitung rücknehmbar; Reihenfolge und Dauer über Neustart erhalten | Tk-freie Frame-/Exporttests; echte Werkzeuge, Exportdateien, Undo, Altleser; Gegenprobe gegen Vorversion | ▶ ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-09 / G21, E-S4 | generischer Dateiimport → erste Fremdquelle kontrolliert übernehmen | Notion A/V nach D26: ZIP, Text/Überschriften/Listen, lokale Bilder/Anhänge, Aufgaben-Kästchen und interne Seitenverweise; Vorschau und Verlustbericht; L | D26; vorhandener Markdown-Import und lokale Verweise | nichts still verlieren oder überschreiben; keine Notion-Datenbank; Unterseiten in bestehende Ordner/Seiten; sichere Größen-/Pfadgrenzen; ein Undo und Vorsicherung | Tk-freie Parser-/Archivtests; künstliche Exportpakete, fehlerhafte Archive, Quellverluste, Abbruch, Undo, Neustart; Gegenprobe gegen Vorversion | ▶ ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-10 / G26, E-S5/D15 | installiertes Python nötig → eigenständig startende Pakete | A/V nach D27: PyInstaller 6.22.3 nur zum Bauen; Python 3.14/Tk 9; macOS arm64 und Windows x64, vollständige Ressourcen, Lizenzbelege und Bauanweisungen; L | native Mac-/Windows-Bau- und Prüfumgebung; I3 für öffentliche Signatur | Start ohne externes Python; Daten außerhalb Paket; Ressourcen/vendor vollständig; Version/Architektur nachvollziehbar; Signaturstatus ehrlich ausgewiesen | native isolierte Start-/Ressourcen-/Datenproben, Hash und Signatur; Gegenprobe: Vorversion benötigt externes Python | ▶ ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-11 / LG01–LG03, E-S6/I8 | Tk-8.6-Logo treppig und großes PNG → geglätteter Rückfall und richtige Symbolgrößen | A/V nach D28: Wege B+C+D+F; Glättung, App-Symbole 16/32/64/256, Tests und Dokumentation; M–L | D28; Master LG04 nach D41, Gestaltungsabnahme offen | Zwischentöne und korrekte Größen bei wechselndem DPI/Akzent; Tk 9 bleibt erhalten; kein großes PNG im Startweg | Tk-freie Raster-/PNGtests; Bildwerte, Tk 8.6/9, Startmessung, native Sichtprüfung; Gegenprobe gegen Vorversion | ▶ ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-12 / A14, E-S7 | Ersatzschriften für einige Symbole → einheitliche und eindeutige Zeichen | A/V nach D29: gesamte ICONS-Tabelle mit Zeichen aus tatsächlich verwendeter UI-Schrift; Größe/Ausrichtung/Bedeutung; M | D29; native Plattformprüfung | nur ICONS; keine zusätzliche Symbolschrift; keine Mehrfachbedeutung; Beschriftung und Tastaturwege erhalten | Symbolprüfung je Plattform, Schrift-/DPI-Wechsel, Kontrast und Sichtabnahme; Gegenprobe für belegte Ersatzschriftfehler | ▶ ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-13 / Bedienfläche ≤ 15 % | zuletzt ≈ 27 %, seit U09/OB05 ungemessen → Inhalt gewinnt Fläche | A/V nach D32: Liste, Heute, Tabelle, Demnächst, Seiten, Pinnwand messen und dauerhafte Bedienfläche über Inhalt reduzieren; M–L | OB02/OB03/N05; D32 | ≤ 15 % bei 1280 × 800 nach P4; 840 zusätzlich berichten; alle Wege erhalten; 860 × 700/große Schrift erreichbar und lesbar | nachvollziehbare Geometriemessung je Ansicht; große Schrift, Tastatur und Auffindbarkeit; Gegenprobe gegen Vorversion | ▶ ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-14 / P03-Rest | geänderte Karten teuer, Startseite 270–300 ms → weniger Aufbau | A/V nach D33: Teilaktualisierung geänderter Karten, viele Karten und Startseiten-Neuaufbau; L | gemessene Baseline; D33 | unveränderte Widgets erhalten; Auswahl/Fokus/Scrollen stabil; Startseite warm ≤ 150 ms; Kalt-Ausnahme D46 ≤ 300 ms direkt/≤ 500 ms Kindprozess, Messbeleg | warm/kalt, Median/p95, 1.000/10.000 Punkte, Widget-/Speicherentwicklung; Gegenprobe gegen Vorversion | ▶ umgesetzt; endgültige Messung nach D46/D47 und eingefrorene Mac-Vollprüfung grün; native Abnahme/Lieferabschluss offen |
| S26-14b / E01-Rest | Einstellungen ≈ 560 ms → schnellerer erster/wiederholter Zugang | A/V nach D34: sichtbare Bereiche zuerst, wiederverwendbare Bereiche erhalten; M–L | eigene Baseline; D34 | erste Anzeige ≤ 250 ms, erneut Median ≤ 150 ms/p95 ≤ 170 ms nach D47; Werte aktuell; keine Rückrufe nach Schließen; Abweichungen ausdrücklich klären | getrennte Erst-/Folgeserien, Median/p95, Themen-/Schriftwechsel, Schließen/Öffnen, Fokus und Lebensdauer; Gegenprobe gegen Vorversion | ▶ umgesetzt; endgültige Messung nach D46/D47 und eingefrorene Mac-Vollprüfung grün; native Abnahme/Lieferabschluss offen |
| S26-15 / Linux-CI | nur Grundstufe verpflichtend → kalibrierte Integrationssuiten | A/V nach D35: gesamte sachlich ausführbare Linux-Matrix verpflichtend; L | Linux mit tkinter/Xvfb; native CI-Ausführung | echte Befunde nicht wegkalibrieren; Plattformfälle ausdrücklich benennen; neue Sprintwege eingeschlossen | native Linux-Läufe, absichtlich fehlerhafte Gegenfälle, CI-Nachweis und rote Vorversion für neue Pflichtsuiten | ◐ Matrix eingerichtet; native Linux-Vollprüfung und sieben passende Defektgegenproben an `6a2cebe` grün; neue Sprint-Suiten künftig ergänzen |
| S26-16 / N12 | Screenreader-Kernabläufe fehlen → Tk-9.1-Zugänglichkeit | A/1 nach D36: Aufgaben erfassen, suchen, Heute planen, Inspektor; L | S26-10; eigens geprüfte Tk-9.1-Laufzeit; native Screenreader | Rollen/Namen/Werte/Zustände; Auswahl/Fokus; kompletter gewählter Kernablauf tatsächlich bedienbar; übrige Arbeitsbereiche ausdrücklich außerhalb | Tk-9.1-Proben plus VoiceOver/NVDA/Linux-Screenreader-Abnahme; Tastatur/Undo/Neustart; Gegenprobe gegen Vorversion | ▶ erste Stufe ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-17 / N13 | Sicherungen nur insgesamt vergleichbar → einzelne Seite wiederherstellen | A/V nach D37: bestehender Sicherungsvergleich mit Vorschau; Text, Bilder/Anhänge, Aufgabenverweise, Live-Listen; L | Sicherungs-/Verweis-/Anhangsregeln; D37 | andere Seiten unverändert; IDs/Verweise konsistent; fehlende Ziele vorab; Vorsicherung und ein Undo; kein neues fortlaufendes Versionssystem | Tk-freie Wiederherstellungsplanung; Sicherungs-Fixtures mit Bildern/Live-Listen, fehlende Ziele, Neustart/Undo; Gegenprobe gegen Vorversion | ▶ vollständig ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-18 / V01, neuer Vorschlag | Überplanung nur angezeigt → ausgewählte Aufgaben direkt entlastend umplanen | A/V nach D38: Heute, Woche, Tagesvorschlag; Auswahl, anderer Tag/Vorrat, Vorher-/Nachher-Bilanz mit ICS-Belegzeiten; M–L | planning_summary; S26-06; D38 | Nutzer wählt Aufgaben und Ziel; keine automatische Verteilung; Fälligkeiten bleiben; ein Undo | Tk-freie Bilanz-/Umplanungsregeln; Kapazität, ungeschätzte Aufgaben, Mehrfachauswahl, alle drei Kontexte, D02; Gegenprobe gegen Vorversion | ▶ vollständig ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-19 / V02, neuer Vorschlag | erneuter Fremdimport kann Dubletten schaffen → Quellen wiedererkennen | A/V nach D39: unverändert/geändert/neu, eigene Änderungen als Konflikt, ausdrücklich gewählte Übernahme; L | S26-09; Datenformat-Tor für Quellenmetadaten; D39 | keine stillen Dubletten oder Überschreibungen; Verlustbericht; keine Live-Synchronisation; Zustände über Neustart erhalten | Tk-freie Zuordnungs-/Konflikttests; gleiche/geänderte Exporte, umbenannte Quellen, Konflikt/Abbruch/Undo, Migration/Altleser | ▶ vollständig ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-20 / I6, W01/W02/W06–W08/N08 | Windows seit 3.33.18, Linux-Sicht und Menschenabnahme offen → belegter Plattformstand | A/V nach D42: native Windows-Vollprüfung je Lieferung; vorhandene Windows-/Linux-Sichtfälle nachführen; L + getrennte Abnahme | native Windows-/Linux-Runner; GitHub Actions aktiviert; Inhaber für Menschenabnahme | Mac/Linux/Windows-Ergebnisse getrennt; kein automatischer Lauf ersetzt Menschenbedienung/DPI/Screenreader; keine unbelegten Plattformfreigaben | native Vollprüfungen je Lieferung, vorhandene manuelle Prüfliste; konkrete Lauf-/Artefaktverweise; echte Readerproben getrennt von Attributtests | ▶ vollständig ausgewählt 10.10.2026; Umsetzung/Abnahme nach D44 beauftragt |
| S26-21 / P05 | gemeinsame Helfer nur teilweise → gezielte Vereinheitlichung | A/1 nach D40: nur nachweislich gleiche UI-Texte/Abläufe im angefassten Sprint-Code; S–M | kein Großumbau, D17; D40 | gleiche Bedeutung, keine stillen Aktions-/Begriffsänderungen; kein Gesamtabgleich | betroffene Aufrufer, Bindungen und bestehende Suites; Gegenprobe für jeweiliges Paketverhalten | ▶ erste Stufe ausgewählt 10.10.2026; Umsetzung nach D44 beauftragt |
| S26-22 / LG04 | Knicke an Rundungsübergängen und enger Innenraum klein → sauberer Master | A/V nach D41: tangentiale Anschlüsse/Kurzsegment, zusätzliche Kleingrößenfassung 16/32; M–L | Vorher-/Nachher-Abnahme vor Übernahme; D28 unabhängig | Silhouette/Farbe erhalten; keine stille Masteränderung; Exporte nachvollziehbar | Vektor-/Rastervergleich, 16/32/54/512 px, Gestaltungsabnahme, App-Symbole/Lieferabgleich; Gegenprobe gegen Vorversion | ▶ vollständig ausgewählt 10.10.2026; Gestaltungsabnahme D45 erteilt; Umsetzung offen |

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

**Runde 4 entschieden (D30–D35):** 13 E-S8a ICS (Einzeltermine oder zusätzlich Serien/Ausnahmen), 14 E-S8b Bewegung (Abhaken/Klappen oder zusätzlich Bereichswechsel), 15 Bedienfläche (Liste/Heute oder alle betroffenen Hauptansichten; alternativ nur messen), 16 P03-Rest (Karten oder zusätzlich Startseiten-Neuaufbau), 17 E01-Rest (erste Anzeige oder zusätzlich Wiederverwendung), 18 Linux (Kernwege oder gesamte sachlich ausführbare Matrix). Jeweils A/1 erste Stufe, A/V vollständig oder B auslassen; bei Bedienfläche B nur messen/C auslassen. Gewählt jeweils A/V. Bedienflächen-Referenz 1280 × 800 folgt bereits dem verbindlichen P4; 840 ist nur Zusatzmessung. Ziele P03 ≤ 150 ms; E01 erste Anzeige ≤ 250 ms, erneutes Öffnen ≤ 150 ms. Abweichungen belegt vorlegen. E01 wird nach D34 getrennt als S26-14b geführt. Gesamtplan D44 bestätigt; nächste freie Entscheidung D48. Die Umsetzungen stehen aus.

### 15.6 Fünfte Auswahlrunde (10.10.2026)

Entschieden durch D36–D41; Schlussrunde anschließend D42/D43, Gesamtplan D44 bestätigt, Logoentwürfe D45 freigegeben; nächste freie Entscheidung D48. Aufwand S bis 1 Arbeitstag, M 2–4, L mehr als 4; N12 vollständig braucht mehrere Pakete. Empfehlungen sind keine Auswahl.

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

**Am 10.10.2026 durch D44 bestätigt, Wortlaut „ja“.** Jede Tabellenzeile ist eine vollständige Lieferung nach §15.3. Die Funktionsumfänge aus §15.1 und D18–D43 werden dadurch nicht verkleinert. Die Folgepaket-Suiten sind geplant; `test_fundament3360` ist inzwischen vorhanden und gezielt geprüft, ihre eingefrorene Mac-Vollprüfung ist grün; die native Linux-/Windows-Abnahme steht noch aus. Terminliche Zusagen werden aus der Aufwandsgröße nicht abgeleitet.

| Folge / Version | Inhalt und Aufgaben | Warum in dieser Reihenfolge | Status |
|---|---|---|---|
| 1 / **3.36.0** | Fundament und Tempo: P03-Rest S26-14, E01-Rest S26-14b, gesamte ausführbare Linux-Matrix S26-15; native Windows-Vollprüfung S26-20 ab dieser Lieferung | belastbare Prüfstände und Tempo vor dem breiten Oberflächenumbau | ▶ in Arbeit seit 10.10.2026 |
| 2 / **3.37.0** | Logo und Symbole: Tk-8.6-Rückfall/App-Symbole S26-11, gesamte ICONS-Tabelle S26-12, Logo-Master und Kleingrößen S26-22 | Grafikgrundlagen vor neuen Oberflächenaufnahmen; Gestaltungsabnahme vor Masterübernahme | beauftragt nach D44; Gestaltungsabnahme D45 erteilt; Umsetzung offen |
| 3 / **3.38.0** | Aufgabenoberfläche nach Bild 1: OB02 S26-01, OB03 S26-02, gemeinsamer Inspektor S26-03, direkte Felder S26-04, Bewegung S26-07, Bedienfläche S26-13 | einheitliche Bearbeitungsfläche als Grundlage für folgende Planungs- und Zugänglichkeitswege | beauftragt nach D44; Umsetzung offen |
| 4 / **3.39.0** | Tagesplanung: Tageshinweise S26-05, ICS-Belegzeiten S26-06, Tag entlasten S26-18 | alle Kapazitätswege teilen dieselbe Bilanz; Entlasten berücksichtigt die neuen Belegzeiten | beauftragt nach D44; Umsetzung offen |
| 5 / **3.40.0** | Pixelanimation S26-08 vollständig mit PNG-Spritesheet/Einzelbildfolge | eigenes Datenformat- und Exportpaket, getrennt vom folgenden Import | beauftragt nach D44; Umsetzung offen |
| 6 / **3.41.0** | Notion-Import S26-09, Wiedererkennung/Konfliktvergleich S26-19, einzelne Seite aus Sicherung S26-17 | Quellenzuordnung und Wiederherstellung gemeinsam gegen Verweis-/Anhangsregeln prüfen | beauftragt nach D44; Umsetzung offen |
| 7 / **3.42.0** | Eigenständige Pakete S26-10: PyInstaller 6.22.3, macOS arm64 und Windows x64, Python 3.14/Tk 9 | vollständigen Funktionsstand samt Ressourcen bündeln; Bauweg vor Tk-9.1-Wechsel festigen | beauftragt nach D44; Umsetzung offen |
| 8 / **4.0.0** | Zugänglicher Aufgaben-Kernablauf S26-16 A/1 mit eigener geprüfter Tk-9.1-Laufzeit und tatsächlichen Readerproben | baut auf gemeinsamem Inspektor und eigenständigen Paketen auf; Stufe 5 des Plans beginnt mit dem gewählten Schnitt | beauftragt nach D44; Readerabnahme offen |

**Durchgehend:** S26-20 umfasst Windows-Vollprüfung je Lieferung sowie Nachführung der vorhandenen Windows-/Linux-Sichtfälle und der getrennten Menschenabnahme. S26-21/P05 A/1 wird nur im tatsächlich angefassten Sprint-Code umgesetzt; seine Aufrufer werden im jeweiligen Paket geprüft. S26-15 nimmt nach der Kalibrierung auch jede neue sachlich ausführbare Sprint-Suite in die verpflichtende Linux-Matrix auf. D19/D21 sind mit erstellten Referenzen und Bildwahl erledigte Planungsvoraussetzungen, keine zusätzliche Produktionsversion. Damit sind S26-01–S26-22 einschließlich S26-14b vollständig zugeordnet.

**Paket 1 – 3.36.0, Fundament und Tempo.** Ausgangslage: echter Startseiten-Neuaufbau 270–300 ms, Einstellungen etwa 560 ms; Linux-Integrationen bisher nicht vollständig verpflichtend, Windows zuletzt 3.33.18. Ziel/Nutzen: kürzere Wartezeit und belastbare Plattformregressionen. Umfang: gezielte Kartenaktualisierung und viele Karten, tatsächlicher Startseiten-Neuaufbau, zuerst sichtbare Einstellungsbereiche und sichere Wiederverwendung. Abnahme: Startseite ≤ 150 ms; erste Einstellungsanzeige ≤ 250 ms, wiederholt ≤ 150 ms auf Referenz-Mac. Warm/kalt und Median/p95 getrennt dokumentieren; Fokus, Scrollposition, Cache-Gültigkeit, aktuelle Werte, Widget-/Speicherentwicklung und freigegebene Rückrufe prüfen. Keine reine Cachetreffer-Messung als Neuaufbau ausgeben. Neue Pflichtsuite `test_fundament3360` mit Gegenprobe gegen 3.35.0; echte Defektfälle sichern die kalibrierten Linux-Erwartungen. Vollständige Matrix mit begründeten nativen Plattformfällen führen. Nachweis: Baseline-/Nachhermessung, Suite/Gegenprobe, Mac-/Linux-/Windows-Ergebnisse. Messbare Zielabweichungen dem Inhaber vorlegen; sie gelten erst nach einer ausdrücklichen Entscheidung als akzeptiert. **D46 (10.10.2026):** Kalt-Ausnahme ≤ 300 ms bei direktem Start und ≤ 500 ms im beobachteten Kindprozessverfahren angenommen; warmer tatsächlicher Builder bleibt ≤ 150 ms, alle Funktionsumfänge erhalten. **D47 (10.10.2026):** erneute Einstellungsanzeige Median ≤ 150 ms/p95 ≤ 170 ms angenommen; erste Anzeige bleibt ≤ 250 ms. [Messnachweis](../01_Repository/Glide/tests/qa-3.36.0/fundament_vorher_nachher/README.md); Endgültiger Quellstand `04a0597…`: Messung nach D46/D47 und eingefrorene Mac-Vollprüfung am 10.10.2026 grün; native Abnahme/Lieferabschluss offen. Erster nativer Kandidat `a7197d4`: Linux zwei Prüfablauffehler und Windows-Vorlauffehler vor Checkout; korrigierte Werkzeuge mit zwei gezielten grünen Mac-Suiten und passenden roten Defekten, Produktionshash unverändert. Zweiter Kandidat `6a2cebe`: native Grundstufe und Linux-Vollprüfung einschließlich sieben Defektgegenproben grün; Windows-Vollprüfung mit zehn Befunden beendet, Fundamentsuite grün. Desktop nur 1024 × 768; Werkzeugnachlauf für bestätigte Referenzgröße, echte absolute Betriebssystempfade und Tcl-Padding vorbereitet. Übrige Befunde bleiben bis zum erneuten nativen Lauf offen.

**Paket 2 – 3.37.0, Logo und Symbole.** Ausgangslage: belegte Tk-8.6-Treppenkanten, langsamer großer PNG-Weg, Ersatzschriftzeichen und Masterknicke. Ziel/Nutzen: saubere Darstellung beim Start und in kleinen Größen. Entwürfe im Vergleich alt/neu sowie 16/32/54/512 px am 10.10.2026 als D45 vom Inhaber freigegeben. Nun technische Glättung per Standardbibliothek, App-Symbole 16/32/64/256 px, freigegebene tangentiale Masterkurven und Kleingrößenfassung liefern. Gesamte ICONS-Tabelle in der UI-Systemschrift auf Abdeckung, Größe, Ausrichtung und Bedeutung prüfen; Beschriftungen/Tastaturwege erhalten. Abnahme: korrekte Rastergrößen/Zwischentöne, DPI-/Akzentwechsel, unveränderter Tk-9-Weg, kein großes PNG im Startweg; native Sichtprüfung gesondert ausweisen. `test_logo3370`, Tk-freie Raster-/PNGtests, Gegenprobe gegen 3.36.0 für die bekannten Darstellungsfehler; Vektor-/Rastervergleich und Ressourcenhashes im Nachweis. Die technische Korrektur D28 und die freigegebenen Master D45 werden gemeinsam umgesetzt.

**Paket 3 – 3.38.0, Aufgabenoberfläche.** Ausgangslage: doppelte Bearbeitungsflächen, dauerhafte Zeilenaktionen und ungemessene Bedienfläche. Ziel/Nutzen: nächste Handlung erkennen und Felder unmittelbar ändern. Umfang vollständig nach D22–D25/D31/D32: vier Textstufen, Heute-Kopf, kontextuelle Aktionen in vier Ansichten, ein Inspektor und direkte Planungsfelder in allen sechs gewählten Kontexten; schmal innerhalb der Inhaltsfläche. Die bestehenden Listen-/Tabellenmodelle, sämtliche Felder, Einstiege, stabilen IDs, Schreibschutz- und Undo-Wege bleiben erhalten. Abnahme: Feld-/Einstiegsmatrix Liste/Tabelle/Heute/Demnächst/Pinnwand/Dokumentverweise; Maus, Tastatur, Kontextmenü und Palette; Popoverposition, Fokus, Abbruch und Neustart. Bewegung ≤ 150 ms, schnelle Folgen abbrechbar, Abschaltoption wirksam und keine zurückbleibenden Rückrufe. Bedienfläche in Liste, Tabelle, Heute, Demnächst, Seiten und Pinnwand ≤ 15 % bei 1280 × 800; 1280 × 840 zusätzlich berichten; 860 × 700 und große Schrift lesbar/erreichbar. `test_aufgaben3380` mit Geometrie-/Bindungs-/Lebensdauerproben, Gegenprobe gegen 3.37.0; Tempo vor/nach und eigene Fensteraufnahmen. Der Entwurf allein ist kein Messbeleg.

**Paket 4 – 3.39.0, Tagesplanung.** Ausgangslage: manuelle Tagesrituale, freie Zeit ohne externe Termine, Überplanung nur als Hinweis. Ziel/Nutzen: rechtzeitig beginnen/abschließen und Überplanung ausdrücklich korrigieren. Umfang vollständig D20/D30/D38: optionale Tageshinweise mit Vorgabe aus, 08:30/17:30, Uhrzeiten/Wochentagen, später erinnern/heute überspringen und gesammelten verpassten Hinweisen; nur laufende App, kein Zwangswechsel und keine doppelte Zustellung über Neustarts. Gewählte lokale ICS-Datei lesend, Einzel-/ganztägige Termine, übliche tägliche/wöchentliche/monatliche/jährliche Serien, Ausnahmen, Zeitzonen/Sommerzeit, transparente/stornierte Termine; nicht unterstützte Regeln sichtbar melden. Überschneidungen als vereinigte Belegzeit zählen. Nutzer wählt Aufgaben und anderen Tag/Vorrat aus Heute, Woche oder Tagesvorschlag; Vorher-/Nachher-Bilanz einschließlich ICS, Fälligkeiten erhalten, eine Aktion ein Undo. Abnahme: dieselbe Bilanz in allen Planungswegen, keine Kalender-Synchronisation oder aus Terminen erzeugten Aufgaben. `test_tag3390`, Tk-freie Zeit-/Zustell-/ICS-/Bilanztests mit künstlicher Uhr und Archiv-Fixtures; Sommerzeit, Randtage, Ausnahmen, Mehrfachauswahl, ungeschätzte Aufgaben, Modalzustand, Neustart/Undo; Gegenprobe gegen 3.38.0.

**Paket 5 – 3.40.0, Pixelanimation.** Ausgangslage: Zeichnungen haben nur einen statischen Zustand. Ziel/Nutzen: kleine Animationen vollständig lokal erstellen/exportieren. Umfang D18: Frames anlegen, duplizieren, löschen, umordnen; gemeinsame und einzelne Dauer; unterbrechbare Vorschau; PNG-Spritesheet und PNG-Einzelbildfolge. Abnahme: alte Zeichnungen verlustfrei erhalten, Reihenfolge/Dauer nach Neustart identisch, Bearbeitungen rücknehmbar, Exporte pixelgenau zu Frames; kein GIF. Eigenes Datenformat-Tor mit Vorsicherung, Migration und schreibgeschütztem Altleser. `test_animation3400`, Tk-freie Frame-/Zeit-/Exporttests und echte Werkzeug-/Undo-/Neustartproben, Gegenprobe gegen 3.39.0; Exportdateien und Migrations-/Altlesernachweis.

**Paket 6 – 3.41.0, Notion und Seitenwiederherstellung.** Ausgangslage: keine kontrollierte Notion-Quellenzuordnung, Sicherungsvergleich bisher lesend. Ziel/Nutzen: Inhalte mit sichtbaren Verlusten übernehmen, spätere Exporte kontrolliert nachziehen und einzelne Fehländerungen reparieren. Umfang vollständig D26/D39/D37: ZIP „Markdown & CSV“, Texte/Überschriften/Listen, lokale Bilder/Anhänge, Aufgaben-Kästchen und interne Seitenverweise; Unterseiten in bestehende Ordner/Seiten. Vorschau, Verlustbericht, Größen-/Pfadgrenzen und Vorsicherung. CSV-Datenbanken und nicht unterstützte Exportbestandteile ausdrücklich ausweisen und Quellen erhalten; keine Notion-Datenbank nachbauen. Unveränderte/neue/geänderte Quellen und lokale Konflikte dauerhaft wiedererkennen; nur ausdrücklich ausgewählte Änderungen übernehmen. Einzelne Seite aus vorhandener Sicherung mit Text/Bildern/Anhängen/Aufgabenverweisen/Live-Listen vergleichen und wiederherstellen; fehlende Ziele vorab zeigen, IDs konsistent, andere Seiten unverändert, ein Undo. Keine Live-Synchronisation oder neues System fortlaufender Seitenversionen. `test_import3410`, Tk-freie Parser-/Archiv-/Zuordnungs-/Konflikt-/Wiederherstellungstests; gleiche/umbenannte/geänderte Quellen, ungültige Archive, fehlende Ziele, Abbruch, Undo/Neustart; Gegenprobe gegen 3.40.0. Quellenmetadaten mit eigenem Datenformat-Tor sichern.

**Paket 7 – 3.42.0, eigenständige Pakete.** Ausgangslage: vorhandener Starter/Bundle braucht installiertes Python. Ziel/Nutzen: geprüften Stand ohne externe Python-Installation starten. Umfang D27: PyInstaller 6.22.3 ausschließlich gepinnte Bauabhängigkeit, native Bauwege macOS arm64/Windows x64 mit Python 3.14/Tk 9, Ressourcen/vendor, Drittanbieter-Lizenzbelege und nachvollziehbare Bauanweisungen. Abnahme: Paketversion/Architektur vollständig belegt, Daten außerhalb Paket, tatsächlicher isolierter Start und Ressourcen-/Import-/Speicherprobe ohne externen Python-Bezug. Leeres PATH allein genügt wegen absoluter Interpreterpfade der Vorversion nicht als Nachweis; zusätzlich Laufzeit-/Bibliotheksabhängigkeiten und den nativen isolierten Prüfstand belegen. `test_paket3420`, native Paketproben und Gegenprobe gegen 3.41.0; Paket-/Quellhashes und Start-/Signaturergebnisse. macOS-Ad-hoc-Signatur im Bauordner und auf Rückkopie prüfen. Windows ohne Inhaberzertifikat als unsigniertes Entwicklungsartefakt kennzeichnen und Integrität nachweisen; öffentliche Signaturen bleiben I3. Linux-Matrix bleibt Pflicht, ein eigenständiges Linux-Paket ist nicht gewählt.

**Paket 8 – 4.0.0, zugänglicher Aufgaben-Kernablauf.** Ausgangslage: bisherige Tk-9.0-Oberfläche hat keine belegte Screenreader-Bedienbarkeit. Ziel/Nutzen: den ausgewählten Kernablauf tatsächlich zugänglich machen. Umfang ausdrücklich D36 A/1: Aufgaben erfassen, suchen, in Heute planen und im gemeinsamen Inspektor bearbeiten; eigens geprüfte Python-3.14-/Tk-9.1-Laufzeit, auch in beiden eigenständigen Paketen. Rollen, Namen, Werte, Zustände, Auswahl, Fokus und Bedienaktionen setzen; eigene Canvas-Flächen im gewählten Kernablauf erhalten semantische Tastaturalternativen. Abnahme: vollständiger Kernablauf mit VoiceOver, NVDA und Linux-Screenreader tatsächlich durchführbar; Tastatur, Undo, Neustart und bestehende Funktionen bleiben erhalten. `test_zugang400`, Tk-9.1-/Semantik-/Fokusproben, Gegenprobe gegen 3.42.0, native Paketstarts und getrennte reale Readerprotokolle. Seiteneditor, Kalender, Pinnwand und Pixel-Werkstatt sind außerhalb dieser ersten Stufe; 4.0.0 bedeutet keine Abnahme dieser übrigen Zukunftsstufe.

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
