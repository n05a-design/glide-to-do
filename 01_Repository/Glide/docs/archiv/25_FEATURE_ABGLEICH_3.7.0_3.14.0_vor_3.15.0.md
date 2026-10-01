# Funktions- und Auftragsabgleich – historische Matrix mit 3.13-Nachtrag

Aktueller Entwicklungsstand: **3.14.0 / Aufgabenformat 14** mit Bearbeitungstag und Aufwand. [Bedienung 3.14](37_PLANUNG_UND_AUFWAND_3.14.0.md), [QA](07_QA_BERICHT.md). Die folgenden Befunde gehören zum jeweils angegebenen älteren Stand.

Stand: 12.09.2026 · Quellstand `src/glide/app.pyw` · Datenformat 12

Dieses Dokument beschreibt die historische 3.7-Matrix. Der aktuelle Ausbau bis
3.14 steht in der [Funktionsübersicht](../../../00_Arbeitsvorbereitung/Glide_Funktionsvorschlaege_2026-09-11.md),
der [Tabellenansicht](36_TABELLENANSICHT_3.13.0.md) und den aktuellen technischen
Dokumenten. Die 3.6-Fassung bleibt
als historische Referenz im [Archiv](archiv/20_FEATURE_ABGLEICH_3.6.0_vor_Nachbesserung_2026-09-11.md) erhalten.

## Ausbau bis 3.14.0

Die frühere Matrix bleibt für Nachweise und Regressionen unverändert lesbar.
Seitdem wurden Erinnerungen, Reiter, Pinnwand, Schnellerfassung, gespeicherte
Filter, „Mein Tag“, die kompakte Tabellenansicht sowie Bearbeitungstag und
Aufwand umgesetzt. Die Tabellen-
ansicht verwendet dieselben Aufgabenobjekte und speichert ihre Spalten je Liste
in den persönlichen Einstellungen. Der [QA-Bericht](07_QA_BERICHT.md) weist
den geprüften 3.13-Stand mit siebzehn Testsuiten nach; für 3.14.0 mit achtzehn
Suiten steht der bestätigende Gesamtlauf noch aus.

## Ursprünglicher Auftrag mit 22 Punkten

Die folgende Matrix führt den früheren Auftrag mit seinen Nachweisen weiter.
Die anschließende Tabelle beschreibt die späteren UI-Korrekturen und die
Ergänzungen von 3.7. Bei Darstellungsdetails gilt die jeweils neuere Angabe.


