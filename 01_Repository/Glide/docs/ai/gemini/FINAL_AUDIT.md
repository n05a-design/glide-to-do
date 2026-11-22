---
project: Glide
document_id: GLIDE-AUDIT
title: Final audit summary
language: en
document_version: 1.0
source_commit: "4ce3697a11321686119313ae5a8e8c891413c85f"
verified_at: "2026-11-22"
status: verified-with-known-gaps
maintainer: project
related_documents: [GLIDE-GEMINI-INDEX, GLIDE-SOURCE-MANIFEST, GLIDE-GAPS]
---

# Final audit summary

Stand 22.11.2026 · Glide 1.0.1 · Aufgabenformat 26 · Quellstand 4ce3697a


**Status refresh 22.11.2026:** Version, localization, shell and release facts were refreshed against `main` `4ce3697a` (Glide 1.0.1, catalog V1.83, `glide_shell` 0.5.0); a second refresh on 22.11.2026 recorded catalog V1.84 and `glide_shell` 0.6.0 with command history and app host (D99). The PR #152 statements below are historical.
## Scope and result

The collection has a file for each requested topic ID 01–20 and supporting index, source manifest, gap register, Gemini import guide, changelog, audit and compact core pack. It is an English, evidence-linked derivative of the Glide project sources. It separates documented current behavior from plans, proposals, historical evidence, unknowns, and owner-controlled release gates.

**Content audit: partial / bounded.** The broad source domains are represented, but this is not an exhaustive independent verification of every feature row, data field, UI string, external claim, license, security property, test, or historical decision. Known absences and contradictions are explicitly listed in `KNOWLEDGE_GAPS.md`.

**Technical audit: passed for the local documentation/tooling baseline only.** The repository CI basic stage passed after the central documentation index was expanded to list every Gemini file. It checked Markdown links, stand rules, privacy, and the repository's tool and unit-test gates. This does not certify exhaustive content accuracy, the full platform matrix, release readiness, or human acceptance.

**Remote status refresh:** PR #152 is currently at remote head `dd469d12`. Earlier isolated workflow #44523315466 passed `test_ui39.py` on Linux/Tk 9.1 and Windows/Tk 9.1 at `042a8d7`, with the callback-error assertion enabled. On prior head `cada01bf`, Linux workflow #44530090137 failed in `test_ui39.py` with `RoundedButton.__init__.<locals>.<lambda>() missing 1 required positional argument: '_event'`; the Windows full job was canceled after the later push. The corrected focused workflow #44538762234 passed UI39 on Linux/Tk 9.1 and Windows/Tk 9.1. Full workflow #44538664389 passed its basic stage; its Linux full-validation job was still running at this snapshot and Windows full validation had not started. The older focused run #44518533866 on `5631333a` has Linux failed and Windows still running. The earlier automatic PR run #44523300465 at `042a8d7` had Linux `apt-get update/install` HTTP 503 responses and exited 100 before tests; calibration failed because no suite-result file existed. The earlier 900-second full-run timeouts on `5631333a` remain historical red evidence. Local V1.52 handling tolerates callbacks with no event object while preserving the UI39 assertion; direct Tcl-callback regression checks and six final-code macOS/Tk 9.0.3 UI39 runs passed. The reason for missing Tcl event substitutions remains unknown.

**Current local V1.52 verification:** The CI basic stage passed on macOS/CPython 3.14.5 after the scroll mutation anchor was updated to retain the new no-event guard. It checked syntax across 447 Python files, version consistency, 707 local Markdown links and indexes, tool/unit tests, static checks, Tk startup/probe, delivery, privacy, storage and synchronization. `test_glide_system.py` passed 5/5, `test_linux_gegenproben.py` 4/4, `test_befunde330.py` passed, and `test_ui39.py` passed 6/6. The external provenance check for `tkinterdnd2` remained unverified because of a local SSL certificate error; the candidate-vs-delivery-copy difference was a permitted warning.

**Validation evidence (19 Nov 2026, macOS / Python 3.14.5):**

```text
tmp=$(mktemp -d /tmp/glide-ci.XXXXXX)
mkdir -p "$tmp/data"
cd 01_Repository/Glide
GLIDE_DATA_DIR="$tmp/data" python3 -B tests/tools/ci_grundstufe.py --protokoll "$tmp/protokoll"
Exit status: 0
```

The final run checked 707 local Markdown links and all indexed documents, then passed fixtures, tool tests, domain unit tests, timezone-independent tests, static analyses, stand/attribute/duplicate checks, Tk startup, delivery-copy synchronization, privacy, and archive checks. `tkinterdnd2` origin verification was skipped because the local SSL certificate chain prevented fetching its original package; this was reported as a non-blocking note. A preceding run exposed missing per-file index entries; those links were added before the successful final run.

## Coverage matrix

| Requirement | Coverage | Limit |
|---|---|---|
| Project identity and user use cases | `01`, Core Pack | Not a customer study |
| Architecture, codebase and data model | `04`–`06` | No full call graph or field-by-field re-audit |
| Features and workflows | `07`–`08` | Canonical 148-row register not duplicated |
| Design and i18n | `09`–`10` | UI visual acceptance and complete localization remain open |
| Development, tests, security/reliability | `11`–`13` | Not a security or compliance audit |
| Roadmap, market, strategy, decisions | `14`–`17` | Dated source references; external claims need refresh |
| Issues, integrations, AI playbook | `18`–`20` | Snapshot-bound and not execution authorization |
| Provenance, gaps, import and maintenance | support docs | Commit must be refreshed when source changes |

## Required follow-up for this audit file

Preserve the unresolved red GitHub full workflow in the same report; documentation CI cannot clear it. Re-run the source and relative-link audit after any later source/document edits.
