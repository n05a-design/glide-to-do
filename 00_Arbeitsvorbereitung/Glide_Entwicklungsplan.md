# Glide – Entwicklungsplan und Aufgabenstand

Stand 05.10.2026 · Glide 3.33.8 · Aufgabenformat 20

Einziges Planungsdokument. Es führt zusammen, was bis 03.10.2026 auf zwölf Planungs-, Auswahl-, Recherche- und Entscheidungsdokumente verteilt war (Entwicklungsplan 3.33ff, Aufgabenauswahl A–H, Funktionsrecherche G01–G32, Arbeits- und Featureplanung P01–P07, Bestandsaufnahme AB/T, UX-Prüfung U01–U24, Übersicht vom 29.09.2026 und die älteren Kataloge). Die Vorfassungen trägt Git.

Verbindliche Entscheidungen stehen in der [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md), Produktgrenzen und Prinzipien in den [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md). Der Auftrag vom 05.10.2026 umfasst gründliche Planung und den Beginn der Feature-Umsetzung. Die Reihenfolge unten konkretisiert diesen Auftrag; D07, Importquelle, Bauwerkzeug und Inhaberfreigaben bleiben eigene Entscheidungen.

## Statusmarken

| Marke | Bedeutung |
|---|---|
| ✅ | erledigt, mit Version |
| ◐ | teilweise erledigt; der offene Rest steht dabei |
| ▶ | beauftragt, als Nächstes |
| ○ | offen, braucht Auftrag oder Entscheidung |
| ◇ | Zukunft, wartet auf einen Auslöser |
| ✕ | bewusst nicht (Produktgrenze oder Entscheidung) |

## 1. Leitsatz und Reihenfolge

*Glide ist der ruhige, lokale Arbeitsplatz für den eigenen Tag – planen, erledigen, festhalten; alles in einer eigenen Datei, ohne Konto. Die Pixel-Werkstatt ist die persönliche Signatur.*

Drei Säulen in dieser Rangfolge: **verlässlich und schnell** (Daten sicher, Aktionen unter 100 ms bei realistischen Beständen) → **klarer Alltag** (Heute, Demnächst, Listen, Seiten; Erfassen ohne Nachdenken) → **Wissen im Kontext** (Aufgaben in Seiten und Notizen, Verweise, Suche).

Reihenfolge der Stufen (Antwort des Inhabers vom 30.09.2026, bestätigt am 01.10.2026): Fundament → Planen → Wissen → Pixel → Austausch und Verteilung. Zielversionen sind Reservierungen, keine Termine.

| Stufe | Inhalt | Stand |
|---|---|---|
| 0 Fundament | Performance P03–P09, T2, CI | ◐ T2, P09a, Startseite-P03, CI-Grundstufe erledigt; P04, P06r, P08, P09b beauftragt |
| 1 Klarer Alltag (3.33.x) | Bereiche, Startseite, Eingabe, Eisenhower, Heute/Demnächst, UX1, Fokus, Aufgaben im Text | ◐ 3.33.1–3.33.6 erledigt, G14-Suchbeginn 3.33.7; UX1, G05/H-02, G29/G31/G32 folgen |
| 2 Wissen im Kontext (3.34.x) | Inspektor, Volltextsuche, Verweise (Format 21), Live-Liste, Titelbild, Kalender eingebettet | ◐ G14 seit 3.33.7; Prüfung/Lieferung 3.33.8 im QA-Bericht; übriger Ausbau offen |
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
| ✅ 3.33.7/3.33.8 | G14-Inhaltssuche, Windows-Formatsicherung und Dateiinhaltsvergleich, Mindesthöhen/Titelbreiten, Editor-Timerabbau; Windows-Vollprüfung grün, Python-Lieferung 3.33.8 abgeglichen. Referenz-Mac/Bundle und menschliche Freigabe offen |
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
| P07 | Volltextsuche als ersetzbarer FTS5-Cache | ○ nach G14 erster Stufe und gemessener Latenz (Stufe 2) |
| P08a | Ein Vergleichsdurchlauf für Verlauf, „zuletzt bearbeitet“, Aktivität (T1: ≈ 78 % von `save_items` bei 10.000 Punkten) | ▶ mit Differenztest alt/neu |
| P08b | Nur geänderte Listen vergleichen, Vollvergleich im Autosave | ▶ nach P08a und Messung |
| P09a | Tabelle misst keine Listenspalten | ✅ 3.33.0 |
| P09b | Kennzahlen einmal je Aktualisierung, Datum über Zwischenspeicher, Schriftobjekte und Zeilenhöhen je Schrift merken (W2–W5) | ▶ Die Messprobe der Analyse (`pruefaufrufe_probe.py` mit `_glide_laden.py`) liegt in Git unter `tests/qa-3.32.3/` (Stand 7f30baf); für die Baseline nach `scripts/pflege` übernehmen |
| T2 | Gemeinsame Formatsicherung | ✅ 3.33.0; Windows-Signatur 3.33.7, Inhaltsvergleich gegen Metadatenkollisionen 3.33.8 |
| – | Einblendung des Einstellungsfensters (Median rund 2,1 s) | ▶ eigener Messpunkt |
| CI | CI-Grundstufe (Linux/Xvfb) | ✅ 01.10.2026; ○ Integrationssuiten unter Linux kalibrieren, damit sie verpflichtend in die CI können |

