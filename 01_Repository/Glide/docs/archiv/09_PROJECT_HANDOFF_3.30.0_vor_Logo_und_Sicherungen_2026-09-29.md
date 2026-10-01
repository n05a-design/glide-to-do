# Projektübergabe – Glide 3.30.0

Stand 27.09.2026 · App 3.30.0 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

## Code und startbare Kopie

- **Kanonisch:** `src/glide/app.pyw` mit den Modulen `drawing.py`, `drawing_image.py`, `backdrop.py`, `page_markdown.py`, `image_preview.py` und `glide_start.py`,
  dazu `resources` und `vendor` (tkinterdnd2, seit 27.09.2026).
- **Startbare Kopie:** `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.30.0.pyw`
  samt denselben Modulen (`glide_start.py` heißt dort `Schnellstart.pyw`),
  `resources` und `vendor`. 3.29.0 und alle Zwischenstände von 3.30 liegen im
  Unterordner `Archiv`.
- Der äußere Projektordner ist kein Git-Checkout.

## 3.30.0 (25.09.2026)

Mit 3.30.0 ist der Modernisierungskatalog vom 25.09.2026 vollständig
umgesetzt.

**Grundlage:** Die Entscheidungen E-01 bis E-16 folgen alle der Empfehlung.
Zusätzlich wurden gewählt:

- verknüpfte Punkte;
- Vorlagen mit Eingabefeldern;
- echte Abhängigkeiten;
- Tagesbeginn und Wochenrückblick;
- Kapazität je Wochentag;
- Zeiterfassung;
- das Design „Pixel“.

**Maßgeblich** für alles Neue ist der
[Vertrag Modernisierung 3.30](66_MODERNISIERUNG_3.30.0.md). Er enthält Umfang,
Bedienung, Datenvertrag Format 20, Einstellungs- und Pinnwandschlüssel,
Architektur, Abweichungen vom Katalog und die mitbehobenen Fehler.

Die Planungsdokumente liegen außerhalb des Repositorys in
`00_Arbeitsvorbereitung/`:

- `Glide_Aufgabenkatalog_Modernisierung_2026-09-25.md` – jetzt mit Status je
  Paket;
- `Glide_Arbeitsvorbereitung_Modernisierung_2026-09-25.md` – Entscheidungen
  als „entschieden 25.09.2026“;
- `Glide_Wettbewerbsrecherche_Modernisierung_2026-09-25.md`.

Die Aufgabensammlung Zeichenfläche führt ZF-100, ZF-120, ZF-210 und die
Anlageoption „Pinnwand“ als umgesetzt.

**Ausbau am selben Tag** (alle Empfehlungen der Rückfrage gewählt):

- Zeitblöcke per Ziehen und Alt+↑/↓;
- Präsentation und Notizfolien als Druckseite bzw. PDF;
- Rückgängig beim Kartenverschieben;
- Detailbereich mit allen Feldern außer Anhängen;
- Gismo still in Leerzuständen;
- Pixelschrift „Pixelify Sans“ (SIL OFL 1.1) für Überschriften im Design
  „Pixel“.

Die Echtdatenprobe mit einer Kopie des Bestands fand einen Datenverlustweg in
3.29 (siehe unten).

**Zweiter Ausbau am 26.09.2026:**

- Anhänge im Detailbereich;
- Zeichnungen als Bild in Folien und Druckseite;
- Stundenraster in „Mein Tag“;
- Gruppierung mit Überschriften und durchgehender Nummerierung;
- Lasttest mit Härtung von `test_ui_followup36`;
- Windows-Prüfpaket;
- Entwurf des Produktdatenblatts 3.30 (`40_Store_Material`).

**Dritter Ausbau am 26.09.2026** (die bekannten Grenzen aus Vertrag 66):

- Punkte aus der Liste von „Mein Tag“ ins Stundenraster ziehen;
- gruppierte Tabelle mit Nummern und Zwischenüberschriften;
- Pixelschrift unter Linux über Fontconfig;
- mitbehoben: „Pinnwand öffnen“ aus der Tabelle.

