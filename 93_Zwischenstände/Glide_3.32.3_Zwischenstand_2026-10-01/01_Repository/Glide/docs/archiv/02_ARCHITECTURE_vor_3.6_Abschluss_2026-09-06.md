# Architektur – Stand 3.4.0

## Ergänzungen 3.4.0 (maßgeblich für die folgenden historischen Abschnitte)

- `HOME_VIEW` ist eine abgeleitete Startseite. Die sechs Systemzeilen lauten
  Startseite, Eingang, In Bearbeitung, Labels, Verspätet, Papierkorb.
- Seitenleisten verwenden eine eigene, rechts ausgerichtete `count`-Spalte.
  Ordner zählen rekursiv Aufgaben, Namen werden nach Pixelbreite gekürzt.
  `SIDEBAR_INDENT=12`; die starre Begrenzung auf 20 Zeichen gilt nur noch für
  die Rückfallebene ohne Tk-Geometrie.
- Die zusätzlichen 24 Pixel `text_gap` stehen im Anzeigeablauf vor `due`;
  die gespeicherte Wertefolge der Baumzeilen bleibt due/labels/due_padding.
- `PALETTE` enthält physische Farben, `THEMES` die semantischen Verwendungen.
  `LabelDropdown.on_change` synchronisiert Artlabel und wechselnde Formfelder;
  die Auswahlfläche liegt ausschließlich rechts vom Chip.
- `themed_message_dialog` und fünf Wrapper ersetzen alle messagebox-Aufrufe.
  Native Dateiauswahl gehört weiterhin dem Betriebssystem.
- `normalize_personal_settings` ergänzt lokale Einstellungen; erste Migration
  sichert die bisherige Datei. `record_recent_list_edits` vergleicht nach
  erfolgreichem Speichern Inhaltsprüfsummen, ohne Aufgabenfelder zu erweitern.
  Ein Tageswechsel wird alle 30 Sekunden geprüft. Vorlagen verwenden
  `sidebar_change` mit neuen IDs. Aufgabenformat und Backups bleiben Version 10.
- Die alten UI-Emoji-Ausnahmen unten gelten nur für 3.2.0. Aktueller Satz:
  `ICONS`, `IMPORTANCE_MARKERS`, `GROUP_MARKER`. Legacy-Marker sind nur Parserdaten.

## Aktueller Aufbau

Die produktive Anwendung ist weiterhin ein bewusst zusammengehaltener Tkinter-Monolith unter `src/glide/app.pyw`. Die Repository-Struktur trennt Source, Tests, Fixtures, Dokumentation, Assets und spätere Packaging-Dateien, ohne zur Stabilisierung gleichzeitig eine risikoreiche Modulzerlegung vorzunehmen.

## Datenmodell

