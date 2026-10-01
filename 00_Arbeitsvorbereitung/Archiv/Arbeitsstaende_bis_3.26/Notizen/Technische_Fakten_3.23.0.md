# Technische Fakten – Glide 3.23.0

Stand: 18.09.2026 · Glide 3.23.0 · interner Entwicklungsstand · Aufgabenformat 16 · Einstellungen 2 · Vorlagen 2

3.23.0 ist ein **Konsolidierungs- und Funktionsstand** aus 46 benannten
Punkten. Schwerpunkt ist nicht Menge, sondern Zusammenführung: eine
Designauswahl statt dreier Schalter, eine Tabellenkomponente statt sieben
Einrichtungen, messbar schnellere Ansichtswechsel und ein Austauschformat
neben dem internen Datenformat.

**Kein Formatsprung.** Aufgabenformat bleibt 16, Einstellungsformat 2,
Vorlagenformat 2.

## Was sich am Datenmodell ändert

| Ort | Änderung |
| --- | --- |
| Einstellungen | Neu: `design` – der gewählte Designschlüssel. Ersetzt die Kombination aus `theme`, `color_mode` und `glass_mode` als Quelle. |
| Einstellungen | `theme`, `color_mode` und `glass_mode` bleiben **abgeleitet** erhalten, damit eine ältere Fassung dieselbe Datei richtig liest. Geschrieben nur in `set_design`. |
| Einstellungen | Neu: `list_detail_mode` – Informationsumfang der Listenansicht. |
| Einstellungen | `pinboards` erhält je Pinnwand `connections`: Liste aus `{"from", "to"}` mit Punktkennungen. |
| Aufgaben | unverändert. |

Alle neuen Einstellungsfelder sind additiv; eine Datei aus 3.22 bleibt gültig.

## Migration

| Schritt | Verhalten |
| --- | --- |
| `theme` + `color_mode` + `glass_mode` → `design` | Einmalig beim Lesen der Einstellungen, vollständig und ohne Verlust. Sieben Ausgangszustände, sieben Ziele; die Zuordnung steht in `docs/50_DESIGNSYSTEM_3.23.0.md`. |
| Ungültiges `design` | Fällt auf `glass_dark` zurück. |
| Verbindungen ohne Karte | Werden beim Normalisieren verworfen: Eine Verbindung braucht zwei vorhandene Karten. |
| Entfallene Kachel `due` | Fällt aus `home_tile_order` und `home_tiles_hidden`, weil sie nicht mehr in `HOME_TILE_KEYS` steht. `today` bleibt sichtbar. |
| Rückwechsel auf 3.22 | Möglich: Das Aufgabenformat ist unverändert, und die abgeleiteten Einstellungswerte stehen weiterhin in der Datei. Verbindungen und `list_detail_mode` ignoriert 3.22. |

## Neue Konstanten und Grenzen

| Grenze | Wert | Konstante |
| --- | --- | --- |
| Designs | 7 | `DESIGNS`, `DESIGN_ORDER` |
| Vorgabedesign | `glass_dark` | `DESIGN_DEFAULT` |
| Verbindungen je Pinnwand | 200 | `ItemWorkspace.MAX_CONNECTIONS` |
| Detailzeilen je Punkt | 12 | `MAX_DETAIL_ROWS_PER_ITEM` |
| Anzeigemodi | 5 | `LIST_DETAIL_MODES` |
| Austauschformat | Version 1 | `EXCHANGE_FORMAT_VERSION` |
| Punkte je Austauschdatei | 5000 | `MAX_EXCHANGE_ITEMS` |
| Ebenen je Austauschdatei | 12 | `MAX_EXCHANGE_DEPTH` |
| Größe je Austauschdatei | 12 MB | `MAX_EXCHANGE_BYTES` |
| Kachelmindestbreite Startseite | 300 px | `HOME_TILE_MIN_WIDTH` |
| Zweispaltig ab | 616 px | `HOME_TWO_COLUMN_WIDTH` (abgeleitet) |
| Dreispaltig ab | 932 px | `HOME_THREE_COLUMN_WIDTH` (abgeleitet) |
| Kopfzeile: volle Dichte ab | 1120 px | `HEADER_DENSITY_FULL` |
| Kopfzeile: kompakt ab | 900 px | `HEADER_DENSITY_COMPACT` |
| Aktionsreihen vollständig ab | 700 px | `ACTION_DENSITY_MIN_WIDTH` |
| Uhrzeit neben dem Datum ab | 380 px | `DueField.MIN_INLINE_TIME_WIDTH` |
| Spaltenumbruch der Punktmaske unter | 684 px | `ResponsiveColumns` (2 × 330 + 24) |
| Mindestkontrast Schrift auf Fläche | 4,5 : 1 | `ensure_contrast` |

