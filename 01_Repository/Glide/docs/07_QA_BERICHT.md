# QA-Bericht – Glide 3.33.8

Stand 06.10.2026 · App 3.33.8 · Datenformat 20 · Windows, Python 3.14.8, Tk 9.0.4; Referenz-Mac zuletzt 3.33.6 mit Python 3.14.5, Tk 9.0.3

Einziger Prüfbericht. Am 03.10.2026 mit dem bisherigen Prüfverlauf (`tests/qa-verlauf.md`) zusammengeführt und auf die Nachweise der letzten sieben Versionen gekürzt; ältere Läufe stehen nur noch als Zeile in der Übersicht, ihre Protokolle trägt Git. 3.33.0 und 3.33.1 liegen seit 05.10.2026 außerhalb dieses Fensters; ihre Zeilen verweisen auf den unveränderlichen Git-Stand. Am 05.10.2026 mit der Windows-Fassung zusammengeführt. Wie geprüft wird: [Prüfplan](05_QA_TESTPLAN.md).

## Aktueller Stand

**3.33.8, Windows / Python 3.14.8 / Tk 9.0.4:** Vollständige Nachprüfung **Exitcode 0: 84 automatische Schritte**, darunter 66 Integrationssuiten, 75 Unit-Tests, Showcase, fünf Analysen, Beispiel-/Release-Reproduktion und Windows-Bildaufnahme. [Grünes Originalergebnis](../tests/qa-3.33.8/windows_2026-10-05/voll_2/ergebnis.json). Titelbreiten, Mindesthöhen, Editor-Timerabbau und Windows-Formatcache korrigiert. Der erste Gesamtbericht hatte 66 grüne Integrationssuiten und einen fehlgeschlagenen Unit-Test; [erhaltenes Original](../tests/qa-3.33.8/windows_2026-10-05/voll/ergebnis.json). Der Inhaltsvergleich verhindert übersehene gleich große Formatwechsel bei identischen Dateizeiten. Alle 75 Unit-Tests bestehen zusätzlich mit Python 3.12.10.

**Python-Lieferung 3.33.8:** 16 Code-Dateien und 131 Ressourcen nach `07_Python-Versionen` SHA-256-abgeglichen; die Hauptdatei 3.33.6 liegt unverändert im Archiv. Showcase nach `05_Probelisten_Testdaten/Showcase` abgeglichen. Direkte Such-/Editor-Lieferproben und die CI-Grundstufe mit `--lieferstand-streng` sind grün. [CI-Ergebnis](../tests/qa-3.33.8/windows_2026-10-05/ci/ergebnis.json). [Nachweis](../tests/qa-3.33.8/windows_2026-10-05/README.md). Referenz-Mac, nativer Bundlebau und menschliche Abnahme bleiben offen.

**Nachprüfung der Windows-Aufnahmen (05.10.2026, ohne neuen Lauf):** `release_hell_dunkel.png` ist byte-gleich mit `release_hell.png`; es gibt für 3.33.8 also keine Dunkelaufnahme. Ursache: `tests/tools/releasedaten.py` setzte `theme_name`, das `apply_theme` aus dem Design neu ableitet. Der Erzeuger wechselt seit 05.10.2026 über `set_design` und bricht bei gleichen Bildern ab (Linux/Tk 8.6, künstliche Daten: zwei verschiedene Aufnahmen). Die helle Aufnahme zeigt das Logo geglättet (116 Farbwerte, Tk 9.0.4). Gekürzte Seitenleistentitel sind dagegen rechts angeschnitten, ohne „…“ (Vorbefund W01). Die Fenstersuite fotografiert seit 05.10.2026 auch unter Windows jedes Fenster. Das Originalergebnis bleibt unverändert; Sichtprüfung und Bestätigung folgen mit dem nächsten Windows-Lauf ([Nachweis](../tests/qa-3.33.8/windows_vorbereitung_2026-10-05/README.md)).

