# Änderungsverlauf

## 3.33.6 – Heute und Demnächst (02.10.2026)

- **Schlanke Ablage (App unverändert, Entscheidung des Inhabers):**
  - Die Arbeitskopie war mit 3.33.1–3.33.6 von 1,2 auf 2,0 GB gewachsen: Versionswechsel und Showcase-Abgleich legten je Lauf rund 75 MB Archivkopien an, jede Vollprüfung brachte rund 25 MB Fensterbilder mit.
  - 335 Dateien mit 912 MB entfernt: Archivkopien von Showcase, Beispieldaten und Rundgang, ein `.fetch`-Rest und die Fensterbilder überholter Vollprüfungen (je Version bleibt die letzte). Vorfassungen trägt Git.
  - `versionswechsel.py` und `showcase_abgleich.py` ohne Archivkopien; `.gitignore` schließt Archivordner, `*.fetch` und `fenster/` aus; neuer CI-Schritt „Ablagegröße“ (`tests/tools/ablagegroesse.py`, 7 Werkzeugtests). [Nachweis](tests/qa-3.33.6/ablage_2026-10-02/README.md).

- **D14:** „Mein Tag“ heißt „Heute“ und beantwortet eine Frage: was ist heute dran? Oben die nächste Aufgabe (dieselbe wie auf der Startseite), dann Verspätet, Liegen geblieben, der Tagesplan (mit Zeitplan und Stundenraster wie bisher), Heute fällig und am Ende der Eingang. Jede Aufgabe steht genau einmal; künftige Fälligkeiten erreicht eine Verweiszeile „Demnächst · N weitere Fälligkeiten“.
- **„In Bearbeitung“ heißt „Demnächst“** und zeigt alle Fälligkeiten chronologisch, Überfälliges oben. Die nächste Aufgabe steht nicht mehr doppelt dort; „Nächste Aufgabe“ in Menü und Startseite führt nach „Heute“.
- **Tagesbeginn und Tagesabschluss** sind Modi von „Heute“: Schalter „Tag …“ in der Filterzeile und Einträge im Kontextmenü der Seitenleistenzeile. An anderen Tagen (◀/▶) zeigt die Ansicht „Tagesplan · Datum“ und was an diesem Tag fällig ist.
- Neue Namen in Seitenleiste, Fenstertitel, Menüs, Befehlspalette, Startseite, Startansicht, Kalenderausgabe, Tageszettel, Handbuch und Kontextmenü („Für heute einplanen“). Interne Kennungen und Einstellungen bleiben; `/meintag` funktioniert weiter. Die Zahl hinter „Heute“ zählt alles, was „Heute“ zeigt.
- **Tk-frei (D17):** `today_view.py` mit sechs Unit-Tests; neue Pflichtsuite `test_heute3336.py`; sieben Altsuiten auf den neuen Vertrag gebracht. Datenformat 20, keine neue Abhängigkeit. [Vertrag](docs/79_HEUTE_3.33.6.md).

## 3.33.5 – Eisenhower als Gruppierung (02.10.2026)

- **G02 nach D13:** Neue Gruppierung „Dringlichkeit × Wichtigkeit“ im Spaltenboard, in Liste und Tabelle – keine eigene Ansicht. Vier Quadranten: Sofort (wichtig und dringend), Einplanen, Kurz halten, Später. Wichtig heißt Wichtigkeit ab mittel; dringend heißt Fälligkeit oder Bearbeitungstag in den nächsten zwei Tagen oder überfällig.
- **Ziehen nach D02:** In einen wichtigen Quadranten wird die Wichtigkeit mittel, in einen unwichtigen niedrig; in einen dringenden wird der Bearbeitungstag heute, in einen nicht dringenden der erste Tag nach dem Zweitagesfenster. Eine Fälligkeit ändert sich nie; macht sie die Aufgabe dringend, lehnt Glide das Ablegen mit Begründung ab. Eine Rückmeldung nennt, was sich geändert hat; ein Rückgängig-Schritt.
- Befehlspalette: der neue Gruppierungsbefehl steht unter „Ansichtseinstellungen“ (Risiko R2: Menübeschriftungen sind Schlüssel). Handbuch ergänzt.
- **Tk-frei (D17):** `eisenhower.py` mit vier Unit-Tests; neue Pflichtsuite `test_eisenhower3335.py`. [Vertrag](docs/78_EISENHOWER_3.33.5.md).

## 3.33.4 – Wiederholungen in der Schnelleingabe (02.10.2026)

