# Glide – Übergabe an eine neue Sitzung

Stand 19.11.2026 · Glide 1.0.0 · Aufgabenformat 26 · Glide-System V1.54 auf PR #153; PR #152 gemergt

Einstieg für die nächste Sitzung: tatsächlichen Entwicklungsstand, Dokumentenautorität, nächste Arbeit und Arbeitsregeln. Aufgaben und Rest führt der [Entwicklungsplan](Glide_Entwicklungsplan.md), den Soll-Umfang Release 1.0 der [Meilenstein-Plan](Glide_Meilenstein_v1_Plan.md) und das öffentliche Tracking [Issue #129](https://github.com/n05a-design/glide-to-do/issues/129); Prüfergebnisse stehen im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md), Entscheidungen in der [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md). **Aktueller Main-Stand:** PR #151 wurde am 19.11.2026 gemergt (Merge-Commit `98f4b816`), Systemregister V1.47. Grundstufe, CodeQL und Analyze bestanden; die Linux-Vollprüfung #44493977406 auf dem früheren PR-Head `de4571dc` scheiterte, Windows-Vollprüfung und Paketbau bestanden. PR #150s Linux-Vollprüfung #44489695633 scheiterte im deutschsprachigen Undo-/Redo-Test an einem englischen Shortcut-Erwartungswert; Windows-Vollprüfung und Paketbau dieses Laufs bestanden. Main-Lauf #44490262454 wurde wegen Workflow-Konkurrenz abgebrochen. Der Mac-Paketbau auf `7260d100` war erfolgreich, die isolierte Startprobe im Workflow [#44490262390](https://github.com/n05a-design/glide-to-do/actions/runs/44490262390) scheiterte, weil das Prüfwerkzeug einen deutschen Checklistennamen fest erwartete, während die App auf Englisch korrekt `New checklist item` meldete. PR #151 korrigiert die Paketprobe und Reader-Proben; der nachgelagerte lokale Commit `0a61a08f` korrigiert zusätzlich die sprachabhängige Undo-/Redo-Testannahme, ist aber noch nicht in `main` und wartet auf eine eigene Remote-Prüfung. Erneuter Paketstart und macOS-Vollprüfung stehen aus. PR #149s frühere Linux-Timeouts bleiben historische rote Ergebnisse. PR #144–#151 dokumentieren Fortschritt, aber nicht die vollständige Erfüllung des Masterprompts. Der ältere macOS-Volllauf des Worktrees `d894e2a` bestand mit 135/135 Schritten, ist aber kein Nachweis für V1.47. Der Quellstand 1.0.0 ist kein öffentlicher Release; am 19.11.2026 waren keine Tags oder GitHub-Releases vorhanden. PR #150 integrierte die Lokalisierungen aus §§21.122–21.124 und den Dialogumbruchfix aus §21.125. Weitere Dialoge, dynamische Undo-Texte, Status-/Fehlertexte, Governance-Prüfungen, externe Homebrew-/winget-Einreichungen und menschliche Sicht-/Bedienabnahme bleiben offen. Wiki-Quellen/Synchronisation sind nach I11 B nicht ausgewählt. Frühere Übergabestände trägt Git.

**Aktueller Folgefix:** PR #152 wurde am 19.11.2026 als Merge-Commit `7241b08b` gemergt. Der V1.53-Schnitt bestand Linux/Tk 9.1 und führte den Windows-Lauf bis `test_features315.py`; dort trat ein ereignisloser Tooltip-Callback auf. Die lokale V1.54-Korrektur macht `ListApp.add_tooltip`'s `<Motion>`-Lambda ereignisneutral und ergänzt die ereignislose direkte Aufrufprobe in `test_features315.py`. Lokal bestehen T315, T312 und `schriftstile`; Remote-Linux-, Remote-Windows-, macOS-Voll- und Paketnachweis des V1.54-Heads stehen aus. Keine Assertions/Timeouts lockern. About-Beschreibung, neue 1.0.0-Aufnahmen und GIF bleiben offen.

**Ganzheitsaudit 19.11.2026:** Der aktive OneDrive-Worktree wurde gegen Git-Historie, Worktrees, Stashes, GitHub-PRs, `main` und die Projektregeln geprüft. Der Arbeitsbaum ist vor der lokalen README-Nachführung sauber; PR #153 ist der einzige offene PR und bleibt bis zur Linux-/Windows-Matrix offen. Historische Zusatz-Worktrees (`glide_ci_recovery`, `claude/etappe4-release-v1`, ältere Mac-Nachträge) enthalten keine ungesicherten lokalen Arbeitsstände. `main` trägt 1.0.0/Format 26/Systemregister V1.53; V1.54 ist nur als noch nicht gemergter PR-Kandidat vorhanden. Die interne README ist auf den 19.11.2026-Stand nachgeführt, wird aber erst mit dem Folge-Head gebündelt gepusht.

**Git-/Remote-Handoff 19.11.2026:** Lokal: Branch `design-shaye-v1-0-0-documentation-analysis`, HEAD `f0f2c71915bb20e8a6960faac35b0356165cf83a`, Arbeitsbaum sauber. Remote-Branch: `origin/design-shaye-v1-0-0-documentation-analysis` steht auf `db3bc6ca1b02bddef94bb1b87c72f8b13170b60e`; der lokale Übergabe-Commit `f0f2c719` ist noch nicht gepusht. `origin/main` steht auf `7241b08b7c01e90621a186f33e7e71755923c561`. PR #153 ist offen, mergebar und prüft den finalen Remote-Head `db3bc6ca`; der Linux-Volllauf läuft noch. Diese zwei Stände nicht vertauschen: Remote-Prüfung gilt für `db3bc6ca`, Übergabe-/QA-Nachführung liegt lokal in `f0f2c719`.

**README-/CI-Nachführung:** Die DE/EN-Projektseite enthält nun Schnellstart, Mindestfenstergrößen, detailliertere Funktionsgruppen sowie Ablage- und Projektstrukturhinweise. T299 bestand mit 23/23, danach bestand die CI-Grundstufe auf macOS/CPython 3.14.5 nach allen Änderungen mit Exitcode 0. Hinweise: zulässige Prüfkandidat-/Lieferstandabweichung sowie `tkinterdnd2`-Herkunft ohne Onlineprüfung wegen Zertifikatsprüfung. Diese Änderungen sind noch lokal und nicht gepusht; README-Bilder 1.0.0, GIF und die deutsche About-Metadatenabweichung bleiben offen.

> [!IMPORTANT]
> **Aktueller strategischer Fokus: Soll-Ist-Abschluss Release 1.0 (v1.0.0 / D93)**
> Der Inhaber beschloss am 17.11.2026 den Feature Freeze für Glide 1.0.0. Der Quellstand wurde gemergt, aber nicht öffentlich veröffentlicht. Das Soll – vollständige DE/EN-Oberfläche und bereitgestellte GitHub-/Homebrew-/winget-Releases – ist noch nicht vollständig erfüllt.
> - **Etappe 1: Skill komplettieren (K4 & K5):** ✅ **ABGESCHLOSSEN** (PR #130, PR #133, V1.39, T328)
> - **Etappe 2: Mehrsprachigkeit (i18n DE/EN):** ◐ Spracheinstellung, Menüs, ausgewählte Seitenleistenbereiche und der Einstellungsdialog sind zweisprachig; weitere Dialoge, Werkzeugleisten, Status-/Fehlertexte und Shell bleiben teilweise deutsch.
> - **Etappe 3: Paketierung & Installer:** ◐ Bauwege, Installer und Paketmanager-Manifeste technisch vorbereitet; Homebrew-/winget-Vorlagen nicht eingereicht.
> - **Etappe 4: Release Cut v1.0.0 & Veröffentlichung:** ◐ Quellstand in `main`, Pflichtchecks auf PR #138 grün; kein Tag/Release, öffentliche Einreichung und menschliche Abnahme offen.
>
> **Erste Handgriffe einer neuen Sitzung:** (1) Den lokalen V1.54-Tooltip-Fix und T315-Gegenprobe nachvollziehen. (2) Den Fix in einem neuen Feature-PR auf GitHub liefern und Linux-/Windows-Vollmatrix auf diesem Head grün abnehmen. (3) Keine Assertions oder Timeoutgrenzen lockern. Erst danach macOS-Vollprüfung und Paketbau starten. Siehe QA-Bericht und Plan §21.138. About-Beschreibung, neue 1.0.0-Aufnahmen und GIF bleiben offen. Wiki-, Release- und Paketmanageraktionen nur nach ausdrücklicher Auswahl/Freigabe.

---

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
| **Version & Schemata** | **Glide 1.0.0** · Aufgabenformat **26** · Einstellungen **2** · Vorlagen **2** · Glide-System **V1.53 auf `main`; V1.54-Kandidat in PR #153** (100 Source-Module M001–M100, 115 Integrationssuiten, 329 Test-/Werkzeugdateien, 5 Analysen). `main` enthält PR #152 auf Merge-Commit `7241b08b`. PR #153 enthält den ereignisneutralen Tooltip-Callback und ist auf Head `03cbc197` unterwegs. Linux-Vollprüfung ist grün; Windows-Vollprüfung läuft. |
| **Meilenstein Release 1.0** | Verbindlicher Feature Freeze (D93). Etappe 1 Skill K4/K5 ist erledigt. Etappe 2 i18n ist teilweise integriert; vollständige UI-Lokalisierung fehlt. Etappe 3 ist technisch vorbereitet, aber Homebrew-/winget-Vorlagen sind nicht eingereicht. Etappe 4 Quellcut ist in `main`; Tag, GitHub-Release und menschliche Abnahme fehlen. Issue #129 bleibt offen. |
| **Agenten-Skill `glide-to-do` (1.0.0)** | **WA-61 (K1, K2, K3, K4, K5 vollständig):** Zentrierte Skill-Implementierung unter `01_Repository/Glide/skills/glide-to-do/`. Formatkopplung an Format 26 über `abdeckung.json`.<br/>- **K1:** Grundskill auf Austauschformat 2.<br/>- **K2:** Labels an Ordnern und Listen, Labelfarbe, KI-Prompt-Schärfung.<br/>- **K3 (E-K5 Option A):** Automatische dateibasierte Vorsicherung vor Import (`vor_import_*.glidebackup`), Markdown-Listen (`markdown` -> `rich_note` mit Checkbox-Aufgabenextraktion), Ordnerarten (`library`, `journal`, `standard`), Wiederholungsregeln (`repeat` tolerant EN/DE mit `kind`-Rundlauf), Erinnerungen (`reminder` relativ/fest).<br/>- **K4 (Bilder/Anhänge):** ZIP-Container (`.glideexchange`/`.zip`) mit Zip-Slip-Schutz (`inspect_exchange_archive`), physischer Import von Anhängen (`ATTACHMENTS_DIR`) mit Prüfsummen- und Namenskonfliktbereinigung (`store_attachment`), Galerie-Listen (`list_kind: "gallery"`), Seiten-Cover (`cover`), Markdown-Bildauflösung in Notizen, Paketausgabe (`write_exchange_package`), atomares Rollback bei Importfehlern.<br/>- **K5 (Verteilung):** `MANIFEST.json` mit Hashes aller 18 Skill-Dateien, `VERTEILUNG.md` für Claude Desktop, Cursor, Gemini CLI, ChatGPT/Web-LLMs, App-Menüfunktion `export_agent_skill`, Release-Workflow (`glide-to-do-skill-v$VERSION.zip`). T327 (`test_austausch_k3.py`, 6/6 OK), T328 (`test_austausch_k4.py`, 9/9 OK), T321 (18/18 OK). |
| **Shell-Pakete (3a, 3c, 4, 5)** | Vier anwendungsneutrale Shell-Bausteine flach in `src/glide`, Modulbudget WA-50 vollständig eingehalten:<br/>1. `modal_session.py` (M096, 3.62.0, T317): Entkoppelter modaler Warteweg.<br/>2. `window_lifetime.py` (M097, 3.64.0, T318/T320): Zeitgeberbesitz je Fenster/Ansicht (`after_scope`).<br/>3. `custom_controls.py` (M098, 3.67.0, T312): Thementaugliche Canvas-Bedienelemente.<br/>4. `desktop_adapter.py` (M099, 3.68.0, T326): Menüleiste, Tastaturkürzel, OS-Aktionen.<br/>Fokusrückgabe D87 (3.65.0) in modalen Dialogen aktiv. Bündelung zu `glide_shell` und Demonstrationshost (Paket 6) sind Post-1.0. |
| **Prüfstand** | Führend ist der [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md). Der final gepushte PR-#153-Head `db3bc6ca` läuft in Workflow [#44585014542](https://github.com/n05a-design/glide-to-do/actions/runs/44585014542); Grundstufe, CodeQL und der vorherige Linux-/Windows-/Paketlauf auf `03cbc197` waren grün. Der finale Linux-Lauf steht noch aus. Lokal bestehen `test_features315.py`, `test_custom_controls.py` 12/12 und `test_arbeitsmodi.py --fall schriftstile` 1/1 auf macOS/Tk 9.0.3. macOS-Voll-/Paketprüfung und menschliche Abnahme bleiben offen. |
| **Lieferstand** | `07_Python-Versionen` und `src/glide` werden außerhalb einer Produktionsrunde weiterhin getrennt geführt. Der V1.54-Kandidat ist nur in PR #153 enthalten; keine neue SHA-256-Aussage für eine freigegebene Lieferfassung. |
| **Ablage-Schutz** | Unberührt und NICHT in Git: `20_Grafik_Master/09_Inspiration/`, `GLIDE_STEPS_GESAMTAUDIT_V2_2026-11-10/`, `glide_master_audit_bericht.md` und `SQLite-Copyright.md`. Diese Pfade dürfen unter keinen Umständen gestaget oder committet werden. |

**Statuskorrektur zu den älteren Laufangaben oben:** PR #150-Workflow #44489695633 ist abgeschlossen und rot; Linux scheiterte am Accelerator-Erwartungswert, Windows-Vollprüfung und Paketbau bestanden. PR #151-Linux #44493977406 prüfte einen älteren Head und scheiterte; sein Windows-Volltest samt Paketbau bestand. PR #152-Workflow #44498011031 auf `f34fb73d` scheiterte in `schriftstile`; der spätere V1.48-Fix ist als `5631333a` gepusht. Der V1.49-Diagnose-/Dokumentationsnachlauf und die 27 Gemini-Dateien wurden mit `042a8d7` auf PR #152 gepusht; `cada01bf` aktualisierte den damaligen Ergebnisstand. Die aktuelle Diagnose und Prüfgrenzen stehen in Plan §21.129–§21.135 und im QA-Bericht.

---

## 2. Zuständige Dokumente und Autoritätsmatrix

In diesem Projekt gilt die Regel **„Ein Thema, ein führendes Dokument“**. Kein Dokument dupliziert die Autorität eines anderen.

```mermaid
flowchart TD
    AR["ARBEITSRICHTUNG.md<br/>(Verbindliche Entscheidungen D01–D93)"] --> EP["Glide_Entwicklungsplan.md<br/>(Gesamter Arbeitsvorrat & Historie)"]
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
| [`01_Repository/Glide/docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md`](../01_Repository/Glide/docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md) | **Shell-Grenzen und Entkopplungsziel** (Post-1.0 Zielbild für `glide_shell` und Demonstrationshost). |
| [`01_Repository/Glide/AGENTS.md`](../01_Repository/Glide/AGENTS.md) | **Agenten-Regeln:** Repository-spezifische Richtlinien für autonome Agenten. |

---

## 3. Nächste Arbeit und Handlungsanweisungen

Der Einstellungsdialog samt stabiler Rückspeicherung (Plan §21.121) ist in PR #148 gemergt. Die lokalen Schnitte §21.122–§21.124 lokalisieren zusätzlich Seiteneditor, Aktionsfeedback, Tastenkürzel-Modifier, Aufgabeninspektor, Kalenderfelder und statische Editorstatusmeldungen; §21.125 behebt lokal die initiale Umbruchschaukel des Einstellungsdialogs. Der gezielte Fall `schriftstile` und `test_ui_design.py` (23/23) bestanden auf macOS; CI-Grundstufe, Linux-Remote-Nachprüfung für den Fix, macOS-Voll-/Paketlauf und Lieferabgleich stehen noch aus. Als nächste App-i18n-Flächen die verbliebenen Dialoge, dynamischen Undo-Texte und Status-/Fehlermeldungen gemäß Masterprompt abgrenzen; keine vollständige Lokalisierung behaupten. Die DE/EN-GitHub-Startseite (§21.119) ist mit PR #146 gemergt; T299 sichert ihre Struktur und lokalen Datei-Links in der CI-Grundstufe ab. Wiki-Inhalte/Synchronisation sind nach I11 B nicht ausgewählt; E-P1–E-P5 sowie sonstige Funktionsvorschläge werden dadurch nicht ausgewählt. Release-, Konto- und Produktentscheidungen bleiben beim Inhaber.

**Nächster technischer Schnitt:** Workflow [#44585014542](https://github.com/n05a-design/glide-to-do/actions/runs/44585014542) auf Head `db3bc6ca` vollständig abnehmen. Nach Grün: PR #153 mergen, `main` aktualisieren und den finalen macOS-Voll-/Paketdispatch auf dem Merge-Commit starten. Nicht anfangen: Tag/Release, Signierung/Notarisierung, Homebrew-/winget-Einreichung oder externe Kontoeinstellungen ohne separate Freigabe. About-Metadaten, neue 1.0.0-Bilder und GIF bleiben offen.

Der verbindliche Soll-Umfang steht im [Meilenstein-Plan Release 1.0](Glide_Meilenstein_v1_Plan.md); der aktuelle Masterprompt-Rest und die README-Nachpflege stehen im Entwicklungsplan [§21.118](Glide_Entwicklungsplan.md#21118-masterprompt-github-internationalisierung-und-verbleibender-soll-ist-umfang-18112026), [§21.119](Glide_Entwicklungsplan.md#21119-github-projektseite-deen-und-windows-prüftakt-18112026) und den i18n-Nachweisen [§21.122](Glide_Entwicklungsplan.md#21122-deen-lokalisierung-des-seiteneditors-aktionsfeedbacks-und-shell-modifier-19112026)–[§21.123](Glide_Entwicklungsplan.md#21123-deen-lokalisierung-des-aufgabeninspektors-und-seiner-kalenderfelder-19112026). Die nachfolgende technische Beschreibung ist Zielumfang, keine Behauptung, dass alle Punkte bereits umgesetzt oder veröffentlicht sind.

```mermaid
flowchart TD
    subgraph MEILENSTEIN ["Meilenstein Version 1.0 (v1.0.0)"]
        E1["Etappe 1: Skill komplettieren (K4 & K5)<br/><b>✅ ERLEDIGT (PR #130, V1.39)</b>"]
        E2["Etappe 2: Mehrsprachigkeit i18n DE/EN<br/><b>◐ TEILWEISE</b>"]
        E3["Etappe 3: Paketbau, Installer & Paketmanager<br/><b>◐ VORBEREITET, NICHT EINGEREICHT</b>"]
        E4["Etappe 4: Release Cut v1.0.0 & Veröffentlichung<br/><b>◐ QUELLCUT GEMERGT, RELEASE OFFEN</b>"]
        E1 --> E2 --> E3 --> E4
    end

    subgraph POST ["Post-1.0 Arbeiten (Version 1.1+)"]
        P1["Shell-Paket 6 Demonstrationshost"]
        P2["glide_shell Namespace-Bündelung"]
        P3["CalDAV & zusätzliche Sprachen"]
    end

    E4 -.->|Nach Release 1.0| POST
```

---

### Status der Etappen bis Release 1.0

- **Etappe 1 (Skill K4 & K5):** Vollständige Dateianhang-Unterstützung im ZIP-Container, Bildauflösung, Export-Aktion, Manifest-Hashprüfung.
- **Etappe 2 (Mehrsprachigkeit i18n DE/EN) – teilweise:** i18n-Modul, Kataloge, Spracheinstellung sowie ausgewählte Menü- und Seitenleistenbeschriftungen sind vorhanden. Vollständige Lokalisierung aller Bereiche ist nicht erreicht.
- **Etappe 3 (Paketbau & Installer) – technische Vorbereitung erledigt:** Bauwege, Windows-Installer und Homebrew-/winget-Manifeste sind vorbereitet; externe Einreichung und Installationsprüfung fehlen.
- **Etappe 4 (Release Cut v1.0.0) – teilweise:** Quellstand 1.0.0 und Pflichtchecks von PR #138 sind in `main`; Tag, GitHub-Release, menschliche Abnahme sowie öffentliche Paketmanager-Einreichung fehlen.

---

### Offene Soll-Lokalisierung (Etappe 2)

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
- **winget Manifeste:** `packaging/winget/manifests/s/Shaye/Glide/1.0.0/` für `winget install Shaye.Glide`.

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
- Die App ist nur teilweise zweisprachig; trotz lokalisierter Einstellungen bleiben weitere Dialoge, Inspektoren, Werkzeugleisten, Status-, Fehler-, Platzhalter- und weitere feste UI-Texte teilweise deutsch.
- Die Shell besitzt kein dokumentiertes oder geprüftes Host-/Locale-Übersetzungskonzept.
- Funding ist nicht eingerichtet. Keine externe Sponsoring- oder Zahlungsfreigabe ist erfolgt.
- Tag, GitHub-Release, externe Homebrew-/winget-Einreichung und saubere öffentliche Installationsprüfungen fehlen.
- Menschliche Sicht-/Bedien- und Accessibility-Abnahmen bleiben offen.

Die vollständige Matrix und die Priorisierung stehen in Entwicklungsplan §21.118 und QA-Bericht „Masterprompt-Nachprüfung und verbleibender Umfang“. Diese Punkte sind nicht durch den grünen CI-Lauf oder PR #144 als erledigt anzusehen.

---

### Schritt 4: Post-1.0 Arbeiten (Zurückgestellt bis Version 1.1+)

Folgende Themen sind bewusst bis nach Release 1.0 zurückgestellt, um den Fokus nicht zu verlieren:
1. **Shell-Paket 6 (Demonstrationshost):** Minimaler Demo-Host zur isolierten Wiederverwendbarkeit von `glide_shell`.
2. **Namespace-Bündelung `glide_shell`:** Zusammenfassung der vier Shell-Module unter einem gemeinsamen Paket-Namespace (D86/D88).
3. **Zusätzliche Sprachen:** Französisch, Spanisch, etc.
4. **CalDAV & Cloud-Optionen:** Kalender-Synchronisation.

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
