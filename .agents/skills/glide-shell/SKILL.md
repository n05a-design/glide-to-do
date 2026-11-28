---
name: glide-shell
description: Arbeit an der Glide Shell (Unterpaket src/glide/glide_shell) oder ihre Nutzung in einem Folgeprojekt. Verwenden bei Änderungen an modal_session, window_lifetime, custom_controls, desktop_adapter, motion, window_geometry, system_appearance, redo_history, text_fit, action_picker, runtime_paths, command_history, app_host, color_roles, settings_registry, controls, workspaces, selftest oder demo, bei der Nutzung der Shell in einem neuen Projekt, beim Herauslösen weiterer Bausteine aus Glide, bei SHELL_VERSION, dem Übernahmewerkzeug shell_uebernehmen.py, dem Framework-Checkpoint framework_checkpoint.py, der Aktualisierung einer vorhandenen Kopie, dem Selbsttest oder den Shell-Tests T319, T330–T334, T336–T338, T375, T376, dem Referenzhost oder dem portablen Designvertrag.
---

# Glide Shell

Dieser Skill ist nur der Einstieg. Inhalt und Regeln stehen an ihren Quellen:

1. **Arbeitshandbuch:** `01_Repository/Glide/docs/GLIDE_SHELL_KI_HANDBUCH.md` – Bausteine, Host-Verträge, erzwungene Regeln, Tests, Prüfwege, Versionierung, Übernahme, Git-Ablauf und Prüfliste für neue Bausteine.
2. **Grenzen und Entscheidungen:** `01_Repository/Glide/docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md` §6–§7 und D86, D94–D99 in `01_Repository/Glide/docs/ARBEITSRICHTUNG.md`. Ein neuer Baustein braucht eine Inhaberfreigabe.
3. **Schnittstellenvertrag:** `SHELL_MODULE` in `01_Repository/Glide/tests/unit/test_shell_importregel.py` (T319). Signaturänderungen dort im selben Commit.
4. **Nutzung für Folgeprojekte:** `01_Repository/Glide/src/glide/glide_shell/README.de.md` (führend) und `README.md` (englische Fassung); für KI-Agenten, die ein neues Projekt bauen, `KI_ANLEITUNG_NEUE_PROJEKTE.md` (führend) und `AI_GUIDE_NEW_PROJECTS.md` im selben Ordner; den Startprompt für neue Sitzungen `STARTPROMPT_KI.md`.
5. **Schnelle Prüfung:** in `01_Repository/Glide` mit isoliertem `GLIDE_DATA_DIR` T319, T332, T334, T336, T331, `test_shell_selbsttest.py`, `test_shell_demohost.py` und `test_shell_referenzhost.py` (T337); danach die CI-Grundstufe.
6. **Gestaltung:** `01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md`, Abschnitt „Portabler Designvertrag für Folgeprojekte“ (Regel-IDs, Geltung, Prüfkriterien).
7. **Shell-First (D106):** `01_Repository/Glide/src/glide/glide_shell/DESIGN_RICHTLINIEN.md` §5 – Abhängigkeiten, Entscheidungsreihenfolge, Individualisierung, Ausnahmen. Bestehende Anwendungen: `KI_MIGRATION_BESTEHENDE_ANWENDUNG.md` im Paket. Durchsetzung: `python -m glide_shell.conformance src/glide` (T353), Versionsprüfung `compat.require_shell`, Galerie-Register `showcase` (jede neue Komponente braucht einen Eintrag; T354/T355).

Arbeitsregeln und Produktgrenzen bleiben in `01_Repository/Glide/AGENTS.md`, `AGENTS.md` (Wurzel) und `CLAUDE.md`. Dieser Skill liegt wortgleich unter `.claude/skills/glide-shell/` (Claude Code, Copilot) und `.agents/skills/glide-shell/` (Antigravity, Codex, Gemini); T338 prüft die Gleichheit. Nicht verwechseln mit dem Produkt-Skill `01_Repository/Glide/skills/glide-to-do` (Glide-Importdateien).

Seit Shell 0.10.0 (E02): Farbrollen und Theme-Provider (`color_roles`), Einstellungsregister (`settings_registry`), allgemeine Bedienelemente (`controls`: `ShellButton`, `SearchField`, `Tooltip`, `Toolbar`) und Arbeitsbereiche (`workspaces`). Eine vorhandene Kopie wird nach [AKTUALISIERUNG.md](../../../01_Repository/Glide/src/glide/glide_shell/AKTUALISIERUNG.md) aktualisiert (Sicherung, Host-Vertrag, Rückkehr); Folgeprojekte übernehmen aus einem Checkpoint, nie aus dem laufenden Glide-Arbeitsbaum.

Aktionsgriff, Ablageanzeige und optische Glyphenzentrierung (Shell 0.9.0) nutzen den [portablen Designvertrag](../../../01_Repository/Glide/src/glide/glide_shell/DESIGN_RICHTLINIEN.md). Der Host bestimmt gültige Ziele und Datenmutationen.
