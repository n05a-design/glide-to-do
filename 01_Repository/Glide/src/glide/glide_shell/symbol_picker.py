# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 28: symbol picker dialog over a `SymbolRegistry` (Shell 0.11.0).

The host supplies the registry (its providers), a renderer and colour roles;
the picker shows categories, search, favourites, recently used, a preview
with origin and licence, and returns the chosen symbol id. Rendering goes
through a `resources.BoundedCache` keyed by (symbol id, size, theme key) so
reopening the picker reuses images and memory stays bounded. A symbol that
cannot be rendered shows a text fallback instead of failing.

Public interface:

- `SymbolPicker(master, registry, roles, render, state=None, title="Symbols",
  texts=None, size=24, columns=8, cache=None, extra_actions=())` –
  `render(symbol, size, roles)` returns a Tk image or None. `texts` overrides
  the English UI strings (keys in `TEXTS`). `extra_actions` are `(label,
  callback)` pairs shown in the footer (for example "Import PNG…"); a
  callback may return True to refresh the registry.
  `run()` → symbol id or None (modal, focus returns to the opener);
  `choose(symbol_id)` and `close()` for tests and keyboard paths.
- `TEXTS` – default English texts.

Keyboard: arrows move in the grid, Return chooses, Escape cancels, Ctrl+F
focuses the search, F toggles the favourite of the selection.
"""
from __future__ import annotations

import tkinter as tk

from glide_shell import color_roles, modal_session, window_lifetime
from glide_shell.controls import SearchField, ShellButton, _font
from glide_shell.resources import BoundedCache

FAVORITES = "__favorites__"
RECENT = "__recent__"
ALL = "__all__"
TEXTS = {"favorites": "Favourites", "recent": "Recently used", "all": "All symbols", "search": "Search symbols",
         "choose": "Choose", "cancel": "Cancel", "favorite": "Favourite", "unfavorite": "Remove favourite",
         "empty": "No symbols here.", "origin": "Origin", "license": "Licence", "category": "Category"}


class SymbolPicker:
    def __init__(self, master, registry, roles, render, state=None, title="Symbols", texts=None, size=24,
                 columns=8, cache=None, extra_actions=()):
        self.master, self.registry, self.render = master, registry, render
        self.roles = color_roles.complete(roles)
        self.state = state
        self.texts = {**TEXTS, **(texts or {})}
        self.size, self.columns = int(size), int(columns)
        self.cache = cache or BoundedCache("symbol-picker", max_entries=600)
        self.result = None
        self.selected = None
        self.category = ALL
        self.cells = {}
        self.extra_actions = tuple(extra_actions)
        r = self.roles
        self.dialog = modal_session.create_dialog(master, title, background=r["bg"], minsize=(620, 440))
        self.dialog.protocol("WM_DELETE_WINDOW", self.close)
        kopf = tk.Frame(self.dialog, bg=r["bg"])
        kopf.pack(fill="x", padx=12, pady=(12, 6))
        self.search = SearchField(kopf, r, placeholder=self.texts["search"], on_change=lambda _t: self.fill(), delay_ms=120)
        self.search.pack(fill="x")
        mitte = tk.Frame(self.dialog, bg=r["bg"])
        mitte.pack(fill="both", expand=True, padx=12)
        self.nav = tk.Frame(mitte, bg=r["card"], width=170)
        self.nav.pack(side="left", fill="y")
        self.nav.pack_propagate(False)
        self.grid_canvas = tk.Canvas(mitte, bg=r["card"], highlightthickness=0)
        self.grid_canvas.pack(side="left", fill="both", expand=True, padx=(8, 0))
        self.grid = tk.Frame(self.grid_canvas, bg=r["card"])
        self.grid_canvas.create_window(0, 0, window=self.grid, anchor="nw")
        self.grid.bind("<Configure>", lambda _e: self.grid_canvas.configure(scrollregion=self.grid_canvas.bbox("all")))
        self.preview = tk.Frame(mitte, bg=r["card"], width=190)
        self.preview.pack(side="left", fill="y", padx=(8, 0))
        self.preview.pack_propagate(False)
        fuss = tk.Frame(self.dialog, bg=r["bg"])
        fuss.pack(fill="x", padx=12, pady=12)
        for label, callback in self.extra_actions:
            ShellButton(fuss, label, lambda cb=callback: self._extra(cb), r, size="small").pack(side="left", padx=(0, 6))
        ShellButton(fuss, self.texts["choose"], lambda: self.choose(self.selected), r, variant="primary").pack(side="right")
        ShellButton(fuss, self.texts["cancel"], self.close, r).pack(side="right", padx=(0, 8))
        for sequence, handler in (("<Escape>", lambda _e: self.close()), ("<Return>", lambda _e: self.choose(self.selected)),
                                  ("<Left>", lambda _e: self.move(-1)), ("<Right>", lambda _e: self.move(1)),
                                  ("<Up>", lambda _e: self.move(-self.columns)), ("<Down>", lambda _e: self.move(self.columns)),
                                  ("<Control-f>", lambda _e: self.search.focus_entry()), ("<KeyPress-f>", self._fav_key)):
            self.dialog.bind(sequence, handler)
        self.build_nav()
        self.fill()

    # --- Navigation -------------------------------------------------------------
    def build_nav(self):
        for kind in self.nav.winfo_children():
            kind.destroy()
        eintraege = [(ALL, self.texts["all"])]
        if self.state is not None:
            eintraege += [(FAVORITES, self.texts["favorites"]), (RECENT, self.texts["recent"])]
        eintraege += [(c, c) for c in self.registry.categories()]
        self.nav_buttons = {}
        for key, label in eintraege:
            knopf = ShellButton(self.nav, label, lambda k=key: self.set_category(k), self.roles,
                                variant="primary" if key == self.category else "quiet", size="small", width=154)
            knopf.pack(padx=8, pady=1, anchor="w")
            self.nav_buttons[key] = knopf

    def set_category(self, key):
        self.category = key
        self.build_nav()
        self.fill()

    def visible(self):
        query = self.search.get()
        if self.category == FAVORITES and self.state is not None:
            symbole = [self.registry.get(i) for i in self.state.favorites]
        elif self.category == RECENT and self.state is not None:
            symbole = [self.registry.get(i) for i in self.state.recent]
        elif self.category == ALL:
            symbole = self.registry.symbols()
        else:
            symbole = self.registry.symbols(self.category)
        return [s for s in symbole if s is not None and s.matches(query)]

    # --- Raster -----------------------------------------------------------------
    def image_for(self, symbol):
        schluessel = (symbol.id, self.size, self.roles.get("text"), self.roles.get("card"))
        bild = self.cache.get(schluessel)
        if bild is None:
            try:
                bild = self.render(symbol, self.size, self.roles)
            except Exception:  # noqa: BLE001 – a broken resource shows the text fallback
                bild = None
            if bild is not None:
                self.cache.put(schluessel, bild)
        return bild

    def fill(self):
        for kind in self.grid.winfo_children():
            kind.destroy()
        self.cells = {}
        self.order = []
        symbole = self.visible()
        if not symbole:
            tk.Label(self.grid, text=self.texts["empty"], bg=self.roles["card"], fg=self.roles["muted"],
                     font=_font(self.grid, None, 10)).grid(row=0, column=0, padx=12, pady=12)
        for index, symbol in enumerate(symbole):
            bild = self.image_for(symbol)
            zelle = tk.Label(self.grid, bg=self.roles["card"], fg=self.roles["text"], width=self.size + 12 if bild else 4,
                             height=self.size + 12 if bild else 2, cursor="hand2", takefocus=0,
                             highlightthickness=2, highlightbackground=self.roles["card"])
            if bild is not None:
                zelle.configure(image=bild, width=self.size + 12, height=self.size + 12)
                zelle.image = bild
            else:
                zelle.configure(text=symbol.label[:3])
            zelle.grid(row=index // self.columns, column=index % self.columns, padx=2, pady=2)
            zelle.bind("<Button-1>", lambda _e, s=symbol.id: self.select(s))
            zelle.bind("<Double-Button-1>", lambda _e, s=symbol.id: self.choose(s))
            self.cells[symbol.id] = zelle
            self.order.append(symbol.id)
        if self.selected not in self.cells:
            self.selected = self.order[0] if self.order else None
        self.select(self.selected)

    def select(self, symbol_id):
        for sid, zelle in self.cells.items():
            zelle.configure(highlightbackground=self.roles["focus"] if sid == symbol_id else self.roles["card"])
        self.selected = symbol_id
        self.show_preview()

    def move(self, step):
        if not self.order:
            return "break"
        index = self.order.index(self.selected) if self.selected in self.order else 0
        self.select(self.order[max(0, min(len(self.order) - 1, index + step))])
        return "break"

    def show_preview(self):
        for kind in self.preview.winfo_children():
            kind.destroy()
        symbol = self.registry.get(self.selected) if self.selected else None
        if symbol is None:
            return
        r = self.roles
        bild = None
        try:
            bild = self.render(symbol, self.size * 2, r)
        except Exception:  # noqa: BLE001
            bild = None
        gross = tk.Label(self.preview, bg=r["card"], fg=r["text"], text="" if bild else symbol.label[:3])
        if bild is not None:
            gross.configure(image=bild)
            gross.image = bild
        gross.pack(pady=(12, 6))
        for text, farbe in ((symbol.label, "text"), (f"{self.texts['category']}: {symbol.category}", "muted"),
                            (f"{self.texts['origin']}: {symbol.origin}", "muted"),
                            (f"{self.texts['license']}: {symbol.license or '—'}", "muted")):
            tk.Label(self.preview, text=text, bg=r["card"], fg=r[farbe], wraplength=170, justify="left",
                     anchor="w", font=_font(self.preview, None, 9)).pack(fill="x", padx=8)
        if self.state is not None:
            fav = symbol.id in self.state.favorites
            ShellButton(self.preview, self.texts["unfavorite" if fav else "favorite"], self.toggle_favorite, r,
                        size="small").pack(pady=10)

    def toggle_favorite(self):
        if self.state is not None and self.selected:
            self.state.toggle_favorite(self.selected)
            if self.category == FAVORITES:
                self.fill()
            else:
                self.show_preview()

    def _fav_key(self, event):
        if event.widget is self.search.entry:
            return None
        self.toggle_favorite()
        return "break"

    def _extra(self, callback):
        if callback():
            self.registry.refresh()
            self.build_nav()
            self.fill()

    # --- Ergebnis -----------------------------------------------------------------
    def choose(self, symbol_id):
        if symbol_id is None or self.registry.get(symbol_id) is None:
            return None
        self.result = symbol_id
        if self.state is not None:
            self.state.used(symbol_id)
        self.close()
        return symbol_id

    def close(self):
        try:
            window_lifetime.scope_for(self.dialog).close()
            self.dialog.destroy()
        except tk.TclError:
            pass

    def run(self):
        """Modal warten; ein bereits geschlossener Dialog (Auswahl vor dem Warten) liefert sein Ergebnis."""
        try:
            if self.dialog.winfo_exists():
                modal_session.run_modal(self.master.winfo_toplevel(), self.dialog, self.master)
        except tk.TclError:
            if self.dialog_alive():
                raise
        return self.result

    def dialog_alive(self):
        try:
            return bool(self.dialog.winfo_exists())
        except tk.TclError:
            return False
