# Glide-Austauschformat – Glide 3.23.0

Stand 18.09.2026 · Glide 3.23.0 · Aufgabenformat 16 · Austauschformat 1

## Wozu ein eigenes Format

Das interne Aufgabenformat ist seit 3.0 sechzehnmal gewachsen. Es trägt Felder,
die eine fremde Stelle weder erfinden kann noch soll – Anhangpfade,
Zustellbelege von Erinnerungen, Verlaufseinträge – und es wird weiter wachsen.
Würde es zum Vertrag mit einem anderen System, müsste dieses jede künftige
Migration mitgehen; umgekehrt wäre Glide daran gebunden, sein internes Format
nicht mehr zu verändern.

Deshalb zwei getrennte Zahlen:

| Zahl | Beschreibt | Aktuell |
|---|---|---|
| `DATA_SCHEMA_VERSION` | wie Glide speichert | 16 |
| `EXCHANGE_FORMAT_VERSION` | worauf sich ein fremdes System verlassen kann | 1 |

Die zweite darf jahrelang stehen bleiben, während die erste weiterzählt.

> **Leitsatz:** Die Quelle beschreibt, was entstehen soll. Glide entscheidet,
> wie es im aktuellen internen Format gespeichert wird.

## Aufbau einer `.glideexchange`

```json
{
  "format": "glide.exchange",
  "format_version": 1,
  "mode": "create",
  "generator": { "type": "ai" },
  "created_for": { "application": "Glide", "application_version": "3.23.0", "data_schema": 16 },
  "capabilities": { "…": "was die erzeugende Fassung kann" },
  "labels":  [ { "key": "label-1", "name": "Release", "color": "accent" } ],
  "folders": [ { "key": "folder-1", "title": "Projekt", "parent": "folder-0" } ],
  "lists":   [ { "key": "list-1", "title": "Titel", "folder": "folder-1",
                 "description": "Wozu diese Liste da ist.", "items": [ … ] } ]
}
```

Ein Punkt:

```json
{
  "type": "task",
  "title": "Kurze Handlung",
  "description": "Ziel und erwartetes Ergebnis.",
  "importance": 3,
  "due": "2026-10-01", "due_time": "14:30",
  "planned_date": "2026-09-28", "estimated_minutes": 90,
  "labels": ["label-1"],
  "done": false,
  "checklist": [ { "text": "Schritt", "done": false } ],
  "children": [ … ]
}
```

### Keine internen Kennungen

Eine erzeugende Stelle soll niemals echte Glide-Kennungen erfinden müssen. Die
Datei arbeitet mit frei wählbaren Schlüsseln (`list-1`, `label-2`); die echten
IDs vergibt Glide beim Import. Das ist zugleich die Zusicherung nach außen:
Eine exportierte Datei enthält keine internen Kennungen.

### Punktarten und ihre Bedeutung

| Art | Bedeutung |
|---|---|
| `task` | Eine ausführbare Handlung mit eindeutigem Ergebnis. |
| `long` | Ein umfangreicherer, textorientierter Arbeitsgegenstand. |
| `group` | Behälter für Punkte. Nicht selbst erledigbar, ohne Termin. |
| `heading` | Reine Gliederung. Keine Fälligkeit, Wichtigkeit oder Erledigung. |

Die Spezifikation erklärt ausdrücklich auch die Bedeutung der Felder, nicht nur
ihre Syntax – insbesondere den Unterschied, den ein fremdes System sonst nicht
erraten kann:

- **`due`** beantwortet: bis wann muss es fertig sein.
- **`planned_date`** beantwortet: wann soll daran gearbeitet werden.
- **`children`** sind eigenständig erledigbare Unterpunkte.
- **`checklist`** sind Arbeitsschritte innerhalb eines Punkts, ohne eigene
  Termine, Labels oder Anhänge.

## Capability-Registry

Die Datei nennt selbst, was die erzeugende Fassung kann. Eine erzeugende Stelle
muss es nicht aus einer Versionsnummer ableiten.

```json
"capabilities": {
  "item_types": ["group", "heading", "long", "task"],
  "nested_items": 1, "descriptions": 1, "labels": 1,
  "due_dates": 1, "due_times": 1, "planned_date": 1,
  "estimated_minutes": 1, "checklists": 1, "folders": 1,
  "attachments": 0, "repeat": 0, "reminders": 0, "patch_mode": 0,
  "max_items": 5000, "max_checklist_entries": 50, "max_depth": 12
}
```

Die Zahl je Fähigkeit ist deren eigene Stufe: 0 heißt „kennt Glide hier nicht“,
1 die erste Ausprägung. Wird eine Fähigkeit später anders aufgebaut, steigt
ihre Zahl – ohne dass die Formatversion steigen muss.

