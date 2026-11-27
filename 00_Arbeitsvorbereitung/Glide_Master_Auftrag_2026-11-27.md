# Glide – Master-Entwicklungsauftrag 27.11.2026: Bestandsaufnahme, Umsetzung Phase 1, Anforderungsmatrix

Stand 27.11.2026 · Glide 1.0.3 · Aufgabenformat 26 · Glide-System V1.87 (Katalog um M122, T345, T346 ergänzt, Versionswechsel offen)

Datierter Bericht zum Master-Auftrag vom 27.11.2026. Aufgabenstatus führt weiter der [Entwicklungsplan](Glide_Entwicklungsplan.md); dieser Bericht ist der Befund- und Übergabebeleg dieser Sitzung und wird nicht als zweite Statusliste fortgeschrieben.

## A. Zusammenfassung

**Ausgangszustand:** Branch `claude/glide-master-development-9435c1`, Commit `6c3a64eb`, Arbeitskopie sauber. Glide 1.0.3, Bento 0.1.0, Shell 0.6.2, Format 26.

**Ziel:** Bestandsaufnahme aller 31 Anforderungen, Behebung der reproduzierbaren Fehler aus den sechs Screenshots, sichere Umsetzung von Phase 1, belastbare Matrix für die übrigen Pakete.

**Ergebnis:** Sechs Befunde mit Ursache behoben und über echte UI-Einstiege getestet (PAGE-01, -03, -04, -05, Dialogumbruch „Anhang umbenennen“, Hänger beim Ablegen von Dateien). Gegenprobe gegen `6c3a64eb` rot. UX-01: Gelb im Dunkelmodus nach Inhaberentscheidung heller (24 %). Zweite Runde: PAGE-06 (zurück an die letzte Stelle), EDITOR-01 (Linkerkennung samt Linkmenü), UX-04 (Symbolknopf erweiterte Eingabe) und PERF-01 (gemessen, Listen-Scrollen rund 40–45 % schneller) umgesetzt und geprüft. Alle übrigen Anforderungen sind mit belegtem Istzustand, Lösungsweg und Entscheidungsbedarf erfasst; sie sind **nicht** umgesetzt.

**Gesamtstatus:** Phase 1 und Teile von Phase 2/3 implementiert und automatisiert verifiziert (Windows 11, Python 3.15.1, Tk 9.0, künstliche Daten). macOS-Sichtprüfung, Versionswechsel, `07_Python-Versionen`-Abgleich, Commit und Push stehen aus.

**Verbleibende Risiken:** macOS-Verhalten von Cmd+C und Drop nur über Bindungslogik und Ereignisnachstellung belegt, nicht nativ. Mehrere Pakete (Kapitel, Prompts) brauchen Datenformatentscheidungen.

## B. Befunde aus den Screenshots

| Bild | Beobachtung | Ursache (im Code belegt) | Status |
|---|---|---|---|
| 1, 2 | „Anhang umbenennen“ bildschirmbreit, Text abgeschnitten; danach „Programm reagiert nicht“ | (a) `themed_input_dialog`: Hinweis-Label ohne `wraplength` (gleiches Muster wie W05). (b) `register_file_drop` rief die Ablage synchron im tkdnd-`<<Drop>>`-Handler; die Ablage öffnete modal `ask_attachment_name`. Der Drop kehrte nicht zurück, die Ziehsitzung von macOS stand. Ursache (b) ist aus dem Code abgeleitet; der Hänger selbst wurde nicht auf einem Mac nachgestellt. | behoben, automatisiert geprüft |
| 4 | Schreibhinweis rechts und tiefer als Griff und Schreibmarke | `sync_placeholder` nutzte `place(x=padx, y=pady)`. Tk 9 zählt den Innenabstand bei `place` mit → doppelter Versatz (gemessen: x = 162 statt 81). Der Editor kennt dafür `place_at`. | behoben (PAGE-01) |
| 5 | Nach Cmd+C: „Hinweis – Zuerst einen Punkt auswählen.“ | Fensterweite Bindung `<Command-c>`/`<Control-c>` → `copy_selected_to_clipboard` läuft nach der Klassenbindung des Textfelds und nahm nur Eingabezeile/Suche aus. Gleiches Muster bei +V (legte Listenpunkte an) und +A. | behoben (PAGE-04) |
| 6 | „Kopieren“ in Blockaktionen grau | Kopieren setzt eine Markierung voraus; es gab keinen Blockbefehl | behoben (PAGE-03) |
| 3 | Pixel-Werkstatt mit wenigen sichtbaren Werkzeugen | siehe PIXEL-01–03 | Konzept offen |
| Nachtrag | Gelber Fensterhintergrund wirkt schmutzig | `appearance.with_background` mischt 16 % Markengelb `#FFDC0B` in den dunklen Grund (`#111113` → `#373112`); gelber Farbton bei so geringer Helligkeit ist Oliv | Inhaberentscheidung 27.11.: Ausnahme Gelb heller → 24 % (`#4A4211`), umgesetzt |

