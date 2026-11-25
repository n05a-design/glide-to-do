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

Stand 24.11.2026 · Glide 1.0.3 · Aufgabenformat 26 · Quellstand 5631333a

## Open evidence gaps

| Gap | Current state | What would close it |
|---|---|---|
| Full Linux/Windows timeout | Historical `test_ui39.py` runs reached 900 seconds on both platforms at `5631333a`; the updated isolated test passed on Linux/Tk 9.1 and Windows/Tk 9.1 at `042a8d7`, with its callback-error assertion enabled. Local V1.52 accepts callbacks invoked without an event object and preserves the assertion; T124 direct no-argument Tcl checks and six final-code macOS/Tk 9.0.3 UI39 runs passed. On prior head `cada01bf`, full workflow #44530090137 captured `RoundedButton.__init__.<locals>.<lambda>() missing 1 required positional argument: '_event'` in Linux `test_ui39.py`; Windows was canceled after the next push. At current head `dd469d12`, focused #44538762234 passed Linux and Windows UI39; full #44538664389 passed basic CI, with Linux full validation still running and Windows not yet started. Why Tk/Tcl omitted event substitutions remains UNKNOWN until full validation completes. | Await the Linux full workflow and subsequent Windows/full validation; resolve failures from exact completed logs |
| Focused workflow final result | #44538762234 passed UI39 on Linux/Tk 9.1 and Windows/Tk 9.1 at corrected head `dd469d12`; older #44518533866 has Linux failed and Windows running on `5631333a` | Focused pass is not the full platform validation; read the older Windows result only as historical context |
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
| Version on `main` vs PR | `main` at `98f4b816`, System V1.47 | PR #152 remote head `dd469d12` includes the V1.48 code candidate plus V1.49/V1.50 follow-ups and the V1.52 callback fix | Different refs; V1.48–V1.52 are not on `main` |
| Targeted local vs remote full test | The original local macOS run blocked in a modal error notice; later runs showed Tk/Tcl invoking bindings without event arguments. V1.52 handles that no-data case; six final-code local UI39 runs and the corrected focused Linux/Windows UI39 dispatch passed. The reason event substitutions are absent is UNKNOWN; the full workflow basic stage passed while Linux full validation remained in progress | The earlier isolated Linux/Windows diagnostic passed, while older full jobs timed out | The corrected focused run verifies UI39 for Linux/Windows but does not explain the missing event substitutions or clear the full-matrix gap |
| V1.48 fix vs PR check | Dialog fix passed targeted macOS tests | New full jobs timed out in `test_ui39.py` before later suites | The timeout is not proof the fix failed or passed remotely |
| Release | Source cut merged to `main` | No tag/Release or package-manager submission observed | “Source cut” is not “published release” |
| Localization | DE/EN framework and some views | Other UI strings still German/English-incomplete | Partial, not full |
| Shell modules | Several modules extracted in Glide | `glide_shell` package/host not built | Current modules are not a released shared integration |

## Unverified areas

No independent audit was performed here of every feature row, every schema field, every import parser, every package file, all external market links, full license chain, all application UI strings, or every historical decision. Treat any question requiring such proof as UNKNOWN until its primary source and actual checks are examined.
