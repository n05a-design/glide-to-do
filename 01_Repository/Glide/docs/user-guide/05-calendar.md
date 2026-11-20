# Calendar – Glide user guide

Status as of 20.11.2026 · Glide 1.0.0 · Task format 26

**Deutsch:** [Funktionen – Kalender im Tagespaket](../20_FUNKTIONEN.md#tagespaket-33314-au01-au03-g05au05-h-02), [Tagesplanung 3.39.0](../20_FUNKTIONEN.md#tagesplanung-3390), [§11 Kalenderdatei](../20_FUNKTIONEN.md#11-import-ausgabe-und-austausch) · [Guide contents](README.md) · Previous: [Day planning](04-day-planning.md) · Next: [Pages and notes](06-pages-and-notes.md)

> Controlled translation of the German function reference. If the texts differ, the German text applies.

Glide has its own week and month calendar for your tasks. It can also read a local calendar file as busy time. **Glide does not sync with any calendar service.** Every calendar file it reads or writes is a file you choose yourself.

## Week and month view

Ctrl/Cmd+K or **View › *Ansichten* › *Kalender …*** opens the calendar inside the main window.

- Switch between **week** and **month**, and move with the previous, today and next buttons. The week starts on the day set under **Settings › Appearance & Controls › Week starts on**.
- Each day shows the same balance as Today: estimated effort including completed tasks, missing estimates, and the free time left. A capacity of 0 counts as "not set".
- The day menu opens existing tasks, or creates a new task with that planned day or with an explicit due date.
- Select one or more tasks, then pick a day and press Enter, or drag them onto a day. Only the planned day changes, and one undo step covers all source lists.
- The month view shows the local moon phases.

## Finding a free time slot

*Freies Zeitfenster* (free time slot) needs a selected open task with an effort estimate. It shows gaps between 08:00 and 18:00. The gaps account for Glide time blocks and your local busy-time calendar. Confirming sets the planned day and time and keeps the due date. If the calendar source is unknown or faulty, Glide shows no free slot rather than an unreliable one.

## Calendar as busy time

**Calendar as busy time …** (in Settings; in the View menu and the palette as *Kalender als Belegzeiten …*) reads one local `.ics` file that you select. After saving, its events reduce your daily capacity in the grid, Today, the week and month view, suggestions, the Home balance and *Tag entlasten* (relieve day).

- Single and all-day events are evaluated within limited bounds. So are daily, weekly, monthly and yearly series, RDATE/EXDATE, single exceptions and time zones including daylight saving time.
- Transparent and cancelled events block no time. Overlapping events count once.
- Unsupported rules are reported. Glide then counts only the single event and does not invent a series.
- Glide never creates tasks from this file and never changes it. Use *Neuladen* (reload) after the file changes.

## Importing and exporting calendar files

- **File › Import › *Kalenderdatei (ICS) importieren …*** creates **tasks** from events, with a preview first. You can choose options for descriptions, locations, categories as labels, reminders, duration as effort and skipping cancelled events. Repeat rules become one repeating task. UIDs prevent duplicates.
- **File › Export › *Kalenderdatei (ICS) …*** writes a read-only `.ics` file of your tasks. See [Import and export](09-import-and-export.md).
