# Manuelle Prüfung – Glide 3.21.4

Stand: 15.09.2026 · Glide 3.21.4 · interner Entwicklungsstand · Aufgabenformat 15

3.21.4 ändert keinen Anwendungscode außer der Versionsangabe. Geprüft wird
deshalb nicht die App, sondern die Dokumentation: ob die aufgeführten falschen
Codeaussagen jetzt das tatsächliche Verhalten beschreiben, ob keine überholte
Formatstufe mehr in einer Standangabe steht, ob jeder Linktext hält, was er
verspricht, und ob kein historisches Dokument mehr Gegenwart behauptet. Der
maschinelle Teil steckt in `tests/tools/standpruefung.py` (jetzt R1 bis R8);
diese Liste prüft, was eine Maschine nicht prüfen kann – nämlich jede Aussage
über Verhalten.

**Arbeitsweise für die Codeaussagen:** Jeder Schritt nennt die Belegstelle in
`src/glide/app.pyw`. Prüfe gegen die Datei, nicht gegen die Erinnerung und nicht
gegen ein früheres Dokument – genau dieser Abgleich hat die zwölf Befunde
erzeugt. Alle Befehle laufen aus `01_Repository/Glide/`.

## Vor der Prüfung

- [ ] Eigenen Datenordner sichern oder `GLIDE_DATA_DIR` auf einen leeren Ordner
      setzen. Das Wiederherstellen eines App-Backups **ersetzt** den Bestand.
- [ ] `05_Probelisten_Testdaten/Glide-Funktionsvorschau_3.21.4.glidebackup` über
      „Listen/Ordner hinzufügen …“ einlesen.

## Standprüfung

- [ ] `python3 tests/tools/standpruefung.py` im Repository: Exitcode 0, keine
      Befunde. Die Kopfzeile nennt vier Zahlen; erwartet werden **93 aktive
      Dokumente (37 fortgeschrieben, 52 festgeschrieben, 4 ohne Standaussage)**.
      Weicht die Summe ab, ist ein Dokument neu, verschoben oder archiviert –
      dann zuerst `docs/00_INDEX.md` prüfen, nicht die Zahl in dieser Liste.
- [ ] Gegenprobe zu R1 bis R5: In einer **Kopie** eines READMEs die Version auf
      3.21.0 setzen, Prüfung erneut laufen lassen – sie muss die Datei mit
      Regelnummer melden. Kopie danach entfernen.
- [ ] Gegenprobe zu R6 bis R8 (neu): In derselben Art Kopie „Format 15“ auf
      „Format 14“ setzen und eine Tabellenzeile `| Datenformat | 15 |` auf `14`.
      Beide Änderungen müssen als R6 beziehungsweise R8 gemeldet werden.
- [ ] Nach „3.21.3“ in aktiven Dokumenten suchen; Archivordner und
      Werkzeugarchive ausschließen. Treffer dürfen nur
      Belegstellen sein: die Abschnitte zu 3.21.3 in Änderungsverlauf,
      QA-Bericht und Weitergabe, der Prüfbeleg `tests/qa-3.21.3/abschluss`, die
      Archivnachweise (`_vor_3.21.4`, `Werkzeuge_3.21.3`) in `docs/00_INDEX.md`
      und den Ordner-READMEs sowie die drei versionsbenannten Notizen aus
      3.21.3 im jeweiligen `Archiv/`. Keine aktive Standangabe.

## Die aufgeführten Codeaussagen

- [ ] `docs/43_AENDERUNGSVERLAUF_3.19.0.md` nennt die Nutzdatendatei
      **`liste_speicher.json`**. Beleg: `grep -n "SAVE_FILE = " src/glide/app.pyw`
      → `os.path.join(BASE_DIR, "liste_speicher.json")`. Der frühere Name
      `glide_liste.json` darf im Bedienvertrag nicht mehr als Nutzdatendatei
      bezeichnet werden. Zitate in Befundberichten und Archivfassungen bleiben
      als historische Belege erhalten.
- [ ] Dasselbe Dokument nennt **eine** Zeilenzahl für den Änderungsverlauf, nicht
      400 und 412 im selben Satz.
- [ ] `docs/45_KALENDERIMPORT_3.21.0.md` nennt **keine Zeilenobergrenze** mehr,
      sondern die beiden echten Grenzen. Beleg:
      `grep -n "MAX_ICS_IMPORT" src/glide/app.pyw` → `MAX_ICS_IMPORT_EVENTS = 2000`
      und `MAX_ICS_IMPORT_BYTES = 12 * 1024 * 1024`. Eine Zeilengrenze gibt es
      nur im CSV-Vertrag, dort zu Recht.
