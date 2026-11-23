---
project: Glide
document_id: GLIDE-PLAYBOOK
title: AI development playbook
language: en
document_version: 1.0
source_commit: "5631333a1c5a80c11c48226016ab115c434b0a64"
verified_at: "2026-11-19"
status: documented-with-known-gaps
maintainer: project
related_documents: [GLIDE-GEMINI-MASTER, GLIDE-DEVELOPMENT, GLIDE-GAPS]
---

# AI development playbook

Stand 23.11.2026 · Glide 1.0.2 · Aufgabenformat 26 · Quellstand 5631333a

## Evidence labels

Use the strongest label justified by evidence, not by confident wording:

- **VERIFIED** — observed in code or an actually run test at a stated commit/environment.
- **DOCUMENTED** — stated in an authoritative project source; implementation may not have been independently run.
- **PLANNED** — explicitly selected/assigned in the authoritative plan but not yet complete.
- **PROPOSED** — suggestion awaiting owner selection.
- **INFERRED** — reasoned interpretation; show the supporting facts and uncertainty.
- **UNKNOWN** — evidence is missing, contradictory, inaccessible, or inconclusive.
- **OBSOLETE** — superseded; preserve its historical date/source rather than applying it as current.

These are not interchangeable. In particular, "workflow started," "test exists," "local Mac passed," and "template exists" do not mean "remote platform passed," "feature fully accepted," or "published."

## Source precedence

1. Current code, format constants, tests, and exact commit for present behavior.
2. `AGENTS.md`, `ARBEITSRICHTUNG.md`, product constraints, data contract, design rules, feature behavior and system register for governing rules.
3. Development plan for selected work and status; QA report for actual outcomes; handoff for current action only.
4. English Gemini documents only as a map and summary. If they conflict with canonical sources, correct this derivative and record the conflict.
5. Dated GitHub runs, issues, and plans only for their exact historic commit/state.

## Safe work procedure

1. Read handoff, repository rules, working direction, plan, document-maintenance matrix, primary behavior contract, and callers before changing code or authoritative docs.
2. Quote the assigned user scope, distinguish authorized choices from proposals, and preserve D01–D99 and the freeze.
3. Set `GLIDE_DATA_DIR` to an isolated short temporary directory before importing Glide; use synthetic data only and `python3 -B`.
4. Keep domain logic Tk-free and unit-tested; reuse existing mutation, save, modal, lifecycle, localization, and UI helpers.
5. Inspect current callers, stable IDs, data formats, side effects, platform bounds, and the product Skill coupling before editing.
6. Make a surgical change; update the leading source, directly affected consequences, changelog, plan, QA, system register/version if applicable, and delivery copy only under its production-round rules.
7. Run narrow tests, then required CI and native platform evidence. Report exact commands, commit, runtime, pass/fail/skip and remaining gates.
8. Never stage secrets, user data, raw logs, protected audit/grafics paths, private machine paths, or unapproved generated archives.

## UI work

For any Tk appearance/layout/interaction change, load the `design-richtlinien` skill and use `DESIGN_RICHTLINIEN.md` as the contract. Check screen size, long German/English strings, focus, keyboard, accessibility, theme, modal ownership, callback cleanup, and geometry. Do not rely on a screenshot substitute or a single-platform result when the issue is native/Tk-specific.

## AI data exchange

Follow `glide-to-do` and the canonical exchange contract. Keep imports reviewable, validate before write, preserve source data and backups, and maintain `abdeckung.json`, helper, references, examples, manifest, and required tests in the same change. The Skill is a user-facing product artifact, not this development playbook.

## Handling unknowns and conflicts

When sources disagree, record each source's date/commit and defer to the assigned authority. Do not silently normalize a contradiction, invent a test outcome, update a historical receipt, or treat a long timeout as proof of the specific call stack. Escalate only an unresolved owner decision; otherwise continue within selected scope.

## Reference

See [`AGENTS.md`](../../../AGENTS.md), [`ARBEITSRICHTUNG.md`](../../ARBEITSRICHTUNG.md), [`DOKUMENTENPFLEGE.md`](../../DOKUMENTENPFLEGE.md), [Gemini Import Guide](./GEMINI_IMPORT_GUIDE.md), and the [source manifest](./SOURCE_MANIFEST.md).
