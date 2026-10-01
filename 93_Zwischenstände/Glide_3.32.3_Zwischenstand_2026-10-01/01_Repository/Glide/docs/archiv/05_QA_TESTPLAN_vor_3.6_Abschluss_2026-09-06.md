# QA-Testplan

Stand: 05.09.2026 · App-Version 3.4.0 · Datenformat 10

Die Versionsüberschriften beschreiben, wann eine Prüfung hinzukam. Der aktuelle
Prüfstand steht in `07_QA_BERICHT.md`, der gemeinsame Aufruf in `../tests/README.md`.
Windows und macOS benötigen kein Xvfb; Linux benötigt für Tk ein Display.


## Automatisiert in 3.4.0

- `test_ui_updates.py`: Artlabelwechsel in beide Richtungen, Zeilenumbrüche,
  Fälligkeit, Auswahlfarben, Chip-Hover, getrennte Zähler und tatsächliche
  24-Pixel-Geometrie bei 1280/980/860 Fensterbreite in beiden Themes.
- Startseite: echte Aufgaben statt Gliederung, heute fällig/überfällig,
  Bearbeitung statt Navigation, Vorlagen mit neuen IDs und Rückgängig.
- Einstellungen: bisherige Datei sichern, unbekannte Schlüssel bewahren,
  persönliche Daten speichern und beim Neustart mit Startseite laden.
- TXT: alte und neue Gruppen-/Wichtigkeitsmarker verstehen.
- `test_dialog_theme.py`: Hilfe, Meldungen und Rückfragen in Hell/Dunkel,
  Rückgabewerte bei allen Schaltflächen/Schließen, Größenänderung, Fettschrift,
  Spalten, Scrollbarkeit und verschachtelte Griff-Rückgabe.
- Optionale Bilder: `test_ui_updates.py --screenshots ORDNER` erzeugt unter
  Windows ausschließlich Aufnahmen eigener Testfenster.

Manuell offen: macOS/Linux, weitere DPI/Monitore und reale Mausbedienung.

## Automatisiert in 3.3.0

Neu abgedeckt durch `tests/integration/test_glide.py`:

- Die Seitenleiste führt fünf Systemzeilen in der Reihenfolge Eingang,
  „In Bearbeitung“, „Labels“, „Verspätet“, Papierkorb.
- Die Ansicht „Labels“ bildet je eigenem Label eine Gruppe, „Ohne Label“ steht
  am Ende, die beiden festen Labels bilden keine Gruppe.
- Ein Punkt mit zwei Labels erscheint in beiden Gruppen, jede Zeile trägt den
  Farbtag ihrer Gruppe.
- Ein Zug in eine andere Gruppe ersetzt genau das Label der Herkunftsgruppe an
  derselben Position; die übrigen Labels bleiben. Ein Zug nach „Ohne Label“
  nimmt nur dieses eine Label. Beide Züge lassen sich zurücknehmen.
- Fälligkeits- und Labelspalte entsprechen dem gemessenen Inhalt, bleiben unter
  dem Musterwert und fassen den längsten Zellinhalt jeder sichtbaren Zeile.
- Beide Spalten sind links ausgerichtet.
- Ein Labelchip zeichnet vollständig innerhalb seiner Fläche (vier Bögen, zwei
  Rechtecke, nichts außerhalb von Breite−1 / Höhe−1).

**Nicht automatisierbar und deshalb in der manuellen Prüfliste:** Ziehen mit
realer Maus, Chiprundung bei anderer Anzeigeskalierung, Spaltenbreiten unter
Segoe UI und SF Pro.

## Automatisiert in 3.2.0

- Die mitgelieferte Beispieldatei
  `tests/fixtures/beispiele/Glide_Beispieldaten.glidebackup` wird auf demselben
  Weg gelesen wie ein echter Import: `inspect_backup_archive`,
  `validate_backup_schema`, `normalize_lists_data`, `normalize_trash_data`.
  Geprüft werden Umfang (mindestens 10 Listen, 5 Ordner, 120 Punkte,
  3 Papierkorbeinträge), das Vorkommen aller vier Punktarten, mindestens zehn
  Long-Tasks, mindestens eine wirklich mehrzeilige Notiz, die Abdeckung aller
  sieben Palettenfarben und dass **kein** Punkt auf ein nicht existierendes
  Label zeigt.
