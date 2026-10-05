# Daten, Backups und Migration – Glide

Stand 05.10.2026 · Glide 3.33.8 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2 · Austauschformat 1

Verbindlicher Datenvertrag. Am 03.10.2026 um das Austauschformat (bisher Vertrag 52) ergänzt und um die Verweise auf gelöschte Einzelverträge bereinigt; die Vorfassungen trägt Git. Formate 4–20 und Legacy 2 bleiben lesbar.

## Ablage

| Datei | Inhalt | Transport |
|---|---|---|
| `liste_speicher.json` | Ordner, Listen, Aufgaben, Labels, Wiederholungen, Erinnerungen, Papierkorb, Änderungsverlauf | Aufgabenbackup |
| `settings.json` | Design, Profil, Anzeige, Startseite, Pinnwände (`pinboards`), Bereichszuordnung, Historien | App-Backup oder Datenordnerkopie |
| `vorlagen.json` | System- und eigene Vorlagen | `.glidetemplates`, App-Backup |
| `attachments/` | lokale Kopien der Anhänge | referenzierte Anhänge im Backup |
| `backups/` | automatische Sicherungen und Vorsicherungen | Datenordnerkopie |
| `window.conf`, `glide.lock`, `datenordner.json` | Fenster, Belegung, gerätebezogener Ablagezeiger | nicht übertragen |

- Der Datenordner liegt außerhalb des Programms. `GLIDE_DATA_DIR` hat Vorrang (Tests), sonst Plattformstandard und optional `datenordner.json`. Ein Wechsel kopiert in ein leeres Ziel oder öffnet einen vorhandenen Bestand; die Quelle bleibt.
- `glide.lock` verhindert gleichzeitiges Schreiben zweier Instanzen; erkannte Fremdbelegung verhindert Speichern. Die Sperre ersetzt keinen Synchronisationsdienst.
- Gespeichert wird sofort und atomar (Temporärdatei, `replace_with_retry`; unter Windows bis 1,5 s Warten bei Dateisperren). Liegengebliebene `.glide-json-*.tmp`, älter als zehn Minuten, räumt der Start auf.

## Format 20

Aufgabenformat **20** (seit 3.30.0) bündelt alle bestandsändernden Pakete des Modernisierungskatalogs (E-02).

**Punkte:** `links` (bis 50 Kennungen); `blocked_by` (bis 50, kreisfrei, Kreise löst das Laden auf); `planned_time` (`HH:MM`, nur mit Bearbeitungstag); `time_spent_minutes` (0–1.000.000); `done_at` (beim Abhaken gesetzt, beim Wiederöffnen geleert). Dazu aus früheren Stufen: `due`, `due_time`, `planned_date`, `estimated_minutes` (1–60.000), `importance`, `labels`, `color`, `kind` (`task`, `long`, `group`, `heading`), `checklist` (`{id, text, done}`), `repeat`, `reminder`, `attachments`, `children`.

**Listen und Ordner:** `icon` (Zeichendokument 16 × 16), `archived`, `archived_at`, `recurring_checklist` (nur Aufgabenlisten).

| Feld | Werte |
|---|---|
| `list_kind` | `tasks`, `note`, `drawing`, `page`, `gallery` |
| `folder_kind` | `standard` (Ordner), `library` (Buch), `journal` (Notizbuch); Unbekanntes wird `standard` |
| `rich_note` | `text`, `spans` (`tag`, `start`, `end` als Python-Zeichenpositionen), `links`; Seiten zusätzlich `images` (`{"img:<kennung>": {attachment, mode, width}}`, `mode` `left`/`right`/`center`, Breite 24–4.000 px) und Aufgabenmarken `item:<id>`. Höchstens 1.000.000 Zeichen und 10.000 Bereiche |
| `journal` | `favorite`, `mood` (feste Auswahl), `location`, `moment_date` (ISO), `prompt` |
| `drawing` | Zellmodell `glide.drawing`, Kodierung `hex8-row-v1`, höchstens 256 Farben; Flächen mit 16/32/64 Zellen tragen `format_version` 2, 128 Zellen Version 1 |
| `drawing_reference` | `null` oder Verweis auf einen PNG-Anhang derselben Liste mit Rahmenwerten |

