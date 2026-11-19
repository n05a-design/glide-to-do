---
project: Glide
document_id: GLIDE-TESTING
title: Testing and quality
language: en
document_version: 1.0
source_commit: "5631333a1c5a80c11c48226016ab115c434b0a64"
verified_at: "2026-11-19"
status: verified-with-known-gaps
maintainer: project
related_documents: [GLIDE-DEVELOPMENT, GLIDE-SECURITY, GLIDE-KNOWN-ISSUES]
---

# Testing and quality

Stand 19.11.2026 · Glide 1.0.0 · Aufgabenformat 26 · Quellstand 5631333a

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

## Current evidence at PR head 042a8d7 (product baseline 5631333a)

**Passed:** local macOS/CPython 3.14.5 `schriftstile` 1/1; `tests/unit/test_ui_design.py` 23/23; local CI basic stage exit 0 and delivery byte-equality. GitHub basic stage, CodeQL, and Analyze passed on the PR head.

**Targeted pass:** workflow #44523315466 passed `test_ui39.py` on Linux/Tk 9.1 and Windows/Tk 9.1 at PR head `042a8d7`. Both logs show completion of light and dark themes and the final `UI 3.9: OK`; the callback-error assertion remained enabled. An initial Linux dependency setup attempt encountered HTTP 503 from Ubuntu package sources, but its retry succeeded.

**Failed / incomplete:** The historical full workflow #44506873603 on Linux/Tk 9.1 and Windows/Tk 9.1 timed out after 900 seconds at `test_ui39.py`; 112 later steps were skipped on each. Test logs for that suite were empty. A local macOS run also blocked after completing the light-theme dropdown loops: the stack shows a scheduled `_show_error_notice` opening a modal `show_warning` dialog during `root.update()`. The callback exception that scheduled the notice remains UNKNOWN. The automatic PR run #44523300465 passed basic CI, Analyze, and CodeQL, but Linux `apt-get update/install` received HTTP 503 responses from Ubuntu package sources and exited 100 before tests. The later calibrated-expectations step also failed because the suite-result file was absent. Windows full validation was still running at last check. Focused UI/work-mode workflow #44518533866 passed UI/UX contracts; its work-mode step was still running. Neither targeted pass substitutes for the full matrix or resolves the macOS callback cause.

The external provenance check for `tkinterdnd2` in local CI could not fetch its source due a local SSL certificate verification failure; the rest of that CI baseline succeeded. This is a validation limitation, not evidence that the dependency is invalid.

## Release criteria and limits

Do not treat a test file's existence as a pass. Tie results to exact commit, platform, Python/Tk, command/workflow, and exit status. A failure stops subsequent integrated tests; skipped tests remain unverified. Automated geometry checks do not replace owner visual/interaction review, accessibility acceptance, multi-monitor/DPI checks, or an actual package install/start. No measured coverage percentage is asserted here.

Primary sources: [`05_QA_TESTPLAN.md`](../../05_QA_TESTPLAN.md), [`07_QA_BERICHT.md`](../../07_QA_BERICHT.md), [system test catalog](../../../src/glide/README.md#5-test--und-werkzeugkatalog).
