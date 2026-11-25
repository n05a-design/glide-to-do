---
project: Glide
document_id: GLIDE-GEMINI-CORE
title: Glide Core Knowledge Pack
language: en
document_version: 1.0
source_commit: "4ce3697a11321686119313ae5a8e8c891413c85f"
verified_at: "2026-11-22"
status: verified-with-known-gaps
maintainer: project
related_documents: [GLIDE-GEMINI-MASTER, GLIDE-SOURCE-MANIFEST, GLIDE-GAPS]
---

# Glide Core Knowledge Pack

Stand 24.11.2026 · Glide 1.0.3 · Aufgabenformat 26 · Quellstand 4ce3697a

## Identity

Glide is a local-first Python/Tk desktop workspace for one person's tasks, lists, pages, notes, notebooks, boards, galleries, and pixel drawings. It aims to help a person capture work, plan the day, and keep related reference material without requiring an account or cloud service. The user owns the local data.

It is not a cloud collaboration service, automatic multi-device sync, built-in AI service, general project-management system, or full word processor. The app does not automatically transmit task data to an AI tool; AI exchange is an explicit, reviewable file workflow.

## Version and source status

- App: Glide 1.0.2.
- Main data schema: 26. Settings: 2. Templates: 2. Exchange format: `glide.exchange` v2.
- Checked source: `main` at `4ce3697a` (22.11.2026), system catalog V1.86, `glide_shell` 0.6.2 (completed, D99).
- PRs #185–#188 are merged: own photos and bilingual showcase, English quick capture, page edit time, WA-49 and localized release notes.
- No GitHub tag/release, notarization or Homebrew/winget submission exists; no final owner acceptance was recorded.

## Architecture

The main desktop host is `src/glide/app.pyw` (`ListApp`). `glide_start.py` bootstraps the process. The host integrates Tk widgets/views/dialogs, smaller domain modules, local persistence, locale catalog, and desktop adapters. Many domain modules are Tk-free; no-Tk import does not automatically mean a module is application-neutral. The reusable shell is the subpackage `glide_shell` 0.6.0 (copied into follow-up projects with `shell_uebernehmen.py`); since V1.84 `app_host` runs the main window and `command_history` undo/redo, with `ListApp` as the controller.

Data is local JSON plus attachments and backups. Writes use same-directory temporary files and atomic replacement. A per-directory lock guards recognized local concurrent writers; it cannot merge unsynchronized cloud/device copies. Newer schema or failed safety checks must not silently overwrite data.

## Data concepts

Folders contain nested folders and fixed-kind lists. Points include schedulable `task`, long text, structural `group`, and `heading`. A task can include completion, `due` deadline, `planned_date` work day, estimate and recorded time, importance, labels, checklist, independent subtasks, recurrence, reminder, links and attachment references. A view projects data; it is not necessarily a new persisted object.

`due` and `planned_date` are distinct. Checklist entries are not independent scheduled tasks. Structural group/heading points are not tasks. Stored identifiers/schema keys are stable across UI locales.

## Key features and workflows

Glide combines quick capture, folders/lists, tasks and structures, Today/upcoming/inbox, daily/weekly planning, saved views, search/filter/grouping, pages and notes, notebooks, pinboards, drawing, image gallery, attachments, undo/redo, backup, import and export. The complete feature inventory is in `src/glide/README.md`; exact behavior and limits are in `docs/20_FUNKTIONEN.md`.

Import/export includes `.glideexchange`, `.glidecontext`, Markdown/TXT, CSV, ICS, Notion archives, JSON Canvas, drawings and app backups. File import is validated/reviewed and protected as specified in the data contract. Formats have loss boundaries; a backup, not a generic export, is the full recovery route.

## Design and language

The design contract is `docs/DESIGN_RICHTLINIEN.md`; it prioritizes content over controls, coherent hierarchy, visible focus, stable geometry, keyboard/platform behavior, and restrained role-based colors. Owner decisions and exact metrics are in the canonical design document. Load the project `design-richtlinien` skill before any UI work.

German and English catalogs exist via `i18n.py`; current UI localization is partial. Settings and selected menus/views/editors/inspector surfaces are bilingual; additional dialogs, dynamic messages and errors remain. Do not claim full DE/EN based on catalog parity.

## Evidence and current red state

At source head `5631333a`, GitHub basic CI, Analyze, and CodeQL passed. Linux/Tk 9.1 and Windows/Tk 9.1 full runs both timed out after 900 seconds in `tests/integration/test_ui39.py`, skipping 112 later checks per job. The updated isolated diagnostic on PR head `042a8d7` passed on both platforms; each run completed both themes and all 15 dropdown loops with callback-error assertions enabled. This does not identify the callback involved in the earlier local macOS modal block (`_show_error_notice` → `show_warning` → `wait_window`), whose cause remains UNKNOWN. On prior head `cada01bf`, Linux full workflow #44530090137 failed `test_ui39.py` with `RoundedButton.__init__.<locals>.<lambda>() missing 1 required positional argument: '_event'`; its Windows job was canceled on the later push. At corrected head `dd469d12`, focused workflow #44538762234 passed Linux/Tk 9.1 and Windows/Tk 9.1; full workflow #44538664389 passed basic CI while Linux full validation remained in progress and Windows full validation had not started. Older focused run #44518533866 at `5631333a` has Linux failed and Windows running. The earlier automatic PR run #44523300465 passed basic CI, Analyze, and CodeQL; Linux `apt-get update/install` received HTTP 503 responses from Ubuntu package sources and exited 100 before tests, while calibration failed because the suite-result file was absent.

The V1.48 settings dialog fix passed targeted macOS `schriftstile` (1/1), UI design unit tests (23/23), and the local CI basic stage. Linux full validation of that fix remains outstanding. The earlier red timeout in settings layout is a separate incident and should not be conflated with `test_ui39`.

## Rules for answers and changes

Classify assertions as **VERIFIED**, **DOCUMENTED**, **PLANNED**, **PROPOSED**, **INFERRED**, **UNKNOWN**, or **OBSOLETE**. Say which commit/platform/test supports a verified claim. A test's existence is not a pass; a timeout is not a pass; skipped checks are unverified; a local result is not cross-platform; a package template is not a published release.

Read `AGENTS.md`, handoff, working direction, development plan, document-maintenance matrix, and relevant canonical source before changing code. Keep new domain logic Tk-free and unit-tested (D17), preserve the existing mutation/save boundaries, isolate tests with `GLIDE_DATA_DIR` before importing Glide, use synthetic data and `python3 -B`, and honor all existing data/design/security constraints. Never commit secrets, user data, private paths, raw logs, or protected evidence.

## Source map

Use `SOURCE_MANIFEST.md` for authority and links, `KNOWLEDGE_GAPS.md` for contradictions/open evidence, `GEMINI_IMPORT_GUIDE.md` for context selection, and `FINAL_AUDIT.md` for coverage/verification state. The authoritative German project sources override this pack.