**Anhänge, Wiederholungen und Erinnerungen stehen bewusst auf 0.** Anhänge sind
Dateien, keine Textangabe; Wiederholungen und Erinnerungen haben eigene
Regelwerke mit Serienende, Zeitzonen und Zustellbelegen, die eine erzeugende
Stelle kaum verlässlich trifft. Ein erfundener Wert wäre schlimmer als ein
fehlender.

## Import

```
Datei wählen
   ↓
JSON prüfen · Formatname · Formatversion · Modus
   ↓
Felder, Werte und Verweise prüfen
   ↓
Vorschau: was würde entstehen
   ↓
Bestätigung durch den Nutzer
   ↓
ein Rückgängig-Schritt
```

**Unbekannte Felder werden nicht still verworfen.** Enthält die Datei eine
Angabe, die diese Fassung nicht kennt, nennt die Vorschau sie – und dann liegt
der Fokus auf „Abbrechen“ statt auf „Importieren“. Wer trotzdem importiert,
weiß, was fehlen wird.

**Der Import legt ausschließlich Neues an.** Vorhandene Listen, Ordner und
Punkte werden nie verändert. Scheitert das Speichern, gehen Listen, Ordner,
Labels und der Rückgängig-Stapel exakt auf den Stand davor zurück.

Grenzen: 12 MB je Datei, 5.000 Punkte, 12 Ebenen Verschachtelung, 50
Checklistenschritte je Punkt.

## Zwei Ebenen, aber nicht zwei Verträge

Die Frage, ob das Format aus einer menschenlesbaren und einer maschinenlesbaren
Ebene bestehen sollte, ist mit **ja, aber mit klarer Rangfolge** beantwortet.
Zwei gleichrangige Formate wären zwei Verträge, zwei Parser und zwei Stellen,
an denen dieselbe Aussage verschieden verstanden werden kann.

- **Verbindlich ist die JSON-Datei.** Sie ist verlustfrei, prüfbar und trägt
  Schlüssel, Labels und Metadaten. Der Rundlauf Export → Import → Export
  liefert dieselben Punkte.
- **Daneben liest Glide eine Gliederung in Markdown.** `# Liste`,
  `## Abschnitt`, `- Aufgabe`, eingerückte Unterpunkte, `- [ ]` als
  Checklistenschritt unter einer Aufgabe ohne eigene Unterpunkte, freier Text
  darunter als Beschreibung. Sie ist das, was ein Sprachmodell am
  zuverlässigsten erzeugt, und ohne Werkzeug lesbar.

Die Markdown-Gliederung trägt bewusst weniger – keine Schlüssel, keine Labels,
keine Metadaten – und ist deshalb für den Rückweg nicht geeignet. Wer einen
Rundlauf braucht, nimmt JSON.

## Bedienung

| Menü „Datei“ | Wirkung |
|---|---|
| Für KI bereitstellen … | Schreibt den gewählten Umfang als `.glideexchange`. |
| KI-Ergebnis importieren … | Liest `.glideexchange`, `.json` oder `.md` mit Vorschau. |
| Austauschformat anzeigen … | Zeigt die Anweisung für eine KI zum Kopieren. |

Die Anweisung wird aus den tatsächlichen Konstanten erzeugt – Formatname,
Version, Grenzen, Punktarten. Sie kann deshalb nicht veralten.

## Was der Rundlauf erhält und was nicht

| Erhalten | Nicht abgebildet |
|---|---|
| Ordner samt Verschachtelung | Anhänge |
| Listen mit Beschreibung | Wiederholungen |
| Alle vier Punktarten | Erinnerungen |
| Unterpunkte bis Ebene 12 | Farben je Punkt |
| Beschreibungen, Labels | Änderungsverlauf |
| Fälligkeit mit Uhrzeit | Papierkorb |
| Bearbeitungstag und Aufwand | Reiter und Pinnwandpositionen |
| Wichtigkeit, Erledigt-Zustand | |
| Checklisten mit Zustand | |

## Nächste Stufen

- **`mode: "patch"`** – Änderungsvorschläge an vorhandenen Punkten statt nur
  Neuanlage. Setzt voraus, dass eine exportierte Datei stabile Verweise auf
  vorhandene Punkte tragen darf, ohne interne Kennungen preiszugeben.
- **Ein Kontextpaket** (`.glidecontext`) mit Spezifikation, Schema und
  ausgewähltem Inhalt in einer Datei.
- **Anhänge** als Verweise mit Prüfsumme, nicht als Inhalt.
