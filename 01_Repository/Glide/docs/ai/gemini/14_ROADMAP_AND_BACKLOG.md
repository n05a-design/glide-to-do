---
project: Glide
document_id: GLIDE-ROADMAP
title: Roadmap and backlog
language: en
document_version: 1.0
source_commit: "4ce3697a11321686119313ae5a8e8c891413c85f"
verified_at: "2026-11-22"
status: documented-with-known-gaps
maintainer: project
related_documents: [GLIDE-GEMINI-MASTER, GLIDE-KNOWN-ISSUES, GLIDE-DECISIONS]
---

# Roadmap and backlog

Stand 24.11.2026 · Glide 1.0.3 · Aufgabenformat 26 · Quellstand 4ce3697a

## Authority and release plan

The only project backlog is [`00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md`](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md); the v1.0 milestone plan and D93 in [`docs/ARBEITSRICHTUNG.md`](../../ARBEITSRICHTUNG.md) define the release scope. This file is a dated index, not an alternative backlog or authorization.

## Release 1.0 status

| Milestone | Target | Snapshot status |
|---|---|---|
| Etappe 1 — agent skill | Completed exchange skill and version-coupled field coverage | Completed; `glide-to-do` skill coupled to Glide 1.0.2, exchange format 2, data schema 26 |
| Etappe 2 — DE/EN | Localize the app UI | Completed (V1.70–V1.81) |
| Etappe 3 — distribution | Native installers/packages and Homebrew/winget paths | Technically complete: macOS package and DMG 1.0.2 checked locally, Windows installer in CI; Homebrew/winget templates not submitted |
| Etappe 4 — release cut/publication | Freeze source, green gates, tag/release, acceptance | Source 1.0.2 on `main`; owner human acceptance completed (23.11.2026); tag, release, notarization are owner steps |

This table separates implementation, verification, release, and owner action. A prepared manifest or workflow does not count as external publication.

## Current engineering gate

On 23.11.2026, the 1.0.2 release round successfully completed the owner human visual and operation acceptance and resolved all identified items (sidebar locale refresh, adaptive cover crop, corner stamp, table flow, natural due words). Multi-agent bootstrap and transactional safety (PR #193) are integrated.

Remaining work is limited to owner gates: tag/release, notarization, and Homebrew/winget submission.

## Roadmap reading rules

- D93 is the release milestone decision; D01–D92 and feature-freeze boundaries remain in force.
- A package marked implemented may still await remote CI, native package validation, visual acceptance, or delivery-copy reconciliation.
- Preserve historical red/green records with their exact commits; only later evidence can supersede them for current status.
- Use the plan's dated section and QA report for exact details. This snapshot should be refreshed when either changes.
