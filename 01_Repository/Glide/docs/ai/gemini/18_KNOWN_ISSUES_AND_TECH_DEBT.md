---
project: Glide
document_id: GLIDE-KNOWN-ISSUES
title: Known issues and technical debt
language: en
document_version: 1.0
source_commit: "5631333a1c5a80c11c48226016ab115c434b0a64"
verified_at: "2026-11-19"
status: verified-with-known-gaps
maintainer: project
related_documents: [GLIDE-TESTING, GLIDE-ROADMAP, GLIDE-ARCHITECTURE]
---

# Known issues and technical debt

Stand 19.11.2026 · Glide 1.0.0 · Aufgabenformat 26 · Quellstand 5631333a

This is a current-state summary for the checked snapshot. Exact historical outcomes and subsequent updates belong in the plan and QA report.

| Issue | Status / impact | Evidence or next verification |
|---|---|---|
| `test_ui39.py` full-run timeout | **Full-matrix gap remains.** Linux/Tk 9.1 and Windows/Tk 9.1 each exceeded 900 seconds on PR #152 head `5631333a`; 112 later checks skipped on each. On head `042a8d7`, isolated `test_ui39.py` passed on both platforms with the callback-error assertion intact. The local V1.52 correction keeps the post-initialization callback collector, tolerates missing event objects in wheel/trackpad and focus-redraw callbacks, and preserves the assertion. `test_befunde330.py` passed direct no-argument Tcl callback checks; final `test_ui39.py` passed 6/6 locally on macOS/Tk 9.0.3. Why Tk/Tcl invoked these callbacks without event substitutions remains UNKNOWN and remote verification is pending. At current remote head `cada01bf`, full workflow #44530090137 reports Linux failed and Windows running; focused #44518533866 also reports Linux failed and Windows running. Failure logs were unavailable while the overall workflows remained active, so their Linux causes are UNKNOWN. | Keep the 900-s full-suite limit and assertions. Deliver V1.52, run the isolated UI39 workflow on that corrected test, and resolve current failed jobs using their completed logs. Local passes do not resolve the historical full-run timeout or the missing-event cause. |
| V1.48 settings wrap fix | Local macOS targeted `schriftstile` and UI design tests pass; no current Linux full-run validation. | Focused workflow #44518533866 has Linux failed and Windows still running at the latest status check; logs were not yet available. Confirm the V1.48 case in the completed Linux/Windows work-mode or full run. |
| DE/EN localization | Partially implemented; remaining dialogs, dynamic messages, status/error text and accessibility-related copy remain. | Follow D93 scope and update both catalogs/tests; never claim full localization from catalog parity alone. |
| Release/distribution | No current tag or GitHub Release in checked status; Homebrew/winget templates are unsubmitted. | Owner-controlled approval, package acceptance, and publication gates remain. |
| macOS package and full QA | Previous package-start attempt on an older merge commit failed on a stale localized accessibility-name expectation; PR #151 corrected the probe, but current-head native macOS package/full run is not evidenced. | Run only after required platform checks are green; retain exact artifacts and probe evidence. |
| GitHub homepage | Bilingual README structural test passes, but the owner observed the live homepage still does not match the requested visual prompt. | Review complete original design prompt and repository preview; do not claim visual acceptance. |
| Large UI host | `app.pyw`/`ListApp` remain substantial integration surface. | Extract only where approved; preserve facades and mutation routes. |
| Shell package | Shell modules exist inside Glide, but separate `glide_shell` package/host is a later goal. | Track only in approved roadmap; do not describe target architecture as shipped. |

Other risks and older failed runs are dated in `src/glide/README.md` and `docs/07_QA_BERICHT.md`. A passing focused test clears only its defined scope.
