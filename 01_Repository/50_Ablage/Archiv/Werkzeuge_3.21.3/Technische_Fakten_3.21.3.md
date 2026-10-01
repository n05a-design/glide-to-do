# Technische Fakten – Glide 3.21.3

Stand: 14.09.2026 · Glide 3.21.3 · interner Entwicklungsstand · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2

3.21.3 ändert **keinen Anwendungscode** außer der Versionsangabe. Es ist ein
Dokumentations- und Prüfstandsstand: Der Prüfstand prüft die Dokumentation
jetzt auch inhaltlich, und die Befunde, die diese Prüfung gefunden hätte, sind
behoben.

## Warum eine eigene Version

3.21.2 ist mit Exitcode 0 abgenommen (macOS, Python 3.14.5, 14.09.2026, 15:04,
36 von 38 Schritten). Der Beleg `tests/qa-3.21.2/abschluss/ergebnis.json` gilt
für **den damals mitgelieferten Prüfstand**. 3.21.3 erweitert `pruefen.py` um
eine dritte Analyse und ändert einen Erzeuger; damit deckt der alte Beleg den
neuen Umfang nicht mehr. Deshalb ein eigener Stand mit eigenem Prüflauf.

## Der Befund: sieben Dokumente, zwei Versionssprünge

| Dokument | stand auf | richtig wäre |
| --- | --- | --- |
| `01_Repository/Glide/README.md` | 3.21.0 | 3.21.2 |
| `docs/00_INDEX.md` (Zeile 3) | 3.21.0 | 3.21.2 |
| `docs/11_BESTANDSANALYSE.md` | 3.21.0 | – (historisch) |
| `docs/12_ABSCHLUSSBERICHT.md` | 3.21.0 | – (historisch) |
| `docs/25_FEATURE_ABGLEICH_3.7.0.md` | 3.21.0 | – (historisch) |
| `10_Dokumentation/README.md` | 3.21.0 | 3.21.2 |
| `40_Store_Material/Produktdatenblatt_3.21.2.md` (Titel) | 3.21.0 | 3.21.2 |

Dazu drei weitere Banner auf **3.14.0** in `08_CODE_BEFUND`,
`28_ABLAGEPRUEFUNG` und `30_DOKUMENTATIONSABGLEICH` – sieben Versionen alt.

Zwei Ursachen, beide strukturell:

1. **Die Fortschreibung arbeitete mit einer Tokenliste.** Sie kannte
   `Glide 3.21.1 ·`, `**3.21.1**`, `v3.21.1.pyw` und ein Dutzend weitere
   Schreibweisen. `Aktueller interner Entwicklungsstand: **3.21.0**` war nicht
   darunter, also blieb die Zeile stehen – bei jedem Stand erneut.
2. **Nichts prüfte die Aussage.** `dokumentation_pruefen` in `pruefen.py`
   verlangt einen Indexeintrag und erreichbare Linkziele. Ein Dokument kann
   beides erfüllen und dennoch inhaltlich überholt sein. Der Prüfstand war grün.

Ein von Hand gepflegtes Banner „Aktueller Entwicklungsstand: …" in einem
historischen Dokument rottet zwangsläufig: Es muss bei jedem Stand angefasst
werden, obwohl das Dokument selbst abgeschlossen ist.

## `tests/tools/standpruefung.py`

Neue dritte Analyse, hinter `analyse_statisch` und `analyse_erreichbarkeit` in
`ANALYSEN`. Ohne Tk, Laufzeit unter einer Sekunde, nur Standardbibliothek, keine
Schreibzugriffe. Läuft gegen die ganze Ablage, wenn das Repository darin liegt,
sonst nur gegen das Repository (und sagt das im Ergebnis).

Grundlage ist die Unterscheidung:

* **festgeschrieben** – Version oder Datum im Dateinamen, Versionsordner im Pfad
  (`tests/qa-3.6.0/…`, `Screenshots/3.5.0/…`) oder „historisch" im Titel. Solche
  Dokumente beschreiben einen abgeschlossenen Stand.
