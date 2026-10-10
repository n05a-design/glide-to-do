# Änderungsverlauf

## 3.37.0 – Logo und Symbole (10.10.2026)

- **Logo unter Tk 8.6:** Ein Tk-freier Rasterweg mit Alpha-Zwischentönen ersetzt den ungeglätteten Canvas-Rückfall; die Akzentfarbe bleibt zur Laufzeit wählbar. Tk 9 nutzt weiter SVG.
- **App-Symbole:** Vorberechnete PNGs in genau 16/32/64/256 px vermeiden Laden und ungefiltertes Verkleinern des großen PNG. Windows-/Linux- und macOS-Ränder werden getrennt berücksichtigt.
- **Freigegebene Master (D45):** Tangentiale Rundungsanschlüsse und entferntes Kurzsegment; breiterer Innenraum ausschließlich bei 16/32 px. Reguläre SVG-Quellen und Exporte ersetzen die Entwurfsquellen; die binäre Affinity-Datei bleibt als nicht nachgeführt gekennzeichnet.
- **Gesamte ICONS-Tabelle:** Auswahl nach tatsächlicher Abdeckung in normalem und fettem UI-Schriftschnitt; lesbare deutsche Kurztexte bei fehlenden Zeichen. Kopfzeilenknöpfe berücksichtigen die Textbreite. Pixel-Kachelköpfe setzen Symbol und Pixelschrift getrennt. Beschriftungen, Aktionskennungen und Tastaturwege bleiben erhalten.
- **Prüfung:** Pflichtsuite `test_logo3370.py` mit getrennten Gegenproben gegen 3.36.0, Raster-/PNG-, Geometrie- und Symbolregeln mit Unit-Tests; kein Formatwechsel und keine zusätzliche Laufzeitbibliothek. Native Vollprüfungen und menschliche Sicht-/DPI-Abnahme getrennt ausweisen.

## 3.36.0 – Fundament und Tempo (10.10.2026)

- **P03 Startseite:** Geänderte Inhalte werden in erhaltenen Flächen abgeglichen; natürliche Kartenhöhen vermeiden zusätzliche Layoutschleifen. Der tatsächliche Builder wird warm und kalt gemessen, keine Cachetreffer als Neuaufbau gezählt. Kalt-Ausnahme D46: ≤ 300 ms bei direktem Start und ≤ 500 ms im beobachteten Kindprozessverfahren, warm weiterhin ≤ 150 ms. Ansichtswechsel und erneuter Abgleich erhalten die bedienbare Scrollleiste.
- **P03 Bibliothek:** Geänderte Karten aktualisieren ihre betroffenen Elemente, unveränderte Karten behalten Fokus und Lebensdauer. Bei 200 Listen/10.000 Aufgaben sinkt der Statusabgleich im Median von rund 550 auf 11 ms; Umordnen war rund 7 % langsamer und bleibt ausdrücklich ausgewiesen.
- **E01 Einstellungen:** Sichtbare Vorschauen entstehen zuerst; ein unveränderter Dialog wird beim nächsten Öffnen wiederverwendet. Abbrechen verwirft Eingaben, geänderte Einstellungen, Listen, Design und Schrift verwerfen den alten Dialog; geschlossene Fenster geben Griff und Rückrufe frei. Erste Anzeige ≤ 250 ms, erneute Anzeige Median ≤ 150 ms/p95 ≤ 170 ms nach Freigabe D47. Kalenderwechsel und Updatekarte bleiben im gezielten Startseitenabgleich aktuell.
- **Native Prüfstände:** Gesamte sachlich ausführbare Linux-Matrix und native Windows-Vollprüfung je Lieferung verpflichtend. Uhrabhängige Prüfaufbauten und Tk-8.6-Fähigkeitszweige gezielt kalibriert, mit absichtlich defekten Gegenfällen. Windows-Checkout erlaubt lange Grafikpfade. Menschliche Sicht-, DPI- und Screenreader-Abnahme bleibt getrennt.
- **Prüfung:** Neue Pflichtsuite `test_fundament3360.py` mit drei getrennten Gegenproben gegen 3.35.0, Tk-freier Widget-Abgleich `render_retention.py` mit Unit-Tests, Lebensdauer- und Vorher-/Nachhermessung. Aufgabenformat 23 und Einstellungenformat 2 unverändert; keine neue Laufzeitabhängigkeit. Endgültige Prüfergebnisse und Lieferhashes im QA-Bericht.

