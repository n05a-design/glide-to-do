# Übergabe Glide 3.5.0

Stand: 05.09.2026 · App-Version 3.5.0 · **Aufgabendatenformat 11** ·
Einstellungsformat 1

Dieses Dokument beschreibt den Stand nach zwei Arbeitsrunden auf Basis von
3.4.0: einem Oberflächen-Nachtrag innerhalb von 3.4.0 und dem Release 3.5.0 mit
wiederkehrenden Aufgaben. Es nennt, was umgesetzt ist, was offen bleibt und was
von Hand aufzuräumen ist.

Ältere Übergaben bleiben als Referenz gültig, soweit sie nicht widersprochen
werden: [Projektübergabe](09_PROJECT_HANDOFF.md),
[Oberfläche 3.4.0](13_OBERFLAECHE_3.4.0.md),
[Nachtrag zu 3.4.0](14_OBERFLAECHE_NACHTRAG_3.4.0.md),
[Wiederholungen 3.5.0](15_WIEDERHOLUNGEN_3.5.0.md).

---

## 1. Was von Hand aufzuräumen ist

Diese Punkte lassen sich nicht aus der Ferne erledigen, weil auf dem Rechner nur
geschrieben, nicht gelöscht oder umbenannt werden kann. **Solange sie offen
sind, meldet der Prüflauf einen Fehler.**

### Zwei überholte Release-Fixtures löschen

Im Ordner `tests/fixtures/beispiele/` liegen zwei Sicherungen im alten
Datenformat 10. Die Fixture-Prüfung verlangt, dass jede Datei außerhalb von
`archiv/` das aktuelle Format trägt:

- `glide_releaseplanung_3.4.0.glidebackup` – Archivkopie liegt bereits unter
  `tests/fixtures/archiv/`; die Datei im aktuellen Ordner kann weg.
- `glide_releaseplanung_3.3.0.glidebackup` – vorher nach
  `tests/fixtures/archiv/` kopieren, dann im aktuellen Ordner entfernen.

Nach der Workspace-Regel genügt das Präfix `XX_`, wenn nicht sofort gelöscht
werden soll.

### Eine Dublette im Fixture-Ordner

`tests/fixtures/beispiele/` enthält `glide_beispieldaten.glidebackup` und
`Glide_Beispieldaten.glidebackup`. Unter Windows ist das dieselbe Datei;
auf einem case-sensitiven Dateisystem wären es zwei. Der Erzeuger schreibt
`Glide_Beispieldaten.glidebackup`, die Testsuite liest denselben Namen. Sollte
tatsächlich eine zweite Datei existieren, gehört die kleingeschriebene weg.

### Release-Planungstexte gegenlesen

`tests/tools/releasedaten.py` enthält handgeschriebene Release-Planungsinhalte –
Features, Blocker, Store-Texte. Ein Wächter in `build()` erzwingt, dass sie bei
jedem Versionssprung geprüft werden. Beim Sprung auf 3.5.0 wurden sie mechanisch
fortgeschrieben (Version, Datenformat, Ordnertitel) und um ein Feature für die
Wiederholungen ergänzt. Blocker und offene Punkte blieben unverändert.

**Nachzulesen ist besonders der Satz** „Interne App-Version bleibt 3.5.0, auch
wenn es die erste Store-Einreichung ist." Das ist eine inhaltliche Aussage zur
Store-Einreichung und keine mechanische Ersetzung.

### Windows-Prüflauf nachholen

Alle Prüfungen liefen bislang nur unter Linux. Die maßgebliche Abnahme:

```
Set-Location -LiteralPath '%USERPROFILE%\OneDrive\Glide ToDo\01_Repository\Glide'
& 'C:\Python312\python.exe' tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.5.0/abschluss
```

### Symbolbefund erheben

Offene Rückfrage: `tests/tools/symbolpruefung.py` auf dem Windows-Rechner
ausführen und die Ausgabe bereitstellen. Erst danach lässt sich entscheiden, ob
Symbole getauscht oder eine eigene Symbolschrift festgelegt wird. Ohne diesen
Befund wäre jede Änderung an der Symbolauswahl geraten.

### Alte Einzeldatei

