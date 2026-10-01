# Glide – Rückmeldung vom 29.09.2026: Befunde, Möglichkeiten, Entscheidungen

Stand 29.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · Entscheidungsvorlage, Q1–Q3 beantwortet, R11 neu

Auftrag: zehn neue Befunde des Inhabers (mit Bildschirmfotos von Glide und
Notion) erst recherchieren, sammeln und vorbereiten. Danach alle übrigen
Entscheidungen, Aufgaben und Schritte zeigen und den Inhaber entscheiden
lassen. **Am Code ist nichts geändert.** Nachgestellt wurde mit getrennten
Testdaten; Fotos zeigen nur das Glide-Fenster.

**So antworten:** „Alle Empfehlungen“ reicht. Sonst je Kennung, etwa
„R4 a, R5 b, R8 wie empfohlen, aber Hinzufügen in der Akzentfarbe“. Drei
Fragen brauchen deine Antwort in jedem Fall (Abschnitt 3).

Aufwand: S bis ein halber Tag, M bis zwei Tage, L mehr. Jede Umsetzung
bekommt Tests, Doku und einen Vollprüflauf.

## 1. Die zehn Befunde

### R1 – „Notizen“ klappt nicht ganz ein

- **Nachgestellt:** Nach dem Einklappen aller drei Bereiche steht
  „Tagebuch“ weiter unter „Notizen ▷“. Technisch ist der Notizbaum weg (Tk
  meldet ihn als ausgepackt).
- **Ursache:** ein Zeichenrest. macOS malt die frei gewordene Fläche am
  unteren Rand der Seitenleiste nicht neu, sie zeigt das letzte Bild des
  Baums. Das trifft vor allem „Notizen“, weil der Bereich ganz unten steht.
- **Behebung:** Nach jedem Ein- und Ausklappen die Seitenleiste neu zeichnen
  lassen, oder unten eine leere Füllfläche einsetzen, die Tk immer zeichnet.
  Den Test dafür baue ich mit einer Pixelprüfung am Fensterfoto.
- **Empfehlung:** beheben. **Aufwand:** S.

### R2 – Pinnwand: Zwei-Finger-Scrollen nach links und rechts geht nicht

- **Ursache:** Tk 9 meldet Trackpad-Gesten als `<TouchpadScroll>`. Den
  waagrechten Anteil trägt es in den oberen 16 Bit, den senkrechten in den
  unteren 16 Bit ([TIP 684](https://core.tcl-lang.org/tips/doc/trunk/tip/684.md)).
  Glide wertet nur den senkrechten Anteil aus (`_on_mousewheel`); der
  waagrechte wird verworfen.
- **Behebung:** den waagrechten Anteil überall auswerten, wo eine Fläche quer
  scrollt: Pinnwand, Tabelle, Galerie, Zeichnung, Kalender.
- **Empfehlung:** beheben. **Aufwand:** S.

### R3 – Globale Suche: Schatten und Schließen

- **Ursache des Schattens:** Tk kann nichts durchscheinen lassen. Glide malt
  deshalb unter der Suche die Karten der App nach und legt den Schatten
  darauf. Farbverläufe und dunkle Designs zeichnet es dabei nicht mit. So
  entsteht das dunkle Rechteck aus deinem Foto, und die Suche wirkt, als
  versinke sie.
- **Schließen:** Heute schließen Esc, ein zweiter Klick auf die Lupe und
  Cmd/Strg+O die Suche. **Ein Klick auf die übrige Fläche schließt sie
  nicht.**
- **Möglichkeiten:**
  - a) Schatten und Nachzeichnen entfallen. Die Karte bekommt einen
    kräftigen Rand in der Akzentfarbe und eine eigene, vom Design abgesetzte
    Fläche: dunkler Grund im hellen Design, hellerer Grund im dunklen Design.
  - b) Den Schatten behalten und die Farbverläufe mit nachzeichnen. Das
    bleibt fehleranfällig, weil jede Fläche darunter mitspielen muss.
  - c) Die ganze App abdunkeln und die Suche darüber legen. In Tk geht das
    nur als Bild der App; das ist langsam und wirkt beim Tippen träge.
- **Empfehlung:** a), dazu schließt ein Klick außerhalb die Suche.
  **Aufwand:** S.

### R4 – Seiten: Rechtsklick fehlt

