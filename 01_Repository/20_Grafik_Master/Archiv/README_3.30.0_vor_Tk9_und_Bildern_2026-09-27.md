# Grafik-Master

Stand 26.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

Arbeitsbereich für Illustrator-/Photoshop-Quellen und freigegebene
Branding-Master. Generierte App-Assets werden erst nach Freigabe in den
Repository-Bereich `assets/` übernommen.

## Struktur

- `Illustrator/`, `Photoshop/`, `Arbeitsdateien/` – Quellen
- `Branding/` – freigegebene Master
- `Archiv/` – überholte Master und deren Arbeitsdateien

## Stand 26.09.2026

- **Logo-Quelle:** Das Logo liegt als Affinity-Datei `Glide-Logo.af` im
  Wurzelordner der Ablage. Ein freigegebenes Masterpaket gibt es noch nicht.
  Deshalb enthält `assets/` bewusst keine Grafiken.
- **App-Symbol:** Gebraucht wird ein quadratischer PNG-Export ab 1024 px.
  - Das macOS-Entwicklungsbundle übernimmt ihn mit
    `packaging/macos/baue_app.py --symbol DATEI.png`.
  - Ohne Export erzeugt es ein Pixel-„G“ als Platzhalter, nur im
    Build-Ordner.
  - Für Windows wird daraus später eine `.ico` (16/24/32/48/256 px).
- **Store-Grafiken:** Anforderungen stehen in den historischen Recherchen für
  [Apple](../40_Store_Material/Archiv/Store_Angaben_Apple_historische_Recherche_2026-09-24.md)
  und [Microsoft](../40_Store_Material/Archiv/Store_Angaben_Microsoft_historische_Recherche_2026-09-24.md).
  Sie sind vor einer Einreichung neu abzurufen; siehe
  [Release-Checkliste](../01_Repository/Glide/docs/10_RELEASE_CHECKLIST.md).

## Hinweis zur Typografie

Glide bringt zwei privat registrierte Schriften mit, beide unter
`src/glide/resources/fonts/` samt Lizenztexten:

- DejaVu Sans in vier Schnitten;
- Pixelify Sans (SIL OFL 1.1) für die Überschriften im Design „Pixel“.

Eine systemweite Installation ist nicht nötig. Die Dateien müssen mit dem
Programm verteilt werden.
