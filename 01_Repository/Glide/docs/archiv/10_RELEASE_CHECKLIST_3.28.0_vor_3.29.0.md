# Release-Checkliste

Stand 23.09.2026 · Glide 3.28.0 · interner Entwicklungsstand · Aufgabenformat 18

## Quellstand

- [x] `VERSION`, `APP_VERSION`, Changelog, startbare Kopie und aktive Dokumente stimmen auf 3.28.0 überein.
- [x] Aufgabenformat 18, `current_v18`, `ensure_schema18_backup` und historische Referenzen 4–17 sind vorhanden.
- [x] Kanonische Datei und startbare 3.28-Kopie sind bytegleich; 3.27 liegt im Archiv.
- [ ] Syntax, Hauptsuite, Integrationssuiten, Analysen, Links, Standprüfung, Fixtures und Erzeugerabgleich laufen im isolierten Datenordner.
- [x] Ergebnis und verbleibende Grenzen sind in [07_QA_BERICHT.md](07_QA_BERICHT.md) konkret dokumentiert.

## Abnahme 3.28

- [ ] Standard- und Tagebuch-Ordner anlegen, bearbeiten, verschachteln, sichern, importieren und aus dem Papierkorb wiederherstellen.
- [ ] Tagebucheintrag anlegen; Favorit, alle Stimmungen, Ort, Momentdatum, Schreibimpuls, Suche und Datumssortierung prüfen.
- [ ] Tagesnotiz, Dankbarkeit, Wochenrückblick und Jahresordner aus Vorlagen erzeugen.
- [ ] Notizwerkzeuge in breiter und minimaler Ansicht prüfen; seltene Werkzeuge sind unter `Mehr`, ohne Funktionsverlust.
- [ ] Mittlere Maustaste halten und Zeiger nach oben, unten, links und rechts bewegen; Totzone, Geschwindigkeit und sofortigen Stopp prüfen.
- [ ] Startseite: Gismo füttern/spielen/ruhen, Tagesabnahme nach Datumswechsel, Wertebereiche 0–100 und Speicherung prüfen.
- [ ] Pinnwandvorschau mit leerer, kleiner und großer Pinnwand prüfen; Vorschau darf keine erfundenen Inhalte enthalten.
- [ ] Mindestbreite: Such-/Eingabefelder, Tabellenfläche, rechte Flucht, Kopfaktionen, Pinnwandoptionen und untere Aktionen prüfen.
- [ ] Hell-/Dunkel- und weitere Designs: neutrale Nebenaktionen, semantische Farben, Kontrast und sichtbarer Tastaturfokus prüfen.
- [ ] Menüs ohne dekorative Outline sowie keine Schaltfläche mit sichtbarem `...` prüfen.

## Migration und Datensicherheit

- [ ] Format-17-Datei in isolierter Ablage öffnen und speichern; bytegleiche `liste_vor_format18_*.json` nachweisen.
- [ ] Format-18-Datei mit einer älteren Fassung sichtbar ablehnen lassen; nie zum Downgrade überschreiben.
- [ ] Vollbackup und additive Übernahme einschließlich `folder_kind` und `journal` vergleichen.
- [ ] Defekte oder unbekannte Tagebuchwerte werden normalisiert, ohne Aufgaben oder Notiztext zu verlieren.

## Noch erforderliche Plattformabnahme

- [ ] Reale Windows-/macOS-Bedienung mit Maus, Trackpad, App-Wechsel und verschachtelten Dialogen.
- [ ] DPI/Mehrmonitor, Hochkontrast/RDP, Screenreader und nur per Tastatur.
- [ ] Druck-/PDF-Dialoge, Ruhezustand/Aufwachen, Dauerlauf und synchronisierte Datenordner.
- [ ] Installer/App-Bundle, Clean Machine, Signatur, Notarisierung/Gatekeeper und Storematerial.

Automatisch grüne Tests sind kein Ersatz für diese manuelle Plattformabnahme
und keine Veröffentlichung. Benachrichtigungen werden weiterhin nur bei
laufender App verarbeitet.
