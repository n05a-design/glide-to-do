# SPDX-License-Identifier: MPL-2.0
"""Bento Inhaltskomponenten (Metric, Actions, EmptyState, Divider).

Wiederverwendbare generische UI-Bausteine für Bento-Karteninhalte (D100, D102).
"""
import tkinter as tk
from typing import Any, Callable, Sequence
from .context import BentoContext


class BentoMetric(tk.Frame):
    """Hervorgehobene Kennzahl mit Beschriftung und optionalem Status-/Trendindikator."""

    def __init__(
        self,
        master: tk.Widget,
        context: BentoContext,
        value: str | int,
        label: str,
        trend: str | None = None,
        trend_color: str | None = None,
        trend_direction: str | None = None,
        **kwargs,
    ):
        bg = context.resolve_color("card_bg")
        super().__init__(master, bg=bg, bd=0, highlightthickness=0, **kwargs)
        self.context = context
        self.value_str = str(value)
        self.label_str = label
        self.trend_str = trend
        self.trend_color_role = trend_color
        self.trend_direction = trend_direction

        self._value_label: tk.Label | None = None
        self._text_label: tk.Label | None = None
        self._trend_label: tk.Label | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        bg = self.context.resolve_color("card_bg")
        fg = self.context.resolve_color("text_primary")
        fg_muted = self.context.resolve_color("text_muted")
        tokens = self.context.tokens

        top_row = tk.Frame(self, bg=bg, bd=0, highlightthickness=0)
        top_row.pack(side="top", fill="x")

        # Große Zahl
        self._value_label = tk.Label(
            top_row,
            text=self.value_str,
            bg=bg,
            fg=fg,
            font=self.context.resolve_font(tokens.font_size_headline, "bold"),
            anchor="w",
        )
        self._value_label.pack(side="left")

        # Optionaler Status-/Trendmarker
        if self.trend_str:
            t_color = self.context.resolve_color(self.trend_color_role or "accent")
            self._trend_label = tk.Label(
                top_row,
                text=self.trend_str,
                bg=bg,
                fg=t_color,
                font=self.context.resolve_font(tokens.font_size_caption, "bold"),
            )
            self._trend_label.pack(side="left", padx=(tokens.gap_compact, 0), pady=(4, 0))

        # Beschriftung darunter
        self._text_label = tk.Label(
            self,
            text=self.label_str,
            bg=bg,
            fg=fg_muted,
            font=self.context.resolve_font(tokens.font_size_small),
            anchor="w",
        )
        self._text_label.pack(side="top", fill="x", pady=(2, 0))

    @property
    def value(self) -> str:
        return self.value_str

    @value.setter
    def value(self, new_val: str | int) -> None:
        self.update_value(new_val)

    @property
    def label(self) -> str:
        return self.label_str

    @property
    def trend(self) -> str | None:
        return self.trend_str

    def update_value(self, value: str | int, trend: str | None = None) -> None:
        """Aktualisiert den Wert der Kennzahl."""
        self.value_str = str(value)
        if self._value_label:
            self._value_label.configure(text=self.value_str)
        if trend is not None and self._trend_label:
            self.trend_str = trend
            self._trend_label.configure(text=trend)


class BentoActions(tk.Frame):
    """Adaptive Aktionsleiste für Bento-Karten (Schaltflächen-Fluss)."""

    def __init__(
        self,
        master: tk.Widget,
        context: BentoContext,
        align: str = "left",  # "left", "right", "fill"
        actions: Sequence[tuple[str, Callable[[], None], str]] | None = None,
        **kwargs,
    ):
        bg = context.resolve_color("card_bg")
        super().__init__(master, bg=bg, bd=0, highlightthickness=0, **kwargs)
        self.context = context
        self.align = align
        self.buttons: list[tk.Button] = []

        if actions:
            for item in actions:
                text = item[0]
                cmd = item[1]
                role = item[2] if len(item) > 2 else "accent"
                self.add_action(text, cmd, color_role=role)

    def add_action(
        self,
        text: str,
        command: Callable[[], None],
        color_role: str = "accent",
        tooltip: str | None = None,
        width: int | None = None,
    ) -> tk.Button:
        """Fügt einen Aktionsknopf zur Leiste hinzu."""
        bg = self.context.resolve_color("card_bg")
        btn_bg = self.context.resolve_color(color_role, self.context.resolve_color("accent"))
        is_highlight = color_role in ("accent", "confirm", "danger", "primary")
        btn_fg = "#FFFFFF" if is_highlight else self.context.resolve_color("text_primary")
        tokens = self.context.tokens

        btn = tk.Button(
            self,
            text=text,
            command=command,
            bg=btn_bg,
            fg=btn_fg,
            font=self.context.resolve_font(tokens.font_size_small, "bold" if is_highlight else "normal"),
            relief="flat",
            bd=0,
            padx=tokens.gap_default,
            pady=4,
            cursor="hand2",
            takefocus=True,
        )
        if width:
            btn.configure(width=width)

        if self.align == "fill":
            btn.pack(side="top", fill="x", pady=(0, tokens.gap_compact))
        else:
            side = "left" if self.align == "left" else "right"
            btn.pack(side=side, padx=(0 if side == "left" else tokens.gap_compact, tokens.gap_compact if side == "left" else 0))

        if tooltip:
            self.context.attach_tooltip(btn, tooltip)

        self.buttons.append(btn)
        return btn


