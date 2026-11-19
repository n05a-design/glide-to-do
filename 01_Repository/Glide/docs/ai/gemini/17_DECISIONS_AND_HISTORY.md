---
project: Glide
document_id: GLIDE-DECISIONS
title: Decisions and history
language: en
document_version: 1.0
source_commit: "5631333a1c5a80c11c48226016ab115c434b0a64"
verified_at: "2026-11-19"
status: documented-with-known-gaps
maintainer: project
related_documents: [GLIDE-ROADMAP, GLIDE-ARCHITECTURE, GLIDE-PLAYBOOK]
---

# Decisions and history

Stand 19.11.2026 · Glide 1.0.0 · Aufgabenformat 26 · Quellstand 5631333a

## Where decisions live

The complete decision register D01–D93 and working procedure are in [`docs/ARBEITSRICHTUNG.md`](../../ARBEITSRICHTUNG.md). Do not reconstruct or renumber decisions from this summary. The development plan holds implementation/status chronologically; QA holds the actual test evidence. Historical records retain the source version and cannot be rewritten as current evidence.

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
- System catalogs and feature releases are independently versioned from the app and data schema. `main` was at catalog V1.47; PR #152's V1.48 app/dialog candidate now has a V1.49 catalog update for diagnostics.
- The v1.0.0 source cut was merged to `main` on 19 November; the repository's recorded release state had no tag or GitHub Release.
- PR #152 contains follow-up localization and a dialog geometry fix. Its latest full Linux/Windows checks are red in `test_ui39.py`; local macOS passes do not supersede them.

This concise history omits many dated choices and implementation details. Use original plan entries, QA records, and Git history to answer exact “when/why” questions.
