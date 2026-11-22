---
project: Glide
document_id: GLIDE-PROJECT-OVERVIEW
title: Project overview
language: en
document_version: 1.0
source_commit: "4ce3697a11321686119313ae5a8e8c891413c85f"
verified_at: "2026-11-22"
status: verified-with-known-gaps
maintainer: project
related_documents: [GLIDE-GEMINI-MASTER, GLIDE-PRODUCT-CONSTRAINTS, GLIDE-ROADMAP]
---

# Project overview

Stand 22.11.2026 · Glide 1.0.1 · Aufgabenformat 26 · Quellstand 4ce3697a

## Identity and purpose

**VERIFIED / DOCUMENTED.** Glide is a local desktop workspace for tasks, lists, notes, pages, notebooks, boards, galleries, and pixel drawings. Its product intent is a calm personal place to plan, complete, and record work without requiring an account or cloud service. The owner-defined principles prioritize familiar behavior, function-led form, one primary path per intent, content over controls, a restrained default surface, and a small set of stable concepts.

Primary contract: [`docs/01_PRODUCT_CONSTRAINTS.md`](../../01_PRODUCT_CONSTRAINTS.md). Current user-facing behavior: [`docs/20_FUNKTIONEN.md`](../../20_FUNKTIONEN.md).

## Users and use cases

**DOCUMENTED.** The product targets individuals managing their own day and projects: capture tasks, distinguish due dates from planned work dates, organize work in lists and folders, plan daily capacity, keep reference pages and notes, and use local file import/export. The project does not define a multi-user collaboration product.

The repository includes an agent-facing exchange workflow, but Glide does not itself call an AI service. The user consciously transfers documents to an external tool and reviews proposed imports in Glide.

## Product boundaries

- Local-first storage; no required account, hosted service, telemetry, or automatic data transfer.
- No simultaneous multi-device editing or conflict-merging service. A local lock detects some concurrent writers; it is not distributed synchronization.
- No mobile app, built-in cloud AI, MCP endpoint, or additional language beyond German and English in the current product boundary.
- Calendar exchange is file-based; it is not a subscription or synchronization service.
- The product is a desktop application, not a general database builder or full word processor.

These are documented product constraints, not security certification claims. See the [security and reliability note](./13_SECURITY_PRIVACY_RELIABILITY.md).

## Platforms and maturity

**VERIFIED at `main` `4ce3697a` (22.11.2026):** App version `1.0.1`, data schema `26`, settings schema `2`, template schema `2`, exchange format `glide.exchange` version `2`, system catalog V1.86, `glide_shell` 0.6.2. PRs #185–#188 are merged. No tag, GitHub release, notarization or package-manager submission exists; human acceptance remains open.

Python/Tk builds and tests target macOS, Windows, and Linux. Current documented reference is Python 3.14 and Tk 9.1; Tk 8.6 remains a compatibility/basic-CI layer with reduced native integrations. Platform support does not mean every platform had a green current full run.

## Positioning and evidenced strengths

**DOCUMENTED / partly VERIFIED:** offline-first data ownership, atomic local persistence, explicit backup and format migration safeguards, undo coverage, a broad integrated workspace, custom Tk controls, and a detailed product/design contract are recurring project strengths. The system register and tests provide evidence for specific components; they do not prove every user journey or all-platform behavior.

The intended differentiator is the combination of local data ownership, daily planning, structured notes/pages, and a playful pixel workshop. Comparative claims about competitors require dated external sources; see [research](./15_PRODUCT_RESEARCH_AND_COMPETITION.md).

## Open product questions and risks

- German/English localization is incomplete even though DE/EN is the 1.0 target.
- The repository has a merged 1.0 source cut but no public release in the checked snapshot.
- Homebrew/winget manifests are repository templates, not external submissions.
- Human visual/interaction acceptance is separate from automated QA.
- GitHub full validation on PR #152 timed out in `test_ui39.py` on both Linux and Windows; cause is unknown.

## Evidence map

See [Master Context](./02_GEMINI_MASTER_CONTEXT.md), [feature inventory](./07_FEATURE_INVENTORY.md), [roadmap](./14_ROADMAP_AND_BACKLOG.md), [known issues](./18_KNOWN_ISSUES_AND_TECH_DEBT.md), and the [source manifest](./SOURCE_MANIFEST.md).
