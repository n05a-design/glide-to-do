# Technische Fakten – Glide 3.21.4

Stand: 15.09.2026 · Glide 3.21.4 · interner Entwicklungsstand · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2

3.21.4 ändert **keinen Anwendungscode** außer der Versionsangabe. Es ist ein
Korrekturstand aus einem vollständigen Durchgang durch alle 93 aktiven
Dokumente der Ablage.

## Warum eine eigene Version

3.21.3 ist mit Exitcode 0 abgenommen (macOS, Python 3.14.5, 14.09.2026, 20:45,
siebenunddreißig von neununddreißig Schritten). Dieser Stand ändert zwei
Dateien, die über den SHA-256-Abgleich gehen (`tests/tools/README.md`,
`src/glide/README.md`), erweitert `standpruefung.py` um drei Regeln und
korrigiert 27 Dokumente. Der 3.21.3-Beleg deckt diesen Umfang nicht.

## Was der Durchgang gefunden hat

Die Standprüfung aus 3.21.3 prüft, ob ein Dokument den **richtigen Stand**
nennt. Sie kann nicht prüfen, ob es die **Wahrheit** über das Verhalten sagt.
Genau dort lagen die Befunde.

### Zehn aufgeführte falsche Aussagen über den Anwendungscode

Jede gegen `src/glide/app.pyw` in 3.21.3 geprüft, nicht gegen ein Abbild.

| Dokument | Behauptung | Befund im Code |
| --- | --- | --- |
| `43_AENDERUNGSVERLAUF_3.19.0` | `glide_liste.json` erhält `history` | `SAVE_FILE = "liste_speicher.json"`; der Name `glide_liste` existiert nirgends |
| `43_AENDERUNGSVERLAUF_3.19.0` | „Wer 400 Zeilen importiert … Sammeleintrag (412 Punkte)" | zwei Zahlen für dieselbe Menge |
| `45_KALENDERIMPORT_3.21.0` | „Zeilen-, Größen- und Terminobergrenze" | nur `MAX_ICS_IMPORT_EVENTS` (2000) und `MAX_ICS_IMPORT_BYTES` (12 MB); keine Zeilengrenze |
| `45_KALENDERIMPORT_3.21.0` | „erledigte beziehungsweise abgesagte Termine überspringen" | `skip_cancelled` prüft nur `STATUS:CANCELLED`; ein `VEVENT` hat keinen Erledigt-Zustand, `VTODO` ist ausgeschlossen |
| `45_KALENDERIMPORT_3.21.0` | „die vier übernehmbaren Termine der RRULE-Tabelle" | es gibt keine RRULE-Tabelle; gemeint sind vier `FREQ`-Werte, aus denen mit `INTERVAL` und `BYDAY` sechs Glide-Arten entstehen |
| `44_KALENDERAUSGABE_3.20.0` | „Ohne Fälligkeit gibt es keinen Termin" | `build_ics_document` ruft `ics_event_lines(…, "planned", …)` für **jeden** Punkt; ein Bearbeitungstag erzeugt auch ohne Fälligkeit einen Planungstermin |
| `44_KALENDERAUSGABE_3.20.0` | „Punkte ohne Fälligkeit erscheinen nicht" | dieselbe Stelle |
| `44_KALENDERAUSGABE_3.20.0` | `BYDAY=MO,DI…` | `ICS_WEEKDAYS = ("MO","TU","WE","TH","FR","SA","SU")`; `DI` ist kein zulässiges Token |
| `44_KALENDERAUSGABE_3.20.0` | „weil `UID` und `SEQUENCE` … neue Fassung" | `"SEQUENCE:0"` steht als Literal in der Ausgabe und steigt nie |
| `41_DRUCK_UND_PDF_3.17.0` | „beginnt bei der mitgelieferten DejaVu Sans" | Schriften werden nur prozesslokal registriert (`FR_PRIVATE`, CoreText-Prozessumfang); die Druckdatei enthält ausdrücklich keine Web-Schrift |

