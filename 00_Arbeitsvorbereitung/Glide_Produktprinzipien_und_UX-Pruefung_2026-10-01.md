# Glide – Produktprinzipien und UX-Prüfung

Stand **01.10.2026** · Glide 3.32.3 · Teil 3 von 4 der Analyse vom 01.10.2026

Prüft Bestand und geplante Funktionen gegen die sechs Produktprinzipien. Grundlage:
- Code 3.32.3,
- Bildschirmfotos aus der isolierten Linux-Probe mit künstlichen Daten ([Bilder](../01_Repository/Glide/tests/qa-3.32.3/analyse_planung_2026-10-01/bilder/), 1280 × 840 px, Tk 8.6),
- die [Featurematrix](Glide_Konkurrenz_und_Featurematrix_2026-10-01.md).

Die Fotos zeigen Linux/Tk 8.6, nicht die macOS-Darstellung des Inhabers. Abstände und Schriften weichen dort ab; Struktur und Anzahl der Elemente sind gleich.

## 1. Die sechs Prinzipien als prüfbare Regeln

Prinzipien helfen nur, wenn man sie prüfen kann. Für Glide gelten sie wie folgt:

| Prinzip | Bedeutung für Glide | Prüffrage | Messbares Kriterium |
|---|---|---|---|
| **P1 Apple-like – funktioniert selbstverständlich** | Die naheliegende Handlung führt zum erwarteten Ergebnis, ohne Hinweistext. Systemkonventionen gelten (Hell/Dunkel, Kürzel, Esc, Entf, Doppelklick). | Kann jemand die Funktion nutzen, ohne einen Hinweis zu lesen? | Keine Funktion, die *nur* über einen Dauerhinweis erklärbar ist. Standardkürzel der Plattform belegt |
| **P2 Form follows function** | Gestaltung trägt Bedeutung: Farbe = Rolle (`BUTTON_ROLE_RULES`), Größe = Wichtigkeit, Position = Zusammenhang. | Würde die Funktion ohne dieses Gestaltungselement schlechter verstanden? | Jede Farbe mit genau einer Bedeutung; keine Dekoration im Standardzustand |
| **P3 Keine Funktion doppelt** | Jede Absicht hat **einen** primären Weg. Menüeintrag und Tastenkürzel dürfen ihn spiegeln, aber keine zweite Oberfläche für dieselbe Aufgabe. | Gibt es eine zweite Oberfläche, die dasselbe Ergebnis erzeugt? | Je Absicht genau eine Bedienoberfläche + optional Menü/Kürzel |
| **P4 Kein Platz verschwenden** | Inhalt vor Bedienung. Bedienelemente erscheinen dort und dann, wo sie gebraucht werden. | Wie viel Fläche zeigt Inhalt, wie viel Bedienung? | Bedienfläche über dem Inhalt ≤ 15 % der Fensterhöhe bei 1280 × 800 |
| **P5 Nur das Wesentliche – klar und wirkungsvoll** | Standardzustand zeigt das für die Tagesarbeit Nötige; alles andere ist erreichbar, aber nicht sichtbar. | Würde jemand dieses Element vermissen, wenn es standardmäßig fehlte? | Startseite ≤ 5 Kacheln im Standard; Kopfzeile ≤ 4 Symbolknöpfe |
| **P6 Geringe Komplexität trotz vieler Funktionen** | Wenige, stabile Grundbegriffe (Aufgabe, Liste, Seite, Notiz, Ordner, Heute). Neue Funktionen erweitern bestehende Orte statt neue zu schaffen. | Braucht die Funktion einen neuen Begriff, eine neue Ansicht oder ein neues Fenster? | Neue Seitenleisteneinträge/Ansichten nur mit Entscheidung |

Ergänzend gelten die bestehenden Hausregeln. Die sechs Prinzipien bauen darauf auf und stehen seit 01.10.2026 auch in den [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md):
- „Form folgt Funktion“ (26.09.2026, Produktgrenzen):
  - Keine Seitenleistenzeile ist ein zweiter Weg zu denselben Punkten.
  - Kein Symbol trägt zwei Bedeutungen.
  - Knöpfe erscheinen dort, wo sie wirken.
  - Bedienelemente ohne Wirkung werden ausgeblendet.
