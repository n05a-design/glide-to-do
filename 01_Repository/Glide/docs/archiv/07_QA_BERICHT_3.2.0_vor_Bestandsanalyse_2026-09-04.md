# QA-Bericht 3.2.0

Stand: 04.09.2026 · App-Version 3.2.0 · Datenformat 10
Laufzeit der Prüfung: Python 3.12 mit Tk 8.6 unter Linux (Xvfb).

Dieser Bericht hält fest, **was tatsächlich geprüft wurde, mit welchem Ergebnis
und was ungeprüft bleibt**. Er ersetzt keine manuelle Prüfung auf den
Zielplattformen; welche Punkte dort offen sind, steht in Abschnitt 6.

Der Bericht zu 2.11.0 – mit der vollständigen Untersuchung des damals
gemeldeten Datenverlusts – liegt unter `docs/archiv/07_QA_BERICHT_2.11.0.md`.
Abschnitt 4 hier fasst zusammen, was davon weiterhin gilt.

---

## 1 Zusammenfassung

| Prüfung | Umfang | Ergebnis |
|---|---|---|
| Syntaxprüfung | `ast.parse` über den gesamten Quellstand | bestanden |
| Integrationstest | 3 167 Zeilen, Funktionen und Datenformate | bestanden |
| Datenintegritätstest | 601 Zeilen, Bestandswächter, Gruppen, Papierkorb, Maske | bestanden |
| App-weiter Durchlauf | 717 Zeilen, Bedienwege über alle Oberflächen | keine Befunde |
| Statische Analyse | AST über den gesamten Quellstand | 0 nie genannte Funktionen, 0 nie genannte Konstanten |
| Erreichbarkeitsanalyse | vom Programmstart aus | 508 von 520 Methoden erreichbar, 0 strukturgleiche Methodenpaare |
| Sichtprüfung | Hell und Dunkel, zwölf Aufnahmen | bestanden |

Quellstand: 14 590 Zeilen, 539 Funktionen und Methoden, 133 Konstanten. Eine
Klasse für die Anwendung, sechs Widget-Klassen, zwei Hilfsklassen
(`DataIntegrityError`, `ChangeRecord`).

---

## 2 Automatisierte Prüfungen

Aufruf jeweils unter Linux mit `xvfb-run -a python3.12 <datei>`. Alle drei
Testdateien isolieren den Datenordner selbst über `GLIDE_DATA_DIR` und fassen
echte Nutzerdaten nie an.

### 2.1 Integrationstest – `tests/integration/test_glide.py`

Der Umfang aus 2.11.0 gilt unverändert weiter: Datenformate 10 bis 2,
verschachtelte Ordner, alle vier Aufgabenarten, Label-Chips, Persistenz,
Austauschformate, Oberfläche. Die vollständige Aufstellung steht im
archivierten Bericht, Abschnitt 2.1.

Seit 3.1.0 kommen hinzu:

- **Gemeinsamer Änderungsrahmen** – eine wirkungslose Aktion hinterlässt keinen
  Rückgängig-Schritt; eine wirksame behält ihn. `focus="first"` richtet den
  Blick auf den ersten statt den letzten Punkt der Auswahl.
- **Kürzung des Rückgängig-Speichers** – bei vollem Speicher kostet eine
  wirkungslose Aktion nicht mehr den ältesten Schritt (Abschnitt 3.2).
- **Ausrücken über die gemeinsame Methode** `lift_item_to_parent_level`.
- **Griff-Rückgabe nach einem modalen Unterdialog** – der Regressionstest zum
  gemeldeten Einfrieren (Abschnitt 3.1).

Seit 3.2.0:

- **Beispielbestand** `tests/fixtures/beispiele/Glide_Beispieldaten.glidebackup`
  wird auf demselben Weg eingelesen wie ein echter Import (Archivprüfung,
  Schemaprüfung, Normalisierung). Geprüft werden Umfang, Artenverteilung,
  Labelverweise und Palettenabdeckung.
