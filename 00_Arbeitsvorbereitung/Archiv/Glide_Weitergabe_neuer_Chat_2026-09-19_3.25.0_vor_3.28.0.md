# Glide – kompakte Weitergabe an einen neuen Chat

Neu in 3.25.0: **vierundzwanzig Punkte unter einem Leitsatz** – „form follows
function“, zurück zu den Kernfunktionen. Menüs nach Zweck gruppiert, ein
Handbuch unter Hilfe (F1), aufklappbare Abschnitte in den Übersichten mit
einem eigenen Abschnitt „Nächste Aufgabe“, „Erweitert“ auch in abgeleiteten
Ansichten, zwei Designs ganz ohne Farbe, Rückmeldung auf jede Aktion,
Pinnwandverbindungen vor den Karten mit Kontextmenü und Rückweg, eine
Startseite mit Pinnwandvorschau und Begleiter. Kein Formatsprung.

**Der gemeldete Stillstand ist auf seine Ursache zurückgeführt und behoben** –
siehe „Fallen, die Zeit gekostet haben“. Seit 3.25 landet jeder Fehler aus
einem Tk-Callback in einem Fehlerprotokoll neben den Daten.

Stand 19.09.2026 · Entwicklungsstand 3.25.0 · Aufgabenformat 16 · Einstellungen 2 · Vorlagen 2

Pfade und Links in diesem Dokument gelten relativ zum Ordner
`00_Arbeitsvorbereitung` der Arbeitsablage.

Umgesetzt sind Erinnerungen mit Dock-/Taskleistenaufmerksamkeit, Reiter und
Pinnwand, Schnellerfassung und gespeicherte Filter, „Mein Tag“ über den
Bearbeitungstag, die Tabellenansicht mit listenspezifischen Spalten,
Bearbeitungstag und Aufwand, Tagesplanung mit Tageskapazität, das vollständige
App-Backup mit Inhaltsvorschau, Druck- und PDF-Ausgabe, CSV-Import mit
Spaltenzuordnung, dauerhafter Änderungsverlauf, Kalenderausgabe und -import als
ICS, Checklisten je Aufgabe, seit 3.23 das Designsystem, die Anzeigemodi der
Listenansicht und das Glide-Austauschformat seit 3.24 die Pinnwand als
Denkfläche mit Mehrfachauswahl, Verbindungsarten, Kartengrößen und globaler
Fläche sowie seit 3.25 das Handbuch, die beiden Minimaldesigns, die
Rückmeldung auf jede Aktion und der Begleiter auf der Startseite. Alle Ansichten zeigen dieselben Aufgabenobjekte, IDs, Termine,
Wiederholungen und Anhänge.

Kanonisch: `01_Repository/Glide/src/glide/app.pyw`. Startbare Kopie:
`07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.25.0.pyw` mit vollständigen
Ressourcen. Python/Tk, lokal ohne Konto oder neue Laufzeitabhängigkeit.

Prüfstand 3.25.0: **30 Suiten** (neu `test_features325.py` und die
Breitenprüfung `test_vollpruefung325.py`) und **fünf Analysen** (neu
`dublettenpruefung.py`). In einer Linux-Vorabumgebung (Python 3.12.3, Tk 8.6
unter Xvfb) laufen **40 von 41 Schritten** grün; Vorlagen-, Beispiel- und
Releasedaten wurden für 3.25.0 neu erzeugt, die Standprüfung lief über alle 31
aktiven Repositoriumsdokumente ohne Befund. Der eine fehlschlagende Schritt ist
die Dokumentprüfung: Der Index verweist auf rund 400 archivierte Dokumente, die
nur am Arbeitsgerät vollständig vorliegen. **Offen: der maßgebliche
Vollprüflauf auf dem Arbeitsgerät**, die Screenshot-Erzeugung und die
Sichtprüfung.

[Übersichtlichkeit und Hierarchie 3.25](../01_Repository/Glide/docs/57_UEBERSICHT_UND_HIERARCHIE_3.25.0.md) ·
[Startseite und Begleiter 3.25](../01_Repository/Glide/docs/58_STARTSEITE_UND_BEGLEITER_3.25.0.md) ·
[Navigation und Pinnwand 3.24](../01_Repository/Glide/docs/55_NAVIGATION_UND_PINNWAND_3.24.0.md) ·
[Startseite und Rückmeldung 3.24](../01_Repository/Glide/docs/56_STARTSEITE_UND_RUECKMELDUNG_3.24.0.md) ·
[Designsystem 3.23](../01_Repository/Glide/docs/50_DESIGNSYSTEM_3.23.0.md) ·
[Austauschformat 3.23](../01_Repository/Glide/docs/52_AUSTAUSCHFORMAT_3.23.0.md) ·
[Anzeigemodi 3.23](../01_Repository/Glide/docs/54_ANZEIGEMODI_3.23.0.md) ·
[Technische Übergabe](../01_Repository/Glide/docs/09_PROJECT_HANDOFF.md) ·
[Prüfstand und Grenzen](../01_Repository/Glide/docs/07_QA_BERICHT.md).