**Regel seit 29.09.2026:** Jede weitere Listen- oder Ordnerart hebt die Formatnummer. Nur so erkennt eine ältere Fassung den Bestand als neuer und öffnet ihn schreibgeschützt, statt ihn zu überschreiben. Das nächste Format (21) wird beim ersten inkompatiblen Inhalt angehoben, etwa Verweise (G08/G30) oder Animation (G17).

Referenz-Fixture: `tests/fixtures/current_v20/reference_v20.json`.

## Formatstufen

| Format | Seit | Ergänzt | Ältere Fassungen |
|---|---|---|---|
| 2 (Legacy), 4–9 | 2.x–2.10 | Grundbestand; 5 Aufgabenfarbe, 6 `kind` (`task`, `group`), 7 `labels` und `trash` | – |
| 10 | 2.11.0 | `due_time`, Papierkorbart `item` | ältere verwerfen Papierkorbeinträge, daher neue Nummer |
| 11 | 3.5.0 | Wiederholungen | – |
| 12 | 3.7.0 | Anhänge an Listen und Ordnern | – |
| 13 | 3.8.0 | Erinnerungen mit Zustellbeleg und Aufschub | – |
| 14 | 3.14.0 | `planned_date`, `estimated_minutes` | ≤ 3.13 können es nicht lesen |
| 15 | 3.19.0 | `history` (Änderungsverlauf, höchstens 15 Einträge und 15 Tage) | ≤ 3.18 |
| 16 | 3.22.0 | `checklist` | ≤ 3.21 |
| 17 | 3.26.0 | `list_kind` (`tasks`, `note`), `rich_note` | ≤ 3.25 |
| 18 | 3.28.0 | `folder_kind`, `journal` | ≤ 3.27 |
| 19 | 3.29.0 | `list_kind` `drawing`, `drawing`, `drawing_reference` | ≤ 3.28 |
| 20 | 3.30.0 | Beziehungen, Zeit, Pixelsymbole, Archiv, Seiten, Galerien, kleine Zeichnungen | ≤ 3.29 und Zwischenstände von 3.30 vor dem 27.09.2026 |

**Glide 3.29 und älter nach der Umstellung nicht mehr starten.** Sie halten einen Format-20-Bestand für beschädigt, beginnen leer und überschreiben ihn bei der ersten Eingabe (nachgewiesen am 25.09.2026 mit einer Kopie eines echten Bestands). Alte Fassungen nur mit getrennter Ablage (`GLIDE_DATA_DIR`) starten.

## Migration und Startprüfung

- **Windows-Dateistand:** Gleich große Überschreibungen können dieselben Dateizeiten behalten. Der Formatcache berücksichtigt daher den vollständigen SHA-256-Inhalt; ein geänderter Formatwert wird auch ohne Metadatenänderung neu gelesen. Unveränderter Inhalt braucht keinen erneuten JSON-Parse.
- **Älteres Format:** wird beim Start umgestellt (`migrate_on_start`), vorher bytegenau und unrotiert gesichert als `backups/liste_vor_format<N>_<Zeitstempel>.json` (`schema_backups.py`). Scheitert die Sicherung, bleibt die Originaldatei unverändert und es wird nicht gespeichert; der nächste Versuch sichert erneut.
- **Neueres Format oder unbekannte Listenart** (`NewerDataError`): öffnet schreibgeschützt mit leerem Bestand und Grund; nichts wird gespeichert.
- **Unlesbare Datei:** erst Kopie `backups/liste_unlesbar_<Zeitstempel>.json`, dann darf ein leerer Bestand sie ersetzen; gelingt die Kopie nicht, bleibt die Sitzung schreibgeschützt.
- **`data_format_written`** merkt das zuletzt geschriebene Format; ist die Datei älter, warnt Glide (eine ältere Version hat gespeichert oder eine ältere Datei wurde hineinkopiert).
- **Titelkürzung:** Container-Titel über 40 Zeichen werden beim Laden gekürzt; vorher `backups/liste_vor_titelkuerzung_<Zeitstempel>.json`. Scheitert die Sicherung, bleiben die Titel.
- Ein beschädigtes Einzelfeld (Checkliste, Verlauf, Ordnerart) fällt auf seinen leeren Wert zurück, statt die Datei unlesbar zu machen.