Die beiden Kalenderbefunde sind die schwersten: Sie beschreiben Verhalten
falsch, das man nur mit einem Kalenderprogramm nachprüfen kann. Wer sich auf
den Vertrag verlässt, sucht den Planungstermin nicht, den Glide erzeugt – und
erwartet eine Aktualisierung, die Glide einem Kalender nicht anzeigt.

### Fünf überholte Formatstufen

`SECURITY.md` („Formate 4 bis 12"), `06_DATA_BACKUP_MIGRATION.md` („Formate
4–14"), `decisions/PRODUCT_IDENTITY.md` (App-Version 3.14.0, Datenformat 13,
Backup-Formate 4 bis 13, Format-13-Fixture), `src/glide/README.md`
(„Datenformat 13") und `27_VORLAGEN_PRAXISANLEITUNG.md` („Format 14 und
benötigen Glide ab 3.14"). Lesbar sind **4 bis 15**.

`PRODUCT_IDENTITY.md` ordnete zusätzlich die lokalen Erinnerungen dem Format 14
zu. Sie kamen mit **Format 13** in 3.8.0; Format 14 brachte 3.14 mit
Bearbeitungstag und Aufwand. Derselbe Versatz stand an zwei weiteren Stellen
desselben Dokuments.

### Acht falsche Verweise

Vier Linktexte „Produktdatenblatt" zeigten auf `40_Store_Material/README.md`
statt auf das Datenblatt. Zwei Linktexte „Aktuelle Funktionsübersicht" zeigten
auf die Vorschlagsliste `Glide_Funktionsvorschlaege_2026-09-11.md` – eine Liste
von Ideen, nicht von Funktionen. Der Probelisten-README verwies für
Tabellenansicht, „Mein Tag", Schnellerfassung, Filter, Reiter und Pinnwände auf
den 3.9-Vertrag; keine dieser Funktionen steht dort. Und
`30_Release_Exports/README.md` bot den 3.13-Vertrag als „Bedienung und
Änderungen" des aktuellen Stands an.

### Sieben Gegenwartsbehauptungen in historischen Dokumenten

Die Banner aus 3.21.3 sind weg, aber in der Prosa standen weiter Sätze im
Präsens: „Dieses Dokument beschreibt den aktuellen lokalen Python-/Tk-Quellstand"
(`08_CODE_BEFUND`), „liegen inzwischen die aktuellen Aufgabenbackups"
(`28_ABLAGEPRUEFUNG`), „verweisen inzwischen auf den 3.13-macOS-Gesamtlauf"
(`30_DOKUMENTATIONSABGLEICH`), „für 3.14.0 steht der bestätigende Gesamtlauf
noch aus" (`25_FEATURE_ABGLEICH`; der Lauf bestand am 13.09.2026), „Nächste
Schritte: … Reiteransicht und Pinnwand" (`12_ABSCHLUSSBERICHT`; seit 3.10.0
umgesetzt), „2. Reiteransicht angehen" (`decisions/SYSTEMBENACHRICHTIGUNGEN`)
und drei Stellen in `50_Ablage/QA/Dokumentation/README.md`.

Diese Klasse lässt sich schwer maschinell fassen: Die Sätze nennen keine
Version, also greift keine Regel der Standprüfung. Was hilft, ist die
Formulierungsregel – ein abgeschlossener Nachweis schreibt im Präteritum.

### Zwei Widersprüche zwischen Dokumenten

`50_Ablage/README.md` nannte `10_Dokumentation` die „aktuelle
Word-Arbeitsgrundlage", während der Ordner-README dort die Word-Berichte als
archiviert und die Markdown-Dokumente als aktuelle Quelle führt. Und dieselbe
Datei verlangte, von den Renderläufen nur den letzten zu behalten, während der
Renderlauf-README festhält, dass keiner gelöscht wurde. Beide aufgelöst.

### Vier eigene Zählfehler aus 3.21.3