| Nr. | Wunsch / bestätigte Ergänzung | Weitergeführte Funktion in 3.7.0 | Beleg und praktische Grenze |
|---|---|---|---|
| 1 | Links Symbole mittig, Hauptpunkte links auf einer Achse; zwei Spalten | Umgesetzt: feste Symbolspalte, eigene Titelspalte, Zähler rechts; alle sieben Systemansichten sichtbar. Unterer Listenbaum behält seine Hierarchie. | `create_ui`, `update_sidebar_list`, Geometrieprüfung in `test_glide`. Einrückung von Unterordnern bleibt absichtlich erhalten. |
| 2 | Textlogo in Startseite und Vorschau zentrieren | Umgesetzt anhand tatsächlicher Canvasgröße und Schriftmetriken; Neuzeichnung bei Größenänderung. | `MonogramBadge`; Windows-Bilder Startseite/Einstellungen. Optischer Ausgleich hängt weiterhin von Glyphenform ab. |
| 3 | Alle Startseiten-Buttons mit Kontur in eigener Farbe | Umgesetzt, einschließlich Verweise zu Listen, Vorlagen und Systemansichten. Rahmen bleiben unter Windows sichtbar. | `home_action_button`, Startseitenbilder Hell/Dunkel. |
| 4 | Art farbig, Long-Task/Überschrift wie festes Label | Umgesetzt in gemeinsamer Punktmaske und Art-Kontextmenü. | `kind_color_key`, `item_form_dialog`, `build_item_context_menu`; UI-Suite. |
| 5 | Zugehörige Liste überall in Listen-/geerbter Ordnerfarbe | Umgesetzt in Punktmaske, Verschiebeauswahl und Kontextaktionen; Hierarchiepfade bleiben lesbar. | `list_color_key`, `themed_choice_dialog`, `_make_option_menu`; UI- und App-Durchlauf. |
| 6 | Neue Liste / neuer Ordner mit mehr Angaben | Umgesetzt: Titel, Farbe, Elternordner, Labels, Beschreibung, passende Listen-/Ordnervorlage; scrollbar, Aktionen am unteren Rand. | `create_container_dialog`; echter Anlage-Rundlauf einschließlich Labels und Beschreibung. |
| 7 | Schriftdatei mitnehmen, keine Installation pro Arbeitsplatz | Umgesetzt mit vier mitgelieferten DejaVu-Sans-TTF-Schnitten und Lizenz. Private Registrierung vor Aufbau der UI, Familienwahl und drei Schriftgrößen. | `register_private_fonts`, `app_font`, `apply_ui_font`; Windows prüft vier Registrierungen und verwendete Familie. macOS-Pfad automatisiert geprüft; native Sichtabnahme bleibt offen. |
| 8 | Cloud-Modus / Zeigerdatei / Sperrdatei | Umgesetzt als frei wählbare Datenablage mit Kopieroption in einen leeren Zielordner, Öffnen vorhandener Daten, Standardordner und Pfadanzeige. Zeiger gerätespezifisch. Erkannte Fremdsperre führt zu Warnung und Schreibschutz. | `change_data_folder`, `acquire_data_lock`, `save_items`; Kopier- und Sperrtests. Kein Synchronisationsdienst und keine verteilte Transaktion. |
| 9 | Einstellungen: Abstand links korrigieren | Umgesetzt: Innenabstand, breiterer zweispaltiger Dialog und Scrollbereich; Speichern/Abbrechen bleiben erreichbar. | `show_settings_dialog`; Windows-Dialogbilder. |
| 10 | Links-Klick plus verzögerter Links-Klick zum Umbenennen | Umgesetzt für Listen/Ordner und einzeilige Aufgaben-/Gruppen-/Überschrifttexte. Doppelklick/F2 bleiben bei Punkten der Detailweg. | `begin_sidebar_rename`, `begin_item_rename`, Drag-/Klickabgrenzung. Long-Tasks bleiben entsprechend Übergabe in der mehrzeiligen Maske. |
| 11 | Runde Auswahl, Hover unverändert | Teilbereich umgesetzt: Labelauswahl und ausgewählter Kalendertag verwenden selbst gezeichnete runde Auswahl. | `LabelDropdown`, `LabelChip`, `DueField`; UI-Suite. Native Treeview-Balken und native Menüs bleiben rechteckig: vom Nutzer nach Erklärung akzeptierte Grenze. |
| 12 | Vorlagenseite für System-Listen/Ordner, Bearbeiten/Speichern | Umgesetzt: zehn Listen- und sechs Ordnervorlagen beim ersten Start. Eigener Katalog, expliziter Bearbeitungsmodus, Bearbeiten/Löschen, Speichern; Rückfrage bei ungespeicherten Änderungen beim Schließen. | `refresh_template_page`, `edit_template`, `toggle_template_editing`, `on_close`; echter Speichern-Rundlauf. |
| 13 | Vorlagen exportieren; Listen/Ordner importieren | Umgesetzt: `.glidetemplates` ergänzt den Katalog; „Listen/Ordner hinzufügen“ ergänzt den Aufgabenbestand. Eigene Listen/Ordner lassen sich einschließlich Struktur und Anhängen als Vorlage speichern. | `capture_template`, `validate_template_payload`, `import_templates_file`, `import_partial_backup`; neue IDs, Dateibytes und leere Unterordner geprüft. |
| 14 | Verweis zur Vorlagenseite auf Startseite | Umgesetzt im Aktionsbereich der Willkommen-Kachel; Vorschaukachel verwendet den tatsächlichen Katalog. Bewusst geleerter Katalog bleibt leer. | `home_template_keys`, `set_template_view`; UI-Suite. |
| 15 | Nur Startseiten-Scrollbar weiter nach rechts | Umgesetzt mit Scrollleiste im äußeren Rand. | `create_ui`; Startseitenbilder. |
| 16 | Kontextmenü: Liste/Ordner exportieren | Umgesetzt als TXT, Markdown und portable Glide-Datei. Teilbackup behält Farben, Labels, Wiederholungen, Unterpunkte, Anhänge und leere Unterordner. | `export_list_as`, `export_folder_as`, `partial_backup_payload`; Dateirundlauf in `test_release36`. TXT/Markdown sind lesbare Exporte, kein verlustfreier Rückweg. |
| 17 | Weitere analoge Elemente prüfen | Mondphase ist als ausdrücklich gewählter Vorschlag umgesetzt. Weitere Vorschläge sind unten bewertet. | `MoonPhase`, `moon_phase_info`. |
| 18 | Mondphase neben analoger Uhr | Umgesetzt: geometrische Mondsichel, Phasenname, beleuchteter Anteil; einzeln abschaltbar. | Datumsprüfungen + Windows-Bild. Näherungsrechnung für Dekoration, kein astronomisches Ephemeridenprogramm. |
| 19 | Jahresanzeige unter Bestand, Lila je Aktivität | Umgesetzt: Tagesraster über 53 Kalenderwochen bis heute, Intensität aus erfolgreichen Aufgabenänderungen in der gewählten Akzentfarbe, aktive Tage, Summe, bester Tag, laufende Serie. | `record_recent_list_edits`, `YearHeatmap`; rollierende lokale Tageshistorie, Zukunftstage ausgeblendet. Ältere gespeicherte Abschlüsse dienen als Rückfallwert. Keine nachträglich erfundene Bearbeitungshistorie oder Zeiterfassung. |
| 20 | Mehr Personalisierung | Umgesetzt: Akzentfarbe, Schriftgröße, Startansicht, Wochenbeginn, Sekundenzeiger, Mondphase, Jahresanzeige und Materialoptik; Name/Monogramm/Bestandsstatistik/Tagesziel bleiben. | `normalize_personal_settings`, `show_settings_dialog`; Einstellungen Version 2. |
| 21 | Moderne Glasoberfläche untersuchen und anwenden | Umgesetzt als abschaltbare Materialoptik: getönte Flächen, helle Kante, Schatten, ruhige Inhaltsebene; optionaler Windows-DWM-Aufruf. Umfangreiche Gegenüberstellung nativer Alternativen vorhanden. | [Glasbericht](<archiv/19_GLASS_SURFACE_3.6.0_vor_Nachbesserung_2026-09-11.md>). Die Tk-Clientfläche zeigt keinen nachgewiesenen echten Desktop-Blur. |
| 22 | Alle Dokumentationen, Feature- und Leistungsberichte aktualisieren | Aktuelle Architektur, Produktgrenzen, Daten-/Backuphandbuch, QA, Übergabe, Funktionsmatrix, Materialbericht und reproduzierbare Leistungsaufnahme zusammengeführt. | [Index](00_INDEX.md), aktuelle 3.7-Dateien in den äußeren Projektordnern. Versionierte historische Nachweise bleiben erhalten. |