**Neue Windows-Messgrenze 3.33.8:** Der Formatcache muss bei identischen Metadaten den vollständigen Inhalt prüfen. SHA-256 einer warmen synthetischen Datei mit 10.000 Punkten: Median 1,5 ms, Maximum 5,6 ms in 21 Runden. Das ist kein gesamter Speichervorgang. Die P08a-Baseline muss diesen Leselauf sowie Verlauf, Aktivität und „zuletzt bearbeitet“ getrennt und insgesamt messen; bestehende Linux-Zahlen sind keine aktuelle Windows-Garantie. [Messung](../01_Repository/Glide/tests/qa-3.33.8/windows_2026-10-05/messung_dateipruefung.json).

**Fertig, wenn:** Abhaken bei 5.000 Punkten ≤ 120 ms (Linux-Referenz, Python 3.14; heute 218 ms) und auf dem Referenz-Mac vergleichbar gemessen; erstes Speichern ohne Zusatz-Parse; Verlauf und „zuletzt bearbeitet“ identisch zum alten Verfahren; Vollprüfung grün; 07/Bundle per SHA-256 abgeglichen.

## 4. Klarer Alltag (Stufe 1)

### 4.1 UX1 „Weniger Oberfläche“ (▶ Folgepaket im Auftrag 05.10.2026)

Vorher stabile Aktionskennungen statt Menübeschriftungen (Risiko R2: die Befehlspalette ordnet Befehle über ihre Beschriftung; 3.33.5 hat das bestätigt). Empfohlene Reihenfolge: U07, U03, U24, U10, U19, U22, U13, U14, N01, U02, U05-Rest, U01, U16.

| ID | Befund (Prinzip) | Empfehlung | Stand |
|---|---|---|---|
| U01 | Kopfzeile mit acht Symbolknöpfen, zwei Suchen (P3, P5) | ⌕ und ⌘ zu einer Befehlspalette (`Strg/Cmd+O`; `Strg/Cmd+K` bleibt Kalender); Verlauf und Drucken ins Menü; Glocke nur bei Bedarf; Ziel ≤ 4 Symbolknöpfe | ○ |
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

3.33.7 ist für den ersten G14-Schnitt verwendet. G29/G31/G32, N07 und N08 bleiben Folgepakete ohne fest zugesagte Zielversion.

## 5. Wissen im Kontext (Stufe 2, 3.34.x)

| ID | Arbeit | Stand |
|---|---|---|
| N05 = U12 | Ein Inspektor statt Maske + Detailbereich | ○ |
| U18 | Seitentitel im Dokument, Platzhalter „Schreiben oder „/“ für Blöcke“ | ○ |
| U15 | Lila nur für Hinzufügen; aktiver Zustand neutral | ○ |
| U08 = E-03 | Vorlagen im Anlegen-Weg, gefüllte Vorschau vor dem Anlegen | ○ |
| G14 = D-01 | Inhaltssuche in Strg/Cmd+O, danach optionaler FTS5-Cache und eine Befehlspalette | ◐ 3.33.7: Inhalt von Seiten, Notizen, Listen-/Aufgabenbeschreibungen mit Ausschnitt; FTS5, Vereinigung und Hervorhebung offen |
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
| N09 | Erinnerungen bei geschlossener App (Stufe C) | ✕ | Produktgrenze |
| N10 | Lokaler MCP-Server | ✕ | Q3: Dokumente statt Schnittstelle |
| N14 = G07 | Systemweiter Erfassungs-Hotkey | ✕ | nur plattformeigen lösbar (Q2) |
| N06 | „Erste Schritte“-Seite, Einstieg für neue Nutzer | ✕ | bewusst nicht gewählt; Rundgang und Showcase vorhanden |
| G23 | Gleichzeitige Bearbeitung auf zwei Geräten | ✕ | Produktgrenze |
| G22 | Verschlüsselte Ablage | ✕ | keine Priorität |
| G12, G13 | Spalten in Seiten, Graph | ✕ | Entscheidungen 29./30.09.2026 |
| ZF-200 | Eigene Felder je Liste | ✕ | am 25.09.2026 nicht gewählt |
| N15–N20 | Spracherfassung, Cloud-KI, Teamfunktionen, freie Datenbankfelder, Web Clipper | ✕ | Produktgrenzen |