- **Symboltabelle** – jedes Zeichen in `ICONS` muss unterhalb von U+1F000
  liegen. Ein versehentlich eingefügtes Emoji fällt damit im Testlauf auf, nicht
  erst auf einem fremden Rechner.
- **Keine Abbildung alter Labelfarbschlüssel mehr** – was nicht in der Palette
  steht, fällt auf die Vorgabefarbe zurück.

### 2.2 Datenintegritätstest – `tests/integration/test_datenintegritaet.py`

Unverändert gegenüber 2.11.0, unverändert bestanden. Prüft die Zusage, an der
alles hängt: **Eine Umbauaktion darf keinen Punkt verlieren.** Kern sind
130 Kombinationen aus Gruppieren und Auflösen über fünf Listenaufbauten und
alle vier Arten. Die vollständige Tabelle steht im archivierten Bericht,
Abschnitt 2.2.

### 2.3 App-weiter Durchlauf – `tests/integration/audit_app.py`

Prüft nicht einzelne Funktionen, sondern die Wege durch die App: Ordner,
Persistenz, jede Ansicht, jedes Kontextmenü, jede Tastenbindung, Ein- und
Ausrücken, Long-Task-Text, Dialogaufbau, simuliertes Drag & Drop, Label-Chips.
Hält beim ersten Fehler nicht an, sondern meldet gesammelt.

**Abweichung zur Dokumentation von 2.11.0, hier festgehalten:** Jener Bericht
nennt „828 Zeilen, elf Phasen". Der heutige Stand hat **717 Zeilen und keine
Phasenstruktur**. Die längere Fassung ging beim Übergang von 2.11.0 auf 2.12.0
verloren – auf dem Rechner lag danach der ältere Stand. Der Durchlauf ist
lauffähig und meldet keine Befunde; was in der verlorenen elften Phase zusätzlich
geprüft wurde, ist **nicht rekonstruierbar**. Wer den Durchlauf erweitert,
beginnt bei der Abschlussprüfung: Endstand schemakonform, keine Fehlermeldung
aufgetreten.

### 2.4 Statische Analyse und Erreichbarkeit

Zwei Werkzeuge mit unterschiedlichem Ansatz, damit sich ihre Schwächen nicht
decken (`tests/tools/analyse_statisch.py`, `tests/tools/analyse_erreichbarkeit.py`).

| Kennzahl | 3.0.2 | 3.2.0 |
|---|---|---|
| Zeilen | 14 704 | 14 590 |
| Nie genannte Funktionen/Konstanten | 1 | 0 |
| Strukturgleiche Methodenpaare | 3 | 0 |
| Wörtlich doppelte Blöcke (≥ 6 Zeilen) | 111 | 102 |
| Stellen mit `undo_stack.pop()` | 39 | 7 |
| `grab_set` + `wait_window` einzeln | 7 | 1 |
| Funktionen über 80 Zeilen | 26 | 25 |
| Emoji im Quelltext | 5 Stellen | 0 |

**Beide Werkzeuge erzeugen Falsch-Positive.** Sie kennen keine Bindungen, die
Tk zur Laufzeit herstellt, und keine Aufrufe über Zeichenketten. In dieser Runde
wurden `LabelChip.set_colors`, `format_file_size`, `_store_pending_attachments`
und `refresh_scrollbar_state` fälschlich als unerreichbar gemeldet; alle vier
sind in Benutzung und wurden **nicht** entfernt. Jeder Fund ist ein Verdacht,
kein Befund.

### 2.5 Nicht mehr durchgeführt

Die **Zufallsläufe** aus 2.11.0 (rund 7 600 simulierte Bedienschritte in drei
Läufen) wurden in dieser Runde **nicht wiederholt**. Sie lagen als Werkzeug
außerhalb der Testsuite und sind nicht im Repository erhalten. Ihr Befund von
damals gilt für den damaligen Stand; für 3.2.0 ist er `NICHT VERIFIZIERT`.

