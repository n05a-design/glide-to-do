---
name: glide-bento
description: Arbeit am Glide Bento Box System (Unterpaket src/glide/glide_bento) oder seine Nutzung in Glide und Folgeprojekten. Verwenden bei Änderungen an BentoCard, BentoGrid, BentoLayoutPlanner, BentoTokens, BentoContext, BentoHeader, BentoMetric, BentoActions, BentoEmptyState, BentoDivider, beim Erstellen oder Überarbeiten von Bento-Karten, bei der Startseitenkomposition (render_home), BENTO_VERSION 0.2.0 (Bandmodell mit span=2, Host-Token-Vertrag Variante C), dem Bento-Selbsttest, der Bento-Demo, dem Referenzhost oder den Bento-Tests T341–T344 und T349 sowie dem Bento-Designvertrag.
---

# Glide Bento Box System

Dieser Skill dient als verbindlicher Einstieg für KI-Agenten bei jeder Arbeit am **Glide Bento Box System** (Ebene B, D100).

## Verbindliche Quellen

1. **Architekturkonzept:** `01_Repository/Glide/docs/GLIDE_BENTO_SYSTEM_KONZEPT.md` – Führendes Architekturkonzept, Ebenentrennung (Ebene A -> Ebene B -> Ebene C), Schichtenmodell, Unabhängigkeitsversprechen und Integrationsmuster.
2. **Designvertrag:** `01_Repository/Glide/src/glide/glide_bento/BENTO_DESIGN_CONTRACT.md` – Verbindliche visuelle und ergonomische Vorgaben für Bento-Komponenten (P1–P6, B11, B15, Maßskalen, Breakpoints 616/932 px).
3. **Dokumentation:** `01_Repository/Glide/src/glide/glide_bento/README.de.md` (deutsch, führend) und `README.md` (englisch).
4. **Entscheidungen:** D100 und D106 (Shell-First) in `01_Repository/Glide/docs/ARBEITSRICHTUNG.md`.
5. **Version und Shell:** `BENTO_VERSION` 0.3.0 verlangt `SHELL_MIN_VERSION` 0.7.0 (Prüfung beim Import über `glide_shell.compat`). Neue Komponenten bekommen einen Eintrag in `glide_bento/showcase.py` und einen Einsatzort in `src/glide/component_gallery.py`. Übernahme in Folgeprojekte nur mit `shell_uebernehmen.py --mit-bento`.

## Harte Architektur- und Importgrenzen (D100)

- **Ebenentrennung:** `glide_bento` gehört zur **Ebene B**. Es darf **keine** Module oder Fachlogik aus Ebene A (`app.pyw`, `home_tiles`, etc.) importieren. Es kennt keine Produktfarben und keine `ListApp`-Instanz. (Erzwungen durch T341 `test_bento_importregel.py`).
- **Framework Shell:** `glide_shell` (Ebene C) darf kein `glide_bento` importieren.
- **Portabilität:** `glide_bento` kann gemeinsam mit `glide_shell` vollständig isoliert in jedem Python/Tkinter-Folgeprojekt ohne Glide-Checkout betrieben werden.
- **Deterministische Planung:** Layoutberechnungen erfolgen rein mathematisch und Tk-frei über `BentoLayoutPlanner`; seit 0.2.0 im Bandmodell (`plan.bands`, `BentoBand`/`BentoLane`, `span=2` nur im Dreispaltenraster zweispaltig). Regeln: `docs/GLIDE_BENTO_SYSTEM_KONZEPT.md` §10.3a. Die Bezeichnung `col_span` gibt es nicht.
- **Tokens (Variante C):** Hosts liefern Theme und Tokens über `BentoContext.for_host(theme_provider=…, token_provider=…, button_factory=…)` und `refresh_from_host()`; Glide über `ui_design.bento_token_values()` und `ListApp.glide_bento_context`. Keine zweiten Skalen in Bento pflegen.

## Schnellprüfung

Immer mit `python3 -B` ausführen:
- **Selbsttest (16/16 Checks):** `PYTHONPATH=01_Repository/Glide/src/glide python3 -B -m glide_bento.selftest`
- **Demo-Galerie:** `PYTHONPATH=01_Repository/Glide/src/glide python3 -B -m glide_bento.demo --test`
- **Bento Unit-Tests:** `python3 -B -m unittest discover -s 01_Repository/Glide/tests/unit -p "test_bento*.py"`
- **Bento Integrationstests:** `python3 -B -m unittest 01_Repository/Glide/tests/integration/test_bento_integration.py`
- **Glide Startseite:** `python3 -B 01_Repository/Glide/tests/integration/test_startseite3332.py` und `python3 -B 01_Repository/Glide/tests/integration/test_glide_110.py`
- **Referenzhost ohne Glide (T349):** `python3 -B -m unittest 01_Repository/Glide/tests/integration/test_bento_referenzhost.py`
- Prüfkopien außerhalb OneDrive anlegen (CLAUDE.md); Werkzeugtests mit kopierten Dateien scheitern sonst am Löschen.

Dieser Skill liegt wortgleich unter `.agents/skills/glide-bento/SKILL.md` (Antigravity, Codex, Gemini) und `.claude/skills/glide-bento/SKILL.md` (Claude Code, Copilot).