## Automatische Sicherungen

- `backups/liste_backup_*.json` entsteht nur bei geändertem Inhalt (SHA-256 gegen die neueste Sicherung), geprüft im Fünf-Minuten-Takt und bei jedem Speichern nach mindestens zwei Minuten.
- Aufbewahrung: die zehn neuesten immer, weitere jünger als 30 Minuten, höchstens 40; zusätzlich je Kalendertag der letzte Stand für 14 Tage (`BACKUP_DAILY_DAYS`, zählt nicht gegen die 40).
- Nie rotiert: `liste_vor_format*`, `liste_unlesbar_*`, `liste_vor_titelkuerzung_*`, `vor_import_*.glidebackup`, `settings_vor_restore_*.json`, `vorlagen_vor_restore_*.json`.

## Backups und Transportwege

- **`.glidebackup`** ist ein ZIP aus `data.json` und den referenzierten Anhängen. Archivpfade, Größen, Symlinks, doppelte Namen und Kompressionsverhältnisse werden geprüft. Portable Backups werden ab Format 4 gelesen.
- **Komplettbackup laden** ersetzt erst nach Validierung und Sicherung (`vor_import_*.glidebackup`). **Teilbackup / Listen und Ordner hinzufügen** importiert additiv mit neuen Kennungen, vollständige Zweige einschließlich leerer Unterordner; Verweise (`links`, `blocked_by`, `item:<id>`, Bildanhänge, Zeichnungsreferenzen) ziehen nach.
- **App-Backup** = Komplettbackup plus Abschnitt `app_backup` (`format_version`, `settings` ohne Tageshistorien, `templates`, `activity`); für ältere Fassungen bleibt es ein gültiges Aufgabenbackup. Wiederherstellen mit Inhaltsvorschau und wählbaren Bereichen. Pinnwände reisen mit und werden beim Import neu zugeordnet.
- **`.glidepage`:** Teilbackup nur mit Seiten und Büchern (`"content": "pages"`); eine Datei mit Listen weist der Seitenimport ab.
- **Vorlagenkatalog** `.glidetemplates` (Vorlagenformat 2) mit portablen Anhängen.
- Benannte Zwischenstände einer Zeichnung sind Anhänge (MIME `application/vnd.glide.drawing-snapshot+json`, höchstens 10).
- **Ausgaben** (Druck-HTML, ICS, CSV, Markdown) schreiben atomar an ein gewähltes Ziel; Nutzdatendateien sind als Ziel ausgeschlossen. Sie erzeugen keinen Verlaufseintrag.
- **Importe** (CSV, ICS, Markdown, Austausch) lesen nur die gewählte Datei, erzeugen Punkte über `new_item` und sind ein Rückgängig-Schritt einschließlich neuer Labels; bestehende Punkte werden nie überschrieben. Eigene ICS-UIDs werden erkannt, damit der Rundlauf keine Kopien anlegt.

## Einstellungen

Einstellungsformat **2**; alle neuen Schlüssel sind additiv und werden beim Laden normalisiert, fehlende Werte ergeben das frühere Verhalten. Persönliche Einstellungen sind nicht Teil eines Aufgabenbackups.

| Bereich | Schlüssel (Auswahl) |
|---|---|
| Erscheinung | `design` (aus `theme`, `color_mode`, `glass_mode` abgeleitet und als Spiegelwerte zurückgeschrieben; Unbekanntes → `glass_dark`), `backdrops` je Design, `animations_enabled` |
| Navigation | `sidebar_visible`, `sidebar_sections_closed`, `label_sections_closed`, `sidebar_locations` (gerätespezifische Bereichszuordnung), `startup_view`, `startup_list_id` |
| Ansichten | `list_detail_mode`, `table_columns`, `table_column_widths`, `saved_filters`, `daily_capacity_minutes` (0–1.440, 0 = kein Vergleich) |
| Startseite | `home_tile_order`, `home_tile_span`, `home_columns`, `home_density`, `home_calendar_mode`, `home_filter_tiles`, `mascot_name`, Gismo-Werte |
| Pinnwände | `pinboards` je Pinnwand: Karten mit Positionen und Größe, Anordnung, Spaltenboard, Bereiche (≤ 50), Verbindungen (≤ `MAX_CONNECTIONS` = 200, mit Art, Beschriftung, Strichart, Farbe), Hintergrund, Vorschau, Auto-Anheften. Verweise auf entfernte Karten fallen beim Normalisieren weg; ältere Fassungen lesen die Pinnwand als freie Fläche |
| Sonstiges | `system_notifications` (Vorgabe aus), `data_format_written`, `today_plan_migrated` |

