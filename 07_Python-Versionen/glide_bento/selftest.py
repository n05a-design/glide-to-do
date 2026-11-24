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
        self.check("1. BENTO_VERSION ist 0.1.0", BENTO_VERSION == "0.1.0")

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

                # Aufräumen
                root.destroy()
            except Exception as exc:
                self.check("Tk-Widget-Prüfung", False, f"Fehler bei Tk-Prüfung: {exc}")

        # Gesamtbewertung
        all_passed = all(r[1] for r in self.results)
        print("--------------------------------------------------", flush=True)
        print(f"Bento-Selbsttest: {sum(1 for r in self.results if r[1])}/{len(self.results)} Prüfungen bestanden.", flush=True)
        return all_passed


def main():
    runner = BentoSelftestRunner()
    ok = runner.run_all()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
