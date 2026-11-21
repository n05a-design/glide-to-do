# SPDX-License-Identifier: MPL-2.0
"""Zentrale Liste der Shell-Module und ihre Importregel (D86, ohne Tk-Import).

Die Shell liegt seit D95 als Unterpaket `src/glide/glide_shell` neben den
Glide-Modulen. Was zur Shell gehört, steht hier in `SHELL_MODULE`. Jedes
dieser Module darf nur die Standardbibliothek, `tkinter` und andere
Shell-Module importieren und keinen Glide-Wert kennen
(Abhängigkeitsrichtung Host → Shell → Tk). Ein Modul, das sich im Kopf als
Shell-Paket ausweist, muss in der Liste stehen.

Der Test liest die Quellen nur als Syntaxbaum. Das Verhalten prüfen
`tests/integration/test_modalvertrag.py` und
`tests/integration/test_fensterlebensdauer.py`.
"""
import ast
from pathlib import Path
import re
import sys
import unittest

SRC = Path(__file__).resolve().parents[2] / "src" / "glide"
# Seit D95 liegt die Shell als Unterpaket `glide_shell` neben den Glide-Modulen.
SHELL = SRC / "glide_shell"
PAKET = "glide_shell"

# Modul: öffentliche Schnittstelle (Funktion oder Klasse.Methode: Parameter ohne self)
SHELL_MODULE = {
    "modal_session": {
        "modal_over": ["root", "parent"],
        "remember_focus": ["root", "dialog", "parent"],
        "return_focus": ["root", "dialog", "remembered"],
        "wait_modal": ["root", "dialog", "parent", "log_error"],
        "create_dialog": ["parent", "title", "background", "transient", "withdrawn", "resizable", "minsize"],
        "run_modal": ["root", "dialog", "parent", "background", "max_screen_share", "log_error"],
    },
    "window_lifetime": {
        "AfterScope.__init__": ["widget", "close_on_destroy"],
        "AfterScope.after": ["delay_ms", "callback"],
        "AfterScope.after_idle": ["callback"],
        "AfterScope.adopt": ["job"],
        "AfterScope.pending": [],
        "AfterScope.cancel": ["job"],
        "AfterScope.cancel_all": [],
        "AfterScope.close": [],
        "scope_for": ["widget"],
        "pending_jobs": ["widget"],
    },
    "custom_controls": {
        "rounded_rect_points": ["x1", "y1", "x2", "y2", "radius"],
        "bind_resize": ["widget", "callback", "add"],
        "paint_canvas_backdrop": ["canvas"],
        "set_font_provider": ["provider"],
        "set_ink_provider": ["provider"],
        "set_backdrop_painter": ["painter"],
        "CanvasLabel.set_halo": ["farbe"],
        "CanvasLabel.set_contrast_fg": ["farbe"],
        "CanvasLabel.text_size": [],
        "GlideCheckbutton.select": [],
        "GlideCheckbutton.deselect": [],
        "GlideCheckbutton.toggle": [],
        "GlideCheckbutton.invoke": [],
        "GlideRadiobutton.select": [],
        "GlideListbox.size": [],
        "GlideListbox.curselection": [],
        "GlideListbox.activate": ["index"],
        "GlideListbox.see": ["index"],
        "GlideScale.get": [],
        "GlideScale.set": ["value", "invoke_command"],
        "ThemedAutoScrollbar.set_command": ["command"],
        "ThemedAutoScrollbar.set_theme": ["bg_color", "track_color", "thumb_color", "active_thumb_color"],
        "ThemedAutoScrollbar.set": ["first", "last"],
        "ThemedAutoScrollbar.is_scrollable": [],
    },
    "motion": {
        "progress": ["elapsed", "duration_ms"],
        "Transitions.__init__": ["schedule", "unschedule", "clock"],
        "Transitions.start": ["key", "update", "finish", "enabled", "duration_ms"],
        "Transitions.cancel": ["key"],
        "Transitions.close": [],
    },
    "window_geometry": {
        "parse": ["geometry"],
        "format_geometry": ["width", "height", "x", "y"],
        "clamp": ["width", "height", "x", "y", "screen_width", "screen_height", "minimum", "origin"],
        "keep_visible": ["x", "y", "width", "bounds", "margin"],
    },
    "system_appearance": {
        "resolve": ["auto", "system_dark", "current"],
        "windows_is_dark": ["read_value"],
        "linux_is_dark": ["color_scheme", "gtk_theme"],
        "tk_is_dark": ["answer"],
    },
    "redo_history": {
        "RedoHistory.__init__": ["limit"],
        "RedoHistory.note_write": [],
        "RedoHistory.clear": [],
        "RedoHistory.mark": ["undo_stack"],
        "RedoHistory.validate": ["undo_stack"],
        "RedoHistory.peek": [],
        "RedoHistory.push": ["entry", "undo_stack"],
        "RedoHistory.pop": [],
        "RedoHistory.restore": ["entry"],
    },
    "selftest": {
        "check_version": ["_root"],
        "check_geometry": ["root"],
        "check_appearance": ["root"],
        "check_redo": ["_root"],
        "check_scope_and_motion": ["root"],
        "check_controls": ["root"],
        "check_modal": ["root"],
        "run": ["out"],
    },
    "demo": {
        "DemoHost.__init__": ["root", "texts", "colors", "geometry"],
        "DemoHost.place": ["geometry"],
        "DemoHost.add": [],
        "DemoHost.undo_step": [],
        "DemoHost.redo_step": [],
        "system_dark": ["root"],
        "DemoHost.tick": [],
        "DemoHost.open_dialog": [],
        "DemoHost.pulse": [],
        "DemoHost.close": [],
        "main": [],
    },
    "desktop_adapter": {
        "is_macos": [],
        "is_windows": [],
        "is_linux": [],
        "platform_name": [],
        "primary_modifier": ["macos_override", "modifier_labels"],
        "format_accelerator": ["macos_override", "modifier_labels"],
        "format_redo_accelerator": ["windows_override", "macos_override", "modifier_labels"],
        "build_menu_tree": ["parent", "entries", "menus_out", "tearoff", "attr_target", "action_resolver"],
        "DesktopMenuBar.create_menubar_frame": ["parent", "bg_color"],
        "DesktopMenuBar.post_popup_menu": ["button", "menu", "previous_focus", "restore_cb"],
        "launch_path": ["path", "windows_override", "macos_override"],
        "copy_to_clipboard": ["widget", "text"],
        "read_from_clipboard": ["widget"],
    },
}
KENNZEICHEN = "Shell-Paket"
VERBOTENE_NAMEN = {"__import__", "importlib", "ListApp"}
VERBOTENE_ANFAENGE = ("glide_", "APP_", "ERROR_LOG", "THEMES", "theme")