- Seitenleiste, Kopf und Inhalt springen nie; Kanten fluchten.
- Funktionen leben eingebettet, nicht in Zusatzfenstern.
- Farben nach `BUTTON_ROLE_RULES`: Rot = Löschen, Grün = Bestätigen, Lila = Hinzufügen/Neu, Gelb = Hinweis.
- Bereits entschieden und hier nicht erneut vorgeschlagen:
  - kein Einstieg für neue Nutzer und kein führender Begleiter (25./27.09.),
  - keine eigenen Felder je Liste,
  - keine Unterseiten,
  - Hinweisgestaltung unverändert (D06).

## 2. Bestandsprüfung

Prioritäten:
- **A** – schnell, risikoarm, deutlich spürbar
- **B** – mittlerer Aufwand
- **C** – mit Entscheidung oder größerem Umbau

Aufwand: S < 1 Tag, M 1–3 Tage, L > 3 Tage (inkl. Tests).

### 2.1 Kopfzeile, Erfassung, Suche

**U01 – Kopfzeile mit acht Symbolknöpfen, zwei Suchen** ([Bild](../01_Repository/Glide/tests/qa-3.32.3/analyse_planung_2026-10-01/bilder/00_liste.png))
- **Befund:**
  - Acht reine Symbole: Verlauf ◷, Drucken, Seitenleiste ◧, Suche ⌕, Aktionen ⌘, Schnellerfassung ↯, Benachrichtigungen ⍾, Einstellungen ⚙. Gut gelöst ist dagegen der Zeiterfassungsknopf: Er erscheint nur, solange eine Erfassung läuft.
  - ⌕ (Schnellsuche) durchsucht bereits Aktionen; ⌘ öffnet einen zweiten Aktionsdialog.
  - ⌘ ist unter Windows/Linux kein vertrautes Zeichen, ⍾ als Glocke ungewöhnlich.
- **Prinzip:** P3, P5, P1
- **Empfehlung:**
  - ⌕ und ⌘ zu **einer** Befehlspalette zusammenführen (`Strg/Cmd+K` und `Strg/Cmd+O`, Bereichsfilter „Alles · Seiten · Punkte · Aktionen“).
  - Verlauf und Drucken ins Menü.
  - Glocke nur bei anstehenden Erinnerungen zeigen.
  - Ziel: Suche, Schnellerfassung, Einstellungen (+ Glocke bei Bedarf).
- **Prio/Aufwand:** **A** / M

**U02 – Dauerhafte Hinweiszeilen** in Liste, Mein Tag, Tabelle, Pinnwand, Seite (2–3 Zeilen, z. B. „Rechtsklick → Art: Long-Task …“)
- **Prinzip:** P1, P4
- **Empfehlung:**
  - Hinweise nur bei Bedarf: kleines „?“ am Rand, das die Hinweise ein-/ausklappt (Zustand gemerkt).
  - Alternativ: nach fünf Nutzungen der Ansicht automatisch einklappen.
  - **Klären, ob D06 („Hinweisgestaltung unverändert“) diese Zeilen umfasst oder nur den Hinweisblock in Seiten** (D11).
- **Prio/Aufwand:** **A** / S

**U03 – „Suche löschen“ ist immer sichtbar**, auch bei leerem Suchfeld
- **Prinzip:** P4, P5; verletzt die bestehende Regel „Bedienelemente ohne Wirkung werden ausgeblendet“
- **Empfehlung:** Löschkreuz im Feld, nur bei Inhalt; `Esc` leert.
- **Prio/Aufwand:** **A** / S

**U04 – Eingabezeile mit „Erweitert“ und „Hinzufügen“ als Textknöpfe**
- **Prinzip:** P4, P5
- **Empfehlung:**
  - Mit G01 ersetzen durch erkannte Feldchips unter der Zeile (Datum, Bearbeitungstag, Label – jeweils mit × zum Zurücknehmen).
  - Ein schlanker „+“-Knopf (Lila) bleibt als sichtbarer Weg; „Erweitert“ wird `Shift+Enter`/Menü.
- **Prio/Aufwand:** B / M (mit G01)

### 2.2 Startseite und Ansichtenmodell

