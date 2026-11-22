---
project: Glide
document_id: GLIDE-DECISIONS
title: Decisions and history
language: en
document_version: 1.0
source_commit: "4ce3697a11321686119313ae5a8e8c891413c85f"
verified_at: "2026-11-22"
status: documented-with-known-gaps
maintainer: project
related_documents: [GLIDE-ROADMAP, GLIDE-ARCHITECTURE, GLIDE-PLAYBOOK]
---

# Decisions and history

Stand 22.11.2026 · Glide 1.0.1 · Aufgabenformat 26 · Quellstand 4ce3697a

## Where decisions live

The complete decision register D01–D99 and working procedure are in [`docs/ARBEITSRICHTUNG.md`](../../ARBEITSRICHTUNG.md). Do not reconstruct or renumber decisions from this summary. The development plan holds implementation/status chronologically; QA holds the actual test evidence. Historical records retain the source version and cannot be rewritten as current evidence.

## Design and engineering principles affecting changes

| Decision | Practical implication |
|---|---|
| D17 | New/changed domain logic is Tk-free and has unit tests; preserve existing UI/mutation entry points |
| D49 | Treat its interpretation as provisional with correction caveat; do not extend it silently |
| D50 | UI/UX quality takes precedence over convenience or feature count |
| D51 | Use phase-based tests: focused checks during work, a frozen full run at phase end; do not run long full suites for every small edit unless needed |
| D52–D54 | Centralize roadmap, design, integration evaluation, and documentation maintenance at their authoritative sources |
| D55 | The selected decisions and feature packages remain bound to the development plan; suggestions are not selected |
| D86–D90 | Shell separation follows the approved sequence and flattens modules until the agreed package/host work; no speculative abstraction |
| D91–D92 | `glide-to-do` is an import-document skill, coupled strictly to format 26 via `abdeckung.json`, helper, references, examples, and tests |
| D93 | Release 1.0 milestone/freeze and four-stage scope; completing a source cut is not itself publication |

## Source and release chronology

- Early Glide development established local-first storage, stable object identities, schema guards, and Tk UI integration.
- System catalogs and feature releases are independently versioned from the app and data schema; `main` is at catalog V1.86 with app 1.0.1 (22.11.2026). D99 records that the Glide Shell work is complete.
- The v1.0.0 source cut was merged to `main` on 19 November and never published; 1.0.1 is the first release candidate. No tag or GitHub Release exists.
- PR #152 contains follow-up localization and a dialog geometry fix. Its latest full Linux/Windows checks are red in `test_ui39.py`; local macOS passes do not supersede them.

This concise history omits many dated choices and implementation details. Use original plan entries, QA records, and Git history to answer exact “when/why” questions.
