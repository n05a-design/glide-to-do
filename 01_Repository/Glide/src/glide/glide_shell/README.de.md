# Glide Shell – Anleitung für Folgeprojekte

Stand 23.11.2026 · Glide 1.0.2 · Glide Shell 0.6.2

<p align="right"><a href="README.md">English</a></p>

Die Glide Shell ist das wiederverwendbare Tk-Fundament aus [Glide](../../../README.md): Dialoge, Zeitgeberbesitz, Übergänge, Bedienelemente, Menüleiste, Fenstergeometrie, Systemdesign, Wiederholen-Stapel, Textkürzung, durchsuchbare Aktionsauswahl und Auflösung des Datenordners. Sie kennt keine Glide-Inhalte. Texte, Farben, Schriften und Aktionskennungen liefert deine Anwendung.

Diese Anleitung beschreibt die Nutzung. Maßgeblich für Grenzen und Entscheidungen ist das [Shell-Konzept §7](../../../docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md#7-paket-glide_shell-und-übernahme-in-folgeprojekte-d95-20112026).

## Voraussetzungen

- Python 3 mit `tkinter`; geprüft mit Python 3.14.5 und Tk 9.1.0 auf macOS, Linux und Windows.
- Keine weitere Abhängigkeit. Jede Datei steht unter `MPL-2.0`.

## Übernehmen

Aus einem Glide-Checkout, mit dem Quellordner deines Projekts als Ziel:

```bash
python3 -B 01_Repository/Glide/scripts/pflege/shell_uebernehmen.py <dein-projekt>/src
```

Das Werkzeug kopiert `glide_shell/` samt dieser Anleitung und schreibt `glide_shell/SHELL_MANIFEST.json` (Paketversion, Quell-Commit, SHA-256 je Datei).

- `--pruefen` meldet je Datei `aktuell`, `veraltet` oder `verändert` und schreibt nichts.
- Hast du Dateien in der Kopie geändert, bricht ein Update ab; erst `--ersetzen` überschreibt sie.
- Eigene Dateien im Ordner bleiben stehen.

## Auf dem Zielrechner prüfen

```bash
cd <dein-projekt>/src
python3 -m glide_shell.selftest
```

Der Selbsttest öffnet kurz ein unsichtbares Tk-Fenster und prüft jeden Baustein mit echtem Tk. Jede Zeile beginnt mit `ok` oder `FAIL`. Exitcode 0 heißt, alles ist bestanden; 2 heißt, Tk konnte kein Fenster öffnen (zum Beispiel ohne Anzeige).

## Beispiel ansehen

```bash
python3 -m glide_shell.demo
```

Der Demonstrationshost ist eine kleine App nur aus Shell-Bausteinen: Menüleiste, Uhr im eigenen Zeitgeberbereich mit kurzem Übergang, Kontrollkästchen, modaler Dialog, Zähler mit Rückgängig und Wiederholen als Befehle (`command_history`), Start über `app_host`, Fensterlage auf dem Bildschirm und Hell/Dunkel nach System. Sein Quelltext [`demo.py`](demo.py) zeigt das Nutzungsmuster.

## Bausteine

Importiere die Bausteine einzeln, etwa `from glide_shell import modal_session, window_lifetime`. Das Paket lädt beim Import nichts nach.

| Modul | Wofür | Wichtigste Namen |
|---|---|---|
| `modal_session` | Dialoge erzeugen und modal warten, Fokus zurückgeben | `create_dialog`, `run_modal`, `wait_modal`, `modal_over` |
| `window_lifetime` | Zeitgeber gehören einem Widget und enden mit ihm | `scope_for`, `AfterScope` |
| `motion` | Kurze, unterbrechbare Übergänge (höchstens 150 ms) | `Transitions`, `progress` |
| `custom_controls` | Thementaugliche Canvas-Bedienelemente | `GlideCheckbutton`, `GlideRadiobutton`, `GlideListbox`, `GlideScale`, `ThemedAutoScrollbar` |
| `desktop_adapter` | Menüleiste, Tastaturkürzel, Plattform, Zwischenablage | `build_menu_tree`, `format_accelerator`, `platform_name`, `launch_path` |
| `window_geometry` | Geometrietexte, Fenster auf der Arbeitsfläche halten | `parse`, `format_geometry`, `clamp`, `keep_visible` |
| `system_appearance` | Hell/Dunkel des Systems deuten | `tk_is_dark`, `windows_is_dark`, `linux_is_dark`, `resolve` |
| `redo_history` | Wiederholen-Stapel neben deinem Rückgängig-Stapel | `RedoHistory` |
| `text_fit` | Text auf Zeichengrenze oder Pixelbreite kürzen, Zeichen auf gleiche Breite bringen | `clip`, `fit`, `settled_wrap_width`, `aligned_markers` |
| `action_picker` | Durchsuchbare Auswahl über die Einträge eines fertigen Menüs | `entries`, `search`, `grouped`, `first_enabled` |
| `runtime_paths` | Daten- und Cacheordner nach Plattformkonvention, Umgebungsvariable und Zeigerdatei | `platform_data_dir`, `platform_cache_dir`, `resolve_base` |
| `command_history` | Rückgängig und Wiederholen für Befehlsobjekte oder Zustandsabbilder, mit Rückweg bei Fehlern | `Command`, `CommandHistory` (`execute`, `record`, `undo`, `redo_step`) |
| `app_host` | Hauptfenster starten: Schritte vor Tk, Startprüfungen, Platzhalter, Controller, Menüleiste, Kürzel, Schließweg | `AppHost`, `bind_shortcuts`, `primary_shortcuts`, `attach_menubar`, `install_close` |

Ein Start mit App-Host und Befehlsverlauf, wie im Demohost:

```python
from glide_shell import app_host, command_history

class App:
    def __init__(self, root):
        self.history = command_history.CommandHistory()
        platform = app_host.platform_of(root.tk.call("tk", "windowingsystem"))
        app_host.bind_shortcuts(root, app_host.primary_shortcuts("z", lambda _e: self.history.undo(), platform), platform)
        app_host.install_close(root, root.destroy, platform)

app_host.AppHost(preflight=(lambda root: None,)).run(App)
```

Für KI-Agenten, die mit der Shell ein neues Projekt bauen, steht der vollständige Ablauf mit Prozessen, Design-Richtlinien und Prüfungen in [`KI_ANLEITUNG_NEUE_PROJEKTE.md`](KI_ANLEITUNG_NEUE_PROJEKTE.md) (englisch: [`AI_GUIDE_NEW_PROJECTS.md`](AI_GUIDE_NEW_PROJECTS.md)); einen fertigen Startprompt für die erste Sitzung enthält [`STARTPROMPT_KI.md`](STARTPROMPT_KI.md).

Ein Muster aus dem Demohost: Zeitgeber und Übergänge eines Fensters über denselben Bereich planen, damit beim Schließen nichts weiterläuft.

```python
from glide_shell import motion, window_lifetime

scope = window_lifetime.scope_for(root)
transitions = motion.Transitions(scope.after, scope.cancel)
transitions.start("clock", lambda value: label.configure(fg=accent if value < 1 else text))
```

## Grenzen

- Kein eigenes Repository und keine eigene Veröffentlichung. Änderungen entstehen in Glide; du übernimmst neue Stände mit dem Werkzeug oben.
- Einige Namen tragen aus Kompatibilitätsgründen `glide` (`_glide_after_scope`, `GlideCheckbutton` …).
- Laufzeitmeldungen der Shell für Entwickler sind Englisch.
