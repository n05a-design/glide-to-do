# Änderungsverlauf

Vollständig beschrieben sind die sieben neuesten Versionen; ältere stehen verdichtet in der Tabelle am Ende. Ihre ausführlichen Einträge, Verträge und Nachweise trägt Git (Stand vor dem 03.10.2026). Das aktuelle Verhalten beschreiben die [Funktionen](docs/20_FUNKTIONEN.md).

## Richtungsdokument (03.10.2026, App unverändert, kein Versionswechsel)

- **Neu: [Richtung](../../00_Arbeitsvorbereitung/Glide_Richtung.md)** – ein Ort für Leitbild, Gedanken und Vorgaben des Inhabers mit Wortlaut und Datum, die sechs Produktprinzipien mit Prinzipien-Check, Produktgrenzen, das Entscheidungsregister D01–D17 mit früheren Antworten, Markt und Wettbewerb, Wegweisungen, Veröffentlichung und GitHub-Stand sowie die offenen Richtungsfragen mit je einer Empfehlung.
- **Wettbewerb wiederhergestellt:** Die Verdichtung vom Vormittag hatte aus den Konkurrenzdokumenten vom 01.10.2026 Produktsteckbriefe, Belegstufen der Vorlieben, Vergleich nach Dimensionen und berichtigte ältere Bewertungen verloren; sie stehen jetzt, auf 3.33.6 nachgeführt, in der Richtung (Featurematrix mit 46 Zeilen).
- **Zusammengeführt und gelöscht:** `00_Arbeitsvorbereitung/Glide_Markt_und_Vorbilder.md`, `docs/01_PRODUCT_CONSTRAINTS.md` (Grenzen je Funktion jetzt in [Funktionen, Abschnitt 13](docs/20_FUNKTIONEN.md#13-grenzen)), `docs/ARBEITSRICHTUNG.md` (Arbeitsablauf und Nachläufe jetzt in [AGENTS.md](AGENTS.md)). Entwicklungsplan und Übergabe verweisen für Leitbild, „bewusst nicht“ und Inhaberfragen auf die Richtung. [Nachweis](tests/qa-3.33.6/richtung_2026-10-03/README.md).

## Aufräumen der Ablage (03.10.2026, App unverändert, kein Versionswechsel)

- **Dokumente zusammengeführt:** `00_Arbeitsvorbereitung` von 24 Dokumenten auf vier ([Übergabe](../../00_Arbeitsvorbereitung/Glide_Uebergabe.md), [Entwicklungsplan](../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) mit Statusmarken, Markt und Vorbilder, manuelle Prüfliste); `docs/` von 53 auf elf Dokumente und fünf Entscheidungen. Die Funktionsverträge 45–79 (32 Dateien) stehen verdichtet in [Funktionen](docs/20_FUNKTIONEN.md), Releasecheckliste, Signierung, Vertrieb, Lizenzentwurf und Inhaberangaben in [Veröffentlichung](docs/10_VEROEFFENTLICHUNG.md), Tk-Fallstricke und Performance-Regeln in der [Architektur](docs/02_ARCHITECTURE.md). Keine Archivordner mehr; gelöscht statt verschoben.
- **Sieben Versionen, drei Bildstände:** Archive, Nachweise (`tests/qa-*`) und Releaseplanungen bleiben nur für die sieben neuesten Versionen; je Datenformat 11–19 eine Releaseplanung als Lesbarkeitsbeleg und 3.30.0 als Messgrundlage. Fensterbilder nur für die drei neuesten Versionen. Neue Regel „Archivalter“ in `tests/tools/ablagegroesse.py` (CI-Schritt „Ablagegröße“), Kürzung mit `scripts/pflege/ablage_kuerzen.py`, das auch `versionswechsel.py` aufruft.
- **Entfernt:** `40_Store_Material` (Inhalt in Veröffentlichung), Archive in 00, 05, 07 und 20, Nutzerkopien 3.30.0 in `05_Probelisten_Testdaten`, Release-Fixtures außerhalb der Regel, Nachweise vor 3.33.0, Sitzungsreste in den Nachweisen 3.33.0/3.33.1. Versionierter Stand 4.985 → 819 Dateien, 1.158 → 404 MB; Markdown-Dateien 659 → 57.
- **Datenschutz:** CI-Schritt „Datenschutz“ und `pfade_bereinigen.py` erkennen Benutzerpfade jetzt auch JSON-maskiert (`\/Users\/…`); ein solcher Fund in einem Aufräumprotokoll war bis dahin durchgerutscht und ist gelöscht. Neuer Werkzeugtest `test_datenschutz.py`.
- **Archivnamen:** Hauptdateien in `07_Python-Versionen/Archiv` ohne Endung `_Z`; `abgleich_07.py` legt sie so ab.
- **`.gitignore`** in Abschnitte Sicherheit (Schlüssel, Zertifikate, Zugangsdaten), Nutzerdaten, Protokolle, Archive und Werkzeuge gegliedert; Grenzen und Durchsetzung durch CI und Secret Scanning im Kopf beschrieben. [Nachweis](tests/qa-3.33.6/aufraeumen_2026-10-03/README.md).

## 3.33.6 – Heute und Demnächst (02.10.2026)

- **Schlanke Ablage (App unverändert, Entscheidung des Inhabers):**
  - Die Arbeitskopie war mit 3.33.1–3.33.6 von 1,2 auf 2,0 GB gewachsen: Versionswechsel und Showcase-Abgleich legten je Lauf rund 75 MB Archivkopien an, jede Vollprüfung brachte rund 25 MB Fensterbilder mit.
  - 335 Dateien mit 912 MB entfernt: Archivkopien von Showcase, Beispieldaten und Rundgang, ein `.fetch`-Rest und die Fensterbilder überholter Vollprüfungen (je Version bleibt die letzte). Vorfassungen trägt Git.
  - `versionswechsel.py` und `showcase_abgleich.py` ohne Archivkopien; `.gitignore` schließt Archivordner, `*.fetch` und `fenster/` aus; neuer CI-Schritt „Ablagegröße“ (`tests/tools/ablagegroesse.py`, 7 Werkzeugtests). [Nachweis](tests/qa-3.33.6/ablage_2026-10-02/README.md).

- **D14:** „Mein Tag“ heißt „Heute“ und beantwortet eine Frage: was ist heute dran? Oben die nächste Aufgabe (dieselbe wie auf der Startseite), dann Verspätet, Liegen geblieben, der Tagesplan (mit Zeitplan und Stundenraster wie bisher), Heute fällig und am Ende der Eingang. Jede Aufgabe steht genau einmal; künftige Fälligkeiten erreicht eine Verweiszeile „Demnächst · N weitere Fälligkeiten“.
- **„In Bearbeitung“ heißt „Demnächst“** und zeigt alle Fälligkeiten chronologisch, Überfälliges oben. Die nächste Aufgabe steht nicht mehr doppelt dort; „Nächste Aufgabe“ in Menü und Startseite führt nach „Heute“.
- **Tagesbeginn und Tagesabschluss** sind Modi von „Heute“: Schalter „Tag …“ in der Filterzeile und Einträge im Kontextmenü der Seitenleistenzeile. An anderen Tagen (◀/▶) zeigt die Ansicht „Tagesplan · Datum“ und was an diesem Tag fällig ist.
- Neue Namen in Seitenleiste, Fenstertitel, Menüs, Befehlspalette, Startseite, Startansicht, Kalenderausgabe, Tageszettel, Handbuch und Kontextmenü („Für heute einplanen“). Interne Kennungen und Einstellungen bleiben; `/meintag` funktioniert weiter. Die Zahl hinter „Heute“ zählt alles, was „Heute“ zeigt.
- **Tk-frei (D17):** `today_view.py` mit sechs Unit-Tests; neue Pflichtsuite `test_heute3336.py`; sieben Altsuiten auf den neuen Vertrag gebracht. Datenformat 20, keine neue Abhängigkeit. [Funktionen](docs/20_FUNKTIONEN.md#4-heute-demnächst-und-planung).

## 3.33.5 – Eisenhower als Gruppierung (02.10.2026)

- **G02 nach D13:** Neue Gruppierung „Dringlichkeit × Wichtigkeit“ im Spaltenboard, in Liste und Tabelle – keine eigene Ansicht. Vier Quadranten: Sofort (wichtig und dringend), Einplanen, Kurz halten, Später. Wichtig heißt Wichtigkeit ab mittel; dringend heißt Fälligkeit oder Bearbeitungstag in den nächsten zwei Tagen oder überfällig.
- **Ziehen nach D02:** In einen wichtigen Quadranten wird die Wichtigkeit mittel, in einen unwichtigen niedrig; in einen dringenden wird der Bearbeitungstag heute, in einen nicht dringenden der erste Tag nach dem Zweitagesfenster. Eine Fälligkeit ändert sich nie; macht sie die Aufgabe dringend, lehnt Glide das Ablegen mit Begründung ab. Eine Rückmeldung nennt, was sich geändert hat; ein Rückgängig-Schritt.
- Befehlspalette: der neue Gruppierungsbefehl steht unter „Ansichtseinstellungen“ (Risiko R2: Menübeschriftungen sind Schlüssel). Handbuch ergänzt.
- **Tk-frei (D17):** `eisenhower.py` mit vier Unit-Tests; neue Pflichtsuite `test_eisenhower3335.py`. [Funktionen](docs/20_FUNKTIONEN.md#5-liste-tabelle-gruppierung).

## 3.33.4 – Wiederholungen in der Schnelleingabe (02.10.2026)

- **Erkannt:** „täglich“, „jeden Tag“, „werktags“, „wöchentlich“, „jeden Montag“, „montags und donnerstags“, „alle 3 Tage“, „alle 2 Wochen“ (als alle 14 Tage), „monatlich“, „jährlich“ – mit Uhrzeit direkt dahinter („jeden Montag 18 Uhr“).
- **Fälligkeit:** Eine Wiederholung setzt die Fälligkeit auf ihren ersten Termin, damit sie im Kalender steht (Entscheidung des Inhabers vom 02.10.2026, Ergänzung zu D10). Steht zusätzlich „bis …“ da, beginnt die Reihe dort. Der Chip zeigt Regel und ersten Termin; × nimmt die Wiederholung zurück.
- Abhaken erzeugt den nächsten Termin über die vorhandene Wiederholungslogik. Regeln, die das Datenmodell nicht kennt („alle 3 Monate“), bleiben Text.
- Drei neue Unit-Tests, `test_eingabe3333.py` um echte Eingabe, Kalender und Folgetermin erweitert; Gegenprobe mit 3.33.3 rot. [Funktionen](docs/20_FUNKTIONEN.md#3-erfassen).

## 3.33.3 – Deutsche Schnelleingabe mit Feldchips (02.10.2026)

- **G01:** Die Eingabezeile erkennt deutsche Angaben: „morgen“, ein Wochentag, „nächsten Freitag“, „in 3 Tagen“ oder ein Datum setzen den Bearbeitungstag; „fällig“ oder „bis“ davor die Fälligkeit (D01). Dazu „um 14:30“/„14 Uhr“ (Uhrzeit; allein heißt sie heute), „45 Minuten“/„1 Std. 30 Min.“ (Aufwand), „!hoch“ (Wichtigkeit) und „#Labelname“ für vorhandene Labels.
- **Feldchips:** Unter der Eingabe steht jede Erkennung als Chip; × nimmt sie zurück, der Text bleibt im Titel. Text in Anführungszeichen bleibt wörtlich. Die Schnellerfassung zeigt dieselben Chips unter dem Titel; ein ausgefülltes Feld „Fällig“ hat Vorrang.
- **D10:** Auch `/morgen`, ein Wochentag oder `/24.12.2026` setzen jetzt den Bearbeitungstag; die Fälligkeit setzen `/bis Freitag` und `/fällig morgen`. Gespeicherte Daten bleiben unverändert; Handbuch nachgeführt.
- **Tk-frei (D17):** `capture_parser.py` mit 14 Unit-Tests; die bisherigen Parser aus `app.pyw` sind dorthin umgezogen. Neue Pflichtsuite `test_eingabe3333.py`; `test_bilder330` prüft die neue Bedeutung von `/morgen`. Wiederholungen („jeden Montag“) sind noch nicht dabei – sie hängen im Datenmodell an der Fälligkeit, das braucht eine Entscheidung. [Funktionen](docs/20_FUNKTIONEN.md#3-erfassen).

## 3.33.2 – Startseite „Ruhig“ und schnellerer Aufbau (02.10.2026)

- **Startseite nach D12:** sieben Standardkacheln – Heute, Gismo, die nächsten sieben Tage, Zuletzt bearbeitet, Pinnwand-Vorschau, Zeichnungen, Angeheftet. Uhr, Begrüßung, Nächste Aufgabe, Vorlagen, Bestand und alle übrigen bleiben wählbar. Eine eigene Auswahl bleibt erhalten; wer die Startseite nie eingerichtet hatte, sieht den neuen Standard.
- **Kachel „Heute“ zusammengeführt:** Tagesziel und nächste Aufgabe stehen darin, solange ihre eigenen Kacheln aus sind – jede Angabe genau einmal.
- **Korrektur:** Eine im Bearbeitungsmodus eingeblendete Kachel verschwand nach dem Neustart wieder, wenn die Startseite nie umsortiert worden war. Ein- und Ausblenden speichern jetzt die ganze Auswahl.
- **Neu:** „Standard wiederherstellen“ im Dialog „Startseite einrichten“.
- **Schnellerer Aufbau (Rest P03):** Größenmeldungen des Hauptfensters werden in Tcl gefiltert, statt für jedes Kind Python aufzurufen (wirkt in allen Ansichten); gerundete Flächen und Knöpfe zeichnen einmal je Leerlauf statt bei jeder Zwischengröße; Umbruchbreite und Hintergrundfarben werden nur bei Änderung gesetzt.
- **Tk-frei (D17):** `home_tiles.py` mit acht Unit-Tests; neue Pflichtsuite `test_startseite3332.py`; neues Messwerkzeug `scripts/pflege/messung_startseite.py`. `versionswechsel.py` legt keine Markdown-Kopien mehr an (Git trägt die Historie, Löschfreigabe vom 01.10.2026). Datenformat 20, keine neue Abhängigkeit. [Funktionen](docs/20_FUNKTIONEN.md#7-startseite).

## 3.33.1 – Vier Bereiche und Fensterbedienung (01.10.2026)

- **Abschluss nach der Mac-Vollprüfung (01./02.10.2026):** Die vier roten Schritte des Prüfkandidaten sind nachgestellt und behoben. [Nachweis](tests/qa-3.33.1/abschluss_2026-10-01/README.md).
  - Dialog „Neu anlegen“ auf niedrigen Bildschirmen: macOS meldet beim Einblenden zuerst 1 × 1 Pixel; seit dem verborgenen Vermessen folgte keine echte Breite mehr. Die breite Maske blieb einspaltig, die Beschreibung lag unter dem sichtbaren Rand. Der Spaltenumschalter übergeht diese Platzhaltergröße.
  - Notizbücher im Bereich Notizen nehmen wieder datierte Zeichnungen auf („Zeichnung · TT.MM.JJJJ“, Vertrag 65; Klarstellung des Inhabers vom 01.10.2026). Anlegen, Ziehen, Verschieben, Einrücken, Wiederherstellen und Vorlagen prüfen dafür den Zielordner (`sidebar_policy.CONTAINED`). Aufgabenlisten und Pinnwände in einem Notizbuch bleiben ein Fall für Listen; ein bestehendes Notizbuch mit Zeichnungen steht wieder unter Notizen.
  - Zwei Prüfungen auf den 3.33.1-Vertrag gebracht: `audit_app` simuliert den Zeiger nur noch über dem Zielbaum (Bereichsüberschriften sind Ablageziele), `test_aufraeumen330` erwartet die Menüfolge, die `test_features330` schon prüft.
  - Zwei neue Tk-freie Unit-Tests; `test_bereiche3331` prüft die Notizbuch-Zeichnung über echtes Ziehen, Momentdatum, Rückgängig und die Ablehnung für gewöhnliche Ordner und Aufgabenlisten.
  - Vollprüfung Exitcode 0 (77 Schritte, 60 Integrationssuiten); `07_Python-Versionen` und neu gebautes macOS-Bundle bytegleich (142/56 Dateien), Signatur gültig. Zwei ungültige Vorläufe sind belegt: gesperrter Bildschirm und wahrscheinlich Tastatureingaben während des Laufs. Der Hintergrundmodus schirmt nur die Maus ab; Testplan und Übergabe nennen diese Grenze.

- **Sicherheit und öffentliches Repository (App unverändert):**
  - GitHub-Sicherheitsrichtlinie (`SECURITY.md` in der Wurzel; ersetzt die dort angelegte GitHub-Vorlage) mit vertraulichem Meldeweg, Dependabot für GitHub Actions; Checkout ohne gespeichertes Token. Der zunächst eingerichtete CodeQL-Workflow ist vom Inhaber deaktiviert.
  - CI-Grundstufe prüft zusätzlich die Herkunft des Fremdcodes (alle 116 Dateien unter `vendor/tkinterdnd2` bytegleich zum PyPI-Paket aus `provenance.json`) und verhindert Benutzerpfade in versionierten Dateien.
  - Rohprotokolle bleiben lokal: `*.log` wieder ausgeschlossen, 263 Protokolle aus dem Stand genommen; 110 Benutzerpfade in 27 Dateien ersetzt; neues Werkzeug `scripts/pflege/pfade_bereinigen.py`.
  - README der Ablage als GitHub-Einstieg neu gegliedert, README des Quellbaums ergänzt. [Nachweis](tests/qa-3.33.1/sicherheit_2026-10-01/README.md).

- Seiten, Listen, Notizen und Zeichnungen als getrennte Bereiche. Seiten/Notizen/Zeichnungen lassen sich in den Einstellungen ausblenden; alle Daten bleiben über Listen erreichbar.
- Einheitliche Inhaltsgrenzen für Anlegen, Vorlagen, Kontextmenüs und Verschieben; Listen erlaubt alle Arten. Gemischte bestehende Ordner bleiben vollständig unter Listen. Kein neuer Inhaltstyp und keine Datenmigration.
- Root-Zuordnung als Anzeigeeinstellung, einschließlich Rückgängig; Zeichnungsübersicht, vier Klappbereiche und begrenzte Baumhöhen bei kleiner Fensterhöhe.
- Logo beginnt auf Höhe der Titeloberkante. Dialoge werden erst fertig positioniert eingeblendet; doppelte Leerlaufabfragen und unveränderte Breitenmessungen vermieden.
- Showcase zeigt die vorhandene Pixelskizze im neuen Zeichnungsbereich. Neue Pflichtsuite für die tatsächlichen Bereichs-, Formular-, Drag-, Settings- und Neustartwege.
- **CI-Grundstufe (D09, App unverändert):** Die GitHub-Vorlage „Python application“ brach mit Exitcode 2 ab, weil `pytest` das ganze Repository einsammelte (Archivkopien, Altstände, Tk-Suiten ohne Bildschirm). Der Workflow führt jetzt `tests/tools/ci_grundstufe.py` aus: Vorprüfungen, Werkzeug- und Unit-Tests, Analysen, Startprobe unter Xvfb, Lieferstand als Hinweis. Integrationssuiten unter Linux nur manuell und informativ. `07_Python-Versionen` mit `abgleich_07.py` auf den Prüfkandidaten 3.33.1 gebracht; `app.pyw.fetch` (Zwischenfassung) und die PyPI-Vorlage entfernt; zwei Verweise auf das entfernte `90_Testdaten_Extern` gelöscht. [Nachweis](tests/qa-3.33.1/ci_grundstufe_2026-10-01/README.md).

## 3.33.0 – Fundament für die geplanten Ausbauten (01.10.2026)

- T2: gemeinsame Formatsicherung in `schema_backups.py`; beim Laden vorhandene Formatinformation nutzen, sonst einmal je Dateistand lesen. Bytegenaue Rückfallkopien, Fehlerabbruch und bestehende Migrationseinstiege erhalten.
- P09a/W1: Tabellen- und Bibliotheksansicht vermessen keine ungenutzten Listenspalten mehr; Listenspalten unverändert.
- Acht Tk-freie Unit-Tests und eine neue Integration für alle Formatstufen, Austausch, Fehler/Retry, Reload und Spaltenbreiten; eigener QA-Fenster-Mausschutz geprüft.
- GitHub-Stand und umgezogene Ablage abgeglichen; ursprüngliche Claude-Übergabe bleibt historisch. D12 ergänzt: Zeichnungen und Pinnwand-Vorschau.
- Oberflächenumbau folgt nach dem Fundament; Datenformat 20 und bestehende Dokumentarten bleiben erhalten.

## Frühere Versionen (verdichtet)

Datenformate und ihre Felder: [Daten und Migration](docs/06_DATA_BACKUP_MIGRATION.md#formatstufen).

| Version | Datum | Kern |
|---|---|---|
| 3.32.3 | 01.10.2026 | Bibliothek und Aktionsleiste behalten unveränderte Karten (Refresh bei 1.000 Aufgaben 776 → 5 ms); aktiver Showcase „Parkquartier“; Beschlüsse D09–D17 |
| 3.32.2 | 30.09.2026 | Drag-and-drop in allen Seitenleistenbereichen (D04); Schriftwerte je Tk-Interpreter zwischengespeichert |
| 3.32.1 | 30.09.2026 | Klappzustände von Labelgruppen, Fächern und Bereichen bleiben erhalten; Klapppfeile per Tastatur; D01–D06 übernommen |
| 3.32.0 | 30.09.2026 | ICO-Export, Aseprite-/ASE-Paletten, selbstfüllende Platzhalter, Tagesabschluss; Hänger bei Menübefehlen und Bildseiten behoben; Pflegewerkzeuge |
| 3.31.0 | 30.09.2026 | Rückmeldungen R1–R11: Menüdialoge öffnen wieder, Editor mit Blockaktionen, Farben nach Bedeutung, schnellere Übersicht |
| 3.30.0 | 25.–29.09.2026 | Modernisierung: Pixel-Werkstatt, Startseite zum Anpassen, Pinnwand als Board, Notizbuch, Seiten mit Bildern, Galerien, Tk 9, Ziehen aus Finder/Explorer, Systemmitteilungen, zehn Designs, Logo; **Format 20** |
| 3.29.0 | 24.09.2026 | Zeichnung als eigene Listenart mit Referenzbild; **Format 19** |
| 3.28.0 | 23.09.2026 | Ordnertypen und Tagebuch (später Notizbuch); **Format 18** |
| 3.26.0 | 21.09.2026 | Notizen als Listenart, Begleiter Gismo, Lizenzentwurf; **Format 17** |
| 3.25.0 | 19.09.2026 | „Form follows function“: Übersicht und Hierarchie, Startseite mit Kacheln und gezeichneter Figur |
| 3.24.0 | 19.09.2026 | Kürzere Navigation; Pinnwand mit Mehrfachauswahl und gerichteten Verbindungen |
| 3.23.0 | 18.09.2026 | Zusammenhalt vorhandener Funktionen (46 Punkte) |
| 3.22.0 | 17.09.2026 | Checkliste je Aufgabe; **Format 16** |
| 3.21.0–3.21.4 | 14.09.2026 | Kalenderimport aus ICS, Serienende ohne UTC-Versatz, Beispielbestand testbar, Standprüfung |
| 3.20.0 | 14.09.2026 | Kalenderausgabe als ICS |
| 3.19.0 | 13.09.2026 | Dauerhafter Änderungsverlauf; **Format 15** |
| 3.18.0 | 13.09.2026 | CSV-Import mit Spaltenzuordnung |
| 3.17.0 | 13.09.2026 | Druck- und PDF-Ausgabe |
| 3.16.0 | 13.09.2026 | Vollständiges App-Backup (`.glideapp`) |
| 3.15.0 | 13.09.2026 | Tagesplanung und Tageskapazität |
| 3.14.0 | 13.09.2026 | Bearbeitungstag und geschätzter Aufwand; **Format 14** |
| 3.13.0 | 13.09.2026 | Tabellenansicht |
| 3.12.0 | 13.09.2026 | „Mein Tag“ (seit 3.33.6 „Heute“) |
| 3.11.0 | 13.09.2026 | Schnellerfassung und gespeicherte Filter |
| 3.10.0 | 13.09.2026 | Reiter und Pinnwand |
| 3.9.0 | 12.09.2026 | Einheitliche Oberfläche, Einstellungen, Hell/Dunkel |
| 3.8.0 | 12.09.2026 | Lokale Erinnerungen, Aufmerksamkeit in Taskleiste und Dock; **Format 13** |
| 3.7.0 | 07.–12.09.2026 | Kompakte Kacheln, Anhänge an Listen und Ordnern, dynamische Übersicht; **Format 12** |
| 3.6.0 | 06.09.2026 | Kachelübersicht der Listen, Jahresanzeige |
| 3.5.0 | 05.09.2026 | Wiederkehrende Aufgaben; **Format 11** |
| 3.4.0 | 05.09.2026 | Startseite neu: Uhr, Tagesziel, Schnellzugriffe, Bestand, Listenfarben |
| 3.3.0 | 04.09.2026 | Ansicht „Labels“ |
| 3.2.0 | 04.09.2026 | Keine Übernahme aus Altordnern; zentrale Textzeichen |
| 3.1.0 | 04.09.2026 | Aufräumversion ohne neue Funktion |
| 3.0.0–3.0.2 | 03.09.2026 | Neue Oberfläche (Inhalt nach oben, kein Schwarz im Hellmodus); Gruppen benutzbar, Mehrmonitor-Dialoge |
| 2.12.0 | 03.09.2026 | Ruhigere Eingabemaske |
| 2.11.0 | 03.09.2026 | Papierkorb auch für Punkte, Mehrfachauswahl, Uhrzeit; **Format 10** |
| 2.10.0 | 03.09.2026 | Label-Chips, verlustfreier TXT-Rundlauf |
| 2.9.0 | 03.09.2026 | Verschachtelte Ordner, Long-Task-Details |
| 2.8.0 | 02.09.2026 | Verspätet, Long-Task, Zwischenüberschrift, Anlage-Dialog |
| 2.7.0–2.7.2 | 02.09.2026 | Papierkorb für Listen und Ordner, Labels; **Format 7** |
| 2.6.0 | 01.09.2026 | Gruppen; **Format 6** |
| 2.5.1–2.5.5 | 31.08.–02.09.2026 | Ordneransicht, fester Eingang, Kontextmenü, „In Bearbeitung“, Anhangspfade; **Format 5** |
| 2.5.0, 2.4.1 | vor 31.08.2026 | Zwischenstand und Ausgangsstand |