## 3.35.0 – Pixel und Austausch (09.10.2026)

- **G24 KI-Austausch Stufe 2:** „Für KI bereitstellen …“ hat einen Zweck „Vorhandene Aufgaben überarbeiten lassen“ und schreibt dann ein Kontextpaket (`.glidecontext`) der aktuellen Liste, des Ordners, aller Listen oder der ausgewählten Punkte – je Aufgabe ein Verweis ohne interne Kennung, ihre Felder und eine Prüfsumme des Ausgangsstands. Die Antwort einer KI (Änderungsvorschlag, `mode: "patch"`, Austauschformat 2) öffnet „KI-Ergebnis importieren …“ in einer eigenen Prüfung: jede Änderung Feld für Feld, Konflikte (die Aufgabe hat sich seither geändert), Unbekanntes und Ungültiges benannt. Übernommen wird nur Anwendbares, nach einer Vorsicherung und als ein Rückgängig-Schritt; Erledigt an einer Wiederholung bleibt dem Abhaken in Glide vorbehalten. Version 1 bleibt unverändert lesbar.
- **F-03 Sicherungen vergleichen:** Datei › Sicherung › „Sicherungen vergleichen …“ zeigt zwischen aktuellem Bestand, automatischen Sicherungen und gewählten Sicherungsdateien, welche Listen und Aufgaben neu, entfernt, verschoben oder geändert sind (mit Feldern). Nur lesend.
- **G19 Farbe ändern mit Vorschau:** Doppelklick (oder wie bisher Umschalt+Klick) auf eine Farbe der Farbleiste ändert sie in der ganzen Zeichnung; die Zeichnung zeigt das Ergebnis vor der Bestätigung, „Nein“ verwirft es ohne Spur in Palette und Verlauf.
- **G-03 Symbolvorschau:** Vor dem ICO-Export zeigt Glide 16, 32 und 48 px auf hellem und dunklem Grund, pixelgleich zur Datei.
- **Lieferung:** Pakete 5 und 6 des Sprints gemeinsam in einem Volllauf (die geplante 3.36.0 entfällt).
- **Prüfung:** Pflichtsuiten `test_pixel3350.py` und `test_austausch3350.py` mit Gegenprobe gegen 3.34.0; neue Tk-freie Module `exchange_patch.py` und `backup_diff.py`, erweitert `drawing.py` (`icon_rgba`, `icon_preview_rows`, `discard_open_action`), jeweils mit Unit-Tests. Datenformat 23 und Einstellungen unverändert, neue nie rotierte Vorsicherung `vor_vorschlag_*.glidebackup`, keine neue Laufzeitabhängigkeit.

## 3.34.0 – Wissen und Seiten (09.10.2026)

- **B4 Bilder in Seiten:** Ein Bild, dessen Zeile noch im Bereich eines vorigen liegt, weicht unter dieses aus; nebeneinander bleiben nur ein linkes und ein rechtes Bild, die zusammen in die Spalte passen (vorher überlappten Bilder auf aufeinanderfolgenden Absätzen). Mehr › „Drucken und PDF …“ öffnet die Seite als Druckseite mit eingebetteten Bildern (Daten-URL, je Bild höchstens 6 MB). „Markdown kopieren“ verweist auf die gespeicherten Bilddateien; „Als Markdown speichern …“ legt sie wie bisher daneben. Rückweg: Markdown aus Zwischenablage oder Datei macht Bilder, deren Datei hier liegt, wieder zu Seitenbildern (ein Undo-Schritt); Netzadressen lädt Glide nie.
- **G14h Treffer hervorheben:** Ein Inhaltstreffer der Suche öffnet die Seite oder Notiz mit allen Fundstellen markiert (gleiche Umlautregeln wie die Suche), die erste im Blick; Tippen oder Esc hebt die Markierung auf. Nie gespeichert.
- **P07 Suche ohne Index:** Messung mit 10.000 Punkten und 200 Seiten: 3.33.21 brauchte von der Eingabe bis zur gezeichneten Trefferliste 100,8 ms im Median. Der Textausschnitt berechnet die Trefferposition jetzt ohne Zeichenschleife (gleichwertig, Unit-Test); 3.34.0 braucht 66,6 ms, p95 73,1 ms. Damit entfällt der FTS5-Index nach der Regel des Plans.
- **D-03 Filter erklären:** Im gespeicherten Filter zeigt „Warum steht das hier? …“ jede Bedingung mit ✓/✗; der Kopf nennt „Ausgeblendet: N“, Ansicht › Oberfläche › „Filter erklären …“ die Gründe. Ansicht und Erklärung werten dieselben Regeln aus (`filter_explain.py`).
- **H-02r Tastaturwege:** Alt+↑/↓/→/← jetzt auch in Seiten, Notizen und Zeichnungen der Seitenleiste; ein Hinweis nennt Ziel und Wirkung mit „Rückgängig“. Befund behoben: Lose Listen und Seiten stehen vor den Ordnern, Alt+→ wies sie deshalb immer ab; jetzt gilt der nächste passende Ordner darunter. Im Spaltenboard nennt Alt+←/→ die Zielspalte und das gesetzte Feld.
- **N08 JPEG unter Linux:** Vorschau über `gdk-pixbuf-thumbnailer` oder `djpeg`, wenn eines davon installiert ist; sonst wie bisher der Platzhalter. Keine neue Abhängigkeit.
- **Prüfung:** Pflichtsuite `test_wissen3340.py` mit Gegenprobe gegen 3.33.21; neue Tk-freie Module `preview_tools.py` und `filter_explain.py`, erweitert `content_search.py` und `page_markdown.py`, jeweils mit Unit-Tests. Datenformat 23 und Einstellungen unverändert, keine neue Laufzeitabhängigkeit.

