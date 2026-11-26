<p align="right"><a href="README.de.md">Deutsch</a></p>

<p align="center">
  <img src="01_Repository/Glide/assets/icons/glide_512.png" alt="Glide app icon" width="88">
</p>

<h1 align="center">Glide</h1>

<p align="center">
  <strong>Plan tasks. Connect ideas.</strong><br>
  Glide is an open-source desktop workspace that brings tasks, daily planning, notes, and visual project organization together. Work locally, connect your ideas, and stay in control of your data.
</p>

<p align="center">
  <img alt="Windows, macOS, and Linux" src="https://img.shields.io/badge/Windows%20%C2%B7%20macOS%20%C2%B7%20Linux-Desktop-555">
  <img alt="Python 3.14" src="https://img.shields.io/badge/Python-3.14-blue">
  <a href="https://github.com/n05a-design/glide-to-do/releases/tag/v1.0.2"><img alt="Prerelease v1.0.2" src="https://img.shields.io/badge/Prerelease-v1.0.2-9E4AC8"></a>
  <a href="LICENSE"><img alt="MPL-2.0 license" src="https://img.shields.io/badge/License-MPL--2.0-2E7D32"></a>
</p>

<p align="center">
  <a href="#download"><strong>Download Glide 1.0.2</strong></a> ·
  <a href="#quickstart-and-system-requirements">Run from source</a> ·
  <a href="05_Probelisten_Testdaten/Showcase/README.md">Showcase</a> ·
  <a href="#what-glide-does">Features</a> ·
  <a href="#a-look-at-glide">Screenshots</a> ·
  <a href="CONTRIBUTING.md">Contribute</a>
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="01_Repository/Glide/assets/marketing/github-social-preview.png">
  <img alt="Glide pinboard with pages, tasks and labelled connections" src="01_Repository/Glide/assets/marketing/glide-1.0-pinnwand-en.png" width="100%">
</picture>

<p align="center"><sub>Glide is available in English and German. Screenshots show Glide 1.0.2 on macOS with the showcase “City Light”, a fictional photo journey; the photos are by Tim von Trostorff. They are not test or package evidence.</sub></p>

## Why Glide?

Glide brings tasks and project notes into one local workspace. The same task stays connected as you move between lists, pages, calendars, and pinboards.

- **Plan your day:** See work dates, due dates, effort, and available time separately.
- **Work with your own material:** Connect tasks, pages, notes, and pinboards.
- **Stay in control:** Keep your data in a folder you choose, with backups and readable exports to support a move.

## A look at Glide

All images show the showcase “City Light”: fictional data, real photos by the author.

<table>
  <tr>
    <td><strong>Home</strong><br><img alt="Glide home with day plan and project tiles" src="01_Repository/Glide/assets/marketing/glide-1.0-startseite-en.png" width="100%"></td>
    <td><strong>Calendar</strong><br><img alt="Glide week calendar with planned tasks" src="01_Repository/Glide/assets/marketing/glide-1.0-kalender-en.png" width="100%"></td>
  </tr>
  <tr>
    <td><strong>Today</strong><br><img alt="Day plan with tasks and time blocks in dark theme" src="01_Repository/Glide/assets/marketing/glide-1.0-heute-en.png" width="100%"></td>
    <td><strong>Pages</strong><br><img alt="Project page with formatted text, images, and tasks" src="01_Repository/Glide/assets/marketing/glide-1.0-seite-en.png" width="100%"></td>
  </tr>
  <tr>
    <td><strong>Task list</strong><br><img alt="Task list with labels and repeating tasks" src="01_Repository/Glide/assets/marketing/glide-1.0-liste-en.png" width="100%"></td>
    <td><strong>Pixel workshop</strong><br><img alt="Pixel workshop with an animated travel stamp" src="01_Repository/Glide/assets/marketing/glide-1.0-pixel-en.png" width="100%"></td>
  </tr>
</table>

[Open the complete showcase](05_Probelisten_Testdaten/Showcase/README.md) · [More screenshots and features](01_Repository/Glide/docs/20_FUNKTIONEN.md)

## What Glide does

Glide's capabilities are structured across six cohesive product pillars:

1. **Task Management:** Hierarchical lists, folders, subtasks, checklists, labels, custom colors, due dates, recurrence, dependencies, and saved views.
2. **Day Planning:** Separate work dates, due dates, effort estimates, calendar events, routines, focus sessions, and available time; compare planning suggestions before applying them.
3. **Personal Knowledge:** Formatted pages, blocks, notes, journals, local file attachments, backlinks, and explicit usage locations.
4. **Visual Workspace:** Lists, tables, boards, pinboards, weekly and monthly calendars, and a configurable home dashboard. *(Note: The responsive Glide Bento Box System 0.1.0 with dynamic 1–3-column grid reflow is currently in active development on `main` following 1.0.2).*
5. **Creative Tools:** Integrated pixel workshop with animated stamps, color palettes, and custom artwork generation for projects and covers.
6. **Open Data & AI Exchange:** Local-first file storage, import/export for Markdown, CSV, iCalendar, JSON Canvas, and `.glideexchange` files; AI integration via the open [agent skill](01_Repository/Glide/skills/glide-to-do/README.md) without cloud lock-in.

## What Glide is not

- **Not a phone or tablet app.** Glide is made for desktop work. A mobile task app is a better fit for mobile-first reminders and planning on the go.
- **Not a cloud team service.** There is no Glide account or real-time collaboration. A shared cloud folder does not merge simultaneous changes from multiple devices; choose a team service built for shared projects when that is your main need.
- **Not an AI service.** Glide does not send content to an AI provider. You can exchange files manually with a tool of your choice; the [`glide-to-do` agent skill](01_Repository/Glide/skills/glide-to-do/README.md) can prepare Glide import documents.

## Download

