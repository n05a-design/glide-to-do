# Codeprüfung und Prüfprozess

Stand: 04.09.2026 · Glide 3.2.0 · Datenformat 10. Fundstellen beziehen sich auf
den Ausgangsstand `src/glide/app.pyw` vor eventuellen Symbolkorrekturen.

## Ausgangslage der Analysewerkzeuge

Die beiden vorhandenen Analysewerkzeuge wurden vor Änderungen ausgeführt. Logs:
`baseline/analyse_statisch.log`, `baseline/analyse_erreichbarkeit.log`.

| Kennzahl | Historischer Bericht `docs/08_CODE_BEFUND.md` | Gemessen 3.2.0 |
|---|---:|---:|
| Zeilen | 14.704 | 14.591 |
| Funktionen/Methoden | 530 | 539 |
| Konstanten | 133 | 133 |
| Erreichbar ab Start | 497/512 | 508/520 |
| Funktionen >80 Zeilen | 26 | 25 |
| Gleiche Textblöcke ≥6 Zeilen | 111 | 102 |
| Strukturgleiche Methodengruppen | nach 3.1.0: 0 | 0 |
| Breite `except Exception` | 20 | 18 |
| `insert_tree_items` | 144 Zeilen, 9 Ebenen | 146 Zeilen, 9 Ebenen |

Nie genannte Funktionen/Konstanten: jeweils 0. Nackte `except`: 0. Auskommentierte
Codezeilen: 2. TODO/FIXME/HACK, Debug-`print`, drei aufeinanderfolgende Leerzeilen:
jeweils 0. „Nur einmal benutzt“: 111 Funktionen. Die konkreten historischen
Funktionslängen `open_calendar_view` und `open_label_manager` sind heute 348 und
186 statt 349 und 187 Zeilen. Die alten Zahlen sind keine aktuellen Fehler.

Alle sechs als nicht erreichbar und ungetestet gemeldeten Namen haben echte
Aufrufer: `LabelChip.set_colors` (2641), `format_file_size` (3215),
`_store_pending_attachments` (3289), `_apply_windows_chrome_theme` (8535),
`refresh_scrollbar_state` (8876), `get_app_data_dir` (97). Die Werkzeuge übersehen
unter anderem verschachtelte Callbacks und den Moduleinstieg. Keine dieser
Funktionen wurde entfernt. 21 angeblich ungelesene und 26 angeblich ungesetzte
Attribute bleiben Heuristik, keine bewiesenen Fehler. Ein Teil davon sind
Tk-Methoden oder aufgerufene Methodenattribute.

Der Bericht 08 ist historisch zu lesen: seine offenen Emoji-Aussagen betreffen
zum Teil bereits ersetzte Anhang-/Kalendersymbole. Ein Beschreibungs-Emoji ist im
Ausgangscode jedoch weiterhin vorhanden. Eine „Phase 11“ ist in der aktuellen
Auditdatei nicht enthalten; ohne Git-Historie lässt sich verlorener Inhalt nicht
rekonstruieren. `audit_app.py` gibt bei vorhandenen Befunden bereits Exitcode 1
zurück – die gegenteilige Annahme gilt für den vorliegenden Stand nicht.

## Belegte Befunde, keine Produktionskorrektur in diesem Teilauftrag

| Symptom | Bereich/Ursache | Maßnahme | Status und nächster Test |
|---|---|---|---|
| 20 Labels werden nach Wechsel auf Long-Task zu 21 | `sync_item_kind_label`, 9211–9226: Systemlabel wird ohne Größenprüfung angehängt; `set_item_kind`, 9178–9198, ruft den Abgleich auf | Mit isoliertem Modul und 20 realen Labels reproduziert; keine Labels stillschweigend entfernt | **GEMELDET**, wichtig. Fachliche Grenze für Systemlabels festlegen; danach alle Artwechsel-/Importwege prüfen |
| Gültiger Punktbaum kann durch Verschieben die Ladetiefe überschreiten | `make_subitem`, 12811–12846, prüft Selbst-/Nachfahrenbezug, nicht `MAX_ITEM_DEPTH`; auch `add_child_item` 11803–11826 und TXT-Baumaufbau 14325–14332 ohne entsprechende Tiefeprüfung | Gültige Kette bis Tiefe 98 plus separater Unterbaum bis Tiefe 2 erzeugt; `normalize_items` zunächst erfolgreich. Verschieben des Unterbaums unter das letzte Kettenglied liefert True; neue Tiefe 101 wird anschließend von `normalize_items` abgelehnt | **GEMELDET**, wichtig und für extreme Verschachtelung datenkritisch. Gemeinsame Prüfung vor allen tiefenerhöhenden Mutationen nötig; UI-End-to-End des Extremfalls noch offen. Kein einseitiger Umbau vorgenommen |
| Emoji trotz verbindlicher Textsymbol-Regel | `insert_tree_items` 10762 setzt den Beschreibungshinweis auf 📝 außerhalb `ICONS` | An Hauptbearbeitung gemeldet, keine eigenständige App-Änderung | **GEMELDET**; sämtliche produktiven Fundstellen und Regressionstest durch Hauptbearbeitung klären |

