# FP-03 Stufe 1 – erweiterte gespeicherte Ansichten

Stand 21.10.2026 · Glide 3.43.1 · Aufgabenformat 25 · Einstellungen 2 · lokaler Kandidat

Auf den abgeschlossenen FP-04-/FP-07-Stand folgt der direkte Fortsetzungsauftrag vom 21.10.2026. Zusätzliche feste Bedingungen, Alle-/Oder-Verknüpfung, gemeinsame Prüfroutinen für Treffer und Erklärung und ein aufklappbarer Bereich im bestehenden Dialog sind umgesetzt. Stufe 2 (gespeicherte Darstellung, Gruppierung, Sortierung, Spalten) gehört nicht zu diesem Schnitt. [Funktionsvertrag](../../../docs/20_FUNKTIONEN.md), [Einstellungsvertrag](../../../docs/06_DATA_BACKUP_MIGRATION.md).

## Prüfung und Grenzen

Neun gezielte App-/UI-Fälle, 812 Fachlogiktests (zusätzlich nochmals ohne Systemzeitzonen) und 152 Werkzeugtests bestanden. Sechs rote App-Adapter-Gegenproben auf dem unveränderten Vorgänger sowie eine zusätzliche rote Großschrift-Gegenprobe sichern die Neuerungen ab. 30 alte Filterkombinationen liefern dieselben Treffer wie der ausgelieferte Leser. Die CI-Grundstufe ist mit Exitcode 0 bestanden: 19 Schritte, 18 ausgeführt und 1 Hinweis. [Zusammenfassung](abschluss.json), [gezielte Ergebnisse](gezielt.json), [sechs Adapter-Gegenproben](gegenprobe.json), [Großschrift-Gegenprobe](gross_gegenprobe.json), [CI-Schrittbilanz](ci_abschluss.json), [Aufrufe des korrigierten Nachlaufs](pruefaufrufe_nachlauf.json). [Aufrufbilanz](pruefaufrufe.json), [Kandidatenmanifest](quellstand.json), [geprüfte Kandidatensicherung](kandidat_sicherung.json), [gesicherter Ausgangsstand](ausgangsmanifest.json).

Die erste gezielte Runde fand einen falsch angesprochenen eigenen Dialogbutton im Prüfwerkzeug und eine echte Überschreitung der 100-ms-Grenze für 10.000 Aufgaben. Die Regeln werden jetzt einmal je Auswertung vorbereitet; Erklärung und schnelle Trefferprüfung verwenden dieselben Prädikate. Ein Zwischenlauf mit währenddessen geänderter Quelle ist ausdrücklich keine Abnahme. Weitere Messvorläufe ersetzten im Fixture die aktive Liste und wurden durch deren Referenzabgleich beeinflusst; der finale Messaufbau ergänzt den Bestand und schreibt ihn über den bestehenden App-Einstieg. Diese Zwischenstände bleiben erhalten.

Der nachfolgende Großschrift-Test fand noch die alte erzwungene Mindestbreite von 980 Pixeln. Der Dialog begrenzt nun die Startbreite und schaltet abhängig von der Schriftgröße auf eine Spalte um. Eine neue Gegenprobe auf dem vorherigen FP-03-Stand ist rot; normaler und großer Schriftmodus gehören jetzt zur Pflichtsuite. Der vorherige Kandidatenstand und seine Sicherung bleiben getrennt erhalten.

Die Baseline und die bisherige Wissens-/Filterprüfung sind grün. Der tatsächliche ausgelieferte Leser 3.43.1 erhält den neuen obersten Namespace; eine zusätzliche Vergleichsprobe gleicht 30 alte Filterkombinationen ab. Die reine Auswertung und der App-Einstieg werden getrennt gemessen. Abbruch und Schreibfehler dürfen den vorherigen Zustand nicht verändern; unbekannte Definitionen bleiben erhalten und liefern sichtbar keine Treffer.

Keine neue Gesamtprüfung von 100 Suiten behauptet: Der [99-Suiten-Vollabschluss](../featurepakete_2026-10-19/README.md) gehört zum Vorgänger vor FP-03. Nach D51 erfolgen während dieser weiteren Umsetzung gezielte Prüfungen und CI; Versionswechsel, native Matrix und Lieferung bleiben am Phasenende. Keine neue 07-/Paketlieferung, kein Commit/Push, keine menschliche oder native Mehrplattformabnahme.

Rohlogs und lokale Orchestrierung bleiben ignoriert. Alle App-Prüfungen verwenden künstliche Daten und setzen einen temporären `GLIDE_DATA_DIR` vor dem Import.

## Abschließende Validierung

Die reine Auswertung von 10.000 künstlichen Aufgaben liegt im Median bei 23.17 ms (Grenze 100 ms); der reale App-Einstieg benötigt im Median 57.30 ms. Alle Einzelwerte stehen im gezielten Ergebnis. Normaler und großer Schriftmodus wurden mit 780 × 570 Pixeln über echte Schaltflächen geprüft; dies ersetzt keine physische DPI-/Mehrmonitorabnahme.

[Hash-, Schutzdatei- und Git-Abgleich](validierung.json), [Datei- und Abschnittslinks](dokumentverweise_abschluss.json), [Datenschutz einschließlich aller neuen Dateien](datenschutz_abschluss.json), [Momentaufnahme der gesamten Ablage](inventur_abschluss.json). 664 Eingaben sind erfasst; ein erlaubter Dokumentnachlauf wird getrennt ausgewiesen. Alle 783 geschützten Liefer-, Beispiel-, Grafik- und Fixturedateien bleiben unverändert. Der letzte 99-Suiten-Vollnachweis bleibt ein Vorgängerbeleg; die neue registrierte 100-Suiten-Matrix wurde nicht erneut ausgeführt.