## C. Anforderungsmatrix

Status: **IV** implementiert und verifiziert · **K** Konzept/Analyse erstellt · **E** technische bzw. Inhaberentscheidung offen · **NB** nicht begonnen · **MA** manuelle Abnahme erforderlich. Aufwand grob: S < 1 Tag, M 1–3 Tage, L > 3 Tage.

| ID | Istzustand (geprüft) | Lösung / Vorschlag | Module | Aufwand | Risiko | Prio | Status |
|---|---|---|---|---|---|---|---|
| PAGE-01 | Griff erscheint auf leerer Seite schon (Fokus/Hover); nur der Hinweis saß versetzt | Hinweis über `dlineinfo('1.0')` + `place_at` | `app.pyw` `PageEditor.sync_placeholder` | S | gering | hoch | IV, MA Mac |
| PAGE-02 | Kapitel gibt es nicht; „Mehr › Gliederung“ springt bereits zu Überschriften (`add_outline_menu`) | Empfehlung: Kapitel = Überschriften H1–H3 der Seite mit stabiler Anker-ID als Formatbereich; Seitenleiste zeigt sie eingerückt unter der Seite. Keine Unterseiten (Produktgrenze „keine Unterseiten“, F073). Anker-ID ist ein neues Feld → Format 27 mit Migration | Seitenmodell, Seitenleiste, Suche, Export | L | Datenformat, Seitenleisten-Performance | mittel | K, E (Format 27) |
| PAGE-03 | Nicht vorhanden | „Block kopieren/ausschneiden“; Markdown des Blocks in die Zwischenablage, eigener Inhalt wird auch einzeilig als Block eingefügt; neue Identitäten über bestehenden Markdown-Import | `page_markdown.document_slice`, `block_markdown`; `PageEditor.copy_block`, `block_bounds`, `paste` | M | gering | hoch | IV |
| PAGE-04 | Fehler bestätigt (Bild 5) | Fensterweite Kürzel kehren in jedem Textfeld zurück (`keyboard_delete_belongs_to_text`, dieselbe Regel wie Entf) | `copy_selected_to_clipboard`, `paste_items_from_clipboard`, `select_all_items` | S | gering | sehr hoch | IV (Strg unter Windows nativ, Cmd als Ereignisnachstellung), MA Mac |
| PAGE-05 | Toolbarknöpfe (`set_block`) schalteten bereits zurück, „Umwandeln in“ nicht | `convert_block` schaltet aktive Art zurück; `block_choice_active` trennt Aufklappüberschrift von Überschrift/Aufklappliste; Haken auch in der Formatleiste | `PageEditor.convert_block`, `block_choice_active`, `_format_bar_block_menu` | S | Aufgabe→Text verliert Abhakzustand (wie bisher „Text“) | hoch | IV |
| PAGE-06 | Keine Positionsspeicherung für Seiten/Listen; nur die Nebenansicht merkte Scrollstand (`_side_view_scroll`) | Umgesetzt: Tk-freies Modul `view_positions` (begrenzt auf 64 Ansichten, nur Sitzung). Seite/Notiz: Zeichenversatz der obersten sichtbaren Stelle und der Schreibmarke, gemerkt beim Abbau des Editors, wiederhergestellt beim Neuaufbau (nicht bei aktiver Suche). Liste: oberste Zeilenkennung, ersatzweise Bruchteil; gemerkt bei jedem Ansichtswechsel (`prepare_inspector_switch`), wiederhergestellt in `set_active_list` vor jedem Sprung des Aufrufers. Über Neustart bewusst nicht | `view_positions.py`, `remember_/restore_editor_position`, `remember_/restore_list_position` | M | Wechselwirkung mit Render-Retention: getestet | hoch | IV, MA Mac |
| UX-01 | siehe B | Inhaberentscheidung: Gelb bekommt in dunklen Designs eine Ausnahme mit 24 % statt 16 % (`DARK_BACKGROUND_SHARE_EXCEPTIONS`). Im echten Glide gemessen: Dunkel `#4A4211`, Pixel `#3D3503`, alle Schriftrollen ≥ 4,5:1 über `legible_text_roles`. Mehrere wählbare Gelbtöne vom Inhaber abgelehnt (27.11.2026): es bleibt ein Gelb | `appearance.py` | S | keiner | mittel | IV, MA Mac |
| UX-02 | Tk-Text kennt kein Skip-Ink; Unterstreichung ist ein Tag-Attribut | Nur über eigenes Zeichnen (Canvas-Overlay je Zeile mit Glyphenmasken) möglich – faktisch eigene Text-Render-Engine. Empfehlung: nicht umsetzen; Alternative: Unterstreichung etwas tiefer/dünner ist in Tk ebenfalls nicht einstellbar | – | L | hoch | niedrig | K: unverhältnismäßig |
| UX-03 | Fußzeilenknopf „Erwähnt ohne Verweis …“ (`toggle_mentions`), immer sichtbar, Zahl erst nach dem Aufklappen; Bereich mischte Rückverweise und Erwähnungen; „Verknüpfen“ (`link_mention`) vorhanden | Umgesetzt nach Inhaberentscheidung D103: Kopfchip „N Verknüpfungen“ nur bei Treffern (Akzentfarbe, Klick/Enter/Leertaste), Bereich unter dem Kopf mit „Verweise hierher“ und „Erwähnt ohne Verweis“. Zählung einmal im Leerlauf nach dem Öffnen (gemessen 9 ms Graph + 12 ms Suche bei 500 Seiten/10 000 Punkten), nach Verknüpfen und beim Aufklappen; FP-05 (keine Suche bei Neuaufbau) bleibt, Aufklappen 52 ms Median. Seitenfuß nur Status | `page_link_count`, `remember_link_count`, `schedule_link_count`, `page_link_chip_text`, `style_link_chip`, `toggle_page_links`, `render_mentions` | M | Zählung veraltet, bis die Seite neu geöffnet wird | mittel | IV, MA Sicht |
| UX-04 | Erweiterte Eingabe existierte (Umschalt+Enter, Menü); U04 (3.33.20) hatte den Textknopf „Erweitert“ ausgeblendet | Umgesetzt: Symbolknopf ✎ (`ICONS["edit"]`, dieselbe Maske wie Bearbeiten; ☰ ist schon „Details“) links vom „+“, ruft `add_item_advanced`, Tooltip und Zugänglichkeitsname DE/EN, weicht bei zu schmaler Eingabezeile über die vorhandene Breitenregel. Alter Textknopf bleibt ausgeblendet | `advanced_icon_button`, `update_advanced_button_visibility` | S | gering | mittel | IV, MA Sicht |
| UX-05 | Seiten hatten den Inline-Hinweis; Listen und Übersichten zeigten passive Texte („Noch keine Punkte vorhanden.“). U20 (3.33.20) erlaubt je Leerzustand nur einen Anlegeweg | Umgesetzt ohne zusätzliche Knöpfe: Regeln im Tk-freien `empty_states.py` (Aufforderung statt Feststellung; Filter-Leere → Grund + Zurücksetzen; Schreibschutz → nur Grund; „…“ nur vor Dialogen). Leere Liste: Aufforderungstext, Klick fokussiert die Eingabezeile. Übersichten Seiten/Notizen/Notizbücher/Zeichnungen: leerer Abschnitt ist eine anklickbare, per Tastatur erreichbare Aufforderung, die direkt anlegt. Zweite Runde: Ordner und Bücher (→ Eingabezeile), Notizbuch (→ erster Eintrag, die Eingabezeile legt dort nur Listen an), Tabellenansicht, Bibliothek, Vorlagen, leere Galerie (Canvas-Text), Startseitenkacheln Zeichnungen/Galeriebilder/Pinnwand/Pinnwände/Labels (über die Render-Retention), leere Untermenüs „Labels“ (Seite/Liste/Ordner) und „Bereich anspringen“. Auf leeren Pinnwand-Kacheln entfällt der doppelte Knopf „Globale Pinnwand öffnen“ (U20). Bewusst Grund statt Aktion: Nebenansicht, Fälligkeits- und Labelübersicht, Archiv, Kopfzähler, Startseitenhinweise ohne Anlegeweg („Zuletzt bearbeitet“, „Heute“). Das Label-Untermenü von Aufgaben erreicht den Leerfall nie (zwei feste Systemlabels). `empty_states` ist Kandidat für Shell/Bento, sobald ein zweites Projekt es braucht | `empty_states.py`, `list_empty_state`, `empty_inline_action`, `overview_empty_action`, `make_inline_action_label`, `render_overview_sections`, Kachelhelfer `cta` | M | gering | mittel | IV, MA Sicht |
| EDITOR-01 | Kein Autolink beim Tippen; Markdown-Import erkannte nackte URLs; Links per Strg/Cmd+K und Öffnen per Strg/Cmd+Klick vorhanden | Umgesetzt: Tk-frei `find_links`/`link_before` (http, https, www. → https, E-Mail → mailto; Satzzeichen und unpaarige Klammern am Ende bleiben Text; `javascript:`/`file:` nie; max. 2048 Zeichen; Unicode-Domains). Editor: bei Leerzeichen, Enter und Einfügen, nicht in Code und nicht in bestehenden Links, eigener Rückgängig-Schritt. Linkmenü: öffnen, kopieren, bearbeiten, entfernen. Kein Netzzugriff ohne Befehl | `page_markdown`, `PageEditor.autolink_range`, `autolink_before_insert`, `add_link_menu` | M | Undo in zwei Schritten (Leerzeichen, dann Link) | mittel | IV |
| EDITOR-02 | Keine Rechtschreibprüfung | Tk-Widgets haben keine native Prüfung. Machbar: gemeinsame Schnittstelle + plattformeigene Adapter (macOS `NSSpellChecker` via pyobjc, Windows `ISpellChecker` via comtypes) oder Hunspell (MPL/LGPL/GPL, Wörterbücher je Sprache ~2–5 MB). Jede Variante ist eine neue Laufzeitabhängigkeit (AGENTS-Regel 4) | neu | L | Abhängigkeiten, Performance beim Tippen | niedrig | K, E (Abhängigkeit) |
| PROMPT-01–05 | Nicht vorhanden; Vorlagen (Format 2) und Seiten existieren | MVP-Vorschlag: Prompt als neue Seitenart (eine Identität, in Seiten und Notizen sichtbar über Filter statt Kopie), Feldgruppen als strukturierte Kopfabschnitte im Seitendokument, Export Markdown/Klartext/ZIP mit Anhängen, Vorlagen über bestehende Vorlagenverwaltung. Keine Anbieterübergabe ohne offizielle Schnittstelle; nur Zwischenablage und Öffnen der Anbieterseite | Datenmodell, Editor, Export | L | Neue Listenart = Formatwechsel (AGENTS-Regel 3) | mittel | K, E (Format 27, Umfang MVP) |
| SHELL-01/02 | Kein Katalog „Weitere Programme“; „Über Glide“ vorhanden | Deklaratives Manifest (JSON: id, Name, Kurztext, Status, Plattformen, URLs, Logo-Pfad) im Host; Darstellung als Bento-Karten in `glide_shell`/`glide_bento` ohne Glide-Fachlogik; offline, keine Telemetrie. Inhalte (STEPS, Chess & Chains …) liefert der Inhaber – nichts erfunden | Shell, Bento | M | gering | niedrig | K, E (Inhalte) |
| PERF-01 | Keine Scrollmessung vorhanden | Neues Werkzeug `messung_scrollen.py` (echte Mausradereignisse). Befund: `yscrollcommand` der Seite kostet nur ~0,1 ms – keine Änderung dort. Listen: `show_quick_plan_row` setzte bei jedem Radschritt Text und Farben aller ~19 Zeilenaktionsknöpfe neu und zeichnete sie vollständig (≈ 15 von 28 ms). Jetzt nur bei geänderten Werten. Ergebnis siehe E. Restkosten liegen im Treeview-Zeichnen von Tk; Trackpad und macOS nicht gemessen | `show_quick_plan_row`, `sync_row_action_colors` | S | gering | hoch | IV (Windows), Mac-Messung offen |
| BENTO-01–05 | Bento 0.1.0: BentoCard, Header, Metric, Actions, EmptyState, Divider, Grid, LayoutPlanner, Tokens | Akzentflächen als Token-Rollen (`surface_accent`, `surface_accent_soft`) mit berechneter Vordergrundfarbe; Bibliothek stufenweise (Konzept führt 15 Komponenten) | `glide_bento` | L | Unruhe, Kontrast | mittel | K (bestehendes Konzept), NB |
| PIXEL-01–03 | Vorhanden u. a.: Pinsel, Füllen, Pipette, Formen (gefüllt/ungefüllt), Auswahl mit Kopieren/Ausschneiden/Einfügen, Größen 1–8, Symmetrie, Füllmuster, Zoom, Vorschau (Kachel/Grau), Palette, Zuletzt-Farben, Farbe ersetzen, Rückgängig, Referenzbild, Bildfolgen und Export. D61 hatte die Werkzeugwahl im Menü „Pinsel ▾“ gebündelt; ein eigener Radierer fehlte | PIXEL-03 umgesetzt nach Inhaberentscheidung D102: Symbolspalte links neben der Fläche mit acht Werkzeugen, aktives hervorgehoben, Kürzel im Tooltip; Leiste oben einzeilig ohne Werkzeugwahl. Radierer (Umschalt+E) malt den Grund (Index 0, D59), nicht unter „Zuletzt“, rückgängig machbar. Symbole aus `ICONS` mit Textrückfall im Symbolvertrag, Zeichen aus DejaVu Sans geprüft. PIXEL-02 (27.11.2026): Drehen/Spiegeln (Tk-frei `flip_region`, `rotate_region`, `DrawingModel.transform_region`; Kürzel H/V/T/Umschalt+T; Auswahl um ihre Mitte, sonst ganze Zeichnung) und Schachbrettanzeige des Grunds umgesetzt; ganzzahliger PNG-Export bestand bereits. Offen: Ebenen (Formatentscheidung) | `ICONS`, `symbol_policy.TEXT_FALLBACKS` (eindeutige ASCII-Ersatzkürzel), `DrawingEditor.TOOLS`, `_build_tool_column`, `sync_tool_column`, `_paint_color`, `_begin_stroke` | M | Feststelltaste macht aus „e“ den Radierer | mittel | IV (PIXEL-03), K (PIXEL-02 Rest) |
| RELEASE-01 | `docs/10_VEROEFFENTLICHUNG.md` vorhanden; Stufentabelle nennt für EV-Zertifikate „sofortiges SmartScreen-Vertrauen“ | Diese Aussage ist nach meinem Kenntnisstand seit 2024 überholt (EV-Zertifikate geben bei SmartScreen keinen Sofortvorsprung mehr). **Nicht mit aktueller Quelle verifiziert** – vor jeder Kaufentscheidung mit offiziellen Microsoft-/Apple-Seiten prüfen. Empfehlung zu prüfen: Apple Developer Program (eine Mitgliedschaft für alle eigenen Apps) + Microsoft Artifact Signing (früher Trusted Signing) | Doku | M | Kosten, Identitätsprüfung | mittel | E, Recherche offen |

