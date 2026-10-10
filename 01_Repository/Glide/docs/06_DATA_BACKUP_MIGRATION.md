# Daten, Backups und Migration – Glide

Stand 10.10.2026 · Glide 3.37.0 · Aufgabenformat 23 · Einstellungen 2 · Vorlagen 2 · Austauschformat 1 (Änderungsvorschläge 2)

Verbindlicher Datenvertrag. Am 03.10.2026 um das Austauschformat (bisher Vertrag 52) ergänzt und um die Verweise auf gelöschte Einzelverträge bereinigt; die Vorfassungen trägt Git. Formate 4–23 und Legacy 2 bleiben lesbar.

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

## Format 23

Seit 3.33.18 tragen Seiten optional `live_lists` (höchstens 20 eindeutige `glide://list/<id>`-Ziele) und `cover`. Die Live-Liste ist eine abgeleitete Ansicht der Originalaufgaben samt Unteraufgaben; sie erzeugt keine Kopien und kann nicht rekursiv andere Live-Listen erweitern. Fehlende und gelöschte Ziele behalten ihre Kennung. Archivierte Quelllisten, auch unter archivierten Ordnern, bleiben sichtbar und werden nicht verändert.

Ein Titelbild ist `{"kind":"image","attachment":"<id>"}` für einen lokalen Anhang derselben Seite oder `{"kind":"drawing","document":<glide.drawing>}` für eine unabhängige Pixelzeichnung. Keine externen Bild-URLs. Ungültige Werte werden abgewiesen; ein fehlender Bildanhang zeigt einen Platzhalter. Die Anhangskennung folgt beim Import genau einmal ihrer neuen Kennung, Live-Listen folgen der gemeinsamen Containerzuordnung. Papierkorb, Wiederherstellung, Kopie, Sicherung und Undo erhalten beide Felder; der Vergleich für Verlauf/Aktivität berücksichtigt Änderungen.

Vor dem ersten Schreiben von Format 23 wird die alte Datei bytegenau nach `liste_vor_format23_*.json` kopiert. Ein Kopierfehler verhindert das Überschreiben. Die unveränderte 3.33.17 (Format 22) erkennt den neuen Bestand und öffnet schreibgeschützt; Start- und Speicherprobe prüfen dieselben Dateibytes. Referenz-Fixture: `tests/fixtures/current_v23/reference_v23.json`. Einstellungen 2 und Vorlagenformat 2 bleiben erhalten; enthaltene Vorlagen-Backups tragen Format 23.

## Format 22

Seit 3.33.17 erweitert Format 22 den Bestand um typisierte lokale Beziehungen. Listen und Aufgaben tragen optional `references`, höchstens 200 eindeutige lokale URLs `glide://list/<id>` oder `glide://item/<id>`. Kennungen sind URL-kodiert; die Namensräume bleiben getrennt. Notiz-/Seitentext verwendet dieselben Ziele in den vorhandenen `rich_note.links` und aktiven Linkspannen. Ungültige Typen, URLs oder Mengen werden beim Laden/Import abgewiesen; fehlende Ziele bleiben als gültige Kennungen erhalten. Rückverweise sind eine abgeleitete Sicht.

Vor dem ersten Schreiben entsteht eine bytegenaue `liste_vor_format22_*.json`-Kopie. Kopierfehler verhindert das Überschreiben. Die unveränderte Vorversion 3.33.16 (Format 21) erkennt Format 22 und öffnet schreibgeschützt; eine tatsächliche Start-/Speicherprobe prüft unveränderte Dateibytes. Die Wochenplanung verwendet vorhandene Felder `planned_date`, `planned_time` und `estimated_minutes`; Einstellungen, Vorlagen und Austausch bleiben unverändert. Referenz: `tests/fixtures/current_v22/reference_v22.json`.

