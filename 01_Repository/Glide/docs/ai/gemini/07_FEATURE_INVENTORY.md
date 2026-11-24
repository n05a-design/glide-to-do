---
project: Glide
document_id: GLIDE-FEATURES
title: Feature inventory
language: en
document_version: 1.0
source_commit: "4ce3697a11321686119313ae5a8e8c891413c85f"
verified_at: "2026-11-22"
status: verified-with-known-gaps
maintainer: project
related_documents: [GLIDE-GEMINI-MASTER, GLIDE-DATA, GLIDE-ROADMAP]
---

# Feature inventory

Stand 24.11.2026 · Glide 1.0.3 · Aufgabenformat 26 · Quellstand 4ce3697a

This document is the English navigation and status layer. The canonical register is the detailed feature table in [`src/glide/README.md`](../../../src/glide/README.md), with user-visible behavior in [`20_FUNKTIONEN.md`](../../20_FUNKTIONEN.md). The system catalog reports 148 feature entries: 128 product/UI entries (including the external agent skill) and 20 technical system capabilities. The counts are inventory counts, not a claim that every row has current cross-platform acceptance.

| Area | Present behavior (summary) | Status and evidence |
|---|---|---|
| Tasks and structures | Tasks, structural points, fixed-kind lists, folders, labels, trash, undo/redo | Integrated features; see F001–F010 and current feature contract |
| Navigation and capture | Four sidebar areas, system views, keyboard navigation, quick capture and action palette | Implemented/documented; UI platform evidence varies |
| Daily planning | Today, upcoming work, day/week planning, capacity and local calendar busy-time input | Implemented in app; repeat/calendar bounds are explicit |
| Lists and views | List/table/grouping, saved views, search, filters, task links and references | Implemented; distinguish projection from stored object |
| Pages and notes | Markdown-oriented pages, block editing, notebooks, live lists and local references | Implemented; page scope is bounded, not a general word processor |
| Pinboard | Spatial cards/edges, layouts and JSON Canvas export | Implemented in catalog; export has a documented loss report/format contract |
| Drawing/gallery | Pixel drawing, image attachments, gallery and animation | Implemented with file/system-dependent preview capabilities |
| Import/export/backup | Exchange/context files, Markdown, CSV, ICS, Notion, drawings and app backups | Implemented with per-format size/compatibility limits |
| Appearance/accessibility | Multiple design profiles, themes, custom Tk controls, keyboard and accessibility adapters | Implemented in parts; human/native acceptance remains independent |
| Internationalization | Complete DE/EN interface, manual, exchange format, templates, home page, AI output and release notes; quick capture understands English and German words | Completed for 1.0 (V1.70–V1.81, T335, `test_i18n`); human acceptance open |
| Product agent skill | `glide-to-do` skill generates/imports supported data documents and has format-coupled tests | Present outside app UI; not a general agent API |
| Showcase and editing time | Bilingual “City Light” showcase with own photos (MPL-2.0); open pages show their last edit time | V1.80, V1.82 |
| Technical shell capabilities | `glide_shell` 0.6.2: modal lifecycle, custom controls, window callback scope, desktop adapters, motion, geometry, appearance, redo, text fit, action picker, runtime paths, command history, app host | Modules present inside Glide; package/host extraction is not complete |

## Example stable feature rows

| Feature IDs | Topic | Verification pointer |
|---|---|---|
| F001–F010 | object kinds, task fields, checklist, title limits, undo, trash | `src/glide/README.md` feature section; data and integration tests |
| F021–F027 | quick capture parsing and templates | `capture_parser.py`, `repeat_rules.py`, unit/integration suites |
| F028–F040 | daily planning, repeats, capacity and calendars | `planning.py`, `calendar_service.py`, `repeat_rules.py` |
| Remaining catalog rows | Current feature families and technical capabilities | Use the full catalog; do not infer IDs/status from this abbreviated view |

## Status semantics

- **Implemented** means the code path exists in the checked snapshot.
- **Tested** means the relevant test was actually run and its result is linked/date-bound.
- **Accepted/released** requires platform/package and owner acceptance gates; code presence is insufficient.
- **Planned** and **proposed** remain separate; unresolved options are not selected by this inventory.

The canonical F-row register is intentionally not duplicated here. If an AI answer requires exact acceptance status, use the QA report and the dated plan section, not this category summary. Known current gaps are in [roadmap](./14_ROADMAP_AND_BACKLOG.md) and [known issues](./18_KNOWN_ISSUES_AND_TECH_DEBT.md).
