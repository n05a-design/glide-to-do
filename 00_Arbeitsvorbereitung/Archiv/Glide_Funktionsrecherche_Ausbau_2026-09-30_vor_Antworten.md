# Glide – Funktionsrecherche für den Ausbau

Stand 30.09.2026 · Glide 3.31.0 · Aufgabenformat 20 · Entscheidungsvorlage, Antworten offen

Auftrag vom 30.09.2026: Recherche zu neuen oder erweiterten Funktionen für einen
größeren Funktionsumfang.

**So antworten:** „Alle Empfehlungen“ reicht. Sonst je Nummer, etwa
„G03 ja, G11 später, G20 nein“. Die Antworten gehören in Abschnitt 12.

## 1. Vorgehen und Rahmen

- **Grundlage:**
  - die [Wettbewerbsrecherche vom 25.09.2026](Glide_Wettbewerbsrecherche_Modernisierung_2026-09-25.md)
    zu Notion, Trello, OneNote, FigJam, Planner, Affinity und Pixel-Werkzeugen;
  - die offenen Punkte F1–F11 und E1–E6 der
    [Übersicht vom 29.09.2026](Glide_Uebersicht_und_Entscheidungen_2026-09-29.md).
  - F1 (Gliederung) und F2 (Aufklapp- und Hinweisblöcke) sind seit 3.31.0 umgesetzt.
- **Neu betrachtet:**
  - Aufgabenplaner: Todoist, TickTick, Things;
  - Tagesplaner: Sunsama, Akiflow;
  - Wissensablagen: Obsidian, Capacities, Anytype;
  - Notion-Neuerungen 2026;
  - Pixel-Werkzeuge: Pixelorama, Aseprite;
  - Technik: Suchindex, Synchronisierung, Oberflächen-Toolkit.
- **Abgleich mit dem Code 3.31.0**, damit nichts Vorhandenes doppelt vorgeschlagen wird.
  - Schon da: Verweise und Rückverweise zwischen Punkten, Zeitblöcke in der
    Tagesplanung, Wochenrückblick, Kachelvorschau und Symmetrie beim Zeichnen,
    Wiederholungen, Stimmung im Notizbuch.
  - Fehlt: Verweise zwischen Seiten, Eisenhower-Matrix, Fokus-Timer,
    Gewohnheiten, Volltextindex, Animation, Verschlüsselung und Erfassen von
    außerhalb der App.
- **Produktgrenzen bleiben:**
  - lokal, ohne Konto, Cloud und Telemetrie;
  - keine neue Laufzeitabhängigkeit ohne dokumentierte Entscheidung;
  - Funktionen leben in der Seitenansicht, nicht in Zusatzfenstern;
  - keine Form ohne Funktion.
  - Vorschläge, die eine dieser Grenzen berühren, sind als **Grenze** markiert.

Aufwand: S bis ein halber Tag, M bis zwei Tage, L mehr, XL mehrere Wochen.

## 2. Was der Markt 2026 zeigt

- **Aufgabenplaner:**
  - TickTick hat 2026 eine Eisenhower-Matrix als Ansicht eingeführt: Aufgaben
    per Ziehen in vier Felder nach dringend und wichtig.
  - TickTick ergänzte außerdem eine Kartenansicht am Desktop und eine
    Schnittstelle für KI-Assistenten (MCP).
  - Todoist lebt von der Schnelleingabe in Alltagssprache: „jeden Freitag“,
    „morgen 14 Uhr“, dazu Projekt und Label im selben Satz.
  - Things fehlt genau das; es wird dort am meisten vermisst.
- **Tagesplaner:**
  - Sunsama führt morgens durch die Planung: Aufgaben holen, Absicht setzen,
    Dauer schätzen.
  - Abends folgt ein Tagesabschluss: was erledigt ist, was liegen blieb, was
    morgen kommt.
  - Akiflow gruppiert Aufgaben in „Slots“ innerhalb eines Zeitblocks.
- **Wissensablagen:**
  - Obsidian: lokale Markdown-Dateien mit beidseitigen Verweisen `[[Seite]]`,
    Rückverweisen und Graph.
  - Capacities und Anytype denken in Objekten; Anytype ist lokal und
    verschlüsselt.
