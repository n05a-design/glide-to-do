# Eisenhower 3.33.5 – Nachweis

02.10.2026 · App 3.33.5 · macOS, Python 3.14.5, Tk 9.0 · temporäres `GLIDE_DATA_DIR`, keine echten Nutzerdaten · [Vertrag 78](../../../docs/78_EISENHOWER_3.33.5.md)

## Vollprüfung und Auslieferung

[Eingefrorener Quellstand](quellstand.json) mit 338 Dateien. [Vollprüfung](vollpruefung/ergebnis.json) rund 14:01–14:27, entsperrt, ohne Eingaben: **Exitcode 0**, 80 Schritte, zwei plattformbedingt übersprungen; Quellstand unverändert. [Lieferabgleich](auslieferung.json): 145 Dateien in `07_Python-Versionen` und 59 im Bundle per SHA-256 gleich `src/glide`, Bundle 3.33.5, Signatur gültig; Showcase ausgeliefert.

## Gezielte Prüfungen

- Unit-Tests grün, davon vier neue für `eisenhower.py`.
- `test_eisenhower3335.py` grün; Gegenprobe mit dem ausgelieferten Stand 3.33.4: Exitcode 1 (kein Menüeintrag „Dringlichkeit × Wichtigkeit“).
- Nacheinander statt parallel (Tastaturfokus): `test_features330`, `test_klappmechanismen3321`, `test_workspace310`, `audit_app` grün; `test_features322` und `test_features325` fanden den nicht zugeordneten Palettenbefehl (R2), nach der Zuordnung grün.
