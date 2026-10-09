# Architektur – Glide

Stand 09.10.2026 · Glide 3.35.0 · Aufgabenformat 23 · Einstellungen 2 · Vorlagen 2

Technischer Einstieg in den Code: Aufbau, Datenwege, Bausteine der Oberfläche, Performance-Regeln und die teuer gelernten Tk-Fallstricke. Zusammengeführt aus Architektur, Projektübergabe, Entwicklungsnotizen und den technischen Teilen der Funktionsverträge 45–79 (03.10.2026); die Vorfassungen trägt Git. Verhalten der Funktionen: [Funktionen](20_FUNKTIONEN.md). Datenformat: [Daten und Migration](06_DATA_BACKUP_MIGRATION.md).

## 1. Aufbau

- **Laufzeit:** Python 3.14 mit Tk 9 ist die Referenz. Aktuell geprüft: Referenz-Mac 3.35.0 mit Python 3.14.5/Tk 9.0.3 (automatische Vollprüfung, Bundle 3.35.0) und Windows 3.33.18 mit Python 3.14.7/Tk 9.0.4; Linux und menschliche Abnahme offen ([QA-Bericht](07_QA_BERICHT.md)). Python 3.12/3.13 mit Tk 8.6 starten, sind aber eingeschränkt: keine `nsimage`- und SVG-Vorschauen, keine Systemmitteilungen über `tk sysnotify`, Logo nur als ungeglättete Fläche, App-Symbol ungefiltert verkleinert; Herkunftszelle in Heute ohne eigene gedämpfte Textfarbe. Ältere Laufzeiten (Python vor 3.12, Tk vor 8.6) weist `runtime_check.py` seit 3.33.20 vor jedem Datenzugriff mit einer Meldung ab (AB08).
- **Kanonischer Quellbaum:** `src/glide/`. `app.pyw` enthält die Klasse `ListApp`, die Daten, Ansichten und Dialoge koordiniert. Seit D17 entsteht jede neue oder angefasste Fachlogik als Tk-freies Modul mit Unit-Tests unter `tests/unit`; `ListApp` ruft sie auf.
- **Startbare Kopie:** `07_Python-Versionen` (bytegleich zu `src/glide`, `glide_start.py` heißt dort `Schnellstart.pyw`) und das macOS-Entwicklungsbundle `build/macos/Glide.app` (lokal, nicht versioniert). Beide entstehen nur in einer Produktionsrunde über `scripts/pflege/abgleich_07.py` und `packaging/macos/baue_app.py` mit SHA-256-Abgleich.
- **Keine Laufzeitabhängigkeit** außer der Standardbibliothek. Einzige mitgelieferte Bibliothek: tkinterdnd2 unter `src/glide/vendor` (optional, beim ersten Ziehen aus Finder/Explorer geladen; [Entscheidung](decisions/ABHAENGIGKEIT_TKDND.md)).
- **Ressourcen:** `src/glide/resources/` – Schriften (DejaVu, Pixelify Sans), Vorlagen, `logo/` (unveränderte Kopien aus `20_Grafik_Master`).

### Module neben `app.pyw`

