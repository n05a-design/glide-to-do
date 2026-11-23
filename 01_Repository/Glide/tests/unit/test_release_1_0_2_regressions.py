# SPDX-License-Identifier: MPL-2.0
"""Regressionstests für Glide 1.0.2: Nachbesserungen nach menschlicher Abnahme.

Prüft die 6 Kernbereiche aus der Abnahme vom 23.11.2026:
1. Dynamischer Sprachwechsel der Seitenleiste (refresh_sidebar_locale)
2. Adaptiver Zuschnitt für Titelbilder (make_page_cover)
3. Pixelzeichnungen als mitscrollendes Ecksymbol (corner_cover)
4. Fußleisten-Dichte bei schmalen Fenstern (sync_foot_density)
5. Bild- und Tabellenumfluss mit Wortumbruch (imgflow / cornerflow wrap='word')
6. Natürliche Datumsangaben (parse_due_words / DueField._on_date_focus_out)
Zusätzlich: Shell-Manifest-Integrität und plattformgerechte Bootstrap-Kommandos.
"""

from datetime import date, timedelta
import importlib.machinery
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import tkinter as tk
import unittest

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "src" / "glide"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import i18n
from glide_shell import selftest

PFLEGE = REPO / "scripts" / "pflege"
if str(PFLEGE) not in sys.path:
    sys.path.insert(0, str(PFLEGE))
import shell_uebernehmen

# Dynamischer Lader für app.pyw
def lade_app():
    if "glide_app_102" in sys.modules:
        return sys.modules["glide_app_102"]
    import importlib.machinery
    import importlib.util
    loader = importlib.machinery.SourceFileLoader("glide_app_102", str(SRC / "app.pyw"))
    spec = importlib.util.spec_from_file_location("glide_app_102", str(SRC / "app.pyw"), loader=loader)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["glide_app_102"] = mod
    loader.exec_module(mod)
    return mod


class DueWordsTests(unittest.TestCase):
    """Testet natürliche Datumswörter ('today', 'heute', etc.) und Fälligkeits-Parsing."""

    def test_relative_words_offsets(self):
        # Import app logic helper dynamically to avoid pulling entire Tk app unless needed
        app_mod = lade_app()
        ref_date = date(2026, 11, 23)

        self.assertEqual(app_mod.ListApp.parse_due_words("today", today=ref_date), "2026-11-23")
        self.assertEqual(app_mod.ListApp.parse_due_words("heute", today=ref_date), "2026-11-23")
        self.assertEqual(app_mod.ListApp.parse_due_words("tomorrow", today=ref_date), "2026-11-24")
        self.assertEqual(app_mod.ListApp.parse_due_words("morgen", today=ref_date), "2026-11-24")
        self.assertEqual(app_mod.ListApp.parse_due_words("yesterday", today=ref_date), "2026-11-22")
        self.assertEqual(app_mod.ListApp.parse_due_words("gestern", today=ref_date), "2026-11-22")
        self.assertEqual(app_mod.ListApp.parse_due_words("day after tomorrow", today=ref_date), "2026-11-25")
        self.assertEqual(app_mod.ListApp.parse_due_words("übermorgen", today=ref_date), "2026-11-25")
        self.assertEqual(app_mod.ListApp.parse_due_words("uebermorgen", today=ref_date), "2026-11-25")

    def test_case_and_whitespace_insensitivity(self):
        app_mod = lade_app()
        ref_date = date(2026, 11, 23)

        self.assertEqual(app_mod.ListApp.parse_due_words("  TODAY  ", today=ref_date), "2026-11-23")
        self.assertEqual(app_mod.ListApp.parse_due_words("Heute", today=ref_date), "2026-11-23")
        self.assertEqual(app_mod.ListApp.parse_due_words("\tTOMORROW\n", today=ref_date), "2026-11-24")
        self.assertEqual(app_mod.ListApp.parse_due_words("Day   After   Tomorrow", today=ref_date), "2026-11-25")

    def test_calendar_boundaries_and_leap_years(self):
        app_mod = lade_app()

        # Schaltjahr: 28.02.2024 -> morgen = 29.02.2024
        leap_ref = date(2024, 2, 28)
        self.assertEqual(app_mod.ListApp.parse_due_words("tomorrow", today=leap_ref), "2024-02-29")

        # Kein Schaltjahr: 28.02.2023 -> morgen = 01.03.2023
        non_leap_ref = date(2023, 2, 28)
        self.assertEqual(app_mod.ListApp.parse_due_words("tomorrow", today=non_leap_ref), "2023-03-01")

        # Monatswechsel
        month_end = date(2026, 11, 30)
        self.assertEqual(app_mod.ListApp.parse_due_words("tomorrow", today=month_end), "2026-12-01")

        # Jahreswechsel
        year_end = date(2026, 12, 31)
        self.assertEqual(app_mod.ListApp.parse_due_words("tomorrow", today=year_end), "2027-01-01")
        year_start = date(2027, 1, 1)
        self.assertEqual(app_mod.ListApp.parse_due_words("yesterday", today=year_start), "2026-12-31")

    def test_fallback_and_invalid_inputs(self):
        app_mod = lade_app()

        # Standard-Datumsformate
        self.assertEqual(app_mod.ListApp.parse_due_words("23.11.2026"), "2026-11-23")
        self.assertEqual(app_mod.ListApp.parse_due_words("2026-11-23"), "2026-11-23")
        self.assertEqual(app_mod.ListApp.parse_due_words(""), "")
        self.assertIsNone(app_mod.ListApp.parse_due_words(None))
        self.assertIsNone(app_mod.ListApp.parse_due_words("ungueltiges-wort"))