def baum(modul):
    quelle = SHELL / f"{modul}.py"
    return ast.parse(quelle.read_text(encoding="utf-8"), filename=str(quelle))


def importe(tree):
    namen = set()
    for knoten in ast.walk(tree):
        if isinstance(knoten, ast.Import):
            namen.update(alias.name.split(".")[0] for alias in knoten.names)
        elif isinstance(knoten, ast.ImportFrom):
            namen.add("." * knoten.level + (knoten.module or "").split(".")[0])
    return namen


def bezeichner(tree):
    """Alle Bezeichner im Code; Docstrings und Kommentare zählen nicht."""
    gefunden = set()
    for knoten in ast.walk(tree):
        if isinstance(knoten, ast.Name):
            gefunden.add(knoten.id)
        elif isinstance(knoten, ast.Attribute):
            gefunden.add(knoten.attr)
    return gefunden


def parameter(funktion):
    args = funktion.args
    return [a.arg for a in args.posonlyargs + args.args + args.kwonlyargs if a.arg != "self"]


class Modulliste(unittest.TestCase):
    def test_jedes_gelistete_modul_existiert(self):
        for modul in SHELL_MODULE:
            self.assertTrue((SHELL / f"{modul}.py").is_file(), modul)
            self.assertFalse((SRC / f"{modul}.py").exists(), f"{modul}: flache Kopie neben dem Paket")

    def test_gekennzeichnete_module_stehen_in_der_liste(self):
        gekennzeichnet = set()
        for quelle in sorted(SRC.glob("*.py")) + sorted(SHELL.glob("*.py")):
            kopf = ast.get_docstring(ast.parse(quelle.read_text(encoding="utf-8"))) or ""
            if kopf and KENNZEICHEN in kopf.splitlines()[0]:
                gekennzeichnet.add(quelle.stem)
        self.assertEqual(gekennzeichnet, set(SHELL_MODULE))