## 3.33.21 – Ruhige Oberfläche (09.10.2026)

- **N01 Automatisch hell/dunkel:** Einstellungen › Darstellung und Bedienung „Automatisch hell/dunkel nach System“. Glide merkt sich das Paar des gewählten Designs und wechselt ohne Neustart mit dem System (macOS über Tk, Windows über die Registrierung, Linux über `gsettings`); Pixel und Dopamin nutzen bei hellem System „Hell“. Das Signaturdesign Pixel steht in der Auswahl vorn.
- **U15 Lila nur für Hinzufügen:** Eingeschaltete Umschalter, Werkzeuge und gewählte Optionen tragen eine neutrale Fläche aus Karten- und Schriftfarbe statt der Auswahlfarbe; markierte Inhalte bleiben in der Auswahlfarbe.
- **U05r Gismo-Kachel:** In Ruhe nur Figur, Satz und Balken; die Pflegeknöpfe erscheinen beim Überfahren oder mit der Tastatur über den Balken, ohne dass die Kachel springt.
- **U09 Pinnwand:** Eine Werkzeugzeile statt zwei; Labelfilter, Kartengröße, Verbindungsart, Zoom, Navigator, Bildvorschau und automatisches Anheften im Menü „…“, ein aktiver Filter bleibt sichtbar.
- **U18 Seitentitel:** Seiten zeigen ihren Titel groß über der Lesespalte (Klick benennt um) und in leerem Zustand „Schreiben oder „/“ für Blöcke“.
- **OB05 Schmale Seitenleiste:** Ansicht › „Seitenleiste schmal“ zeigt Systemansichten und Angeheftetes als Symbole mit Titel im Hinweis; Tastatur, gemerkter Zustand.
- **OB01r Gestaltungsskala:** Startseite, Bibliothek, Einstellungen und Schnellerfassung nehmen ihre Abstände wertgleich aus der gemeinsamen Skala (direkte Zahlen 134 → 3), ohne sichtbare Änderung.
- **W05 Dialoge:** „Tabellenspalten“ und „Für KI bereitstellen“ öffnen nach ihrer Mindestbreite statt nach der Länge eines Hinweises (vorher 1251 bzw. 1504 px), die Knopfreihe steht rechts. W07/W08 ließen sich auf dem Mac nicht nachstellen und bleiben für die Windows-Sichtprüfung.
- **Prüfung:** Pflichtsuite `test_oberflaeche33321.py` mit Gegenprobe gegen 3.33.20; neues Tk-freies Modul `appearance.py` mit Unit-Tests. Einstellungen additiv (`design_auto`, `sidebar_narrow`), Datenformat 23 unverändert, keine neue Laufzeitabhängigkeit. Werkzeuge: R10 der Standprüfung prüft die 07-README gegen den Ordner 07 (W13), `design_inventory.py` misst auch Dialoge.

## 3.33.20 – Komfort im Alltag (09.10.2026)

