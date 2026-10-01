# Glide – kompakte Weitergabe an einen neuen Chat

Neu in 3.21.4: Ein vollständiger Durchgang durch alle 93 aktiven Dokumente hat zehn aufgeführte falsche Aussagen über den Anwendungscode gefunden – darunter einen erfundenen Dateinamen, eine Grenze, die es nicht gibt, ein ungültiges `BYDAY`-Beispiel und die Zusage, die Kalenderausgabe zeige einem Kalender eine neue Fassung an (`SEQUENCE` steht fest auf `0`). Alle behoben. Die Standprüfung prüft jetzt auch die Formatstufen gegen `DATA_SCHEMA_VERSION`. Anwendungscode unverändert. [Prüfungen und Umfang](../01_Repository/Glide/tests/README.md).

Stand 15.09.2026 · Entwicklungsstand 3.21.4 · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2

Pfade und Links in diesem Dokument gelten relativ zum Ordner `00_Arbeitsvorbereitung` der Arbeitsablage.

Umgesetzt sind Erinnerungen mit Dock-/Taskleistenaufmerksamkeit, Reiter und Pinnwand, Schnellerfassung und gespeicherte Filter, „Mein Tag“, die Tabellenansicht mit listenspezifischen Spalten, Bearbeitungstag und Aufwand, die Tagesplanung mit Tageskapazität, das vollständige App-Backup mit Inhaltsvorschau, die Druck- und PDF-Ausgabe, der CSV-Import mit Spaltenzuordnung, der dauerhafte Änderungsverlauf sowie Kalenderausgabe und Kalenderimport als ICS. Alle Ansichten zeigen dieselben Aufgabenobjekte, IDs, Termine, Wiederholungen und Anhänge.

Durchgehende Grundlage, unabhängig von der jeweils neuesten Funktion: verschachtelte Listen und Ordner, Aufgaben, Long-Tasks, Gruppen, Überschriften und Unterpunkte, Notizen, Fälligkeit mit Uhrzeit, Wichtigkeit, sechs Wiederholungsarten, Erinnerungen innerhalb der laufenden App, Labels, Farben, Beschreibungen und lokale Anhänge an Punkten, Listen und Ordnern, Kalenderansicht, Suche und Offen-Filter, Mehrfachauswahl, Ziehen, Rückgängig und Papierkorb, 16 Praxisvorlagen mit eigenem Katalog zum Bearbeiten, Importieren und Exportieren, TXT-, CSV- und Markdown-Austausch, portable Aufgabenbackups sowie Hell- und Dunkelmodus mit Akzentfarbe und drei Schriftgrößen.

Kanonisch: `01_Repository/Glide/src/glide/app.pyw`. Startbare Kopie: `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.21.4.pyw` mit vollständigen Ressourcen. Python/Tk, lokal ohne Konto oder neue Laufzeitabhängigkeit.

Prüfstand: 3.15.0 bis 3.18.0, **3.21.1**, **3.21.2** und **3.21.3** sind automatisiert abgenommen (macOS/Python 3.14.5, Exitcode 0). Der 3.21.3-Lauf vom 14.09.2026 um 20:45 umfasst **neununddreißig Schritte, siebenunddreißig ausgeführt**: `tests/qa-3.21.3/abschluss/ergebnis.json`; übersprungen blieben allein die plattformgebundene Screenshot-Erzeugung und die Sichtprüfung. Der Lauf zu 3.21.0 war fehlgeschlagen (Exitcode 1, drei Schritte) – zwei Zeitzonenfehler im ICS-Rundlauf und ein Fehler im Fixture-Abgleich, der seit 3.19 nie grün werden konnte; beide Ursachen sind in 3.21.1 behoben, der Beleg bleibt als `tests/qa-3.21.0/abschluss`. Für 3.19.0 und 3.20.0 wurden keine eigenen macOS-Läufe nachgeholt; sie sind im 3.21.1-Lauf enthalten. Der vollständige Abschlusslauf zu **3.21.4** bestand am **15.09.2026 um 10:23** auf macOS mit Python 3.14.5 und `TZ=Europe/Berlin`: **Exitcode 0**, **39 Schritte, davon 37 ausgeführt**. Alle **25 Testsuiten**, drei Analysen, Vorprüfungen sowie Beispiel- und Releaseabgleiche bestanden. Übersprungen blieben ausschließlich die plattformgebundene Screenshot-Erzeugung und die manuelle Sichtprüfung. [Prüfprotokoll](../50_Ablage/QA/qa-3.21.4/abschluss/ergebnis.json). Offen bleiben die native Sichtabnahme auf macOS und Windows, DPI-/Mehrmonitorprofile, Screenreader, Langzeitbetrieb, Installer und Signierung.