Additiver Import und Vorlagenkopie remappen enthaltene Listen- und Aufgabenkennungen getrennt, auch in Textlinks; externe Ziele bleiben unverändert. Listen-/Aufgabenkopien und Papierkorbwiederherstellung erhalten die Beziehungen, Undo/Redo kann die Objekte ersetzen; der Graph wird dann neu berechnet. Markdown importiert/exportiert interne Links mit denselben URLs.

## Format 21

Seit 3.33.15 schützt Format 21 Aufgaben im Notiztext und Textverweise. `item:<id>` bindet eine Heimatzeile; `taskref:<id>` verweist auf eine Aufgabe mit derselben Kennung an einem anderen Heimatort. Die Heimat bleibt ausschließlich in `lists[].items`/`children`. Beim Übernehmen in eine Aufgabenliste wechseln die zugehörigen Heimatmarken zu Textverweisen. Mehrere Verweiszeilen kopieren keine Aufgabe. Papierkorb- und fehlende Ziele behalten ihre Kennung; Laden erzeugt keinen Ersatzpunkt. Nur das Rückgängigmachen einer tatsächlich entfernten Heimatzeile stellt deren Aufgabe wieder her.

Der bestehende Startmigrationsweg schreibt den Bestand erst nach erfolgreicher bytegenauer `liste_vor_format21_*.json`-Sicherung. Scheitert die Kopie, bleibt die alte Datei unverändert. 3.33.14 erkennt den neueren Bestand und sperrt Schreiben. Referenz-Fixture: `tests/fixtures/current_v21/reference_v21.json`. Einstellungen bleiben Format 2; gespeicherte Filter ergänzen additiv `source` (`all`/`pages`). Allgemeine Dokumentverweise G08/G30 verwenden seit 3.33.17 die eigene Formatstufe 22.

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

**Regel seit 29.09.2026:** Jede weitere Listen- oder Ordnerart hebt die Formatnummer. Nur so erkennt eine ältere Fassung den Bestand als neuer und öffnet ihn schreibgeschützt, statt ihn zu überschreiben. Format 21 ist seit 3.33.15 für Aufgaben-Textverweise angehoben; spätere inkompatible Inhalte benötigen erneut eine Formatstufe.

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
| 21 | 3.33.15 | Aufgaben im Notiztext, stabile Textverweise `taskref:<id>` und Heimatwechsel | 3.33.14 und ältere Format-20-Leser öffnen schreibgeschützt |
| 22 | 3.33.17 | Typisierte lokale Listen-/Aufgabenbeziehungen und Textlinks, abgeleitete Rückverweise | 3.33.16 und ältere Format-21-Leser öffnen schreibgeschützt |
| 23 | 3.33.18 | Live-Listen und Titelbilder in Seiten | 3.33.17 und ältere Format-22-Leser öffnen schreibgeschützt |

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
- Nie rotiert: `liste_vor_format*`, `liste_unlesbar_*`, `liste_vor_titelkuerzung_*`, `vor_import_*.glidebackup`, `vor_vorschlag_*.glidebackup` (3.35.0), `settings_vor_restore_*.json`, `vorlagen_vor_restore_*.json`.

## Backups und Transportwege

