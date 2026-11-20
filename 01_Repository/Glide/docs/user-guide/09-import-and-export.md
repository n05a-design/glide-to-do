# Import and export – Glide user guide

Status as of 20.11.2026 · Glide 1.0.0 · Task format 26

**Deutsch:** [Funktionen §11 Import, Ausgabe und Austausch](../20_FUNKTIONEN.md#11-import-ausgabe-und-austausch), [Austauschformat](../06_DATA_BACKUP_MIGRATION.md#austauschformat-glideexchange) · [Guide contents](README.md) · Previous: [Pixel workshop](08-pixel-workshop.md) · Next: [Backups](10-backups.md)

> Controlled translation of the German function reference. If the texts differ, the German text applies. Most import, export and exchange menu entries are still German; see [how this guide names controls](README.md#interface-language).

**Principles:** every import shows a preview first and is one undo step. An import never overwrites existing items; it only adds new ones. The single exception is a reviewed AI change proposal (see below). Exports write to a file or folder you choose. They never write into Glide's own data files.

## Import

All imports are under **File › Import**.

| Menu entry | What happens |
|---|---|
| **Import TXT …** / *TXT als neue Liste(n) …* | Lines become items in the open list, or new lists. |
| *CSV importieren …* | Glide detects the encoding, separator and header. You map columns, and values such as done, importance, kind, minutes and level are checked. The target is a new list or the open one. |
| *Kalenderdatei (ICS) importieren …* | Events become tasks; see [Calendar](05-calendar.md#importing-and-exporting-calendar-files). |
| *Zeichnung (SVG/JSON) importieren …* | A Glide drawing file becomes a new drawing. |
| *Seite aus Datei …* / *Seite aus Zwischenablage* | Markdown becomes a page. Local images become page images. |
| *Notion-Export übernehmen …* | A "Markdown & CSV" ZIP from Notion. Nothing is preselected: you choose each page. Pages you changed in Glide need an extra conflict release. CSV databases stay in the original archive, which is kept as an attachment. Glide does not sync live with Notion. |
| *Glide-Seiten importieren …* | Pages and books from `.glidepage`, with their attachments and new IDs. |

## Export

Exports are under **File › Export**, in a page's **More** menu, or in the drawing editor.

| Menu entry | Contents |
|---|---|
| **As TXT … / As Markdown … / As CSV …** | The open list. |
| *Alles als Markdown-Ordner …* (everything as a Markdown folder) | All lists, pages, notes, galleries and drawings, including archived ones. Files are sorted into folders like the sidebar. The folder also contains CSV tables, PNG drawings, `INDEX.md`, `INVENTAR.json` with all fields and `MANIFEST.json` with SHA-256 checksums. It is a readable copy of your content. It is **not** a guaranteed re-import path; use an app backup to restore. |
| *Als Glide-Seite …* | A `.glidepage` file. |
| **Pinboard as JSON Canvas (.canvas) …** | See [Pinboards](07-pinboards.md#export-as-json-canvas). |
| *Kalenderdatei (ICS) …* | A read-only calendar file of your tasks. Glide does not sync it. |
| *Drucken und PDF …* (Ctrl/Cmd+P) | A self-contained HTML page with no external references. Print it from your browser or save it as PDF. |

On Windows, keep the chosen target path at 130 characters or shorter, so that exported paths stay within 240 characters.

## Working with AI tools

Glide itself never contacts an AI service. You exchange files with a tool of your choice, under **File › *Datenaustausch*** (data exchange):

- *Für KI bereitstellen …* (provide for AI) writes a `.glideexchange` request or a `.glidecontext` package, or copies it to the clipboard. It contains your selected context, instructions and the response schema. Five built-in instructions help, for example splitting a note into tasks or suggesting labels. You can also write your own instructions. *Vorschau …* (preview) shows the exact content before anything leaves the dialog.
- *KI-Ergebnis importieren …* (import AI result) reads the answer. New tasks are added after a preview. A change proposal is checked field by field and marked applicable, conflict, not found or invalid. Only applicable changes are applied, after an automatic pre-backup, as one undo step.
- *Austauschformat anzeigen …* shows the exchange format specification.
- *KI-Skill exportieren …* exports the **`glide-to-do` agent skill**. It lets AI agents with skill support prepare Glide import files. Installation for each agent is in the [skill README](../../skills/glide-to-do/README.md).
