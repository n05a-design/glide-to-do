# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 23: general controls – button, search field, tooltip, toolbar (Shell 0.10.0).

Closes the gap the portable design contract listed as "not yet in the shell"
(§5.6): general buttons, search fields, tooltips and toolbars. Colours come
from a role dictionary (`color_roles`), fonts from the host's font provider
(`custom_controls.set_font_provider`) or an explicit `font`; timers run in the
widget's `AfterScope`, so nothing fires after a widget is destroyed.

Public interface:

- `ShellButton(master, text, command, roles, variant="secondary",
  size="medium", icon=False, font=None, width=None)` – canvas button with
  hover, pressed, focus ring and disabled state; Space and Return invoke it.
  Variants `primary`, `secondary`, `danger`, `quiet`; sizes `small` (28 px),
  `medium` (34 px), `large` (42 px); `icon=True` makes it square (B15: fixed
  outer size, visible focus). Methods: `invoke()`, `set_theme(roles)`,
  `set_text(text)`, `set_enabled(flag)`, `enabled`.
- `SearchField(master, roles, placeholder="", on_change=None, on_submit=None,
  delay_ms=150, font=None)` – entry with placeholder, clear button and
  debounced `on_change(text)`; Escape clears, Return calls `on_submit(text)`.
  Methods: `get()`, `set(text, notify=True)`, `clear()`, `focus_entry()`,
  `set_theme(roles)`.
- `Tooltip(widget, text, roles, delay_ms=500, font=None)` – text or callable
  shown after the delay; hides on leave, click, focus loss and destroy.
  `attach_tooltip(...)` is a shortcut; `Tooltip.detach()` removes the bindings.
- `Toolbar(master, roles, wrap=True)` – groups of buttons with separators;
  `add_group(name)` -> `ToolGroup` with `add_button(text, command, **kw)`.
  With `wrap=True` groups flow onto further rows when the toolbar is narrower
  than their combined width (responsive). `set_theme(roles)` updates all.

