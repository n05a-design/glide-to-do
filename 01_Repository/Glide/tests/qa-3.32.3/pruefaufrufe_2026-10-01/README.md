# Wiederholte Prüfaufrufe 3.32.3 – Nachweise

Datiert 01.10.2026 · App unverändert 3.32.3 · keine Produktionsversion

Anlass ist die Frage des Inhabers, ob Bestandteile wie die Schriftart nur einmal beim Start geprüft werden können. Auswertung und Vorschlag P09: [Bestandsaufnahme T8](../../../../../00_Arbeitsvorbereitung/Glide_Bestandsaufnahme_Code_und_Dokumentation_2026-10-01.md#t8--wiederholte-prüfungen-und-messungen-je-bedienschritt-neu-gemessen). Zusammenfassung und Dateiliste: [`ergebnis.json`](ergebnis.json).

Alle Proben laufen mit künstlichen Daten in einem temporären `GLIDE_DATA_DIR`, der vor dem Import gesetzt wird. Sie nutzen den Ladeweg [`_glide_laden.py`](../analyse_planung_2026-10-01/werkzeuge/_glide_laden.py) der Analyse vom selben Tag.

## Inhalt

| Pfad | Zweck |
|---|---|
| [`werkzeuge/pruefaufrufe_probe.py`](werkzeuge/pruefaufrufe_probe.py) | Aufrufe je Schritt zählen (cProfile) und je fünf warme Läufe ohne Profiler messen; Variante `basis` oder `einmal` |
| [`werkzeuge/pixelschrift_probe.py`](werkzeuge/pixelschrift_probe.py) | Tk-Abfragen nach „Pixelify Sans“ im Pixel-Design zählen (W3) |
| [`ergebnisse/`](ergebnisse/) | Rohwerte je Variante und Bestand, Pixelschrift mit und ohne Xft |

**Variante `einmal`:**
- Ersetzt im laufenden Messprozess vier Stellen durch ihre einmal berechnete Fassung:
  - W1: keine Zeilenmessung in der Tabellenansicht,
  - W2: Zeilenhöhe je Schrift,
  - W4: Kennzahlen je Aktualisierung,
  - W5: Datum je Zeichenkette.
- Der Quellcode bleibt unverändert. Die Variante belegt nur die Größenordnung.
- Kontrolle: Die Kennzahlen der Liste sind in beiden Varianten gleich; es gibt keine Callbackfehler.

## Umgebung

- Linux-Container, Xvfb 1280 × 860 × 24
- Python 3.12.3 + Tk 8.6.14 (Ubuntu, mit Xft)
- Für W3 zusätzlich Python 3.14.0rc2 + Tk 8.6.14 ohne Xft
- Kein macOS, kein Tk 9. Werte sind Trends; verbindlich bleibt die Messung auf dem Referenz-Mac.

## Aufruf

```sh
cd 01_Repository/Glide/tests/qa-3.32.3/pruefaufrufe_2026-10-01/werkzeuge
xvfb-run -a -s "-screen 0 1280x860x24" python3 -B pruefaufrufe_probe.py --punkte 1000 --variante basis  --json ../ergebnisse/basis_1000_py3.12.json
xvfb-run -a -s "-screen 0 1280x860x24" python3 -B pruefaufrufe_probe.py --punkte 1000 --variante einmal --json ../ergebnisse/einmal_1000_py3.12.json
xvfb-run -a -s "-screen 0 1280x860x24" python3 -B pixelschrift_probe.py --json ../ergebnisse/pixelschrift_py3.12.json
```

## Ergebnisse (Median von fünf warmen Läufen, Python 3.12)

| Schritt | 1.000 heute | 1.000 einmal | 5.000 heute | 5.000 einmal |
|---|---:|---:|---:|---:|
| Tabellenansicht öffnen | 558 ms | **69 ms** | 2.671 ms | **292 ms** |
| Listenansicht öffnen | 79 ms | 87 ms | 418 ms | **260 ms** |
| Liste öffnen und abhaken | 234 ms | 208 ms | 860 ms | 799 ms |
| Startseite | 251 ms | 254 ms | 315 ms | 340 ms |
| Mein Tag | 131 ms | 137 ms | 1.391 ms | 1.549 ms |

**Aufrufzahlen** (je ein profilierter Lauf):
- **Tabelle:**
  - 1.025 bzw. 5.025 `font.measure` heute, 23 in der Variante.
  - `content_column_widths` misst Titel und Typ jeder Zeile; das Ergebnis verwirft `sync_task_tree_columns`.
- **Listenaufbau:** 4 × `page_chips`, 5 × `due_status` je Punkt, 10.002 `strptime` bei 5.000 Punkten; in der Variante 1 × `page_chips` und 1.667 `strptime`.
- **Schrift:**
  - 1 × `tkfont.families` je Sitzung; `ui_font_family` ohne Tk-Aufruf aus dem Zwischenspeicher.
  - Je Ansichtswechsel 13–21 neue `tkfont.Font` mit 12–19 `metrics`-Abfragen, überwiegend aus `hint_line_height` (8–12 Aufrufe je Wechsel).
- **Pixelschrift (W3):**
  - Mit Xft gefunden, danach keine weitere Abfrage.
  - Ohne Xft 20 Abfragen beim ersten und 10 beim zweiten Startseitenaufbau.

## Grenzen

- **Künstliche Daten:** eine Liste mit 1.000 bzw. 5.000 Punkten, keine Bilder oder Zeichnungen.
- **Einzelne Ansichten:** Startseite und Mein Tag schwanken um ±10 %. Die Unterschiede dort liegen im Rauschen.
- **Keine Vollprüfung:** Die 58 Integrationssuiten liefen nicht in dieser Umgebung.
