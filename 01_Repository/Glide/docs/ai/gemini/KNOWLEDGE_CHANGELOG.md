---
project: Glide
document_id: GLIDE-KNOWLEDGE-CHANGELOG
title: Knowledge base changelog
language: en
document_version: 1.0
source_commit: "4ce3697a11321686119313ae5a8e8c891413c85f"
verified_at: "2026-11-22"
status: current
maintainer: project
related_documents: [GLIDE-GEMINI-INDEX, GLIDE-AUDIT]
---

# Knowledge base changelog

Stand 23.11.2026 · Glide 1.0.2 · Aufgabenformat 26 · Quellstand 4ce3697a

## 1.2 — 2026-11-23 — status refresh for Glide 1.0.2

- Refreshed version and release facts to Glide 1.0.2 across the knowledge base.
- Recorded full owner completion of human visual and operation acceptance (Release 1.0, Etappe 2) and resolution of all acceptance findings.
- Recorded multi-agent bootstrap and transactional safety integration (PR #193).

## 1.1 — 2026-11-22 — status refresh for Glide 1.0.1

- Refreshed version, localization, shell and release status against `main` `4ce3697a`: Glide 1.0.1, system catalog V1.83, complete DE/EN interface, `glide_shell` 0.5.0 completed (D99), PRs #185–#188 merged.
- Removed claims that localization is partial and that the shell package is a post-1.0 goal; marked the PR #152 timeout issues as historical.
- Topic content outside these status facts keeps its original snapshot `5631333a`; the source manifest names which files were refreshed.

## 1.0 — 2026-11-19 — initial Gemini knowledge base

- Added the 20 requested topic modules plus index, source manifest, knowledge gaps, import guide, changelog, audit, and compact Core Knowledge Pack.
- Captured source branch commit `5631333a`, the PR #152 / `main` distinction, current full-run timeouts, remaining localization scope, and release/publication gates.
- Used evidence labels and linked each summary to canonical Glide documents; unknowns remain explicit.
- This documentation set is derived from one source snapshot. It has not yet been accepted as a public or permanent project contract.

## 1.0.1 — 2026-11-19 — diagnostic and technical-validation refresh

- Updated the system-catalog status to V1.49 for the `test_ui39.py` diagnostic instrumentation; the application/source baseline remains commit `5631333a` and the V1.48 settings-dialog candidate.
- Added links for all 27 knowledge-base files to the canonical documentation index after the first CI run identified the missing entries.
- Recorded the passing local CI basic stage and its remaining external-package network limitation in `FINAL_AUDIT.md`.
- A local macOS diagnostic run exposed a modal error-notice block in `wait_window`; the triggering callback exception remains unknown. The test now suppresses that notice while retaining the callback-error assertion.
- The Linux/Windows full-suite timeout is still unresolved; no platform or release gate is claimed green by this documentation update.

## 1.0.2 — 2026-11-19 — remote diagnostic status refresh

- Recorded PR #152 head `042a8d7`, delivery of the V1.49 diagnostic follow-up, and the V1.50 evidence/catalog refresh.
- Added the local V1.51/V1.52 callback correction, its local test/CI evidence, and a fresh status snapshot for PR head `cada01bf` and workflows #44530090137/#44518533866. Current Linux failures are recorded without guessing their causes because logs were unavailable while the workflows were active.
- Recorded V1.52 delivery as `dd469d12`, the confirmed Linux `RoundedButton` missing-`_event` failure on prior head `cada01bf`, and the active corrected-head workflows #44538664389 and #44538762234.
- Added the local V1.51 UI39 test correction: reinstall the callback collector after `ListApp` initialization, retain callback-error assertions, and record five later macOS/Tk 9.0.3 passes. The triggering `bind_mousewheel` callback remains unexplained; remote verification is pending.
- Added the local V1.52 no-event callback handling: wheel/trackpad callbacks and `RoundedButton` focus redraw now tolerate missing event objects; direct Tcl regression checks passed and `test_ui39.py` passed 6/6 locally. The reason Tk/Tcl omitted event substitutions remains unknown; remote verification is pending.
- The isolated `test_ui39.py` diagnostic passed on Linux/Tk 9.1 and Windows/Tk 9.1 with callback-error assertions retained.
- Distinguished the historical full-suite timeout from the newer Linux setup failure: Ubuntu package sources returned HTTP 503 during native prerequisite installation, and the later calibration step had no suite-result file. The Windows full run and focused work-mode run were still active at last check.
- Kept the callback exception from the local macOS modal path and full platform-matrix completion explicitly unresolved.

## 1.0.3 — 2026-11-19 — corrected-head UI39 status

- Recorded the passing focused UI39 jobs on Linux/Tk 9.1 and Windows/Tk 9.1 at `dd469d12`.
- Recorded that the full workflow basic stage passed while its Linux full-validation job was still running; no full-matrix or macOS/package result is claimed.

## 1.0.4 — 2026-11-19 — bilingual homepage and local CI refresh

- Recorded the local README expansion, the English `Status as of` label, and the stand-check regression test that accepts the English label while rejecting stale versions.
- The focused stand-check suite passed 23/23 and the macOS CI basic stage passed after all README and documentation edits; the corrected-head Linux full workflow was still running at the latest status check.
- The README/documentation changes remain local and unpushed; GitHub About metadata, new 1.0.0 screenshots/GIF, full platform validation, and the macOS package run remain open.

## Maintenance rule

Record each meaningful update with date, source commit, documents affected, reason, and evidence. Do not rewrite older source QA results; update present status in the current plan/QA sources first.
