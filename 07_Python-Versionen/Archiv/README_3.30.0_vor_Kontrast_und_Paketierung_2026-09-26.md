# Aktuelle startbare Python-Fassung

Glide 3.30.0 · Entwicklungsstand 26.09.2026 · Aufgabenformat 20 · Vorlagenformat 2

[Glide-Aufgaben-und-Listen_v3.30.0.pyw](Glide-Aufgaben-und-Listen_v3.30.0.pyw)
ist die bytegleiche Arbeitskopie des kanonischen Codes. Die Module
[`drawing.py`](drawing.py) und [`drawing_image.py`](drawing_image.py) gehören
bytegleich in denselben Ordner; ohne sie startet die Anwendung nicht. Der
vollständige Nachbarordner `resources` gehört ebenfalls dazu. Mit einem
Tk-fähigen Python starten; eine laufende ältere Instanz vorher schließen.

## Neu in 3.30

- **Pixel-Werkstatt:** Flächen mit 16, 32, 64 und 128 Zellen, Linie,
  Rechteck und Ellipse, Symmetrie, Auswahl, Paletten, Rückgängig je Aktion,
  Zwischenstände, PNG-Export und gezeichnete Symbole für Listen und Ordner.
- **Startseite und Seitenleiste:** anpassbare Kacheln, angeheftete Seiten und
  Filter, einklappbare Abschnitte, Suche mit Strg/Cmd+O.
- **Pinnwand als Board:** Spalten nach Feldern, Bereiche, beschriftete
  Verbindungen, Hintergründe, Präsentation, Zeichnungen als Karten.
- **Liste, Tabelle, Tagebuch:** Gruppierung, Detailbereich, Tagebuch mit allen
  Inhaltsarten und Filtern.
- **Planung:** verknüpfte Punkte, „wartet auf“, Zeitplan in „Mein Tag“,
  Zeiterfassung, Kapazität je Wochentag, Tagesbeginn und Wochenrückblick,
  Vorlagen mit Eingabefeldern, Archiv.
- **Design „Pixel · Blockfarben“** mit der Pixelschrift „Pixelify Sans“
  (SIL OFL 1.1) für Überschriften; sie liegt in `resources/fonts`.
- **Ausbau:** Zeitblöcke in „Mein Tag“ ziehen, Präsentation und Notizfolien
  als PDF, Rückgängig beim Kartenverschieben, Detailbereich mit allen Feldern,
  Gismo in Leerzuständen.
- **Zweiter Ausbau (26.09.2026):** Anhänge im Detailbereich, Zeichnungen als
  Bild in Folien und Druck, Stundenraster neben „Mein Tag“ (Blöcke ziehen),
  Gruppierung mit Überschriften und erhaltener Nummerierung.
- **Dritter Ausbau (26.09.2026):** Punkte aus der Liste ins Stundenraster
  ziehen, gruppierte Tabelle mit Nummern und Überschriften, Pixelschrift
  unter Linux über Fontconfig.
- **Kleine Fenster (26.09.2026):** Bei Mindestgröße bleibt das Wichtigste,
  nichts wird gequetscht oder angeschnitten; Überschriften auch in der
  sortierten Tabelle.

## Datenformat und frühere Fassungen

Aufgabenformat 20 legt beim ersten Speichern eines älteren Bestands die
unveränderte Sicherung `liste_vor_format20_<Zeitstempel>.json` an.

**Glide 3.29 danach nicht mehr starten.** Es hält den Bestand für beschädigt,
beginnt leer und überschreibt ihn bei der ersten Eingabe. Zurück zu 3.29 geht
es nur mit der Vorsicherung in einer getrennten Ablage. 3.30 selbst öffnet
einen Bestand aus einer neueren Version nur schreibgeschützt.

Vorherige startbare Fassungen liegen im Unterordner `Archiv`:

- 3.29.0 liegt mit seinen beiden Modulen im eigenen Ordner
  `Archiv/Glide-Aufgaben-und-Listen_v3.29.0` und startet von dort – nur mit
  einer getrennten Ablage (`GLIDE_DATA_DIR`), nie mit dem umgestellten
  Bestand. Ohne `resources` nutzt sie die Systemschrift und die eingebauten
  Ersatzvorlagen.
- Der Stand 3.30.0 vor dem Ausbau vom 25.09.2026 liegt als Zwischenstand samt
  Modulen unter `Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Ausbau_2026-09-25`
  (Format 20 wie der aktuelle Stand). Der Stand vor dem zweiten Ausbau vom
  26.09.2026 liegt ebenso unter
  `Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Ausbau2_2026-09-26`, der
  Stand vor dem dritten Ausbau unter
  `Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Ausbau3_2026-09-26`, der
  vor der Überarbeitung für kleine Fenster unter
  `Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Mindestgroesse_2026-09-26`.
- 3.28.0 und älter liegen direkt im Archiv; sie brauchen keine Module.
- 3.27.0 ist als undokumentierter UI-/UX-Zwischenstand erhalten.

Benachrichtigungen funktionieren weiterhin nur bei laufender App.

[Modernisierung 3.30](../01_Repository/Glide/docs/66_MODERNISIERUNG_3.30.0.md) ·
[Zeichnungsseite 3.29](../01_Repository/Glide/docs/65_ZEICHNUNGSSEITE_3.29.0.md) ·
[Prüfstand](../01_Repository/Glide/docs/07_QA_BERICHT.md) ·
[Dokumentationsindex](../01_Repository/Glide/docs/00_INDEX.md)