Die Tiefenreproduktion lief nur im isolierten Arbeitsspeicher; es wurde kein
Nutzerdatenbestand oder defektes Benutzerbackup erzeugt. Die Labelreproduktion
ergab ausdrücklich `20` vor und `21` nach dem Artwechsel. Zusätzlich wurde der
echte Aktionspfad mit einem isolierten Tk-Fenster geprüft: ausgewählten Punkt
über `convert_selected_kind(ITEM_KIND_LONG)` umwandeln, Speicherdatei lesen.
Ergebnis: **21 Labels im Punkt und 21 Labels tatsächlich gespeichert**.
Damit ist der Grenzübertritt auch über die produktive Kontextmenü-Aktion
belegt. Die Auslösung erfolgte durch Methodenaufruf, nicht per simuliertem
Mausklick. Bestehende Labels dürfen bei einer späteren Korrektur nicht einfach
abgeschnitten werden.

## Geprüfte Mechanismen und verbleibende Unsicherheiten

- **Dialoge:** einziger echter `wait_window` in `run_modal` (2281), kein
  `wait_variable`. Zusätzliche Griffe sind Popup öffnen/schließen (1146,
  1210–1224), native Dateiauswahl mit `finally`-Rückgabe (3222–3235), Kalender-
  Wiederherstellung (3677–3715) und Kontextmenü-Freigabe. Das Popup ist
  ereignisgesteuert und wartet nicht in einer separaten Schleife. Das bekannte
  Einfrieren bleibt **NICHT VERIFIZIERT**; dieser Lauf reproduziert es nicht.
- **`insert_tree_items`:** Filter, Überschriften-Zähler, Gruppen, Farbvorrang,
  Long-Task-Folgezeilen und rekursiver Aufbau gelesen. Außer dem Beschreibungs-
  Emoji kein reproduzierter neuer Darstellungs- oder Datenverlustfehler. Die
  hohe Verschachtelung bleibt ein Wartungsrisiko, kein Auftrag zur Aufteilung.
- **Aktive Liste:** `set_active_list` (4669–4699) setzt ID, Punktreferenz und
  Titel gemeinsam. Laden, Import, Papierkorb und Undo setzen vor Neuaktivierung
  die ID bewusst auf `None`. Erststart-/Fehlerlisten übernehmen den bestehenden
  Titel. Kein produktiver Aufruf gefunden, der die aktive ID von Hand auf eine
  andere gültige Liste setzt und anschließend mit altem Titel speichert.
  `current_list` (4651–4659) kann bei einer bereits ungültigen ID auf die erste
  Liste wechseln, ohne Titel/Punktreferenz mitzuziehen: **Verdacht bei verletzter
  interner Vorbedingung**, kein normaler UI-Weg nachgewiesen.
- **Zeitgeber:** Windows-Retries (8522–8545), Scrollbar (8865–8881), Autosave
  (9816–9844) und Long-Task-Reflow (11005–11026) registrieren/entfernen IDs;
  `cancel_pending_callbacks` (9047–9059) räumt die zentrale Sammlung auf. Der
  Umbenennungszeitgeber (5595) wird separat durch `_cancel_sidebar_rename_timer`
  (5556–5564) abbestellt und nicht von der zentralen Schlussroutine erfasst.
  Beim normalen Schließen wird direkt danach das gesamte Tk-Fenster zerstört.
  Kein Ressourcenleck/Einfrieren dadurch reproduziert; Schließen bei laufender
  Umbenennungsverzögerung bleibt ein gezielter manueller Test.
- **Dateien und temporäre Ressourcen:** alle gefundenen produktiven Datei-
  Öffnungen benutzen `with`; das explizit gehaltene Import-ZIP wird in `finally`
  geschlossen (14115–14119), ebenso das Staging-Verzeichnis. Atomare JSON-,
  Anhangs- und Backup-Zwischendateien werden in `finally` aufgeräumt. Die beiden
  Suiten `test_datenintegritaet.py` und `audit_app.py` erzeugen dagegen mit
  `mkdtemp` Diagnosebestände ohne Cleanup; diese bleiben isoliert zurück.
- **Ausnahmen:** 18 breite Fänge statt historisch 20; keine nackten Fänge. Da
  hier keine Git-Historie verfügbar ist, kann das Hinzukommen einzelner Stellen
  seit 3.0.2 nicht aus einem Versionsdiff bewiesen werden. Die bereits geprüften
  Fänge wurden nicht erneut pauschal umgebaut.
