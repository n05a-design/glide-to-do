# Backups – Glide user guide

Status as of 20.11.2026 · Glide 1.0.0 · Task format 26

**Deutsch:** [Funktionen – Sicherungsübersicht](../20_FUNKTIONEN.md#sicherungsübersicht-und-anhangsrückfrage-3450), [§11 Sicherungen](../20_FUNKTIONEN.md#11-import-ausgabe-und-austausch), [Daten und Migration](../06_DATA_BACKUP_MIGRATION.md#automatische-sicherungen) · [Guide contents](README.md) · Previous: [Import and export](09-import-and-export.md) · Next: [Keyboard shortcuts](11-keyboard-shortcuts.md)

> Controlled translation of the German function reference. If the texts differ, the German text applies.

## What is in your data folder

| File or folder | Contents |
|---|---|
| `liste_speicher.json` | Folders, lists, tasks, labels, repeat rules, reminders, trash, change history |
| `settings.json` | Design, profile, display, Home, pinboard layouts, sidebar placement |
| `vorlagen.json` | System and your own templates |
| `attachments/` | Local copies of attachments |
| `backups/` | Automatic backups and pre-backups |

Glide saves every change immediately and atomically. A half-written file never replaces the previous one. **File › Backups › Open backup folder** opens the backup folder.

## Automatic backups

- Glide checks every five minutes, and on saving after at least two minutes. When the content has changed, it writes `backups/liste_backup_*.json`.
- Glide keeps the ten newest backups, any others younger than 30 minutes (up to 40 in total), plus the last state of each day for 14 days.
- Before risky steps, Glide writes a **pre-backup** that is never rotated away. Such steps are a format upgrade, an import, applying an AI proposal and restoring.

A backup on the same disk does not replace an independent copy on another drive.

## Backup types

All of these are under **File › Backups**:

| Menu entry | Use |
|---|---|
| **Save task backup …** / **Load task backup …** | Task backup (`.glidebackup`): all tasks and attachments. Loading replaces the collection after validation and a pre-backup. |
| **Save full app backup …** / **Restore app backup …** | App backup: the task backup plus settings, templates and pinboard layouts. On restore you choose which areas to restore. |
| **Add lists/folders …** | Adds lists and folders from a backup with new IDs, without replacing anything. |

Templates travel separately as a template catalog (`.glidetemplates`, **File › *Vorlagen***). Pages and books can be saved as `.glidepage` ([Import and export](09-import-and-export.md)).

## Backup overview, comparing and restoring

- **Backup overview …** lists the files in the backup folder, newest first, and you can search them. **File …** adds an external backup file for this session. **Read** checks a backup's data part. **Compare** opens the comparison. **Restore …** starts the normal restore with confirmation and a pre-backup. Selecting an entry alone changes nothing.
- **Compare backups …** puts two states side by side: the current one, an automatic backup or a chosen file. It shows lists and tasks as new, removed, moved or changed. It is read-only.
- **Restore single page …** restores one page from a backup, with its text, images, cover, attachments and task links. Other pages stay unchanged.

## Storage status

**File › Backups › Storage status …** shows open save problems for tasks, settings, templates and automatic backups, and the size of the data files. **Save again** retries. A hint **Storage problem · details** stays at the bottom of the window until saving works again. Above 80 % of the 32 MiB budget, a *Sicherungsreserve · Details* (backup reserve) warning appears. Glide never deletes data on its own to make space. See [Troubleshooting](12-troubleshooting.md).

## Moving to another computer

Copy the whole data folder, or create an app backup and restore it on the other computer. Glide does not merge simultaneous changes from two computers in a shared cloud folder.
