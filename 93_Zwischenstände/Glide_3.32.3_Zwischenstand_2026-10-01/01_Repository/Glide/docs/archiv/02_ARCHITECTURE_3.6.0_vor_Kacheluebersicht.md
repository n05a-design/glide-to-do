# Architektur – Glide 3.6.0

Stand: 06.09.2026 · Aufgabenformat 11

## UI-Nachbesserung nach den 14 Rückmeldungen

`ButtonFlow` ordnet vollständige Buttons in passende Zeilen. Die
`template_actions` sind ein fester Geschwisterbereich zum scrollbaren Inhalt;
die Textspalten der Vorlagen wechseln bei geringer Breite auf zwei Zeilen.
`SystemNavigation` bewahrt den nativen Treeview-Vertrag und zeichnet nur die
Symbolspalte als um zwei Pixel angehobenen Canvas-Text. Mausaktionen werden
an den Treeview weitergeleitet; Auswahl, Hover und Tastatur bleiben gekoppelt.
`active_theme` trennt `ui_accent`/`selection` von der gespeicherten Palettenfarbe
`accent` (Lila). `calendar_moon_phases` berechnet Hauptphasen lokal, ohne Netzwerk
oder zusätzliche Laufzeitbibliothek. Details: [UI-Nachbesserung](22_UI_NACHBESSERUNG_3.6.0.md).


## Anwendung und Zuständigkeiten

`src/glide/app.pyw` bleibt der kanonische Python-/Tk-Monolith. `ListApp`
koordiniert Daten, Ansichten und Dialoge. Aufgabenbäume und die verschachtelte
Seitenleiste verwenden ttk.Treeview; die Systemnavigation zeigt getrennte
Symbol-, Titel- und Zählerspalten. Rundungen, Uhr, Mondphase, Labelchips und
Jahresanzeige werden auf Tk-Canvas gezeichnet.

`item_change` und `sidebar_change` kapseln normale Bestandsänderungen,
Undo, Auswahl und Aktualisierung. Strukturelle Umbauten verwenden zusätzlich
`guarded_structural_change`. Backup-Restore hat einen eigenen transaktionalen
Pfad mit vorheriger Sicherung, begrenztem Entpacken und atomarem Commit.
Modale Dialoge laufen über `run_modal` und geben den Grab an ihren Aufrufer zurück.

## Neue Bausteine 3.6

- `normalize_template_records`, `capture_template` und die Vorlagenseite
  verwalten einen eigenständigen Katalog. Einfache Systemvorlagen enthalten
  Aufgaben-/Listentitel. Eigene Vorlagen enthalten ein portables Teilpayload,
  Labeldefinitionen und eingebettete Anhangsbytes.
- `partial_backup_payload` wählt vollständige Zweige einschließlich leerer
  Unterordner. `import_full_backup(additive=True)` nutzt den regulären
  Archivprüf- und Stagingpfad. `prepare_additive_import` erzeugt neue IDs und
  ordnet Labels zu, ohne bestehende Listen zu ersetzen.
- `get_app_data_dir`, `change_data_folder`, `read_foreign_lock` und die
  Acquire-/Refresh-/Release-Methoden verwalten Zeiger, Kopie und Belegungsprüfung.
  Eine bekannte Fremdbelegung sperrt das Speichern.
- `active_theme` berechnet Materialfarben und Akzent. `RoundedContainer`
  zeichnet dezente Kanten. DWM-Mica ist optional und von System und
  Clientflächen abhängig; Tk besitzt keine echte per Widget Blur-Schicht.
- `register_private_fonts` registriert TTF/OTF über GDI bzw. CoreText.
  `app_font` verwendet den tatsächlichen Familiennamen der Tk-Standardschrift.
  So vermeidet Glide die Interpretation des Tupelnamens „TkDefaultFont“ als Arial.
- `MoonPhase` zeichnet Kreisrand und Terminator; `YearHeatmap` stellt
  53 Wochen mit dem heutigen Tag dar. Mondwerte sind eine dekorative Näherung
  aus einem mittleren Mondzyklus, keine astronomische Ephemeride.
- `record_recent_list_edits` erfasst erfolgreiche Änderungen. Die
  Bearbeitungshistorie und Erledigungshistorie werden getrennt geführt.

## Daten und Laufzeit

`liste_speicher.json`, `settings.json`, `vorlagen.json`, `attachments/`,
`backups/`, `window.conf` und `glide.lock` liegen in der Datenablage.
Keine Laufzeitdaten gehören in `src/`. Schriftdateien und Lizenz sind
Programmressourcen unter `src/glide/resources/fonts/`.

Die App-Version ist unabhängig vom Datenformat. 3.6 verwendet weiter Format 11.
Alte Referenzbestände bleiben als Migrationseingänge erhalten. Persönliche
Einstellungen werden additiv auf Format 2 normalisiert.

## Prüf- und Wartungspunkte

Sieben Suiten plus zwei Analysen laufen über `tests/tools/pruefen.py`.
`test_release36.py` prüft die neuen Bedien- und Datendurchläufe.
`leistungspruefung.py` misst synthetische Bestände. Keine statische
Erreichbarkeitsvermutung führt automatisch zum Löschen von Code.

Das ursprüngliche Langzeit-Einfrieren wurde nicht reproduziert. Weitere DPI,
mehrere Monitore, macOS, echte Cloudkonflikte und signierte Pakete benötigen
eigene Plattformabnahmen. [QA](18_QA_3.6.0.md) ·
[Datenvertrag](06_DATA_BACKUP_MIGRATION.md) · [Leistung](21_LEISTUNGSBERICHT_3.6.0.md).