## D. Architektur

- **Neu, Tk-frei (D17):** `page_markdown.document_slice`, `block_markdown`, `find_links`, `link_before`; Modul `view_positions.py` (M122). Werkzeug `scripts/pflege/messung_scrollen.py`.
- **Neu im Editor/App:** `PageEditor.autolink_range`, `autolink_before_insert`, `link_tag_at`, `copy_link`, `edit_link`, `remove_link`, `open_link_tag`, `add_link_menu`; `ListApp.view_positions`, `remember_/restore_editor_position`, `remember_/restore_list_position`, `list_rows_in_view_order`, `advanced_icon_button`, `advanced_icon_reserve`.
- **Geändert:** `appearance.with_background` (Gelb-Ausnahme), `show_quick_plan_row`, `sync_row_action_colors`, `set_active_list`, `prepare_inspector_switch`, `markdown_shortcut`, `newline`, `paste_plain`, `PageEditor.sync_placeholder`, `convert_block`, neu `block_choice_active`, `block_bounds`, `copy_block`; `paste` erkennt den eigenen Blockinhalt; `ListApp.copy_selected_to_clipboard`, `paste_items_from_clipboard`, `select_all_items`, `register_file_drop`, `themed_input_dialog`.
- **Datenmodell:** unverändert (Format 26). Keine Migration.
- **Schichten:** alles Ebene A; nichts in Shell/Bento verschoben.

