# Paket Tempo 3.33.19 – Mac-Vollprüfung, Lieferung und Messungen (09.10.2026)

Stand 09.10.2026 · Glide 3.33.19 · Referenz-Mac, Python 3.14.5 (python.org), Tk 9.0.3 · künstliche Daten, isolierter `GLIDE_DATA_DIR`

Paket 1 des Sprints (Entwicklungsplan §15): P06r, P04, P03r, E01, P01r, P08c. Geprüft auf einer eingefrorenen Kopie der Ablage außerhalb von OneDrive (ohne `.git`, `.claude`, `archiv`, `build`); aus derselben Kopie wurden 07, Showcase und Bundle geliefert.

| Schritt | Ergebnis |
|---|---|
| [Vollprüfung](voll/ergebnis.json) | Exitcode 0: 94 ausgeführt, 2 übersprungen (Linux-Aufnahmen, menschliche Sichtprüfung); darin `test_tempo33319` mit 77 Integrationssuiten |
| Python-Lieferung | `abgleich_07.py`: 28 Code-Dateien und 131 Ressourcen, keine Abweichung; Hauptdatei 3.33.18 ins Archiv (sieben Versionen); `app.pyw` SHA-256 `1159e8e2…` |
| Showcase | `showcase_abgleich.py` Exit 0, sechs Dateien nach `05_Probelisten_Testdaten/Showcase` |
| [Bundle](bundle.json) | `build/macos/Glide.app` 3.33.19, Ad-hoc-Signatur geprüft, 74 Dateien, alle Code- und Ressourcendateien SHA-256-gleich zu 07 |

## Messungen

Zwei Messreihen, getrennt nach Bedingung. Rohwerte in [messungen](messungen/); jede Datei nennt ihre Bedingung.

1. **Sprintmessung** (`p0*`): während der Umsetzung auf Zwischenständen des Quellbaums (Kennung im Datensatz noch 3.33.18) gegen den Lieferstand 3.33.18. Strom- und Fenstermodus wurden nicht protokolliert.
2. **Lieferstand** (`lieferstand_*`): ausgelieferte 3.33.19 und 3.33.18 aus den eingefrorenen Kopien, unmittelbar nacheinander im macOS-Hintergrundmodus und **im Akkubetrieb**. Akku und inaktiver Prozess verlangsamen Tk-lastige Schritte und streuen stärker.

| Messung (Median) | 3.33.18 | 3.33.19 | Reihe |
|---|---|---|---|
| P04 Seite mit 30 Bildern, Tippen fern von Bildern | 273 ms | 2,5 ms | Sprint |
| P04 dito | 267 ms | 3,9 ms | Lieferstand |
| P04 Tippen im Umflussbereich eines Bilds | 275 ms | 22,5 ms | Sprint |
| P04 dito | 277 ms | 43 ms (Einzelwerte 27–48 ms) | Lieferstand |
| P03r Startseite aktualisieren ohne Änderung (1.000 Aufgaben) | 517 ms | 0,2 ms | Sprint |
| P03r dito | 502 ms | 0,3 ms | Lieferstand |
| P03r Wechsel Liste → Startseite | 561 ms | 273 ms | Sprint |
| P03r dito | 543 ms | 297 ms | Lieferstand |
| P08c Abhaken bei 5.000 Punkten (`item_change`) | 62 ms | 61 ms | Sprint |
| P08c dito | 112 ms | 119 ms | Lieferstand |

- **P06r** (Zählung, bedingungsunabhängig, 200 Aufgaben): Abhaken schreibt `settings.json` einmal statt dreimal und die Sperrdatei nicht mehr dreimal; Rückgängig, Umbenennen, Archivieren, Zurückholen, Löschen und Papierkorb leeren bauen die Seitenleiste einmal statt zweimal auf, Duplizieren zweimal statt dreimal. Die Pflichtsuite zählt dieselben Wege über echte Einstiege (Gegenprobe gegen 3.33.18 rot).
- **P08c:** Das Ziel 120 ms wird in beiden Reihen erreicht, im Akkubetrieb knapp. Tempo 3.33.19 ändert den Abhakweg selbst kaum; der Unterschied zwischen den Reihen ist Bedingung, nicht Version. Ohne Bearbeitungsverlauf 103 ms (Lieferstand), 1.000 Punkte 17 ms, 10.000 Punkte 118 ms (Sprint).
- **E01:** Umbruch je Spalte statt je Beschriftung; das Fenster erscheint auf dem Referenz-Mac in etwa 560 statt 677 ms (Sprint, Einzelmessung ohne Rohdatensatz). Der Rest ist Tk-Zeichnen unter macOS (dokumentierte Grenze).
- **Nicht belegt:** ein Gewinn im Vordergrund mit Netzstrom für den Lieferstand; dafür ist eine Wiederholung am Netz nötig.

Menschliche Sicht- und Bedienabnahme (I6) bleibt offen; Rohprotokolle und Fensterfotos blieben lokal.
