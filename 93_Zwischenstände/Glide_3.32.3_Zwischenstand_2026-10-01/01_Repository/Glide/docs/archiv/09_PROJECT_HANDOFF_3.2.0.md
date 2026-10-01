# PROJECT HANDOFF – Glide

Stand: 04.09.2026 · App-Version **3.2.0** · Datenformat **10**
Nach der Bestandsanalyse aktualisiert. Die archivierte Vorgängerfassung
enthält den ursprünglichen Übergabetext. Erstellt für die Übergabe an einen neuen Agenten. Ersetzt nicht die Quelldateien,
sondern sagt, wo man hinsieht und was bereits entschieden ist.

---

## 1. Projektübersicht

**Glide** ist eine lokale Desktop-Aufgaben- und Listen-App in Python/Tkinter für
**Windows und macOS** (gleichwertige Zielplattformen; Linux läuft, ist aber kein
erklärtes Ziel). Kein Benutzerkonto, keine Cloud, kein Netzwerkzugriff für
Kernfunktionen. Nutzdaten liegen außerhalb des Programmordners im
plattformgerechten Benutzerverzeichnis.

Produktprinzipien: Local First · nur Python-Standardbibliothek plus Tk ·
Datenkompatibilität vor interner Umstrukturierung · Deutsch, einsprachig ·
kein Datenverlust unter keinen Umständen.

Aktueller Entwicklungsstand: funktional weit fortgeschritten und automatisiert
geprüft; **noch kein öffentliches Release**. Das nächste größere Ziel ist die
Release-Reife (manuelle Plattformprüfung, Build-Kette, Produktidentität), nicht
weitere Funktionalität.

Auftraggeber ist Grafikdesigner; die App wird für den eigenen Arbeitsalltag im
Bereich Marketing/Städtebau gebaut.

---

## 2. Aktueller Stand

| | |
|---|---|
| Version | 3.2.0 (`VERSION`, `APP_VERSION`) |
| Datenformat | 10 (`DATA_SCHEMA_VERSION`), unverändert seit 2.11.0 |
| Portable Backups lesbar ab Format | 4 (`MIN_PORTABLE_BACKUP_SCHEMA_VERSION`) |
| `src/glide/app.pyw` | 14.591 Zeilen, Monolith |
| Testsuiten | 3; Windows-Prüfung mit Python 3.12.12 / Tk 8.6.17 bestanden; aktueller Nachweis im QA-Bericht |
| Sichtprüfung | vorhandene Linux-Aufnahmen plus neue Windows-Aufnahmen der Arbeitslisten; Nachweis in Bestandsanalyse |
| Statische Analyse | 0 nie genannte Funktionen/Konstanten, 0 strukturgleiche Methodenpaare |
| Vollständige manuelle Plattformmatrix | **offen**; Windows-Arbeitsdaten in Hell/Dunkel visuell geprüft |

Die letzten beiden Versionen dieser Sitzung waren reine Aufräum- und
Konsolidierungsversionen ohne neue Bedienfunktionen.

---

## 3. Architektur / Technologie

- **Sprache/Laufzeit:** Python 3 (getestet 3.12) mit Tk/Tcl 8.6. Nur
  Standardbibliothek. Jede weitere Laufzeitabhängigkeit braucht eine
  dokumentierte Entscheidung (`AGENTS.md`).
- **Aufbau:** bewusst gehaltener Monolith `src/glide/app.pyw`, Klasse `ListApp`
  plus die Widget-Klassen `LabelChip`, `RoundedButton`, `RoundedContainer`,
  `ThemedAutoScrollbar`, `DueField`, `LabelDropdown`; Hilfsklassen
  `DataIntegrityError`, `ChangeRecord`.