**U05 – Startseite überladen** ([Bild](../01_Repository/Glide/tests/qa-3.32.3/analyse_planung_2026-10-01/bilder/01_startseite.png))
- **Befund:**
  - 12 von 19 Kacheln standardmäßig sichtbar.
  - „Heute/Als Nächstes“ erscheint viermal: Kopfzeile der Uhrkachel, „Heute geschafft 0 von 5“, Kachel „Heute“, Kachel „Nächste Aufgabe“.
  - Mondphase und Vorlagenwerbung im Standard; Gismo-Pflege als große Kachel (bewusst gewünscht: „Standardreihenfolge zeigt Gismo höher“, Entscheidung Arbeitsbegleiter).
  - Die Zahlen „0 von 5“ und „7 eingeplant“ stehen nebeneinander, ohne erkennbaren Bezug (Tagesziel vs. Plan).
  - Teuerste Ansicht im Aufbau (348 ms).
- **Prinzip:** P5, P3, P6
- **Empfehlung:**
  - Standard „Ruhig“: **Heute** (Tagesziel + eingeplant + nächste Aufgabe in *einer* Kachel), **Gismo** (wie gewünscht), **Woche**, **Zuletzt bearbeitet**, **Angeheftet**.
  - Alle übrigen Kacheln bleiben wählbar.
  - Gismo-Kachel kompakter (Pflegeknöpfe erst beim Überfahren) (D12).
- **Prio/Aufwand:** **A** (Standardauswahl) / S · B (Kachelzusammenlegung) / M

**U06 – Überlappende Ansichten:** Mein Tag, In Bearbeitung („alle Aufgaben mit Fälligkeit“), Verspätet, Nächste Aufgabe, Tagesbeginn, Startseite-„Heute“
- **Befund:** Der Name „In Bearbeitung“ beschreibt nicht, was die Ansicht zeigt.
- **Prinzip:** P6, P1
- **Empfehlung:**
  - Zwei Hauptansichten:
    - **Heute** = Mein Tag inkl. Abschnitt „Verspätet“ und „Heute fällig“,
    - **Demnächst** = bisher „In Bearbeitung“, chronologisch.
  - „Nächste Aufgabe“ ist die erste Zeile von Heute.
  - Tagesbeginn/-abschluss bleiben **Modi** von Heute, keine eigenen Orte (D14).
- **Prio/Aufwand:** C / M

**U07 – Eingang nicht in der Seitenleiste.** Schnell Erfasstes landet im Eingang, der nur über Menü oder Startseite erreichbar ist.
- **Prinzip:** P1
- **Empfehlung:** Seitenleistenzeile „Eingang (n)“ erscheint automatisch, solange er Einträge enthält; leer verschwindet sie (kein Platzverbrauch).
- **Prio/Aufwand:** **A** / S

**U08 – Vorlagen dreifach präsent:** Seitenleiste „Vorlagen (20)“, Startseitenkachel, Menü
- **Prinzip:** P3, P5
- **Empfehlung:** Vorlagen gehören in den Anlegen-Weg: „+“ neben Listen/Seiten → „Leer · Aus Vorlage …“. Seitenleisteneintrag entfällt; Katalog bleibt über Menü und Befehlspalette erreichbar.
- **Prio/Aufwand:** B / S

### 2.3 Inhaltsansichten

**U09 – Pinnwand mit schwerer Bedienleiste** ([Bild](../01_Repository/Glide/tests/qa-3.32.3/analyse_planung_2026-10-01/bilder/07_pinnwand.png))
- **Befund:** 12 Knöpfe in zwei Reihen, drei Zeilen Hinweise, zwei Auswahlfelder. Rund 180 px vor der Fläche.
- **Prinzip:** P4, P5
- **Empfehlung:** Eine kompakte Leiste: Anheften · Neue Aufgabe · Verbinden · Modus (Frei/Board) · Zoom · „…“ für Raster, Vorschau, Auto-Anheften, Finden, Vollbild, Reiter. Hinweise über „?“.
- **Prio/Aufwand:** B / M

**U10 – Kopfzeile kürzt den Titel zugunsten der Kennzahlen** ([Tabelle](../01_Repository/Glide/tests/qa-3.32.3/analyse_planung_2026-10-01/bilder/03_tabelle.png): „Eing…“, [Mein Tag](../01_Repository/Glide/tests/qa-3.32.3/analyse_planung_2026-10-01/bilder/02_mein_tag.png): „Mein Tag · Donnerstag, 0…“ mit vierzeilig umbrochenen Kennzahlen)
- **Befund:** Kennzahlen stehen je nach Ansicht unter oder neben dem Titel.
- **Prinzip:** P2, „nichts springt“
- **Empfehlung:** Eine Regel für alle Ansichten: Titel hat Vorrang und wird nie vor den Kennzahlen gekürzt; Kennzahlen immer in der Unterzeile.
- **Prio/Aufwand:** **A** / S