* **fortgeschrieben** – alles andere. Muss den aktuellen Stand nennen.

| Regel | Inhalt |
| --- | --- |
| R1 | Ein fortgeschriebenes Dokument trägt mindestens eine Standzeile mit der Version aus `VERSION`. Das erzwingt Datum und Version an derselben Stelle. |
| R2 | Nennt eine Standzeile eine andere Version, muss dieselbe Zeile auch die aktuelle nennen. Herkunft bleibt erlaubt, eine allein stehende überholte Angabe nicht. |
| R3 | **Kein** Dokument behauptet einen aktuellen Stand mit fremder Version. Diese Regel trifft die gerotteten Banner. |
| R4 | Trägt der Dateiname eine Version, nennt keine Standzeile eine andere als diese oder die aktuelle. |
| R5 | Der Titel eines versionsbenannten Dokuments nennt keine ältere Version als der Dateiname. |

Zwei Vorfilter machen die Prüfung brauchbar:

* **Fremde Versionsangaben** fallen weg: `Python 3.14.5`, `Tk 8.6`,
  `Aufgabenformat 15`, `Einstellungen 2`, Datumsangaben. Ohne diesen Filter
  meldet die Prüfung die Python-Version im QA-Bericht.
* **Zitate und Codespannen** fallen weg (`„…"`, `` `…` ``). Der Änderungsverlauf
  zitiert die gerotteten Banner wörtlich; ohne diesen Filter meldete die Prüfung
  genau den Satz, der den Fehler dokumentiert. Dieselbe Falle hat in 3.21.2 ein
  Tokendurchgang gestellt, der ein historisches Zitat auf die neue Version hob.

Zwei ausdrückliche Listen bleiben nötig, jede mit Begründung im Quelltext:
`GEPFLEGT` (Weitergabe und Funktionsvorschläge tragen ein Datum im Namen, sind
aber die je eine aktive Fassung) und `FESTGESCHRIEBEN` (der Reiterentwurf
`32_REITERANSICHT.md`). Eine neue Datei, die in keine Kategorie passt, lässt die
Prüfung fehlschlagen – das ist beabsichtigt: Sie erzwingt eine Entscheidung,
statt still durchzulaufen.

## Was die Prüfung erzwungen hat

* **Sechs Standzeilen ohne Version.** `01_PRODUCT_CONSTRAINTS`, `02_ARCHITECTURE`,
  `03_STARTKONTEXT`, `05_QA_TESTPLAN`, `06_DATA_BACKUP_MIGRATION` und
  `10_RELEASE_CHECKLIST` sagten „Stand 13.09.2026 · Aufgabenformat 15" – ohne
  Versionsnummer. Ein externer Agent konnte nicht erkennen, welchen Stand sie
  beschreiben, und die Fortschreibung hatte keinen Anker. Jetzt tragen alle die
  kanonische Zeile `Stand <Datum> · Glide <Version> · …`.
