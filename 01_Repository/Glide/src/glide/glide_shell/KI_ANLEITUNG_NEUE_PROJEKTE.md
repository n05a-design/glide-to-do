# Glide Shell – Anleitung für KI-Agenten in neuen Projekten

Stand 23.11.2026 · Glide 1.0.2 · Glide-System V1.86 · Glide Shell 0.6.2 · [English version](AI_GUIDE_NEW_PROJECTS.md)

Diese Anleitung richtet sich an KI-Agenten (Claude Code, Codex, Cursor, Gemini und andere), die mit der Glide Shell eine **neue** Tk-Desktopanwendung bauen. Sie erklärt den Aufbau von Glide, Glide-System und Glide Shell, den Start eines Projekts, die Architekturregeln, die Design-Richtlinien, die Arbeitsprozesse und die Prüfungen. Sie liegt im Paket `glide_shell` und wird bei jeder Übernahme mitkopiert. Einen fertigen Prompt für die erste Sitzung samt Übersicht, was wo liegt, enthält [`STARTPROMPT_KI.md`](STARTPROMPT_KI.md).

Führende Quellen bleiben in Glide; diese Anleitung fasst sie für Folgeprojekte zusammen und verlinkt sie. Bei Widerspruch gelten die verlinkten Glide-Dokumente. Glide-Repository: <https://github.com/n05a-design/glide-to-do> (im Folgenden `GLIDE`).

---

## 1. Das Gesamtbild

```text
Glide (die App)                 Glide-System (der Bestand)            Glide Shell (das Paket)
src/glide/app.pyw               src/glide/README.md                   src/glide/glide_shell/
ListApp = Controller            Register: Module M…, Features F…,     neutrale Tk-Bausteine,
Fachmodule (Tk-frei)            Bausteine, Tests T…, Versionsverlauf   keine Glide-Werte
Daten, Ansichten, Texte         GLIDE_SYSTEM_VERSION (V1.86)          SHELL_VERSION (0.6.2)
        │                                 │                                  ▲
        └──── nutzt ──────────────────────┼──────────── Host → Shell → Tk ───┘
                                          └─ dokumentiert beides, versioniert unabhängig
```

