# SPDX-License-Identifier: MPL-2.0
"""Bento composition library for the gallery (Bento 0.4.0).

About fifty distinct compositions built from a small set of base components
(`charts`, `marketing`, `BentoCard`, `BentoGrid`). Every entry documents its
category, base components, data contract, interaction, theming and typical
scenarios. Data are artificial, deterministic samples – a host shows these
only in a gallery clearly marked as such. No variant differs only by colour.

`composition_entries(version)` returns `ShowcaseEntry` objects; ids start with
``bento.viz.``. `COMPOSITION_IDS` lists them for coverage checks.
"""
from __future__ import annotations

import tkinter as tk

from glide_shell.showcase import ShowcaseEntry

from . import charts as c
from . import data as d
from .card import BentoCard
from .context import BentoContext
from .grid import BentoGrid
from .specs import BentoCardSpec


def _ctx(env):
    ctx = (env.extra or {}).get("bento_context")
    return ctx if ctx is not None else BentoContext.for_host(theme_provider=lambda: env.palette)


def _frame(master, env):
    return tk.Frame(master, bg=env.color("card", "#FFFFFF"))


def _with_selection(master, env, factory):
    """Composition with a live selection line: proves the callback contract."""
    rahmen = _frame(master, env)
    anzeige = tk.Label(rahmen, text="Selection: –", bg=env.color("card", "#FFFFFF"), fg=env.color("muted", "#666666"), anchor="w")
    widget = factory(rahmen, lambda eid: anzeige.configure(text=f"Selection: {eid}"))
    widget.pack(fill="x")
    anzeige.pack(fill="x")
    rahmen.chart = widget
    return rahmen


MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def _s(sid, label, values, labels=MONTHS, unit=""):
    return d.series(sid, label, list(zip(labels, values)), unit=unit)


def _chart(cls, data_f, interactive=True, **opt):
    def bauen(master, env):
        if interactive:
            return _with_selection(master, env, lambda m, sel: cls(m, data_f(), context=_ctx(env), on_select=sel, **opt))
        rahmen = _frame(master, env)
        cls(rahmen, data_f(), context=_ctx(env), **opt).pack(fill="x")
        return rahmen
    return bauen


def _widget(factory):
    def bauen(master, env):
        rahmen = _frame(master, env)
        factory(rahmen, _ctx(env))
        return rahmen
    return bauen


def _grid_of(cards):
    def bauen(master, env):
        ctx = _ctx(env)
        raster = BentoGrid(master, context=ctx)
        for key, titel, span, inhalt in cards:
            karte = BentoCard(raster, context=ctx, title=titel, spec=BentoCardSpec(key, span=span))
            inhalt(karte.body, ctx).pack(fill="x")
            raster.add_card(karte)
        return raster
    return bauen


def _calendar(weeks, every=1):
    import datetime as dt
    start = dt.date(2026, 9, 7)
    return {(start + dt.timedelta(days=i)).isoformat(): ((i * 7) % 5 if i % every == 0 else None) for i in range(weeks * 7)}


def _tree():
    return [d.Node("root", "Programme"), d.Node("a", "Planning", "root"), d.Node("b", "Delivery", "root"),
            d.Node("a1", "Scope", "a"), d.Node("a2", "Budget", "a"), d.Node("b1", "Build", "b"), d.Node("b2", "Review", "b")]


def _gantt():
    return [d.Span(f"t{i}", f"Task {i + 1}", i * 3, i * 3 + 4 + (i % 3) * 2, f"Phase {1 + i // 4}") for i in range(10)]


