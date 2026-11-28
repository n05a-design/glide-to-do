"""Prüfläufe im Hintergrund (macOS): Tk-Fenster holen sich nicht den Vordergrund und nehmen keine Maus.

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
fotografieren; sie können über anderen Fenstern erscheinen und nehmen keine
Maus. Die Tastatur ist nicht abgeschirmt: Die Prüf-App bleibt aktiv, und
Tastatureingaben während eines Laufs können in Prüfdialogen landen (Prüfplan,
„Hintergrund unter macOS“). Während einer Vollprüfung deshalb nicht tippen
und den Mac nicht sperren. `pruefen.py --vordergrund` schaltet das ab.
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


# --- Unbeaufsichtigte Läufe auf allen Plattformen (seit 28.11.2026, Ecosystem E03) ------------------
#
# Mit GLIDE_QA_AUTOSCHLIESSEN=<Sekunden> wartet kein Prüf- oder Messlauf auf einen Menschen:
# - Native Meldungen (`tkinter.messagebox`) und Dateidialoge (`tkinter.filedialog`) erscheinen nicht;
#   sie liefern die Standardantwort (Meldung: "ok", Frage: Nein/Abbrechen, Datei: leer) und werden
#   auf stderr protokolliert.
# - Jedes modale Warten (`wait_window`, `wait_variable`) endet spätestens nach der Frist: Das Fenster
#   wird zerstört bzw. die Variable gesetzt, ebenfalls mit Protokollzeile. Galerie, Fehlerberichte und
#   eigene Dialoge der App bleiben damit nie offen stehen.
# Glide selbst bleibt unverändert; ohne die Variable wirkt dieser Abschnitt nicht.
if os.environ.get("GLIDE_QA_AUTOSCHLIESSEN"):
    import tkinter as _tk
    from tkinter import filedialog as _fd, messagebox as _mb

    try:
        _FRIST_MS = max(1, int(float(os.environ["GLIDE_QA_AUTOSCHLIESSEN"]) * 1000))
    except ValueError:
        _FRIST_MS = 30000

    def _protokoll(text):
        sys.stderr.write(f"[QA-Autoschließen] {text}\n")
        sys.stderr.flush()

    def _meldung(art, antwort):
        def ersatz(title=None, message=None, **_kw):
            _protokoll(f"{art} unterdrückt: {title!r} – {str(message)[:160]!r} → {antwort!r}")
            return antwort
        return ersatz

    for _name in ("showinfo", "showwarning", "showerror"):
        setattr(_mb, _name, _meldung(_name, "ok"))
    for _name, _antwort in (("askyesno", False), ("askokcancel", False), ("askretrycancel", False),
                            ("askyesnocancel", None), ("askquestion", "no")):
        setattr(_mb, _name, _meldung(_name, _antwort))
    for _name in ("askopenfilename", "asksaveasfilename", "askdirectory"):
        setattr(_fd, _name, _meldung(_name, ""))
    _fd.askopenfilenames = _meldung("askopenfilenames", ())

    _alt_wait_window = _tk.Misc.wait_window
    _alt_wait_variable = _tk.Misc.wait_variable

    def _wait_window(self, window=None):
        ziel = self if window is None else window

        def schliessen():
            try:
                if ziel.winfo_exists():
                    _protokoll(f"Fenster {ziel.winfo_class()} {str(ziel)!r} ({ziel.winfo_toplevel().title()!r}) "
                               f"nach {_FRIST_MS / 1000:g} s geschlossen")
                    ziel.destroy()
            except _tk.TclError:
                pass
        job = self.after(_FRIST_MS, schliessen)
        try:
            return _alt_wait_window(self, window)
        finally:
            try:
                self.after_cancel(job)
            except _tk.TclError:
                pass

    def _wait_variable(self, name="PY_VAR"):
        def setzen():
            _protokoll(f"Warten auf Variable {str(name)!r} nach {_FRIST_MS / 1000:g} s beendet")
            try:
                self.setvar(str(name), self.getvar(str(name)))
            except _tk.TclError:
                pass
        job = self.after(_FRIST_MS, setzen)
        try:
            return _alt_wait_variable(self, name)
        finally:
            try:
                self.after_cancel(job)
            except _tk.TclError:
                pass

    _tk.Misc.wait_window = _wait_window
    _tk.Misc.waitvar = _tk.Misc.wait_variable = _wait_variable
