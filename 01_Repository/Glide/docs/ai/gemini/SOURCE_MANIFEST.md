---
project: Glide
document_id: GLIDE-SOURCE-MANIFEST
title: Source manifest
language: en
document_version: 1.0
source_commit: "5631333a1c5a80c11c48226016ab115c434b0a64"
verified_at: "2026-11-19"
status: verified-with-known-gaps
maintainer: project
related_documents: [GLIDE-GEMINI-INDEX, GLIDE-GAPS, GLIDE-AUDIT]
---

# Source manifest

Stand 19.11.2026 · Glide 1.0.0 · Aufgabenformat 26 · Quellstand 5631333a

## Snapshot and authority

This collection describes the application/code baseline at topic-branch commit `5631333a1c5a80c11c48226016ab115c434b0a64`. PR #152 is open at remote head `cada01bfcf561c242f20590862892219399048eb`; the V1.49 diagnostic and V1.50 evidence/documentation follow-ups are already on the branch. The baseline carried the V1.48 candidate and was not `main`; `main` was at merge commit `98f4b816`, catalog V1.47. The local V1.51–V1.52 candidate updates `tests/integration/test_ui39.py`, `src/glide/app.pyw`, `tests/integration/test_befunde330.py`, `tests/tools/linux_gegenproben.py`, and their inventory/documentation. It reinstalls the test collector after app initialization and safely handles Tk callbacks invoked without event objects; direct Tcl regression checks, six local macOS UI39 runs, and the local CI basic stage passed. At current remote head, workflow #44530090137 reports Linux failed and Windows still running; focused workflow #44518533866 reports Linux failed and Windows still running. Failure logs were unavailable while the overall workflows remained active, so the current Linux causes are unknown and remote verification of V1.52 remains open. The reason event substitutions are missing is also unknown. Data format, app version, and release scope are unchanged. Refresh this manifest and affected summaries when the local candidate is delivered.

`RELATIVE PATH` entries are repository paths; links below resolve from this document. The leading sources are authoritative for their named subject. “Reviewed” means read as source, not a complete audit of every statement or line.

## Primary sources