* **Sechs Banner entfernt.** Historische Dokumente verweisen ohne Nummer auf
  Index und QA-Bericht. Dieselbe Behandlung erhielten vier Prosastellen
  („Der aktuelle kumulative Stand ist Glide 3.13.0", „Der aktuelle Bestand ist
  Glide 3.21.0", „Der aktuelle Arbeitsstand ist Glide 3.13.0", „Der aktuelle
  Ausbau bis 3.14").
* **Versionen aus Linktexten.** Im Index stand „QA-Bericht 3.21.0", während der
  Bericht bei 3.21.2 lag; ebenso bei Daten/Backups, Projektübergabe und
  Release-Checkliste. Zeigt ein Linktext auf ein fortgeschriebenes Dokument,
  gehört keine Nummer hinein.

## `09_PROJECT_HANDOFF.md`

Das Dokument behauptete an **drei** Stellen gleichzeitig, 3.15, 3.16 und 3.21
seien „das zuletzt umgesetzte Funktionspaket", und nannte als „nächste offene
Ideen" den dauerhaften Änderungsverlauf, den CSV-Import und benutzerdefinierte
Felder – die ersten zwei seit 3.19 beziehungsweise 3.18 umgesetzt. Für einen
externen Agenten ist das die irreführendste Stelle der ganzen Ablage: Sie
beschreibt den Einstiegspunkt in die Technik.

Neu geordnet: eine Aussage zum aktuellen Funktionspaket, die Vorgänger als
Bestandsabschnitte mit gleichbleibendem Wortlaut („3.16 brachte …"), eigene
Abschnitte für 3.21.1 bis 3.21.3 und eine Ideenzeile, die nur Offenes nennt.

## Lückenhafte Funktionsübersichten

Gemessen gegen den Funktionsbestand des Produktdatenblatts:

| Dokument | fehlende Funktionen |
| --- | --- |
| `01_Repository/Glide/README.md` | 12 |
| `docs/09_PROJECT_HANDOFF.md` | 5 |
| `README.md` (Wurzel) | 4 – Anhänge, Hell/Dunkel, Papierkorb, Punktarten |
| `Glide_Weitergabe_neuer_Chat` | 2 – Hell/Dunkel, Papierkorb |
| `05_Probelisten_Testdaten/README.md` | 2 – Darstellung, Papierkorb |
| `Produktdatenblatt` | 1 – Schnellerfassung |

Der Repository-README trug außerdem einen Aufmacher „Neu in 3.15" – sechs
Funktionen später. Alle sechs Dokumente führen jetzt denselben Satz über die
durchgehende Grundlage. Ein Wortlaut an einer Stelle gepflegt und übernommen ist
besser als sechs eigenständig gepflegte Listen mit sechs Ständen.

## Stille Fehlfarbe im Beispielbestand

`tests/tools/beispieldaten.py` legte die Liste „Kalender, Erinnerungen und
Tagesplanung" mit `color="due_soon"` an. `due_soon` steht **nicht** in
`LIST_COLOR_KEYS`; die App verwirft eine unbekannte Farbe still
(`raw.get("color") if raw.get("color") in cls.LIST_COLOR_KEYS else None`). Die
Liste hatte damit seit 3.21.2 keine Farbe, während Changelog und Notizen sie
behaupteten.

Der Fixture-Abgleich kann das nicht finden – die Neuerzeugung verwirft denselben
Wert genauso. Behoben: Die Liste trägt `"import"` (Braun), und der `Builder`
prüft jede Farbe gegen `LIST_COLOR_KEYS` und bricht bei einem unbekannten Wert
ab. Alle sieben Palettenfarben sind weiterhin im Bestand vertreten; „Ablage &
Ideen" bleibt die absichtlich farblose Liste.

## Archivierung: zwei echte Lücken

* **`07_Python-Versionen`** enthielt **neun** überholte startbare Fassungen
  (3.14.0 bis 3.21.2) aktiv neben der aktuellen, während `Archiv/` nur bis
  3.13.0 reichte: Seit 3.14 hatte niemand nachgezogen, obwohl der Ordner-README
  „Aktuelle startbare Python-Fassung" heißt. Sie liegen jetzt im Archiv, und der
  README sagt das auch.
* **`Claude outputs`** enthielt drei Übertragungspakete (3.19.0-Quellstand,
  3.21.0-Quellstand, 3.21.1-Ablagepaket), vollständig in der Ablage aufgegangen.
  Aus 3.21.2 offen, jetzt nach `50_Ablage/Archiv/Uebertragungspakete`
  verschoben.

Absichtlich **nicht** archiviert: die **neunzehn** versionierten
Releaseplanungen in `tests/fixtures/beispiele`. Die Fixtureprüfung erwartet bei
versioniertem Dateinamen genau dessen Version und belegt damit jede Formatstufe.
Das steht jetzt in `tests/fixtures/README.md`, damit der nächste Durchgang sie
nicht aufräumt.

## Releaseerzeuger: die letzten vier Literale

`tests/tools/releasedaten.py` trug noch vier Versionsangaben als Literal: in der
Bestandsmemo („Funktionsbestand Glide 3.21.2 / Format 15"), im Verweis auf den
maßgeblichen Prüflauf, im Ordnernamen „Releaseplanung 3.21.2" und in der
Listennotiz. Genau diese Art von Angabe stand bis 3.21.1 sieben Versionen lang
falsch im Releasebestand. Alle vier sind an `APP_VERSION` und
`DATA_SCHEMA_VERSION` gebunden.

## Ausgelieferte statt geflickte Testberichte

`tests/README.md` und `tests/fixtures/README.md` gehen seit 3.21.3 über den
SHA-256-Abgleich von `ablegen_3213.py` statt über Fortschreibungsregeln. Beide
waren überholt: Der Testbericht sprach von „achtzehn Suiten" und „zwei Analysen"
bei tatsächlich 25 Suiten, der Fixture-Bericht verwies auf
`glide_releaseplanung_3.14.0.glidebackup` und nannte Releaseplanungen „bis 3.13"
als historisch. Eine Datei, die als Ganzes ausgeliefert wird, kann nicht
teilweise überholt sein.

## Geänderte Dateien

| Datei | Änderung |
| --- | --- |
| `tests/tools/standpruefung.py` | neu: Standprüfung mit fünf Regeln |
| `tests/tools/pruefen.py` | `standpruefung.py` in `ANALYSEN`; Vollprüflauf 38 → 39 Schritte |
| `tests/tools/beispieldaten.py` | Farbe `due_soon` → `import`; Farbprüfung im `Builder` |
| `tests/tools/releasedaten.py` | vier Literale an `APP_VERSION`/`DATA_SCHEMA_VERSION` gebunden |
| `tests/README.md`, `tests/fixtures/README.md` | neu gefasst, jetzt mit dem Quellstand ausgeliefert |
| `src/glide/app.pyw`, `VERSION`, `test_glide.py`, `test_glide_36.py` | nur Versionsangabe |
| `tests/fixtures/beispiele/*`, `resources/templates/*` | neu erzeugt |
| `docs/*`, Wurzel- und Ordner-READMEs, Weitergabe, Produktdatenblatt | Standzeilen, Banner, Funktionslisten |
| `07_Python-Versionen`, `Claude outputs` | neun Fassungen und drei Pakete archiviert |

## Prüfstand

Alle **25 Suiten** und die **drei Analysen** mit Exitcode 0 in der
Linux-Vorabumgebung (Python 3.12.3, Tk 8.6 unter Xvfb, `TZ=Europe/Berlin`).
Beispiel- und Releaseabgleich gegen eine unabhängige Zweiterzeugung: gleich.
Fixtureprüfung: 20 Backups und alle historischen Referenzformate. Ausgenommen
blieb dort allein der Dokumentationsindex, weil die Dokumente in der
Arbeitskopie nicht mitliegen. Der maßgebliche macOS-Lauf steht aus:
`python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.21.3/abschluss`.

## Wissensstand für andere Agenten

Die vollständige Übergabe liegt in
`00_Arbeitsvorbereitung/Glide_Weitergabe_neuer_Chat_2026-09-11.md`. Verbindlich
für Änderungen sind zusätzlich `AGENTS.md` im Repository und
`docs/09_PROJECT_HANDOFF.md`. Vier Dinge, die man ohne sie falsch macht:

1. **Tests niemals ohne temporären `GLIDE_DATA_DIR`.** Jeder App-Import ohne
   diese Isolierung arbeitet auf dem echten Nutzerdatenordner.
2. **Prüfläufe nicht in UTC.** Der Prüfstand setzt `TZ=Europe/Berlin`, wenn
   keine Zone vorgegeben ist. In UTC ist jeder Zeitzonenfehler unsichtbar.
3. **Die Version steht in genau einer Zeile je Dokument.** Historische
   Dokumente nennen sie überhaupt nicht, sondern verweisen auf Index und
   QA-Bericht. `standpruefung.py` prüft das.
4. **Ein Abgleich gegen die eigene Neuerzeugung findet keinen Textfehler.**
   Fixture und Neuerzeugung tragen denselben überholten Text. Standangaben und
   Farben deshalb an Konstanten binden und gegen die App prüfen.
