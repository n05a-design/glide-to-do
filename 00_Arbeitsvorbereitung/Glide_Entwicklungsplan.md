# Glide – Entwicklungsplan und Aufgabenstand

Stand 03.10.2026 · Glide 3.33.6 · Aufgabenformat 20

Einziges Planungsdokument. Es führt zusammen, was bis 03.10.2026 auf zwölf Planungs-, Auswahl-, Recherche- und Entscheidungsdokumente verteilt war (Entwicklungsplan 3.33ff, Aufgabenauswahl A–H, Funktionsrecherche G01–G32, Arbeits- und Featureplanung P01–P07, Bestandsaufnahme AB/T, UX-Prüfung U01–U24, Übersicht vom 29.09.2026 und die älteren Kataloge). Die Vorfassungen trägt Git.

Leitbild, Prinzipien, Produktgrenzen, Entscheidungen, Wettbewerb und offene Richtungsfragen stehen in der [Richtung](Glide_Richtung.md). Dieser Plan ist eine Empfehlung: Jeder Umsetzungsschnitt braucht einen ausdrücklichen Auftrag, die offene Auswahl A–H und D07 entscheidet der Inhaber.

## Statusmarken

| Marke | Bedeutung |
|---|---|
| ✅ | erledigt, mit Version |
| ◐ | teilweise erledigt; der offene Rest steht dabei |
| ▶ | beauftragt, als Nächstes |
| ○ | offen, braucht Auftrag oder Entscheidung |
| ◇ | Zukunft, wartet auf einen Auslöser |
| ✕ | bewusst nicht (Produktgrenze oder Entscheidung) |

## 1. Stufen

