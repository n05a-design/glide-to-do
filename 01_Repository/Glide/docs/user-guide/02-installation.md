# Installation – Glide user guide

Status as of 20.11.2026 · Glide 1.0.1 · Task format 26

**Deutsch:** [Funktionen – Eigenständiger Start](../20_FUNKTIONEN.md#eigenständiger-start-3450), [§13 Bekannte Grenzen](../20_FUNKTIONEN.md#13-bekannte-grenzen), [technischer Schnellstart](../../README.md#schnellstart-aus-dem-quellstand) · [Guide contents](README.md) · Previous: [Getting started](01-getting-started.md) · Next: [Tasks and lists](03-tasks-and-lists.md)

> Controlled translation of the German function reference. If the texts differ, the German text applies.

## Availability

**No public installer has been released for Glide 1.0.1 yet.** No GitHub release or tag exists yet. The [project README](../../../../README.md#download) shows what is available today:

- **Run from source** on Windows, macOS and Linux (described below).
- **Development builds** for Windows x64 and macOS Apple Silicon from GitHub Actions. They need a GitHub sign-in. They carry no Windows certificate, or only an ad-hoc macOS signature. They are not a published installer.

The standalone development packages bundle Python, Tcl/Tk, fonts, templates, time zone data and the drag-and-drop libraries with their licenses. They need no separate Python. Which builds passed which checks is recorded only in the [QA report](../07_QA_BERICHT.md).

## Run from source

Requirements:

- Python **3.14 with Tk 9** is recommended. Python 3.12/3.13 and Tk 8.6 start with known limitations. Older versions are rejected with a message before Glide touches any data.
- No additional runtime packages.

From the repository root:

```text
cd 01_Repository/Glide
python3 src/glide/app.pyw
```

On Windows, use `python src\glide\app.pyw` for the second command. Keep the resources in `src/glide/resources` next to the application.

## Window size

The main window needs at least **860 × 700 px**. Compact mode (**View › Compact mode**, Ctrl/Cmd+Shift+K) works down to **480 × 560 px**. In small windows, controls that do not fit move into the "⋯" button, the context menu, the menu bar or a shortcut. They are never squeezed or cut off.

## Your data folder

Glide stores your content outside the program folder:

| Platform | Default data folder |
|---|---|
| Windows | `%APPDATA%/Glide` |
| macOS | `~/Library/Application Support/Glide` |
| Linux | `$XDG_DATA_HOME/Glide`, otherwise `~/.local/share/Glide` |

**Settings › Appearance & Controls › Change data folder …** (also **File › *Datenablage* › *Datenordner wechseln …***) moves to another folder. **File › *Datenablage* › *Wo liegen meine Daten?*** shows the current folder. The new folder must be empty, or it must already contain a Glide collection. If a folder you chose is not reachable when Glide starts, for example because a drive is not mounted, Glide shows the path and quits without creating anything. Details: [backups](10-backups.md) and [data and migration (German)](../06_DATA_BACKUP_MIGRATION.md#ablage).

A shared cloud folder does not merge changes made at the same time on several computers. Glide locks its data folder while a session can write. A second copy then opens read-only.

## Trying Glide safely

To explore Glide with synthetic data, use the [showcase (German)](../../../../05_Probelisten_Testdaten/Showcase/README.md). It uses its own data folder.
