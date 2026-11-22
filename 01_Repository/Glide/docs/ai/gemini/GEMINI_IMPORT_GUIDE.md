---
project: Glide
document_id: GLIDE-GEMINI-IMPORT
title: Gemini import guide
language: en
document_version: 1.0
source_commit: "5631333a1c5a80c11c48226016ab115c434b0a64"
verified_at: "2026-11-19"
status: documented-with-known-gaps
maintainer: project
related_documents: [GLIDE-GEMINI-INDEX, GLIDE-GEMINI-CORE, GLIDE-GAPS]
---

# Gemini import guide

Stand 22.11.2026 · Glide 1.0.1 · Aufgabenformat 26 · Quellstand 5631333a

## Recommended small context

Load `GEMINI_CORE_KNOWLEDGE_PACK.md` for a general question. This is intentionally a concise, self-contained view with the current red CI and publication boundaries.

## Add topic context only when needed

| Task | Load |
|---|---|
| Feature scope or user behavior | `01_PROJECT_OVERVIEW.md`, `07_FEATURE_INVENTORY.md`, then primary `20_FUNKTIONEN.md` |
| Code change | `02_GEMINI_MASTER_CONTEXT.md`, `04_SYSTEM_ARCHITECTURE.md`, `05_CODEBASE_REFERENCE.md`, `11_DEVELOPMENT_GUIDE.md`, `20_AI_DEVELOPMENT_PLAYBOOK.md` |
| Data or exchange | `03_GLOSSARY_AND_ONTOLOGY.md`, `06_DATA_MODEL_AND_PERSISTENCE.md`, `19_INTEGRATIONS_AND_ECOSYSTEM.md`, canonical data contract and Skill coverage |
| UI/localization | `09_UX_UI_DESIGN_SYSTEM.md`, `10_INTERNATIONALIZATION.md`, canonical design rules and locale sources |
| QA, release, or incident | `12_TESTING_AND_QUALITY.md`, `18_KNOWN_ISSUES_AND_TECH_DEBT.md`, QA report, current plan section |
| Market/product claims | `15_PRODUCT_RESEARCH_AND_COMPETITION.md`, `16_PRODUCT_STRATEGY_AND_MARKETING.md`, then refresh canonical external citations |
| Data safety/security | `13_SECURITY_PRIVACY_RELIABILITY.md`, primary security/data contracts; do not infer a security audit |

Use the [Source Manifest](./SOURCE_MANIFEST.md) to identify primary authority and [Knowledge Gaps](./KNOWLEDGE_GAPS.md) for unresolved evidence.

## Import order and chunking

1. Import the Core Pack or Master Context, not both initially unless long context is available.
2. Load the topic page plus its primary source for implementation decisions.
3. Keep the Source Manifest and Known Gaps available when asking for claims or release readiness.
4. Do not upload all historical QA archives; use the current QA report plus a dated receipt only for a specific historical question.
5. After a source commit, update the header/source manifest and all affected summaries. Remove stale status context from the active Gemini knowledge base rather than layering contradictory current-status copies.

## Suggested Gemini instruction

> Treat this knowledge base as a dated, derived map, not the source of product authority. For each answer distinguish VERIFIED, DOCUMENTED, PLANNED, PROPOSED, INFERRED, UNKNOWN, and OBSOLETE evidence. Prefer current code/tests and the linked canonical Glide documents. Never claim a skipped, timed-out, focused, or local-only check as a green full platform run. Do not infer publication or owner approval from a template. Preserve local-first/product/data boundaries and flag conflicts.

## Data handling

Use only public repository material and synthetic examples. Do not upload real Glide data, local user paths, credentials, signing files, tokens, private audit evidence, or unsanitized test logs. A Core Pack does not authorize Gemini to modify files or send data to Glide.
