# Glide – kompakte Weitergabe an einen neuen Chat

Neu in 3.23.0: **46 Punkte aus einem Master-Arbeitsauftrag.** Die Erscheinung
lag an drei Stellen und liegt jetzt an einer; sieben Tabellen hatten sieben
Einrichtungen und haben jetzt eine; der Ansichtswechsel dauerte 336 ms und
dauert 129 ms; ein Austauschformat steht neben dem internen Datenformat. Dazu
ein Fehler, der zwei Versionen lang ein leeres Fenster zeigte, und das
Prüfwerkzeug, das ihn künftig findet. Kein Formatsprung.
[Abschlussbericht mit Rückführung auf alle 46 Punkte](Glide_Abschlussbericht_3.23.0.md).

Stand 18.09.2026 · Entwicklungsstand 3.23.0 · Aufgabenformat 16 · Einstellungen 2 · Vorlagen 2

Pfade und Links in diesem Dokument gelten relativ zum Ordner
`00_Arbeitsvorbereitung` der Arbeitsablage.

Umgesetzt sind Erinnerungen mit Dock-/Taskleistenaufmerksamkeit, Reiter und
Pinnwand, Schnellerfassung und gespeicherte Filter, „Mein Tag“ über den
Bearbeitungstag, die Tabellenansicht mit listenspezifischen Spalten,
Bearbeitungstag und Aufwand, Tagesplanung mit Tageskapazität, das vollständige
App-Backup mit Inhaltsvorschau, Druck- und PDF-Ausgabe, CSV-Import mit
Spaltenzuordnung, dauerhafter Änderungsverlauf, Kalenderausgabe und
-import als ICS, Checklisten je Aufgabe sowie seit 3.23 das Designsystem, die
Anzeigemodi der Listenansicht, das Glide-Austauschformat und die Pinnwand als
Arbeitsfläche mit Verbindungen, Vollbild und Druck. Alle Ansichten zeigen
dieselben Aufgabenobjekte, IDs, Termine, Wiederholungen und Anhänge.

Durchgehende Grundlage: verschachtelte Listen und Ordner, Aufgaben,
Long-Tasks, Gruppen, Überschriften und Unterpunkte, Fälligkeit mit Uhrzeit,
Wichtigkeit, sechs Wiederholungsarten, Erinnerungen innerhalb der laufenden
App, Labels, Farben, Beschreibungen und lokale Anhänge an Punkten, Listen und
Ordnern, Checklisten, Kalenderansicht, Suche und Offen-Filter,
Mehrfachauswahl, Ziehen, Rückgängig und Papierkorb, 16 Praxisvorlagen mit
eigenem Katalog, TXT-, CSV- und Markdown-Austausch, portable Aufgabenbackups
sowie sieben Designs mit Akzentfarbe und drei Schriftgrößen.

Kanonisch: `01_Repository/Glide/src/glide/app.pyw`. Startbare Kopie:
`07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.23.0.pyw` mit vollständigen
Ressourcen. Python/Tk, lokal ohne Konto oder neue Laufzeitabhängigkeit.

Prüfstand 3.23.0: **27 Suiten, vier Analysen**, Versions-, Fixture- und
Standprüfung sowie beide Reproduktionsabgleiche. Der maßgebliche Vollprüflauf
bestand am **18.09.2026 um 19:09 unter Windows** mit Python 3.12.10 und
Exitcode 0 – dreiundvierzig Schritte, davon zweiundvierzig ausgeführt;
übersprungen blieb allein die Sichtprüfung. Er brachte fünf Befunde, die eine
Linux-Vorabumgebung nicht zeigen kann; sie stehen unten unter „Fallen".
Offen bleiben die Sichtabnahme am Gerät, ein macOS-Lauf desselben Befehls,
DPI- und Mehrmonitorprofile, Screenreader, Langzeitbetrieb, Installer und
Signierung. [Manuelle Prüfung](Checklisten/Manuelle_Pruefung_3.23.0.md) ·
[Abnahme am Gerät](Checklisten/Abnahme_Windows_macOS_3.23.0.md).

[Designsystem 3.23](../01_Repository/Glide/docs/50_DESIGNSYSTEM_3.23.0.md) ·
[Leistung und Oberfläche 3.23](../01_Repository/Glide/docs/51_LEISTUNG_UND_OBERFLAECHE_3.23.0.md) ·
[Austauschformat 3.23](../01_Repository/Glide/docs/52_AUSTAUSCHFORMAT_3.23.0.md) ·
[Pinnwand 3.23](../01_Repository/Glide/docs/53_PINNWAND_ARBEITSFLAECHE_3.23.0.md) ·
[Anzeigemodi 3.23](../01_Repository/Glide/docs/54_ANZEIGEMODI_3.23.0.md) ·
[Technische Übergabe](../01_Repository/Glide/docs/09_PROJECT_HANDOFF.md) ·
[Prüfstand und Grenzen](../01_Repository/Glide/docs/07_QA_BERICHT.md).