- **KO02 Termin überspringen:** „Diesen Termin überspringen“ rückt eine Wiederholung um genau einen Termin vor, „Verpasste Termine überspringen“ (nur bei Überfälligem) auf den ersten Termin ab heute – im Kontextmenü von Liste und Übersichten, im Detailbereich, unter Bearbeiten › Aufgabe ändern und in der Befehlspalette. Ohne Erledigung und Tageszahl, ein Undo-Schritt für die ganze Auswahl; feste Erinnerung und Bearbeitungstag entfallen wie beim Vorrücken.
- **Befund behoben:** „Als erledigt markieren“ in Heute und Demnächst setzte nur das Feld; Wiederholungen rückten nicht vor, die Tageszahl zählte nicht, eine wiederkehrende Checkliste öffnete sich nicht wieder. Jetzt derselbe Weg wie das Abhaken in der Liste.
- **KO03 Erinnerung beim Erfassen:** „erinnere 9 Uhr“, „Erinnerung morgen 14:30“, „Erinnerung 30 min vorher“, „bei Fälligkeit“ und `/erinnern` in Eingabezeile und Schnellerfassung; Chip mit „nur bei laufender Glide“, Vorlauf ohne Fälligkeit bleibt Text mit Hinweis.
- **KO05 Mehrere Zeilen einfügen:** Rückfrage „N Aufgaben anlegen?“ – je Zeile eine Aufgabe (Aufzählungen und Kästchen entfallen, `[x]` erledigt, ein Undo-Schritt), als eine Aufgabe oder Abbrechen.
- **KO06 Zuletzt benutzte Ziele:** Labels-Menü und „In Liste verschieben …“ nennen die zuletzt benutzten Ziele zuerst.
- **U04/U20 Anlegen:** runder „+“-Knopf statt „Hinzufügen“/„Erweitert“; Umschalt+Enter und Datei › Neu anlegen › „Neuer Punkt mit allen Angaben …“ öffnen die vollständige Maske (bisher nur über den Knopf erreichbar). Unter sichtbarer Eingabezeile kein zweiter Anlegeknopf im Leerzustand; das Notizbuch behält „Ersten Eintrag anlegen“.
- **AU06 Routinen in „Heute“:** wiederkehrende Checklisten auf Wunsch als Abschnitt mit offenen Punkten und Fortschritt; ohne Gewohnheitsstatistik.
- **N07 Neu in Glide:** einmalige Karte auf der Startseite nach einem Update, nicht beim ersten Start.
- **Weitere Befunde:** Ein leerer Ordner zeigt unter der Eingabezeile keinen zweiten Anlegeknopf; die Entscheidung folgt der Ansicht, nicht dem Zeichenzeitpunkt. Neue Einstellungswerte werden beim Laden geprüft; Unlesbares ergibt das frühere Verhalten.
- **AB08 Mindestlaufzeit:** Python vor 3.12 und Tk vor 8.6 werden vor jedem Datenzugriff verständlich abgewiesen; der Start lenkt den Bytecode vorher aus dem Bundle.
- **Prüfung:** Pflichtsuite `test_komfort33320.py` mit Gegenprobe gegen 3.33.19; Unit-Tests für `repeat_rules`, `capture_parser`, `routines`, `release_notes`, `runtime_check`, `interaction_policy`. Neue Tk-freie Module `routines.py`, `release_notes.py`, `runtime_check.py`. Einstellungen additiv (`today_routines`, `routine_done_days`, `recent_labels`, `recent_move_targets`, `release_notes_seen`), Datenformat 23 unverändert, keine neue Laufzeitabhängigkeit.

## 3.33.19 – Tempo (09.10.2026)

