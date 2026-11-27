# SPDX-License-Identifier: MPL-2.0
"""BentoContext – Host-Kontext für Themes, Schriften, Icons und Zeitgeber.

Der Kontext entkoppelt das Bento-System vollständig von Glides Anwendungsfachlogik.
Er stellt Komponenten alle visuellen Ressourcen (Farben, Schriften, Icons,
Tooltips, Zeitgeber) über Provider-Funktionen bereit (D100).
"""
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping
from .tokens import BentoTokens, DEFAULT_TOKENS

# Neutrale Standardfarben für den Fallback ohne aktiven Host
_FALLBACK_THEME = {
    "card_bg": "#FFFFFF",
    "canvas_bg": "#F5F5F7",
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
    "line": "#D1D1D6",
    "input": "#E5E5EA",
}


def _default_font_provider(size: int, weight: str = "normal", slant: str = "roman") -> Any:
    """Neutraler Fallback für Schriftarten ohne Host."""
    wt = "bold" if weight in ("bold", "semibold") else "normal"
    return ("Helvetica", size, wt)


def _default_icon_provider(key: str) -> str:
    """Neutraler Fallback für Icons: gibt ein passendes Unicode-Symbol oder den Schlüssel zurück."""
    _FALLBACK_ICONS = {
        "check": "✓",
        "task_open": "○",
        "pinned": "📌",
        "drawing": "🎨",
        "gallery": "🖼",
        "list": "📋",
        "folder": "📁",
        "calendar": "📅",
        "today": "☀️",
        "focus": "🎯",
        "clock": "🕒",
        "more": "⋯",
        "add": "+",
        "arrow_right": "→",
        "arrow_down": "↓",
    }
    return _FALLBACK_ICONS.get(key, key)


@dataclass(slots=True)
class BentoContext:
    """Verwaltet den Host-Kontext für eine Bento-Komposition."""

    theme: Mapping[str, str] = field(default_factory=lambda: dict(_FALLBACK_THEME))
    font_provider: Callable[[int, str], Any] = _default_font_provider
    icon_provider: Callable[[str], Any] = _default_icon_provider
    tokens: BentoTokens = DEFAULT_TOKENS
    tooltip_installer: Callable[[Any, Any], None] | None = None
    after_scope: Any | None = None
    glass_mode: bool = False
    glass_highlight: str | None = None
    glass_shadow: str | None = None
    glass_gradient: str | None = None
    custom: dict[str, Any] = field(default_factory=dict)
    # Bento 0.2.0, Variante C: Der Host kann Theme und Tokens als Provider
    # übergeben; ``refresh_from_host`` liest sie nach Design-, Schrift- oder
    # Themenwechsel neu, ohne den Kontext (und die Karten, die ihn halten)
    # auszutauschen.
    theme_provider: Callable[[], Mapping[str, str]] | None = None
    token_provider: Callable[[], Mapping[str, Any]] | None = None
    # Knöpfe des Hosts (master, text, command, color_role) -> Widget mit pack().
    button_factory: Callable[[Any, str, Callable[[], Any], str], Any] | None = None

    def make_button(self, master: Any, text: str, command: Callable[[], Any], color_role: str = "accent") -> Any:
        """Knopf über die Host-Fabrik oder als neutraler Tk-Knopf (Fallback ohne Host)."""
        if self.button_factory is not None:
            return self.button_factory(master, text, command, color_role)
        import tkinter as tk
        tokens = self.tokens
        highlight = color_role in ("accent", "confirm", "danger", "primary")
        return tk.Button(
            master, text=text, command=command,
            bg=self.resolve_color(color_role, self.resolve_color("accent" if highlight else "button_bg")),
            fg="#FFFFFF" if highlight else self.resolve_color("text_primary"),
            font=self.resolve_font(tokens.font_size_small, "bold" if highlight else "normal"),
            relief="flat", bd=0, padx=tokens.gap_default, pady=4, cursor="hand2", takefocus=True,
        )

    @classmethod
    def for_host(cls, **kwargs) -> "BentoContext":
        """Kontext mit Host-Providern anlegen und sofort aus ihnen befüllen."""
        context = cls(**kwargs)
        return context.refresh_from_host()

    def refresh_from_host(self, **values) -> "BentoContext":
        """Theme und Tokens aus den Host-Providern neu lesen (in place).

        Zusätzliche Schlüsselwörter (z. B. ``glass_mode``) werden direkt
        übernommen. Ohne Provider bleiben Fallback-Theme und Tokens stehen.
        """
        if self.theme_provider is not None:
            theme = self.theme_provider()
            if theme:
                self.theme = theme
        if self.token_provider is not None:
            self.tokens = BentoTokens.from_host(self.token_provider())
        for name, value in values.items():
            if name not in self.__slots__:
                raise AttributeError(f"BentoContext has no field {name!r}")
            setattr(self, name, value)
        return self

    def resolve_color(self, role: str, fallback: str | None = None) -> str:
        """Löst eine semantische Farbrolle gegen das Host-Theme auf."""
        # 1. Direkte Suche im Theme
        if role in self.theme:
            return self.theme[role]
        # 2. Übliche Rollen-Synonyme zwischen Glide und Bento
        _ALIASES = {
            "card_bg": "card",
            "canvas_bg": "bg",
            "card_border": "line",
            "text_primary": "text",
            "text_secondary": "muted",
            "text_muted": "muted",
            "accent": "ui_accent",
            "button_bg": "card",
            "button_fg": "text",
        }
        alias = _ALIASES.get(role)
        if alias and alias in self.theme:
            return self.theme[alias]
        if fallback is not None:
            return fallback
        return _FALLBACK_THEME.get(role, "#000000")

    def resolve_font(self, size: int, weight: str = "normal", slant: str = "roman") -> Any:
        """Löst eine Schriftart über den font_provider auf."""
        try:
            return self.font_provider(size, weight)
        except Exception:  # noqa: BLE001 – Fremdhost-Provider dürfen Bento nicht stoppen
            return _default_font_provider(size, weight)

    def resolve_icon(self, key: str) -> Any:
        """Löst ein Icon über den icon_provider auf."""
        return self.icon_provider(key)

    def attach_tooltip(self, widget: Any, text_or_callable: Any) -> None:
        """Verknüpft einen Tooltip mit einem Widget, sofern ein Installer übergeben wurde."""
        if self.tooltip_installer is not None and widget is not None:
            self.tooltip_installer(widget, text_or_callable)

    def clone_with(self, **kwargs) -> "BentoContext":
        """Erzeugt eine Kopie des Kontexts mit partiellen Überschreibungen."""
        current = {
            "theme": self.theme,
            "font_provider": self.font_provider,
            "icon_provider": self.icon_provider,
            "tokens": self.tokens,
            "tooltip_installer": self.tooltip_installer,
            "after_scope": self.after_scope,
            "glass_mode": self.glass_mode,
            "glass_highlight": self.glass_highlight,
            "glass_shadow": self.glass_shadow,
            "glass_gradient": self.glass_gradient,
            "custom": dict(self.custom),
            "theme_provider": self.theme_provider,
            "token_provider": self.token_provider,
            "button_factory": self.button_factory,
        }
        current.update(kwargs)
        return BentoContext(**current)
