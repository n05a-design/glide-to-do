# Entscheidungen und Umsetzungsstand 3.26.0

Stand 20.09.2026 · App-Version 3.26.0 · Datenformat 17 · in Arbeit

Der Entwicklungsauftrag ist fachliche Referenz. Ausgeführt wird der ausdrückliche Nutzerauftrag, fehlende Änderungen umzusetzen und vorhandene zu überprüfen. Die alten Screenshots und frühere Agentenaussagen sind keine Nachweise für den aktuellen Quellstand.

## Festlegungen

- Bestehende Daten, Funktionen und persönliche Einstellungen bleiben erhalten; Tests verwenden ausschließlich GLIDE_DATA_DIR in temporären Ordnern.
- „Auto“ ist im bestehenden Produkt automatisches Anheften neuer Punkte, keine automatische Kartengröße. Die Funktion bleibt erhalten und heißt Auto anheften. Die abweichende Beschreibung im Auftrag wird nicht als Anlass verwendet, die bestehende Funktion umzudeuten.
- Lasso: vollständige Einschließung; mit Strg/Cmd ergänzend. Ein leerer Klick hebt die Auswahl auf.
- Ausrichtung an anderen Karten ist optional und zunächst aus. Toleranz sechs Canvas-Pixel, Alt unterdrückt sie während des Ziehens. Das bestehende Raster bleibt separat schaltbar.
- Sehr große Pinnwandvorschauen sind ausdrücklich als verdichtete Übersicht gekennzeichnet. Sie zeigen höchstens 40 Karten; Gesamtzahl und tatsächliche Anzahl der dargestellten Karten werden genannt. Koordinaten werden dadurch nicht verändert.
- Verlauf wird im Bestand gespeichert und auf 15 Einträge beziehungsweise 15 Tage begrenzt. Die erste Schema-17-Speicherung sichert die Originaldatei vor der Übernahme.
- Die Listenart kann zwischen Aufgaben und Notiz wechseln. Notizinhalt bleibt beim Zurückschalten erhalten. Rich Text verwendet Standard-Tk, keinen HTML-Renderer und keine neue Laufzeitabhängigkeit.
- Gerichtete Aufgabenabhängigkeiten, Reisen von Pinnwänden und dauerhaft benannte Bereiche bleiben offene Produktentscheidungen. Verbindungsrichtungen stellen keine Aufgabenabhängigkeit dar.
- Kein Big-Bang-Umbau auf ttk oder ein neues Ereignissystem. PanedWindow, Navigator und weitere Architekturänderungen werden nach Nutzen und Prüfbarkeit bewertet.

## Nachgewiesener Zwischenstand

Neue Regressionen in tests/integration/test_features326.py prüfen Vorschaugeometrie mit 205 Karten, unveränderte gespeicherte Positionen, Verbindungsstil bei Mehrfachauswahl, Ordnergrenzen auch gegen fehlerhafte Dialogdaten, Lasso, optionale Ausrichtungseinstellung, Akzente, Notizformatierung/Undo/Redo, Speicher- und Duplikatrundlauf, bytegenaue Migrationssicherung und Verlaufsgrenzen. Die Attributprüfung meldet derzeit keine Befunde.

## Noch nicht vollständig abgenommen

Zoom auf allen Elementen und allen sechs Stufen; vollständiges FieldPairGrid in der Punktmaske; Mini-Map-Bewertung; sämtliche Notizformate, Vorlagen, Exporte und fehlgeschlagene Schreibvorgänge; Verlauf für Import/Export/Backup-Aktionen; vollständiger Dopamin-Abgleich; Kommentarbereinigung und Dokumentationsabgleich; Handbuch-Druck/Export; Produkt-, Lizenz-, Branding- und Signierungsunterlagen; Release-Dateien; vollständiger QA-Abschluss und Sichtprüfung.

Diese Liste wird erst nach tatsächlicher Umsetzung und Prüfung reduziert. Eine bestandene Teilprüfung ist keine Freigabe der Gesamtversion.