## Wo liegt was

| Ort | Inhalt |
|---|---|
| `01_Repository/Glide/src/glide/app.pyw` | **kanonische Anwendung**, ein Monolith. Alles andere ist Kopie oder abgeleitet. |
| `01_Repository/Glide/AGENTS.md` | verbindliche Änderungsregeln. Vor jeder Änderung lesen. |
| `01_Repository/Glide/docs/` | Bedienverträge je Funktion (Dateiname trägt die Version ihrer Entstehung), Index, QA-Bericht, Entscheidungen, Archiv |
| `01_Repository/Glide/tests/integration/` | 30 Suiten; `tests/tools/` die Werkzeuge, `tests/fixtures/` Referenzformate und Beispielbestände |
| `00_Arbeitsvorbereitung/` | **diese Weitergabe** (genau eine aktive), Analysen, Notizen, Checklisten, Entscheidungen je Version |
| `05_Probelisten_Testdaten/` | Nutzerkopien der Probedateien mit eigener Prüfwege-Tabelle |
| `07_Python-Versionen/` | startbare Fassungen je Version samt `resources/` |
| `10_Dokumentation/`, `40_Store_Material/` | Vorlagenanleitung, Produktdatenblatt, Store-Arbeitsstände |
| `50_Ablage/` | Werkzeuge und Vorfassungen abgeschlossener Versionssprünge, QA-Nachweise, Screenshots |

In **jedem** Ordner gilt: überholte Fassungen liegen in `archiv/` beziehungsweise
`Archiv/` desselben Ordners, nichts wird gelöscht. Der Prüfstand verlangt, dass
**jede** Datei unter `docs/` – Archiv eingeschlossen – im Index
`docs/00_INDEX.md` steht.

## Datenregeln von 3.25.0

**Kein Formatsprung.** Aufgabenformat 16, Einstellungsformat 2, Vorlagenformat 2.

- `overview_sections_closed` trägt die zugeklappten Abschnitte der Übersichten.
  Nur bekannte Kennungen überleben die Normalisierung – eine alte Datei kann
  damit keine Zeilen verbergen, die es nicht mehr gibt.
- `action_feedback` steuert den Umfang der Rückmeldung: `auto` (Vorgabe, im
  Dopamin-Design alles, sonst nur Meilensteine), `milestones` oder `all`. Der
  Hauptschalter `animations_enabled` bleibt darüber.
- `mascot_name` ist der vergebene Name des Begleiters, höchstens 24 Zeichen.
- Die Kachelschlüssel `boardpreview` und `mascot` sowie die Designschlüssel
  `minimal_light` und `minimal_dark` sind neu und additiv.
- Das **Fehlerprotokoll** `fehlerprotokoll.txt` liegt neben den Daten und
  wandert beim Wechsel der Datenablage mit. Es ist keine Einstellung und kein
  Teil eines Backups.

### Datenregeln von 3.24.0

- `pinboards[*].cards[*].scale` trägt den Kartenmaßstab (`large`, `normal`,
  `small`). Er hängt an der Karte, nicht am Punkt: Derselbe Punkt kann auf
  mehreren Pinnwänden verschieden groß sein. Ein fehlender Wert bedeutet
  `normal`.
- `pinboards[*].connections[*].style` trägt die Verbindungsart (`line`,
  `forward`, `backward`, `both`). Die Reihenfolge von `from`/`to` ist seit 3.24
  die Richtung und wird **nicht mehr sortiert**; doppelt bleibt eine Verbindung
  trotzdem ausgeschlossen, geprüft über das ungeordnete Paar. Ein unbekannter
  Wert fällt auf `line` zurück, die Verbindung bleibt.
- `pinboards["global"]` ist die Pinnwand über den gesamten Bestand. Sie wird
  beim additiven Import **nicht** übernommen – sonst bliebe offen, welche von
  beiden gilt.
- **`complete_backup_payload()` trägt einen Abschnitt `pinboards`.** Er steht
  neben den Aufgabenfeldern, nicht in ihnen. Beim vollständigen Import wird er
  unverändert übernommen, beim additiven über die neuen Kennungen nachgezogen
  (`pinboards_from_backup`, gespeist aus `prepare_additive_import`). Ältere
  Fassungen lesen dieselbe Datei und übergehen den Abschnitt.
