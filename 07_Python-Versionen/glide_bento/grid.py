# SPDX-License-Identifier: MPL-2.0
"""BentoGrid – responsiver Raster-Container für Bento-Karten.

Rendert Karten anhand des vom BentoLayoutPlanner berechneten Plans in
deterministische Spalten unter Verwendung von Tkinter-Frames (D100, D102).
"""
import tkinter as tk
from typing import Any, Callable

from glide_shell.custom_controls import bind_resize
from .card import BentoCard
from .context import BentoContext
from .layout import BentoLayoutPlanner
from .specs import BentoCardSpec, BentoGridSpec, BentoLayoutPlan


class BentoGrid(tk.Frame):
    """Adaptiver Raster-Container für Bento-Karten."""

    def __init__(
        self,
        master: tk.Widget,
        context: BentoContext | None = None,
        spec: BentoGridSpec | None = None,
        **kwargs,
    ):
        self.context = context or BentoContext()
        self.grid_spec = spec or BentoGridSpec()
        self.planner = BentoLayoutPlanner(self.context.tokens)

        bg = self.context.resolve_color("canvas_bg")
        super().__init__(master, bg=bg, bd=0, highlightthickness=0, **kwargs)

        self._cards: list[tuple[BentoCardSpec, tk.Widget]] = []
        self._header_frame: tk.Frame | None = None
        self._columns_frame: tk.Frame | None = None
        self._column_frames: list[tk.Frame] = []
        self._last_width: int = 0
        self._last_plan: BentoLayoutPlan | None = None
        self._layout_active = False

        self._build_scaffolding()
        bind_resize(self, self._on_resize)

    def _build_scaffolding(self) -> None:
        """Erzeugt Kopf- und Spalten-Rahmen."""
        bg = self.context.resolve_color("canvas_bg")
        self._header_frame = tk.Frame(self, bg=bg, bd=0, highlightthickness=0)
        self._header_frame.pack(side="top", fill="x")

        self._columns_frame = tk.Frame(self, bg=bg, bd=0, highlightthickness=0)
        self._columns_frame.pack(side="top", fill="both", expand=True)

    def add_card(self, widget: tk.Widget, spec: BentoCardSpec | None = None) -> None:
        """Fügt eine Karte oder ein Widget mit Spezifikation zum Raster hinzu."""
        card_spec = spec or getattr(widget, "spec", None) or BentoCardSpec(key=f"card_{len(self._cards)}")
        self._cards.append((card_spec, widget))
        # Re-Layout anfordern
        self.schedule_layout()

    def remove_card(self, key: str) -> None:
        """Entfernt eine Karte anhand ihres Schlüssels."""
        self._cards = [item for item in self._cards if item[0].key != key]
        self.schedule_layout()

    def clear(self) -> None:
        """Leert alle Karten aus dem Raster."""
        for _spec, widget in self._cards:
            try:
                widget.destroy()
            except tk.TclError:
                pass
        self._cards.clear()
        self._clear_dom()

    def _clear_dom(self) -> None:
        """Entfernt alle Platzierungen aus den Unterrahmen."""
        if self._header_frame:
            for child in self._header_frame.winfo_children():
                child.pack_forget()
        if self._columns_frame:
            for child in self._columns_frame.winfo_children():
                child.grid_forget()
        self._column_frames.clear()

    @property
    def current_columns(self) -> int:
        """Aktuelle Spaltenanzahl des zuletzt ausgeführten Layoutplans."""
        return self._last_plan.column_count if self._last_plan else 1

    def reflow(self) -> None:
        """Führt eine sofortige synchrone Neuberechnung und Platzierung aus."""
        self._execute_layout()

    def schedule_layout(self) -> None:
        """Plant eine Neuberechnung des Rasters ein."""
        if self._layout_active:
            return
        self._layout_active = True
        self.after_idle(self._execute_layout)

    def _on_resize(self, _event=None) -> None:
        """Reagiert auf Größenänderungen des Rasters."""
        w = self.winfo_width()
        if w <= 1:
            return
        # Entprellung: wenn Breite identisch, überspringen
        if abs(w - self._last_width) < 4:
            return
        self._last_width = w
        self.schedule_layout()

    def _execute_layout(self) -> None:
        """Führt den Layout-Planner aus und platziert Widgets in den Spalten."""
        self._layout_active = False
        try:
            available_w = self.winfo_width()
            if available_w <= 1:
                available_w = self.winfo_reqwidth()
        except tk.TclError:
            return

        if available_w <= 1:
            available_w = self.context.tokens.card_min_width

        specs = [item[0] for item in self._cards]
        widgets_by_key = {item[0].key: item[1] for item in self._cards}

        plan = self.planner.plan(available_w, specs, self.grid_spec)
        self._last_plan = plan

        # 1. Kopfbereich (Vollbreitenkarten)
        if self._header_frame:
            for card_spec in plan.header_cards:
                widget = widgets_by_key.get(card_spec.key)
                if widget and widget.winfo_manager() != "pack":
                    widget.pack(in_=self._header_frame, side="top", fill="x", pady=(0, self.context.tokens.gap_default))

        # 2. Spaltenrahmen aufbauen
        if not self._columns_frame:
            return

        # Spaltenanzahl angleichen
        current_cols = len(self._column_frames)
        bg = self.context.resolve_color("canvas_bg")
        gap = plan.gap

        if current_cols != plan.column_count:
            # Alte Spalten leeren
            for col in self._column_frames:
                for child in col.winfo_children():
                    child.pack_forget()
                col.grid_forget()
                col.destroy()
            self._column_frames.clear()

            # Neue Spalten erzeugen
            for idx in range(plan.column_count):
                col_frame = tk.Frame(self._columns_frame, bg=bg, bd=0, highlightthickness=0)
                pad_left = 0 if idx == 0 else gap
                col_frame.grid(row=0, column=idx, sticky="new", padx=(pad_left, 0))
                self._columns_frame.columnconfigure(idx, weight=1, uniform="bento_columns")
                self._column_frames.append(col_frame)
        else:
            # Bestehende Spalten von alten Karten lösen
            for col in self._column_frames:
                for child in col.winfo_children():
                    child.pack_forget()

        # 3. Karten in die Spalten packen
        for col_idx, col_cards in enumerate(plan.columns):
            if col_idx >= len(self._column_frames):
                break
            target_col = self._column_frames[col_idx]
            for card_spec in col_cards:
                widget = widgets_by_key.get(card_spec.key)
                if widget:
                    widget.pack(in_=target_col, side="top", fill="x", pady=(0, self.context.tokens.gap_default))

    def update_theme(self, context: BentoContext) -> None:
        """Aktualisiert Theme für Raster und alle enthaltenen BentoCards."""
        self.context = context
        bg = context.resolve_color("canvas_bg")
        self.configure(bg=bg)
        if self._header_frame:
            self._header_frame.configure(bg=bg)
        if self._columns_frame:
            self._columns_frame.configure(bg=bg)
        for col in self._column_frames:
            col.configure(bg=bg)

        for _spec, widget in self._cards:
            if isinstance(widget, BentoCard):
                widget.set_theme(context)
        self.schedule_layout()