- Ordner enthalten Listen **und weitere Ordner**. Die Zugehörigkeit steht im Feld `parent_id`; fehlt es oder zeigt es ins Leere, steht der Ordner auf oberster Ebene. Die Verschachtelung endet bei `MAX_FOLDER_DEPTH` Ebenen, und ein Ordner kann nie sein eigener Vorfahre werden: `can_move_folder_into` ist die einzige Stelle, die das entscheidet, und gilt damit für Maus, Menü und Tastatur gleichermaßen. `normalize_folder_parents` räumt beim Laden unbekannte Eltern, Kreise und zu tiefe Zweige auf; ein Kreis in einem portablen Backup wird abgewiesen.
- Listen und Ordner enthalten einen freien Beschreibungstext; intern bleibt das kompatible Feld `note` erhalten.
- Listen enthalten verschachtelte Punkte.
- Ein Punkt trägt Text, Status, Wichtigkeit, Fälligkeit, **optionale Uhrzeit**, Beschreibung, Anhänge, optionale Farbe, **Art** und Unterpunkte.
- Die Fälligkeit hat drei Zustände: keine, nur Datum (`due`), Datum und Uhrzeit (`due` plus `due_time`). Die Uhrzeit hängt am Datum – ohne `due` ist `due_time` immer `null`. Sie wirkt auf Anzeige, Suche, Export und die Sortierung innerhalb desselben Tages; `due_status` und die abgeleiteten Ansichten rechnen weiterhin auf Tagesbasis.
- Die Art steht im Feld `kind` mit vier Werten: `task`, `group`, `long` (Long-Task) und `heading` (Zwischenüberschrift). Fehlt das Feld oder ist der Wert unbekannt, gilt der Punkt als Aufgabe.
- **Aufgabe und Long-Task** teilen Status- und Terminlogik; Long-Tasks erlauben zusätzlich gespeicherte Zeilenumbrüche und erhalten ein festes Artlabel. **Gruppe und Zwischenüberschrift** sind reine Gliederung: `done` bleibt false, `due` bleibt null, `importance` bleibt 0. Die Normalisierung erzwingt das bei jedem Laden, damit kein manipulierter Bestand eine Gruppe oder Überschrift mit Status erzeugen kann.
- Gruppen und Überschriften zählen nicht als Aufgaben. Fortschrittsanzeige, Listenzähler in der Seitenleiste, „In Bearbeitung“, „Verspätet“ und der Kalender werten ausschließlich echte Aufgaben aus (`is_schedulable_item`). Bei aktivem Statusfilter werden sie nur über passende Unterpunkte sichtbar.
- Ein **Punkttext ist einzeilig**, außer beim Long-Task: `normalize_item_text` bewahrt dort bis zu 40 Textzeilen. Die Liste stellt davon höchstens fünf Zeilen dar; die vollständige Fassung bleibt in den Punktdetails zugänglich.
- Punkte, **Listen und Ordner** tragen eine Liste von **Label-IDs** im Feld `labels`. Fehlt das Feld, trägt der Datensatz keine Labels.
- Zwei **feste Labels** gehören zum Programm und tragen die Art eines Punkts: „Long-Task“ und „Überschrift“, erkennbar am Feld `system` (`long`/`heading`), nicht am Namen. `sync_item_kind_label` ist die einzige Stelle, die Art und Label angleicht; sie läuft bei jeder Neuanlage, bei jeder Umwandlung und einmal vollständig nach dem Laden – auch über die Kopien im Papierkorb. Ein Label zu vergeben wandelt den Punkt um, es zu nehmen wandelt ihn zurück. Entfernen und Umbenennen sind gesperrt, die Farbe ist frei. Für Listen und Ordner stehen sie nicht zur Auswahl.
- **Labels** stehen als eigene Sammlung auf oberster Ebene (`labels`) und bestehen aus ID, Name und Farbschlüssel. Sie nutzen dieselbe Palette wie Listen- und Aufgabenfarben; die Labelfarbe bleibt trotzdem eine eigene Eigenschaft und wird getrennt gesetzt und gespeichert. Beim Laden werden unbekannte Label-IDs überall entfernt, sodass kein Datensatz auf ein gelöschtes Label zeigt.
- Der **Papierkorb** ist eine eigene Sammlung auf oberster Ebene (`trash`). Ein Eintrag hält das vollständige Original eines gelöschten **Punkts**, einer gelöschten Liste oder eines gelöschten Ordners, den Löschzeitpunkt und die Herkunft. Ein gelöschter Punkt bringt seine Unterpunkte, seine Beschreibung und seine Anhänge mit und kehrt beim Wiederherstellen an dieselbe Stelle zurück; ist die nicht mehr da, ans Ende seiner Liste. Kein Löschen eines Punkts ist damit endgültig, solange der Eintrag im Papierkorb steht. Gelöschte Daten bleiben damit vollwertige Daten: ihre Anhänge zählen als referenziert und liegen in jedem Komplettbackup. Eine Obergrenze von 200 Einträgen verhindert, dass die Speicherdatei unbegrenzt wächst.
- Eine Liste mit `system_role: inbox` bildet den geschützten Eingang.
- Eingang, die virtuellen Ansichten „In Bearbeitung“ und „Verspätet“ sowie der Papierkorb bilden vier Systemzeilen am Kopf der Seitenleiste. Von der Überschrift „Listen“ und dem Listenbaum trennt sie ausschließlich Abstand – weder Band noch Linie noch zweiter Rahmen.
- „In Bearbeitung“ und „Verspätet“ werden bei jeder Anzeige aus allen echten Listen berechnet, chronologisch sortiert und nie als Liste oder Aufgabenkopie gespeichert. Sie teilen Aufbau, Zeilenformat und Navigation (`TASK_OVERVIEW_VIEWS`) und unterscheiden sich nur im Filter: „Verspätet“ zeigt, was `due_status` als `overdue` einstuft – vergangene Fälligkeit und nicht erledigt. Aktionen aus beiden Ansichten wirken direkt auf die Originalaufgabe in ihrer Quellliste.
- Der Zeilentext einer Seitenleistenzeile wird gegen die tatsächliche Spaltenbreite gemessen: der Zähler bleibt immer vollständig, gekürzt wird nur der Titel. Eine Breitenänderung passt ausschließlich die Zeilentexte an, nicht den ganzen Baum.
- Der Aufgabenbaum nutzt neben der flexiblen Hierarchiespalte eine feste rechte Fälligkeitsspalte, rechts daneben die Labelspalte und ganz rechts eine schmale Innenabstands-Spalte. Die Labelspalte hat die Breite 0, solange nichts anzuzeigen wäre – also weder ein eigenes Label existiert noch ein Punkt eines der festen Labels trägt – oder die aktive Ansicht keine Labels zeigt. Wird der Baum schmal, weicht zuerst die Label-, dann die Fälligkeitsspalte; `task_tree_column_widths` ist dafür eine reine Rechenmethode und ohne Fenster prüfbar. Das gespeicherte ISO-Datum und alle Import-/Exportformate bleiben davon unberührt.
- Listen können in der Seitenleiste und in der Ordnerübersicht per Drag & Drop umsortiert oder in einen anderen Ordner verschoben werden. Beide Wege verwenden dieselben kanonischen Verschiebeoperationen. Der Listenbaum erlaubt Mehrfachauswahl (`selectmode=extended`); alle Seitenleistenaktionen arbeiten auf der Auswahlmenge, bei genau einer markierten Zeile unverändert wie zuvor.
- Lange Namen werden in der Seitenleiste nach 20 Zeichen gekürzt; die Hauptüberschrift kürzt nur so weit, wie der verfügbare Platz es erzwingt. Gespeicherte Titel, Fenstertitel und Export bleiben vollständig.
- Datenformat-Version: 10 (unverändert seit 2.11.0).
- **Keine automatische Übernahme aus fremden Ordnern.** Bis 3.1.0 sah Glide beim
  Start nach, ob unter einem früheren Programmnamen oder im Skriptordner
  Nutzerdaten liegen, und kopierte sie herüber. Seit 3.2.0 nicht mehr: Der
  Datenordner ist der Datenordner, `GLIDE_DATA_DIR` überschreibt ihn, sonst
  nichts. Ältere Bestände kommen über „Komplettbackup einlesen“ herein – die
  Formatprüfung und die `normalize_*`-Funktionen bleiben unverändert und
  ergänzen fehlende Felder wie zuvor.

