# Pinboards – Glide user guide

Status as of 24.11.2026 · Glide 1.0.3 · Task format 27

**Deutsch:** [Funktionen §6 Pinnwand](../20_FUNKTIONEN.md#6-pinnwand), [JSON-Canvas-Export](../20_FUNKTIONEN.md#fundortübersicht-json-canvas-10-und-themengerechte-steuerelemente-3540-10112026) · [Guide contents](README.md) · Previous: [Pages and notes](06-pages-and-notes.md) · Next: [Pixel workshop](08-pixel-workshop.md)

> Controlled translation of the German function reference. If the texts differ, the German text applies.

A **pinboard** (called **Board** in the interface) is a view of the tasks of a list, a folder or your whole collection. It is not a separate content type. A card is the original task, and editing the card edits the task. There is a board per list, per folder and one **global board**.

## Layouts

The toolbar button with the current name opens the layout menu:

- **Free arrangement** (default): place cards anywhere.
- **Ordered cards.**
- **Column board:** columns grouped as in a [list](03-tasks-and-lists.md#views-list-table-and-board), for example by importance or label. Dragging a card to another column sets that field. Double-click a column to create an item with its value. *Hide empty columns* and *Only open* are in the More menu.

## Cards

- A card's height follows its content: title, status, date, a checklist with five tickable steps, description, image, labels and source.
- Card size (large, normal, small) and color (stripe, header or full card) belong to the card, not to the task.
- **Pin all items** adds every item. **Auto** silently pins new items.
- Pages, notes and drawings can be pinned as cards, from their sidebar menu or by dragging. The card shows the title, icon or cover, an excerpt and the number of open tasks. Double-click opens the original.
- Ctrl/Cmd+Enter on a card opens a title field next to it, optionally connected, for "thinking further". Double-click opens the task inspector.

## Connections and areas

- **Connections** link two cards (one per pair). They can be a plain line or an arrow in either or both directions, with a label of up to 40 characters, dashes and a color. Drag from the handle at a card's edge to connect.
- **Areas** are named rectangles (up to 50). Cards whose center lies inside move with the area. Areas exist only in free arrangement.

## Working on the board

- Ctrl/Cmd+click selects several cards in order. Connect, complete, resize and remove act on the selection.
- Arrow keys select the next card, Home/End the first and last, and Enter opens it. Alt+arrows move the selected card by one grid step. In the column board, Alt+←/→ moves the card to the next column and sets its field.
- F11 or **Full screen** switches to full screen. Escape leaves step by step: connecting, then full screen, then the board.
- Shift+mouse wheel or the trackpad scrolls sideways. A pressed middle button drags the canvas. **Tidy up** arranges the selection in a grid.
- Backgrounds: dots, lines or grid.
- **Present** shows the areas as full-screen slides. **Presentation as PDF …** opens a print page with one A4 landscape page per area.

Every move, connection and area change is one undo step.

## Where board layout is stored

Positions, connections and areas are stored in your settings, not in the task data. A full **app backup** includes them. A task-only backup does not. See [Backups](10-backups.md).

## Export as JSON Canvas

**Area › As JSON Canvas (.canvas) …** on the board, or **File › Export › Pinboard as JSON Canvas (.canvas) …**, writes the open board in the open JSON Canvas 1.0 format. Areas, cards and connections keep their positions. A report afterwards lists what the format cannot hold: interactive checklists, repeat rules, reminders, attachments and pixel data.
