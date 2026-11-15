# Dreieckmarker – 3.63.0, 15.11.2026

Künstliche, über `GLIDE_DATA_DIR` isolierte Testdaten. Baseline B09 grün; B09 nach Umbau grün einschließlich echter Klicks und Themenwechsel. Sichtproben `seitenleiste-light.png` und `seitenleiste-dark.png` geprüft: gefüllte kleine Dreiecke, keine Marker an Blattzeilen. Der ältere Screenshot `seitenleiste-hell.png` ist ein überholter Zwischenstand und kein Abnahmebeleg.

- `grundstufe/`: erster, integritätsroter Lauf (Quellen während der Ausführung geändert). Fachtests darin Exitcode 0; Folgeschritte übersprungen.
- `grundstufe-final/`: alle funktionalen Schritte grün; Ablagegröße rot wegen zweier mit dem Versionswechsel veralteter 3.51.0-Dateien, Synchronisation danach übersprungen.
- `grundstufe-abschluss/`: separater Nachlauf nach den abschließenden Darstellungs- und Ablagekorrekturen; tatsächliches Ergebnis in `ergebnis.json`.
- `test_arbeitsmodi.py --fall seitenleistenzeilen3507`: 48 Konfigurationen, 384 sichtbare Zeilen, vier Schriftstile, drei Größen, hell/dunkel und zwei Breiten sowie vier Neustarts grün.

Die beiden 3.51.0-Dateien (Releaseplanungs-Fixture und archivierte Python-Hauptdatei) werden nach der Aufbewahrungsregel entfernt; die Git-Historie bewahrt sie. Historische QA-Verzeichnisse bleiben erhalten.
- Native Mac-/Linux-Matrix, vollständige DPI-/Schriftstilprüfung, Screenreader, eigenständige Pakete und menschliche Sichtabnahme offen.

Geprüfter Umfang und Historie im zentralen QA-Bericht. Eine grüne Grundstufe ersetzt keine Plattform- oder Releaseabnahme.


Für die Git-Veröffentlichung wurden lokale Pfadpräfixe in den JSON-Nachweisen anonymisiert. Prüfstatus und Messwerte sind unverändert; die unveränderten Rohfassungen bleiben lokal außerhalb des versionierten Bestands erhalten.
