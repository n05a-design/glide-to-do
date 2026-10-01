# Glide – KI-Austauschformat und Zukunftsarchitektur

## Ziel

Für zukünftige KI-gestützte Arbeitsabläufe sollte **nicht das interne Glide-Datenformat direkt an eine KI gegeben werden**. Stattdessen sollte eine eigene, stabile **Glide-Austauschspezifikation für KI-Ausgaben** entstehen.

So kann Glide intern weiterwachsen, während KI-Ausgaben über Jahre kompatibel bleiben.

---

# 1. Grundidee

Glide sollte künftig drei Datenebenen unterscheiden:

## Ebene A – internes Glide-Datenformat

Das bleibt das, was Glide intern benutzt.

**Heute:** Datenformat 15.

Es darf sich mit Glide verändern:

15 → 16 → 17 → 18 …

Die KI muss dieses Format **nicht vollständig verstehen**.

## Ebene B – Glide Exchange Format

Neu, beispielsweise:

**`*.glideexchange`**

Das wäre die stabile Schnittstelle für:

- ChatGPT
- Claude
- lokale LLMs
- andere KI-Systeme
- zukünftige Plugins
- Importgeneratoren
- eventuell später eine Glide-API

Das Format bekommt eine eigene Version:

```text
Glide App Version:       3.21.4
Glide Data Schema:       15
Glide Exchange Schema:   1
```

Wenn Glide irgendwann bei Datenformat 24 ist, kann `Glide Exchange Schema 1` möglicherweise immer noch importiert werden.

## Ebene C – KI-Beschreibung

Dazu gibt es eine Datei wie:

**`GLIDE_EXCHANGE_SPEC.md`**

Diese Datei kann an eine KI angehängt werden.

Sie erklärt in verständlicher Sprache:

- welche Punktarten es gibt,
- was Gruppen und Überschriften bedeuten,
- wie Unteraufgaben funktionieren,
- wie Labels verwendet werden,
- welche Felder erlaubt sind,
- welche Funktionen aktuell unterstützt werden,
- welche Regeln die KI beim Erzeugen beachten soll.

---

# 2. Warum nicht direkt `.glidebackup`

Die aktuelle Glide-Datenstruktur unterstützt bereits sehr viele Funktionen:

- `task`
- `long`
- `group`
- `heading`
- rekursive `children`
- Beschreibung
- Labels
- Anhänge
- Wiederholung
- Erinnerung
- Bearbeitungstag
- Aufwand

Gerade deshalb sollte das interne Format **nicht** zum externen KI-Vertrag werden.

Wenn später beispielsweise `notes`, benutzerdefinierte Felder oder neue Punktarten entstehen, müsste sonst jede externe KI jede interne Migration kennen.

---

# 3. Glide erzeugt die KI-Anlage selbst

Langfristig sollte Glide einen Menüpunkt bekommen:

**Datei → Für KI bereitstellen …**

oder:

**KI → Kontextdatei erstellen …**

Dann erzeugt Glide automatisch eine Datei wie:

`Glide_KI_Kontext_3.21.4.glidecontext`

Möglicher Inhalt:

```text
manifest.json
schema.json
README_AI.md
context.json
attachments/
```

## `README_AI.md`

Menschen- und KI-lesbare Anleitung.

## `schema.json`

Maschinenlesbare Definition der erlaubten Felder.

## `context.json`

Optional der Inhalt der ausgewählten Liste beziehungsweise des ausgewählten Ordners.

## `attachments/`

Nur Anhänge, die ausdrücklich für die KI mitgegeben werden sollen.

---

# 4. Die KI gibt eine `.glideexchange` zurück

Beispiel:

`projektanalyse.glideexchange`

Glide öffnet diese Datei nicht blind.

Stattdessen erscheint eine Importvorschau:

```text
KI-Import

Enthalten:

1 Ordner
4 Listen
38 Aufgaben
7 Long-Tasks
9 Überschriften
5 Gruppen
26 Unteraufgaben
11 Labels
0 unbekannte Funktionen

[Vorschau]
[Importieren]
```

Das entspricht der bestehenden Sicherheitsphilosophie von Glide: Inhalte werden vor kritischer Übernahme geprüft.

