---
project: Glide
document_id: GLIDE-KNOWN-ISSUES
title: Known issues and technical debt
language: en
document_version: 1.0
source_commit: "4ce3697a11321686119313ae5a8e8c891413c85f"
verified_at: "2026-11-22"
status: verified-with-known-gaps
maintainer: project
related_documents: [GLIDE-TESTING, GLIDE-ROADMAP, GLIDE-ARCHITECTURE]
---

# Known issues and technical debt

Stand 22.11.2026 · Glide 1.0.1 · Aufgabenformat 26 · Quellstand 4ce3697a

This is a current-state summary for the checked snapshot. Exact historical outcomes and subsequent updates belong in the plan and QA report.

| Issue | Status / impact | Evidence or next verification |
|---|---|---|
| `test_ui39.py` full-run timeout (historical, PR #152) | Resolved by later rounds; full runs on macOS/Tk 9.1 and the CI matrix pass the suite. Details in the QA report. | – |
| V1.48 settings wrap fix | Delivered; covered by `schriftstile` in the work-mode suites. | – |
| DE/EN localization | Completed for 1.0 (V1.70–V1.81). | Report remaining German text with the localization issue form; keep catalogs and T335 in sync. |
| Release/distribution | No current tag or GitHub Release in checked status; Homebrew/winget templates are unsubmitted. | Owner-controlled approval, package acceptance, and publication gates remain. |
| macOS package and full QA | Previous package-start attempt on an older merge commit failed on a stale localized accessibility-name expectation; PR #151 corrected the probe, but current-head native macOS package/full run is not evidenced. | Run only after required platform checks are green; retain exact artifacts and probe evidence. |
| GitHub homepage | Bilingual README structural test passes, but the owner observed the live homepage still does not match the requested visual prompt. | Review complete original design prompt and repository preview; do not claim visual acceptance. |
| Large UI host | `app.pyw`/`ListApp` remain substantial integration surface. | Extract only where approved; preserve facades and mutation routes. |
| Shell package | Shell modules exist inside Glide, but separate `glide_shell` package/host is a later goal. | Track only in approved roadmap; do not describe target architecture as shipped. |

Other risks and older failed runs are dated in `src/glide/README.md` and `docs/07_QA_BERICHT.md`. A passing focused test clears only its defined scope.
