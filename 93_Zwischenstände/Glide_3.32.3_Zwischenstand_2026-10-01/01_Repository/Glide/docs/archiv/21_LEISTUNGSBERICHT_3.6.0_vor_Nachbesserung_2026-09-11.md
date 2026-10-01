# Leistungsbericht – Glide 3.6.0

Messung: 06.09.2026 · Rohdaten: [leistung.json](../tests/qa-3.6.0/abschluss/leistung.json)

## Aussage

Auf diesem Windows-Rechner lag der Median einer vollständigen Neudarstellung
einer flachen Liste mit 5.000 Aufgaben bei 137,26 ms ohne bzw. 144,73 ms mit
Materialoptik. Bei 1.000 Aufgaben waren es 26,65 bzw. 29,67 ms. Der gemessene
Aufbau einer neuen App-Instanz dauerte 1.193,04 ms. Diese Werte beschreiben
eine lokale synthetische Messung, keine garantierten Antwortzeiten.

Die Materialoptik zeigte in diesem kleinen Versuch keinen erkennbaren
zusätzlichen Engpass. Reihenfolge, Dateicache, Windows-Auslastung und nur drei
Wiederholungen beeinflussen den Vergleich; einzelne Werte sind deshalb keine
Geschwindigkeitszusage.

## Umgebung und Methode

- Windows 11, Build 26200; Python 3.12.7; Tk 8.6.13.
- Tk-Skalierung 1,333989824; tatsächlich verwendete UI-Schrift DejaVu Sans.
- Vollständig temporärer Datenordner, keine echten Nutzdaten.
- Synthetische flache Aufgaben ohne Anhänge, drei Neudarstellungen je Szenario.
- `refresh_tree` einschließlich ausstehender UI-Aktualisierung wird gemessen.
- Speichern je Szenario einmal; enthalten ist der aktuelle lokale Speicherweg.
- Erster App-Aufbau einmal; kein Kaltstartvergleich nach Rechnerneustart.

## Ergebnisse

| Aufgaben | Materialoptik | Neudarstellung Median | Einzelmessungen | Speichern |
|---:|---|---:|---|---:|
| 100 | aus | 28,33 ms | 28,33 / 21,68 / 28,54 ms | 53,87 ms |
| 100 | an | 8,39 ms | 6,98 / 8,39 / 9,79 ms | 31,80 ms |
| 1.000 | aus | 26,65 ms | 30,50 / 23,63 / 26,65 ms | 81,43 ms |
| 1.000 | an | 29,67 ms | 35,86 / 29,67 / 26,66 ms | 69,34 ms |
| 5.000 | aus | 137,26 ms | 130,08 / 151,86 / 137,26 ms | 256,21 ms |
| 5.000 | an | 144,73 ms | 200,02 / 144,73 / 121,69 ms | 243,82 ms |

## Was sich daraus ableiten lässt

Die Liste wird weiterhin mit ttk.Treeview aufgebaut. Die Materialoptik erzeugt
keine fortlaufenden Desktopaufnahmen und keine Blur-Berechnung pro Bild. Für
die hier getesteten Größen bleibt die Neudarstellung unter 150 ms. Bei größeren
Beständen ist der komplette Neuaufbau der Liste ein sinnvolleres
Optimierungsziel als das Entfernen statischer Konturen. Erst ein Profil mit
realen Arbeitsbeständen kann Prioritäten für inkrementelles Rendern oder
Virtualisierung begründen.

## Grenzen

Nicht gemessen wurden RAM-Spitzen, CPU über Stunden, Akkubelastung, echtes
Desktop-Acrylic, Netzlaufwerke, OneDrive-Latenz, 100 Ebenen tiefe Bäume, viele
Long-Tasks, große Dateianhänge und Mehrmonitorwechsel. Dieser Bericht enthält
keine Behauptung über FPS, einen Frameworkvergleich oder eine Beschleunigung
gegenüber 3.5.0. Dafür fehlt ein identischer Vergleichslauf.

## Reproduzieren

```powershell
C:\Python312\python.exe tests/tools/leistungspruefung.py --ziel tests/qa-3.6.0/abschluss/leistung.json
```

Das Werkzeug setzt seine eigene temporäre Ablage vor dem App-Import. Ein neuer
Lauf überschreibt die Zieldatei; den Bericht anschließend anhand dieser Rohdaten
neu berechnen, statt die Zahlen aus diesem Text unverändert weiterzuverwenden.