| Authority | Repository path | Subject / use | Snapshot assessment |
|---|---|---|---|
| Workspace rules | [`AGENTS.md`](../../../AGENTS.md) | Product boundaries, work rules, completion gates | Reviewed; normative |
| Handoff | [`00_Arbeitsvorbereitung/Glide_Uebergabe.md`](../../../../../00_Arbeitsvorbereitung/Glide_Uebergabe.md) | Active state and next actions | Reviewed; dated operational pointer |
| Working direction | [`docs/ARBEITSRICHTUNG.md`](../../ARBEITSRICHTUNG.md) | Owner decisions D01–D93 | Reviewed; normative |
| Roadmap | [`00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md`](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) | Selected packages and implementation state | Reviewed; sole backlog |
| v1 milestone | [`00_Arbeitsvorbereitung/Glide_Meilenstein_v1_Plan.md`](../../../../../00_Arbeitsvorbereitung/Glide_Meilenstein_v1_Plan.md) | D93 release target and stages | Reviewed; normative |
| Product constraints | [`docs/01_PRODUCT_CONSTRAINTS.md`](../../01_PRODUCT_CONSTRAINTS.md) | Identity, boundaries, principles | Reviewed; normative |
| Architecture | [`docs/02_ARCHITECTURE.md`](../../02_ARCHITECTURE.md) | Current system architecture and Tk rules | Reviewed; current-state authority |
| Data contract | [`docs/06_DATA_BACKUP_MIGRATION.md`](../../06_DATA_BACKUP_MIGRATION.md) | Schemas, backups, migrations, exchange | Reviewed; normative |
| UI behavior | [`docs/20_FUNKTIONEN.md`](../../20_FUNKTIONEN.md) | User-visible feature behavior | Reviewed; normative |
| Design contract | [`docs/DESIGN_RICHTLINIEN.md`](../../DESIGN_RICHTLINIEN.md) | App-wide appearance and interaction rules | Reviewed; normative |
| System inventory | [`src/glide/README.md`](../../../src/glide/README.md) | Complete module, feature, component, risk, and test register | Reviewed; sole complete inventory |
| System version | [`GLIDE_SYSTEM_VERSION`](../../../GLIDE_SYSTEM_VERSION) | Independent catalog version | Product baseline V1.48; PR #152 diagnostic follow-up V1.49; prior evidence/catalog update V1.50; local callback-collector correction V1.51; no-event callback handling V1.52 |
| QA test plan | [`docs/05_QA_TESTPLAN.md`](../../05_QA_TESTPLAN.md) | Test layers and manual checks | Reviewed; procedure |
| QA report | [`docs/07_QA_BERICHT.md`](../../07_QA_BERICHT.md) | Actual dated runs and limitations | Reviewed; result authority |
| Release policy | [`docs/10_VEROEFFENTLICHUNG.md`](../../10_VEROEFFENTLICHUNG.md) | Packaging, licensing, GitHub, release gates | Reviewed; owner gates retained |
| Release notes | [`CHANGELOG.md`](../../../CHANGELOG.md) | Shipped/released version history | Reviewed; source publication distinction |
| Data model reference | [`skills/glide-to-do/references/glide-aufbau.md`](../../../skills/glide-to-do/references/glide-aufbau.md) | Skill-facing schema/object explanation | Reviewed; format-coupled |
| Skill coverage | [`skills/glide-to-do/abdeckung.json`](../../../skills/glide-to-do/abdeckung.json) | Field-level exchange coverage | Not independently re-derived here |
| Localization code | [`src/glide/i18n.py`](../../../src/glide/i18n.py) | Locale and catalog behavior | Referenced; requires code-level refresh after changes |
| Locale catalogs | [`resources/locales/de.json`](../../../src/glide/resources/locales/de.json), [`en.json`](../../../src/glide/resources/locales/en.json) | German and English strings | Referenced; coverage is not full-app acceptance |
| Shell target | [`docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md`](../../GLIDE_SHELL_FRAMEWORK_KONZEPT.md) | Planned Shell boundaries and migration | Reviewed; distinct from current architecture |
| Public docs | [`README.md`](../../../../../README.md), [`README.en.md`](../../../../../README.en.md) | German/English project homepage | Structural test documented; live visual acceptance open |
| Community process | [`.github/ISSUE_TEMPLATE/`](../../../../../.github/ISSUE_TEMPLATE/), [PR template](../../../../../.github/PULL_REQUEST_TEMPLATE.md) | Public GitHub workflows | Current repository source; external settings not inferred |
| Security model | [`SECURITY.md`](../../../SECURITY.md), [`SECURITY.md`](../../../../../SECURITY.md) | Local security boundaries and reporting | Reviewed; not a security audit |
| Market research | [`00_Arbeitsvorbereitung/Glide_Markt_und_Vorbilder.md`](../../../../../00_Arbeitsvorbereitung/Glide_Markt_und_Vorbilder.md) | Dated external comparisons and suggestions | Indexed only; facts require refresh at use time |

## Test evidence referenced

The historical full-run failure is workflow #44506873603, PR head `5631333a`, Linux/Tk 9.1 and Windows/Tk 9.1; both timed out after 900 seconds in `test_ui39.py`. The updated isolated diagnostic on PR head `042a8d7` passed on Linux/Tk 9.1 and Windows/Tk 9.1 with the callback-error assertion enabled. At current remote head `cada01bf`, full workflow #44530090137 reports Linux failed and Windows still running; focused workflow #44518533866 reports Linux failed and Windows still running. Failure logs were unavailable while the overall workflows remained active, so the current Linux causes are not known. The automatic PR run #44523300465 at an earlier head passed basic CI, Analyze, and CodeQL; Linux `apt-get update/install` received HTTP 503 responses from Ubuntu package sources and exited 100 before tests. The later calibration step failed because the suite-result file was absent. A local macOS run exposed a modal error-notice block in `wait_window`; the triggering callback exception remains unknown. See the [QA report](../../07_QA_BERICHT.md) for all limitations and links.

## Exclusions and evidence quality

- Historical receipts remain historical; do not rewrite them to match the current state.
- The source does not establish a current GitHub Release/tag, Homebrew/winget submission, human visual acceptance, or native current-head macOS package.
- No exact test coverage percentage or external market-size claim is asserted.
- This manifest contains no absolute machine path, real user data, token, or credentials.
