# Glide Bento Box System – guide for follow-up projects

**Layer B Component & Composition System for Python/Tkinter**

Status as of 28.11.2026 · Glide 1.0.3 · Bento 0.4.0 · Glide Shell ≥ 0.11.0 · Glide-System V1.98 · Layer B (D100)

**Since 0.4.0 (Ecosystem E03/E04):** `glide_bento.data` (Tk-free data contracts: points, series, nodes, edges, spans; missing values stay missing and are never drawn as zero), `glide_bento.charts` (bar, line with zoom/pan, scatter, pie/donut, sparkline, heatmap, calendar heatmap, linear/segmented/radial progress, timeline, graph/tree, radar, table, badge, status, metric trend – all with theme roles, coalesced redraw, hover, selection callback and keyboard), `glide_bento.marketing` (product cards and portfolio from the shell's software catalogue) and `glide_bento.gallery` (55 documented compositions). Import them explicitly like `glide_bento.showcase`. Requires shell ≥ 0.11.0. `BentoCard` skips unchanged sizes and draws its surface once per idle cycle.

**Since 0.3.0:** on import Bento checks `SHELL_MIN_VERSION` (0.7.0) against the installed shell and stops with `ShellVersionError` when it is too old or incompatible. Take it over together with the shell: `shell_uebernehmen.py --mit-bento` (writes `BENTO_MANIFEST.json`). `glide_bento.showcase.bento_entries()` returns gallery entries for every component for a `glide_shell.showcase.ShowcaseRegistry`; Glide shows them under Help › "Component gallery …".

---

## 1. Overview

The **Glide Bento Box System** (`glide_bento`) is a modular, portable, Tkinter-native UI composition system inspired by modern Bento Grid patterns (Apple HIG, modern dashboard designs).

It provides:
- **`BentoTokens`**: Semantic design tokens (spacing, corner radiuses, typography scales, responsive breakpoints).
- **`BentoContext`**: Dependency injection container for theme palettes, icon providers, font providers, glass styling, and tooltips.
- **`BentoLayoutPlanner`**: Pure, Tk-free deterministic layout engine calculating columns, column widths, and greedy weight distribution.
- **`BentoCard`**: Composable rounded card container with auto-height synchronization, focus ring, hover styling, and semantic sub-areas (`BentoHeader`, `body`, `footer`).
- **`BentoGrid`**: Responsive Tkinter container automatically reflowing child cards across 1, 2, or 3 columns based on measured width.
- **`BentoMetric`, `BentoActions`, `BentoEmptyState`, `BentoDivider`**: Reusable card content widgets.

---

## 2. Architecture & Layer Separation (D100)

Glide follows a strict 3-tier architectural layering:
- **Layer A (Application):** `app.pyw`, domain entities, task management, user workflows.
- **Layer B (Bento System):** `glide_bento` (generic card & grid composition, zero domain knowledge).
- **Layer C (Framework Shell):** `glide_shell` (portable desktop adapter, window lifetime, modal session).

```
Layer A: Application (Glide Home, Dialogs, Workspaces)
   │
   ▼
Layer B: Bento System (glide_bento: BentoCard, BentoGrid, BentoLayoutPlanner)
   │
   ▼
Layer C: Framework Shell (glide_shell: custom_controls, motion, window_lifetime)
```

**Boundary Rules:**
- `glide_bento` MUST NEVER import any module from Layer A (`app.pyw`, `home_tiles.py`, etc.).
- `glide_shell` MUST NEVER import `glide_bento`.
- Reusability: `glide_bento` can be copied and used in any standalone Python/Tkinter application alongside `glide_shell`.

---

## 3. Quickstart

```python
import tkinter as tk
from glide_bento import BentoContext, BentoGrid, BentoCard, BentoCardSpec, BentoMetric

root = tk.Tk()
root.geometry("800x600")

# Setup context
context = BentoContext(
    theme={"bg": "#F5F5F7", "card": "#FFFFFF", "line": "#E5E5E7", "text": "#1D1D1F", "accent": "#0071E3"}
)

# Create responsive grid
grid = BentoGrid(root, context=context)
grid.pack(fill="both", expand=True)

# Add cards
card1 = BentoCard(grid, context=context, title="System Status", icon="●")
BentoMetric(card1.body, context=context, value="99.9%", label="Uptime", trend="+0.2%").pack()
grid.add_card(card1)

card2 = BentoCard(grid, context=context, title="Full Width Alert", spec=BentoCardSpec(key="alert", span="wide"))
tk.Label(card2.body, text="All systems operational.", bg="#FFFFFF").pack()
grid.add_card(card2)

root.mainloop()
```

---

## 4. Selftest and Demo Gallery

- **Autonomous Selftest:**
  ```bash
  python3 -B -m glide_bento.selftest
  ```
  Executes 13 automated checks verifying token ranges, context fallbacks, greedy layout math, and component lifecycles.

- **Standalone Gallery Demo:**
  ```bash
  python3 -B -m glide_bento.demo
  ```
  Interactive component gallery with Light/Dark/Contrast theme switcher and Auto/1/2/3 column layout controls.

---

## 5. Design Contract

See [`BENTO_DESIGN_CONTRACT.md`](BENTO_DESIGN_CONTRACT.md) for the complete design contract, scale definitions, accessibility rules, and token specifications.