**Kleine Fenster am 26.09.2026:** Bei Mindestgröße 860 × 700 bleibt das
Wichtigste, nichts ist gequetscht oder angeschnitten. Details stehen in
[Vertrag 66, Abschnitt 2.5](66_MODERNISIERUNG_3.30.0.md).
Dazu gehören Überschriften auch in der sortierten gruppierten Tabelle.

**Weitere Runde am 26.09.2026** (Details in Vertrag 66, Abschnitte 2.4–2.7):

- Dialoge bei Mindestgröße;
- Kontrast aller Designs nach WCAG AA;
- Stundenraster statt Liste in schmalen Fenstern;
- Einplanen über „Mein Tag“ in der Seitenleiste;
- Paketierung als Vorstufe mit den Kennungen `de.shaye.glide` und
  `Shaye.Glide`.

**Hintergrundverläufe am 26.09.2026:** fünf Verläufe je Design mit Lesezone,
Liquid-Glass-Tönung und Auswahl mit Vorschau (Vertrag 66, Abschnitt 2.8).

**Tk 9, Bilder in Seiten und feste Bestandteile am 27.09.2026** (Vertrag 66,
Abschnitt 2.14): Bilder in Seiten mit Umfluss, Verschieben und Größe;
Vorschauen über Tk 9 (`image_preview.py`); Ziehen aus Finder/Explorer
(`vendor/tkinterdnd2`); Systemmitteilungen (Option); „/“-Befehle;
wiederkehrende Checklisten; kein Ordnerpfad über dem Titel; feste Kopfzeile,
Werkzeugleiste und Fußbereich; runde Suche mit Schatten; schnelleres
Speichern und sofort sichtbares Fenster; Probedaten „Rundgang“.

**Kompression am 27.09.2026:** Titel höchstens 40 Zeichen (Kürzung beim
Laden mit Sicherung), Beschreibung nur in der Kennzahlenzeile, Klapppfeile
für Seiten und Listen, Bibliothek als Tabelle, „Notizbuch“ statt
„Tagebuch“, einheitliche Innenränder, Hinweise ohne Stapel (Vertrag 66,
Abschnitt 2.13). Offen: Titelbild und Unterseiten; eine Bildbibliothek für
JPEG unter Windows wäre eine Entscheidung über eine Laufzeitabhängigkeit.

**Aufräumen, Seitenbereich und Galerie am 27.09.2026:** Aktionsleiste nur
bei Auswahl, Kopfzeile aus Symbolen, Seitenleiste ohne Fußknöpfe, Umschalter
Liste · Tabelle · Pinnwand, Pinnwand in einer Zeile. Seiten haben einen
eigenen Bereich mit Vorlagen und dem Format `.glidepage`, dazu kommt die
neue Listenart „Galerie“ (Vertrag 66, Abschnitt 2.12). Felder, Darstellung
der Bibliothek und „Notizbuch“ statt „Tagebuch“ sind seit der Kompression
erledigt; offen bleiben Titelbild und Unterseiten.

**Seiten und Ordnertypen am 26.09.2026:** Seitenart „Seite“ für KI-Berichte,
Übersicht „Seiten“, Ordnertypen Ordner, Bibliothek und Notizbuch (Vertrag
66, Abschnitt 2.11). Als Nächstes: Glide-weite Felder, Titelbild und
Unterseiten; die Fragen dazu stehen im Konzept.

**Zweite Rückmeldung am 26.09.2026:** Punktdialoge bedienbar, Farben nach
Bedeutung, Aufräumen, deutlich schnellere Oberfläche (Vertrag 66, Abschnitt
2.10). Offen zur Entscheidung: das
[Konzept „Seiten wie Notion“](../../../00_Arbeitsvorbereitung/Glide_Konzept_Seiten_wie_Notion_2026-09-26.md).

