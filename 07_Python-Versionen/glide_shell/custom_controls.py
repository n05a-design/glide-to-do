# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 4: Wiederverwendbare Tk-/Canvas-Bedienelemente ohne App-Bindung.

Enthält CanvasLabel, GlideCheckbutton, GlideRadiobutton, GlideListbox,
GlideScale, ThemedAutoScrollbar, bind_resize, paint_canvas_backdrop und
rounded_rect_points.

Importregel (D86): Nur Standardbibliothek und tkinter; keine Abhängigkeit
vom App-Host (Abhängigkeitsrichtung Host -> Shell -> Tk).
"""
from __future__ import annotations

import sys
import tkinter as tk
from tkinter import font as tkfont

_FONT_PROVIDER = None
_INK_PROVIDER = None
_BACKDROP_PAINTER = None


def set_font_provider(provider):
    """Registriert einen optionalen Schriftenauflöser des Hosts: provider(size, *styles)."""
    global _FONT_PROVIDER
    _FONT_PROVIDER = provider


def set_ink_provider(provider):
    """Registriert einen optionalen Glyphenmetrik-Rechner des Hosts: provider(label, font, text, width)."""
    global _INK_PROVIDER
    _INK_PROVIDER = provider


def set_backdrop_painter(painter):
    """Registriert einen optionalen Hintergrundverlauf-Maler des Hosts: painter(canvas)."""
    global _BACKDROP_PAINTER
    _BACKDROP_PAINTER = painter


def _default_font(size=10, widget=None):
    provider = getattr(widget, "_font_provider", None) if widget is not None else None
    if not callable(provider) and widget is not None:
        try:
            provider = getattr(widget.winfo_toplevel(), "_font_provider", None)
        except Exception:
            pass
    if not callable(provider):
        provider = _FONT_PROVIDER
    if callable(provider):
        try:
            return provider(size)
        except Exception:
            pass
    return ("TkDefaultFont", size)


def _font_obj(root, font):
    root = root or getattr(tk, "_default_root", None)
    if isinstance(font, tkfont.Font):
        return font
    return tkfont.Font(root=root, font=font)


def rounded_rect_points(x1, y1, x2, y2, radius):
    """Stützpunkte eines abgerundeten Rechtecks für create_polygon (smooth=True)."""
    return [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]


def bind_resize(widget, callback, add=None):
    """Ruft callback(event) nur, wenn sich die Größe des Widgets geändert hat."""
    def bei_groesse(event):
        if getattr(event, "widget", None) is not widget:
            return None
        groesse = (event.width, event.height)
        if getattr(widget, "_resize_seen", None) == groesse:
            return None
        widget._resize_seen = groesse
        return callback(event)

    return widget.bind("<Configure>", bei_groesse, add=add)


def paint_canvas_backdrop(canvas):
    """Legt den Hintergrundverlauf als unterste Ebene in eine Canvas-Fläche."""
    painter = getattr(canvas, "_backdrop_painter", None)
    if not callable(painter):
        try:
            painter = getattr(canvas.winfo_toplevel(), "_backdrop_painter", None)
        except Exception:
            pass
    if not callable(painter):
        painter = _BACKDROP_PAINTER
    if callable(painter):
        try:
            return painter(canvas)
        except Exception:
            pass
    try:
        canvas.delete("backdrop")
        info = getattr(canvas, "_backdrop", None)
        if not info:
            return
        for bild, x, y in info:
            canvas.create_image(x, y, image=bild, anchor="nw", tags=("backdrop",))
        canvas.tag_lower("backdrop")
    except tk.TclError:
        pass


class CanvasLabel(tk.Canvas):
    """Beschriftung ohne eigene Fläche: Text auf einer Canvas statt in einem Label."""

    LABEL_INSET_X = 1
    LABEL_INSET_Y = 2
    TEXT_OPTIONS = ("text", "font", "fg", "foreground", "anchor", "justify", "wraplength", "padx", "pady")

    def __init__(self, master, text="", font=None, fg=None, foreground=None, bg=None, background=None,
                 anchor="center", justify="left", wraplength=0, padx=1, pady=1, cursor="", takefocus=0,
                 inset_y=None, fit_ink=False, **kwargs):
        self._fit_ink = bool(fit_ink)
        if inset_y is not None:
            self.LABEL_INSET_Y = max(0, int(inset_y))
        farbe = bg or background
        if farbe is None:
            try:
                farbe = master.cget("bg")
            except tk.TclError:
                farbe = "#FFFFFF"
        optionen = {"highlightthickness": 0, "bd": 0, "bg": farbe, "cursor": cursor, "takefocus": takefocus,
                    "width": 1, "height": 1}
        optionen.update(kwargs)
        super().__init__(master, **optionen)
        self._opts = {"text": str(text), "font": font or "TkDefaultFont", "fg": fg or foreground or "#000000",
                      "anchor": anchor, "justify": justify, "wraplength": wraplength, "padx": padx, "pady": pady}
        self._halo = None
        self._fg_override = None
        self._text_ids = []
        self._required = (1, 1)
        self._text_w = 0
        self._text_h = 0
        self.bind("<Configure>", lambda _event: self._place_text(), add="+")
        self._render()

    def configure(self, cnf=None, **kwargs):
        if isinstance(cnf, dict):
            kwargs = {**cnf, **kwargs}
        elif isinstance(cnf, str) and not kwargs:
            if cnf in self.TEXT_OPTIONS:
                return (cnf, cnf, cnf, None, self.cget(cnf))
            return super().configure(cnf)
        eigene = {key: kwargs.pop(key) for key in list(kwargs) if key in self.TEXT_OPTIONS}
        if "background" in kwargs:
            kwargs["bg"] = kwargs.pop("background")
        if kwargs:
            super().configure(**kwargs)
        if eigene:
            if "foreground" in eigene:
                eigene["fg"] = eigene.pop("foreground")
            if "text" in eigene:
                eigene["text"] = str(eigene["text"])
            self._opts.update(eigene)
            self._render()
        return None

    config = configure

    def cget(self, key):
        if key == "foreground":
            key = "fg"
        if key in self._opts:
            return self._opts[key]
        if key == "background":
            key = "bg"
        return super().cget(key)

    def __getitem__(self, key):
        return self.cget(key)

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def keys(self):
        opts = set(super().keys())
        opts.update(self._opts.keys())
        opts.update(("text", "font", "fg", "foreground", "bg", "background", "anchor", "justify", "wraplength", "padx", "pady"))
        return sorted(opts)

    def set_halo(self, farbe):
        """Farbe einer dezenten Glas-Pille hinter dem Text – oder None."""
        if farbe != self._halo:
            self._halo = farbe
            self._render()

    def set_contrast_fg(self, farbe):
        """Schriftfarbe für den Verlauf darunter – oder None für die Designfarbe."""
        if farbe != self._fg_override:
            self._fg_override = farbe
            try:
                self.itemconfigure("text", fill=farbe or self._opts["fg"])
            except tk.TclError:
                pass

    def text_size(self):
        """(Breite, Höhe) des Texts einschließlich Innenabstand."""
        return self._required

    def _render(self):
        self.delete("text")
        o = self._opts
        breite = int(float(o["wraplength"] or 0))
        gemeinsam = {"text": o["text"], "font": o["font"], "justify": o["justify"], "anchor": "nw",
                     "tags": ("text",)}
        if breite > 0:
            gemeinsam["width"] = breite
        self._text_ids = []
        haupt = self.create_text(0, 0, fill=self._fg_override or o["fg"], **gemeinsam)
        self._text_ids.append((haupt, 0, 0))
        box = self.bbox(haupt) or (0, 0, 0, 0)
        padx = int(float(o["padx"] or 0)) + self.LABEL_INSET_X
        pady = int(float(o["pady"] or 0)) + self.LABEL_INSET_Y
        self._text_w, self._text_h = box[2] - box[0], box[3] - box[1]
        self._text_ink_top = 0
        if self._fit_ink:
            provider = getattr(self, "_ink_provider", None)
            if not callable(provider):
                try:
                    provider = getattr(self.winfo_toplevel(), "_ink_provider", None)
                except Exception:
                    pass
            if not callable(provider):
                provider = _INK_PROVIDER
            if callable(provider):
                try:
                    ink = provider(self, o["font"], o["text"], breite)
                    if ink is not None:
                        self._text_ink_top, self._text_h = ink
                        self._text_ids = [(haupt, 0, -self._text_ink_top)]
                except Exception:
                    pass
        self._required = (self._text_w + 2 * padx, self._text_h + 2 * pady)
        super().configure(width=max(1, self._required[0]), height=max(1, self._required[1]))
        self._place_text()
        paint_canvas_backdrop(self)

    def _place_text(self):
        o = self._opts
        breite = self.winfo_width() if self.winfo_width() > 1 else self._required[0]
        hoehe = self.winfo_height() if self.winfo_height() > 1 else self._required[1]
        padx = int(float(o["padx"] or 0)) + self.LABEL_INSET_X
        pady = int(float(o["pady"] or 0)) + self.LABEL_INSET_Y
        anker = str(o["anchor"] or "center")
        if "w" in anker:
            x = padx
        elif "e" in anker:
            x = breite - padx - self._text_w
        else:
            x = (breite - self._text_w) / 2
        if anker.startswith("n"):
            y = pady
        elif anker.startswith("s"):
            y = hoehe - pady - self._text_h
        else:
            y = (hoehe - self._text_h) / 2
        for kennung, dx, dy in self._text_ids:
            self.coords(kennung, x + dx, y + dy)
        self.delete("pill")
        if self._halo:
            rand_x, rand_y = 6, 2
            self.create_polygon(
                rounded_rect_points(x - rand_x, y - rand_y, x + self._text_w + rand_x, y + self._text_h + rand_y, 8),
                smooth=True, splinesteps=16, fill=self._halo, outline="", tags=("pill", "text"))
            self.tag_lower("pill", "text")


class GlideCheckbutton(tk.Canvas):
    """Themebares Auswahlkästchen auf Canvas-Grundlage ohne native Systemkästchen."""

    BOX_SIZE = 16
    BOX_GAP = 8
    PAD_X = 4
    PAD_Y = 3

    def __init__(self, master, **kwargs):
        self._variable = kwargs.pop("variable", None)
        self._command = kwargs.pop("command", None)
        self._onvalue = kwargs.pop("onvalue", True)
        self._offvalue = kwargs.pop("offvalue", False)
        name = kwargs.pop("name", None)
        cursor = kwargs.pop("cursor", "hand2")
        takefocus = kwargs.pop("takefocus", 1)
        bg = kwargs.pop("bg", kwargs.pop("background", None))
        if bg is None:
            try:
                bg = master.cget("bg")
            except Exception:
                bg = "#1e1e1e"
        self._init_opts(kwargs, bg)
        init_kw = dict(
            bg=bg, bd=0, highlightthickness=self._highlightthickness,
            highlightbackground=self._highlightbackground, highlightcolor=self._highlightcolor,
            cursor=cursor, takefocus=takefocus,
        )
        if name is not None:
            init_kw["name"] = name
        super().__init__(master, **init_kw)
        self._trace_id = None
        self._focused = False
        self._hovered = False
        self._required = (1, 1)
        self._attach_variable(self._variable)
        self._bind_events()
        self._render()

    def _init_opts(self, kwargs, bg):
        self._opts = {
            "text": str(kwargs.pop("text", "") or ""),
            "font": kwargs.pop("font", None) or _default_font(10, widget=self),
            "bg": bg,
            "fg": kwargs.pop("fg", kwargs.pop("foreground", "#e5e5e5")),
            "activebackground": kwargs.pop("activebackground", bg),
            "activeforeground": kwargs.pop("activeforeground", "#e5e5e5"),
            "selectcolor": kwargs.pop("selectcolor", bg),
            "disabledforeground": kwargs.pop("disabledforeground", "#888888"),
            "anchor": kwargs.pop("anchor", "w"),
            "justify": kwargs.pop("justify", "left"),
            "wraplength": kwargs.pop("wraplength", 0),
            "padx": kwargs.pop("padx", self.PAD_X),
            "pady": kwargs.pop("pady", self.PAD_Y),
            "state": kwargs.pop("state", "normal"),
            "relief": kwargs.pop("relief", "flat"),
            "bd": kwargs.pop("bd", kwargs.pop("borderwidth", 0)),
        }
        self._highlightthickness = kwargs.pop("highlightthickness", 0)
        self._highlightbackground = kwargs.pop("highlightbackground", bg)
        self._highlightcolor = kwargs.pop("highlightcolor", self._opts["fg"])
        for rest in list(kwargs):
            self._opts[rest] = kwargs.pop(rest)

    def _bind_events(self):
        self.bind("<Button-1>", self._on_click)
        self.bind("<space>", self._on_key_toggle)
        self.bind("<Return>", self._on_key_toggle)
        self.bind("<FocusIn>", self._on_focus_in, add="+")
        self.bind("<FocusOut>", self._on_focus_out, add="+")
        self.bind("<Enter>", self._on_enter, add="+")
        self.bind("<Leave>", self._on_leave, add="+")
        self.bind("<Configure>", self._on_configure, add="+")
        self.bind("<Destroy>", self._on_destroy, add="+")

    def _attach_variable(self, variable):
        if self._variable is not None and self._trace_id is not None:
            try:
                self._variable.trace_remove("write", self._trace_id)
            except Exception:
                pass
        self._variable = variable
        self._trace_id = None
        if variable is not None and hasattr(variable, "trace_add"):
            try:
                self._trace_id = variable.trace_add("write", lambda *_: self._safe_render())
            except Exception:
                self._trace_id = None

    def _on_destroy(self, event):
        if event.widget is self:
            self._attach_variable(None)

    def _safe_render(self):
        if getattr(self, "_rendering", False):
            return
        self._rendering = True
        try:
            if self.winfo_exists():
                self._render()
        except tk.TclError:
            pass
        finally:
            self._rendering = False

    def _is_checked(self):
        if self._variable is None:
            return bool(getattr(self, "_internal_checked", False))
        try:
            val = self._variable.get()
        except Exception:
            return False
        if isinstance(self._onvalue, bool):
            return bool(val) is self._onvalue
        return val == self._onvalue or bool(val)

    def select(self):
        if self._variable is not None:
            try:
                self._variable.set(self._onvalue)
            except Exception:
                pass
        else:
            self._internal_checked = True
        self._safe_render()

    def deselect(self):
        if self._variable is not None:
            try:
                self._variable.set(self._offvalue)
            except Exception:
                pass
        else:
            self._internal_checked = False
        self._safe_render()

    def toggle(self):
        if self._is_checked():
            self.deselect()
        else:
            self.select()

    def invoke(self):
        if str(self._opts.get("state", "normal")) == "disabled":
            return "break"
        if getattr(self, "_accessible_step_index", None) is not None and callable(self._command):
            return self._command()
        self.toggle()
        if callable(self._command):
            return self._command()
        return None

    def _on_click(self, _event=None):
        if str(self._opts.get("state", "normal")) == "disabled":
            return "break"
        try:
            self.focus_set()
        except tk.TclError:
            pass
        self.invoke()
        return "break"

    def _on_key_toggle(self, _event=None):
        if str(self._opts.get("state", "normal")) == "disabled":
            return "break"
        if getattr(self, "_accessible_step_index", None) is not None:
            return None
        self.invoke()
        return "break"

    def _on_focus_in(self, _event=None):
        self._focused = True
        self._safe_render()

    def _on_focus_out(self, _event=None):
        self._focused = False
        self._safe_render()

    def _on_enter(self, _event=None):
        self._hovered = True
        self._safe_render()

    def _on_leave(self, _event=None):
        self._hovered = False
        self._safe_render()

    def _on_configure(self, event=None):
        if event is not None:
            w, h = getattr(event, "width", None), getattr(event, "height", None)
            if w is not None and h is not None and w == getattr(self, "_last_conf_w", None) and h == getattr(self, "_last_conf_h", None):
                return
            self._last_conf_w = w
            self._last_conf_h = h
        self._safe_render()

    def configure(self, cnf=None, **kwargs):
        werte = dict(cnf or {}, **kwargs)
        if not werte:
            return super().configure()
        canvas_kw = {}
        for k in ("highlightthickness", "highlightbackground", "highlightcolor", "cursor", "takefocus"):
            if k in werte:
                canvas_kw[k] = werte.pop(k)
        if "background" in werte:
            werte["bg"] = werte.pop("background")
        if "foreground" in werte:
            werte["fg"] = werte.pop("foreground")
        if "variable" in werte:
            self._attach_variable(werte.pop("variable"))
        if "command" in werte:
            self._command = werte.pop("command")
        if "onvalue" in werte:
            self._onvalue = werte.pop("onvalue")
        if "offvalue" in werte:
            self._offvalue = werte.pop("offvalue")
        if "bg" in werte:
            canvas_kw["bg"] = werte["bg"]
            if "highlightbackground" not in canvas_kw and int(float(super().cget("highlightthickness") or 0)) == 0:
                canvas_kw["highlightbackground"] = werte["bg"]
        changed = any(self._opts.get(k) != v for k, v in werte.items()) or bool(canvas_kw)
        self._opts.update(werte)
        if canvas_kw:
            super().configure(**canvas_kw)
        if changed:
            self._safe_render()

    config = configure

    def cget(self, key):
        if key == "background":
            key = "bg"
        elif key == "foreground":
            key = "fg"
        if key == "variable":
            return str(self._variable) if self._variable is not None else ""
        if key == "command":
            return self._command
        if key == "onvalue":
            return self._onvalue
        if key == "offvalue":
            return self._offvalue
        if key in self._opts:
            return self._opts[key]
        return super().cget(key)

    def __getitem__(self, key):
        return self.cget(key)

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def keys(self):
        opts = set(super().keys())
        opts.update(self._opts.keys())
        opts.update(("text", "variable", "command", "onvalue", "offvalue", "font", "state", "justify", "wraplength", "padx", "pady"))
        return sorted(opts)

    def _render(self):
        self.delete("all")
        o = self._opts
        disabled = str(o.get("state", "normal")) == "disabled"
        checked = self._is_checked()
        padx = max(0, int(float(o.get("padx") or 0)))
        pady = max(0, int(float(o.get("pady") or 0)))
        box_s = self.BOX_SIZE
        gap = self.BOX_GAP if o.get("text") else 0
        wrap = int(float(o.get("wraplength") or 0))
        text_wrap = max(40, wrap - box_s - gap - 2 * padx) if wrap > 0 else 0
        fg = o["disabledforeground"] if disabled else o["fg"]
        text_kw = {
            "text": str(o.get("text") or ""),
            "font": o["font"],
            "fill": fg,
            "anchor": "nw",
            "justify": o.get("justify", "left"),
            "tags": ("text",),
        }
        if text_wrap > 0:
            text_kw["width"] = text_wrap
        tid = self.create_text(padx + box_s + gap, pady, **text_kw)
        tbox = self.bbox(tid) or (padx + box_s + gap, pady, padx + box_s + gap, pady + box_s)
        tw = max(0, tbox[2] - tbox[0])
        th = max(box_s, tbox[3] - tbox[1])
        req_w = padx * 2 + box_s + gap + tw + 4
        req_h = pady * 2 + max(box_s, th)
        if (req_w, req_h) != self._required:
            self._required = (req_w, req_h)
            self._last_conf_w = max(1, req_w)
            self._last_conf_h = max(1, req_h)
            super().configure(width=max(1, req_w), height=max(1, req_h))
        h = self.winfo_height() if self.winfo_height() > 1 else req_h
        if "\n" in str(o.get("text") or "") or th > box_s + 6:
            by = pady + 2
            ty = pady
        else:
            by = max(pady, (h - box_s) / 2)
            ty = max(pady, (h - (tbox[3] - tbox[1])) / 2)
        self.coords(tid, padx + box_s + gap, ty)
        self._draw_box(padx, by, box_s, fg, checked, disabled)
        paint_canvas_backdrop(self)

    def _draw_box(self, bx, by, box_s, fg, checked, disabled):
        o = self._opts
        box_fill = o.get("selectcolor") or o["bg"]
        border_col = fg if (checked or self._focused or self._hovered) and not disabled else o.get("disabledforeground", fg)
        self.create_polygon(
            rounded_rect_points(bx, by, bx + box_s, by + box_s, 4),
            smooth=True, splinesteps=12, fill=box_fill, outline=border_col, width=1.4 if self._focused else 1,
            tags=("box",),
        )
        if checked:
            self.create_line(
                bx + 3.5, by + box_s * 0.52,
                bx + box_s * 0.44, by + box_s - 4,
                bx + box_s - 3.2, by + 4,
                fill=fg, width=2, capstyle="round", joinstyle="round", tags=("check",),
            )


class GlideRadiobutton(GlideCheckbutton):
    """Themebarer Radioschalter auf Canvas-Grundlage."""

    def __init__(self, master, **kwargs):
        self._value = kwargs.pop("value", "")
        super().__init__(master, **kwargs)

    def _is_checked(self):
        if self._variable is None:
            return False
        try:
            return self._variable.get() == self._value
        except Exception:
            return False

    def select(self):
        if self._variable is not None:
            try:
                self._variable.set(self._value)
            except Exception:
                pass
        self._safe_render()

    def deselect(self):
        pass

    def toggle(self):
        self.select()

    def configure(self, cnf=None, **kwargs):
        werte = dict(cnf or {}, **kwargs)
        if "value" in werte:
            self._value = werte.pop("value")
        return super().configure(werte)

    config = configure

    def cget(self, key):
        if key == "value":
            return self._value
        return super().cget(key)

    def keys(self):
        opts = set(super().keys())
        opts.add("value")
        return sorted(opts)

    def _render(self):
        super()._render()
        self.delete("box", "check")
        o = self._opts
        disabled = str(o.get("state", "normal")) == "disabled"
        checked = self._is_checked()
        padx = max(0, int(float(o.get("padx") or 0)))
        pady = max(0, int(float(o.get("pady") or 0)))
        box_s = self.BOX_SIZE
        h = self.winfo_height() if self.winfo_height() > 1 else self._required[1]
        by = max(pady, (h - box_s) / 2)
        bx = padx
        fg = o["disabledforeground"] if disabled else o["fg"]
        box_fill = o.get("selectcolor") or o["bg"]
        border_col = fg if (checked or self._focused or self._hovered) and not disabled else o.get("disabledforeground", fg)
        self.create_oval(
            bx, by, bx + box_s, by + box_s,
            fill=box_fill, outline=border_col, width=1.4 if self._focused else 1, tags=("box",),
        )
        if checked:
            inset = 4
            self.create_oval(
                bx + inset, by + inset, bx + box_s - inset, by + box_s - inset,
                fill=fg, outline="", tags=("check",),
            )


class GlideListbox(tk.Canvas):
    """Themebare Listenauswahl auf Canvas-Grundlage mit kompatibler Listbox-Schnittstelle."""

    ROW_PAD_X = 6
    ROW_PAD_Y = 3

    def __init__(self, master, **kwargs):
        self._height_rows = int(kwargs.pop("height", 6) or 6)
        self._width_chars = int(kwargs.pop("width", 36) or 36)
        name = kwargs.pop("name", None)
        bg = kwargs.pop("bg", kwargs.pop("background", "#1e1e1e"))
        self._opts = {
            "bg": bg,
            "fg": kwargs.pop("fg", kwargs.pop("foreground", "#e5e5e5")),
            "selectbackground": kwargs.pop("selectbackground", "#335588"),
            "selectforeground": kwargs.pop("selectforeground", "#ffffff"),
            "font": kwargs.pop("font", None) or _default_font(10, widget=self),
            "activestyle": kwargs.pop("activestyle", "none"),
            "relief": kwargs.pop("relief", "flat"),
            "bd": kwargs.pop("bd", kwargs.pop("borderwidth", 0)),
            "state": kwargs.pop("state", "normal"),
            "height": self._height_rows,
            "width": self._width_chars,
        }
        highlightthickness = kwargs.pop("highlightthickness", 0)
        takefocus = kwargs.pop("takefocus", 1)
        for k in list(kwargs):
            self._opts[k] = kwargs.pop(k)
        self._items = []
        self._item_styles = {}
        self._selected = set()
        self._active_index = 0
        self._top_index = 0
        self._yscrollcommand = self._opts.pop("yscrollcommand", None)
        row_h = self._row_height()
        char_w = self._char_width()
        init_kw = dict(
            bg=bg, bd=0, highlightthickness=highlightthickness, takefocus=takefocus,
            width=max(60, self._width_chars * char_w),
            height=max(24, self._height_rows * row_h),
        )
        if name is not None:
            init_kw["name"] = name
        super().__init__(master, **init_kw)
        self.bind("<Button-1>", self._on_click)
        self.bind("<Up>", lambda _e: self._move_selection(-1))
        self.bind("<Down>", lambda _e: self._move_selection(1))
        self.bind("<Home>", lambda _e: self._jump_selection(0))
        self.bind("<End>", lambda _e: self._jump_selection(max(0, len(self._items) - 1)))
        self.bind("<Configure>", self._on_configure, add="+")
        self._render()

    def _on_configure(self, event=None):
        if event is not None:
            w, h = getattr(event, "width", None), getattr(event, "height", None)
            if w is not None and h is not None and w == getattr(self, "_last_conf_w", None) and h == getattr(self, "_last_conf_h", None):
                return
            self._last_conf_w = w
            self._last_conf_h = h
        self._safe_render()

    def _row_height(self):
        try:
            f = _font_obj(root=self, font=self._opts["font"])
            return max(20, int(f.metrics("linespace")) + 2 * self.ROW_PAD_Y)
        except Exception:
            return 22

    def _char_width(self):
        try:
            f = _font_obj(root=self, font=self._opts["font"])
            return max(6, int(f.measure("0")))
        except Exception:
            return 8

    def _resolve_index(self, index):
        if index in (tk.END, "end"):
            return max(0, len(self._items) - 1)
        if index == "active":
            return max(0, min(self._active_index, max(0, len(self._items) - 1)))
        try:
            idx = int(index)
        except (TypeError, ValueError):
            idx = 0
        if idx < 0:
            idx = max(0, len(self._items) + idx)
        return idx

    def size(self):
        return len(self._items)

    def delete(self, first, last=None):
        if first == "all":
            return super().delete("all")
        start = self._resolve_index(first)
        if last is None:
            if 0 <= start < len(self._items):
                self._items.pop(start)
        else:
            end = len(self._items) - 1 if last in (tk.END, "end") else self._resolve_index(last)
            if start <= end:
                del self._items[start:end + 1]
        if not self._items:
            self._selected.clear()
            self._item_styles.clear()
            self._active_index = 0
            self._top_index = 0
        else:
            self._selected = {i for i in self._selected if 0 <= i < len(self._items)}
            self._active_index = min(self._active_index, len(self._items) - 1)
            self._top_index = max(0, min(self._top_index, len(self._items) - 1))
        self._safe_render()

    def insert(self, index, *elements):
        if index in (tk.END, "end"):
            pos = len(self._items)
        else:
            pos = max(0, min(self._resolve_index(index), len(self._items)))
        for offset, text in enumerate(elements):
            self._items.insert(pos + offset, str(text))
        self._safe_render()

    def get(self, first, last=None):
        if not self._items:
            return () if last is not None else ""
        start = max(0, min(self._resolve_index(first), len(self._items) - 1))
        if last is None:
            return self._items[start]
        end = len(self._items) - 1 if last in (tk.END, "end") else max(0, min(self._resolve_index(last), len(self._items) - 1))
        return tuple(self._items[start:end + 1])

    def curselection(self):
        return tuple(sorted(i for i in self._selected if 0 <= i < len(self._items)))

    def selection_set(self, first, last=None):
        if not self._items:
            return
        start = max(0, min(self._resolve_index(first), len(self._items) - 1))
        end = start if last is None else max(0, min(self._resolve_index(last), len(self._items) - 1))
        for i in range(min(start, end), max(start, end) + 1):
            self._selected.add(i)
        self._safe_render()

    select_set = selection_set

    def selection_clear(self, first, last=None):
        if first == 0 and last in (tk.END, "end"):
            self._selected.clear()
        else:
            start = self._resolve_index(first)
            end = start if last is None else self._resolve_index(last)
            for i in range(min(start, end), max(start, end) + 1):
                self._selected.discard(i)
        self._safe_render()

    select_clear = selection_clear

    def selection_includes(self, index):
        return self._resolve_index(index) in self._selected

    def activate(self, index):
        if self._items:
            self._active_index = max(0, min(self._resolve_index(index), len(self._items) - 1))
            self._safe_render()

    def see(self, index):
        if not self._items:
            return
        idx = max(0, min(self._resolve_index(index), len(self._items) - 1))
        vis = max(1, self._visible_rows())
        if idx < self._top_index:
            self._top_index = idx
        elif idx >= self._top_index + vis:
            self._top_index = max(0, idx - vis + 1)
        self._safe_render()

    def itemconfig(self, index, cnf=None, **kwargs):
        idx = self._resolve_index(index)
        werte = dict(cnf or {}, **kwargs)
        if "fg" in werte:
            werte["foreground"] = werte.pop("fg")
        if "bg" in werte:
            werte["background"] = werte.pop("bg")
        self._item_styles.setdefault(idx, {}).update(werte)
        self._safe_render()

    itemconfigure = itemconfig

    def itemcget(self, index, option):
        if isinstance(index, str) and not index.isdigit() and index not in ("end", "active"):
            return super().itemcget(index, option)
        idx = self._resolve_index(index)
        if option == "fg":
            option = "foreground"
        elif option == "bg":
            option = "background"
        styles = self._item_styles.get(idx, {})
        if option in styles:
            return styles[option]
        if option == "foreground":
            return self._opts["fg"]
        if option == "background":
            return self._opts["bg"]
        if option in ("selectforeground", "selectbackground"):
            return self._opts[option]
        return ""

    def bbox(self, *args):
        if len(args) == 1 and (isinstance(args[0], int) or str(args[0]).isdigit() or args[0] in ("end", "active")):
            if not self._items:
                return None
            idx = max(0, min(self._resolve_index(args[0]), len(self._items) - 1))
            row_h = self._row_height()
            y = (idx - self._top_index) * row_h
            w = max(1, self.winfo_width() if self.winfo_width() > 1 else self._width_chars * self._char_width())
            return (0, y, w, row_h)
        return super().bbox(*args)

    def nearest(self, y):
        if not self._items:
            return 0
        row_h = max(1, self._row_height())
        idx = self._top_index + int(y // row_h)
        return max(0, min(idx, len(self._items) - 1))

    def _visible_rows(self):
        row_h = max(1, self._row_height())
        h = self.winfo_height()
        if h > 1:
            return max(1, h // row_h)
        return max(1, self._height_rows)

    def yview(self, *args):
        total = len(self._items)
        vis = self._visible_rows()
        if not args:
            if total <= vis or total == 0:
                return (0.0, 1.0)
            first = max(0.0, min(1.0, self._top_index / total))
            last = max(0.0, min(1.0, (self._top_index + vis) / total))
            return (first, last)
        cmd = args[0]
        if cmd == "moveto" and len(args) >= 2:
            frac = max(0.0, min(1.0, float(args[1])))
            self._top_index = max(0, min(max(0, total - vis), int(round(frac * total))))
        elif cmd == "scroll" and len(args) >= 2:
            delta = int(float(args[1]))
            unit = args[2] if len(args) >= 3 else "units"
            step = delta * (max(1, vis - 1) if unit == "pages" else 1)
            self._top_index = max(0, min(max(0, total - vis), self._top_index + step))
        self._safe_render()
        return None

    def yview_moveto(self, fraction):
        self.yview("moveto", fraction)

    def yview_scroll(self, number, what):
        self.yview("scroll", number, what)

    def configure(self, cnf=None, **kwargs):
        werte = dict(cnf or {}, **kwargs)
        if not werte:
            return super().configure()
        if "background" in werte:
            werte["bg"] = werte.pop("background")
        if "foreground" in werte:
            werte["fg"] = werte.pop("foreground")
        if "yscrollcommand" in werte:
            self._yscrollcommand = werte.pop("yscrollcommand")
        if "height" in werte:
            self._height_rows = int(werte["height"] or 6)
        if "width" in werte:
            self._width_chars = int(werte["width"] or 36)
        canvas_kw = {}
        if "bg" in werte:
            canvas_kw["bg"] = werte["bg"]
        if "height" in werte or "font" in werte:
            canvas_kw["height"] = max(24, self._height_rows * self._row_height())
        if "width" in werte or "font" in werte:
            canvas_kw["width"] = max(60, self._width_chars * self._char_width())
        self._opts.update(werte)
        if canvas_kw:
            super().configure(**canvas_kw)
        self._safe_render()

    config = configure

    def cget(self, key):
        if key == "background":
            key = "bg"
        elif key == "foreground":
            key = "fg"
        if key == "yscrollcommand":
            return self._yscrollcommand
        if key == "selectmode":
            return self._opts.get("selectmode", "browse")
        if key in self._opts:
            return self._opts[key]
        return super().cget(key)

    def __getitem__(self, key):
        return self.cget(key)

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def keys(self):
        opts = set(super().keys())
        opts.update(self._opts.keys())
        opts.update(("yscrollcommand", "selectmode", "activestyle"))
        return sorted(opts)

    def _on_click(self, event):
        if str(self._opts.get("state", "normal")) == "disabled":
            return "break"
        try:
            self.focus_set()
        except tk.TclError:
            pass
        if not self._items:
            return "break"
        idx = self.nearest(event.y)
        self._selected = {idx}
        self._active_index = idx
        self._safe_render()
        self.event_generate("<<ListboxSelect>>")
        return "break"

    def _move_selection(self, delta):
        if not self._items:
            return "break"
        cur = self.curselection()
        base = cur[0] if cur else self._active_index
        target = max(0, min(len(self._items) - 1, base + delta))
        self._selected = {target}
        self._active_index = target
        self.see(target)
        self.event_generate("<<ListboxSelect>>")
        return "break"

    def _jump_selection(self, target):
        if not self._items:
            return "break"
        target = max(0, min(len(self._items) - 1, target))
        self._selected = {target}
        self._active_index = target
        self.see(target)
        self.event_generate("<<ListboxSelect>>")
        return "break"

    def _safe_render(self):
        if getattr(self, "_rendering", False):
            return
        self._rendering = True
        try:
            if self.winfo_exists():
                self._render()
        except tk.TclError:
            pass
        finally:
            self._rendering = False

    def _render(self):
        super().delete("all")
        o = self._opts
        row_h = self._row_height()
        w = max(1, self.winfo_width() if self.winfo_width() > 1 else self._width_chars * self._char_width())
        vis = self._visible_rows()
        total = len(self._items)
        if self._top_index > max(0, total - vis):
            self._top_index = max(0, total - vis)
        for row_offset in range(vis + 1):
            idx = self._top_index + row_offset
            if idx >= total:
                break
            y0 = row_offset * row_h
            y1 = y0 + row_h
            st = self._item_styles.get(idx, {})
            selected = idx in self._selected
            bg = st.get("selectbackground", o["selectbackground"]) if selected else st.get("background", o["bg"])
            fg = st.get("selectforeground", o["selectforeground"]) if selected else st.get("foreground", o["fg"])
            if selected or bg != o["bg"]:
                self.create_rectangle(0, y0, w, y1, fill=bg, outline="", tags=("row",))
            self.create_text(
                0, (y0 + y1) / 2,
                text=self._items[idx], font=o["font"], fill=fg, anchor="w", tags=("text",),
            )
        if callable(self._yscrollcommand):
            try:
                first, last = self.yview()
                self._yscrollcommand(first, last)
            except Exception:
                pass


class GlideScale(tk.Canvas):
    """Themebarer Schieberegler auf Canvas-Grundlage mit kompatibler Scale-Schnittstelle."""

    def __init__(self, master, **kwargs):
        self._from = float(kwargs.pop("from_", kwargs.pop("from", 0.0)))
        self._to = float(kwargs.pop("to", 100.0))
        self._resolution = float(kwargs.pop("resolution", 1.0) or 1.0)
        self._orient = kwargs.pop("orient", "horizontal")
        self._variable = kwargs.pop("variable", None)
        self._command = kwargs.pop("command", None)
        length = int(kwargs.pop("length", 240) or 240)
        bar_w = int(kwargs.pop("width", 12) or 12)
        self._slider_len = int(kwargs.pop("sliderlength", 22) or 22)
        bg = kwargs.pop("bg", kwargs.pop("background", "#335588"))
        try:
            parent_bg = master.cget("bg")
        except Exception:
            parent_bg = bg
        self._opts = {
            "bg": bg,
            "fg": kwargs.pop("fg", kwargs.pop("foreground", "#e5e5e5")),
            "troughcolor": kwargs.pop("troughcolor", "#444444"),
            "activebackground": kwargs.pop("activebackground", bg),
            "showvalue": kwargs.pop("showvalue", False),
            "sliderrelief": kwargs.pop("sliderrelief", "flat"),
            "state": kwargs.pop("state", "normal"),
            "length": length,
            "width": bar_w,
        }
        highlightthickness = kwargs.pop("highlightthickness", 0)
        bd = kwargs.pop("bd", kwargs.pop("borderwidth", 0))
        for k in list(kwargs):
            self._opts[k] = kwargs.pop(k)
        self._value = self._from
        self._trace_id = None
        super().__init__(
            master, bg=parent_bg, bd=bd, highlightthickness=highlightthickness,
            width=length, height=max(22, bar_w + 10), cursor="hand2", takefocus=1,
        )
        self._attach_variable(self._variable)
        self.bind("<Button-1>", self._on_pointer)
        self.bind("<B1-Motion>", self._on_pointer)
        self.bind("<Left>", lambda _e: self._step(-1))
        self.bind("<Right>", lambda _e: self._step(1))
        self.bind("<Configure>", self._on_configure, add="+")
        self.bind("<Destroy>", self._on_destroy, add="+")
        self._render()

    def _on_configure(self, event=None):
        if event is not None:
            w, h = getattr(event, "width", None), getattr(event, "height", None)
            if w is not None and h is not None and w == getattr(self, "_last_conf_w", None) and h == getattr(self, "_last_conf_h", None):
                return
            self._last_conf_w = w
            self._last_conf_h = h
        self._safe_render()

    def _attach_variable(self, variable):
        if self._variable is not None and self._trace_id is not None:
            try:
                self._variable.trace_remove("write", self._trace_id)
            except Exception:
                pass
        self._variable = variable
        self._trace_id = None
        if variable is not None:
            try:
                self._value = float(variable.get())
            except Exception:
                pass
            if hasattr(variable, "trace_add"):
                try:
                    self._trace_id = variable.trace_add("write", lambda *_: self._sync_from_var())
                except Exception:
                    self._trace_id = None

    def _on_destroy(self, event):
        if event.widget is self:
            self._attach_variable(None)

    def _sync_from_var(self):
        if self._variable is not None:
            try:
                self._value = float(self._variable.get())
            except Exception:
                pass
        self._safe_render()

    def _clamp(self, value):
        lo, hi = min(self._from, self._to), max(self._from, self._to)
        val = max(lo, min(hi, float(value)))
        if self._resolution > 0:
            steps = round((val - self._from) / self._resolution)
            val = max(lo, min(hi, self._from + steps * self._resolution))
            if self._resolution == int(self._resolution):
                return int(round(val))
        return val

    def get(self):
        if self._variable is not None:
            try:
                return self._clamp(self._variable.get())
            except Exception:
                pass
        return self._clamp(self._value)

    def set(self, value, *, invoke_command=False):
        clamped = self._clamp(value)
        self._value = clamped
        if self._variable is not None:
            try:
                self._variable.set(clamped)
            except Exception:
                pass
        self._safe_render()
        if invoke_command and callable(self._command):
            self._command(str(clamped))

    def _on_pointer(self, event):
        if str(self._opts.get("state", "normal")) == "disabled":
            return "break"
        try:
            self.focus_set()
        except tk.TclError:
            pass
        w = max(1, self.winfo_width())
        pad = self._slider_len / 2
        usable = max(1.0, w - 2 * pad)
        frac = max(0.0, min(1.0, (event.x - pad) / usable))
        self.set(self._from + frac * (self._to - self._from), invoke_command=True)
        return "break"

    def _step(self, direction):
        if str(self._opts.get("state", "normal")) == "disabled":
            return "break"
        step = self._resolution if self._resolution > 0 else 1
        self.set(self.get() + direction * step, invoke_command=True)
        return "break"

    def configure(self, cnf=None, **kwargs):
        werte = dict(cnf or {}, **kwargs)
        if not werte:
            return super().configure()
        if "from_" in werte:
            self._from = float(werte.pop("from_"))
        if "to" in werte:
            self._to = float(werte.pop("to"))
        if "resolution" in werte:
            self._resolution = float(werte.pop("resolution") or 1.0)
        if "orient" in werte:
            self._orient = werte.pop("orient")
        if "variable" in werte:
            self._attach_variable(werte.pop("variable"))
        if "command" in werte:
            self._command = werte.pop("command")
        self._opts.update(werte)
        self._safe_render()

    config = configure

    def cget(self, key):
        if key in ("from", "from_"):
            return self._from
        if key == "to":
            return self._to
        if key == "resolution":
            return self._resolution
        if key == "orient":
            return self._orient
        if key == "variable":
            return str(self._variable) if self._variable is not None else ""
        if key == "command":
            return self._command
        if key in self._opts:
            return self._opts[key]
        return super().cget(key)

    def __getitem__(self, key):
        return self.cget(key)

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def keys(self):
        opts = set(super().keys())
        opts.update(self._opts.keys())
        opts.update(("from", "from_", "to", "resolution", "variable", "command", "orient", "length"))
        return sorted(opts)

    def _safe_render(self):
        if getattr(self, "_rendering", False):
            return
        self._rendering = True
        try:
            if self.winfo_exists():
                self._render()
        except tk.TclError:
            pass
        finally:
            self._rendering = False

    def _render(self):
        super().delete("all")
        o = self._opts
        w = max(40, self.winfo_width() if self.winfo_width() > 1 else int(o["length"]))
        h = max(18, self.winfo_height() if self.winfo_height() > 1 else 22)
        cy = h / 2
        pad = self._slider_len / 2
        usable = max(1.0, w - 2 * pad)
        span = (self._to - self._from) or 1.0
        frac = max(0.0, min(1.0, (float(self.get()) - self._from) / span))
        sx = pad + frac * usable
        self.create_polygon(
            rounded_rect_points(4, cy - 3, w - 4, cy + 3, 3),
            smooth=True, splinesteps=8, fill=o["troughcolor"], outline="",
        )
        self.create_polygon(
            rounded_rect_points(sx - pad, cy - 6, sx + pad, cy + 6, 5),
            smooth=True, splinesteps=10, fill=o["bg"], outline=o["fg"], width=1,
        )


class ThemedAutoScrollbar(tk.Canvas):
    """Themebare Canvas-Scrollbar ohne native weiße Windows-/Tk-Hintergründe."""

    FULLY_VISIBLE_RATIO = 0.999

    def __init__(
        self,
        master,
        bg_color,
        track_color,
        thumb_color,
        active_thumb_color,
        width=14,
        radius=7,
        orient="vertical",
        length=None,
    ):
        self.orient = "horizontal" if orient == "horizontal" else "vertical"
        super().__init__(
            master,
            bg=bg_color,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
            **({"width": width} if self.orient == "vertical" else {"height": width}),
            **({} if length is None else ({"height": length} if self.orient == "vertical" else {"width": length})),
        )
        self.bg_color = bg_color
        self.track_color = track_color
        self.thumb_color = thumb_color
        self.active_thumb_color = active_thumb_color
        self.bar_width = width
        self.radius = radius
        self.command = None
        self.first = 0.0
        self.last = 1.0
        self.dragging = False
        self.drag_offset = 0
        self.is_hovered = False

        bind_resize(self, lambda _event: self._draw())
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<B1-Motion>", self._on_motion)
        self.bind("<ButtonRelease-1>", self._on_release)

    def set_command(self, command):
        self.command = command

    def set_theme(self, bg_color, track_color, thumb_color, active_thumb_color):
        self.bg_color = bg_color
        self.track_color = track_color
        self.thumb_color = thumb_color
        self.active_thumb_color = active_thumb_color
        self.configure(bg=bg_color)
        self._draw()

    def set(self, first, last):
        try:
            self.first = max(0.0, min(1.0, float(first)))
            self.last = max(0.0, min(1.0, float(last)))
        except (TypeError, ValueError):
            self.first = 0.0
            self.last = 1.0
        self._draw()

    def _rounded_rect(self, x1, y1, x2, y2, radius, fill):
        return self.create_polygon(
            rounded_rect_points(x1, y1, x2, y2, radius),
            smooth=True, splinesteps=18, fill=fill, outline="",
        )

    def _metrics(self):
        if self.orient == "vertical":
            quer = max(self.winfo_width(), self.bar_width)
            laengs = max(self.winfo_height(), 30)
        else:
            quer = max(self.winfo_height(), self.bar_width)
            laengs = max(self.winfo_width(), 30)
        track_pad_x = max(3, int(quer * 0.28))
        track_pad_y = 4
        track_x1 = track_pad_x
        track_x2 = quer - track_pad_x
        track_y1 = track_pad_y
        track_y2 = laengs - track_pad_y
        track_h = max(1, track_y2 - track_y1)
        visible_ratio = max(0.05, min(1.0, self.last - self.first))
        thumb_h = max(28, int(track_h * visible_ratio))
        thumb_h = min(thumb_h, track_h)
        max_y = max(track_y1, track_y2 - thumb_h)
        thumb_y1 = track_y1 + int((track_h - thumb_h) * self.first / max(0.0001, 1.0 - visible_ratio)) if visible_ratio < 1 else track_y1
        thumb_y1 = max(track_y1, min(max_y, thumb_y1))
        thumb_y2 = thumb_y1 + thumb_h
        return track_x1, track_y1, track_x2, track_y2, thumb_y1, thumb_y2

    def _along(self, event):
        return event.y if self.orient == "vertical" else event.x

    def _place(self, quer1, laengs1, quer2, laengs2, radius, fill):
        if self.orient == "vertical":
            self._rounded_rect(quer1, laengs1, quer2, laengs2, radius, fill)
        else:
            self._rounded_rect(laengs1, quer1, laengs2, quer2, radius, fill)

    def is_scrollable(self):
        return (self.last - self.first) < self.FULLY_VISIBLE_RATIO

    def _draw(self):
        self.delete("all")
        paint_canvas_backdrop(self)
        if not self.is_scrollable():
            return
        track_x1, track_y1, track_x2, track_y2, thumb_y1, thumb_y2 = self._metrics()
        track_radius = max(2, (track_x2 - track_x1) / 2)
        self._place(track_x1, track_y1, track_x2, track_y2, track_radius, self.track_color)
        thumb_color = self.active_thumb_color if self.is_hovered or self.dragging else self.thumb_color
        self._place(track_x1, thumb_y1, track_x2, thumb_y2, track_radius, thumb_color)

    def _on_enter(self, _event):
        if not self.is_scrollable():
            return
        self.is_hovered = True
        self._draw()

    def _on_leave(self, _event):
        self.is_hovered = False
        if not self.dragging:
            self._draw()

    def _on_press(self, event):
        if not self.is_scrollable():
            return
        _tx1, track_y1, _tx2, track_y2, thumb_y1, thumb_y2 = self._metrics()
        position = self._along(event)
        if thumb_y1 <= position <= thumb_y2:
            self.dragging = True
            self.drag_offset = position - thumb_y1
        else:
            thumb_h = thumb_y2 - thumb_y1
            self._moveto_from_thumb_y(position - thumb_h / 2, track_y1, track_y2, thumb_h)

    def _on_motion(self, event):
        if not self.dragging:
            return
        _tx1, track_y1, _tx2, track_y2, thumb_y1, thumb_y2 = self._metrics()
        thumb_h = thumb_y2 - thumb_y1
        self._moveto_from_thumb_y(self._along(event) - self.drag_offset, track_y1, track_y2, thumb_h)

    def _on_release(self, _event):
        self.dragging = False
        self._draw()

    def _moveto_from_thumb_y(self, proposed_y, track_y1, track_y2, thumb_h):
        available = max(1, (track_y2 - track_y1) - thumb_h)
        fraction = (proposed_y - track_y1) / available
        fraction = max(0.0, min(1.0, fraction))
        if callable(self.command):
            self.command("moveto", fraction)
