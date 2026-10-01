"""Prüfläufe im Hintergrund (macOS): Tk-Fenster nehmen weder Fokus noch Tastatur.

Seit 30.09.2026. `tests/tools/pruefen.py` legt diesen Ordner unter macOS in
den PYTHONPATH und setzt GLIDE_QA_HINTERGRUND=1; Python lädt die Datei dann
beim Start jeder Suite. Glide selbst bleibt unverändert.

Ablauf je Tk-Hauptfenster:

- Tk starten; Tk holt sich dabei den Vordergrund.
- Das Programm als „Zubehör“ kennzeichnen (NSApplicationActivationPolicy
  Accessory: kein Dock-Symbol, keine Menüleiste).
- Mit `deactivate` den Vordergrund an das vorherige Programm zurückgeben.

`focus_force` wird zu `focus_set`: Tk behält seinen inneren Fokus, holt die App
aber nicht mehr nach vorn. Fenster werden weiter gezeichnet und lassen sich
fotografieren; sie können über anderen Fenstern erscheinen, nehmen aber weder
Tastatur noch Maus. `pruefen.py --vordergrund` schaltet das ab.
"""
import os
import sys

if sys.platform == "darwin" and os.environ.get("GLIDE_QA_HINTERGRUND"):
    import ctypes
    import ctypes.util
    import tkinter

    _objc = ctypes.cdll.LoadLibrary(ctypes.util.find_library("objc"))
    _objc.objc_getClass.restype = ctypes.c_void_p
    _objc.objc_getClass.argtypes = [ctypes.c_char_p]
    _objc.sel_registerName.restype = ctypes.c_void_p
    _objc.sel_registerName.argtypes = [ctypes.c_char_p]
    _id = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(("objc_msgSend", _objc))
    _mit_zahl = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong)(("objc_msgSend", _objc))
    _ohne = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)(("objc_msgSend", _objc))

    def _sel(name):
        return _objc.sel_registerName(name)

    _count = ctypes.CFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p, ctypes.c_void_p)(("objc_msgSend", _objc))
    _index = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong)(("objc_msgSend", _objc))
    _set_bool = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_bool)(("objc_msgSend", _objc))

    def _maus_ignorieren():
        app = _id(_objc.objc_getClass(b"NSApplication"), _sel(b"sharedApplication"))
        windows = _id(app, _sel(b"windows"))
        for index in range(_count(windows, _sel(b"count"))):
            window = _index(windows, _sel(b"objectAtIndex:"), index)
            _set_bool(window, _sel(b"setIgnoresMouseEvents:"), True)

    _alt_init = tkinter.Tk.__init__

    def _neu_init(self, *args, **kwargs):
        _alt_init(self, *args, **kwargs)
        try:
            app = _id(_objc.objc_getClass(b"NSApplication"), _sel(b"sharedApplication"))
            _mit_zahl(app, _sel(b"setActivationPolicy:"), 1)  # Zubehör: kein Dock, kein Menü
            _ohne(app, _sel(b"deactivate"))
        except Exception:
            pass
        # Auch später gemappte Dialoge und Tooltips gehören nur diesem Prozess.
        pending = [None]

        def apply():
            pending[0] = None
            _maus_ignorieren()

        def mapped(_event):
            if pending[0] is None:
                pending[0] = self.after_idle(apply)

        def destroyed(event):
            if event.widget is self and pending[0] is not None:
                self.after_cancel(pending[0])
                pending[0] = None

        self.bind_all("<Map>", mapped, add="+")
        self.bind("<Destroy>", destroyed, add="+")
        _maus_ignorieren()

    tkinter.Tk.__init__ = _neu_init
    tkinter.Misc.focus_force = tkinter.Misc.focus_set