- [ ] Dasselbe Dokument verspricht **nicht** mehr, erledigte Termine zu
      überspringen. Beleg: `grep -n "CANCELLED" src/glide/app.pyw` – geprüft wird
      ausschließlich `CANCELLED`; ein `VEVENT` hat keinen Erledigt-Zustand, und
      `VTODO` ist ausgeschlossen.
- [ ] `docs/44_KALENDERAUSGABE_3.20.0.md` sagt, dass ein **Bearbeitungstag auch
      ohne Fälligkeit** einen Planungstermin erzeugt. Beleg: in
      `build_ics_document` hängt der Planungstermin allein an
      `options.get("planned")` und `ics_event_lines(..., "planned", ...)`, nicht
      an der Fälligkeit. Der alte Wortlaut „Ohne Fälligkeit gibt es keinen
      Termin“ darf nicht mehr vorkommen.
- [ ] Dasselbe Dokument zeigt in jedem `BYDAY`-Beispiel nur zulässige Token.
      Beleg: `grep -n "ICS_WEEKDAYS = " src/glide/app.pyw` →
      `("MO", "TU", "WE", "TH", "FR", "SA", "SU")`. Gegenprobe:
      `grep -rIn "BYDAY=[A-Z,]*DI" docs/` muss leer sein.
- [ ] Dasselbe Dokument stützt die Wiedererkennung im Kalender allein auf die
      **stabile UID**. Beleg: `grep -n "SEQUENCE" src/glide/app.pyw` → die Zeile
      steht fest auf `"SEQUENCE:0"` und wird nie erhöht. Eine Zusage, der
      Kalender zeige eine neue Fassung an, darf nicht mehr darin stehen.
- [ ] `docs/41_DRUCK_UND_PDF_3.17.0.md` verspricht **keine mitgelieferte
      Schrift** in der Druckdatei. Beleg: die Registrierung in `app.pyw`
      (`AddFontResourceExW` unter Windows, `CTFontManagerRegisterFontsForURL`
      unter macOS) wirkt prozesslokal; die Druckdatei nennt DejaVu Sans nur als
      erste Wahl einer CSS-Kette und bindet keine Web-Schrift ein.
- [ ] Gesamtprobe: `python3 tests/tools/analyse_statisch.py` und
      `analyse_erreichbarkeit.py` bleiben grün – die Korrekturen betreffen nur
      Dokumente, kein Verhalten.

## Formatstufen

- [ ] Aktuelle Standangaben nennen Aufgabenformat **15** und die lesbaren
      portablen Formate **4 bis 15**. Historische Verträge und
      Migrationsbelege behalten ihre damaligen Formatstufen. Fünf Stellen waren betroffen und sind
      nachgezogen: `SECURITY.md`, `docs/06_DATA_BACKUP_MIGRATION.md`,
      `docs/decisions/PRODUCT_IDENTITY.md` (vier Werte), `src/glide/README.md`,
      `docs/27_VORLAGEN_PRAXISANLEITUNG.md`.
- [ ] `PRODUCT_IDENTITY.md` ordnet die lokalen Erinnerungen **Format 13 / 3.8.0**
      zu, nicht Format 14.
- [ ] `CHANGELOG.md` behält historische Formatbereiche wie „Formate 2 bis 9“ und
      vergleichbare historische Angaben – der Änderungsverlauf ist von R6/R7
      ausgenommen, weil die Angaben dort zum jeweiligen Stand richtig waren.

## Verweise

- [ ] Viermal zeigt „Produktdatenblatt“ jetzt auf
      `40_Store_Material/Produktdatenblatt_3.21.4.md`, nicht auf den
      Ordner-README.
- [ ] Die beiden Verweise auf `Glide_Funktionsvorschlaege_2026-09-11.md` heißen
      nicht mehr „Aktuelle Funktionsübersicht“ – es ist eine Vorschlagsliste.
- [ ] `05_Probelisten_Testdaten/README.md` verweist für die Funktionen aus 3.10
      bis 3.13 auf die **jeweils eigenen** Verträge, nicht auf den 3.9-Vertrag.
- [ ] `30_Release_Exports/README.md` bietet den 3.13-Vertrag nicht mehr als
      „Bedienung und Änderungen“ an.
- [ ] `python3 tests/tools/pruefen.py --modus voll` prüft die Auflösbarkeit
      aller Links (zuletzt 708). Das findet ein falsches **Ziel** nicht – nur
      ein fehlendes. Der Linktext bleibt Sichtprüfung.

