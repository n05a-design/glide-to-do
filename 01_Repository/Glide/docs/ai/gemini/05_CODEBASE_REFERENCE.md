---
project: Glide
document_id: GLIDE-CODEBASE
title: Codebase reference
language: en
document_version: 1.0
source_commit: "5631333a1c5a80c11c48226016ab115c434b0a64"
verified_at: "2026-11-19"
status: verified-with-known-gaps
maintainer: project
related_documents: [GLIDE-ARCHITECTURE, GLIDE-GEMINI-CORE]
---

# Codebase reference

Stand 24.11.2026 · Glide 1.0.3 · Aufgabenformat 26 · Quellstand 5631333a

## Entry points

| Path | Responsibility | Related tests |
|---|---|---|
| `src/glide/app.pyw` | `ListApp`, application start, UI/event coordination, compatibility facades, persistence calls | broad integration suites; no single class-level test |
| `src/glide/glide_start.py` | launch/bootstrap and runtime setup | `tests/integration/test_startwege.py`, runtime tool tests |
| `src/glide/runtime_check.py` | Python/Tk runtime version check | `tests/unit/test_runtime_check.py` |
| `src/glide/runtime_config.py` | data/cache path resolution and explicit directory preparation | `tests/unit/test_runtime_config.py` |

## Domain and UI support modules

The following are navigation anchors, not a substitute for signatures or current implementations.

| Area | Representative modules | Notes |
|---|---|---|
| Task mutation/history | `task_editing.py`, `undo_history.py`, `structural_guard.py`, `item_index.py` | IDs, ownership and mutation guards are critical; preserve undo and persistence behavior |
| Planning/time | `planning.py`, `today_view.py`, `week_planning.py`, `day_proposal.py`, `day_relief.py`, `calendar_service.py`, `ics_*` | Keep date rules pure where possible; distinguish planned date from due date |
| Views/navigation | `sidebar_policy.py`, `view_definition.py`, `view_metrics.py`, `side_view.py`, `action_catalog.py`, `action_menu.py`, `home_dashboard.py` | Mostly projections/policies; host remains `ListApp` |
| Documents/media | `page_markdown.py`, `page_features.py`, `pinboard_pages.py`, `drawing.py`, `drawing_image.py`, `image_conversion.py`, `animation.py` | Validate formats, attachments, limits, and round trips |
| Persistence/safety | `persistence.py`, `schema_backups.py`, `backup_*`, `session_guard.py`, `save_result.py`, `storage_health.py` | Failure paths and byte preservation are as important as successful writes |
| Appearance/accessibility | `appearance.py`, `ui_design.py`, `font_catalog.py`, `symbol_policy.py`, `custom_controls.py`, `accessibility*.py` | Follow central design contract and test actual geometry/labels |
| Localization/desktop | `i18n.py`, `desktop_adapter.py`, `modal_session.py`, `window_lifetime.py` | Host adapters and fallback semantics must remain compatible |

The register contains 100 Python source files (99 runtime files and a separate drawing prototype), 148 feature entries, 25 reusable-component candidates, 25 dated risks, and 329 test/tool files in its snapshot. Counts describe inventory, not pass rate or package approval.

## Contracts and dependencies

- `ListApp` calls domain modules and retains user-visible mutation entry points.
- New/changed domain logic is expected to be Tk-free with unit tests (D17).
- The product Skill's `abdeckung.json`, reference pages, examples, and `ki_ausgabe.py` are coupled to schema and exchange changes; see `skills/glide-to-do/`.
- Packaging uses explicit source/runtime manifests and compares compiled/runtime contents; see `packaging/README.md`.
- The runtime copy under `07_Python-Versionen/` is a deliverable copy, not a second canonical source tree.

## How to find call relationships

Search the current snapshot for the function/class identifier and its callers; do not use line numbers copied from this snapshot as a stable API. Before moving a function, inspect its callers in `app.pyw`, tests, build manifests, and the system register. Use the existing tests and architecture notes to confirm behavior; this table intentionally does not invent a complete call graph.

## Failure handling

Important paths return structured save outcomes or preserve explicit errors; do not replace them with broad catches or success-shaped fallback values. `session_guard.py` and `runtime_diagnostics.py` support post-crash diagnosis but do not recover unsaved in-memory state after a hard process termination.

## Primary index

The full, machine-maintained module/test catalog is [`src/glide/README.md`](../../../src/glide/README.md). Historical file sizes and module counts in older architecture text are dated snapshots, not current measurements.