**Rückmeldung am 26.09.2026:** Absturz beim Start behoben, Milchglas je
Kachel und Fenster, aufgeräumte Oberfläche (Verlauf als Knopf, „In
Bearbeitung“ in „Mein Tag“, gleiche Unterkanten, ruhige Zeichenfläche);
Vertrag 66, Abschnitte 2.8 und 2.9.

**Bewusst nicht umgesetzt:**

- Einstieg für neue Nutzer (nicht gewählt);
- eigene Felder je Liste (nicht gewählt, die Gesamtanalyse rät ab);
- ein führender Begleiter mit Hinweisen und Führung (setzt ein Onboarding voraus).

## Worauf man achten muss

- **Glide 3.29 nach der Umstellung nicht mehr starten.** 3.29 hält einen
  Format-20-Bestand für beschädigt, beginnt leer und überschreibt ihn bei der
  ersten Eingabe. Zurück geht es nur über `liste_vor_format20_*.json`.
  - 3.30 selbst öffnet neuere Formate schreibgeschützt
    (`_read_only_reason`).
  - Unlesbare Dateien sichert 3.30 als `liste_unlesbar_*` und warnt über
    `data_format_written`, wenn eine ältere Version zwischendurch
    geschrieben hat.
  - Beim nächsten Formatwechsel diesen Weg beibehalten.

- **Leistengrenzen:** Zeichnung, Startseite und Pinnwand blenden Leisten
  unabhängig voneinander aus.
  - `_refresh_tree` ruft zuerst `restore_note_chrome()` und
    `restore_drawing_chrome()`, erst danach ordnet die Pinnwand. Diese
    Reihenfolge nicht umdrehen.
  - Ist die Listenoberfläche ausgeblendet, legt `restore_drawing_chrome` die
    Leisten in die Merkliste der Startseite.
- **Gruppierung:** Gruppierung und Spaltenboard teilen `group_columns`,
  `item_group_keys` und `set_group_value`. Neue Felder dort ergänzen, nicht
  in einer Ansicht.
- **Pinnwand-Rückgängig:** Flächenänderungen, die mehrere Karten betreffen,
  laufen über `board_view_change` und sind so zurücknehmbar.
- **Zeichnungskarten:** Sie tragen `page:<Seitenkennung>`. `valid_cards`
  liefert Punkte und Seiten, `valid_items` nur Punkte.
- **Detailbereich:** Er übergibt `item_change` bewusst keine Kennungen. Sonst
  würde die Auswahl beim Übernehmen auf den alten Punkt zurückspringen.
  - Wiederholungsregel und Beziehungsaufnahme teilen Maske und Bereich
    (`read_repeat_rule`, `add_relation_targets`). Neue Regeln dort ergänzen.
- **Pixelschrift:** `pixel_heading_family` fragt Tk direkt, nicht die beim
  Aufbau gefüllte Familienliste – im Gesamttest fehlte die Schrift dort.
  `reapply_heading_fonts` setzt die Überschriften kurz nach dem Start neu.
- **Druckseiten:** Pinnwanddruck und Folien teilen `board_region_lines`;
  geöffnet wird über `open_print_html`. Zeichnungskarten liefert
  `drawing_data_uri` als PNG.
- **Gruppierte Liste:** Zwischenüberschriften sind synthetische Zeilen
  (`GROUP_HEADING_IID_MARKER`). `iter_tree_ids`, Klick und Ziehen überspringen
  sie wie Abstands- und Checklistenzeilen. Die Nummern kommen aus
  `list_view_number_paths`.
- **Stundenraster:** `sync_plan_day_grid` läuft nach jedem Aufbau. Änderungen
  gehen wie im Zeitplan über `apply_time_plan`.
  - Das Ziehen aus der Liste läuft über `on_time_plan_drag_*`.
  - Liegt der Zeiger über dem Raster, bestimmt `plan_grid_minutes_at` die
    Zeit aus Bildschirmkoordinaten; `plan_grid_drop` setzt sie.
