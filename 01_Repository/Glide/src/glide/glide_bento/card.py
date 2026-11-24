# SPDX-License-Identifier: MPL-2.0
"""BentoCard und Basiskomponenten (Header, Body, Footer).

Generische, anwendungsneutrale Kartenoberfläche auf Basis von Tkinter-Canvas und
eingebettetem inneren Frame. Nutzt glide_shell.custom_controls für Geometrie
und Größenabgleich (D100, D102).
"""
import tkinter as tk
from typing import Any, Callable

from glide_shell.custom_controls import bind_resize, rounded_rect_points
from .context import BentoContext
from .specs import BentoCardSpec
from .tokens import DEFAULT_TOKENS


class BentoHeader(tk.Frame):
    """Einheitlicher Kopfbereich einer Bento-Karte (Titel, Icon, Untertitel, Aktion)."""

    def __init__(
        self,
        master: tk.Widget,
        context: BentoContext,
        title: str | None = None,
        icon: Any | None = None,
        subtitle: str | None = None,
        action: tuple[str, Callable, str] | None = None,
        **kwargs,
    ):
        bg = context.resolve_color("card_bg")
        super().__init__(master, bg=bg, bd=0, highlightthickness=0, **kwargs)
        self.context = context
        self.title_text = title or ""
        self.subtitle_text = subtitle
        self.icon_data = icon
        self.action_spec = action

        self._icon_label: tk.Label | None = None
        self._title_label: tk.Label | None = None
        self._subtitle_label: tk.Label | None = None
        self._action_button: tk.Widget | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        bg = self.context.resolve_color("card_bg")
        fg = self.context.resolve_color("text_primary")
        fg_muted = self.context.resolve_color("text_muted")
        tokens = self.context.tokens

        # 1. Optionale rechte Aktion (zuerst nach rechts packen)
        if self.action_spec:
            caption, command, color_role = self.action_spec
            btn_bg = self.context.resolve_color(color_role, self.context.resolve_color("accent"))
            self._action_button = tk.Button(
                self,
                text=caption,
                command=command,
                bg=btn_bg,
                fg="#FFFFFF" if color_role in ("accent", "confirm", "danger") else fg,
                font=self.context.resolve_font(tokens.font_size_caption, "bold"),
                relief="flat",
                bd=0,
                padx=tokens.gap_compact,
                pady=2,
                cursor="hand2",
                takefocus=True,
            )
            self._action_button.pack(side="right", padx=(tokens.gap_compact, 0), pady=0)

        # 2. Textspalte links (Titel + optionaler Untertitel)
        text_col = tk.Frame(self, bg=bg, bd=0, highlightthickness=0)
        text_col.pack(side="left", fill="x", expand=True)

        title_row = tk.Frame(text_col, bg=bg, bd=0, highlightthickness=0)
        title_row.pack(side="top", fill="x")

        # 3. Optionales Icon vor dem Titel
        if self.icon_data:
            icon_symbol = self.context.resolve_icon(self.icon_data) if isinstance(self.icon_data, str) else self.icon_data
            self._icon_label = tk.Label(
                title_row,
                text=str(icon_symbol) if isinstance(icon_symbol, str) else "",
                bg=bg,
                fg=fg,
                font=self.context.resolve_font(tokens.font_size_subtitle, "bold"),
            )
            if not isinstance(icon_symbol, str):
                self._icon_label.configure(image=icon_symbol)
            self._icon_label.pack(side="left", padx=(0, tokens.header_icon_gap))

        # 4. Titel
        if self.title_text:
            display_title = self.title_text
            if len(display_title) > tokens.title_max_chars:
                display_title = display_title[: tokens.title_max_chars - 1] + "…"
            self._title_label = tk.Label(
                title_row,
                text=display_title,
                bg=bg,
                fg=fg,
                font=self.context.resolve_font(tokens.font_size_subtitle, "bold"),
                anchor="w",
            )
            self._title_label.pack(side="left", fill="x", expand=True)

        # 5. Optionaler Untertitel
        if self.subtitle_text:
            self._subtitle_label = tk.Label(
                text_col,
                text=self.subtitle_text,
                bg=bg,
                fg=fg_muted,
                font=self.context.resolve_font(tokens.font_size_caption),
                anchor="w",
            )
            self._subtitle_label.pack(side="top", fill="x", pady=(2, 0))

    def update_theme(self, context: BentoContext) -> None:
        """Aktualisiert Theme-Farben und Schriften."""
        self.context = context
        bg = context.resolve_color("card_bg")
        fg = context.resolve_color("text_primary")
        fg_muted = context.resolve_color("text_muted")
        tokens = context.tokens

        self.configure(bg=bg)
        for child in self.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=bg)
                for subchild in child.winfo_children():
                    if isinstance(subchild, tk.Frame):
                        subchild.configure(bg=bg)

        if self._icon_label:
            self._icon_label.configure(bg=bg, fg=fg, font=context.resolve_font(tokens.font_size_subtitle, "bold"))
        if self._title_label:
            self._title_label.configure(bg=bg, fg=fg, font=context.resolve_font(tokens.font_size_subtitle, "bold"))
        if self._subtitle_label:
            self._subtitle_label.configure(bg=bg, fg=fg_muted, font=context.resolve_font(tokens.font_size_caption))

    @property
    def title(self) -> str:
        return self.title_text

    @property
    def subtitle(self) -> str | None:
        return self.subtitle_text

    @property
    def icon(self) -> Any | None:
        return self.icon_data
        if self._action_button and self.action_spec:
            color_role = self.action_spec[2]
            btn_bg = context.resolve_color(color_role, context.resolve_color("accent"))
            self._action_button.configure(bg=btn_bg, fg="#FFFFFF" if color_role in ("accent", "confirm", "danger") else fg)


