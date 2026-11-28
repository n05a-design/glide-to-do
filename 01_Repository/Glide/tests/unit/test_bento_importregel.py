# SPDX-License-Identifier: MPL-2.0
"""Architektur- und Importregeln für das Glide Bento Box System (D100, Ebene B).

Regeln:
1. Ebene B (glide_bento) darf ausschließlich die Python-Standardbibliothek,
   Tkinter, glide_shell und interne glide_bento-Module importieren.
   Kein glide_bento-Modul darf Fachlogik oder Module aus Ebene A (Glide-Applikation)
   importieren.
2. Ebene C (glide_shell) darf KEIN glide_bento importieren (strikte Schichtung
   Ebene A -> Ebene B -> Ebene C).
3. Öffentliche Schnittstellenprüfung von glide_bento.
"""
import ast
from pathlib import Path
import unittest

SRC = Path(__file__).resolve().parents[2] / "src" / "glide"
BENTO = SRC / "glide_bento"
SHELL = SRC / "glide_shell"

BENTO_MODULES = (
    "tokens",
    "context",
    "specs",
    "layout",
    "card",
    "grid",
    "components",
    "selftest",
    "demo",
    "showcase",
)


class TestBentoImportregel(unittest.TestCase):
    """Prüft strikte Modulisolation von glide_bento über den AST."""

    def test_bento_module_existieren(self):
        """Alle deklarierten Bento-Module müssen im Dateisystem vorhanden sein."""
        self.assertTrue(BENTO.is_dir(), f"Bento-Verzeichnis fehlt: {BENTO}")
        for mod in BENTO_MODULES:
            pfad = BENTO / f"{mod}.py"
            self.assertTrue(pfad.is_file(), f"Bento-Modul fehlt: {pfad}")

    def test_bento_importiert_keine_glide_anwendung(self):
        """glide_bento darf keine Module aus der Glide-Anwendungsebene A importieren."""
        erlaubte_praefixe = (
            "glide_bento",
            "glide_shell",
            "tkinter",
            "dataclasses",
            "typing",
            "collections",
            "math",
            "sys",
            "os",
            "re",
            "pathlib",
            "unittest",
            "time",
            "functools",
        )

        for py_file in BENTO.glob("*.py"):
            tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        name = alias.name.split(".")[0]
                        # Relative Importe oder Standardbibliothek/Shell
                        self.assertTrue(
                            name in erlaubte_praefixe or not (SRC / f"{name}.py").exists(),
                            f"Verbotener Import in {py_file.name}: import {alias.name} (Ebene A verletzt)",
                        )
                elif isinstance(node, ast.ImportFrom):
                    if node.level and node.level > 0:
                        # Relativer Import innerhalb glide_bento ist erlaubt
                        continue
                    if node.module:
                        root_mod = node.module.split(".")[0]
                        self.assertTrue(
                            root_mod in erlaubte_praefixe or not (SRC / f"{root_mod}.py").exists(),
                            f"Verbotener Import in {py_file.name}: from {node.module} import ... (Ebene A verletzt)",
                        )

    def test_shell_importiert_kein_bento(self):
        """glide_shell (Ebene C) darf unter keinen Umständen glide_bento (Ebene B) importieren."""
        for py_file in SHELL.glob("*.py"):
            tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.assertFalse(
                            "bento" in alias.name.lower(),
                            f"Verbotener Bento-Import in Shell {py_file.name}: import {alias.name}",
                        )
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self.assertFalse(
                            "bento" in node.module.lower(),
                            f"Verbotener Bento-Import in Shell {py_file.name}: from {node.module} import ...",
                        )

    def test_bento_exporte(self):
        """__init__.py muss alle Kernkomponenten exportieren."""
        init_file = BENTO / "__init__.py"
        self.assertTrue(init_file.is_file())
        tree = ast.parse(init_file.read_text(encoding="utf-8"), filename=str(init_file))
        all_exports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "__all__":
                        if isinstance(node.value, (ast.List, ast.Tuple)):
                            for elt in node.value.elts:
                                if isinstance(elt, ast.Constant):
                                    all_exports.append(elt.value)
        erwartet = {
            "BENTO_VERSION",
            "__version__",
            "BentoTokens",
            "DEFAULT_TOKENS",
            "BentoContext",
            "BentoCardSpec",
            "BentoGridSpec",
            "BentoLayoutPlan",
            "BentoLayoutPlanner",
            "BentoCard",
            "BentoHeader",
            "BentoGrid",
            "BentoMetric",
            "BentoActions",
            "BentoEmptyState",
            "BentoDivider",
        }
        self.assertTrue(erwartet.issubset(set(all_exports)), f"Fehlende Exporte in __all__: {erwartet - set(all_exports)}")


class TestBentoPaketbau(unittest.TestCase):
    """Das eigenständige Paket muss `glide_bento` als Paket mitnehmen (D100)."""

    def test_stage_modules_enthaelt_das_bento_paket(self):
        import importlib.util
        import sys
        pfad = SRC.parents[1] / "packaging" / "paket" / "package_spec.py"
        sys.path.insert(0, str(pfad.parent))
        try:
            spec = importlib.util.spec_from_file_location("glide_package_spec_pruefling", pfad)
            modul = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modul)
        finally:
            sys.path.remove(str(pfad.parent))
        gefunden = modul.stage_modules(SRC, "start_glide.py")
        erwartet = {"glide_bento"} | {f"glide_bento.{name}" for name in BENTO_MODULES}
        self.assertLessEqual(erwartet, set(gefunden), sorted(erwartet - set(gefunden)))
        for name in erwartet:
            self.assertTrue(gefunden[name].is_file(), name)

    def test_paketmanifest_kopiert_das_bento_paket(self):
        """Ohne diesen Eintrag kopierte der Paketbau `glide_bento/` nicht in den Bauordner."""
        import importlib.util
        pfad = SRC.parents[1] / "packaging" / "paket" / "package_sources.py"
        spec = importlib.util.spec_from_file_location("glide_package_sources_pruefling", pfad)
        modul = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modul)
        erwartet = {"glide_bento/__init__.py"} | {f"glide_bento/{name}.py" for name in BENTO_MODULES}
        for ziel in modul.TARGETS:
            with self.subTest(ziel=ziel):
                dateien = modul.manifest(SRC, ziel)
                self.assertLessEqual(erwartet, set(dateien), sorted(erwartet - set(dateien)))
                self.assertFalse({n for n in dateien if n.startswith("glide_bento/") and not n.endswith(".py")})


if __name__ == "__main__":
    unittest.main()