- **Tabelle gruppiert/verschachtelt:** Die Baumspalte zeigt die Nummer aus
  `_table_number_paths`, die `fill_table_rows` nur während des Aufbaus setzt.
  Überschriften in der gruppierten Tabelle entstehen in
  `fill_grouped_table_rows` mit derselben Kennung wie in der Liste.
- **Kleine Fenster:** Neue Bedienelemente brauchen eine Antwort auf die
  Frage, was bei Mindestgröße mit ihnen geschieht.
  - Höhenstufen liefert `height_density`, die Breite der Kopfzeile
    `header_density`.
  - Knöpfe der Suchzeile werden vor `search_row_anchor()` gepackt.
  - `test_mindestgroesse330.py` misst jede Ansicht; ein neuer Befund dort ist
    ein Fehler, keine Messungenauigkeit.
- **Bindtags:** Ein Widget, das Ereignisse an seinen Rahmen weitergeben
  soll, bekommt nie das Bindtag des Rahmens. Dann erreichen den Rahmen auch
  fremde `<Configure>`-Meldungen, und sein Layout schaukelt sich auf. Unter
  macOS endet das in einem Tk-Absturz. Stattdessen gezielt weiterleiten, wie
  `GlideBackdrop` es tut.
- **Seitenaufgaben:** Aufgaben einer Seite laufen über die Wege in `ListApp`
  (`create_page_task` usw.), nicht direkt über den Baum. Die Seite hat keine
  sichtbare Punktliste.
- **Knopffarben:** Neue Knöpfe bekommen einen Bedeutungsschlüssel (confirm,
  delete, attention). Alles andere wird neutral (`button_color_key`); ein
  Farbwert statt eines Schlüssels wird nur als Grün oder Rot erkannt.
- **Canvas-Widgets:** `<Configure>` über `bind_resize` binden, nicht direkt.
  Sonst zeichnen sie bei jeder Verschiebung neu, beim Scrollen der
  Startseite hundertfach.
- **Dialoge nicht nachträglich umfärben:** Farben beim Aufbau aus
  `self.theme` nehmen. Ein Umfärben nach dem Zeigen ließ Tk im Punktdialog
  endlos neu anordnen.
- **Kopfzeilenknöpfe:** Ein neuer Knopf gehört in die Reihe von
  `pack_header_controls`, nie in ein eigenes `pack()`.
- **Kacheln mit Verlauf:** Widgets in einer Kachel nehmen deren Tönung
  automatisch an, wenn ihr Hintergrund die Kartenfarbe ist. Eine eigene
  Farbe bleibt eigene Farbe.
- **Hintergrund:** Neue Flächen in der Grundfarbe bekommen den Verlauf
  automatisch; Text darauf gehört in ein `CanvasLabel`. Ein `tk.Label` in der
  Grundfarbe stünde als Kasten auf dem Verlauf. Flächen, die ständig neu
  zeichnen, gehören in `backdrop_excluded`.
- **Farben:** Neue Schriftfarben laufen über die Rollen des Designs;
  `legible_text_roles` sichert sie ab. Knöpfe sichern sich über
  `RoundedButton.legible_text` selbst. Eine feste Farbe an einem Label ohne
  Designrolle umgeht das, und `test_kontrast330` findet sie.
- **Dialoge:** Jeder Dialog läuft über `run_modal`. Dort wird die
  Mindestbreite an den Inhalt angepasst.
- **Kennungen:** Die Kennungen `APP_BUNDLE_ID` und `APP_USER_MODEL_ID` dürfen
  sich nie ändern.
- **Schriften:** `register_private_fonts` registriert für den laufenden
  Prozess – Windows über `FR_PRIVATE`, macOS über CoreText, Linux über
  `register_fontconfig_dir`.
- **Windows:** Die Vollprüfung startet `tests/tools/windows_vollpruefung.cmd`;
  ihr Ergebnis gehört in QA-Bericht und QA-Verlauf.
