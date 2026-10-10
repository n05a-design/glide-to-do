# Native Baseline vor 3.36.0

Stand 10.10.2026 · Glide 3.35.0 · App unverändert · künstliche Daten

[Actions-Lauf 38034929760](https://github.com/n05a-design/glide-to-do/actions/runs/38034929760) prüfte den Commit `38b3e1329b3490c6662898b65d9cb64c7f5b9076`. Dieser enthält nur den bestätigten Sprintplan und die verpflichtenden nativen Jobs; Produktionscode, 07 und Bundle entsprechen weiterhin 3.35.0. Grundstufe grün. Die Jobs liefen nacheinander.

| Prüfstand | Ergebnis und Grenze |
|---|---|
| Linux/Xvfb, Python 3.14.8, Tk 8.6 | [Vollständiges Ergebnis](linux.json): 95 ausgeführt, fünf fehlgeschlagen, menschliche Sichtprüfung übersprungen; insgesamt 82 Integrationssuiten aufgerufen. |
| Windows x64 | Checkout fehlgeschlagen: ein vorhandener langer Grafik-Dateiname. Keine App-Prüfung ausgeführt; daraus folgt kein Windows-Funktionsbefund. `core.longpaths` wird vor Checkout aktiviert. |

Die fünf Linux-Befunde: `test_mindestgroesse330` und `test_rueckmeldung330` erwarten einen Kopfzeilenplatz ohne offene Hinweise, verwenden jedoch uhrzeitabhängige Erinnerungs-Fixtures; `test_befunde330` verlangt SVG-Konvertierung auch ohne SVG-Leser; `test_tempo330` erzeugt das unter Tk 8.6 unbekannte TouchpadScroll-Ereignis; `test_planen33313` übernimmt im nativen Lauf nicht den gewählten Tag. Der letzte Fall ist ungeklärt und erhält zunächst zusätzliche Feld-/Fehlerdiagnostik. Keiner gilt hier als behoben oder abgenommen.

Rohprotokolle verbleiben lokal bzw. als zeitlich begrenzte Actions-Artefakte. Kalibrierung, echte Defekt-Gegenfälle und erneute vollständige native Läufe gehören zur Lieferung 3.36.0.
