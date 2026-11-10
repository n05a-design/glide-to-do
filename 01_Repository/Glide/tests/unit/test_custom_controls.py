# SPDX-License-Identifier: MPL-2.0
"""Dauerhafte Regressionstests für D78-Custom-Controls (CanvasLabel, GlideCheckbutton, GlideRadiobutton, GlideListbox, GlideScale)."""
from pathlib import Path
import sys
import unittest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "src/glide"))

import tkinter as tk
import glide.app as gapp


class TestCustomControlsUnit(unittest.TestCase):
    """Reine Unit-Tests ohne offene Fensterinteraktion."""

    def test_keys_cget_and_item_access_consistency(self):
        root = tk.Tk()
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
        try:
            var = tk.DoubleVar(value=10.0)
            sc = gapp.GlideScale(root, from_=0, to=100, variable=var)
            self.assertIsNotNone(sc._trace_id)
            sc.destroy()
            self.assertIsNone(sc._variable)
        finally:
            root.destroy()


if __name__ == "__main__":
    unittest.main()