- **P06r Einmal schreiben, einmal aufbauen:** Die Buchhaltung einer Aktion (Tageszahl, zuletzt bearbeitet, Aktivität, Seitenleistenzuordnung) schreibt `settings.json` am Ende genau einmal, auch nach einem Abbruch; gleiche Einstellungen werden nicht erneut geschrieben, eine gelöschte oder fremd geänderte Datei schon. Die Belegungsdatei wird weiter geprüft, aber nur bei neuem Zeitstempel geschrieben. Nach erfolgreichem Speichern entfällt der zweite Aufbau der Seitenleiste. Abhaken schreibt die Einstellungen einmal statt viermal und die Belegungsdatei höchstens einmal statt dreimal; Rückgängig, Umbenennen, Archivieren, Löschen und Papierkorb leeren bauen die Seitenleiste einmal statt zweimal auf.
- **P04 Bildlayout in Seiten:** Nur Bilder mit geänderter Größe, geändertem Modus oder Umflusstext werden neu umflossen, nur geänderte neu gezeichnet. Seite mit 30 Bildern auf dem Referenz-Mac: Tippen fern von Bildern 273 → 2,3 ms, im Umfluss 277 → 22,5 ms je Layoutlauf (Median).
- **P03r Startseite:** Unveränderte Startseite bleibt stehen. Aktualisierung ohne Änderung 517 → 0,2 ms, Wechsel Liste → Startseite 561 → 273 ms (1.000 Aufgaben, Median); der Rest ist Zeichnen in Tk.
- **E01 Einstellungsfenster:** Umbruch je Spalte statt je Beschriftung; der verbleibende Anteil ist der Zeichenaufwand von Tk unter macOS.
- **Prüfung und Werkzeuge:** Pflichtsuite `test_tempo33319.py` mit Gegenprobe gegen 3.33.18, Zählwerkzeug `zaehlung_aktualisierungen.py`, Messwerkzeug `messung_bildseite.py`, `messung_speicherweg.py` mit Verlauf an/aus und Speicherentwicklung. Werkzeugkorrekturen ohne App-Bezug: Aufbewahrung unter macOS (W10), Kommentare zur Tastaturabschirmung (W11), Dunkelfälle über das Design (W02), Zeilenenden der ganzen Ablage (W03), Synchronisationswächter in der CI (W04), zwei Suiten für den macOS-Hintergrundmodus. Kein Formatwechsel, keine neue Laufzeitabhängigkeit.

## 3.33.18 – 08.10.2026

- Seiten im Alltag (G28/G09/U08): Live-Listen zeigen Originalaufgaben samt Unteraufgaben direkt in Seiten. Abhaken und Details verwenden denselben Heimatpunkt; Verknüpfungen lösen erhält die Quellliste. Archiv, Papierkorb und fehlende Ziele bleiben erkennbar.
- Titelbilder für Seiten und Bibliothekskarten aus lokalen Bilddateien oder einer übernommenen Pixelzeichnung. Anhänge, Kopie, Import, Papierkorb und Undo bewahren das Titelbild.
- Vorlagen im Anlegen-Menü, ausgefüllte Vorschau mit Scrollleiste vor dem Anlegen, einschließlich Seitentext, Unteraufgaben und derselben verschobenen Termine. Abbrechen verändert den Bestand nicht. Vorlagen aus einem Ordner-Menü werden vor dem ersten Speichern im gewählten Ordner eingeordnet; ein Undo und Schreibfehler sind gemeinsam abgesichert.
- Aufgabenformat 23 mit bytegenauer Vorsicherung und schreibgeschützter Vorversion; neue Fachlogik ohne Tk und ohne zusätzliche Laufzeitabhängigkeit. Prüf- und Lieferstand im QA-Bericht; native und menschliche Abnahme separat.

## Frühere Versionen (verdichtet)

Vollständig beschrieben sind die sieben neuesten Versionen; ältere stehen verdichtet in der Tabelle darunter. Ihre ausführlichen Einträge, Verträge und Nachweise trägt Git (3.33.13–3.33.16 im Commit `6098877`, ältere im Stand vor dem 03.10.2026). Das aktuelle Verhalten beschreiben die [Funktionen](docs/20_FUNKTIONEN.md).