**U11 – Kalender als modales Fenster** (`open_calendar_view` erzeugt `tk.Toplevel`, blockiert die App)
- **Prinzip:** Hausregel „eingebettet“, P6
- **Empfehlung:**
  - Kalender als Ansicht im Inhaltsbereich wie Mein Tag (Monat/Woche).
  - Ziehen einer Aufgabe auf einen Tag setzt den Bearbeitungstag gemäß D02.
  - Das Ziel muss vor dem Loslassen sichtbar sein.
- **Prio/Aufwand:** B / L

**U12 – Zwei vollständige Editoren für einen Punkt:** Detailbereich („alle Felder außer Anhängen“) und Maske `item_form_dialog` (F2, 725 Zeilen) mit allen Feldern
- **Prinzip:** P3, P1
- **Empfehlung:**
  - Der Detailbereich wird **der** Inspektor (inkl. Anhänge). F2/Doppelklick öffnet ihn.
  - Die Maske bleibt nur für „Neu mit allen Feldern“ – oder entfällt, wenn der Inspektor auch das Anlegen trägt.
  - Apple (iOS 27) und Things bearbeiten Felder am Objekt.
- **Prio/Aufwand:** C / L

**U13 – Bibliothek: doppelte Wege** ([Bild](../01_Repository/Glide/tests/qa-3.32.3/analyse_planung_2026-10-01/bilder/04_bibliothek.png))
- **Befund:**
  - „Liste öffnen“ dupliziert den Klick auf die Kachel.
  - „Liste importieren“ und „Listen/Ordner hinzufügen“ sind nicht unterscheidbar.
  - Zwei Aktionsreihen am Fuß.
- **Prinzip:** P3, P4
- **Empfehlung:**
  - Kachelklick öffnet; „Bearbeiten“ als Symbol beim Überfahren.
  - Fußleiste: „Neu ▾“ · „Importieren ▾“ · „Archiv (n)“ · Kartengröße.
- **Prio/Aufwand:** **A** / S

**U18 – Seite ohne Titel im Dokument** ([Bild](../01_Repository/Glide/tests/qa-3.32.3/analyse_planung_2026-10-01/bilder/06_neue_seite.png))
- **Befund:**
  - Titel nur in der App-Kopfzeile, darunter „Noch keine Aufgaben“.
  - Leere Seite ohne Platzhalter.
  - Große Lücke zwischen Formatleiste und Hinweis.
- **Prinzip:** P1, P2 (Notion-Vorbild)
- **Empfehlung:**
  - Großer Seitentitel im Dokument (bearbeitbar).
  - Unterzeile mit „zuletzt bearbeitet · Wörter“ statt Aufgabenzählung.
  - Platzhalter „Schreiben oder „/“ für Blöcke“.
  - Formatleiste erst bei Markierung (R4 bereits entschieden).
- **Prio/Aufwand:** B / M

**U19 – Mein Tag: Quellliste und Listennummer vor jedem Titel** („Eingang — 1. …“) verbraucht etwa ein Viertel der Breite und kürzt Titel
- **Prinzip:** P4, P5
- **Empfehlung:** Titel zuerst; Quelle als gedämpfte rechte Spalte oder Gruppierung nach Liste (umschaltbar). Listennummern in abgeleiteten Ansichten weglassen.
- **Prio/Aufwand:** **A** / S

**U22 – Bearbeitungstag in Listenzeilen unsichtbar.** Nur die Fälligkeit hat eine Spalte; „Website-Texte prüfen“ (Bearbeitungstag morgen) wirkt terminlos ([Bild](../01_Repository/Glide/tests/qa-3.32.3/analyse_planung_2026-10-01/bilder/00_liste.png)).
- **Prinzip:** P1, D01
- **Empfehlung:** Kleines Symbol ◉ + Tag in der Datumsspalte, wenn nur ein Bearbeitungstag gesetzt ist. Bei beiden Feldern: Fälligkeit zeigen, Bearbeitungstag als Tooltip/Inspektor.
- **Prio/Aufwand:** **A** / S

### 2.4 Menü, Begriffe, Erscheinungsbild