## Austauschformat (`.glideexchange`)

Transportformat für fremde Systeme und KI, **kein Speicherformat**. Zwei getrennte Zahlen: `DATA_SCHEMA_VERSION` (wie Glide speichert, 20) und `EXCHANGE_FORMAT_VERSION` (worauf sich ein fremdes System verlassen kann, 1). Leitsatz: Die Quelle beschreibt, was entstehen soll; Glide entscheidet, wie es intern gespeichert wird.

```json
{
  "format": "glide.exchange",
  "format_version": 1,
  "mode": "create",
  "generator": { "type": "ai" },
  "created_for": { "application": "Glide", "application_version": "…", "data_schema": 20 },
  "capabilities": { "…": "was die erzeugende Fassung kann" },
  "labels":  [ { "key": "label-1", "name": "Release", "color": "accent" } ],
  "folders": [ { "key": "folder-1", "title": "Projekt", "parent": "folder-0" } ],
  "lists":   [ { "key": "list-1", "title": "Titel", "folder": "folder-1",
                 "description": "Wozu diese Liste da ist.", "items": [ … ] } ]
}
```

Ein Punkt: `type` (`task` ausführbare Handlung, `long` textorientierter Arbeitsgegenstand, `group` Behälter ohne Termin, `heading` reine Gliederung), `title`, `description`, `importance`, `due`/`due_time` (bis wann fertig), `planned_date` (wann daran arbeiten), `estimated_minutes`, `labels` (Schlüssel), `done`, `checklist` (Schritte ohne eigene Termine), `children` (eigenständig erledigbare Unterpunkte).

- **Keine internen Kennungen:** Die Datei arbeitet mit frei wählbaren Schlüsseln; echte IDs vergibt Glide beim Import. Eine exportierte Datei enthält keine internen Kennungen.
- **Capabilities** nennen je Fähigkeit eine Stufe (0 = unbekannt). Anhänge, Wiederholungen, Erinnerungen und `patch_mode` stehen bewusst auf 0. Grenzen: `max_items` 5.000, `max_checklist_entries` 50, `max_depth` 12, 12 MB je Datei.
- **Import:** JSON, Formatname, Version und Modus prüfen → Felder, Werte, Verweise prüfen → Vorschau → Bestätigung → ein Rückgängig-Schritt. Unbekannte Felder nennt die Vorschau, der Fokus liegt dann auf „Abbrechen“. Der Import legt ausschließlich Neues an; scheitert das Speichern, gehen Listen, Ordner, Labels und Rückgängig-Stapel exakt zurück.
- **Markdown-Gliederung** als zweite, schwächere Ebene: `# Liste`, `## Abschnitt`, `- Aufgabe`, eingerückte Unterpunkte, `- [ ]` als Checklistenschritt, freier Text als Beschreibung. Ohne Schlüssel und Labels, daher nicht für den Rückweg.
- **Bedienung:** Datei › „Für KI bereitstellen …“ (Export), „KI-Ergebnis importieren …“ (`.glideexchange`, `.json`, `.md`), „Austauschformat anzeigen …“ (Anweisung für eine KI, aus den tatsächlichen Konstanten erzeugt).
- **Rundlauf erhält** Ordner, Listen mit Beschreibung, alle vier Punktarten, Unterpunkte bis Ebene 12, Beschreibungen, Labels, Fälligkeit mit Uhrzeit, Bearbeitungstag, Aufwand, Wichtigkeit, Erledigt und Checklisten; **nicht** Anhänge, Wiederholungen, Erinnerungen, Farben je Punkt, Verlauf, Papierkorb, Pinnwandpositionen.
- **Nächste Stufe** (G24, Plan Stufe 4): `mode: "patch"` mit stabilen Verweisen ohne interne Kennungen, Kontextpaket `.glidecontext`, Anhänge als Verweise mit Prüfsumme.
