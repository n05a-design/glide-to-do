# Bestandsanalyse 3.2.0

Stand: 04.09.2026 · App-Version 3.2.0 · Datenformat 10

## Fakt: Umfang und Ausgangslage

Geprüft wurden die lokale Repository-Kopie `01_Repository/Glide` und die
erreichbaren äußeren Arbeits-, Dokumentations-, Versions- und Store-Ordner.
Der zuerst übergebene Kontext wurde vor dem Arbeitsauftrag gelesen. Der
genannte Pfad `Claude outputs/09_ARBEITSAUFTRAG_BESTANDSANALYSE.md` existiert
nicht; das Dokument liegt unter `docs/09_ARBEITSAUFTRAG_BESTANDSANALYSE.md`.
Der Text ist eine Referenz des Auftrags, kein Ersatz für geprüfte Dateifakten.

`git status` meldet, dass diese Kopie kein Git-Repository ist. Aussagen über
verlorene frühere Dateien, „Phase 11“ oder die unbelegten Dokumentnummern 03/04
lassen sich deshalb nicht über `git log` absichern. Es wurden keine Dokumente
nur zur Füllung dieser Nummernlücken erfunden.

`VERSION`, `APP_VERSION`, die explizite Testprüfung und der oberste
Changelog-Eintrag nennen 3.2.0. `DATA_SCHEMA_VERSION` ist 10; portable Backups
werden von 4 bis 10 unterstützt. Die acht JSON-Fixtures bleiben unverändert.
Die kanonische App und `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.2.0.pyw`
sind bytegleich und wurden nicht verändert.

App-SHA-256: `6309f2669f5490777d342138e9fe304b27a4e728404d0359952e3cd4bfc01715`.

## Befund und Maßnahme: Inkonsistenzen

Fundstellen nennen Abschnitt und eindeutigen Suchtext; der unveränderte
Ausgangswortlaut bleibt jeweils in der versionierten Archivkopie erhalten.

| Schwere | Fundstelle im Ausgangsbestand | Befund | Maßnahme / Ergebnis |
|---|---|---|---|
| wichtig | Handoff, Dokumentationstabelle; Startkontext, bekannte Fehler | Register/QA/Release angeblich 2.11.0; Dateien waren bereits auf 3.2.0, Register bereits Schema 10 | Kontext gegen echte Dateien fortgeschrieben |
| wichtig | Architektur, Datenmodell „Mehrzeiligkeit … erst bei Darstellung“ | widerspricht gespeicherten Long-Task-Zeilen in `normalize_item_text` | 40 gespeicherte / höchstens fünf dargestellte Zeilen korrekt beschrieben |
| wichtig | Architektur, zweiter Abschnitt „Symbole“ | erlaubte Emoji außerhalb Aufgabenliste, widersprach Zielvorgabe | doppelte widersprüchliche Passage entfernt; drei tatsächliche Ausnahmen transparent dokumentiert |
| wichtig | README/Changelog/QA/Register „alle Symbole“, „0 Emoji“ | 📁, 🚩 und 📝 außerhalb ICONS vorhanden | Aussage korrigiert, keine gestalterische Eigenentscheidung |
| wichtig | Backup-Dokument, „Backup-Kompatibilität“ | Formate nur 4 bis 9; zwei Fixturelisten nur fünf statt acht Bestände | Formate 4 bis 10 und alle acht Referenzen nachgeführt |
| wichtig | Backup-Dokument, Datenformat 7 | entfernte `LEGACY_LABEL_COLOR_MAP` als aktiv beschrieben | lokale Vorgabefarbe vs. portable strikte Ablehnung erklärt |
| wichtig | Architektur, „Bewusste Übergangsentscheidung“; Word-Plan | Modulaufteilung als nächster Schritt | Monolith als aktuelle Entscheidung erhalten |
| wichtig | QA-Bericht/Startkontext „alle Tests grün“, „nur Linux“ | erste aktuelle Windows-Prüfung fand zwei Testabbrüche | Ausgangslauf protokolliert, Testannahmen gezielt korrigiert, alle drei Suiten erneut bestanden |
| wichtig | `test_glide.py`, Windows-Layoutblock | Zugriff auf entferntes `system_box` | aktuelles `system_listbox` und Fehlen des Rahmens geprüft |
| kosmetisch | `test_glide.py`, Kopfmetrik | Windows reqheight43 vs. Button42 | explizite max.1px Fonttoleranz; Labelwechselhöhe weiterhin exakt gleich |
| wichtig | `test_datenintegritaet.py`, Start/Drag | leere bbox vor nativer Fensterereignisverarbeitung | `root.update()` nach Aufbau; Assertions unverändert |
| wichtig | Index/Releasecheckliste, Produktdatenabschnitt | angeblich letztes Datenblatt2.6.0, obwohl3.2.0 vorhanden | aktive3.2-Quelle verlinkt und inhaltlich korrigiert |
| wichtig | Store-/Word-Unterlagen | geplante Laufzeit, Plattformabnahme, Sandbox oder Pflichtfelder teils als fertig dargestellt | belegte App-Fakten, recherchierte Vorgaben und offene Freigaben getrennt |
| kosmetisch | QA-Testplan/Architektur, LabelChip | Radius6 statt tatsächlichem9 | gegen `LabelChip.RADIUS` korrigiert |
| kosmetisch | Handoff, Quellzeilen / Werkzeuge |14.590 statt Werkzeugzählung14.591; tools-README angeblich nur Screenshot | aktuelle Zählweise festgehalten; bereits vorhandene vier Werkzeuge anerkannt und neue ergänzt |
| wichtig | `scripts/test/run_core_tests.ps1` | startete nur Hauptsuite | Aufruf des gemeinsamen Prüfskripts statt unvollständiger Testfolge |
| kosmetisch | `requirements/runtime.txt` | Kommentar noch Glide2.9.0 | auf3.2.0 nachgeführt, keine neue Abhängigkeit |

