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
| `test_ui39.py` full-run timeout | **Red / unresolved.** Linux/Tk 9.1 and Windows/Tk 9.1 each exceeded 900 seconds on PR #152 head `5631333a`; 112 later checks skipped on each. A local macOS run completed the light-theme dropdown loops, then blocked in a modal error notice during the dark-theme start. The callback exception that triggered the notice remains UNKNOWN. | The test now logs progress/stacks, suppresses the modal error notice, and retains callback-error assertions. Run the isolated Linux/Windows diagnostic dispatch to expose the triggering exception; do not raise the full-suite timeout or weaken assertions. |
| V1.48 settings wrap fix | Local macOS targeted `schriftstile` and UI design tests pass; no Linux full-run validation because the independent `test_ui39` timeout prevented later tests. | Focused workflow #44518533866 checked UI/UX contracts; work-mode result was pending at last status. Run the V1.49 targeted diagnostic then repeat full matrix. |
| DE/EN localization | Partially implemented; remaining dialogs, dynamic messages, status/error text and accessibility-related copy remain. | Follow D93 scope and update both catalogs/tests; never claim full localization from catalog parity alone. |
| Release/distribution | No current tag or GitHub Release in checked status; Homebrew/winget templates are unsubmitted. | Owner-controlled approval, package acceptance, and publication gates remain. |
| macOS package and full QA | Previous package-start attempt on an older merge commit failed on a stale localized accessibility-name expectation; PR #151 corrected the probe, but current-head native macOS package/full run is not evidenced. | Run only after required platform checks are green; retain exact artifacts and probe evidence. |
| GitHub homepage | Bilingual README structural test passes, but the owner observed the live homepage still does not match the requested visual prompt. | Review complete original design prompt and repository preview; do not claim visual acceptance. |
| Large UI host | `app.pyw`/`ListApp` remain substantial integration surface. | Extract only where approved; preserve facades and mutation routes. |
| Shell package | Shell modules exist inside Glide, but separate `glide_shell` package/host is a later goal. | Track only in approved roadmap; do not describe target architecture as shipped. |

Other risks and older failed runs are dated in `src/glide/README.md` and `docs/07_QA_BERICHT.md`. A passing focused test clears only its defined scope.