[Bedienung 3.21](../01_Repository/Glide/docs/45_KALENDERIMPORT_3.21.0.md) · [Bedienung 3.20](../01_Repository/Glide/docs/archiv/44_KALENDERAUSGABE_3.20.0.md) · [Bedienung 3.19](../01_Repository/Glide/docs/archiv/43_AENDERUNGSVERLAUF_3.19.0.md) · [Bedienung 3.18](../01_Repository/Glide/docs/archiv/42_CSV_IMPORT_3.18.0.md) · [Technische Übergabe](../01_Repository/Glide/docs/09_PROJECT_HANDOFF.md) · [Aktueller Prüfstand und Grenzen](../01_Repository/Glide/docs/07_QA_BERICHT.md).

## Wo liegt was

| Ort | Inhalt |
|---|---|
| `01_Repository/Glide/src/glide/app.pyw` | **kanonische Anwendung**, ein Monolith. Alles andere ist Kopie oder abgeleitet. |
| `01_Repository/Glide/AGENTS.md` | verbindliche Änderungsregeln. Vor jeder Änderung lesen. |
| `01_Repository/Glide/docs/` | Bedienverträge je Funktion (Dateiname trägt die Version ihrer Entstehung), Index, QA-Bericht, Entscheidungen, Archiv |
| `01_Repository/Glide/tests/integration/` | 25 Suiten; `tests/tools/` die Werkzeuge, `tests/fixtures/` Referenzformate und Beispielbestände |
| `01_Repository/Glide/tests/qa-<version>/abschluss/` | Belege abgeschlossener Prüfläufe, `ergebnis.json` je Lauf |
| `00_Arbeitsvorbereitung/` | **diese Weitergabe** (genau eine aktive), Notizen, Checklisten, Entscheidungen je Version |
| `05_Probelisten_Testdaten/` | Nutzerkopien der Probedateien zum Ausprobieren, mit eigener Prüfwege-Tabelle |
| `07_Python-Versionen/` | startbare Fassungen je Version samt `resources/` |
| `10_Dokumentation/`, `40_Store_Material/` | Vorlagenanleitung, Produktdatenblatt, Store-Arbeitsstände |
| `50_Ablage/` | Werkzeuge und Vorfassungen abgeschlossener Versionssprünge, QA-Nachweise, Screenshots |

In **jedem** Ordner gilt: überholte Fassungen liegen in `archiv/` beziehungsweise `Archiv/` desselben Ordners, nichts wird gelöscht. Der Prüfstand verlangt, dass **jede** Datei unter `docs/` – Archiv eingeschlossen – im Index `docs/00_INDEX.md` steht.

## Wie ein neuer Stand abgelegt wird

Bewährter Weg, weil die Geräteverbindung zur Ablage langsam und unzuverlässig ist:

1. Entwickeln und prüfen in einer Arbeitskopie, **nicht** in der Ablage.
2. Ein **einziges** ZIP mit Quellstand, Ablageskript und Fortschreibungsskript übertragen. Einzeldateien laufen in Zeitüberschreitungen; 16 Dateien haben das nachweislich getan.
3. `ablegen_<version>.py` legt den Quellstand ab, archiviert Vorfassungen, prüft jede Datei über SHA-256 und ist wiederholbar.
4. `fortschreiben_<version>.py --probe` **zuerst**. Der Probelauf zeigt jede Änderung, ohne zu schreiben, und bricht ab, wenn eine Pflichtstelle nicht zum erwarteten Wortlaut passt. Er hat mehrfach echte Denkfehler gefunden, bevor sie Schaden anrichteten.
5. Danach derselbe Aufruf ohne `--probe`. Beide Skripte sind wiederholbar; ab dem zweiten Lauf bleibt alles still.
6. Endkontrolle: `pruefen.py --modus schnell`, `tests/tools/standpruefung.py`, ablageweite Linkprüfung, Restsuche nach der Vorversion, Werkzeugordner nach `50_Ablage/Archiv`.
7. Diese Weitergabe fortschreiben und als Projektdokument hochladen.
8. Nach dem Prüflauf das Ergebnis in QA-Bericht, Weitergabe und Technische Fakten **derselben** Version eintragen. Bis 3.21.2 stand es immer erst in den Dokumenten der nächsten Version – dadurch behauptete jeder Stand, sein eigener Prüflauf stehe noch aus.

## Fallen, die Zeit gekostet haben