| Datei | Aufgabe | Seit |
|---|---|---|
| `glide_start.py` | Startet `app.pyw` als Modul mit Bytecode-Cache im Systemcache (`sys.pycache_prefix`) | 3.30 |
| `drawing.py` | Zellmodell der Pixel-Werkstatt: Größen 16–128, Aktionspuffer (`begin_action`/`end_action`), Formen, Symmetrie, Muster, JSON `hex8-row-v1`, Glide-SVG, PNG/ICO-Kodierung, Paletten (GPL, HEX, ASE, Aseprite) | 3.29 |
| `drawing_image.py` | Tk-Bildfunktionen und Miniaturen der Zeichnung | 3.29 |
| `backdrop.py` | Hintergrundverläufe: Entwürfe, Lesezone, PNG schreiben/lesen | 3.30 |
| `page_markdown.py` | Markdown ↔ Seitendokument | 3.30 |
| `image_preview.py` | `PreviewCache`: Vorschauen über Tk 9 `nsimage`, SVG, Windows WIC, `sips` (macOS) | 3.30 |
| `logo.py` | Logo aus den SVG-Mastern mit Akzentfarbe, Canvas-Rückfall unter Tk 8.6 | 3.30 |
| `schema_backups.py` | Formatsicherung vor Migrationen mit Dateistandprüfung (T2) | 3.33.0 |
| `sidebar_policy.py` | Zuordnung, Inhaltsgrenzen, Vorlagenprüfung und Reihenfolge der vier Seitenleistenbereiche; `CONTAINED` lässt datierte Zeichnungen im Notizbuch zu | 3.33.1 |
| `svg_geometry.py` | SVG-Pfade einschließlich verkürzter kubischer Kurven, CSS-/Attributfarben, transparente Innenkonturen | 3.33.1 |
| `home_tiles.py` | Startseitenkacheln: Bestand, Standard (D12), Normalisierung, eigene Auswahl, zusammengeführte Kachel „Heute“ | 3.33.2 |
| `capture_parser.py` | Deutsche Schnelleingabe (G01): Bearbeitungstag, Fälligkeit, Uhrzeit, Aufwand, Wichtigkeit, Labels, „/“-Befehle, Wiederholungen; jede Erkennung mit Textstelle zum Zurücknehmen | 3.33.3 |
| `eisenhower.py` | Quadranten „Dringlichkeit × Wichtigkeit“ und Änderung beim Ablegen (`DRINGEND_TAGE`, `WICHTIG_AB`) | 3.33.5 |
| `today_view.py` | Aufteilung von „Heute“ ohne Dubletten, nächste Aufgabe, Zählung | 3.33.6 |
| `content_search.py` | Inhaltssuche, Titelrang und Ausschnitt ohne Tk, I/O oder Index | 3.33.7 |
| `save_comparison.py` | Gemeinsamer Speichervergleich; Prüfsummen der Teilbäume einmal von unten nach oben, Verlaufswerte und Abschlusszeit im selben Durchlauf (P08a) | 3.33.9 |
| `view_metrics.py` | Kennzahlen in einem Durchlauf, begrenztes Datumslesen, frischer Fälligkeitsstatus und Zeilenhöhenformel (P09b) | 3.33.10 |
| `action_catalog.py` | Stabile Aktionskennungen, Gruppen und virtuelle Editorbefehle (Tk-frei) | 3.33.11 |
| `ui_design.py` | Gemeinsame Abstände, Radien, Schriftgrößen und Zeilenhöhen; Titel-/Herkunftsbreiten (Tk-frei, OB01/U10/U19) | 3.33.12 |
| `planning.py` | Bearbeitungstagsziele, Wochentagskapazität, gemeinsame Bilanz und Vorschau ohne Mutation (Tk-frei, KO01/AU02) | 3.33.13 |
| `day_proposal.py` | Erklärbare Tagesauswahl, Auswahlbudget und Prüfung veralteter Vorschläge (Tk-frei, AU01) | 3.33.14 |
| `focus_timer.py` | Pausierbarer Fokus, Intervallzeit und wiederholbare Buchung nach Schreibfehler/Neustart (Tk-frei, G05/AU05) | 3.33.14 |
| `task_references.py` | Heimat und Textverweise, Quellenindex, Zielzustand, ID-Neuvergabe und bearbeitete Zeilentitel ohne Tk | 3.33.15 |
| `interaction_policy.py` | Palettensuche, gemerkte Hinweise und getrennte Datumsanzeige (Tk-frei) | 3.33.16 |
| `object_references.py` | Typisierte lokale Verweise, abgeleitete Rückverweise und Import-/Kopierregeln (Tk-frei) | 3.33.17 |
| `week_planning.py` | Gemeinsame Wochenbilanz und Zeitfenster aus vorhandenen Glide-Blöcken (Tk-frei) | 3.33.17 |
| `page_features.py` | Live-Listen, Titelbildvertrag und gefüllte Vorlagenvorschau ohne Bestandsmutation (Tk-frei) | 3.33.18 |
| `repeat_rules.py` | Wiederholungsregeln (bis 3.33.19 Klassenmethoden von `ListApp`, die weiter delegieren), Termin überspringen, verpasste Termine überspringen (Tk-frei, KO02) | 3.33.20 |
| `routines.py` | Routinen in „Heute“: Auswahl, Fortschritt, heute vollständig (Tk-frei, AU06) | 3.33.20 |
| `runtime_check.py` | Mindestversion Python/Tk vor jedem Datenzugriff, bewusst in einfacher Syntax (AB08) | 3.33.20 |
| `release_notes.py` | Katalog und Regeln der einmaligen Karte „Neu in …“ (Tk-frei, N07) | 3.33.20 |
| `appearance.py` | Designpaar und Erkennung des Systemmodus für „Automatisch hell/dunkel“ (Tk-frei, N01) | 3.33.21 |
| `preview_tools.py` | Systemwerkzeuge für Bildvorschauen unter Linux, JPEG-Größe (Tk-frei, N08) | 3.34.0 |
| `filter_explain.py` | Bedingungen gespeicherter Filter prüfen und erklären (Tk-frei, D-03) | 3.34.0 |
| `exchange_patch.py` | KI-Austausch Stufe 2: Kontextpaket, Änderungsvorschlag prüfen, Konflikte (Tk-frei, G24) | 3.35.0 |
| `backup_diff.py` | Zwei Datenstände vergleichen, nur lesend (Tk-frei, F-03) | 3.35.0 |

`drawing_prototype.pyw` ist die isolierte Bedienprobe der Zeichenfläche von 2026-09-24; sie gehört nicht zur App und nicht zu den Lieferwegen. Ein neues Modul muss in `packaging/macos/baue_app.py`, `scripts/pflege/abgleich_07.py`, `src/glide/README.md`, `packaging/README.md`, `07_Python-Versionen/README.md` und hier stehen; die Standprüfung (R10) meldet Lücken.

## 2. Nutzdaten und Speicherweg