| Angabe | stand auf | richtig |
| --- | --- | --- |
| versionierte Releaseplanungen | neunzehn | **zwanzig** (mit 3.21.4: einundzwanzig) |
| archivierte startbare Fassungen | neun | **zehn** (3.14.0 bis 3.21.2) |
| Dokumente mit dem Grundlagensatz | sechs | **vier**; Produktdatenblatt und Probelisten-README führen eigene Tabellen |
| Farbkorrektur im Änderungsverlauf | fehlte | nachgetragen |

Die Zahl neun kam daher, dass ich bei der Zählung 3.21.2 noch als aktuelle
Fassung geführt habe – mit dem Sprung auf 3.21.3 wanderte auch sie ins Archiv.

## Neu: Regeln R6 bis R8 der Standprüfung

Drei der fünf Formatbefunde wären mechanisch zu finden gewesen, denn die
Formatstufe steht im Code. `tests/tools/standpruefung.py` liest jetzt
`DATA_SCHEMA_VERSION` und `MIN_PORTABLE_BACKUP_SCHEMA_VERSION` über den
Syntaxbaum aus `app.pyw` – ein Import würde Tk starten und den echten
Nutzerdatenordner anfassen – und prüft:

| Regel | Inhalt |
| --- | --- |
| R6 | Eine Formatstufe in einer Standangabe entspricht `DATA_SCHEMA_VERSION` |
| R7 | Ein Formatbereich reicht von `MIN_PORTABLE_BACKUP_SCHEMA_VERSION` bis `DATA_SCHEMA_VERSION` |
| R8 | Eine Tabellenzeile „Datenformat", „… Backup-Formate" oder „App-Version" nennt die aktuellen Werte |

Der Änderungsverlauf ist von der Formatprüfung ausgenommen (`NUR_GESCHICHTE`):
Dort war „Formate 2 bis 9" damals richtig – dieselbe Überlegung wie beim
Zitatschutz. Gegenprobe bestanden: Eine Testdatei mit „Aufgabenformat 14",
„Formate 4 bis 12", „| Datenformat | 13 |" und „| App-Version | 3.14.0 |" wird
mit vier Befunden und Exitcode 1 gemeldet.

## Prüfergebnis in derselben Version

Bis 3.21.2 stand das Ergebnis eines Prüflaufs immer erst in den Dokumenten der
**nächsten** Version. Folge: Jeder Stand behauptete, sein eigener Prüflauf stehe
noch aus – auch Monate später. Seit 3.21.4 ist der Eintrag Schritt 8 des
Ablagewegs in der Weitergabe. Der 3.21.3-Lauf ist im aktuellen QA-Bericht und in der Weitergabe nachgetragen.
Die archivierten Technischen Fakten zu 3.21.3 behalten ihren ursprünglichen
Wortlaut; der abgeschlossene Prüflauf ist separat erhalten.

## Ausgelieferte statt geflickte Repository-READMEs

`tests/tools/README.md` und `src/glide/README.md` gehen jetzt über den
SHA-256-Abgleich von `ablegen_3214.py`, wie die beiden Testberichte seit
3.21.3. Beide trugen Angaben, die bei jedem Stand hätten mitgehen müssen:
„Achtzehn Suiten" bei tatsächlich 25, „Demonstrationsbestand Format 14", „Drei
Release-Arbeitslisten für 3.14", „`--stichtag 2026-09-13`", ein
„Windows-Nachweis: Python 3.12.7" ohne Datum und Stand, und eine Funktionsliste,
die bei 3.13 endete. Die Werkzeugtabelle nennt jetzt auch `standpruefung.py`
und `vorlagendaten.py`; die Zwecke sind bewusst ohne Versions- und
Formatzahlen formuliert.

## Geänderte Dateien