Datenformate und ihre Felder: [Daten und Migration](docs/06_DATA_BACKUP_MIGRATION.md#formatstufen).

| Version | Datum | Kern |
|---|---|---|
| 3.33.17 | 07.10.2026 | Wissen und Woche: eingebetteter Kalender, Kapazität/Zeitfenster, lokale Objektverweise und Rückverweise; Format 22 |
| 3.33.16 | 07.10.2026 | Bedienkomfort: eine Palette für Inhalte und Aktionen, höchstens vier Kopfknöpfe, einklappbare Hinweise, Bibliothekswege, Bearbeitungstag in der Datumsspalte, eindeutige Symbole (U01/U02/U13/U14/U16/U22/U24) |
| 3.33.15 | 07.10.2026 | Aufgaben im Wissen: echte Aufgaben im Notiztext, Übernahme in Listen mit erhaltenen IDs, „Aus Seiten“ (G29/G31/G32); Format 21 |
| 3.33.14 | 07.10.2026 | Tagesvorschlag „Was passt heute?“, geführter Tagesbeginn, Zeitblöcke per Tastatur, Fokus mit genau einmal gebuchter Zeit (AU01/AU03/H-02/G05) |
| 3.33.13 | 07.10.2026 | Gemeinsames Menü „Einplanen“ und verfügbare Zeit in allen Planungswegen (KO01/AU02, `planning.py`) |
| 3.33.12 | 06.10.2026 | Titel vor Kennzahlen, Herkunft rechts in Heute (U10/U19), erste Gestaltungsskala (OB01); ausführlicher Stand in Git |
| 3.33.11 | 06.10.2026 | Gezielter Speichervergleich (P08b), stabile Aktionskennungen, U03/U07; ausführlicher Stand in Git |
| 3.33.10 | 06.10.2026 | Kennzahlen und Messwerte je Aufbau wiederverwenden (P09b); ausführlicher Stand in Git |
| 3.33.9 | 05.10.2026 | Gemeinsamer Speichervergleich (P08a); ausführlicher Stand in Git |
| – | 05.10.2026 | Windows-Prüfung und Befunde festgehalten, App unverändert; ausführlicher Stand in Git |
| 3.33.8 | 05.10.2026 | Windows-Layout, Prüflaufzeit, Formatsicherung mit Inhaltsvergleich; ausführlicher Stand in Git |
| 3.33.7 | 05.10.2026 | Inhaltssuche in der Palette (G14 erste Stufe); ausführlicher Stand in Git |
| – | 03.10.2026 | Aufräumen der Ablage, App unverändert; ausführlicher Stand in Git |
| 3.33.6 | 02.10.2026 | Heute/Demnächst und Tagesmodi (D14); ursprüngliche Mac-Abnahme im festen Git-Stand |
| 3.33.5 | 02.10.2026 | Eisenhower-Gruppierung mit erhaltener Fälligkeit (D13); ausführlicher Stand in Git |
| 3.33.4 | 02.10.2026 | Wiederholungen in der Schnelleingabe mit erstem Termin und Feldchip; ausführlicher Stand in Git |
| 3.33.3 | 02.10.2026 | Deutsche Schnelleingabe mit Feldchips (G01, D10); ausführlicher Stand in Git |
| 3.33.2 | 02.10.2026 | Startseite Ruhig und beschleunigter Aufbau; ausführlicher Stand in Git |
| 3.33.1 | 01.10.2026 | Vier Seitenleistenbereiche, Fensterbedienung, Logo und Schaltflächen nachgezogen; ausführlicher Stand in Git |
| 3.33.0 | 01.10.2026 | Tk-freies Fundament: gemeinsame Formatsicherung, Bereichsregeln, SVG-Geometrie und Startseitenkacheln |
| 3.32.3 | 01.10.2026 | Bibliothek und Aktionsleiste behalten unveränderte Karten (Refresh bei 1.000 Aufgaben 776 → 5 ms); aktiver Showcase „Parkquartier“; Beschlüsse D09–D17 |
| 3.32.2 | 30.09.2026 | Drag-and-drop in allen Seitenleistenbereichen (D04); Schriftwerte je Tk-Interpreter zwischengespeichert |
| 3.32.1 | 30.09.2026 | Klappzustände von Labelgruppen, Fächern und Bereichen bleiben erhalten; Klapppfeile per Tastatur; D01–D06 übernommen |
| 3.32.0 | 30.09.2026 | ICO-Export, Aseprite-/ASE-Paletten, selbstfüllende Platzhalter, Tagesabschluss; Hänger bei Menübefehlen und Bildseiten behoben; Pflegewerkzeuge |
| 3.31.0 | 30.09.2026 | Rückmeldungen R1–R11: Menüdialoge öffnen wieder, Editor mit Blockaktionen, Farben nach Bedeutung, schnellere Übersicht |
| 3.30.0 | 25.–29.09.2026 | Modernisierung: Pixel-Werkstatt, Startseite zum Anpassen, Pinnwand als Board, Notizbuch, Seiten mit Bildern, Galerien, Tk 9, Ziehen aus Finder/Explorer, Systemmitteilungen, zehn Designs, Logo; **Format 20** |
| 3.29.0 | 24.09.2026 | Zeichnung als eigene Listenart mit Referenzbild; **Format 19** |
| 3.28.0 | 23.09.2026 | Ordnertypen und Tagebuch (später Notizbuch); **Format 18** |
| 3.26.0 | 21.09.2026 | Notizen als Listenart, Begleiter Gismo, Lizenzentwurf; **Format 17** |
| 3.25.0 | 19.09.2026 | „Form follows function“: Übersicht und Hierarchie, Startseite mit Kacheln und gezeichneter Figur |
| 3.24.0 | 19.09.2026 | Kürzere Navigation; Pinnwand mit Mehrfachauswahl und gerichteten Verbindungen |
| 3.23.0 | 18.09.2026 | Zusammenhalt vorhandener Funktionen (46 Punkte) |
| 3.22.0 | 17.09.2026 | Checkliste je Aufgabe; **Format 16** |
| 3.21.0–3.21.4 | 14.09.2026 | Kalenderimport aus ICS, Serienende ohne UTC-Versatz, Beispielbestand testbar, Standprüfung |
| 3.20.0 | 14.09.2026 | Kalenderausgabe als ICS |
| 3.19.0 | 13.09.2026 | Dauerhafter Änderungsverlauf; **Format 15** |
| 3.18.0 | 13.09.2026 | CSV-Import mit Spaltenzuordnung |
| 3.17.0 | 13.09.2026 | Druck- und PDF-Ausgabe |
| 3.16.0 | 13.09.2026 | Vollständiges App-Backup (`.glideapp`) |
| 3.15.0 | 13.09.2026 | Tagesplanung und Tageskapazität |
| 3.14.0 | 13.09.2026 | Bearbeitungstag und geschätzter Aufwand; **Format 14** |
| 3.13.0 | 13.09.2026 | Tabellenansicht |
| 3.12.0 | 13.09.2026 | „Mein Tag“ (seit 3.33.6 „Heute“) |
| 3.11.0 | 13.09.2026 | Schnellerfassung und gespeicherte Filter |
| 3.10.0 | 13.09.2026 | Reiter und Pinnwand |
| 3.9.0 | 12.09.2026 | Einheitliche Oberfläche, Einstellungen, Hell/Dunkel |
| 3.8.0 | 12.09.2026 | Lokale Erinnerungen, Aufmerksamkeit in Taskleiste und Dock; **Format 13** |
| 3.7.0 | 07.–12.09.2026 | Kompakte Kacheln, Anhänge an Listen und Ordnern, dynamische Übersicht; **Format 12** |
| 3.6.0 | 06.09.2026 | Kachelübersicht der Listen, Jahresanzeige |
| 3.5.0 | 05.09.2026 | Wiederkehrende Aufgaben; **Format 11** |
| 3.4.0 | 05.09.2026 | Startseite neu: Uhr, Tagesziel, Schnellzugriffe, Bestand, Listenfarben |
| 3.3.0 | 04.09.2026 | Ansicht „Labels“ |
| 3.2.0 | 04.09.2026 | Keine Übernahme aus Altordnern; zentrale Textzeichen |
| 3.1.0 | 04.09.2026 | Aufräumversion ohne neue Funktion |
| 3.0.0–3.0.2 | 03.09.2026 | Neue Oberfläche (Inhalt nach oben, kein Schwarz im Hellmodus); Gruppen benutzbar, Mehrmonitor-Dialoge |
| 2.12.0 | 03.09.2026 | Ruhigere Eingabemaske |
| 2.11.0 | 03.09.2026 | Papierkorb auch für Punkte, Mehrfachauswahl, Uhrzeit; **Format 10** |
| 2.10.0 | 03.09.2026 | Label-Chips, verlustfreier TXT-Rundlauf |
| 2.9.0 | 03.09.2026 | Verschachtelte Ordner, Long-Task-Details |
| 2.8.0 | 02.09.2026 | Verspätet, Long-Task, Zwischenüberschrift, Anlage-Dialog |
| 2.7.0–2.7.2 | 02.09.2026 | Papierkorb für Listen und Ordner, Labels; **Format 7** |
| 2.6.0 | 01.09.2026 | Gruppen; **Format 6** |
| 2.5.1–2.5.5 | 31.08.–02.09.2026 | Ordneransicht, fester Eingang, Kontextmenü, „In Bearbeitung“, Anhangspfade; **Format 5** |
| 2.5.0, 2.4.1 | vor 31.08.2026 | Zwischenstand und Ausgangsstand |