- **Glide** ist ein lokaler Desktop-Planer in Python/Tk. `ListApp` in `app.pyw` ist der Controller: Er baut Ansichten, hält den Bestand und reagiert auf Befehle. Fachlogik steckt in vielen kleinen, Tk-freien Modulen mit Unit-Tests.
- **Das Glide-System** ist kein Code, sondern das verbindliche Register aller Module, Features, Bausteine und Tests mit eigener Versionsnummer ([`src/glide/README.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/src/glide/README.md)). Jede Änderung an Modulen, Tests oder Katalog hebt `GLIDE_SYSTEM_VERSION` im selben Commit.
- **Die Glide Shell** ist das wiederverwendbare Tk-Fundament. Sie kennt keine Glide-Inhalte; Texte, Farben, Prüfungen und Handler liefert der Host. Neue Projekte übernehmen sie als Kopie.

Abhängigkeitsrichtung ohne Ausnahme: **Host → Shell → Tk/Standardbibliothek.** Die Shell importiert nie aus dem Host.

---

## 2. Bausteine der Shell

| Modul | Wofür | Wichtigste Namen | Host liefert |
|---|---|---|---|
| `app_host` | Hauptfenster starten und beenden (Phase 5) | `AppHost` (`before_tk`, `preflight`, `splash`, `on_ready`, `run`), `bind_shortcuts`, `primary_shortcuts`, `attach_menubar`, `install_close`, `platform_of` | Controller-Klasse, Startprüfungen, Kürzeltabelle, Schließhandler |
| `command_history` | Rückgängig/Wiederholen (Phase 4) | `Command`, `CommandHistory` (`execute`, `record`, `undo`, `redo_step`, `trim`, `clear`), `DONE`/`EMPTY`/`FAILED`/`HANDLED` | Befehlsobjekte oder `capture`/`apply`/`rollback` für Zustandsabbilder |
| `modal_session` | Dialoge erzeugen, modal warten, Fokus zurückgeben | `create_dialog`, `run_modal`, `wait_modal`, `modal_over` | Titel, Hintergrund, Fehlerprotokoll |
| `window_lifetime` | Zeitgeber gehören einem Widget | `scope_for`, `AfterScope` | das besitzende Widget |
| `motion` | kurze, unterbrechbare Übergänge (≤ 150 ms) | `Transitions`, `progress` | Zeitplanung aus dem Bereich |
| `custom_controls` | thementaugliche Canvas-Bedienelemente | `GlideCheckbutton`, `GlideRadiobutton`, `GlideListbox`, `GlideScale`, `ThemedAutoScrollbar` | Schrift, Tinte, Hintergrund über `set_*_provider` |
| `desktop_adapter` | Menübaum, Kürzeltexte, Plattform, Zwischenablage, Startweg | `build_menu_tree`, `format_accelerator`, `primary_modifier`, `launch_path` | Menüeinträge, Aktionskennungen, Beschriftungen |
| `window_geometry` | Geometrietexte, Fenster auf der Arbeitsfläche halten | `parse`, `format_geometry`, `clamp`, `keep_visible` | Mindestmaß |
| `system_appearance` | Hell/Dunkel des Systems | `tk_is_dark`, `windows_is_dark`, `linux_is_dark`, `resolve` | Designpaar |
| `redo_history` | Gültigkeit des Wiederholen-Stapels | `RedoHistory` | – (nutzt `command_history` intern) |
| `text_fit` | Text auf Zeichen-/Pixelbreite kürzen | `clip`, `fit`, `settled_wrap_width`, `aligned_markers` | Messfunktion |
| `action_picker` | durchsuchbare Aktionsauswahl aus einem Menü | `entries`, `search`, `grouped`, `first_enabled` | Menüzeilen, Platzhalter |
| `runtime_paths` | Daten- und Cacheordner ohne Seiteneffekt | `platform_data_dir`, `platform_cache_dir`, `resolve_base` | Produktname, Variablen-/Dateinamen |
| `selftest` | Prüfung der Kopie auf dem Zielrechner | `python -m glide_shell.selftest` | – |
| `demo` | lauffähiges Beispiel nur aus Shell-Bausteinen | `python -m glide_shell.demo` | – |

Die verbindliche Liste aller öffentlichen Funktionen mit Parameternamen steht in `SHELL_MODULE` in [`tests/unit/test_shell_importregel.py`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/tests/unit/test_shell_importregel.py) (T319).

---

## 3. Ein neues Projekt anlegen

### 3.1 Empfohlene Struktur (nach dem Muster von Glide)

```text
<projekt>/
  AGENTS.md                verbindliche Arbeitsregeln und Abschlusskriterium (Muster: Glide AGENTS.md)
  CLAUDE.md                Ergänzungen für Claude-Code-Sitzungen, verweist auf AGENTS.md
  VERSION                  App-Version (SemVer)
  SYSTEM_VERSION           Version des eigenen Registers (V1.0 zu Beginn)
  src/<app>/
    app.py                 Controller und Ansichten; Start über glide_shell.app_host
    <fach>.py              Tk-freie Fachmodule
    glide_shell/           unveränderte Kopie samt SHELL_MANIFEST.json
    resources/locales/     de.json, en.json (Texte des Hosts)
    README.md              Systemregister: Module M…, Features F…, Tests T…, Versionsverlauf
  tests/unit/              Tk-freie Tests, je Fachmodul einer
  tests/integration/       echte Tk-Suiten (eigene Prozesse, künstliche Daten)
  tests/tools/             Werkzeugtests, Grundstufe, Vollprüfung
  docs/
    ARBEITSRICHTUNG.md     Entscheidungen D01… mit Datum und Quelle
    ENTWICKLUNGSPLAN.md    einziger Aufgabenplan mit §-Abschnitten
    FUNKTIONEN.md          Verhalten aus Nutzersicht (führend für das Handbuch)
    DESIGN_RICHTLINIEN.md  Gestaltungsvertrag (Abschnitt 5)
    QA_BERICHT.md          tatsächliche Läufe mit Commit, Plattform und Grenzen
    DOKUMENTENPFLEGE.md    Pflegematrix: führende Quelle je Thema und Folgebezüge
  CHANGELOG.md
```

Nur anlegen, was das Projekt braucht; aber jede Aussage hat **genau eine führende Quelle**. Zusammenführen statt parallel pflegen.

### 3.2 Shell übernehmen

```bash
python3 -B <glide>/01_Repository/Glide/scripts/pflege/shell_uebernehmen.py <projekt>/src/<app>                          # anlegen oder aktualisieren
python3 -B <glide>/01_Repository/Glide/scripts/pflege/shell_uebernehmen.py --agenten-bootstrap <projekt>/src/<app>     # inklusive AGENTS.md und Agenten-Skills
python3 -B <glide>/01_Repository/Glide/scripts/pflege/shell_uebernehmen.py --agenten-bootstrap --projekt-root <root> <projekt>/src/<app>  # explizite Projektwurzel
python3 -B <glide>/01_Repository/Glide/scripts/pflege/shell_uebernehmen.py --commit <REV> <projekt>/src/<app>          # aus einem festen Git-Commit übernehmen
python3 -B <glide>/01_Repository/Glide/scripts/pflege/shell_uebernehmen.py --pruefen <projekt>/src/<app>                # nur prüfen
cd <projekt>/src/<app> && python3 -m glide_shell.selftest                                                              # Exitcode 0 = alle 13/13 Prüfungen bestanden
```

- Das Werkzeug kopiert alle `*.py` und `*.md` aus `glide_shell/` (inklusive `DESIGN_RICHTLINIEN.md` als offline-fähigem Gestaltungsvertrag) und schreibt `SHELL_MANIFEST.json` mit Paketversion, Glide-Systemversion, Quell-Commit und SHA-256 je Datei.
- **Projektwurzel-Erkennung:** Mit `--agenten-bootstrap` ermittelt das Werkzeug die Projektwurzel automatisch aufwärts anhand von Projektmarkern (`.git`, `pyproject.toml`, `setup.py`, `Pipfile`, `requirements.txt`, `AGENTS.md`, `CLAUDE.md`) oder Standard-Python-Layouts (`src/<app>/glide_shell`). Alternativ kann die Wurzel per `--projekt-root <PFAD>` bzw. `--project-root <PFAD>` explizit vorgegeben werden (eine Platzierung innerhalb des Glide-Quellbaums wird strikt abgewiesen).
- **Dynamische relative Links:** Die generierten `AGENTS.md` und Agenten-Skills (`.agents/skills/glide-shell/SKILL.md`, `.claude/skills/glide-shell/SKILL.md`) berechnen relative POSIX-Pfade dynamisch anhand der relativen Lage zur übernommenen `glide_shell/`-Kopie. Alle Markdown-Verweise lösen zuverlässig auf, auch in tief verschachtelten Projektbäumen und bei Pfaden mit Leerzeichen (`%20`).
- **Transaktionssicherheit & Schutz:** Der gesamte Übernahme- und Bootstrap-Prozess ist transaktionsgesichert (`BootstrapTransaction`). Vor Beginn der Mutation wird ein vollständiger Schnappschuss erstellt; bei Lese-, Schreib- oder Abbruchfehlern erfolgt ein automatischer Rollback aller erzeugten oder veränderten Dateien und Verzeichnisse ohne Teilzustände. Bestehende Dateien der Zielanwendung bleiben geschützt und werden nur mit `--ersetzen` überschrieben.
- **Manifest & Vertrauensgrenzen:** `SHELL_MANIFEST.json` dient als Integritätsanker. Der Selbsttest (`selftest.py`) prüft die SHA-256-Prüfsummen aller Module, erkennt unzulässige Modifikationen, gelöschte oder hinzugefügte unmanaged Dateien/Unterpakete und blockiert Symlinks. In Fremdkopien wird ein fehlendes Manifest zwingend mit Exitcode 1 abgewiesen; die quellinterne Ausnahmeregel ist manipulationssicher gegen vorgetäuschte Quellbäume abgesichert.
- **Die Kopie nie von Hand ändern.** Änderungen an der Shell entstehen in Glide (mit Freigabe des Glide-Inhabers) und kommen über das Werkzeug zurück. `--pruefen` meldet veraltete oder veränderte Dateien; `--ersetzen` überschreibt bewusst.
- Lizenz: MPL-2.0. Kopfzeile `# SPDX-License-Identifier: MPL-2.0` und Lizenztext `LICENSE` bleiben erhalten.

### 3.3 Gerüst einer Anwendung

```python
# src/<app>/app.py
import json
import os
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

from glide_shell import app_host, command_history, desktop_adapter, runtime_paths, window_lifetime

APP = "Beispiel"
TEXTS = json.loads((Path(__file__).parent / "resources/locales/de.json").read_text(encoding="utf-8"))


def t(key):
    return TEXTS.get(key, key)


def data_dir():
    # Kein Ordner wird beim Import angelegt; erst der Start entscheidet (Muster WA-49).
    base, _forced = runtime_paths.resolve_base(None, os.environ, "BEISPIEL_DATA_DIR",
                                               runtime_paths.platform_data_dir(APP))
    return Path(base)


def check_tk(_root):
    return None if tk.TkVersion >= 8.6 else (t("start.title"), t("start.tk_too_old"))


class Increment(command_history.Command):
    def __init__(self, app):
        self.app = app

    def execute(self):
        self.app.count += 1
        self.app.refresh()

    def undo(self):
        self.app.count -= 1
        self.app.refresh()


class App:
    """Controller: baut den Inhalt im Fenster des App-Hosts."""

    def __init__(self, root):
        self.root, self.count = root, 0
        self.scope = window_lifetime.scope_for(root)          # alle Zeitgeber dieses Fensters
        self.history = command_history.CommandHistory(limit=50)
        self.platform = app_host.platform_of(root.tk.call("tk", "windowingsystem"))
        root.title(t("app.title"))
        menus = []
        menubar = desktop_adapter.build_menu_tree(root, [
            (t("menu.edit"), [
                (t("menu.undo"), self.undo, desktop_adapter.format_accelerator("Z"), "undo"),
                (t("menu.redo"), self.redo, desktop_adapter.format_redo_accelerator(), "redo"),
            ]),
        ], menus_out=menus)
        app_host.attach_menubar(root, menubar)
        app_host.bind_shortcuts(root, app_host.primary_shortcuts("z", lambda _e: self.undo(), self.platform)
                                + app_host.primary_shortcuts("Z", lambda _e: self.redo(), self.platform, shift=True)
                                + [("<Escape>", lambda _e: self.request_close(), app_host.ALL)],
                                self.platform)
        app_host.install_close(root, self.request_close, self.platform, scope=self.scope)
        self.label = tk.Label(root)
        self.label.pack(padx=20, pady=20)
        tk.Button(root, text=t("action.add"), command=lambda: self.history.execute(Increment(self))).pack()
        self.refresh()

    def refresh(self):
        self.label.configure(text=t("count").format(count=self.count))

    def undo(self):
        return self.history.undo() == command_history.DONE

    def redo(self):
        return self.history.redo_step() == command_history.DONE

    def request_close(self):
        # Offene Änderungen hier abfragen: Dialog über modal_session.create_dialog
        # aufbauen und mit modal_session.run_modal(self.root, dialog) warten.
        self.root.destroy()


def main():
    host = app_host.AppHost(
        before_tk=(),                                   # z. B. private Schriften registrieren (vor dem ersten Tk!)
        preflight=(check_tk,),                          # (titel, meldung) bricht mit Exitcode 1 ab
        show_error=lambda title, message, parent=None: messagebox.showerror(title, message, parent=parent))
    host.run(App)


if __name__ == "__main__":
    main()
```

Für Zustandsabbilder statt Befehlen (wie Glide): `CommandHistory(capture, apply, rollback, stack=lambda: self.undo_stack)`; `apply(state)` meldet `True` nur nach erfolgreichem Speichern, sonst stellt `rollback` den Arbeitsspeicher wieder her und beide Stapel bleiben unverändert. Ein Beispiel ist Glides `ListApp.command_history` in `app.pyw`.

---

## 4. Architekturregeln

Diese Regeln stammen aus Glide und sind dort durch Tests erzwungen. Übernimm sie mit eigenen Tests.

1. **Fachlogik ist Tk-frei und hat Unit-Tests** (Glide D17). Neue oder angefasste Logik lebt in eigenen Modulen ohne `tkinter`; der Controller ruft sie auf.
2. **Modulbudget** (Glide WA-50): je Funktion höchstens 50 Codezeilen, Verschachtelungstiefe höchstens 15. In Glide prüft das `tests/tools/analyse_statisch.py --budget` mit T322.
3. **Import ohne Seiteneffekte** (Glide WA-49): Der Import legt keine Ordner an, ändert kein Tk-Verhalten und liest keine Zeigerdateien. Das alles passiert beim Start im Controller oder in `AppHost`.
4. **Start über `AppHost`.** Schritte, die vor dem ersten Tk-Interpreter passieren müssen (private Schriften unter macOS Aqua, Windows-Anwendungskennung), gehören in `before_tk`. Prüfungen von Laufzeit und Datenordner gehören in `preflight`; sie melden und beenden, bevor Daten geöffnet werden.
5. **Ein zweites `tk.Tk()` im selben Prozess vermeiden.** Unter macOS ist es nicht stabil (Exitcode 133 beobachtet). Was vor dem Fenster laufen muss, gehört in einen eigenen Prozess (Muster: Glides Showcase-Starter).
6. **Zeitgeber nur über einen Bereich** (`window_lifetime.scope_for(widget).after(…)`). Beim Abbau des Widgets endet alles; ein roher `root.after` ist ein Fehler. Glide hält das mit einer Sperrklinke in T319 fest.
7. **Dialoge nur über `modal_session`** (`create_dialog`, `run_modal`). Kein eigener `wait_window`, kein roher `Toplevel` außer Tooltips.
8. **Bewegung ≤ 150 ms, unterbrechbar** (`motion.Transitions` im selben Bereich). Bewegungsreduktion nimmt die Bewegung, nie die Funktion.
9. **Rückgängig über `CommandHistory`.** Ein Schritt pro Nutzerabsicht; ein gescheitertes Speichern lässt beide Stapel unverändert und meldet den Fehler.
10. **Daten lokal, atomar und gesichert.** Schreiben über Temporärdatei und `os.replace`, Vorsicherung vor Migrationen, Schreibsperre für den Datenordner. Glides Muster: `persistence.py`, `data_lock.py`, `schema_backups.py` (keine Shell-Bausteine; als Vorlage lesen, nicht importieren).
11. **Texte gehören dem Host.** Shell-Bausteine bekommen fertige Beschriftungen. Lokalisierung über Kataloge `de.json`/`en.json` mit Paritätstest (Muster: Glide `i18n.py`, T329, T335). Entwicklermeldungen im Code auf Englisch.
12. **Kein Code aus `glide`-Modulen außerhalb der Shell importieren.** Wer einen weiteren Glide-Baustein braucht, beantragt ihn in Glide als neuen Shell-Baustein (Abschnitt 9).

---

## 5. Design-Richtlinien

Glides Gestaltungsvertrag und der verbindliche transportable Rahmen für Folgeprojekte stehen in [`docs/DESIGN_RICHTLINIEN.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md) (siehe Abschnitt [*Portabler Designvertrag für Folgeprojekte*](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md#portabler-designvertrag-für-folgeprojekte)). Übernimm die Grundsätze in ein eigenes `DESIGN_RICHTLINIEN.md` des Projekts; konkrete Glide-Maße und -Entscheidungen gelten nur, wenn dein Projekt sie ausdrücklich übernimmt.

**Sechs Grundsätze (P1–P6):**

| Grundsatz | Bedeutung für die Oberfläche |
|---|---|
| P1 Funktioniert selbstverständlich | Die naheliegende Handlung führt ohne Hinweistext zum Ziel; Systemkonventionen (Hell/Dunkel, Esc, Entf, Kürzel) gelten |
| P2 Form folgt Funktion | Farbe = Rolle, Größe = Wichtigkeit, Position = Zusammenhang; keine Dekoration im Standard |
| P3 Keine Funktion doppelt | Je Absicht ein primärer Weg; Menü, Kürzel und Aktionsauswahl spiegeln ihn (`action_picker` liest das Menü, keine zweite Befehlsliste) |
| P4 Kein Platz verschwenden | Inhalt vor Bedienung; Bedienfläche über dem Inhalt höchstens 15 % bei 1280 × 800 |
| P5 Nur das Wesentliche | Der Standard zeigt das Nötige; Kopfzeile höchstens vier Symbolknöpfe |
| P6 Geringe Komplexität | Wenige stabile Begriffe; Neues erweitert bestehende Orte |

**Verbindliche Vorgaben, die jedes Projekt braucht:**

- **Bedienelemente schützen (B15):** Jeder Knopf bleibt in allen vorgesehenen Fenstergrößen sichtbar, lesbar und erreichbar; Texte dürfen ihn nicht überdecken. Positionen nach jedem Neuumbruch neu berechnen.
- **Informationshierarchie (B11):** Titel und Inhalt verschwinden zuletzt; Metadaten sind so breit wie ihr Inhalt und weichen bei Enge ganz, statt abgeschnitten zu werden.
- **Fluchten (B02, B05, B07–B09):** Zusammengehöriges teilt Kanten, Abstände und Höhen; Symbolmitte auf der Mitte der Großbuchstabenhöhe, gerechnet aus Glyphenrahmen, nicht aus festen Pixelversätzen.
- **Stabile Symbole (B10, B12, B14):** Ein Symbol, eine Bedeutung; ◂/▸ blättern, ▸/▾ klappen; Zeichen aus der verwendeten Schrift oder einer mitgelieferten Symbolschrift.
- **Ruhige Flächen (B17, B19):** Elemente übernehmen die Farbe ihrer Trägerfläche; keine zufälligen Hintergrundrechtecke.
- **Hinweise bei Bedarf (B06):** Ergänzende Hilfen sind abschaltbar; notwendige Zustände und Fehler bleiben immer sichtbar.
- **Vorhersehbar reagieren (B01, B16):** Rückmeldung im selben Ereignis, keine künstlichen Wartezeiten, gleichmäßiges Scrollen.
- **Kurze Umschaltbefehle:** „Kompaktmodus“, nicht „Kompaktmodus ein/aus“.
- **Aus der Marktanalyse (D83):** Leerer Bereich erklärt sich in einem Satz mit einem Knopf; ändernde Sammeldialoge zeigen Vorher/Nachher und sind in einem Schritt rücknehmbar; Summen in den Abschnittskopf; Überfälliges neutral benennen; Zeit sichtbar, nicht alarmierend.
- **Worst-Case-Daten prüfen:** lange Titel, fehlende und lange Metadaten, leere und volle Zustände, große Schrift, kleinste Fenstergröße.

**Nachweis je angefasstem UI-Paket:** Vor der Umsetzung die betroffenen Regeln nennen; danach echte Screenshots und Geometrieprüfung mit künstlichen Daten in mindestens zwei Fenstergrößen (Glide: 860 × 700 und 1280 × 800), mittlerer und großer Schrift, hellem und dunklem Design, langen Texten. Screenshots und Attribute ersetzen keine menschliche Sicht- und Bedienabnahme.

---

## 6. Arbeitsprozesse

### 6.1 Auftrag, Entscheidungen, Plan

- **Nur beauftragte Arbeit umsetzen.** Offene Produktauswahl trifft der Inhaber, nicht der Agent. Eine Entscheidungsvorlage nennt Optionen, Empfehlung und Aufwand.
- **Entscheidungen** stehen nummeriert in `ARBEITSRICHTUNG.md` (D01, D02 …) mit Datum, Quelle und Umsetzungsort. Wird der Bereich größer, Bereichsangaben wie „D01–D12“ in allen Einstiegen mitziehen.
- **Ein einziger Aufgabenplan.** Jeder Schnitt bekommt einen Abschnitt mit **A – Auftrag**, **B – Umsetzung**, **C – Prüfung**, **D – Rest**. Statusmarken: ✅ erledigt, ◐ teilweise, ○ offen, ◇ registriert. Ein ✅ nur mit Prüfbeleg.

### 6.2 Versionen

| Zähler | Wann erhöhen |
|---|---|
| App-Version (`VERSION`) | nur in einer Produktionsrunde (Versionswechsel, Lieferabgleich, Prüfsummen) |
| Register-Version (`SYSTEM_VERSION`) | jeder Schnitt mit neuem Modul, neuem Test oder geändertem Katalog; Datei und Registerkopf im selben Commit |
| Datenformat | nur mit Migration, Vorsicherung, Altleser-Test und Fixtures im selben Schnitt |
| `SHELL_VERSION` der Kopie | nie im Projekt; kommt mit der Übernahme |

### 6.3 Dokumentation

- **Pflegematrix:** Für jedes Thema eine führende Quelle und die Folgebezüge, die bei Änderungen mitgehen (Muster: Glide [`docs/DOKUMENTENPFLEGE.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/DOKUMENTENPFLEGE.md)).
- **Jede aktive Datei trägt eine Standzeile** `Stand TT.MM.JJJJ · <App> <Version> · …`; historische Belege behalten ihre Stände. Glides `tests/tools/standpruefung.py` prüft das und lässt sich anpassen.
- **Interne Dokumente auf Deutsch, öffentliche Texte zweisprachig** (README, Benutzerhandbuch, Issue- und Release-Texte), wenn das Projekt es so festlegt. Das englische Handbuch ist eine kontrollierte Übersetzung der führenden Funktionsbeschreibung und nennt Bedienelemente mit den Beschriftungen der Kataloge.
- **QA-Bericht nur mit tatsächlichen Läufen:** Commit, Plattform, Python/Tk-Version, Befehl, Ergebnis, Grenzen. „Vorhanden“ ist nicht „getestet“, „getestet“ ist nicht „abgenommen“.

### 6.4 Git

- Topic-Zweige, Pull Requests, Merge nach grüner CI. Aufeinander aufbauende Zweige mit Merge-Commit zusammenführen, nicht per Squash.
- **Keine Force-Pushes, keine Tags, Releases, Paketmanager-Einreichungen oder Veröffentlichungen ohne ausdrückliche Freigabe des Inhabers.**
- Vor jedem `git add` den Status prüfen; nie blind `git add -A`. Geschützte lokale Pfade des Projekts nie stagen.
- Keine Benutzerpfade, keine echten Nutzerdaten, keine Rohprotokolle (`*.log`) in versionierten Dateien. Glides `scripts/pflege/pfade_bereinigen.py --pruefen` findet Benutzerpfade.
- `__pycache__` vor Prüfläufen und Commits entfernen.

---

## 7. Prüfungen

### 7.1 Grundregeln

- **Nie echte Nutzerdaten.** Jeder Test setzt einen eigenen Datenordner über die Umgebungsvariable des Projekts (Glide: `GLIDE_DATA_DIR`), bevor er die App importiert. Werkzeuge mit `python3 -B` starten.
- **GUI-Suiten nie parallel** und nie im Hintergrund, wenn sie Tastaturfokus brauchen. Unter macOS mit gesperrtem Bildschirm liefert ein App-Wechsel kein FocusOut; Fokusfälle erst bei entsperrtem Bildschirm werten.
- **Ergebnisse kennzeichnen:** Plattform, Tk-Version, „künstliche Daten“. Ein Linux-Container ersetzt keine macOS- oder Windows-Abnahme.

### 7.2 Stufen

| Stufe | Inhalt | Muster in Glide |
|---|---|---|
| Unit | Tk-freie Fachmodule, Kataloge, Register | `tests/unit/*` |
| Integration | echte Tk-Fenster, eigener Prozess je Suite, Gegenproben | `tests/integration/*`, z. B. Modal-, Abbau- und Fensterlebensdauervertrag |
| Werkzeuge | Stand-, Link-, Ablage-, Lizenz- und Registerprüfung | `tests/tools/*` |
| Grundstufe | alles Schnelle in einem Lauf, auch in der CI | `tests/tools/ci_grundstufe.py --protokoll <Ordner>` |
| Vollprüfung | alle Suiten nacheinander mit Zeitgrenze und Folgestopp | `tests/tools/pruefen.py --modus voll --vordergrund --protokoll <Ordner>` |
| Paket | Bau, isolierter Start ohne externes Python, Prüfsummen | `packaging/paket/baue_und_pruefe_macos.sh`, DMG mit `hdiutil verify` |

### 7.3 Shell-Prüfungen im Projekt

```bash
cd <projekt>/src/<app>
python3 -m glide_shell.selftest          # 13/13 checks passed
python3 -O -m glide_shell.selftest       # muss dasselbe melden
python3 -m glide_shell.demo              # Sichtprobe des Nutzungsmusters
```

Übernimm zusätzlich drei Vertragstests nach Glides Muster für den eigenen Controller: Start (alle Einstiege gegen leeren, vorhandenen, gesperrten und beschädigten Datenordner), Abbau (nach dem Schließen keine offenen Zeitgeber) und Modal (Griff, Fokus, verschachtelte Dialoge).

### 7.4 Abschlusskriterium eines Schnitts

1. Gezielte Tests der geänderten Stelle grün.
2. Grundstufe grün.
3. Register, Versionen, Plan, QA-Bericht, CHANGELOG und Folgebezüge der Pflegematrix nachgeführt.
4. Vor dem Phasenende eine Vollprüfung (Glide D51).
5. Offene Punkte ehrlich im Abschnitt **D – Rest**; nichts als erledigt markieren, was nur begonnen ist.

---

## 8. Das Glide-System im eigenen Projekt weiterbenutzen

- **Eigenes Register nach Glides Format:** Tabelle der Module (`M001 | Datei | Zweck | Schnittstelle | Tests`), Features (`F001 …`), Bausteinpakete, Tests (`T001 …`) und ein Versionsverlauf mit Datum und Bezug zur App-Version. Ein Werkzeugtest prüft, dass Register und Dateibestand übereinstimmen (Muster: `tests/tools/test_glide_system.py`).
- **Bausteine außerhalb der Shell** (Persistenz, Sicherungen, Import/Export, Planung, Wiederholungsregeln …) stehen im Übernahmevertrag von Glide: [`src/glide/README.md` §9](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/src/glide/README.md#9-grundlage-für-steps-und-weitere-projekte). Sie sind **keine freigegebene Bibliothek**: Wer einen davon übernimmt, kopiert ihn mit Herkunft (Glide-Commit, Lizenz), passt Namen, Pfade und Datenmodell an und belegt ihn mit eigenen Tests.
- **Werkzeuge** wie Standprüfung, Ablagegröße, Pfadbereinigung, statische Analyse und die Vollprüfung enthalten Glide-Pfade und -Namen. Vor der ersten Ausführung im Projekt anpassen und mit einer Gegenprobe zeigen, dass sie Fehler finden.
- **Keine Freigaben übernehmen:** Glides Entscheidungen, Signaturen, Abnahmen und Releasefreigaben gelten nicht automatisch für ein neues Projekt.

---

## 9. Änderungen an der Shell

Braucht dein Projekt etwas, das die Shell nicht hat:

1. Nicht in der Kopie ändern. Im Projekt mit einem eigenen Modul lösen oder in Glide einen neuen Baustein vorschlagen.
2. Ein neuer Shell-Baustein braucht eine Freigabe des Glide-Inhabers (Entscheidung D…) und folgt der Prüfliste im [KI-Handbuch der Shell §9](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/GLIDE_SHELL_KI_HANDBUCH.md): neutraler Teil in `glide_shell/<name>.py`, Kopfzeile `Shell-Paket N:`, englische Laufzeitmeldungen, `SHELL_MODULE` in T319, Verhaltenstest, `SHELL_VERSION` anheben, Selbsttest, Dateilisten für Lieferabgleich und Paketbau, Doku.
3. Danach im Projekt mit dem Übernahmewerkzeug aktualisieren und den Selbsttest ausführen.

Kompatibilitätsnamen mit `glide` (`_glide_after_scope`, `GlideCheckbutton` …) bleiben bewusst; nicht umbenennen.

---

## 10. Prüflisten

**Projektstart**

- [ ] Struktur aus 3.1 angelegt; `AGENTS.md` mit Arbeitsregeln und Abschlusskriterium
- [ ] Shell übernommen, `SHELL_MANIFEST.json` vorhanden, Selbsttest 13/13 (auch mit `-O`)
- [ ] Start über `AppHost` mit `preflight`; Import ohne Seiteneffekte
- [ ] Datenordner über `runtime_paths` und eigene Umgebungsvariable für Tests
- [ ] Kataloge `de.json`/`en.json` mit Paritätstest; Entwicklermeldungen Englisch
- [ ] Register mit V1.0, Plan, Entscheidungen, Design-Richtlinien, QA-Bericht, Pflegematrix

**Jedes Feature**

- [ ] Auftrag und betroffene Entscheidungen/Design-Regeln genannt
- [ ] Fachlogik Tk-frei mit Unit-Test; Modulbudget eingehalten
- [ ] Zeitgeber über Bereich, Dialoge über `modal_session`, Rückgängig über `CommandHistory`
- [ ] Texte in beiden Katalogen; Bedienelemente geschützt; Worst-Case-Daten geprüft
- [ ] Register, Systemversion, Plan (A/B/C/D), CHANGELOG, QA-Bericht nachgeführt

**Vor dem Pull Request**

- [ ] Gezielte Tests und Grundstufe grün; GUI-Suiten nacheinander
- [ ] Keine Benutzerpfade, keine echten Daten, kein `__pycache__`, keine geschützten Pfade
- [ ] PR-Beschreibung nennt Prüfungen, Plattform und offene Grenzen

**Release** (nur mit Freigabe)

- [ ] Produktionsrunde: Versionswechsel, Lieferabgleich, Prüfsummen
- [ ] Vollprüfung, Paketbau, isolierter Start, Abbild geprüft
- [ ] Tag, Release, Signatur, Notarisierung und Einreichungen erst nach ausdrücklicher Freigabe

---

## 11. Stolperstellen aus Glide

- **macOS Aqua** legt den Schriftbestand beim ersten `Tk()` fest: private Schriften in `before_tk` registrieren.
- **Zweites `Tk()`** im selben Prozess stürzt unter macOS ab: Vorarbeit in einen Kindprozess.
- **Cmd+Q** umgeht unter macOS `WM_DELETE_WINDOW`: immer `install_close` verwenden; das Beenden läuft im Leerlauf.
- **Command-Modifikator** ist unter Windows Num-Lock: Cmd-Kürzel nur mit Plattform `MACOS` binden (`bind_shortcuts`).
- **Tk 9.1** navigiert in Treeviews über virtuelle Ereignisse, die auch Emacs-Kürzel auslösen; eigene Strg-Kürzel in Listen gegen die Klassenbindung schützen.
- **Bytecode** nicht in den Quellbaum schreiben (`sys.pycache_prefix` vor dem ersten eigenen Import setzen); sonst schlagen Startweg-Prüfungen fehl.
- **Feste Versionswerte in Tests** brechen beim Versionswechsel: Version aus `VERSION` lesen, Release-Reihenfolge statt Zahlenvergleich.
- **Lange Pfade** (OneDrive, Windows ohne Langpfade): Prüfkopien und Temp in kurzen lokalen Ordnern.
- **Gesperrter Bildschirm** verfälscht Fokusprüfungen: Vollprüfungen im Vordergrund mit entsperrtem Bildschirm.

---

## 12. Weiterlesen

| Thema | Quelle in Glide |
|---|---|
| Arbeitsregeln | [`AGENTS.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/AGENTS.md) |
| Shell für Agenten, die an der Shell arbeiten | [`docs/GLIDE_SHELL_KI_HANDBUCH.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/GLIDE_SHELL_KI_HANDBUCH.md) |
| Shell-Grenzen und Phasen | [`docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md) |
| Architektur | [`docs/02_ARCHITECTURE.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/02_ARCHITECTURE.md) |
| Design | [`docs/DESIGN_RICHTLINIEN.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md) (Abschnitt *Portabler Designvertrag*) |
| Entscheidungen | [`docs/ARBEITSRICHTUNG.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/ARBEITSRICHTUNG.md) |
| Prüfplan und QA | [`docs/05_QA_TESTPLAN.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/05_QA_TESTPLAN.md), [`docs/07_QA_BERICHT.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/07_QA_BERICHT.md) |
| Register und Übernahmevertrag | [`src/glide/README.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/src/glide/README.md) |
| Dokumentenpflege | [`docs/DOKUMENTENPFLEGE.md`](https://github.com/n05a-design/glide-to-do/blob/main/01_Repository/Glide/docs/DOKUMENTENPFLEGE.md) |
