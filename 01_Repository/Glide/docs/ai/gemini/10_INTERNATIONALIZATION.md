---
project: Glide
document_id: GLIDE-I18N
title: Internationalization
language: en
document_version: 1.0
source_commit: "5631333a1c5a80c11c48226016ab115c434b0a64"
verified_at: "2026-11-19"
status: verified-with-known-gaps
maintainer: project
related_documents: [GLIDE-UX, GLIDE-DATA, GLIDE-ROADMAP]
---

# Internationalization

Stand 19.11.2026 · Glide 1.0.0 · Aufgabenformat 26 · Quellstand 5631333a

## Current mechanism

`src/glide/i18n.py` is a standard-library-only module. It supports `de` and `en`, defaults to German, resolves a user preference or the system locale, loads JSON catalogs, formats placeholders, and falls back to German and then to a supplied default/key. Catalog files are under `src/glide/resources/locales/`. The app stores language preference in its settings and localizes selected app surfaces.

The module catches catalog/locale failures and returns fallback language/text; a missing or malformed translation can therefore appear as fallback UI instead of preventing startup. Tests must check parity and visible outcomes, not only module import.

## Current coverage

**Partially integrated.** Recent work covers the language setting, menus, selected sidebar areas, settings, page/editor actions and statuses, task inspector/calendar fields, selected accessibility probes and action labels. Remaining UI includes additional dialogs, dynamic toasts, status/error messages and other hard-coded strings. D93 establishes DE/EN as the 1.0 target; it does not mean full localization has been achieved.

Tests include catalog key/placeholder parity (T329) and targeted visible behavior (T118), as described in the canonical system/test register. Exact current test status is in the QA report.

## Data and formatting

The persisted language preference is distinct from task data and the active process language. Stored task kinds/field names remain stable across locale changes; UI strings and platform accelerator labels can vary. Tests and fixtures must force the intended language where they assert localized text. Dates and recurrence syntax have domain rules; do not assume locale formatting or translate stored values without a contract.

## Glide-Shell boundary

`i18n.py` is an extracted module within the Glide source tree. Shell-oriented modules `modal_session.py`, `window_lifetime.py`, `custom_controls.py`, and `desktop_adapter.py` also exist in the Glide repository. There is no verified shared language service between separate Glide and Glide-Shell applications, and no separately released `glide_shell` package/host at this snapshot. Package consolidation is documented as post-1.0 work. Do not describe that target as an active integration.

## Safe extension strategy

1. Check both JSON catalogs and existing keys before adding strings.
2. Keep the German and English key sets and placeholders in parity; prefer stable semantic keys.
3. Keep language-specific strings at UI boundaries; do not translate identifiers, enum values, or persisted schema fields.
4. Test active-language changes, fallback behavior, keyboard/accessibility names, long strings, and representative DE/EN UI paths.
5. Update user-facing public docs in both languages when required by project policy; internal authoritative docs remain German unless the artifact is explicitly an English Gemini export.
6. Re-run the applicable CI and platform checks; module-level parity is not full UI acceptance.

## Source references

`src/glide/i18n.py`, `src/glide/resources/locales/de.json`, `src/glide/resources/locales/en.json`, `tests/unit/test_i18n.py` (T329), `tests/integration/test_arbeitsmodi.py` (T118), [`07_QA_BERICHT.md`](../../07_QA_BERICHT.md), and [roadmap](./14_ROADMAP_AND_BACKLOG.md).
