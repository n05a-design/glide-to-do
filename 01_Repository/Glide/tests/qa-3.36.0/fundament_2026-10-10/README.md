# Fundament und Tempo – Liefernachweis 3.36.0

Stand 10.10.2026 · Glide 3.36.0 · Aufgabenformat 23 · native Abnahme offen

P03 und E01 sind lokal umgesetzt und geprüft. Die Lieferkopien tragen 3.36.0; ein vollständiger Produktionsabschluss setzt zusätzlich die native Linux-/Windows-Prüfung voraus. Ausgangsproduktion 3.35.0 aus `62ad554`, Prüfstand-Commit `38b3e13`.

| Tor | Ergebnis |
|---|---|
| Pflichtsuite `test_fundament3360` | grün im endgültigen eingefrorenen Mac-Volllauf; echte Änderungen, Undo, aktuelle Werte, Fokus/Scrollen, Host- und Dialoglebensdauer |
| Drei Gegenproben gegen 3.35.0 | passend rot: Heute-Zählung mehrfach je Aufbau, geänderte Bibliothekskarte ersetzt, wiederverwendbarer Einstellungsdialog fehlt; [Ergebnis](gegenproben-vorversion.json) |
| Kalibrierte Erwartungen | sieben positive Mac-Suiten grün, sieben passende Defektkopien rot; [Ergebnis](mac-defektgegenproben.json). Native Linux-Proben ausstehend |
| Tatsächlicher Builder/Modalweg | finale Quellfassung `04a0597…` hält D46/D47 ein; [sämtliche Rohwerte und Messverfahren](../fundament_vorher_nachher/README.md) |
| Sichtvergleich | eigene isolierte Hell-/Dunkelfenster bei 1280 × 800 und 860 × 700 mit großer Schrift geprüft; Scrollleiste korrigiert |
| Eingefrorene Mac-Vollprüfung | Exit 0, 100 ausgeführt, zwei übersprungen; 83 Integrationssuiten, 264 Unit-Tests. 835 Dateien nach Lauf unverändert; [Ergebnis](mac-voll.json) |
| Native Linux-/Windows-Vollprüfung | ausstehend am unveränderten Kandidatcommit; Menschenabnahme getrennt |
| 07 und Showcase | 38 Code-Dateien, 131 Ressourcen, sechs Showcase-Dateien SHA-256-gleich; [Hashabgleich](lieferabgleich.json) |
| macOS-Bundle | 3.36.0; 38 Code-Dateien und 45 Mac-Ressourcen bytegleich; Ad-hoc-Signatur im Bauordner und auf Rückkopie mit `codesign --verify --deep --strict` grün; [Nachweis](bundle.json) |
| Menschliche Plattform-/DPI-/Screenreader-Abnahme | getrennt offen; keine automatische Freigabe |

Der [erste Volllauf](mac-erster-volllauf.json) bleibt mit seinen drei Befunden erhalten. Korrekturen: getrennte Kalenderrahmen für Monats-/Wochenlayout, vollständige Signatur der Updatekarte, Esc-Prüfung für zurückgezogenen Einstellungsdialog einschließlich beendetem Modalzustand und freiem Griff. Der abschließende Volllauf enthält alle Korrekturen. Tageszahlen werden nur innerhalb desselben Renderdurchgangs wiederverwendet.

D46 erlaubt Startseite kalt ≤ 300 ms direkt/≤ 500 ms im beobachteten Kindprozessverfahren, warm ≤ 150 ms. D47 erlaubt Einstellungen erneut Median ≤ 150 ms/p95 ≤ 170 ms, zuerst ≤ 250 ms. Keine Funktionen entfernt. Bibliotheksstatus bei 200 Listen/10.000 Aufgaben 550 → 11 ms Median; Umordnen etwa 7 % langsamer. Auch die zwischenzeitlich rote Kaltmessung bleibt im Messnachweis.

Rohprotokolle und Fensteraufnahmen bleiben lokal außerhalb von OneDrive. Die [strenge CI-Grundstufe](ci-grundstufe.json) ist grün auf einer isolierten Git-Projektkopie ohne die externen unversionierten Skill-Dateien. Der Vendor-Originalabruf blieb lokal wegen SSL-Zertifikatsprüfung ein Hinweis; native CI wiederholt ihn. Den Arbeitsordner mit externen Skill-Dateien nicht als vollständig grün geprüft bezeichnen.

Der [erste native Kandidatlauf](native-erster-kandidat.json) auf `a7197d4` ist abgeschlossen: Grundstufe grün, Linux mit zwei Suitefehlern, Windows bereits vor Checkout wegen eines falschen Arbeitsverzeichnisses beendet. Kein Windows-App-Ergebnis. Beide Linux-Befunde betrafen Prüfabläufe: Hintergrundvorschauen wurden vor dem sichtbaren Abschnitt gezählt; der ersetzte Modalweg ließ Escape zur Hauptauswahl gelangen. Die Tests verwenden nun den wirklichen Modalweg. Genau sechs Vorschauen, unveränderte Auswahl beim Abbruch und tatsächlich übernommenes Datum bleiben verbindlich. Beide Suiten sind lokal grün, die beiden passenden Defekte rot; [Werkzeugnachlauf](mac-werkzeugnachlauf.json). App, 07 und Bundle bleiben bytegleich zum eingefrorenen Volllauf. Die [strenge lokale CI des Werkzeugnachlaufs](ci-werkzeugnachlauf.json) ist grün (bekannter SSL-Hinweis). Der nächste native Lauf prüft alle Suiten und sieben Defektgegenproben.