Leitsatz, Säulen und Begründung der Reihenfolge: [Richtung, Abschnitt 2](Glide_Richtung.md#2-leitbild). Zielversionen sind Reservierungen, keine Termine.

| Stufe | Inhalt | Stand |
|---|---|---|
| 0 Fundament | Performance P03–P09, T2, CI | ◐ T2, P09a, Startseite-P03, CI-Grundstufe erledigt; P04, P06r, P08, P09b beauftragt |
| 1 Klarer Alltag (3.33.x) | Bereiche, Startseite, Eingabe, Eisenhower, Heute/Demnächst, UX1, Fokus, Aufgaben im Text | ◐ 3.33.1–3.33.6 erledigt; UX1, G05/H-02, G29/G31/G32 offen |
| 2 Wissen im Kontext (3.34.x) | Inspektor, Volltextsuche, Verweise (Format 21), Live-Liste, Titelbild, Kalender eingebettet | ○ |
| 3 Pixel (3.35.x) | Palettenbearbeitung, Symbolvorschau, Animation (D07) | ○ |
| 4 Austausch und Verteilung (3.36.x) | KI-Austausch Stufe 2, Import, Sicherungsvergleich, Paket mit eigenem Python (D15) | ○ |
| 5 Zukunft (4.x) | Screenreader (Tk 9.1), Seitenversionen, SQLite nur nach D16-Neubewertung | ◇ |

## 2. Erledigt seit 3.30

| Version | Inhalt |
|---|---|
| ✅ 3.30.0–3.31.0 | Modernisierung: Pinnwand-Board, Ordnertypen, Seiten und Galerie, Pixel-Werkstatt mit Größen 16–128, Format 20, Bilder in Seiten, Tk 9, Ziehen aus Finder/Explorer, Systemmitteilungen (Option), Logo, Sicherungen nur bei Änderung, Startprüfung, Notizbereich, gemeinsamer Editor für Notizen und Seiten, Inhaltsverzeichnis, Aufklapp- und Hinweisblöcke (F1/F2) |
| ✅ 3.32.0 | Etappe 1: G16 Symbol-Export (ICO), G20 Paletten aus Aseprite/Adobe, G11 Platzhalter, G03 Tagesabschluss; zwei Hänger behoben |
| ✅ 3.32.1 | D08 Klappkontrolle mit Pflichtsuite |
| ✅ 3.32.2 | D04 Ziehen in Seiten-/Notizbäumen; P02 Schriftcache, gebündelte Layouts, gemeinsamer Hover |
| ✅ 3.32.3 | A-01 Bibliothekskarten erhalten; Teil A-03 (Archiv-Zurückholen einmal); Showcase |
| ✅ 3.33.0 | T2 gemeinsame Formatsicherung, P09a Tabelle ohne Listenspaltenmessung |
| ✅ 3.33.1 | Vier Seitenleistenbereiche, Inhaltsgrenzen, neues Logo, Dialoge fertig positioniert einblenden |
| ✅ 3.33.2 | D12 Startseite „Ruhig“ mit sieben Kacheln, Rest P03 für die Startseite (764 → 507 ms) |
| ✅ 3.33.3 | G01 deutsche Schnelleingabe mit Feldchips, D10 |
| ✅ 3.33.4 | Wiederholungen in der Schnelleingabe (setzen die Fälligkeit) |
| ✅ 3.33.5 | G02 Eisenhower als Gruppierung (D13) |
| ✅ 3.33.6 | D14 „Heute“ und „Demnächst“ |
| ✅ 01.–03.10.2026 | D09 Repository als Ablage, CI-Grundstufe, Ablagegröße, Bereinigung der Ablage und Dokumentation |

## 3. Performance (Stufe 0, beauftragt)

Fortlaufender Auftrag des Inhabers: „Ich habe Performance Probleme mit Glide, hilf mir die Code-Basis zu optimieren, mit Variabeln für die gleichen Funktionen, Streamlinen und optimieren.“ Gleiche Funktionen und Werte nur bei gleicher Bedeutung bündeln, Aufbau- und Schreibaufwand messbar senken, Daten-, Undo- und Fokusverhalten erhalten. Keine pauschale Ersetzung von Datenschlüsseln durch Variablen.

| ID | Arbeit | Stand |
|---|---|---|
| P01 | Messbasis: unprofilierte Serien mit 100/1.000/10.000 Punkten, Notiz, Bildseite | ◐ Serien seit 3.32.2; offen: Verlaufvarianten, Speicherentwicklung |
| P02 | Schriftcache je Tk-Interpreter | ✅ 3.32.2 |
| P03 | Aufbau und Layout | ◐ Bibliothekskarten ✅ 3.32.3, Startseite ✅ 3.33.2 (764 → 507 ms). Offen: unveränderte Startseitenkacheln erhalten statt neu bauen (Lebensdauer/Invalidierung wie A-01), Elemente geänderter Karten, sehr viele Karten |
| P04 = A-02 | Bildlayout nur bei geänderter Geometrie, Platzieren beim Scrollen | ▶ |
| P05 | Gemeinsame Helfer | ◐ Hover ✅ 3.32.2; gleiche UI-Texte nur bei gleicher Bedeutung zentralisieren |
| P06r = A-03 | Doppelte Refresh-/Schreibanforderungen je Aktion | ▶ Archiv-Zurückholen ✅ 3.32.3; 21 Kandidaten im Codeabgleich, keine bestätigten Fehler |
| P07 | Volltextsuche als ersetzbarer FTS5-Cache | ○ mit G14 (Stufe 2) |
| P08a | Ein Vergleichsdurchlauf für Verlauf, „zuletzt bearbeitet“, Aktivität (T1: ≈ 78 % von `save_items` bei 10.000 Punkten) | ▶ mit Differenztest alt/neu |
| P08b | Nur geänderte Listen vergleichen, Vollvergleich im Autosave | ▶ nach P08a und Messung |
| P09a | Tabelle misst keine Listenspalten | ✅ 3.33.0 |
| P09b | Kennzahlen einmal je Aktualisierung, Datum über Zwischenspeicher, Schriftobjekte und Zeilenhöhen je Schrift merken (W2–W5) | ▶ Die Messprobe der Analyse (`pruefaufrufe_probe.py` mit `_glide_laden.py`) liegt in Git unter `tests/qa-3.32.3/` (Stand 7f30baf); für die Baseline nach `scripts/pflege` übernehmen |
| T2 | Gemeinsame Formatsicherung | ✅ 3.33.0 |
| – | Einblendung des Einstellungsfensters (Median rund 2,1 s) | ▶ eigener Messpunkt |
| CI | CI-Grundstufe (Linux/Xvfb) | ✅ 01.10.2026; ○ Integrationssuiten unter Linux kalibrieren, damit sie verpflichtend in die CI können |

**Fertig, wenn:** Abhaken bei 5.000 Punkten ≤ 120 ms (Linux-Referenz, Python 3.14; heute 218 ms) und auf dem Referenz-Mac vergleichbar gemessen; erstes Speichern ohne Zusatz-Parse; Verlauf und „zuletzt bearbeitet“ identisch zum alten Verfahren; Vollprüfung grün; 07/Bundle per SHA-256 abgeglichen.

## 4. Klarer Alltag (Stufe 1)

### 4.1 UX1 „Weniger Oberfläche“ (○, braucht Auftrag, 5–7 AT)

Vorher stabile Aktionskennungen statt Menübeschriftungen (Risiko R2: die Befehlspalette ordnet Befehle über ihre Beschriftung; 3.33.5 hat das bestätigt). Empfohlene Reihenfolge: U07, U03, U24, U10, U19, U22, U13, U14, N01, U02, U05-Rest, U01, U16.

| ID | Befund (Prinzip) | Empfehlung | Stand |
|---|---|---|---|
| U01 | Kopfzeile mit acht Symbolknöpfen, zwei Suchen (P3, P5) | ⌕ und ⌘ zu einer Befehlspalette (`Strg/Cmd+K`/`+O`); Verlauf und Drucken ins Menü; Glocke nur bei Bedarf; Ziel ≤ 4 Symbolknöpfe | ○ |
| U02 | Dauerhafte Hinweiszeilen (P1, P4) | „?“ klappt Hinweise ein/aus, Zustand gemerkt (D11) | ○ |
| U03 | „Suche löschen“ auch bei leerer Suche | Löschkreuz nur bei Inhalt, `Esc` leert | ○ |
| U04 | „Erweitert“/„Hinzufügen“ als Textknöpfe | ◐ Feldchips ✅ 3.33.3; offen: „+“-Knopf, `Shift+Enter` für „Erweitert“ | ◐ |
| U05 | Startseite überladen | ✅ 3.33.2 (D12); offen: Gismo-Kachel kompakter (Pflegeknöpfe beim Überfahren) | ◐ |
| U06 | Überlappende Ansichten | ✅ 3.33.6 (D14) | ✅ |
| U07 | Eingang nicht in der Seitenleiste | Zeile „Eingang (n)“ nur solange er Einträge hat | ○ |
| U10 | Kopfzeile kürzt den Titel zugunsten der Kennzahlen | Titel hat Vorrang, Kennzahlen immer in der Unterzeile | ○ |
| U13 | Bibliothek mit doppelten Wegen | Kachelklick öffnet; Fußleiste „Neu ▾ · Importieren ▾ · Archiv (n) · Kartengröße“ | ○ |
| U14 | Menüeinträge am falschen Ort, drei Sicherungsbegriffe | Papierkorb leeren → Bearbeiten; Mitteilung testen → Einstellungen; Sicherung vereinheitlichen | ○ |
| U16 | Begriffe uneinheitlich (Punkt/Aufgabe/Eintrag, „Long-Task“) | Glossar: Aufgabe, Langtext, Zwischenüberschrift, Gruppe | ○ |
| U17/N01 | Kein „wie System“ | „Automatisch (hell/dunkel)“ als Standard, Signaturdesign vorn | ○ |
| U19 | Quellliste und Nummer vor jedem Titel in „Heute“ | Titel zuerst, Quelle gedämpft rechts | ○ |
| U22 | Bearbeitungstag in Listenzeilen unsichtbar | Symbol ◉ + Tag in der Datumsspalte | ○ |
| U24 | Symbole mit mehreren Bedeutungen (▲ ▼ ◷ ≡ ◐) | eigene Zeichen für Eingang, Verspätet, Zeiterfassung; Doppelungsregel in der Symbolprüfung | ○ |

**Fertig, wenn:** Kopfzeile ≤ 4 Symbolknöpfe; Bedienfläche über dem Inhalt ≤ 15 % bei 1280 × 800 (heute ≈ 27 %); kein Symbol mit zwei Bedeutungen (Bewegungspfeile ausgenommen).

### 4.2 Weitere Arbeiten der Stufe 1

| ID | Arbeit | Stand |
|---|---|---|
| G05 = B-02 | Fokus mit Timer an der vorhandenen Zeiterfassung, eingebettet in „Heute“; Zeit wird genau einmal gebucht, auch nach Pause, Wechsel, Neustart | ○ (2–4 AT mit H-02) |
| H-02 | Tastaturwege für alles, was sich ziehen lässt, mit sichtbarem Ziel und einem Undo-Schritt | ○ |
| G29 = C-01 | Einzelne Aufgaben im Notiztext mit derselben ID wie im Aufgabenbereich (D05, Q5) | ○ Referenz- und Löschregeln zuerst (Abschnitt 8) |
| G31 = C-02 | Seitenaufgabe über ID in eine Liste schicken, Verweis bleibt | ○ |
| G32 = C-03 | Filter „aus Seiten“ in vorhandenen Ansichten (Kopfzähler gibt es schon) | ○ |
| N07 = U21 | Einmalige Karte „Neu in …“ nach einem Update | ○ |
| N08 | JPEG-Vorschau unter Linux über ein Systemwerkzeug | ○ |
| U20 | Leerzustand ohne doppelten Anlegen-Knopf | ○ |
| DOK2 | Code-Kommentar AB06 („Benachrichtigungen … Nicht-Ziel“) nachführen; Mindestversion Python/Tk festlegen und beim Start prüfen (AB08) | ○ nächster Produktionsschnitt (AB03–AB05, AB07 ✅) |
| – | Kommentare in `tests/tools/pruefen.py` und `tests/tools/hintergrund/sitecustomize.py` versprechen noch Tastaturabschirmung | ○ nächster Werkzeugschnitt |

Reservierung 3.33.7: G29, G31, G32, N07, N08 (4–7 AT).

## 5. Wissen im Kontext (Stufe 2, 3.34.x)

| ID | Arbeit | Stand |
|---|---|---|
| N05 = U12 | Ein Inspektor statt Maske + Detailbereich | ○ |
| U18 | Seitentitel im Dokument, Platzhalter „Schreiben oder „/“ für Blöcke“ | ○ |
| U15 | Lila nur für Hinzufügen; aktiver Zustand neutral | ○ |
| U08 = E-03 | Vorlagen im Anlegen-Weg, gefüllte Vorschau vor dem Anlegen | ○ |
| G14 = D-01 | Volltextsuche (FTS5 als Cache) in der einen Befehlspalette; Datenöffnung ohne Index muss gehen | ○ |
| D-03 | Erklären, warum ein Filter einen Punkt zeigt oder ausblendet | ○ |
| G08/G30 = D-02 | Seiten-, Listen- und Aufgabenverweise mit Rückverweisen; **Datenformat-Tor 21** (Altleser nur lesend) | ○ |
| G28 = E-01 | Live-Liste in einer Seite (Originalaufgaben, keine Kopien) | ○ nach G08/G30 |
| G09 = E-02 | Titelbild für Seiten und Bibliothekskarten, auch als Pixelzeichnung | ○ |
| N04 = U11 + B-03 | Kalender als eingebettete Ansicht, Ziehen auf Tage (D02), freie Zeitfenster vorschlagen | ○ |
| U09 | Kompakte Pinnwandleiste | ○ |
| B4 | Bilder in Seiten: Überlappung verhindern, Bilder in Druck/PDF und Markdown | ○ |

**Fertig, wenn:** Suche findet Wörter in Seiten-, Notiz- und Beschreibungstext, fehlender Index wird neu aufgebaut; Umbenennen, Verschieben, Papierkorb und Import erhalten Verweise, „Ziel fehlt“ ist sichtbar; ältere Fassungen öffnen Format 21 nur lesend; Kalender ohne modales Fenster.

## 6. Pixel, Austausch, Verteilung (Stufen 3–4)

| ID | Arbeit | Stand |
|---|---|---|
| G19 = G-01 | Paletteneintrag ändern färbt die Zeichnung um, mit Undo (indizierter Kern vorhanden) | ○ |
| G-03 | Symbolvorschau in 16/32/48 px vor dem Export | ○ |
| G17 = G-02 | Animation: Frames, Dauer, Vorschau; **D07 offen** (abspielbares GIF oder zunächst Frames/Vorschau/Spritesheet; Empfehlung: zuerst Spritesheet) | ○ |
| G24 = F-01 | KI-Austausch Stufe 2 über Dokumente: Kontextpaket, Markdown/Felder, Änderungsvorschläge mit Feldvergleich (Q3) | ○ |
| G21 = F-02 | Begrenzter Import (zuerst eine Quelle: Notion-Markdown/ZIP oder Todoist-CSV – Inhaberentscheidung) mit Verlustbericht | ○ |
| F-03 | Zwei Sicherungsstände lesbar vergleichen, ohne Schreibzugriff | ○ |
| G26 = H-03 | Paket mit eingebettetem Python 3.14 + Tk 9 je Plattform (D15); Bauwerkzeug als eigene Abhängigkeitsentscheidung (Vorschlag PyInstaller ≥ 6.22) | ○ |
| – | Windows-/Linux-Abnahme, Linux-App (AppImage/Flatpak später) | ○ Inhaber |
| H-01 | Kontrollmatrix echter Bedienwege fortführen | laufend |

## 7. Zukunft und bewusst nicht

| ID | Thema | Marke | Grund / Auslöser |
|---|---|---|---|
| N12 = U23 | Screenreader über Tk 9.1 `tk accessible` | ◇ | Tk 9.1.0 ist erschienen (29.09.2026); Voraussetzung G26 und eigene Abnahme |
| N13 | Seitenversionen wiederherstellen | ◇ | nach F-03 |
| – | SQLite als Hauptspeicher | ◇ | nur bei realen Beständen über 20.000 Punkten (D16) |
| G25, Mobile | Toolkit-Probe, iPhone/iPad | ◇ | D03 aufheben |
| G18, G15, G10 | Kachelsatz, Filter in Alltagssprache, Registerkarten-Block | ◇ | Vorrat |
| G06 | Gewohnheiten | ◇ | vorerst nicht; zuerst G05 |
| B1 | Seitenleiste als Ganzes scrollen | ◇ | wenn die kleinen Bereiche im Alltag stören |
| B7 | Tk-Fehler (Rahmen einer ausgeblendeten Leinwand) an Tcl/Tk melden | ○ | braucht ein Konto bei core.tcl-lang.org |

**Bewusst nicht (✕):** N09, N10, N14 = G07, N06, G23, G22, G12, G13, ZF-200, N15–N20 – Gründe in der [Richtung, Abschnitt 5](Glide_Richtung.md#5-was-glide-ist-und-was-es-nicht-wird).

## 8. Abhängigkeiten und Regeln vor der Umsetzung

- **Referenz- und Löschregeln vor G29/G31/G28:** Eine Aufgabe hat genau einen Heimatort (Liste, Seite oder Notiz), andere Orte zeigen einen Verweis. Entfernt man eine Verweiszeile, entfällt nur der Verweis. Entfernt man die Zeile am Heimatort, wandert die Aufgabe in den Papierkorb; Verweise zeigen „im Papierkorb“ bzw. nach endgültigem Löschen „Ziel fehlt“. Undo stellt beides zusammen her.
- **Datenformat-Tor 21:** beim ersten inkompatiblen Inhalt (Verweise, Animation), mit Vorsicherung, Migration und schreibgeschütztem Altleser.
- UX1 vor G14 (eine Befehlspalette); P08a vor P08b; D07 vor G17; G24 vor G21; D15 vor G26 vor N12.

## 9. Risiken

| Nr. | Risiko | Gegenmaßnahme |
|---|---|---|
| R1 | Regressionen in der Klasse `ListApp` (rund 54.500 Zeilen in `app.pyw`) | kleine Schnitte, echte Bedienproben, Vollprüfung je Schnitt, Fachlogik als Tk-freies Modul (D17) |
| R2 | Menübeschriftungen sind Schlüssel für Aktionen; Umbenennen bricht Zuordnungen | stabile Aktionskennungen vor UX1; Test „jede Aktion erreichbar“ |
| R3 | Neue Dokumentinhalte gehen in älteren Fassungen verloren | Datenformat-Tor 21 |
| R4 | P08b übersieht einen Änderungsweg | Vollvergleich im Autosave, Differenztest |
| R5 | Windows/Linux ungeprüft | Linux-CI, Windows-Checkliste, D15 |
| R7 | Umfang wächst | Klassifizierung, Prinzipien-Check mit Vorgeschichte |
| R9 | Gewohnheitsbruch durch D10/D12/D14 | Bestandseinstellungen bleiben; N07 |
| R10 | Namenskollision „Glide“ | Markenprüfung durch den Inhaber |
| R11 | Linux-Messungen nicht auf den Mac übertragbar | Abnahme auf dem Referenz-Mac |

## 10. Messbare Ziele

| Bereich | Ziel | Stand (Beleg) |
|---|---|---|
| Abhaken 1.000 / 5.000 / 10.000 Punkte | ≤ 50 / 120 / 200 ms | 56 / 218 / 446 ms (Linux, Python 3.14, Median) |
| Erstes Speichern, 10 MB | ≤ Folgespeichern + 50 ms | ✅ ohne Zusatz-Parse seit 3.33.0 |
| Startseite aufbauen | ≤ 150 ms | 507 ms (macOS, 1.000 Punkte, 3.33.2) |
| Tabellenansicht öffnen, 5.000 Punkte | ≤ 400 ms | 2.671 → 292 ms in der Messung zu T8 (Linux); P09a seit 3.33.0, danach nicht erneut als Ganzes gemessen |
| Kopfzeilen-Symbolknöpfe | ≤ 4 | 8 |
| Bedienfläche über Inhalt (Liste, 1280 × 840) | ≤ 15 % | ≈ 27 % |
| Startseitenkacheln im Standard | 7 (D12) | ✅ 7 seit 3.33.2 |
| Symbole mit mehreren Bedeutungen | 0 (Bewegungspfeile ausgenommen) | 5 |

Verbindlich ist die Messung auf dem Referenz-Mac mit Aufwärmen, Median und p95; Linux-Werte gelten als Trend.

## 11. Nur durch den Inhaber

Auswahl A–H, D07, Importquelle (G21), Bauwerkzeug (G26), Inhaberangaben und Freigaben I1–I6 sowie die Rechte- und Repository-Fragen stehen mit Optionen und je einer Empfehlung in der [Richtung, Abschnitt 10](Glide_Richtung.md#10-offene-richtungsfragen).

## 12. Pflege

- Bei jeder Produktionsrunde Statusmarken, Abschnitt 2 und die Ziele nachführen. Keine datierte Kopie anlegen; Git trägt die Vorfassung.
- Neue Ideen erst nach dem [Prinzipien-Check](Glide_Richtung.md#prinzipien-check-für-neue-funktionen) und mit Marke aufnehmen.
- Neue Entscheidungen gehören in die [Richtung](Glide_Richtung.md#6-entscheidungen), nicht hierher.
