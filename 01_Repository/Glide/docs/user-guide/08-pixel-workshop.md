# Pixel workshop – Glide user guide

Status as of 24.11.2026 · Glide 1.0.3 · Task format 26

**Deutsch:** [Funktionen §9 Pixel-Werkstatt](../20_FUNKTIONEN.md#9-pixel-werkstatt), [Bildfolgen](../20_FUNKTIONEN.md#bildfolgen-seit-3400), [Anzeigeprofile](../20_FUNKTIONEN.md#nachabnahme-3630-zeilenaktionen-aufschub-und-zeichenprofile) · [Guide contents](README.md) · Previous: [Pinboards](07-pinboards.md) · Next: [Import and export](09-import-and-export.md)

> Controlled translation of the German function reference. If the texts differ, the German text applies.

A **drawing** is a pixel canvas inside the main window. Its size is 16, 32, 64 or 128 cells per side and is fixed when you create it (**File › New › New drawing**).

## Tools

| Tool | Key |
|---|---|
| Brush | B |
| Fill | F |
| Eyedropper | I |
| Line | L |
| Rectangle | U |
| Ellipse | E |
| Selection | S |
| Symmetry | M |

Tool options set the size (1/2/4/8), outline or filled, symmetry and fill patterns. Shift keeps angles and squares.

## Colors

The left swatch is the foreground color, the right one the background color. X swaps them and D resets them. The color bar shows the palette and your seven most recent colors. Double-click or Shift+click a color in the bar to replace it in the whole drawing. You see a preview first: **Yes** applies it as one undo step, **No** discards it.

## View and reference

- Ctrl+mouse wheel zooms around the pointer, and the **Zoom** menu offers zoom in, zoom out and fit to canvas. The middle mouse button pans. **Preview** (P) shows original size, with **Tile** (3 × 3) and **Grayscale** previews.
- A **reference image** (PNG, JPEG, HEIC, SVG …) can be loaded (**Load image**), shown with adjustable opacity, reframed (**Reframe**) and traced (**Trace pixels**).
- **Display profiles:** **Standard**, **Extended**, **Animation** and **Pixelate** decide which tool rows are visible. Hidden functions stay under **More**. The profile does not change the drawing.

## History and snapshots

Each action is an undo step, up to 50 steps. Up to 10 **named snapshots** are stored as attachments.

## Animation

**Frames …** manages the frames: add, duplicate, delete and reorder, up to 120 frames of the same size. Each frame can have its own duration between 20 and 60,000 ms. **Play …** shows a copy of the sequence and changes nothing. In the Standard profile, both are under **More › Animation**.

## Palettes and export

- The **Glide 32** palette is included. Save your own palettes and import or export them as `.gpl`/`.hex`. You can also import Adobe Swatch Exchange and Aseprite palettes (up to 256 colors).
- **PNG:** scaled by whole numbers without smoothing, up to 2,048 px.
- **ICO:** 16/32/48/256 px, optionally with a transparent background. You see a pixel-exact preview before saving.
- **Glide SVG** and **JSON** for a lossless round trip.
- **Image sequence:** a PNG sprite sheet, or single PNG frames, with a JSON timeline. Glide does not export GIF.

## Pixel icons

A 16 × 16 drawing can serve as the **pixel icon** of a list, page or folder. It appears in the sidebar, in overviews and in search. Unpainted cells are transparent.
