# Pixel workshop – Glide user guide

Status as of 20.11.2026 · Glide 1.0.0 · Task format 26

**Deutsch:** [Funktionen §9 Pixel-Werkstatt](../20_FUNKTIONEN.md#9-pixel-werkstatt), [Bildfolgen](../20_FUNKTIONEN.md#bildfolgen-seit-3400), [Anzeigeprofile](../20_FUNKTIONEN.md#nachabnahme-3630-zeilenaktionen-aufschub-und-zeichenprofile) · [Guide contents](README.md) · Previous: [Pinboards](07-pinboards.md) · Next: [Import and export](09-import-and-export.md)

> Controlled translation of the German function reference. If the texts differ, the German text applies. **In the 1.0.0 baseline the drawing editor is still German.** Its English translation is in open pull requests [#157](https://github.com/n05a-design/glide-to-do/pull/157) and [#158](https://github.com/n05a-design/glide-to-do/pull/158). German labels are therefore given first on this page.

A **drawing** (*Zeichnung*) is a pixel canvas inside the main window. Its size is 16, 32, 64 or 128 cells per side and is fixed when you create it (**File › New › New drawing**).

## Tools

| Tool | Key |
|---|---|
| Brush (*Pinsel*) | B |
| Fill (*Füllen*) | F |
| Eyedropper (*Pipette*) | I |
| Line (*Linie*) | L |
| Rectangle (*Rechteck*) | U |
| Ellipse | E |
| Selection (*Auswahl*) | S |
| Symmetry (*Symmetrie*) | M |

Tool options set the size (1/2/4/8), outline or filled, symmetry and fill patterns. Shift keeps angles and squares.

## Colors

The left swatch is the foreground color, the right one the background color. X swaps them and D resets them. The color bar shows the palette and your seven most recent colors. Double-click or Shift+click a color in the bar to replace it in the whole drawing. You see a preview first: **Yes** applies it as one undo step, **No** discards it.

## View and reference

- Ctrl+mouse wheel zooms around the pointer. The middle mouse button pans. P shows a preview at original size. There are also a 3 × 3 tile preview and a grayscale preview.
- A **reference image** (PNG, JPEG, HEIC, SVG …) can be shown with adjustable opacity, reframed and traced.
- **Display profiles** (*Anzeigeprofil*): *Standard*, *Erweitert* (extended), *Animation* and *Bilder pixeln* (pixelate images) decide which tool rows are visible. Hidden functions stay under **More** (*Mehr*). The profile does not change the drawing.

## History and snapshots

Each action is an undo step, up to 50 steps. Up to 10 **named snapshots** (*Zwischenstände*) are stored as attachments.

## Animation

**Images …** (*Bilder …*) manages the frames: add, duplicate, delete and reorder, up to 120 frames of the same size. Each frame can have its own duration between 20 and 60,000 ms. **Play …** (*Abspielen …*) shows a copy of the sequence and changes nothing. In the Standard profile, both are under **More › Image sequence** (*Mehr › Bildfolge*).

## Palettes and export

- The **Glide 32** palette is included. Save your own palettes and import or export them as `.gpl`/`.hex`. You can also import Adobe Swatch Exchange and Aseprite palettes (up to 256 colors).
- **PNG:** scaled by whole numbers without smoothing, up to 2,048 px.
- **ICO:** 16/32/48/256 px, optionally with a transparent background. You see a pixel-exact preview before saving.
- **Glide SVG** and **JSON** for a lossless round trip.
- **Image sequence:** a PNG sprite sheet, or single PNG frames, with a JSON timeline. Glide does not export GIF.

## Pixel icons

A 16 × 16 drawing can serve as the **pixel icon** of a list, page or folder. It appears in the sidebar, in overviews and in search. Unpainted cells are transparent.
