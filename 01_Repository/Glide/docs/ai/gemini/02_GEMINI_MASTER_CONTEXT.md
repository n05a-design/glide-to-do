---
project: Glide
document_id: GLIDE-GEMINI-MASTER
title: Gemini master context
language: en
document_version: 1.0
source_commit: "5631333a1c5a80c11c48226016ab115c434b0a64"
verified_at: "2026-11-19"
status: verified-with-known-gaps
maintainer: project
related_documents: [GLIDE-GEMINI-CORE, GLIDE-ARCHITECTURE, GLIDE-DATA, GLIDE-PLAYBOOK]
---

# Gemini master context

Stand 19.11.2026 · Glide 1.0.0 · Aufgabenformat 26 · Quellstand 5631333a

## What Glide is

Glide is a local-first desktop workspace for an individual's tasks, lists, pages, notes, notebooks, pinboards, galleries, and pixel drawings. The app is implemented in Python with Tk. Its current source release target is 1.0.0; the checked code baseline has schema 26, exchange format 2, and a V1.48 settings-dialog candidate. The current PR worktree includes a V1.49 system-catalog update for test diagnostics.

## How it works

The canonical app starts through `src/glide/glide_start.py` or `src/glide/app.pyw`; the large `ListApp` class coordinates the Tk UI and adapts many smaller, mostly Tk-free domain modules. Data is held locally in JSON files and attachments. Saves use atomic replacement and local write protection. Import/export is document- or file-based; Glide does not provide a cloud backend or built-in AI service.

## Facts versus plans

- **Current branch snapshot:** commit `5631333a1c5a80c11c48226016ab115c434b0a64`, PR #152 open; this is not `main`.
- **App/data versions:** 1.0.0 / 26. Settings 2, templates 2, exchange format 2.
- **Localization:** German default and English supported in the i18n mechanism; only some UI areas are translated end-to-end.
- **Release:** source cut is merged on `main`, but the checked state reported no tag or GitHub release. Public package-manager submissions and owner acceptance are not complete.
- **QA:** local macOS basic suite passed on the candidate. GitHub basic stage, CodeQL, and Analyze passed. Linux and Windows full workflows failed after 900 seconds in `test_ui39.py`; the timeout location inside that test is unknown. A separate focused UI/work-mode workflow was running when this context was recorded.

## Architecture and critical rules

1. Treat `AGENTS.md`, product constraints, architecture, data contract, design rules, feature behavior, and QA report as the authorities. This Gemini collection is a navigation layer, not a competing contract.
2. Keep new or changed domain logic Tk-free and unit-tested (D17); adapt through existing app entry points.
3. Preserve IDs, schema compatibility, backups, write locks, atomic persistence, undo/redo, and user data. Never use real user data in tests.
4. Do not infer completion from a feature description or a test file. State the exact run, commit, OS, Python/Tk, and limits.
5. Apply the design rules to UI, code, tests, and docs; inspect language and accessibility effects.
6. Do not broaden product scope, choose unselected options, publish a release, or infer owner approval from a technical template.

## High-risk areas

- `app.pyw` is a large integration/coordination module; broad rewrites are not authorized by its size.
- Data migrations and import/restore paths require byte-preservation and backup checks.
- Tk event ordering, geometry, modal lifetime, focus, callbacks, and platform-specific menus are fragile.
- DE/EN strings, accessible names, keyboard labels, and fixed test expectations can drift.
- Automated platform runs can be flaky or stop at the first failure; unknown/timeout is not green.
- `07_Python-Versionen` is a separate deliverable copy; when a permitted production round requires it, use `scripts/pflege/abgleich_07.py` and verify byte equality.

## Start here for task-specific context

| Task | Primary source |
|---|---|
| Product behavior and terms | [`20_FUNKTIONEN.md`](../../20_FUNKTIONEN.md), [`03_GLOSSARY_AND_ONTOLOGY.md`](./03_GLOSSARY_AND_ONTOLOGY.md) |
| Architecture and modules | [`02_ARCHITECTURE.md`](../../02_ARCHITECTURE.md), [`src/glide/README.md`](../../../src/glide/README.md) |
| Persistence/migration/import | [`06_DATA_BACKUP_MIGRATION.md`](../../06_DATA_BACKUP_MIGRATION.md) |
| UI/design/i18n | [`DESIGN_RICHTLINIEN.md`](../../DESIGN_RICHTLINIEN.md), [`10_INTERNATIONALIZATION.md`](./10_INTERNATIONALIZATION.md) |
| Current tasks and decisions | [`Glide_Entwicklungsplan.md`](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md), [`ARBEITSRICHTUNG.md`](../../ARBEITSRICHTUNG.md) |
| Test truth and current failures | [`07_QA_BERICHT.md`](../../07_QA_BERICHT.md), [`12_TESTING_AND_QUALITY.md`](./12_TESTING_AND_QUALITY.md) |
| Agent procedure | [`20_AI_DEVELOPMENT_PLAYBOOK.md`](./20_AI_DEVELOPMENT_PLAYBOOK.md) |

Full evidence and limitations are in the [Core Knowledge Pack](./GEMINI_CORE_KNOWLEDGE_PACK.md) and [Knowledge Gaps](./KNOWLEDGE_GAPS.md).
