# SPDX-License-Identifier: MPL-2.0
"""Shell-Phasen 4 und 5 (D99): `command_history` und `app_host` ohne Glide-Werte, dazu Glides Einbindung.

Phase 4: Befehlsverlauf mit Befehlsobjekten und Zustandsabbildern, Rückweg
bei gescheitertem Herstellen, Kürzen nur mit Erlaubnis des Hosts, Sonder-
schritte beim Wiederholen. Phase 5: App-Host mit Schritten vor Tk,
Startprüfungen, Platzhalter, Controller, Kürzeltabelle nach Plattform,
Menüleiste und Schließweg; ohne echtes Tk über Attrappen. Glide-Seite:
`ListApp.command_history` nutzt den Wiederholen-Stapel des Hosts, die
Kürzeltabelle bindet Cmd nur unter macOS.
"""

import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import tkinter as tk
import unittest

SRC = Path(__file__).resolve().parents[2] / "src/glide"
sys.path.insert(0, str(SRC))

from glide_shell import app_host, command_history, custom_controls, redo_history  # noqa: E402


class Zaehler(command_history.Command):
    def __init__(self, box, fehler=False):
        self.box, self.fehler = box, fehler

    def execute(self):
        self.box.append("x")

    def undo(self):
        if self.fehler:
            raise RuntimeError("probe")
        self.box.pop()


class Befehlsverlauf(unittest.TestCase):
    def test_befehle_rueckgaengig_und_wiederholen(self):
        box, verlauf = [], command_history.CommandHistory(limit=3)
        for _ in range(4):
            verlauf.execute(Zaehler(box))
        self.assertEqual((len(box), len(verlauf)), (4, 3), "Höchstzahl kürzt den ältesten Schritt")
        self.assertEqual(verlauf.undo(), command_history.DONE)
        self.assertTrue(verlauf.can_redo())
        self.assertEqual(verlauf.redo_step(), command_history.DONE)
        self.assertEqual(len(box), 4)
        verlauf.undo()
        verlauf.execute(Zaehler(box))
        self.assertFalse(verlauf.can_redo(), "neuer Schritt verwirft Wiederholen")
        self.assertEqual(command_history.CommandHistory().undo(), command_history.EMPTY)
        self.assertEqual(command_history.CommandHistory().redo_step(), command_history.EMPTY)

    def test_befehl_mit_fehler_bleibt_auf_dem_stapel(self):
        verlauf = command_history.CommandHistory()
        verlauf.execute(Zaehler([], fehler=True))
        with self.assertRaises(RuntimeError):
            verlauf.undo()
        self.assertEqual(len(verlauf), 1)

    def test_zustandsabbild_mit_rueckweg(self):
        stand, rueckweg = {"v": 1}, []
        gelingt = [True]

        def herstellen(abbild):
            if not gelingt[0]:
                return False
            stand.clear()
            stand.update(abbild)
            return True

        verlauf = command_history.CommandHistory(lambda: dict(stand), herstellen, rueckweg.append)
        verlauf.record()
        stand["v"] = 2
        gelingt[0] = False
        self.assertEqual(verlauf.undo(), command_history.FAILED)
        self.assertEqual((stand["v"], len(verlauf), rueckweg), (2, 1, [{"v": 2}]),
                         "Schritt bleibt, Rückweg erhält den Stand davor")
        self.assertFalse(verlauf.can_redo())
        gelingt[0] = True
        self.assertEqual(verlauf.undo(), command_history.DONE)
        self.assertEqual(stand["v"], 1)
        gelingt[0] = False
        self.assertEqual(verlauf.redo_step(), command_history.FAILED)
        self.assertTrue(verlauf.can_redo(), "gescheitertes Wiederholen legt den Schritt zurück")
        self.assertEqual(len(verlauf), 0)

    def test_hoststapel_kuerzen_vorbereiten_und_sonderschritt(self):
        eigener, halten = [], [True]
        redo = redo_history.RedoHistory(2)
        verlauf = command_history.CommandHistory(
            lambda: {"v": 0}, lambda abbild: True, stack=lambda: eigener, redo=lambda: redo, limit=2,
            can_trim=lambda: not halten[0], prepare=lambda e: dict(e, vorbereitet=True),
            link=lambda e, aktuell: aktuell.update(marke=e.get("marke")))
        for n in range(3):
            verlauf.record({"v": n, "marke": n}, trim=True)
        self.assertEqual(len(eigener), 3, "der Host hält den Stapel fest")
        halten[0] = False
        self.assertTrue(verlauf.trim())
        self.assertEqual([e["v"] for e in eigener], [1, 2])
        self.assertIs(verlauf.redo, redo)
        verlauf.undo()
        self.assertEqual(redo.peek()["marke"], 2, "link überträgt Angaben auf den erfassten Stand")
        gesehen = []
        self.assertEqual(verlauf.redo_step(handle=lambda e: gesehen.append(e) or True), command_history.HANDLED)
        self.assertEqual(len(gesehen), 1)
        with self.assertRaises(ValueError):
            command_history.CommandHistory().record()
        verlauf.clear()
        self.assertEqual((len(eigener), len(redo)), (0, 0))


