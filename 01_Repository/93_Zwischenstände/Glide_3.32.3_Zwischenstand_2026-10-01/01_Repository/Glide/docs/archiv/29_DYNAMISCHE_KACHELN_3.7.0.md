# Dynamische Ordner- und Listenkacheln

Stand 12.09.2026 · unveröffentlichter Entwicklungsstand 3.7.0

## Verhalten

Die Bestandsübersicht passt jede Kachel an ihren Inhalt an. Je nach verfügbarer
Breite werden ein bis drei Spalten unabhängig untereinander gestapelt.
Die zusätzliche erste Zeile „LISTE“ beziehungsweise „ORDNER“ entfällt.
Öffnen und Bearbeiten bleiben ausdrücklich beschriftet und per Tastatur erreichbar.

Alle Kacheln erhalten 16 Pixel Innenabstand an jeder Seite. Zwischen benachbarten
Kacheln liegen 12 Pixel. Lange Titel und Vorschauen umbrechen; die beiden Aktionen
wechseln bei Platzmangel in zwei Zeilen. Es gibt keine feste Kachelhöhe und keine
Auffüllung auf die Höhe einer Nachbarkachel. Der letzte Stapel kann kürzer sein.

Die Einträge werden in der bisherigen Seitenleistenreihenfolge zyklisch auf die
Spalten verteilt. Das hält die Zuordnung während Textumbrüchen stabil. Die Spalten
haben keine künstlichen Zwischenräume innerhalb ihres Stapels; eine globale
Umsortierung nach der jeweils kürzesten Spalte findet nicht statt.

Die leere Übersicht zeigt ihren Hinweis über die gesamte Inhaltsbreite. Die
unteren Aktionen zum Anlegen und Importieren bleiben außerhalb des Scrollbereichs.

## Umsetzung und Grenzen

Die Änderung ist auf `ListApp.refresh_library_page()` begrenzt. Die bestehenden
`RoundedContainer` und `ButtonFlow` bleiben gemeinsame Bausteine; separate
Spaltenrahmen lösen das zuvor zeilenweise gestreckte Raster ab. Buttonbreiten
berücksichtigen die tatsächliche Schrift. Fokussierte Aktionen werden bei Bedarf
in den sichtbaren Canvas-Ausschnitt gescrollt.

Datenmodell, Versionen und Speicherformat bleiben unverändert. Die Darstellung
ändert keine Listen, Ordner, Labels, Aufgaben, Anhänge oder deren Reihenfolge.
Der zuvor abgeschlossene [Vorlagen-/Mac-Nachtrag](26_MAC_VORLAGEN_UND_ABLAGE_3.7.0.md)
ist im selben Quellstand enthalten; der Mac-Dropdownersatz bleibt auf macOS begrenzt.

## Prüfung

Die Geometrieprüfung in `tests/integration/test_ui_followup36.py` deckt beide
Themes, ein bis drei Spalten, kleine/mittlere/große UI-Schrift, lange Titel,
Vorschauen, Labels, leere Listen/Ordner, eine vollständig leere Übersicht sowie
Fokus-Scrollen ab. Sie prüft Kartenränder, gleiche Abstände, fehlende Überlappungen,
vollständige Aktionen und unveränderte Daten einschließlich Öffnen/Rückkehr/Neustart.

Tk aktualisiert eingebettete Frames außerhalb des sichtbaren Ausschnitts erst
beim Sichtbarwerden. Deshalb scrollt die Prüfung jede Karte vor der Prüfung ihrer
inneren Geometrie ins Sichtfeld. Die endgültigen Stapelpositionen werden danach
gemeinsam geprüft. Eine native Sichtabnahme und eine Ausführung unter Windows
werden dadurch nicht ersetzt. Der aktuelle Laufstatus steht im
[QA-Bericht](../07_QA_BERICHT.md).
