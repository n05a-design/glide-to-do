# SPDX-License-Identifier: MPL-2.0
"""Dauerhafte Integrations- und UI-Vertragstests für D78-Custom-Controls.

Prüft Schnittstellenkompatibilität (keys, cget, configure, getitem, setitem, Aliase,
Tk-Variablen, Deaktivierung und Ereignisbehandlung) der D78-Custom-Controls
(CanvasLabel, GlideCheckbutton, GlideRadiobutton, GlideListbox, GlideScale).
"""
import argparse
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
parser.add_argument("--report", type=Path)
args, _ = parser.parse_known_args()

_temp_dir = tempfile.TemporaryDirectory(prefix="glide-custom-controls-")
os.environ["GLIDE_DATA_DIR"] = _temp_dir.name
os.environ["GLIDE_TEST_MODE"] = "1"
sys.path.insert(0, str(args.app.parent))
loader = importlib.machinery.SourceFileLoader("glide_app_controls", str(args.app.resolve()))
gapp = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
sys.modules[loader.name] = gapp
loader.exec_module(gapp)


def tearDownModule():
    try:
        _temp_dir.cleanup()
    except Exception:
        pass


import tkinter as tk  # noqa: E402


class TestCustomControlsUnit(unittest.TestCase):
    """Schnittstellen- und Optionsprüfungen der D78-Custom-Controls."""

    def test_temp_data_dir_persists_during_suite_execution(self):
        """Prüft, dass das temporäre Testdatenverzeichnis während der gesamten Suiten-Ausführung verfügbar bleibt."""
        data_dir = Path(os.environ["GLIDE_DATA_DIR"])
        self.assertTrue(data_dir.exists(), f"GLIDE_DATA_DIR {data_dir} muss während der Testausführung existieren")
        self.assertTrue(data_dir.is_dir(), f"GLIDE_DATA_DIR {data_dir} muss ein Verzeichnis sein")

    def test_keys_cget_and_item_access_consistency(self):
        root = tk.Tk()
        root.withdraw()
        try:
            cl = gapp.CanvasLabel(root, text="LabelText", fg="#123456", bg="#abcdef")
            for k in cl.keys():
                self.assertEqual(cl.cget(k), cl[k], f"CanvasLabel mismatch for {k}")

            cb = gapp.GlideCheckbutton(root, text="CheckText", onvalue=10, offvalue=5)
            for k in cb.keys():
                self.assertEqual(cb.cget(k), cb[k], f"GlideCheckbutton mismatch for {k}")
            self.assertEqual(cb.cget("onvalue"), 10)
            self.assertEqual(cb.cget("offvalue"), 5)

            rb = gapp.GlideRadiobutton(root, text="RadioText", value="opt1")
            for k in rb.keys():
                self.assertEqual(rb.cget(k), rb[k], f"GlideRadiobutton mismatch for {k}")
            self.assertEqual(rb.cget("value"), "opt1")

            lb = gapp.GlideListbox(root, selectmode="extended")
            for k in lb.keys():
                self.assertEqual(lb.cget(k), lb[k], f"GlideListbox mismatch for {k}")
            self.assertEqual(lb.cget("selectmode"), "extended")

            sc = gapp.GlideScale(root, from_=5, to=50, resolution=2.5, orient="horizontal")
            for k in sc.keys():
                self.assertEqual(sc.cget(k), sc[k], f"GlideScale mismatch for {k}")
            self.assertEqual(sc.cget("from"), 5.0)
            self.assertEqual(sc.cget("from_"), 5.0)
            self.assertEqual(sc.cget("to"), 50.0)
            self.assertEqual(sc.cget("resolution"), 2.5)
            self.assertEqual(sc.cget("orient"), "horizontal")
        finally:
            root.destroy()

    def test_option_aliases_consistency(self):
        root = tk.Tk()
        root.withdraw()
        try:
            cl = gapp.CanvasLabel(root, text="T", background="#111111", foreground="#eeeeee")
            self.assertEqual(cl.cget("bg"), "#111111")
            self.assertEqual(cl.cget("background"), "#111111")
            self.assertEqual(cl.cget("fg"), "#eeeeee")
            self.assertEqual(cl.cget("foreground"), "#eeeeee")

            cb = gapp.GlideCheckbutton(root, text="T", background="#222222", foreground="#dddddd")
            self.assertEqual(cb.cget("bg"), "#222222")
            self.assertEqual(cb.cget("background"), "#222222")
            self.assertEqual(cb.cget("fg"), "#dddddd")
            self.assertEqual(cb.cget("foreground"), "#dddddd")

            sc = gapp.GlideScale(root, from_=10, to=100)
            self.assertEqual(sc.cget("from"), 10.0)
            self.assertEqual(sc.cget("from_"), 10.0)
            self.assertEqual(sc["from"], 10.0)
            self.assertEqual(sc["from_"], 10.0)
        finally:
            root.destroy()

    def test_configure_and_state_transitions(self):
        root = tk.Tk()
        root.withdraw()
        try:
            cb = gapp.GlideCheckbutton(root, text="Start", onvalue="JA", offvalue="NEIN")
            cb.configure(text="Geändert", onvalue=1, offvalue=0, state="disabled")
            self.assertEqual(cb.cget("text"), "Geändert")
            self.assertEqual(cb["text"], "Geändert")
            self.assertEqual(cb.cget("onvalue"), 1)
            self.assertEqual(cb.cget("offvalue"), 0)
            self.assertEqual(cb.cget("state"), "disabled")

            sc = gapp.GlideScale(root, from_=0, to=10)
            sc.configure(from_=2, to=20, resolution=0.5, orient="vertical")
            self.assertEqual(sc.cget("from"), 2.0)
            self.assertEqual(sc.cget("to"), 20.0)
            self.assertEqual(sc.cget("resolution"), 0.5)
            self.assertEqual(sc.cget("orient"), "vertical")
        finally:
            root.destroy()