- **Ablage:** `liste_speicher.json` (Aufgaben, Listen, Ordner, Verlauf), `settings.json`, `vorlagen.json`, `attachments/`, `backups/`, `window.conf`, `glide.lock` im Nutzerdatenordner; `GLIDE_DATA_DIR` ersetzt ihn. **Jeder Test und jede Messung setzt `GLIDE_DATA_DIR` vor dem Import** auf einen temporären Ordner.
- **Mutationsgrenzen:** Aufgaben ändern sich über `item_change`, Listen und Ordner über `sidebar_change`, strukturelle Umbauten zusätzlich über `guarded_structural_change` (Bestandswächter gegen verlorene Punkte). Import und Restore haben eigene transaktionale Prüf- und Stagingpfade; Punkte entstehen nur über `new_item`, Übernahmen sind ein `snapshot_undo`-Schritt.
- **Speichern:** `save_items` schreibt sofort (kein verzögertes Sammeln, E-08), atomar über `write_json_atomic` (`json.dumps` in einem Stück, ab Python 3.14 C-Kodierer auch mit Einrückung) und `replace_with_retry` (Windows-Dateisperre). Dort entsteht auch der Änderungsverlauf (`update_history`, höchstens 15 Einträge und 15 Tage).
- **Speichervergleich (P08a, 3.33.9):** `list_comparison` baut in `save_comparison.py` einen frischen Vergleichsstand für Verlauf, Abschlusszeit, Listenänderung und Aktivität. Jeder Aufgabenbaum wird einmal gelesen; Kind-Prüfsummen fließen in die Eltern-Prüfsumme ein, statt den Teilbaum erneut zu kodieren. Aktivität und „zuletzt bearbeitet“ übernehmen den Stand erst nach erfolgreichem Schreiben. Reine `history_snapshot`-Abfragen erstellen keine Aktivitäts-Prüfsummen und ändern kein Abschlussdatum. Keine persistierten Prüfsummen, kein Cache nach Objektidentität; Undo/Import dürfen Objekte ersetzen. P08b ergänzt seit 3.33.11 deklarierte lokale Punktänderungen: 22 geprüfte Aufrufe in 18 Methoden liefern vor/nach der Mutation stabile Listen-IDs; die aktive Liste wird wegen der Referenzsynchronisierung mitgelesen. Unbekannte oder leere Auswahlen, 27 übrige Punktänderungseinstiege, sidebar_change, direkte Speicherung, Import und Undo vergleichen vollständig. `prepare_comparison` merkt pro Listen-ID nur berechnete Werte erfolgreicher Speicherung; Fehler und Laden verwerfen sie. Neue/gelöschte Listen und die aktuelle Reihenfolge bleiben berücksichtigt. Autosave vergleicht auch bei dirty=False vollständig.
- **Sicherungen:** nur bei geändertem Inhalt (`latest_backup_digest`, SHA-256), dazu je Tag der letzte Stand für 14 Tage. Tests, die Sicherungen löschen, setzen `_latest_backup = None`.
- **Formatwechsel:** `migrate_on_start` stellt ein älteres Format beim Laden um, mit bytegenauer, unrotierter Vorsicherung `liste_vor_format<N>_<Zeit>.json` (`ensure_schema<N>_backup` → `schema_backups.py`). Scheitert die Sicherung, bricht das Speichern vor dem Überschreiben ab. Neuere Formate oder unbekannte Listenarten (`NewerDataError`) öffnen schreibgeschützt (`_read_only_reason`); Unlesbares wird als `liste_unlesbar_*` gesichert. **Neue Listen- oder Ordnerarten nur mit neuer Formatnummer.**
- **Endgültiges Entfernen:** Jeder Weg (Papierkorb leeren, Einträge entfernen, Überlauf in `push_trash_entry`) ruft `drop_dangling_references`. Neue Kennungen ziehen alle Verweise nach: `remap_item_references` (Links, `blocked_by`) und `remap_rich_note_items` (Aufgabenmarken `item:<id>` im Text).
- **Rückgängig:** Schnappschüsse als komprimiertes JSON (`PackedState`). Pinnwand-Flächenänderungen über `board_view_change` (eigener Stapel, den `undo_last_change` zuerst befragt); Zeichnungsstriche über das Editor-Undo, Strukturaktionen der Zeichnung über `apply_drawing_change` (`snapshot_keeping_drawings`).
- **Einstellungen** sind additiv normalisiert (Einstellungsformat 2); Pinnwandpositionen und -verbindungen liegen je Pinnwand unter `pinboards` in `settings.json` und gehören nicht zum Aufgabenbackup.
- **Kennungen, die sich nie ändern:** `APP_BUNDLE_ID` (`de.shaye.glide`) und `APP_USER_MODEL_ID` (`Shaye.Glide`).

**Fokusbuchung (3.33.14):** additive `time_booking` in Einstellungen 2 enthält Kennung und Vorher-/Nachherzeit. Schreiben: Nachweis → Aufgabe über `item_change` → Nachweis/Timer leeren. Wiederholung entscheidet anhand der Aufgabenzeit, ob sie noch anzuwenden oder bereits gebucht ist; Konflikte bleiben offen. `snapshot_undo` und `undo_last_change` lösen einen offenen Nachweis vor weiteren Mutationen auf oder verweigern sie. Pause/Resume verwenden `focus_timer.py`; kurzlebige Fokusbuttons nutzen `_make_dialog_button`, damit Themewechsel keine zerstörten Widgets aus der globalen Buttonliste ansprechen.