- **Notion 2026:**
  - Registerkarten-Block auf Seiten;
  - Feed-Ansicht als Blog-Strom;
  - Dashboards;
  - Titelbilder aus Museumssammlungen (Netz).
- **Pixel-Werkzeuge:**
  - Pixelorama 1.1 hat Kachel-Ebenen (rechteckig, isometrisch, sechseckig).
  - Außerdem: indizierte Farben, Textwerkzeug, Projektpaletten mit
    Rückgängig und Aseprite-Paletten.
  - Animation mit Zeitleiste, Zwiebelhaut und Bild-Markierungen.
- **Technik:**
  - SQLite (in Python enthalten) bringt mit FTS5 einen Volltextindex mit
    Rangfolge und Textausschnitten; tippfehlertolerant ist er nicht.
  - Synchronisierung ohne Konflikte (CRDT, etwa Automerge) ist ausgereift,
    für Python aber ohne gepflegte Bibliothek.
  - Bei Oberflächen-Toolkits gilt PySide6 (Qt 6) als Standard für große
    Desktop-Apps, Tkinter als Lösung für kleine Werkzeuge.

## 3. Erfassen und Planen

| Nr. | Funktion | Nutzen | Vorbild | Stand in Glide | Empfehlung | Aufwand |
|---|---|---|---|---|---|---|
| G01 | **Alltagssprache in der Eingabezeile**, erweitert: „jeden Montag“, „alle 2 Wochen“, „morgen 14 Uhr“, „#Label“, „!hoch“ | schneller erfassen; ersetzt F7 und geht darüber hinaus | Todoist | „/heute“, „/morgen“, Wochentage; Wiederholungen nur im Dialog | **ja** – deutsche Grammatik, erkannte Teile farbig in der Zeile | M |
| G02 | **Eisenhower-Matrix** als Ansicht: vier Felder nach Priorität × Fälligkeit, Ziehen ändert beide | Entscheiden statt Sammeln | TickTick 2026 | Priorität und Fälligkeit vorhanden; Pinnwand kann Felder | **ja**, als Anzeigemodus der Pinnwand (kein neues Datenfeld) | M |
| G03 | **Tagesbeginn und Tagesabschluss** als geführter Ablauf in „Mein Tag“ | ruhiger Start, bewusstes Ende | Sunsama | „Tagesbeginn …“ und Wochenrückblick vorhanden, kein Abschluss | **ja**, Abschluss ergänzen: Erledigtes, Liegengebliebenes auf morgen, eine Notiz ins Notizbuch | S–M |
| G04 | **Zeitleiste des Tages**: Zeitblöcke als Spalte neben „Mein Tag“, Ziehen setzt Uhrzeit | Planen in der Zeit statt in der Liste | Sunsama, Akiflow | `time_blocks` berechnet Blöcke, zeigt sie aber nur als Text | **ja** | M–L |
| G05 | **Fokus mit Timer** (F8 + Pomodoro aus F9): eine Aufgabe groß, Zeit läuft, Pausen | konzentriert arbeiten; füllt `time_spent_minutes` | Things, TickTick | Zeiterfassung vorhanden | **ja**, eingebettet in die Ansicht, kein Zusatzfenster | M |
| G06 | **Gewohnheiten** mit Serie und Monatsraster (F9) | tägliche Routinen sichtbar | TickTick, Streaks | Wiederholungen; wiederkehrende Checklisten | **später**; zuerst G05 | M |
| G07 | **Erfassen von außerhalb**: systemweites Tastenkürzel öffnet eine Eingabezeile | Gedanken festhalten, ohne Glide zu suchen | Things, Todoist | nur innerhalb der App | **Grenze:** unter macOS braucht das PyObjC (neue Abhängigkeit) und die Bedienungshilfen-Freigabe. Empfehlung: **später**, mit dem Paket (E3) | M |

## 4. Seiten, Notizen und Wissen

