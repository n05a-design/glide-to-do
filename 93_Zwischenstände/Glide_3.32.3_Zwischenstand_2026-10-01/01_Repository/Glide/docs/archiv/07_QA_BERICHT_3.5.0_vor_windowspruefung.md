# QA-Bericht 3.5.0

Stand: 05.09.2026 · App-Version 3.5.0 · Datenformat 11

Die Fassung 3.4.0 dieses Berichts steht unter
`docs/archiv/07_QA_BERICHT_3.4.0_vor_3.5.0.md`.

## Prüfstand 3.5.0 – Wiederkehrende Aufgaben

Alle fünf Suiten, beide Analysen sowie Syntax-, Versions- und Fixture-Prüfung
liefen mit Exitcode 0 und isoliertem `GLIDE_DATA_DIR`.

Neu geprüft:

- die Rechenregel jeder Wiederholungsart, einschließlich der Monatsreihe ab dem
  31. eines Monats über einen Februar hinweg;
- das Vorrücken beim Abhaken, das Rückgängigmachen und das Ende einer Reihe;
- das Verwerfen unvollständiger Regeln (Abstand 0, leere Wochentage, unbekannte
  Art);
- der Klartextweg für den TXT-Export und -Import;
- die neue Referenzdatei `tests/fixtures/current_v11/reference_v11.json` neben
  dem unveränderten Format-10-Bestand;
- Beispiel- und Releasedaten wurden für Format 11 neu erzeugt.

**Die Läufe fanden unter Linux mit Python 3.12.3 und Tcl/Tk 8.6 statt.** Der
Windows-Prüflauf ist die maßgebliche Abnahme und steht noch aus:

```
Set-Location -LiteralPath 'C:\Users\Timvo\OneDrive\Glide ToDo\01_Repository\Glide'
& 'C:\Python312\python.exe' tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.5.0/abschluss
```

Unter Windows besonders anzusehen: die erweiterte Eingabemaske mit ein- und
ausgeblendeten Zusatzfeldern bei kleiner Fensterhöhe, und ob `↻` dort aus
derselben Schrift kommt wie die übrigen Symbole
(`tests/tools/symbolpruefung.py`).

Nicht geprüft und bewusst offen: ein Wechsel der Zeitzone oder der Systemuhr
während einer laufenden Reihe. Gerechnet wird mit dem lokalen Datum. Ältere
Glide-Versionen lesen ein Format-11-Backup nicht; für den Austausch ist der
TXT-Export der Weg.


## Prüfstand des Oberflächen-Nachtrags

Der Nachtrag wurde in zwei Schritten geprüft. Beide Male liefen alle fünf
Suiten (`test_glide`, `test_datenintegritaet`, `audit_app`, `test_dialog_theme`,
`test_ui_updates`), beide Analysen sowie Syntax-, Versions- und Fixture-Prüfung
mit Exitcode 0 und isoliertem `GLIDE_DATA_DIR`.

Der zweite Schritt betrifft die neu aufgebaute Startseite. Zusätzlich zu den
Suiten wurden Startseite und Einstellungen in beiden Themes aufgenommen und
angesehen, ebenso das Wochendiagramm mit gesetzten Testwerten und die
Übersichten mit eingefärbten Listen.

**Beide Läufe fanden unter Linux mit Python 3.12.3 und Tcl/Tk 8.6 statt.** Der
Windows-Prüflauf ist die maßgebliche Abnahme und steht noch aus.

Unter Windows besonders anzusehen:

- die Fälligkeitsspalte – die neue Reserve wirkt dort stärker, weil `▦` aus
  einer breiteren Ersatzschrift gezeichnet wird;
- die Symbole `▣` und `▲` neben `▼`, `◐` und `◈` in Segoe UI. Welche Zeichen
  dort tatsächlich aus einer Ersatzschrift kommen, beantwortet
  `tests/tools/symbolpruefung.py` auf dem jeweiligen Rechner;
- die analoge Uhr bei anderer Anzeigeskalierung;
- der Hover der Startseitenverweise, den Tk je Plattform unterschiedlich zeichnet.

Nicht geprüft und bewusst offen: Die Tageszahlen der Herausforderung beginnen
mit dieser Fassung bei null – es gibt keine rückwirkenden Daten. Import,
Rückgängig und das Wiederherstellen aus dem Papierkorb verändern die Tageszahl
nicht; das ist Absicht und keine Lücke.


Geändert wurden ausschließlich Oberflächenteile: zwei Symbole in `ICONS`,
die Kacheln und Abstände der Startseite, wechselnde Begrüßungen und die
Breitenberechnung der Fälligkeitsspalte. Datenformat, Migration, Speicherung
und Nutzerdaten sind unberührt.

