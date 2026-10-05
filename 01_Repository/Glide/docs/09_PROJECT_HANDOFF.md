# Projektübergabe, Entscheidungen und Arbeitsstand

Stand 05.10.2026 · Glide 3.33.8 laut VERSION · Aufgabenformat 20

Diese lokale Übergabekopie war beim Einstieg bereits vorhanden. Ihre früheren Angaben zu fehlenden Dateien und abweichenden Versionen wurden am 05.10.2026 am Code widerlegt: VERSION, APP_VERSION, Hauptsuite und CHANGELOG stimmten mit 3.33.6 überein; die Python-Hauptdatei und capture_parser.py waren vorhanden. Die damalige Behauptung ist keine aktuelle Prüfaussage.

Verbindlich bleiben die [Sitzungsübergabe](../../../00_Arbeitsvorbereitung/Glide_Uebergabe.md), der [Entwicklungsplan](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md), die [Arbeitsrichtung](ARBEITSRICHTUNG.md) und [Markt und Vorbilder](../../../00_Arbeitsvorbereitung/Glide_Markt_und_Vorbilder.md). Die Tabellen unten sind Herkunftskontext und ersetzen deren aktuellen Aufgabenstatus nicht. Automatische Ergebnisse und Plattformgrenzen stehen im [QA-Bericht](07_QA_BERICHT.md).

Der aktuelle Auftrag vom 05.10.2026 autorisiert Planung und Beginn der Feature-Umsetzung. Erster Schnitt: G14-Inhaltssuche im vorhandenen Strg/Cmd+O-Weg, ohne neues Datenformat; danach Performance, stabile Aktionskennungen/UX1, Aufgaben im Text und Verweise. D07, Importquelle, Bauwerkzeug und Inhaberfreigaben bleiben offen.

## Erledigte Pakete

| Paket | Belegter Implementierungsstand |
|---|---|
| Pixel-Werkstatt, Seiten/Galerien, Format 20 | Implementiert; Bedien-/Daten-/Zeichenvertrag |
| G16, G20, G11, G03 | Symbolausgabe, Palettenimport, Vorlagenplatzhalter, Tagesabschluss in 3.32.0 |
| D08 | Klappkontrolle und Pflichtsuite in 3.32.1 |
| D04 / P02 | Gemeinsame Drag-Bindungen und Schriftcache in 3.32.2 |
| A-01 / Teil P03 / Teil P06 | Bibliothekskarten erhalten, Archiv-Refresh konsolidiert in 3.32.3 |
| T2 / P09a | Gemeinsame Formatsicherung und nutzlose Tabellenmessung entfernt in 3.33.0 |
| Vier Bereiche / Notizbuchzeichnungen | Typregeln und Fensterkorrektur in 3.33.1 |
| D12 / Teil P03 | Sieben Startkacheln, eigene Auswahl erhalten, Standard zurücksetzen in 3.33.2 |
| G01 / D10 | Deutsche Eingabe und Feldchips in 3.33.3 |
| CI-Grundstufe | Eingerichtet; Linux-Integrationskalibrierung bleibt offen |

## Verbindliche Entscheidungen

