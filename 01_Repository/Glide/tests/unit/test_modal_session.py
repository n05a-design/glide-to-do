# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 3a: Importregel und Schnittstelle von `modal_session` (ohne Tk-Import).

`modal_session` ist der erste Baustein der Shell. Er darf nur die
Standardbibliothek und `tkinter` importieren und keinen Glide-Wert kennen
(Abhängigkeitsrichtung Host → Shell → Tk). Dieser Test liest die Quelle nur
als Syntaxbaum; das Verhalten mit echtem Grab prüft
`tests/integration/test_modalvertrag.py`.
"""
import ast
from pathlib import Path
import sys
import unittest

QUELLE = Path(__file__).resolve().parents[2] / "src" / "glide" / "modal_session.py"
ERLAUBT = {"contextlib", "tkinter"}
SCHNITTSTELLE = {
    "modal_over": ["root", "parent"],
    "ensure_min_width": ["dialog", "max_screen_share"],
    "bring_to_front": ["dialog"],
    "remember_focus": ["root", "dialog", "parent"],
    "return_focus": ["root", "dialog", "remembered"],
    "wait_modal": ["root", "dialog", "parent", "log_error"],
    "run_modal": ["root", "dialog", "parent", "background", "max_screen_share", "log_error"],
}


def baum():
    return ast.parse(QUELLE.read_text(encoding="utf-8"), filename=str(QUELLE))


def importe(tree):
    namen = set()
    for knoten in ast.walk(tree):
        if isinstance(knoten, ast.Import):
            namen.update(alias.name.split(".")[0] for alias in knoten.names)
        elif isinstance(knoten, ast.ImportFrom):
            if knoten.level:
                namen.add("." * knoten.level + (knoten.module or ""))
            else:
                namen.add((knoten.module or "").split(".")[0])
    return namen


class Importregel(unittest.TestCase):
    def test_nur_standardbibliothek_und_tkinter(self):
        gefunden = importe(baum())
        self.assertLessEqual(gefunden, ERLAUBT, f"unerlaubte Importe: {sorted(gefunden - ERLAUBT)}")
        for name in gefunden:
            self.assertIn(name, sys.stdlib_module_names, name)

    def namen(self):
        """Alle Bezeichner im Code; Docstrings und Kommentare zählen nicht."""
        gefunden = set()
        for knoten in ast.walk(baum()):
            if isinstance(knoten, ast.Name):
                gefunden.add(knoten.id)
            elif isinstance(knoten, ast.Attribute):
                gefunden.add(knoten.attr)
        return gefunden

    def test_kein_dynamischer_import_und_kein_glide_modul(self):
        for name in self.namen():
            self.assertNotIn(name, {"__import__", "importlib", "ListApp", "self"}, name)
            self.assertFalse(name.startswith("glide_"), name)

    def test_keine_produktwerte(self):
        """Theme, Texte und Fehlerprotokoll kommen vom Host, nicht aus dem Modul."""
        for name in self.namen():
            self.assertFalse(name.startswith(("APP_", "ERROR_LOG", "THEMES", "theme")), name)


class Schnittstelle(unittest.TestCase):
    def test_oeffentliche_funktionen_und_parameter(self):
        funktionen = {knoten.name: knoten for knoten in baum().body if isinstance(knoten, ast.FunctionDef)}
        for name, erwartet in SCHNITTSTELLE.items():
            self.assertIn(name, funktionen, name)
            args = funktionen[name].args
            parameter = [a.arg for a in args.posonlyargs + args.args + args.kwonlyargs]
            self.assertEqual(parameter, erwartet, name)

    def test_modal_over_ist_kontextmanager(self):
        funktion = next(k for k in baum().body if isinstance(k, ast.FunctionDef) and k.name == "modal_over")
        dekoratoren = [ast.unparse(d) for d in funktion.decorator_list]
        self.assertEqual(dekoratoren, ["contextlib.contextmanager"])

    def test_kompatible_attributnamen(self):
        """Einstellungsdialog und Fensterwechsel der App lesen diese Attribute."""
        werte = {}
        for knoten in baum().body:
            if isinstance(knoten, ast.Assign) and isinstance(knoten.value, ast.Constant):
                for ziel in knoten.targets:
                    if isinstance(ziel, ast.Name):
                        werte[ziel.id] = knoten.value.value
        self.assertEqual(werte.get("ACTIVE_ATTRIBUTE"), "_glide_modal_active")
        self.assertEqual(werte.get("FINISHED_ATTRIBUTE"), "_glide_modal_finished")
        self.assertEqual(werte.get("DEFAULT_MAX_SCREEN_SHARE"), 0.88)


if __name__ == "__main__":
    unittest.main()
