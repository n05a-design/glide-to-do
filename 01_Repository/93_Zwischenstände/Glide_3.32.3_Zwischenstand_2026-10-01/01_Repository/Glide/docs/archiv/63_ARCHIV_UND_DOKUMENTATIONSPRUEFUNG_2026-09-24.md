# Archiv- und Dokumentationsprüfung

Stand 24.09.2026 · Glide 3.28.0 · Aufgabenformat 18

## Zweck

Diese Prüfung reduziert den aktiven Lesebestand für neue Bearbeiter und
Agenten. Historische Nachweise bleiben erhalten, dürfen aber nicht mehr als
aktueller Projektstand gelesen werden. Maßgeblich bleiben der
[Dokumentationsindex](00_INDEX.md), die
[Zeichenflächen-Übergabe](62_ZEICHENFLAECHE_WEITERGABE_2026-09-24.md), der
[Dokumenten-Existenzbericht](64_DOKUMENTEN_EXISTENZPRUEFUNG_2026-09-24.md), der
[QA-Bericht](07_QA_BERICHT.md) und die jeweils dort verlinkten Fachverträge.

## Ergebnis

Die automatische Standprüfung sank von **sieben Befunden auf null**. Nach der
anschließenden Existenzprüfung klassifiziert sie 76 nicht archivierte
Markdown-Dokumente: 38 fortgeschriebene Dokumente, 34 festgeschriebene Belege
und vier Dateien ohne Standaussage.
Festgeschrieben bedeutet nicht automatisch aktiv zu lesen: datierte
Prüfbelege und ausdrücklich historische Unterlagen bleiben nur als Nachweis.

Vor jeder Korrektur wurden 21 damalige Dokumentstände in den zuständigen
Archivordner kopiert. Anschließend wurden 44 eindeutig historische Langdokumente, Dateien
beziehungsweise Arbeitsordner aus aktiven Bereichen verschoben. Gelöscht wurde
nichts.

## Archivierte Altstände

Aus der aktiven Arbeitsvorbereitung wurden verschoben:

- alte manuelle Prüfungen 3.21.4 bis 3.25 sowie die Geräteabnahme 3.23;
- sämtliche abgeschlossenen Ausführungspläne 2.5.1 bis 3.0 sowie sechs
  ausdrücklich historische Repository-Berichte sowie der 3.26-Umsetzungsstand;
- alte Entscheidungs- und Faktenblätter 3.21.4 bis 3.26;
- Abschlussberichte 3.23 und 3.25;
- Chat-Weitergaben vom 16.09. und 23.09.2026;
- ältere Gesamt-, Konkurrenz-, Feature-Gap- und KI-Vorschlagsanalysen;
- der Prüfbericht und die Umsetzungshilfen zu 3.26;
- der vollständige Eingabe- und Bildbestand des Auftrags 3.25/3.26.

Zusätzlich wurden archiviert:

- die drei noch aktiv liegenden Nutzerdateien 3.21.4 aus
  `05_Probelisten_Testdaten`;
- die Vorlagenanleitung 3.21.4 aus `10_Dokumentation`;
- das Produktdatenblatt 3.21.4 und die langen historischen Store-Recherchen;
- sämtliche vor der Bereinigung gültigen Fassungen der geänderten READMEs und
  Verträge.

Lange historische Inhalte, auf die alte Links noch zeigen, besitzen höchstens
einen kurzen aktiven Wegweiser. Der Wegweiser enthält keine alte Planung und
verweist eindeutig ins Archiv.

## Aktualisierte aktive Verträge

Folgende echte Gegenwartsfehler wurden korrigiert:

- portable Backupformate überall von 4–17 auf **4–18**;
- Produktregister auf Datenformat **18**;
- Startkontext auf Notizformat 17 und Tagebuchformat 18;
- Vorlagenanleitung auf die aktiven Dateien 3.28.0 und Aufgabenformat 18;
- Release-Export auf Aufgabenformat 18 und fehlendes aktuelles
  Produktdatenblatt;
- Ablage-README auf App-Stand 3.28.0 und den aktuellen QA-Bericht;
- der KI-Architektur-Wegweiser auf den aktuellen Stand und sein Archivziel;
- Probedaten-README nach erfolgreicher Verschiebung der 3.21.4-Dateien.

## Bewusst weiterhin nicht archiviert

Nicht jede Datei mit einer älteren Versionsnummer ist überholt:

- `docs/45_...` bis `docs/58_...` sind im aktuellen Index ausdrücklich als
  fortgeltende Funktionsverträge geführt. Sie dokumentieren die Einführung
  noch vorhandener Funktionen und werden erst archiviert, wenn ein neuer
  kumulativer Vertrag sie ersetzt.
- ältere Dateien unter `tests/fixtures` und `90_Testdaten_Extern` sind aktive
  Migrations- und Kompatibilitätseingaben. Ihre alten Formatnummern sind ihr
  Testzweck.
- datierte QA-Ergebnisse unter `tests/qa-*` und `50_Ablage/QA` sind
  unveränderliche Prüfbelege, keine aktuelle Freigabe.
- `07_Python-Versionen/Archiv` enthält bewusst startbare Altstände; aktiv liegt
  dort nur die aktuelle Arbeitskopie.

Diese Ausnahmen verhindern, dass für Migration, Regression oder einen
fortgeltenden Funktionsvertrag notwendige Belege versehentlich entfernt werden.

## Leseregel für einen neuen Agenten

1. `AGENTS.md` lesen.
2. Dieses Dokument und `docs/62_ZEICHENFLAECHE_WEITERGABE_2026-09-24.md` lesen.
3. Nur die dort für die konkrete Aufgabe genannten Fachverträge öffnen.
4. `Archiv/` oder `archiv/` ausschließlich bei einer historischen Frage,
   Regression oder Migrationsprüfung durchsuchen.
5. Datierte Dateien nicht als aktuellen Stand interpretieren.
6. Vor einer Dokumentänderung die aktive Fassung erneut archivieren.

Damit ist ein Vollscan der historischen Ablage für normale Folgearbeiten weder
notwendig noch erwünscht.

## Prüfung

Ausgeführt wurden:

- Versionskonsistenz von `VERSION`, App, Hauptsuite und Changelog;
- `standpruefung.py` über die gesamte Ablage;
- Repository-Dokumentationsindex einschließlich Archiv;
- lokale Markdown-Dateilinks der aktiven Repository-Dokumente;
- Suche nach Gegenwartsbehauptungen mit alten App- und Formatständen;
- projektweite Prüfung von 959 lokalen Links in 77 aktiven Markdown-Dateien;
- Kontrolle der aktiven Probedaten-, Dokumentations-, Store- und
  Arbeitsvorbereitungsordner.

Die Standprüfung meldet **keinen Befund**. Die verbleibenden roten Punkte eines
früheren Gesamtlaufs betreffen die bekannten Fixture-, Vorlagen- und
UI-Regressionen; sie sind keine Archiv- oder Dokumentationsfehler.

Eine anschließende strengere Existenzprüfung archivierte zusätzlich sechs
aktive Dateien ohne eigenständigen Gegenwartszweck und ordnete jede
verbliebene Dokumentdatei einer begründeten Bestandklasse zu. Der vollständige
Nachweis steht in der
[Dokumenten-Existenzprüfung](64_DOKUMENTEN_EXISTENZPRUEFUNG_2026-09-24.md).
