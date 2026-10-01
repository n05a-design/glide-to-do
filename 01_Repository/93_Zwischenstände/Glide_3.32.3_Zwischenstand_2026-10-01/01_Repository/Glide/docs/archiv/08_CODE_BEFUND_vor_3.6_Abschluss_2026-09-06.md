# Codebefund 3.0.2 und was in 3.1.0 daraus wurde

Stand des Abgleichs: 04.09.2026 · App 3.2.0 · Schema 10.
Der folgende Befund erhält die Ergebnisse von 3.0.2/3.1.0 als Historie.
Aktuell gemessen: 14.591 Zeilen, 539 Funktionen/Methoden, 133 Konstanten,
508/520 Methoden erreichbar, 25 Funktionen über 80 Zeilen, 102 doppelte Blöcke,
0 strukturgleiche Methodenpaare, 18 breite `except Exception`.
Die Verzeichnis-Migration ist seit 3.2.0 entfernt. Alle acht Schema-Fixtures
(2 und 4 bis 10) bleiben erhalten. Drei Symbolarten außerhalb `ICONS` sind
noch Emoji. Ein behaupteter Verlust von „Phase 11“ ist aus dem vorliegenden
Bestand ohne Git-Historie nicht nachweisbar. Aktuelle Einzelbefunde und offene
Grenzwerte stehen in `11_BESTANDSANALYSE.md`; historische Kennzahlen unten
sind keine erneuten Prüfnachweise.

Ergebnis der ersten Etappe der Codeüberprüfung. Zwei Werkzeuge mit
unterschiedlichem Ansatz, damit sich ihre Schwächen nicht decken:

- `tests/tools/analyse_statisch.py` liest den Syntaxbaum und fragt: Was ist
  definiert, wie groß, wie tief verschachtelt, wie oft wörtlich wiederholt?
- `tests/tools/analyse_erreichbarkeit.py` geht vom Programmstart aus und fragt:
  Was ist von dort erreichbar, welche Methoden haben denselben Aufbau, welche
  Attribute werden geschrieben, ohne je gelesen zu werden?

Dass zwei Verfahren nötig sind, hat sich sofort gezeigt: Der erste Lauf der
Erreichbarkeitsanalyse hielt 144 Methoden für tot – sie waren über
`command=self.foo` und `bind(…, self.foo)` gebunden, also als Wert genannt und
nicht aufgerufen. Nach der Korrektur blieben 9. Umgekehrt meldete die statische
Analyse „0 ungenutzte Konstanten", weil `self.KONSTANTE` als Nennung zählt;
über den Datenfluss fand die zweite Analyse trotzdem welche.

## Kennzahlen

| | |
|---|---|
| Zeilen | 14.704 |
| Funktionen und Methoden | 530 |
| Klassenkonstanten | 133 |
| Vom Start erreichbar | 497 von 512 |
| Funktionen über 80 Zeilen | 26 |
| Wörtlich doppelte Blöcke (≥ 6 Zeilen) | 111 Stellen |
| Auskommentierter Code | 2 Zeilen |
| TODO/FIXME/HACK | 0 |
| `print()` im Quelltext | 0 |
| Nacktes `except:` | 0 |

Der Bestand ist deutlich besser als das Wort „Code-Reste" vermuten lässt: keine
Altlasten in Form von auskommentierten Blöcken, keine offenen Merkzettel, keine
Debug-Ausgaben. Was es gibt, ist Wiederholung und Größe.

## Befunde nach Gewicht

### 1. Zwei Abläufe wiederholen sich durch die ganze Anwendung

Der häufigste doppelte Block kommt **achtmal** vor:

```python
if not changed:
    if self.undo_stack:
        self.undo_stack.pop()
    return "break"
self.save_items()
self.refresh_tree(selected_id=item_ids[-1])
```

Der zweithäufigste **sechsmal**:

```python
if not self.require_list_view():
    return "break"
item_ids = self.get_selected_item_ids()
if not item_ids:
    messagebox.showwarning("Hinweis", "Zuerst einen Punkt auswählen.")
    return "break"
self.snapshot_undo()
```

Zusammen sind das Anfang und Ende praktisch jeder Änderungsoperation. Ein
gemeinsamer Rahmen – ein Kontextmanager wie der vorhandene
`guarded_structural_change` – ersetzt rund 140 Zeilen und macht aus einer
stillschweigenden Konvention eine erzwungene. Der Fehler, den das verhindert,
ist konkret: Wer den Rücknahme-Zweig vergisst, hinterlässt bei jeder wirkungslos
gebliebenen Aktion einen Undo-Punkt, der nichts rückgängig macht.

**Aufwand:** mittel. **Nutzen:** hoch – weniger Zeilen und eine Fehlerklasse
weniger.

### 2. Zehn Funktionen tragen ein Fünftel des Quelltexts