## E. Qualitätssicherung (Windows 11, Python 3.15.1, Tk 9.0, künstliche Daten)

| Prüfung | Ergebnis |
|---|---|
| `tests/integration/test_befunde_1127.py` (T345) | bestanden |
| T345 gegen `6c3a64eb` (Gegenprobe) | fehlgeschlagen wie erwartet (Hinweis x = 162 statt 81) |
| `tests/unit/test_page_markdown.py` (11 Tests, 4 neu) | bestanden |
| `tests/unit/test_appearance.py` (Gelb-Ausnahme) | bestanden |
| Gelbgrund im echten Glide (Dunkel, Pixel) | Schriftrollen ≥ 4,5:1, Fensterbilder `Glide_UX01_Gelb_24_*.png` |
| `test_befunde330.py` (Rechtsklick, Umwandeln, Zeilen) | bestanden |
| `test_oberflaeche33321.py` (Schreibhinweis, Dialogbreiten) | bestanden |
| `tests/tools/test_glide_system.py` nach Katalogpflege | bestanden |
| CI-Grundstufe in der OneDrive-Arbeitskopie | 1 Fehler in `test_shell_uebernahme` (`rmtree` im OneDrive-Ordner); derselbe Test besteht mit denselben Änderungen in einer lokalen Prüfkopie |
| CI-Grundstufe in lokaler Prüfkopie (Stand Runde 1) | bestanden; Hinweis Lieferstand (07 nicht abgeglichen) zulässig |
| CI-Grundstufe Runde 2 (lokale Prüfkopie) | bestanden, alle Schritte; Hinweis Lieferstand (6 Dateien, 07 nicht abgeglichen) zulässig |
| `test_aufgaben3380.py`, `test_arbeitsmodi.py` (72 grün), `test_glide.py` | bestanden |
| `tests/unit/test_view_positions.py` (T346, 4 Tests) | bestanden |
| T345 Runde 2 (UX-04, EDITOR-01, PAGE-06) | bestanden |
| `test_komfort33320.py`, `test_uiux_paket.py` | bestanden |
| `tests/unit/test_empty_states.py` (T347, 4 Tests) und T345 mit UX-05 | bestanden |
| Runde 3 (UX-05): `test_komfort33320` (U20), `test_datenintegritaet`, `test_features315`, `test_features330`, `test_heute3336`, `test_uiux_paket`, `test_glide`, `test_befunde330`, `test_oberflaeche33321` | bestanden |
| CI-Grundstufe Runde 3 (lokale Prüfkopie) | bestanden, alle Schritte; Hinweis Lieferstand (7 Dateien) zulässig |
| Runde 4 (UX-05 Rest): T345 erweitert (Ordner, Notizbuch, Label-Menü, Startseitenkachel), T347 (5 Tests), `test_startseite3332`, `test_bento_integration`, `test_features315/324/325/330`, `test_aufraeumen330`, `test_bereiche3331`, `test_komfort33320`, `test_glide`, `test_datenintegritaet`, `test_uiux_paket` | bestanden |
| CI-Grundstufe Runde 4 (lokale Prüfkopie) | bestanden; Hinweis Lieferstand (7 Dateien) zulässig |
| Runde 5 (PIXEL-03): T345 erweitert, `test_drawing_pixel35`, 16 Zeichnungs- und Editorsuiten (u. a. `test_pixel3350`, `test_animation3400`, `test_arbeitsmodi`, `test_features330` angepasst an D102) | bestanden |
| `test_symbol_policy` | zunächst rot: Textersatz „Fü“ nicht ASCII und „Li“/„Au“/„Pi“ doppelt belegt; korrigiert auf eindeutige ASCII-Kürzel, danach bestanden |
| CI-Grundstufe Runde 5 (lokale Prüfkopie) | bestanden; Hinweis Lieferstand (8 Dateien) zulässig |
| Runde 6 (UX-03): T345 erweitert, `test_erwaehnungen` (FP-05, angepasst: Zählung nach dem Öffnen, keine Suche bei Neuaufbau, Aufklappen 52 ms Median bei 500 Seiten), `test_arbeitsmodi`, `test_oberflaeche33321`, `test_glide`, `test_uiux_paket`, `test_features330`, `test_befunde330` | bestanden |
| T340 `test_sync_foot_density_behavior` | zunächst rot (erwartete den Knopf wieder im Seitenfuß); an D103 angepasst, Fälle 1 und 3 unverändert, bestanden |
| Attributprüfung | zunächst rot (`self.__dict__`, `log_exception`); auf `getattr` und `log_error` umgestellt, bestanden |
| CI-Grundstufe Runde 6 (lokale Prüfkopie) | bestanden; Hinweis Lieferstand (8 Dateien) zulässig |
| macOS (Cmd-Tasten nativ, Drop aus Finder, Tk 9 Sicht, Trackpad) | nicht ausgeführt – MA |
| Linux | nicht ausgeführt |

