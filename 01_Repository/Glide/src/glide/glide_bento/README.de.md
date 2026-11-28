# Glide Bento Box System – Anleitung für Folgeprojekte

**Wiederverwendbare UI-Kompositionsschicht (Ebene B) für Python/Tkinter**

Stand 28.11.2026 · Glide 1.0.3 · Bento 0.4.0 · Glide Shell ≥ 0.11.0 · Glide-System V1.98 · Ebene B (D100)

**Seit 0.4.0 (Ecosystem E03/E04):** `glide_bento.data` (Tk-freie Datenverträge: Punkte, Reihen, Knoten, Kanten, Spannen; fehlende Werte bleiben fehlend und werden nie als null gezeichnet), `glide_bento.charts` (Balken, Linien mit Zoom/Pan, Punkte, Kreis/Ring, Sparkline, Heatmap, Kalender-Heatmap, Fortschritt linear/segmentiert/radial, Zeitachse, Graph/Baum, Radar, Tabelle, Badge, Status, Trendkennzahl – alle mit Theme-Rollen, gebündeltem Neuzeichnen, Hover, Auswahl-Rückruf und Tastatur), `glide_bento.marketing` (Produktkarten und Portfolio aus dem Softwarekatalog der Shell) und `glide_bento.gallery` (55 dokumentierte Kompositionen). Explizit importieren wie `glide_bento.showcase`. Verlangt Shell ≥ 0.11.0. `BentoCard` überspringt unveränderte Größen und zeichnet seine Fläche einmal je Leerlauf.

**Seit 0.3.0:** Bento prüft beim Import `SHELL_MIN_VERSION` (0.7.0) gegen die installierte Shell und bricht mit `ShellVersionError` ab, wenn sie zu alt oder inkompatibel ist. Übernahme zusammen mit der Shell: `shell_uebernehmen.py --mit-bento` (schreibt `BENTO_MANIFEST.json`). `glide_bento.showcase.bento_entries()` liefert die Galerie-Einträge aller Komponenten für einen `glide_shell.showcase.ShowcaseRegistry`; Glide zeigt sie unter Hilfe › „Komponenten-Galerie …“.

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