## Symbole

Die zentrale Symboltabelle `ICONS` enthält Textzeichen. Die angestrebte
vollständige Zentralisierung ist wegen der unten genannten Ausnahmen noch offen. Farbige Emoji kommen aus einer Ersatzschrift des Systems, ignorieren
die eingestellte Textfarbe, sind auf Windows und macOS verschieden breit und
passen nicht zuverlässig in die feste Zeilenhöhe des Aufgabenbaums. Ein
Textzeichen nimmt die Farbe der Zeile an – deshalb kann das Labelsymbol in der
Labelfarbe stehen und das Fälligkeitssymbol in Rot, wenn ein Punkt überfällig
ist.

`DUE_COLUMN_ICON` und `LABEL_COLUMN_ICON` verweisen auf die Tabelle, statt ihr
Zeichen selbst zu führen: Beide stehen im Aufgabenbaum unmittelbar nebeneinander
und müssen aus derselben Zeichenfamilie kommen. Der Integrationstest prüft, dass
kein Zeichen in `ICONS` oberhalb von U+1F000 liegt.

**Ausnahme, Stand 3.2.0:** Drei Symbolarten außerhalb von `ICONS` sind weiterhin
farbige Emoji und wurden beim Umbau übersehen:

| Konstante | Zeichen | Wo sichtbar |
|---|---|---|
| `IMPORTANCE_MARKERS[3]` | 🚩 (U+1F6A9) | Aufgabenbaum, Kalender, Zwischenablage – Wichtigkeit „hoch“ |
| `GROUP_MARKER` | 📁 (U+1F4C1) | Aufgabenbaum vor Gruppentiteln **und** im TXT-Export |
| `description_suffix` (zwei Ansichten) | 📝 (U+1F4DD) | Beschreibungsmarker in Aufgabenbaum und Aufgabenübersicht |

Der Test prüft nur `ICONS` und hat sie deshalb nicht gemeldet. Die Umstellung
ist offen und keine reine Aufräumarbeit: Das Zeichen für „hoch“ ist eine
Gestaltungsentscheidung, und `GROUP_MARKER` wird beim TXT-**Import** wieder
gelesen – ein neues Zeichen macht ältere Exportdateien beim Reimport zu
gewöhnlichen Aufgaben.

## Die Ansicht „Labels“

Neben Eingang, „In Bearbeitung“, „Verspätet“ und Papierkorb steht seit 3.3.0 eine vierte Systemansicht: `LABELS_VIEW`. Sie trägt denselben Bestand wie die beiden Fälligkeitsansichten zusammen, gruppiert ihn aber nach Labels. `DERIVED_ITEM_VIEWS` fasst alle drei abgeleiteten Ansichten zusammen – überall dort, wo dieselbe Regel gilt: nicht direkt befüllbar, Doppelklick öffnet die Quellliste, Kontextmenü arbeitet über `in_progress_item_sources`.

`label_view_groups()` liefert je Label die zugehörigen Punkte in der Reihenfolge der Labelverwaltung, gefolgt von „Ohne Label“. Ein Punkt mit mehreren Labels erscheint in jeder zugehörigen Gruppe; gezählt wird er über seine Kennung nur einmal. Die beiden festen Labels bilden keine Gruppe: Sie tragen die Art eines Punkts, und ein Zug dorthin würde ihn umwandeln statt ihn zu etikettieren. „Ohne Label“ sammelt ausschließlich `is_schedulable_item`-Punkte – Gruppen und Zwischenüberschriften sind Gliederung und ohne Label kein Rückstand.

`refresh_label_overview()` baut Gruppen- und Punktzeilen auf. Beide tragen den Tag `itemcolor_<Palettenschlüssel>` der Labelfarbe, sodass eine Gruppe optisch zusammenhängt. Die Zeilenkennungen führen das Label mit (`labelitem:<label>:<punkt>`), weil derselbe Punkt mehrfach im Baum steht; `label_view_row_groups` hält die Zuordnung Zeile → Gruppe. Die Labelspalte zeigt in dieser Ansicht die *übrigen* Labels: Das Label der Gruppe steht bereits in der Gruppenzeile.

