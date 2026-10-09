# Glide – Entwicklungsplan und Aufgabenstand

Stand 09.10.2026 · Glide 3.35.0 · Aufgabenformat 23

Einziges Planungsdokument. Es führt zusammen, was bis 03.10.2026 auf zwölf Planungs-, Auswahl-, Recherche- und Entscheidungsdokumente verteilt war (Entwicklungsplan 3.33ff, Aufgabenauswahl A–H, Funktionsrecherche G01–G32, Arbeits- und Featureplanung P01–P07, Bestandsaufnahme AB/T, UX-Prüfung U01–U24, Übersicht vom 29.09.2026 und die älteren Kataloge). Die Vorfassungen trägt Git.

Verbindliche Entscheidungen stehen in der [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md), Produktgrenzen und Prinzipien in den [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md). Der Auftrag vom 05.10.2026 umfasst gründliche Planung und den Beginn der Feature-Umsetzung; am selben Tag um das [Ausbauprogramm Alltag, Komfort und Oberfläche](#43-ausbauprogramm-alltag-komfort-und-oberfläche) erweitert. Die Reihenfolge unten konkretisiert diesen Auftrag; D07, Importquelle, Bauwerkzeug und Inhaberfreigaben bleiben eigene Entscheidungen.

**Sprint ab 08.10.2026:** Der Auftrag vom 08.10.2026 verlangt Analyse, Recherche und die vollständige Umsetzung eines festgelegten Aufgabenumfangs. Maßgeblich für diesen Sprint sind der [Aufgabenkatalog in Abschnitt 15](#15-sprint-ab-08102026-aufgabenkatalog) mit Phasen, Aufgabenkarten und benötigten Inhaberentscheidungen sowie die [Analyse](Glide_Analyse.md). Die Abschnitte 2–13 bleiben die fortlaufende Aufgabenliste; ihre Marken werden mit jedem Paket nachgeführt.

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
| 0 Fundament | Performance P03–P09, T2, CI | ◐ P08a/P09b/P08b mit 3.33.9–3.33.11 Windows/Python geprüft und geliefert, Referenz-Mac offen. P04/P06r beauftragt |
| 1 Klarer Alltag (3.33.x) | Bereiche, Startseite, Eingabe, Eisenhower, Heute/Demnächst, UX1, Fokus, Aufgaben im Text; Ausbau Komfort, Tag und Oberfläche Welle 1–2 (§4.3) | ◐ 3.33.1–3.33.6 erledigt, G14-Suchbeginn 3.33.7; erste UX1-Schnitte 3.33.11/3.33.12 und KO01/AU02 3.33.13 Windows/Python geliefert; Tagespaket 3.33.14 umgesetzt, Windows-Gesamtprüfung und Python-Lieferung grün; strenge CI Exit 0 (17 Schritte, 24 Werkzeugtests); G29/G31/G32 mit 3.33.15 umgesetzt; Bedienkomfort U01/U02/U13/U14/U16/U22/U24 mit 3.33.16 Windows/Python geprüft und geliefert; native/menschliche Abnahme offen |
| 2 Wissen im Kontext (seit 3.33.17; weiterer Ausbau 3.34.x) | Inspektor, Volltextsuche, allgemeine Verweise (eigenes Formattor), Live-Liste, Titelbild, Kalender eingebettet mit Wochenplanung (Welle 3, §4.3) | ◐ G14 seit 3.33.7; Prüfung/Lieferung 3.33.8 im QA-Bericht. G08/G30 und N04/AU04 mit Format 22 in 3.33.17 Windows/Python geprüft und geliefert; G28/G09/U08 mit 3.33.18 Windows/Python geprüft und geliefert; native/menschliche Abnahme offen |
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
| ✅ 3.33.3 | G01 = B-01 deutsche Schnelleingabe mit Feldchips, D10 |
| ✅ 3.33.4 | Wiederholungen in der Schnelleingabe (setzen die Fälligkeit) |
| ✅ 3.33.5 | G02 Eisenhower als Gruppierung (D13) |
| ✅ 3.33.6 | D14 „Heute“ und „Demnächst“ |
| ✅ 3.33.7/3.33.8 | G14-Inhaltssuche, Windows-Formatsicherung und Dateiinhaltsvergleich, Mindesthöhen/Titelbreiten, Editor-Timerabbau; Windows-Vollprüfung grün, Python-Lieferung 3.33.8 abgeglichen. Referenz-Mac/Bundle und menschliche Freigabe offen |
| ◐ 3.33.9 | P08a gemeinsamer Speichervergleich, gleiche Verlaufssnapshots/-ereignisse und Aktivitätsregeln; Windows-Vollprüfung grün, Python/Showcase abgeglichen. Referenz-Mac/Bundle offen |
| ◐ 3.33.10 | P09b Kennzahlen je Aufbau, gemeinsames Datumslesen, Messschrift-/Zeilenraumcache und Timerabbau; gezielte Differenz-/Undo-/Tages-/Host-/Neustartprüfung und Windows-Vollprüfung grün, Python/Showcase abgeglichen. Referenz-Mac/Bundle offen |
| ◐ 3.33.11 | P08b für lokale Punktänderungen, stabile Aktionskennungen, U03/U07; Windows-Vollprüfung und 120 Differenzfälle grün, Python/Showcase ausgeliefert; Referenz-Mac/Bundle offen |
| ◐ 3.33.12 | U10/U19 Titel vor Kennzahlen, Herkunft rechts in Heute; erste OB01-Übernahme (`ui_design.py`) |
| ◐ 3.33.13 | KO01 Einplanen, AU02 verfügbare Zeit in allen Planungswegen (`planning.py`) |
| ◐ 3.33.14 | Tagespaket: AU01 Tagesvorschlag, geführter AU03-Weg, G05/AU05 Fokus, H-02 für Zeitblöcke |
| ◐ 3.33.15 | Aufgaben im Wissen G29/G31/G32, Format 21 |
| ◐ 3.33.16 | Bedienkomfort U01/U02/U13/U14/U16/U22/U24 |
| ◐ 3.33.17 | Wissen und Woche N04/AU04, G08/G30, Format 22 |
| ◐ 3.33.18 | Seiten im Alltag G28/G09/U08, Format 23 |
| ◐ 3.33.21 | Ruhige Oberfläche N01/U15/U05r/U09/U18/OB05/OB01r/W05; Mac-Vollprüfung, Python/Showcase und Bundle 3.33.21 geliefert; W07/W08, Windows-Vollprüfung und menschliche Abnahme offen |
| ◐ 3.33.20 | Komfort KO02/KO03/KO05/KO06/U04/U20/N07/AB08/AU06; Mac-Vollprüfung, Python/Showcase und Bundle 3.33.20 geliefert; Windows-Vollprüfung und menschliche Abnahme offen |
| ◐ 3.33.19 | Tempo P06r/P04/P03r/E01, P08c/P01r gemessen; Mac-Vollprüfung, Python/Showcase und Bundle 3.33.19 geliefert; Windows-Vollprüfung und menschliche Abnahme offen |
| Gemeinsam 3.33.9–3.33.18 | jeweils Windows/Python-Vollprüfung grün und Python/Showcase geliefert; Mac-Vollprüfung und Bundle 3.33.18 seit 09.10.2026 grün (PR01); ◐ bis zur menschlichen Abnahme (I6) |
| ✅ 01.–03.10.2026 | D09 Repository als Ablage, CI-Grundstufe, Ablagegröße, Bereinigung der Ablage und Dokumentation |

## 3. Performance (Stufe 0, beauftragt)

Fortlaufender Auftrag des Inhabers: „Ich habe Performance Probleme mit Glide, hilf mir die Code-Basis zu optimieren, mit Variabeln für die gleichen Funktionen, Streamlinen und optimieren.“ Gleiche Funktionen und Werte nur bei gleicher Bedeutung bündeln, Aufbau- und Schreibaufwand messbar senken, Daten-, Undo- und Fokusverhalten erhalten. Keine pauschale Ersetzung von Datenschlüsseln durch Variablen.

| ID | Arbeit | Stand |
|---|---|---|
| P01 | Messbasis: unprofilierte Serien mit 100/1.000/10.000 Punkten, Notiz, Bildseite | ◐ Serien seit 3.32.2; offen: Verlaufvarianten, Speicherentwicklung |
| P02 | Schriftcache je Tk-Interpreter | ✅ 3.32.2 |
| P03 | Aufbau und Layout | ◐ Bibliothekskarten ✅ 3.32.3, Startseite ✅ 3.33.2 (764 → 507 ms), unveränderte Startseitenkacheln bleiben ✅ 3.33.19 (P03r). Offen: Elemente geänderter Karten, sehr viele Karten |
| P04 = A-02 | Bildlayout nur bei geänderter Geometrie, Platzieren beim Scrollen | ✅ 3.33.19 (Tippen fern vom Bild 267–273 → 2,5–3,9 ms) |
| P05 | Gemeinsame Helfer | ◐ Hover ✅ 3.32.2; gleiche UI-Texte nur bei gleicher Bedeutung zentralisieren |
| P06r = A-03 | Doppelte Refresh-/Schreibanforderungen je Aktion | ✅ 3.33.19 (je Aktion ein Seitenleistenaufbau und ein Einstellungsschreiben); Archiv-Zurückholen ✅ 3.32.3 |
| P07 | Volltextsuche als ersetzbarer FTS5-Cache | ✕ 09.10.2026 nach Messung (3.34.0): Median 66,6 ms, p95 73,1 ms bei 10.000 Punkten und 200 Seiten – unter der Regelgrenze 100 ms, kein FTS5-Index; 3.33.21 lag bei 100,8 ms, gesenkt durch Ausschnitt ohne Zeichenschleife |
| P08a | Ein Vergleichsdurchlauf für Verlauf, „zuletzt bearbeitet“, Aktivität (T1: ≈ 78 % von `save_items` bei 10.000 Punkten) | ◐ 3.33.9 implementiert, Windows-Vollprüfung/120 Differenzfälle grün, Python/Showcase ausgeliefert; Referenz-Mac/Bundle offen |
| P08b | Nur geänderte Listen vergleichen, Vollvergleich im Autosave | ◐ 3.33.11 Windows/Python geprüft und geliefert: 22 lokale Einstiege in 18 Methoden; übrige 27 Einstiege und Autosave vollständig. 120 Differenzfälle, Fehler/Retry/Undo/Reload grün; Zielwert 120 ms und Referenz-Mac offen |
| P09a | Tabelle misst keine Listenspalten | ✅ 3.33.0 |
| P09b | Kennzahlen einmal je Aktualisierung, Datum über Zwischenspeicher, Schriftobjekte und Zeilenhöhen je Schrift merken (W2–W5) | ◐ 3.33.10 implementiert; Tk-freies `view_metrics.py`, Messprobe aus Git 7f30baf nach `scripts/pflege` übernommen. Windows-Vollprüfung/120 Differenzfälle grün, Python/Showcase ausgeliefert; Referenz-Mac/Bundle offen |
| T2 | Gemeinsame Formatsicherung | ✅ 3.33.0; Windows-Signatur 3.33.7, Inhaltsvergleich gegen Metadatenkollisionen 3.33.8 |
| – | Einblendung des Einstellungsfensters (Median rund 2,1 s) | ▶ eigener Messpunkt |
| CI | CI-Grundstufe (Linux/Xvfb) | ✅ 01.10.2026; ○ Integrationssuiten unter Linux kalibrieren, damit sie verpflichtend in die CI können |

**Neue Windows-Messgrenze 3.33.8:** Der Formatcache muss bei identischen Metadaten den vollständigen Inhalt prüfen. SHA-256 einer warmen synthetischen Datei mit 10.000 Punkten: Median 1,5 ms, Maximum 5,6 ms in 21 Runden. Das ist kein gesamter Speichervorgang. Die P08a-Baseline muss diesen Leselauf sowie Verlauf, Aktivität und „zuletzt bearbeitet“ getrennt und insgesamt messen; bestehende Linux-Zahlen sind keine aktuelle Windows-Garantie. [Messung](https://github.com/n05a-design/glide-to-do/blob/254541aeae4577c0529d1ef768846a5c4546e59f/01_Repository/Glide/tests/qa-3.33.8/windows_2026-10-05/messung_dateipruefung.json).

**Fertig, wenn:** Abhaken bei 5.000 Punkten ≤ 120 ms (Linux-Referenz, Python 3.14; heute 218 ms) und auf dem Referenz-Mac vergleichbar gemessen; erstes Speichern ohne Zusatz-Parse; Verlauf und „zuletzt bearbeitet“ identisch zum alten Verfahren; Vollprüfung grün; 07/Bundle per SHA-256 abgeglichen.

**P08a-Messung 3.33.9:** Windows/Python 3.14.7, 21 warme abwechselnde Runden gegen den unveränderten Git-Stand 3.33.8, gleiche künstliche Daten. Bei 10.000 Aufgaben: reine Vergleichsarbeit flach Median 159,344 → 150,785 ms (5,4 %), p95 222,387 → 236,274 ms; mit Unteraufgaben Median 183,92 → 148,653 ms (19,2 %), p95 266,806 → 235,931 ms. Separater vollständiger Speicherweg, neun warme Runden: `save_items` 360,018 → 344,883 ms im Median, Abhaken 518,702 → 553,785 ms. Ein allgemeiner Gewinn für die Bedienlatenz ist damit nicht belegt; P09b/P08b bleiben erforderlich. Rohwerte und Abnahme: Nachweis (historischer Nachweis außerhalb der Aufbewahrung).

**P09b-Messung 3.33.10:** 1.000 Aufgaben: neun warme Runden; 10.000 Aufgaben: zwei Serien alt/neu und neu/alt, zusammen 18 warme Werte je Variante. Große einzelne Liste: Median Öffnen 992,50 → 747,75 ms (24,7 %), Tabelle 630,95 → 498,60 ms (21,0 %), Öffnen + Abhaken 1.961,95 → 1.493,85 ms (23,9 %). Heute bleibt mit rund 6,8 s deutlich langsam. Separater Speicherweg (10.000 Aufgaben in 50 Listen): gepoolter Save-/Abhakmedian schlechter; zweites Paar beim Abhaken nahezu gleich (613,349 → 615,246 ms). Kein belastbarer Gesamtgewinn für diesen Weg. Finalmessung nach Timerregistrierung: eine Kennzahlberechnung je Listenaufbau, zwei neue Schriftobjekte, keine warmen Datums-Parses; native Mac-Abnahme offen. Nachweis (historischer Nachweis außerhalb der Aufbewahrung).

**P08b-Messung 3.33.11:** Windows/Python 3.14.7, 10.000 Aufgaben in 50 Listen, zwei serielle Paare alt/neu und neu/alt mit zusammen 18 warmen Werten. Abhaken mit sofortiger vollständiger Speicherung: Median 589,577 → 347,075 ms (41,1 %), p95 1.010,782 → 426,874 ms; beide Paare bestätigen die Richtung. 1.000 Aufgaben: Median 199,780 → 176,797 ms (11,5 %). Vollspeicherung schwankt und wird bei 1.000 Aufgaben langsamer. Zielwert 120 ms bleibt offen; kein gleicher Gewinn für eine einzelne große Liste oder Heute belegt. historischer Nachweis außerhalb der Aufbewahrung.

## 4. Klarer Alltag (Stufe 1)

### 4.1 UX1 „Weniger Oberfläche“ (▶ Folgepaket im Auftrag 05.10.2026)

Stabile Aktionskennungen sowie U03/U07 sind seit 3.33.11 umgesetzt, U10/U19 und die erste OB01-Übernahme mit 3.33.12; Windows-Vollprüfung und Python-Lieferung grün, native und menschliche Abnahme offen. KO01/AU02 mit 3.33.13 Windows/Python geprüft und geliefert; native und menschliche Abnahme offen. Tagespaket AU01/AU03/G05/AU05/Raster-H-02 mit 3.33.14 umgesetzt; Windows-Gesamtprüfung und Python-Lieferung grün (§4.4); strenge CI Exit 0 (17 Schritte, 24 Werkzeugtests). Aufgaben im Wissen (G29/G31/G32) mit 3.33.15 Windows/Python geprüft und geliefert; native/menschliche Abnahme offen. Bedienkomfort U01/U02/U13/U14/U16/U22/U24 mit 3.33.16 Windows/Python geprüft und geliefert; native/menschliche Abnahme offen. Weitere UX1-Arbeit: N01 und U05-Rest; größere Gestaltungsschritte nach I7. Wissen und Woche N04/AU04/G08/G30 mit 3.33.17 Windows/Python geprüft und geliefert; G28/G09/U08 mit 3.33.18 Windows/Python geprüft und geliefert.

| ID | Befund (Prinzip) | Empfehlung | Stand |
|---|---|---|---|
| U01 = N03 | Kopfzeile mit acht Symbolknöpfen, zwei Suchen (P3, P5) | ⌕ und ⌘ zu einer Befehlspalette (`Strg/Cmd+O`; `Strg/Cmd+K` bleibt Kalender); Verlauf und Drucken ins Menü; Glocke nur bei Bedarf; Ziel ≤ 4 Symbolknöpfe | ◐ 3.33.16 Windows/Python geprüft und geliefert; native/menschliche Abnahme offen |
| U02 | Dauerhafte Hinweiszeilen (P1, P4) | „?“ klappt Hinweise ein/aus, Zustand gemerkt (D11) | ◐ 3.33.16 Windows/Python geprüft und geliefert; native/menschliche Abnahme offen |
| U03 | „Suche löschen“ auch bei leerer Suche | Löschkreuz nur bei Inhalt, `Esc` leert | ◐ 3.33.11 Windows/Python grün; echte Esc-Bindung, 860 × 700/große Schrift/hell/dunkel geprüft; native/menschliche Abnahme I6 offen |
| U04 | „Erweitert“/„Hinzufügen“ als Textknöpfe | Feldchips ✅ 3.33.3; „+“-Knopf und Umschalt+Enter ✅ 3.33.20 | ✅ |
| U05 | Startseite überladen | ✅ 3.33.2 (D12); Gismo-Kachel mit Pflegeleiste bei Bedarf ✅ 3.33.21 (U05r) | ✅ |
| U06 | Überlappende Ansichten | ✅ 3.33.6 (D14) | ✅ |
| U07 = N02 | Eingang nicht in der Seitenleiste | Zeile „Eingang (n)“ nur solange er Einträge hat | ◐ 3.33.11 Windows/Python grün; Navigation/Leerwerden/Undo/Reload und 860 × 700/große Schrift geprüft; native/menschliche Abnahme I6 offen |
| U10 | Kopfzeile kürzt den Titel zugunsten der Kennzahlen | Titel hat Vorrang, Kennzahlen immer in der Unterzeile | ◐ 3.33.12 Windows/Python geprüft und geliefert; OB06/I6 und Referenz-Mac offen |
| U13 | Bibliothek mit doppelten Wegen | Kachelklick öffnet; Fußleiste „Neu ▾ · Importieren ▾ · Archiv (n) · Kartengröße“ | ◐ 3.33.16 Windows/Python geprüft und geliefert; native/menschliche Abnahme offen |
| U14 | Menüeinträge am falschen Ort, drei Sicherungsbegriffe | Papierkorb leeren → Bearbeiten; Mitteilung testen → Einstellungen; Sicherung vereinheitlichen | ◐ 3.33.16 Windows/Python geprüft und geliefert; native/menschliche Abnahme offen |
| U16 | Begriffe uneinheitlich (Punkt/Aufgabe/Eintrag, „Long-Task“) | Glossar: Aufgabe, Langtext, Zwischenüberschrift, Gruppe | ◐ 3.33.16 Windows/Python geprüft und geliefert; native/menschliche Abnahme offen |
| U17/N01 | Kein „wie System“ | „Automatisch (hell/dunkel)“ als Standard, Signaturdesign vorn | ○ |
| U19 | Quellliste und Nummer vor jedem Titel in „Heute“ | Titel zuerst, Quelle gedämpft rechts | ◐ 3.33.12 Windows/Python geprüft und geliefert; OB06/I6 und Referenz-Mac offen |
| U22 | Bearbeitungstag in Listenzeilen unsichtbar | Symbol ◉ + Tag in der Datumsspalte | ◐ 3.33.16 Windows/Python geprüft und geliefert; native/menschliche Abnahme offen |
| U24 | Symbole mit mehreren Bedeutungen (▲ ▼ ◷ ≡ ◐) | eigene Zeichen für Eingang, Verspätet, Zeiterfassung; Doppelungsregel in der Symbolprüfung | ◐ 3.33.16 Windows/Python geprüft und geliefert; native/menschliche Abnahme offen |

**Fertig, wenn:** Kopfzeile ≤ 4 Symbolknöpfe; Bedienfläche über dem Inhalt ≤ 15 % bei 1280 × 800 (heute ≈ 27 %); kein Symbol mit zwei Bedeutungen (Bewegungspfeile ausgenommen).

### 4.2 Weitere Arbeiten der Stufe 1

| ID | Arbeit | Stand |
|---|---|---|
| G05 = B-02 | Fokus mit Timer an der vorhandenen Zeiterfassung, eingebettet in „Heute“; Zeit wird genau einmal gebucht, auch nach Pause, Wechsel, Neustart | ◐ 3.33.14 umgesetzt und gezielt Windows-geprüft; Windows-Gesamtprüfung und Python-Lieferung grün; strenge CI Exit 0 (17 Schritte, 24 Werkzeugtests), native/menschliche Abnahme offen |
| H-02 | Tastaturwege für alles, was sich ziehen lässt, mit sichtbarem Ziel und einem Undo-Schritt | ◐ Zeitblöcke/Raster 3.33.14; Pinnwand und Seitenbäume in passenden Folgepaketen offen |
| G29 = C-01 | Einzelne Aufgaben im Notiztext mit derselben ID wie im Aufgabenbereich (D05, Q5) | ◐ 3.33.15 echte Notiz-/Textaufgaben mit gemeinsamen IDs, Verweisen und Lösch-/Undo-Regeln; Paketprüfung grün, Windows-Gesamtprüfung und Python-/Showcase-Lieferung grün; strenge CI Exit 0 (17 Schritte) |
| G31 = C-02 | Seitenaufgabe über ID in eine Liste schicken, Verweis bleibt | ◐ 3.33.15 gleicher Punkt samt Unteraufgaben in Aufgabenliste, Text bleibt Verweis; Windows-Gesamtprüfung/Python-Lieferung grün, native/menschliche Abnahme offen |
| G32 = C-03 | Filter „aus Seiten“ in vorhandenen Ansichten (Kopfzähler gibt es schon) | ◐ 3.33.15 Aus-Seiten-Filter in vorhandenen Ansichten, Quellen öffnen, Archiv/Mehrfachverweise geprüft; Windows-Gesamtprüfung/Python-Lieferung grün, native/menschliche Abnahme offen |
| N07 = U21 | Einmalige Karte „Neu in …“ nach einem Update | ✅ 3.33.20 |
| N08 | JPEG-Vorschau unter Linux über ein Systemwerkzeug | ✅ 3.34.0 (`gdk-pixbuf-thumbnailer` oder `djpeg`, wenn vorhanden; auf dem Mac mit erzwungenem Linux-Weg geprüft, Linux-Sichtprüfung offen) |
| U20 | Leerzustand ohne doppelten Anlegen-Knopf | ✅ 3.33.20 |
| DOK2 | Code-Kommentar AB06 berichtigt (3.33.9); Mindestversion Python/Tk festlegen und beim Start prüfen (AB08) | ✅ AB08 3.33.20 (`runtime_check.py`); AB03–AB05, AB07 ✅ |
| W11 | Kommentare in `tests/tools/pruefen.py` und `tests/tools/hintergrund/sitecustomize.py` versprechen noch Tastaturabschirmung | ✅ 08.10.2026 berichtigt (nur Kommentare/Docstrings, Syntaxbaum sonst unverändert) |
| LG01 | Logo-Rückfall unter Tk 8.6 geglättet: Ein Tk-freies Modul rastert die Umrisse aus `svg_geometry.outline` mit Flächenanteil je Pixel und übergibt ein RGBA-PNG (Weg B der [Diagnose](../01_Repository/Glide/docs/diagnosen/LOGO_KANTENGLAETTUNG.md)) | ○ Auswahl I8 |
| LG02 | App-Symbol in 16, 32, 64 und 256 px vorrechnen (`baue_symbole.py`), `icon_photos` lädt sie unter Tk 8.6 direkt; spart rund 0,5 s beim Start. Unbenutztes `glide-logo.png` und Modulkopf von `logo.py` berichtigen (Wege C und F) | ○ Auswahl I8; nur in einer Produktionsrunde |
| LG03 | `test_logo330` verlangt für beide Wege Zwischentöne an der Logokante, zum Beispiel mindestens 20 Farbwerte bei 54 px (Weg D) | ○ Auswahl I8 |
| LG04 | Logo-Master überarbeiten: Rundungen tangential an die geneigten Geraden, Kleinstabweichungen, Kurzsegment, optional Kleingrößenfassung (Weg E; [Befunde](../20_Grafik_Master/README.md#befunde-am-logo-master-05102026-entscheidung-beim-inhaber)) | ○ Gestaltung beim Inhaber |
| W01 | Seitenleistentitel unter Windows/Tk 9 rechts um etwa ein Zeichen angeschnitten, ohne „…“ (Aufnahme 05.10.2026). Die Breitenrechnung in `sidebar_available_text_width` mit dem tatsächlich gezeichneten Platz der Treeview-Spalte abgleichen | ○ in der Sichtprüfung bestätigen (Prüfliste B1), dann Produktionsschnitt |
| W02 | `test_ui_updates` (Dunkelschleife) und `test_ui_polish36` setzen `theme_name` direkt; seit das Design die einzige Quelle ist, wirkt das nicht, die Dunkelfälle laufen hell. Auf `set_design` umstellen und auf Mac und Windows nachprüfen | ◐ 08.10.2026 umgestellt, Dunkelfall mit Luminanzprüfung belegt; Mac ✅ in den Volläufen 3.33.19–3.35.0, Windows offen; `releasedaten.py` ✅ 05.10.2026 |
| W03 | Zeilenenden in der Wurzel festlegen (`.gitattributes` mit `text=auto`, `-text` für `vendor` und Schriften auch in `07_Python-Versionen`). Bisher regelt nur `01_Repository/Glide` sie; Dateien aus der Windows-Arbeitskopie kamen beim Übernehmen in einen Linux-Klon mit CRLF ins Repository (3.33.8, vor dem Push bereinigt) | ✅ 08.10.2026: Wurzel-`.gitattributes`; zusätzlich Glide-Datenformate `-text`, weil eine Showcase-Vorlage mit CRLF ihr Manifest-SHA beim Commit verloren hätte; 215 Textdateien des Arbeitsstands auf LF normalisiert |
| W05 | Dialoge „Für KI bereitstellen“ (1705 px) und „Tabellenspalten“ (1317 px) unter Windows sehr breit, Knopfreihe links statt wie sonst rechts (Aufnahme 05.10.2026) | ✅ 3.33.21 auf dem Mac nachgestellt (1251/1504 px) und behoben (Textumbruch 460 px, Knöpfe rechts); Windows-Sichtprüfung B1a bestätigt |
| W06 | Auf 13 von 22 Fotos von „Neue Liste“/„Neuer Ordner“ fehlen Überschrift und Feldbeschriftungen (weiße Flächen); Aufnahmezeitpunkt oder echte Zeichenlücke der Leinwandbeschriftungen | ○ Sichtprüfung B1a; bei Bestätigung Produktionsschnitt, sonst Fotozeitpunkt in `test_fenster330` nach dem verzögerten Zeichnen |
| W07 | „PNG auf 128 × 128 einpassen“ nach „Ganzes Bild zeigen“: Hinweistext doppelt und überlagert | ◇ auf dem Mac nicht nachstellbar (3.33.21); Sichtprüfung B1a |
| W08 | „Pixelsymbol“: 16 × 16-Raster nur rund 60 px groß in großer leerer Fläche | ◇ auf dem Mac nicht nachstellbar (3.33.21); Sichtprüfung B1a |
| W09 | Einmaliger Absturz von Python 3.14.8 unter Windows in `attributpruefung` („Executing a cache“, 0xC0000409); 0 von 30 Wiederholungen | ◇ beobachten; bei Wiederholung mit Speicherauszug an CPython melden |
| W04 | Wächter in der CI-Grundstufe gegen Synchronisationskopien (Dateiname mit `-<Gerätename>` neben einem gleichnamigen Original) und gegen stark geschrumpfte Hauptdokumente ohne Vermerk | ✅ 08.10.2026: `synchronisationswaechter.py`, Schritt „Synchronisation“ der CI-Grundstufe, acht Werkzeugtests |

3.33.7 ist für den ersten G14-Schnitt verwendet. G29/G31/G32 sind mit 3.33.15 Windows/Python geprüft und geliefert. N07 und N08 bleiben Folgepakete ohne fest zugesagte Zielversion.

### 4.3 Ausbauprogramm Alltag, Komfort und Oberfläche

Auftrag des Inhabers vom 05.10.2026 (Wortlaut): „Mehr Features, Mehr Quality of Life Updates, Mehr Unterstützung im Alltag und eine modernere Oberfläche genau wie in der Konkurrenz Analyse beschrieben“; Umfang und Arbeitsdokument daran anpassen. Dieser Abschnitt ist die Planung dazu. Umgesetzt wird je Paket nach Auftrag; Status ○ heißt geplant.

**Grundlage:** [Markt und Vorbilder](Glide_Markt_und_Vorbilder.md):
- Abschnitt 1.1: Fertiger Tagesablauf (erfassen → machbaren Tag planen → arbeiten → abschließen). Heute, nächste Handlung und verfügbare Zeit erhalten den stärksten visuellen Rang.
- Abschnitt 1, Punkt 5: Es ist zu viel dauerhaft sichtbar.
- Abschnitt 3: TickTick schlägt Tagesaufgaben vor; Things setzt auf Feinschliff mit Schlummer-Intervallen und frühem Erledigen von Wiederholungen; Apple bietet Felder am Objekt und Erinnerungen in eigenen Worten; Super Productivity hat Fokus und Timeboxing; Sunsama hat ein Tagesritual.
- Abschnitt 6: abgeleitete Prioritäten.

**Regeln für jedes Paket:**
- Prinzipien-Check der [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md) bestehen: vorhandenen Weg erweitern statt einen zweiten bauen und benennen, was dafür verschwindet.
- D01/D02 gelten. Fachlogik entsteht als Tk-freies Modul mit Unit-Tests (D17).
- Keine neue Laufzeitabhängigkeit. Kein Formatwechsel, außer er ist ausdrücklich genannt.
- Aufwand ist geschätzt, nicht terminiert: S bis 1 Arbeitstag (AT), M 2–4 AT, L mehr als 4 AT.

**Bereits vorhanden, deshalb nicht neu geplant:** Tagesbeginn und Tagesabschluss, Wochenrückblick, Kapazität je Wochentag, Stundenraster, Jahres-Heatmap, Zeiterfassung, Schnelleingabe mit Feldchips und Wiederholungen, mehrzeiliges Einfügen in Listen (`paste_items_from_clipboard`), Seitenleiste ein-/ausblenden, Startseitendichte, Vorlagen mit Platzhaltern (einschließlich „Wochenplanung“), Fokusmodus der Pinnwand.

#### A. Moderne, ruhige Oberfläche

Vorbilder: Things (Feinschliff), Notion (Weißraum, Lesefluss), Apple („Felder am Objekt“). Lücken laut Analyse: zu viel dauerhaft sichtbar; Erscheinungsbild „wie System“ fehlt. Bereits geplant und Teil dieses Bereichs: UX1 (§4.1), N01/U17 „Automatisch (hell/dunkel)“, N05/U12 Inspektor, U15, U18, U09.

| ID | Paket | Nutzen | Abnahme (Auszug) | Aufwand | Stand |
|---|---|---|---|---|---|
| OB01 | Gestaltungsgrundlage: eine Skala für Abstände, Radien, Schriftgrößen und Zeilenhöhen als Tk-freies Modul. Sie ersetzt schrittweise Einzelwerte wie `PAD_X` oder `HOME_CARD_RADIUS`. | Einheitlicher Rhythmus; spätere Gestaltungsänderungen an einer Stelle | Erster Schnitt ohne sichtbare Änderung; Kontrast- und Mindestgrößenprüfung grün; Zahl der Abstandswerte je Ansicht gemessen | M | ◐ 3.33.12 erste Übernahme in Hauptfenster/Kopf und Karten-/Feldkonstanten; Startseite, Bibliothek, Einstellungen und Schnellerfassung ✅ 3.33.21 (OB01r, direkte Zahlen 134 → 3); native Abnahme offen |
| OB02 | Klare Hierarchie mit vier Textstufen (Ansichtstitel, Abschnitt, Text, Metadaten). Der Kopf von „Heute“ zeigt nächste Aufgabe, verfügbare Zeit und Fortschritt als stärkstes Element. | Analyse 1.1: Heute, nächste Handlung und verfügbare Zeit zuerst | 860 × 700 und große Schrift; jede Angabe genau einmal (Regel aus D12) | M | ○ nach OB01, U10, U19 und I7 |
| OB03 | Zeilenaktionen nur bei Bedarf: Einplanen, Termin und „…“ erscheinen in Listen-, Heute- und Tabellenzeilen beim Überfahren und bei Auswahl. Dauerhafte Zeilensymbole entfallen. | Weniger dauerhaft sichtbare Bedienung (UX1) | Jede Aktion auch über Tastatur (H-02), Kontextmenü und Befehlspalette; Ziel „Bedienfläche ≤ 15 %“ | M | ◐ Kalenderaktion mit KO01 in 3.33.13; Termin/… und weitere Gestaltung nach I7 offen |
| OB04 | Dezente Bewegung beim Abhaken, Auf- und Zuklappen und Bereichswechsel (≤ 150 ms), nur bei eingeschalteten Animationen | Zeitgemäßes, ruhiges Bediengefühl | Keine messbare Verschlechterung der Ziele aus §3; ohne Animation gleiches Ergebnis | M | ◇ Inhaberentscheidung, nach Stufe 0 |
| OB05 | Schmale Seitenleiste: eingeklappt nur Pixelsymbole und Systemzeilen, ausgeklappt wie bisher | Mehr Inhaltsfläche bei kleinen Fenstern | Zustand gemerkt; Tastatur; 860 × 700 | M | ✅ 3.33.21 |
| OB06 | Gestaltungsabnahme je Paket: Vorher-/Nachher-Fensterbilder bei 1280 × 800 und 860 × 700, hell und dunkel. Der Inhaber bewertet; die Bilder bleiben lokal und unversioniert. | Gestaltung wird abgenommen, nicht nur getestet | Entscheidung im QA-Bericht vermerkt | S je Paket | ◐ Bilder 3.33.12–3.33.14 lokal vorhanden; Inhaberbewertung offen |

#### B. Komfort im täglichen Gebrauch

Vorbilder: Todoist Quick Add, Things 3.23/3.24, Apple „Erinnerung in eigenen Worten“. Bereits geplant und Teil dieses Bereichs: U01, U03, U04, U07, U14, U16, H-02, N07.

| ID | Paket | Nutzen | Abnahme (Auszug) | Aufwand | Stand |
|---|---|---|---|---|---|
| KO01 | Ein Menü „Einplanen“ mit Heute, Morgen, Wochenende, Nächste Woche, Datum … und Ohne Tag. Es steht im Kontextmenü, in der Auswahlleiste, als Kürzel und als Zeilenaktion (OB03), wirkt auf die Mehrfachauswahl und setzt nur den Bearbeitungstag. | Umplanen ohne Dialog; ersetzt verstreute Einzelwege | Ein Undo-Schritt je Aktion; Fälligkeit bleibt; dieselbe Auswahl im Tagesbeginn | S–M | ◐ 3.33.13 Windows/Python geprüft und geliefert; Referenz-Mac/Bundle und menschliche Abnahme offen |
| KO02 | Wiederholungen: „Diesen Termin überspringen“ und vorzeitiges Erledigen ohne doppelten Folgetermin | Weniger Nacharbeit bei Routinen (Things 3.23) | Unit-Tests der Wiederholungslogik; die Serie bleibt erhalten | S | ✅ 3.33.20 |
| KO03 | Erinnerungen in der Schnelleingabe („erinnere 9 Uhr“, „30 min vorher“) als Chip; das Datenmodell ist vorhanden | Erinnerung gleich beim Erfassen (Todoist, Apple) | Chip rücknehmbar; der Chip nennt die Grenze „nur bei laufender App“ | S | ✅ 3.33.20 |
| KO04 | Felder am Objekt: Ein Klick auf Termin, Wichtigkeit oder Label einer Zeile öffnet die kleine Auswahl direkt dort | Weniger Masken (Apple, Analyse Abschnitt 3) | Ein Undo-Schritt; Tastatur; einheitlich mit dem Inspektor N05 | M | ○ zusammen mit N05 |
| KO05 | Mehrzeiliges Einfügen in die Eingabezeile legt nach Rückfrage je Zeile eine Aufgabe an. Es nutzt den vorhandenen Einfügeweg der Liste und den Parser je Zeile. | Schnelle Übernahme aus Mails und Notizen | Vorschau „N Aufgaben anlegen“; ein Undo-Schritt | S | ✅ 3.33.20 |
| KO06 | Zuletzt benutzte Ziele zuerst bei „Verschieben nach …“ und in der Labelauswahl | Weniger Suchen in großen Beständen | Keine neue Einstellung; Reihenfolge nur lokal | S | ✅ 3.33.20 |

#### C. Unterstützung im Alltag

Leitbild: Analyse 1.1. Vorbilder: TickTick 8.0 (vorgeschlagene Tagesaufgaben), Sunsama (Tagesritual), Super Productivity (Fokus, Timeboxing). Bereits geplant und Teil dieses Bereichs: G05, H-02, N04 mit B-03.

| ID | Paket | Nutzen | Abnahme (Auszug) | Aufwand | Stand |
|---|---|---|---|---|---|
| AU01 | Tagesvorschlag „Was passt heute?“: Im Tagesbeginn wählt Glide aus Verspätetem, heute oder bald Fälligem, Liegengebliebenem und Wichtigkeit so viel vor, wie in die freie Kapazität passt (Aufwand, sonst 30 Minuten). Jede Zeile nennt ihren Grund; Übernehmen mit einem Klick. | Ein machbarer Tag ohne Grübeln und ohne Cloud-KI | Tk-freies Modul mit Unit-Tests; deterministisch; nichts ändert sich ohne Bestätigung; Fälligkeit unverändert; ein Undo-Schritt | M | ◐ 3.33.14 umgesetzt und gezielt Windows-geprüft; Windows-Gesamtprüfung und Python-Lieferung grün; strenge CI Exit 0 (17 Schritte, 24 Werkzeugtests), native/menschliche Abnahme offen |
| AU02 | Verfügbare Zeit überall beim Planen: Tagesbeginn, Ziehen auf einen Tag, „Einplanen“ (KO01) und der Kopf von „Heute“ zeigen z. B. „frei heute 1 h 20 min“ und benennen Überplanung | Planung sieht die Kapazität | Eine Rechenstelle (`planning_summary`); benennen, nicht verhindern | S–M | ◐ 3.33.13 Windows/Python geprüft und geliefert; Referenz-Mac/Bundle und menschliche Abnahme offen |
| AU03 | Geführter Tagesbeginn in drei Schritten (Rückblick → Vorschlag AU01 → Zeitblöcke im Raster), dazu ein optionaler Hinweis zu Tagesbeginn und Tagesabschluss zur festen Uhrzeit, solange die App läuft | Tagesritual ohne Einrichtung | Vorgabe des Hinweises: Inhaberentscheidung; Systemmitteilung nur über die vorhandene Option | M | ◐ Geführter Rückblick → Vorschlag → Raster 3.33.14; automatische Hinweise/Vorgabe offen |
| AU04 | Wochenplanung im eingebetteten Kalender (N04): Woche mit Kapazitätsbalken je Tag; Ziehen setzt den Bearbeitungstag (D02); Übernahme aus dem Wochenrückblick | Die Woche einmal planen statt täglich zu suchen | Teil von N04, kein zweiter Kalender | M | ◐ 3.33.17 Windows/Python geprüft und geliefert; native/menschliche Abnahme offen |
| AU05 | Fokussitzung (= G05) mit der nächsten Aufgabe aus „Heute“, Pausenhinweis und direktem Wechsel zur nächsten Aufgabe nach dem Abhaken | Arbeiten statt Umschalten | Abnahme von G05: Zeit genau einmal gebucht | M | ◐ 3.33.14 umgesetzt = G05; Windows-Gesamtprüfung und Python-Lieferung grün; strenge CI Exit 0 (17 Schritte, 24 Werkzeugtests), native/menschliche Abnahme offen |
| AU06 | Routinen: wiederkehrende Checklisten (Morgen, Abend, Wochenabschluss) erscheinen als eigener Abschnitt in „Heute“, ohne Gewohnheitsstatistik | Alltagsroutinen sichtbar ohne neues Datenmodell | Nutzt die vorhandene wiederkehrende Checkliste; kein Formatwechsel | M | ✅ 3.33.20 (ersetzt die Prüfung von G06) |
| AU07 | Termine als belegte Zeit: Eine Kalenderdatei (ICS) wird nur gelesen und im Stundenraster als belegt gezeigt, ohne Aufgaben anzulegen | Realistische Kapazität an Besprechungstagen | Berührt die Produktgrenze „ICS ist Dateiaustausch“ und braucht voraussichtlich ein Datenfeld | M–L | ◇ Inhaberentscheidung |

#### D. Funktionsausbau

Die größten Lücken laut Analyse (Abschnitt 1, Punkt 3) sind bereits geplant; dafür gibt es keine neuen Kennungen. Neu ist nur die Zuordnung:
- G29/G31/G32 (Aufgaben im Text)
- G08/G30 (Verweise mit Rückverweisen), mit „@“ als Eingabeweg wie bei Notion und Rückverweisen wie bei Obsidian
- G28 (Live-Liste)
- G09 (Titelbild)
- N04 (Kalender eingebettet) mit AU04
- G14 (FTS5 nach Messung)
- U08 (Vorlagen im Anlegen-Weg)

Die Stufen 3–4 (Pixel, G24, G21, F-03, G26) bleiben unverändert.

#### Reihenfolge in Wellen

Reservierungen, keine Termine. Die beauftragte Kernfolge bleibt: Aktionskennungen → UX1 → G05/H-02 → G29/G31/G32. Neue Pakete werden dort eingehängt, wo sie dieselbe Codestelle berühren; der Auftrag vom 07.10.2026 beauftragt größere Umsetzungspakete und ihre Folgeplanung (§4.4). Offene Produktentscheidungen bleiben vorbehalten.

| Welle | Inhalt | Begründung |
|---|---|---|
| 0 | P08a/P09b/P08b mit 3.33.9–3.33.11 Windows/Python geprüft und geliefert | Fundament zuerst (Rangfolge der Säulen); weitere Optimierungen nach Messung |
| 1 Komfort und Tag (3.33.x) | Aktionskennungen → U03/U07/U10/U19 und OB01 → KO01 mit AU02 → AU01 → G05/AU05 mit H-02 → G29/G31/G32; KO02, KO03, KO05, KO06 als kleine Schnitte dazwischen | Größter Alltagsnutzen; Aufgabenverweise G29/G31/G32 verwenden das abgesicherte Format 21 |
| 2 Moderne Oberfläche (3.33.x/3.34.0) | Bedienkomfort U01/U02/U13/U14/U16/U22/U24 mit 3.33.16 geliefert. Nach I7: OB02 → OB03 → N05 mit KO04 → N01/U17; automatische Tageshinweise AU03 offen | Sichtbarer Modernisierungsschritt auf Grundlage der Referenzentwürfe |
| 3 Wissen und Woche (seit 3.33.17) | G08/G30 und N04/AU04 in 3.33.17 mit Format 22 Windows/Python geprüft und geliefert; G28/G09/U08 mit 3.33.18 ebenfalls Windows/Python geprüft und geliefert | Wissen im Kontext; native/menschliche Abnahme offen |
| Später | OB04, OB05, AU06, AU07; Stufen 3–4 | Entscheidung oder Auslöser offen |

**Fertig (Programm), wenn:**
- Ein Tag lässt sich aus „Heute“ in höchstens drei Schritten planen: Tagesbeginn → Vorschlag übernehmen → Zeitblöcke.
- Die verfügbare Zeit ist überall sichtbar, wo geplant wird.
- Die Oberflächenziele aus §10 sind erreicht.
- Der Inhaber hat jede Welle gestalterisch abgenommen (OB06).

### 4.4 Größere Umsetzungspakete (Auftrag 07.10.2026)

Der Inhaber beauftragt mehrere zusammengehörige Features je Umsetzung, abgeleitet aus den abgelegten Analyse-, Recherche- und Konkurrenzdokumenten. Umfangreiche Prüfung bleibt verbindlich. Die folgende Paketfolge ersetzt die bisherige Abfolge einzelner Produktionsschnitte; es braucht innerhalb dieses Auftrags keine erneute Freigabe jeder Teilfunktion. Offene Produktentscheidungen bleiben offen.

| Reihenfolge | Paket und Ergebnis | Bestandteile und Herkunft | Abhängigkeiten / Stand |
|---|---|---|---|
| Geliefert | **Den Tag planen und fokussiert abarbeiten:** vom begründeten Tagesvorschlag über Zeitblöcke zur nächsten Aufgabe | AU01; geführter Weg AU03 ohne automatische Hinweise; G05/AU05; H-02 für Zeitblöcke. Analyse §1.1, Ausbauprogramm §4.3 C, Markt §6: Sunsama-Tagesplanung und Super-Productivity-Fokus | ◐ 3.33.14 umgesetzt, Paketprüfung grün; Windows-Gesamtprüfung und Python-Lieferung grün; strenge CI Exit 0 (17 Schritte, 24 Werkzeugtests). Format 20, keine neue Abhängigkeit |
| Geliefert | **Aufgaben im Wissen:** Aufgaben im Notiztext, aus Seiten in Listen übernehmen und wiederfinden | G29/G31/G32; Referenz-/Löschregeln D05/Q5. Markt §2/§6: Notion, Obsidian, AFFiNE | ◐ 3.33.15 umgesetzt; 153 Unit-Tests/Paketprüfung grün; Format 21 mit Vorsicherung/Vorversionsprobe. Windows-Gesamtprüfung und Python-/Showcase-Lieferung grün; strenge CI Exit 0 (17 Schritte); native/menschliche Abnahme offen |
| Geliefert | **Weniger Bedienung, mehr Inhalt:** gemeinsame Palette, einklappbare Hinweise, sichtbarer Bearbeitungstag und konsistente Begriffe | U01/U02/U13/U14/U16/U22/U24, auf Aktionskennungen und OB01 aufbauen; Analyse §1/§4 und Prinzipien P1–P6 | ◐ 3.33.16 Windows/Python geprüft und geliefert; größere visuelle Umbauten OB02/OB03/N05 mit KO04 weiterhin nach I7 |
| Geliefert | **Wissen und Woche:** eingebetteter Kalender mit Wochenkapazität sowie Verweise und Rückverweise | N04/AU04, G08/G30; Markt §4–§6. G28/G09/U08 sind mit 3.33.18 als eigenes Paket geliefert | ◐ 3.33.17 Windows/Python geprüft und geliefert; Format 22 mit bytegenauer Vorsicherung und Vorversionsschutz; native/menschliche Abnahme offen |
| Geliefert | **Seiten im Alltag:** Originalaufgaben als Live-Liste, Titelbild und gefüllte Vorlagenvorschau | G28/G09/U08; allgemeine Verweis-/Import-/Löschregeln gemeinsam | ◐ 3.33.18 Windows/Python geprüft und geliefert; Format 23; native/menschliche Abnahme offen |

**Prüfstrategie pro Paket:** Die grüne Vollprüfung des Ausgangsstands bleibt ihr eigener Nachweis. Vor Produktionsänderungen gezielte Baselines der betroffenen Bereiche; während der Umsetzung Unit-Tests und echte Bedienwege je Teilfunktion. Danach ein gemeinsamer eingefrorener Paketstand mit vollständiger Regression, Interaktions-/Fehler-/Undo-/Neustartprüfung, Mindestgröße/großer Schrift/hell/dunkel sowie Messung. Erst nach grüner Gesamtprüfung Python/Showcase synchronisieren und strenge CI ausführen. Weitere Vollläufe nur nach ausführbaren Änderungen oder einem tatsächlichen Fehlerbefund. Teilfunktionen erhalten keine künstlichen Zwischenversionen. Native und menschliche Abnahme werden getrennt ausgewiesen.

**Umfang des ersten Pakets:** Tagesvorschläge bleiben erklärbar, deterministisch und bestätigen jede Bestandsänderung. Fehlende Schätzung verwendet ausschließlich für die Auswahl 30 Minuten; Kapazität 0 bleibt unbekannt. Vorschau vor Übernahme auf Tageswechsel, Kapazität und stabile Quellkennungen prüfen. Fokus nutzt dieselbe eine Zeiterfassung; Pausen zählen nicht, Zeit wird auch nach Wechsel und Neustart genau einmal gebucht. Zeitblöcke erhalten einen Tastaturweg mit sichtbarem Datum/Uhrzeit und einem Undo-Schritt. Die Vorgabe automatischer Tageshinweise (AU03) bleibt eine Inhaberentscheidung; H-02 für Pinnwand und Seitenbäume folgt in deren passenden Paketen.


**Geliefertes Paket 3.33.15 – Aufgaben im Wissen (G29/G31/G32):** Ein vorhandener Aufgabenpunkt lässt sich im Notiz-/Seitentext über dieselbe Kennung verwenden; eine Seitenaufgabe kann in eine Liste übernommen werden und der Textverweis bleibt erhalten. „Aus Seiten“ findet solche Aufgaben in vorhandenen Ansichten. Gemeinsam abnehmen: Verschieben und Umbenennen erhalten die Verbindung; Abhaken bleibt über beide Wege konsistent; fehlende bzw. im Papierkorb liegende Ziele sind erkennbar; Import remappt Kennungen; Rücknahme und Neustart erhalten den Zusammenhang. Die Regeln sind im Tk-freien Modul `task_references.py` konkretisiert. Format 21 schützt diese Aufgabenverweise; allgemeine Objektverweise G08/G30 folgen als eigenes Paket 3.33.17 mit Format 22. Windows-Vollprüfung Exit 0: 92 Schritte, 73 Integrationssuiten, 153 Unit-Tests; 354 eingefrorene Dateien unverändert. 24 Code-Dateien/131 Ressourcen/Showcase bytegleich, direkte Lieferprobe und 22 Modulimporte grün. Strenge CI Exit 0 (17 Schritte). Native und menschliche Abnahme offen.

**Geliefertes Paket 3.33.16 – Weniger Bedienung, mehr Inhalt (U01/U02/U13/U14/U16/U22/U24):** Suche und Aktionen in einer Palette bündeln, Hinweise einklappbar machen, Bibliothekswege vereinheitlichen, Menüaktionen passend platzieren, Bearbeitungstag sichtbar machen und Begriffe/Symbole konsistent führen. Gemeinsame Abnahme: bestehende Aktionen über Tastatur, Menü und Palette weiterhin erreichbar; Editorfokus erhalten; Auswahllogik, Undo und gemerkte Anzeigezustände intakt; Mindestfenster/große Schrift/hell/dunkel; weniger dauerhaft belegte Bedienfläche. Die Gestaltung übernimmt vorhandene Rollen und OB01. Neue Referenzgestaltung für OB02/OB03/N05 bleibt von I7 abhängig. Windows-/Python-Vollprüfung und Lieferung grün; native/menschliche Abnahme offen.

**Geliefertes Paket 3.33.17 – Wissen und Woche (N04/AU04, G08/G30):** Eingebettete Wochen-/Monatsansicht auf derselben Planungsbilanz, Tastatur-/Mausplanung mit getrenntem Bearbeitungstag und Verbindung zum Wochenrückblick. Bestätigte Zeitfenster aus vorhandenen Glide-Blöcken; allgemeine lokale Seiten-/Listen-/Aufgabenverweise mit @ und abgeleiteten Rückverweisen. Format 22, bytegenaue Vorsicherung, unveränderte 3.33.16 schreibgeschützt; Import/Kopie/Papierkorb/Undo/Neustart und Speicherfehler geprüft. Windows/Python-Vollprüfung, Python-/Showcase-Lieferung und strenge CI grün; native/menschliche Abnahme offen. G28/G09/U08 sind mit 3.33.18 als eigene Etappe Windows/Python geprüft und geliefert; AU07 und automatische Tageshinweise bleiben offen.

**Geliefertes Paket 3.33.18 – Seiten im Alltag (G28/G09/U08):** Live-Listen mit Originalaufgaben, Titelbilder aus lokalen Anhängen oder übernommenen Pixelzeichnungen und gefüllte Vorlagenvorschau im Anlegen-Weg. Format 23 mit bytegenauer Vorsicherung und unveränderter 3.33.17 schreibgeschützt. Windows-Vollprüfung Exit 0: 95 Schritte, 76 Integrationssuiten, 170 Unit-Tests; 365 eingefrorene Dateien unverändert. 28 Code-Dateien, 131 Ressourcen und sechs Showcase-Dateien bytegleich; drei direkte Lieferproben und 26 Modulimporte grün. Strenge CI Exit 0 (17 Schritte, 25 Werkzeugtests). Native Mac-/Linux-, Bundle- und menschliche Abnahme offen.

## 5. Wissen im Kontext (Stufe 2, seit 3.33.17; weiterer Ausbau 3.34.x)

| ID | Arbeit | Stand |
|---|---|---|
| N05 = U12 | Ein Inspektor statt Maske + Detailbereich | ○ |
| U18 | Seitentitel im Dokument, Platzhalter „Schreiben oder „/“ für Blöcke“ | ✅ 3.33.21 |
| U15 | Lila nur für Hinzufügen; aktiver Zustand neutral | ✅ 3.33.21 (neutrale Rolle `active`) |
| U08 = E-03 | Vorlagen im Anlegen-Weg, gefüllte Vorschau vor dem Anlegen | ◐ 3.33.18 Windows/Python geprüft und geliefert; native/menschliche Abnahme offen |
| G14 = D-01 | Inhaltssuche in Strg/Cmd+O, danach optionaler FTS5-Cache und eine Befehlspalette | ✅ 3.34.0: Inhaltssuche 3.33.7, gemeinsame Palette 3.33.16, Hervorhebung im Dokument 3.34.0 (G14h); FTS5 nach Messung nicht nötig (P07 ✕) |
| D-03 | Erklären, warum ein Filter einen Punkt zeigt oder ausblendet | ✅ 3.34.0 (gespeicherte Filter) |
| G08/G30 = D-02 | Seiten-, Listen- und Aufgabenverweise mit Rückverweisen; **eigenes Datenformat-Tor** (Altleser nur lesend; Format 21 enthält bereits Aufgabenverweise) | ◐ 3.33.17 Windows/Python geprüft und geliefert; native/menschliche Abnahme offen |
| G28 = E-01 | Live-Liste in einer Seite (Originalaufgaben, keine Kopien) | ◐ 3.33.18 Windows/Python geprüft und geliefert; native/menschliche Abnahme offen |
| G09 = E-02 | Titelbild für Seiten und Bibliothekskarten, auch als Pixelzeichnung | ◐ 3.33.18 Windows/Python geprüft und geliefert; native/menschliche Abnahme offen |
| N04 = U11 + B-03 | Kalender als eingebettete Ansicht, Ziehen auf Tage (D02), freie Zeitfenster vorschlagen | ◐ 3.33.17 Windows/Python geprüft und geliefert; native/menschliche Abnahme offen |
| U09 | Kompakte Pinnwandleiste | ✅ 3.33.21 |
| B4 | Bilder in Seiten: Überlappung verhindern, Bilder in Druck/PDF und Markdown | ✅ 3.34.0 |

**Fertig, wenn:** Suche findet Wörter in Seiten-, Notiz- und Beschreibungstext, fehlender Index wird neu aufgebaut; Umbenennen, Verschieben, Papierkorb und Import erhalten Verweise, „Ziel fehlt“ ist sichtbar; ältere Fassungen öffnen den dann neuen Bestand nur lesend; Kalender ohne modales Fenster.

## 6. Pixel, Austausch, Verteilung (Stufen 3–4)

| ID | Arbeit | Stand |
|---|---|---|
| G19 = G-01 | Paletteneintrag ändern färbt die Zeichnung um, mit Undo (indizierter Kern vorhanden) | ✅ 3.35.0 |
| G-03 | Symbolvorschau in 16/32/48 px vor dem Export | ✅ 3.35.0 |
| G17 = G-02 | Animation: Frames, Dauer, Vorschau; **D07 offen** (abspielbares GIF oder zunächst Frames/Vorschau/Spritesheet; Empfehlung: zuerst Spritesheet) | ○ |
| G24 = F-01 | KI-Austausch Stufe 2 über Dokumente: Kontextpaket, Markdown/Felder, Änderungsvorschläge mit Feldvergleich (Q3) | ✅ 3.35.0 |
| G21 = F-02 | Begrenzter Import (zuerst eine Quelle: Notion-Markdown/ZIP oder Todoist-CSV – Inhaberentscheidung; Empfehlung: Notion als Vorbild des Inhabers) mit Verlustbericht | ○ |
| F-03 | Zwei Sicherungsstände lesbar vergleichen, ohne Schreibzugriff | ✅ 3.35.0 |
| G26 = H-03 = N11 | Paket mit eingebettetem Python 3.14 + Tk 9 je Plattform (D15); Bauwerkzeug als eigene Abhängigkeitsentscheidung (Vorschlag PyInstaller ≥ 6.22) | ○ |
| – | Windows-/Linux-Abnahme, Linux-App (AppImage/Flatpak später) | ○ Inhaber |
| H-01 | Kontrollmatrix echter Bedienwege fortführen | laufend |

## 7. Zukunft und bewusst nicht

| ID | Thema | Marke | Grund / Auslöser |
|---|---|---|---|
| N12 = U23 | Screenreader und beschriftete Canvas-Bedienung über Tk 9.1 `tk accessible` | ◇ | Tk 9.1.0 ist erschienen (29.09.2026); Voraussetzung G26 und eigene Abnahme |
| N13 | Seitenversionen wiederherstellen | ◇ | nach F-03 |
| – | SQLite als Hauptspeicher | ◇ | nur bei realen Beständen über 20.000 Punkten (D16) |
| G25, Mobile | Toolkit-Probe, iPhone/iPad | ◇ | D03 aufheben |
| G18, G15, G10 | Kachelsatz, Filter in Alltagssprache, Registerkarten-Block | ◇ | Vorrat |
| G06 | Gewohnheiten | ◇ | vorerst nicht; nach G05 als Routinen in „Heute“ (AU06, §4.3) neu bewerten |
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
- **Datenformat-Tore:** Format 21 (Aufgabenverweise, 3.33.15), 22 (allgemeine Verweise, 3.33.17) und 23 (Live-Listen/Titelbild, 3.33.18) sind vergeben. Der nächste inkompatible Inhalt (etwa Animation G17) bekommt die nächste freie Nummer, mit Vorsicherung, Migration und schreibgeschütztem Altleser.
- UX1 vor Zusammenführung der Befehlspalette und dem FTS5-Ausbau; die erste Inhaltssuche in Strg/Cmd+O benötigt weder Menüumbau noch Index; P08a vor P08b; D07 vor G17; G24 vor G21; D15 vor G26 vor N12.

## 9. Risiken

| Nr. | Risiko | Gegenmaßnahme |
|---|---|---|
| R1 | Regressionen in der Klasse `ListApp` (rund 54.500 Zeilen in `app.pyw`) | kleine Schnitte, echte Bedienproben, Vollprüfung je Schnitt, Fachlogik als Tk-freies Modul (D17) |
| R2 | Beschriftungs- oder Positionswechsel darf die falsche Aktion nicht auslösen | seit 3.33.11 stabile Aktionskennungen; alte Suchtreffer erneut über ID auflösen, Editorfokus und Erreichbarkeit prüfen |
| R3 | Neue Dokumentinhalte gehen in älteren Fassungen verloren | Datenformat-Tor 21 |
| R4 | P08b übersieht einen Änderungsweg | Vollvergleich im Autosave, Differenztest |
| R5 | Aktueller Plattform-/Liefernachweis offen | Windows-Gesamtprüfung und Python-Lieferung bis 3.33.18 grün; seit 08.10.2026 automatische Vollprüfung und Bundlebau auf dem Referenz-Mac (Sprint, Abschnitt 15). Linux und menschliche Prüfliste bleiben eigene Tore, D15. Der Arbeitsstand 3.33.9–3.33.18 ist noch nicht eingecheckt; vor einem Upload CI-Grundstufe einschließlich Synchronisation und Ablagegröße |
| R7 | Umfang wächst | Klassifizierung, Prinzipien-Check mit Vorgeschichte |
| R9 | Gewohnheitsbruch durch D10/D12/D14 | Bestandseinstellungen bleiben; N07 |
| R10 | Namenskollision „Glide“ | Markenprüfung durch den Inhaber |
| R11 | Linux-Messungen nicht auf den Mac übertragbar | Abnahme auf dem Referenz-Mac |
| R12 | Gestaltungsumbau ohne Referenzentwurf erzeugt Nacharbeit | I7 vor OB02/OB03; Gestaltungsabnahme OB06 je Welle |
| R13 | Tagesvorschläge wirken bevormundend oder unpassend | AU01 schlägt nur vor, nennt je Zeile den Grund, ändert nichts ohne Bestätigung und wird freiwillig aufgerufen |
| R14 | Mehr Funktionen in der ohnehin großen `ListApp` | Neue Fachlogik nur als Tk-freies Modul (D17), zusammengehörige Pakete in Wellenreihenfolge, je Paket „was verschwindet dafür“ |

## 10. Messbare Ziele

| Bereich | Ziel | Stand (Beleg) |
|---|---|---|
| Abhaken 1.000 / 5.000 / 10.000 Punkte | ≤ 50 / 120 / 200 ms | 56 / 218 / 446 ms (Linux, Python 3.14, Median) |
| Erstes Speichern, 10 MB | ≤ Folgespeichern + 50 ms | ✅ ohne Zusatz-Parse seit 3.33.0 |
| Startseite aufbauen | ≤ 150 ms | 507 ms (macOS, 1.000 Punkte, 3.33.2) |
| Tabellenansicht öffnen, 5.000 Punkte | ≤ 400 ms | 2.671 → 292 ms in der Messung zu T8 (Linux); P09a seit 3.33.0, danach nicht erneut als Ganzes gemessen |
| Kopfzeilen-Symbolknöpfe | ≤ 4 | ✅ ≤ 4 seit 3.33.16 (Einstellungen, Erfassen, Suche, Seitenleiste; Glocke und Zeitanzeige nur bei Bedarf; Code `pack_header_controls`, Analyse A02) |
| Bedienfläche über Inhalt (Liste, 1280 × 840) | ≤ 15 % | ≈ 27 % |
| Startseitenkacheln im Standard | 7 (D12) | ✅ 7 seit 3.33.2 |
| Symbole mit mehreren Bedeutungen | 0 (Bewegungspfeile ausgenommen) | ✅ 0 seit 3.33.16 (doppelt nur ▲/▼ für Verschieben und Sortieren; Auszählung `ICONS` 08.10.2026) |
| Tag aus „Heute“ planen (Tagesbeginn → Vorschlag → Zeitblöcke) | ≤ 3 Schritte | ◐ geführter Weg 3.33.14 umgesetzt und Windows-geprüft; reale Klick-/Zeitmessung und menschliche Abnahme offen |
| Verfügbare Zeit beim Einplanen sichtbar | in allen Planungswegen (Tagesbeginn, Ziehen auf Tag, Einplanen, Kopf von Heute) | ◐ 3.33.13 alle vier Planungswege Windows-automatisch geprüft; native und menschliche Abnahme offen |
| Abstandswerte in den Hauptansichten | nur Werte der Skala aus OB01 | Ausgangswert vor OB01 messen |

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
| I5 | Aktuelles Python auf dem Mac installieren | ◐ Der Referenz-Mac hat Python 3.14.5 mit Tk 9.0.3; damit läuft seit 08.10.2026 die native automatische Vollprüfung. python.org führt seit 30.09.2026 3.14.8 (Windows-Absturz W09 beobachten); Installation braucht das Passwort des Inhabers |
| I6 | Windows-Vollprüfung und manuelle Prüfsitzungen | ◐ 3.33.15 Windows-Gesamtprüfung Exit 0 (92 Schritte, 73 Integrationssuiten, 153 Unit-Tests, Python 3.14.7/Tk 9.0.4), Python/Showcase ausgeliefert; strenge CI Exit 0 (17 Schritte). Referenz-Mac/Bundle und menschliche Sicht-/Bedienabnahme B1a–B1e, B2–B13, C ○ [Prüfliste](Glide_Manuelle_Pruefung.md) |
| – | Erste Importquelle für G21, Bauwerkzeug für G26 | ○ erst in Stufe 4 |
| I8 | Lösungsweg für das Logo unter Tk 8.6: Rückfall glätten (LG01), App-Symbol vorrechnen (LG02), Prüfung schärfen (LG03), Master überarbeiten (LG04); Weg A (Python 3.14/Tk 9) gilt bisher nur für die Windows-Prüflaufzeit | ○ [Diagnose, Abschnitt 7](../01_Repository/Glide/docs/diagnosen/LOGO_KANTENGLAETTUNG.md#7-lösungswege) |
| I7 | Referenzentwürfe für „Heute“, Liste und Seite (Affinity) als Gestaltungsrichtung für OB02/OB03 | ○ vor Welle 2 (§4.3) |
| I9 | Rechte an Fremdbildern (Bildagenturen, Webquellen) im öffentlichen Repository prüfen: `20_Grafik_Master/05_Inspiration`, `06_Beispielbilder` und die sechs von dort übernommenen Showcase-Motive (`tests/fixtures/showcase/bilder`, eingebettet auch in beiden `Glide-Showcase.glidebackup`) | ○ behalten mit Rechtenachweis oder entfernen und den Showcase mit eigenen Motiven neu erzeugen; Empfehlung: ohne Nachweis entfernen |
| I10 | Git-Historie bereinigen (gelöschte Protokolle mit Benutzerpfaden, frühere Archivkopien) | ○ eigener Auftrag; ändert alle Commit-Kennungen ([Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md#github-auftritt)) |
| I11 | GitHub-Auftritt: Beschreibung, Tags, Wiki, Issues, KI-Codeprüfung | ○ Empfehlungen in der [Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md#github-auftritt) |
| – | Ausbauprogramm: Vorgabe des Hinweises zu Tagesbeginn/-abschluss (AU03), dezente Bewegung (OB04), Termine als belegte Zeit (AU07, berührt eine Produktgrenze) | ○ wenn das jeweilige Paket ansteht |

**Auswahl A–H** (Aufgabenauswahl vom 30.09.2026): A Tempo und Stabilität · B Planen und Fokus · C Aufgaben im Text · D Suchen und Wissen · E Projektseiten · F Austausch und Sicherungen · G Pixel-Werkstatt · H Bedienkontrolle und Auslieferung. Die Aufgaben A-01 bis H-03 stehen mit Status in den Abschnitten oben. Bearbeitungstiefe je Richtung oder Aufgabe: recherchieren, Umsetzung vorbereiten, kleinen Teil umsetzen, später oder nicht verfolgen; „umsetzen“ meint nur den beschriebenen kleinen Schnitt samt Prüfung und Auslieferung.

## 12. Zukunftsperspektive und nächste Umsetzung (05.10.2026)

**Entscheidungsgrundlage:** [Markt und Vorbilder](Glide_Markt_und_Vorbilder.md#6-verifizierter-abgleich-und-konsequenzen-05102026), aktueller Code und isolierte Windows-Baseline. Die breite Produktmatrix ist keine vollständige neue Herstellerprüfung. Es liegen keine Nutzungsdaten vor; Prioritäten folgen konkreter Funktionslücke, vorhandener Entscheidung, Aufwand und Regressionsrisiko, nicht erfundenen RICE-Zahlen.

| Reihenfolge | Paket / Nutzen | Abhängigkeit und Abnahme | Status |
|---|---|---|---|
| Jetzt | G14 erste Stufe: vorhandene Inhalte wiederfinden; Windows-Formatsicherung korrigieren | Kein Formatwechsel, keine neue Laufzeitabhängigkeit; Inhalte/IDs/Archiv/Neustart, Differenz zur Vorversion | seit 3.33.7 implementiert, mit 3.33.8 Python-Lieferung; Grenzen im QA-Bericht |
| Prüftor/Lieferung | Windows-Gesamtabnahme 3.33.8 und 07-Abgleich; Referenz-Mac/Bundle separat | Veraltete Testannahmen korrigiert; Titel-/Mindesthöhen-/Editor-Timerbefunde und übersehene Formatwechsel bei identischen Dateimetadaten behoben. 66 Integrationssuiten/75 Unit-Tests grün, 07/Showcase SHA-256-abgeglichen | ◐ Windows/Python-Lieferung erledigt; Referenz-Mac/Bundle und menschliche Abnahme offen |
| Performance-Fortsetzung 3.33.11 | P08b: geprüfte lokale Listen vergleichen, Autosave vollständig | 49 Mutationseinstiege abgeglichen: 22 lokale, 27 Vollvergleich; 120 Differenzfälle, Fehler/Retry/Autosave/Undo/Reload grün | ◐ 3.33.11 Windows/Python geprüft und geliefert, native/menschliche Abnahme offen |
| Aktueller UX1-Schnitt | U10/U19 und OB01 Gestaltungsgrundlage | 3.33.12: Titel vor Kennzahlen, Heute-Titel vor Quelle; OB01 übernimmt vorhandene Zahlen. 70 Integrationssuiten/109 Unit-Tests, Vollprüfung und strenge CI grün; Python/Showcase bytegleich | ◐ Windows/Python geliefert; weitere OB01-Übernahmen, OB06/I6 und Referenz-Mac/Bundle offen |
| Geliefertes Produktionspaket | Den Tag planen und fokussiert abarbeiten: AU01, geführter AU03-Weg, G05/AU05, Raster-H-02 (§4.4) | Erklärbares Budget, Vorschau vor Mutation, Zeitblöcke mit Tastatur, Fokus/Pause/Wechsel und genau einmal gebuchte Zeit; 137 Unit-Tests und Paketprüfung grün | ◐ 3.33.14 umgesetzt; Windows-Gesamtprüfung und Python-Lieferung grün; strenge CI Exit 0 (17 Schritte, 24 Werkzeugtests), native/menschliche Abnahme offen |
| Geliefertes Produktionspaket | Aufgaben im Wissen: G29/G31/G32 (§4.4) | Echte Aufgaben, gemeinsame IDs, Heimatwechsel und Textquellen; Format 21 mit Vorsicherung/Vorversionsschutz, 153 Unit-Tests und Paketprüfung grün | ◐ 3.33.15 umgesetzt; Windows-Gesamtprüfung und Python-/Showcase-Lieferung grün; strenge CI Exit 0 (17 Schritte), native/menschliche Abnahme offen |
| Geliefert | Bedienkomfort: U01/U02/U13/U14/U16/U22/U24 (§4.4) | Zusammengehörige Auswahl-/Tastatur-/Dialogwege, gemeinsame Abnahme; vorhandene Oberfläche bewahren | ◐ 3.33.16 Windows/Python geprüft und geliefert; native/menschliche Abnahme offen |
| Geliefert | Wochenplanung N04/AU04 und Rückverweise G08/G30 (§4.4) | Vor neuen inkompatiblen Beziehungen eigenes Formattor, Vorsicherung und Vorversionsprobe; Referenz-/Import-/Undo-/Löschregeln gemeinsam | ◐ 3.33.17, Format 22; Windows/Python geprüft und geliefert; native/menschliche Abnahme offen |
| Geliefert | Seiten im Alltag G28/G09/U08 (§4.4) | Original-IDs, Anhänge, vorbereitete Termine, ein Undo und Formatprüfung 23 gemeinsam geprüft | ◐ 3.33.18 Windows/Python geprüft und geliefert; native/menschliche Abnahme offen |
| Nach I7 | Welle 2 „Moderne Oberfläche“: OB02, OB03, N05 mit KO04, N01/U17 und automatische AU03-Hinweise (§4.3); U01 ist seit 3.33.16 geliefert | Gestaltungsabnahme durch den Inhaber je Paket (OB06); Oberflächenziele aus §10 | ○ geplant |
| Nach Messung | G14 FTS5-Ausbau | Nur bei gemessener Suchlatenz; Index vollständig ersetzbar, Öffnen ohne Index, keine SQLite-Hauptablage | ○ geplant |
| Später | Pixel/Animation, Austausch und Paketierung | D07, erste Importquelle, Bauwerkzeug separat; Paketierung vor Screenreader-Abnahme | ◇ an bestehende Entscheidungen gebunden |

**Vertrag KO01/AU02 (umgesetzt in 3.33.13):** Vorhandene Planungswege als Baseline aufgenommen, Gegenprobe gegen 3.33.12 rot. `planning_summary` zählt fehlende Schätzungen getrennt, erhält erledigte Schätzungen in der Tagesbilanz und liefert bei Kapazität 0 keinen freien Rest; diese Regeln sind im Tk-freien `planning.py` nach D17 erhalten. Der bestehende Auswahldialog erlaubt nur Listenansichten. „Heute“ verwendet stabile Quelllisten-/Punktkennungen; Mehrfachauswahl über mehrere Listen wirkt mit einem Undo-Schritt, ohne die allgemeine Listenvoraussetzung aufzuweichen. Fälligkeit, Aufwand und Uhrzeit dürfen durch das reine Einplanen nicht mitgeändert werden. Die verfügbare Zeit muss sich überall auf denselben Zieltag und dieselbe Bilanz beziehen.

**Vertrag AU01 (3.33.14):** Auf der gemeinsamen Zieltagbilanz aus KO01/AU02 aufbauen. Bereits für heute eingeplante Aufgaben einschließlich erledigter Schätzungen belegen Kapazität und werden nicht doppelt vorgeschlagen. Der im Paket vorgesehene 30-Minuten-Ersatz bei fehlender Schätzung ist nur eine deutlich benannte Auswahlannahme; `estimated_minutes` bleibt leer und AU02 rät weiterhin keinen Aufwand. Kapazität 0 bleibt unbekannt und darf keinen angeblich passenden freien Rest ergeben. Gründe, stabile Kennungen und deterministische Reihenfolge vor der Übernahme zeigen; Bestätigung schreibt nur den Bearbeitungstag und ergibt einen Undo-Schritt über alle Quelllisten. Baseline: bestehender Tagesbeginn, Abbruch/Undo/Neustart und Tageswechsel; native und menschliche Abnahme separat.

**Abschlussanalyse 3.33.13 am 07.10.2026 (vor dem Paketauftrag):** KO01/AU02 sind im Quellstand durchgängig an die vorhandenen Mutations-, Speicher- und Undo-Wege angebunden. Das App-Modul umfasst 54.652 Zeilen; weitere Fachlogik schrittweise nach D17 auslagern, um die Kopplung der nächsten Feature-Schnitte zu begrenzen. `planning.py` ist Tk-frei, das Datenformat bleibt 20 und beide Lieferwerkzeuge enthalten das neue Modul. Windows-Vollprüfung und Python-Lieferung sind abgeschlossen (90 Schritte, 71 Integrationssuiten, 117 Unit-Tests; 21 Code-Dateien/131 Ressourcen und Showcase bytegleich); eine ältere Kopfzeilenprüfung erwartete im vollständigen Diagnoselauf die vorige Anzeige statt der freien Zieltagkapazität. Der App-Code bleibt bei der Korrektur dieser Prüfung unverändert. Auf Windows kann das native macOS-Bundle weder gebaut noch mit `codesign` abgenommen werden; sein Stand darf deshalb nicht als erledigt markiert werden.

**Gemeinsame Paketprüfung AU01/G05/H-02 (3.33.14):** Die Vorschlagsberechnung und die Übernahme getrennt prüfen. Ein Vorschlag darf weder den Bestand noch den Undo-Stapel ändern. Fälle: exakt passende Kapazität, voller/überplanter Tag, unbekannte Kapazität, fehlende Schätzung, bereits heute eingeplante und erledigte Aufgaben, archivierte Quelllisten sowie dieselbe Aufgabe in mehreren abgeleiteten Zeilen. Vor der Übernahme Aufgaben über ihre stabilen Quelllisten-/Punktkennungen neu auflösen und Kapazität nachrechnen; gelöschte oder inzwischen geänderte Aufgaben dürfen nicht aus einer veralteten Vorschau heraus überschrieben werden. Tageswechsel, Abbruch, Speicherfehler, Undo und Neustart über echte Bedienwege sichern. Der Tagesvorschlag ergänzt den bestehenden Tagesbeginn; Fokus und Raster-Tastaturwege gehören in dasselbe Paket. Aufgaben im Text folgen als nächstes Paket.

**Messung des ersten Suchschnitts:** Tk-freier Fachvergleich synthetischer Beschreibungen, Windows/Python 3.12.10, sieben warme Runden: 1.000/5.000/10.000 Inhaltstreffer im Median 16,3/76,5/151,5 ms, p95 23,9/77,0/152,1 ms. Ohne Treffer bei 10.000 Punkten 17,9 ms. Das umfasst nicht die Oberfläche; nächste Suchoptimierung: Ausschnitte erst für die angezeigten Treffer erzeugen und anschließend die gesamte Eingabe bis zur Anzeige messen, bevor ein FTS5-Cache eingeführt wird. [Rohwerte](https://github.com/n05a-design/glide-to-do/blob/254541aeae4577c0529d1ef768846a5c4546e59f/01_Repository/Glide/tests/qa-3.33.7/suche_2026-10-05/messung_fachsuche.json).

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

## 15. Sprint ab 08.10.2026: Aufgabenkatalog

**Stand 09.10.2026: Sprintumfang umgesetzt und geliefert** (3.33.19 bis 3.35.0); Abgleich, Abweichungen und Offenes in [15.4](#154-abschlussabgleich-abs-09102026).

**Auftrag des Inhabers vom 08.10.2026** (Kern im Wortlaut): „Führe auf dieser Grundlage anschließend einen langfristigen, umfangreichen Feature-Sprint durch.“ Der Auftrag verlangt Analyse ([Analyse](Glide_Analyse.md)), Recherche ([Markt und Vorbilder §7](Glide_Markt_und_Vorbilder.md#7-recherche-08102026-für-den-sprint)), dieses zentrale Aufgabendokument und die vollständige Umsetzung aller hier festgelegten Aufgaben mit Prüfung. Bereits entschiedene Fragen werden nicht neu vorgelegt; offene Produktentscheidungen bleiben beim Inhaber und sind unten als Blockade mit benötigter Entscheidung geführt.

**Abgrenzung des Sprintumfangs.** Zum Sprint gehören alle offenen Aufgaben der Stufen 0–4, deren Voraussetzungen erfüllt sind und die keine offene Inhaberentscheidung berühren, dazu die neuen Befunde aus der Analyse. Nicht dazu gehören (mit Grund, nicht stillschweigend):
- **Blockiert durch Inhaberentscheidung:** G17 (D07), OB02/OB03-Rest/N05/KO04 (I7), AU03-Rest (Vorgabe der Hinweise), OB04, AU07, G21 (Importquelle), G26 und danach N12 (Bauwerkzeug, D15), LG01–LG04 (I8), OB06 (Gestaltungsabnahme), Symbolschriften (A14), I1–I6, I9–I11.
- **Blockiert durch die Umgebung:** W01/W06 (Sichtprüfung unter Windows), Linux-Kalibrierung der Integrationssuiten (kein Linux auf dem Referenz-Mac, kein Containerwerkzeug), B7 (Konto bei core.tcl-lang.org), menschliche Abnahme (I6).
- **Stufe 5 „Zukunft (4.x)“ nach der Reihenfolge des Inhabers vom 30.09.2026:** N13 Seitenversionen, SQLite-Neubewertung (D16, Auslöser 20.000 Punkte), G25/Mobile (D03), Vorrat G10/G15/G18, B1 (Auslöser: Rückmeldung aus dem Alltag), W09 (Beobachtung).

**Reihenfolge.** Grundlage vor Funktion: erst Ablage, Mac-Basis und Werkzeuge (Phase 0), dann Tempo (Stufe 0 hat Vorrang nach dem Leitsatz), dann Komfort und Alltag, dann Oberfläche, dann Wissen (Stufe 2), Pixel (Stufe 3) und Austausch (Stufe 4). Jedes Paket ist eine Produktionsversion mit gezielten Prüfungen, einem eingefrorenen Volllauf auf dem Referenz-Mac, Python-/Showcase-Lieferung, Bundlebau mit Signaturprüfung und strenger CI-Grundstufe. Die Windows-Vollprüfung bleibt beim Inhaber (Prüfliste B0).

**Prioritäten:** P1 Fundament/Fehler · P2 hoher Alltagsnutzen · P3 Ausbau · P4 nachgelagert.

### 15.1 Übersicht

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
| 0 | DOK3 | Dokumentation inhaltlich nachführen (Analyse A02–A13) | P2 | A01 | ✅ 09.10.2026 (A02–A13 erledigt, laufend mit A15–A22; A14 wartet auf E-S7) |
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
| Abschluss | ABS | Abgleich Aufgabendokument ↔ Code ↔ Prüfergebnisse | P1 | alle | ✅ 09.10.2026 (§15.4: Abweichungen benannt, Offenes aufgelistet) |

### 15.2 Aufgabenkarten

Jede Karte: **Ausgangslage/Ziel** · **Nutzen** · **Umfang** · **Entscheidungen** · **Akzeptanz** · **Prüfung** · **Nachweis** (nach Umsetzung). Gemeinsam gilt für alle Produktionsaufgaben: Prinzipien-Check, Fachlogik Tk-frei mit Unit-Tests (D17), `item_change`/`sidebar_change`/`run_modal`, ein Undo-Schritt je Aktion, keine neue Laufzeitabhängigkeit, Mindestgröße 860 × 700, große Schrift, hell und dunkel, Kontrast; kein Datenformatwechsel, sofern nicht genannt.

#### Phase 0 – Grundlage

**A01 Dokumentinhalte aus `main` übernehmen** · Ausgangslage: Der Arbeitsstand 3.33.9–3.33.18 entstand auf Basis `254541a`; die Commits `270b7e7`/`80331ce` (PR #15) fehlten. Ziel: kein Verlust von Leitgedanken, Featurematrix, I9–I11, GitHub-Auftritt. Umfang: Drei-Wege-Abgleich der zwölf Dokumente, Konflikte zugunsten des neueren Stands mit den Ergänzungen aus `main`. Akzeptanz: alle Abschnitte aus `main` vorhanden, Standprüfung grün. Nachweis: ✅ 08.10.2026, Standprüfung 50 Dokumente grün; Begriffe an U16 angeglichen.

**PR01 Native Mac-Vollprüfung und Bundle** · Ausgangslage: Seit 3.33.6 gab es keine Mac-Vollprüfung und kein neues Bundle. Ziel: Der unveränderte Stand 3.33.18 ist auf dem Referenz-Mac automatisch geprüft und als Bundle gebaut. Umfang: `pruefen.py --modus voll`, `baue_app.py`, `codesign --verify --deep --strict`, SHA-256 Bundle ↔ `src/glide`. Akzeptanz: Exitcode 0 oder jeder rote Schritt mit belegter Ursache und Korrektur; Bundle trägt 3.33.18. Prüfung: Vollprüfung, Paketierungssuite. Nachweis: `tests/qa-3.33.18/mac_basis_2026-10-08/`.

**W10 Aufbewahrungswerkzeug** · Ausgangslage: `ablage_kuerzen.py` lehnt jeden Pfad ab, dessen Elternordner oberhalb der Ablage eine Verknüpfung ist (macOS `/var`), Unit-Test `test_retention` rot auf dem Mac. Ziel: nur Verknüpfungen innerhalb der Ablage ablehnen. Akzeptanz: Unit-Test grün auf macOS, Schutz gegen Verknüpfungen in der Ablage bleibt (neuer Test mit Verknüpfung innerhalb). Prüfung: Unit-Tests, Werkzeugtests.

**W11 Kommentare Tastaturabschirmung** · Ziel: Kommentare in `pruefen.py` und `hintergrund/sitecustomize.py` sagen dasselbe wie Prüfplan und Architektur (Maus abgeschirmt, Tastatur nicht). Akzeptanz: Syntaxbaum der Programmlogik unverändert, Text korrekt.

**W02 Dunkeltests** · Ausgangslage: `test_ui_updates` und `test_ui_polish36` setzen `theme_name` direkt; die Dunkelfälle laufen hell. Ziel: Wechsel über `set_design`. Akzeptanz: Die Suiten prüfen nachweislich ein dunkles Design (Hintergrundluminanz), Gegenprobe: alte Zuweisung würde scheitern. Prüfung: beide Suiten auf dem Mac.

**W03 Zeilenenden** · Ziel: `.gitattributes` in der Wurzel mit `text=auto`, LF für Text, `-text` für `vendor` und Schriften auch in `07_Python-Versionen`. Akzeptanz: `git check-attr` zeigt die Regeln für Stichproben; kein Inhaltswechsel bestehender Dateien. Prüfung: CI-Grundstufe.

**W04 CI-Wächter** · Ziel: Die CI-Grundstufe meldet Dateien `<Name>-<Gerätename>.<Endung>` neben einem gleichnamigen Original und Hauptdokumente, die gegenüber dem letzten Commit um mehr als 40 % schrumpfen, ohne Vermerk. Akzeptanz: Werkzeugtests mit positiven und negativen Fällen; bestehende Ablage grün. Prüfung: Werkzeugtests, CI-Grundstufe.

**DOK3 Dokumentation nachführen** · Ziel: Analysebefunde A02–A13 berichtigen (Zielwerte §10, Tabelle §2, Formattor §8, Prüfplan-Modulliste, I5, Mac-Stand, Markt §4.1, Messwerte). Akzeptanz: Standprüfung und Linkprüfung grün; jede Berichtigung in der Analyse als behoben vermerkt.

#### Paket 1 – Tempo (3.33.19)

Gemeinsame Messregel: Referenz-Mac, gleiche künstliche Fixture, Aufwärmlauf, kalt/warm getrennt, Median und p95, Rohwerte im Nachweis; Gegenprobe gegen 3.33.18 im selben Lauf. Kein Gewinn wird ohne unprofilierte Messung behauptet.

**P04 Bildlayout** · Ausgangslage: Seiten mit Bildern rechnen Layout und Platzierung bei jedem Scroll- und Configure-Ereignis vollständig (`layout_images`, `place_images`). Ziel: Layout nur bei geänderter Geometrie (Breite, Bildgröße, Text vor dem Anker), beim Scrollen nur Platzieren sichtbarer Bilder. Nutzen: flüssiges Scrollen in Bildseiten. Akzeptanz: gleiche Bildpositionen wie 3.33.18 in einer Differenzprobe (≥ 20 Seiten-/Breitenfälle); messbar weniger Layoutaufrufe je Scrollschritt; kein verschachteltes `update`. Prüfung: neue Pflichtsuite, `test_bilder330`, `test_seiten330`, Messung Scrollen in einer Seite mit 30 Bildern.

**P06r Doppelte Aktualisierungen** · Ausgangslage: 21 Kandidaten aus dem Codeabgleich, keine bestätigten Fehler. Ziel: je Kandidat messen, ob eine Aktion mehrfach speichert oder neu aufbaut; bestätigte Doppelungen beseitigen. Akzeptanz: Zähler je Aktion (Speichern, `_refresh_tree`, Seitenleistenaufbau) für die Kandidaten dokumentiert; bestätigte Fälle auf genau einen Lauf reduziert; Verhalten/Undo unverändert. Prüfung: Zählsuite mit echten Bedienwegen.

**P03r Startseitenkacheln behalten** · Ziel: Kacheln, deren Eingangswerte sich nicht geändert haben, bleiben beim Neuaufbau der Startseite erhalten (Cache nach Kachel-ID und Wertesignatur, an die Lebensdauer des Hosts gebunden, vollständige Invalidierung bei Design, Schrift, Größe, Tageswechsel). Akzeptanz: Zweiter Aufbau ohne Änderung erzeugt keine neuen Kachel-Widgets; jede Änderung einer Eingangsgröße erneuert genau die betroffene Kachel; Aufbauzeit gemessen. Prüfung: `test_startseite3332`, neue Pflichtfälle, Messung 1.000 Punkte.

**E01 Einstellungsfenster** · Ausgangslage: Median rund 2,1 s bis zur Anzeige. Ziel: Ursache messen (Profil zur Erklärung, unprofilierte Messung zur Abnahme) und die Einblendung deutlich verkürzen, ohne Inhalte zu entfernen. Akzeptanz: Median auf dem Referenz-Mac ≤ 50 % des Ausgangswerts oder begründete Grenze; alle Einstellungen unverändert wirksam; Mindestgröße. Prüfung: Einstellungssuiten, `test_mindestgroesse330`, Messung.

**P08c Abhaken bei 5.000 Punkten** · Ziel: Ausgangswert auf dem Mac messen, den teuersten Anteil (Vergleich, Kodierung, Schreiben, Aufbau) bestimmen und dort kürzen, wo die Messung es trägt. Grenze nach D16: Der Bestand bleibt eine JSON-Datei, die in einem Stück atomar geschrieben wird. Akzeptanz: Messwert dokumentiert; jede Optimierung mit Differenzprobe gegen 3.33.18; Ziel 120 ms erreicht oder Grenze begründet. Prüfung: `test_speichervergleich3339`, `test_fortsetzung33311`, Messung.

**P01r Messbasis** · Ziel: `messung_speicherweg.py` um Verlauf an/aus und Speicherentwicklung (RSS vor/nach 50 Aktionen) ergänzen. Akzeptanz: Werkzeug liefert beide Reihen reproduzierbar; Werkzeugtest.

#### Paket 2 – Komfort und Alltag (3.33.20)

**KO02 Wiederholungen** · Ausgangslage: Abhaken rückt die Fälligkeit genau einen Schritt nach der alten Fälligkeit vor; eine täglich verpasste Routine muss mehrfach abgehakt werden; „Überspringen“ fehlt. Recherche: Things 3.23 erlaubt frühes Erledigen mit genau einem Folgetermin und Ausnahmen beim Verschieben. Ziel: (1) „Diesen Termin überspringen“ rückt ohne Erledigung vor (kein `done_at`, keine Aktivität „erledigt“); (2) „Verpasste Termine überspringen“ rückt eine überfällige Reihe auf den ersten Termin ab heute; (3) frühes Erledigen erzeugt genau einen Folgetermin (bestehendes Verhalten, abgesichert). Abhaken einer überfälligen Reihe bleibt unverändert (ein Schritt), die neue Aktion ist ausdrücklich. Ort: Kontextmenü, Detailbereich, Palette, nur bei Aufgaben mit Regel. Entscheidungen: D01/D02 – nur die Fälligkeit der Reihe ändert sich, Bearbeitungstag wird wie beim Vorrücken geleert. Akzeptanz: Unit-Tests der Tk-freien Logik (Monatsende, Wochentage, Enddatum, Ende der Reihe); ein Undo; Mehrfachauswahl; Erinnerungen folgen wie beim Vorrücken. Prüfung: neue Pflichtsuite mit echten Menüwegen, Neustart.

**KO03 Erinnerung in der Schnelleingabe** · Ziel: „erinnern 9 Uhr“, „erinnere um 14:30“, „Erinnerung 30 min vorher“, „/erinnern 9:00“ erzeugen einen Chip; fest am Bearbeitungstag bzw. an der Fälligkeit (sonst heute), relativ vor der Fälligkeit. Der Chip nennt „nur bei laufender Glide“. Entscheidungen: Produktgrenze Erinnerungen (laufende App), D01. Akzeptanz: Parser-Unit-Tests (Varianten, Konflikte mit Uhrzeit des Datums, Zurücknehmen, Anführungszeichen); relative Erinnerung ohne Fälligkeit wird nicht still verworfen, sondern als Text belassen mit Chiphinweis; gespeicherte Erinnerung entspricht `normalize_reminder`. Prüfung: Unit-Tests, Pflichtsuite Erfassen → Erinnerungsliste.

**KO05 Mehrzeiliges Einfügen** · Ziel: Einfügen von mehreren Zeilen in die Eingabezeile fragt „N Aufgaben anlegen?“ mit „Als eine Aufgabe“, „N Aufgaben“ und „Abbrechen“; jede Zeile läuft durch den Parser; Aufzählungszeichen und Kästchen (`- [ ]`) werden entfernt; leere Zeilen übersprungen; höchstens 200 Zeilen. Ein Undo. Recherche: Todoist „Add X tasks?“. Akzeptanz: Unit-Tests der Zeilenzerlegung; Abbruch ohne Änderung; vorhandener Einfügeweg der Liste bleibt. Prüfung: Pflichtsuite mit echtem `<<Paste>>`.

**KO06 Zuletzt benutzte Ziele** · Ziel: „Verschieben nach …“ und Labelauswahl zeigen bis zu fünf zuletzt benutzte Ziele zuerst (abgetrennt), danach wie bisher. Gespeichert nur lokal in den Einstellungen (additiv, Format 2), fehlende Ziele fallen weg. Akzeptanz: Unit-Tests der Reihenfolge; keine neue Einstellung in der Oberfläche; Undo unberührt. Prüfung: Pflichtsuite über Kontextmenü.

**U04 Eingabezeile** · Ziel: „Hinzufügen“ wird ein runder „+“-Knopf (Rolle Hinzufügen), „Erweitert“ entfällt als Dauerknopf; Umschalt+Enter öffnet die erweiterte Maske mit dem eingegebenen Text; Tooltip nennt das Kürzel. Akzeptanz: Mindestgröße ohne Ausblenden; Tastatur; Menüweg „Erweitert …“ bleibt; Kontrast. Prüfung: Pflichtsuite, Mindestgröße, Kartenfuß.

**U20 Leerzustand** · Ziel: Leerzustände zeigen genau einen Anlegeweg; wo die Eingabezeile sichtbar ist, entfällt der zusätzliche Anlegen-Knopf in der Fläche. Akzeptanz: je Ansicht ein Weg (Inventar aller Leerzustände in der Suite). Prüfung: Pflichtsuite über alle Ansichten.

**N07 „Neu in …“** · Ziel: Nach einem Versionswechsel erscheint einmal eine schließbare Karte auf der Startseite bzw. in Heute mit drei bis fünf Neuerungen der Version (Tk-freier Katalog je Version); „Gelesen“ merkt die Version in den Einstellungen. Kein Einstieg für neue Nutzer (N06 bleibt ✕): Erster Start ohne Vorgängerversion zeigt nichts. Akzeptanz: Unit-Tests für Versionsvergleich und Katalog; Karte erscheint genau einmal, auch nach Neustart nicht erneut. Prüfung: Pflichtsuite mit simuliertem Versionswechsel.

**AB08 Mindestversion** · Ziel: Beim Start prüft Glide Python ≥ 3.12 und Tk ≥ 8.6; darunter erscheint ein verständlicher Hinweis und Glide beendet sich ohne Datenzugriff; zwischen Python 3.12/3.13 bzw. Tk 8.6 und der Referenz läuft Glide mit dem bestehenden Hinweis auf Einschränkungen. Akzeptanz: Tk-freie Prüffunktion mit Unit-Tests; keine Wirkung auf Nutzerdaten. Prüfung: Unit-Tests, Startprobe.

**AU06 Routinen** · Ausgangslage: Wiederkehrende Checklisten gibt es als Listenschalter; sie stehen nicht in „Heute“. Ziel: Ein eingeklappbarer Abschnitt „Routinen“ in Heute zeigt die Listen mit wiederkehrender Checkliste, die der Nutzer über das Listenmenü „In Heute als Routine zeigen“ ausgewählt hat (lokale Anzeigeeinstellung, additiv), mit Fortschritt und abhakbaren Punkten. Keine Gewohnheitsstatistik, kein Formatwechsel. Entscheidungen: G06 vorerst nicht, AU06 ersetzt dessen Prüfung. Akzeptanz: Abhaken in Heute ändert den Punkt der Routine (gleiche ID, ein Undo); Zurücksetzen der Checkliste wie bisher; Klappzustand gemerkt (D08); Mindestgröße. Prüfung: Pflichtsuite, `test_klappmechanismen3321`, `test_heute3336`.

#### Paket 3 – Ruhige Oberfläche (3.33.21)

**N01 Automatisch (hell/dunkel)** · Ausgangslage: Kein Erscheinungsbild „wie System“ (Analyse O02). Recherche: TIP 750 (Tk 9.1) bringt `winfo isdark` und `<<AppearanceChanged>>`; Tk 9.0 auf macOS liefert `tk::unsupported::MacWindowStyle isdark`. Ziel: Einstellung „Automatisch (hell/dunkel)“ wählt je Systemmodus das helle oder dunkle Gegenstück eines Designpaars (Vorgabe Hell/Dunkel, wählbar auch Pixel, Liquid Glass, Kontrast, Minimal); Erkennung macOS über Tk, Windows über die Registry (`winreg`, Standardbibliothek), Linux über Desktop-Einstellung (`gsettings`/Portal), sonst hell. Prüfung bei Fensteraktivierung und alle 60 s ohne sichtbaren Aufwand; das Signaturdesign „Pixel“ steht in der Auswahl vorn. Entscheidungen: Widerspruch A04 – kein Gestaltungsumbau, deshalb ohne I7; keine neuen Farben. Akzeptanz: Tk-freie Auflösung mit Unit-Tests (Paar, unbekannt, Fehler der Erkennung); Wechsel ohne Neustart, Kontrast in beiden Zuständen; bestehende Wahl bleibt nach Update erhalten. Prüfung: Pflichtsuite mit simulierter Erkennung, `test_kontrast330`.

**U15 Lila nur für Hinzufügen** · Ziel: Aktive Zustände (geöffnete Ansicht im Umschalter, ausgewählte Optionen) verwenden eine neutrale Auswahlrolle; Lila bleibt Hinzufügen/Neu/Nachzeichnen. Akzeptanz: Inventar aller Verwendungen der Akzentrolle; Kontrastsuite grün; keine handgefärbten Knöpfe. Prüfung: `test_kontrast330`, `design_inventory.py`.

**U05r Gismo-Kachel** · Ziel: Pflegeknöpfe erscheinen beim Überfahren und bei Tastaturfokus; im Ruhezustand nur Figur und Balken. Akzeptanz: Tastatur erreicht die Knöpfe; kein Neuaufbau der Startseite beim Überfahren. Prüfung: `test_startseite3332`, Mindestgröße.

**U09 Pinnwandleiste** · Ziel: Die Pinnwand-Werkzeuge belegen eine Zeile im Werkzeugband; seltene Werkzeuge wandern in „…“. Akzeptanz: alle Werkzeuge per Menü/Kürzel erreichbar; Bedienfläche über der Pinnwand gemessen kleiner. Prüfung: `test_workspace310`, `test_features324`, Mindestgröße.

**U18 Seitentitel im Dokument** · Ziel: Seiten zeigen den Titel groß als erste Zeile der Lesespalte (aus dem Listentitel, bearbeitbar über denselben Weg), leere Seiten den Platzhalter „Schreiben oder „/“ für Blöcke“. Kein Datenformatwechsel: Der Titel bleibt Listentitel. Akzeptanz: Umbenennen aktualisiert beide Orte; Platzhalter verschwindet beim Tippen, wird nicht gespeichert. Prüfung: `test_seiten330`, Pflichtfälle.

**OB05 Schmale Seitenleiste** · Ziel: Dritter Zustand der Seitenleiste: schmal mit Systemzeilen-Symbolen und Pixelsymbolen angehefteter Elemente, Tooltip mit Titel; Zustand gemerkt. Akzeptanz: Tastatur, Mindestgröße, kein Springen von Kopf/Inhalt. Prüfung: Pflichtsuite, `test_festlayout330`.

**OB01r Gestaltungsskala** · Ziel: weitere Ansichten (Heute, Startseite, Dialoge) verwenden Werte aus `ui_design.py`; Zahl abweichender Einzelwerte gemessen und gesenkt, ohne sichtbare Änderung. Akzeptanz: Messung vorher/nachher; Fensterfotos unverändert bis auf belegte Rundungsdifferenzen. Prüfung: `test_titel33312`, Kontrast, Mindestgröße.

**W05/W07/W08 Dialogbefunde** · Ziel: Auf dem Mac nachstellen; bestätigte Ursachen beheben (Mindestbreite statt Inhaltsbreite für Text, Knopfreihe rechts; Hinweis nur einmal; Raster passt sich der Fläche an). Akzeptanz: Fensterfoto zeigt den Befund nicht mehr; nicht reproduzierbare Befunde bleiben für die Windows-Sichtprüfung offen. Prüfung: `test_fenster330`, Mindestgröße.

#### Paket 4 – Wissen und Seiten (3.34.0)

**B4 Bilder in Seiten** · Ziel: (1) zwei Bilder auf gleicher Höhe überlappen nicht (zweites Bild weicht unter das erste aus); (2) Druck/PDF bettet Seitenbilder als Daten-URL ein (größenbegrenzt); (3) Markdown kopieren/speichern schreibt Bildverweise auf die exportierten Dateien. Akzeptanz: Geometrietests ohne Überlappung; HTML enthält die Bilder ohne externe Verweise; Markdown-Rundlauf erhält Bilder. Prüfung: `test_bilder330`, `test_seiten330`, Unit-Tests.

**G14h Treffer hervorheben** · Ziel: Öffnen eines Inhaltstreffers scrollt zur Fundstelle und markiert alle Vorkommen des Suchbegriffs im Dokument, bis man tippt oder Esc drückt. Akzeptanz: Umlautgleichheit wie in der Suche; keine Speicherung der Markierung. Prüfung: `test_suche3337`, Pflichtfall.

**P07 FTS5 nach Messung** · Ziel: Gesamte Eingabe → Anzeige bei 10.000 Punkten messen. Liegt der Median unter 100 ms, wird kein Index gebaut (✕ mit Messbeleg); sonst ersetzbarer FTS5-Cache. Akzeptanz: Messbericht mit Median/p95; Entscheidung nach dieser Regel dokumentiert.

**D-03 Filter erklären** · Ziel: Im Filter- und gespeicherten Filterweg zeigt „Warum?“ an einem Punkt die erfüllten bzw. verfehlten Bedingungen; „Ausgeblendet: N“ erklärt auf Wunsch die Gründe. Tk-freie Auswertung. Akzeptanz: Unit-Tests je Bedingung; Ansicht ändert keine Daten. Prüfung: Pflichtsuite.

**H-02r Tastaturwege** · Ziel: Pinnwand: Pfeiltasten bewegen die ausgewählte Karte um ein Raster, Alt+Pfeile wechseln die Spalte im Board (setzt das Gruppenfeld nach D02), Enter öffnet; Seitenbäume: Alt+↑/↓ ordnen um, Alt+→ in den Ordner darüber, Alt+← heraus. Ziel und Wirkung vor dem Ausführen sichtbar, ein Undo. Akzeptanz: echte Tastenereignisse; Undo; Neustart erhält Positionen. Prüfung: Pflichtsuite, `test_klappmechanismen3321`.

**N08 JPEG unter Linux** · Ziel: Unter Linux wandelt `djpeg` (libjpeg) oder `gdk-pixbuf-thumbnailer` JPEG in PNM/PNG für die Vorschau, sonst bleibt der Platzhalter. Keine Laufzeitabhängigkeit: Werkzeug nur, wenn vorhanden. Akzeptanz: Unit-Test der Werkzeugwahl; auf dem Mac der Weg über `djpeg` gezielt erzwungen. Prüfung: Unit-Tests, `test_bilder330`. Linux-Sichtprüfung bleibt offen.

#### Paket 5 – Pixel (3.35.0)

*Lieferentscheidung 09.10.2026 (technisch, kein Inhaberentscheid):* Pakete 5 und 6 gehen gemeinsam als 3.35.0 in einen eingefrorenen Volllauf. Paket 5 ist klein (zwei Dialogergänzungen), beide Pakete lagen gleichzeitig fertig vor; jede behält ihre Pflichtsuite mit Gegenprobe gegen 3.34.0. Die Versionsnummer 3.36.0 entfällt.

**G19 Palette umfärben** · Ziel: Ändern einer Palettenfarbe ersetzt diese Farbe in der Zeichnung (indizierter Kern), ein Undo, Vorschau vor dem Bestätigen. Akzeptanz: Unit-Tests im Zellmodell; Referenzfarben unverändert; Zwischenstände unberührt. Prüfung: `test_drawing330`, Pflichtfälle.

**G-03 Symbolvorschau** · Ziel: Vor dem ICO-Export zeigt eine Vorschau die Zeichnung in 16, 32 und 48 px auf hellem und dunklem Grund, pixelscharf. Akzeptanz: Vorschau entspricht den exportierten Bildern (Pixelvergleich). Prüfung: `test_etappe1_332`, Pflichtfall.

#### Paket 6 – Austausch (geliefert mit Paket 5 als 3.35.0)

**G24 KI-Austausch Stufe 2** · Ziel: (1) Kontextpaket einer Auswahl (Liste/Seite/Aufgaben) mit Prüfsummen und Ausgangsstand je Objekt; (2) Import eines Änderungsvorschlags (`patch`): Feldvergleich je Aufgabe (alt → neu), Konflikte, wenn der Ausgangsstand nicht mehr stimmt, nie still überschreiben; Übernahme nach Bestätigung mit Vorsicherung als ein Undo-Schritt. Austauschformat-Version 2, Version 1 bleibt lesbar. Entscheidungen: Q3 (Dokumente statt Schnittstelle). Akzeptanz: Unit-Tests für Patch-Prüfung und Konflikte; Spezifikation im Datenvertrag; Vorschau zeigt jede Änderung. Prüfung: Pflichtsuite, `test_features3xx` des Austauschs.

**F-03 Sicherungen vergleichen** · Ziel: Zwei Sicherungsstände (automatische Sicherung, Backupdatei) lesbar vergleichen: Listen und Aufgaben neu/entfernt/geändert mit Feldern, ohne Schreibzugriff. Akzeptanz: Tk-freie Vergleichslogik mit Unit-Tests; keine Datei wird geschrieben. Prüfung: Pflichtsuite.

#### Abschluss

**ABS Abgleich** · Ziel: Jede Zeile in 15.1 mit tatsächlichem Code, Prüfung und Nachweis abgleichen; Abweichungen benennen; Übergabe, QA-Bericht, Funktionen, CHANGELOG und Arbeitsrichtung inhaltlich nachgeführt.

### 15.3 Benötigte Inhaberentscheidungen (Stand 08.10.2026)

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

### 15.4 Abschlussabgleich ABS (09.10.2026)

Jede Zeile aus 15.1 gegen Code, Prüfung und Nachweis abgeglichen. Quelle der Prüfzahlen sind die eingefrorenen Mac-Volläufe (Referenz-Mac, Python 3.14.5, Tk 9.0.3, künstliche Daten); Nachweise unter `01_Repository/Glide/tests/qa-<Version>/`.

| Version | Aufgaben | Einstieg im Code (Auswahl) | Pflichtsuite, Gegenprobe | Volllauf, Lieferung |
|---|---|---|---|---|
| 3.33.19 Tempo | P04, P06r, P03r, E01, P08c, P01r | `layout_images` (inkrementell), `settings_write_batch`, Startseitenkacheln behalten | `test_tempo33319`, gegen 3.33.18 rot | Exit 0, 94 ausgeführt; 07, Showcase, Bundle SHA-256-gleich |
| 3.33.20 Komfort | KO02, KO03, KO05, KO06, U04, U20, N07, AB08, AU06 | `repeat_rules.py`, `capture_parser.py`, `routines.py`, `release_notes.py`, `runtime_check.py` | `test_komfort33320`, gegen 3.33.19 rot | Exit 0, 95 ausgeführt; gleich geliefert |
| 3.33.21 Ruhige Oberfläche | N01, U15, U05r, U09, U18, OB05, OB01r, W05 | `appearance.py`, `with_active_role`, `board_controls`, `PageEditor.title_label`, `sidebar_rail` | `test_oberflaeche33321`, gegen 3.33.20 rot | Exit 0, 96 ausgeführt (nach W14/W15); gleich geliefert |
| 3.34.0 Wissen und Seiten | B4, G14h, D-03, H-02r, N08; P07 ✕ | `image_push`, `build_page_print_html`, `page_document_from_markdown`, `highlight_matches`, `filter_explain.py`, `keyboard_sidebar_move`, `preview_tools.py`, `content_search._original_index` | `test_wissen3340`, gegen 3.33.21 rot | Exit 0, 97 ausgeführt; gleich geliefert |
| 3.35.0 Pixel und Austausch | G19, G-03, G24, F-03 | `drawing_replace_color` + `DrawingModel.discard_open_action`, `drawing_icon_preview`, `exchange_patch.py` + `show_exchange_patch_dialog`, `backup_diff.py` + `show_backup_compare_dialog` | `test_pixel3350`, `test_austausch3350`, beide gegen 3.34.0 rot | Exit 0, 99 ausgeführt; 07 (37 Code-Dateien), Showcase, Bundle SHA-256-gleich |

**Abweichungen von den Aufgabenkarten (benannt, nicht stillschweigend):**

- **H-02r:** Ziel und Wirkung erscheinen beim Ausführen als Hinweis mit „Rückgängig“, nicht vorher – eine Vorabfrage je Tastendruck würde die Tastaturbedienung bremsen. Pfeile ohne Alt wählen auf der Pinnwand weiter Karten (wie in Liste und Seitenleiste); Alt+Pfeile bewegen. Wer eine Vorabanzeige will, entscheidet das als Inhaber.
- **D-03:** „Warum?“ und „Ausgeblendet: N“ gelten für gespeicherte Filter; die einfache Listensuche mit Statusschalter hat nur zwei sichtbare Bedingungen und bekam keinen Erklärdialog.
- **P07:** kein FTS5-Index – nach der Regel der Karte belegt (3.33.21 100,8 ms → 3.34.0 66,6 ms Median).
- **B4:** zusätzlich der Rückweg (Markdown mit Bildern wird wieder Seite mit Seitenbildern), weil die Abnahme „Markdown-Rundlauf erhält Bilder“ sonst nicht erfüllbar war.
- **N08, W07, W08:** Linux- bzw. Windows-Sichtprüfung steht aus (◇/offen); auf dem Mac sind N08 mit erzwungenem Linux-Weg und W05 belegt, W07/W08 nicht nachstellbar.
- **Pakete 5 und 6:** gemeinsam als 3.35.0 geliefert; 3.36.0 entfällt (Begründung bei Paket 5).
- **Bundle:** `codesign --verify` scheitert direkt im OneDrive-Ordner am Dateianbieter; geprüft im Bauordner und auf einer Rückkopie, Inhalt gleich.
- **Nachweise 3.33.13–3.33.16:** waren nie eingecheckt und fielen planmäßig aus der Aufbewahrung; ihre Werte stehen nur im QA-Bericht.

**Befunde des Sprints** (Analyse A15–A23): Lieferabsatz nach Werkzeuglauf, fehlender Menüweg zur vollständigen Eingabemaske, „Als erledigt markieren“ in Übersichten, zwei zeitabhängige Prüfwerkzeuge, Alt+→ bei losen Listen, Suchengpass, Bilder in Seiten – alle behoben und in der jeweiligen Version geprüft. Beim Prüfen von 3.35.0 kam ein Dreifachklick auf der Farbleiste hinzu (öffnete den Dialog erneut), behoben.

**Offen nach dem Sprint:** W02 und alle Lieferungen ab 3.33.19 auf Windows nachprüfen; W07/W08 (Windows-Sichtprüfung B1a); N08 unter Linux ansehen; menschliche Abnahme I6; Inhaberentscheidungen E-S1–E-S8 (15.3) und I1–I11. Der Arbeitsstand ist nicht eingecheckt: Die Versionen 3.33.19–3.35.0 samt Nachweisen sollten vom Inhaber committet werden, bevor die Aufbewahrung weitere uneingecheckte Nachweise entfernt.