## 3. Oberfläche

### Ansichtsaufbau

- `_refresh_tree` baut in fester Reihenfolge: zuerst `restore_note_chrome()` und `restore_drawing_chrome()`, dann Pinnwand vorbereiten, Inhalt, Pinnwand, Notiz, Zeichnung (`sync_drawing_view`), Detailbereich; zuletzt `sync_view_chrome`, das Eingabezeile und Leisten je Ansicht ein- oder ausblendet. Diese Reihenfolge nicht umdrehen.
- `sync_view_chrome` packt nichts ein, solange eine Seitenansicht offen ist (`home_frame` gepackt). Ein neuer Ausblendweg braucht dieselbe Sperre. Beim Wiedereinpacken richtet es sich am nächsten sichtbaren Nachbarn in `list_frame_outer` aus.
- **Feste Bestandteile:** Werkzeuge einer Ansicht gehören in `tool_band_host()`, ihr Hinweis in `surface_hint_text()`; `sync_tool_band` hält die Oberkante, `sync_card_foot` den Kartenfuß (Hinweis oder Auswahlleiste) bis zur Unterkante. Keine andere Stelle blendet sie aus. `test_festlayout330` und `test_kartenfuss330` messen es.
- Zeichnung und Galerie sind Flächenlisten (`is_surface_list`): keine Punkte, keine Tabelle, keine Pinnwand; `hide_drawing_chrome` blendet Eingabe, Suche und Aufgabenbaum aus.
- **Kleine Fenster** (Mindestgröße 860 × 700): `height_density` staffelt nach Höhe, `header_density` nach Breite; Knöpfe der Suchzeile werden vor `search_row_anchor()` gepackt. Jedes neue Bedienelement braucht eine Antwort, was bei Mindestgröße mit ihm geschieht (`test_mindestgroesse330`).
- **Kopfzeile:** Neue Knöpfe gehören in die Reihe von `pack_header_controls`, nie in ein eigenes `pack()`. Das Logo hängt nur an der Breite.

### Bausteine