---

# 5. Keine internen UUIDs von der KI

Eine KI sollte niemals echte Glide-UUIDs erfinden müssen.

Statt:

```json
"id": "ae0ed99789455f20bfdfd60d06fb11e6"
```

soll die Austauschdatei temporäre Schlüssel verwenden:

```json
"key": "release-001"
```

Labels genauso:

```json
{
  "key": "label-release",
  "name": "Release"
}
```

Referenz:

```json
"labels": ["label-release"]
```

Glide erzeugt beim Import die echten internen IDs.

---

# 6. Beispiel einer `.glideexchange`

```json
{
  "format": "glide.exchange",
  "format_version": 1,

  "created_for": {
    "application": "Glide",
    "application_version": "3.21.4",
    "data_schema": 15
  },

  "generator": {
    "type": "ai"
  },

  "mode": "create",

  "labels": [
    {
      "key": "label-release",
      "name": "Release",
      "color": "accent"
    },
    {
      "key": "label-entscheidung",
      "name": "Entscheidung",
      "color": "clear"
    }
  ],

  "lists": [
    {
      "key": "list-release",
      "title": "Glide – Releasevorbereitung",
      "description": "Aufgaben bis zur Veröffentlichung.",

      "items": [
        {
          "type": "heading",
          "title": "Plattformabnahme"
        },

        {
          "type": "long",
          "title": "Ziel der Plattformabnahme",
          "description": "Windows und macOS vollständig nativ prüfen."
        },

        {
          "type": "group",
          "title": "Windows",
          "children": [
            {
              "type": "task",
              "title": "Vollständigen QA-Lauf durchführen",
              "description": "Aktuellen Prüfstand unter Windows ausführen.",
              "importance": 3,
              "labels": ["label-release"],

              "children": [
                {
                  "type": "task",
                  "title": "Ergebnisprotokoll archivieren"
                },
                {
                  "type": "task",
                  "title": "Abweichungen dokumentieren"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

---

# 7. Zukünftiges Notizmodell

Eine wichtige Erweiterung ist die Trennung zwischen **Beschreibung** und **Notiz**.

## Beschreibung

Beschreibt:

- was die Aufgabe bedeutet,
- was getan werden soll,
- welches Ergebnis erwartet wird,
- fachlichen Kontext.

Sie kann vom Benutzer, einer Vorlage, einem Import oder einer KI stammen.

## Notiz

Dokumentiert:

- persönliche Erkenntnisse,
- Bearbeitungsverlauf,
- Gesprächsstände,
- Rückmeldungen,
- Entscheidungen,
- Beobachtungen.

Statt eines einzelnen zusätzlichen Textfelds sollte ein echtes Notizmodell geprüft werden:

```json
"notes": [
  {
    "id": "...",
    "text": "Mit Stefan telefoniert. Angebot kommt nächste Woche.",
    "created_at": "2026-09-16T13:45:00",
    "updated_at": "2026-09-16T13:45:00",
    "source": "user"
  }
]
```

Mögliche Herkunft:

```text
user
ai
import
system
```

Wichtig: Beschreibung darf nicht technisch auf „KI“ und Notiz nicht technisch auf „Mensch“ festgelegt werden.

---

# 8. Unteraufgaben

Unteraufgaben sind datentechnisch bereits vorbereitet, weil jedes Item `children` besitzen kann.

Es sollte daher **keine zweite `subtasks`-Struktur** eingeführt werden.

Stattdessen muss die Bedienung ausgebaut werden:

```text
☐ Windows Release
    ☐ Installer erstellen
        ☐ Icon integrieren
        ☐ AppUserModelID vergeben
        ☐ Upgrade testen
    ☐ Signatur testen
    ☐ Clean-Machine-Test