## Neue gemeinsame Bausteine

| Baustein | Zweck |
| --- | --- |
| `DESIGNS` | Registry der Erscheinung; ein neues Design ist eine Zeile |
| `render_pass()` / `render_cached()` | Kennzahlen einmal je Aufbau |
| `_parse_iso_date()` | Datumsprüfung mit `lru_cache` |
| `prepare_table()` | einheitliche Tabellenspalten |
| `ResponsiveColumns` | zweispaltige Masken mit Umbruch |
| `attach_calendar_picker()` | Kalender an jedem Datumsfeld |
| `dialog_label()` | linksbündige Dialogbeschriftung für `ListApp` |
| `contrast_ratio()`, `readable_text_color()`, `ensure_contrast()` | Kontrast als Rechnung |
| `pack_relative()` | Packen ohne Abbruch bei fehlendem Bezug |
| `build_exchange_payload()` / `parse_exchange_document()` / `apply_exchange_payload()` | Austauschformat |

## Leistung

Gemessen über 1.584 Punkte in zwölf Listen und sechs Ordnern, je zwanzig
Ansichtswechsel unter `cProfile`:

| Größe | 3.22 | 3.23 |
| --- | --- | --- |
| Ansichtswechsel | 336 ms | **129 ms** |
| Funktionsaufrufe | 13,2 Mio | **4,6 Mio** |
| `update_sidebar_list` | 272 ms | 61 ms |
| `content_column_widths` | 164 ms | 24 ms |

Drei Ursachen: wiederholtes `strptime` auf denselben Zeichenketten, mehrfacher
vollständiger Bestandsdurchlauf je Ansichtswechsel, Textbreitenmessung je
Zeile. Alle drei behoben, keine Ladeanimation ergänzt.

## Prüfstand

| Größe | Wert |
| --- | --- |
| Integrationssuiten | 27 (neu: `test_features323.py`) |
| Analysen | 4 (neu: `attributpruefung.py`) |
| Zeilen in `app.pyw` | rund 29.900 |
| Umgebung der Vorabprüfung | Linux, Python 3.12.3, Tk 8.6, Xvfb, TZ Europe/Berlin |
| Maßgeblicher Lauf | Windows, Python 3.12.10, 18.09.2026 – alle Suiten, Analysen, Abgleiche und Bilder |

In der Linux-Vorabumgebung laufen zwei Schritte nicht: die
Dokumentationsprüfung (rund 400 historische Archivdateien liegen dort nicht
vor) und die Screenshot-Erzeugung. Beide sind im Windows-Lauf am Arbeitsgerät
bestanden.

Der Windows-Lauf brachte fünf Befunde, die eine Linux-Vorabumgebung nicht
zeigen kann: `TZ` wird dort nicht ausgewertet und erzeugt eine Zone ohne
Sommerzeitregel; die Textanhänge der Beispieldaten entstanden mit CRLF und
machten den Abgleich unerreichbar; sechs Linkziele waren tot; eine Suite
scheiterte am fehlenden Systemfokus statt an der Anwendung; dreizehn
Standangaben der äußeren Ablage standen auf der Vorversion. Alle behoben,
Einzelheiten im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md).

## Offen

Sichtabnahme auf Windows und macOS · DPI- und Mehrmonitorprofile ·
Screenreader · Langzeitbetrieb · Installer und Signierung ·
Endnutzer-Einstieg beim ersten Start.
