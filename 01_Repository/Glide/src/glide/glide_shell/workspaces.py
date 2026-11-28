# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 24: workspaces – navigation, views and status for any host (Shell 0.10.0).

A host registers its product areas (Glide: lists and pages; STEPS: keyboard,
theory, library; Chess & Chains: board, games, training) as *workspaces*; the
shell provides the navigation sidebar, the view area, lazy view creation,
keyboard switching, a status line and orderly teardown. The shell knows no
product data model: a workspace is an id, a title and a factory.

Public interface:

- `Workspace(id, title, factory, group="", order=0, shortcut=None,
  keep_alive=True, actions=())` – `factory(master, host)` returns the view
  widget; `actions` are `(label, callback)` pairs offered in the toolbar of
  the view area. A view may define `on_show()`, `on_hide()` and `on_close()`.
- `WorkspaceRegistry(workspaces=())` (Tk-free): `register`, `get`, `ordered()`
  (by group, order, registration), `groups()`, `ids()`, `neighbour(id, step)`.
- `WorkspaceHost(master, registry, roles, on_change=None, font=None)` – frame
  with sidebar, view area and status line. `show(id)` creates the view on
  first use and keeps it (`keep_alive`) or rebuilds it; `current`, `view(id)`,
  `next(step=1)`, `set_status(text)`, `set_theme(roles)`, `bind_shortcuts(
  widget, platform)` (Ctrl/Cmd+number per `shortcut`, Ctrl+Tab cycling),
  `close()` calls `on_close` of every live view, then destroys them; also
  run automatically when the host frame is destroyed.

