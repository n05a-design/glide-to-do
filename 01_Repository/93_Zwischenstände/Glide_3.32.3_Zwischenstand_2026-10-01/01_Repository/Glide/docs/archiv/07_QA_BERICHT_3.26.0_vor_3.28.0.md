# QA-Bericht – Glide 3.26.0

Stand 21.09.2026 · App 3.26.0 · Datenformat 17 · Windows, Python 3.13.15

## Prüfstand

Der [abschließende Windows-Gesamtlauf](../tests/qa-3.26.0/abschluss_final_2026-09-21/ergebnis.json) endete mit **Exitcode 0**: 48 Prüfschritte, davon 47 erfolgreich ausgeführt. Einzig die im Prüfwerkzeug als manuell definierte Sichtprüfung ist übersprungen. Python 3.13.15, W. Europe Daylight Time mit Sommerzeitregel. Syntax, Versionen, Dokumentlinks, 27 Backup-Fixtures und historische Formate, sämtliche Integrationssuiten, fünf Analysen, Erzeugerabgleich für Beispiel- und Releasedaten sowie Screenshot-Erzeugung bestanden.

- [Ausgangslauf vor der Nachbesserung](../tests/qa-3.26.0/vor_umsetzung_2026-09-20/ergebnis.json): Exitcode 1. Bereits vorhanden waren Probleme mit Fixtures, Vorlagenreproduktion, Popup-Tests und Laufzeitgrenzen.
- [Zwischenlauf](../tests/qa-3.26.0/gesamtpruefung_2026-09-21/ergebnis.json): Exitcode 1. Veraltete Testannahmen zu Formulargeometrie, Verlauf und Auto-Beschriftung sowie Dokumentstände und ein verwaister Vorschau-Platzhalter wurden danach korrigiert. Die betroffenen Einzeltests bestanden anschließend.
- [Erster Abschlusslauf](../tests/qa-3.26.0/abschluss_2026-09-21/ergebnis.json): Exitcode 1 durch zwei Testumgebungsfehler. Ein Mondphasen-Test verwies auf einen inzwischen archivierten Beleg; die Referenz liegt nun bei den dauerhaften Fixtures. Der Dropdown-Test benötigte unter Windows ausdrücklich den Fensterfokus. Die [gezielte Nachprüfung](../tests/qa-3.26.0/abschluss_nachpruefung_2026-09-21/ergebnis.json) bestand, danach der oben verlinkte vollständige Gesamtlauf ebenfalls.
- Neue Suite `tests/integration/test_features326.py`: Vorschau mit 205 Karten, Auswahlverbindungen, Ordnergrenzen, Lasso, Zoom/Printkoordinaten, Navigator, Akzente, Gismo, Rich-Text-Formate, Unicode, Undo/Redo, Speicherung, Duplikate, Vorlagen, Austausch, Migrationssicherung und Verlaufsgrenzen. Zusätzlich Suchaktualisierungen, Rückmeldungszuordnung und HTML-Escaping.
- Eigene Windows-[Sichtproben](../tests/qa-3.26.0/sichtpruefung/notiz.png) liegen in `tests/qa-3.26.0/sichtpruefung`. Angesehen: breite und schmale Punktmaske, Notizliste mit sechs Aufgabenzeilen und nutzbarem Editor, lesbarer Verlauf, Pinnwand bei 50/100/200 %, Navigator, Gismo und Startseiten-Vorschau mit 205 Karten. Scrollbare Dialoginhalte bleiben über dem festen Fußbereich erreichbar. Der simulierte Fehlschlag beim Schreiben der Notiz ließ die alte Datei intakt; ein zweiter Versuch speicherte den unverlorenen Entwurf.

Alle App-Importe und Tests verwenden temporäre GLIDE_DATA_DIR-Verzeichnisse mit künstlichen Daten. Nutzerdaten wurden nicht als Testbestand geöffnet.

## Grenzen

Automatisierte Tk-Ereignisse und diese gezielten Windows-Bildprüfungen ersetzen keinen vollständigen Bedienungstest durch einen Menschen auf allen Zielgeräten. macOS, native Druckdialoge, DPI-/Mehrmonitor-Sonderfälle, Screenreader, reale Installer, Zertifikate und Notarisierung wurden hier nicht ausgeführt. Gismo-Bildmaterial bleibt ein separat vom Nutzer zu lieferndes Asset; die vorhandene zeichenbasierte Darstellung funktioniert weiterhin ohne neue Abhängigkeit. Offene Produktentscheidungen sind in der [Umsetzungsmatrix](decisions/Entscheidungen_3.26.0.md) getrennt aufgeführt.

Der historische [3.25-Abschluss](../tests/qa-3.25.0/abschluss/ergebnis.json) ist erhalten und wird nicht als Prüfnachweis für 3.26 ausgegeben.

