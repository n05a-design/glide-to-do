# Funktionen – Glide

Stand 03.10.2026 · Glide 3.33.6 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

Gültiges Verhalten je Bereich, verdichtet aus den Funktionsverträgen 45–79 (Glide 3.21–3.33.6, Zusammenführung am 03.10.2026). Überholte Zwischenstände sind weggelassen; die Vorfassungen trägt Git. Die Spalte „Herkunft“ nennt die früheren Vertragsnummern, damit ältere Verweise im Code und in Nachweisen auffindbar bleiben. Ausführbarer Vertrag sind die Pflichtsuiten unter `tests/integration` und `tests/unit`.

Aufbau und Bausteine: [Architektur](02_ARCHITECTURE.md). Datenfelder und Formate: [Daten und Migration](06_DATA_BACKUP_MIGRATION.md). Prinzipien, Produktgrenzen und Prinzipien-Check für neue Funktionen: [Richtung](../../../00_Arbeitsvorbereitung/Glide_Richtung.md#4-produktprinzipien).

| Abschnitt | Herkunft | Pflichtsuiten (Auswahl) |
|---|---|---|
| [1 Grundbegriffe](#1-grundbegriffe) | 47, 59, 65, 66 | `test_glide`, `test_datenintegritaet`, `test_features322` |
| [2 Seitenleiste](#2-seitenleiste-und-navigation) | 55, 66, 69, 70, 74 | `test_bereiche3331`, `test_notizbereich330`, `test_klappmechanismen3321`, `test_drag_performance3322` |
| [3 Erfassen](#3-erfassen) | 66, 68, 77 | `test_eingabe3333`, `test_features311`, `test_bilder330` |
| [4 Heute und Planung](#4-heute-demnächst-und-planung) | 46, 66, 68, 79 | `test_heute3336`, `test_features312`, `test_features315`, `test_etappe1_332` |
| [5 Listenansichten](#5-liste-tabelle-gruppierung) | 47, 48, 54, 57, 66, 78 | `test_features313`, `test_features323`, `test_eisenhower3335` |
| [6 Pinnwand](#6-pinnwand) | 49, 53, 55, 66 | `test_workspace310`, `test_features324`, `test_features330` |
| [7 Startseite](#7-startseite) | 48, 56, 58, 59, 60, 76 | `test_startseite3332`, `test_ui_updates`, `test_features328` |
| [8 Seiten, Notizen, Galerie](#8-seiten-notizen-notizbuch-galerie) | 59, 66 | `test_seiten330`, `test_aufraeumen330`, `test_bilder330`, `test_befunde330` |
| [9 Pixel-Werkstatt](#9-pixel-werkstatt) | 61, 65, 66, 68 | `test_drawing`, `test_drawing330`, `test_features329`, `test_etappe1_332` |
| [10 Suche, Aktionen, Erinnerungen](#10-suche-aktionen-erinnerungen) | 56, 66 | `test_reminders`, `test_fenster330` |
| [11 Import und Ausgabe](#11-import-ausgabe-und-austausch) | 45, 52, 66 | `test_features316`–`test_features321`, `test_template_workflows` |
| [12 Erscheinungsbild](#12-erscheinungsbild-und-fenster) | 50, 51, 57, 66, 74, 75 | `test_kontrast330`, `test_mindestgroesse330`, `test_hintergrund330`, `test_logo330`, `test_festlayout330`, `test_kartenfuss330` |
| [13 Grenzen](#13-grenzen) | 66 §11 und Folgeverträge, Produktgrenzen | – |

## 1. Grundbegriffe

- **Dokumentarten** (`LIST_KINDS`): Aufgabenliste (auch als Pinnwand angelegt, startet dann als Fläche), Notiz, Seite, Zeichnung, Galerie. Die Art ist nach dem Anlegen fest; es gibt keine allgemeine Umwandlung (D05).
- **Ordnerarten** (`FOLDER_KINDS`, Feld `folder_kind`): Ordner (`standard`), Buch (`library`, früher „Bibliothek“; neue Einträge darin sind Seiten), Notizbuch (`journal`, früher „Tagebuch“). Unbekannte Werte werden „Ordner“. Unterordner erben die Art von Buch und Notizbuch.
- **Punktarten:** Aufgabe, Long-Task (mehrzeiliger Text), Gruppe, Zwischenüberschrift. Gruppen und Überschriften tragen keine Planungsfelder und keine Checkliste.
- **Felder einer Aufgabe:** Fälligkeit (`due`, `due_time`) und Bearbeitungstag (`planned_date`, `planned_time`) sind getrennt – die Fälligkeit sagt, bis wann, der Bearbeitungstag, wann man es anfasst (D01). Dazu Aufwand, erfasste Zeit (eine laufende Zeiterfassung, der Kopf zeigt sie), Wichtigkeit, Labels, Farbe, Wiederholung, Erinnerungen, Anhänge, „Verknüpft mit“, „Wartet auf“ (mit Kreisprüfung; ein wartender Punkt fragt vor dem Abhaken).
- **Checkliste je Aufgabe:** kurze Schritte mit Text und Zustand, höchstens 50 Schritte zu 200 Zeichen. Ein abgehakter Schritt erledigt die Aufgabe nicht und zählt nicht in Bestand, Tagesziel oder Aufwand. Wiederkehrende Checkliste (Listenschalter): nach dem letzten Haken öffnen sich nach 1,2 s alle Punkte und Schritte wieder.
- **Titel** von Listen, Seiten und Ordnern höchstens 40 Zeichen (`CONTAINER_TITLE_MAX`, Zähler im Feld); Aufgabentitel sind frei.
- **Rückgängig** überall: Jede Aktion ist ein Schritt, auch Importe, Ziehen und Mehrfachänderungen. Der Hinweis nach Abhaken, Löschen oder Lösen nimmt nur zurück, was er meldet.
- **Papierkorb:** Gelöschtes wandert dorthin und ist wiederherstellbar; „Erledigte Punkte löschen“ ebenso.

## 2. Seitenleiste und Navigation

- **Systemzeilen:** Startseite, Heute, Labels, Vorlagen, Papierkorb. „Demnächst“, „Verspätet“ und der Eingang haben bewusst keine eigene Zeile (D14, U06); sie sind über „Heute“, das Ansichtsmenü, die Suche und die Startseite erreichbar. Der Änderungsverlauf ist ein Kopfzeilenknopf ◷ (Strg+H).
- **Vier Bereiche** in der Reihenfolge Seiten → Listen → Notizen → Zeichnungen (3.33.1):

  | Bereich | Inhalt | Ausblendbar |
  |---|---|---|
  | Seiten | Bücher, Ordner, Seiten | ja |
  | Listen | alle Dokument- und Ordnerarten | nein |
  | Notizen | Notizbücher, Ordner, Notizen; im Notizbuch auch datierte Zeichnungen | ja |
  | Zeichnungen | Ordner, Zeichnungen | ja |

  Ausblenden entfernt nur die Navigation; alles bleibt unter Listen erreichbar. Gemischte Altordner stehen vollständig unter Listen, ohne Umwandlung. Die Bereichszuordnung einer Ordnerwurzel ist eine lokale Anzeigeeinstellung (`sidebar_locations`), nicht Teil des Aufgabenbackups. Neue Inhalte und Verschiebungen müssen im Zielbereich zulässig sein; Ordner werden samt Inhalt geprüft.
- **Je Bereich:** Klapppfeil (Zustand in `sidebar_sections_closed`), Titel öffnet die Übersicht, „+“ mit passenden Anlegewegen, beim Überfahren „+“ und „…“ an Ordner- und Listenzeilen. Seiten- und Notizbaum höchstens acht Zeilen, der Listenbaum mindestens fünf.
- **Angeheftet:** bis zu 20 Seiten über das Kontextmenü, Block unter den Systemzeilen.
- **Ziehen** (D04, 3.32.2) in allen Bäumen mit denselben Bindungen: obere/untere Zeilenhälfte = davor/danach, Ordnermitte = hinein. Ein neutraler Ordnerwechsel ändert weder Bearbeitungstag noch Fälligkeit; im Notizbuch bleibt ein vorhandenes Momentdatum, sonst gilt das Erstellungsdatum. Zyklen und zu tiefe Verschachtelung sind gesperrt. Auf „Heute“ gezogen, wird ein Punkt für den angezeigten Tag eingeplant statt verschoben.
- **Klappzustände** (D08, 3.32.1): Labelgruppen, Abschnitte von Heute/Demnächst, Gruppen in Liste und Tabelle, Seitenleistenbereiche, Pinnwandspalten und Aufklappblöcke schließen über echte Pfeilklicks und Tastatur, bleiben beim Neuaufbau zu und überstehen den Neustart, soweit der Vertrag Speichern vorsieht. Neue Klappflächen gehören in `test_klappmechanismen3321`.
- **Startansicht** (Einstellung): letzte Ansicht (Vorgabe), Startseite, Heute, Demnächst, Listen und Ordner, Vorlagen, globale Pinnwand oder eine feste Liste; eine fehlende Liste führt auf die Startseite.

## 3. Erfassen

**Eingabezeile und Schnellerfassung** lesen den Titel mit demselben Parser (`capture_parser.py`, 3.33.3). Jede Erkennung erscheint vor dem Speichern als Chip unter der Zeile; × nimmt sie zurück, der Text bleibt im Titel und wird nicht teilweise neu gedeutet.

| Eingabe | Feld |
|---|---|
| Datum ohne Zusatz: heute, morgen, übermorgen, Wochentag, „nächsten Freitag“, „in 3 Tagen“, „in einer Woche“, „24.12.“, „24.12.2026“ | Bearbeitungstag (D01) |
| „fällig“, „fällig am“, „bis“, „bis zum“ vor einem Datum | Fälligkeit |
| Uhrzeit („14:30“, „14 Uhr“, „um 9:00“) direkt nach einem Datum | Uhrzeit dieses Datums; allein: Bearbeitungstag heute mit Uhrzeit |
| „45 Minuten“, „45 min“, „2h“, „1,5 Stunden“, „1 Std. 30 Min.“ | Aufwand |
| „!hoch“, „!wichtig“, „!mittel“, „!niedrig“ | Wichtigkeit |
| „#Label“ eines vorhandenen Labels | Label (unbekannte Namen bleiben Text) |
| `/morgen`, `/Freitag`, `/24.12.2026`, `/meintag` | Bearbeitungstag (D10) |
| `/bis …`, `/fällig …` | Fälligkeit |
| `/wichtig`, `/hoch`, `/mittel`, `/niedrig`, `/Labelname` | Wichtigkeit, Label |
| täglich, werktags, wöchentlich, „jeden Montag“, „montags und donnerstags“, „alle 3 Tage“, „alle 2 Wochen“, monatlich, jährlich | Wiederholung; die Fälligkeit wird der erste Termin (3.33.4), eine ausdrückliche Fälligkeit hat Vorrang |

- Je Art zählt die erste Angabe; ein Wochentag meint den nächsten, heute eingeschlossen, „nächsten“ schließt heute aus. Text in Anführungszeichen wird nicht gedeutet. Regeln, die das Datenmodell nicht kennt („alle 3 Monate“), bleiben Text.
- Tab ergänzt angefangene „/“-Wörter, Escape blendet die Chipleiste aus. Nach dem Anlegen steht „Angelegt · …“ mit Rückgängig.
- In der Schnellerfassung hat ein ausgefülltes Feld „Fällig“ Vorrang vor einer Fälligkeit im Titel. Die volle Eingabemaske hat eigene Felder, keinen Parser.
- Neue Punkte ohne Bearbeitungstag landen im **Eingang**. Keine Schnellerfassung für Seiten (E-09).
- **Vorlagen mit Platzhaltern:** `{{Datum}}`/`{{Heute}}`/`{{Tag}}`, `{{Wochentag}}`, `{{KW}}`, `{{Monat}}`, `{{Jahr}}`, `{{Uhrzeit}}`, `{{Morgen}}`, `{{Gestern}}` füllen sich ohne Dialog (3.32.0); nur übrige Namen wie `{{Projektname}}` werden abgefragt (höchstens 12). Gilt für Listen-, Ordner- und Seitenvorlagen. Praxis: [Vorlagen im Unternehmensalltag](27_VORLAGEN_PRAXISANLEITUNG.md).

## 4. Heute, Demnächst und Planung

**Heute** (bisher „Mein Tag“, interne Kennung `planday`) zeigt am heutigen Tag, jede Aufgabe genau einmal (`today_view.py`, D14, 3.33.6):

| Abschnitt | Inhalt |
|---|---|
| Nächste Aufgabe | genau eine nach `task_urgency_rank`: heute eingeplant, sonst überfällig oder heute fällig, sonst liegen geblieben; dieselbe wie die Startseitenkachel |
| Verspätet | vergangene Fälligkeit, nicht für heute eingeplant |
| Liegen geblieben | an einem früheren Tag eingeplant, offen, nicht überfällig |
| Tagesplan | für heute eingeplant (mit Uhrzeiten als Zeitplan/Ohne Uhrzeit) |
| Heute fällig | Fälligkeit heute, nicht eingeplant – auch aus dem Eingang |
| Verweis „Demnächst · N weitere Fälligkeiten“ | Doppelklick oder Return öffnet Demnächst |
| Eingang | Eingangspunkte ohne Bearbeitungstag (höchstens 50) |

- Andere Tage (◀/▶): „Tagesplan · Wochentag, Datum“ mit Tagesplan, „An diesem Tag fällig“ und Eingang. „Tag leeren“ nimmt den Bearbeitungstag, die Aufgaben bleiben.
- Die Zahl hinter „Heute“ zählt alles, was Heute ohne Filter zeigt (ohne Eingang).
- **Demnächst** (bisher „In Bearbeitung“, Kennung `in_progress`): alle Aufgaben mit Fälligkeit chronologisch, Überfälliges oben.
- **Tagesbeginn und Tagesabschluss** sind Modi von Heute (Schalter „Tag …“, Kontextmenü der Seitenleistenzeile). Der Tagesbeginn geht Überfälliges, Liegengebliebenes und den Eingang durch (heute, morgen, nächste Woche, ohne Tag, erledigt, überspringen). Der Tagesabschluss (3.32.0) zeigt Erledigtes, verschiebt Liegengebliebenes auf morgen und legt auf Wunsch eine Notiz ins Notizbuch. Der Wochenrückblick zeigt Erledigtes, Weitergewandertes, geschätzte gegen erfasste Zeit und die Kapazität je Tag.
- **Zeitplan:** Punkte mit Uhrzeit stehen vorn; Dauer aus der Schätzung, sonst 30 Minuten für die Überschneidungsprüfung. Überschneidungen werden benannt, nicht verschoben. Ziehen setzt die Uhrzeit (obere Blockhälfte endet am Blockbeginn, untere beginnt am Blockende, „Ohne Uhrzeit“ entfernt sie); Alt+↑/↓ verschiebt um 15 Minuten.
- **Stundenraster** („Raster“): ab 900 px neben dem Zeitplan, darunter statt der Liste; 6–22 Uhr, erweitert sich, rote Linie für jetzt. Ziehen im 15-Minuten-Raster, auch aus Liste, Eingang und „Ohne Uhrzeit“.
- **Kapazität** minutenbasiert je Wochentag; `planning_summary` ist die einzige Rechenstelle für Tages-, Auswahl- und Tabellensumme.
- **Wiederholungen:** Abhaken erzeugt den Folgetermin; das Vorrücken leert den Bearbeitungstag, statt einen Folgetag zu erfinden.

## 5. Liste, Tabelle, Gruppierung

- **Umschalter** Liste · Tabelle · Pinnwand fest nebeneinander; die offene Ansicht trägt die Auswahlfarbe.
- **Anzeige der Liste:** Kompakt (Titel, Termin, Labels), Standard (mit Symbolen für Beschreibung, Checkliste, Anhänge), Checklisten (jeder Schritt als abhakbare Zeile), Anhänge (Name und Größe), Erweitert (alles plus Beschreibungsanfang, 160 Zeichen). Detailzeilen sind Darstellung: höchstens zwölf je Punkt, nicht auswählbar, nicht in Exporten; abhaken schreibt in die Checkliste des Punkts.
- **Auswahlleiste** im Kartenfuß nur bei markierten Punkten: Anzahl, Wichtigkeit, Fällig, Einplanen, Labels, Löschen. Alles Übrige im Menü, Rechtsklick, in der Suche und als Kürzel.
- **Tabelle:** listenspezifische Spaltenwahl und -reihenfolge (`table_columns`), Überschriften linksbündig, Sortieren über die Überschrift; bei Enge weichen ganze Spalten nach `TABLE_COLUMN_PRIORITY`, der Titel behält 220 px. Verschachtelt oder gruppiert steht in der Baumspalte die Nummer aus der Liste.
- **Gruppieren** in Liste, Tabelle und Board über dieselbe Logik: Fälligkeit, Bearbeitungstag, Wichtigkeit, Label, Erledigt, Liste (Ordner- und globale Pinnwand) und **Dringlichkeit × Wichtigkeit** (3.33.5). Abschnitte sind aufklappbar, Zwischenüberschriften bleiben als Trennzeilen, jeder Punkt trägt seine Nummer aus der ungruppierten Liste. Ziehen zwischen Abschnitten oder Alt+←/→ setzt genau dieses Feld (D02): beim Datum bleibt die Uhrzeit, eine Wiederholung bleibt Serie, beim Label ersetzt das Ziel das Quelllabel, „Überfällig“ nimmt nichts an und sagt warum.
- **Eisenhower** (`eisenhower.py`, D13): dringend heißt Fälligkeit oder Bearbeitungstag höchstens zwei Tage nach heute oder vorbei; wichtig heißt Wichtigkeit ab mittel.

  | Quadrant | Ablegen setzt |
  |---|---|
  | Sofort · wichtig und dringend | Wichtigkeit mittel (falls niedriger), Bearbeitungstag heute (falls nicht dringend) |
  | Einplanen · wichtig, nicht dringend | Wichtigkeit mittel, Bearbeitungstag auf den Tag nach dem Fenster (falls nur er dringend macht) |
  | Kurz halten · dringend, nicht wichtig | Wichtigkeit niedrig (falls höher), Bearbeitungstag heute (falls nicht dringend) |
  | Später · weder noch | Wichtigkeit niedrig, Bearbeitungstag nach dem Fenster (falls nötig) |

  Eine Fälligkeit im Fenster wird nie gelöscht: Glide lehnt „nicht dringend“ dann ab und sagt warum.
- **Detailbereich** (zuschaltbar, ab 980 px, 280–640 px breit): alle Felder einschließlich Anhänge; übernommen beim Verlassen eines Felds, je Übernahme ein Rückgängig-Schritt. „Alle Felder …“ öffnet die Maske.
- **Labels-Ansicht** gruppiert nach Label; **gespeicherte Filter** sind eine reine Ableitung, bis zu vier als Startseitenkachel.
- **„Erweitert“ in abgeleiteten Ansichten** legt neu an und belegt vor: in Heute den betrachteten Tag, in Labels das Label der Gruppe.

## 6. Pinnwand

- **Anordnungen:** frei (Vorgabe), geordnete Karten, Spaltenboard. Das Board zeigt alle Aufgaben und Long-Tasks des Bereichs (E-16), gruppiert wie in Abschnitt 5; Spalten teilen sich die Breite (220 px bis 1,5 × Kartenbreite), „Leere Spalten ausblenden“, „Nur offene“, Doppelklick in eine Spalte legt einen Punkt mit ihrem Wert an.
- **Karten:** Höhe folgt dem Inhalt (Titel, Status, Termin, Checkliste mit fünf abhakbaren Schritten, Beschreibung 160 Zeichen, Bild, Labels, Quelle). Größe groß/normal/klein (1,30/1,00/0,78) hängt an der Karte, nicht am Punkt. Farbe als Streifen, Kopf oder ganze Karte. „Alle Punkte anheften“, „Auto“ heftet neue Punkte still an. Zeichnungen als Karte mit Miniatur (`page:<Seitenkennung>`).
- **Auswahl:** Strg/Cmd+Klick als Reihenfolge; die erste Karte ist der Anker. Verbinden, Erledigt, Größe und Entfernen wirken auf die Auswahl; Escape hebt sie zuerst auf.
- **Verbindungen** speichern eine Beziehung zwischen Punktkennungen (höchstens eine je Paar), mit Art `line`/`forward`/`backward`/`both`, Beschriftung bis 40 Zeichen, gestrichelt, Farbe. Ziehpunkt am Kartenrand verbindet durch Ziehen.
- **Bereiche:** benannte Rechtecke (höchstens 50); Karten mit Mittelpunkt darin wandern mit. Nur bei „Frei anordnen“.
- **Weiterdenken:** Strg/Cmd+Enter öffnet neben der Karte ein Titelfeld (E-08), auf Wunsch automatisch verbunden. Doppelklick öffnet die volle Maske.
- **Bedienung:** Vollbild über „Fläche“ oder F11; Escape von innen nach außen (Verbinden → Vollbild → Pinnwand). Scrollposition bleibt erhalten. Shift+Mausrad und Trackpad quer scrollen, gedrücktes Mausrad zieht. „Aufräumen“ ordnet die Auswahl in ein Raster. Kartenverschieben ist ein Rückgängig-Schritt.
- **Hintergrund** Punkte, Linien oder Karo (höchstens 2.500 Marken, nur sichtbarer Ausschnitt). **Präsentieren:** Bereiche als Folien im Vollbild; „Präsentation als PDF …“ öffnet eine Druckseite (je Bereich A4 quer) im Browser.
- Positionen, Verbindungen und Bereiche liegen je Pinnwand in `settings.json` (`pinboards`), nicht im Aufgabenbackup. Die Pinnwand ist keine zweite Datenhaltung.

## 7. Startseite

- **Standard „Ruhig“** (D12, 3.33.2): Heute, Gismo, Die nächsten sieben Tage, Zuletzt bearbeitet, Pinnwand-Vorschau, Zeichnungen, Angeheftet. Alle übrigen Kacheln (Uhr, Begrüßung, Nächste Aufgabe, Vorlagen, Bestand, Kalendervorschau, Verspätet, Fortschritt, Labels, Impuls, angeheftete Filter …) sind wählbar.
- **„Heute“** zeigt Tagesziel und nächste Aufgabe nur, solange Begrüßung bzw. Nächste Aufgabe ausgeblendet sind – jede Angabe steht genau einmal.
- **Eigene Auswahl bleibt:** Eine gespeicherte Reihenfolge ändert ein Update nicht; neue Kacheln kommen dort ausgeblendet hinzu. „Standard wiederherstellen“ im Dialog „Startseite einrichten“. „Startseite anpassen“ ist ein eingebetteter Bearbeitungsmodus (Ziehen, Alt+↑/↓, ganze Breite, aus-/einblenden).
- **Raster:** Spaltenzahl folgt der Fensterbreite (eine unter 980 px, zwei bis 1.500, darüber drei) oder fest; Ausführlichkeit normal (fünf Zeilen) oder kompakt (drei); Kalendervorschau als Monat, Woche oder nächste Termine.
- **Pinnwand-Vorschau** zeichnet die globale Fläche maßstäblich (höchstens 40 Karten) und öffnet sie per Klick.
- **Gismo** ([Entscheidung](decisions/ARBEITSBEGLEITER.md)): gezeichnete Figur ohne Datei; Zustände sorgt/freut/winkt/schläft/ruhig spiegeln den Bestand, nicht den Menschen. Pflege über Füttern, Spielen, Ruhen (Sättigung, Energie, Vertrauen), Zustand nur in den Einstellungen; ein Pflegeschritt aktualisiert nur die Balken, nie die ganze Startseite. In Leerzuständen still und klein (56 px), „Spielereien aus“ blendet ihn aus.
- **Rückmeldung beim Erledigen** (`animations_enabled`, Vorgabe an) in jedem Design; im Dopamin-Design als Stapel mit Kombo-Zähler.

## 8. Seiten, Notizen, Notizbuch, Galerie

- **Seite** (`page`, `PageEditor`): für lange, KI-erzeugte Berichte – Lesespalte bis 760 px (umschaltbar), endlos scrollend, keine Unterseiten (29.09.2026). Markdown-Kürzel beim Tippen, „/“ am Zeilenanfang öffnet die Blockauswahl, Enter setzt Listen und Aufgaben fort.
- **Blöcke:** Überschriften 1–4, Aufzählung, Nummerierung, Aufgabe, Zitat, Code, Trennlinie, Tabelle (ausgerichteter Text), Einzüge, Aufklappliste und Aufklappüberschrift (Zustand gespeichert), Hinweisblock. „Mehr › Gliederung“ springt zu Überschriften. Rechtsklickmenü und schwebende Formatleiste über einer Markierung (Blockart, B, I, U, S, Code, Markieren, Link).
- **Aufgaben in Seiten** sind echte Punkte der Seite (`item:<id>`): Abhaken im Text, Doppelklick öffnet die Details, Titeländerungen laufen in beide Richtungen, eine gelöschte Zeile legt den Punkt in den Papierkorb (Rückgängig holt ihn zurück). Seitenfelder: Titel, Beschreibung, Farbe, Labels, Erstellungsdatum.
- **Bilder in Seiten:** einfügen (Werkzeugleiste, „/“, Ziehen aus Finder/Explorer), Text davor und dahinter, links/mittig/rechts mit Umfluss, Größe über die Ecke (Seitenverhältnis bleibt), Rechtsklick für Umfluss und Breite, Entf entfernt nur das Bild aus dem Text.
- **Markdown:** hinein über „Aus Zwischenablage“, Datei › Importieren oder Einfügen; hinaus über Mehr › Als Markdown speichern/kopieren (Bilder in einen Ordner daneben). **`.glidepage`** exportiert und importiert Seiten und Bücher mit Anhängen; Kennungen werden neu vergeben, Aufgabenmarken ziehen nach. Mitgelieferte Seitenvorlagen: Bericht, Besprechung, Projektseite.
- **Notiz:** derselbe Editor ohne Aufgabenzeilen (`NoteEditor`); die Punktliste darüber erscheint erst mit dem ersten Punkt. „Mehr“ bietet Zeitstempel, Tagesabschnitt, Schreibimpuls.
- **Notizbuch:** neue Einträge sind datierte Notizen („Tagesnotiz · Datum“) oder datierte Zeichnungen, sortiert nach Momentdatum; Kopf mit Datum, Favorit, Stimmung, Ort; Zeitraumfilter. Vorlagen: Tagesnotiz, Dankbarkeit, Wochenrückblick, Jahresordner mit Quartalen.
- **Übersichten:** Seiten (Favoriten, Zuletzt geöffnet bis 12, alle Seiten), Notizen (Notizbücher, alle Notizen, ab sieben auch zuletzt bearbeitet), Zeichnungen, Bücher als Tabelle (Titel, Beschreibung, Farbe, Labels, Aufgaben, Erstellt). Listen und Ordner als Kartengalerie mit Archivschalter.
- **Galerie** (`gallery`): Bilder sind Anhänge der Liste mit Titel und Notiz; Kachelraster in drei Größen, Großansicht in der Fläche mit Blättern. Vorschauen nach Plattform siehe Abschnitt 13.

## 9. Pixel-Werkstatt

- **Zeichnung** als eigene Listenart, eingebettet im Inhaltsbereich; Größe 16, 32, 64 oder 128 Zellen je Seite, beim Anlegen fest.
- **Werkzeuge** mit Kontextleiste: Pinsel (B), Füllen (F), Pipette (I), Linie (L), Rechteck (U), Ellipse (E), Auswahl (S); Größe 1/2/4/8, Umriss/gefüllt, Symmetrie (M), Füllmuster. Umschalt hält Winkel und Quadrate.
- **Farben:** links Vorder-, rechts Hintergrundfarbe, X tauscht, D setzt zurück; Farbleiste mit Palette und den sieben zuletzt benutzten Farben; Umschalt+Klick ersetzt eine Farbe in der ganzen Zeichnung.
- **Ansicht:** Strg+Mausrad zoomt um den Zeiger, mittlere Maustaste verschiebt, Vorschau in Originalgröße (P), Kachelvorschau 3 × 3, Referenzbild mit Deckkraft (PNG, JPEG, HEIC, SVG …).
- **Rückgängig** je Aktion, höchstens 50 Schritte. Benannte Zwischenstände als Anhang (höchstens 10).
- **Paletten:** „Glide 32“ mitgeliefert; eigene speichern; ein- und ausgeben als `.gpl`/`.hex`, einlesen auch Adobe Swatch Exchange und Aseprite (nur Palette, höchstens 256 Farben).
- **Export:** PNG ganzzahlig vergrößert ohne Glättung (bis 2.048 px); ICO mit 16/32/48/256 px, Grund wahlweise durchsichtig (3.32.0). Glide-SVG und JSON (`hex8-row-v1`) für den Rundlauf.
- **Pixelsymbol:** eigene 16 × 16-Zeichnung im Listen- oder Ordnerobjekt (E-09), sichtbar in Seitenleiste, Übersicht und Suche.

## 10. Suche, Aktionen, Erinnerungen

- **Suche** über Seiten, Punkte und Aktionen: Strg/Cmd+O oder die Lupe ⌕ in der Kopfzeile, eingebettet unter dem Kopf; ohne Eingabe die zuletzt geöffneten Seiten; Umlaute wie ae/oe/ue/ss. Ein Klick außerhalb schließt sie. Eine Volltextsuche über Seiteninhalte gibt es noch nicht (G14).
- **Alle App-Aktionen** (⌘) gruppiert wie das Tastenkürzel-Fenster; eine Aktion ohne Gruppe erscheint sichtbar unter „Weitere Aktionen“ (die Prüfung verlangt, dass diese Gruppe leer bleibt).
- **Erinnerungen** relativ zur Fälligkeit oder fest, mit Zustellbeleg; Prüfung alle 15 Sekunden, solange Glide läuft. **Systemmitteilungen** (Einstellung, Vorgabe aus) über Tk 9, je Prüflauf eine Sammelmeldung; sonst Hervorheben im Dock bzw. in der Taskleiste. Keine Zustellung bei beendetem Programm ([Entscheidung](decisions/SYSTEMBENACHRICHTIGUNGEN.md)).

## 11. Import, Ausgabe und Austausch

- **Grundsatz:** Vorschau zuerst, ein Rückgängig-Schritt, nie über vorhandene Punkte schreiben; Punkte entstehen nur über `new_item`.
- **CSV-Import:** Kodierung, Trennzeichen und Kopfzeile werden erkannt, Spalten zugeordnet, Werte (Erledigt, Wichtigkeit, Art, Minuten, Ebene) geprüft; Ziel neue oder geöffnete Liste.
- **Kalenderdatei (ICS) importieren:** Vorschau mit Dateiname, Kalendername, Erzeuger und Terminzahl; Optionen Beschreibungen, Orte, Kategorien als Labels, Erinnerungen, Dauer als Aufwand, Abgesagtes überspringen; Zeitraum alles/ab heute/ab Datum. `SUMMARY` → Titel, `DTSTART` → Fälligkeit (ganztägig oder mit Uhrzeit), `PRIORITY` 1–4/5/6–9 → hoch/mittel/niedrig, `RRULE` (DAILY/WEEKLY/MONTHLY/YEARLY mit INTERVAL, BYDAY, UNTIL) → eine Aufgabe mit Wiederholung, `UID` → Duplikaterkennung. Unbekanntes wird gemeldet, nicht geraten.
- **Kalenderausgabe (ICS)** aus denselben Mengen wie der Druck; rein lesend, keine Synchronisierung.
- **Druck und PDF:** eigenständige HTML-Datei ohne externe Verweise, im Browser gedruckt oder als PDF gesichert; Pinnwand und Folien mit Karten und Verbindungen, Zeichnungen pixelscharf.
- **Sicherungen:** Teilbackup (`.glidebackup`, Listen und Ordner hinzufügen), Komplettbackup, App-Backup mit Einstellungen und Vorlagen (Inhaltsvorschau, Bereiche wählbar), portabler Vorlagenkatalog. Details: [Daten und Migration](06_DATA_BACKUP_MIGRATION.md).
- **KI-Austausch Stufe 1** über Dokumente statt Schnittstelle (Q3): `.glideexchange` mit eigener Formatnummer, „Für KI bereitstellen“, „KI-Ergebnis importieren“, „Austauschformat anzeigen“; Spezifikation in [Daten und Migration](06_DATA_BACKUP_MIGRATION.md#austauschformat-glideexchange).

## 12. Erscheinungsbild und Fenster

- **Designs** (eine Auswahl, Tabelle `DESIGNS`): Hell, Dunkel, Liquid Glass hell/dunkel, Dopamin, Kontrast hell/dunkel (farbenblindenfreundlich), Minimal hell/dunkel, Pixel (Pixelify Sans für Überschriften). Der Hell-/Dunkel-Schalter der Kopfzeile wechselt zum Gegenstück.
- **Kontrast:** jeder Text in jedem Design mindestens 4,5:1 (große Schrift 3:1), berechnet statt geraten.
- **Hintergrundverläufe:** je Design „Aus“ und fünf Verläufe, in einem Thread berechnet und im Systemcache abgelegt (die letzten sechs); eine Lesezone oben dämpft den Verlauf; Kacheln erhalten eine flache Milchglas-Tönung. Karten, Listen und Eingaben bleiben deckend.
- **Akzentfarbe** der Oberfläche färbt Logo und Akzente; das Logo steht links in der Kopfzeile ab 900 px Kopfbreite und öffnet „Über Glide“.
- **Farben nach Bedeutung:** Rot nur Löschen/Entfernen, Grün nur Bestätigen (auch Wiederherstellen), festes Lila für Hinzufügen/Neu/Nachzeichnen, Gelb für Hinweise und Mitteilungen, sonst neutral; Knöpfe mit „…“ sind neutral.
- **Feste Bestandteile:** Seitenleiste, Kopfzeile (feste Höhe) und Inhaltsfläche springen beim Ansichtswechsel nicht; die Werkzeugleiste nimmt den Platz fehlender Eingabe- oder Suchzeilen ein; die Inhaltskarte reicht bis zur Unterkante, Hinweis und Auswahlleiste stehen im Kartenfuß. Kein Ordnerpfad über dem Titel.
- **Kleine Fenster** (Mindestgröße 860 × 700): Was weicht, weicht ganz und bleibt über „⋯“, Kontextmenü, Menüleiste oder Kürzel erreichbar; nichts wird gequetscht oder angeschnitten. Gilt auch für jeden Dialog bei großer Schrift.
- **Dialoge** erscheinen erst fertig positioniert; jeder schließt mit Escape. Schaltflächen wachsen mit ihrer Beschriftung; Feldpaare stehen auf einer Linie (`FieldPairGrid`).
- **Hinweise:** höchstens ein Tooltip sichtbar, jeder Klick schließt ihn. Hinweiszeilen der Ansichten werden nach D11 einklappbar (noch offen, UX1); der Hinweisblock in Seiten bleibt unverändert (D06).

## 13. Grenzen

### Bewusste Grenzen je Funktion

| Bereich | Grenze |
|---|---|
| Zeichnung | 16–128 Zellen, eine bemalbare Ebene, höchstens 256 Farben, deckend weißer Grund; keine Vektorobjekte, Texte, Ebenen, Transparenz, Stiftdruck, Touchgesten, kein allgemeiner Fremd-SVG-Import. Mitgeliefert nur die eigene Palette |
| Seiten | ein Blatt ohne Unterseiten; Tabellen als ausgerichteter Text; Blöcke nicht einzeln mit der Maus ziehbar |
| Galerie und Vorschauen | Bilder sind lokale Anhänge; JPEG, HEIC, WebP, TIFF, BMP über das System (macOS `nsimage`/`sips`, Windows WIC, HEIC/WebP nur mit Store-Erweiterungen), unter Linux nur PNG, GIF, SVG |
| Kalender (ICS) | Import einer gegebenen Datei und Ausgabe als Datei; keine Synchronisierung, kein Abonnement, keine Teilnehmer, Ausnahmetermine oder VTODO; höchstens 2.000 Termine, 12 MB |
| CSV | Import mit Spaltenzuordnung; kein XLSX, keine Anhänge, Wiederholungen oder Erinnerungen aus Spalten, kein Abgleich mit Vorhandenem; 5.000 Zeilen, 64 Spalten, 12 MB |
| Druck und PDF | HTML-Druckansicht im Standardprogramm; kein eigener PDF-Schreiber, keine Druckerauswahl, ab 2.000 Punkten abgeschnitten |
| App-Backup | kein Cloudspeicher, kein Zeitplan, kein Zusammenführen, kein Passwortschutz |
| Änderungsverlauf | Aufgabenbestand, höchstens 15 Einträge und 15 Tage, abschaltbar; kein Wiederherstellen alter Werte |
| Planung | Bearbeitungstag und Aufwand erzeugen keine Fälligkeit; Kapazität je Wochentag, keine automatische Terminverteilung und keine Bewertung der arbeitenden Person |
| Gismo | spiegelt den Bestand, nie den Menschen; leitet aus Abschlüssen keine Bewertung ab |

### Bekannte Mängel und Prüflücken

- **Plattformen:** Abnahme nur auf macOS mit Python 3.14/Tk 9. Windows (Vorschauen über WIC, Systemmitteilungen, Ziehen aus dem Explorer, Lupe, Logo unter Tk 8.6) und Linux (Pixelschrift über Fontconfig nur nachgebildet geprüft) sind ungeprüft; ebenso DPI, mehrere Monitore und Screenreader.
- **Vorschauen:** offen sind JPEG unter Linux (N08) und SVG unter Tk 8.6. Die Großansicht vergrößert kleine Bilder nicht.
- **Bilder in Seiten:** Umfluss über Ränder nachgebildet; zwei Bilder auf gleicher Höhe können sich überlappen; Druck/PDF und „Markdown kopieren“ zeigen nur Dateinamen (B4). Oben am Textfeld bis zu 18 px Versatz beim Scrollen.
- **Seiten:** Titelbild fehlt (G09). Ältere Glide-Stände verwerfen die Blockarten `h4`, `toggle`, `toggle_closed`, `callout` (Text bleibt).
- **Milchglas:** keine echte Durchsicht; beim Scrollen gleichen sich die Flächen erst in der Ruhe an.
- **Seitenleiste:** jeder Baum scrollt für sich (B1).
- **Startseite:** Aufbau 507 ms (macOS, 1.000 Punkte), Ziel 150 ms nicht erreicht; Einstellungsfenster rund 2,1 s bis zur Anzeige.
- **Systemmitteilungen** erscheinen aus Python gestartet unter „Python“, nur aus dem Bundle unter „Glide“.
- **Tagesstände** der Sicherung: bis zu 14 zusätzliche Dateien im Datenordner (in Cloudordnern zählen sie mit).
- **Messungen** von Mindestgröße und Kontrast decken Widgets ab, nicht Texte auf Zeichenflächen (Pinnwandkarten, Kalenderzellen, Startseitengrafiken).
- **Kalender** ist noch ein modales Fenster (N04); **Aufgaben im Notiztext**, Verweise, Volltextsuche, Animation und Paket mit eigenem Python sind geplant, nicht vorhanden ([Entwicklungsplan](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md)).
