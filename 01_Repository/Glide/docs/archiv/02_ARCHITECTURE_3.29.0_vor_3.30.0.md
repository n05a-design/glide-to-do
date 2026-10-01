# Architektur – Glide 3.29.0

Stand 24.09.2026 · Glide 3.29.0 · Aufgabenformat 19

3.29 ergänzt die Listenart `drawing`. `drawing.py` (Zellvertrag, JSON,
Glide-SVG) und `drawing_image.py` (Tk-Bildfunktionen) liegen als Module neben
`app.pyw`, das seinen Ordner dafür an den Anfang von `sys.path` stellt.
`DrawingEditor` ist ein eingebettetes Widget im Inhaltsbereich; `sync_drawing_view`
baut es am Ende jedes `_refresh_tree` auf oder ab und blendet über
`hide_drawing_chrome` Eingabe, Suche und Aufgabenbaum aus. Autosave läuft über
`store_drawing` und `save_items`, Strukturaktionen über `apply_drawing_change`
mit markiertem globalen Snapshot; `snapshot_keeping_drawings` verhindert, dass
ein älterer Rückgängig-Stand Zellstriche mitnimmt. `LIST_KINDS` ist die zentrale
Typregistrierung. [Vertrag](65_ZEICHNUNGSSEITE_3.29.0.md).

3.28 ergänzt `folder_kind` und die normalisierten `journal`-Metadaten auf der
bestehenden Listen-/Ordnerstruktur. `create_journal_entry` nutzt denselben
Mutations-, Speicher-, Verlauf- und Sicherungsweg wie andere Seiten. Gismo
bleibt eine reine Einstellung; Tagebuchinhalt bleibt Teil des portablen
Aufgabenbestands. [Bedienvertrag](59_TAGEBUCH_UND_UI_3.28.0.md).

`src/glide/app.pyw` bleibt der kanonische Python-/Tk-Monolith. `ListApp` koordiniert Daten, Ansichten und Dialoge. Keine neue Laufzeitabhängigkeit.

Änderungen an Aufgaben laufen durch `item_change`, Listen/Ordner durch `sidebar_change`; strukturelle Umbauten zusätzlich durch `guarded_structural_change`. Modale Dialoge verwenden `run_modal` und geben bestehende Grabs zurück. Import und Restore behalten ihre transaktionalen Prüf-/Stagingpfade.

`AppOptionMenu`, `OptionRows`, `LabelDropdown` und `DropdownPopup` teilen seit 3.9 die Auswahlbedienung auf allen Plattformen. Popups sind eingebettete Frames, ohne `Toplevel` und ohne `grab_set`. Die temporäre Ereignisbindung wird bei jedem Schließen entfernt. Datenvariablen und Menüaufrufe bleiben kompatibel; `MacOptionMenu` ist ein interner Alias. Details: [UI-Vertrag](archiv/32_UI_UND_BEDIENUNG_3.9.0.md).

`app_action_entries` liest die vorhandenen Menüs rekursiv. `show_actions_dialog` stellt sie durchsuchbar dar, `invoke_app_action` führt denselben Befehl nach Schließen aus und erhält den vorherigen Textfokus. `_apply_sidebar_visibility` gibt die gesamte Inhaltsbreite frei. Die Sichtbarkeit wird additiv in Einstellungen gespeichert.

`ButtonFlow` ordnet vollständige Aktionen in passende Zeilen. `RoundedContainer` folgt auf Wunsch der Inhaltshöhe. `SystemNavigation` bewahrt den nativen Treeview-Vertrag. Startseite, Vorlagen und Bestandsübersicht teilen den scrollbaren Canvas; Aktionsleisten sind feste Geschwisterbereiche. Vorlagen verwenden `TemplateDraft` zur isolierten Bearbeitung. Private Schriftregistrierung läuft über GDI/CoreText.

Seit 3.23.0 tragen Design, Farbmodus und Dopamin-Modus **eine** Auswahl. `DESIGNS` beschreibt jedes Design durch Grundmodus (`base`), optionale Farbschicht (`layer`), Glasflag (`glass`) und Partnerdesign für den Schnellwechsel; `DESIGN_ORDER` bestimmt die Reihenfolge in der Oberfläche, `DESIGN_SWATCH` die Vorschaufarbe. `set_design`, `design_info`, `glass_enabled` und `color_mode` lesen ausschließlich aus dieser Tabelle; `active_theme` baut daraus die Farbwerte und setzt `glass_gradient`. Ein neues Design ist damit ein Tabelleneintrag, kein Sonderfall im Code. Bestehende Einstellungen mit `theme`, `color_mode` und `glass_mode` werden beim Laden zu `design` zusammengeführt und als abgeleitete Spiegelwerte zurückgeschrieben, sodass ältere Fassungen dieselbe Datei weiter lesen. Kontrastsicherung liegt in den Modulfunktionen `contrast_ratio`, `readable_text_color` und `ensure_contrast`: Auswahl- und Hover-Flächen bekommen ihre Textfarbe berechnet, nicht geraten. Details: [Designsystem](50_DESIGNSYSTEM_3.23.0.md).

