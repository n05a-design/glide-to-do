# Glide – Konkurrenz- und Featurematrix

Stand und Online-Abruf **01.10.2026** · Glide 3.32.3 · Teil 2 von 4 der Analyse vom 01.10.2026

Ergänzt die [Konkurrenzübersicht und persönlichen Vorlieben](Glide_Konkurrenzuebersicht_und_persoenliche_Vorlieben_2026-10-01.md). Diese bleibt maßgeblich für **deine belegten Vorlieben** (Notion als ausdrückliches Vorbild; Trello, OneNote, FigJam, Planner, Affinity als benannte Referenzen). Dieses Dokument ergänzt drei Dinge:
- bisher fehlende, direkt relevante Konkurrenten,
- den Stand 2026,
- eine Feature-für-Feature-Matrix mit Glides tatsächlichem Codestand aus der [Bestandsaufnahme](Glide_Bestandsaufnahme_Code_und_Dokumentation_2026-10-01.md).

## 1. Ergebnis in Kürze

1. **Glides Funktionsbreite ist für ein Ein-Personen-Projekt außergewöhnlich.** Bei Tagesplanung (Bearbeitungstag ≠ Fälligkeit, Kapazität, Zeitblöcke, Tagesbeginn/-abschluss, Zeiterfassung) liegt Glide auf dem Niveau spezialisierter Planer. Pixel-Werkstatt und Pinnwand mit echten Aufgabenkarten bietet so kein anderes untersuchtes Produkt.
2. **Zwei bisher fehlende Konkurrenten sind die direktesten Vergleiche:** **AFFiNE** (Dokumente + unendliche Leinwand + Datenbanken, lokal-first, quelloffen) und **AppFlowy** (Dokumente + Datenbanken mit Tabelle/Board/Kalender, lokal, eigene KI-Modelle möglich). Beide haben rund 70.000 GitHub-Sterne. Die Aussage, die Kombination aus Seiten, Aufgaben, Pinnwand und lokalen Daten liege „selten im Mittelpunkt“, gilt deshalb nur noch eingeschränkt. Glides Abgrenzung muss über die **Tagesführung** laufen, nicht über die Kombination an sich.
3. **Die größten Lücken gegenüber dem Stand der Technik:**
   - Volltextsuche im Inhalt
   - Verweise zwischen Seiten
   - natürliche Eingabe mit sichtbarer Erkennung
   - Erinnerungen bei geschlossener App (bewusst nicht, Produktgrenze)
   - Erscheinungsbild folgt dem System
   - Sync/Mobil (bewusst zurückgestellt)
4. **Der Stand der Technik 2026 wird von KI bestimmt.** Beispiele: Spracherfassung (Todoist Ramble, Apple Erinnerungen iOS 27), Agenten und MCP-Schnittstellen (Notion 3.3, Todoist MCP). Eingebaute Cloud-KI widerspricht Glides Produktgrenzen. Glides Antwort ist bereits entschieden (Q3, 30.09.2026): **Austausch über Dokumente statt Schnittstelle** (G24 Stufe 2 mit Kontextpaket und Änderungsvorschlägen, Vorschau vor Übernahme). Das bleibt mit jedem Sprachmodell und ohne Netz nutzbar; eine MCP-Schnittstelle wird hier nicht erneut vorgeschlagen.
5. **Bei Bedienkomfort und Informationsarchitektur liegt Glide hinter den Vorbildern.** Es fehlt nicht an Funktionen, sondern es ist zu viel dauerhaft sichtbar. Details in der [UX-Prüfung](Glide_Produktprinzipien_und_UX-Pruefung_2026-10-01.md).

## 2. Vergleichsfeld

| Produkt | Kategorie | Warum im Vergleich | In bisherigen Unterlagen |
|---|---|---|---|
| **Notion** | Arbeitsbereich mit Seiten und Datenbanken | Ausdrückliches persönliches Vorbild | ja |
| **Todoist** | Aufgabenverwaltung | Maßstab für Erfassung und Datumssprache | ja |
| **Things 3** | Persönlicher Planer (Apple) | Maßstab für Ruhe, Apple-Anmutung, Start/Deadline-Trennung | ja |
| **TickTick** | Aufgaben + Fokus + Gewohnheiten | Maßstab für Fokus, Eisenhower, Kalender | ja |
| **Super Productivity** | Lokale Aufgaben + Zeiterfassung | Direktester lokaler Planer-Vergleich | ja |
| **AFFiNE** | Lokal-first Dokumente + Leinwand + Datenbanken | Kombination Seiten + Pinnwand + lokal | **neu** |
| **AppFlowy** | Lokal-first Notion-Alternative | Seiten + Datenbankansichten + lokale KI | **neu** |
| **Obsidian** | Lokale Markdown-Wissensbasis | Verweise, Canvas, Bases, offene Dateien | ja |
| **Apple Erinnerungen + Notizen** | Systemapps | Selbstverständlichkeit, Apple-Maßstab; iOS/macOS 27 | **neu** |
| Ergänzend: Sunsama, Capacities, Heptabase, Logseq 2.0, Craft, Microsoft Planner | jeweils Teilaspekte | Ritual, Objekte, Karten-Whiteboard, DB-PKM, Gestaltung | teils neu |