- **Datenspeicher:** JSON unter `get_app_data_dir()`
  – Windows `%APPDATA%\Glide\`, macOS `~/Library/Application Support/Glide/`,
  Linux `$XDG_DATA_HOME/Glide/`. `GLIDE_DATA_DIR` überschreibt das vollständig
  und ist der **einzige** zulässige Weg der Testisolierung.
- **Dateien im Datenordner:** `liste_speicher.json`, `settings.json`,
  `window.conf`, `backups/` (40 rotierende Stände), `attachments/`.
- **Backupformat:** `.glidebackup` = ZIP mit `data.json` + `attachments/`.
- **Austauschformate:** TXT, Markdown, CSV (Semikolon, UTF-8-BOM).

### Zentrale Architekturmechanismen (alle aktiv)

1. **`guarded_structural_change(action_name, expected_removals=None)`** –
   Kontextmanager. Zählt alle Punkt-IDs vor und nach einer Umbauaktion; fehlt
   eine, wird der Vorzustand aus dem Rückgängig-Speicher hergestellt und der
   Vorgang gemeldet. Das ist die Zielregel für Umbauaktionen; `indent_selected`,
   `outdent_selected` und `toggle_indent_selected` laufen derzeit nur im
   Änderungsrahmen, ohne diesen zusätzlichen Wächter → offene
   Architekturabweichung, Abschnitt 13, **P1.4**.
2. **`item_change(item_ids, focus, restore, update_sidebar)`** und
   **`sidebar_change(refresh_tree)`** – seit 3.1.0 der gemeinsame Rahmen um
   viele Änderungen. `add_child_item` und
   `apply_sidebar_rename` nutzen noch eigene Snapshot-/Speicherfolgen.
   Der Rahmen legt den Rückgängig-Punkt an, lässt die Änderung laufen,
   schließt ab (speichern, neu zeichnen, Auswahl wiederherstellen). Die Änderung
   meldet ihre Wirkung über `ChangeRecord.mark()`; ohne Meldung entfällt der
   Rückgängig-Punkt. `item_change` sitzt **innerhalb** von
   `guarded_structural_change`, nie darum herum.
3. **`selected_items_for_change(warn, top_level_only, view_message)`** –
   Gemeinsame Eingangsprüfung für Punktänderungen (offene Liste, Auswahl vorhanden,
   Hinweis bei leerer Auswahl) oder `None`.
4. **`run_modal(dialog, parent=None)`** – seit 3.1.0 der **einzige** Weg, auf
   dem ein Dialog wartet. Setzt den Griff, wartet, gibt ihn zurück.
   `modal_over(parent=None)` ermittelt den vorherigen Griffhalter notfalls
   selbst über `grab_current()`.
5. **`snapshot_undo(trim=True)` / `trim_undo_stack()`** – der
   Rückgängig-Speicher hält `MAX_UNDO_STEPS = 20` Schritte; gekürzt wird erst,
   wenn feststeht, dass ein Schnappschuss bleibt.
6. **`ICONS`-Tabelle** – jedes Oberflächensymbol ist ein Textzeichen und steht
   dort. Das ist die Zielregel. Abweichungen im Ist-Code: `GROUP_MARKER` (📁),
   `IMPORTANCE_MARKERS[3]` (🚩), `description_suffix` (📝, zwei Baumansichten)
   und `note_marker` (📝, Ordnerübersicht); die reine `ICONS`-Prüfung erkennt
   sie nicht → offen, Abschnitt 13, **P1.3**.

---

## 4. Relevante Projektstruktur und Dateien

### Produktiv

| Pfad | Funktion | Status | Besonderheiten |
|---|---|---|---|
| `src/glide/app.pyw` | gesamte Anwendung | aktiv, 14.591 Z. | Monolith; `.pyw` ist per `importlib` **nicht** als Modul ladbar → `importlib.machinery.SourceFileLoader` nötig |
| `VERSION` | Versionsdatei | aktiv | muss mit `APP_VERSION` übereinstimmen; Test prüft das |
| `CHANGELOG.md` | Änderungsverlauf | aktiv | neueste Version oben; enthält 3.2.0 und 3.1.0 |
| `AGENTS.md` | Arbeitsregeln | verbindlich | Abschlusskriterium + Testisolierung |

### Tests (alle drei müssen grün sein)

| Pfad | Funktion | Status |
|---|---|---|
| `tests/integration/test_glide.py` | Hauptsuite, linear geschriebenes Skript (keine pytest-Struktur) | aktiv |
| `tests/integration/test_datenintegritaet.py` | Bestandswächter, Papierkorb, 130 Gruppen-Kombinationen, Ziehen, Mehrfachauswahl | aktiv |
| `tests/integration/audit_app.py` | app-weiter Durchlauf, meldet „Befunde" | aktiv |

Gemeinsamer Aufruf: `python tests/tools/pruefen.py --modus schnell`. Unter Linux ohne Display mit Xvfb; unter Windows und macOS mit einer funktionierenden Python/Tk-Installation. Siehe `tests/README.md`.

### Werkzeuge (kein Ja/Nein-Ergebnis, liefern Material)

| Pfad | Funktion | Status |
|---|---|---|
| `tests/tools/screenshots.py` | Sichtprüfung hell/dunkel, baut eigene kleine Demo-Ablage; braucht ImageMagick (`import`) | aktiv |
| `tests/tools/analyse_statisch.py` | AST-Analyse: ungenutzte Namen, Funktionslängen, Verschachtelung, wörtliche Dopplungen | aktiv, in 3.0.2 neu |
| `tests/tools/analyse_erreichbarkeit.py` | Erreichbarkeit ab Startpunkt, strukturgleiche Methoden, Attribut-Datenfluss | aktiv, in 3.0.2 neu |
| `tests/tools/beispieldaten.py` | erzeugt die Beispiel-Backupdatei; Inhalt steht dort im Quelltext | aktiv, in 3.2.0 neu |

### Fixtures

| Pfad | Funktion | Status |
|---|---|---|
| `tests/fixtures/current_v4…v10/` | Referenzbestände je Datenformat | aktiv, **nicht entfernen** |
| `tests/fixtures/legacy_v2/probelisten_5_listen_v2.json` | Altbestand Format 2 | aktiv |
| `tests/fixtures/beispiele/Glide_Beispieldaten.glidebackup` | ausführliche Beispieldaten zum Einlesen | aktiv, generiert, in 3.2.0 neu |

### Dokumentation

| Pfad | Status |
|---|---|
| `docs/01_PRODUCT_CONSTRAINTS.md` | aktuell, verbindlich |
| `docs/02_ARCHITECTURE.md` | **auf 3.2.0 aktualisiert** |
| `docs/08_CODE_BEFUND.md` | aktuell (Befund 3.0.2 + Ergebnis 3.1.0) |
| `docs/decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md` | aktuell |
| `docs/decisions/PRODUCT_IDENTITY.md` | aktuell: 3.2.0 / Schema 10; offene Inhaberentscheidungen |
| `docs/07_QA_BERICHT.md` | aktuelle Windows-Ausgangs- und Abschlussprüfung, historische Linux-Nachweise getrennt |
| `docs/10_RELEASE_CHECKLIST.md` | aktuell: Freigabegates für 3.2.0 |
| `docs/05_QA_TESTPLAN.md`, `docs/06_DATA_BACKUP_MIGRATION.md` | abgeglichen: Schema 10, Long-Task-Zeilen, aktuelle Normalisierung |
| `docs/exec-plans/*` | Referenz/Historie, bis 3.0.0 |
| `tests/tools/README.md` | vollständig; enthält auch `pruefen.py` und `releasedaten.py` |
| `tests/fixtures/README.md` | aktuell, enthält Abschnitt zu den Beispieldaten |

### Äußerer Workspace

`00_Arbeitsvorbereitung/`, `10_Dokumentation/`, `30_Release_Exports/` und
`40_Store_Material/` sind erreichbar und wurden geprüft. Aktive Unterlagen
einschließlich Word-Arbeitsgrundlage und `Produktdatenblatt_3.2.0.md` wurden
abgeglichen; alte Fassungen bleiben im dezentralen Archiv.

Neue Nachweise: `docs/11_BESTANDSANALYSE.md`, `tests/README.md` sowie ein
gemeinsames `glide_releaseplanung_3.2.0.glidebackup` für die drei Arbeitslisten.
Das Einlesen eines Komplettbackups ersetzt den ganzen Bestand; vor einem
manuellen Import eigene Daten vollständig sichern oder einen isolierten
Testdatenordner verwenden.

---

## 5. Funktionsumfang

- Listen mit verschachtelten Punkten; Ordner bis **5 Ebenen** tief
  (`MAX_FOLDER_DEPTH`), Ordner enthalten Listen *und* Ordner.
- **Vier Punktarten** (`kind`): `task`, `group`, `long` (Long-Task),
  `heading` (Zwischenüberschrift).
- Geschützter **Eingang** (`system_role: inbox`), abgeleitete Ansichten
  **„In Bearbeitung"** und **„Verspätet"**, **Papierkorb** (max. 200 Einträge).
- **Labels** an Punkten, Listen und Ordnern; zwei feste Systemlabels
  („Long-Task", „Überschrift") tragen die Art.
- Fälligkeit mit optionaler Uhrzeit, Wichtigkeit (0–3), Punktfarbe,
  Beschreibungstext, Anhänge als verwaltete lokale Kopie.
- Kalenderansicht (Wochen-/Monatsraster, rein lokal).
- Suche, Filter „Nur offene Punkte", Sortierung, Mehrfachauswahl,
  Drag & Drop in Baum und Seitenleiste, Umbenennen direkt in der Seitenleiste.
- Rückgängig (20 Schritte), Autosave, Backup-Rotation, Komplettbackup
  (Export/Import), TXT-/Markdown-/CSV-Export, TXT-Import.
- Hell-/Dunkelmodus, Zustand wird gespeichert.

---

## 6. Verbindliche Anforderungen des Nutzers

Alles hier ist **vom Nutzer festgelegt**, nicht vorgeschlagen.

### Grundsätzliches

- Keine Datenverluste. Höchste Priorität, mehrfach betont.
- Sauberer, effizienter Code ohne „Dummen-Code", Code-Reste und Dopplungen –
  ausdrücklich als Grundlage zum Weiterbauen.
- Kleine, nachvollziehbare Schritte statt großer Sprünge
  (*„ich möchte mehr kleinere Schritte haben"*).
- Iterativ arbeiten: Änderungswünsche sind gezielte Korrekturen; alles nicht
  Genannte bleibt erhalten.

### Aus dieser Sitzung, aktuell gültig

- **Nur Textzeichen als Symbole, keine Emoji.** Begründung des Nutzers:
  *„Ich versuche eine breite Unterstützung aufzubauen."* Anhangssymbol
  ausdrücklich **`⊕`**.
- **Keine Rückwärtskompatibilität für die Verzeichnis-Migration.**
  Wortlaut: *„Ich will keine ältere Sicherung öffnen, spare mir lieber die
  110 Zeilen."*
- **Beispieldaten** umfangreich und realitätsnah: Marketing-Vorlagen,
  Projektumsetzung, Design, Branding, Aufgaben, Notizen als Long-Tasks,
  Teil-Überschriften.
- **Dunkelmodus bleibt grau**, kein Dunkelblau (`#111113`, `#1C1C1E`, `#2C2C2E`).
- **Ordner-Klappdreiecke:** die nativen von Tk, keine selbstgezeichneten.
- **Auf-/Zuklappen eines Ordners darf nicht umbenennen.**
- Keine Symbole bei „Liste importieren" und „Neuer Ordner".

### Aus früheren Runden, weiterhin gültig

- Hellmodus: Dunkelblau `#15243C` statt Schwarz.
- Listenübersicht ganz oben in der Seitenleiste.
- Labels über ein Aufklappfeld mit Mehrfachauswahl, überall wo Labels wählbar sind.
- Fälligkeit über ein Kalendersymbol statt eingebettetem Monatskalender.
- Listen-Labels rechts unter der Erledigt-Anzeige, ohne Springen des Kopfbereichs.
- Jahr im Datum abgekürzt (`04.10.26`), aber vollständig sichtbar.
- Ein Label je Zeile plus „+n"; Labels als abgerundete Chips.
- Suchzeile über der Liste, nicht volle Breite.
- „Nur erledigte Punkte" entfernt; „Nur offene Punkte" weiter rechts.
- Systemlabel „Überschrift" nicht in der Listenansicht anzeigen.
- „Auswahl gruppieren" auf oberster Menüebene.
- Dialoge müssen auf dem Bildschirm erscheinen, auf dem das Fenster steht.
- „Erweiterte Eingabe" ausblenden, bevor sie zusammengequetscht wird.

---

## 7. UI-/UX- und Designvorgaben

### Farbwerte

| | Hell | Dunkel |
|---|---|---|
| Text/Grundton | `#15243C` | Grau-Stufen |
| Hintergrund | hell | `#111113` |
| Karte | | `#1C1C1E` |
| Eingabefeld | | `#2C2C2E` |

### Symboltabelle `ICONS` (Textzeichen; weitere Marker außerhalb der Tabelle sind noch offen)

```
inbox ↓ · in_progress ◐ · overdue ‼ · trash ×
theme_to_dark ☾ · theme_to_light ☀
labels ◈ · calendar ▦ · attachment ⊕
```

`DUE_COLUMN_ICON = ICONS["calendar"]`, `LABEL_COLUMN_ICON = ICONS["labels"]` –
beide verweisen auf die Tabelle, führen ihr Zeichen nicht selbst.
Der Test erzwingt: kein Zeichen in `ICONS` oberhalb von U+1F000.

**Begründung (relevant für künftige Entscheidungen):** Farbige Emoji kommen aus
einer Ersatzschrift des Systems, ignorieren die Textfarbe, sind auf Windows und
macOS verschieden breit und passen nicht zuverlässig in die feste Zeilenhöhe des
Treeview. Ein Textzeichen nimmt die Zeilenfarbe an – deshalb steht das
Fälligkeitssymbol bei überfälligen Punkten in Rot.

### Maßgebliche Konstanten

`MAX_UNDO_STEPS = 20` · `SIDEBAR_RENAME_DELAY_MS = 550` ·
`CONTENT_SECTION_GAP = 18` · `GROUP_DROP_EDGE_SHARE = 0.28` ·
`ENTRY_MIN_WIDTH = 300` · `INPUT_ROW_GAP = 10` ·
`SIDEBAR_TITLE_MAX_CHARS = 20` · `TREE_FONT = ("TkDefaultFont", 12)` ·
`LABEL_COLUMN_NAME_MAX_CHARS = 14` · `MAX_LABELS_PER_ITEM = 20` ·
`LabelChip.RADIUS = 9` · `SIDEBAR_TITLE_BASELINE_SHIFT = 3` ·
Fenstermindestgröße `860 × 700`.

**Wichtig:** Spaltenbreiten müssen gegen `TREE_FONT` gemessen werden, nicht
gegen die Standardschriftgröße – das war schon einmal ein Fehler
(Datumsspalte 151 statt 188 px).

---

## 8. Datenmodell / Geschäftslogik

- **Datenformat 10.** Keine Migrationszweige je Formatversion; beim Laden wird
  nur geprüft, ob die Version im gültigen Bereich liegt, und die
  `normalize_*`-Funktionen ergänzen fehlende Felder. Das ist der bewusst
  gewählte robuste Ansatz.
- **Punkt:** `id`, `text`, `done`, `importance` (0–3), `due` (ISO),
  `due_time`, `description`, `attachments`, `color`, `kind`, `labels`,
  `children`.
- **Punkttext ist einzeilig** – Ausnahme Long-Task: dort sind eigene
  Zeilenumbrüche erlaubt (`normalize_item_text`), höchstens
  `MAX_LONG_TASK_TEXT_LINES = 40` gespeichert, in der Liste bis zu fünf sichtbar.
- **Gruppe und Zwischenüberschrift** sind reine Gliederung: `done` bleibt false,
  `due` null, `importance` 0. Die Normalisierung erzwingt das bei jedem Laden.
- **Gruppen und Überschriften zählen nicht als Aufgaben.** Fortschritt,
  Seitenleistenzähler, „In Bearbeitung", „Verspätet" und Kalender werten nur
  `is_schedulable_item` aus.
- **Feste Labels:** `sync_item_kind_label` ist die einzige Stelle, die Art und
  Label angleicht. Label vergeben = Punkt umwandeln.
- **Papierkorb** hält vollständige Originale mit Herkunft; Anhänge gelöschter
  Listen zählen als referenziert und liegen in jedem Komplettbackup.
- **Fälligkeit:** drei Zustände (keine / nur Datum / Datum+Uhrzeit). Ohne `due`
  ist `due_time` immer null.

### Fallstricke, die im Code stehen und die man kennen muss

- **`sync_current_list_reference()`** schreibt `self.app_title` in den Titel der
  aktiven Liste zurück. Wer `active_list_id` von Hand umsetzt, ohne `app_title`
  mitzuziehen, **benennt beim nächsten `save_items()` eine Liste um.** Genau
  dieser Fehler ist beim Bau der Beispieldaten zweimal aufgetreten.
- **`current_list()`** zeigt beim ersten Start auf die mitgelieferte
  Standardliste, **nicht** auf den Eingang. Der Eingang wird über
  `is_inbox_list()` gesucht.
- `normalize_labels_data(data)` erwartet die **Liste**, nicht das ganze
  Datenobjekt. Der echte Import setzt `self.labels` über `normalize_lists_data`.
- `import_full_backup` setzt vor `set_active_list` bewusst
  `active_list_id = None`, damit `sync_current_list_reference` übersprungen wird.

---

## 9. Verbindliche Projektentscheidungen

1. **Monolith bleibt.** Keine Modulzerlegung von `app.pyw` zur Stabilisierung.
2. **Nur Standardbibliothek + Tk.** Neue Laufzeitabhängigkeit nur mit
   dokumentierter Entscheidung.
3. **Datenformat 10 bleibt**, solange keine Funktion es erzwingt.
4. **Drei Ordnungsmittel, keine Verschmelzung:** Zwischenüberschrift (Zäsur),
   Gruppe (Punkte einer Liste), Ordner (ganze Listen). Begründung vollständig in
   `docs/decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md`.
5. **Fixtures und Formatprüfung bleiben.** Sie kosten nichts am Programm und
   sichern, dass ältere Backups lesbar sind. Nur die *Verzeichnis*-Migration
   wurde entfernt.
6. **Testisolierung ausschließlich über `GLIDE_DATA_DIR`.** `%APPDATA%` allein
   wirkt nur unter Windows und träfe sonst echte Nutzerdaten.
7. **Jede Änderung läuft durch `item_change`/`sidebar_change`**, jede
   Umbauaktion zusätzlich durch `guarded_structural_change`. Zielregel; die
   offenen Ist-Abweichungen stehen in Abschnitt 13, **P1.4**.
8. **Jeder modale Dialog läuft über `run_modal`.**
9. **Alle Symbole aus `ICONS`, nur Textzeichen.** Zielregel; drei Symbolarten
   weichen im Ist-Code noch ab, Abschnitt 13, **P1.3**.
10. **Deutsch, einsprachig.** Auch Kommentare und Dokumentation.
11. **Abschlusskriterium:** Syntaxprüfung + alle passenden Tests grün +
    konsistente Versionsangaben + ausdrücklich benannte manuelle Restprüfungen.

---

## 10. Bekannte Fehler und technische Risiken

### RISIKO – App friert zeitweise ein

- **Symptom:** *„Die App hängt sich irgendwie bei dieser Version jetzt auf
  teilweise"* (gemeldet zu 3.0.1).
- **Bereich:** modale Dialoge, Tk-Griff (`grab`).
- **Gefundene Ursache:** `grab_set` + `wait_window` standen an sieben Stellen
  einzeln; nur eine gab den Griff an das aufrufende Fenster zurück. Aus einer
  Maske heraus geöffnete Unterdialoge (Farbauswahl, Namensabfrage,
  Listenauswahl) hinterließen eine sichtbare, aber nicht mehr bedienbare Maske.
- **Maßnahmen:** `run_modal` als einziger Weg; `modal_over` ermittelt den
  Griffhalter über `grab_current()`; zwei ältere Grab-Fehler bereits in 3.0.2
  behoben (`_close_popup(restore_grab=False)` im Destroy-Pfad, `modal_over` für
  Unterdialoge). Regressionstest vorhanden.
- **Status:** **NICHT VERIFIZIERT.** Der Fehler ließ sich nie reproduzieren.
  Die Aussage stützt sich auf den Mechanismus, nicht auf eine Reproduktion.
- **Nächster Test:** längere Benutzung auf Windows durch den Nutzer, gezielt mit
  verschachtelten Dialogen.

### BELEGT, NICHT BEHOBEN – Systemlabel überschreitet `MAX_LABELS_PER_ITEM`

- **Symptom:** Ein Punkt mit 20 Labels hat nach dem Wechsel auf Long-Task 21.
- **Ursache:** `sync_item_kind_label` (≈9201–9226) hängt das Systemlabel ohne
  Größenprüfung an; aufgerufen aus `set_item_kind` (≈9178–9198).
- **Beleg:** im isolierten Modul reproduziert (20 → 21) und zusätzlich über den
  produktiven Weg `convert_selected_kind(ITEM_KIND_LONG)`: 21 Labels im Punkt und
  21 Labels tatsächlich gespeichert. Fundstellen in `docs/11_BESTANDSANALYSE.md`.
- **Status:** offen. Eine Korrektur darf bestehende Labels nicht abschneiden;
  zuerst ist die fachliche Grenze für Systemlabels festzulegen. → Abschnitt 13,
  **P1.1**

### BELEGT, NICHT BEHOBEN – Einrücken kann `MAX_ITEM_DEPTH` überschreiten

- **Symptom:** Ein gültiger Punktbaum wird durch Verschieben so tief, dass
  `normalize_items` ihn beim nächsten Laden ablehnt.
- **Ursache:** `make_subitem` (≈12811–12846) prüft Selbst- und Nachfahrenbezug,
  aber nicht `MAX_ITEM_DEPTH = 100`; ohne Tiefenprüfung ebenso `add_child_item`
  (≈11803–11826) und der TXT-Baumaufbau (≈14325–14332).
- **Beleg:** Kette bis Tiefe 98 plus Unterbaum bis Tiefe 2; das Verschieben
  liefert `True`, die entstandene Tiefe 101 wird anschließend von
  `normalize_items` abgelehnt. Reproduktion nur im Arbeitsspeicher, kein
  Nutzerbestand betroffen.
- **Status:** offen und bei extremer Verschachtelung datenkritisch. Nötig ist
  eine gemeinsame Prüfung vor allen tiefenerhöhenden Änderungen; der
  Ende-zu-Ende-Fall über die Oberfläche ist **NOCH ZU TESTEN**. → Abschnitt 13,
  **P1.1**

### BEHOBEN – wirkungslose Aktion kostete den ältesten Rückgängig-Schritt

- **Symptom:** Bei vollem Rückgängig-Speicher (20) verlor der Nutzer den
  ältesten Schritt, auch wenn die Aktion nichts bewirkte.
- **Ursache:** `snapshot_undo` kürzte schon beim Anlegen.
- **Maßnahme:** `snapshot_undo(trim=False)` in beiden Rahmen +
  `trim_undo_stack()` erst nach bestätigter Wirkung. Test vorhanden.
- **Status:** behoben in 3.1.0, durch Test abgedeckt.

### BEHOBEN (frühere Runde) – Datenverlust beim Auflösen einer Gruppe

- Ein Punkt aus der Mitte verschwand, nicht im Papierkorb.
- Abgesichert durch `guarded_structural_change` + 130 geprüfte Kombinationen im
  Datenintegritätstest. Siehe `docs/07_QA_BERICHT.md` Abschnitt 3.
- **Diesen Bereich mit besonderer Vorsicht behandeln.**

### RISIKO – `insert_tree_items`, neun Verschachtelungsebenen

- 146 Zeilen, tiefste Verschachtelung im Bestand, „der wahrscheinlichste Ort für
  einen Fehler, den niemand beim Lesen findet". Nicht angefasst.

### RISIKO – Test grün, Oberfläche kaputt

- Präzedenzfall: Symbole verschwanden nach Fensterbreiten-Änderung, weil
  `refresh_sidebar_row_texts` die Texte ohne Symbole neu baute. Der Test war
  grün, nur die Sichtprüfung fand es. Behoben über die gemeinsame Methode
  `sidebar_display_title`.
- **Konsequenz: Nach Layoutänderungen immer `screenshots.py` laufen lassen.**

### Bekannte Grenzen (kein Fehler, nicht behebbar ohne Umbau)

- **Labels als Chips in der Aufgabenliste:** technisch unmöglich mit
  `ttk.Treeview` (keine Widgets/Bilder in Wertspalten, keine Zelleneinfärbung,
  feste Zeilenhöhe). Dokumentiert, offen.
- **Menü-Rahmen unter Windows:** Fensterrahmen des Betriebssystems, Tk gibt ihn
  nicht frei. Nicht behebbar ohne kompletten Menü-Umbau.
- **`winfo_screenwidth()`** meldet unter Windows nur den Hauptmonitor – Ursache
  für Dialoge auf dem falschen Bildschirm; in `_center_dialog` durch Ausweitung
  auf die Elternfenster-Geometrie umgangen.

---

## 11. Bereits erledigt / nicht erneut bearbeiten

### Version 3.1.0 – Aufräumversion

- Gemeinsamer Änderungsrahmen `item_change` / `sidebar_change` / `ChangeRecord`
  eingeführt; 31 von 39 `undo_stack.pop()`-Stellen ersetzt.
- `selected_items_for_change` ersetzt sechs Kopien des Auswahl-Vorfilters.
- `run_modal` + `modal_over` mit `grab_current()`.
- `on_sidebar_drag_end` in `drop_sidebar_list` / `drop_sidebar_folder` geteilt.
- `lift_item_to_parent_level` als gemeinsamer Kern von `outdent_selected` und
  `toggle_indent_selected`.
- Zusammengeführt: `sidebar_row_font`/`task_row_font` → `cached_font`;
  `_make_calendar_surface` → `_make_field(inner=…)`;
  `iter_all_list_objects`/`iter_all_folder_objects` → `iter_live_and_trashed`.
- Entfernt: `self.calendar_button_label` (gesetzt, nie gelesen); veralteter
  Kommentar über selbstgezeichnete Klappdreiecke.
- `MAX_UNDO_STEPS` als Konstante statt der Zahl 20.
- Undo-Kürzungsfehler behoben (siehe Abschnitt 10).

### Version 3.2.0 – Altlasten und Symbole

- Entfernt: `migrate_from_legacy_app_dirs`, `migrate_legacy_file`,
  `_legacy_app_data_dir`, `LEGACY_APP_NAMES`, `LEGACY_BASE_DIR`,
  `LEGACY_LABEL_COLOR_MAP` (64 Zeilen). `resolve_label_color` fällt jetzt auf
  `DEFAULT_LABEL_COLOR` zurück.
- Zentrale Anhangs- und Fälligkeitssymbole durch Textzeichen ersetzt: `⊕` für Anhänge (3 Stellen), `▦` für
  Fälligkeit (Spalte + Kalenderknopf). Test erzwingt das dauerhaft.
- `tests/tools/beispieldaten.py` + `Glide_Beispieldaten.glidebackup` neu:
  5 Ordner (2 verschachtelt), 10 Listen, 140 Punkte, davon 10 Gruppen,
  13 Long-Tasks, 25 Zwischenüberschriften, 9 Labels über alle sieben
  Palettenfarben, 3 Papierkorbeinträge. Inhaltlich Exposé-Produktion,
  Website/Redaktionsplan, Frühjahrskampagne, Vermarktungsstart,
  Baustellenkommunikation, CD-Regelwerk, Druckdaten-Checkliste, Textbausteine.
  Fristen relativ zum Erzeugungstag.
- `docs/02_ARCHITECTURE.md` und `tests/fixtures/README.md` aktualisiert.

### Code-Überprüfung, Etappen 1–4 abgeschlossen

- **Etappe 1:** zwei Analysewerkzeuge gebaut, iterativ von Falsch-Positiven
  befreit, `docs/08_CODE_BEFUND.md` geschrieben.
- **Etappe 2:** gemeinsamer Rahmen (siehe 3.1.0).
- **Etappe 3:** kleine Reste entfernt, drei strukturgleiche Methodenpaare
  zusammengeführt. Ergebnis: 0 nie genannte Namen, 0 strukturgleiche Paare.
- **Etappe 4:** alle 20 breiten `except Exception` durchgegangen. Ergebnis:
  19 sind an ihrer Stelle richtig (Migration, Einstellungen, Fenstergeometrie,
  Win32, Autosave-Takt, Export/Import-Meldungen). Der Aufhänger saß im Tk-Griff.
  **Diese Analyse nicht wiederholen.**

### Bestandsanalyse vom 04.09.2026

- Aktive Dokumentation, Startkontext, QA-Bericht, Release-Checkliste und
  Produktidentitätsregister auf 3.2.0 abgeglichen; Vorgängerfassungen liegen in
  `docs/archiv/` und `docs/decisions/archiv/`.
- Prüf- und Erzeugungswerkzeuge dokumentiert: gemeinsamer Prüfaufruf
  `tests/tools/pruefen.py`, beschrieben in `tests/README.md` und
  `tests/tools/README.md`.
- Äußere Arbeitsvorbereitung, Word-Arbeitsgrundlage und Produktdatenblatt auf
  3.2.0 fortgeschrieben.
- Belege und Fundstellen: `docs/11_BESTANDSANALYSE.md`, Kurzfassung in
  `docs/12_ABSCHLUSSBERICHT.md`. Der Auftragstext
  `docs/09_ARBEITSAUFTRAG_BESTANDSANALYSE.md` ist als abgeschlossen markiert
  und **nicht erneut auszuführen**.

### Früher in dieser Sitzung erledigt (2.12.0 / 3.0.0 / 3.0.1 / 3.0.2)

Label-Aufklappfeld mit Mehrfachauswahl, Fälligkeit auf Kalendersymbol reduziert,
Listen-Labels ohne Kopfsprung, Dunkelblau im Hellmodus, Listenübersicht nach
oben, Symboltabelle, Umbenennen in der Seitenleiste, Bildlaufleiste nur bei
Bedarf, Dropdown-Rahmen, Mehrmonitor-Fix für Dialoge, Punkt per Zug in eine
Gruppe legen, Labels in der Eingabemaske anlegen, `docs/decisions/
GRUPPE_ORDNER_UEBERSCHRIFT.md`.

---

## 12. Umsetzung wahrscheinlich, aber nicht verifiziert

- **Ein plausibler Einfrier-Mechanismus wurde adressiert** – der Mechanismus ist belegt, der Fehler
  wurde nie reproduziert. Erst die Benutzung auf Windows zeigt es.
- **Manuelles Verhalten auf Windows und macOS insgesamt.** In dieser Runde
  liefen alle drei automatisierten Suiten auf Windows; die vollständige manuelle
  Matrix und macOS sind weiterhin offen. Textzeichen-Symbole, Schriftmessung, Dialogpositionierung,
  Strg-/Cmd-Klick: **NOCH ZU TESTEN** auf echten Geräten.
- **Die neuen Textzeichen `⊕` und `▦` in echten Windows-/macOS-Schriften.**
  Unter Xvfb sehen sie korrekt aus; die Darstellung auf den Zielplattformen ist
  **NICHT VERIFIZIERT**.
- **Beispieldaten in der echten App eingelesen.** Der Importweg wurde
  programmatisch nachgebildet und geprüft, ein Import über das Menü durch den
  Nutzer hat **noch nicht** stattgefunden.

---

## 13. Offene Aufgaben

### P0 – Kritisch

Keine offenen P0-Punkte bekannt. Der gemeldete Einfrier-Fehler wurde durch eine
plausible Grab-Korrektur adressiert, seine Behebung ist aber unbestätigt →
siehe **P1.2**. Die belegte Tiefenlücke (**P1.1**) ist datenkritisch, greift
aber nur bei extremer Verschachtelung; sie steht deshalb an der Spitze von P1
und nicht in P0.

### P1 – Release-relevant

1. **Punkttiefe und Systemlabel-Grenze absichern.** Beide Fehler sind belegt
   reproduziert und in Abschnitt 10 beschrieben.
   Bereich: `make_subitem`, `add_child_item`, TXT-Baumaufbau,
   `sync_item_kind_label` / `set_item_kind`.
   Nächste Aktion: eine gemeinsame Tiefenprüfung vor allen tiefenerhöhenden
   Änderungen; fachliche Grenze für Systemlabels festlegen, ohne bestehende
   Labels abzuschneiden; anschließend alle Artwechsel- und Importwege
   gegenprüfen und den Ende-zu-Ende-Fall über die Oberfläche testen.
   **Vor dem Release zwingend** – ein grüner Testlauf deckt beide Randfälle
   derzeit nicht ab.
2. **Manuelle Prüfung auf Windows und macOS.**
   Bereich: gesamte Oberfläche. Abhängigkeit: echte Geräte.
   Vorarbeit: `docs/05_QA_TESTPLAN.md`, Release-Checkliste.
   Nächste Aktion: Matrix abarbeiten und dokumentieren; besonders Strg+Klick
   (Windows) / Cmd+Klick (macOS), Dialogpositionierung auf mehreren Monitoren,
   Darstellung der `ICONS`-Textzeichen, das gemeldete Einfrieren.
3. **Verbliebene Emoji außerhalb `ICONS` ersetzen.** Die Regel „nur Textzeichen"
   ist im Ist-Code an drei Symbolarten nicht erfüllt: `GROUP_MARKER`
   (📁, ≈1401), `IMPORTANCE_MARKERS[3]` (🚩, ≈1435) sowie der
   Beschreibungsmarker 📝 in zwei Baumansichten (`description_suffix` ≈10388,
   ≈10762) und in der Ordnerübersicht (`note_marker` ≈10628). Die reine
   `ICONS`-Prüfung erkennt sie nicht.
   **Folge beachten:** `GROUP_MARKER` und die Wichtigkeitsmarker stehen auch im
   TXT-Export (≈13509, ≈13520) und in der TXT-Wiedererkennung beim Import
   (≈11616/11626, ≈14299/14309). Ein Austausch bricht den Rundlauf mit bereits
   exportierten Dateien, solange die alten Zeichen beim Lesen nicht weiter
   akzeptiert werden.
   Nächste Aktion: Ersatzzeichen vom Nutzer freigeben lassen (Gestaltung ist
   keine Agentenentscheidung), Lesepfad abwärtskompatibel halten,
   Symbolprüfung im Test auf alle drei Arten ausweiten.
4. **Umbauaktionen ohne Bestandswächter – offene Architekturabweichung.**
   `indent_selected` (≈12905), `outdent_selected` (≈12922) und
   `toggle_indent_selected` (≈12879) laufen nur im `item_change`-Rahmen, ohne
   `guarded_structural_change`; `add_child_item` (≈11803) und
   `apply_sidebar_rename` (≈5532) nutzen weiterhin eigene Snapshot- und
   Speicherfolgen. Die verbindliche Zielregel (Abschnitt 9.7) ist damit nicht
   lückenlos umgesetzt.
   Nächste Aktion: Wächter nachziehen, Reihenfolge
   `item_change` ⊂ `guarded_structural_change` einhalten, Verhalten exakt
   erhalten. Betrifft dieselben Einrückwege wie P1.1 – zusammen planen.
5. **Produktidentität festlegen** (Publisher, Copyright, Support-E-Mail,
   Website, Datenschutz-URL, Lizenzmodell, Preis, Windows-Zielarchitektur,
   macOS Bundle Identifier, AppUserModelID, Inno-Setup-AppId, Markenprüfung
   „Glide"). **Entscheidung des Inhabers, nicht des Agenten.**
6. **Build-Kette aufbauen:** PyInstaller-OneDir, Windows-Installer,
   macOS-App/DMG, Signing, Notarisierung, SHA-256-Manifest.
   Status: nichts davon existiert.
7. **Migration, Backup und Restore mit Kopien echter Testdaten prüfen.**

### P2 – Funktionale Erweiterungen

8. **Drag & Drop für Anhänge** – braucht eine externe Bibliothek (gegen
   Projektregel) oder einen Win32-Eingriff. Dem Nutzer vorgelegt,
   **Entscheidung steht aus.** Nicht ohne Freigabe bauen.
9. **Labels als Chips in der Aufgabenliste** – mit `ttk.Treeview` unmöglich.
   Nur mit Ersatz des Treeview durch eine eigene Zeichenfläche; großer Eingriff.

### P3 – Optimierung / Nice-to-have

10. **Etappe 5 der Code-Überprüfung:** die zehn größten Funktionen aufteilen
    (`create_ui` 465 Z., `item_form_dialog` 432, `open_calendar_view` 348,
    `apply_theme` 225, `validate_backup_schema` 223, `open_label_manager` 186,
    `import_full_backup` 171, `create_list_sidebar` 166, `__init__` 157,
    `insert_tree_items` 146). Erster Kandidat: `insert_tree_items` wegen der
    neun Ebenen. Vom Nutzer nie beauftragt, als „nur wenn Budget bleibt"
    eingestuft.
11. **`audit_app.py` Phase 11** – aus der Vorgeschichte als „verloren"
    vermerkt. **STATUS UNKLAR:** Die Datei enthält nummerierte Abschnitte 1–10; eine frühere elfte Phase ist unbelegt.
    Vor Arbeit daran erst klären, was gemeint war.

---

## 14. Verworfene oder ersetzte Ansätze

**Nicht erneut vorschlagen.**

| Ansatz | Grund |
|---|---|
| Dunkelblau `#15243C` im Dunkelmodus | Nutzer: nur im Hellmodus sinnvoll, Dunkelmodus bleibt grau |
| Selbstgezeichnete Ordner-Klappdreiecke | Nutzer: „die neuen Ordner Icons verändern sich nicht" → Tk zeichnet wieder selbst |
| Symbole bei „Liste importieren" / „Neuer Ordner" | Nutzer: entfernen |
| Umbenennen beim Klick aufs Klappdreieck | Nutzer: „Wenn ich einen Ordner auf und zumachen will, will ich ihn nicht umbenennen" |
| Emoji als Symbole (`📅`, `📎`) | ERSETZT durch Textzeichen `▦`, `⊕` |
| `LEGACY_LABEL_COLOR_MAP`, Verzeichnis-Migration | ENTFERNT auf ausdrücklichen Wunsch |
| Fixtures und Formatprüfung entfernen | Geprüft und **abgelehnt**: spart nichts am Programm, nimmt der Prüfung die Grundlage |
| Import-/Backup-Wege in den `item_change`-Rahmen zwingen | Bewusst nicht: eigene Rücknahme (Labelbestand), eigener Abbruchpfad, datenkritischster Teil |
| Breite `except Exception` pauschal verengen | Geprüft: 19 von 20 sind richtig |
| `ADVANCED_BUTTON_MIN_WIDTH = 520` als wirksame Grenze | ERSETZT durch `advanced_button_min_width()`, das aus echten Knopfbreiten rechnet; die Konstante ist nur noch Untergrenze |
| `ChangeRecord.select()` | Sofort wieder entfernt, weil nie benutzt |

---

## 15. Ungeklärte Fragen

1. **Ist das Einfrieren wirklich weg?** Nur der Nutzer kann das auf Windows
   bestätigen. → `NOCH ZU TESTEN`
2. **Drag & Drop für Anhänge:** externe Bibliothek zulassen oder Win32-Eingriff
   oder verwerfen? → Entscheidung des Nutzers offen.
3. **Was war „Phase 11" in `audit_app.py`?** → `STATUS UNKLAR`
4. **Externe Ordner:** geprüft; aktive Unterlagen auf 3.2.0 abgeglichen.
   Fertige signierte Release-Pakete fehlen weiterhin.
5. Alle Produktidentitäts-Felder (Publisher, Lizenz, Preis, URLs) → offen,
   Inhaberentscheidung.

---

## 16. Wichtige Abhängigkeiten und Zusammenhänge

- **Version an drei Stellen konsistent halten:** `VERSION`,
  `APP_VERSION` in `app.pyw`, Prüfung in `test_glide.py`. Der Test schlägt sonst
  fehl.
- **`beispieldaten.py` → `Glide_Beispieldaten.glidebackup` → `test_glide.py`.**
  Ändert sich das Werkzeug, muss die Datei neu erzeugt werden; der Test prüft
  Umfang, Artenverteilung, Labelverweise und Palettenabdeckung.
- **`ICONS` → `DUE_COLUMN_ICON`/`LABEL_COLUMN_ICON` → Spaltenbreitenberechnung
  (`task_tree_column_widths`).** Ein längeres Symbol verändert die Spaltenbreite.
- **`item_change` ⊂ `guarded_structural_change`.** Reihenfolge nie umdrehen.
- **`.pyw` laden:** immer `importlib.machinery.SourceFileLoader`, nie
  `spec_from_file_location`.
- **Linux ohne Display braucht `xvfb-run`.** Das bisherige Linux-Screenshotwerkzeug
  braucht ImageMagick (`import`); Windows-/macOS-Suiten brauchen kein Xvfb.
- **`GLIDE_DATA_DIR` muss vor dem Import gesetzt sein**, nicht danach.

---

## 17. Arbeitsregeln für den nächsten Agenten

Abgeleitet aus dem tatsächlichen Verlauf:

1. **Kein Datenverlust, unter keinen Umständen.** Der Bereich um Gruppen,
   Papierkorb und Undo wurde nach einem echten Datenverlust abgesichert – dort
   besonders vorsichtig arbeiten.
2. **Nach jeder Änderung alle drei Testsuiten laufen lassen**, nicht nur eine.
3. **Nach Layoutänderungen zusätzlich `screenshots.py`.** Ein grüner Test hat
   schon einmal eine kaputte Oberfläche verdeckt.
4. **Keine bestehende Funktion entfernen, die nicht ausdrücklich zur Entfernung
   freigegeben wurde.** Vor dem Löschen prüfen, ob ein Analysewerkzeug nur ein
   Falsch-Positiv meldet – das ist mehrfach vorgekommen
   (`LabelChip.set_colors`, `format_file_size`, `_store_pending_attachments`,
   `refresh_scrollbar_state` sind **nicht** tot).
5. **Verhalten bei Refactorings exakt erhalten.** Wo eine Vereinheitlichung das
   Verhalten ändern würde, das alte Verhalten beibehalten und den Grund
   kommentieren.
6. **In kleinen, einzeln prüfbaren Schritten arbeiten.**
7. **Ehrlich über den Status berichten.** Was nicht reproduziert wurde, wird
   nicht als „behoben" verkauft. Der Nutzer hat auf diese Unterscheidung
   ausdrücklich Wert gelegt.
8. **Nicht eigenmächtig gestalten.** Symbole, Farben und Layout sind
   Nutzerentscheidungen; Abweichungen vorlegen statt umsetzen.
9. **Kommentare erklären das Warum**, nicht das Was – so ist der Bestand
   geschrieben, dieser Stil wird fortgeführt.
10. **Alles auf Deutsch:** Code-Kommentare, Dokumentation, Antworten.
11. **Bei unklarem Umsetzungsstatus zuerst die Projektdateien prüfen**, nicht
    aus dem Gedächtnis arbeiten.
12. **`CHANGELOG.md` und die betroffene Dokumentation mitführen** – das ist
    Bestandteil des Abschlusskriteriums in `AGENTS.md`.

---

## 18. Empfohlener nächster Arbeitsschritt

Zuerst die beiden belegten Grenzwertfehler bei Punkttiefe und Systemlabel-Limit
absichern (**P1.1**) – sie sind datenkritisch und von keinem Testlauf gedeckt;
die Einrückwege dabei zusammen mit **P1.4** betrachten, weil dieselben Stellen
betroffen sind. Parallel die drei Release-Arbeitslisten aus
`glide_releaseplanung_3.2.0.glidebackup` in einem isolierten Testdatenordner
ansehen und die Windows-Matrix mit längerer Dialogbenutzung abarbeiten
(**P1.2**). Produktidentität und Vertriebsweg (**P1.5**, **P1.6**) sind
Inhaberentscheidungen und halten die Build-Kette auf.

Die Dokumentationskonsolidierung ist erledigt. Der nächste Bearbeiter findet
Inventur, Fundstellen, Maßnahmen und offene Punkte in `docs/11_BESTANDSANALYSE.md`.