## 8. Abhängigkeiten und Regeln vor der Umsetzung

- **Referenz- und Löschregeln vor G29/G31/G28:** Eine Aufgabe hat genau einen Heimatort (Liste, Seite oder Notiz), andere Orte zeigen einen Verweis. Entfernt man eine Verweiszeile, entfällt nur der Verweis. Entfernt man die Zeile am Heimatort, wandert die Aufgabe in den Papierkorb; Verweise zeigen „im Papierkorb“ bzw. nach endgültigem Löschen „Ziel fehlt“. Undo stellt beides zusammen her.
- **Datenformat-Tor 21:** beim ersten inkompatiblen Inhalt (Verweise, Animation), mit Vorsicherung, Migration und schreibgeschütztem Altleser.
- UX1 vor Zusammenführung der Befehlspalette und dem FTS5-Ausbau; die erste Inhaltssuche in Strg/Cmd+O benötigt weder Menüumbau noch Index; P08a vor P08b; D07 vor G17; G24 vor G21; D15 vor G26 vor N12.

## 9. Risiken

| Nr. | Risiko | Gegenmaßnahme |
|---|---|---|
| R1 | Regressionen in der Klasse `ListApp` (rund 54.500 Zeilen in `app.pyw`) | kleine Schnitte, echte Bedienproben, Vollprüfung je Schnitt, Fachlogik als Tk-freies Modul (D17) |
| R2 | Menübeschriftungen sind Schlüssel für Aktionen; Umbenennen bricht Zuordnungen | stabile Aktionskennungen vor UX1; Test „jede Aktion erreichbar“ |
| R3 | Neue Dokumentinhalte gehen in älteren Fassungen verloren | Datenformat-Tor 21 |
| R4 | P08b übersieht einen Änderungsweg | Vollvergleich im Autosave, Differenztest |
| R5 | Aktueller Plattform-/Liefernachweis offen | Windows-Gesamtprüfung 3.33.8 grün; Referenz-Mac, Bundle, Linux und menschliche Prüfliste bleiben eigene Tore, D15 |
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

