---
name: glide-shell
description: Arbeit an der Glide Shell (Unterpaket src/glide/glide_shell) oder ihre Nutzung in einem Folgeprojekt. Verwenden bei Änderungen an modal_session, window_lifetime, custom_controls, desktop_adapter, motion, window_geometry, system_appearance, redo_history, text_fit, action_picker, runtime_paths, selftest oder demo, beim Herauslösen weiterer Bausteine aus Glide, bei SHELL_VERSION, dem Übernahmewerkzeug shell_uebernehmen.py, dem Selbsttest oder den Shell-Tests T319 und T330–T334.
---

# Glide Shell

Dieser Skill ist nur der Einstieg. Inhalt und Regeln stehen an ihren Quellen:

1. **Arbeitshandbuch:** `01_Repository/Glide/docs/GLIDE_SHELL_KI_HANDBUCH.md` – Bausteine, Host-Verträge, erzwungene Regeln, Tests, Prüfwege, Versionierung, Übernahme, Git-Ablauf und Prüfliste für neue Bausteine.
2. **Grenzen und Entscheidungen:** `01_Repository/Glide/docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md` §6–§7 und D86, D94–D98 in `01_Repository/Glide/docs/ARBEITSRICHTUNG.md`. Ein neuer Baustein braucht eine Inhaberfreigabe.
3. **Schnittstellenvertrag:** `SHELL_MODULE` in `01_Repository/Glide/tests/unit/test_shell_importregel.py` (T319). Signaturänderungen dort im selben Commit.
4. **Nutzung für Folgeprojekte:** `01_Repository/Glide/src/glide/glide_shell/README.de.md` (führend) und `README.md` (englische Fassung).
5. **Schnelle Prüfung:** in `01_Repository/Glide` mit isoliertem `GLIDE_DATA_DIR` T319, T332, T334, T331, `test_shell_selbsttest.py` und `test_shell_demohost.py`; danach die CI-Grundstufe.

Arbeitsregeln und Produktgrenzen bleiben in `01_Repository/Glide/AGENTS.md` und `CLAUDE.md`.
