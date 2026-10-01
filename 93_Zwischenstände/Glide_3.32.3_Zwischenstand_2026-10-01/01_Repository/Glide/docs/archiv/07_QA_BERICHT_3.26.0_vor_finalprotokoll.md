# QA-Bericht – Glide 3.26.0

Stand 21.09.2026 · App 3.26.0 · Datenformat 17 · Windows, Python 3.13.15

## Prüfstand

Die Nachbesserung ist implementiert; der abschließende Gesamtlauf steht noch aus. Dieser Bericht wird nach dem tatsächlichen Ergebnis ergänzt. Einzelne bestandene Tests ersetzen keine Gesamtfreigabe.

- [Ausgangslauf vor der Nachbesserung](../tests/qa-3.26.0/vor_umsetzung_2026-09-20/ergebnis.json): Exitcode 1. Bereits vorhanden waren Probleme mit Fixtures, Vorlagenreproduktion, Popup-Tests und Laufzeitgrenzen.
- [Zwischenlauf](../tests/qa-3.26.0/gesamtpruefung_2026-09-21/ergebnis.json): Exitcode 1. Veraltete Testannahmen zu Formulargeometrie, Verlauf und Auto-Beschriftung sowie Dokumentstände und ein verwaister Vorschau-Platzhalter wurden danach korrigiert. Die betroffenen Einzeltests bestanden anschließend.
- Neue Suite `tests/integration/test_features326.py`: Vorschau mit 205 Karten, Auswahlverbindungen, Ordnergrenzen, Lasso, Zoom/Printkoordinaten, Navigator, Akzente, Gismo, Rich-Text-Formate, Unicode, Undo/Redo, Speicherung, Duplikate, Vorlagen, Austausch, Migrationssicherung und Verlaufsgrenzen. Zusätzlich Suchaktualisierungen, Rückmeldungszuordnung und HTML-Escaping.
- Eigene Windows-Sichtproben liegen in `tests/qa-3.26.0/sichtpruefung`. Geprüft: breite und schmale Punktmaske, Notizliste mit sechs Aufgabenzeilen und nutzbarem Editor sowie Verlauf. Scrollbare Dialoginhalte bleiben über dem festen Fußbereich erreichbar.

Alle App-Importe und Tests verwenden temporäre GLIDE_DATA_DIR-Verzeichnisse mit künstlichen Daten. Nutzerdaten wurden nicht als Testbestand geöffnet.

## Grenzen

Automatisierte Tk-Ereignisse und Sichtprüfung ersetzen keinen vollständigen Bedienungstest durch einen Menschen. macOS, native Druckdialoge, reale Installer, Zertifikate und Notarisierung wurden hier nicht ausgeführt. Gismo-Bildmaterial bleibt ein separat vom Nutzer zu lieferndes Asset; die vorhandene zeichenbasierte Darstellung funktioniert weiterhin ohne neue Abhängigkeit. Offene Produktentscheidungen sind in der [Umsetzungsmatrix](decisions/Entscheidungen_3.26.0.md) getrennt aufgeführt.

Der historische [3.25-Abschluss](../tests/qa-3.25.0/abschluss/ergebnis.json) ist erhalten und wird nicht als Prüfnachweis für 3.26 ausgegeben.