- **Feste Bestandteile:** Eine neue Zeile über oder unter der Inhaltsfläche
  ist ein Fehler, solange sie nur in manchen Ansichten erscheint. Werkzeuge
  einer Ansicht gehören in `tool_band_host()`; `sync_tool_band` und
  `sync_foot_band` gleichen den Rest aus. Den Hinweis nie auspacken, um ihn
  zu verstecken – Pinnwand und Reiter merken sich die Zeilenordnung
  (`_hint_blank`). `test_festlayout330` misst es.
- **`place` im Textfeld (Tk 9):** Der Ursprung liegt am Innenabstand
  (padx/pady), unter Tk 8.6 am Rand – `PageEditor.place_origin` misst ihn.
- **Canvas.lift** hebt Zeichenelemente, nicht das Widget; für das Widget
  `widget.tk.call("raise", widget._w)`.
- **Zeitgeber in Tests:** `root.update()` in einer schnellen Schleife lässt
  `after`-Aufträge liegen, die Größenmeldungen immer neu ansetzen. Wer das
  Ergebnis sehen will, lässt zwischen den Runden kurz Zeit vergehen.
- **Speichern:** `write_json_atomic` schreibt mit `json.dumps` in einem Stück;
  `json.dump` in eine Datei ist bei großen Beständen fünfmal langsamer.

## Früherer Stand

Die Vorgeschichte der Zeichenfläche steht in
[Zeichnungsseite 3.29](65_ZEICHNUNGSSEITE_3.29.0.md) und
[Zeichenflächen-Übergabe](archiv/62_ZEICHENFLAECHE_WEITERGABE_2026-09-24.md) (seit 26.09.2026 im Archiv). Deren
Aussagen zu Zell-Undo (20), fester Größe 128 und fehlenden Formwerkzeugen
sind seit 3.30 überholt.

Weitere ältere Stände:

- Tagebuch, Gismo und responsive Oberfläche:
  [Tagebuch und UI 3.28](59_TAGEBUCH_UND_UI_3.28.0.md);
- Flackerkorrektur:
  [Flackern und Ablageprüfung 3.28](60_FLACKERN_UND_ABLAGEPRUEFUNG_3.28.0.md).

Der Übergabetext zu 3.29 liegt im Archiv:
[Projektübergabe vor 3.30.0](archiv/09_PROJECT_HANDOFF_3.29.0_vor_3.30.0.md).

## Weiterarbeit und Prüfung

**Zuerst lesen:**

- [Sitzungsprotokoll 24.–26.09.2026](67_SITZUNGSPROTOKOLL_2026-09-24_BIS_2026-09-26.md) – Aufträge,
  Entscheidungen, Lehren und Prüfläufe der letzten Sitzung;
- [QA-Bericht](07_QA_BERICHT.md);
- [Release-Checkliste](10_RELEASE_CHECKLIST.md);
- [Daten und Migration](06_DATA_BACKUP_MIGRATION.md);
- die manuelle Prüfliste
  `00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.30.0.md`.

Tests immer mit isoliertem `GLIDE_DATA_DIR`.

**Vollaufruf:**

`python tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.30.0/<neuer-Ordner> --timeout 900`

**Einzelsuiten der Neuerungen:**

- `tests/integration/test_drawing330.py`;
- `tests/integration/test_features330.py`.

Seit 3.30 öffnet der Zeichnungsimport eine Vorschau. Tests, die den Import
aufrufen, müssen `run_modal` ersetzen und „Als neue Zeichnung“ bestätigen –
sonst warten sie auf eine Eingabe (so geschehen in `test_features329`,
inzwischen angepasst).

**Keine menschliche Freigabe ersetzen die automatischen Prüfungen für:**

- Installer, Signatur;
- macOS;
- DPI und mehrere Monitore;
- Bildschirmleser;
- reale Maus- und Trackpadbedienung.

Diese Grenzen stehen im QA-Bericht und dürfen nicht als abgeschlossen
ausgegeben werden.