class Wurzel:
    """Attrappe eines Hauptfensters für den App-Host."""

    def __init__(self, menue_abgelehnt=False):
        self.log, self.bindungen, self.menue_abgelehnt = [], {}, menue_abgelehnt

    def withdraw(self):
        self.log.append("withdraw")

    def destroy(self):
        self.log.append("destroy")

    def mainloop(self):
        self.log.append("mainloop")

    def bind(self, sequenz, handler):
        self.bindungen[sequenz] = handler

    def config(self, menu=None):
        if self.menue_abgelehnt:
            raise tk.TclError("probe")
        self.log.append(("menu", menu))

    def protocol(self, name, handler):
        self.log.append(("protocol", name, handler))

    def createcommand(self, name, handler):
        self.log.append(("command", name))
        self.quit = handler


class Bereich:
    def __init__(self):
        self.idle = []

    def after_idle(self, callback):
        self.idle.append(callback)


class AppHost(unittest.TestCase):
    def test_ablauf_und_startpruefung(self):
        reihenfolge, wurzel = [], Wurzel()

        class Platzhalter:
            def destroy(self):
                reihenfolge.append("platzhalter weg")

        host = app_host.AppHost(before_tk=(lambda: reihenfolge.append("vor tk"),),
                                preflight=(lambda w: reihenfolge.append("prüfung") or None,),
                                splash=lambda w: reihenfolge.append("platzhalter") or Platzhalter(),
                                on_ready=lambda w: reihenfolge.append("bereit"), tk_factory=lambda: wurzel)
        controller = host.run(lambda w: reihenfolge.append("controller") or "c")
        self.assertEqual(controller, "c")
        self.assertEqual(reihenfolge, ["vor tk", "prüfung", "platzhalter", "controller", "platzhalter weg", "bereit"])
        self.assertEqual(wurzel.log, ["mainloop"])
        gezeigt, wurzel = [], Wurzel()
        host = app_host.AppHost(preflight=(lambda w: None, lambda w: ("T", "M")),
                                show_error=lambda *a, **k: gezeigt.append((a, k)), tk_factory=lambda: wurzel)
        with self.assertRaises(SystemExit) as ende:
            host.run(lambda w: self.fail("Controller darf nicht entstehen"))
        self.assertEqual(ende.exception.code, 1)
        self.assertEqual(gezeigt, [(("T", "M"), {"parent": wurzel})])
        self.assertEqual(wurzel.log, ["withdraw", "destroy"])

    def test_kuerzel_menue_und_schliessweg(self):
        self.assertEqual([app_host.platform_of(n) for n in ("aqua", "win32", "x11")],
                         [app_host.MACOS, app_host.WINDOWS, app_host.LINUX])
        handler = object()
        mac = app_host.primary_shortcuts("z", handler, app_host.MACOS, shift=True)
        self.assertEqual([s for s, _h, _p in mac], ["<Control-Shift-z>", "<Command-Shift-z>"])
        tabelle = mac + [("<Control-y>", handler, app_host.WINDOWS)]
        wurzel = Wurzel()
        self.assertEqual(app_host.bind_shortcuts(wurzel, tabelle, app_host.LINUX), ["<Control-Shift-z>"])
        self.assertEqual(app_host.bind_shortcuts(Wurzel(), tabelle, app_host.WINDOWS), ["<Control-Shift-z>", "<Control-y>"])
        self.assertTrue(app_host.attach_menubar(wurzel, "leiste"))
        self.assertFalse(app_host.attach_menubar(Wurzel(menue_abgelehnt=True), "leiste"))
        schliessen, bereich = object(), Bereich()
        self.assertFalse(app_host.install_close(wurzel, schliessen, app_host.LINUX))
        self.assertIn(("protocol", "WM_DELETE_WINDOW", schliessen), wurzel.log)
        mac_wurzel = Wurzel()
        self.assertTrue(app_host.install_close(mac_wurzel, schliessen, app_host.MACOS, scope=bereich))
        mac_wurzel.quit()
        self.assertEqual(bereich.idle, [schliessen], "Cmd+Q läuft im Leerlauf über den Bereich")

        class Unterfenster:
            """Wie ein Toplevel: Fensterknopf, aber kein createcommand."""

            def __init__(self):
                self.log = []

            def protocol(self, name, handler):
                self.log.append((name, handler))

        unter = Unterfenster()
        self.assertFalse(app_host.install_close(unter, schliessen, app_host.MACOS, scope=bereich),
                         "ein eingebettetes Fenster übernimmt nicht das Beenden der Anwendung")
        self.assertEqual(unter.log, [("WM_DELETE_WINDOW", schliessen)])


