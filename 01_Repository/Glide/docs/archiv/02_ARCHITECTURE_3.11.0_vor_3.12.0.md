# Architektur – Glide 3.11.0

Stand 13.09.2026 · Aufgabenformat 13

`src/glide/app.pyw` bleibt der kanonische Python-/Tk-Monolith. `ListApp` koordiniert Daten, Ansichten und Dialoge. Keine neue Laufzeitabhängigkeit.

Änderungen an Aufgaben laufen durch `item_change`, Listen/Ordner durch `sidebar_change`; strukturelle Umbauten zusätzlich durch `guarded_structural_change`. Modale Dialoge verwenden `run_modal` und geben bestehende Grabs zurück. Import und Restore behalten ihre transaktionalen Prüf-/Stagingpfade.

`AppOptionMenu`, `OptionRows`, `LabelDropdown` und `DropdownPopup` teilen seit 3.9 die Auswahlbedienung auf allen Plattformen. Popups sind eingebettete Frames, ohne `Toplevel` und ohne `grab_set`. Die temporäre Ereignisbindung wird bei jedem Schließen entfernt. Datenvariablen und Menüaufrufe bleiben kompatibel; `MacOptionMenu` ist ein interner Alias. Details: [UI-Vertrag](32_UI_UND_BEDIENUNG_3.9.0.md).

`app_action_entries` liest die vorhandenen Menüs rekursiv. `show_actions_dialog` stellt sie durchsuchbar dar, `invoke_app_action` führt denselben Befehl nach Schließen aus und erhält den vorherigen Textfokus. `_apply_sidebar_visibility` gibt die gesamte Inhaltsbreite frei. Die Sichtbarkeit wird additiv in Einstellungen gespeichert.

`ButtonFlow` ordnet vollständige Aktionen in passende Zeilen. `RoundedContainer` folgt auf Wunsch der Inhaltshöhe. `SystemNavigation` bewahrt den nativen Treeview-Vertrag. Startseite, Vorlagen und Bestandsübersicht teilen den scrollbaren Canvas; Aktionsleisten sind feste Geschwisterbereiche. Vorlagen verwenden `TemplateDraft` zur isolierten Bearbeitung. Private Schriftregistrierung läuft über GDI/CoreText.

`process_reminders` ist eine Datenoperation mit persistentem Zustellbeleg; `reminder_tick` prüft alle 15 Sekunden und fordert anschließend optional Plattformaufmerksamkeit an. Umbenannt ist ausschließlich das Thema in der UI, nicht der Datenvertrag. Bei beendetem Programm läuft keine Zustellung.

Aufgabenformat 13, Einstellungsformat 2 und Vorlagenformat 2 bleiben unverändert. `GLIDE_DATA_DIR` isoliert jeden Test. Nutzdaten umfassen `liste_speicher.json`, `settings.json`, `vorlagen.json`, `attachments/`, `backups/`, `window.conf` und `glide.lock`. Ressourcen liegen unter `src/glide/resources/`.

[QA](07_QA_BERICHT.md) · [Daten und Migration](06_DATA_BACKUP_MIGRATION.md) · [Historische Detailverträge](00_INDEX.md).

3.11 ergänzt `SavedFilters` als reine Ableitung aus bestehenden Listen und Punkten. `SavedFilters.entries` erzeugt beim Öffnen neue Referenzen und berechnet relative Fälligkeiten mit dem aktuellen Tag; die Aufgabenobjekte werden nicht kopiert. Die Schnellerfassung verwendet den vorhandenen `new_item`-/`item_change`-Pfad und speichert keine neue Datenstruktur. `saved_filters` und `active_saved_filter` werden additiv in den Einstellungen normalisiert. [Bedienung 3.11](34_SCHNELLERFASSUNG_UND_FILTER_3.11.0.md).