`07_Python-Versionen/` enthält jetzt `_v3.3.0`, `_v3.4.0` und `_v3.5.0`. Ob
ältere Stände dort bleiben oder ins dortige `Archiv/` wandern, ist eine
Aufräumentscheidung – die Prüfung stört sich nicht daran.

---

## 2. Was umgesetzt wurde

### Nachtrag innerhalb von 3.4.0 – Symbole und Fälligkeitsspalte

- **Symbole vereinheitlicht.** Startseite `▣` statt `⌂`, Verspätet `▲` statt
  `‼`. Beide alten Zeichen fielen aus der Reihe – eine feine Umrisslinie und ein
  Satzzeichen neben gefüllten Formen. Die Ersatzzeichen stammen aus demselben
  Unicode-Block „Geometrische Formen" wie `▼`, `◐`, `◈`, `▦`. Papierkorb,
  Themenschalter und Wichtigkeitsfähnchen bleiben bewusst außerhalb dieser
  Familie – dort trägt keine geometrische Form die Bedeutung.
- **Fälligkeitsspalte.** Datum und Uhrzeit passen jetzt immer vollständig in die
  Zeile. Ursache war eine Messlücke: Tk misst mit der eingestellten Schrift,
  Windows zeichnet `▦` aber aus einer breiteren Ersatzschrift, dazu kommt der
  innere Zellenrand der Treeview. Die Spalte bekommt eine an der Schriftgröße
  bemessene Reserve; sobald irgendwo eine Uhrzeit steht, gilt zusätzlich die
  volle Musterbreite als Untergrenze.
- **Startseitenkacheln** abgerundet, mit gleichen Abständen oben, unten und zur
  Seitenleiste.
- **Begrüßungen** wechseln beim Zurückkehren zur Startseite.

### Nachtrag innerhalb von 3.4.0 – Startseite neu aufgebaut

- **Kopfzeile** mit analoger Uhr (aus Tk-Grundformen gezeichnet), Wochentag und
  Datum, nächstem anstehendem Termin in der Farbe seiner Liste und dem Sprung in
  die Kalenderansicht.
- **Willkommenskachel**: farbiges Textlogo links, Begrüßung rechts, darunter
  eine wechselnde Aufforderung.
- **Textlogo** als farbige Fläche mit derselben Rechnung wie ein Labelchip.
  Farbe wählbar unter **Bearbeiten → Einstellungen**, mit sofortiger Vorschau.
- **Tägliche Herausforderung**: Tagesziel einstellbar, Fortschritt als Balken.
  Gezählt wird zentral in `item_change`, nur der Übergang offen → erledigt.
- **Schnellzugriffe** nebeneinander statt untereinander; jede anklickbare
  Fläche der Startseite hat denselben Hover wie eine Zeile in der Seitenleiste.
- **Reihenfolge**: „Dein aktueller Bestand" ganz unten, mit farbigen Kennzahlen
  (erledigt grün, offen orange, Listen blau), Verweisen auf „In Bearbeitung" und
  „Verspätet" und einem Balkendiagramm der letzten sieben Tage.
- **Zuletzt bearbeitet** zeigt drei statt sechs Einträge.
- **Vorlagen**: zehn statt drei, davon wechseln drei zufällig.
- **Listenfarben** auf der Startseite; in „In Bearbeitung" und „Verspätet" erbt
  ein Punkt ohne eigene Farbe die seiner Liste oder ihres Ordners.
