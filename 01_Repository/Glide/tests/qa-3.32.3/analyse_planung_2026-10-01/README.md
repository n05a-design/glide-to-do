# Analyse-/Planungsnachlauf 3.32.3 – Nachweise

Datiert 01.10.2026 · App unverändert 3.32.3 · keine Produktionsversion

Belege zur Analyse in `00_Arbeitsvorbereitung`:
- [Bestandsaufnahme](../../../../../00_Arbeitsvorbereitung/Glide_Bestandsaufnahme_Code_und_Dokumentation_2026-10-01.md)
- [UX-Prüfung](../../../../../00_Arbeitsvorbereitung/Glide_Produktprinzipien_und_UX-Pruefung_2026-10-01.md)
- [Entwicklungsplan](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan_3.33ff_2026-10-01.md)

Zusammenfassung und Dateiliste: [`ergebnis.json`](ergebnis.json).

Alle Proben laufen mit künstlichen Daten in einem temporären `GLIDE_DATA_DIR`, der vor dem Import gesetzt wird. Fotos zeigen ausschließlich eine Xvfb-Anzeige, auf der nur Glide läuft.

## Inhalt

| Pfad | Zweck |
|---|---|
| [`messung_speicherweg/`](messung_speicherweg/) | Rohwerte des Pflegewerkzeugs [`messung_speicherweg.py`](../../../scripts/pflege/messung_speicherweg.py) für 1.000/5.000/10.000 Punkte (Python 3.14rc2) und 1.000/10.000 (Python 3.12), Profil bei 10.000 |
| [`werkzeuge/`](werkzeuge/) | Start- und Ansichtsprobe mit gemeinsamem Ladeweg (`_glide_laden.py`, Standard `src/glide/app.pyw`, `--code` für `07_Python-Versionen`) |
| [`ergebnisse/`](ergebnisse/) | Start-/Ansichtsprobe (JSON) und SHA-256 der 139 Laufzeitdateien aus `07_Python-Versionen` |
| [`bilder/`](bilder/) | Bildschirmfotos 1280 × 840 der Linux-Probe |

## Umgebung

- Linux-Container (Intel Xeon 2,1 GHz, 4 Kerne), Xvfb 1280 × 860 × 24
- Python 3.12.3 + Tk 8.6.14 aus Ubuntu (`python3-tk`, mit Xft/Fontconfig)
- Python 3.14.0rc2 + Tk 8.6.14 aus python-build-standalone (`uv python install 3.14`), **ohne Xft** – Symbole erscheinen dort als `\uXXXX`
- Kein macOS, kein Tk 9. Werte sind Trends; verbindlich bleibt die Messung auf dem Referenz-Mac.

## Aufruf

```sh
cd 01_Repository/Glide
xvfb-run -a -s "-screen 0 1280x860x24" python3 -B scripts/pflege/messung_speicherweg.py --items 10000 --profil --json <Ausgabe>
cd tests/qa-3.32.3/analyse_planung_2026-10-01/werkzeuge
xvfb-run -a -s "-screen 0 1280x860x24" python3 -B startprobe.py --bild start.png
xvfb-run -a -s "-screen 0 1280x860x24" python3 -B ansichten_probe.py --ausgabe ../bilder
```

## Ergebnisse (Median / p95, warm)

| Bestand | Python | Abhaken | `save_items` | Undo-Schnappschuss | Erstes Speichern |
|---:|---|---:|---:|---:|---:|
| 1.000 | 3.14rc2 | 55,7 / 68,5 ms | 39,3 / 48,0 ms | 9,9 / 11,7 ms | 85,7 ms |
| 5.000 | 3.14rc2 | 217,6 / 257,1 ms | 160,8 / 199,2 ms | 38,1 / 39,9 ms | 384,0 ms |
| 10.000 | 3.14rc2 | 446,0 / 502,0 ms | 355,5 / 491,2 ms | 84,4 / 105,0 ms | 843,9 ms |
| 1.000 | 3.12 | 73,3 / 100,9 ms | 55,3 / 62,8 ms | 6,5 / 8,3 ms | 106,1 ms |
| 10.000 | 3.12 | 613,3 / 721,9 ms | 487,0 / 534,7 ms | 58,7 / 71,2 ms | 1.098,6 ms |

**Profil** (10.000 Punkte, 3.14, Anteile an `save_items`):
- `update_history` ≈ 53 %
- `record_recent_list_edits` ≈ 25 %
- Dateischreibvorgänge ≈ 9 %

**Ansichtswechsel** mit Beispieldaten (3.12, Einzelmessung inkl. `update()`):
- Liste 37 ms, Startseite 348 ms, Mein Tag 77 ms, Tabelle 62 ms
- Bibliothek 148 ms, Seitenübersicht 66 ms, neue Seite 150 ms, Pinnwand 127 ms

## Grenzen

- **Künstliche Daten:** 200 Punkte je Liste, keine Bilder, Zeichnungen oder großen Seiten. Reale Bestände mit Zeichnungen erhöhen die Vergleichskosten zusätzlich.
- **Keine Vollprüfung:** Die 58 Integrationssuiten liefen nicht in dieser Umgebung. Die bestehende 3.32.3-Vollprüfung bleibt der Laufzeitnachweis.
