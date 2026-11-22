# Glide Shell – Arbeitshandbuch für KI-Agenten

Stand 22.11.2026 · Glide 1.0.1 · Glide-System V1.69 · Glide Shell 0.5.0 · Aufgabenformat 26

Dieses Handbuch bündelt alles, was ein KI-Agent braucht, um an der Glide Shell zu arbeiten oder sie in einem Folgeprojekt zu nutzen: Zweck, Bausteine, Host-Verträge, Regeln, Tests, Prüfwege, Versionierung, Übernahme, Git-Ablauf und Stolperstellen. Es **verweist** auf die führenden Quellen und doppelt deren Regeln nicht. Bei Widerspruch gelten die verlinkten Quellen.

| Frage | Führende Quelle |
|---|---|
| Was gehört zur Shell, was bleibt bei Glide, warum? | [Shell-Konzept](GLIDE_SHELL_FRAMEWORK_KONZEPT.md), §6 „Validierte Grenzen“ und §7 „Paket `glide_shell`“ |
| Welche Entscheidungen gelten? | [Arbeitsrichtung](ARBEITSRICHTUNG.md), D86, D94–D98 |
| Wie nutzt ein Folgeprojekt die Shell? | [`glide_shell/README.de.md`](../src/glide/glide_shell/README.de.md) (führend), [`README.md`](../src/glide/glide_shell/README.md) (englische Fassung) |
| Welche Module und Tests gibt es (M-/T-Nummern)? | [Glide-System](../src/glide/README.md), Modultabelle M101–M109 und Testtabelle |
| Wie ist die Shell in Glide eingebaut? | [Architektur](02_ARCHITECTURE.md), Absatz „Shell-Paket `glide_shell`“ |
| Was wurde wann umgesetzt und geprüft? | [Entwicklungsplan](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) §21.148–§21.157, [QA-Bericht](07_QA_BERICHT.md), [CHANGELOG](../CHANGELOG.md) |
| Allgemeine Arbeitsregeln im Repository | [AGENTS.md](../AGENTS.md), [CLAUDE.md](../../../CLAUDE.md), [Dokumentenpflege](DOKUMENTENPFLEGE.md) |

## 1. Zweck in einem Absatz

Die Glide Shell ist das wiederverwendbare Tk-Fundament aus Glide: Dialoge, Zeitgeberbesitz, Übergänge, Bedienelemente, Menüleiste, Fenstergeometrie, Systemdesign, Wiederholen-Stapel, Textkürzung, Aktionsauswahl und Datenordner-Auflösung. Sie liegt als Unterpaket `src/glide/glide_shell/` in Glide, kennt keine Glide-Inhalte und wird von Folgeprojekten als Kopie übernommen (D95). Es gibt **kein eigenes Repository und keine eigene Veröffentlichung**; Änderungen entstehen in Glide.

## 2. Aufbau des Pakets

```text
src/glide/glide_shell/
  __init__.py          SHELL_VERSION, Modulliste (__all__), lädt nichts nach
  modal_session.py     Shell-Paket 1   Dialogfabrik, modaler Warteweg, Fokusrückgabe
  window_lifetime.py   Shell-Paket 3c  Zeitgeber gehören einem Widget (AfterScope)
  custom_controls.py   Shell-Paket 4   Canvas-Bedienelemente mit Host-Hooks
  desktop_adapter.py   Shell-Paket 5   Menüleiste, Kürzel, Plattform, Zwischenablage, Startweg
  demo.py              Shell-Paket 6   Demonstrationshost nur aus Shell-Bausteinen
  motion.py            Shell-Paket 7   kurze, unterbrechbare Übergänge (≤150 ms)
  window_geometry.py   Shell-Paket 8   Geometrietexte, Fenster auf der Arbeitsfläche halten
  system_appearance.py Shell-Paket 9   Hell/Dunkel des Systems deuten
  redo_history.py      Shell-Paket 10  Wiederholen-Stapel neben dem Rückgängig-Stapel
  selftest.py          Shell-Paket 11  Selbsttest einer Kopie auf dem Zielrechner
  text_fit.py          Shell-Paket 12  Text auf Zeichen-/Pixelbreite kürzen, Marker ausgleichen
  action_picker.py     Shell-Paket 13  durchsuchbare Auswahl aus einem fertigen Menü
  runtime_paths.py     Shell-Paket 14  Daten-/Cacheordner nach Plattform, Umgebung, Zeiger
  README.de.md         Anleitung für Folgeprojekte (führend)
  README.md            kontrollierte englische Fassung
```