- **Labelnamen** bei der Eingabe auf 14 Zeichen begrenzt (Maßstab „Freigabe
  nötig"); vorhandene längere Namen bleiben unangetastet.

### Release 3.5.0 – Wiederkehrende Aufgaben

- Sechs Arten: täglich, alle N Tage (1–365), an festen Wochentagen, wöchentlich,
  monatlich, jährlich – jede wahlweise mit Enddatum.
- **Beim Abhaken** rückt der Punkt auf seinen nächsten Termin vor und steht
  wieder offen. Es entsteht keine zweite Zeile; was geschafft wurde, hält die
  Tageszahl fest.
- **Monats- und Jahresabstände** rechnen vom Ursprungstermin: 31.01 → 28.02 →
  31.03, nicht dauerhaft auf den 28.
- **Am Reihenende** bleibt der Punkt erledigt und verliert seine Regel.
- **Darstellung** `↻` hinter dem Aufgabentext; Klartext in Suche, TXT-Export
  und -Import.
- **Datenformat 10 → 11**, additive Migration. Ein fehlendes Feld heißt
  „wiederholt sich nicht"; alte Daten werden nicht umgeschrieben. Eine
  unvollständige oder unbekannte Regel wird verworfen statt geraten.
- **Produktgrenzen getrennt**: Wiederholungen sind Bestandteil des Produkts,
  Erinnerungen mit Benachrichtigung und Push-Infrastruktur bleiben
  ausgeschlossen.

---

## 3. Was offen ist

### Zugesagt, aber nicht gebaut

**Vorlagenverwaltung.** Zehn Vorlagen liegen in `LIST_TEMPLATES`, drei
wechselnde stehen auf der Startseite. Offen: exportierte Listen als Vorlage
importieren, Vorlagen gegen versehentliches Bearbeiten schützen und nur über
eine ausdrückliche Aktion „Vorlage bearbeiten" freigeben. Braucht einen eigenen
Vorlagenspeicher – neben `settings.json` oder in den Nutzdaten. Die Entscheidung
steht aus.

**Cloud-Modus.** Datenordner frei wählbar, damit mehrere Rechner über einen
gemeinsamen Cloud-Ordner denselben Bestand sehen. Technisch klein:
`GLIDE_DATA_DIR` steuert den Ordner bereits vollständig, es fehlen eine
Zeigerdatei neben der App und ein Dialog „Datenordner wechseln" samt Umzug der
vorhandenen Daten. Zwei Dinge sind vorher zu klären:

- **Gleichzeitiger Zugriff.** Glide schreibt die ganze Datei atomar; wer zuletzt
  speichert, gewinnt, und ein Cloud-Dienst legt dann stumm eine Konfliktkopie
  an. Vorschlag: eine Sperrdatei, die beim Start vermerkt, welcher Rechner den
  Ordner offen hat – der zweite bekommt eine Warnung statt eines stillen
  Datenverlusts.
- **Abgrenzung zum Nicht-Ziel „Cloud-Synchronisation".** Ein gemeinsamer Ordner
  ist kein Dienst und kein Konto. Das gehört so in
  `docs/01_PRODUCT_CONSTRAINTS.md` geschrieben, wie es bei den Wiederholungen
  gemacht wurde.

### Bewusst zurückgestellt

**Mehrere Farben in einer Zeile.** Eine `ttk.Treeview` färbt immer die ganze
Zeile; Farben pro Zelle oder pro Wort sind mit ihr nicht möglich. Entschieden
wurde „eine Farbe pro Zeile": Ein Punkt ohne eigene Aufgabenfarbe erbt die
seiner Liste oder ihres Ordners. Echte Mehrfarbigkeit erforderte einen Umbau der
Aufgabenliste von der Treeview auf eine eigene Canvas-Liste – mit allem, was
daran hängt: Drag & Drop, Mehrfachauswahl, Tastaturbedienung, Bildlauf. Das
wäre der größte Einzeleingriff im Projekt und sollte nicht nebenbei passieren.

### Nicht geprüft

- **macOS und Linux als Zielplattformen**, weitere Anzeigeskalierungen, mehrere
  Monitore, längere reale Mausbedienung.
- **Zeitzonen- oder Systemuhrwechsel** während einer laufenden Wiederholung.
  Gerechnet wird mit dem lokalen Datum.
- **Native Dateiauswahldialoge** folgen dem Betriebssystem und können vom
  App-Theme abweichen. Das bleibt so.
- **Installer, Signierung und Store-Veröffentlichung** sind unverändert offen.

### Bekannte Grenzen des Bestands

- Die **Tageszahlen** der Herausforderung beginnen mit dem Nachtrag bei null.
  Rückwirkende Daten gibt es nicht. Import, Rückgängig und das Wiederherstellen
  aus dem Papierkorb verändern die Tageszahl nicht – das ist Absicht.
- Die **Historie zuletzt bearbeiteter Listen** beginnt mit 3.4.0.
- **Persönliche Einstellungen** liegen in `settings.json`, sind gerätespezifisch
  und nicht Bestandteil eines Aufgabenbackups. Das gilt auch für Tagesziel,
  Tageszahlen und Logofarbe.
- **Ältere Glide-Versionen lesen ein Format-11-Backup nicht.** Für den Austausch
  mit einem Rechner, der noch 3.4 fährt, ist der TXT-Export der Weg.
- Der Ordner heißt „Repository", enthält aber kein Git-Repository. Es gibt keine
  Commits, Branches oder Git-Sicherungen, auf die man zurückgreifen könnte.

---

## 4. Prüfstand

Alle fünf Suiten (`test_glide`, `test_datenintegritaet`, `audit_app`,
`test_dialog_theme`, `test_ui_updates`), beide Analysen sowie Syntax-,
Versions- und Fixture-Prüfung laufen mit Exitcode 0.

**Sämtliche Läufe fanden unter Linux mit Python 3.12.3 und Tcl/Tk 8.6 statt.**
Protokoll und Bildnachweise dieser Vorprüfung liegen unter
`tests/qa-3.5.0/linux-vorpruefung/`. Beide Ordner tragen eine `LIESMICH.md`, die
die Grenzen der Aussage benennt.

Zwei Testanpassungen waren nötig, beide Verschärfungen:

- Die Messung der Feldkanten in der Eingabemaske berücksichtigt nur noch
  **sichtbare** Felder. Seit die Maske Felder je nach Auswahl ein- und
  ausblendet, lägen nicht gepackte Widgets auf der Position ihres nächsten
  sichtbaren Vorfahren und meldeten einen Abstand, den niemand sieht.
- Die Formularprüfung kennt das neue Feld `repeat` und prüft, dass ohne Auswahl
  keine Wiederholung entsteht.

Neue Prüfungen: jede Wiederholungsart, die Monatsreihe ab dem 31. über einen
Februar, Vorrücken, Rückgängig, Reihenende, das Verwerfen kaputter Regeln, der
TXT-Rückweg und die Referenzdatei `tests/fixtures/current_v11/reference_v11.json`
neben dem unveränderten Format-10-Bestand.

---

## 5. Regeln, die bei Weiterarbeit gelten

- **Symbole** ausschließlich als Textzeichen aus `ICONS`; der Integrationstest
  erzwingt das. Neue Zeichen zuerst aus dem Block „Geometrische Formen" wählen.
- **Änderungen an Punkten** laufen durch `item_change`, an Listen und Ordnern
  durch `sidebar_change`, Umbauten zusätzlich durch
  `guarded_structural_change`. Modale Fenster ausschließlich über `run_modal`.
- **Startseite**: `HOME_EDGE_GAP` trägt denselben Wert wie der Abstand zwischen
  Seitenleiste und Inhalt; wird einer geändert, ist der andere mitzuziehen. Jede
  anklickbare Fläche braucht `<Enter>`/`<Leave>` auf `theme["hover"]` – Tk färbt
  `activebackground` erst beim Drücken.
- **Wiederholungen**: Monats- und Jahresabstände immer vom Anker `start`
  rechnen, nie vom letzten Termin. Beim Umpacken der Maske muss `repeat_block`
  unmittelbar nach `due_block` mitgepackt werden.
- **Dateien im Repository** haben CRLF-Zeilenenden und kein BOM.
- **Überholte Dokumente** werden nicht überschrieben, sondern zuerst in den
  `archiv/`-Unterordner desselben Ordners kopiert, benannt nach der Version, die
  sie beschreiben. Jede `.md` unter `docs/` muss in `00_INDEX.md` verlinkt sein.
- **Tests** setzen `GLIDE_DATA_DIR` vor dem Import der App auf ein isoliertes
  Verzeichnis. Niemals echte Nutzerdaten für Tests, Beispieldatenimporte oder
  Oberflächenaufnahmen verwenden.
- **Ein Versionssprung** zieht mit: `VERSION`, `APP_VERSION` in `app.pyw`, das
  `assert mod.APP_VERSION == …` in `tests/integration/test_glide.py`, die oberste
  `##`-Überschrift im `CHANGELOG.md`, `APP_VERSION` und `DEFAULT_TARGET` in
  `tests/tools/releasedaten.py` samt Planungstexten, die neu zu erzeugenden
  Fixtures `glide_releaseplanung_<Version>.glidebackup` und
  `Glide_Beispieldaten.glidebackup` sowie versionsbenannte Dokumente und ihre
  Verweise in `00_INDEX.md`, `README.md` und `03_STARTKONTEXT.md`.
