# Vorhandene Aufgaben überarbeiten

Stand 23.11.2026 · Glide 1.0.2 · Aufgabenformat 26 · Austauschformat 2

Glide gibt dir vorhandene Aufgaben nie direkt, sondern als **Kontextpaket**: Der Nutzer wählt Datei › Datenaustausch › „Für KI bereitstellen …“ mit dem Zweck „Vorhandene Aufgaben überarbeiten lassen“ und reicht dir die `.glidecontext`-Datei weiter. Du antwortest mit einem **Änderungsvorschlag**. Glide zeigt jede Änderung Feld für Feld und übernimmt nur, was noch zum Ausgangsstand passt.

## Kontextpaket lesen

```json
{"format": "glide.context", "format_version": 2, "application_version": "3.69.0",
 "instructions": "…", "fields": ["title", "description", "importance", "due", "due_time",
 "planned_date", "estimated_minutes", "done", "labels"],
 "lists": [{"ref": "r-…", "kind": "list", "title": "…", "description": "…"}],
 "items": [{"ref": "r-…", "kind": "item", "list": "r-…", "parent": null,
            "base": "…", "fields": {"title": "…", "due": "2026-11-27", "labels": ["Extern"]}}]}
```

`instructions` kann einen Auftrag des Nutzers enthalten, etwa „Priorisierung mit Begründung vorschlagen“. `application_version` nennt die Glide-Fassung.

## Antwort

```json
{"format": "glide.exchange", "format_version": 2, "mode": "patch",
 "changes": [{"ref": "r-…", "base": "…", "set": {"due": "2026-11-25", "importance": 3}}]}
```

- `ref` und `base` **unverändert** aus dem Paket kopieren; je Aufgabe höchstens eine Änderung.
- In `set` nur Felder, die sich ändern sollen, aus diesen neun: `title` (1–40 Zeichen), `description` (bis 20.000), `importance` (0–3), `due`, `planned_date` (`JJJJ-MM-TT` oder `null`), `due_time` (`HH:MM` oder `null`), `estimated_minutes` (1–10.080 oder `null`), `done` (`true`/`false`), `labels` (Liste von Namen; neue Namen legt Glide an).
- Erledigt an einer wiederkehrenden Aufgabe lehnt Glide ab; sie rückt nur beim Abhaken in Glide vor.
- Neue Aufgaben gehören nicht in einen Änderungsvorschlag, sondern in eine eigene Datei mit `mode: "create"`.

## Was Glide daraus macht

Jede Änderung erhält einen Zustand: anwendbar, ohne Änderung, **Konflikt** (die Aufgabe wurde seit dem Paket geändert), nicht gefunden oder ungültig. Übernommen wird nur Anwendbares, nach einer automatischen Vorsicherung und als ein Rückgängig-Schritt. Konflikte werden nie überschrieben.

## Prüfen

```
python3 scripts/glide_datei.py pruefen vorschlag.glideexchange --kontext paket.glidecontext
```

Das Skript meldet Verweise, die nicht im Paket stehen, veränderte `base`-Werte und ungültige Feldwerte.