Die erste Zeile jedes Modul-Docstrings beginnt mit `Shell-Paket N:`. T319 verlangt, dass jedes so gekennzeichnete Modul in `SHELL_MODULE` steht und umgekehrt.

### Öffentliche Schnittstelle

Die verbindliche Liste aller öffentlichen Funktionen und Methoden mit Parameternamen steht in `SHELL_MODULE` in [`tests/unit/test_shell_importregel.py`](../tests/unit/test_shell_importregel.py). Wer eine Signatur ändert, ändert sie dort im selben Commit. Kurzüberblick:

| Modul | Wichtigste Namen | Host liefert |
|---|---|---|
| `modal_session` | `create_dialog`, `run_modal`, `wait_modal`, `modal_over`, `remember_focus`, `return_focus` | Titel, Hintergrund, Fehlerprotokoll-Rückruf |
| `window_lifetime` | `scope_for`, `AfterScope` (`after`, `after_idle`, `adopt`, `cancel`, `cancel_all`, `close`), `pending_jobs` | das besitzende Widget |
| `custom_controls` | `GlideCheckbutton`, `GlideRadiobutton`, `GlideListbox`, `GlideScale`, `ThemedAutoScrollbar`, `CanvasLabel` | Schrift (`set_font_provider`), Tinte (`set_ink_provider`), Hintergrund (`set_backdrop_painter`) |
| `desktop_adapter` | `build_menu_tree`, `DesktopMenuBar`, `format_accelerator`, `primary_modifier`, `platform_name`, `launch_path`, Zwischenablage | Menüeinträge, Aktionskennungen, Beschriftungen, `modifier_labels` |
| `motion` | `Transitions` (`start`, `cancel`, `close`), `progress` | Zeitplanung (`scope.after`, `scope.cancel`) |
| `window_geometry` | `parse`, `format_geometry`, `clamp` (Mindestmaß Pflicht), `keep_visible` | Mindestmaß, Bildschirmmaße |
| `system_appearance` | `tk_is_dark`, `windows_is_dark`, `linux_is_dark`, `resolve` | Registry-/gsettings-Rückrufe, Designpaar |
| `redo_history` | `RedoHistory` (`note_write`, `mark`, `validate`, `peek`, `push`, `pop`, `restore`, `clear`) | den eigenen Rückgängig-Stapel |
| `text_fit` | `clip`, `fit`, `settled_wrap_width`, `pad_to_width`, `aligned_markers`, `HAIR_SPACE` | Messfunktion (`font.measure`), Grenzen |
| `action_picker` | `Entry`, `entries`, `search`, `grouped`, `first_enabled`, `counts`, `check_label`, `clean_label` | Menüzeilen, Abschnittsnamen, Platzhalter, Sperrgrund-Rückruf, optional Suchschlüssel |
| `runtime_paths` | `platform_data_dir`, `platform_cache_dir`, `env_dir`, `read_pointer`, `resolve_base` | Produktname, Variablen- und Dateinamen |
| `selftest` | `run`, `CHECKS`, `check_*` | nichts; läuft mit `python -m glide_shell.selftest` |
| `demo` | `DemoHost`, `main`, `system_dark` | optional Texte, Farben, Geometrie |

Kompatibilitätsnamen mit `glide` bleiben bewusst: `_glide_modal_active`, `_glide_modal_finished`, `_glide_after_scope`, `_glide_action_ids`, Klassennamen `Glide…`.

## 3. Regeln, die Tests erzwingen

