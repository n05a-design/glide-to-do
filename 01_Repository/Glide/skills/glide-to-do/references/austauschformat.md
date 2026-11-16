# Glide-Austauschformat für neue Inhalte

Stand 16.11.2026 · Glide 3.66.0 · Aufgabenformat 26 · Austauschformat 2

Eine `.glideexchange`-Datei ist ein JSON-Objekt. Sie beschreibt, was entstehen soll; Glide entscheidet, wie es gespeichert wird. Der Import legt ausschließlich neue Ordner, Listen, Labels und Punkte an. Maßgeblich ist die Prüfung in Glide; das Hilfsskript bildet sie nach.

## Wurzel

```json
{
  "format": "glide.exchange",
  "format_version": 2,
  "mode": "create",
  "generator": {"type": "ai", "name": "glide-to-do"},
  "labels": [ … ],
  "folders": [ … ],
  "lists": [ … ]
}
```

| Feld | Pflicht | Bedeutung |
|---|---|---|
| `format` | ja | immer `"glide.exchange"` |
| `format_version` | ja | `2` |
| `mode` | nein | `"create"` (Vorgabe) für Neues, `"patch"` für Änderungsvorschläge ([eigene Seite](aenderungsvorschlag.md)) |
| `generator` | nein | Herkunft, z. B. `{"type": "ai", "name": "glide-to-do"}`; Glide zeigt `type` in der Vorschau |
| `labels`, `folders` | nein | Listen von Objekten, siehe unten |
| `lists` | ja | mindestens eine Liste |
| `notes`, `created_for`, `capabilities` | nein | werden gelesen, aber nicht übernommen |

Jedes andere Feld nennt Glide als unbekannt und schlägt „Abbrechen“ vor.

## Labels

`{"key": "label-1", "name": "Extern"}` – `key` frei und eindeutig, `name` höchstens 40 Zeichen. Gibt es den Namen in Glide schon, wird das vorhandene Label verwendet. Eine Farbe (`color`) übernimmt diese Glide-Fassung nicht; sie vergibt die Farbe selbst. Insgesamt hält Glide höchstens 80 Labels, je Punkt 20.

## Ordner

`{"key": "folder-1", "title": "Büroumzug", "description": "…", "parent": "folder-0"}`

| Feld | Bedeutung |
|---|---|
| `key` | frei wählbar, eindeutig; Listen und Unterordner verweisen darauf |
| `title` | höchstens 40 Zeichen |
| `description` | Zweck des Ordners |
| `parent` | Schlüssel eines **weiter oben** in `folders` stehenden Ordners; sonst entsteht der Ordner auf oberster Ebene |

Ordnerart Buch oder Notizbuch und `labels` an Ordnern übernimmt diese Glide-Fassung noch nicht.

## Listen

`{"key": "list-1", "title": "Planung", "folder": "folder-1", "description": "…", "list_kind": "tasks", "items": [ … ]}`

| Feld | Bedeutung |
|---|---|
| `key` | frei wählbar, eindeutig |
| `title` | höchstens 40 Zeichen |
| `description` | Zweck der Liste |
| `folder` | Schlüssel eines Ordners aus `folders`; ohne Angabe liegt die Liste auf oberster Ebene |
| `list_kind` | Art der Liste, siehe unten; Vorgabe `tasks` |
| `items` | Punkte der Liste |
| `rich_note` | Text einer Notiz oder Seite |
| `drawing`, `animation` | Pixelzeichnung und Bildfolge einer Zeichnung |

| `list_kind` | Inhalt | Hinweise |
|---|---|---|
| `tasks` (Vorgabe) | Aufgabenliste mit `items` | – |
| `note` | Notiz: Text in `rich_note`, optional `items` als Aufgaben über dem Text | Text ohne Formatierung: `"rich_note": {"text": "…", "spans": [], "links": {}}` |
| `page` | Seite | formatierte Seiten besser als [Markdown-Datei](seiten-markdown.md); `rich_note` wird nicht aus Markdown umgewandelt |
| `drawing` | Pixelzeichnung in `drawing`, keine `items` | nur mit dem Hilfsskript kodieren |
| `gallery` | Galerie | sinnlos ohne Bilder, die das Format nicht trägt |

`labels` an Listen übernimmt diese Glide-Fassung noch nicht. Welches Glide-Feld über welchen Weg ankommt, steht maschinenlesbar in `abdeckung.json` im Skillordner. `rich_note.spans` wären Formatbereiche mit Python-Zeichenpositionen; lass sie leer.

## Punkte

```json
{"type": "task", "title": "Angebote einholen", "description": "Ziel und Ergebnis.",
 "importance": 2, "due": "2026-11-27", "due_time": "14:00", "planned_date": "2026-11-23",
 "estimated_minutes": 60, "labels": ["label-1"], "done": false,
 "checklist": [{"text": "Anfrage senden", "done": false}],
 "children": [ … ]}
```

| Feld | Werte | Hinweise |
|---|---|---|
| `type` | `task`, `long`, `group`, `heading` | unbekannt → Aufgabe |
| `title` | Text, höchstens 40 Zeichen | Pflicht; `text` ist ein gleichwertiger Altname |
| `description` | Text | Details, Mengen, Begründung, lange Originaltitel |
| `importance` | 0–3 | nur `task`/`long` |
| `due` | `JJJJ-MM-TT` | bis wann fertig |
| `due_time` | `HH:MM` | nur zusammen mit `due` |
| `planned_date` | `JJJJ-MM-TT` | wann daran arbeiten |
| `estimated_minutes` | ganze Zahl 1–60.000 | sonst lässt Glide den Aufwand still leer |
| `labels` | Liste von Label-Schlüsseln oder -Namen | unbekannte Namen legt Glide an |
| `done` | `true`/`false` | nur `task`/`long` |
| `checklist` | bis 50 Schritte `{"text", "done"}`, Text bis 200 Zeichen | keine eigenen Termine |
| `children` | Punkte, bis 12 Ebenen tief | eigenständig erledigbar |

`group` und `heading` tragen weder Termine noch Wichtigkeit, Erledigt oder Checkliste; Glide verwirft solche Angaben dort.

Langtexte und Überschriften erhalten in Glide automatisch ihre festen Labels „Langtext“ und „Zwischenüberschrift“; die Art bestimmt das Label. Diese Namen deshalb nicht als eigene Labels verwenden, sondern `type` setzen.

## Zeichnung

Eine Liste mit `"list_kind": "drawing"` trägt `drawing` im Format `glide.drawing`: quadratisch mit 16, 32, 64 oder 128 Zellen, Palette mit `#FFFFFF` an erster Stelle (Grund, im Symbol durchsichtig; deckendes Weiß ist `#FEFEFE`), je Zeile ein Hexwert pro Zelle (`hex8-row-v1`). Das Hilfsskript erzeugt das Dokument aus einer Zeichenlegende. Bildfolgen (`animation`) prüft erst Glide.

## Grenzen

Höchstens 5.000 Punkte, 12 MB, 12 Ebenen und 50 Checklistenschritte je Punkt. Nicht übernommen werden heute Wiederholungen, Erinnerungen, Farben, Pixelsymbole, Ordnerarten, Verknüpfungen, Anhänge, Vorlagen, Pinnwand und Ansichten.
