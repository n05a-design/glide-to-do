# SPDX-License-Identifier: MPL-2.0
"""Showcase-Einträge des Bento-Systems für die Galerie eines Hosts (Bento 0.3.0, D105).

Jeder Eintrag baut die echte Bento-Komponente mit künstlichen, als Beispiel
gekennzeichneten Daten. Der Host übergibt in `env.extra["bento_context"]` den
`BentoContext`, den er auch produktiv verwendet (Glide:
`ListApp.glide_bento_context`); ein Themawechsel ist damit ein Neuaufbau mit
einem neu befüllten Kontext. Ohne Kontext entsteht einer aus `env.palette`.

Registriert werden die Einträge in einem `glide_shell.showcase.ShowcaseRegistry`;
Bento selbst kennt keinen Host.
"""
from __future__ import annotations

import tkinter as tk

from glide_shell.showcase import ShowcaseEntry

BENTO_COMPONENTS = ("bento.card", "bento.metric", "bento.actions", "bento.empty_state", "bento.divider",
                    "bento.grid", "bento.layout_planner")


def _context(env):
    from .context import BentoContext
    kontext = env.extra.get("bento_context")
    if kontext is None:
        kontext = BentoContext(theme=dict(env.palette))
    return kontext


def _build_card(master, env):
    from .card import BentoCard
    from .specs import BentoCardSpec
    kontext = _context(env)
    karte = BentoCard(master, context=kontext, spec=BentoCardSpec(
        key="showcase-card", title="Sample card", subtitle="Example data", icon="today",
        heading_action=("Action", lambda: None, "accent")))
    tk.Label(karte.body, text="Card body with sample content.", bg=kontext.resolve_color("card_bg"),
             fg=kontext.resolve_color("text_primary"), font=kontext.resolve_font(10), anchor="w").pack(fill="x")
    return karte


def _build_metric(master, env):
    from .components import BentoMetric
    return BentoMetric(master, context=_context(env), value=42, label="Sample metric",
                       trend="+3 example", trend_color="confirm")


def _build_actions(master, env):
    from .components import BentoActions
    leiste = BentoActions(master, context=_context(env), align="left")
    leiste.add_action("Primary", lambda: None, "accent")
    leiste.add_action("Secondary", lambda: None, "button_bg")
    return leiste


def _build_empty(master, env):
    from .components import BentoEmptyState
    return BentoEmptyState(master, context=_context(env), title="Nothing here yet",
                           description="Example empty state with one main and one secondary action.",
                           action=("Create sample", lambda: None, "accent"),
                           secondary_action=("Learn more", lambda: None, "button_bg"))


def _build_divider(master, env):
    from .components import BentoDivider
    kontext = _context(env)
    rahmen = tk.Frame(master, bg=kontext.resolve_color("card_bg"))
    for text in ("Above the divider", "Below the divider"):
        tk.Label(rahmen, text=text, bg=kontext.resolve_color("card_bg"), fg=kontext.resolve_color("text_primary"),
                 font=kontext.resolve_font(10), anchor="w").pack(fill="x")
        if text.startswith("Above"):
            BentoDivider(rahmen, context=kontext)
    return rahmen


def _build_grid(master, env):
    from .card import BentoCard
    from .grid import BentoGrid
    from .specs import BentoCardSpec, BentoGridSpec
    kontext = _context(env)
    raster = BentoGrid(master, context=kontext, spec=BentoGridSpec(columns="auto"))
    for schluessel, titel, spanne in (("wide", "Sample · two columns", 2), ("a", "Sample A", 1),
                                      ("b", "Sample B", 1), ("c", "Sample C", 1)):
        karte = BentoCard(raster, context=kontext, spec=BentoCardSpec(key=schluessel, title=titel, span=spanne,
                                                                        weight=1))
        tk.Label(karte.body, text=f"span={spanne}", bg=kontext.resolve_color("card_bg"),
                 fg=kontext.resolve_color("text_muted"), font=kontext.resolve_font(9), anchor="w").pack(fill="x")
        raster.add_card(karte)
    return raster


def _build_planner(master, env):
    from .layout import BentoLayoutPlanner
    from .specs import BentoCardSpec
    kontext = _context(env)
    planer = BentoLayoutPlanner(kontext.tokens)
    karten = [BentoCardSpec(key="wide", span=2), BentoCardSpec(key="a"), BentoCardSpec(key="b")]
    rahmen = tk.Frame(master, bg=kontext.resolve_color("card_bg"))
    for breite in (360, 700, 1100):
        plan = planer.plan(breite, karten)
        tk.Label(rahmen, text=f"{breite:>4} px → {plan.column_count} column(s), {len(plan.bands)} band(s)",
                 bg=kontext.resolve_color("card_bg"), fg=kontext.resolve_color("text_primary"),
                 font=kontext.resolve_font(10), anchor="w").pack(fill="x")
    return rahmen


def bento_entries(version=None):
    """Showcase-Einträge für die öffentlichen Bento-Komponenten."""
    if version is None:
        from . import BENTO_VERSION as version
    gemeinsam = dict(framework="Glide Bento", version=version)
    return [
        ShowcaseEntry("bento.card", "BentoCard / BentoHeader", module="glide_bento.card",
                      summary="Rounded, themed card with header (title, icon, subtitle, action), body and footer.",
                      states=("standard", "hover", "glass", "heading action"), sizes=("auto height", "span 1–3"),
                      theming="BentoContext roles card_bg, card_border, text_primary", build=_build_card, **gemeinsam),
        ShowcaseEntry("bento.metric", "BentoMetric", module="glide_bento.components",
                      summary="Key figure with label and optional trend in a semantic colour.",
                      states=("value", "trend up", "trend neutral"), sizes=("font scale from tokens",),
                      theming="confirm / warning / muted roles", build=_build_metric, **gemeinsam),
        ShowcaseEntry("bento.actions", "BentoActions", module="glide_bento.components",
                      summary="Row of card actions created through the host's button factory.",
                      states=("primary", "secondary", "focus"), sizes=("left", "right", "fill"),
                      theming="host button factory (make_button)", build=_build_actions, **gemeinsam),
        ShowcaseEntry("bento.empty_state", "BentoEmptyState", module="glide_bento.components",
                      summary="Empty state with title, explanation, main and secondary action.",
                      states=("with actions", "message only"), sizes=("card width",),
                      theming="text roles, accent", build=_build_empty, **gemeinsam),
        ShowcaseEntry("bento.divider", "BentoDivider", module="glide_bento.components",
                      summary="Thin separator line inside a card.", states=("default",), sizes=("height 1 px",),
                      theming="card_border", build=_build_divider, **gemeinsam),
        ShowcaseEntry("bento.grid", "BentoGrid", module="glide_bento.grid",
                      summary="Responsive 1–3 column grid with multi-span bands and widget retention.",
                      states=("1 column", "2 columns", "3 columns", "span 2"), sizes=("breakpoints from tokens",),
                      theming="canvas_bg", limits="layout follows the width of the gallery area",
                      build=_build_grid, **gemeinsam),
        ShowcaseEntry("bento.layout_planner", "BentoLayoutPlanner", module="glide_bento.layout",
                      summary="Deterministic, Tk-free plan of columns and bands for a width.",
                      states=("narrow", "medium", "wide"), sizes=("any width",), theming="tokens only",
                      build=_build_planner, **gemeinsam),
    ]
