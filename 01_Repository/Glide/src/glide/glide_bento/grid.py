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
        self._last_signature: tuple | None = None
        self.layout_runs = 0

        self._build_scaffolding()
        bind_resize(self, self._on_resize)

    def _build_scaffolding(self) -> None:
        """Erzeugt den Bandrahmen (``_header_frame`` bleibt für 0.1.0-Aufrufer leer erhalten)."""
        bg = self.context.resolve_color("canvas_bg")
        self._header_frame = tk.Frame(self, bg=bg, bd=0, highlightthickness=0)
        self._header_frame.pack(side="top", fill="x")

        self._columns_frame = tk.Frame(self, bg=bg, bd=0, highlightthickness=0)
        self._columns_frame.pack(side="top", fill="both", expand=True)

    def add_card(self, widget: tk.Widget, spec: BentoCardSpec | None = None) -> None:
        """Fügt eine Karte oder ein Widget mit Spezifikation zum Raster hinzu."""
        card_spec = spec or getattr(widget, "spec", None) or BentoCardSpec(key=f"card_{len(self._cards)}")
        self._cards = [item for item in self._cards if item[0].key != card_spec.key]
        self._cards.append((card_spec, widget))
        self._last_signature = None
        # Re-Layout anfordern
        self.schedule_layout()

    def remove_card(self, key: str) -> None:
        """Entfernt eine Karte anhand ihres Schlüssels."""
        self._cards = [item for item in self._cards if item[0].key != key]
        self._last_signature = None
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
        """Baut alle Band- und Bahnrahmen ab."""
        for frame in self._column_frames:
            try:
                frame.destroy()
            except tk.TclError:
                pass
        self._column_frames.clear()
        self._last_signature = None

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
        self._pending_after = self.after_idle(self._execute_layout)

    def destroy(self) -> None:
        """Ausstehende Layoutaufträge freigeben, dann abbauen (keine verwaisten after-Rückrufe)."""
        pending = getattr(self, "_pending_after", None)
        if pending is not None:
            try:
                self.after_cancel(pending)
            except tk.TclError:
                pass
            self._pending_after = None
        self._layout_active = False
        super().destroy()

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
        """Führt den Layout-Planner aus und platziert Widgets im Bandmodell (0.2.0).

        Kartenwidgets bleiben erhalten (Render-Retention): Bei geändertem Plan
        werden nur Band- und Bahnrahmen neu angelegt und die vorhandenen
        Karten per ``pack(in_=…)`` umgehängt. Ein unveränderter Plan löst
        keine Geometrieänderung aus, damit Configure-Ereignisse nicht
        kaskadieren (Lehre aus dem Xvfb-Livelock, D-Regel 12).
        """
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
        widgets_by_key = {}
        for spec, widget in self._cards:
            widgets_by_key.setdefault(spec.key, widget)

        plan = self.planner.plan(available_w, specs, self.grid_spec)
        signature = (plan.column_count, plan.placements(), tuple(sorted(widgets_by_key)))
        if signature == self._last_signature and self._column_frames:
            self._last_plan = plan
            return
        self._last_signature = signature
        self._last_plan = plan
        self.layout_runs += 1

        if not self._columns_frame:
            return
        bg = self.context.resolve_color("canvas_bg")
        gap = plan.gap
        card_gap = self.context.tokens.gap_default

        # Karten lösen, alte Band-/Bahnrahmen abbauen (Karten gehören dem Raster)
        for widget in widgets_by_key.values():
            try:
                if widget.winfo_manager():
                    widget.pack_forget()
            except tk.TclError:
                pass
        for frame in self._column_frames:
            try:
                frame.destroy()
            except tk.TclError:
                pass
        self._column_frames.clear()

        for band_index, band in enumerate(plan.bands):
            band_frame = tk.Frame(self._columns_frame, bg=bg, bd=0, highlightthickness=0)
            band_frame.pack(side="top", fill="x")
            for idx in range(plan.column_count):
                band_frame.columnconfigure(idx, weight=1, uniform="bento_columns")
            self._column_frames.append(band_frame)
            for lane in band.lanes:
                lane_frame = tk.Frame(band_frame, bg=bg, bd=0, highlightthickness=0)
                pad_left = 0 if lane.column == 0 else gap
                lane_frame.grid(row=0, column=lane.column, columnspan=lane.span,
                                sticky="new", padx=(pad_left, 0))
                lane_frame.bento_lane = lane
                for card_spec in lane.cards:
                    widget = widgets_by_key.get(card_spec.key)
                    if widget is None:
                        continue
                    widget.pack(in_=lane_frame, side="top", fill="x", pady=(0, card_gap))
                    # Fensterstapel: Canvas überschreibt lift() mit tag_raise
                    widget.tk.call("raise", str(widget))

    def update_theme(self, context: BentoContext) -> None:
        """Aktualisiert Theme für Raster und alle enthaltenen BentoCards."""
        self.context = context
        self.planner = BentoLayoutPlanner(context.tokens)
        self._last_signature = None
        bg = context.resolve_color("canvas_bg")
        self.configure(bg=bg)
        if self._header_frame:
            self._header_frame.configure(bg=bg)
        if self._columns_frame:
            self._columns_frame.configure(bg=bg)
        for col in self._column_frames:
            col.configure(bg=bg)
            for lane_frame in col.winfo_children():
                lane_frame.configure(bg=bg)

        for _spec, widget in self._cards:
            if isinstance(widget, BentoCard):
                widget.set_theme(context)
        self.schedule_layout()
