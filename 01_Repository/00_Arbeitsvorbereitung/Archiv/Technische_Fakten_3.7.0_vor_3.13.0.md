# Technische Fakten Glide 3.7.0

Stand: 12.09.2026. Kanonisch: `01_Repository/Glide/src/glide/app.pyw`, `VERSION`
und die aktuellen QA-Rohlogs. Aufgabenformat 12, Einstellungen 2, Vorlagenformat 2.
Python/Tk und Standardbibliothek; vier DejaVu-Sans-TTF-Schnitte mit Lizenz.

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

Datenordner frei wählbar, Fremdsperre führt zum Schreibschutz. Containeranhänge
werden in den vorhandenen portablen Aufgabenbackups mitgeführt; persönliche
Einstellungen und der separate Vorlagenkatalog gehören nicht zu diesen Backups.
Materialoptik ist kein nachgewiesener selektiver Desktop-Blur.

[Funktionsübersicht](../../01_Repository/Glide/docs/25_FEATURE_ABGLEICH_3.7.0.md) ·
[QA](../../01_Repository/Glide/docs/07_QA_BERICHT.md).