## 3. Stand 2026 – was sich seit der letzten Recherche bewegt hat

| Produkt | Entwicklung (Quelle) | Bedeutung für Glide |
|---|---|---|
| Notion | Offline-Modus seit 2.53 (19.08.2025) mit Offline-Übersicht; 3.2 (01/2026) KI-Notizen und Agenten auf Mobilgeräten; 3.3 (02/2026) **Custom Agents** mit Auslösern, Zeitplänen und MCP-Anbindung ([Release 2.53](https://www.notion.com/en-gb/releases/2025-08-19), [3.2](https://www.notion.com/de/releases/2026-01-20), [3.3](https://alternativeto.net/news/2026/2/notion-3-3-launches-custom-agents-for-autonomous-team-automation)) | „Notion kann nicht offline“ ist endgültig kein Unterscheidungsmerkmal mehr. Notions Richtung geht zu Team-Automation; Glides Richtung bleibt der persönliche Arbeitsplatz |
| Todoist | **Ramble**: Sprache → strukturierte Aufgaben mit Datum, Priorität, Projekt (Beta, Gemini-basiert); offizieller **MCP-Server**; Project Insights jetzt in Pro ([Ramble](https://www.todoist.com/help/articles/from-voice-to-tasks-ramble-july-1), [TechCrunch 01/2026](https://techcrunch.com/2026/01/21/todoists-app-now-lets-you-add-tasks-to-your-to-do-list-by-speaking-to-its-ai/), [Changelog 2026](https://www.todoist.com/help/articles/2026-changelog), [MCP](https://mcpservers.org/remote-mcp-servers/todoist)) | Natürliche Erfassung ist Standard. Glides G01 muss mindestens Datumssprache mit sichtbarer Erkennung liefern |
| Things 3 | 3.23 (21.08.2026) überarbeitete Wiederholungen: frühes Erledigen mit Folgetermin nach Regel; 3.24 (09/2026) Schlummer-Intervalle, Siri/Apple-Intelligence-Anbindung ([offizielle macOS-Release Notes](https://culturedcode.com/things/support/articles/1100684/)) | Feinschliff statt Funktionsfülle – genau das Apple-Prinzip |
| TickTick | 8.0 (01/2026): „Suggested Tasks“ zur täglichen Auswahl, Jahresansicht mit Heatmap, freie Akzentfarbe im Dunkelmodus; Telegram-Erfassung ([AlternativeTo](https://alternativeto.net/news/2026/1/ticktick-8-0-adds-suggested-tasks-improved-yearly-monthly-views-and-customization-options/), [Release Notes](https://releasebot.io/updates/ticktick)) | Glide hat Tagesbeginn und Jahres-Heatmap bereits – gute Bestätigung der Richtung |
| Apple Erinnerungen/Notizen | iOS/macOS 27: Erinnerung in eigenen Worten beschreiben, Apple Intelligence setzt Felder; Metadaten in einer Box um die aktive Erinnerung; Notizen exportieren als **Markdown** ([9to5Mac](https://9to5mac.com/2026/06/12/heres-everything-new-for-reminders-in-ios-27/), [Apfelpatient](https://www.apfelpatient.de/en/news/apple-brings-smart-updates-for-reminders-and-notes)) | Apples Muster: Felder **am Objekt** bearbeiten, nicht in einem Dialog – bestätigt U12 |
| AFFiNE | Dokument und Leinwand sind dieselbe Seite („edgeless“); Datenbank-/Kanban-Ansichten; lokal-first mit optionaler Cloud; KI für Text, Mindmaps, Präsentationen ([GitHub](https://github.com/toeverything/affine), [Whiteboard](https://affine.pro/blog/interactive-whiteboard-app)) | Stärkster Vergleich für Pinnwand + Seiten. Schwach in persönlicher Tagesplanung [Einschätzung] |
| AppFlowy | Tabelle, Board, Kalender, Galerie, Liste, Diagramm; **Vault Workspace**: offline mit lokaler KI (Ollama) ([Funktionen](https://mintlify.com/AppFlowy-IO/AppFlowy/features)) | Zeigt, dass lokale KI technisch alltagstauglich ist – aber mit großer Laufzeitabhängigkeit |
| Obsidian | 1.10 (01.10.2025): **Bases** mit Gruppieren, Zusammenfassungen, Listenansicht, API ([Changelog](https://obsidian.md/changelog/2025-10-01-desktop-v1.10.0/)) | Datenbankansichten über offene Dateien – Glide hat feste Felder, das bleibt richtig |
| Logseq | 2.0 Beta (13.07.2026): Wechsel von Markdown-Dateien zu SQLite-Datenbank, typisierte Eigenschaften, Datenverlust-Risiko in der Beta ([Diskussion](https://discuss.logseq.com/t/whats-new-with-logseq-db-may-16th-2026/35020), [Übersicht](https://kompozy.io/reviews/logseq-2-0)) | Warnbeispiel: Speicherwechsel ist ein Mehrjahresprojekt. Bestätigt D16 Option A (JSON optimieren statt SQLite als Primärspeicher) |
| Capacities | Aufgaben im zentralen Kalender, Eingang und Heute, Kalenderanbindung Google/Microsoft/Apple/CalDAV ([Docs](https://docs.capacities.io/reference/dates-and-daily-notes)) | Aufgaben im Wissenskontext sind Branchenstandard geworden |
| Heptabase | Karten auf Whiteboards, Standortanzeige „wo liegt diese Karte überall“, Web-Karten, KI auf Karten ([Roadmap](https://wiki.heptabase.com/roadmap)) | Glides globale Pinnwand mit echten Objekten ist dasselbe Prinzip |
| Microsoft Planner | Großes Update 2026, u. a. Whiteboard-Reiter und iCalendar-Feed entfallen ([Neowin](https://www.neowin.net/amp/microsoft-confirms-major-2026-update-to-remove-several-planner-features-add-new-ones/)) | Planner als Pinnwandreferenz nur noch für Gruppierungslogik |
| Super Productivity | Weiterhin lokal, ohne Konto, MIT-lizenziert; Pomodoro, Zeiterfassung, Timeboxing, WebDAV-Sync ([Produkt](https://super-productivity.com/), [Vergleich 2026](https://super-productivity.com/blog/best-local-first-todo-apps-2026/)) | Bleibt der direkteste Planer-Konkurrent im Lokal-Segment |
| Tcl/Tk | 9.1.0 laut offizieller Release-Seite veröffentlicht am 29.09.2026, einschließlich Screenreader-Unterstützung; python.org-Installer macOS liefert ab 3.14.5 Tk 9.0.3 ([Tcl 9.1](https://www.tcl-lang.org/software/tcltk/9.1.html), [TIP 733](https://core.tcl-lang.org/tips/doc/main/tip/733.md)) | Technische Chance für Barrierefreiheit und Verteilung (D15) |

## 4. Featurematrix

**Legende:**
- ● vorhanden
- ◐ teilweise, eingeschränkt oder nur in Bezahltarif
- ○ fehlt
- P nur per Erweiterung/Plugin
- – nicht Zweck des Produkts
- ? nicht verifiziert

**Spalten:** **Gl** Glide 3.32.3 · **No** Notion · **Td** Todoist · **Th** Things 3 · **TT** TickTick · **SP** Super Productivity · **AF** AFFiNE · **AP** AppFlowy · **Ob** Obsidian · **Ap** Apple Erinnerungen + Notizen

Glides Werte stammen aus dem Code. Die übrigen Werte beruhen auf Herstellerangaben und Recherche vom 01.10.2026, nicht auf Praxistests. Werte mit „?“ vor Übernahme in Entscheidungen prüfen.

### 4.1 Erfassen

| Funktion | Gl | No | Td | Th | TT | SP | AF | AP | Ob | Ap | Glide-Codebeleg / Anmerkung |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Schnelleingabe mit Feldern im Text | ◐ | ◐ | ● | ◐ | ● | ◐ | – | – | P | ● | `/`-Befehle: Wochentage, Wichtigkeit, Labels, `/meintag` |
| Natürliche Datumssprache mit sichtbarer Erkennung | ◐ | ◐ | ● | ● | ● | ◐ | – | – | P | ● | Datumshelfer vorhanden; Vorschau/Rücknahme fehlt (G01, D01) |
| Systemweite Schnellerfassung (App im Hintergrund) | ○ | ● | ● | ● | ● | ◐ | ? | ? | ◐ | ● | Nur in Glide selbst (`Strg+Alt+N`); G07 am 30.09. verworfen (nur plattformeigen lösbar) |
| KI-/Spracherfassung | ○ | ● | ● | ◐ | ? | ○ | ◐ | ◐ | P | ● | Bewusst keine Cloud-KI |

### 4.2 Planen und Arbeiten

| Funktion | Gl | No | Td | Th | TT | SP | AF | AP | Ob | Ap | Glide-Codebeleg / Anmerkung |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bearbeitungstag getrennt von Fälligkeit | ● | ◐ | ● | ● | ◐ | ◐ | – | ◐ | P | ○ | `planned_date`/`due`; D01 |
| Heute-Ansicht | ● | ◐ | ● | ● | ● | ● | ◐ | ◐ | ◐ | ● | Mein Tag mit Tagesnavigation |
| Tageskapazität / Aufwand | ● | – | ◐ | ○ | ◐ | ● | – | – | – | ○ | Kapazität je Wochentag, `estimated_minutes` |
| Zeitblöcke / Stundenraster | ● | ◐ | ◐ | ○ | ● | ● | ○ | ◐ | P | ◐ | `planned_time`, Stundenraster in Mein Tag |
| Kalender Monat/Woche | ● | ● | ◐ | ◐ | ● | ◐ | ? | ● | P | ● | Als **modales Fenster** (U11) |
| Tagesbeginn / Tagesabschluss / Wochenrückblick | ● | ○ | ◐ | ○ | ◐ | ● | ○ | ○ | P | ○ | Sunsama ist hier Maßstab |
| Wiederholungen | ● | ◐ | ● | ● | ● | ● | ○ | ? | P | ● | Regel am Punkt, Folgetermin beim Abhaken |
| Erinnerung bei geschlossener App | ○ | ● | ● | ● | ● | ◐ | ○ | ◐ | P | ● | Bewusst nicht (Stufe C, Produktgrenze „kein Push bei geschlossener App“) |
| Fokusmodus / Pomodoro | ◐ | ○ | ○ | ○ | ● | ● | ○ | ○ | P | ○ | Laufende Zeiterfassung vorhanden; Fokusansicht fehlt (G05) |
| Zeiterfassung je Aufgabe | ● | ◐ | ○ | ○ | ◐ | ● | ○ | ○ | P | ○ | `time_spent_minutes`, eine laufende Erfassung |
| Eisenhower-Matrix | ○ | ◐ | ○ | ○ | ● | ● | ○ | ◐ | P | ○ | G02 geplant; Vorschlag: als Board-Gruppierung (D13) |
| Abhängigkeiten | ● | ● | ○ | ○ | ○ | ○ | ○ | ○ | P | ○ | `blocked_by` |
| Gewohnheiten | ○ | ◐ | ○ | ○ | ● | ◐ | ○ | ○ | P | ○ | G06 bewusst Vorrat |

### 4.3 Ordnen und Ansichten

| Funktion | Gl | No | Td | Th | TT | SP | AF | AP | Ob | Ap | Glide-Codebeleg / Anmerkung |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Listen/Projekte, Ordner/Bereiche | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | Ordner, Bibliothek, Notizbuch |
| Labels / Tags | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | |
| Gespeicherte Filter / intelligente Listen | ● | ● | ● | ◐ | ● | ◐ | ◐ | ● | ● | ● | `SavedFilters` |
| Board / Kanban | ● | ● | ● | ○ | ● | ● | ● | ● | ◐ | ● | Pinnwand als Board mit Gruppierung |
| Tabelle | ● | ● | ○ | ○ | ○ | ○ | ● | ● | ● | ○ | Spaltenwahl, verschachtelt/flach |
| Galerie / Karten | ● | ● | ○ | ○ | ○ | ○ | ? | ● | ◐ | ○ | Galerie, Bibliothekskarten |
| Vorlagen | ● | ● | ● | ◐ | ● | ◐ | ● | ● | ● | ◐ | 16 mitgelieferte Vorlagen |
| Unteraufgaben / Checklisten | ● | ● | ● | ● | ● | ● | ◐ | ◐ | P | ● | Unterpunkte + Checkliste |
| Archiv und Papierkorb | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | |

### 4.4 Seiten und Wissen

| Funktion | Gl | No | Td | Th | TT | SP | AF | AP | Ob | Ap | Glide-Codebeleg / Anmerkung |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Block-Editor mit `/`-Menü | ● | ● | – | – | ◐ | ◐ | ● | ● | ◐ | ◐ | 13 Blockarten, Aufklapp-/Hinweisblock |
| Bilder in Seiten | ● | ● | – | – | ◐ | ○ | ● | ● | ● | ● | Linux: nur PNG/GIF/SVG |
| Echte Aufgaben im Dokument | ◐ | ◐ | – | – | – | – | ◐ | ◐ | P | ◐ | In Seiten ja, in Notizen nein (G29) |
| Interne Verweise / Rückverweise | ◐ | ● | ○ | ○ | ○ | ○ | ● | ● | ● | ● | Nur Punkt↔Punkt; keine Seitenverweise (G08/G30) |
| Volltextsuche im Inhalt | ◐ | ● | ● | ● | ● | ● | ● | ● | ● | ● | Nur Titel und Punkttexte (G14) |
| Datenbank-/Eigenschaftsansichten | ◐ | ● | – | – | – | – | ● | ● | ● | – | Feste Glide-Felder (bewusst) |
| Tagesnotiz / Notizbuch | ● | ◐ | – | – | ◐ | ◐ | ● | ? | ● | ○ | Notizbuch mit Stimmung und Impulsen |
| Seitensymbol / Titelbild | ◐ | ● | – | – | – | – | ● | ● | P | ○ | 16×16-Pixelsymbol; Titelbild fehlt (G09) |
| Markdown-Import/-Export | ● | ● | ◐ | ◐ | ◐ | ◐ | ● | ● | ● | ◐ | `page_markdown.py` |

### 4.5 Visuell

| Funktion | Gl | No | Td | Th | TT | SP | AF | AP | Ob | Ap | Glide-Codebeleg / Anmerkung |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Freie Leinwand / Pinnwand | ● | ○ | ○ | ○ | ○ | ○ | ● | ○ | ● | ◐ | Mit echten Aufgabenkarten, Verbindungen, Bereichen |
| Pixel-Zeichnen und Symbol-Export | ● | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | **Alleinstellungsmerkmal** im Vergleichsfeld |
| Animation | ○ | – | – | – | – | – | – | – | – | – | G17, D07 offen |

### 4.6 Daten, Plattform, Integration

| Funktion | Gl | No | Td | Th | TT | SP | AF | AP | Ob | Ap | Glide-Codebeleg / Anmerkung |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ohne Konto vollständig nutzbar | ● | ○ | ○ | ● | ○ | ● | ● | ◐ | ● | ◐ | |
| Daten als offene lokale Datei | ● | ○ | ○ | ○ | ○ | ◐ | ◐ | ◐ | ● | ○ | Eine lesbare JSON-Datei |
| Automatische Sicherungen / Versionen | ● | ● | ● | ◐ | ◐ | ◐ | ● | ◐ | ● | ◐ | Sicherungen + Tagesstände + Verlauf |
| Sync zwischen Geräten | ◐ | ● | ● | ● | ● | ● | ● | ● | ● | ● | Datenordner in Cloud-Ablage mit Sperre, ohne Zusammenführen |
| Mobile Apps | ○ | ● | ● | ● | ● | ● | ● | ● | ● | ● | D03: zurückgestellt |
| Windows / macOS / Linux | ● | ◐ | ● | ○ | ● | ● | ● | ● | ● | ○ | Linux eingeschränkt (Tk 8.6, Bildformate) |
| Import aus anderen Apps | ◐ | ● | ● | ◐ | ● | ◐ | ● | ● | ● | ○ | CSV/TXT/MD/ICS; kein Notion-/Todoist-Import (G21) |
| Kalenderdatei/-abo (ICS) | ● | ◐ | ● | ◐ | ● | ◐ | ○ | ○ | P | ● | ICS-Import/-Export als Datei |
| Eingebaute KI | ○ | ● | ● | ◐ | ? | ○ | ● | ● | P | ● | Bewusst nicht; Austauschformat für externe KI |
| API / MCP für Assistenten | ◐ | ● | ● | ◐ | ◐ | ? | ? | ◐ | ◐ | ◐ | `.glideexchange`; Q3: Dokumente statt Schnittstelle |

### 4.7 Bedienung und Hilfe

| Funktion | Gl | No | Td | Th | TT | SP | AF | AP | Ob | Ap | Glide-Codebeleg / Anmerkung |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Befehlspalette | ● | ● | ● | ◐ | ◐ | ◐ | ● | ◐ | ● | ○ | Doppelt: Schnellsuche **und** Aktionsdialog (U01) |
| Erscheinungsbild folgt dem System | ○ | ● | ● | ● | ● | ● | ● | ● | ● | ● | 10 Designs, aber kein „wie System“ |
| Rückgängig auch für Strukturänderungen | ● | ● | ◐ | ● | ◐ | ◐ | ● | ● | ● | ● | 20 Schritte, Bestandswächter |
| Geführter Einstieg / Beispielinhalt | ◐ | ● | ● | ● | ● | ◐ | ◐ | ◐ | ◐ | ◐ | Probedaten „Rundgang“ und Showcase, Vorlagen; Einstieg für neue Nutzer bewusst nicht gewählt (27.09.) |
| Hilfe in der App | ● | ● | ● | ● | ● | ◐ | ◐ | ◐ | ◐ | ◐ | Handbuch F1, Kürzel, Dauerhinweise in Fußzeilen |
| Screenreader | ○ | ? | ? | ● | ? | ? | ? | ? | ? | ● | Tk 9.1 bringt Grundlage (T6) |

## 5. Vergleich nach Dimensionen

| Dimension | Benchmark und warum | Glide heute | Lücke | Konsequenz |
|---|---|---|---|---|
| **Features** | Notion (Breite), TickTick (Planung + Fokus), AFFiNE (Seite + Leinwand) | Sehr breit; bei Tagesplanung führend im Lokal-Segment | Volltext, Seitenverweise, Fokusansicht, Eisenhower, Hintergrund-Erinnerung | Keine neue Breite, sondern die vier Lücken im Kern schließen (Plan Stufe 1–2) |
| **Workflow / Alltag** | Things (Heute → Demnächst → Irgendwann), Sunsama (Ritual) | Ritual vorhanden; Ansichten überlappen (Mein Tag, In Bearbeitung, Verspätet, Nächste Aufgabe, Startseite-„Heute“) | Klares mentales Modell fehlt | Ansichtenmodell vereinfachen (D14) |
| **Quality of Life** | Todoist (Erfassung), Apple (Felder am Objekt) | Viele Komfortdetails: Undo überall, Tageszählung, Nachführen offener Abschnitte | Erkennung beim Tippen nicht sichtbar; Detailbearbeitung doppelt (Dialog + Bereich) | G01 mit Feldvorschau; ein Inspektor (U12) |
| **Bedienkomfort / Geschwindigkeit** | Things, Apple: unter 100 ms für jede Aktion | 1.000 Punkte: Abhaken 56 ms; 10.000 Punkte: 458 ms; Startseite teuerste Ansicht | Linearer Speicherweg (T1), Startseitenaufbau (Rest P03) | P03-Rest, P08 |
| **Design / Informationsarchitektur** | Things, Notion: viel Weißraum, wenige sichtbare Bedienelemente | Durchdacht im Detail (Kontrast, Symbolfamilie), aber dicht: 8 Kopfsymbole, Dauerhinweise, Pinnwand mit ≈ 175 px Bedienleisten | Zu viel dauerhaft sichtbar | UX-Bereinigung Stufe 1 (U01–U10) |
| **Support / Hilfe** | Things („Erste Schritte“ als echtes Projekt), Notion (Startseite mit Beispielen) | Handbuch, Kürzelübersicht, Hinweiszeilen in jeder Ansicht, Probedaten „Rundgang“ und Showcase | Kein „Was ist neu“, Hilfe dauerhaft statt bei Bedarf; Erststart bewusst nicht gewählt | Hinweise bei Bedarf (D11), „Neu in …“ nach Update (N07) |
| **Branding / Wiedererkennung** | Things (eine starke Gestalt), Notion (Schwarz-Weiß-Minimalismus) | Eigenes „g“-Logo, Gismo als pflegbarer Begleiter (Entscheidung Arbeitsbegleiter), Pixel-Design – starke Ansätze | 10 Designs verwässern die Gestalt; Name „Glide“ kollidiert mit bekannten Produkten (z. B. der No-Code-Plattform Glide) | Ein Signaturdesign + Dunkelvariante als Standard, Gismo als Markenfigur behalten; Markenprüfung bleibt Inhaberentscheidung |
| **State of the Art 2026** | Todoist Ramble/MCP, Notion Agents, Apple Intelligence | Austauschformat `.glideexchange` für externe KI | Keine direkte Assistenten-Schnittstelle – bewusst (Q3) | G24 Stufe 2 (Kontextpaket, Änderungsvorschläge mit Vorschau) umsetzen |

## 6. Positionierung (aktualisiert)

Die Kombination „Seiten + Aufgaben + Leinwand + lokal“ allein trägt nicht mehr: AFFiNE und AppFlowy decken sie quelloffen ab. Was im untersuchten Feld **keiner** in dieser Form vereint:

> **Glide ist der ruhige, lokale Arbeitsplatz für den eigenen Tag:**
> - planen mit Bearbeitungstag, Fälligkeit und Kapazität,
> - erledigen mit Zeit und Fokus,
> - festhalten in Seiten, Notizbuch und Pinnwand,
> - alles in einer eigenen Datei, ohne Konto.
> Die Pixel-Werkstatt ist die persönliche Signatur.

Daraus folgt für die Priorisierung:
- **Stärken vertiefen:** Tagesführung (G01, G05, D14), Aufgaben im Kontext (G29, G31, G08/G30) und Wiederfinden (G14).
- **Nicht nachbauen:** Team, Cloud, frei definierbare Datenbanken, eingebaute Cloud-KI.

## 7. Funktionslücken: notwendig, sinnvoll, Zukunft, bewusst nicht

Neue Vorschläge tragen die Kennung **N01–N20**; bestehende Kennungen (G, A–H) werden weitergeführt. Abgleich mit früheren Entscheidungen (Funktionsrecherche 30.09., Bestandsprüfung 27.09., Produktgrenzen): Bereits entschiedene Punkte sind entsprechend eingeordnet und werden nicht erneut zur Entscheidung gestellt.

| Kennung | Lücke | Wer es hat | Klasse | Begründung |
|---|---|---|---|---|
| G01 | Natürliche Eingabe mit Feldvorschau | Todoist, Things, TickTick, Apple | **notwendig** | Standard 2026; D01 entschieden |
| G14 | Volltextsuche im Inhalt (FTS5) | alle Wissenswerkzeuge | **notwendig** | Seiten ohne Inhaltssuche verlieren mit wachsendem Bestand ihren Wert |
| G29/G31/G32 | Aufgaben in Notizen, Seitenaufgabe in Liste, Filter „aus Seiten“ | Capacities, Craft, Notion | sinnvoll | D05 entschieden; Kern der Positionierung |
| G08/G30 | Seiten-/Listenverweise mit Rückverweisen | Notion, Obsidian, AFFiNE | sinnvoll | Wissensetappe; Datenformat-Tor |
| G05 | Fokusansicht mit Timer | TickTick, SP | sinnvoll | Zeiterfassung existiert; kleine Ergänzung |
| G02 | Eisenhower | TickTick, SP | sinnvoll | Als Board-Gruppierung statt neuer Ansicht (D13) |
| N01 | Erscheinungsbild folgt dem System (Hell/Dunkel automatisch) | alle | sinnvoll, klein | Apple-Prinzip „funktioniert selbstverständlich“ |
| N02 | Eingang sichtbar, sobald er Einträge enthält | Things, Todoist, Capacities | sinnvoll, klein | Erfasstes muss auffindbar sein (U07) |
| N03 | Eine Befehlspalette (Suche + Aktionen), `Strg/Cmd+K` | Notion, Todoist, Obsidian | sinnvoll, klein | Doppelte Funktion entfernen (U01) |
| N04 | Kalender als eingebettete Ansicht mit Ziehen auf Tage | TickTick, Notion, AppFlowy | sinnvoll, mittel | Modal widerspricht „eingebettet“ (U11); D02 |
| N05 | Ein Inspektor für Punktdetails (Bereich statt Maske) | Apple 27, Things, Notion | sinnvoll, mittel | Zwei Editoren für ein Objekt (U12) |
| N06 | ~~Beispielseite „Erste Schritte“~~ | Things, Notion | entfällt | Einstieg für neue Nutzer am 25./27.09. bewusst nicht gewählt; Probedaten „Rundgang“ und Showcase decken Beispielinhalt ab |
| N07 | „Was ist neu“ nach einem Update (einmalig, eingebettet) | Things, Notion | sinnvoll, klein | Viele Versionen; Funktionen werden sonst nicht entdeckt |
| N08 | JPEG-Vorschau unter Linux über Systemwerkzeug-Fallback | – | sinnvoll, klein | Plattformgleichheit (T5) |
| N09 | Erinnerungen bei geschlossener App | alle Cloud-Apps | bewusst nicht | Produktgrenze „kein Push bei geschlossener App“, Stufe C der Systembenachrichtigungen bewusst nicht |
| N10 | Lokaler MCP-Server | Notion, Todoist (Cloud) | bewusst nicht | Q3 vom 30.09.2026: Dokumente statt Schnittstelle (G24) |
| N11 | = **G26/H-03** Paket mit eingebettetem Python + Tk 9 | alle Desktop-Apps | sinnvoll | Bereits „ja, vorbereiten“; neu: Linux/Windows-Gleichstand und Tk 9.1 als Begründung (D15) |
| N12 | Screenreader über Tk 9.1 | Apple, Things | Zukunft | Erst nach stabiler Tk-Freigabe; Canvas-Widgets beschriften (T6) |
| N13 | Seitenversionen wiederherstellen | Notion, AFFiNE | Zukunft | F-03 Sicherungsvergleich ist der Einstieg |
| N14 | = **G07** Systemweiter Erfassungs-Hotkey | Todoist, Things | bewusst nicht | G07 am 30.09. verworfen: nur plattformeigen lösbar |
| N15 | Spracherfassung | Todoist, Apple | bewusst nicht | Cloud-KI oder große lokale Modelle; widerspricht Abhängigkeitsregel |
| N16 | Gewohnheiten | TickTick | bewusst nicht (vorerst) | Überschneidung mit Wiederholungen; G06 bleibt Vorrat |
| N17 | Teamfunktionen, Teilen, Kommentare | Notion, Asana, ClickUp | bewusst nicht | Produktgrenze |
| N18 | Frei definierbare Datenbankfelder | Notion, AppFlowy, Obsidian Bases | bewusst nicht | Entschieden: Felder Glide-weit |
| N19 | Unterseiten, Graph | Notion, Obsidian | bewusst nicht | Entschieden bzw. G13 zurückgestellt |
| N20 | Web Clipper | Evernote, Notion | bewusst nicht | Browsererweiterung = neue Plattform |

## 8. Quellen

Herstellerseiten und Berichte wie verlinkt; Abruf 01.10.2026. Einige Quellen sind Drittberichte (z. B. AlternativeTo, MacRumors, 9to5Mac) – für Kaufentscheidungen Herstellerseiten prüfen. Zusätzlich die Quellen der [Konkurrenzübersicht](Glide_Konkurrenzuebersicht_und_persoenliche_Vorlieben_2026-10-01.md), Abschnitte 4–7. Glides Werte: Code 3.32.3, siehe [Bestandsaufnahme](Glide_Bestandsaufnahme_Code_und_Dokumentation_2026-10-01.md).

- Notion: [Release 2.53 Offline](https://www.notion.com/en-gb/releases/2025-08-19), [Release 3.2](https://www.notion.com/de/releases/2026-01-20), [3.3 Custom Agents](https://alternativeto.net/news/2026/2/notion-3-3-launches-custom-agents-for-autonomous-team-automation)
- Todoist: [Ramble](https://www.todoist.com/help/articles/from-voice-to-tasks-ramble-july-1), [TechCrunch](https://techcrunch.com/2026/01/21/todoists-app-now-lets-you-add-tasks-to-your-to-do-list-by-speaking-to-its-ai/), [Changelog 2026](https://www.todoist.com/help/articles/2026-changelog), [MCP-Server](https://mcpservers.org/remote-mcp-servers/todoist)
- Things: [3.23](https://macrumors.com/2026/08/19/things-3-23-brings-long-requested-overhaul-of-repeating-to-dos), [iOS 27](https://macrumors.com/2026/09/14/things-3-updated-for-ios-27)
- TickTick: [8.0](https://alternativeto.net/news/2026/1/ticktick-8-0-adds-suggested-tasks-improved-yearly-monthly-views-and-customization-options/), [Release Notes](https://releasebot.io/updates/ticktick)
- Apple: [Erinnerungen iOS 27](https://9to5mac.com/2026/06/12/heres-everything-new-for-reminders-in-ios-27/), [Notizen/Erinnerungen](https://www.apfelpatient.de/en/news/apple-brings-smart-updates-for-reminders-and-notes)
- AFFiNE: [GitHub](https://github.com/toeverything/affine), [Whiteboard](https://affine.pro/blog/interactive-whiteboard-app), [Vergleich](https://fabric.so/comparison/affine-vs-notion)
- AppFlowy: [Funktionen](https://mintlify.com/AppFlowy-IO/AppFlowy/features)
- Obsidian: [1.10 Bases](https://obsidian.md/changelog/2025-10-01-desktop-v1.10.0/)
- Logseq: [DB-Stand 05/2026](https://discuss.logseq.com/t/whats-new-with-logseq-db-may-16th-2026/35020), [2.0 Beta](https://kompozy.io/reviews/logseq-2-0)
- Capacities: [Termine und Tagesnotizen](https://docs.capacities.io/reference/dates-and-daily-notes)
- Heptabase: [Roadmap](https://wiki.heptabase.com/roadmap)
- Super Productivity: [Produkt](https://super-productivity.com/), [Lokal-first-Vergleich 2026](https://super-productivity.com/blog/best-local-first-todo-apps-2026/)
- Microsoft Planner: [Änderungen 2026](https://www.neowin.net/amp/microsoft-confirms-major-2026-update-to-remove-several-planner-features-add-new-ones/)
- Sunsama: [Überblick 2026](https://efficient.app/apps/sunsama)
- Tcl/Tk: [9.1](https://www.tcl-lang.org/software/tcltk/9.1.html), [TIP 733 Barrierefreiheit](https://core.tcl-lang.org/tips/doc/main/tip/733.md)
- Python: [macOS-Installer mit Tk 9.0.3](https://discuss.python.org/t/python-org-macos-installer-users-of-tkinter-python-3-14-with-tcl-tk-9-0-3-instead-of-8-6-17/107206)

## Primärquellen-Nachprüfung beim lokalen Start 3.33.0

Am 01.10.2026 geprüft: [Notion 3.2](https://www.notion.com/releases/2026-01-20) bestätigt mobile AI Notes/Agenten; [Things macOS](https://culturedcode.com/things/support/articles/1100684/) bestätigt frühes Erledigen von Wiederholungen ab 3.23 (21.08.2026) und die beschriebenen Erweiterungen ab 3.24. [Tcl/Tk 9.1](https://www.tcl-lang.org/software/tcltk/9.1.html) nennt jetzt 9.1.0 vom 29.09.2026 statt nur eine geplante stabile Veröffentlichung. Das erfüllt den externen Veröffentlichungsanlass für N12, aber nicht Glides Paket- und Bedienabnahme. Glide 3.33.0 bleibt auf der vorhandenen geprüften Laufzeit; keine Installation/Abhängigkeit daraus abgeleitet. Andere Wettbewerbszeilen wurden in diesem Schnitt nicht erneut vollständig verifiziert.