Glide 1.0.2 is available as an official **public prerelease** on [GitHub Releases (v1.0.2)](https://github.com/n05a-design/glide-to-do/releases/tag/v1.0.2). Standalone packages bundle Python, Tk, typography, and required libraries; no separate runtime installation is needed.

> **Note on 1.0.3 (as of 26.11.2026):** The [v1.0.3](https://github.com/n05a-design/glide-to-do/releases/tag/v1.0.3) release page exists but does not carry download files yet. Until the verified packages are attached, 1.0.2 remains the downloadable version.

| Platform | Download Asset | Size | Notes |
|---|---|---|---|
| **Windows 10/11 (x64)** | [Glide-1.0.2-windows-x64-setup.exe](https://github.com/n05a-design/glide-to-do/releases/download/v1.0.2/Glide-1.0.2-windows-x64-setup.exe) | ~17.0 MB | Setup wizard (installs unprivileged to `%LOCALAPPDATA%\Programs\Glide`) |
| **Windows 10/11 (x64)** | [Glide-1.0.2-windows-x64.zip](https://github.com/n05a-design/glide-to-do/releases/download/v1.0.2/Glide-1.0.2-windows-x64.zip) | ~19.5 MB | Portable zip (unzip and run `Glide.exe` directly) |
| **macOS (Apple Silicon, arm64)** | [Glide-1.0.2-macos-arm64.dmg](https://github.com/n05a-design/glide-to-do/releases/download/v1.0.2/Glide-1.0.2-macos-arm64.dmg) | ~20.7 MB | Disk image (drag `Glide.app` into `/Applications`) |
| **macOS (Apple Silicon, arm64)** | [Glide-1.0.2-macos-arm64.tar.gz](https://github.com/n05a-design/glide-to-do/releases/download/v1.0.2/Glide-1.0.2-macos-arm64.tar.gz) | ~18.2 MB | Portable archive |
| **Agent Skill** | [glide-to-do-skill-v1.0.2.zip](https://github.com/n05a-design/glide-to-do/releases/download/v1.0.2/glide-to-do-skill-v1.0.2.zip) | ~39 KB | Document exchange skill for AI developer agents |
| **Linux (x64 / arm64)** | [Run from source](#quickstart-and-system-requirements) | — | Python 3.14 + Tk 9 recommended; no standalone binary yet |

> [!NOTE]
> **Prerelease & Signature Status:** Commercial EV and Apple Developer ID certificates are deferred until software catalog expansion (decision I3 / D43). On macOS, Gatekeeper may require opening **System Settings › Privacy & Security › Open Anyway** or running `xattr -d com.apple.quarantine /Applications/Glide.app`. On Windows, click **More info › Run anyway** on the SmartScreen prompt.
> All packages can be verified using official cryptographic SHA-256 checksums; see the [Installation Guide](01_Repository/Glide/docs/user-guide/02-installation.md).

## Quickstart and system requirements

Python 3.14 with Tk 9 is recommended for running from source; Tk 8.6 starts with known limitations. No additional runtime packages are required. From the repository root:

```text
cd 01_Repository/Glide
python3 src/glide/app.pyw
```

On Windows, use `python src\glide\app.pyw` for the second command. The main window requires at least **860 × 700 px**; compact mode can use **480 × 560 px**. See the [technical quickstart (German)](01_Repository/Glide/README.md#schnellstart-aus-dem-quellstand) for other start options and prerequisites. Try the [showcase (German)](05_Probelisten_Testdaten/Showcase/README.md) with synthetic data.

The [English user guide](01_Repository/Glide/docs/user-guide/README.md) explains the features of Glide 1.0.2, from getting started to troubleshooting. It is a controlled translation of the authoritative [German function reference](01_Repository/Glide/docs/20_FUNKTIONEN.md), which also covers every limit in detail.

## Your data

Glide stores content and attachments in a data folder outside the program directory. You choose where it lives. Automatic backups, a trash folder, and undo help protect your work; Markdown and JSON Canvas exports make it easier to take content elsewhere. Glide does not upload your data to its own cloud service.

| Area | Storage and purpose |
|---|---|
| Your content and settings | In the local data folder you choose; see [data and migration (German)](01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md#ablage) for details and platform paths. |
| Attachments and backups | Managed with the data folder; a shared cloud folder does not merge simultaneous changes from multiple devices. |
| Sample data | The [showcase (German)](05_Probelisten_Testdaten/Showcase/README.md) uses synthetic content and its own data folder. |

## Project structure

| Path | Contents |
|---|---|
| [`01_Repository/Glide/`](01_Repository/Glide/README.md) | Application, Bento system (`glide_bento`), framework shell (`glide_shell`), tests, technical documentation, and packaging |
| [`07_Python-Versionen/`](07_Python-Versionen/) | Separate Python delivery; see the [QA report (German)](01_Repository/Glide/docs/07_QA_BERICHT.md) for validation and source alignment |
| [`05_Probelisten_Testdaten/Showcase/`](05_Probelisten_Testdaten/Showcase/README.md) | Synthetic showcase dataset |
| [`00_Arbeitsvorbereitung/`](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) | Development plan and handover |
| [`20_Grafik_Master/`](20_Grafik_Master/README.md) | Source files for project artwork |

## Frequently asked questions

<details>
<summary><strong>Can I use Glide on two computers?</strong></summary>

You can keep the data folder in a cloud storage service of your choice. Glide does not merge simultaneous changes from multiple devices.
</details>

<details>
<summary><strong>Does Glide connect to an AI provider?</strong></summary>

No. File exchange stays under your control; Glide does not automatically send anything to an AI service.
</details>

<details>
<summary><strong>Has Glide been accessibility-tested?</strong></summary>

Glide offers keyboard access, adjustable text sizes, and contrast themes. A complete native keyboard and screen-reader acceptance test remains open; the [QA report](01_Repository/Glide/docs/07_QA_BERICHT.md) lists what has been tested.
</details>

## Feedback and contributions

Use the [bilingual issue forms for bugs and ideas](https://github.com/n05a-design/glide-to-do/issues/new/choose). Target a specific area:
[Documentation](.github/ISSUE_TEMPLATE/dokumentation.yml) ·
[Localization](.github/ISSUE_TEMPLATE/lokalisierung.yml) ·
[Accessibility](.github/ISSUE_TEMPLATE/accessibility.yml).
Please use synthetic example data only. Report security vulnerabilities confidentially through the [security policy](SECURITY.md). Find help in [SUPPORT.md](SUPPORT.md) and community rules in [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Development and quality

Status as of 24.11.2026 · Glide 1.0.3

<a href="https://github.com/n05a-design/glide-to-do/actions/workflows/python-app.yml"><img alt="Automated checks on main" src="https://github.com/n05a-design/glide-to-do/actions/workflows/python-app.yml/badge.svg?branch=main"></a>

Glide 1.0.2 was officially published as a public prerelease on 23.11.2026 (Tag `v1.0.2`, Commit `7dcd8dc0`). Development continues on `main` towards post-1.0 milestones (Glide-System V1.87, Glide Bento 0.1.0). The badge above tracks checks on `main`, not this README's branch or another pull request. The [quality and testing report](01_Repository/Glide/docs/07_QA_BERICHT.md) ties results to specific commits and distinguishes CI, available development builds, and outstanding human acceptance. See the [contributing guide](CONTRIBUTING.md) and [roadmap](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) for the development process and open work.

## License

The project code is licensed under the [Mozilla Public License 2.0](LICENSE). Third-party components, fonts, and other resources may have separate license terms.
