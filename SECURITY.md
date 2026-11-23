# Security policy

Status as of 23.11.2026 · Glide 1.0.2 · data format 26

[Read this policy in German](SECURITY.de.md).

Glide handles tasks, notes, pages, pinboards, and attachments locally. Core functionality needs neither an account nor network access. Links and attachments opened by the user are handed to the operating system's default application; their processing is outside Glide. The [technical security boundaries (German)](01_Repository/Glide/SECURITY.md) provide additional detail.

## Supported versions

Security fixes are made for the current source baseline on `main` and then carried into the Python distribution and native packages. The [QA report (German)](01_Repository/Glide/docs/07_QA_BERICHT.md) records the actual package and test status. Earlier development versions are not maintained separately.

## Report a vulnerability

Please report vulnerabilities privately through [Security → Report a vulnerability](https://github.com/n05a-design/glide-to-do/security/advisories/new). Do not disclose security findings in public issues.

Include the affected app and package version, operating system, Python/Tk version if relevant, reproducible steps, and expected versus observed behavior. Use synthetic examples and remove credentials, real user content, personal paths, and private attachments from evidence.

Reports are assessed and reproduced with synthetic data. Confirmed findings are addressed with a tested fix; a Security Advisory may follow when appropriate. No fixed response time is currently promised.

## Scope and trust boundaries

- The application in `01_Repository/Glide/src/glide` and its delivery copy in `07_Python-Versionen`.
- Untrusted inputs: backups, templates, exchange files, Notion archives, CSV, ICS, Markdown, and attachments. Local files can also be manipulated.
- Data handling: source data, backups, settings, lock ownership, and recovery; protection against unnoticed overwrites or data loss.
- Bundled native code, system decoders, packaging, build dependencies, maintenance tools, and GitHub workflows.
- Reportable issues include reachable violations of these boundaries with a substantiated impact on confidentiality, integrity, or availability. Local execution alone does not make a finding irrelevant.

Please also report defects in unmodified Python, Tcl/Tk, or the operating system to their respective maintainers. Issues in Glide's use or packaging of those components remain in scope. This policy does not add other exclusions or accepted risks.

## Protecting the project

GitHub Actions uses limited permissions, checkout without persisted credentials, and immutable action commits. Build dependencies are pinned by version and original SHA-256; pip enforces hash checking. CI checks include tests, delivery alignment, third-party code provenance, user paths, and repository storage limits. Each run documents only the source revision it actually tested.

Keys, certificates, tokens, real user data, raw logs, and local working copies do not belong in the public repository. `.gitignore` helps prevent accidental addition of new files, but already tracked files, `git add -f`, and web uploads still require review. Package checks and signatures are documented separately in the [delivery report (German)](01_Repository/Glide/docs/07_QA_BERICHT.md).