`move_item_to_label_group()` führt den Zug aus. Es ersetzt genau das Label der Herkunftsgruppe durch das der Zielgruppe und lässt alle übrigen Labels stehen; das neue Label tritt an die Position des alten, damit das in der Liste sichtbare erste Label seinen Platz behält. Ein Zug nach „Ohne Label“ nimmt nur das Label der Herkunftsgruppe. `MAX_LABELS_PER_ITEM` wird vor dem Anhängen geprüft – ein Zug schneidet niemals bestehende Labels ab. Die Änderung läuft durch `item_change` und ist damit rückgängig zu machen.

## Datenintegrität

**Offene Grenzen im Stand 3.2.0:** `make_subitem` prüft die resultierende
Punkttiefe vor dem Umhängen nicht durchgehend; ein zuvor gültiger Bestand kann
dadurch die beim Laden erlaubte Tiefe überschreiten. `sync_item_kind_label`
kann zu 20 Labels ein weiteres Systemlabel hinzufügen. Beide Randfälle sind
reproduziert und in [der Bestandsanalyse](11_BESTANDSANALYSE.md) dokumentiert.
Der Bestandswächter bilanziert IDs; er ersetzt diese Grenzprüfungen nicht.

Zielvorgabe: Jede Aktion, die Punkte umordnet, soll unter
`guarded_structural_change` laufen. Die Umsetzung ist noch nicht lückenlos:
`indent_selected` und `outdent_selected` verwenden nur `item_change`. Der
Wächter zählt vor und nach der Aktion alle Punkt-IDs in allen Listen und im
Papierkorb; fehlt danach eine, wird der vorherige Stand aus dem
Rückgängig-Speicher hergestellt und der Vorgang gemeldet. Planmäßig entfallen
darf allein, was der Aufrufer über `expected_removals` nennt – in der Praxis nur
die leere Hülle einer aufgelösten Gruppe.

Das ersetzt keine korrekte Einzelfunktion, sondern sichert sie ab: Die Zusage
„Das Auflösen einer Gruppe darf niemals einen enthaltenen Punkt löschen“ hängt
damit nicht mehr an der Fehlerfreiheit einer Methode, sondern an einer Bilanz,
die jede dieser Methoden nach jedem Aufruf einhalten muss. `apply_snapshot` ist
die gemeinsame Grundlage von „Rückgängig“ und dem Wächter, damit beide denselben
Weg zurückgehen.

## Der Rahmen um eine Änderung

Seit 3.1.0 bündeln `item_change` und `sidebar_change` viele Änderungen an
Punkten, Listen und Ordnern. Die vollständige Nutzung bleibt die Zielvorgabe:
`add_child_item` und `apply_sidebar_rename` haben noch eigene Snapshot-/
Speicherfolgen. Die ausdrücklich gesonderten Import-/Backup-Wege bleiben
ebenfalls außerhalb dieser Rahmen. Beide Kontextmanager tun dasselbe in drei
Schritten: Rückgängig-Punkt anlegen, die Änderung ausführen lassen, abschließen.
Die Änderung meldet ihre Wirkung über `ChangeRecord.mark()`; bleibt die Meldung
aus, verschwindet der Rückgängig-Punkt wieder, und es wird weder gespeichert noch
neu gezeichnet.

Der Rahmen ist keine Bequemlichkeit, sondern eine Zusage: Vorher stand dieselbe
Abfolge an 36 Stellen wörtlich im Quelltext, und wer den Rücknahme-Zweig vergaß,
hinterließ bei jeder wirkungslos gebliebenen Aktion einen Rückgängig-Schritt, der
nichts zurücknimmt. Das kann jetzt nicht mehr passieren, weil der Rahmen die
Entscheidung erzwingt.

`selected_items_for_change` ist die dazugehörige Eingangsprüfung: offene Liste,
vorhandene Auswahl, Hinweis bei leerer Auswahl – oder `None`.

Der Rahmen sitzt **innerhalb** von `guarded_structural_change`, nicht darum
herum: Der Wächter bilanziert den Bestand über die gesamte Umbauaktion, der
Rahmen kümmert sich um einen einzelnen Rückgängig-Schritt darin.

`snapshot_undo(trim=False)` und `trim_undo_stack` gehören zu dieser Aufteilung.
Der Speicher hält `MAX_UNDO_STEPS` Schritte; gekürzt wird erst, wenn feststeht,
dass ein Schnappschuss bleibt. Sonst kostete eine wirkungslose Aktion bei vollem
Speicher den ältesten Schritt.

## Modale Fenster

`run_modal` ist der einzige Weg, auf dem ein Dialog wartet. Er setzt den Griff,
wartet auf das Fenster und gibt den Griff anschließend an den vorherigen Halter
zurück – den `modal_over` über `grab_current()` selbst ermittelt, wenn ihn der
Aufrufer nicht nennt.