- **Seitenleiste:** vier Bäume (Seiten, Listen, Notizen, Zeichnungen) über `build_sidebar_section`, gemeinsame `sidebar_iid_to_row`; jede Kennung steht in genau einem Baum (`sidebar_tree_for_entry`, `sidebar_tree_for_folder`, Regeln in `sidebar_policy.py`). Kein `Treeview.see` beim Neuaufbau, sondern `reveal_sidebar_row`. Klappzustände über `remember_tree_open_states`, Auswahl über `see_unless_folded`.
- **Editoren:** `RichNoteEditor` speichert Text und semantische Spannen (Python-Zeichenindizes), kein HTML. `PageEditor` erweitert ihn um Lesespalte, Kürzel und Aufgaben als Kästchen mit `item:<id>` und `taskref:<id>`; `NoteEditor` erweitert `PageEditor` (`ALLOW_TASKS = True`, gemeinsame IDs in Text und Punktliste). Beide teilen Rechtsklickmenü, schwebende Formatleiste, `convert_block`, Aufklapplisten (`toggle`/`toggle_closed`, Ansichtsformat `folded`, nie gespeichert, `apply_folds`) und Gliederung. Textaufgaben und ihre gemeinsamen Editor-Mutationen laufen über `create_page_task`, `rename_page_tasks`, `remove_page_tasks`, `restore_page_task`, `edit_page_task`.
- **Bilder in Seiten:** Ankerzeichen U+FFFC mit `img:<kennung>`, Angaben unter `rich_note.images`, Bildflächen per `place` über dem Text (`layout_images`, `flow_around`, `place_images`, `place_origin`). Vorschauen über `PreviewCache`.
- **Gruppierung** an einer Stelle für Board, Liste und Tabelle: `group_columns`, `item_group_keys`, `set_group_value` (auch Eisenhower). Gruppenüberschriften sind synthetische Zeilen (`GROUP_HEADING_IID_MARKER`); Nummern aus `list_view_number_paths` bzw. `_table_number_paths`.
- **Pinnwand:** `ItemWorkspace` mit freier Fläche und Spaltenboard, Bereichen, Verbindungen (über Punktkennungen, nie als gezeichnete Linie), Präsentation; Zeichnungskarten tragen `page:<Seitenkennung>` (`valid_cards` liefert Punkte und Seiten, `valid_items` nur Punkte). Vorschau und echte Positionen sind getrennt; eine Vorschau schreibt nie Modellkoordinaten zurück.
- **Zeichnung:** `DrawingEditor` eingebettet im Inhaltsbereich; Autosave über `store_drawing` und `save_items`. `LIST_KINDS` ist die zentrale Typregistrierung, `FOLDER_KINDS` die der Ordnerarten.
- **Heute und Stundenraster:** `today_view_pool` und `plan_day_sections` liefern „Heute“ aus `today_view.py`; `sync_plan_day_grid` läuft nach jedem Aufbau, Änderungen über `apply_time_plan`, Ziehen über `plan_grid_minutes_at`/`plan_grid_drop`.
- **Startseite:** Kacheln aus `home_tiles.py`; `set_home_tile_hidden` für Tests. Gismo-Zustand liegt nur in den Einstellungen.
- **Designs:** eine Tabelle `DESIGNS` (Grundpalette `base`, Farbschicht `layer`, `glass`, `partner`), Reihenfolge `DESIGN_ORDER`; `active_theme` baut die Farben. Ein neues Design ist ein Tabelleneintrag. Kontrast über `contrast_ratio`, `readable_text_color`, `ensure_contrast`, `legible_text_roles` und `RoundedButton.legible_text` (WCAG 2.2 AA, `test_kontrast330`).
- **Knopffarben:** `button_color_key` bestimmt die Rolle aus der Beschriftung (`BUTTON_ROLE_RULES`: Rot löschen, Grün bestätigen, Lila hinzufügen/neu, Gelb Hinweis, sonst neutral). Knöpfe nie von Hand einfärben.
- **Hintergrundverläufe:** `backdrop_choice`, Rechnen im Thread, `sync_backdrop_surfaces`; Rahmen erhalten einen Ausschnitt (`_frame_backdrop`), Canvas-Flächen ein Bildelement. Text auf dem Verlauf gehört in ein `CanvasLabel`. Ständig neu zeichnende Flächen stehen in `backdrop_excluded` (Pinnwand). Mausereignisse leitet das Bindtag `GlideBackdrop` weiter.
- **Dialoge:** jeder über `run_modal` (Mindestbreite über `ensure_dialog_min_width`, Griffwiederherstellung, Escape). `_center_dialog` misst das fertige, noch verborgene Fenster und zeigt es erst positioniert.
- **Menübefehle:** `defer_window_menu_commands` legt jeden `add_command`/`insert_command` auf `after_idle` (macOS-Menüverfolgung). Häkchen und Auswahlpunkte bleiben unmittelbar.
- **Aktionen (3.33.11):** `build_menu` registriert stabile Kennungen; Varianten erhalten explizite IDs. `action_catalog.py` ordnet Gruppen und virtuelle Editorbefehle nach ID zu. `app_action_entries` liest aktuelle Beschriftungen/Pfade, fasst gleiche Aktionen zusammen und liefert die ID. `invoke_app_action` löst sie vor Ausführung neu auf, sodass ein alter Menüindex keinen anderen Befehl ausführt. Editorfokus für Copy/Paste/Undo/SelectAll bleibt erhalten. Die alte Beschriftungsabfrage ist eine abgeleitete Kompatibilitätsansicht für Prüfwerkzeuge.
- **Auswahlfelder:** `AppOptionMenu`, `OptionRows`, `LabelDropdown`, `DropdownPopup` als eingebettete Frames ohne `Toplevel` und ohne `grab_set`.
- **Austausch, Import, Ausgabe** (datennah, ohne UI): `build_exchange_payload`, `parse_exchange_document`, `apply_exchange_payload`, `exchange_payload_from_markdown`; CSV (`read_csv_table` … `import_csv_table`), ICS-Import (`parse_ics_events`, `ics_events_to_items`, `import_ics_events`) und -Ausgabe (`build_ics_document`), Druck/PDF als eigenständiges HTML (`build_print_html`, `board_region_lines`, `open_print_html`), App-Backup (`app_backup_payload`, `restore_app_backup`).
- **Erinnerungen:** `process_reminders` mit persistentem Zustellbeleg; `reminder_tick` alle 15 Sekunden. Systemmitteilungen über `tk sysnotify`/`tk systray` (`system_notification_backend`). Bei beendetem Programm keine Zustellung.
- **Schriften:** `register_private_fonts` registriert für den Prozess (Windows GDI `FR_PRIVATE`, macOS CoreText, Linux Fontconfig). `pixel_heading_family` fragt Tk direkt.

## 4. Performance-Regeln

Gemessen wird unprofiliert mit gleicher Fixture, Aufwärmlauf, Median und p95 (`scripts/pflege/messung_performance.py`, `messung_startseite.py`, `messung_speicherweg.py`). Profiling erklärt Ursachen, belegt aber keinen Gewinn.

