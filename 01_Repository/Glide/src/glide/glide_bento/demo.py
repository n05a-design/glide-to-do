# SPDX-License-Identifier: MPL-2.0
"""Bento Demonstrationshost und Komponenten-Galerie (D100).

Eigenständige visuelle Referenzanwendung für alle Bento-Komponenten.
Startbar ohne Glide Application über: python3 -B -m glide_bento.demo
"""
import sys
import tkinter as tk
from typing import Any

from . import (
    BENTO_VERSION,
    BentoCard,
    BentoGrid,
    BentoContext,
    BentoCardSpec,
    BentoGridSpec,
    BentoMetric,
    BentoActions,
    BentoEmptyState,
    BentoDivider,
)

# Neutrale Farbpaletten für die Demonstration
THEMES = {
    "light": {
        "card_bg": "#FFFFFF",
        "canvas_bg": "#F2F2F7",
        "card_border": "#E5E5EA",
        "text_primary": "#1C1C1E",
        "text_secondary": "#48484A",
        "text_muted": "#8E8E93",
        "accent": "#007AFF",
        "confirm": "#34C759",
        "warning": "#FF9500",
        "danger": "#FF3B30",
        "focus": "#007AFF",
        "hover": "#E5E5EA",
        "button_bg": "#E5E5EA",
        "button_fg": "#1C1C1E",
    },
    "dark": {
        "card_bg": "#1C1C1E",
        "canvas_bg": "#000000",
        "card_border": "#38383A",
        "text_primary": "#FFFFFF",
        "text_secondary": "#EBEBF5",
        "text_muted": "#8E8E93",
        "accent": "#0A84FF",
        "confirm": "#30D158",
        "warning": "#FF9F0A",
        "danger": "#FF453A",
        "focus": "#0A84FF",
        "hover": "#2C2C2E",
        "button_bg": "#2C2C2E",
        "button_fg": "#FFFFFF",
    },
    "contrast": {
        "card_bg": "#000000",
        "canvas_bg": "#000000",
        "card_border": "#FFFFFF",
        "text_primary": "#FFFFFF",
        "text_secondary": "#FFFFFF",
        "text_muted": "#E5E5EA",
        "accent": "#FFFF00",
        "confirm": "#00FF00",
        "warning": "#FFA500",
        "danger": "#FF0000",
        "focus": "#FFFF00",
        "hover": "#333333",
        "button_bg": "#000000",
        "button_fg": "#FFFFFF",
    },
}


