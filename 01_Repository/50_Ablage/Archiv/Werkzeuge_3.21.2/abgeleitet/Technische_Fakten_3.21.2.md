# Technische Fakten – Glide 3.21.2

Stand: 14.09.2026 · interner Entwicklungsstand · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2

3.21.2 ändert **keinen Anwendungscode** außer der Versionsangabe. Es ist ein
Daten- und Dokumentationsstand: Der mitgelieferte Beispielbestand deckt die
Funktionen seit 3.14 erstmals testbar ab, überholte Angaben in Erzeugern und
READMEs sind richtiggestellt, und der QA-Bericht trägt das Ergebnis des
abgenommenen 3.21.1-Laufs.

## Warum eine eigene Version

3.21.1 ist mit Exitcode 0 abgenommen (macOS, Python 3.14.5, 14.09.2026, 36
Schritte). Der Beleg `tests/qa-3.21.1/abschluss/ergebnis.json` gilt für **den
damals mitgelieferten Bestand**. Wer die Beispieldaten nachträglich ändert, macht
den Beleg unzutreffend, ohne dass es jemand sieht. Deshalb ein eigener Stand mit
eigenem Prüflauf.

## Beispielbestand: was fehlte und was jetzt drin ist

Gemessen am alten Bestand mit 149 Punkten:

| Merkmal | 3.21.1 | 3.21.2 |
| --- | --- | --- |
| Punkte / Listen | 149 / 11 | 166 / 12 |
| Erinnerungen | **0** | 2 (relativ und fest) |
| Bearbeitungstage | 1 | 7 |
| Aufwandsangaben | 1 | 6 |
| Wiederholungen | 2 von 6 Arten | **alle 6 Arten** |
| davon mit Enddatum | 1 | 2 |
| Fälligkeiten / mit Uhrzeit | 27 / 4 | 35 / 7 |
| Listenanhänge | 1 | 2 |

Dass der Bestand keine Erinnerung enthielt, war nicht nur eine Lücke: Der
Ordner-README behauptete ausdrücklich, Erinnerungen ließen sich „in den
Punktdetails der Beispielaufgaben ausprobieren".

Neu ist die Liste **„Kalender, Erinnerungen und Tagesplanung"** im Ordner
„Website-Betrieb", `color="due_soon"`. Aufbau:

- **Tagesplanung.** Sechs Punkte auf `b.day(0)`, Summe 270 Minuten. Einer ohne
  Schätzung (die Tagesplanung zählt solche getrennt), einer erledigt (bleibt nach
  der Regel aus 3.15 in der Summe). Ein siebter Punkt liegt auf `b.day(1)` mit 120
  Minuten, damit der Tageswechsel etwas zeigt.
- **Erinnerungen.** `{"mode": "relative", "minutes": 30}` an einem Punkt mit
  Uhrzeit; `{"mode": "fixed", "at": app.local_reminder_time(b.day(4), "08:00")}`
  an einem Ganztagstermin. `local_reminder_time` rechnet die Ortszeit in die
  gespeicherte UTC-Form und weist Zeiten in einer ausgelassenen Stunde zurück.
- **Wiederholungen.** `taeglich`, `wochentage` mit `tage: [0, 2]` **und**
  `ende: b.day(140)`, `monatlich`, `jaehrlich`. Zusammen mit `woechentlich` und
  `tage`/`abstand: 14` in „Wartung und Freigaben" sind alle sechs Arten vertreten.
  Die Wochentagsregel mit Enddatum ist genau der Fall, der bis 3.21.0 beim
  ICS-Rundlauf um einen Tag verrutschte.
- **Rundlaufanleitung** als Long-Task, vier Schritte samt Gegentest mit
  ersetzten UIDs. Ein Textanhang an der Liste belegt, dass die Kalenderausgabe
  rein lesend bleibt.

Die Zusicherungen der Suiten an den Beispielbestand sind durchweg **Untergrenzen**
(`>= 120` Punkte, `>= 10` Listen, `>= 10` Long-Tasks, `>= 5` Ordner, `>= 3`
Papierkorbeinträge, jede Art mindestens einmal). Erweitern bricht sie nicht;
keine Suite musste angepasst werden.

## Releaseerzeuger: Standangaben an die Konstanten gebunden

`tests/tools/releasedaten.py` hängte in `code()` an **jeden** Codebeleg den
Zusatz „Stand: 3.14.0 / Datenformat 13" und trug im Kopf eine Memo-Zeile mit
derselben Angabe. Beides stand seit 3.14 unverändert, während die App bei 3.21.1
und Format 15 lag. `DEFAULT_TARGET` zeigte auf
`glide_releaseplanung_3.14.0.glidebackup`.

Der Prüfstand konnte das nicht finden: Der Release-Abgleich vergleicht die
Fixture mit ihrer eigenen Neuerzeugung, und beide trugen denselben überholten
Text. Jetzt speisen `APP_VERSION` und die neue Modulkonstante
`DATA_SCHEMA_VERSION = 15` diese Texte, und dieselbe Konstante speist die schon
vorhandene Zusicherung `app.DATA_SCHEMA_VERSION != DATA_SCHEMA_VERSION` – ein
Wert für Aussage und Prüfung.

## Geänderte Dateien

| Datei | Änderung |
| --- | --- |
| `tests/tools/beispieldaten.py` | neue Liste „Kalender, Erinnerungen und Tagesplanung" mit Erinnerungen, Tagesplanung, allen Wiederholungsarten und Rundlaufanleitung |
| `tests/tools/releasedaten.py` | Standangaben an `APP_VERSION`/`DATA_SCHEMA_VERSION`, neue Modulkonstante, `DEFAULT_TARGET` versionsabhängig, Inhaltstexte auf 3.21.2 |
| `src/glide/app.pyw`, `VERSION`, `test_glide.py`, `test_glide_36.py` | nur Versionsangabe |
| `tests/fixtures/beispiele/*`, `resources/templates/*` | neu erzeugt |
| `05_Probelisten_Testdaten/*` | Nutzerkopien auf 3.21.2, acht überholte Fassungen archiviert, README neu |

## Prüfstand

Alle **25 Suiten** und beide statischen Analysen mit Exitcode 0 in der
Linux-Vorabumgebung (Python 3.12.3, Tk 8.6 unter Xvfb, `TZ=Europe/Berlin`).
Beispiel- und Releaseabgleich wurden gegen eine unabhängige Zweiterzeugung
nachgestellt und fallen gleich aus. Fixtureprüfung: 19 Backups und alle
historischen Referenzformate. Der maßgebliche macOS-Lauf steht aus:
`python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.21.2/abschluss`.

## Wissensstand für andere Agenten

Die vollständige Übergabe liegt in
`00_Arbeitsvorbereitung/Glide_Weitergabe_neuer_Chat_2026-09-11.md`. Verbindlich
für Änderungen sind zusätzlich `AGENTS.md` im Repository und
`docs/09_PROJECT_HANDOFF.md`. Zwei Dinge, die man ohne sie falsch macht:

1. **Tests niemals ohne temporären `GLIDE_DATA_DIR`.** Jeder App-Import ohne
   diese Isolierung arbeitet auf dem echten Nutzerdatenordner.
2. **Prüfläufe nicht in UTC.** Der Prüfstand setzt `TZ=Europe/Berlin`, wenn keine
   Zone vorgegeben ist. In UTC ist jeder Zeitzonenfehler unsichtbar, weil der
   Versatz null ist – so blieb der `UNTIL`-Fehler bis zum macOS-Lauf unentdeckt.