- **`.glidebackup`** ist ein ZIP aus `data.json` und den referenzierten Anhängen. Archivpfade, Größen, Symlinks, doppelte Namen und Kompressionsverhältnisse werden geprüft. Portable Backups werden ab Format 4 gelesen.
- **Komplettbackup laden** ersetzt erst nach Validierung und Sicherung (`vor_import_*.glidebackup`). **Teilbackup / Listen und Ordner hinzufügen** importiert additiv mit neuen Kennungen, vollständige Zweige einschließlich leerer Unterordner; Verweise (`links`, `blocked_by`, `references`, interne Textlinks, `item:<id>`, Bildanhänge, Zeichnungsreferenzen) ziehen nach.
- **App-Backup** = Komplettbackup plus Abschnitt `app_backup` (`format_version`, `settings` ohne Tageshistorien, `templates`, `activity`); für ältere Fassungen bleibt es ein gültiges Aufgabenbackup. Wiederherstellen mit Inhaltsvorschau und wählbaren Bereichen. Pinnwände reisen mit und werden beim Import neu zugeordnet.
- **`.glidepage`:** Teilbackup nur mit Seiten und Büchern (`"content": "pages"`); eine Datei mit Listen weist der Seitenimport ab.
- **Vorlagenkatalog** `.glidetemplates` (Vorlagenformat 2) mit portablen Anhängen.
- Benannte Zwischenstände einer Zeichnung sind Anhänge (MIME `application/vnd.glide.drawing-snapshot+json`, höchstens 10).
- **Ausgaben** (Druck-HTML, ICS, CSV, Markdown) schreiben atomar an ein gewähltes Ziel; Nutzdatendateien sind als Ziel ausgeschlossen. Sie erzeugen keinen Verlaufseintrag.
- **Importe** (CSV, ICS, Markdown, Austausch) lesen nur die gewählte Datei, erzeugen Punkte über `new_item` und sind ein Rückgängig-Schritt einschließlich neuer Labels; bestehende Punkte werden nie überschrieben. Einzige Ausnahme ist der geprüfte Änderungsvorschlag (Stufe 2 des Austauschformats).
- **Sicherungen vergleichen** (3.35.0, F-03): Datei › Sicherung › „Sicherungen vergleichen …“ liest zwei Stände – den aktuellen Bestand, eine automatische Sicherung oder eine gewählte `.glidebackup`/`.json` – mit den Grenzen des Imports und zeigt Listen und Aufgaben neu, entfernt, verschoben und geändert mit Feldern (`backup_diff.py`, Tk-frei). Nur lesend: keine Datei wird geschrieben, nichts wiederhergestellt. Eigene ICS-UIDs werden erkannt, damit der Rundlauf keine Kopien anlegt.

## Einstellungen

Einstellungsformat **2**; alle neuen Schlüssel sind additiv und werden beim Laden normalisiert, fehlende Werte ergeben das frühere Verhalten. Persönliche Einstellungen sind nicht Teil eines Aufgabenbackups.

