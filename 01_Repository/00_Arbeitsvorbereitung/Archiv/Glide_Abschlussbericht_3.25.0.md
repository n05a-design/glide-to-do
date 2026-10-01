# Abschlussbericht – Glide 3.25.0

Stand: 19.09.2026 · Glide 3.25.0 · Aufgabenformat 16 · Einstellungen 2 · Vorlagen 2

Auftrag vom 19.09.2026: „3.25 fokussiert auf Bug-Fixes, Anpassungen wie
Übersichtlichkeit, bessere Hierarchie ganz im Sinne ‚form follows function‘ –
ich möchte eine minimalistischere Benutzeroberfläche, um wieder auf die
Kernfunktionen zurückzukommen.“

**Kein Formatsprung.** Aufgabenformat 16, Einstellungsformat 2, Vorlagenformat 2.

## Punkt für Punkt

### 1. Allgemein

| Nr. | Auftrag | Stand | Wie |
|---|---|---|---|
| 1.1 | Tagesziel und Tageskapazität an der Unterkante ausrichten | umgesetzt | `FieldPairGrid` – Beschriftung und Feld in getrennten Rasterzeilen |
| 1.2 | „Erweitert“ in „Mein Tag“ zeigt Info statt Maske | umgesetzt | Maske öffnet mit vorbelegtem Bearbeitungstag |
| 1.3 | Dasselbe in „In Bearbeitung“ und „Labels“ | umgesetzt | Labelansicht belegt das Label der Gruppe vor |
| 1.4 | Anzeige-Panel zu weit rechts, zu viel Text | umgesetzt | `align="auto"` im Dropdown, fünf einzeilige Erklärungen |
| 1.5 | Ansicht „nächste Aufgabe“ anpassen, von der Startseite verlinken | umgesetzt | Eigener Abschnitt, Kachel „Nächste Aufgabe“, `open_next_task` |
| 1.6 | Eingang in „Mein Tag“ einklappbar | umgesetzt | Abschnitte sind Elternzeilen; Zustand in den Einstellungen |
| 1.7 | Buttons in „Drucken und PDF“ abgeschnitten | umgesetzt | Schaltflächen messen ihre Beschriftung selbst |
| 1.8 | In „Über Glide“ Arbeitsdateien verschieben | umgesetzt | Drei Folgeaktionen über `themed_message_dialog(extra_buttons=…)` |
| 1.9 | Menüs besser gruppieren | umgesetzt | `menubar_structure()`, sechs Gruppen in „Ansicht“ statt 25 Einträgen |
| 1.10 | Handbuch unter Hilfe | umgesetzt | 9 Bereiche, 63 Zeilen, Suchfeld, F1 |
| 1.11 | Minimal dark und Minimal light | umgesetzt | Echte Neutraltöne, Kontrast gerechnet und geprüft |
| 1.12 | Dopamin-Animation auf jede Aktion | umgesetzt | `feedback()` mit 23 Vorgängen, drei Stufen |

### 2. Erweiterte Eingabe

| Nr. | Auftrag | Stand | Wie |
|---|---|---|---|
| 2.1 | Dialoge breiter, Spalten ausrichten | umgesetzt | Spaltenmindestbreite 380 → 440, `FieldPairGrid` in Punkt- und Planungsmaske |
| 2.2 | Abgetrennter Bereich „nächste Aufgabe“ | umgesetzt | Erster Abschnitt in „In Bearbeitung“, mit `task_urgency_rank` |

### 3. Pinnwand

| Nr. | Auftrag | Stand | Wie |
|---|---|---|---|
| 3.1 | Pfeile hinter den Karten | umgesetzt | `border_point`, Linien vor den Karten, schrumpfende Spitze |
| 3.2 | Rückweg aus der globalen Pinnwand | umgesetzt | „◂ Übersicht“ als erste Fläche der Reiterzeile |
| 3.3 | Reiter zu wenig Innenabstand, Text zu lang | umgesetzt | 14 Zeichen am Wortende, 22 Pixel je Seite |
| 3.4 | Punkte per Kontextmenü bearbeiten | umgesetzt | Rechtsklick wählt die Karte und zeigt ihre Aktionen |

### 4. Startseite

| Nr. | Auftrag | Stand | Wie |
|---|---|---|---|
| 4.1 | Vorschaukachel der Pinnwand | umgesetzt | `BoardPreview` mit echten Positionen und Verbindungen |
| 4.2 | Maskottchen als Tamagotchi-Kachel, Anforderungen an die Daten | umgesetzt | `MascotCanvas` mit fünf Zuständen; Lieferliste und zwei Beispielaufträge in `ARBEITSBEGLEITER.md` |
| 4.3 | Begrüßungsbereich aufräumen | umgesetzt | Vier Flächen plus „Weitere …“ in drei Gruppen |

### 5. Debugging und Prüfung