RAW = [
    # id, name, category, components, data contract, interaction, scenarios, builder, summary
    ("badges", "Badges", "Basics", ("Badge",), "text + colour role", "none", ("status labels", "tags"),
     _widget(lambda m, ctx: [c.Badge(m, ctx, t, r).pack(side="left", padx=3) for t, r in (("New", "accent"), ("Done", "confirm"), ("Risk", "warning"), ("Blocked", "danger"))]),
     "Compact labels in semantic roles with readable text colour."),
    ("status", "Status indicators", "Basics", ("StatusDot",), "state ok/warning/error/idle + text", "none", ("health", "sync state"),
     _widget(lambda m, ctx: [c.StatusDot(m, ctx, s, t).pack(anchor="w") for s, t in (("ok", "Backup current"), ("warning", "Review due"), ("error", "Export failed"), ("idle", "Not started"))]),
     "Coloured dot with text; meaning never relies on colour alone."),
    ("metric-trend", "Metric with change", "Metrics", ("MetricTrend",), "value, previous", "none", ("KPI", "weekly change"),
     _widget(lambda m, ctx: c.MetricTrend(m, ctx, "Completed", 42, previous=35).pack(fill="x")), "Value with signed change against the previous period."),
    ("metric-target", "Metric with target", "Metrics", ("MetricTrend",), "value, target", "none", ("goal tracking",),
     _widget(lambda m, ctx: c.MetricTrend(m, ctx, "Practice minutes", 95, target=120, unit="min").pack(fill="x")), "Value with its target shown below."),
    ("metric-lower-better", "Metric where lower is better", "Metrics", ("MetricTrend",), "value, previous, higher_is_better=False", "none", ("errors", "overdue items"),
     _widget(lambda m, ctx: c.MetricTrend(m, ctx, "Overdue", 3, previous=7, higher_is_better=False).pack(fill="x")), "Falling value shown as improvement."),
    ("metric-spark", "Metric with sparkline", "Metrics", ("MetricTrend", "Sparkline"), "value + Series", "none", ("trend at a glance",),
     _widget(lambda m, ctx: c.MetricTrend(m, ctx, "Daily games", 12, previous=9, trend=_s("t", "Games", [4, 6, 5, 8, 9, 12])).pack(fill="x")),
     "Key figure with a compact trend line."),
    ("metric-group", "Metric group", "Metrics", ("BentoGrid", "BentoCard", "MetricTrend"), "three values", "responsive grid", ("dashboard header",),
     _grid_of([(f"m{i}", t, 1, (lambda v, p: (lambda m, ctx: c.MetricTrend(m, ctx, "this week", v, previous=p)))(v, p)) for i, (t, v, p) in
               enumerate((("Open", 18, 21), ("Done", 31, 24), ("New", 9, 9)))]), "Three key figures that flow from three to one column."),
    ("progress-linear", "Linear progress", "Progress", ("ProgressBar",), "value, maximum", "none", ("project progress",),
     _widget(lambda m, ctx: c.ProgressBar(m, 0.62, label="Chapter 3", context=ctx).pack(fill="x")), "Share of a whole with percentage."),
    ("progress-segmented", "Segmented progress", "Progress", ("ProgressBar",), "value, maximum, segments", "none", ("steps of a course",),
     _widget(lambda m, ctx: c.ProgressBar(m, 3, 5, segments=5, label="Lessons", context=ctx).pack(fill="x")), "Completed steps as segments."),
    ("progress-target", "Progress with threshold", "Progress", ("ProgressBar",), "value, maximum, target", "none", ("quota", "threshold"),
     _widget(lambda m, ctx: c.ProgressBar(m, 0.45, target=0.8, label="Goal 80 %", context=ctx).pack(fill="x")), "Progress with a target marker."),
    ("progress-unknown", "Progress without value", "Progress", ("ProgressBar",), "value=None", "none", ("missing data",),
     _widget(lambda m, ctx: c.ProgressBar(m, None, label="Not measured", context=ctx).pack(fill="x")), "A missing value is shown as unknown, never as 0 %."),
    ("progress-radial", "Radial progress", "Progress", ("RadialProgress",), "value, maximum", "none", ("completion ring",),
     _widget(lambda m, ctx: c.RadialProgress(m, 7, 10, label="Exercises", context=ctx).pack(fill="x")), "Full ring with centred percentage."),
    ("progress-semicircle", "Semicircle gauge", "Progress", ("RadialProgress",), "value, maximum, semicircle", "none", ("gauge",),
     _widget(lambda m, ctx: c.RadialProgress(m, 0.3, semicircle=True, label="Capacity", context=ctx, height=100).pack(fill="x")), "Half-circle gauge."),
    ("progress-multi", "Parallel progress", "Progress", ("MultiProgress",), "(id, label, value, maximum) rows", "hover, selection", ("several projects",),
     _chart(c.MultiProgress, lambda: [("a", "Alpha", 8, 10), ("b", "Beta", 3, 12), ("c", "Gamma with a long name", 5, 5), ("d", "Delta", None, 4)]),
     "Several progress rows; unknown values marked."),
    ("bar-vertical", "Bar chart", "Bars", ("BarChart",), "Series", "hover, selection, keyboard", ("monthly values",),
     _chart(c.BarChart, lambda: [_s("v", "Visits", [12, 19, 7, 15, 22, 18])], height=190), "Single series with nice ticks."),
    ("bar-horizontal", "Horizontal bars", "Bars", ("BarChart",), "Series", "hover, selection", ("ranking",),
     _chart(c.BarChart, lambda: [d.series("h", "Score", [("Openings", 8), ("Endgames", 5), ("Tactics", 11), ("Strategy", 4)])], orientation="horizontal", height=170),
     "Horizontal bars for long category names."),
    ("bar-grouped", "Grouped bars", "Bars", ("BarChart",), "several Series", "hover, selection", ("comparison",),
     _chart(c.BarChart, lambda: [_s("a", "2025", [5, 7, 6, 9]), _s("b", "2026", [6, 9, 8, 12])], height=190), "Two series side by side."),
    ("bar-stacked", "Stacked bars", "Bars", ("BarChart",), "several Series, mode=stacked", "hover, selection", ("composition",),
     _chart(c.BarChart, lambda: [_s("o", "Open", [4, 3, 5, 2]), _s("p", "In progress", [2, 4, 1, 3]), _s("d", "Done", [6, 7, 9, 11])], mode="stacked", height=190),
     "Parts stacked to their sum."),
    ("bar-negative", "Bars with negative values", "Bars", ("BarChart",), "Series with negatives", "hover", ("balance", "delta"),
     _chart(c.BarChart, lambda: [_s("n", "Delta", [3, -2, 5, -4, 1, 0])], height=190), "Zero line between positive and negative values."),
    ("bar-missing", "Bars with missing values", "Bars", ("BarChart",), "Series with None", "hover", ("incomplete data",),
     _chart(c.BarChart, lambda: [_s("m", "Measured", [3, None, 5, None, 2])], height=190), "Missing values leave a gap, not a zero bar."),
    ("bar-many", "Many categories", "Bars", ("BarChart",), "30 points", "hover", ("daily values",),
     _chart(c.BarChart, lambda: [d.series("d", "Daily", [(f"{i + 1}", (i * 7) % 11) for i in range(30)])], height=180), "Labels shorten instead of overlapping."),
    ("line-single", "Line chart", "Lines", ("LineChart",), "Series", "hover, selection, keyboard", ("trend",),
     _chart(c.LineChart, lambda: [_s("l", "Accuracy", [61, 64, 70, 68, 75, 79], unit="%")], height=190), "Single series with markers."),
    ("line-multi", "Several series", "Lines", ("LineChart",), "several Series", "hover, selection", ("comparison over time",),
     _chart(c.LineChart, lambda: [_s("a", "Player A", [1500, 1520, 1510, 1560, 1580]), _s("b", "Player B", [1490, 1500, 1540, 1530, 1600])], height=190),
     "Several lines from the shared palette."),
    ("line-area", "Area chart", "Lines", ("LineChart",), "Series, area", "hover", ("volume",),
     _chart(c.LineChart, lambda: [_s("a", "Minutes", [20, 35, 30, 45, 40, 55])], area=True, height=190), "Filled area down to zero."),
    ("line-gaps", "Line with gaps", "Lines", ("LineChart",), "Series with None", "hover", ("sensor gaps",),
     _chart(c.LineChart, lambda: [_s("g", "Value", [4, 5, None, 6, 7, None, None, 5, 6, 8, 7, 9])], height=190), "Missing values break the line."),
    ("line-zoom", "Zoom and pan", "Lines", ("LineChart",), "200 points", "wheel zoom, drag pan, reset", ("long history",),
     _chart(c.LineChart, lambda: [d.series("z", "History", [(f"#{i}", 50 + ((i * 37) % 23) - (i % 9)) for i in range(200)])], markers=False, height=190),
     "Mouse wheel zooms around the pointer, dragging pans the window."),
    ("sparkline-row", "Sparkline row", "Lines", ("Sparkline",), "Series", "none", ("table cells", "compact trends"),
     _widget(lambda m, ctx: [c.Sparkline(m, _s(f"s{i}", "x", v), context=ctx).pack(side="left", padx=6) for i, v in
                             enumerate(([1, 3, 2, 5, 4], [5, 4, 4, 2, 1], [2, 2, None, 3, 4]))]), "Three trends without axes."),
    ("scatter", "Scatter plot", "Points", ("ScatterChart",), "Points with time (x) and value (y)", "hover, selection", ("correlation",),
     _chart(c.ScatterChart, lambda: [d.Series("sc", "Games", [d.Point(f"p{i}", f"Game {i}", 40 + (i * 13) % 50, time=i * 3 % 31) for i in range(25)])], height=190),
     "Points placed by two values."),
    ("scatter-single", "Single point", "Points", ("ScatterChart",), "one Point", "hover", ("edge case",),
     _chart(c.ScatterChart, lambda: [d.Series("one", "One", [d.Point("only", "Only", 5, time=2)])], height=150), "A single point stays centred and readable."),
    ("pie", "Pie chart", "Circular", ("PieChart",), "Series of positive values", "hover, selection", ("shares",),
     _chart(c.PieChart, lambda: d.series("p", "Share", [("Pages", 12), ("Lists", 20), ("Notes", 7)]), height=170), "Shares with legend and percentages."),
    ("donut", "Donut chart", "Circular", ("PieChart",), "Series, donut", "hover, selection", ("status split",),
     _chart(c.PieChart, lambda: d.series("dn", "Status", [("Done", 31), ("Open", 18), ("Overdue", 3)]), donut=True, height=170), "Ring with total in the centre."),
    ("donut-many", "Many slices", "Circular", ("PieChart",), "12 values", "hover", ("categories",),
     _chart(c.PieChart, lambda: d.series("dm", "Keys", [(k, 2 + (i * 5) % 9) for i, k in enumerate("C G D A E B F# Db Ab Eb Bb F".split())]), donut=True, height=200),
     "Palette continues with derived tones beyond five slices."),
    ("pie-excluded", "Pie with excluded values", "Circular", ("PieChart",), "Series with None, 0 and negatives", "hover", ("data quality",),
     _chart(c.PieChart, lambda: d.series("px", "Mixed", [("Valid A", 5), ("Zero", 0), ("Missing", None), ("Negative", -3), ("Valid B", 3)]), height=170),
     "Only positive values form slices; the others are excluded and listed by id."),
    ("heatmap", "Heatmap", "Heatmaps", ("Heatmap",), "(row, column) → Point", "hover, selection", ("matrix", "practice by weekday"),
     lambda master, env: _with_selection(master, env, lambda m, sel: c.Heatmap(
         m, ("Morning", "Noon", "Evening"), MONTHS[:8],
         {(r, k): d.Point(f"{r}-{k}", f"{r} {k}", (i * j) % 7) for i, r in enumerate(("Morning", "Noon", "Evening")) for j, k in enumerate(MONTHS[:8])},
         context=_ctx(env), on_select=sel, height=150)),
     "Values as colour intensity from the accent."),
    ("calendar", "Calendar heatmap", "Heatmaps", ("CalendarHeatmap",), "ISO date → value", "hover, selection", ("activity", "streaks"),
     lambda master, env: _with_selection(master, env, lambda m, sel: c.CalendarHeatmap(m, _calendar(12), context=_ctx(env), on_select=sel, height=150)),
     "Weeks as columns, weekdays as rows."),
    ("calendar-sparse", "Calendar with unknown days", "Heatmaps", ("CalendarHeatmap",), "ISO date → value or None", "hover", ("partial records",),
     lambda master, env: _with_selection(master, env, lambda m, sel: c.CalendarHeatmap(m, _calendar(8, every=3), context=_ctx(env), on_select=sel, height=150)),
     "Unknown days are outlined, not coloured as zero."),
    ("timeline", "Timeline with lanes", "Time", ("Timeline",), "Span with lane", "hover, selection", ("roadmap",),
     lambda master, env: _with_selection(master, env, lambda m, sel: c.Timeline(m, [d.Span("p", "Plan", 0, 6, "Team A"), d.Span("b", "Build", 5, 14, "Team B"),
                                                                                d.Span("m", "Review", 14, None, "Team A")], context=_ctx(env), on_select=sel, height=140)),
     "Spans per lane and a milestone."),
    ("milestones", "Milestones", "Time", ("Timeline",), "Span with end=None", "hover, selection", ("deadlines",),
     lambda master, env: _with_selection(master, env, lambda m, sel: c.Timeline(m, [d.Span(f"m{i}", f"Milestone {i}", i * 7, None) for i in range(6)],
                                                                                context=_ctx(env), on_select=sel, height=110, axis_label=lambda v: f"+{int(v)} d")),
     "Milestones on a single axis with day labels."),
    ("gantt", "Gantt-like plan", "Time", ("Timeline",), "Spans in phases", "hover, selection", ("project schedule",),
     lambda master, env: _with_selection(master, env, lambda m, sel: c.Timeline(m, _gantt(), context=_ctx(env), on_select=sel, height=160)),
     "Tasks as bars grouped into phases."),
    ("sequence", "Sequence", "Time", ("Timeline",), "adjacent Spans", "hover", ("chord sequence", "move sequence"),
     lambda master, env: _with_selection(master, env, lambda m, sel: c.Timeline(m, [d.Span(f"s{i}", n, i * 4, i * 4 + 4, "Bar") for i, n in enumerate(("I", "vi", "IV", "V"))],
                                                                                context=_ctx(env), on_select=sel, height=90)),
     "Equal steps in order; content comes from the host."),
    ("tree", "Tree", "Hierarchies", ("GraphChart",), "Node with parent", "hover, selection", ("structure", "outline"),
     lambda master, env: _with_selection(master, env, lambda m, sel: c.GraphChart(m, _tree(), context=_ctx(env), on_select=sel, height=200)),
     "Parent-child layers from left to right."),
    ("dag", "Dependency graph", "Hierarchies", ("GraphChart",), "Node + Edge", "hover, selection", ("dependencies",),
     lambda master, env: _with_selection(master, env, lambda m, sel: c.GraphChart(m, [d.Node(n, n.title()) for n in ("design", "build", "test", "docs", "release")],
                                                                                  [d.Edge("design", "build"), d.Edge("build", "test"), d.Edge("design", "docs"),
                                                                                   d.Edge("test", "release"), d.Edge("docs", "release")], context=_ctx(env), on_select=sel, height=190)),
     "Directed edges in layers."),
    ("graph-cycle", "Graph with a cycle", "Hierarchies", ("GraphChart",), "Edges forming a cycle", "hover", ("data check",),
     lambda master, env: _with_selection(master, env, lambda m, sel: c.GraphChart(m, [d.Node("a", "A"), d.Node("b", "B"), d.Node("c", "C")],
                                                                                  [d.Edge("a", "b"), d.Edge("b", "c"), d.Edge("c", "a")], context=_ctx(env), on_select=sel, height=150)),
     "A cycle is broken deterministically and reported."),
    ("tree-wide", "Wide tree", "Hierarchies", ("GraphChart",), "many children", "hover", ("catalogue",),
     lambda master, env: _with_selection(master, env, lambda m, sel: c.GraphChart(m, [d.Node("r", "Library")] + [d.Node(f"c{i}", f"Topic {i}", "r") for i in range(8)],
                                                                                  context=_ctx(env), on_select=sel, height=240)),
     "Eight children stay readable."),
    ("table-sort", "Sortable table", "Tables", ("BentoTable",), "columns + rows with id", "click title to sort, select row", ("overview",),
     lambda master, env: _with_selection(master, env, lambda m, sel: c.BentoTable(m, _ctx(env), [("name", "Name", "text"), ("open", "Open", "number"), ("done", "Done", "number")],
                                                                                  [{"id": "a", "name": "Alpha", "open": 3, "done": 9}, {"id": "b", "name": "Beta", "open": 7, "done": 2},
                                                                                   {"id": "c", "name": "Gamma", "open": 0, "done": 5}], on_select=sel)),
     "Click a column title to sort ascending, again for descending."),
    ("table-missing", "Table with missing values", "Tables", ("BentoTable",), "rows with None", "sort keeps missing values last", ("incomplete data",),
     _widget(lambda m, ctx: c.BentoTable(m, ctx, [("k", "Key", "text"), ("v", "Value", "number")],
                                         [{"id": "1", "k": "Measured", "v": 4}, {"id": "2", "k": "Unknown", "v": None}, {"id": "3", "k": "Zero", "v": 0}]).pack(fill="x")),
     "Missing values show a dash and stay last when sorting."),
    ("table-matrix", "Comparison matrix", "Tables", ("BentoTable",), "numeric columns", "sort", ("feature comparison",),
     _widget(lambda m, ctx: c.BentoTable(m, ctx, [("opt", "Option", "text"), ("speed", "Speed", "number"), ("memory", "Memory MB", "number"), ("score", "Score", "number")],
                                         [{"id": o, "opt": o, "speed": s, "memory": mem, "score": sc} for o, s, mem, sc in
                                          (("Retained", 9, 120, 8.5), ("Rebuild", 4, 80, 6), ("Virtual", 8, 60, 9))]).pack(fill="x")),
     "Numbers right-aligned for comparison."),
    ("table-detail", "Table with detail", "Tables", ("BentoTable", "BentoCard"), "rows + detail text", "select row shows detail", ("master-detail",),
     lambda master, env: _with_selection(master, env, lambda m, sel: c.BentoTable(m, _ctx(env), [("t", "Title", "text"), ("d", "Due", "text")],
                                                                                  [{"id": f"r{i}", "t": f"Item {i}", "d": f"2026-12-{i + 1:02d}"} for i in range(6)], on_select=sel, max_rows=5)),
     "Selecting a row reports its id to the host; max_rows limits the view."),
    ("radar", "Radar chart", "Circular", ("RadarChart",), "Series with ≥ 3 points", "hover, selection", ("skill profile",),
     _chart(c.RadarChart, lambda: [d.series("a", "Now", [("Tactics", 7), ("Openings", 5), ("Endgame", 4), ("Time", 6), ("Calculation", 8)]),
                                   d.series("b", "Goal", [("Tactics", 9), ("Openings", 7), ("Endgame", 7), ("Time", 7), ("Calculation", 9)])], maximum=10, height=220),
     "Profiles on shared axes; sensible only for comparable dimensions."),
    ("dashboard", "Dashboard composition", "Compositions", ("BentoGrid", "BentoCard", "MetricTrend", "BarChart", "PieChart", "ProgressBar"), "several contracts", "responsive grid",
     ("start page", "project overview"),
     _grid_of([("k1", "Open", 1, lambda m, ctx: c.MetricTrend(m, ctx, "now", 18, previous=21, higher_is_better=False)),
               ("k2", "Progress", 1, lambda m, ctx: c.ProgressBar(m, 0.6, label="Release", context=ctx)),
               ("k3", "Status", 1, lambda m, ctx: c.PieChart(m, d.series("st", "Status", [("Done", 31), ("Open", 18)]), donut=True, context=ctx, height=140)),
               ("k4", "Throughput", 2, lambda m, ctx: c.BarChart(m, [_s("t", "Done", [5, 8, 6, 9, 11, 7])], context=ctx, height=150))]),
     "Metric, progress, status and trend cards with multi-span."),
    ("kpi-row", "KPI row", "Compositions", ("BentoGrid", "BentoCard", "MetricTrend", "Sparkline"), "values + Series", "responsive grid", ("header strip",),
     _grid_of([(f"r{i}", t, 1, (lambda v, s: (lambda m, ctx: c.MetricTrend(m, ctx, "7 days", v, trend=_s("x", "x", s))))(v, s))
               for i, (t, v, s) in enumerate((("Lessons", 6, [1, 0, 2, 1, 1, 1]), ("Games", 14, [2, 3, 1, 4, 2, 2]), ("Notes", 9, [1, 2, 1, 2, 2, 1]),
                                              ("Pages", 3, [0, 1, 0, 1, 0, 1])))]), "Four compact figures with trends."),
    ("empty-chart", "Empty chart", "Compositions", ("BarChart", "LineChart"), "empty Series", "none", ("first use",),
     _widget(lambda m, ctx: [c.BarChart(m, [d.series("e", "Empty", [])], context=ctx, height=90).pack(fill="x"),
                             c.LineChart(m, [d.series("e2", "Empty", [])], context=ctx, height=90).pack(fill="x")]), "Charts without data say so instead of drawing axes."),
    ("highlight-card", "Highlighted card", "Compositions", ("BentoCard", "MetricTrend"), "card variant", "none", ("selected item", "featured"),
     lambda master, env: (lambda ctx: (lambda karte: (c.MetricTrend(karte.body, ctx, "Featured", 7).pack(fill="x"), karte)[1])(
         BentoCard(master, context=ctx, title="Selected", fill_key="hover", outline_key="focus", spec=BentoCardSpec("hl"))))(_ctx(env)),
     "Selected cards use roles derived from the theme accent, never a fixed colour."),
]