Das ist notwendig, weil ein modaler Dialog den Griff an sich nimmt und ihn beim
Schließen nicht von allein zurückgibt. Öffnet man aus einer Eingabemaske heraus
Farbauswahl, Namensabfrage oder Listenauswahl, bliebe die Maske danach sichtbar,
nähme aber keine Eingabe mehr an – für den Benutzer nicht von einem Absturz zu
unterscheiden. Bis 3.0.2 stand `grab_set` + `wait_window` an sieben Stellen
einzeln, und nur eine davon gab den Griff zurück.

## Bedienung und Kontextmenüs

Jede Oberfläche besitzt ein eigenes, vollständiges Kontextmenü: Aufgabe und Gruppe im Aufgabenbaum, der leere Listenbereich, Seitenleisten-Listen, Seitenleisten-Ordner, eine Mehrfachauswahl in der Seitenleiste, die Ordnerübersicht, die Ansicht „In Bearbeitung“ und der Papierkorb. Nicht anwendbare Einträge werden sichtbar gesperrt statt ausgeblendet, damit die Menüform stabil bleibt und ihre Position erlernbar ist. Die Menüs werden bei jedem Öffnen neu aufgebaut und beim nächsten Öffnen kontrolliert zerstört.

## Spaltenbreiten folgen dem Inhalt

`due_column_width()` und `label_column_width()` messen weiterhin den längsten überhaupt möglichen Fall – Datum mit Uhrzeit, ein auf `LABEL_COLUMN_NAME_MAX_CHARS` gekürzter Name mit Zähler. Seit 3.3.0 ist das nur noch die Obergrenze: `content_column_widths()` misst nach jedem Baumaufbau den tatsächlichen Zelleninhalt, `fit_tree_columns_to_content()` setzt die Spalten danach, und `active_due_column_width()` / `active_label_column_width()` liefern das Minimum aus beidem. `finish_tree_refresh()` ist der gemeinsame Abschluss jedes Aufbauwegs; er ruft die Anpassung und danach die Prüfung der Bildlaufleiste auf.

Beide Spalten sind links ausgerichtet. Rechtsbündig richteten sie sich am rechten Zellenrand aus, sodass Kalender- und Labelsymbol je nach Textlänge in jeder Zeile an einer anderen Stelle standen; links stehen sie untereinander, und die Spalte ist ohnehin genau so breit wie ihr längster Inhalt. Im schmalen Fenster weichen weiterhin zuerst die Labels (`LABEL_COLUMN_MIN_TREE_WIDTH`), dann die Fälligkeit (`DUE_COLUMN_MIN_TREE_WIDTH`, seit 3.3.0 520 statt 470 – der alte Wert lag unterhalb der bei Fenstermindestgröße erreichbaren Baumbreite und griff nie).

## Labels als Chips

Ein Label wird seit 2.10.0 als abgerundete Fläche mit dunklem Text gezeichnet
(`LabelChip`, eine `tk.Canvas`): 9 Pixel Radius (`LabelChip.RADIUS`), links und rechts derselbe
Abstand, oben zwei Pixel weniger als unten – Großbuchstaben tragen oben mehr
Luft mit sich, optisch steht der Text damit mittig.

Die Flächenfarbe entsteht nicht aus einem festen Mischanteil, sondern aus einer
Zielhelligkeit. Ein fester Anteil trifft die sieben Palettenfarben ungleich:
Gelb ist von Haus aus rund doppelt so hell wie Lila und verschwände mit demselben
Anteil Weiß im Hintergrund. `mix_to_luminance` sucht per Intervallhalbierung den
Anteil, bei dem die Mischung die Zielhelligkeit erreicht – dadurch liegen alle
Farben auf demselben Kontrastniveau, in Hell und Dunkel.

`pack_label_chips` legt Chips zeilenweise ab und bricht um, statt seitlich
auszulaufen. Tk kennt kein Flow-Layout; da ein Chip seine Breite selbst messen
kann (`LabelChip.measure`), lässt sich der Umbruch beim Aufbau ausrechnen.

## Labelfarben und die Grenze der Treeview

Eine `ttk.Treeview` kann eine einzelne Zelle nicht getrennt einfärben:
`tag_configure` wirkt immer auf die ganze Zeile. In der Labelspalte des
Aufgabenbaums steht deshalb reiner Text.

2.7.0 versuchte es mit einem farbigen Punkt aus der Emoji-Schrift vor jedem
Labelnamen. Das ist gescheitert: Tk unter Windows rendert diese Zeichen
monochrom und täuschte damit eine falsche Farbe vor. Die Punkte sind entfernt.

Farbig – und damit eindeutig – ist ein Label überall dort, wo Tk eine
Einzelfärbung erlaubt:

- die Labelverwaltung färbt jede Zeile ihrer `tk.Listbox` über `itemconfig`,
- der Farbauswahldialog nutzt denselben Weg und zeigt jede Farbe in ihrer Farbe,
- jeder Menüeintrag trägt die Labelfarbe als `foreground`,
- die Kopfzeile einer geöffneten Liste oder eines Ordners verwendet
  `LabelChip`-Widgets mit eigener Flächenfarbe.