Keine festgestellte Versionsinkonsistenz von `VERSION`/App/Test musste durch
eine Versionserhöhung kaschiert werden. Historische Versionsnummern in
Ausführungsplänen, Changelog und Schema-Fixtures sind fachlich richtig und
wurden nicht pauschal ersetzt.

## Maßnahme: Dateistruktur und Archiv

Es bestanden bereits dezentrale Archive. Dieses Konzept wurde fortgeführt:
`archiv/` innerhalb des Repositorys, `Archiv/` in den äußeren Bereichen.
Vor dem Überschreiben wurden alte Dokumentstände mit Version und bei mehreren
3.2-Fassungen zusätzlich Datum/Anlass kopiert. Das jeweilige Archiv-README
erklärt Zweck, Benennung und Grund. Bestehende Projekt-/Nutzdateien wurden
nicht gelöscht; alte Codeversionen und alle Kompatibilitäts-Fixtures bleiben
erhalten. Historische interne Verweise sind Originaltext und können frühere
Speicherorte nennen; aktive Markdown-Links und der aktuelle Index werden geprüft.

Es wurde keine Verschiebung von produktiv gelesenen Fixtures oder App-Quellen
vorgenommen. Die äußeren historischen 2.6-/2.11-Unterlagen sind von den aktiven
3.2-Dateien getrennt. Die Word-Gliederung und Gestaltung wurden bei der
Fortschreibung erhalten. Sämtliche aktuellen Dokumente unter `docs/` sowie
die Archivdateien sind einzeln im `00_INDEX.md` verzeichnet.

## Codeprüfung und Prozessverbesserung

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
| Emoji trotz verbindlicher Textsymbol-Regel | `insert_tree_items` 10762 setzt den Beschreibungshinweis auf 📝 außerhalb `ICONS` | An Hauptbearbeitung gemeldet, keine eigenständige App-Änderung | **GEMELDET**; sämtliche produktiven Fundstellen und Regressionstest als drei Symbolarten dokumentiert; Änderung bleibt offen |

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
Windows begründet übersprungen. Release-Fixture/Sichtnachweis und abschließende Dokument- und Fixtureergänzungen benötigen den abschließenden Gesamtprüflauf.


### Ergänzender Architekturabgleich

Die gemeinsame Änderungslogik ist noch nicht lückenlos umgesetzt.
`indent_selected` (12905) und `outdent_selected` (12923) verwenden
`item_change` ohne zusätzlichen Bestandswächter. `add_child_item` (11803)
und `apply_sidebar_rename` (5532) nutzen noch direkte Snapshot-/Speicherfolgen.
Die Dokumentation hatte die verbindliche Zielregel als vollständig erreichten
Istzustand ausgegeben. Dieser Überanspruch ist korrigiert; eine strukturelle
Umstellung der verbleibenden Aufrufer wurde nicht eigenmächtig vorgenommen.
Status: **GEMELDET**, wichtiger Architekturrest, kein hier neu reproduzierter
Datenverlust. Vor weiterer Änderung gezielt mit Rückgängig-/Fehlerpfaden prüfen.