| Entscheidung | Konsequenz für weitere Arbeit |
|---|---|
| D01 | Allgemeine Datumsangaben setzen den Bearbeitungstag; ausdrücklich „fällig/bis“ setzt die Fälligkeit. |
| D02 | Eine Aktion bewirkt die im sichtbaren Zielkontext erwartbare Änderung. Beim Ziehen in einen ausdrücklich bezeichneten Terminkontext das passende Feld ändern; neutrales Umordnen erhält Termine. Bearbeitungstag und Fälligkeit bleiben getrennt. |
| D03 | Desktop/Tk optimieren. Mobile und eine Toolkit-Probe sind zurückgestellt. |
| D04 | Drag-and-drop erweitert bestehende Bereiche; umgesetzt in 3.32.2. |
| D05 | Einzelne Aufgaben in Notizen und Seiten unterstützen, ihre Identität über IDs erhalten. Notiz, Seite und Liste bleiben eigenständige Arten; keine allgemeine Konvertierungspflicht. F11 ist beantwortet. |
| D06 | Die Gestaltung von Hinweisblöcken in Seiten bleibt unverändert; D11 regelt separat die Hinweiszeilen der Ansichten. |
| D07 | Exportumfang für Animation offen: abspielbares GIF oder zunächst Frames/Vorschau/PNG-Spritesheet. Erst bei der Animationsetappe erforderlich. |
| D08 | Alle Klappmechanismen über echte Bedienbindungen prüfen, einschließlich Zustandserhalt, Tastatur, verschachtelter Bereiche und Tk-Callbackfehler. Korrektur und Pflichtsuite seit 3.32.1. |
| D09 | Das GitHub-Repository `glide-to-do` ist die maßgebliche Ablage (Wurzel = Projektordner, Quellbaum `01_Repository/Glide`). Uploads nur in diese Struktur. Das Repository ist öffentlich: Rohprotokolle (`*.log`) bleiben seit 01.10.2026 lokal (Entscheidung des Inhabers); veröffentlichte Prüfergebnisse enthalten keine Benutzerpfade (`scripts/pflege/pfade_bereinigen.py`, CI-Schritt „Datenschutz“). Sicherheitsmeldungen über GitHub (`SECURITY.md` in der Wurzel) und Dependabot laufen im Repository; der CodeQL-Workflow ist vom Inhaber deaktiviert. Neue Zwischenstände als Git-Tags; lokale Archive folgen der Sieben-Versionen-Grenze. CI-Grundstufe seit 01.10.2026 (`.github/workflows/python-app.yml`, `tests/tools/ci_grundstufe.py`); Integrationssuiten unter Linux nur manuell und informativ. |
| D10 | Ein Datum ohne Zusatz setzt den Bearbeitungstag, auch in `/morgen`; die Fälligkeit nur mit „fällig“/„bis“. D01 gilt ohne Slash-Ausnahme. G01 ist im vorhandenen Quellstand 3.33.3 umgesetzt. |
| D11 | D06 gilt nur für den Hinweisblock in Seiten. Hinweiszeilen der Ansichten werden über „?“ ein-/ausgeklappt, Zustand gespeichert (U02). |
| D12 | Startseiten-Standard „Ruhig“ mit sieben Kacheln einschließlich Gismo. Fest: Heute (zusammengeführt), Gismo, Woche, Zuletzt bearbeitet, Angeheftet. Zusätzlich beschlossen am 01.10.2026: Zeichnungen und Pinnwand-Vorschau. Eigene Auswahl bleibt erhalten. |
| D13 | Eisenhower als Gruppierung „Dringlichkeit × Wichtigkeit“ im vorhandenen Board, keine eigene Ansicht. Ziehen ändert Wichtigkeit bzw. Bearbeitungstag (D02); Fälligkeiten werden nie gelöscht. |
| D14 | Zwei Hauptansichten: **Heute** (Mein Tag, Verspätet, Heute fällig, nächste Aufgabe) und **Demnächst** (bisher In Bearbeitung). Tagesbeginn/-abschluss sind Modi von Heute; interne Kennungen bleiben. |
| D15 | Verteilung als Paket mit eingebettetem Python und Tk 9 je Plattform (G26/H-03), nach Stufe 1. Das Bauwerkzeug wird als eigene Abhängigkeitsentscheidung vorgelegt. |
| D16 | Speicherformat JSON bleibt; der Speicherweg wird beschleunigt (T2, P08a/b, P09). SQLite nur als Suchindex-Cache (G14); Neubewertung erst bei realen Beständen über 20.000 Punkten. |
| D17 | Kein Großumbau: Jede neue oder angefasste Fachlogik entsteht als Tk-freies Modul mit Unit-Tests; `ListApp` ruft sie auf. G27 wird so schrittweise erledigt. |

Lokale Nutzung ohne Konto/Cloud, vorhandene Architektur, Daten/Undo, stabile IDs, Gestaltung und möglichst wenige Abhängigkeiten gelten weiter. Offene Inhaber-/Storeangaben bleiben offen. Seit D09 (01.10.2026) ist das GitHub-Repository `glide-to-do` die maßgebliche Ablage; „Git vertagt“ gilt nicht mehr. Keine erneute Entscheidung über D01–D06 und D08–D17 einfordern; offen bleibt D07.

## Gemeinsamer Aufgabenvorrat

### Notwendig (N)