`pyflakes` wurde in dieser Runde nicht ausgeführt – es ist keine
Projektabhängigkeit und stand in der Prüfumgebung nicht zur Verfügung.

---

## 3 Befunde und Behebungen dieser Runde

### 3.1 Das gemeldete Einfrieren

**Symptom:** Zu 3.0.1 gemeldet – „Die App hängt sich irgendwie bei dieser
Version jetzt auf teilweise."

**Untersucht wurde die Griff-Verwaltung (`grab`).** Ein modaler Dialog nimmt den
Tastatur- und Mausgriff an sich und gibt ihn beim Schließen nicht von allein an
das aufrufende Fenster zurück.

> `grab_set` und `wait_window` standen an **sieben** Stellen einzeln
> nebeneinander. **Eine einzige** davon gab den Griff zurück
> (`themed_due_dialog`, seit 3.0.2).

Wer aus einer Eingabemaske heraus Farbauswahl, Namensabfrage oder Listenauswahl
öffnete, hatte danach eine Maske vor sich, die noch zu sehen war, aber keine
Eingabe mehr annahm – für den Benutzer nicht von einem Absturz zu unterscheiden.

**Behoben in 3.1.0:** `run_modal` ist der einzige Weg, auf dem ein Dialog
wartet. `modal_over` ermittelt den vorherigen Griffhalter notfalls selbst über
`grab_current()`. Ein Regressionstest prüft: Fenster mit Griff, Unterdialog
darüber, nach dessen Ende muss der Griff zurück sein.

**Status: NICHT VERIFIZIERT.** Der Fehler ließ sich in der Prüfumgebung nie
reproduzieren. Die Aussage stützt sich auf den Mechanismus, nicht auf eine
Reproduktion. Ob es die einzige Ursache war, kann nur die Benutzung auf Windows
zeigen.

### 3.2 Wirkungslose Aktion kostete den ältesten Rückgängig-Schritt

**Symptom:** Bei vollem Rückgängig-Speicher (20 Schritte) verlor der Benutzer
den ältesten Schritt – auch dann, wenn die auslösende Aktion nichts bewirkte.

**Ursache:** `snapshot_undo` kürzte den Stapel schon beim Anlegen des
Schnappschusses, bevor feststand, ob er bleibt.

**Behoben in 3.1.0:** `snapshot_undo(trim=False)` in beiden Änderungsrahmen,
`trim_undo_stack()` erst nach bestätigter Wirkung. Der Fehler war seit jeher
vorhanden und wurde erst durch den Test des neuen Rahmens sichtbar.

**Status: behoben und durch Test abgedeckt.**

### 3.3 Strukturelle Absicherung

Seit 3.1.0 läuft jede Änderung an Punkten durch `item_change`, jede an Listen
und Ordnern durch `sidebar_change`. Beide legen den Rückgängig-Punkt an, lassen
die Änderung laufen und schließen ab; ohne gemeldete Wirkung entfällt der
Rückgängig-Punkt. Vorher stand dieselbe Abfolge an 36 Stellen wörtlich im
Quelltext – wer den Rücknahme-Zweig vergaß, hinterließ einen Schritt, der nichts
zurücknimmt. Das kann jetzt nicht mehr passieren.

`item_change` sitzt **innerhalb** von `guarded_structural_change`, nie darum
herum: Der Wächter bilanziert den Bestand über die gesamte Umbauaktion, der
Rahmen kümmert sich um einen einzelnen Rückgängig-Schritt darin.

---

## 4 Was aus 2.11.0 weiter gilt

Der damals gemeldete **Datenverlust** ist behoben. Die Gruppenfunktion war
**nicht** die Ursache; gefunden wurden fünf andere, die zusammen dasselbe Bild
ergaben – allen voran ein `delete_item`, das am Papierkorb vorbeiging. Die
vollständige Aufstellung steht im archivierten Bericht, Abschnitt 3.