| Funktion | Zeilen |
|---|---|
| `create_ui` | 465 |
| `item_form_dialog` | 433 |
| `open_calendar_view` | 349 |
| `apply_theme` | 225 |
| `validate_backup_schema` | 223 |
| `open_label_manager` | 187 |
| `import_full_backup` | 171 |
| `create_list_sidebar` | 166 |
| `__init__` | 157 |
| `insert_tree_items` | 144 |

Zusammen 2.520 Zeilen. `insert_tree_items` ist zusätzlich neun Ebenen tief
verschachtelt – die höchste Zahl im Bestand und der wahrscheinlichste Ort für
einen Fehler, den niemand beim Lesen findet.

Diese Funktionen sind nicht schlecht geschrieben, sie sind gewachsen: Jede
besteht aus mehreren klar abgrenzbaren Abschnitten, die bereits durch
Kommentare getrennt sind. Aus jedem Abschnitt eine Methode zu machen ist
mechanisch und risikoarm.

**Aufwand:** hoch. **Nutzen:** hoch, aber langfristig – heute funktioniert alles.

### 3. Kleine echte Reste

- `self.calendar_button_label` wird gesetzt und nie gelesen (aus 3.0.0).
- `LabelChip.set_colors` und `_store_pending_attachments` sind über
  Zeichenketten oder Tests erreichbar, aber im Programmablauf nicht mehr.
- Drei Methodenpaare mit identischem Aufbau: `_make_field`/`_make_calendar_surface`,
  `sidebar_row_font`/`task_row_font`, `iter_all_list_objects`/`iter_all_folder_objects`.

**Aufwand:** gering. **Nutzen:** gering, aber es kostet nichts.

### 4. Zwanzig breite `except Exception`

Kein nacktes `except:`, aber zwanzig Stellen fangen jede Ausnahme. Bei Tk ist
das oft richtig – ein zerstörtes Widget wirft je nach Zeitpunkt Verschiedenes.
An anderen Stellen verdeckt es Fehler. Jede Stelle einzeln zu prüfen lohnt.

**Aufwand:** mittel. **Nutzen:** mittel – findet möglicherweise die Ursache des
gemeldeten Einfrierens.

### 5. Altdaten: weniger Ballast als erwartet

Die Freigabe, Rückwärtskompatibilität aufzugeben, bringt weniger als gedacht –
weil es kaum Code gibt, der nur dafür da ist. Die Anwendung hat **keine
Migrationszweige je Formatversion**; sie prüft beim Laden nur, ob die Version
im gültigen Bereich liegt, und die `normalize_*`-Funktionen ergänzen fehlende
Felder. Das ist der robuste Ansatz und trägt sich selbst.

Was tatsächlich an Altlasten existiert:

- rund 100 Zeilen Verzeichnis-Migration (`migrate_from_legacy_app_dirs` und
  Helfer) für Nutzerdaten aus früheren Programmnamen,
- `LEGACY_LABEL_COLOR_MAP` mit gut zehn Zeilen,
- sieben Fixture-Ordner für die Formate 2 bis 9.

Die Fixtures sind kein Ballast, sondern die Absicherung dafür, dass alte
Sicherungen weiter lesbar sind. Sie zu entfernen spart nichts am Programm und
nimmt der Prüfung ihre Grundlage.

**Empfehlung:** nichts davon entfernen. Der Gewinn wären etwa 110 Zeilen, der
Verlust die Fähigkeit, eine ältere Sicherung zu öffnen.

## Was daraus folgt

Vorschlag für die Reihenfolge war:

1. **Die beiden wiederkehrenden Abläufe zusammenfassen** – größter Hebel, klar
   abgrenzbar, sofort prüfbar.
2. **Kleine Reste entfernen** – billig.
3. **Die breiten `except`-Blöcke durchgehen** – möglicherweise steckt hier der
   Aufhänger.
4. **Die großen Funktionen aufteilen** – nur wenn Budget bleibt; sie
   funktionieren heute, der Gewinn ist künftige Lesbarkeit.

# Was in 3.1.0 daraus geworden ist

## Punkt 1 – erledigt

`item_change` und `sidebar_change` ersetzen 31 der 39 Stellen mit
`undo_stack.pop()`; `selected_items_for_change` ersetzt die sechs Kopien des
Auswahl-Vorfilters. Die verbliebenen sieben Stellen sind die beiden Rahmen
selbst, „Rückgängig" und die Import-Wege (siehe unten).

**Dabei gefunden:** Der Rückgängig-Speicher kürzte schon beim Anlegen des
Schnappschusses. Bei vollem Speicher kostete damit eine Aktion, die
anschließend nichts bewirkte, den ältesten Schritt. Der Fehler war
seit jeher da und wäre ohne den Rahmen weiter unentdeckt geblieben – erst der
Test des Rahmens hat ihn sichtbar gemacht. Gekürzt wird jetzt erst, wenn
feststeht, dass der Schnappschuss bleibt (`snapshot_undo(trim=False)` +
`trim_undo_stack`).

