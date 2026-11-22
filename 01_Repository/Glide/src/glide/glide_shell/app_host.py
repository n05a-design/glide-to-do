# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 16: App-Host – Hauptfenster, Startprüfungen, Menüleiste, Kürzel und Beenden für einen Controller (Phase 5).

Die Shell übernimmt den Lebenslauf des Hauptfensters; die Anwendung ist der
Controller, der darin seinen Inhalt aufbaut. Ablauf von `AppHost.run`:

1. `before_tk`: Schritte vor dem ersten Tk-Interpreter (etwa private
   Schriften registrieren – Aqua legt den Schriftbestand beim ersten `Tk()`
   fest – oder eine Windows-Anwendungskennung setzen).
2. Hauptfenster anlegen.
3. `preflight`: Startprüfungen. Jede erhält das Fenster und liefert `None`
   oder `(titel, meldung)`. Beim ersten Befund zeigt der Host die Meldung,
   schließt das Fenster und beendet mit Exitcode 1; der Controller entsteht
   dann nicht.
4. `splash`: optionaler Platzhalter, solange der Controller aufbaut.
5. `controller_factory(root)` baut den Inhalt; `on_ready(root)` meldet den
   fertigen Aufbau; danach läuft die Ereignisschleife.

Dazu kommen Bausteine, die der Controller aufruft: `attach_menubar`,
`bind_shortcuts` (Kürzeltabelle mit Plattformangabe), `primary_shortcuts`
(Strg und unter macOS zusätzlich Cmd) und `install_close` (Fenster schließen
und unter macOS das Beenden aus dem App-Menü über denselben Weg).
Texte, Prüfungen und Handler liefert der Host.
"""

import tkinter as tk
from tkinter import messagebox

from glide_shell import window_lifetime

ALL = None
MACOS = "macos"
WINDOWS = "windows"
LINUX = "linux"


def platform_of(windowing_system):
    """Plattformkennung aus `tk windowingsystem`: aqua, win32 oder x11."""
    return {"aqua": MACOS, "win32": WINDOWS}.get(windowing_system, LINUX)


def _show_error(title, message, parent=None):
    messagebox.showerror(title, message, parent=parent)


class AppHost:
    """Startet das Hauptfenster und bettet den Controller ein."""

    def __init__(self, *, before_tk=(), preflight=(), splash=None, on_ready=None,
                 show_error=None, tk_factory=None):
        self.before_tk = tuple(before_tk)
        self.preflight = tuple(preflight)
        self.splash = splash
        self.on_ready = on_ready
        self.show_error = show_error or _show_error
        self.tk_factory = tk_factory or tk.Tk
        self.root = None
        self.controller = None

    def create_root(self):
        for step in self.before_tk:
            step()
        self.root = self.tk_factory()
        return self.root

    def check(self, root):
        """Startprüfungen; beim ersten Befund Meldung, Fenster schließen, Exitcode 1."""
        for check in self.preflight:
            problem = check(root)
            if problem:
                title, message = problem[0], problem[1]
                root.withdraw()
                self.show_error(title, message, parent=root)
                root.destroy()
                raise SystemExit(1)

    def build(self, controller_factory, root):
        placeholder = self.splash(root) if self.splash is not None else None
        try:
            self.controller = controller_factory(root)
        finally:
            if placeholder is not None:
                placeholder.destroy()
        if self.on_ready is not None:
            self.on_ready(root)
        return self.controller

    def run(self, controller_factory, mainloop=True):
        """Gesamter Start; `mainloop=False` baut nur auf (Tests, eingebettete Nutzung)."""
        root = self.create_root()
        self.check(root)
        controller = self.build(controller_factory, root)
        if mainloop:
            root.mainloop()
        return controller


def attach_menubar(root, menubar):
    """Menüleiste als Fenstermenü setzen; False, wenn Tk sie ablehnt."""
    try:
        root.config(menu=menubar)
    except tk.TclError:
        return False
    return True


def primary_shortcuts(key, handler, platform, shift=False):
    """Kürzel mit der Hauptmodifikatortaste: Strg überall, unter macOS zusätzlich Cmd."""
    middle = "Shift-" if shift else ""
    entries = [(f"<Control-{middle}{key}>", handler, ALL)]
    if platform == MACOS:
        entries.append((f"<Command-{middle}{key}>", handler, MACOS))
    return entries


def bind_shortcuts(widget, entries, platform):
    """Kürzeltabelle binden; Einträge sind (Sequenz, Handler, Plattform oder None).

    Liefert die gebundenen Sequenzen in Reihenfolge; Einträge anderer
    Plattformen bleiben ungebunden.
    """
    bound = []
    for sequence, handler, only in entries:
        if only is not ALL and only != platform:
            continue
        widget.bind(sequence, handler)
        bound.append(sequence)
    return bound


def install_close(root, on_close, platform, quit_command=True, scope=None):
    """Fenster schließen und – unter macOS – Beenden aus dem App-Menü auf `on_close` legen.

    macOS fängt Cmd+Q ab und würde sonst `WM_DELETE_WINDOW` und damit eine
    Rückfrage des Hosts überspringen. Das Beenden läuft im Leerlauf über den
    Zeitgeberbereich des Fensters, weil es innerhalb der Menüverfolgung von
    macOS eintrifft und eine Rückfrage dort hängen bliebe. Ein Host mit
    eigenem Zeitgeberbereich für das Hauptfenster reicht ihn als `scope` ein.
    """
    root.protocol("WM_DELETE_WINDOW", on_close)
    # Das Beenden aus dem App-Menü gehört zum Hauptfenster (`tk.Tk`). Ein
    # eingebettetes Fenster (`Toplevel`) setzt nur seinen Fensterknopf und
    # überschreibt nicht den Beenden-Weg der Anwendung.
    if platform != MACOS or not quit_command or not callable(getattr(root, "createcommand", None)):
        return False
    if scope is None:
        scope = window_lifetime.scope_for(root)
    try:
        root.createcommand("::tk::mac::Quit", lambda *_args: scope.after_idle(on_close))
    except tk.TclError:
        return False
    return True
