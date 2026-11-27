# Getting started – Glide user guide

Status as of 24.11.2026 · Glide 1.0.3 · Task format 26

**Deutsch:** [Funktionen §1 Grundbegriffe](../20_FUNKTIONEN.md#1-grundbegriffe), [§2 Seitenleiste und Navigation](../20_FUNKTIONEN.md#2-seitenleiste-und-navigation), [§7 Startseite](../20_FUNKTIONEN.md#7-startseite) · [Guide contents](README.md) · Next: [Installation](02-installation.md)

> Controlled translation of the German function reference. If the texts differ, the German text applies. The interface is available in English; see [Interface language](README.md#interface-language).

Glide is a local desktop planner. Your tasks, pages, notes, pinboards and drawings live in one data folder on your computer. You need no account, internet connection or cloud service.

## Content types

When you create something in Glide, you choose its type. The type cannot be changed later.

| Type | What it is |
|---|---|
| **Task list** | Items shown as a list, table or pinboard. A list created as a pinboard opens as a free canvas. |
| **Page** | A long document with real tasks inside. Pages have no sub-pages. |
| **Note** | Rich text with a task area above it. |
| **Drawing** | A pixel canvas of 16, 32, 64 or 128 cells per side. |
| **Gallery** | A collection of images stored as attachments. |

Folders come in three kinds: a normal **folder**, a **book** (new entries are pages) and a **notebook** (entries are sorted by their date). Subfolders inherit the kind of a book or notebook.

A list contains **items** of four kinds: **task**, **long text** (multi-line), **group** and **subheading**. Groups and subheadings structure a list. They have no planning fields and no checklist.

## Due date and planned day

Glide keeps two dates apart:

- The **due date** says when something must be finished.
- The **planned day** says when you intend to work on it.

A task can also have effort, tracked time, importance, labels, a color, a repeat rule, reminders, attachments and relations (**linked with**, **waiting for**). A checklist holds up to 50 steps of up to 200 characters each. Ticking a step does not complete the task.

New and renamed titles of lists, pages, notes, folders, templates and tasks are limited to 40 characters. A counter in the field shows how many characters are left.

## Undo, redo and trash

- Every action is one undo step, including imports, dragging and bulk changes. **Edit › Undo** or Ctrl/Cmd+Z.
- **Edit › Redo**, Ctrl/Cmd+Shift+Z (on Windows also Ctrl+Y) redoes up to 20 undone steps. Redo is kept only in memory. A new change or a restart clears it.
- Deleted content goes to the **Trash**. You can restore it there. The trash keeps up to 200 entries, newest first.

## Sidebar

The sidebar shows system rows: **Home**, **Today**, **Labels**, **Templates** and **Trash**. The **Inbox** row appears only when it has content. Below them are four sections in this order: **Pages**, **Lists**, **Notes** and **Drawings**. You can hide Pages, Notes and Drawings. Hidden content stays reachable under Lists.

- Drag entries to reorder them, or drop them onto a folder to move them in. Dragging an item onto **Today** plans it for the day shown.
- Alt+↑/↓ moves the selected row among its siblings, Alt+→ moves it into the folder above, Alt+← moves it up one level. Every move can be undone.
- Up to 20 pages can be **pinned** from their context menu.
- **View › Interface › Narrow sidebar** shows a 64 px icon strip instead of the trees.

## Home

**Home** is an adaptive Bento grid of cards (1 to 3 responsive columns with breakpoints at 616 px and 932 px, based on the Glide Bento Box System 0.1.0). The default layout "Calm" shows Today, Gismo, the next seven days, recently edited items, a pinboard preview, drawings, gallery images and pinned items. You can add more tiles, such as the clock, next task, templates, calendar preview, overdue items, progress, labels and pinned filters.

- **Two columns** (development state 1.1.0, Glide Bento 0.2.0): in **Customize home**, a tile can span two of three columns at its place in the order (**Two columns**, back with **One column**). With two columns it spans the full width at its place, with one column it is normal. **Full width** still puts a tile above the grid.
- **Empty states** (development state 1.1.0): if all tiles are hidden, a card offers **Set up home …** and **Show default tiles**. Empty lists, Today, the page overview, boards and notebooks name their state and the next step; there is no first-run wizard or tour.
- **Customize home**, below the tiles, lets you drag, hide and resize tiles. **Settings › Appearance & Controls › Configure Home …** offers **Restore default**.
- After an update, a "New in Glide" card lists what changed in the last three versions with entries. **Help › About Glide › What's new …** keeps the full history.
- **Gismo** is Glide's drawn companion. His mood mirrors your task collection, not you. Hide his tile if you do not want him.

## Search and the command palette

Ctrl/Cmd+O or the magnifier in the header opens search. It finds pages, items and actions. From two characters on, it also searches page and note text and descriptions. Case and the German umlaut spellings (ä/ae, ö/oe, ü/ue, ß/ss) are treated as equal. Type `>` to show only actions. Search is a palette of all app actions too.

## Where to go next

- [Install and start Glide](02-installation.md).
- [Create tasks and lists](03-tasks-and-lists.md).
- [Plan your day](04-day-planning.md).