**Windows-Lauf 18:29 mit Fensterfotos (05.10.2026):** Der Inhaber hat den Lauf mit den neuen Prüfwerkzeugen gestartet. Ergebnis: Exitcode 1, 83 von 85 Schritten ausgeführt, alle 66 Suiten grün. Gescheitert ist allein `attributpruefung` an einem Absturz des Python-Interpreters (0xC0000409, „Executing a cache“). Glide-Code lief dabei nicht, und 30 Einzelwiederholungen liefen ohne Absturz; die Ursache ist nicht belegt. 50 Fensterfotos und eine echte Dunkelaufnahme bestätigen die Werkzeuge. Aus den Aufnahmen kommen die Vorbefunde W01 und W05–W08, die am Gerät zu bestätigen sind ([Nachweis](../tests/qa-3.33.8/windows_2026-10-05_1829/README.md), [Original](../tests/qa-3.33.8/windows_2026-10-05_1829/ergebnis.json)).

**3.33.7, Windows / Python 3.12.10 / Tk 8.6:** Inhaltssuche und Formatsicherung implementiert; 72 Unit-Tests, Suchsuite und CI grün. Gegenprobe gegen Git-Stand 3.33.6 scheiterte erwartungsgemäß am fehlenden Seiteninhaltstreffer. Der zuerst diagnostisch beendete Volllauf hatte zwei überholte UI-/Font-Assertions. Nach deren Korrektur wurde ein vollständiges diagnostisches Ergebnis erzeugt: 56 von 65 Integrationssuiten grün, neun fehlgeschlagen; [Originalergebnis](../tests/qa-3.33.7/abnahme_windows_2026-10-05/ergebnis.json). Tk 8.6 erklärt SVG-/Touchpad-Befunde, weitere Testannahmen betrafen Windows-Menüs, Zeilenenden und noch nicht abgeschlossene Größenwechsel; echte Titel-/Höhenbefunde führten zu 3.33.8. Keine Lieferung von 3.33.7. Ursprung der Funktion und Fachmessung: [Nachweis](../tests/qa-3.33.7/suche_2026-10-05/README.md).

**Einstieg unter Windows (05.10.2026):** VERSION, APP_VERSION, Hauptsuite und CHANGELOG waren konsistent mit 3.33.6; Hauptdatei und `capture_parser.py` lagen in der Python-Lieferung. Die abweichenden Aussagen einer veralteten lokalen Übergabekopie (`docs/09_PROJECT_HANDOFF.md`, am 05.10.2026 aufgelöst) sind damit widerlegt. Die bestehende Seitensuite war grün. Ein CI-Vorlauf während der Umsetzung scheiterte an den vorhandenen Dokumentverweisen/Modullisten; er ist keine eingefrorene Baseline und wird nicht als grüner Nachweis ausgegeben.

**Referenz-Mac, zuletzt 3.33.6 (02.10.2026):** geprüft und lokal ausgeliefert. Vollprüfung Exitcode 0 im dritten Lauf – 81 Schritte, alle 64 Integrationssuiten, Unit-Tests, Showcase und fünf Analysen; Quellstand (342 Dateien) unverändert. 146 Python-/60 Bundle-Dateien per SHA-256 gleich `src/glide`, Bundle `de.shaye.glide`, `codesign --verify --deep --strict` bestanden. [Nachweis](../tests/qa-3.33.6/heute_2026-10-02/README.md). Für 3.33.7 und 3.33.8 gibt es keine Mac- und keine Bundle-Abnahme.

**Grenzen jeder bisherigen Abnahme:** echte Tastatur-, Maus- und Trackpadbedienung, Windows-Bedienung (automatisch wieder geprüft seit 3.33.8, davor zuletzt 3.26.0), Linux, DPI und mehrere Monitore, Screenreader. Übersprungene Sichtprüfungen sind keine menschliche Freigabe. Alle Läufe mit temporärem `GLIDE_DATA_DIR` und künstlichen Daten; keine echten Nutzerdaten gelesen. Entwicklungsbundle mit Ad-hoc-Signatur und installiertem Python; **keine Releasefreigabe**.