1. **Abhängigkeitsrichtung Host → Shell → Tk.** Shell-Module importieren nur die Standardbibliothek, `tkinter` und einander absolut über `glide_shell` (kein relativer Import). T319.
2. **Keine Glide-Werte.** Bezeichner, die mit `glide_`, `APP_`, `ERROR_LOG`, `THEMES` oder `theme` beginnen, sowie `ListApp`, `importlib`, `__import__`, `exec`, `eval`, `import_module` sind verboten. Darum heißt es im Selbsttest `from glide_shell import SHELL_VERSION` statt `glide_shell.SHELL_VERSION`. T319.
3. **Kein gleichnamiges Modul neben dem Paket.** `src/glide/<name>.py` darf es für kein Shell-Modul geben; deshalb heißt der Baustein aus `action_menu` `action_picker`. T319.
4. **Entwicklermeldungen auf Englisch (D96).** Zeichenketten im Code (außer Docstrings) dürfen keine Umlaute und keine deutschen Füllwörter wie „der/die/das/und/nicht/kein/fehlt/Fehler/ungültig“ enthalten. Docstrings und Kommentare bleiben Deutsch. Sichtbare Texte liefert der Host. T319.
5. **Muster D96/D98 für neue Bausteine.** Nur der neutrale Teil wandert in die Shell; das Glide-Modul reicht **dieselben Objekte** weiter (`from glide_shell.x import name  # noqa: F401`) oder ruft sie mit Glide-Werten auf. Glide-Konstanten, Texte, Grenzen und Namen bleiben beim Host. T332/T334 prüfen die Identität mit `assertIs`.
6. **Sperrklinke der Restkopplung (D94).** `app.pyw` darf höchstens einen direkten `tk.Toplevel` (Tooltip) und keinen Zeitgeber ohne `AfterScope` enthalten; sinkt eine Zahl, wird die Grenze in `RESTKOPPLUNG` im selben Commit gesenkt. T319.
7. **Paketbau nimmt die Shell mit.** `packaging/paket/package_spec.py` und `package_sources.py` müssen alle Shell-Module liefern (T319 `Paketbau`). Zusätzlich führen [`scripts/pflege/abgleich_07.py`](../scripts/pflege/abgleich_07.py) und [`packaging/macos/baue_app.py`](../packaging/macos/baue_app.py) eine **ausdrückliche Dateiliste** `glide_shell/<name>.py`; jedes neue Modul dort ergänzen.
8. **Der Selbsttest bleibt unter `python -O` wirksam.** Prüfungen nutzen `expect()` statt `assert`; Ereignisschleifen laufen außerhalb von Prüfanweisungen. T333 führt die Gegenprobe ohne und mit `-O` aus.

## 4. Tests rund um die Shell

| T-Nr. | Datei | Art | Prüft |
|---|---|---|---|
| T319 | [`tests/unit/test_shell_importregel.py`](../tests/unit/test_shell_importregel.py) | Syntaxbaum, ohne Tk | Modulliste, Importregel, verbotene Namen, englische Meldungen, Signaturen, Sperrklinke, Paketbau |
| T317 | [`tests/unit/test_modal_session.py`](../tests/unit/test_modal_session.py) | Unit | `modal_session` |
| T326 | [`tests/unit/test_desktop_adapter.py`](../tests/unit/test_desktop_adapter.py) | Unit | Plattform, Kürzeltexte, Menübaum |
| T055 | [`tests/unit/test_motion.py`](../tests/unit/test_motion.py) | Unit | `motion` |
| T332 | [`tests/unit/test_shell_d96.py`](../tests/unit/test_shell_d96.py) | Unit | `window_geometry`, `system_appearance`, `redo_history`; Weitergabe durch Glide |
| T334 | [`tests/unit/test_shell_d98.py`](../tests/unit/test_shell_d98.py) | Unit | `text_fit`, `action_picker`, `runtime_paths`; Weitergabe durch Glide |
| T312 | [`tests/integration/test_custom_controls.py`](../tests/integration/test_custom_controls.py) | echtes Tk | Bedienelemente |
| T316 | [`tests/integration/test_modalvertrag.py`](../tests/integration/test_modalvertrag.py) | echtes Tk, 18 Fälle | Grab, Fokus, Verschachtelung |
| T318 | [`tests/integration/test_abbauvertrag.py`](../tests/integration/test_abbauvertrag.py) | volle App | Abbau ohne offene Zeitgeber |
| T320 | [`tests/integration/test_fensterlebensdauer.py`](../tests/integration/test_fensterlebensdauer.py) | echtes Tk, ohne Glide, 10 Fälle | `window_lifetime` |
| T330 | [`tests/integration/test_shell_demohost.py`](../tests/integration/test_shell_demohost.py) | Paketkopie ohne Glide | Demohost, Paketgrenze |
| T333 | [`tests/integration/test_shell_selbsttest.py`](../tests/integration/test_shell_selbsttest.py) | Paketkopie, eigener Prozess | Selbsttest 10/10, Gegenprobe ohne und mit `-O` |
| T331 | [`tests/tools/test_shell_uebernahme.py`](../tests/tools/test_shell_uebernahme.py) | Werkzeugtest | Übernahme, Manifest, Schutz lokaler und fremder Dateien |