- **Befund:** Der Text einer Seite hat kein Kontextmenü; nur Bilder haben
  eines. Blockarten gibt es heute:
  - Text, Überschrift 1–3, Liste, nummerierte Liste, Aufgabe;
  - Zitat, Code, Tabelle, Trennlinie, Bild.

  Umwandeln geht nur über die Werkzeugleiste und „/“.
- **Vorbild (deine Notion-Bilder):**
  - Markierung zeigt eine schwebende Formatleiste: Textart, Fett, Kursiv,
    Unterstrichen, Durchgestrichen, Code, Link, Kommentar.
  - Das Blockmenü „Umwandeln in“ bietet Text, H1–H4, Seite, Aufzählung,
    Nummerierung, To-do, Aufklappliste, Code, Zitat, Hinweisblock (Callout),
    Formel, synchronisierten Block, Spalten und Aufklappüberschriften.
- **Möglichkeiten:**
  - **a) Stufe 1 – Rechtsklick mit den vorhandenen Blockarten:**
    - Ausschneiden, Kopieren, Einfügen, als reiner Text einfügen, alles
      markieren;
    - Formatieren: Fett, Kursiv, Unterstrichen, Durchgestrichen, Code,
      Markieren, Link, Formatierung entfernen;
    - „Umwandeln in ›“: Text, H1–H3, Liste, Nummeriert, Aufgabe, Zitat, Code;
    - Block duplizieren, löschen, nach oben und unten verschieben;
    - als Markdown kopieren.
  - **b) zusätzlich die schwebende Formatleiste** bei Markierung, wie in
    Notion.
  - **c) Stufe 2 – neue Blockarten:** Überschrift 4, Aufklappliste und
    Aufklappüberschrift (passen zu „eine Seite, unendlich scrollend“) sowie
    Hinweisblöcke. Das ist eine Erweiterung des Seitendokuments. Ich prüfe
    vorher, dass ältere Stände unbekannte Blöcke nicht verwerfen, sonst
    braucht es eine neue Formatnummer.
  - **Nicht empfohlen:** Spalten, Formeln, synchronisierte Blöcke,
    Unterseiten. Weg A (ein Textfeld) trägt sie nicht sauber; Unterseiten
    hast du ausgeschlossen.
- **Empfehlung:** a) und b) jetzt, c) danach. **Aufwand:** a) M, b) S–M,
  c) M–L.

### R5 – Notizen sollen schreiben wie Seiten

- **Befund:** Notiz und Seite haben zwei Editoren.
  - **Seite (`PageEditor`):** Lesespalte mit Abständen, Markdown-Kürzel,
    „/“, Bilder, Aufgaben im Text, Werkzeuge in der festen Leiste.
  - **Notiz (`RichNoteEditor`):** eigene Werkzeugzeile (B, I, U, H2, Liste,
    Link, Mehr), Zeitstempel, Tagesabschnitt, Präsentieren; die Punktliste
    steht über dem Text.
  - Der Seiteneditor baut auf dem Notizeditor auf; das Dokumentformat ist
    dasselbe.
- **Möglichkeiten:**
  - **a) Ein Editor für beide.** Der Notiztext wird der Seiteneditor:
    - gleiche Abstände, Kürzel, „/“, Bilder und Rechtsklick (R4);
    - Werkzeuge in derselben festen Leiste;
    - die Notizfunktionen wandern mit;
    - die Punktliste bleibt über dem Text und zeigt ohne Punkte nur eine
      Zeile „+ Punkt“ (B3 der Übersicht);
    - kein neues Datenformat.
  - **b) Die Notiz wird zur Seite mit Datumskopf.** Punkte stehen im Text wie
    auf Seiten; bestehende Notizpunkte wandern in den Text. Das ist ein
    Umbau mit Migration. Die Grenze „Seite und Notiz bleiben getrennt“ vom
    26.09. verschwimmt.
  - **c) Nur die Optik angleichen** (Abstände, Schrift); zwei Editoren
    bleiben.
- **Empfehlung:** a). **Aufwand:** M–L.

### R6 – Ruckeln beim Scrollen

Gemessen am 29.09.2026 (Mac, Retina, Fenster 1400 × 950, Releaseplanung
3.30 mit 106 Punkten):