- Jedes Zeichen in `ICONS` liegt unterhalb von U+1F000. Der Test gilt nur für
  diese Tabelle; die drei Emoji-Ausnahmen außerhalb von `ICONS` sind in
  `01_PRODUCT_CONSTRAINTS.md` dokumentiert.
- `DUE_COLUMN_ICON` und `LABEL_COLUMN_ICON` verweisen auf `ICONS`, statt ihr
  Zeichen selbst zu führen.
- `LEGACY_LABEL_COLOR_MAP` existiert nicht mehr; `resolve_label_color` fällt für
  jeden unbekannten Wert auf die Vorgabefarbe zurück.

## Automatisiert in 3.1.0

- **Gemeinsamer Änderungsrahmen:** Eine Änderung ohne gemeldete Wirkung
  hinterlässt keinen Rückgängig-Schritt; eine mit Wirkung behält ihn und lässt
  sich zurücknehmen. `focus="first"` richtet den Blick auf den ersten statt den
  letzten Punkt der Auswahl.
- **Kürzung des Rückgängig-Speichers:** Bei vollem Speicher
  (`MAX_UNDO_STEPS`) kostet eine wirkungslose Aktion **nicht** den ältesten
  Schritt. Geprüft über die Objektidentität des ältesten Schnappschusses.
- `selected_items_for_change` liefert ohne Auswahl `None` statt einer leeren
  Liste; mit Auswahl die Auswahl.
- Ein Unterpunkt kehrt über `lift_item_to_parent_level` hinter sein Elternteil
  zurück – der gemeinsame Kern von „Ausrücken“ und der Tab-Umschaltung.
- **Griff-Rückgabe nach einem modalen Unterdialog:** Ein Fenster mit Griff, ein
  Unterdialog darüber, und nach dessen Ende muss der Griff zurück sein. Das ist
  der Regressionstest zum gemeldeten Einfrieren.

## Automatisiert in 3.0.0

- Symbole der Systemzeilen und der Schaltflächen werden aus `ICONS` gelesen –
  ein Wechsel des Zeichens trifft nur diese Tabelle.
- Labelspalte und Hinweiszeile weichen bei derselben Breite
  (`LABEL_COLUMN_MIN_TREE_WIDTH`); geprüft wird knapp darüber und knapp darunter.
- Labelspaltenbreite kommt aus `label_column_width()`, gemessen mit der Schrift
  der Liste.
- Das Symbol vor einem Label steht in der Zelle, in der Liste wie in der
  Ordnerübersicht.

## Automatisiert in 2.12.0

- `LabelDropdown`: Rückgabe in der Reihenfolge der Labelverwaltung, Vorbelegung
  aus einem Punkt, Zuordnung auf ein gelöschtes Label fällt heraus, geschlossene
  Zeile zeigt Namen beziehungsweise Platzhalter.
- `DueField`: kompakte Ausprägung ohne eingebetteten Kalender, aber mit
  Kalenderknopf; vollständige Ausprägung mit Monatsraster. `set_due` und
  `read()` verhalten sich in beiden gleich.
- Kopfbereich: `stats_label` und `page_labels_frame` liegen in `header_meta`;
  die Labelzeile ist mit und ohne Labels exakt gleich hoch.
- `pack_label_chips` mit `max_rows=1` erzeugt genau eine Reihe und hängt einen
  Zähler an.
- Suchzeile liegt in `content_frame`, Seitenleiste und Listenbereich in
  `main_area`; Filterbox und „Suche löschen“ liegen in der Suchzeile.
- Der Filter „Nur erledigte Punkte“ ist restlos entfernt (`show_done_only_var`
  existiert nicht mehr); eine gespeicherte Einstellung `filter_mode: "done"`
  fällt beim Start auf „alle“ zurück.
- Fälligkeitsspalte: zweistelliges Jahr in der Liste, Spaltenbreite aus
  `due_column_width()` – gemessen mit der Schrift der Liste.
- Labelspalte: ein Label je Zeile, Rest als Zähler; die Spalte bleibt bei einer
  Baumbreite von 630 Pixeln stehen und weicht erst darunter.

## Automatisiert in 2.11.0

Neue Testdatei: `tests/integration/test_datenintegritaet.py`.