class BentoCard(tk.Canvas):
    """Generische, themebare Bento-Karte mit abgerundeten Ecken und innerem Inhaltsbereich."""

    def __init__(
        self,
        master: tk.Widget,
        context: BentoContext | None = None,
        spec: BentoCardSpec | None = None,
        title: str | None = None,
        icon: Any | None = None,
        subtitle: str | None = None,
        variant: str = "standard",
        auto_height: bool = True,
        command: Callable[[], None] | None = None,
        **kwargs,
    ):
        self.context = context or BentoContext()
        self.spec = spec or BentoCardSpec(
            key=kwargs.pop("key", "card"),
            title=title,
            subtitle=subtitle,
            icon=icon,
            variant=variant,
        )
        self.auto_height = auto_height
        self.command = command
        self._hovered = False
        self._focused = False

        tokens = self.context.tokens
        self.pad_x = kwargs.pop("inner_pad_x", tokens.card_padding_x if self.spec.variant != "compact" else tokens.card_compact_padding_x)
        self.pad_y = kwargs.pop("inner_pad_y", tokens.card_padding_y if self.spec.variant != "compact" else tokens.card_compact_padding_y)
        self.inner_pad_x = self.pad_x
        self.inner_pad_y = self.pad_y
        self.radius = kwargs.pop("radius", tokens.card_radius)
        self.fill_key = kwargs.pop("fill_key", "card")
        self.outline_key = kwargs.pop("outline_key", "line")
        kwargs.pop("register", None)
        kwargs.pop("natural_height", None)
        kwargs.pop("padding", None)

        bg = self.context.resolve_color("canvas_bg")
        card_bg = self.context.resolve_color("card_bg")
        self.bg_color = bg
        self.fill_color = card_bg
        self.outline_color = self.context.resolve_color("card_border")
        self.glass_mode = self.context.glass_mode
        self.glass_highlight = self.context.glass_highlight
        self.glass_shadow = self.context.glass_shadow
        self.glass_gradient = getattr(self.context, "glass_gradient", "")

        super().__init__(
            master,
            bg=bg,
            highlightthickness=0,
            bd=0,
            takefocus=bool(self.command),
            **kwargs,
        )

        # Innerer Container für Widgets
        self.inner = tk.Frame(self, bg=card_bg, bd=0, highlightthickness=0)
        self._window_id = self.create_window(self.pad_x, self.pad_y, anchor="nw", window=self.inner)

        # Standard-Strukturbereiche
        self._header: BentoHeader | None = None
        self._body: tk.Frame | None = None
        self._footer: tk.Frame | None = None
        self._auto_height_value: int | None = None

        # Wenn Spezifikation oder Argumente Titel/Icon mitgeben, Header aufbauen
        card_title = self.spec.title or title
        card_icon = self.spec.icon or icon
        card_subtitle = self.spec.subtitle or subtitle
        if card_title or card_icon or self.spec.heading_action:
            self.set_header(card_title, card_icon, card_subtitle, self.spec.heading_action)

        # Ereignis-Verdrahtung
        bind_resize(self, self._on_configure)
        if self.auto_height:
            self.inner.bind("<Configure>", self._sync_auto_height)

        if self.command:
            self._bind_interactions()

        self._draw_surface()

    @property
    def header(self) -> BentoHeader | None:
        return self._header

    @property
    def body(self) -> tk.Frame:
        """Liefert den primären Inhaltsbereich (erzeugt ihn bei Bedarf)."""
        if self._body is None:
            card_bg = self.context.resolve_color("card_bg")
            self._body = tk.Frame(self.inner, bg=card_bg, bd=0, highlightthickness=0)
            pady_top = self.context.tokens.header_gap if self._header else 0
            self._body.pack(side="top", fill="both", expand=True, pady=(pady_top, 0))
        return self._body

    @property
    def footer(self) -> tk.Frame:
        """Liefert den Fußbereich (erzeugt ihn bei Bedarf)."""
        if self._footer is None:
            card_bg = self.context.resolve_color("card_bg")
            self._footer = tk.Frame(self.inner, bg=card_bg, bd=0, highlightthickness=0)
            self._footer.pack(side="bottom", fill="x", pady=(self.context.tokens.footer_gap, 0))
        return self._footer

    def set_header(
        self,
        title: str | None = None,
        icon: Any | None = None,
        subtitle: str | None = None,
        action: tuple[str, Callable, str] | None = None,
    ) -> BentoHeader:
        """Konfiguriert oder ersetzt den Kartenkopf."""
        if self._header is not None:
            self._header.destroy()
        self._header = BentoHeader(
            self.inner,
            self.context,
            title=title,
            icon=icon,
            subtitle=subtitle,
            action=action,
        )
        self._header.pack(side="top", fill="x", pady=(0, self.context.tokens.header_gap))
        return self._header

    def _sync_auto_height(self, _event=None) -> None:
        """Passt die Canvas-Höhe an den Inhaltsbedarf des inneren Frames an."""
        if not self.auto_height:
            return
        try:
            needed = max(1, self.inner.winfo_reqheight() + self.pad_y * 2)
        except tk.TclError:
            return
        if needed == self._auto_height_value:
            return
        self._auto_height_value = needed
        try:
            self.configure(height=needed)
        except tk.TclError:
            pass

    def _on_configure(self, _event=None) -> None:
        """Reagiert auf Größenänderungen der Karte."""
        w = max(self.winfo_width(), self.pad_x * 2 + 2)
        h = max(self.winfo_height(), self.pad_y * 2 + 2)
        inner_w = max(1, w - self.pad_x * 2)

        self.coords(self._window_id, self.pad_x, self.pad_y)
        if self.auto_height:
            self.itemconfigure(self._window_id, width=inner_w, height=0)
            self._sync_auto_height()
        else:
            self.itemconfigure(self._window_id, width=inner_w, height=max(1, h - self.pad_y * 2))
        self._draw_surface()

    def _draw_surface(self) -> None:
        """Zeichnet den abgerundeten Hintergrund, Rahmen und Glass-Effekte."""
        self.delete("surface")
        w = max(self.winfo_width(), 4)
        h = max(self.winfo_height(), 4)

        card_bg = self.context.resolve_color("card_bg")
        border = self.context.resolve_color("card_border")
        tokens = self.context.tokens

        # Aktive Hervorhebung bei Fokus oder Hover
        if self._focused:
            border = self.context.resolve_color("focus")
        elif self._hovered and self.command:
            card_bg = self.context.resolve_color("hover", card_bg)

        # Optionaler Glass-Modus
        if self.context.glass_mode and self.context.glass_shadow:
            self.create_polygon(
                rounded_rect_points(1, 2, w - 1, h, self.radius),
                smooth=True,
                splinesteps=24,
                fill="",
                outline=self.context.glass_shadow,
                width=2,
                tags=("surface",),
            )

        # Hauptpolygon (Füllung und Kontur)
        outline_width = tokens.focus_width if self._focused else tokens.border_width
        self.create_polygon(
            rounded_rect_points(1, 1, w - 1, h - 1, self.radius),
            smooth=True,
            splinesteps=24,
            fill=card_bg,
            outline=border,
            width=outline_width,
            tags=("surface",),
        )

    def _bind_interactions(self) -> None:
        """Verknüpft Maus- und Tastaturinteraktionen für anklickbare Karten."""
        def on_enter(_=None):
            self._hovered = True
            self._draw_surface()

        def on_leave(_=None):
            self._hovered = False
            self._draw_surface()

        def on_click(_=None):
            if self.command:
                self.command()

        def on_focus_in(_=None):
            self._focused = True
            self._draw_surface()

        def on_focus_out(_=None):
            self._focused = False
            self._draw_surface()

        self._on_enter = on_enter
        self._on_leave = on_leave
        self._on_click = on_click
        self._on_focus_in = on_focus_in
        self._on_focus_out = on_focus_out

        for target in (self, self.inner):
            target.bind("<Enter>", on_enter)
            target.bind("<Leave>", on_leave)
            target.bind("<Button-1>", on_click)

        self.bind("<FocusIn>", on_focus_in)
        self.bind("<FocusOut>", on_focus_out)
        self.bind("<Return>", on_click)
        self.bind("<space>", on_click)

    def _draw(self) -> None:
        """Alias für _draw_surface zur Kompatibilität mit DeferredDrawCanvas und Themesync."""
        self._draw_surface()

    def set_theme(self, context_or_bg: Any, fill_color: Optional[str] = None, outline_color: Optional[str] = None, **options: Any) -> None:
        """Aktualisiert das Theme der Karte und ihrer Unterkomponenten.

        Unterstützt sowohl ein BentoContext-Objekt als auch die klassische Signatur
        (bg_color, fill_color, outline_color, **options) für nahtlose Rückwärtskompatibilität.
        """
        if isinstance(context_or_bg, BentoContext):
            self.context = context_or_bg
            self.bg_color = self.context.resolve_color("canvas_bg")
            self.fill_color = self.context.resolve_color("card_bg")
            self.outline_color = self.context.resolve_color("card_border")
        else:
            self.bg_color = str(context_or_bg)
            if fill_color is not None:
                self.fill_color = str(fill_color)
            if outline_color is not None:
                self.outline_color = str(outline_color)
            if isinstance(self.context.theme, dict):
                self.context.theme["bg"] = self.bg_color
                self.context.theme["card"] = self.fill_color
                self.context.theme["line"] = self.outline_color

        self.configure(bg=self.bg_color)
        self.inner.configure(bg=self.fill_color)
        if self._header:
            self._header.update_theme(self.context)
        if self._body:
            self._body.configure(bg=self.fill_color)
        if self._footer:
            self._footer.configure(bg=self.fill_color)
        self._draw_surface()