class BentoEmptyState(tk.Frame):
    """Ruhiger, kompakter Leerzustand für Karten ohne Einträge (P4 / P5)."""

    def __init__(
        self,
        master: tk.Widget,
        context: BentoContext,
        message: str | None = None,
        title: str | None = None,
        description: str | None = None,
        icon: Any | None = None,
        action: tuple[str, Callable[[], None], str] | None = None,
        action_caption: str | None = None,
        action_command: Callable[[], None] | None = None,
        action_color: str = "accent",
        **kwargs,
    ):
        bg = context.resolve_color("card_bg")
        super().__init__(master, bg=bg, bd=0, highlightthickness=0, **kwargs)
        self.context = context
        self.title_str = title or message or ""
        self.desc_str = description or (message if title else "")
        self.icon_data = icon
        if action:
            self.action = action
        elif action_caption and action_command:
            self.action = (action_caption, action_command, action_color)
        else:
            self.action = None

        self.action_button: tk.Button | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        bg = self.context.resolve_color("card_bg")
        fg = self.context.resolve_color("text_primary")
        fg_muted = self.context.resolve_color("text_muted")
        tokens = self.context.tokens

        # Optionales Icon
        if self.icon_data:
            icon_lbl = tk.Label(
                self,
                text=str(self.icon_data),
                bg=bg,
                fg=fg_muted,
                font=self.context.resolve_font(tokens.font_size_headline),
                anchor="w",
            )
            icon_lbl.pack(side="top", anchor="w", pady=(0, tokens.gap_compact))

        # Titel / Hauptnachricht
        if self.title_str:
            title_lbl = tk.Label(
                self,
                text=self.title_str,
                bg=bg,
                fg=fg,
                font=self.context.resolve_font(tokens.font_size_subtitle, "bold"),
                anchor="w",
                justify="left",
            )
            title_lbl.pack(side="top", fill="x", pady=(0, 2))

        # Beschreibung darunter
        if self.desc_str and self.desc_str != self.title_str:
            desc_lbl = tk.Label(
                self,
                text=self.desc_str,
                bg=bg,
                fg=fg_muted,
                font=self.context.resolve_font(tokens.font_size_body),
                anchor="w",
                justify="left",
                wraplength=260,
            )
            desc_lbl.pack(side="top", fill="x", pady=(0, tokens.gap_default))

        # Optionale Aktion zum Befüllen
        if self.action:
            caption, command, color_role = self.action
            btn_bg = self.context.resolve_color(color_role, self.context.resolve_color("accent"))
            self.action_button = tk.Button(
                self,
                text=caption,
                command=command,
                bg=btn_bg,
                fg="#FFFFFF" if color_role in ("accent", "confirm", "danger", "primary") else self.context.resolve_color("text_primary"),
                font=self.context.resolve_font(tokens.font_size_caption, "bold"),
                relief="flat",
                bd=0,
                padx=tokens.gap_default,
                pady=4,
                cursor="hand2",
                takefocus=True,
            )
            self.action_button.pack(side="top", anchor="w")


class BentoDivider(tk.Frame):
    """Subtile 1-px-Trennlinie zwischen Kartenabschnitten."""

    def __init__(self, master: tk.Widget, context: BentoContext, pady: int | tuple[int, int] = 6, height: int = 1, **kwargs):
        border_color = context.resolve_color("card_border")
        super().__init__(master, bg=border_color, height=height, bd=0, highlightthickness=0, **kwargs)
        if isinstance(pady, int):
            self.pack(fill="x", pady=pady)
        else:
            self.pack(fill="x", pady=pady)