class MultiHostProviderIsolation(unittest.TestCase):
    def tearDown(self):
        custom_controls.set_font_provider(None)
        custom_controls.set_ink_provider(None)
        custom_controls.set_backdrop_painter(None)

    def test_default_font_provider_isolation_and_precedence(self):
        # 1. Fallback ohne Provider
        self.assertEqual(custom_controls._default_font(12), ("TkDefaultFont", 12))

        # 2. Globaler Provider
        custom_controls.set_font_provider(lambda s: ("GlobalFont", s))
        self.assertEqual(custom_controls._default_font(12), ("GlobalFont", 12))

        # 3. Toplevel-spezifischer Provider
        class DummyToplevel:
            def _font_provider(self, s):
                return ("ToplevelFont", s)

        class DummyWidget:
            def __init__(self, top):
                self._top = top

            def winfo_toplevel(self):
                return self._top

        top = DummyToplevel()
        w = DummyWidget(top)
        self.assertEqual(custom_controls._default_font(14, widget=w), ("ToplevelFont", 14))

        # 4. Widget-spezifischer Provider hat Vorrang vor Toplevel und Global
        w._font_provider = lambda s: ("WidgetFont", s)
        self.assertEqual(custom_controls._default_font(16, widget=w), ("WidgetFont", 16))

    def test_backdrop_painter_isolation_and_precedence(self):
        called = []

        class DummyCanvas:
            def __init__(self, top=None):
                self._top = top

            def winfo_toplevel(self):
                return self._top

        # Globaler Painter
        custom_controls.set_backdrop_painter(lambda c: called.append("global"))
        c1 = DummyCanvas()
        custom_controls.paint_canvas_backdrop(c1)
        self.assertEqual(called, ["global"])

        # Toplevel-spezifischer Painter
        called.clear()

        class DummyTop:
            def _backdrop_painter(self, c):
                called.append("toplevel")

        c2 = DummyCanvas(DummyTop())
        custom_controls.paint_canvas_backdrop(c2)
        self.assertEqual(called, ["toplevel"])

        # Canvas-spezifischer Painter hat Vorrang
        called.clear()
        c2._backdrop_painter = lambda c: called.append("canvas")
        custom_controls.paint_canvas_backdrop(c2)
        self.assertEqual(called, ["canvas"])


def lade_glide():
    os.environ["GLIDE_DATA_DIR"] = tempfile.mkdtemp(prefix="glide-phase45-")
    loader = importlib.machinery.SourceFileLoader("glide_phase45", str(SRC / "app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    modul = importlib.util.module_from_spec(spec)
    loader.exec_module(modul)
    return modul


class GlideEinbindung(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = lade_glide()

    def test_glide_nutzt_die_shell_bausteine(self):
        self.assertIs(self.mod.glide_command_history, command_history)
        self.assertIs(self.mod.glide_app_host, app_host)
        app = self.mod.ListApp.__new__(self.mod.ListApp)
        app.undo_stack, app.dirty = [], False
        verlauf = app.command_history()
        self.assertIs(verlauf.redo, app.redo_steps(), "derselbe Wiederholen-Stapel wie bisher")
        self.assertIs(verlauf.undo_stack, app.undo_stack)
        self.assertEqual(verlauf.limit, self.mod.ListApp.MAX_UNDO_STEPS)

    def test_kuerzeltabelle_nach_plattform(self):
        class Attrappe:
            def __getattr__(self, name):
                return lambda *a, **k: None

        tabelle = self.mod.ListApp.keyboard_shortcuts(Attrappe())
        sequenzen = [s for s, _h, _p in tabelle]
        self.assertEqual(len(sequenzen), len(set(sequenzen)), "jede Sequenz genau einmal")
        self.assertTrue(all(p == app_host.MACOS for s, _h, p in tabelle if s.startswith("<Command-")))
        self.assertEqual([p for s, _h, p in tabelle if s == "<Control-y>"], [app_host.WINDOWS])
        self.assertIn(self.mod.ListApp.host_platform(), (app_host.MACOS, app_host.WINDOWS, app_host.LINUX))
        host = self.mod.app_host()
        self.assertEqual(host.preflight, (self.mod.startup_tk_check, self.mod.startup_data_dir_check))


if __name__ == "__main__":
    unittest.main()
