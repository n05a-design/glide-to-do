# Prüfungen für Glide

Stand 26.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · 40 Suiten aus `pruefen.py` und fünf Analysen. Alle App-Tests setzen vor dem App-Import einen temporären `GLIDE_DATA_DIR`; echte Nutzerdaten sind ausgeschlossen. Die isolierten Zeichentests importieren `ListApp` nicht und berühren keinen Datenordner; `test_features329.py` prüft die produktive Zeichnungsseite, `test_drawing330.py` den erweiterten Zeichenkern und `test_features330.py` alle Pakete aus 3.30, jeweils mit eigenem temporärem Datenordner.

Vollständiger Lauf aus dem Repository-Stamm `01_Repository/Glide`: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.30.0/abschluss --timeout 900`. Unter Windows startet `tests/tools/windows_vollpruefung.cmd` denselben Lauf. Unter Windows heißt der Aufruf `python`; das Zeitlimit von 300 Sekunden je Suite ist dort mit Virenschutz und synchronisiertem Ordner knapp, `--timeout 900` ist realistischer.

Der Prüfstand setzt `TZ=Europe/Berlin`, wenn der Aufrufer keine Zone vorgibt, und **misst seit 3.23.0 nach, was davon tatsächlich gilt**. In einer Zone ohne Versatz ist jeder Zeitzonenfehler unsichtbar: Der `UNTIL`-Fehler aus 3.21.0 war in einer UTC-Vorabumgebung grün und fiel erst im macOS-Lauf auf.

**Unter Windows wird `TZ` nicht gesetzt.** Die dortige Laufzeit kennt kein `time.tzset()` und liest aus `Europe/Berlin` keine benannte Zone, sondern eine erfundene ohne Sommerzeitregel – im ersten Windows-Lauf meldete sie sich als „ope“ mit +01:00, während in Berlin +02:00 galt. Jede Umrechnung in Ortszeit lag damit eine Stunde daneben. Maßgeblich ist dort die Systemzeitzone; wer eine andere Zone nachstellen will, stellt sie um. Misst der Schritt „Zeitzone“ einen Versatz von null – oder findet er unter Windows ein gesetztes `TZ` –, endet der Lauf mit Exitcode 2: unvollständig, nicht bestanden. Mitgemessen wird, ob die Zone eine Sommerzeitregel kennt; ohne sie lässt sich die Fehlerklasse um Serienenden nicht zeigen.

## Was der Vollmodus umfasst

| Gruppe | Inhalt |
|---|---|
| Vorprüfungen | Syntax, Versionskonsistenz (VERSION, `APP_VERSION`, Hauptsuite, CHANGELOG), Dokumentationsindex mit Linkzielen, Fixtures samt historischen Referenzformaten, Tk-Voraussetzung und seit 3.23 der gemessene Zeitzonenversatz |
| 40 Suiten | Kernfunktionen, Datenintegrität, isoliertes Zeichenmodell samt JSON-/SVG-Rundlauf, Bedienprobe mit Referenzrahmen, Zentrierung, erstem Strich und Farbeingabe, Audit, Themes, UI, Vorlagen, Backups, Migration, Benachrichtigungen, Reiter/Pinnwand, Schnellerfassung und Filter, „Mein Tag“, Tabellenansicht, Planung und Aufwand, Tagesplanung, App-Backup, Druck/PDF, CSV-Import, Änderungsverlauf, Kalenderausgabe, Kalenderimport, Checkliste seit 3.23 Designsystem, Anzeigemodi, Austauschformat und Pinnwandfläche, seit 3.24 Navigation, globale Pinnwand und Startansicht und seit 3.25 Übersichtlichkeit und Hierarchie (`test_features325.py`) sowie die Breitenprüfung (`test_vollpruefung325.py`) und seit 3.29 die Zeichnungsseite mit Format-19-Migration, Autosave, Schreibfehler, Referenz, Nachzeichnung, Rückgängig, Backups, Austausch, Vorlagen und Tagebuch (`test_features329.py`) und seit 3.30 Pixel-Werkstatt, Format 20, Startseite, Board, Tagebuch und Detailbereich (`test_drawing330.py`, `test_features330.py`), Mindestgröße aller Ansichten und Dialoge (`test_mindestgroesse330.py`), Kontrast nach WCAG AA in allen Designs (`test_kontrast330.py`) und die Paketierungsvorstufe (`test_paketierung330.py`) |
| Fünf Analysen | `analyse_statisch.py`, `analyse_erreichbarkeit.py`, seit 3.21.3 `standpruefung.py` (Standangaben und Formatstufen der Dokumente gegen VERSION und `DATA_SCHEMA_VERSION`), seit 3.23 `attributpruefung.py` (Aufrufe über `self` ohne Ziel in ihrer Klasse) und seit 3.25 `dublettenpruefung.py` (wiederholte Codeblöcke; meldet, bewertet aber nicht) |
| Reproduktion | Beispieldaten und Releasedaten neu erzeugen und mit den Fixtures vergleichen; Bilder nur auf geeigneten Plattformen |

Übersprungen bleiben regelmäßig nur die plattformgebundene Screenshot-Erzeugung und die Sichtprüfung; beide sind ausdrücklich manuelle Aufgaben. Ein übersprungener Schritt „Tk-Voraussetzung“ oder „Zeitzone“ ist etwas anderes: Er bedeutet, dass der Lauf einen Teil seiner Aussage nicht treffen kann, und zieht Exitcode 2 nach sich.

## Gezielte Läufe

- `python3 tests/integration/test_ui39.py` – eingebettete Dropdowns, echte Außenklickereignisse, Tastatur, unveränderte modale Grabs, Dialoggrößen, Kopfzeile, Einstellungen, Seitenleiste und App-Aktionen.
- `python3 tests/integration/test_workspace310.py` – Reiter und Pinnwände, Referenzidentität, Einstellungen und native Tk-Ereignisse.
- `python3 tests/integration/test_features314.py` – Planung, Aufwand, Datenformat-14-Migration und Sicherungsfehler, gemeinsame Aktionen, Vorlagen, Backups, Exporte sowie Dialoge in beiden Themes.
- `python3 tests/tools/standpruefung.py` – nur die Standangaben und Formatstufen; läuft ohne Tk und in Sekunden.
- `python3 tests/integration/test_features325.py` – jeder Punkt des Auftrags vom 19.09.2026 einzeln: Feldraster, erweiterte Eingabe in Übersichten, aufklappbare Abschnitte, nächste Aufgabe, Menügruppen, Handbuch, Minimaldesigns, Rückmeldungsstufen, Pinnwandverbindungen, Startseite und Fehlerbericht.
- `python3 tests/integration/test_vollpruefung325.py` – Breitenprüfung: jede Ansicht in jedem Design in drei Fensterbreiten, jeder Anzeigeumfang, jede Startseitenkachel einzeln, jede Menüaktion, jede Pinnwandaktion. Dauert länger als jede andere Suite und findet eine andere Art Fehler: den Aufruf, den es in dieser Klasse nicht gibt, und den Themeschlüssel, den ein Design nicht kennt.
- `python3 tests/integration/test_features329.py` – produktive Zeichnungsseite: Typregistrierung, Ablehnung unbekannter Listenarten, Format-19-Vorsicherung, eingebettete Fläche ohne Extrafenster, Pinselvorschau je Zoom, gebündeltes Autosave, Schreibfehler, Referenz-PNG, Nachzeichnung mit Vorher-Snapshot, Duplizieren, Papierkorb, Backups, Austausch, Vorlagen, Datei-Import/-Export und Tagebuchübersicht.
- `python3 tests/integration/test_drawing330.py` – Zeichenkern 3.30:
  - Rückgängig je Aktion, Formen, Symmetrie, Muster, Kachel;
  - Auswahl, Farbe ersetzen, Paletten, PNG-Kodierung, Größen 16–128.
- `python3 tests/integration/test_features330.py` – alle 3.30-Pakete:
  - Zeichen-Editor, Format 20, Beziehungen, Zeit, Symbole, Archiv;
  - Startseite anpassen, Suche, Gruppierung, Spaltenboard, Pinnwandbereiche
    und Präsentation;
  - Tagebuch, Detailbereich, Leerzustände, Design „Pixel“, Vorlagen mit
    Eingabefeldern, Zeitblöcke;
  - Referenz-Fixture Format 20 und Regressionen der mitbehobenen Fehler.
- `python3 tests/integration/test_mindestgroesse330.py` – jede Ansicht bei 860 × 700
  in fünf Kombinationen aus Design, Schriftgröße und Fenstergröße, dazu jeder Dialog der Menüleiste
  bei seiner Mindestgröße. Befunde: Überstand, Quetschung, abgeschnittener Text. Braucht keinen
  Bildschirm.
- `python3 tests/integration/test_kontrast330.py` – Kontrast jedes dargestellten Texts
  und jedes Knopfzustands in allen zehn Designs (WCAG AA).
- `python3 tests/integration/test_paketierung330.py` – Kennungen, Windows-Skript und unter macOS
  das gebaute, signierte Entwicklungsbundle.
- `python3 tests/integration/test_drawing.py` – isolierter Vertrag für Zellmodell, Pinsel, 4er-Füllung, zellweises Undo, kanonisches JSON, Glide-SVG und verbotene SVG-Inhalte; keine produktiven Nutzerdaten und kein `ListApp`-Import.
- `python3 tests/integration/test_drawing_prototype.py` – Tk-Regression für den ersten Strich, horizontale und vertikale Zentrierung, flexible Farbeingabe, Einpassen einer PNG-Referenz sowie den Nachzeichner mit Weißhintergrund, Konturerhalt und höchstens 64 Farben.
- `python3 tests/tools/dublettenpruefung.py --laenge 8` – wiederholte Codeblöcke; ohne Tk, in Sekunden.

Termine in Suiten liegen bewusst in der Zukunft. Ein Punkt mit Fälligkeit „heute 14:00“ und relativer Erinnerung wurde ab 13:30 Ortszeit mitten im Lauf ausgeliefert und veränderte den Bestand – zwei Suiten schlugen dadurch tageszeitabhängig fehl.

[Aktueller QA-Bericht](../docs/07_QA_BERICHT.md) · [Prüfplan und manuelle Grenzen](../docs/05_QA_TESTPLAN.md).
