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

Glide is a local-first desktop workspace for an individual's tasks, lists, pages, notes, notebooks, pinboards, galleries, and pixel drawings. The app is implemented in Python with Tk. Its current source release target is 1.0.0; the checked code baseline has schema 26, exchange format 2, and a V1.48 settings-dialog candidate. PR #152 is open at remote head `dd469d12`; V1.52 callback handling, tests, and status documentation were pushed in that commit. Earlier V1.49 diagnostics and V1.50 evidence refreshes are also on the branch. The local V1.52 follow-up installs the UI39 test collector after app initialization and safely ignores wheel/focus callback invocations without an event object. `test_befunde330.py` passed and `test_ui39.py` passed six times locally on macOS/Tk 9.0.3; focused remote UI39 passed on Linux/Tk 9.1 and Windows/Tk 9.1. The full workflow basic stage passed and Linux full validation remained in progress at the status snapshot; why Tk/Tcl invoked bindings without event fields remains unexplained.

## How it works

The canonical app starts through `src/glide/glide_start.py` or `src/glide/app.pyw`; the large `ListApp` class coordinates the Tk UI and adapts many smaller, mostly Tk-free domain modules. Data is held locally in JSON files and attachments. Saves use atomic replacement and local write protection. Import/export is document- or file-based; Glide does not provide a cloud backend or built-in AI service.

## Facts versus plans

- **Current branch snapshot:** PR #152 is open at remote head `dd469d122cca3dd5bf01823364c95c365bcdaae7`; its app/code baseline for product descriptions is `5631333a1c5a80c11c48226016ab115c434b0a64`, with the V1.49 test-diagnostic and V1.50 evidence/documentation follow-ups on top. V1.52 adds safe handling for wheel/focus callbacks without event objects and has been pushed; focused remote UI39 passed on Linux and Windows. This is not `main`.
- **App/data versions:** 1.0.0 / 26. Settings 2, templates 2, exchange format 2.
- **Localization:** German default and English supported in the i18n mechanism; only some UI areas are translated end-to-end.
- **Release:** source cut is merged on `main`, but the checked state reported no tag or GitHub release. Public package-manager submissions and owner acceptance are not complete.
- **QA:** local macOS basic suite passed on the V1.52 candidate. On earlier PR head `042a8d7`, isolated `test_ui39.py` passed on Linux/Tk 9.1 and Windows/Tk 9.1 with the callback-error assertion intact. The historical full run timed out at 900 seconds on both platforms at `5631333a`. On prior head `cada01bf`, full workflow #44530090137 failed Linux `test_ui39.py`; the callback assertion captured `RoundedButton.__init__.<locals>.<lambda>() missing 1 required positional argument: '_event'`. Its Windows job was canceled by the later push. V1.52 now tolerates the absent event object; local regression checks and six uninstrumented `test_ui39.py` runs passed. At current head `dd469d12`, focused workflow #44538762234 passed Linux and Windows UI39; full workflow #44538664389 passed basic CI while Linux full validation remained in progress and Windows full validation had not started. The old focused workflow #44518533866 on `5631333a` has Linux failed and Windows still running. Why Tk/Tcl invoked the bound callbacks without substitution values remains unknown.

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