```

Ziele:

- Unteraufgaben direkt in einer Aufgabe anlegen,
- Hierarchie sichtbar machen,
- auf-/zuklappen,
- direkt erledigen,
- per Tastatur bedienen,
- Reihenfolge verändern,
- Navigation zum übergeordneten Punkt.

---

# 9. Pinnwand 2.0

Heute ist die Pinnwand primär manuell.

Künftig sollte sie auch dynamisch funktionieren können:

```text
Pinnwand-Modus:
○ Manuell
● Alle Punkte dieser Liste
○ Nach Filter
○ Nach Label
○ Nur offene Punkte
```

Beispieldefinition:

```json
{
  "mode": "dynamic",
  "source": {
    "type": "list",
    "list_id": "..."
  },
  "filter": {
    "done": false
  }
}
```

Die Karten werden berechnet, nicht kopiert.

Eine Änderung auf der Pinnwand verändert weiterhin dieselbe Aufgabe.

---

# 10. Allgemeines Ansichtsmodell

Langfristig könnte Glide ein allgemeines `ViewDefinition`-Modell erhalten.

Heute existieren bereits:

- normale Liste
- Tabelle
- Reiter
- Pinnwand
- Mein Tag
- Tagesplanung
- Filteransichten

Beispiel:

```json
{
  "type": "table",

  "source": "list",

  "columns": [
    {
      "field": "title",
      "width": 320
    },
    {
      "field": "due",
      "width": 120
    },
    {
      "field": "planned_date",
      "width": 120
    },
    {
      "field": "estimated_minutes",
      "width": 100
    }
  ],

  "sort": [
    {
      "field": "planned_date",
      "direction": "asc"
    }
  ]
}
```

Dadurch könnten verschiedene Ansichten dieselben Quellen-, Filter- und Sortierregeln wiederverwenden.

---

# 11. Verstellbare Spalten

Die aktuelle Tabellenansicht sollte langfristig mehr speichern als nur die Auswahl sichtbarer Felder.

Beispiel:

```json
[
  {
    "field": "text",
    "visible": true,
    "width": 340
  },
  {
    "field": "labels",
    "visible": true,
    "width": 180
  }
]
```

Später zusätzlich möglich:

- Reihenfolge,
- Mindestbreite,
- Sortierung,
- Gruppierung,
- eingefrorene Spalten,
- benutzerdefinierte Felder.

---

# 12. Einheitliche Scrollbars

Die unterschiedlichen Tk-Komponenten führen heute zu abweichendem Scrollverhalten.

Eine gemeinsame Abstraktion wäre sinnvoll, beispielsweise:

```text
GlideScrollSurface
```

mit Adaptern:

```text
CanvasScrollAdapter
TreeScrollAdapter
TextScrollAdapter
BoardScrollAdapter
```

Gemeinsame Regeln:

- gleiche Scrollbar,
- gleicher Abstand,
- gleiche Breite,
- gleiche Hoverdarstellung,
- gleiches Mausradverhalten,
- Trackpad,
- Shift+Scroll horizontal,
- Tastaturscrollen,
- Fokusbehandlung,
- obere/untere Grenze,
- Hell/Dunkel.

---

# 13. Capability-System

Die KI-Kontextdatei sollte explizit beschreiben, was die installierte Glide-Version kann.

Heute beispielsweise:

```json
"capabilities": {
  "item_types": [
    "task",
    "long",
    "group",
    "heading"
  ],

  "nested_items": true,
  "notes": false,
  "label_descriptions": false,
  "custom_fields": false,
  "pinboard_dynamic_views": false
}
```

Später:

```json
"capabilities": {
  "item_types": [
    "task",
    "long",
    "group",
    "heading"
  ],

  "nested_items": true,
  "notes": true,
  "label_descriptions": true,
  "custom_fields": true,
  "pinboard_dynamic_views": true
}
```

Die KI muss dadurch nicht aus einer App-Version erraten, welche Features existieren.

---

# 14. Unbekannte Felder niemals still verwerfen

Wenn eine Datei beispielsweise `notes` enthält, die installierte Glide-Version aber keine Notes unterstützt, darf Glide diese Daten nicht unbemerkt wegwerfen.

Stattdessen:

```text
Diese Datei verwendet Funktionen, die Glide 3.21.4 noch nicht unterstützt:

– Notizen
– Labelbeschreibungen

Datei wurde nicht verändert.

