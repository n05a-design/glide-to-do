# Glide Shell Framework – Architektur- und Entkopplungskonzept

Stand 11.11.2026 · Glide 3.55.0 · Aufgabenformat 26

Dieses Konzeptdokument beschreibt die architektonische Entkopplung des wiederverwendbaren Desktop-Fundaments (**Glide Shell Framework**) von den fachspezifischen Domänenmodulen der Aufgaben- und Produktivitätsanwendung Glide. Es dient als verbindliche Richtschnur für zukünftige Refactorings und als Blaupause für Schwesterprojekte (z. B. *Steps*).

---

## 1. Ausgangslage und Zielsetzung

Historisch wuchs Glide als Desktop-Anwendung rund um die monolithische Klasse `ListApp` in [`app.pyw`](../src/glide/app.pyw). Trotz erfolgreicher Auslagerung zahlreicher Fachmodule (mittlerweile 95 Python-Quelldateien im Glide-System) verbleiben in `app.pyw` erhebliche Überschneidungen zwischen:
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
|  Lifecycle, Window Manager, Appearance, Widgets, Undo |
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

Die Shell umfasst alle Komponenten, die für jede plattformübergreifende Tkinter-Desktop-Anwendung benötigt werden:

| Bereich | Modul / Komponente | Verantwortung |
|---|---|---|
| **Laufzeit & Konfiguration** | [`runtime_config.py`](../src/glide/runtime_config.py) | Auflösung von AppData-, Cache- und Logpfaden ohne Modulimport-Seiteneffekte; CLI-Flag-Parsing; Headless- & Testumgebungs-Erkennung. |
| **Lebenszyklus (Lifecycle)** | `shell_lifecycle.py` *(neu)* | Kontrollierter Start, sauberer Exit (`WM_DELETE_WINDOW`), Session-Restore, Verhindern doppelter Instanzen (Lockfile). |
| **Theme & Design-System** | [`appearance.py`](../src/glide/appearance.py), [`ui_design.py`](../src/glide/ui_design.py) | Dark-/Light-/Systemmodus-Erkennung, Farb- und Abstands-Token, dynamische Re-Theming-Events ohne Neustart. |
| **Typografie & Symbole** | [`font_catalog.py`](../src/glide/font_catalog.py), [`glyph_metrics.py`](../src/glide/glyph_metrics.py), [`symbol_policy.py`](../src/glide/symbol_policy.py) | Plattformspezifische Schriftarten, Skalierungsfaktoren, optische Zentrierung von Glyphen, sichere ASCII-/Unicode-Fallbacks. |
| **Fenster & Navigation** | [`compact_mode.py`](../src/glide/compact_mode.py), `window_manager.py` *(neu)* | Bildschirmgrenzen-Prüfung, DPI-Awareness, Multi-Monitor-Positionierung, Statusleisten, Sidebar-Layouts. |
| **Dialog-Infrastruktur** | `modal_runner.py` *(neu)* | Robuste modale Dialoge (`app.run_modal`-Abstraktion) mit ausnahmesicherer Tcl-Grab- und Focus-Wiederherstellung. |
| **Custom Controls (D78)** | `controls/` *(abgeleitet)* | Konsistente, zugängliche Widgets (Ersatz für veraltete Tk-Widgets: Schalter, Eingabefelder, Card-Views) mit vollständiger Tk-Schnittstellenkompatibilität (`keys`, `cget`, `configure`, `[]`). |
| **Undo/Redo-Fundament** | [`undo_history.py`](../src/glide/undo_history.py) | Generischer Memento-/Command-Stack mit Snapshot-Drosselung, Tiefenbegrenzung und Transaktionsklammern (`group_undo`). |
| **Barrierefreiheit (A11y)** | [`accessibility.py`](../src/glide/accessibility.py), [`accessibility_bindings.py`](../src/glide/accessibility_bindings.py) | Semantische Rollen, Screenreader-Announcements, Tastaturfokus-Traversierung. |

---

### 2.2 Glide-Fachinhalt (Spezifische Anwendungsdomäne)

Diese Module gehören exklusiv zur fachlichen Identität von Glide und dürfen **nicht** in die Shell einfließen:

| Domänenbereich | Zugehörige Module |
|---|---|
| **Aufgaben- & Listenmodell** | [`persistence.py`](../src/glide/persistence.py), [`storage_health.py`](../src/glide/storage_health.py), [`item_index.py`](../src/glide/item_index.py), [`data_lock.py`](../src/glide/data_lock.py), [`schema_backups.py`](../src/glide/schema_backups.py) (Aufgabenformat 26, Validierung, Migration). |
| **Planung & Kapazität** | [`planning.py`](../src/glide/planning.py), [`day_relief.py`](../src/glide/day_relief.py), [`occupied_time.py`](../src/glide/occupied_time.py), [`week_planning.py`](../src/glide/week_planning.py), [`day_proposal.py`](../src/glide/day_proposal.py). |
| **Produktivitätsmethoden** | [`eisenhower.py`](../src/glide/eisenhower.py) (Matrix), [`focus_timer.py`](../src/glide/focus_timer.py) (Pomodoro), [`routines.py`](../src/glide/routines.py), [`daily_hints.py`](../src/glide/daily_hints.py). |
| **Kalender- & Zeitverwaltung** | [`busy_calendar.py`](../src/glide/busy_calendar.py), [`calendar_service.py`](../src/glide/calendar_service.py), [`repeat_rules.py`](../src/glide/repeat_rules.py), [`repeat_ics.py`](../src/glide/repeat_ics.py), [`ics_busy.py`](../src/glide/ics_busy.py), [`timezones.py`](../src/glide/timezones.py). |
| **Notizen, Seiten & Canvas** | [`page_markdown.py`](../src/glide/page_markdown.py), [`markdown_tree.py`](../src/glide/markdown_tree.py), [`pinboard_pages.py`](../src/glide/pinboard_pages.py) (JSON-Canvas 1.0), [`attachment_paths.py`](../src/glide/attachment_paths.py). |
| **Import / Export** | [`notion_import.py`](../src/glide/notion_import.py), [`notion_archive.py`](../src/glide/notion_archive.py), [`exchange_patch.py`](../src/glide/exchange_patch.py). |