Gelaufen sind alle fünf Suiten (`test_glide`, `test_datenintegritaet`,
`audit_app`, `test_dialog_theme`, `test_ui_updates`), beide Analysen sowie
Syntax-, Versions- und Fixture-Prüfung – jeweils mit Exitcode 0 und isoliertem
`GLIDE_DATA_DIR`. Zusätzlich wurden Startseite und Liste in beiden Themes
als Bild aufgenommen und angesehen.

**Diese Läufe fanden unter Linux mit Python 3.12.3 und Tcl/Tk 8.6 statt.**
Der Windows-Prüflauf mit `C:/Python312/python.exe` steht noch aus und ist die
maßgebliche Abnahme:

```
Set-Location -LiteralPath 'C:\Users\Timvo\OneDrive\Glide ToDo\01_Repository\Glide'
& 'C:\Python312\python.exe' tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.4.0/nachtrag
```

Besonders unter Windows nachzusehen ist die Fälligkeitsspalte: Die neue Reserve
wirkt dort stärker, weil `▦` aus einer breiteren Ersatzschrift gezeichnet wird.
Ebenfalls unter Windows zu beurteilen sind die beiden neuen Symbole `▣` und `▲`
in Segoe UI – Größe und Strichstärke im Vergleich zu `▼`, `◐` und `◈`.

## Prüfstand 3.4.0 (Erstabnahme)

## Aktueller Windows-Prüflauf

Prüflaufzeit: vorhandenes `C:/Python312/python.exe`, Python 3.12.7 und Tcl/Tk 8.6.13.
Alle App-Imports verwenden **vorher** ein isoliertes `GLIDE_DATA_DIR`.
Die echten Nutzdaten wurden nicht geladen oder verändert.

Die fünf Suiten sind `test_glide`, `test_datenintegritaet`, `audit_app`,
`test_dialog_theme` und `test_ui_updates`. Zusätzlich prüft der gemeinsame
Vollmodus Syntax, Versionskonsistenz, Dokumentverweise, Fixtures, zwei Analysen,
Beispieldaten-Reproduktion und Releasedaten-Reproduktion.

Das vollständige maschinenlesbare Ergebnis liegt unter
`tests/qa-3.4.0/abschluss/ergebnis.json`; es ist der maßgebliche Prüfnachweis.
**Ergebnis: Exitcode 0.** Alle fünf Suiten, beide Analysen, Syntax, Versionen,
Dokumentverweise, Fixtures und beide Daten-Reproduktionen waren erfolgreich.
Nach dem Entfernen einmaliger Arbeitshelfer wurden Syntax, Versionen und
Dokumentverweise erneut erfolgreich geprüft (12 aktuelle Python-Dateien).
Die startbare Einzeldatei 3.4.0 ist per SHA-256 bytegleich mit dem geprüften Source.
Der Ausgangslauf unter `tests/qa-baseline-3.3.0-native` dokumentiert bereits
vor den Änderungen vorhandene Probleme: zwei fehlende Archivverweise, eine
historische Release-Backupdatei mit älterer Erzeugerversion und einen
datumsabhängigen Test mit inzwischen ebenfalls überfälligen Alt-Testpunkten.
Die Versionsprüfung unterscheidet jetzt ausdrücklich versionierte historische
Release-Fixtures. Der Datumstest bilanziert seine eigenen zusätzlichen
Punkte gegen den vorherigen Bestand. Keine dieser Anpassungen ändert Nutzdaten.

## Gezielte neue Prüfungen

- 24 Pixel Abstand vor Metadaten und identische rechte Zählerkanten bei
  1280, 980 und 860 Pixel Fensterbreite in Hell/Dunkel.
- Farbige Menüeinträge und ausgewählte Felder für Farben und alle Wichtigkeiten.
- Feste Labels wechseln Punktart und Form; Zeilenumbrüche, weitere Labels,
  Datum und Uhrzeit bleiben beim Hin- und Herwechsel erhalten.
- Auswahl-/Hoverfläche nur hinter dem unveränderten Labelchip.
- Hilfe mit zwei Spalten und fetten Tasten, Scrollbarkeit und Größenänderung;
  alle Antwortwerte der Rückfragen und Griff-Rückgabe an den Elterndialog.
- Persönliche Einstellungen mit Erst-Sicherung, Bestandszahlen statt Gliederung,
  heute fällige Listen, tatsächliche Änderungen statt bloßer Navigation,
  neue Vorlagen-IDs und Rückgängig sowie Neustart mit Begrüßung/Monogramm/Startseite.
- Alte und neue TXT-Marker für Gruppen und Wichtigkeit.

## Sichtnachweise und Grenzen

`tests/qa-3.4.0/screenshots` enthält 16 Bilder aus eigenen Windows-Testfenstern:
Liste breit/schmal, Startseite, Eingabe, Einstellungen, Tastenkürzel, Über Glide
und Rückfrage, jeweils in Hell/Dunkel. Erzeuger:
`test_ui_updates.py --screenshots tests/qa-3.4.0/screenshots`.

