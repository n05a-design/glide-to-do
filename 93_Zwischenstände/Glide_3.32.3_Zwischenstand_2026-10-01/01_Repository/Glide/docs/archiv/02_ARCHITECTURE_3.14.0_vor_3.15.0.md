# Architektur – Glide 3.14.0

Stand 13.09.2026 · Aufgabenformat 14

`src/glide/app.pyw` bleibt der kanonische Python-/Tk-Monolith. `ListApp` koordiniert Daten, Ansichten und Dialoge. Keine neue Laufzeitabhängigkeit.

Änderungen an Aufgaben laufen durch `item_change`, Listen/Ordner durch `sidebar_change`; strukturelle Umbauten zusätzlich durch `guarded_structural_change`. Modale Dialoge verwenden `run_modal` und geben bestehende Grabs zurück. Import und Restore behalten ihre transaktionalen Prüf-/Stagingpfade.

`AppOptionMenu`, `OptionRows`, `LabelDropdown` und `DropdownPopup` teilen seit 3.9 die Auswahlbedienung auf allen Plattformen. Popups sind eingebettete Frames, ohne `Toplevel` und ohne `grab_set`. Die temporäre Ereignisbindung wird bei jedem Schließen entfernt. Datenvariablen und Menüaufrufe bleiben kompatibel; `MacOptionMenu` ist ein interner Alias. Details: [UI-Vertrag](32_UI_UND_BEDIENUNG_3.9.0.md).

`app_action_entries` liest die vorhandenen Menüs rekursiv. `show_actions_dialog` stellt sie durchsuchbar dar, `invoke_app_action` führt denselben Befehl nach Schließen aus und erhält den vorherigen Textfokus. `_apply_sidebar_visibility` gibt die gesamte Inhaltsbreite frei. Die Sichtbarkeit wird additiv in Einstellungen gespeichert.

`ButtonFlow` ordnet vollständige Aktionen in passende Zeilen. `RoundedContainer` folgt auf Wunsch der Inhaltshöhe. `SystemNavigation` bewahrt den nativen Treeview-Vertrag. Startseite, Vorlagen und Bestandsübersicht teilen den scrollbaren Canvas; Aktionsleisten sind feste Geschwisterbereiche. Vorlagen verwenden `TemplateDraft` zur isolierten Bearbeitung. Private Schriftregistrierung läuft über GDI/CoreText.

`process_reminders` ist eine Datenoperation mit persistentem Zustellbeleg; `reminder_tick` prüft alle 15 Sekunden und fordert anschließend optional Plattformaufmerksamkeit an. Umbenannt ist ausschließlich das Thema in der UI, nicht der Datenvertrag. Bei beendetem Programm läuft keine Zustellung.

Aufgabenformat 14, Einstellungsformat 2 und Vorlagenformat 2 bleiben unverändert. `GLIDE_DATA_DIR` isoliert jeden Test. Nutzdaten umfassen `liste_speicher.json`, `settings.json`, `vorlagen.json`, `attachments/`, `backups/`, `window.conf` und `glide.lock`. Ressourcen liegen unter `src/glide/resources/`.

[QA](07_QA_BERICHT.md) · [Daten und Migration](06_DATA_BACKUP_MIGRATION.md) · [Historische Detailverträge](00_INDEX.md).

3.11 ergänzt `SavedFilters` als reine Ableitung, 3.12 ergänzt `today_plan` als geordnete ID-Referenz auf bestehende Aufgaben, 3.13 ergänzt `table_columns` als listenspezifische Spaltenliste. `SavedFilters.entries`, `today_plan_entries` und `table_entries` erzeugen beim Öffnen keine Kopien. Die Tabellenzeilen tragen echte Aufgaben-IDs; Bearbeitungen laufen über denselben `item_change`-Pfad. `saved_filters`, `active_saved_filter`, `today_plan` und `table_columns` werden additiv in den Einstellungen normalisiert. [Bedienung 3.13](36_TABELLENANSICHT_3.13.0.md).

3.14 ergänzt `planned_date` und `estimated_minutes` am bestehenden Aufgabenobjekt. `normalize_planning` prüft alle Schreib-/Importwege. `_make_planning_editor` wird von Einzel- und Mehrfachbearbeitung verwendet; Mehrfachänderungen laufen über `apply_planning_selected` und `item_change`. `DueField(show_time=False)` verwendet denselben Kalender ohne Uhrzeit. `ensure_schema14_backup` schützt die erste Migration. Keine neue Laufzeitabhängigkeit. [Bedienung 3.14](37_PLANUNG_UND_AUFWAND_3.14.0.md).