---

## 3. Bewertung der Zwei-Fenster- und Multi-Window-Architektur

### 3.1 Aktuelle Situation in Glide
Glide verwendet eine primäre Tk-`root`-Instanz für das Hauptfenster und `Toplevel`-Instanzen für Zusatzfenster (z. B. Nebenansichten, Modaldialoge, Einstellungen oder Zeichenflächen).

**Erkannte Herausforderungen:**
1. **macOS Event Loop & Menübindung:** Auf macOS gehört das Anwendungsmenü (`Apple Menu`) zwingend zur primären `root`-Instanz. Wenn ein Toplevel-Fenster schließt oder den Fokus wechselt, darf das Menü nicht in einen verwaisten Zustand fallen.
2. **Modal Grab Deadlocks:** Wird ein Modalfenster (`grab_set()`) nicht absolut ausnahmesicher geschlossen (oder stürzt der Aufrufer währenddessen ab), bleibt der Tcl-Grab aktiv. Die gesamte Anwendung blockiert, da keine Mausklicks oder Tastaturevents mehr an das Hauptfenster zugestellt werden (dies war die Ursache historischer CI-Timeouts unter Linux/Xvfb).
3. **Multi-Monitor DPI-Scaling (Windows Per-Monitor V2):** Wenn Haupt- und Nebenfenster auf Monitoren mit unterschiedlichen Skalierungsfaktoren (z. B. 100% vs. 175%) liegen, müssen Schriften und Widgetabstände je Fensterinstanz isoliert berechnet werden können.

### 3.2 Architekturvorgabe für die Shell
Die Shell führt einen zentralen `WindowManager` ein:
- **Root-Transparenz:** Die Anwendung erstellt Fenster nicht direkt per `tk.Toplevel(self.root)`, sondern fordert Fenster über den `WindowManager` an:
  `window = shell.create_window(title="Tagesentlastung", kind=WindowKind.MODAL_DIALOG, parent=...)`
- **Ausnahmesicherer Modal-Runner:**
  Ein einheitlicher Context Manager klammert alle modalen Interaktionen:
  ```python
  with shell.modal_session(dialog_window):
      shell.wait_window(dialog_window)
  # Garantiert: grab_release(), focus_set() auf Parent und Zerstörung von Hooks
  ```
- **Zwei-Fenster- und Pane-Orchestrierung:**
  Für Dual-Pane-Ansichten (Hauptliste + Detailinspektor) stellt die Shell native Container bereit (z. B. splitfähige PanedWindows oder Side-Drawers), die Fensterkoordinaten automatisch innerhalb der virtuellen Desktopgrenzen halten (`compact_mode.py`).

---

## 4. Empfohlene Migrationsreihenfolge (Schritt-für-Schritt)

Die Entkopplung erfolgt inkrementell ohne Bruch der bestehenden Funktionalität oder Datenformate:

### Phase 1: Laufzeit- und Pfad-Entkopplung (Bereits in 3.55.0 umgesetzt)
- **Status:** **Erledigt mit [`runtime_config.py`](../src/glide/runtime_config.py)** (M095, WA-49).
- **Nutzen:** Daten- und Konfigurationspfade können ohne Seiteneffekte und ohne Tk-Initialisierung instanziiert werden. Tests und Headless-Werkzeuge greifen auf isolierte Pfade zu.

### Phase 2: Design- und Widget-Extraktion
- **Aufgabe:** Zusammenfassung von [`appearance.py`](../src/glide/appearance.py), [`ui_design.py`](../src/glide/ui_design.py) und den D78-Custom-Controls in ein Teilpaket `glide_shell.ui`.
- **Ziel:** Einheitliche Widget-Schnittstelle (`keys()`, `configure()`, Event-Binding) unabhängig vom konkreten Glide-Inhalt.

### Phase 3: Modal- und Dialog-Manager
- **Aufgabe:** Formalisierung von `run_modal` aus `app.pyw` in ein isoliertes Modul `glide_shell.dialogs`.
- **Ziel:** Schutz vor Livelocks, standardisierte Bestätigungs-, Eingabe- und Auswahldialoge mit einheitlicher Tastaturbedienung (Escape zum Abbrechen, Enter zum Bestätigen).

### Phase 4: Undo/Command-Abstraktion
- **Aufgabe:** Entkopplung von [`undo_history.py`](../src/glide/undo_history.py) von den Datenstrukturen der Aufgabenliste.
- **Ziel:** `UndoHistory` akzeptiert beliebige serialisierbare Memento-Objekte oder Command-Objekte mit `execute()` und `undo()`.

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
1. **Volle Testbarkeit ohne Tkinter:** Domänenfeatures wie die Kapazitätsanalyse (`planning.capacity_analysis`) oder Datumsberechnungen können zu 100% in schnellen Unit-Tests geprüft werden.
2. **Wiederverwendbarkeit für Folgeprojekte:** Neue Anwendungen wie *Steps* binden lediglich die Shell ein und bringen eigene Domänen-Controller und Ansichten mit.
3. **Plattform-Sicherheit:** Alle Plattform-Eigenheiten (macOS Cocoa-Menüs, Windows DPI, Linux X11/Wayland-Clipboard) sind an einer einzigen Stelle im Shell-Fundament gekapselt.
