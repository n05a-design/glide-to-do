# Technische Fakten – Glide 3.22.0

Stand: 17.09.2026 · Glide 3.22.0 · interner Entwicklungsstand · Aufgabenformat 16 · Einstellungen 2 · Vorlagen 2

3.22.0 ist ein **Funktionsstand**. Er entstand aus einer Sichtprüfung mit
zwanzig benannten Punkten – vier Umbauten und sechzehn Nachbesserungen.
Zum ersten Mal seit 3.19 steigt das Aufgabenformat wieder, von 15 auf **16**.

## Was sich am Datenmodell ändert

| Ort | Änderung |
| --- | --- |
| Punkt | Neues additives Feld `checklist`: Liste aus `{"id", "text", "done"}`, höchstens 50 Einträge, je 200 Zeichen. Gliederung trägt immer `[]`. |
| Punkt | `planned_date` trägt jetzt allein „Mein Tag“. Das Feld selbst ist unverändert. |
| Einstellungen | Neu: `today_plan_migrated`, `table_column_widths`, `table_sort`, `home_tile_order`, `home_tiles_hidden`, `home_columns`, `color_mode`. |
| Einstellungen | `pinboards` erhält je Pinnwand `preview` und `auto`; `layout` hat den neuen Standard `free`. |
| Einstellungen | `today_plan` entfällt nach der einmaligen Migration. |

Einstellungsformat bleibt **2**, Vorlagenformat bleibt **2**. Alle neuen
Einstellungsfelder sind additiv; eine Datei aus 3.21 bleibt gültig.

## Migration

| Schritt | Verhalten |
| --- | --- |
| Format 15 → 16 | Beim Laden erhält jeder Punkt ein leeres `checklist`. Vor dem ersten Speichern in Format 16 entsteht `backups/liste_vor_format16_<Zeitstempel>.json` – unverändert und unrotiert. Bei Fehler wird nicht gespeichert. |
| `today_plan` → `planned_date` | Einmalig beim ersten Start. Jeder Punkt, der an diesem Kalendertag in der Auswahl stand und noch keinen Bearbeitungstag trägt, bekommt den heutigen. Danach `today_plan_migrated = true`. Eine Auswahl von gestern war schon in 3.21 verfallen. |
| Rückwechsel | Glide bis 3.21 kann Format 16 nicht lesen. Der Rückweg führt über die Originalkopie in `backups/`; sie enthält keine späteren Änderungen. |

Lesbar bleiben die Formate **4 bis 16** sowie Legacy 2.

## Grenzen im Code

| Grenze | Wert | Konstante |
| --- | --- | --- |
| Checklistenschritte je Punkt | 50 | `MAX_CHECKLIST_ENTRIES` |
| Zeichen je Schritt | 200 | `MAX_CHECKLIST_TEXT` |
| Tabellenspaltenbreite | 60 bis 1200 px | `TABLE_COLUMN_MIN_WIDTH`, `TABLE_COLUMN_MAX_WIDTH` |
| Eingangsblock in „Mein Tag“ | 50 sichtbare Zeilen | `PLAN_INBOX_VISIBLE` |
| Bildvorschauen je Pinnwandaufbau | 60 | `ItemWorkspace.PREVIEW_LIMIT` |
| Karten je Pinnwand | 500 (unverändert) | `ItemWorkspace.MAX_CARDS` |

## Was die Oberfläche technisch anders macht

- **`ThemedAutoScrollbar` kann waagerecht** (`orient="horizontal"`). Die
  Pinnwand war die letzte Fläche mit einer nativen `ttk.Scrollbar`.
- **Kein Vollaufbau mehr bei Pinnwandaktionen.** Verschieben, Einstellungen und
  Kartenauswahl zeichnen nur noch die Pinnwand. Beim Ziehen bewegt
  `canvas.move` die getaggten Elemente der Karte statt ein Vorschaurechteck
  neu zu zeichnen.
- **Knopf 2 gehört nur unter macOS dem Kontextmenü.** Dort meldet Tk den
  Rechtsklick so; unter Windows und Linux ist es das Mausrad. `bind_drag_scroll`
  und `bind_horizontal_wheel` hängen an Baum, Seitenleiste, Startseite und
  Pinnwand.
- **`active_theme()` ist der einzige Ort für den Farbmodus.** `CONTRAST_THEMES`
  und `DOPAMINE_THEME` überschreiben Rollen des Grundthemes; die Glasoptik
  entfällt in beiden Modi unabhängig von der Einstellung.
- **Die Startseite baut nur bei Spaltenwechsel neu auf**, nicht bei jeder
  Pixeländerung der Breite.

## Prüfstand

- **26 Suiten** (neu: `tests/integration/test_features322.py`),
  drei Analysen, Vorprüfungen, Beispiel- und Releaseabgleich.
- Neu erzeugt für Format 16: Vorlagenkatalog, Beispieldaten, Releaseplanung
  `glide_releaseplanung_3.22.0.glidebackup`, Referenzformat
  `tests/fixtures/current_v16/reference_v16.json`.
- `tests/tools/pruefen.py` kennt die Formatstufe der Releaseplanungen bis
  3.21.4 (15) getrennt von der aktuellen (16).
- Linux-Vorablauf mit Python 3.12.3 und Tk 8.6 unter Xvfb: alle 26 Suiten,
  drei Analysen und beide Reproduktionsabgleiche mit Exitcode 0.

## Was offen bleibt

| Offen | Warum nur am Gerät prüfbar |
| --- | --- |
| Maßgeblicher Lauf auf macOS oder Windows | Plattformabnahme |
| Ziehen mit gedrücktem Mausrad | Echte Maus, echte Zeigerdarstellung |
| Shift + Rad quer | Plattformabhängige Radereignisse |
| Bildvorschau auf Karten | Echte Bildanhänge in der Nutzerablage |
| Beide Farbmodi | Bildschirmlupe, Vorlesefunktion, Kontrastmessung am Gerät |
| Screenshot-Erzeugung und Sichtprüfung | Ausdrücklich manuelle Aufgaben |

[Tagesmodell](../../01_Repository/Glide/docs/46_TAGESMODELL_3.22.0.md) ·
[Checkliste](../../01_Repository/Glide/docs/47_CHECKLISTE_3.22.0.md) ·
[Ansichten und Startseite](../../01_Repository/Glide/docs/48_ANSICHTEN_UND_STARTSEITE_3.22.0.md) ·
[Pinnwand und Darstellung](../../01_Repository/Glide/docs/49_PINNWAND_UND_DARSTELLUNG_3.22.0.md) ·
[Datenvertrag](../../01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md)
