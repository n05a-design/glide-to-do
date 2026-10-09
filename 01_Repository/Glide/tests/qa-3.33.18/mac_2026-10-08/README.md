# Mac-Vollprüfung und Bundle 3.33.18 (08./09.10.2026)

Stand 09.10.2026 · Glide 3.33.18 · Referenz-Mac, Python 3.14.5 (python.org), Tk 9.0.3 · künstliche Daten, isolierter `GLIDE_DATA_DIR`

Erste native Mac-Vollprüfung seit 3.33.6 (PR01, Entwicklungsplan §15). Beide Läufe liefen auf einer eingefrorenen Kopie der Ablage außerhalb von OneDrive; die Kopie hält den Quellstand fest. Der App-Code ist in beiden Läufen bytegleich zu `07_Python-Versionen` (`app.pyw` SHA-256 `1f2cdbe6…`).

| Lauf | Inhalt | Ergebnis |
|---|---|---|
| [basis](basis/ergebnis.json) | unveränderter Stand 3.33.18 mit seinen Prüfwerkzeugen | Exitcode 1: 89 ausgeführt, 4 fehlgeschlagen, 2 übersprungen |
| [voll](voll/ergebnis.json) | App 3.33.18 unverändert, Prüfwerkzeuge mit den Korrekturen unten | Exitcode 0: 93 ausgeführt, 2 übersprungen (Linux-Aufnahmen, menschliche Sichtprüfung) |

Ursachen der vier roten Schritte im Basislauf, jeweils nachgestellt und belegt; keiner liegt im App-Code:

1. **Fachlogik-Unit-Tests:** `ablage_kuerzen.py` prüfte Verknüpfungen auch oberhalb der Ablage; unter macOS ist `/var` eine Verknüpfung (W10, behoben, zwei Gegenproben ergänzt).
2. **test_release37:** Die echte Mausposition über dem Prüffenster öffnete den Hinweis der Pinnwand-Vorschau, der den geprüften Heatmap-Hinweis nach der Ein-Hinweis-Regel schloss. Die Suite legt fremde Hinweise während der Prüfung still.
3. **test_tagpaket33314:** Im macOS-Hintergrundmodus hat die deaktivierte Prüf-App nach einem nativen modalen Dialog kein Schlüsselfenster und damit keinen Tk-Fokus; die folgenden Tastaturprüfungen liefen deshalb nie. Der echte Dialog steht jetzt am Ende der Suite.
4. **standpruefung:** Artefakt der Kopie ohne `.git`: ein Claude-Worktree unter `.claude/` wurde als Projektdokument gelesen. Kopien schließen `.claude/` seitdem aus; auf der bereinigten Kopie Exitcode 0.

Bundle: [bundle.json](bundle.json) – `build/macos/Glide.app` 3.33.18, Ad-hoc-Signatur geprüft, 73 Dateien SHA-256-gleich zu `07_Python-Versionen`. Menschliche Sicht- und Bedienabnahme (I6) bleibt offen; Rohprotokolle und Fensterfotos blieben lokal.