**Fokus seit 3.33.14:** `time_tracking` erhält additiv `focus`, `elapsed_seconds` und `goal_seconds`; `started_at = null` bedeutet Pause. `time_booking` enthält die Aufgabenkennung und erfasste Minuten vor/nach einer vorbereiteten Buchung. Ablauf und Fehlerwiederholung stehen in [Architektur](02_ARCHITECTURE.md#2-nutzdaten-und-speicherweg). Aufgabenformat 20 und Einstellungsformat 2 bleiben erhalten. Die alte Normalisierung in 3.33.13 entfernt die Fokuszusatzfelder und verwirft pausierte Timer; solche Fassungen dürfen einen laufenden oder noch ungeklärten Fokusbestand daher nur in getrennter Testablage öffnen. Vor einem Versionsrückwechsel Fokus in 3.33.14 vollständig buchen und beenden; offene Buchungsnachweise zuerst klären.

| Bereich | Schlüssel (Auswahl) |
|---|---|
| Erscheinung | `design` (aus `theme`, `color_mode`, `glass_mode` abgeleitet und als Spiegelwerte zurückgeschrieben; Unbekanntes → `glass_dark`), `design_auto` (Designpaar `light`/`dark` für „Automatisch hell/dunkel“, 3.33.21; Unlesbares → aus), `backdrops` je Design, `animations_enabled` |
| Navigation | `sidebar_visible`, `sidebar_narrow` (schmale Seitenleiste, 3.33.21), `sidebar_sections_closed`, `label_sections_closed`, `sidebar_locations` (gerätespezifische Bereichszuordnung), `startup_view`, `startup_list_id` |
| Ansichten | `list_detail_mode`, `table_columns`, `table_column_widths`, `saved_filters`, `daily_capacity_minutes` (0–1.440, 0 = kein Vergleich), `today_routines` (≤ 20 Listenkennungen) und `routine_done_days` (Kennung → ISO-Tag) für Routinen in „Heute“ (3.33.20), `recent_labels`/`recent_move_targets` (je ≤ 5, 3.33.20) |
| Startseite | `home_tile_order`, `home_tile_span`, `home_columns`, `home_density`, `home_calendar_mode`, `home_filter_tiles`, `mascot_name`, Gismo-Werte |
| Pinnwände | `pinboards` je Pinnwand: Karten mit Positionen und Größe, Anordnung, Spaltenboard, Bereiche (≤ 50), Verbindungen (≤ `MAX_CONNECTIONS` = 200, mit Art, Beschriftung, Strichart, Farbe), Hintergrund, Vorschau, Auto-Anheften. Verweise auf entfernte Karten fallen beim Normalisieren weg; ältere Fassungen lesen die Pinnwand als freie Fläche |
| Sonstiges | `system_notifications` (Vorgabe aus), `data_format_written`, `today_plan_migrated`, `release_notes_seen` (zuletzt gelesene Karte „Neu in …“, 3.33.20; Unlesbares entfällt) |

## Austauschformat (`.glideexchange`)

Transportformat für fremde Systeme und KI, **kein Speicherformat**. Zwei getrennte Zahlen: `DATA_SCHEMA_VERSION` (wie Glide speichert, 23) und `EXCHANGE_FORMAT_VERSION` (worauf sich ein fremdes System verlassen kann, 1). Leitsatz: Die Quelle beschreibt, was entstehen soll; Glide entscheidet, wie es intern gespeichert wird.

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
- **Capabilities** nennen je Fähigkeit eine Stufe (0 = unbekannt). Anhänge, Wiederholungen und Erinnerungen stehen bewusst auf 0; `patch_mode` steht seit 3.35.0 auf 1 (Änderungsvorschläge, unten). Grenzen: `max_items` 5.000, `max_checklist_entries` 50, `max_depth` 12, 12 MB je Datei.
- **Import:** JSON, Formatname, Version und Modus prüfen → Felder, Werte, Verweise prüfen → Vorschau → Bestätigung → ein Rückgängig-Schritt. Unbekannte Felder nennt die Vorschau, der Fokus liegt dann auf „Abbrechen“. Der Import legt ausschließlich Neues an; scheitert das Speichern, gehen Listen, Ordner, Labels und Rückgängig-Stapel exakt zurück.
- **Markdown-Gliederung** als zweite, schwächere Ebene: `# Liste`, `## Abschnitt`, `- Aufgabe`, eingerückte Unterpunkte, `- [ ]` als Checklistenschritt, freier Text als Beschreibung. Ohne Schlüssel und Labels, daher nicht für den Rückweg.
- **Bedienung:** Datei › „Für KI bereitstellen …“ (Export), „KI-Ergebnis importieren …“ (`.glideexchange`, `.json`, `.md`), „Austauschformat anzeigen …“ (Anweisung für eine KI, aus den tatsächlichen Konstanten erzeugt).
- **Rundlauf erhält** Ordner, Listen mit Beschreibung, alle vier Punktarten, Unterpunkte bis Ebene 12, Beschreibungen, Labels, Fälligkeit mit Uhrzeit, Bearbeitungstag, Aufwand, Wichtigkeit, Erledigt und Checklisten; **nicht** Anhänge, Wiederholungen, Erinnerungen, Farben je Punkt, Verlauf, Papierkorb, Pinnwandpositionen.

### Stufe 2: Kontextpaket und Änderungsvorschlag (seit 3.35.0, G24)

Vorhandenes ändern, ohne interne Kennungen preiszugeben und ohne still zu überschreiben (Entscheidung Q3: Dokumente statt Schnittstelle). Version 1 bleibt unverändert lesbar; Änderungsvorschläge tragen `format_version` 2.

**Kontextpaket** (`.glidecontext`, „Für KI bereitstellen …“ mit Zweck „Vorhandene Aufgaben überarbeiten lassen“; Umfang aktuelle Liste, Ordner, alles oder die ausgewählten Punkte):

```json
{
  "format": "glide.context", "format_version": 2, "created_at": "…", "application_version": "3.35.0",
  "instructions": "Antworte mit … mode \"patch\" …",
  "fields": ["title", "description", "importance", "due", "due_time", "planned_date", "estimated_minutes", "done", "labels"],
  "lists": [ { "ref": "r-…", "kind": "list", "title": "…", "description": "…" } ],
  "items": [ { "ref": "r-…", "kind": "item", "list": "r-…", "parent": "r-…" | null,
               "base": "…", "fields": { "title": "…", "importance": 2, "due": "JJJJ-MM-TT" | null, "labels": ["Name"], … } } ]
}
```

- `ref` ist `r-` plus die ersten 16 Hexzeichen von SHA-256 über `glide-ref\0<Kennung>`: stabil, aber ohne Rückschluss auf die Kennung. Glide findet die Aufgabe über denselben Verweis wieder.
- `base` ist die Prüfsumme (SHA-256, 16 Zeichen) des kanonischen JSON der neun Austauschfelder – der Ausgangsstand.
- Nur Aufgaben und Langtexte (planbare Punkte); Labels erscheinen mit Namen.

**Änderungsvorschlag** (Antwort, `.glideexchange` oder `.json`):

```json
{ "format": "glide.exchange", "format_version": 2, "mode": "patch",
  "changes": [ { "ref": "r-…", "base": "…", "set": { "due": "2026-10-20", "importance": 3 } } ] }
```

- **Prüfung** (`exchange_patch.py`, Tk-frei): Rahmen, höchstens 5.000 Änderungen, je Feld Typ und Grenzen (Titel 1–500 Zeichen, Beschreibung bis 20.000, Wichtigkeit 0–3, Datum `JJJJ-MM-TT` oder `null`, Uhrzeit `HH:MM` oder `null`, Aufwand 1–10.080 Minuten oder `null`, Erledigt `true`/`false`, Labels als Namen). Je Änderung ein Zustand: anwendbar, ohne Änderung, **Konflikt** (Prüfsumme passt nicht mehr – die Aufgabe wurde seit dem Paket geändert), nicht gefunden (gelöscht, archiviert oder nie im Paket), ungültig (Feld unbekannt, Wert falsch, dieselbe Aufgabe doppelt, Erledigt an einer Wiederholung).
- **Vorschau:** jede Änderung Feld für Feld (alt → neu) mit Zustand; übernommen wird nur Anwendbares. Konflikte werden nie überschrieben.
- **Übernahme:** erst eine Vorsicherung `backups/vor_vorschlag_<Zeitstempel>.glidebackup` (wie `vor_import_*`, nie rotiert), dann alle Änderungen als ein Rückgängig-Schritt über `item_change`. Unbekannte Labelnamen entstehen neu; ohne Fälligkeit bzw. Bearbeitungstag entfällt die zugehörige Uhrzeit. Kennungen, Anhänge, Wiederholungen und Erinnerungen bleiben unberührt.

**Einplanen 3.33.13 (KO01/AU02):** kein Formatwechsel und kein neues Feld. Die gemeinsame Aktion schreibt ausschließlich `planned_date`; „Ohne Tag“ erhält `planned_time`. Fälligkeit/Uhrzeit, Aufwand, Wiederholung, Anhänge und Kennungen bleiben erhalten. Mehrere Quelllisten werden über `item_change` atomar im bisherigen Speicherweg geschrieben, ein Undo nimmt die gesamte Auswahl zurück. Die Kapazitätsvorschau verändert keine Daten. Feldverträge und Bedienung stehen in [Funktionen](20_FUNKTIONEN.md).