Glide-seitige Verhaltenstests, die beim Umbau eines Glide-Moduls unverändert grün bleiben müssen: `test_ui_design.py`, `test_action_menu.py`, `test_runtime_config.py` (simuliert macOS/Windows/Linux über `rc.os`, `rc.IS_MACOS`, `rc.IS_WINDOWS` – deshalb liest `runtime_config._platform()` diese Werte zur Aufrufzeit), `test_appearance.py`, `test_compact_mode.py`, `test_undo_history.py`, `test_i18n.py` (T329, `modifier_labels`).

## 5. Prüfwege

Immer mit isoliertem `GLIDE_DATA_DIR`, künstlichen Daten und `python3 -B`; nie echte Nutzerdaten. Referenzumgebung auf dem Mac: Python 3.14.5 mit eigener Tk 9.1 (`PYTHONPATH=<Tk-9.1-Laufzeit>/python-extension:tests/tools/hintergrund`), `GLIDE_QA_HINTERGRUND=1`, `LANGUAGE=de`; ohne die eigene Laufzeit liefert das Framework-Python nur Tk 9.0.x, dann das Ergebnis so kennzeichnen. Im Linux-Container: „Linux/Tk 8.6, künstliche Daten“. GUI-Suiten nie parallel starten; sie brauchen den Tastaturfokus.

```bash
cd 01_Repository/Glide
export GLIDE_DATA_DIR="$(mktemp -d)"
python3 -B -m unittest tests/unit/test_shell_importregel.py tests/unit/test_shell_d96.py tests/unit/test_shell_d98.py
python3 -B -m unittest tests/tools/test_shell_uebernahme.py
python3 -B tests/integration/test_shell_selbsttest.py
python3 -B tests/integration/test_shell_demohost.py
python3 -B tests/integration/test_fensterlebensdauer.py
python3 -B tests/integration/test_modalvertrag.py
```

| Stufe | Befehl | Enthält |
|---|---|---|
| Gezielte Teilprüfung | Befehle oben | Shell allein |
| CI-Grundstufe | `python3 -B tests/tools/ci_grundstufe.py --protokoll <Ordner>` | alle Unit- und Werkzeugtests, Analysen, Stand-/Link-/Ablageprüfung, Datenschutz, Startprobe |
| Vollprüfung | `python3 -B tests/tools/pruefen.py --zugang-nativ --modus voll --protokoll <Ordner> --timeout 900` | zusätzlich alle Suiten aus `SUITEN` (darunter T312, T316, T318, T320, T330, T333, Startwege) und Beispiel-/Releasedaten |
| GitHub | `.github/workflows/python-app.yml` | Grundstufe, Linux- und Windows-Vollprüfung bei jedem PR |
| macOS-Paket | `.github/workflows/macos-paket.yml` (Push auf `main`; per `workflow_dispatch` mit `vollpruefung`) | Bundlebau mit eigener Tk 9.1, isolierter Start, optional native Vollprüfung |

Der Selbsttest selbst ist zugleich der schnellste Nachweis auf einem fremden Rechner:

```bash
cd src/glide
python3 -m glide_shell.selftest      # Exitcode 0 ok, 1 Befund, 2 kein Tk-Fenster
python3 -O -m glide_shell.selftest   # muss dasselbe melden
```

Lokal auf dem Mac die Vollprüfung mit `--vordergrund` und ohne `tests/tools/hintergrund` im `PYTHONPATH` laufen lassen, wie der macOS-Workflow: Im Hintergrundmodus bekommen die Prüffenster keinen Tastaturfokus, und Fälle wie `kompakt_verlorenes_loslassen` melden `focus: None`. Während des Laufs Maus und Tastatur nicht benutzen. Der frühere Hänger in `anhangsnamen` war eine echte Umbruchschaukel und ist seit V1.69 behoben (QA-Bericht).

