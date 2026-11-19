---
project: Glide
document_id: GLIDE-ROADMAP
title: Roadmap and backlog
language: en
document_version: 1.0
source_commit: "5631333a1c5a80c11c48226016ab115c434b0a64"
verified_at: "2026-11-19"
status: documented-with-known-gaps
maintainer: project
related_documents: [GLIDE-GEMINI-MASTER, GLIDE-KNOWN-ISSUES, GLIDE-DECISIONS]
---

# Roadmap and backlog

Stand 19.11.2026 · Glide 1.0.0 · Aufgabenformat 26 · Quellstand 5631333a

## Authority and release plan

The only project backlog is [`00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md`](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md); the v1.0 milestone plan and D93 in [`docs/ARBEITSRICHTUNG.md`](../../ARBEITSRICHTUNG.md) define the release scope. This file is a dated index, not an alternative backlog or authorization.

## Release 1.0 status

| Milestone | Target | Snapshot status |
|---|---|---|
| Etappe 1 — agent skill | Completed exchange skill and version-coupled field coverage | Completed per plan; `glide-to-do` 1.0.0, exchange format 2, data schema 26 |
| Etappe 2 — DE/EN | Localize the app UI | Partial: central catalogs, settings, selected views/editors/inspector; more dialogs, dynamic messages and error/status copy remain |
| Etappe 3 — distribution | Native installers/packages and Homebrew/winget paths | Technical preparation exists; external Homebrew/winget submissions and native current-head evidence remain incomplete |
| Etappe 4 — release cut/publication | Freeze source, green gates, tag/release, acceptance | Source cut is in `main`; no tag/GitHub release or final human acceptance was recorded |

This table separates implementation, verification, release, and owner action. A prepared manifest or workflow does not count as external publication.

## Current engineering gate

PR #152 remains open at `042a8d7`; product-code baseline `5631333a` carries the V1.48 settings-dialog layout fix and additional i18n work, while the V1.49 follow-up adds test diagnostics. The isolated `test_ui39.py` workflow #44523315466 passed on Linux/Tk 9.1 and Windows/Tk 9.1 with the callback-error assertion intact; this status refresh records its result in catalog V1.50. The historical Linux/Windows full runs timed out after 900 seconds at the previous head `5631333a`; the exact callback exception is unknown. A local macOS diagnostic run completed the light-theme dropdown loops, then blocked in the scheduled modal error notice at the dark-theme start (`_show_error_notice` → `wait_window`). The automatic PR run #44523300465 passed basic CI, CodeQL, and Analyze; Linux `apt-get update/install` received HTTP 503 responses from Ubuntu package sources and exited 100 before tests, and the later calibrated-expectations step failed because the suite-result file was absent. Windows full validation was still running at last check. Focused UI/work-mode workflow #44518533866 passed the Linux UI/UX contract step; its work-mode step was still running at last check. These targeted results do not replace the full matrix. Native macOS full validation and packaging remain deferred until required platform checks are green.

The plan's remaining work includes diagnosing that red run, continuing the defined DE/EN and public-homepage audit, and completing the release/owner gates. Do not select E-P1–E-P5, add features beyond the freeze, publish externally, or merge without the required authorization.

## Roadmap reading rules

- D93 is the release milestone decision; D01–D92 and feature-freeze boundaries remain in force.
- A package marked implemented may still await remote CI, native package validation, visual acceptance, or delivery-copy reconciliation.
- Preserve historical red/green records with their exact commits; only later evidence can supersede them for current status.
- Use the plan's dated section and QA report for exact details. This snapshot should be refreshed when either changes.