- **Bestandswächter:** Ein absichtlich herbeigeführter Verlust wird
  zurückgerollt und gemeldet; eine reine Umsortierung bleibt unangetastet; ein
  `DataIntegrityError` bricht sauber ab, ohne die Anwendung zu stoppen; der
  Papierkorb zählt in der Bilanz mit, sodass Löschen kein Verlust ist.
- **Gruppieren und Auflösen, 130 Kombinationen:** fünf Listenaufbauten über alle
  vier Arten mit Unterpunkten, dazu jede Auswahl von zwei bis fünf Punkten,
  benachbart wie verstreut. Nach jedem Schritt: Bestand vollständig, Baum
  vollständig, nichts nur hinter einem Klapppfeil sichtbar. Zusätzlich
  verschachtelte und leere Gruppen.
- **Papierkorb für einzelne Punkte:** Löschen mit Unterpunkten, Titel und
  Detailzeile im Papierkorb, Wiederherstellen an dieselbe Stelle, Rundlauf über
  Speichern und Laden, Anhänge im Komplettbackup, und der Fall, dass die
  Herkunftsliste nicht mehr existiert.
- **Ziehen mit Mehrfachauswahl:** Reihenfolge beim Einfügen nach und vor dem
  Ziel, Shift+Drag als Unterpunkt, Schutz vor dem eigenen Unterbereich.
- **Drop auf die Seitenleiste:** Rückfrage vorhanden, Verschieben korrekt,
  Ablehnung ohne jede Wirkung.
- **Mehrfachauswahl-Taste:** Strg+Klick (macOS: Cmd) erweitert und verkleinert
  die Auswahl; auf Nicht-macOS-Systemen ist `<Control-Button-1>` an keinem der
  drei Bäume mehr belegt.
- **Gemeinsame Eingabemaske:** Anlegen und Bearbeiten liefern denselben
  Feldsatz; Datum und Uhrzeit werden über das Formular gesetzt, übernommen und
  überstehen TXT- und Speicher-Rundlauf; eine unlesbare Uhrzeit hält das
  Formular offen; die erweiterte Eingabe übernimmt, was in der Schnelleingabe
  steht.

- **Label-Chips:** Maße (aktuell Radius 9, gleiche Seitenabstände, oben zwei Pixel
  weniger als unten), Farbmischung an den Rändern und in der Mitte,
  Helligkeitssuche, Kontrast **aller sieben Palettenfarben in beiden Themes**
  gegen Text und gegen den Fensterhintergrund, Umbruch bei schmaler Fläche,
  Chips in der Kopfzeile ohne gestapelte Leerreihen.
- **TXT-Rundlauf aller vier Arten:** Aufgabe, einzeiliger Long-Task,
  mehrzeiliger Long-Task, Zwischenüberschrift und Gruppe kehren mit derselben
  Art zurück; Wichtigkeit und Erledigt-Zustand ebenso.
- **Tote-Code-Analyse** über AST: keine ungenutzten Methoden oder Konstanten.

Der ausführliche Bericht zu einem konkreten Lauf – Umfang, Ergebnis, Befunde und
was ungeprüft bleibt – steht in `07_QA_BERICHT.md`.

## Automatisiert seit 2.9.0

### App-weiter Durchlauf (`tests/integration/audit_app.py`)

Prüft nicht einzelne Funktionen, sondern die Wege durch die App, und meldet alle
Abweichungen auf einmal statt beim ersten Fehler zu stoppen:

- Ordnerhierarchie: Ebenen, Vorfahren, rekursive Zähler, Unterbaumhöhe.
- Kreis- und Tiefenschutz an jedem Weg (Maus, Menü, Tastatur).
- Verschieben, Herauslösen, relatives Sortieren, Auflösen mit Nachrücken.
- Papierkorb: ganzer Ordnerzweig hinein und mit Hierarchie zurück.
- Speicher-Rundlauf, unbekannte Elternverweise, Ordnerkreis in der Datei und im
  portablen Backup.
- Jede Ansicht mit Filter, Suche, Kopfzeile, Statistik, Eingabefeld und Hinweiszeile.
- Jedes Kontextmenü für jede Zeilenart, jede Systemzeile und jede Mehrfachauswahl.
- Jede erwartete Tastenbindung an Aufgabenbaum, Seitenleiste, Systembereich und
  Hauptfenster – in Tks kanonischer Schreibweise verglichen.
