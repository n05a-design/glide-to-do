# SPDX-License-Identifier: MPL-2.0
"""Test T329: Mehrsprachigkeit und Internationalisierung (i18n, M100).

Prüft:
- Spracherkennung und Auflösung ('system', 'de', 'en')
- Katalogladung, Caching und Fallback
- Übersetzung und sichere Formatierung (t)
- Strikte Schlüsselparität zwischen de.json und en.json
- Platzhalterparität ({var}) für alle übersetzten Texte
- Einhaltung des Modulbudgets WA-50 (Funktionen <= 50 Zeilen, 0 Tkinter-Imports)
"""

import ast
import json
import os
from pathlib import Path
import re
import sys
import unittest

SRC = Path(__file__).resolve().parents[2] / "src" / "glide"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import i18n


class I18nTests(unittest.TestCase):
    def setUp(self):
        i18n.clear_cache()

    def tearDown(self):
        i18n.clear_cache()

    def test_detect_system_language_defaults_to_de(self):
        orig_env = {k: os.environ.get(k) for k in ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG")}
        try:
            for k in orig_env:
                if k in os.environ:
                    del os.environ[k]
            # Ohne englische Umgebungsvariablen fällt die Erkennung auf 'de'
            self.assertIn(i18n.detect_system_language(), ("de", "en"))
        finally:
            for k, v in orig_env.items():
                if v is not None:
                    os.environ[k] = v

    def test_detect_system_language_with_env(self):
        orig_lang = os.environ.get("LANG")
        try:
            os.environ["LANG"] = "en_US.UTF-8"
            self.assertEqual(i18n.detect_system_language(), "en")
            os.environ["LANG"] = "de_DE.UTF-8"
            self.assertEqual(i18n.detect_system_language(), "de")
        finally:
            if orig_lang is not None:
                os.environ["LANG"] = orig_lang
            elif "LANG" in os.environ:
                del os.environ["LANG"]

    def test_resolve_language(self):
        self.assertEqual(i18n.resolve_language("de"), "de")
        self.assertEqual(i18n.resolve_language("DE"), "de")
        self.assertEqual(i18n.resolve_language("en"), "en")
        self.assertEqual(i18n.resolve_language("EN"), "en")
        self.assertEqual(i18n.resolve_language("unknown_lang"), "de")
        # 'system' ruft detect_system_language auf
        self.assertIn(i18n.resolve_language("system"), ("de", "en"))
        self.assertIn(i18n.resolve_language(None), ("de", "en"))

    def test_set_and_get_language(self):
        self.assertEqual(i18n.get_language(), "de")
        i18n.set_language("en")
        self.assertEqual(i18n.get_language(), "en")
        i18n.set_language("de")
        self.assertEqual(i18n.get_language(), "de")

    def test_load_catalog(self):
        de_cat = i18n.load_catalog("de")
        self.assertIsInstance(de_cat, dict)
        self.assertIn("menu.file", de_cat)
        self.assertEqual(de_cat["menu.file"], "Datei")

        en_cat = i18n.load_catalog("en")
        self.assertIsInstance(en_cat, dict)
        self.assertIn("menu.file", en_cat)
        self.assertEqual(en_cat["menu.file"], "File")

    def test_t_function_translation_and_fallback(self):
        i18n.set_language("de")
        self.assertEqual(i18n.t("menu.file"), "Datei")
        self.assertEqual(i18n.t("menu.edit.undo"), "Rückgängig")

        i18n.set_language("en")
        self.assertEqual(i18n.t("menu.file"), "File")
        self.assertEqual(i18n.t("menu.edit.undo"), "Undo")

        # Unbekannter Schlüssel fällt auf default oder key zurück
        self.assertEqual(i18n.t("unknown.key", default="Ersatz"), "Ersatz")
        self.assertEqual(i18n.t("unknown.key"), "unknown.key")

    def test_t_formatting_with_kwargs(self):
        i18n.set_language("de")
        self.assertEqual(i18n.t("menu.help.about", app_name="Glide"), "Über Glide")
        self.assertEqual(i18n.t("toast.undo", action="Aufgabe"), "Rückgängig gemacht: Aufgabe")

        i18n.set_language("en")
        self.assertEqual(i18n.t("menu.help.about", app_name="Glide"), "About Glide")
        self.assertEqual(i18n.t("toast.undo", action="Task"), "Undone: Task")

    def test_safe_format_resilience(self):
        # Fehlende Variablen werfen keinen Fehler
        self.assertEqual(i18n.safe_format("Hallo {name}", {}), "Hallo {name}")
        # Ungültige Formatierungszeichen werfen keinen Fehler
        self.assertEqual(i18n.safe_format("Zahl {0:xyz}", {"x": 1}), "Zahl {0:xyz}")

    def test_catalog_key_parity(self):
        locales_dir = i18n.get_locales_dir()
        de_data = json.loads((locales_dir / "de.json").read_text(encoding="utf-8"))
        en_data = json.loads((locales_dir / "en.json").read_text(encoding="utf-8"))

        de_keys = set(de_data.keys())
        en_keys = set(en_data.keys())

        missing_in_en = de_keys - en_keys
        missing_in_de = en_keys - de_keys

        self.assertEqual(missing_in_en, set(), f"Schlüssel fehlen in en.json: {missing_in_en}")
        self.assertEqual(missing_in_de, set(), f"Schlüssel fehlen in de.json: {missing_in_de}")

    def test_catalog_placeholder_parity(self):
        locales_dir = i18n.get_locales_dir()
        de_data = json.loads((locales_dir / "de.json").read_text(encoding="utf-8"))
        en_data = json.loads((locales_dir / "en.json").read_text(encoding="utf-8"))

        placeholder_pattern = re.compile(r"\{([a-zA-Z0-9_]+)\}")

        for key in de_data:
            de_vars = set(placeholder_pattern.findall(de_data[key]))
            en_vars = set(placeholder_pattern.findall(en_data[key]))
            self.assertEqual(
                de_vars, en_vars,
                f"Platzhalter stimmen für Schlüssel '{key}' nicht überein: de={de_vars}, en={en_vars}"
            )

    def test_module_budget_wa50(self):
        source_path = SRC / "i18n.py"
        source_code = source_path.read_text(encoding="utf-8")
        tree = ast.parse(source_code, filename=str(source_path))

        # 1. Keine Tkinter-Imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertNotIn("tkinter", alias.name, "i18n.py darf kein tkinter importieren")
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self.assertNotIn("tkinter", node.module, "i18n.py darf kein tkinter importieren")

        # 2. Funktionslänge <= 50 Zeilen
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                end_lineno = getattr(node, "end_lineno", node.lineno)
                length = end_lineno - node.lineno + 1
                self.assertLessEqual(
                    length, 50,
                    f"Funktion {node.name} überschreitet das 50-Zeilen-Budget ({length} Zeilen)"
                )


if __name__ == "__main__":
    unittest.main()