**Scrollmessung** (`messung_scrollen.py --schritte 30`, Windows 11, Python 3.15.1, Tk 9.0, Mausrad, Median/p95 je Schritt in ms, vorher = Stand ohne PERF-01-Änderung):

| Größe | Liste vorher | Liste nachher | Seite vorher | Seite nachher |
|---|---|---|---|---|
| 10 | 0,06 / 0,47 | 0,05 / 0,10 | 0,09 / 0,14 | 0,09 / 0,29 |
| 100 | 20,9 / 66,1 | 12,8 / 26,3 | 5,9 / 9,4 | 9,6 / 17,5 |
| 500 | 20,8 / 23,8 | 12,7 / 16,6 | 7,7 / 16,0 | 8,0 / 15,8 |
| 1000 | 27,4 / 36,5 | 14,9 / 16,7 | 6,4 / 10,5 | 7,1 / 13,5 |

Bei 10 Einträgen scrollt nichts (passt ins Fenster). Die Seitenwerte schwanken zwischen Läufen im selben Bereich; dort wurde nichts geändert.

Manuelle Mac-Abnahme: (1) Text in einer Seitenaufzählung markieren, Cmd+C → keine Meldung, Cmd+V woanders. (2) Neue Seite: Hinweis direkt rechts vom Griff. (3) Bildschirmfoto mit 41 Zeichen auf eine Seite ziehen → Dialog schmal, App bleibt bedienbar. (4) Aufzählung über „Umwandeln in › Aufzählung“ erneut → Text. (5) Blockaktionen › Block kopieren → auf anderer Seite einfügen. (6) Adresse tippen, Leertaste → Link; Rechtsklick auf Link. (7) Lange Seite scrollen, zu einer Liste und zurück → gleiche Stelle. (8) ✎ neben „+“ öffnet die volle Eingabemaske. (9) Lange Liste mit Trackpad scrollen und Flüssigkeit beurteilen.

