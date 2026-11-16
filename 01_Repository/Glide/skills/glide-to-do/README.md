# Glide-Agenten-Skill `glide-to-do`

Stand 16.11.2026 · Glide 3.65.0 · Aufgabenformat 26

Skillversion `1.0` (Feld `metadata.version` in `SKILL.md`).

Mit diesem Skill legen KI-Agenten ihre Ergebnisse direkt als Dateien an, die Glide importiert: Recherchen und Berichte als Seite, Aufgaben-, Einkaufs- und Projektlisten mit Ordnern, Terminen, Aufwand und Labels, Notizen, Pixelzeichnungen und Änderungsvorschläge zu vorhandenen Aufgaben. Glide prüft jede Datei, zeigt eine Vorschau und übernimmt sie mit einem einzigen Rückgängig-Schritt. Der Skill braucht weder Netz noch Schlüssel und schreibt nie in den Glide-Datenordner.

Der Ordner folgt dem offenen Standard für Agent Skills (`SKILL.md` mit Name und Beschreibung, dazu `references/`, `scripts/`, `assets/`). Einstieg für den Agenten ist [SKILL.md](SKILL.md).

## Einrichten

Den Ordner `glide-to-do` unverändert kopieren; der Ordnername muss `glide-to-do` bleiben.

| Agent | Ort | Beleg |
|---|---|---|
| Claude Code | `~/.claude/skills/glide-to-do/` für alle Projekte oder `.claude/skills/glide-to-do/` im Projekt | Hersteller |
| Claude-Apps (Web, Desktop) | Ordner als ZIP packen und unter „Skills“ hochladen; Codeausführung muss eingeschaltet sein | Hersteller |
| OpenAI Codex | `.agents/skills/glide-to-do/` im Projekt oder im Nutzerordner | Hersteller |
| ChatGPT | Skills in der Desktop-App, je nach Tarif | Hersteller |
| GitHub Copilot, Gemini CLI, Cursor | laut Drittquellen `.github/skills/`, `.gemini/skills/` bzw. `.cursor/skills/`, teils auch `.agents/skills/` | vor Gebrauch in der Herstellerdokumentation prüfen |
| Chat ohne Skills | Inhalt von `SKILL.md` und der benötigten Datei aus `references/` der Anfrage voranstellen, oder in Glide Datei › Datenaustausch › „Austauschformat anzeigen …“ kopieren | – |

Recherchestand und Quellen: [Markt und Vorbilder §17](../../../../00_Arbeitsvorbereitung/Glide_Markt_und_Vorbilder.md#17-agenten-skills-und-dokumentbasierter-ki-austausch-16112026).

## Importieren in Glide

- `.glideexchange`: Datei › Datenaustausch › „KI-Ergebnis importieren …“
- `.md`: Datei › Importieren › „Seite aus Datei …“; kopierter Text über „Seite aus Zwischenablage“
- Vorhandene Aufgaben überarbeiten: zuerst Datei › Datenaustausch › „Für KI bereitstellen …“ mit dem Zweck „Vorhandene Aufgaben überarbeiten lassen“, die Antwort wieder über „KI-Ergebnis importieren …“

## Grenzen dieser Fassung

Paket K1 des Vorhabens WA-61 auf dem vorhandenen Austauschformat 2, ohne Änderung an Glide. Nicht übernommen werden Wiederholungen, Erinnerungen, Farben, Pixelsymbole, Ordnerarten, Verknüpfungen, Anhänge, Vorlagen, Pinnwände und Ansichten; Labels nur an Punkten. Ausbau und Reihenfolge stehen im [Entwicklungsplan §21.102](../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#21102-glide-agenten-skill-glide-to-do-recherche-und-pflegeeinbindung-16112026), die Verhaltensbeschreibung in [Funktionen §11](../../docs/20_FUNKTIONEN.md#11-import-ausgabe-und-austausch).

## Pflege

Glide ist die einzige Quelle. Ändert sich der Austauschweg, gehen `scripts/glide_datei.py`, die Referenzen und die Beispiele im selben Schnitt mit. `tests/tools/test_agenten_skill.py` vergleicht die Regeln des Hilfsskripts mit dem Glide-Code und prüft jedes Beispiel mit dem echten Import. Ab Paket K2 werden die Referenzen aus dem Code erzeugt ([Pflegematrix](../../docs/DOKUMENTENPFLEGE.md#zuständigkeiten-und-änderungsbezüge)).

Lizenz: MPL-2.0 wie Glide.
