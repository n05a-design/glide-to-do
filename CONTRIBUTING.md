# Contributing to Glide

Status as of 19.11.2026 · Glide 1.0.2

[Read this guide in German](CONTRIBUTING.de.md).

Want to report a bug, suggest an idea, improve the documentation, or contribute code? This page links to the right starting points and project references.

[Project overview](README.md) · [Roadmap](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) · [Features (German)](01_Repository/Glide/docs/20_FUNKTIONEN.md) · [Application architecture (German)](01_Repository/Glide/docs/02_ARCHITECTURE.md) · [Development process](#development-process) · [Quality report (German)](01_Repository/Glide/docs/07_QA_BERICHT.md)

## Find the right starting point

| If you want to … | Start here |
|---|---|
| see current work and what is planned | [Roadmap and task status](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) |
| understand how a feature works | [Feature guide (German)](01_Repository/Glide/docs/20_FUNKTIONEN.md) |
| learn how the application is structured | [Architecture (German)](01_Repository/Glide/docs/02_ARCHITECTURE.md), [system inventory (German)](01_Repository/Glide/src/glide/README.md), and [Shell target architecture (German)](01_Repository/Glide/docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md) |
| set up a development environment and run Glide | [Requirements and quickstart (German)](01_Repository/Glide/README.md#schnellstart-aus-dem-quellstand) |
| continue existing work | [Handoff and current status (German)](00_Arbeitsvorbereitung/Glide_Uebergabe.md), then [repository rules (German)](01_Repository/Glide/AGENTS.md) |
| run checks or understand results | [Test plan (German)](01_Repository/Glide/docs/05_QA_TESTPLAN.md), [test tools (German)](01_Repository/Glide/tests/README.md), and [QA report (German)](01_Repository/Glide/docs/07_QA_BERICHT.md) |
| improve text, links, or instructions | [Documentation ownership and change matrix (German)](01_Repository/Glide/docs/DOKUMENTENPFLEGE.md#zuständigkeiten-und-änderungsbezüge) and [documentation index (German)](01_Repository/Glide/docs/00_INDEX.md) |

The development plan is the single roadmap. Feature behavior, architecture, and test results are maintained in their linked source documents.

## Report bugs and suggest ideas

Use the [bilingual issue forms](https://github.com/n05a-design/glide-to-do/issues/new/choose), or choose a focused form:

- [Documentation issue](.github/ISSUE_TEMPLATE/dokumentation.yml)
- [Localization issue](.github/ISSUE_TEMPLATE/lokalisierung.yml)
- [Accessibility issue](.github/ISSUE_TEMPLATE/accessibility.yml)

For a bug report, include the Glide version, operating system, reproduction steps, and expected versus observed behavior. Use synthetic content or the [showcase (German)](05_Probelisten_Testdaten/Showcase/README.md) for screenshots and sample files. Code changes should follow the bilingual [pull request template](.github/PULL_REQUEST_TEMPLATE.md).

For a feature idea, describe the situation you are trying to handle before proposing a solution. Check the roadmap and [product boundaries (German)](01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md) first. Larger changes and new dependencies require owner review; suggestions and priorities are tracked in the development plan.

Report security vulnerabilities privately according to the [security policy](SECURITY.md). General help is available in [SUPPORT.md](SUPPORT.md); the project follows the [Code of Conduct](CODE_OF_CONDUCT.md).

## Development process

1. **Clarify the task and scope.** Read the handoff and roadmap, narrow the affected area, and account for existing decisions in the [project direction (German)](01_Repository/Glide/docs/ARBEITSRICHTUNG.md). Product decisions belong to the owner.
2. **Understand and check the baseline.** Read the [repository rules (German)](01_Repository/Glide/AGENTS.md), relevant feature contracts, and architecture. Inspect callers as well as the implementation, then run a suitable existing check. UI work must follow the [design guidelines (German)](01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md).
3. **Make a focused change.** Preserve existing behavior, user data, and data formats. Keep domain logic and UI concerns separated as required by the repository rules. Format changes require migration, backup, and appropriate tests.
4. **Verify and document the result.** Run relevant checks, record results and limitations, and update affected source documents using the central [documentation change matrix (German)](01_Repository/Glide/docs/DOKUMENTENPFLEGE.md#zuständigkeiten-und-änderungsbezüge). It describes the relationships between the roadmap, system inventory, and Shell target. The [implementation process (German)](01_Repository/Glide/docs/ARBEITSRICHTUNG.md#arbeitsablauf-einer-implementierung) defines validation phases; documentation-only and tooling work follow the documented [follow-up rules (German)](01_Repository/Glide/docs/ARBEITSRICHTUNG.md#nachläufe-ohne-neue-app-version).
5. **Submit the change for review.** A pull request should explain the reason, actual changes, checks run, open items, and risks. Merging requires explicit approval; packaging and release have separate gates.

## Develop and test locally

The source code is under `01_Repository/Glide/src/glide`. The [technical entry point (German)](01_Repository/Glide/README.md) lists prerequisites, launch commands, and the CI baseline. The [module inventory (German)](01_Repository/Glide/src/glide/README.md) helps locate relevant code and tests.

Tests must use a dedicated temporary data directory through `GLIDE_DATA_DIR`. Never use real user data. The [test plan (German)](01_Repository/Glide/docs/05_QA_TESTPLAN.md) and [test-tool overview (German)](01_Repository/Glide/tests/README.md) describe safe test environments, modes, and commands.

## Quality, packaging, and release

The [QA report (German)](01_Repository/Glide/docs/07_QA_BERICHT.md) ties results to their source revision and platform. Focused tests, full suites, native packaging, and human acceptance are reported separately. Failed or skipped checks and open manual cases remain visible.

A green CI run is not release approval. The [manual checklist (German)](00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md) describes owner acceptance; the [release guide (German)](01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md) covers packaging and publication steps.

## License

The project code is licensed under the [Mozilla Public License 2.0](LICENSE). See the [license scope and third-party notices (German)](01_Repository/Glide/LICENSE.md) as well.
