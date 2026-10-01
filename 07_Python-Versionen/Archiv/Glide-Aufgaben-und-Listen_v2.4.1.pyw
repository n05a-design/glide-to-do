import calendar
import copy
import csv
import json
import os
import re
import shutil
import sys
import tkinter as tk
import tkinter.ttk as ttk
import uuid
from tkinter import messagebox, filedialog
from datetime import datetime, date

# --- Produkt-Branding -------------------------------------------------------
APP_NAME = "Glide"
APP_TAGLINE = "Aufgaben und Listen"
APP_PRODUCT_NAME = f"{APP_NAME} \u2013 {APP_TAGLINE}"
APP_VERSION = "2.4.1"
# Frühere App-/Ordnernamen, aus denen bestehende Nutzerdaten automatisch
# übernommen werden, wenn im Glide-Ordner noch nichts liegt.
LEGACY_APP_NAMES = ["Lokale Listen-App"]
LEGACY_BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_app_data_dir():
    """Plattformgerechter, beschreibbarer Speicherort ohne externe Bibliotheken."""
    if sys.platform == "darwin":
        base = os.path.join(os.path.expanduser("~"), "Library", "Application Support")
        path = os.path.join(base, APP_NAME)
    elif os.name == "nt":
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
        path = os.path.join(base, APP_NAME)
    else:
        base = os.environ.get("XDG_DATA_HOME") or os.path.join(os.path.expanduser("~"), ".local", "share")
        path = os.path.join(base, APP_NAME)
    os.makedirs(path, exist_ok=True)
    return path


BASE_DIR = get_app_data_dir()
SAVE_FILE = os.path.join(BASE_DIR, "liste_speicher.json")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
os.makedirs(BACKUP_DIR, exist_ok=True)


def migrate_legacy_file(filename):
    """Übernimmt bestehende Daten aus dem alten Skriptordner, wenn im Nutzerordner noch nichts liegt."""
    legacy_path = os.path.join(LEGACY_BASE_DIR, filename)
    target_path = os.path.join(BASE_DIR, filename)
    try:
        if LEGACY_BASE_DIR != BASE_DIR and os.path.exists(legacy_path) and not os.path.exists(target_path):
            shutil.copy2(legacy_path, target_path)
    except Exception:
        pass


for _filename in ("liste_speicher.json", "settings.json", "window.conf"):
    migrate_legacy_file(_filename)


def _legacy_app_data_dir(app_name):
    """Datenordner, den eine frühere Version unter einem anderen App-Namen genutzt hätte."""
    if sys.platform == "darwin":
        return os.path.join(os.path.expanduser("~"), "Library", "Application Support", app_name)
    if os.name == "nt":
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
        return os.path.join(base, app_name)
    base = os.environ.get("XDG_DATA_HOME") or os.path.join(os.path.expanduser("~"), ".local", "share")
    return os.path.join(base, app_name)


def migrate_from_legacy_app_dirs():
    """Übernimmt Daten aus früheren App-Namen, falls im aktuellen Glide-Ordner noch nichts liegt.

    Dadurch verlieren bestehende Testnutzer beim Umbenennen auf 'Glide' keine Listen.
    """
    if os.path.exists(SAVE_FILE):
        return
    for legacy_name in LEGACY_APP_NAMES:
        legacy_dir = _legacy_app_data_dir(legacy_name)
        if not legacy_dir or legacy_dir == BASE_DIR or not os.path.isdir(legacy_dir):
            continue
        copied_any = False
        for filename in ("liste_speicher.json", "settings.json", "window.conf"):
            src = os.path.join(legacy_dir, filename)
            dst = os.path.join(BASE_DIR, filename)
            try:
                if os.path.exists(src) and not os.path.exists(dst):
                    shutil.copy2(src, dst)
                    copied_any = True
            except Exception:
                pass
        if copied_any:
            break


migrate_from_legacy_app_dirs()