| Nr. | Aufgabe | Stand |
|---|---|---|
| A–H | Richtung und Bearbeitungstiefe der weiteren Auswahl | Auftrag 05.10.2026: Umsetzung beginnen; konkrete Folgepakete unten. Export-, Import- und Veröffentlichungsentscheidungen bleiben offen |
| D07 | Animationsexport | ○ erst zur Pixel-Etappe |
| I1 | Inhaberangaben bestätigen | ○ Vorschläge in [Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md#inhaberangaben) |
| I2 | Lizenzbedingungen veröffentlichen | ○ Entwurf: kostenlos für private, nicht kommerzielle Nutzung |
| I3 | Apple-Developer-Konto, Windows-Code-Signing-Zertifikat | ○ |
| I4 | Markenprüfung „Glide“ | ○ Fachanwalt für Markenrecht |
| I5 | Python 3.14.7 auf dem Mac installieren | ○ braucht das Passwort des Inhabers |
| I6 | Windows-Vollprüfung und manuelle Prüfsitzungen | ◐ Windows-Gesamtprüfung 3.33.8 grün (66 Integrationssuiten, 75 Unit-Tests, Python 3.14.8/Tk 9.0.4); menschliche Abnahme ○ [Prüfliste](Glide_Manuelle_Pruefung.md) |
| – | Erste Importquelle für G21, Bauwerkzeug für G26 | ○ erst in Stufe 4 |

## 12. Zukunftsperspektive und nächste Umsetzung (05.10.2026)

**Entscheidungsgrundlage:** [Markt und Vorbilder](Glide_Markt_und_Vorbilder.md#6-verifizierter-abgleich-und-konsequenzen-05102026), aktueller Code und isolierte Windows-Baseline. Die breite Produktmatrix ist keine vollständige neue Herstellerprüfung. Es liegen keine Nutzungsdaten vor; Prioritäten folgen konkreter Funktionslücke, vorhandener Entscheidung, Aufwand und Regressionsrisiko, nicht erfundenen RICE-Zahlen.

| Reihenfolge | Paket / Nutzen | Abhängigkeit und Abnahme | Status |
|---|---|---|---|
| Jetzt | G14 erste Stufe: vorhandene Inhalte wiederfinden; Windows-Formatsicherung korrigieren | Kein Formatwechsel, keine neue Laufzeitabhängigkeit; Inhalte/IDs/Archiv/Neustart, Differenz zur Vorversion | seit 3.33.7 implementiert, mit 3.33.8 Python-Lieferung; Grenzen im QA-Bericht |
| Prüftor/Lieferung | Windows-Gesamtabnahme 3.33.8 und 07-Abgleich; Referenz-Mac/Bundle separat | Veraltete Testannahmen korrigiert; Titel-/Mindesthöhen-/Editor-Timerbefunde und übersehene Formatwechsel bei identischen Dateimetadaten behoben. 66 Integrationssuiten/75 Unit-Tests grün, 07/Showcase SHA-256-abgeglichen | ◐ Windows/Python-Lieferung erledigt; Referenz-Mac/Bundle und menschliche Abnahme offen |
| Nächster Produktionsschnitt | P08a: ein Vergleichslauf für Verlauf/Aktivität/Änderungsdatum; anschließend P09b | Gleiche synthetische Bestände, Median/p95, Differenztest aller Änderungen; alte und neue Historie identisch | ▶ bestehender Performance-Auftrag |
| Danach | Stabile Aktionskennungen, anschließend UX1 in kleinen Paketen (U03/U07/U10/U19 zuerst) | Jede Aktion über Menü und Palette erreichbar, Copy/Paste/Undo mit Editorfokus; Kalender bleibt Strg/Cmd+K (bestehende Entscheidung) | ▶ im aktuellen Feature-Auftrag vorgesehen, noch nicht umgesetzt |
| Danach | G05 Fokus auf vorhandener Zeiterfassung, H-02 Tastaturwege | Zeit genau einmal buchen bei Pause, Wechsel und Neustart; 860 × 700/große Schrift, ein Undo je Strukturaktion | ○ geplant |
| Danach | G29/G31/G32 Aufgaben im Text, dann G08/G30 Rückverweise | Heimatort, Papierkorb/fehlendes Ziel, Rename/Move/Import/Undo zuerst testen; vor inkompatiblen Verweisen Format-21-Tor | ○ geplant |
| Nach Messung | G14 FTS5-Ausbau | Nur bei gemessener Suchlatenz; Index vollständig ersetzbar, Öffnen ohne Index, keine SQLite-Hauptablage | ○ geplant |
| Später | Pixel/Animation, Austausch und Paketierung | D07, erste Importquelle, Bauwerkzeug separat; Paketierung vor Screenreader-Abnahme | ◇ an bestehende Entscheidungen gebunden |

**Messung des ersten Suchschnitts:** Tk-freier Fachvergleich synthetischer Beschreibungen, Windows/Python 3.12.10, sieben warme Runden: 1.000/5.000/10.000 Inhaltstreffer im Median 16,3/76,5/151,5 ms, p95 23,9/77,0/152,1 ms. Ohne Treffer bei 10.000 Punkten 17,9 ms. Das umfasst nicht die Oberfläche; nächste Suchoptimierung: Ausschnitte erst für die angezeigten Treffer erzeugen und anschließend die gesamte Eingabe bis zur Anzeige messen, bevor ein FTS5-Cache eingeführt wird. [Rohwerte](../01_Repository/Glide/tests/qa-3.33.7/suche_2026-10-05/messung_fachsuche.json).

**Bewusst begrenzt:** Kein allgemeiner Notion-Nachbau, kein neuer Sync-/Cloud-Dienst. Konto- und netzunabhängige Tagesplanung mit eigenen Daten, Wissen im Kontext und persönlicher Pixelgestaltung ist die Richtung. Die Pixel-Werkstatt ist eine besondere Kombination, keine weltweit bewiesene Alleinstellung. Suchlatenz und Fokus-/Tastaturbedienung werden je Schnitt geprüft; eine automatische Windows-Prüfung ersetzt weder den Referenz-Mac noch die menschliche Freigabe.

## 13. Abgleich mit dem ursprünglichen Zukunftsdokument

Original vollständig aus der Git-Historie gelesen: „Glide – KI-Austauschformat und Zukunftsarchitektur“, frühere Datei `00_Arbeitsvorbereitung/Archiv/Glide_KI_Austauschformat_und_Zukunftsarchitektur_Dublette_2026-09-18.md`, Commit `569020ef65880b28a50408e229a8027ba2a65898`. Die späteren namensähnlichen Fassungen waren nur Verweise. Die ursprünglichen Beispiele beziehen sich auf Format 15 und sind keine aktuellen Formatverträge. [Original in Git](https://github.com/n05a-design/glide-to-do/blob/569020ef65880b28a50408e229a8027ba2a65898/00_Arbeitsvorbereitung/Archiv/Glide_KI_Austauschformat_und_Zukunftsarchitektur_Dublette_2026-09-18.md).

| Ursprüngliche Idee | Heutiger Code / Entscheidung | Konsequenz |
|---|---|---|
| Internes Format, Exchange und KI-Beschreibung trennen | `DATA_SCHEMA_VERSION = 20`, `EXCHANGE_FORMAT_VERSION = 1`, `exchange_manifest`, erzeugte Spezifikation vorhanden | ✅ Grundlage erhalten; neue Funktionen nicht automatisch zum Exchange-Vertrag erklären |
| Create mit freien Schlüsseln statt erfundener UUIDs | `parse_exchange_document`, Preview und Import; echte IDs werden von Glide vergeben | ✅ kein neuer Importweg nötig |
| Capability Registry, unbekannte Felder sichtbar | `exchange_capabilities`, Feldlisten, Importbericht; Anhänge/Repeat/Reminder/Patch bewusst Stufe 0 | ✅ bei G24 Registry, Spezifikation und Verlustbericht gemeinsam weiterführen |
| `.glidecontext` plus geprüfte Patch-Operationen | Kontextpaket und `patch_mode` noch nicht implementiert | ○ G24: Auswahlumfang, Prüfsummen, Ausgangsstand und Feldvergleich; Vorschau, Bestätigung, Vorsicherung, atomarer Undo-Schritt. Stale Konflikte nie still überschreiben |
| Echte Notizen je Aufgabe, getrennt von Beschreibung | Eigenständige Notizlisten/Seiten vorhanden; kein datiertes `item.notes[]`-Modell | ◇ ZF-NOTES: optionaler Wissensausbau nach G29/Verweisen; erst konkreten Bediennutzen, Migration, Lösch- und Exchange-Regeln definieren. Keine zweite Beschreibung ergänzen |
| Unteraufgaben mit `children`, keine zweite `subtasks`-Struktur | rekursive Aufgaben, Klappkontrolle und Strukturmutationen vorhanden | ✅ Datenstruktur behalten; H-02 prüft die verbleibenden Tastaturwege |
| Dynamische Pinnwand statt Aufgabenkopien | vorhandenes Board nutzt echte Aufgaben, Quellen/Filter/Gruppierung | ◐ ursprüngliches Ziel weitgehend erreicht; kein zweiter Board-Inhaltstyp |
| Allgemeines ViewDefinition-Modell | vorhandene Ansichten/Filter, D17 verbietet Großumbau | ◇ nur gleiche Quellen-, Filter- und Sortierlogik schrittweise extrahieren; kein Architekturprojekt ohne gemessenen Nutzen |
| Tabellenbreiten und gemeinsame UI-Bausteine | `table_column_widths`, `table_sort`, `ThemedAutoScrollbar`, `DropdownPopup` vorhanden | ◐ vorhandene Bausteine weiterverwenden; Fokus/Trackpad/Kontrast über echte Bedienwege prüfen |
| Labelbeschreibungen und eigene Felder | Label-Felder derzeit key/name/color; eigene Felder je Liste später bewusst nicht gewählt | ◇ ZF-LABEL: Beschreibungen nur mit belegtem Bedarf; ✕ eigene Datenbankfelder gemäß Produktgrenze. Historische Vorschläge überschreiben keine spätere Entscheidung |
| Eigener KI-Bereich, Plugins/API und Systemintegration | Dateimenü enthält die Austauschwege; Q3 entscheidet Dokumente statt Schnittstelle | Kein neuer Hauptbereich nötig; Kontextpaket/Änderungsvorschlag im vorhandenen Dateiaustausch, kein MCP-/Cloud-/API-Auftrag daraus ableiten |

Die erste Inhaltssuche unterstützt dieses Zielbild unmittelbar: bestehende Beschreibungen, Seiten und Notizen werden nutzbar wiedergefunden. G24 folgt später, weil sichere Änderungsübernahme, Referenzen und Versionstore vor automatischem Bearbeiten wichtiger sind als ein weiterer KI-Knopf.

## 14. Pflege

- Bei jeder Produktionsrunde Statusmarken, Abschnitt 2 und die Ziele nachführen. Keine datierte Kopie anlegen; Git trägt die Vorfassung.
- Neue Ideen erst nach dem [Prinzipien-Check](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md#prinzipien-check-für-neue-funktionen) und mit Marke aufnehmen.
- Neue Entscheidungen gehören in die [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md), nicht hierher.
