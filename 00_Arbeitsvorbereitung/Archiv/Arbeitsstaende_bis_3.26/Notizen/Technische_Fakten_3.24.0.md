# Technische Fakten – Glide 3.24.0

Stand: 19.09.2026 · Glide 3.24.0 · interner Entwicklungsstand · Aufgabenformat 16 · Einstellungen 2 · Vorlagen 2

3.24.0 beantwortet zwanzig benannte Punkte. Schwerpunkt sind zwei Fragen: Wie
viel muss eine Seitenleiste zeigen, damit man sich zurechtfindet – und was
fehlt der Pinnwand, um mehr zu sein als eine Ablage für Zettel.

**Kein Formatsprung.** Aufgabenformat bleibt 16, Einstellungsformat 2,
Vorlagenformat 2.

## Was sich am Datenmodell ändert

| Ort | Änderung |
| --- | --- |
| Einstellungen | `pinboards[*].cards[*].scale` – Kartenmaßstab `large`/`normal`/`small`. Fehlt der Wert, gilt `normal`. |
| Einstellungen | `pinboards[*].connections[*].style` – Verbindungsart `line`/`forward`/`backward`/`both`. Unbekannt fällt auf `line` zurück; die Verbindung bleibt. |
| Einstellungen | `pinboards[*].connection_style` – die Art, die für die nächste Verbindung dieser Fläche gilt. |
| Einstellungen | Neuer Bereichsschlüssel `pinboards["global"]` neben `list:<id>` und `folder:<id>`. |
| Einstellungen | Neu: `startup_list_id`, `animations_enabled`, `home_calendar_mode`, `home_density`. |
| Backup | **Neu:** `complete_backup_payload()` trägt einen Abschnitt `pinboards` neben den Aufgabenfeldern. |
| Aufgaben | unverändert. |

Alle neuen Einstellungsfelder sind additiv; eine Datei aus 3.23 bleibt gültig.

## Die Richtung einer Verbindung

Bis 3.23 war eine Verbindung ungerichtet und wurde als **sortiertes** Paar
gespeichert. Seit 3.24 bleibt die Reihenfolge von `from`/`to` so, wie sie
gesetzt wurde – sie ist bei einem Pfeil die Aussage selbst. Doppelt bleibt eine
Verbindung trotzdem ausgeschlossen: Geprüft wird weiterhin über das
ungeordnete Paar, zwischen zwei Karten liegt höchstens eine Linie.

Für eine Datei aus 3.23 ändert sich dadurch nichts: Ihre Paare sind sortiert
und tragen nach dem Normalisieren die Art `line`.

## Die Anordnung im Backup

| Weg | Verhalten |
| --- | --- |
| Komplettbackup schreiben | `pinboards` wird aus den persönlichen Einstellungen übernommen. |
| Vollständiger Import | Die Anordnung wird unverändert übernommen; Kennungen bleiben gleich. |
| Listen/Ordner hinzufügen | Container- und Punktkennungen werden neu vergeben; `pinboards_from_backup` zieht Karten und Verbindungen über die Zuordnungen aus `prepare_additive_import` nach. Nicht zuordenbares fällt weg. |
| Globale Pinnwand beim additiven Import | wird **nicht** übernommen – sonst bliebe offen, welche von beiden gilt. |
| Ältere Glide-Fassung liest die Datei | übergeht den Abschnitt; Aufgabenformat bleibt 16. |

`copy_items_with_new_ids(items, mapping=None)` füllt auf Wunsch eine Zuordnung
alt → neu. `prepare_additive_import` legt beide Zuordnungen unter
`self._additive_import_maps` ab; die Rückgabe ist unverändert.

## Neue oder geänderte Methoden

| Methode | Zweck |
| --- | --- |
| `ItemWorkspace.active_ids()` | Worauf eine Aktion der Arbeitsfläche wirkt – Mehrfachauswahl auf der Pinnwand, der eine Punkt im Reiter. |
| `ItemWorkspace.selection()` / `select_card(identity, additive)` | geordnete Mehrfachauswahl; eine von außen gesetzte `selected_id` ersetzt sie. |
| `ItemWorkspace.board_action_groups()` | die drei Aktionsgruppen an einer Stelle. |
| `ItemWorkspace.set_card_scale(key)` | Maßstab der ausgewählten Karten. |
| `ListApp.open_global_board()` / `GLOBAL_BOARD_VIEW` | die Fläche über den gesamten Bestand. |
| `ListApp.open_inbox_list()` | der Weg zum Eingang ohne Seitenleistenzeile. |
| `ListApp.show_option_panel(...)` | Auswahlfläche im App-Stil; trägt „Anzeige“. |
| `ListApp.apply_startup_view()` | acht Ziele für die Ansicht beim Öffnen. |
| `ListApp.arcade_mode()` | getrennt von `animations_enabled()`: Rückmeldung ja/nein gegen darf-übertreiben. |
| `ResponsiveColumns.required_width(...)` | Fensterbreite aus der Spaltenschwelle statt geraten. |

## Was der Prüfstand dazu prüft

`tests/integration/test_features324.py` – 28. Suite. Nachgewiesen werden
Seitenleiste und Abschnitte, der Abstand des Zahnrads nach einem erzwungenen
Dichtewechsel, Mehrfachauswahl, Verbindungsarten samt Normalisierung und
Druck, Kartenmaßstab, Vollbild mit Packreihenfolge vor und nach dem Rückweg,
`pinboards_from_backup` in beiden Importwegen, die globale Fläche, die
Anzeigefläche, die Startansicht, `required_width` sowie Rückmeldung, Kombo und
Dopamin-Kontrast.
