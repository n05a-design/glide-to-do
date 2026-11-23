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
import drawing as glide_drawing
import drawing_image as glide_drawing_image
import image_preview


def erstelle_test_ppm(pfad, breite, hoehe, farbe=(120, 160, 200)):
    """Erzeugt ein valides PPM-Testbild (P6) ohne externe Bibliotheken."""
    kopf = f"P6\n{breite} {hoehe}\n255\n".encode("ascii")
    pixel = bytes(farbe)
    pfad.write_bytes(kopf + pixel * (breite * hoehe))

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


_SHARED_ROOT = None

def get_shared_root():
    """Gemeinsame tk.Tk()-Instanz für die Testsuite zur Vermeidung von Mehrfachinitialisierungen."""
    global _SHARED_ROOT
    if _SHARED_ROOT is None:
        try:
            _SHARED_ROOT = tk.Tk()
            _SHARED_ROOT.withdraw()
        except tk.TclError as exc:
            if os.environ.get("GLIDE_REQUIRE_TK") == "1":
                raise RuntimeError(f"GLIDE_REQUIRE_TK=1 ist aktiv, aber Tk konnte nicht initialisiert werden: {exc}") from exc
            _SHARED_ROOT = False
    if _SHARED_ROOT is False and os.environ.get("GLIDE_REQUIRE_TK") == "1":
        raise RuntimeError("GLIDE_REQUIRE_TK=1 ist aktiv, aber kein Tk-Display verfügbar!")
    return _SHARED_ROOT if _SHARED_ROOT is not False else None


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
        root = get_shared_root()
        if not root:
            if os.environ.get("GLIDE_REQUIRE_TK") == "1":
                self.fail("GLIDE_REQUIRE_TK=1: Kein Display verfuegbar")
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

    def test_adaptive_cover_crop_production_integration(self):
        """Testet make_page_cover() unter realistischen Bedingungen mit echten Bildern und Größenänderungen.

        Prüft:
        - 300px Breite -> geklemmt auf min 110px
        - 500px Breite -> 170px (500 * 0.34)
        - 1000px Breite -> geklemmt auf max 240px
        - Hochformat (400x800) mit Fokuspunkt (oben = -round((image.height() - cover_h) * 0.38))
        - Querformat (1200x400)
        - Quadratisches Bild (500x500)
        - Sehr kleines Ausgangsbild (50x50) mit Begrenzung der Skalierung (COVER_MAX_UPSCALE = 1.5 -> 75px)
        - Fehlendes Bild und beschädigtes Bild (Fallback-Text ohne Absturz)
        - Negativgegenprobe: erkennt fehlerhafte Implementierung des Verhältnisses oder des Fokuspunkts.
        """
        app_mod = lade_app()
        root = get_shared_root()
        if not root:
            if os.environ.get("GLIDE_REQUIRE_TK") == "1":
                self.fail("GLIDE_REQUIRE_TK=1: Kein Display verfuegbar")
            self.skipTest("Kein Display verfuegbar")
        for child in list(root.winfo_children()):
            try:
                child.destroy()
            except tk.TclError:
                pass
        root.withdraw()
        root.deiconify()
        root.geometry("500x400")
        root.update()

        with tempfile.TemporaryDirectory(prefix="glide-cover-crop-") as temp_dir:
            td = Path(temp_dir)
            p_portrait = td / "portrait.ppm"
            erstelle_test_ppm(p_portrait, 400, 800)

            p_landscape = td / "landscape.ppm"
            erstelle_test_ppm(p_landscape, 1200, 400)

            p_square = td / "square.ppm"
            erstelle_test_ppm(p_square, 500, 500)

            p_tiny = td / "tiny.ppm"
            erstelle_test_ppm(p_tiny, 50, 50)

            p_corrupt = td / "corrupt.ppm"
            p_corrupt.write_bytes(b"ungueltige_bilddaten_ohne_header\n")

            cache = image_preview.PreviewCache(cache_dir=str(td / "cache"))

            class CoverProductionAdapter:
                COVER_RATIO = app_mod.ListApp.COVER_RATIO
                COVER_MAX_HEIGHT = app_mod.ListApp.COVER_MAX_HEIGHT
                COVER_FOCUS = app_mod.ListApp.COVER_FOCUS
                COVER_MAX_UPSCALE = app_mod.ListApp.COVER_MAX_UPSCALE
                theme = {"input": "#ffffff", "muted": "#888888"}
                previews = cache
                make_page_cover = app_mod.ListApp.make_page_cover

                def resolve_attachment_path(self, a):
                    return str(td / a["name"]) if a else None

            app_obj = CoverProductionAdapter()

            # 1. Breiten-Matrix und Hochformat
            entry_portrait = {
                "cover": {"kind": "image", "attachment": "att_port"},
                "attachments": [{"id": "att_port", "name": "portrait.ppm"}]
            }
            canvas = app_obj.make_page_cover(root, entry_portrait, height=110, adaptive=True)
            canvas.pack(fill="x")
            root.update()

            # Bei 500px: Höhe 170
            self.assertEqual(canvas.winfo_width(), 500)
            self.assertEqual(int(float(canvas.cget("height"))), 170)
            photo = getattr(canvas, "_photo", None)
            self.assertIsNotNone(photo)
            # Fokuspunkt-Rechnung prüfen: Y-Position des Fotos ist -round((image.height() - 170) * 0.38)
            coords = canvas.coords(canvas.find_all()[0])
            oben_erwartet = -round((photo.height() - 170) * app_mod.ListApp.COVER_FOCUS)
            self.assertEqual(coords, [250.0, float(oben_erwartet)])

            # Bei 300px: Geklemmt auf Minimum 110px
            root.geometry("300x400")
            root.update()
            canvas.event_generate("<Configure>", width=300)
            root.update()
            self.assertEqual(int(float(canvas.cget("height"))), 110)

            # Bei 1000px: Geklemmt auf Maximum 240px
            root.geometry("1000x400")
            root.update()
            canvas.event_generate("<Configure>", width=1000)
            root.update()
            self.assertEqual(int(float(canvas.cget("height"))), 240)
            canvas.destroy()

            # 2. Querformat und Quadrat
            root.geometry("500x400")
            root.update()
            entry_landscape = {
                "cover": {"kind": "image", "attachment": "att_land"},
                "attachments": [{"id": "att_land", "name": "landscape.ppm"}]
            }
            c_land = app_obj.make_page_cover(root, entry_landscape, height=110, adaptive=True)
            c_land.pack(fill="x")
            root.update()
            self.assertEqual(int(float(c_land.cget("height"))), 170)
            self.assertIsNotNone(getattr(c_land, "_photo", None))
            c_land.destroy()

            entry_square = {
                "cover": {"kind": "image", "attachment": "att_sq"},
                "attachments": [{"id": "att_sq", "name": "square.ppm"}]
            }
            c_sq = app_obj.make_page_cover(root, entry_square, height=110, adaptive=True)
            c_sq.pack(fill="x")
            root.update()
            self.assertEqual(int(float(c_sq.cget("height"))), 170)
            self.assertIsNotNone(getattr(c_sq, "_photo", None))
            c_sq.destroy()

            # 3. Sehr kleines Bild: Skalierungsgrenze (COVER_MAX_UPSCALE)
            entry_tiny = {
                "cover": {"kind": "image", "attachment": "att_tiny"},
                "attachments": [{"id": "att_tiny", "name": "tiny.ppm"}]
            }
            c_tiny = app_obj.make_page_cover(root, entry_tiny, height=110, adaptive=True)
            c_tiny.pack(fill="x")
            root.update()
            photo_tiny = getattr(c_tiny, "_photo", None)
            self.assertIsNotNone(photo_tiny)
            # 50px * 1.5 = 75px; darf keinesfalls auf 500px aufgeblasen werden
            self.assertEqual(photo_tiny.width(), 75)
            self.assertLess(photo_tiny.width(), 500)
            c_tiny.destroy()

            # 4. Fehlendes Bild -> Fallback-Text
            entry_missing = {
                "cover": {"kind": "image", "attachment": "nicht_vorhanden"},
                "attachments": []
            }
            c_missing = app_obj.make_page_cover(root, entry_missing, height=110, adaptive=True)
            c_missing.pack(fill="x")
            root.update()
            self.assertIsNone(getattr(c_missing, "_photo", None))
            text_items = [i for i in c_missing.find_all() if c_missing.type(i) == "text"]
            self.assertTrue(len(text_items) > 0)
            c_missing.destroy()

            # 5. Beschädigtes Bild -> Fallback-Text ohne Exception
            entry_corrupt = {
                "cover": {"kind": "image", "attachment": "att_corrupt"},
                "attachments": [{"id": "att_corrupt", "name": "corrupt.ppm"}]
            }
            c_corrupt = app_obj.make_page_cover(root, entry_corrupt, height=110, adaptive=True)
            c_corrupt.pack(fill="x")
            root.update()
            self.assertIsNone(getattr(c_corrupt, "_photo", None))
            c_corrupt.destroy()

        for child in list(root.winfo_children()):
            try:
                child.destroy()
            except tk.TclError:
                pass
        root.withdraw()


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
            self.assertIn("Set-Location -LiteralPath 'src/app core' -ErrorAction Stop; python -m glide_shell.selftest", inhalt_agents)
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
            # PowerShell entwertet ' durch '' und verwendet Set-Location -LiteralPath mit -ErrorAction Stop
            self.assertIn("Set-Location -LiteralPath 'src/app ''core''' -ErrorAction Stop; python -m glide_shell.selftest", inhalt_agents)