| ID | Arbeit | Quelle | Begründung | Aufwand | Risiko | Stufe |
|---|---|---|---|---|---|---|
| P03r | Rest P03: Startseitenkarten, einzelne Kartenelemente, viele Karten | beauftragt | Startseite teuerste Ansicht | M–L | mittel (Fokus/Scroll) | 0 |
| P04 | Bildlayout nur bei geänderter Geometrie | beauftragt, A-02 | Gemessen nötig vor Optimierung | M | mittel | 0 |
| P06r | Doppelte Refresh-/Schreibanforderungen | beauftragt, A-03 | Bestätigte Doppelarbeit | M | mittel (Fehlerpfade) | 0 |
| P09b | W2–W5: Kennzahlen einmal je Aktualisierung, Datum über Zwischenspeicher, Schriftobjekte und Zeilenhöhen je Schrift merken | T8 | Listenaufbau −38 % bei 5.000 Punkten | S | gering–mittel | 0 |
| P08a | Ein Vergleichsdurchlauf für Verlauf, „zuletzt bearbeitet“, Aktivität | T1 | ≈ 78 % von `save_items` bei 10.000 Punkten | M | mittel | 0 |
| P08b | Nur geänderte Listen vergleichen, Vollvergleich im Autosave | T1 | Kosten pro Aktion unabhängig vom Bestand | M–L | mittel–hoch | 0 |
| DOK2 | Kommentare und Lieferordner-README (AB03–AB08), Mindestversion prüfen | AB03–AB08 | Widersprüche | S | gering | nächster Produktionsschnitt |
| G14 | Volltextsuche (FTS5 als Cache) in der Befehlspalette | G14, D-01, P07 | Seiten ohne Inhaltssuche verlieren Wert | L | mittel | 2 |

### Sinnvoll (S)

| ID | Arbeit | Quelle | Aufwand | Stufe |
|---|---|---|---|---|
| CI | Offen: vier reine Linux-Abweichungen der Integrationssuiten kalibrieren; die CI-Grundstufe ist eingerichtet und steht in den erledigten Paketen | D09, T4 | M | 0 |
| UX1 | **Weniger Oberfläche:** U01 Befehlspalette (N03), U02 Hinweise bei Bedarf, U03, U05-Standard, U07 Eingang (N02), U10 Kopfzeile, U13 Bibliothek, U14 Menü, U16 Begriffe, U19, U22, U24 Symbole, N01/U17 Automatisch hell/dunkel + Signaturdesign | UX, D11, D12 | 5–8 AT | 1 |
| G05 | Fokusansicht an vorhandener Zeiterfassung | G05, B-02 | M | 1 |
| D14 | Heute/Demnächst | U06 | M | 1 |
| G02 | Eisenhower als Board-Gruppierung | G02, D13, D02 | M | 1 |
| H-02 | Tastaturwege für Ziehen | H-02 | M | 1 |
| N08 | JPEG-Vorschau Linux über Systemwerkzeug | T5 | S | 1 |
| N07 | „Neu in …“-Karte nach Update | U21 | S | 1 |
| G29 | Aufgaben im Notiztext (gleiche IDs) | G29, C-01, D05 | L | 1 |
| G31 | Seitenaufgabe über ID in Liste schicken | G31, C-02 | M | 1 |
| G32 | Filter „aus Seiten“ | G32, C-03 | S | 1 |
| N04 | Kalender als eingebettete Ansicht, Ziehen auf Tage (D02), freie Zeitfenster | U11, B-03 | L | 2 |
| N05 | Ein Inspektor statt Maske + Detailbereich | U12 | L | 2 |
| U18 | Seitentitel im Dokument, Platzhalter | U18 | M | 2 |
| U09 | Kompakte Pinnwandleiste | U09 | M | 2 |
| U08 | Vorlagen im Anlegen-Weg, gefüllte Vorschau | U08, E-03 | M | 2 |
| U15/U20 | Lila nur für Hinzufügen; Leerzustände ohne doppelten Anlegen-Knopf | U15, U20 | S | 2 |
| G08/G30 | Seiten-/Listenverweise, Rückverweise (Format-21-Tor) | G08/G30, D-02 | L–XL | 2 |
| G28 | Live-Liste in Seite | G28, E-01 | L | 2 |
| G09 | Titelbild für Seiten und Bibliothekskarten | G09, E-02 | M | 2 |
| D-03 | Filterwirkung erklären | D-03 | S | 2 |
| G19 | Palettenbearbeitung mit Undo | G19, G-01 | M–L | 3 |
| G17 | Animation (D07) | G17, G-02 | XL | 3 |
| G-03 | Symbolvorschau 16/32/48 px | G-03 | S–M | 3 |
| G24 | Kontextpaket, Markdown/Felder, Änderungsvorschläge (Q3) | G24, F-01 | L | 4 |
| G21 | Begrenzter Notion-/Todoist-Import mit Verlustbericht | G21, F-02 | L | 4 |
| F-03 | Sicherungsvergleich | F-03 | M | 4 |
| G26 | Paket mit eingebettetem Python 3.14 + Tk 9 je Plattform (N11) | G26, H-03, D15 | L–XL | 4 |
| H-01 | Kontrollmatrix fortführen | H-01 | laufend | alle |

### Zukunft (Z) und bewusst nicht (X)