Errors: unknown ids raise `KeyError`; an exception in a view factory is
reported through `on_error(workspace, exc)` (default: re-raise) and leaves the
previous view visible.
"""
from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass, field
from typing import Callable

from glide_shell import app_host, color_roles
from glide_shell.controls import ShellButton, _font


@dataclass(frozen=True)
class Workspace:
    id: str
    title: str
    factory: Callable
    group: str = ""
    order: int = 0
    shortcut: str | None = None
    keep_alive: bool = True
    actions: tuple = field(default=())

    def __post_init__(self):
        if not str(self.id).strip() or not str(self.title).strip():
            raise ValueError("Workspace needs id and title")
        if not callable(self.factory):
            raise ValueError(f"Workspace {self.id!r}: factory must be callable")
        object.__setattr__(self, "actions", tuple(self.actions))


class WorkspaceRegistry:
    def __init__(self, workspaces=()):
        self._items = {}
        for workspace in workspaces:
            self.register(workspace)

    def register(self, workspace):
        if not isinstance(workspace, Workspace):
            raise TypeError("only Workspace objects can be registered")
        if workspace.id in self._items:
            raise ValueError(f"duplicate workspace id {workspace.id!r}")
        if workspace.shortcut and any(w.shortcut == workspace.shortcut for w in self._items.values()):
            raise ValueError(f"shortcut {workspace.shortcut!r} already used")
        self._items[workspace.id] = workspace
        return workspace

    def get(self, workspace_id):
        return self._items[workspace_id]

    def ordered(self):
        position = {key: index for index, key in enumerate(self._items)}
        gruppen = list(dict.fromkeys(w.group for w in self._items.values()))
        return sorted(self._items.values(), key=lambda w: (gruppen.index(w.group), w.order, position[w.id]))

    def ids(self):
        return [w.id for w in self.ordered()]

    def groups(self):
        ergebnis = {}
        for workspace in self.ordered():
            ergebnis.setdefault(workspace.group, []).append(workspace)
        return ergebnis

    def neighbour(self, workspace_id, step=1):
        ids = self.ids()
        return ids[(ids.index(workspace_id) + step) % len(ids)]

    def __len__(self):
        return len(self._items)


class WorkspaceHost(tk.Frame):
    """Sidebar navigation, view area and status line for registered workspaces."""

    def __init__(self, master, registry, roles, on_change=None, on_error=None, font=None):
        self.roles = color_roles.complete(roles)
        super().__init__(master, bg=self.roles["bg"])
        self.registry, self.on_change, self.on_error = registry, on_change, on_error
        self.font = _font(self, font, 10)
        self.current = None
        self._views = {}
        self._closed = False
        self.sidebar = tk.Frame(self, bg=self.roles["card"], width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        rechts = tk.Frame(self, bg=self.roles["bg"])
        rechts.pack(side="left", fill="both", expand=True)
        self.actionbar = tk.Frame(rechts, bg=self.roles["bg"])
        self.actionbar.pack(side="top", fill="x")
        self.area = tk.Frame(rechts, bg=self.roles["bg"])
        self.area.pack(side="top", fill="both", expand=True)
        self.status = tk.Label(rechts, text="", anchor="w", bg=self.roles["card"], fg=self.roles["muted"],
                               font=self.font, padx=8, pady=3)
        self.status.pack(side="bottom", fill="x")
        self.nav_buttons = {}
        self._build_nav()
        self.bind("<Destroy>", self._on_destroy, add="+")

    # --- Navigation ------------------------------------------------------------
    def _build_nav(self):
        for kind in self.sidebar.winfo_children():
            kind.destroy()
        self.nav_buttons = {}
        for gruppe, eintraege in self.registry.groups().items():
            if gruppe:
                tk.Label(self.sidebar, text=gruppe, anchor="w", bg=self.roles["card"], fg=self.roles["muted"],
                         font=self.font, padx=10).pack(fill="x", pady=(10, 2))
            for workspace in eintraege:
                knopf = ShellButton(self.sidebar, workspace.title, lambda w=workspace.id: self.show(w),
                                    self.roles, variant="quiet", width=184, font=self.font)
                knopf.pack(padx=8, pady=1, anchor="w")
                knopf.bind("<Up>", lambda _e, w=workspace.id: self._focus_nav(w, -1))
                knopf.bind("<Down>", lambda _e, w=workspace.id: self._focus_nav(w, 1))
                self.nav_buttons[workspace.id] = knopf
        self._mark_current()

    def _focus_nav(self, workspace_id, step):
        self.nav_buttons[self.registry.neighbour(workspace_id, step)].focus_set()
        return "break"

    def _mark_current(self):
        for workspace_id, knopf in self.nav_buttons.items():
            knopf.variant = "primary" if workspace_id == self.current else "quiet"
            knopf._draw()

    # --- Ansichten -------------------------------------------------------------
    def view(self, workspace_id):
        return self._views.get(workspace_id)

    def live_views(self):
        return dict(self._views)

    def show(self, workspace_id):
        workspace = self.registry.get(workspace_id)
        if workspace_id == self.current:
            return self._views.get(workspace_id)
        ansicht = self._views.get(workspace_id)
        if ansicht is None:
            try:
                ansicht = workspace.factory(self.area, self)
            except Exception as fehler:  # pylint: disable=broad-except
                if self.on_error is None:
                    raise
                self.on_error(workspace, fehler)
                return None
            self._views[workspace_id] = ansicht
        vorher = self.current
        if vorher is not None:
            alt = self._views.get(vorher)
            if alt is not None:
                _call(alt, "on_hide")
                alt.pack_forget()
                if not self.registry.get(vorher).keep_alive:
                    _call(alt, "on_close")
                    alt.destroy()
                    del self._views[vorher]
        ansicht.pack(fill="both", expand=True)
        self.current = workspace_id
        self._build_actions(workspace)
        _call(ansicht, "on_show")
        self._mark_current()
        if callable(self.on_change):
            self.on_change(workspace_id)
        return ansicht

    def next(self, step=1):
        if not len(self.registry):
            return None
        start = self.current or self.registry.ids()[0]
        return self.show(self.registry.neighbour(start, step) if self.current else start)

    def _build_actions(self, workspace):
        for kind in self.actionbar.winfo_children():
            kind.destroy()
        for label, callback in workspace.actions:
            ShellButton(self.actionbar, label, callback, self.roles, size="small", font=self.font).pack(
                side="left", padx=(8, 0), pady=4)

    # --- Status, Theme, Kürzel -------------------------------------------------
    def set_status(self, text):
        self.status.configure(text=str(text))

    def set_theme(self, roles):
        self.roles = color_roles.complete(roles)
        t = self.roles
        for widget in (self, self.area, self.actionbar, self.area.master):
            widget.configure(bg=t["bg"])
        self.sidebar.configure(bg=t["card"])
        self.status.configure(bg=t["card"], fg=t["muted"])
        self._build_nav()
        if self.current:
            self._build_actions(self.registry.get(self.current))
        for ansicht in self._views.values():
            if callable(getattr(ansicht, "set_theme", None)):
                ansicht.set_theme(t)

    def bind_shortcuts(self, widget, platform):
        eintraege = []
        for workspace in self.registry.ordered():
            if workspace.shortcut:
                eintraege += app_host.primary_shortcuts(
                    workspace.shortcut, lambda _e, w=workspace.id: (self.show(w), "break")[1], platform)
        eintraege.append(("<Control-Tab>", lambda _e: (self.next(1), "break")[1], app_host.ALL))
        return app_host.bind_shortcuts(widget, eintraege, platform)

    # --- Abbau -------------------------------------------------------------------
    def close(self):
        if self._closed:
            return
        self._closed = True
        for ansicht in list(self._views.values()):
            _call(ansicht, "on_close")
            try:
                ansicht.destroy()
            except tk.TclError:
                pass
        self._views.clear()
        self.current = None

    def _on_destroy(self, event):
        if event.widget is self:
            self.close()


def _call(widget, name):
    methode = getattr(widget, name, None)
    if callable(methode):
        methode()