- **Pfadsicherheit:** `validate_attachment_storage` (9230–9250) erlaubt nur
  flache `attachments/NAME`-Pfade; Traversal, Backslashes, Steuerzeichen,
  NTFS-Doppelpunkt, reservierte Gerätebezeichnungen und problematische Endungen
  werden abgefangen. `resolve_attachment_path` (9283–9300) kontrolliert den
  echten Pfad einschließlich Symlink-Ziel. `validate_backup_target` (13716–13731)
  schützt Speicher-/Einstellungsdatei und internen Anhangsordner über reale Pfade.
  `inspect_backup_archive` (13768–13813) kontrolliert kanonische Namen,
  Duplikate, Symlinks, Verschlüsselung, Größen und Kompressionsverhältnis. Kein
  weiterer Traversal-Durchbruch gefunden; kein umfassender Security-Nachweis.
- **Grenzen:** Undo wird auf 20 begrenzt (11335–11338), wirkungslose Aktionen
  trimmen erst nach Wirkung. Papierkorb wird beim Einfügen und Normalisieren auf
  200 begrenzt (6410–6412, 7748, 7782). Ordner-Moves beziehen Unterbaumhöhe ein
  (4194–4210), neue/restorete Ordner und Normalisierung respektieren fünf Ebenen.
  Labelnormalisierung begrenzt 20 (4551); obiger Artabgleich umgeht diese Grenze.
  Punktgrenze wird beim Laden/Schema validiert (7530, 7577, 9507), nicht in jedem
  Erzeugungs-/Umhängeschritt. Grenzwerte daher **nicht durchgehend eingehalten**.
- **Plattformen:** Windows-Pfade/App-ID/DWM, macOS-Anwendungsmenü/Shortcuts/
  Scrollereignisse/Dateiöffnen und Linux-Fallbacks gelesen. Windows 3.12.12 /
  Tk 8.6.17 ist nun automatisiert geprüft; macOS und plattformgerechte Builds
  bleiben ungeprüft. Native Dateidialoge, mehrere Bildschirme, Skalierungen und
  längere verschachtelte Dialognutzung sind weiterhin **NOCH ZU TESTEN**.

## Änderungen und Nachweis im Prüfprozess

Die folgenden vier Abläufe sind mit „Prozessen“ gemeint:

| Ablauf | Vorher | Jetzt |
|---|---|---|
| Prüfprozess | Einzelaufrufe; PowerShell startete nur Hauptsuite | `tests/tools/pruefen.py`: alle drei Suiten, beide Analysen, Syntax und optional Bilder; Status/Grund und strukturierte Logs |
| Versionsprozess | Abgleich hauptsächlich in Hauptsuite | Früher AST-Abgleich von VERSION, Appkonstante, Testkonstante, oberstem nummeriertem Changelog-Eintrag; keine automatische Erhöhung |
| Dokumentationsprozess | Fachliche manuelle Pflege ohne gemeinsamen Gate | Indexabdeckung und lokale echte Markdown-Dateilinks im Prüfskript; historische Aussagen/Funktionsnamen bleiben fachlich zu prüfen |
| Beispieldatenprozess | Erzeuger und Datei nur durch Umfangstests gekoppelt | Vollmodus erzeugt in temporärem Ordner neu und vergleicht vollständigen semantischen Inhalt mit kanonisierten IDs und relativen Fristen; keine automatische Überschreibung |

Die Hauptsuite erhält ihre realen Import-/Schemaprüfungen; das Werkzeug ersetzt
keine Suite. Analyse-Verdachtszahlen werden nicht als Fehlercode missverstanden.
Ein Audit mit `BEFUNDE (N)` wird auch bei unerwartetem Exitcode 0 als Fehler
erkannt. Fehlendes Tk überspringt alle drei Pflichtsuiten mit Grund und liefert
Exitcode 2; fehlende optionale Bilder ergeben keinen Fehlschlag. Eine tatsächliche
Sichtprüfung wird niemals maschinell als bestanden behauptet.

`tests/integration/test_datenintegritaet.py` verarbeitet nach dem ersten Layout
mit einem zusätzlichen `root.update()` das native Fenstermapping. Damit ist die
ursprüngliche Windows-`bbox`-Ausnahme reproduzierbar behoben; keine Inhalts-
Assertion wurde gelockert. Die gesamte Suite ist danach grün.

Erster vollständiger Lauf mit Inkscape Python 3.12.12: Syntax, Version,
Dokumentation, Fixtures, drei Suiten, zwei Analysen und semantischer Beispieldaten-
Abgleich erfolgreich. Logs in `pruefen_erster_lauf/`. Negativlauf mit der
unvollständigen gebündelten Tk-Installation: `UNVOLLSTÄNDIG`, Exitcode 2 in
`pruefen_tk_fehlt/ergebnis.json`; kein falsches Grün. Linux-Screenshots auf
Windows begründet übersprungen. Release-Fixture/Sichtnachweis und spätere
Produktionsänderungen benötigen den abschließenden Gesamtprüflauf.