- Ein- und Ausrücken per Tastatur, Sortieren unter Geschwistern, Ablegezonen.
- Simuliertes Drag & Drop für alle Quell-/Ziel-Kombinationen inklusive der
  abgelehnten Kreisbildung.
- Rückgängig nach Strukturänderungen, Punktverschiebung zwischen Listen, Löschen
  eines Long-Tasks samt Fortsetzungszeilen, Aktionen von einer Fortsetzungszeile
  aus, Suche über verschachtelte Ordner, Backup-Rundlauf, Anlegen in Unterordnern.
- Aufbau jedes Dialogs mit der erwarteten Anzahl Bildlaufleisten.

### Integrationstest (`tests/integration/test_glide.py`)

- Verschachtelte Ordner: Ebene, Vorfahrenkette, direkte und rekursive
  Listenzähler, Unterbaumhöhe, Ordner- und Listenpfad, Aufbau des Baums in der
  Seitenleiste mit rekursivem Zähler.
- Kreisschutz (Ordner in sich selbst, Ordner in einen Nachfahren) und
  Tiefengrenze; eine abgelehnte Verschiebung verändert nichts.
- Ablegezonen: oberes Viertel davor, Mitte hinein, unteres Viertel danach.
- Tastatur: Einrücken legt in den Ordner darüber, Ausrücken hebt genau eine
  Ebene, Alt+↑/↓ sortiert nur unter Geschwistern.
- Auflösen hebt Listen und Unterordner eine Ebene an; der Papierkorb nimmt den
  ganzen Zweig und bringt ihn mit Hierarchie zurück.
- Format 10: `due_time` und die Papierkorbart `item` werden geschrieben, geladen
  und geprüft; Bestände bis Format 9 laden unverändert.
- Format 9: `parent_id` wird geschrieben und geprüft, unbekannte Eltern und
  Kreise werden beim Laden bereinigt, ein Ordnerkreis und ein unbekannter
  Elternordner im Komplettbackup werden abgewiesen.
- Ordnermenü mit „Ordner verschieben“ und „Neuer Unterordner …“, Unterordner in
  der Ordnerübersicht, IID-Auflösung für Unterordner- und Listenzeilen.
- Long-Task: Zeilenumbrüche bleiben erhalten, jede andere Art bleibt einzeilig,
  beim Zurückwandeln verschwinden sie; der Umbruch beginnt an jedem eigenen
  Zeilenumbruch neu und bleibt bei fünf Zeilen; TXT-Rundlauf über
  `Text:`-Fortsetzungen liefert denselben Text und dieselbe Art zurück.
- Bildlaufleisten: drei im Long-Task-Detailfenster, zwei im gewöhnlichen, je eine
  im Beschreibungstext-Dialog und in der Labelverwaltung.

### Weiterhin geprüft (aus 2.8.0)

- Systemzeilen inklusive „Verspätet“ samt Zähler, Filterlogik und eigenem Menü.
- Sicherheitsbereich des Seitenleistenzählers, responsive Spaltenbreiten,
  Hover-Tags in beiden Themes.
- Zwischenüberschrift: Schriftbild, Abstandszeile, Nummerierungsneustart.
- Feste Labels: Entstehen, Schutz, Gleichlauf mit der Art in beide Richtungen.
- Erweiterter Anlage-Dialog inklusive abweichender Zielliste.
- Referenzbestände der Formate 10, 9, 8, 7, 6, 5, 4 und 2 durch die aktuelle
  Normalisierung.

## Automatisiert seit 2.7.1

- Die Entf-Taste ist in beiden Seitenleistenbäumen gebunden, legt die dortige
  Auswahl in den Papierkorb, meldet „break“ zurück und lässt Systemzeilen
  unangetastet.
- Farbzuordnung aller Aktionsschaltflächen: obere Reihe gemischt
  (blau, rot, orange, türkis, grün, braun), untere Reihe durchgehend lila.
- Labels nutzen exakt `LIST_COLOR_CHOICES`. **Seit 3.2.0** gibt es keine
  Abbildung der Farbschlüssel des internen Teststands 2.7.0 mehr
  (`LEGACY_LABEL_COLOR_MAP` ist entfernt): Alles, was nicht in der Palette
  steht, fällt auf `DEFAULT_LABEL_COLOR` zurück – ein alter Schlüssel macht
  dabei keinen Unterschied zu einem unsinnigen.
