# Installation – Glide user guide

Status as of 24.11.2026 · Glide 1.0.2 · Task format 26

**Deutsch:** [Funktionen – Eigenständiger Start](../20_FUNKTIONEN.md#eigenständiger-start-3450), [§13 Bekannte Grenzen](../20_FUNKTIONEN.md#13-bekannte-grenzen), [technischer Schnellstart](../../README.md#schnellstart-aus-dem-quellstand) · [Guide contents](README.md) · Previous: [Getting started](01-getting-started.md) · Next: [Tasks and lists](03-tasks-and-lists.md)

> Controlled translation of the German function reference. If the texts differ, the German text applies.

## Public Prerelease downloads

Glide 1.0.2 is available as a **public prerelease** on [GitHub Releases (v1.0.2)](https://github.com/n05a-design/glide-to-do/releases/tag/v1.0.2). Standalone packages bundle Python, Tk, typography, and required dependencies. No separate Python installation is required for standalone binaries.

| Platform | Download asset | Size | Description & Type |
|---|---|---|---|
| **Windows 10/11 (x64)** | [Glide-1.0.2-windows-x64-setup.exe](https://github.com/n05a-design/glide-to-do/releases/download/v1.0.2/Glide-1.0.2-windows-x64-setup.exe) | ~17.0 MB | Setup wizard: installs to `%LOCALAPPDATA%\Programs\Glide`, adds Start menu shortcut |
| **Windows 10/11 (x64)** | [Glide-1.0.2-windows-x64.zip](https://github.com/n05a-design/glide-to-do/releases/download/v1.0.2/Glide-1.0.2-windows-x64.zip) | ~19.5 MB | Portable archive: unzip and run `Glide.exe` directly |
| **macOS (Apple Silicon, arm64)** | [Glide-1.0.2-macos-arm64.dmg](https://github.com/n05a-design/glide-to-do/releases/download/v1.0.2/Glide-1.0.2-macos-arm64.dmg) | ~20.7 MB | Disk image: drag `Glide.app` into `/Applications` |
| **macOS (Apple Silicon, arm64)** | [Glide-1.0.2-macos-arm64.tar.gz](https://github.com/n05a-design/glide-to-do/releases/download/v1.0.2/Glide-1.0.2-macos-arm64.tar.gz) | ~18.2 MB | Tarball archive: unpack and run |
| **Agent Skill** | [glide-to-do-skill-v1.0.2.zip](https://github.com/n05a-design/glide-to-do/releases/download/v1.0.2/glide-to-do-skill-v1.0.2.zip) | ~39 KB | Document exchange skill for AI developer agents |
| **Linux (x64 / arm64)** | [Source repository](https://github.com/n05a-design/glide-to-do) | — | Run from source (Python 3.14 + Tk 9 recommended) |

### macOS Gatekeeper notes

Standalone macOS application bundles are ad-hoc signed but not yet notarized with an Apple Developer ID certificate (decision I3 / D43; commercial certificates are deferred until software catalog expansion). On first launch, macOS Gatekeeper may display a security alert.

1. **Recommended System Settings path (Standard macOS flow):**
   - Attempt to open `Glide.app`. When the warning appears, click **Cancel**.
   - Open **System Settings › Privacy & Security** (*Systemeinstellungen › Datenschutz & Sicherheit*).
   - Scroll down to the **Security** section where a notification states: *"Glide.app was blocked from use because it is not from an identified developer."*
   - Click **Open Anyway** (*Dennoch öffnen*) and confirm with your password or Touch ID.
2. **Targeted Terminal command (Advanced users):**
   - If preferred, you can explicitly remove only the quarantine flag from the application bundle after moving it to `/Applications`:
     ```bash
     xattr -d com.apple.quarantine /Applications/Glide.app
     ```
   - *Note:* Do not run broad recursive commands like `xattr -cr`, which strip all extended attributes; `xattr -d com.apple.quarantine` targets solely the downloaded quarantine attribute.

### Windows SmartScreen notes

The Windows installer is self-contained and completely unprivileged. Because commercial EV code signing certificates are deferred (decision I3 / D43), Windows Defender SmartScreen may display an "Unknown publisher" (*Der Computer wurde durch Windows geschützt*) prompt:
1. In the SmartScreen dialog, click **More info** (*Weitere Informationen*).
2. Verify the publisher is listed as unknown and the file name matches `Glide-1.0.2-windows-x64-setup.exe`.
3. Click **Run anyway** (*Trotzdem ausführen*).

### Checksum verification (SHA-256)

You can verify the cryptographic integrity and authenticity of your downloaded files using the official SHA-256 digests:

```text
1aeb2247b60384dca14b19fd93147a5d5819b4bc4134948adea33ff88e43b7cc  Glide-1.0.2-macos-arm64.dmg
6240b163480507bfcf0b7ec2adb2c7fde4c5bab52026f9738c257fe53f518b71  Glide-1.0.2-macos-arm64.tar.gz
567e9549b1adf396d262d07d7475e7c47ef9fc561c38e4990d0ab5a31c3fee6e  Glide-1.0.2-windows-x64-setup.exe
e82b045ffdbd8caf1c00ff861195be580ed9b987841866424e0c5bbf74ba4799  Glide-1.0.2-windows-x64.zip
c1b35c21084c3848c7aae401f93720bcd6330728a74c7ea2caa51d80bc9c9ae6  glide-to-do-skill-v1.0.2.zip
```

*Note:* Inside both Windows packages, the compiled executable `Glide.exe` carries SHA-256 `77d720d5208ddcb41e36ef8e25a40306855bd54d66f1e6dd818e04ca567606fd`.

#### Executable verification commands

**Windows (PowerShell):**
```powershell
Get-FileHash -LiteralPath ".\Glide-1.0.2-windows-x64-setup.exe" -Algorithm SHA256
```
Compare the resulting `Hash` string with the table above.

**macOS (Terminal):**
```bash
shasum -a 256 "Glide-1.0.2-macos-arm64.dmg"
```

**Linux (Terminal):**
```bash
sha256sum "Glide-1.0.2-macos-arm64.tar.gz"
```

If the output digest matches the table above, the package is unaltered and complete. If any hash differs, do not execute the file; discard it and download freshly from the official [GitHub Release v1.0.2](https://github.com/n05a-design/glide-to-do/releases/tag/v1.0.2).

## Detailed installation paths

### 1. Windows Setup Wizard (`Glide-1.0.2-windows-x64-setup.exe`)
- **Architecture:** 64-bit Windows (x64 / AMD64 / Intel 64). Windows 10 (version 1809+) or Windows 11.
- **Prerequisites:** None. Bundles Python 3.14, Tk, typography, and libraries. No administrator privileges required.
- **Installation:** Run the setup executable. By default, it installs into `%LOCALAPPDATA%\Programs\Glide` (per-user, non-admin). It adds an entry to the Windows Start menu and creates an uninstaller.
- **First Launch:** Launch from Start menu or desktop shortcut. Handle the SmartScreen prompt as described above.
- **Updating:** Download the new setup version and run it. It cleanly replaces the program files without affecting your database.
- **Uninstallation:** Use **Windows Settings › Apps › Installed apps** and choose **Uninstall**. All program binaries are removed; your user workspace in `%APPDATA%\Glide` remains untouched.
- **Limitations:** 32-bit Windows and Windows on ARM (native arm64) are not supported by the x64 binary.

### 2. Windows Portable Archive (`Glide-1.0.2-windows-x64.zip`)
- **Architecture:** 64-bit Windows (x64).
- **Prerequisites:** None.
- **Installation:** Unzip the archive to any desired location (e.g. `C:\Tools\Glide` or an external drive).
- **First Launch:** Double-click `Glide.exe`.
- **Updating:** Overwrite the application directory with the files from the newer `.zip` archive.
- **Uninstallation:** Delete the extracted directory.
- **Limitations:** Does not register Start menu entries or file type associations automatically.

### 3. macOS Disk Image (`Glide-1.0.2-macos-arm64.dmg`)
- **Architecture:** Apple Silicon (arm64, M1/M2/M3/M4). macOS 13 (Ventura), macOS 14 (Sonoma), or macOS 15 (Sequoia).
- **Prerequisites:** Apple Silicon Mac.
- **Installation:** Double-click `Glide-1.0.2-macos-arm64.dmg` to mount the disk image. Drag `Glide.app` into `/Applications`.
- **First Launch:** Open `/Applications/Glide.app`. On the Gatekeeper prompt, follow the System Settings flow or run `xattr -d com.apple.quarantine /Applications/Glide.app`.
- **Updating:** Mount the new `.dmg`, drag `Glide.app` into `/Applications`, and select **Replace**.
- **Uninstallation:** Drag `/Applications/Glide.app` to the Trash. User data in `~/Library/Application Support/Glide` is preserved.
- **Limitations:** Intel Macs (x86_64) require running from source with Python.

### 4. macOS Portable Archive (`Glide-1.0.2-macos-arm64.tar.gz`)
- **Architecture:** Apple Silicon (arm64).
- **Installation:** Extract the archive using `tar -xzf Glide-1.0.2-macos-arm64.tar.gz`.
- **First Launch:** Run `open Glide.app` or `./Glide.app/Contents/MacOS/Glide`. Gatekeeper notes apply as above.
- **Uninstallation:** Delete the extracted bundle.

### 5. AI Agent Skill (`glide-to-do-skill-v1.0.2.zip`)
- **Purpose:** Document-based AI agent exchange skill conforming to the open Agent Skills standard.
- **Compatible Agents:** Google Antigravity, OpenAI Codex / ChatGPT, Claude Code, Gemini CLI.
- **Installation:** Unzip the skill package into your agent skill directory (e.g. `.agents/skills/glide-to-do/` or `.claude/skills/glide-to-do/`).
- **Capabilities:** Enables agents to create structured project plans, task collections, notes, and pixel stamps directly formatted as `.glideexchange` and Markdown files matching task format 26.
- **Validation:** Test agent output files locally using `python3 -B tests/tools/ki_ausgabe.py <FILE>`.

## Run from source (macOS, Windows, Linux)

Requirements:

- Python **3.14 with Tk 9** is recommended. Python 3.12/3.13 and Tk 8.6 start with known limitations.
- Standard library only; no extra pip dependencies required for core usage.
- Optional: `tkinterdnd2` for native drag and drop.

From the repository root:

```bash
cd 01_Repository/Glide
python3 src/glide/app.pyw
```

On Windows: `python src\glide\app.pyw`. Keep the resources in `src/glide/resources` next to the application.

## Window size

The main window needs at least **860 × 700 px**. Compact mode (**View › Compact mode**, Ctrl/Cmd+Shift+K) works down to **480 × 560 px**. In small windows, controls that do not fit move into the "⋯" button, the context menu, the menu bar or a shortcut. They are never squeezed or cut off.

## Your data folder

Glide stores your content outside the program folder:

| Platform | Default data folder |
|---|---|
| Windows | `%APPDATA%/Glide` |
| macOS | `~/Library/Application Support/Glide` |
| Linux | `$XDG_DATA_HOME/Glide`, otherwise `~/.local/share/Glide` |

**Settings › Appearance & Controls › Change data folder …** (also **File › *Datenablage* › *Datenordner wechseln …***) moves to another folder. **File › *Datenablage* › *Wo liegen meine Daten?*** shows the current folder. The new folder must be empty, or it must already contain a Glide collection. If a folder you chose is not reachable when Glide starts, for example because an external drive is not mounted, Glide shows the path and quits safely without creating or deleting anything. Details: [backups](10-backups.md) and [data and migration (German)](../06_DATA_BACKUP_MIGRATION.md#ablage).

Your user data remains intact when updating or uninstalling Glide.

## Trying Glide safely

To explore Glide with synthetic data without touching your personal workspace, use the [showcase (German)](../../../../05_Probelisten_Testdaten/Showcase/README.md). It uses its own separate data folder.
