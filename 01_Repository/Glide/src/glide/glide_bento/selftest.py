# SPDX-License-Identifier: MPL-2.0
"""Bento Selbsttest – Autonome Prüfung des Bento Box Systems auf dem Zielrechner.

Prüft alle Kernfunktionen unabhängig von Glide Application (D100, D102).
Aufruf: python3 -B -m glide_bento.selftest
"""
import sys
import tkinter as tk
from typing import List, Tuple

from . import (
    BENTO_VERSION,
    BentoTokens,
    DEFAULT_TOKENS,
    BentoContext,
    BentoCardSpec,
    BentoGridSpec,
    BentoLayoutPlan,
    BentoLayoutPlanner,
    BentoCard,
    BentoHeader,
    BentoGrid,
    BentoMetric,
    BentoActions,
    BentoEmptyState,
    BentoDivider,
)


class BentoSelftestRunner:
    """Führt autonome Prüfungen des Bento-Systems durch."""

    def __init__(self):
        self.results: List[Tuple[str, bool, str]] = []

    def check(self, name: str, condition: bool, reason: str = "") -> bool:
        self.results.append((name, bool(condition), reason))
        status = "PASS" if condition else "FAIL"
        detail = f" - {reason}" if reason else ""
        print(f"[{status}] {name}{detail}", flush=True)
        return bool(condition)

    def run_all(self) -> bool:
        print(f"=== Glide Bento Selftest (v{BENTO_VERSION}) ===", flush=True)

        # 1. Versionsintegrität
        self.check("1. BENTO_VERSION ist 0.2.0", BENTO_VERSION == "0.2.0")

        # 2. Token-Integrität und Skalen
        t = DEFAULT_TOKENS
        self.check(
            "2. Tokens Wertebereich",
            t.gap_default == 12 and t.card_radius == 18 and t.card_min_width == 300 and t.grid_margin == 16,
            f"gap={t.gap_default}, radius={t.card_radius}, min_w={t.card_min_width}",
        )

        # 3. Token Overrides
        custom_t = t.with_overrides(card_radius=24, gap_default=14)
        self.check(
            "3. Token Overrides",
            custom_t.card_radius == 24 and custom_t.gap_default == 14 and custom_t.grid_margin == 16,
        )

        # 4. Context Theme & Provider Fallbacks
        ctx = BentoContext()
        color_card = ctx.resolve_color("card_bg")
        color_canvas = ctx.resolve_color("canvas_bg")
        font_tuple = ctx.resolve_font(12, "bold")
        icon_str = ctx.resolve_icon("check")
        self.check(
            "4. BentoContext Fallbacks",
            color_card == "#FFFFFF" and color_canvas == "#F5F5F7" and font_tuple[1] == 12 and icon_str == "✓",
            f"card={color_card}, canvas={color_canvas}, icon={icon_str}",
        )

        # 5. Spezifikationen und Full-Width Erkennung
        s1 = BentoCardSpec(key="k1", title="Standard")
        s2 = BentoCardSpec(key="k2", variant="full_width")
        s3 = BentoCardSpec(key="k3", span="full")
        self.check("5. CardSpec Full-Width Erkennung", (not s1.is_full_width) and s2.is_full_width and s3.is_full_width)

        # 6. Tk-freier Layout-Planner Spaltenstufen
        planner = BentoLayoutPlanner(t)
        cols_small = planner.compute_column_count(500)
        cols_mid = planner.compute_column_count(750)
        cols_large = planner.compute_column_count(1100)
        self.check(
            "6. Layout-Planner Spaltenstufen",
            cols_small == 1 and cols_mid == 2 and cols_large == 3,
            f"500px={cols_small}, 750px={cols_mid}, 1100px={cols_large}",
        )

        # 7. Deterministische Greedy-Verteilung
        cards = [
            BentoCardSpec(key="h1", variant="full_width", order=0),
            BentoCardSpec(key="c1", weight=1, order=1),
            BentoCardSpec(key="c2", weight=2, order=2),
            BentoCardSpec(key="c3", weight=2, order=3),
            BentoCardSpec(key="c4", weight=2, order=4),
        ]
        plan_3 = planner.plan(1000, cards)
        self.check(
            "7. Deterministische Greedy-Verteilung",
            plan_3.column_count == 3
            and len(plan_3.header_cards) == 1
            and plan_3.header_cards[0].key == "h1"
            and len(plan_3.columns) == 3
            and plan_3.column_weights == (3, 2, 2),
            f"weights={plan_3.column_weights}, cols={[len(c) for c in plan_3.columns]}",
        )

        # 14. Multi-Span-Bandmodell (0.2.0): deterministisch und überlappungsfrei
        ms_cards = [
            BentoCardSpec(key="a", span=2, weight=3, order=0),
            BentoCardSpec(key="b", weight=2, order=1),
            BentoCardSpec(key="c", weight=1, order=2),
            BentoCardSpec(key="d", span="full", order=3),
            BentoCardSpec(key="e", order=4),
            BentoCardSpec(key="f", order=5),
        ]
        ok_bands = True
        detail = ""
        for width, cols in ((1100, 3), (750, 2), (500, 1)):
            first = planner.plan(width, ms_cards)
            again = planner.plan(width, list(ms_cards))
            seen = [key for key, *_rest in first.placements()]
            for band in first.bands:
                used: set[int] = set()
                for lane in band.lanes:
                    span_cols = set(range(lane.column, lane.column + lane.span))
                    if used & span_cols or max(span_cols) >= first.column_count:
                        ok_bands = False
                    used |= span_cols
            if first.placements() != again.placements() or sorted(seen) != sorted(c.key for c in ms_cards)                     or first.column_count != cols:
                ok_bands = False
            detail += f" {width}px={[b.kind for b in first.bands]}"
        split = planner.plan(1100, ms_cards).bands[0]
        ok_bands = ok_bands and split.kind == "split" and split.lanes[0].span == 2             and [c.key for c in split.lanes[1].cards] == ["b", "c"]
        self.check("14. Multi-Span-Bandmodell", ok_bands, detail)

        # 15. Host-Context-Token-Vertrag (Variante C) mit Fallback
        host_tokens = BentoTokens.from_host({"gap_relaxed": 20, "card_radius": 12, "unknown": "x", "gap_default": -1})
        host_ctx = BentoContext.for_host(theme_provider=lambda: {"card": "#202020"},
                                         token_provider=lambda: {"card_radius": 14})
        self.check(
            "15. Host-Token-Injection und Fallback",
            host_tokens.gap_relaxed == 20 and host_tokens.card_radius == 12 and host_tokens.gap_default == 12
            and host_tokens.three_column_min_width == 300 * 3 + 20 * 2 and host_tokens.custom.get("unknown") == "x"
            and host_ctx.tokens.card_radius == 14 and host_ctx.resolve_color("card_bg") == "#202020"
            and BentoTokens.from_host(None) is DEFAULT_TOKENS,
        )

        # 8. Tk-Initialisierung und Widget-Lebenszyklus
        tk_ok = False
        try:
            root = tk.Tk()
            root.withdraw()
            tk_ok = True
        except tk.TclError as e:
            print(f"[SKIP] Tk-Oberfläche nicht verfügbar: {e}", flush=True)

        if tk_ok:
            try:
                # 9. BentoCard Erstellung und Header
                card = BentoCard(root, context=ctx, title="Testkarte", icon="pinned", subtitle="Untertitel")
                card.update_idletasks()
                self.check("8. BentoCard & Header Widget-Erstellung", card.header is not None and card.inner is not None)

                # 10. BentoBody und BentoFooter
                body = card.body
                lbl = tk.Label(body, text="Inhalt")
                lbl.pack()
                footer = card.footer
                f_lbl = tk.Label(footer, text="Footer")
                f_lbl.pack()
                card.update_idletasks()
                self.check("9. BentoBody & BentoFooter Befüllung", len(body.winfo_children()) == 1 and len(footer.winfo_children()) == 1)

                # 11. BentoMetric Komponente
                metric = BentoMetric(body, context=ctx, value=42, label="Aktive Punkte", trend="+5 heute", trend_color="confirm")
                metric.pack()
                self.check("10. BentoMetric Komponente", metric.value_str == "42")

                # 12. BentoActions Komponente
                actions = BentoActions(body, context=ctx)
                btn = actions.add_action("Klick mich", lambda: None, "accent")
                self.check("11. BentoActions Komponente", len(actions.buttons) == 1 and btn.cget("text") == "Klick mich")

                # 13. BentoGrid Raster-Erstellung
                grid = BentoGrid(root, context=ctx)
                grid.pack(fill="both", expand=True)
                grid.add_card(card, s1)
                grid.update_idletasks()
                grid._execute_layout()
                self.check("12. BentoGrid Raster-Rendering", len(grid._cards) == 1)

                # 14. BentoEmptyState & BentoDivider
                divider = BentoDivider(body, context=ctx)
                empty = BentoEmptyState(body, context=ctx, message="Keine Daten vorhanden", action=("Anlegen", lambda: None, "accent"))
                self.check("13. BentoDivider & BentoEmptyState", divider is not None and empty is not None)

                # 16. Multi-Span im Raster: Bahnen getrennt, Karten bleiben beim Reflow erhalten
                root.geometry("1100x600")
                root.deiconify()
                ms_grid = BentoGrid(root, context=ctx)
                ms_grid.pack(fill="both", expand=True)
                ms_widgets = {}
                for spec in ms_cards:
                    widget = BentoCard(ms_grid, context=ctx, title=spec.key)
                    ms_widgets[spec.key] = widget
                    ms_grid.add_card(widget, spec)
                root.update()
                ms_grid.reflow()
                root.update()
                ids_before = {key: str(widget) for key, widget in ms_widgets.items()}
                wide_x = ms_widgets["a"].winfo_rootx() + ms_widgets["a"].winfo_width()
                side_x = ms_widgets["b"].winfo_rootx()
                three_cols = ms_grid.current_columns == 3
                root.geometry("500x600")
                root.update()
                ms_grid.reflow()
                root.update()
                retained = all(widget.winfo_exists() for widget in ms_widgets.values()) and                     ids_before == {key: str(widget) for key, widget in ms_widgets.items()}
                runs = ms_grid.layout_runs
                ms_grid.reflow()
                stable = ms_grid.layout_runs == runs
                self.check("16. BentoGrid Multi-Span, Retention und ruhiger Reflow",
                           three_cols and wide_x <= side_x and retained and ms_grid.current_columns == 1 and stable,
                           f"wide_end={wide_x}, side_start={side_x}, runs={runs}")

                # Aufräumen
                root.destroy()
            except Exception as exc:
                self.check("Tk-Widget-Prüfung", False, f"Fehler bei Tk-Prüfung: {exc}")

        # Gesamtbewertung
        all_passed = all(r[1] for r in self.results)
        print("--------------------------------------------------", flush=True)
        print(f"Bento-Selbsttest: {sum(1 for r in self.results if r[1])}/{len(self.results)} Prüfungen bestanden"
              + ("" if tk_ok else " (Tk-Prüfungen 8–13 und 16 SKIPPED, nicht bestanden)") + ".", flush=True)
        return all_passed


def main():
    runner = BentoSelftestRunner()
    ok = runner.run_all()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
