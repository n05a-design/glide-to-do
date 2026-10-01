# Glide – Arbeits- und Featureplanung nach Recherche und Codeabgleich

Stand 01.10.2026 · Glide 3.32.3 · Basisanalyse 3.32.0, Klappkorrektur 3.32.1 · Aufgabenformat 20

**Empfehlung:** Zuerst die sichtbaren Editorprobleme prüfen und die teuren
Ansichtsaufbauten optimieren. Danach die bereits gewählte Reihenfolge
**Planen → Wissen → Pixel → Austausch** fortsetzen. Vorhandene Funktionen
werden erweitert; sie stehen nicht erneut als Neuentwicklung im Backlog.

Die ursprüngliche Recherche und die Messungen beziehen sich auf 3.32.0.
Die Antworten des Inhabers D01–D06 sind jetzt verbindlich eingetragen;
D07 ist nach Begriffserklärung noch offen. D08 beauftragt die Kontrolle
aller Klappmechanismen und bessere Prüfungen. Die Korrektur wird als 3.32.1
geführt; Nachweise und Grenzen stehen im
[Klappkontrollbericht](../01_Repository/Glide/docs/69_KLAPPKONTROLLE_3.32.1.md).
Frühere Dokumente und zitierte Chat-Aufträge sind historische Belege.
Die Performance-Abschlussaufgabe bleibt wörtlich in Abschnitt 9 erhalten.

## 1. Welche Unterlagen einbezogen wurden

| Grundlage | Verwendung in dieser Planung |
|---|---|
| [Arbeitsvorbereitung Modernisierung](Glide_Arbeitsvorbereitung_Modernisierung_2026-09-25.md), [Aufgabenkatalog](Glide_Aufgabenkatalog_Modernisierung_2026-09-25.md), [Sitzungslehren](Glide_Sitzungsprotokoll_und_Lehren_2026-09-24_bis_26.md) | Arbeitsregeln, gewählte Pakete, Datenstrategie und Lehren aus früheren Fehlern |
| [Gesamtanalyse 16.09.](Archiv/Glide_Gesamtanalyse_2026-09-16.md), [Feature-Gap-Analyse 18.09.](Archiv/Glide_Feature_Gap_Analyse_2026-09-18.md) | Historische Versionsanalyse und Architekturentwicklung; damalige Lücken neu gegenprüfen |
| [Konkurrenzanalyse 17.09.](Archiv/Glide_Konkurrenzanalyse_2026-09-17.md), [Wettbewerbsrecherche 25.09.](Glide_Wettbewerbsrecherche_Modernisierung_2026-09-25.md), [Funktionsrecherche 30.09.](Glide_Funktionsrecherche_Ausbau_2026-09-30.md) | Wettbewerbsbefund, bestehende G-Kennungen und bereits beantwortete Entscheidungen |
| [Übergabe für den aktuellen Chat](Glide_Sitzungsuebergabe_2026-09-30.md), [technische Projektübergabe](../01_Repository/Glide/docs/09_PROJECT_HANDOFF.md) | Tatsächliche Einstiegspfade und nächste Etappen |
| [Änderungsverlauf](../01_Repository/Glide/CHANGELOG.md), [Vertrag 66](../01_Repository/Glide/docs/66_MODERNISIERUNG_3.30.0.md), [Vertrag 68](../01_Repository/Glide/docs/68_AUSBAU_3.32.0.md) | Versionsvergleich 3.30, 3.31 und 3.32 |
| [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md), [Architektur](../01_Repository/Glide/docs/02_ARCHITECTURE.md), [Datenvertrag](../01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md), [QA](../01_Repository/Glide/docs/07_QA_BERICHT.md) | Umsetzungsmöglichkeiten, Kompatibilität und Prüfgrenzen |
| Die fünf Bildschirmfotos vom 30.09.2026, 08:13:53, 08:14:01, 13:31:05, 13:34:00 und 13:34:14 | Sichtbare Fehler und Layoutzustände; keine Ableitung eines Stacktraces aus einem Bild |

### Versionsbefund

- **3.30:** Pixel-Werkstatt, Board, Seiten, Notizbuch, Galerie,
  Aufgabenverknüpfungen, Zeiterfassung und Stundenraster sind vorhanden.
- **3.31:** Gliederung, Aufklapp- und Hinweisblöcke, gemeinsamer Seiten- und
  Notizeditor sowie Verbesserungen für Menüs, Ziehen und Scrollen.
- **3.32:** ICO-Export, Paletten aus Aseprite/Adobe, selbstfüllende
  Datumsplatzhalter und Tagesabschluss; zusätzlicher Schutz gegen den
  rekursiven Bildlayout-Aufruf und weitere Menü-Hänger.
- Die ältere Konkurrenzanalyse nennt Rich Text noch als fehlend; das ist
  für diese Code-Basis überholt. Die älteren Marktpreise werden nicht
  weiterverwendet.
- Historische Vollprüfung: 55 Suiten, Exitcode 0 am 30.09.2026. Das ersetzt
  keine Abnahme der nachfolgenden Bildschirmfotos oder anderer Plattformen.

## 2. Aktuelle Konkurrenzrecherche und Konsequenzen

Recherche am 30.09.2026 anhand offizieller Herstellerunterlagen. Die Spalte
„Für Glide“ ist unsere Ableitung, keine Aussage des jeweiligen Herstellers.

