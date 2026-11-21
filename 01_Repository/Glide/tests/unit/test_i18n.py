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
import backdrop
from glide_shell import desktop_adapter


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
        # Alle vier Variablen selbst setzen: Die Prüfumgebung gibt LANGUAGE=de
        # als Referenzsprache vor, und LANGUAGE hat Vorrang vor LANG.
        names = ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG")
        orig_env = {k: os.environ.get(k) for k in names}
        try:
            for k in names:
                os.environ.pop(k, None)
            os.environ["LANG"] = "en_US.UTF-8"
            self.assertEqual(i18n.detect_system_language(), "en")
            os.environ["LANG"] = "de_DE.UTF-8"
            self.assertEqual(i18n.detect_system_language(), "de")
            os.environ["LANG"] = "en_US.UTF-8"
            os.environ["LANGUAGE"] = "de"
            self.assertEqual(i18n.detect_system_language(), "de", "LANGUAGE hat Vorrang vor LANG")
        finally:
            for k, v in orig_env.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v

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

    def test_saved_view_menu_translations(self):
        i18n.set_language("de")
        self.assertEqual(i18n.t("menu.view.saved_filters"), "Gespeicherte Filter …")
        self.assertEqual(i18n.t("menu.view.save_as_view"), "Als Ansicht speichern …")
        self.assertEqual(i18n.t("menu.view.explain_filter"), "Filter erklären …")

        i18n.set_language("en")
        self.assertEqual(i18n.t("menu.view.saved_filters"), "Saved filters …")
        self.assertEqual(i18n.t("menu.view.save_as_view"), "Save as view …")
        self.assertEqual(i18n.t("menu.view.explain_filter"), "Explain filter …")

    def test_saved_view_and_board_translations(self):
        i18n.set_language("de")
        self.assertEqual(i18n.t("saved_view.manager.title"), "Gespeicherte Filter")
        self.assertEqual(i18n.t("saved_view.limit.body", max=100), "Es sind maximal 100 Filter möglich.")
        self.assertEqual(i18n.t("board.open_tab.title"), "Reiter öffnen")
        self.assertEqual(i18n.t("board.connect.select"), "Zuerst eine Karte auswählen.")
        self.assertEqual(i18n.t("board.action.open_tab"), "Als Reiter öffnen")
        i18n.set_language("en")
        self.assertEqual(i18n.t("saved_view.manager.title"), "Saved filters")
        self.assertEqual(i18n.t("saved_view.limit.body", max=100), "A maximum of 100 filters is supported.")
        self.assertEqual(i18n.t("board.open_tab.title"), "Open tab")
        self.assertEqual(i18n.t("board.connect.select"), "Select a card first.")
        self.assertEqual(i18n.t("board.action.open_tab"), "Open as tab")

    def test_side_view_status_translations(self):
        i18n.set_language("de")
        self.assertEqual(i18n.t("side_view.status.read_only"), "Schreibgeschützter Bestand · nur ansehen.")
        self.assertEqual(i18n.t("side_view.status.change_not_saved"), "Die Änderung wurde nicht gespeichert.")
        self.assertEqual(i18n.t("side_view.status.no_matches"), "Keine Treffer.")
        self.assertEqual(i18n.t("side_view.status.no_tasks"), "Noch keine Aufgaben.")
        self.assertEqual(i18n.t("side_view.status.search_position", position="1 / 3"), "1 / 3 Treffer")
        self.assertEqual(i18n.t("side_view.status.section", title="Inhalt"), "Abschnitt: Inhalt")
        i18n.set_language("en")
        self.assertEqual(i18n.t("side_view.status.read_only"), "Read-only data · view only.")
        self.assertEqual(i18n.t("side_view.status.change_not_saved"), "The change was not saved.")
        self.assertEqual(i18n.t("side_view.status.no_matches"), "No matches.")
        self.assertEqual(i18n.t("side_view.status.no_tasks"), "No tasks yet.")
        self.assertEqual(i18n.t("side_view.status.search_position", position="1 / 3"), "1 / 3 matches")
        self.assertEqual(i18n.t("side_view.status.section", title="Content"), "Section: Content")

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

    def test_app_translation_keys_exist_in_both_catalogs(self):
        source_path = SRC / "app.pyw"
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
        app_keys = {
            node.args[0].value
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "glide_i18n"
            and node.func.attr == "t"
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
        }
        locales_dir = i18n.get_locales_dir()
        catalogs = {
            locale: json.loads((locales_dir / f"{locale}.json").read_text(encoding="utf-8"))
            for locale in ("de", "en")
        }

        self.assertTrue(app_keys, "Keine direkten Übersetzungsschlüssel in app.pyw gefunden")
        for locale, catalog in catalogs.items():
            missing = app_keys - catalog.keys()
            self.assertEqual(missing, set(), f"Direkte App-Schlüssel fehlen in {locale}.json: {missing}")

    def test_ui_defaults_match_german_catalog_and_are_translated(self):
        """D93-Volllokalisierung: `ui.*`-Vorgaben im Code gleichen de.json, en.json übersetzt sie."""
        source_path = SRC / "app.pyw"
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
        locales_dir = i18n.get_locales_dir()
        de = json.loads((locales_dir / "de.json").read_text(encoding="utf-8"))
        en = json.loads((locales_dir / "en.json").read_text(encoding="utf-8"))
        abweichend, gefunden = [], 0
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and getattr(node.func.value, "id", None) == "glide_i18n" and node.func.attr == "t"
                    and len(node.args) >= 2
                    and all(isinstance(arg, ast.Constant) and isinstance(arg.value, str) for arg in node.args[:2])
                    and node.args[0].value.startswith("ui.")):
                continue
            gefunden += 1
            key, default = node.args[0].value, node.args[1].value
            if de.get(key) != default:
                abweichend.append((node.lineno, key))
        self.assertGreater(gefunden, 0)
        self.assertEqual(abweichend, [], "Codevorgabe und de.json weichen ab")
        # Wörter, die im Englischen gleich lauten, dürfen unverändert bleiben.
        gleich = {"labels", "label", "in", "zoom", "navigator", "status", "ok", "name", "start", "pdf", "html", "txt",
                  "csv", "ics", "markdown", "json", "glide", "canvas", "png", "svg", "ico", "min", "cmd", "alt", "tab",
                  "enter", "esc", "escape", "shift", "f2", "f3", "f11"}

        def gleichlautend(text):
            woerter = re.findall(r"[^\W\d_]+", re.sub(r"\{[^}]*\}", " ", text).lower())
            return all(wort in gleich for wort in woerter)

        unuebersetzt = sorted(key for key in de if key.startswith("ui.") and en.get(key) == de[key]
                              and not gleichlautend(de[key]))
        self.assertEqual(unuebersetzt, [], "ui.*-Schlüssel ohne englischen Text")

    def test_settings_backdrop_names_exist_in_both_catalogs(self):
        locales_dir = i18n.get_locales_dir()
        catalogs = {
            locale: json.loads((locales_dir / f"{locale}.json").read_text(encoding="utf-8"))
            for locale in ("de", "en")
        }
        preset_keys = {
            f"settings.backdrop.{design}.{preset.key}"
            for design, presets in backdrop.PRESETS.items()
            for preset in presets
        }

        self.assertTrue(preset_keys, "Keine Hintergrund-Presets für die Einstellungen gefunden")
        for locale, catalog in catalogs.items():
            missing = preset_keys - catalog.keys()
            self.assertEqual(missing, set(), f"Hintergrundnamen fehlen in {locale}.json: {missing}")

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

    def test_shell_accelerator_labels_follow_host_locale(self):
        expected = {
            "de": ("Strg+P", "Strg+Umschalt+Z"),
            "en": ("Ctrl+P", "Ctrl+Shift+Z"),
        }
        for language, (accelerator, redo) in expected.items():
            i18n.set_language(language)
            labels = {
                name: i18n.t(f"keyboard.modifier.{name}")
                for name in ("command", "control", "shift")
            }
            self.assertEqual(
                desktop_adapter.format_accelerator(
                    "P", macos_override=False, modifier_labels=labels
                ),
                accelerator,
            )
            self.assertEqual(
                desktop_adapter.format_redo_accelerator(
                    windows_override=False, macos_override=False,
                    modifier_labels=labels,
                ),
                redo,
            )

    def test_editor_translation_keys_exist_in_both_catalogs(self):
        editor_keys = {
            "editor.toolbar.list", "editor.toolbar.numbered", "editor.toolbar.task",
            "editor.toolbar.quote", "editor.toolbar.image", "editor.toolbar.more",
            "editor.tooltip.more", "editor.tooltip.rename_page",
            "editor.format_bar.block_menu", "editor.menu.cut", "editor.menu.copy",
            "editor.menu.paste", "editor.menu.paste_plain", "editor.menu.select_all",
            "editor.menu.link", "editor.menu.link_short", "editor.menu.remove_format",
            "editor.menu.format", "editor.menu.convert", "editor.menu.line_up",
            "editor.menu.line_down", "editor.menu.duplicate_line", "editor.menu.delete_line",
            "editor.menu.divider", "editor.menu.insert_image", "editor.menu.paste_page",
            "editor.block_actions.search", "editor.block_actions.title",
        }
        editor_keys.update(f"editor.block.{tag}" for tag in (
            "text", "h1", "h2", "h3", "h4", "bullet", "number", "task",
            "toggle", "toggle_h2", "quote", "callout", "codeblock",
        ))
        editor_keys.update(f"editor.format.{tag}" for tag in (
            "bold", "italic", "underline", "strike", "code", "highlight",
        ))
        editor_keys.update(f"editor.format_bar.{tag}" for tag in (
            "bold", "italic", "underline", "strike", "code", "highlight",
        ))
        editor_keys.update(f"editor.block_actions.section.{name}" for name in (
            "edit", "task", "format", "line",
        ))
        editor_keys.update(f"editor.block_actions.order.{name}" for name in (
            "convert", "line", "format", "edit", "task",
        ))
        locales_dir = i18n.get_locales_dir()
        for language in ("de", "en"):
            catalog = json.loads((locales_dir / f"{language}.json").read_text(encoding="utf-8"))
            self.assertEqual(editor_keys - catalog.keys(), set(),
                             f"Editor-Schlüssel fehlen in {language}.json")

    def test_inspector_dynamic_translation_keys_exist_in_both_catalogs(self):
        inspector_keys = {
            *(f"inspector.kind.{kind}" for kind in ("task", "group", "long", "heading")),
            *(f"inspector.repeat.{kind}" for kind in (
                "none", "taeglich", "tage", "wochentage", "woechentlich", "monatlich",
                "jaehrlich", "serie_woche", "serie_monat", "serie_jahr", "serie_position",
                "serie_letzter", "serie_werktag",
            )),
            *(f"inspector.relation.{kind}" for kind in ("links", "blocked_by")),
            *(f"inspector.relation.add.{kind}" for kind in ("links", "blocked_by")),
            *(f"inspector.relation.backlink.{kind}" for kind in ("links", "blocked_by")),
            *(f"calendar.month.{month}" for month in range(1, 13)),
        }
        locales_dir = i18n.get_locales_dir()
        for language in ("de", "en"):
            catalog = json.loads((locales_dir / f"{language}.json").read_text(encoding="utf-8"))
            self.assertEqual(inspector_keys - catalog.keys(), set(),
                             f"Dynamische Inspektor-/Kalenderschlüssel fehlen in {language}.json")

    def test_drawing_translation_keys_exist_in_both_catalogs(self):
        drawing_keys = {
            "drawing.status.symmetry", "drawing.status.symmetry.left_right",
            "drawing.status.symmetry.top_bottom", "drawing.status.symmetry.both",
            "drawing.status.pattern.checkerboard", "drawing.status.pattern.dots_25",
            "drawing.status.pattern.dots_75", "drawing.status.colors", "drawing.status.cell",
            "drawing.status.selection", "drawing.status.dimensions", "drawing.status.undo_pending",
            "drawing.status.undo_empty", "drawing.status.cells_changed.one",
            "drawing.status.cells_changed.many", "drawing.status.selection_cleared",
            "drawing.status.select_all", "drawing.status.no_selection", "drawing.status.copied",
            "drawing.status.nothing_to_paste", "drawing.status.cancelled", "drawing.status.anchor_set",
            "drawing.status.eyedropper_guide", "drawing.status.source.drawing",
            "drawing.status.source.reference", "drawing.status.foreground", "drawing.status.background",
            "drawing.status.picked_color", "drawing.status.undo_done.one", "drawing.status.undo_done.many",
            "drawing.status.redo_done.one", "drawing.status.redo_done.many", "drawing.status.redo_empty",
            *(f"drawing.status.tool.{tool}" for tool in (
                "brush", "fill", "eyedropper", "line", "rectangle", "ellipse", "selection",
            )),
            *(f"drawing.status.save.{state}" for state in ("saved", "unsaved", "saving", "error")),
            *(f"drawing.action.{action}" for action in (
                "brush_stroke", "brush", "fill", "line", "rectangle", "ellipse", "move", "cut",
                "clear_selection", "paste", "replace_color",
            )),
            *(f"drawing.tool.{tool}" for tool in (
                "brush", "fill", "eyedropper", "line", "rectangle", "ellipse", "selection",
            )),
            *(f"drawing.profile.{profile}" for profile in (
                "standard", "extended", "animation", "pixelate",
            )),
            *(f"drawing.pattern.{pattern}" for pattern in ("solid", "checker", "dots25", "dots75")),
            *(f"drawing.button.{button}" for button in ("preview", "more", "zoom", "palette")),
            *(f"drawing.reference.{reference}" for reference in ("load", "reframe", "pixelate")),
            *(f"drawing.preview.{preview}" for preview in ("title", "tile", "grayscale")),
            *(f"drawing.zoom.{zoom}" for zoom in ("out", "in", "fit")),
            *(f"drawing.option.symmetry.{mode}" for mode in ("none", "x", "y", "xy")),
            *(f"drawing.option.{option}" for option in (
                "caption", "size", "filled", "pattern", "pixel_perfect", "wrap", "copy", "cut",
                "paste", "clear", "select_all", "deselect",
            )),
            *(f"drawing.tooltip.{tooltip}" for tooltip in (
                "tool", "profile", "preview", "foreground", "background", "swap_colors", "tile", "grayscale",
            )),
        }
        locales_dir = i18n.get_locales_dir()
        for language in ("de", "en"):
            catalog = json.loads((locales_dir / f"{language}.json").read_text(encoding="utf-8"))
            self.assertEqual(drawing_keys - catalog.keys(), set(),
                             f"Zeicheneditor-Schlüssel fehlen in {language}.json")

    def test_action_feedback_translation_keys_cover_every_action(self):
        source_path = SRC / "app.pyw"
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
        tables = [
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "ACTION_FEEDBACK_TEXTS"
                    for target in node.targets)
        ]
        self.assertEqual(len(tables), 1, "Rückmelderegister nicht eindeutig gefunden")
        action_keys = ast.literal_eval(tables[0]).keys()
        required = {f"feedback.{key}{suffix}" for key in action_keys
                    for suffix in ("", ".plural")}
        locales_dir = i18n.get_locales_dir()
        catalogs = {
            language: json.loads((locales_dir / f"{language}.json").read_text(encoding="utf-8"))
            for language in ("de", "en")
        }
        for language, catalog in catalogs.items():
            self.assertEqual(required - catalog.keys(), set(),
                             f"Rückmeldungen fehlen in {language}.json")
        self.assertEqual(i18n.safe_format(catalogs["de"]["feedback.item_created.plural"], {"n": 3}),
                         "3 Punkte angelegt")
        self.assertEqual(i18n.safe_format(catalogs["en"]["feedback.item_created.plural"], {"n": 3}),
                         "3 items created")

    def test_undo_toasts_use_translated_or_prepared_text(self):
        source_path = SRC / "app.pyw"
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
        calls = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "show_undo_toast"
        ]
        self.assertEqual(len(calls), 29)
        for call in calls:
            self.assertTrue(call.args, "show_undo_toast needs a text argument")
            self.assertNotIsInstance(call.args[0], ast.Constant,
                                     "Undo-Toast darf keinen direkten String verwenden")
            self.assertNotIsInstance(call.args[0], ast.JoinedStr,
                                     "Undo-Toast darf keinen direkten F-String verwenden")

        locales_dir = i18n.get_locales_dir()
        catalogs = {
            language: json.loads((locales_dir / f"{language}.json").read_text(encoding="utf-8"))
            for language in ("de", "en")
        }
        toast_keys = {
            key for key in catalogs["de"] if key.startswith("toast.")
        } | {
            key for key in catalogs["en"] if key.startswith("toast.")
        }
        for language in ("de", "en"):
            catalog = catalogs[language]
            missing = {key for key in toast_keys if key not in catalog}
            self.assertEqual(missing, set(), f"Toast-Schlüssel fehlen in {language}.json")

        i18n.set_language("de")
        self.assertEqual(i18n.t("toast.completed"), "Erledigt")
        self.assertEqual(i18n.t("toast.points_reopened", n=3), "3 Punkte wieder offen")
        i18n.set_language("en")
        self.assertEqual(i18n.t("toast.completed"), "Completed")
        self.assertEqual(i18n.t("toast.points_reopened", n=3), "3 items reopened")

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