class Importregel(unittest.TestCase):
    def test_nur_standardbibliothek_tkinter_und_shell(self):
        for modul in SHELL_MODULE:
            for name in importe(baum(modul)):
                with self.subTest(modul=modul, importiert=name):
                    self.assertFalse(name.startswith("."), "Shell-Module importieren einander absolut über glide_shell")
                    self.assertTrue(name in sys.stdlib_module_names or name in SHELL_MODULE or name == PAKET, name)

    def test_keine_glide_bezeichner_und_kein_dynamischer_import(self):
        for modul in SHELL_MODULE:
            for name in bezeichner(baum(modul)):
                with self.subTest(modul=modul, name=name):
                    self.assertNotIn(name, VERBOTENE_NAMEN)
                    self.assertFalse(name.startswith(VERBOTENE_ANFAENGE))

    def test_kein_glide_modul_wird_ueber_umwege_geladen(self):
        """Auch Zeichenketten wie `import_module("…")` sind in der Shell nicht vorgesehen."""
        for modul in SHELL_MODULE:
            for knoten in ast.walk(baum(modul)):
                if isinstance(knoten, ast.Call):
                    with self.subTest(modul=modul):
                        self.assertNotIn(ast.unparse(knoten.func), {"exec", "eval", "import_module"})


DEUTSCH = re.compile(r"[äöüÄÖÜß]|\b(der|die|das|und|nicht|kein|keine|fehlt|Fehler|ungültig)\b")