## Historische Dokumente

- [ ] Kein als historisch gekennzeichnetes Dokument behauptet Gegenwart.
      Betroffen waren `docs/08_CODE_BEFUND.md` („aktueller lokaler
      Python-/Tk-Quellstand“), `docs/28_ABLAGEPRUEFUNG_2026-09-11.md`
      („inzwischen“), `docs/30_DOKUMENTATIONSABGLEICH_2026-09-12.md`
      („verweisen inzwischen“), `docs/25_FEATURE_ABGLEICH_3.7.0.md` („steht noch
      aus“ – am 13.09.2026 nachgeholt), `docs/12_ABSCHLUSSBERICHT.md`
      („Nächste Schritte: … Reiteransicht und Pinnwand“ – seit 3.10.0 umgesetzt),
      `docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md` („2. Reiteransicht angehen“)
      und `50_Ablage/QA/Dokumentation/README.md` (drei Stellen, darunter „Die
      aktuelle App-Prüfung liegt unter `tests/qa-3.13.0/`“).
- [ ] Stichprobe: `grep -rIn "inzwischen\|aktuelle" docs/08_CODE_BEFUND.md
      docs/28_ABLAGEPRUEFUNG_2026-09-11.md` – Treffer müssen sich auf den
      damaligen Stand beziehen und im Präteritum stehen.

## Widersprüche zwischen Dokumenten

- [ ] `50_Ablage/README.md` nennt `10_Dokumentation` **nicht** mehr die
      „aktuelle Word-Arbeitsgrundlage“; der Ordner-README dort führt die
      Word-Berichte als archiviert und die Markdown-Dokumente als aktuelle
      Quelle. Beide Aussagen decken sich jetzt.
- [ ] `50_Ablage/README.md` verlangt nicht mehr, Renderläufe bis auf den letzten
      zu archivieren – der Renderlauf-README hält fest, dass keiner gelöscht
      wurde.

## Ausgelieferte READMEs

- [ ] Vier Dateien gehen über den SHA-256-Abgleich des Ablageskripts statt über
      Fortschreibungsregeln: `tests/README.md`, `tests/fixtures/README.md`
      (seit 3.21.3), `tests/tools/README.md`, `src/glide/README.md` (neu). Das
      Ablageskript meldet für jede „gleich“ oder „ersetzt“, nie „unbekannt“.
- [ ] `tests/tools/README.md` nennt **25 Suiten**, führt `standpruefung.py` und
      `vorlagendaten.py` in der Werkzeugtabelle und beschreibt die Zwecke **ohne
      Versions- und Formatzahlen**. Der Windows-Nachweis trägt Datum und Stand.
- [ ] `src/glide/README.md` nennt Aufgabenformat 15 und keine Funktionsliste,
      die bei 3.13 endet.

## Eigene Zählfehler

- [ ] Der 3.21.3-Eintrag im Änderungsverlauf nennt **zwanzig** versionierte
      Releaseplanungen und **zehn** archivierte startbare Fassungen (3.14.0 bis
      3.21.2) und trägt die Farbkorrektur aus `beispieldaten.py` nach.
- [ ] Der Satz über die durchgehende Grundlage steht wortgleich in **vier**
      Dokumenten: Wurzel-README, `01_Repository/Glide/README.md`,
      `docs/09_PROJECT_HANDOFF.md` und der Weitergabe. Produktdatenblatt und
      `05_Probelisten_Testdaten/README.md` führen ihre eigene Funktionstabelle –
      sie gehören **nicht** dazu.
- [ ] `tests/fixtures/README.md` nennt **einundzwanzig** aktiv liegende
      Releaseplanungen (3.5.0 bis 3.21.4) und begründet, warum sie nicht ins
      Archiv gehören.

## Archivierung

- [ ] `07_Python-Versionen` enthält aktiv nur
      `Glide-Aufgaben-und-Listen_v3.21.4.pyw`, den README, `resources/` und
      `Archiv/`. **Ausnahme:** `__pycache__` liegt weiterhin dort (Bytecode zu
      3.6/3.7). Die Geräteverbindung darf nicht löschen, und ein `__pycache__`
      ins Archiv zu verschieben wäre unsinnig – es entsteht beim nächsten Start
      neu. Das ist eine offene Entscheidung, kein Befund. Die Fassungen 3.14.0
      bis 3.21.3 liegen im Archiv (elf Stück).
- [ ] Die startbare Fassung 3.21.4 startet und zeigt in „Über Glide“ die
      Version 3.21.4.
