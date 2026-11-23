# Glide – Übergabe an eine neue Sitzung

Stand 23.11.2026 · Glide 1.0.2 · Aufgabenformat 26 · Glide-System V1.86 · Glide Shell 0.6.2 · Multi-Agent Readiness (abgeschlossen) · Lokalisierung DE/EN vollständig · Release-Härtung 1.0.2 auf `fix/glide-1.0.2-release-hardening` (PR #195, Zielbranch `main`; historisch: `claude/v101-release`, `glide_shell_multi_agent_readiness`) · kein Tag, kein GitHub-Release, keine Paketmanager-Einreichung

Einstieg für die nächste Sitzung: tatsächlichen Entwicklungsstand, Dokumentenautorität, nächste Arbeit und Arbeitsregeln. Aufgaben und Rest führt der [Entwicklungsplan](Glide_Entwicklungsplan.md), den Soll-Umfang Release 1.0 der [Meilenstein-Plan](Glide_Meilenstein_v1_Plan.md) und das öffentliche Tracking [Issue #129](https://github.com/n05a-design/glide-to-do/issues); Prüfergebnisse stehen im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md), Entscheidungen in der [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md). Frühere Übergabestände und historische rote Läufe bleiben in Git erhalten.

**Aktueller Stand (23.11.2026):** `main` steht auf `1d5f01a2` (Merge PR #194). PR #191, #192, #193 und #194 sind vollständig in `main` gemergt. Die anschließende Release-Härtung von Glide 1.0.2 in PR #195 (`fix/glide-1.0.2-release-hardening`) schließt verbliebene Sicherheits-, Integritäts-, Test- und Dokumentationslücken ab: Die Glide Shell verfügt über transaktionale Übernahme mit Snapshot-Integrität und atomarem Bootstrap-Rollback (`BootstrapTransaction` auch standalone via `bootstrap_agenten()`), synchronisierte Manifest-Integrität (`shell_uebernehmen.py` und `selftest.py`), terminierende Fehlerbehandlung bei fehlgeschlagenem Verzeichniswechsel unter PowerShell (`Set-Location -LiteralPath ... -ErrorAction Stop;`), sichere POSIX-Kommandos (`shlex.quote`), deduplizierten Skill-Generatorcode, Unterstützung verschachtelter Ziel-Layouts (`src/app/glide_shell`), dynamische relative Linkberechnung mit Leerzeichen-Encoding (`%20`), isolierten Referenzhost (T337), agentenübergreifende Einstiege (T338), manipulationssichere 13/13 Selbsttests mit Spoofing-Schutz, den offline verfügbaren portablen Designvertrag (`glide_shell/DESIGN_RICHTLINIEN.md`) sowie dessen automatisierte Konsistenzprüfung (`test_design_vertrag_konsistenz.py`). Die UI-Regressionen (T340) sind durch tiefe Integrationsprüfungen für adaptiven Titelbildzuschnitt (Hoch-/Querformat, Skalierungsgrenze, Fokuspunkt), kollisionsfreien Bild-/Tabellenumfluss und den vollständigen Lebenszyklus des Pixel-Ecksymbols mit echten Widgets belastbar abgesichert.

> [!IMPORTANT]
> **Release 1.0 (D93) – Soll-Ist**
> - **Etappe 1: Skill komplettieren (K4 & K5):** ✅ abgeschlossen (PR #130, PR #133, V1.39, T328)
> - **Etappe 2: Mehrsprachigkeit (i18n DE/EN):** ✅ abgeschlossen: gesamte Oberfläche, Handbuch, Austauschformat und KI-Ausgabe (V1.70–V1.79, T335), englische Schnellerfassung (V1.81)
> - **Glide Shell:** ✅ abgeschlossen: `glide_shell` 0.6.2 mit Demonstrationshost, Referenzhost (T337), Selbsttest, Anleitung, KI-Handbuch und Bausteinen D94–D98 (V1.64–V1.69), WA-49 (V1.83) sowie Befehlsverlauf und App-Host als Konzeptphasen 4 und 5 (V1.84, D99)
> - **Etappe 3: Paketierung & Installer:** ✅ technisch fertig; macOS-Paket und DMG lokal gebaut und geprüft, Windows-Installer in der CI. Homebrew-/winget-Vorlagen nicht eingereicht.
> - **Etappe 4: Release & Veröffentlichung:** ◐ Quellstand bereit; menschliche Sicht- und Bedienabnahme durchgeführt (23.11.2026); Tag, GitHub-Release und Paketmanager-Einreichung nur mit Freigabe des Inhabers.
>
> **Erste Handgriffe einer neuen Sitzung:** aktuellen `main` holen, offene PRs und ihre CI prüfen, dann [Entwicklungsplan §3](Glide_Entwicklungsplan.md) und [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md) lesen. Keine Releases, Tags, Force-Pushes oder Einreichungen ohne ausdrückliche Freigabe.

---


### Menschliche Sicht- und Bedienabnahme Release 1.0 (Etappe 2) & Layout-Verfeinerung (23.11.2026)

- **Menschliche Abnahme durchgeführt:** Alle 5 Prüfschritte aus `00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md` wurden durch den Inhaber auf dem Kandidatenstand durchlaufen und positiv abgenommen.
- **Dynamischer Sprachwechsel (Schritt 1):** `refresh_sidebar_locale()` aktualisiert Seitenleisten-Titel (Seiten/Pages, Listen/Lists, Notizen/Notes, Zeichnungen/Drawings) und Tooltips bei Sprachwechsel in `apply_settings()` sofort ohne Neustart.
- **Adaptiver Zuschnitt von Titelbildern (Schritt 2):** `make_page_cover(..., adaptive=True)` mit `COVER_RATIO = 0.34`, `COVER_MAX_HEIGHT = 240`, `COVER_FOCUS = 0.38`, `COVER_MAX_UPSCALE = 1.5` verhindert vertikale Verzerrung und zentriert das Bild optimal.
- **Zeichnungen als kompakter Eckstempel (Schritt 2):** Pixel-Zeichnungen als Cover sitzen als 56px-Miniatur (`CORNER_COVER_SIZE = 56`) oben rechts in der Lesespalte und scrollen mit dem Text (`show_corner_cover`, `layout_corner_cover`, `place_corner_cover`).
- **Fußleisten-Dichte (Schritt 2):** `sync_foot_density()` blendet „Erwähnt ohne Verweis …“ bei minimaler Kopfstufe (`minimal`) aus, so dass die Fußzeile einzeilig bleibt.
- **Kollisionsfreier Bild- und Tabellenumfluss (Schritt 2):** `imgflow:right` und `cornerflow` erzwingen `wrap='word'` im Umflussbereich, so dass Tabellen und Bildflächen niemals überlappen. Stadtseiten mit Tabellen (Wuppertal, Berlin) nutzen im Showcase linksbündige Bilder (`mode='left'`), und alle 3 Modi (`left`, `center`, `right`) sind im Showcase vertreten.
- **Tastatur & Editor (Schritte 3 & 4):** Vom Inhaber vollständig positiv abgenommen („Passt komplett“, „Funktioniert perfekt!“).
- **Natürliche Datumswörter (Schritt 5):** `parse_due_words` erkennt „today“, „heute“, „tomorrow“, „morgen“, „yesterday“, „gestern“ im Datumsfeld und Kalenderdialog.
- **Geprüfter Stand:** `pruefe_showcase.py` (DE und EN), `ci_grundstufe.py` (19/19 Schritte), `standpruefung.py` (148 Dokumente) und `test_release_1_0_2_regressions.py` (T340, 20/20 Tests mit realistischer UI-Integration für Titelbild, Umfluss, Ecksymbol, Sprachwechsel, Fälligkeit und Persistenz) vollständig grün; `07_Python-Versionen` bytegleich abgeglichen.


### Multi-Agent Readiness & Verified Reuse (V1.86, Shell 0.6.2, 23.11.2026)

- **Agentenübergreifender Einstieg (T338):** Schlanker `AGENTS.md` in der Repository-Wurzel, `glide-shell`-Skill unter `.agents/skills/` gespiegelt zu `.claude/skills/`, `.github/copilot-instructions.md` und `.gemini/settings.json` ergänzt. Trennung von Produkt-Skill `glide-to-do` und Shell-Entwicklungsskill strikt gewahrt.
- **Reproduzierbare & transaktionssichere Übernahme (T331, 36 Tests):** `shell_uebernehmen.py` mit vollständiger Erfassung von Rollback-Fehlern ohne `pass`, atomarer `BootstrapTransaction` (auch für eigenständigen `bootstrap_agenten()`-Aufruf), synchronisierter Manifest-Integrität zu `selftest.py` (Ausschluss maskierter lokaler Änderungen, expliziter Fehlerausweis bei fehlendem/ungültigem Manifest), sicheren zsh-/bash-Kommandos (`shlex.quote`) und terminierenden PowerShell-Befehlen (`Set-Location -LiteralPath ... -ErrorAction Stop;`), Bereinigung doppelter Skill-Generatorblöcke, Symlink- und Dateitypschutz (`is_symlink()` vor `exists()`, Abweisung externer Ziele vor Mutation), Schutz vor unvollständigen Snapshots, RFC-3986-URL-Quoting für Pfade mit Leerzeichen/Klammern (`%20`, `%28`, `%29`) sowie 10 Fehlerszenarien in der Regressionsprüfung nachgewiesen.
- **Verschachtelte Layouts, Bootstrap-Inhaltsprüfung & Status:** Ermittlung der Projektwurzel anhand von Markern oder Python-Layouts sowie Vorgabe per `--projekt-root`. `--pruefen --agenten-bootstrap` mit Statusdifferenzierung (`korrekt verwaltet`, `gültig angepasst`, `veraltet`, `beschädigt`, `nicht vorhanden`, `nicht überprüfbar`). Dynamische relative POSIX-Links in `AGENTS.md` und Skills für beliebige Ordnertiefen.
- **Selbsttest & Spoofing-Schutz (T333, 13/13):** Autonome Validierung über `SHELL_MANIFEST.json` ohne Glide-Checkout, inklusive Pfad- und Symlinksicherheit sowie gehärteter Quellbaum-Erkennung.
- **Multi-Host UI-Provider-Isolation & B15-GUI-Abnahme (T336, 15 Tests):** Hierarchischer Fallback (`widget` → `toplevel` → global) für Schriften, Verläufe und Glyphenmetrik mit 4-Argument-Signatur. Echte Tk-Integrationsprüfung (860x700 und 1280x800) für ButtonFlow, B15-Klemmung, Tastaturnavigation und Modalfokus.
- **Substanzielle Designvertrag-Konsistenzprüfung (T339, 9 Tests):** Inhaltliche Verifikation von P1–P6, B15, B11, B01/B16, B03, B10/B12/B14, WCAG AA Kontrast (4.5:1 Text, 3:1 UI), Fokus/Tastatur, 13 Shell-Schnittstellen und Markengrenzen inklusive 6 Negativgegenproben.
- **End-to-End-Referenzhost & Consumer-Projekte (T337, 5 Tests):** Testprojekt A (vollständig isolierter AppHost mit Dialogen und Timern), Testprojekt B (historischer Upgrade 0.5.0 Commit `3c91e0c8` auf 0.6.2 unter Erhalt aller Host-Dateien und Konfigurationen) und Testprojekt C (Diagnose beschädigter Installationen und `python -O` Selbsttest).
- **Prüfergebnis:** CI-Grundstufe (19/19) und alle Shell-Suiten (109 Tests) lokal bestanden. PR #195 führt die CI-Matrix auf GitHub.

## 0. Sofortübergabe WA-41 – zuerst lesen

> [!IMPORTANT]
> Diese Überschrift bleibt als bestehendes Linkziel im Gesamtsystem unverändert erhalten. Sie betrifft die historische Fehleruntersuchung zur Systemstabilität; aktuelle operative Entwicklungsprioritäten stehen in [Abschnitt 3](#3-nächste-arbeit-und-handlungsanweisungen).

- **WA-41A:** Sporadische Interpreter-/Prozessfehler auf PC-02 Intel, unter anderem `0xC0000005`, `0xC0000409`, „Executing a cache“. WHEA-/Systembefunde sind eine Hardware-Spur, kein abschließend bewiesener CPU-Defekt.
- **WA-41B:** Einmalig abweichender gespeicherter/geladener künstlicher Bestand; konkrete betroffene Felder und Ursache ungeklärt, kein belegter Verlust echter Nutzerdaten. Beide Spuren getrennt erhalten.
- **AMD-Gegenlauf:** Zehn isolierte AMD-Prozesse waren grün; vollständige Suiten erzeugten UUIDs/Zeitstempel selbst. Kein byteidentischer Intel-Replay und kein Ursachenbeweis. Siehe [AMD-Nachweis](https://github.com/n05a-design/glide-to-do/blob/40c20fd62db6ec31b4e3668dfc9e7f1550f67974/01_Repository/Glide/tests/qa-3.48.0/amd_vergleich_2026-10-27/README.md) und [Gerätevergleich](https://github.com/n05a-design/glide-to-do/blob/f1a5b5b6e0f97f2b5eab1ac552999c33c6416e69/01_Repository/Glide/tests/qa-3.49.0/geraetevergleich_2026-10-29/README.md).
- **Stabilitäts-Vorgabe:** BIOS-/CPU-Einstellungen nicht ändern, keine unnötige neue Stressserie am instabilen PC-02. Keine spekulativen Mengenschranken, kein Chunking oder willkürliches `gc.collect()` als angeblicher Fix. Historischen Referenzstand und Originalkriterien bewahren.
- **Dokumentierte Referenzen:** [Ursachenanalyse](https://github.com/n05a-design/glide-to-do/blob/40c20fd62db6ec31b4e3668dfc9e7f1550f67974/01_Repository/Glide/tests/qa-3.48.0/wa41_2026-10-27/README.md), [Python-Vergleich](https://github.com/n05a-design/glide-to-do/blob/40c20fd62db6ec31b4e3668dfc9e7f1550f67974/01_Repository/Glide/tests/qa-3.48.0/python315_vergleich_2026-10-27/README.md), [WHEA-/Lastbefunde und Dumpinventar](https://github.com/n05a-design/glide-to-do/blob/594f4c85eb60370a44282b06fcb8017df8181d70/01_Repository/Glide/tests/qa-3.50.5/abnahme_2026-11-05/aufbewahrung.json), [470-Dateien-Referenz](https://github.com/n05a-design/glide-to-do/blob/594f4c85eb60370a44282b06fcb8017df8181d70/01_Repository/Glide/tests/qa-3.50.5/abnahme_2026-11-05/aufbewahrung.json). Spätere Schutzfunktionen und Lieferungen schließen diese Ursachenfragen nicht.
- **Geschützte lokale Bestände:** `01_Repository/Glide/tests/qa-3.48.0/lokale_belege/eingang/initial.json` und `lokale_belege/minidumps/`; [Sicherungsmanifest](https://github.com/n05a-design/glide-to-do/blob/594f4c85eb60370a44282b06fcb8017df8181d70/01_Repository/Glide/tests/qa-3.50.5/abnahme_2026-11-05/aufbewahrung.json). Anfangsbestand 28.548.872 Bytes, SHA-256 `a3b8c0cac4c72e1820e71730ad78e312f2a30338678fbcfe2a2b6d91dae081f4`. Acht bekannte Minidumps sind keine FullMemory-Aufnahmen. Ein früher genannter externer Exportordner wurde nicht lokal bestätigt; keine Originale löschen.
- **Ablagegrenze:** Dumps, Rohlogs und lokale Eingänge bleiben Git-ausgeschlossen und sind bei Rechnerwechsel ausdrücklich geschützt zu übertragen. Temporärpfade und Runtimeorte aus alten Berichten vor Wiederverwendung prüfen; Version, `sys.executable`, Tk und Binärhashes erfassen. Der Standardbefehl `python` ist kein Laufzeitnachweis.

---

## 1. Tatsächlicher Stand

| Achse | Stand |
|---|---|
| **Version & Schemata** | **Glide 1.0.2** · Aufgabenformat **26** · Einstellungen **2** · Vorlagen **2** · Glide-System **V1.86** (Register und Zählungen in [Glide-System](../01_Repository/Glide/src/glide/README.md)) |
| **Meilenstein Release 1.0** | Feature Freeze (D93). Skill, Lokalisierung, Shell, Paketbau und menschliche Sicht- und Bedienabnahme (23.11.2026) sind vollständig abgeschlossen; offen sind nur Veröffentlichung und Paketmanager-Einreichung nach Inhaberfreigabe. |
| **Agenten-Skill `glide-to-do` (1.0.0)** | **WA-61 (K1, K2, K3, K4, K5 vollständig):** Zentrierte Skill-Implementierung unter `01_Repository/Glide/skills/glide-to-do/`. Formatkopplung an Format 26 über `abdeckung.json`.<br/>- **K1:** Grundskill auf Austauschformat 2.<br/>- **K2:** Labels an Ordnern und Listen, Labelfarbe, KI-Prompt-Schärfung.<br/>- **K3 (E-K5 Option A):** Automatische dateibasierte Vorsicherung vor Import (`vor_import_*.glidebackup`), Markdown-Listen (`markdown` -> `rich_note` mit Checkbox-Aufgabenextraktion), Ordnerarten (`library`, `journal`, `standard`), Wiederholungsregeln (`repeat` tolerant EN/DE mit `kind`-Rundlauf), Erinnerungen (`reminder` relativ/fest).<br/>- **K4 (Bilder/Anhänge):** ZIP-Container (`.glideexchange`/`.zip`) mit Zip-Slip-Schutz (`inspect_exchange_archive`), physischer Import von Anhängen (`ATTACHMENTS_DIR`) mit Prüfsummen- und Namenskonfliktbereinigung (`store_attachment`), Galerie-Listen (`list_kind: "gallery"`), Seiten-Cover (`cover`), Markdown-Bildauflösung in Notizen, Paketausgabe (`write_exchange_package`), atomares Rollback bei Importfehlern.<br/>- **K5 (Verteilung):** `MANIFEST.json` mit Hashes aller 18 Skill-Dateien, `VERTEILUNG.md` für Claude Desktop, Cursor, Gemini CLI, ChatGPT/Web-LLMs, App-Menüfunktion `export_agent_skill`, Release-Workflow (`glide-to-do-skill-v$VERSION.zip`). T327 (`test_austausch_k3.py`, 6/6 OK), T328 (`test_austausch_k4.py`, 9/9 OK), T321 (18/18 OK). |
| **Shell-Paket `glide_shell`** | Abgeschlossen: Unterpaket `src/glide/glide_shell` mit `SHELL_VERSION` 0.6.2, Demonstrationshost, Referenzhost (T337), Selbsttest (13/13), Anleitung DE/EN und [KI-Handbuch](../01_Repository/Glide/docs/GLIDE_SHELL_KI_HANDBUCH.md); Übernahme in Folgeprojekte mit `scripts/pflege/shell_uebernehmen.py`. Weitere Shell-Arbeit nur aus konkretem Bedarf. |
| **Prüfstand** | Führend ist der [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md) mit dem lokalen macOS-Volllauf, Paket und DMG der Release-Runde 1.0.2. |
| **Lieferstand** | `07_Python-Versionen` wird in der Produktionsrunde 1.0.2 mit `abgleich_07.py` und SHA-256 auf den Quellstand gebracht. |
| **Ablage-Schutz** | Unberührt und NICHT in Git: `20_Grafik_Master/09_Inspiration/`, `GLIDE_STEPS_GESAMTAUDIT_V2_2026-11-10/`, `glide_master_audit_bericht.md` und `SQLite-Copyright.md`. Diese Pfade dürfen unter keinen Umständen gestaget oder committet werden. |


---

## 2. Zuständige Dokumente und Autoritätsmatrix

In diesem Projekt gilt die Regel **„Ein Thema, ein führendes Dokument“**. Kein Dokument dupliziert die Autorität eines anderen.

```mermaid
flowchart TD
    AR["ARBEITSRICHTUNG.md<br/>(Verbindliche Entscheidungen D01–D99)"] --> EP["Glide_Entwicklungsplan.md<br/>(Gesamter Arbeitsvorrat & Historie)"]
    MPLAN["Glide_Meilenstein_v1_Plan.md<br/>(Verbindlicher Schnittpunkt Release 1.0)"] --> EP
    ISSUE["GitHub Issue #129<br/>(Meilenstein-Tracking v1.0.0)"] --> MPLAN
    PC["01_PRODUCT_CONSTRAINTS.md<br/>(Unverrückbare Produktgrenzen)"] --> EP
    EP --> PROD["01_Repository/Glide/src/glide<br/>(Quellcode & Implementierung)"]
    DR["DESIGN_RICHTLINIEN.md<br/>(Gestaltungsregister, Farben, Schriften)"] --> PROD
    SK["GLIDE_SHELL_FRAMEWORK_KONZEPT.md<br/>(Shell-Grenzen und Entkopplungsziel)"] --> PROD
    PROD --> QA["07_QA_BERICHT.md<br/>(Prüfergebnisse, CI-Status, Plattformbelege)"]
    PROD --> MAN["Glide_Manuelle_Pruefung.md<br/>(Menschliche Abnahmeliste für Inhaber)"]
    DP["DOKUMENTENPFLEGE.md<br/>(Konsistenzmatrix bei Versionswechsel)"] --> PROD
    UEB["Glide_Uebergabe.md<br/>(Einstieg & Handover für KI-Agenten)"] --> MPLAN
```

| Dokument | Führende Zuständigkeit |
|---|---|
| [`00_Arbeitsvorbereitung/Glide_Meilenstein_v1_Plan.md`](Glide_Meilenstein_v1_Plan.md) | **Verbindlicher Meilenstein- und Fahrplan Version 1.0 (D93):** Definiert den exakten Scope Freeze, die vier Etappen bis zum öffentlichen Release sowie Paketmanager-Ziele (Homebrew, winget). |
| [GitHub Issue #129](https://github.com/n05a-design/glide-to-do/issues/129) | **Öffentliches Meilenstein-Tracking:** Führt den aktuellen Fortschritt der fünf Meilenstein-Kernelemente. |
| [`00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md`](Glide_Entwicklungsplan.md) | **Einziges Planungsdokument:** Führt den gesamten Arbeitsvorrat ([§Aktueller Arbeitsvorrat](Glide_Entwicklungsplan.md#aktueller-arbeitsvorrat)), historische Sprints und chronologische Umsetzungsberichte ([§21.98](Glide_Entwicklungsplan.md#2198-richtungsentscheidungen-zur-shell-trennung-d86d90-15112026)–[§21.110](Glide_Entwicklungsplan.md#21110-agenten-skill-pakete-k4--k5-bilderanhänge-im-austausch--verteilung-17112026)). Es entsteht kein zweiter Backlog! |
| [`01_Repository/Glide/docs/ARBEITSRICHTUNG.md`](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md) | **Verbindliche Architektur- und Prozessentscheidungen:** Register D01 bis D93 (D93: Release 1.0 Meilensteinschnitt). |
| [`01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md`](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md) | **Produktgrenzen:** Was Glide bewusst ist und was es strikt ausschließt (kein Cloud-Sync, keine Telemetrie, keine Online-Konten, Offline-First). |
| [`01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md`](../01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md) | **Gestaltungsregister & UI-Verträge:** Typografie (Rubik, DM Mono, DM Serif Display, Charis SIL), Farben, Abstände, Randmaße und verbindliche D83-Regeln. |
| [`01_Repository/Glide/docs/07_QA_BERICHT.md`](../01_Repository/Glide/docs/07_QA_BERICHT.md) | **Prüf- und Lieferstände:** Führt die tatsächlichen Testergebnisse, CI-Status, Plattformnachweise und Grenzwerte geordnet nach Version und Commit. |
| [`00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md`](Glide_Manuelle_Pruefung.md) | **Menschliche Abnahmeliste:** Fälle, die ausschließlich vom Inhaber interaktiv am Mac geprüft werden können (DPI, Sicht, Bedienung). |
| [`01_Repository/Glide/docs/DOKUMENTENPFLEGE.md`](../01_Repository/Glide/docs/DOKUMENTENPFLEGE.md) | **Pflegematrix:** Regelt, welche Dateien bei Versionswechsel, Merges oder neuen Modulen zwingend synchron nachgezogen werden müssen. |
| [`01_Repository/Glide/docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md`](../01_Repository/Glide/docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md) | **Shell-Grenzen und Entkopplungsziel** (abgeschlossen nach D99; Bausteine und Grenzen von `glide_shell` und Demonstrationshost). |
| [`01_Repository/Glide/AGENTS.md`](../01_Repository/Glide/AGENTS.md) | **Agenten-Regeln:** Repository-spezifische Richtlinien für autonome Agenten. |

---

## 3. Nächste Arbeit und Handlungsanweisungen

Der Einstellungsdialog samt stabiler Rückspeicherung (§21.121) ist in PR #148 gemergt; Seiteneditor, Aktionsfeedback, Tastenkürzel-Modifier, Aufgabeninspektor, Kalenderfelder, Editorstatus und Mehr-Menü (§§21.122–21.124) sind mit PR #150 in `main`. PR #154 (Governance/English-first) und PR #156 (Ansichtenreparatur) sind ebenfalls gemergt. Die lokale Fortsetzung (§§21.144–21.145) lokalisiert Statusmeldungen, Werkzeugwahl, Anzeigeprofile, Referenz-/Vorschauknöpfe, Zoom und Kontextmenüs des Zeicheneditors. Animationsleiste, Mehr-Menü-Inhalte, weitere Dialoge sowie Zeichen-/Exportmeldungen bleiben offen. Die menschliche DE/EN-Sicht-/Bedienabnahme ist in der [manuellen Prüfliste](Glide_Manuelle_Pruefung.md#offene-sicht-und-bedienabnahme-deen-release-10-etappe-2) ausdrücklich offen. Wiki-Inhalte/Synchronisation sind nach I11 B nicht ausgewählt; E-P1–E-P5 sowie sonstige Funktionsvorschläge werden dadurch nicht ausgewählt. Release-, Konto- und Produktentscheidungen bleiben beim Inhaber.

**Nächster technischer Schnitt:** (1) Ergebnis des macOS-Workflows auf `17c06424` auswerten und rote Schritte beheben. (2) Stapel #161 → #164 nach Freigabe mergen. (3) Nächster Etappe-2-Schnitt im Zeicheneditor: Import- und Einfügevorschau, Bildfolgen-Dialog und -Export, Symbolvorschau, Farbwahl; danach Journal-Untermenü, `RoundedButton.action_text` und dynamische Undo-Texte appweit (Plan §21.151 D). Eine lokale Mac-Vollprüfung braucht einen ungestörten Rechner oder `--vordergrund`; lokal ist der Paketbau blockiert, weil der Quellenabruf für die Lizenzbasis nur im Hosted-CI erlaubt ist (QA-Bericht). Keine Tags/Release, Signierung/Notarisierung, Homebrew-/winget-Einreichung oder externe Kontoaktionen ohne Freigabe.

Der verbindliche Soll-Umfang steht im [Meilenstein-Plan Release 1.0](Glide_Meilenstein_v1_Plan.md); der aktuelle Masterprompt-Rest und die README-Nachpflege stehen im Entwicklungsplan [§21.118](Glide_Entwicklungsplan.md#21118-masterprompt-github-internationalisierung-und-verbleibender-soll-ist-umfang-18112026), [§21.119](Glide_Entwicklungsplan.md#21119-github-projektseite-deen-und-windows-prüftakt-18112026) und den i18n-Nachweisen [§21.122](Glide_Entwicklungsplan.md#21122-deen-lokalisierung-des-seiteneditors-aktionsfeedbacks-und-shell-modifier-19112026)–[§21.123](Glide_Entwicklungsplan.md#21123-deen-lokalisierung-des-aufgabeninspektors-und-seiner-kalenderfelder-19112026). Die nachfolgende technische Beschreibung ist Zielumfang, keine Behauptung, dass alle Punkte bereits umgesetzt oder veröffentlicht sind.

```mermaid
flowchart TD
    subgraph MEILENSTEIN ["Meilenstein Version 1.0 (v1.0.0)"]
        E1["Etappe 1: Skill komplettieren (K4 & K5)<br/><b>✅ ERLEDIGT (PR #130, V1.39)</b>"]
        E2["Etappe 2: Mehrsprachigkeit i18n DE/EN<br/><b>✅ ERLEDIGT</b>"]
        E3["Etappe 3: Paketbau, Installer & Paketmanager<br/><b>◐ VORBEREITET, NICHT EINGEREICHT</b>"]
        E4["Etappe 4: Release Cut v1.0.0 & Veröffentlichung<br/><b>◐ QUELLCUT GEMERGT, RELEASE OFFEN</b>"]
        E1 --> E2 --> E3 --> E4
    end

    subgraph POST ["Post-1.0 Arbeiten (Version 1.1+)"]
        P3["CalDAV & zusätzliche Sprachen"]
    end

    E4 -.->|Nach Release 1.0| POST
```

---

### Status der Etappen bis Release 1.0

- **Etappe 1 (Skill K4 & K5):** Vollständige Dateianhang-Unterstützung im ZIP-Container, Bildauflösung, Export-Aktion, Manifest-Hashprüfung.
- **Etappe 2 (Mehrsprachigkeit i18n DE/EN) – erledigt:** Gesamte Oberfläche, Handbuch, Austauschformat, Startseite, Vorlagen, Showcase und Schnellerfassung sind zweisprachig.
- **Etappe 3 (Paketbau & Installer) – technische Vorbereitung erledigt:** Bauwege, Windows-Installer und Homebrew-/winget-Manifeste sind vorbereitet; externe Einreichung und Installationsprüfung fehlen.
- **Etappe 4 (Release Cut v1.0.0) – teilweise:** Quellstand 1.0.0 und Pflichtchecks von PR #138 sind in `main`; Tag, GitHub-Release, menschliche Abnahme sowie öffentliche Paketmanager-Einreichung fehlen.

---

### Lokalisierung (Etappe 2) – umgesetzt

#### Motivation & Ziel
Für die vorgesehene Verteilung über Homebrew und winget verlangt der Meilenstein vollständige Zweisprachigkeit (**Englisch und Deutsch**). Die Spracheinstellung existiert, aber der Integrationsstand deckt die Oberfläche nicht vollständig ab. Die folgenden Bereiche beschreiben den Soll-Umfang; die noch fehlende Arbeit ist im Entwicklungsplan nachgeführt.

#### Architektur & Moduldesign M100 (`src/glide/i18n.py`)
1. **Modulstatus:** Neues Modul M100 im [Glide-System](../01_Repository/Glide/src/glide/README.md), abgelegt unter `01_Repository/Glide/src/glide/i18n.py`.
2. **Technologische Randbedingungen:**
   - **Ausschließlich Python-Standardbibliothek** (`json`, `locale`, `os`, `pathlib`, `typing`). Keine externen Abhängigkeiten!
   - **Modulbudget (WA-50 / T322):** Jede Funktion/Methode höchstens 50 Zeilen Code, maximale Verschachtelungstiefe <= 15.
   - **Thread-sicher:** Sichere globale Zustandsspeicherung der aktiven Sprache.
3. **Katalogstruktur:**
   - JSON-basierte Übersetzungskataloge unter `01_Repository/Glide/src/glide/resources/locales/`:
     - `de.json` (deutsche Begriffe, Referenz- und Standardsprache)
     - `en.json` (englische Übersetzungen)
   - Flache oder hierarchische Punktschreibweise: `t("menu.file", "Datei")`, `t("sidebar.tasks", "Aufgaben")`, `t("dialog.settings.title", "Einstellungen")`.
4. **Kernfunktionen der Schnittstelle:**
   - `t(key: str, default: str | None = None, **kwargs) -> str`: Liefert die Übersetzung für `key`. Fehlt die Übersetzung, wird `default` zurückgegeben (oder der Schlüssel selbst, falls `default is None`). Platzhalter via Python-Formatierung (`t("status.saved_items", count=5)` -> `"5 Elemente gespeichert"`).
   - `set_locale(locale_code: str) -> None`: Setzt die aktive Sprache (`"de"`, `"en"` oder `"system"`).
   - `get_locale() -> str`: Liefert das aktuelle Sprachkürzel (`"de"` oder `"en"`).
   - `detect_system_locale() -> str`: Erkennt die Sprache des Betriebssystems über `locale.getlocale()` bzw. `locale.getdefaultlocale()`. Beginnt der Code mit `"de"`, wird `"de"` gewählt, sonst standardmäßig `"en"`.
5. **Persistenz in Einstellungen:**
   - `settings.json`: Neues Feld `"language": "system"` (Standard: `"system"`, Alternativen: `"de"`, `"en"`).
   - `settings_dialog.py`: Neues Dropdown-Feld *Sprache / Language* mit den Optionen:
     - `System (Automatisch)` / `System (Auto)`
     - `Deutsch`
     - `English`
   - Hinweis bei Sprachwechsel: Dynamische UI-Aktualisierung oder sauberer Hinweis „Sprachänderung wird nach Neustart vollständig wirksam“.
6. **Zu lokalisierende Oberflächenbereiche:**
   - **Menüleiste (`desktop_adapter.py`):** Menütitel (*Datei/File, Bearbeiten/Edit, Ansicht/View, Datenaustausch/Exchange, Hilfe/Help*), alle Menüeinträge und Tastenkürzeltexte.
   - **Seitenleiste:** Systemordner (*Eingang/Inbox, Heute/Today, Erledigt/Completed, Papierkorb/Trash*), Navigationsbereiche (*Aufgaben/Tasks, Listen/Lists, Ordner/Folders, Pinnwand/Pinboard, Zeichnen/Drawing, Notizen/Notes*).
   - **Dialoge:** Einstellungen, Suchdialog, Entlastungsbilanz, Tagesschau, Datenaustausch (Import/Export), Bestätigungsdialoge (*Löschen, Abbrechen, Speichern*).
   - **Status- & Feedbackmeldungen:** Speicherhinweise, Undo-Toasts, Fehleranzeigen.
7. **Qualitätssicherung & Tests:**
   - Neuer Test **T329** `tests/unit/test_i18n.py`:
     - Prüft Schlüsselparität: Jeder Schlüssel in `de.json` muss auch in `en.json` existieren (keine Lücken).
     - Platzhalterkonsistenz: Platzhalter (`{count}`, `{name}`) müssen in beiden Sprachen übereinstimmen.
     - Fallback-Verhalten: Unbekannte Schlüssel geben `default` oder `key` zurück (nie Abbruch).
     - Umschaltung und Locale-Erkennung isoliert getestet.
   - Systemregister: **V1.47 auf `main`** (M100, T329, 329 Test-/Werkzeugdateien); der nachgelagerte Undo-/Redo-Testfix `0a61a08f` ist noch nicht in `main`. Differenz und Prüfstatus in Plan §21.127 und QA-Bericht dokumentiert.

---

### Schritt 2: Etappe 3 – Paketbau, Installer & Paketmanager-Vorbereitung [TECHNISCH VORBEREITET; NICHT VERÖFFENTLICHT]

#### 1. macOS (Homebrew Cask)
- **Paket:** `.dmg` und `.tar.gz` werden über `.github/workflows/macos-paket.yml` gebaut (arm64 Apple Silicon).
- **Homebrew Cask:** `packaging/homebrew/Casks/glide.rb` im Repository `n05a-design/homebrew-glide`:
  ```ruby
  cask "glide" do
    version "1.0.0"
    sha256 "<macos-arm64-dmg-sha256>"
    url "https://github.com/n05a-design/glide-to-do/releases/download/v#{version}/Glide-#{version}-macos-arm64.dmg"
    name "Glide"
    desc "Local-first task, project and visual organization tool"
    homepage "https://github.com/n05a-design/glide-to-do"
    app "Glide.app"
    zap trash: "~/Library/Application Support/Glide"
  end
  ```

#### 2. Windows (Inno Setup & winget)
- **Installer-Skript:** `packaging/windows/glide_setup.iss` für Inno Setup:
  - Unprivilegierte Installation nach `%LOCALAPPDATA%\Programs\Glide` (`PrivilegesRequired=lowest`).
  - Startmenü-Verknüpfung mit sauber gesetzter `AppUserModelID: Shaye.Glide`.
  - Saubere Deinstallation ohne Rückstände.
- **CI-Integration:** In `.github/workflows/windows-paket.yml` Inno Setup (`iscc`) ausführen und `Glide-<version>-windows-x64-setup.exe` erzeugen.
- **winget Manifeste:** `packaging/winget/manifests/s/Shaye/Glide/1.0.2/` für `winget install Shaye.Glide`.

---

### Schritt 3: Etappe 4 – Release Cut, GitHub-Release & Veröffentlichung [QUELLCUT GEMERGT; ÖFFENTLICHE VERÖFFENTLICHUNG OFFEN]

1. **Versionswechsel:** Der Quellstand wurde am 17.11.2026 auf `1.0.0` angehoben und PR #138 am 18.11.2026 nach `main` gemergt.
2. **Release-Artefakte:**
   - `Glide-1.0.0-macos-arm64.dmg` + `.sha256`
   - `Glide-1.0.0-windows-x64-setup.exe` + `.sha256`
   - `Glide-1.0.0-windows-x64.zip` + `.sha256`
   - `glide-to-do-skill-v1.0.0.zip` + `.sha256`
3. **Veröffentlichung:** Noch offen: Release-Draft auf GitHub veröffentlichen, winget PR einreichen (`wingetcreate`), Homebrew-Tap aktivieren. Vorher verbleibende Lokalisierungs- und Abnahmegates abschließen; Kontofreigaben liegen beim Inhaber.

#### Nachprüfung des 906-Zeilen-Masterprompts (19.11.2026)

PR #144 hat drei eng begrenzte Dokumentationspakete umgesetzt. Der gesamte Masterprompt ist nicht vollständig umgesetzt. Verbleibender Soll-Ist-Umfang:

**Nachpflege 19.11.2026:** PR #146 hat die gekürzte deutsche Startseite und die vollständige englische `README.en.md` gemergt; PR #147 hat T299 zur README-Regressionsprüfung gemergt; PR #148 hat die DE/EN-Lokalisierung des Einstellungsdialogs gemergt. Die lokalen i18n-Kandidaten §§21.122–§21.124 erweitern Seiteneditor, Aktionsfeedback, Shell-Modifier, Aufgabeninspektor, Kalenderfelder und Editorstatus; sie sind lokal geprüft, aber nicht Teil von `main`. Wiki-Quellen, weitere App-/Shell-i18n und Governance-Automatisierung bleiben offen. Siehe Plan §§21.119–21.124 und den aktuellen [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md).

- Die öffentliche README-Navigation ist mit PR #146 zweisprachig; öffentliche Wiki-Quellen fehlen (nicht ausgewählt, I11 B).
- Weitere Issue-Formulare, Projektansichten, Discussion-Richtlinien und belastbare Governance-Automatisierung fehlen.
- ~~Die App ist nur teilweise zweisprachig~~ – mit V1.70–V1.81 erledigt.
- ~~Die Shell besitzt kein Host-/Locale-Übersetzungskonzept~~ – die Shell übernimmt Texte vom Host (Shell-Anleitung, D96–D98).
- Funding ist nicht eingerichtet. Keine externe Sponsoring- oder Zahlungsfreigabe ist erfolgt.
- Tag, GitHub-Release, externe Homebrew-/winget-Einreichung und saubere öffentliche Installationsprüfungen fehlen.
- Menschliche Sicht-/Bedien- und Accessibility-Abnahmen bleiben offen.

Die vollständige Matrix und die Priorisierung stehen in Entwicklungsplan §21.118 und QA-Bericht „Masterprompt-Nachprüfung und verbleibender Umfang“. Diese Punkte sind nicht durch den grünen CI-Lauf oder PR #144 als erledigt anzusehen.

---

### Schritt 4: Post-1.0 Arbeiten (Zurückgestellt bis Version 1.1+)

Folgende Themen sind bewusst bis nach Release 1.0 zurückgestellt, um den Fokus nicht zu verlieren:
1. **Zusätzliche Sprachen:** Französisch, Spanisch, etc.
2. **CalDAV & Cloud-Optionen:** Kalender-Synchronisation.

---

## 4. Verbindliche Arbeitsregeln und Schutzplanken für KI-Agenten

Jeder KI-Agent, der an diesem Projekt arbeitet, hat folgende verbindliche Regeln ausnahmslos zu befolgen:

### 4.1 Sprache & Kommunikation
- **Ausschließlich Deutsch:** Alle Ausgaben, Dokumentationstexte, Git-Commit-Nachrichten, PR-Titel und PR-Beschreibungen werden in deutscher Sprache verfasst.

### 4.2 Git- und Zweig-Workflow
- **Niemals Direkt-Push auf `main`:** `main` ist geschützt. Alle Änderungen entstehen auf Topic-Branches nach dem Muster `claude/<thema>` (z. B. `claude/i18n-mehrsprachigkeit-wa61`).
- **Pull Requests:** Für jeden Schnitt wird ein Pull Request auf GitHub eröffnet. Der Merge nach `main` erfolgt per Squash-Merge erst nach erfolgreicher CI-Prüfung.
- **Atomare, saubere Schnitte:** Jeder Schnitt hat eine klare Aufgabe, eigene Tests, aktualisierte Dokumente und einen sauberen Versionswechsel.

### 4.3 Strenger Schutz untrackter und lokaler Dateien (Safeguard)
- Folgende Ordner und Dateien existieren im Arbeitsverzeichnis, sind lokal geschützt und dürfen **NIEMALS** gestaget, committet oder verändert werden:
  - `20_Grafik_Master/09_Inspiration/`
  - `GLIDE_STEPS_GESAMTAUDIT_V2_2026-11-10/`
  - `glide_master_audit_bericht.md`
  - `01_Repository/Glide/packaging/paket/lizenzen/macos/SQLite-Copyright.md`
- Vor jedem `git add` ist der Status mit `git status` zu prüfen. Niemals blind `git add .` oder `git add -A` ausführen!

### 4.4 Shell-Architekturregeln (D86 / T319)
- Shell-Module (`modal_session.py`, `window_lifetime.py`, `custom_controls.py`, `desktop_adapter.py`) dürfen **ausschließlich die Python-Standardbibliothek und `tkinter` importieren**.
- Sie dürfen **keine** Glide-Fachmodule (`glide.*`, `app.pyw`, `runtime_config`, `brand`, etc.) importieren.
- **Verbotene Bezeichner:** Keine Variablen/Funktionen, die mit `("glide_", "APP_", "ERROR_LOG", "THEMES", "theme")` beginnen.

### 4.5 Modulbudget (WA-50 / T322)
- Für neue und modularisierte Dateien gilt:
  - Jede Funktion / Methode: **höchstens 50 Zeilen Code**.
  - Maximale Verschachtelungstiefe: **höchstens 15**.
  - 0 Tk-Imports in reiner Fachlogik.
- Wird automatisch über `test_modulbudget.py` (T322) und `analyse_statisch.py` geprüft.

### 4.6 Mac-Vertragsprüfpflicht (D90)
- Vor dem Eröffnen eines Pull Requests lokal auf dem Referenz-Mac (macOS arm64) mindestens folgende Tests ausführen (mit isoliertem Temp-Ordner):
  ```bash
  python3 -B 01_Repository/Glide/tests/tools/test_glide_system.py
  python3 -B 01_Repository/Glide/tests/tools/test_agenten_skill.py
  python3 -B 01_Repository/Glide/tests/tools/test_ki_ausgabe.py
  python3 -B 01_Repository/Glide/tests/integration/test_austausch_k4.py
  python3 -B 01_Repository/Glide/tests/integration/test_austausch_k3.py
  python3 -B 01_Repository/Glide/tests/tools/standpruefung.py
  python3 -B 01_Repository/Glide/scripts/pflege/abgleich_07.py
  ```

### 4.7 Test-Isolierung und Datenschutz
- **Datenisolierung:** Automatisierte und manuelle Tests dürfen niemals den echten Nutzer-Datenordner berühren. Vor jedem Start oder Import ist die Umgebungsvariable `GLIDE_DATA_DIR` auf ein temporäres Verzeichnis (z. B. über `tempfile.mkdtemp()`) zu setzen, **bevor** irgendein Modul importiert wird!
- **Datenschutz:** Keine versionierten Dateien dürfen echte Benutzernamen oder benutzerspezifische Pfade (`/Users/<Name>/`, `C:\Users\<Name>`, `/home/<Name>/`) enthalten. Nur erlaubte Platzhalter verwenden.

### 4.8 Versions- und Dokumentenpflege
- Bei jedem Versionswechsel müssen folgende Werkzeuge aus `01_Repository/Glide` ausgeführt werden:
  1. `python3 scripts/pflege/versionswechsel.py <neue_version> <datum>`
  2. `python3 scripts/pflege/abgleich_07.py` (synchronisiert `07_Python-Versionen` bytegleich mit `src/glide`).
  3. `CHANGELOG.md` mit neuem Versionsabschnitt und Datum ergänzen.
  4. `01_Repository/Glide/src/glide/README.md` (Systembestand Mxxx/Txxx) aktualisieren.
  5. `standpruefung.py` und `ci_grundstufe.py` zur Validierung durchlaufen lassen.
