# SPDX-License-Identifier: MPL-2.0
"""Zentrale Liste der Shell-Module und ihre Importregel (D86, ohne Tk-Import).

Die Shell liegt bis zum Paket `glide_shell` flach neben den Glide-Modulen in
`src/glide`. Was zur Shell gehört, steht deshalb hier in `SHELL_MODULE`. Jedes
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
import sys
import unittest

SRC = Path(__file__).resolve().parents[2] / "src" / "glide"

# Modul: öffentliche Schnittstelle (Funktion oder Klasse.Methode: Parameter ohne self)
SHELL_MODULE = {
    "modal_session": {
        "modal_over": ["root", "parent"],
        "remember_focus": ["root", "dialog", "parent"],
        "return_focus": ["root", "dialog", "remembered"],
        "wait_modal": ["root", "dialog", "parent", "log_error"],
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
    "desktop_adapter": {
        "is_macos": [],
        "is_windows": [],
        "is_linux": [],
        "platform_name": [],
        "primary_modifier": ["macos_override"],
        "format_accelerator": ["macos_override"],
        "format_redo_accelerator": ["windows_override", "macos_override"],
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
    quelle = SRC / f"{modul}.py"
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
            self.assertTrue((SRC / f"{modul}.py").is_file(), modul)

    def test_gekennzeichnete_module_stehen_in_der_liste(self):
        gekennzeichnet = set()
        for quelle in sorted(SRC.glob("*.py")):
            kopf = ast.get_docstring(ast.parse(quelle.read_text(encoding="utf-8"))) or ""
            if kopf and KENNZEICHEN in kopf.splitlines()[0]:
                gekennzeichnet.add(quelle.stem)
        self.assertEqual(gekennzeichnet, set(SHELL_MODULE))


class Importregel(unittest.TestCase):
    def test_nur_standardbibliothek_tkinter_und_shell(self):
        for modul in SHELL_MODULE:
            for name in importe(baum(modul)):
                with self.subTest(modul=modul, importiert=name):
                    self.assertFalse(name.startswith("."), "relative Importe gibt es in der flachen Ablage nicht")
                    self.assertTrue(name in sys.stdlib_module_names or name in SHELL_MODULE, name)

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


if __name__ == "__main__":
    unittest.main()