class CoverCropAndLayoutTests(unittest.TestCase):
    """Testet die Berechnungen für adaptiven Titelbildzuschnitt und Dichte."""

    def test_adaptive_cover_height_clamping(self):
        app_mod = lade_app()

        ratio = app_mod.ListApp.COVER_RATIO
        max_h = app_mod.ListApp.COVER_MAX_HEIGHT
        base_h = 110

        # Schmal: 300px * 0.34 = 102px -> unter 110, bleibt 110
        h_small = max(base_h, min(max_h, round(300 * ratio)))
        self.assertEqual(h_small, 110)

        # Mittel: 500px * 0.34 = 170px -> zwischen 110 und 240
        h_mid = max(base_h, min(max_h, round(500 * ratio)))
        self.assertEqual(h_mid, 170)

        # Breit: 1000px * 0.34 = 340px -> über 240, wird auf 240 gekappt
        h_large = max(base_h, min(max_h, round(1000 * ratio)))
        self.assertEqual(h_large, 240)

    def test_cover_upscale_limit_and_focus_point(self):
        app_mod = lade_app()

        max_upscale = app_mod.ListApp.COVER_MAX_UPSCALE
        focus = app_mod.ListApp.COVER_FOCUS

        # Natürliche Breite 100px bei Canvas-Breite 600px darf nie 600px werden
        natur_w = 100
        canvas_w = 600
        ziel_w = min(canvas_w, max(1, round(natur_w * max_upscale)))
        self.assertEqual(ziel_w, 150)

        # Fokuspunkt oberhalb der Bildmitte
        img_h = 300
        cover_h = 170
        oben = -round((img_h - cover_h) * focus)
        self.assertEqual(oben, -round(130 * 0.38))

    def test_make_page_cover_canvas_widget(self):
        """Prüft das reale tk.Canvas-Widget aus make_page_cover und die adaptive Höhenanpassung."""
        app_mod = lade_app()
        try:
            root = tk.Tk()
            root.withdraw()
        except tk.TclError:
            self.skipTest("Kein Display verfuegbar")

        class CoverAppAdapter:
            COVER_RATIO = app_mod.ListApp.COVER_RATIO
            COVER_MAX_HEIGHT = app_mod.ListApp.COVER_MAX_HEIGHT
            COVER_FOCUS = app_mod.ListApp.COVER_FOCUS
            COVER_MAX_UPSCALE = app_mod.ListApp.COVER_MAX_UPSCALE
            theme = {"input": "#ffffff", "muted": "#888888"}
            previews = None
            make_page_cover = app_mod.ListApp.make_page_cover

        app_obj = CoverAppAdapter()
        entry = {"cover": None}

        # 1. Adaptiver Modus: Canvas entsteht mit Basis-Höhe
        canvas_adapt = app_obj.make_page_cover(root, entry, height=110, adaptive=True)
        self.assertEqual(int(float(canvas_adapt.cget("height"))), 110)

        # 2. Nicht-adaptiver Modus: Canvas behält immer Höhe
        canvas_fixed = app_obj.make_page_cover(root, entry, height=110, adaptive=False)
        self.assertEqual(int(float(canvas_fixed.cget("height"))), 110)

        canvas_adapt.destroy()
        canvas_fixed.destroy()
        root.destroy()


