# Vollständiger Auftragsabgleich – Glide 3.6.0

Stand: 06.09.2026 · Grundlage: ursprünglicher Nutzerauftrag, bestätigte Ergänzungen und Claudes Übergabe. Maßgeblich ist der lokale Quellstand, nicht das überlieferte Linux-Prüfprotokoll.

## Ergebnis und Einordnung

Die 3.6-Funktionen sind im Repository implementiert. Der vorhandene Ansatz wurde
übernommen und in den tatsächlichen Bedienwegen vervollständigt. Behauptungen
wie „alles gebaut“ oder „Windows bestanden“ wurden nicht aus der Übergabe
übernommen. Der aktuelle Nachweis steht in [QA](18_QA_3.6.0.md); Messwerte stehen
im [Leistungsbericht](21_LEISTUNGSBERICHT_3.6.0.md).

„Umgesetzt“ bezeichnet nutzbaren Code. Die Grenze einer Plattform oder eine vom
Nutzer akzeptierte Ausnahme wird gesondert aufgeführt. Ein grüner automatischer
Lauf ersetzt keine macOS-, Mehrmonitor-, Screenreader- oder Langzeitabnahme.

## Jeder Punkt des ursprünglichen Auftrags

| Nr. | Wunsch / bestätigte Ergänzung | Ergebnis in 3.6.0 | Beleg und praktische Grenze |
|---|---|---|---|
| 1 | Links Symbole mittig, Hauptpunkte links auf einer Achse; zwei Spalten | Umgesetzt: feste Symbolspalte, eigene Titelspalte, Zähler rechts; alle sieben Systemansichten sichtbar. Unterer Listenbaum behält seine Hierarchie. | `create_ui`, `update_sidebar_list`, Geometrieprüfung in `test_glide`. Einrückung von Unterordnern bleibt absichtlich erhalten. |
| 2 | Textlogo in Startseite und Vorschau zentrieren | Umgesetzt anhand tatsächlicher Canvasgröße und Schriftmetriken; Neuzeichnung bei Größenänderung. | `MonogramBadge`; Windows-Bilder Startseite/Einstellungen. Optischer Ausgleich hängt weiterhin von Glyphenform ab. |
| 3 | Alle Startseiten-Buttons mit Kontur in eigener Farbe | Umgesetzt, einschließlich Verweise zu Listen, Vorlagen und Systemansichten. Rahmen bleiben unter Windows sichtbar. | `home_action_button`, Startseitenbilder Hell/Dunkel. |
| 4 | Art farbig, Long-Task/Überschrift wie festes Label | Umgesetzt in gemeinsamer Punktmaske und Art-Kontextmenü. | `kind_color_key`, `item_form_dialog`, `build_item_context_menu`; UI-Suite. |
| 5 | Zugehörige Liste überall in Listen-/geerbter Ordnerfarbe | Umgesetzt in Punktmaske, Verschiebeauswahl und Kontextaktionen; Hierarchiepfade bleiben lesbar. | `list_color_key`, `themed_choice_dialog`, `_make_option_menu`; UI- und App-Durchlauf. |
| 6 | Neue Liste / neuer Ordner mit mehr Angaben | Umgesetzt: Titel, Farbe, Elternordner, Labels, Beschreibung, passende Listen-/Ordnervorlage; scrollbar, Aktionen am unteren Rand. | `create_container_dialog`; echter Anlage-Rundlauf einschließlich Labels und Beschreibung. |
| 7 | Schriftdatei mitnehmen, keine Installation pro Arbeitsplatz | Umgesetzt mit vier mitgelieferten DejaVu-Sans-TTF-Schnitten und Lizenz. Private Registrierung vor Aufbau der UI, Familienwahl und drei Schriftgrößen. | `register_private_fonts`, `app_font`, `apply_ui_font`; Windows prüft vier Registrierungen und verwendete Familie. macOS-Pfad implementiert, hier nicht nativ geprüft. |
| 8 | Cloud-Modus / Zeigerdatei / Sperrdatei | Umgesetzt als frei wählbare Datenablage mit Kopieroption in einen leeren Zielordner, Öffnen vorhandener Daten, Standardordner und Pfadanzeige. Zeiger gerätespezifisch. Erkannte Fremdsperre führt zu Warnung und Schreibschutz. | `change_data_folder`, `acquire_data_lock`, `save_items`; Kopier- und Sperrtests. Kein Synchronisationsdienst und keine verteilte Transaktion. |
| 9 | Einstellungen: Abstand links korrigieren | Umgesetzt: Innenabstand, größerer Dialog und Scrollbereich; Speichern/Abbrechen bleiben erreichbar. | `show_settings_dialog`; Windows-Dialogbilder. |
| 10 | Links-Klick plus verzögerter Links-Klick zum Umbenennen | Umgesetzt für Listen/Ordner und einzeilige Aufgaben-/Gruppen-/Überschrifttexte. Doppelklick/F2 bleiben bei Punkten der Detailweg. | `begin_sidebar_rename`, `begin_item_rename`, Drag-/Klickabgrenzung. Long-Tasks bleiben entsprechend Übergabe in der mehrzeiligen Maske. |
| 11 | Runde Auswahl, Hover unverändert | Teilbereich umgesetzt: Labelauswahl und ausgewählter Kalendertag verwenden selbst gezeichnete runde Auswahl. | `LabelDropdown`, `LabelChip`, `DueField`; UI-Suite. Native Treeview-Balken und native Menüs bleiben rechteckig: vom Nutzer nach Erklärung akzeptierte Grenze. |
| 12 | Vorlagenseite für System-Listen/Ordner, Bearbeiten/Speichern | Umgesetzt: zehn Listen- und zwei Ordnervorlagen beim ersten Start. Eigener Katalog, expliziter Bearbeitungsmodus, Bearbeiten/Löschen, Speichern; Rückfrage bei ungespeicherten Änderungen beim Schließen. | `refresh_template_page`, `edit_template`, `toggle_template_editing`, `on_close`; echter Speichern-Rundlauf. |
| 13 | Vorlagen exportieren; Listen/Ordner importieren | Umgesetzt: `.glidetemplates` ergänzt den Katalog; „Listen/Ordner hinzufügen“ ergänzt den Aufgabenbestand. Eigene Listen/Ordner lassen sich einschließlich Struktur und Anhängen als Vorlage speichern. | `capture_template`, `validate_template_payload`, `import_templates_file`, `import_partial_backup`; neue IDs, Dateibytes und leere Unterordner geprüft. |
| 14 | Verweis zur Vorlagenseite auf Startseite | Umgesetzt im oberen Aktionsbereich; Vorschaukachel verwendet den tatsächlichen Katalog. Bewusst geleerter Katalog bleibt leer. | `home_template_keys`, `set_template_view`; UI-Suite. |
| 15 | Nur Startseiten-Scrollbar weiter nach rechts | Umgesetzt mit zusätzlichem seitlichem Abstand zur Inhaltsfläche. | `create_ui`; Startseitenbilder. |
| 16 | Kontextmenü: Liste/Ordner exportieren | Umgesetzt als TXT, Markdown und portable Glide-Datei. Teilbackup behält Farben, Labels, Wiederholungen, Unterpunkte, Anhänge und leere Unterordner. | `export_list_as`, `export_folder_as`, `partial_backup_payload`; Dateirundlauf in `test_release36`. TXT/Markdown sind lesbare Exporte, kein verlustfreier Rückweg. |
| 17 | Weitere analoge Elemente prüfen | Mondphase ist als ausdrücklich gewählter Vorschlag umgesetzt. Weitere Vorschläge sind unten bewertet. | `MoonPhase`, `moon_phase_info`. |
| 18 | Mondphase neben analoger Uhr | Umgesetzt: geometrische Mondsichel, Phasenname, beleuchteter Anteil; einzeln abschaltbar. | Datumsprüfungen + Windows-Bild. Näherungsrechnung für Dekoration, kein astronomisches Ephemeridenprogramm. |
| 19 | Jahresanzeige unter Bestand, Lila je Aktivität | Umgesetzt: Tagesraster über 53 Kalenderwochen bis heute, Intensität aus erfolgreichen Aufgabenänderungen, aktive Tage, Summe, bester Tag, laufende Serie. | `record_recent_list_edits`, `YearHeatmap`; 371 Tage lokale Historie, Zukunftstage ausgeblendet. Ältere gespeicherte Abschlüsse dienen als Rückfallwert. Keine nachträglich erfundene Bearbeitungshistorie oder Zeiterfassung. |
| 20 | Mehr Personalisierung | Umgesetzt: Akzentfarbe, Schriftgröße, Startansicht, Wochenbeginn, Sekundenzeiger, Mondphase, Jahresanzeige und Materialoptik; Name/Monogramm/Bestandsstatistik/Tagesziel bleiben. | `normalize_personal_settings`, `show_settings_dialog`; Einstellungen Version 2. |
| 21 | Moderne Glasoberfläche untersuchen und anwenden | Umgesetzt als abschaltbare Materialoptik: getönte Flächen, helle Kante, Schatten, ruhige Inhaltsebene; optionaler Windows-DWM-Aufruf. Umfangreiche Gegenüberstellung nativer Alternativen vorhanden. | [Glasbericht](19_GLASS_SURFACE_3.6.0.md). Die Tk-Clientfläche zeigt keinen nachgewiesenen echten Desktop-Blur. |
| 22 | Alle Dokumentationen, Feature- und Leistungsberichte aktualisieren | Aktuelle Architektur, Produktgrenzen, Daten-/Backuphandbuch, QA, Übergabe, Funktionsmatrix, Materialbericht und reproduzierbare Leistungsaufnahme zusammengeführt. | [Index](00_INDEX.md), aktuelle 3.6-Dateien in den äußeren Projektordnern. Versionierte historische Nachweise bleiben erhalten. |

