# Glide Bento Box System – Anleitung für Folgeprojekte

**Wiederverwendbare UI-Kompositionsschicht (Ebene B) für Python/Tkinter**

Stand 26.11.2026 · Glide 1.0.3 · Bento 0.2.0 · Glide-System V1.88 · Ebene B (D100)

---

## 1. Übersicht

Das **Glide Bento Box System** (`glide_bento`) ist ein modulares, portables, Tkinter-natives System zur UI-Komposition nach modernen Bento-Grid-Prinzipien (Apple HIG, Dashboard-Gestaltung, D100).

Es stellt bereit:
- **`BentoTokens`**: Semantische Design-Tokens für Abstände, Eckenradien, Schriftgrößen und Schwellenwerte.
- **`BentoContext`**: Kontext- und Dependency-Injection-Behälter für Farbpaletten (Themes), Icon-Provider, Schriften, Glas-Effekte und Tooltips.
- **`BentoLayoutPlanner`**: Tk-freier deterministischer Layout-Planner zur mathematischen Vorberechnung von Spalten, Spaltenbreiten und Greedy-Gewichtsverteilung.
- **`BentoCard`**: Universeller abgerundeter Kartencontainer mit automatischer Höhenanpassung, Tastaturfokus, Hover-Zuständen und Unterstrukturen (`BentoHeader`, `body`, `footer`).
- **`BentoGrid`**: Adaptiver Tkinter-Container, der Karten dynamisch über 1, 2 oder 3 Spalten verteilt.
- **`BentoMetric`, `BentoActions`, `BentoEmptyState`, `BentoDivider`**: Vorgefertigte, konsistente Inhaltskomponenten für Bento-Karten.

---

## 2. Architektur & Schichtentrennung (D100)

Glide folgt einer strikten 3-Ebenen-Architektur:
- **Ebene A (Glide-Anwendung):** `app.pyw`, Fachlogik, Aufgabenverwaltung, Benutzereinstellungen.
- **Ebene B (Bento-System):** `glide_bento` (generische UI-Komposition, frei von Anwendungslogik).
- **Ebene C (Framework Shell):** `glide_shell` (portabler Desktop-Adapter, Fensterlebensdauer, Modalität).

```
Ebene A: Glide-Anwendung (Startseite, Dialoge, Editoren)
   │
   ▼
Ebene B: Bento-System (glide_bento: BentoCard, BentoGrid, BentoLayoutPlanner)
   │
   ▼
Ebene C: Framework Shell (glide_shell: custom_controls, motion, window_lifetime)
```

**Verbindliche Grenzregeln:**
- `glide_bento` darf NIEMALS Module aus Ebene A importieren (erzwungen durch `tests/unit/test_bento_importregel.py`).
- `glide_shell` darf KEIN `glide_bento` importieren.
- Wiederverwendbarkeit: `glide_bento` kann gemeinsam mit `glide_shell` in jedem beliebigen neuen Tkinter-Projekt ohne Glide-Abhängigkeiten eingesetzt werden.

---

## 3. Schnellstart

```python
import tkinter as tk
from glide_bento import BentoContext, BentoGrid, BentoCard, BentoCardSpec, BentoMetric

root = tk.Tk()
root.geometry("800x600")

# Kontext initialisieren
context = BentoContext(
    theme={"bg": "#F5F5F7", "card": "#FFFFFF", "line": "#E5E5E7", "text": "#1D1D1F", "accent": "#0071E3"}
)

# Responsives Raster anlegen
grid = BentoGrid(root, context=context)
grid.pack(fill="both", expand=True)

# Karten hinzufügen
k1 = BentoCard(grid, context=context, title="Projektfortschritt", icon="★")
BentoMetric(k1.body, context=context, value="87%", label="Erledigt", trend="+5%").pack()
grid.add_card(k1)

k2 = BentoCard(grid, context=context, title="Hinweis", spec=BentoCardSpec(key="hinweis", span="wide"))
tk.Label(k2.body, text="Wartungsfenster heute Nacht.", bg="#FFFFFF").pack()
grid.add_card(k2)

root.mainloop()
```

---

## 4. Selbsttest und Demo-Galerie

- **Autonomer Selbsttest:**
  ```bash
  python3 -B -m glide_bento.selftest
  ```
  Führt 13 automatisierte Prüfungen für Tokens, Fallbacks, Greedy-Algorithmus und Komponenten aus.

- **Eigenständige Demo-Galerie:**
  ```bash
  python3 -B -m glide_bento.demo
  ```
  Interaktive Komponentengalerie mit Umschaltung für Hell/Dunkel/Kontrast und 1/2/3/Auto-Spalten.

---

## 5. Designvertrag

Siehe [`BENTO_DESIGN_CONTRACT.md`](BENTO_DESIGN_CONTRACT.md) für den vollständigen Designvertrag, Skalen, Barrierefreiheit und Token-Definitionen.