| Vorbild und belegte Funktion | Für Glide |
|---|---|
| [Todoist: Datum/Uhrzeit aus der Eingabe erkennen, Erkennung sichtbar zurücknehmen](https://www.todoist.com/help/todoist/features/schedule-a-date-and-time-for-your-todoist-tasks-q7VobO) | G01: eine kleine deutsche Grammatik mit Vorschau und abschaltbarer Erkennung; Fälligkeit und Bearbeitungstag ausdrücklich unterscheiden |
| [TickTick: Eisenhower-Matrix, Pomodoro und Gewohnheiten](https://www.ticktick.com/features) | G02 und G05 sind sinnvoll. Gewohnheiten G06 bleiben im Vorrat; das Einführungsjahr der Matrix wird nicht als „neu 2026“ behauptet |
| [Sunsama: Tagesabschluss](https://roadmap.sunsama.com/changelog/daily-shutdown) und [Weitertragen unvollständiger Aufgaben](https://help.sunsama.com/docs/getting-started/basics/task-rollover-and-recurring-tasks-the-basics/) | G03 ist erledigt. Glide soll die bewusste Tagesentscheidung erhalten; kein automatisches Verschieben von Fälligkeiten |
| [Obsidian: interne Links](https://obsidian.md/help/links) und [Rückverweise](https://obsidian.md/help/plugins/backlinks) | G08/G30: Projektwissen und Aufgaben über stabile Kennungen verbinden; Graph weiterhin zurückstellen |
| [Notion: verknüpfte Datenquellen, gemeinsame Inhalte mit eigenen Ansichten](https://www.notion.com/help/data-sources-and-linked-databases) | G28: vorhandene Aufgaben in einer Projektseite zeigen, ohne eine zweite Kopie ihres Status anzulegen |
| [Trello: Spiegelkarten](https://support.atlassian.com/trello/docs/mirroring-cards/) und [Planner: Gruppierung von Aufgaben](https://support.microsoft.com/en-us/planner/training/organize-your-team-s-tasks-in-microsoft-planner) | Eine Aufgabe darf in mehreren Ansichten auftauchen. Board und Gruppierungslogik sind schon da; Erweiterungen nutzen dieselben Objekte |
| [Aseprite: indizierte Farben](https://www.aseprite.org/docs/color-mode/) und [Animation mit Frames und Vorschau](https://www.aseprite.org/docs/animation/) | G19 auf Palettenbearbeitung begrenzen; G17 als eigene, begrenzte Animationsetappe behandeln |
| [Notion: Markdown-/CSV-Export als ZIP, Hinweisblöcke teilweise als HTML](https://www.notion.com/help/export-your-content) | G21 braucht eine Importvorschau mit Verlustbericht. Ein vorhandener Markdown-Parser ist noch kein vollständiger Notion-Importer |

Glides sinnvolle Position bleibt: ein lokales persönliches Arbeitswerkzeug
mit Aufgaben, Projektwissen und kleiner Pixel-Werkstatt. Konten,
Mehrbenutzerbetrieb und ein eigener Cloudservice sind weiterhin außerhalb
des Produkts. Zusammenarbeit oder cloudbasierte KI-Funktionen werden deshalb
nicht in diese Umsetzungsliste aufgenommen.

**Korrektur älterer Recherche:** Todoists offizielle Datumsdokumentation
nennt auch den Beginner-Tarif. Die alte Aussage, natürliche Datumerkennung
sei grundsätzlich eine Pro-Funktion, ist keine belastbare Vergleichsbasis.

## 3. Features gegen den tatsächlichen Code geprüft

Codebezug: [app.pyw](../01_Repository/Glide/src/glide/app.pyw),
[drawing.py](../01_Repository/Glide/src/glide/drawing.py),
[page_markdown.py](../01_Repository/Glide/src/glide/page_markdown.py).
Zeilenangaben beziehen sich auf den unveränderten Stand dieser Prüfung.

| Kennung | Tatsächlicher Stand | Verbleibender Umfang und Abnahme |
|---|---|---|
| G03/G11/G16/G20 | **Umgesetzt und erneut getestet**: Tagesabschluss, Platzhalter, ICO, Aseprite-/Adobe-Paletten | Aus dem offenen Backlog nehmen; nur bestehende manuelle Abnahme |
| G04 | **Vorhanden**: `time_blocks` 17107, `build_plan_grid` 17391, Ziehen 17491–17561 | Kein zweites Stundenraster entwickeln. Nur konkret nachgewiesene Bedienlücken aufnehmen |
| G01 | **Teilweise**: `parse_due_input` 36214, `parse_repeat_text` 36738; bestehende Schnell- und Slash-Erfassung | Gemeinsamen Parser erweitern. Erkennung vor Speichern anzeigen, Text unverändert zurücknehmen können; D01 entscheidet die Semantik |
| G02 | **Fehlt als Ansicht**; `ItemWorkspace`, `group_columns` und `set_group_value` liefern Bausteine | Vier Quadranten, Tastaturalternative zum Ziehen, ein Undo-Schritt. Ausdrückliche Terminkontexte verändern das passende Datumsfeld gemäß D02 |
| G05 | **Teilweise**: `running_timer` 46162, `start_time_tracking`, `stop_time_tracking`, `time_spent_minutes` vorhanden | Eingebettete Fokusansicht plus Pausen/Countdown. Eine laufende Erfassung, keine Doppelbuchung nach Pause, Wechsel oder Neustart |
| G29 | **Fehlt**: `NoteEditor.ALLOW_TASKS = False` 10507; Markdown-Aufgaben werden zu Aufzählungen | Notiztext und Aufgabenbereich müssen dieselben IDs zeigen. Das Umschalten eines Flags reicht nicht: `page_entry` und sämtliche Aufgabenwege erwarten heute die Seitenart |
| G31 | **Teilweise**: `move_items_to_list` 46949 vorhanden, aber abhängig von Baumzeilen | Eine Aufgabenzeile einer Seite besitzt keine normale Baum-Auswahl. Bewegung über IDs, Textreferenz zurücklassen; Undo, Löschen und Wiederherstellen müssen beide Ansichten erhalten |
| G32 | **Teilweise schon vorhanden**: `page_chips` 34318 zählt offen, erledigt und überfällig auch in Seiten | Nur Filter „aus Seiten“ und durchgängige Aktualisierung ergänzen. Keine zweite Zählerberechnung und keine zusätzliche Kennzahlenleiste |
| G08/G30 | **Fehlt für Seiten-/Listenverweise**; Punktverknüpfungen und `item_backlinks` vorhanden | IDs statt Titel als Referenz; Umbenennen, Verschieben, Papierkorb, Import mit ID-Neuzuordnung und „Ziel fehlt“ testen |
| G14 | **Kein FTS-Index**: `quick_open_results` 52256 durchsucht linear vor allem Titel/Punkttexte | Abgeleiteten Index für Titel, Notiz-/Seitentext und Anhangnamen einführen. Aufbau, Aktualisierung und Rückfall ohne FTS5 prüfen; Anhanginhalt ist ein eigener späterer Umfang |
| G09 | **Teilweise**: Seitenbilder, Galerie und Bibliothekstabelle vorhanden, Titelbild fehlt | Lokales Bild oder Pixelzeichnung als Cover; Bibliotheksgalerie darauf aufbauen. Nicht die vorhandene Anhanggalerie duplizieren |
| G28 | **Fehlt**: keine live eingebettete Liste im Seitendokument | Listen-ID plus Ansichtsangaben; dieselben Aufgaben ändern, keine Kopien. Verschachtelte Einbettungszyklen ablehnen |
| G19 | **Datenkern schon indiziert**: `DrawingModel.cells` enthält Palettenindizes; `to_png` 1150 schreibt indiziertes PNG; `replace_color` 1060 vorhanden | Paletteneintrag direkt bearbeiten, Farbvarianten und Paletten-Undo ergänzen. Index 0 ist heute fest weiß; Transparenz ist damit nicht bereits gelöst |
| G17 | **Fehlt**: kein Animationsmodell; „frames“ beim Aseprite-Import liest nur die Palette | Frame-Dauer, begrenzte Frame-Zahl, Vorschau und Spritesheet. Mehrbild-GIF-Export technisch nachweisen; Unterstützung einzelner GIF-Bilder reicht als Beleg nicht |
| G24/G21 | **Teilweise**: `.glideexchange`, Markdown, CSV, Vorschau und Importwege vorhanden | Kontextpaket, sicherer Änderungsabgleich und Herkunftszuordnung ergänzen; darauf Notion-/Todoist-Import aufbauen |

G07 (plattformeigene externe Erfassung), G12 (Seitenspalten), G13 (Graph)
und G23 (gleichzeitige Gerätebearbeitung) bleiben zurückgestellt bzw.
ausgeschlossen. G22 (Verschlüsselung) hat gemäß dokumentierter Entscheidung
keine Priorität. G06/G15/G18 bleiben Vorrat. Q5/G29 und die grobe Reihenfolge
sind bereits beantwortet und werden nicht erneut als offene Grundsatzfragen
gestellt.

### Datenformat als eigenes Arbeitstor

`RichNoteEditor.normalize` (8547) akzeptiert nur bekannte Formatbereiche,
Bildanker, Aufgabenreferenzen und HTTP-/Mail-Links. Unbekannte Inhalte werden
teilweise verworfen. Neue interne Links oder Einbettungsblöcke einfach unter
Format 20 zu speichern, wäre deshalb riskant: Eine ältere Fassung könnte sie
beim nächsten Speichern verlieren.

Vor G08/G28/G30 und neuen Cover-/Animationsdaten die Normalisierung älterer
Leser prüfen. Bei einer inkompatiblen Erweiterung: Schema anheben,
Vorsicherung, Migration und schreibgeschützten Altleser testen. **Format 21
ist nicht pauschal allein für Animation reserviert.** Kommt die erste
inkompatible Wissensfunktion früher, nutzt bereits sie das nächste Format;
die spätere Animation wird danach eingeordnet.

## 4. Bildschirmfotos und technische Befunde

| Beleg | Sicher sichtbar | Einordnung und nächste Prüfung |
|---|---|---|
| 08:13:53 und 08:14:01 | Seitenbilder mit verschiedenen Größen; anschließend Fehlermeldung | Kein Stacktrace und keine Versionsnummer im Bild. Der dokumentierte rekursive Bildlayout-Fehler passt als Hypothese; die Fotos allein beweisen seine Ursache nicht |
| 13:31:05 | Großer unterer Bildausschnitt; leere umrandete Fläche bei Textauswahl | Kandidaten: gespeicherte Bildbreite/Umfluss und schwebende Formatleiste. `sync_format_bar` 9778 ruft noch `update_idletasks()` auf; das verdient eine gezielte Reentranzprüfung, ist noch kein bestätigter Fehler |
| 13:34:00 und 13:34:14 | Startseite mit abweichender Lage bzw. Sichtbarkeit der Aktionsleiste | Scrollposition und Hover unterscheiden sich. Daraus folgt noch kein Layoutfehler; am oberen Rand und nach Rückkehr aus einer Seite reproduzieren |

**P0 für die nächste Implementierungsrunde:** Künstliche Seite mit zwei
lokalen Bildern anlegen, vergrößern/verkleinern, Text markieren, scrollen,
Ansicht wechseln und zurückkehren. Prüfungen: kein Rekursionsfehler, sichtbare
Werkzeuge bei Auswahl, keine stehenden leeren Überlagerungen, Bilder und
Text nicht unbeabsichtigt verdecken. Bildüberlappung B4 und Bildausgabe in
Druck/Markdown bleiben eigene offene Arbeiten.

Die aktuellen Kopien in `07_Python-Versionen` und `Glide.app` wurden gegen
die jeweiligen Kopier-/Paketregeln verglichen: **139 bzw. 53 Dateien
bytegleich**. Das belegt den aktuellen Abgleich auf der Festplatte; es sagt
nicht, welche ältere Instanz bei Aufnahme der Bildschirmfotos noch lief.
Echte Nutzdaten und das persönliche Fehlerprotokoll wurden nicht geöffnet.

## 5. Performance: Messung und priorisierte Optimierung

Nachweise und Prüfschritte:
[Ergebnis mit SHA-256](../01_Repository/Glide/tests/qa-3.32.0/recherche_planung_2026-09-30/ergebnis.json),
[Scrolltest](../01_Repository/Glide/tests/qa-3.32.0/recherche_planung_2026-09-30/test_tempo330.log),
[Ansichtswechsel mit Profil](../01_Repository/Glide/tests/qa-3.32.0/recherche_planung_2026-09-30/messung_ansichtswechsel.log),
[statische Analyse](../01_Repository/Glide/tests/qa-3.32.0/recherche_planung_2026-09-30/analyse_codebasis.log).

Umgebung: macOS, Python 3.14.5; die letzte Vollprüfung nennt Tk 9.0.3.
Tests/Messung verwenden temporäre Datenordner und künstliche Beispieldaten.
`app.pyw`: **54.050 Zeilen, 38 Klassen, 2.461 Funktionen**. Identisch ist
eine gefundene Gruppe von zwei Hover-Funktionen; ähnlich aussehender Code
wird nicht allein deshalb zusammengelegt.

| Ansicht | Scrollen, ms je Ereignis/Zeichendurchlauf | Wechsel, Median unter cProfile |
|---|---:|---:|
| Reine Tk-Vergleichsliste | 50,7 | – |
| Aufgabenliste | 77,1 | 263,3 |
| Tabelle | 25,9 | 327,5 |
| Seite | 81,0 | nicht im Wechsel-Fixture enthalten |
| Startseite mit Verlauf | 74,7 | 638,6, anderer Messablauf |
| Listen und Ordner mit Verlauf | 128,8 | 3.259,9, anderer Messablauf |
| Pinnwand | nicht gemessen | 876,0 |
| Mein Tag | nicht gemessen | 169,3 |
| Vorlagen | nicht gemessen | 661,4 |

**Grenzen der Messung:** Die Wechselwerte enthalten Profilaufwand und
mehrere Ereignisschleifendurchläufe; sie sind keine unverfälschten
Produktlatenzen. Je Ansicht werden nur drei warme Wechsel ausgewertet.
Das Wechsel-Fixture enthält 14 Aufgabenlisten und eine Zeichnung, keine
Seite/Notiz. Der Scrolltest prüft andere Daten und Zustände. Ein Lasttest mit
26.420 Punkten belegt bisher Speichern/Laden, nicht den Aufbau ebenso vieler
sichtbarer Zeilen. Für belastbare Zielzeiten fehlen noch unprofilierte
Serien, Bild-/Notiz-Fixtures, p95 und Speicherentwicklung.

Im Profil kostet `refresh_library_page` über drei Aufrufe kumulativ 9,644 s;
`ButtonFlow.reflow` läuft 960-mal und kostet kumulativ 1,766 s. Tk-Aufrufe
dominieren. Kumulative Zeiten enthalten Unteraufrufe und werden nicht
addiert. Das ist ein stärkerer Hinweis auf wiederholtes Aufbauen und Layouten
als auf teure Python-Dictionaryzugriffe.

| Arbeit | Konkrete Änderungsidee | Nachweis / Risiko |
|---|---|---|
| P01 – Messbasis | Warme/kalte Wechsel ohne Profil getrennt messen; Varianten mit/ohne Verlauf, 100/1.000/10.000 Punkte und Seiten mit mehreren Bildern | Erst danach verbindliche Millisekunden-Ziele; gleiche Daten, Fenstergröße und Laufzeit beim Vergleich |
| P02 – Schriften | `app_font` 202 fragt pro Aufruf Name, Familie und Größe bei Tk ab; 404 Aufrufstellen. Familien-/Größenwerte und benötigte Tupel zwischenspeichern | In `apply_ui_font` 23661 invalidieren; mehrere Tk-Interpreter, Designwechsel und Systemskalierung berücksichtigen. Beschleunigung erst nach Vorher/Nachher-Messung behaupten |
| P03 – Aufbau und Layout | Ursprünglicher Befund 3.32.0: Startseite/Bibliothek zerstören alle Kinder. 3.32.3 erhält unveränderte Bibliothekskarten innerhalb derselben Ansicht; Startseite und Aufbau großer Bestände weiter untersuchen | Tastaturfokus, Scrollposition, Hover, Auswahl, Drag-and-drop und Designwechsel bewahren; virtuelle Listen erst nach Messung, E6 ist für große UI-Bestände noch nicht abgeschlossen |
| P04 – Seitenbilder | Bestehenden `PreviewCache` weiterverwenden; Layout von bloßem Platzieren trennen; Neuberechnung nur bei geänderter Breite/Text/Bildgeometrie | Bereits vorhanden sind Größen-Cache und gebremstes Ziehen. Kein zweiter Bildcache; keine verschachtelte Ereignisschleife in Scroll-/Configure-Rückrufen |
| P05 – Gemeinsame Helfer | `DueField._add_hover` 2644 und `LabelDropdown._hover` 3407 zusammenführen; gleiche Beschriftungen zentral halten: Abbrechen 29×, Alle Dateien 26×, Übernehmen 13× | Wartbarkeit, kein versprochener FPS-Gewinn; Signatur, Bindungen und dynamische Designfarbe erhalten |
| P06 – Speichern/Aktualisieren | `save_items` 37280 schreibt atomar und aktualisiert die Seitenleiste; `save_settings` 16423 schreibt ebenfalls. Mehrfache identische Schreib-/Refresh-Anforderungen je Aktion erfassen und reduzieren | `item_change`, `sidebar_change`, Sperrdatei, Sicherungen, `fsync`, Undo und Fehleranzeige bewahren. Kein ungesichertes Verzögern von Nutzdaten |
| P07 – Suche | G14 mit bestehender Suche verbinden; FTS5 nur als jederzeit neu aufbaubaren lokalen Cache | FTS5 hier in SQLite 3.50.4 verfügbar, aber pro Paket beim Start prüfen. Indexfehler dürfen Datenöffnung nicht verhindern |

**Schnelle Lösung:** P01/P02/P05, gezieltes Zusammenfassen redundanter
Layout-Rückrufe und P0 reproduzieren. Gemeinsame Konstanten für UI-Texte,
Abstände oder Zeitintervalle nur dort, wo ihre Bedeutung tatsächlich gleich
ist. Schlüssel wie `planned_date` und alle `theme[...]`-Zugriffe pauschal in
Variablen zu verwandeln bringt keinen belegten Performancegewinn.

**Saubere Lösung:** P03/P04/P06, eindeutig invalidierte Caches und teilweise
aktualisierte Ansichten. Der vorhandene `render_pass` bleibt die Grundlage;
keinen dauerhaften Kennzahlen-Cache ohne vollständige Invalidierung ergänzen.
Neue Parser-/Suchlogik möglichst als Modul ohne Tk-Abhängigkeit hinzufügen.

**Professionelle Langfristlösung:** Daten- und Fachlogik schrittweise von
der Oberfläche trennen, Versionsverwaltung und Plattformprüfung vorbereiten,
danach gegebenenfalls Toolkit-Probe G25. Die bestehende Entscheidung
„Git vorerst nicht“ wird hier nicht aufgehoben. Ohne diesen neuen Beschluss
bleibt eine große Monolith-Aufteilung zurückgestellt.

### Toolkit-Probe ist eine Entscheidung, keine Sofortmaßnahme

Die gemessenen rund 50 ms der reinen Tk-Liste sind **keine allgemeine
Tk-Untergrenze**; schon die Glide-Tabelle liegt hier darunter. Auch ein
Qt-/Flet-Wechsel garantiert keine 60 FPS oder einen passenden Texteditor.

[Qt beschreibt iOS-Deployment mit PySide6/Qt 6.12](https://www.qt.io/blog/python-mobile-app-development-bringing-pyside6-on-ios),
einschließlich Simulator und erzeugtem Xcode-Projekt; Einschränkungen
betreffen unter anderem Drittanbieterpakete. Die ältere Recherche mit
„kein Simulator, Xcode-Projekt von Hand“ wird daher nicht fortgeschrieben.
[Flet dokumentiert iOS-Paketierung](https://flet.dev/docs/publish/ios/)
auf macOS mit Xcode. Build-Voraussetzungen und Signatur für die Verteilung
sind getrennt von der gewünschten plattformübergreifenden Nutzung.

**Entscheidung D03:** Mobile Nutzung liegt weit außerhalb des aktuellen
Fokus. Die Toolkit-Probe G25 und iPhone/iPad-Arbeit sind zurückgestellt.
Zuerst wird die vorhandene Desktop-Anwendung mit Tk verbessert.

## 6. Entscheidungen des Inhabers und offene Punkte

Maßgeblich sind die Antworten vom 30.09.2026. Frühere Empfehlungen in
Dokumenten ändern diese Festlegungen nicht.

| Nr. / Bezug | Verbindliche Festlegung | Status |
|---|---|---|
| D01 / G01 | Allgemeine Datumsangaben wie „morgen“ setzen den **Bearbeitungstag**. „fällig“/„bis“ benennt die Fälligkeit. Erkannte Felder werden vor Speichern angezeigt und bleiben rücknehmbar. | entschieden; Parser-Ausbau geplant |
| D02 / G02, Drag-and-drop | Beim Ziehen in einen ausdrücklich erkennbaren neuen Terminkontext muss die erwartbare Terminänderung erfolgen. Allgemein müssen Aktionen die erkennbar zugehörige Wirkung haben. | Grundsatz entschieden; im jeweiligen UI-Vertrag konkretisieren |
| D03 / G25 | Mobile Nutzung ist weit weg und aktuell kein Fokus. Desktop/Tk verbessern; keine Mobile- oder Toolkit-Probe in der nächsten Runde. | zurückgestellt |
| D04 / B1/B2 | Zunächst die **bestehenden** Bereiche der Seitenleiste um Drag-and-drop erweitern, besonders Seiten und Notizen. | umgesetzt 3.32.2; native Drag-Bindungen aller bestehenden Inhaltsbereiche |
| D05 / F11, G29/G31 | Einzelne Aufgaben in **Notizen und Seiten** unterstützen. Liste, Notiz und Seite behalten ihren Zweck und Typ; keine allgemeine Formatkonvertierung. | entschieden; Aufgaben-/Referenzwege in Paket B |
| D06 / Hinweisblock | **Keine Gestaltungsänderungen** an den Hinweisen. | entschieden; Gestaltungsvarianten aus dem aktiven Backlog entfernt |
| D07 / G17 | Begriffserklärung angefordert; noch keine Auswahl des Exportumfangs. | offen, siehe unten |
| D08 / Klappkontrolle | Alle Klappmechanismen kontrollieren, Labelgruppen korrigieren und bessere Kontrollmechanismen einführen. | Korrektur 3.32.1; [Bedienproben und Prüfstand](../01_Repository/Glide/docs/69_KLAPPKONTROLLE_3.32.1.md) |

**D02 als Implementierungsvertrag:** Ziehen auf einen Bearbeitungstag setzt
`planned_date`, auf einen Zeitblock zusätzlich `planned_time`; Ziehen auf
einen ausdrücklich bezeichneten Fälligkeitstermin setzt `due` bzw.
`due_time`. Ein neutraler Listen-/Ordnerwechsel ändert diese Felder nicht.
Der Zielkontext und das geänderte Feld müssen vor dem Loslassen erkennbar
sein. Eine Aktion erhält einen gemeinsamen Undo-Schritt. Bei der
Eisenhower-Matrix ist die konkrete Abbildung der Quadranten zuerst im
UI-Vertrag festzuhalten: Ein abstraktes „nicht dringend“ nennt noch keinen
neuen Termin. Die Antwort ist keine pauschale Erlaubnis zum Löschen von
Abgabeterminen.

**D07 verständlich:** Eine Animation besteht aus mehreren Pixelbildern
(Frames), die mit einer Dauer nacheinander abgespielt werden. Ein animiertes
GIF exportiert diese Folge als einzelne `.gif`-Datei, die sich außerhalb von
Glide abspielen lässt, zum Beispiel ein winkendes Symbol. Ein Spritesheet
exportiert die Frames nebeneinander in **eine PNG-Datei**; es ist ein
Bildatlas und spielt von sich aus keine Animation ab.

**Noch zu entscheiden:** Muss die erste Animationsetappe bereits ein
abspielbares GIF liefern, oder reichen zunächst Frames, Vorschau und
Spritesheet? Empfehlung weiterhin: zunächst Frames/Vorschau/Spritesheet,
GIF anschließend nach Mehrbild-Exportnachweis. Bis zur Antwort bleibt D07
offen; die technische Vorbereitung kann ohne Festlegung auf ein Exportformat
geplant werden.

**Weiterhin nur durch den Inhaber:** Inhaberangaben/Lizenz, Signatur-/Store-
Konten, Markenprüfung und Windows-/Linux-Abnahme. Einzelheiten stehen in der
[Übersicht vom 29.09.](Glide_Uebersicht_und_Entscheidungen_2026-09-29.md)
und im [Produktregister](../01_Repository/Glide/docs/decisions/PRODUCT_IDENTITY.md).
Git bleibt nach bestehendem Beschluss vertagt. F11 ist durch D05 beantwortet,
Hinweisvarianten durch D06 und die aktuelle Toolkit-Frage durch D03.

## 7. Umsetzungsplan mit Abhängigkeiten und Abnahme

Aufwand ist eine Planungsschätzung für Implementierung, Tests und Doku;
kein Liefertermin. Manueller Plattformtest und eventuelle Migrationen kommen
hinzu. Die bestehenden Zielversionen sind Reservierungen, keine Freigaben.

| Paket | Umfang und Reihenfolge | Voraussetzung | Fertig, wenn … | Grober Aufwand |
|---|---|---|---|---|
| A – Stabilisieren | D08 Klappkontrolle (3.32.1), D04 Seiten-/Notiz-Drag; P0 Editor/Bilder; P01 Messbasis; P02/P05; danach teuerste Pfade P03/P04/P06 | aktuelle Kopien und isolierte Tests | nachgewiesene Fehler geschlossen, Messprotokoll vor/nach, keine Fokus-/Scroll-/Datenregression | 2–5 Arbeitstage, abhängig vom Befund |
| B – Planen, Ziel 3.33 | G01 → G05; G29 Einzelaufgaben in Notizen/Seiten; G31; Rest von G32; G02 mit explizitem Zielkontext | A; D01/D02/D05; ID-basierte Aufgabenwege | eine Aufgabe in Text und Liste, stabile Planung/Fälligkeit, einmalige Zeitbuchung, Undo und Tastaturwege | 5–9 Arbeitstage |
| C – Wissen, Ziel 3.34 | gemeinsame Referenzschicht G08/G30 → G28; G14; G09 mit Bibliotheksgalerie | B; Datenformat-Prüfung vor dem ersten neuen Dokumentinhalt | Umbenennen/Import/Papierkorb verlieren keine Verweise; Einbettungen verwenden Originalpunkte; Suchindex ist ersetzbar | 7–12 Arbeitstage |
| D – Pixel, Ziel 3.35 | G19 Palettenbearbeitung → G17 Animation | A; D07; Migrationsvertrag | Paletten-Undo, Bestand bleibt lesbar, Frame-/Dateigrenzen, reproduzierbarer Export | 7–12 Arbeitstage |
| E – Austausch, danach | G24 Kontextpaket → Markdown/Felder → Änderungsdiff → G21 Notion/Todoist | Referenzen und Modell aus C | Vorschau zeigt Verluste und Zieländerungen; veraltete Vorschläge überschreiben nichts still; begrenzter Import und Undo | 5–10 Arbeitstage |
| F – Produktionsweg | Desktop-Verpackung G26, dann Signatur/Store; G25/Mobile zurückgestellt | Inhaberangaben, Plattformabnahme, getrennte Abhängigkeitsentscheidung | reproduzierbare Pakete und dokumentierte Geräteprüfung | separat schätzen |

**Abhängigkeiten:** B und C werden nicht gemeinsam in einen großen Patch
gepackt. G31/G28 brauchen gemeinsame Referenzregeln, damit Löschen einer
Textzeile nicht versehentlich die Aufgabe in ihrer anderen Liste löscht.
G14 darf technisch vorbereitet werden, ohne bereits C als erledigt zu
melden. Vorratsideen bleiben hinter den gewählten Paketen.

## 8. Arbeitsablauf je Implementierungsrunde

1. **Konkreten Umfang wählen:** Paket und Teilaufgaben notieren, offene
   Detailentscheidung aus Abschnitt 6 prüfen; keinen offenen Beschluss
   automatisch durch eine Empfehlung ersetzen.
2. **Baseline sichern:** Quellstand und startbare Arbeitskopie archivieren,
   SHA-256 festhalten; bestehende Einzelsuiten vor der Änderung ausführen.
   Alle Tests mit temporärem `GLIDE_DATA_DIR`, keine echten Daten kopieren.
3. **Datenvertrag zuerst:** Bei neuen Dokumentinhalten Altleser,
   Normalisierung, Backup, Import, Migration und Rückfall festlegen. IDs und
   Quellen sind stabil; Daten haben jeweils eine maßgebliche Stelle.
4. **Kleinen Schnitt implementieren:** Neue reine Fachlogik als Modul;
   Mutationen über `item_change`/`sidebar_change`, Umbau zusätzlich geschützt,
   modale Dialoge über `run_modal`. Vorhandene Caches und Komponenten nutzen.
5. **Gezielt prüfen:** Speichern/Laden, Undo, Papierkorb, Import und die
   betroffene UI. Klappbedienwege mit echten Pfeilklicks, nativen
   Tastaturbindungen, Neuaufbau und Callbackfehler-Erfassung prüfen; direkte
   Setter allein reichen nicht. Für P0 Bildgrößen/Selektion/Scrollen, für P02
   Schriftwechsel,
   für G29/G31 Referenzen und Löschverhalten. Cache-Tests auf Invalidierung,
   nicht nur auf den ersten Aufruf ausrichten.
6. **Vergleich messen:** ohne Profiler messen, dann Profiler zum Erklären
   verwenden. Warme und kalte Werte, Median/p95, Fixture und Hardware nennen.
   Erst bei nachgewiesenem Gewinn die Optimierung als erfolgreich führen.
7. **Version und Abschlussprüfung:** tatsächliche Codeänderung versionieren,
   CHANGELOG/Vertrag/QA/Planung fortschreiben, vorherige Dokumente archivieren;
   Syntax, Stand-/Linkprüfung und erforderliche Vollprüfung ausführen.
8. **Beim Inhaber ankommen:** `abgleich_07.py`, Bundle neu bauen und Hashes
   prüfen. Manuelle Prüfungen benennen; Windows/Linux, DPI, Screenreader,
   echte Maus/Trackpad und Signatur bleiben gesonderte Nachweise.

**Prüfstand der ursprünglichen Recherche (3.32.0):** Standprüfung, statische Analyse,
`test_etappe1_332` und `test_tempo330` bestanden; Ansichtswechsel profiliert.
Anwendungsquellcode vor/nach bytegleich. Keine erneute Vollprüfung aller
55 Suiten, keine neue Windows-/Linux-/Screenreader-Abnahme. Die fünf
eingereichten Fotos sind noch nicht als in dieser Runde behoben markiert.

**Nachtrag Klappkorrektur 3.32.1:** D08 umgesetzt; Vollprüfung mit
71 automatisierten Schritten und 56 Suiten bestanden. Beide Startfassungen
sind gemäß Paketregeln per SHA-256 abgeglichen (139/53 Dateien).
[QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md) und
[Kontrollmatrix](../01_Repository/Glide/docs/69_KLAPPKONTROLLE_3.32.1.md)
halten Nachweise und die offene manuelle Plattformprüfung fest. D04/G29
und die folgenden Performance-Pakete bleiben geplante Folgeimplementierungen.

**Fortsetzung 3.32.2:** D04 umgesetzt; P02 Schriftcache abgeschlossen; P01 um unprofilierte Serien mit 100/1.000/10.000 Aufgaben, Bildseite und Notiz ergänzt; P03 gebündelte Layouts und P05 gemeinsamer Hover umgesetzt, restliche Teile offen. [Drag-/Performance-Vertrag 3.32.2](../01_Repository/Glide/docs/70_DRAG_UND_PERFORMANCE_3.32.2.md) nennt Bedienproben und Messgrenzen. Nächster Schnitt: unveränderte Bibliotheks-/Startseitenkarten erhalten, dann Bildlayout und Speicherkonsolidierung; anschließend Featureetappe 3.33. D07 bleibt offen.

### Konkreter Anschluss nach 3.32.2

1. **P03 zuerst Bibliothek:** `refresh_library_page` löscht sämtliche Kinder von `home_content`; dieselbe Fläche wird für Startseite und weitere Ansichten genutzt. Vor dem Kartencache daher Ansichtshost/Lebensdauer festlegen. Bestehende Karten über `(Art, ID)` identifizieren, nur geänderte Vorschauen/Buttons aktualisieren. Keine Tk-Widgets umparenten. Anfangs gleiche Ansicht erneut aktualisieren; Wiederverwendung über Ansichtswechsel erst mit eigener Lebensdauerprobe.
2. **Invalidierung vollständig:** Reihenfolge/Ordnerpfad, Titel/Farbe/Symbol, Vorschauaufgaben mit Status/Termin/Wichtigkeit, Archiv, Kartengröße, Schrift/Design und Bildinhalt berücksichtigen. Bei Tageswechsel hängen Fälligkeitszähler am neuen Datum. Der vorhandene `render_pass` bleibt ein Durchgangscache; daraus keinen unvollständig invalidierten dauerhaften Datenzähler machen.
3. **Abnahme P03:** Ein Haken aktualisiert genau die betroffene Vorschau; Umordnen erhält Reihenfolge; Neu/Löschen/Undo/Papierkorb und Archivwechsel stimmen; Fokus bleibt auf dem vorhandenen Knopf, Scrollposition stabil, Fenstergrößen/Designwechsel korrekt. Neuerzeuge- und Grid-Aufrufe zusätzlich zu unprofilierter Latenz zählen. Der 3.32.2-Messvergleich ist die nächste Baseline.
4. **P04/P06 danach:** Bildgeometrie vs. Platzierung getrennt invalidieren. Bei Speichern zunächst Requests pro Aktion erfassen: `save_items` aktualisiert bereits die Seitenleiste, viele Aufrufer aktualisieren sie anschließend nochmals. Nur nachgewiesene Doppelarbeit entfernen; tatsächliches atomares Schreiben, `fsync`, Backup, Sperre und Fehlerpfade erhalten.
5. **Featureetappe 3.33:** G01 Parser mit Bearbeitungstag/Fälligkeit-Vorschau, danach G05 Fokus an vorhandener Zeiterfassung. G29/G31/G32 zusammen mit ID- und Altleserprüfung; G02 mit klar bezeichnetem Feld-/Terminkontext. Keine neue Entscheidung zu D01–D06 erforderlich. D07 betrifft erst Animation.

**Abnahme 3.32.2:** [Vollprotokoll](../01_Repository/Glide/tests/qa-3.32.2/drag_performance_2026-09-30/vollpruefung/ergebnis.json): Exitcode 0, 72 automatisierte Schritte, 57 Suiten und fünf Analysen. [Auslieferungsabgleich](../01_Repository/Glide/tests/qa-3.32.2/drag_performance_2026-09-30/abgleich.json): 139 Python-/53 Bundle-Dateien bytegleich, Bundleversion 3.32.2 und gültige Ad-hoc-Signatur. Der abschließend geprüfte Quellstand blieb unverändert. Eine neu gefundene Zeichnungsleistenregression ist geschlossen und dauerhaft geprüft. Windows/Linux, physische Bedienung, DPI und Screenreader bleiben offen. Nächster Umfang folgt der konkreten Anschlussplanung oben; D07 bleibt für Animation offen.

### Weitere Aufgaben und Richtungsauswahl

**Fortsetzung auf „weitermachen und nicht aufhören“:** 3.32.3 setzt den bereits geplanten ersten Bibliotheksschnitt P03/A-01 um und entfernt den belegten zweiten Archiv-Refresh (Teil P06/A-03). [Vertrag 71](../01_Repository/Glide/docs/71_KARTEN_PERFORMANCE_3.32.3.md) dokumentiert Lebensdauer, Invalidierung, Bedienproben und Messgrenzen. Vollprüfung und Lieferung abgeschlossen: 73 Schritte/58 Suiten/fünf Analysen grün, 139 Python-/53 Bundle-Dateien bytegleich und Signatur geprüft. Das wählt keine zusätzliche neue Feature-Richtung aus; nächste offene Performance-Arbeit bleibt Startseite/P04/P06.

Auf neuen Wunsch des Inhabers sammelt [Weitere Aufgaben und Richtungsauswahl nach 3.32.2](Glide_Aufgabenauswahl_nach_3.32.2_2026-09-30.md) **24 Aufgaben in acht Richtungen**. Bestehende offene G-/P-Arbeiten und neue Vorschläge sind getrennt gekennzeichnet, mit Codegrundlage, notwendiger Recherche und konkreter Abnahme. Erste Richtung, zweite Priorität und Bearbeitungstiefe bleiben offen. D01–D06 gelten weiter; D07 wird erst bei der Animationsetappe relevant. Bis zur Antwort gilt keine Empfehlung als beauftragt. Die neue Auswahl ersetzt nicht die bereits erledigten Nachweise 3.32.2.

### Konkreter Anschluss nach 3.32.3

- **P03/A-01 abgeschlossen für die bestehende Bibliothek:** gleicher Host/ID, frische Vorschaudaten, passende Invalidierung und weniger Neuerzeugungen. Startseite, Aktualisierung einzelner Elemente geänderter Karten und viele Karten bleiben separate Teile von P03; physische Fokus-/Plattformabnahme offen.
- **P04/A-02:** Scrollen verwendet bereits `place_images`. Zuerst Aufrufe von `fit_read_width`/`schedule_image_layout`/`layout_images`/`render_image` bei Scrollen, Resize, Text/Format, Auswahl und Ziehen zählen. Unveränderte effektive Lesespaltengeometrie ist der erste Skip-Kandidat. Text/Anker, Modi/Größen, Schrift, Faltungen und fertig konvertierte Anhänge müssen weiter invalidieren. Keine verschachtelten `update`-Rückrufe.
- **P06/A-03 teilweise:** Archiv-Zurückholen aktualisiert einmal. 21 statische Kandidaten sind noch keine bestätigten Fehler; zunächst z. B. Kalender-Neuanlage und Seitenleisten-Umbenennen samt Undo zählen. `save_items` aktualisiert die Seitenleiste erst nach erfolgreichem Schreiben, Änderungsrahmen auch bei Fehlern. Fehlerfall/Dirty/Warnung/Bestand prüfen, bevor zentrale Aufrufe entfallen. Atomares Schreiben, Sicherungen und Sperren bewahren.
- **Nachweise:** [Vollprotokoll](../01_Repository/Glide/tests/qa-3.32.3/karten_performance_2026-10-01/vollpruefung/ergebnis.json), [Abgleich](../01_Repository/Glide/tests/qa-3.32.3/karten_performance_2026-10-01/abgleich.json), [Messvertrag 71](../01_Repository/Glide/docs/71_KARTEN_PERFORMANCE_3.32.3.md), [statischer Codeabgleich](../01_Repository/Glide/tests/qa-3.32.3/karten_performance_2026-10-01/folgeschnitt_codebefunde.json). Zusätzliche Feature-Richtungsauswahl bleibt offen; bisherige D01–D06 weiter verbindlich.

## 9. Abschlussaufgabe – ausdrücklich aufnehmen

> Ich habe Performance Probleme mit Glide, hilf mir die Code-Basis zu optimieren, mit Variabeln für die gleichen Funktionen, Streamlinen und optimieren.

**Status:** 3.32.3 ergänzt erhaltene Bibliothekskarten, gemeinsame Aktionsleisten und einmaliges Archiv-Zurückholen (73 Schritte/58 Suiten bestanden; beide Startfassungen abgeglichen). Erster Schnitt in 3.32.2 umgesetzt und gemessen: Schriftcache, gebündelte Formatleistenlayouts und gemeinsamer Hover. P01/P03/P05 sind teilweise, P02 ist umgesetzt. Offen bleiben Verlauf-/Speichermessung, Startseitenkarten und Aktualisierung einzelner Elemente geänderter Karten, Bildlayout, gemeinsame UI-Texte sowie P06/P07. Die bestehenden Bild-/Formatierungsprüfungen sind erneut grün; die Originalfotos beweisen weiterhin keinen konkreten Fehlerablauf. P02/P05 bündeln gleiche Funktionen und Werte;
P03/P04/P06 reduzieren den tatsächlichen Aufbau-, Layout- und Schreibaufwand.
Ergebnis: wartbare gemeinsame Helfer, belegte Vorher-/Nachher-Messungen,
grüne passende Tests, keine verlorenen Daten oder Bedienfunktionen und
abgeglichene startbare Fassungen. Ein Toolkit-Wechsel ist gemäß D03
zurückgestellt; die Optimierung betrifft zunächst Tk. Eine spätere
Neubewertung gehört zu einem gesonderten Auftrag.
