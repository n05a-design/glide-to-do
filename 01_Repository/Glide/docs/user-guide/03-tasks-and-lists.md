# Tasks and lists – Glide user guide

Status as of 20.11.2026 · Glide 1.0.0 · Task format 26

**Deutsch:** [Funktionen §3 Erfassen](../20_FUNKTIONEN.md#3-erfassen), [§5 Liste, Tabelle, Gruppierung](../20_FUNKTIONEN.md#5-liste-tabelle-gruppierung), [Erweiterte Wiederholungsrhythmen](../20_FUNKTIONEN.md#erweiterte-wiederholungsrhythmen-fp-02-3440) · [Guide contents](README.md) · Previous: [Installation](02-installation.md) · Next: [Day planning](04-day-planning.md)

> Controlled translation of the German function reference. If the texts differ, the German text applies. The quick-entry words below are recognized **in German**; English words are not parsed yet.

## Capturing tasks

Type a title into the entry line and press Enter or the round **+** button. Shift+Enter opens the full entry form. **File › New › New task with all details …** opens it without the entry line. **Quick capture** (Ctrl/Cmd+Alt+N) works from anywhere in Glide.

The entry line and quick capture read dates and other details from the title. Each detected value appears as a chip below the line before you save. Click × on a chip to keep the text as plain title text.

| Typed (German) | Sets |
|---|---|
| `heute`, `morgen`, a weekday, `in 3 Tagen`, `24.12.` | Planned day |
| `fällig`, `bis` before a date | Due date |
| `14:30`, `14 Uhr` right after a date | Time of that date |
| `45 min`, `2h`, `1,5 Stunden` | Effort |
| `!hoch`, `!wichtig`, `!mittel`, `!niedrig` | Importance |
| `#Label` of an existing label | Label |
| `täglich`, `werktags`, `jeden Montag`, `alle 2 Wochen`, `monatlich am 15.` | Repeat rule (the first occurrence becomes the due date) |
| `erinnere 9 Uhr`, `Erinnerung 30 min vorher` | Reminder |
| `/morgen`, `/bis …`, `/wichtig`, `/Labelname` | Slash commands for the same fields |

Text in quotation marks is never parsed. Rules Glide cannot store stay plain text, and a muted hint names them. Tab completes a started `/` word. Escape hides the chips.

**Pasting several lines** asks whether to create one task per line (up to 200 lines, one undo step) or one task for all of it. Bullets, numbers and checkboxes are removed. `[x]` creates a completed task.

New items without a planned day go to the **Inbox**.

## Views: list, table and board

The switcher shows ☷ List, ⊞ Table and ▨ Pinboard. The open view is highlighted.

- **List display:** compact, standard, checklists (each step as a row), attachments, or extended with the start of the description.
- **Table:** choose and order columns per list, and click a heading to sort. In narrow windows, whole columns give way. The title column stays readable.
- **Grouping** works the same in list, table and board: by due date, planned day, importance, label, completed, list, or **urgency × importance** (Eisenhower). Dragging between groups, or Alt+←/→, sets exactly that field.

When items are selected, the footer shows a **selection bar** with count, importance, due, schedule, labels and delete.

## The task inspector

Double-click a task, or open it from Today, Coming up, a pinboard or a page, and the **task inspector** opens. It is one panel with every field, including attachments, relations and the checklist. **Save** or Ctrl/Cmd+S applies your changes. **Close** or Escape checks for unsaved input first. A successful edit is one undo step.

Clicking a visible planned day, due date, importance or label in a row opens exactly that picker. The "…" button next to a visible task opens its menu, including **Schedule** and **Due date**.

## Repeating tasks

The inspector offers weekly intervals on several days, monthly and yearly intervals, the nth or last weekday, the last day of the month and the last working day. Intervals range from 1 to 365. A preview shows up to five next dates.

- **From due date** keeps the fixed rhythm. **From completion** counts from the day you complete the task.
- **Pause series** stops creating new occurrences.
- **Occurrences incl. current** limits a series to 1–10,000 remaining occurrences.
- **Edit › Change task › Skip this occurrence** and **Skip missed occurrences** advance the series without completing it.

## Labels, filters and saved views

- **Labels** (Ctrl/Cmd+L, **Edit › Change task › Manage labels …**) group items in the Labels view. The label menu lists your five most recent labels first.
- **Saved filters** (**View › Interface › Saved filters …**) combine list, status, importance, labels, due date, planned day, effort, blocked/free and search text. Choose whether all conditions or at least one must match. Up to four filters can appear as Home tiles.
- In a saved filter, **Why is this here? …** in an item's context menu shows every condition with ✓ or ✗. **View › Interface › Explain filter …** counts the hidden tasks by the first condition they miss.
- **View › Interface › Save as view …** turns the current list, table or board into a saved view with its search, filter, grouping, sorting and columns.

## Cleaning up

- **Edit › Delete completed tasks** moves completed items to the trash after you confirm. Parents with open children stay.
- **Clear list** empties a list after you confirm. It is one undo step.
- Delete (on macOS also Backspace) moves the selected item to the trash. This works only while no text field has focus.