class TestCustomControlsInteractions(unittest.TestCase):
    """Interaktionstests mit Ereignisverarbeitung und Tk-Variablen."""

    def test_checkbutton_and_radiobutton_variable_sync_and_invoke(self):
        root = tk.Tk()
        root.withdraw()
        try:
            var_b = tk.BooleanVar(value=False)
            cmds = []
            cb = gapp.GlideCheckbutton(root, text="Check", variable=var_b, command=lambda: cmds.append("cb"))
            self.assertFalse(cb._is_checked())
            cb.invoke()
            self.assertTrue(var_b.get())
            self.assertTrue(cb._is_checked())
            self.assertEqual(cmds, ["cb"])
            cb.invoke()
            self.assertFalse(var_b.get())
            self.assertFalse(cb._is_checked())
            self.assertEqual(cmds, ["cb", "cb"])

            var_s = tk.StringVar(value="none")
            rb1 = gapp.GlideRadiobutton(root, text="R1", value="opt1", variable=var_s)
            rb2 = gapp.GlideRadiobutton(root, text="R2", value="opt2", variable=var_s)
            self.assertFalse(rb1._is_checked())
            self.assertFalse(rb2._is_checked())
            rb1.invoke()
            self.assertEqual(var_s.get(), "opt1")
            self.assertTrue(rb1._is_checked())
            self.assertFalse(rb2._is_checked())
            rb2.invoke()
            self.assertEqual(var_s.get(), "opt2")
            self.assertFalse(rb1._is_checked())
            self.assertTrue(rb2._is_checked())
        finally:
            root.destroy()

    def test_disabled_controls_prevent_actions(self):
        root = tk.Tk()
        root.withdraw()
        try:
            cmds = []
            cb = gapp.GlideCheckbutton(root, text="Disabled", state="disabled", command=lambda: cmds.append("fired"))
            res_click = cb._on_click(None)
            self.assertEqual(res_click, "break")
            cb.invoke()
            self.assertEqual(cmds, [])

            lb = gapp.GlideListbox(root, state="disabled")
            lb.insert(0, "A", "B")
            self.assertEqual(lb._on_click(None), "break")

            sc = gapp.GlideScale(root, from_=0, to=10, state="disabled", command=lambda val: cmds.append(val))
            self.assertEqual(sc._step(1), "break")
            self.assertEqual(sc._on_pointer(None), "break")
            self.assertEqual(cmds, [])
        finally:
            root.destroy()

    def test_scale_variable_sync_and_clamping(self):
        root = tk.Tk()
        root.withdraw()
        try:
            var = tk.DoubleVar(value=20.0)
            sc = gapp.GlideScale(root, from_=0, to=100, resolution=5.0, variable=var)
            self.assertEqual(sc.get(), 20.0)
            sc.set(37.0)
            self.assertEqual(sc.get(), 35.0)  # clamped by resolution 5.0
            self.assertEqual(var.get(), 35.0)

            var.set(80.0)
            sc._sync_from_var()
            self.assertEqual(sc.get(), 80.0)
        finally:
            root.destroy()

    def test_listbox_operations_and_bounds(self):
        root = tk.Tk()
        root.withdraw()
        try:
            lb = gapp.GlideListbox(root)
            self.assertEqual(lb.size(), 0)
            lb.insert("end", "Erstes", "Zweites", "Drittes")
            self.assertEqual(lb.size(), 3)
            self.assertEqual(lb.get(0), "Erstes")
            self.assertEqual(lb.get(2), "Drittes")
            lb.selection_set(1)
            self.assertEqual(lb.curselection(), (1,))
            lb.delete(1)
            self.assertEqual(lb.size(), 2)
            self.assertEqual(lb.get(1), "Drittes")
        finally:
            root.destroy()

    def test_widget_destruction_and_callback_cleanup(self):
        root = tk.Tk()
        root.withdraw()
        try:
            var = tk.DoubleVar(value=10.0)
            sc = gapp.GlideScale(root, from_=0, to=100, variable=var)
            self.assertIsNotNone(sc._trace_id)
            sc.destroy()
            self.assertIsNone(sc._variable)
        finally:
            root.destroy()

    def test_configure_event_recursion_and_render_guard(self):
        """Prüft, dass wiederholte oder kaskadierende <Configure>-Ereignisse keine Endlosschleife auslösen."""
        root = tk.Tk()
        root.withdraw()
        try:
            cb = gapp.GlideCheckbutton(root, text="Recursion Guard Test")
            cb.pack()
            root.update_idletasks()

            # Mehrfache identische Configure-Aufrufe dürfen nicht mehrfach rendern
            renders = [0]
            orig_render = cb._render
            def counted_render():
                renders[0] += 1
                return orig_render()
            cb._render = counted_render

            class DummyEvent:
                width = 150
                height = 24

            event = DummyEvent()
            # Erstes Ereignis setzt die Dimensionen
            cb._on_configure(event)
            self.assertEqual(renders[0], 1)

            # Zweites identisches Ereignis muss ignoriert werden
            renders[0] = 0
            cb._on_configure(event)
            self.assertEqual(renders[0], 0, "Identisches <Configure>-Ereignis darf kein Re-Render auslösen")

            # Re-entrancy guard prüfen
            cb._rendering = True
            cb._safe_render()
            self.assertEqual(renders[0], 0, "_safe_render darf während laufendem Rendern nicht reentrant aufgerufen werden")
            cb._rendering = False
        finally:
            root.destroy()

    def test_buttonflow_configure_and_reflow_guard(self):
        """Prüft Breiten-Filterung, Breiten-Deduplizierung und Re-Entrancy-Guard von ButtonFlow."""
        root = tk.Tk()
        try:
            flow = gapp.ButtonFlow(root, bg="#ffffff", gap=8)

            class DummyEvent:
                def __init__(self, width, height=20, widget=None):
                    self.width = width
                    self.height = height
                    self.widget = widget or flow

            reflows = [0]
            orig_schedule = flow.schedule_reflow

            def counted_schedule():
                reflows[0] += 1
                return orig_schedule()

            flow.schedule_reflow = counted_schedule

            # 0. Ereignisse für fremde/untergeordnete Widgets dürfen kein schedule_reflow auslösen
            other_widget = tk.Frame(root)
            flow._on_configure(DummyEvent(width=300, height=40, widget=other_widget))
            self.assertEqual(reflows[0], 0, "ButtonFlow darf bei Ereignissen fremder Widgets kein Reflow planen")

            # 1. Breiten <= 1 (ungemappter Zustand) dürfen kein schedule_reflow auslösen
            flow._on_configure(DummyEvent(width=1, height=1))
            self.assertEqual(reflows[0], 0, "ButtonFlow darf bei Breite <= 1 kein Reflow planen")

            # 2. Reale Breite löst schedule_reflow aus
            flow._on_configure(DummyEvent(width=300, height=40))
            self.assertEqual(reflows[0], 1, "ButtonFlow muss bei neuer Breite schedule_reflow aufrufen")

            # 3. Reine Höhenänderung (Breite bleibt 300) darf KEIN weiteres Reflow auslösen
            reflows[0] = 0
            flow._on_configure(DummyEvent(width=300, height=80))
            self.assertEqual(reflows[0], 0, "ButtonFlow darf bei reiner Höhenänderung kein Reflow planen")

            # 4. Re-Entrancy Guard
            flow._reflowing = True
            called = [False]

            def dummy_cancel():
                called[0] = True

            flow.cancel_reflow = dummy_cancel
            flow.reflow()
            self.assertFalse(called[0], "reflow() darf während aktivem _reflowing nicht ausgeführt werden")
            flow._reflowing = False

            # 5. In zurückgezogenem Dialog (withdraw) darf update_idletasks() nicht livelocken
            dlg = tk.Toplevel(root)
            dlg.withdraw()
            dlg_flow = gapp.ButtonFlow(dlg, bg="#ffffff", gap=8)
            dlg_flow.pack(fill="x")
            btn1 = tk.Button(dlg_flow, text="Knopf 1")
            btn2 = tk.Button(dlg_flow, text="Knopf 2")
            dlg_flow.add(btn1)
            dlg_flow.add(btn2)
            dlg.update_idletasks()
            self.assertEqual(len(dlg_flow._rows), 1, "Im ungemappten Dialog müssen alle Knöpfe in Zeile 0 liegen")
            dlg.destroy()
        finally:
            root.destroy()

    def test_buttonflow_reflow_ends_nonconsecutive_width_cycle(self):
        root = tk.Tk()
        root.withdraw()
        try:
            widths = [320]
            window_width = [800]
            reflows = []
            root.winfo_width = lambda: window_width[0]
            flow = gapp.ButtonFlow(root, bg="#ffffff", gap=8, on_layout=lambda: reflows.append(True))
            flow.winfo_width = lambda: widths[0]

            for width in (320, 400, 320, 400):
                widths[0] = width
                flow.reflow()

            self.assertEqual(len(reflows), 3, "Eine wiederkehrende Breite muss die Reflow-Schaukel beenden")
            self.assertEqual(flow._layout_signature[0], 320, "Die stabilisierte Leiste muss die engste Breite verwenden")

            window_width[0] = 900
            widths[0] = 400
            flow.reflow()
            self.assertEqual(flow._layout_signature[0], 400, "Eine echte Fensterbreitenänderung muss neu messen")
        finally:
            root.destroy()

    def test_multi_host_provider_isolation(self):
        """Prüft, dass Schriften, Hintergründe und Tintenberechnung hierarchisch aufgelöst werden."""
        from glide_shell import custom_controls

        root = tk.Tk()
        root.withdraw()
        top1 = tk.Toplevel(root)
        top1.withdraw()
        top2 = tk.Toplevel(root)
        top2.withdraw()
        try:
            # 1. Globaler Fallback
            custom_controls.set_font_provider(lambda size, *s: ("Courier", size))
            custom_controls.set_backdrop_painter(lambda c: c.create_line(0, 0, 10, 10, tags=("global_bg",)))
            self.assertEqual(custom_controls._default_font(12), ("Courier", 12))

            # 2. Toplevel-spezifischer Override (top1)
            top1._font_provider = lambda size, *s: ("Times", size)
            top1._backdrop_painter = lambda c: c.create_line(0, 0, 20, 20, tags=("top1_bg",))
            lbl1 = custom_controls.CanvasLabel(top1, text="Test 1")
            self.assertEqual(custom_controls._default_font(14, widget=lbl1), ("Times", 14))

            # Canvas in top1 erhält top1-Painter
            cv1 = tk.Canvas(top1, width=50, height=50)
            custom_controls.paint_canvas_backdrop(cv1)
            self.assertTrue(bool(cv1.find_withtag("top1_bg")))
            self.assertFalse(bool(cv1.find_withtag("global_bg")))

            # 3. top2 ohne Override fällt auf global zurück (Multi-Host Isolation)
            lbl2 = custom_controls.CanvasLabel(top2, text="Test 2")
            self.assertEqual(custom_controls._default_font(14, widget=lbl2), ("Courier", 14))

            cv2 = tk.Canvas(top2, width=50, height=50)
            custom_controls.paint_canvas_backdrop(cv2)
            self.assertTrue(bool(cv2.find_withtag("global_bg")))
            self.assertFalse(bool(cv2.find_withtag("top1_bg")))

            # 4. Widget-spezifischer Override überstimmt Toplevel
            lbl1._font_provider = lambda size, *s: ("Helvetica", size)
            self.assertEqual(custom_controls._default_font(16, widget=lbl1), ("Helvetica", 16))
        finally:
            custom_controls.set_font_provider(None)
            custom_controls.set_backdrop_painter(None)
            top1.destroy()
            top2.destroy()
            root.destroy()

    def test_design_vertrag_und_provider_in_hell_dunkel(self):
        """Prüft den transportablen Designvertrag: Provider (_ink_provider, _font_provider, _backdrop_painter), Kontrast, B15, B11 und Tastaturnavigation."""
        from glide_shell import custom_controls, system_appearance, text_fit

        root = tk.Tk()
        root.withdraw()
        top_light = tk.Toplevel(root)
        top_light.withdraw()
        top_dark = tk.Toplevel(root)
        top_dark.withdraw()
        try:
            # 1. Theme- und Farbrollenauflösung (Hell / Dunkel)
            theme_def = {
                "light": {"bg": "#ffffff", "fg": "#111111", "card": "#f5f5f5"},
                "dark": {"bg": "#1e1e1e", "fg": "#f0f0f0", "card": "#2d2d2d"},
            }
            pal_light = system_appearance.resolve(theme_def, False, theme_def["light"])
            pal_dark = system_appearance.resolve(theme_def, True, theme_def["light"])
            self.assertEqual(pal_light["bg"], "#ffffff")
            self.assertEqual(pal_dark["bg"], "#1e1e1e")

            # 2. Kontrastprüfung (WCAG AA 4,5:1 für Standardtext)
            def luminance(hex_col):
                hex_col = hex_col.lstrip("#")
                r, g, b = [int(hex_col[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
                def chan(c):
                    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
                return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)

            def contrast_ratio(c1, c2):
                l1, l2 = luminance(c1), luminance(c2)
                return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)

            ratio_light = contrast_ratio(pal_light["fg"], pal_light["bg"])
            ratio_dark = contrast_ratio(pal_dark["fg"], pal_dark["bg"])
            self.assertGreaterEqual(ratio_light, 4.5, f"Kontrast im Hellmodus unter 4.5:1 ({ratio_light:.2f})")
            self.assertGreaterEqual(ratio_dark, 4.5, f"Kontrast im Dunkelmodus unter 4.5:1 ({ratio_dark:.2f})")

            # 3. Provider-Nutzung: _ink_provider, _font_provider und _backdrop_painter
            top_light._font_provider = lambda size, *s: ("Helvetica", size)
            top_light._ink_provider = lambda char, size: (size * 0.6, size * 0.8)
            top_light._backdrop_painter = lambda c: c.create_rectangle(0, 0, 50, 50, fill=pal_light["card"], tags=("bg_light",))

            top_dark._font_provider = lambda size, *s: ("Helvetica", size)
            top_dark._ink_provider = lambda char, size: (size * 0.65, size * 0.85)
            top_dark._backdrop_painter = lambda c: c.create_rectangle(0, 0, 50, 50, fill=pal_dark["card"], tags=("bg_dark",))

            # Canvas in top_light / top_dark
            cv_light = tk.Canvas(top_light, width=60, height=60)
            custom_controls.paint_canvas_backdrop(cv_light)
            self.assertTrue(bool(cv_light.find_withtag("bg_light")))

            cv_dark = tk.Canvas(top_dark, width=60, height=60)
            custom_controls.paint_canvas_backdrop(cv_dark)
            self.assertTrue(bool(cv_dark.find_withtag("bg_dark")))

            # 4. B11 Text Fit (Priorität vor Metadaten, kein Abschneiden ohne Ellipsis)
            titel = "Ein extrem langer Titel einer anstehenden Aufgabe im System"
            gekuerzt = text_fit.clip(titel, 25, ellipsis="…")
            self.assertLessEqual(len(gekuerzt), 25)
            self.assertTrue(gekuerzt.endswith("…"))

            # 5. Tastaturnavigation und Interaktion (Tab / Space / Return)
            var_b = tk.BooleanVar(value=False)
            check = custom_controls.GlideCheckbutton(top_light, text="Option", variable=var_b, bg=pal_light["bg"], fg=pal_light["fg"])
            check.pack()
            top_light.update()
            self.assertFalse(check._is_checked())
            check.invoke()
            self.assertTrue(var_b.get())
            self.assertTrue(check._is_checked())
        finally:
            top_light.destroy()
            top_dark.destroy()
            root.destroy()


def main():
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
