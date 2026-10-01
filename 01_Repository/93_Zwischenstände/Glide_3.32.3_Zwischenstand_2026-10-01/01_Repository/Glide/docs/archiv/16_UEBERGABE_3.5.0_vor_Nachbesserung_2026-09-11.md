# Übergabe Glide 3.5.0

Stand: 05.09.2026 · App-Version 3.5.0 · **Aufgabendatenformat 11** ·
Einstellungsformat 1

Dieses Dokument beschreibt den Stand nach zwei Arbeitsrunden auf Basis von
3.4.0: einem Oberflächen-Nachtrag innerhalb von 3.4.0 und dem Release 3.5.0 mit
wiederkehrenden Aufgaben. Es nennt, was umgesetzt ist, was offen bleibt und welche Aufräumarbeiten und Windows-Prüfungen
am selben Tag abgeschlossen wurden.

Ältere Übergaben bleiben als Referenz gültig, soweit sie nicht widersprochen
werden: [Projektübergabe](09_PROJECT_HANDOFF.md),
[Oberfläche 3.4.0](13_OBERFLAECHE_3.4.0.md),
[Nachtrag zu 3.4.0](14_OBERFLAECHE_NACHTRAG_3.4.0.md),
[Wiederholungen 3.5.0](15_WIEDERHOLUNGEN_3.5.0.md).

---

## 1. Aufräumarbeiten und Windows-Prüfung abgeschlossen

Am 05.09.2026 wurden die benannten Dublettenordner und der Löschmerker entfernt.
Die Release-Fixtures 3.2.0, 3.3.0 und 3.4.0 liegen vollständig im Fixture-Archiv;
im aktuellen Beispielordner bleiben zwei Backups mit Datenformat 11.
Der Beispielname wurde auf `Glide_Beispieldaten.glidebackup` vereinheitlicht.

Vor der Entfernung wurde ein vollständiges, per Datei geprüftes Sicherungsarchiv
unter `50_Ablage/Archiv/Glide_3.5.0_vor_Bereinigung_2026-09-05.zip` angelegt.
Eine nicht identische Startseitenvorfassung bleibt zusätzlich unter
`50_Ablage/Screenshots/3.5.0/archiv/startseite_vorfassung_dunkel.png` erhalten.
Die ursprüngliche Löschliste steht in der archivierten Fassung dieses Dokuments.

Die Releaseplanung wurde inhaltlich gegengelesen und korrigiert: Wiederholungen,
Labelchips und aktuelle Textsymbole gehören zum Produkt. Die erste
Store-Paketversion bleibt eine Entscheidung bei Buildfreigabe; 3.5.0 benennt
den internen Planungsstand. Der korrigierte Erzeuger und das neu erzeugte Backup
stimmen im Windows-Vollmodus überein.

Der Windows-Abschluss besteht mit Exitcode 0. Zusätzlich sind die Symbolausgabe,
14 Zustände der Wiederholungsmaske bei 760 × 700 Pixeln und Windows-Bildnachweise
vorhanden. **Schriftbefund:** Die in vielen Widgets verwendeten
`TkDefaultFont`-Tupelangaben ergeben hier Arial und für geometrische Symbole
teilweise MS Gothic. Die benannte Tk-Standardschrift selbst ist Segoe UI.
Daraus wurde keine ungeprüfte Symboländerung abgeleitet.

Details und verbleibende manuelle Prüfungen: [QA-Bericht](07_QA_BERICHT.md).
Die ältere startbare Einzeldatei 3.4.0 bleibt erhalten; 3.5.0 ist bytegleich
mit dem unveränderten App-Quellcode. Die äußeren Arbeitsordner verweisen nun auf
den aktuellen Prüfstand und enthalten auch die aktuellen Beispielbackups.

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

**Windows-Vollmodus: Exitcode 0**, Python 3.12.7 und Tcl/Tk 8.6.13.
Alle fünf Suiten, beide Analysen, Syntax, Versionen, Dokumentverweise,
Fixtures und beide Daten-Reproduktionen bestehen.
Protokoll: `tests/qa-3.5.0/abschluss/ergebnis.json`.
Windows-Bilder: `50_Ablage/Screenshots/3.5.0/windows-abschluss/`.
Die früheren Linux-Logs bleiben unter `tests/qa-3.5.0/linux-vorpruefung/`.

Die Zusatzprüfung der Wiederholungsmaske umfasst sieben Auswahlen in beiden
Themes bei 760 × 700 Pixeln. Reale Mausbedienung über längere Zeit, weitere
DPI-/Mehrmonitor-Konfigurationen, macOS/Linux als Zielplattformen und Uhrwechsel
bleiben offen. Vollständige Details im [QA-Bericht](07_QA_BERICHT.md).

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