Eine farbige Zelle im Aufgabenbaum wäre nur mit einem eigengezeichneten Ersatz
für die Treeview möglich; das ist bewusst nicht Teil dieser Version.

## Mehrzeilige Punkte und Zwischenüberschriften in einer Treeview

Eine `ttk.Treeview` hat eine feste, für alle Zeilen gleiche Zeilenhöhe. Weder
ein Zeilenumbruch im Text noch ein hohes Bild ändert daran etwas; beides wird
auf `rowheight` abgeschnitten. Daraus folgen zwei Konstruktionen:

- Ein **Long-Task** besteht aus einer Kopfzeile mit Nummer und Symbolen plus
  Fortsetzungszeilen. Ihre IID trägt das Suffix `::line<n>`; `is_synthetic_row`
  und `owner_row_id` führen Klick, Kontextmenü, Auswahl und Ziehen auf den
  echten Punkt zurück, `iter_tree_ids` lässt sie aus. Hat der Punkt
  Unterpunkte, stehen die Fortsetzungszeilen als deren erste Kinder – sonst
  lägen sie hinter dem Unterbaum. Der Umbruch misst mit der tatsächlichen
  Schrift gegen die tatsächliche Spaltenbreite und hat eine zeichenbasierte
  Rückfallebene, falls beides nicht verfügbar ist.
- Der Abstand über einer **Zwischenüberschrift** ist eine leere Zeile mit dem
  Suffix `::gap<n>`. Sie ist nicht auswählbar und reagiert nicht auf den Hover.
  Ein halber Zeilenabstand ist hier nicht darstellbar.

Die Nummerierung setzt bei jeder gezeichneten Überschrift beide Zähler zurück:
`position_index` für die ungefilterte und `visible_index` für die gefilterte
Ansicht.

## Verschachtelte Ordner

Die Seitenleiste zeichnet den Ordnerbaum rekursiv (`_insert_sidebar_folder_rows`),
begrenzt durch dieselbe Tiefe, die auch das Verschieben begrenzt. Der Zähler einer
Ordnerzeile nennt alle Listen im gesamten Zweig, nicht nur die direkt darin
liegenden – sonst zeigte ein Ordner, der nur Unterordner enthält, eine Null.

Beim Ziehen entscheidet die Höhe im Ziel, was gemeint ist: oberes und unteres
Viertel sortieren davor und danach, die mittlere Hälfte legt hinein
(`sidebar_drop_zone`). Für Listen bleibt es beim alten Verhalten – auf einen
Ordner gezogen landet sie darin.

Ein gelöschter Ordner wandert mit seinem gesamten Zweig in den Papierkorb, von
innen nach außen, damit ein Elternteil erst nach seinen Kindern verschwindet.
Beim Wiederherstellen läuft es umgekehrt: der Ordner kehrt zurück, dann seine
Listen, dann seine Unterordner mit deren Inhalt. Existiert der frühere
Elternordner nicht mehr, landet der Zweig auf der obersten Ebene.

Überall dort, wo eine Liste zur Auswahl steht, nennt `list_path_title` ihren
vollständigen Pfad. Zwei gleichnamige Listen in verschiedenen Unterordnern wären
sonst nicht auseinanderzuhalten.

## Mehrzeiliger Aufgabentext

Der Text eines Punkts ist einzeilig – außer beim Long-Task. Das ist keine
Darstellungsfrage, sondern eine Formatfrage: Kalenderzelle, „In Bearbeitung“,
„Verspätet“, Zwischenablage und die Kopfzeile im TXT-Export haben genau eine
Zeile. `normalize_item_text` entscheidet das an einer Stelle und läuft bei jeder
Neuanlage, jeder Umwandlung und jedem Laden; `item_display_text` liefert überall
dort, wo eine Zeile gebraucht wird, die einzeilige Fassung.

Der TXT-Export schreibt die Folgezeilen eines Long-Tasks als
`Text:`-Fortsetzungen – dieselbe Mechanik wie beim Beschreibungstext – und der
Import setzt sie wieder zusammen; der Markdown-Export rückt sie ein.

## Auswahl und Hover

Eine `ttk.Treeview` färbt eine Zeile auf zwei Wegen: über die Zustandskarte des
Stils (`selected`) und über die Tags der Zeile. Der Auswahlzustand gewinnt gegen
eine Hintergrundfarbe aus einem Tag – genau darauf beruht die Aufteilung: **Lila
markiert die Auswahl, Hellblau den Hover.** Der Hover-Tag setzt ausschließlich
`background`, die Farbtags ausschließlich `foreground`; beide mischen sich
sauber, und eine ausgewählte Zeile bleibt lila, auch wenn der Mauszeiger darüber
steht. Während eines Ziehvorgangs wird der Hover unterdrückt, damit die
Zielmarkierung eindeutig bleibt.

## Kalender