- Der Farbauswahldialog erhält je Zeile einen Farbschlüssel und markiert die
  aktuelle Farbe; die Emoji-Punkte sind vollständig entfernt.
- Labels an Ordnern und Listen: Zuweisen und Lösen über das Kontextmenü, Anzeige
  in der Labelspalte der Ordnerübersicht und als farbige Kopfzeile der
  geöffneten Seite, keine Anzeige in der Seitenleiste, Persistenz über Speichern
  und Laden, Ablösen beim Löschen eines Labels und Ablehnung ungültiger
  Labelfelder im Komplettbackup.
- Kalender: `calendar_month_grid` liefert das montagsausgerichtete Raster eines
  Monats – fünf Wochen für September 2026, sechs für Februar 2026 – und
  `shift_month` blättert korrekt über Jahresgrenzen.
- Alt+Pfeiltasten sind im Aufgabenbaum und in der Seitenleiste gebunden.

## Automatisiert seit 2.7.0

- Systemblock der Seitenleiste: Eingang, „In Bearbeitung“, „Verspätet“ und
  Papierkorb stehen aktuell in einem vierzeiligen Feld, der Listenbaum darunter.
- Papierkorb: Löschen einer Liste erzeugt einen vollständigen Eintrag mit
  Herkunftsordner; Wiederherstellen setzt sie dorthin zurück. Ein gelöschter
  Ordner nimmt seine Listen mit und bringt sie gemeinsam zurück. „Ordner
  auflösen“ behält die Listen und legt nur die leere Hülle ab. „Papierkorb
  leeren“ entfernt endgültig. Der Eingang bleibt löschgeschützt.
- Papierkorb überlebt Speichern, Laden und Komplettbackup einschließlich der
  Anhänge gelöschter Listen; deren Dateien liegen im Archiv und sind nach dem
  Import wieder auflösbar und inhaltsgleich.
- Kollidierende Punkt-IDs zwischen aktiven und gelöschten Listen werden im
  Komplettbackup abgewiesen und beim Normalisieren eindeutig gemacht.
- Gemeinsamer Bearbeiten-Dialog für Listen und Ordner: ein Fenster mit Titel und
  Beschreibungstext; beim Eingang ist nur das Titelfeld gesperrt. Die früheren
  getrennten Menüeinträge existieren nicht mehr.
- Mehrfachauswahl in der Seitenleiste: gemeinsames Verschieben in einen Ordner,
  Herauslösen, Einfärben und Verschieben in den Papierkorb; Alt+Auf/Ab sortiert
  die Auswahl ohne Maus.
- Labels: eigene Farbpalette in beiden Themes, Zuweisen und Lösen über die
  Auswahl, Anzeige in der rechten Labelspalte neben der Fälligkeit, Spaltenbreite
  0 ohne Labels, Bereinigung von Verweisen auf gelöschte Labels, Ablehnung
  doppelter Label-IDs im Komplettbackup sowie der Rundlauf über TXT, CSV und
  Markdown.
- Kalender: Wochenstart am Montag, aktuelles Wochen- oder Monatsraster, Sammeln
  aller Fälligkeiten im Zeitraum ohne Gruppen, Sprung in die Quellliste.
- Automatisches Speichern: Zeitsperre gegen Sicherungsflut, erzwungener
  Sicherungspunkt, erneutes Speichern eines offenen Standes und Neuplanung des
  Zyklus; `cancel_pending_callbacks` beendet ihn.
- Backup-Rotation: Mindestbestand bleibt auch bei ausschließlich alten
  Sicherungen erhalten, ältere darüber hinaus werden entfernt, die Obergrenze
  greift, und portable `vor_import_*.glidebackup` bleiben unangetastet.
- Datenformat 7 mit Referenzbestand `tests/fixtures/current_v7/`; ein Format-6-
  Bestand ohne `labels` und `trash` lädt unverändert.

## Automatisiert seit 2.6.0

- Gruppen als eigene Punktart pruefen: Statusfelder werden verworfen, Umwandeln
  in beide Richtungen, Zaehlung und Fortschritt ohne Gruppen, Marker und Anzahl
  in der Zeile, eigener Tag, keine Faelligkeitsspalte.