**U14 – Menüeinträge am falschen Ort**
- **Befund:**
  - „Papierkorb leeren“ und „Systemmitteilung testen“ unter *Ansicht*.
  - „Tabelle: verschachtelt“/„… flach“ als zwei Befehle.
  - Drei Sicherungsbegriffe (Komplettbackup, App-Backup, Listen/Ordner hinzufügen).
- **Prinzip:** P6, P3
- **Empfehlung:**
  - Papierkorb leeren → *Bearbeiten*/Papierkorbansicht.
  - Mitteilung testen → Einstellungen.
  - Verschachtelt als Häkchen.
  - Sicherung: „Sicherung speichern …“ mit Option „inkl. Einstellungen und Anhänge“ + „Sicherung laden …“ + „Teile aus Sicherung übernehmen …“.
- **Prio/Aufwand:** **A** / S

**U15 – Lila hat zwei Bedeutungen:** Hinzufügen (Umriss) und aktiver Zustand (gefüllte Reiter, Umschalter). Grün für „Anheften“ im leeren Board ist keine Bestätigung.
- **Prinzip:** P2
- **Empfehlung:** Aktiver Zustand neutral-kräftig (gefüllt in Textfarbe/Grau) oder Akzentfarbe ≠ Hinzufügen-Lila im Standard; „Anheften“ als Hinzufügen (Lila).
- **Prio/Aufwand:** B / S

**U16 – Begriffe uneinheitlich**
- **Befund:**
  - „Punkt“, „Listenpunkt“, „Aufgabe“, „Eintrag“ gemischt.
  - „Long-Task“ (englisch).
  - „Zwischenüberschrift“/„Überschrift“ für dieselbe Art.
