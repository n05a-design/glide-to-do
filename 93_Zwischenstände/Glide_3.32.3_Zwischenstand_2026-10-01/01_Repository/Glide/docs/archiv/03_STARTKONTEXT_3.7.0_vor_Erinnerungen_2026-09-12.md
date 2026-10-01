# Startkontext – Glide 3.7.0

Stand: 12.09.2026 · Aufgabenformat 12 · Einstellungen 2 · Vorlagenformat 2

Projektwurzel: `01_Repository/Glide` innerhalb der Glide-ToDo-Arbeitsablage.
Kanonische App: `src/glide/app.pyw`. Die startbare Kopie im äußeren
`07_Python-Versionen/` benötigt den vollständigen Nachbarordner `resources`.
Keine fest codierten Benutzer- oder Windows-Pfade als Voraussetzung verwenden.

Zuerst `AGENTS.md`, [Produktgrenzen](01_PRODUCT_CONSTRAINTS.md),
[Architektur](02_ARCHITECTURE.md), [Funktionsübersicht](25_FEATURE_ABGLEICH_3.7.0.md),
[aktuellen QA-Bericht](07_QA_BERICHT.md) und [Übergabe](09_PROJECT_HANDOFF.md) lesen.

## Aktueller Stand

Vollständiger isolierter Vorlageneditor mit App-Farben, Labels, Anhängen,
relativen Terminen und erhaltener Baumstruktur; 16 Praxisvorlagen.
Mac-Auswahlfelder einschließlich Popup verwenden App-Farben, während Windows
und Linux den bisherigen OptionMenu-Pfad behalten. Die Bestandsübersicht nutzt
1–3 unabhängig gestapelte Spalten mit eigener Inhaltshöhe, ohne redundante
Typzeile, mit 16 Pixel Innenabstand und 12 Pixel Kartenabstand. Vollständige
Öffnen-/Bearbeiten-Aktionen umbrechen und werden beim Tastaturfokus sichtbar.

Der aktuelle kombinierte Prüflauf auf macOS/Python 3.14.5 bestand mit Exitcode 0:
elf Testsuiten, zwei statische Analysen sowie Beispiel-/Releaseabgleiche.
Die neuen UI-Änderungen wurden nicht auf einem Windows-System ausgeführt.
Frühere Windows-Protokolle belegen ausschließlich den damaligen Quellstand.
Native Sichtabnahme, physisches Trackpad, weitere DPI/Monitore, Screenreader,
Langzeitbetrieb, Installer und Signierung bleiben offen.

## Prüfaufruf

```text
python3 tests/tools/pruefen.py --modus voll --timeout 600 --protokoll tests/qa-3.7.0/erneute-pruefung
```

Unter Windows den vorhandenen Python-Interpreter verwenden. App-Tests setzen
vor dem Import einen eigenen temporären `GLIDE_DATA_DIR`. Niemals echte Nutzdaten
für Experimente laden. Historische Migrations-Fixtures bleiben erhalten.
Änderungen über `item_change`, `sidebar_change`, `guarded_structural_change`;
modale Dialoge über `run_modal`, Symbole aus `ICONS`.

Vor dem Ersetzen aktueller Dokumente deren Vorfassung lokal archivieren.
Die [Chatweitergabe](../../../00_Arbeitsvorbereitung/Glide_Weitergabe_neuer_Chat_2026-09-11.md)
führt Nutzerprioritäten und Prüfgrenzen weiter. Frühere Pläne im Archiv sind keine
neuen Aufgaben; abgeschlossene UI-Korrekturen nicht erneut als offen behandeln.