## 6. Versionierung

| Zähler | Ort | Wann erhöhen |
|---|---|---|
| `SHELL_VERSION` (SemVer, derzeit 0.5.0) | `glide_shell/__init__.py` | Minor bei neuem Baustein oder neuer öffentlicher Funktion; Patch bei Korrektur ohne Schnittstellenänderung; Major (≥1.0) erst bei einer zugesagten stabilen Schnittstelle |
| Glide-System-Version (derzeit 1.83) | `GLIDE_SYSTEM_VERSION`, Kopf und Versionstabelle in [`src/glide/README.md`](../src/glide/README.md) | jeder Schnitt mit neuem Modul, neuem Test oder geändertem Katalog; `test_glide_system.py` prüft, dass Datei und Katalogkopf übereinstimmen |
| App-Version (1.0.0) | `VERSION`, `app.pyw` | nur in einer Produktionsrunde |
| Aufgabenformat (26) | Datenformat | Shell-Arbeit ändert es nicht |
| Entscheidungen | [Arbeitsrichtung](ARBEITSRICHTUNG.md) | jeder neue Baustein braucht eine Inhaberfreigabe (D96-Muster), festgehalten als neue Zeile D9x; dann Bereichsangabe „D01–D9x“ in `AGENTS.md`, `CLAUDE.md`, Übergabe und `docs/ai/gemini/*` mitziehen |

Verlauf: 3.62.0–3.68.0 Pakete 1–5 flach in `src/glide` (D86) · V1.61–V1.62 Restkopplung R1–R4 (D94) · V1.64 Unterpaket `glide_shell` 0.1.0 und Demohost (D95) · V1.66 `motion`, Übernahmewerkzeug (0.2.0) · V1.67 `window_geometry`, `system_appearance`, `redo_history`, englische Meldungen (D96, 0.3.0) · V1.68 Selbsttest, Demohost, Anleitung (D97, 0.4.0) · V1.69 `text_fit`, `action_picker`, `runtime_paths` (D98, 0.5.0).

## 7. Übernahme in ein Folgeprojekt

```bash
python3 -B 01_Repository/Glide/scripts/pflege/shell_uebernehmen.py <projekt>/src             # anlegen/aktualisieren
python3 -B 01_Repository/Glide/scripts/pflege/shell_uebernehmen.py --pruefen <projekt>/src   # nur prüfen
python3 -B 01_Repository/Glide/scripts/pflege/shell_uebernehmen.py --ersetzen <projekt>/src  # bewusst überschreiben
```

- Kopiert alle `*.py` und `*.md` aus `glide_shell/` und schreibt `glide_shell/SHELL_MANIFEST.json` (`paket`, `shell_version`, `glide_system_version`, `quell_commit`, `quelle_unveraendert`, `lizenz` MPL-2.0, `dateien` mit SHA-256).
- `--pruefen` meldet je Datei `aktuell`, `veraltet`, `verändert`, `fehlt`, `neu in der Quelle` oder `nicht mehr in der Quelle`.
- Ohne `--ersetzen` bricht die Übernahme ab (Exitcode 2), wenn eine Datei vom eigenen Manifest abweicht, der Zielordner ohne Manifest nicht leer ist oder eine neue Shell-Datei eine eigene Datei gleichen Namens überschreiben würde.
- Ziele im Glide-Quellbaum lehnt das Werkzeug ab.
- Danach im Folgeprojekt `python3 -m glide_shell.selftest` ausführen.

## 8. Glide als Host – wo die Shell eingebunden ist

| Glide-Modul | Shell-Baustein | Was beim Host bleibt |
|---|---|---|
| `app.pyw` | `modal_session`, `window_lifetime`, `custom_controls`, `desktop_adapter`, `motion` (`from glide_shell import …`) | Fassaden wie `ListApp.run_modal`, Designs, Texte |
| `compact_mode.py` | `window_geometry` | Mindestmaße (`COMPACT_MIN`), Kürzelregel, Kompaktlage |
| `appearance.py` | `system_appearance` | Designpaare, Hintergrundwahl |
| `undo_history.py` | `redo_history` | Pinnwand-Einträge, Rückgängig-Stapel |
| `ui_design.py` | `text_fit` | Skalen, Titelgrenze `clip_title`, `task_title`, `today_columns` |
| `action_menu.py` | `action_picker` | Sperrgründe, Platzhalter, Zustandstexte, Suchschlüssel aus `content_search` |
| `runtime_config.py` | `runtime_paths` | `Glide`, `GLIDE_DATA_DIR`, `GLIDE_CACHE_DIR`, `datenordner.json`, `RuntimePaths`, Meldungen |