| Nr. | Auftrag | Stand | Wie |
|---|---|---|---|
| 5.1 | Testumfang erweitern | umgesetzt | 28 → **30 Suiten**, 4 → **5 Analysen**; neue Breitenprüfung |
| 5.2 | App hängt, Kopfleiste wird weiß | **Ursache gefunden und behoben** | Siehe unten |
| 5.3 | Codebasis auf Dubletten prüfen | umgesetzt | Neues Werkzeug; vier gemeinsame Bausteine entstanden |

## Der Stillstand – die Ursache

Glide startet als `.pyw`, also unter `pythonw.exe`. Dort sind `sys.stdout` und
`sys.stderr` **`None`**. Tkinter meldet jeden Fehler aus einem Callback über
`traceback.print_exception(..., file=sys.stderr)`; die Meldung scheitert damit
selbst mit einem `AttributeError`, und zwar **innerhalb** des Tcl-Aufrufs. Der
Interpreter bekommt einen Fehler in der Fehlerbehandlung, die Ereignisschleife
verarbeitet nichts mehr – und Windows zeichnet die Fläche eines Fensters, das
seine Nachrichten nicht mehr verarbeitet, weiß.

Sichtbar war die letzte Stufe, verursacht hat es die erste. Jeder beliebige
Fehler an jeder beliebigen Stelle konnte den Stillstand auslösen; deshalb
„manchmal“ und deshalb kein Muster.

Behoben in drei Schichten – Ströme sichern, Fehler protokollieren, modale
Dialoge gegen ein gescheitertes `grab_set` absichern. Der Fehler bleibt
sichtbar (Hilfe → Fehlerprotokoll öffnen), hält die Anwendung aber nicht mehr
an. **Tritt der Stillstand erneut auf, steht die Ursache jetzt in einer Datei.**

## Weitere behobene Fehler

| Fehler | Ursache |
|---|---|
| Abgeschnittene Schaltflächen | Breite als Zahl statt gemessen |
| Pfeile hinter den Karten | Linie von Mittelpunkt zu Mittelpunkt |
| „Verspätet“ sprang zur Startseite | Ersatzmarkierung in der Seitenleiste, deren Auswahlereignis die Ansicht verließ |
| Versetzte Eingabefelder | Beschriftung und Feld in derselben Rasterzelle |
| `unknown color name` | Unbekannter Themeschlüssel ging ungeprüft an die Zeichenfläche |
| Beispieldatei unter Linux nicht auffindbar | Groß-/Kleinschreibung im Dateinamen |

## Codebasis

`dublettenpruefung.py` fand **14 Fundstellen mit 21 vermeidbaren
Wiederholungen**. Daraus entstanden vier gemeinsame Bausteine:

| Baustein | Vorher |
|---|---|
| `finish_page_switch()` | 4 Kopien à 12 Zeilen |
| `rounded_rect_points()` | 3 Kopien à 14 Zeilen |
| `reveal_tree_row()` | 2 Kopien, eine ohne Fehlerbehandlung |
| `GLASS_LAYERS` | 2 Zweige mit identischer Rechnung |

Danach: **9 Fundstellen mit 13 Wiederholungen**. Der Rest sind Farbtafeln und
Erstauf-Initialisierung – Daten und bewusst ausgeschriebene Parallelzweige.
Dass die Farbtafeln unverändert sind, ist belegt: alle neun Designs vor und
nach dem Umbau vollständig ausgegeben und verglichen.

Weitere zusammengefasste Stellen aus dieser Version: `build_menu`,
`restore_focus`, `dialog_color`, `FieldPairGrid`, `tab_label`,
`themed_message_dialog(extra_buttons=…)`, `task_urgency_rank`.

## Prüfstand

| | Vorher | Jetzt |
|---|---|---|
| Suiten | 28 | **30** |
| Analysen | 4 | **5** |
| Schritte im Schnellmodus | 39 | **41** |

In der Linux-Vorabumgebung laufen **40 von 41 Schritten** grün. Der eine
fehlschlagende Schritt ist die Dokumentprüfung: Der Index verweist auf rund
400 archivierte Dokumente, die nur am Arbeitsgerät vollständig vorliegen.

## Was offen bleibt

1. **Der maßgebliche Vollprüflauf am Arbeitsgerät** –
   `python tests\tools\pruefen.py --modus voll --protokoll tests\qa-3.25.0\abschluss --timeout 900`.
2. **Die manuelle Prüfung** nach
   [Manuelle Prüfung 3.25.0](Checklisten/Manuelle_Pruefung_3.25.0.md) – elf
   Abschnitte, beginnend mit dem Nachweis, dass der Stillstand weg ist.
3. **Vier Entscheidungen** in
   [Offene Entscheidungen 3.25.0](Entscheidungen/Offene_Entscheidungen_3.25.0.md):
   Assets für den Begleiter, Vorgabe der Rückmeldung, Akzentton in den
   Minimaldesigns, Umgang mit dem Fehlerprotokoll.
