---
project: Glide
document_id: GLIDE-GEMINI-INDEX
title: Gemini knowledge base
language: en
document_version: 1.0
source_commit: "5631333a1c5a80c11c48226016ab115c434b0a64"
verified_at: "2026-11-19"
status: verified-with-known-gaps
maintainer: project
related_documents: [GLIDE-GEMINI-MASTER, GLIDE-GEMINI-CORE]
---

# Glide knowledge base for Gemini

Stand 23.11.2026 · Glide 1.0.2 · Aufgabenformat 26 · Quellstand 5631333a

This collection is a curated, evidence-linked view of Glide at the source snapshot named above. It is not a replacement for the application, the canonical product contract, or the dated QA record. Read [Gemini Master Context](./02_GEMINI_MASTER_CONTEXT.md) first; use [Source Manifest](./SOURCE_MANIFEST.md) to navigate primary evidence.

## Contents

| ID | Document |
|---|---|
| 01–03 | [Project overview](./01_PROJECT_OVERVIEW.md), [master context](./02_GEMINI_MASTER_CONTEXT.md), [glossary](./03_GLOSSARY_AND_ONTOLOGY.md) |
| 04–06 | [Architecture](./04_SYSTEM_ARCHITECTURE.md), [codebase reference](./05_CODEBASE_REFERENCE.md), [data model](./06_DATA_MODEL_AND_PERSISTENCE.md) |
| 07–10 | [Feature inventory](./07_FEATURE_INVENTORY.md), [user workflows](./08_USER_WORKFLOWS.md), [design system](./09_UX_UI_DESIGN_SYSTEM.md), [internationalization](./10_INTERNATIONALIZATION.md) |
| 11–13 | [Development guide](./11_DEVELOPMENT_GUIDE.md), [testing and quality](./12_TESTING_AND_QUALITY.md), [security and reliability](./13_SECURITY_PRIVACY_RELIABILITY.md) |
| 14–16 | [Roadmap](./14_ROADMAP_AND_BACKLOG.md), [research](./15_PRODUCT_RESEARCH_AND_COMPETITION.md), [strategy and marketing](./16_PRODUCT_STRATEGY_AND_MARKETING.md) |
| 17–20 | [Decisions and history](./17_DECISIONS_AND_HISTORY.md), [known issues](./18_KNOWN_ISSUES_AND_TECH_DEBT.md), [integrations](./19_INTEGRATIONS_AND_ECOSYSTEM.md), [AI playbook](./20_AI_DEVELOPMENT_PLAYBOOK.md) |
| Support | [Source manifest](./SOURCE_MANIFEST.md), [knowledge gaps](./KNOWLEDGE_GAPS.md), [Gemini import guide](./GEMINI_IMPORT_GUIDE.md), [knowledge changelog](./KNOWLEDGE_CHANGELOG.md), [final audit](./FINAL_AUDIT.md), [Core Knowledge Pack](./GEMINI_CORE_KNOWLEDGE_PACK.md) |

## How to use and maintain

Start with the Core Knowledge Pack for short sessions; add the topic-specific document and its primary source when the task needs detail. Treat all status and CI claims as dated snapshots. When code, decisions, or a test result changes, update the authoritative German project source first, then the affected Gemini document, source manifest, changelog, and audit metadata. See [AI Development Playbook](./20_AI_DEVELOPMENT_PLAYBOOK.md) and [maintenance guidance](./GEMINI_IMPORT_GUIDE.md).

## Limits

The collection is derived from one branch snapshot, not an exhaustive independent re-audit of every historical commit or every external project. Some topic documents summarize canonical inventories rather than copying all rows. Unknowns, stale claims, and unavailable native/manual evidence are listed in [Knowledge Gaps](./KNOWLEDGE_GAPS.md). No credentials, private filesystem paths, or user data belong here.