| Datei | Änderung |
| --- | --- |
| `tests/tools/standpruefung.py` | Regeln R6 bis R8, Konstanten aus `app.pyw` über den Syntaxbaum, `NUR_GESCHICHTE` |
| `tests/tools/README.md`, `src/glide/README.md` | neu gefasst, jetzt mit dem Quellstand ausgeliefert |
| `tests/README.md`, `tests/fixtures/README.md` | Version, Protokollpfad, Zahl der Releaseplanungen |
| `SECURITY.md`, `docs/06_DATA_BACKUP_MIGRATION.md`, `docs/decisions/PRODUCT_IDENTITY.md`, `docs/27_VORLAGEN_PRAXISANLEITUNG.md` | Formatstufen |
| `docs/41`, `docs/43`, `docs/44`, `docs/45` | zehn aufgeführte Aussagen über den Anwendungscode |
| `docs/08`, `docs/12`, `docs/25`, `docs/28`, `docs/30`, `docs/decisions/SYSTEMBENACHRICHTIGUNGEN`, `50_Ablage/QA/Dokumentation/README` | Gegenwart in historischen Dokumenten |
| `docs/09_PROJECT_HANDOFF.md`, `docs/07_QA_BERICHT.md`, Weitergabe | 3.21.3-Ergebnis und 3.21.4-Abschnitt |
| `CHANGELOG.md` | vier Zahlen im 3.21.3-Eintrag, fehlende Farbkorrektur, neuer Eintrag |
| Ordner-READMEs, Store-Angaben, Produktdatenblatt, Probelisten-README | Verweise, Widersprüche, Startseite, Formatpaar |
| `src/glide/app.pyw`, `VERSION`, `test_glide.py`, `test_glide_36.py`, `releasedaten.py` | nur Versionsangabe |
| `tests/fixtures/beispiele/*`, `resources/templates/*` | neu erzeugt |

## Prüfstand

Der vollständige Abschlusslauf zu **3.21.4** bestand am **15.09.2026 um 10:23** auf macOS mit Python 3.14.5 und `TZ=Europe/Berlin`: **Exitcode 0**, **39 Schritte, davon 37 ausgeführt**. Alle **25 Testsuiten**, drei Analysen, Vorprüfungen sowie Beispiel- und Releaseabgleiche bestanden. Übersprungen blieben ausschließlich die plattformgebundene Screenshot-Erzeugung und die manuelle Sichtprüfung.

[Prüfprotokoll](../../50_Ablage/QA/qa-3.21.4/abschluss/ergebnis.json).

Die Ablageprüfung korrigierte außerdem eine fehlende Wortgrenze in Regel R6: `Vorlagenformat 2` und `Einstellungsformat 2` dürfen nicht als Aufgabenformat gelesen werden. Positive und negative Gegenproben bestanden. Das Original des Prüfwerkzeugs liegt im lokalen Archiv; der Anwendungscode bleibt bis auf die Versionsnummer unverändert.

## Wissensstand für andere Agenten

Die vollständige Übergabe liegt in
`00_Arbeitsvorbereitung/Glide_Weitergabe_neuer_Chat_2026-09-11.md`. Verbindlich
für Änderungen sind zusätzlich `AGENTS.md` im Repository und
`docs/09_PROJECT_HANDOFF.md`. Fünf Dinge, die man ohne sie falsch macht:

1. **Tests niemals ohne temporären `GLIDE_DATA_DIR`.** Jeder App-Import ohne
   diese Isolierung arbeitet auf dem echten Nutzerdatenordner.
2. **Prüfläufe nicht in UTC.** Der Prüfstand setzt `TZ=Europe/Berlin`, wenn
   keine Zone vorgegeben ist. In UTC ist jeder Zeitzonenfehler unsichtbar.
3. **Die Version steht in genau einer Zeile je Dokument**, die Formatstufe
   kommt aus dem Code. `standpruefung.py` prüft beides.
4. **Ein historisches Dokument schreibt im Präteritum.** Ein Satz im Präsens
   nennt keine Version und entgeht damit jeder maschinellen Prüfung.
5. **Ein Abgleich gegen die eigene Neuerzeugung findet keinen Textfehler und
   keine stille Fehlfarbe.** Standangaben, Formate und Farben an Konstanten
   binden und gegen die App prüfen.
