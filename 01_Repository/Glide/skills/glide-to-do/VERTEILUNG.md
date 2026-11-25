# Verteilung und Einbindung des KI-Skills `glide-to-do`

Stand: 24.11.2026 · Skill-Version 1.4 · Glide 1.0.3 · Austauschformat 2

Der Skill `glide-to-do` befähigt Sprachmodelle und KI-Agenten, strukturierte Ergebnisse direkt im nativen Glide-Austauschformat (`.glideexchange`, ZIP-Pakete oder Markdown-Seiten `.md`) bereitzustellen. Der Nutzer kann diese Dateien mit einem Klick in Glide importieren.

---

## 1. Export direkt aus der Glide-App

Glide bringt den Skill bereits fertig gebündelt mit. Nutzer können das vollständige Skill-Paket direkt aus der laufenden App exportieren:

1. Glide öffnen.
2. Im Menü: **Datei › Datenaustausch › „KI-Skill exportieren …“** wählen.
3. Den gewünschten Speicherort auswählen (erzeugt `glide-to-do-skill-v1.4.zip`).
4. Das Archiv entpacken oder direkt im gewünschten KI-Werkzeug einbinden.

---

## 2. Einbindung nach Umgebung

### A. Claude Desktop

In Claude Desktop kann der Skill als System-Instruktion oder über das MCP-Dateisystem bereitgestellt werden:

1. **Als Prompt / Anweisung in Projekten:**
   Kopiere den Inhalt von `SKILL.md` in die Projektanweisungen (Custom Instructions) deines Claude-Projekts.

2. **Über Dateisystem-MCP (Claude Desktop Config):**
   Füge den Pfad zum entpackten Skill-Ordner in deine Konfigurationsdatei ein:
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

   ```json
   {
     "mcpServers": {
       "filesystem": {
         "command": "npx",
         "args": [
           "-y",
           "@modelcontextprotocol/server-filesystem",
           "/Pfad/zu/deinem/Projektordner",
           "/Pfad/zu/skills/glide-to-do"
         ]
       }
     }
   }
   ```

---

### B. Cursor

Für die Arbeit in Cursor kann der Skill projektweit oder global hinterlegt werden:

1. **Projektweit (`.cursorrules`):**
   Lege eine Datei `.cursorrules` im Hauptverzeichnis deines Projekts an und verweise auf den Skill:
   ```markdown
   Wenn Aufgaben, Pläne oder Recherchen für Glide erstellt werden sollen:
   Befolge strikt die Regeln in `skills/glide-to-do/SKILL.md`.
   Erzeuge `.glideexchange`-Dateien oder Markdown-Seiten mit höchstens 40 Zeichen pro Titel.
   Nutze `python3 skills/glide-to-do/scripts/glide_datei.py pruefen <datei>` zur Validierung.
   ```

2. **Als Cursor-Agent-Skill:**
   Kopiere den Ordner `glide-to-do` in dein `.cursor/skills/`-Verzeichnis oder dein aktives Arbeitsverzeichnis.

---

### C. Gemini CLI & Google Antigravity

In Antigravity und kompatiblen Agenten-Runtimes wird der Skill direkt als Antigravity-Skill erkannt:

1. Kopiere den Ordner `glide-to-do` in das Verzeichnis:
   - Global: `~/.gemini/antigravity/skills/glide-to-do/`
   - Im Workspace: `.gemini/skills/glide-to-do/`
2. Der Skill wird bei Erwähnung von „Glide“, Aufgabenlisten oder Projekten automatisch geladen.

---

### D. ChatGPT, Custom GPTs & Web-Assistenten

Für Assistenten ohne direkten Dateizugriff:

1. **Custom GPT / System-Prompt:**
   Füge die Abschnitte 1 und 2 aus `SKILL.md` in die Instruktionen deines Custom GPTs ein.
   Lade `references/austauschformat.md` als Wissensdatei (Knowledge File) hoch.

2. **Im Chat-Prompt:**
   Gib der KI die Anweisung:
   ```text
   Erstelle das Ergebnis als Glide-Austauschdatei (.glideexchange).
   Antworte ausschließlich mit einem validen JSON-Objekt (mode: "create", format: "glide.exchange", format_version: 2).
   Titel dürfen maximal 40 Zeichen lang sein; Details gehören in description.
   ```

---

## 3. Unterstützte Ausgabeformate

| Format | Endung | Verwendung |
|---|---|---|
| Reine Austauschdatei | `.glideexchange` / `.json` | Aufgaben, Listen, Notizen, Pixelzeichnungen |
| Austauschpaket mit Anhängen | `.glideexchange` / `.zip` | Listen oder Aufgaben mit Bildern, Dokumenten oder Galerieinhalten |
| Formatierte Seite | `.md` | Berichte, Protokolle und Dokumente mit Checkbox-Aufgaben |
| Änderungsvorschlag | `.glideexchange` (patch) | Antwort auf ein Glide-Kontextpaket (`.glidecontext`) |

---

## 4. Validierung vor der Übergabe

Jede erzeugte Datei kann lokal mit dem mitgelieferten Prüfskript getestet werden:

```bash
python3 scripts/glide_datei.py pruefen mein-ergebnis.glideexchange
```

Exitcode `0` garantiert, dass Glide die Datei fehlerfrei einliest und übernimmt.