| Ansicht | hell, ohne Verlauf | dunkel, mit Verlauf |
|---|---|---|
| **Reines Tk 9, eine Liste mit 85 Zeilen (Vergleich)** | **49 ms** | – |
| Startseite | 72 ms | 159 ms |
| Listen und Ordner | 53 ms | 125 ms |
| Liste (85 Punkte) | 74 ms | 75 ms |
| Tabelle | 40 ms | 77 ms |
| Seite mit 200 Absätzen | 79 ms | 79 ms |

Die Werte gelten je Scrollschritt. Flüssig wirkt es unter 16 ms.

- **Ursachen:**
  - Schon reines Tk 9 braucht unter macOS rund 49 ms, um eine Liste neu zu
    zeichnen. Das ist eine bekannte Schwäche des macOS-Ports; jedes
    `update` markiert dort alle Fenster zum Neuzeichnen
    ([Tk-Ticket](https://core.tcl-lang.org/tk/tktview/01ef6cad33)).
  - Glides eigener Python-Code braucht je Schritt nur wenige Millisekunden.
  - Glide legt aber viele eingebettete Flächen übereinander: runde Kacheln,
    Verläufe hinter jeder Leinwand. Mit Verlauf verdoppelt sich die Zeit auf
    Startseite und Übersichten.
  - Ein Trackpad schickt viele Scrollereignisse je Sekunde, und Glide
    zeichnet nach jedem neu.
- **Möglichkeiten:**
  - a) Scrollereignisse bündeln: höchstens ein Neuzeichnen je Bild, dafür
    ein entsprechend größerer Schritt.
  - b) Verläufe beim Scrollen nicht neu malen und als ein Bild je Fläche
    statt je Leinwand.
  - c) Die 27 erzwungenen Neuzeichnungen (`update`, `update_idletasks`)
    prüfen und in häufigen Wegen entfernen.
  - d) Startseite und Übersichten mit weniger eingebetteten Widgets: Kacheln
    als Zeichnung auf einer Fläche statt als eigene Leinwände.
  - e) Langfristig ein anderes Oberflächenwerkzeug (Qt o. ä.). Das ist ein
    Neubau der Oberfläche und nur als Forschungsfrage aufgeführt.
- **Empfehlung:** a) bis c) zuerst, dazu eine Messsuite mit Grenzwerten
  gegenüber reinem Tk. Dann messen und über d) entscheiden. **Aufwand:**
  a)–c) M, d) L.

### R7 – Bilder in Seiten ruckeln beim Größeziehen

- **Ursache:** Beim Ziehen an der Ecke rechnet Glide das Bild bei *jeder*
  Mausbewegung in der neuen Größe neu (`image_motion` → `previews.image`).
  Bei PNG und SVG sind das jedes Mal Dutzende Millisekunden.
- **Behebung:** Beim Ziehen zeigt Glide nur den Rahmen und das zuletzt
  gerechnete Bild. Neu gerechnet wird höchstens alle 100 ms und endgültig
  beim Loslassen. Das Verschieben bleibt, wie es ist.
- **Empfehlung:** beheben. **Aufwand:** S–M.

### R8 – Farben nach Bedeutung

- **Befund:**
  - Die Farbrolle `clear` ist auf Rot abgebildet. Deshalb sind „Listen/Ordner
    hinzufügen …“ und „Breiten und Sortierung zurücksetzen“ rot.
  - Grün tragen 40 Knöpfe, darunter Öffnen- und Hinzufügen-Aktionen:
    „Globale Pinnwand“, „Neue Seite“, „Neue Notiz“, „Bilder hinzufügen …“,
    „Mein Tag öffnen“, „Heute“, „Filtern“, „Hinzufügen“, „Nachzeichnen …“.
  - Umgekehrt stehen einige Löschknöpfe neutral statt rot.
- **Vorschlag für feste Regeln** (eine zentrale Tabelle; eine Prüfregel
  vergleicht jede Knopfbeschriftung mit ihrer Rolle):