## F. Git- und Entwicklungsstatus

Ausgangsbranch/-commit `claude/glide-master-development-9435c1` @ `6c3a64eb`. Keine Commits, kein Push. Geänderte Dateien: `src/glide/app.pyw`, `src/glide/page_markdown.py`, `src/glide/appearance.py`, `tests/unit/test_appearance.py`, `src/glide/resources/locales/de.json`, `en.json`, `src/glide/README.md` (M122, T345, T346, Zählungen), `src/glide/view_positions.py` (neu), `scripts/pflege/messung_scrollen.py` (neu), `scripts/pflege/README.md`, Modullisten in `scripts/pflege/abgleich_07.py` und `packaging/macos/baue_app.py`, `tests/unit/test_view_positions.py` (neu), `src/glide/empty_states.py` (neu, M123), `tests/unit/test_empty_states.py` (neu, T347), `tests/unit/test_page_markdown.py`, `CHANGELOG.md`, `docs/20_FUNKTIONEN.md`; neu `tests/integration/test_befunde_1127.py`, dieser Bericht, Fensterbilder `Glide_UX01_Gelb_24_dark.png`/`_pixel.png`. Offen für die Produktionsrunde: Glide-System V1.88 samt Standzeilen, App-Version, `abgleich_07.py`/SHA-256, eingefrorene Vollprüfung (D51).

