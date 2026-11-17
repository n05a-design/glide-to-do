# Glide-Agenten-Skill `glide-to-do`

Stand 17.11.2026 · Glide 1.0.0 · Aufgabenformat 26

Skillversion `1.1` (Feld `metadata.version` in `SKILL.md`).

Mit diesem Skill legen KI-Agenten ihre Ergebnisse direkt als Dateien an, die Glide importiert: Recherchen und Berichte als Seite, Aufgaben-, Einkaufs- und Projektlisten mit Ordnern, Terminen, Aufwand und Labels, Notizen, Pixelzeichnungen und Änderungsvorschläge zu vorhandenen Aufgaben. Glide prüft jede Datei, zeigt eine Vorschau und übernimmt sie mit einem einzigen Rückgängig-Schritt. Der Skill braucht weder Netz noch Schlüssel und schreibt nie in den Glide-Datenordner.

Der Ordner folgt dem offenen Standard für Agent Skills: `SKILL.md` mit Name und Beschreibung, dazu `references/`, `scripts/`, `assets/` und die Feldübersicht `abdeckung.json`. Einstieg für den Agenten ist [SKILL.md](SKILL.md).

## Einrichten

Den Ordner `glide-to-do` vollständig und unverändert kopieren; der Ordnername muss `glide-to-do` bleiben. Den Ordner gibt es im [Glide-Repository](https://github.com/n05a-design/glide-to-do/tree/main/01_Repository/Glide/skills/glide-to-do) (über „Code › Download ZIP“ das ganze Repository laden und den Ordner herausnehmen).

**Ein Ordner für mehrere Agenten:** `.agents/skills/glide-to-do/` in einem Projektordner lesen OpenAI Codex, Google Antigravity und Gemini CLI gemeinsam; Claude Code liest `.claude/skills/`.

### Claude (Anthropic)

| Wo | So geht es |
|---|---|
| Claude Code | Für alle Projekte nach `~/.claude/skills/glide-to-do/` kopieren, für ein Projekt nach `.claude/skills/glide-to-do/`. In einer neuen Sitzung lädt Claude den Skill bei passender Anfrage; direkt aufrufen mit `/glide-to-do`. |
| Claude-Apps (Web, Desktop) | 1. Codeausführung einschalten (englische Oberfläche: Settings › Capabilities). 2. Den Ordner `glide-to-do` als ZIP packen (Windows: Rechtsklick › Senden an › ZIP-komprimierter Ordner; macOS: Rechtsklick › „glide-to-do“ komprimieren). 3. Unter Customize › Skills auf „+“, dann „Create skill“ › „Upload a skill“ und das ZIP wählen. In Team- und Enterprise-Konten gibt die Organisation Skills frei; eigene Skills sehen andere erst, wenn du sie teilst. |

### OpenAI

| Wo | So geht es |
|---|---|
| Codex (CLI, IDE-Erweiterung) | Für ein Projekt nach `.agents/skills/glide-to-do/` im Repository kopieren (Codex sucht vom Arbeitsordner bis zur Repository-Wurzel), für alle Projekte nach `~/.agents/skills/glide-to-do/`. Codex wählt den Skill bei passender Aufgabe selbst; direkt mit `$glide-to-do` oder über `/skills`. Erscheint er nicht, Codex neu starten. |
| ChatGPT | Skills stehen in der ChatGPT-Desktop-App im Bereich „Skills“ der Seitenleiste und werden mit `@` aufgerufen. Ob du einen eigenen Skill hinzufügen kannst, hängt von Tarif und Organisation ab; den genauen Weg vor Gebrauch in der OpenAI-Hilfe nachsehen. Rückfall siehe unten. |

### Google

| Wo | So geht es |
|---|---|
| Antigravity (App, CLI `agy`, IDE) | Seit 18.06.2026 Nachfolger der Gemini CLI für Privatkonten. Für ein Projekt nach `.agents/skills/glide-to-do/` im Arbeitsordner kopieren, für alle Projekte nach `~/.gemini/config/skills/glide-to-do/`; die CLI liest zusätzlich `~/.gemini/skills/`. Danach in der CLI `/skills reload`. Antigravity wählt den Skill selbst; direkt mit `/glide-to-do`. |
| Gemini CLI | Weiter nutzbar mit API-Schlüssel oder Unternehmenslizenz. Nach `.agents/skills/` oder `.gemini/skills/` im Projekt beziehungsweise `~/.agents/skills/` oder `~/.gemini/skills/` kopieren, oder `gemini skills install <Pfad zum Ordner>`. Vor der ersten Nutzung fragt Gemini CLI um Zustimmung; `/skills list` zeigt den Skill. |
| Gemini-App (Web, Mobil) | Ein Weg für Agent Skills ist nicht belegt. Rückfall siehe unten. |

### Weitere Agenten und Chats ohne Skills

- GitHub Copilot und Cursor lesen laut Drittquellen `.github/skills/` beziehungsweise `.cursor/skills/`, teils auch `.agents/skills/`; vor Gebrauch in der Herstellerdokumentation prüfen.
- **Rückfall für jeden Chat:** den Inhalt von `SKILL.md` und der passenden Datei aus `references/` der Anfrage voranstellen, oder in Glide Datei › Datenaustausch › „Austauschformat anzeigen …“ kopieren. Die Antwort als Datei speichern (`.glideexchange` oder `.md`).

Stand der Herstellerangaben 16.11.2026; Quellen im [Marktbericht §17](https://github.com/n05a-design/glide-to-do/blob/main/00_Arbeitsvorbereitung/Glide_Markt_und_Vorbilder.md#17-agenten-skills-und-dokumentbasierter-ki-austausch-16112026).

## Importieren in Glide

- `.glideexchange`: Datei › Datenaustausch › „KI-Ergebnis importieren …“
- `.md`: Datei › Importieren › „Seite aus Datei …“; kopierter Text über „Seite aus Zwischenablage“
- Vorhandene Aufgaben überarbeiten: zuerst Datei › Datenaustausch › „Für KI bereitstellen …“ mit dem Zweck „Vorhandene Aufgaben überarbeiten lassen“, die Antwort wieder über „KI-Ergebnis importieren …“

## Prüfen, ob Glide die Ausgabe richtig zeigt

- Im Agenten oder von Hand, ohne Glide: `python3 scripts/glide_datei.py pruefen DATEI`.
- Im Glide-Repository mit dem echten Glide-Code: `python3 -B tests/tools/ki_ausgabe.py DATEI`; mit `--oberflaeche` in einer echten Glide-Instanz mit künstlichem Datenordner, gespeichert, neu gestartet und mit abgelesener Anzeige. Die Vollprüfung von Glide führt das für alle Beispiele aus.

## Grenzen dieser Fassung

Auf dem Austauschformat 2, ohne eigene Änderung an Glide. Nicht übernommen werden Wiederholungen, Erinnerungen, Farben, Pixelsymbole, Ordnerarten, Verknüpfungen, Anhänge, Vorlagen, Pinnwände und Ansichten; Labels nur an Punkten. Je Feld: [abdeckung.json](abdeckung.json). Ausbau und Reihenfolge im [Entwicklungsplan](https://github.com/n05a-design/glide-to-do/blob/main/00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#21102-glide-agenten-skill-glide-to-do-recherche-und-pflegeeinbindung-16112026), Verhalten in den [Funktionen §11](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/20_FUNKTIONEN.md#11-import-ausgabe-und-austausch).

## Pflege

Glide ist die einzige Quelle; der Skill ist an Glides Datenformat gekoppelt. `tests/tools/test_agenten_skill.py` vergleicht `abdeckung.json`, die Regeln des Hilfsskripts und die Referenzen mit dem Glide-Code und prüft jedes Beispiel mit dem echten Import. Ändert sich das Datenformat, ein Feld, eine Art oder der Austauschweg, schlägt die Prüfung fehl, bis der Skill im selben Schnitt nachgezogen ist. Ab Paket K2 werden die Referenzen aus dem Code erzeugt ([Pflegematrix](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/DOKUMENTENPFLEGE.md#zuständigkeiten-und-änderungsbezüge)).

Lizenz: MPL-2.0 wie Glide.
