---
project: Glide
document_id: GLIDE-GAPS
title: Knowledge gaps and contradictions
language: en
document_version: 1.0
source_commit: "5631333a1c5a80c11c48226016ab115c434b0a64"
verified_at: "2026-11-19"
status: verified-with-known-gaps
maintainer: project
related_documents: [GLIDE-SOURCE-MANIFEST, GLIDE-AUDIT, GLIDE-ROADMAP]
---

# Knowledge gaps and contradictions

Stand 19.11.2026 · Glide 1.0.0 · Aufgabenformat 26 · Quellstand 5631333a

## Open evidence gaps

| Gap | Current state | What would close it |
|---|---|---|
| Full Linux/Windows timeout | Historical `test_ui39.py` runs reached 900 seconds on both platforms at `5631333a`; the updated isolated test passed on Linux/Tk 9.1 and Windows/Tk 9.1 at `042a8d7`, with its callback-error assertion enabled. Local macOS still shows a modal `_show_error_notice` blocking `root.update()` after the light theme; triggering callback exception UNKNOWN. In the new Linux full run, `apt-get update/install` received HTTP 503 responses from Ubuntu package sources and exited 100 before tests; the later calibration step failed because the suite-result file was absent. Windows full run was still in progress at last check. | Keep historical red evidence; rerun the Linux full job after Ubuntu package sources recover, complete Windows full run, and investigate the macOS callback cause only if reproducible |
| Focused workflow final result | #44518533866 passed UI/UX contracts but its work-mode step was still running at last check | Read its completed status and record exact run result; it is not the full `test_ui39` validation |
| V1.48 Linux evidence | Targeted macOS case passed; current Linux full run stopped during prerequisite package installation before any test suite | Updated Linux full run including working-mode case |
| Native current-head Mac package | Prior package probe used an older commit and failed on a localized expectation; a fix was pushed but current head is not proven here | Native package build, isolated start test, artifact digest and package/source comparison on the current accepted head |
| Full DE/EN coverage | Catalog mechanism and selected UI are localized; remaining dialogs/messages exist | Complete approved scope inventory with DE/EN visible tests and native review |
| GitHub homepage visual fidelity | User reports the live page still does not match the requested prompt; only structural/link validation is cited | Compare live repository page against original prompt/design refs and verify at intended viewport; owner visual approval |
| External distribution | Homebrew/winget are prepared repository manifests; no submission or release recorded | Owner-approved submissions and provider-confirmed result |
| Market facts | Canonical report is dated and external facts age | Refresh citations/dates before current comparative or quantitative claims |
| Glide Shell package | Modules exist in Glide; standalone package/host is a later target | Approved roadmap package and implementation/test evidence |
| Broad native UX/accessibility | Automated contracts cover subsets; complete human/native acceptance is not evidenced | Owner's documented visual, DPI, keyboard, screenreader and device pass |

## Important distinctions (not contradictions to resolve by guessing)

| Topic | Evidence A | Evidence B | Correct interpretation |
|---|---|---|---|
| Version on `main` vs PR | `main` at `98f4b816`, System V1.47 | PR #152 head `042a8d7` includes the V1.48 code candidate and V1.49 diagnostic follow-up | Different refs; V1.48 and V1.49 are not on `main` |
| Targeted local vs remote full test | Local macOS `test_ui39.py` blocked in a modal error notice; triggering callback exception UNKNOWN | Updated isolated Linux/Windows diagnostic passed, while older full jobs timed out | Targeted test is green on those two platforms; it does not identify the macOS callback cause or clear the full-matrix gap |
| V1.48 fix vs PR check | Dialog fix passed targeted macOS tests | New full jobs timed out in `test_ui39.py` before later suites | The timeout is not proof the fix failed or passed remotely |
| Release | Source cut merged to `main` | No tag/Release or package-manager submission observed | “Source cut” is not “published release” |
| Localization | DE/EN framework and some views | Other UI strings still German/English-incomplete | Partial, not full |
| Shell modules | Several modules extracted in Glide | `glide_shell` package/host not built | Current modules are not a released shared integration |

## Unverified areas

No independent audit was performed here of every feature row, every schema field, every import parser, every package file, all external market links, full license chain, all application UI strings, or every historical decision. Treat any question requiring such proof as UNKNOWN until its primary source and actual checks are examined.