| Nr. | Funktion | Nutzen | Vorbild | Stand in Glide | Empfehlung | Aufwand |
|---|---|---|---|---|---|---|
| G08 | **Seitenverweise `[[Seite]]` mit Rückverweisen** unten auf jeder Seite | Wissen verknüpfen; Notizbuch und Seiten wachsen zusammen | Obsidian, Notion | Punkte haben Verweise und Rückverweise, Seiten nicht | **ja** – „[[“ öffnet die Seitenauswahl, Umbenennen zieht nach | M–L |
| G09 | **Titelbild für Seiten**, auch als Pixelzeichnung (F4), danach Bibliothek als Galerie (F5) | Wiedererkennung; stärkt die Pixel-Nische | Notion | Bilder in Seiten, Galerie für Anhänge | **ja**, ohne Netzbilder | M + M |
| G10 | **Registerkarten-Block** in Seiten | lange Seiten gliedern ohne Unterseiten | Notion 2026 | Aufklapplisten seit 3.31.0 | **nein vorerst** – Aufklapplisten und Gliederung decken den Bedarf; Registerkarten brächten einen zweiten Weg | – |
| G11 | **Vorlagen mit Platzhaltern** (`{{Datum}}`, `{{Wochentag}}`, `{{KW}}`) | Tagesnotizen und Protokolle vorausgefüllt | Obsidian, Notion | Vorlagen ohne Platzhalter | **ja** | S |
| G12 | **Spalten in Seiten** (F3) | Text neben Text | Notion | Textfeld trägt das nur eingeschränkt | **nein** (wie am 29.09.) | L |
| G13 | **Graph aller Verweise** | Überblick über Wissen | Obsidian | – | **nein** – Schmuck ohne Arbeitsnutzen; Rückverweise (G08) reichen | – |

## 5. Suchen und Wiederfinden

| Nr. | Funktion | Nutzen | Vorbild | Stand in Glide | Empfehlung | Aufwand |
|---|---|---|---|---|---|---|
| G14 | **Volltextindex** über Punkte, Notizen, Seiten und Anhänge-Namen, mit Textausschnitt und Hervorhebung | große Bestände schnell durchsuchen | Obsidian, Anytype | Suche geht linear durch den Bestand | **ja** – SQLite FTS5 aus der Standardbibliothek, als abgeleiteter Index im Cache (nie die Datenquelle), Tippfehlertoleranz über die vorhandene unscharfe Suche | M |
| G15 | **Filter in Alltagssprache** („offen, Label Arbeit, diese Woche“) | gespeicherte Filter schneller anlegen | Todoist | gespeicherte Filter vorhanden | **später**, nach G01 (gleicher Parser) | M |

## 6. Pixel-Werkstatt (Nische)

| Nr. | Funktion | Nutzen | Vorbild | Stand in Glide | Empfehlung | Aufwand |
|---|---|---|---|---|---|---|
| G16 | **Symbol-Export ICO und Favicon** 16/32/48 (F10) | eigene App- und Website-Symbole | – | PNG-Export | **ja**, schnellster Gewinn der Nische | S |
| G17 | **Animation**: Bilder (Frames), Zwiebelhaut, Vorschau, Export als GIF und Spritesheet | Figuren und kleine Animationen – der häufigste Wunsch in Pixel-Werkzeugen | Aseprite, Pixelorama | Einzelbild | **ja, als eigene Etappe** – Datenformat 21 (Frames in der Zeichnung), GIF über Tk 9 | L |
| G18 | **Kachel-Modus** mit Kachelsatz (Tileset) | Spielgrafik und Muster | Pixelorama | Kachelvorschau ohne Kachelsatz | **später**, nach G17 | L |
| G19 | **Indizierte Farben**: Palette ändern färbt die Zeichnung um | Farbvarianten einer Figur in Sekunden | Aseprite, Pixelorama | „Farbe ersetzen“ je Farbe | **ja** | M |
| G20 | **Aseprite-Paletten importieren** (`.aseprite`, `.ase`) | vorhandene Paletten weiter nutzen | Pixelorama | GPL und HEX | **ja**, klein | S |

## 7. Daten, Sicherheit und Austausch

| Nr. | Funktion | Nutzen | Vorbild | Stand in Glide | Empfehlung | Aufwand |
|---|---|---|---|---|---|---|
| G21 | **Import aus Notion und Todoist** (F6), Export des ganzen Bestands als Markdown-Ordner | Umzug ohne Abtippen; Daten bleiben lesbar | Obsidian (Dateien) | Seiten nehmen Markdown an; Austauschformat | **ja**, zuerst Notion-Markdown-Export (ZIP) und Todoist-CSV | M |
| G22 | **Verschlüsselte Ablage** mit Passwort | Schutz bei Verlust oder in Cloudordnern | Anytype | – | **Grenze:** braucht eine Kryptobibliothek (neue Abhängigkeit) und ein Passwortkonzept ohne Wiederherstellung. Empfehlung: **Forschung**, erst mit dem Paket | L |
| G23 | **Zwei Geräte gleichzeitig** über Konfliktzusammenführung (CRDT) | kein „nacheinander arbeiten“ mehr | Anytype, Automerge | Belegungsdatei, nacheinander | **nein vorerst** – keine gepflegte Python-Bibliothek, großer Umbau des Datenmodells | XL |
| G24 | **Lokale Schnittstelle für KI-Assistenten** (MCP über stdio, ohne Netz), nur lesend oder mit Bestätigung | Aufgaben mit einem lokalen Assistenten besprechen | TickTick 2026 | „Für KI bereitstellen“ als Export | **Frage an dich** – kein Netz nötig, berührt aber „keine KI-Automatik“ aus der Recherche vom 25.09. | M |

## 8. Plattform und Produktion

| Nr. | Funktion | Nutzen | Stand | Empfehlung | Aufwand |
|---|---|---|---|---|---|
| G25 | **Tempo-Grenze von Tk**: ein Bild kostet in reinem Tk rund 50 ms; Glide liegt beim 1,5- bis 2,5-Fachen | flüssiges Scrollen wie in nativen Apps | Tk 9, gemessen in `test_tempo330` | **Forschung:** Probe mit PySide6 an einer Ansicht (Liste mit 85 Zeilen, Startseite mit Verlauf), gleiche Messung. Erst danach über einen Wechsel entscheiden; ein Wechsel wäre XL und setzt E1 (Aufteilen) voraus | M (Probe) |
| G26 | **App-Paket** mit eingebettetem Python (E3), danach Signatur | Weitergabe ohne installiertes Python | Entwicklungsbundle | **ja, vorbereiten** (wie 29.09.) | M |
| G27 | **Aufteilen von `app.pyw`** (E1, E2) | Voraussetzung für G25, G17 und schnelleres Arbeiten | 52.000 Zeilen | wartet auf Versionsverwaltung (Antwort vom 29.09.) | L |

## 9. Vorschlag für die Reihenfolge

| Etappe | Inhalt | Aufwand | Version |
|---|---|---|---|
| 1 | Schnelle Gewinne: G16 Symbol-Export, G11 Platzhalter, G20 Aseprite-Paletten, G03 Tagesabschluss | 2–3 Tage | 3.32.0 |
| 2 | Erfassen und Planen: G01 Alltagssprache, G02 Eisenhower-Matrix, G05 Fokus mit Timer | 1 Woche | 3.33.0 |
| 3 | Wissen: G08 Seitenverweise, G14 Volltextindex, G09 Titelbild und Galerie | 1–1,5 Wochen | 3.34.0 |
| 4 | Pixel-Etappe: G19 indizierte Farben, G17 Animation (Format 21) | 1,5–2 Wochen | 3.35.0 |
| 5 | Austausch: G21 Import und Markdown-Export; G04 Zeitleiste | 1 Woche | 3.36.0 |
| Forschung parallel | G25 Toolkit-Probe, G26 Paket; G07, G22, G24 nach deiner Antwort | – | – |

Jede Etappe endet wie bisher:

- Vollprüfung mit neuer Suite;
- Doku;
- Abgleich nach `07_Python-Versionen` und Neubau von `Glide.app` (SHA-256);
- neue Version.

## 10. Fragen, die nur du beantworten kannst

- **Q1 – Schwerpunkt:** Soll der Ausbau eher Planen (Etappe 2), Wissen
  (Etappe 3) oder die Pixel-Nische (Etappe 4) zuerst stärken?
  **Empfehlung:** Reihenfolge wie oben, weil Etappe 1 und 2 im Alltag sofort
  wirken.
- **Q2 – Neue Abhängigkeiten:** Dürfen für G07 (PyObjC) und G22 (Kryptobibliothek)
  Abhängigkeiten dazukommen, sobald es ein Paket gibt?
- **Q3 – KI-Schnittstelle (G24):** Lokal und ohne Netz – ja, nein oder nur lesend?
- **Q4 – Toolkit-Probe (G25):** Soll ich die PySide6-Probe als reine Messung
  bauen (außerhalb von Glide, ohne Nutzerdaten)?

## 11. Bewusst nicht vorgeschlagen

| Funktion | Vorbild | Grund |
|---|---|---|
| Zusammenarbeit, Kommentare, Zuweisung | Notion, TickTick | Konto und Server sind Produktgrenze |
| KI-Vorschläge, KI-Zusammenfassung, Sprache zu Text in der Cloud | TickTick, Notion | Netz und Datenschutz |
| Feed-Ansicht, Dashboards mit Kennzahlen | Notion 2026 | Team-Funktionen; die Startseite deckt den persönlichen Überblick |
| Titelbilder aus Netzsammlungen | Notion | automatischer Netzzugriff |
| Eigene Feldtypen, Datenbank-Baukasten | Notion | bleibt ZF-200 (wie 25.09.) |

## 12. Antworten des Inhabers

Offen.

| Nr. | Antwort | Umsetzung |
|---|---|---|
| G01–G27 | | |
| Q1–Q4 | | |
| Reihenfolge | | |

## Quellen

- [TickTick 8.0: Vorschläge, Jahres- und Monatsansicht (AlternativeTo, Januar 2026)](https://alternativeto.net/news/2026/1/ticktick-8-0-adds-suggested-tasks-improved-yearly-monthly-views-and-customization-options/)
- [TickTick vs. Things 3 (ClickUp, 2026)](https://clickup.com/blog/ticktick-vs-things3/) und [TickTick-Überblick 2026](https://clickup.com/learn/topic/task-management/tools/ticktick/)
- [Todoist vs. TickTick (Asian Efficiency, Juli 2026)](https://www.asianefficiency.com/task-management/todoist-vs-ticktick/)
- [Todoist: Datum und Uhrzeit](https://todoist.com/help/articles/205325931) · [Todoist: wiederkehrende Termine](https://todoist.com:443/help/articles/360000636289)
- [Sunsama vs. Akiflow (Morgen, 2026)](https://www.morgen.so/blog-posts/sunsama-vs-akiflow) · [Akiflow vs. Sunsama (Toolfinder)](https://toolfinder.com/comparisons/sunsama-vs-akiflow)
- [Obsidian vs. Anytype (The Business Dive, 2026)](https://thebusinessdive.com/obsidian-vs-anytype) · [Top-10 Notiz-Apps 2026](https://guptadeepak.com/tools/top-10-note-taking-pkm-apps-2026/)
- [Notion Releases 2.52](https://www.notion.com/releases/2025-07-10) · [Notion Release-Highlights](https://releases.sh/notion/notion-releases/highlights)
- [Pixelorama v1.1: Kachel-Ebenen, indizierte Farben, Text](https://orama-interactive.itch.io/pixelorama/devlog/913933/pixelorama-v11-is-out) · [Pixelorama v1.1.5](https://orama-interactive.itch.io/pixelorama/devlog/1025693/pixelorama-v115-is-out)
- [SQLite FTS5](https://sqlite.org/fts5.html)
- [Automerge](https://automerge.org/docs/hello/) · [Automerge Repo](https://automerge.org/blog/automerge-repo/)
- [quickmachotkey (globale Tastenkürzel unter macOS)](https://pypi.org/project/quickmachotkey)
- Vergleich der Python-Oberflächen 2026 (PySide6, Flet, Tkinter): [Unite.AI](https://www.unite.ai/?p=362242)