[Trotzdem ohne diese Daten importieren …]
[Abbrechen]
```

Standardmäßig sollte **Abbrechen** sicherer sein.

---

# 15. Zwei KI-Arbeitsweisen

## A. `create`

Die KI erstellt neue Daten.

Beispiel:

> Erstelle aus diesem Projektbericht einen Glide-Arbeitsplan.

Ergebnis:

`Glide_Projektplan.glideexchange`

```json
"mode": "create"
```

Glide fügt neue Ordner, Listen, Labels und Punkte kontrolliert hinzu.

## B. `patch`

Später kann Glide bestehenden Kontext exportieren und die KI nur Änderungen vorschlagen lassen.

Beispiel:

```json
{
  "mode": "patch",

  "operations": [
    {
      "operation": "update",
      "target": "item:3be91...",
      "set": {
        "description": "Aktualisierte Beschreibung ..."
      }
    },

    {
      "operation": "add_child",
      "parent": "item:3be91...",
      "item": {
        "key": "new-1",
        "type": "task",
        "title": "Windows-Sichtprüfung dokumentieren"
      }
    },

    {
      "operation": "add_note",
      "target": "item:3be91...",
      "note": {
        "text": "Aus aktuellem QA-Bericht ergänzt.",
        "source": "ai"
      }
    }
  ]
}
```

Glide zeigt die Änderungen vor der Übernahme.

---

# 16. KI darf den Bestand niemals direkt überschreiben

Vorgesehener Ablauf:

```text
KI-Datei
   ↓
Syntax prüfen
   ↓
Exchange-Version prüfen
   ↓
Capabilities prüfen
   ↓
Felder validieren
   ↓
Referenzen prüfen
   ↓
Vorschau
   ↓
Benutzer bestätigt
   ↓
Rückfallsicherung
   ↓
eine atomare Änderung
   ↓
Undo möglich
```

---

# 17. Semantische Regeln für KI

Die Spezifikation sollte nicht nur Syntax, sondern auch Bedeutung erklären.

## `task`

Eine ausführbare Handlung mit eindeutigem Ergebnis.

## `long`

Eine umfangreichere Aufgabe beziehungsweise textorientierter Arbeitsgegenstand.

## `heading`

Nur Gliederung.

Keine Fälligkeit, Wichtigkeit oder Erledigung.

## `group`

Struktureller Container für Punkte.

Nicht selbst erledigbar.

## `description`

Erklärt Aufgabe, Ziel, Kontext und erwartetes Ergebnis.

## `note`

Dokumentiert Erkenntnisse oder Verlauf.

## `children`

Konkrete Unterpunkte.

---

# 18. KI soll nicht alles zur Aufgabe machen

Ein Projektbericht könnte beispielsweise strukturiert werden als:

```text
Glide – nächste Entwicklung
│
├── ÜBERSCHRIFT
│   Releasefähigkeit
│
├── LONG-TASK
│   Zielbild 3.22
│   Beschreibung:
│   Stabiler installierbarer Stand ...
│
├── GRUPPE
│   Plattformabnahme
│   │
│   ├── AUFGABE
│   │   Windows Vollrun
│   │   │
│   │   ├── Unteraufgabe
│   │   │   Protokoll archivieren
│   │   └── Unteraufgabe
│   │       Fehler klassifizieren
│   │
│   └── AUFGABE
│       macOS Sichtabnahme
│
├── ÜBERSCHRIFT
│   Produkt
│
└── GRUPPE
    Onboarding
    │
    ├── AUFGABE
    │   First-Run entwickeln
    │
    └── LONG-TASK
        Onboarding-Konzept dokumentieren
