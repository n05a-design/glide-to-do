---
project: Glide
document_id: GLIDE-SECURITY
title: Security, privacy and reliability
language: en
document_version: 1.0
source_commit: "5631333a1c5a80c11c48226016ab115c434b0a64"
verified_at: "2026-11-19"
status: documented-with-known-gaps
maintainer: project
related_documents: [GLIDE-DATA, GLIDE-TESTING, GLIDE-ISSUES]
---

# Security, privacy and reliability

Stand 19.11.2026 · Glide 1.0.0 · Aufgabenformat 26 · Quellstand 5631333a

## Data and privacy model

Glide is documented as local-first: user data lives outside the installation directory. The core product does not require an account or cloud service and does not automatically transmit task data. File-based exchange and opening a link are user-directed actions. This document is a repository-grounded summary, not a privacy/legal audit or GDPR determination.

## Trust boundaries and input handling

External files, archives, exchange documents, Markdown, ICS, CSV, Notion exports, images and drawings are untrusted input. Import paths have validation, explicit limits, preview/conflict checks and backup requirements. Archive path traversal protections and attachment naming/identity handling are documented in the system register. A request to “import” is not permission to overwrite the user's existing state.

## Persistence safeguards

- Store is outside program directories; tests isolate it via `GLIDE_DATA_DIR`.
- Writes are atomic and guarded by local ownership lock.
- Newer schemas open protected/read-only rather than being silently downgraded.
- Migrations and repair require preservation of original bytes.
- Backups are local; a backup on the same disk is not an independent disaster-recovery copy.
- The lock cannot coordinate unsynchronized copies on separate devices/cloud sync.

## Dependencies and secrets

Runtime dependencies are intentionally limited; `tkinterdnd2` is optional, with vendored source provenance and license records. Packaged resources include licensed fonts and native runtime components. Build pipelines inspect sources and license files. No signing certificates, tokens, passwords, or recovery codes may be committed; repository guidance keeps those actions outside source control.

## Reliability and diagnostics

Session markers and bounded diagnostic files can support investigation after an abnormal exit. They do not prove or reconstruct unsaved in-memory work. Failure to acquire a lock, validate data, back up before import, or write a protected format must remain explicit; do not convert failures into success-shaped defaults.

## Findings and unknowns

- The project has a documented security/privacy model and extensive data-integrity checks.
- This task did not perform a full threat model, dependency vulnerability scan, or legal compliance assessment.
- The current remote full run has a 900-second test timeout; that is a CI reliability issue with unknown test-internal cause, not a proven data security defect.
- Current behavior of every parser/format requires checking the specific code and tests before making security claims.

Primary references: [`01_PRODUCT_CONSTRAINTS.md`](../../01_PRODUCT_CONSTRAINTS.md), [`06_DATA_BACKUP_MIGRATION.md`](../../06_DATA_BACKUP_MIGRATION.md), `tests/tools/` import/fixture checks, and [`07_QA_BERICHT.md`](../../07_QA_BERICHT.md).
