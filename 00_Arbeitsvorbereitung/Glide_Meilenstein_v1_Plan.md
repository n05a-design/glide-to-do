# Meilenstein- und Fahrplan Release 1.0 (Glide 1.0.0)

Stand 17.11.2026 · Glide 1.0.0 · Aufgabenformat 26 · Glide-System V1.40

Dieser Plan definiert den verbindlichen **Schnittpunkt (Feature Freeze / D93)** für die offizielle **Version 1.0 von Glide**, die als GitHub-Release veröffentlicht und über **Homebrew** (macOS) und **winget** (Windows) bereitgestellt wird. Er beantwortet die Frage, wo die Grenze gezogen wird, um endlosen Scope Creep zu verhindern.

Tracking-Issue: [GitHub Issue #129](https://github.com/n05a-design/glide-to-do/issues/129)

---

## 1. Strategischer Schnittpunkt: Was gehört in Version 1.0 (und was nicht)?

Um nicht endlos weiterzuentwickeln, wird der Umfang für **Version 1.0** strikt auf die Kernanforderungen für einen erstklassigen ersten öffentlichen Auftritt begrenzt.

```mermaid
flowchart TD
    subgraph V1 ["Glide Version 1.0 (Scope Freeze / D93)"]
        S["1. Agenten-Skill komplett<br/>(K4 Bilder/Anhänge + K5 Verteilung)<br/><b>✅ ERLEDIGT (PR #130)</b>"]
        I["2. Mehrsprachigkeit<br/>(Englisch & Deutsch umschaltbar)<br/><b>✅ ERLEDIGT (PR #134)</b>"]
        P["3. Paketierung & Installer<br/>(macOS DMG / Windows Setup.exe)<br/><b>✅ ERLEDIGT (PR #135)</b>"]
        M["4. Paketmanager-Einbindung<br/>(Homebrew Cask + winget Manifest)<br/><b>✅ ERLEDIGT (PR #135)</b>"]
        Q["5. Grüne CI-Vollmatrix & Release Cut<br/>(macOS arm64, Windows x64, Linux)<br/><b>✅ ERLEDIGT</b>"]
    end

    subgraph POST ["Version 1.1+ / Spätere Versionen"]
        S6["Shell-Paket 6 Demonstrationshost & glide_shell Bündelung"]
        CAL["CalDAV / Kalender-Sync"]
        LANG["Weitere Sprachen (FR, ES, ...)"]
        MOB["Mobile Apps / Cloud-Option"]
    end

    V1 -.->|Release Cut v1.0.0| POST
```

### Der verbindliche Leistungsumfang (Must-Haves für v1.0)
1. **Vollständiger Agenten-Skill `glide-to-do` (✅ Abgeschlossen):**
   - K1–K3: Austauschformat 2, Labels, Vorsicherung, Markdown, Ordnerarten, Wiederholungen, Erinnerungen.
   - **K4 (Bilder & Anhänge):** ZIP-Container (`.glideexchange`/`.zip`), Zip-Slip-Schutz, Anhänge für Aufgaben/Listen/Ordner in `ATTACHMENTS_DIR`, Galerielisten, Seiten-Cover, Markdown-Bildauflösung, Export (`write_exchange_package`), Rollback-Bereinigung.
   - **K5 (Ökosystem & Verteilung):** `MANIFEST.json`, `VERTEILUNG.md`, Desktop-Menüaktion `export_agent_skill`, Workflow-Paketierung in GitHub Release-Assets (`glide-to-do-skill-v$VERSION.zip`).
2. **Mehrsprachigkeit (i18n: Deutsch & Englisch) (🎯 Nächster Schritt):**
   - Komplette App-Oberfläche umschaltbar: Automatisch (nach OS), Deutsch, Englisch.
   - Menüs (`desktop_adapter.py`), Werkzeugleiste, Seitenleiste, Kern-Dialoge, Einstellungen, Status- und Fehlermeldungen.
   - Modul `src/glide/i18n.py` (M100) im Glide-System (Standardbibliothek only, Modulbudget-konform).
3. **Plattformpakete & Installer:**
   - **macOS:** `.app`-Bundle, `.dmg` und `.tar.gz` (Ad-hoc signiert, arm64).
   - **Windows:** Inno-Setup-Installer `Glide-setup.exe` (Startmenü-Icon, saubere Deinstallation, AppUserModelID `Shaye.Glide`, unprivilegiert nach `%LOCALAPPDATA%\Programs\Glide`) + portable `.zip`.
4. **Paketmanager:**
   - **Homebrew:** Cask `packaging/homebrew/Casks/glide.rb` im Repository `n05a-design/homebrew-glide`.
   - **winget:** Manifeste `packaging/winget/manifests/s/Shaye/Glide/` für `winget install Shaye.Glide`.
5. **Qualität:**
   - Alle CI-Workflows 100 % grün (Linux-Vollprüfung, Windows x64, macOS arm64).

> [!IMPORTANT]
> **Was bewusst NICHT in Version 1.0 kommt (Post-1.0):**
> Tiefere interne Shell-Umbauten (Shell-Paket 6 Demonstrationshost, Namespace-Bündelung `glide_shell`), zusätzliche Sprachen jenseits DE/EN, externe Kalendersynchronisation (CalDAV) oder Plugin-Systeme werden bis nach Version 1.0 zurückgestellt.

---

## 2. Die vier Etappen bis zum Release v1.0

### Etappe 1: Agenten-Skill komplettieren (Paket K4 & K5) – ✅ ERLEDIGT
- **K4 (Bilder und Dateianhänge im Austausch):**
  - ZIP-Container-Erkennung mit Zip-Slip-Schutz (`inspect_exchange_archive`).
  - Physischer Import von Anhängen für Ordner, Listen, Aufgaben in `ATTACHMENTS_DIR`.
  - Galerielisten (`list_kind: "gallery"`), Cover (`cover`), Markdown-Bildauflösung.
  - Paketausgabe (`write_exchange_package`) und atomare Rollback-Bereinigung.
- **K5 (Verteilung):**
  - `MANIFEST.json` mit Hashes aller 18 Skill-Dateien.
  - `VERTEILUNG.md` für Claude Desktop, Cursor, Gemini CLI, Web-LLMs.
  - App-Menüfunktion `export_agent_skill`.
  - GitHub Actions Workflow packt Skill-ZIP mit Prüfsummen.
- **Nachweis:** Integrationstest T328 (`test_austausch_k4.py`, 9/9 OK), Werkzeugtest T321 (18/18 OK), PR #130 gemergt.

### Etappe 2: Mehrsprachigkeit (i18n: Deutsch / Englisch) – ✅ ERLEDIGT
- **Architektur:**
  - Neues leichtgewichtiges Modul `src/glide/i18n.py` (M100) im Glide-System (Standardbibliothek only, Modulbudget max. 50 Zeilen je Funktion, WA-50 konform).
  - Strukturierte Übersetzungskataloge: `src/glide/resources/locales/de.json` und `src/glide/resources/locales/en.json`.
  - Robuster Aufruf: `t(key, default, **kwargs)` mit sicherer Formatierung (`safe_format`).
  - Einstellungsdialog: Dropdown zur Sprachauswahl (`Automatisch (System)`, `Deutsch`, `English`), persistiert in `settings.json` als `language`.
- **Übersetzungsumfang:**
  - Menüleiste (`menubar_structure` / `create_menubar`) und Tastaturkürzel/Mnemonics.
  - Seitenleiste (Systembereiche: Startseite, Heute, Eingang, Labels, Vorlagen, Papierkorb).
  - Aktionsleisten, Knöpfe, Inspektoren und Einstellungen.
- **Nachweis:**
  - Neuer Test T329 (`test_i18n.py`): 11 Tests für Spracherkennung, Auflösung, Fallbacks, 100 % Schlüsselparität und 100 % Platzhalterparität zwischen `de.json` und `en.json`, WA-50-Budget.
  - Werkzeugtest `test_modulbudget.py` um `i18n.py` erweitert.
  - Systemregister auf V1.40 angehoben (`test_glide_system.py` 5/5 OK).
  - CI-Grundstufe 19/19 OK.

### Etappe 3: Paketbau, Installer & Paketmanager-Vorbereitung – ✅ ERLEDIGT
- **macOS:**
  - DMG-Erzeugung in `.github/workflows/macos-paket.yml` verifiziert.
  - Homebrew-Cask `packaging/homebrew/Casks/glide.rb` aktualisiert auf Version 3.70.0.
- **Windows:**
  - Inno-Setup-Skript `packaging/windows/glide_setup.iss` für unprivilegierte Benutzer-Installation nach `%LOCALAPPDATA%\Programs\Glide`, Startmenüeintrag (`AppUserModelID: "Shaye.Glide"`), Sprachunterstützung (DE/EN) und saubere Deinstallation ohne Nutzerdatenverlust.
  - Build-Schritt in `.github/workflows/windows-paket.yml` verankert (Erzeugung von `Glide-$version-windows-x64-setup.exe` samt SHA-256 und Artefakt-Upload).
  - Release-Workflow `.github/workflows/release.yml` um Installer-Einbindung und Download-Tabelleneintrag erweitert.
  - winget-Manifeste unter `packaging/winget/manifests/s/Shaye/Glide/3.70.0/` auf `InstallerType: inno` und zweisprachige Metadaten (de-DE, en-US) umgestellt.

### Etappe 4: Release Cut, GitHub-Release & Veröffentlichung – ✅ ERLEDIGT
- **Versionierung:**
  - Anheben der Version auf `1.0.0` (über `scripts/pflege/versionswechsel.py 1.0.0 17.11.2026 --ohne-ablagekuerzung`).
  - Systemregister auf V1.40 gehoben (100 Module M001–M100, 329 Testdateien T001–T329).
  - Standprüfung (86 Dokumente, 0 Befunde) und Lieferabgleich `abgleich_07.py` (0 Abweichungen).
  - GitHub Actions `release.yml` baut automatisch alle Artefakte und berechnet SHA-256-Hashes bei Git-Tag `v1.0.0`.
- **Veröffentlichung:**
  - GitHub Release v1.0.0 veröffentlichen.
  - Manifeste für Homebrew Cask und winget auf v1.0.0 aktualisiert.

---

## 3. GitHub Issue Tracking (#129)

Aktueller Stand in [Issue #129](https://github.com/n05a-design/glide-to-do/issues/129):

- [x] **1. Agenten-Skill `glide-to-do` (WA-61)** (K1–K5 vollständig abgeschlossen via PR #127, PR #128, PR #130)
- [x] **2. Mehrsprachigkeit (i18n: Deutsch / Englisch)** (M100 `i18n.py`, JSON-Kataloge, Einstellungen, Lokalisierung Menüs/Seitenleiste, T329 via PR #134)
- [x] **3. Paketierung & Installer** (macOS DMG, Windows Inno-Setup `Glide-setup.exe`, GitHub Workflows via PR #135)
- [x] **4. Paketmanager** (Homebrew Cask 1.0.0, winget Manifeste 1.0.0)
- [x] **5. Qualität & Freigabe** (100 % grüne Vollmatrix, Release Cut v1.0.0)
