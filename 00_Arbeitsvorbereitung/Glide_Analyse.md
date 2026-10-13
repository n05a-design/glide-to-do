# Glide – Analyse: Funktionen, Oberfläche, Entscheidungen, Nutzung

Stand 13.10.2026 · Glide 3.40.0 · Aufgabenformat 24 · Analyse vom 08.10.2026, fortgeschrieben am 12.10.2026 nach Paket 2 und während der Paket-3-Neuabnahme (Code, Dokumente, Git-Historie, Plattformnachweise); Bestandsaufnahme und Gap-Analyse nach Wettbewerbs- und Codeabgleich am 13.10.2026 (§8)

Bestandsaufnahme im Auftrag vom 08.10.2026: lokale Ablage untersuchen, Dokumentation und Code abgleichen, daraus den Sprint ableiten. Dieses Dokument trägt die **Analyse** (Funktions-, Oberflächen-, Entscheidungs- und Nutzungsanalyse sowie den Abgleich Dokumentation ↔ Code). Der Wettbewerb steht in [Markt und Vorbilder](Glide_Markt_und_Vorbilder.md), die Entscheidungen selbst in der [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md), die daraus abgeleiteten Aufgaben ausschließlich im [Entwicklungsplan, Abschnitt 14](Glide_Entwicklungsplan.md#14-sprint-ab-08102026-aufgabenkatalog). Erledigte Befunde werden hier als erledigt markiert, nicht gelöscht, bis die nächste Analyse sie ersetzt.

**Belegstufen** in allen Tabellen: **[Code]** im Quellstand nachgelesen · **[Test]** durch eine automatische Prüfung belegt · **[Mac]** in der nativen Mac-Vollprüfung vom 08.10.2026 (Python 3.14.5, Tk 9.0.3, künstliche Daten) gesehen · **[Dok]** nur in Dokumenten belegt · **[Einschätzung]** eigene Schlussfolgerung · **[Unbestätigt]** Annahme ohne Beleg. Es liegen **keine Nutzungsdaten** vor (keine Telemetrie nach Produktgrenze, keine Nutzerstudie); Aussagen über Nutzer sind deshalb als Einschätzung gekennzeichnet.

## 1. Untersuchter Bestand

| Bereich | Umfang am 09.10.2026 (3.35.0) | Beleg |
|---|---|---|
| Code | `src/glide/app.pyw` 57.409 Zeilen, 35 Begleitmodule (davon 27 Tk-freie Fachmodule nach D17); am 08.10.2026 waren es 55.826 Zeilen und 27 Module | [Code] |
| Tests | 82 Integrationssuiten, 257 Unit-Tests, 34 Werkzeugtests, fünf Analysen (08.10.2026: 76 Suiten, 170 Unit-Tests) | [Code], [Test] |
| Dokumente | 44 Markdown-Dokumente außerhalb der Nachweisordner; Planung, Entscheidungen, Funktionen, QA, Daten, Markt | [Dok] |
| Git | Arbeitsstand 3.33.9–3.35.0 am 09.10.2026 eingecheckt (Commit `6098877` auf `claude/glide-3.33.15`); die Dokumentationscommits aus `main` (PR #15) waren am 08.10.2026 per Drei-Wege-Abgleich übernommen | [Code] |
| Laufzeit auf dem Referenz-Mac | Python 3.14.5 (python.org) mit Tk 9.0.3; python.org führt inzwischen 3.14.8 (30.09.2026) | [Code], [Mac] |

**Sprintfortsetzung 12.10.2026:** Der Tabellenbestand oben bleibt die datierte 3.35.0-Baseline. Fundament/Tempo 3.36.0 und Logo/Symbole 3.37.0 sind inzwischen mit Mac-/Linux-/Windows-Vollprüfungen geliefert. Der Tk-8.6-Logorückfall samt App-Symbolen und Systemzeichen ist damit umgesetzt; Sicht-/DPI-Abnahme bleibt getrennt. Paket 3 / 3.38.0 ist am Hash bcdbc4da nach korrigierten Auswahl-/Windows-Menübefunden auf Mac/Linux/Windows vollständig automatisch geliefert: 42 Code-Dateien, 85 Suiten/294 Units, gemeinsamer Inspektor, direkte Felder, Textstufen und Übergänge. Paket 4 / 3.39.0 ist am Hash 7995ecbc auf Mac/Linux/Windows automatisch geliefert: 51 Code-Dateien, 86 Suiten/432 Units. Gewählte Folgepakete und Stufen stehen in [Plan §15.7](Glide_Entwicklungsplan.md#157-bestätigter-gesamtplan-acht-produktionsversionen), Ergebnisse im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md).

## 2. Funktionsanalyse

Vollständigkeit: **●** im Alltag vollständig nutzbar · **◐** nutzbar mit dokumentierter Lücke · **○** fehlt. „Plattform“ meint die zuletzt automatisch geprüften Systeme.

| Bereich | Vorhanden (Version) | Vollständigkeit | Offene Erweiterung (Aufgabe) |
|---|---|---|---|
| Erfassen | Schnelleingabe mit Feldchips (D01/D10), Wiederholungen, Erinnerung als Chip (3.33.20), „/“-Befehle, Labels, mehrzeiliges Einfügen auch in die Eingabezeile (3.33.20), „+“ und Umschalt+Enter | ● | – |
| Heute und Planung | Heute/Demnächst, Tagesbeginn/-abschluss, Vorschlag, verfügbare Zeit, Einplanen, Zeitblöcke, Fokus, Woche/Routinen; seit 3.39.0 optionale Tageshinweise, gemeinsame lokale ICS-Belegzeiten und ausdrückliche Mehrfachentlastung | ● | 3.39.0 geliefert; tatsächliche Menschenabnahme offen |
| Wiederholungen | Regeln täglich … jährlich, Enddatum, Anker gegen Monatsende-Drift; Termin und verpasste Termine überspringen (3.33.20) | ● | – |
| Listen, Tabelle, Board | Gruppierung inkl. Eisenhower, Auswahlleiste, Tabellenspalten, gemeinsamer Inspektor und direkte Felder im Quellstand 3.38.0, zuletzt benutzte Ziele (3.33.20) | ● | N05/KO04 in 3.38.0 geliefert, Mac/Linux/Windows automatisch grün; Menschen-/DPI-Abnahme getrennt offen |
| Pinnwand | frei/geordnet/Spaltenboard, Bereiche, Verbindungen, Präsentation, eine Werkzeugzeile (3.33.21), Tastaturwege mit Hinweis (3.34.0) | ● | – |
| Seiten und Notizen | Block-Editor, Bilder ohne Überlappung und in Druck/Markdown (3.34.0), Aufgaben mit Original-ID, Verweise/Rückverweise, Live-Listen, Titelbild, Seitentitel im Dokument (3.33.21) | ● | – |
| Suche | gemeinsame Palette für Inhalte und Aktionen, Treffer im Dokument markiert (3.34.0), erklärte gespeicherte Filter (3.34.0); 66,6 ms bei 10.000 Punkten | ● | – (FTS5 nach Messung nicht nötig) |
| Erinnerungen | fest/relativ, Zustellbeleg, Systemmitteilung (Option) bei laufender App | ● | Zustellung bei geschlossener App bewusst nicht (N09) |
| Pixel-Werkstatt | 16–128 Zellen, Werkzeuge, Paletten mit Umfärben und Vorschau (3.35.0), ICO mit Symbolvorschau (3.35.0), PNG/SVG/JSON, Pixelsymbol | ◐ | Animation (G17, E-S1/D07) |
| Austausch | CSV, Markdown mit Bildern, ICS, `.glidepage`, Backups, KI-Austausch Stufe 1 und 2 (3.35.0), Sicherungen vergleichen (3.35.0) | ◐ | erste Fremdquelle (G21, E-S4) |
| Erscheinungsbild | zehn Designs, „Automatisch hell/dunkel“ (3.33.21), neutrale aktive Rolle, schmale Seitenleiste, berechneter Kontrast, Mindestgröße 860 × 700 | ◐ | Hierarchie, Zeilenaktionen und Bewegung mit 3.38.0 geliefert, Mac/Linux/Windows automatisch grün; Menschen-/DPI-Abnahme getrennt offen |
| Hilfe | Handbuch, Kürzel, einklappbare Hinweise (D11), Showcase/Rundgang, Karte „Neu in Glide“ (3.33.20) | ● | – |
| Betrieb | Formatschutz bis Format 23, Vorsicherungen, Sperrdatei, Sicherungen nur bei Änderung, Mindestversion beim Start (3.33.20), Linux-JPEG-Vorschau mit Systemwerkzeug (3.34.0) | ◐ | Paket mit eigenem Python (G26, S26-10); Logo/Symbole mit 3.37.0 automatisch geprüft, menschliche Sichtabnahme offen |
| Tempo | Abhaken 17/61/118 ms bei 1.000/5.000/10.000 Punkten, Bildlayout, einmal schreiben/aufbauen, unveränderte Startseite 0,3 ms (3.33.19) | ◐ | 3.39.0: fünf direkte Prozesse/200 warme Werte; Startseite kalt p95 294 ms, warm Median/p95 72/78 ms; Einstellungen zuerst p95 203 ms, erneut 136/170 ms. D46/D48 erfüllt; historische Ausnahmen/Messreihen im QA-Bericht |

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
| A24 | Architektur §1 „Laufzeit“ | nannte als aktuell geprüft Mac 3.35.0 und Windows 3.33.18, Linux offen; seit 3.36.0 laufen je Lieferung Mac-, Linux- und Windows-Vollprüfungen [QA] | veraltet | 13.10.2026: Versionsangabe durch Verweis auf den QA-Bericht ersetzt |
| A25 | Markt und Vorbilder §1 Punkt 3, §4 (Animation), §4.1 (Komfort, Gestaltung) | Inspektor, Felder am Objekt und OB02/OB03 als offen „nach I7“, Animation „D07 offen“; geliefert in 3.38.0 bzw. entschieden durch D18 [Dok] | veraltet | 13.10.2026 berichtigt |
| A26 | `repeat_rules.py` gegenüber `ics_recurrence.py` | zwei getrennte Wiederholungsrechner: Aufgaben kennen sechs feste Arten ohne Intervall für Woche/Monat/Jahr; der ICS-Leser (3.39.0) rechnet INTERVAL, COUNT, UNTIL, BYDAY mit Ordinal, BYMONTHDAY und BYSETPOS [Code] | technische Doppelung | offen; Vorschlag FP-02 ([Plan §16](Glide_Entwicklungsplan.md#16-vorschläge-aus-wettbewerbs--und-open-source-analyse-13102026)) |
| A27 | `SavedFilters.normalize_settings`, `ItemWorkspace.prune` | Unbekannte Schlüssel auf oberster Ebene der Einstellungen bleiben erhalten (`normalize_personal_settings` kopiert `dict(data)`); innerhalb bekannter Strukturen bauen die Normalisierer Einträge aber nur aus bekannten Schlüsseln, und `prune` behält als Seitenkarte nur Zeichnungen. Einstellungen haben kein Formattor. Eine Erweiterung **innerhalb** gespeicherter Filter oder der Pinnwand würde von einer älteren Fassung beim nächsten Einstellungsschreiben still gekürzt [Code; Nachprüfung 13.10.2026] | Vorwärtsverträglichkeit fehlt | offen; WA-09 vor FP-04; FP-03 kann über einen eigenen Schlüssel auf oberster Ebene ohne WA-09 auskommen |
| A28 | ICS-Ausgabe `ics_repeat_rule`, ICS-Import `ics_repeat_from_rule` | „monatlich“ wird als `FREQ=MONTHLY`, „jährlich“ als `FREQ=YEARLY` ausgegeben. Glide klemmt Termine am 29.–31. auf das Monatsende (31.01. → 28.02. → 31.03.), ein RFC-5545-Leser überspringt Monate ohne diesen Tag (31.01. → 31.03. → 31.05.); bei „jährlich ab 29.02.“ fehlen dort drei von vier Jahren. Umgekehrt wird eine importierte Monatsserie am 31. in Glide zusätzlich auf Monatsenden gelegt – entgegen dem eigenen Grundsatz der Methode, nicht Abbildbares zu verwerfen. Korrektur `BYMONTHDAY=28,29,30,31;BYSETPOS=-1` (bzw. 28,29,30 / 28,29; jährlich mit `BYMONTH=2`) stimmt in allen fünf Proben mit Glides Folge überein [Code; Probe `probe_wiederholung.py`] | Fehler (Randfall, Austausch) | behoben in 3.39.1 (geliefert); WA-17 in FP-00 |
| A29 | Schnelleingabe `capture_parser._wiederholung` | Wiederholungsangaben mit Ankertag werden teilweise erkannt und anders gebildet als gemeint: „monatlich am 15.“ und „jeden Monat am Ersten“ wiederholen ab heute (13.), „am 15.“ bleibt Titeltext; „wöchentlich montags“, „alle 2 Wochen montags“ und „… montags und donnerstags“ wiederholen ab heute (Dienstag), die Wochentage bleiben Titeltext; „alle 2 Wochen am Montag“ setzt eine Dienstagsserie und zusätzlich Montag als Bearbeitungstag; „jeden zweiten Dienstag“, „jeden 2. Dienstag“ und „jeden ersten Montag im Monat“ ergeben nur einen einmaligen Bearbeitungstag. Der Chip nennt dabei nur Art und Fälligkeit („Wiederholung monatlich · fällig ab Di 13.10.2026“), die Abweichung fällt erst beim genauen Lesen auf [Code; Probe `probe_wiederholung.py`, Stichtag Dienstag 13.10.2026] | Fehler (Kernfunktion Erfassen) | behoben in 3.39.1 (geliefert); WA-18 in FP-00 |
| A30 | ICS-Import der Aufgaben `parse_ics_moment` | `TZID` wurde nur über die Zeitzonendatenbank des Systems gelesen: Windows-Namen wie „W. Europe Standard Time“ fielen immer auf Ortszeit zurück, unter Windows ohne Systemdatenbank auch jeder IANA-Name; der Import meldete dann „tzid“. Belegzeiten (3.39.0) nutzten bereits die mitgelieferten Daten [Code; Gegenprobe `tests/qa-3.39.1/wiederholung_2026-10-13/gegenprobe.py` an 3.39.0] | Fehler (Plattform, Austausch) | behoben in 3.39.1 (geliefert); mit FP-00 |

## 4. Oberflächenanalyse

Grundlage: Code (`_refresh_tree`, `sync_view_chrome`, `pack_header_controls`, Seitenleiste, Dialoge), Prüfsuiten zu Mindestgröße/Kontrast/festem Layout und die Fensterfotos der Mac-Vollprüfung vom 08.10.2026 (lokal, nicht versioniert).

**Aufbau.** Ein Fenster mit drei festen Zonen: Seitenleiste (Systemzeilen Startseite/Heute/Labels/Vorlagen/Papierkorb, bedingt „Eingang“, angeheftete Seiten, vier klappbare Bäume Seiten → Listen → Notizen → Zeichnungen), Kopf (Titel, Kennzahlen in der Unterzeile, bis zu vier Symbolknöpfe) und Inhaltskarte mit Werkzeugband oben und Kartenfuß unten. Feste Kanten werden durch `test_festlayout330`/`test_kartenfuss330` erzwungen [Code][Test].

**Navigation.** Primär über die Seitenleiste; gleichwertig über die Palette (Strg/Cmd+O, `>` für Aktionen), Menüleiste und Kürzel. Stabile Aktionskennungen seit 3.33.11 verhindern, dass ein umbenannter Eintrag eine falsche Aktion auslöst [Code][Test]. Ansichtswechsel innerhalb einer Liste: Liste · Tabelle · Pinnwand fest nebeneinander; seit 3.33.21 eine schmale Seitenleiste mit Symbolen.

**Interaktionen.** Kontextmenü an jeder Zeile, Auswahlleiste im Kartenfuß bei Mehrfachauswahl, Ziehen nach D02 mit sichtbarem Ziel, Zeilenaktion „Einplanen“ beim Überfahren, Undo für jede Aktion. Seit 3.34.0 gibt es Tastaturwege auch für Pinnwand und alle Bereichsbäume (H-02r) [Code][Test].

**Zustände.** Leerzustände mit Gismo und einer Anlegen-Aktion; Schreibschutz bei neuerem Format oder Fremdbelegung mit Grund; Fehler- und Speicherfehlerwege mit Rücknahme. Ladezustände gibt es kaum, weil Aufbau synchron ist; lange Aufbauten (Heute bei 10.000 Aufgaben, Einstellungsfenster) zeigen keinen Fortschritt [Code][Einschätzung].

**Nutzerführung.** Hinweiszeilen je Ansicht einklappbar (D11, Vorgabe eingeklappt), Tooltips (höchstens einer), Feldchips der Schnelleingabe, Handbuch und Kürzelübersicht. Keine Einführung für neue Nutzer (bewusst nicht, N06).

**Inkonsistenzen und Potenziale** (Aufgaben im Entwicklungsplan §14; Stand 09.10.2026):

| Nr. | Befund | Prinzip | Aufgabe |
|---|---|---|---|
| O01 | Eingabezeile mit zwei Textknöpfen „Hinzufügen“ und „Erweitert“; „Erweitert“ verschwindet bei schmalem Fenster ganz und ist dann nur über Menü erreichbar [Code] | P4, P5 | U04 ✅ 3.33.20 |
| O02 | Kein Erscheinungsbild „wie System“; der Hell/Dunkel-Schalter wechselt nur zum Gegenstück des gewählten Designs [Code] | P1 | N01/U17 ✅ 3.33.21 |
| O03 | Lila erscheint auch für aktive Zustände (Auswahl, geöffnete Ansicht), nicht nur für Hinzufügen [Dok] | P2 | U15 ✅ 3.33.21 |
| O04 | Leerzustände zeigen teils zwei Wege zum Anlegen (Knopf in der Fläche und „+“) [Dok] | P3 | U20 ✅ 3.33.20 |
| O05 | Pinnwandleiste belegt dauerhaft eine ganze Werkzeugzeile [Dok] | P4 | U09 ✅ 3.33.21 |
| O06 | Seitentitel steht nur im Kopf, nicht im Dokument; leere Seite ohne Schreibhinweis [Dok] | P1 | U18 ✅ 3.33.21 |
| O07 | Gismo-Kachel mit dauerhaft sichtbaren Pflegeknöpfen [Dok] | P4, P5 | U05r ✅ 3.33.21 |
| O08 | Nach einem Update sieht man nicht, was neu ist; Gewohnheitsbrüche (D10/D12/D14) bleiben unerklärt (R9) [Einschätzung] | P1 | N07 ✅ 3.33.20 |
| O09 | Zwei Dialoge unter Windows sehr breit, Knopfreihe links (W05); Hinweis doppelt (W07); kleines Pixelraster (W08) [Dok] | P2, P4 | W05 ✅ 3.33.21; W07/W08 ◇ Windows-Sichtprüfung |
| O10 | Bilder in Seiten können sich auf gleicher Höhe überlappen [Dok] | P1 | B4 ✅ 3.34.0 |
| O11 | Eingeklappte Seitenleiste blendet ganz aus; eine schmale Zwischenstufe fehlt [Dok] | P4 | OB05 ✅ 3.33.21 |

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

**Auswahl- und Umsetzungsstand 12.10.2026:** Alle Funktionskandidaten durch D18–D43 entschieden; Paket 1 (3.36.0) und Paket 2 (3.37.0) umgesetzt und geliefert. Paket 3 (3.38.0, Apphash bcdbc4da) ist ebenfalls automatisch geliefert: Mac/Linux/Windows-Vollprüfung grün, 07/Showcase/Bundle nach der nativen Matrix erneut bytegleich und signaturgeprüft. Weitere Pakete bleiben beauftragt. N12/P05 ausdrücklich erste Stufe; Animation, OB02/OB03/N05/KO04 nach Bild 1, Tageshinweise, Notion einschließlich Wiedererkennung, eigenständige Mac-/Windows-Pakete, Logo/Symbole einschließlich Master/Kleingrößen, ICS-Belegzeiten, Bewegung, Bedienflächenziel, P03/E01-Rest, Linux-Matrix, Seitenwiederherstellung und Tag entlasten jeweils vollständig im angebotenen Rahmen. Native Windows-Vollprüfung je Lieferung gewählt (D42). Gesamtplan mit „ja“ bestätigt (D44), Logoentwürfe vor Masterübernahme freigegeben (D45), Tempoausnahmen D46/D47 und Folgeentscheidung D48 entschieden (Einstellungen künftig warm Median ≤ 150 ms/p95 ≤ 190 ms, erste Anzeige ≤ 250 ms). Phase 2 läuft; Paket 1 und Paket 2 sind auf Mac/Linux/Windows automatisch grün, 07/Showcase/Bundle bytegleich und signaturgeprüft. Offen: tatsächliche Menschen-/Readerabnahme; Veröffentlichungstore I1–I5/I9–I11 bleiben nach D43 gesondert offen. Aufgaben, acht bestätigte Versionen und Abnahmetore ausschließlich im [Entwicklungsplan §15](Glide_Entwicklungsplan.md#15-neuer-feature-sprint-ab-09102026-gemeinsame-planung).

**Widerspruch mit Vorschlag:** A04 – N01/U17 ist eine Systemkonvention (P1) und kein Gestaltungsumbau im Sinn von R12. Vorschlag war, N01 ohne I7 umzusetzen; so geschehen in 3.33.21 (Pixel als Signaturdesign vorn, ohne neue Farben).

## 6. Nutzungsanalyse

**Nutzergruppen.** Belegt ist nur der Inhaber als täglicher Nutzer auf Mac und Windows mit eigenem Bestand [Dok]. Als erste Zielgruppe nennt die Marktanalyse Menschen, die am Desktop mehrere eigene Projekte bearbeiten (Gestaltung, Schreiben, Entwicklung, Wissensarbeit) [Einschätzung, Markt §1.1]. Unternehmensalltag mit Vorlagen ist in der [Vorlagenpraxis](../01_Repository/Glide/docs/27_VORLAGEN_PRAXISANLEITUNG.md) beschrieben [Dok]. Weitere Gruppen sind unbestätigt.

**Anwendungsfälle und Arbeitsabläufe** (aus Funktionen und Vorlagen abgeleitet):

| Ablauf | Schritte am 08.10.2026 | Schwierigkeit [Einschätzung] | Potenzial (Aufgabe, Stand 09.10.2026) |
|---|---|---|---|
| Morgens den Tag planen | Heute → Tagesbeginn → Vorschlag übernehmen → Raster | Routinen (Morgen/Abend) sind verstreute Wiederholungen | AU06 Routinen in Heute ✅ 3.33.20 |
| Unterwegs Gesammeltes übernehmen | Liste öffnen, Zeilen einfügen oder einzeln tippen | Mehrere Zeilen in der Eingabezeile werden ein Titel | KO05 ✅ 3.33.20 |
| Routine verpasst | Wiederkehrende Aufgabe überfällig, Abhaken rückt nur einen Schritt vor | Mehrfaches Abhaken bis heute; kein „überspringen“ | KO02 ✅ 3.33.20 |
| Termin mit Hinweis erfassen | Erfassen, danach Maske für Erinnerung öffnen | Zweiter Weg für ein häufiges Feld | KO03 ✅ 3.33.20 |
| Aufgaben umsortieren | „Verschieben nach …“ mit allen Listen alphabetisch | Lange Menüs bei großem Bestand | KO06 ✅ 3.33.20 |
| Projektseite pflegen | Seite mit Bildern, Aufgaben, Live-Liste | Bilder überlappen, fehlen im Druck/Markdown | B4 ✅ 3.34.0 |
| Etwas wiederfinden | Palette mit Inhaltssuche | Fundstelle im Dokument nicht markiert | G14-Hervorhebung ✅ 3.34.0 |
| Filter verstehen | gespeicherte Filter | Unklar, warum etwas fehlt | D-03 ✅ 3.34.0 |
| Mit KI arbeiten | „Für KI bereitstellen“ → externes Werkzeug → Ergebnis importieren | Bestehende Aufgaben werden nicht geändert, nur neu angelegt | G24 ✅ 3.35.0 |
| Sicherung prüfen | Backup-Ordner, Wiederherstellen | Unterschiede zweier Stände nicht sichtbar | F-03 ✅ 3.35.0 |
| Pixelsymbol gestalten | Zeichnung, Palette, Export | Palettenänderung färbt nicht um; keine Vorschau in Zielgrößen | G19, G-03 ✅ 3.35.0 |
| Abends hell/dunkel | Design wählen | System-Wechsel wird nicht übernommen | N01 ✅ 3.33.21 |

**Anforderungen, die daraus folgen** [Einschätzung]: kurze Wege für häufige Planungsfelder; keine zusätzliche Dauerfläche; jede Änderung mit Vorschau und einem Undo; Tempo bei großen Beständen; Daten bleiben lokal.

## 7. Pflege

Bei der nächsten Analyse fortschreiben statt kopieren. Befunde mit „Behoben“ erst entfernen, wenn eine neue Analyse den Abschnitt ersetzt; ihre Vorfassung trägt Git.

## 8. Bestandsaufnahme und Gap-Analyse (13.10.2026)

Auftrag des Inhabers vom 12./13.10.2026: vor Wettbewerbsrecherche und Feature-Planung den tatsächlichen Entwicklungsstand verifizieren; maßgeblich ist der Code. Grundlage: Arbeitskopie auf `claude/glide-sprint-2026-10-09`, Commit `c38d960`, `VERSION` 3.39.0, `src/glide/app.pyw` mit SHA-256 `7995ecbc…` (gleich `07_Python-Versionen`). Keine Produktionsänderung, kein GUI-Lauf. Belegstufen wie oben, zusätzlich **[QA]** = im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md) belegter automatischer Prüfstand. Wettbewerb und Codeanalyse fremder Projekte: [Markt und Vorbilder §9](Glide_Markt_und_Vorbilder.md#9-wettbewerbs--und-open-source-analyse-13102026); Pakete: [Entwicklungsplan §16](Glide_Entwicklungsplan.md#16-vorschläge-aus-wettbewerbs--und-open-source-analyse-13102026).

**Statuswerte:** **Implementiert** (im Code, automatisch geprüft) · **Teilweise** (vorhanden, mit benannter Lücke) · **Fehlerhaft** (reproduzierbares Problem) · **Geplant** (dokumentiert, nicht im Lieferstand) · **Nicht vorhanden** · **Unklar** (noch zu verifizieren). „Implementiert“ heißt automatisch geprüft, nicht menschlich abgenommen; die Menschen-, DPI- und Readerabnahme ist für alle Versionen offen (I6).

### 8.1 Funktionsinventar

| Bereich | Funktion | Status | Beleg | Einschränkung, Prüfstand |
|---|---|---|---|---|
| Aufgaben | Arten Aufgabe, Langtext, Gruppe, Zwischenüberschrift; Unterpunkte rekursiv | Implementiert | [Code] `ITEM_KINDS`, `new_item` | Austauschformat-Rundlauf erhält Unterpunkte bis Ebene 12 (`max_depth`) |
| | Checklisten | Implementiert | [Code] `MAX_CHECKLIST_ENTRIES = 50`, 200 Zeichen | bewusst knapp; wiederkehrende Checklisten öffnen sich neu |
| | „Wartet auf“ (`blocked_by`) mit Kreisprüfung, Verknüpfungen (`links`) | Implementiert | [Code] `is_blocked`, `normalize_item_references` (≤ 50) | Tagesvorschlag überspringt blockierte Aufgaben [Code `day_proposal.propose`] |
| | Wichtigkeit 0–3, Farbe, Labels, Aufwand, gebuchte Zeit | Implementiert | [Code] `new_item` | Zeit als Summe je Aufgabe, nicht je Tag |
| | Gemeinsamer Inspektor, direkte Felder, Zeilenaktionen | Implementiert (3.38.0) | [Code][QA] | Menschen-/DPI-Abnahme offen |
| | Rückgängig | Implementiert | [Code] `MAX_UNDO_STEPS = 20`, `undo_last_change`, `PackedState` | Vollschnappschuss von Listen, Ordnern, Labels, Papierkorb |
| | Wiederholen nach Rückgängig für Aufgaben- und Strukturänderungen | Nicht vorhanden | [Code] kein Redo in `ListApp`; Wiederholen nur in `RichNoteEditor`, `PageEditor`, `DrawingEditor` | FP-01 |
| Organisation | Listenarten Aufgaben, Notiz, Seite, Galerie, Zeichnung; Ordner, Buch, Notizbuch | Implementiert | [Code] `LIST_KINDS`, `FOLDER_KINDS` | neue Arten nur mit neuer Formatnummer |
| | Labels, Archiv, Papierkorb, Eingang, vier Seitenleistenbereiche, schmale Seitenleiste | Implementiert | [Code][QA] | – |
| Planung | Heute und Demnächst (früher „Mein Tag“, „In Bearbeitung“; D14) | Implementiert | [Code] `today_view.py` | – |
| | Bearbeitungstag ≠ Fälligkeit, Kapazität je Wochentag, Zeitblöcke, eingebettete Woche/Monat | Implementiert | [Code] `planning.py`, `week_planning.py` | – |
| | Tagesvorschlag, Routinen, Fokus mit genau einmal gebuchter Zeit, Tagesbeginn/-abschluss | Implementiert | [Code] `day_proposal.py`, `routines.py`, `focus_timer.py` | – |
| | Tageshinweise, lokale ICS-Belegzeiten, Tag entlasten | Implementiert (3.39.0) | [Code] `daily_hints.py`, `ics_busy.py`, `day_relief.py`; [QA] Mac/Linux/Windows | Menschenabnahme offen |
| | Erinnerungen fest/relativ mit Zustellbeleg, Systemmitteilungen (Option) | Implementiert | [Code] `process_reminders` | nur bei laufender App (Produktgrenze) |
| | Wiederholungen | Teilweise | [Code] `repeat_rules.KINDS`: täglich, alle N Tage, Wochentage, wöchentlich, monatlich, jährlich; Start/Ende; Termin bzw. verpasste Termine überspringen | kein Intervall für Woche/Monat/Jahr, kein n-ter oder letzter Wochentag, nicht ab Erledigung, keine Pause → FP-02 |
| | Wiederholungen in der Schnelleingabe | Implementiert (3.39.1) | [Code][Test] A29 | Ankertag und Wochentage gehören zur Regel; nicht Abbildbares bleibt vollständig Text mit Hinweis (FP-00); n-ter Wochentag, Monats-/Jahresintervalle erst mit FP-02 |
| | Wiederholungen in ICS-Ausgabe und -Import | Implementiert (3.39.1) | [Code][Test] A28/A30 | Monatsende-Klemmform in der Ausgabe, Starttagprüfung im Import, Zeitzonen über mitgelieferte IANA-Daten (FP-00) |
| | ICS-Serienrechner `ics_recurrence.py` (Belegzeiten 3.39.0) | Implementiert, unabhängig gegengeprüft | [Code][Probe] 11.192 Regel-/Startkombinationen gegen eigenständige RFC-5545-Abtastung ohne Abweichung | Randfall UNTIL vor DTSTART: kein Termin (Auslegungsfrage) |
| Ansichten | Liste (fünf Anzeigestufen), Tabelle (Spaltenwahl je Liste, Sortieren), Gruppieren einschließlich Eisenhower | Implementiert | [Code] `group_columns`, `table_sort` | – |
| | Pinnwand frei/geordnet/Spaltenboard, Bereiche, Verbindungen, Präsentation, PDF, Tastaturwege | Implementiert | [Code] `ItemWorkspace` | – |
| | Seiten und Notizen als Pinnwandkarte | Nicht vorhanden | [Code] `ItemWorkspace.valid_pages` lässt nur Zeichnungen zu (ZF-100) | FP-04 |
| | Gespeicherte Filter mit Erklärung | Teilweise | [Code] `SavedFilters`, `filter_explain.py` | Bedingungen nur Liste, Quelle, Status, Wichtigkeit (genau), Labels (beliebig/alle), feste Fälligkeitsstufen, Text; kein Bearbeitungstag, Aufwand, „wartet auf“ oder Ausschluss; Ergebnis immer nach Fälligkeit, Darstellung nicht gespeichert → FP-03 |
| Wissen | Seiten mit Block-Editor, Bildern, Titelbild, Live-Listen, Aufgaben mit Original-ID; Notizen, Notizbuch, Galerie, Bücher | Implementiert | [Code] `PageEditor`, `NoteEditor`, `page_features.py` | Unterseiten, Spalten bewusst nicht |
| | Verweise und Rückverweise (Seiten, Listen, Aufgaben) | Implementiert | [Code] `object_references.py`, `task_references.py` | – |
| | Unverknüpfte Erwähnungen | Nicht vorhanden | [Code] keine Fundstelle | FP-05 |
| | Anhänge an Punkten, Listen und Galerien | Implementiert | [Code] `normalize_attachments` | Vorschauformate je System |
| Suche | Palette für Inhalte und Aktionen, markierte Fundstellen, erklärte Filter | Implementiert | [Code] `content_search.py`; [QA] 66,6 ms bei 10.000 Punkten | Rangfolge nach Titelrang |
| Statistik, Verlauf | Startseitenkachel mit Jahres-Heatmap, Wochenrückblick (geschätzt gegen gebucht für erledigte Aufgaben), Änderungsverlauf | Teilweise | [Code] `YearHeatmap`, `COMPLETION_HISTORY_DAYS = 371`, `week_review_data`, `MAX_HISTORY_ENTRIES = 15` | keine Zeitauswertung je Tag, Liste oder Label; Verlauf ohne Wiederherstellen (Produktgrenze) → WA-08 |
| Vorlagen | Katalog mit Platzhaltern und Vorschau; Liste oder Ordner als Vorlage speichern | Implementiert | [Code] `save_list_as_template`, `TEMPLATE_FORMAT_VERSION = 2` | keine wiederkehrenden Vorlagen → WA-14 |
| Austausch | CSV, Markdown, TXT, ICS, `.glidepage`, Druck/PDF je Liste/Ordner; KI-Austausch Stufe 1/2 | Implementiert | [Code] `export_list_as`, `export_folder_as`, `exchange_patch.py` | – |
| | Gesamtexport als offener Dateibaum; Pinnwand als offenes Format | Nicht vorhanden | [Code] keine Fundstelle | FP-07 |
| | Notion-Import mit Wiedererkennung; einzelne Seite aus Sicherung | Geplant (Paket 6 / 3.41.0) | [Dok] Übergabe §6: privat vorbereitet, keine Produktionsübernahme | – |
| Sicherung | atomares Schreiben, Vorsicherung je Format, Sicherungen bei Änderung, 14 Tagesstände, Teil-/Komplett-/App-Backup, Vergleich | Implementiert | [Code] `write_json_atomic`, `migrate_on_start`, `schema_backups.py`, `backup_diff.py` | Pinnwandlayout und Einstellungen nur im App-Backup [Dok 06] |
| Gestaltung | zehn Designs (`DESIGN_ORDER`: Pixel, Hell, Dunkel, Liquid Glass hell/dunkel, Minimal hell/dunkel, Dopamin, Kontrast hell/dunkel), automatisch hell/dunkel, Akzent, Verläufe, WCAG AA | Implementiert | [Code] `DESIGNS`, `contrast_ratio`; Rückfallwert ohne gültige Einstellung `DESIGN_DEFAULT = "glass_dark"` | – |
| Pixel | Zeichnungen 16–128 Zellen, Paletten, PNG/ICO/SVG, Pixelsymbol | Implementiert; Animation Geplant (Paket 5) | [Code] `drawing.py` | – |
| Verteilung, Zugang | eigenständige Pakete (Paket 7), Screenreader-Kernablauf (Paket 8) | Geplant | [Dok] Plan §15.7 | – |
| Bekannte Befunde | W01 Seitenleistentitel unter Windows angeschnitten | Unklar | [Dok] eine Aufnahme vom 05.10.2026, Sichtprüfung offen | – |
| | W07/W08 Windows-Dialogdarstellung | Unklar | [Dok] auf dem Mac nicht nachstellbar | – |
| | W09 einmaliger Absturz von Python 3.14.8 unter Windows | Unklar | [Dok] 0 von 30 Wiederholungen | beobachten |
| | B7 Rahmen einer ausgeblendeten Leinwand wird unter Tk 9 wieder eingeblendet | Fehlerhaft (Tk), in Glide umgangen | [Dok] Architektur §5 | Meldung an Tcl/Tk offen |

**Ergebnis der Verifikation:** Kein Datenintegritätsrisiko für den gespeicherten Bestand. Die erste Durchsicht vom 13.10.2026 fand keinen reproduzierbaren Fehler; die anschließende Vorprüfung für FP-02 belegte **zwei reproduzierbare Fehler** im Lieferstand: Teilerkennung von Wiederholungsangaben in der Schnelleingabe (A29) und abweichende Monats-/Jahresserien in ICS-Ausgabe und -Import (A28). Dazu zwei Dokumentabweichungen (A24, A25, behoben), eine technische Doppelung (A26), eine fehlende Vorwärtsverträglichkeit innerhalb der Einstellungen (A27) und die Funktionslücken oben. Der in 3.39.0 neue ICS-Serienrechner stimmt mit einer unabhängigen Referenz überein.

### 8.2 Technische Einschränkungen

| Befund [Code] | Wirkung | Konsequenz |
|---|---|---|
| `app.pyw` 59.534 Zeilen, davon `ListApp` Zeilen 13.376–58.987 (rund 45.600); 50 Begleitmodule einschließlich `glide_start.py`, mit `app.pyw` zusammen 68.966 Zeilen | Regressionsrisiko R1/R14 bei jeder Erweiterung | D17 fortsetzen; neue Logik der Vorschläge ausschließlich als Tk-freie Module; kein Großumbau (Kosten-Nutzen im Plan §16.6) |
| Rückgängig als Vollschnappschuss, 20 Schritte | Speicher wächst mit Bestand × Schritte; ein Wiederholen-Stapel verdoppelt schlimmstenfalls | FP-01 misst Speicher bei 10.000 Punkten vor der Lieferung |
| Ganzer Bestand wird je Änderung atomar geschrieben | gemessen unkritisch (Plan §10); D16 gilt | keine Änderung vorgeschlagen |
| Einstellungen ohne Formattor; Normalisierer verwerfen Unbekanntes innerhalb bekannter Strukturen, oberste Ebene bleibt erhalten (A27) | Erweiterungen innerhalb gespeicherter Filter oder der Pinnwand gingen in älteren Fassungen still verloren | WA-09 eine Version vor FP-04; FP-03 über eigenen Schlüssel auf oberster Ebene (Lehre aus 3.29/3.30, Übergabe §4) |
| Zwei Wiederholungsrechner (A26) | doppelte Regeln, unterschiedliche Fähigkeiten | FP-02 vereinheitlicht über `ics_recurrence.py` |
| Tk-Leinwand ohne Kantenglättung unter Windows/X11 | Formen und Kurven würden treppig | keine Formen-/Freihandwerkzeuge auf der Pinnwand |
| Screenreader erst mit eigener Tk-9.1-Laufzeit | Zugänglichkeit vor Paket 8 nicht belegbar | neue Vorschläge mit semantischen Tastaturwegen planen |

### 8.3 Gap-Analyse

- **Überzeugend gelöst** (nicht umbauen): Tagesführung mit Bearbeitungstag, Kapazität, Zeitblöcken und Belegzeiten – im untersuchten Open-Source-Feld ohne Gegenstück; Datensicherheit mit Vorsicherung, Altleserschutz, Bestandswächter und Sicherungsvergleich; Aufgaben im Wissen mit Original-ID und Live-Listen; Pinnwand mit echten Aufgaben und D02-Semantik; Befehlspalette mit stabilen Aktionskennungen; berechneter Kontrast in zehn Designs; Prüfkultur mit Gegenproben. **Differenzierung** gegenüber AFFiNE, AppFlowy und Obsidian liegt hier, nicht in Editor oder Datenbank.
- **Vorhanden, verbessern:** Wiederholungsregeln (FP-02), gespeicherte Filter (FP-03), Inhalte der Pinnwand (FP-04), Rückverweise (FP-05), Bedienung des KI-Austauschs (FP-06), Ausgabe (FP-07), Zeitauswertung (WA-08).
- **Fehlerhaft (P0 nach Auftragsdefinition):** Teilerkennung von Wiederholungsangaben (A29) und Monatsende-Serien im ICS-Austausch (A28), dazu Zeitzonen im Aufgabenimport (A30); ohne Formatwechsel in 3.39.1 behoben und geliefert (FP-00).
- **Fehlend mit hohem Nutzen:** Wiederholen nach Rückgängig (FP-01) – eine Systemkonvention nach P1, die jedes Vergleichsprodukt bietet.
- **Vereinfachung bestehender Abläufe** [Einschätzung]: KI-Austausch braucht heute eigene Anweisungen je Auftrag (FP-06 macht daraus eine Auswahl); Projektwand mit Wissen erfordert Wechsel zwischen Seite und Pinnwand (FP-04); Sonderrhythmen wie „jeden zweiten Dienstag“ werden mit mehreren Aufgaben nachgebildet (FP-02).
- **Redundant oder inkonsistent:** zwei Wiederholungsrechner (A26); drei Rückblickwege mit verschiedener Reichweite – Rückgängig (20 Schritte), Änderungsverlauf (15 Einträge, ohne Wiederherstellen), Sicherungsvergleich – sinnvoll getrennt, aber der Verlauf verweist nicht auf den Wiederherstellungsweg (Vorschlag in FP-01, Stufe 2); mehrere Filterwege (Listensuche mit Status, gespeicherte Filter, Pinnwand-Labelfilter, Gruppierung) – FP-03 vereinheitlicht nur die Auswertung gespeicherter Filter, die einfachen Wege bleiben; Pinnwandlayout reist nur im App-Backup, ein Komplettbackup stellt es nicht her [Dok 06] – in FP-07 sichtbar benennen.
- **Bewusst nicht erneut vorgelegt:** Unterseiten, Spalten, Graph, Datenbank-Baukasten und freie Felder, freie Klebezettel und Freihand, Sync und gleichzeitige Bearbeitung, eingebaute Cloud-KI und MCP, Spracherfassung, systemweiter Hotkey, Gewohnheiten, Mobile (Produktgrenzen, Plan §7). Die Recherche liefert keinen Beleg, der eine dieser Entscheidungen entkräftet; Logseq und Super Productivity bestätigen die Kosten von Speicherwechsel bzw. Sync.

### 8.4 Einordnung der Kandidaten

| Kandidat | In bestehendes Modul | Eigene Ansicht | Optionale Erweiterung | Architekturänderung | Besser nicht |
|---|---|---|---|---|---|
| FP-00 Fehlerbehebung Wiederholungen | ✓ Schnelleingabe, ICS-Ausgabe/-Import | – | – | – | – |
| FP-01 Wiederholen | ✓ Rückgängig-Weg, Menü, Palette | – | – | – | – |
| FP-02 Wiederholungsregeln | ✓ Wiederholung, Schnelleingabe, ICS-Ausgabe | – | – | Formattor | – |
| FP-03 Gespeicherte Ansichten | ✓ gespeicherte Filter, `filter_explain` | – | – | eigener Einstellungsschlüssel auf oberster Ebene (ohne WA-09) | – |
| FP-04 Seitenkarten | ✓ Pinnwand | – | – | WA-09 | – |
| FP-05 Unverknüpfte Erwähnungen | ✓ Rückverweise | – | – | – | – |
| FP-06 KI-Aufträge | ✓ Datei › KI-Austausch | – | ✓ | – | – |
| FP-07 Offene Ausgabe | ✓ Datei › Ausgabe | – | – | – | – |
| WA-08 Zeitauswertung | ✓ Wochenrückblick | – | – | Formattor (Zeiteinträge je Tag) | – |
| WA-10 Lokaler KI-Endpunkt | – | – | ✓ | neue Schnittstelle (Q3) | ohne Entscheidung |
| Block-Editor-Neubau, Whiteboard-Engine, Sync/CRDT, Toolkit-Wechsel | – | – | – | ✓ | ✓ |
