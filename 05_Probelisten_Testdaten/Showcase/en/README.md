# City Light · Glide showcase

Status as of 24.11.2026 · Glide 1.0.3 · Task format 27 · Templates 2 · [Deutsche Fassung](../README.md)

A photo journey through seven cities: Wuppertal, Berlin, Munich, Vienna, Monaco, Bilbao and Seoul. Two weeks by train and two flights, followed by the selection for a small travel book. The showcase presents the same data from many angles: travel plan, a travel guide with one page per city, a travel diary, a gallery, a pixel stamp and three pinboards.

All photos were taken by Tim von Trostorff (shaye Design) and, like the source code, are licensed under the Mozilla Public License 2.0 ([LICENSE](https://github.com/n05a-design/glide-to-do/blob/main/LICENSE)); Tim von Trostorff remains the author. The [source record](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/tests/fixtures/showcase/quellen.json) lists the original and checksum of every working copy.

## Open and edit

From the project folder, run `py -3.14 05_Probelisten_Testdaten/Showcase/en/Showcase_starten.pyw` (Windows) or `python3 05_Probelisten_Testdaten/Showcase/en/Showcase_starten.pyw` (macOS). On first launch the starter loads the app backup into the folder `Workspace-City-Light`; your own changes stay there. The sample data refers to Friday, 20 Nov 2026. You can select this day directly in Today and Calendar.

| File | Use |
|---|---|
| [Glide-Showcase_App.glideapp](Glide-Showcase_App.glideapp) | Complete example with home, global pinboard, settings and travel diary. For a separate data folder. |
| [Glide-Showcase.glidebackup](Glide-Showcase.glidebackup) | Editable project to add to existing data via **File → Add lists/folders …**. |
| [Glide-Showcase.glidetemplates](Glide-Showcase.glidetemplates) | Evening note with date and city fields, plus the recurring checklist for every change of city. |
| [City-Light.canvas](City-Light.canvas) | JSON Canvas 1.0 from the global pinboard with cards, an area and labelled connections. |
| [manifest.json](manifest.json) | Documents, format version and SHA-256 of the four files. |

## A tour of the features

- **Travel guide (book):** The overview page has a pixel drawing as its cover, a page icon, a route table, a quote, a divider, tasks, a collapsed block with packing tips and an embedded live list of the travel plan. Each of the seven city pages carries its photo as cover and in the text (right, left or centred), a table of places, times and tips, a quote, a callout, a code block with camera settings and tasks. The **Travel kitty** page shows a plain cost table without a cover.
- **Project pinboard:** Four regions as areas (Germany, Austria, Mediterranean and Atlantic, Korea) and an "After the journey" area. The city pages are connected as cards; the connections carry the legs ("ICE · 3 h", "Flight to Nice"), flights dashed. The **global pinboard** has its own area, a line background and four labelled connections; export it as JSON Canvas from the pinboard menu. The **travel plan** also appears as a column pinboard by planned day.
- **Travel plan:** headings, long text, a group with subtasks, importance, due date with time, planned day and time, effort and time spent, checklists, dependencies, links, a mention of the gallery, a fixed reminder, attachments and coloured labels. On 20 Nov more minutes are planned than there is capacity; **Lighten the day** moves work to other days.
- **Photo routines** show every repeat type, series on the last weekday and the second Tuesday, interval after completion, a limited count and a paused series. **Before every change of city** is a recurring checklist.
- **Gallery "City Light · Selection"** with 14 photos, titles and captions in large tiles. The **evening round** is a note with tasks, an attachment and references to a task, a page and the gallery.
- **Travel diary (notebook):** one dated entry per city with place, mood, prompt and favourites, plus the evening after coming home.
- **Pixel workshop:** the travel stamp changes its sky colour from morning to night across four frames, with a PNG reference, a 16-pixel icon and the palette as GPL and HEX.
- Also: two saved views (approvals, Eisenhower week as a table), pinned pages, favourites, tabs, a custom AI task, an archived folder with the first route and two items in the inbox.

## Update

In `01_Repository/Glide`, generate both languages:

```
python3 -B tests/tools/showcase.py --tag 2026-11-20
python3 -B tests/tools/showcase.py --tag 2026-11-20 --sprache en
```

`python3 -B scripts/pflege/showcase_abgleich.py` checks both versions through import, templates, references, export and restart, and copies them to `05_Probelisten_Testdaten/Showcase` and `…/Showcase/en`.