Die 16 Windows-Renderings wurden angesehen; Form, Felder, Texte und Aktionen
sind in den geprüften Größen lesbar bzw. über die Bildlaufleiste erreichbar.
Die unteren Formularaktionen bleiben fest sichtbar. Die Sichtprüfung ersetzt keine
Bedienung mit realer Maus, keine mehrstündige Stabilitätsprüfung und keine
weitere DPI-/Mehrmonitor-Matrix. macOS/Linux sind für 3.4.0 noch ungeprüft.
Native Dateiauswahldialoge können das Betriebssystem-Theme verwenden.
Das Textlogo ist ein Monogramm, kein importiertes Bild. Bestandszahlen sind
keine Nutzungszeitmessung. Persönliche Einstellungen reisen nicht im
Aufgaben-Komplettbackup mit. Es entstand kein signierter Installer.

## Historische Nachweise

# QA-Bericht 3.3.0

Stand: 04.09.2026 · App-Version 3.3.0 · Datenformat 10

## Nachweis 3.3.0

Umgebung: Linux mit Xvfb, Python 3.12.3, Tk 8.6.14. Ausgeführt wurde
`tests/tools/pruefen.py --modus schnell`: Syntax, Versionskonsistenz,
Dokumentabgleich (65 Verweise), Fixtures, alle drei Suiten und beide Analysen –
sämtlich erfolgreich. Die Sichtprüfung erzeugte zwölf Aufnahmen, darunter zwei
neue der Labelansicht in Hell und Dunkel; sie wurden angesehen.

Geprüft wurden zusätzlich gezielt: Aufbau der Labelgruppen, Mehrfachvorkommen
eines Punkts mit zwei Labels, Farbgebung der Gruppen- und Punktzeilen, der
Labeltausch per Zug in beide Richtungen einschließlich „Ohne Label“, das
Zurücknehmen des Zugs sowie die neuen Spaltenbreiten und die Chipgeometrie.

**Nicht geprüft:** Windows und macOS. Der neue Stand ist dort weder automatisiert
noch manuell gelaufen. Offen sind insbesondere das Ziehen zwischen Labelgruppen
mit realer Maus, die gemessenen Spaltenbreiten unter Segoe UI beziehungsweise
SF Pro, die Chipdarstellung bei anderer Anzeigeskalierung und das gemeldete
Einfrieren bei verschachtelten Dialogen.

## Nachweis 3.2.0 (Windows)

Die Bestandsanalyse wurde auf Windows mit Python 3.12.12 und Tcl/Tk 8.6.17
ausgeführt. Alle App-Imports und Prüfungen nutzen isolierte Testdaten. Die
gebündelte Python-3.12.14-Laufzeit konnte Tcl nicht initialisieren; verwendet
wurde die vorhandene, funktionierende Python/Tk-Installation von Inkscape.
Das ist eine Prüf-Laufzeit und keine neue Produktabhängigkeit.

| Prüfung | Ausgangslauf | Nach Korrektur |
|---|---|---|
| Integration `test_glide.py` | Abbruch: veraltetes Attribut `system_box` | bestanden |
| Datenintegrität `test_datenintegritaet.py` | Abbruch: leere Zeilengeometrie vor Windows-Mapping | bestanden |
| App-Durchlauf `audit_app.py` | keine Befunde | keine Befunde |
| Syntax/Version | App 3.2.0, Schema 10 | unverändert; zentraler Prüfablauf prüft mit |
| Statische Analyse | 0 nie genannte Funktionen/Konstanten | keine Quelländerung |
| Erreichbarkeit | 508/520, 0 gleiche Methodenstrukturen | Kandidaten sind keine bewiesenen toten Funktionen |

Logs liegen im äußeren Workspace unter
`50_Ablage/QA/Bestandsanalyse_3.2.0/`; der abschließende Gesamtlauf wird dort
gesondert festgehalten: `abschluss/ergebnis.json`, Vollmodus, Exitcode 0.
Syntax, Versionen, Index, alle drei Suiten, beide Analysen und die semantische
Reproduktion beider Backupdateien sind erfolgreich. Die Release-Arbeitsdaten werden zusätzlich über den
Backup-Prüf- und Normalisierungspfad im Integrationstest kontrolliert.

## Gezielte Testkorrekturen

1. Der nur unter Windows laufende Layouttest verwies auf `system_box`, das
   seit dem Wegfall des Systemrahmens nicht mehr existiert. Er prüft jetzt
   Reihenfolge und Abstand des realen `system_listbox` und ausdrücklich das
   Fehlen des alten Rahmens.