class BentoDemoApp:
    """Verwaltet das Hauptfenster der Bento-Demonstration."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"Glide Bento Box System {BENTO_VERSION} – Component Gallery")
        self.root.geometry("1060x780")
        self.root.minsize(580, 480)

        self.current_theme_key = "light"
        self.context = BentoContext(theme=THEMES[self.current_theme_key])

        self.grid_spec = BentoGridSpec(columns="auto")
        self.grid: BentoGrid | None = None
        self.cards: list[BentoCard] = []

        self._build_chrome()
        self._build_content()

    def _build_chrome(self) -> None:
        """Erzeugt Menü- und Werkzeugleiste am oberen Rand."""
        self.toolbar = tk.Frame(self.root, bg=self.context.resolve_color("canvas_bg"), pady=8, padx=16)
        self.toolbar.pack(side="top", fill="x")

        # Titel in Toolbar
        title = tk.Label(
            self.toolbar,
            text=f"Bento Box System {BENTO_VERSION}",
            bg=self.context.resolve_color("canvas_bg"),
            fg=self.context.resolve_color("text_primary"),
            font=self.context.resolve_font(13, "bold"),
        )
        title.pack(side="left", padx=(0, 16))

        # Theme-Umschaltung
        lbl_theme = tk.Label(
            self.toolbar,
            text="Theme:",
            bg=self.context.resolve_color("canvas_bg"),
            fg=self.context.resolve_color("text_muted"),
            font=self.context.resolve_font(10),
        )
        lbl_theme.pack(side="left", padx=(0, 4))

        for key in ("light", "dark", "contrast"):
            btn = tk.Button(
                self.toolbar,
                text=key.capitalize(),
                command=lambda k=key: self.switch_theme(k),
                font=self.context.resolve_font(9),
                padx=8,
                pady=2,
            )
            btn.pack(side="left", padx=2)

        # Spalten-Wahl
        lbl_col = tk.Label(
            self.toolbar,
            text="Spalten:",
            bg=self.context.resolve_color("canvas_bg"),
            fg=self.context.resolve_color("text_muted"),
            font=self.context.resolve_font(10),
        )
        lbl_col.pack(side="left", padx=(16, 4))

        for opt in ("auto", 1, 2, 3):
            label_text = "Auto" if opt == "auto" else f"{opt}"
            btn = tk.Button(
                self.toolbar,
                text=label_text,
                command=lambda o=opt: self.switch_columns(o),
                font=self.context.resolve_font(9),
                padx=8,
                pady=2,
            )
            btn.pack(side="left", padx=2)

    def _build_content(self) -> None:
        """Erzeugt das scrollbare BentoGrid und füllt es mit Beispielkarten."""
        # Scrollbarer Rahmen
        self.container = tk.Frame(self.root, bg=self.context.resolve_color("canvas_bg"))
        self.container.pack(side="top", fill="both", expand=True)

        self.canvas = tk.Canvas(self.container, bg=self.context.resolve_color("canvas_bg"), bd=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.grid = BentoGrid(self.canvas, context=self.context, spec=self.grid_spec)
        self.canvas_window = self.canvas.create_window((16, 16), window=self.grid, anchor="nw")

        def on_canvas_configure(event):
            # Grid auf die Canvasbreite minus Rand erweitern
            w = max(1, event.width - 32)
            self.canvas.itemconfigure(self.canvas_window, width=w)

        def on_grid_configure(_event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.canvas.bind("<Configure>", on_canvas_configure)
        self.grid.bind("<Configure>", on_grid_configure)

        self._populate_cards()

    def _populate_cards(self) -> None:
        """Erzeugt repräsentative Beispielkarten zur Demonstration aller Komponenten."""
        assert self.grid is not None

        # 1. Vollbreiten-Ankündigungskarte
        card_welcome = BentoCard(
            self.grid,
            context=self.context,
            spec=BentoCardSpec(
                key="welcome",
                title=f"Bento Box System {BENTO_VERSION} – Architektur & Komponenten",
                icon="today",
                variant="full_width",
                heading_action=("Dokumentation", lambda: None, "accent"),
            ),
        )
        lbl = tk.Label(
            card_welcome.body,
            text=(
                "Glide Bento Box System ist die wiederverwendbare UI-Kompositionsschicht (Ebene B) für kartenbasierte "
                "Oberflächen in Desktop-Anwendungen. Es kombiniert semantische Tokens, flexible Kartenkomponenten "
                "und eine deterministische Layout-Engine vollständig ohne fachliche Anwendungsabhängigkeiten."
            ),
            bg=self.context.resolve_color("card_bg"),
            fg=self.context.resolve_color("text_primary"),
            font=self.context.resolve_font(11),
            justify="left",
            wraplength=600,
        )
        lbl.pack(anchor="w", pady=(0, 4))
        self.grid.add_card(card_welcome)

        # 2. Kennzahlen-Karte (BentoMetric)
        card_metrics = BentoCard(
            self.grid,
            context=self.context,
            spec=BentoCardSpec(key="metrics", title="Projektkennzahlen", icon="focus", weight=2),
        )
        m1 = BentoMetric(card_metrics.body, context=self.context, value=128, label="Abgeschlossene Aufgaben", trend="+14% diese Woche", trend_color="confirm")
        m1.pack(fill="x", pady=(0, 8))
        BentoDivider(card_metrics.body, context=self.context)
        m2 = BentoMetric(card_metrics.body, context=self.context, value="99.4%", label="Testabdeckung Core", trend="optimal", trend_color="confirm")
        m2.pack(fill="x", pady=(8, 0))
        self.grid.add_card(card_metrics)

        # 3. Interaktive Liste mit Aktionsleiste
        card_tasks = BentoCard(
            self.grid,
            context=self.context,
            spec=BentoCardSpec(key="tasks", title="Heute anstehend · zwei Spalten", icon="calendar", weight=3, span=2),
        )
        for text in ("Architekturkonzept prüfen", "BentoCard Widget-Testlauf", "Geometrische Grenzen messen"):
            row = tk.Frame(card_tasks.body, bg=self.context.resolve_color("card_bg"))
            row.pack(fill="x", pady=2)
            chk = tk.Label(row, text="○", bg=self.context.resolve_color("card_bg"), fg=self.context.resolve_color("accent"), font=self.context.resolve_font(12))
            chk.pack(side="left", padx=(0, 6))
            t_lbl = tk.Label(row, text=text, bg=self.context.resolve_color("card_bg"), fg=self.context.resolve_color("text_primary"), font=self.context.resolve_font(10))
            t_lbl.pack(side="left")

        actions = BentoActions(card_tasks.footer, context=self.context, align="left")
        actions.pack(fill="x")
        actions.add_action("Neuer Punkt", lambda: None, "accent")
        actions.add_action("Alle öffnen", lambda: None, "button_bg")
        self.grid.add_card(card_tasks)

        # 4. Bild- und Zeichnungsvorschau
        card_gallery = BentoCard(
            self.grid,
            context=self.context,
            spec=BentoCardSpec(key="gallery", title="Galerievorschau", icon="gallery", weight=2),
        )
        box = tk.Canvas(card_gallery.body, width=280, height=120, bg=self.context.resolve_color("canvas_bg"), bd=0, highlightthickness=0)
        box.pack(fill="x", pady=4)
        box.create_text(140, 60, text="[Visuelle Inhaltsfläche / Canvas]", fill=self.context.resolve_color("text_muted"))
        f_lbl = tk.Label(card_gallery.footer, text="6 Einträge synchronisiert", bg=self.context.resolve_color("card_bg"), fg=self.context.resolve_color("text_muted"), font=self.context.resolve_font(9))
        f_lbl.pack(anchor="w")
        self.grid.add_card(card_gallery)

        # 5. Leerzustand (BentoEmptyState)
        card_empty = BentoCard(
            self.grid,
            context=self.context,
            spec=BentoCardSpec(key="empty", title="Benachrichtigungen", icon="pinned", weight=1),
        )
        empty = BentoEmptyState(
            card_empty.body,
            context=self.context,
            message="Keine neuen Mitteilungen. Alles ist auf dem aktuellen Stand.",
            action=("Aktualisieren", lambda: None, "accent"),
        )
        empty.pack(fill="x")
        self.grid.add_card(card_empty)

    def switch_theme(self, theme_key: str) -> None:
        """Wechselt das aktive Theme zur Laufzeit."""
        if theme_key not in THEMES:
            return
        self.current_theme_key = theme_key
        self.context = BentoContext(theme=THEMES[theme_key])

        bg = self.context.resolve_color("canvas_bg")
        self.root.configure(bg=bg)
        self.toolbar.configure(bg=bg)
        self.container.configure(bg=bg)
        self.canvas.configure(bg=bg)
        if self.grid:
            self.grid.update_theme(self.context)

    def switch_columns(self, option: Any) -> None:
        """Schaltet zwischen Auto- und fester Spaltenanzahl um."""
        self.grid_spec = BentoGridSpec(columns=option)
        if self.grid:
            self.grid.grid_spec = self.grid_spec
            self.grid.schedule_layout()


def main():
    root = tk.Tk()
    app = BentoDemoApp(root)
    # Prüfen, ob als Kurztest ausgeführt (z.B. --headless oder --test)
    if "--test" in sys.argv:
        root.update_idletasks()
        print("BentoDemoApp erfolgreich initialisiert (Testmodus).", flush=True)
        root.destroy()
        sys.exit(0)
    root.mainloop()


if __name__ == "__main__":
    main()
