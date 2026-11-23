# Glide Shell – Guide for AI agents in new projects

Status as of 22.11.2026 · Glide 1.0.2 · Glide-System V1.86 · Glide Shell 0.6.2 · [Deutsche Fassung](KI_ANLEITUNG_NEUE_PROJEKTE.md)

This guide is for AI agents (Claude Code, Codex, Cursor, Gemini and others) that build a **new** Tk desktop application on the Glide Shell. It explains how Glide, the Glide-System and the Glide Shell fit together, how to start a project, the architecture rules, the design rules, the working processes and the checks. It lives in the `glide_shell` package and is copied with every adoption. A ready prompt for the first session, with an overview of what lives where, is in [`STARTPROMPT_KI.md`](STARTPROMPT_KI.md). The German version is authoritative; this is its controlled English translation.

The authoritative sources stay in Glide; this guide summarizes and links them for follow-up projects. Where they disagree, the linked Glide documents apply. Many of them are written in German. Glide repository: <https://github.com/n05a-design/glide-to-do>.

---

## 1. The big picture

```text
Glide (the app)                 Glide-System (the inventory)          Glide Shell (the package)
src/glide/app.pyw               src/glide/README.md                   src/glide/glide_shell/
ListApp = controller            register: modules M…, features F…,    neutral Tk building blocks,
domain modules (Tk-free)        packages, tests T…, version history   no Glide values
data, views, texts              GLIDE_SYSTEM_VERSION (V1.86)          SHELL_VERSION (0.6.2)
        │                                 │                                  ▲
        └──── uses ───────────────────────┼──────────── host → shell → Tk ───┘
                                          └─ documents both, versioned independently
```