| Rolle | Farbe | Nur für |
|---|---|---|
| Löschen | Rot | Löschen, Entfernen, Leeren, endgültig Entfernen |
| Bestätigen | Grün | Abschließen eines Dialogs oder einer Aufgabe: Anlegen, Speichern, Übernehmen, Fertig, Erledigt, Wiederherstellen (Q2) |
| Hinzufügen | Lila | Neues anlegen oder hinzufügen: Neue Liste, Neue Seite, „+“, Hinzufügen, Bilder hinzufügen, Listen/Ordner hinzufügen, Nachzeichnen (Q2) – festes Lila in jedem Design (Q1) |
| Hinweis | Orange/Gelb | Hinweise, Warnungen, Benachrichtigungen – keine Aktion |
| Neutral | Grau (Linie) | Öffnen, Navigieren, Umschalten, Abbrechen, Importieren, Exportieren, Filtern |
| Auswahl | Akzentfarbe | nur der aktive Zustand (gewählte Ansicht, aktives Werkzeug) |

- **Empfehlung:** so umsetzen. Offen sind die Fragen Q1 und Q2
  (Abschnitt 3). **Aufwand:** M (rund 150 Knöpfe durchsehen).

### R9 – Zeichnung: zu viele Farben in der Leiste

- **Befund:** „Diese Zeichnung“ zeigt bis zu 64 benutzte Farben; daneben
  stehen „Zuletzt“ (drei Farben) und „Palette“.
- **Möglichkeiten:**
  - a) „Diese Zeichnung“ auf die sieben zuletzt benutzten Farben begrenzen;
    alle übrigen im Palettenmenü.
  - b) „Zuletzt“ und „Diese Zeichnung“ zu *einer* Reihe mit den sieben
    zuletzt benutzten Farben zusammenlegen. Das ist ein Weg statt zweier.
- **Empfehlung:** b). **Aufwand:** S.

### R10 – Referenzbild-Fenster und Prüfung aller Fenster

- **Probelauf:** Das Fenster „PNG auf 128 × 128 einpassen“ öffnet sich
  vollständig; alle sechs Knöpfe sind sichtbar. „Nur als Referenz“ legt die
  Referenz an. Den Fehler habe ich so **nicht** nachgestellt.
- **Wahrscheinliche Ursachen:**
  - Der Knopf „Referenz“ öffnet ohne geladene Referenz kein Fenster. Er zeigt
    nur unten den Satz „Keine Referenz geladen · Mehr → PNG-Referenz laden …“,
    der leicht zu übersehen ist.
  - Nur PNG ist erlaubt; JPEG oder SVG lehnt Glide ab.
  - Sehr große Bilder lehnt Glide ab.
- **Möglichkeiten:**
  - Der Knopf „Referenz“ öffnet ohne Referenz direkt die Bildauswahl.
  - JPEG und SVG über die vorhandene Vorschau (Tk 9) zulassen.
  - Die Fehlermeldung nennt den Grund im Fenster statt unten im Status.
- **Prüfsoftware:**
  - 48 Funktionen öffnen Fenster; 11 davon ruft keine Suite namentlich auf,
    etwa Handbuch, Filterdialog des Notizbuchs, Austauschformat und die
    Kachelwahl der Startseite.
  - Vorschlag: eine neue Suite `test_fenster330`. Sie öffnet jedes Fenster
    über den Weg, den du nimmst (Knopf oder Menü), und prüft:
    - Das Fenster ist sichtbar und liegt ganz auf dem Bildschirm.
    - Jeder Knopf ist erreichbar; Esc und Abbrechen schließen.
    - Die Hauptaktion wirkt.
  - Im Vollmodus legt sie von jedem Fenster ein Foto in den Protokollordner.
    Der QA-Bericht nennt danach die Zahl der geprüften Fenster.
- **Empfehlung:** alles davon. **Aufwand:** Knopf und Formate S, Suite M.

### R11 – Fenster öffnen sich teils gar nicht (neu nach Antwort Q3)

- **Befund des Inhabers:** Das Fenster zum Laden eines Referenzbilds öffnete
  sich gar nicht; es war nicht das erste Fenster, das sich beim Klicken nicht
  öffnete.
- **Probelauf:** Direkt aufgerufen öffnet sich das Referenzfenster. Der Weg
  des Inhabers führt aber über ein Menü: „Mehr › PNG-Referenz laden …“. Das
  Menü ist ein Aufklappmenü (`tk_popup`), und sein Befehl öffnet sofort die
  Dateiauswahl des Systems. Diesen Weg kann die Prüfsoftware heute nicht
  gehen: Sie ruft die Funktionen direkt auf.