## Personalisierung: Zusage gegenüber Ideensammlung

Claude nannte zusätzlich Datumsformat, Reihenfolge/Sichtbarkeit jeder einzelnen
Startseitenkachel, Standardliste für neue Punkte und frei wählbaren Begrüßungston
als Möglichkeiten. Seine konkrete 3.6-Zusage umfasste Akzentfarbe, Schriftgröße,
Startansicht, Wochenbeginn und die drei Schalter für Uhr/Mond/Jahr. Diese Zusage
ist umgesetzt. Für Datum, Kachelreihenfolge, Standardliste und Begrüßungston
besteht bislang kein ausgearbeiteter Bedien- und Speichervertrag; sie werden
hier als geprüfte Erweiterungsideen festgehalten, nicht als ausgelieferte Funktion.
Die vorhandene Startansicht bietet letzte Ansicht, Startseite und Vorlagen.

## Weitere analoge und nicht zeitbezogene Gestaltungsideen

| Idee | Nutzen | Entscheidung für diesen Stand |
|---|---|---|
| Mondphase | Ruhiges dekoratives Gegengewicht zur Uhr | Vom Nutzer gewählt und umgesetzt; abschaltbar. |
| Tagesring | Fälligkeiten im Tagesverlauf sichtbar | Sinnvoll bei vielen Uhrzeiten; braucht Überlagerungs-, Leerzustands- und Tastaturkonzept. |
| Zeiger für Tagesziel | Schnelles Ablesen des Tagesfortschritts | Möglich; aktueller Balken bleibt präzise und kompakt. |
| Sanduhr für Überfälliges | Anteil überfälliger Aufgaben sichtbar | Metapher kann Zeitdruck verstärken; keine Umsetzung ohne Auswahl. |
| Kalenderblatt / Wochenscheibe | Datum und Wochenfortschritt | Ergänzt bereits vorhandene Kalenderansicht, wäre teilweise doppelte Information. |
| Mechanischer Bestandszähler | Offene/erledigte Punkte als Zählwerk | Nicht zeitbezogen; sinnvoll nur ohne dauernde Animation. |
| Registerkarten / beschriftete Reiter | Listen als greifbare Sammlung | Nicht zeitbezogen; gute Richtung für Navigation mit klaren Textbeschriftungen. |
| Stecktafel mit Farbmarken | Verteilung nach Labels oder Projekten | Nicht zeitbezogen; muss zu denselben Daten wie die Labelansicht führen. |
| Balanceanzeige / Waage | Verhältnis offen zu erledigt | Nicht zeitbezogen; braucht Erklärung, damit keine neue Bewertung der Person suggeriert wird. |

Keine dieser nicht gewählten Ideen wird als offene Implementierung einer bereits
bestätigten 3.6-Zusage ausgegeben. Der Abgleich lässt sie sichtbar und bewertet.

## Datensicherheit und verbleibende Freigaben

Die bisherige einfache Teilimportkopie wurde durch den geprüften Backupweg mit
Schema-, Archiv- und Pfadprüfung, separater Anhangbereitstellung und Sicherung
vor dem Import ersetzt. Eine bekannte Fremdsperre darf nicht durch eigenes
Speichern überschrieben werden. OneDrive kann beim Offline-Parallelstart trotzdem
zwei gültig wirkende Arbeitskopien erzeugen; Glide führt diese nicht zusammen.

Die Freigabe für einen Store, Signierung, Anbieteridentitäten, reale Arbeit auf
zwei synchronisierenden Rechnern, macOS und die komplette DPI-/Accessibility-
Matrix bleiben gesonderte Freigaben. Sie sind im [QA-Bericht](18_QA_3.6.0.md)
und in der [Releasecheckliste](10_RELEASE_CHECKLIST.md) ausdrücklich aufgeführt.