- **Glide** is a local desktop planner in Python/Tk. `ListApp` in `app.pyw` is the controller: it builds the views, holds the data and reacts to commands. Domain logic lives in many small, Tk-free modules with unit tests.
- **The Glide-System** is not code but the binding register of all modules, features, building blocks and tests, with its own version number ([`src/glide/README.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/src/glide/README.md)). Every change to modules, tests or the catalog raises `GLIDE_SYSTEM_VERSION` in the same commit.
- **The Glide Shell** is the reusable Tk foundation. It knows no Glide content; the host supplies texts, colors, checks and handlers. New projects adopt it as a copy.

Dependency direction without exception: **host → shell → Tk/standard library.** The shell never imports from the host.

---

## 2. Shell building blocks

| Module | Purpose | Main names | Host supplies |
|---|---|---|---|
| `app_host` | Start and end the main window (phase 5) | `AppHost` (`before_tk`, `preflight`, `splash`, `on_ready`, `run`), `bind_shortcuts`, `primary_shortcuts`, `attach_menubar`, `install_close`, `platform_of` | controller class, startup checks, shortcut table, close handler |
| `command_history` | Undo/redo (phase 4) | `Command`, `CommandHistory` (`execute`, `record`, `undo`, `redo_step`, `trim`, `clear`), `DONE`/`EMPTY`/`FAILED`/`HANDLED` | command objects, or `capture`/`apply`/`rollback` for snapshots |
| `modal_session` | Create dialogs, wait modally, return focus | `create_dialog`, `run_modal`, `wait_modal`, `modal_over` | title, background, error log |
| `window_lifetime` | Timers belong to a widget | `scope_for`, `AfterScope` | the owning widget |
| `motion` | Short, interruptible transitions (≤ 150 ms) | `Transitions`, `progress` | scheduling from the scope |
| `custom_controls` | Theme-aware canvas controls | `GlideCheckbutton`, `GlideRadiobutton`, `GlideListbox`, `GlideScale`, `ThemedAutoScrollbar` | font, ink, background via `set_*_provider` |
| `desktop_adapter` | Menu tree, shortcut labels, platform, clipboard, launching | `build_menu_tree`, `format_accelerator`, `primary_modifier`, `launch_path` | menu entries, action ids, labels |
| `window_geometry` | Geometry strings, keep windows on the work area | `parse`, `format_geometry`, `clamp`, `keep_visible` | minimum size |
| `system_appearance` | System light/dark mode | `tk_is_dark`, `windows_is_dark`, `linux_is_dark`, `resolve` | theme pair |
| `redo_history` | Validity of the redo stack | `RedoHistory` | – (used inside `command_history`) |
| `text_fit` | Fit text to a character or pixel width | `clip`, `fit`, `settled_wrap_width`, `aligned_markers` | measure function |
| `action_picker` | Searchable action picker from a menu | `entries`, `search`, `grouped`, `first_enabled` | menu rows, placeholders |
| `runtime_paths` | Data and cache folders without side effects | `platform_data_dir`, `platform_cache_dir`, `resolve_base` | product name, variable and file names |
| `selftest` | Check the copy on the target machine | `python -m glide_shell.selftest` | – |
| `demo` | Runnable example built only from the shell | `python -m glide_shell.demo` | – |

The binding list of every public function with its parameter names is `SHELL_MODULE` in [`tests/unit/test_shell_importregel.py`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/tests/unit/test_shell_importregel.py) (T319).

---

## 3. Starting a new project

### 3.1 Recommended layout (following Glide)

```text
<project>/
  AGENTS.md                binding working rules and completion criterion (model: Glide AGENTS.md)
  CLAUDE.md                additions for Claude Code sessions, points to AGENTS.md
  VERSION                  app version (SemVer)
  SYSTEM_VERSION           version of your own register (V1.0 to start)
  src/<app>/
    app.py                 controller and views; starts through glide_shell.app_host
    <domain>.py            Tk-free domain modules
    glide_shell/           unchanged copy including SHELL_MANIFEST.json
    resources/locales/     de.json, en.json (the host's texts)
    README.md              system register: modules M…, features F…, tests T…, version history
  tests/unit/              Tk-free tests, one per domain module
  tests/integration/       real Tk suites (own processes, synthetic data)
  tests/tools/             tool tests, base stage, full run
  docs/
    ARBEITSRICHTUNG.md     decisions D01… with date and source
    ENTWICKLUNGSPLAN.md    the single task plan with § sections
    FUNKTIONEN.md          behavior from the user's view (leads the manual)
    DESIGN_RICHTLINIEN.md  design contract (section 5)
    QA_BERICHT.md          actual runs with commit, platform and limits
    DOKUMENTENPFLEGE.md    maintenance matrix: leading source per topic and dependent references
  CHANGELOG.md
```

Create only what the project needs, but every statement has **exactly one leading source**. Merge instead of maintaining in parallel.

### 3.2 Adopting the shell

```bash
python3 -B <glide>/01_Repository/Glide/scripts/pflege/shell_uebernehmen.py <project>/src/<app>                         # create or update
python3 -B <glide>/01_Repository/Glide/scripts/pflege/shell_uebernehmen.py --agent-bootstrap <project>/src/<app>      # includes AGENTS.md and agent skills
python3 -B <glide>/01_Repository/Glide/scripts/pflege/shell_uebernehmen.py --agent-bootstrap --project-root <root> <project>/src/<app>  # explicit project root
python3 -B <glide>/01_Repository/Glide/scripts/pflege/shell_uebernehmen.py --commit <REV> <project>/src/<app>         # adopt from a specific Git commit
python3 -B <glide>/01_Repository/Glide/scripts/pflege/shell_uebernehmen.py --pruefen <project>/src/<app>               # check only
cd <project>/src/<app> && python3 -m glide_shell.selftest                                                              # exit code 0 = all 13/13 checks passed
```

- The tool copies every `*.py` and `*.md` from `glide_shell/` (including `DESIGN_RICHTLINIEN.md` as an offline-accessible design contract) and writes `SHELL_MANIFEST.json` with package version, Glide-System version, source commit and SHA-256 per file.
- **Project root detection:** Passing `--agent-bootstrap` (or `--agenten-bootstrap`) automatically discovers the project root upwards using standard markers (`.git`, `pyproject.toml`, `setup.py`, `Pipfile`, `requirements.txt`, `AGENTS.md`, `CLAUDE.md`) or Python package heuristics (`src/<app>/glide_shell`). The project root can also be passed explicitly via `--project-root <PATH>` or `--projekt-root <PATH>` (placement inside the Glide source tree is rejected).
- **Dynamic relative links:** The generated `AGENTS.md` and agent skills (`.agents/skills/glide-shell/SKILL.md`, `.claude/skills/glide-shell/SKILL.md`) compute POSIX relative paths dynamically from their actual location to the adopted `glide_shell/` directory. All markdown links resolve cleanly across nested folder layouts and directory names with spaces (`%20`).
- **Transactional safety:** The adoption and bootstrap operation is atomic and transaction-managed (`BootstrapTransaction`). A complete snapshot is taken before mutations start; any read, write, or interruption triggers a complete rollback of created or modified files and directories without leaving partial state. Pre-existing user files are preserved and never overwritten unless `--ersetzen` is passed.
- **Manifest & trust boundaries:** `SHELL_MANIFEST.json` acts as the cryptographic trust anchor. The self-test (`selftest.py`) verifies SHA-256 digests for all modules, detects modifications, unmanaged subpackages or extraneous modules, and forbids symlinks. Consumer copies without a manifest exit with code 1; the source-tree exemption is spoof-proof.
- **Never edit the copy by hand.** Shell changes happen in Glide (approved by the Glide owner) and come back through the tool. `--pruefen` reports outdated or modified files; `--ersetzen` overwrites on purpose.
- License: MPL-2.0. Keep the `# SPDX-License-Identifier: MPL-2.0` header and the `LICENSE` file.

### 3.3 Application skeleton

The skeleton in the German version (section 3.3) runs unchanged; this is the same code with English comments.

```python
# src/<app>/app.py
import json
import os
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

from glide_shell import app_host, command_history, desktop_adapter, runtime_paths, window_lifetime

APP = "Example"
TEXTS = json.loads((Path(__file__).parent / "resources/locales/en.json").read_text(encoding="utf-8"))


def t(key):
    return TEXTS.get(key, key)


def data_dir():
    # Importing creates no folder; only the start decides (pattern WA-49).
    base, _forced = runtime_paths.resolve_base(None, os.environ, "EXAMPLE_DATA_DIR",
                                               runtime_paths.platform_data_dir(APP))
    return Path(base)


def check_tk(_root):
    return None if tk.TkVersion >= 8.6 else (t("start.title"), t("start.tk_too_old"))


class Increment(command_history.Command):
    def __init__(self, app):
        self.app = app

    def execute(self):
        self.app.count += 1
        self.app.refresh()

    def undo(self):
        self.app.count -= 1
        self.app.refresh()


class App:
    """Controller: builds the content inside the app host's window."""

    def __init__(self, root):
        self.root, self.count = root, 0
        self.scope = window_lifetime.scope_for(root)          # every timer of this window
        self.history = command_history.CommandHistory(limit=50)
        self.platform = app_host.platform_of(root.tk.call("tk", "windowingsystem"))
        root.title(t("app.title"))
        menus = []
        menubar = desktop_adapter.build_menu_tree(root, [
            (t("menu.edit"), [
                (t("menu.undo"), self.undo, desktop_adapter.format_accelerator("Z"), "undo"),
                (t("menu.redo"), self.redo, desktop_adapter.format_redo_accelerator(), "redo"),
            ]),
        ], menus_out=menus)
        app_host.attach_menubar(root, menubar)
        app_host.bind_shortcuts(root, app_host.primary_shortcuts("z", lambda _e: self.undo(), self.platform)
                                + app_host.primary_shortcuts("Z", lambda _e: self.redo(), self.platform, shift=True)
                                + [("<Escape>", lambda _e: self.request_close(), app_host.ALL)],
                                self.platform)
        app_host.install_close(root, self.request_close, self.platform, scope=self.scope)
        self.label = tk.Label(root)
        self.label.pack(padx=20, pady=20)
        tk.Button(root, text=t("action.add"), command=lambda: self.history.execute(Increment(self))).pack()
        self.refresh()

    def refresh(self):
        self.label.configure(text=t("count").format(count=self.count))

    def undo(self):
        return self.history.undo() == command_history.DONE

    def redo(self):
        return self.history.redo_step() == command_history.DONE

    def request_close(self):
        # Ask about unsaved changes here: build a dialog with modal_session.create_dialog
        # and wait with modal_session.run_modal(self.root, dialog).
        self.root.destroy()


def main():
    host = app_host.AppHost(
        before_tk=(),                                   # e.g. register private fonts (before the first Tk!)
        preflight=(check_tk,),                          # (title, message) stops with exit code 1
        show_error=lambda title, message, parent=None: messagebox.showerror(title, message, parent=parent))
    host.run(App)


if __name__ == "__main__":
    main()
```

For snapshots instead of commands (as Glide does): `CommandHistory(capture, apply, rollback, stack=lambda: self.undo_stack)`. `apply(state)` reports `True` only after a successful save; otherwise `rollback` restores memory and both stacks stay unchanged. Glide's `ListApp.command_history` in `app.pyw` is an example.

---

## 4. Architecture rules

These rules come from Glide, where tests enforce them. Adopt them with tests of your own.

1. **Domain logic is Tk-free and unit-tested** (Glide D17). New or touched logic lives in its own modules without `tkinter`; the controller calls it.
2. **Module budget** (Glide WA-50): at most 50 code lines per function, nesting depth at most 15. In Glide, `tests/tools/analyse_statisch.py --budget` with T322 checks it.
3. **Imports without side effects** (Glide WA-49): importing creates no folders, changes no Tk behavior and reads no pointer files. All of that happens at start in the controller or in `AppHost`.
4. **Start through `AppHost`.** Steps that must run before the first Tk interpreter (private fonts on macOS Aqua, the Windows application id) go into `before_tk`. Runtime and data folder checks go into `preflight`; they report and exit before any data is opened.
5. **Avoid a second `tk.Tk()` in the same process.** On macOS it is not stable (exit code 133 observed). Anything that must run before the window belongs in a separate process (pattern: Glide's showcase starter).
6. **Timers only through a scope** (`window_lifetime.scope_for(widget).after(…)`). Everything ends when the widget is destroyed; a raw `root.after` is a bug. Glide guards this with a ratchet in T319.
7. **Dialogs only through `modal_session`** (`create_dialog`, `run_modal`). No own `wait_window`, no raw `Toplevel` except tooltips.
8. **Motion ≤ 150 ms and interruptible** (`motion.Transitions` in the same scope). Reduced motion removes the movement, never the function.
9. **Undo through `CommandHistory`.** One step per user intention; a failed save leaves both stacks unchanged and reports the error.
10. **Data local, atomic and backed up.** Write through a temporary file and `os.replace`, back up before migrations, lock the data folder for writing. Glide's patterns: `persistence.py`, `data_lock.py`, `schema_backups.py` (not shell modules; read them as templates, do not import them).
11. **Texts belong to the host.** Shell modules receive finished labels. Localize through `de.json`/`en.json` catalogs with a parity test (pattern: Glide `i18n.py`, T329, T335). Developer messages in code are English.
12. **Do not import code from `glide` modules outside the shell.** If you need another Glide building block, request it in Glide as a new shell module (section 9).

---

## 5. Design rules

Glide's design contract and the portable design contract for consumer projects are documented in [`docs/DESIGN_RICHTLINIEN.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md) (German; see section [*Portabler Designvertrag für Folgeprojekte*](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md#portabler-designvertrag-für-folgeprojekte)). Adopt the principles into your project's own design document; concrete Glide sizes and decisions apply only if your project adopts them explicitly.

**Six principles (P1–P6):**

| Principle | Meaning for the interface |
|---|---|
| P1 Works as expected | The obvious action reaches the goal without hint text; system conventions apply (light/dark, Esc, Delete, shortcuts) |
| P2 Form follows function | Color = role, size = importance, position = relationship; no decoration by default |
| P3 No duplicate function | One primary path per intention; menu, shortcut and action picker mirror it (`action_picker` reads the menu, no second command list) |
| P4 No wasted space | Content before controls; controls above the content take at most 15 % at 1280 × 800 |
| P5 Only the essentials | The default shows what is needed; at most four icon buttons in the header |
| P6 Low complexity | Few stable terms; new features extend existing places |

**Binding rules every project needs:**

- **Protect controls (B15):** every button stays visible, readable and reachable in every intended window size; text must not cover it. Recompute positions after every rewrap.
- **Information hierarchy (B11):** title and content disappear last; metadata are as wide as their content and give way entirely when space is short instead of being clipped.
- **Alignment (B02, B05, B07–B09):** related items share edges, spacing and heights; the visual center of a symbol sits on the middle of the cap height, computed from glyph boxes, not from fixed pixel offsets.
- **Stable symbols (B10, B12, B14):** one symbol, one meaning; ◂/▸ page, ▸/▾ expand; characters from the font in use or a bundled symbol font.
- **Calm surfaces (B17, B19):** elements take the color of the surface they sit on; no accidental background rectangles.
- **Hints when needed (B06):** supplementary help can be switched off; required states and errors stay visible.
- **Predictable response (B01, B16):** feedback within the same event, no artificial delays, even scrolling.
- **Short toggle commands:** “Compact mode”, not “Compact mode on/off”.
- **From the market analysis (D83):** an empty area explains itself in one sentence with one button; bulk-changing dialogs show before/after and can be undone in one step; totals go into the section header; name overdue items neutrally; make time visible, not alarming.
- **Check worst-case data:** long titles, missing and long metadata, empty and full states, large font, the smallest window size.

**Evidence per touched UI package:** before implementing, name the affected rules; afterwards take real screenshots and check geometry with synthetic data in at least two window sizes (Glide: 860 × 700 and 1280 × 800), medium and large font, light and dark design, long texts. Screenshots and attributes do not replace human visual and operation acceptance.

---

## 6. Working processes

### 6.1 Assignment, decisions, plan

- **Only implement assigned work.** Open product choices belong to the owner, not the agent. A decision proposal names options, a recommendation and the effort.
- **Decisions** are numbered in `ARBEITSRICHTUNG.md` (D01, D02 …) with date, source and where they were implemented. When the range grows, update range mentions such as “D01–D12” in every entry document.
- **A single task plan.** Each cut gets a section with **A – Assignment**, **B – Implementation**, **C – Checks**, **D – Remainder**. Status marks: ✅ done, ◐ partial, ○ open, ◇ registered. Use ✅ only with evidence.

### 6.2 Versions

| Counter | When to raise it |
|---|---|
| App version (`VERSION`) | only in a production round (version switch, delivery sync, checksums) |
| Register version (`SYSTEM_VERSION`) | every cut with a new module, new test or changed catalog; file and register header in the same commit |
| Data format | only with migration, pre-backup, old-reader test and fixtures in the same cut |
| `SHELL_VERSION` of the copy | never in the project; it comes with the adoption |

### 6.3 Documentation

- **Maintenance matrix:** one leading source per topic plus the references that must change with it (model: Glide [`docs/DOKUMENTENPFLEGE.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/DOKUMENTENPFLEGE.md)).
- **Every active file carries a status line** `Stand DD.MM.YYYY · <App> <version> · …`; historical evidence keeps its own dates. Glide's `tests/tools/standpruefung.py` checks this and can be adapted.
- **Internal documents in one language, public texts bilingual** (README, user guide, issue and release texts) if the project decides so. The English guide is a controlled translation of the leading feature description and names controls with the labels from the catalogs.
- **QA report only with actual runs:** commit, platform, Python/Tk version, command, result, limits. “Present” is not “tested”, “tested” is not “accepted”.

### 6.4 Git

- Topic branches, pull requests, merge after green CI. Merge branches that build on each other with a merge commit, not a squash.
- **No force pushes, no tags, releases, package-manager submissions or publications without explicit approval from the owner.**
- Check the status before every `git add`; never run `git add -A` blindly. Never stage the project's protected local paths.
- No user paths, no real user data, no raw logs (`*.log`) in versioned files. Glide's `scripts/pflege/pfade_bereinigen.py --pruefen` finds user paths.
- Remove `__pycache__` before test runs and commits.

---

## 7. Checks

### 7.1 Ground rules

- **Never real user data.** Every test sets its own data folder through the project's environment variable (Glide: `GLIDE_DATA_DIR`) before importing the app. Run tools with `python3 -B`.
- **Never run GUI suites in parallel**, and never in the background when they need keyboard focus. On macOS with a locked screen, switching apps delivers no FocusOut; evaluate focus cases only with the screen unlocked.
- **Label results:** platform, Tk version, “synthetic data”. A Linux container does not replace macOS or Windows acceptance.

### 7.2 Stages

| Stage | Content | Model in Glide |
|---|---|---|
| Unit | Tk-free domain modules, catalogs, register | `tests/unit/*` |
| Integration | real Tk windows, one process per suite, counter-checks | `tests/integration/*`, e.g. modal, teardown and window-lifetime contracts |
| Tools | status, link, storage, license and register checks | `tests/tools/*` |
| Base stage | everything fast in one run, also in CI | `tests/tools/ci_grundstufe.py --protokoll <folder>` |
| Full run | every suite in sequence with time limit and stop on failure | `tests/tools/pruefen.py --modus voll --vordergrund --protokoll <folder>` |
| Package | build, isolated start without external Python, checksums | `packaging/paket/baue_und_pruefe_macos.sh`, DMG with `hdiutil verify` |

### 7.3 Shell checks in the project

```bash
cd <project>/src/<app>
python3 -m glide_shell.selftest          # 13/13 checks passed
python3 -O -m glide_shell.selftest       # must report the same
python3 -m glide_shell.demo              # visual check of the usage pattern
```

Also adopt three contract tests following Glide's pattern for your own controller: start (every entry point against an empty, existing, locked and damaged data folder), teardown (no open timers after closing) and modal (grab, focus, nested dialogs).

### 7.4 Completion criterion for a cut

1. Targeted tests of the changed area pass.
2. The base stage passes.
3. Register, versions, plan, QA report, CHANGELOG and the dependent references of the maintenance matrix are updated.
4. A full run before the end of a phase (Glide D51).
5. Open points stated honestly under **D – Remainder**; nothing marked done that was only started.

---

## 8. Reusing the Glide-System in your project

- **Your own register in Glide's format:** tables of modules (`M001 | file | purpose | interface | tests`), features (`F001 …`), building-block packages, tests (`T001 …`) and a version history with date and app version. A tool test checks that the register matches the files (model: `tests/tools/test_glide_system.py`).
- **Building blocks outside the shell** (persistence, backups, import/export, planning, repeat rules …) are listed in Glide's adoption contract: [`src/glide/README.md` §9](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/src/glide/README.md#9-grundlage-für-steps-und-weitere-projekte). They are **not an approved library**: whoever adopts one copies it with its origin (Glide commit, license), adapts names, paths and data model, and covers it with tests of their own.
- **Tools** such as the status check, storage size, path cleaning, static analysis and the full run contain Glide paths and names. Adapt them before the first run in the project and show with a counter-check that they find errors.
- **Do not inherit approvals:** Glide's decisions, signatures, acceptances and release approvals do not apply to a new project automatically.

---

## 9. Changing the shell

If your project needs something the shell does not have:

1. Do not change the copy. Solve it with a module of your own in the project, or propose a new building block in Glide.
2. A new shell module needs approval from the Glide owner (a decision D…) and follows the checklist in the [shell handbook for agents §9](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/GLIDE_SHELL_KI_HANDBUCH.md): neutral part in `glide_shell/<name>.py`, header line `Shell-Paket N:`, English runtime messages, `SHELL_MODULE` in T319, behavior test, raise `SHELL_VERSION`, self-test, file lists for delivery sync and packaging, documentation.
3. Then update the project with the adoption tool and run the self-test.

Compatibility names containing `glide` (`_glide_after_scope`, `GlideCheckbutton` …) are kept on purpose; do not rename them.

---

## 10. Checklists

**Project start**

- [ ] Layout from 3.1 created; `AGENTS.md` with working rules and completion criterion
- [ ] Shell adopted, `SHELL_MANIFEST.json` present, self-test 13/13 (also with `-O`)
- [ ] Start through `AppHost` with `preflight`; imports without side effects
- [ ] Data folder via `runtime_paths` and its own environment variable for tests
- [ ] `de.json`/`en.json` catalogs with a parity test; developer messages in English
- [ ] Register at V1.0, plan, decisions, design rules, QA report, maintenance matrix

**Every feature**

- [ ] Assignment and affected decisions/design rules named
- [ ] Domain logic Tk-free with a unit test; module budget kept
- [ ] Timers through a scope, dialogs through `modal_session`, undo through `CommandHistory`
- [ ] Texts in both catalogs; controls protected; worst-case data checked
- [ ] Register, system version, plan (A/B/C/D), CHANGELOG, QA report updated

**Before the pull request**

- [ ] Targeted tests and base stage pass; GUI suites one after another
- [ ] No user paths, no real data, no `__pycache__`, no protected paths
- [ ] The PR description names the checks, the platform and open limits

**Release** (only with approval)

- [ ] Production round: version switch, delivery sync, checksums
- [ ] Full run, package build, isolated start, disk image verified
- [ ] Tag, release, signing, notarization and submissions only after explicit approval

---

## 11. Pitfalls learned in Glide

- **macOS Aqua** fixes its font set at the first `Tk()`: register private fonts in `before_tk`.
- **A second `Tk()`** in the same process crashes on macOS: do preparatory work in a child process.
- **Cmd+Q** bypasses `WM_DELETE_WINDOW` on macOS: always use `install_close`; quitting runs when idle.
- **The Command modifier** is Num Lock on Windows: bind Cmd shortcuts only for platform `MACOS` (`bind_shortcuts`).
- **Tk 9.1** navigates treeviews through virtual events that Emacs shortcuts also trigger; protect your own Ctrl shortcuts in lists against the class binding.
- **Bytecode** must not land in the source tree (set `sys.pycache_prefix` before the first own import); otherwise start-path checks fail.
- **Fixed version values in tests** break on a version switch: read the version from `VERSION` and compare by release order instead of numbers.
- **Long paths** (OneDrive, Windows without long-path support): keep test copies and temp folders in short local folders.
- **A locked screen** falsifies focus checks: run full runs in the foreground with the screen unlocked.

---

## 12. Further reading

| Topic | Source in Glide |
|---|---|
| Working rules | [`AGENTS.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/AGENTS.md) |
| Shell for agents working on the shell itself | [`docs/GLIDE_SHELL_KI_HANDBUCH.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/GLIDE_SHELL_KI_HANDBUCH.md) |
| Shell boundaries and phases | [`docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md) |
| Architecture | [`docs/02_ARCHITECTURE.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/02_ARCHITECTURE.md) |
| Design | [`docs/DESIGN_RICHTLINIEN.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md) (section *Portabler Designvertrag*) |
| Decisions | [`docs/ARBEITSRICHTUNG.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/ARBEITSRICHTUNG.md) |
| Test plan and QA | [`docs/05_QA_TESTPLAN.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/05_QA_TESTPLAN.md), [`docs/07_QA_BERICHT.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/07_QA_BERICHT.md) |
| Register and adoption contract | [`src/glide/README.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/src/glide/README.md) |
| Document maintenance | [`docs/DOKUMENTENPFLEGE.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/DOKUMENTENPFLEGE.md) |
