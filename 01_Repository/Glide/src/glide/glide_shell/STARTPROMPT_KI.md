# Glide Shell – Startprompt für KI-Agenten

Stand 23.11.2026 · Glide 1.0.2 · Glide-System V1.86 · Glide Shell 0.6.2

Diese Datei gibt einer neuen KI-Sitzung in einem Schritt alles, was sie braucht, um mit der Glide Shell ein Projekt zu beginnen oder weiterzuführen. Den passenden Prompt unten unverändert in die Sitzung kopieren und die Platzhalter in `<…>` ersetzen. Die Datei liegt im Paket `glide_shell` und kommt mit jeder Übernahme ins Projekt.

## Was liegt wo

**Im Glide-Repository** (<https://github.com/n05a-design/glide-to-do>, lokal etwa `Github/glide-to-do`):

| Was | Pfad |
|---|---|
| Shell-Paket (Quelle, nur hier ändern) | `01_Repository/Glide/src/glide/glide_shell/` |
| Anleitung für KI-Agenten in neuen Projekten | `…/glide_shell/KI_ANLEITUNG_NEUE_PROJEKTE.md` (führend), `AI_GUIDE_NEW_PROJECTS.md` |
| Anleitung für Folgeprojekte (Kurzfassung) | `…/glide_shell/README.de.md` (führend), `README.md` |
| Dieser Startprompt | `…/glide_shell/STARTPROMPT_KI.md` |
| Übernahmewerkzeug | `01_Repository/Glide/scripts/pflege/shell_uebernehmen.py` |
| Handbuch für Arbeit **an** der Shell | `01_Repository/Glide/docs/GLIDE_SHELL_KI_HANDBUCH.md` |
| Grenzen, Phasen, Entscheidungen | `01_Repository/Glide/docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md`, `docs/ARBEITSRICHTUNG.md` (D86, D94–D99) |
| Schnittstellenvertrag | `01_Repository/Glide/tests/unit/test_shell_importregel.py` (`SHELL_MODULE`, T319) |
| Design-Richtlinien | `01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md` |
| Arbeitsregeln | `01_Repository/Glide/AGENTS.md`, `CLAUDE.md` (Wurzel) |
| Systemregister und Übernahmevertrag | `01_Repository/Glide/src/glide/README.md` (§9) |
| Prüfwerkzeuge als Vorlage | `01_Repository/Glide/tests/tools/` (Grundstufe, Vollprüfung, Standprüfung), `scripts/pflege/pfade_bereinigen.py` |
| Claude-Code-Skill zur Shell | `.claude/skills/glide-shell/SKILL.md` |

**Im neuen Projekt** nach der Übernahme:

| Was | Pfad |
|---|---|
| Kopie der Shell (nie von Hand ändern) | `src/<app>/glide_shell/` |
| Herkunft und Prüfsummen der Kopie | `src/<app>/glide_shell/SHELL_MANIFEST.json` |
| Anleitung, Kurzanleitung, Startprompt | `src/<app>/glide_shell/KI_ANLEITUNG_NEUE_PROJEKTE.md`, `README.de.md`, `STARTPROMPT_KI.md` |
| Selbsttest | `cd src/<app> && python3 -m glide_shell.selftest` |
| Beispiel nur aus Shell-Bausteinen | `cd src/<app> && python3 -m glide_shell.demo` |

---

## Prompt A – neues Projekt anlegen (Deutsch)

```text
Du baust eine neue Tk-Desktopanwendung „<Projektname>“ auf Basis der Glide Shell.

Quelle der Shell: das Glide-Repository unter <Pfad zu glide-to-do> (öffentlich: https://github.com/n05a-design/glide-to-do).
Zielordner des neuen Projekts: <Pfad zum neuen Projekt>.

Lies zuerst, in dieser Reihenfolge:
1. 01_Repository/Glide/src/glide/glide_shell/KI_ANLEITUNG_NEUE_PROJEKTE.md – vollständig. Sie ist dein Arbeitsvertrag:
   Aufbau von Glide, Glide-System und Shell, Projektstruktur, Gerüst, Architekturregeln, Design-Richtlinien,
   Prozesse, Prüfungen, Prüflisten und Stolperstellen.
2. 01_Repository/Glide/src/glide/glide_shell/README.de.md – Bausteine und Übernahme in Kurzform.
3. 01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md – Grundsätze P1–P6 und die verbindlichen B-Regeln.

Dann:
1. Lege die Projektstruktur aus Abschnitt 3.1 der Anleitung an (AGENTS.md, CLAUDE.md, VERSION, SYSTEM_VERSION,
   src/<app>/, tests/unit, tests/integration, tests/tools, docs/ mit Arbeitsrichtung, Entwicklungsplan, Funktionen,
   Design-Richtlinien, QA-Bericht und Pflegematrix).
2. Übernimm die Shell mit
   python3 -B <glide>/01_Repository/Glide/scripts/pflege/shell_uebernehmen.py <projekt>/src/<app>
   und prüfe sie mit `python3 -m glide_shell.selftest` (erwartet: 13/13, auch mit `python3 -O`).
3. Baue das Gerüst aus Abschnitt 3.3: Start über app_host.AppHost mit preflight, Controller-Klasse,
   Kürzel über bind_shortcuts, Schließweg über install_close, Rückgängig über command_history,
   Datenordner über runtime_paths, Texte aus de.json/en.json.
4. Halte dich an die Architekturregeln aus Abschnitt 4: Fachlogik Tk-frei mit Unit-Tests, höchstens 50 Zeilen
   je Funktion, Import ohne Seiteneffekte, Zeitgeber nur über window_lifetime, Dialoge nur über modal_session.
5. Schreibe Tests ab dem ersten Modul; nie echte Nutzerdaten, eigener Datenordner per Umgebungsvariable,
   GUI-Suiten nacheinander.
6. Führe Register (SYSTEM_VERSION), Entwicklungsplan (A/B/C/D je Schnitt), CHANGELOG und QA-Bericht mit.

Grenzen: Die Kopie von glide_shell nie ändern; fehlt etwas, eigenes Modul im Projekt oder Vorschlag in Glide.
Offene Produktentscheidungen trifft der Inhaber. Keine Force-Pushes, Tags, Releases oder Veröffentlichungen
ohne ausdrückliche Freigabe. Melde am Ende, was geprüft ist und was offen bleibt.

Mein Auftrag für dieses Projekt: <Beschreibung der Anwendung und des ersten Schnitts>
```

## Prompt B – an einem bestehenden Shell-Projekt weiterarbeiten (Deutsch)

```text
Du arbeitest im Projekt „<Projektname>“ unter <Pfad>. Es nutzt die Glide Shell als Kopie in src/<app>/glide_shell/.

Lies zuerst:
1. AGENTS.md und CLAUDE.md des Projekts (Arbeitsregeln, Abschlusskriterium).
2. src/<app>/glide_shell/KI_ANLEITUNG_NEUE_PROJEKTE.md (Architekturregeln, Design-Richtlinien, Prozesse, Prüfungen).
3. docs/ENTWICKLUNGSPLAN.md und docs/ARBEITSRICHTUNG.md des Projekts (Stand, offene Aufgaben, Entscheidungen).

Prüfe vor der Arbeit:
- `cd src/<app> && python3 -m glide_shell.selftest` (erwartet: alle Prüfungen ok).
- Ist die Kopie aktuell? python3 -B <glide>/01_Repository/Glide/scripts/pflege/shell_uebernehmen.py --pruefen src/<app>
  Bei „veraltet“ mit dem Werkzeug aktualisieren; bei „verändert“ nicht überschreiben, sondern melden.

Dann den Auftrag umsetzen, mit gezielten Tests und Grundstufe, und Register, Plan, CHANGELOG und QA-Bericht
nachführen. glide_shell nie von Hand ändern. Keine Force-Pushes, Tags oder Releases ohne Freigabe.

Auftrag: <Beschreibung>
```

---

## Prompt A – start a new project (English)

```text
You are building a new Tk desktop application "<project name>" on the Glide Shell.

Source of the shell: the Glide repository at <path to glide-to-do> (public: https://github.com/n05a-design/glide-to-do).
Target folder of the new project: <path to the new project>.

Read first, in this order:
1. 01_Repository/Glide/src/glide/glide_shell/AI_GUIDE_NEW_PROJECTS.md – completely. It is your working contract:
   how Glide, the Glide-System and the shell fit together, project layout, skeleton, architecture rules, design rules,
   processes, checks, checklists and pitfalls.
2. 01_Repository/Glide/src/glide/glide_shell/README.md – building blocks and adoption in short.
3. 01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md (German) – principles P1–P6 and the binding B rules;
   section 5 of the guide summarizes them in English.

Then:
1. Create the project layout from section 3.1 of the guide (AGENTS.md, CLAUDE.md, VERSION, SYSTEM_VERSION,
   src/<app>/, tests/unit, tests/integration, tests/tools, docs/ with decisions, plan, features,
   design rules, QA report and maintenance matrix).
2. Adopt the shell with
   python3 -B <glide>/01_Repository/Glide/scripts/pflege/shell_uebernehmen.py <project>/src/<app>
   and check it with `python3 -m glide_shell.selftest` (expected: 13/13, also with `python3 -O`).
3. Build the skeleton from section 3.3: start through app_host.AppHost with preflight, a controller class,
   shortcuts through bind_shortcuts, close path through install_close, undo through command_history,
   data folder through runtime_paths, texts from de.json/en.json.
4. Follow the architecture rules from section 4: Tk-free domain logic with unit tests, at most 50 lines
   per function, imports without side effects, timers only through window_lifetime, dialogs only through modal_session.
5. Write tests from the first module on; never real user data, own data folder via environment variable,
   GUI suites one after another.
6. Keep the register (SYSTEM_VERSION), plan (A/B/C/D per cut), CHANGELOG and QA report up to date.

Limits: never change the glide_shell copy; if something is missing, write your own module or propose it in Glide.
Open product decisions belong to the owner. No force pushes, tags, releases or publications without explicit
approval. Report at the end what is verified and what remains open.

My assignment for this project: <description of the application and the first cut>
```

## Prompt B – continue an existing shell project (English)

```text
You are working in the project "<project name>" at <path>. It uses the Glide Shell as a copy in src/<app>/glide_shell/.

Read first:
1. The project's AGENTS.md and CLAUDE.md (working rules, completion criterion).
2. src/<app>/glide_shell/AI_GUIDE_NEW_PROJECTS.md (architecture rules, design rules, processes, checks).
3. The project's docs/ENTWICKLUNGSPLAN.md and docs/ARBEITSRICHTUNG.md (state, open tasks, decisions).

Check before working:
- `cd src/<app> && python3 -m glide_shell.selftest` (expected: all checks ok).
- Is the copy current? python3 -B <glide>/01_Repository/Glide/scripts/pflege/shell_uebernehmen.py --pruefen src/<app>
  If "veraltet" (outdated), update with the tool; if "verändert" (modified), do not overwrite but report it.

Then implement the assignment with targeted tests and the base stage, and update the register, plan, CHANGELOG
and QA report. Never edit glide_shell by hand. No force pushes, tags or releases without approval.

Assignment: <description>
```
