# SPDX-License-Identifier: MPL-2.0
"""Bento visualisations on a Tk canvas (Bento 0.4.0).

All charts share `BentoChart`: colours from the Bento context (theme roles of
the host, including its brand accent), a series palette derived from those
roles, coalesced redraw on resize (one redraw per idle cycle through the
widget's `AfterScope`, no Configure cascade), hover with an in-canvas tooltip,
selection with `on_select(element_id)`, keyboard navigation (Left/Right or
Up/Down move, Return selects, Escape clears) and a visible focus ring.
Data comes as `glide_bento.data` contracts; missing values are drawn as gaps
or left out and are never treated as zero.

Charts: `BarChart` (vertical/horizontal; single, grouped, stacked),
`LineChart` (multi-series, area, zoom with the mouse wheel and pan by
dragging, `reset_view()`), `ScatterChart`, `PieChart` (pie or donut),
`Sparkline`, `Heatmap`, `CalendarHeatmap`, `ProgressBar` (linear, segmented,
target), `RadialProgress` (full or semicircle), `MultiProgress`, `Timeline`
(spans, milestones, lanes; Gantt-like), `GraphChart` (trees and directed
graphs from `layer_layout`), `RadarChart`, `BentoTable` (compact, sortable,
selectable), `Badge`, `StatusDot`, `MetricTrend` (value, change, target and
sparkline).

Each chart exposes `elements()` – the stable ids it draws – and
`redraws` for tests; `set_data(...)` replaces data and redraws once; `update_theme(context)`
recolours without rebuilding the widget.
"""
from __future__ import annotations

import math
import tkinter as tk

from glide_shell import color_roles, window_lifetime

from . import data as bd
from .context import BentoContext


def _mix(a, b, share):
    try:
        ra, rb = color_roles._rgb(a), color_roles._rgb(b)
    except ValueError:
        return a
    return "#" + "".join(f"{round(x + (y - x) * share):02X}" for x, y in zip(ra, rb))


def _readable(fill):
    try:
        return "#FFFFFF" if color_roles.contrast_ratio(fill, "#FFFFFF") >= color_roles.contrast_ratio(fill, "#000000") else "#000000"
    except ValueError:
        return "#000000"