- **Erkannt:** „täglich“, „jeden Tag“, „werktags“, „wöchentlich“, „jeden Montag“, „montags und donnerstags“, „alle 3 Tage“, „alle 2 Wochen“ (als alle 14 Tage), „monatlich“, „jährlich“ – mit Uhrzeit direkt dahinter („jeden Montag 18 Uhr“).
- **Fälligkeit:** Eine Wiederholung setzt die Fälligkeit auf ihren ersten Termin, damit sie im Kalender steht (Entscheidung des Inhabers vom 02.10.2026, Ergänzung zu D10). Steht zusätzlich „bis …“ da, beginnt die Reihe dort. Der Chip zeigt Regel und ersten Termin; × nimmt die Wiederholung zurück.
- Abhaken erzeugt den nächsten Termin über die vorhandene Wiederholungslogik. Regeln, die das Datenmodell nicht kennt („alle 3 Monate“), bleiben Text.
- Drei neue Unit-Tests, `test_eingabe3333.py` um echte Eingabe, Kalender und Folgetermin erweitert; Gegenprobe mit 3.33.3 rot. [Vertrag](docs/77_EINGABE_3.33.3.md#ergänzung-3334-wiederholungen).

## 3.33.3 – Deutsche Schnelleingabe mit Feldchips (02.10.2026)

- **G01:** Die Eingabezeile erkennt deutsche Angaben: „morgen“, ein Wochentag, „nächsten Freitag“, „in 3 Tagen“ oder ein Datum setzen den Bearbeitungstag; „fällig“ oder „bis“ davor die Fälligkeit (D01). Dazu „um 14:30“/„14 Uhr“ (Uhrzeit; allein heißt sie heute), „45 Minuten“/„1 Std. 30 Min.“ (Aufwand), „!hoch“ (Wichtigkeit) und „#Labelname“ für vorhandene Labels.
- **Feldchips:** Unter der Eingabe steht jede Erkennung als Chip; × nimmt sie zurück, der Text bleibt im Titel. Text in Anführungszeichen bleibt wörtlich. Die Schnellerfassung zeigt dieselben Chips unter dem Titel; ein ausgefülltes Feld „Fällig“ hat Vorrang.
- **D10:** Auch `/morgen`, ein Wochentag oder `/24.12.2026` setzen jetzt den Bearbeitungstag; die Fälligkeit setzen `/bis Freitag` und `/fällig morgen`. Gespeicherte Daten bleiben unverändert; Handbuch nachgeführt.
- **Tk-frei (D17):** `capture_parser.py` mit 14 Unit-Tests; die bisherigen Parser aus `app.pyw` sind dorthin umgezogen. Neue Pflichtsuite `test_eingabe3333.py`; `test_bilder330` prüft die neue Bedeutung von `/morgen`. Wiederholungen („jeden Montag“) sind noch nicht dabei – sie hängen im Datenmodell an der Fälligkeit, das braucht eine Entscheidung. [Vertrag](docs/77_EINGABE_3.33.3.md).

## 3.33.2 – Startseite „Ruhig“ und schnellerer Aufbau (02.10.2026)

- **Startseite nach D12:** sieben Standardkacheln – Heute, Gismo, die nächsten sieben Tage, Zuletzt bearbeitet, Pinnwand-Vorschau, Zeichnungen, Angeheftet. Uhr, Begrüßung, Nächste Aufgabe, Vorlagen, Bestand und alle übrigen bleiben wählbar. Eine eigene Auswahl bleibt erhalten; wer die Startseite nie eingerichtet hatte, sieht den neuen Standard.
- **Kachel „Heute“ zusammengeführt:** Tagesziel und nächste Aufgabe stehen darin, solange ihre eigenen Kacheln aus sind – jede Angabe genau einmal.
- **Korrektur:** Eine im Bearbeitungsmodus eingeblendete Kachel verschwand nach dem Neustart wieder, wenn die Startseite nie umsortiert worden war. Ein- und Ausblenden speichern jetzt die ganze Auswahl.
- **Neu:** „Standard wiederherstellen“ im Dialog „Startseite einrichten“.
- **Schnellerer Aufbau (Rest P03):** Größenmeldungen des Hauptfensters werden in Tcl gefiltert, statt für jedes Kind Python aufzurufen (wirkt in allen Ansichten); gerundete Flächen und Knöpfe zeichnen einmal je Leerlauf statt bei jeder Zwischengröße; Umbruchbreite und Hintergrundfarben werden nur bei Änderung gesetzt.
- **Tk-frei (D17):** `home_tiles.py` mit acht Unit-Tests; neue Pflichtsuite `test_startseite3332.py`; neues Messwerkzeug `scripts/pflege/messung_startseite.py`. `versionswechsel.py` legt keine Markdown-Kopien mehr an (Git trägt die Historie, Löschfreigabe vom 01.10.2026). Datenformat 20, keine neue Abhängigkeit. [Vertrag](docs/76_STARTSEITE_3.33.2.md).

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

## 3.32.3 – 01.10.2026

- **Beschlüsse D09–D17 und Prüfaufrufe (App unverändert):**
  - Richtungsentscheidungen D09–D17 in Entscheidungsvorlage, Arbeitsrichtung, Plan und Übergaben eingetragen (D12 mit sieben Startseitenkacheln).
  - `.gitignore` gibt Prüfprotokolle `tests/qa-*/**/*.log` frei (D09).
  - Messbefund T8/P09: Die Schriftart wird bereits einmal geprüft; die Tabellenansicht misst nach jedem Aufbau jede Zeile ohne Nutzen. Neue Proben `pruefaufrufe_probe.py` und `pixelschrift_probe.py`.
  - [Nachweis](tests/qa-3.32.3/pruefaufrufe_2026-10-01/README.md).

- **Analyse-/Planungsnachlauf (App unverändert):** Bestandsaufnahme Code/Doku, Konkurrenz- und Featurematrix, Produktprinzipien mit UX-Prüfung, Entwicklungsplan ab 3.33 und Entscheidungsvorlage D09–D17 in `00_Arbeitsvorbereitung`. Produktgrenzen korrigiert (Verlaufsgrenze 15/15, Bildvorschau Windows, Lila = Hinzufügen) und um die sechs Produktprinzipien ergänzt. Neues Pflegewerkzeug `scripts/pflege/messung_speicherweg.py`. Repository-Ablage auf die Projektstruktur ausgerichtet; tkdnd-Linux-Bibliotheken, CRLF-Drittdateien und Showcase-Sicherung wiederhergestellt. [Nachweis](tests/qa-3.32.3/analyse_planung_2026-10-01/README.md).

- **Aktiver Showcase:** Zehn zusammenhängende Projektdokumente, sechs Originalmotive, drei eingebettete Seitenbilder, vollständige Anhänge, Projektpinnwände, Tagesplanung, Tagebuch und zwei Zusatzvorlagen. Separater Starter erhält Demo-Bearbeitungen. Funktionsvorschau mit frischen Terminen; Import-/Neustartprüfung jetzt verpflichtend. Daten-/Werkzeugnachlauf zur unveränderten App. [Umfang und Abnahme](docs/72_SHOWCASE_3.32.3.md).

- **Dokumentations-/Prüfwerkzeugnachlauf:** Fortlaufende Arbeitsrichtung mit D01–D08 und Abnahme verankert; aktive Übergaben, Pläne, Checklisten und technische Regeln inhaltlich abgeglichen. Standprüfung erfasst gepflegte datierte Einstiege, aktuelle Titel und erste Vollprüfungsaufrufe; gezielte Werkzeugregression. Laufzeit und Startfassungen unverändert.

- **Bibliothek:** Unveränderte Karten und Öffnen-Buttons in derselben Ansicht erhalten. Anzeigedaten frisch berechnen; nur betroffene Karten neu aufbauen. Reihenfolge, Ordnerpfade, Labels, Status/Termine, Symbole, Zeichnungen und Design-/Schriftwechsel berücksichtigen. Zerstörter Ansichtshost gibt den Cache frei.
- **Gemeinsame Aktionsleiste:** Unveränderte Aktionen erhalten; Befehle und Höhenstufe berücksichtigen. Ersetzte Configure-Bindung freigeben, damit wiederholte Änderungen keine Rückrufe ansammeln.
- **Archiv:** „Zurückholen“ verwendet die vorhandene zentrale Aktualisierung einmal; der zusätzliche identische Refresh entfällt.
- **Tempo:** Bei 1.000 synthetischen Aufgaben sinkt unveränderter Bibliotheks-Refresh im Median 776,2 → 4,9 ms; Statusänderung 785,3 → 388,3 ms. Neue gerundete Container 17 → 0 bzw. 2. Erneutes Rendern in derselben Ansicht, keine allgemeine Speicher-/Wechsellatenz.
- **QA:** Neue Pflichtsuite `test_library_performance3323.py` mit nativen Knopfereignissen, Undo, Tageswechsel, Breiten-/Designwechsel und Lebensdauerprüfung. Vorher-/Nachher-Serien mit 100/1.000/10.000 Aufgaben, Rohwerten und Containerzählung. Format 20, keine neue Abhängigkeit.

[Vertrag, Messgrenzen und Prüfstand](docs/71_KARTEN_PERFORMANCE_3.32.3.md).

## 3.32.2 – 30.09.2026

- **D04:** Drag-and-drop in allen bestehenden Seitenleistenbereichen; Seiten, Notizen, Bibliotheken und Notizbücher umordnen/verschieben. Zielkoordinaten bei Bereichswechsel korrekt, native Klapppfeile erhalten, Arten und Termine bewahrt, gemeinsames Undo und Bestandswächter.
- **Performance:** Schriftwerte je Tk-Interpreter zwischenspeichern und beim Schriftwechsel invalidieren; Formatleistenlayouts bündeln und unveränderte Geometrie nicht neu schreiben. Gemeinsamer Hoverhelfer für Datums- und Labelauswahl.
- **Nachweis:** Unprofilierte Vorher-/Nachher-Serien mit Aufgaben, Notiz und Bildseite; Median/p95 und Rohwerte. Bibliotheks-, Bildseiten- und Notizwechsel messbar schneller; Widget-Neuerzeugung bleibt ein Folgethema.
- **QA:** Neue Pflichtsuite `test_drag_performance3322.py` bedient echte Drag-Bindungen, prüft Daten/Undo/Neustart, Schriftwechsel und Werkzeugleisten. Datenformat 20, keine neue Abhängigkeit, Hinweise unverändert.

Vertrag und Messgrenzen: [Drag-and-drop und Performance 3.32.2](docs/70_DRAG_UND_PERFORMANCE_3.32.2.md).

## 3.32.1 – 30.09.2026

- **Labelgruppen klappen wieder:** Die Drag-Klickbehandlung verarbeitet jetzt
  den Klapppfeil. Der Zustand bleibt bei Suche, Neuaufbau, Ansichtswechsel und
  erneutem Laden der Einstellungen erhalten, einschließlich „Ohne Label“.
- **Gemeinsame Zustandskontrolle:** Native Aufklappaktionen werden nach dem
  Tk-Zustandswechsel gespeichert. Globale Klappaktionen merken auch Label-
  und Gruppierungsfächer sowie Übersichtsabschnitte. Eine ausgewählte
  Kindzeile öffnet geschlossene Vorfahren beim Neuaufbau nicht mehr.
- **Seitenleiste:** Klapppfeile von Seiten/Listen/Notizen und Angeheftet sind
  per Tab erreichbar und per Enter/Leertaste bedienbar.
- **Bibliothek:** Unterordner werden beim Öffnen nur einmal eingefügt;
  der Fehler „Item folder-folder:… already exists“ ist korrigiert.
- **QA:** Neue Pflichtsuite `test_klappmechanismen3321.py` bedient die
  tatsächlichen UI-Bindungen und erfasst Tk-Callbackfehler. Datenformat 20
  bleibt unverändert; keine neue Abhängigkeit.
- **Planung:** D01–D06 übernommen, D07 erklärt und offen, D08 umgesetzt.
  Mobile/Toolkit-Probe zurückgestellt, bestehende Bereiche um Drag-and-drop
  erweitern, einzelne Aufgaben in Notizen/Seiten, Hinweise unverändert.

Vertrag und Kontrollmatrix: [Klappkontrolle 3.32.1](docs/69_KLAPPKONTROLLE_3.32.1.md).

## 3.32.0 – 30.09.2026

**Dokumentationsnachtrag, Anwendungscode unverändert:**
[Arbeits- und Featureplanung](../../00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md)
gleicht Arbeitsunterlagen, Versionsanalyse, Übergabe, Konkurrenzquellen und
Bildschirmfotos gegen den Code ab. G04 ist vorhanden, G32/G19 teilweise;
offene Entscheidungen D01–D07, Datenformatprüfung und Performance-Pakete
P01–P07 sind aufgenommen. Zwei passende Suiten erneut grün, Ansichtswechsel
profiliert, Kopien per SHA-256 geprüft. Kein neuer Vollprüflauf oder Release.

Etappe 1 der [Funktionsrecherche vom 30.09.2026](../../00_Arbeitsvorbereitung/Glide_Funktionsrecherche_Ausbau_2026-09-30.md):
schnelle Gewinne. Datenformat unverändert 20. Vertrag:
[docs/68_AUSBAU_3.32.0.md](docs/68_AUSBAU_3.32.0.md).

- **Symbol-Export (G16):** Zeichnung als ICO mit 16, 32, 48 und 256 Pixeln,
  Grund wahlweise durchsichtig – Programmsymbol und favicon.ico auf allen
  Plattformen.
- **Paletten aus Aseprite und Adobe (G20):** `.aseprite` und `.ase` werden
  gelesen (nur die Palette, alles oder nichts).
- **Selbstfüllende Platzhalter (G11):** {{Datum}}, {{Wochentag}}, {{KW}},
  {{Monat}}, {{Jahr}}, {{Uhrzeit}}, {{Morgen}}, {{Gestern}} füllen sich beim
  Anlegen; gefragt wird nur der Rest.
- **Tagesabschluss (G03):** Offenes von heute bekommt einen neuen Tag; der
  Rückblick wandert auf Wunsch in die Tagesnotiz.
- **Mitbehoben:** Leere gerahmte Leiste neben zwei Seitenaktionen;
  „Mein Tag öffnen“ und „Zur Startseite“ standen am Ende des Tagesbeginns
  doppelt.
- **Hänger behoben (dringend):** „Hilfe › Über Glide“ ließ Glide einfrieren,
  bis zum Zwangsbeenden. Die macOS-Berichte vom 29. und 30.09.2026 zeigen die
  Ursache: Ein Menübefehl öffnete ein modales Fenster, während macOS die
  Menüverfolgung noch nicht abgeschlossen hatte; beide warteten aufeinander.
  Betroffen waren 13 Menüpunkte ohne „…“ (etwa Neue Liste, Einfügen,
  Tastenkürzel anzeigen, Über Glide) sowie „Beenden“ mit Rückfrage. Seit
  3.32.0 läuft jeder Menübefehl erst nach dem Schließen des Menüs.
- **Hänger beim Öffnen einer Seite mit Bildern behoben:** Das Fehlerprotokoll
  zeigte `RecursionError` in harmlosen Rückrufen. Nachgestellt stieg die
  Stapeltiefe beim Öffnen, Wechseln und Vergrößern auf 992 (Grenze 1000):
  Die Bildplatzierung maß mit `update_idletasks()`, das den Scroll-Rückruf und
  damit wieder die Bildplatzierung auslöste. Jetzt wird einmal gemessen und
  danach gerechnet; Stapeltiefe 16.
- **Prüfungen im Hintergrund (macOS):** Prüffenster nehmen weder Fokus noch
  Tastatur mehr; man kann während einer Vollprüfung weiterarbeiten
  (`--vordergrund` schaltet das ab).
- **Pflegewerkzeuge** unter `scripts/pflege/`: Versionswechsel, Abgleich nach
  `07_Python-Versionen` mit SHA-256, Messung der Ansichtswechsel, Codeanalyse.
- **Archiv:** Der vollständige Stand 3.31.0 liegt wieder startbar unter
  `07_Python-Versionen/Archiv/Glide-Aufgaben-und-Listen_v3.31.0_Endstand_2026-09-30`
  (`drawing.py` aus 3.32.0 zurückgerechnet).
- **Prüfung:** neue Suite `test_etappe1_332` (55 Suiten).

## 3.31.0 – 30.09.2026

Rückmeldungen vom 29.09.2026 (R1–R11) und die Nachprüfung vom 30.09.2026.
Datenformat unverändert 20. Vertrag:
[docs/66_MODERNISIERUNG_3.30.0.md](docs/66_MODERNISIERUNG_3.30.0.md),
Abschnitte 2.17 und 2.18.

**Nachprüfung 30.09.2026**

- **Warum die Fehler beim Inhaber weiter auftraten:** Die startbare Fassung in
  `07_Python-Versionen` und `build/macos/Glide.app` stammten vom 29.09.2026,
  13:37, also von vor allen Änderungen des Abends. Beide sind jetzt auf 3.31.0
  abgeglichen.
- **Einklappen (R1, zweiter Teil):** Das „…“ beim Überfahren einer Zeile blieb
  beim Einklappen von Seiten und Notizen samt Zeilenbild stehen. Es
  verschwindet jetzt mit dem Baum.
- **Suche (R3):** eigene, vom Design abgesetzte Fläche zusätzlich zum Rahmen.
- **Farben (R8):** Die Glocke der Mitteilungen ist gelb statt türkis; die
  Minimaldesigns bleiben auch beim Hinzufügen farblos.

**Rückmeldung vom Abend 29.09.2026** (Vertrag 66, Abschnitt 2.17)

- **Fenster öffnen sich wieder (R11):** Menübefehle mit „…“ laufen nach dem
  Schließen des Menüs; Dialoge kommen nach vorn. Drei stumme Befehle melden
  sich jetzt. Tiefe Fehler stehen gekürzt, aber vollständig im Protokoll.
- **Editor wie Notion (R4, R5, F1):** Rechtsklick, schwebende Formatleiste,
  Zeilen verschieben, duplizieren und löschen, Umwandeln in eine andere
  Blockart. Neu: Überschrift 4, Aufklappliste, Aufklappüberschrift,
  Hinweisblock und „Mehr › Gliederung“. Notizen schreiben sich mit dem
  Seiteneditor; eine Notiz ohne Punkte zeigt keine leere Liste.
- **Farben nach Bedeutung (R8):** Rot nur Löschen, Grün nur Bestätigen,
  festes Lila für Hinzufügen und Neu, Hinweise gelb, alles andere neutral.
- **Suche (R3):** Rahmen in Akzentfarbe statt Schatten; Klick außerhalb
  schließt.
- **Trackpad quer (R2)** auf der Pinnwand; **Notizbereich** ohne
  stehengebliebenes Bild (R1); **Bild ziehen** ohne Ruckeln (R7);
  **Zeichenfarben** auf die letzten sieben begrenzt (R9); **Referenzbild**
  öffnet den Dateidialog und nimmt JPEG, HEIC und SVG (R10).
- **Tempo (R6):** Übersicht mit Verlauf 3,5 → 8 Bilder/s, Startseite
  9 → 13,5 Bilder/s.
- **Prüfung:** neue Suiten `test_befunde330`, `test_fenster330` (41 Fenster)
  und `test_tempo330`; 54 Suiten.

## 3.30.0 – 25.09.2026

Modernisierung nach dem Aufgabenkatalog vom 25.09.2026 (alle fünf Etappen)
plus die gewählten Punkte aus dem älteren Ideenvorrat. Produktentscheidungen
E-01 bis E-16: alle Empfehlungen, bestätigt am 25.09.2026. Vertrag:
[docs/66_MODERNISIERUNG_3.30.0.md](docs/66_MODERNISIERUNG_3.30.0.md).

**Pixel-Werkstatt (Etappen A, D, E)**

- Zeichen-Editor mit Kontextleiste und sieben Werkzeugen: Pinsel, Füllen,
  Pipette, Linie, Rechteck, Ellipse, Auswahl (B, F, I, L, U, E, S). Zwei Farben
  mit Rechtsklick, Farbleiste mit Palette und zuletzt benutzten Farben,
  eingebettete Vorschau in Originalgröße, Zoom mit Strg+Mausrad und
  Verschieben mit der mittleren Maustaste.
- Rückgängig **je Aktion** statt je Zelle (E-11): ein Pinselzug, eine Form, eine
  Füllung ist ein Schritt, bis zu 50.
- Symmetrie (waagerecht, senkrecht, beide), Muster (Schachbrett, Punktraster),
  Kachelvorschau und Pinsel über den Rand, pixelgenaue 1×1-Linie, Graustufen,
  Deckkraft der Referenz, Auswahl mit Verschieben, Kopieren und Einfügen auch
  zwischen Zeichnungen.
- Flächengrößen 16, 32, 64 und 128 (E-14), Paletten mit Import und Export als
  .gpl/.hex (mitgeliefert nur „Glide 32“, E-15), Farbe in der ganzen Zeichnung
  ersetzen, unbenutzte Farben entfernen, benannte Zwischenstände als Anhang
  (E-12) und PNG-Export in ganzzahligen Vergrößerungen bis 2048 px (E-13).
- Pixelsymbole (16 × 16) für Listen und Ordner (E-09) in Seitenleiste,
  Übersicht und Suche.

**Aufgabenformat 20 (E-02, gebündelt)**

- Punkte: `links`, `blocked_by`, `planned_time`, `time_spent_minutes`,
  `done_at`. Listen und Ordner: `icon`, `archived`, `archived_at`. Zeichnungen
  in 16/32/64 tragen Dokumentversion 2; 128 bleibt Version 1.
- Unveränderte Vorsicherung `liste_vor_format20_<Zeitstempel>.json`. Verweise
  werden beim Kopieren und beim additiven Import neu zugeordnet, Kreise in
  Abhängigkeiten aufgelöst.
- **Glide 3.29 nach der Umstellung nicht mehr starten:** Es hält Format 20 für
  beschädigt, beginnt leer und überschreibt die Datei bei der ersten Eingabe
  (siehe „Ausbau“). Zurück nur über die Vorsicherung.
- Verknüpfte Punkte, echte Abhängigkeiten („wartet auf“, Rückfrage vor dem
  Abhaken), Zeiterfassung je Punkt, Kapazität je Wochentag, Erledigt-Zeitpunkt.
- Archivieren statt Löschen für Listen und Ordner: archivierte Seiten fallen
  aus Planung, Seitenleiste, Startseite und gespeicherten Filtern heraus und
  lassen sich in „Listen und Ordner“ zurückholen.

**Startseite, Suche und Übersichten (Etappe B)**

- Startseite direkt anpassen: Kacheln ziehen oder mit Alt+↑/↓ verschieben,
  ganze Breite, aus- und einblenden. Neue Kacheln „Zeichnungen“, „Angeheftet“
  und „Angeheftete Filter“; eine bestehende Startseite bleibt nach dem Update
  unverändert.
- Seiten und gespeicherte Filter anheften; Block „Angeheftet“ in der
  Seitenleiste. Abschnitte der Seitenleiste einklappbar, „+“ und „…“ beim
  Überfahren von Ordnern.
- Seiten- und Befehlssuche mit Strg/Cmd+O (E-03), zuletzt geöffnete Seiten,
  anklickbarer Pfad über dem Titel, kompakte Eigenschaften im Seitenkopf,
  Rückgängig direkt im Hinweis, Galerie mit Vorschau in „Listen und Ordner“.
- Tagesbeginn und Wochenrückblick als Unterseiten der Startseite.

**Pinnwand als Board (Etappe C)**

- Spaltenboard als dritte Anordnung mit allen Punkten des Bereichs (E-16):
  Gruppieren nach Fälligkeit, Bearbeitungstag, Wichtigkeit, Label, Erledigt
  oder Liste; Ziehen und Alt+←/→ setzen das Feld (E-07: kein neues Statusfeld).
- Dieselbe Gruppierung in Liste und Tabelle (Abschnitte, Ziehen setzt das
  Feld); Tabelle mit verschachtelten Unterpunkten.
- Karteninhalt (Beschreibung, abhakbare Checkliste, Bild) und Kartenfarbe
  (Streifen, Kopf, ganze Karte; Punktfarbe oder erstes Label; Formen im
  Kontrastdesign). Zeichnungen als Karte mit Miniatur und Rückweg.
- Benannte Bereiche, Aufräumen, Strg/Cmd+Enter für eine neue Karte daneben
  (E-08), Ziehpunkt zum Verbinden, Verbindungen mit Beschriftung, Strichart und
  Farbe, Flächenhintergrund (Punkte, Linien, Karo). Aufräumen und
  Bereichsänderungen sind je ein Rückgängig-Schritt.
- Anlageoption „Pinnwand“ (Aufgabenliste, die als Fläche startet).

**Tagebuch, Planung, Oberfläche**

- Tagebuch nimmt alle Inhaltsarten auf (ZF-120): Momentdatum bei der Anlage,
  stabile Sortierung, Tages- und Von-bis-Filter, Datum beim Verschieben bewahrt.
- Vorlagen mit Eingabefeldern (`{{Projektname}}`), Zeitblöcke in „Mein Tag“.
- Eingebetteter Detailbereich (zuschaltbar, E-04), Leerzustände mit einer
  Hauptaktion, zehntes Design „Pixel“ (E-05), Präsentationsmodus für
  Pinnwandbereiche und Notizüberschriften.

**Ausbau am selben Tag** (Rückfrage nach dem ersten Abschluss, alle
Empfehlungen gewählt)

- „Mein Tag“: Zeitblöcke per Ziehen verschieben. Obere Zeilenhälfte eines
  Blocks – davor, untere – danach, „Ohne Uhrzeit“ – ohne Zeit; Alt+↑/↓
  verschiebt um 15 Minuten. Jede Änderung ist ein Rückgängig-Schritt.
- „Präsentation als PDF …“ auf der Pinnwand und „Folien als PDF …“ in der
  Notiz: eine Druckseite mit einer A4-Seite quer je Folie; das PDF erzeugt der
  Druckdialog des Browsers.
- Einfaches Kartenverschieben mit Maus oder Alt+Pfeil lässt sich mit
  Strg/Cmd+Z zurücknehmen.
- Detailbereich mit allen Feldern außer Anhängen: Art, Farbe, Wiederholung,
  Erinnerung, erfasste Zeit, Checkliste bearbeiten, „Verknüpft mit“ und
  „Wartet auf“. Er scrollt; ein Wechsel zu Gruppe oder Überschrift fragt nach,
  wenn Planungsfelder verloren gingen.
- Gismo steht still neben der Hauptaktion leerer Zustände; „Spielereien aus“
  blendet ihn aus.
- Design „Pixel“ mit der Pixelschrift „Pixelify Sans“ (SIL OFL 1.1) für
  Seitentitel und Kachelköpfe. Herkunft und Prüfsummen in
  `resources/fonts/provenance.json`.

**Mitbehoben**

- Verbindungslinien stapelten sich beim Ziehen einer Karte.
- Nach Startseite → neue Zeichnung → Startseite fehlte die Eingabezeile bis zum
  Neustart; nach Zeichnung → Pinnwand-Liste stand sie über der Fläche.
- „Ansicht › Liste › Zur Listenansicht“ meldete aus der Tabelle heraus, es sei
  keine Liste geöffnet.
- Kopfzeile und Zuletzt-geöffnet-Speicherung liefen beim Schließen des Fensters
  in bereits zerstörte Widgets.
- Eine unlesbare oder neuere Speicherdatei überschrieb Glide nach einem leeren
  Start beim ersten Speichern. Jetzt gilt:
  - ein neueres Format öffnet schreibgeschützt;
  - eine unlesbare Datei wird zuerst als `backups/liste_unlesbar_*.json`
    gesichert;
  - eine Rückfallerkennung (`data_format_written`) warnt, wenn eine ältere
    Version zwischendurch geschrieben hat.
- Mit kaputtem JSON scheiterte jedes Speichern an den Formatsicherungen.
- Ein zweites Beenden (etwa Cmd+Q während der Speicherabfrage) leerte
  `window.conf`; der nächste Start verlor die Fensterposition.

**Prüfstand**

- Neue Suiten `test_drawing330.py` und `test_features330.py`; Referenz-Fixture
  `current_v20`, Beispieldaten, Releaseplanung 3.30.0 und Praxisvorlagen neu
  erzeugt. Angepasst: `test_features322` (Übergang der Startseitenkacheln),
  `test_features323` (fünfte Farbschicht), `test_datenintegritaet` (Maskenfelder),
  `test_features329` (bestätigt die neue Importvorschau).
- Vollprüfung am 25.09.2026 auf macOS mit Python 3.14.5: **Exitcode 0**, alle
  52 automatisierten Schritte bestanden
  ([Protokoll](tests/qa-3.30.0/abschluss_2026-09-25/ergebnis.json)).
  Offen bleibt die [manuelle Prüfung](docs/07_QA_BERICHT.md).
- Echtdatenprobe mit einer Kopie des Bestands (6 Seiten, 138 Punkte):
  Umstellung ohne Inhaltsänderung, Vorsicherung bytegleich, Original
  unverändert. 3.29 überschrieb den umgestellten Bestand – daher die
  Schutzmaßnahmen oben.
- `pruefen.py`: Das Momentdatum gewöhnlicher Listen ist ein Anlagetag und wird
  auch im Releaseabgleich relativ zum Exporttag verglichen. Vorher scheiterte
  der Abgleich an jedem Tag nach der Erzeugung – aufgefallen, als ein Lauf
  über Mitternacht ging.
- `test_ui_followup36`: Die Sichtbarkeit der Kartenknöpfe wird wie die
  Innenabstände im stabilen Endzustand gemessen; unter Last meldete eine frisch
  gescrollte Karte „Liste öffnen“ einmal als noch nicht eingeblendet.
- Abschlusslauf nach dem Ausbau am 26.09.2026: **Exitcode 0**, alle 52
  automatisierten Schritte bestanden
  ([Protokoll](tests/qa-3.30.0/ausbau_abschluss_2026-09-26/ergebnis.json)).

**Seitenleiste mit Notizen 29.09.2026** (zweiter Auftrag des Tages, Vertrag
66, Abschnitt 2.16)

- **Einklappen behoben:** Ein Ordner mit der geöffneten Liste ging nach jeder
  Änderung wieder auf (`Treeview.see` beim Neuaufbau). Jetzt klappt nur eine
  neu geöffnete Zeile ihre Ordner auf (`reveal_sidebar_row`). Zugeklappte
  Bibliotheken im Seitenbereich bleiben ebenfalls zu.
- **„Notizen +“** unter den Listen: Notizen ohne Ordner und Notizbücher samt
  Inhalt. Der Pfeil klappt ein, der Titel öffnet die neue Notizübersicht
  (`NOTES_VIEW`). „+“ bietet Tagesnotiz, neue Notiz, Vorlagen und ein neues
  Notizbuch.
- **Ordner in Seiten und Notizen:** „+“ und „…“ beim Überfahren jetzt in allen
  drei Bäumen. Das „+“ einer Bibliothek bietet nur Seiten an; ein Unterordner
  erbt die Art von Bibliothek und Notizbuch.
- **Mitbehoben:**
  - Der Notiztext bekommt bei 860 × 700 wieder mehrere Zeilen, und der
    schwarze Fokusrahmen um ihn entfällt.
  - Seiten- und Notizübersicht fluchten als Tabelle.
  - Ein Doppelklick auf den Titel einer Übersicht öffnete den Dialog der
    zuletzt geöffneten Liste.
  - Unter Tk 9 galt die Liste auf der Startseite als sichtbar, weil der
    Kartenfuß den ausgepackten Rahmen wieder einblendete.
- **Prüfung:** neue Suite `test_notizbereich330` (51 Suiten); `test_reminders`
  und `test_release37` an die Umstellung beim Start angepasst.

**Logo, Suche, Arbeitsfläche, Sicherungen und Startprüfung 29.09.2026**
(Auftrag mit Bildschirmfotos und Antworten auf die Prüfung vom 28.09.2026,
Vertrag 66, Abschnitt 2.15)

- **Logo** aus `20_Grafik_Master` als SVG (`logo.py`, `resources/logo`): in
  der Akzentfarbe links neben Titel und Unterzeile, ab der ersten
  Breitenstufe; in „Über Glide“ und im Startfenster; als Programmsymbol für
  Fenster, Dock und Taskleiste. Unter Tk 8.6 als gezeichnete Fläche.
  `packaging/baue_symbole.py` erzeugt ICO und PNG für die Pakete.
- **Lupe ⌕** in der Kopfzeile für die Suche über Seiten, Punkte und Aktionen
  (Strg/Cmd+O).
- **Startseite ohne Eingabeleiste:** Nach dem Wechsel aus „Mein Tag“ und
  anderen Ansichten stand die Eingabezeile unter den Kacheln.
- **Arbeitsfläche bis ganz unten:** Hinweis und Auswahlleiste stehen im Fuß
  der Karte (`card_foot`); Pinnwand, Notiz, Seite, Zeichnung und Galerie
  reichen bis zur Kante.
- **Sicherungen nur bei Änderung** (SHA-256), dazu je Tag der letzte Stand 14
  Tage lang.
- **Startprüfung:** Ältere Formate werden beim Start umgestellt; eine
  unbekannte Listenart öffnet schreibgeschützt; liegengebliebene
  Zwischendateien werden aufgeräumt.
- **Bytecode** landet auch beim direkten Start im Cacheordner des Systems.
- **Mitbehoben:** Verweise auf endgültig entfernte Punkte blieben bis zum
  nächsten Laden stehen; unter Windows wartet das Ersetzen der Speicherdatei
  bis zu 1,5 s auf eine Sperre.
- **Prüfung:** neue Suiten `test_logo330`, `test_kartenfuss330` und
  `test_speicherlast330` (26.420 Punkte in 0,6 s); `standpruefung.py` mit
  den Regeln R9 bis R11.

**Tk 9, Bilder in Seiten und feste Bestandteile 27.09.2026**
(Entscheidungsvorlage vom 27.09.2026, Vertrag 66, Abschnitt 2.14)

- **Bilder in Seiten:** einfügen über „Bild“, „/“ oder Ziehen aus
  Finder/Explorer; links oder rechts mit Text daneben oder mittig in eigener
  Zeile; verschieben per Ziehen, Größe an der Ecke, Rechtsklickmenü, Entf und
  Rückgängig. Bilder sind Anhänge der Seite; `rich_note.images` additiv in
  Format 20. Markdown-Export legt einen Bildordner an.
- **Tk 9:** neue Datei `image_preview.py` – Vorschauen über `nsimage`
  (macOS, auch JPEG/HEIC/WebP), SVG, rationale Skalierung, Windows über WIC;
  Zwischenspeicher für Galerie, Seiten und Pinnwandkarten.
- **Systemmitteilungen** (Stufe B) über `tk sysnotify`, Einstellung
  `system_notifications`, standardmäßig aus; Ansicht › Systemmitteilung
  testen.
- **Ziehen aus Finder/Explorer:** tkinterdnd2 0.6.3 (MIT) unter
  `src/glide/vendor`, Entscheidung in `docs/decisions/ABHAENGIGKEIT_TKDND.md`.
- **„/“-Befehle** beim Anlegen eines Punkts, mit Vorschlagszeile und Tab.
- **Wiederkehrende Checkliste** (`recurring_checklist`, additiv in Format 20)
  und „Alle Punkte wieder öffnen“.
- **Feste Bestandteile:** kein Ordnerpfad über dem Titel (MO-020 entfällt);
  Kopfzeile mit fester Höhe; Werkzeugleiste und Fußbereich halten Ober- und
  Unterkante der Fläche in jeder Ansicht; die Auswahlleiste ersetzt den
  Hinweis statt die Liste zu kürzen; Werkzeuge von Seite, Zeichnung und
  Galerie stehen in der Leiste über der Fläche.
- **Globale Suche** mit runden Ecken und Schlagschatten, unter der Kopfzeile.
- **Tempo:** Speichern 3,3× schneller (JSON in einem Stück, leere
  Verlaufswerte, gemerkte Titelkürzung); das Fenster erscheint sofort.
- **Handbuch:** Bilder in Seiten, „/“-Befehle, Auswahlleiste, wiederkehrende
  Checkliste, Systemmitteilung.
- **Probedaten:** „Rundgang“ (`tests/tools/rundgang.py`,
  `05_Probelisten_Testdaten/Glide-Rundgang_3.30.0.glidebackup`).
- **Mitbehoben:** „Seiten“ in der Seitenleiste nahm beim Designwechsel die
  Farbe nicht an; die Grenze der Pinnwand-Hintergrundpunkte zählt jetzt auch
  die Randreihen; ein einmaliger Befund in `test_glide` wartet jetzt auf den
  stabilen Endzustand.
- **Prüfstand:** Vollmodus im dritten Lauf mit Exitcode 0, 62 Schritte, 47
  Suiten (`tests/qa-3.30.0/tk9_bilder_2026-09-27`).
- **Prüfung:** neue Suiten `test_bilder330` und `test_festlayout330`;
  `test_workspace310`, `test_features315`, `test_features330`,
  `test_rueckmeldung330` und `test_paketierung330` an das feste Layout, die
  Kennzahlenkürzung und das Bundle angepasst.

**Kompression, Bibliothekstabelle und Notizbuch 27.09.2026**

- Titel von Listen, Seiten und Ordnern höchstens 40 Zeichen.
  - Die Titelfelder zählen mit.
  - Ältere, längere Titel kürzt Glide beim nächsten Start; vorher sichert es
    die Datei und meldet danach die gekürzten Titel.
- Keine eigene Beschreibungszeile mehr: Eine Beschreibung unter 50 Zeichen
  steht neben den Kennzahlen, Systemansichten zeigen dort ihren Untertitel.
- Seiten- und Listenbereich klappen mit Pfeilen ein, stehen enger
  beieinander und tragen keine Symbole mehr.
- Bibliothek als sortierbare Tabelle: Titel, Beschreibung, Farbe, Labels,
  Aufgaben, Erstellt.
- „Tagebuch“ heißt überall „Notizbuch“; neue Einträge heißen „Tagesnotiz ·
  Datum“.
- Einheitliche Innenränder für Notiz, Seite, Zeichnung und Galerie.
- Hinweise:
  - Sie stapeln sich nicht mehr, jeder Klick schließt sie.
  - Sie wandern nicht mehr sichtbar ins Fenster.
- Einstellungen: „Akzentfarbe der Oberfläche“ ohne Zusatz.
- Behoben: doppelter, versetzter Leertext über einer Notiz.
- Neue Suite `test_kompression330`.
- Vollmodus: **Exitcode 0**, alle 60 automatisierten Schritte mit 45 Suiten
  ([Protokoll](tests/qa-3.30.0/kompression_2026-09-27/ergebnis.json)).

**Aufräumen, Seitenbereich und Galerie 27.09.2026**

- Aktionsleiste nur bei Auswahl:
  - eine Reihe mit Anzahl, Wichtigkeit, Fällig, Einplanen, Labels und
    Löschen statt zwölf fester Knöpfe;
  - alles Übrige bleibt im Menü, im Rechtsklick und als Kürzel.
- Kopfzeile nur mit Symbolen: ⌘ Aktionen, ↯ Schnellerfassung (vorher „+“ wie
  „Neue Liste“), ⍾ Benachrichtigungen mit Zahl. Kennzahlen stehen nur noch
  unter dem Titel.
- Seitenleiste:
  - Die Knöpfe unter dem Listenbaum entfallen; das „+“ neben „Listen“ öffnet
    das Anlegen-Menü samt Import.
  - Listenzeilen zeigen „…“ beim Überfahren.
- Liste · Tabelle · Pinnwand als fester Umschalter.
- Pinnwand:
  - Aktionen und Schalter in einer Zeile;
  - Spalten teilen sich die Breite;
  - aktive Schalter in der Auswahlfarbe statt Grün.
- Seiten:
  - eigener Bereich „Seiten +“ mit Bibliotheken;
  - Vorlagen: Bericht, Besprechung, Projektseite und eigene;
  - eigenes Format `.glidepage` mit Aufgaben, Labels und Anhängen.
- Neue Listenart „Galerie“: Bilder als Anhänge, Kachelraster, Großansicht
  mit Titel und Notiz. JPEG und HEIC erhalten die Vorschau unter macOS über
  `sips`.
- Textlogo in der Akzentfarbe; die Akzentfarbe steht oben in den
  Einstellungen.
- Behoben:
  - Kästen hinter Text in „Startseite anpassen“;
  - Gismos farbiges Rechteck;
  - die „Erledigt!“-Fahne über dem Suchfeld;
  - Eingabezeile auf einer Seite nach einer Zeichnung;
  - „Noch keine Aufgaben“ im Kopf einer Zeichnung;
  - Aufgabenmarken einer kopierten oder importierten Seite.
- Neue Suite `test_aufraeumen330`.
- Vollmodus: **Exitcode 0**, alle 59 automatisierten Schritte mit 44 Suiten
  ([Protokoll](tests/qa-3.30.0/aufraeumen_2026-09-27/ergebnis.json)).

**Seiten und Ordnertypen 26.09.2026**

- Neue Seitenart „Seite“, gedacht vor allem für KI-Berichte:
  - Lesen: ruhige Lesespalte, endlos scrollend;
  - Schreiben: Markdown-Kürzel, „/“-Menü, Enter setzt Listen und Aufgaben fort;
  - Markdown aus Zwischenablage oder Datei wird zur Seite (Überschriften,
    Listen, Tabellen, Zitate, Code, Links);
  - Export als Markdown.
- Aufgaben in Seiten sind echte Glide-Punkte: abhaken, alle Punktdetails,
  „Mein Tag“, Kalender, Papierkorb samt Rückgängig.
- Übersicht „Seiten“ in der Seitenleiste mit Favoriten, Zuletzt und allen
  Seiten.
- Ordnertypen: Ordner (bisher Standard), Bibliothek (neu, darin entstehen
  Seiten), Notizbuch (bisher Tagebuch).
- Neues Modul `page_markdown.py`, neue Suite `test_seiten330`.
- Kopfzeile: Der Titel rechnet den Innenabstand der Beschriftung mit ein
  (am Sonntag war er 5 px zu schmal, gefunden von `test_mindestgroesse330`).
- Vollmodus: **Exitcode 0**, alle 58 automatisierten Schritte mit 43 Suiten
  ([Protokoll](tests/qa-3.30.0/seiten_2026-09-27/ergebnis.json)).

**Zweite Rückmeldung 26.09.2026: Bedienbarkeit, Farben, Tempo**

- Punktdetails und erweiterte Eingabe:
  - Mit Hintergrundverlauf blieben sie klein und reagierten nicht, weil Tk
    endlos neu anordnete. Behoben.
  - Dialoge haben jetzt einen statischen, zum Verlauf passenden Grund.
- Farben nur mit Bedeutung:
  - Grün für die Hauptaktion, Rot für Löschen und Leeren;
  - sonst neutral grau.
- Kennzahlen unter dem Titel ohne Kasten.
- „Startseite anpassen“ unter den Kacheln.
- Ohne Funktion ausgeblendet: Eingabezeile in abgeleiteten Ansichten und im
  Papierkorb, Knopfleisten im Papierkorb.
- Leertexte brechen um; „Notiz“ unter der Notizeingabe entfernt.
- Pinnwand linksbündig; Auswahlfelder nicht mehr abgeschnitten.
- Zeichenfläche: Um die Zeichnung herum steht die Kartenfarbe.
- „Erledigte Punkte löschen“ überall erreichbar, jetzt über den Papierkorb.
- Tempo:
  - Scrollen mit Verlauf etwa dreieinhalbmal, ohne Verlauf doppelt so
    schnell; Startseite und Listen deutlich schneller;
  - Verlaufsbild und Rückgängig-Speicher brauchen weit weniger Speicher;
  - Schnellstart `glide_start.py` (ab dem zweiten Start rund 0,5 s schneller).
- Konzept „Seiten wie Notion“ als Entscheidungsvorlage in der
  Arbeitsvorbereitung.
- Vollmodus: **Exitcode 0**, alle 57 automatisierten Schritte mit 42 Suiten
  ([Protokoll](tests/qa-3.30.0/rueckmeldung2_2026-09-26/ergebnis.json)).

**Rückmeldung zu den Hintergrundverläufen 26.09.2026**

- Absturz behoben: Mit Verlauf, Startseite und schmalem Fenster stürzte Glide
  beim Start ab (Tk, `XMoveResizeWindow`).
  - Ursache waren Hintergrundbilder mit dem Bindtag ihres Rahmens.
  - Sie leiten jetzt nur noch Mausereignisse weiter.
- Milchglas: Kacheln, Listen und Fenster nehmen die weichgezeichnete Farbe
  des Verlaufs hinter sich an (im Glasdesign kräftiger), mit 4,5:1 für die
  Schrift. Die Kontrastdesigns bleiben deckend.
- Hinweistexte auf dem Verlauf ohne Kasten: Die Schrift weicht im eigenen
  Farbton aus, die Pille ist nur noch der letzte Ausweg.
- Glas-Kacheln: Der Glanz bleibt im oberen Innenrand; hinter Texten
  erschienen dadurch helle Kästen.
- Aufgeräumt:
  - Verlauf als Knopf ◷ in der Kopfzeile statt Seitenleistenzeile; die Seite
    steht auf einer Karte;
  - „In Bearbeitung“ als Abschnitt in „Mein Tag“ statt Seitenleistenzeile;
  - kein Klapppfeil mehr bei „Listen“.
- Kopfzeile: feste Knopfreihenfolge. Das Zahnrad wanderte nach einem
  Breitenwechsel nach links.
- Gleiche Unterkanten: Pinnwand, Zeichenfläche und Verlauf standen 14 Pixel
  tiefer als die Seitenleiste, die Startseite 4 Pixel höher.
- Zeichenfläche:
  - ruhig beim Umschalten (Statuszeile mit fester Höhe, Kontextleiste mit
    reservierten Zeilen);
  - ein Klick neben die Auswahl hebt sie auf, dazu der Knopf „Aufheben“;
  - Verschiebe-Zeiger über der Auswahl.
- Neue Suite `test_rueckmeldung330`; `test_hintergrund330` erweitert.
- Vollmodus: **Exitcode 0**, alle 57 automatisierten Schritte mit 42 Suiten
  ([Protokoll](tests/qa-3.30.0/rueckmeldung_2026-09-26/ergebnis.json)).

**Hintergrundverläufe 26.09.2026**

- Je Design fünf moderne Hintergründe, zur Wahl in den Einstellungen (mit
  Vorschau) und unter „Ansicht › Oberfläche › Hintergrund“; standardmäßig
  aus.
  - Mesh-, Nordlicht- und Körnungsverläufe;
  - im Pixel-Design Pixelblöcke mit schwachem Dithering;
  - im Kontrastdesign kaum sichtbare Tönungen.
- Lesbarkeit: Unter Titel und Unterzeile bleibt der Verlauf leiser (4,5:1
  gesichert). Andere Texte bekommen bei Bedarf eine Milchglas-Pille.
- Liquid Glass: Karten nehmen einen Hauch der Verlaufsfarbe an, ihr oberer
  Lichtverlauf spiegelt sie.
- Technik:
  - Neues Modul `backdrop.py`, nur Standardbibliothek.
  - Gerechnet wird im Hintergrund-Thread und im System-Cache zwischengespeichert.
  - Titel, Unterzeile, Kennzahlen, Pfad und Hinweis sind jetzt Canvas-Text
    (`CanvasLabel`).
- Neue Suite `test_hintergrund330`.
- `CanvasLabel` misst wie ein Tk-Label, damit Kopfzeile und Mindestgrößen
  gleich bleiben.
- Vollmodus: **Exitcode 0**, alle 56 automatisierten Schritte mit 41 Suiten
  ([Protokoll](tests/qa-3.30.0/hintergrund_2026-09-26/ergebnis.json)).

**Dialoge, Kontrast, Raster, Paketierung 26.09.2026**

- Dialoge bei Mindestgröße, in mittlerer und großer Schrift:
  - Die Mindestbreite deckt immer den Inhalt.
  - Kalenderzellen kürzen nach Pixeln und zeigen „+N“.
  - Der Kalenderknopf neben dem Datum und die Aufklapppfeile passen.
  - Mitbehoben: „In Liste verschieben …“ stürzte beim Öffnen ab (`KeyError`).
- Kontrast nach WCAG AA in allen zehn Designs:
  - Die Grundpalette trägt kontrastfeste Schriftfarben: „Hell“ mit tieferem
    Grün, Orange, Türkis, Blau, Lila, Rot und Platzhalter; „Dunkel“ mit
    helleren Platzhaltern, Lila, Rot und Blau.
  - Gemischte Designs werden zur Laufzeit im eigenen Farbton nachgezogen.
  - Knopfschrift bleibt in jedem Zustand lesbar.
  - Neue Suite `test_kontrast330` mit rund 13.700 gemessenen Paaren.
- Stundenraster:
  - In Fenstern unter 900 px steht es statt der Liste.
  - Aus jeder Liste auf „Mein Tag“ in der Seitenleiste ziehen plant ein.
- Paketierung (Vorstufe):
  - Kennungen `de.shaye.glide` / `Shaye.Glide`.
  - Windows-Anmeldung mit AppUserModelID.
  - `packaging/macos/baue_app.py` (Entwicklungsbundle, ad hoc signiert).
  - `packaging/windows/verknuepfung_anlegen.ps1`.
  - Neue Suite `test_paketierung330`.
- Vollmodus: **Exitcode 0**, alle 55 automatisierten Schritte mit 40 Suiten
  ([Protokoll](tests/qa-3.30.0/kontrast_paketierung_2026-09-26/ergebnis.json)).

**Kleine Fenster 26.09.2026**

- Höhenstufen bei niedrigem Fenster:
  - Die Aktionsreihen schrumpfen auf eine Reihe (Liste leeren, Löschen,
    Wichtigkeit, Fällig).
  - Die Seitenleiste zeigt „Ordner“, „Bearbeiten“ und „–“ in einer Zeile.
  - „Liste importieren“ bleibt im Menü „Datei“.

  Bei 860 × 700 zeigt die Liste rund 8 statt 6 Zeilen, der Listenbaum 5 bis 6
  statt 2 bis 3.
- Nichts mehr angeschnitten: Kennzahlen unter dem Titel nur als ganze Chips,
  Unterzeilen mit „…“; die Kennzahlen rechts oben brechen um, statt dem
  Titel den Platz zu nehmen.
- Nichts mehr gequetscht: „Pinnwand“ und „Liste“ in der Suchzeile, „Raster“
  in der Pinnwandleiste bei großer Schrift. In der Tabelle weichen ganze
  Spalten nach Priorität, der Titel behält mindestens 220 px.
- „Listen und Ordner“ und „Vorlagen“: Knöpfe fließen in Spalten statt
  einzeln untereinander.
- Gruppierte Tabelle: Überschriften bleiben auch bei Spaltensortierung; sortiert
  wird innerhalb jeder Überschrift.
- Mitbehoben: Der Seitentitel wurde nach einem Wechsel der Schrift- oder
  Fenstergröße mit veralteten Breiten gekürzt.
- Neue Suite `test_mindestgroesse330.py`: 75 Ansichten in fünf Kombinationen
  aus Design, Schriftgröße und Fenstergröße ohne Befund. Am vorherigen Stand
  fand sie 24 Befunde.
- Vollmodus: **Exitcode 0**, alle 53 automatisierten Schritte mit 38 Suiten
  ([Protokoll](tests/qa-3.30.0/mindestgroesse_2026-09-26/ergebnis.json)).

**Dritter Ausbau 26.09.2026** (die bekannten Grenzen des Vertrags)

- Stundenraster: Jeder Punkt aus der Liste von „Mein Tag“ lässt sich ins
  Raster ziehen, auch ohne Uhrzeit oder aus dem Eingang. Eine gestrichelte
  Linie zeigt die Startzeit; der Punkt wird für den angezeigten Tag
  eingeplant.
- Gruppierte Tabelle: Nummern aus der Liste in der Baumspalte und
  Zwischenüberschriften als Trennzeilen, solange nicht nach einer Spalte
  sortiert wird.
- Pixelschrift unter Linux: Der Schriftordner wird über Fontconfig
  (`FcConfigAppFontAddDir`) nur für den laufenden Prozess registriert.
- Mitbehoben:
  - „Pinnwand öffnen“ aus Menü und Kontextmenü meldete in der Tabelle
    „Zuerst eine Liste oder einen Ordner öffnen“.
  - Die Baumspalte der Tabelle zeigte den Titel abgeschnitten ein zweites
    Mal.
- Vollmodus: **Exitcode 0**, alle 52 automatisierten Schritte
  ([Protokoll](tests/qa-3.30.0/ausbau3_2026-09-26/ergebnis.json)).

**Zweiter Ausbau 26.09.2026**

- Detailbereich mit Anhängen: anfügen, öffnen, entfernen. Dieselbe Datei
  kommt nicht doppelt.
- Druckseite und Folien zeigen Zeichnungskarten als pixelscharfes PNG.
- Stundenraster in „Mein Tag“ (Knopf „Raster“): Blöcke nach Uhrzeit, Ziehen
  im 15-Minuten-Takt, Doppelklick öffnet den Punkt.
- Gruppierte Listen behalten Zwischenüberschriften als Trennzeilen und die
  Nummern der ungruppierten Liste.
- Windows-Prüfpaket (`tests/tools/windows_vollpruefung.cmd`/`.ps1`) mit
  Anleitung; Entwurf des Produktdatenblatts 3.30 mit Store-Texten.
- Lasttest `test_ui_followup36` mit vier parallelen Läufen: kein
  Datenunterschied. Die Knopfprüfung scheiterte, weil die Karte unter Last
  nach einmaligem Scrollen teils außerhalb des Sichtbereichs lag. Der Test
  scrollt jetzt vor jeder Messung neu; die zweite Lastrunde war 4/4 grün.
- Vollmodus nach dem zweiten Ausbau: **Exitcode 0**, alle 52 automatisierten
  Schritte ohne parallele Last
  ([Protokoll](tests/qa-3.30.0/ausbau2_2026-09-26/ergebnis.json)).

**Dokumentabgleich 26.09.2026** (keine Programmänderung)

- Sitzungsprotokoll 24.–26.09.2026 als
  [docs/67](docs/67_SITZUNGSPROTOKOLL_2026-09-24_BIS_2026-09-26.md) und als
  Auswertung für die Arbeitsvorbereitung
  (`00_Arbeitsvorbereitung/Glide_Sitzungsprotokoll_und_Lehren_2026-09-24_bis_26.md`).
- Abgelöste Berichte 62–64 vom 24.09.2026 archiviert, Verweise nachgeführt.
  Die Prüfprotokolle 3.25–3.27 liegen jetzt in `50_Ablage/QA/`.
- Berichtigt:
  - Release-Checkliste (Stand 3.28/Format 18);
  - `src/glide/README.md`;
  - Arbeitsbegleiter (zehn Designs);
  - die widerlegte Aussage „ältere Fassungen lehnen Format 20 sichtbar ab“;
  - Überholt-Hinweise in den Planungs- und Recherchedokumenten.

  Alle Vorfassungen liegen als `…_3.30.0_vor_Dokumentabgleich_2026-09-26` im
  Archiv.

## Planung nach 3.29.0 – Wettbewerbsrecherche und Aufgabenkatalog – 25.09.2026

Keine Programmänderung.

- Online-Recherche: Startseite und Modernisierung mit Notion verglichen,
  Pinnwand mit Trello, OneNote, FigJam und Microsoft Planner, Aufgaben und
  Ordner mit Notion, der Zeichenablauf mit Affinity. Für Glides
  Pixel-Design-Nische kamen Aseprite, Pixelorama und Lospec hinzu.
- Arbeitsvorbereitung und Aufgabenkatalog mit 44 neuen Paketen in fünf Etappen.
  Enthalten sind Datenklassen, Einstiegspunkte im Code, Abnahmekriterien und
  16 offene Produktentscheidungen. Die Dateien liegen in
  `00_Arbeitsvorbereitung/`; die Projektübergabe nennt sie.
- Die Aufgabensammlung Zeichenfläche verweist bei ZF-200 und ZF-300 auf die
  daraus abgeleiteten Pakete; ihre Kennungen bleiben gültig.

## 3.29.0 – 24.09.2026

Erste produktive Stufe der Zeichenfläche (Etappe 1 der Integration). Die
Zeichnung ist eine eigene, unveränderliche Listenart im normalen Glide-Bestand.

- Neue Listenart **Zeichnung** neben Aufgaben und Notiz. Anlage über „Neue
  Liste …“ (Listenart „Zeichnung“), „Datei → Neu anlegen → Neue Zeichnung“ und
  die Kontextmenüs von Listen und Ordnern – auch in Tagebuchordnern mit
  Momentdatum.
- Die Zeichenfläche liegt **eingebettet in der Seitenanzeige** statt in einem
  eigenen Fenster: Pinsel 1×1 bis 8×8, Füllen, Pipette, Farbe mit Spektrum und
  Direkteingabe, Zell-Undo/-Redo (20), Zoom, Raster, Treffer-Vorschau und ein
  Tastaturcursor (Pfeiltasten, Leertaste, B/F/I, 1/2/4/8, +/−/0, G, R, C).
  Der Zoom folgt der verfügbaren Fläche, bis manuell gezoomt wird.
- **Autosave** bündelt Striche nach einer kurzen Pause (700 ms) und sichert
  offene Striche vor Seitenwechsel, Export, Backup, jeder weiteren Änderung und
  Programmende. Der Status „Ungespeichert / Speichert / Gespeichert / Speichern
  fehlgeschlagen“ steht unter der Fläche; ein Schreibfehler lässt die Datei
  unverändert.
- **PNG-Referenz** als lokaler Anhang der Zeichnungsseite mit Rahmenwahl
  (füllen/einpassen, Größe, Versatz). „Nur als Referenz“ zeigt das Bild blass
  hinter weißen Zellen; „Nachzeichnen“ erzeugt nach Vorschau ein Zellmodell mit
  höchstens 64 Farben. Nachzeichnen, Ersetzen durch Import, Leeren und
  Referenzwechsel legen einen vollständigen Vorher-Snapshot an (Rückgängig,
  zusätzlich „Nachzeichnung zurücksetzen“).
- Export als Glide-SVG und JSON; Import als neue Zeichnungsseite (Standard) oder
  ausdrücklich ersetzend.
- **Aufgabenformat 19** mit Feldern `drawing` und `drawing_reference`, zentraler
  Typregistrierung und unveränderter Vorsicherung
  `liste_vor_format19_<Zeitstempel>.json`. Unbekannte Listenarten eines
  Format-19-Bestands werden sichtbar abgelehnt statt still zu Aufgaben zu
  werden.
- Zeichnungen reisen durch Duplizieren, Papierkorb, Wiederherstellung,
  Komplett-, Teil- und App-Backup, Vorlagen und das Austauschformat. Beim
  additiven Import folgt der Referenzverweis den neu vergebenen Anhangskennungen.
- Listen- und Ordnerart sind nach der Anlage fest; der Bearbeiten-Dialog zeigt
  sie nur noch an.
- Der Änderungsverlauf speichert für Zeichnungen nur eine Prüfsumme und meldet
  „Zeichnung geändert“. Aufeinanderfolgende Änderungen derselben Seite innerhalb
  von zehn Minuten bilden einen Eintrag (gilt auch für Notizen).
- Globales Rückgängig nimmt Zellstriche nicht mehr über einen älteren,
  unabhängigen Stand mit zurück; nur Strukturaktionen der Zeichnung stellen ihr
  Zellmodell zurück.
- Zeichnungen nehmen keine Punkte auf: Schnellerfassung, Verschieben,
  Ablegen, CSV-/ICS-Import und Pinnwand-Zielauswahl schließen sie aus.
- Gemeinsame Bildfunktionen liegen in `src/glide/drawing_image.py`; Bedienprobe
  und App verwenden dieselbe Rahmen- und Nachzeichnerlogik.
- Prüfstand: neue Suite `test_features329.py`, Referenz-Fixture `current_v19`,
  Releaseplanung 3.29.0 und neu erzeugte Beispieldaten mit Zeichnung. Die fünf
  vorbestehenden roten Befunde sind behoben: Fixture-Zuordnung Format 17/18,
  tagesabhängiges Momentdatum im Vorlagenerzeuger sowie drei veraltete
  UI-Erwartungen (Schalter „Nur offene Punkte“, Ansichtsumschalter,
  plattformabhängige Menüzeile). Der Vollmodus vergleicht reproduzierte Beispiel-
  und Releasedaten jetzt ohne die Listenzeitpunkte `created_at`/`updated_at`.

Nachbesserung und Abnahmeprüfung am selben Tag:

- Das Farbspektrum öffnet immer mit voller Helligkeit; bei Schwarz als
  aktueller Farbe wirkte es zuvor wie ein schwarzer Kasten. Der
  Helligkeitsregler hat einen sichtbaren Schieber.
- Scrollleisten erscheinen nur noch, wenn die Fläche größer als die Ansicht
  ist. Zuvor rechnete der Scrollbereich mit der Außenbreite einschließlich
  Fokusrahmen; es blieben wenige Pixel zu scrollen, und die Fläche verrutschte
  beim Zeichnen.
- Scheitert das Speichern beim Verlassen einer Zeichnung, erscheint einmalig
  eine Warnung.
- Zusätzliche Abnahmetests: Wiederherstellung in leerem Datenordner,
  Teilbackup eines Zweigs, beschädigtes Archiv, gescheiterte Vorsicherung,
  unveränderter Format-18-Inhalt, Verschieben, Rahmen- und
  Nachzeichnungsdialog, Farbdialog, Scrollbereich.
- `test_ui_followup36` misst die Innenabstände der Bestandskarten nach Resize
  erst im stabilen Endzustand; unter Last war die Messung zu früh.
- Begriffsabgrenzung im Dokumentationsindex; die bereits angewendeten
  Reparaturskripte aus dem Repository-Stamm liegen im Werkzeugarchiv.

Details: [Zeichnungsseite 3.29](docs/65_ZEICHNUNGSSEITE_3.29.0.md).

## Vorarbeit zu 3.29.0 – isolierter Zeichenflächenkern – 24.09.2026

- Repository-README für GitHub neu aufgebaut: Projektstatus, Funktionsumfang,
  Schnellstart, lokale Datenhaltung, Testweg, Repository-Struktur,
  Zeichenflächenstatus und der noch offene Lizenzstatus sind jetzt klar
  getrennt und direkt verlinkt.
- Existenzrecht aller aktiven Dokumentdateien sowie der Archivklasse erneut
  geprüft. Vier historische Wegweiser, eine doppelte Pflegekurzfassung und der
  abgelöste Reiterentwurf wurden verlustfrei archiviert; aktive Verweise führen
  nun direkt zum maßgeblichen Vertrag oder Archivziel.
- Veraltete Laufzeit- und Plattformhinweise in den Requirements und
  Prüfwerkzeugen korrigiert. Der neue Bericht 64 führt jede aktive Datei einer
  begründeten Bestandklasse zu und dokumentiert die Archivdubletten-Regel.
- Archiv- und Dokumentationsprüfung abgeschlossen: sieben veraltete
  Standangaben korrigiert, 44 historische Langdokumente, Dateien beziehungsweise
  Arbeitsordner aus aktiven Bereichen verschoben und die aktuellen Einstiege
  auf eine kurze Lesereihenfolge reduziert. Alte 3.21.4-Probedaten,
  Vorlagenanleitung und Produktdatenblatt liegen jetzt im Archiv.
- UI-unabhängiges 128-×-128-Zellmodell mit höchstens 256 konkreten Farben,
  vier Pinselgrößen, 4er-Füllung, Pipette und zellweisem 20er-Undo ergänzt.
- Kanonisches `hex8-row-v1`-JSON und ein streng validiertes Glide-SVG-Profil
  mit eingebettetem Modell, Modell-/Grafikhash und statischen Rechteckläufen
  umgesetzt.
- Isolierte Tk-Bedienprobe mit Raster, Zoom, Treffer-Vorschau, JSON-/SVG-
  Dateidialogen und optionaler PNG-Referenz ergänzt. Lokale PNGs bis
  4096 × 4096 Pixel lassen sich auf die feste Referenzebene einpassen,
  zuschneiden, vergrößern und verschieben.
- Zeichenfläche horizontal und vertikal zentriert, Abbruch des ersten Strichs
  beim anfänglichen Fokuswechsel behoben und sichtbares Farbspektrum ergänzt.
  Direkte Eingaben akzeptieren jetzt auch `RGB`, `RRGGBB` und Tk-Farbnamen und
  werden vor dem Zeichnen eindeutig als `#RRGGBB` validiert.
- Der PNG-Ablauf bietet nach dem Rahmen die getrennten Wege „Nur als Referenz“
  und „Nachzeichnen“. Der Nachzeichner erzeugt vor der Übernahme eine
  bearbeitbare 128-×-128-Vorschau mit Weiß als Hintergrund und höchstens 64
  Farben einschließlich Weiß. Weißtoleranz und Vorschau-Raster sind
  einstellbar. Eine 4-×-4-Teilflächenabtastung erhält dunkle Konturen gezielt,
  sobald sie mindestens ein Drittel einer logischen Zelle abdecken.
- Eine kanonische Zeichenflächen-Übergabe dokumentiert Entscheidungen,
  Umsetzungsschritte und Gründe, gelöste und offene Probleme, Dateiverträge,
  Prüfbelege sowie die sichere Fortsetzungsreihenfolge für einen neuen Agenten.
- Automatisierte Vertragstests prüfen Rundlauf, schnelle Striche,
  4er-Nachbarschaft, Undo-Grenze und die Ablehnung aktiver SVG-Inhalte.
- Noch keine Integration in `ListApp`, keine Datenmigration und keine Änderung
  des produktiven Aufgabenformats 18.

Details: [isolierter Zeichenflächenkern](docs/61_ZEICHENFLAECHE_ISOLIERTER_KERN_2026-09-24.md).

## 3.28.0 – 23.09.2026

Der undokumentierte UI-/UX-Zwischenstand 3.27.0 wurde als Ausgangsbasis in den
kanonischen Quelltext übernommen. 3.28.0 ergänzt:

- Tagebuch-Ordner und datierte Notizseiten mit Favorit, Stimmung, Ort,
  Momentdatum, Schreibimpulsen, Suche und Datumssortierung;
- Vorlagen für Tagesnotiz, Dankbarkeit, Wochenrückblick und Jahresordner;
- Datenformat 18 mit `folder_kind`, `journal`, Referenz-Fixture und unveränderter
  Originalsicherung vor der ersten Migration;
- Gismo-Zustände Sättigung, Energie und Vertrauen samt Füttern, Spielen, Ruhen
  und begrenzter täglicher Abnahme;
- eine funktional lesbarere Pinnwandvorschau mit Raster, Kartenhierarchie und
  Verbindungen;
- kontinuierliches automatisches Scrollen bei gedrücktem Mausrad und
  Zeigerbewegung;
- konturlose Menüschaltflächen, kleinere Mindestbreite der Eingabefelder,
  priorisierte Aktionen bei Minimalbreite, verdichtete Notizwerkzeuge und eine
  gegliederte Punktmaske;
- neutrale Farbgebung für nachrangige Kopf- und Fußaktionen; semantische Farben
  bleiben für Bestätigung, Gefahr, Fälligkeit und Wichtigkeit reserviert.
- kein weißer Startseiten-Neuaufbau mehr nach Gismos `Füttern`, `Spielen` oder
  `Ruhen`: Nur die drei Pflegebalken und Gismos Zeichenzustand werden lokal
  aktualisiert; ein Dopamin-Regressionsfall sichert den Pfad ab.

Recherchebezug, lokale Grenzen, Migration und Prüfstand:
[Tagebuch und UI 3.28](docs/59_TAGEBUCH_UND_UI_3.28.0.md) und
[QA-Bericht](docs/07_QA_BERICHT.md).

## 3.26.0 – 21.09.2026

Die Nachbesserung des zuvor unvollständigen Standes ergänzt die folgenden Funktionen. Prüfergebnisse und Plattformgrenzen sind im QA-Bericht dokumentiert.

- Doppeltes Eingangssymbol in Mein Tag entfernt; die native Aufklappfunktion bleibt bestehen.
- Große oder extrem lange Pinnwände erhalten eine beschriftete verdichtete Vorschau; keine erfundenen Karten bei leerer Pinnwand und keine inneren Trennlinien.
- Vorhandene Verbindungen zwischen ausgewählten Karten übernehmen die gewählte Verbindungsart. Die Ziellistenauswahl einer Ordnerpinnwand und die Mutation selbst sind auf deren Listen begrenzt.
- Auswahlrechteck mit vollständiger Einschließung; optionales Ausrichten an Kartenkanten und Mittellinien, sichtbare Hilfslinien.
- Gismo als Standardname, höhere Standardposition, kontextbezogene Sätze, Füttern, Hover-Reaktion und eigener Schalter für Spielereien.
- Tatsächlicher Monatsname in der Kalenderkachel; normale Aktionsbuttons ohne Dialogellipsen. Kompakte Symbole für Aktionen, Anzeige und Erweitert; Fortschritt im kleinsten Kopfzeilenmodus ausgeblendet.
- Minimaldesigns mit wählbarem Akzent und Kontrastgrau; aktive und berührte Buttonflächen mit passender Outline.
- Neue Listenart Notiz mit Aufgabenbereich und Rich-Text-Editor, Formatspannen, Links, Zeitstempeln und lokalem Undo/Redo. Formatierte Inhalte werden gespeichert, dupliziert und in Backups/Austauschdateien übernommen.
- Aufgabenformat **17** mit unveränderter Originalsicherung vor der ersten Migration. Persönliche Einstellungen bleiben Format 2.
- Verlauf als Seitenleistenansicht; höchstens 15 Einträge und höchstens 15 Tage, auch beim Laden und Speichern geprüft.

- Sechs Zoomstufen, optionale Mini-Map, Abstands-Guides und zoomunabhängige Druckgeometrie.
- Vollständig responsive Punktmaske, unabhängige Buttonzeilen und nutzbarer Notizeditor unter sechs Aufgabenzeilen.
- Handbuch als HTML speichern/drucken; Import-, Export- und Backup-Ereignisse im Verlauf; ergänzte Aktionsrückmeldungen.
- Dokumentarchivierung, Schema-17-Referenzdaten und reproduzierbare Vorlagen; Lizenzentwurf und Signierungs-/Vertriebsvorbereitung.

Prüfstand und offene Anforderungen: [Entscheidungen und Umsetzungsstand](docs/75_DOKUMENTATIONSREDUKTION_UND_LOGOS_3.33.1.md).

## 3.25.0 – 19.09.2026

Vierundzwanzig Punkte aus einem Arbeitsauftrag mit einem einzigen Leitsatz:
„form follows function“ – zurück zu den Kernfunktionen, mit einer
minimalistischeren Oberfläche. Das bedeutet an den meisten Stellen weniger:
weniger Text in einer Auswahl, weniger Schaltflächen nebeneinander, weniger
Einträge in einem Menü. An einigen Stellen bedeutet es das Gegenteil – dort,
wo bisher nichts stand, obwohl eine Frage offen war.

Kein Formatsprung: Das Aufgabenformat bleibt **16**, das Einstellungsformat
bleibt **2**. Alle neuen Werte sind additiv.

### Behobene Fehler

- **Abgeschnittene Schaltflächen.** Eine Schaltfläche bekam ihre Breite als Zahl mitgegeben; war die Beschriftung länger, lief der Text über die Fläche hinaus und wurde an beiden Enden abgeschnitten – „s HTML speicher“ statt „Als HTML speichern“. Sie misst ihre Beschriftung jetzt selbst und wächst, wenn sie muss. Betroffen war jede Fläche mit langer Beschriftung und jede Fläche bei vergrößerter Oberflächenschrift.
- **Pfeile hinter den Karten.** Eine Verbindung lief von Kartenmittelpunkt zu Kartenmittelpunkt und lag damit zwangsläufig unter beiden Karten – samt ihrer Pfeilspitze. Sie endet jetzt am Kartenrand und liegt vor den Karten; die Spitze schrumpft, wenn die Linie kurz ist. Der Druck benutzt dieselbe Geometrie.
- **„Verspätet“ sprang zur Startseite.** Die Ansicht verlor mit 3.24 ihre Zeile in der Seitenleiste. Ohne Zeile markierte die Seitenleiste ersatzweise die erste – und deren Auswahlereignis warf die Ansicht im nächsten Leerlauf auf die Startseite. Eine Ersatzmarkierung gibt es jetzt nur noch, wenn wirklich nichts geöffnet ist.
- **Versetzte Eingabefelder.** Tagesziel und Tageskapazität standen um eine Zeilenhöhe versetzt, weil die eine Beschriftung umbrach und die andere nicht. Dasselbe in der Punktmaske bei Art/Wichtigkeit und Farbe/Zielliste. Beschriftungen und Felder stehen jetzt in getrennten Rasterzeilen (`FieldPairGrid`).
- **Stillstand nach einem Fehler.** Glide startet als `.pyw`, also ohne Konsole – `sys.stderr` ist dort `None`. Tkinter meldet jeden Fehler aus einem Callback genau dorthin, die Meldung scheiterte also selbst, und zwar innerhalb des Tcl-Aufrufs: Die Ereignisschleife verarbeitete nichts mehr, das Fenster wurde nicht mehr neu gezeichnet, und Windows füllte die stehen gebliebene Fläche weiß. Das ist das Bild „die obere Leiste wird weiß und die App reagiert nicht mehr“. Der Prozess bekommt jetzt vor allem anderen beschreibbare Ströme, und jeder Fehler landet mit Zeitstempel und Traceback im **Fehlerprotokoll** neben den Daten (Hilfe › Fehlerprotokoll öffnen).
- **Modale Dialoge ohne Rückweg.** Scheitert `grab_set` – etwa weil eine andere Anwendung den Griff hält –, riss die Ausnahme bis 3.24 den Aufrufer mit: Der Dialog blieb offen, das Ergebnis wurde nie gelesen. Ein Dialog ohne Griff ist unschön; ein Dialog ohne Rückweg ist ein Stillstand.
- **Unbekannte Farbschlüssel.** Ein Themeschlüssel, den ein Theme nicht kennt, wanderte unverändert an die Zeichenfläche und endete dort als `unknown color name`. Eine fehlende Farbe ist ein Schönheitsfehler, kein Grund, ein Fenster nicht zu öffnen.

### Erweiterte Eingabe und Masken (1.1, 1.2, 1.3, 2.1)

- **„Erweitert“ arbeitet in jeder Ansicht.** In „Mein Tag“, „In Bearbeitung“, „Verspätet“ und „Labels“ antwortete die Schaltfläche mit dem Hinweis, man möge die Aufgabe in ihrer Quellliste öffnen – die Antwort auf eine andere Frage. Die Maske führt die Zielliste ohnehin als Feld. Sie öffnet jetzt überall und bringt mit, was die Ansicht weiß: „Mein Tag“ den Bearbeitungstag, die Labelansicht das betrachtete Label.
- **Breitere Masken.** Die Mindestbreite einer Spalte steigt von 380 auf 440 Pixel. 380 reichte, damit nichts abbricht – nicht, damit eine Spalte lesbar bleibt.
- **Dieselbe Rasterlogik in der Planungseingabe** (Bearbeitungstag und Aufwand).

### Übersichten mit Hierarchie (1.5, 1.6, 2.2)

- **Abschnitte sind aufklappbar.** Die Überschriften der Übersichten sind Elternzeilen mit Aufklapppfeil; ihre Punkte hängen darunter. Der Zustand liegt in den Einstellungen und übersteht den Neustart – besonders nützlich für den Eingangsblock in „Mein Tag“, der die Tagesplanung sonst aus dem Bild schiebt.
- **Ein Abschnitt „Nächste Aufgabe“** am Kopf von „In Bearbeitung“ zeigt genau eine Aufgabe. Sie wird aus den übrigen Abschnitten herausgenommen; zweimal dieselbe Zeile wäre keine Hervorhebung, sondern eine Dublette.
- **Eine Rangfolge für beide Orte.** `task_urgency_rank` entscheidet, welche Aufgabe als Nächstes drankommt: heute eingeplant, dann überfällig, dann länger geplant, dann alles Weitere; innerhalb einer Stufe nach Wichtigkeit und Termin. Bis 3.24 beantwortete die Übersicht die Frage nach Fälligkeit und die Startseitenkachel nach einer eigenen Rangfolge – zwei Antworten auf dieselbe Frage. Die Kachel heißt jetzt „Nächste Aufgabe“ statt „Fokus“ und führt in diesen Abschnitt.

### Anzeige, Menüs und Handbuch (1.4, 1.8, 1.9, 1.10)

- **Die Anzeigeauswahl ist kürzer** – eine Zeile je Umfang statt eines Satzes – **und öffnet unter ihrem Auslöser**, statt an den Fensterrand geschoben zu werden.
- **Menüs nach Zweck gruppiert.** „Ansicht“ trug fünfundzwanzig Einträge hintereinander. In der obersten Ebene steht jetzt nur noch, worum es geht: Ansichten, Mein Tag, Liste, Reiter, Pinnwand, Oberfläche. Ebenso in Datei (Neu anlegen, Importieren, Exportieren, Datenaustausch, Sicherung, Vorlagen, Datenablage) und Bearbeiten (Zwischenablage, Punkt ändern, Struktur). Die Beschriftungen bleiben Wort für Wort dieselben – sie sind die Schlüssel der durchsuchbaren App-Aktionen.
- **Ein Handbuch** unter Hilfe (F1): neun Bereiche, je Baustein eine Zeile aus Name, Wirkung und Ort, mit Suchfeld über alle drei Spalten. Es beantwortet die Frage, die weder Tastenkürzel noch App-Aktionen beantworteten: *wo finde ich das?*
- **„Über Glide“ führt zur Datenablage.** Drei Folgeaktionen: Arbeitsdateien verschieben, Standardordner benutzen, Ordner öffnen. Für den Cloudbetrieb – dieselbe Ablage auf mehreren Geräten – ist das der Einstieg.

### Zwei Designs ohne Farbe (1.11)

- **„Minimal hell“ und „Minimal dunkel“.** Kein abgeschwächter Kontrastmodus, sondern die Gegenrichtung: Was sonst über Farbe unterschieden wird – überfällig, heute fällig, erledigt, wichtig –, unterscheidet sich hier über Helligkeit. Je dringender, desto größer der Abstand zur Fläche. Jeder Wert ist ein echter Neutralton; normaler Text liegt auf jeder Fläche über 4,5:1, Platzhalter über 3:1.

### Rückmeldung auf jede Aktion (1.12)

- **Jeder abgeschlossene Vorgang meldet sich** – Liste angelegt, Ordner angelegt, kopiert, eingefügt, gruppiert, dupliziert, angeheftet, verbunden, rückgängig. Wie viel gemeldet wird, entscheidet eine neue Einstellung: im Dopamin-Design standardmäßig jede Aktion, sonst nur Erledigtes und erreichte Ziele. Der Hauptschalter „Bewegte Rückmeldung“ bleibt darüber.

### Pinnwand (3.2, 3.3, 3.4)

- **Ein Rückweg aus der globalen Pinnwand** als erste Fläche der Reiterzeile.
- **Kürzere Reiterbeschriftungen** mit mehr Innenabstand, am Wortende geschnitten; den vollständigen Titel zeigt der Tooltip.
- **Ein Kontextmenü auf der Fläche.** Rechtsklick auf eine Karte wählt sie aus und zeigt ihre Aktionen; auf freier Fläche zeigt er, was man dort anlegen kann.

### Startseite (4.1, 4.2, 4.3)

- **Eine Pinnwand-Vorschau als Bild.** Die Kachel zeichnet die echte globale Fläche – maßstäblich verkleinert, mit den echten Positionen und Verbindungen. Ein Klick führt hinein. Ohne Karten zeigt sie eine Andeutung statt eines leeren Rahmens.
- **Ein Begleiter.** Eine gezeichnete Figur mit fünf Zuständen, Blinzeln, einer Regung auf Berührung und einem vergebbaren Namen. Ihr Zustand spiegelt den Bestand – überfällige Fristen, ein erreichtes Tagesziel, ein leerer Tag –, nicht den Menschen: Glide leitet aus Abschlüssen keine Bewertung ab. Sie kommt ohne Bilddatei aus und folgt jedem Design, auch den farblosen.
- **Ein aufgeräumter Begrüßungsbereich.** Vier Wege stehen als Fläche da – Mein Tag, In Bearbeitung, Eingang, Pinnwand –, alles Übrige hinter „Weitere …“ in drei Gruppen. Zehn gleich aussehende Schaltflächen nebeneinander sind keine Auswahl, sondern eine Wand.

### Prüfung und Codebasis (5.1, 5.3)

- **Zwei neue Prüfsuiten.** `test_features325.py` weist jeden Auftragspunkt einzeln nach. `test_vollpruefung325.py` prüft in die Breite: neun Designs × drei Fensterbreiten × zwölf Ansichten, alle fünf Anzeigeumfänge, alle sechzehn Startseitenkacheln einzeln, alle vierundachtzig Menüaktionen, alle Pinnwandaktionen, alle Rückmeldungsstufen und alle Zustände des Begleiters. Damit sind es **30 Suiten**.
- **Ein neues Analysewerkzeug.** `dublettenpruefung.py` findet wiederholte Codeblöcke. Daraus entstanden vier gemeinsame Bausteine: `finish_page_switch` (vier Kopien), `rounded_rect_points` (drei), `reveal_tree_row` (zwei) und die Tabelle `GLASS_LAYERS` (zwei Zweige). Die Farbtafeln der Designs bleiben ausgeschrieben – sie sind Daten, keine Logik.
- **Weitere zusammengefasste Stellen:** `build_menu` (Menüaufbau samt Theme-Anmeldung), `restore_focus`, `dialog_color`, `FieldPairGrid`, `tab_label`, `themed_message_dialog(extra_buttons=…)`.

### Neue Einstellungswerte

| Wert | Bedeutung | Vorgabe |
|---|---|---|
| `overview_sections_closed` | zugeklappte Abschnitte der Übersichten | leer |
| `action_feedback` | Umfang der Rückmeldung | `auto` |
| `mascot_name` | Name des Begleiters | leer |

Dazu die Kachelschlüssel `boardpreview` und `mascot` sowie die Designschlüssel
`minimal_light` und `minimal_dark`.

[Übersichtlichkeit und Hierarchie](docs/57_UEBERSICHT_UND_HIERARCHIE_3.25.0.md) ·
[Startseite und Begleiter](docs/58_STARTSEITE_UND_BEGLEITER_3.25.0.md)

## 3.24.0 – 19.09.2026

Zwanzig Punkte aus einem Arbeitsauftrag. Der Schwerpunkt liegt auf zwei
Fragen: Wie viel muss eine Seitenleiste zeigen, damit man sich zurechtfindet –
und was fehlt der Pinnwand, um mehr zu sein als eine Ablage für Zettel.

Kein Formatsprung: Das Aufgabenformat bleibt **16**, das Einstellungsformat
bleibt **2**. Alle neuen Werte sind additiv.

### Navigation: sechs Zeilen statt acht (Punkte 1, 2)

- **Der Eingang ist ein Abschnitt, keine Zeile.** 3.23 stellte ihn eingerückt unter „Mein Tag“ – richtig gedacht und trotzdem eine Zeile zu viel, denn „Mein Tag“ zeigte denselben Bestand ohnehin schon als Eingangsblock. Die Zeile entfällt; der Abschnitt bleibt, und ein Doppelklick auf seine Überschrift öffnet den Eingang als Liste.
- **„Verspätet“ steht in „In Bearbeitung“.** Als erster Abschnitt unter eigener Überschrift, gefolgt von „Noch offen“. Gibt es nichts Überfälliges, entfällt die Überschrift und die Ansicht sieht aus wie vorher. Die eigene Ansicht bleibt vollständig erhalten – über Ansichtsmenü, App-Aktionen, Startseite und den Doppelklick auf die Überschrift.
- **Beide Ziele bleiben benannt erreichbar.** „Verspätet“, „Eingang öffnen“ und „Globale Pinnwand öffnen“ stehen in der Aktionsgruppe „Ansichten“ und damit in der durchsuchbaren Aktionsliste.

### Pinnwand als Denkfläche (Punkte 4, 5, 9, 10, 11, 12)

- **Mehrere Karten auswählen.** `Strg`/`Cmd` und Klick nimmt eine Karte hinzu oder heraus. Die Auswahl ist eine Reihenfolge: Die zuerst gewählte Karte ist der Anker und trägt einen stärkeren Rahmen. „Verbinden“ verbindet den Anker mit jeder weiteren – der Sternfall, aus dem eine Hierarchie entsteht. Erledigt umschalten, Kartengröße und Entfernen wirken auf die ganze Auswahl.
- **Verbindungen haben eine Richtung.** Vier Arten: Linie ohne Richtung, Pfeil vorwärts, Pfeil rückwärts, Pfeil in beide Richtungen. Gespeichert wird die Art, nicht die gezeichnete Spitze; eine Austauschdatei kann sie deshalb ohne Zeichenfläche auswerten. Die Spitzen erscheinen auch im Druck. Zwischen zwei Karten liegt weiterhin höchstens eine Verbindung.
- **Drei Kartengrößen.** Eine Fläche kennt keine Einrückung – was in einer Liste die Ebene ist, ist hier die Größe. „Groß · Hauptgedanke“, „Normal“, „Klein · Randnotiz“. Der Faktor wirkt auf Kartenbreite, Titelgröße und Akzentstreifen gemeinsam. Der Maßstab hängt an der Karte, nicht am Punkt: Derselbe Punkt kann auf der einen Fläche Hauptgedanke und auf der anderen Randnotiz sein.
- **Neue Punkte in der vollständigen Maske.** Der Doppelklick auf die freie Fläche fragte bis 3.23 nach einer Zeile Text. Auf der Karte stehen aber Beschreibung, Labels, Termin, Checkliste und Anhänge; jetzt öffnet sich dieselbe Maske wie hinter „Erweitert“. Ordner- und globale Pinnwand fragen zusätzlich nach der Zielliste, statt den Weg zu sperren.
- **Aktionen in drei Gruppen.** Elf gleich aussehende Schaltflächen in einer Reihe sind keine Ordnung, sondern eine Aufzählung – und sie kosteten vier Zeilen Höhe. Sichtbar bleiben vier; alles Übrige steht unter „Weitere Aktionen …“ in den Gruppen Inhalt, Ausgewählte Karte und Fläche.
- **Eine globale Pinnwand.** Über den gesamten Bestand, erreichbar aus der Listen- und Ordnerübersicht und von der Startseite. Kein zweiter Kartenspeicher, sondern eine Pinnwand wie jede andere mit dem Bereichsschlüssel `global`.

### Die Anordnung reist mit (Punkt 8)

- **Jedes Komplettbackup trägt die Pinnwände.** Bis 3.23 lagen Kartenpositionen und Verbindungen ausschließlich in den persönlichen Einstellungen und reisten nur im vollständigen App-Backup mit; ein Komplettbackup und eine exportierte Liste verloren sie. Der neue Abschnitt `pinboards` steht neben den Aufgabenfeldern – nicht in ihnen, weil derselbe Punkt auf mehreren Pinnwänden an verschiedenen Stellen liegen kann.
- **Beim Hinzufügen wandert sie mit.** Listen, Ordner und Punkte bekommen dabei neue Kennungen; Karten und Verbindungen ziehen um. Was sich nicht zuordnen lässt, fällt weg, statt auf fremde Objekte zu zeigen. Die globale Pinnwand des Gebers wird bewusst nicht übernommen.
- Ältere Glide-Fassungen lesen dieselbe Datei weiterhin und übergehen den Abschnitt.

### Vollbild und ein Fehler beim Rückweg (Punkte 6, 7)

- **„Fläche“ heißt jetzt „Vollbild“** und zeigt im eingeschalteten Zustand dieselbe dauerhafte Füllung wie die übrigen Flächenschalter. Vorher wechselte nur die Randfarbe, und der aktive Zustand war auf einer vollen Fläche nicht zu erkennen.
- **Kopfzeile und Eingabezeile stehen nach dem Rückweg wieder oben.** `pack_info()` beschreibt Seite, Füllung und Abstände, aber nicht die Stelle in der Packreihenfolge – ein später wieder gepacktes Widget landet am Ende seines Elternteils. Gemerkt wird jetzt zusätzlich der erste nachfolgende sichtbare Nachbar.

### Anzeige, Startansicht und Fensterbreiten (Punkte 3, 13, 14, 20)

- **Das Zahnrad steht auf der rechten Flucht.** Die Dichteregelung der Kopfzeile packte es bei jedem Stufenwechsel mit acht Pixeln rechtem Abstand neu und schob es damit vor die Flucht von „Hinzufügen“ und „Anzeige“.
- **„Anzeige“ öffnet eine Fläche im App-Stil** statt eines Systemmenüs: Name und Erklärung je Zeile, Haken auf der aktiven, Bedienung mit Pfeiltasten, Return und Escape.
- **Acht Ziele für die Ansicht beim Öffnen** statt dreier: letzte Ansicht, Startseite, Mein Tag, In Bearbeitung, Listen- und Ordnerübersicht, Vorlagen, globale Pinnwand oder eine feste Liste. Die Listenauswahl erscheint nur, wenn sie etwas entscheidet; eine Liste, die es nicht mehr gibt, führt auf die Startseite.
- **Zweispaltige Masken bekommen die Breite zweier Spalten.** Die Schwelle wird aus der Mindestbreite einer Spalte gerechnet statt geraten. Die Punktmaske öffnete mit 760 Pixeln knapp über der damaligen Schwelle von 684 – zweispaltig und gequetscht zugleich.
- **Tagesziel und Tageskapazität stehen nebeneinander.** Beide tragen eine einzelne Zahl und ließen über die volle Spaltenbreite je drei Viertel Leerraum stehen.

### Rückmeldung und Startseite (Punkte 15, 16, 17, 18, 19)

- **Die Rückmeldung beim Erledigen gibt es in jedem Design.** Sie hing bis 3.23 am Dopamin-Design; jetzt ist sie eine eigene Einstellung (Vorgabe an). Das Dopamin-Design steigert sie, statt sie zu besitzen.
- **Arcade im Dopamin-Modus.** Aus der einen Fahne wird ein Stapel aus fünf: versetzt gestartet, versetzt gestellt, in wechselnden Farben, mit pulsendem Rand. Dazu eine Kombo für mehrere Erledigungen innerhalb von acht Sekunden – sie zählt keine Daten und lebt nur in der laufenden Sitzung. Die Farben gehen eine Stufe tiefer ins Schwarz und eine Stufe höher in die Sättigung; der Textkontrast steigt dadurch.
- **Vier weitere Startseitenkacheln:** Kalendervorschau, Verspätet, Fortschritt und Pinnwände. Die Kalendervorschau kennt drei Darstellungen – Monat als Raster, laufende Woche, nächste Termine – und liest Fälligkeit und Bearbeitungstag gemeinsam. Ein zweiter Schalter sagt, wie ausführlich die Kacheln sind.

### Prüfstand

**28 Suiten** (neu: `test_features324.py`) und vier Analysen. Die Anordnung der
Pinnwand hat mit `pinboards_from_backup` eine eigene Prüfung; Mehrfachauswahl,
Verbindungsarten, Kartengröße, globale Fläche, Startansicht, Anzeigefläche und
der Rückweg aus dem Vollbild werden einzeln nachgewiesen.

## 3.23.0 – 18.09.2026

Sechsundvierzig Punkte aus einem Master-Arbeitsauftrag. Der Schwerpunkt liegt
nicht auf neuen Funktionen, sondern auf dem, was die vorhandenen zusammenhält:
eine Designauswahl statt dreier Schalter, eine Tabellenkomponente statt sieben
einzelner, messbar schnellere Ansichtswechsel und ein Austauschformat, über das
Glide mit anderen Systemen sprechen kann, ohne sein internes Format offenzulegen.

Kein Formatsprung: Das Aufgabenformat bleibt **16**, das Einstellungsformat
bleibt **2**. Alle neuen Werte sind additiv.

### Ein Designsystem statt dreier Schalter (Punkte 3, 4, 5)

- **Eine Auswahl „Design“.** Bis 3.22 stand die Erscheinung an drei Stellen: „Design · Hell / Dunkel“, darunter „Farbmodus“ und weiter oben ein Häkchen „Materialoptik“. Erst ihre Kombination ergab das Bild – und zwei der acht Kombinationen waren wirkungslos, weil Kontrast und Dopamin die Glasoptik ohnehin abschalteten. Seit 3.23 gibt es sieben Designs in einer Liste: **Hell**, **Dunkel**, **Liquid Glass hell**, **Liquid Glass dunkel**, **Dopamin**, **Kontrast hell** und **Kontrast dunkel**.
- **Erweiterbar als Registry.** Ein Design ist eine Zeile in `DESIGNS` mit vier Angaben: Grundpalette, Farbschicht, Materialoptik und das Gegenstück für den Hell-/Dunkel-Schalter. Ein weiteres Design braucht eine weitere Zeile, keinen zusätzlichen Code.
- **Übernahme ohne Verlust.** Aus `theme`, `color_mode` und `glass_mode` wird einmalig ein Design. Wer im Dunkelmodus mit Dopamin arbeitete, findet „Dopamin“ wieder; wer den Dunkelmodus mit Materialoptik hatte – die Vorgabe seit 3.7 –, bekommt „Liquid Glass · dunkel“ und damit genau das Bild von vorher. Die drei alten Werte bleiben als abgeleitete Angaben in `settings.json` stehen, damit eine ältere Glide-Fassung dieselbe Datei weiterhin richtig liest.
- **Der Hell-/Dunkel-Schalter bleibt im Design.** Wer im Kontrastdesign arbeitet, landet im hellen Kontrastdesign statt im normalen Hellmodus. Dopamin hat kein helles Gegenstück; der Schalter sagt das, statt einen Wechsel zu versprechen.
- **Liquid Glass ausgebaut.** Tk kann keine Fläche weichzeichnen. Tiefe entsteht deshalb aus dem, was Tk kann: einem senkrechten Verlauf über dem oberen Drittel jeder Karte, oben heller als unten, aus höchstens zwölf Streifen. Darunter bleibt die volle Flächenfarbe, damit Text überall auf demselben Grund sitzt. Dazu die vorhandene helle Innenkante, die dunkle Außenkante und unter Windows der native Systemhintergrund.

### Navigation, Eingang und Startseite (Punkte 6, 7, 8, 22, 23)

- **Der Eingang steht unter „Mein Tag“.** Er war ein eigener Hauptpunkt und damit gleichrangig neben der Ansicht, deren Vorstufe er ist. Jetzt steht er eingerückt darunter – dieselbe Liste, derselbe Klick, eine Ebene tiefer. Ebenso „Verspätet“ unter „In Bearbeitung“, dessen Teilmenge es ist.
- **Reihenfolge nach dem Tagesablauf:** Startseite, Mein Tag (mit Eingang), In Bearbeitung (mit Verspätet), Labels, Vorlagen, Papierkorb.
- **Tagespfeile in Leserichtung.** „◀“ stand rechts von „▶“, weil bei `side="right"` das zuerst gepackte Widget am weitesten rechts landet. Jetzt links, wie man es liest.
- **Auf- und Zuklappen wirkt global.** Bis 3.22 betraf es nur die Punkte der offenen Liste; Ordner der Seitenleiste blieben unberührt. Jetzt klappt „Zuklappen“ auch alle Ordner zu – mit einer Ausnahme: Der Pfad zur geöffneten Liste bleibt offen, sonst verschwände genau das aus dem Bild, woran gerade gearbeitet wird.
- **Eine Kachel „Heute“ statt zweier.** „Mein Tag“ und „Heute fällig“ standen als zwei gleich aussehende Kacheln nebeneinander. Es sind zwei Fragen – woran arbeite ich heute, was muss heute fertig sein –, aber nebeneinander in einer Kachel beantworten sie sich besser: Erst so wird sichtbar, ob das eine zum anderen passt.

### Ansichtswechsel: 336 auf 129 Millisekunden (Punkt 9)

Gemessen über einen Bestand von 1.584 Punkten in zwölf Listen und sechs Ordnern,
je zwanzig Ansichtswechsel unter `cProfile`.

- **Befund 1: dieselbe Zeichenkette 347.000-mal geprüft.** `normalize_due` baute für jede Datumsprüfung mit `strptime` ein `datetime`-Objekt auf – 2,9 von 11,3 Sekunden. Die Datumswerte eines Bestands wiederholen sich stark; ein Zwischenspeicher über den Eingabetext trifft fast immer.
- **Befund 2: derselbe Bestand mehrfach je Wechsel durchlaufen.** Die Seitenleiste fragt für ihre Zeilen nacheinander nach fälligen, überfälligen, eingeplanten und gelabelten Punkten – jede Frage lief über alle Listen und alle verschachtelten Punkte. Danach rechnete die Textanpassung dieselben Zahlen erneut, und die Ansicht ein drittes Mal. Neu ist ein Zwischenspeicher, der ausschließlich innerhalb eines Aufbaus lebt: Außerhalb rechnet jede Abfrage wie bisher frisch, sodass er nichts Veraltetes liefern kann.
- **Befund 3: jede Tabellenzeile einzeln vermessen.** Die Spaltenbreite wurde aus `font.measure` für jede Zeile ermittelt – 164 Millisekunden je Aufbau. Fälligkeiten wiederholen sich; jeder Text wird jetzt einmal gemessen.
- **Ergebnis:** 336 → **129 Millisekunden** je Ansichtswechsel (−62 %), Funktionsaufrufe 13,2 → 4,6 Millionen. Der verbleibende Anteil liegt im Zeichnen durch Tk, nicht mehr in Python. Es wurde keine Ladeanimation ergänzt: Bei 129 Millisekunden wäre sie länger sichtbar als der Vorgang dauert.

### Dialoge: Schnellerfassung, Kalender, mehrspaltige Masken (Punkte 10, 11, 20)

- **Schnellerfassung überarbeitet.** Beschreibung ergänzt (Strg+Enter speichert von dort), Kalenderknopf am Fälligkeitsfeld, das native ttk-Kästchen durch ein Glide-Kästchen ersetzt, Fensterleiste im aktiven Design – sie war der einzige Dialog ohne diese Anpassung und blieb unter Windows weiß.
- **Kalenderauswahl an jedem Datumsfeld.** Neue gemeinsame Methode `attach_calendar_picker`; ergänzt in der Schnellerfassung und am Serienende der Wiederholung, dem letzten Datumsfeld, das nur getippt werden konnte. Getippt werden darf weiterhin überall – beide Wege schreiben in dieselbe Variable.
- **Punktmaske zweispaltig.** Titel, Art, Wichtigkeit, Farbe und Zielliste stehen über den Spalten; darunter links Fälligkeit, Wiederholung, Erinnerung und Bearbeitungstag, rechts Labels, Beschreibung, Checkliste und Anhänge. Unter 684 Pixeln steht wieder alles untereinander – vollständig, nicht gequetscht. Das Uhrzeitfeld rutscht bei schmaler Spalte unter das Datum, statt auf vierzig Pixel zusammenzuschrumpfen.
- **Fensterleiste nachgezogen** in fünf weiteren Dialogen, die sie nicht hatten.

### Tabellen: eine Komponente statt sieben (Punkte 15, 16, 17, 18, 19, 25, 27, 43)

- **Der Spaltendialog öffnete sich leer.** Seit 3.21.4 rief er `self.label(…)` – eine Methode, die es nur in `ItemWorkspace` gibt, nicht in `ListApp`. Tk verschluckte den AttributeError im Callback; sichtbar war ein Fenster ohne Inhalt. Behoben, und **`tests/tools/attributpruefung.py`** findet einen solchen Aufruf künftig vor dem Ausliefern.
- **Spaltenbreiten bleiben stehen.** Bis 3.22 prüfte Glide erst beim Loslassen, ob der Zeiger über einer Trennlinie steht – nach dem Ziehen steht er dort fast nie mehr. Entscheidend ist jetzt, wo der Klick begann.
- **`prepare_table` richtet jede Tabelle gleich ein:** linksbündig, Mindestbreite nie kleiner als die eigene Überschrift, an den Trennlinien ziehbar. Damit ist „Zeitpunkt (Ortszeit)“ in den Benachrichtigungen nicht mehr angeschnitten, und der Änderungsverlauf hat Überschriften – vier Spalten ohne Überschrift ließen raten, was worin steht, und boten keine Trennlinie zum Ziehen.
- **Hover bleibt lesbar.** Ohne eigene Zuordnung nahm Tk für eine Überschrift unter dem Mauszeiger seine helle Systemfarbe, behielt aber die Schriftfarbe des Themes: weiße Schrift auf weißem Grund. Beide Tabellenstile haben jetzt eine ausdrückliche Hover-Farbe, deren Schrift aus der Helligkeit der Fläche folgt.
- **Auswahlkontrast gerechnet statt geschätzt.** Weiß auf dem Lila der Auswahl erreichte 3,5:1 und lag damit unter dem, was normaler Text braucht. Statt die Schrift zu wechseln, wird die Fläche so weit nachgezogen, bis Weiß trägt: Alle 49 Kombinationen aus sieben Designs und sieben Akzentfarben erreichen jetzt mindestens 4,5:1.
- **Siebzehn Beschriftungen linksbündig verankert.** `justify="left"` richtet nur mehrere Zeilen zueinander aus; wo der Block im Widget sitzt, entscheidet `anchor`. Daran lag der schiefe Hinweistext der Benachrichtigungen – und an sechzehn weiteren Stellen dasselbe.

### Globale Aktionen und schmale Fenster (Punkte 24, 28, 29, 30, 31, 32)

- **Drucken und PDF in der Kopfzeile.** Die Funktion gibt es seit 3.17, lag aber nur im Menü „Datei“ und hinter Strg+P. Sie steht jetzt als Schaltfläche neben dem Seitenleistenschalter – beide wirken auf die geöffnete Ansicht, nicht auf einen ausgewählten Punkt. Bewusst genau eine zusätzliche Schaltfläche; alles Weitere liegt im Überlaufmenü.
- **Drei Dichtestufen.** Die Regel „Essentielles bleibt, Sekundäres geht zuerst“ war nirgends umgesetzt – stattdessen schrumpfte der Titel als Einziges, weil er als Letztes um Platz bat. Jetzt weicht ab 1120 Pixeln die Beschriftung „Benachrichtigungen“ zugunsten der Zahl, ab 900 wandern Drucken und Einstellungen ins Überlaufmenü.
- **Aktionsreihen und Statuszeile.** „Liste leeren“, „Löschen“, „Bearbeiten“ und „Rückgängig“ weichen bei schmaler Reihe – alle vier bleiben über Kontextmenü, Menüleiste und Tastenkürzel erreichbar. Die Fortschrittszeile zeigt nur noch ihre ersten Angaben, der Rest steht im Tooltip. „Suche löschen“ erscheint nur, wenn es etwas zu löschen gibt.
- **Pinnwandwerkzeuge priorisiert:** „Raster“, „Finden“ und „Fläche“ bleiben, „Vorschau“ und „Auto“ weichen zuerst.
- **Zweispaltige Startseite ab 616 statt 980 Pixeln.** Die Schwellen waren geraten; jetzt folgen sie der Mindestbreite einer lesbaren Kachel (300 Pixel) plus Zwischenraum. Ein auf die Bildschirmhälfte gelegtes Fenster bleibt damit zweispaltig.

### Listenansicht mit Checklisten und Anhängen (Punkte 33, 34, 35)

- **Umschalter „Anzeige“** mit fünf Stufen: **Kompakt** (nur Titel, Termin, Labels), **Standard**, **Checklisten**, **Anhänge**, **Erweitert**. Der Umfang gilt für jede Ansicht, die Punkte als Zeilen zeigt.
- **Checklistenschritte als eigene Zeilen** – und direkt abhakbar: Ein Klick oder die Leertaste auf einer Schrittzeile schreibt in die Checkliste ihres Punkts, nicht in den Punkt selbst. Dazu Anhänge mit Namen und Größe sowie der Anfang der Beschreibung.
- **Warum das zählt:** Ein KI-Dokument mit 42 Hauptpunkten und je fünf Schritten war bis 3.22 nur über 42 einzeln geöffnete Dialoge prüfbar. Detailzeilen sind Darstellung, keine Daten: Sie tragen ein eigenes IID-Suffix, zählen nicht als Punkte und wandern nicht in Exporte. Höchstens zwölf je Punkt, damit eine Liste lesbar bleibt.

### Glide-Austauschformat (Punkte 36, 37, 38, 39, 40)

- **`.glideexchange`, Formatversion 1.** Ein eigenes Format neben dem internen: Das interne Aufgabenformat ist sechzehnmal gewachsen und wird weiter wachsen; würde es zum Vertrag mit einem fremden System, müsste dieses jede künftige Migration mitgehen. Zwei getrennte Zahlen – `DATA_SCHEMA_VERSION` beschreibt, wie Glide speichert, `EXCHANGE_FORMAT_VERSION`, worauf man sich verlassen kann.
- **Keine internen Kennungen.** Die Datei arbeitet mit frei wählbaren Schlüsseln (`list-1`, `label-2`); die echten IDs vergibt Glide beim Import. Abgebildet werden Ordner, Listen, Punkte aller vier Arten, Unterpunkte, Beschreibungen, Labels, Fälligkeit mit Uhrzeit, Bearbeitungstag, Aufwand, Wichtigkeit, Erledigt-Zustand und Checklisten.
- **Capability-Registry.** Die Datei nennt selbst, was die erzeugende Fassung kann – eine KI muss es nicht aus der Versionsnummer raten. Anhänge, Wiederholungen und Erinnerungen stehen ausdrücklich auf 0: Sie hätten eigene Regelwerke, die eine erzeugende Stelle kaum verlässlich trifft.
- **Import mit Vorschau.** Erst Prüfung von Aufbau, Formatversion, Feldnamen, Werten und Verweisen, dann eine Zählung dessen, was entstehen würde, dann die Bestätigung. Ein Feld, das diese Fassung nicht kennt, wird **nicht still verworfen**, sondern genannt – und dann ist Abbrechen die Vorgabe. Der Import legt ausschließlich Neues an und ist ein einziger Rückgängig-Schritt.
- **Zwei Ebenen, aber nicht zwei Verträge.** Verbindlich ist die JSON-Datei: verlustfrei, prüfbar, roundtrip-fähig. Daneben liest Glide eine **Gliederung in Markdown** – „# Liste“, „## Abschnitt“, „- Aufgabe“, eingerückte Unterpunkte, „- [ ]“ als Checklistenschritt. Sie ist das, was ein Sprachmodell am zuverlässigsten erzeugt, und ohne Werkzeug lesbar; sie trägt bewusst weniger und ist für den Rückweg nicht geeignet.
- **„Austauschformat anzeigen …“** erzeugt die Anweisung für eine KI aus den tatsächlichen Konstanten – sie kann deshalb nicht veralten.

### Pinnwand: Fläche, Verbindungen, Druck (Punkte 12, 13, 14)

- **Vollbild für die Fläche.** Seitenleiste, Kopfzeile, Eingabe-, Filter- und Aktionsreihen weichen; die Pinnwand bekommt das Fenster. Escape arbeitet sich von innen nach außen: erst das Verbinden abbrechen, dann das Vollbild, dann die Pinnwand. Die Scrollposition bleibt in beide Richtungen erhalten.
- **Verbindungen als Beziehung, nicht als Linie.** Gespeichert wird ein Paar von Punktkennungen, gezeichnet wird bei jedem Aufbau neu. Dadurch stimmt die Linie immer – auch nach dem Verschieben, nach einem Filter und nach dem Neustart –, und sie lässt sich später auslesen. Bewusst ungerichtet: Eine verbindliche Reihenfolge wäre eine Aufgabenabhängigkeit mit eigener Prüfung auf Kreise, nicht etwas, das nebenbei aus einer Linie entsteht. Fällt eine Karte weg, verschwindet ihre Verbindung mit.
- **Punkte direkt auf der Fläche.** „Neue Aufgabe“, „Neue Notiz“ und der Doppelklick ins Leere legen einen echten Punkt in der Quellliste an und heften ihn an die Klickposition. Das ist der Unterschied zu einem Whiteboard-Programm: Was hier entsteht, steht anschließend auch in der Liste, in der Tabelle, im Kalender und im Backup – es gibt keine zweite Datenhaltung, die auseinanderlaufen könnte.
- **Drucken und PDF.** Gedruckt wird nicht der Bildschirmausschnitt, sondern das Rechteck, in dem tatsächlich Karten liegen; das Papierformat folgt dessen Seitenverhältnis. Verbindungen kommen als SVG-Linien mit, Karten als positionierte Kästen mit Titel, Frist, Checklistenstand und Labels.
- **Bewusst noch nicht:** freies Zeichnen, Zoom und Notizzettel ohne zugehörigen Punkt. Sie stehen als Stufe 2 in `docs/50_PINNWAND_ARBEITSFLAECHE_3.23.0.md`.

### Prüfstand (Punkte 26, 41, 42, 44, 46)

- **Neue Suite `test_features323.py`** mit rund 250 Zusicherungen über alle umgesetzten Punkte, darunter Regressionstests für den leeren Spaltendialog, die nicht gespeicherten Spaltenbreiten, die vertauschten Tagespfeile und die unlesbare Auswahl.
- **Neue Analyse `attributpruefung.py`** als vierte neben statischer Analyse, Erreichbarkeit und Standprüfung.
- **Der Zeitzonenversatz wird gemessen, nicht gesetzt.** Der Prüfstand setzte `TZ=Europe/Berlin` und verließ sich darauf – das ist eine Absicht, kein Nachweis. Windows kennt kein `time.tzset()` und wertet die Variable nicht aus; maßgeblich bleibt dort die Systemzeitzone. Ein Lauf auf einem Rechner in UTC wäre gegen Zeitzonenfehler so blind gewesen wie die Vorabumgebung, in der der `UNTIL`-Fehler aus 3.21.0 grün blieb – hätte im Protokoll aber das Gegenteil behauptet. Der neue Schritt „Zeitzone“ misst den Versatz in derselben Umgebung, die auch die Suiten bekommen, und stuft einen Lauf ohne Versatz als unvollständig ein statt als bestanden.
- **Unter Windows wird `TZ` nicht mehr gesetzt.** Der erste Windows-Lauf zeigte, dass die dortige Laufzeit aus `Europe/Berlin` keine benannte Zone liest, sondern eine erfundene: Sie meldete sich als „ope“ mit +01:00, während in Berlin an diesem Tag +02:00 galt – ein Versatz ohne Sommerzeitregel, der plausibel aussieht und es nicht ist. Jede Umrechnung in Ortszeit lag damit eine Stunde daneben. Maßgeblich ist dort die Systemzeitzone. Der Schritt „Zeitzone“ meldet ein unter Windows gesetztes `TZ` als Befund und misst zusätzlich, ob die Zone überhaupt eine Sommerzeitregel kennt.
- **Der Datenabgleich nennt die Stelle, nicht nur den Umstand.** „Beispieldaten unterscheiden sich vom Erzeuger“ war eine Meldung ohne Fundstelle – bei mehreren tausend Feldern beginnt danach jedes Mal dieselbe Suche von Hand. Beide Abgleiche nennen jetzt die ersten Pfade samt beider Werte, etwa `Bestand.lists[3].items[7].due: Fixture 5, Erzeuger 6`.
- **Die Beispieldaten entstehen auf jeder Plattform gleich.** Die vier Textanhänge wurden im Textmodus ohne Angabe des Zeilenendes geschrieben: Unter Windows wurde daraus CRLF, und jede Datei wuchs um ein Byte je Zeile – 83 statt 86, 72 statt 75, 74 statt 75, 136 statt 138. Da der Abgleich auch die Anhanggrößen vergleicht, konnte er unter Windows **nie** gleich ausfallen; aufgefallen ist es erst, weil es vorher keinen Windows-Vollprüflauf gab. Erzeuger der Beispieldaten und des Vorlagenkatalogs schreiben jetzt ausdrücklich mit `\n`. Die Fixture blieb unangetastet – sie war richtig.
- **Datenintegrität ausdrücklich geprüft:** Auf- und Zuklappen fasst den Bestand nicht an, Detailzeilen zählen nicht als Punkte, ein Import ist ein einziger Rückgängig-Schritt, eine entfernte Karte nimmt ihre Verbindungen mit, und ein Punkt, der auf der Pinnwand entsteht, steht auch in der Liste.

## 3.22.0 – 17.09.2026

Ein Funktionsstand aus zwanzig Punkten einer Sichtprüfung. Vier davon sind
Umbauten, die übrigen Nachbesserungen an vorhandenen Ansichten.

### Mein Tag: ein Tagesmodell statt zweier

- **„Mein Tag“ und „Tagesplanung“ sind eine Ansicht.** Bis 3.21 beantworteten zwei Ansichten dieselbe Frage: „Mein Tag“ als bewusste Auswahl von Punktkennungen in `settings.json`, die um Mitternacht verfiel und in keinem Aufgabenbackup stand, und die „Tagesplanung“ als Rechnung über `planned_date` am Punkt mit Tagesnavigation und Kapazitätsvergleich. Wer beides benutzte, pflegte zwei Listen für denselben Tag. Geblieben ist **Mein Tag** über `planned_date`: mit Tagesnavigation, Aufwandssumme und Kapazitätsvergleich, gespeichert am Punkt und damit in jedem Backup und im Änderungsverlauf. Die Seitenleiste zeigt eine Tageszeile statt zweier.
- **Eingangsblock.** Am Ende derselben Ansicht stehen die offenen Punkte des Eingangs ohne Bearbeitungstag – neu erfasste Aufgaben bleiben damit nicht unbemerkt liegen. Ein Rechtsklick plant sie auf den betrachteten Tag ein; die Statuszeile nennt die Anzahl.
- **Einmalige Migration.** Beim ersten Start von 3.22 bekommt jeder Punkt, der an diesem Kalendertag in `today_plan` stand und noch keinen Bearbeitungstag trägt, den heutigen. Danach wird `today_plan` nicht mehr geschrieben. Eine Auswahl von gestern war schon in 3.21 verfallen.

### Checkliste je Aufgabe – Aufgabenformat 16

- **Neues additives Feld `checklist`** am Punkt: kurze Schritte mit Text und Zustand, wie in der Checkliste einer Planner-Aufgabe. Die Maske legt sie zwischen Beschreibung und Anhängen an; Enter legt den nächsten Schritt an, die Leertaste hakt ab, „▲“ und „▼“ ordnen. Grenzen: fünfzig Schritte je Punkt, zweihundert Zeichen je Schritt. Wer Termin, Labels oder Anhänge braucht, legt weiterhin einen Unterpunkt an; Gruppen und Überschriften tragen keine Checkliste.
- **Sichtbar** in der Zeile (`☑ 2/5`), als eigene Tabellenspalte, als Fortschrittsbalken auf der Pinnwandkarte, in der Reiteransicht, im Markdown-Export als Kästchenliste und im Druck als Zeile „Checkliste: 2 von 5“.
- **Format 15 bleibt gültig**: Fehlt das Feld, trägt der Punkt keine Checkliste. Vor dem ersten Speichern in Format 16 entsteht `backups/liste_vor_format16_<Zeitstempel>.json`. Ein beschädigtes Feld führt auf eine leere Checkliste zurück, statt die Datei unlesbar zu machen; die strenge Backupprüfung weist eine Checkliste ab, die keine Liste ist. Der Änderungsverlauf protokolliert sie als eigenes Feld. Referenzformat: `tests/fixtures/current_v16/reference_v16.json`.

### Startseite, Aktionen, Tabelle und Filterzeile

- **Startseite als einstellbares Kachelraster.** Die Spaltenzahl folgt der Fensterbreite (eine Spalte unter 980 Pixeln, zwei bis 1500, darüber drei) und lässt sich festsetzen; jede Kachel ist ein- und ausschaltbar und in ihrer Reihenfolge verschiebbar („Startseite einrichten …“). Neu: **Mein Tag**, **Fokus** (ein konkreter nächster Schritt), **Die nächsten sieben Tage**, **Labels im Bestand**, **Impuls für den Tag**. Bestehende Startseiten bleiben unverändert – die neuen Kacheln sind aus, bis jemand sie einschaltet. Die Verteilung setzt jede Kachel in die bislang kürzeste Spalte; ohne das stünde die hohe Bestandskachel allein neben einer leeren Spalte.
- **Aktionen nach Aufgabengruppen.** Der Dialog „Alle App-Aktionen“ gliedert in zehn Gruppen mit Zwischenüberschrift und Zwischenraum – dieselbe Form wie im Tastenkürzel-Fenster. Die Bereichsauswahl filtert nach diesen Gruppen statt nach Menütiteln; Auswahl und Enter überspringen Überschriften. Eine nicht zugeordnete Aktion landet sichtbar unter „Weitere Aktionen“, und die Regression verlangt, dass diese Gruppe leer bleibt.
- **Tabellenansicht:** Überschriften linksbündig statt zentriert über linksbündigen Werten; Spaltenbreiten selbst ziehbar und je Liste gespeichert; Sortieren per Klick auf die Überschrift in drei Zuständen (aufsteigend, absteigend, Listenreihenfolge) mit ▲/▼ in der Überschrift; leere Zellen bleiben in beiden Richtungen am Ende; neue Spalte „Checkliste“; „Breiten und Sortierung zurücksetzen“ im Spaltendialog.
- **Rückweg aus der Tabelle.** Der Umschalter verschwand dort und war nur über das Ansichtsmenü erreichbar. Er bleibt jetzt stehen und heißt in der Tabelle „Liste“.
- **Abstände der Filterzeile.** Jede Schaltfläche trug ihren Zwischenraum rechts; dadurch stand die äußerste acht Pixel vor der Flucht der Eingabezeile, und zwischen „Suche löschen“ und „Tabelle“ fehlte er ganz. Der Abstand sitzt jetzt links; die Zeile endet bündig.
- **„Gespeicherte Filter“ aus der Seitenleiste entfernt.** Die Schaltfläche stand an deren auffälligster Stelle, obwohl sie selten gebraucht wird, und zeichnete ihre Ecken gegen den Fensterhintergrund statt gegen die Kartenfläche – daher der dunkle Block darum. Der Manager bleibt über „Ansicht › Gespeicherte Filter …“ und die App-Aktionen erreichbar.

### Pinnwand

- **Mehr Fläche:** Raster, Vorschau, Auto-Anheften und „Finden“ stehen in der Zeile „Liste · Pinnwand“; die Statuszeile „1 von 1 Karten …“ ist entfallen. Zusammen rund achtzig Pixel mehr Höhe.
- **Frei anordnen ist der Standard**; vorhandene Pinnwände behalten ihre gespeicherte Wahl.
- **Kartenhöhe folgt dem Inhalt** statt fester 250 Pixel; in der geordneten Ansicht füllt jede Spalte ihre eigene Höhe.
- **Bildvorschau** für PNG-, GIF- und PPM-Anhänge auf der Karte, je Pinnwand abschaltbar. JPEG bräuchte eine zusätzliche Bibliothek und bleibt außen vor.
- **„Alle Punkte anheften“** und ein Schalter, der neue Punkte der Liste automatisch anheftet. Doppelklick auf die freie Fläche öffnet die Punktauswahl.
- **„Alle Karten finden“ räumt auf, statt umzuschalten:** Die freie Anordnung bleibt, die Karten kommen an aufgeräumte Positionen zurück.
- **Kein Flackern mehr beim Verschieben.** Über der Fläche lag ein gestricheltes Rechteck, das bei jeder Mausbewegung neu gezeichnet wurde; beim Ablegen baute Glide die gesamte Oberfläche neu auf. Jetzt wandert die Karte selbst mit dem Zeiger, und es wird nur die Pinnwand neu gezeichnet. Dasselbe gilt für ihre Schalter.
- **Waagerechte Bildlaufleiste im App-Stil.** Sie war als einzige Fläche eine native ttk-Leiste im Systemstil; `ThemedAutoScrollbar` kann jetzt auch quer.
- Kartenpositionen bleiben wie bisher je Pinnwand gespeichert. `pinboards` erhält additiv `preview` und `auto`.

### Mausbedienung und Darstellung

- **Gedrücktes Mausrad zieht die Fläche** in Aufgabenbaum, Seitenleiste, Startseite und Pinnwand; **Shift und Mausrad** schieben quer. Knopf 2 war app-weit dem Kontextmenü zugeordnet – unter macOS richtig, weil Tk den Rechtsklick dort so meldet, unter Windows und Linux blockierte es das Schnellscrollen. Die Zuordnung gilt jetzt nur noch unter macOS.
- **Farbmodus „Kontrast · farbenblindenfreundlich“**: Palette nach Okabe und Ito, die bei Rot-Grün-Schwäche unterscheidbar bleibt, dazu deutlich stärkerer Text- und Linienkontrast. Farbe bleibt nie die einzige Auskunft.
- **Farbmodus „Dopamin · kräftige Farben“**: dunkle Flächen wie im Dunkelmodus, darauf kräftigere Töne, und eine kurze Rückmeldung beim Abhaken und beim Erreichen des Tagesziels. Beide Modi schalten die Materialoptik mit Glaskanten ab, weil sie Kontrast kostet. Additiv als `color_mode` in `settings.json`, frei mit Hell und Dunkel kombinierbar.

### Daten, Prüfung und Dokumentation

- Aufgabenformat **16**, Einstellungen **2**, Vorlagen **2**. Additive Einstellungsfelder: `today_plan_migrated`, `table_column_widths`, `table_sort`, `home_tile_order`, `home_tiles_hidden`, `home_columns`, `color_mode`; `pinboards` erhält `preview` und `auto`. `today_plan` entfällt nach der Migration.
- Neue Suite `tests/integration/test_features322.py`; `test_features312.py` prüft jetzt das zusammengeführte Tagesmodell. Der Prüfstand wächst von 25 auf **26 Suiten**.
- Vorlagenkatalog, Beispieldaten und Releaseplanung sind für Format 16 neu erzeugt; die Vorgängerstände liegen im jeweiligen `archiv/`.
- Vier neue Fachdokumente: Tagesmodell, Checkliste, Ansichten und Startseite, Pinnwand und Darstellung. Alle fortgeschriebenen Dokumente sind vor der Änderung im `archiv/` gesichert.
- Keine neue Laufzeitabhängigkeit.

## 3.21.4 – 14.09.2026

- Ablageprüfung am 15.09.2026: Die neue Regel R6 erkannte irrtümlich das Wortende in `Vorlagenformat 2` als Aufgabenformat. Eine Wortgrenze verhindert diese Fehlalarme; positive und negative Gegenproben für R6 bis R8 bestanden. Zusätzlich verbliebene Formatangaben, Kalenderzusagen, historische Prüfstände und Linkziele korrigiert.
- Der vollständige Ablagelauf fand außerdem einen tagesabhängigen Fehler beim Beispielabgleich: Feste Erinnerungen wurden als absolute UTC-Zeitpunkte verglichen, obwohl der Erzeuger sie relativ zum Erzeugungstag setzt. `pruefen.py` vergleicht jetzt ihren Tagesabstand und ihre Ortszeit; die absolute Releaseprüfung bleibt unverändert. Paket, Neuerzeugung, Sommerzeitwechsel und absichtlich falsche Zeiten wurden gegengeprüft. Der erste fehlgeschlagene Prüflauf bleibt als Nachweis erhalten.

- Korrekturstand aus einem vollständigen Durchgang durch **alle 93 aktiven Dokumente** der Ablage. Anlass war die Frage, ob die Dokumentation inhaltlich stimmt – nicht nur, ob die Standzeilen zur Version passen. Der Durchgang hat Befunde ergeben, die keine maschinelle Prüfung finden konnte, weil sie Aussagen über Verhalten betreffen.
- **Zehn aufgeführte falsche Aussagen über den Anwendungscode**, jede gegen `src/glide/app.pyw` geprüft:
  - `43_AENDERUNGSVERLAUF_3.19.0.md` nannte die Nutzdatendatei `glide_liste.json`. Sie heißt `liste_speicher.json` (`SAVE_FILE`); der falsche Name kam in keinem anderen Dokument und in keiner Codezeile vor.
  - `45_KALENDERIMPORT_3.21.0.md` führte eine **Zeilenobergrenze**, die es nicht gibt – der ICS-Import kennt nur `MAX_ICS_IMPORT_EVENTS` (2000) und `MAX_ICS_IMPORT_BYTES` (12 MB). Der Wortlaut war aus dem CSV-Vertrag übernommen, wo Zeilen und Spalten wirklich begrenzt sind.
  - Derselbe Vertrag versprach, **erledigte** Termine zu überspringen. Ein `VEVENT` hat keinen Erledigt-Zustand; `STATUS` kennt dort nur `TENTATIVE`, `CONFIRMED` und `CANCELLED`, und der Code prüft ausschließlich `CANCELLED`. `VTODO` ist ausdrücklich ausgeschlossen.
  - `44_KALENDERAUSGABE_3.20.0.md` schrieb „Ohne Fälligkeit gibt es keinen Termin" und „Punkte ohne Fälligkeit erscheinen nicht". Die Ausgabe erzeugt aus einem Bearbeitungstag **auch ohne Fälligkeit** einen Planungstermin – genau der Fall, für den die Option gedacht ist, fiel nach dem alten Wortlaut heraus.
  - Derselbe Vertrag zeigte `BYDAY=MO,DI` als Ausgabe. `DI` ist kein zulässiges `BYDAY`-Token; `ICS_WEEKDAYS` enthält ausschließlich `MO,TU,WE,TH,FR,SA,SU`.
  - Und er stützte die Aktualisierung im Kalender auf `UID` **und** `SEQUENCE`. `SEQUENCE` steht im Code fest auf `0` und steigt nie – die Identität trägt allein die stabile UID; ob ein Kalender den Termin ersetzt, entscheidet er selbst.
  - `41_DRUCK_UND_PDF_3.17.0.md` versprach die **mitgelieferte** DejaVu Sans in der Druckdatei. Die Schnitte werden nur prozesslokal registriert (`FR_PRIVATE` unter Windows, Prozessumfang unter macOS); das Anzeigeprogramm der Datei sieht sie nicht, und die Datei enthält ausdrücklich keine Web-Schrift.
  - `43_AENDERUNGSVERLAUF_3.19.0.md` wechselte im selben Satz von 400 auf 412 Zeilen.
- **Fünf überholte Formatstufen** in fortgeschriebenen Dokumenten: `SECURITY.md` „Formate 4 bis 12", `06_DATA_BACKUP_MIGRATION.md` „Formate 4–14", `decisions/PRODUCT_IDENTITY.md` vier Werte auf Format 13 und App-Version 3.14.0, `src/glide/README.md` „Datenformat 13", `27_VORLAGEN_PRAXISANLEITUNG.md` „Format 14 und benötigen Glide ab 3.14". Lesbar sind 4 bis 15. `PRODUCT_IDENTITY.md` ordnete zusätzlich die lokalen Erinnerungen Format 14 zu – sie kamen mit Format 13 in 3.8.0.
- **Neue Regeln R6 bis R8 in `tests/tools/standpruefung.py`**: Eine Formatstufe in einer Standangabe muss `DATA_SCHEMA_VERSION` entsprechen, ein Formatbereich muss von `MIN_PORTABLE_BACKUP_SCHEMA_VERSION` bis dorthin reichen, und eine Tabellenzeile „Datenformat" oder „App-Version" nennt die aktuellen Werte. Die Werte liest das Werkzeug über den Syntaxbaum aus `app.pyw` – ein Import würde Tk starten und den echten Nutzerdatenordner anfassen. Drei der fünf Formatbefunde hätte das mechanisch gefunden. Der Änderungsverlauf ist ausgenommen: Dort war „Formate 2 bis 9" damals richtig.
- **Acht Verweise zeigten auf ein anderes Ziel als ihr Linktext.** Viermal führte „Produktdatenblatt" auf den Ordner-README statt auf das Datenblatt, zweimal hieß eine Vorschlagsliste „Aktuelle Funktionsübersicht", einmal verwies der Probelisten-README für vier Funktionen aus 3.10 bis 3.13 auf den 3.9-Vertrag, und `30_Release_Exports/README.md` bot den 3.13-Vertrag als „Bedienung und Änderungen" an.
- **Sieben Gegenwartsbehauptungen in historischen Dokumenten**: „Dieses Dokument beschreibt den aktuellen lokalen Python-/Tk-Quellstand" (`08_CODE_BEFUND.md`), „liegen inzwischen die aktuellen Aufgabenbackups" (`28_ABLAGEPRUEFUNG`), „verweisen inzwischen auf den 3.13-macOS-Gesamtlauf" (`30_DOKUMENTATIONSABGLEICH`), „für 3.14.0 steht der bestätigende Gesamtlauf noch aus" (`25_FEATURE_ABGLEICH`, tatsächlich am 13.09.2026 nachgeholt), „Nächste Schritte: … Reiteransicht und Pinnwand" (`12_ABSCHLUSSBERICHT`, seit 3.10.0 umgesetzt), „2. Reiteransicht angehen" (`decisions/SYSTEMBENACHRICHTIGUNGEN.md`) und drei Stellen in `50_Ablage/QA/Dokumentation/README.md`, darunter „Die aktuelle App-Prüfung liegt unter `tests/qa-3.13.0/`". Alle ins Präteritum gesetzt oder mit der Umsetzung versehen.
- **Zwei Widersprüche zwischen Dokumenten** aufgelöst: `50_Ablage/README.md` nannte `10_Dokumentation` die „aktuelle Word-Arbeitsgrundlage", während dieser Ordner-README die Word-Berichte als archiviert und die Markdown-Dokumente als aktuelle Quelle führt; und dieselbe Datei verlangte, Renderläufe bis auf den letzten zu archivieren, während der Renderlauf-README festhält, dass keiner gelöscht wurde.
- **Vier eigene Zählfehler aus 3.21.3 berichtigt**, im Änderungsverlauf und in den Notizen: es sind **zwanzig** versionierte Releaseplanungen (nicht neunzehn, mit 3.21.4 jetzt einundzwanzig), **zehn** archivierte startbare Fassungen 3.14.0 bis 3.21.2 (nicht neun), und den gemeinsamen Satz über die durchgehende Grundlage tragen **vier** Dokumente, nicht sechs – Produktdatenblatt und Probelisten-README führen ihre eigene Funktionstabelle. Der 3.21.3-Eintrag trägt außerdem die Farbkorrektur nach, die dort fehlte.
- Das Ergebnis eines Prüflaufs steht ab jetzt in den Dokumenten **derselben** Version: Der 3.21.3-Lauf (macOS, Python 3.14.5, 14.09.2026, 20:45, Exitcode 0, siebenunddreißig von neununddreißig Schritten) ist im aktuellen QA-Bericht und in der Weitergabe eingetragen; die archivierten Technischen Fakten zu 3.21.3 behalten ihren ursprünglichen Wortlaut. Bis 3.21.2 stand das Ergebnis immer erst in den Dokumenten der nächsten Version – dadurch behauptete jeder Stand, sein eigener Prüflauf stehe noch aus.
- `tests/tools/README.md` und `src/glide/README.md` werden jetzt **mit dem Quellstand ausgeliefert** und gehen über den SHA-256-Abgleich, wie die beiden Testberichte seit 3.21.3. Beide trugen Angaben, die bei jedem Stand hätten mitgehen müssen: „Achtzehn Suiten" bei tatsächlich 25, „Format 14", „für 3.14", „Windows-Nachweis: Python 3.12.7" ohne Datum und Stand, und eine Funktionsliste, die bei 3.13 endete. Die Werkzeugtabelle nennt jetzt auch `standpruefung.py` und `vorlagendaten.py` und ihre Zwecke ohne Versions- und Formatzahlen.
- Anwendungscode unverändert: keine Änderung an `src/glide/app.pyw` außer der Versionsangabe. Aufgabenformat bleibt 15, Einstellungen 2, Vorlagen 2. Unverändert 25 Suiten, drei Analysen und neununddreißig Schritte im Vollmodus. Keine neue Laufzeitabhängigkeit.

## 3.21.3 – 14.09.2026

- Neues Prüfwerkzeug `tests/tools/standpruefung.py`, als dritte Analyse im Prüfstand eingehängt. Es prüft jede aktive Markdown-Datei der Ablage gegen `VERSION`. Anlass: **Sieben Dokumente standen zwei Versionssprünge lang auf 3.21.0** – Repository-README, Dokumentationsindex, Bestandsanalyse, Abschlussbericht, Feature-Abgleich, `10_Dokumentation/README.md` und das Produktdatenblatt. Der Prüfstand konnte das nicht finden: Er prüft Dokumente auf Indexeintrag und erreichbare Links, nie auf Aktualität ihrer Aussage. Ein Dokument kann vollständig verlinkt und dennoch inhaltlich überholt sein.
- Das Werkzeug unterscheidet **fortgeschriebene** von **festgeschriebenen** Dokumenten: Festgeschrieben ist, was eine Version oder ein Datum im Dateinamen trägt, in einem Versionsordner liegt oder „historisch" im Titel führt. Fünf Regeln: eine Standzeile mit der aktuellen Version (R1), keine allein stehende überholte Angabe in einer Standzeile (R2), **keine Behauptung über den aktuellen Stand mit fremder Version in irgendeinem Dokument** (R3), keine fremde Version in der Standzeile eines versionsbenannten Dokuments (R4), kein älterer Titel als der Dateiname (R5). Genau R5 trifft „# Glide Produktdatenblatt 3.21.0" in `Produktdatenblatt_3.21.2.md`.
- Sechs historische Dokumente trugen ein von Hand gepflegtes Banner „Aktueller Entwicklungsstand: …" – in `08_CODE_BEFUND`, `28_ABLAGEPRUEFUNG` und `30_DOKUMENTATIONSABGLEICH` auf **3.14.0**, in `11_BESTANDSANALYSE`, `12_ABSCHLUSSBERICHT` und `25_FEATURE_ABGLEICH` auf **3.21.0**. Ein solches Banner rottet zwangsläufig. Die Banner sind durch einen Verweis ohne Nummer auf Index und QA-Bericht ersetzt; damit kann diese Fehlerklasse in historischen Dokumenten nicht wiederkehren. Dieselbe Behandlung erhielten die vier Prosastellen „Der aktuelle … Stand ist Glide 3.13.0/3.21.0".
- `09_PROJECT_HANDOFF.md` behauptete an drei Stellen gleichzeitig, 3.15, 3.16 und 3.21 seien „das zuletzt umgesetzte Funktionspaket", und nannte als „nächste offene Ideen" den dauerhaften Änderungsverlauf und den CSV-Import – beide seit 3.19 beziehungsweise 3.18 umgesetzt. Das Dokument ist neu geordnet: eine Aussage zum aktuellen Funktionspaket, die Vorgänger als Bestandsabschnitte, eigene Abschnitte für 3.21.1 bis 3.21.3 und eine Ideenzeile, die nur Offenes nennt.
- Die Funktionsübersichten waren lückenhaft. Der Repository-README nannte zwölf vorhandene Funktionen nicht, `09_PROJECT_HANDOFF.md` fünf, der Wurzel-README vier (Anhänge, Hell- und Dunkelmodus, Papierkorb, Punktarten), die Weitergabe zwei und das Produktdatenblatt eine (Schnellerfassung). Wurzel-README, Repository-README, Projektübergabe und Weitergabe tragen jetzt denselben Satz über die durchgehende Grundlage; Produktdatenblatt und Probelisten-README führen ihre eigene Funktionstabelle – ein Wortlaut, der beim nächsten Stand an einer Stelle gepflegt und übernommen wird.
- `tests/README.md` und `tests/fixtures/README.md` sind neu gefasst und werden **mit dem Quellstand ausgeliefert** statt durch Fortschreibungsregeln geflickt; beide gehen damit über den SHA-256-Abgleich. Der Testbericht beschrieb „achtzehn Suiten" und „zwei Analysen" bei tatsächlich 25 Suiten, der Fixture-Bericht verwies auf `glide_releaseplanung_3.14.0.glidebackup` und nannte Releaseplanungen „bis 3.13" als historisch.
- Neu dokumentiert: Die **zwanzig versionierten Releaseplanungen** in `tests/fixtures/beispiele/` liegen absichtlich alle aktiv und gehören nicht ins Archiv. Die Fixtureprüfung erwartet bei versioniertem Dateinamen genau dessen Version und belegt damit jede Formatstufe. Ohne diesen Hinweis räumt der nächste Durchgang sie auf und nimmt dem Prüfstand seine Migrationsbelege.
- In `07_Python-Versionen` lagen **zehn überholte startbare Fassungen** (3.14.0 bis 3.21.2) aktiv neben der aktuellen, während das Archiv nur bis 3.13.0 reichte: Seit 3.14 hat niemand nachgezogen. Sie liegen jetzt im Archiv, und der Ordner-README sagt das auch. Drei Übertragungspakete aus `Claude outputs` sind nach `50_Ablage/Archiv/Uebertragungspakete` verschoben.
- `tests/tools/releasedaten.py` trug noch vier Versionsangaben als Literal – in der Bestandsmemo, im Verweis auf den maßgeblichen Prüflauf, im Ordnernamen der Releaseplanung und in der Listennotiz. Genau diese Art von Angabe stand bis 3.21.1 sieben Versionen lang falsch im Releasebestand, ohne dass der Abgleich es finden konnte: Er vergleicht die Fixture mit ihrer eigenen Neuerzeugung. Alle vier sind an `APP_VERSION` und `DATA_SCHEMA_VERSION` gebunden.
- Der QA-Bericht trägt das Ergebnis des maßgeblichen 3.21.2-Laufs nach: macOS, Python 3.14.5, 14.09.2026 um 15:04, Exitcode 0, sechsunddreißig von achtunddreißig Schritten ausgeführt; übersprungen blieben allein die plattformgebundene Screenshot-Erzeugung und die Sichtprüfung. Ergänzt ist außerdem, dass 3.19.0 und 3.20.0 keinen eigenen macOS-Lauf haben und durch den 3.21.1-Lauf abgedeckt sind – im Bericht stand bei beiden „steht noch aus", ohne diesen Zusammenhang.
- `tests/tools/beispieldaten.py` legte die Liste „Kalender, Erinnerungen und Tagesplanung“ mit `color="due_soon"` an. Der Wert steht nicht in `LIST_COLOR_KEYS`; die App verwirft eine unbekannte Farbe still, die Liste hatte deshalb seit 3.21.2 **keine Farbe**. Der Fixture-Abgleich kann das nicht finden – die Neuerzeugung verwirft denselben Wert genauso. Jetzt `import` (Braun), und der `Builder` bricht bei unbekannter Farbe ab.
- Anwendungscode unverändert: keine Änderung an `src/glide/app.pyw` außer der Versionsangabe. Aufgabenformat bleibt 15, Einstellungen 2, Vorlagen 2. Unverändert 25 Suiten; die Analysen wachsen von zwei auf drei, der Vollprüflauf von achtunddreißig auf neununddreißig Schritte. Keine neue Laufzeitabhängigkeit.

## 3.21.2 – 14.09.2026

- Der mitgelieferte Beispielbestand deckt die Funktionen seit 3.14 jetzt wirklich testbar ab. Bisher enthielt er **keine einzige Erinnerung**, obwohl die Anleitung das Gegenteil behauptete, führte nur einen Bearbeitungstag und einen geschätzten Aufwand und kannte von den sechs Wiederholungsarten nur zwei. Tagesplanung, Tageskapazität und der Kalenderrundlauf ließen sich damit nicht sinnvoll ausprobieren.
- Neue Liste „Kalender, Erinnerungen und Tagesplanung" im Ordner „Website-Betrieb": sechs Punkte auf demselben Bearbeitungstag mit 270 Minuten Gesamtaufwand – darunter einer ohne Schätzung und ein erledigter, damit die Rechenregeln aus 3.15 sichtbar werden –, ein Punkt auf dem Folgetag für den Tageswechsel, beide Erinnerungsarten (relativ 30 Minuten vor dem Termin, fest am Vortag um 8 Uhr) und **alle sechs Wiederholungsarten**. Die Wochentagsregel trägt ein Enddatum: genau der Fall, der bis 3.21.0 beim Kalenderrundlauf um einen Tag verrutschte.
- Ein Long-Task in derselben Liste beschreibt den Rundlauf aus 3.20 und 3.21 in vier Schritten – exportieren, Datei ansehen, importieren, Duplikaterkennung prüfen – samt Gegentest mit ersetzten UIDs. Ein Anhang an der Liste zeigt, dass die Kalenderausgabe rein lesend bleibt.
- Der Beispielbestand wächst damit von 149 auf 166 Punkte und von 11 auf 12 Listen; Fälligkeiten von 27 auf 35, Uhrzeittermine von 4 auf 7, Bearbeitungstage von 1 auf 7, Aufwandsangaben von 1 auf 6. Alle Zusicherungen der Suiten sind Untergrenzen und bleiben unverändert gültig.
- `tests/tools/releasedaten.py` bindet seine Standangaben an `APP_VERSION` und `DATA_SCHEMA_VERSION`. Bis 3.21.1 hing an jedem Codebeleg unverändert der Zusatz „Stand: 3.14.0 / Datenformat 13" und im Kopf eine Memo-Zeile mit derselben überholten Angabe – sieben Versionen alt. Der Abgleich fand es nicht, weil er die Fixture mit ihrer eigenen Neuerzeugung vergleicht. `DATA_SCHEMA_VERSION` ist jetzt eine Modulkonstante und speist zugleich die vorhandene Zusicherung, dass die App dieses Format schreibt.
- Die Probedateien in `05_Probelisten_Testdaten` sind auf 3.21.2 erneuert. Sie standen auf **3.14.0 und Aufgabenformat 14**, während der Ordner-README „Glide 3.21.1" mit Aufgabenformat 15 behauptete und im Text noch „Die neuen Backups sind Format 14" sagte. Acht überholte Fassungen lagen aktiv im Ordner, obwohl der README sie im Archiv verortete.
- Mehrere READMEs nannten einen überholten Stand, weil die Version dort in Fettschrift oder mit anderem Trenner steht und die Fortschreibung sie übersprang: Wurzel-README und `01_Repository/Glide/README.md` standen auf 3.21.0, `10_Dokumentation` ebenso, `50_Ablage/QA/Dokumentation` auf 3.13.0 mit Datenformat 13. Die Fortschreibung erfasst diese Schreibweisen jetzt.
- Der QA-Bericht trägt das Ergebnis des maßgeblichen 3.21.1-Laufs nach: macOS, Python 3.14.5, Exitcode 0, sechsunddreißig Schritte ausgeführt, übersprungen blieben allein die plattformgebundene Screenshot-Erzeugung und die Sichtprüfung. Damit ist 3.21.1 automatisiert abgenommen – einschließlich Beispiel- und Releaseabgleich, der seit 3.19 nie grün werden konnte.
- Zwei überholte Testfassungen (`test_glide_3.12.0_vor_3.13.0.py`, `test_glide_36_3.12.0_vor_3.13.0.py`) lagen im aktiven Suitenordner und liegen jetzt unter `tests/integration/archiv/`.
- Der Vorlagenkatalog zeigte die Funktionen seit 3.14 nicht: Über alle 16 Vorlagen und 283 Punkte gab es **keinen Bearbeitungstag, keine Aufwandsangabe** und von den sechs Wiederholungsarten nur `woechentlich`. Eine Planungsvorlage konnte die Tagesplanung aus 3.15 damit nicht bedienen. Jetzt tragen „Tagesplanung", „Wochenplanung" und „Haushalt" Bearbeitungstag und Aufwand (je 10 Punkte), und der Katalog deckt **alle sechs Wiederholungsarten** ab, eine davon mit Enddatum. Die Wochenregel aller übrigen Haushaltspunkte bleibt erhalten.
- Erinnerungen bleiben im Vorlagenkatalog **bewusst** außen vor: Eine Vorlage soll beim Import keine Benachrichtigungen anlegen. Beide Erinnerungsarten sind im Beispielbestand abgedeckt, wo sie hingehören.
- Zwei Suiten hatten einen tageszeitabhängigen Fehler: `test_features320.py` und `test_features321.py` legten einen Punkt mit Fälligkeit **heute 14:00** und relativer Erinnerung von 30 Minuten an. Ab 13:30 Ortszeit lieferte die Erinnerungsverarbeitung mitten im Lauf aus und schrieb `delivered_key` und `delivered_at` in den Punkt, dazu einen Verlaufseintrag – die Zusicherungen „Abbrechen ändert nichts" und „Die Ausgabe verändert keine Daten" schlugen dann zufällig fehl. Nachgewiesen mit einem gezielten Vergleichslauf. Beide Termine liegen jetzt in der Zukunft; sechzehn Läufe in Folge sind grün. Der abgenommene 3.21.1-Lauf hatte diese Stelle um vier Minuten knapp passiert.
- Anwendungscode unverändert: keine Änderung an `src/glide/app.pyw` außer der Versionsangabe. Aufgabenformat bleibt 15, Einstellungen 2, Vorlagen 2. Gesamtsuite unverändert 25 Suiten, keine neue Laufzeitabhängigkeit.

## 3.21.1 – 14.09.2026

- Fehlerbehebung im Kalenderrundlauf: Das Enddatum einer Wiederholung überlebte „exportieren, importieren" nur in der Zeitzone UTC. Die Ausgabe schrieb `UNTIL` als UTC-Zeitpunkt (`…T235959Z`), obwohl `DTSTART` in schwebender Ortszeit beziehungsweise als reines Datum steht. Der Import rechnete die Angabe folgerichtig in Ortszeit um und landete östlich von Greenwich einen Tag zu spät, westlich einen Tag zu früh. `UNTIL` trägt jetzt dieselbe Zeitform wie `DTSTART`: ohne „Z" beim Uhrzeittermin, als Datum beim Ganztagstermin – so, wie RFC 5545 es verlangt.
- Fehlerbehebung beim Lesen fremder Kalender: `UNTIL` ist die Obergrenze einer Terminreihe, kein Zeitpunkt, den jemand abliest. Die neue Methode `parse_ics_until` nimmt den Kalendertag der Angabe, ohne Zeitzonenumrechnung. Fremde Programme schreiben das Tagesende üblicherweise als `…T235959Z`; wer das als Zeitpunkt in Ortszeit holte, verlängerte die Reihe östlich von Greenwich um einen Tag. Unlesbare Angaben werden weiterhin verworfen und gezählt, nicht geraten.
- Fehlerbehebung im Prüfstand: Der Beispiel- und Releaseabgleich in `--modus voll` konnte seit 3.19 nie gleich ausfallen. `inhalt_normalisieren` blendete `exported_at`, `deleted_at` und `added_at` aus, nicht aber das Feld `at` der Verlaufseinträge. Der Verlauf entsteht beim Speichern und trägt den echten Zeitpunkt, eine Neuerzeugung liefert also zwangsläufig andere Werte. Die Verlaufszeiten bleiben jetzt genauso draußen wie `exported_at`; Art, Aktion, Ziel, Liste und Anzahl werden weiterhin verglichen.
- Der Prüfstand führt Suiten jetzt in einer Zone mit Versatz aus (`TZ=Europe/Berlin`), wenn der Aufrufer keine vorgibt. In UTC ist jeder Zeitzonenfehler unsichtbar, weil der Versatz null ist – genau deshalb war der `UNTIL`-Fehler in der Linux-Vorabumgebung grün und fiel erst im macOS-Lauf auf. Ein gesetztes `TZ` bleibt unangetastet, damit sich jede Zone gezielt nachstellen lässt.
- `test_features321.py` prüft das Enddatum jetzt in vier Zonen von `America/New_York` bis `Pacific/Kiritimati`, in allen drei Schreibweisen (Ortszeit, Datum, fremdes UTC) und lehnt unbrauchbare Angaben ab. `test_features320.py` sichert die Zeitform der Ausgabe. Gesamtsuite unverändert 25 Suiten; Aufgabenformat bleibt 15, keine neue Laufzeitabhängigkeit.
- Beispiel-/Releaseplanung, Vorlagenkatalog und startbare Python-Fassung auf 3.21.1 abgestimmt. Der fehlgeschlagene Lauf zu 3.21.0 bleibt als `tests/qa-3.21.0/abschluss` erhalten, damit die Prüfhistorie nachvollziehbar ist.

## 3.21.0 – 14.09.2026

- Kalenderimport aus ICS: Termine einer Kalenderdatei werden Aufgaben mit Fälligkeit. Gelesen werden Titel, Beginn mit und ohne Uhrzeit, Dauer als geschätzter Aufwand (aus `DURATION` oder `DTEND`), Beschreibung, Ort als angehängte Zeile, Kategorien als Labels, Priorität als Wichtigkeit, abbildbare Wiederholungsregeln und Erinnerungen.
- Erreichbar über Datei → „Kalenderdatei (ICS) importieren …", die App-Aktionen sowie die Kontextmenüs von Liste und Listenhintergrund. Der Dialog nennt Kalendername, Erzeuger und Terminzahl, zeigt eine Vorschau der ersten acht Termine und erlaubt sechs Inhaltsoptionen, einen Zeitraumfilter (alles, ab heute, letzte zwölf Monate und später) sowie die Wahl zwischen neuer und geöffneter Liste.
- Ein wiederkehrender Termin wird **eine** Aufgabe mit Wiederholungsregel. Übernommen werden `FREQ=DAILY` (auch mit `INTERVAL`), `WEEKLY` (auch mit `BYDAY`), `MONTHLY`, `YEARLY` und `UNTIL`. Was Glide nicht genauso abbilden kann – `COUNT`, `BYMONTHDAY`, `BYSETPOS`, Intervalle bei Wochen, Monaten und Jahren –, wird verworfen und gezählt statt still vereinfacht; die Aufgabe entsteht dann ohne Wiederholung.
- Zeitangaben: Ortszeit bleibt Ortszeit, UTC wird umgerechnet, `TZID` nutzt die Zeitzonendatenbank der Standardbibliothek und fällt mit Hinweis auf Ortszeit zurück, wenn das System sie nicht mitbringt. Ganztägige Mehrtagestermine landen auf ihrem ersten Tag.
- Eigene UIDs (`glide-<Punkt-ID>@glide.local`) werden erkannt: Der Rundlauf „mit 3.20 schreiben, wieder einlesen" legt keine Kopien an. Fremde UIDs werden nicht gemerkt – derselbe Fremdkalender zweimal importiert ergibt zweimal Aufgaben; ein Abgleich wäre eine Synchronisierung und bleibt offen.
- Übersprungen und mit Grund gezählt werden Termine ohne Titel, ohne Beginn, mit `STATUS:CANCELLED`, außerhalb des Zeitraums und bereits aus Glide stammende. Der Parser liest gefaltete Zeilen, escapte Sonderzeichen, CRLF und LF, BOM sowie Parameter in Anführungszeichen; Grenzen sind 2000 Termine und 12 MB je Datei, geprüft vor jeder Bestandsänderung.
- Der Import ist ein einzelner Rückgängig-Schritt einschließlich neu angelegter Labels; bestehende Punkte werden nie überschrieben. Keine Synchronisierung, kein Abonnement, kein Netzzugriff, keine Teilnehmer, Anhänge oder Ausnahmetermine, keine `VTODO`-Einträge. Aufgabenformat 15, Einstellungsformat 2 und Vorlagenformat 2 bleiben unverändert; keine neue Laufzeitabhängigkeit.
- Neue Integrationssuite `test_features321.py` für Rundlauf samt Duplikaterkennung, Parser, Zeitzonen, Dauerangaben, alle abbildbaren und sechs nicht abbildbare Wiederholungsregeln, vier Erinnerungsfälle, alle Übersprungsgründe, Zeitraumfilter, Grenzen, beide Importziele, Rückgängig und Dialog. Gesamtsuite jetzt 25 Suiten. Beispiel-/Releaseplanung, Vorlagenkatalog und startbare Python-Fassung auf 3.21 abgestimmt.

## 3.20.0 – 14.09.2026

- Kalenderausgabe als ICS: Fälligkeiten werden als Kalenderdatei geschrieben, die Apple Kalender, Outlook, Thunderbird und Google Kalender einlesen. Vier Umfänge – aktuelle Liste oder Ordner, alle Listen, „Mein Tag und heute Fällige", Tagesplanung des gewählten Tages.
- Punkte mit Uhrzeit werden Termine mit Beginn und Ende, Punkte ohne Uhrzeit Ganztagstermine. Die Dauer kommt aus dem geschätzten Aufwand, sonst gilt eine halbe Stunde. Wichtigkeit wird zur Priorität, Labels werden Kategorien, Beschreibung, Quellliste und Aufwand stehen in der Terminbeschreibung.
- Wiederholungen erscheinen als `RRULE` (alle sechs Arten samt `UNTIL`), Erinnerungen als `VALARM` – relativ als `TRIGGER:-PT…M`, fest als UTC-Zeitpunkt. Bearbeitungstage lassen sich als eigene Ganztagstermine mitausgeben.
- Termine stehen in schwebender Ortszeit, damit keine Zeitzonentabelle mitgeliefert werden muss, die mit jeder Sommerzeitreform veraltet; nur Dateizeitstempel und feste Erinnerungen stehen in UTC. Die UID je Punkt bleibt stabil: Wer die Datei erneut einliest, aktualisiert seine Termine statt sie zu verdoppeln.
- Erreichbar über Datei → „Kalenderdatei (ICS) …", die App-Aktionen sowie die Kontextmenüs von Liste und Listenhintergrund. Sechs Inhaltsoptionen einzeln zuschaltbar; die Kopfzeile des Dialogs nennt vorab die Zahl der Termine und der übersprungenen Punkte ohne Fälligkeit.
- RFC-5545-konformer Aufbau: UTF-8, CRLF, Faltung bei 75 Oktetten, Escaping von Backslash, Semikolon, Komma und Umbruch. Geschrieben wird atomar; Nutzdatendateien sind als Ziel ausgeschlossen, ab 2000 Terminen endet die Ausgabe mit Hinweis. Die Ausgabe verändert weder Aufgaben noch Einstellungen und erzeugt keinen Verlaufseintrag.
- Keine Synchronisierung und kein Rückweg aus dem Kalender, keine `VTODO`-Ausgabe, keine Teilnehmer, Orte oder Ausnahmetermine. Aufgabenformat 15, Einstellungsformat 2 und Vorlagenformat 2 bleiben unverändert; keine neue Laufzeitabhängigkeit.
- Neue Integrationssuite `test_features320.py` für Aufbau aller Umfänge, Termintypen, Dauerregeln, alle Optionen, alle Wiederholungsarten, beide Erinnerungsarten, Escaping und Faltung, stabile UIDs, Obergrenze, Dateischreibung und den Dialog in beiden Themes. Gesamtsuite jetzt 24 Suiten. Beispiel-/Releaseplanung, Vorlagenkatalog und startbare Python-Fassung auf 3.20 abgestimmt.

## 3.19.0 – 13.09.2026

- Dauerhafter Änderungsverlauf: Anlegen, Ändern, Erledigen, Wiederöffnen, Verschieben, Umbenennen, Papierkorb, Wiederherstellen und endgültiges Entfernen werden mit Zeitpunkt, Objektnamen, Liste und – bei Änderungen – den betroffenen Feldern protokolliert. Der Verlauf übersteht Programmneustarts und schließt die Lücke zwischen Rückgängig (nur bis zum Programmstart) und Papierkorb (nur gelöschte Objekte).
- Der Verlauf entsteht beim Speichern aus dem Vergleich zweier Stände, nicht an jeder Bedienstelle einzeln. Dadurch ist jede Änderung erfasst, gleich über welchen Weg sie kam – Klick, Tastatur, Kontextmenü, Mehrfachbearbeitung, Ziehen, Import, Vorlage, Serienvorrücken –, und er benennt das Ergebnis einer Änderung statt der Absicht dahinter.
- Eigene Ansicht über **Ansicht → „Änderungsverlauf …"**, Strg/Cmd+H und die App-Aktionen: Tabelle mit Zeitpunkt, Vorgang, Objekt und Liste, Suche über alle Felder, Zeitraumfilter (heute, 7 Tage, 30 Tage) und Artfilter (Punkte, Listen und Ordner, Papierkorb), Ausgabe als Textdatei und Leeren nach Rückfrage.
- Ab 25 gleichartigen Ereignissen eines Speichervorgangs entsteht ein Sammeleintrag mit Anzahl, damit ein Import mit hunderten Zeilen das Protokoll nicht flutet. Obergrenze 4000 Einträge; die ältesten fallen weg. Namen werden auf 120 Zeichen gekürzt, Beschreibungs- und Anhangsinhalte nicht mitgeschrieben.
- In den Einstellungen abschaltbar („Änderungen protokollieren"). Ausgeschaltet entstehen keine neuen Einträge, vorhandene bleiben lesbar. Rückgängig stellt den Bestand wieder her und lässt die Einträge stehen – die Rücknahme erscheint als weiteres Ereignis.
- **Aufgabenformat 15**: `history` liegt neben den Aufgabenfeldern. Ein Bestand im Format 14 oder älter wird beim ersten Speichern gehoben und erhält ein leeres Protokoll; vorher entsteht die unveränderte Kopie `liste_vor_format15_<Zeitstempel>.json` im Backup-Ordner. Ein defektes oder fremdes `history`-Feld wird beim Laden verworfen, ohne die Aufgaben zu berühren. Komplettbackup und App-Backup führen den Verlauf mit, ein Teilbackup als Auszug nicht. Einstellungsformat 2 und Vorlagenformat 2 bleiben unverändert; keine neue Laufzeitabhängigkeit.
- Neue Integrationssuite `test_features319.py` für Migration samt Originalkopie, jeden erfassten Vorgang, Feldlisten, Verschieben, die drei Papierkorbvorgänge, Sammeleinträge, Obergrenze, Backup-Rundlauf, defekte Verlaufsfelder, abschaltbare Erfassung, Leeren, Filter und den Dialog in beiden Themes. Gesamtsuite jetzt 23 Suiten; neues Referenz-Fixture `current_v15/reference_v15.json`; `test_features318.py` vergleicht Bestände ohne das Protokoll. Beispiel-/Releaseplanung, Vorlagenkatalog und startbare Python-Fassung auf 3.19 abgestimmt.

## 3.18.0 – 13.09.2026

- CSV-Import mit Spaltenzuordnung: Glide liest CSV-Dateien beliebiger Herkunft. Trennzeichen (Semikolon, Komma, Tabulator, senkrechter Strich) und Kodierung (UTF-8 mit und ohne BOM, Windows-1252, UTF-16) werden erkannt und sind im Dialog umstellbar; die Kopfzeile wird erkannt und lässt sich zu- und abschalten.
- Zwölf Zielfelder sind zuordenbar: Aufgabentext (Pflicht), Beschreibung, Erledigt, Wichtigkeit, Fälligkeit, Uhrzeit, Art, Labels, Bearbeitungstag, Aufwand sowie Ebene und Nummer für die Verschachtelung. Die Zuordnung wird aus den Spaltennamen vorbelegt – eigene Exportbezeichnungen sowie gängige deutsche und englische Schreibweisen.
- Eine mit „Als CSV“ geschriebene Liste ist vollständig zurücklesbar: Struktur, Art, Erledigt-Zustand, Wichtigkeit, Fälligkeit mit Uhrzeit, Labels, Bearbeitungstag und Aufwand. Die Vorschau zeigt die ersten acht Zeilen so, wie Glide sie anlegen würde.
- Ziel ist eine neue Liste (Titel aus dem Dateinamen, in der Ordneransicht im geöffneten Ordner) oder die geöffnete Liste. Erreichbar über Datei → „CSV importieren …“, die App-Aktionen und die Kontextmenüs von Liste und Listenhintergrund.
- Zeilen ohne Aufgabentext und nicht lesbare Zellen werden gezählt und mit Zeilennummer genannt, ohne die übrigen Zeilen zu verwerfen. Gruppen und Überschriften übernehmen keine Status- und Fristangaben; eine Überschrift erhält keine Unterpunkte. Grenzen: 5000 Zeilen, 64 Spalten, 12 MB je Datei, geprüft vor jeder Bestandsänderung.
- Ein Import ist ein einzelner Schritt und mit Rückgängig vollständig zurücknehmbar, einschließlich der dabei neu angelegten Labels. Bestehende Punkte werden nie überschrieben. Aufgabenformat 14, Einstellungsformat 2 und Vorlagenformat 2 bleiben unverändert; keine neue Laufzeitabhängigkeit.
- Neue Integrationssuite `test_features318.py` für Erkennung, Zuordnung, Werteregeln, Verschachtelung, Importziele, Grenzen, Bericht, Rückgängig und Dialog. Gesamtsuite jetzt 22 Suiten; `test_ui39.py` an die zweite CSV-Aktion angepasst. Beispiel-/Releaseplanung, Vorlagenkatalog und startbare Python-Fassung auf 3.18 abgestimmt.

## 3.17.0 – 13.09.2026

- Druck- und PDF-Ausgabe in vier Formaten: Tageszettel für heute, aktuelle Liste oder Ordner, Tagesplanung des gewählten Tages und Checkliste zum Abhaken.
- Glide schreibt eine eigenständige HTML-Druckansicht mit Druck-CSS (A4, Seitenumbruchregeln) und öffnet sie im Standardprogramm; dessen Druckdialog druckt auf Papier oder speichert als PDF. Alternativ lässt sich die Datei direkt als HTML speichern. Kein eigener PDF-Schreiber, keine neue Laufzeitabhängigkeit, keine externen Verweise in der Datei.
- Einzeln zuschaltbar: erledigte Punkte, Beschreibungen, Labels, Fälligkeit und Wiederholung, Bearbeitungstag und Aufwand, Ankreuzkästchen vor jedem Punkt sowie freie Notizzeilen am Ende. Übersichten nennen zusätzlich die Quellliste.
- Erreichbar über Datei → „Drucken und PDF …“, Strg/Cmd+P, die App-Aktionen und das Kontextmenü einer Liste. Gruppen und Überschriften behalten Art und Einrückung; ab 2000 Punkten wird mit Hinweis abgeschnitten.
- Die Ausgabe liest nur vorhandene Objekte und verändert weder Daten noch Einstellungen; Nutzdatendateien sind als Druckziel ausgeschlossen, geschrieben wird atomar.
- Neue Integrationssuite `test_features317.py` für Grundgerüst aller Formate, Escaping, jede Option einzeln, Mengen je Format, Ordnerdruck, Obergrenze, Dateischreibung und den Dialog in beiden Themes. Gesamtsuite jetzt 21 Suiten. Beispiel-/Releaseplanung, Vorlagenkatalog und startbare Python-Fassung auf 3.17 abgestimmt.

## 3.16.0 – 13.09.2026

- Vollständiges App-Backup: Aufgaben, Anhänge, persönliche Einstellungen, Vorlagenkatalog und Aktivitätsdaten liegen gemeinsam in einem Archiv mit der Endung `.glideapp`. Der Zusatzteil steht neben den Aufgabenfeldern, deshalb bleibt die Datei für ältere Glide-Fassungen ein lesbares Aufgabenbackup.
- Wiederherstellung mit Inhaltsvorschau: Vor dem Überschreiben zeigt Glide Erzeugerversion, Datenformat, Zeitstempel, Aufgaben, Listen, Ordner, Gruppen, Labels, Papierkorbeinträge, Anhänge, Vorlagen und erfasste Aktivitätstage. Jeder der vier Bereiche ist einzeln zuschaltbar; nicht enthaltene Bereiche bleiben gesperrt.
- Die Aufgaben laufen durch denselben geprüften Importpfad wie ein Komplettbackup, einschließlich Sicherung des vorherigen Stands. Einstellungen und Vorlagen werden vor dem Ersetzen als eigene Kopien im Backup-Ordner gesichert; scheitert eine Sicherung, bleibt der alte Stand bestehen.
- Ohne die Aufgaben desselben Archivs werden Reiter, Pinnwände, Tagesauswahl, gespeicherte Filter, Tabellenspalten und die Liste zuletzt bearbeiteter Listen nicht übernommen: Sie verweisen auf Punkte, die dann fehlen würden. Aktivitätsdaten sind ein eigener Bereich und überschreiben die Jahresanzeige nur auf Wunsch.
- Aufgabenformat 14, Einstellungsformat 2 und Vorlagenformat 2 bleiben unverändert. Keine neue Laufzeitabhängigkeit, kein Netzzugriff, keine Cloudsicherung.
- Neue Integrationssuite `test_features316.py` für Archivaufbau, Rundlauf, Vorschauwerte, ungültige und fremde Archive, Teilbereiche, Rückfallsicherungen, Abbruch und Dialoge in beiden Themes. Gesamtsuite jetzt 20 Suiten. Beispiel-/Releaseplanung, Vorlagenkatalog und startbare Python-Fassung auf 3.16 abgestimmt.

## 3.15.0 – 13.09.2026

- Neue Systemansicht „Tagesplanung": alle Aufgaben mit Bearbeitungstag an einem wählbaren Tag, sortiert nach Wichtigkeit, Fälligkeit und Titel. Tageswechsel über „◀“/„▶“, das Ansichtsmenü und die App-Aktionen.
- Neue persönliche Einstellung „Tageskapazität · Minuten" (0–1440, Vorgabe 0 = kein Vergleich). Aufgabenformat 14, Einstellungsformat 2 und Vorlagenformat 2 bleiben unverändert.
- Aufwandsbilanz an einer Stelle gebündelt: Summen in Tagesplanung, „Mein Tag", Tabellenansicht und auf der Startseite. Punkte ohne Schätzung werden gezählt statt geraten, erledigte bleiben in der Summe und werden getrennt ausgewiesen, der Kapazitätsrest nennt immer die Bezugsgröße.
- Kontextmenü der Tagesplanung verschiebt oder entfernt den Bearbeitungstag, ohne die Fälligkeit anzutasten; Serien leeren den Bearbeitungstag beim Vorrücken wie bisher.
- Keine Zeiterfassung, keine automatische Terminverteilung, keine Auslastungsbewertung und keine gespeicherte Tagesbilanz. Keine neue Laufzeitabhängigkeit.
- Neue Integrationssuite `test_features315.py` für Rechenregeln, Grenzwerte, Einstellungsrückfall, Ansicht, Filter, Punktaktionen, Serien, Startseite und Einstellungsdialog in beiden Themes. Gesamtsuite jetzt 19 Suiten. Beispiel-/Releaseplanung und startbare Python-Fassung auf 3.15 abgestimmt.

## 3.14.0 – 13.09.2026

- Optionaler Bearbeitungstag und geschätzter Aufwand in Minuten für Aufgaben und Long-Tasks, unabhängig von Fälligkeit und „Mein Tag“.
- Gemeinsame Eingabe in Punktdetails und Mehrfachbearbeitung; neue Tabellenspalten und Angaben im Punktreiter. Nicht angehakte Felder bleiben bei Mehrfachbearbeitung erhalten.
- Kopien, Papierkorb, Vorlagen und Backups bewahren die Angaben. Relative Vorlagen verschieben auch Bearbeitungstage ohne Fälligkeit. Serien leeren den Bearbeitungstag beim Vorrücken und behalten den Aufwand.
- Aufgabenformat 14 mit Originaldateisicherung vor der ersten Migration. TXT-Rundlauf und Markdown-/CSV-Export erweitert; CSV-Spalten werden angehängt.
- Neue Integrationssuite für Planung, Datenmigration, Sicherungsfehler, Aktionen, Austausch und Dialoge in beiden Themes. Gesamtsuite jetzt 18 Suiten. Unterlagen, Beispiel-/Releaseplanung und startbare Python-Fassung auf 3.14 abgestimmt.
- Dokumentationsabgleich 13.09.2026: Versions-, Format- und Prüfstandsangaben in Index, Produktgrenzen, QA-Bericht, Abschlussbericht, Funktionsabgleich und den äußeren Arbeitsdokumenten vereinheitlicht. `FORM_KEYS` in `test_datenintegritaet.py` auf den Feldsatz von Format 14 ergänzt; der wiederholte Vollmodus-Lauf besteht mit Exitcode 0 und achtzehn Suiten. Kein Programmcode geändert. [Protokoll](docs/archiv/38_DOKUMENTATIONSABGLEICH_2026-09-13.md).

## 3.13.0 – Kompakte Tabellenansicht (13.09.2026)

- Aufgaben einer Liste flach und kompakt in den Spalten Aufgabe, Art, Fälligkeit, Wichtigkeit, Labels und Status anzeigen.
- Suchfeld, Offenfilter, Auswahl, Leertaste, Kontextmenü und Detaildialoge arbeiten mit denselben Aufgabenobjekten wie die Listenansicht.
- Sichtbare Spalten über „Spalten …“ je Liste wählen; die Einstellung wird additiv in `settings.json` gespeichert.
- Gruppen und Zwischenüberschriften bleiben strukturell erhalten und werden für die Tabelle als enthaltene Aufgaben flach dargestellt.
- Eigenständige Regression für Filter, Objektidentität, gemeinsame Aktionen und Spaltenpersistenz ergänzt.

## 3.12.0 – Bewusste Tagesauswahl „Mein Tag“ (13.09.2026)

- Aufgaben aus mehreren Listen unabhängig von ihrer Fälligkeit für den aktuellen Tag auswählen.
- Eigene „Mein Tag“-Ansicht mit Reihenfolge, Erledigungsstatus, Quelllisten und direktem Öffnen.
- Hinzufügen und Entfernen über Aufgabenmenü, Seitenleiste, Startseite und Ansichtsmenü; veraltete Referenzen werden bereinigt.
- Tagesauswahl liegt additiv in den Einstellungen, wird beim Tageswechsel automatisch geleert und verändert weder Aufgaben noch Fälligkeiten.
- Regression für listenübergreifende Referenzen, Persistenz, Tageswechsel-Schutz und identische Aufgabenobjekte ergänzt.

## 3.11.0 – Schnellerfassung und gespeicherte Filter (13.09.2026)

- Schnellerfassung aus jeder Glide-Ansicht über Kopfzeilen-Schaltfläche und Strg/Cmd+Alt+N; Eingang als Standard, direkte Ziellistenauswahl und Mehrfacherfassung.
- Deutsche Fristvorschau für heute, morgen, Wochentage, relative Tage/Wochen und Datumswerte mit optionaler Uhrzeit.
- Gespeicherte Filter über Listen, Labels, Status, Wichtigkeit, Fälligkeit und Suchtext; relative Zeiträume werden beim Öffnen neu berechnet.
- Filtermanager, Bearbeiten, Löschen, Vorschau der Trefferzahl, entfernte Referenzen und additive Persistenz in Einstellungen; Aufgabenformat 13 bleibt unverändert.
- Regression für Parser, Datenidentität, Undo, dynamische Filter, Schreibfehler und beide Ansichten ergänzt.

## 3.10.0 – Reiter und Pinnwand (13.09.2026)

- Aufgaben, Long-Tasks und Gruppen gezielt als Reiter öffnen; vollständige Details, Anhänge und Unterpunkte mit gemeinsamer Bearbeitung. Zwölf offene Punktreiter, Übersicht, Reihenfolge und Tastaturwechsel.
- Pinnwände für Listen und Ordner einschließlich Unterlisten: vorhandene Punkte anheften, Label-/Textfilter, geordnete Karten oder freie Anordnung, Raster, drei Kartenbreiten und Tastaturbedienung.
- Reiter schließen und Karten abheften ändern ausschließlich die Ansicht. Punkte, IDs, Wiederholungen und Papierkorb bleiben dieselben; verschwundene Referenzen werden entfernt.
- Offene Reiter, aktive Ansichten und Pinnwände liegen additiv in Einstellungen. Aufgabenformat 13, Einstellungsformat 2 und Vorlagenformat 2 bleiben erhalten.
- Eigenständige Regression für Identität, Neustart, Erledigen/Undo, Serien, Papierkorb, Filter, Drag-/Tastaturbewegung und beide Themes.


## 3.9.0 – Einheitliche Oberfläche und Bedienung (12.09.2026)

- App-weite Umbenennung von Erinnerungen zu Benachrichtigungen; thematische Übersicht und Zähler in der kompakten Kopfzeile.
- Einstellungszahnrad; Light/Dark Mode im Einstellungsdialog mit gespeicherter Auswahl.
- Durchsuchbare App-Aktionen für sämtliche eigenen Datei-/Bearbeiten-/Ansicht-/Hilfebefehle einschließlich Untermenüs.
- Ein-/ausblendbare Seitenleiste mit gespeicherter Einstellung und voller Breite für Inhalt/Aktionsleisten.
- Gemeinsame grafische Dropdowns auf allen Plattformen, direkt im Elternfenster ohne separate Fenster oder eigenen Grab. Einheitliche Schließ- und Tastaturbedienung; Regression für Außerklick-Blockierung.
- Neue Listen/Ordner nach tatsächlicher Formularhöhe, Zweispaltenmodus bei knappem Bildschirm; thematische Felder und grafische Labelauswahl.
- Gleichmäßige Abstände am Vorlagenbutton „Verwenden“.
- Aufgabenformat 13, Einstellungen 2 und Vorlagenformat 2 unverändert; neue additive Einstellung `sidebar_visible`. Keine Änderung an Zustellung, Backups oder technischen `reminder`-Feldern.


## 3.8.0 – Aufmerksamkeit bei Erinnerungen 12.09.2026

- Eine neu zugestellte Erinnerung hebt den Eintrag in Taskleiste bzw. Dock hervor: einmal je Prüflauf, ohne Fokusdiebstahl, abschaltbar in den persönlichen Einstellungen.
- Windows blinkt über `FlashWindowEx`, macOS fordert Aufmerksamkeit über das Dock an; beides über bereits vorhandene `ctypes`-Wege, keine neue Laufzeitabhängigkeit.
- Kein Anstoß ohne gespeicherten Zustellbeleg, keiner bei offenem Bearbeitungsdialog, keiner ohne neue Zustellung.
- Echte Systembenachrichtigungen bleiben offen: Sie setzen eine registrierte, installierte Anwendung voraus. Ein Hilfsprozess mit Autostart ist ausgeschlossen.

Begründung, Stufen und Grenzen: [Systembenachrichtigungen](docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md).

## 3.8.0 – Lokale Erinnerungen 12.09.2026

- Feste einmalige und relative Erinnerungen direkt in der Aufgabenmaske; sichtbarer Standard 09:00 Uhr bei ganztägigen Fristen.
- Gemeinsame Übersicht mit Aufschub, Bestätigung, Öffnen und Erledigen; verpasste Termine nach Start oder Pause gesammelt.
- Gespeicherte Zustellbelege gegen Duplikate, Serienbezug und lokale Zeitumstellungen; Hinweise innerhalb der laufenden App.
- Aufgabenformat 13 mit additiver Migration und unrotierter Originalsicherung. Backup/Restore und isolierte Regressionen ergänzt.
- „Aufgabe öffnen“ aus der Übersicht hebt eine aktive Suche auf und markiert die Aufgabe in ihrer Quellliste, statt sie auszublenden.
- Keine neue Laufzeitabhängigkeit, kein Hintergrunddienst; Systembenachrichtigungen bei beendetem Programm bleiben offen.

Details und Grenzen: [Erinnerungen 3.8.0](docs/archiv/31_ERINNERUNGEN_3.8.0.md).

## 3.7.0 – Dynamische Übersicht 12.09.2026

- Dokumentationsabgleich: Funktionsmatrix, aktuelle Einstiege, Produktdatenblatt und Chatweitergabe aktualisiert; historische Prüfstände und Vorgänger nachvollziehbar archiviert.

- Ordner- und Listenkacheln mit eigener Inhaltshöhe in ein bis drei unabhängig gestapelten Spalten; keine gemeinsamen Rasterzeilen und keine redundante Typzeile.
- Rundum 16 Pixel Innenabstand und 12 Pixel zwischen Kacheln. Vollständig beschriftete Öffnen-/Bearbeiten-Aktionen brechen bei Bedarf um; Tastaturfokus scrollt sie ins Sichtfeld.
- Leere Übersicht mit Hinweis über die volle Breite. Bestehende Inhalte, Reihenfolge, Farben und Bearbeitungsziele bleiben erhalten.

Details: [Dynamische Kachelübersicht](docs/archiv/29_DYNAMISCHE_KACHELN_3.7.0.md).

## 3.7.0 – Nachbesserung 11.09.2026

- Zweiter UI-Nachtrag: Vorlagenbaum mit Listenstil, gerundeter Fläche, dynamischen Metadatenspalten und App-Scrollleiste; aufgeklappte Zweige bleiben beim Bearbeiten erhalten.
- Mac-Auswahlfelder einschließlich Popup in App-Farben; Tastaturauswahl, Abbruch und Rückgabe an modale Dialoge. Windows verwendet unverändert das bisherige OptionMenu.
- Mac-Trackpad-Ereignisse von Tk 9 und kleine Mausradbewegungen werden durchgehend verarbeitet.
- Vollständig thematisierter Vorlageneditor mit Struktur, den vorhandenen Detailmasken, Labels, Anhängen und verlustfreier Sortierung. Abbruch verwirft den isolierten Entwurf.
- 16 ausführliche Praxisvorlagen, darunter Immobilienvermarktung, WordPress, WEG und Baukommunikation.
- Vorlagenformat 2 mit optionalen relativen Terminen; Format 1 bleibt lesbar und wird vor dem ersten Überschreiben gesichert. Aufgabenformat bleibt 12.
- Listenübersicht mit Typ, Fortschritt, Labels und drei getrennten nächsten Aufgaben.
- Beispielbackups, Dokumentation und Python-Arbeitskopie aktualisiert; alte Arbeitsstände nachvollziehbar archiviert.
- Zusätzliche Regression für Datenisolierung, Migration, Wiederverwendung und Tk-9-Scrollen; plattformunabhängiger .pyw-Testlader.


## 3.7.0 – 07.09.2026

- Kompakte Listen-/Ordnerkacheln in voller Breite mit außenliegender Scrollleiste und direktem Bearbeiten.
- Zweispaltige Seitendetails mit Farben, Labels und lokalen Anhängen.
- Datenformat 12 mit additiver Migration und unrotierter Originalkopie vor dem ersten Speichern älterer Daten; Containeranhänge in Backups, Importen, Vorlagen und Papierkorb.
- Zuverlässiges Mausrad über Startseitendiagrammen und Label-Chips, kein Scrollen ohne Überlauf auf der Vorlagenseite.
- Wochentag/Datum/Bearbeitungszahl beim Hover im Jahresraster; Erläuterung der nach dem Löschen erhaltenen Tageswerte.
- Nur das Listen-Symbol der Seitenüberschrift optisch abgesenkt.
- Version, Referenzformat 12, Beispieldaten und Releaseplanung fortgeschrieben; gezielte 3.7-Suite ergänzt.

Details und Nachweise: [Version 3.7.0](docs/archiv/24_VERSION_3.7.0.md).

## 3.6.0 – 06.09.2026

Weiterer UI-Nachtrag vom 07.09.2026:

- „Listen“ mit Symbol und anklickbarer Kachelübersicht aller normalen Listen,
  Ordner und Unterordner; ein bis drei Spalten, Inhaltsvorschau und feste
  untere Aktionsgruppen. Letzte Ansicht wird beim Neustart wieder geöffnet.
- Vorlagen ohne Hinweiszeile und leere Scrollreserve, mit gerundeten Kacheln,
  kompakter Namensspalte und den gewohnten Zwischenflächen unter den Aktionen.
- Jahresanzeige erhält ältere Erledigungstage auch nach den ersten neuen
  Bearbeitungen, ohne Doppelzählung oder Umschreiben der Historien.
  Wochentage sitzen an ihren Zeilen, beide Diagramme nutzen dieselbe Breite.
- Neun App-/Audit-Suiten einschließlich neuer Layout-, Historien- und
  Navigationsregressionen mit isolierten Daten.

Details: [Kachelübersicht und Jahresanzeige](<docs/archiv/23_KACHELUEBERSICHT_UND_JAHRESANZEIGE_3.6.0_vor_Nachbesserung_2026-09-11.md>).

Nachbesserung anhand von 14 UI-Rückmeldungen (interner 3.6.0-Stand):

- Einheitliche runde Outline-Buttons mit farbiger Hover-Füllung auch auf der
  Startseite, in der Datumswahl, bei Datenordneraktionen und im Windows-Menü.
- Willkommen-Aktionen mit Kalender; bei schmaler Inhaltsbreite nur Eingang,
  Vorlagen und Einstellungen. Lange Listenverweise brechen lesbar um.
- Vorlagen in linksbündigen Spalten, kurze Textsymbole, korrekte Hintergründe
  in Hell/Dunkel. Aktionen bleiben unten außerhalb des Scrollbereichs und
  brechen bei Platzmangel vollständig in weitere Zeilen um.
- Jahresraster mit ausreichender dynamischer Höhe; Labelauswahl mit echtem
  Zeilenhover sowie festen Buttons „+ Neues Label“ und „Fertig“ unten.
- Einstellungen in zwei Spalten; Textlogo optisch angehoben. Akzentfarbe für
  Auswahlmarkierungen und Oberflächenaktionen, Lila als Voreinstellung;
  gespeicherte Listen-/Labelfarben bleiben davon unabhängig.
- Aufgabe und Gruppe besitzen verschiedene Standardfarben. Systemnavigation
  zeichnet die Textsymbole zwei Pixel oberhalb der bisherigen Position.
- Vier berechnete Hauptmondphasen unten rechts im Wochen-/Monatskalender,
  mit lokalem Kalendertag und erläuternden Hinweisen. Offline-Berechnung
  nach John Walkers gemeinfreiem Moontool, gegen USNO-Ereignisse geprüft.
- Eigene Regressionen für schmale Fenster, Farben, Hover, Symbolklicks,
  Aktionsleisten und Mondtermine. Aufgabenformat 11 bleibt unverändert.

Details und Prüfnachweis: [UI-Nachbesserung](<docs/archiv/22_UI_NACHBESSERUNG_3.6.0_vor_Nachbesserung_2026-09-11.md>).


Persönlicher Ausbau und sicherer lokaler Datenpfad bei unverändertem
Aufgabendatenformat 11.

- **Jahresanzeige:** 371 Tage lokale Erledigungshistorie, Aktivitätsfelder für
  53 Wochen, aktive Tage, Summe, bester Tag und laufende Serie.
- **Mondphase und Uhr:** Mondphase mit Name und Beleuchtungsanteil in der
  Startseiten-Kopfzeile; Sekundenzeiger, Mondphase und Jahresanzeige sind in
  den Einstellungen einzeln abschaltbar.
- **Vorlagen:** Separater Bestand in `vorlagen.json`, Listen- und
  Ordnervorlagen, Vorlagenansicht, Hinzufügen/Exportieren als
  `.glidetemplates` und Vorlagen aus bestehenden Listen oder Ordnern.
- **Teilbackups:** Listen und Ordner können als verlustfreies
  `.glidebackup`-Teilformat exportiert und über „Listen/Ordner hinzufügen“
  ergänzend importiert werden.
- **Datenordner:** Wechselbarer lokaler Datenordner mit Zeiger in
  `%APPDATA%\\Glide\\datenordner.json`; eine `glide.lock` warnt bei einem
  gleichzeitig geöffneten gemeinsamen Ordner. Der Umzug kopiert den Bestand
  und löscht den bisherigen Ordner nicht.
- **Schrift und Personalisierung:** Optionale TTF/OTF-Registrierung nur für den
  laufenden Prozess, Schriftfamilie/-größe und Wochenbeginn in den Einstellungen.

## 3.5.0 – 05.09.2026

Wiederkehrende Aufgaben. **Aufgabendatenformat 10 → 11** mit additiver Migration;
Format-10-Bestände und -Backups bleiben unverändert gültig. Keine neue
Laufzeitabhängigkeit, kein Hintergrunddienst, keine Benachrichtigungen.

- **Wiederholung am Punkt:** täglich, alle N Tage (1–365), an festen
  Wochentagen, wöchentlich, monatlich oder jährlich – wahlweise mit Enddatum.
  Auswählbar in der erweiterten Eingabe direkt unter der Fälligkeit; ohne
  Fälligkeitsdatum gibt es keine Wiederholung.
- **Beim Abhaken** rückt der Punkt auf seinen nächsten Termin vor und steht
  wieder offen. Es wird nichts im Voraus erzeugt und nichts dupliziert – eine
  tägliche Aufgabe hinterließe sonst in einem Jahr 365 abgehakte Zeilen. Was
  geschafft wurde, hält die Tageszahl der Startseite fest. Rückgängig nimmt das
  Vorrücken zurück.
- **Monats- und Jahresabstände** rechnen vom ursprünglichen Termin, nicht vom
  letzten: Der 31. Januar wird zum 28. Februar und danach wieder zum 31. März,
  statt dauerhaft auf den 28. zu rutschen.
- **Reihenende:** Ist das Enddatum überschritten oder findet die Regel keinen
  Termin mehr, bleibt der Punkt erledigt und verliert seine Regel.
- **Darstellung:** `↻` hinter dem Aufgabentext. Klartext („monatlich",
  „jeden Mo, Mi, Fr bis 31.12.2026") in Suche, TXT-Export und -Import.
- **Produktgrenzen:** Das Nicht-Ziel wurde getrennt. Wiederholungen sind jetzt
  Bestandteil des Produkts; Erinnerungen mit Benachrichtigung und Push-
  Infrastruktur bleiben ausdrücklich ausgeschlossen.
- **Migration:** Ein fehlendes Wiederholungsfeld heißt „wiederholt sich nicht".
  Alte Daten werden nicht umgeschrieben. Eine unvollständige oder unbekannte
  Regel wird verworfen statt geraten – sie dürfte sonst Termine erzeugen, die
  niemand gesetzt hat.
- **Prüfung:** neue Referenzdatei `tests/fixtures/current_v11/reference_v11.json`;
  der Format-10-Bestand bleibt Teil derselben Regressionsprüfung. Die Messung
  der Feldkanten in der Eingabemaske berücksichtigt jetzt nur sichtbare Felder.

### Nachtrag 05.09.2026 – Bereinigung und Windows-Prüfung

- Überholte Release-Fixtures archiviert, Dublettenordner nach vollständiger
  geprüfter Sicherung entfernt und eine zusätzliche Bildvorfassung erhalten.
- Releaseplanung zu Wiederholungen, Symbolen, Labelchips, Startseite und
  Store-Paketversion berichtigt; Format-11-Backup neu erzeugt und reproduziert.
- Windows-Vollmodus erfolgreich, zusätzliche 14 Maskenzustände geprüft,
  Symbolausgabe und Windows-Bilder am regulären Ort abgelegt.
- Aktuelle Einstiegstexte und äußere Ablagen fortgeschrieben, Originale archiviert.
  App-Quellcode, App-Version und Datenformate bleiben unverändert.

## 3.4.0 – 05.09.2026

### Nachtrag 05.09.2026 – Startseite neu aufgebaut

Nachgereicht innerhalb von 3.4.0: App-Version, Datenformat 10, Migration und
Aufgabendaten sind unverändert. Neue persönliche Einstellungen kommen additiv
in `settings.json` dazu; es kam keine Laufzeitabhängigkeit hinzu.

- **Kopfzeile:** flache, breite Zeile mit analoger Uhr (`AnalogClock`, aus
  Tk-Grundformen gezeichnet), Wochentag und Datum, dem nächsten anstehenden
  Termin in der Farbe seiner Liste und dem Sprung in die Kalenderansicht.
- **Willkommenskachel:** Textlogo links als farbige Fläche (`MonogramTile`,
  gerechnet wie ein Labelchip), Begrüßung rechts daneben, darunter eine
  wechselnde Aufforderung aus `HOME_PROMPTS`.
- **Textlogo:** Farbe aus der Palette von Listen, Aufgaben und Labels, unter
  **Bearbeiten → Einstellungen** wählbar – mit sofortiger Vorschau.
- **Tägliche Herausforderung:** Tagesziel in den Einstellungen, Fortschritt als
  Balken auf der Startseite. Gezählt wird der Übergang offen → erledigt,
  zentral in `item_change`; die Tageszahlen liegen lokal in `settings.json`.
- **Verweise:** Schnellzugriffe stehen nebeneinander statt untereinander –
  Eingang, In Bearbeitung, Verspätet, Labels, neue Liste, Einstellungen. Jede
  anklickbare Fläche der Startseite hat jetzt denselben Hover wie eine Zeile
  in der Seitenleiste.
- **Reihenfolge:** „Dein aktueller Bestand" steht ganz unten, mit farbigen
  Kennzahlen (erledigt grün, offen orange, Listen blau), Verweisen auf
  In Bearbeitung und Verspätet und einem Balkendiagramm der letzten sieben Tage.
- **Zuletzt bearbeitet:** drei statt sechs Einträge (`HOME_RECENT_VISIBLE`).
- **Vorlagen:** zehn statt drei; angeboten werden jeweils drei, und welche das
  sind, wechselt beim Zurückkehren zur Startseite.
- **Listenfarben:** Listen und Ordner tragen auf der Startseite ihre Farbe. In
  „In Bearbeitung" und „Verspätet" erbt ein Punkt ohne eigene Aufgabenfarbe die
  Farbe seiner Liste oder ihres Ordners (`inherited_list_color`). Eine
  ttk.Treeview färbt immer die ganze Zeile – es bleibt bei einer Farbe je Punkt.
- **Labelnamen:** bei der Eingabe höchstens 14 Zeichen
  (`LABEL_NAME_INPUT_LIMIT`, Maßstab „Freigabe nötig"). Die Speichergrenze
  bleibt bei 40 Zeichen, damit vorhandene Namen unangetastet bleiben.
- **Werkzeug:** `tests/tools/symbolpruefung.py` nennt je Symbol die Schrift, aus
  der Tk es tatsächlich zeichnet, und markiert jede Ersatzschrift. Damit lässt
  sich belegen, warum dieselben Zeichen auf zwei Systemen verschieden aussehen.

### Nachtrag 05.09.2026 – Oberflächen-Feinschliff

Nachgereicht innerhalb von 3.4.0: App-Version, Datenformat 10, Migration und
Nutzerdaten sind unverändert; es kam keine Laufzeitabhängigkeit hinzu.

- **Symbole:** Startseite `▣` statt `⌂`, Verspätet `▲` statt `‼`. Beide alten
  Zeichen fielen aus der Reihe – das Häuschen als feine Umrisslinie, das
  doppelte Ausrufezeichen als Satzzeichen. Die Ersatzzeichen stammen aus
  demselben Unicode-Block „Geometrische Formen“ wie `▼`, `◐`, `◈` und `▦` und
  haben damit dieselbe optische Größe und Strichstärke. Papierkorb,
  Themenschalter und Wichtigkeitsfähnchen bleiben bewusst unverändert.
- **Startseite:** Die Kacheln haben abgerundete Ecken im selben Radius wie
  Seitenleiste und Listenrahmen (`HOME_CARD_RADIUS`). Oben und unten liegen
  jetzt dieselben 18 Pixel Luft wie zwischen Seitenleiste und Inhalt
  (`HOME_EDGE_GAP`); der Zwischenraum von 12 Pixeln steht zwischen den
  Kacheln und nicht mehr zusätzlich hinter der letzten.
- **Begrüßung:** sieben feste Formulierungen in `HOME_GREETINGS`. Gewechselt
  wird beim Zurückkehren zur Startseite, nicht bei jedem Neuaufbau – Abhaken
  oder Speichern lässt den Satz stehen. Der Startpunkt ist je Programmstart
  zufällig, danach geht es reihum.
- **Fälligkeitsspalte:** Datum und Uhrzeit passen jetzt immer vollständig in
  die Zeile. Die Spaltenbreite bekommt eine an der Schrift bemessene Reserve
  (`TREE_CELL_RESERVE_CHARS`) für den inneren Zellenrand der Treeview und für
  Symbolzeichen, die Windows aus einer breiteren Ersatzschrift zeichnet;
  vorher fehlte dadurch das letzte Zeichen. Sobald irgendwo eine Uhrzeit
  gesetzt ist, gilt zusätzlich die volle Musterbreite als Untergrenze.
- **Intern:** `RoundedContainer` kann seine Höhe dem Inhalt folgen lassen
  (`auto_height`); kurzlebige Boxen tragen sich nicht mehr in die Themenliste ein.

Persönliche Startseite, Einstellungen und die gewünschten Darstellungsänderungen
auf Basis von 3.3.0. Aufgabendatenformat bleibt 10, keine neue Laufzeitabhängigkeit.

- **Seitenleiste:** Namen links, Aufgabenanzahl rechts in eigener Spalte; Ordner
  summieren Aufgaben ihrer Listen und Unterordner. Einzug 12 statt 20 Pixel.
  Namen nutzen die verfügbare Breite und werden erst bei Platzmangel gekürzt.
- **Liste:** feste 24 Pixel zwischen Titelzelle und sichtbaren Metadaten,
  12 statt 30 Pixel Zellreserve, 4 statt 16 Pixel rechte Abstandsspalte.
- **Textsymbole:** Eingang `▼`, Papierkorb `🗑`, Wichtigkeit `⚐`/`⚑`/`⚑⚑`,
  Gruppe `▸`, Beschreibung `≡`, alle über `ICONS`. Alte TXT-Gruppen- und
  Wichtigkeitsmarker werden weiterhin gelesen. Das Papierkorbzeichen verwendet
  seine Unicode-Standard-Textdarstellung; ein VS15 würde in Windows/Tk 8.6
  einen sichtbaren zusätzlichen Leerraum erzeugen.
- **Eingaben:** Farbnamen und Wichtigkeiten sind in Menüs und im ausgewählten
  Feld farbig. `PALETTE` bündelt die festen Farbwerte hinter Theme-Rollen.
- **Labels:** Hover/Auswahl beginnt hinter dem unverändert gefärbten Chip.
  Die festen Labels wechseln die Punktart direkt in derselben Eingabemaske;
  Artwahl und Labelwahl bleiben synchron. Entwürfe, Zeilenumbrüche, Termine
  und weitere Labels bleiben beim Hin- und Herwechsel erhalten. Speichern
  und Abbrechen bleiben auch beim Scrollen am unteren Fensterrand erreichbar.
- **Fenster:** App-eigene Meldungen, Rückfragen, Über Glide und Tastenkürzel
  folgen dem Theme. Tasten links fett, Wirkung rechts; lange Inhalte scrollen.
  Über Glide enthält Dank, persönliche Motivation und Shaye.de / mailme@shaye.de.
- **Einstellungen:** Begrüßungsname, Textlogo aus 1–3 Buchstaben/Ziffern,
  Startseite beim Öffnen und Bestandsstatistiken ein-/ausblenden.
- **Startseite:** aktueller Aufgabenbestand, heute fällige Listen, sechs zuletzt
  tatsächlich bearbeitete Listen, Vorlagen Tagesplanung/Projektstart/Einkauf.
  Vorlagen erzeugen unabhängige Listen und lassen sich rückgängig machen.
- **Speicherung:** persönliche Angaben bleiben in settings.json. Additive
  Normalisierung `settings_version=1`; vor der ersten Umstellung bleibt eine
  Kopie `settings.before-v1.json`. Aufgaben und Komplettbackups bleiben Format 10.
- **QA:** zwei neue isolierte Windows/Tk-Suiten ergänzen die drei bestehenden;
  Screenshots für beide Themes. Veraltete Ausgangsprüfungen zu Datum, Index und
  ausdrücklich historischen Fixture-Versionen korrigiert. Plattformgrenzen und
  Prüfergebnisse stehen in `docs/07_QA_BERICHT.md`.

## 3.3.0 – 04.09.2026

Neue Ansicht **Labels** in der Seitenleiste: der gesamte Bestand nach Labels
gruppiert, jeder Punkt in der Farbe seines Labels. Dazu Feinschliff an der
Liste – runde Labelchips, engere Spalten, ruhigere Ausrichtung.
Datenformat bleibt 10.

### Ansicht „Labels“

- **Zwischen „In Bearbeitung“ und „Verspätet“**, mit eigenem Symbol aus `ICONS`.
  Der Zähler nennt die Punkte mit mindestens einem eigenen Label; ein Punkt mit
  drei Labels bleibt darin ein Punkt.
- **Eine Gruppe je Label**, in der Reihenfolge der Labelverwaltung, gefolgt von
  **„Ohne Label“**. Gruppenzeile und Punkte tragen die Labelfarbe.
- **Ein Punkt mit mehreren Labels steht in jeder zugehörigen Gruppe.** Die
  Labelspalte zeigt dort die *übrigen* Labels: Das Label der Gruppe steht schon
  in der Gruppenzeile.
- **Drag & Drop tauscht das Label.** Der Zug aus einer Gruppe in eine andere
  ersetzt genau das Label der Herkunftsgruppe und lässt alle übrigen Labels des
  Punkts stehen; das neue Label tritt an die Stelle des alten, damit das in der
  Liste sichtbare erste Label seine Position behält. Aus „Ohne Label“ herausziehen
  vergibt ein Label, hineinziehen nimmt nur das Label der Herkunftsgruppe.
  `MAX_LABELS_PER_ITEM` wird dabei geprüft – ein Zug schneidet nie Labels ab.
- **Die beiden festen Labels bilden keine Gruppe.** „Long-Task“ und
  „Überschrift“ tragen die Art eines Punkts; ein Zug dorthin würde ihn umwandeln
  statt ihn zu etikettieren.
- Doppelklick, Enter und Rechtsklick verhalten sich wie in „In Bearbeitung“:
  Der Punkt wird in seiner Quellliste geöffnet oder dort geändert.
- Jede Änderung läuft durch den gemeinsamen Änderungsrahmen und ist damit
  rückgängig zu machen.

### Liste: Chips, Spalten, Ausrichtung

- **Labelchips werden nicht mehr an den Kanten beschnitten.** Die Fläche entsteht
  jetzt aus vier Kreisvierteln und zwei Rechtecken innerhalb der Zeichenfläche;
  das geglättete Polygon lag genau auf der Schnittkante, wodurch die Rundung
  verschwand. Der Auswahlrahmen folgt derselben Kontur.
- **Fälligkeits- und Labelspalte folgen dem tatsächlichen Inhalt.** Bisher waren
  sie so breit wie der längste überhaupt mögliche Fall (Datum mit Uhrzeit,
  ausgereizter Labelname mit Zähler); dazwischen stand eine leere Fläche. Die
  Musterwerte bleiben die Obergrenze, damit nichts abgeschnitten wird. Im
  Beispielbestand sinkt die Fälligkeitsspalte von 187 auf 127 und die
  Labelspalte von 290 auf 128 Pixel – der Aufgabentext gewinnt rund 70 Prozent.
- **Beide Spalten sind links ausgerichtet.** Rechtsbündig richteten sie sich am
  rechten Zellenrand aus, sodass Kalender- und Labelsymbol je nach Textlänge in
  jeder Zeile an einer anderen Stelle standen.
- **Die Fälligkeit weicht im schmalen Fenster.** `DUE_COLUMN_MIN_TREE_WIDTH`
  steigt von 470 auf 520: Der alte Wert lag unterhalb der Baumbreite, die bei der
  Fenstermindestgröße überhaupt entsteht, und griff deshalb nie.

### Nebenbei behoben

- **Zurücknehmen bleibt in der abgeleiteten Ansicht.** Wer in „Verspätet“ eine
  Änderung zurücknahm, landete in der zuletzt geöffneten Liste; wiederhergestellt
  wurden bisher nur „In Bearbeitung“ und der Papierkorb.

### Prüfstand

- Alle drei Suiten, beide Analysen und der Dokumentabgleich laufen grün
  (Linux/Xvfb, Python 3.12.3, Tk 8.6.14). Die Sichtprüfung erzeugt zwei neue
  Aufnahmen der Labelansicht in Hell und Dunkel.
- **Auf Windows und macOS ist der neue Stand nicht geprüft** – insbesondere das
  Ziehen zwischen Labelgruppen mit realer Maus, die Spaltenbreiten unter Segoe UI
  und die Darstellung der Chips bei anderer Anzeigeskalierung.

## 3.2.0 – 04.09.2026

Die automatische Übernahme von Nutzerdaten aus früheren Programmnamen entfällt.
Anhangs- und Fälligkeitssymbole kommen jetzt aus der zentralen Textzeichentabelle.
Drei weitere Symbolarten sind noch Emoji; siehe Bestandsanalyse.
Neu dabei: ein ausführlicher Beispielbestand zum Einlesen. Datenformat bleibt 10.

### Bestandsanalyse und Dokumentationsabgleich – 04.09.2026

- Repository-Dokumentation, Startkontext, Übergabe, Produktdaten und Word-
  Arbeitsgrundlage auf den tatsächlichen Stand 3.2.0 / Schema 10 abgeglichen.
  Vorherige Fassungen dezentral archiviert; historische Fixtures bleiben erhalten.
- Windows-Prüfung ausgeführt. Haupttest vom entfernten `system_box` auf die
  reale Baumgeometrie umgestellt; ein Pixel native Schriftmetrik-Toleranz beim
  Kopfblock, unverändert exakte Höhenprüfung mit/ohne Labels. Datenintegritätstest
  wartet beim Start auf Windows-Fenstermapping. Keine Änderung an `app.pyw`.
- `tests/tools/pruefen.py` bündelt Syntax, Versions-/Dokumentabgleich, Fixtures,
  drei Suiten, Analysen und im Vollmodus Reproduktion/Screenshotversuch.
- `tests/tools/releasedaten.py` erzeugt ein gemeinsames importierbares Backup
  mit Unterlagen & Assets, Vermarktungsstrategie und belegter Feature-Übersicht;
  recherchierte Vorgaben tragen Quelle und Abrufdatum.
- `docs/11_BESTANDSANALYSE.md` enthält Inventur, Widersprüche, belegte
  Grenzwertlücken und manuelle Restprüfungen. Die ursprüngliche Einfriermeldung
  bleibt nicht verifiziert; offene Fehler werden nicht als behoben ausgegeben.
- Übergabe und Auftragstext nachgezogen: `docs/09_ARBEITSAUFTRAG_BESTANDSANALYSE.md`
  ist als abgeschlossen markiert, verweist auf `docs/09_PROJECT_HANDOFF.md` und
  kennzeichnet überholte Plattformaussagen als historischen Stand. Die offenen
  Aufgaben im Handoff führen jetzt Punkttiefe und Systemlabel-Grenze, die Emoji
  außerhalb `ICONS` sowie die Umbauaktionen ohne Bestandswächter als P1;
  erledigte Punkte stehen im Erledigt-Abschnitt statt in der offenen Liste.
  Keine Änderung an `app.pyw`, Version und Datenformat unverändert.

### Entfernt: die Verzeichnis-Migration

- **`migrate_from_legacy_app_dirs`, `migrate_legacy_file` und `_legacy_app_data_dir`
  sind weg**, samt `LEGACY_APP_NAMES` und `LEGACY_BASE_DIR`. Sie haben beim Start
  geprüft, ob im Ordner einer früheren Programmfassung („Lokale Listen-App") oder
  im Skriptordner noch Daten liegen, und diese übernommen.
- **`LEGACY_LABEL_COLOR_MAP` ist weg.** Farbschlüssel aus der internen
  Testfassung 2.7.0 werden nicht mehr auf die Palette abgebildet; was nicht in
  der Palette steht, bekommt die Vorgabefarbe.

  **Folge, ausdrücklich:** Wer Glide auf einem Rechner startet, auf dem noch
  Daten unter einem alten Programmnamen liegen, beginnt jetzt mit einer leeren
  Ablage. Ein Komplettbackup einer älteren Fassung lässt sich weiterhin einlesen –
  die Formatprüfung und die `normalize_*`-Funktionen bleiben unverändert. Nur der
  automatische Griff in fremde Ordner beim Programmstart entfällt.

### Symbole: zentrale Textzeichen und dokumentierte Reststellen

- **`⊕` für Anhänge** statt `📎`, an allen drei Stellen: Anhangsliste in der
  Eingabemaske, Aufgabenbaum und Aufgabenübersicht.
- **`▦` für die Fälligkeit** statt `📅`, in der Datumsspalte und auf dem
  Kalenderknopf der Eingabemaske.
- **Zentrale Symbole kommen aus `ICONS`.** `DUE_COLUMN_ICON` und `LABEL_COLUMN_ICON`
  verweisen jetzt auf die Tabelle, statt ihr Zeichen selbst zu führen. Außerhalb der Tabelle
  bestehen noch Gruppen-, Wichtigkeits- und Beschreibungsmarker. Ihre Änderung
  ist offen; insbesondere beim Gruppenmarker ist TXT-Kompatibilität betroffen.
- Der Integrationstest prüft das dauerhaft: Jedes Zeichen in `ICONS` muss
  unterhalb von U+1F000 liegen. Ein versehentlich eingefügtes Emoji fällt damit
  beim nächsten Testlauf auf, nicht erst auf einem fremden Rechner.

Hintergrund: Farbige Emoji kommen aus einer Ersatzschrift des Systems
(Segoe UI Emoji, Apple Color Emoji). Sie ignorieren die Textfarbe, sind auf
Windows und macOS verschieden breit und passen nicht zuverlässig in die feste
Zeilenhöhe des Aufgabenbaums.

### Neu: Beispieldaten zum Einlesen

`tests/fixtures/beispiele/Glide_Beispieldaten.glidebackup` – ein
Komplettbackup, das sich über „Datei → Komplettbackup einlesen“ importieren
lässt.

| | |
|---|---|
| Ordner | 5, davon 2 verschachtelt |
| Listen | 10 |
| Punkte | 140 |
| davon Gruppen | 10 |
| davon Long-Tasks (Notizen) | 13 |
| davon Zwischenüberschriften | 25 |
| Labels | 9, über alle sieben Palettenfarben |
| Papierkorb | 3 Einträge (Liste, Ordner, einzelner Punkt) |

Inhaltlich ein Grafik- und Marketingarbeitsplatz im Wohn- und Städtebau:
Exposé-Produktion von der Datenübernahme bis zur Druckfreigabe, Website und
Redaktionsplan, eine Frühjahrskampagne mit Print, Außenwerbung und Digital,
Vermarktungsstart und Baustellenkommunikation eines Neubauvorhabens sowie ein
Ordner mit Gestaltungsregelwerk, Druckdaten-Checkliste und Textbausteinen.

Die Notizen sind echte Notizen, keine Platzhalter: Farbwerte mit Begründung,
Logo-Schutzraum, Bildsprache, Tonalität, Vorbereitung eines Fototermins. Fristen
entstehen relativ zum Erzeugungstag – überfällige, heutige und künftige Punkte
sind also immer vertreten.

- **Erzeugt von `tests/tools/beispieldaten.py`.** Der Inhalt steht dort im
  Quelltext; wer ihn ändern will, ändert ihn an einer Stelle und lässt das
  Werkzeug neu laufen.
- **Der Integrationstest liest die Datei** auf demselben Weg ein wie ein echter
  Import (Archivprüfung, Schemaprüfung, Normalisierung) und prüft Umfang,
  Artenverteilung, Labelverweise und Palettenabdeckung.

### Zahlen

| | 3.1.0 | 3.2.0 |
|---|---|---|
| Zeilen | 14.654 | 14.590 |
| Emoji im Quelltext | 5 Stellen | 0 |
| Symbolliterale außerhalb von `ICONS` | 2 | 0 |

## 3.1.0 – 04.09.2026

Aufräumversion. Kein neues Merkmal, keine geänderte Bedienung, kein neues
Datenformat (weiterhin 10). Was sich ändert, ist der Aufbau darunter: Zwei
Abläufe, die durch die ganze Anwendung hindurch wiederholt dastanden, gibt es
jetzt einmal – und mit ihnen verschwindet eine Fehlerklasse, die sich sonst bei
jeder neuen Aktion neu einschleichen konnte.

### Ein Rahmen für jede Änderung

- **`item_change` und `sidebar_change`** kapseln, was bisher an 36 Stellen
  wörtlich wiederholt stand: Rückgängig-Punkt anlegen, Änderung ausführen,
  speichern, neu zeichnen, Auswahl wiederherstellen – und bei ausgebliebener
  Wirkung den Rückgängig-Punkt wieder verwerfen. Wer den letzten Schritt vergaß,
  hinterließ einen Rückgängig-Schritt, der nichts zurücknimmt. Das kann jetzt
  nicht mehr passieren, weil der Rahmen ihn erzwingt.
- **`selected_items_for_change`** fasst die drei Vorbedingungen jeder
  Punktänderung zusammen: offene Liste, vorhandene Auswahl, Hinweis bei leerer
  Auswahl. Vorher standen sie sechsmal einzeln da.
- **Behoben: Eine wirkungslose Aktion kostete den ältesten Rückgängig-Schritt.**
  Bei vollem Speicher (20 Schritte) kürzte schon das Anlegen des
  Schnappschusses die Liste – auch dann, wenn die Aktion anschließend nichts
  bewirkte. Der Schnappschuss wird jetzt erst gekürzt, wenn feststeht, dass er
  bleibt.

### Modale Fenster: eine Stelle statt sieben

- **`run_modal` ist der einzige Weg, auf dem ein Dialog wartet.** Vorher standen
  `grab_set` und `wait_window` an sieben Stellen einzeln nebeneinander, und nur
  eine davon gab den Griff an das aufrufende Fenster zurück. Öffnete man aus
  einer Maske heraus einen weiteren Dialog – Farbauswahl, Namensabfrage,
  Listenauswahl –, blieb die Maske danach sichtbar, nahm aber keine Eingabe mehr
  an. Das ist der gemeldete „hängt sich auf"-Fall.
- **`modal_over` fragt jetzt Tk selbst**, wer den Griff hält (`grab_current`),
  statt darauf zu warten, dass jeder Aufrufer sein Fenster durchreicht. Damit
  greift die Absicherung auch dort, wo zwischen Maske und Unterdialog noch ein
  drittes Fenster liegt.

### Zusammengeführt und entfernt

- `on_sidebar_drag_end` war neun Ebenen tief verschachtelt und ist in
  `drop_sidebar_list` und `drop_sidebar_folder` geteilt.
- `outdent_selected` und `toggle_indent_selected` teilen sich
  `lift_item_to_parent_level`; beide beschrieben denselben Vorgang in eigenem
  Wortlaut.
- `sidebar_row_font`/`task_row_font` → `cached_font`,
  `_make_calendar_surface` → `_make_field(inner=…)`,
  `iter_all_list_objects`/`iter_all_folder_objects` → `iter_live_and_trashed`.
- `self.calendar_button_label` wurde gesetzt und nie gelesen; ein Kommentar
  beschrieb noch die selbstgezeichneten Ordner-Klappdreiecke, die es seit 3.0.1
  nicht mehr gibt. Beides entfernt.
- Neue Konstante `MAX_UNDO_STEPS` statt der Zahl 20 im Quelltext.

### Was ausdrücklich nicht angefasst wurde

- **Die Import- und Backup-Wege.** Sie haben eine eigene Rücknahme (den
  Labelbestand vor dem Einlesen) und einen eigenen Abbruchpfad. Sie in den
  gemeinsamen Rahmen zu zwingen hätte den datenkritischsten Teil der Anwendung
  ohne Gewinn umgebaut.
- **Die Rückwärtskompatibilität.** Die Freigabe, sie aufzugeben, brachte
  nachweislich nichts: Die Anwendung hat keine Migrationszweige je Formatversion,
  nur rund 110 Zeilen Verzeichnis-Migration. Siehe `docs/08_CODE_BEFUND.md`.

### Zahlen

| | 3.0.2 | 3.1.0 |
|---|---|---|
| Zeilen | 14.704 | 14.654 |
| Stellen mit `undo_stack.pop()` | 39 | 7 |
| Stellen mit `grab_set()` + `wait_window` | 7 | 1 |
| Wörtlich doppelte Blöcke | 111 | 102 |
| Funktionen über 80 Zeilen | 26 | 25 |
| Nie genannte Funktionen/Konstanten | 1 | 0 |
| Strukturgleiche Methodenpaare | 3 | 0 |

Die Zeilenzahl sinkt nur um 50, weil rund 110 Zeilen gemeinsamer Rahmen
hinzugekommen sind. Verschwunden sind rund 160 Zeilen Wiederholung – die
Rechnung, die zählt, steht in der Zeile darüber.

Alle drei Prüfläufe grün, Sichtprüfung hell und dunkel unverändert.

## 3.0.2 – 03.09.2026

Gruppen werden benutzbar, Labels lassen sich dort anlegen, wo man sie braucht.
Datenformat bleibt 10.

### Gruppen

- **Ein Punkt lässt sich in eine Gruppe ziehen.** Wer auf die Mitte einer Gruppenzeile zieht, legt den Punkt hinein; wer an den oberen oder unteren Rand zieht, sortiert daneben ein – dieselbe Unterscheidung wie in einem Dateimanager. Vorher ging Hineinlegen nur über Shift+Ziehen, was man kennen musste. Der Vorgang läuft unter dem Bestandswächter wie jede andere Umbauaktion.
- **Eine leere Gruppe sagt „(leer)" statt „(0)".** Die Null ließ offen, wofür sie steht.
- **Neu: `docs/decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md`** – wann eine Gruppe, wann ein Ordner, wann eine Zwischenüberschrift das richtige Mittel ist, und warum es bei dreien bleibt.

### Labels

- **Labels lassen sich direkt in der Eingabemaske anlegen.** Das Aufklappfeld hat unten „＋ Neues Label"; Name und Farbe werden abgefragt wie in der Labelverwaltung, und das neue Label ist sofort ausgewählt. Vorher musste man die Maske verlassen, das Label anlegen und von vorn beginnen.
- Das Labelfeld erscheint auch dann, wenn noch kein Label existiert – sonst käme man an das Anlegen nicht heran.
- Anlegen läuft über eine gemeinsame Methode (`create_label_interactively`), die Labelverwaltung und Eingabemaske teilen. Vorher stand derselbe Ablauf zweimal im Quelltext.

### Grundlage

- **`modal_over` sichert jeden Unterdialog ab.** Öffnet man aus einer modalen Maske heraus ein weiteres Fenster – Kalender, Farbauswahl, Namensabfrage –, nimmt dieses den Tastatur- und Mausgriff an sich und gibt ihn beim Schließen nicht von allein zurück. Die Maske nahm dann keine Eingabe mehr an und wirkte eingefroren. Die Rückgabe stand bisher einmal von Hand im Kalenderdialog; jetzt deckt ein gemeinsamer Helfer alle Fälle ab.

## 3.0.1 – 03.09.2026

Feinschliff und fünf Fehler aus der Benutzung von 3.0.0. Datenformat bleibt 10.

### Behoben

- **Dialoge öffneten sich auf dem falschen Bildschirm.** `winfo_screenwidth` meldet unter Windows nur den Hauptmonitor. Lag das Hauptfenster auf einem zweiten Bildschirm, klemmte die Sicherheitsprüfung den Dialog auf den ersten zurück. Die Grenzen umfassen jetzt Hauptbildschirm *und* Hauptfenster – betrifft Kalender, erweiterte Eingabe und jeden anderen Dialog.
- **Die erweiterte Eingabe öffnete zu klein.** Die Maske liegt in einem Bildlaufbereich, dessen angeforderte Höhe nichts über den Inhalt aussagt – das Fenster startete in Mindestgröße und musste jedes Mal von Hand größer gezogen werden. Die Höhe wird jetzt aus dem tatsächlichen Inhalt berechnet, gedeckelt auf 88 % der Bildschirmhöhe.
- **Ungleiche Ränder in der Eingabemaske.** Die Bildlaufleiste nahm rechts 16 Pixel weg, ohne dass links etwas ausgeglichen wurde. Der Innenabstand ist rechts jetzt um genau diesen Betrag kleiner – der sichtbare Rand ist beidseitig gleich, und die Feldkante links bleibt dort, wo sie app-weit liegt.
- **Ein möglicher Grund für das Einfrieren.** Klappte die Labelauswahl auf, während der Dialog geschlossen wurde, gab sie den Tastatur- und Mausgriff an ein gerade verschwindendes Fenster zurück. Der Griff blieb dann an nichts hängen, und die Anwendung nahm keine Eingabe mehr an. Beim Abbau wird der Griff jetzt nur noch freigegeben, nicht zurückgesetzt.
- **Gruppieren war kaum zu finden** – es lag unter „Art", direkt neben „In Gruppe umwandeln", das fast gleich hieß und das Gegenteil tut: Es macht aus *jedem* markierten Punkt eine eigene leere Gruppe. „Auswahl gruppieren …" steht jetzt auf der obersten Menüebene mit seinem Tastenkürzel; der andere Weg heißt „Jeden Punkt zur leeren Gruppe machen".

### Feinschliff

- Die Labels im Kopfbereich enden auf derselben Flucht wie die Statuszeile darüber. Der letzte Chip einer Reihe trug rechts noch seinen Abstand.
- Labelchips haben rundere Ecken (Radius 6 → 9).
- Die Überschrift „Listen" sitzt drei Pixel tiefer und damit optisch auf der Mitte des Knopfs daneben.

### Bekannt, aber nicht behoben

- **Der helle Rahmen um Kontext- und Auswahlmenüs.** Er stammt nicht aus der Anwendung, sondern ist der Fensterrahmen, den Windows um jedes Menü zeichnet; Tk gibt ihn nicht frei. Ihn loszuwerden hieße, alle Menüs durch eigene Fenster zu ersetzen.

## 3.0.0 – 03.09.2026

Eine Hauptversion, weil sich die Oberfläche sichtbar ändert: Der Inhalt rückt
nach oben, die Listenübersicht beginnt ganz oben, Schwarz weicht im Hellmodus
einem Dunkelblau, und die Bedienelemente tragen Symbole. Datenformat bleibt
bei 10 – an den Daten ändert sich nichts.

### Farbe

- **Kein Schwarz mehr im Hellmodus.** Text und Themenschalter stehen jetzt in `#15243C`. Der Dunkelmodus bleibt bewusst grau: Ein blauer Grundton wirkt dort als Farbstich, wo die Fläche selbst dunkel ist, statt als ruhiger Kontrast zum Weiß.

### Aufbau

- **Die Übersicht der Listen und Ordner beginnt ganz oben**, auf Höhe der Eingabezeile. Dafür ist die Eingabe „Listenpunkt eingeben“ in den rechten Bereich gewandert und steht bündig mit dem Suchfeld. Vorher lief sie über die volle Fensterbreite und schob alles darunter nach unten.
- **Weniger Luft nach oben.** Die Abstände zwischen Menüleiste und Inhalt sind durchgehend verringert.
- **Die Standard-Fenstergröße ist 1280×860** statt 1000×800 – passend zu einem 1920er Bildschirm und oberhalb der Schwelle, ab der Labels und Hinweiszeile stehen bleiben.

### Aufgabenliste

- **Long-Task und Überschrift erscheinen nicht mehr in der Labelspalte.** Beide beschreiben die Art des Punkts, und die sieht man der Zeile ohnehin an. Gespeichert bleiben sie – sie tragen die Art.
- **Ein Symbol vor dem Label**, wie das Kalendersymbol vor dem Datum. Bewusst ein Textzeichen (`◆`): Es nimmt die Labelfarbe an und passt in die feste Zeilenhöhe, was für ein Farb-Emoji nicht garantiert ist.
- **Labelnamen werden so begrenzt, dass nichts abgeschnitten wird.** Die Spaltenbreite wird mit der Schrift der Liste gemessen, nicht geschätzt.
- **Labelspalte und Hinweiszeile weichen bei derselben Breite** – rund 960 Pixel Fensterbreite, der halben Breite eines 1920er Bildschirms. Vorher blieb die Hinweiszeile stehen, während die Labels längst verschwunden waren.

### Bedienung

- **Listen und Ordner lassen sich in der Seitenleiste umbenennen**, ohne einen Dialog zu öffnen: ein Klick auf eine bereits ausgewählte Zeile, F2 oder „Umbenennen“ im Kontextmenü. Ein Doppelklick öffnet weiterhin den Bearbeiten-Dialog und hat Vorrang; nach einem Zug passiert nichts. Der Eingang bleibt außen vor – er trägt einen festen Systemnamen.
- **Symbole für Eingang, In Bearbeitung, Verspätet, Papierkorb, Labels, Kalender und den Themenschalter.** Alle liegen in der Tabelle `ICONS` an einer Stelle; ein Wechsel ist ein geändertes Zeichen. Durchgängig Textzeichen und keine Emoji: Sie sehen auf Windows, macOS und Linux gleich aus, nehmen die Textfarbe an und können keine Zeile sprengen.
- Der Themenschalter zeigt, wohin er führt: ☾ im Hellmodus, ☀ im Dunkelmodus.
- **Kopfzeile und Themenschalter schließen auf einer Linie ab.** Die Statuszeile beginnt auf Höhe der Oberkante des Schalters, die Labelzeile endet auf Höhe seiner Unterkante – beide Blöcke sind exakt gleich hoch.
- **Ein gleichmäßiger Abstand um die Aufgabenliste.** Der Abstand zur Aktionsleiste entspricht dem Abstand zur Seitenleiste, auch wenn die Hinweiszeile bei schmalem Fenster verschwindet. Vorher klebte die Liste dann an den Schaltflächen.
- **„Erweitert" weicht, bevor der Knopf gestaucht wird.** Die Schwelle wird aus den tatsächlichen Knopfbreiten berechnet, nicht geschätzt – bei anderer Anzeigeskalierung greift sie deshalb ebenfalls rechtzeitig.
- **Ein Klick auf das Klappdreieck eines Ordners öffnet und schließt ihn, sonst nichts.** Umbenennen an Ort und Stelle löst nur ein Klick auf den Namen aus.

### Behoben

- **Die Bildlaufleiste zeigte sich, obwohl es nichts zu scrollen gab.** Bei vollständig sichtbarem Inhalt zeichnete sie einen Regler über die ganze Höhe – optisch eine Leiste, die nichts tat. Sichtbar war das in der erweiterten Punkteingabe.
- **Die aufgeklappten Auswahlmenüs trugen einen harten Rahmen**, der zu nichts anderem in der Oberfläche passte. Betrifft Art, Wichtigkeit, Farbe, Zielliste und alle Kontextmenüs.

### Offen

- Labels als abgerundete Chips in der Aufgabenliste. `ttk.Treeview` kann in Wertspalten weder Widgets noch Bilder darstellen; dafür braucht es eine eigene Zeichenfläche neben der Liste.

## 2.12.0 – 03.09.2026

Die Oberfläche wird ruhiger. Die Eingabemaske verliert den dauerhaft
aufgeklappten Kalender und die Chipfläche für Labels und wird dadurch rund 300
Pixel kürzer. Der Kopfbereich springt nicht mehr, die Listenübersicht beginnt
eine Zeile weiter oben, und ein Fälligkeitsdatum wird endlich vollständig
angezeigt. Datenformat bleibt bei 10 – es ändert sich nichts an den Daten.

### Eingabemaske

- **Labels sind ein Aufklappfeld mit Mehrfachauswahl.** Vorher lagen alle Labels als Chipfläche in der Maske und belegten gut 130 Pixel – auch dann, wenn kein einziges vergeben war. Geschlossen ist es jetzt eine Zeile wie jedes andere Feld; die Liste klappt darunter auf und bleibt für mehrere Klicks offen. Die Farben bleiben sichtbar: In der aufgeklappten Liste steht neben jedem Haken der echte Chip. Neue Komponente `LabelDropdown`.
- **Die Fälligkeit zeigt nur noch einen Kalenderknopf.** In einer Maske, die ohnehin Titel, Art, Wichtigkeit, Farbe, Labels, Beschreibung und Anhänge trägt, kostete ein fest eingebauter Monatskalender mehr Platz als er nützte. Datum und Uhrzeit stehen weiter als Felder da, der Kalender öffnet sich auf Knopfdruck als eigenes Fenster. `DueField` kennt dafür den Schalter `compact`; das Kalenderfenster selbst benutzt weiter die vollständige Ausprägung.
- Der Kalender gibt den Grab an die aufrufende Maske zurück (`themed_due_dialog(..., parent=…)`). Ohne das hätte die Maske nach dem Schließen des Kalenders keine Eingabe mehr angenommen.

### Kopfbereich und Listenübersicht

- **Die Labels einer Liste stehen rechts unter der Fortschrittszeile.** Vorher standen sie links unter dem Beschreibungstext und wurden ausgeblendet, wenn eine Liste keine hatte – dadurch sprang der ganze Kopfbereich um eine Zeilenhöhe, sobald man zwischen einer Liste mit und einer ohne Labels wechselte. Die Zeile behält ihre Höhe jetzt in jedem Fall; ihre Höhe wird aus der echten Chiphöhe berechnet, nicht geschätzt.
- **Die Übersicht der Listen und Ordner beginnt eine Zeile weiter oben.** Such- und Filterzeile stehen nicht mehr über die volle Fensterbreite, sondern über der Aufgabenliste. Die Seitenleiste startet damit auf Höhe der Suchzeile.
- **„Nur erledigte Punkte“ ist entfallen.** Der Filter stand dauerhaft im Weg und war über die Ansicht „Erledigt“ ohnehin erreichbar. „Nur offene Punkte“ bleibt und steht jetzt rechts neben dem Suchfeld. Eine gespeicherte Einstellung `filter_mode: "done"` aus 2.11.0 fällt beim Start auf „alle“ zurück – sonst bliebe ein Filterzustand stehen, den kein Schalter mehr abstellen kann.

### Aufgabenliste

- **Das Fälligkeitsdatum wird vollständig angezeigt.** Vorher stand dort „06.09.2026, 10:3“ – die Uhrzeit brach ab. Ursache war die Spaltenbreite: Sie war gegen die Standardschriftgröße gerechnet, die Liste zeichnet aber mit `TkDefaultFont 12`. Die Breite wird jetzt mit genau dieser Schrift gemessen (188 statt 151 Pixel). Zusätzlich ist das Jahr in der Spalte zweistellig – „06.09.26, 10:30“. Dialoge, Suche und alle Exporte behalten das vierstellige Jahr.
- **Eine Zeile zeigt ein Label, alles Weitere als Zähler.** Zwei Labels nebeneinander verdrängten den Aufgabentext. Lange Namen werden auf 14 Zeichen gekürzt; gespeichert und exportiert wird weiter der volle Name.
- **Das feste Label „Überschrift“ erscheint nicht mehr in der Liste.** Eine Zwischenüberschrift ist an ihrer Darstellung zu erkennen; das Label wiederholte diese Auskunft nur. Gespeichert bleibt es – es trägt die Art des Punkts.
- **Die Labelspalte bleibt im Standardfenster stehen.** Sie wich bisher ab einer Baumbreite von 640 Pixeln; das frisch geöffnete Fenster (1000 Pixel) lag darunter, sodass Labels dort nie zu sehen waren. Die Schwelle liegt jetzt bei 540.

### Werkzeuge

- **`tests/tools/screenshots.py`** erzeugt Aufnahmen aller wichtigen Ansichten in hell und dunkel. Das Werkzeug liegt im Repository, nicht in einem Arbeitsordner: Aufnahmen, deren Erzeuger nur lokal existiert, lassen sich später nicht wiederholen.
- `audit_app.py` rief `themed_multiline_dialog` auf – eine Methode, die es seit 2.11.0 nicht mehr gibt. Der Aufruf ist entfernt, der Durchlauf läuft wieder vollständig.

## 2.11.0 – 03.09.2026

Der gemeldete Datenverlust ist behoben, und zwar an der Wurzel: Ein gelöschter
Punkt geht jetzt in den Papierkorb, Strg+Klick wählt wieder mehrfach aus, und
jede Umbauaktion wird von einem Bestandswächter begleitet. Anlegen und
Bearbeiten benutzen dieselbe Maske – mit Kalender, optionaler Uhrzeit,
Beschreibung, Labels und Anhängen. Datenformat steigt von 9 auf 10; die
Ergänzung ist additiv.

### Kein Datenverlust mehr

- **Ein gelöschter Punkt landet im Papierkorb.** Vorher entfernte „Löschen“ ihn sofort und endgültig: Er stand weder im Papierkorb noch sonst wo, und nach einem Neustart war auch Rückgängig verbraucht. Das ist die Ursache des gemeldeten Verlusts – besonders bei Mehrfachauswahl, wenn nach einer Shift-Bereichsauswahl versehentlich Entf gedrückt wird. Der Papierkorbeintrag hält den Punkt mit Unterpunkten, Beschreibung und Anhängen sowie seiner Herkunft; beim Wiederherstellen kehrt er an dieselbe Stelle zurück. Existiert die Herkunftsliste nicht mehr, landet er am Ende der aktuellen Liste – verloren geht er nie.
- **Bestandswächter um jede Umbauaktion.** Gruppieren, Auflösen, Ziehen, Ein- und Ausrücken sowie das Verschieben in eine andere Liste laufen jetzt unter `guarded_structural_change`: Der Wächter zählt vor und nach der Aktion alle Punkt-IDs in allen Listen und im Papierkorb. Fehlt danach einer, wird der vorherige Stand vollständig wiederhergestellt und der Vorgang gemeldet, statt den Verlust still zu speichern. Planmäßig entfallen darf allein die leere Hülle einer aufgelösten Gruppe.
- **Auflösen prüft zusätzlich einzeln nach.** Vor dem Speichern wird verglichen, ob jeder Punkt der Gruppe wieder in der Liste steht. Das ist der Weg, den der Nutzer am häufigsten geht, und er trägt deshalb eine eigene Zusicherung – über den allgemeinen Wächter hinaus.
- **Ein Drop auf die Seitenleiste fragt nach.** Vorher wanderte die Auswahl kommentarlos in eine andere Liste, sobald der Zeiger beim Sortieren nach links abrutschte. Jetzt nennt eine Rückfrage Ziel und Anzahl und weist auf Strg+Z hin.
- **Ziehen bewegt die ganze Auswahl.** Bisher wurde bei mehreren markierten Punkten nur der angefasste verschoben; die übrigen blieben unbemerkt zurück. Das gilt für das Umsortieren wie für Shift+Drag.

### Strg+Klick wählt wieder mehrfach aus

- `<Control-Button-1>` war auf allen drei Bäumen an das Kontextmenü gebunden – als macOS-Ersatz für die rechte Maustaste. Tk bevorzugt jedoch die spezifischere Bindung, sodass unter Windows und Linux `<Button-1>` gar nicht mehr ankam: Das Menü ging auf, und mehrere Punkte ließen sich überhaupt nicht auswählen. Der eingebaute Strg-Zweig war dort toter Code.
- Der Zusatz wird jetzt nur noch unter macOS belegt. Unter Windows und Linux ist Strg+Klick wieder die Mehrfachauswahl, unter macOS übernimmt das Cmd+Klick. Hinweiszeile und Tastenkürzel nennen die jeweils passende Taste.

### Unterpunkte bleiben sichtbar

- Ein Punkt auf oberster Ebene wurde offen gezeichnet, derselbe Punkt eine Ebene tiefer zugeklappt. Beim Gruppieren verschwanden dadurch die Unterpunkte aus der Ansicht, obwohl sie in den Daten standen – von außen nicht von einem Datenverlust zu unterscheiden. Offen ist jetzt der Normalfall: Zugeklappt bleibt nur, was der Nutzer selbst zugeklappt hat.

### Eine Maske für Anlegen und Bearbeiten

- Beide Fenster waren unterschiedlich mächtig: Der Anlage-Dialog kannte keine Beschreibung und keine Anhänge, das Detailfenster keine Art, Wichtigkeit, Farbe, Fälligkeit und Labels. Wer einen Punkt anlegte, musste ihn danach noch einmal öffnen. Beide benutzen jetzt dieselbe Implementierung (`item_form_dialog`); der Modus steuert nur Beschriftung und Vorbelegung, nicht den Umfang.
- **Kalender überall.** Die Fälligkeit ist eine eigene Komponente (`DueField`): Datumsfeld, Monatskalender mit Blättern und Hervorhebung von heute und ausgewähltem Tag, dazu „Heute“, „Morgen“ und „Keine Fälligkeit“. Tippen und Klicken schreiben in dasselbe Feld. Dieselbe Komponente trägt das Menü „Fälligkeit“; der frühere `themed_date_picker` ist entfallen.
- **Optionale Uhrzeit.** Ein Punkt hat keine Fälligkeit, nur ein Datum, oder Datum und Uhrzeit. Die Uhrzeit hängt am Datum: Ohne Tag gibt es keine Uhrzeit. Sie erscheint in der Liste, in „In Bearbeitung“ und „Verspätet“, in Suche, TXT-, Markdown- und CSV-Export und entscheidet beim Sortieren innerhalb desselben Tages.
- **Anhänge auch beim Anlegen.** Dateien und Bilder lassen sich sofort mitgeben, statt den Punkt danach erneut zu öffnen.
- Die Labelauswahl zeigt rund fünf Chipzeilen statt zwei.
- Die Maske ist hoch und bringt deshalb eine eigene Bildlaufleiste mit; kein Dialog wird höher als der Bildschirm.

### Erweiterte Eingabe neben der Schnelleingabe

- Die Schnelleingabe bleibt unverändert der kürzeste Weg: tippen, Enter, fertig. Daneben steht „Erweitert“ und öffnet dieselbe vollständige Maske. Was schon im Eingabefeld steht, wird übernommen.
- Die vollständige Maske erscheint überall dort, wo ein Punkt entsteht: über „Erweitert“, per Doppelklick auf einen Kalendertag, beim Anlegen eines Unterpunkts und über das Kontextmenü im leeren Listenbereich.

### Datenformat 10

- Neu: `due_time` an einem Punkt und die Papierkorbart `item` mit Herkunftsangabe. Beide Ergänzungen sind additiv – Bestände der Formate 2 bis 9 laden unverändert, eine fehlende Uhrzeit heißt „ganztägig“.
- Die Zählung steigt trotzdem, weil eine ältere Glide-Version einen Papierkorbeintrag der Art `item` beim Laden stillschweigend verwerfen würde. Mit der höheren Zahl weist sie die Datei stattdessen sichtbar ab.

### Prüfung

- Neu: `tests/integration/test_datenintegritaet.py` – Bestandswächter, 130 Kombinationen aus Gruppieren und Auflösen über alle vier Punktarten, Papierkorb-Rundlauf für Punkte, Ziehen mit Mehrfachauswahl, Listenwechsel, Mehrfachauswahl-Taste, gemeinsame Eingabemaske und Uhrzeit.
- Zusätzlich liefen drei Zufallsläufe über rund 7.600 simulierte Bedienschritte: Datenbilanz je Liste, listenübergreifende Bilanz einschließlich Papierkorb und ein Abgleich von Baum und Daten nach jedem Schritt. Sie sind Werkzeug, nicht Teil der Testsuite.

## 2.10.0 – 03.09.2026

Labels erscheinen als Chips, der TXT-Rundlauf ist für alle vier Aufgabenarten
verlustfrei, und die Code-Basis ist von totem Code befreit. Datenformat bleibt 9.

### Labels als Chips

- Ein Label ist jetzt eine abgerundete Fläche mit dunklem Text in seiner eigenen Farbe: 6 Pixel Radius, links und rechts derselbe Abstand, oben zwei Pixel weniger als unten. Ein farbiger Punkt oder farbiger Text sagt nur „hier ist etwas markiert“ – eine Fläche mit lesbarem Text sagt, **welches** Label es ist.
- Die Flächenfarbe entsteht nicht aus einem festen Mischanteil, sondern aus einer Zielhelligkeit. Ein fester Anteil trifft die sieben Palettenfarben ungleich: Gelb ist von Haus aus dreimal so hell wie Lila und verschwände im Hintergrund, während Lila noch kräftig wäre. Jetzt liegen alle Farben auf demselben Kontrastniveau – über 4,5:1 zwischen Text und Fläche, in Hell und Dunkel.
- Chips stehen in der Kopfzeile einer geöffneten Liste oder eines Ordners, in der Labelverwaltung und im Anlage-Dialog. Bei vielen Labels brechen sie in Reihen um, statt seitlich aus dem Feld zu laufen.
- Die Labelverwaltung zeigt statt einer Textliste eine Chipliste mit Farbname, Verwendungszahl und dem Vermerk „fest“ bei den beiden Systemlabels. Der Farbauswahldialog zeigt den Labelnamen in jeder Farbe zur Auswahl.
- Unverändert: In der Labelspalte des Aufgabenbaums steht weiter reiner Text. Eine `ttk.Treeview` kann eine einzelne Zelle nicht einfärben; ein Chip ist dort nicht darstellbar.

### Behoben

- Ein **einzeiliger Long-Task verlor beim TXT-Export seine Art**. Die Fortsetzungszeilen waren das einzige Merkmal, und bei einzeiligem Text gibt es sie nicht. Ein Long-Task trägt jetzt einen eigenen Marker (`»`), analog zu Gruppe und Zwischenüberschrift. Der TXT-Rundlauf ist damit für alle vier Arten verlustfrei – einschließlich Wichtigkeit und Erledigt-Zustand.

### Code-Basis

- Vier tote Bausteine entfernt: `themed_multiline_dialog` (seit 2.7.0 durch den gemeinsamen Bearbeiten-Dialog ersetzt), der Alias `refresh_in_progress_overview`, `system_label_ids` und `cycle_importance_from_click` – ein Bedienweg ohne Bindung.
- Drei ungenutzte Bausteine wieder eingebunden, statt sie zu entfernen: `sync_all_item_kind_labels` ersetzt eine Doppelung beim Laden, `get_sidebar_iid_for_row` eine if-Kette beim Aufbau der Seitenleiste, und `CALENDAR_MODES` prüft jetzt den Moduswechsel. Eine AST-Analyse belegt: keine ungenutzten Methoden oder Konstanten mehr.

### Dokumentation und Vorbereitung

- Neu: `docs/07_QA_BERICHT.md` – was geprüft wurde, mit welchem Ergebnis, was ungeprüft bleibt und wie sich der Lauf wiederholen lässt.
- Neu: eine importierbare Veröffentlichungs-Checkliste im Glide-TXT-Format mit 46 Punkten in fünf Abschnitten, erzeugt und gegengeprüft über den TXT-Export und -Import der App selbst.
- Die Funktionsvorschau enthält jetzt eine Liste „00 Was Glide kann“ mit jeder Art, jeder Wichtigkeit, jeder der sieben Farben, jedem Fälligkeitszustand und jedem Zusatz genau einmal – dazu zwei echte Anhänge, verschachtelte Gruppen und einen dritten Ordnerzweig über drei Ebenen.

## 2.9.0 – 03.09.2026

Ordner dürfen ineinander liegen, der Long-Task bekommt ein eigenes
Detailfenster mit mehrzeiligem Titel, und jedes längere Feld hat jetzt eine
sichtbare Bildlaufleiste. Datenformat steigt von 8 auf 9; die Ergänzung ist
additiv.

### Verschachtelte Ordner

- Ein Ordner lässt sich in einen anderen legen – per Drag & Drop, über „Ordner verschieben“ im Kontextmenü oder mit Tab beziehungsweise Alt+→ und Alt+←. Beim Ziehen sortieren das obere und das untere Viertel einer Ordnerzeile wie bisher davor und danach; die mittlere Hälfte legt hinein. Ohne diese Zonen wäre entweder das Umsortieren oder das Verschachteln per Maus nicht mehr erreichbar.
- Der Zähler eines Ordners nennt alle Listen darin, auch die in Unterordnern. Die Ordnerübersicht im Hauptbereich zeigt die Unterordner über den Listen; ein Doppelklick öffnet sie, ein Rechtsklick bietet dasselbe Menü wie in der Seitenleiste.
- Ein Ordner kommt weder in sich selbst noch in einen seiner eigenen Unterordner; die Verschachtelung endet bei fünf Ebenen. Beide Grenzen gelten für Maus, Menü und Tastatur gleichermaßen, und eine abgelehnte Verschiebung sagt, warum.
- „Ordner auflösen“ hebt Listen **und** Unterordner eine Ebene an, statt sie auf die Hauptebene zu werfen. Ein Ordner im Papierkorb nimmt seinen gesamten Zweig mit und bringt ihn samt Hierarchie zurück; existiert der frühere Elternordner nicht mehr, landet er auf der obersten Ebene.
- Wo eine Liste zur Auswahl steht – „In Liste verschieben“, der Anlage-Dialog, das Ablegen einer Aufgabe auf einem Ordner, die Herkunftsspalte in „In Bearbeitung“ und „Verspätet“ – steht jetzt ihr vollständiger Pfad. Zwei gleichnamige Listen in verschiedenen Unterordnern sind sonst nicht auseinanderzuhalten.
- Alt+↑/↓ sortiert einen Ordner nur unter seinen Geschwistern und ändert seine Ebene nicht mehr.

### Punktdetails (Long-Task)

- Ein Long-Task öffnet ein eigenes Detailfenster mit **mehrzeiligem Titelfeld**. Enter setzt dort eine neue Zeile, gespeichert wird mit der Schaltfläche oder Strg+Enter – genau wie im Beschreibungsfeld.
- Die Zeilenumbrüche bleiben erhalten: in der Liste beginnt an jedem eigenen Umbruch eine neue Zeile, danach greift wieder der automatische Umbruch. Sichtbar bleiben höchstens fünf Zeilen. Jede andere Punktart bleibt einzeilig; beim Zurückwandeln eines Long-Tasks werden seine Umbrüche zu Leerzeichen, statt unsichtbar im Datensatz zu bleiben.
- TXT-Export und -Import erhalten den mehrzeiligen Text über Fortsetzungszeilen (`Text:`), der Markdown-Export über eingerückte Folgezeilen. Kalender, Aufgabenübersichten und Zwischenablage zeigen den Text einzeilig, weil dort genau eine Zeile zur Verfügung steht.

### Bildlaufleisten

- Titel (Long-Task), Beschreibung und Anhänge in den Punktdetails, der Beschreibungstext von Listen und Ordnern, die Labelverwaltung, die Labelauswahl im Anlage-Dialog und jede Auswahlliste haben jetzt eine themenkonforme Bildlaufleiste. Längerer Inhalt war vorher zwar mit Rad und Tastatur erreichbar, aber nicht als solcher erkennbar.

### QA

- Neu: `tests/integration/audit_app.py` – ein app-weiter Durchlauf, der nicht einzelne Funktionen prüft, sondern die Wege durch die App: jede Ansicht, jedes Kontextmenü, jede Verschiebeoperation, jede Tastenbindung, simuliertes Drag & Drop für alle Quell-/Ziel-Kombinationen, Rückgängig nach Strukturänderungen, der Papierkorb-Rundlauf mit ganzen Ordnerzweigen und der Aufbau jedes Dialogs samt Bildlaufleisten. Er meldet alle Abweichungen, statt beim ersten Fehler zu stoppen.
- Der Integrationstest deckt die Ordnerhierarchie vollständig ab: Ebenen, Vorfahren, rekursive Zähler, Kreis- und Tiefenschutz, Ablegezonen, Tastaturwege, Auflösen, Papierkorb-Rundlauf, Format-9-Migration und die Abweisung eines Ordnerkreises im Komplettbackup.
- Neuer Referenzbestand `tests/fixtures/current_v9/reference_v9.json` mit zwei Verschachtelungsebenen und einem Long-Task mit echten Zeilenumbrüchen.

## 2.8.0 – 02.09.2026

Vier neue Bausteine – Verspätet, Long-Task, Zwischenüberschrift und ein
vollständiger Anlage-Dialog – dazu Feinschliff an Seitenleiste und Liste.
Datenformat steigt von 7 auf 8; alle Ergänzungen sind additiv.

### Neue Aufgabenarten

- **Long-Task.** Ein mehrzeiliger Punkt, dessen vollständiger Text in der Liste sichtbar bleibt – bis zu fünf Zeilen. Nummer, Wichtigkeits- und Erledigt-Symbol stehen in der ersten Zeile, die Folgezeilen beginnen bündig darunter. Umwandeln und Zurückwandeln über das Rechtsklickmenü unter „Art“. Inhaltlich bleibt es eine gewöhnliche Aufgabe: Fälligkeit, Wichtigkeit, Farbe, Labels, Anhänge, Unterpunkte und Erledigt-Zustand verhalten sich unverändert.
- **Zwischenüberschrift.** Gliedert eine Liste in Abschnitte. Sie trägt das Schriftbild von „Eingang“, „In Bearbeitung“ und „Listen“, bekommt eine Leerzeile Abstand nach oben und lässt die Nummerierung darunter wieder bei 1 beginnen. Sie zählt nicht als Aufgabe und trägt weder Status noch Fälligkeit noch Wichtigkeit.
- **Feste Labels.** „Long-Task“ und „Überschrift“ gehören fest zum Programm und tragen die Art eines Punkts. Das Label zu vergeben bewirkt genau dasselbe wie die Umwandlung im Kontextmenü – und es wieder zu nehmen dasselbe wie die Rückwandlung. Beide lassen sich nicht entfernen und nicht umbenennen; die Farbe ist frei wählbar. Für Listen und Ordner stehen sie nicht zur Auswahl, weil sie dort keine Bedeutung hätten.

### Verspätet

- Vierte Systemzeile über dem Listenbereich: alle Aufgaben, deren Fälligkeit in der Vergangenheit liegt und die nicht als erledigt markiert sind. Aufbau, Navigation und Doppelklick verhalten sich wie in „In Bearbeitung“; erledigte Aufgaben verlassen die Ansicht von selbst.

### Neuer Punkt

- Das Fenster für einen neuen Punkt bietet jetzt alles an, was ein Punkt tragen kann: Titel, Art, Wichtigkeit, Farbe des Listenpunkts, Fälligkeit, Labels und – wo sinnvoll – die Zielliste. Nur der Titel ist Pflicht; alles andere bleibt freiwillig und später änderbar. Dasselbe Fenster öffnet der Kalender beim Doppelklick auf einen Tag, mit bereits eingetragener Fälligkeit.

### Darstellung

- Das graue Trennband aus 2.7.2 entfällt. Systembereich und Listenbereich trennt jetzt ausschließlich Abstand – kein Band, kein Rahmen, keine Linie.
- Der Zähler einer Seitenleistenzeile hält einen Sicherheitsbereich zur rechten Kante ein. Reicht der Platz nicht, wird ausschließlich der Titel weiter gekürzt; der Zähler bleibt immer vollständig lesbar und passt sich beim Ziehen des Fensterrands sofort an.
- Die Zeile unter dem Mauszeiger wird hellblau – im Aufgabenbaum, im Listenbaum und im Systembereich. Lila bleibt der Auswahl vorbehalten: eine ausgewählte Zeile behält ihre Farbe. Ein Long-Task leuchtet über alle seine Zeilen hinweg auf. Während eines Ziehvorgangs zeigt der Baum das Ziel statt des Hovers.
- Wird das Fenster schmal, weichen erst die Labelspalte und danach die Fälligkeitsspalte; die frei werdende Breite gehört dem Aufgabentext. Ein Long-Task bricht dabei sofort neu um.

### Datenformat

- Sprung von 7 auf 8, rein additiv: `kind` kennt zusätzlich `long` und `heading`, ein Label kann das Feld `system` tragen. Eine unbekannte Art lädt weiterhin als gewöhnliche Aufgabe, statt den Punkt zu verlieren. Fehlt ein festes Label in der Datei, ergänzt Glide es beim Laden und gleicht es mit der Art jedes Punkts ab – auch im Papierkorb. Bestände und Komplettbackups der Formate 4 bis 8 bleiben lesbar.
- TXT-Export und -Import erhalten die Zwischenüberschrift über einen eigenen Marker; im Markdown-Export wird sie zur echten Überschrift, in der CSV-Spalte „Art“ steht der ausgeschriebene Name.

### Beispieldatei

- `Glide-Funktionsvorschau.glidebackup` enthält eine vollständige Projektvorlage für ein Redesign- und Branding-Projekt in zehn Phasen, dazu Tagesgeschäft, Ideensammlung, gefüllten Eingang und Papierkorb – 15 Listen, zwei Ordner, sechs eigene Labels, Zwischenüberschriften, Long-Tasks, Gruppen, Unterpunkte und Fälligkeiten von überfällig bis in drei Monaten.

### QA

- Der Integrationstest deckt alle neun Punkte ab: Systemzeile „Verspätet“ samt Zähler und Filterlogik, Nummerierungsneustart unter einer Überschrift, Abstandszeile, Umbruchlogik des Long-Tasks als reine Rechenmethode, Gleichlauf von Art und festem Label in beide Richtungen, Schutz der festen Labels, responsive Spaltenbreiten an vier Fensterbreiten, Hover-Tags in beiden Themes sowie den erweiterten Anlage-Dialog inklusive abweichender Zielliste.
- Neuer Referenzbestand `tests/fixtures/current_v8/reference_v8.json` mit beiden neuen Arten, einem Long-Task ohne festes Label und einem Punkt mit unbekannter Art.

## 2.7.2 – 02.09.2026

### Behoben

- Die Pfeiltasten bewegten die Auswahl im Aufgabenbaum nicht. Die eigene Drag-Auswahl beantwortet jeden Klick mit „break“ und unterdrückte damit auch die native Bindung, die den Baum fokussiert – ohne Tastaturfokus bleiben Pfeiltasten wirkungslos. Der Baum fordert den Fokus jetzt selbst an und ist zusätzlich als fokussierbar markiert. Dieselbe Absicherung gilt für den Listenbaum der Seitenleiste.

### Darstellung

- Systembereich und Listenbereich trennt jetzt ein Band in der Fensterfarbe mit Abstand darüber und darunter. Der Rahmen aus 2.7.1 entfällt: eine gerahmte Fläche innerhalb der ohnehin gerahmten Seitenleiste wirkte wie ein Kasten im Kasten.

### Kalender

- Der Tag unter dem Mauszeiger bekommt eine hellblaue Umrandung. Der Wechsel zwischen Zelle und Beschriftungen lässt sie nicht flackern, und der heutige Tag erhält seine Markierung beim Verlassen zurück.
- Ein Doppelklick auf einen Tag legt dort eine Aufgabe mit genau dieser Fälligkeit an. Der Dialog nennt die Zielliste: die geöffnete Liste, andernfalls der Eingang. Der Kalender aktualisiert sich sofort und bleibt geöffnet.

### QA

- Der Integrationstest prüft die Fokussierbarkeit des Aufgabenbaums, das graue Trennband samt Abständen sowie das Anlegen einer Aufgabe über den Kalender einschließlich Abbruch, leerem Titel und Rückfall auf den Eingang.

## 2.7.1 – 02.09.2026

Überarbeitung des internen Teststands 2.7.0 nach Sichtprüfung. Datenformat
bleibt 7; die Ergänzungen sind wie dort rein additiv.

### Behoben

- Die Entf-Taste löschte in der Seitenleiste nichts: sie war ausschließlich an den Aufgabenbaum gebunden. Seitenleiste und Systembereich haben jetzt eine eigene Entf-Bindung, die die dortige Auswahl in den Papierkorb legt und die globale Bindung abfängt. Systemzeilen bleiben geschützt.

### Darstellung

- Der Systembereich mit Eingang, „In Bearbeitung“ und Papierkorb liegt in einer eigenen gerahmten Fläche – derselbe Rahmen wie bei den Filter- und Suchfeldern. Die frühere horizontale Trennlinie entfällt ersatzlos; Systemblock und Listenbereich trennt nur noch Abstand.
- „Labels“ und „Kalender“ übernehmen die Farben ihrer Vorgänger an derselben Stelle: Labels grün, Kalender braun. Die obere Aktionsreihe ist damit wieder durchgehend farblich gemischt, die untere durchgehend lila.

### Labels

- Labels nutzen jetzt exakt dieselbe Farbpalette wie Listen- und Aufgabenfarben (Lila, Blau, Türkis, Grün, Gelb, Rot, Braun). Die eigenen Labelfarben aus 2.7.0 entfallen; dort angelegte Labels werden beim Laden auf die neue Palette abgebildet.
- Der Farbauswahldialog stellt jede Farbe in ihrer eigenen Farbe dar und markiert die aktuelle mit einem Haken.
- Die farbigen Emoji-Punkte vor den Labelnamen sind entfernt. Sie wurden unter Windows monochrom gerendert und täuschten damit eine falsche Farbe vor. In der Aufgabenliste steht jetzt reiner Text; farbig sind Labels dort, wo Tk es zulässt: in der Labelverwaltung, im Farbauswahldialog, in den Kontextmenüs und in der Kopfzeile einer Liste oder eines Ordners.
- Auch **Ordner und Listen** lassen sich mit Labels versehen. Zugewiesen wird über ihr Kontextmenü; angezeigt werden sie ausschließlich in der großen Darstellung im Hauptbereich – als farbige Zeile unter dem Seitentitel und in der Labelspalte der Ordnerübersicht. Die Seitenleiste bleibt davon frei.

### Kalender

- Umschaltbar zwischen **„Diese Woche“** und **„Dieser Monat“**; die aktive Ansicht ist gefüllt markiert.
- Die Monatsansicht zeigt das montagsausgerichtete Raster des Referenzmonats – vom Montag der ersten bis zum Sonntag der letzten Woche. Für September 2026 sind das unverändert fünf Wochen; Monate wie Februar 2026 brauchen sechs.
- Statt des festen Worts „Kalender“ steht jetzt der dargestellte Monat mit Jahr in der Überschrift.
- Die Pfeile blättern in der Monatsansicht ganze Monate und in der Wochenansicht einzelne Wochen. Eine neue Schaltfläche „Heute“ springt in beiden Ansichten zurück.
- Tage benachbarter Monate sind ausgegraut und tragen ihr Monatskürzel.
- Die Wochenansicht nutzt die volle Fensterhöhe für sieben Tagesspalten, zeigt bis zu 14 Aufgaben je Tag und bricht lange Aufgabentitel um, statt sie zu kürzen.

### Bedienung

- Alt+↑ und Alt+↓ verschieben ausgewählte Listenpunkte, Alt+← und Alt+→ rücken sie aus und ein. In der Seitenleiste verschieben dieselben Kürzel Listen und Ordner beziehungsweise lösen eine Liste aus einem Ordner heraus oder rücken sie hinein.

### QA

- Der Integrationstest prüft zusätzlich die neue Seitenleistenfläche ohne Trennlinie, die Entf-Bindung beider Bäume, die Farbzuordnung aller Aktionsschaltflächen, die Labelpalette samt Abbildung der 2.7.0-Farbschlüssel, den farbigen Farbauswahldialog, Labels an Ordnern und Listen inklusive Anzeigeorten und Persistenz sowie das Monatsraster und die Monatsnavigation über Jahresgrenzen.

## 2.7.0 – 02.09.2026

### Neu

- **Papierkorb.** Gelöschte Listen und Ordner werden nicht mehr sofort verworfen, sondern wandern vollständig in einen Papierkorb und lassen sich von dort wiederherstellen. Eine Liste kehrt in ihren Herkunftsordner zurück, sofern dieser noch existiert; ein gelöschter Ordner nimmt seine Listen mit und bringt sie gemeinsam zurück. Neben „Wiederherstellen“ gibt es „In Ordner wiederherstellen“, „Endgültig entfernen“ und „Papierkorb leeren“. Der Eingang bleibt weiterhin löschgeschützt.
- **Labels.** Punkte lassen sich mit frei benennbaren Labels versehen. Labels besitzen eine eigene Farbpalette, die bewusst unabhängig von der Aufgabenfarbe ist, und werden über das Kontextmenü eines Punkts sowie aus „In Bearbeitung“ heraus zugewiesen. In der Liste stehen sie in einer eigenen Spalte ganz rechts neben der Fälligkeit; ohne angelegte Labels ist die Spalte nicht vorhanden.
- **Labelverwaltung** über die neue Schaltfläche „Labels“ (früher „Export: TXT“): anlegen, umbenennen, Farbe wählen, entfernen – jeweils mit der Zahl der betroffenen Punkte. Ein entferntes Label wird von allen Punkten gelöst, die Punkte selbst bleiben unverändert.
- **Kalender** über die neue Schaltfläche „Kalender“ (früher „Import: TXT“): ein Raster aus der laufenden Woche plus vier weiteren Wochen, der heutige Tag umrandet, je Tag die Aufgaben mit Fälligkeit, „Diese Woche“ als Rücksprung und ein Klick auf eine Aufgabe öffnet sie in ihrer Liste. TXT-Import und -Export bleiben unverändert über Menü „Datei“, das Kontextmenü einer Liste und Strg+E beziehungsweise Strg+I erreichbar.
- **Automatisches Speichern** alle fünf Minuten: ein wegen eines Fehlers offen gebliebener Stand wird erneut geschrieben, andernfalls entsteht ein garantierter Sicherungspunkt. Der Zyklus arbeitet ohne Dialoge im Hintergrund.
- **Sicherungsrotation.** Neue automatische Sicherungen entstehen frühestens alle zwei Minuten statt bei jeder einzelnen Änderung. Die Rotation hält die neuesten zehn Sicherungen immer, entfernt darüber hinaus alles ältere als 30 Minuten und begrenzt den Rest auf 40. Portable `vor_import_*.glidebackup` bleiben davon unberührt.
- **Systembereich der Seitenleiste.** Eingang, „In Bearbeitung“ und Papierkorb bilden zusammen mit der Überschrift „Listen“ und ihrer Plus-Schaltfläche einen Block oberhalb der Trennlinie. Darunter beginnen ausschließlich Ordner und Listen.
- **Mehrfachauswahl in der Seitenleiste.** Mit Shift und Strg lassen sich mehrere Listen und Ordner markieren und gemeinsam in einen Ordner verschieben, herauslösen, einfärben oder in den Papierkorb legen; auch Drag & Drop nimmt die Auswahl mit. Alt+Auf und Alt+Ab verschieben die Auswahl ohne Maus, Strg+A markiert alle sichtbaren Zeilen.
- **Gemeinsamer Bearbeiten-Dialog** für Listen und Ordner: Titel und Beschreibungstext liegen in einem Fenster, aufgebaut wie „Punktdetails“. Beim Eingang ist nur das Titelfeld gesperrt, sein Beschreibungstext bleibt frei bearbeitbar.
- Neue Tastenkürzel: Strg+L öffnet die Labelverwaltung, Strg+K den Kalender.

### Geändert

- Die Menüeinträge „Umbenennen …“ und „Beschreibungstext bearbeiten …“ einer Liste oder eines Ordners sind durch den gemeinsamen Eintrag „Bearbeiten (Titel, Beschreibungstext) …“ ersetzt. Die vier zugehörigen Einzelmethoden wurden entfernt, weil sie keinen Aufrufer mehr hatten.
- „Liste entfernen“ heißt jetzt „In den Papierkorb“; das Ordnermenü unterscheidet zwischen „Ordner auflösen (Listen bleiben)“ und „Ordner mit Listen in den Papierkorb“.
- Die Schaltfläche „Titel“ in der Seitenleiste heißt „Bearbeiten“, weil sie beide Felder öffnet.
- Die Bestätigung vor dem endgültigen Entfernen nennt jetzt korrekt, dass Rückgängig den Schritt innerhalb der laufenden Sitzung noch zurücknehmen kann.

### Behoben

- Ein fehlgeschlagener oder ergebnisloser TXT-Import konnte beim Lesen der neuen Labelzeilen Labels anlegen, die anschließend liegen geblieben wären. Der Labelbestand wird in diesen Fällen exakt zurückgesetzt und der wirkungslose Rückgängig-Schritt verworfen.
- Ein manipulierter Papierkorbeintrag beendet die Wiederherstellung nicht mehr mit einer unbehandelten Ausnahme; der betroffene Eintrag bleibt liegen und wird gemeldet.

### Datenformat und Austausch

- Datenformat 7 ergänzt rein additiv `labels` und `trash` auf oberster Ebene sowie `labels` je Punkt. Fehlen die Felder – also in jedem Bestand bis Format 6 –, gilt „keine Labels“ und „leerer Papierkorb“; ein destruktiver Migrationsschritt entfällt.
- Komplettbackups der Formate 4 bis 7 bleiben importierbar. Abgewiesen werden eine unbekannte Papierkorbart, doppelte Label-IDs, eine unbekannte Labelfarbe sowie Label- oder Papierkorbfelder, die keine Listen sind.
- Anhänge gelöschter, aber noch wiederherstellbarer Listen gelten als referenziert und liegen deshalb in jedem Komplettbackup. Ohne sie wäre eine Wiederherstellung aus dem Backup unvollständig.
- TXT führt Labels als Zeile `Labels: …` unter dem Punkt und liest sie beim Import wieder ein; unbekannte Namen legen ein neues Label an. Markdown hängt sie als Code-Auszeichnung an die Zeile. CSV erhält die zusätzliche Spalte „Labels“ am Ende; die Position aller bisherigen Spalten bleibt unverändert.

### QA

- Der Integrationstest prüft zusätzlich den Systemblock, den vollständigen Papierkorb-Lebenszyklus, den gemeinsamen Bearbeiten-Dialog, die Mehrfachauswahl, das Label-Datenmodell samt Anzeige und Austauschformaten, die Kalenderberechnung, den Autosave-Zyklus und die gesamte Rotationslogik. Neu geprüft werden außerdem Speicheridempotenz, ein abgebrochener Import ohne Nebenwirkung, ein Schreibfehler ohne Datenverlust, beschädigte Speicherdateien und kollidierende IDs zwischen aktiven und gelöschten Listen.
- Neuer Referenzbestand `tests/fixtures/current_v7/reference_v7.json`; der Format-6-Bestand belegt zusätzlich die verlustfreie Migration.
- Keine neue Laufzeitabhängigkeit.

### Bewusste Grenze

- Eine `ttk.Treeview` kann eine einzelne Zelle nicht getrennt einfärben. Im Aufgabenbaum trägt deshalb ein farbiger Punkt aus der Emoji-Schrift des Systems die Labelfarbe; unter Windows und macOS wird er farbig gerendert. In der Labelverwaltung und in den Kontextmenüs ist die Farbe plattformunabhängig sichtbar.

## 2.6.0 – 01.09.2026

### Neu

- Punkte innerhalb einer Liste lassen sich zu Gruppen zusammenfassen. Eine Gruppe ist ein Behälter ohne Erledigt-Zustand, ohne Fälligkeit und ohne Wichtigkeit; Beschreibungstext, Anhänge und Farbe bleiben möglich. Sie erscheint mit Ordnersymbol, fetterem Schnitt und der Anzahl enthaltener Aufgaben, und Leertaste wie Doppelklick klappen sie auf und zu.
- „Auswahl gruppieren“ fasst mehrere markierte Punkte derselben Ebene zusammen, „Gruppe auflösen“ setzt den Inhalt wieder an ihre Stelle. Beides liegt im Kontextmenü, im Menü „Bearbeiten“ und auf Strg+G beziehungsweise Cmd+G.
- Gruppen zählen nicht als Aufgaben: Fortschrittsanzeige, Listenzähler und die Ansicht „In Bearbeitung“ berücksichtigen ausschließlich echte Aufgaben. Bei aktivem Offen-/Erledigt-Filter bleibt eine Gruppe nur sichtbar, wenn ein Unterpunkt passt.
- Jede Oberfläche besitzt ein vollständiges Kontextmenü: Aufgaben und Gruppen mit Bearbeiten, Erledigt, Neu anlegen, Gruppenaktionen, Wichtigkeit, Fälligkeit, Farbe, Struktur und Zwischenablage; der leere Listenbereich mit Neuanlage, Sortieren, Export und Liste leeren; Seitenleisten-Listen mit Umbenennen, Beschreibungstext, Verschieben, Duplizieren, Exportieren und Entfernen; Ordner mit Umbenennen, neuer Liste, Auf-/Zuklappen und Auflösen; die Ordnerübersicht und die Ansicht „In Bearbeitung“ mit den jeweils sinnvollen Aktionen. Nicht anwendbare Einträge sind sichtbar gesperrt statt versteckt.
- Aktionen der abgeleiteten Ansicht „In Bearbeitung“ wirken direkt auf die Originalaufgabe in ihrer Quellliste, ohne die Ansicht zu verlassen.
- Die Hauptüberschrift nutzt den schwersten verfügbaren Schnitt der Oberflächenschrift, unter Windows „Segoe UI Black“. Semibold und Demibold sind ausgeschlossen, weil sie leichter als Bold sind. Eine spätere Hausschrift wird über die Konstante `HEADER_FONT_FAMILY` gesetzt; benennt der Wert bereits einen schweren Schnitt, wird er unverändert übernommen.

### Behoben

- Duplizierte Punkte und Listen übernahmen die IDs des Originals. Der Aufgabenbaum brach damit beim Einfügen ab, und listenübergreifende Suchen hätten den falschen Punkt getroffen. Kopien erhalten jetzt durchgängig neue IDs.
- Beim ersten Start und nach einem Ladefehler blieben Hinweiszeile, Eingabefeld-Platzhalter und Beschreibungsvorschau im Grundzustand, weil der Pfad ohne vorhandene Speicherdatei die Ansichtsinitialisierung übersprang.

### Datenformat und Austausch

- Datenformat 6 ergänzt ausschließlich das optionale Feld `kind` mit den Werten `task` und `group`. Fehlt es – also in jedem Bestand bis Format 5 –, gilt der Punkt als gewöhnliche Aufgabe; ein destruktiver Migrationsschritt entfällt. Komplettbackups der Formate 4 und 5 bleiben importierbar, ein Backup mit unbekannter Punktart wird abgewiesen.
- TXT führt Gruppen mit Ordnermarker an derselben Stelle wie die Wichtigkeitsmarker und liest ihn beim Import zurück. Markdown gibt Gruppen als fette Zeile ohne Kontrollkästchen aus. CSV erhält die zusätzliche Spalte „Art“ am Ende; die Position aller bisherigen Spalten bleibt unverändert. Kopieren und Einfügen behalten die Punktart.

### QA

- Der Integrationstest prüft zusätzlich das Gruppen-Datenmodell, Darstellung, Statistik, Statusfilter, Export- und Importrundlauf, die Vollständigkeit aller Kontextmenüs, eindeutige IDs beim Duplizieren sowie die Auswahl des schwersten Schriftschnitts. Die neuen Zusicherungen schlagen gegen 2.5.5 fehl.
- Keine neue Laufzeitabhängigkeit.

## 2.5.5 – 01.09.2026

### Behoben und gehärtet

- Anhänge, deren Dateiname nach der Bereinigung auf einen Punkt endete (`report.`, `a.b.`) oder deren Endung außerhalb von A–Z/0–9 lag (`daten.☃`), erhielten einen Speicherpfad, den die Anhangsprüfung ablehnt. Sie galten sofort als „nicht gefunden“, verschwanden beim nächsten Start still aus den Daten und ließen jedes Komplettbackup scheitern. Namensbildung und Prüfung liegen jetzt in einer gemeinsamen Funktion, die vor dem Kopieren validiert; Datensatz-ID und Dateiname bleiben gekoppelt, der Anzeigename bleibt vollständig erhalten.
- Das Laden eines Komplettbackups konnte die Anwendung einfrieren: Die Suche nach einem freien Zielnamen für importierte Anhänge lief unbegrenzt, wenn der Anzeigename nicht normierbar war. Die Suche ist jetzt begrenzt und meldet im Ausnahmefall einen Fehler.
- Ein langer Listentitel schob den Design-Umschalter und die Fortschrittszeile aus dem Fenster. Der Kopfbereich reserviert deren Platz zuerst; der angezeigte Titel wird nur so weit gekürzt wie nötig. Gespeicherter Titel, Fenstertitel, Seitenleiste und Exporte bleiben vollständig.
- Eine gespeicherte Fensterposition wird auf den sichtbaren Bereich begrenzt. Nach einem Monitorwechsel startete das Fenster zuvor außerhalb jeder Anzeige. Dialoge werden ebenfalls begrenzt.
- Der Listenaufbau registrierte bei jedem Durchlauf eine `after`-ID, die nie entfernt wurde. Aufrufe innerhalb eines Leerlaufzyklus werden zusammengefasst, abgelaufene IDs verworfen.
- Alle Zugriffe auf das Fokus-Widget laufen über einen abgesicherten Aufruf; `focus_get()` löst eine Ausnahme aus, sobald der Fokus auf einem von Tk selbst erzeugten Fenster liegt.
- Ausrücken und Verschieben hinterließen in Fehlerpfaden einen wirkungslosen Rückgängig-Schritt oder verwarfen umgekehrt eine erfolgte Änderung ungespeichert. Beide Fälle sind bereinigt.
- `settings.json` wird atomar geschrieben wie die Nutzdaten.

### Darstellung

- Titel, Beschreibung und Anhangsliste in „Punktdetails“ beginnen an derselben senkrechten Linie. Zuvor stand der Titeltext bündig an der Feldkante, während die Beschreibung eingerückt war.
- Alle Eingabeflächen der Anwendung verwenden einen gemeinsamen Feldrahmen mit identischem Innenabstand; Beschriftungen stehen bündig an der Feldkante.
- Seitenleisten-Box und untere Aktionsgruppe im Hauptbereich enden auf derselben Linie.
- Der 10-px-Einzug der Seitenleisten-Trennlinie bleibt unverändert; er richtet die Linie an der Textspalte von „Eingang“ und „Listen“ aus. Der zuvor irreführende Codekommentar wurde korrigiert und der Wert als Konstante benannt.

### macOS

- Cmd+Q löst über `::tk::mac::Quit` den regulären Schließvorgang aus. Zuvor umging macOS `WM_DELETE_WINDOW`, wodurch die Abfrage zu ungespeicherten Änderungen und das Sichern der Fenstergeometrie entfielen.
- Die Rückschritt-Taste löscht ausgewählte Punkte, da Mac-Tastaturen in der Regel keine Entf-Taste besitzen. In Eingabe- und Suchfeld bleibt sie unverändert.
- Ergänzte Command-Kürzel für Speichern, Export, Import, Design wechseln, neue Liste und Wichtigkeit. Cmd+W und Cmd+M bleiben bewusst unbelegt, weil macOS sie für „Fenster schließen“ und „Minimieren“ vorsieht.
- Menü- und Hilfetexte zeigen plattformgerecht „Cmd“ statt „Strg“ und „Rückschritt“ statt „Entf“.
- Der modale Dialog gibt seinen Grab für den nativen Dateiauswahldialog kurz frei.

### Tests und Datenpfade

- `GLIDE_DATA_DIR` überschreibt den Nutzerdatenordner vollständig und ist der einzige plattformunabhängige Weg, Tests zu isolieren. Der Integrationstest setzte bisher nur `APPDATA`, was ausschließlich unter Windows wirkt; auf macOS oder Linux hätte ein Testlauf die echten Nutzerdaten verwendet und überschrieben. Der Test isoliert jetzt über `GLIDE_DATA_DIR`, womit AGENTS.md Regel 5 auf allen Plattformen gilt.

### Kompatibilität und QA

- Datenformat bleibt Version 5; Nutzerdatenpfade sowie Import- und Exportformate sind unverändert.
- In beide Richtungen geprüft: 2.5.4 schreibt – 2.5.5 liest und umgekehrt, jeweils inklusive Ordnern, Beschreibungstexten, Anhängen und Komplettbackup.
- Integrationstestsuite grün; ergänzt um Regressionstests für kritische Anhangsdateinamen, den vollständigen Backup-Rundlauf, die Kopfzeilenbreite und die Feldabstände in allen Dialogen.
- Keine neue Laufzeitabhängigkeit.

## 2.5.4 – 02.09.2026

### Neu und verbessert

- „In Bearbeitung“ zeigt chronologisch alle Aufgaben mit gültigem Fälligkeitsdatum aus allen Listen. Die Ansicht ist rein abgeleitet, speichert keine Aufgabenkopien und führt per Doppelklick, Enter oder Kontextmenü zur Originalaufgabe.
- Listen lassen sich nun auch in der Ordnerübersicht per Drag & Drop umsortieren oder in einen anderen Ordner verschieben.
- Ordner besitzen im Rechtsklickmenü die gezielte Aktion „Beschreibungstext bearbeiten …“. Die bisher sichtbare Bezeichnung „Seitennotiz“ wurde für Listen und Ordner einheitlich durch „Beschreibungstext“ ersetzt; das kompatible Datenfeld und alte TXT-Blöcke bleiben lesbar.
- Lange Listen- und Ordnernamen laufen in der Seitenleiste nach 20 Zeichen mit `...` aus, ohne den gespeicherten Titel zu verändern.

### Behoben und gehärtet

- Eingang und „Listen“ beginnen an derselben linken Kante. Ein ausgerichteter horizontaler Balken trennt die beiden Systemzeilen mit gleichem sichtbarem Abstand nach oben und unten vom Listenbereich.
- Seitenleistenordner behalten ihren eigenen Auf-/Zu-Zustand bei Aktualisierungen; das Schließen eines zweiten Ordners öffnet keinen zuvor geschlossenen Ordner mehr.
- Der Pfeil verschachtelter Aufgaben liegt mit Innenabstand im Auswahlbalken; ein Klick auf ihn klappt Elternaufgaben trotz eigener Drag-Bindings zuverlässig ein und aus.
- Die feste Fälligkeitsanzeige erhält einen konstanten rechten Innenabstand innerhalb des lila Aufgabenbalkens.
- Neue Anhänge werden atomar als lokale Kopie gespeichert und vorab auf die bestehende 512-MB-Grenze geprüft. Ein Fehler beim Übernehmen mehrerer Dateien räumt bereits neu erzeugte Kopien auf.

### Kompatibilität und QA

- Datenformat bleibt Version 5; keine virtuelle Systemansicht und kein gekürzter Titel werden in Nutzdaten geschrieben.
- Format-4-Komplettbackups, ältere JSON-Daten und historische TXT-Markierungen für Beschreibungstexte bleiben unterstützt.
- Der erweiterte Integrationstest prüft Layoutgeometrie, Einklappzustände, Ordnerübersicht-DnD, Quellnavigation, Anhangskopien sowie die Nicht-Persistenz der Smart-Ansicht.
- Keine neue Laufzeitabhängigkeit.

## 2.5.3 – 01.09.2026

### Behoben und verbessert

- Das Aufgaben-Kontextmenü bleibt nach dem Öffnen bestehen; Bearbeiten, Wichtigkeit, Fälligkeit, Farbe und Entfernen lassen sich wieder per Rechtsklick ausführen.
- Eine eigene, feste Datumsspalte hält vorhandene Fälligkeiten unabhängig von Aufgabentext, Einrückung und Fensterbreite ganz rechts innerhalb der Aufgabenzeile.
- Der Eingang wird ohne Haussymbol und unabhängig von einer gespeicherten Listenfarbe mit derselben schwarzen beziehungsweise themegerechten Schriftwirkung wie die Überschrift „Listen“ dargestellt.

### Struktur und QA

- Der neue äußere Bereich `50_Ablage` trennt projektbegleitende QA- und Zwischenstände vom kanonischen Repository und vom dauerhaften Archiv.
- Zehn bisherige DOCX-QA-Ordner wurden unverändert nach `50_Ablage/QA/Dokumentation/Renderlaeufe` verschoben. Ein SHA-256-Manifest bestätigt 237 Dateien und 70.203.909 Bytes ohne Abweichung.
- Der Integrationstest prüft zusätzlich die Lebensdauer des Rechtsklickmenüs, die feste Fälligkeitsspalte und den Eingang-Stil.

### Kompatibilität

- Datenformat bleibt Version 5; Format-4-Komplettbackups und ältere JSON-Daten bleiben unterstützt.
- Keine neue Laufzeitabhängigkeit.

## 2.5.2 – 01.09.2026

### Neu und verbessert

- Der feste Eingang besitzt in der Seitenleiste ein eigenes einzeiliges Feld oberhalb der normalen Listen; ein sichtbarer Abstand trennt beide Bereiche.
- Das Aufgaben-Kontextmenü bietet Bearbeiten von Titel, Beschreibung und Anhängen sowie direkte Auswahl von Wichtigkeit, Fälligkeit und Aufgabenfarbe. Die Metadatenaktionen funktionieren auch für Mehrfachauswahl.
- Aufgabenfarben werden im Datenmodell gespeichert, beim Laden normalisiert und in der Aufgabenansicht dargestellt.
- Der native Windows-Dark-Mode wird nach dem tatsächlichen Mapping des Hauptfensters und der Dialoge mit begrenzten Wiederholungen angewendet. Dadurch ist die Titelleiste bereits beim Start im gespeicherten Dark Mode dunkel.

### Behoben und gehärtet

- Die unter Windows/Tk nicht überall bekannte Sequenz `ISO_Left_Tab` wird optional gebunden und kann den App-Start nicht mehr abbrechen.
- Auswahl, Kontextmenü und Drag-&-Drop-Zielerkennung berücksichtigen den getrennten Eingang und den normalen Listenbaum konsistent.
- Komplettbackups aus Glide 2.5.1/Datenformat 4 bleiben importierbar und werden beim Laden verlustfrei auf Datenformat 5 normalisiert.
- Der Integrationstest prüft den separaten Eingang, Aufgabenmetadaten und -farben, das Kontextmenü, die v4→v5-Kompatibilität sowie unter Windows den realen DWM-Wert beim ersten Fenster-Mapping und beim Theme-Wechsel.

### Kompatibilität

- Datenformat 5 ergänzt die optionale Aufgabenfarbe.
- Bestehende JSON-Daten bis Format 4 sowie vollständige `.glidebackup`-Archive aus Format 4 bleiben unterstützt.

## 2.5.1 – 31.08.2026

### Neu

- Ordner zeigen ihre enthaltenen Listen direkt im Hauptbereich; Doppelklick oder Enter öffnet eine Liste.
- Fest integrierter, geschützter Eingang für unsortierte Aufgaben.
- Aufgaben lassen sich per Drag & Drop in andere Listen oder über einen Ordner in eine Zielliste verschieben.
- Freie Seiten- und Ordnernotizen.
- Aufgabendetails mit mehrzeiliger Beschreibung sowie lokalen Datei-/Bildanhängen.
- Portables `.glidebackup` mit Daten und Anhängen.
- Dunkle Windows-Menüzeile und – soweit vom Betriebssystem unterstützt – dunkle native Titelleiste.

### Behoben und gehärtet

- NumLock wurde unter Windows von Tk nicht länger als Command-Taste fehlinterpretiert; Eingaben springen dadurch nicht mehr zur Suche und `a` löst nicht mehr „Alles auswählen“ aus.
- Das dunkle Windows-Menü verwendet robuste Buttons statt falsch geparenteter Menubuttons.
- CapsLock löst nicht versehentlich Strg+Shift-Kürzel aus.
- Drops außerhalb von Aufgabenbaum oder Seitenleiste verändern keine Einträge mehr.
- Speichern liefert einen eindeutigen Erfolgsstatus und hält fehlgeschlagene Änderungen als „ungespeichert“ fest.
- Komplettbackups werden atomar geschrieben und bei fehlenden Anhängen abgebrochen.
- Restore prüft Schema, IDs, Pfade, Größen, ZIP-Inhalt und Referenzintegrität vor jeder Änderung.
- Importierte Anhänge erhalten neue Dateinamen; vorhandene Dateien werden niemals überschrieben.
- Vor jedem Restore wird ein vollständiges Rückfall-Backup erzeugt.
- TXT-Import erhält Seitennotizen, mehrzeilige Beschreibungen und Fälligkeiten; notiz-only TXT/Markdown-Export ist möglich.
- CSV-Nutzertexte werden gegen Formelausführung in Tabellenprogrammen abgesichert.

### Kompatibilität

- Datenformat bleibt Version 4.
- Ältere JSON-Formate und die frühere direkte Aufgabenliste bleiben importierbar.

## 2.5.0 – Zwischenstand

Unvollständiger Entwicklungsstand, aus dem 2.5.1 stabilisiert wurde. Nicht als finaler Release vorgesehen.

## 2.4.1

Letzter vorhandener Stand vor der Notion-/Quality-of-Life-Erweiterung.
