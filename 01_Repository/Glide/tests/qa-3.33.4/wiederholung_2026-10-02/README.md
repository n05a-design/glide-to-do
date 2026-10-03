# Wiederholungen in der Eingabe 3.33.4 – Nachweis

02.10.2026 · App 3.33.4 · macOS, Python 3.14.5, Tk 9.0 · temporäres `GLIDE_DATA_DIR`, keine echten Nutzerdaten · [Funktionen, Erfassen](../../../docs/20_FUNKTIONEN.md#3-erfassen)

## Vollprüfung und Auslieferung

[Eingefrorener Quellstand](quellstand.json) mit 334 Dateien. [Vollprüfung](vollpruefung/ergebnis.json) rund 13:27–13:51, entsperrt, ohne Eingaben, `caffeinate -dims`: **Exitcode 0**, 79 Schritte, zwei plattformbedingt übersprungen; Quellstand vor und nach dem Lauf unverändert. [Lieferabgleich](auslieferung.json): 144 Dateien in `07_Python-Versionen` und 58 im Bundle per SHA-256 gleich `src/glide`, Bundle 3.33.4, `de.shaye.glide`, Signatur gültig; Showcase ausgeliefert.

## Gezielte Prüfungen

- 51 Unit-Tests grün, davon drei neue für Wiederholungen.
- `test_eingabe3333.py` mit neuem Block grün; Gegenprobe mit dem ausgelieferten Stand 3.33.3 (`07_Python-Versionen`): Exitcode 1, „Sport jeden Montag 18 Uhr“ wurde dort als Bearbeitungstag erkannt.