Gemeinsame Bausteine, die 3.23.0 hinzufügt: `render_pass()` ist ein Kontextmanager, der einen Aufbau als einen Durchlauf markiert; `render_cached(schlüssel, fabrik)` hält innerhalb dieses Durchlaufs wiederholte Auswertungen – Bestandszählungen, Tagesplanung, Ordnersummen – genau einmal; `save_items` leert den Zwischenspeicher. `prepare_table` vereinheitlicht Spaltenbreiten, Mindestbreiten, Ausrichtung und Sortierung aller sieben Treeviews. `ResponsiveColumns` verteilt Formularblöcke auf zwei Spalten und fällt unterhalb der Mindestbreite auf eine zurück. `attach_calendar_picker` bindet Datumsfeld, Kalendersymbol und Kalenderfenster projektweit zusammen. `dialog_label` ersetzt den fehlerhaften Aufruf, der das leere Spaltenfenster verursachte. `pack_relative` packt ein Widget nur dann relativ zu einem anderen, wenn dieses tatsächlich gepackt ist. `header_density`, `sync_action_density` und `show_header_overflow_menu` regeln, welche Bedienelemente bei geringer Fensterbreite sichtbar bleiben und welche ins Überlaufmenü wandern. Details: [Leistung und Oberfläche](51_LEISTUNG_UND_OBERFLAECHE_3.23.0.md).

Die Austauschschicht ist datennah und ohne UI-Abhängigkeit: `build_exchange_payload`, `parse_exchange_document`, `apply_exchange_payload` und `exchange_payload_from_markdown` bilden Ordner, Listen, Punkte, Checklisten, Metadaten und stabile IDs in beide Richtungen ab; `ExchangeReport` sammelt Befunde, ohne den Bestand anzufassen. Grenzen (`MAX_EXCHANGE_BYTES`, `MAX_EXCHANGE_ITEMS`, `MAX_EXCHANGE_DEPTH`) gelten vor dem Schreiben. Details: [Austauschformat](52_AUSTAUSCHFORMAT_3.23.0.md).

`ItemWorkspace` führt Pinnwandverbindungen als eigene, ungerichtete und deduplizierte Liste je Pinnwand in `settings.json`; `draw_connections` zeichnet sie beim Verschieben mit, `unpin` räumt sie ab. Fokusmodus und Flächenausgabe (`board_print_geometry`, `build_board_print_html`) arbeiten auf der belegten Fläche, nicht auf dem Bildschirmausschnitt. Details: [Pinnwand](53_PINNWAND_ARBEITSFLAECHE_3.23.0.md). Die Listenansicht kennt fünf Anzeigemodi; synthetische Zeilen für Checklisten, Anhänge und Notizen tragen Markerpräfixe in der IID und werden von Punktaktionen abgefangen. Details: [Anzeigemodi](54_ANZEIGEMODI_3.23.0.md).

`process_reminders` ist eine Datenoperation mit persistentem Zustellbeleg; `reminder_tick` prüft alle 15 Sekunden und fordert anschließend optional Plattformaufmerksamkeit an. Umbenannt ist ausschließlich das Thema in der UI, nicht der Datenvertrag. Bei beendetem Programm läuft keine Zustellung.

Aufgabenformat 16 seit 3.22 (Feld `checklist`), Einstellungsformat 2 und Vorlagenformat 2 unverändert; 3.23.0 bringt keinen Formatsprung und ergänzt ausschließlich additive Einstellungswerte. `GLIDE_DATA_DIR` isoliert jeden Test. Nutzdaten umfassen `liste_speicher.json`, `settings.json`, `vorlagen.json`, `attachments/`, `backups/`, `window.conf` und `glide.lock`. Ressourcen liegen unter `src/glide/resources/`.

[QA](07_QA_BERICHT.md) · [Daten und Migration](06_DATA_BACKUP_MIGRATION.md) · [Historische Detailverträge](00_INDEX.md).