class Entwicklermeldungen(unittest.TestCase):
    """D96: Laufzeittexte der Shell für Entwickler sind Englisch.

    Geprüft werden alle Zeichenketten im Code außer Docstrings; Kommentare
    und Docstrings bleiben in der Projektsprache. Sichtbare Texte liefert
    der Host als Argument.
    """

    def test_keine_deutschen_zeichenketten_ausser_docstrings(self):
        for modul in SHELL_MODULE:
            tree = baum(modul)
            docs = {id(k.body[0].value) for k in ast.walk(tree)
                    if isinstance(k, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
                    and k.body and isinstance(k.body[0], ast.Expr) and isinstance(k.body[0].value, ast.Constant)}
            for knoten in ast.walk(tree):
                if isinstance(knoten, ast.Constant) and isinstance(knoten.value, str) and id(knoten) not in docs:
                    with self.subTest(modul=modul, zeile=knoten.lineno):
                        self.assertIsNone(DEUTSCH.search(knoten.value), knoten.value[:80])

    def test_gegenprobe_erkennt_deutsche_meldung(self):
        probe = ast.parse('def f():\n    """Doku auf Deutsch."""\n    raise ValueError("Rolle fehlt")\n')
        texte = [k.value for k in ast.walk(probe) if isinstance(k, ast.Constant) and isinstance(k.value, str)]
        self.assertTrue(any(DEUTSCH.search(t) for t in texte[1:]))


class Schnittstelle(unittest.TestCase):
    def test_oeffentliche_namen_und_parameter(self):
        for modul, erwartet in SHELL_MODULE.items():
            vorhanden = {}
            for knoten in baum(modul).body:
                if isinstance(knoten, ast.FunctionDef):
                    vorhanden[knoten.name] = parameter(knoten)
                elif isinstance(knoten, ast.ClassDef):
                    for teil in knoten.body:
                        if isinstance(teil, ast.FunctionDef):
                            vorhanden[f"{knoten.name}.{teil.name}"] = parameter(teil)
            for name, args in erwartet.items():
                with self.subTest(modul=modul, name=name):
                    self.assertIn(name, vorhanden)
                    self.assertEqual(vorhanden[name], args)

    def test_zeitgeberbereich_nennt_sein_attribut(self):
        werte = {}
        for knoten in baum("window_lifetime").body:
            if isinstance(knoten, ast.Assign) and isinstance(knoten.value, ast.Constant):
                for ziel in knoten.targets:
                    werte[ziel.id] = knoten.value.value
        self.assertEqual(werte.get("SCOPE_ATTRIBUTE"), "_glide_after_scope")


# Sperrklinke der Restkopplung (D94, 20.11.2026): Diese Zahlen dürfen nur
# sinken. Wer einen Dialog auf `create_dialog` oder einen Zeitgeber auf einen
# `AfterScope` umstellt, senkt die Grenze im selben Commit; neue direkte
# Fenster oder Zeitgeber ohne Bereich lässt der Test nicht zu. Im Bereich ist
# ein Zeitgeber über `after_scope()` oder `scope_for(...)` oder direkt in
# `_register_after(...)` bzw. `.adopt(...)` (R2, V1.61).
RESTKOPPLUNG = {
    # Einzig der Tooltip (`overrideredirect`) ist kein Dialog und bleibt direkt (R4, V1.62).
    "direkte tk.Toplevel": 1,
    "Zeitgeber ohne AfterScope": 0,
}


def restkopplung(pfad):
    zahlen = dict.fromkeys(RESTKOPPLUNG, 0)
    baum = ast.parse(pfad.read_text(encoding="utf-8"), filename=str(pfad))
    umhuellt = set()
    for knoten in ast.walk(baum):
        if (isinstance(knoten, ast.Call) and isinstance(knoten.func, ast.Attribute)
                and knoten.func.attr in ("_register_after", "adopt")):
            umhuellt.update(id(arg) for arg in knoten.args)
    for knoten in ast.walk(baum):
        if not (isinstance(knoten, ast.Call) and isinstance(knoten.func, ast.Attribute)):
            continue
        ziel = ast.unparse(knoten.func.value)
        if knoten.func.attr == "Toplevel" and ziel == "tk":
            zahlen["direkte tk.Toplevel"] += 1
        elif (knoten.func.attr in ("after", "after_idle") and id(knoten) not in umhuellt
              and "after_scope" not in ziel and "scope_for(" not in ziel):
            zahlen["Zeitgeber ohne AfterScope"] += 1
    return zahlen


class Sperrklinke(unittest.TestCase):
    def test_restkopplung_steigt_nicht_und_grenze_ist_aktuell(self):
        gezaehlt = restkopplung(SRC / "app.pyw")
        for name, grenze in RESTKOPPLUNG.items():
            self.assertLessEqual(gezaehlt[name], grenze,
                                 f"{name}: {gezaehlt[name]} statt höchstens {grenze} – Shell-Weg benutzen")
            self.assertEqual(gezaehlt[name], grenze,
                             f"{name}: nur noch {gezaehlt[name]} – Grenze in RESTKOPPLUNG senken")


class Paketbau(unittest.TestCase):
    """Das eigenständige Paket muss `glide_shell` als Paket mitnehmen (D95).

    `glide_app.py` wird im Bundle als Datei geladen; PyInstaller sieht seine
    Importe nicht. Fehlte das Paket in `hiddenimports`, scheiterte der native
    Start mit `No module named 'glide_shell'` (macOS-Lauf 44812703263).
    """

    def test_stage_modules_enthaelt_das_shell_paket(self):
        import importlib.util
        pfad = SRC.parents[1] / "packaging" / "paket" / "package_spec.py"
        sys.path.insert(0, str(pfad.parent))
        try:
            spec = importlib.util.spec_from_file_location("glide_package_spec_pruefling", pfad)
            modul = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modul)
        finally:
            sys.path.remove(str(pfad.parent))
        gefunden = modul.stage_modules(SRC, "start_glide.py")
        erwartet = {PAKET} | {f"{PAKET}.{name}" for name in SHELL_MODULE}
        self.assertLessEqual(erwartet, set(gefunden), sorted(erwartet - set(gefunden)))
        self.assertIn("i18n", gefunden)
        self.assertFalse({n for n in gefunden if n.startswith(("vendor", "resources", "licenses"))})
        for name in erwartet:
            self.assertTrue(gefunden[name].is_file(), name)

    def test_paketmanifest_kopiert_das_shell_paket(self):
        """Ohne diesen Eintrag kopierte der Paketbau `glide_shell/` nicht in den Bauordner."""
        import importlib.util
        pfad = SRC.parents[1] / "packaging" / "paket" / "package_sources.py"
        spec = importlib.util.spec_from_file_location("glide_package_sources_pruefling", pfad)
        modul = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modul)
        erwartet = {f"{PAKET}/__init__.py"} | {f"{PAKET}/{name}.py" for name in SHELL_MODULE}
        for ziel in modul.TARGETS:
            with self.subTest(ziel=ziel):
                dateien = modul.manifest(SRC, ziel)
                self.assertLessEqual(erwartet, set(dateien), sorted(erwartet - set(dateien)))
                self.assertFalse({n for n in dateien if n.startswith(PAKET + "/") and not n.endswith(".py")})


if __name__ == "__main__":
    unittest.main()
