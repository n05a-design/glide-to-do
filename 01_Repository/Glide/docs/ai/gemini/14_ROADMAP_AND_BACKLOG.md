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

Stand 22.11.2026 · Glide 1.0.1 · Aufgabenformat 26 · Quellstand 4ce3697a

## Authority and release plan

The only project backlog is [`00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md`](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md); the v1.0 milestone plan and D93 in [`docs/ARBEITSRICHTUNG.md`](../../ARBEITSRICHTUNG.md) define the release scope. This file is a dated index, not an alternative backlog or authorization.

## Release 1.0 status

| Milestone | Target | Snapshot status |
|---|---|---|
| Etappe 1 — agent skill | Completed exchange skill and version-coupled field coverage | Completed; `glide-to-do` skill coupled to Glide 1.0.1, exchange format 2, data schema 26 |
| Etappe 2 — DE/EN | Localize the app UI | Completed (V1.70–V1.81) |
| Etappe 3 — distribution | Native installers/packages and Homebrew/winget paths | Technically complete: macOS package and DMG 1.0.1 checked locally, Windows installer in CI; Homebrew/winget templates not submitted |
| Etappe 4 — release cut/publication | Freeze source, green gates, tag/release, acceptance | Source 1.0.1 on `main` (`4ce3697a`); tag, release, notarization and human acceptance are owner steps |

This table separates implementation, verification, release, and owner action. A prepared manifest or workflow does not count as external publication.

## Current engineering gate

On 22.11.2026 PR #188 merged the 1.0.1 release round with PRs #185–#187 into `main` (`4ce3697a`): WA-49 closed (V1.83), localized release notes, bilingual showcase, English quick capture and page edit time. The shell is completed (D99).

Remaining work is limited to owner gates: tag/release, notarization, Homebrew/winget submission and human visual/operation acceptance. Do not select E-P1–E-P5, add features beyond the freeze, publish externally, or merge without the required authorization.

## Roadmap reading rules

- D93 is the release milestone decision; D01–D92 and feature-freeze boundaries remain in force.
- A package marked implemented may still await remote CI, native package validation, visual acceptance, or delivery-copy reconciliation.
- Preserve historical red/green records with their exact commits; only later evidence can supersede them for current status.
- Use the plan's dated section and QA report for exact details. This snapshot should be refreshed when either changes.