class WidgetIntegration102Tests(unittest.TestCase):
    """Echte Tk-Widget-Tests für Sprachumschaltung, DueField-Formatierung und Bildumfluss."""

    @classmethod
    def setUpClass(cls):
        cls.root = get_shared_root()
        cls.tk_available = cls.root is not None
        if not cls.tk_available and os.environ.get("GLIDE_REQUIRE_TK") == "1":
            raise RuntimeError("GLIDE_REQUIRE_TK=1 ist gesetzt, aber kein Tk-Display verfügbar!")

    def setUp(self):
        if not self.tk_available:
            if os.environ.get("GLIDE_REQUIRE_TK") == "1":
                self.fail("GLIDE_REQUIRE_TK=1: Kein Tkinter Display verfuegbar")
            self.skipTest("Kein Tkinter Display verfuegbar")
        for child in list(self.root.winfo_children()):
            try:
                child.destroy()
            except tk.TclError:
                pass
        self.root.deiconify()
        self.root.geometry("600x500")
        self.root.update()

    def tearDown(self):
        if getattr(self, "tk_available", False) and getattr(self, "root", None):
            for child in list(self.root.winfo_children()):
                try:
                    child.destroy()
                except tk.TclError:
                    pass
            try:
                self.root.withdraw()
                self.root.update_idletasks()
            except tk.TclError:
                pass

    def _make_due_app_adapter(self, app_mod, today_ref=None):
        class DueAppAdapter:
            def __init__(self, t_ref):
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
                self._today_ref = t_ref or date.today()

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

        return DueAppAdapter(today_ref)

    def test_due_field_on_date_focus_out_formatting(self):
        """Testet echtes DueField-Widget mit Parsing von 'today', 'tomorrow', 'yesterday' und read()."""
        app_mod = lade_app()
        ref_today = date(2026, 11, 23)
        app_obj = self._make_due_app_adapter(app_mod, ref_today)
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

        # 2. 'tomorrow' tippen und mit Enter bestätigen (über <Return>-Handler)
        entry.delete(0, tk.END)
        entry.insert(0, "tomorrow")
        field._on_date_focus_out()  # <Return> ruft denselben Handler wie <FocusOut> auf
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

        # 5. Rundenlauf: Speicherung im Item-Objekt und erneutes Auslesen
        item = {"title": "Aufgabe", "due": None}
        item["due"] = res[0]
        self.assertEqual(item["due"], "2026-12-15")

        # 6. Ungültiges Wort -> Fehlermeldung
        entry.delete(0, tk.END)
        entry.insert(0, "kein-datum")
        field._on_date_focus_out()
        res, err = field.read()
        self.assertIsNone(res)
        self.assertIn("TT.MM.JJJJ", err)

        # 7. Leeres Feld -> (None, None)
        entry.delete(0, tk.END)
        res, err = field.read()
        self.assertEqual(res, (None, None))
        self.assertIsNone(err)

        field.destroy()

    def test_due_field_real_persistence_lifecycle(self):
        """Verifiziert den vollständigen Persistenzpfad natürlicher Fälligkeiten über DueField und Dateispeicherung.

        Ablauf:
        1. Aufgabe anlegen
        2. Natürliche Eingabe ('today' und 'tomorrow') im DueField-Widget tätigen
        3. Dialog-Übernahme simulieren (<Return>/FocusOut und read())
        4. Echten atomaren Speichermechanismus (write_json_atomic mit Format 26) ausführen
        5. Datei von Platte neu einlesen und gespeichertes ISO-Datum validieren
        6. Reimportiertes Datum im DueField erneut darstellen
        7. Sicherstellen, dass das angezeigte formatiertes Datum zum gespeicherten ISO-Datum passt.
        """
        app_mod = lade_app()
        ref_today = date.today()
        ref_tomorrow = ref_today + timedelta(days=1)

        with tempfile.TemporaryDirectory(prefix="glide-due-persist-") as temp_dir:
            save_path = Path(temp_dir) / "aufgaben.json"

            # 1. & 2. Aufgabe mit DueField bearbeiten: 'today'
            app_mock_today = self._make_due_app_adapter(app_mod, ref_today)
            field_today = app_mod.DueField(self.root, app_mock_today, due=None, compact=True)
            field_today.date_entry.delete(0, tk.END)
            field_today.date_entry.insert(0, "today")
            field_today._on_date_focus_out()
            val_today, err_today = field_today.read()
            self.assertIsNone(err_today)
            self.assertEqual(val_today, (ref_today.isoformat(), None))
            iso_today = val_today[0]

            # 3. & 4. In Datenstruktur überführen und atomar speichern
            item1 = {"id": "t_persist_today", "title": "Aufgabe Heute", "due": iso_today}
            payload1 = {
                "format": 26,
                "version": "1.0.2",
                "lists": [{"id": "list_due_1", "name": "Persistenzliste", "items": [item1]}]
            }
            app_mod.ListApp.write_json_atomic(str(save_path), payload1)
            self.assertTrue(save_path.is_file())

            # 5. Von Platte neu einlesen
            loaded1 = json.loads(save_path.read_text(encoding="utf-8"))
            reloaded_item1 = loaded1["lists"][0]["items"][0]
            self.assertEqual(reloaded_item1["due"], ref_today.isoformat())

            # 6. & 7. Erneut im DueField darstellen und prüfen
            field_reloaded1 = app_mod.DueField(self.root, app_mock_today, due=reloaded_item1["due"], compact=True)
            self.assertEqual(field_reloaded1.date_entry.get(), ref_today.strftime("%d.%m.%Y"))
            self.assertEqual(field_reloaded1.read(), ((ref_today.isoformat(), None), None))

            field_today.destroy()
            field_reloaded1.destroy()

            # Gegenprobe mit 'tomorrow'
            app_mock_tom = self._make_due_app_adapter(app_mod, ref_today)
            field_tomorrow = app_mod.DueField(self.root, app_mock_tom, due=None, compact=True)
            field_tomorrow.date_entry.delete(0, tk.END)
            field_tomorrow.date_entry.insert(0, "tomorrow")
            field_tomorrow._on_date_focus_out()
            val_tom, err_tom = field_tomorrow.read()
            self.assertIsNone(err_tom)
            self.assertEqual(val_tom, (ref_tomorrow.isoformat(), None))
            iso_tom = val_tom[0]

            item2 = {"id": "t_persist_tom", "title": "Aufgabe Morgen", "due": iso_tom}
            payload2 = {
                "format": 26,
                "version": "1.0.2",
                "lists": [{"id": "list_due_2", "name": "Persistenzliste 2", "items": [item2]}]
            }
            app_mod.ListApp.write_json_atomic(str(save_path), payload2)

            loaded2 = json.loads(save_path.read_text(encoding="utf-8"))
            reloaded_item2 = loaded2["lists"][0]["items"][0]
            self.assertEqual(reloaded_item2["due"], ref_tomorrow.isoformat())

            field_reloaded2 = app_mod.DueField(self.root, app_mock_tom, due=reloaded_item2["due"], compact=True)
            self.assertEqual(field_reloaded2.date_entry.get(), ref_tomorrow.strftime("%d.%m.%Y"))
            self.assertEqual(field_reloaded2.read(), ((ref_tomorrow.isoformat(), None), None))

            field_tomorrow.destroy()
            field_reloaded2.destroy()

    def test_page_editor_flow_around_and_table_wrap(self):
        """Prüft den produktiven Layoutpfad des Seiteneditors mit echtem Text, Tabelle und Bildumfluss.

        Verifiziert:
        - Text umfließt linksbündiges Bild (imgflow:l1, lmargin1/lmargin2 gesetzt, wrap='word')
        - Text umfließt rechtsbündiges Bild (imgflow:r1, rmargin gesetzt, wrap='word')
        - Tabelle ist format-isoliert (Tag 'table' besitzt wrap='none')
        - flow_around berechnet Zeilenanzahl exakt anhand der Bildhöhe
        - Neuberechnung bei Größenänderungen des Fensters.
        """
        app_mod = lade_app()
        text = tk.Text(self.root, wrap='word', padx=20, pady=10)
        text.pack(fill='both', expand=True)

        # Textabschnitt 1
        text.insert('1.0', "Absatz vor dem ersten Bild. " * 4 + "\n\n")

        # Linksbündiges Bild
        anchor_l1 = text.index('end -1c')
        text.insert('end', "Bildanker Links\n")
        text.insert('end', ("Text fließt rechts am linksbündigen Bild vorbei. " * 8) + "\n\n")

        # Tabellenblock (Markdown-Tabelle)
        anchor_table = text.index('end -1c')
        table_lines = "| Spalte 1 | Spalte 2 | Spalte 3 |\n| --- | --- | --- |\n| Wert A | Wert B | Wert C |\n"
        text.insert('end', table_lines + "\n")
        end_table = text.index('end -1c')
        text.tag_add('table', anchor_table, end_table)
        text.tag_configure('table', lmargin1=14, lmargin2=14, spacing1=0, spacing3=0, wrap='none')

        # Rechtsbündiges Bild
        anchor_r1 = text.index('end -1c')
        text.insert('end', "Bildanker Rechts\n")
        text.insert('end', ("Text fließt links am rechtsbündigen Bild vorbei. " * 8) + "\n\n")

        self.root.update()

        class FlowEditorAdapter:
            def __init__(self, t):
                self.text = t
            flow_around = app_mod.PageEditor.flow_around
            ypixels = app_mod.PageEditor.ypixels
            column_bounds = app_mod.PageEditor.column_bounds

        editor = FlowEditorAdapter(text)

        # Umfluss anwenden
        text.tag_configure('imgflow:l1', lmargin1=120, lmargin2=120, wrap='word')
        editor.flow_around('imgflow:l1', anchor_l1, 70, 'l1')

        text.tag_configure('imgflow:r1', rmargin=120, wrap='word')
        editor.flow_around('imgflow:r1', anchor_r1, 70, 'r1')

        self.root.update()

        # Prüfungen
        self.assertEqual(text.tag_cget('table', 'wrap'), 'none')
        self.assertEqual(text.tag_cget('imgflow:l1', 'wrap'), 'word')
        self.assertEqual(text.tag_cget('imgflow:r1', 'wrap'), 'word')
        self.assertEqual(int(float(text.tag_cget('imgflow:l1', 'lmargin1'))), 120)
        self.assertEqual(int(float(text.tag_cget('imgflow:r1', 'rmargin'))), 120)

        # Tag-Bereiche müssen exakt vorhanden und beschränkt sein
        ranges_l1 = text.tag_ranges('imgflow:l1')
        ranges_r1 = text.tag_ranges('imgflow:r1')
        self.assertTrue(bool(ranges_l1))
        self.assertTrue(bool(ranges_r1))

        # Geometrische Überprüfungen via Tk-API (bbox, dlineinfo, column_bounds):
        # 1. Text neben linksbündigem Bild:
        # Erste Zeile des Umflusses muss messbar um den linken Rand versetzt sein
        l1_start = ranges_l1[0]
        dline_normal = text.dlineinfo('1.0')
        dline_flow_l = text.dlineinfo(l1_start)
        if dline_normal and dline_flow_l:
            self.assertGreaterEqual(dline_flow_l[0], 120)
            self.assertGreater(dline_flow_l[0], dline_normal[0])

        # 2. Text neben rechtsbündigem Bild:
        r1_start = ranges_r1[0]
        dline_flow_r = text.dlineinfo(r1_start)
        if dline_flow_r:
            self.assertLessEqual(dline_flow_r[0] + dline_flow_r[2], text.winfo_width())

        # 3. Tabellenbereich: Tag 'table' besitzt wrap='none' und lmargin1=14
        # Tabelle darf keine Umflussträger enthalten (Ausschluss räumlicher Überlappung)
        table_start_idx = text.index(anchor_table)
        table_end_idx = text.index(end_table)
        self.assertTrue(text.compare(ranges_l1[-1], '<=', table_start_idx))
        self.assertTrue(text.compare(ranges_r1[0], '>=', table_end_idx))

        # 4. Verhalten bei schmalem Fenster (400 px) vs breitem Fenster (850 px)
        self.root.geometry("400x450")
        self.root.update()
        rand_s, spalte_s = editor.column_bounds()
        self.assertLessEqual(spalte_s, 400)
        editor.flow_around('imgflow:l1', anchor_l1, 70, 'l1')
        self.root.update()

        self.root.geometry("850x550")
        self.root.update()
        rand_b, spalte_b = editor.column_bounds()
        self.assertGreater(spalte_b, spalte_s)
        editor.flow_around('imgflow:l1', anchor_l1, 70, 'l1')
        self.root.update()
        self.assertTrue(bool(text.tag_ranges('imgflow:l1')))

        text.destroy()

    def test_corner_cover_full_lifecycle(self):
        """Prüft den vollständigen Lebenszyklus des Pixel-Ecksymbols mit echten Produktionsfunktionen.

        Schritte:
        1. show_corner_cover mit echtem DrawingModel
        2. Anfangsplatzierung rechts oben in der Lesespalte
        3. Umfluss mit cornerflow (wrap='word', rmargin)
        4. Text-Scrollen und place_corner_cover
        5. Aktualisierung bei Größenänderung (layout_corner_cover)
        6. Ersetzen durch ein zweites Cover
        7. Vollständige Bereinigung via clear_corner_cover (keine verwaisten Widgets/Tags).
        """
        app_mod = lade_app()
        text = tk.Text(self.root, wrap='word', padx=20, pady=10)
        text.pack(fill='both', expand=True)

        long_para = "Titel der Seite\n" + ("Fließtext der Seite, der neben dem Pixel-Ecksymbol umbricht. " * 6) + "\n\n"
        text.insert('1.0', long_para)
        for i in range(80):
            text.insert('end', f"Fortlaufende Inhaltszeile {i} für verlässliche Scroll-Tests.\n")
        self.root.update()

        class FullCornerEditorAdapter:
            def __init__(self, t):
                self.text = t
                self.CORNER_COVER_SIZE = 56
                self.IMAGE_GAP = 12
                self.app = type('App', (), {
                    'theme': {'card': '#ffffff'},
                    'add_tooltip': lambda *a: None,
                    'bind_mousewheel': lambda *a: None
                })()
                self._corner_cover = None
                self._image_views = {}
                self.images = {}
                self._image_drag = None
                self.entry_id = 'page1'
            flow_around = app_mod.PageEditor.flow_around
            ypixels = app_mod.PageEditor.ypixels
            column_bounds = app_mod.PageEditor.column_bounds
            line_top = app_mod.PageEditor.line_top
            place_origin = app_mod.PageEditor.place_origin
            place_at = app_mod.PageEditor.place_at
            layout_corner_cover = app_mod.PageEditor.layout_corner_cover
            place_corner_cover = app_mod.PageEditor.place_corner_cover
            clear_corner_cover = app_mod.PageEditor.clear_corner_cover
            show_corner_cover = app_mod.PageEditor.show_corner_cover

        editor = FullCornerEditorAdapter(text)

        # 1. Erzeugung & exakte Anfangsplatzierung
        doc1 = glide_drawing.DrawingModel().to_document()
        editor.show_corner_cover({'kind': 'drawing', 'document': doc1})
        self.root.update()

        lbl1 = editor._corner_cover
        self.assertIsNotNone(lbl1)
        self.assertTrue(lbl1.winfo_exists())
        self.assertEqual(lbl1.winfo_manager(), "place")
        
        # Koordinatenprüfung gegen die Produktionsberechnung in place_corner_cover
        links, spalte = editor.column_bounds()
        req_w = lbl1.winfo_reqwidth()
        exp_x = links + spalte - req_w
        exp_y = editor.line_top('1.0') + 4
        self.assertEqual(int(lbl1.place_info()['x']), exp_x)
        self.assertEqual(int(lbl1.place_info()['y']), exp_y)
        self.assertEqual(text.tag_cget('cornerflow', 'wrap'), 'word')
        self.assertTrue(bool(text.tag_ranges('cornerflow')))

        # 2. Scrollen im Text: Partielle Verschiebung und vollständiges Ausblenden (keine Geister-Overlays)
        # 2a. Leichtes Scrollen: Y-Koordinate passt sich an
        text.yview_scroll(2, 'units')
        self.root.update()
        editor.place_corner_cover()
        self.root.update()
        new_y = editor.line_top('1.0') + 4
        if new_y + lbl1.winfo_reqheight() >= 0 and new_y <= text.winfo_height() and lbl1.place_info():
            self.assertEqual(int(lbl1.place_info()['y']), new_y)

        # 2b. Weites Scrollen: Zeile 1 weit außerhalb des Sichtbereichs -> place_forget() muss greifen!
        text.yview_moveto(0.6)
        self.root.update()
        editor.place_corner_cover()
        self.root.update()
        self.assertFalse(bool(lbl1.place_info()), "Aus dem Sichtbereich gescrolltes Ecksymbol muss mit place_forget entkoppelt werden")

        # 2c. Zurück an den Anfang scrollen -> Symbol wird wieder exakt platziert
        text.yview_moveto(0.0)
        self.root.update()
        editor.place_corner_cover()
        self.root.update()
        self.assertTrue(bool(lbl1.place_info()))
        self.assertEqual(int(lbl1.place_info()['x']), exp_x)
        self.assertEqual(int(lbl1.place_info()['y']), exp_y)

        # 3. Layoutaktualisierung bei Fenstergrößenänderung
        self.root.geometry("850x550")
        self.root.update()
        editor.layout_corner_cover()
        self.root.update()
        new_links, new_spalte = editor.column_bounds()
        self.assertEqual(int(lbl1.place_info()['x']), new_links + new_spalte - req_w)
        self.assertTrue(bool(text.tag_ranges('cornerflow')))

        # 4. Ersetzen durch ein anderes Cover (Atomarität)
        doc2 = glide_drawing.DrawingModel().to_document()
        editor.show_corner_cover({'kind': 'drawing', 'document': doc2})
        self.root.update()
        lbl2 = editor._corner_cover
        self.assertIsNotNone(lbl2)
        self.assertTrue(lbl2.winfo_exists())

        # 5. Vollständige Bereinigung via clear_corner_cover (keine Reste, keine Geistertags)
        editor.clear_corner_cover()
        self.root.update()
        self.assertIsNone(editor._corner_cover)
        self.assertFalse(lbl2.winfo_exists())
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