```

Dadurch wird ein KI-Ergebnis in Glide wirklich bearbeitbar.

---

# 19. Labels

Die KI darf Labels erzeugen, sollte aber nicht für jede einzelne Aufgabe ein neues Label anlegen.

Beispiele:

```text
Release
Windows
macOS
QA
UX
Entscheidung
Blocker
Dokumentation
Architektur
```

Später könnten Labels Beschreibungen erhalten:

```json
{
  "name": "Blocker",
  "color": "red",
  "description": "Verhindert den nächsten Release-Schritt."
}
```

Das wäre eine echte zukünftige Datenmodellerweiterung.

---

# 20. Glide Capability Registry

Eine zentrale Registry wäre sinnvoll:

```python
GLIDE_CAPABILITIES = {
    "tasks": 1,
    "long_tasks": 1,
    "groups": 1,
    "headings": 1,
    "children": 1,
    "labels": 1,
    "attachments": 1,
    "repetition": 1,
    "reminders": 1,
    "planned_date": 1,
    "estimated_minutes": 1,

    "notes": 0,
    "label_descriptions": 0,
    "custom_fields": 0,
    "dynamic_pinboards": 0
}
```

Später:

```python
"notes": 1
```

oder bei einem Formatwechsel der Fähigkeit:

```python
"notes": 2
```

Die KI-Beschreibung kann dann automatisch aus Glide erzeugt werden.

---

# 21. Eigener KI-Bereich in Glide

Langfristig denkbar:

```text
KI
├── Kontext für KI exportieren …
├── KI-Ergebnis importieren …
├── Änderungsvorschlag prüfen …
└── Austauschformat anzeigen …
```

Beim Export könnte der Benutzer auswählen:

```text
Was soll die KI sehen?

☑ Diese Liste
☑ Unteraufgaben
☑ Beschreibungen
☑ Notizen
☑ Labels
☐ Anhänge
☐ Erledigte Aufgaben
☐ Änderungsverlauf

Zweck
○ Neue Aufgaben vorschlagen
○ Bestehende Struktur überarbeiten
○ Projektstatus analysieren
○ Dokument in Aufgaben umwandeln
```

Das wäre nicht an einen bestimmten KI-Anbieter gebunden.

---

# 22. Warum `.glideexchange` statt `.glideai`

Der Name sollte die Schnittstelle nicht unnötig auf KI begrenzen.

Später könnten dieselben Dateien auch erzeugt werden von:

- Excel-Konvertern
- Browser-Erweiterungen
- Outlook-Importen
- CLI-Tools
- anderen Glide-Instanzen
- Firmenanwendungen
- KI

Im Manifest:

```json
"generator": {
  "type": "ai"
}
```

oder:

```json
"generator": {
  "type": "glide"
}
```

---

# 23. Gesamtsystem

```text
                    GLIDE
                      │
                      │ Für KI exportieren
                      ▼
             ┌───────────────────┐
             │ .glidecontext     │
             │                   │
             │ manifest.json     │
             │ schema.json       │
             │ README_AI.md      │
             │ context.json      │
             │ attachments/      │
             └─────────┬─────────┘
                       │
                       ▼
                 ChatGPT / Claude
                 lokale KI / etc.
                       │
                       ▼
             ┌───────────────────┐
             │ .glideexchange    │
             │                   │
             │ mode=create/patch │
             │ labels            │
             │ folders           │
             │ lists             │
             │ items             │
             │ operations        │
             └─────────┬─────────┘
                       │
                       ▼
                    GLIDE
                       │
                 Validierung
                       │
                    Vorschau
                       │
                  Bestätigung
                       │
                 Rückfallsicherung
                       │
                       ▼
              Datenformat 15/16/…
```

---

# 24. Vier größere Entwicklungsstränge

Die zukünftigen Ideen lassen sich sinnvoll in vier größere Bereiche bündeln:

## 1. Datenmodell

- echte Notizen
- eventuell Labelbeschreibungen
- später benutzerdefinierte Felder

## 2. View Engine

- bessere Liste/Tabelle
- konfigurierbare Spalten
- dynamische Pinnwand
- später eigene Ansichten

## 3. UI-Grundbausteine

- einheitliche Scroll-Flächen
- Dropdowns
- Tabellen-/Board-Komponenten
- Größenverhalten
- Fokus
- Trackpad/Maus/Tastatur

## 4. Glide Exchange

- versionierter KI-/Importvertrag
- zunächst `create`
- später `patch`
- Capability-System
- Validierung
- Vorschau
- Rückfallsicherung
- Undo

---

# 25. Leitprinzip

Der entscheidende Grundsatz sollte sein:

> **Die KI beschreibt, was in Glide entstehen soll. Glide selbst entscheidet, wie dies im aktuellen internen Datenformat gespeichert wird.**

Dadurch bleibt die KI-Schnittstelle stabil, auch wenn Glide intern weiterwächst.
