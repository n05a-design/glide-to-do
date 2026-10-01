# Glide

Glide ist eine lokale Desktop-App für Aufgaben, Listen und einfache Notizen. Die Anwendung läuft ohne Benutzerkonto, Cloudpflicht oder Server und speichert ihre Nutzdaten außerhalb des Programmordners.

## Aktueller Stand

- App-Version: 3.4.0
- Datenformat: 11 (seit 3.5.0; Migration aus 10 ist additiv)
- Reifestufe: interner, getesteter Vorabstand; noch kein signiertes Store-Release
- Kanonischer Quellstand: `src/glide/app.pyw`
- Historische Einzeldateien: außerhalb des Repository-Bereichs unter `07_Python-Versionen/`

Version 3.5 bringt **wiederkehrende Aufgaben**: täglich, alle N Tage, an festen
Wochentagen, wöchentlich, monatlich oder jährlich, wahlweise mit Enddatum. Beim
Abhaken rückt der Punkt auf seinen nächsten Termin vor; es wird nichts im Voraus
erzeugt und nichts gemeldet. Details in
[Wiederholungen 3.5](docs/15_WIEDERHOLUNGEN_3.5.0.md).

Ein Nachtrag innerhalb von 3.4.0 schleift die Oberfläche nach: Symbole aus einer
Zeichenfamilie, abgerundete Startseitenkacheln mit gleichen Rändern, wechselnde
Begrüßungen und eine Fälligkeitsspalte, in die Datum und Uhrzeit immer vollständig
passen. Details in [Oberfläche 3.4 – Nachtrag](docs/14_OBERFLAECHE_NACHTRAG_3.4.0.md).

Version 3.4 ergänzte eine persönliche Startseite, **Bearbeiten → Einstellungen**,
farbige Eingaben, feste Artlabels im Punktdialog, ausgerichtete Seitenleistenzähler
und Hilfe im aktiven Theme. Bedienung, Symbolvergleich und Grenzen stehen in
[Oberfläche 3.4](docs/13_OBERFLAECHE_3.4.0.md).

Historisch: Version 3.2 brachte:

- **Textzeichen in der zentralen Symboltabelle.** Anhang `⊕`, Fälligkeit `▦` – die
  zentralen Symbole stehen in `ICONS`. Gruppenmarker, hohe Wichtigkeit und
  Beschreibungsmarker sind noch Emoji-Ausnahmen (siehe Produktgrenzen). Farbige
  Emoji kommen aus einer Ersatzschrift des Systems, ignorieren die Textfarbe und
  sind auf Windows und macOS verschieden breit.
- **Keine Übernahme aus fremden Ordnern.** Glide sucht beim Start nicht mehr in
  Verzeichnissen früherer Programmnamen nach Nutzerdaten.
- **Ein ausführlicher Beispielbestand zum Einlesen** – zehn Listen in fünf teils
  verschachtelten Ordnern, 140 Punkte mit Gruppen, Notizen und
  Zwischenüberschriften.

Version 3.1 war eine Aufräumversion ohne neue Bedienfunktion:

- **Gemeinsame Rahmen für Änderungen.** `item_change` und
  `sidebar_change` ersetzen eine Abfolge, die an 36 Stellen wörtlich im
  Quelltext stand. Wer den Rücknahme-Zweig vergaß, hinterließ einen
  Rückgängig-Schritt, der nichts zurücknimmt – das kann jetzt nicht mehr
  passieren.
- **Ein gemeinsamer Weg für jeden modalen Dialog.** `run_modal` gibt den
  Tastatur- und Mausgriff an das aufrufende Fenster zurück. Vorher tat das eine
  von sieben Stellen; die übrigen hinterließen eine Maske, die sichtbar blieb,
  aber keine Eingabe mehr annahm.
- **Behoben:** Bei vollem Rückgängig-Speicher kostete eine wirkungslose Aktion
  den ältesten Schritt.

Version 3.0 brachte:

- **Eine ruhigere Farbgebung.** Schwarz weicht im Hellmodus einem Dunkelblau; der Dunkelmodus bleibt grau.
- **Mehr Liste, weniger Rand.** Die Übersicht der Listen und Ordner beginnt ganz oben, die Eingabezeile steht bündig über der Liste, die Abstände sind durchgehend kleiner.
- **Umbenennen ohne Dialog.** Ein Klick auf eine bereits ausgewählte Liste, F2 oder das Kontextmenü öffnen ein Eingabefeld an Ort und Stelle.
- **Symbole für Eingang, Ansichten, Papierkorb und die Schaltflächen** – alle an einer Stelle im Quelltext hinterlegt.
- **Aufgeräumte Liste.** Long-Task und Überschrift stehen nicht mehr in der Labelspalte, ein Symbol markiert Labels, und Labels wie Hinweiszeile weichen gemeinsam, sobald das Fenster schmal wird.

Version 2.12 brachte:

- **Eine ruhigere Oberfläche.** Die Eingabemaske verliert den dauerhaft aufgeklappten Kalender und die Chipfläche für Labels: Labels sind ein Aufklappfeld mit Mehrfachauswahl, die Fälligkeit ein Datumsfeld mit Kalenderknopf.
- **Ein Kopfbereich, der nicht springt.** Die Labels einer Liste stehen rechts unter der Fortschrittszeile und halten ihre Zeilenhöhe auch dann, wenn eine Liste keine Labels hat.
- **Mehr Platz für die Liste.** Such- und Filterzeile stehen über der Aufgabenliste statt über die volle Breite; die Übersicht der Listen und Ordner beginnt eine Zeile weiter oben. „Nur erledigte Punkte“ ist entfallen.
- **Ein vollständig lesbares Fälligkeitsdatum.** Die Uhrzeit brach vorher ab. Die Spaltenbreite wird jetzt mit der Schrift der Liste gemessen, das Jahr steht dort zweistellig.

Davor 2.11:

- **Absicherung gegen Datenverlust.** Ein gelöschter Punkt geht in den Papierkorb – mit Unterpunkten, Anhängen und seiner Herkunft – statt sofort und endgültig zu verschwinden. Viele Umbauaktionen laufen unter einem Bestandswächter, der vor und nach der Aktion alle Punkte zählt und bei einer Lücke den vorherigen Stand herstellt.
- **Strg+Klick wählt wieder mehrfach aus.** Der Zusatz war an das Kontextmenü gebunden und blockierte unter Windows und Linux die Mehrfachauswahl vollständig. Unter macOS übernimmt Cmd+Klick.
- **Eine Maske für Anlegen und Bearbeiten.** Beide Fenster waren unterschiedlich mächtig; jetzt bieten sie denselben Umfang – Art, Wichtigkeit, Farbe, Fälligkeit, Labels, Beschreibung und Anhänge.
- **Kalender und optionale Uhrzeit.** Der Monatskalender ist überall erreichbar, wo eine Fälligkeit gesetzt wird – seit 2.12 als eigenes Fenster hinter dem Kalenderknopf. Ein Punkt hat keine Fälligkeit, nur ein Datum oder Datum und Uhrzeit.
- **Erweiterte Eingabe neben der Schnelleingabe.** Tippen und Enter bleibt der kürzeste Weg; „Erweitert“ öffnet dieselbe vollständige Maske und übernimmt, was schon im Feld steht.

Davor: 2.10 Labels als Chips und verlustfreier TXT-Rundlauf; 2.9 verschachtelte
Ordner, das Long-Task-Detailfenster und Bildlaufleisten; 2.8 die vier
Aufgabenarten, „Verspätet“ und den vollständigen Anlage-Dialog.

Das Datenformat steht seit 2.11.0 auf 10 und ist seitdem unverändert. Bestände und Komplettbackups der Formate 4 bis 10 sind lesbar; die Ergänzungen von damals (`due_time`, Papierkorbart `item`) waren additiv.

Projektbegleitende QA-Renderläufe liegen außerhalb des Repository-Bereichs unter `50_Ablage/QA/`; das produktive Repository bleibt davon getrennt.

## Starten

```powershell
pythonw src/glide/app.pyw
```

Benötigt wird Python 3 mit Tk/Tcl. Die Kernanwendung nutzt nur die Python-Standardbibliothek.

## Testen

```powershell
python tests/integration/test_glide.py
python tests/integration/test_datenintegritaet.py
python tests/integration/audit_app.py
```

