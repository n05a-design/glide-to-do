# Abnahme Glide 3.33.0 – Fundament

Stand 01.10.2026 · Glide 3.33.0 · Datenformat 20

Erster Schnitt T2/P09a aus der neuen Claude-Planung, GitHub-Ausgangspunkt 569020e. Die vollständige Regression ist `vollpruefung/ergebnis.json`: Exitcode 0. 59 Integrationssuiten, acht Unit-Tests, Showcase, fünf Analysen. 311 eingefrorene Dateien unverändert; Python-Fassung (140 Dateien) und Bundle (54 Quell-/Ressourcendateien) bytegleich, Signatur gültig.

- `ablageabgleich.json`, `eingangsstand.json`, `dokumentvorsicherungen.json`, `vorsicherungen.json`: Herkunft und unveränderte Archive.
- `funktionsmessung.json`: alternierender Vergleich im selben Prozess. Die anderen ersten Serien schwanken mit Rechnerlast und sind keine allgemeine Beschleunigungsbehauptung.
- `native_isolation.json`: alter QA-Hintergrund wird im Negativtest erkannt, neuer Hintergrund besteht.
- `auslieferung.json`, `fixture_auslieferung.json`, `showcase_auslieferung.log`, `launcher_probe.json`: tatsächlicher Lieferstand und getrennter Starter.
- `anschluss_codeabgleich.json`: folgende Performance-/Featurepakete mit Codeeinstiegen und Abnahme.

Echte Nutzerdaten wurden nicht verwendet. Physische OS-Bedienung, Windows/Linux, Mehrmonitor/DPI und Screenreader bleiben offen; ad hoc signiertes Entwicklungsbundle, weiterhin installiertes Python erforderlich.
