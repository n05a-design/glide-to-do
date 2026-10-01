# Release-Checkliste

Stand 26.09.2026 · Glide 3.30.0 · interner Entwicklungsstand · Aufgabenformat 20

## Quellstand

- [x] `VERSION`, `APP_VERSION`, Changelog, startbare Kopie und aktive Dokumente stimmen auf 3.30.0 überein.
- [x] Aufgabenformat 20, `current_v20`, `ensure_schema20_backup` und historische Referenzen 4–19 sind vorhanden.
- [x] Kanonische Dateien (`app.pyw`, `drawing.py`, `drawing_image.py`, `resources`) und die startbare
  3.30-Kopie sind bytegleich; 3.29.0 und die Stände vor dem ersten, zweiten und dritten Ausbau sowie vor den Runden „kleine Fenster“, „Kontrast und Paketierung“, „Hintergrundverläufe“ und „Rückmeldung“ liegen startfähig im Archiv.
- [x] Syntax, Hauptsuite, Integrationssuiten, Analysen, Links, Standprüfung, Fixtures und Erzeugerabgleich
  laufen im isolierten Datenordner, dazu Mindestgröße, Kontrast, Paketierung,
  Hintergrundverläufe und Rückmeldung – Vollmodus am 26.09.2026 mit Exitcode 0
  ([Protokoll](../tests/qa-3.30.0/rueckmeldung_2026-09-26/ergebnis.json)).
- [x] Ergebnis und verbleibende Grenzen sind in [07_QA_BERICHT.md](07_QA_BERICHT.md) konkret dokumentiert.

## Abnahme 3.28 (weiterhin offen)

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

- [x] Format-19-Bestand (Kopie echter Daten) öffnen und speichern; bytegleiche
  `liste_vor_format20_*.json` nachgewiesen (Echtdatenprobe 25.09.2026).
- [ ] **Rückfall:** Glide 3.29 überschreibt einen Format-20-Bestand bei der ersten Eingabe. Vor einer
  Veröffentlichung in Hinweisen und Store-Texten deutlich sagen: nach dem Update keine ältere Version starten;
  zurück nur über die Vorsicherung in einer getrennten Ablage.
- [x] Glide 3.30 öffnet einen Bestand aus einer neueren Version schreibgeschützt, sichert eine unlesbare Datei als
  `liste_unlesbar_*.json` und warnt über `data_format_written` (automatisch geprüft).
- [ ] Vollbackup und additive Übernahme mit Beziehungen, Zeiterfassung, Pixelsymbolen und Archiv vergleichen.
- [ ] Zeichnungsseiten nach [manueller Prüfung 3.29](../../../00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.29.0.md) prüfen: Maus/Trackpad, Tastatur, Autosave und Neustart, Referenz-PNG, Nachzeichnung, SVG in Browser, Illustrator und Affinity.
- [ ] 3.30 nach [manueller Prüfung 3.30](../../../00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.30.0.md) prüfen:
  - Pixel-Werkstatt mit Maus und Trackpad;
  - Spaltenboard und Bereiche per Ziehen;
  - Startseite anpassen, Detailbereich, Design „Pixel“ mit Pixelify Sans;
  - Zeitblöcke ziehen, Folien als PDF, Gismo in Leerzuständen;
  - DPI, Mehrmonitor und Bildschirmleser.
- [ ] Paket enthält `drawing.py`, `drawing_image.py` und `resources` (Schriften mit Lizenztexten und
  `provenance.json`, Vorlagen) neben `app.pyw`.

## Noch erforderliche Plattformabnahme

- [ ] Windows-Vollprüfung mit `tests/tools/windows_vollpruefung.cmd`
  ([Anleitung](../../../00_Arbeitsvorbereitung/Checklisten/Windows_Pruefung_3.30.0.md));
  Ergebnis in QA-Bericht und QA-Verlauf eintragen.
- [ ] [Produktdatenblatt 3.30](../../../40_Store_Material/Produktdatenblatt_3.30.0_Entwurf.md)
  nach der manuellen Abnahme freigeben; Screenshots vom realen Build.
- [x] Kennungen festgelegt: `de.shaye.glide` und `Shaye.Glide`
  ([Produktregister](decisions/PRODUCT_IDENTITY.md)).
- [x] macOS-Entwicklungsbundle mit Ad-hoc-Signatur baut und startet als
  „Glide“ (`packaging/macos/baue_app.py`, `test_paketierung330`).
- [ ] Windows-Verknüpfung mit AppUserModelID unter Windows prüfen
  (`packaging/windows/verknuepfung_anlegen.ps1`).
- [ ] Hintergrundverläufe unter Windows ansehen: Kopfzeile, Rand, Seitenleiste,
  Größenänderung und Scrollen ohne Bildreste (Vertrag 66, Abschnitt 2.8).
- [ ] Release-Build mit eingebettetem Python (PyInstaller pinnen),
  Developer-ID-Signatur und Notarisierung, Installer; echtes Logo als
  Symbol statt des Platzhalters.
- [ ] Reale Windows-/macOS-Bedienung mit Maus, Trackpad, App-Wechsel und verschachtelten Dialogen.
- [ ] DPI/Mehrmonitor, Hochkontrast/RDP, Screenreader und nur per Tastatur.
- [ ] Druck-/PDF-Dialoge, Ruhezustand/Aufwachen, Dauerlauf und synchronisierte Datenordner.
- [ ] Installer/App-Bundle, Clean Machine, Signatur, Notarisierung/Gatekeeper und Storematerial.

Automatisch grüne Tests sind kein Ersatz für diese manuelle Plattformabnahme
und keine Veröffentlichung. Benachrichtigungen werden weiterhin nur bei
laufender App verarbeitet.