Der daraufhin eingeführte **Bestandswächter** ist unverändert aktiv und durch
130 geprüfte Kombinationen abgesichert.

---

## 5 Sichtprüfung

Zwölf Aufnahmen, erzeugt mit `tests/tools/screenshots.py`, abgelegt unter
`50_Ablage/Screenshots/3.2.0/`:

- Hauptfenster hell und dunkel
- Kopfbereich mit und ohne Labels, hell und dunkel
- Punktdetails hell und dunkel
- Aufgeklappte Labelauswahl hell und dunkel
- Kalenderfenster hell und dunkel
- Der Beispielbestand nach dem Import, hell und dunkel

Geprüft: Die Textzeichen aus `ICONS` stehen an ihrer Stelle, das
Fälligkeitssymbol nimmt bei überfälligen Punkten die Warnfarbe an, Abstände und
Ausrichtungen sind gegenüber 3.0.2 unverändert.

**Warum die Sichtprüfung nicht entfallen darf:** In einer früheren Runde
verschwanden Symbole nach einer Fensterbreiten-Änderung, weil
`refresh_sidebar_row_texts` die Texte ohne Symbole neu baute. Der Testlauf war
grün; nur die Sichtprüfung fand es.

---

## 6 Was ungeprüft bleibt

Diese Punkte kann kein Skript in dieser Umgebung beantworten.

| Bereich | Warum ungeprüft |
|---|---|
| Windows-Darstellung | Geprüft wird unter Linux/Tk. Schriftmetrik, DPI-Skalierung, dunkle Titelleiste und native Dateidialoge verhalten sich dort anders. **Neu wichtig:** die Textzeichen `⊕` und `▦` in den echten Systemschriften. |
| macOS-Darstellung | Dasselbe, zusätzlich Cmd-Tastenkürzel, Cmd+Q über die Speicherabfrage und Gatekeeper. Unter macOS bleibt Strg+Klick das Kontextmenü und Cmd+Klick wird die Mehrfachauswahl – auf einem echten Mac zu bestätigen. |
| Das gemeldete Einfrieren | Nie reproduziert. Nur längere Benutzung auf Windows kann bestätigen, dass die behobene Ursache die einzige war. |
| Reale Nutzerdaten | Der Test arbeitet mit erzeugten Beständen. Eine Migration mit einer Kopie des echten Datenordners steht aus. |
| Echte Eingabegeräte | Drag & Drop wird simuliert, nicht mit Maus oder Trackpad ausgeführt. |
| Große Bestände | Geprüft wurden bis rund 200 Aufgaben. Verhalten bei mehreren Tausend ist nicht gemessen. |
| Installation und Signatur | Es gibt noch kein Build-Artefakt (siehe `10_RELEASE_CHECKLIST.md`). |
| Zufallsläufe | Siehe 2.5 – für 3.2.0 nicht wiederholt. |

---

## 7 Prüfung wiederholen

Unter Linux:

```
xvfb-run -a python3.12 tests/integration/test_glide.py
xvfb-run -a python3.12 tests/integration/test_datenintegritaet.py
xvfb-run -a python3.12 tests/integration/audit_app.py
python3.12 tests/tools/analyse_statisch.py
python3.12 tests/tools/analyse_erreichbarkeit.py
xvfb-run -a --server-args="-screen 0 1400x1100x24" python3.12 tests/tools/screenshots.py --out /tmp/shots
```

Unter Windows:

```powershell
$env:GLIDE_DATA_DIR = "$env:TEMP\Glide-Test"
python tests\integration\test_glide.py
python tests\integration\test_datenintegritaet.py
python tests\integration\audit_app.py
```

Alle drei Testdateien isolieren den Datenordner selbst; die Variable oben ist
nur eine zusätzliche Sicherung. Ein Lauf dauert zusammen unter drei Minuten.
Die Sichtprüfung braucht ImageMagick (`import`) und ist unter Windows und macOS
nicht vorgesehen – dort wird von Hand geprüft.