- `startup_view` kennt acht Werte, `startup_list_id` die feste Liste;
  `animations_enabled`, `home_calendar_mode` und `home_density` sind additiv.
- Die Datenregeln von 3.23 und früher gelten unverändert weiter.

## Änderungsdisziplin

Vor Änderungen `AGENTS.md` lesen, aktuelle Tests ausführen und alle
App-Importe mit temporärem `GLIDE_DATA_DIR` isolieren. Aufgabenmutationen über
`item_change`, Container über `sidebar_change`, Struktur über
`guarded_structural_change`, Dialoge über `run_modal`. Symbole aus `ICONS`.
Eine neue Methode gehört in die Klasse, die sie ruft; eine neue Tabelle läuft
über `prepare_table`; eine neue Farbe auf gemischter Fläche über
`readable_text_color` oder `ensure_contrast`; ein neues Datumsfeld bekommt
`attach_calendar_picker`. Dokumentvorfassungen archivieren, nie überschreiben.

**Neu seit 3.24:** Eine zweispaltige Maske setzt ihre Mindestbreite nicht als
Zahl, sondern über `ResponsiveColumns.required_width(...)`. Eine Pinnwandaktion
gehört in `board_action_groups()` und damit in genau eine der drei Gruppen.

**Neu seit 3.25:** Zwei Felder nebeneinander stehen in einem `FieldPairGrid`,
nie in zwei selbstgepackten Zellen. Ein Menüeintrag entsteht in
`menubar_structure()`, nicht mit `add_command` – `build_menu` meldet jedes
Menü beim Theme an. Eine neue Aktion mit Rückmeldung bekommt eine Zeile in
`ACTION_FEEDBACK_TEXTS` und ruft `feedback(schluessel, anzahl)`; sie
entscheidet nicht selbst, ob gemeldet wird. Ein neuer Baustein der Oberfläche
gehört ins Handbuch (`MANUAL_SECTIONS`). Wiederholungen findet
`tests/tools/dublettenpruefung.py`.

## Fallen, die Zeit gekostet haben

Die Listen aus 3.21.4 und 3.23.0 gelten unverändert weiter. Neu dazu:

- **`pack_info()` kennt die Packreihenfolge nicht.** Es liefert Seite, Füllung
  und Abstände, aber nicht die Stelle unter den Geschwistern. Ein später wieder
  gepacktes Widget landet am Ende seines Elternteils – deshalb standen
  Kopfzeile und Eingabezeile nach dem Rückweg aus dem Vollbild unter der Liste.
  Wer etwas ausblendet und zurückholt, merkt sich zusätzlich den ersten
  nachfolgenden Nachbarn, der sichtbar bleibt, und packt mit `before=`.
- **Eine Dichteregelung, die neu packt, setzt Abstände neu.** Das Zahnrad stand
  acht Pixel vor der rechten Flucht, weil `sync_header_density` es bei jedem
  Stufenwechsel mit `padx=(0, 8)` neu packte. Der Aufbau war richtig; die
  Korrektur danach war es nicht.
- **Eine neue Ansicht braucht eine Zeile in der Zuordnung der Seitenleiste.**
  Fehlt sie, fällt `update_sidebar_list` auf „die zuletzt geöffnete Liste“
  zurück, markiert deren Zeile – und das Auswahlereignis verlässt die gerade
  geöffnete Ansicht sofort wieder. Genau das passierte der globalen Pinnwand.
- **Eine Aktion der Arbeitsfläche darf nicht direkt die Kartenauswahl lesen.**
  Im Punktreiter gibt es keine Karten; `active_ids()` beantwortet die Frage für
  beide Betriebsarten. Ohne sie wirkte „Erledigt umschalten“ im Reiter auf
  nichts.
- **Neue Startseitenkacheln bleiben ohne `home_tile_order` aus.** Die
  Normalisierung fügt jede Kachel, die es vorher nicht gab, der Ausblendliste
  hinzu, solange keine Reihenfolge gespeichert ist. Wer im Test nur
  `home_tiles_hidden` setzt, sieht beim nächsten Speichern nichts mehr.
- **Die Standprüfung ist erst am Gerät vollständig.** Eine Vorabumgebung
  kennt nur die Ordner, die jemand dorthin gestellt hat – 72 von 129
  Dokumenten. Fünf READMEs in `assets/`, `packaging/`, `50_Ablage/QA/` und
  `50_Ablage/Screenshots/` standen zwei Versionssprünge lang auf 3.23.0, weil
  sie in keinem Vorablauf vorkamen. Ein grüner Lauf über einen Teilbaum sagt
  nichts über die Dokumente, die dieser Teilbaum nicht enthält; die **Zahl der
  geprüften Dokumente** ist deshalb die eigentliche Aussage des Laufs.
