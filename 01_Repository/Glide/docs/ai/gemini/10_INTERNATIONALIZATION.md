---
project: Glide
document_id: GLIDE-I18N
title: Internationalization
language: en
document_version: 1.0
source_commit: "4ce3697a11321686119313ae5a8e8c891413c85f"
verified_at: "2026-11-22"
status: verified-with-known-gaps
maintainer: project
related_documents: [GLIDE-UX, GLIDE-DATA, GLIDE-ROADMAP]
---

# Internationalization

Stand 24.11.2026 · Glide 1.0.3 · Aufgabenformat 27 · Quellstand 4ce3697a

## Current mechanism

`src/glide/i18n.py` is a standard-library-only module. It supports `de` and `en`, defaults to German, resolves a user preference or the system locale, loads JSON catalogs, formats placeholders, and falls back to German and then to a supplied default/key. Catalog files are under `src/glide/resources/locales/`. The app stores language preference in its settings and localizes selected app surfaces.

The module catches catalog/locale failures and returns fallback language/text; a missing or malformed translation can therefore appear as fallback UI instead of preventing startup. Tests must check parity and visible outcomes, not only module import.

## Current coverage

**Completed for 1.0.** The whole interface follows the chosen language (V1.70–V1.79): menus, views, dialogs, toasts, status and error messages, undo texts, the built-in manual, exchange format, system labels, templates, home page, AI output and release notes. Since V1.81 quick capture understands English and German words. Only names that users gave their own content stay as written. T335 (`test_lokalisierung_d93`) and `test_i18n.py` guard the catalogs.

Tests include catalog key/placeholder parity (T329) and targeted visible behavior (T118), as described in the canonical system/test register. Exact current test status is in the QA report.

## Data and formatting

The persisted language preference is distinct from task data and the active process language. Stored task kinds/field names remain stable across locale changes; UI strings and platform accelerator labels can vary. Tests and fixtures must force the intended language where they assert localized text. Dates and recurrence syntax have domain rules; do not assume locale formatting or translate stored values without a contract.

## Glide-Shell boundary

`i18n.py` is a module within the Glide source tree. The shell (`glide_shell` 0.6.2) loads no catalogs: the host passes already translated labels in (locale contract in the shell concept). There is no shared language service between separate applications.

## Safe extension strategy

1. Check both JSON catalogs and existing keys before adding strings.
2. Keep the German and English key sets and placeholders in parity; prefer stable semantic keys.
3. Keep language-specific strings at UI boundaries; do not translate identifiers, enum values, or persisted schema fields.
4. Test active-language changes, fallback behavior, keyboard/accessibility names, long strings, and representative DE/EN UI paths.
5. Update user-facing public docs in both languages when required by project policy; internal authoritative docs remain German unless the artifact is explicitly an English Gemini export.
6. Re-run the applicable CI and platform checks; module-level parity is not full UI acceptance.

## Source references

`src/glide/i18n.py`, `src/glide/resources/locales/de.json`, `src/glide/resources/locales/en.json`, `tests/unit/test_i18n.py` (T329), `tests/integration/test_arbeitsmodi.py` (T118), [`07_QA_BERICHT.md`](../../07_QA_BERICHT.md), and [roadmap](./14_ROADMAP_AND_BACKLOG.md).