class ShellManifestIntegrityTests(unittest.TestCase):
    """Testet die Härtung von manifest_fehler, lokale_abweichungen und check_manifest."""

    def test_lokale_abweichungen_defensive_types(self):
        # Darf nicht mit TypeError abstürzen bei None oder ungültigem Typ
        self.assertEqual(shell_uebernehmen.lokale_abweichungen(Path("."), None), [])
        self.assertEqual(shell_uebernehmen.lokale_abweichungen(Path("."), {}), [])
        self.assertEqual(shell_uebernehmen.lokale_abweichungen(Path("."), {"dateien": "kein_dict"}), [])

    def test_manifest_fehler_validierung(self):
        self.assertEqual(shell_uebernehmen.manifest_fehler("kein_dict"), ["kein JSON-Objekt"])

        daten_ungueltig = {
            "paket": "falsches_paket",
            "lizenz": "GPL-3.0",
            "shell_version": "nicht-semver",
            "quell_commit": "nicht-hex-40",
            "dateien": "kein_dict",
        }
        fehler = shell_uebernehmen.manifest_fehler(daten_ungueltig)
        self.assertTrue(any("paket ist nicht" in f for f in fehler))
        self.assertTrue(any("lizenz ist nicht MPL-2.0" in f for f in fehler))
        self.assertTrue(any("shell_version fehlt oder ist kein SemVer" in f for f in fehler))
        self.assertTrue(any("quell_commit ist kein Commit-Hash" in f for f in fehler))
        self.assertTrue(any("dateien fehlt oder nennt kein __init__.py" in f for f in fehler))

    def test_check_manifest_corrupted_json(self):
        with tempfile.TemporaryDirectory(prefix="glide-manifest-test-") as temp_dir:
            p = Path(temp_dir)
            manifest = p / "SHELL_MANIFEST.json"
            manifest.write_text("{defektes: json", encoding="utf-8")

            with self.assertRaises(AssertionError) as ctx:
                selftest.check_manifest(folder=p)
            self.assertIn("not valid JSON", str(ctx.exception))

    def test_check_manifest_non_dict_json(self):
        with tempfile.TemporaryDirectory(prefix="glide-manifest-test-") as temp_dir:
            p = Path(temp_dir)
            manifest = p / "SHELL_MANIFEST.json"
            manifest.write_text('["eintrag1", "eintrag2"]', encoding="utf-8")

            with self.assertRaises(AssertionError) as ctx:
                selftest.check_manifest(folder=p)
            self.assertIn("not a JSON object", str(ctx.exception))


class BootstrapCommandTests(unittest.TestCase):
    """Testet plattformgerechte Bootstrap-Kommandos unter Berücksichtigung von Leerzeichen und Sonderzeichen."""

    def test_bootstrap_inhalte_spaces_and_symbols(self):
        with tempfile.TemporaryDirectory(prefix="glide-bootstrap-test-") as temp_dir:
            root = Path(temp_dir) / "Mein Projekt" / "V1 (2026)"
            shell = root / "src" / "app core" / "glide_shell"
            shell.mkdir(parents=True)
            for name in ("KI_ANLEITUNG_NEUE_PROJEKTE.md", "AI_GUIDE_NEW_PROJECTS.md",
                         "STARTPROMPT_KI.md", "DESIGN_RICHTLINIEN.md", "SHELL_MANIFEST.json"):
                (shell / name).write_text("# Test\n", encoding="utf-8")

            inhalt_agents, _, _ = shell_uebernehmen.generiere_bootstrap_inhalte(root, shell)
            self.assertIn("python3 -m glide_shell.selftest", inhalt_agents)
            # Enthält ordnungsgemäß gequoteten cd-Befehl für POSIX und PowerShell
            self.assertIn("cd 'src/app core' && python3 -m glide_shell.selftest", inhalt_agents)
            self.assertIn("cd -LiteralPath 'src/app core'; python -m glide_shell.selftest", inhalt_agents)
            self.assertNotIn('cd "src/app core" &&', inhalt_agents)

    def test_bootstrap_inhalte_variables_and_quotes(self):
        import shlex
        with tempfile.TemporaryDirectory(prefix="glide-bootstrap-test-") as temp_dir:
            root = Path(temp_dir) / "Mein $VAR Projekt"
            shell = root / "src" / "app 'core'" / "glide_shell"
            shell.mkdir(parents=True)
            for name in ("KI_ANLEITUNG_NEUE_PROJEKTE.md", "AI_GUIDE_NEW_PROJECTS.md",
                         "STARTPROMPT_KI.md", "DESIGN_RICHTLINIEN.md", "SHELL_MANIFEST.json"):
                (shell / name).write_text("# Test\n", encoding="utf-8")

            inhalt_agents, _, _ = shell_uebernehmen.generiere_bootstrap_inhalte(root, shell)
            # shlex.quote schützt Single Quotes und Variablen vor zsh/bash Expansion
            q_target = "src/app 'core'"
            expected_posix = f"cd {shlex.quote(q_target)} && python3 -m glide_shell.selftest"
            self.assertIn(expected_posix, inhalt_agents)
            # PowerShell entwertet ' durch '' und verwendet -LiteralPath
            self.assertIn("cd -LiteralPath 'src/app ''core'''; python -m glide_shell.selftest", inhalt_agents)