class BentoChart(tk.Canvas):
    min_size = (120, 80)

    def __init__(self, master, context=None, height=200, on_select=None, title=None, **kwargs):
        self.context = context or BentoContext()
        kwargs.setdefault("takefocus", 1)
        super().__init__(master, height=height, highlightthickness=0, bd=0,
                         bg=self.context.resolve_color("card_bg"), **kwargs)
        self.on_select = on_select
        self.title = title
        self.selected = None
        self.hovered = None
        self.redraws = 0
        self._order = []
        self._pending = None
        self._focused = False
        self.scope = window_lifetime.scope_for(self)
        self.bind("<Configure>", lambda _e: self.schedule_draw(), add="+")
        self.bind("<Motion>", self._motion, add="+")
        self.bind("<Leave>", lambda _e: self._hover(None), add="+")
        self.bind("<Button-1>", self._click, add="+")
        for key, step in (("<Left>", -1), ("<Up>", -1), ("<Right>", 1), ("<Down>", 1)):
            self.bind(key, lambda _e, s=step: self.move_selection(s), add="+")
        self.bind("<Return>", lambda _e: self.select(self.selected), add="+")
        self.bind("<Escape>", lambda _e: self.select(None, notify=False), add="+")
        self.bind("<FocusIn>", lambda _e: self._focus(True), add="+")
        self.bind("<FocusOut>", lambda _e: self._focus(False), add="+")

    # --- Farben ------------------------------------------------------------------
    def color(self, role):
        return self.context.resolve_color(role)

    def palette(self, count):
        basis = [self.color(r) for r in ("accent", "confirm", "warning", "danger", "text_secondary")]
        card = self.color("card_bg")
        farben = []
        for i in range(max(1, count)):
            farbe = basis[i % len(basis)]
            runde = i // len(basis)
            farben.append(_mix(farbe, card, min(0.6, 0.3 * runde)) if runde else farbe)
        return farben

    def font(self, size=9, weight="normal"):
        return self.context.resolve_font(size, weight)

    def update_theme(self, context):
        self.context = context
        self.configure(bg=self.color("card_bg"))
        self.draw()

    # --- Zeichnen ------------------------------------------------------------------
    def schedule_draw(self):
        if self._pending is None and not self.scope.closed:
            self._pending = self.scope.after_idle(self._scheduled)

    def _scheduled(self):
        self._pending = None
        self.draw()

    def size(self):
        try:
            w, h = self.winfo_width(), self.winfo_height()
        except tk.TclError:
            return None
        if w <= 1:
            w = self.winfo_reqwidth()
        if h <= 1:
            h = self.winfo_reqheight()
        return max(w, self.min_size[0]), max(h, self.min_size[1])

    def draw(self):
        abmessung = self.size()
        if abmessung is None:
            return
        self.redraws += 1
        self.delete("all")
        self._order = []
        w, h = abmessung
        top = 4
        if self.title:
            self.create_text(8, 6, text=self.title, anchor="nw", fill=self.color("text_primary"), font=self.font(10, "bold"))
            top = 24
        self.render(8, top, w - 8, h - 6)
        if self._focused:
            self.create_rectangle(1, 1, w - 2, h - 2, outline=self.color("focus"), width=2, tags=("focusring",))
        self._decorate()

    def render(self, x0, y0, x1, y1):
        raise NotImplementedError

    def empty(self, x0, y0, x1, y1, text="No data"):
        self.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=text, fill=self.color("text_muted"), font=self.font(9))

    def element(self, item, element_id, label):
        """Register a drawn item as interactive element `element_id` with tooltip `label`."""
        self.addtag_withtag(f"el:{element_id}", item)
        self.addtag_withtag("element", item)
        if element_id not in self._order:
            self._order.append(element_id)
        self._labels = getattr(self, "_labels", {})
        self._labels[element_id] = label

    def elements(self):
        return list(self._order)

    def _decorate(self):
        for eid in self._order:
            if eid == self.selected:
                for item in self.find_withtag(f"el:{eid}"):
                    self._outline(item, self.color("focus"), 3)
            elif eid == self.hovered:
                for item in self.find_withtag(f"el:{eid}"):
                    self._outline(item, self.color("text_primary"), 2)
        if self.hovered and self.hovered in getattr(self, "_labels", {}):
            self._tooltip(self._labels[self.hovered])

    def _outline(self, item, colour, width):
        typ = self.type(item)
        try:
            if typ in ("rectangle", "oval", "polygon", "arc"):
                self.itemconfigure(item, outline=colour, width=width)
            elif typ == "line":
                self.itemconfigure(item, width=width + 1)
        except tk.TclError:
            pass

    def _tooltip(self, text):
        self.delete("tooltip")
        w, _h = self.size()
        item = self.create_text(w - 10, 8, text=text, anchor="ne", fill=self.color("card_bg"), font=self.font(9),
                                tags=("tooltip",))
        x0, y0, x1, y1 = self.bbox(item)
        hinter = self.create_rectangle(x0 - 6, y0 - 3, x1 + 6, y1 + 3, fill=self.color("text_primary"), outline="",
                                       tags=("tooltip",))
        self.tag_lower(hinter, item)

    # --- Interaktion -----------------------------------------------------------------
    def element_at(self, x, y):
        for item in reversed(self.find_overlapping(x - 1, y - 1, x + 1, y + 1)):
            for tag in self.gettags(item):
                if tag.startswith("el:"):
                    return tag[3:]
        return None

    def _motion(self, event):
        self._hover(self.element_at(event.x, event.y))

    def _hover(self, element_id):
        if element_id != self.hovered:
            self.hovered = element_id
            self.draw()

    def _click(self, event):
        self.focus_set()
        self.select(self.element_at(event.x, event.y))

    def select(self, element_id, notify=True):
        self.selected = element_id
        self.draw()
        if notify and element_id is not None and callable(self.on_select):
            self.on_select(element_id)
        return "break"

    def move_selection(self, step):
        if not self._order:
            return "break"
        index = self._order.index(self.selected) if self.selected in self._order else (-1 if step > 0 else 0)
        self.selected = self._order[(index + step) % len(self._order)]
        self.hovered = self.selected
        self.draw()
        return "break"

    def _focus(self, flag):
        self._focused = flag
        self.draw()

    # --- Achsen ----------------------------------------------------------------------
    def value_axis(self, low, high, x0, y0, x1, y1, horizontal=False, unit=""):
        ticks = bd.nice_ticks(low, high, 5)
        low, high = ticks[0], ticks[-1]
        muted, line = self.color("text_muted"), self.color("line")
        for t in ticks:
            if horizontal:
                x = x0 + bd.scale(t, low, high, x1 - x0)
                self.create_line(x, y0, x, y1, fill=line)
                self.create_text(x, y1 + 2, text=bd.format_value(t, unit), anchor="n", fill=muted, font=self.font(8))
            else:
                y = y1 - bd.scale(t, low, high, y1 - y0)
                self.create_line(x0, y, x1, y, fill=line)
                self.create_text(x0 - 4, y, text=bd.format_value(t, unit), anchor="e", fill=muted, font=self.font(8))
        return low, high


def _clip(text, n=14):
    text = str(text)
    return text if len(text) <= n else text[: n - 1] + "…"