## G. Offene Arbeitsaufträge

- **Implementiert und verifiziert:** PAGE-01, PAGE-03, PAGE-04, PAGE-05, PAGE-06, UX-01 (Gelb 24 %), UX-03 (D103), UX-04, UX-05, PIXEL-03 (D102), EDITOR-01, PERF-01 (Listen-Scrollen), Dialogumbruch, Drop-Hänger (jeweils mit MA Mac).
- **Technische/Inhaberentscheidung offen:** PAGE-02 und PROMPT (Format 27), EDITOR-02 (Abhängigkeit), SHELL-01 (Inhalte), RELEASE-01 (Kosten nach verifizierter Recherche).
- **Konzept erstellt, nicht begonnen:** BENTO-01–05, PIXEL-02 Ebenen (Formatentscheidung).
- **Offen innerhalb PERF-01:** Trackpad- und macOS-Messung.
- **Bewusst zurückgestellt:** UX-02 (unverhältnismäßig in Tk).

Empfohlene Reihenfolge danach: Mac-Abnahme dieser Runde → PIXEL-02 ohne Formatwechsel (Drehen/Spiegeln, Transparenzraster) → Entscheidungen Format 27 (Kapitel, Prompts gemeinsam bündeln, D51) → BENTO/SHELL-Katalog nach Inhaltslieferung.