## Nachfolgende UI-Korrekturen und Ergänzungen

| Bereich | Stand 3.7.0 | Nachweis |
|---|---|---|
| Einheitlicher Buttonstil | Import, neuer Ordner und alle Aktionsleisten teilen Farben, Konturen und Hover-Verhalten. | Button-Helfer, UI-Screenshots |
| Startseitenkachel | Eingang, In Bearbeitung, Verspätet, Kalender, Vorlagen, Neue Liste und Einstellungen liegen gemeinsam in der Willkommen-Kachel; bei schmaler Breite bleiben Eingang, Vorlagen und Einstellungen sichtbar. | Startseiten-UI-Suite |
| Kalender und Mondphasen | Kalender ist in den Startseitenbereich integriert; die absolute Mondphase kann in der Kopfzeile und am Kalendertag angezeigt werden. | Kalender-/Mondphasen-Suite |
| Jahresanzeige | Raster und Statistik haben dieselbe Breite; Montag beginnt an der korrekten Rasterposition, letzte Tage werden nicht abgeschnitten. Hover zeigt Wochentag, Datum und Zahl. | `YearHeatmap`, Tageshover-Screenshot |
| Vorlagenlayout | Keine künstliche Zusatzzeile, linksbündige Beschreibung, getrennte Spalten für Name/Beschreibung/Aktionen, Kachelradius wie im übrigen UI und kein Leerraumscrollen. | Vorlagen-Screenshots |
| Vorlageneditor | Isolierter Entwurf, App-Baumstil in Hell/Dunkel, dynamische Metadaten, erhaltene geschlossene Zweige, Labels, Anhänge und relative Termine. | `TemplateDraft`, `edit_template`, `test_template_workflows` |
| Mac-Auswahlfelder | Thematisiertes Feld und Popup mit Tastaturauswahl, Escape und modaler Grab-Rückgabe; bisheriger Windows/Linux-Pfad bleibt erhalten. | `MacOptionMenu`, `_make_option_menu`, `test_template_workflows` |
| Vorlagenaktionen | Aktionen sitzen in der bekannten unteren Leiste und brechen bei schmalem Fenster kontrolliert um; Löschen nutzt das Papierkorb-Symbol, Bearbeiten bleibt beschriftet. | Vorlagen-UI-Suite |
| Listen-/Ordner-Symbole | Vorlagen und Kachelübersicht verwenden Textsymbole für Listen und Ordner. Das Symbol an der Überschrift „Listen“ sitzt in 3.7 tiefer; die anderen Navigationssymbole behalten ihre Achse. | zentrale `ICONS`-Tabelle, `sidebar_heading_icon` |
| Aufgaben-/Ordnerarten | Automatische Farben werden je Auswahl eindeutig vergeben; Wiederholungen innerhalb der Auswahl werden vermieden. | Art-Auswahl-Suite |
| Labelauswahl | Vorhandene Labels reagieren auf Hover; Auswahlbereich ist scrollbar; „+ Neues Label“ und „Fertig“ stehen als hervorgehobene, feste Abschlussleiste bereit. | Label-Screenshot |
| Einstellungen | Einstellungsfenster ist zweispaltig angelegt, breiter statt unnötig hoch; Textlogo liegt optisch höher; Akzentfarbe steuert die Auswahlfarbe und startet standardmäßig lila. | Dialog-Suite, beide Themes |
| Listen-/Ordner-Kachelansicht | Klick auf „Listen“ zeigt alle Listen und Ordner in 1–3 unabhängig gestapelten Spalten mit eigener Inhaltshöhe, 16 px Innenabstand, 12 px Zwischenraum und ohne zusätzliche Typzeile. | `refresh_library_page`, `test_ui_followup36`, [Geometrie](../tests/qa-3.7.0/dynamische-kacheln/geometrie.json) |
| Kachelaktionen | „Liste/Ordner öffnen“ und „Liste/Ordner bearbeiten“ umbrechen vollständig; Tastaturfokus scrollt die Aktion ins Sichtfeld. Details umfassen Titel, Beschreibung, Farbe, Labels und Anhänge. | Seitendetails-Screenshots |
| Anhänge und Datenablage | Anhänge werden für Container unterstützt, auf sichere Pfade geprüft und in Backup, Import, Vorlage, Kopie, Papierkorb und Restore mitgeführt. | Release-37-Integrationssuite |
| Migration | Datenformat 11 wird nach 12 migriert; vor dem ersten Schreiben wird eine Originalkopie angelegt. | Migrations- und Schreibschutztests |
| Bildlaufstabilität | Startseite, Vorlagen, Labelauswahl und Kacheln propagieren Mausrad-Ereignisse korrekt und hängen am unteren/oberen Rand nicht. | Scroll-Suite |
| Statistik nach Löschen | Historisch aufgezeichnete Tagesbearbeitungen bleiben in den Aktivitätsdaten und damit in der Statistik erhalten, auch wenn erledigte Aufgaben aus dem Bestand gelöscht werden. | Statistik-Suite |
| Dokumentation und Release | Version, Funktionsübersicht, QA, Datenmigration, Bestandsanalyse, Abschlussbericht, äußere Arbeitsdokumente und Produktdatenblatt sind auf 3.7.0/Format 12 aktualisiert. | `docs/00_INDEX.md`, Dokumentationsprüfung |

