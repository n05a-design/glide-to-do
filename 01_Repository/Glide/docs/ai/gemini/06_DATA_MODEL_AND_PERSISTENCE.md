---
project: Glide
document_id: GLIDE-DATA
title: Data model and persistence
language: en
document_version: 1.0
source_commit: "4ce3697a11321686119313ae5a8e8c891413c85f"
verified_at: "2026-11-22"
status: verified-with-known-gaps
maintainer: project
related_documents: [GLIDE-GLOSSARY, GLIDE-ARCHITECTURE, GLIDE-SECURITY]
---

# Data model and persistence

Stand 24.11.2026 · Glide 1.0.3 · Aufgabenformat 26 · Quellstand 4ce3697a

## Persisted stores

| Store | Contents |
|---|---|
| `liste_speicher.json` | folders, lists, points/tasks, labels, repeats, reminders, trash, history |
| `settings.json` | appearance, profile, view/start options, pinboards, section mapping, selected history |
| `vorlagen.json` | system and user templates |
| `attachments/` | local copies referenced by stable attachment IDs |
| `backups/` | automatic, schema, pre-import, and recovery backups |
| `window.conf`, `glide.lock`, `datenordner.json` | local window/session/ownership/path-pointer state; not ordinary portable task data |

The default user-data location is outside the installation directory and varies by OS. `GLIDE_DATA_DIR` is the supported test override. Never point tests at a real user directory.

## Core entities

Folders contain nested folders and lists. Lists have a fixed kind: task list, note, page, drawing, gallery, or board-related view. Points include task, long text, group, and heading. Tasks may carry due/planned dates and times, estimate/recorded time, importance, completion, labels, checklist, subtasks, repeats, reminders, attachments, references, and dependency/waiting links. Exact field inventory and field behavior are maintained by [`glide-aufbau.md`](../../../skills/glide-to-do/references/glide-aufbau.md), `abdeckung.json`, and [`06_DATA_BACKUP_MIGRATION.md`](../../06_DATA_BACKUP_MIGRATION.md).

## Version contracts

- Main data schema: `26`.
- Settings schema: `2`.
- Template format: `2`.
- Exchange format: `glide.exchange` version `2`.
- App backup format and drawing/page subformats have their own version contracts.

Do not conflate these versions with app version `1.0.2` or the independently versioned system catalog (V1.86 on `main`). Older app versions must not silently overwrite a newer data schema. A data-format change requires migration, pre-write backup, fixtures, old-reader behavior tests, and updates to Skill coverage/examples in the same change.

## Persistence guarantees and limits

**DOCUMENTED / CODE-VERIFIED at the referenced snapshot:** file saves use a same-directory temporary file and atomic replacement. A per-data-directory lock prevents recognized local concurrent writers; it does not coordinate two unsynchronized cloud copies across devices. The app protects files when format is newer, size/validation limits are exceeded, or pre-save backup fails. There is no distributed merge service.

Automatic saves and multiple file stores mean a failed save must be represented explicitly. A successful write of one file does not prove all follow-up UI or diagnostic actions succeeded. Preserve structured save results and dirty/undo state.

## Import and export

Supported paths include `.glideexchange` for new content, `.glidecontext` for context-based change proposals, Markdown/TXT pages, CSV, ICS, Notion archive, drawings, `.glidepage`, and backups. Export includes Markdown, CSV, TXT, ICS, printing/PDF through the system, JSON Canvas, and full Markdown exports. Each format has limits and lossy boundaries; backup is the complete recovery route where applicable.

Glide does not write user files directly on behalf of an AI agent. Import/restore paths validate, preview, and preserve originals before mutation. See [`20_FUNKTIONEN.md`](../../20_FUNKTIONEN.md) and the [integration map](./19_INTEGRATIONS_AND_ECOSYSTEM.md).

## Recovery and testing

Schema migration creates a prior byte copy and refuses to write if backup fails. Recovery after an unexpected exit detects local session state, checks the existing store, and preserves originals before explicit repair; it cannot guarantee recovery of unsaved memory. Test data must be synthetic and isolated. See [QA guidance](./12_TESTING_AND_QUALITY.md).