- **Ein plattformgebundener Zweig in einer Suite ist eine blinde Stelle.**
  `test_glide.py` maß die Textflucht des Systembereichs an der Eingangszeile,
  die 3.24 entfernt hat – in einem `if os.name == "nt"`-Block. Unter Linux
  läuft er nicht, unter Windows scheiterte er sofort. Dieselbe Datei prüft
  weiter oben, dass es diese Zeile nicht mehr gibt; die beiden Stellen
  widersprachen sich, und nur eine war je zu sehen. Eine Geometriezusicherung
  nennt deshalb keine Navigationszeile beim Namen, sondern nimmt die erste
  vorhandene. Und: Die Vorabumgebung ersetzt den Lauf am Gerät nicht.
- **Eine `.pyw` hat keinen `stderr`.** Unter `pythonw.exe` sind `sys.stdout`
  und `sys.stderr` `None`. Tkinter meldet jeden Callback-Fehler genau dorthin –
  die Meldung scheitert dann selbst, **innerhalb** des Tcl-Aufrufs, und die
  Ereignisschleife bleibt stehen. Windows zeichnet die Fläche eines Fensters,
  das seine Nachrichten nicht mehr verarbeitet, weiß. Das war der gemeldete
  Stillstand mit weißer Kopfleiste. Seit 3.25 sichert `_ensure_streams()` die
  Ströme, und `report_callback_exception` schreibt ins Fehlerprotokoll.
  **Wer einen gemeldeten Fehler untersucht, fragt zuerst nach dieser Datei.**
- **Eine Ansicht ohne Seitenleistenzeile braucht keine Ersatzmarkierung.**
  „Verspätet“ verlor seine Zeile in 3.24; die Seitenleiste markierte
  ersatzweise die erste, und deren Auswahlereignis warf die Ansicht im nächsten
  Leerlauf auf die Startseite. Sichtbar war das erst nach einem `update()` –
  die bestehende Zusicherung im Test blieb deshalb grün. Jetzt gibt es eine
  Ersatzmarkierung nur noch, wenn wirklich nichts geöffnet ist.
- **Eine Schaltflächenbreite ist keine Zahl, sondern eine Messung.** Wird die
  Beschriftung länger oder die Schrift größer, läuft der Text sonst über die
  Fläche hinaus und wird an beiden Enden abgeschnitten.
- **Eine Linie zwischen zwei Karten endet am Rand, nicht im Mittelpunkt.**
  Sonst liegt sie samt Pfeilspitze unter beiden Karten, und die Richtung ist
  nicht zu erkennen.
- **Gruppieren kostet Höhe.** Der erste Entwurf der gruppierten
  Pinnwandaktionen hatte drei Überschriften und drei Reihen – die Fläche
  schrumpfte bei 860×700 auf sieben Pixel. Ordnung entsteht hier nicht durch
  mehr Beschriftung, sondern durch weniger sichtbare Schaltflächen.

## Nächste Schritte

1. **Vollprüflauf am Gerät** (`python tests/tools/pruefen.py --modus voll
   --protokoll tests/qa-3.25.0/abschluss --timeout 900`) und die manuelle
   Prüfung nach [Manuelle Prüfung 3.25.0](Checklisten/Manuelle_Pruefung_3.25.0.md).
   Wichtigster Punkt: der Nachweis, dass der Stillstand mit weißer Kopfleiste
   nicht wiederkehrt – und, falls doch, der Inhalt des Fehlerprotokolls.
1a. **Vier Entscheidungen** in
   [Offene Entscheidungen 3.25.0](Entscheidungen/Offene_Entscheidungen_3.25.0.md):
   Assets für den Begleiter, Vorgabe der Rückmeldung, Akzentton in den
   Minimaldesigns, Umgang mit dem Fehlerprotokoll.
2. Endnutzer-Einstieg beim ersten Start.
3. Paketierung mit Installer und Signierung; daran hängen die
   Systembenachrichtigungen.

Danach die verbliebenen Funktionen aus Abschnitt 2.4 der
[Feature-Gap-Analyse](Glide_Feature_Gap_Analyse_2026-09-18.md): verknüpfte
Punkte, Wochenrückblick, geführter Tagesbeginn. „Bereiche auf der Pinnwand“ ist
mit den Kartengrößen und der globalen Fläche teilweise beantwortet.
