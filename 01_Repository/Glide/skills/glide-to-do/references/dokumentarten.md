# Rezepte je Dokumentart

Stand 16.11.2026 · Glide 3.67.0 · Aufgabenformat 26

Kurze Muster für häufige Anfragen. Die Beispiele liegen in `assets/beispiele/`.

## Recherche, Bericht, Übersicht

- **Seite** als `.md`, beginnend mit `# Titel` ([Seiten in Markdown](seiten-markdown.md)).
- Ergebnis zuerst, dann Vergleich (Tabelle), Bewertung, Empfehlung (Zitat), nächste Schritte als `- [ ]`, Quellen mit Datum.
- Beispiel: `recherchebericht.md`.

## Aufgabenliste

- Eine Liste je Thema; Abschnitte als `heading`, Teilschritte als `checklist`, eigenständige Teilaufgaben als `children`.
- Termine nur, wenn genannt. Aufwand schätzen, wenn der Nutzer planen will; dann ehrlich runden.

## Einkaufsliste, Packliste

- Eine Liste; Abschnitte nach Laden oder Bereich als `heading`; je Artikel ein `task`, Menge in `description`.
- Ein Punkt „Einkaufen gehen“ mit `planned_date` und `estimated_minutes`, wenn ein Tag feststeht.
- Ein Label nur, wenn es etwas unterscheidet (z. B. „Wochenmarkt“).
- Beispiel: `einkaufsliste.glideexchange`.

## Projekt

- Ein Ordner mit `description` (Ziel, Zeitraum); darin Listen je Phase oder Bereich; Unterordner über `parent`, der Elternordner steht davor.
- Meilensteine als `task` mit `due` und `importance`; Arbeitspakete als `group` mit `children`; Abläufe eines Tages mit `due` und `due_time`.
- Hintergrund und Entscheidungen zusätzlich als Seite (`.md`).
- Beispiel: `projekt.glideexchange`.

## Aufgabenübersicht, Wochenplan

- Eine Liste je Woche oder Bereich; die Arbeitstage als `planned_date`, Fristen als `due`.
- Bereits Erledigtes nur aufnehmen, wenn der Nutzer einen Rückblick möchte (`done: true`).

## Notiz, Gesprächsnotiz, Protokoll

- Kurz und ohne Formatierung: `list_kind: "note"` mit `rich_note.text`; Folgeaufgaben als `items`. Beispiel: `notiz.glideexchange`.
- Mit Überschriften, Tabellen oder vielen Aufgaben: lieber eine Seite (`.md`).

## Zeichnung, Symbol

- Größe 16 für Symbole, 32 oder 64 für Motive. Legende mit wenigen Farben; `.` für den durchsichtigen Grund, `#FEFEFE` für deckendes Weiß.
- `python3 scripts/glide_datei.py zeichnung eingabe.json ausgabe.glideexchange`; mit `--nur-zeichnung` entsteht ein `glide.drawing`-Dokument für Datei › Importieren › „Zeichnung (SVG/JSON) importieren …“.
- Beispiel: `zeichnung-eingabe.json` → `zeichnung.glideexchange`.

## Überarbeiten, Priorisieren, Termine verschieben

- Nur über ein Kontextpaket ([Änderungsvorschlag](aenderungsvorschlag.md)). Beispiel: `kontextpaket.glidecontext` → `aenderungsvorschlag.glideexchange`.

## Noch nicht möglich

Wiederkehrende Aufgaben, Erinnerungen, Farben, Notizbücher, Bücher, Vorlagen, Galerien, Pinnwände. Die gewünschte Angabe in die Beschreibung schreiben und dem Nutzer sagen, dass er sie in Glide setzt.