class WidgetIntegration102Tests(unittest.TestCase):
    """Echte Tk-Widget-Tests für Sprachumschaltung, DueField-Formatierung und Bildumfluss."""

    @classmethod
    def setUpClass(cls):
        try:
            cls.root = tk.Tk()
            cls.root.withdraw()
            cls.tk_available = True
        except tk.TclError:
            cls.tk_available = False

    @classmethod
    def tearDownClass(cls):
        if getattr(cls, "tk_available", False) and getattr(cls, "root", None):
            try:
                cls.root.destroy()
            except tk.TclError:
                pass

    def setUp(self):
        if not self.tk_available:
            self.skipTest("Kein Tkinter Display verfuegbar")

    def test_due_field_on_date_focus_out_formatting(self):
        """Testet echtes DueField-Widget mit Parsing von 'today', 'tomorrow', 'yesterday' und read()."""
        app_mod = lade_app()
        ref_today = date(2026, 11, 23)

        class AppAdapter:
            def __init__(self, today_ref):
                self.theme = {
                    "input": "#ffffff", "text": "#000000", "selection": "#0000ff",
                    "selection_text": "#ffffff", "bg": "#f0f0f0", "card": "#ffffff",
                    "muted": "#888888", "placeholder": "#aaaaaa", "ui_accent": "#0000ff"
                }
                self.settings = {"week_start": "monday"}
                self.WEEKDAYS_DE = app_mod.ListApp.WEEKDAYS_DE
                self.MONTHS_DE = app_mod.ListApp.MONTHS_DE
                self.DUE_WORDS = app_mod.ListApp.DUE_WORDS
                self.FIELD_BORDER_WIDTH = 1
                self.FIELD_LABEL_GAP = 4
                self.FIELD_PAD_X = 4
                self.FIELD_PAD_Y = 2
                self.ICONS = {"calendar": "cal"}
                self._today_ref = today_ref

            def _make_field_label(self, parent, text):
                return tk.Label(parent, text=text)

            def _make_field(self, parent):
                b = tk.Frame(parent)
                f = tk.Frame(b)
                return b, f

            def normalize_due(self, due):
                return app_mod.ListApp.normalize_due(due)

            def normalize_due_time(self, t):
                return app_mod.ListApp.normalize_due_time(t)

            def parse_due_words(self, text):
                return app_mod.ListApp.parse_due_words(text, today=self._today_ref)

            def parse_due_time_input(self, t):
                return app_mod.ListApp.parse_due_time_input(t)

            def format_due_display(self, d):
                return app_mod.ListApp.format_due_display(d)

            def shift_month(self, y, m, d):
                return app_mod.ListApp.shift_month(y, m, d)

            def calendar_month_grid(self, y, m):
                return app_mod.ListApp.calendar_month_grid(y, m)

            def _make_dialog_button(self, parent, *args, **kwargs):
                return tk.Button(parent)

            def _make_calendar_surface(self, parent):
                b = tk.Frame(parent)
                f = tk.Frame(b)
                return b, f

        app_obj = AppAdapter(ref_today)
        field = app_mod.DueField(self.root, app_obj, compact=True)
        entry = field.date_entry

        # 1. 'today' tippen und Fokus verlieren -> wird formatiert
        entry.delete(0, tk.END)
        entry.insert(0, "today")
        field._on_date_focus_out()
        self.assertEqual(entry.get(), "23.11.2026")
        res, err = field.read()
        self.assertIsNone(err)
        self.assertEqual(res, ("2026-11-23", None))

        # 2. 'tomorrow' tippen
        entry.delete(0, tk.END)
        entry.insert(0, "tomorrow")
        field._on_date_focus_out()
        self.assertEqual(entry.get(), "24.11.2026")
        res, err = field.read()
        self.assertIsNone(err)
        self.assertEqual(res, ("2026-11-24", None))

        # 3. 'yesterday' tippen
        entry.delete(0, tk.END)
        entry.insert(0, "yesterday")
        field._on_date_focus_out()
        self.assertEqual(entry.get(), "22.11.2026")
        res, err = field.read()
        self.assertIsNone(err)
        self.assertEqual(res, ("2026-11-22", None))

        # 4. Standard ISO / deutsches Format
        entry.delete(0, tk.END)
        entry.insert(0, "15.12.2026")
        field._on_date_focus_out()
        res, err = field.read()
        self.assertIsNone(err)
        self.assertEqual(res, ("2026-12-15", None))

        # 5. Ungültiges Wort -> Fehlermeldung
        entry.delete(0, tk.END)
        entry.insert(0, "kein-datum")
        field._on_date_focus_out()
        res, err = field.read()
        self.assertIsNone(res)
        self.assertIn("TT.MM.JJJJ", err)

        # 6. Leeres Feld -> (None, None)
        entry.delete(0, tk.END)
        res, err = field.read()
        self.assertEqual(res, (None, None))
        self.assertIsNone(err)

        field.destroy()

    def test_tag_flow_wrap_mode(self):
        """Prüft, dass imgflow (left und right) sowie cornerflow wrap='word' setzen."""
        text = tk.Text(self.root)
        text.tag_configure('cornerflow', rmargin=60, wrap='word')
        self.assertEqual(text.tag_cget('cornerflow', 'wrap'), 'word')

        text.tag_configure('imgflow:r1', rmargin=120, wrap='word')
        self.assertEqual(text.tag_cget('imgflow:r1', 'wrap'), 'word')

        text.tag_configure('imgflow:l1', lmargin1=120, lmargin2=120, wrap='word')
        self.assertEqual(text.tag_cget('imgflow:l1', 'wrap'), 'word')

        # Text einfügen und Tags anwenden
        text.insert('1.0', "Ein langer Text, der ohne Überlappung um das Bild oder die Tabelle fließen soll.")
        text.tag_add('cornerflow', '1.0', '1.20')
        self.assertTrue(bool(text.tag_ranges('cornerflow')))
        text.destroy()

    def test_corner_cover_lifecycle_and_clear(self):
        """Prüft den Lebenszyklus des Pixel-Ecksymbols und sauberes Entfernen via clear_corner_cover."""
        app_mod = lade_app()
        text = tk.Text(self.root, wrap='word')
        text.insert('1.0', "Titel der Seite\nErste Inhaltszeile mit fortlaufendem Text.")
        text.tag_configure('cornerflow', rmargin=66, wrap='word')
        text.tag_add('cornerflow', '1.0', '1.15')
        text.tag_add('imgend:corner', '1.15', '1.16')

        label = tk.Label(text, text="🎨")

        class EditorMock:
            def __init__(self, t, lbl):
                self.text = t
                self._corner_cover = lbl
            clear_corner_cover = app_mod.PageEditor.clear_corner_cover

        editor = EditorMock(text, label)
        self.assertTrue(label.winfo_exists())
        self.assertTrue(bool(text.tag_ranges('cornerflow')))

        editor.clear_corner_cover()
        self.assertIsNone(editor._corner_cover)
        self.assertFalse(label.winfo_exists())
        self.assertFalse(bool(text.tag_ranges('cornerflow')))
        self.assertFalse(bool(text.tag_ranges('imgend:corner')))

        text.destroy()

    def test_sync_foot_density_behavior(self):
        """Prüft Ausblenden und Einblenden des Erwähnt-Knopfs bei minimaler Kopfstufe mit echten Widgets."""
        app_mod = lade_app()

        container = tk.Frame(self.root)
        container.pack()
        status = tk.Label(container, text="3 Seiten")
        status.pack(side="left")
        knopf = tk.Button(container, text="Erwähnt ohne Verweis (3)")
        knopf.pack(side="left", before=status)

        class DensityAppAdapter:
            def __init__(self, density):
                self._density = density
            def header_density(self):
                return self._density

        class RealEditorFoot:
            def __init__(self, btn, st, d_app):
                self._mentions_button = btn
                self.status = st
                self.app = d_app
                self._mentions_open = False
            sync_foot_density = app_mod.PageEditor.sync_foot_density

        # Fall 1: Minimale Dichte, Erwähnungen zu -> Button wird ausgeblendet
        editor = RealEditorFoot(knopf, status, DensityAppAdapter("minimal"))
        self.assertTrue(bool(knopf.winfo_manager()))
        editor.sync_foot_density()
        self.assertFalse(bool(knopf.winfo_manager()))

        # Fall 2: Normale Dichte -> Button wird wieder vor dem Status eingeblendet
        editor.app = DensityAppAdapter("normal")
        editor.sync_foot_density()
        self.assertTrue(bool(knopf.winfo_manager()))
        self.assertEqual(knopf.winfo_manager(), "pack")

        # Fall 3: Minimale Dichte, aber Erwähnungen offen -> Button bleibt sichtbar
        editor.app = DensityAppAdapter("minimal")
        editor._mentions_open = True
        editor.sync_foot_density()
        self.assertTrue(bool(knopf.winfo_manager()))

        container.destroy()

    def test_sidebar_locale_refresh(self):
        """Prüft Umschaltung DE -> EN -> DE mit echten Labels, Pfeil-Icons und Add-Buttons."""
        app_mod = lade_app()

        container = tk.Frame(self.root)
        label_lists = tk.Label(container, text="Listen")
        label_pages = tk.Label(container, text="Seiten")
        label_notes = tk.Label(container, text="Notizen")
        label_drawings = tk.Label(container, text="Zeichnungen")

        icon_lists = tk.Label(container, text="v")
        icon_pages = tk.Label(container, text="v")
        icon_notes = tk.Label(container, text="v")
        icon_drawings = tk.Label(container, text="v")

        btn_pages = tk.Button(container, text="+")
        btn_notes = tk.Button(container, text="+")
        btn_drawings = tk.Button(container, text="+")

        class RealAppWithSidebar:
            def __init__(self):
                self.sidebar_title = label_lists
                self.pages_title = label_pages
                self.notes_title = label_notes
                self.drawings_title = label_drawings
                self.sidebar_heading_icon = icon_lists
                self.pages_heading_icon = icon_pages
                self.notes_heading_icon = icon_notes
                self.drawings_heading_icon = icon_drawings
                self.add_pages_button = btn_pages
                self.add_notes_button = btn_notes
                self.add_drawings_button = btn_drawings
                self.tooltips = {}
            def add_tooltip(self, widget, text):
                self.tooltips[widget] = text
            refresh_sidebar_locale = app_mod.ListApp.refresh_sidebar_locale

        app_instance = RealAppWithSidebar()

        # Umschaltung auf Englisch
        i18n.set_language("en")
        app_instance.refresh_sidebar_locale()
        self.assertEqual(label_lists.cget("text"), "Lists")
        self.assertEqual(label_pages.cget("text"), "Pages")
        self.assertEqual(label_notes.cget("text"), "Notes")
        self.assertEqual(label_drawings.cget("text"), "Drawings")
        self.assertEqual(app_instance.tooltips.get(label_lists), "Show all lists and folders as tiles")
        self.assertEqual(app_instance.tooltips.get(label_pages), "All pages with favorites and recently opened")
        self.assertEqual(app_instance.tooltips.get(label_notes), "All notes and notebooks")
        self.assertEqual(app_instance.tooltips.get(label_drawings), "All drawings")

        # Umschaltung zurück auf Deutsch
        i18n.set_language("de")
        app_instance.refresh_sidebar_locale()
        self.assertEqual(label_lists.cget("text"), "Listen")
        self.assertEqual(label_pages.cget("text"), "Seiten")
        self.assertEqual(label_notes.cget("text"), "Notizen")
        self.assertEqual(label_drawings.cget("text"), "Zeichnungen")
        self.assertEqual(app_instance.tooltips.get(label_lists), "Alle Listen und Ordner als Kacheln anzeigen")
        self.assertEqual(app_instance.tooltips.get(label_pages), "Alle Seiten mit Favoriten und Zuletzt geöffnet")
        self.assertEqual(app_instance.tooltips.get(label_notes), "Alle Notizen und Notizbücher")
        self.assertEqual(app_instance.tooltips.get(label_drawings), "Alle Zeichnungen")

        container.destroy()


if __name__ == "__main__":
    unittest.main()
