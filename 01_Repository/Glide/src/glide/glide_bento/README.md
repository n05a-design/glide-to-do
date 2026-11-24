# Glide Bento Box System 0.1.0

**Layer B Component & Composition System for Python/Tkinter**

Stand: 24.11.2026 · Bento Version: `0.1.0` · System Level: Ebene B (D100)

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
