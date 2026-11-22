# Glide Shell Framework – Architektur- und Entkopplungskonzept

Stand 22.11.2026 · Glide 1.0.1 · Aufgabenformat 26

Dieses Konzeptdokument beschreibt das Zielbild für die Entkopplung des wiederverwendbaren Desktop-Fundaments (**Glide Shell Framework**) von Glides Fachmodulen. Ein unabhängig nutzbares Shell-Paket und die unten skizzierten Schnittstellen sind noch nicht abgenommen. Die Umsetzung erfolgt nur im jeweils beauftragten Umfang.

**Zuständigkeiten:** Der tatsächliche Architekturzustand steht in der [Architektur](02_ARCHITECTURE.md), vorhandene Module, Tests, Kopplungen und Übernahmeverträge im [Glide-System](../src/glide/README.md). Auftrag, Priorität und Umsetzungsrest von WA-49/50 stehen ausschließlich in der [Roadmap](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md); Prüfungen und Abnahme im [QA-Bericht](07_QA_BERICHT.md). Änderungen werden nach der [Pflegematrix](DOKUMENTENPFLEGE.md#zuständigkeiten-und-änderungsbezüge) abgeglichen.

---

## 1. Ausgangslage und Zielsetzung

Historisch wuchs Glide als Desktop-Anwendung rund um die Klasse `ListApp` in [`app.pyw`](../src/glide/app.pyw). Trotz ausgelagerter Fachmodule verbleiben dort Überschneidungen zwischen:
- generischer Desktop-Infrastruktur (Fensterverwaltung, Dialog-Modale, Theme-Token, Event-Loop, Menüleisten),
- anwendungsspezifischer Steuerung (Listen, Aufgaben, Canvas, Kalender, Notizen).

**Ziel des Glide Shell Frameworks:**
Ein sauberes, modulares Schichtenmodell, bei dem das Fundament als eigenständige Desktop-Shell agieren kann, ohne Wissen über Aufgabenformate, Fälligkeiten oder Todo-Metadaten zu besitzen.

```
+-------------------------------------------------------+
|             Glide Applikation (Domäne)               |
|   Aufgaben, Notizen, Eisenhower, Kalender, Canvas     |
+-------------------------------------------------------+
                           |
            (nutzt Ports / Interfaces)
                           v
+-------------------------------------------------------+
|             Glide Shell Framework (Fundament)         |
|  Lifecycle, Fenster, Appearance, Widgets, Aktionen    |
+-------------------------------------------------------+
                           |
            (steuert UI & Plattform)
                           v
+-------------------------------------------------------+
|       Tkinter / Tcl 9 / OS (macOS, Windows, Linux)    |
+-------------------------------------------------------+
```

---

## 2. Klare Modulgrenzen und Verantwortlichkeiten

### 2.1 Wiederverwendbare Desktop-Shell (Plattform- & UI-Fundament)

Die folgende Tabelle beschreibt Zielverantwortungen. Dateibestand, Featurezuordnung, Testdateien und Wiederverwendungseignung werden ausschließlich im Systemregister gepflegt.

| Zielbereich | Entkopplungsvertrag | Vorhandene Grundlage und Grenze |
|---|---|---|
| Laufzeit und Lebenszyklus | Pfade ohne Tk oder Dateisystemmutation ermitteln; Start, Ende, Session und Schreibbesitz ausdrücklich koordinieren | [Start/Architektur](../src/glide/README.md#startarchitektur). `runtime_config.py` löst Pfade auf; CLI-Auswertung, App-Import und Desktop-Initialisierung bleiben eigene Schritte (WA-49). Eine `shell_lifecycle.py` wäre ein neuer Entwurf. |
| Design, Typografie und Symbole | Theme-Token, Schrift-/Glyphenwahl und Maßberechnung über eine stabile UI-Schnittstelle bereitstellen | [Design/Branding](../src/glide/README.md#designbranding) und [Designvertrag](DESIGN_RICHTLINIEN.md). Vorhandene Module bilden noch kein unabhängig geprüftes UI-Paket. |
| Fenster, Navigation und modale Dialoge | Root-/Toplevel-Lebensdauer, Fokus, Grab-Freigabe, Bildschirmgrenzen und Menübesitz koordinieren | [UI/Navigation](../src/glide/README.md#uinavigation) und [Tk-Regeln](02_ARCHITECTURE.md#5-tk-fallstricke-teuer-gelernt). Der modale Warteweg liegt seit 3.62.0 in `modal_session.py`, `ListApp.run_modal` ist Fassade; ein `window_manager.py` für Fensterlebensdauer und Abbau ist weiter nur ein vorgeschlagener Schnitt. |
| Steuerelemente und Zugänglichkeit | Theme, Tastaturbedienung und semantische Rollen erhalten; benötigte `keys`-/`cget`-/`configure`-/Indexzugriffe kompatibel halten | [Oberflächenbestand](../src/glide/README.md#oberflächen-bestandsprüfung) und [Barrierefreiheit](../src/glide/README.md#barrierefreiheit). Die D78-Controls liegen in `app.pyw`; ein eigenes `controls/`-Paket ist kein Istzustand. |
| Undo und Commands | Transaktionsgrenzen der App über einen expliziten Vertrag anbinden, ohne Aufgabenformate in die Shell einzubauen | [Daten/Schutz](../src/glide/README.md#datenschutz). `undo_history.py` enthält `RedoHistory` für Wiederholen; der Undo-Gesamtablauf liegt weiterhin in der App. Ein generischer Command-Stack ist Zielarbeit. Validierung 13.11.2026: Der Ablauf hängt an Aufgabenmodellen, Einstellungen und Speicherweg und bleibt beim Host; die Shell bindet Verfügbarkeit und Auslösen als Aktionen an. |

---

### 2.2 Glide-Fachinhalt (Spezifische Anwendungsdomäne)

Aufgabenformate, Listen, Fälligkeiten, Kapazitätsplanung, Kalenderregeln, Seiten und inhaltliche Import-/Exportabbildungen bleiben außerhalb der Shell. Die Zuordnung steht im [Modulregister](../src/glide/README.md#1-python-module), das gültige Verhalten in den [Funktionen](20_FUNKTIONEN.md) und im [Datenvertrag](06_DATA_BACKUP_MIGRATION.md).

Ein heute fachnahes Modul kann einen wiederverwendbaren Anteil enthalten. Beispielsweise sind Schreibbesitz und Sicherungen technische Fähigkeiten, deren aktuelle Glide-Kopplung vor einer Übernahme aufzulösen ist. Deshalb ganze Dateien nicht pauschal als ausschließlich fachlich oder bereits neutral einstufen; maßgeblich sind die [technischen Systemfähigkeiten](../src/glide/README.md#technische-systemfähigkeiten-für-folgeprojekte) und [Übernahmeverträge](../src/glide/README.md#9-grundlage-für-steps-und-weitere-projekte).

---

## 3. Bewertung der Zwei-Fenster- und Multi-Window-Architektur

### 3.1 Aktuelle Situation in Glide
Glide verwendet eine primäre Tk-`root`-Instanz für das Hauptfenster und `Toplevel`-Instanzen für Dialoge, Einstellungen, Meldungen und Hinweise. Nebenansicht und Aufgabeninspektor sind eingebettete Flächen im Hauptfenster (D55) und keine eigenen Fenster.

**Erkannte Herausforderungen:**
1. **macOS Event Loop & Menübindung:** Auf macOS gehört das Anwendungsmenü (`Apple Menu`) zwingend zur primären `root`-Instanz. Wenn ein Toplevel-Fenster schließt oder den Fokus wechselt, darf das Menü nicht in einen verwaisten Zustand fallen.
2. **Modal Grab Deadlocks:** Ein nicht freigegebener Tcl-Grab kann Eingaben an das Hauptfenster blockieren. Ausnahmesichere Freigabe und Fokuswiederherstellung bleiben Pflicht; konkrete Timeout-Ursachen benötigen ihren jeweiligen Laufnachweis.
3. **Multi-Monitor DPI-Scaling (Windows Per-Monitor V2):** Wenn Haupt- und Nebenfenster auf Monitoren mit unterschiedlichen Skalierungsfaktoren (z. B. 100% vs. 175%) liegen, müssen Schriften und Widgetabstände je Fensterinstanz isoliert berechnet werden können.

### 3.2 Architekturvorgabe für die Shell
Das Zielbild sieht einen zentralen `WindowManager` vor. Die folgenden Namen und Aufrufe sind Schnittstellenskizzen, keine vorhandene API:
- **Root-Transparenz:** Die Anwendung erstellt Fenster nicht direkt per `tk.Toplevel(self.root)`, sondern fordert Fenster über den `WindowManager` an:
  `window = shell.create_window(title="Tagesentlastung", kind=WindowKind.MODAL_DIALOG, parent=...)`
- **Ausnahmesicherer Modal-Runner:**
  Ein einheitlicher Context Manager klammert alle modalen Interaktionen:
  ```python
  with shell.modal_session(dialog_window):
      shell.wait_window(dialog_window)
  # Geforderter Vertrag: Grab freigeben, Fokus und Hooks aufräumen
  ```
- **Zwei-Fenster- und Pane-Orchestrierung:**
  Hauptfenster, Nebenansichten und geteilte Arbeitsbereiche sollen eine gemeinsame Lebensdauer-/Geometriekoordination erhalten. `compact_mode.py` ist eine bestehende Teilgrundlage; es kapselt nicht bereits die gesamte Fenster-, DPI- und Pane-Steuerung.

---

## 4. Empfohlene Migrationsreihenfolge (Schritt-für-Schritt)

Diese Reihenfolge beschreibt technische Abhängigkeiten, keine zweite Aufgaben- oder Statusliste. Beauftragter Umfang und Rest von WA-49/50 werden nur in der Roadmap geführt. Istbelege kommen aus Architektur/Systemregister; jede Umsetzung benötigt neue passende Prüfungen.

### Phase 1: Laufzeit- und Pfad-Entkopplung
- **Architekturschritt:** Auf der Tk-freien Pfadauflösung aufbauen und App-Import, CLI-Auswertung, Verzeichnisanlage und Tk-Initialisierung explizit trennen. Seiteneffektfreiheit für jeden Einstieg gesondert prüfen; Eigenschaften von `runtime_config.py` nicht auf den App-Import übertragen.

### Phase 2: Design- und Widget-Extraktion
- **Aufgabe:** Zusammenfassung von [`appearance.py`](../src/glide/appearance.py), [`ui_design.py`](../src/glide/ui_design.py) und den D78-Custom-Controls in ein Teilpaket `glide_shell.ui`. Lieferabgleich und Paketbau erfassen heute nur flache Module; bis zur Entscheidung über Namensraum und Paketgrenze bleibt die Shell-Zugehörigkeit eine Modulliste mit Importregel.
- **Ziel:** Einheitliche Widget-Schnittstelle (`keys()`, `configure()`, Event-Binding) unabhängig vom konkreten Glide-Inhalt.

### Phase 3: Modal- und Dialog-Manager
- **Aufgabe:** Formalisierung von `run_modal` aus `app.pyw` in ein isoliertes Modul. Erster Schritt umgesetzt in 3.62.0: `modal_session.py`, zunächst als flaches Modul; seit V1.64 (D95) im Paket als `glide_shell.modal_session`. Die Liste der Shell-Module führt `tests/unit/test_shell_importregel.py`.
- **Ziel:** Schutz vor Livelocks, standardisierte Bestätigungs-, Eingabe- und Auswahldialoge mit einheitlicher Tastaturbedienung (Escape zum Abbrechen, Enter zum Bestätigen).

### Phase 4: Undo/Command-Abstraktion
- **Aufgabe:** Entkopplung von [`undo_history.py`](../src/glide/undo_history.py) von den Datenstrukturen der Aufgabenliste.
- **Ziel:** Einen noch zu definierenden Undo-/Command-Vertrag für Memento- oder Command-Objekte schaffen; `execute()` und `undo()` wären vorgeschlagene Schnittstellen, keine heutige `UndoHistory`-API. Vor einer Verlagerung steht der Nachweis fachlicher Unabhängigkeit; bis dahin bleibt Undo beim Host.

### Phase 5: Trennung von Shell und App-Controller
- **Aufgabe:** Reduzierung von `ListApp` in `app.pyw` auf die reine Controller-Rolle für die Aufgabenverwaltung.
- **Ziel:** Die Shell initialisiert das Tk-Fenster, die Menüs und die globalen Shortcuts und bettet den `GlideAppController` als primären Inhalt ein.

---

## 5. Entkopplungsmuster: Ports & Adapters (Hexagonale Architektur)

Um die Shell unabhängig von Glide zu halten, kommuniziert die Anwendungsdomäne ausschließlich über definierte Schnittstellen (Ports):

```
                     +---------------------------+
                     |    Glide Domänenlogik     |
                     +---------------------------+
                                   |
                         (verwendet Ports)
                                   v
             +-------------------------------------------+
             |                Shell-Ports                |
             |-------------------------------------------|
             | + show_notification(title, message)       |
             | + open_dialog(dialog_descriptor) -> result|
             | + request_theme_change(theme_name)        |
             | + register_action(action_id, shortcut)    |
             | + record_undo(undo_operation)             |
             +-------------------------------------------+
                                   ^
                         (implementiert Ports)
                                   |
                     +---------------------------+
                     |     Glide Shell Tk-Core   |
                     |  (Tk-Fenster, Menüs, OS)  |
                     +---------------------------+
```

### Vorteile:
1. **Gezielte Prüfung ohne Tkinter:** Fachberechnungen über explizite Ports mit Unit-Tests prüfen; UI-, Host- und Plattformverhalten benötigt weiterhin Integrationstests.
2. **Wiederverwendung für Folgeprojekte:** Ein künftig entkoppeltes Fundament könnte eigene Domänen-Controller und Ansichten aufnehmen. Bis dahin gelten die bestehenden Übernahmeverträge und ihre Kopplungsgrenzen.
3. **Gebündelte Plattformverträge:** Menübesitz, DPI und Zwischenablage über definierte Adapter kapseln und auf jeder Plattform prüfen. Die bloße Modultrennung beweist keine Plattformfreigabe.

---

## 6. Validierte Grenzen (13.11.2026)

Die Architekturvalidierung auf `45ab307e` hat die Zielgrenzen an den tatsächlichen Aufrufern geprüft. Auftrag, Pakete und Status stehen in der [Roadmap](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2189-glide-3600-erste-shell-schnitte-start-baseline-und-beruhigter-einstellungsdialog-13112026); die Arbeitsübergabe im [Masterprompt](FABLE_GLIDE_SHELL_MIGRATION_PROMPT.md).

- **Abhängigkeitsrichtung:** Host/Glide → Shell → Tk/OS. Shell-Module importieren nur Standardbibliothek, `tkinter` und andere Shell-Module. Glide-Werte kommen als Argumente, Werte und Callbacks; ein Port entsteht nur, wo er eine konkrete Abhängigkeit entfernt.
- **Vorgehen:** Inkrementelle Extraktion mit vorhandenen Fassaden. `ListApp`-Methoden und die Pfadkonstanten des App-Moduls bleiben Aufrufstellen, weil Tests und Werkzeuge an ihnen hängen. Ein physisches Teilpaket berührt Lieferabgleich, Paketbau und Importwege und ist eine eigene Entscheidung.
- **Start:** Direktstart, Schnellstart und Paketstarter verhalten sich gegen leere, vorhandene, fremd gesperrte und beschädigte Ablage gleich; sie unterscheiden sich nur in der Überwachung durch den Begleitprozess. Der Bytecode-Ordner wird dreifach aufgelöst, weil jeder Einstieg ihn vor seinem ersten eigenen Import braucht; ein Test hält die drei Auflösungen gleich.
- **Modal:** `run_modal` ist der einzige Warteweg. Seit 3.62.0 wartet `modal_session.wait_modal`; Theme, Bildschirmanteil und Fehlerprotokoll reicht die `ListApp`-Fassade als Argumente hinein. Vor einer Verlagerung steht ein Vertragstest mit echtem Grab, Fokus, Abbruch und Besitzerabbau. Seit 14.11.2026 hält `test_modalvertrag.py` diesen Vertrag fest, seit 3.65.0 in 17 Fällen mit neun Gegenproben, seit V1.60 (R1) in 18 Fällen mit zehn Gegenproben. Seit 3.65.0 gibt die Shell den Fokus nach dem Schließen selbst zurück (D87): `remember_focus` fragt das aufrufende Fenster nach seinem letzten Fokus, `return_focus` setzt ihn zurück, fällt bei verschwundenem Widget auf das Fenster und lässt ein drittes Fenster unberührt. Die bisherigen Rückgaben einzelner Aufrufer (`restore_focus`) bleiben und wirken danach.
- **Abbau:** Beim Beenden verwirft Glide am `<Destroy>` der Wurzel alle Tcl-Zeitgeber und gibt die Datensperre ein zweites Mal frei; `test_abbauvertrag.py` hält das fest. Für den Abbau einer Ansicht ohne das Hauptfenster reicht das nicht: Vor dem Schließen sind `_save_recent_pages` (Zeitgeber, auch im Ruhezustand), dazu nach einem Designwechsel mit Hintergrundverlauf `abholen` (Zeitgeber des Hintergrundverlaufs), `abgleichen`, `collapse_emptied_frames`, `draw_icons` und `sync_backdrop_surfaces` (Leerlauf) nicht registriert. Eine Shell-Fensterlebensdauer muss diese Aufträge je Host oder Ansicht besitzen.
- **Fensterlebensdauer (seit 3.64.0):** `window_lifetime.AfterScope` besitzt die Zeitgeber eines Widgets und endet mit ihm. Das Hauptfenster hat einen Bereich (`ListApp.after_scope`), dessen Bestand `_after_ids` ist; die sieben oben genannten freien Zeitgeber laufen darüber, die der Baumansichten über den Bereich des eigenen Widgets. Seit R3/R4 (V1.62, D94) laufen alle 104 Zeitgeberaufrufe in `app.pyw` über einen Bereich: die der Wurzel über `ListApp.after_scope()` oder `_register_after`, die von Widgets und Dialogen über `window_lifetime.scope_for` des Widgets, auf das sie wirken. Alle Dialoge entstehen über `modal_session.create_dialog` (R1/R4); direkt erzeugt wird nur der Tooltip als randloses Popup. Die Sperrklinke in `test_shell_importregel.py` steht auf 1 direktem Fenster und 0 Zeitgebern ohne Bereich. Zu beachten: `cancel_pending_callbacks` bricht beim Beenden mit `cancel_all` jetzt auch die neu in den Wurzelbereich gelegten Rückrufe ab; das ist gewollt. Schließen bei offener modaler Rückfrage ist geprüft und endet sauber.

| Modul | Neutral | Glide-gebunden |
|---|---|---|
| `motion` (seit V1.66 in `glide_shell`) | vollständig; Importregel in `test_shell_importregel.py`, Verhalten in `tests/unit/test_motion.py` | – |
| `modal_session` (seit 3.62.0) | vollständig; Importregel in `test_shell_importregel.py` und `test_modal_session.py` | Attributnamen `_glide_modal_active`/`_glide_modal_finished` aus Kompatibilität |
| `window_lifetime` (seit 3.64.0) | vollständig; Importregel in `test_shell_importregel.py` | Attributname `_glide_after_scope` am Widget |
| `custom_controls` (seit 3.67.0) | vollständig; Importregel in `test_shell_importregel.py`, Verhalten in `test_custom_controls.py` | Klassennamen `GlideCheckbutton`, `GlideRadiobutton`, `GlideListbox`, `GlideScale` aus Kompatibilität; Schrift, Tinte und Hintergrund setzt der Host über `set_font_provider`, `set_ink_provider` und `set_backdrop_painter`; `app.pyw` re-exportiert die Bedienelemente |
| `desktop_adapter` (seit 3.68.0) | vollständig; Importregel in `test_shell_importregel.py`, Verhalten in `tests/unit/test_desktop_adapter.py` | Attributname `_glide_action_ids` an Menüs; Menüeinträge, Aktionskennungen und Beschriftungen liefert der Host |
| `compact_mode` | `parse`, `format_geometry`, `clamp`, `keep_visible` liegen seit V1.67 in `glide_shell.window_geometry` (D96) | Mindestmaße, Einstellungsname, Kürzelregel, Kompaktlage |
| `appearance` | Erkennung des Systemmodus und `resolve` liegen seit V1.67 in `glide_shell.system_appearance` (D96) | Designpaare (`pair_for`, `normalize_auto`), Hintergrundauswahl, `with_background` |
| `ui_design` | Kürzen, Breitenausgleich und ruhige Umbruchbreite liegen seit V1.69 in `glide_shell.text_fit` (S10, D98) | Skalen, Titelgrenze (`clip_title`), `task_title`, `today_columns`, `page_icon_layout` |
| `action_menu` | Eintragsmodell, Ordnen, Suchen und Gruppieren liegen seit V1.69 in `glide_shell.action_picker` (D98) | Sperrgründe, Platzhalter, Zustandstexte, Kopfverweise, Suchschlüssel aus `content_search` |
| `accessibility`, `accessibility_bindings`, `core_accessibility` | `Attributes`, `set_attributes`, `Binding`, allgemeine Binder | `task_value`, alle Binder mit `app` |
| `undo_history` | `RedoHistory` liegt seit V1.67 in `glide_shell.redo_history` (D96) | Board-Einträge, Rückgängig-Stapel in `ListApp` |
| `runtime_config` | Plattformordner, Umgebung, Zeiger und Reihenfolge liegen seit V1.69 in `glide_shell.runtime_paths` (D98) | Produktname, Datei- und Variablennamen, `RuntimePaths`, Meldungen |

### Locale-Vertrag für sichtbare Shell-Beschriftungen

Shell-Module erhalten bereits angezeigte Menütexte, Aktionen und Beschriftungen vom Host; sie laden keine Glide-Kataloge und wählen keine Produktsprache. `desktop_adapter` ergänzt dafür bei `primary_modifier`, `format_accelerator` und `format_redo_accelerator` den optionalen Parameter `modifier_labels` (`command`, `control`, `shift`). Glide reicht die aktiven DE/EN-Katalogwerte ein. Bestehende Aufrufer ohne diesen Parameter behalten ihre bisherigen Beschriftungen (`Cmd`, `Strg`, `Shift`). Dieser kleine Host→Shell-Vertrag führt weder einen eigenen Übersetzungsdienst noch eine neue Shell-Abstraktion ein. T319 und T326 sichern Imports, öffentliche Signaturen und den rückwärtskompatiblen Fallback; T329 prüft die beiden Katalogwerte.

---

## 7. Paket `glide_shell` und Übernahme in Folgeprojekte (D95, 20.11.2026)

Seit Glide-System V1.64 ist die Shell ein Unterpaket `src/glide/glide_shell` mit eigener Paketversion `SHELL_VERSION` (getrennt von App- und Systemversion; 0.1.0 mit V1.64, 0.2.0 seit V1.66 mit `motion`, 0.3.0 seit V1.67 mit den D96-Bausteinen, 0.4.0 seit V1.68 mit dem Selbsttest). Es enthält `modal_session` (Dialogfabrik `create_dialog`, modaler Warteweg, Fokusrückgabe), `window_lifetime` (`AfterScope`, `scope_for`), `custom_controls` (Canvas-Bedienelemente), `desktop_adapter` (Menüleiste, Tastaturkürzel, Betriebssystemaktionen), seit V1.66 `motion` (kurze, unterbrechbare Übergänge mit injizierter Zeitplanung, etwa über `AfterScope.after`/`cancel`) seit V1.67 `window_geometry` (Geometrietexte, Fenster auf der Arbeitsfläche halten), `system_appearance` (Hell/Dunkel des Systems deuten) und `redo_history` (Wiederholen-Stapel) sowie den Demonstrationshost `demo` (Paket 6) und seit V1.68 den Selbsttest `selftest` (D97). Die bisherigen Glide-Module `compact_mode`, `appearance` und `undo_history` reichen die neutralen Namen weiter.

**Übernahme:** Ein Folgeprojekt übernimmt den Ordner `glide_shell` unverändert in seinen Quellbaum, seit V1.66 über `python3 -B scripts/pflege/shell_uebernehmen.py <Quellordner des Folgeprojekts>`. Das Werkzeug schreibt `glide_shell/SHELL_MANIFEST.json` (Paketversion, Glide-Systemversion, Quell-Commit, SHA-256 je Datei); `--pruefen` meldet je Datei aktuell, veraltet oder verändert. Lokale Änderungen in der Kopie überschreibt es nur mit `--ersetzen`, Dateien ohne Manifesteintrag lässt es stehen. Danach importiert das Folgeprojekt die Bausteine einzeln, etwa `from glide_shell import modal_session, window_lifetime`. Voraussetzungen sind Python mit `tkinter` (geprüft mit 3.14.5 und Tk 9.1.0 auf macOS, Linux/Xvfb und Windows über Glides Matrix); es gibt keine weitere Abhängigkeit. Jede Datei trägt `SPDX-License-Identifier: MPL-2.0`. Texte, Farben, Schriften und Aktionskennungen liefert der Host; `custom_controls` nimmt Schrift, Tinte und Hintergrund über `set_font_provider`, `set_ink_provider` und `set_backdrop_painter` an. `python -m glide_shell.demo` zeigt das Nutzungsmuster.

**Nachweis:** `tests/integration/test_shell_demohost.py` (T330) kopiert nur `glide_shell` in ein leeres Verzeichnis, startet den Host in eigenem Prozess und belegt, dass kein Modul aus `src/glide` geladen wird, Menü, Uhr und `motion`-Übergang im `AfterScope`, modaler Dialog und Abbau ohne offene Zeitgeber funktionieren. Die Verträge der Bausteine prüfen T316 (Modal, 18 Fälle, 10 Gegenproben), T320 (Lebensdauer, 10 Fälle, 7 Gegenproben), T312, T326 und T055 (`motion`); T319 hält Importregel, Signaturen, Paketort und die Sperrklinke der Restkopplung; T331 prüft das Übernahmewerkzeug gegen Temporärordner.

**Anleitung und Selbsttest (D97):** Die Anleitung für Folgeprojekte liegt im Paket: [`README.de.md`](../src/glide/glide_shell/README.de.md) ist führend, [`README.md`](../src/glide/glide_shell/README.md) ihre kontrollierte englische Fassung; das Übernahmewerkzeug kopiert beide mit. Nach der Übernahme prüft `python -m glide_shell.selftest` die Kopie auf dem Zielrechner mit echtem Tk (Exitcode 0 bestanden, 1 Befund, 2 kein Tk-Fenster); T333 belegt ihn mit Kopie und Gegenprobe. Der Demohost zeigt seit V1.68 auch Fensterlage, Systemdesign und Wiederholen.

**Sprache (D96):** Laufzeittexte für Entwickler (Ausnahmen, Protokoll) sind Englisch, T319 prüft das; Docstrings und Kommentare bleiben Deutsch, sichtbare Texte liefert der Host.

Für Agenten bündelt das [Arbeitshandbuch](GLIDE_SHELL_KI_HANDBUCH.md) Bausteine, Regeln, Tests, Prüfwege und Versionierung.

**Grenzen:** Kein eigenes Repository und keine eigene Veröffentlichung; Änderungen entstehen weiter in Glide und werden von Folgeprojekten als Kopie übernommen. Die Kompatibilitätsnamen (`_glide_modal_active`, `_glide_after_scope`, Klassennamen `Glide…`) bleiben. Noch nicht zur Shell gehören die Barrierefreiheit (S12, nicht freigegeben) und der Rückgängig-Stapel; von `ui_design`, `action_menu` und `runtime_config` liegt seit V1.69 nur der neutrale Teil in der Shell (D98).