class BarChart(BentoChart):
    def __init__(self, master, series_list, orientation="vertical", mode="grouped", unit="", **kwargs):
        self.series_list, self.orientation, self.mode, self.unit = list(series_list), orientation, mode, unit
        super().__init__(master, **kwargs)

    def set_data(self, series_list):
        self.series_list = list(series_list)
        self.draw()

    def render(self, x0, y0, x1, y1):
        reihen = self.series_list
        ext = bd.extent(reihen, stacked=self.mode == "stacked")
        if ext is None:
            return self.empty(x0, y0, x1, y1)
        horizontal = self.orientation == "horizontal"
        labels = [p.label for p in reihen[0].points] if reihen else []
        if horizontal:
            x0 += 90
            y1 -= 14
            low, high = self.value_axis(*ext, x0, y0, x1, y1, horizontal=True, unit=self.unit)
        else:
            x0 += 40
            y1 -= 16
            low, high = self.value_axis(*ext, x0, y0, x1, y1, unit=self.unit)
        farben = self.palette(len(reihen))
        n = max(1, len(labels))
        laenge = (y1 - y0) if horizontal else (x1 - x0)
        band = laenge / n
        for i, label in enumerate(labels):
            start = (y0 if horizontal else x0) + i * band
            if horizontal:
                self.create_text(x0 - 6, start + band / 2, text=_clip(label), anchor="e", fill=self.color("text_secondary"), font=self.font(8))
            else:
                self.create_text(start + band / 2, y1 + 2, text=_clip(label, max(4, int(band / 7))), anchor="n",
                                 fill=self.color("text_secondary"), font=self.font(8))
            plus = minus = 0.0
            for s_index, reihe in enumerate(reihen):
                if i >= len(reihe.points):
                    continue
                punkt = reihe.points[i]
                wert = punkt.number
                if wert is None:
                    continue
                if self.mode == "stacked":
                    basis = plus if wert >= 0 else minus
                    a, b = basis, basis + wert
                    if wert >= 0:
                        plus += wert
                    else:
                        minus += wert
                    breite, versatz = band * 0.7, band * 0.15
                else:
                    a, b = 0.0, wert
                    breite = band * 0.8 / max(1, len(reihen))
                    versatz = band * 0.1 + s_index * breite
                pa, pb = bd.scale(max(min(a, high), low), low, high, (x1 - x0) if horizontal else (y1 - y0)), \
                    bd.scale(max(min(b, high), low), low, high, (x1 - x0) if horizontal else (y1 - y0))
                farbe = punkt.color or reihe.color or farben[s_index]
                if horizontal:
                    item = self.create_rectangle(x0 + min(pa, pb), start + versatz, x0 + max(pa, pb), start + versatz + breite,
                                                 fill=farbe, outline="")
                else:
                    item = self.create_rectangle(start + versatz, y1 - max(pa, pb), start + versatz + breite, y1 - min(pa, pb),
                                                 fill=farbe, outline="")
                self.element(item, punkt.id, f"{reihe.label} · {punkt.label}: {bd.format_value(wert, self.unit)}")


