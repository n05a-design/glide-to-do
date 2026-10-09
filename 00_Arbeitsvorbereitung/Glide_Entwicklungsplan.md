# Glide – Entwicklungsplan und Aufgabenstand

Stand 09.10.2026 · Glide 3.35.0 · Aufgabenformat 23

Einziges Planungsdokument: alle Aufgaben mit Marke, Stufen, Ziele und was der Inhaber entscheidet. Erledigte Zwischenstände (Paketbeschreibungen, Messerzählungen, Aufgabenkarten) werden nach der Lieferung gelöscht; Ergebnisse stehen im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md) und im [CHANGELOG](../01_Repository/Glide/CHANGELOG.md), Verhalten in den [Funktionen](../01_Repository/Glide/docs/20_FUNKTIONEN.md), Vorfassungen in Git.

Verbindliche Entscheidungen stehen in der [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md), Produktgrenzen und Prinzipien in den [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md). D07, Importquelle, Bauwerkzeug und Inhaberfreigaben bleiben eigene Entscheidungen (§11).

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
| 3 Pixel | Palettenbearbeitung, Symbolvorschau, Animation | ◐ G19, G-03 ✅ 3.35.0; G17 wartet auf D07 |
| 4 Austausch und Verteilung | KI-Austausch Stufe 2, Import, Sicherungsvergleich, Paket mit eigenem Python | ◐ G24, F-03 ✅ 3.35.0; G21 und G26 warten auf Entscheidungen |
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
| P03 | Aufbau und Layout | ◐ Bibliothekskarten 3.32.3, Startseite 3.33.2, unveränderte Kacheln bleiben 3.33.19 (P03r). Offen: Elemente geänderter Karten, sehr viele Karten, Neuaufbau der Startseite (270–300 ms, Grenze Tk-Zeichnen) |
| P04 = A-02 | Bildlayout nur bei geänderter Geometrie, Platzieren beim Scrollen | ✅ 3.33.19 |
| P05 | Gemeinsame Helfer | ◐ Hover 3.32.2; gleiche UI-Texte nur bei gleicher Bedeutung zentralisieren |
| P06r = A-03 | Doppelte Refresh-/Schreibanforderungen je Aktion | ✅ 3.33.19 |
| P07 | Volltextsuche als ersetzbarer FTS5-Cache | ✕ nach Messung 3.34.0: 66,6 ms Median bei 10.000 Punkten (Regel: unter 100 ms kein Index) |
| P08a/P08b | Ein Vergleichsdurchlauf für Verlauf und Aktivität; nur geänderte Listen vergleichen, Vollvergleich im Autosave | ✅ 3.33.9 / 3.33.11 |
| P08c | Abhaken bei 5.000 Punkten ≤ 120 ms | ✅ gemessen 3.33.19: 61 ms |
| P09a/P09b | Tabelle ohne Listenspaltenmessung; Kennzahlen, Datum und Schriftmaße einmal je Aufbau | ✅ 3.33.0 / 3.33.10 |
| T2 | Gemeinsame Formatsicherung | ✅ 3.33.0; Windows-Signatur 3.33.7, Inhaltsvergleich 3.33.8 |
| E01 | Einblendung des Einstellungsfensters | ✅ 3.33.19 (≈ 560 ms; Rest Tk-Zeichnen) |
| CI | CI-Grundstufe (Linux/Xvfb) | ✅ 01.10.2026; ○ Integrationssuiten unter Linux kalibrieren, damit sie verpflichtend in die CI können |

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
| LG04 | Logo-Master überarbeiten (Weg E; [Befunde](../20_Grafik_Master/README.md#befunde-am-logo-master-05102026-entscheidung-beim-inhaber)) | ○ Gestaltung beim Inhaber |
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
| OB02 | Vier Textstufen; Kopf von „Heute“ zeigt nächste Aufgabe, verfügbare Zeit und Fortschritt als stärkstes Element | 860 × 700, große Schrift; jede Angabe genau einmal | M | ○ nach I7 (E-S2) |
| OB03 | Zeilenaktionen nur bei Bedarf (Einplanen, Termin, „…“ beim Überfahren und bei Auswahl) | jede Aktion auch über Tastatur, Kontextmenü, Palette; Bedienfläche ≤ 15 % | M | ◐ Kalenderaktion 3.33.13; Rest nach I7 (E-S2) |
| OB04 | Dezente Bewegung beim Abhaken, Klappen und Bereichswechsel (≤ 150 ms), nur mit Animationen | keine messbare Verschlechterung der Ziele aus §10 | M | ◇ E-S8 |
| OB05 | Schmale Seitenleiste mit Symbolen | Zustand gemerkt; Tastatur; 860 × 700 | M | ✅ 3.33.21 |
| OB06 | Gestaltungsabnahme je Paket: Vorher-/Nachher-Fensterbilder, vom Inhaber bewertet; Bilder lokal und unversioniert | Entscheidung im QA-Bericht vermerkt | S je Paket | ◐ Bewertung durch den Inhaber offen |

#### B. Komfort im täglichen Gebrauch

| ID | Paket | Abnahme (Auszug) | Aufwand | Stand |
|---|---|---|---|---|
| KO01 | Ein Menü „Einplanen“ (Heute, Morgen, Wochenende, Nächste Woche, Datum …, Ohne Tag) für die Mehrfachauswahl | ein Undo-Schritt; Fälligkeit bleibt | S–M | ✅ 3.33.13 |
| KO02 | Wiederholungen: Termin überspringen, verpasste Termine überspringen | Serie bleibt; ein Undo-Schritt | S | ✅ 3.33.20 |
| KO03 | Erinnerungen in der Schnelleingabe als Chip | Chip nennt „nur bei laufender App“ | S | ✅ 3.33.20 |
| KO04 | Felder am Objekt: Klick auf Termin, Wichtigkeit oder Label öffnet die kleine Auswahl dort | ein Undo-Schritt; einheitlich mit N05 | M | ○ mit N05 nach I7 (E-S2) |
| KO05 | Mehrzeiliges Einfügen in die Eingabezeile nach Rückfrage | ein Undo-Schritt | S | ✅ 3.33.20 |
| KO06 | Zuletzt benutzte Ziele zuerst bei „Verschieben nach …“ und Labels | keine neue Einstellung | S | ✅ 3.33.20 |

#### C. Unterstützung im Alltag

| ID | Paket | Abnahme (Auszug) | Aufwand | Stand |
|---|---|---|---|---|
| AU01 | Tagesvorschlag „Was passt heute?“ mit Grund je Zeile | deterministisch; nichts ohne Bestätigung; ein Undo-Schritt | M | ✅ 3.33.14 |
| AU02 | Verfügbare Zeit in allen Planungswegen | eine Rechenstelle (`planning_summary`) | S–M | ✅ 3.33.13 |
| AU03 | Geführter Tagesbeginn (Rückblick → Vorschlag → Zeitblöcke) und optionaler Hinweis zu Tagesbeginn/-abschluss | Vorgabe des Hinweises entscheidet der Inhaber | M | ◐ geführter Weg 3.33.14; Hinweise nach E-S3 |
| AU04 | Wochenplanung im eingebetteten Kalender mit Kapazitätsbalken | Teil von N04 | M | ✅ 3.33.17 |
| AU05 | Fokussitzung mit nächster Aufgabe (= G05) | Zeit genau einmal gebucht | M | ✅ 3.33.14 |
| AU06 | Routinen als Abschnitt in „Heute“ | kein Formatwechsel | M | ✅ 3.33.20 |
| AU07 | Termine aus einer ICS-Datei als belegte Zeit im Stundenraster | berührt die Produktgrenze „ICS ist Dateiaustausch“ | M–L | ◇ E-S8 |

**Fertig (Programm), wenn:** Ein Tag lässt sich aus „Heute“ in höchstens drei Schritten planen ✅ (3.33.14); die verfügbare Zeit ist überall sichtbar, wo geplant wird ✅ (3.33.13); die Oberflächenziele aus §10 sind erreicht – offen (Bedienfläche); der Inhaber hat jede Welle gestalterisch abgenommen (OB06) – offen.

### 4.4 Größere Umsetzungspakete (Auftrag 07.10.2026)

Der Inhaber beauftragt mehrere zusammengehörige Features je Umsetzung, abgeleitet aus Analyse, Recherche und Konkurrenzdokumenten; innerhalb dieses Auftrags braucht es keine erneute Freigabe jeder Teilfunktion. Offene Produktentscheidungen bleiben offen. Geliefert als 3.33.14–3.33.18 und im Sprint 3.33.19–3.35.0 (§14).

**Prüfstrategie pro Paket:** gezielte Baselines der betroffenen Bereiche vor Produktionsänderungen; Unit-Tests und echte Bedienwege je Teilfunktion; eine Pflichtsuite mit Gegenprobe gegen die Vorversion; ein gemeinsamer eingefrorener Volllauf mit vollständiger Regression, Interaktions-/Fehler-/Undo-/Neustartprüfung, Mindestgröße, großer Schrift, hell und dunkel sowie Messung. Erst danach Python, Showcase und Bundle liefern. Weitere Vollläufe nur nach ausführbaren Änderungen oder einem Fehlerbefund; keine künstlichen Zwischenversionen. Native und menschliche Abnahme getrennt ausweisen.

## 5. Wissen im Kontext (Stufe 2)

| ID | Arbeit | Stand |
|---|---|---|
| N05 = U12 | Ein Inspektor statt Maske + Detailbereich | ○ nach I7 (E-S2) |
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
| G17 = G-02 | Animation: Frames, Dauer, Vorschau | ○ E-S1 (D07) |
| G24 = F-01 | KI-Austausch Stufe 2: Kontextpaket, Änderungsvorschläge mit Feldvergleich (Q3) | ✅ 3.35.0 |
| G21 = F-02 | Begrenzter Import aus einer ersten Quelle mit Verlustbericht | ○ E-S4 |
| F-03 | Zwei Sicherungsstände lesbar vergleichen | ✅ 3.35.0 |
| G26 = H-03 = N11 | Paket mit eingebettetem Python 3.14 + Tk 9 je Plattform (D15) | ○ E-S5 |
| – | Windows-/Linux-Abnahme, Linux-App (AppImage/Flatpak später) | ○ Inhaber |
| H-01 | Kontrollmatrix echter Bedienwege fortführen | laufend |

## 7. Zukunft und bewusst nicht

| ID | Thema | Marke | Grund / Auslöser |
|---|---|---|---|
| N12 = U23 | Screenreader und beschriftete Canvas-Bedienung über Tk 9.1 `tk accessible` | ◇ | Tk 9.1.0 ist erschienen (29.09.2026); Voraussetzung G26 und eigene Abnahme |
| N13 | Seitenversionen wiederherstellen | ◇ | Bedarf aus dem Alltag; der Sicherungsvergleich F-03 (3.35.0) zeigt Unterschiede bereits lesend |
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
| R5 | Plattform- und Menschenabnahme fehlen | automatische Vollprüfung auf dem Referenz-Mac je Paket; Windows-Vollprüfung zuletzt 3.33.18; Linux und menschliche Prüfliste bleiben eigene Tore (I6) |
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
| Bedienfläche über Inhalt (Liste, 1280 × 840) | ≤ 15 % | ○ zuletzt ≈ 27 %; nach U09/OB05 neu messen |
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
| I6 | Windows-Vollprüfung des aktuellen Stands und manuelle Prüfsitzungen | ○ Windows zuletzt 3.33.18; menschliche Sicht- und Bedienabnahme aller Versionen nach der [Prüfliste](Glide_Manuelle_Pruefung.md) |
| I7 | Referenzentwürfe für „Heute“, Liste und Seite (Affinity) | ○ E-S2 |
| I8 | Lösungsweg für das Logo unter Tk 8.6 (LG01–LG04) | ○ E-S6, [Diagnose, Abschnitt 7](../01_Repository/Glide/docs/diagnosen/LOGO_KANTENGLAETTUNG.md#7-lösungswege) |
| I9 | Rechte an Fremdbildern im öffentlichen Repository (`20_Grafik_Master/05_Inspiration`, `06_Beispielbilder`, die sechs Showcase-Motive) | ○ behalten mit Rechtenachweis oder entfernen und den Showcase mit eigenen Motiven neu erzeugen; Empfehlung: ohne Nachweis entfernen |
| I10 | Git-Historie bereinigen (gelöschte Protokolle mit Benutzerpfaden, frühere Archivkopien) | ○ eigener Auftrag; ändert alle Commit-Kennungen ([Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md#github-auftritt)) |
| I11 | GitHub-Auftritt: Beschreibung, Tags, Wiki, Issues, KI-Codeprüfung | ○ Empfehlungen in der [Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md#github-auftritt) |
| A–H | Bearbeitungstiefe der Auswahl vom 30.09.2026 (A Tempo · B Planen und Fokus · C Aufgaben im Text · D Suchen und Wissen · E Projektseiten · F Austausch und Sicherungen · G Pixel-Werkstatt · H Bedienkontrolle und Auslieferung) | beauftragte Teile umgesetzt (Aufgaben A-01 bis H-03 mit Status oben); weitere Tiefe je Richtung entscheidet der Inhaber |

**Benötigte Entscheidungen** (Stand 09.10.2026; Empfehlungen sind keine Entscheidungen):

| Nr. | Frage | Blockiert | Empfehlung |
|---|---|---|---|
| E-S1 | D07: Animationsexport GIF oder zuerst Frames/Spritesheet? | G17 | Spritesheet zuerst |
| E-S2 | I7: Referenzentwürfe liefern, oder N05/KO04 ohne Entwurf mit den bestehenden Rollen bauen? | OB02, OB03-Rest, N05, KO04 | N05 ohne Entwurf freigeben, OB02/OB03 weiter nach I7 |
| E-S3 | AU03: Vorgabe automatischer Tageshinweise (Uhrzeiten, an/aus) | AU03-Rest | Option, Vorgabe aus, 08:30/17:30 |
| E-S4 | G21: erste Importquelle | G21 | Notion-Markdown/ZIP |
| E-S5 | D15/G26: Bauwerkzeug | G26, N12 | PyInstaller ≥ 6.22 als reine Bauabhängigkeit |
| E-S6 | I8: Logo-Rückfall unter Tk 8.6 | LG01–LG04 | Weg B + D |
| E-S7 | A14: Symbolschrift | einheitliche Symbolgröße | Zeichen aus der Systemschrift wählen |
| E-S8 | AU07, OB04 | AU07, OB04 | AU07 nur lesend aus gewählter ICS-Datei; OB04 nach Tempozielen |

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

**Offen nach dem Sprint:** W02 und alle Lieferungen ab 3.33.19 auf Windows nachprüfen; W07/W08 (Windows-Sichtprüfung B1a); N08 unter Linux ansehen; menschliche Abnahme I6; Inhaberentscheidungen E-S1–E-S8 und I1–I11 (§11). Eingecheckt am 09.10.2026.