class RoundedButton(tk.Canvas):
    """Nativer Tkinter-Button mit abgerundeter Outline und Hover-Fill."""

    def __init__(
        self,
        master,
        text,
        command,
        border_color,
        hover_fill,
        text_color,
        hover_text_color="#FFFFFF",
        bg_color="#FFFFFF",
        height=42,
        radius=18,
        width=132,
        font=("TkDefaultFont", 10, "bold"),
    ):
        super().__init__(
            master,
            height=height,
            width=width,
            bg=bg_color,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
            takefocus=1,
        )
        self.text = text
        self.command = command
        self.border_color = border_color
        self.hover_fill = hover_fill
        self.text_color = text_color
        self.hover_text_color = hover_text_color
        self.bg_color = bg_color
        self.height = height
        self.radius = radius
        self.font = font
        self.is_hovered = False
        self.is_pressed = False

        self.bind("<Configure>", lambda event: self._draw())
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<space>", self._on_keyboard_activate)
        self.bind("<Return>", self._on_keyboard_activate)

        self._draw()

    def set_theme(self, bg_color, text_color, border_color=None, hover_fill=None, hover_text_color=None):
        self.bg_color = bg_color
        self.text_color = text_color
        if border_color is not None:
            self.border_color = border_color
        if hover_fill is not None:
            self.hover_fill = hover_fill
        if hover_text_color is not None:
            self.hover_text_color = hover_text_color
        self.configure(bg=bg_color)
        self._draw()

    def set_text(self, text):
        self.text = text
        self._draw()

    def _rounded_rect(self, x1, y1, x2, y2, radius, fill, outline, width=1):
        points = [
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
        return self.create_polygon(
            points,
            smooth=True,
            splinesteps=24,
            fill=fill,
            outline=outline,
            width=width,
        )

    def _draw(self):
        self.delete("all")
        w = max(self.winfo_width(), 30)
        h = max(self.winfo_height(), self.height)
        pad = 2

        fill = self.hover_fill if self.is_hovered else self.bg_color
        text_color = self.hover_text_color if self.is_hovered else self.border_color
        border_width = 1.4

        if self.is_pressed and self.is_hovered:
            pad = 3
            border_width = 1.8

        self._rounded_rect(
            pad,
            pad,
            w - pad,
            h - pad,
            self.radius,
            fill=fill,
            outline=self.border_color,
            width=border_width,
        )
        self.create_text(
            w / 2,
            h / 2,
            text=self.text,
            fill=text_color,
            font=self.font,
        )

    def _on_enter(self, _event):
        self.is_hovered = True
        self._draw()

    def _on_leave(self, _event):
        self.is_hovered = False
        self.is_pressed = False
        self._draw()

    def _on_press(self, _event):
        self.is_pressed = True
        self._draw()

    def _on_keyboard_activate(self, _event):
        if callable(self.command):
            self.command()
        return "break"

    def _on_release(self, event):
        was_pressed = self.is_pressed
        self.is_pressed = False
        inside = 0 <= event.x <= self.winfo_width() and 0 <= event.y <= self.winfo_height()
        self._draw()
        if was_pressed and inside and callable(self.command):
            self.command()


class RoundedContainer(tk.Canvas):
    """Runde, themebare Box mit innenliegendem Frame für normale Tkinter-Widgets.

    Hinweis: Normale Tkinter-Widgets sind rechteckig. Damit sie die gerundeten Ecken
    nicht optisch überdecken, kann der innenliegende Frame zusätzlich eingerückt werden.
    """

    def __init__(self, master, bg_color, fill_color, outline_color=None, radius=18, padding=1, width=None, height=None, inner_pad_x=None, inner_pad_y=None):
        kwargs = {
            "bg": bg_color,
            "highlightthickness": 0,
            "bd": 0,
        }
        if width is not None:
            kwargs["width"] = width
        if height is not None:
            kwargs["height"] = height
        super().__init__(master, **kwargs)
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.outline_color = outline_color or fill_color
        self.radius = radius
        self.padding = padding
        self.inner_pad_x = padding if inner_pad_x is None else inner_pad_x
        self.inner_pad_y = padding if inner_pad_y is None else inner_pad_y
        self.inner = tk.Frame(self, bg=fill_color, bd=0, highlightthickness=0)
        self._window_id = self.create_window(
            self.inner_pad_x,
            self.inner_pad_y,
            anchor="nw",
            window=self.inner,
        )
        self.bind("<Configure>", self._on_configure)
        self._draw()

    def set_theme(self, bg_color, fill_color, outline_color=None):
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.outline_color = outline_color or fill_color
        self.configure(bg=bg_color)
        self.inner.configure(bg=fill_color)
        self._draw()

    def _rounded_rect(self, x1, y1, x2, y2, radius, fill, outline, width=1):
        points = [
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
        self.create_polygon(points, smooth=True, splinesteps=24, fill=fill, outline=outline, width=width, tags=("surface",))

    def _on_configure(self, _event=None):
        pad_x = self.inner_pad_x
        pad_y = self.inner_pad_y
        w = max(self.winfo_width(), pad_x * 2 + 2)
        h = max(self.winfo_height(), pad_y * 2 + 2)
        self.coords(self._window_id, pad_x, pad_y)
        self.itemconfigure(
            self._window_id,
            width=max(1, w - pad_x * 2),
            height=max(1, h - pad_y * 2),
        )
        self._draw()

    def _draw(self):
        self.delete("surface")
        w = max(self.winfo_width(), 4)
        h = max(self.winfo_height(), 4)
        pad = 1
        self._rounded_rect(
            pad,
            pad,
            w - pad,
            h - pad,
            self.radius,
            fill=self.fill_color,
            outline=self.outline_color,
            width=1,
        )
        self.tag_lower("surface")


class ThemedAutoScrollbar(tk.Canvas):
    """Themebare Canvas-Scrollbar ohne native weiße Windows-/Tk-Hintergründe."""

    def __init__(
        self,
        master,
        bg_color,
        track_color,
        thumb_color,
        active_thumb_color,
        width=14,
        radius=7,
    ):
        super().__init__(
            master,
            width=width,
            bg=bg_color,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
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

        self.bind("<Configure>", lambda _event: self._draw())
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
        points = [
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
        self.create_polygon(points, smooth=True, splinesteps=18, fill=fill, outline="")

    def _metrics(self):
        w = max(self.winfo_width(), self.bar_width)
        h = max(self.winfo_height(), 30)
        track_pad_x = max(3, int(w * 0.28))
        track_pad_y = 4
        track_x1 = track_pad_x
        track_x2 = w - track_pad_x
        track_y1 = track_pad_y
        track_y2 = h - track_pad_y
        track_h = max(1, track_y2 - track_y1)
        visible_ratio = max(0.05, min(1.0, self.last - self.first))
        thumb_h = max(28, int(track_h * visible_ratio))
        thumb_h = min(thumb_h, track_h)
        max_y = max(track_y1, track_y2 - thumb_h)
        thumb_y1 = track_y1 + int((track_h - thumb_h) * self.first / max(0.0001, 1.0 - visible_ratio)) if visible_ratio < 1 else track_y1
        thumb_y1 = max(track_y1, min(max_y, thumb_y1))
        thumb_y2 = thumb_y1 + thumb_h
        return track_x1, track_y1, track_x2, track_y2, thumb_y1, thumb_y2

    def _draw(self):
        self.delete("all")
        track_x1, track_y1, track_x2, track_y2, thumb_y1, thumb_y2 = self._metrics()
        track_radius = max(2, (track_x2 - track_x1) / 2)
        self._rounded_rect(track_x1, track_y1, track_x2, track_y2, track_radius, self.track_color)
        thumb_color = self.active_thumb_color if self.is_hovered or self.dragging else self.thumb_color
        self._rounded_rect(track_x1, thumb_y1, track_x2, thumb_y2, track_radius, thumb_color)

    def _on_enter(self, _event):
        self.is_hovered = True
        self._draw()

    def _on_leave(self, _event):
        self.is_hovered = False
        if not self.dragging:
            self._draw()

    def _on_press(self, event):
        _tx1, track_y1, _tx2, track_y2, thumb_y1, thumb_y2 = self._metrics()
        if thumb_y1 <= event.y <= thumb_y2:
            self.dragging = True
            self.drag_offset = event.y - thumb_y1
        else:
            thumb_h = thumb_y2 - thumb_y1
            self._moveto_from_thumb_y(event.y - thumb_h / 2, track_y1, track_y2, thumb_h)
        self._draw()

    def _on_motion(self, event):
        if not self.dragging:
            return
        _tx1, track_y1, _tx2, track_y2, thumb_y1, thumb_y2 = self._metrics()
        thumb_h = thumb_y2 - thumb_y1
        self._moveto_from_thumb_y(event.y - self.drag_offset, track_y1, track_y2, thumb_h)

    def _on_release(self, _event):
        self.dragging = False
        self._draw()

    def _moveto_from_thumb_y(self, proposed_y, track_y1, track_y2, thumb_h):
        available = max(1, (track_y2 - track_y1) - thumb_h)
        fraction = (proposed_y - track_y1) / available
        fraction = max(0.0, min(1.0, fraction))
        if callable(self.command):
            self.command("moveto", fraction)


class ListApp:
    THEMES = {
        "light": {
            "bg": "#F5F5F7",
            "card": "#FFFFFF",
            "input": "#FFFFFF",
            "input_border": "#D8D8DE",
            "text": "#1D1D1F",
            "muted": "#6E6E73",
            "placeholder": "#A7A7AD",
            "accent": "#AF52DE",
            "theme_toggle": "#000000",
            "theme_toggle_hover_text": "#FFFFFF",
            "delete": "#FF3B30",
            "export": "#34C759",
            "import": "#8B5E34",
            "clear": "#0A84FF",
            "flag": "#FF9500",
            "priority_low": "#8E8E93",
            "priority_medium": "#FF9500",
            "priority_high": "#FF3B30",
            "line": "#E5E5EA",
            "selection": "#AF52DE",
            "overdue": "#FF3B30",
            "due_today": "#FF9500",
            "due_action": "#30B0C7",
            "confirm": "#34C759",
        },
        "dark": {
            "bg": "#111113",
            "card": "#1C1C1E",
            "input": "#2C2C2E",
            "input_border": "#3A3A3C",
            "text": "#F5F5F7",
            "muted": "#A1A1A6",
            "placeholder": "#6F6F75",
            "accent": "#BF5AF2",
            "theme_toggle": "#8E8E93",
            "theme_toggle_hover_text": "#111113",
            "delete": "#FF453A",
            "export": "#30D158",
            "import": "#D0A46F",
            "clear": "#0A84FF",
            "flag": "#FF9F0A",
            "priority_low": "#A1A1A6",
            "priority_medium": "#FF9F0A",
            "priority_high": "#FF453A",
            "line": "#2C2C2E",
            "selection": "#BF5AF2",
            "overdue": "#FF453A",
            "due_today": "#FF9F0A",
            "due_action": "#40C8E0",
            "confirm": "#30D158",
        },
    }

    EMPTY_ROW_ID = "__empty__"
    MAX_BACKUPS = 40  # Anzahl automatischer Sicherungen, die maximal aufbewahrt werden.
    IMPORTANCE_MARKERS = {0: "", 1: "⚐ ", 2: "⚑ ", 3: "🚩 "}
    IMPORTANCE_NAMES = {0: "keine", 1: "niedrig", 2: "mittel", 3: "hoch"}

    # Listen lassen sich einfärben – ausschließlich mit Farben, die ohnehin schon
    # im Einsatz sind (Theme-Schlüssel, damit die Farbe in Hell und Dunkel passt).
    LIST_COLOR_CHOICES = [
        ("Lila", "accent"),
        ("Blau", "clear"),
        ("Türkis", "due_action"),
        ("Grün", "export"),
        ("Gelb", "flag"),
        ("Rot", "delete"),
        ("Braun", "import"),
    ]
    LIST_COLOR_KEYS = [key for _label, key in LIST_COLOR_CHOICES]

    def __init__(self, root):
        self.root = root
        self.root.title(APP_PRODUCT_NAME)
        self.root.geometry("1000x800")
        self.root.minsize(860, 700)

        self.items = []
        self.lists = []
        self.folders = []
        self.sidebar_rows = []
        self.sidebar_iid_to_row = {}
        self.sidebar_drag_start_iid = None
        self.sidebar_drag_start_y = 0
        self.sidebar_drag_has_moved = False
        self.active_list_id = None
        self.undo_stack = []
        self._after_ids = []

        self.settings = self.load_settings()
        self.search_var = tk.StringVar()
        initial_filter_mode = self.settings.get("filter_mode")
        if initial_filter_mode not in ("all", "open", "done"):
            initial_filter_mode = "open" if bool(self.settings.get("hide_done", False)) else "all"
        self.hide_done_var = tk.BooleanVar(value=initial_filter_mode == "open")
        self.show_done_only_var = tk.BooleanVar(value=initial_filter_mode == "done")
        self.entry_placeholder_text = "Listenpunkt eingeben"
        self.search_placeholder_text = "Suchwort eingeben"
        self.entry_placeholder_active = False
        self.search_placeholder_active = False
        self.filters_visible = True
        self.selection_anchor_id = None
        self.drag_start_id = None
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.drag_has_moved = False
        self.expanded_ids = set()

        self.theme_name = self.settings.get("theme", "light")
        if self.theme_name not in self.THEMES:
            self.theme_name = "light"
        self.active_list_id = self.settings.get("active_list_id") if isinstance(self.settings.get("active_list_id"), str) else None
        self.app_title = self.settings.get("title", "Meine Liste").strip() or "Meine Liste"
        self.theme = self.THEMES[self.theme_name]
        self.theme_widgets = []
        self.rounded_containers = []
        self.buttons = []

        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.update_window_title()
        self.root.configure(bg=self.theme["bg"])
        self.create_ui()
        self.apply_theme()
        self.load_items()
        self.restore_window_position()

        # Tastaturkürzel
        # Enter wird direkt im Eingabefeld behandelt, damit add_item nicht doppelt ausgelöst wird.
        self.root.bind("<Delete>", self.delete_item)
        self.root.bind("<Control-e>", lambda e: self.export_as_txt())
        self.root.bind("<Control-i>", lambda e: self.import_from_txt())
        self.root.bind("<Control-s>", lambda e: self.save_items())
        self.root.bind("<Control-q>", lambda e: self.root.quit())
        self.root.bind("<Control-z>", self.undo_last_change)
        self.root.bind("<Control-c>", self.copy_selected_to_clipboard)
        self.root.bind("<Control-v>", self.paste_items_from_clipboard)
        self.root.bind("<Control-a>", self.select_all_items)
        self.root.bind("<Command-c>", self.copy_selected_to_clipboard)
        self.root.bind("<Command-v>", self.paste_items_from_clipboard)
        self.root.bind("<Command-a>", self.select_all_items)
        self.root.bind("<Command-z>", self.undo_last_change)
        self.root.bind("<Command-f>", self.focus_search)
        self.root.bind("<Control-n>", self.focus_entry)
        self.root.bind("<Control-N>", self.create_new_list)
        self.root.bind("<Control-w>", self.delete_current_list)
        self.root.bind("<Control-f>", self.focus_search)
        self.root.bind("<Control-F>", self.cycle_importance_selected)
        self.root.bind("<Alt-p>", self.cycle_importance_selected)
        self.root.bind("<Escape>", self.handle_escape)
        self.root.bind("<F2>", lambda e: self.edit_item())
        self.root.bind("<F3>", lambda e: self.edit_title())
        self.root.bind("<Control-d>", lambda e: self.toggle_theme())
        self.root.bind("<Control-t>", self.set_due_date_selected)
        self.root.bind("<Command-t>", self.set_due_date_selected)

    # -----------------------------
    # Einstellungen / Basis
    # -----------------------------
    def load_settings(self):
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
                    data = json.load(file)
                if isinstance(data, dict):
                    return data
        except Exception:
            pass
        return {}

    def save_settings(self):
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    {
                        "theme": self.theme_name,
                        "title": self.app_title,
                        "hide_done": bool(self.hide_done_var.get()) if hasattr(self, "hide_done_var") else False,
                        "filter_mode": self.get_filter_mode() if hasattr(self, "hide_done_var") else "all",
                        "active_list_id": self.active_list_id,
                    },
                    file,
                    ensure_ascii=False,
                    indent=4,
                )
        except Exception:
            pass

    def save_theme_setting(self):
        self.save_settings()

    def update_window_title(self):
        self.root.title(f"{self.app_title} \u00b7 {APP_NAME}")

    def register_theme_widget(self, widget, bg_key="bg", fg_key=None):
        self.theme_widgets.append((widget, bg_key, fg_key))
        return widget

    def make_rounded_container(self, master, fill_key="card", outline_key="line", radius=18, padding=1, width=None, height=None, inner_pad_x=None, inner_pad_y=None):
        container = RoundedContainer(
            master,
            bg_color=self.theme["bg"],
            fill_color=self.theme[fill_key],
            outline_color=self.theme[outline_key],
            radius=radius,
            padding=padding,
            width=width,
            height=height,
            inner_pad_x=inner_pad_x,
            inner_pad_y=inner_pad_y,
        )
        container.fill_key = fill_key
        container.outline_key = outline_key
        self.rounded_containers.append(container)
        return container

    def make_button(
        self,
        master,
        text,
        command,
        color_key="accent",
        width=132,
        height=42,
        radius=18,
        font=("TkDefaultFont", 10, "bold"),
        bg_key="bg",
    ):
        button = RoundedButton(
            master,
            text=text,
            command=command,
            border_color=self.theme[color_key],
            hover_fill=self.theme[color_key],
            text_color=self.theme[color_key],
            bg_color=self.theme[bg_key],
            width=width,
            height=height,
            radius=radius,
            font=font,
        )
        button.color_key = color_key
        button.bg_key = bg_key
        self.buttons.append(button)
        return button

    # -----------------------------
    # Themenkonforme Eingabe-Dialoge
    # -----------------------------
    def _center_dialog(self, dialog, min_width=420):
        """Setzt Größe und Position eines Dialogs zentriert über dem Hauptfenster."""
        dialog.update_idletasks()
        width = max(dialog.winfo_reqwidth(), min_width)
        height = dialog.winfo_reqheight()
        try:
            parent_w = self.root.winfo_width()
            parent_h = self.root.winfo_height()
            parent_x = self.root.winfo_rootx()
            parent_y = self.root.winfo_rooty()
            x = parent_x + max((parent_w - width) // 2, 0)
            y = parent_y + max((parent_h - height) // 3, 0)
        except tk.TclError:
            x, y = 200, 150
        dialog.geometry(f"{width}x{height}+{x}+{y}")

    def _make_dialog_button(self, master, text, command, color_key, width=124, height=40):
        """RoundedButton für Dialoge – bewusst NICHT in self.buttons, da der Dialog kurzlebig ist."""
        return RoundedButton(
            master,
            text=text,
            command=command,
            border_color=self.theme[color_key],
            hover_fill=self.theme[color_key],
            text_color=self.theme[color_key],
            bg_color=self.theme["bg"],
            width=width,
            height=height,
            radius=16,
            font=("TkDefaultFont", 10, "bold"),
        )

    def themed_input_dialog(self, title, prompt="", initial="", ok_text="OK", accent_key="confirm"):
        """Modaler, an Hell-/Dunkelmodus angepasster Texteingabe-Dialog.

        Verhält sich wie simpledialog.askstring: liefert den eingegebenen Text
        oder None bei Abbruch (Escape / Abbrechen / Fenster schließen).
        """
        result = {"value": None}

        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.configure(bg=self.theme["bg"])
        dialog.transient(self.root)
        dialog.resizable(False, False)

        container = tk.Frame(dialog, bg=self.theme["bg"])
        container.pack(fill="both", expand=True, padx=24, pady=22)

        heading = tk.Label(
            container,
            text=title,
            bg=self.theme["bg"],
            fg=self.theme["text"],
            font=("TkDefaultFont", 15, "bold"),
            anchor="w",
            justify="left",
        )
        heading.pack(anchor="w", pady=(0, 6))

        if prompt:
            prompt_label = tk.Label(
                container,
                text=prompt,
                bg=self.theme["bg"],
                fg=self.theme["muted"],
                font=("TkDefaultFont", 10),
                anchor="w",
                justify="left",
            )
            prompt_label.pack(anchor="w", pady=(0, 14))

        # Eingabefeld mit dünnem, themenkonformem Rahmen und Innenabstand.
        border = tk.Frame(container, bg=self.theme["input_border"])
        border.pack(fill="x")
        field = tk.Frame(border, bg=self.theme["input"])
        field.pack(fill="x", padx=1, pady=1)
        entry = tk.Entry(
            field,
            bg=self.theme["input"],
            fg=self.theme["text"],
            insertbackground=self.theme["text"],
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=("TkDefaultFont", 12),
        )
        entry.pack(fill="x", padx=12, pady=9)
        entry.insert(0, initial or "")
        entry.select_range(0, "end")

        button_row = tk.Frame(container, bg=self.theme["bg"])
        button_row.pack(fill="x", pady=(20, 0))

        def submit(event=None):
            result["value"] = entry.get()
            dialog.destroy()
            return "break"

        def cancel(event=None):
            result["value"] = None
            dialog.destroy()
            return "break"

        ok_button = self._make_dialog_button(button_row, ok_text, submit, accent_key)
        cancel_button = self._make_dialog_button(button_row, "Abbrechen", cancel, "muted")
        ok_button.pack(side="right")
        cancel_button.pack(side="right", padx=(0, 10))

        dialog.bind("<Return>", submit)
        dialog.bind("<Escape>", cancel)
        dialog.protocol("WM_DELETE_WINDOW", cancel)

        self._center_dialog(dialog)
        entry.focus_set()
        dialog.grab_set()
        self.root.wait_window(dialog)
        return result["value"]

    MONTHS_DE = ["Januar", "Februar", "März", "April", "Mai", "Juni",
                 "Juli", "August", "September", "Oktober", "November", "Dezember"]
    WEEKDAYS_DE = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

    def themed_date_picker(self, initial_iso=None):
        """Themebarer Kalender zur Auswahl eines Fälligkeitsdatums.

        Öffnet automatisch im aktuellen Monat (bzw. im Monat des vorhandenen Datums),
        hebt den heutigen Tag und die laufende Woche hervor.
        Rückgabe: ISO-Datum (gewählt), "" (Fälligkeit entfernen) oder None (Abbruch).
        """
        result = {"value": None}
        today = date.today()
        try:
            selected = date.fromisoformat(initial_iso) if initial_iso else None
        except (TypeError, ValueError):
            selected = None
        view = {"year": (selected or today).year, "month": (selected or today).month}

        dialog = tk.Toplevel(self.root)
        dialog.title("Fälligkeit")
        dialog.configure(bg=self.theme["bg"])
        dialog.transient(self.root)
        dialog.resizable(False, False)

        container = tk.Frame(dialog, bg=self.theme["bg"])
        container.pack(fill="both", expand=True, padx=22, pady=20)

        tk.Label(
            container, text="Fälligkeit wählen", bg=self.theme["bg"], fg=self.theme["text"],
            font=("TkDefaultFont", 15, "bold"), anchor="w",
        ).pack(anchor="w", pady=(0, 14))

        header = tk.Frame(container, bg=self.theme["bg"])
        header.pack(fill="x", pady=(0, 10))
        month_label = tk.Label(
            header, bg=self.theme["bg"], fg=self.theme["text"], font=("TkDefaultFont", 12, "bold"),
        )

        def shift_month(delta):
            index = view["month"] - 1 + delta
            view["year"] += index // 12
            view["month"] = index % 12 + 1
            render()

        prev_btn = RoundedButton(
            header, text="\u2039", command=lambda: shift_month(-1),
            border_color=self.theme["line"], hover_fill=self.theme["accent"], text_color=self.theme["text"],
            bg_color=self.theme["bg"], width=40, height=34, radius=12, font=("TkDefaultFont", 13, "bold"),
        )
        next_btn = RoundedButton(
            header, text="\u203a", command=lambda: shift_month(1),
            border_color=self.theme["line"], hover_fill=self.theme["accent"], text_color=self.theme["text"],
            bg_color=self.theme["bg"], width=40, height=34, radius=12, font=("TkDefaultFont", 13, "bold"),
        )
        prev_btn.pack(side="left")
        next_btn.pack(side="right")
        month_label.pack(side="left", expand=True)

        grid_wrap = tk.Frame(container, bg=self.theme["bg"])
        grid_wrap.pack()
        cells = {"frame": None}

        def choose(day):
            result["value"] = day.isoformat()
            dialog.destroy()

        def render():
            month_label.config(text=f"{self.MONTHS_DE[view['month'] - 1]} {view['year']}")
            if cells["frame"] is not None:
                cells["frame"].destroy()
            frame = tk.Frame(grid_wrap, bg=self.theme["bg"])
            frame.pack()
            cells["frame"] = frame

            for col, name in enumerate(self.WEEKDAYS_DE):
                tk.Label(
                    frame, text=name, bg=self.theme["bg"], fg=self.theme["muted"],
                    font=("TkDefaultFont", 9, "bold"), width=4,
                ).grid(row=0, column=col, padx=2, pady=(0, 4))

            cal = calendar.Calendar(firstweekday=0)  # Montag zuerst
            weeks = cal.monthdatescalendar(view["year"], view["month"])
            for row, week in enumerate(weeks, start=1):
                for col, day in enumerate(week):
                    in_month = day.month == view["month"]
                    is_today = day == today
                    is_selected = selected is not None and day == selected
                    base_bg = self.theme["bg"]
                    fg = self.theme["text"] if in_month else self.theme["placeholder"]
                    hl_thick, hl_color = 0, self.theme["bg"]
                    if is_selected:
                        base_bg = self.theme["due_action"]; fg = "#FFFFFF"
                    elif is_today:
                        hl_thick, hl_color = 2, self.theme["accent"]; fg = self.theme["accent"]
                    cell = tk.Label(
                        frame, text=str(day.day), width=4, cursor="hand2",
                        font=("TkDefaultFont", 10, "bold"), bg=base_bg, fg=fg,
                        padx=2, pady=6, bd=0,
                        highlightthickness=hl_thick, highlightbackground=hl_color, highlightcolor=hl_color,
                    )
                    cell.grid(row=row, column=col, padx=3, pady=3)
                    cell.bind("<Button-1>", lambda _e, d=day: choose(d))
                    if not is_selected:
                        cell._base_bg = base_bg
                        cell.bind("<Enter>", lambda _e, c=cell: c.configure(bg=self.theme["input"]))
                        cell.bind("<Leave>", lambda _e, c=cell: c.configure(bg=c._base_bg))

        render()

        footer = tk.Frame(container, bg=self.theme["bg"])
        footer.pack(fill="x", pady=(16, 0))

        def pick_today():
            result["value"] = today.isoformat()
            dialog.destroy()

        def clear_due():
            result["value"] = ""
            dialog.destroy()

        def cancel(event=None):
            result["value"] = None
            dialog.destroy()
            return "break"

        today_button = self._make_dialog_button(footer, "Heute", pick_today, "confirm", width=92, height=38)
        clear_button = self._make_dialog_button(footer, "Entfernen", clear_due, "delete", width=104, height=38)
        cancel_button = self._make_dialog_button(footer, "Abbrechen", cancel, "muted", width=104, height=38)
        today_button.pack(side="left")
        cancel_button.pack(side="right")
        clear_button.pack(side="right", padx=(0, 10))

        dialog.bind("<Escape>", cancel)
        dialog.protocol("WM_DELETE_WINDOW", cancel)
        self._center_dialog(dialog, min_width=360)
        dialog.grab_set()
        self.root.wait_window(dialog)
        return result["value"]


    # -----------------------------
    # Mehrere Listen / Seitenregister
    # -----------------------------
    def new_list_object(self, title=None, items=None, list_id=None, folder_id=None, color=None):
        title = (title or "Neue Liste").strip() or "Neue Liste"
        return {
            "id": list_id or uuid.uuid4().hex,
            "title": title,
            "folder_id": folder_id if isinstance(folder_id, str) and folder_id else None,
            "color": color if color in self.LIST_COLOR_KEYS else None,
            "items": items if isinstance(items, list) else [],
        }

    def new_folder_object(self, title=None, folder_id=None, color=None):
        title = (title or "Neuer Ordner").strip() or "Neuer Ordner"
        return {
            "id": folder_id or uuid.uuid4().hex,
            "title": title,
            "color": color if color in self.LIST_COLOR_KEYS else None,
        }

    def current_list(self):
        if not self.lists:
            self.lists = [self.new_list_object(self.app_title, self.items)]
            self.active_list_id = self.lists[0]["id"]
        for entry in self.lists:
            if entry.get("id") == self.active_list_id:
                return entry
        self.active_list_id = self.lists[0]["id"]
        return self.lists[0]

    def sync_current_list_reference(self):
        current = self.current_list()
        current["items"] = self.items
        current["title"] = self.app_title

    def set_active_list(self, list_id, refresh=True):
        if not list_id:
            return
        target = None
        for entry in self.lists:
            if entry.get("id") == list_id:
                target = entry
                break
        if target is None:
            return

        if self.active_list_id and self.lists:
            self.sync_current_list_reference()

        self.active_list_id = target["id"]
        self.items = target.setdefault("items", [])
        self.app_title = target.get("title", "Meine Liste").strip() or "Meine Liste"
        self.undo_stack.clear()
        self.expanded_ids = set()
        self.selection_anchor_id = None
        self.update_window_title()
        if hasattr(self, "title_label"):
            self.title_label.configure(text=self.app_title)
        if refresh:
            self.update_sidebar_list()
            self.refresh_tree()
            self.save_settings()

    def create_list_sidebar(self):
        title_row = self.register_theme_widget(tk.Frame(self.sidebar_frame, bg=self.theme["card"]), "card")
        title_row.pack(fill="x", pady=(4, 10))

        self.sidebar_title = self.register_theme_widget(
            tk.Label(
                title_row,
                text="Listen",
                font=("TkDefaultFont", 12, "bold"),
                bg=self.theme["card"],
                fg=self.theme["text"],
                anchor="w",
            ),
            "card",
            "text",
        )
        self.sidebar_title.pack(side="left", fill="x", expand=True, padx=(10, 0))

        self.add_list_button = self.make_button(
            title_row,
            text="+",
            command=self.create_new_list,
            color_key="accent",
            width=42,
            height=32,
            radius=14,
            bg_key="card",
            font=("TkDefaultFont", 13, "bold"),
        )
        self.add_list_button.pack(side="right")

        self.sidebar_listbox = ttk.Treeview(
            self.sidebar_frame,
            show="tree",
            selectmode="browse",
            style="Sidebar.Treeview",
            takefocus=True,
        )
        self.sidebar_listbox.pack(fill="both", expand=True)
        self.sidebar_listbox.heading("#0", text="")
        self.sidebar_listbox.column("#0", anchor="w", stretch=True, width=220)
        self.sidebar_listbox.bind("<<TreeviewSelect>>", self.on_sidebar_select)
        self.sidebar_listbox.bind("<Double-Button-1>", self.edit_selected_sidebar_title)
        self.sidebar_listbox.bind("<Tab>", self.toggle_sidebar_indent)
        self.sidebar_listbox.bind("<Shift-Tab>", self.outdent_selected_sidebar_list)
        self.sidebar_listbox.bind("<ISO_Left_Tab>", self.outdent_selected_sidebar_list)
        self.sidebar_listbox.bind("<ButtonPress-1>", self.on_sidebar_drag_start)
        self.sidebar_listbox.bind("<B1-Motion>", self.on_sidebar_drag_motion)
        self.sidebar_listbox.bind("<ButtonRelease-1>", self.on_sidebar_drag_end)
        self.sidebar_listbox.bind("<Button-3>", self.show_sidebar_context_menu)
        self.sidebar_listbox.bind("<Button-2>", self.show_sidebar_context_menu)
        self.sidebar_listbox.bind("<Control-Button-1>", self.show_sidebar_context_menu)
        self.bind_mousewheel(self.sidebar_listbox)

        # Untere Seitenleisten-Aktionen in einem gemeinsamen Grid.
        # Dadurch liegen die unteren Kanten sauber auf einer Linie und die Abstände bleiben stabil.
        sidebar_actions = self.register_theme_widget(tk.Frame(self.sidebar_frame, bg=self.theme["card"]), "card")
        sidebar_actions.pack(side="bottom", fill="x", pady=(10, 0))
        sidebar_actions.columnconfigure((0, 1), weight=1, uniform="sidebar_actions")

        self.import_list_button = self.make_button(
            sidebar_actions,
            text="Liste importieren",
            command=self.import_txt_as_new_lists,
            color_key="import",
            width=150,
            height=38,
            radius=16,
            bg_key="card",
            font=("TkDefaultFont", 8, "bold"),
        )
        self.import_list_button.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        self.add_folder_button = self.make_button(
            sidebar_actions,
            text="+ Neuer Ordner",
            command=self.create_new_folder,
            color_key="accent",
            width=150,
            height=38,
            radius=16,
            bg_key="card",
            font=("TkDefaultFont", 8, "bold"),
        )
        self.add_folder_button.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        self.rename_list_button = self.make_button(
            sidebar_actions,
            text="Titel",
            command=self.edit_selected_sidebar_title,
            color_key="accent",
            width=76,
            height=38,
            radius=16,
            bg_key="card",
            font=("TkDefaultFont", 8, "bold"),
        )
        self.rename_list_button.grid(row=2, column=0, sticky="ew", padx=(0, 6))

        self.delete_list_button = self.make_button(
            sidebar_actions,
            text="–",
            command=self.delete_selected_sidebar_entry,
            color_key="delete",
            width=46,
            height=38,
            radius=16,
            bg_key="card",
            font=("TkDefaultFont", 13, "bold"),
        )
        self.delete_list_button.grid(row=2, column=1, sticky="ew")

    def update_sidebar_list(self):
        if not hasattr(self, "sidebar_listbox"):
            return
        self._updating_sidebar = True
        try:
            self.sidebar_rows = []
            self.sidebar_iid_to_row = {}
            for row_id in self.sidebar_listbox.get_children(""):
                self.sidebar_listbox.delete(row_id)

            assigned_folder_ids = {folder.get("id") for folder in self.folders if isinstance(folder, dict)}

            # Listen ohne Ordner zuerst anzeigen.
            for entry in self.lists:
                folder_id = entry.get("folder_id")
                if folder_id in assigned_folder_ids:
                    continue
                self._insert_sidebar_list_row(entry, parent="")

            # Danach Ordner mit enthaltenen Listen.
            for folder in self.folders:
                folder_id = folder.get("id")
                if not folder_id:
                    continue
                folder_title = str(folder.get("title") or "Ordner").strip() or "Ordner"
                child_lists = [entry for entry in self.lists if entry.get("folder_id") == folder_id]
                iid = f"folder:{folder_id}"
                preview = f"{folder_title}  ({len(child_lists)})"
                folder_color = folder.get("color") if folder.get("color") in self.LIST_COLOR_KEYS else None
                folder_tags = (f"listcolor_{folder_color}",) if folder_color else ("folder",)
                self.sidebar_listbox.insert("", "end", iid=iid, text=preview, open=True, tags=folder_tags)
                self.sidebar_rows.append(("folder", folder_id))
                self.sidebar_iid_to_row[iid] = ("folder", folder_id)
                for entry in child_lists:
                    self._insert_sidebar_list_row(entry, parent=iid)

            active_iid = f"list:{self.active_list_id}" if self.active_list_id else None
            if active_iid and self.sidebar_listbox.exists(active_iid):
                self.sidebar_listbox.selection_set(active_iid)
                self.sidebar_listbox.focus(active_iid)
                self.sidebar_listbox.see(active_iid)
            elif self.sidebar_listbox.get_children(""):
                first = self.sidebar_listbox.get_children("")[0]
                self.sidebar_listbox.selection_set(first)
                self.sidebar_listbox.focus(first)
        finally:
            self._updating_sidebar = False

    def _insert_sidebar_list_row(self, entry, parent=""):
        title = entry.get("title", "Meine Liste").strip() or "Meine Liste"
        item_count = self.count_items(entry.get("items", []))
        item_id = entry.get("id")
        if not item_id:
            item_id = uuid.uuid4().hex
            entry["id"] = item_id
        color_key = entry.get("color") if entry.get("color") in self.LIST_COLOR_KEYS else None
        preview = f"{title}  ({item_count})"
        iid = f"list:{item_id}"
        tags = (f"listcolor_{color_key}",) if color_key else ("list",)
        self.sidebar_listbox.insert(parent, "end", iid=iid, text=preview, tags=tags)
        self.sidebar_rows.append(("list", item_id))
        self.sidebar_iid_to_row[iid] = ("list", item_id)

    def get_selected_sidebar_row(self):
        if not hasattr(self, "sidebar_listbox"):
            return None
        selection = self.sidebar_listbox.selection()
        if not selection:
            return None
        return self.sidebar_iid_to_row.get(selection[0])

    def get_sidebar_iid_for_row(self, row):
        if not row:
            return None
        row_type, row_id = row
        return f"{row_type}:{row_id}"

    def on_sidebar_select(self, event=None):
        if getattr(self, "_updating_sidebar", False):
            return
        row = self.get_selected_sidebar_row()
        if not row:
            return
        row_type, row_id = row
        if row_type == "list" and row_id != self.active_list_id:
            self.set_active_list(row_id)

    def edit_selected_sidebar_title(self, event=None):
        row = self.get_selected_sidebar_row()
        if row and row[0] == "folder":
            return self.edit_folder_title(row[1])
        return self.edit_title()

    def show_sidebar_context_menu(self, event):
        """Rechtsklick auf eine Liste oder einen Ordner: schnelle Farbauswahl."""
        iid = self.sidebar_listbox.identify_row(event.y)
        if not iid:
            return "break"
        row = self.sidebar_iid_to_row.get(iid)
        if not row:
            return "break"
        row_type, row_id = row
        if row_type == "folder":
            entries = self.folders
            heading = "Ordnerfarbe"
            setter = self.set_folder_color
        else:
            entries = self.lists
            heading = "Listenfarbe"
            setter = self.set_list_color
        current = next((e.get("color") for e in entries if e.get("id") == row_id), None)

        menu = tk.Menu(
            self.root,
            tearoff=0,
            bg=self.theme["card"],
            fg=self.theme["text"],
            activebackground=self.theme["accent"],
            activeforeground="#FFFFFF",
            bd=0,
            relief="flat",
        )
        menu.add_command(label=heading, state="disabled")
        menu.add_separator()
        for label, color_key in self.LIST_COLOR_CHOICES:
            prefix = "\u2713 " if current == color_key else "      "
            menu.add_command(
                label=f"{prefix}{label}",
                foreground=self.theme[color_key],
                command=lambda c=color_key: setter(row_id, c),
            )
        menu.add_separator()
        prefix = "\u2713 " if not current else "      "
        menu.add_command(label=f"{prefix}Keine Farbe", command=lambda: setter(row_id, None))
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
        return "break"

    def set_list_color(self, list_id, color_key):
        """Setzt oder entfernt die Farbe einer Liste und speichert die Änderung."""
        self._apply_entry_color(self.lists, list_id, color_key)

    def set_folder_color(self, folder_id, color_key):
        """Setzt oder entfernt die Farbe eines Ordners und speichert die Änderung."""
        self._apply_entry_color(self.folders, folder_id, color_key)

    def _apply_entry_color(self, entries, entry_id, color_key):
        entry = next((e for e in entries if e.get("id") == entry_id), None)
        if not entry:
            return
        new_color = color_key if color_key in self.LIST_COLOR_KEYS else None
        if entry.get("color") == new_color:
            return
        entry["color"] = new_color
        self.save_items()  # aktualisiert auch die Seitenleiste

    def edit_folder_title(self, folder_id):
        folder = next((entry for entry in self.folders if entry.get("id") == folder_id), None)
        if not folder:
            return "break"
        current_title = folder.get("title", "Ordner")
        new_title = self.themed_input_dialog("Ordner umbenennen", "Neuer Ordnertitel:", initial=current_title, ok_text="Speichern")
        if new_title is None:
            return "break"
        new_title = new_title.strip()
        if not new_title:
            messagebox.showwarning("Hinweis", "Bitte einen Titel eingeben.")
            return "break"
        folder["title"] = new_title
        self.save_items()
        self.update_sidebar_list()
        return "break"

    def create_new_folder(self, event=None):
        title = self.themed_input_dialog("Neuer Ordner", "Titel des neuen Ordners:", ok_text="Anlegen")
        if title is None:
            return "break"
        self.folders.append(self.new_folder_object(title.strip() or "Neuer Ordner"))
        self.save_items()
        self.update_sidebar_list()
        return "break"

    def delete_selected_sidebar_entry(self, event=None):
        row = self.get_selected_sidebar_row()
        if row and row[0] == "folder":
            return self.delete_folder(row[1])
        return self.delete_current_list(event)

    def delete_folder(self, folder_id):
        folder = next((entry for entry in self.folders if entry.get("id") == folder_id), None)
        if not folder:
            return "break"
        title = folder.get("title", "Ordner")
        if not messagebox.askyesno("Ordner löschen", f"Ordner '{title}' löschen?\n\nDie enthaltenen Listen bleiben erhalten und werden auf die Hauptebene verschoben."):
            return "break"
        for entry in self.lists:
            if entry.get("folder_id") == folder_id:
                entry["folder_id"] = None
        self.folders = [entry for entry in self.folders if entry.get("id") != folder_id]
        self.save_items()
        self.update_sidebar_list()
        return "break"

    def get_sidebar_visible_iids(self):
        if not hasattr(self, "sidebar_listbox"):
            return []
        result = []
        def collect(parent=""):
            for iid in self.sidebar_listbox.get_children(parent):
                result.append(iid)
                collect(iid)
        collect("")
        return result

    def toggle_sidebar_indent(self, event=None):
        row = self.get_selected_sidebar_row()
        if not row or row[0] != "list":
            return "break"
        list_entry = next((entry for entry in self.lists if entry.get("id") == row[1]), None)
        if not list_entry:
            return "break"
        if list_entry.get("folder_id"):
            list_entry["folder_id"] = None
            self.save_items()
            self.update_sidebar_list()
            return "break"

        selected_iid = f"list:{row[1]}"
        visible = self.get_sidebar_visible_iids()
        target_folder_id = None
        if selected_iid in visible:
            selected_index = visible.index(selected_iid)
            for iid in reversed(visible[:selected_index]):
                row_type, row_id = self.sidebar_iid_to_row.get(iid, (None, None))
                if row_type == "folder":
                    target_folder_id = row_id
                    break
        if not target_folder_id:
            messagebox.showinfo("Hinweis", "Zum Einrücken muss oberhalb ein Ordner vorhanden sein. Lege zuerst über '+ Neuer Ordner' einen Ordner an.")
            return "break"
        list_entry["folder_id"] = target_folder_id
        self.save_items()
        self.update_sidebar_list()
        return "break"

    def outdent_selected_sidebar_list(self, event=None):
        row = self.get_selected_sidebar_row()
        if not row or row[0] != "list":
            return "break"
        list_entry = next((entry for entry in self.lists if entry.get("id") == row[1]), None)
        if list_entry:
            list_entry["folder_id"] = None
            self.save_items()
            self.update_sidebar_list()
        return "break"

    def on_sidebar_drag_start(self, event):
        iid = self.sidebar_listbox.identify_row(event.y)
        self.sidebar_drag_start_iid = iid if iid else None
        self.sidebar_drag_start_y = event.y
        self.sidebar_drag_has_moved = False
        if iid:
            self.sidebar_listbox.selection_set(iid)
            self.sidebar_listbox.focus(iid)

    def on_sidebar_drag_motion(self, event):
        if not self.sidebar_drag_start_iid:
            return
        if abs(event.y - self.sidebar_drag_start_y) > 5:
            self.sidebar_drag_has_moved = True
        target_iid = self.sidebar_listbox.identify_row(event.y)
        self.clear_sidebar_drop_target_tags()
        if target_iid and target_iid != self.sidebar_drag_start_iid:
            try:
                tags = set(self.sidebar_listbox.item(target_iid, "tags"))
                tags.add("drop_target")
                self.sidebar_listbox.item(target_iid, tags=tuple(tags))
            except tk.TclError:
                pass

    def on_sidebar_drag_end(self, event):
        source_iid = self.sidebar_drag_start_iid
        target_iid = self.sidebar_listbox.identify_row(event.y)
        moved = self.sidebar_drag_has_moved
        self.sidebar_drag_start_iid = None
        self.sidebar_drag_has_moved = False
        self.clear_sidebar_drop_target_tags()
        if not source_iid or not moved:
            return
        source_row = self.sidebar_iid_to_row.get(source_iid)
        target_row = self.sidebar_iid_to_row.get(target_iid) if target_iid else None
        if not source_row:
            return

        changed = False
        if source_row[0] == "list":
            if target_row and target_row[0] == "folder":
                changed = self.move_sidebar_list_into_folder(source_row[1], target_row[1])
            elif target_row and target_row[0] == "list" and target_row[1] != source_row[1]:
                place = "after"
                try:
                    bbox = self.sidebar_listbox.bbox(target_iid)
                    if bbox:
                        _x, y, _w, h = bbox
                        place = "before" if event.y < y + h / 2 else "after"
                except tk.TclError:
                    pass
                changed = self.move_sidebar_list_relative(source_row[1], target_row[1], place=place)
            elif not target_row:
                changed = self.move_sidebar_list_to_top_level_end(source_row[1])
        elif source_row[0] == "folder":
            if target_row and target_row[0] == "folder" and target_row[1] != source_row[1]:
                place = "after"
                try:
                    bbox = self.sidebar_listbox.bbox(target_iid)
                    if bbox:
                        _x, y, _w, h = bbox
                        place = "before" if event.y < y + h / 2 else "after"
                except tk.TclError:
                    pass
                changed = self.move_sidebar_folder_relative(source_row[1], target_row[1], place=place)
            elif not target_row:
                changed = self.move_sidebar_folder_to_end(source_row[1])
        if changed:
            self.save_items()
            self.update_sidebar_list()

    def clear_sidebar_drop_target_tags(self):
        if not hasattr(self, "sidebar_listbox"):
            return
        for iid in self.get_sidebar_visible_iids():
            try:
                tags = tuple(tag for tag in self.sidebar_listbox.item(iid, "tags") if tag != "drop_target")
                self.sidebar_listbox.item(iid, tags=tags)
            except tk.TclError:
                pass

    def move_sidebar_list_into_folder(self, list_id, folder_id):
        list_entry = next((entry for entry in self.lists if entry.get("id") == list_id), None)
        if not list_entry or not any(folder.get("id") == folder_id for folder in self.folders):
            return False
        list_entry["folder_id"] = folder_id
        # In der internen Reihenfolge ans Ende setzen, damit die Sortierung innerhalb des Ordners nachvollziehbar ist.
        self.lists = [entry for entry in self.lists if entry.get("id") != list_id]
        self.lists.append(list_entry)
        return True

    def move_sidebar_list_relative(self, source_id, target_id, place="after"):
        if source_id == target_id:
            return False
        source = next((entry for entry in self.lists if entry.get("id") == source_id), None)
        target = next((entry for entry in self.lists if entry.get("id") == target_id), None)
        if not source or not target:
            return False
        self.lists = [entry for entry in self.lists if entry.get("id") != source_id]
        target_index = next((idx for idx, entry in enumerate(self.lists) if entry.get("id") == target_id), len(self.lists))
        source["folder_id"] = target.get("folder_id")
        insert_index = target_index if place == "before" else target_index + 1
        self.lists.insert(insert_index, source)
        return True

    def move_sidebar_list_to_top_level_end(self, list_id):
        source = next((entry for entry in self.lists if entry.get("id") == list_id), None)
        if not source:
            return False
        self.lists = [entry for entry in self.lists if entry.get("id") != list_id]
        source["folder_id"] = None
        self.lists.append(source)
        return True

    def move_sidebar_folder_relative(self, source_id, target_id, place="after"):
        if source_id == target_id:
            return False
        source = next((entry for entry in self.folders if entry.get("id") == source_id), None)
        if not source:
            return False
        self.folders = [entry for entry in self.folders if entry.get("id") != source_id]
        target_index = next((idx for idx, entry in enumerate(self.folders) if entry.get("id") == target_id), len(self.folders))
        insert_index = target_index if place == "before" else target_index + 1
        self.folders.insert(insert_index, source)
        return True

    def move_sidebar_folder_to_end(self, folder_id):
        source = next((entry for entry in self.folders if entry.get("id") == folder_id), None)
        if not source:
            return False
        self.folders = [entry for entry in self.folders if entry.get("id") != folder_id]
        self.folders.append(source)
        return True

    def create_new_list(self, event=None):
        title = self.themed_input_dialog("Neue Liste", "Titel der neuen Liste:", ok_text="Anlegen")
        if title is None:
            return "break"
        title = title.strip() or "Neue Liste"
        self.sync_current_list_reference()
        new_entry = self.new_list_object(title, [])
        self.lists.append(new_entry)
        self.set_active_list(new_entry["id"])
        self.save_items()
        return "break"

    def delete_current_list(self, event=None):
        if len(self.lists) <= 1:
            messagebox.showinfo("Liste löschen", "Die letzte Liste kann nicht gelöscht werden.")
            return "break"
        current = self.current_list()
        title = current.get("title", "Diese Liste")
        if not messagebox.askyesno("Liste löschen", f"Liste '{title}' wirklich löschen?"):
            return "break"
        delete_id = current.get("id")
        self.lists = [entry for entry in self.lists if entry.get("id") != delete_id]
        next_id = self.lists[0]["id"]
        self.active_list_id = None
        self.set_active_list(next_id)
        self.save_items()
        return "break"

    def normalize_lists_data(self, data):
        self.folders = []
        if isinstance(data, dict) and isinstance(data.get("lists"), list):
            folder_ids = set()
            raw_folders = data.get("folders", []) if isinstance(data.get("folders", []), list) else []
            for folder in raw_folders:
                if not isinstance(folder, dict):
                    continue
                folder_id = folder.get("id") if isinstance(folder.get("id"), str) and folder.get("id") else uuid.uuid4().hex
                title = str(folder.get("title") or "Ordner").strip() or "Ordner"
                color = folder.get("color") if folder.get("color") in self.LIST_COLOR_KEYS else None
                self.folders.append(self.new_folder_object(title, folder_id, color))
                folder_ids.add(folder_id)

            lists = []
            for entry in data.get("lists", []):
                if not isinstance(entry, dict):
                    continue
                title = str(entry.get("title") or "Meine Liste").strip() or "Meine Liste"
                list_id = entry.get("id") if isinstance(entry.get("id"), str) and entry.get("id") else None
                folder_id = entry.get("folder_id") if entry.get("folder_id") in folder_ids else None
                items = self.normalize_items(entry.get("items", []))
                color = entry.get("color") if entry.get("color") in self.LIST_COLOR_KEYS else None
                lists.append(self.new_list_object(title, items, list_id, folder_id, color))
            active_id = data.get("active_list_id") if isinstance(data.get("active_list_id"), str) else None
            return lists, active_id

        # Abwärtskompatibilität: alte Speicherdatei war direkt eine Item-Liste.
        title = self.settings.get("title", "Meine Liste") if isinstance(self.settings, dict) else "Meine Liste"
        self.folders = []
        return [self.new_list_object(str(title).strip() or "Meine Liste", self.normalize_items(data))], None

    # -----------------------------
    # UI
    # -----------------------------
    def create_ui(self):
        self.create_menubar()
        self.shell = self.register_theme_widget(tk.Frame(self.root, bg=self.theme["bg"]), "bg")
        self.shell.pack(fill="both", expand=True, padx=28, pady=24)

        # Kopfbereich über die volle Fensterbreite: Titel wieder ganz links.
        top_frame = self.register_theme_widget(tk.Frame(self.shell, bg=self.theme["bg"]), "bg")
        top_frame.pack(fill="x")

        title_block = self.register_theme_widget(tk.Frame(top_frame, bg=self.theme["bg"]), "bg")
        title_block.pack(side="left", fill="x", expand=True)

        title_row = self.register_theme_widget(tk.Frame(title_block, bg=self.theme["bg"]), "bg")
        title_row.pack(anchor="w", fill="x", pady=(0, 4))

        self.title_label = self.register_theme_widget(
            tk.Label(
                title_row,
                text=self.app_title,
                font=("TkDefaultFont", 24, "bold"),
                bg=self.theme["bg"],
                fg=self.theme["text"],
                cursor="hand2",
            ),
            "bg",
            "text",
        )
        self.title_label.pack(side="left", anchor="w")
        self.title_label.bind("<Double-Button-1>", lambda event: self.edit_title())

        self.theme_button = self.make_button(
            top_frame,
            text="Dark Mode" if self.theme_name == "light" else "Light Mode",
            command=self.toggle_theme,
            color_key="theme_toggle",
            width=122,
        )
        self.theme_button.pack(side="right", padx=(12, 0), pady=(0, 4))

        # Eingabebereich über die volle Fensterbreite.
        input_frame = self.register_theme_widget(tk.Frame(self.shell, bg=self.theme["bg"]), "bg")
        input_frame.pack(fill="x", pady=(20, 14))

        self.entry_border = self.make_rounded_container(
            input_frame,
            fill_key="input",
            outline_key="input_border",
            radius=16,
            padding=1,
            height=42,
            inner_pad_x=10,
            inner_pad_y=5,
        )
        self.entry_border.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_border.pack_propagate(False)
        self.entry_inner = self.entry_border.inner

        self.entry = tk.Entry(
            self.entry_inner,
            font=("TkDefaultFont", 12),
            bg=self.theme["input"],
            fg=self.theme["text"],
            insertbackground=self.theme["text"],
            relief="flat",
            bd=0,
            borderwidth=0,
            highlightthickness=0,
            highlightbackground=self.theme["input"],
            highlightcolor=self.theme["input"],
            selectborderwidth=0,
        )
        self.entry.pack(fill="both", expand=True, ipady=0, padx=(2, 2), pady=0)
        self.entry.bind("<Return>", self.on_entry_return)
        self.entry.bind("<FocusIn>", self.clear_entry_placeholder)
        self.entry.bind("<FocusOut>", self.set_entry_placeholder)

        self.add_button = self.make_button(
            input_frame,
            text="Hinzufügen",
            command=self.add_item,
            color_key="export",
            width=132,
        )
        self.add_button.pack(side="right")

        # Suche / Filter über die volle Fensterbreite.
        self.search_frame = self.register_theme_widget(tk.Frame(self.shell, bg=self.theme["bg"]), "bg")
        self.search_frame.pack(fill="x", pady=(0, 14))
        self.search_frame.bind("<Configure>", self.update_responsive_filter_visibility)

        self.clear_search_button = self.make_button(
            self.search_frame,
            text="Suche löschen",
            command=self.clear_search,
            color_key="flag",
            width=126,
            height=38,
            radius=16,
            font=("TkDefaultFont", 9, "bold"),
        )
        self.clear_search_button.pack(side="right")

        self.hide_done_box_border = self.make_rounded_container(
            self.search_frame,
            fill_key="input",
            outline_key="input_border",
            radius=16,
            padding=1,
            width=178,
            height=42,
            inner_pad_x=10,
            inner_pad_y=5,
        )
        self.hide_done_box_border.pack(side="left", fill="y", padx=(0, 10))
        self.hide_done_box_border.pack_propagate(False)
        self.hide_done_box_inner = self.hide_done_box_border.inner

        self.hide_done_check = tk.Checkbutton(
            self.hide_done_box_inner,
            text="Nur offene Punkte",
            variable=self.hide_done_var,
            command=self.on_open_only_changed,
            bg=self.theme["input"],
            fg=self.theme["text"],
            activebackground=self.theme["input"],
            activeforeground=self.theme["text"],
            selectcolor=self.theme["input"],
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=("TkDefaultFont", 10),
            cursor="hand2",
            takefocus=1,
            anchor="w",
        )
        self.hide_done_check.pack(fill="both", expand=True, ipady=0, padx=(2, 2), pady=0)

        self.done_only_box_border = self.make_rounded_container(
            self.search_frame,
            fill_key="input",
            outline_key="input_border",
            radius=16,
            padding=1,
            width=192,
            height=42,
            inner_pad_x=10,
            inner_pad_y=5,
        )
        self.done_only_box_border.pack(side="left", fill="y", padx=(0, 10))
        self.done_only_box_border.pack_propagate(False)
        self.done_only_box_inner = self.done_only_box_border.inner

        self.show_done_only_check = tk.Checkbutton(
            self.done_only_box_inner,
            text="Nur erledigte Punkte",
            variable=self.show_done_only_var,
            command=self.on_done_only_changed,
            bg=self.theme["input"],
            fg=self.theme["text"],
            activebackground=self.theme["input"],
            activeforeground=self.theme["text"],
            selectcolor=self.theme["input"],
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=("TkDefaultFont", 10),
            cursor="hand2",
            takefocus=1,
            anchor="w",
        )
        self.show_done_only_check.pack(fill="both", expand=True, ipady=0, padx=(2, 2), pady=0)

        self.search_border = self.make_rounded_container(
            self.search_frame,
            fill_key="input",
            outline_key="input_border",
            radius=16,
            padding=1,
            height=42,
            inner_pad_x=10,
            inner_pad_y=5,
        )
        self.search_border.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_border.pack_propagate(False)
        self.search_inner = self.search_border.inner

        self.search_entry = tk.Entry(
            self.search_inner,
            textvariable=self.search_var,
            font=("TkDefaultFont", 11),
            bg=self.theme["input"],
            fg=self.theme["text"],
            insertbackground=self.theme["text"],
            relief="flat",
            bd=0,
            borderwidth=0,
            highlightthickness=0,
            highlightbackground=self.theme["input"],
            highlightcolor=self.theme["input"],
            selectborderwidth=0,
        )
        self.search_entry.pack(fill="both", expand=True, ipady=0, padx=(2, 2), pady=0)
        self.search_entry.bind("<FocusIn>", self.clear_search_placeholder)
        self.search_entry.bind("<FocusOut>", self.set_search_placeholder)
        self.search_var.trace_add("write", lambda *_: self.refresh_tree())
        self.set_entry_placeholder()
        self.set_search_placeholder()

        # Unterhalb von Titel/Eingabe/Suche: links das Listenregister, rechts die aktive Liste.
        self.main_area = self.register_theme_widget(tk.Frame(self.shell, bg=self.theme["bg"]), "bg")
        self.main_area.pack(fill="both", expand=True)

        self.sidebar_shell = self.make_rounded_container(
            self.main_area,
            fill_key="card",
            outline_key="line",
            radius=18,
            padding=10,
            width=250,
        )
        # Gleicher oberer/unterer Außenabstand wie der rechte Listenbereich,
        # damit Seitenleisten-Box und Listenpunkt-Box exakt auf derselben Höhe starten.
        self.sidebar_shell.pack(side="left", fill="y", padx=(0, 18), pady=(6, 14))
        self.sidebar_shell.pack_propagate(False)
        self.sidebar_frame = self.register_theme_widget(tk.Frame(self.sidebar_shell.inner, bg=self.theme["card"]), "card")
        self.sidebar_frame.pack(fill="both", expand=True)
        self.create_list_sidebar()

        self.content_frame = self.register_theme_widget(tk.Frame(self.main_area, bg=self.theme["bg"]), "bg")
        self.content_frame.pack(side="left", fill="both", expand=True)

        # Listenbereich mit echter Hierarchie über Treeview
        self.list_frame_outer = self.make_rounded_container(
            self.content_frame,
            fill_key="card",
            outline_key="line",
            radius=18,
            padding=10,
        )
        self.list_frame_outer.pack(fill="both", expand=True, pady=(6, 4))
        self.list_frame = self.register_theme_widget(tk.Frame(self.list_frame_outer.inner, bg=self.theme["card"]), "card")
        self.list_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            self.list_frame,
            show="tree",
            selectmode="extended",
            style="App.Treeview",
        )
        self.tree.pack(side="left", fill="both", expand=True, padx=(14, 14), pady=14)
        self.tree.heading("#0", text="")
        self.tree.column("#0", anchor="w", stretch=True, width=520)

        self.scrollbar = ThemedAutoScrollbar(
            self.list_frame,
            bg_color=self.theme["card"],
            track_color=self.theme["card"],
            thumb_color=self.theme["input_border"],
            active_thumb_color=self.theme["muted"],
            width=14,
        )
        self.scrollbar_visible = False
        self.tree.config(yscrollcommand=self.on_tree_scroll)
        self.scrollbar.set_command(self.tree.yview)

        # Drag & Drop: Ohne Shift wird nur die Reihenfolge geändert.
        # Mit Shift + Drag auf einen Punkt wird ein Unterpunkt erstellt.
        # Shift + Klick wird beim Loslassen als Bereichsauswahl ausgewertet.
        # Shift + Drag bleibt dadurch weiterhin für "Unterpunkt erstellen" nutzbar.
        self.tree.bind("<ButtonPress-1>", self.on_drag_start)
        self.tree.bind("<B1-Motion>", self.on_drag_motion)
        self.tree.bind("<ButtonRelease-1>", self.on_drag_end)
        self.tree.bind("<Double-Button-1>", self.toggle_done)
        self.tree.bind("<Button-3>", self.cycle_importance_from_click)
        self.tree.bind("<Button-2>", self.cycle_importance_from_click)
        self.tree.bind("<Control-Button-1>", self.cycle_importance_from_click)
        self.tree.bind("<Tab>", self.toggle_indent_selected)
        self.tree.bind("<space>", self.toggle_done)
        self.bind_mousewheel(self.tree)

        self.hint_label = self.register_theme_widget(
            tk.Label(
                self.content_frame,
                text="Drag & Drop: Reihenfolge ändern · Shift + Drag: Unterpunkt · Shift + Klick: Bereich auswählen · Strg+A: alle auswählen · Tab: ein-/ausrücken · Strg+F: Suche · Strg+Shift+F/Rechtsklick: Wichtigkeit · Strg+T: Fälligkeit · Strg+Z: Rückgängig · Strg+C/V: Kopieren/Einfügen · F2: Bearbeiten",
                font=("TkDefaultFont", 9),
                bg=self.theme["bg"],
                fg=self.theme["muted"],
                wraplength=900,
                justify="left",
            ),
            "bg",
            "muted",
        )
        self.hint_label.pack(anchor="w", fill="x", pady=(0, 8))
        self.hint_label.bind("<Configure>", lambda event: self.hint_label.configure(wraplength=max(240, event.width)))

        # Steuer-Buttons: Outline standardmäßig, gefüllt beim Hover
        # Gemeinsamer Helfer: ein Paar zusammengehöriger Aktionen in einer sichtbaren Box.
        def make_action_group(parent, column, padx, height):
            group = self.make_rounded_container(
                parent, fill_key="card", outline_key="line", radius=16, padding=7, height=height
            )
            group.grid(row=0, column=column, sticky="ew", padx=padx)
            group.inner.columnconfigure((0, 1), weight=1, uniform="pair")
            return group

        top_opts = {"width": 104, "height": 42, "radius": 17, "font": ("TkDefaultFont", 9, "bold"), "bg_key": "card"}
        util_opts = {"width": 100, "height": 38, "radius": 17, "font": ("TkDefaultFont", 8, "bold"), "bg_key": "card"}

        # Erste Aktionsreihe – drei gruppierte Paare:
        # Liste leeren & Löschen · Wichtigkeit & Fällig · Export & Import.
        button_frame = self.register_theme_widget(tk.Frame(self.content_frame, bg=self.theme["bg"]), "bg")
        button_frame.pack(fill="x", pady=(0, 8))
        button_frame.columnconfigure((0, 1, 2), weight=1, uniform="action_groups")

        group_cleardel = make_action_group(button_frame, 0, (0, 12), 60)
        self.clear_button = self.make_button(group_cleardel.inner, "Liste leeren", self.clear_list, "clear", **top_opts)
        self.clear_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.delete_button = self.make_button(group_cleardel.inner, "Löschen", self.delete_item, "delete", **top_opts)
        self.delete_button.grid(row=0, column=1, sticky="ew")

        group_mark = make_action_group(button_frame, 1, (0, 12), 60)
        self.flag_button = self.make_button(group_mark.inner, "Wichtigkeit", self.cycle_importance_selected, "flag", **top_opts)
        self.flag_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.due_button = self.make_button(group_mark.inner, "Fällig", self.set_due_date_selected, "due_action", **top_opts)
        self.due_button.grid(row=0, column=1, sticky="ew")

        group_io = make_action_group(button_frame, 2, (0, 0), 60)
        self.export_button = self.make_button(group_io.inner, "Export: TXT", self.export_as_txt, "export", **top_opts)
        self.export_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.import_button = self.make_button(group_io.inner, "Import: TXT", self.import_from_txt, "import", **top_opts)
        self.import_button.grid(row=0, column=1, sticky="ew")

        # Zweite Aktionsreihe – drei gruppierte Paare:
        # Bearbeiten & Rückgängig · Kopieren & Einfügen · Aufklappen & Zuklappen.
        utility_frame = self.register_theme_widget(tk.Frame(self.content_frame, bg=self.theme["bg"]), "bg")
        utility_frame.pack(fill="x", pady=(0, 10))
        utility_frame.columnconfigure((0, 1, 2), weight=1, uniform="utility_groups")

        group_edit = make_action_group(utility_frame, 0, (0, 12), 54)
        self.edit_item_button = self.make_button(group_edit.inner, "Bearbeiten", self.edit_item, "accent", **util_opts)
        self.edit_item_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.undo_button = self.make_button(group_edit.inner, "Rückgängig", self.undo_last_change, "accent", **util_opts)
        self.undo_button.grid(row=0, column=1, sticky="ew")

        group_clip = make_action_group(utility_frame, 1, (0, 12), 54)
        self.copy_button = self.make_button(group_clip.inner, "Kopieren", self.copy_selected_to_clipboard, "accent", **util_opts)
        self.copy_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.paste_button = self.make_button(group_clip.inner, "Einfügen", self.paste_items_from_clipboard, "accent", **util_opts)
        self.paste_button.grid(row=0, column=1, sticky="ew")

        group_fold = make_action_group(utility_frame, 2, (0, 0), 54)
        self.expand_button = self.make_button(group_fold.inner, "Aufklappen", self.expand_all, "accent", **util_opts)
        self.expand_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.collapse_button = self.make_button(group_fold.inner, "Zuklappen", self.collapse_all, "accent", **util_opts)
        self.collapse_button.grid(row=0, column=1, sticky="ew")

        # Fortschritts-/Statuszeile: oben rechts, direkt links neben dem Hell-/Dunkel-Umschalter.
        self.stats_label = self.register_theme_widget(
            tk.Label(
                top_frame,
                text="",
                font=("TkDefaultFont", 10),
                bg=self.theme["bg"],
                fg=self.theme["muted"],
                anchor="e",
                justify="right",
            ),
            "bg",
            "muted",
        )
        self.stats_label.pack(side="right", padx=(0, 16), pady=(0, 4))

    def apply_theme(self):
        self.theme = self.THEMES[self.theme_name]
        self.root.configure(bg=self.theme["bg"])

        for widget, bg_key, fg_key in self.theme_widgets:
            try:
                config = {"bg": self.theme[bg_key]}
                if fg_key is not None:
                    config["fg"] = self.theme[fg_key]
                widget.configure(**config)
            except tk.TclError:
                pass

        self.entry.configure(
            bg=self.theme["input"],
            fg=self.theme["placeholder"] if getattr(self, "entry_placeholder_active", False) else self.theme["text"],
            insertbackground=self.theme["text"],
            highlightthickness=0,
            highlightbackground=self.theme["input"],
            highlightcolor=self.theme["input"],
            relief="flat",
            bd=0,
            borderwidth=0,
        )
        if hasattr(self, "search_entry"):
            self.search_entry.configure(
                bg=self.theme["input"],
                fg=self.theme["placeholder"] if getattr(self, "search_placeholder_active", False) else self.theme["text"],
                insertbackground=self.theme["text"],
                highlightthickness=0,
                highlightbackground=self.theme["input"],
                highlightcolor=self.theme["input"],
                relief="flat",
                bd=0,
                borderwidth=0,
            )
        for check_name in ("hide_done_check", "show_done_only_check"):
            check = getattr(self, check_name, None)
            if check is not None:
                check.configure(
                    bg=self.theme["input"],
                    fg=self.theme["text"],
                    activebackground=self.theme["input"],
                    activeforeground=self.theme["text"],
                    selectcolor=self.theme["input"],
                )
        if hasattr(self, "scrollbar"):
            self.scrollbar.set_theme(
                bg_color=self.theme["card"],
                track_color=self.theme["card"],
                thumb_color=self.theme["input_border"],
                active_thumb_color=self.theme["muted"],
            )
        if hasattr(self, "sidebar_listbox"):
            self.style.configure(
                "Sidebar.Treeview",
                background=self.theme["card"],
                fieldbackground=self.theme["card"],
                foreground=self.theme["text"],
                borderwidth=0,
                relief="flat",
                rowheight=34,
                font=("TkDefaultFont", 11),
            )
            try:
                self.style.layout("Sidebar.Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
            except tk.TclError:
                pass
            self.style.map(
                "Sidebar.Treeview",
                background=[("selected", self.theme["selection"])],
                foreground=[("selected", "#FFFFFF")],
            )
            self.sidebar_listbox.tag_configure("folder", foreground=self.theme["muted"])
            self.sidebar_listbox.tag_configure("list", foreground=self.theme["text"])
            self.sidebar_listbox.tag_configure("drop_target", background=self.theme["input_border"])
            for color_key in self.LIST_COLOR_KEYS:
                self.sidebar_listbox.tag_configure(f"listcolor_{color_key}", foreground=self.theme[color_key])

        self.style.configure(
            "App.Treeview",
            background=self.theme["card"],
            fieldbackground=self.theme["card"],
            foreground=self.theme["text"],
            borderwidth=0,
            relief="flat",
            rowheight=36,
            font=("TkDefaultFont", 12),
        )
        try:
            # Entfernt die native Treeview-Rahmen-/Focus-Outline um den Listenbereich.
            self.style.layout("App.Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
        except tk.TclError:
            pass
        self.style.map(
            "App.Treeview",
            background=[("selected", self.theme["selection"])],
            foreground=[("selected", "#FFFFFF")],
        )

        if hasattr(self, "tree"):
            self.tree.tag_configure("open", foreground=self.theme["text"])
            self.tree.tag_configure("priority_low", foreground=self.theme["priority_low"])
            self.tree.tag_configure("priority_medium", foreground=self.theme["priority_medium"])
            self.tree.tag_configure("priority_high", foreground=self.theme["priority_high"])
            self.tree.tag_configure("overdue", foreground=self.theme["overdue"])
            self.tree.tag_configure("due_today", foreground=self.theme["due_today"])
            self.tree.tag_configure("done", foreground=self.theme["muted"])
            self.tree.tag_configure("empty", foreground=self.theme["muted"])
            self.tree.tag_configure("drop_target", background=self.theme["input_border"])

        for button in self.buttons:
            color_key = getattr(button, "color_key", "accent")
            bg_key = getattr(button, "bg_key", "bg")
            hover_text_color = self.theme.get("theme_toggle_hover_text") if color_key == "theme_toggle" else "#FFFFFF"
            button.set_theme(
                bg_color=self.theme[bg_key],
                text_color=self.theme[color_key],
                border_color=self.theme[color_key],
                hover_fill=self.theme[color_key],
                hover_text_color=hover_text_color,
            )

        for container in getattr(self, "rounded_containers", []):
            fill_key = getattr(container, "fill_key", "card")
            outline_key = getattr(container, "outline_key", "line")
            container.set_theme(
                bg_color=self.theme["bg"],
                fill_color=self.theme[fill_key],
                outline_color=self.theme[outline_key],
            )

        if hasattr(self, "theme_button"):
            self.theme_button.set_text("Dark Mode" if self.theme_name == "light" else "Light Mode")

        self.refresh_tree()

    def toggle_theme(self):
        self.theme_name = "dark" if self.theme_name == "light" else "light"
        self.save_theme_setting()
        self.apply_theme()

    # -----------------------------
    # Titel / Fenster
    # -----------------------------
    def edit_title(self):
        new_title = self.themed_input_dialog(
            "Titel bearbeiten",
            "Neuer Listentitel:",
            initial=self.app_title,
            ok_text="Speichern",
        )
        if new_title is None:
            return

        new_title = new_title.strip()
        if not new_title:
            messagebox.showwarning("Hinweis", "Bitte einen Titel eingeben.")
            return

        self.app_title = new_title
        self.current_list()["title"] = new_title
        self.title_label.configure(text=self.app_title)
        self.update_window_title()
        self.update_sidebar_list()
        self.save_items()
        self.save_settings()

    @staticmethod
    def safe_filename(value):
        cleaned = "".join(char if char.isalnum() or char in (" ", "-", "_") else "_" for char in value)
        cleaned = "_".join(cleaned.strip().split())
        return cleaned.lower() or "meine_liste"

    def restore_window_position(self):
        geom_file = os.path.join(BASE_DIR, "window.conf")
        default_geometry = "980x740"
        min_restore_width = 820
        min_restore_height = 660
        try:
            if os.path.exists(geom_file):
                with open(geom_file, "r", encoding="utf-8") as f:
                    geom = f.read().strip()
                match = re.match(r"^(\d+)x(\d+)", geom or "")
                if match:
                    width = int(match.group(1))
                    height = int(match.group(2))
                    if width >= min_restore_width and height >= min_restore_height:
                        self.root.geometry(geom)
                    else:
                        # Alte, zu kleine Fenstergrößen aus früheren Versionen würden die Aktionsleisten abschneiden.
                        self.root.geometry(default_geometry)
                else:
                    self.root.geometry(default_geometry)
        except Exception:
            self.root.geometry(default_geometry)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        try:
            with open(os.path.join(BASE_DIR, "window.conf"), "w", encoding="utf-8") as f:
                f.write(self.root.geometry())
        except Exception:
            pass
        self.cancel_pending_callbacks()
        self.root.destroy()

    def schedule_scrollbar_refresh(self):
        if not hasattr(self, "root"):
            return
        try:
            after_id = self.root.after_idle(self.refresh_scrollbar_state)
            self._after_ids.append(after_id)
        except tk.TclError:
            pass

    def cancel_pending_callbacks(self):
        if not hasattr(self, "root"):
            return
        for after_id in getattr(self, "_after_ids", []):
            try:
                self.root.after_cancel(after_id)
            except tk.TclError:
                pass
        self._after_ids = []

    # -----------------------------
    # Datenmodell / Migration
    # -----------------------------
    def clamp_importance(self, value):
        try:
            value = int(value)
        except (TypeError, ValueError):
            return 0
        return max(0, min(3, value))

    def new_item(self, text, done=False, children=None, item_id=None, importance=0, due=None):
        return {
            "id": item_id or uuid.uuid4().hex,
            "text": str(text),
            "done": bool(done),
            "importance": self.clamp_importance(importance),
            "due": self.normalize_due(due),
            "children": children if isinstance(children, list) else [],
        }

    @staticmethod
    def normalize_due(value):
        """Akzeptiert ein ISO-Datum (JJJJ-MM-TT) oder None und liefert ein sauberes ISO-Datum bzw. None."""
        if not value or not isinstance(value, str):
            return None
        value = value.strip()
        try:
            return datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            return None

    @staticmethod
    def parse_due_input(text):
        """Wandelt Nutzereingaben in ein ISO-Datum um.

        Rückgaben: ISO-String bei Erfolg, '' wenn das Datum entfernt werden soll
        (leere Eingabe), oder None bei ungültiger Eingabe.
        """
        if text is None:
            return None
        text = text.strip()
        if not text:
            return ""
        for fmt in ("%d.%m.%Y", "%d.%m.%y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return None

    @staticmethod
    def format_due_display(iso_value):
        """Formatiert ein ISO-Datum als TT.MM.JJJJ für die Anzeige."""
        if not iso_value:
            return ""
        try:
            return datetime.strptime(iso_value, "%Y-%m-%d").strftime("%d.%m.%Y")
        except ValueError:
            return ""

    def due_status(self, item):
        """Liefert 'overdue', 'today', 'soon', 'future' oder '' (kein Datum)."""
        iso_value = item.get("due")
        if not iso_value:
            return ""
        try:
            due_date = datetime.strptime(iso_value, "%Y-%m-%d").date()
        except ValueError:
            return ""
        if item.get("done"):
            return "future"
        delta = (due_date - datetime.now().date()).days
        if delta < 0:
            return "overdue"
        if delta == 0:
            return "today"
        if delta <= 2:
            return "soon"
        return "future"

    def normalize_items(self, data):
        if not isinstance(data, list):
            return []

        normalized = []
        for entry in data:
            if isinstance(entry, str):
                normalized.append(self.new_item(entry, False))
                continue

            if isinstance(entry, dict):
                text = str(entry.get("text", "")).strip()
                if not text:
                    continue
                children = self.normalize_items(entry.get("children", []))
                item_id = entry.get("id") if isinstance(entry.get("id"), str) and entry.get("id") else None
                importance = entry.get("importance", entry.get("priority", 0))
                due = entry.get("due")
                normalized.append(self.new_item(text, entry.get("done", False), children, item_id, importance, due))
        return normalized

    def load_items(self):
        if not os.path.exists(SAVE_FILE):
            self.folders = []
            self.lists = [self.new_list_object(self.app_title, [])]
            self.active_list_id = self.lists[0]["id"]
            self.items = self.lists[0]["items"]
            self.update_sidebar_list()
            self.refresh_tree()
            return
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            self.lists, active_id_from_file = self.normalize_lists_data(data)
            if not self.lists:
                self.lists = [self.new_list_object(self.app_title, [])]
            preferred_active_id = self.active_list_id or active_id_from_file
            if preferred_active_id not in [entry.get("id") for entry in self.lists]:
                preferred_active_id = active_id_from_file if active_id_from_file in [entry.get("id") for entry in self.lists] else self.lists[0]["id"]
            self.active_list_id = None
            self.set_active_list(preferred_active_id, refresh=False)
            self.update_sidebar_list()
            self.refresh_tree()
        except json.JSONDecodeError:
            messagebox.showerror("Fehler", "Die Speicherdatei ist beschädigt.")
            self.folders = []
            self.lists = [self.new_list_object(self.app_title, [])]
            self.active_list_id = self.lists[0]["id"]
            self.items = self.lists[0]["items"]
            self.update_sidebar_list()
            self.refresh_tree()
        except OSError as e:
            messagebox.showerror("Fehler", f"Die Speicherdatei konnte nicht gelesen werden:\n{e}")
            self.folders = []
            self.lists = [self.new_list_object(self.app_title, [])]
            self.active_list_id = self.lists[0]["id"]
            self.items = self.lists[0]["items"]
            self.update_sidebar_list()
            self.refresh_tree()

    def save_items(self):
        try:
            self.sync_current_list_reference()
            if os.path.exists(SAVE_FILE):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                backup_file = os.path.join(BACKUP_DIR, f"liste_backup_{timestamp}.json")
                shutil.copy2(SAVE_FILE, backup_file)
                self.prune_backups()

            payload = {
                "version": 3,
                "active_list_id": self.active_list_id,
                "folders": self.folders,
                "lists": self.lists,
            }
            temp_file = SAVE_FILE + ".tmp"
            with open(temp_file, "w", encoding="utf-8") as file:
                json.dump(payload, file, ensure_ascii=False, indent=4)
            os.replace(temp_file, SAVE_FILE)
            self.update_sidebar_list()
        except Exception as e:
            messagebox.showerror("Fehler beim Speichern", str(e))

    def prune_backups(self):
        """Begrenzt die automatischen Sicherungen auf MAX_BACKUPS, damit der Ordner nicht unbegrenzt wächst."""
        try:
            backups = [
                os.path.join(BACKUP_DIR, name)
                for name in os.listdir(BACKUP_DIR)
                if name.startswith("liste_backup_") and name.endswith(".json")
            ]
            if len(backups) <= self.MAX_BACKUPS:
                return
            backups.sort(key=lambda path: os.path.getmtime(path))
            for old_path in backups[: len(backups) - self.MAX_BACKUPS]:
                try:
                    os.remove(old_path)
                except OSError:
                    pass
        except OSError:
            pass

    def walk_items(self, items=None):
        if items is None:
            items = self.items
        for item in items:
            yield item
            yield from self.walk_items(item.get("children", []))

    def find_item(self, item_id, items=None, parent_list=None, parent_item=None):
        if items is None:
            items = self.items
            parent_list = self.items
            parent_item = None

        for index, item in enumerate(items):
            if item.get("id") == item_id:
                return item, items, index, parent_item
            found = self.find_item(item_id, item.get("children", []), item.get("children", []), item)
            if found:
                return found
        return None

    def item_contains_id(self, item, target_id):
        for child in item.get("children", []):
            if child.get("id") == target_id or self.item_contains_id(child, target_id):
                return True
        return False

    def remove_item_by_id(self, item_id):
        found = self.find_item(item_id)
        if not found:
            return None
        item, siblings, index, _parent_item = found
        return siblings.pop(index)

    def is_mouse_event(self, event):
        """True nur bei echten Maus-/Touchpad-Klicks, nicht bei Tastatur-Events."""
        try:
            return isinstance(getattr(event, "num", None), int) and getattr(event, "num", None) in (1, 2, 3)
        except Exception:
            return False

    def get_item_number_path(self, item_id, items=None, prefix=None):
        """Ermittelt die sichtunabhängige hierarchische Nummerierung eines Punkts."""
        if items is None:
            items = self.items
        if prefix is None:
            prefix = []
        for index, item in enumerate(items, start=1):
            current = prefix + [index]
            if item.get("id") == item_id:
                return current
            child_result = self.get_item_number_path(item_id, item.get("children", []), current)
            if child_result:
                return child_result
        return None

    # -----------------------------
    # Treeview Darstellung
    # -----------------------------
    def on_tree_scroll(self, first, last):
        """Blendet die Scrollbar nur dann ein, wenn der Listeninhalt wirklich scrollbar ist."""
        if not hasattr(self, "scrollbar"):
            return
        try:
            first_f = float(first)
            last_f = float(last)
        except (TypeError, ValueError):
            self.scrollbar.set(first, last)
            return

        self.scrollbar.set(first, last)
        needs_scrollbar = not (first_f <= 0.0 and last_f >= 1.0)

        if needs_scrollbar and not getattr(self, "scrollbar_visible", False):
            self.scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=14)
            self.scrollbar_visible = True
        elif not needs_scrollbar and getattr(self, "scrollbar_visible", False):
            self.scrollbar.pack_forget()
            self.scrollbar_visible = False

    def refresh_scrollbar_state(self):
        if hasattr(self, "tree"):
            self.tree.yview_moveto(self.tree.yview()[0])

    def remember_expanded_state(self):
        if not hasattr(self, "tree"):
            return
        expanded = set()
        for item in self.walk_items():
            item_id = item.get("id")
            try:
                if item_id and self.tree.exists(item_id) and self.tree.item(item_id, "open"):
                    expanded.add(item_id)
            except tk.TclError:
                pass
        self.expanded_ids = expanded

    # -----------------------------
    # Platzhalter / responsive Filterleiste
    # -----------------------------
    def set_entry_placeholder(self, event=None):
        if not hasattr(self, "entry"):
            return
        if not self.entry.get().strip():
            self.entry_placeholder_active = True
            self.entry.configure(fg=self.theme["placeholder"])
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.entry_placeholder_text)

    def clear_entry_placeholder(self, event=None):
        if not hasattr(self, "entry"):
            return
        if self.entry_placeholder_active:
            self.entry_placeholder_active = False
            self.entry.configure(fg=self.theme["text"])
            self.entry.delete(0, tk.END)

    def get_entry_text(self):
        if not hasattr(self, "entry"):
            return ""
        raw_text = self.entry.get().strip()
        if getattr(self, "entry_placeholder_active", False):
            if raw_text == self.entry_placeholder_text:
                return ""
            # Robuste Absicherung: Falls Text per Zwischenablage oder Skript eingefügt wurde,
            # während der Platzhalterstatus noch aktiv war, wird der echte Text trotzdem übernommen.
            self.entry_placeholder_active = False
            self.entry.configure(fg=self.theme["text"])
        return raw_text

    def set_search_placeholder(self, event=None):
        if not hasattr(self, "search_entry"):
            return
        if not self.search_var.get().strip():
            self.search_placeholder_active = True
            self.search_entry.configure(fg=self.theme["placeholder"])
            self.search_var.set(self.search_placeholder_text)

    def clear_search_placeholder(self, event=None):
        if not hasattr(self, "search_entry"):
            return
        if self.search_placeholder_active:
            self.search_placeholder_active = False
            self.search_entry.configure(fg=self.theme["text"])
            self.search_var.set("")

    def update_responsive_filter_visibility(self, event=None):
        """Blendet die beiden Filterboxen bei schmalen Fenstern aus, damit die Suche bedienbar bleibt."""
        if not all(hasattr(self, name) for name in ("hide_done_box_border", "done_only_box_border")):
            return
        width = event.width if event is not None else self.search_frame.winfo_width()
        should_show = width >= 880
        if should_show == getattr(self, "filters_visible", True):
            return
        self.filters_visible = should_show
        if should_show:
            self.hide_done_box_border.pack(side="left", fill="y", padx=(0, 10), before=self.search_border)
            self.done_only_box_border.pack(side="left", fill="y", padx=(0, 10), before=self.search_border)
        else:
            self.hide_done_box_border.pack_forget()
            self.done_only_box_border.pack_forget()

    def current_search_query(self):
        if not hasattr(self, "search_var"):
            return ""
        raw_text = self.search_var.get().strip()
        if getattr(self, "search_placeholder_active", False):
            if raw_text == self.search_placeholder_text:
                return ""
            # Robuste Absicherung: Falls Text per Zwischenablage oder Skript eingefügt wurde,
            # während der Platzhalterstatus noch aktiv war, wird der echte Text trotzdem als Suche genutzt.
            self.search_placeholder_active = False
            if hasattr(self, "search_entry"):
                self.search_entry.configure(fg=self.theme["text"])
        return raw_text.lower()

    def item_text_matches_query(self, item, query):
        if not query:
            return True
        haystack = " ".join([
            str(item.get("text", "")),
            self.IMPORTANCE_NAMES.get(self.clamp_importance(item.get("importance", 0)), ""),
            "erledigt" if item.get("done") else "offen",
            self.format_due_display(item.get("due")),
        ]).lower()
        return query in haystack

    def get_filter_mode(self):
        if getattr(self, "show_done_only_var", None) is not None and self.show_done_only_var.get():
            return "done"
        if getattr(self, "hide_done_var", None) is not None and self.hide_done_var.get():
            return "open"
        return "all"

    def item_matches_status_filter(self, item):
        mode = self.get_filter_mode()
        if mode == "open":
            return not item.get("done", False)
        if mode == "done":
            return bool(item.get("done", False))
        return True

    def item_visible_by_filter(self, item):
        query = self.current_search_query()
        self_matches = self.item_text_matches_query(item, query) and self.item_matches_status_filter(item)
        child_matches = any(self.item_visible_by_filter(child) for child in item.get("children", []))
        return self_matches or child_matches

    def has_active_filter(self):
        return bool(self.current_search_query()) or self.get_filter_mode() != "all"

    def on_open_only_changed(self):
        if self.hide_done_var.get():
            self.show_done_only_var.set(False)
        self.on_filter_changed()

    def on_done_only_changed(self):
        if self.show_done_only_var.get():
            self.hide_done_var.set(False)
        self.on_filter_changed()

    def on_filter_changed(self):
        self.save_settings()
        self.refresh_tree()

    def clear_search(self):
        self.search_placeholder_active = False
        self.search_var.set("")
        if hasattr(self, "search_entry"):
            self.search_entry.configure(fg=self.theme["text"])
            if self.root.focus_get() != self.search_entry:
                self.set_search_placeholder()

    def focus_search(self, event=None):
        if hasattr(self, "search_entry"):
            self.search_entry.focus_set()
            self.clear_search_placeholder()
            self.search_entry.select_range(0, tk.END)
        return "break"

    def focus_entry(self, event=None):
        if hasattr(self, "entry"):
            self.entry.focus_set()
            self.clear_entry_placeholder()
        return "break"

    def handle_escape(self, event=None):
        focus = self.root.focus_get()
        if focus == getattr(self, "search_entry", None) and self.search_var.get():
            self.clear_search()
        elif focus == getattr(self, "entry", None):
            if not getattr(self, "entry_placeholder_active", False):
                self.entry.delete(0, tk.END)
        else:
            self.clear_tree_selection()
        return "break"

    def compute_stats(self, items):
        total = 0
        done = 0
        overdue = 0
        for item in self.walk_items(items):
            total += 1
            if item.get("done"):
                done += 1
            elif self.due_status(item) == "overdue":
                overdue += 1
        return total, done, overdue

    def update_stats_label(self):
        if not hasattr(self, "stats_label"):
            return
        total, done, overdue = self.compute_stats(self.items)
        if total == 0:
            text = "Noch keine Aufgaben in dieser Liste."
        else:
            percent = round(done / total * 100)
            open_count = total - done
            text = f"{done} von {total} erledigt \u00b7 {percent}\u00a0%"
            if open_count:
                text += f" \u00b7 {open_count} offen"
            if overdue:
                text += f" \u00b7 {overdue} \u00fcberf\u00e4llig"
        try:
            self.stats_label.configure(text=text)
        except tk.TclError:
            pass

    def refresh_tree(self, selected_id=None):
        if not hasattr(self, "tree"):
            return

        self.update_stats_label()

        if selected_id is None:
            selected_id = self.get_selected_item_id()
        self.remember_expanded_state()

        for row_id in self.tree.get_children(""):
            self.tree.delete(row_id)

        if not self.items:
            self.tree.insert("", "end", iid=self.EMPTY_ROW_ID, text="Noch keine Punkte vorhanden.", tags=("empty",))
            self.schedule_scrollbar_refresh()
            return

        inserted = self.insert_tree_items("", self.items, [])
        if inserted == 0:
            self.tree.insert("", "end", iid=self.EMPTY_ROW_ID, text="Keine Treffer für den aktuellen Filter.", tags=("empty",))
            self.schedule_scrollbar_refresh()
            return

        if selected_id and self.tree.exists(selected_id):
            self.tree.selection_set(selected_id)
            self.tree.focus(selected_id)
            self.tree.see(selected_id)

        self.schedule_scrollbar_refresh()

    def insert_tree_items(self, parent_id, items, number_prefix):
        inserted_count = 0
        visible_index = 0
        query = self.current_search_query()

        for original_index, item in enumerate(items, start=1):
            if not self.item_visible_by_filter(item):
                continue

            visible_index += 1
            # Ohne Filter bleibt die ursprüngliche Nummerierung erhalten. Mit Filter wird die sichtbare Ansicht sauber durchnummeriert.
            display_index = visible_index if self.has_active_filter() else original_index
            current_number = number_prefix + [display_index]
            number_text = ".".join(str(part) for part in current_number)
            importance = self.clamp_importance(item.get("importance", 0))
            item["importance"] = importance
            flag_prefix = self.IMPORTANCE_MARKERS.get(importance, "")
            done_prefix = "✓ " if item.get("done") else ""
            due_state = self.due_status(item)
            due_text = self.format_due_display(item.get("due"))
            due_suffix = f"   \U0001F4C5 {due_text}" if due_text else ""
            row_text = f"{number_text}. {flag_prefix}{done_prefix}{item.get('text', '')}{due_suffix}"
            item_id = item.get("id") or uuid.uuid4().hex
            item["id"] = item_id
            has_children = bool(item.get("children"))
            should_open = item_id in self.expanded_ids or parent_id == "" or bool(query)
            if item.get("done"):
                tag = "done"
            elif due_state == "overdue":
                tag = "overdue"
            elif due_state == "today":
                tag = "due_today"
            elif importance == 3:
                tag = "priority_high"
            elif importance == 2:
                tag = "priority_medium"
            elif importance == 1:
                tag = "priority_low"
            else:
                tag = "open"
            self.tree.insert(
                parent_id,
                "end",
                iid=item_id,
                text=row_text,
                open=should_open,
                tags=(tag,),
            )
            inserted_count += 1
            if has_children:
                inserted_count += self.insert_tree_items(item_id, item.get("children", []), current_number)
        return inserted_count

    def get_selected_item_ids(self):
        if not hasattr(self, "tree"):
            return []
        selected = []
        for item_id in self.tree.selection():
            if item_id and item_id != self.EMPTY_ROW_ID and self.find_item(item_id):
                selected.append(item_id)
        return selected

    def get_selected_item_id(self):
        if not hasattr(self, "tree"):
            return None
        focus_id = self.tree.focus()
        if focus_id and focus_id != self.EMPTY_ROW_ID and focus_id in self.tree.selection() and self.find_item(focus_id):
            return focus_id
        selected = self.get_selected_item_ids()
        return selected[0] if selected else None

    def iter_tree_ids(self, parent_id=""):
        if not hasattr(self, "tree"):
            return []
        result = []
        for child_id in self.tree.get_children(parent_id):
            if child_id != self.EMPTY_ROW_ID:
                result.append(child_id)
                result.extend(self.iter_tree_ids(child_id))
        return result

    def select_all_items(self, event=None):
        if self.root.focus_get() in (getattr(self, "entry", None), getattr(self, "search_entry", None)):
            try:
                self.root.focus_get().selection_range(0, tk.END)
            except tk.TclError:
                pass
            return "break"
        ids = self.iter_tree_ids()
        if ids:
            self.tree.selection_set(ids)
            self.tree.focus(ids[0])
            self.selection_anchor_id = ids[0]
        return "break"

    def select_range_from_click(self, event=None):
        if event is None or not hasattr(self, "tree"):
            return "break"
        target_id = self.tree.identify_row(event.y)
        if not target_id or target_id == self.EMPTY_ROW_ID:
            return "break"
        ids = self.iter_tree_ids()
        if target_id not in ids:
            return "break"
        anchor_id = self.selection_anchor_id or self.get_selected_item_id() or target_id
        if anchor_id not in ids:
            anchor_id = target_id
        start = ids.index(anchor_id)
        end = ids.index(target_id)
        if start > end:
            start, end = end, start
        selected_range = ids[start:end + 1]
        self.tree.selection_set(selected_range)
        self.tree.focus(target_id)
        return "break"

    def filter_top_level_selection(self, item_ids):
        selected_set = set(item_ids)
        top_level_ids = []
        for item_id in item_ids:
            found = self.find_item(item_id)
            if not found:
                continue
            parent_item = found[3]
            is_descendant = False
            while parent_item:
                parent_id = parent_item.get("id")
                if parent_id in selected_set:
                    is_descendant = True
                    break
                parent_found = self.find_item(parent_id)
                parent_item = parent_found[3] if parent_found else None
            if not is_descendant:
                top_level_ids.append(item_id)
        return top_level_ids

    def clear_tree_selection(self):
        if hasattr(self, "tree"):
            self.tree.selection_remove(self.tree.selection())
            self.selection_anchor_id = None

    # -----------------------------
    # Undo / Komfortaktionen
    # -----------------------------
    def snapshot_undo(self):
        self.undo_stack.append(copy.deepcopy(self.items))
        if len(self.undo_stack) > 20:
            self.undo_stack.pop(0)

    def undo_last_change(self, event=None):
        if not self.undo_stack:
            messagebox.showinfo("Rückgängig", "Es gibt keine Änderung zum Rückgängigmachen.")
            return "break"
        self.items = self.undo_stack.pop()
        self.current_list()["items"] = self.items
        self.save_items()
        self.refresh_tree()
        return "break"

    def format_item_lines(self, item, number_prefix, level=0):
        number_text = ".".join(str(part) for part in number_prefix)
        indent = "   " * level
        flag_prefix = self.IMPORTANCE_MARKERS.get(self.clamp_importance(item.get("importance", 0)), "")
        done_prefix = "✓ " if item.get("done") else ""
        lines = [f"{indent}{number_text}. {flag_prefix}{done_prefix}{item.get('text', '')}"]
        for index, child in enumerate(item.get("children", []), start=1):
            lines.extend(self.format_item_lines(child, number_prefix + [index], level + 1))
        return lines

    def copy_selected_to_clipboard(self, event=None):
        if self.root.focus_get() in (getattr(self, "entry", None), getattr(self, "search_entry", None)):
            return None
        selected_ids = self.get_selected_item_ids()
        if not selected_ids:
            messagebox.showwarning("Hinweis", "Zuerst einen Punkt auswählen.")
            return "break"

        selected_ids = self.filter_top_level_selection(selected_ids)
        blocks = []
        for item_id in selected_ids:
            found = self.find_item(item_id)
            if not found:
                continue
            item, _siblings, _index, _parent_item = found
            number_path = self.get_item_number_path(item_id) or [1]
            blocks.extend(self.format_item_lines(item, number_path))
        if not blocks:
            return "break"
        text = "\n".join(blocks)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        return "break"

    def paste_items_from_clipboard(self, event=None):
        """Fügt Aufgaben aus der Zwischenablage als neue Punkte ein.

        Unterstützt den eigenen Kopier-/TXT-Export-Stil mit Nummerierung sowie
        einfache mehrzeilige Texte. Ist ein Listenpunkt ausgewählt, werden die
        eingefügten Punkte direkt danach als gleichrangige Punkte eingefügt;
        ohne Auswahl werden sie am Ende der Hauptliste ergänzt.
        """
        if self.root.focus_get() in (getattr(self, "entry", None), getattr(self, "search_entry", None)):
            # In Textfeldern soll Strg+V die normale System-Einfügefunktion behalten.
            return None

        try:
            clipboard_text = self.root.clipboard_get()
        except tk.TclError:
            messagebox.showwarning("Einfügen", "Die Zwischenablage enthält keinen Text.")
            return "break"

        clipboard_text = clipboard_text.strip()
        if not clipboard_text:
            messagebox.showwarning("Einfügen", "Die Zwischenablage enthält keinen Text.")
            return "break"

        pasted_items = self.parse_clipboard_items(clipboard_text)
        if not pasted_items:
            messagebox.showwarning("Einfügen", "Aus dem Inhalt der Zwischenablage konnten keine Punkte erstellt werden.")
            return "break"

        selected_id = self.get_selected_item_id()
        self.snapshot_undo()
        target_list = self.items
        insert_index = len(target_list)

        if selected_id:
            found = self.find_item(selected_id)
            if found:
                _selected_item, siblings, index, _parent_item = found
                target_list = siblings
                insert_index = index + 1

        for offset, item in enumerate(pasted_items):
            target_list.insert(insert_index + offset, item)

        self.save_items()
        self.refresh_tree(selected_id=pasted_items[-1].get("id"))
        return "break"

    def parse_clipboard_items(self, clipboard_text):
        lines = [line.rstrip() for line in clipboard_text.splitlines() if line.strip()]
        if not lines:
            return []

        # Bei einem vollständigen TXT-Export steht häufig zuerst ein Titel und
        # danach eine Linie aus Gleichheitszeichen. Diese Kopfzeile gehört nicht
        # als Aufgabe in die Liste.
        if len(lines) >= 2 and set(lines[1].strip()) == {"="}:
            lines = lines[2:]

        # Zuerst den vorhandenen TXT-Parser nutzen, aber nur wenn tatsächlich
        # nummerierte Listenzeilen enthalten sind. Unnummerierte Clipboard-Texte
        # werden im Fallback sauber als Bullet-/Checkbox-Zeilen interpretiert.
        numbered_line_pattern = re.compile(r"^\d+(?:\.\d+)*\.\s+")
        if any(numbered_line_pattern.match(line.strip()) for line in lines):
            parsed = self.parse_txt_items(lines)
            if parsed:
                return parsed

        # Fallback: Jede nicht leere Zeile wird als eigener Hauptpunkt eingefügt.
        plain_items = []
        bullet_pattern = re.compile(r"^[-*•–—]\s+")
        checkbox_pattern = re.compile(r"^\[\s*([xX])?\s*\]\s+")

        for raw_line in lines:
            text = raw_line.strip()
            done = False
            importance = 0

            checkbox_match = checkbox_pattern.match(text)
            if checkbox_match:
                done = bool(checkbox_match.group(1) and checkbox_match.group(1).lower() == "x")
                text = checkbox_pattern.sub("", text, count=1).strip()

            text = bullet_pattern.sub("", text, count=1).strip()

            for marker, marker_importance in (("🚩 ", 3), ("⚑ ", 2), ("⚐ ", 1)):
                if text.startswith(marker):
                    importance = marker_importance
                    text = text[len(marker):].strip()
                    break

            if text.startswith("✓ ") or text.startswith("✅ "):
                done = True
                text = text[2:].strip()

            if text:
                plain_items.append(self.new_item(text, done=done, importance=importance))

        return plain_items

    def expand_all(self, event=None):
        self.set_tree_open_state(True)
        return "break"

    def collapse_all(self, event=None):
        self.set_tree_open_state(False)
        return "break"

    def set_tree_open_state(self, is_open):
        def apply(row_id):
            try:
                self.tree.item(row_id, open=is_open)
                for child_id in self.tree.get_children(row_id):
                    apply(child_id)
            except tk.TclError:
                pass
        for row_id in self.tree.get_children(""):
            apply(row_id)
        self.remember_expanded_state()

    # -----------------------------
    # Listenaktionen
    # -----------------------------
    def on_entry_return(self, event=None):
        self.add_item()
        return "break"

    def add_item(self):
        text = self.get_entry_text()
        if not text:
            messagebox.showwarning("Hinweis", "Bitte einen Punkt eingeben.")
            return
        self.snapshot_undo()
        self.items.append(self.new_item(text, False))
        self.entry.delete(0, tk.END)
        self.entry_placeholder_active = False
        self.entry.configure(fg=self.theme["text"])
        self.save_items()
        self.refresh_tree(selected_id=self.items[-1]["id"])

    def delete_item(self, event=None):
        # Bei Tastatur-Events soll Entf in Eingabe-/Suchfeldern normal Text löschen.
        # Per Button darf Löschen unabhängig vom aktuellen Textfeld-Fokus funktionieren.
        if event is not None and self.root.focus_get() in (self.entry, getattr(self, "search_entry", None)):
            return "break"

        selected_ids = self.get_selected_item_ids()
        if not selected_ids:
            messagebox.showwarning("Hinweis", "Zuerst einen Punkt auswählen.")
            return

        # Tiefere Unterpunkte zuerst löschen, damit Mehrfachauswahl aus Haupt- und Unterpunkten stabil bleibt.
        selected_ids = sorted(selected_ids, key=lambda item_id: len(self.get_item_number_path(item_id) or []), reverse=True)
        self.snapshot_undo()
        removed_any = False
        for item_id in selected_ids:
            if self.remove_item_by_id(item_id):
                removed_any = True
        if not removed_any:
            if self.undo_stack:
                self.undo_stack.pop()
            return
        self.save_items()
        self.refresh_tree()

    def clear_list(self):
        if messagebox.askyesno("Löschen", "Alle Punkte wirklich löschen?"):
            self.snapshot_undo()
            self.items.clear()
            self.save_items()
            self.refresh_tree()

    def edit_item(self):
        item_id = self.get_selected_item_id()
        if not item_id:
            return
        found = self.find_item(item_id)
        if not found:
            return
        item, _siblings, _index, _parent_item = found
        new_text = self.themed_input_dialog(
            "Punkt bearbeiten",
            "Text des Punktes:",
            initial=item["text"],
            ok_text="Speichern",
        )
        if new_text is None:
            return

        new_text = new_text.strip()
        if not new_text:
            messagebox.showwarning("Hinweis", "Bitte einen Text eingeben.")
            return

        if new_text != item.get("text", ""):
            self.snapshot_undo()
            item["text"] = new_text
            self.save_items()
            self.refresh_tree(selected_id=item_id)

    def is_tree_indicator_click(self, event, item_id):
        """Erkennt Klicks auf den Ein-/Ausklapp-Pfeil, damit diese nicht als Erledigt-Klick zählen."""
        if event is None or not item_id or item_id == self.EMPTY_ROW_ID:
            return False

        try:
            element = self.tree.identify_element(event.x, event.y)
            if element and "indicator" in element.lower():
                return True
        except tk.TclError:
            pass

        # Fallback für Tk-/Windows-Varianten, die den Indicator nicht eindeutig melden.
        try:
            if self.tree.get_children(item_id):
                bbox = self.tree.bbox(item_id, "#0")
                if bbox:
                    x, _y, _w, _h = bbox
                    return event.x <= x + 22
        except tk.TclError:
            pass

        return False

    def toggle_done(self, event=None):
        item_ids = []
        if event is not None and self.is_mouse_event(event):
            item_id = self.tree.identify_row(event.y)
            if self.is_tree_indicator_click(event, item_id):
                return "break"
            if item_id and item_id != self.EMPTY_ROW_ID:
                self.tree.selection_set(item_id)
                self.tree.focus(item_id)
                self.selection_anchor_id = item_id
                item_ids = [item_id]

        if not item_ids:
            item_ids = self.get_selected_item_ids()
        if not item_ids:
            return "break"

        first_found = self.find_item(item_ids[0])
        if not first_found:
            return "break"
        new_state = not first_found[0].get("done", False)

        self.snapshot_undo()
        changed = False
        for item_id in item_ids:
            found = self.find_item(item_id)
            if not found:
                continue
            item, _siblings, _index, _parent_item = found
            if item.get("done", False) != new_state:
                item["done"] = new_state
                changed = True
        if not changed and self.undo_stack:
            self.undo_stack.pop()
        else:
            self.save_items()
            self.refresh_tree(selected_id=item_ids[-1])
            for selected_id in item_ids:
                if self.tree.exists(selected_id):
                    self.tree.selection_add(selected_id)
        return "break"

    # -----------------------------
    # Wichtigkeit / Flaggen
    # -----------------------------
    def cycle_importance_selected(self, event=None):
        item_ids = self.get_selected_item_ids()
        if not item_ids:
            messagebox.showwarning("Hinweis", "Zuerst einen Punkt auswählen.")
            return "break"

        self.snapshot_undo()
        changed = False
        for item_id in item_ids:
            found = self.find_item(item_id)
            if not found:
                continue
            item, _siblings, _index, _parent_item = found
            item["importance"] = (self.clamp_importance(item.get("importance", 0)) + 1) % 4
            changed = True
        if not changed:
            if self.undo_stack:
                self.undo_stack.pop()
            return "break"
        self.save_items()
        self.refresh_tree(selected_id=item_ids[-1])
        for selected_id in item_ids:
            if self.tree.exists(selected_id):
                self.tree.selection_add(selected_id)
        return "break"

    def cycle_importance_from_click(self, event=None):
        if event is not None:
            item_id = self.tree.identify_row(event.y)
            if not item_id or item_id == self.EMPTY_ROW_ID:
                return "break"
            self.tree.selection_set(item_id)
            self.tree.focus(item_id)
            self.selection_anchor_id = item_id
        return self.cycle_importance_selected(event)

    # -----------------------------
    # Fälligkeitsdatum
    # -----------------------------
    def set_due_date_selected(self, event=None):
        """Setzt oder entfernt das Fälligkeitsdatum der ausgewählten Punkte."""
        if event is not None and self.root.focus_get() in (
            getattr(self, "entry", None),
            getattr(self, "search_entry", None),
        ):
            return None

        item_ids = self.get_selected_item_ids()
        if not item_ids:
            messagebox.showwarning("Hinweis", "Zuerst einen Punkt auswählen.")
            return "break"

        first_found = self.find_item(item_ids[0])
        current_iso = first_found[0].get("due") if first_found else None
        answer = self.themed_date_picker(current_iso)
        if answer is None:
            return "break"  # Abbruch

        new_due = answer or None  # "" entfernt die Fälligkeit
        self.snapshot_undo()
        changed = False
        for item_id in item_ids:
            found = self.find_item(item_id)
            if not found:
                continue
            item = found[0]
            if item.get("due") != new_due:
                item["due"] = new_due
                changed = True

        if not changed:
            if self.undo_stack:
                self.undo_stack.pop()
            return "break"

        self.save_items()
        self.refresh_tree(selected_id=item_ids[-1])
        for selected_id in item_ids:
            if self.tree.exists(selected_id):
                self.tree.selection_add(selected_id)
        return "break"

    # -----------------------------
    # Hierarchie / Einrücken / Ausrücken
    # -----------------------------
    def make_subitem(self, source_id, target_id):
        if not source_id or not target_id or source_id == target_id:
            return False
        if target_id == self.EMPTY_ROW_ID:
            return False

        source_found = self.find_item(source_id)
        target_found = self.find_item(target_id)
        if not source_found or not target_found:
            return False

        source_item, _source_siblings, _source_index, _source_parent = source_found
        target_item, _target_siblings, _target_index, _target_parent = target_found

        if self.item_contains_id(source_item, target_id):
            messagebox.showwarning("Nicht möglich", "Ein Punkt kann nicht unter einen eigenen Unterpunkt verschoben werden.")
            return False

        moved_item = self.remove_item_by_id(source_id)
        if not moved_item:
            return False

        # Ziel nach dem Entfernen erneut suchen, weil sich die Struktur geändert haben kann.
        target_found_after_remove = self.find_item(target_id)
        if not target_found_after_remove:
            # Fallback: rückgängig möglichst sicher an oberster Ebene anhängen.
            self.items.append(moved_item)
            return False

        target_item = target_found_after_remove[0]
        target_item.setdefault("children", []).append(moved_item)
        self.expanded_ids.add(target_id)
        return True

    def move_item_relative_to_target(self, source_id, target_id, place="after"):
        if not source_id or not target_id or source_id == target_id:
            return False
        if target_id == self.EMPTY_ROW_ID:
            return False

        source_found = self.find_item(source_id)
        target_found = self.find_item(target_id)
        if not source_found or not target_found:
            return False

        source_item = source_found[0]
        if self.item_contains_id(source_item, target_id):
            messagebox.showwarning("Nicht möglich", "Ein Punkt kann nicht in den eigenen Unterbereich verschoben werden.")
            return False

        moved_item = self.remove_item_by_id(source_id)
        if not moved_item:
            return False

        target_found_after_remove = self.find_item(target_id)
        if not target_found_after_remove:
            self.items.append(moved_item)
            return False

        _target_item, target_siblings, target_index, _target_parent = target_found_after_remove
        insert_index = target_index if place == "before" else target_index + 1
        target_siblings.insert(insert_index, moved_item)
        return True

    def toggle_indent_selected(self, event=None):
        """Tab schaltet einen Punkt zwischen Hauptpunkt und Unterpunkt um."""
        source_id = self.get_selected_item_id()
        if not source_id:
            return "break"

        found = self.find_item(source_id)
        if not found:
            return "break"

        _source_item, _source_siblings, _source_index, parent_item = found

        if parent_item:
            self.snapshot_undo()
            moved_item = self.remove_item_by_id(source_id)
            if not moved_item:
                if self.undo_stack:
                    self.undo_stack.pop()
                return "break"

            parent_found_after_remove = self.find_item(parent_item.get("id"))
            if not parent_found_after_remove:
                self.items.append(moved_item)
                if self.undo_stack:
                    self.undo_stack.pop()
                return "break"

            _parent_item, parent_siblings, parent_index, _grand_parent = parent_found_after_remove
            parent_siblings.insert(parent_index + 1, moved_item)
            self.save_items()
            self.refresh_tree(selected_id=source_id)
            return "break"

        previous_sibling_id = self.tree.prev(source_id)
        if previous_sibling_id:
            self.snapshot_undo()
            if self.make_subitem(source_id, previous_sibling_id):
                self.save_items()
                self.refresh_tree(selected_id=source_id)
            elif self.undo_stack:
                self.undo_stack.pop()
        return "break"

    def indent_selected(self, event=None):
        source_id = self.get_selected_item_id()
        if not source_id:
            return "break"

        previous_sibling_id = self.tree.prev(source_id)
        if not previous_sibling_id:
            messagebox.showinfo("Hinweis", "Der Punkt kann nur unter den vorherigen Punkt eingerückt werden.")
            return "break"

        self.snapshot_undo()
        if self.make_subitem(source_id, previous_sibling_id):
            self.save_items()
            self.refresh_tree(selected_id=source_id)
        else:
            self.undo_stack.pop()
        return "break"

    def outdent_selected(self, event=None):
        source_id = self.get_selected_item_id()
        if not source_id:
            return "break"

        found = self.find_item(source_id)
        if not found:
            return "break"
        _source_item, _source_siblings, _source_index, parent_item = found
        if not parent_item:
            messagebox.showinfo("Hinweis", "Der Punkt ist bereits ein Hauptpunkt.")
            return "break"

        self.snapshot_undo()
        parent_id = parent_item.get("id")
        moved_item = self.remove_item_by_id(source_id)
        if not moved_item:
            return "break"

        parent_found_after_remove = self.find_item(parent_id)
        if not parent_found_after_remove:
            self.items.append(moved_item)
            return "break"

        _parent_item, parent_siblings, parent_index, _grand_parent = parent_found_after_remove
        parent_siblings.insert(parent_index + 1, moved_item)
        self.save_items()
        self.refresh_tree(selected_id=source_id)
        return "break"

    # -----------------------------
    # Drag & Drop
    # -----------------------------
    def on_drag_start(self, event):
        row_id = self.tree.identify_row(event.y)
        self.drag_start_id = None if row_id == self.EMPTY_ROW_ID else row_id
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.drag_has_moved = False
        if self.drag_start_id:
            shift_pressed = bool(event.state & 0x0001)
            ctrl_pressed = bool(event.state & 0x0004)
            # Shift + Klick soll den bestehenden Anker für die Bereichsauswahl behalten.
            # Shift + Drag nutzt dieselben Startdaten und erstellt beim Loslassen einen Unterpunkt.
            if not shift_pressed:
                if ctrl_pressed:
                    current_selection = set(self.tree.selection())
                    if self.drag_start_id in current_selection:
                        self.tree.selection_remove(self.drag_start_id)
                    else:
                        self.tree.selection_add(self.drag_start_id)
                    self.tree.focus(self.drag_start_id)
                    self.selection_anchor_id = self.drag_start_id
                else:
                    self.tree.selection_set(self.drag_start_id)
                    self.tree.focus(self.drag_start_id)
                    self.selection_anchor_id = self.drag_start_id
        return "break"

    def on_drag_motion(self, event):
        if not self.drag_start_id:
            return
        if abs(event.x - self.drag_start_x) + abs(event.y - self.drag_start_y) > 6:
            self.drag_has_moved = True

        target_id = self.tree.identify_row(event.y)
        self.clear_drop_target_tags()
        if target_id and target_id not in (self.EMPTY_ROW_ID, self.drag_start_id):
            try:
                current_tags = set(self.tree.item(target_id, "tags"))
                current_tags.add("drop_target")
                self.tree.item(target_id, tags=tuple(current_tags))
            except tk.TclError:
                pass

    def on_drag_end(self, event):
        source_id = self.drag_start_id
        target_id = self.tree.identify_row(event.y)
        shift_pressed = bool(event.state & 0x0001)

        self.clear_drop_target_tags()
        self.drag_start_id = None

        if not source_id or not target_id or target_id == self.EMPTY_ROW_ID:
            return

        if not self.drag_has_moved:
            if shift_pressed:
                self.select_range_from_click(event)
            return

        if target_id == source_id:
            return

        changed = False
        self.snapshot_undo()
        if shift_pressed:
            # Shift + Drag: Quelle wird Unterpunkt des Zielpunkts.
            changed = self.make_subitem(source_id, target_id)
        else:
            # Normales Drag & Drop: nur Reihenfolge ändern. Ober-/Unterhälfte entscheidet vor/nach Zielpunkt.
            place = "after"
            try:
                bbox = self.tree.bbox(target_id)
                if bbox:
                    _x, y, _w, h = bbox
                    place = "before" if event.y < y + h / 2 else "after"
            except tk.TclError:
                pass
            changed = self.move_item_relative_to_target(source_id, target_id, place=place)

        if changed:
            self.save_items()
            self.refresh_tree(selected_id=source_id)
        else:
            if self.undo_stack:
                self.undo_stack.pop()

    def clear_drop_target_tags(self):
        if not hasattr(self, "tree"):
            return
        for item_id in self.tree.get_children(""):
            self.clear_drop_target_tags_recursive(item_id)

    def clear_drop_target_tags_recursive(self, item_id):
        try:
            tags = tuple(tag for tag in self.tree.item(item_id, "tags") if tag != "drop_target")
            self.tree.item(item_id, tags=tags)
            for child_id in self.tree.get_children(item_id):
                self.clear_drop_target_tags_recursive(child_id)
        except tk.TclError:
            pass

    # -----------------------------
    # Export / Import
    # -----------------------------
    def import_txt_as_new_lists(self, event=None):
        paths = filedialog.askopenfilenames(
            title="Eine oder mehrere TXT-Dateien als neue Listen importieren",
            filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")],
        )
        if not paths:
            return "break"
        self.sync_current_list_reference()
        created = []
        for path in paths:
            try:
                with open(path, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                imported = self.parse_txt_items(lines)
                if not imported:
                    continue
                title = self.extract_txt_list_title(lines, path)
                created.append(self.new_list_object(title, imported))
            except Exception as e:
                messagebox.showerror("Fehler beim Listenimport", f"{os.path.basename(path)} konnte nicht importiert werden:\n{e}")
                return "break"
        if not created:
            messagebox.showwarning("Import", "In den ausgewählten Dateien wurden keine Listenpunkte gefunden.")
            return "break"
        self.lists.extend(created)
        self.set_active_list(created[-1]["id"])
        self.save_items()
        messagebox.showinfo("Import erfolgreich", f"{len(created)} Liste(n) importiert.")
        return "break"

    def extract_txt_list_title(self, lines, path):
        for raw_line in lines:
            line = raw_line.strip()
            if not line or line.startswith("===") or line.startswith("Exportiert am:"):
                continue
            if re.match(r"^\d+(?:\.\d+)*\.\s+", line):
                break
            return line[:80]
        base = os.path.splitext(os.path.basename(path))[0]
        base = base.replace("_", " ").replace("-", " ").strip()
        return base.title() or "Importierte Liste"

    def export_as_txt(self):
        if not self.items:
            messagebox.showwarning("Hinweis", "Keine Punkte zum Exportieren.")
            return
        default_filename = f"{self.safe_filename(self.app_title)}_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.txt"
        path = filedialog.asksaveasfilename(
            title="Liste als TXT speichern",
            defaultextension=".txt",
            initialfile=default_filename,
            filetypes=[("Textdatei", "*.txt"), ("Alle Dateien", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(f"{self.app_title}\n")
                file.write("=" * 30 + "\n\n")
                self.write_items_to_txt(file, self.items, [])
                file.write(f"\nExportiert am: {datetime.now().strftime('%d.%m.%Y um %H:%M Uhr')}\n")
            messagebox.showinfo("Export erfolgreich", f"Liste exportiert nach:\n{path}")
        except Exception as e:
            messagebox.showerror("Fehler beim Export", str(e))

    def write_items_to_txt(self, file, items, number_prefix):
        for index, item in enumerate(items, start=1):
            current_number = number_prefix + [index]
            number_text = ".".join(str(part) for part in current_number)
            indent = "   " * (len(current_number) - 1)
            flag_prefix = self.IMPORTANCE_MARKERS.get(self.clamp_importance(item.get("importance", 0)), "")
            done_prefix = "✓ " if item.get("done") else ""
            file.write(f"{indent}{number_text}. {flag_prefix}{done_prefix}{item.get('text', '')}\n")
            self.write_items_to_txt(file, item.get("children", []), current_number)

    def export_as_markdown(self):
        if not self.items:
            messagebox.showwarning("Hinweis", "Keine Punkte zum Exportieren.")
            return
        default_filename = f"{self.safe_filename(self.app_title)}_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.md"
        path = filedialog.asksaveasfilename(
            title="Liste als Markdown speichern",
            defaultextension=".md",
            initialfile=default_filename,
            filetypes=[("Markdown", "*.md"), ("Alle Dateien", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(f"# {self.app_title}\n\n")
                self.write_items_to_markdown(file, self.items, 0)
                file.write(f"\n_Exportiert am {datetime.now().strftime('%d.%m.%Y um %H:%M Uhr')}_\n")
            messagebox.showinfo("Export erfolgreich", f"Liste exportiert nach:\n{path}")
        except Exception as e:
            messagebox.showerror("Fehler beim Export", str(e))

    def write_items_to_markdown(self, file, items, level):
        indent = "  " * level
        for item in items:
            checkbox = "[x]" if item.get("done") else "[ ]"
            flag = self.IMPORTANCE_MARKERS.get(self.clamp_importance(item.get("importance", 0)), "")
            due_text = self.format_due_display(item.get("due"))
            due_suffix = f" (f\u00e4llig {due_text})" if due_text else ""
            file.write(f"{indent}- {checkbox} {flag}{item.get('text', '')}{due_suffix}\n")
            self.write_items_to_markdown(file, item.get("children", []), level + 1)

    def export_as_csv(self):
        if not self.items:
            messagebox.showwarning("Hinweis", "Keine Punkte zum Exportieren.")
            return
        default_filename = f"{self.safe_filename(self.app_title)}_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv"
        path = filedialog.asksaveasfilename(
            title="Liste als CSV speichern",
            defaultextension=".csv",
            initialfile=default_filename,
            filetypes=[("CSV", "*.csv"), ("Alle Dateien", "*.*")],
        )
        if not path:
            return
        try:
            # utf-8-sig + Semikolon, damit Excel (DE) die Datei direkt korrekt öffnet.
            with open(path, "w", encoding="utf-8-sig", newline="") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(["Nummer", "Ebene", "Aufgabe", "Erledigt", "Wichtigkeit", "Fällig"])
                self.write_items_to_csv(writer, self.items, [])
            messagebox.showinfo("Export erfolgreich", f"Liste exportiert nach:\n{path}")
        except Exception as e:
            messagebox.showerror("Fehler beim Export", str(e))

    def write_items_to_csv(self, writer, items, number_prefix):
        for index, item in enumerate(items, start=1):
            current_number = number_prefix + [index]
            number_text = ".".join(str(part) for part in current_number)
            writer.writerow([
                number_text,
                len(current_number),
                item.get("text", ""),
                "ja" if item.get("done") else "nein",
                self.IMPORTANCE_NAMES.get(self.clamp_importance(item.get("importance", 0)), "keine"),
                self.format_due_display(item.get("due")),
            ])
            self.write_items_to_csv(writer, item.get("children", []), current_number)

    def export_full_backup(self):
        """Sichert alle Listen, Ordner und das Datenmodell in einer einzelnen JSON-Datei."""
        self.sync_current_list_reference()
        default_filename = f"glide_backup_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.json"
        path = filedialog.asksaveasfilename(
            title="Komplettbackup speichern (alle Listen)",
            defaultextension=".json",
            initialfile=default_filename,
            filetypes=[("Glide-Backup", "*.json"), ("Alle Dateien", "*.*")],
        )
        if not path:
            return
        try:
            payload = {
                "app": APP_NAME,
                "app_version": APP_VERSION,
                "version": 3,
                "exported_at": datetime.now().isoformat(timespec="seconds"),
                "active_list_id": self.active_list_id,
                "folders": self.folders,
                "lists": self.lists,
            }
            with open(path, "w", encoding="utf-8") as file:
                json.dump(payload, file, ensure_ascii=False, indent=4)
            messagebox.showinfo("Backup erstellt", f"Komplettbackup gespeichert nach:\n{path}")
        except Exception as e:
            messagebox.showerror("Fehler beim Backup", str(e))

    def import_full_backup(self):
        """Lädt ein Komplettbackup und ersetzt alle aktuellen Listen (vorher wird automatisch gesichert)."""
        path = filedialog.askopenfilename(
            title="Komplettbackup laden (ersetzt alle Listen)",
            filetypes=[("Glide-Backup", "*.json"), ("JSON-Dateien", "*.json"), ("Alle Dateien", "*.*")],
        )
        if not path:
            return
        if not messagebox.askyesno(
            "Backup importieren",
            "Beim Import werden alle aktuell vorhandenen Listen ersetzt.\n\n"
            "Vom aktuellen Stand wird automatisch ein Sicherungsbackup angelegt.\n\nFortfahren?",
        ):
            return
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
            new_lists, active_from_file = self.normalize_lists_data(data)
            if not new_lists:
                messagebox.showwarning("Import", "In der Datei wurden keine Listen gefunden.")
                return
            self.lists = new_lists
            existing_ids = [entry.get("id") for entry in self.lists]
            preferred = active_from_file if active_from_file in existing_ids else self.lists[0]["id"]
            self.active_list_id = None
            self.set_active_list(preferred, refresh=False)
            self.save_items()
            self.update_sidebar_list()
            self.refresh_tree()
            messagebox.showinfo("Import erfolgreich", f"{len(self.lists)} Liste(n) importiert.")
        except json.JSONDecodeError:
            messagebox.showerror("Fehler", "Die Datei ist kein gültiges Glide-Backup.")
        except Exception as e:
            messagebox.showerror("Fehler beim Import", str(e))

    def sort_current_list(self, key="due"):
        """Sortiert die aktive Liste rekursiv nach Fälligkeit, Wichtigkeit oder Alphabet."""
        if not self.items:
            return
        self.snapshot_undo()
        self._sort_items_recursive(self.items, key)
        self.save_items()
        self.refresh_tree()

    def _sort_items_recursive(self, items, key):
        if key == "due":
            def sort_key(it):
                iso = it.get("due")
                try:
                    parsed_date = datetime.strptime(iso, "%Y-%m-%d").date() if iso else None
                except ValueError:
                    parsed_date = None
                return (
                    1 if it.get("done") else 0,
                    parsed_date is None,
                    parsed_date or datetime.max.date(),
                )
            items.sort(key=sort_key)
        elif key == "importance":
            items.sort(key=lambda it: (1 if it.get("done") else 0, -self.clamp_importance(it.get("importance", 0))))
        elif key == "alpha":
            items.sort(key=lambda it: str(it.get("text", "")).lower())
        for it in items:
            self._sort_items_recursive(it.get("children", []), key)

    def import_from_txt(self):
        path = filedialog.askopenfilename(
            title="Liste aus TXT laden",
            filetypes=[("Textdatei", "*.txt"), ("Alle Dateien", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            imported = self.parse_txt_items(lines)
            if imported:
                self.snapshot_undo()
                self.items.extend(imported)
                self.save_items()
                self.refresh_tree(selected_id=imported[-1]["id"])
                messagebox.showinfo("Import erfolgreich", f"{self.count_items(imported)} Punkte importiert.")
        except Exception as e:
            messagebox.showerror("Fehler beim Import", str(e))

    def parse_txt_items(self, lines):
        imported_root = []
        level_stack = {-1: imported_root}
        pattern = re.compile(r"^(?P<number>\d+(?:\.\d+)*)\.\s+(?P<text>.*)$")

        # Eigene Exporte beginnen mit Titel + Trennlinie. Den Kopf robust überspringen,
        # auch wenn der Listentitel vom aktuellen App-Titel abweicht.
        nonempty = [(idx, line.strip()) for idx, line in enumerate(lines) if line.strip()]
        skip_indices = set()
        if len(nonempty) >= 2 and nonempty[1][1] and set(nonempty[1][1]) <= {"="}:
            skip_indices.update({nonempty[0][0], nonempty[1][0]})

        for line_index, raw_line in enumerate(lines):
            if line_index in skip_indices:
                continue
            stripped = raw_line.strip()
            if (
                not stripped
                or stripped == self.app_title
                or stripped.startswith("Meine Liste")
                or stripped.startswith("===")
                or stripped.startswith("Exportiert am:")
            ):
                continue

            done = False
            importance = 0
            level = 0
            text = stripped
            match = pattern.match(stripped)
            if match:
                number = match.group("number")
                level = number.count(".")
                text = match.group("text").strip()
            elif ". " in stripped:
                # Abwärtskompatibilität für einfache alte Exporte.
                text = stripped.split(". ", 1)[1].strip()

            for marker, marker_importance in (("🚩 ", 3), ("⚑ ", 2), ("⚐ ", 1)):
                if text.startswith(marker):
                    importance = marker_importance
                    text = text[len(marker):].strip()
                    break

            if text.startswith("✓ "):
                done = True
                text = text[2:].strip()
            if text.startswith("✅ "):
                done = True
                text = text[2:].strip()

            if not text:
                continue

            new = self.new_item(text, done, importance=importance)
            parent_level = level - 1
            if parent_level not in level_stack:
                level = 0
                parent_level = -1

            level_stack[parent_level].append(new)
            level_stack[level] = new["children"]

            # Tiefere Stack-Ebenen entfernen, damit folgende Zeilen sauber einsortiert werden.
            for stack_level in list(level_stack.keys()):
                if stack_level > level:
                    del level_stack[stack_level]

        return imported_root

    def count_items(self, items):
        total = 0
        for item in items:
            total += 1
            total += self.count_items(item.get("children", []))
        return total

    # -----------------------------
    # Mausrad / Menü / Dialoge
    # -----------------------------
    def bind_mousewheel(self, widget):
        """Scrollrad-Unterstützung plattformübergreifend (Windows/macOS: MouseWheel, Linux: Button-4/5)."""
        widget.bind("<MouseWheel>", lambda e: self._on_mousewheel(e, widget))
        widget.bind("<Button-4>", lambda e: self._on_mousewheel(e, widget))
        widget.bind("<Button-5>", lambda e: self._on_mousewheel(e, widget))

    def _on_mousewheel(self, event, widget):
        num = getattr(event, "num", None)
        if num == 4:
            delta = -1
        elif num == 5:
            delta = 1
        else:
            delta = -1 if getattr(event, "delta", 0) > 0 else 1
        try:
            widget.yview_scroll(delta, "units")
        except tk.TclError:
            pass
        return "break"

    def create_menubar(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Neue Liste", accelerator="Strg+Shift+N", command=self.create_new_list)
        file_menu.add_command(label="Neuer Ordner", command=self.create_new_folder)
        file_menu.add_separator()
        file_menu.add_command(label="TXT importieren …", accelerator="Strg+I", command=self.import_from_txt)
        file_menu.add_command(label="TXT als neue Liste(n) …", command=self.import_txt_as_new_lists)
        export_menu = tk.Menu(file_menu, tearoff=0)
        export_menu.add_command(label="Als TXT …", accelerator="Strg+E", command=self.export_as_txt)
        export_menu.add_command(label="Als Markdown …", command=self.export_as_markdown)
        export_menu.add_command(label="Als CSV …", command=self.export_as_csv)
        file_menu.add_cascade(label="Aktive Liste exportieren", menu=export_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Komplettbackup speichern …", command=self.export_full_backup)
        file_menu.add_command(label="Komplettbackup laden …", command=self.import_full_backup)
        file_menu.add_command(label="Backup-Ordner öffnen", command=self.open_backup_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Beenden", accelerator="Strg+Q", command=self.on_close)
        menubar.add_cascade(label="Datei", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Rückgängig", accelerator="Strg+Z", command=self.undo_last_change)
        edit_menu.add_separator()
        edit_menu.add_command(label="Kopieren", accelerator="Strg+C", command=self.copy_selected_to_clipboard)
        edit_menu.add_command(label="Einfügen", accelerator="Strg+V", command=self.paste_items_from_clipboard)
        edit_menu.add_command(label="Alle auswählen", accelerator="Strg+A", command=self.select_all_items)
        edit_menu.add_separator()
        edit_menu.add_command(label="Punkt bearbeiten", accelerator="F2", command=self.edit_item)
        edit_menu.add_command(label="Wichtigkeit ändern", command=self.cycle_importance_selected)
        edit_menu.add_command(label="Fälligkeitsdatum …", accelerator="Strg+T", command=self.set_due_date_selected)
        edit_menu.add_command(label="Löschen", accelerator="Entf", command=self.delete_item)
        menubar.add_cascade(label="Bearbeiten", menu=edit_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Design wechseln (Hell/Dunkel)", accelerator="Strg+D", command=self.toggle_theme)
        view_menu.add_separator()
        view_menu.add_command(label="Aufklappen", command=self.expand_all)
        view_menu.add_command(label="Zuklappen", command=self.collapse_all)
        view_menu.add_separator()
        sort_menu = tk.Menu(view_menu, tearoff=0)
        sort_menu.add_command(label="Nach Fälligkeit", command=lambda: self.sort_current_list("due"))
        sort_menu.add_command(label="Nach Wichtigkeit", command=lambda: self.sort_current_list("importance"))
        sort_menu.add_command(label="Alphabetisch", command=lambda: self.sort_current_list("alpha"))
        view_menu.add_cascade(label="Aktive Liste sortieren", menu=sort_menu)
        menubar.add_cascade(label="Ansicht", menu=view_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Tastenkürzel anzeigen", command=self.show_shortcuts_dialog)
        help_menu.add_command(label=f"Über {APP_NAME}", command=self.show_about_dialog)
        menubar.add_cascade(label="Hilfe", menu=help_menu)

        try:
            self.root.config(menu=menubar)
        except tk.TclError:
            pass
        self.menubar = menubar

    def open_backup_folder(self):
        try:
            if sys.platform == "darwin":
                os.system(f'open "{BACKUP_DIR}"')
            elif os.name == "nt":
                os.startfile(BACKUP_DIR)  # type: ignore[attr-defined]
            else:
                os.system(f'xdg-open "{BACKUP_DIR}"')
        except Exception as e:
            messagebox.showinfo("Backup-Ordner", f"Die automatischen Sicherungen liegen unter:\n{BACKUP_DIR}\n\n({e})")

    def show_about_dialog(self):
        messagebox.showinfo(
            f"Über {APP_NAME}",
            f"{APP_PRODUCT_NAME}\n"
            f"Version {APP_VERSION}\n\n"
            "Eine schlanke, lokale App für Aufgaben und verschachtelte Listen.\n"
            "Alle Daten bleiben auf diesem Gerät.\n\n"
            f"Speicherort der Daten:\n{BASE_DIR}",
        )

    def show_shortcuts_dialog(self):
        shortcuts = (
            "Enter – Punkt hinzufügen\n"
            "Doppelklick / Leertaste – erledigt umschalten\n"
            "Rechtsklick / Strg+Shift+F – Wichtigkeit ändern\n"
            "Strg+T – Fälligkeitsdatum setzen oder entfernen\n"
            "F2 – Punkt bearbeiten · F3 – Titel bearbeiten\n"
            "Rechtsklick auf Liste oder Ordner – Farbe wählen\n"
            "Tab – ein-/ausrücken · Drag & Drop – Reihenfolge ändern\n"
            "Shift+Drag – Unterpunkt · Shift+Klick – Bereich auswählen\n"
            "Strg+A – alle auswählen · Strg+Z – rückgängig\n"
            "Strg+C / Strg+V – kopieren / einfügen\n"
            "Strg+F – Suche · Strg+E – Export TXT · Strg+I – Import TXT\n"
            "Strg+D – Design wechseln · Strg+S – speichern\n"
            "Strg+Shift+N – neue Liste · Strg+W – Liste löschen"
        )
        messagebox.showinfo("Tastenkürzel", shortcuts)


if __name__ == "__main__":
    root = tk.Tk()
    app = ListApp(root)
    root.mainloop()