`audit_app.py` enthält nummerierte Abschnitte 1 bis 10. Die Behauptung, es
gebe keinerlei Phasenstruktur, war falsch; nur die frühere elfte Phase bleibt
ohne Originaldatei/Git-Historie unbelegt.

## Drei Arbeitslisten im nativen Glide-Format

`tests/tools/releasedaten.py` erzeugt genau ein gemeinsames Backup unter
`tests/fixtures/beispiele/glide_releaseplanung_3.2.0.glidebackup`. Es enthält
die Listen „Unterlagen & Assets“, „Vermarktungsstrategie“ und „Feature-Übersicht“
in einem Release-Ordner sowie den technisch erforderlichen geschützten Eingang.
„3.2.0“ bezeichnet den tatsächlichen App-Stand; ein erfundenes Release1.0
wurde vermieden. Alle vier Punktarten und der kleine Labelsatz werden verwendet.

Store-, Icon-, Text- und Signaturvorgaben sowie Wettbewerbsangaben tragen
Quelle und Abrufdatum04.09.2026 in den Beschreibungstexten. Recherchierte
Anforderungen werden nach Windows-Vertriebspfad bzw. macOS-Store/Direktvertrieb
getrennt. Zielgruppen-, Kanal- und Preisüberlegungen sind Vorschläge, keine
Inhaberentscheidung. Fristen sind relative Planungsvorschläge ab Erzeugung,
keine vereinbarten Termine. Eine erneute Erzeugung aktualisiert keine Webrecherche.

Archivprüfung, Schemaprüfung, Listen-/Papierkorbnormierung und Labelreferenzen
werden mit dem echten App-Code kontrolliert. Die Hauptsuite prüft das neue
Fixture dauerhaft. Der Generator prüft außerdem das tatsächliche Einlesen.

**Ein Komplettbackup ersetzt den gesamten Bestand.** Zum Testen ein isoliertes
`GLIDE_DATA_DIR` verwenden; vor Import in eine eigene Ablage vollständig sichern.
Es wurden keine Arbeitslisten in den echten Datenbestand des Nutzers importiert.

Erzeugter Inhalt: 1 Ordner, 4 Listen einschließlich Eingang, 114 Punkte, 9 Labels einschließlich Systemlabels. Arten: {'task': 77, 'group': 10, 'long': 11, 'heading': 16}.

## Abschließender Prüflauf

Zeitpunkt: 2026-09-04T18:02:39. Modus: voll. Exitcode: 0.

| Schritt | Status | Ergebnis/Grund |
|---|---|---|
| Syntax | ausgeführt | 10 Python-Quelldateien gelesen; keine Bytecode-Dateien erzeugt |
| Versionskonsistenz | ausgeführt | VERSION, App, Hauptsuite und CHANGELOG: 3.2.0; Datenformat 10 |
| Dokumentation | ausgeführt | Alle Dokumente einschließlich Archiv im Index; 53 lokale Markdown-Dateilinks aktueller Dokumente geprüft. Inhaltliche Prüfung bleibt manuell. |
| Fixtures | ausgeführt | 2 aktuelle Backups und alle historischen Referenzformate vorhanden; echte Importprüfung folgt in der Hauptsuite |
| Tk-Voraussetzung | ausgeführt | Tk-Fenster im gewählten Python gestartet und geschlossen |
| test_glide | ausgeführt | Exitcode 0 |
| test_datenintegritaet | ausgeführt | Exitcode 0 |
| audit_app | ausgeführt | Exitcode 0 |
| analyse_statisch | ausgeführt | Exitcode 0 |
| analyse_erreichbarkeit | ausgeführt | Exitcode 0 |
| Beispieldaten-erzeugen | ausgeführt | Exitcode 0 |
| Beispieldaten-Abgleich | ausgeführt | Inhalt, Verknüpfungen und relative Fristen gleich; IDs und Erzeugungszeit sind ausgenommen |
| Release-erzeugen | ausgeführt | Exitcode 0 |
| Release-Abgleich | ausgeführt | Inhalt, Fristen und Verknüpfungen zum Planungsstichtag 2026-09-04 gleich |
| Screenshots | ausgeführt | Exitcode 0 |
| Sichtprüfung | übersprungen | Bilder müssen von einer Person angesehen werden; native Plattformprüfung bleibt offen |

