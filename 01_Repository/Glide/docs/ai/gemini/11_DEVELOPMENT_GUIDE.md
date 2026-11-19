---
project: Glide
document_id: GLIDE-DEVELOPMENT
title: Development guide
language: en
document_version: 1.0
source_commit: "5631333a1c5a80c11c48226016ab115c434b0a64"
verified_at: "2026-11-19"
status: documented-with-known-gaps
maintainer: project
related_documents: [GLIDE-TESTING, GLIDE-ARCHITECTURE, GLIDE-PLAYBOOK]
---

# Development guide

Stand 19.11.2026 · Glide 1.0.0 · Aufgabenformat 26 · Quellstand 5631333a

## Environment

The reference runtime is CPython 3.14 with Tk 9.1 for native full validation. Basic CI also checks Tk 8.6; this is not equivalent to the Tk 9.1 platform matrix. Windows, macOS, and Linux are supported/prepared desktop environments, but native runners and human acceptance are separate.

No separate application package manifest is required for basic development. Runtime is primarily Python standard library plus optional `tkinterdnd2`. Build dependencies are pinned in packaging workflows.

## Source layout and launch

Canonical code is in `01_Repository/Glide/src/glide/`. The principal UI is `app.pyw`; `glide_start.py` is the normal bootstrap path. `07_Python-Versionen/` is the separately tracked Python delivery copy, synchronized only under a production round.

Use the repository's own launch and test scripts. For tests, set `GLIDE_DATA_DIR` to a short temporary directory before the app is imported, and use `python3 -B` (or `python -B` in CI) to avoid bytecode artifacts.

## Focused validation examples

From `01_Repository/Glide`:

```sh
GLIDE_DATA_DIR=/tmp/glide-test-data python3 -B tests/integration/test_arbeitsmodi.py --fall schriftstile
GLIDE_DATA_DIR=/tmp/glide-test-data python3 -B tests/unit/test_ui_design.py
GLIDE_DATA_DIR=/tmp/glide-test-data python3 -B tests/tools/ci_grundstufe.py --protokoll /tmp/glide-ci
```

Use unique synthetic directories for independent runs. Platform-specific commands and full validation steps are maintained in [`05_QA_TESTPLAN.md`](../../05_QA_TESTPLAN.md) and [`07_QA_BERICHT.md`](../../07_QA_BERICHT.md). Do not use the exact sample directory concurrently or put test data in the repository.

## Engineering workflow

1. Read `AGENTS.md`, the handoff, working direction, development plan, document-maintenance matrix, relevant contract, and callers.
2. Identify existing patterns and stable IDs; decide whether the change touches data format, design, locale, system inventory, or the delivery copy.
3. Make the smallest change at the existing boundary. Domain logic is Tk-free and unit-tested (D17); retain app mutation and compatibility facades.
4. Add focused regression evidence and update `CHANGELOG.md` plus the applicable authoritative docs.
5. Run syntax checks and the narrowest relevant tests, then CI basic stage. For UI behavior, perform native tests on the affected platform and state untested limits.
6. Keep commits on the approved topic branch. Never push directly to `main`. PRs and merges follow repository policy; release and external account actions need explicit authorization.

## Platform and repository cautions

- Use `python3 -B` for repository tools and synthetic data.
- OneDrive paths can exceed sync or Windows path limits; put test/QA material in short local temporary roots and copy only permitted flat evidence to the repository.
- Never stage protected graphics/audit folders, real user data, local logs, tokens, certificates, or private paths.
- Do not overwrite an independent package with a macOS pre-stage build.
- The app checks and runtime/package versions must match the documentation and delivery copy.

This is not a complete setup/install guide for every platform. The repo's package README and workflow files are authoritative for native build prerequisites.