- Gruppieren, Aufloesen, Unterpunkt anlegen und Duplizieren auf echten Daten
  pruefen; nach dem Duplizieren muessen alle Punkt-IDs eindeutig bleiben.
- Statusfilter: eine Gruppe bleibt nur sichtbar, wenn ein Unterpunkt passt.
- Gruppen erscheinen nicht in der abgeleiteten Faelligkeitsansicht.
- Export und Import halten die Punktart in TXT, Markdown und CSV.
- Komplettbackup mit unbekannter Punktart wird abgewiesen.
- Vollstaendigkeit der Kontextmenues fuer Aufgabe, Gruppe, leeren Listenbereich,
  Seitenleisten-Liste, Ordner und die abgeleitete Ansicht pruefen; der Eingang
  bleibt unbenennbar.
- Auswahl des schwersten Schriftschnitts pruefen, einschliesslich der Regel,
  dass Semibold nicht gegen Bold gewinnt.

- Anwendung mit isoliertem temporärem App-Datenordner starten. Die Isolierung
  läuft über `GLIDE_DATA_DIR` und wird zu Testbeginn gegen `BASE_DIR` verifiziert.
  `APPDATA` allein wirkt nur unter Windows; unter macOS und Linux hätte ein
  Testlauf sonst die echten Nutzerdaten benutzt.
- Anhangsnamen, die nach der Bereinigung ungültig würden (`report.`, `a.b.`,
  `datei.☃`, reservierte Windows-Namen, überlange Namen), auf einen speicherbaren
  und wieder auflösbaren Pfad prüfen; Anzeigename und Datensatz-ID bleiben erhalten.
- Anhangs-Remapping beim Backup-Import mit einem nicht normierbaren Anzeigenamen
  terminieren lassen.
- Gespeicherte Fenstergeometrie auf den sichtbaren Bildschirmbereich begrenzen.
- Wiederholten Listenaufbau ohne Ansammlung toter `after`-IDs prüfen.
- Sehr langen Listentitel setzen und sicherstellen, dass Design-Umschalter und
  Fortschrittszeile im Fenster bleiben und der Titel gekürzt dargestellt wird.
- Textanfang aller Eingabefelder in Punktdetails, Titel-, Beschreibungstext- und
  Zielauswahldialog auf denselben Wert prüfen.
- Eingang anlegen, schützen und mit „Listen“ exakt linksbündig darstellen.
- Systemzeilen und ausgerichteten horizontalen Trenner geometrisch prüfen.
- „In Bearbeitung“ als rein abgeleitete, chronologische Ansicht aller gültig datierten Aufgaben prüfen; Quellnavigation sowie Schutz vor einer versehentlichen virtuellen Listenpersistenz verifizieren.
- NumLock-/Command-Bindings unter Windows prüfen.
- Optionales `ISO_Left_Tab` auf Tk-Varianten ohne diesen Keysym abfangen.
- Dark-Mode-Menü einfärben, robuste Menübuttons prüfen und den realen DWM-Dark-Wert bereits beim ersten Mapping sowie beim Umschalten verifizieren.
- Aufgabe zwischen Listen verschieben und global rückgängig machen.
- Aufgaben-Kontextmenü, Mehrfachauswahl, direkte Wichtigkeit, Fälligkeit und persistente Farbe prüfen.
- Sicherstellen, dass das gepostete Aufgaben-Kontextmenü nicht vor der Benutzeraktion zerstört wird und beim nächsten Öffnen kontrolliert aufgeräumt wird.
- Fälligkeiten getrennt vom Aufgabentext in der festen rechten Treeview-Spalte und mit konstantem rechten Innenabstand prüfen.
- Aufklappen/Zuklappen verschachtelter Aufgaben sowie unabhängige Zustände mehrerer Seitenleistenordner über eine Aktualisierung hinweg prüfen.
- Ordnerübersicht, Listenneuanlage im Ordner, tatsächliches Umsortieren und Verschieben in einen anderen Ordner per Drag & Drop prüfen.
- Reine Anzeigekürzung langer Seitenleistentitel und unveränderte Speicherung des vollständigen Namens prüfen.
- Beschreibungstext auf Liste und Ordner, gezielte Ordner-Kontextaktion, Aufgabenbeschreibung und Anhang normalisieren und speichern.
- Anhang unabhängig von der Quelldatei öffnen können; atomaren Kopierpfad, Fehlerbereinigung und 512-MB-Grenze prüfen.
- Eingecheckte v7-, v6-, v5-, v4- und v2-Referenzdaten tatsächlich laden und normalisieren.
- Datenformat 10, ältere JSON-Daten sowie die Backup-Kompatibilität der Formate 4 bis 10 prüfen.
- Komplettbackup inklusive Anhang exportieren und wiederherstellen.
- Kollisionen beim Restore durch neue Anhangspfade ausschließen.
- Fehlende Anhänge, Speicherfehler, ungültige Schemata und unsichere ZIP-Pfade ablehnen.
- TXT-Beschreibung, Fälligkeit und historischen `[Seitennotiz]`-Block erhalten; CSV-Formelpräfix absichern.