Der Kalender ist eine abgeleitete Ansicht ohne eigene Daten und ohne externe
Anbindung: er liest ausschließlich die Fälligkeiten der vorhandenen Aufgaben. Er
öffnet als eigenes Fenster, weil ein Tagesraster im Aufgabenbaum nicht
darstellbar ist. Zwei Modi teilen sich dieselbe Zellenlogik:

- **Monatsansicht**: das montagsausgerichtete Raster des Referenzmonats, vom
  Montag der ersten bis zum Sonntag der letzten Woche – je nach Monat fünf oder
  sechs Zeilen. Die Pfeile blättern ganze Monate. Tage benachbarter Monate
  bleiben sichtbar, treten aber farblich zurück.
- **Wochenansicht**: genau eine Woche von Montag bis Sonntag über die volle
  Fensterhöhe, mit Platz für eine begrenzte Zahl sichtbarer Aufgaben je Tag und Zeilenumbruch statt
  Kürzung. Die Pfeile blättern einzelne Wochen; welchem Monat eine Woche
  zugerechnet wird, entscheidet ihr Donnerstag.

Die Überschrift nennt den dargestellten Monat, der heutige Tag ist umrandet, und
der Tag unter dem Mauszeiger erhält eine hellblaue Umrandung. Ein Klick auf eine
Aufgabe schließt das Fenster und öffnet sie in ihrer Quellliste; ein Doppelklick
auf einen Tag legt dort eine Aufgabe mit genau dieser Fälligkeit an. Sie entsteht
in der geöffneten Liste, ersatzweise im Eingang; der Dialog nennt das Ziel.

## Tastaturfokus im Aufgabenbaum

Die eigene Drag-Auswahl beantwortet jeden Klick auf den Aufgabenbaum mit
„break“, weil sie Mehrfachauswahl, Bereichsauswahl und Unterpunkt-Drop selbst
behandelt. Damit entfällt aber auch der Teil der nativen Class-Bindung, der den
Baum fokussiert – und ohne Tastaturfokus bleiben die Pfeiltasten wirkungslos.
Der Klickhandler fordert den Fokus deshalb ausdrücklich an; derselbe Aufruf
steht im Listenbaum der Seitenleiste.

Seit 2.8.0 sind zusätzlich `<Up>` und `<Down>` belegt: sie überspringen die
Fortsetzungs- und Abstandszeilen eines Long-Tasks beziehungsweise einer
Zwischenüberschrift. Ohne diese Bindung bliebe die Auswahl auf einer Zeile
stehen, hinter der kein Punkt steht, und jede Folgeaktion liefe ins Leere.

## Automatisches Speichern und Sicherungsrotation

Jede Änderung speichert weiterhin sofort. Zusätzlich läuft ein Zyklus von fünf
Minuten: ein wegen eines Fehlers offen gebliebener Stand wird erneut geschrieben,
andernfalls entsteht ein garantierter Sicherungspunkt. Der Zyklus meldet Fehler
bewusst nicht per Dialog, weil er im Hintergrund läuft; der nächste manuelle
Speichervorgang zeigt das Problem sichtbar an.

Automatische Sicherungen entstehen frühestens alle zwei Minuten, damit nicht
jeder Tastendruck eine Datei erzeugt. Die Rotation greift in dieser Reihenfolge:
die neuesten zehn Sicherungen bleiben immer erhalten, aus dem Rest verschwinden
alle älter als 30 Minuten, und zuletzt begrenzt die Obergrenze von 40 den Rest.
Portable `vor_import_*.glidebackup` unterliegen dieser Rotation nicht.

## Typografie

Die Oberfläche verwendet die Systemschrift. Für die Hauptüberschrift wird der schwerste verfügbare Schnitt gewählt: Tk kennt für `weight` nur `normal` und `bold`, schwerere Schnitte liegen unter Windows als eigene Schriftfamilien vor (`Segoe UI Black`). Existiert eine solche Familie, wird sie direkt benannt und ohne zusätzliches Bold gesetzt; sonst bleibt es beim regulären Fettschnitt. Semibold und Demibold sind ausgeschlossen, weil sie leichter als Bold sind. Die Konstante `HEADER_FONT_FAMILY` erlaubt eine eigene Hausschrift; benennt sie bereits einen schweren Schnitt, wird er unverändert übernommen.

## Speicher

`liste_speicher.json`, Einstellungen, automatische JSON-Sicherungen und verwaltete Anhänge liegen unter dem Benutzer-App-Datenordner. Die Umgebungsvariable `GLIDE_DATA_DIR` überschreibt diesen Ordner vollständig und ist der plattformunabhängige Weg, Tests zu isolieren. Neue Anhänge werden atomar in `attachments/` kopiert; der Speichername entsteht aus derselben geprüften Funktion wie beim Backup-Import, sodass ein geschriebener Pfad garantiert wieder auflösbar ist. Das portable `.glidebackup` bündelt einen validierten Daten-Snapshot und sämtliche referenzierten Anhänge.

## Workspace und Repository