- **Prinzip:** P1, P6
- **Empfehlung:**
  - Glossar: **Aufgabe** (abhakbar), **Notizzeile**/**Langtext** statt Long-Task, **Zwischenüberschrift**, **Gruppe**.
  - „Punkt“ nur als Oberbegriff in technischen Texten.
- **Prio/Aufwand:** **A** / S (Texte)

**U17 – Erscheinungsbild**
- **Befund:** 10 Designs, Hintergrundverläufe, Akzentfarbe, Schriftfamilie und -größe – aber kein „wie System“.
- **Prinzip:** P1, P5, Branding
- **Empfehlung:**
  - „Automatisch (wie System)“ als Standard (N01).
  - Signaturdesign hell/dunkel vorn; übrige Designs unter „Weitere“.
- **Prio/Aufwand:** **A** (Automatik) / S–M

### 2.5 Hilfe, Leerzustände, Barrierefreiheit

**U20 – Leerzustand: „Ersten Punkt anlegen“-Knopf direkt unter dem leeren Eingabefeld**
- **Prinzip:** P3
- **Empfehlung:** Leerzustand nur mit Text + Gismo; Fokus ins Eingabefeld setzen.
- **Prio/Aufwand:** C (gering) / S

**U21 – Kein „Was ist neu“**
- **Befund:**
  - Ein Einstieg für neue Nutzer wurde am 25./27.09. bewusst nicht gewählt.
  - Beispielinhalt liefern die Probedaten „Rundgang“ und der Showcase.
  - Offen bleibt, dass neue Funktionen nach einem Update nicht sichtbar werden.
- **Prinzip:** P1
- **Empfehlung:** Nach Updates eine einmalige, eingebettete „Neu in …“-Karte auf der Startseite (N07). Keine Touren mit Overlays.
- **Prio/Aufwand:** B / S

**U23 – Barrierefreiheit:** Selbstgezeichnete Canvas-Bedienelemente haben keine zugänglichen Rollen/Namen; Tk 8.6/9.0 bieten keinen Screenreader-Zugang.
- **Prinzip:** P1
- **Empfehlung:** Nach stabiler Tk-9.1-Freigabe mit `tk accessible` beginnen. Bis dahin: vollständige Tastaturwege (H-02) und Kontrast (vorhanden).
- **Prio/Aufwand:** Zukunft / L

**U24 – Symbole mit mehreren Bedeutungen** (`ICONS`)
- **Befund:**
  - ▲ steht für „nach oben“, „verspätet“ und „aufsteigend“.
  - ▼ steht für „nach unten“, „Eingang“ und „absteigend“.
  - ◷ steht für Verlauf und Zeiterfassung.
  - ≡ steht für Details und Beschreibung.
  - ◐ steht für In Bearbeitung und Mondviertel.
- **Prinzip:** P2, P3; verletzt die bestehende Regel „Kein Symbol trägt zwei Bedeutungen“
- **Empfehlung:**
  - Eingang, Verspätet und Zeiterfassung erhalten eigene Zeichen aus derselben Familie.
  - Sortier- und Verschiebepfeile dürfen gleich bleiben, wenn der Kontext eindeutig ist (Bewegung).
  - Die Symbolprüfung um eine Doppelungsregel mit Ausnahmeliste ergänzen.
- **Prio/Aufwand:** **A** / S

**Was ausdrücklich gut ist und bleiben soll:**
- Symbolfamilie aus einem Unicode-Block,
- berechneter WCAG-Kontrast,
- Farbregeln nach Bedeutung,
- Rückgängig überall,
- Tagesnavigation in Mein Tag,
- Seitenleiste mit klappbaren Bereichen,
- leere Zustände mit Gismo,
- Kartendarstellung der Bibliothek mit „Nächste Aufgaben“.

## 3. Geplante und neue Funktionen gegen die Prinzipien

Urteil:
- **aufnehmen**
- **mit Auflage** – nur in der genannten Form
- **zurückstellen**
- **nicht aufnehmen**

| Funktion | Nutzen | Prinzipien-Risiko | Gestaltungsvorgabe | Urteil |
|---|---|---|---|---|
| G01 Deutsche Eingabe mit Feldvorschau | Schnelleres Erfassen | Unsichtbare Magie (P1), drei Parser (P3) | **Ein** Parsermodul (Tk-frei) für Eingabezeile, Schnellerfassung und Dialoge. Erkannte Felder als Chips mit ×; Text bleibt unverändert zurückholbar. Semantik nach D01 plus Klärung D10 | **mit Auflage** |
| G02 Eisenhower | Priorisieren | Weitere Ansicht (P6) | Keine neue Ansicht: Board-Gruppierung „Dringlichkeit × Wichtigkeit“ in der vorhandenen Pinnwand (`group_columns`/`set_group_value`). Ziehen ändert nur Wichtigkeit bzw. Bearbeitungstag; Fälligkeit wird nie gelöscht (D02) | **mit Auflage** (D13) |
| G05 Fokus/Timer | Konzentriert arbeiten, Zeit buchen | Neues Fenster, Einstellungszoo (P5) | Fokus = Heute mit einer vergrößerten Aufgabe im Inhaltsbereich; ein Timer (vorhandene Zeiterfassung), ein Pausenrhythmus mit einer Einstellung. Kein Zusatzfenster | **mit Auflage** |
| G29 Aufgaben im Notiztext | Gedanke → Aufgabe ohne Ortswechsel | Doppelte Darstellung Notiz/Liste (P3) | Dieselbe ID in Text und Aufgabenbereich; keine Kopie. Löschen der Textzeile fragt nicht, sondern legt die Aufgabe in den Papierkorb (Undo) | **aufnehmen** |
| G31 Seitenaufgabe in Liste schicken | Projektseite → Arbeitsliste | Verweis-Löschfallen | Bewegung über ID, in der Seite bleibt ein Verweis-Chip; Regeln vor G28 festlegen | **aufnehmen** |
| G32 Filter „aus Seiten“ | Überblick | Zweite Zählung | Nur Filter in vorhandenen Ansichten, keine neue Kennzahlenleiste | **aufnehmen** |
| G08/G30 Verweise | Wissen verbinden | Neuer Begriff, Formatrisiko | `[[`-Eingabe wie in Notion/Obsidian; Rückverweise im Inspektor/Seitenende; Format-21-Tor | **aufnehmen** (Stufe 2) |
| G14 Volltextsuche | Wiederfinden | Zweite Suchoberfläche (P3) | Nur in der einen Befehlspalette (U01); Index als ersetzbarer Cache | **aufnehmen** |
| G28 Live-Liste in Seite | Projektseite als Zentrale | Verschachtelte Komplexität | Zunächst nur Listenansicht, keine Einbettung in Einbettung, dieselben Objekte | **mit Auflage** |
| G09 Titelbild | Wiedererkennung | Dekoration ohne Funktion (P2) | Nur für Seiten und deren Bibliothekskarte; optional; Bildhöhe fest, kein Springen | **mit Auflage** |
| G19 Palettenbearbeitung | Pixel-Arbeit | gering | In der vorhandenen Palettenleiste, mit Undo | **aufnehmen** |
| G17 Animation | Pixel-Signatur | Hoher Bedienumfang (P6) | Eigener Modus der Zeichnung: Bildstreifen + Abspielen + Dauer; Export nach D07 | **zurückstellen** bis Stufe 3 |
| G24/G21 Austausch, Import | Umstieg, KI-Kontext | Unklare Verluste | Vorschau mit Verlustbericht, Undo | **aufnehmen** (Stufe 4) |
| N01 Automatisch hell/dunkel | Selbstverständlich | – | Standard „Automatisch“ | **aufnehmen** |
| N04 Kalender eingebettet | Planen per Ziehen | Großer Umbau | Wie U11 | **aufnehmen** (Stufe 1–2) |
| N05 Ein Inspektor | Weniger Doppelung | Großer Umbau | Wie U12 | **aufnehmen** (Stufe 2) |
| N09 Erinnerung bei geschlossener App | Verlässlichkeit | Hintergrunddienst, Plattformcode | – | **nicht aufnehmen** (Produktgrenze, Stufe C bewusst nicht) |
| N10 Lokaler MCP-Server | KI-Assistenten | Neue Angriffsfläche, Datenänderung durch Dritte | – | **nicht aufnehmen** (Q3, 30.09.: Dokumente statt Schnittstelle; G24 trägt den KI-Austausch) |
| G06 Gewohnheiten | Routine | Neuer Begriff neben Wiederholung (P6) | – | **nicht aufnehmen** (vorerst) |
| Eingebaute Cloud-KI, Spracherfassung | Komfort | Produktgrenze, Abhängigkeit | – | **nicht aufnehmen** |

## 4. Prinzipien-Check für jede neue Funktion (Vorlage)

Vor Umsetzung in den Vertrag der Version aufnehmen und beantworten:

0. **Vorgeschichte:** Wurde die Funktion schon entschieden, verworfen oder zurückgestellt? Prüfen in Produktgrenzen, Funktionsrecherche (G-Liste, Q-Antworten), Bestandsprüfung vom 27.09. („bewusst nicht gewählt“) und D-Entscheidungen. Entschiedenes nicht erneut vorlegen.
1. **Absicht:** Welche Nutzerabsicht bedient die Funktion in einem Satz?
2. **Ort:** Welcher *bestehende* Ort (Ansicht, Inspektor, Befehlspalette, Menü) nimmt sie auf? Wenn keiner: Begründung und Entscheidung.
3. **Doppelung:** Gibt es bereits einen Weg zum selben Ergebnis? Wenn ja: welcher entfällt?
4. **Sichtbarkeit:** Was ist im Standardzustand sichtbar, was erst bei Bedarf? Zusätzliche Dauerfläche in px bei 1280 × 800?
5. **Selbstverständlichkeit:** Funktioniert es ohne Hinweistext? Welche Plattformkonvention gilt (Kürzel, Ziehen, Esc)?
6. **Farbe/Form:** Welche Rolle aus `BUTTON_ROLE_RULES`? Neue Symbole aus `ICONS`?
7. **Begriffe:** Neue Wörter? Mit Glossar abgleichen.
8. **Rücknahme:** Ein Undo-Schritt? Sichtbare Wirkung vor dem Loslassen (D02)?
9. **Daten:** Neues Feld/Format? Datenformat-Tor, Altleser, Migration.
10. **Tempo:** Kosten pro Aktion in Abhängigkeit vom Bestand (O(1), O(Liste), O(Bestand))? Messung mit 1.000/10.000 Punkten.

## 5. Zusammenfassung der Prioritäten

| Paket | Inhalt | Aufwand gesamt | Voraussetzung |
|---|---|---|---|
| **UX-Bereinigung 1 „Weniger Oberfläche“** | U01, U02, U03, U07, U10, U13, U14, U16, U19, U22, U24, N01, Startseiten-Standard aus U05 | ≈ 5–8 Arbeitstage | D11, D12 |
| **UX-Bereinigung 2 „Ein Ort je Aufgabe“** | U04 mit G01, U06, U08, U09, U15, U18, U21 (N07) | ≈ 7–11 Arbeitstage | D10, D13, D14 |
| **UX-Umbau „Eingebettet“** | U11 Kalender, U12 Inspektor | ≈ 8–12 Arbeitstage | nach Stufe 1, vor Wissen |

Einordnung in Versionen und Abhängigkeiten: [Entwicklungsplan](Glide_Entwicklungsplan_3.33ff_2026-10-01.md).
