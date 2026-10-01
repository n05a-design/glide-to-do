# Analyse 01.10.2026 – Werkzeuge, Messungen, Bilder

Belege zur [Bestandsaufnahme](../Glide_Bestandsaufnahme_Code_und_Dokumentation_2026-10-01.md) und [UX-Prüfung](../Glide_Produktprinzipien_und_UX-Pruefung_2026-10-01.md). Alle Proben laufen mit **künstlichen Daten in einem temporären `GLIDE_DATA_DIR`**, der vor dem Import gesetzt wird. Echte Nutzerdaten werden nie gelesen. Fotos zeigen ausschließlich eine Xvfb-Anzeige, auf der nur Glide läuft.

## Inhalt

| Pfad | Zweck |
|---|---|
| [`werkzeuge/_glide_laden.py`](werkzeuge/_glide_laden.py) | Gemeinsamer Ladeweg: Isolierung, Laden der Hauptdatei aus `07_Python-Versionen` als Modul, kein Bytecode im Laufzeitordner |
| [`werkzeuge/startprobe.py`](werkzeuge/startprobe.py) | Start, Aufbauzeit, Widgetzahl, Fehlerprotokoll, optional Foto |
| [`werkzeuge/ansichten_probe.py`](werkzeuge/ansichten_probe.py) | Beispieldaten + Vorlagen anlegen, Hauptansichten wechseln, Zeiten messen, Fotos |
| [`werkzeuge/persistenz_messung.py`](werkzeuge/persistenz_messung.py) | Speicherweg bei 1.000/5.000/10.000 Punkten, optional cProfile |
| [`ergebnisse/`](ergebnisse/) | Rohdaten (JSON), Profil, SHA-256 der 139 Laufzeitdateien |
| [`bilder/`](bilder/) | Bildschirmfotos 1280 × 840 |

## Umgebung der Messungen vom 01.10.2026

- Linux-Container (Intel Xeon 2,1 GHz, 4 Kerne), Xvfb 1280 × 860 × 24.
- **Python 3.12.3 + Tk 8.6.14** aus Ubuntu (`python3-tk`, mit Xft/Fontconfig).
- **Python 3.14.0rc2 + Tk 8.6.14** aus python-build-standalone (`uv python install 3.14`), **ohne Xft** – Symbole erscheinen dort als `\uXXXX`.
- Kein macOS, kein Tk 9. Ergebnisse sind Trends; verbindlich bleibt die Messung auf dem Referenz-Mac.

## Aufruf

```sh
# Voraussetzungen (Linux): Xvfb, ImageMagick (import), Python mit tkinter
cd 00_Arbeitsvorbereitung/Analyse_2026-10-01/werkzeuge
xvfb-run -a -s "-screen 0 1280x860x24" python3 -B startprobe.py --bild ../bilder/start.png
xvfb-run -a -s "-screen 0 1280x860x24" python3 -B ansichten_probe.py --ausgabe ../bilder
xvfb-run -a -s "-screen 0 1280x860x24" python3 -B persistenz_messung.py --punkte 10000 --profil
```

Unter macOS ohne `xvfb-run` direkt starten; Fenster erscheinen dann sichtbar. Für Fotos dort `screencapture -l <Fensternummer>` statt `import` verwenden (Regel: nur eigenes Fenster).

## Ergebnisse (Median, warm)

| Bestand | Python | Abhaken (`item_change`) | `save_items` | Undo-Schnappschuss | JSON eingerückt / kompakt | Erstes Speichern |
|---:|---|---:|---:|---:|---:|---:|
| 1.000 | 3.14rc2 | 55,7 ms | 37,1 ms | 8,1 ms | 2,5 / 2,6 ms | 88,3 ms |
| 5.000 | 3.14rc2 | 231,9 ms | 178,5 ms | 38,2 ms | 14,4 / 13,7 ms | 456,1 ms |
| 10.000 | 3.14rc2 | 457,6 ms | 356,5 ms | 82,8 ms | 29,2 / 26,5 ms | 1.017,5 ms |
| 1.000 | 3.12 | 80,3 ms | 51,6 ms | 5,7 ms | 14,9 / 3,8 ms | 117,6 ms |
| 10.000 | 3.12 | 685,0 ms | 550,2 ms | 56,8 ms | 153,2 / 35,0 ms | 1.188,2 ms |

Profil (3 × Abhaken, 10.000 Punkte, 3.14): [`profil_abhaken_py3.14rc2_10000.txt`](ergebnisse/profil_abhaken_py3.14rc2_10000.txt). Anteile an `save_items`:
- `update_history` ≈ 51 %
- `record_recent_list_edits` ≈ 28 %
- Dateischreibvorgänge ≈ 8 %

Ansichtswechsel mit Beispieldaten (3.12, eine Messung inkl. `update()`):
- Liste 37 ms, Startseite 348 ms, Mein Tag 77 ms, Tabelle 62 ms
- Bibliothek 148 ms, Seitenübersicht 66 ms, neue Seite 150 ms, Pinnwand 127 ms

## Grenzen

- Künstliche Daten: 200 Punkte je Liste, keine Bilder, Zeichnungen oder großen Seiten. Reale Bestände mit Zeichnungen erhöhen die Kosten von Verlauf und Signaturen zusätzlich (SHA-256 je Zeichnung bei jedem Speichern).
- Wenige Wiederholungen (7 bzw. 5), kein p95. Für Abnahmen den Messablauf aus der Übergabe §6 verwenden.
- Die Proben ersetzen weder die 58 Integrationssuiten noch Bedienproben.

## Prüfsumme des Laufzeitstands

[`ergebnisse/sha256_07_Laufzeitdateien.txt`](ergebnisse/sha256_07_Laufzeitdateien.txt) enthält SHA-256 der 139 Laufzeitdateien aus `07_Python-Versionen` (ohne `README.md` und `Archiv/`). Prüfen:

```sh
cd 07_Python-Versionen && sha256sum -c ../00_Arbeitsvorbereitung/Analyse_2026-10-01/ergebnisse/sha256_07_Laufzeitdateien.txt
```