Nicht in der Shell und nicht freigegeben: S12 Barrierefreiheit (`accessibility*`), der Rückgängig-Stapel von `ListApp`.

## 9. Ablauf: neuen Baustein hinzufügen (Prüfliste)

1. Freigabe des Inhabers einholen (Entscheidungsvorlage nach D96) und als D9x in der Arbeitsrichtung festhalten.
2. Neutralen Teil nach `glide_shell/<name>.py` legen; Kopfzeile `Shell-Paket N: …`; Laufzeittexte Englisch; keine verbotenen Namen; Name darf nicht mit einem Glide-Modul kollidieren.
3. Glide-Modul auf Weitergabe umstellen; Glide-Werte als Argumente einreichen; bestehende Glide-Tests unverändert grün halten.
4. `SHELL_MODULE` in T319 ergänzen; Verhaltenstest (Muster T332/T334) mit `assertIs` für die Weitergabe.
5. `__init__.py`: Docstring-Liste, `__all__`, `SHELL_VERSION` anheben.
6. Selbsttest um eine Prüfung ergänzen, Zahl in T333 anpassen.
7. Dateilisten in `abgleich_07.py` und `baue_app.py` ergänzen.
8. Doku nachziehen: Anleitung (DE führend, EN), Shell-Konzept §6/§7, Architektur, Katalog (Versionszeile, M-/T-Zeilen, Zählungen, Kopf), `GLIDE_SYSTEM_VERSION`, CHANGELOG, QA-Testplan, QA-Bericht, Entwicklungsplan §21.x, Übergabe- und Meilensteinkopf, Bereich „D01–D9x“, dieses Handbuch.
9. Grundstufe und gezielte Suiten; vor dem Phasenende eine Vollprüfung (D51).

## 10. Git-Ablauf und Stolperstellen

- Commits im frischen Klon außerhalb OneDrive; Identität aus dem letzten `main`-Commit; keine Force-Pushes; keine Tags oder Releases ohne Freigabe.
- Nie stagen: `20_Grafik_Master/09_Inspiration/`, `GLIDE_STEPS_GESAMTAUDIT_V2_2026-11-10/`, `glide_master_audit_bericht.md`, `SQLite-Copyright.md`.
- Vor dem Commit `__pycache__` entfernen; kein `py_compile`; keine Benutzerpfade in versionierten Dateien (CI „Datenschutz“).
- Aufeinander aufbauende Zweige gegen `main` mit **„Create a merge commit“** mergen. Nach einem Squash-Merge `origin/main` in den Folgezweig mergen und dessen geprüften Baum behalten (`git restore --source=<zweig> --staged --worktree :/`), dann normal pushen.
- `07_Python-Versionen` und der Lieferstand ändern sich nur in einer Produktionsrunde; die Grundstufe meldet Abweichungen dorthin als zulässigen Hinweis.
- OneDrive: Pfade kurz halten (Prüfkopien in `~/gq`), vor Befunden über fehlende Dateien einen Synchronisationsfehler ausschließen.

## 11. Einstieg für eine neue KI-Sitzung

1. [AGENTS.md](../AGENTS.md) und [CLAUDE.md](../../../CLAUDE.md) lesen.
2. Dieses Handbuch, dann [Shell-Konzept](GLIDE_SHELL_FRAMEWORK_KONZEPT.md) §6–§7 und D94–D98 in der [Arbeitsrichtung](ARBEITSRICHTUNG.md).
3. `SHELL_MODULE` in T319 als Schnittstellenvertrag; Quelltext des betroffenen Moduls **und seiner Glide-Aufrufer** (Funktionsnamen suchen).
4. Gezielte Prüfung aus §5, dann Grundstufe.
5. In Claude-Code-Sitzungen lädt der Projekt-Skill `glide-shell` (`.claude/skills/glide-shell/SKILL.md`) dieses Handbuch.
