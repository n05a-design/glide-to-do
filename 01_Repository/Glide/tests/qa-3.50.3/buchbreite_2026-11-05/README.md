# Buchbreite – menschlicher Nachtest 3.50.3

Stand 05.11.2026 · Glide 3.50.3 · Aufgabenformat 26

Direkte Rückmeldung: Nachtestpunkte 4 (Tabelle) und 5 (Labels) „ist sehr gut“, Punkt 6 (Buch) bis auf ungenutzte Breite beinahe perfekt. Ergänzung: auch bei schmaler beziehungsweise ausgeblendeter Seitenleiste prüfen. Eingangsbild lokal unverändert gesichert; SHA-256 und genaue Quellstände im [Ergebnis](ergebnis.json). Die menschlichen Teilfreigaben gehören weiterhin zum ursprünglichen Windows-Kandidaten; Buchbreite nach der Korrektur noch nicht menschlich bestätigt.

## Ursache und Änderung

`fit_library_columns` zog unabhängig vom Design vier Pixel Rahmenbreite ab. `App.Treeview` hat keinen Rahmen; Karteninnenabstände sind bereits durch das Packlayout berücksichtigt. Dadurch belegten die Buchspalten bei Mindestbreite nur 504 von 508 Pixeln. Der Abzug entfällt. Nur die verfügbare Baumfläche wird vollständig genutzt; äußere Abstände und Metadatenprioritäten bleiben erhalten.

## Prüfung

- Bestehender Fall `menschen3503` vor der Änderung grün.
- Neuer Pflichtfall `buchbreite3503` im normalen Arbeitsmodi-Register, damit auch im vollständigen UI-Nachlauf enthalten. Unveränderte Vorfassung `ed3fd6dd…` scheitert gezielt mit 504/508 Pixeln.
- Auf Quelle `449f8aec…` **64 Breitenprüfungen grün**: 860/1280 Pixel, volle/schmale/ausgeblendete Seitenleiste samt Rückwechsel, Hell/Dunkel/Glas und mittlere/große Schrift. Jeweils direkter Layoutwechsel im geöffneten Buch sowie erneutes Öffnen aus Labels. Spaltensumme und tatsächliche rechte Zellenkante müssen die ganze Baumfläche erreichen; leere Beschreibung und ungenutzte Aktionsreserve bleiben ausgeschlossen.
- Bestehende Fälle `menschen3503`, `werkzeugzeile` und UI-/UX-Fall `b11` grün. Syntax grün; Python-Lieferung mit 92 Code-Dateien und 171 Ressourcen bytegleich.
- Windows / Python 3.14.7 / bestehende eigene Tcl/Tk 9.1.0, ausschließlich synthetische Testablagen.

## Lieferung und Grenzen

Die korrigierte Python-Fassung ist abgeglichen und als eingefrorener lokaler Nachtest mit eigener Kopie des regulär geschlossenen synthetischen Abnahmebestands geöffnet. „Wissen und Bildmaterial“ sichtbar. Lokaler Starter und Rohbelege unter `%USERPROFILE%/gq/b3503/`; bisheriger Bestand und eigenständige EXE unverändert erhalten.

**Offen:** menschlicher Breiten-Nachtest, neuer eigenständiger Windows-Paketbau, Mac-/Linux-Matrix und übrige Abnahmeblöcke. Die frühere strenge Grundstufe 19/19 gehört zu `ed3fd6dd…` und ist durch diese gezielten Nachprüfungen nicht erneuert. Keine neue Version, kein Commit/Push/Release.
