# Glide – kompakte Weitergabe an einen neuen Chat

Neu in 3.24.0: **zwanzig Punkte aus einem Arbeitsauftrag.** Die Seitenleiste
trägt sechs Zeilen statt acht; Eingang und „Verspätet“ sind Abschnitte ihrer
Ansicht geworden. Die Pinnwand kennt Mehrfachauswahl, gerichtete Verbindungen,
drei Kartengrößen und eine globale Fläche über den gesamten Bestand – und ihre
Anordnung reist erstmals im Komplettbackup mit. Dazu die Ansicht beim Öffnen
mit acht Zielen statt dreier, vier neue Startseitenkacheln und eine bewegte
Rückmeldung, die es in jedem Design gibt. Kein Formatsprung.

Stand 19.09.2026 · Entwicklungsstand 3.24.0 · Aufgabenformat 16 · Einstellungen 2 · Vorlagen 2

Pfade und Links in diesem Dokument gelten relativ zum Ordner
`00_Arbeitsvorbereitung` der Arbeitsablage.

Umgesetzt sind Erinnerungen mit Dock-/Taskleistenaufmerksamkeit, Reiter und
Pinnwand, Schnellerfassung und gespeicherte Filter, „Mein Tag“ über den
Bearbeitungstag, die Tabellenansicht mit listenspezifischen Spalten,
Bearbeitungstag und Aufwand, Tagesplanung mit Tageskapazität, das vollständige
App-Backup mit Inhaltsvorschau, Druck- und PDF-Ausgabe, CSV-Import mit
Spaltenzuordnung, dauerhafter Änderungsverlauf, Kalenderausgabe und -import als
ICS, Checklisten je Aufgabe, seit 3.23 das Designsystem, die Anzeigemodi der
Listenansicht und das Glide-Austauschformat sowie seit 3.24 die Pinnwand als
Denkfläche mit Mehrfachauswahl, Verbindungsarten, Kartengrößen und globaler
Fläche. Alle Ansichten zeigen dieselben Aufgabenobjekte, IDs, Termine,
Wiederholungen und Anhänge.

Kanonisch: `01_Repository/Glide/src/glide/app.pyw`. Startbare Kopie:
`07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.24.0.pyw` mit vollständigen
Ressourcen. Python/Tk, lokal ohne Konto oder neue Laufzeitabhängigkeit.

Prüfstand 3.24.0: **28 Suiten** (neu `test_features324.py`) und vier Analysen.
In einer Linux-Vorabumgebung (Python 3.12.3, Tk 8.6 unter Xvfb) sind alle
Suiten sowie Attribut-, Struktur- und Erreichbarkeitsanalyse mit Exitcode 0
gelaufen; Vorlagen- und Releasedaten wurden für 3.24.0 neu erzeugt, die
Standprüfung lief ohne Befund. **Offen: der maßgebliche Vollprüflauf auf dem
Arbeitsgerät**, die Screenshot-Erzeugung und die Sichtprüfung.

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
| `01_Repository/Glide/tests/integration/` | 28 Suiten; `tests/tools/` die Werkzeuge, `tests/fixtures/` Referenzformate und Beispielbestände |
| `00_Arbeitsvorbereitung/` | **diese Weitergabe** (genau eine aktive), Analysen, Notizen, Checklisten, Entscheidungen je Version |
| `05_Probelisten_Testdaten/` | Nutzerkopien der Probedateien mit eigener Prüfwege-Tabelle |
| `07_Python-Versionen/` | startbare Fassungen je Version samt `resources/` |
| `10_Dokumentation/`, `40_Store_Material/` | Vorlagenanleitung, Produktdatenblatt, Store-Arbeitsstände |
| `50_Ablage/` | Werkzeuge und Vorfassungen abgeschlossener Versionssprünge, QA-Nachweise, Screenshots |

In **jedem** Ordner gilt: überholte Fassungen liegen in `archiv/` beziehungsweise
`Archiv/` desselben Ordners, nichts wird gelöscht. Der Prüfstand verlangt, dass
**jede** Datei unter `docs/` – Archiv eingeschlossen – im Index
`docs/00_INDEX.md` steht.

## Datenregeln von 3.24.0

**Kein Formatsprung.** Aufgabenformat 16, Einstellungsformat 2, Vorlagenformat 2.

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
- **Gruppieren kostet Höhe.** Der erste Entwurf der gruppierten
  Pinnwandaktionen hatte drei Überschriften und drei Reihen – die Fläche
  schrumpfte bei 860×700 auf sieben Pixel. Ordnung entsteht hier nicht durch
  mehr Beschriftung, sondern durch weniger sichtbare Schaltflächen.

## Nächste Schritte

1. **Vollprüflauf am Gerät** (`python tests/tools/pruefen.py --modus voll
   --protokoll tests/qa-3.24.0/abschluss`) und die Sichtabnahme der neuen
   Bedienung: Mehrfachauswahl mit Maus, Pfeilspitzen und Kartengrößen auf einer
   vollen Fläche, Arcade-Eindruck des Dopamin-Designs, Breite der
   zweispaltigen Masken.
2. Endnutzer-Einstieg beim ersten Start.
3. Paketierung mit Installer und Signierung; daran hängen die
   Systembenachrichtigungen.

Danach die verbliebenen Funktionen aus Abschnitt 2.4 der
[Feature-Gap-Analyse](Glide_Feature_Gap_Analyse_2026-09-18.md): verknüpfte
Punkte, Wochenrückblick, geführter Tagesbeginn. „Bereiche auf der Pinnwand“ ist
mit den Kartengrößen und der globalen Fläche teilweise beantwortet.
