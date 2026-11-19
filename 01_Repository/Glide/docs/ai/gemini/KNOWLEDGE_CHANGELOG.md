---
project: Glide
document_id: GLIDE-KNOWLEDGE-CHANGELOG
title: Knowledge base changelog
language: en
document_version: 1.0
source_commit: "5631333a1c5a80c11c48226016ab115c434b0a64"
verified_at: "2026-11-19"
status: current
maintainer: project
related_documents: [GLIDE-GEMINI-INDEX, GLIDE-AUDIT]
---

# Knowledge base changelog

Stand 19.11.2026 · Glide 1.0.0 · Aufgabenformat 26 · Quellstand 5631333a

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
- The isolated `test_ui39.py` diagnostic passed on Linux/Tk 9.1 and Windows/Tk 9.1 with callback-error assertions retained.
- Distinguished the historical full-suite timeout from the newer Linux full-run setup failure before tests; the Windows full run and focused work-mode run were still active at last check.
- Kept the callback exception from the local macOS modal path and full platform-matrix completion explicitly unresolved.

## Maintenance rule

Record each meaningful update with date, source commit, documents affected, reason, and evidence. Do not rewrite older source QA results; update present status in the current plan/QA sources first.
