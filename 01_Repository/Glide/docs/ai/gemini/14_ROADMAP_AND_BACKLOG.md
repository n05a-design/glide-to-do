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

Stand 22.11.2026 · Glide 1.0.1 · Aufgabenformat 26 · Quellstand 5631333a

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

PR #152 remains open at remote head `dd469d12`; product-code baseline `5631333a` carries the V1.48 settings-dialog layout fix and additional i18n work, while V1.49/V1.50 follow-ups added test diagnostics and evidence. The isolated `test_ui39.py` workflow #44523315466 passed on Linux/Tk 9.1 and Windows/Tk 9.1 at earlier head `042a8d7` with the callback-error assertion intact. V1.52 reinstalls the test collector after `ListApp` initialization and safely handles callbacks invoked without an event object; this was observed for wheel/trackpad bindings and a focus redraw. `test_befunde330.py` passed its no-argument Tcl callback checks, and the final local `test_ui39.py` passed 6/6 on macOS/Tk 9.0.3. Why Tk/Tcl omitted event substitutions remains unknown. On prior head `cada01bf`, full workflow #44530090137 failed Linux `test_ui39.py` with a `RoundedButton` lambda missing `_event`; the Windows job was canceled after the new push. At current head `dd469d12`, focused UI39 workflow #44538762234 passed on Linux/Tk 9.1 and Windows/Tk 9.1. Full workflow #44538664389 passed its basic stage; its Linux full-validation job was still running at this snapshot and Windows full validation had not started. Older focused workflow #44518533866 has Linux failed and Windows running on `5631333a`. The earlier automatic run #44523300465 passed basic CI, CodeQL, and Analyze but Linux `apt-get update/install` received HTTP 503 responses before tests; the later calibrated-expectations step failed because the suite-result file was absent. These results do not replace the full matrix. Native macOS full validation and packaging remain deferred until required platform checks are green.

The plan's remaining work includes diagnosing that red run, continuing the defined DE/EN and public-homepage audit, and completing the release/owner gates. Do not select E-P1–E-P5, add features beyond the freeze, publish externally, or merge without the required authorization.

## Roadmap reading rules

- D93 is the release milestone decision; D01–D92 and feature-freeze boundaries remain in force.
- A package marked implemented may still await remote CI, native package validation, visual acceptance, or delivery-copy reconciliation.
- Preserve historical red/green records with their exact commits; only later evidence can supersede them for current status.
- Use the plan's dated section and QA report for exact details. This snapshot should be refreshed when either changes.