Required colour roles: `card`, `bg`, `text`, `muted`, `line`, `hover`,
`input`, `input_border`, `placeholder`, `ui_accent`, `selection_text`,
`delete`; `focus` and `disabled` fall back as in `color_roles.complete`.
"""
from __future__ import annotations

import tkinter as tk

from glide_shell import custom_controls, color_roles, window_lifetime

SIZES = {"small": 28, "medium": 34, "large": 42}
VARIANTS = ("primary", "secondary", "danger", "quiet")


def _font(widget, font, size=10):
    return font if font is not None else custom_controls._default_font(size, widget)


class ShellButton(tk.Canvas):
    """Themed canvas button (see module docstring)."""

    def __init__(self, master, text, command, roles, variant="secondary", size="medium",
                 icon=False, font=None, width=None):
        if variant not in VARIANTS:
            raise ValueError(f"variant must be one of {VARIANTS}")
        if size not in SIZES:
            raise ValueError(f"size must be one of {tuple(SIZES)}")
        self.roles = color_roles.complete(roles)
        hoehe = SIZES[size]
        super().__init__(master, height=hoehe, width=width or hoehe, highlightthickness=0, bd=0,
                         bg=self.roles["card"], takefocus=1, cursor="hand2")
        self.text, self.command, self.variant, self.icon = str(text), command, variant, bool(icon)
        self.font = _font(self, font, 11 if icon else 10)
        self.fixed_width = width
        self.enabled = True
        self.hovered = self.pressed = self.focused = False
        for sequence, handler in (("<Enter>", self._enter), ("<Leave>", self._leave),
                                  ("<ButtonPress-1>", self._press), ("<ButtonRelease-1>", self._release),
                                  ("<FocusIn>", self._focus_in), ("<FocusOut>", self._focus_out),
                                  ("<KeyPress-space>", self._key), ("<Return>", self._key),
                                  ("<Configure>", lambda _e: self._draw())):
            self.bind(sequence, handler, add="+")
        self._fit()
        self._draw()

    # --- Zustand ---------------------------------------------------------------
    def set_theme(self, roles):
        self.roles = color_roles.complete(roles)
        self.configure(bg=self.roles["card"])
        self._draw()

    def set_text(self, text):
        self.text = str(text)
        self._fit()
        self._draw()

    def set_enabled(self, flag):
        self.enabled = bool(flag)
        self.configure(cursor="hand2" if self.enabled else "arrow", takefocus=1 if self.enabled else 0)
        self._draw()

    def invoke(self):
        if self.enabled and callable(self.command):
            return self.command()
        return None

    # --- Ereignisse ------------------------------------------------------------
    def _enter(self, _e=None):
        self.hovered = True
        self._draw()

    def _leave(self, _e=None):
        self.hovered = self.pressed = False
        self._draw()

    def _press(self, _e=None):
        if self.enabled:
            self.pressed = True
            self.focus_set()
            self._draw()

    def _release(self, event=None):
        war = self.pressed
        self.pressed = False
        self._draw()
        inside = event is None or (0 <= event.x < self.winfo_width() and 0 <= event.y < self.winfo_height())
        if war and inside:
            self.invoke()

    def _key(self, _e=None):
        self.invoke()
        return "break"

    def _focus_in(self, _e=None):
        self.focused = True
        self._draw()

    def _focus_out(self, _e=None):
        self.focused = False
        self._draw()

    # --- Zeichnen --------------------------------------------------------------
    def _fit(self):
        if self.icon or self.fixed_width:
            return
        try:
            breite = custom_controls._font_obj(self, self.font).measure(self.text)
        except tk.TclError:
            breite = 8 * len(self.text)
        self.configure(width=max(int(self["height"]) * 2, breite + 28))

    def colours(self):
        """(fill, outline, text) for the current state; public for tests and hosts."""
        t = self.roles
        if not self.enabled:
            return t["card"], t["line"], t["disabled"]
        if self.variant == "primary":
            fill = t["ui_accent"]
            return fill, fill, t["on_accent"]
        if self.variant == "danger":
            return (t["delete"], t["delete"], t["on_accent"]) if self.hovered or self.pressed else (t["card"], t["delete"], t["delete"])
        if self.variant == "quiet":
            return (t["hover"] if self.hovered or self.pressed else t["card"]), (t["hover"] if self.hovered else t["card"]), t["text"]
        return (t["hover"] if self.hovered or self.pressed else t["card"]), t["input_border"], t["text"]

    def _draw(self):
        try:
            self.delete("all")
            w, h = max(self.winfo_width(), int(self["width"])), max(self.winfo_height(), int(self["height"]))
            if self.winfo_width() > 1:
                w = self.winfo_width()
            fill, outline, ink = self.colours()
            radius = min(10, h // 2 - 1)
            versatz = 1 if self.pressed else 0
            self.create_polygon(custom_controls.rounded_rect_points(1, 1 + versatz, w - 2, h - 2, radius),
                                smooth=True, fill=fill, outline=outline, width=1)
            if self.focused and self.enabled:
                self.create_polygon(custom_controls.rounded_rect_points(-1, -1, w, h, radius + 2), smooth=True,
                                    fill="", outline=self.roles["focus"], width=2)
            self.create_text(w // 2, h // 2 + versatz, text=self.text, fill=ink, font=self.font)
        except tk.TclError:
            pass


class SearchField(tk.Frame):
    """Entry with placeholder, clear button and debounced change callback."""

    def __init__(self, master, roles, placeholder="", on_change=None, on_submit=None, delay_ms=150, font=None):
        self.roles = color_roles.complete(roles)
        super().__init__(master, bg=self.roles["input"], highlightthickness=1,
                         highlightbackground=self.roles["input_border"], highlightcolor=self.roles["focus"])
        self.placeholder, self.on_change, self.on_submit, self.delay_ms = placeholder, on_change, on_submit, int(delay_ms)
        self.scope = window_lifetime.scope_for(self)
        self._job = None
        self.variable = tk.StringVar(self)
        schrift = _font(self, font, 10)
        self.entry = tk.Entry(self, textvariable=self.variable, relief="flat", bd=0, font=schrift,
                              bg=self.roles["input"], fg=self.roles["text"], insertbackground=self.roles["text"])
        self.entry.pack(side="left", fill="x", expand=True, padx=(8, 2), pady=5)
        self.hint = tk.Label(self, text=placeholder, font=schrift, bg=self.roles["input"], fg=self.roles["placeholder"])
        self.hint.bind("<Button-1>", lambda _e: self.focus_entry())
        self.clear_button = ShellButton(self, "×", self.clear, self.roles, variant="quiet", size="small", icon=True)
        self.clear_button.configure(bg=self.roles["input"])
        self.variable.trace_add("write", self._changed)
        self.entry.bind("<Escape>", lambda _e: (self.clear(), "break")[1])
        self.entry.bind("<Return>", self._submit)
        self.entry.bind("<FocusIn>", lambda _e: self._update_hint(), add="+")
        self.entry.bind("<FocusOut>", lambda _e: self._update_hint(), add="+")
        self._update_hint()

    def get(self):
        return self.variable.get()

    def set(self, text, notify=True):
        self._silent = not notify
        try:
            self.variable.set(text)
        finally:
            self._silent = False

    def clear(self):
        self.set("")
        self.focus_entry()

    def focus_entry(self):
        self.entry.focus_set()

    def set_theme(self, roles):
        self.roles = color_roles.complete(roles)
        t = self.roles
        self.configure(bg=t["input"], highlightbackground=t["input_border"], highlightcolor=t["focus"])
        self.entry.configure(bg=t["input"], fg=t["text"], insertbackground=t["text"])
        self.hint.configure(bg=t["input"], fg=t["placeholder"])
        self.clear_button.set_theme(t)
        self.clear_button.configure(bg=t["input"])

    _silent = False

    def _changed(self, *_args):
        self._update_hint()
        if self._silent or not callable(self.on_change):
            return
        if self._job is not None:
            self.scope.cancel(self._job)
        self._job = self.scope.after(self.delay_ms, self._fire)

    def _fire(self):
        self._job = None
        self.on_change(self.get())

    def flush(self):
        """Run a pending change callback now (tests, closing a view)."""
        if self._job is not None:
            self.scope.cancel(self._job)
            self._fire()

    def _submit(self, _e=None):
        self.flush()
        if callable(self.on_submit):
            self.on_submit(self.get())
        return "break"

    def _update_hint(self):
        leer = not self.get()
        if leer and self.focus_get() is not self.entry and self.placeholder:
            self.hint.place(in_=self.entry, x=0, rely=0.5, anchor="w")
        else:
            self.hint.place_forget()
        if leer:
            self.clear_button.pack_forget()
        elif not self.clear_button.winfo_ismapped():
            self.clear_button.pack(side="right", padx=2)


class Tooltip:
    """Delayed tooltip for one widget (see module docstring)."""

    def __init__(self, widget, text, roles, delay_ms=500, font=None):
        self.widget, self.text, self.delay_ms = widget, text, int(delay_ms)
        self.roles = color_roles.complete(roles)
        self.font = font
        self.window = None
        self._job = None
        self.scope = window_lifetime.scope_for(widget)
        self._bindings = [(seq, widget.bind(seq, handler, add="+")) for seq, handler in
                          (("<Enter>", self._schedule), ("<Leave>", self.hide), ("<ButtonPress>", self.hide),
                           ("<FocusOut>", self.hide), ("<Destroy>", self.hide))]

    def current_text(self):
        return str(self.text() if callable(self.text) else self.text or "")

    def _schedule(self, _e=None):
        self._cancel()
        self._job = self.scope.after(self.delay_ms, self.show)

    def _cancel(self):
        if self._job is not None:
            self.scope.cancel(self._job)
            self._job = None

    def show(self):
        self._job = None
        text = self.current_text()
        if not text or self.window is not None:
            return None
        try:
            x = self.widget.winfo_rootx() + 8
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
            self.window = tk.Toplevel(self.widget)
            self.window.wm_overrideredirect(True)
            self.window.wm_geometry(f"+{x}+{y}")
            tk.Label(self.window, text=text, justify="left", wraplength=360, font=_font(self.widget, self.font, 9),
                     bg=self.roles["text"], fg=self.roles["card"], padx=8, pady=4).pack()
        except tk.TclError:
            self.window = None
        return self.window

    def hide(self, _e=None):
        self._cancel()
        if self.window is not None:
            try:
                self.window.destroy()
            except tk.TclError:
                pass
            self.window = None

    def detach(self):
        self.hide()
        for sequence, funcid in self._bindings:
            try:
                self.widget.unbind(sequence, funcid)
            except tk.TclError:
                pass
        self._bindings = []


def attach_tooltip(widget, text, roles, delay_ms=500, font=None):
    return Tooltip(widget, text, roles, delay_ms=delay_ms, font=font)


class ToolGroup(tk.Frame):
    def __init__(self, toolbar, name):
        super().__init__(toolbar, bg=toolbar.roles["card"])
        self.toolbar, self.name, self.buttons = toolbar, name, []

    def add_button(self, text, command, **kwargs):
        knopf = ShellButton(self, text, command, self.toolbar.roles, **kwargs)
        knopf.pack(side="left", padx=2, pady=2)
        self.buttons.append(knopf)
        self.toolbar.schedule_layout()
        return knopf


class Toolbar(tk.Frame):
    """Grouped tool buttons with separators; flows onto rows when narrow."""

    def __init__(self, master, roles, wrap=True):
        self.roles = color_roles.complete(roles)
        super().__init__(master, bg=self.roles["card"])
        self.wrap = wrap
        self.groups = []
        self._separators = []
        self.rows = 1
        self.relayouts = 0
        self._pending = None
        self.scope = window_lifetime.scope_for(self)
        # Größenwechsel werden im Leerlauf gebündelt (keine Configure-Kaskade, kein
        # update_idletasks im Ereignis); der Zeitgeberbereich endet mit dem Widget.
        self.bind("<Configure>", lambda _e: self.schedule_layout(), add="+")

    def add_group(self, name):
        gruppe = ToolGroup(self, name)
        self.groups.append(gruppe)
        self.schedule_layout()
        return gruppe

    def schedule_layout(self):
        if self._pending is None and not self.scope.closed:
            self._pending = self.scope.after_idle(self._run_scheduled)

    def _run_scheduled(self):
        self._pending = None
        self._relayout()

    def set_theme(self, roles):
        self.roles = color_roles.complete(roles)
        self.configure(bg=self.roles["card"])
        for gruppe in self.groups:
            gruppe.configure(bg=self.roles["card"])
            for knopf in gruppe.buttons:
                knopf.set_theme(self.roles)
        for trenner in self._separators:
            trenner.configure(bg=self.roles["line"])

    _layout = None

    def plan(self, available):
        """Row index per group for `available` pixels (pure; used by `_relayout`)."""
        zeilen, zeile, belegt = [], 0, 0
        for index, gruppe in enumerate(self.groups):
            breite = gruppe.winfo_reqwidth() + 9
            if self.wrap and index and belegt + breite > available:
                zeile, belegt = zeile + 1, 0
            zeilen.append(zeile)
            belegt += breite
        return zeilen

    def _relayout(self):
        """Sofortige Neuberechnung (Tests, Host nach Größenwechsel); sicher nach dem Abbau."""
        try:
            if not self.winfo_exists():
                return
            verfuegbar = self.master.winfo_width() if self.master.winfo_width() > 1 else 10 ** 6
        except tk.TclError:
            return
        zeilen = self.plan(verfuegbar)
        if zeilen == self._layout:
            return
        self._layout = zeilen
        self.relayouts += 1
        for trenner in self._separators:
            trenner.destroy()
        self._separators = []
        spalte, vorige = 0, None
        for gruppe, zeile in zip(self.groups, zeilen):
            if zeile != vorige:
                spalte, vorige = 0, zeile
            if spalte:
                trenner = tk.Frame(self, width=1, bg=self.roles["line"])
                trenner.grid(row=zeile, column=spalte, sticky="ns", padx=4, pady=6)
                self._separators.append(trenner)
                spalte += 1
            gruppe.grid(row=zeile, column=spalte, sticky="w")
            spalte += 1
        self.rows = (zeilen[-1] + 1) if zeilen else 1
