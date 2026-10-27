# Startseite – Tagesaufgaben direkt erledigen

Stand 26.10.2026 · Glide 3.45.0 · Aufgabenformat 26 · lokaler Featurekandidat

Fortsetzungsauftrag: „weiter mit der Feature Umsetzung“. Umfang und Rest ausschließlich im [Plan §21.22](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2122-startseitenaufgaben-direkt-erledigen), Verhalten in [Funktionen](../../../docs/20_FUNKTIONEN.md). Diese Datei hält ausgeführte Nachweise; keine neue Gesamtroadmap.

## Umsetzung und Prüfung

Die Heute-Kachel zeigt die ersten fünf offenen geplanten Aufgaben in der bisherigen Planreihenfolge. Erledigte werden vor dem Begrenzen ausgesiebt. Ein eigener Kästchenknopf erledigt direkt, der Titel öffnet das Original. Nächste Aufgabe und Planung/Fälligkeit bleiben getrennt. Erledigen verwendet den bisherigen Übersichts-/Mutationsweg, eine aktuelle Besitzprüfung und stabile IDs. Schreibschutz unterbindet Erledigen und erhält Öffnen; ein alter doppelter Callback toggelt nicht zurück. Der Schreibschutzstatus gehört zur Startseitensignatur.

`home_task_tiles.py` übernimmt die Komposition beider Aufgaben-Kacheln über unveränderliche Anzeigemodelle, sechs UI-Operationen und sechs bestehende Aktionsports. Keine App-/Tk-Imports, Modellobjekte in Callbacks, eigenen Timer oder Fenster. Die bestehenden Karten/Text-/Aktions-/Retentionbausteine bleiben beim Host. `home_dashboard.planned_preview` ist lesend. Alle Funktionen des neuen Renderermoduls bleiben unter 50 Zeilen.

| Prüfung | Ausgeführtes Ergebnis |
|---|---|
| Baseline vor Produktionsänderung | Zwölf vorhandene Dashboard-Fachtests und `test_startseite3332.py` grün; temporärer `GLIDE_DATA_DIR` vor Import |
| Betroffene Fachsuiten | `test_home_dashboard.py` 14/14, `test_home_task_tiles.py` 6/6, `test_home_tiles.py` 13/13; insgesamt 33 grün |
| Erweiterte echte Startseitensuite | Fünf offene Plätze trotz sechs davor sortierter erledigter Punkte; Klick und aktuelle Datei, ein Undo/Redo, neue Objekte nach Undo, alter/doppelter Callback und Original öffnen geprüft |
| Schreibschutz und Fehler | Gescheiterte Besitzprüfung/zwischenzeitlicher Schreibschutz stoppen vor Änderung und Undo; readonly ohne Kästchen/Erledigenaktion. Hauptdateifehler bewahrt Originalbytes, offene Änderung mit einem Undo bleibt, kein Erfolgshinweis; Retry grün |
| Retention | Identische Knöpfe nach drei erzwungenen Aufbauten weiterhin dieselben Widgets; Callbackdaten stabil, keine Bindung an die kurzlebige Rendererinstanz |
| Geometrie | Vier Konfigurationen, drei Scrolllagen, 300 Knopfprüfungen grün; [Bedien-/Geometriebericht](bedienung.json) |
| Bestehende UI-Regression | [B01](b01.json): Gelesen/Seitenanfang, Scrollbewahrung, Neustart. [B02](b02.json): Rasterkante bei 1280 × 800 / 860 × 700 / 1600 × 900. [B04](b04.json): sechs Galerievorschauen, Öffnen, eigene Auswahl und fehlende Datei. Alle grün |
| Syntax / Quell- und Dokumentabgleich | Alle 88 Laufzeitdateien kompiliert, Kopierlisten geprüft; [Abschluss und SHA-256-Manifest](abschluss.json) über [Prüfskript](abschluss.py) |

Die neue Bedienprüfung ist Teil der bereits registrierten Suite `tests/integration/test_startseite3332.py`; kein unregistrierter zusätzlicher Integrationseinstieg. Die bisherigen D12-, Modell-/Scope-, Archiv-/Datums-, Erledigen-/Undo-, Rücksetz- und Designwechselprüfungen liefen im selben Aufruf weiter grün. Neue Tests verwenden künstliche Daten; echte Nutzerdaten werden nicht gelesen oder verändert.

Reproduktion aus dem Repository: `python -B -m unittest discover -s tests/unit -p test_home_dashboard.py`, entsprechend `test_home_task_tiles.py` und `test_home_tiles.py`; danach `python -B tests/integration/test_startseite3332.py`. Optional vor dem letzten Aufruf `GLIDE_HOME_ACTION_REPORT` auf den gewünschten JSON-Zielpfad und unter Windows `GLIDE_HOME_CAPTURE` auf einen Bildordner setzen. Für die drei UI-Nachläufe `python -B tests/integration/test_uiux_paket.py --fall b01` bzw. `b02`/`b04`. Der vorhandene Testharness setzt vor Appimport seinen eigenen temporären Datenordner.

## Sichtbelege und Grenzen

Vier echte Fensteraufnahmen mit künstlichen Daten gesichtet: [hell 860 × 700](screenshots/light-860x700.png), [dunkel/groß 1280 × 800](screenshots/dark-1280x800.png), [Verlauf/groß 860 × 700](screenshots/glass_light-860x700.png), [kompakt/groß 480 × 560](screenshots/light-480x560.png). Kästchen und getrennte Öffnungstitel sind erkennbar und erreichbar; untereinander liegende Kacheln bleiben im bestehenden Scrollbereich. Bilder sind lokale Sichtbelege und können nach den bestehenden Uploadregeln von Git ausgeschlossen bleiben.

Die Geometrieprüfung gilt der ruhenden Ansicht. Im ersten Vorlauf waren noch die vorhandene Erledigungsfahne und der Undo-Hinweis aktiv; sie überlagerten die Geometrieprobe. Der Harness lässt die kurzlebige Fahne nun natürlich auslaufen und schließt den Undo-Hinweis vor dem Größen-/Scrolltest. Kein Produktions-Grenzwert wurde gelockert. Die erste neue Öffnungsassertion wurde vom nicht vorhandenen `selected_id` auf die tatsächliche Baumselektion korrigiert. Diese beiden Vorläufe sind keine belegten Produktionsfehler.

Quellstand weiter 3.45.0 / Format 26. Hauptdatei 65.373 → 65.364 Zeilen; `_render_home` 1.056 → 1.005. Der erste echte Widgetbereich ist ausgelagert; `ListApp` bleibt mit 1.748 Methoden groß. 88 Laufzeitdateien, acht Unterschiede zur eingefrorenen Lieferung: `app.pyw`, `compact_mode.py`, `home_dashboard.py`, `home_task_tiles.py`, `image_conversion.py`, `image_preview.py`, `persistence.py`, `save_comparison.py`. Sechs dieser Dateien waren bereits im vorherigen Technikpaket abweichend; dessen Nachweise bleiben an ihre damaligen Bytes gebunden. Zusätzlich sind jetzt `home_dashboard.py` und `home_task_tiles.py` abweichend, und `app.pyw` ist weiterentwickelt. Kein Versionswechsel, Vollmatrix, 07-/Paketabgleich, Commit/Push/Merge oder öffentliche Freigabe. Native Menschen-/Reader-/DPI-/Mehrmonitor-/Macabnahme und Linux-/Tk-9.1-Kompaktursache bleiben getrennt offen.