- **P09b (3.33.10):** `list_metrics` hält unveränderliche Kennzahlen nach Listen-ID und heutigem Datum nur im `render_pass`. `page_chips` verwendet denselben Stand für Kopf und Fortschritt, mit Ansicht und Workspace-Zustand als Schlüssel. Speichern leert das vorhandene Cache-Dictionary, sodass die verschachtelte Durchgangsgrenze erhalten bleibt. Außerhalb des Durchgangs wird frisch gelesen; kein Leerlauf-Timer, keine Objektidentität als Schlüssel. `view_metrics.parsed_date`/`display_date` haben jeweils höchstens 4.096 Zeichenketten; die Tagesbewertung wird nicht gecacht. Messschriften und Zeilenraum gehören zu einer `ListApp`/ihrem Tk-Interpreter, Schlüssel enthalten Schrift und Tk-Skalierung; benannte Schriften werden aktuell aufgelöst. Höchstens 128 Einträge, Leeren beim Schriftwechsel. Labelrand wird bei jeder Höhenabfrage frisch gelesen.
- **Durchgangscache:** `render_pass()` markiert einen Aufbau; `render_cached(schlüssel, fabrik)` hält wiederholte Auswertungen (Zählungen, Tagesplanung, Ordnersummen) genau einmal je Durchgang. Kein dauerhafter Kennzahlen-Cache ohne vollständige Invalidierung.
- **Widget-Caches** nach stabiler `(Art, ID)` und an die Lebensdauer des Ansichtshosts gebunden (`_library_card_cache`, `library_card_preview`); zerstörte Hosts geben Widgets und PhotoImages frei. Kein Umparenten, keine Wiederverwendung über Ansichtswechsel ohne eigene Prüfung. Befehle lesen aktuelle Objekte über IDs, weil Undo Objekte ersetzt.
- **Invalidierung vollständig:** Titel, Pfad, Labels, Status, Termine, Wichtigkeit, Notiz-/Bildinhalt, Archiv, Reihenfolge, Tageswechsel, Kartengröße, Schrift und Design.
- **Layout bündeln:** `ButtonFlow` sammelt `add`/Configure zu einem Leerlauflayout (explizites `reflow` bleibt synchron); `DeferredDrawCanvas` zeichnet gerundete Flächen einmal je Leerlauf; Umbruchbreite und Hintergrundfarbe nur bei Änderung setzen; `bind_main_window_resize` filtert Größenmeldungen in Tcl. Synchrone Höhenleser brauchen vorher ein fertiges Layout (Zeichnungs-Kontextleiste: `row.reflow()`).
- **Canvas-Widgets** binden `<Configure>` über `bind_resize` (zeichnen nur bei Größenänderung). Bilder nur in sichtbaren Teilen zeichnen.
- **Aktionsleisten** (`refresh_page_actions`) überspringen den Aufbau nur bei identischen Specs einschließlich Befehl; ersetzte Configure-Bindungen werden abgemeldet.
- **Schriften** je Tk-Interpreter zwischengespeichert (`app_font`), `apply_ui_font` invalidiert.
- **Formatsicherung** merkt Dateistand und Formatnummer (`schema_backups.py`); kein erneuter JSON-Parse nach dem Laden. Unter Windows gehört der vollständige SHA-256-Inhalt zur Signatur, weil gleich große In-place-Schreibvorgänge selbst native ChangeTime unverändert lassen können. POSIX behält die Metadatensignatur mit ctime. Der zusätzliche Windows-Leselauf bleibt Bestandteil der Speicherwegmessung P08.
- **Live-Suche** fasst Änderungen mit `after_idle` je Ereigniszyklus zusammen; Rich-Text-Autosave wartet 400 ms und wird vor Seitenwechsel und Ausgabe geleert.
- Keine pauschale Ersetzung von Datenschlüsseln oder `theme[...]`-Zugriffen durch Variablen; das bringt keinen belegten Gewinn.

Ereignisgrenzen: `item_change` → Speichern/Verlauf/Ansicht; `sidebar_change` → Speichern/Seitenleiste; Designwechsel → zentrale Stile; Import/Restore normalisieren vollständig vor dem Neuaufbau. Eine zweite Benachrichtigungsschicht daneben ist bewusst nicht eingeführt (Risiko doppelter Aktualisierungen).

## 5. Tk-Fallstricke (teuer gelernt)

### Ereignisse, Menüs, macOS

- **Kein `update()`/`update_idletasks()` in Rückrufen, die sich selbst auslösen können** (Scroll-, Configure-, Leerlauf-Rückrufe). Die Bildplatzierung lief so bis zum `RecursionError`. Ein `RecursionError` in flachen Rückrufen (`sync_backdrop_surfaces`, `draw_icons`) im Fehlerprotokoll heißt: nach verschachteltem `update` suchen; Nachweis über Stapeltiefe wie in `test_etappe1_332`.
- **Menübefehle unter macOS** laufen, während das Menü noch verfolgt wird. Ein modales Fenster direkt aus dem Befehl friert die App ein (Hänger 29./30.09.2026); deshalb `after_idle` für jeden Befehl, auch `::tk::mac::Quit`. Tests, die `menu.invoke()` rufen, müssen danach `update()` ausführen.
- **`after`-Aufträge** an `<Destroy>` des Hauptfensters binden und abbrechen, sonst „invalid command name“. `<Configure>`-Rückrufe laufen beim Schließen noch einmal: vor neuen Kindern `winfo_exists()` prüfen.
- **`bind(…, add="+")`** hängt bei jedem Aufruf eine weitere Bindung an; `add_tooltip` hält deshalb genau eine Bindung je Widget.
- **Bindtags:** Ein Widget bekommt nie das Bindtag seines Rahmens, um Ereignisse weiterzugeben – dann erreichen den Rahmen auch fremde `<Configure>`-Meldungen, unter macOS bis zum Tk-Absturz (`XMoveResizeWindow`). Stattdessen eigenes Bindtag mit `event_generate` (`GlideBackdrop`).
- **Treeview:** `TreeviewOpen` kommt vor dem Umschalten – Zustand erst im Leerlauf lesen. `Treeview.see` öffnet alle Vorfahren. Drag-Bindungen mit `break` prüfen, welche native Funktion (z. B. Klapppfeile) sie unterdrücken.
- **`<TouchpadScroll>`** (Tk 9, TIP 684): `delta` trägt X in den oberen, Y in den unteren 16 Bit, jeweils mit Vorzeichen.
- **Schwebende Fenster:** `withdraw()`, positionieren, `deiconify()` – sonst wandern sie unter macOS sichtbar.
- **Dialoge nicht nachträglich umfärben:** Farben beim Aufbau aus `self.theme` nehmen; Umfärben nach dem Zeigen ließ Tk endlos neu anordnen.

