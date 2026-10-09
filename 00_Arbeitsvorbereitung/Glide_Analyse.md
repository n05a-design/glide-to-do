# Glide – Analyse: Funktionen, Oberfläche, Entscheidungen, Nutzung

Stand 09.10.2026 · Glide 3.35.0 · Aufgabenformat 23 · Analyse vom 08.10.2026 (Code, Dokumente, Git-Historie, native Mac-Vollprüfung)

Bestandsaufnahme im Auftrag vom 08.10.2026: lokale Ablage untersuchen, Dokumentation und Code abgleichen, daraus den Sprint ableiten. Dieses Dokument trägt die **Analyse** (Funktions-, Oberflächen-, Entscheidungs- und Nutzungsanalyse sowie den Abgleich Dokumentation ↔ Code). Der Wettbewerb steht in [Markt und Vorbilder](Glide_Markt_und_Vorbilder.md), die Entscheidungen selbst in der [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md), die daraus abgeleiteten Aufgaben ausschließlich im [Entwicklungsplan, Abschnitt 15](Glide_Entwicklungsplan.md#15-sprint-ab-08102026-aufgabenkatalog). Erledigte Befunde werden hier als erledigt markiert, nicht gelöscht, bis die nächste Analyse sie ersetzt.

**Belegstufen** in allen Tabellen: **[Code]** im Quellstand nachgelesen · **[Test]** durch eine automatische Prüfung belegt · **[Mac]** in der nativen Mac-Vollprüfung vom 08.10.2026 (Python 3.14.5, Tk 9.0.3, künstliche Daten) gesehen · **[Dok]** nur in Dokumenten belegt · **[Einschätzung]** eigene Schlussfolgerung · **[Unbestätigt]** Annahme ohne Beleg. Es liegen **keine Nutzungsdaten** vor (keine Telemetrie nach Produktgrenze, keine Nutzerstudie); Aussagen über Nutzer sind deshalb als Einschätzung gekennzeichnet.

## 1. Untersuchter Bestand

| Bereich | Umfang am 08.10.2026 | Beleg |
|---|---|---|
| Code | `src/glide/app.pyw` 55.826 Zeilen (Klasse `ListApp` 42.357 Zeilen, 1.505 Methoden), 27 Begleitmodule (davon 18 Tk-freie Fachmodule nach D17 seit 3.33.0) | [Code] |
| Tests | 76 Integrationssuiten, 23 Unit-Testdateien mit 170 Tests, 25 Werkzeugtests, fünf Analysen | [Code], [Test] |
| Dokumente | 50 aktive Markdown-Dokumente; Planung, Entscheidungen, Funktionen, QA, Daten, Markt | [Dok] |
| Git | Arbeitsstand 3.33.9–3.33.18 noch nicht eingecheckt (Zweig `claude/glide-3.33.15`, Basis `254541a`); `main` enthält zwei Dokumentationscommits vom 06.10.2026 (PR #15), die dem Arbeitsstand fehlten und am 08.10.2026 per Drei-Wege-Abgleich übernommen wurden | [Code] |
| Laufzeit auf dem Referenz-Mac | Python 3.14.5 (python.org) mit Tk 9.0.3; python.org führt inzwischen 3.14.8 (30.09.2026) | [Code], [Mac] |

## 2. Funktionsanalyse

Vollständigkeit: **●** im Alltag vollständig nutzbar · **◐** nutzbar mit dokumentierter Lücke · **○** fehlt. „Plattform“ meint die zuletzt automatisch geprüften Systeme.

| Bereich | Vorhanden (Version) | Vollständigkeit | Fehlende Erweiterung (Aufgabe) |
|---|---|---|---|
| Erfassen | Schnelleingabe mit Feldchips, D01/D10, Wiederholungen, „/“-Befehle, Labels, mehrzeiliges Einfügen in Listen (3.33.3/3.33.4) | ◐ | Erinnerung beim Erfassen (KO03); mehrzeiliges Einfügen in die Eingabezeile (KO05); „+“-Knopf und Umschalt+Enter statt zweier Textknöpfe (U04) |
| Heute und Planung | Heute/Demnächst (D14), Tagesbeginn/-abschluss, Tagesvorschlag (AU01), verfügbare Zeit (AU02), Einplanen (KO01), Zeitblöcke mit Tastatur, Fokus (G05), Wochenkalender (N04/AU04) | ● | Routinen als Abschnitt in Heute (AU06); automatische Tageshinweise (AU03, Vorgabe offen); Termine als belegte Zeit (AU07, Produktgrenze) |
| Wiederholungen | Regeln täglich … jährlich, Enddatum, Anker gegen Monatsende-Drift; Abhaken rückt die Fälligkeit vor | ◐ | „Diesen Termin überspringen“, verpasste Termine überspringen statt nachholen (KO02) [Code: `advance_repeating_items` rückt genau einen Schritt nach der alten Fälligkeit vor] |
| Listen, Tabelle, Board | Gruppierung inkl. Eisenhower, Auswahlleiste, Tabellenspalten, Detailbereich | ● | „Verschieben nach …“ und Labelauswahl ohne zuletzt benutzte Ziele (KO06); Inspektor statt Maske + Detailbereich (N05/KO04, nach I7) |
| Pinnwand | frei/geordnet/Spaltenboard, Bereiche, Verbindungen, Präsentation | ◐ | Tastaturwege (H-02-Rest); kompakte Leiste (U09) |
| Seiten und Notizen | Block-Editor, Bilder, Aufgaben mit Original-ID, Verweise/Rückverweise, Live-Listen, Titelbild, Vorlagenvorschau | ◐ | Bilder überlappen auf gleicher Höhe, fehlen in Druck/PDF/Markdown (B4); Seitentitel im Dokument und Platzhalter (U18); Tastaturwege im Seitenbaum (H-02-Rest) |
| Suche | gemeinsame Palette für Inhalte und Aktionen (G14 erste Stufe, U01) | ◐ | Treffer im Dokument hervorheben; FTS5 nur nach gemessener Latenz (G14/P07); Begründung, warum ein Filter einen Punkt zeigt (D-03) |
| Erinnerungen | fest/relativ, Zustellbeleg, Systemmitteilung (Option) bei laufender App | ● | Zustellung bei geschlossener App bewusst nicht (N09) |
| Pixel-Werkstatt | 16–128 Zellen, Werkzeuge, Paletten, ICO/PNG/SVG/JSON, Pixelsymbol | ◐ | Palettenfarbe ändern färbt die Zeichnung um (G19); Symbolvorschau 16/32/48 (G-03); Animation (G17, D07 offen) |
| Austausch | CSV, Markdown, ICS, `.glidepage`, Backups, `.glideexchange` Stufe 1 | ◐ | KI-Austausch Stufe 2 mit Kontextpaket und Änderungsvorschlägen (G24); zwei Sicherungen vergleichen (F-03); erste Fremdquelle (G21, Entscheidung offen) |
| Erscheinungsbild | zehn Designs, berechneter Kontrast, Hintergrundverläufe, Mindestgröße 860 × 700 | ◐ | „Automatisch (hell/dunkel)“ nach System (N01/U17); Lila nur für Hinzufügen, aktiver Zustand neutral (U15); schmale Seitenleiste (OB05) |
| Hilfe | Handbuch, Kürzel, einklappbare Hinweise (D11), Showcase/Rundgang | ◐ | einmalige Karte „Neu in …“ nach einem Update (N07); Leerzustand ohne doppelten Anlegen-Knopf (U20) |
| Betrieb | Formatschutz bis Format 23, Vorsicherungen, Sperrdatei, Sicherungen nur bei Änderung | ◐ | Mindestversion Python/Tk beim Start prüfen (AB08) [Code: keine Prüfung vorhanden]; Linux-JPEG-Vorschau (N08) |
| Tempo | P02/P03/P08a/P08b/P09a/P09b umgesetzt | ◐ | Bildlayout nur bei geänderter Geometrie (P04), doppelte Aktualisierungen (P06r), Einstellungsfenster ≈ 2,1 s, unveränderte Startseitenkacheln behalten (P03-Rest), Abhaken bei 5.000 Punkten ≤ 120 ms (P08b-Ziel) |

## 3. Abgleich Dokumentation ↔ Implementierung

Abweichungen, veraltete Angaben und unbestätigte Annahmen, Stand 08.10.2026. Spalte „Behoben“ wird bei Erledigung nachgetragen.

| Nr. | Fundstelle | Befund | Art | Behoben |
|---|---|---|---|---|
| A01 | Arbeitsstand gegenüber `main` | Zwei Dokumentationscommits vom 06.10.2026 (Leitgedanken des Inhabers, erweiterte Featurematrix, I9–I11, GitHub-Auftritt) fehlten in allen 3.33.9–3.33.18-Dokumenten | fehlender Inhalt | 08.10.2026 per Drei-Wege-Abgleich übernommen |
| A02 | Entwicklungsplan §10 | „Kopfzeilen-Symbolknöpfe 8“ und „Symbole mit mehreren Bedeutungen 5“ sind seit 3.33.16 überholt; `pack_header_controls` zeigt im Standard Einstellungen, Erfassen, Suche, Seitenleiste (≤ 4), Glocke und Zeitanzeige nur bei Bedarf [Code] | veraltet | 08.10.2026 §10 nachgeführt |
| A03 | Entwicklungsplan §2 | Tabelle „Erledigt seit 3.30“ endet bei 3.33.11; 3.33.12–3.33.18 fehlen, Reihenfolge 3.33.11 vor 3.33.10 | veraltet | 08.10.2026 §2 bis 3.33.18 ergänzt; 3.33.19 am 09.10.2026 |
| A04 | Entwicklungsplan §4.3 Welle 2 gegenüber Übergabe §6 | N01/U17 steht einmal „nach I7“, einmal ohne diese Abhängigkeit. I7 betrifft laut R12 nur Gestaltungsumbauten (OB02/OB03); N01 ist eine Systemkonvention nach P1 | Widerspruch | 08.10.2026 aufgelöst: N01 ohne I7 (Sprintkatalog, Paket 3) |
| A05 | Entwicklungsplan §8 | „Datenformat-Tor 21 beim ersten inkompatiblen Inhalt (Verweise, Animation)“: die Formatnummern 21, 22 und 23 sind vergeben, eine Animation bräuchte die nächste freie Nummer | veraltet | 08.10.2026 §8 berichtigt |
| A06 | Prüfplan „Fachlogik-Unit-Tests“ | nennt 15 Module; vorhanden sind 23 Unit-Testdateien (u. a. `task_references`, `object_references`, `week_planning`, `page_features`, `interaction_policy`) | unvollständig | 08.10.2026 Prüfplan nachgeführt (Ordner maßgeblich) |
| A07 | `scripts/pflege/ablage_kuerzen.py` | Die Verknüpfungsprüfung läuft über alle Elternordner bis zur Dateisystemwurzel. Unter macOS ist `/var` eine Verknüpfung, deshalb scheitert `test_retention` nur auf dem Mac [Mac] | Werkzeugfehler | 08.10.2026 W10 behoben, zwei Gegenproben |
| A08 | `tests/tools/pruefen.py` (Kommentar) | verspricht, Prüffenster nähmen „weder Fokus noch Tastatur“; Prüfplan und Architektur sagen richtig, dass die Tastatur nicht abgeschirmt ist | widersprüchlicher Kommentar (bekannt) | 08.10.2026 W11 Kommentare berichtigt |
| A09 | Übergabe, I5 | „Python 3.14.7 auf dem Mac installieren“: Der Mac hat 3.14.5 mit Tk 9.0.3; python.org führt seit 30.09.2026 3.14.8. Die Mac-Vollprüfung ist mit 3.14.5 möglich | überholt | 08.10.2026 im Entwicklungsplan (I5) |
| A10 | Übergabe, QA-Bericht, Architektur | „Native Mac-Abnahme seit 3.33.6 offen“: Die automatische Mac-Vollprüfung ist auf diesem Rechner möglich und wurde am 08.10.2026 ausgeführt; menschliche Abnahme bleibt offen | überholt | 09.10.2026: Mac-Vollprüfung 3.33.18 Exitcode 0, Bundle 3.33.18 |
| A11 | Konsolenumleitung in den OneDrive-Ordner | Ein Prüflauf, dessen Ausgabe in eine Datei im OneDrive-Ordner umgeleitet wurde, endete nach dem ersten Fehler mit Exitcode 120 (Ausgabestrom). Ausgabe außerhalb der synchronisierten Ablage schreiben | Prüffallstrick | 08.10.2026 als Regel im Prüfplan |
| A12 | Markt und Vorbilder §4.1 | Spalte „Glide 3.33.8“ und Lücken „Seitenverweise, Fokus, Aufgaben im Notiztext“ sind seit 3.33.14–3.33.17 geschlossen | veraltet | 08.10.2026 §4.1 auf 3.33.18 nachgeführt |
| A13 | Funktionen §13 | „Startseite 507 ms (macOS, 1.000 Punkte)“ und „Einstellungsfenster rund 2,1 s“ stammen aus 3.33.2 bzw. älteren Messungen | unbestätigt für 3.33.18 | 09.10.2026 mit Messwerten 3.33.19 ersetzt |
| A14 | `symbolpruefung.py` | meldet unter macOS Ersatzschriften für ⌕, ⍾, ⎙ (Menlo, Apple Symbols); Größen- und Stärkeunterschiede zwischen Systemen sind damit erklärt, eine Entscheidung fehlt | offener Befund | |
| A15 | `07_Python-Versionen/README.md` | `versionswechsel.py` führt nur die Standzeile nach; der Lieferabsatz nannte nach dem Wechsel auf 3.33.19 weiter die Hauptdatei 3.33.18 [Ablage] | veraltet nach Werkzeuglauf | 09.10.2026 bei der Lieferung 3.33.19 berichtigt; `abgleich_07.py` prüft es seitdem (W12) |
| A16 | Eingabezeile, Menüs | Die vollständige Eingabemaske für einen neuen Punkt war nur über den Textknopf „Erweitert“ erreichbar, weder über ein Menü noch über die Befehlspalette [Code] | fehlender Weg | Arbeitsstand 3.33.20: Datei › Neu anlegen › „Neuer Punkt mit allen Angaben …“ und Palette |
| A17 | Übersichten (Heute, Demnächst) | „Als erledigt markieren“ im Kontextmenü setzte nur das Feld: Wiederholungen rückten nicht vor, die Tageszahl zählte nicht, wiederkehrende Checklisten öffneten sich nicht wieder [Code] | Fehler | Arbeitsstand 3.33.20: derselbe Weg wie Abhaken in der Liste |
| A18 | `test_wissen33315`, `test_woche33317`, `test_seiten33318` | Die Altleser-Proben starten eine feste Vorversion aus `07_Python-Versionen`; die Aufbewahrung entfernt sie planmäßig (3.33.14 beim Wechsel auf 3.33.21), der Volllauf wurde rot [Prüfwerkzeug] | Zeitzünder | 09.10.2026 W14: gemeinsamer Helfer `tests/integration/vorversion.py`, Probe entfällt ausdrücklich nur außerhalb der Aufbewahrung |
| A19 | `test_tempo33319` | Die Zählprüfung erlaubte beim Abhaken ein Schreiben der Sperrdatei; deren Zeitstempel ist sekundengenau, unter Last überschreitet die Aktion eine Sekundengrenze und schreibt richtig zweimal [Prüfwerkzeug] | zeitabhängige Prüfung | 09.10.2026 W15: Grenze je angebrochene Sekunde |
| A20 | Seitenleiste, alle Bereiche | Alt+→ legt eine Zeile in den Ordner darüber. Lose Listen und Seiten stehen in jedem Bereich vor den Ordnern; für sie gab es nie einen Ordner darüber, Glide wies Alt+→ immer mit „Zum Einrücken muss oberhalb ein Ordner vorhanden sein“ ab. In Seiten, Notizen und Zeichnungen fehlten die Alt-Pfeile ganz [Code] | toter Weg | Arbeitsstand 3.34.0 (H-02r): nächster passender Ordner darunter, Hinweis mit Ziel und Rückgängig, Bindungen in allen Bereichen; geliefert 3.34.0 |
| A21 | Suche (Strg/Cmd+O) | Der Textausschnitt eines Inhaltstreffers normalisierte jedes Zeichen einzeln; bei 10.000 Punkten lag die Eingabe bis zur gezeichneten Liste mit 99–101 ms (eingefrorene 3.33.21: 100,8 ms) genau an der Grenze, ab der der Plan einen FTS5-Index vorsah [Messung `messung_suche.py`, Profil] | Engpass | Arbeitsstand 3.34.0: Positionsabbildung per Halbierungssuche, gleichwertig zur alten Fassung (Unit-Test), Median 66,6 ms; P07 ✕; geliefert 3.34.0 |
| A22 | Seiten | Zwei Bilder auf aufeinanderfolgenden Absätzen überlappten (nachgestellt: drei Bilder links, je 30 px versetzt übereinander); Druck und „Markdown kopieren“ zeigten statt der Bilder nur Dateinamen, Markdown-Import machte Bilder zu Textverweisen [Code, Nachstellprobe] | Fehler bzw. Lücke (B4) | geliefert 3.34.0 |
| A23 | Pixel-Werkstatt, Farbleiste | Mit dem neuen Doppelklick (G19) passte auch ein dritter Klick auf die Doppelklick-Bindung und öffnete „ersetzen durch …“ erneut – mit der Farbe, die nach dem Ersetzen an dieser Stelle steht [Prüfung `test_pixel3350`] | Fehler im Arbeitsstand | vor der Lieferung behoben: Dreifachklick abgefangen, in der Suite geprüft; geliefert 3.35.0 |

## 4. Oberflächenanalyse

Grundlage: Code (`_refresh_tree`, `sync_view_chrome`, `pack_header_controls`, Seitenleiste, Dialoge), Prüfsuiten zu Mindestgröße/Kontrast/festem Layout und die Fensterfotos der Mac-Vollprüfung vom 08.10.2026 (lokal, nicht versioniert).

**Aufbau.** Ein Fenster mit drei festen Zonen: Seitenleiste (Systemzeilen Startseite/Heute/Labels/Vorlagen/Papierkorb, bedingt „Eingang“, angeheftete Seiten, vier klappbare Bäume Seiten → Listen → Notizen → Zeichnungen), Kopf (Titel, Kennzahlen in der Unterzeile, bis zu vier Symbolknöpfe) und Inhaltskarte mit Werkzeugband oben und Kartenfuß unten. Feste Kanten werden durch `test_festlayout330`/`test_kartenfuss330` erzwungen [Code][Test].

**Navigation.** Primär über die Seitenleiste; gleichwertig über die Palette (Strg/Cmd+O, `>` für Aktionen), Menüleiste und Kürzel. Stabile Aktionskennungen seit 3.33.11 verhindern, dass ein umbenannter Eintrag eine falsche Aktion auslöst [Code][Test]. Ansichtswechsel innerhalb einer Liste: Liste · Tabelle · Pinnwand fest nebeneinander.

**Interaktionen.** Kontextmenü an jeder Zeile, Auswahlleiste im Kartenfuß bei Mehrfachauswahl, Ziehen nach D02 mit sichtbarem Ziel, Zeilenaktion „Einplanen“ beim Überfahren, Undo für jede Aktion. Tastaturwege fehlen noch für Pinnwand und Seitenbäume (H-02-Rest) [Dok][Code].

**Zustände.** Leerzustände mit Gismo und einer Anlegen-Aktion; Schreibschutz bei neuerem Format oder Fremdbelegung mit Grund; Fehler- und Speicherfehlerwege mit Rücknahme. Ladezustände gibt es kaum, weil Aufbau synchron ist; lange Aufbauten (Heute bei 10.000 Aufgaben, Einstellungsfenster) zeigen keinen Fortschritt [Code][Einschätzung].

**Nutzerführung.** Hinweiszeilen je Ansicht einklappbar (D11, Vorgabe eingeklappt), Tooltips (höchstens einer), Feldchips der Schnelleingabe, Handbuch und Kürzelübersicht. Keine Einführung für neue Nutzer (bewusst nicht, N06).

**Inkonsistenzen und Potenziale** (Aufgaben im Entwicklungsplan §15):

| Nr. | Befund | Prinzip | Aufgabe |
|---|---|---|---|
| O01 | Eingabezeile mit zwei Textknöpfen „Hinzufügen“ und „Erweitert“; „Erweitert“ verschwindet bei schmalem Fenster ganz und ist dann nur über Menü erreichbar [Code] | P4, P5 | U04 |
| O02 | Kein Erscheinungsbild „wie System“; der Hell/Dunkel-Schalter wechselt nur zum Gegenstück des gewählten Designs [Code] | P1 | N01/U17 |
| O03 | Lila erscheint auch für aktive Zustände (Auswahl, geöffnete Ansicht), nicht nur für Hinzufügen [Dok] | P2 | U15 |
| O04 | Leerzustände zeigen teils zwei Wege zum Anlegen (Knopf in der Fläche und „+“) [Dok] | P3 | U20 |
| O05 | Pinnwandleiste belegt dauerhaft eine ganze Werkzeugzeile [Dok] | P4 | U09 |
| O06 | Seitentitel steht nur im Kopf, nicht im Dokument; leere Seite ohne Schreibhinweis [Dok] | P1 | U18 |
| O07 | Gismo-Kachel mit dauerhaft sichtbaren Pflegeknöpfen [Dok] | P4, P5 | U05-Rest |
| O08 | Nach einem Update sieht man nicht, was neu ist; Gewohnheitsbrüche (D10/D12/D14) bleiben unerklärt (R9) [Einschätzung] | P1 | N07 |
| O09 | Zwei Dialoge unter Windows sehr breit, Knopfreihe links (W05); Hinweis doppelt (W07); kleines Pixelraster (W08) [Dok] | P2, P4 | W05/W07/W08 |
| O10 | Bilder in Seiten können sich auf gleicher Höhe überlappen [Dok] | P1 | B4 |
| O11 | Eingeklappte Seitenleiste blendet ganz aus; eine schmale Zwischenstufe fehlt [Dok] | P4 | OB05 |

## 5. Entscheidungsanalyse

**Getroffen und begründet** (Register: [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md)):

| Gruppe | Entscheidungen | Begründung (Kurzfassung) | Wirkung auf den Sprint |
|---|---|---|---|
| Planungslogik | D01, D02, D10, D13, D14 | Bearbeitungstag ≠ Fälligkeit; eine Aktion ändert nur das im Ziel sichtbare Feld; zwei Hauptansichten | Jede neue Planungsaktion (KO02, KO03, AU06) setzt nur das genannte Feld und ist ein Undo-Schritt |
| Architektur | D16, D17, Q2, Q3, Formatregel 29.09.2026 | JSON bleibt Hauptspeicher; Fachlogik Tk-frei; keine plattformeigenen Abhängigkeiten; KI über Dokumente | Neue Logik als Modul mit Unit-Tests; G24 bleibt dateibasiert; FTS5 nur als löschbarer Cache |
| Oberfläche | D04, D06, D08, D11, D12, P1–P6, Hausregeln | Weniger dauerhaft sichtbar; Farben nach Rolle; feste Kanten | Jede neue Fläche besteht den Prinzipien-Check und die Mindestgröße |
| Ablage und Prüfung | D09, Dokumentenpflege 03.10.2026, Paketauftrag 07.10.2026 | öffentliche Ablage, ein Thema ein Dokument, Pakete statt Einzelschnitte | Analyse in einem Dokument; ein eingefrorener Volllauf je Paket |
| Plattform | D03, D15, E-01 27.09.2026 | Desktop/Tk; Python 3.14/Tk 9; Paket später | Mac-Vollprüfung jetzt möglich; Paketierung bleibt Stufe 4 |

**Bewusst verworfen** (nicht erneut vorlegen): Konten/Cloud/Mehrbenutzer, Zustellung bei geschlossener App (N09), MCP-Server (N10), systemweiter Hotkey (G07/N14), Einstieg für neue Nutzer (N06), gleichzeitige Bearbeitung (G23), verschlüsselte Ablage (G22), Spalten in Seiten und Graph (G12/G13), eigene Felder je Liste (ZF-200), Spracherfassung/Cloud-KI/Team/Web Clipper (N15–N20), freie Klebezettel, Bilder aus dem Netz, Unterseiten, allgemeine Umwandlung (D05).

**Offen beim Inhaber** und was davon abhängt:

| Frage | Blockiert | Empfehlung (keine Entscheidung) |
|---|---|---|
| D07 Animationsexport | G17 | zuerst Frames/Vorschau/PNG-Spritesheet, GIF später |
| I7 Referenzentwürfe | OB02, OB03-Rest, N05 mit KO04 | Entwürfe liefern; alternativ N05 ausdrücklich ohne Entwurf mit bestehenden Rollen freigeben |
| AU03 Vorgabe automatischer Tageshinweise | AU03-Rest | Option, Vorgabe aus (wie Systemmitteilungen seit 27.09.2026) |
| OB04 dezente Bewegung | OB04 | erst nach den Tempozielen aus §3 |
| AU07 Termine als belegte Zeit | AU07 | nur lesend aus einer gewählten ICS-Datei, ohne Abo; berührt die Produktgrenze |
| G21 erste Importquelle | G21 | Notion-Markdown/ZIP (Vorbild des Inhabers) |
| G26/D15 Bauwerkzeug | G26, danach N12 | PyInstaller ≥ 6.22 als reine Bauabhängigkeit |
| I8 Logo unter Tk 8.6 | LG01–LG04 | Weg B (vorgerechnetes RGBA-PNG) und Weg D (Prüfschärfe) |
| I1–I4, I6, I9–I11 | Veröffentlichung, menschliche Abnahme | siehe Entwicklungsplan §11 |
| Symbolschriften (A14) | einheitliche Symbolgröße | Zeichen wählen, die die Systemschrift enthält, oder eine mitgelieferte Symbolschrift (bräuchte eine Entscheidung) |

**Widerspruch mit Vorschlag:** A04 – N01/U17 ist eine Systemkonvention (P1) und kein Gestaltungsumbau im Sinn von R12. Vorschlag: N01 ohne I7 umsetzen; das Design „Pixel“ als Signaturdesign vorn bleibt Teil von N01, ohne neue Farben. Begründung und Umsetzung im Entwicklungsplan §15.

## 6. Nutzungsanalyse

**Nutzergruppen.** Belegt ist nur der Inhaber als täglicher Nutzer auf Mac und Windows mit eigenem Bestand [Dok]. Als erste Zielgruppe nennt die Marktanalyse Menschen, die am Desktop mehrere eigene Projekte bearbeiten (Gestaltung, Schreiben, Entwicklung, Wissensarbeit) [Einschätzung, Markt §1.1]. Unternehmensalltag mit Vorlagen ist in der [Vorlagenpraxis](../01_Repository/Glide/docs/27_VORLAGEN_PRAXISANLEITUNG.md) beschrieben [Dok]. Weitere Gruppen sind unbestätigt.

**Anwendungsfälle und Arbeitsabläufe** (aus Funktionen und Vorlagen abgeleitet):

| Ablauf | Schritte heute | Schwierigkeit [Einschätzung] | Potenzial (Aufgabe) |
|---|---|---|---|
| Morgens den Tag planen | Heute → Tagesbeginn → Vorschlag übernehmen → Raster | Routinen (Morgen/Abend) sind verstreute Wiederholungen | AU06 Routinen in Heute |
| Unterwegs Gesammeltes übernehmen | Liste öffnen, Zeilen einfügen oder einzeln tippen | Mehrere Zeilen in der Eingabezeile werden ein Titel | KO05 |
| Routine verpasst | Wiederkehrende Aufgabe überfällig, Abhaken rückt nur einen Schritt vor | Mehrfaches Abhaken bis heute; kein „überspringen“ | KO02 |
| Termin mit Hinweis erfassen | Erfassen, danach Maske für Erinnerung öffnen | Zweiter Weg für ein häufiges Feld | KO03 |
| Aufgaben umsortieren | „Verschieben nach …“ mit allen Listen alphabetisch | Lange Menüs bei großem Bestand | KO06 |
| Projektseite pflegen | Seite mit Bildern, Aufgaben, Live-Liste | Bilder überlappen, fehlen im Druck/Markdown | B4 |
| Etwas wiederfinden | Palette mit Inhaltssuche | Fundstelle im Dokument nicht markiert | G14-Hervorhebung |
| Filter verstehen | gespeicherte Filter | Unklar, warum etwas fehlt | D-03 |
| Mit KI arbeiten | „Für KI bereitstellen“ → externes Werkzeug → Ergebnis importieren | Bestehende Aufgaben werden nicht geändert, nur neu angelegt | G24 |
| Sicherung prüfen | Backup-Ordner, Wiederherstellen | Unterschiede zweier Stände nicht sichtbar | F-03 |
| Pixelsymbol gestalten | Zeichnung, Palette, Export | Palettenänderung färbt nicht um; keine Vorschau in Zielgrößen | G19, G-03 |
| Abends hell/dunkel | Design wählen | System-Wechsel wird nicht übernommen | N01 |

**Anforderungen, die daraus folgen** [Einschätzung]: kurze Wege für häufige Planungsfelder; keine zusätzliche Dauerfläche; jede Änderung mit Vorschau und einem Undo; Tempo bei großen Beständen; Daten bleiben lokal.

## 7. Pflege

Bei der nächsten Analyse fortschreiben statt kopieren. Befunde mit „Behoben“ erst entfernen, wenn eine neue Analyse den Abschnitt ersetzt; ihre Vorfassung trägt Git.