- [x] `Claude outputs` ist leer; das Übertragungspaket liegt unter
      `50_Ablage/Archiv/Uebertragungspakete`.
- [x] `05_Probelisten_Testdaten` enthält aktiv nur die drei 3.21.4-Dateien und
      den README; alle älteren Fassungen liegen in `Archiv/`.
- [x] `00_Arbeitsvorbereitung/Notizen`, `Checklisten` und `Entscheidungen`
      enthalten je nur die 3.21.4-Fassung; die 3.21.3-Fassungen liegen im
      jeweiligen `Archiv/`.
- [x] `tests/fixtures/beispiele` enthält weiterhin **alle** versionierten
      Releaseplanungen von 3.5.0 bis 3.21.4. Sie gehören dorthin und dürfen
      nicht archiviert werden.
- [x] `50_Ablage/Archiv/Werkzeuge_3.21.4` enthält Ablage- und
      Fortschreibungsskript dieses Stands.

## Beispielbestand (Rückfallprüfung, unverändert gegenüber 3.21.3)

- [ ] Die Liste „Kalender, Erinnerungen und Tagesplanung“ im Ordner
      „Website-Betrieb“ hat eine **Farbe** (Braun); „Ablage & Ideen“ bleibt die
      einzige Liste ohne Farbe – das ist gewollt.
- [ ] Ansicht → Tagesplanung, heutiger Tag: **sechs** Punkte, Summe **270
      Minuten**; morgen **ein** Punkt mit 120 Minuten.
- [ ] Beide Erinnerungsarten stehen an „Rückruf Bauträger“ (relativ, 30 Minuten)
      und „Angebotsfrist Parkquartier“ (fest, Vortag 8 Uhr).
- [ ] Alle sechs Wiederholungsarten sind vertreten; die Wochentagsserie Mo/Mi
      trägt ein Enddatum.

## Kalenderrundlauf (Rückfallprüfung)

- [ ] Kalenderausgabe als ICS für die Liste, Datei im Texteditor ansehen:
      `UNTIL` steht **ohne „Z“** und beim Ganztagstermin als reines Datum;
      jedes `BYDAY` nennt nur Token aus `ICS_WEEKDAYS`; jede `SEQUENCE`-Zeile
      steht auf `0`.
- [ ] Mit eingeschalteter Planungsausgabe erzeugt ein Punkt **ohne Fälligkeit,
      aber mit Bearbeitungstag** einen Termin – die Stelle, die der alte Vertrag
      falsch beschrieb.
- [ ] Dieselbe Datei importieren: alle Termine als Duplikate übersprungen.
- [ ] Gegentest mit ersetzten `UID:`-Zeilen: Aufgaben entstehen, das Serienende
      bleibt der 140. Tag – auch nach einem Wechsel der Systemzeitzone.

## Prüflauf

- [x] `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.21.4/abschluss`
      auf dem Mac: Exitcode 0, **neununddreißig** Schritte, davon
      siebenunddreißig ausgeführt; übersprungen bleiben allein die
      plattformgebundene Screenshot-Erzeugung und die Sichtprüfung.
- [x] Ergebnis danach in QA-Bericht, Weitergabe und Technische Fakten **dieses**
      Stands eintragen – nicht erst beim nächsten. Bis 3.21.2 stand das Ergebnis
      immer in den Dokumenten der Folgeversion; dadurch behauptete jeder Stand,
      sein eigener Prüflauf stehe noch aus.

## Offen und nicht Teil dieser Prüfung

Native Sichtabnahme unter Windows, DPI- und Mehrmonitorprofile, Screenreader,
Langzeitbetrieb, Installer und Signierung.

## Nachweis der Ablageprüfung am 15.09.2026

Der vollständige Abschlusslauf zu **3.21.4** bestand am **15.09.2026 um 10:23** auf macOS mit Python 3.14.5 und `TZ=Europe/Berlin`: **Exitcode 0**, **39 Schritte, davon 37 ausgeführt**. Alle **25 Testsuiten**, drei Analysen, Vorprüfungen sowie Beispiel- und Releaseabgleiche bestanden. Übersprungen blieben ausschließlich die plattformgebundene Screenshot-Erzeugung und die manuelle Sichtprüfung.

Die markierten Punkte wurden ausgeführt. Weitere Kontrollkästchen bleiben als
manuelle Prüfwege bestehen. Der [Ablagenachweis](../../50_Ablage/Archiv/Werkzeuge_3.21.4/Ablageprotokoll_2026-09-15.md) dokumentiert Archivierung, Prüfsummen und die ergänzenden Korrekturen.