Die separat angesehenen Windows-Aufnahmen und das Word-Renderprotokoll sind
im äußeren QA-Ordner erhalten. Ein automatisiertes Werkzeug kann diese
Sichtabnahme selbst nicht bescheinigen.

## Offen / nicht beurteilbar

- **Vor Release zu beheben:** fehlende Tiefenprüfung vor tiefenerhöhenden
  Mutationen und Überschreitung der Labelgrenze durch Artwechsel. Eine
  strukturell konsistente Behebung wurde nicht durch einen lokalen Sonderfall ersetzt.
- **NICHT VERIFIZIERT:** Behebung des gemeldeten Einfrierens; keine
  Reproduktion des ursprünglichen Anwendersymptoms.
- **NOCH ZU TESTEN:** vollständige manuelle Windows-/macOS-Matrix,
  mehrere Monitore/DPI, reale Eingabegeräte, Langzeitnutzung und echte Datenkopien.
- **STATUS UNKLAR:** frühere Git-Historie, Dokumentnummern03/04, verlorene
  Auditphase und ehemalige Zufallslaufwerkzeuge. Keine Rekonstruktion erfunden.
- **Inhaberentscheidungen:** Publisher, Copyright, URLs/Kontakte, Lizenz,
  Preis, IDs, Zielarchitekturen, Betriebssystem-Mindestversionen, Markenfreigabe
  und Vertriebswege. Produktive Storeformulare wurden nicht eingereicht.
- **Noch nicht vorhanden:** freigegebener Branding-Master, reproduzierbare
  Installer/App-Bundles, Signing-/Notarisierungsnachweis und finale Storeassets.

## Vollständige Datei-Inventur des Repositorys

Jede vorhandene Datei wird genau einmal kategorisiert. „3.2.0 abgeglichen“
bezeichnet die geprüfte aktuelle Gültigkeit, nicht eine erfundene ursprüngliche
Entstehungsversion. Historische Werkzeuge und Metadaten tragen ihre eigene Rolle.
Externe Arbeitsartefakte sind oben beschrieben und über ihre Ordner-README erreichbar.

