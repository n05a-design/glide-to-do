# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 6: Demonstrationshost – eine kleine Tk-App nur aus Shell-Bausteinen (D95).

Der Host zeigt Folgeprojekten das Nutzungsmuster der Glide Shell ohne Glide:
Menüleiste über `desktop_adapter`, ein wiederkehrender Zeitgeber im eigenen
`AfterScope`, ein kurzer Übergang aus `motion` im selben Bereich,
Bedienelemente aus `custom_controls`, ein modaler Dialog über
`modal_session.create_dialog` und `run_modal`, eine Fensterlage über
`window_geometry`, das Systemdesign über `system_appearance` (nur ohne
vorgegebene Farben) und ein Zähler mit Rückgängig/Wiederholen als
Befehlsobjekte über `command_history`. `main` startet über `app_host`:
Fenster, Kürzel (Strg/Cmd+Z, Wiederholen) und Schließweg kommen aus der
Shell, der Demohost ist der Controller. Texte und Farben liefert der Host
selbst; die Shell kennt sie nicht.

Start: `python -m glide_shell.demo` mit dem Ordner über `glide_shell` im
Suchpfad. Vertrag: `tests/integration/test_shell_demohost.py`.
"""

import time
import tkinter as tk

from glide_shell import (app_host, command_history, custom_controls, desktop_adapter, modal_session, motion,
                         system_appearance, window_geometry, window_lifetime)

PALETTE = {"bg": "#F5F5F7", "card": "#FFFFFF", "text": "#15243C", "muted": "#6E6E73", "accent": "#0A84FF"}
DARK_PALETTE = {"bg": "#1C1C1E", "card": "#2C2C2E", "text": "#F2F2F7", "muted": "#98989D", "accent": "#0A84FF"}
MIN_SIZE = (360, 220)
TEXTS = {
    "title": "Glide Shell demo",
    "menu_file": "File",
    "menu_dialog": "Open dialog …",
    "menu_quit": "Quit",
    "hint": "Built only from glide_shell and tkinter.",
    "toggle": "Show seconds",
    "dialog_title": "Example dialog",
    "dialog_text": "A modal dialog from create_dialog; Escape or OK closes it.",
    "ok": "OK",
    "menu_edit": "Edit",
    "menu_undo": "Undo",
    "menu_redo": "Redo",
    "add": "Add one",
    "count": "Count: {count}",
}
TICK_MS = 1000


class _Increment(command_history.Command):
    """Ein Schritt des Zählers als Befehl."""

    def __init__(self, host):
        self.host = host

    def execute(self):
        self.host.count += 1
        self.host._show_count()

    def undo(self):
        self.host.count -= 1
        self.host._show_count()


class DemoHost:
    """Hauptfenster des Beispielhosts; besitzt seine Zeitgeber über einen Bereich."""

    def __init__(self, root, texts=None, colors=None, geometry=None):
        self.root = root
        self.texts = dict(TEXTS, **(texts or {}))
        # Ohne Farben des Hosts folgt der Demohost dem Systemdesign.
        self.system_dark = None if colors else system_dark(root)
        self.colors = dict(DARK_PALETTE if self.system_dark else PALETTE, **(colors or {}))
        self.count = 0
        self.history = command_history.CommandHistory()
        self.redo = self.history.redo
        if geometry:
            self.place(geometry)
        self.scope = window_lifetime.scope_for(root)
        self.transitions = motion.Transitions(self.scope.after, self.scope.cancel)
        self.dialogs_opened = 0
        self.counter = None
        root.title(self.texts["title"])
        root.configure(bg=self.colors["bg"])
        self.menus = []
        self.platform = app_host.platform_of(root.tk.call("tk", "windowingsystem"))
        self.menubar = desktop_adapter.build_menu_tree(root, [
            (self.texts["menu_file"], [
                (self.texts["menu_dialog"], self.open_dialog,
                 desktop_adapter.format_accelerator("D"), "open_dialog"),
                None,
                (self.texts["menu_quit"], self.close, "", "quit"),
            ]),
            (self.texts["menu_edit"], [
                (self.texts["menu_undo"], self.undo_step, desktop_adapter.format_accelerator("Z"), "undo"),
                (self.texts["menu_redo"], self.redo_step, desktop_adapter.format_redo_accelerator(), "redo"),
            ]),
        ], menus_out=self.menus)
        app_host.attach_menubar(root, self.menubar)
        app_host.bind_shortcuts(root, app_host.primary_shortcuts("z", lambda _e: self.undo_step(), self.platform)
                                + app_host.primary_shortcuts("Z", lambda _e: self.redo_step(), self.platform, shift=True),
                                self.platform)
        app_host.install_close(root, self.request_close, self.platform, scope=self.scope)
        tk.Label(root, text=self.texts["hint"], bg=self.colors["bg"], fg=self.colors["muted"]).pack(
            padx=20, pady=(16, 4), anchor="w")
        self.seconds = tk.BooleanVar(root, value=True)
        self.toggle = custom_controls.GlideCheckbutton(
            root, text=self.texts["toggle"], variable=self.seconds,
            bg=self.colors["bg"], fg=self.colors["text"], command=self._toggled)
        self.toggle.pack(padx=20, anchor="w")
        self.clock = tk.Label(root, bg=self.colors["bg"], fg=self.colors["text"], font=("TkDefaultFont", 18))
        self.clock.pack(padx=20, pady=(8, 4), anchor="w")
        self.counter = tk.Label(root, bg=self.colors["bg"], fg=self.colors["text"])
        self.counter.pack(padx=20, anchor="w")
        tk.Button(root, text=self.texts["add"], command=self.add).pack(padx=20, pady=(4, 16), anchor="w")
        self._show_count()
        self.tick()

    def place(self, geometry):
        """Gemerkte Lage übernehmen, aber auf dem Bildschirm halten (`window_geometry`)."""
        parsed = window_geometry.parse(geometry)
        if parsed is None:
            return None
        placed = window_geometry.format_geometry(*window_geometry.clamp(
            *parsed, self.root.winfo_screenwidth(), self.root.winfo_screenheight(), MIN_SIZE))
        self.root.geometry(placed)
        return placed

    def _show_count(self):
        if self.counter is not None:
            self.counter.configure(text=self.texts["count"].format(count=self.count))

    def add(self):
        """Eine Änderung als Befehl; ein neuer Schritt verwirft Wiederholen."""
        self.history.execute(_Increment(self))

    def undo_step(self):
        return self.history.undo() == command_history.DONE

    def redo_step(self):
        return self.history.redo_step() == command_history.DONE

    def _toggled(self):
        self.tick()
        self.pulse()

    def pulse(self):
        """Uhr kurz in der Akzentfarbe aufleuchten lassen; ein neuer Puls bricht den alten ab."""
        self.transitions.start(
            "clock", lambda value: self.clock.configure(
                fg=self.colors["accent"] if value < 1.0 else self.colors["text"]),
            duration_ms=120)

    def tick(self):
        """Uhr aktualisieren und den nächsten Lauf im eigenen Bereich planen."""
        muster = "%H:%M:%S" if self.seconds.get() else "%H:%M"
        self.clock.configure(text=time.strftime(muster))
        job = getattr(self, "_tick_job", None)
        if job is not None:
            self.scope.cancel(job)
        self._tick_job = self.scope.after(TICK_MS, self.tick)

    def open_dialog(self):
        """Modaler Dialog über die Dialogfabrik; endet mit Escape oder OK."""
        dialog = modal_session.create_dialog(
            self.root, self.texts["dialog_title"], background=self.colors["bg"],
            withdrawn=True, resizable=(False, False))
        tk.Label(dialog, text=self.texts["dialog_text"], bg=self.colors["bg"], fg=self.colors["text"],
                 wraplength=320, justify="left").pack(padx=20, pady=(16, 8))
        tk.Button(dialog, text=self.texts["ok"], command=dialog.destroy).pack(pady=(0, 16))
        dialog.bind("<Escape>", lambda _event: dialog.destroy())
        dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)
        dialog.deiconify()
        self.dialogs_opened += 1
        modal_session.run_modal(self.root, dialog, background=self.colors["bg"])
        return "break"

    def request_close(self):
        """Schließweg des App-Hosts: Fensterknopf und unter macOS Cmd+Q."""
        self.close()

    def close(self):
        """Fenster schließen; Übergänge enden, der Bereich bricht alle Zeitgeber ab."""
        self.transitions.close()
        self.root.destroy()


def system_dark(root):
    """Hell/Dunkel des Systems über Tk erfragen; None, wenn Tk es nicht meldet."""
    if root.tk.call("tk", "windowingsystem") != "aqua":
        return None
    try:
        return system_appearance.tk_is_dark(root.tk.call("tk::unsupported::MacWindowStyle", "isdark", root))
    except tk.TclError:
        return None


def main():
    """Start über den App-Host der Shell; der Demohost ist der Controller."""
    return app_host.AppHost().run(DemoHost)


if __name__ == "__main__":
    main()