## Punkt 2 – erledigt

- `self.calendar_button_label`: entfernt.
- Kommentar über die selbstgezeichneten Ordner-Klappdreiecke: entfernt, die
  Sache gibt es seit 3.0.1 nicht mehr.
- Alle drei strukturgleichen Methodenpaare zusammengeführt. Die
  Erreichbarkeitsanalyse meldet jetzt **0 Gruppen** statt 3.
- `LabelChip.set_colors`, `_store_pending_attachments`, `format_file_size` und
  `refresh_scrollbar_state` sind **nicht** tot – die erste Analyse hat sich
  geirrt, weil ihre Aufrufer selbst nicht vom gewählten Einstiegspunkt aus
  erreichbar sind. Vor dem Löschen geprüft, nichts entfernt.

## Punkt 3 – anders ausgegangen als vermutet

Die zwanzig breiten `except Exception` sind der falsche Verdächtige. Neunzehn
davon sind an ihrer Stelle richtig: Migration beim Start, Einstellungen,
Fenstergeometrie, Win32-Aufrufe, Autosave-Takt, Export- und Import-Meldungen.
Ein `raise` an diesen Stellen würde das Programm beenden statt es zu retten.

Der Aufhänger steckte woanders – im Griff (`grab`), den ein modaler Dialog an
sich nimmt:

> `grab_set` und `wait_window` standen an **sieben** Stellen einzeln
> nebeneinander. **Eine einzige** davon gab den Griff hinterher an das
> aufrufende Fenster zurück (`themed_due_dialog`, seit 3.0.2).

Wer aus einer Eingabemaske heraus die Farbauswahl, die Namensabfrage oder die
Listenauswahl öffnete, hatte danach eine Maske vor sich, die noch zu sehen war,
aber keine Eingabe mehr annahm. Genau die Beschreibung des gemeldeten
„hängt sich auf".

**Behoben:** `run_modal` ist jetzt der einzige Weg, auf dem ein Dialog wartet,
und `modal_over` ermittelt den vorherigen Griffhalter bei Bedarf selbst über
`grab_current()`. Der Fall ist im Test abgedeckt: Ein Fenster mit Griff, ein
Unterdialog darüber, und nach dessen Ende muss der Griff zurück sein.

Das ist eine belegte Ursache für ein Einfrieren, aber **kein Beweis, dass es die
einzige war**. Der Fehler ließ sich hier nicht nachstellen; die Aussage stützt
sich auf den Mechanismus, nicht auf eine Reproduktion.

## Punkt 4 – teilweise

`on_sidebar_drag_end` war der zweittiefste Fall (acht Ebenen) und ist in
`drop_sidebar_list` und `drop_sidebar_folder` geteilt. Die zehn größten
Funktionen sind unangetastet: Sie sind Aufbau-Code für die Oberfläche, jede
Teilung dort ist Textverschiebung ohne heutigen Gewinn. `insert_tree_items` mit
neun Ebenen bleibt der wahrscheinlichste Ort für einen stillen Fehler und ist
der erste Kandidat, falls diese Arbeit fortgesetzt wird.

## Punkt 5 – ausdrücklich nicht angefasst

**Die Import- und Backup-Wege** (`import_txt_as_new_lists`, `import_from_txt`,
`import_full_backup`). Sie haben eine eigene Rücknahme – den Labelbestand vor
dem Einlesen – und einen eigenen Abbruchpfad mit Aufräumen angelegter Dateien.
Sie in den gemeinsamen Rahmen zu zwingen hätte den datenkritischsten Teil der
Anwendung umgebaut, ohne etwas zu gewinnen.

**Die Rückwärtskompatibilität.** Die Freigabe brachte nichts: keine
Migrationszweige je Formatversion, nur rund 110 Zeilen Verzeichnis-Migration.

## Offen geblieben

- **Uneinheitliche Symbole.** Die `ICONS`-Tabelle begründet ausdrücklich, warum
  Textzeichen statt farbiger Emoji verwendet werden – aber `DUE_COLUMN_ICON`
  ist `📅`, der Kalenderknopf in der Eingabemaske ebenfalls, und die
  Anhang-Anzeige nutzt `📎` an drei Stellen. Das war nicht Teil der
  Symbolauswahl von 3.0.0 und wurde deshalb **nicht** eigenmächtig geändert;
  es wäre eine Entscheidung, keine Aufräumarbeit.
- **`insert_tree_items`**, neun Ebenen tief.
- **Phase 11 von `audit_app.py`**, seit der Übernahme verloren.