- **Eine Zahl im Zweck einer Werkzeugtabelle rottet.** `tests/tools/README.md` beschrieb den Vollprüflauf als „Achtzehn Suiten“, den Beispielerzeuger als „Format 14“ und die Releaseplanung als „für 3.14“ – drei Angaben, die bei jedem Stand hätten mitgehen müssen. Zwecke ohne Zahl formulieren und die Zahl im Quelltext an eine Konstante binden.
- **Eine Formatstufe gehört nicht in Prosa.** Fünf Dokumente trugen eine überholte: `SECURITY.md` „Formate 4 bis 12“, `06_DATA_BACKUP_MIGRATION.md` „Formate 4–14“, `PRODUCT_IDENTITY.md` vier Werte auf Format 13 und App-Version 3.14.0. Seit 3.21.4 prüft `standpruefung.py` das gegen den Code.
- **Ein Linktext muss halten, was er verspricht.** An vier Stellen zeigte „Produktdatenblatt“ auf den Ordner-README, an zwei Stellen hieß eine Vorschlagsliste „Aktuelle Funktionsübersicht“. Ein Linktext, der etwas anderes verspricht als sein Ziel, führt jeden externen Agenten in die Irre.
- **Ein historisches Dokument darf keine Gegenwart behaupten.** Sieben solche Sätze standen in Dokumenten, die als historisch gekennzeichnet sind – vom „aktuellen Quellstand“ bis zu „Nächste Schritte: … Reiteransicht“, die seit 3.10.0 umgesetzt ist. Präteritum verwenden oder die Umsetzung benennen.
- **Ein von Hand gepflegtes Banner „Aktueller Entwicklungsstand“ rottet.** Sechs historische Dokumente trugen eines; drei standen auf 3.14.0, drei auf 3.21.0. Historische Dokumente verweisen ohne Nummer auf Index und QA-Bericht, dann kann die Angabe nicht falsch werden. Die Version steht in genau einer Zeile je Dokument, und `tests/tools/standpruefung.py` prüft das.
- **Versionen in Linktexten fortgeschriebener Dokumente rotten genauso.** Im Index stand „QA-Bericht 3.21.0“, während der Bericht bei 3.21.2 lag. Linktext ohne Nummer, wenn das Ziel fortgeschrieben wird.
- **Die neunzehn versionierten Releaseplanungen in `tests/fixtures/beispiele` gehören nicht ins Archiv.** Die Fixtureprüfung erwartet bei versioniertem Dateinamen genau dessen Version; die Reihe ist der Migrationsnachweis. Nur die unversionierten Bestände werden ersetzt und ihre Vorfassung archiviert.
- **Prüfläufe nie in UTC.** Bei Versatz null ist jeder Zeitzonenfehler unsichtbar. Der `UNTIL`-Fehler aus 3.21.0 war in einer UTC-Vorabumgebung grün und fiel erst im macOS-Lauf auf. `pruefen.py` setzt darum `TZ=Europe/Berlin`, wenn der Aufrufer keine Zone vorgibt.
- **`mv -n` tut nichts, wenn das Ziel existiert** – still, mit Rückgabewert 0. Wer danach nur das Archiv prüft, hält das Verschieben für erfolgreich, während die Datei noch aktiv daneben liegt. Immer die **Quelle** prüfen.
- **Versionsangaben stehen in mehreren Schreibweisen.** `**3.21.0**`, `· Glide 3.21.0`, `– Glide 3.21.0`, `Stand 3.21.0`, `v3.21.0.pyw`. Eine Tokenliste, die nur eine Form kennt, lässt READMEs jahrelang auf einem alten Stand stehen. Nach dem Fortschreiben mit `grep -rlF` gegen **jede** Form suchen.
- **Pauschale Ersetzungen zerschreiben Belegstellen.** `qa-3.21.0 → qa-3.21.1` hätte genau die Stellen getroffen, die den fehlgeschlagenen Lauf dokumentieren. Nur den Verweis auf den *maßgeblichen* Lauf mitziehen.
- **Der Fixture-Abgleich vergleicht die Fixture mit ihrer eigenen Neuerzeugung.** Ein überholter Text in beiden fällt nicht auf. So stand „Stand: 3.14.0 / Datenformat 13" sieben Versionen lang unbemerkt im Releasebestand. Solche Angaben an Konstanten binden.
- **Unreproduzierbare Werte gehören aus dem Abgleich heraus.** `history[].at` entsteht beim Speichern; solange es verglichen wurde, konnte der Schritt seit 3.19 nie grün werden.
- **Der Index ist Pflicht.** Jede neue Datei unter `docs/`, auch eine Archivkopie, muss in `00_INDEX.md`. Sonst schlägt der Prüfstand fehl – zuverlässig und zu Recht.

