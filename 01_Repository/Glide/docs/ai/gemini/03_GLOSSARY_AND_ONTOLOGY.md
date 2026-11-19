---
project: Glide
document_id: GLIDE-GLOSSARY
title: Glossary and ontology
language: en
document_version: 1.0
source_commit: "5631333a1c5a80c11c48226016ab115c434b0a64"
verified_at: "2026-11-19"
status: verified-with-known-gaps
maintainer: project
related_documents: [GLIDE-GEMINI-MASTER, GLIDE-DATA]
---

# Glossary and ontology

Stand 19.11.2026 · Glide 1.0.0 · Aufgabenformat 26 · Quellstand 5631333a

Terms below are aligned with [`skills/glide-to-do/references/glide-aufbau.md`](../../../skills/glide-to-do/references/glide-aufbau.md), the canonical German feature contract, and schema names. Technical identifiers are not necessarily UI labels.

| English concept | German UI / project term | Technical identifier or distinction |
|---|---|---|
| Workspace / area | Bereich | Sidebar domain: Pages, Lists, Notes, Drawings |
| Folder | Ordner | `folder`; kinds include `standard`, `library` (Buch), `journal` (Notizbuch) |
| List/container | Liste | Stable container ID; a list has a fixed kind after creation |
| Task/item | Aufgabe / Punkt | `task` is a schedulable point; Punkt is the broader term |
| Long text | Langtext | `long`; not a schedulable task |
| Group | Gruppe | `group`; structural outline node, not an executable task |
| Heading | Zwischenüberschrift | `heading`; structural node |
| Due date | Fälligkeit | `due`, optional `due_time`; deadline |
| Planned date | Bearbeitungstag / geplant für | `planned_date`, optional `planned_time`; intended work day, not deadline |
| Estimate | Aufwand / Schätzung | Planned duration input used in scheduling/capacity views |
| Recorded time | Erfasste Zeit | Actual time capture, distinct from estimate |
| Importance | Wichtigkeit | Integer/rank 0–3, not general status |
| Checklist | Checkliste | Short substeps within a task; checking a step does not complete the task |
| Subtask | Unterpunkt | Independent point with its own fields and lifecycle |
| Label | Label | User-defined tag; special fixed labels relate to point kind |
| View | Ansicht | List/table/calendar/board/etc. projection; not a new data object by itself |
| Today | Heute | Planned-day view; counts a task once and uses planned date |
| Inbox | Eingang | Tasks without a planned date; not a standalone list kind |
| Pinboard | Pinnwand | Canvas-like spatial view; differs from a list |
| Page | Seite | Rich document with blocks; can include task points and live lists |
| Note | Notiz | Text-oriented list kind |
| Notebook | Notizbuch | Folder kind `journal`, date-oriented entries |
| Gallery | Galerie | Fixed list kind for local images/attachments |
| Drawing | Zeichnung / Pixel-Werkstatt | Pixel-art document; independent object kind |
| Attachment | Anhang | Local asset stored under the data directory and referenced by ID |
| Undo / redo | Rückgängig / Wiederholen | In-memory history with explicit save/guard semantics; not an archival version history |
| Exchange format | Austauschformat | `glide.exchange`, version 2; not the same as data schema 26 |
| Data schema | Aufgabenformat / Datenformat | Main persisted-list schema, currently 26 |
| System catalog | Glide-System | Independent module/feature/test inventory version; current PR #152 worktree candidate V1.49 |
| Glide Shell | Glide-Shell | Set of extracted shell-oriented modules inside Glide; not yet a separately released/shared package |

## Ontology notes

- A folder contains lists and/or folders; pages and notes are lists of distinct fixed kinds.
- A task is a point, but not every point is a task. Group and heading nodes are structural.
- Due date and planned date are independent fields. Planning a task for today does not make it due today.
- A checklist is not a set of independently scheduled tasks; subtasks are.
- Views project existing data. Do not infer a duplicate object or a new persistence type from a view name.
- The visible label may be localized, while stored kind identifiers and schema fields remain stable.

## Terminology risks

Historical documents may use older product versions, “Bibliothek”/“Tagebuch,” “Long-Task,” or “In Bearbeitung.” Prefer current code identifiers and current feature contracts; retain historical wording only when quoting dated evidence. “Punkt” is a general category, not a synonym for task.