`01_Repository/Glide` bleibt die technische Source of Truth. Der äußere Bereich `50_Ablage` nimmt QA-Renderläufe und projektbegleitende Zwischenstände auf. **Archiviert wird dezentral:** Jeder versionsführende Ordner besitzt einen eigenen Unterordner `Archiv/` für überholte Stände genau dieses Ordners – im Repository als `archiv/`, im äußeren Workspace als `Archiv/`. Ein zentrales `100_Archiv` gab es bis 3.1.0; es wurde aufgelöst, weil ein Rückgriff auf eine einzelne Vorgängerdatei nicht bedeuten soll, einen ganzen Altbestand durchsuchen zu müssen.

## Bewusste Architekturentscheidung

Der Monolith bleibt erhalten. Eine Modulzerlegung ist weder Voraussetzung der
Stabilisierung noch Teil des aktuellen Auftrags. `VERSION` und `APP_VERSION`
werden gemeinsam geprüft. Das Datenformat bleibt 10; fehlende Felder älterer
unterstützter Formate werden durch die bestehende Normalisierung ergänzt.

## Eine Eingabemaske für Anlegen und Bearbeiten

`item_form_dialog` ist seit 2.11.0 die einzige Maske für einen Punkt;
`new_item_dialog` und `themed_item_details_dialog` sind dünne Aufrufer. Der
Modus steuert nur Beschriftung und Vorbelegung, nicht den Funktionsumfang –
vorher waren es zwei Fenster, die jeweils die Hälfte der Eigenschaften kannten.
`apply_item_details` überträgt das Ergebnis auf einen bestehenden Punkt und ist
die einzige Stelle, die das tut.

Die Fälligkeit ist eine eigene Komponente: `DueField` (eine `tk.Frame`) trägt
Datumsfeld und Uhrzeitfeld. Tippen und Klicken schreiben in dasselbe Feld, und
`read()` prüft beide Eingaben – die Fehlermeldung entsteht damit einmal und gilt
überall. Dieselbe Komponente trägt `themed_due_dialog` hinter dem Menü
„Fälligkeit“; der frühere `themed_date_picker` ist entfallen.

Seit 2.12.0 hat die Komponente zwei Ausprägungen. `compact=True` zeigt Datum,
Uhrzeit und einen Kalenderknopf – so steht sie in der Eingabemaske, die neben
der Frist noch Titel, Art, Farbe, Labels, Beschreibung und Anhänge tragen muss.
Ohne den Schalter kommt der eingebettete Monatskalender dazu; so steht sie im
Kalenderfenster, wo der Kalender der Zweck ist. `_render_month` prüft eine
Bedingung, damit `set_due` und `_on_typed_date` beide Ausprägungen unverändert
bedienen. Wer aus einer modalen Maske heraus den Kalender öffnet, gibt sie als
`parent` mit: `themed_due_dialog` setzt den Grab danach dorthin zurück, sonst
nähme die Maske keine Eingabe mehr an.

Die Labelauswahl ist die zweite eigene Komponente: `LabelDropdown` zeigt
geschlossen eine Zeile und klappt für die Mehrfachauswahl auf. Das Aufklappfenster
setzt seinen eigenen Grab und gibt ihn beim Schließen an den Dialog zurück –
dieselbe Regel wie beim Kalender. `read()` liefert die gewählten IDs in der
Reihenfolge der Labelverwaltung, nicht in Klickreihenfolge: Sonst hinge die
gespeicherte Reihenfolge davon ab, in welcher Folge jemand angeklickt hat.

## Umbenennen in der Seitenleiste

`begin_sidebar_rename` legt ein `tk.Entry` über die Zeile, statt einen Dialog zu
öffnen. Drei Wege führen hinein: ein Klick auf eine bereits ausgewählte Zeile
(verzögert um `SIDEBAR_RENAME_DELAY_MS`), F2, und der Kontextmenüeintrag.

Die Verzögerung ist nötig, weil dieselbe Maustaste in der Seitenleiste bereits
Auswahl, Drag & Drop und Doppelklick bedient. `on_sidebar_drag_start` hält fest,
was vor dem Klick ausgewählt war – danach ist diese Auskunft nicht mehr zu
bekommen. Der Doppelklick bricht den Zeitgeber ab und behält den
Bearbeiten-Dialog; nach einem Zug passiert nichts.

`apply_sidebar_rename` setzt einen Undo-Punkt und aktualisiert Kopfzeile,
Fenstertitel, Seitenleiste und Liste. Der Eingang bleibt außen vor: Sein Name
ist ein Systemname. Ein leerer Name wird verworfen – eine Liste ohne Titel wäre
in der Seitenleiste nicht mehr auffindbar.

## Maus: Kontextmenü und Mehrfachauswahl

`<Control-Button-1>` wird ausschließlich unter macOS an das Kontextmenü
gebunden (`bind_context_menu_modifier`). Tk bevorzugt die spezifischere
Bindung: Unter Windows und Linux verdeckte der Zusatz sonst `<Button-1>`
vollständig, sodass das Menü aufging und die Mehrfachauswahl per Strg gar nicht
erreichbar war. `selection_modifier_pressed` und `selection_modifier_name`
liefern plattformgerecht Strg beziehungsweise Cmd – für die Logik wie für jeden
Hinweistext.
