# Glide verstehen: Aufbau und Datenmodell

Stand 22.11.2026 · Glide 1.0.1 · Aufgabenformat 26 · Austauschformat 2

Für Agenten, die Nutzern Glide erklären oder an Glide mitarbeiten. Was der Skill davon anlegen kann, steht je Feld in `abdeckung.json`.

## Bereiche der Oberfläche

Die Seitenleiste ordnet alles in vier Bereiche: **Seiten** (Bücher, Ordner, Seiten), **Listen** (alle Arten), **Notizen** (Notizbücher, Notizen) und **Zeichnungen**. Darüber stehen Systemzeilen: Startseite, Heute, Labels, Vorlagen, Papierkorb und bei Inhalt der Eingang. „Heute“ zeigt jede Aufgabe des Tages genau einmal, mit Tagesbilanz aus Aufwand und Kapazität.

## Objekte

| Objekt | Arten | Wichtige Felder |
|---|---|---|
| Ordner | Ordner (`standard`), Buch (`library`, neue Einträge sind Seiten), Notizbuch (`journal`, datierte Einträge) | Titel, Beschreibung, Elternordner, Farbe, Pixelsymbol, Labels |
| Liste | Aufgabenliste (`tasks`), Notiz (`note`), Seite (`page`), Zeichnung (`drawing`), Galerie (`gallery`); die Art ist nach dem Anlegen fest | Titel, Beschreibung, Ordner, Punkte, Text (`rich_note`), Zeichnung, Labels, Archiv |
| Punkt | Aufgabe (`task`), Langtext (`long`), Gruppe (`group`), Zwischenüberschrift (`heading`) | Titel, Beschreibung, Fälligkeit mit Uhrzeit, Bearbeitungstag mit Uhrzeit, Aufwand, Wichtigkeit 0–3, Erledigt, Labels, Checkliste, Unterpunkte, Wiederholung, Erinnerung, Anhänge, Verknüpfungen, „Wartet auf“ |
| Label | eigene Labels; feste Labels „Langtext“ und „Zwischenüberschrift“ folgen der Punktart | Name, Farbe |

## Grundsätze, die der Skill weiterträgt

- **Fälligkeit ist nicht Bearbeitungstag.** Die Fälligkeit sagt, bis wann etwas fertig sein muss; der Bearbeitungstag, wann man daran arbeitet. „Heute“ plant mit dem Bearbeitungstag.
- **Titel kurz, Inhalt in die Beschreibung.** Neue Titel haben höchstens 40 Zeichen.
- **Gliederung ist keine Aufgabe.** Gruppen und Überschriften haben keine Termine, Wichtigkeit, Erledigt-Zustand oder Checkliste.
- **Unterpunkte oder Checkliste:** Unterpunkte sind eigenständig erledigbar, Checklistenschritte kurze Schritte innerhalb eines Punkts ohne eigene Termine; ein abgehakter Schritt erledigt den Punkt nicht.
- **Aufgaben in Seiten sind echte Punkte.** Ein `- [ ]` in einer importierten Seite wird ein Punkt, der in „Heute“ eingeplant werden kann.
- **Lokal und geprüft.** Glide läuft ohne Konto und Netz. Fremde Dateien ändern den Bestand nie unbesehen: Prüfung, Vorschau, ein Rückgängig-Schritt. Vorhandenes ändert nur ein Änderungsvorschlag mit Konfliktprüfung.

## Wie Glide speichert

Glide hält alle Listen, Ordner, Labels und Punkte in `liste_speicher.json` im Datenordner (Windows `%APPDATA%\Glide`, macOS `~/Library/Application Support/Glide`, Linux `~/.local/share/Glide`), dazu `settings.json` und `vorlagen.json`. Gespeichert wird sofort und atomar; eine Sperrdatei verhindert zwei schreibende Instanzen. Die Datei trägt eine Formatnummer (`version`, derzeit 26): Ältere Glide-Fassungen öffnen neuere Bestände nur schreibgeschützt, neuere Fassungen sichern einen älteren Bestand vor der Umstellung. **Ein Agent schreibt nie in diese Dateien**, auch nicht lesend-ändernd; dafür gibt es die Importwege.

## Importwege und Ausgaben

| Weg | Datei | Menü in Glide |
|---|---|---|
| Neue Inhalte | `.glideexchange` | Datei › Datenaustausch › „KI-Ergebnis importieren …“ |
| Seite | `.md`, `.markdown`, `.txt` | Datei › Importieren › „Seite aus Datei …“ oder „Seite aus Zwischenablage“ |
| Vorhandenes ändern | Kontextpaket `.glidecontext` → Änderungsvorschlag | „Für KI bereitstellen …“, Antwort über „KI-Ergebnis importieren …“ |
| Weitere Importe | CSV, Kalenderdatei (ICS), TXT, Notion-Export, Zeichnung (SVG/JSON), `.glidepage` | Datei › Importieren |
| Ausgaben | Markdown, CSV, TXT, ICS, Druck/PDF, JSON Canvas, Markdown-Gesamtausgabe | Datei › Exportieren |
| Sicherungen | `.glidebackup`, `.glideapp` | Datei › Sicherung – nur Glide selbst schreibt sie |

„Austauschformat anzeigen …“ zeigt die Formatbeschreibung der installierten Glide-Fassung; sie ist die Grundlage dieses Skills.

## Für die Arbeit am Glide-Quellcode

Im Repository `n05a-design/glide-to-do` (Quellbaum `01_Repository/Glide`):

- Austauschweg: `src/glide/app.pyw` (Abschnitt „Glide-Austauschformat“, `parse_exchange_document`, `apply_exchange_payload`), `src/glide/exchange_patch.py`, `src/glide/page_markdown.py`, `src/glide/drawing.py`.
- Datenvertrag und Formatstufen: `docs/06_DATA_BACKUP_MIGRATION.md`; Verhalten: `docs/20_FUNKTIONEN.md`; Modulregister: `src/glide/README.md`.
- Kopplung: `tests/tools/test_agenten_skill.py` vergleicht `abdeckung.json` mit den Feldern, Arten und Fähigkeiten im Code. Ändert sich das Datenformat oder der Austauschweg, schlägt die Prüfung fehl, bis Skill, Referenzen und Beispiele nachgezogen sind.
- Darstellung: `tests/tools/ki_ausgabe.py` prüft eine KI-Ausgabe mit dem echten Glide-Code; `--oberflaeche` legt sie in einer echten Glide-Instanz an, startet neu und liest die Anzeige ab. Die Vollprüfung führt das als `test_ki_ausgabe_darstellung.py` aus.
