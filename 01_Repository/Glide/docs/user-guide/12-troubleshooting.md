# Troubleshooting – Glide user guide

Status as of 20.11.2026 · Glide 1.0.2 · Task format 26

**Deutsch:** [Funktionen – Speicherstatus](../20_FUNKTIONEN.md#speicherstatus-und-sicherungsreserve-wa-40wa-47-seit-3450-geliefert), [Schreibbesitz](../20_FUNKTIONEN.md#schreibbesitz-und-mehrfachaktionen-roadmap-paket-1), [§13 Bekannte Grenzen](../20_FUNKTIONEN.md#13-bekannte-grenzen), [Wiederanlauf](../06_DATA_BACKUP_MIGRATION.md#abgesicherter-wiederanlauf-nach-absturz-lokaler-kandidat-3490) · [Guide contents](README.md) · Previous: [Keyboard shortcuts](11-keyboard-shortcuts.md)

> Controlled translation of the German function reference. If the texts differ, the German text applies.

## Glide does not start

- **"Python or Tk is too old":** Glide needs Python 3.12 or newer with Tk 8.6 or newer. Python 3.14 with Tk 9 is recommended. See [Installation](02-installation.md).
- **The data folder is not reachable:** if the chosen folder cannot be created, Glide shows its path and quits without creating anything. This happens, for example, when a drive is not mounted. Mount the drive and start again. Glide does not silently switch to the default folder.

## Glide opens read-only

Glide protects your data instead of overwriting it. It opens read-only and names the reason when:

- **another Glide window or computer is using the same data folder.** The lock file `glide.lock` allows only one writing session. Close the other session.
- **the data was written by a newer Glide version.** Use that newer version.
- **Glide ended unexpectedly last time.** Glide first checks the data read-only. Release it in **File › Backups › Storage status …**. Glide then checks again and keeps a byte-identical copy of the original before writing.
- **a data file exceeds 32 MiB.** Check the file outside Glide and restart.

Before Glide replaces an unreadable file, it keeps a copy in `backups/`. It never replaces missing or invalid data with an empty collection without telling you.

## A save failed

The hint **Storage problem · details** appears at the bottom of the window. Open it, or use **File › Backups › Storage status …**, to see which area failed. Then use **Save again**. The hint stays until that area saves successfully. Autosave never interrupts your work with dialogs.

## Restoring older content

- An item you deleted is in the **Trash**.
- To undo a recent change, use Undo (Ctrl/Cmd+Z). The **change history** (Ctrl/Cmd+H) lists changes.
- To go further back, use **Compare backups …** or **Restore single page …**. See [Backups](10-backups.md).

## Reminders did not appear

Reminders and daily prompts are delivered **only while Glide is running**. Missed ones are collected and shown later. System notifications are optional. When Glide runs from Python, they appear under "Python"; only the packaged app shows them under "Glide".

## Something looks wrong

- **German text in the English interface:** the whole interface is translated; names of your own content stay as you wrote them. If you still find German text, see [Interface language](README.md#interface-language). Please report it with the [localization issue form](https://github.com/n05a-design/glide-to-do/issues/new?template=lokalisierung.yml).
- **No image preview:** supported formats depend on your system. On Linux, previews need a system tool such as `gdk-pixbuf-thumbnailer`. SVG previews need Tk 9.
- **Long sidebar titles cut off on Windows:** a known open issue.
- **Window opens off-screen:** Glide pulls a window back onto a visible screen at start-up.

## Help inside Glide

- **Help › Manual …** (F1) and **Help › Show keyboard shortcuts** explain the app in the chosen language.
- **Help › Open error log** opens the local error log. If no error has occurred, Glide says so.
- Nothing from these help functions leaves your computer.

## Reporting a problem

Use the [bilingual issue forms](https://github.com/n05a-design/glide-to-do/issues/new/choose) and include **synthetic example data only**, never your own content. Report security vulnerabilities confidentially as described in the [security policy](../../../../SECURITY.md).
