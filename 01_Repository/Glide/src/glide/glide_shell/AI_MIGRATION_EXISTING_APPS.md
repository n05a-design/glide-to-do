# Glide Shell – moving an existing application onto the shell (guide and start prompt for AI agents)

Status as of 27.11.2026 · Glide 1.0.3 · Glide-System V1.92 · Glide Shell 0.9.0 · Glide Bento 0.3.0 · [Deutsche Fassung](KI_MIGRATION_BESTEHENDE_ANWENDUNG.md)

This file is for applications that **already exist** with their own interface, such as STEPS or Chess & Chains. For a new project, use [AI_GUIDE_NEW_PROJECTS.md](AI_GUIDE_NEW_PROJECTS.md). Both files are part of the shell package and arrive with every takeover. The German version is authoritative.

## 1. The idea

The Glide Shell is the application's foundation, not a library to pick single parts from. Wrong: the application keeps its own theme system, buttons and window handling and imports a few shell modules on the side. That gives you two theme systems, two kinds of buttons and conflicting rules. Right: the existing **domain logic** moves into the shell architecture in a controlled way, and the application's own general UI parts are replaced step by step. The domain logic is not rewritten.

Binding: the [shell-first contract](DESIGN_RICHTLINIEN.md#5-shell-first-vertrag-d105-d106) (dependencies, decision order, exceptions), the design rules in [DESIGN_RICHTLINIEN.md](DESIGN_RICHTLINIEN.md) and the module table in [README.md](README.md).

## 2. Steps

| Step | What | Record |
|---|---|---|
| 1 | Inventory domain functions (each function, its entry point, its data) | list in the project's `docs/` |
| 2 | Inventory data models and storage locations | schema, format version, paths, backups |
| 3 | Check and run existing tests | baseline green or with named gaps |
| 4 | Split UI parts: **general** (window, dialog, button, field, menu, shortcut, colours, scrolling) vs. **domain** (board, notation, chord grid …) | mapping table |
| 5 | Name competing framework functions: own theme table, dialog factory, undo stack, path logic | list with the matching shell module |
| 6 | Take over the shell (and Bento when needed): `python3 -B <glide>/01_Repository/Glide/scripts/pflege/shell_uebernehmen.py --mit-bento <project>/src/<app>` | `SHELL_MANIFEST.json`, `BENTO_MANIFEST.json` |
| 7 | Build the host on `app_host` (main window, start checks, menu, shortcuts, quit) | start through the app host |
| 8 | Connect domain logic: existing modules stay, the host calls them | no domain logic in shell or Bento |
| 9 | Move views to shell modules one by one (`modal_session`, `custom_controls`, `desktop_adapter`, `window_geometry`, `command_history` …) | before/after note per view |
| 10 | Pass colours as a role dictionary to shell and Bento (`system_appearance.resolve`, `BentoContext.for_host`) | one colour source |
| 11 | Use Bento where cards or grids fit the domain | – |
| 12 | Keep user data: back up before every switch, change formats only with migration and a way back | backup and test log |
| 13 | Compare behaviour before and after (same artificial data, same steps) | comparison log |
| 14 | Remove redundant general components only after a green comparison | removal list with reasons |
| 15 | Regression tests and `python -m glide_shell.conformance src/<app>` | "conform" |
| 16 | Native visual and interaction check on the target platforms | result per platform |

## 3. User data

- Never test with real user data; isolate the test data folder with an environment variable before importing the app module.
- Before the first start of the migrated version, make a byte-identical backup of the old data.
- An older version must not overwrite newer data (check the format version, otherwise read only).
- No function may get lost in the migration. If the shell lacks a module, the old solution stays until the framework is extended. Record that as an exception under section 5.5 of the shell-first contract.

## 4. Spotting competing components

Signs of a second general UI system: colour constants inside views, own `Toplevel` dialogs with `grab_set`, own scrollbars, own undo list, own platform switches for shortcuts, own window-size logic. Each hit gets its shell module or an exception entry. A native Tk widget by itself is not a violation. What counts is whether it does general work.

## 5. Required tests

1. `python3 -m glide_shell.selftest` in `src/<app>` (copy, manifest, geometry; also with `python3 -O`).
2. `python3 -m glide_bento.selftest` when Bento is taken over.
3. `python3 -m glide_shell.conformance src/<app>`: layers, public modules, cycles, versions.
4. `python3 -B <glide>/01_Repository/Glide/scripts/pflege/shell_uebernehmen.py --pruefen --mit-bento src/<app>`: copies unchanged.
5. The project's existing domain tests, still green.
6. One integration test per migrated view through the real entry point (start, interaction, close, data unchanged).

## 6. Done means

- The application starts through `app_host`; all dialogs run through `modal_session`.
- There is exactly one colour source; the theme colour works in every view.
- No general component exists twice; every exception is recorded with a reason.
- `conformance` reports "conform"; self-tests and domain tests are green.
- Every earlier function is reachable; the before/after comparison is documented.
- The native check is recorded per platform, open platforms are named.

## 7. Start prompt (paste into a new session)

```text
You are moving the existing Tk application "<project name>" at <path> onto the Glide Shell.
Shell source: <path to glide-to-do> (https://github.com/n05a-design/glide-to-do).

Read completely first:
1. 01_Repository/Glide/src/glide/glide_shell/AI_MIGRATION_EXISTING_APPS.md (this procedure),
2. …/glide_shell/DESIGN_RICHTLINIEN.md, section 5 "Shell-First-Vertrag",
3. …/glide_shell/README.md (modules) and, if cards are needed, …/glide_bento/README.md.

Rules:
- The shell is the foundation. No second general UI architecture, no copies of shell modules.
- Domain logic is kept and connected, not rewritten.
- Never touch user data; tests only with artificial data in an isolated data folder.
- If a module is missing: record an exception and report the need; do not build a general system yourself.
- After every step: self-tests, `python -m glide_shell.conformance src/<app>` and the domain tests.

Work through the 16 steps of section 2 in order. Before step 6, store the inventories from steps 1–5 in the
project and show them to me before you remove any general component.
The migration is done only when every point of section 6 is met and documented.
```