| ID | Thema | Klasse | Grund / Auslöser für Neubewertung |
|---|---|---|---|
| N12 | Screenreader und beschriftete Canvas-Bedienung | Z | Laufzeit-/Paketentscheidung und eigene Plattformabnahme erforderlich |
| N13 | Seitenversionen wiederherstellen | Z | Nach F-03 |
| – | SQLite als Hauptspeicher | Z | Reale Bestände > 20.000 Punkte (D16) |
| G25, Mobile | Toolkit-Probe, Mobile | Z | D03 aufheben |
| G18, G10, G15 | Kachelsatz, Registerkarten-Block, Filter in Alltagssprache | Z | Vorrat laut Funktionsrecherche |
| N09 | Erinnerungen bei geschlossener App | X | Produktgrenze, Stufe C bewusst nicht |
| N10 | Lokaler MCP-Server | X | Q3: Dokumente statt Schnittstelle |
| N14 = G07 | Systemweiter Erfassungs-Hotkey | X | 30.09.: nur plattformeigen lösbar |
| N06 | „Erste Schritte“-Seite | X | Einstieg für neue Nutzer bewusst nicht gewählt; Rundgang/Showcase vorhanden |
| G23 | Gleichzeitige Gerätebearbeitung | X | Produktgrenze Konfliktzusammenführung |
| N15–N20, G06, G12, G13 | Spracherfassung, Gewohnheiten, Teamfunktionen, freie DB-Felder, Spalten, Unterseiten/Graph, Web Clipper | X | Produktgrenzen bzw. Entscheidungen |

Die A–H-Kennungen bleiben in den Quellen-/ID-Spalten zugeordnet; bereits
erledigte A-01 und B-01/G01 stehen in den erledigten Paketen. Es gibt keine
zweite, parallel zu pflegende Aufgabentabelle.

## Nächster beauftragter Schnitt

Die beim Einstieg behaupteten Versions-/Lieferabweichungen sind am Quellstand widerlegt. Der Auftrag vom 05.10.2026 umfasst Feature-Planung und Umsetzungsbeginn; G14-Inhaltssuche seit 3.33.7 und Windows-Layout-/Sicherheitskorrekturen in 3.33.8 konkretisieren ihn. Aktueller Prüf- und Lieferstatus steht ausschließlich im QA-Bericht.

Als nächste Schnitte gelten P08a/P09b mit Differenz- und Latenzmessung, danach stabile Aktionskennungen/UX1, Fokus/H-02 und Aufgaben im Text. P03/P04/P06r bleiben beauftragt. Reihenfolge, Invarianten und Format-21-Tor stehen im verbindlichen Entwicklungsplan; die alten Tabellen oben sind Herkunftskontext. D07, Importquelle, Bauwerkzeug und Inhaber-/Releaseangaben bleiben eigene Entscheidungen. Historische Linux-Zahlen sind keine aktuellen Mac- oder Windows-Abnahmen.

## Erhaltene Inhaberantworten

> gerne in der Reihenfolge, erst die schnellen Gewinne, dann Planen, dann Wissen und dann Pixel. Verschlüsselte Ablage ist keine Priorität und keine Mac-exklusiven Features, weil ich plattformunabhängig arbeiten möchte, Mac, Linux, Windows und später mal iPhone/iPad.

Antwort vom 30.09.2026: Q3 wählt Austausch über Dokumente statt Schnittstelle;
G24 umfasst Kontextpaket, Markdown/Felder und bestätigte Änderungsvorschläge.
G07 (systemweiter Erfassungshotkey) ist nicht gewählt. Q5/D05 erlaubt echte
Aufgabenzeilen in Notizen und Seiten mit derselben Identität, keine Pflicht
zur allgemeinen Konvertierung. D06 erhält Seitenhinweisblöcke; D11 betrifft
separat die Hilfezeilen der Ansichten. Bestätigte Entscheidungen nicht erneut vorlegen.

## Einstieg und Prüfung

1. AGENTS.md, diese Übergabe und betroffene Fachverträge lesen.
2. Tatsächliche Funktion und alle Aufrufer prüfen; keine historische Lücke ungeprüft übernehmen.
3. Bestehende passende Baseline mit temporärem GLIDE_DATA_DIR ausführen.
4. Begrenzten Schnitt, Invarianten, echte Bedienbindungen und Fehlerpfade prüfen.
5. Stand/Links und betroffene Tests, danach erforderliche Vollprüfung durchführen.
6. Erst nach grünem Lauf Python-Lieferung und Mac-Bundle abgleichen; manuelle Grenzen nennen.

Prüfaufrufe stehen gesammelt im [Testplan](05_QA_TESTPLAN.md).
Modulübersicht: [Architektur](02_ARCHITECTURE.md).
Reine Dokumentations-/Werkzeugpflege erhöht keine Produktionsversion und
baut keine unveränderten Startfassungen neu. Git trägt Dokumenthistorie.
