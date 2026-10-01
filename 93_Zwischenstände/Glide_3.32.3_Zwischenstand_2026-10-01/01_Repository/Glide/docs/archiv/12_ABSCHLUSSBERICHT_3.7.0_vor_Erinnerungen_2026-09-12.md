# Abschlussbericht – Glide 3.7.0

Stand: 12.09.2026 · unveröffentlichter Entwicklungsstand · Aufgabenformat 12

## Ergebnis

Vollständiger isolierter Vorlageneditor mit App-Farben, Labels, Anhängen,
relativen Terminen und erhaltener Baumstruktur; 16 Praxisvorlagen.
Mac-Auswahlfelder einschließlich Popup verwenden App-Farben, während Windows
und Linux den bisherigen OptionMenu-Pfad behalten. Die Bestandsübersicht nutzt
1–3 unabhängig gestapelte Spalten mit eigener Inhaltshöhe, ohne redundante
Typzeile, mit 16 Pixel Innenabstand und 12 Pixel Kartenabstand. Vollständige
Öffnen-/Bearbeiten-Aktionen umbrechen und werden beim Tastaturfokus sichtbar.

Der vorangegangene Mac-Bildlauf, die vollständige Vorlagenbearbeitung,
Vorlagenformat 2 und der praxisbezogene Katalog sind enthalten.
[Funktionsübersicht](25_FEATURE_ABGLEICH_3.7.0.md) · [Versionsübersicht](24_VERSION_3.7.0.md).

## Nachweise und Grenzen

Der aktuelle kombinierte Prüflauf auf macOS/Python 3.14.5 bestand mit Exitcode 0:
elf Testsuiten, zwei statische Analysen sowie Beispiel-/Releaseabgleiche.
Die neuen UI-Änderungen wurden nicht auf einem Windows-System ausgeführt.
Frühere Windows-Protokolle belegen ausschließlich den damaligen Quellstand.
Native Sichtabnahme, physisches Trackpad, weitere DPI/Monitore, Screenreader,
Langzeitbetrieb, Installer und Signierung bleiben offen.

- [Vollständiger Abschlusslauf](../tests/qa-3.7.0/dynamische-kacheln/abschluss/ergebnis.json)
- [18 Geometriefälle](../tests/qa-3.7.0/dynamische-kacheln/geometrie.json)
- [Code-/Arbeitskopie-Prüfsummen](../tests/qa-3.7.0/dynamische-kacheln/gepruefter_quellstand_sha256.json)
- [QA-Bericht](07_QA_BERICHT.md)
- [Startbare Arbeitskopie](../../../07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.7.0.pyw)

Die bisherigen Word-Berichte liegen im äußeren `10_Dokumentation/Archiv/`.
Sie sind historische Nachweise. Die aktuellen Markdown-Dokumente im
[Dokumentationsindex](00_INDEX.md) sind der verbindliche Einstieg.
Frühere Leistungszahlen bleiben als Messungen ihres damaligen Stands gekennzeichnet.