- **Wahrscheinliche Ursachen** (noch nicht belegt):
  - Unter macOS öffnet Tk die Dateiauswahl aus einem noch aktiven
    Aufklappmenü nicht zuverlässig. Glide öffnet an vielen Stellen Fenster
    direkt aus Menübefehlen.
  - Ein Fehler beim Aufbau des Fensters, den Glide nur ins Fehlerprotokoll
    schreibt, ohne ihn zu zeigen.
  - Das Fenster öffnet sich hinter dem Hauptfenster oder auf einem anderen
    Bildschirm.
- **Vorgehen:**
  1. Fehlerprotokoll `fehlerprotokoll.txt` im echten Datenordner lesen – nur
     mit deiner Erlaubnis und nur die Fehlereinträge.
  2. Jeder Menübefehl, der ein Fenster öffnet, startet es erst, nachdem das
     Menü geschlossen ist (`after_idle`). Jedes neue Fenster wird nach vorn
     geholt.
  3. Scheitert der Aufbau eines Fensters, erscheint eine Meldung statt
     Stille.
  4. `test_fenster330` (R10) öffnet jedes Fenster über denselben Menüweg wie
     du.
- **Empfehlung:** 1 bis 4, vor allen anderen Etappen. **Aufwand:** M.

## 2. Noch offen aus der Übersicht vom 29.09.2026

Diese Punkte stehen unverändert in der
[Übersicht vom 29.09.2026](Glide_Uebersicht_und_Entscheidungen_2026-09-29.md).
Die Kurzfassung hier nennt Überschneidungen mit den neuen Befunden.

| Nr. | Thema | Empfehlung dort | Bezug |
|---|---|---|---|
| B1 | Seitenleiste als Ganzes scrollen wie Notion | später | – |
| B2 | Ziehen in Seiten- und Notizbaum | ja | – |
| B3 | Leere Notiz: nur eine Zeile „+ Punkt“ | ja | Teil von R5 a) |
| B4 | Bilder in Seiten: Überlappung, Druck | ja | zusammen mit R7 |
| B5 | Windows, Linux ungeprüft | Vollprüfung (I6) | – |
| B6 | Windows-Bestand Format 17 | vorher Vollsicherung | – |
| B7 | Tk-Fehler melden | ja | dazu der macOS-Zeichenrest aus R1 |
| E1–E2 | `app.pyw` aufteilen | erst mit Versionsverwaltung | R6 d) wäre ein guter erster Schnitt |
| E3 | Paket mit PyInstaller 6.22 | vorbereiten | – |
| E4, E5 | Linux-App, Prüfung auf drei Systemen | später | – |
| E6 | Tempo langer Listen messen | messen | **erledigt durch R6** (Messung oben) |
| F1 | Inhaltsverzeichnis in Seiten | ja | passt zu R4 |
| F2 | Aufklapp- und Hinweisblöcke | ja | **= R4 c)** |
| F3 | Spalten | nein | wie R4 |
| F4, F5 | Titelbild, Bibliothek als Galerie | ja | – |
| F6 | Import aus Notion und Todoist | ja | – |
| F7 | Natürliche Datumsangaben | ja | – |
| F8 | Fokusansicht | ja | – |
| F9 | Gewohnheiten, Pomodoro | später | – |
| F10 | Zeichnung als ICO/Favicon | ja | – |
| F11 | Wechsel Aufgaben ↔ Notiz | Frage | – |
| I1–I7 | Nur durch dich (Inhaberangaben, Lizenz, Konten, Marke, Python 3.14.7, Windows-Prüfung, `_Z` löschen) | – | – |

## 3. Fragen, die nur du beantworten kannst

- **Q1 – Farbe für „Hinzufügen“:** ein festes Lila in jedem Design, oder die
  gewählte Akzentfarbe? Bei dir ist die Akzentfarbe Orange, und Orange soll
  für Hinweise stehen. Das spricht für festes Lila. **Empfehlung:** festes
  Lila.
- **Q2 – Grenzfälle der Farben:** Welche Farbe tragen:
  - Wiederherstellen (Vorschlag: Grün, es schließt etwas ab);
  - Importieren (Vorschlag: neutral);
  - Nachzeichnen (Vorschlag: Lila, es legt etwas an)?
- **Q3 – Referenzbild:** Was genau ist passiert? Kam kein Fenster, blieb es
  leer, oder wurde das Bild abgelehnt? Welches Dateiformat hattest du? Ohne
  Antwort setze ich die drei wahrscheinlichen Ursachen aus R10 um.