### Layout und Pack

- **Pack-Reihenfolge entscheidet:** Wer zuerst gepackt ist, bekommt zuerst Platz; `expand` verteilt nur den Rest. Feste Knöpfe vor dehnbare Felder. Neu packen hängt hinten an – wer Knöpfe ein- und ausblendet, packt die ganze Reihe in fester Reihenfolge neu (`pack_header_controls`).
- **Nichts auspacken, was sich andere merken:** Pinnwand und Reiter merken sich `pack_slaves()`; zum Verstecken leeren statt auspacken.
- **Leere Rahmen schrumpfen nicht:** `grid_propagate(False)`/`pack_propagate(False)` und `height=1`. `winfo_reqwidth()` stimmt erst nach dem Leerlauf; direkt nach Änderungen die Kinder messen (`packed_width`).
- **Widgets lassen sich nicht umhängen:** Sie gehören dem gemeinsamen Elternrahmen und werden mit `pack(in_=zeile)` gesetzt; heben mit `widget.tk.call("raise", widget._w)` – `Canvas.lift` hebt nur Zeichenelemente.
- **Tk 9 blendet eingebettete Rahmen wieder ein:** Ein Rahmen in einer ausgepackten Leinwand (`create_window`) erscheint nach einer Änderung darin wieder (`winfo_ismapped` = 1). Den Inhalt einer ausgeblendeten Karte deshalb nicht umpacken. Für schwebende Flächen einen Rahmen mit `place` nehmen, nicht `create_window`.
- **macOS malt frei gewordene Flächen nach `pack_forget` nicht immer neu:** Hintergrundfarbe des Elternrahmens neu setzen (`repaint_sidebar`).
- **Keine transparenten Flächen in Tk:** `Frame` mit `bg=""` zeigt unter Windows Bildreste. Jede Fläche zeichnet ihren Ausschnitt selbst (`photo copy -from … -shrink`).
- **`CanvasLabel` misst wie ein Label** (`LABEL_INSET_X/Y`), sonst verrutschen getestete Höhen. Beim Neuaufbau meldet das Hauptfenster kurz 1 px; Höhenstufen ignorieren das.

### Text-Widget

- **`place` im Textfeld:** Unter Tk 9 liegt der Ursprung am Innenabstand, unter Tk 8.6 am Rand; `PageEditor.place_origin` misst einmal je Programmlauf, ob Tk ihn mitzählt.
- **Umfluss:** `lmargin1`/`lmargin2`/`rmargin` wirken je Anzeigezeile nach dem Tag ihres ersten Zeichens. Anzeigezeilen misst `count -update -ypixels`; `dlineinfo` liefert für unsichtbare Zeilen nichts.
- **Formate beim Tippen:** Eingefügter Text erbt nur Formate beider Nachbarzeichen; Zeilenformate schließen den Umbruch ein, `spread_line_tags` überträgt sie. Eingebettete Fenster zählen als ein Index, fehlen aber in `get()`.

### Zeichnen und Bilder

- **Die Leinwand glättet unter Windows und X11 nicht:** Flächen, Linien und Bögen (`create_polygon`, `create_line`, `create_arc`) rastert Tk dort ohne Kantenglättung, auch unter Tk 9; nur macOS glättet. Geneigte Kanten werden treppig. Glatte Formen entstehen nur als Bild: SVG über Tk 9 (`logo_photo`) oder ein vorgerechnetes PNG mit Alphakanal. Gefunden am Logo-Rückfall unter Tk 8.6 ([Diagnose](diagnosen/LOGO_KANTENGLAETTUNG.md)).
- **`PhotoImage.subsample` und `zoom` filtern nicht:** Sie übernehmen jedes n-te Pixel bzw. vervielfachen es. Verkleinerte Symbole in Zielgröße vorrechnen oder unter Tk 9 das SVG in Zielgröße laden.
- **Rückfallwege brauchen ein Qualitätskriterium:** Ein Test, der beim Rückfall nur Elementtyp, Farbe und Rahmen prüft, bleibt grün, während die Darstellung unbrauchbar ist.

### Daten und Objekte

- **Detailbereich:** übergibt `item_change` bewusst `()` und ruft `change.mark()`, sonst springt die Auswahl zurück. Wiederholungsregel und Beziehungen teilen Maske und Bereich (`read_repeat_rule`, `add_relation_targets`).
- **Nach Rückgängig sind Listenobjekte neu:** Referenzen frisch aus `app.lists` holen.
- **`copy.deepcopy` für Schnappschüsse** ist so schnell wie komprimiertes JSON, braucht aber rund zehnmal so viel Speicher.
- **Bytecode:** `app.pyw` setzt `sys.pycache_prefix` (`bytecode_cache_dir`) vor dem Import der Module.

