# Projektübergabe – Glide 3.7.0

Stand: 12.09.2026 · Aufgabenformat 12 · Einstellungen 2 · Vorlagenformat 2

Kanonischer Code: `src/glide/app.pyw`. Die startbare Arbeitskopie liegt im
äußeren `07_Python-Versionen/` samt vollständigem `resources`-Ordner.
Der Entwicklungsstand ist unveröffentlicht und kein Git-Checkout.

## Abgeschlossene Änderungen

Vollständiger isolierter Vorlageneditor mit App-Farben, Labels, Anhängen,
relativen Terminen und erhaltener Baumstruktur; 16 Praxisvorlagen.
Mac-Auswahlfelder einschließlich Popup verwenden App-Farben, während Windows
und Linux den bisherigen OptionMenu-Pfad behalten. Die Bestandsübersicht nutzt
1–3 unabhängig gestapelte Spalten mit eigener Inhaltshöhe, ohne redundante
Typzeile, mit 16 Pixel Innenabstand und 12 Pixel Kartenabstand. Vollständige
Öffnen-/Bearbeiten-Aktionen umbrechen und werden beim Tastaturfokus sichtbar.

Startseite verarbeitet kleine Mausrad- und Tk-9-Trackpadereignisse.
Nutzdaten und Datenformat wurden durch die jüngsten UI-Korrekturen nicht geändert.
Arbeitskopie und sieben Ressourcen stimmen mit dem Projekt überein.

## Prüfstand

Der aktuelle kombinierte Prüflauf auf macOS/Python 3.14.5 bestand mit Exitcode 0:
elf Testsuiten, zwei statische Analysen sowie Beispiel-/Releaseabgleiche.
Die neuen UI-Änderungen wurden nicht auf einem Windows-System ausgeführt.
Frühere Windows-Protokolle belegen ausschließlich den damaligen Quellstand.
Native Sichtabnahme, physisches Trackpad, weitere DPI/Monitore, Screenreader,
Langzeitbetrieb, Installer und Signierung bleiben offen.

[Gesamtlauf](../tests/qa-3.7.0/dynamische-kacheln/abschluss/ergebnis.json) · [QA](07_QA_BERICHT.md).

## Fortsetzung

Zuerst `AGENTS.md`, [Startkontext](03_STARTKONTEXT.md),
[Funktionsübersicht](25_FEATURE_ABGLEICH_3.7.0.md), [Vorlagen-/Mac-Nachtrag](26_MAC_VORLAGEN_UND_ABLAGE_3.7.0.md)
und [Kachelnachtrag](29_DYNAMISCHE_KACHELN_3.7.0.md) lesen.
Tests ausschließlich mit temporärem `GLIDE_DATA_DIR`; Originaldaten bewahren.
Vor Dokumentänderungen die Vorfassung im lokalen Archiv sichern.

Die [kompakte Chatweitergabe](../../../00_Arbeitsvorbereitung/Glide_Weitergabe_neuer_Chat_2026-09-11.md)
enthält die Nutzerprioritäten: Erinnerungen zuerst, danach mögliche Reiter/Pinnwand;
keine zusätzliche Statusablage und keine parallele Projektmappe.
Diese Zukunftsfunktionen sind nicht umgesetzt und nicht pauschal freigegeben.
Aktueller Code und belegte Prüfungen haben Vorrang vor historischen Berichten.