3.11 ergänzt `SavedFilters` als reine Ableitung, 3.12 ergänzt `today_plan` als geordnete ID-Referenz auf bestehende Aufgaben, 3.13 ergänzt `table_columns` als listenspezifische Spaltenliste. `SavedFilters.entries`, `today_plan_entries` und `table_entries` erzeugen beim Öffnen keine Kopien. Die Tabellenzeilen tragen echte Aufgaben-IDs; Bearbeitungen laufen über denselben `item_change`-Pfad. `saved_filters`, `active_saved_filter`, `today_plan` und `table_columns` werden additiv in den Einstellungen normalisiert. [Bedienung 3.13](archiv/36_TABELLENANSICHT_3.13.0.md).

3.21 ergänzt `read_ics_file`, `unfold_ics_lines`, `parse_ics_property`, `parse_ics_events`, `parse_ics_moment`, `parse_ics_duration`, `unescape_ics_text`, `ics_repeat_from_rule`, `ics_importance_from_priority`, `ics_events_to_items`, `ics_preview_text`, `import_ics_events`, `known_glide_item_ids` und `show_ics_import_dialog`. Der Parser arbeitet ohne Fremdbibliothek: Entfalten, Eigenschaften mit Parametern, VEVENT- und VALARM-Blöcke. Punkte entstehen ausschließlich über `new_item`, die Übernahme läuft als ein `snapshot_undo`-Schritt. Kein neues Datenfeld, keine neue Laufzeitabhängigkeit – `zoneinfo` ist Standardbibliothek und wird nur genutzt, wenn das System die Zeitzonendatenbank mitbringt. [Bedienung 3.21](45_KALENDERIMPORT_3.21.0.md).

3.20 ergänzt `build_ics_document`, `ics_sources`, `ics_event_lines`, `ics_alarm_lines`, `ics_repeat_rule`, `write_ics_document`, `escape_ics_text`, `fold_ics_line`, `ics_utc_stamp`, `ics_local_stamp` und `show_calendar_export_dialog`. Die Mengen kommen aus `print_document_sections` – dieselbe Datengrundlage wie der Druck, damit Ausgabe und Ansicht nicht auseinanderlaufen. Die Ausgabe ist rein lesend: kein neues Datenfeld, kein Verlaufseintrag, keine neue Laufzeitabhängigkeit. [Bedienung 3.20](archiv/44_KALENDERAUSGABE_3.20.0.md).

3.19 ergänzt `history_snapshot`, `history_events`, `group_history_events`, `record_history_events`, `update_history`, `reset_history_baseline`, `normalize_history_entries`, `filtered_history`, `clear_history`, `history_entry_line`, `show_history_dialog` und `ensure_schema15_backup`. Der Verlauf entsteht in `update_history` innerhalb von `save_items` aus dem Vergleich zweier Vergleichsstände – eine Stelle für alle Änderungswege. `normalize_lists_data` legt den gelesenen Verlauf in `_loaded_history` ab, damit ein fremdes Archiv den laufenden Bestand nicht überschreibt. Neues Datenfeld `history` im Aufgabenformat 15, keine neue Laufzeitabhängigkeit. [Bedienung 3.19](archiv/43_AENDERUNGSVERLAUF_3.19.0.md).

3.18 ergänzt `read_csv_table`, `detect_csv_encoding`, `decode_csv_bytes`, `detect_csv_delimiter`, `guess_csv_header`, `csv_auto_mapping`, `csv_rows_to_items`, `csv_preview_text`, `import_csv_table`, `csv_import_summary` und `show_csv_import_dialog` sowie die Werteparser `parse_csv_flag`, `parse_csv_importance`, `parse_csv_kind`, `parse_csv_minutes` und `parse_csv_level`. Gelesen wird mit dem `csv`-Modul der Standardbibliothek; `csv_rows_to_items` erzeugt Punkte ausschließlich über `new_item`, `import_csv_table` übernimmt sie über `snapshot_undo` und `save_items` als einen Schritt. Kein neues Datenfeld, keine neue Laufzeitabhängigkeit. [Bedienung 3.18](archiv/42_CSV_IMPORT_3.18.0.md).

3.17 ergänzt `print_document_sections`, `flatten_print_items`, `print_item_details`, `build_print_html`, `write_print_document` und `show_print_dialog`. Die Druckansicht ist reine Ausgabe: Sie liest vorhandene Objekte, erzeugt eine eigenständige HTML-Datei ohne externe Verweise und übergibt sie an `open_external_path`. Kein neues Datenfeld, keine neue Laufzeitabhängigkeit, kein eigener PDF-Schreiber; `escape_print_text` ersetzt eine Fremdbibliothek für Markup-Sicherheit. [Bedienung 3.17](archiv/41_DRUCK_UND_PDF_3.17.0.md).