### Tests

- `DrawingEditor` beendet beim eigenen `<Destroy>` die Aufträge für Kontextzeilen, Größenanpassung, Vorschau und Speichern. Vor dem Seitenwechsel überträgt `flush_drawing_editor` offene Pixel; der Abbaucallback speichert nicht erneut. Widgetabbau allein löscht die Tcl-Timer nicht. `test_editor3338` prüft die Timerkennungen und den Dateistand bei acht Wechseln.

- `event_generate("<Return>")` erreicht ein Feld nur mit Tk-Fokus. Hintergrundläufe ersetzen `focus_force()` durch `focus_set()`; echter OS-Fokus bleibt manuelle Plattformprüfung.
- Neue modale Dialoge auf bestehenden Wegen lassen ältere Tests warten: `run_modal` im Test ersetzen und den Knopf drücken.
- `root.update()` in einer schnellen Schleife lässt `after`-Aufträge liegen; zwischen den Runden kurz Zeit vergehen lassen. Kurze Animationen (Fahne 0,5 s) direkt nach dem Auslösen prüfen.
- In Messwerkzeugen nur erwartete Tk-Fehler abfangen; ein abgefangener `AttributeError` lieferte einmal eine falsche Null.
- Fensteraufnahmen nur vom eigenen Fenster: unter macOS `screencapture -l <Fensternummer>`, nie `-R`; unter Windows `PrintWindow` (`save_windows_screenshot` in `tests/tools/releasedaten.py`).
- **Design statt `theme_name` setzen:** `apply_theme` leitet `theme_name` aus dem Design ab (`_compose_theme`); eine direkte Zuweisung wirkt nicht. Tests und Erzeuger wechseln mit `set_design(key, apply_now=False)` und danach `apply_theme()`. Die Windows-Dunkelaufnahme war deshalb bis 05.10.2026 eine zweite helle Aufnahme; `test_ui_updates` und `test_ui_polish36` enthalten die wirkungslose Zuweisung noch (Entwicklungsplan W02).
- Prüffenster laufen unter macOS im Hintergrund (`tests/tools/hintergrund/sitecustomize.py`: Aktivierungsrichtlinie Zubehör). Das schirmt die Maus ab, **nicht die Tastatur** – während einer Vollprüfung nicht tippen und den Mac nicht sperren.

**Gestaltung seit 3.33.12 (OB01):** `ui_design.py` enthält unveränderliche Skalen mit den vorhandenen Zahlen für Abstand, Radius, Schriftgröße und Zeilenhöhe; Hauptfenster/Kopf sowie gemeinsame Karten- und Feldkonstanten verwenden sie. Die Übernahme ist schrittweise und keine neue Designentscheidung. `fit_text` und `today_columns` berechnen text- bzw. breitenabhängige Darstellung ohne Tk. Die Quelle wird je Baumaufbau nach Zeilen-ID vollständig gemerkt; Breiten-/Schriftwechsel passen nur ihre Darstellung an, Undo ersetzt den Aufbau. Die gedämpfte Zelle verwendet die native [Tk-9-Zellmarkierung](https://www.tcl-lang.org/man/tcl9.0/TkCmd/ttk_treeview.html), ohne Overlay oder neue Bindungen; ein älteres Tk fällt auf die normale Zeilenfarbe zurück. Keine neuen Timer.

**Planungswege seit 3.33.13:** `ListApp.planning_summary` bleibt kompatible Schnittstelle zur Tk-freien Bilanz. Quick-Plan-Menüs halten ausschließlich Punktkennungen, frische Objekte werden je Aktion nach Undo aufgelöst. Heute-Auswahl löst zusätzlich ihre Quelllistenkennung auf; die allgemeine Listenbindung anderer Aktionen wird nicht erweitert. `item_change(local=True)` speichert die betroffenen Listen gemeinsam, No-op ohne Undo; fehlgeschlagene Speicherung meldet keine erfolgreiche Planung. Der Menüaufbau scannt den Bestand einmal für alle Zielvorschauen; ein gemeinsamer Stichtag und festgehaltene ISO-Ziele erhalten Datum und Bilanz über Mitternacht. Die optionale Zeilenaktion merkt nur Ansicht/Zeile/Punktkennung und wird bei Neuaufbau, Scrollen und Größenwechsel entfernt. Keine neuen Timer oder Datenfelder.

Seit 3.33.15 bündelt `PageEditor.task_change` Text und Aufgaben in einem `item_change` (ein Undo, eine Speicherung). Die bestehenden Speicher-/Mutationswege bleiben die Adapter; Wiederherstellen im Editor ist auf neu zurückgekehrte Heimatzeilen begrenzt. `task_references.target_index` löst Ziele einmal je Aufgabenaufbau auf, ohne langlebigen Cache; Undo/Import/Neustart verwenden aktuelle Objekte. Gespeicherte Filter erhalten additiv die Quellenwahl. `page_markdown.insert_blocks` trennt überschneidende Formatbereiche und bewahrt Bilder/Links; Export löst Aufgabenzustand und Titel über dieselbe ID auf.
