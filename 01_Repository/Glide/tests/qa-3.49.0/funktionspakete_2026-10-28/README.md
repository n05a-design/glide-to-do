# Drei funktionale Pakete weitergeführt

Stand 28.10.2026 · Glide 3.49.0 · Aufgabenformat 26 · lokaler Quellkandidat

Der korrigierte Nutzerauftrag meint die Funktionspakete aus Plan §21.26. Deren erste Ausbaustufe ist bereits im Quellstand enthalten. Diese Runde ergänzt sichtbaren Funktionsumfang in denselben Bereichen; die vorherige Robustheitsrunde ersetzt ihn nicht.

| Paket | Zusätzliche Bedienung | Erhaltene Verträge |
|---|---|---|
| Tagesnavigation | Woche in der Tageskachel: betrachtete/vorige/nächste Woche, Wochentag und eindeutiges Datum, Suchauswahl | Flüchtig, readonly möglich, Tagwechsel leert Tagesauswahl, alte Menüs wirkungslos, keine Datenmutation |
| Mehrfachbearbeitung | Fälligkeit setzen/entfernen; Aufwand je Aufgabe über Vorgabe/eigene Dauer/Entfernen | Bearbeitungstag bleibt; Uhrzeit nur beim Entfernen einer Fälligkeit löschen; Serien-Fälligkeit einzeln; ein Undo/Redo, kein Erfolg bei Schreibfehler |
| Verweise | Kopieren, bewusstes Hauptöffnen und Verknüpfen des sichtbaren Inhalts/der Aufgabe über bestehenden Dialog | Kopieren ohne Mutation; readonly/Archiv geschützt; ein Undo/Redo beim Verknüpfen, IDs nach Snapshot und Kontext nach Dialog erneut prüfen |

Neue Regeln liegen in vorhandenen Tk-freien Modulen. Keine neue Abhängigkeit, Datenart, Format- oder Zwischenversion. Vorhandene 3.48.0/3.49.0-Änderungen einschließlich Schutzfunktionen bleiben erhalten.

## Prüfung

- Baseline: 14 bestehende Dreipaket-Fachfälle und sieben Rendererfälle grün.
- Zwölf neue Tk-freie Fachfälle, alle 1060 Fachtests einmal grün; neun Neuerungskatalogfälle nach Textpflege gezielt grün.
- Neue echte Bedienfälle: Wochenwahl, Mehrfach-Fälligkeit/Aufwand und Verweisaktionen; Auswahl-/Datei-/Dialogwechsel, Abbruch, Undo/Redo, readonly, Serien und Schreibfehler.
- Alte Tagesnavigation, Wichtigkeit/Labels und Verweisnavigation gezielt als Regression. Maschinenlesende Einzelberichte und Abschluss in diesem Ordner.
- 384 Knopfprüfungen, vier Größen-/Schrift-/Designkonfigurationen einschließlich 480×560 Kompaktmodus und drei Scrolllagen; Nebenansicht bei 280px. Sieben eigene künstliche Fensteraufnahmen lokal. Status der Sichtung in ergebnis.json.

Ein neuer Prüfer-Vorlauf verwendete irrtümlich eine nicht vorhandene Testhilfsmethode get_list; nach Umstellung auf frische IDs grün. Eine isolierte alte Task-Editing-Suite benötigte explizites PYTHONPATH und bestand danach elf Fälle. Diese Vorläufe sind keine Produktdefekte. Geänderte Übergabezeilen mit mehrfach falsch dekodierten Umlauten wurden nach Eingangs-Hashaufnahme verlustfrei nach UTF-8 berichtigt (kodierung.json).

## Abschlussgrenzen

Kein neuer vollständiger 105-Suiten-/Last-/Native-/Reader-/DPI-/Menschenabschluss oder neuer Gesamt-CI-Lauf aus diesem Funktionsnachlauf. WA-41A/B bleiben ungeklärte Ursachen-/Freigabetore. Startbare Python-/Showcase-Lieferung bleibt 3.47.0, native Pakete 3.45.0. Kein Commit/Push. Vorherige Belege bleiben ihrer damaligen Quelle zugeordnet.
