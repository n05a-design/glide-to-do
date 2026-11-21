# Glide Shell – guide for follow-up projects

Status as of 21.11.2026 · Glide 1.0.0 · Glide Shell 0.4.0

<p align="right"><a href="README.de.md">Deutsch</a></p>

The Glide Shell is the reusable Tk foundation from [Glide](../../../README.md): dialogs, timer ownership, transitions, controls, menu bar, window geometry, system appearance and a redo stack. It knows nothing about Glide content. Your application supplies texts, colours, fonts and action IDs.

This guide is a **controlled translation** of [`README.de.md`](README.de.md). The German text applies if the two ever differ. Limits and decisions are set in the [shell concept §7](../../../docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md#7-paket-glide_shell-und-übernahme-in-folgeprojekte-d95-20112026) (German).

## Requirements

- Python 3 with `tkinter`; tested with Python 3.14.5 and Tk 9.1.0 on macOS, Linux and Windows.
- No other dependency. Every file is licensed under `MPL-2.0`.

## Adopting the shell

From a Glide checkout, with your project's source folder as the target:

```bash
python3 -B 01_Repository/Glide/scripts/pflege/shell_uebernehmen.py <your-project>/src
```

The tool copies `glide_shell/` including this guide and writes `glide_shell/SHELL_MANIFEST.json` (package version, source commit, SHA-256 per file).

- `--pruefen` (check) reports each file as `aktuell` (current), `veraltet` (outdated) or `verändert` (changed) and writes nothing.
- If you changed files in your copy, an update stops; only `--ersetzen` (replace) overwrites them.
- Your own files in the folder stay where they are.

## Checking it on the target machine

```bash
cd <your-project>/src
python3 -m glide_shell.selftest
```

The self-test briefly opens a hidden Tk window and checks every building block with real Tk. Each line starts with `ok` or `FAIL`. Exit code 0 means everything passed; 2 means Tk could not open a window (for example without a display).

## Seeing an example

```bash
python3 -m glide_shell.demo
```

The demo host is a small app built only from shell building blocks: menu bar, a clock in its own timer scope with a short transition, a checkbox, a modal dialog, a counter with undo and redo, a window position kept on screen and light/dark following the system. Its source [`demo.py`](demo.py) shows the usage pattern.

## Building blocks

Import the building blocks one by one, for example `from glide_shell import modal_session, window_lifetime`. The package loads nothing on import.

| Module | Purpose | Main names |
|---|---|---|
| `modal_session` | Create dialogs, wait modally, return focus | `create_dialog`, `run_modal`, `wait_modal`, `modal_over` |
| `window_lifetime` | Timers belong to a widget and end with it | `scope_for`, `AfterScope` |
| `motion` | Short, interruptible transitions (at most 150 ms) | `Transitions`, `progress` |
| `custom_controls` | Theme-aware canvas controls | `GlideCheckbutton`, `GlideRadiobutton`, `GlideListbox`, `GlideScale`, `ThemedAutoScrollbar` |
| `desktop_adapter` | Menu bar, keyboard shortcuts, platform, clipboard | `build_menu_tree`, `format_accelerator`, `platform_name`, `launch_path` |
| `window_geometry` | Geometry strings, keep windows on the work area | `parse`, `format_geometry`, `clamp`, `keep_visible` |
| `system_appearance` | Interpret the system's light/dark mode | `tk_is_dark`, `windows_is_dark`, `linux_is_dark`, `resolve` |
| `redo_history` | Redo stack next to your undo stack | `RedoHistory` |

A pattern from the demo host: schedule a window's timers and transitions through the same scope so that nothing keeps running after it closes.

```python
from glide_shell import motion, window_lifetime

scope = window_lifetime.scope_for(root)
transitions = motion.Transitions(scope.after, scope.cancel)
transitions.start("clock", lambda value: label.configure(fg=accent if value < 1 else text))
```

## Limits

- No separate repository and no separate release. Changes are made in Glide; you take over new versions with the tool above.
- Some names carry `glide` for compatibility (`_glide_after_scope`, `GlideCheckbutton` …).
- The shell's runtime messages for developers are in English.
