---
project: Glide
document_id: GLIDE-UX
title: UX, UI and design system
language: en
document_version: 1.0
source_commit: "5631333a1c5a80c11c48226016ab115c434b0a64"
verified_at: "2026-11-19"
status: documented-with-known-gaps
maintainer: project
related_documents: [GLIDE-I18N, GLIDE-WORKFLOWS, GLIDE-PLAYBOOK]
---

# UX, UI and design system

Stand 19.11.2026 · Glide 1.0.0 · Aufgabenformat 26 · Quellstand 5631333a

## Authority

[`docs/DESIGN_RICHTLINIEN.md`](../../DESIGN_RICHTLINIEN.md) is the app-wide design contract. Product principles are in [`01_PRODUCT_CONSTRAINTS.md`](../../01_PRODUCT_CONSTRAINTS.md); platform/layout implementation is in [`02_ARCHITECTURE.md`](../../02_ARCHITECTURE.md). This summary is not a second design authority.

## Hierarchy and layout

- Favor content over controls; the owner-defined content/control budget is at most 15% controls at 1280×800.
- Keep the default surface restrained, with one primary path per intent.
- Use a stable hierarchy appropriate to the view. Task title, due/planned context, board relationships, and document text do not have one global order.
- Keep edges, baselines, spacing, and icon centers aligned; use shared tokens/helpers instead of isolated pixel patches.
- Protect visible controls from clipping/overlap at minimum window size, large type, long German text, and view changes.
- Preserve the fixed workspace and page structure; do not introduce new surfaces or navigation without an owner decision.

## Color, type, icons

The owner-defined button roles are semantic: red for delete, green for confirm, selected theme color for add/new, yellow for notices, otherwise neutral. Fonts are selected by design profile; resource fonts and license provenance are checked in packaging. Icons use the central `ICONS`/`symbol_policy` contract, with documented exceptions for the logo and filled triangle markers. Do not invent Unicode glyphs or import a web/CSS icon pattern into Tk.

## Interaction, motion, and accessibility

Keyboard and mouse paths should follow platform conventions. Modal dialogs use `run_modal`; focus return, callback cleanup, and stable identity matter. Hover, active, selected, disabled, and focus states remain legible. Accessibility labels and reader behavior must follow current platform evidence, not assumed equivalence from translation or widget construction.

Animations and time-based callbacks must be interruptible and owned by the correct window lifetime. Avoid nested `update()`/`update_idletasks()` in self-triggering callbacks.

## Existing implementation

Core UI remains in `app.pyw` plus reusable Tk-free policies and control modules (`ui_design.py`, `custom_controls.py`, `modal_session.py`, `window_lifetime.py`, accessibility and symbol modules). Existing palette, brand, fonts, and layout data are listed in [`src/glide/README.md`](../../../src/glide/README.md).

## Evidence and gaps

Automated tests validate selected geometry, roles, controls, focus contracts, and design permutations. Current PR #152 full Linux/Windows runs timed out in `test_ui39.py`, so later native UI/working-mode suites were not reached. A focused UI/working-mode workflow is a distinct check; human visual, DPI, multi-monitor, and full native Mac acceptance remain separate gates. See [testing](./12_TESTING_AND_QUALITY.md).
