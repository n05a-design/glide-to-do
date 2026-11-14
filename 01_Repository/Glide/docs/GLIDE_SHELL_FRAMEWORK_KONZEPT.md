# Glide Shell Framework – Architektur- und Entkopplungskonzept

Stand 14.11.2026 · Glide 3.61.0 · Aufgabenformat 26

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
| Fenster, Navigation und modale Dialoge | Root-/Toplevel-Lebensdauer, Fokus, Grab-Freigabe, Bildschirmgrenzen und Menübesitz koordinieren | [UI/Navigation](../src/glide/README.md#uinavigation) und [Tk-Regeln](02_ARCHITECTURE.md#5-tk-fallstricke-teuer-gelernt). `run_modal` liegt in `ListApp`; ein `window_manager.py` oder `modal_runner.py` ist hier nur ein vorgeschlagener Schnitt. |
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
- **Aufgabe:** Formalisierung von `run_modal` aus `app.pyw` in ein isoliertes Modul `glide_shell.dialogs`.
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
- **Modal:** `run_modal` ist der einzige Warteweg und hängt an Theme, Mindestbreite, Vordergrund und Fehlerprotokoll der `ListApp`. Vor einer Verlagerung steht ein Vertragstest mit echtem Grab, Fokus, Abbruch und Besitzerabbau.

| Modul | Neutral | Glide-gebunden |
|---|---|---|
| `motion` | vollständig | – |
| `compact_mode` | `parse`, `format_geometry`, `clamp`, `keep_visible` | Mindestmaße, Einstellungsname, Kürzelregel |
| `appearance` | Designpaar, Erkennung des Systemmodus | Hintergrundauswahl, `with_background` |
| `ui_design` | Skalen, `fit_text`, `clip_title`, Breitenausgleich, `settled_wrap_width` | `task_title`, `today_columns`, `page_icon_layout` |
| `action_menu` | Eintragsmodell, Gruppierung, Auswahl | Begründungstexte, Bindung an `content_search` |
| `accessibility`, `accessibility_bindings`, `core_accessibility` | `Attributes`, `set_attributes`, `Binding`, allgemeine Binder | `task_value`, alle Binder mit `app` |
| `undo_history` | `RedoHistory` | Board-Einträge |
| `runtime_config` | Auflösungsmechanik | Produktname, Dateinamen, Umgebungsvariablen |