`test_glide.py` prüft Funktionen und Datenformate, `test_datenintegritaet.py` die
Zusage, dass keine Umbauaktion einen Punkt verliert, und `audit_app.py` die Wege
durch die App: jede Ansicht, jedes Kontextmenü, jede Verschiebeoperation, jede
Tastenbindung, simuliertes Drag & Drop und den Aufbau jedes Dialogs.

Daneben liegen unter `tests/tools/` Werkzeuge für Prüfung und Arbeitsdaten,
unter anderem: `screenshots.py` für die Sichtprüfung in hell und
dunkel, `analyse_statisch.py` und `analyse_erreichbarkeit.py` für die
Codeanalyse, `beispieldaten.py` für den mitgelieferten Beispielbestand.

Der Test isoliert den App-Datenordner über die Umgebungsvariable `GLIDE_DATA_DIR` und verändert keine echten Glide-Nutzdaten. Dieselbe Variable eignet sich für manuelle Probeläufe mit Testbeständen:

```powershell
$env:GLIDE_DATA_DIR = "C:\Temp\glide-test"; pythonw src\glide\app.pyw
```

## Nutzdaten

- Windows: `%APPDATA%\Glide\`
- macOS: `~/Library/Application Support/Glide/`
- Linux: `$XDG_DATA_HOME/Glide/` beziehungsweise `~/.local/share/Glide/`
- Überschreibbar: `GLIDE_DATA_DIR`

Portable Sicherungen verwenden die Endung `.glidebackup`. TXT, Markdown und CSV sind Austauschformate; nur `.glidebackup` enthält auch die Binärdateien der Anhänge.

## Testdaten

- Kleine, versionierte Fixtures für den Integrationstest:
  `tests/fixtures/current_v10/` bis `current_v4/` sowie `legacy_v2/`. Alle acht
  laufen bei jedem Testlauf durch die aktuelle Normalisierung und sichern, dass
  ältere Sicherungen lesbar bleiben.
- Ausführlicher Beispielbestand zum Einlesen:
  `tests/fixtures/beispiele/Glide_Beispieldaten.glidebackup`, erzeugt von
  `tests/tools/beispieldaten.py`. In Glide über „Datei → Komplettbackup laden …“.
  **Ein Komplettbackup ersetzt den vorhandenen Bestand** – Glide sichert vorher
  automatisch, aber wer eigene Listen führt, macht besser selbst ein Backup.
- Derselbe Bestand liegt außerhalb des Repositorys unter
  `05_Probelisten_Testdaten/` für manuelle Prüfungen.

Die vollständige Einbindung aller Änderungswege in Rahmen und Bestandswächter
ist noch offen, unter anderem bei `add_child_item`, `apply_sidebar_rename`
und dem Ein-/Ausrücken. Siehe Bestandsanalyse.

## Dokumentation und Release-Arbeitslisten

Aktueller Einstieg: [Dokumentationsindex](docs/00_INDEX.md),
[Bestandsanalyse](docs/11_BESTANDSANALYSE.md),
[QA-Bericht](docs/07_QA_BERICHT.md) und [Testaufrufe](tests/README.md).
Die [Word-Arbeitsgrundlage](<../../10_Dokumentation/3.2.0 – Glide_Arbeitsvorbereitung_Codex_Build_Release_Plan.docx>)
führt den bisherigen Plan mit seiner Gliederung auf Stand 3.2.0 fort.

Eine [gemeinsame Backupdatei](tests/fixtures/beispiele/glide_releaseplanung_3.3.0.glidebackup)
enthält drei editierbare Arbeitslisten: Unterlagen & Assets, Vermarktungsstrategie
und Feature-Übersicht. Quelle und Recherchezeitpunkt stehen in den Beschreibungen.
**Der Import ersetzt den gesamten Bestand**; zuerst eine isolierte Testablage
verwenden oder eigene Daten vollständig sichern.

## Noch offen vor einer öffentlichen Veröffentlichung

Publisher, Lizenzmodell, Supportkontakt, Bundle-/Installer-IDs, Signing, Notarisierung, Branding-Master, reproduzierbare Builds und Clean-Machine-Tests sind noch festzulegen beziehungsweise umzusetzen. Der technisch bereits belegte Teil steht in `docs/decisions/PRODUCT_IDENTITY.md`; die Abnahmeliste in `docs/10_RELEASE_CHECKLIST.md`.