| Pfad | Rolle | Kategorie | Inhaltlicher Stand | Besonderheit |
|---|---|---|---|---|
| `.editorconfig` | Entwicklungs-/Dateiformatregeln | Werkzeug | versionsneutral, für 3.2.0 gültig | vorhanden; Git-Historie fehlt in dieser Kopie |
| `.gitattributes` | Entwicklungs-/Dateiformatregeln | Werkzeug | versionsneutral, für 3.2.0 gültig | vorhanden; Git-Historie fehlt in dieser Kopie |
| `.gitignore` | Entwicklungs-/Dateiformatregeln | Werkzeug | versionsneutral, für 3.2.0 gültig | vorhanden; Git-Historie fehlt in dieser Kopie |
| `AGENTS.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `archiv/.gitignore_3.2.0_vor_Bestandsanalyse_2026-09-04` | Vorgängerfassung/Archivnachweis | Werkzeug | 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `archiv/CHANGELOG_3.2.0_vor_Bestandsanalyse_2026-09-04.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `archiv/README.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | Archivkonzept 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `archiv/README_3.2.0_vor_Bestandsanalyse_2026-09-04.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `assets/README.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `CHANGELOG.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `docs/00_INDEX.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `docs/01_PRODUCT_CONSTRAINTS.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `docs/02_ARCHITECTURE.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `docs/05_QA_TESTPLAN.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `docs/06_DATA_BACKUP_MIGRATION.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `docs/07_QA_BERICHT.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `docs/08_CODE_BEFUND.md` | Aktuell eingeordnete historische Referenz | Dokumentation, aktuell | 3.2.0 mit gekennzeichneter Historie | ursprüngliche Inhalte erhalten; aktuelle Abweichungen vorangestellt |
| `docs/archiv/09_ARBEITSAUFTRAG_BESTANDSANALYSE_3.2.0_abgeschlossen.md` (bis 3.3.0 unter `docs/09_ARBEITSAUFTRAG_BESTANDSANALYSE.md`) | Aktuell eingeordnete historische Referenz | Dokumentation, aktuell | 3.2.0 mit gekennzeichneter Historie | ursprüngliche Inhalte erhalten; aktuelle Abweichungen vorangestellt |
| `docs/09_PROJECT_HANDOFF.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `docs/03_STARTKONTEXT.md` (bis 3.3.0 unter `docs/09_STARTKONTEXT.md`) | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `docs/10_RELEASE_CHECKLIST.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `docs/11_BESTANDSANALYSE.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `docs/12_ABSCHLUSSBERICHT.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `docs/archiv/00_INDEX_3.2.0_vor_Bestandsanalyse_2026-09-04.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `docs/archiv/01_PRODUCT_CONSTRAINTS_3.2.0_vor_Bestandsanalyse_2026-09-04.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `docs/archiv/02_ARCHITECTURE_3.2.0_vor_Bestandsanalyse_2026-09-04.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `docs/archiv/05_QA_TESTPLAN_3.2.0_vor_Bestandsanalyse_2026-09-04.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `docs/archiv/06_DATA_BACKUP_MIGRATION_3.2.0_vor_Bestandsanalyse_2026-09-04.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `docs/archiv/07_QA_BERICHT_2.11.0.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | 2.11.0 | bewusst unverändert; nicht aktive Quelle |
| `docs/archiv/07_QA_BERICHT_3.2.0_vor_Bestandsanalyse_2026-09-04.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `docs/archiv/08_CODE_BEFUND_3.2.0_vor_Bestandsanalyse_2026-09-04.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `docs/archiv/09_ARBEITSAUFTRAG_BESTANDSANALYSE_3.2.0_vor_Bestandsanalyse_2026-09-04.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `docs/archiv/09_PROJECT_HANDOFF_3.2.0_vor_Bestandsanalyse_2026-09-04.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `docs/archiv/09_STARTKONTEXT_3.2.0_vor_Bestandsanalyse_2026-09-04.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `docs/archiv/10_RELEASE_CHECKLIST_2.11.0.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | 2.11.0 | bewusst unverändert; nicht aktive Quelle |
| `docs/archiv/10_RELEASE_CHECKLIST_3.2.0_vor_Bestandsanalyse_2026-09-04.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `docs/archiv/PRODUCT_IDENTITY_2.11.0.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | 2.11.0 | bewusst unverändert; nicht aktive Quelle |
| `docs/archiv/README.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | Archivkonzept 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `docs/decisions/archiv/PRODUCT_IDENTITY_3.2.0_vor_Bestandsanalyse_2026-09-04.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `docs/decisions/archiv/README.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | Archivkonzept 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `docs/decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `docs/decisions/PRODUCT_IDENTITY.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `docs/exec-plans/2.10.0-label-chips-und-codepflege.md` | Historischer Ausführungsplan | Dokumentation, historisch | 2.10.0 | Entscheidungsverlauf, nicht heutiger Prüfnachweis |
| `docs/exec-plans/2.11.0-datenintegritaet-und-eingabemaske.md` | Historischer Ausführungsplan | Dokumentation, historisch | 2.11.0 | Entscheidungsverlauf, nicht heutiger Prüfnachweis |
| `docs/exec-plans/2.12.0-oberflaeche-verdichten.md` | Historischer Ausführungsplan | Dokumentation, historisch | 2.12.0 | Entscheidungsverlauf, nicht heutiger Prüfnachweis |
| `docs/exec-plans/2.5.1-stabilisierung.md` | Historischer Ausführungsplan | Dokumentation, historisch | 2.5.1 | Entscheidungsverlauf, nicht heutiger Prüfnachweis |
| `docs/exec-plans/2.5.2-qol-stabilisierung.md` | Historischer Ausführungsplan | Dokumentation, historisch | 2.5.2 | Entscheidungsverlauf, nicht heutiger Prüfnachweis |
| `docs/exec-plans/2.5.3-ui-und-struktur-stabilisierung.md` | Historischer Ausführungsplan | Dokumentation, historisch | 2.5.3 | Entscheidungsverlauf, nicht heutiger Prüfnachweis |
| `docs/exec-plans/2.5.4-uebersichten-und-ui-stabilisierung.md` | Historischer Ausführungsplan | Dokumentation, historisch | 2.5.4 | Entscheidungsverlauf, nicht heutiger Prüfnachweis |
| `docs/exec-plans/2.5.5-fehlerbehebung-und-macos.md` | Historischer Ausführungsplan | Dokumentation, historisch | 2.5.5 | Entscheidungsverlauf, nicht heutiger Prüfnachweis |
| `docs/exec-plans/2.6.0-gruppen-und-kontextmenues.md` | Historischer Ausführungsplan | Dokumentation, historisch | 2.6.0 | Entscheidungsverlauf, nicht heutiger Prüfnachweis |
| `docs/exec-plans/2.7.0-papierkorb-labels-kalender.md` | Historischer Ausführungsplan | Dokumentation, historisch | 2.7.0 | Entscheidungsverlauf, nicht heutiger Prüfnachweis |
| `docs/exec-plans/2.7.1-ui-feinschliff.md` | Historischer Ausführungsplan | Dokumentation, historisch | 2.7.1 | Entscheidungsverlauf, nicht heutiger Prüfnachweis |
| `docs/exec-plans/2.7.2-fokus-und-kalenderinteraktion.md` | Historischer Ausführungsplan | Dokumentation, historisch | 2.7.2 | Entscheidungsverlauf, nicht heutiger Prüfnachweis |
| `docs/exec-plans/2.8.0-arten-verspaetet-und-hover.md` | Historischer Ausführungsplan | Dokumentation, historisch | 2.8.0 | Entscheidungsverlauf, nicht heutiger Prüfnachweis |
| `docs/exec-plans/2.9.0-verschachtelte-ordner.md` | Historischer Ausführungsplan | Dokumentation, historisch | 2.9.0 | Entscheidungsverlauf, nicht heutiger Prüfnachweis |
| `docs/exec-plans/3.0.0-oberflaeche-und-symbole.md` | Historischer Ausführungsplan | Dokumentation, historisch | 3.0.0 | Entscheidungsverlauf, nicht heutiger Prüfnachweis |
| `LICENSE.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `packaging/README.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `README.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `requirements/archiv/README.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | Archivkonzept 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `requirements/archiv/runtime_3.2.0_vor_Bestandsanalyse_2026-09-04.txt` | Vorgängerfassung/Archivnachweis | Werkzeug | 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `requirements/build-macos.txt` | Laufzeit-/Builddeklaration | Werkzeug | 3.2.0 abgeglichen | keine externe App-Laufzeitabhängigkeit; Buildpins noch offen |
| `requirements/build-windows.txt` | Laufzeit-/Builddeklaration | Werkzeug | 3.2.0 abgeglichen | keine externe App-Laufzeitabhängigkeit; Buildpins noch offen |
| `requirements/dev.txt` | Laufzeit-/Builddeklaration | Werkzeug | 3.2.0 abgeglichen | keine externe App-Laufzeitabhängigkeit; Buildpins noch offen |
| `requirements/runtime.txt` | Laufzeit-/Builddeklaration | Werkzeug | 3.2.0 abgeglichen | keine externe App-Laufzeitabhängigkeit; Buildpins noch offen |
| `scripts/release/finalize_release_plan_docx_v252.py` | Historisches Word-Fortschreibungswerkzeug | Werkzeug | 2.5.x | nicht für aktuelle App-/Dokumentversion aufrufen; als Historie erhalten |
| `scripts/release/update_release_plan_docx.py` | Historisches Word-Fortschreibungswerkzeug | Werkzeug | 2.5.x | nicht für aktuelle App-/Dokumentversion aufrufen; als Historie erhalten |
| `scripts/release/update_release_plan_docx_v252.py` | Historisches Word-Fortschreibungswerkzeug | Werkzeug | 2.5.x | nicht für aktuelle App-/Dokumentversion aufrufen; als Historie erhalten |
| `scripts/test/run_core_tests.ps1` | Prüf-/Erzeugungswerkzeug | Werkzeug | 3.2.0 | CLI/Voraussetzungen im zugehörigen README |
| `SECURITY.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `src/glide/app.pyw` | Gesamte Anwendung | produktiv | 3.2.0 / Schema 10 | unveränderter Monolith; SHA-256 geprüft |
| `src/glide/archiv/README.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | Archivkonzept 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `src/glide/archiv/README_3.2.0_vor_Bestandsanalyse_2026-09-04.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `src/glide/README.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `tests/fixtures/archiv/README.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | Archivkonzept 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `tests/fixtures/archiv/README_3.2.0.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `tests/fixtures/beispiele/Glide_Beispieldaten.glidebackup` | Importierbarer Beispiel-/Arbeitsbestand | Fixture | 3.2.0 / Schema 10 | generiert; Erzeuger unter tests/tools; Schema-/Importprüfung |
| `tests/fixtures/beispiele/glide_releaseplanung_3.2.0.glidebackup` | Importierbarer Beispiel-/Arbeitsbestand | Fixture | 3.2.0 / Schema 10 | generiert; Erzeuger unter tests/tools; Schema-/Importprüfung |
| `tests/fixtures/current_v10/reference_v10.json` | Kompatibilitätsreferenz | Fixture | Schema 10 | historische Daten bewusst erhalten und aktuell geladen |
| `tests/fixtures/current_v4/reference_v4.json` | Kompatibilitätsreferenz | Fixture | Schema 4 | historische Daten bewusst erhalten und aktuell geladen |
| `tests/fixtures/current_v5/reference_v5.json` | Kompatibilitätsreferenz | Fixture | Schema 5 | historische Daten bewusst erhalten und aktuell geladen |
| `tests/fixtures/current_v6/reference_v6.json` | Kompatibilitätsreferenz | Fixture | Schema 6 | historische Daten bewusst erhalten und aktuell geladen |
| `tests/fixtures/current_v7/reference_v7.json` | Kompatibilitätsreferenz | Fixture | Schema 7 | historische Daten bewusst erhalten und aktuell geladen |
| `tests/fixtures/current_v8/reference_v8.json` | Kompatibilitätsreferenz | Fixture | Schema 8 | historische Daten bewusst erhalten und aktuell geladen |
| `tests/fixtures/current_v9/reference_v9.json` | Kompatibilitätsreferenz | Fixture | Schema 9 | historische Daten bewusst erhalten und aktuell geladen |
| `tests/fixtures/legacy_v2/probelisten_5_listen_v2.json` | Kompatibilitätsreferenz | Fixture | Schema 2 | historische Daten bewusst erhalten und aktuell geladen |
| `tests/fixtures/README.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `tests/integration/audit_app.py` | Automatisierte Funktions-/Integritätsprüfung | Test | 3.2.0 | lineares Skript; isolierte Daten |
| `tests/integration/test_datenintegritaet.py` | Automatisierte Funktions-/Integritätsprüfung | Test | 3.2.0 | lineares Skript; isolierte Daten |
| `tests/integration/test_glide.py` | Automatisierte Funktions-/Integritätsprüfung | Test | 3.2.0 | lineares Skript; isolierte Daten |
| `tests/README.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `tests/tools/analyse_erreichbarkeit.py` | Prüf-/Erzeugungswerkzeug | Werkzeug | 3.2.0 | CLI/Voraussetzungen im zugehörigen README |
| `tests/tools/analyse_statisch.py` | Prüf-/Erzeugungswerkzeug | Werkzeug | 3.2.0 | CLI/Voraussetzungen im zugehörigen README |
| `tests/tools/archiv/README.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | Archivkonzept 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `tests/tools/archiv/README_3.2.0_vor_bestandsanalyse.md` | Vorgängerfassung/Archivnachweis | Dokumentation, historisch | 3.2.0 | bewusst unverändert; nicht aktive Quelle |
| `tests/tools/beispieldaten.py` | Prüf-/Erzeugungswerkzeug | Werkzeug | 3.2.0 | CLI/Voraussetzungen im zugehörigen README |
| `tests/tools/pruefen.py` | Prüf-/Erzeugungswerkzeug | Werkzeug | 3.2.0 | CLI/Voraussetzungen im zugehörigen README |
| `tests/tools/README.md` | Projekt-/Prozessdokumentation | Dokumentation, aktuell | 3.2.0 abgeglichen | Stand aus Code/Dateien geprüft; offene Freigaben nicht erfunden |
| `tests/tools/releasedaten.py` | Prüf-/Erzeugungswerkzeug | Werkzeug | 3.2.0 | CLI/Voraussetzungen im zugehörigen README |
| `tests/tools/screenshots.py` | Prüf-/Erzeugungswerkzeug | Werkzeug | 3.2.0 | CLI/Voraussetzungen im zugehörigen README |
| `VERSION` | App-Version | produktiv | 3.2.0 | mit App/Test/Changelog abgeglichen |

Inventur: **102 Dateien**, `.git/` ausgenommen; 0 nicht sicher zugeordnet.
