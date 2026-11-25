---
project: Glide
document_id: GLIDE-TESTING
title: Testing and quality
language: en
document_version: 1.0
source_commit: "4ce3697a11321686119313ae5a8e8c891413c85f"
verified_at: "2026-11-22"
status: verified-with-known-gaps
maintainer: project
related_documents: [GLIDE-DEVELOPMENT, GLIDE-SECURITY, GLIDE-KNOWN-ISSUES]
---

# Testing and quality

Stand 24.11.2026 · Glide 1.0.3 · Aufgabenformat 26 · Quellstand 4ce3697a

## Test architecture

Glide uses custom Python test tools rather than a blanket pytest collection. The repository has unit tests for Tk-free domain modules, many Tk integration suites, static/structural tools, CI scripts, fixture checks, native runtime and package-start checks. The system register lists 329 test/tool files in its current inventory; this is a file count, not test coverage.

## CI layers

- **Basic CI:** syntax/source count, version consistency, documentation links/index, fixtures, tools, unit logic, static audits, Tk start probe, delivery synchronization notice, privacy/storage checks.
- **Native full runs:** build/use own Tk 9.1 runtime on Linux and Windows and run the integrated suite. macOS native full QA/package is a separate workflow requiring a native Mac runner.
- **Focused runs:** workflows may select UI/work-mode or other specific stages. They are not substitutes for full gates unless the plan expressly says so.
- **Packages:** native build, source/runtime/libraries/license validation and isolated start probe are distinct from source test success.

## Reproducible commands

From `01_Repository/Glide`, first set `GLIDE_DATA_DIR` to a short synthetic temp directory:

```sh
python3 -B tests/tools/ci_grundstufe.py --protokoll /tmp/glide-ci
python3 -B tests/integration/test_arbeitsmodi.py --fall schriftstile
python3 -B tests/unit/test_ui_design.py
python3 -B tests/tools/pruefen.py --modus voll --protokoll /tmp/glide-full --timeout 900
```

Native full commands require the workflow's Tk runtime and desktop setup; use repository instructions rather than assuming a system Tk result is equivalent.

## Current evidence on `main` 4ce3697a (Glide 1.0.1, 22.11.2026)

The 1.0.1 release round ran the full suite on macOS arm64 with Tk 9.1 in foreground mode: all steps passed except one focus case (`kompakt_verlorenes_loslassen`), which cannot be observed while the screen is locked; it passed in an earlier run on the same app code. The macOS package passed its isolated start probe, the DMG was verified against the package, and `abgleich_07.py` reported no deviations. The CI basic stage and documentation workflow pass on `main`. Exact runs, hashes and limits are in the [QA report](../../07_QA_BERICHT.md).

## Historical evidence at PR head dd469d12 (product baseline 5631333a, 19.11.2026)

**Passed locally:** macOS/CPython 3.14.5 `schriftstile` 1/1; `tests/unit/test_ui_design.py` 23/23; CI basic stage exit 0 and delivery byte-equality. `test_befunde330.py` passed and `test_ui39.py` passed 6/6 on the final local V1.52 candidate. These local results do not establish remote or cross-platform verification.

**Historical targeted pass:** workflow #44523315466 passed `test_ui39.py` on Linux/Tk 9.1 and Windows/Tk 9.1 at earlier PR head `042a8d7`. Both logs show completion of light and dark themes and the final `UI 3.9: OK`; the callback-error assertion remained enabled. An initial Linux dependency setup attempt encountered HTTP 503 from Ubuntu package sources, but its retry succeeded. This did not test the local V1.52 code.

**Remote findings and current status:** On prior remote head `cada01bf`, full workflow #44530090137 failed Linux in `test_ui39.py`; the callback assertion captured `RoundedButton.__init__.<locals>.<lambda>() missing 1 required positional argument: '_event'`. The Windows full job was canceled after the subsequent push. At current head `dd469d12`, focused workflow #44538762234 passed UI39 on Linux/Tk 9.1 and Windows/Tk 9.1. Full workflow #44538664389 passed basic CI; its Linux full-validation job was still running at this snapshot and Windows full validation had not started. The older focused workflow #44518533866 on `5631333a` has Linux failed and Windows still running. Earlier automatic PR run #44523300465 passed basic CI, Analyze, and CodeQL, but Linux `apt-get update/install` received HTTP 503 responses from Ubuntu package sources and exited 100 before tests; the calibrated-expectations step then failed because the suite-result file was absent.

**Historical red evidence:** Full workflow #44506873603 on Linux/Tk 9.1 and Windows/Tk 9.1 timed out after 900 seconds at `test_ui39.py`; 112 later steps were skipped on each. Test logs for that suite were empty. A local macOS run also blocked after completing the light-theme dropdown loops: the stack shows a scheduled `_show_error_notice` opening a modal `show_warning` dialog during `root.update()`. The callback exception that scheduled the notice remains UNKNOWN. Neither an isolated targeted pass nor local V1.52 runs substitute for the full matrix or resolve the original callback cause.

**Local callback correction (V1.52):** `ListApp.__init__` replaces a callback handler installed before construction, so the former test handler did not prevent the app's modal error notice. `test_ui39.py` now reinstalls its collector on the root after initialization, prints full tracebacks, and retains the callback-error assertion. Further diagnosis showed Tkinter invoking registered callbacks without event arguments (`args=()`), observed for `<Button-4>`, `<Button-5>`, and `<TouchpadScroll>`; another run reported a `RoundedButton` focus redraw callback without its unused event parameter. The app now treats missing event data as a no-op for wheel/trackpad handling and focus redraw. `test_befunde330.py` directly exercises these Tcl commands without arguments and passed; `test_ui39.py` passed six uninstrumented macOS/Tk 9.0.3 runs after the final change. The T276 mutation anchor was updated to preserve the new event guard; its tool tests passed 4/4. The local CI basic stage then passed. The reason Tk/Tcl omitted event substitutions remains UNKNOWN. The new code has not been verified remotely.

The external provenance check for `tkinterdnd2` in local CI could not fetch its source due a local SSL certificate verification failure; the rest of that CI baseline succeeded. This is a validation limitation, not evidence that the dependency is invalid.

## Release criteria and limits

Do not treat a test file's existence as a pass. Tie results to exact commit, platform, Python/Tk, command/workflow, and exit status. A failure stops subsequent integrated tests; skipped tests remain unverified. Automated geometry checks do not replace owner visual/interaction review, accessibility acceptance, multi-monitor/DPI checks, or an actual package install/start. No measured coverage percentage is asserted here.

Primary sources: [`05_QA_TESTPLAN.md`](../../05_QA_TESTPLAN.md), [`07_QA_BERICHT.md`](../../07_QA_BERICHT.md), [system test catalog](../../../src/glide/README.md#5-test--und-werkzeugkatalog).