## 4. Vorschlag für die Reihenfolge

| Etappe | Inhalt | Aufwand |
|---|---|---|
| 0 | Fenster, die sich nicht öffnen (R11) | etwa 1 Tag |
| 1 | Fehler: R1, R2, R3 (Hervorhebung, Klick außerhalb), R7, R9, R10 (Knopf und Formate) | etwa 1 Tag |
| 2 | Prüfsoftware: `test_fenster330` und Fensterfotos (R10); Messsuite für das Tempo (R6) | etwa 1 Tag |
| 3 | Farben nach Bedeutung (R8) mit Prüfregel | 1–2 Tage |
| 4 | Seiten: Rechtsklick und Formatleiste (R4 a, b), dann ein Editor für Notizen und Seiten (R5 a, B3) | 3–4 Tage |
| 5 | Tempo: R6 a) bis c), messen, dann Entscheidung über d) | 2 Tage |
| 6 | Neue Blockarten (R4 c, F1, F2), danach die übrigen F-Punkte nach Wahl | je nach Wahl |

Jede Etappe endet mit Vollprüfung, Doku und Abgleich nach
`07_Python-Versionen`.

## 5. Antworten des Inhabers

Beantwortet am 29.09.2026; Etappen 0 bis 6 umgesetzt (Vertrag 66,
Abschnitt 2.17). Offen bleiben die Punkte in Abschnitt 6.

| Nr. | Antwort | Umsetzung |
|---|---|---|
| R1–R11 | „Alle Empfehlungen“ (29.09.2026) | umgesetzt: R1–R5, R7–R11 vollständig; R6 a–c umgesetzt und gemessen, R6 d (Aufteilen von `app.pyw`) nicht, siehe E1 |
| Q1 | „gerne ein festes Lila“ (29.09.2026) | Hinzufügen erhält eine feste Farbrolle Lila in allen Designs |
| Q2 | „Wiederherstellen grün, Importieren neutral, Nachzeichnen lila“ (29.09.2026) | in die Farbtabelle von R8 übernommen |
| Q3 | „Das Fenster […] hatte sich gar nicht erst geöffnet, und es war nicht das erste Fenster, das sich beim Klicken nicht geöffnet hatte“ (29.09.2026) | neuer Befund R11 |
| Reihenfolge | „Alle Empfehlungen“ (29.09.2026) | Etappen 0–6 in dieser Reihenfolge |
| Fehlerprotokoll lesen | „Ja, lesen“ (29.09.2026) | nur die Fehlereinträge gelesen: ein `RecursionError`, nicht nachstellbar; Protokoll schreibt tiefe Ketten jetzt vollständig |
| B3, F1, F2, E6 | mit R5, R4 c und R6 erledigt | Leere Notiz ohne Liste; „Mehr › Gliederung“; Aufklappliste, Aufklappüberschrift, Hinweisblock, Überschrift 4; Tempo gemessen |
| übrige B, E, F, I (Abschnitt 2) | offen | siehe Abschnitt 6 |

## 6. Noch zu entscheiden

- **Hinweisblock:** Er ist ein Hintergrund in der Eingabefarbe und im hellen
  Design kaum sichtbar. Die Regel „keine Kästen hinter Text“ spricht dagegen,
  Notion dafür. Wahl: so lassen, kräftiger tönen oder statt Hintergrund
  eingerückt mit Zeichen „ⓘ“ am Anfang.
- **Übrige F-Punkte** nach Wahl: F4/F5 Titelbild und Galerie, F6 Import aus
  Notion/Todoist, F7 natürliche Datumsangaben, F8 Fokusansicht, F10
  Zeichnung als ICO, F11 Wechsel Aufgaben ↔ Notiz.
- **B1, B2, B4, B7, E1–E5, I1–I7** wie in der Übersicht vom 29.09.2026.

Quellen der Recherche: [TIP 684 – Touchpad-Scrollen in Tk](https://core.tcl-lang.org/tips/doc/trunk/tip/684.md),
[Tk-Ticket zur Zeichenleistung unter macOS](https://core.tcl-lang.org/tk/tktview/01ef6cad33),
[Tk-Ticket zu Canvas-Neuzeichnen unter macOS](https://core.tcl-lang.org/tk/tktview/f642d7c0f4).