3.16 ergänzt `app_backup_payload`, `app_backup_section`, `describe_app_backup`, `read_app_backup_file`, `restore_app_backup_extras` und `restore_app_backup`. Das Archiv bleibt das bestehende ZIP; der Abschnitt `app_backup` liegt neben den Aufgabenfeldern, deshalb bleibt es für ältere Fassungen ein Aufgabenbackup. Die Aufgaben laufen weiter durch `import_full_backup`, das jetzt `confirm=False` kennt, weil die Inhaltsvorschau die Rückfrage ersetzt. `ask_app_backup_sections` zeigt die Vorschau und liefert die gewählten Bereiche. [Bedienung 3.16](archiv/40_APP_BACKUP_3.16.0.md).

3.15 ergänzt die Systemansicht `PLAN_DAY_VIEW`. `plan_day_entries` filtert den vorhandenen Bestand nach `planned_date` und liefert dieselbe Tupelform wie die übrigen Aufgabenübersichten; `refresh_task_overview` zeigt sie unverändert an. `planning_summary` und `format_planning_summary` sind die einzige Rechenstelle für Tages-, Auswahl- und Tabellensumme. Der betrachtete Tag liegt als `plan_day_value` nur im Laufzeitzustand, die Kapazität additiv als `daily_capacity_minutes` in den Einstellungen. `update_in_progress_item` akzeptiert zusätzlich `planned_date`. Keine gespeicherte Tagesbilanz, kein neues Datenfeld. [Bedienung 3.15](archiv/39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md).

3.14 ergänzt `planned_date` und `estimated_minutes` am bestehenden Aufgabenobjekt. `normalize_planning` prüft alle Schreib-/Importwege. `_make_planning_editor` wird von Einzel- und Mehrfachbearbeitung verwendet; Mehrfachänderungen laufen über `apply_planning_selected` und `item_change`. `DueField(show_time=False)` verwendet denselben Kalender ohne Uhrzeit. `ensure_schema14_backup` schützt die erste Migration. Keine neue Laufzeitabhängigkeit. [Bedienung 3.14](archiv/37_PLANUNG_UND_AUFWAND_3.14.0.md).


## Bewertung 3.26: Widgets und Ereignisse

Die Notizansicht verwendet eine feste Höhe von sechs Aufgabenzeilen mit eigenem Scrollen und einen wachsenden Editor. Ein PanedWindow würde die vereinbarte 5–7-Zeilen-Vorgabe ohne zusätzlichen Nutzen aufweichen. Pinnwand-Eigenschaften und eine ständig sichtbare Detailansicht sind derzeit keine unabhängigen Paneele; deshalb dort kein Splitter.

Comboboxen, kompakte Zoomauswahl und bestehende Fortschrittskomponenten bleiben erhalten. Spinbox, Scale und Notebook liefern für die vorhandenen Eingaben keinen belegten Bedienvorteil und werden nicht parallel eingeführt.

Die direkten Abhängigkeiten sind: item_change -> Speichern/Verlauf/Statistik und aktuelle Aufgabenansicht; sidebar_change -> Speichern/Sidebar und Listenansicht; guarded_structural_change schützt Strukturumbauten. Theme-Wechsel aktualisieren zentrale Styles und sichtbare Views; Import/Restore normalisiert vollständig vor dem Neuaufbau. Auswahl bleibt lokal im Workspace, Pinnwandänderungen in dessen Refresh-Pfad. Verlauf wird aus dem gespeicherten Modellzustand abgeleitet.

Damit sind TaskChanged, ListChanged und StructureChanged mögliche spätere Signale an den Mutationsgrenzen; SelectionChanged/BoardChanged bleiben lokal; ThemeChanged/SettingsChanged gehören an die zentralen Einstellungswege; HistoryChanged an den Verlaufsschreibpunkt; DataReloaded erst hinter die vollständige Normalisierung. 3.26 führt keine zweite Benachrichtigungsschicht neben diesen Aufrufen ein: Das würde sonst doppelte Refreshes und unklare Reihenfolge riskieren. Eine spätere Migration muss pro Grenze den direkten Aufruf ersetzen und Reentranz testen.

Live-Suchänderungen werden mit after_idle je Ereigniszyklus zusammengefasst; ein expliziter Refresh verwirft den geplanten Doppelaufruf. Rich-Text-Autosave wartet 400 ms, Flushing vor Seitenwechsel und Datenausgabe schließt ausstehende Änderungen ab. Resize-, Scrollbar- und Canvas-Aktualisierungen verwenden ihre vorhandenen Scheduler weiter.
