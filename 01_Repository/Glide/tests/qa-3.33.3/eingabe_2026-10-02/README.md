# Schnelleingabe 3.33.3 – Nachweis

02.10.2026 · App 3.33.3 · macOS, Python 3.14.5, Tk 9.0 · temporäres `GLIDE_DATA_DIR`, keine echten Nutzerdaten · [Funktionen, Erfassen](../../../docs/20_FUNKTIONEN.md#3-erfassen)

## Vollprüfung und Auslieferung

[Eingefrorener Quellstand](quellstand.json) mit 333 Dateien. [Vollprüfung](vollpruefung/ergebnis.json) rund 11:58–12:22, entsperrt, ohne Eingaben, `caffeinate -dims`: **Exitcode 0**, 79 Schritte, zwei plattformbedingt übersprungen; Quellstand vor und nach dem Lauf unverändert. [Lieferabgleich](auslieferung.json): 144 Dateien in `07_Python-Versionen` und 58 im Bundle per SHA-256 gleich `src/glide`, Bundle 3.33.3, `de.shaye.glide`, Signatur gültig; Showcase ausgeliefert.

## Gezielte Prüfungen

- 14 Unit-Tests für `capture_parser.py` mit festem Stichtag (Freitag, 02.10.2026), alle Unit-Tests grün.
- Neue Pflichtsuite `test_eingabe3333.py` grün; Gegenprobe mit dem ausgelieferten Stand 3.33.2 (`07_Python-Versionen`): Exitcode 1 (`_capture_hint` fehlt).
- `test_bilder330` (jetzt `/morgen` = Bearbeitungstag), `test_features311` (Schnellerfassung mit Feld „Fällig“), `test_glide`, `audit_app`, `test_datenintegritaet`, `test_features323`, `test_features329`, `test_seiten330`, `test_ui39`, `test_kontrast330` grün.
- `test_features330` scheiterte einmal, als vier Suiten parallel liefen, an einem Return in der Befehlspalette (nicht verändert); allein grün. Parallel laufende Suiten nehmen sich gegenseitig die aktive App und damit die Tastatur.
