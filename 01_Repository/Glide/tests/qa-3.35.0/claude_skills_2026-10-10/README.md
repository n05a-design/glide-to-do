# Claude-Skills 3.35.0 (10.10.2026)

Stand 10.10.2026 · Glide 3.35.0 · Nachlauf ohne neue App-Version · Linux-Container, Python 3.14.6, Tk 9.0, künstliche Daten

Auftrag des Inhabers: die im Projektordner als `.md` abgelegten Claude-Skills so installieren, dass Claude sie erkennt und ihre Regeln anwendet.

## Befund

- Im lokalen Projektordner lagen, beide unversioniert, `Apple Design Skill.md` in der Wurzel und `skills-main/`, der ZIP-Download von `emilkowalski/skills` (MIT, 14 Skills). Claude Code erkennt Skills nur als `.claude/skills/<Name>/SKILL.md` im Projekt oder `~/.claude/skills/<Name>/SKILL.md` beim Benutzer; keine der beiden Ablagen wurde geladen.
- `Apple Design Skill.md` ist `skills/apple-design/SKILL.md` aus `emilkowalski/skills` (Commit `e8a175d`, 02.10.2026) ohne den Abschnitt „Initial Response“, der den Skill beim ersten Aufruf auf einen festen Begrüßungssatz beschränkt.
- Die Standprüfung erfasst auch Markdown unter `.claude/` und meldete einen Probe-Skill ohne Glide-Standzeile als R1. Derselbe Befund machte im Sprintzweig `claude/glide-sprint-2026-10-09` den Vorlauf `tests/qa-3.35.0/planung_2026-10-10` für den lokalen Arbeitsordner rot.

## Änderung

| Datei | Änderung |
|---|---|
| `.claude/skills/apple-design/SKILL.md` | Fassung des Inhabers unverändert übernommen (SHA-256 `11840b24…5e61`) |
| `.claude/skills/apple-design/LICENSE` | MIT-Lizenz, bytegleich zum Original (SHA-256 `4ff5bdb7…260b`) |
| `tests/tools/standpruefung.py` | `SKILL.md` in `OHNE_STAND`: keine Standzeile verlangt; R3, R6–R9 und R11 gelten weiter |
| `tests/tools/test_standpruefung.py` | Regressionstest: ohne Werkzeugänderung rot (R1), mit ihr grün; R3 greift weiter, andere Markdown-Dateien unter `.claude/` brauchen weiter eine Standzeile |
| `CLAUDE.md` | Abschnitt „Skills“: Ablageort, Umgang mit Fremdskills, Web-Bezug von `apple-design` |

Nicht übernommen: die übrigen 13 Skills aus `skills-main/`. Sie richten sich an Web, React, Expo oder Swift; welche davon Glide nützen, entscheidet der Inhaber.

## Prüfung

| Schritt | Ergebnis |
|---|---|
| Werkzeugtest `test_standpruefung` | 12 Tests grün; der neue Test ohne die Werkzeugänderung rot |
| Standprüfung | 55 aktive Dokumente einschließlich dieses Nachweises, `SKILL.md` als „ohne Standaussage“ gezählt, keine Befunde |
| [CI-Grundstufe](ci/ergebnis.json) | Exitcode 0; Ausgangsstand `b5f5c22` vorher ebenfalls Exitcode 0 |
| App und Lieferung | `src/glide`, `07_Python-Versionen` und Showcase gegenüber `b5f5c22` unverändert |

Prüfgrenze: Linux-Container mit künstlichen Daten. Ob Claude den Skill lädt, zeigt die nächste Claude-Code-Sitzung auf diesem Stand (`/apple-design` oder eine Aufgabe zu Bewegung, Typografie oder Materialien); im Container ist das nicht automatisch prüfbar.
