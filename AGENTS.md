# Glide – Einstieg für KI-Agenten (Repository-Wurzel)

Stand 22.11.2026 · Glide 1.0.1 · Glide-System V1.86 · Glide Shell 0.6.2

Dünner, agentenneutraler Adapter für Antigravity, Codex, GitHub Copilot, Gemini und andere Werkzeuge, die `AGENTS.md` in der Repository-Wurzel lesen. Er enthält **keine eigenen Regeln**; verbindlich sind die verlinkten Quellen. Claude Code liest zusätzlich [`CLAUDE.md`](CLAUDE.md).

## Verbindliche Quellen (gezielt lesen, nicht das ganze Repository)

1. [`01_Repository/Glide/AGENTS.md`](01_Repository/Glide/AGENTS.md) – Arbeitsregeln, Produktgrenzen, Abschlusskriterium.
2. [`00_Arbeitsvorbereitung/Glide_Uebergabe.md`](00_Arbeitsvorbereitung/Glide_Uebergabe.md) – aktueller Stand; Entscheidungen D01–D99 in [`docs/ARBEITSRICHTUNG.md`](01_Repository/Glide/docs/ARBEITSRICHTUNG.md).
3. [`docs/DOKUMENTENPFLEGE.md`](01_Repository/Glide/docs/DOKUMENTENPFLEGE.md) – führende Quelle je Thema; zusammenführen statt parallel pflegen.
4. **Gestaltung:** [`docs/DESIGN_RICHTLINIEN.md`](01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md) ist für jede neue oder angefasste Oberfläche verbindlich.

## Aufgabe → Einstieg

| Aufgabe | Einstieg |
|---|---|
| Arbeit **an** der Glide Shell (`src/glide/glide_shell`, `shell_uebernehmen.py`, T319/T330–T338) | Skill `glide-shell` (`.agents/skills/` bzw. `.claude/skills/`) → [`GLIDE_SHELL_KI_HANDBUCH.md`](01_Repository/Glide/docs/GLIDE_SHELL_KI_HANDBUCH.md) |
| Shell in einem **anderen** Projekt nutzen | [`KI_ANLEITUNG_NEUE_PROJEKTE.md`](01_Repository/Glide/src/glide/glide_shell/KI_ANLEITUNG_NEUE_PROJEKTE.md), Startprompt [`STARTPROMPT_KI.md`](01_Repository/Glide/src/glide/glide_shell/STARTPROMPT_KI.md) |
| Ergebnisse als Glide-Importdatei erzeugen | Produkt-Skill [`01_Repository/Glide/skills/glide-to-do`](01_Repository/Glide/skills/glide-to-do/SKILL.md) – **nicht** für Shell-Entwicklung |
| Daten- und Objektmodell | `.claude/skills/glide-aufbau/SKILL.md` |

## Harte Grenzen

- Die Shell bleibt frei von Glide-Fachlogik (D86, D94–D99; erzwungen durch T319). Kopierte Shell-Dateien in Folgeprojekten nie von Hand ändern.
- Nie echte Nutzerdaten: `GLIDE_DATA_DIR` vor dem Import auf einen temporären Ordner setzen, Werkzeuge mit `python3 -B`, Prüfpfade kurz und außerhalb OneDrive.
- Kein Force-Push, Merge, Tag oder Release ohne ausdrückliche Freigabe; fremde Worktrees nicht verändern.
- Übergabe am Ende einer Sitzung in die bestehende Übergabestruktur (Übergabe, Entwicklungsplan, QA-Bericht), keine parallelen Statusdateien.