## Datenregeln je Stand

Datenregeln von 3.21.4: Kein Formatsprung, kein neues Feld, keine Änderung am Anwendungscode. `standpruefung.py` prüft zusätzlich die **Formatstufen**: Eine Formatangabe in einer Standzeile muss `DATA_SCHEMA_VERSION` entsprechen (R6), ein Formatbereich muss von `MIN_PORTABLE_BACKUP_SCHEMA_VERSION` bis dorthin reichen (R7), und eine Tabellenzeile „Datenformat“ oder „App-Version“ nennt die aktuellen Werte (R8). Die Werte liest das Werkzeug über den Syntaxbaum aus `app.pyw` – ein Import würde Tk starten und den echten Nutzerdatenordner anfassen. Der Änderungsverlauf ist von der Formatprüfung ausgenommen: Dort war „Formate 2 bis 9“ damals richtig. `tests/tools/README.md` und `src/glide/README.md` werden seit 3.21.4 mit dem Quellstand ausgeliefert, zusammen mit den beiden Testberichten aus 3.21.3.

Datenregeln von 3.21.3: Kein Formatsprung, kein neues Feld, keine Änderung am Anwendungscode. Neu ist `tests/tools/standpruefung.py` als dritte Analyse: Ein Dokument mit Version oder Datum im Dateinamen, in einem Versionsordner oder mit „historisch“ im Titel gilt als **festgeschrieben** und darf keinen aktuellen Stand behaupten; jedes andere aktive Dokument muss eine Standzeile mit der Version aus `VERSION` tragen. Zitate und Codespannen sind ausgenommen, sonst meldet die Prüfung den Satz, der den Fehler dokumentiert. `tests/README.md` und `tests/fixtures/README.md` werden seit 3.21.3 mit dem Quellstand ausgeliefert und gehen damit über den SHA-256-Abgleich statt über Fortschreibungsregeln.

Datenregeln von 3.21.2: Kein Formatsprung, kein neues Feld, keine Änderung am Anwendungscode. Der Beispielbestand wächst von 149 auf 166 Punkte und von 11 auf 12 Listen; alle Zusicherungen der Suiten sind Untergrenzen und bleiben gültig. `tests/tools/releasedaten.py` bindet seine Standangaben an `APP_VERSION` und die neue Modulkonstante `DATA_SCHEMA_VERSION`; bis 3.21.1 hing an jedem Codebeleg unverändert „Stand: 3.14.0 / Datenformat 13“, sieben Versionen überholt. Die Probedateien in `05_Probelisten_Testdaten` sind die Nutzerkopien der Repo-Bestände und tragen jetzt denselben Stand; acht überholte Fassungen liegen im Archiv.

Datenregeln von 3.21.1: Kein Formatsprung, kein neues Feld. `UNTIL` trägt in der Kalenderausgabe dieselbe Zeitform wie `DTSTART` – ohne „Z“ beim Uhrzeittermin, als Datum beim Ganztagstermin. Beim Lesen nimmt `parse_ics_until` den Kalendertag der Angabe ohne Zeitzonenumrechnung, weil `UNTIL` eine Datumsgrenze ist und kein Zeitpunkt. Im Prüfstand bleiben die Verlaufszeiten (`history[].at`) aus dem Fixture-Abgleich heraus, genauso wie `exported_at`; Suiten laufen ohne eigene Vorgabe unter `TZ=Europe/Berlin`.

Datenregeln von 3.21: Der Kalenderimport liest eine gewählte Datei und schreibt selbst keine. Punkte entstehen über `new_item`, Labels über `ensure_label_by_name`; bestehende Punkte werden nie überschrieben. Eigene UIDs gelten als Duplikat und werden übersprungen; nicht abbildbare Wiederholungsregeln und Erinnerungen werden verworfen und gezählt. Grenzen: 2000 Termine, 12 MB je Datei. Ein Import ist ein Rückgängig-Schritt einschließlich neuer Labels.

Datenregeln von 3.20: Die Kalenderausgabe ist rein lesend – sie schreibt nur ICS-Dateien an ein gewähltes Ziel (atomar, Nutzdatendateien ausgeschlossen), verändert weder Bestand noch Einstellungen und erzeugt keinen Verlaufseintrag. Termine stehen in schwebender Ortszeit, nur `DTSTAMP` und feste Alarme in UTC; die UID je Punkt ist stabil, damit erneutes Einlesen aktualisiert statt verdoppelt. Obergrenze 2000 Termine.

