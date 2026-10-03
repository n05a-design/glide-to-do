# Glide – Richtung

Stand 03.10.2026 · Glide 3.33.6 · Aufgabenformat 20 · Wettbewerb recherchiert am 01.10.2026 · GitHub-Stand vom 03.10.2026

Das Richtungsdokument: wohin Glide geht, woran sich jede Entscheidung misst und was der Inhaber dazu gesagt und entschieden hat. Es führt zusammen, was bis 03.10.2026 in den Produktgrenzen und -prinzipien (`docs/01_PRODUCT_CONSTRAINTS.md`), im Entscheidungsregister (`docs/ARBEITSRICHTUNG.md`), in „Markt und Vorbilder“ und den Konkurrenzanalysen vom 01.10.2026 (Featurematrix, Konkurrenzübersicht mit persönlichen Vorlieben) stand; dazu die Wettbewerbsrecherche vom 25.09., das Konzept „Seiten wie Notion“ vom 26.09. und die Entscheidungsvorlage vom 01.10.2026. Die Vorfassungen trägt Git.

**Abgrenzung:** Was als Nächstes umgesetzt wird und mit welchem Stand, steht im [Entwicklungsplan](Glide_Entwicklungsplan.md); wie gearbeitet und abgenommen wird, in den [Arbeitsregeln](../01_Repository/Glide/AGENTS.md); wie sich Glide heute verhält, in den [Funktionen](../01_Repository/Glide/docs/20_FUNKTIONEN.md).

**Grundsatz:** Entschiedenes wird nicht erneut vorgelegt. Empfehlungen in diesem Dokument sind als solche gekennzeichnet und ersetzen keine Entscheidung des Inhabers; jeder Umsetzungsschnitt außerhalb der beauftragten Performance-Arbeit braucht einen ausdrücklichen Auftrag.

## 1. Auf einen Blick