def _product_card(master, env):
    from glide_shell import software_catalog
    from .marketing import ProductCard
    katalog = software_catalog.load_ecosystem()
    produkt = katalog.get("steps") or (katalog.products() or [None])[0]
    if produkt is None:
        return _frame(master, env)
    return ProductCard(master, _ctx(env), produkt, on_link=lambda _url: None)


def _portfolio(master, env):
    from glide_shell import software_catalog
    from .marketing import PortfolioView
    return PortfolioView(master, _ctx(env), software_catalog.load_ecosystem(), current_id="glide", on_link=lambda _url: None)


RAW += [
    ("product-card", "Product card", "Marketing", ("ProductCard", "BentoCard"), "software_catalog.Product", "link buttons call the host opener",
     ("more programs", "about"), _product_card, "Product from the shared catalogue in the host's design; links only after a click."),
    ("portfolio", "Portfolio", "Marketing", ("PortfolioView", "BentoGrid", "ProductCard"), "software_catalog.Catalog", "responsive grid, links on click",
     ("more programs",), _portfolio, "All other products of the ecosystem, without the current app."),
]

COMPOSITION_IDS = tuple(f"bento.viz.{r[0]}" for r in RAW)


def composition_entries(version=None):
    if version is None:
        from . import BENTO_VERSION as version
    eintraege = []
    for key, name, kategorie, komponenten, vertrag, interaktion, szenarien, bauen, zusammenfassung in RAW:
        eintraege.append(ShowcaseEntry(
            f"bento.viz.{key}", name, framework="Glide Bento", version=version, module="glide_bento.gallery",
            summary=zusammenfassung, states=(interaktion,), sizes=("responsive width",),
            theming="BentoContext roles (accent, confirm, warning, danger, text, card)", build=bauen,
            category=kategorie, components=tuple(komponenten), data_contract=vertrag, interaction=interaktion,
            scenarios=tuple(szenarien)))
    return eintraege
