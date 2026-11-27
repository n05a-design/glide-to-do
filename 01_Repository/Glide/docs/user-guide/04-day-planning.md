# Day planning – Glide user guide

Status as of 24.11.2026 · Glide 1.0.3 · Task format 26

**Deutsch:** [Funktionen §4 Heute, Demnächst und Planung](../20_FUNKTIONEN.md#4-heute-demnächst-und-planung), [Tageskapazität und Entlastung](../20_FUNKTIONEN.md#tageskapazität-und-entlastung-seit-3550), [Tagespaket](../20_FUNKTIONEN.md#tagespaket-33314-au01-au03-g05au05-h-02) · [Guide contents](README.md) · Previous: [Tasks and lists](03-tasks-and-lists.md) · Next: [Calendar](05-calendar.md)

> Controlled translation of the German function reference. If the texts differ, the German text applies.

## Today

**Today** shows each task exactly once, in these sections:

| Section | Contents |
|---|---|
| Next task | One task: planned for today, otherwise overdue or due today, otherwise left over |
| Overdue | Past due date, not planned for today |
| Left over | Planned for an earlier day, still open, not overdue |
| Day plan | Planned for today, with a timed schedule and an untimed part |
| Due today | Due today but not planned |
| Routines | Selected repeating checklists with their open steps |
| Inbox | Items without a planned day (up to 50) |

Use ◂/▸ to look at other days. **Clear day** removes the planned day from its tasks and keeps the tasks themselves.

**Coming up** lists every task with a due date in time order, overdue first. It is reached from Today, **View › Views › Coming up**, search and Home.

## Scheduling

**Schedule** sets only the planned day. Due date, effort, time, repeat rule and attachments stay unchanged. It is available from the context menu, the selection bar, the "…" row button, Ctrl/Cmd+Shift+P and the command palette. The targets are Today, Tomorrow, Weekend, Next week, Date … and No day. The menu shows the actual date and the free time left on that day.

## Available time and capacity

Set a **daily capacity** in minutes, globally or per weekday, in **Settings** (**Daily capacity** and **Capacity by weekday**). The day balance shows:

- free time left, or the time you are over-planned (for example "45 min overplanned"),
- time blocked by calendar events (see [Calendar](05-calendar.md)),
- how many tasks have no estimate. Missing estimates are counted separately, not as zero minutes.

Completed tasks still count towards the day. A capacity of 0 means "not set". Over-planning is allowed.

## Schedule and hourly grid

Tasks with a time appear first. Dragging sets the time, and Alt+↑/↓ moves a block by 15 minutes. The **grid** shows 6:00–22:00 with a red line for now. Drag tasks onto it in 15-minute steps. **Set time block …** (Ctrl/Cmd+Shift+T) sets date and time in a dialog. Overlaps are named, not moved.

## Suggestions and relief

- **What fits today?** (**View › Views**) suggests overdue, due, left-over, soon-due and important tasks. It also suggests tasks whose completion unblocks others. Each row shows the reason, source list and effort. Accepting sets only the planned day.
- **Lighten the day …** (**View › Views**) shows a before/after balance. You choose a new day, or the backlog, for marked tasks. Under the balance, each over-planned day gets a line with its reasons. Nothing changes until you press **Reschedule**, and the whole change is one undo step.

## Tasks past their due date

Development state 1.1.0. **Late** shows a calm line at the top: how many open tasks are past their due date and how old the oldest is. Nothing moves on its own.

- **Plan for today** sets only the workday of these tasks to today. The due date stays and remains visible. One undo step.
- **Reset due dates …** asks for a new date from today on, names the number of tasks and the recurring tasks it leaves unchanged, and changes the due dates only after you confirm. One undo step.
- The **Late** home tile also offers **Plan for today**.

## Starting and ending the day

The **Day …** switch in Today and **View › Views** offer two modes:

- **Day start** walks through overdue tasks, left-over tasks and the Inbox.
- **Day close** shows what you completed, moves left-over tasks to tomorrow and can add a note to your notebook.

The **Week review** compares estimated and tracked time per day.

**Daily prompts** (**Settings › Daily prompts …**, or **View › Views › Set up daily hints …**) can remind you at chosen times to start or end the day. They are off by default and arrive only while Glide is running.

## Focus timer

Ctrl/Cmd+Shift+F starts a focus session for the selected or next open task. Choose 15, 25 or 50 minutes, or the task's effort. **+5 minutes** extends a session. **Switch to …** changes to another task for today. Ending a session books the time to the task. **Done & next** books the time, completes the task and starts the next one. There is a single timer, shared with time tracking.

## Reminders

Reminders are relative to the due date or fixed at a time. Glide checks them every 15 seconds **while it is running**. Nothing is delivered while Glide is closed. System notifications are optional (Settings, off by default). Otherwise the taskbar or Dock is highlighted. In **View › Notifications …**, **All until tomorrow** postpones open reminders and daily prompts to 09:00 the next day.
