# Release-Checkliste

Stand 30.09.2026 · Glide 3.32.2 · interner Entwicklungsstand · Aufgabenformat 20

## Quellstand

- [ ] `VERSION`, `APP_VERSION`, Changelog, startbare Kopie und aktive Dokumente stimmen nach Abgleich auf 3.32.2 überein.
- [x] Aufgabenformat 20, historische Referenzen und Sicherungswege erhalten; keine neue Abhängigkeit.
- [ ] Python-Fassung und macOS-Bundle nach Vollprüfung per SHA-256 abgleichen und Signatur prüfen. Vorheriger 3.32.1-Vollstand und Bundle sind vollständig archiviert.
- [ ] Vollprüfung mit 57 Suiten einschließlich neuer Drag-/Performance-Pflichtsuite, fünf Analysen, Syntax/Version/Stand/Links, Fixtures und Erzeugerabgleich abschließen.
- [x] Unprofilierte Vorher-/Nachher-Messungen und gezielte Drag-, Schrift-, Layout-, Bild-/Formatierungsproben dokumentiert: [Vertrag 70](70_DRAG_UND_PERFORMANCE_3.32.2.md).
- [ ] Abschlussergebnis und manuelle Grenzen in [QA-Bericht](07_QA_BERICHT.md) nachführen.

## Abnahme 3.28 (weiterhin offen)

- [ ] Ordner und Notizbücher (bis 27.09.2026 „Standard“ und „Tagebuch“) anlegen, bearbeiten, verschachteln, sichern, importieren und aus dem Papierkorb wiederherstellen.
- [ ] Notizbucheintrag anlegen; Favorit, alle Stimmungen, Ort, Momentdatum, Schreibimpuls, Suche und Datumssortierung prüfen.
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
- [ ] Zeichnungsseiten nach der [manuellen Prüfung 3.30](../../../00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.30.0.md) prüfen (enthält seit 29.09.2026 die Punkte aus 3.29): Maus/Trackpad, Tastatur, Autosave und Neustart, Referenz-PNG, Nachzeichnung, SVG in Browser, Illustrator und Affinity.
- [ ] 3.30 nach [manueller Prüfung 3.30](../../../00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.30.0.md) prüfen:
  - Pixel-Werkstatt mit Maus und Trackpad;
  - Spaltenboard und Bereiche per Ziehen;
  - Startseite anpassen, Detailbereich, Design „Pixel“ mit Pixelify Sans;
  - Zeitblöcke ziehen, Folien als PDF, Gismo in Leerzuständen;
  - Bilder in Seiten, Ziehen aus Finder/Explorer, Systemmitteilungen,
    feste Bestandteile beim Wechseln der Ansichten (27.09.2026);
  - DPI, Mehrmonitor und Bildschirmleser.
- [ ] Paket enthält `drawing.py`, `drawing_image.py`, `backdrop.py`, `page_markdown.py`, `image_preview.py`, `logo.py` und `glide_start.py` und `resources` (Schriften mit Lizenztexten und
  `provenance.json`, Vorlagen) neben `app.pyw`, dazu `vendor/tkinterdnd2` mit Lizenz und nur den
  Bibliotheken der Zielplattform (das macOS-Entwicklungsbundle prüft `test_paketierung330`).
- [ ] Die tkDnD-Bibliothek ist mit dem Release signiert und notarisiert
  ([Entscheidung](decisions/ABHAENGIGKEIT_TKDND.md)).
- [ ] Inhaberangaben aus den [Vorschlägen](../../../40_Store_Material/Inhaberangaben_Vorschlaege_2026-09-27.md)
  bestätigt und ins Produktregister übernommen.

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
- [x] Echtes Logo als Programmsymbol statt des Platzhalters: Master in
  `20_Grafik_Master`, Paketsymbole in `assets/icons` (29.09.2026).
- [ ] Release-Build mit eingebettetem Python (PyInstaller ab 6.22 pinnen, das
  Tk 9 unterstützt), Developer-ID-Signatur und Notarisierung, Installer.
- [ ] Reale Windows-/macOS-Bedienung mit Maus, Trackpad, App-Wechsel und verschachtelten Dialogen.
- [ ] DPI/Mehrmonitor, Hochkontrast/RDP, Screenreader und nur per Tastatur.
- [ ] Druck-/PDF-Dialoge, Ruhezustand/Aufwachen, Dauerlauf und synchronisierte Datenordner.
- [ ] Installer/App-Bundle, Clean Machine, Signatur, Notarisierung/Gatekeeper und Storematerial.

Automatisch grüne Tests sind kein Ersatz für diese manuelle Plattformabnahme
und keine Veröffentlichung. Benachrichtigungen werden weiterhin nur bei
laufender App verarbeitet.
