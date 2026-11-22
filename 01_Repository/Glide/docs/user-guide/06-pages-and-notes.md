# Pages and notes – Glide user guide

Status as of 20.11.2026 · Glide 1.0.1 · Task format 26

**Deutsch:** [Funktionen §8 Seiten, Notizen, Notizbuch, Galerie](../20_FUNKTIONEN.md#8-seiten-notizen-notizbuch-galerie), [Arbeitsmodi und Seitenbedienung](../20_FUNKTIONEN.md#arbeitsmodi-und-seitenbedienung-d55-seit-3450-geliefert), [Aufgaben im Wissen](../20_FUNKTIONEN.md#aufgaben-im-wissen-33315-g29g31g32), [Seiten im Alltag](../20_FUNKTIONEN.md#seiten-im-alltag-33318-g28g09u08) · [Guide contents](README.md) · Previous: [Calendar](05-calendar.md) · Next: [Pinboards](07-pinboards.md)

> Controlled translation of the German function reference. If the texts differ, the German text applies.

## Pages

A **page** is a long document with a reading column of up to 760 px. It scrolls without end and has no sub-pages. Its title is the title in the header. Double-click the header title to rename the page.

- **Markdown shortcuts** work while you type. **/** at the start of a line opens the block picker. Enter continues lists and tasks.
An open page shows when it was last edited in the header. Hover over the time or choose **More › Show last edit time …** to see the exact local date, time and UTC offset. The menu also works when the header is too narrow.

- **Blocks:** headings 1–4, bulleted and numbered lists, tasks, quote, code, divider, table, indents, toggle list, toggle heading and callout.
- **Block actions:** Ctrl/Cmd+/ or the ⠿ handle left of a line. Drag the handle to move a block, or press Escape to cancel. A floating format bar appears over selected text.
- **More** opens a searchable list of every page action. Disabled entries say why they are disabled.
- **Images:** insert them from the toolbar, with "/" or by dragging from Finder/Explorer. Align them left, center or right with text wrap, and resize them from the corner.
- **Cover image** and **pixel icon:** **More › Cover image** and **More › Pixel icon …**.
- **Live list:** **More › Embed live list …** shows the original tasks of another list on the page. You can tick them off there.
- **Print and PDF:** **More › Print and PDF …** opens an A4 print page in your browser, with images embedded.

## Real tasks inside text

A task in a page or note is a **real task**, not a copy:

- Tick it off in the text, or double-click it to open the inspector. A title change in either place updates the other.
- **Link task …** inserts an existing task as a reference. It stays in its home list.
- **Move to list …** moves a task from the text into a task list. The text line becomes a reference.
- Deleting a home line moves the task to the trash. Deleting a reference line removes only the reference.

## Links, backlinks and mentions

- Type **@** at the start of a word to link a page, list or task. Ctrl/Cmd+click opens the target. Ctrl/Cmd+Shift+click opens it in the read-only **side view**.
- **View › References and backlinks** lists outgoing links and the pages that link here.
- **Mentioned without reference** below the text finds your title in other content when you expand it. **Link** connects such a mention explicitly.
- **View › *Fundorte anzeigen …*** (show usages) lists every place that uses a task or list.

## Side view

The **side view** shows a list, page or note read-only next to your work. Open it from the sidebar context menu (**Open in side view**), with Shift+Enter on a search result, or via **View › Interface › Open side view …**. It has its own search (Ctrl/Cmd+F), a history (Alt+←/→) and section jumps (Alt+↑/↓).

## Notes and notebooks

- A **note** uses the same editor with real tasks and links. Its task list appears with the first item. **More** offers a timestamp, a day section and a writing prompt.
- A **notebook** holds dated notes and dated drawings, sorted by date, with favorite, mood, place and writing prompt under **More**. Templates include a daily note, gratitude, a weekly review and a year folder with quarters.

## Galleries

A **gallery** is an image collection. Each image is an attachment with a title and a note. Images appear as tiles in three sizes and open in a large view where you can page through them.

## Markdown and templates

- Pages come in with **Paste**, **File › Import › Page from file …** or **Page from clipboard**. They go out with **More › Save as Markdown …** and **Copy page**. Local images make the round trip. Web addresses are never loaded.
- **`.glidepage`** exports and imports pages and books with their attachments.
- **From template …** shows a filled-in preview before anything is created. Placeholders such as `{{Datum}}` fill in automatically. Other names are asked for. The built-in page templates are German: report, meeting and project page.
