---
name: glide-bento
description: Arbeit am Glide Bento Box System (Unterpaket src/glide/glide_bento) oder seine Nutzung in Glide und Folgeprojekten. Verwenden bei Änderungen an BentoCard, BentoGrid, BentoLayoutPlanner, BentoTokens, BentoContext, BentoHeader, BentoMetric, BentoActions, BentoEmptyState, BentoDivider, beim Erstellen oder Überarbeiten von Bento-Karten, bei der Startseitenkomposition (render_home), BENTO_VERSION 0.1.0, dem Bento-Selbsttest, der Bento-Demo oder den Bento-Tests T341–T344 sowie dem Bento-Designvertrag.
---

# Glide Bento Box System

Dieser Skill dient als verbindlicher Einstieg für KI-Agenten bei jeder Arbeit am **Glide Bento Box System** (Ebene B, D100).

## Verbindliche Quellen

1. **Architekturkonzept:** `01_Repository/Glide/docs/GLIDE_BENTO_SYSTEM_KONZEPT.md` – Führendes Architekturkonzept, Ebenentrennung (Ebene A -> Ebene B -> Ebene C), Schichtenmodell, Unabhängigkeitsversprechen und Integrationsmuster.
2. **Designvertrag:** `01_Repository/Glide/src/glide/glide_bento/BENTO_DESIGN_CONTRACT.md` – Verbindliche visuelle und ergonomische Vorgaben für Bento-Komponenten (P1–P6, B11, B15, Maßskalen, Breakpoints 616/932 px).
3. **Dokumentation:** `01_Repository/Glide/src/glide/glide_bento/README.de.md` (deutsch, führend) und `README.md` (englisch).
4. **Entscheidungen:** D100 in `01_Repository/Glide/docs/ARBEITSRICHTUNG.md`.

## Harte Architektur- und Importgrenzen (D100)

- **Ebenentrennung:** `glide_bento` gehört zur **Ebene B**. Es darf **keine** Module oder Fachlogik aus Ebene A (`app.pyw`, `home_tiles`, etc.) importieren. Es kennt keine Produktfarben und keine `ListApp`-Instanz. (Erzwungen durch T341 `test_bento_importregel.py`).
- **Framework Shell:** `glide_shell` (Ebene C) darf kein `glide_bento` importieren.
- **Portabilität:** `glide_bento` kann gemeinsam mit `glide_shell` vollständig isoliert in jedem Python/Tkinter-Folgeprojekt ohne Glide-Checkout betrieben werden.
- **Deterministische Planung:** Layoutberechnungen erfolgen rein mathematisch und Tk-frei über `BentoLayoutPlanner`.

## Schnellprüfung

Immer mit `python3 -B` ausführen:
- **Selbsttest (13/13 Checks):** `PYTHONPATH=01_Repository/Glide/src/glide python3 -B -m glide_bento.selftest`
- **Demo-Galerie:** `PYTHONPATH=01_Repository/Glide/src/glide python3 -B -m glide_bento.demo --test`
- **Bento Unit-Tests:** `python3 -B -m unittest discover -s 01_Repository/Glide/tests/unit -p "test_bento*.py"`
- **Bento Integrationstests:** `python3 -B -m unittest 01_Repository/Glide/tests/integration/test_bento_integration.py`
- **Glide Startseite:** `python3 -B 01_Repository/Glide/tests/integration/test_startseite3332.py`

Dieser Skill liegt wortgleich unter `.agents/skills/glide-bento/SKILL.md` (Antigravity, Codex, Gemini) und `.claude/skills/glide-bento/SKILL.md` (Claude Code, Copilot).
