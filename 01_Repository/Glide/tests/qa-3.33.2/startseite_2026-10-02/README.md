# Startseite 3.33.2 – Nachweis

02.10.2026 · App 3.33.2 · macOS, Python 3.14.5, Tk 9.0 · temporäres `GLIDE_DATA_DIR`, keine echten Nutzerdaten · [Funktionen, Startseite](../../../docs/20_FUNKTIONEN.md#7-startseite)

## Ausgangsstand

`vorher/quelle`: Quellstand 3.33.1, wie am 02.10.2026 geprüft und ausgeliefert (App-Prüfsumme `0d432ea8…`). Er dient als Vergleichsstand der Messungen (`--app`).

## Messung

`scripts/pflege/messung_startseite.py` (neu): feste Inhalte mit 1.000 Punkten in zwölf Listen, Bearbeitungstage und Fälligkeiten über die Woche verteilt, drei Zeichnungen, zwei angeheftete Seiten; Fenster 1400 × 950; je Lauf ein Aufwärmwert und sechs warme Runden; „Wechsel“ von einer Liste zur Startseite, „Aktualisierung“ als Neuaufbau an Ort und Stelle; `--kacheln alt` (zwölf Kacheln bis 3.33.1) bzw. `d12` (sieben Kacheln). Alter und neuer Code laufen abwechselnd in vier Paaren (`messung/`). Ergänzend `messung_performance.py` für alle Ansichten in zwei Paaren.

[Zusammenfassung](messung/zusammenfassung.json): Aktualisierung der Startseite im Median 764,2 ms (3.33.1, zwölf Kacheln) → 506,7 ms (3.33.2, sieben Kacheln); bei gleichen zwölf Kacheln 620,7 ms. Wechsel 789,7 → 547,8 ms. Ansichtswerkzeug: Bibliothek 974 → 856 ms, übrige Ansichten unverändert. Keine Callbackfehler. Verhalten: [Funktionen, Startseite](../../../docs/20_FUNKTIONEN.md#7-startseite).

## Ursachensuche

Profil und Gegenproben (Probe-Skripte im Arbeitsverzeichnis der Sitzung, Ergebnisse im Vertrag): Python-Anteil rund 90 ms, Rest Tk-Layout mit rund zehn Größenmeldungen je Widget. Gewinn je Maßnahme bei zwölf Kacheln: Tcl-Filter rund 90 ms, Zeichnen rund 220 ms Obergrenze, Umbruch rund 50 ms, Hintergrundfarbe rund 37 ms. Ohne Gewinn: Ausblenden während des Aufbaus, Schriften vorhalten.

## Vollprüfung und Auslieferung

[Eingefrorener Quellstand](quellstand.json) mit 329 Dateien. Erster Versuch ([Ergebnis](vollpruefung_versuch1/ergebnis.json), [damaliger Quellstand](quellstand_versuch1.json)): 77 Schritte grün, `attributpruefung` rot – die Hilfsklasse für gebündeltes Zeichnen erbte nicht von `tk.Canvas`. Nach der Korrektur (`DeferredDrawCanvas`) gezielte Suiten grün und zweiter Lauf ([Ergebnis](vollpruefung/ergebnis.json), rund 11:00–11:24, entsperrt, ohne Eingaben, `caffeinate -dims`): **Exitcode 0**, 78 Schritte, zwei plattformbedingt übersprungen; Quellstand vor und nach dem Lauf unverändert.

[Lieferabgleich](auslieferung.json): `abgleich_07.py` ohne Abweichung, 3.33.1-Hauptdatei als `_Z` archiviert; Bundle neu gebaut; 143 Dateien in `07_Python-Versionen` und 57 im Bundle per SHA-256 gleich `src/glide`, Bundle 3.33.2, `de.shaye.glide`, Signatur gültig. Showcase mit `showcase_abgleich.py` ausgeliefert (vorherige Daten im Showcase-Archiv).

## Gegenprobe

`test_startseite3332.py` mit dem Quellstand 3.33.1 (`vorher/quelle`): Exitcode 1 am D12-Standard; mit 3.33.2 Exitcode 0.