## Personalisierung und weitere Gestaltungsideen

Akzentfarbe, Schriftgröße, Startansicht, Wochenbeginn, Name, Textlogo, Tagesziel
und die Schalter für Uhr, Mondphase, Jahresanzeige und Materialoptik sind
umgesetzt. Frei wählbares Datumsformat, Kachelreihenfolge, Standardliste und
Begrüßungston bleiben Erweiterungsideen. Tagesring, Zeigerinstrument, Sanduhr,
Kalenderblatt, Wochenscheibe, Bestandszähler, Registerkarten, Stecktafel und
Balanceanzeige sind bewertet, aber nicht als zusätzliche Funktionen umgesetzt.
Die frühere Bewertung steht im [Abgleich 3.6](<archiv/20_FEATURE_ABGLEICH_3.6.0_vor_Nachbesserung_2026-09-11.md>).

## Statistik und Aufbewahrung

Gebuchte Erledigungen bleiben beim Löschen einer Aufgabe erhalten. Der aktuelle
Bestand zählt nur vorhandene Aufgaben. Die Tageshistorien werden rollierend
aufbewahrt und liegen in `settings.json`; Aufgabenbackups enthalten sie nicht.
Fehlende ältere Ereignisse lassen sich aus bereits gelöschten Aufgaben nicht
rekonstruieren. Details: [Statistik und Datenmigration](24_VERSION_3.7.0.md).