class LineChart(BentoChart):
    def __init__(self, master, series_list, area=False, markers=True, unit="", **kwargs):
        self.series_list, self.area, self.markers, self.unit = list(series_list), area, markers, unit
        self.view = None  # (first index, last index) when zoomed
        self._drag = None
        super().__init__(master, **kwargs)
        self.bind("<MouseWheel>", self._wheel, add="+")
        self.bind("<Button-4>", lambda e: self._zoom(+1, e.x), add="+")
        self.bind("<Button-5>", lambda e: self._zoom(-1, e.x), add="+")
        self.bind("<B1-Motion>", self._pan, add="+")
        self.bind("<ButtonRelease-1>", lambda _e: setattr(self, "_drag", None), add="+")

    def set_data(self, series_list):
        self.series_list = list(series_list)
        self.view = None
        self.draw()

    def count(self):
        return max((len(s.points) for s in self.series_list), default=0)

    def window(self):
        n = self.count()
        return self.view if self.view else (0, max(0, n - 1))

    def _wheel(self, event):
        self._zoom(1 if event.delta > 0 else -1, event.x)

    def _zoom(self, direction, x):
        n = self.count()
        if n < 4:
            return "break"
        a, b = self.window()
        breite = b - a
        neu = max(3, int(breite * (0.7 if direction > 0 else 1.4)))
        w, _ = self.size()
        mitte = a + breite * min(1, max(0, (x - 48) / max(1, w - 56)))
        a = int(round(mitte - neu / 2))
        a = max(0, min(a, n - 1 - neu))
        b = min(n - 1, a + neu)
        self.view = None if (a, b) == (0, n - 1) else (a, b)
        self.draw()
        return "break"

    def _pan(self, event):
        if self.view is None:
            return
        if self._drag is None:
            self._drag = event.x
            return
        a, b = self.view
        w, _ = self.size()
        schritt = int(round((self._drag - event.x) / max(1, (w - 56) / max(1, b - a))))
        if schritt:
            n = self.count()
            schritt = max(-a, min(schritt, n - 1 - b))
            self.view = (a + schritt, b + schritt)
            self._drag = event.x
            self.draw()

    def reset_view(self):
        self.view = None
        self.draw()

    def render(self, x0, y0, x1, y1):
        a, b = self.window()
        sicht = [bd.Series(s.id, s.label, s.points[a:b + 1], s.unit, s.color) for s in self.series_list]
        ext = bd.extent(sicht, include_zero=self.area)
        if ext is None:
            return self.empty(x0, y0, x1, y1)
        x0 += 40
        y1 -= 16
        low, high = self.value_axis(*ext, x0, y0, x1, y1, unit=self.unit)
        farben = self.palette(len(sicht))
        n = max(2, max(len(s.points) for s in sicht))
        dx = (x1 - x0) / (n - 1)
        if sicht and sicht[0].points:
            for i, p in enumerate(sicht[0].points):
                if n <= 12 or i % max(1, n // 8) == 0:
                    self.create_text(x0 + i * dx, y1 + 2, text=_clip(p.label, 8), anchor="n", fill=self.color("text_muted"), font=self.font(8))
        for s_index, reihe in enumerate(sicht):
            farbe = reihe.color or farben[s_index]
            abschnitt = []
            abschnitte = []
            for i, p in enumerate(reihe.points):
                if p.number is None:
                    if abschnitt:
                        abschnitte.append(abschnitt)
                    abschnitt = []
                    continue
                abschnitt.append((x0 + i * dx, y1 - bd.scale(p.number, low, high, y1 - y0), p))
            if abschnitt:
                abschnitte.append(abschnitt)
            for teil in abschnitte:
                koordinaten = [c for x, y, _p in teil for c in (x, y)]
                if self.area and len(teil) > 1:
                    null = y1 - bd.scale(max(low, min(0.0, high)), low, high, y1 - y0)
                    self.create_polygon(teil[0][0], null, *koordinaten, teil[-1][0], null,
                                        fill=_mix(farbe, self.color("card_bg"), 0.7), outline="")
                if len(teil) > 1:
                    self.create_line(*koordinaten, fill=farbe, width=2)
                for x, y, p in teil:
                    if self.markers or len(teil) == 1:
                        item = self.create_oval(x - 3, y - 3, x + 3, y + 3, fill=farbe, outline=farbe)
                        self.element(item, p.id, f"{reihe.label} · {p.label}: {bd.format_value(p.number, self.unit)}")


class ScatterChart(BentoChart):
    """Points use `time` as x and `value` as y."""

    def __init__(self, master, series_list, **kwargs):
        self.series_list = list(series_list)
        super().__init__(master, **kwargs)

    def render(self, x0, y0, x1, y1):
        punkte = [(s, p) for s in self.series_list for p in s.points if p.number is not None and bd._number(p.time) is not None]
        if not punkte:
            return self.empty(x0, y0, x1, y1)
        xs = [p.time for _s, p in punkte]
        ext = bd.extent(self.series_list, include_zero=False)
        x0 += 40
        y1 -= 16
        low, high = self.value_axis(*ext, x0, y0, x1, y1)
        xl, xh = min(xs), max(xs)
        if xl == xh:
            xl, xh = xl - 1, xh + 1
        farben = self.palette(len(self.series_list))
        for s, p in punkte:
            x = x0 + bd.scale(p.time, xl, xh, x1 - x0)
            y = y1 - bd.scale(p.number, low, high, y1 - y0)
            farbe = p.color or s.color or farben[self.series_list.index(s)]
            item = self.create_oval(x - 4, y - 4, x + 4, y + 4, fill=farbe, outline="")
            self.element(item, p.id, f"{p.label}: {bd.format_value(p.time)} / {bd.format_value(p.number)}")


class PieChart(BentoChart):
    def __init__(self, master, series, donut=False, unit="", **kwargs):
        self.series, self.donut, self.unit = series, donut, unit
        super().__init__(master, **kwargs)

    def set_data(self, series):
        self.series = series
        self.draw()

    def render(self, x0, y0, x1, y1):
        teile = [p for p in self.series.points if p.number is not None and p.number > 0]
        self.excluded = [p.id for p in self.series.points if p.number is None or p.number <= 0]
        gesamt = sum(p.number for p in teile)
        if not gesamt:
            return self.empty(x0, y0, x1, y1)
        d = min(x1 - x0 - 120, y1 - y0)
        cx, cy = x0 + d / 2, (y0 + y1) / 2
        farben = self.palette(len(teile))
        winkel = 90.0
        for i, p in enumerate(teile):
            umfang = 360.0 * p.number / gesamt
            farbe = p.color or farben[i]
            item = self.create_arc(cx - d / 2, cy - d / 2, cx + d / 2, cy + d / 2, start=winkel, extent=-umfang,
                                   fill=farbe, outline=self.color("card_bg"), style="pieslice")
            self.element(item, p.id, f"{p.label}: {bd.format_value(p.number, self.unit)} ({p.number / gesamt:.0%})")
            ly = y0 + 4 + i * 16
            if ly < y1 - 8:
                self.create_rectangle(x0 + d + 12, ly, x0 + d + 22, ly + 10, fill=farbe, outline="")
                self.create_text(x0 + d + 28, ly + 5, text=_clip(p.label, 16), anchor="w", fill=self.color("text_secondary"), font=self.font(8))
            winkel -= umfang
        if self.donut:
            r = d * 0.3
            self.create_oval(cx - r, cy - r, cx + r, cy + r, fill=self.color("card_bg"), outline="")
            self.create_text(cx, cy, text=bd.format_value(gesamt, self.unit), fill=self.color("text_primary"), font=self.font(10, "bold"))


class Sparkline(BentoChart):
    min_size = (40, 16)

    def __init__(self, master, series, height=28, width=120, **kwargs):
        self.series = series
        super().__init__(master, height=height, width=width, takefocus=0, **kwargs)

    def render(self, x0, y0, x1, y1):
        werte = self.series.values()
        gueltig = [v for v in werte if v is not None]
        if not gueltig:
            return
        low, high = min(gueltig), max(gueltig)
        if low == high:
            low, high = low - 1, high + 1
        dx = (x1 - x0) / max(1, len(werte) - 1)
        teil = []
        for i, v in enumerate(werte + [None]):
            if v is None:
                if len(teil) >= 4:
                    self.create_line(*teil, fill=self.color("accent"), width=2)
                elif len(teil) == 2:  # einzelner Wert zwischen Lücken: Punkt statt Linie
                    x, y = teil
                    self.create_oval(x - 2, y - 2, x + 2, y + 2, fill=self.color("accent"), outline="")
                teil = []
                continue
            teil += [x0 + i * dx, y1 - bd.scale(v, low, high, y1 - y0)]


class Heatmap(BentoChart):
    """`cells` maps (row label, column label) to a `Point`; rows and columns keep their order."""

    def __init__(self, master, rows, columns, cells, unit="", **kwargs):
        self.rows, self.columns, self.cells, self.unit = list(rows), list(columns), dict(cells), unit
        super().__init__(master, **kwargs)

    def render(self, x0, y0, x1, y1):
        werte = [p.number for p in self.cells.values() if p.number is not None]
        if not werte or not self.rows or not self.columns:
            return self.empty(x0, y0, x1, y1)
        low, high = min(werte), max(werte)
        links = x0 + 60
        cw = (x1 - links) / len(self.columns)
        ch = (y1 - y0 - 14) / len(self.rows)
        akzent, leer = self.color("accent"), self.color("card_bg")
        for r, zeile in enumerate(self.rows):
            self.create_text(links - 4, y0 + r * ch + ch / 2, text=_clip(zeile, 9), anchor="e", fill=self.color("text_muted"), font=self.font(8))
            for c, spalte in enumerate(self.columns):
                p = self.cells.get((zeile, spalte))
                xa, ya = links + c * cw, y0 + r * ch
                if p is None or p.number is None:
                    item = self.create_rectangle(xa + 1, ya + 1, xa + cw - 1, ya + ch - 1, fill="", outline=self.color("line"), dash=(2, 2))
                    continue
                anteil = 0.15 + 0.85 * ((p.number - low) / (high - low) if high > low else 1.0)
                item = self.create_rectangle(xa + 1, ya + 1, xa + cw - 1, ya + ch - 1, fill=_mix(leer, akzent, anteil), outline="")
                self.element(item, p.id, f"{zeile} · {spalte}: {bd.format_value(p.number, self.unit)}")
        for c, spalte in enumerate(self.columns):
            if len(self.columns) <= 14 or c % max(1, len(self.columns) // 10) == 0:
                self.create_text(links + c * cw + cw / 2, y1 - 2, text=_clip(spalte, 5), anchor="s", fill=self.color("text_muted"), font=self.font(7))


class CalendarHeatmap(Heatmap):
    """`days` maps ISO dates (``YYYY-MM-DD``) to values; weeks are columns, weekdays rows."""

    WEEKDAYS = ("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")

    def __init__(self, master, days, weekdays=None, unit="", **kwargs):
        import datetime as dt
        tage = sorted(days)
        zellen, spalten = {}, []
        namen = tuple(weekdays or self.WEEKDAYS)
        if tage:
            erster = dt.date.fromisoformat(tage[0])
            start = erster - dt.timedelta(days=erster.weekday())
            for iso in tage:
                tag = dt.date.fromisoformat(iso)
                woche = (tag - start).days // 7
                spalte = f"W{woche + 1}"
                if spalte not in spalten:
                    spalten.append(spalte)
                zellen[(namen[tag.weekday()], spalte)] = bd.Point(f"day:{iso}", iso, days[iso])
        super().__init__(master, namen, spalten, zellen, unit=unit, **kwargs)


class ProgressBar(BentoChart):
    min_size = (60, 18)

    def __init__(self, master, value, maximum=1.0, segments=None, target=None, label="", height=34, **kwargs):
        self.value, self.maximum, self.segments, self.target, self.label = value, maximum, segments, target, label
        super().__init__(master, height=height, takefocus=0, **kwargs)

    def set_value(self, value):
        self.value = value
        self.draw()

    def render(self, x0, y0, x1, y1):
        wert = bd._number(self.value)
        mitte = (y0 + y1) / 2 + 4
        self.create_rectangle(x0, mitte - 5, x1, mitte + 5, fill=self.color("line"), outline="")
        text = self.label
        if wert is None or not self.maximum:
            text = (text + " · " if text else "") + "–"
        else:
            anteil = max(0.0, min(1.0, wert / self.maximum))
            if self.segments:
                breite = (x1 - x0) / self.segments
                for i in range(self.segments):
                    if (i + 1) / self.segments <= anteil + 1e-9:
                        self.create_rectangle(x0 + i * breite + 1, mitte - 5, x0 + (i + 1) * breite - 1, mitte + 5,
                                              fill=self.color("accent"), outline="")
            else:
                self.create_rectangle(x0, mitte - 5, x0 + (x1 - x0) * anteil, mitte + 5, fill=self.color("accent"), outline="")
            text = (text + " · " if text else "") + f"{anteil:.0%}"
        if self.target is not None and self.maximum:
            tx = x0 + (x1 - x0) * max(0.0, min(1.0, self.target / self.maximum))
            self.create_line(tx, mitte - 9, tx, mitte + 9, fill=self.color("text_primary"), width=2)
        self.create_text(x0, y0, text=text, anchor="nw", fill=self.color("text_secondary"), font=self.font(8))


class RadialProgress(BentoChart):
    min_size = (60, 40)

    def __init__(self, master, value, maximum=1.0, semicircle=False, label="", height=120, **kwargs):
        self.value, self.maximum, self.semicircle, self.label = value, maximum, semicircle, label
        super().__init__(master, height=height, takefocus=0, **kwargs)

    def render(self, x0, y0, x1, y1):
        wert = bd._number(self.value)
        d = min(x1 - x0, (y1 - y0) * (2 if self.semicircle else 1)) - 8
        cx = (x0 + x1) / 2
        cy = (y1 - 4) if self.semicircle else (y0 + y1) / 2
        box = (cx - d / 2, cy - d / 2, cx + d / 2, cy + d / 2)
        start, umfang = (180, -180) if self.semicircle else (90, -359.9)
        self.create_arc(*box, start=start, extent=umfang, style="arc", outline=self.color("line"), width=10)
        if wert is not None and self.maximum:
            anteil = max(0.0, min(1.0, wert / self.maximum))
            if anteil:
                self.create_arc(*box, start=start, extent=umfang * anteil, style="arc", outline=self.color("accent"), width=10)
            text = f"{anteil:.0%}"
        else:
            text = "–"
        self.create_text(cx, cy - (d / 6 if self.semicircle else 0), text=text, fill=self.color("text_primary"), font=self.font(12, "bold"))
        if self.label:
            self.create_text(cx, y0, text=self.label, anchor="n", fill=self.color("text_muted"), font=self.font(8))


class MultiProgress(BentoChart):
    def __init__(self, master, items, height=None, **kwargs):
        """`items`: (id, label, value, maximum) – parallel progress rows."""
        self.items = list(items)
        super().__init__(master, height=height or 26 * max(1, len(self.items)) + 10, **kwargs)

    def render(self, x0, y0, x1, y1):
        if not self.items:
            return self.empty(x0, y0, x1, y1)
        zeile = (y1 - y0) / len(self.items)
        farben = self.palette(len(self.items))
        for i, (eid, label, wert, maximum) in enumerate(self.items):
            y = y0 + i * zeile + zeile / 2
            self.create_text(x0, y, text=_clip(label, 18), anchor="w", fill=self.color("text_secondary"), font=self.font(8))
            links = x0 + 120
            self.create_rectangle(links, y - 4, x1 - 40, y + 4, fill=self.color("line"), outline="")
            zahl = bd._number(wert)
            if zahl is not None and maximum:
                anteil = max(0.0, min(1.0, zahl / maximum))
                item = self.create_rectangle(links, y - 4, links + (x1 - 40 - links) * anteil, y + 4, fill=farben[i], outline="")
                self.element(item, eid, f"{label}: {bd.format_value(zahl)} / {bd.format_value(maximum)}")
                self.create_text(x1, y, text=f"{anteil:.0%}", anchor="e", fill=self.color("text_muted"), font=self.font(8))
            else:
                self.create_text(x1, y, text="–", anchor="e", fill=self.color("text_muted"), font=self.font(8))


class Timeline(BentoChart):
    """Spans with start/end (numbers, e.g. day offsets or timestamps); `end=None` is a milestone."""

    def __init__(self, master, spans, axis_label=None, **kwargs):
        self.spans, self.axis_label = list(spans), axis_label
        super().__init__(master, **kwargs)

    def render(self, x0, y0, x1, y1):
        ext = bd.time_extent(self.spans)
        if ext is None:
            return self.empty(x0, y0, x1, y1)
        low, high = ext
        if low == high:
            low, high = low - 1, high + 1
        bahnen = list(dict.fromkeys(s.lane or "" for s in self.spans))
        links = x0 + (80 if any(bahnen) else 0)
        y1 -= 14
        hoehe = (y1 - y0) / max(1, len(bahnen))
        for t in bd.nice_ticks(low, high, 6):
            if low <= t <= high:
                x = links + bd.scale(t, low, high, x1 - links)
                self.create_line(x, y0, x, y1, fill=self.color("line"))
                self.create_text(x, y1 + 2, text=self.axis_label(t) if self.axis_label else bd.format_value(t), anchor="n",
                                 fill=self.color("text_muted"), font=self.font(8))
        farben = self.palette(len(bahnen))
        for s in self.spans:
            b = bahnen.index(s.lane or "")
            y = y0 + b * hoehe + hoehe / 2
            if b == 0 or True:
                if s.lane:
                    self.create_text(x0, y, text=_clip(s.lane, 11), anchor="w", fill=self.color("text_secondary"), font=self.font(8))
            xa = links + bd.scale(s.start, low, high, x1 - links)
            if s.end is None:
                item = self.create_polygon(xa, y - 7, xa + 7, y, xa, y + 7, xa - 7, y, fill=self.color("warning"), outline="")
            else:
                xb = links + bd.scale(s.end, low, high, x1 - links)
                item = self.create_rectangle(xa, y - 6, max(xb, xa + 3), y + 6, fill=farben[b], outline="")
            self.element(item, s.id, s.label)


class GraphChart(BentoChart):
    """Trees (nodes with `parent`) and directed graphs (`edges`) in layers from left to right."""

    def __init__(self, master, nodes, edges=(), **kwargs):
        self.nodes, self.edges = list(nodes), list(edges)
        super().__init__(master, **kwargs)

    def render(self, x0, y0, x1, y1):
        if not self.nodes:
            return self.empty(x0, y0, x1, y1)
        lage, self.problems = bd.layer_layout(self.nodes, self.edges)
        ebenen = max(l for l, _o in lage.values()) + 1
        je = {}
        for nid, (l, o) in lage.items():
            je[l] = max(je.get(l, 0), o + 1)
        dx = (x1 - x0) / ebenen
        pos = {}
        for nid, (l, o) in lage.items():
            dy = (y1 - y0) / je[l]
            pos[nid] = (x0 + l * dx + dx / 2, y0 + o * dy + dy / 2)
        kanten = [(n.parent, n.id) for n in self.nodes if n.parent in pos] + \
                 [(e.source, e.target) for e in self.edges if e.source in pos and e.target in pos]
        for a, b in kanten:
            (xa, ya), (xb, yb) = pos[a], pos[b]
            self.create_line(xa + 40, ya, xb - 40, yb, fill=self.color("text_muted"), arrow="last", width=1)
        for n in self.nodes:
            x, y = pos[n.id]
            item = self.create_rectangle(x - 40, y - 11, x + 40, y + 11, fill=self.color("hover"), outline=self.color("line"))
            self.create_text(x, y, text=_clip(n.label, 12), fill=self.color("text_primary"), font=self.font(8))
            self.element(item, n.id, n.label)


class RadarChart(BentoChart):
    def __init__(self, master, series_list, maximum=None, **kwargs):
        self.series_list, self.maximum = list(series_list), maximum
        super().__init__(master, **kwargs)

    def render(self, x0, y0, x1, y1):
        if not self.series_list or len(self.series_list[0].points) < 3:
            return self.empty(x0, y0, x1, y1)
        achsen = [p.label for p in self.series_list[0].points]
        hoch = self.maximum or max((v for s in self.series_list for v in s.valid()), default=1) or 1
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        r = min(x1 - x0, y1 - y0) / 2 - 18
        n = len(achsen)
        for i, name in enumerate(achsen):
            w = math.pi / 2 - 2 * math.pi * i / n
            self.create_line(cx, cy, cx + r * math.cos(w), cy - r * math.sin(w), fill=self.color("line"))
            self.create_text(cx + (r + 10) * math.cos(w), cy - (r + 10) * math.sin(w), text=_clip(name, 10),
                             fill=self.color("text_muted"), font=self.font(8))
        farben = self.palette(len(self.series_list))
        for s_index, s in enumerate(self.series_list):
            punkte = []
            for i, p in enumerate(s.points[:n]):
                if p.number is None:
                    continue
                w = math.pi / 2 - 2 * math.pi * i / n
                anteil = max(0.0, min(1.0, p.number / hoch))
                punkte += [cx + r * anteil * math.cos(w), cy - r * anteil * math.sin(w)]
            if len(punkte) >= 6:
                item = self.create_polygon(*punkte, fill="", outline=s.color or farben[s_index], width=2)
                self.element(item, s.id, s.label)


class BentoTable(tk.Frame):
    """Compact table: `columns` = [(key, title, kind)], `rows` = [{"id": ..., key: value}]; click a title to sort."""

    def __init__(self, master, context, columns, rows, on_select=None, max_rows=None, **kwargs):
        self.context = context
        super().__init__(master, bg=context.resolve_color("card_bg"), **kwargs)
        self.columns, self.rows, self.on_select, self.max_rows = list(columns), list(rows), on_select, max_rows
        self.sort_key, self.descending, self.selected = None, False, None
        self.labels = {}
        self.render()

    def sorted_rows(self):
        if self.sort_key is None:
            return list(self.rows)
        def schluessel(zeile):
            wert = zeile.get(self.sort_key)
            return (wert is None, wert if not isinstance(wert, str) else wert.casefold())
        vorhanden = [z for z in self.rows if z.get(self.sort_key) is not None]
        fehlend = [z for z in self.rows if z.get(self.sort_key) is None]
        return sorted(vorhanden, key=schluessel, reverse=self.descending) + fehlend

    def sort_by(self, key):
        self.descending = not self.descending if self.sort_key == key else False
        self.sort_key = key
        self.render()

    def select(self, row_id):
        self.selected = row_id
        self.render()
        if callable(self.on_select):
            self.on_select(row_id)

    def render(self):
        for kind in self.winfo_children():
            kind.destroy()
        c = self.context
        bg, text, muted = c.resolve_color("card_bg"), c.resolve_color("text_primary"), c.resolve_color("text_muted")
        for spalte, (key, titel, _kind) in enumerate(self.columns):
            pfeil = (" ▼" if self.descending else " ▲") if key == self.sort_key else ""
            kopf = tk.Label(self, text=titel + pfeil, bg=bg, fg=muted, font=c.resolve_font(8, "bold"), anchor="w", cursor="hand2")
            kopf.grid(row=0, column=spalte, sticky="we", padx=4, pady=(0, 2))
            kopf.bind("<Button-1>", lambda _e, k=key: self.sort_by(k))
        zeilen = self.sorted_rows()
        if self.max_rows:
            zeilen = zeilen[: self.max_rows]
        self.labels = {}
        for r, zeile in enumerate(zeilen, start=1):
            gewaehlt = zeile.get("id") == self.selected
            fuell = c.resolve_color("hover") if gewaehlt else bg
            for spalte, (key, _titel, kind) in enumerate(self.columns):
                wert = zeile.get(key)
                anzeige = bd.format_value(wert) if kind == "number" else ("–" if wert is None else str(wert))
                feld = tk.Label(self, text=anzeige, bg=fuell, fg=text, font=c.resolve_font(9),
                                anchor="e" if kind == "number" else "w")
                feld.grid(row=r, column=spalte, sticky="we", padx=4)
                feld.bind("<Button-1>", lambda _e, i=zeile.get("id"): self.select(i))
                self.labels.setdefault(zeile.get("id"), []).append(feld)
        for spalte in range(len(self.columns)):
            self.columnconfigure(spalte, weight=1)


class Badge(tk.Label):
    def __init__(self, master, context, text, role="accent", **kwargs):
        fill = context.resolve_color(role)
        super().__init__(master, text=text, bg=fill, fg=_readable(fill), font=context.resolve_font(8, "bold"), padx=6, pady=1, **kwargs)


class StatusDot(tk.Frame):
    STATES = {"ok": "confirm", "warning": "warning", "error": "danger", "idle": "text_muted"}

    def __init__(self, master, context, state, text, **kwargs):
        bg = context.resolve_color("card_bg")
        super().__init__(master, bg=bg, **kwargs)
        punkt = tk.Canvas(self, width=10, height=10, bg=bg, highlightthickness=0)
        punkt.create_oval(1, 1, 9, 9, fill=context.resolve_color(self.STATES.get(state, "text_muted")), outline="")
        punkt.pack(side="left", padx=(0, 6))
        tk.Label(self, text=text, bg=bg, fg=context.resolve_color("text_primary"), font=context.resolve_font(9)).pack(side="left")
        self.state = state


class MetricTrend(tk.Frame):
    """A value with optional previous value (change), target and trend series."""

    def __init__(self, master, context, label, value, previous=None, target=None, unit="", trend=None, higher_is_better=True, **kwargs):
        bg = context.resolve_color("card_bg")
        super().__init__(master, bg=bg, **kwargs)
        tk.Label(self, text=label, bg=bg, fg=context.resolve_color("text_muted"), font=context.resolve_font(9), anchor="w").pack(fill="x")
        zeile = tk.Frame(self, bg=bg)
        zeile.pack(fill="x")
        tk.Label(zeile, text=bd.format_value(bd._number(value), unit), bg=bg, fg=context.resolve_color("text_primary"),
                 font=context.resolve_font(20, "bold")).pack(side="left")
        self.change = None
        jetzt, vorher = bd._number(value), bd._number(previous)
        if jetzt is not None and vorher is not None:
            self.change = jetzt - vorher
            besser = (self.change >= 0) == higher_is_better
            rolle = "confirm" if self.change == 0 or besser else "danger"
            zeichen = "▲" if self.change > 0 else ("▼" if self.change < 0 else "■")
            tk.Label(zeile, text=f"{zeichen} {bd.format_value(abs(self.change), unit)}", bg=bg, fg=context.resolve_color(rolle),
                     font=context.resolve_font(9, "bold")).pack(side="left", padx=8)
        if target is not None:
            ziel = bd._number(target)
            tk.Label(self, text=f"→ {bd.format_value(ziel, unit)}", bg=bg, fg=context.resolve_color("text_muted"),
                     font=context.resolve_font(8), anchor="w").pack(fill="x")
        if trend is not None:
            Sparkline(self, trend, context=context).pack(fill="x", pady=(4, 0))
