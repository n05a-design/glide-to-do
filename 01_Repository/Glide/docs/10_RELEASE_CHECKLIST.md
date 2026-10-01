# Release-Checkliste

Stand 01.10.2026 · Glide 3.33.1 · interner Entwicklungsstand · Aufgabenformat 20

## Quellstand 3.32.3

- [x] VERSION/App/Hauptsuite auf 3.32.3; Datenformat 20, bisherige Speicherwege und Hinweisgestaltung erhalten.
- [x] Quellstand, Python-Vollstand und Bundle 3.32.2 vor Änderung archiviert; [Vorsicherungsnachweis](../tests/qa-3.32.3/karten_performance_2026-10-01/vorsicherungen.json).
- [x] Bibliotheks-/Aktionsleisten-Bedienproben bestanden; [Vertrag 71](71_KARTEN_PERFORMANCE_3.32.3.md).
- [x] Unprofilierte Vorher-/Nachher-Messungen mit 100/1.000/10.000 Aufgaben, Rohwerten und Neuerzeugungen dokumentiert.
- [x] Vollprüfung mit 58 Suiten und fünf Analysen einschließlich Syntax/Version/Stand/Links, Fixtures und Erzeugerabgleich bestanden (73 Schritte, Exitcode 0); [Protokoll](../tests/qa-3.32.3/karten_performance_2026-10-01/vollpruefung/ergebnis.json).
- [x] Python-Fassung (139 Dateien) und macOS-Bundle (53 Quell-/Ressourcendateien) nach Vollprüfung per SHA-256 bytegleich, Version 3.32.3 und Signatur geprüft; [Abgleich](../tests/qa-3.32.3/karten_performance_2026-10-01/abgleich.json).
- [x] Abschlussergebnis und manuelle Grenzen im [QA-Bericht](07_QA_BERICHT.md) nachgeführt.

## Aktuelle manuelle Abnahme

Die ursprünglichen 3.28–3.30-Listen sind in der [fortgeschriebenen manuellen Prüfliste](../../../00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.30.0.md) zusammengeführt. Ihr Anhang unterscheidet automatisch geprüfte Logik, offenes Handgefühl, überholte Punkte und beantwortete Entscheidungen; F11 ist durch D05 beantwortet. Die alten zehn Abnahmepunkte werden hier nicht als zusätzliche ungeprüfte Funktionen weitergeführt.

- [ ] Physische macOS-Bedienung A1–A21 durchführen; insbesondere Klappmechanismen, Drag-Ziele und Fokus/Scrollen bei Kartenaktualisierung.
- [ ] Windows/Linux, Tastatur/Screenreader, DPI/Mehrmonitor und Dauerbetrieb nach derselben Prüfliste durchführen und Befunde zuordnen.

Automatische Abnahme und menschliche Geräteprüfung werden getrennt dokumentiert. [Arbeitsrichtung](ARBEITSRICHTUNG.md).

## Migration und Datensicherheit

- [x] Format-19-Bestand (Kopie echter Daten) öffnen und speichern; bytegleiche
  `liste_vor_format20_*.json` nachgewiesen (Echtdatenprobe 25.09.2026).
- [ ] **Rückfall:** Glide 3.29 überschreibt einen Format-20-Bestand bei der ersten Eingabe. Vor einer
  Veröffentlichung in Hinweisen und Store-Texten deutlich sagen: nach dem Update keine ältere Version starten;
  zurück nur über die Vorsicherung in einer getrennten Ablage.
- [x] Glide 3.30 öffnet einen Bestand aus einer neueren Version schreibgeschützt, sichert eine unlesbare Datei als
  `liste_unlesbar_*.json` und warnt über `data_format_written` (automatisch geprüft).
- [x] Automatischer Voll-/Additivbackup-Rundlauf mit Beziehungen, Zeiterfassung, Pixelsymbolen und Archiv in der 3.32.3-Vollprüfung; reale Plattformbedienung bleibt in der manuellen Prüfliste offen.
- [ ] Zeichnungsseiten nach der [manuellen Prüfung 3.30](../../../00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.30.0.md) prüfen (enthält seit 29.09.2026 die Punkte aus 3.29): Maus/Trackpad, Tastatur, Autosave und Neustart, Referenz-PNG, Nachzeichnung, SVG in Browser, Illustrator und Affinity.
- [ ] Aktuelle App nach [manueller Prüfliste](../../../00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.30.0.md) prüfen:
  - Pixel-Werkstatt mit Maus und Trackpad;
  - Spaltenboard und Bereiche per Ziehen;
  - Startseite anpassen, Detailbereich, Design „Pixel“ mit Pixelify Sans;
  - Zeitblöcke ziehen, Folien als PDF, Gismo in Leerzuständen;
  - Bilder in Seiten, Ziehen aus Finder/Explorer, Systemmitteilungen,
    feste Bestandteile beim Wechseln der Ansichten (27.09.2026);
  - DPI, Mehrmonitor und Bildschirmleser.
- [x] macOS-Entwicklungspaket enthält `drawing.py`, `drawing_image.py`, `backdrop.py`, `page_markdown.py`, `image_preview.py`, `logo.py` und `glide_start.py` und `resources` (Schriften mit Lizenztexten und
  `provenance.json`, Vorlagen) neben `app.pyw`, dazu `vendor/tkinterdnd2` mit Lizenz und nur den
  Bibliotheken der Zielplattform (automatische Prüfung und 53-Dateien-SHA-Abgleich für macOS 3.32.3). Die vollständige Python-Fassung enthält 139 Dateien; Windows-/Linux-Releasepakete bleiben offen.
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