## Technische Leitplanken

- Textzeichen bleiben die plattformübergreifende Symbolgrundlage; neue
  Bildabhängigkeiten sind nicht erforderlich.
- Schreibvorgänge verwenden atomare Dateien und bewahren Daten vor Migration
  und Import auf.
- Die vollständige automatisierte Prüfung ist reproduzierbar mit:

  `tests/tools/pruefen.py --modus voll --timeout 600 --protokoll tests/qa-3.7.0/automatisch`

## Prüfstand 3.7.0 und offene Freigaben

Der damalige kombinierte Prüflauf auf macOS/Python 3.14.5 bestand mit Exitcode 0:
elf Testsuiten, zwei statische Analysen sowie Beispiel-/Releaseabgleiche.
Die neuen UI-Änderungen wurden nicht auf einem Windows-System ausgeführt.
Frühere Windows-Protokolle belegen ausschließlich den damaligen Quellstand.
Native Sichtabnahme, physisches Trackpad, weitere DPI/Monitore, Screenreader,
Langzeitbetrieb, Installer und Signierung bleiben offen.

[Gesamtlauf](../tests/qa-3.7.0/dynamische-kacheln/abschluss/ergebnis.json) · [QA-Bericht](07_QA_BERICHT.md).

## Aktuelle Nachträge und Zukunftsideen

[Mac und vollständige Vorlagenbearbeitung](26_MAC_VORLAGEN_UND_ABLAGE_3.7.0.md) ·
[Dynamische Kacheln](29_DYNAMISCHE_KACHELN_3.7.0.md).

Erinnerungen hatten bei den Erweiterungen Vorrang und sind seit 3.8.0 umgesetzt
([Vertrag](31_ERINNERUNGEN_3.8.0.md)); diese Übersicht beschreibt den 3.7-Bestand.
Reiter und die erste Pinnwand sind seit 3.10.0 implementiert; [aktueller Bedienvertrag](33_REITER_UND_PINNWAND_3.10.0.md). „In Bearbeitung“
und Labels decken die Statusablage ab. Keine zusätzliche Projektmappe als
parallele Datenstruktur. Die [Vorschlagsdatei](../../../00_Arbeitsvorbereitung/Glide_Funktionsvorschlaege_2026-09-11.md)
ist eine Ideensammlung, keine pauschale Umsetzungsfreigabe.