- **Leitsatz:** *Glide ist der ruhige, lokale Arbeitsplatz für den eigenen Tag – planen, erledigen, festhalten; alles in einer eigenen Datei, ohne Konto. Die Pixel-Werkstatt ist die persönliche Signatur.*
- **Vorbild:** Notion für Schreiben und Ordnen („Die App gefällt mir sehr gut“), Trello/Planner/FigJam/OneNote für die Pinnwand, Affinity für den Zeichenablauf – jeweils als Bedienprinzip, nicht als Funktionsumfang.
- **Abgrenzung im Wettbewerb:** nicht die Kombination aus Seiten, Aufgaben, Leinwand und lokalen Daten – die bieten AFFiNE und AppFlowy inzwischen quelloffen –, sondern die **Tagesführung** (Bearbeitungstag ≠ Fälligkeit, Kapazität, Zeitblöcke, Heute/Demnächst, Tagesbeginn und -abschluss, Zeiterfassung) und die **Pixel-Werkstatt** als Alleinstellung.
- **Maßstab für jede Funktion:** sechs Produktprinzipien – selbstverständlich wie bei Apple, Form folgt Funktion, nichts doppelt, kein Platz verschwendet, nur das Wesentliche, geringe Komplexität trotz vieler Funktionen.
- **Reihenfolge:** Fundament (Performance, beauftragt) → klarer Alltag → Wissen im Kontext → Pixel → Austausch und Verteilung. Zuerst weniger sichtbare Oberfläche, dann neue Funktionen.
- **Technische Leitplanken:** JSON bleibt das Speicherformat (D16), neue Fachlogik als Tk-freies Modul (D17), keine neue Laufzeitabhängigkeit ohne Entscheidung, Paket mit eigenem Python und Tk 9 vor einer Veröffentlichung (D15).
- **Bewusst nicht:** Konten, Cloud, Team, Mobile, eingebaute KI, Erinnerungen bei geschlossener App, frei definierbare Datenbanken, Unterseiten.
- **Stand:** 3.33.6 geprüft und ausgeliefert, öffentlich auf GitHub, keine Releasefassung, keine Lizenz. Offen beim Inhaber: Auswahl A–H, D07, Inhaberangaben, Lizenz, Signatur, Markenprüfung ([Abschnitt 10](#10-offene-richtungsfragen)).

## 2. Leitbild

**Zielbild:** ein angenehmer persönlicher Arbeitsort, in dem Aufgaben, Seiten, Notizbücher, Pinnwände und Pixelbilder zusammenpassen. Notion prägt das Schreiben und Ordnen, Trello und Planner das Board, FigJam und OneNote die freie Fläche, Affinity und die Pixel-Editoren das Zeichnen. Glide bleibt dabei ein Planer mit fester, verständlicher Struktur (Ordner, Liste, Punkt) – kein Baukasten.

**Drei Säulen in dieser Rangfolge:**

1. **Verlässlich und schnell:** Daten sind sicher (atomares Speichern, Vorsicherungen, Rückgängig für alles), jede Aktion bleibt bei realistischen Beständen unter 100 ms.
2. **Klarer Alltag:** Heute, Demnächst, Listen, Seiten; Erfassen ohne Nachdenken; jede Aufgabe genau einmal sichtbar.
3. **Wissen im Kontext:** Aufgaben dort, wo man schreibt; Verweise; Wiederfinden über die Volltextsuche.

**Stufen** (Antwort des Inhabers vom 30.09.2026, bestätigt am 01.10.2026; Zielversionen sind Reservierungen, keine Termine; Stand je Aufgabe im [Entwicklungsplan](Glide_Entwicklungsplan.md#1-stufen)):

| Stufe | Inhalt |
|---|---|
| 0 Fundament | Performance, Speicherweg, CI |
| 1 Klarer Alltag (3.33.x) | Bereiche, Startseite, Eingabe, Eisenhower, Heute/Demnächst (erledigt); UX1 „Weniger Oberfläche“, Fokus, Aufgaben im Notiztext |
| 2 Wissen im Kontext (3.34.x) | ein Inspektor, Volltextsuche, Verweise (Datenformat 21), Live-Liste, Titelbild, eingebetteter Kalender |
| 3 Pixel (3.35.x) | Palettenbearbeitung, Symbolvorschau, Animation (D07) |
| 4 Austausch und Verteilung (3.36.x) | KI-Austausch über Dokumente, Import, Sicherungsvergleich, Paket mit eigenem Python (D15) |
| 5 Zukunft (4.x) | Screenreader über Tk 9.1, Seitenversionen; SQLite nur nach Neubewertung (D16) |

## 3. Gedanken und Vorgaben des Inhabers

Wortlaute stehen in Anführungszeichen; alles andere ist die dokumentierte Entscheidung oder ihre Zusammenfassung.

### 3.1 Was Glide sein soll

| Datum | Gedanke bzw. Vorgabe | Was daraus folgt |
|---|---|---|
| 18.09.2026 | Master-Auftrag für 3.23 (46 Punkte): Schwerpunkt nicht auf neuen Funktionen, sondern auf dem Zusammenhalt der vorhandenen | eine Designauswahl statt dreier Schalter, eine Tabellenkomponente, Austauschformat |
| 19.09.2026 | Leitsatz für 3.25: „form follows function“ – zurück zu den Kernfunktionen, minimalistischere Oberfläche | weniger Text, weniger Knöpfe, weniger Menüeinträge; wird Prinzip P2 |
| 25.09.2026 | Referenzen je Bereich: Notion für Startseite, Darstellung und Ordnerstruktur; Trello, OneNote, Figma/FigJam und Microsoft Planner für die Pinnwand; Affinity für Zeichnen und künstlerische Entfaltung. Glide soll die **Pixel-Design-Nische** besetzen | Affinity als Vorbild für Ablauf und Oberfläche, nicht für den Umfang; Aseprite, Pixelorama, Lospec als Nischenreferenzen |
| 26.09.2026 | „Ich will allgemein mehr werden wie Notion, die App gefällt mir sehr gut.“ | Seitenart „Seite“, gemeinsamer Editor, Bibliotheken; Notion als Schreib- und Ordnungsort, nicht als Datenbank-Baukasten |
| 26.–29.09.2026 | Seite und datierte Notiz bleiben getrennt; Seiten vor allem für KI-Berichte; keine Unterseiten; Felder, wenn sie kommen, Glide-weit | siehe [Abschnitt 5](#5-was-glide-ist-und-was-es-nicht-wird) |
| 30.09.2026 | keine Funktion nur für eine Plattform; keine plattformeigenen Abhängigkeiten (Q2) | kein systemweiter Erfassungs-Hotkey (G07) |
| 30.09.2026 | KI-Austausch über Dokumente statt Schnittstelle (Q3) | `.glideexchange`, Kontextpaket, Änderungsvorschläge mit Vorschau (G24); kein MCP-Server |
| 01.10.2026 | Sechs Produktprinzipien: „Apple-like“ – funktioniert selbstverständlich; „form follows function“; keine Funktion doppelt; kein Platz verschwenden; „nur das Wesentliche – klar und wirkungsvoll“; geringe Komplexität trotz vieler Funktionen | [Abschnitt 4](#4-produktprinzipien) |
| 01.10.2026 | Startseite: „‚Ruhig‘ mit 7 Kacheln inkl. Gismo“; Ansichten: „zwei Hauptansichten“; Eisenhower „als Gruppierung im Board“; Hinweise „nur bei Bedarf“; Eingabe mit „einheitlicher Bedeutung“ | D10–D14, umgesetzt in 3.33.2–3.33.6 außer D11 |

**Notion – was gefällt** (ausdrücklich belegt bzw. durch Entscheidungen belegt): endlos nach unten wachsende Seite, leichter Schreib- und Lesefluss, Seiten für KI-Berichte, integrierte Aufgaben, Formatleiste bei Markierung, Rechtsklick „Umwandeln in“, Aufklapp- und Hinweisblöcke, großer Seitentitel und Weißraum, Bibliotheken und Galerien, Favoriten und Zuletzt im Seitenkontext.

**Notion – bewusst anders:** Seite und datierte Notiz bleiben verschiedene Inhalte; keine Unterseiten; Aufgaben in Seiten und Notizen sind echte Glide-Aufgaben; Felder gelten Glide-weit, kein Feldsystem je Liste; keine Spalten; Desktop zuerst, Mobile zurückgestellt.

### 3.2 Wie gearbeitet wird

| Datum | Gedanke bzw. Vorgabe |
|---|---|
| fortlaufend | „Ich habe Performance Probleme mit Glide, hilf mir die Code-Basis zu optimieren, mit Variabeln für die gleichen Funktionen, Streamlinen und optimieren.“ – gleiche Werte nur bei gleicher Bedeutung bündeln, Aufwand messbar senken, Daten-, Undo- und Fokusverhalten erhalten |
| 30.09.2026 | Reihenfolge schnelle Gewinne → Planen → Wissen → Pixel → Austausch (Q1); Toolkit-Probe zurückgestellt (Q4) |
| 01.10.2026 | „Das Repository wird die maßgebliche Ablage“ (D09); „bestehendes JSON-Speichern beschleunigen“ (D16); „schrittweise in eigene Module je Funktion zerlegen“ (D17); „Paket mit eigenem Python und Tk 9“ (D15) |
| 01.10.2026, abends | Das Repository ist öffentlich – Rohprotokolle bleiben lokal, veröffentlichte Ergebnisse ohne Benutzerpfade |
| 02.10.2026 | keine Archivkopien mehr; Vorfassungen trägt Git |
| 03.10.2026 | „Ich möchte keine aufgeblasene Ordnerstruktur mehr“; „jetzt wird auch mal wieder gelöscht anstatt immer nur archiviert und _Z zu schreiben“; Archive auf die letzten sieben Versionen, Screenshots auf die letzten drei; Dokumente, die das Gleiche beschreiben, zusammenführen |

**Entscheidungsstil des Inhabers:** nummerierte Fragen mit Optionen, Vor- und Nachteilen und genau einer Empfehlung; Antwort in Kurzform („D09 B, D10 B …“); Lizenz- und Quellenfragen gleich mit Quelle vorlegen; Entschiedenes nicht erneut vorlegen; nur den beauftragten Schnitt umsetzen.

## 4. Produktprinzipien

Die sechs Prinzipien (Auftrag vom 01.10.2026) als prüfbare Regeln:

| Prinzip | Bedeutung für Glide | Prüffrage | Kriterium |
|---|---|---|---|
| **P1 Funktioniert selbstverständlich** („Apple-like“) | Die naheliegende Handlung führt zum erwarteten Ergebnis, ohne Hinweistext; Systemkonventionen gelten (Hell/Dunkel, Kürzel, Esc, Entf, Doppelklick). | Geht es ohne Hinweis? | Keine Funktion nur über einen Dauerhinweis erklärbar |
| **P2 Form folgt Funktion** | Farbe = Rolle, Größe = Wichtigkeit, Position = Zusammenhang. | Würde die Funktion ohne dieses Element schlechter verstanden? | Jede Farbe mit genau einer Bedeutung; keine Dekoration im Standard |
| **P3 Keine Funktion doppelt** | Jede Absicht hat einen primären Weg; Menü und Kürzel dürfen ihn spiegeln. | Gibt es eine zweite Oberfläche für dasselbe Ergebnis? | Je Absicht eine Bedienoberfläche |
| **P4 Kein Platz verschwenden** | Inhalt vor Bedienung; Bedienelemente erscheinen dort und dann, wo sie gebraucht werden. | Wie viel Fläche zeigt Inhalt? | Bedienfläche über dem Inhalt ≤ 15 % bei 1280 × 800 |
| **P5 Nur das Wesentliche** | Der Standard zeigt das für die Tagesarbeit Nötige, alles andere ist erreichbar. | Würde man das Element vermissen? | Startseite sieben Kacheln (D12); Kopfzeile ≤ 4 Symbolknöpfe |
| **P6 Geringe Komplexität** | Wenige stabile Grundbegriffe (Aufgabe, Liste, Seite, Notiz, Ordner, Heute); neue Funktionen erweitern bestehende Orte. | Braucht es einen neuen Begriff, eine neue Ansicht, ein neues Fenster? | Neue Seitenleisteneinträge und Ansichten nur mit Entscheidung |

**Hausregeln** (seit 26./29.09.2026):

- Keine Seitenleistenzeile ist ein zweiter Weg zu denselben Punkten; kein Symbol trägt zwei Bedeutungen (Bewegungspfeile ausgenommen); Knöpfe erscheinen, wo sie wirken; Bedienelemente ohne Wirkung werden ausgeblendet.
- Seitenleiste, Kopf und Inhalt springen nie; Kanten fluchten. Funktionen leben eingebettet in der Ansicht, nicht in Zusatzfenstern.
- Farben nach `BUTTON_ROLE_RULES`: Rot nur Löschen, Grün nur Bestätigen, festes Lila für Hinzufügen und Neu, Gelb für Hinweise, sonst neutral. Knöpfe nie von Hand einfärben.
- Mindestgröße 860 × 700 ohne Quetschen oder Anschneiden; jeder Text erreicht WCAG 2.2 AA in allen Designs.
- Hinweisblöcke in Seiten bleiben gestalterisch unverändert (D06); Hinweiszeilen der Ansichten werden einklappbar (D11).

**Was gut ist und bleiben soll:** Symbolfamilie aus einem Unicode-Block, berechneter Kontrast, Farbregeln nach Bedeutung, Rückgängig überall, Tagesnavigation, klappbare Seitenleistenbereiche, Leerzustände mit Gismo, Bibliothekskarten mit nächsten Aufgaben, Datensicherheit mit Vorsicherungen.

### Prinzipien-Check für neue Funktionen

Vor der Umsetzung im Entwicklungsplan aufnehmen und beantworten:

0. **Vorgeschichte:** schon entschieden, verworfen oder zurückgestellt? In diesem Dokument und im Entwicklungsplan prüfen; Entschiedenes nicht erneut vorlegen.
1. **Absicht** in einem Satz.
2. **Ort:** welcher bestehende Ort (Ansicht, Inspektor, Befehlspalette, Menü)? Wenn keiner: Begründung und Entscheidung.
3. **Doppelung:** gibt es schon einen Weg? Welcher entfällt?
4. **Sichtbarkeit:** was im Standard sichtbar, was bei Bedarf? Zusätzliche Dauerfläche in px bei 1280 × 800?
5. **Selbstverständlichkeit:** ohne Hinweistext? Welche Plattformkonvention?
6. **Farbe und Form:** Rolle aus `BUTTON_ROLE_RULES`, Symbol aus `ICONS`.
7. **Begriffe:** neue Wörter mit dem Glossar abgleichen (Aufgabe, Langtext, Zwischenüberschrift, Gruppe; „Punkt“ nur als Oberbegriff).
8. **Rücknahme:** ein Undo-Schritt; Wirkung vor dem Loslassen sichtbar (D02).
9. **Daten:** neues Feld oder Format? Datenformat-Tor, Altleser, Migration.
10. **Tempo:** Kosten je Aktion abhängig vom Bestand; Messung mit 1.000 und 10.000 Punkten.

## 5. Was Glide ist und was es nicht wird

**Glide ist:**

- eine deutschsprachige, lokale Desktop-Anwendung für Aufgaben, Listen, Notizen, Seiten, Notizbücher, Pinnwände, Galerien und Pixelzeichnungen;
- ohne Internet, Benutzerkonto oder Cloudservice nutzbar; kein automatischer Datentransfer, keine Telemetrie; nur ein angeklickter Link öffnet den Browser;
- Python 3.14 mit Tk 9 und Standardbibliothek; mitgeliefert nur tkinterdnd2 und privat registrierte Schriften (DejaVu Sans, Pixelify Sans unter SIL OFL 1.1). Eine neue Laufzeitabhängigkeit braucht eine dokumentierte Entscheidung;
- plattformunabhängig: macOS, Windows, Linux; keine Funktion nur für eine Plattform;
- mit Nutzerdaten außerhalb des Programmordners, auch in einem extern synchronisierten Ordner. Glide synchronisiert selbst nicht; die Belegungsdatei verhindert erkannte Fremdnutzung, kann aber zwei unsynchronisierte Cloudkopien nicht verriegeln – nacheinander arbeiten: schließen, synchronisieren, am anderen Gerät öffnen;
- mit Erinnerungen und Systemmitteilungen (Option, Vorgabe aus) nur bei laufender App; verpasste Hinweise erscheinen gesammelt.

**Glide wird nicht:**

| Thema | Grund |
|---|---|
| Konten, eigener Cloudservice, Mehrbenutzerbetrieb, Kommentare, Zuweisung, Teilen | Produktgrenze |
| Gleichzeitige Bearbeitung auf zwei Geräten, Konfliktzusammenführung (G23) | Produktgrenze |
| Zustellung bei beendetem Programm (N09), externe Kalender- oder Mailintegration | Produktgrenze; ICS-Import und -Ausgabe sind Dateien, keine Synchronisierung |
| Mobile Apps, Toolkit-Wechsel (G25) | zurückgestellt (D03, Q4) |
| Mehrsprachigkeit | Produktgrenze |
| Eingebaute Cloud-KI, Spracherfassung (N15), KI-Schnittstelle/MCP (N10) | Q3: Austausch über Dokumente |
| Systemweiter Erfassungs-Hotkey (G07/N14) | nur plattformeigen lösbar (Q2) |
| Einstieg für neue Nutzer, führender Begleiter, Touren (N06) | 25./27.09.2026 nicht gewählt; Rundgang und Showcase vorhanden |
| Eigene Felder je Liste, Datenbank-Baukasten, Formulare (ZF-200, N18) | 25.09.2026 nicht gewählt; Felder, wenn sie kommen, Glide-weit |
| Unterseiten, Spalten in Seiten, Verweisgraph (G12, G13) | 29./30.09.2026 entschieden |
| Allgemeine Umwandlung zwischen Liste, Notiz und Seite | D05 |
| Freie Klebezettel ohne Aufgabe, Freihand-Tinte auf der Pinnwand | zweiter Datenbestand; Zeichnung ist eine eigene Art und erscheint als Karte |
| Vektorpfade, Ebeneneffekte, generative Bildfunktionen | verwässert die Pixel-Nische |
| Bilder aus dem Netz (etwa Titelbilder aus Bilddiensten), Web Clipper (N20) | automatischer Netzzugriff bzw. neue Plattform |
| Echte Transparenz oder Unschärfe je Widget | Tk kann das nicht; Milchglas ist eine Tönung |
| Bildbibliothek (etwa Pillow), allgemeines Textverarbeitungsprogramm | Abhängigkeit bzw. nicht Ziel |
| Gewohnheiten (G06), verschlüsselte Ablage (G22) | vorerst nicht; zuerst Fokus (G05) |

Grenzen einzelner Funktionen (Zeichnung, Seiten, Vorschauen, ICS, CSV, Druck): [Funktionen, Abschnitt 13](../01_Repository/Glide/docs/20_FUNKTIONEN.md#13-grenzen). Die Kennungen `de.shaye.glide` und `Shaye.Glide` ändern sich nie.

## 6. Entscheidungen

Verbindliches Register. Neue Entscheidungen werden hier als D18 ff. eingetragen, mit Datum und Wortlaut der Antwort.

| Nr. | Entscheidung | Stand |
|---|---|---|
| D01 | Allgemeine Datumsangaben setzen den Bearbeitungstag; ausdrücklich „fällig/bis“ setzt die Fälligkeit. Erkannte Felder sind vor dem Speichern sichtbar und rücknehmbar. | umgesetzt 3.33.3 |
| D02 | Eine Aktion bewirkt die im sichtbaren Zielkontext erwartbare Änderung: Ziehen auf einen Bearbeitungstag setzt `planned_date`, auf einen Zeitblock zusätzlich `planned_time`, auf einen ausdrücklichen Fälligkeitstermin `due`/`due_time`; neutrales Umordnen erhält Termine. Ziel und Feld sind vor dem Loslassen erkennbar, ein Undo-Schritt. Keine pauschale Erlaubnis, Fälligkeiten zu löschen. | gilt für jeden UI-Vertrag |
| D03 | Desktop/Tk optimieren; Mobile und Toolkit-Probe zurückgestellt. | gilt |
| D04 | Drag-and-drop erweitert die bestehenden Bereiche. | umgesetzt 3.32.2 |
| D05 | Einzelne Aufgaben in Notizen und Seiten mit erhaltener ID; Liste, Notiz und Seite bleiben eigenständige Arten, keine allgemeine Umwandlung. | G29/G31 offen |
| D06 | Die Gestaltung der Hinweisblöcke in Seiten bleibt unverändert. | gilt |
| D07 | Exportumfang der Animation: abspielbares GIF oder zunächst Frames/Vorschau/PNG-Spritesheet. | **offen**, erst zur Pixel-Etappe |
| D08 | Alle Klappmechanismen über echte Bedienbindungen prüfen, einschließlich Zustandserhalt, Tastatur und Tk-Callbackfehler. | umgesetzt 3.32.1, Pflichtsuite |
| D09 | Das GitHub-Repository `glide-to-do` ist die maßgebliche Ablage (Wurzel = Projektordner, Quellbaum `01_Repository/Glide`); Uploads nur in diese Struktur. Öffentlich: Rohprotokolle (`*.log`) bleiben lokal, veröffentlichte Ergebnisse ohne Benutzerpfade. Keine Archivkopien; Archive und Nachweise nur der sieben neuesten Versionen, Fensterbilder nur der drei neuesten; Dokumente werden zusammengeführt und gelöscht statt archiviert (CI „Datenschutz“, „Ablagegröße“). Sicherheitsmeldungen über GitHub, Dependabot; CodeQL-Workflow vom Inhaber deaktiviert. Zwischenstände als Git-Tags. | gilt; CI-Grundstufe seit 01.10.2026; noch kein Tag gesetzt |
| D10 | Ein Datum ohne Zusatz setzt den Bearbeitungstag, auch `/morgen`; die Fälligkeit nur mit „fällig“/„bis“, `/bis`, `/fällig`. Eine Wiederholung in der Eingabe setzt die Fälligkeit auf ihren ersten Termin (Ergänzung 02.10.2026). | umgesetzt 3.33.3/3.33.4 |
| D11 | D06 gilt nur für Hinweisblöcke in Seiten; Hinweiszeilen der Ansichten werden über „?“ ein-/ausgeklappt, Zustand gespeichert (U02). | offen (UX1) |
| D12 | Startseite „Ruhig“ mit sieben Kacheln: Heute (zusammengeführt), Gismo, Woche, Zuletzt bearbeitet, Angeheftet, Zeichnungen, Pinnwand-Vorschau; eigene Auswahl bleibt. | umgesetzt 3.33.2 |
| D13 | Eisenhower als Gruppierung „Dringlichkeit × Wichtigkeit“ im vorhandenen Board; Ziehen ändert Wichtigkeit bzw. Bearbeitungstag, Fälligkeiten werden nie gelöscht. | umgesetzt 3.33.5 |
| D14 | Zwei Hauptansichten: Heute (Tag, Verspätet, Heute fällig, nächste Aufgabe) und Demnächst; Tagesbeginn/-abschluss sind Modi von Heute; interne Kennungen bleiben. | umgesetzt 3.33.6 |
| D15 | Verteilung als Paket mit eingebettetem Python und Tk 9 je Plattform (G26/H-03), nach Stufe 1; das Bauwerkzeug ist eine eigene Abhängigkeitsentscheidung. | offen (Stufe 4) |
| D16 | JSON bleibt Speicherformat; der Speicherweg wird beschleunigt (T2, P08, P09). SQLite nur als Suchindex-Cache (G14); Neubewertung erst über 20.000 Punkten. | gilt |
| D17 | Kein Großumbau: jede neue oder angefasste Fachlogik als Tk-freies Modul mit Unit-Tests; `ListApp` ruft sie auf (G27 schrittweise). | gilt, sieben Module seit 3.33.0 |

**Frühere Antworten, die weiter gelten:**

| Herkunft | Inhalt |
|---|---|
| 25.09.2026 (E-01–E-16) | Format 20 als ein Paket; Suche `Strg/Cmd+O` (`Strg/Cmd+K` bleibt Kalender); Detailbereich zuschaltbar statt Maske ersetzen; eigenes Design „Pixel“; Rückgängig je Aktion; Zwischenstände als Anhänge; Größen 16/32/64/128; nur eigene Palette mitgeliefert; Pixelsymbol als eigene 16 × 16-Zeichnung; Spaltenboard zeigt alle Punkte; `Strg/Cmd+Enter` auf der Pinnwand legt eine Karte nur mit Titel an. Nicht gewählt: Einstieg für neue Nutzer, eigene Felder je Liste |
| 26.09.2026 | Seite und Notiz bleiben getrennt; Seiten vor allem für KI-Berichte; Ordnerarten Ordner, Buch, Notizbuch; Kennungen `de.shaye.glide`/`Shaye.Glide`; Milchglas als Tönung je Kachel |
| 27.09.2026 (E-01–E-13) | Python 3.14 mit Tk 9 als Grundlage; Systemmitteilungen als Option, Vorgabe aus; Vorschauen mit Tk-9-Mitteln ohne Bildbibliothek; Ziehen aus Finder/Explorer über tkinterdnd2; sofort speichern statt verzögert bündeln; keine Schnellerfassung für Seiten; Direktvertrieb zuerst (Windows x64, macOS arm64); kein Ordnerpfad über dem Titel; Titel höchstens 40 Zeichen |
| 28./29.09.2026 | Sicherungen nur bei Änderung plus Tagesstände; unbekannte Listenart öffnet schreibgeschützt, neue Arten nur mit neuer Formatnummer; Umstellung gleich beim Start; Bytecode im Systemcache; keine Unterseiten; Farben: festes Lila für Hinzufügen, Wiederherstellen grün, Importieren neutral, Nachzeichnen lila |
| 30.09.2026 (Q1–Q5) | Reihenfolge schnelle Gewinne → Planen → Wissen → Pixel → Austausch (Q1); keine plattformeigenen Abhängigkeiten, daher kein G07 (Q2); KI-Austausch über Dokumente statt Schnittstelle (Q3); Toolkit-Probe zurückgestellt (Q4, D03); Aufgabenzeilen im Notiztext, die Liste darüber zeigt genau diese Punkte (Q5); verschlüsselte Ablage keine Priorität |
| 01.10.2026 | Notizbücher nehmen im Bereich Notizen datierte Zeichnungen auf; Dokumentationskopien nach Wissensabgleich löschen statt archivieren; Repository öffentlich, Rohprotokolle lokal |
| 02.10.2026 | Wiederholung in der Eingabe setzt die Fälligkeit (D10); keine Archivkopien von Fixtures und Showcase |
| 03.10.2026 | Archive auf die sieben neuesten Versionen, Fensterbilder auf die drei neuesten; Dokumente gleichen Inhalts zusammenführen, ungenutzte Ordner auflösen; löschen statt archivieren und `_Z` |

## 7. Markt und Wettbewerb

**Verlässlichkeit:** Glides Werte stammen aus dem Code (Stand 3.33.6). Die übrigen beruhen auf Herstellerangaben und Berichten, abgerufen am 01.10.2026 (Wettbewerbsrecherche 25.09.2026, ältere Analysen 16.–23.09.2026), nicht auf Praxistests. Vorteile, Nachteile und Übertragbarkeit sind Einschätzungen. Vor einer Entscheidung, die auf einem Wettbewerbswert beruht, die Herstellerseite erneut prüfen.

### 7.1 Ergebnis

1. **Funktionsbreite:** für ein Ein-Personen-Projekt außergewöhnlich. In der Tagesführung liegt Glide auf dem Niveau spezialisierter Planer; Pixel-Werkstatt und Pinnwand mit echten Aufgabenkarten bietet kein anderes untersuchtes Produkt.
2. **Direkteste Vergleiche:** AFFiNE und AppFlowy decken „Seiten + Datenbanken + Leinwand + lokal“ quelloffen ab; Super Productivity ist der direkteste lokale Planer. „Lokal ohne Konto“ allein ist deshalb kein Alleinstellungsmerkmal mehr.
3. **Größte Lücken:** Volltextsuche im Inhalt (G14), Verweise zwischen Seiten (G08/G30), Aufgaben im Notiztext (G29), Fokusansicht (G05), Erscheinungsbild „wie System“ (N01). Seit 3.33.3–3.33.6 geschlossen: natürliche Eingabe mit sichtbarer Erkennung, Eisenhower, Heute-Ansicht ohne Dubletten.
4. **Stand der Technik 2026 ist KI** (Todoist Ramble und MCP, Notion Custom Agents, Apple Intelligence). Glides Antwort ist entschieden: Austausch über Dokumente (Q3, G24) – mit jedem Sprachmodell und ohne Netz nutzbar.
5. **Bedienkomfort und Informationsarchitektur** liegen hinter den Vorbildern: nicht zu wenig Funktion, sondern zu viel dauerhaft sichtbar (UX1).

### 7.2 Vorbilder des Inhabers

Belegstufen: **ausdrücklich belegt** (persönliche Aussage oder Entscheidung dokumentiert) · **als Vorbild benannt** (für einen Bereich vorgegeben, Einzelmerkmale aus der Recherche) · **Recherchebezug** (betrachtet, keine persönliche Vorliebe belegt).

| Produkt | Belegstufe | Übernommene Merkmale | Bewusst anders |
|---|---|---|---|
| **Notion** | ausdrücklich belegt („Die App gefällt mir sehr gut“, 26.09.2026); Schreiben durch die Entscheidungen R4/R5 vom 29.09.2026 | Seite, Editor, Bibliotheken, Erscheinungsbild ([Abschnitt 3.1](#31-was-glide-sein-soll)) | kein Baukasten, keine Unterseiten, Seite ≠ Notiz |
| **Trello** | als Vorbild benannt (Pinnwand) | Karten in Spalten, Cover und Farben, einklappbare Listen, derselbe Inhalt in mehreren Kontexten | – |
| **OneNote** | als Vorbild benannt (Pinnwand) | freie Anordnung, Notizbuchcharakter, große Fläche, Linien/Karo | keine Handschrift |
| **FigJam** (Figma als Whiteboard) | als Vorbild benannt (Pinnwand) | Klebezettel, beschriftete Verbinder, benannte Bereiche, Auswahl aufräumen, schnell den nächsten Zettel | keine Zettel ohne Aufgabe |
| **Microsoft Planner** | als Vorbild benannt (Aufgaben auf der Pinnwand) | Gruppieren nach Status, Termin oder Label; Ziehen ändert die passende Eigenschaft (D02); Checkliste, Beschreibung, Bild auf der Karte | – |
| **Affinity** | als Vorbild benannt (Zeichnen) | kontextbezogene Werkzeuge, direkte Farbauswahl und Paletten, Vorschau, Zwischenstände, Exportablauf | kein Vektor- oder Layoutumfang; Pixel-Nische ist eigene Vorgabe |

Für Todoist, TickTick, Things, Sunsama, Akiflow, Obsidian, Anytype, Capacities, Evernote, Miro, Aseprite, Pixelorama, Asana, ClickUp und monday.com gilt nur der Recherchebezug.

### 7.3 Vergleichsfeld

Je Produkt: wofür es steht, wo seine Grenze liegt und welcher Impuls für Glide daraus folgt.

**Aufgaben und Tagesplanung**

| Produkt | Stärke | Grenze | Impuls für Glide |
|---|---|---|---|
| [Todoist](https://www.todoist.com/features) | Natürliche Schnelleingabe, Datum und Deadline getrennt, Liste/Board/Kalender; 2026 Ramble (Sprache → Aufgaben) und MCP-Server | Konto und Cloud; Kalenderlayout, Dauer und Deadlines teils nur in Bezahltarifen | Erfassung mit sichtbarer Erkennung – seit 3.33.3 umgesetzt |
| [Things 3](https://culturedcode.com/things/support/articles/2803579/) | Ruhiger Ablauf Heute/Demnächst/Jederzeit/Irgendwann; Startdatum ≠ Deadline; 3.23/3.24 Feinschliff an Wiederholungen und Schlummern | nur Apple-Geräte, getrennte Käufe | Feinschliff statt Fülle – das Apple-Prinzip; Vorbild für D14 |
| [TickTick](https://ticktick.com/features) | Aufgaben, Kalender, Kanban, Gewohnheiten, Pomodoro, Eisenhower; 8.0 vorgeschlagene Tagesaufgaben, Jahres-Heatmap | dichte Oberfläche, vieles Premium | Fokus neben der Aufgabe (G05); bestätigt Tagesbeginn und Heatmap |
| [Super Productivity](https://super-productivity.com/) | lokal, ohne Konto, MIT; Fokus, Zeiterfassung, Timeboxing, Eisenhower, optionaler WebDAV-Sync | eher Arbeitszeit als Seiten und Bibliotheken | direktester lokaler Planer-Konkurrent; Fokus und Zeit gehören zusammen |
| [Sunsama](https://www.sunsama.com/) | geführte Tagesplanung, Zeitblöcke, Tagesabschluss, Wochenanalyse | Abonnement; lebt von gepflegter Routine | Maßstab für Tagesbeginn/-abschluss; Schätzung und echte Zeit nebeneinander |
| [Akiflow](https://akiflow.com/) | Universal Inbox, Time Blocking, automatische Planung | Abonnement, Integrationspflege | Zeit durch Ziehen sichtbar zuweisen; freie Zeitfenster vorschlagen (B-03) |
| [Microsoft To Do](https://www.microsoft.com/en-us/microsoft-365/microsoft-to-do-list-app) | „Mein Tag“ ohne Einrichtung verständlich | wenig Struktur, Konto | Tagesfokus, den man sofort versteht |
| [Apple Erinnerungen/Notizen](https://9to5mac.com/2026/06/12/heres-everything-new-for-reminders-in-ios-27/) | iOS/macOS 27: Erinnerung in eigenen Worten, Felder am Objekt, Notizen als Markdown | Apple-Plattform, Apple Intelligence | Felder am Objekt statt Dialog – stützt den Inspektor (N05/U12) |

**Seiten, Notizen und Wissen**

| Produkt | Stärke | Grenze | Impuls für Glide |
|---|---|---|---|
| [Notion](https://www.notion.com/help/writing-and-editing-basics) | Seiten und Blöcke, Slash-Menü, Datenbanken mit Ansichten, Galerie, Titelbild; Offline seit 2.53 (08/2025), 3.3 Custom Agents mit MCP | Datenbankpflege kostet Aufmerksamkeit; Richtung Team-Automation | zentrales Vorbild für Editor, Bibliotheken, Navigation, Aufgaben im Kontext |
| [AFFiNE](https://github.com/toeverything/affine) | Dokument und Leinwand sind dieselbe Seite, Kanban, lokal-first mit optionaler Cloud, KI | schwach in persönlicher Tagesplanung (Einschätzung) | stärkster Vergleich für Pinnwand + Seiten; Abgrenzung über die Tagesführung |
| [AppFlowy](https://github.com/AppFlowy-IO/AppFlowy) | Tabelle, Board, Kalender, Galerie; lokale KI über Ollama | große Laufzeitabhängigkeit für lokale KI | lokale KI ist machbar, widerspricht aber Glides Abhängigkeitsregel |
| [Obsidian](https://obsidian.md/) | lokale Markdown-Dateien, Rückverweise, Canvas; 1.10 Bases mit Gruppieren | Aufgabenplanung braucht Plugins und Eigenbau | stabile Verweise und Rückverweise (G08/G30); feste Glide-Felder bleiben richtig |
| [Logseq](https://discuss.logseq.com/t/whats-new-with-logseq-db-may-16th-2026/35020) | 2.0 Beta mit typisierten Eigenschaften | Wechsel von Dateien zu SQLite mit Datenverlustrisiko | Warnbeispiel; bestätigt D16 |
| [Capacities](https://capacities.io/), [Heptabase](https://wiki.heptabase.com/roadmap), [Anytype](https://github.com/anyproto/anytype-ts) | typisierte Objekte, Tagesnotizen, Karten auf Whiteboards mit „wo liegt diese Karte überall“, lokale verschlüsselte Objekte | Umgewöhnung an Objektmodelle; teils Cloud-Sync | Aufgaben im Wissenskontext sind Branchenstandard; Bibliotheken mit festen Eigenschaften |
| [OneNote](https://support.microsoft.com/en-us/onenote/take-and-format-notes) | Notizbücher, frei platzierte Inhalte, Tags | To-do-Tags ersetzen keine Planung | Notizbuchgefühl; Aufgaben bleiben echte Objekte |
| [Evernote](https://evernote.com/en-us/features/notes-app), [Joplin](https://joplinapp.org/), [Google Keep](https://support.google.com/keep/answer/6191044?hl=de) | Sammeln, Web Clipper und Suche (Evernote); lokal mit optionalem Sync (Joplin); geringe Schwelle (Keep) | Cloud und Tarife bzw. Einrichtungsaufwand bzw. wenig Struktur | Wiederfinden ist Kernnutzen (G14); Eingang sichtbar, bis eingeordnet (U07) |

**Boards, Pinnwände und Teamwerkzeuge**

| Produkt | Stärke | Grenze | Impuls für Glide |
|---|---|---|---|
| [Trello](https://trello.com/en/pricing) | anschaulicher Kartenfluss, Cover, Checklisten, Spiegelkarten | Konto; Ansichten je Tarif | einfaches Kanban, Karte bearbeiten mit Kontext |
| [Microsoft Planner](https://support.microsoft.com/en-us/planner/compare-microsoft-planner-basic-vs-premium-plans) | Gruppieren nach Status, Termin, Label; Premium mit Abhängigkeiten | Lizenzabhängig; 2026 entfallen Whiteboard-Reiter und iCal-Feed | nur noch Referenz für die Gruppierungslogik |
| [FigJam](https://help.figma.com/hc/en-us/articles/15300412458647-Explore-FigJam-files), [Miro](https://miro.com/features/) | Zettel, Verbinder, Bereiche, Aufräumen; Frames und Präsentation | Objekte sind keine Aufgaben; für eine persönliche Fläche überdimensioniert | benannte Bereiche, beschriftete Verbindungen, Präsentation aus Bereichen (vorhanden) |
| [Asana](https://asana.com/features/project-management), [ClickUp](https://clickup.com/features/views), [monday.com](https://monday.com/capabilities) | Verantwortung, Abhängigkeiten, viele Ansichten, Automationen | Team- und Prozesspflege, tarifabhängig | eine Aufgabe in mehreren Kontexten ohne Kopie; Blockaden sichtbar – Team bleibt außen vor |

**Zeichnen und Pixel**

| Produkt | Stärke | Grenze | Impuls für Glide |
|---|---|---|---|
| [Affinity](https://www.canva.com/newsroom/news/all-new-affinity/) | Vektor, Pixel und Layout in einer App, kontextbezogene Studios | viel größerer Umfang; Aktivierung über Canva-Konto | kontextbezogene Werkzeugleisten, erreichbare Farben, klarer Export |
| [Aseprite](https://www.aseprite.org/) | Pixel-Art, Ebenen, Animation, Zwiebelhaut, Spritesheet | spezialisiert, kein Organisationswerkzeug | Animation als eigener, begrenzter Arbeitsbereich (G17, D07) |
| [Pixelorama](https://orama-interactive.itch.io/pixelorama) | quelloffen; indizierte Farben, Paletten, Tilemaps, PNG/GIF/Spritesheet | Einarbeitung | Palettenverwaltung und Umfärben über indizierte Farben (G19) |
| [Lospec](https://lospec.com/palette-list) | Palettenverzeichnis | – | Paletten-Import (GPL/HEX, seit 3.32.0 auch Aseprite/ASE) |

**Laufzeit:** [Tcl/Tk 9.1.0](https://www.tcl-lang.org/software/tcltk/9.1.html) (29.09.2026) bringt eine Screenreader-Grundlage; der python.org-Installer für macOS liefert ab Python 3.14.5 Tk 9.0.3. Chance für Barrierefreiheit (N12) und gleiche Verteilung auf allen Plattformen (D15).

### 7.4 Entwicklung bis Oktober 2026

| Produkt | Entwicklung | Bedeutung für Glide |
|---|---|---|
| Notion | Offline-Modus seit 2.53 (08/2025); 3.2 KI-Notizen und Agenten mobil; 3.3 Custom Agents mit Zeitplänen und MCP ([2.53](https://www.notion.com/en-gb/releases/2025-08-19), [3.2](https://www.notion.com/de/releases/2026-01-20)) | „Notion kann nicht offline“ ist kein Unterscheidungsmerkmal mehr; Notion zielt auf Team-Automation |
| Todoist | Ramble: Sprache → Aufgaben mit Feldern; offizieller MCP-Server ([Ramble](https://www.todoist.com/help/articles/from-voice-to-tasks-ramble-july-1), [Changelog 2026](https://www.todoist.com/help/articles/2026-changelog)) | natürliche Erfassung ist Standard – Glide hat sie seit 3.33.3 |
| Things 3 | 3.23 (21.08.2026) frühes Erledigen von Wiederholungen; 3.24 Schlummer-Intervalle, Siri-Anbindung ([Release Notes](https://culturedcode.com/things/support/articles/1100684/)) | Feinschliff statt Funktionsfülle |
| TickTick | 8.0: vorgeschlagene Tagesaufgaben, Jahres-Heatmap ([AlternativeTo](https://alternativeto.net/news/2026/1/ticktick-8-0-adds-suggested-tasks-improved-yearly-monthly-views-and-customization-options/)) | bestätigt Tagesbeginn und Heatmap in Glide |
| Apple | iOS/macOS 27: Erinnerung in eigenen Worten, Felder am Objekt, Notizen als Markdown | Inspektor statt Maske (N05) |
| AFFiNE, AppFlowy | lokal-first mit Leinwand bzw. Datenbankansichten und lokaler KI | Abgrenzung über die Tagesführung |
| Obsidian | 1.10 Bases ([Changelog](https://obsidian.md/changelog/2025-10-01-desktop-v1.10.0/)) | feste Glide-Felder bleiben richtig |
| Logseq | 2.0 Beta: Dateien → SQLite mit Datenverlustrisiko | bestätigt D16 |
| Microsoft Planner | Update 2026 nimmt Whiteboard-Reiter und iCal-Feed heraus | Planner nur noch Gruppierungsreferenz |
| Tcl/Tk | 9.1.0 am 29.09.2026 | N12 nach D15 |

### 7.5 Featurematrix

● vorhanden · ◐ teilweise, eingeschränkt oder nur im Bezahltarif · ○ fehlt · P per Erweiterung · – nicht Zweck · ? nicht verifiziert
**Gl** Glide 3.33.6 · **No** Notion · **Td** Todoist · **Th** Things 3 · **TT** TickTick · **SP** Super Productivity · **AF** AFFiNE · **AP** AppFlowy · **Ob** Obsidian · **Ap** Apple Erinnerungen + Notizen

| Bereich | Funktion | Gl | No | Td | Th | TT | SP | AF | AP | Ob | Ap | Glide |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Erfassen | Natürliche Eingabe mit sichtbarer Erkennung | ● | ◐ | ● | ● | ● | ◐ | – | – | P | ● | seit 3.33.3, Wiederholungen seit 3.33.4 |
| | Systemweite Schnellerfassung | ○ | ● | ● | ● | ● | ◐ | ? | ? | ◐ | ● | bewusst nicht (G07) |
| | KI-/Spracherfassung | ○ | ● | ● | ◐ | ? | ○ | ◐ | ◐ | P | ● | bewusst nicht (Q3) |
| Planen | Bearbeitungstag getrennt von Fälligkeit | ● | ◐ | ● | ● | ◐ | ◐ | – | ◐ | P | ○ | D01 |
| | Heute-Ansicht ohne Dubletten | ● | ◐ | ● | ● | ● | ● | ◐ | ◐ | ◐ | ● | D14, seit 3.33.6 |
| | Kapazität, Aufwand, Zeitblöcke | ● | – | ◐ | ○ | ● | ● | ○ | ◐ | P | ◐ | Stundenraster |
| | Kalender Monat/Woche | ◐ | ● | ◐ | ◐ | ● | ◐ | ? | ● | P | ● | noch modales Fenster (N04) |
| | Tagesbeginn, Tagesabschluss, Wochenrückblick | ● | ○ | ◐ | ○ | ◐ | ● | ○ | ○ | P | ○ | Modi von Heute |
| | Wiederholungen | ● | ◐ | ● | ● | ● | ● | ○ | ? | P | ● | |
| | Erinnerung bei geschlossener App | ○ | ● | ● | ● | ● | ◐ | ○ | ◐ | P | ● | bewusst nicht (N09) |
| | Fokusansicht/Pomodoro | ◐ | ○ | ○ | ○ | ● | ● | ○ | ○ | P | ○ | Zeiterfassung ja, Fokus fehlt (G05) |
| | Zeiterfassung je Aufgabe | ● | ◐ | ○ | ○ | ◐ | ● | ○ | ○ | P | ○ | eine laufende Erfassung |
| | Eisenhower | ● | ◐ | ○ | ○ | ● | ● | ○ | ◐ | P | ○ | Gruppierung seit 3.33.5 |
| | Abhängigkeiten | ● | ● | ○ | ○ | ○ | ○ | ○ | ○ | P | ○ | „wartet auf“ mit Kreisprüfung |
| | Gewohnheiten | ○ | ◐ | ○ | ○ | ● | ◐ | ○ | ○ | P | ○ | vorerst nicht (G06) |
| Ordnen | Listen, Ordner, Labels, Archiv, Papierkorb | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | |
| | Gespeicherte Filter | ● | ● | ● | ◐ | ● | ◐ | ◐ | ● | ● | ● | |
| | Board/Kanban | ● | ● | ● | ○ | ● | ● | ● | ● | ◐ | ● | Pinnwand als Board |
| | Tabelle | ● | ● | ○ | ○ | ○ | ○ | ● | ● | ● | ○ | |
| | Galerie/Karten | ● | ● | ○ | ○ | ○ | ○ | ? | ● | ◐ | ○ | |
| | Vorlagen | ● | ● | ● | ◐ | ● | ◐ | ● | ● | ● | ◐ | mit selbstfüllenden Platzhaltern |
| | Unteraufgaben, Checklisten | ● | ● | ● | ● | ● | ● | ◐ | ◐ | P | ● | |
| Wissen | Block-Editor mit „/“-Menü, Bilder in Seiten | ● | ● | – | – | ◐ | ◐ | ● | ● | ◐ | ◐ | Linux-Bilder eingeschränkt |
| | Echte Aufgaben im Dokument | ◐ | ◐ | – | – | – | – | ◐ | ◐ | P | ◐ | in Seiten ja, in Notizen nein (G29) |
| | Verweise und Rückverweise | ◐ | ● | ○ | ○ | ○ | ○ | ● | ● | ● | ● | nur Punkt ↔ Punkt (G08/G30) |
| | Volltextsuche im Inhalt | ◐ | ● | ● | ● | ● | ● | ● | ● | ● | ● | nur Titel und Punkttexte (G14) |
| | Eigenschafts-/Datenbankansichten | ◐ | ● | – | – | – | – | ● | ● | ● | – | feste Glide-Felder (bewusst) |
| | Tagesnotiz, Notizbuch | ● | ◐ | – | – | ◐ | ◐ | ● | ? | ● | ○ | |
| | Seitensymbol, Titelbild | ◐ | ● | – | – | – | – | ● | ● | P | ○ | Pixelsymbol ja, Titelbild fehlt (G09) |
| | Markdown-Import/-Export | ● | ● | ◐ | ◐ | ◐ | ◐ | ● | ● | ● | ◐ | |
| Visuell | Freie Leinwand mit echten Aufgabenkarten | ● | ○ | ○ | ○ | ○ | ○ | ● | ○ | ● | ◐ | |
| | Pixel-Zeichnen und Symbol-Export | ● | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | **Alleinstellung** |
| | Animation | ○ | – | – | – | – | – | – | – | – | – | G17, D07 offen |
| Daten | Ohne Konto vollständig nutzbar | ● | ○ | ○ | ● | ○ | ● | ● | ◐ | ● | ◐ | |
| | Offene lokale Datei, automatische Sicherungen | ● | ○ | ○ | ◐ | ○ | ● | ◐ | ◐ | ● | ○ | eine lesbare JSON-Datei, Tagesstände |
| | Sync zwischen Geräten | ◐ | ● | ● | ● | ● | ● | ● | ● | ● | ● | Datenordner in Cloud-Ablage, ohne Zusammenführen |
| | Mobile Apps | ○ | ● | ● | ● | ● | ● | ● | ● | ● | ● | zurückgestellt (D03) |
| | Windows, macOS, Linux | ● | ◐ | ● | ○ | ● | ● | ● | ● | ● | ○ | Linux eingeschränkt (Tk 8.6, Bildformate) |
| | Import aus anderen Apps | ◐ | ● | ● | ◐ | ● | ◐ | ● | ● | ● | ○ | CSV/MD/ICS; Notion/Todoist fehlt (G21) |
| | Kalenderdatei (ICS) | ● | ◐ | ● | ◐ | ● | ◐ | ○ | ○ | P | ● | als Datei, kein Abo |
| | Eingebaute KI, Assistenten-Schnittstelle | ○ | ● | ● | ◐ | ? | ○ | ● | ● | P | ● | bewusst nicht; `.glideexchange` (Q3) |
| Bedienung | Eine Befehlspalette | ◐ | ● | ● | ◐ | ◐ | ◐ | ● | ◐ | ● | ○ | Suche und Aktionsdialog doppelt (U01) |
| | Erscheinungsbild wie System | ○ | ● | ● | ● | ● | ● | ● | ● | ● | ● | N01 |
| | Rückgängig auch für Strukturänderungen | ● | ● | ◐ | ● | ◐ | ◐ | ● | ● | ● | ● | 20 Schritte, Bestandswächter |
| | Beispielinhalt | ◐ | ● | ● | ● | ● | ◐ | ◐ | ◐ | ◐ | ◐ | Showcase und Rundgang; Einstieg bewusst nicht |
| | Screenreader | ○ | ? | ? | ● | ? | ? | ? | ? | ? | ● | N12 nach Tk 9.1 |

### 7.6 Vergleich nach Dimensionen

| Dimension | Maßstab | Glide 3.33.6 | Lücke | Konsequenz |
|---|---|---|---|---|
| Funktionen | Notion (Breite), TickTick (Planung + Fokus), AFFiNE (Seite + Leinwand) | sehr breit; in der Tagesplanung führend im Lokal-Segment | Volltext, Seitenverweise, Fokus, Aufgaben im Notiztext | keine neue Breite, sondern die Lücken im Kern schließen (Stufen 1–2) |
| Alltag | Things (Heute → Demnächst), Sunsama (Ritual) | Heute und Demnächst, Tagesbeginn/-abschluss als Modi (D14) | Fokus fehlt | G05 eingebettet in Heute |
| Komfort | Todoist (Erfassung), Apple (Felder am Objekt) | Feldchips seit 3.33.3, Undo überall | Detailbearbeitung doppelt (Maske + Bereich) | ein Inspektor (N05/U12) |
| Tempo | Things, Apple: jede Aktion unter 100 ms | Abhaken 56 / 218 / 446 ms bei 1.000 / 5.000 / 10.000 Punkten (Linux); Startseite 507 ms (Mac) | linearer Speicherweg, Aufbau | Stufe 0: P08, P09b, P03-Rest |
| Gestaltung | Things, Notion: viel Weißraum, wenige Bedienelemente | durchdacht im Detail, aber dicht: 8 Kopfsymbole, ≈ 27 % Bedienfläche, 5 Symbole mit Mehrfachbedeutung | zu viel dauerhaft sichtbar | UX1 vor neuen Funktionen |
| Hilfe | Things („Neu in …“), Notion | Handbuch, Kürzel, Showcase; Hinweise dauerhaft | Hilfe bei Bedarf, „Was ist neu“ | D11/U02, N07 |
| Marke | Things (eine starke Gestalt), Notion (Minimalismus) | Logo, Gismo, Design „Pixel“ | zehn Designs verwässern die Gestalt; Namenskollision „Glide“ | ein Signaturdesign mit Dunkelvariante vorn (N01), Gismo als Markenfigur, Markenprüfung (I4) |
| KI 2026 | Todoist Ramble/MCP, Notion Agents, Apple Intelligence | `.glideexchange` für externe KI | keine direkte Schnittstelle – bewusst | G24 Stufe 2: Kontextpaket und Änderungsvorschläge mit Vorschau |

### 7.7 Berichtigte ältere Bewertungen

Frühere Analysen (16.–18.09.2026) enthalten Aussagen, die nicht mehr gelten; sie dürfen nicht als aktuelle Entscheidung gelesen werden:

1. „Notion ist kein Ziel“ ist seit der Aussage vom 26.09.2026 überholt – Notions Seitenkonzept ist ausdrücklich gewünscht, nur nicht der Baukasten.
2. Bearbeitungstag getrennt von der Fälligkeit ist kein exklusives Glide-Merkmal (Things: Startdatum/Deadline; Todoist: Datum/Deadline).
3. Natürliche Eingabe ist bei Todoist nicht nur Pro; Things hat natürliche Datumseingabe in Termin- und Erinnerungsfeldern.
4. Notion hat einen begrenzten, gerätebezogenen Offlinemodus.
5. Mobile bedeutet nicht zwingend Konto und Server (Super Productivity, Joplin); Glides Desktop-Fokus ist eine Entscheidung (D03), keine technische Notwendigkeit.
6. Alte Ausschlüsse (Rich Text, Seiten, Rückverweise, Animation) sind durch spätere Entscheidungen ersetzt; es gilt dieses Dokument.

### 7.8 Positionierung und Marke

> **Glide ist der ruhige, lokale Arbeitsplatz für den eigenen Tag:** planen mit Bearbeitungstag, Fälligkeit und Kapazität; erledigen mit Zeit und Fokus; festhalten in Seiten, Notizbuch und Pinnwand; alles in einer eigenen Datei, ohne Konto. Die Pixel-Werkstatt ist die persönliche Signatur.

- **Stärken vertiefen:** Tagesführung (G05), Aufgaben im Kontext (G29, G31, G08/G30), Wiederfinden (G14), weniger dauerhaft sichtbare Bedienung (UX1).
- **Nische sichtbar machen:** Keine untersuchte Anwendung verbindet Organisation mit einem echten Pixelraster. Die Nische wird stärker, je sichtbarer Pixelbilder in der Organisation werden: Pixelsymbole an Listen und Ordnern, Kachel „Zeichnungen“, Galerie, Zeichnung als Pinnwandkarte, Titelbild als Pixelzeichnung (G09).
- **Nicht nachbauen:** Team, Cloud, frei definierbare Datenbanken, eingebaute Cloud-KI.
- **Marke:** Der Name „Glide“ kollidiert mit bekannten Produkten (etwa der No-Code-Plattform Glide); Markenprüfung durch einen Fachanwalt (I4). Stärkste Wiedererkennung: Gismo und das Pixel-Design.

## 8. Wegweisungen

Was aus Vorgaben, Entscheidungen und Wettbewerb für die nächsten Schritte folgt. Stand und Abnahme je Aufgabe stehen im [Entwicklungsplan](Glide_Entwicklungsplan.md).

1. **Erst das Fundament fertig:** Die beauftragte Performance-Arbeit (P04, P06r, P08a/b, P09b, Einstellungsfenster, Startseitenkacheln erhalten) geht vor neuen Funktionen. Ziel: Abhaken bei 5.000 Punkten ≤ 120 ms.
2. **Dann weniger Oberfläche, nicht mehr:** UX1 vor jeder neuen Ansicht – Kopfzeile ≤ 4 Symbolknöpfe, Bedienfläche ≤ 15 %, kein Symbol mit zwei Bedeutungen. Vorher stabile Aktionskennungen statt Menübeschriftungen (Risiko R2).
3. **Das Profil über die Tagesführung schärfen:** Fokus mit Timer eingebettet in Heute (G05) und Tastaturwege für alles, was sich ziehen lässt (H-02). Gewohnheiten erst danach.
4. **Aufgaben dorthin, wo geschrieben wird:** Aufgaben im Notiztext (G29), Seitenaufgabe in eine Liste schicken (G31), Filter „aus Seiten“ (G32). Vorher die Referenzregel festlegen: eine Aufgabe hat genau einen Heimatort, andere Orte zeigen Verweise.
5. **Wiederfinden vor weiterer Breite:** ein Inspektor, eine Befehlspalette mit Volltextsuche (SQLite FTS5 nur als ersetzbarer Cache), Verweise mit Datenformat-Tor 21.
6. **Pixel als Signatur, nicht als zweites Programm:** Palettenbearbeitung, Symbolvorschau, Animation erst nach D07; keine Vektoren, Ebeneneffekte oder generativen Funktionen.
7. **KI über Dokumente:** Kontextpaket und Änderungsvorschläge mit Feldvergleich und Vorschau (G24); keine Schnittstelle, keine eingebaute KI.
8. **Technik ohne Großumbau:** JSON beschleunigen (D16), Fachlogik als Tk-freies Modul (D17), Rückwärtsverhalten vor jedem Formatwechsel mit einer Kopie echter Daten messen, neue Arten nur mit neuer Formatnummer.
9. **Gleichwertig auf allen Plattformen:** Paket mit eigenem Python und Tk 9 (D15) macht Windows und Linux gleichwertig und ist Voraussetzung für Signatur und Screenreader (N12).
10. **Veröffentlichen erst mit Rechtsgrundlage:** Lizenz, Markenprüfung und Inhaberangaben vor jeder Bewerbung; Direktvertrieb zuerst, Stores später ([Abschnitt 9](#9-veröffentlichung-und-github)).
11. **Ablage schlank halten:** ein Thema, ein Dokument; sieben Versionen, drei Bildstände; löschen statt archivieren.

## 9. Veröffentlichung und GitHub

**GitHub heute** (abgerufen am 03.10.2026):

| Merkmal | Stand |
|---|---|
| Repository | [`n05a-design/glide-to-do`](https://github.com/n05a-design/glide-to-do), angelegt am 24.09.2026, öffentlich, Standardzweig `main`, maßgebliche Ablage (D09) |
| Beschreibung | englisch: „Glide is an offline desktop app for tasks, lists, notes, and journals, featuring daily planning, a calendar, pinboards, and local backups. No account or cloud service required. Built with Python and Tkinter.“ – nennt weder Seiten noch Pixel-Werkstatt; „journals“ heißt in Glide seit 27.09.2026 „Notizbuch“ |
| Releases, Tags | keine (D09 sieht Tags für Zwischenstände vor) |
| Lizenz | keine; `LICENSE.md` räumt ausdrücklich keine Nutzungs-, Änderungs- oder Weiterverteilungsrechte ein |
| Pull Requests | elf, alle gemergt (PR 1–11, 01.–03.10.2026) |
| Prüfungen | „Glide-Prüfung“ (CI-Grundstufe) grün; Dependabot aktiv; CodeQL-Workflow deaktiviert; KI-Codeprüfung „github-advanced-security“ scheitert am aufgebrauchten Monatskontingent |
| Funktionen | Issues (keine offen) und Wiki eingeschaltet, Discussions und Pages aus, keine Homepage |
| Größe | rund 530 MB, überwiegend Git-Historie; die Arbeitskopie hat seit 03.10.2026 rund 400 MB |

**Richtung der Veröffentlichung** (entschieden): zuerst Direktvertrieb über die eigene Website mit Developer-ID-Signatur und Notarisierung (macOS arm64, DMG) und signiertem Windows-Installer (x64); Stores später (27.09.2026). Davor: Paket mit eigenem Python und Tk 9 (D15), Lizenz (I2), Markenprüfung (I4), Inhaberangaben (I1), Zertifikate (I3), Windows-Abnahme (I6). Kanäle laut Auftrag: GitHub, eigene Website, Social Media, Product Hunt, itch.io, Heise Software-Verzeichnis, winget. Einzelheiten: [Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md).

**Empfehlungen für den GitHub-Auftritt** (nicht entschieden):

1. **Beschreibung aktualisieren**, etwa: „Calm, local desktop workspace for your day – tasks, pages, notebooks, pinboards and a pixel workshop. No account, no cloud, German UI. Python 3.14 + Tk 9.“
2. **Tags je ausgelieferter Version** ab `v3.33.6`, wie D09 es vorsieht; eine GitHub-Release erst mit signiertem Paket und Lizenz.
3. **Wiki ausschalten:** Die Dokumentation liegt im Repository; ein Wiki wäre ein zweiter Ort (P3).
4. **Issues** bis zur Lizenz ausschalten oder nur für Fehlermeldungen öffnen; Sicherheitsmeldungen laufen ohnehin vertraulich über *Security → Report a vulnerability*.
5. **KI-Codeprüfung** abschalten oder das Kontingent anpassen, damit kein dauerhaft roter Haken am PR steht.
6. **Git-Historie bereinigen** (eigener Auftrag): Sie enthält eine gelöschte Protokolldatei mit Benutzerpfaden und frühere Archivkopien; Umschreiben verkleinert das Repository deutlich, ändert aber alle Commit-Kennungen.

## 10. Offene Richtungsfragen

Nur der Inhaber entscheidet. Format: nummerierte Frage, Optionen, eine Empfehlung.

| Nr. | Frage | Optionen | Empfehlung | Wann |
|---|---|---|---|---|
| A–H | Richtung und Bearbeitungstiefe nach der Performance-Arbeit | je Richtung recherchieren, vorbereiten, kleinen Teil umsetzen, später oder nicht verfolgen (Übersicht unten) | Performance fertig (A), dann UX1, danach C-01 Aufgaben im Notiztext | nach Stufe 0 |
| D07 | Animationsexport | abspielbares GIF oder zunächst Frames/Vorschau/PNG-Spritesheet | Spritesheet zuerst | zur Pixel-Etappe |
| G21 | Erste Importquelle | Notion-Markdown/ZIP oder Todoist-CSV | Notion (Vorbild des Inhabers) | Stufe 4 |
| G26 | Bauwerkzeug für das Paket (D15) | z. B. PyInstaller ab 6.22, gepinnt | PyInstaller, eigene Abhängigkeitsentscheidung | Stufe 4 |
| I1 | Inhaberangaben (Copyright, Datenschutz-URL, Sicherheitskontakt, Inno-AppId) | Vorschläge bestätigen oder ändern | Vorschläge in der [Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md#inhaberangaben) bestätigen | vor dem ersten Release |
| I2 | Lizenz | Entwurf (private, nicht kommerzielle Nutzung kostenlos) veröffentlichen, ändern oder Open Source | Entwurf rechtlich prüfen und veröffentlichen, bevor das Repository beworben wird | vor jeder Bewerbung |
| I3 | Apple-Developer-Konto, Windows-Code-Signing-Zertifikat | – | erst mit D15 | Stufe 4 |
| I4 | Markenprüfung „Glide“ | Fachanwalt, ggf. Namenswechsel | vor Website, Store und Werbung | vor dem ersten Release |
| I5 | Python 3.14.7 auf dem Mac installieren | – | bei nächster Gelegenheit | jederzeit |
| I6 | Windows-Vollprüfung und manuelle Prüfsitzungen | [Prüfliste](Glide_Manuelle_Pruefung.md) | vor D15 | Stufe 4 |
| R1 | Rechte an Fremdbildern in `20_Grafik_Master/05_Inspiration` und `06_Beispielbilder`; sechs dieser Motive stecken auch im Showcase (`tests/fixtures/showcase/bilder`, Showcase-Backups in `05_Probelisten_Testdaten`) | behalten (mit Rechtenachweis) oder aus dem öffentlichen Repository entfernen und den Showcase mit eigenen Motiven neu erzeugen | ohne Nachweis entfernen | bald |
| R2 | Git-Historie umschreiben | belassen oder bereinigen (Force-Push, neu klonen) | bereinigen, solange es noch keine fremden Kopien gibt | bald |
| R3 | GitHub-Auftritt | Empfehlungen aus [Abschnitt 9](#9-veröffentlichung-und-github) | übernehmen | jederzeit |

**Die Auswahl A–H** (Stand 03.10.2026):

| Richtung | Erster Schnitt | Stand |
|---|---|---|
| A Tempo und Stabilität | P04 Bildlayout, P06r doppelte Aktualisierungen | beauftragt (Stufe 0) |
| B Planen und Fokus | Fokus mit Timer (G05), freie Zeitfenster vorschlagen (B-03) | Eingabe (B-01) umgesetzt 3.33.3; Rest offen |
| C Aufgaben im Text | Aufgaben im Notiztext (G29), Seitenaufgabe in Liste (G31), Filter „aus Seiten“ (G32) | offen; Referenzregeln zuerst |
| D Suchen und Wissen | Volltextsuche mit Fundstelle (G14), Verweise (G08/G30), Filter erklären (D-03) | offen |
| E Projektseiten | gefüllte Vorlage vor dem Anlegen prüfen (E-03), Live-Liste (G28), Titelbild (G09) | offen |
| F Austausch und Sicherungen | zwei Sicherungsstände vergleichen (F-03), KI-Austausch Stufe 2 (G24), Import (G21) | offen |
| G Pixel-Werkstatt | Paletteneintrag umfärben (G19), Symbolvorschau, Animation (D07) | offen |
| H Bedienkontrolle und Auslieferung | Kontrollmatrix echter Bedienwege (H-01), Tastaturwege (H-02), Paket (H-03 = D15) | H-01 laufend |

## 11. Pflege

- Neue Entscheidungen als D18 ff. in [Abschnitt 6](#6-entscheidungen) mit Datum und Wortlaut; neue Gedanken des Inhabers in [Abschnitt 3](#3-gedanken-und-vorgaben-des-inhabers) mit Datum und Beleg.
- Wettbewerbswerte vor jeder darauf gestützten Entscheidung an der Herstellerseite prüfen und Datum nachführen; Glides Spalte bei jeder Produktionsrunde.
- Aufgaben und ihr Stand gehören in den Entwicklungsplan, nicht hierher. Keine datierte Kopie; Git trägt die Vorfassung.