## Vor jedem Release manuell

- Papierkorb mit realen Daten: Listen und Ordner löschen, per Doppelklick und
  Kontextmenü wiederherstellen, in einen anderen Ordner wiederherstellen,
  einzelne Einträge endgültig entfernen und den Papierkorb leeren. Nach einem
  Neustart müssen alle Einträge unverändert vorhanden sein.
- Labels anlegen, umbenennen, umfärben und entfernen; Zuweisung über das
  Kontextmenü eines Punkts, einer Liste, eines Ordners und in „In Bearbeitung“
  prüfen. Farbig dargestellt sein müssen: Labelverwaltung, Farbauswahldialog,
  Kontextmenüeinträge und die Kopfzeile einer geöffneten Liste oder eines
  Ordners. In der Aufgabenliste steht Text in der Labelfarbe – ein Label je
  Zeile, alles Weitere als Zähler. Chips sind dort nicht möglich, solange die
  Liste eine `ttk.Treeview` ist.
- Kopfbereich beim Listenwechsel: zwischen einer Liste mit Labels und einer
  ohne wechseln. Fortschrittszeile, Titel und alles darunter dürfen sich nicht
  um einen Pixel verschieben.
- Eingabemaske auf 1366×768: Die Maske muss ohne Bildlauf oder mit sauberem
  Bildlauf bedienbar sein. Kalenderknopf öffnet das Kalenderfenster; nach dem
  Schließen nimmt die Maske wieder Eingaben an. Dasselbe für die aufgeklappte
  Labelauswahl.
- Fälligkeit in der Liste: Ein Punkt mit Datum und Uhrzeit muss beides
  vollständig zeigen – auch bei anderer Systemschriftgröße.
- **Symbole auf Windows und macOS ansehen.** Der automatische Prüflauf zeichnet
  mit Linux-Schriften und sagt über die Darstellung auf den Zielsystemen nichts
  aus. Zu prüfen: Erscheint jedes Symbol (kein leeres Kästchen)? Sprengt eines
  die Zeilenhöhe der Aufgabenliste? Sitzt der Themenschalter-Wechsel ☾/☀?
- Umbenennen in der Seitenleiste: Klick auf eine ausgewählte Zeile öffnet nach
  kurzer Verzögerung das Eingabefeld; ein Doppelklick öffnet stattdessen den
  Dialog; nach einem Zug passiert nichts. Escape verwirft, Enter übernimmt, ein
  leerer Name wird verworfen. Der Eingang lässt sich nicht umbenennen.
- Bildlaufleisten: In einem Dialog mit wenig Inhalt darf keine Leiste zu sehen
  sein; sobald der Inhalt wächst, muss sie erscheinen.
- Auswahlmenüs: Kein Rahmen um die aufgeklappte Liste und keiner um den Eintrag
  unter dem Zeiger – in Hell und Dunkel.
- Pfeiltasten im Aufgabenbaum und in der Seitenleiste: nach einem Klick muss
  Auf/Ab die Auswahl bewegen.
- Kalender: über die Tage fahren – jeder Tag bekommt eine hellblaue Umrandung,
  der heutige Tag erhält seine Markierung beim Verlassen zurück. Doppelklick auf
  einen Tag legt eine Aufgabe mit dieser Fälligkeit an; der Dialog nennt die
  Zielliste, und der Kalender zeigt die Aufgabe sofort.