## Versionen 3.33.0–3.33.8

| Version | Datum | Inhalt | Vollprüfung | Lieferung | Nachweis |
|---|---|---|---|---|---|
| 3.33.8 | 05.10.2026 | Windows-Layout, Editorlebensdauer, Prüflaufzeit | Windows: Exit 0 im 2. Lauf, 84 Schritte, 66 Suiten (Python 3.14.8, Tk 9.0.4); Referenz-Mac offen | 16 Code-Dateien und 131 Ressourcen in 07 bytegleich; kein Bundle | [README](../tests/qa-3.33.8/windows_2026-10-05/README.md) · [Protokoll](../tests/qa-3.33.8/windows_2026-10-05/voll_2/ergebnis.json) · [Lieferung](../tests/qa-3.33.8/windows_2026-10-05/lieferabgleich.json) · [Lauf 18:29](../tests/qa-3.33.8/windows_2026-10-05_1829/README.md) |
| 3.33.7 | 05.10.2026 | Inhaltssuche (G14, erste Stufe), Windows-Formatsicherung | Windows diagnostisch (Python 3.12.10, Tk 8.6): 56 von 65 Suiten grün | nicht ausgeliefert | [README](../tests/qa-3.33.7/suche_2026-10-05/README.md) · [Protokoll](../tests/qa-3.33.7/abnahme_windows_2026-10-05/ergebnis.json) · [Nachprüfung](../tests/qa-3.33.7/nachpruefung_windows_2026-10-05/ergebnis.json) |
| 3.33.6 | 02.10.2026 | Heute und Demnächst (D14) | Exit 0 im 3. Lauf, 81 Schritte, 64 Suiten | 146/60 bytegleich | [README](../tests/qa-3.33.6/heute_2026-10-02/README.md) · [Protokoll](../tests/qa-3.33.6/heute_2026-10-02/vollpruefung/ergebnis.json) · [Lieferung](../tests/qa-3.33.6/heute_2026-10-02/auslieferung.json) |
| 3.33.5 | 02.10.2026 | Eisenhower als Gruppierung (D13) | Exit 0, 80 Schritte, 63 Suiten | 145/59 | [README](../tests/qa-3.33.5/eisenhower_2026-10-02/README.md) · [Protokoll](../tests/qa-3.33.5/eisenhower_2026-10-02/vollpruefung/ergebnis.json) · [Lieferung](../tests/qa-3.33.5/eisenhower_2026-10-02/auslieferung.json) |
| 3.33.4 | 02.10.2026 | Wiederholungen in der Schnelleingabe | Exit 0, 79 Schritte, 62 Suiten | 144/58 | [README](../tests/qa-3.33.4/wiederholung_2026-10-02/README.md) · [Protokoll](../tests/qa-3.33.4/wiederholung_2026-10-02/vollpruefung/ergebnis.json) · [Lieferung](../tests/qa-3.33.4/wiederholung_2026-10-02/auslieferung.json) |
| 3.33.3 | 02.10.2026 | Deutsche Schnelleingabe mit Feldchips (G01, D10) | Exit 0, 79 Schritte, 62 Suiten | 144/58 | [README](../tests/qa-3.33.3/eingabe_2026-10-02/README.md) · [Protokoll](../tests/qa-3.33.3/eingabe_2026-10-02/vollpruefung/ergebnis.json) · [Lieferung](../tests/qa-3.33.3/eingabe_2026-10-02/auslieferung.json) |
| 3.33.2 | 02.10.2026 | Startseite „Ruhig“ (D12), Aufbau 764 → 507 ms | Exit 0 im 2. Lauf, 78 Schritte, 61 Suiten | 143/57 | [README](../tests/qa-3.33.2/startseite_2026-10-02/README.md) · [Protokoll](../tests/qa-3.33.2/startseite_2026-10-02/vollpruefung/ergebnis.json) · [Messung](../tests/qa-3.33.2/startseite_2026-10-02/messung/zusammenfassung.json) |
| 3.33.1 | 01./02.10.2026 | Vier Bereiche, Fenster, Logo | Exit 0 im 3. Lauf, 77 Schritte, 60 Suiten | 142/56 | [README](https://github.com/n05a-design/glide-to-do/blob/267baab914c5dee5bdd85e8556288e82a711b0ea/01_Repository/Glide/tests/qa-3.33.1/abschluss_2026-10-01/README.md) · [Protokoll](https://github.com/n05a-design/glide-to-do/blob/267baab914c5dee5bdd85e8556288e82a711b0ea/01_Repository/Glide/tests/qa-3.33.1/abschluss_2026-10-01/vollpruefung_3/ergebnis.json) · [Lieferung](https://github.com/n05a-design/glide-to-do/blob/267baab914c5dee5bdd85e8556288e82a711b0ea/01_Repository/Glide/tests/qa-3.33.1/abschluss_2026-10-01/auslieferung.json) |
| 3.33.0 | 01.10.2026 | Fundament T2, P09a | Exit 0, 76 Schritte, 59 Suiten | 140/54 | [README](https://github.com/n05a-design/glide-to-do/blob/267baab914c5dee5bdd85e8556288e82a711b0ea/01_Repository/Glide/tests/qa-3.33.0/fundament_2026-10-01/README.md) · [Protokoll](https://github.com/n05a-design/glide-to-do/blob/267baab914c5dee5bdd85e8556288e82a711b0ea/01_Repository/Glide/tests/qa-3.33.0/fundament_2026-10-01/vollpruefung/ergebnis.json) · [Lieferung](https://github.com/n05a-design/glide-to-do/blob/267baab914c5dee5bdd85e8556288e82a711b0ea/01_Repository/Glide/tests/qa-3.33.0/fundament_2026-10-01/auslieferung.json) |

Die Mac-Läufe 3.33.0–3.33.3 meldeten je zwei übersprungene Schritte. „Lieferung“ nennt die Python-/Bundle-Dateien, die per SHA-256 gleich `src/glide` sind; bis 3.33.6 jede Version mit gültiger Signatur und ausgeliefertem Showcase. Ab 3.33.7 steht der Bundlebau aus; 3.33.8 ist nur als Python-Fassung samt Showcase ausgeliefert. Jede Funktionsversion hat eine neue Pflichtsuite, deren Gegenprobe mit der Vorversion rot war.

### Befunde und ungültige Läufe

Regeln, die aus diesen Läufen folgen (nicht tippen, nicht sperren, Last vermeiden, „Flaky“ ist keine Ursache), stehen im [Prüfplan](05_QA_TESTPLAN.md#regeln).

- **3.33.8:** Der erste Gesamtlauf hatte 66 grüne Suiten und einen fehlgeschlagenen Unit-Test (gleich große In-place-Änderung im Windows-Formatcache); nach der Korrektur sind alle 75 grün ([erster Lauf](../tests/qa-3.33.8/windows_2026-10-05/voll/ergebnis.json)). Die Dunkelaufnahme beider Läufe ist byte-gleich mit der hellen (Werkzeugfehler, am 05.10.2026 behoben). Vorbefund W01: angeschnittene Seitenleistentitel. Der Lauf um 18:29 mit Fensterfotos war rot, weil der Python-Interpreter in `attributpruefung` einmalig abstürzte; nicht reproduzierbar (0 von 30).
- **3.33.7:** Diagnostischer Volllauf unter Tk 8.6 mit zwei überholten UI-/Font-Assertions; nach deren Korrektur neun Suiten rot. Tk 8.6 erklärt die SVG- und Touchpad-Befunde, weitere betrafen Windows-Menüs, Zeilenenden und Größenwechsel. Echte Titel- und Höhenbefunde führten zu 3.33.8.
- **3.33.6 unter Windows (05.10.2026):** Die unveränderte Unit-Baseline hatte 61 Tests mit 16 fehlgeschlagenen Format-Subtests (wiederholter JSON-Parse unter Windows, [Ergebnis](../tests/qa-3.33.6/baseline_2026-10-05/ergebnis.json)); behoben in 3.33.7.
- **3.33.6:** Zwei ungültige Vorläufe: gesperrter Bildschirm (`test_ui39`, `test_workspace310` rot, Stillstand) und ein Zeitrennen unter Last: `test_speicherlast330` prüfte den 700 ms später gezeigten Formathinweis erst nach seinem Leerlauf, während OneDrive über 200 % CPU belegte. Laden plus Leerlauf je rund 420–433 ms in 3.33.5 und 3.33.6, also keine Verlangsamung; die Suite akzeptiert jetzt „vorgemerkt oder gezeigt“. Sieben Altsuiten auf D14 gebracht.
- **3.33.5:** `test_features322`/`325` fanden einen nicht zugeordneten Palettenbefehl (Risiko R2, Gruppierung über Beschriftungen); behoben.
- **3.33.2:** Erster Lauf nur an der Attributprüfung gescheitert (Hilfsklasse ohne Canvas-Basis, heute `DeferredDrawCanvas`). Messung auf macOS mit 1.000 Punkten: Aktualisierung 764,2 → 506,7 ms, Wechsel 789,7 → 547,8 ms, Bibliothek 974 → 856 ms; Ziel 150 ms nicht erreicht, der Rest ist Tk-Layout je Widget.
- **3.33.1:** Erste Vollprüfung des Prüfkandidaten rot (`audit_app`, `test_ui39`, `test_features329`, `test_aufraeumen330`): Dialog „Neu anlegen“ blieb auf niedrigen Bildschirmen einspaltig (echter Fehler), Notizbücher nahmen keine datierten Zeichnungen auf (Klarstellung des Inhabers), zwei Prüfungen veraltet. Danach zwei ungültige Läufe: gesperrter Bildschirm ab 00:16 und vermutlich Tastatureingaben während des Laufs. Die Aktivierungsprobe zeigt: Der Hintergrundmodus schirmt die Maus ab, nicht die Tastatur. Einstellungsfenster bis zur Anzeige im Median rund 2,1 s.
- **3.33.0:** Formatsicherung 161,406 → 17,896 ms kalt und 0,064 ms nach dem Laden (5.000 Aufgaben, zwölf Runden), neun → eine JSON-Lesung; ungenutzte Tabellenmessung 77,117 → 0,001 ms. Der alte QA-Hintergrund scheitert absichtlich am nativen Mausisolierungstest, der neue besteht ([Nachweis](https://github.com/n05a-design/glide-to-do/blob/267baab914c5dee5bdd85e8556288e82a711b0ea/01_Repository/Glide/tests/qa-3.33.0/fundament_2026-10-01/native_isolation.json)). Drei historische Recherchelogs fehlen seit dem GitHub-Upload.

### Nachläufe ohne neue App-Version

| Datum | Nachlauf | Nachweis |
|---|---|---|
| 06.10.2026 | Richtungsentwurf vom 03.10.2026 in Markt und Vorbilder, Arbeitsrichtung, Produktgrenzen, Veröffentlichung und Entwicklungsplan eingearbeitet, ohne neues Dokument (Linux/Tk 8.6, künstliche Daten) | [README](../tests/qa-3.33.8/richtung_2026-10-06/README.md) |
| 05.10.2026 | Windows-Prüfung vorbereitet: Dunkelaufnahme und Fensterfotos unter Windows, Prüfliste B0, Befunde der Logo-Diagnose übernommen, Synchronisationskopien zusammengeführt (Linux/Tk 8.6, künstliche Daten) | [README](../tests/qa-3.33.8/windows_vorbereitung_2026-10-05/README.md) |
| 05.10.2026 | Planung Ausbauprogramm Alltag, Komfort und Oberfläche | [README](../tests/qa-3.33.8/planung_2026-10-05/README.md) |
| 03.10.2026 | Bereinigung der Ablage und Dokumentation: Archive auf 3.33.0–3.33.6, Fensterbilder nur 3.33.4–3.33.6, Dokumente zusammengeführt (Linux/Tk 8.6, künstliche Daten) | [README](../tests/qa-3.33.6/aufraeumen_2026-10-03/README.md) |
| 02.10.2026 | Schlanke Ablage: Archivkopien entfernt, CI-Schritt „Ablagegröße“ | [README](../tests/qa-3.33.6/ablage_2026-10-02/README.md) |
| 01.10.2026 | Analyse und Planung, Beschlüsse D09–D17, Showcase, Prüfaufruf- und Speicherwegmessung (Linux, Xvfb), Dokumentations- und Werkzeugabgleich zu 3.32.3 | Protokolle in Git (Ordner `tests/qa-3.32.3`, gelöscht am 03.10.2026) |

## Ältere Versionen

Nur das Ergebnis; Berichte und Protokolle stehen in der Git-Historie.

| Version | Datum | Ergebnis |
|---|---|---|
| 3.32.3 | 01.10.2026 | Exit 0, 73 Schritte, 58 Suiten; Bibliotheksrefresh bei 1.000 Aufgaben 776,2 → 4,9 ms; 139/53 bytegleich |
| 3.32.2 | 30.09.2026 | Exit 0, 72 Schritte, 57 Suiten; Ziehen in Seiten/Notizen (D04), Schriftcache, gebündelte Layouts |
| 3.32.1 | 30.09.2026 | Exit 0, 71 Schritte, 56 Suiten; Klappkontrolle (D08) |
| 3.32.0 | 30.09.2026 | Exit 0, 70 Schritte, 55 Suiten; Etappe 1, zwei Hänger behoben, Prüfungen erstmals im Hintergrund |
| 3.31.0 | 30.09.2026 | Exit 0, 69 Schritte, 54 Suiten; Rückmeldung R1–R11, 41 Fenster geprüft |
| 3.30.0 | 25.–29.09.2026 | Modernisierung, Format 20; zuletzt Exit 0 mit 66 Schritten, 51 Suiten |
| 3.29.0 | 24.09.2026 | Exit 0, 50 Schritte; Zeichnungsseite, Format 19 |
| 3.28.0 | 23.09.2026 | Gesamtlauf offen (OneDrive-Platzhalter, Zeitüberschreitungen); Tagebuch, Format 18 |
| 3.26.0 | 21.09.2026 | Exit 0, 47 Schritte (Windows, Python 3.13.15); Notizlisten, Format 17 |
| 3.25.0 | 19.09.2026 | Exit 0 (Windows, Python 3.13.15) |

## Offen und nur manuell prüfbar

Einzelpunkte: [Manuelle Prüfung](../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md).

- Bedienung mit echter Maus, Trackpad und Tastatur, vor allem Ziehen (Board, Seitenleiste, Stundenraster), Zeichnen, Chips der Schnelleingabe, „Heute“ und „Tag …“;
- Migration eines echten Bestands (mit Kopie automatisch geprüft; offen bleibt die Sichtkontrolle). **3.29 nach der Umstellung nicht mehr starten**;
- Referenz-Mac-Vollprüfung und Bundle für 3.33.7/3.33.8; Sichtprüfung der Windows-Aufnahmen (W01, W05–W08); Linux-Desktop, Pixelschrift unter Windows und Linux;
- Bildschirmleser (NVDA, VoiceOver); DPI 100/150/200 % und zwei Monitore;
- Druck und PDF mit und ohne Pinnwandhintergrund; flüssige Bedienung mit 500 Karten; Anhänge unter Windows (Prüfliste B13).

**Nicht durch Agenten prüfbar:** Signatur, Notarisierung und Installer; Markenprüfung; Store-Freigabe.

Rohprotokolle bleiben lokal und sind nicht in Git. Erhaltene Original-JSONs bleiben unverändert; ihre früheren Dateipfade können entfernte Artefakte benennen. Die Projektbereinigung hat eigene Werkzeug-, Stand-/Link-, Dateibestand- und Hashprüfungen; ihr Ergebnis steht im [Pflegestatus](DOKUMENTENPFLEGE.md).