2. Windows meldet für den Kopfblock 43 Pixel und für den festen Themenschalter
   42 Pixel angeforderte Höhe. Der Vergleich erlaubt höchstens einen Pixel
   native Schriftmetrik-Differenz. Die Höhe der Labelzeile mit/ohne Labels wird
   weiterhin **exakt gleich** verlangt. Das ist keine Behauptung pixelgleicher
   Bedienelemente; die Darstellung ist zusätzlich visuell zu prüfen.
3. Der Datenintegritätstest verarbeitet nach dem Aufbau einmal die
   Windows-Fensterereignisse mit `root.update()`, bevor er Drag-Koordinaten
   ausliest. Alle Bestands- und Strukturassertionen bleiben unverändert.

Der produktive App-Quelltext und die gleichlautende externe `.pyw` blieben
bytegleich. App-SHA-256:
`6309f2669f5490777d342138e9fe304b27a4e728404d0359952e3cd4bfc01715`.

## Codebefunde und Grenzen

- 14.591 Textzeilen, 539 Funktionen/Methoden, 133 Konstanten, 25 Funktionen
  über 80 Zeilen, 102 wörtlich doppelte Blöcke; `insert_tree_items` hat
  146 Zeilen und neun Verschachtelungsebenen. Zeilenangaben folgen dem
  aktuellen Analysewerkzeug, nicht dem gerundeten Übergabetext.
- 18 breite `except Exception` im aktuellen Code; die ältere Prüfung von 20
  Stellen ist historisch. Es wurde keine pauschale erneute Bereinigung gemacht.
- Die frühere Aussage „0 Emoji im Quelltext“ war falsch: Gruppenmarker 📁,
  Wichtigkeit hoch 🚩 und Beschreibungsmarker 📝 (an zwei Stellen) sind noch
  vorhanden. Die Tabellenprüfung von `ICONS` erfasst sie nicht.
- `run_modal` ist der einzige `wait_window`-Pfad. Weitere Grabs dienen
  Dropdowns, der kontrollierten Übergabe an native Dialoge und der Rückgabe.
- Das zu 3.0.1 gemeldete Einfrieren wurde nicht reproduziert. Der in 3.1.0
  zentralisierte Grab-Lebenszyklus adressiert einen plausiblen Mechanismus;
  die Behebung der ursprünglichen Meldung bleibt **NICHT VERIFIZIERT**.

Einzelfunde mit Fundstelle, Maßnahme und nächstem Test stehen in
`11_BESTANDSANALYSE.md`. Es wurden weder der Monolith aufgeteilt noch Symbole
ersetzt oder Datenformate geändert.

## Sichtprüfung und historische Nachweise

Die zwölf vorhandenen Linux-Aufnahmen unter
`50_Ablage/Screenshots/3.2.0/` sind historische Nachweise der früheren Runde.
Sie sind keine Windows-/macOS- oder Store-Abnahme. Die neuen Release-Arbeitsdaten
wurden gesondert in Windows eingelesen und als Sichtnachweis aufgenommen.
Die finalen Bilder `abschluss/screenshots/release_hell.png` und
`abschluss/screenshots/release_hell_dunkel.png` im genannten QA-Ordner wurden
beide angesehen: Kopfbereich einschließlich der zwei Listenlabels ohne
Überlappung; dunkles Theme grau, alle drei Arbeitslisten sichtbar. Der
Unterschied 43/42 Pixel im angeforderten Kopfmaß bleibt als Messtoleranz
dokumentiert und verursachte hier keinen sichtbaren Überlauf.

Die früheren ausführlichen QA-Berichte sind in `archiv/` erhalten. Die
behaupteten Zufallsläufe aus 2.11.0 wurden nicht wiederholt; das zugehörige
Werkzeug fehlt. Der behauptete Verlust einer „Phase 11“ lässt sich ohne
Git-Historie oder Originaldatei nicht belegen. `pyflakes` ist kein aktuelles
Projektgate; es wurde keine zusätzliche Testabhängigkeit installiert.

## Noch manuell zu prüfen

- Windows: mehrere Monitore und DPI-Stufen, echte Strg-/Shift-Auswahl,
  Drag & Drop, Textzeichen, lange Benutzung mit verschachtelten Dialogen.
- macOS: gesamte Plattformmatrix einschließlich Cmd-Auswahl, Cmd+Q,
  nativer Dateidialoge, Darstellung und Dateipfade.
- Wiederherstellung mit Kopien echter Daten und Anhänge; Verhalten großer
  Bestände ist trotz technischer Validierungslimits nicht als performant belegt.
- Installer/App-Bundle, Signatur, Notarisierung, gegebenenfalls Sandbox und
  Store-Import: offen, weil keine fertigen Build-Artefakte vorliegen.

Wiederholbarer Prüfaufruf und Voraussetzungen: `../tests/README.md`.