- Kalender in Hell und Dunkel: zwischen „Diese Woche“ und „Dieser Monat“
  umschalten, mit den Pfeilen Wochen beziehungsweise ganze Monate blättern,
  „Heute“ zurückspringen. Der heutige Tag ist umrandet, Tage benachbarter
  Monate sind ausgegraut, ein Klick auf eine Aufgabe öffnet sie in ihrer Liste,
  „+N weitere“ listet den ganzen Tag auf. In der Wochenansicht müssen lange
  Aufgabentitel umbrechen statt abgeschnitten zu werden.
- Verschieben per Tastatur: Alt+↑/↓ und Alt+←/→ im Aufgabenbaum und in der
  Seitenleiste; Entf in der Seitenleiste legt die Auswahl in den Papierkorb.
- Mehrfachauswahl in der Seitenleiste mit Shift und Strg, Drag & Drop mehrerer
  Listen auf einen Ordner, Alt+Auf/Ab.
- Automatisches Speichern über mindestens 15 Minuten laufen lassen und den
  Backup-Ordner beobachten: es dürfen weder unbegrenzt Dateien entstehen noch
  darf der Mindestbestand unterschritten werden.

- Windows 10 und 11: NumLock an/aus, CapsLock an/aus, alle Tastenkürzel.
- Titelschrift auf Windows sichtbar pruefen: die Hauptueberschrift muss in
  „Segoe UI Black“ erscheinen, nicht im regulaeren Fettschnitt.
- Alle Kontextmenues einzeln oeffnen und jeden Eintrag ausfuehren; gesperrte
  Eintraege duerfen nicht ausloesen.
- Gruppen mit realen Daten anlegen, verschachteln, per Drag & Drop umsortieren,
  zwischen Listen verschieben, exportieren und wieder importieren.
- macOS: Cmd+Q mit ungespeicherten Änderungen, Rückschritt zum Löschen eines
  Punktes, Command-Kürzel für Speichern, Export, Import, Design und neue Liste
  sowie die plattformgerechten Beschriftungen in Menü und Tastenkürzel-Dialog.
- macOS: Dateien im Punktdetails-Dialog anhängen; der Dialog muss nach dem
  nativen Dateiauswahlfenster weiterhin bedienbar bleiben.
- Dark Mode beim Start und beim Umschalten; Titelleiste, vier Menüs und alle Dialoge.
- Rechtsklickaktionen einzeln ausführen; Escape und Klick außerhalb dürfen keine Daten ändern.
- Fälligkeit bei Mindestbreite, 1000-Pixel-Standardbreite, langen Texten und Unterpunkten rechts im lila Auswahlbalken prüfen.
- Eingang und „In Bearbeitung“ in Hell- und Dunkelmodus, Trennlinie, Einzüge und Abstände prüfen.
- Sehr lange Listen-/Ordnernamen in der Seitenleiste prüfen; die Hauptüberschrift
  kürzt bei Platzmangel sichtbar mit `…`, Dialoge, Fenstertitel und Export
  enthalten weiterhin den vollständigen Namen.
- Fenster auf einem zweiten Monitor positionieren, Monitor abmelden, Glide neu
  starten: Das Fenster muss sichtbar erscheinen.
- Ordnerübersicht: Listen innerhalb des Ordners sortieren und in beide Richtungen zwischen Ordnern verschieben.
- Mehrere Seitenleistenordner unabhängig schließen; Auswahl und Aktualisierung dürfen keinen anderen Ordner wieder öffnen.
- Verschachtelte Aufgabe mit Unterpunkten über den Pfeil schließen und wieder öffnen.
- „In Bearbeitung“ mit datierten Aufgaben aus mehreren Listen, Eingang, erledigten Aufgaben, Suche und Statusfilter sichten.
- Drag & Drop innerhalb einer Liste, zwischen Listen, auf Ordner und außerhalb gültiger Ziele.
- Große Listen, Scrollen, Mehrfachauswahl, Rückgängig, Suche und Filter.
- Öffnen, Entfernen und Restore von realen Bild- und Dateianhängen; eine gelöschte Quelldatei darf die verwaltete Kopie nicht beeinträchtigen.
- Neustart mit bestehenden v2-, v3-, v4- und v5-Daten sowie einem v4-Komplettbackup.
- Clean-Machine-Test ohne Entwicklungs-Python erst nach vorhandenem Build.

## Release-Gate

Ein grüner Integrationstest belegt den Source-Stand, ersetzt aber keine Installer-, Signing-, macOS- oder Store-Prüfung.
