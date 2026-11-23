---
project: Glide
document_id: GLIDE-INTEGRATIONS
title: Integrations and ecosystem
language: en
document_version: 1.0
source_commit: "4ce3697a11321686119313ae5a8e8c891413c85f"
verified_at: "2026-11-22"
status: documented-with-known-gaps
maintainer: project
related_documents: [GLIDE-DATA, GLIDE-I18N, GLIDE-ARCHITECTURE]
---

# Integrations and ecosystem

Stand 23.11.2026 · Glide 1.0.2 · Aufgabenformat 26 · Quellstand 4ce3697a

## Runtime and desktop

Glide uses Python/Tk and local filesystem APIs. `tkinterdnd2` is an optional dependency for drag-and-drop from Finder/Explorer; it is not required for core data functionality. Native menus, app launch, clipboard, and some image/preview behavior are provided by the operating system adapters or its installed tools.

## User-directed file formats

| Format or route | Role | Boundary |
|---|---|---|
| `.glideexchange` | Exchange document/package for supported Glide data | Version 2; validation, preview and schema/field mapping required |
| `.glidecontext` | Context-driven change proposal | User reviews proposed changes; not direct AI write access |
| Markdown/TXT | Page/note import/export | Parsing and supported block conversion may be lossy |
| CSV | Tabular import/export | Not a complete backup or arbitrary object round trip |
| ICS | Calendar busy-time input and task calendar export | File-based; not a subscription or sync channel |
| Notion archive | Import from an exported archive | Archive and content limits apply |
| JSON Canvas | Pinboard interchange | Export loss report applies |
| Glide backup | Full app recovery | Local backup is not remote disaster recovery |

Exact capabilities and limits belong in [`06_DATA_BACKUP_MIGRATION.md`](../../06_DATA_BACKUP_MIGRATION.md) and [`20_FUNKTIONEN.md`](../../20_FUNKTIONEN.md).

## AI ecosystem

The `glide-to-do` skill generates/imports supported documents for external agent tools, including Claude Desktop, Cursor, Gemini CLI and web LLM workflows. It is not a Glide API, MCP server, or automatic remote connection. The app does not send task data to an AI service. User-reviewed export/import is explicit. Schema 26 changes are coupled to `abdeckung.json`, Skill references/examples, and tests.

## Build and public ecosystem

GitHub Actions validate source and prepare release/package paths. Homebrew Cask and winget manifests are repository templates; no external submission was recorded. No published current release, release tag, or service integration should be assumed. The package's local ad-hoc macOS signature is not Developer ID signing or notarization.

## Glide Shell

The reusable shell is the subpackage `glide_shell` 0.6.2; follow-up projects copy it with `scripts/pflege/shell_uebernehmen.py` and check the copy with `python -m glide_shell.selftest`. There is no separate repository or release; D99 closes the shell work.