## Wo liegt was

| Ort | Inhalt |
|---|---|
| `01_Repository/Glide/src/glide/app.pyw` | **kanonische Anwendung**, ein Monolith. Alles andere ist Kopie oder abgeleitet. |
| `01_Repository/Glide/AGENTS.md` | verbindliche Änderungsregeln. Vor jeder Änderung lesen. |
| `01_Repository/Glide/docs/` | Bedienverträge je Funktion (Dateiname trägt die Version ihrer Entstehung), Index, QA-Bericht, Entscheidungen, Archiv |
| `01_Repository/Glide/tests/integration/` | 27 Suiten; `tests/tools/` die Werkzeuge, `tests/fixtures/` Referenzformate und Beispielbestände |
| `00_Arbeitsvorbereitung/` | **diese Weitergabe** (genau eine aktive), Analysen, Notizen, Checklisten, Entscheidungen je Version |
| `05_Probelisten_Testdaten/` | Nutzerkopien der Probedateien mit eigener Prüfwege-Tabelle |
| `07_Python-Versionen/` | startbare Fassungen je Version samt `resources/` |
| `10_Dokumentation/`, `40_Store_Material/` | Vorlagenanleitung, Produktdatenblatt, Store-Arbeitsstände |
| `50_Ablage/` | Werkzeuge und Vorfassungen abgeschlossener Versionssprünge, QA-Nachweise, Screenshots |

In **jedem** Ordner gilt: überholte Fassungen liegen in `archiv/` beziehungsweise
`Archiv/` desselben Ordners, nichts wird gelöscht. Der Prüfstand verlangt, dass
**jede** Datei unter `docs/` – Archiv eingeschlossen – im Index
`docs/00_INDEX.md` steht.

## Datenregeln von 3.23.0

**Kein Formatsprung.** Aufgabenformat 16, Einstellungsformat 2, Vorlagenformat 2.

- `design` ist die einzige Quelle der Erscheinung. `theme`, `color_mode` und
  `glass_mode` bleiben als **abgeleitete** Werte in `settings.json` – damit
  eine ältere Fassung dieselbe Datei richtig liest. Geschrieben werden sie
  ausschließlich in `set_design`.
- `list_detail_mode` ist additiv; ein fehlender Wert bedeutet `standard` und
  damit genau die Ansicht aus 3.22.
- `pinboards[*].connections` speichert Verbindungen als Paar von
  Punktkennungen, nicht als gezeichnete Linie. Eine Verbindung ohne zwei
  vorhandene Karten wird beim Normalisieren verworfen.
- Der Austauschimport legt **ausschließlich** neue Listen, Ordner und Punkte
  an; vorhandene werden nie verändert. Scheitert das Speichern, gehen Listen,
  Ordner, Labels und der Rückgängig-Stapel exakt zurück.
- Der Aufbau-Zwischenspeicher lebt nur innerhalb eines Aufbaus. Außerhalb
  rechnet jede Abfrage frisch – deshalb kann er nichts Veraltetes liefern.

Die Datenregeln von 3.22 und früher gelten unverändert weiter; sie stehen in
den Technischen Fakten der jeweiligen Version unter `Notizen/`.

## Änderungsdisziplin

Vor Änderungen `AGENTS.md` lesen, aktuelle Tests ausführen und alle
App-Importe mit temporärem `GLIDE_DATA_DIR` isolieren – ein Import ohne diese
Isolierung arbeitet auf dem echten Nutzerdatenordner. Aufgabenmutationen über
`item_change`, Container über `sidebar_change`, Struktur über
`guarded_structural_change`, Dialoge über `run_modal`. Symbole aus `ICONS`.
Dokumentvorfassungen archivieren, nie überschreiben. Keine neue
Laufzeitabhängigkeit ohne dokumentierte Entscheidung. Nie echte Nutzdaten als
Testbestand öffnen.

**Neu seit 3.23:** Eine neue Methode gehört in die Klasse, die sie ruft –
`tests/tools/attributpruefung.py` prüft das. Eine neue Tabelle läuft über
`prepare_table`. Eine neue Farbe auf einer gemischten Fläche läuft über
`readable_text_color` oder `ensure_contrast`. Ein neues Datumsfeld bekommt
`attach_calendar_picker`.

## Fallen, die Zeit gekostet haben

