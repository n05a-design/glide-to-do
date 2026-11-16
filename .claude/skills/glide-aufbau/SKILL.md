---
name: glide-aufbau
description: Glides Aufbau und Datenmodell verstehen und den Agenten-Skill glide-to-do mitpflegen. Verwenden bei Arbeit an Datenformat, Datenfeldern, Listen-, Ordner- oder Punktarten, Austauschformat (.glideexchange, .glidecontext), Import und Export, Seitenimport aus Markdown, Zeichenformat oder am Skill glide-to-do selbst, und wenn geprüft werden soll, ob eine KI-Ausgabe in Glide richtig dargestellt wird.
---

# Glide-Aufbau und Agenten-Skill

Dieser Skill ist nur der Einstieg für die Entwicklung. Inhalt und Regeln stehen an ihren Quellen:

1. **Glide verstehen:** `01_Repository/Glide/skills/glide-to-do/references/glide-aufbau.md` – Bereiche, Objekte, Felder, Speicherweg, Importwege. Der Produkt-Skill `glide-to-do` daneben (`SKILL.md`, `references/`) beschreibt, wie Agenten Glide-Dateien anlegen.
2. **Datenvertrag:** `01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md` (Formatstufen, Austauschformat, Ausbaurahmen für Agenten-Skills); Verhalten in `docs/20_FUNKTIONEN.md`; Module in `src/glide/README.md`.
3. **Kopplung:** `skills/glide-to-do/abdeckung.json` ordnet jedes Datenfeld ein. Wer das Datenformat, ein Feld, eine Art oder den Austauschweg ändert, zieht im selben Schnitt `abdeckung.json`, Hilfsskript, Referenzen und Beispiele nach; `tests/tools/test_agenten_skill.py` schlägt sonst fehl. Pflegeregel in der Pflegematrix (`docs/DOKUMENTENPFLEGE.md`).
4. **Darstellung prüfen:** `python3 -B tests/tools/ki_ausgabe.py DATEI [--oberflaeche]` legt eine KI-Ausgabe mit dem echten Glide-Code an und vergleicht Feld für Feld, mit `--oberflaeche` in einer echten Glide-Instanz mit Neustart und abgelesener Anzeige. Die Vollprüfung führt `tests/integration/test_ki_ausgabe_darstellung.py` aus.

Arbeitsregeln, Entscheidungen und Produktgrenzen bleiben in `01_Repository/Glide/AGENTS.md` und `docs/ARBEITSRICHTUNG.md`; der Produkt-Skill wird nicht um Entwicklungsregeln ergänzt.
