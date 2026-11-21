# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 6: Demonstrationshost – eine kleine Tk-App nur aus Shell-Bausteinen (D95).

Der Host zeigt Folgeprojekten das Nutzungsmuster der Glide Shell ohne Glide:
Menüleiste über `desktop_adapter`, ein wiederkehrender Zeitgeber im eigenen
`AfterScope`, ein kurzer Übergang aus `motion` im selben Bereich,
Bedienelemente aus `custom_controls` und ein modaler Dialog über
`modal_session.create_dialog` und `run_modal`. Texte und Farben liefert der
Host selbst; die Shell kennt sie nicht.

Start: `python -m glide_shell.demo` mit dem Ordner über `glide_shell` im
Suchpfad. Vertrag: `tests/integration/test_shell_demohost.py`.
"""

import time
import tkinter as tk

from glide_shell import custom_controls, desktop_adapter, modal_session, motion, window_lifetime

PALETTE = {"bg": "#F5F5F7", "card": "#FFFFFF", "text": "#15243C", "muted": "#6E6E73", "accent": "#0A84FF"}
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
}
TICK_MS = 1000


class DemoHost:
    """Hauptfenster des Beispielhosts; besitzt seine Zeitgeber über einen Bereich."""

    def __init__(self, root, texts=None, colors=None):
        self.root = root
        self.texts = dict(TEXTS, **(texts or {}))
        self.colors = dict(PALETTE, **(colors or {}))
        self.scope = window_lifetime.scope_for(root)
        self.transitions = motion.Transitions(self.scope.after, self.scope.cancel)
        self.dialogs_opened = 0
        root.title(self.texts["title"])
        root.configure(bg=self.colors["bg"])
        self.menus = []
        self.menubar = desktop_adapter.build_menu_tree(root, [
            (self.texts["menu_file"], [
                (self.texts["menu_dialog"], self.open_dialog,
                 desktop_adapter.format_accelerator("D"), "open_dialog"),
                None,
                (self.texts["menu_quit"], self.close, "", "quit"),
            ]),
        ], menus_out=self.menus)
        root.configure(menu=self.menubar)
        tk.Label(root, text=self.texts["hint"], bg=self.colors["bg"], fg=self.colors["muted"]).pack(
            padx=20, pady=(16, 4), anchor="w")
        self.seconds = tk.BooleanVar(root, value=True)
        self.toggle = custom_controls.GlideCheckbutton(
            root, text=self.texts["toggle"], variable=self.seconds,
            bg=self.colors["bg"], fg=self.colors["text"], command=self._toggled)
        self.toggle.pack(padx=20, anchor="w")
        self.clock = tk.Label(root, bg=self.colors["bg"], fg=self.colors["text"], font=("TkDefaultFont", 18))
        self.clock.pack(padx=20, pady=(8, 16), anchor="w")
        self.tick()

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

    def close(self):
        """Fenster schließen; Übergänge enden, der Bereich bricht alle Zeitgeber ab."""
        self.transitions.close()
        self.root.destroy()


def main():
    root = tk.Tk()
    DemoHost(root)
    root.mainloop()


if __name__ == "__main__":
    main()
