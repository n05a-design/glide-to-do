# Updating an existing shell copy

Status as of 28.11.2026 · Glide 1.0.3 · Glide Shell 0.10.0 (path from 0.6.2) · Glide Bento 0.3.0 · License MPL-2.0 · [Deutsche Fassung](AKTUALISIERUNG.md)

This contract applies to follow-up projects that keep `glide_shell` as a managed copy with `SHELL_MANIFEST.json` (as of E01: STEPS and Chess & Chains with 0.6.2 from Glide commit `793596f1`). It describes what changes, how to update and how to return to the previous state.

## 1. Compatibility

- `SHELL_COMPAT_SINCE` stays **0.6.2**. Between 0.6.2 and 0.10.0 no public function, class or method was removed and no parameter was renamed or reordered. The framework checkpoint checks this mechanically (`interface_changes`: `removed` and `changed` are empty).
- A host that uses only the public names of 0.6.2 runs unchanged after the update. T376 proves this with an artificial 0.6.2 host. It is **not** proven for STEPS or Chess & Chains themselves; their E03 tasks check that with their own regression tests.
- New parameters have defaults (`AppHost(on_callback_error=None)`). Behaviour without these arguments is unchanged.
- Data formats of follow-up projects are not affected; the shell writes no application data.

## 2. What is new

| Version | New | For follow-up projects |
|---|---|---|
| 0.7.0 | `compat`, `conformance`, `showcase` | version check, architecture check, gallery registry |
| 0.8.0 | `spellcheck` | spell-checking contract without an engine |
| 0.9.0 | `ActionHandle`, `DropIndicator`, `symbol_ink_offset` | handles, drop feedback, optical glyph centre |
| 0.9.1 | handle-axis rule (D108) | design rule, no code |
| 0.10.0 | `color_roles`, `settings_registry`, `controls`, `workspaces`; `AppHost.add_shutdown`/`shutdown`/`on_callback_error`; conformance rule `host-api` | theme provider, settings, button/search field/tooltip/toolbar, workspaces, ordered shutdown |

Glide Bento 0.3.0 requires shell ≥ 0.7.0. The tool refuses a Bento copy next to shell 0.6.2, so shell and Bento are updated together.

## 3. Host requirements from 0.10.0

- Colours: a role dictionary with `color_roles.CORE_ROLES`. `color_roles.validate` reports missing roles and contrast below WCAG 2.2 AA. A brand colour comes through `with_accent` or `ThemeProvider(accent=...)`, never through constants inside components.
- Fonts: `custom_controls.set_font_provider`, as before.
- Settings: the host keeps its own storage format. `SettingsRegistry` only describes, validates and groups; unknown keys are kept.
- Workspaces: product views are registered as `Workspace(id, title, factory)`. The shell knows no data model.

## 4. Procedure

1. Secure the follow-up project's working state (Git commit or copy).
2. Check without writing:
   `python3 -B tools/shell_uebernehmen.py --pruefen --mit-bento <project>/src`
   The output lists outdated, missing and locally modified files. "Host-Vertrag" lists every import of a name the new shell does not have.
3. Update with a backup:
   `python3 -B tools/shell_uebernehmen.py --mit-bento --sicherung <folder-outside> <project>/src`
   The tool refuses on local changes to the copy, on a downgrade, on host imports of missing names, on an incompatible shell/Bento combination and on foreign files with the same name. Host product files are never overwritten; if a step fails, the folder is rolled back.
4. Verify: `python -m glide_shell.selftest` (16/16), `python -m glide_bento.selftest` (16/16), `python -m glide_shell.conformance <src>` (conform) and the project's own regression tests.
5. Return if needed: `python3 -B tools/shell_uebernehmen.py --zurueck <backup-folder> <project>/src` restores the backed-up state byte for byte. A modified backup is refused.

## 5. Limits

- Verified on Windows 11 with Tk 9 and artificial data. Native macOS and Linux and the real follow-up projects are open (E03, E06).
- `--commit` reads an older source; the host contract is not checked in that case.
- The shell is pre-1.0. Compatible additions remain possible until stabilisation after E03; breaking changes only with a raised `SHELL_COMPAT_SINCE` and an entry here.