Datenregeln von 3.19: `history` liegt neben den Aufgabenfeldern; Format 14 wird beim ersten Speichern auf 15 gehoben, vorher entsteht `liste_vor_format15_*`. Der Verlauf entsteht in `update_history` beim Speichern aus dem Vergleich zweier Stände; `normalize_lists_data` legt einen gelesenen Verlauf nur in `_loaded_history` ab, damit ein fremdes Archiv das laufende Protokoll nicht überschreibt. Obergrenze 4000 Einträge, Sammeleinträge ab 25 gleichartigen Ereignissen, abschaltbar über `history_enabled`. Rückgängig nimmt den Bestand zurück, nicht das Protokoll.

Datenregeln von 3.18: Der CSV-Import liest eine gewählte Datei und schreibt selbst keine Datei. Punkte entstehen ausschließlich über `new_item`, Labels über `ensure_label_by_name`; bestehende Punkte werden nie überschrieben. Der Vorgang ist ein einzelner Rückgängig-Schritt einschließlich neuer Labels; scheitert er, werden Labelbestand und Rückgängig-Stapel exakt zurückgesetzt. Grenzen: 5000 Zeilen, 64 Spalten, 12 MB je Datei, geprüft vor jeder Bestandsänderung. Aufgabenformat 14 bleibt unverändert.

Datenregeln von 3.17: Die Druckausgabe liest nur vorhandene Objekte, schreibt ausschließlich HTML an ein gewähltes Ziel oder in den temporären Ordner und verändert weder Aufgaben noch Einstellungen; Nutzdatendateien sind als Ziel ausgeschlossen, die Obergrenze liegt bei 2000 Punkten.

Datenregeln von 3.16: Das App-Backup ist dasselbe ZIP wie ein Komplettbackup, ergänzt um den JSON-Abschnitt `app_backup` (`settings` ohne Tageshistorien, `templates`, `activity`). Ältere Fassungen lesen die Datei weiterhin als Aufgabenbackup. Aufgaben laufen beim Wiederherstellen durch `import_full_backup`; vor dem Ersetzen entstehen `vor_import_*.glidebackup`, `settings_vor_restore_*.json` und `vorlagen_vor_restore_*.json`. Ansichtsverweise werden nur zusammen mit den Aufgaben desselben Archivs übernommen.

Datenregeln von 3.15: `planning_summary` ist die einzige Rechenstelle für alle Aufwandssummen; gezählt werden nur Aufgaben und Long-Tasks, Punkte ohne Schätzung getrennt, erledigte bleiben in der Summe. Die Tageskapazität liegt additiv als `daily_capacity_minutes` (0–1440, Vorgabe 0 = kein Vergleich) in den Einstellungen, der betrachtete Tag nur im Laufzeitzustand. Aufgabenformat 14 bleibt unverändert; Backups enthalten weder Kapazität noch Ansichtszustand.

Der 3.9-Bestand mit einheitlichen eingebetteten Dropdowns, App-Aktionen, kompaktem Kopf, Einstellungen und ausblendbarer Seitenleiste bleibt erhalten. Benachrichtigungen erscheinen bei laufender App, optional mit Dock-/Taskleistenaufmerksamkeit. Echte Systemzustellung hängt an installierter Registrierung und Signierung. Kein Autostart-Hilfsprozess. [Entscheidung](../01_Repository/Glide/docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md).

## Änderungsdisziplin

Vor Änderungen `AGENTS.md` lesen, aktuelle Tests ausführen und alle App-Importe mit temporärem `GLIDE_DATA_DIR` isolieren – ein Import ohne diese Isolierung arbeitet auf dem echten Nutzerdatenordner. Aufgabenmutationen über `item_change`, Container über `sidebar_change`, Struktur über `guarded_structural_change`, Dialoge über `run_modal`. Symbole aus `ICONS`. Dokumentvorfassungen archivieren, nie überschreiben. Keine neue Laufzeitabhängigkeit ohne dokumentierte Entscheidung. Nie echte Nutzdaten als Testbestand öffnen und keine vorhandenen Nutzerdaten durch ein Beispielbackup ersetzen.

Nächste offene Ideen: benutzerdefinierte Felder und darauf aufbauende eigene Ansichten; eine echte Kalendersynchronisierung bleibt bewusst außen vor. Größere Pinnwandoptionen separat planen. Keine zusätzliche Projektmappe oder parallele Statusablage. [Vorschläge und Einordnung](Glide_Funktionsvorschlaege_2026-09-11.md) · [Offene Entscheidungen](Entscheidungen/Offene_Entscheidungen_3.21.4.md).