Die Liste aus 3.21.4 gilt unverändert weiter (Zahlen in Zwecktexten,
Formatstufen in Prosa, Linktexte mit Versionsnummern, historische Dokumente
mit Gegenwartsaussagen, `mv -n`, Prüfläufe in UTC, pauschale Ersetzungen,
Fixture-Abgleich gegen die eigene Neuerzeugung, Indexpflicht). Neu dazu:

- **Ein AttributeError in einem Tk-Callback ist unsichtbar.** Der Spaltendialog
  öffnete sich zwei Versionen lang leer, weil `self.label(...)` in `ListApp`
  gerufen wurde – eine Methode, die es nur in `ItemWorkspace` gibt. Weder
  Syntaxprüfung noch Erreichbarkeitsanalyse finden so etwas. Seit 3.23 tut es
  `attributpruefung.py`.
- **`before=` bricht den ganzen Zeilenaufbau ab, wenn das Bezugswidget fehlt.**
  Seit Schaltflächen bei schmalem Fenster verschwinden, kann das passieren.
  `pack_relative` packt defensiv.
- **Ein Zwischenspeicher, der über seinen Anlass hinaus lebt, ist eine
  Zeitbombe.** Der erste Entwurf des Aufbau-Zwischenspeichers wurde per
  `after_idle` verworfen – und lieferte im Test veraltete Werte, sobald ein
  Bestand ohne Leerlauf geändert wurde. Er lebt jetzt ausschließlich innerhalb
  eines `render_pass()`.
- **`justify="left"` richtet Zeilen zueinander aus, nicht den Block im
  Widget.** Dafür ist `anchor` zuständig. Siebzehn Beschriftungen standen
  deshalb mittig, ohne dass es jemandem auffiel.
- **Bei `side="right"` steht das zuerst gepackte Widget am weitesten rechts.**
  Daran lag die vertauschte Reihenfolge der Tagespfeile.
- **`TZ` wirkt unter Windows nicht – und richtet dabei Schaden an.** Es gibt
  dort kein `time.tzset()`, und aus `Europe/Berlin` liest die Laufzeit keine
  benannte Zone, sondern baut eine eigene ohne Sommerzeitregel: „ope" mit
  +01:00, während in Berlin +02:00 galt. Der Prüfstand setzt `TZ` dort nicht
  mehr und **misst** den Versatz stattdessen.
- **Ein Erzeuger, der Text im Standardmodus schreibt, ist plattformabhängig.**
  Die vier Anhänge der Beispieldaten wuchsen unter Windows um ein Byte je
  Zeile, weil `write_text` ohne `newline="\n"` CRLF schreibt. Der
  Beispieldaten-Abgleich vergleicht Anhanggrößen und konnte dort deshalb **nie**
  gleich ausfallen. Behoben gehört so etwas in den Erzeuger; wer die Fixture
  neu erzeugt, dreht den Fehlschlag nur auf die andere Plattform.
- **Ein Abgleich, der nur „unterscheidet sich" meldet, kostet jedes Mal
  dieselbe Suche.** Beide Datenabgleiche nennen jetzt die ersten Fundstellen
  mit Pfad und beiden Werten. Ohne diese Änderung wäre der Zeilenende-Befund
  nicht zu finden gewesen.
- **Ohne Systemfokus schließt sich jedes Dropdown selbst.** `root.focus_get()`
  liefert unter Windows `None`, solange das Fenster nicht das aktive
  Systemfenster ist – im automatisierten Lauf steht die Konsole im
  Vordergrund. Eine Suite, die ein Popup prüft, muss den Fokus erzwingen,
  sonst prüft sie die Fensterverwaltung der Prüfmaschine.
- **Die Standprüfung erfasst die äußere Ablage, der Dokumentationsindex
  nicht.** Dreizehn Standangaben in `20_` bis `90_` standen auf der
  Vorversion, und zwei Verweise auf startbare Fassungen zeigten ins Archiv.
  Eine Prüfung nur gegen `docs/` sieht davon nichts.

## Nächste Schritte

1. Sichtabnahme am Gerät – die automatisierte Windows-Abnahme steht, die
   Blöcke B bis L der [Abnahme am Gerät](Checklisten/Abnahme_Windows_macOS_3.23.0.md)
   stehen aus; dazu ein macOS-Lauf desselben Befehls.
2. Endnutzer-Einstieg beim ersten Start.
3. Paketierung mit Installer und Signierung; daran hängen die
   Systembenachrichtigungen.

Danach die vier Funktionen aus Abschnitt 2.4 der
[Feature-Gap-Analyse](Glide_Feature_Gap_Analyse_2026-09-18.md): verknüpfte
Punkte, Wochenrückblick, Bereiche auf der Pinnwand, geführter Tagesbeginn.
[Offene Entscheidungen](Entscheidungen/Offene_Entscheidungen_3.23.0.md).
