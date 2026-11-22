# Stadtlicht · Glide-Showcase

Stand 21.11.2026 · Glide 1.0.0 · Aufgabenformat 26 · Vorlagen 2 · [English version](en/README.md)

Eine Fotoreise durch sieben Städte: Wuppertal, Berlin, München, Wien, Monaco, Bilbao und Seoul. Zwei Wochen mit der Bahn und zwei Flügen, danach die Auswahl für ein kleines Reisebuch. Der Showcase zeigt denselben Bestand aus vielen Blickwinkeln: Reiseplan, Reiseführer mit einer Seite pro Stadt, Reisetagebuch, Galerie, Pixelstempel und drei Pinnwände.

Alle Fotos sind eigene Aufnahmen von Tim von Trostorff (shaye Design) und stehen wie der Quellcode unter der Mozilla Public License 2.0 ([LICENSE](https://github.com/n05a-design/glide-to-do/blob/main/LICENSE)); Urheber bleibt Tim von Trostorff. Der [Quellennachweis](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/tests/fixtures/showcase/quellen.json) nennt Original und Prüfsumme jeder Arbeitskopie.

## Öffnen und bearbeiten

Im Projektordner `py -3.14 05_Probelisten_Testdaten/Showcase/Showcase_starten.pyw` (Windows) oder `python3 05_Probelisten_Testdaten/Showcase/Showcase_starten.pyw` (macOS) ausführen. Der Starter lädt die App-Sicherung beim ersten Öffnen in den Ordner `Arbeitsstand-Stadtlicht`; eigene Änderungen bleiben dort gespeichert. Die Beispieldaten sind auf Freitag, den 20.11.2026, bezogen. In Heute und Kalender lässt sich dieser Tag direkt auswählen.

| Datei | Verwendung |
|---|---|
| [Glide-Showcase_App.glideapp](Glide-Showcase_App.glideapp) | Gesamtes Beispiel mit Startseite, globaler Pinnwand, Einstellungen und Reisetagebuch. Für einen separaten Datenordner. |
| [Glide-Showcase.glidebackup](Glide-Showcase.glidebackup) | Bearbeitbares Projekt über **Datei → Listen/Ordner hinzufügen …** in einen Bestand übernehmen. |
| [Glide-Showcase.glidetemplates](Glide-Showcase.glidetemplates) | Abendnotiz mit Datums- und Stadtfeld sowie die wiederkehrende Checkliste für jeden Stadtwechsel. |
| [Stadtlicht.canvas](Stadtlicht.canvas) | JSON Canvas 1.0 aus der globalen Pinnwand mit Karten, Bereich und beschrifteten Verbindungen. |
| [manifest.json](manifest.json) | Dokumente, Formatversion und SHA-256 der vier Dateien. |

## Ein Rundgang durch die Funktionen

- **Reiseführer (Buch):** Die Überblicksseite hat eine Pixelzeichnung als Titelbild, ein Seitensymbol, eine Routentabelle, ein Zitat, eine Trennlinie, Aufgaben, einen zugeklappten Block mit Packtipps und eine eingebettete Live-Liste des Reiseplans. Jede der sieben Stadtseiten trägt ihr Foto als Titelbild und im Text (rechts, links oder mittig), eine Tabelle mit Orten, Zeiten und Tipps, ein Zitat, eine Hervorhebung, einen Codeblock mit Kameradaten und Aufgaben. Die Seite **Reisekasse** zeigt eine schlichte Kostentabelle ohne Titelbild.
- **Projektpinnwand:** Vier Regionen als Bereiche (Deutschland, Österreich, Mittelmeer und Atlantik, Korea) und ein Bereich „Nach der Reise“. Die Stadtseiten sind als Karten verbunden; die Verbindungen tragen die Etappen („ICE · 3 Std.“, „Flug nach Nizza“), Flüge gestrichelt. Die **globale Pinnwand** hat einen eigenen Bereich, Linienhintergrund und vier beschriftete Verbindungen; über das Pinnwandmenü als JSON Canvas exportierbar. Der **Reiseplan** zeigt sich zusätzlich als Spaltenpinnwand nach Bearbeitungstag.
- **Reiseplan:** Überschriften, Langtext, Gruppe mit Unterpunkten, Wichtigkeit, Fälligkeit mit Uhrzeit, Bearbeitungstag und -zeit, Aufwand und erfasste Zeit, Checklisten, Abhängigkeiten, Verknüpfungen, Erwähnung der Galerie, feste Erinnerung, Anhänge und farbige Labels. Am 20.11. sind mehr Minuten eingeplant als Kapazität vorhanden ist; **Tag entlasten** schiebt Arbeit auf andere Tage.
- **Fotoroutinen** zeigen alle Wiederholungsarten, Serien am letzten Werktag und am zweiten Dienstag, Abstand nach Erledigung, begrenzte Anzahl und eine pausierte Reihe. **Vor jedem Stadtwechsel** ist eine wiederkehrende Checkliste.
- **Galerie „Stadtlicht · Auswahl“** mit 14 Fotos, Titeln und Bildunterschriften in großer Kachelgröße. Die **Abendrunde** ist eine Notiz mit Aufgaben, Anhang und Verweisen auf Aufgabe, Seite und Galerie.
- **Reisetagebuch (Notizbuch):** ein datierter Eintrag pro Stadt mit Ort, Stimmung, Leitfrage und Favoriten, dazu der Abend nach der Rückkehr.
- **Pixel-Werkstatt:** Der Reisestempel wechselt in vier Bildern die Himmelsfarbe von Morgen bis Nacht, mit PNG-Referenz, 16-Pixel-Symbol und Palette als GPL und HEX.
- Außerdem: zwei gespeicherte Ansichten (Freigaben, Eisenhower-Woche als Tabelle), angeheftete Seiten, Favoriten, Reiter, ein eigener KI-Auftrag, ein archivierter Ordner mit der ersten Route und zwei Punkte im Eingang.

## Aktualisieren

Im Verzeichnis `01_Repository/Glide` beide Sprachen erzeugen:

```
python3 -B tests/tools/showcase.py --tag 2026-11-20
python3 -B tests/tools/showcase.py --tag 2026-11-20 --sprache en
```

`python3 -B scripts/pflege/showcase_abgleich.py` prüft beide Fassungen über Import, Vorlagen, Verweise, Export und Neustart und gleicht sie nach `05_Probelisten_Testdaten/Showcase` und `…/Showcase/en` ab.
