import calendar
import copy
import csv
import ctypes
import json
import mimetypes
import os
import re
import shutil
import stat
import sys
import tempfile
import tkinter as tk
import tkinter.ttk as ttk
import uuid
import zipfile
from tkinter import messagebox, filedialog
from datetime import datetime, date, timedelta

# --- Produkt-Branding -------------------------------------------------------
APP_NAME = "Glide"
APP_TAGLINE = "Aufgaben und Listen"
APP_PRODUCT_NAME = f"{APP_NAME} \u2013 {APP_TAGLINE}"
APP_VERSION = "2.5.3"
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
ATTACHMENTS_DIR = os.path.join(BASE_DIR, "attachments")
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(ATTACHMENTS_DIR, exist_ok=True)


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
    DATA_SCHEMA_VERSION = 5
    MIN_PORTABLE_BACKUP_SCHEMA_VERSION = 4
    MAX_BACKUP_MEMBERS = 4096
    MAX_BACKUP_DATA_BYTES = 32 * 1024 * 1024
    MAX_BACKUP_ATTACHMENT_BYTES = 512 * 1024 * 1024
    MAX_BACKUP_TOTAL_BYTES = 2 * 1024 * 1024 * 1024
    MAX_BACKUP_COMPRESSION_RATIO = 500
    BACKUP_COPY_CHUNK = 1024 * 1024
    MAX_ITEM_DEPTH = 100
    MAX_BACKUP_ITEMS = 200000
    IMPORTANCE_MARKERS = {0: "", 1: "⚐ ", 2: "⚑ ", 3: "🚩 "}
    IMPORTANCE_NAMES = {0: "keine", 1: "niedrig", 2: "mittel", 3: "hoch"}
    SIDEBAR_SECTION_FONT = ("TkDefaultFont", 12, "bold")
    DUE_COLUMN_WIDTH = 132
    TASK_TREE_EDGE_PADDING = 2

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
    ITEM_COLOR_CHOICES = LIST_COLOR_CHOICES
    ITEM_COLOR_KEYS = LIST_COLOR_KEYS
    WINDOWS_CHROME_RETRY_DELAYS_MS = (0, 40, 120, 300)

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
        self.active_folder_id = None
        self.view_mode = "list"
        self.undo_stack = []
        self.dirty = False
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
        self.drag_item_ids = []
        self.expanded_ids = set()
        self._item_context_menu = None

        self.theme_name = self.settings.get("theme", "light")
        if self.theme_name not in self.THEMES:
            self.theme_name = "light"
        self.active_list_id = self.settings.get("active_list_id") if isinstance(self.settings.get("active_list_id"), str) else None
        saved_folder_id = self.settings.get("active_folder_id")
        self.active_folder_id = saved_folder_id if isinstance(saved_folder_id, str) and saved_folder_id else None
        self.view_mode = "folder" if self.active_folder_id else "list"
        self.app_title = self.settings.get("title", "Meine Liste").strip() or "Meine Liste"
        self.theme = self.THEMES[self.theme_name]
        self.theme_widgets = []
        self.rounded_containers = []
        self.buttons = []

        if os.name == "nt":
            # Der native Wrapper-HWND existiert beim ersten apply_theme-Aufruf
            # häufig noch nicht. Nach jedem echten Mapping erneut anwenden.
            self.root.bind("<Map>", self._on_windows_window_map, add="+")

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
        self.root.bind("<Control-q>", lambda e: self.on_close())
        self.root.bind("<Control-z>", self.undo_last_change)
        self.root.bind("<Control-c>", self.copy_selected_to_clipboard)
        self.root.bind("<Control-v>", self.paste_items_from_clipboard)
        self.root.bind("<Control-a>", self.select_all_items)
        # Command ist nur unter macOS Meta/Cmd. Unter Windows ordnet Tk diesen
        # Modifikator Num-Lock zu; dadurch wurden normale Buchstaben wie a/f
        # fälschlich als Tastenkürzel behandelt und der Fokus sprang zur Suche.
        if sys.platform == "darwin":
            self.root.bind("<Command-c>", self.copy_selected_to_clipboard)
            self.root.bind("<Command-v>", self.paste_items_from_clipboard)
            self.root.bind("<Command-a>", self.select_all_items)
            self.root.bind("<Command-z>", self.undo_last_change)
            self.root.bind("<Command-f>", self.focus_search)
            self.root.bind("<Command-t>", self.set_due_date_selected)
        self.root.bind("<Control-n>", self.handle_control_n)
        self.root.bind("<Control-N>", self.handle_control_n)
        self.root.bind("<Control-w>", self.delete_current_list)
        self.root.bind("<Control-f>", self.handle_control_f)
        self.root.bind("<Control-F>", self.handle_control_f)
        self.root.bind("<Alt-p>", self.cycle_importance_selected)
        self.root.bind("<Escape>", self.handle_escape)
        self.root.bind("<F2>", lambda e: self.edit_item())
        self.root.bind("<F3>", lambda e: self.edit_title())
        self.root.bind("<Control-d>", lambda e: self.toggle_theme())
        self.root.bind("<Control-t>", self.set_due_date_selected)
        self.root.bind("<Control-m>", self.edit_page_note)

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
                        "active_folder_id": self.active_folder_id if self.view_mode == "folder" else None,
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
        self.root.title(f"{self.get_display_title()} \u00b7 {APP_NAME}")

    def get_folder(self, folder_id):
        return next((folder for folder in self.folders if folder.get("id") == folder_id), None)

    def get_folder_lists(self, folder_id):
        return [entry for entry in self.lists if entry.get("folder_id") == folder_id]

    def get_display_title(self):
        if self.view_mode == "folder" and self.active_folder_id:
            folder = self.get_folder(self.active_folder_id)
            if folder:
                return str(folder.get("title") or "Ordner").strip() or "Ordner"
        return self.app_title

    def get_active_page(self):
        if self.view_mode == "folder" and self.active_folder_id:
            return self.get_folder(self.active_folder_id)
        return self.current_list() if self.lists else None

    def require_list_view(self, message=True):
        """Verhindert, dass Aktionen unsichtbar die zuletzt geöffnete Liste ändern."""
        if self.view_mode == "list":
            return True
        if message:
            messagebox.showinfo("Ordnerübersicht", "Öffne zuerst eine Liste in diesem Ordner.")
        return False

    def register_theme_widget(self, widget, bg_key="bg", fg_key=None):
        self.theme_widgets.append((widget, bg_key, fg_key))
        return widget

    @staticmethod
    def bind_optional(widget, sequence, callback):
        """Bindet plattformspezifische Tk-Sequenzen ohne den App-Start zu blockieren."""
        try:
            widget.bind(sequence, callback)
            return True
        except tk.TclError:
            return False

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
        self._schedule_windows_chrome_theme(dialog)
        entry.focus_set()
        dialog.grab_set()
        self.root.wait_window(dialog)
        return result["value"]

    def themed_multiline_dialog(self, title, prompt="", initial="", ok_text="Speichern"):
        """Mehrzeiliger, themenkonformer Editor für Seiten- und Aufgaben-Notizen."""
        result = {"value": None}
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.configure(bg=self.theme["bg"])
        dialog.transient(self.root)
        dialog.minsize(560, 380)

        container = tk.Frame(dialog, bg=self.theme["bg"])
        container.pack(fill="both", expand=True, padx=24, pady=22)
        tk.Label(
            container,
            text=title,
            bg=self.theme["bg"],
            fg=self.theme["text"],
            font=("TkDefaultFont", 15, "bold"),
            anchor="w",
        ).pack(anchor="w", pady=(0, 6))
        if prompt:
            tk.Label(
                container,
                text=prompt,
                bg=self.theme["bg"],
                fg=self.theme["muted"],
                font=("TkDefaultFont", 10),
                anchor="w",
                justify="left",
            ).pack(anchor="w", pady=(0, 12))

        border = tk.Frame(container, bg=self.theme["input_border"])
        border.pack(fill="both", expand=True)
        text = tk.Text(
            border,
            wrap="word",
            undo=True,
            bg=self.theme["input"],
            fg=self.theme["text"],
            insertbackground=self.theme["text"],
            selectbackground=self.theme["selection"],
            selectforeground="#FFFFFF",
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=("TkDefaultFont", 11),
            padx=12,
            pady=10,
        )
        text.pack(fill="both", expand=True, padx=1, pady=1)
        text.insert("1.0", initial or "")

        button_row = tk.Frame(container, bg=self.theme["bg"])
        button_row.pack(fill="x", pady=(16, 0))

        def submit(event=None):
            result["value"] = text.get("1.0", "end-1c")
            dialog.destroy()
            return "break"

        def cancel(event=None):
            dialog.destroy()
            return "break"

        self._make_dialog_button(button_row, ok_text, submit, "confirm").pack(side="right")
        self._make_dialog_button(button_row, "Abbrechen", cancel, "muted").pack(side="right", padx=(0, 10))

        dialog.bind("<Control-Return>", submit)
        if sys.platform == "darwin":
            dialog.bind("<Command-Return>", submit)
        dialog.bind("<Escape>", cancel)
        dialog.protocol("WM_DELETE_WINDOW", cancel)
        self._center_dialog(dialog, min_width=620)
        self._schedule_windows_chrome_theme(dialog)
        text.focus_set()
        dialog.grab_set()
        self.root.wait_window(dialog)
        return result["value"]

    @staticmethod
    def format_file_size(size):
        try:
            value = float(size)
        except (TypeError, ValueError):
            value = 0.0
        units = ("B", "KB", "MB", "GB")
        unit = units[0]
        for candidate in units:
            unit = candidate
            if value < 1024 or candidate == units[-1]:
                break
            value /= 1024
        return f"{int(value)} {unit}" if unit == "B" else f"{value:.1f} {unit}"

    def themed_choice_dialog(self, title, prompt, choices):
        """Kleine modale Auswahl; choices enthält (Wert, sichtbarer Text)."""
        if not choices:
            return None
        result = {"value": None}
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.configure(bg=self.theme["bg"])
        dialog.transient(self.root)
        dialog.resizable(False, False)
        container = tk.Frame(dialog, bg=self.theme["bg"])
        container.pack(fill="both", expand=True, padx=24, pady=22)
        tk.Label(
            container, text=title, bg=self.theme["bg"], fg=self.theme["text"],
            font=("TkDefaultFont", 15, "bold"), anchor="w",
        ).pack(anchor="w", pady=(0, 6))
        tk.Label(
            container, text=prompt, bg=self.theme["bg"], fg=self.theme["muted"],
            font=("TkDefaultFont", 10), anchor="w", justify="left",
        ).pack(anchor="w", pady=(0, 12))
        listbox = tk.Listbox(
            container,
            height=min(9, max(3, len(choices))), width=48,
            bg=self.theme["input"], fg=self.theme["text"],
            selectbackground=self.theme["selection"], selectforeground="#FFFFFF",
            activestyle="none", relief="flat", bd=0, highlightthickness=1,
            highlightbackground=self.theme["input_border"], font=("TkDefaultFont", 10),
        )
        listbox.pack(fill="both", expand=True)
        for _value, label in choices:
            listbox.insert(tk.END, label)
        listbox.selection_set(0)
        listbox.activate(0)

        footer = tk.Frame(container, bg=self.theme["bg"])
        footer.pack(fill="x", pady=(16, 0))

        def submit(event=None):
            selection = listbox.curselection()
            if selection:
                result["value"] = choices[int(selection[0])][0]
            dialog.destroy()
            return "break"

        def cancel(event=None):
            dialog.destroy()
            return "break"

        self._make_dialog_button(footer, "Auswählen", submit, "confirm").pack(side="right")
        self._make_dialog_button(footer, "Abbrechen", cancel, "muted").pack(side="right", padx=(0, 10))
        listbox.bind("<Double-Button-1>", submit)
        dialog.bind("<Return>", submit)
        dialog.bind("<Escape>", cancel)
        dialog.protocol("WM_DELETE_WINDOW", cancel)
        self._center_dialog(dialog, min_width=520)
        self._schedule_windows_chrome_theme(dialog)
        listbox.focus_set()
        dialog.grab_set()
        self.root.wait_window(dialog)
        return result["value"]

    def open_external_path(self, path):
        try:
            if not path or not os.path.exists(path):
                messagebox.showwarning("Datei öffnen", "Die Datei ist nicht mehr vorhanden.")
                return False
            if os.name == "nt":
                os.startfile(path)  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                import subprocess
                subprocess.Popen(["open", path])
            else:
                import subprocess
                subprocess.Popen(["xdg-open", path])
            return True
        except Exception as exc:
            messagebox.showerror("Datei öffnen", f"Die Datei konnte nicht geöffnet werden:\n{exc}")
            return False

    def themed_item_details_dialog(self, item):
        """Bearbeitet Titel, Beschreibung und lokale Datei-/Bildanhänge eines Punkts."""
        result = {"value": None}
        attachments = copy.deepcopy(item.get("attachments", []))

        dialog = tk.Toplevel(self.root)
        dialog.title("Punktdetails")
        dialog.configure(bg=self.theme["bg"])
        dialog.transient(self.root)
        dialog.minsize(680, 590)

        container = tk.Frame(dialog, bg=self.theme["bg"])
        container.pack(fill="both", expand=True, padx=24, pady=22)
        tk.Label(
            container,
            text="Punktdetails",
            bg=self.theme["bg"],
            fg=self.theme["text"],
            font=("TkDefaultFont", 16, "bold"),
            anchor="w",
        ).pack(anchor="w", pady=(0, 16))

        tk.Label(
            container, text="Titel", bg=self.theme["bg"], fg=self.theme["muted"],
            font=("TkDefaultFont", 9, "bold"), anchor="w",
        ).pack(anchor="w", pady=(0, 5))
        title_border = tk.Frame(container, bg=self.theme["input_border"])
        title_border.pack(fill="x", pady=(0, 14))
        title_entry = tk.Entry(
            title_border,
            bg=self.theme["input"], fg=self.theme["text"], insertbackground=self.theme["text"],
            selectbackground=self.theme["selection"], selectforeground="#FFFFFF",
            relief="flat", bd=0, highlightthickness=0, font=("TkDefaultFont", 12),
        )
        title_entry.pack(fill="x", padx=1, pady=1, ipady=9)
        title_entry.insert(0, item.get("text", ""))

        tk.Label(
            container, text="Beschreibung", bg=self.theme["bg"], fg=self.theme["muted"],
            font=("TkDefaultFont", 9, "bold"), anchor="w",
        ).pack(anchor="w", pady=(0, 5))
        description_border = tk.Frame(container, bg=self.theme["input_border"])
        description_border.pack(fill="both", expand=True, pady=(0, 14))
        description_text = tk.Text(
            description_border,
            height=8, wrap="word", undo=True,
            bg=self.theme["input"], fg=self.theme["text"], insertbackground=self.theme["text"],
            selectbackground=self.theme["selection"], selectforeground="#FFFFFF",
            relief="flat", bd=0, highlightthickness=0, font=("TkDefaultFont", 10),
            padx=10, pady=8,
        )
        description_text.pack(fill="both", expand=True, padx=1, pady=1)
        description_text.insert("1.0", item.get("description", ""))

        attachment_heading = tk.Frame(container, bg=self.theme["bg"])
        attachment_heading.pack(fill="x", pady=(0, 5))
        tk.Label(
            attachment_heading, text="Anhänge", bg=self.theme["bg"], fg=self.theme["muted"],
            font=("TkDefaultFont", 9, "bold"), anchor="w",
        ).pack(side="left")
        tk.Label(
            attachment_heading,
            text="Bilder und andere Dateien werden als lokale Kopie gespeichert.",
            bg=self.theme["bg"], fg=self.theme["placeholder"], font=("TkDefaultFont", 8), anchor="e",
        ).pack(side="right")

        attachment_border = tk.Frame(container, bg=self.theme["input_border"])
        attachment_border.pack(fill="x")
        attachment_list = tk.Listbox(
            attachment_border,
            height=5,
            bg=self.theme["input"], fg=self.theme["text"],
            selectbackground=self.theme["selection"], selectforeground="#FFFFFF",
            activestyle="none", relief="flat", bd=0, highlightthickness=0,
            font=("TkDefaultFont", 9),
        )
        attachment_list.pack(fill="x", padx=1, pady=1)

        def attachment_path(entry):
            if entry.get("pending_path"):
                return entry.get("pending_path")
            return self.resolve_attachment_path(entry)

        def render_attachments(select_index=None):
            attachment_list.delete(0, tk.END)
            for attachment in attachments:
                path = attachment_path(attachment)
                exists = bool(path and os.path.isfile(path))
                if attachment.get("pending_path") and exists:
                    try:
                        size = os.path.getsize(path)
                    except OSError:
                        size = 0
                else:
                    size = attachment.get("size", 0)
                state = "" if exists else "  ·  nicht gefunden"
                attachment_list.insert(
                    tk.END,
                    f"📎  {attachment.get('name', 'Anhang')}  ·  {self.format_file_size(size)}{state}",
                )
            if attachments:
                index = min(select_index if select_index is not None else 0, len(attachments) - 1)
                attachment_list.selection_set(index)
                attachment_list.activate(index)

        def add_attachments():
            paths = filedialog.askopenfilenames(title="Dateien oder Bilder anhängen", parent=dialog)
            known = {os.path.normcase(os.path.abspath(attachment_path(a) or "")) for a in attachments}
            for path in paths:
                normalized = os.path.normcase(os.path.abspath(path))
                if normalized in known:
                    continue
                attachments.append({"name": os.path.basename(path), "pending_path": path})
                known.add(normalized)
            render_attachments(len(attachments) - 1)

        def selected_attachment_index():
            selection = attachment_list.curselection()
            return int(selection[0]) if selection else None

        def open_attachment(event=None):
            index = selected_attachment_index()
            if index is not None:
                self.open_external_path(attachment_path(attachments[index]))
            return "break"

        def remove_attachment():
            index = selected_attachment_index()
            if index is None:
                return
            # Die physische Kopie bleibt für Rückgängig/ältere Backups erhalten.
            attachments.pop(index)
            render_attachments(max(0, index - 1))

        action_row = tk.Frame(container, bg=self.theme["bg"])
        action_row.pack(fill="x", pady=(9, 0))
        self._make_dialog_button(action_row, "+ Datei", add_attachments, "due_action", width=104, height=36).pack(side="left")
        self._make_dialog_button(action_row, "Öffnen", open_attachment, "export", width=104, height=36).pack(side="left", padx=(8, 0))
        self._make_dialog_button(action_row, "Entfernen", remove_attachment, "delete", width=104, height=36).pack(side="left", padx=(8, 0))
        attachment_list.bind("<Double-Button-1>", open_attachment)
        render_attachments()

        footer = tk.Frame(container, bg=self.theme["bg"])
        footer.pack(fill="x", pady=(18, 0))

        def submit(event=None):
            title = title_entry.get().strip()
            if not title:
                messagebox.showwarning("Hinweis", "Bitte einen Titel eingeben.", parent=dialog)
                title_entry.focus_set()
                return "break"
            stored_attachments = []
            for attachment in attachments:
                if attachment.get("pending_path"):
                    try:
                        stored = self.store_attachment(attachment["pending_path"])
                    except Exception as exc:
                        messagebox.showerror(
                            "Anhang speichern",
                            f"'{attachment.get('name', 'Datei')}' konnte nicht gespeichert werden:\n{exc}",
                            parent=dialog,
                        )
                        return "break"
                    attachment.clear()
                    attachment.update(stored)
                stored_attachments.append(copy.deepcopy(attachment))
            result["value"] = {
                "text": title,
                "description": description_text.get("1.0", "end-1c"),
                "attachments": stored_attachments,
            }
            dialog.destroy()
            return "break"

        def cancel(event=None):
            dialog.destroy()
            return "break"

        self._make_dialog_button(footer, "Speichern", submit, "confirm").pack(side="right")
        self._make_dialog_button(footer, "Abbrechen", cancel, "muted").pack(side="right", padx=(0, 10))
        dialog.bind("<Control-Return>", submit)
        if sys.platform == "darwin":
            dialog.bind("<Command-Return>", submit)
        dialog.bind("<Escape>", cancel)
        dialog.protocol("WM_DELETE_WINDOW", cancel)
        self._center_dialog(dialog, min_width=720)
        self._schedule_windows_chrome_theme(dialog)
        title_entry.focus_set()
        title_entry.select_range(0, tk.END)
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
        self._schedule_windows_chrome_theme(dialog)
        dialog.grab_set()
        self.root.wait_window(dialog)
        return result["value"]


    # -----------------------------
    # Mehrere Listen / Seitenregister
    # -----------------------------
    def new_list_object(
        self,
        title=None,
        items=None,
        list_id=None,
        folder_id=None,
        color=None,
        note="",
        system_role=None,
    ):
        title = (title or "Neue Liste").strip() or "Neue Liste"
        return {
            "id": list_id or uuid.uuid4().hex,
            "title": title,
            "folder_id": folder_id if isinstance(folder_id, str) and folder_id else None,
            "color": color if color in self.LIST_COLOR_KEYS else None,
            "note": str(note or ""),
            "system_role": "inbox" if system_role == "inbox" else None,
            "items": items if isinstance(items, list) else [],
        }

    def new_folder_object(self, title=None, folder_id=None, color=None, note=""):
        title = (title or "Neuer Ordner").strip() or "Neuer Ordner"
        return {
            "id": folder_id or uuid.uuid4().hex,
            "title": title,
            "color": color if color in self.LIST_COLOR_KEYS else None,
            "note": str(note or ""),
        }

    def is_inbox_list(self, entry_or_id):
        if isinstance(entry_or_id, dict):
            entry = entry_or_id
        else:
            entry = next((item for item in self.lists if item.get("id") == entry_or_id), None)
        return bool(entry and entry.get("system_role") == "inbox")

    def ensure_inbox_list(self):
        """Stellt genau einen geschützten, immer oben angeordneten Eingang sicher."""
        before = [
            (entry.get("id"), entry.get("title"), entry.get("folder_id"), entry.get("system_role"))
            for entry in self.lists
        ]
        inboxes = [entry for entry in self.lists if self.is_inbox_list(entry)]
        if inboxes:
            inbox = inboxes[0]
            for duplicate in inboxes[1:]:
                duplicate["system_role"] = None
        else:
            inbox = self.new_list_object("Eingang", [], system_role="inbox", color="due_action")
            self.lists.insert(0, inbox)
        inbox["title"] = "Eingang"
        inbox["folder_id"] = None
        self.lists = [inbox] + [entry for entry in self.lists if entry is not inbox]
        after = [
            (entry.get("id"), entry.get("title"), entry.get("folder_id"), entry.get("system_role"))
            for entry in self.lists
        ]
        self._last_inbox_repair = before != after
        return inbox

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
        # In der Ordnerübersicht zeigt der Kopf den Ordnertitel. Der Titel der
        # zuletzt aktiven Liste darf dadurch beim Speichern nicht überschrieben werden.
        if self.view_mode == "list":
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

        self.view_mode = "list"
        self.active_folder_id = None
        self.active_list_id = target["id"]
        self.items = target.setdefault("items", [])
        self.app_title = target.get("title", "Meine Liste").strip() or "Meine Liste"
        self.expanded_ids = set()
        self.selection_anchor_id = None
        self.update_window_title()
        if hasattr(self, "title_label"):
            self.title_label.configure(text=self.app_title)
        self.update_page_note_preview()
        self.update_entry_mode()
        if refresh:
            self.update_sidebar_list()
            self.refresh_tree()
            self.save_settings()

    def set_active_folder(self, folder_id, refresh=True):
        folder = self.get_folder(folder_id)
        if not folder:
            return
        if self.active_list_id and self.lists:
            self.sync_current_list_reference()
        self.view_mode = "folder"
        self.active_folder_id = folder_id
        self.expanded_ids = set()
        self.selection_anchor_id = None
        self.update_window_title()
        if hasattr(self, "title_label"):
            self.title_label.configure(text=self.get_display_title())
        self.update_page_note_preview()
        self.update_entry_mode()
        if refresh:
            self.update_sidebar_list()
            self.refresh_tree()
            self.save_settings()

    def create_list_sidebar(self):
        # Der Eingang ist bewusst kein Bestandteil des normalen Listenbaums:
        # ein eigenes, einzeiliges Feld plus Abstand macht seinen Systemstatus
        # sichtbar, ohne Klick- oder Task-Drop-Verhalten zu verlieren.
        self.inbox_listbox = ttk.Treeview(
            self.sidebar_frame,
            show="tree",
            selectmode="browse",
            style="Sidebar.Treeview",
            takefocus=True,
            height=1,
        )
        self.inbox_listbox.pack(fill="x", pady=(4, 18))
        self.inbox_listbox.heading("#0", text="")
        self.inbox_listbox.column("#0", anchor="w", stretch=True, width=220)
        self.inbox_listbox.bind("<<TreeviewSelect>>", self.on_inbox_select)
        self.inbox_listbox.bind("<Button-3>", self.show_sidebar_context_menu)
        self.inbox_listbox.bind("<Button-2>", self.show_sidebar_context_menu)
        self.inbox_listbox.bind("<Control-Button-1>", self.show_sidebar_context_menu)
        self.bind_mousewheel(self.inbox_listbox)

        title_row = self.register_theme_widget(tk.Frame(self.sidebar_frame, bg=self.theme["card"]), "card")
        title_row.pack(fill="x", pady=(0, 10))

        self.sidebar_title = self.register_theme_widget(
            tk.Label(
                title_row,
                text="Listen",
                font=self.SIDEBAR_SECTION_FONT,
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
        self.sidebar_listbox.heading("#0", text="")
        self.sidebar_listbox.column("#0", anchor="w", stretch=True, width=220)
        self.sidebar_listbox.bind("<<TreeviewSelect>>", self.on_sidebar_select)
        self.sidebar_listbox.bind("<Double-Button-1>", self.edit_selected_sidebar_title)
        self.sidebar_listbox.bind("<Tab>", self.toggle_sidebar_indent)
        self.sidebar_listbox.bind("<Shift-Tab>", self.outdent_selected_sidebar_list)
        self.bind_optional(self.sidebar_listbox, "<ISO_Left_Tab>", self.outdent_selected_sidebar_list)
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

        # Der flexible Listenbaum wird bewusst erst nach den unteren Aktionen
        # gepackt. So reserviert der Packer bei 1000x800 und selbst bei der
        # Mindesthöhe zuerst den vollständigen Aktionsbereich, statt ihn unten
        # abzuschneiden.
        self.sidebar_listbox.pack(fill="both", expand=True)

    def update_sidebar_list(self):
        if not hasattr(self, "sidebar_listbox") or not hasattr(self, "inbox_listbox"):
            return
        self._updating_sidebar = True
        try:
            self.sidebar_rows = []
            self.sidebar_iid_to_row = {}
            for row_id in self.inbox_listbox.get_children(""):
                self.inbox_listbox.delete(row_id)
            for row_id in self.sidebar_listbox.get_children(""):
                self.sidebar_listbox.delete(row_id)

            assigned_folder_ids = {folder.get("id") for folder in self.folders if isinstance(folder, dict)}

            # Der feste Eingang steht in seinem eigenen einzeiligen Feld.
            inbox = next((entry for entry in self.lists if self.is_inbox_list(entry)), None)
            if inbox:
                self._insert_sidebar_list_row(inbox, parent="", tree=self.inbox_listbox)

            # Danach alle übrigen Listen ohne Ordner anzeigen.
            for entry in self.lists:
                if self.is_inbox_list(entry):
                    continue
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

            inbox_selection = self.inbox_listbox.selection()
            if inbox_selection:
                self.inbox_listbox.selection_remove(*inbox_selection)
            sidebar_selection = self.sidebar_listbox.selection()
            if sidebar_selection:
                self.sidebar_listbox.selection_remove(*sidebar_selection)
            if self.view_mode == "folder" and self.active_folder_id:
                active_iid = f"folder:{self.active_folder_id}"
            else:
                active_iid = f"list:{self.active_list_id}" if self.active_list_id else None
            if active_iid and self.inbox_listbox.exists(active_iid):
                self.inbox_listbox.selection_set(active_iid)
                self.inbox_listbox.focus(active_iid)
            elif active_iid and self.sidebar_listbox.exists(active_iid):
                self.sidebar_listbox.selection_set(active_iid)
                self.sidebar_listbox.focus(active_iid)
                self.sidebar_listbox.see(active_iid)
            elif self.inbox_listbox.get_children(""):
                first = self.inbox_listbox.get_children("")[0]
                self.inbox_listbox.selection_set(first)
                self.inbox_listbox.focus(first)
            elif self.sidebar_listbox.get_children(""):
                first = self.sidebar_listbox.get_children("")[0]
                self.sidebar_listbox.selection_set(first)
                self.sidebar_listbox.focus(first)
        finally:
            self._updating_sidebar = False

    def _insert_sidebar_list_row(self, entry, parent="", tree=None):
        target_tree = tree or self.sidebar_listbox
        title = entry.get("title", "Meine Liste").strip() or "Meine Liste"
        item_count = self.count_items(entry.get("items", []))
        item_id = entry.get("id")
        if not item_id:
            item_id = uuid.uuid4().hex
            entry["id"] = item_id
        is_inbox = self.is_inbox_list(entry)
        preview = f"{title}  ({item_count})"
        iid = f"list:{item_id}"
        if is_inbox:
            tags = ("inbox",)
        else:
            color_key = entry.get("color") if entry.get("color") in self.LIST_COLOR_KEYS else None
            tags = (f"listcolor_{color_key}",) if color_key else ("list",)
        target_tree.insert(parent, "end", iid=iid, text=preview, tags=tags)
        self.sidebar_rows.append(("list", item_id))
        self.sidebar_iid_to_row[iid] = ("list", item_id)

    def get_selected_sidebar_row(self):
        if not hasattr(self, "sidebar_listbox"):
            return None
        if hasattr(self, "inbox_listbox"):
            inbox_selection = self.inbox_listbox.selection()
            if inbox_selection:
                return self.sidebar_iid_to_row.get(inbox_selection[0])
        selection = self.sidebar_listbox.selection()
        if not selection:
            return None
        return self.sidebar_iid_to_row.get(selection[0])

    def get_sidebar_iid_for_row(self, row):
        if not row:
            return None
        row_type, row_id = row
        return f"{row_type}:{row_id}"

    def get_sidebar_tree_for_iid(self, iid):
        if not iid:
            return None
        for tree_name in ("inbox_listbox", "sidebar_listbox"):
            tree = getattr(self, tree_name, None)
            try:
                if tree is not None and tree.exists(iid):
                    return tree
            except tk.TclError:
                continue
        return None

    def on_inbox_select(self, event=None):
        if getattr(self, "_updating_sidebar", False):
            return
        selection = self.inbox_listbox.selection()
        if not selection:
            return
        sidebar_selection = self.sidebar_listbox.selection()
        if sidebar_selection:
            self.sidebar_listbox.selection_remove(*sidebar_selection)
        row = self.sidebar_iid_to_row.get(selection[0])
        if row and row[0] == "list" and (row[1] != self.active_list_id or self.view_mode != "list"):
            self.set_active_list(row[1])

    def on_sidebar_select(self, event=None):
        if getattr(self, "_updating_sidebar", False):
            return
        if self.sidebar_listbox.selection() and hasattr(self, "inbox_listbox"):
            inbox_selection = self.inbox_listbox.selection()
            if inbox_selection:
                self.inbox_listbox.selection_remove(*inbox_selection)
        row = self.get_selected_sidebar_row()
        if not row:
            return
        row_type, row_id = row
        if row_type == "list":
            if row_id != self.active_list_id or self.view_mode != "list":
                self.set_active_list(row_id)
        elif row_type == "folder":
            if row_id != self.active_folder_id or self.view_mode != "folder":
                self.set_active_folder(row_id)

    def edit_selected_sidebar_title(self, event=None):
        row = self.get_selected_sidebar_row()
        if row and row[0] == "folder":
            return self.edit_folder_title(row[1])
        if row and row[0] == "list" and self.is_inbox_list(row[1]):
            messagebox.showinfo("Eingang", "Der fest integrierte Eingang behält seinen Namen.")
            return "break"
        return self.edit_title()

    def show_sidebar_context_menu(self, event):
        """Rechtsklick auf eine Liste oder einen Ordner: schnelle Farbauswahl."""
        tree = event.widget if event.widget in (getattr(self, "inbox_listbox", None), self.sidebar_listbox) else self.sidebar_listbox
        iid = tree.identify_row(event.y)
        if not iid:
            return "break"
        if tree is self.inbox_listbox:
            sidebar_selection = self.sidebar_listbox.selection()
            if sidebar_selection:
                self.sidebar_listbox.selection_remove(*sidebar_selection)
        else:
            inbox_selection = self.inbox_listbox.selection()
            if inbox_selection:
                self.inbox_listbox.selection_remove(*inbox_selection)
        tree.selection_set(iid)
        tree.focus(iid)
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
        self.snapshot_undo()
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
        if new_title == current_title:
            return "break"
        self.snapshot_undo()
        folder["title"] = new_title
        if self.view_mode == "folder" and self.active_folder_id == folder_id:
            self.title_label.configure(text=new_title)
            self.update_window_title()
        self.save_items()
        self.update_sidebar_list()
        return "break"

    def create_new_folder(self, event=None):
        title = self.themed_input_dialog("Neuer Ordner", "Titel des neuen Ordners:", ok_text="Anlegen")
        if title is None:
            return "break"
        self.snapshot_undo()
        self.folders.append(self.new_folder_object(title.strip() or "Neuer Ordner"))
        self.save_items()
        self.update_sidebar_list()
        return "break"

    def delete_selected_sidebar_entry(self, event=None):
        row = self.get_selected_sidebar_row()
        if row and row[0] == "folder":
            return self.delete_folder(row[1])
        if row and row[0] == "list" and self.is_inbox_list(row[1]):
            messagebox.showinfo("Eingang", "Der fest integrierte Eingang kann nicht gelöscht werden.")
            return "break"
        return self.delete_current_list(event)

    def delete_folder(self, folder_id):
        folder = next((entry for entry in self.folders if entry.get("id") == folder_id), None)
        if not folder:
            return "break"
        title = folder.get("title", "Ordner")
        if not messagebox.askyesno("Ordner löschen", f"Ordner '{title}' löschen?\n\nDie enthaltenen Listen bleiben erhalten und werden auf die Hauptebene verschoben."):
            return "break"
        self.snapshot_undo()
        for entry in self.lists:
            if entry.get("folder_id") == folder_id:
                entry["folder_id"] = None
        self.folders = [entry for entry in self.folders if entry.get("id") != folder_id]
        if self.view_mode == "folder" and self.active_folder_id == folder_id:
            inbox = self.ensure_inbox_list()
            self.active_folder_id = None
            self.set_active_list(inbox.get("id"), refresh=False)
        self.save_items()
        self.update_sidebar_list()
        self.refresh_tree()
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
        if self.is_inbox_list(list_entry):
            messagebox.showinfo("Eingang", "Der Eingang bleibt fest oberhalb aller Ordner und Listen.")
            return "break"
        if list_entry.get("folder_id"):
            self.snapshot_undo()
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
        self.snapshot_undo()
        list_entry["folder_id"] = target_folder_id
        self.save_items()
        self.update_sidebar_list()
        return "break"

    def outdent_selected_sidebar_list(self, event=None):
        row = self.get_selected_sidebar_row()
        if not row or row[0] != "list":
            return "break"
        list_entry = next((entry for entry in self.lists if entry.get("id") == row[1]), None)
        if list_entry and not self.is_inbox_list(list_entry):
            if not list_entry.get("folder_id"):
                return "break"
            self.snapshot_undo()
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
        target_iid, _target_row = self.identify_sidebar_drop_row(event)
        self.clear_sidebar_drop_target_tags()
        if target_iid and target_iid != self.sidebar_drag_start_iid:
            try:
                target_tree = self.get_sidebar_tree_for_iid(target_iid)
                if target_tree is None:
                    return
                tags = set(target_tree.item(target_iid, "tags"))
                tags.add("drop_target")
                target_tree.item(target_iid, tags=tuple(tags))
            except tk.TclError:
                pass

    def on_sidebar_drag_end(self, event):
        source_iid = self.sidebar_drag_start_iid
        target_iid, target_row = self.identify_sidebar_drop_row(event)
        pointer_inside_sidebar = self.pointer_is_over_widget(self.sidebar_listbox, event)
        moved = self.sidebar_drag_has_moved
        self.sidebar_drag_start_iid = None
        self.sidebar_drag_has_moved = False
        self.clear_sidebar_drop_target_tags()
        if not source_iid or not moved or not pointer_inside_sidebar:
            return
        source_row = self.sidebar_iid_to_row.get(source_iid)
        if not source_row:
            return

        changed = False
        self.snapshot_undo()
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
        elif self.undo_stack:
            self.undo_stack.pop()

    def clear_sidebar_drop_target_tags(self):
        for tree_name in ("inbox_listbox", "sidebar_listbox"):
            tree = getattr(self, tree_name, None)
            if tree is None:
                continue
            stack = list(tree.get_children(""))
            while stack:
                iid = stack.pop()
                stack.extend(tree.get_children(iid))
                try:
                    tags = tuple(tag for tag in tree.item(iid, "tags") if tag != "drop_target")
                    tree.item(iid, tags=tags)
                except tk.TclError:
                    pass

    def move_sidebar_list_into_folder(self, list_id, folder_id):
        list_entry = next((entry for entry in self.lists if entry.get("id") == list_id), None)
        if not list_entry or self.is_inbox_list(list_entry) or not any(folder.get("id") == folder_id for folder in self.folders):
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
        if not source or not target or self.is_inbox_list(source):
            return False
        self.lists = [entry for entry in self.lists if entry.get("id") != source_id]
        target_index = next((idx for idx, entry in enumerate(self.lists) if entry.get("id") == target_id), len(self.lists))
        source["folder_id"] = target.get("folder_id")
        insert_index = target_index if place == "before" else target_index + 1
        self.lists.insert(insert_index, source)
        return True

    def move_sidebar_list_to_top_level_end(self, list_id):
        source = next((entry for entry in self.lists if entry.get("id") == list_id), None)
        if not source or self.is_inbox_list(source):
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
        self.snapshot_undo()
        self.sync_current_list_reference()
        target_folder_id = self.active_folder_id if self.view_mode == "folder" else None
        new_entry = self.new_list_object(title, [], folder_id=target_folder_id)
        self.lists.append(new_entry)
        self.set_active_list(new_entry["id"])
        self.save_items()
        return "break"

    def delete_current_list(self, event=None):
        if not self.require_list_view():
            return "break"
        if self.is_inbox_list(self.current_list()):
            messagebox.showinfo("Eingang", "Der fest integrierte Eingang kann nicht gelöscht werden.")
            return "break"
        if len(self.lists) <= 1:
            messagebox.showinfo("Liste löschen", "Die letzte Liste kann nicht gelöscht werden.")
            return "break"
        current = self.current_list()
        title = current.get("title", "Diese Liste")
        if not messagebox.askyesno("Liste löschen", f"Liste '{title}' wirklich löschen?"):
            return "break"
        self.snapshot_undo()
        delete_id = current.get("id")
        self.lists = [entry for entry in self.lists if entry.get("id") != delete_id]
        next_id = self.lists[0]["id"]
        self.active_list_id = None
        self.set_active_list(next_id)
        self.save_items()
        return "break"

    def validate_backup_schema(self, data, *, portable=False):
        """Prüft ein Backup strikt, ohne den aktuellen App-Zustand zu ändern.

        Alte reine JSON-Aufgabenlisten bleiben für die Migration zulässig. Ein
        portables .glidebackup muss einem ausdrücklich unterstützten Glide-
        Datenformat entsprechen; Format 4 wird verlustfrei auf Format 5 gehoben.
        """
        if isinstance(data, list):
            if portable:
                raise ValueError("Ein Komplettbackup benötigt das aktuelle Glide-Schema.")
            raw_folders = []
            raw_lists = [{"items": data}]
        elif isinstance(data, dict):
            version = data.get("version")
            if portable:
                if (
                    data.get("app") != APP_NAME
                    or not isinstance(version, int)
                    or not self.MIN_PORTABLE_BACKUP_SCHEMA_VERSION <= version <= self.DATA_SCHEMA_VERSION
                ):
                    raise ValueError("Das Komplettbackup stammt nicht aus einer unterstützten Glide-Version.")
            elif version is not None and (
                not isinstance(version, int) or version < 1 or version > self.DATA_SCHEMA_VERSION
            ):
                raise ValueError(f"Die Datenformat-Version {version!r} wird nicht unterstützt.")
            raw_folders = data.get("folders", [])
            raw_lists = data.get("lists")
            if not isinstance(raw_folders, list) or not isinstance(raw_lists, list):
                raise ValueError("Das Backup enthält keine gültigen Ordner- und Listenfelder.")
        else:
            raise ValueError("Die ausgewählte Datei ist kein Glide-Backup.")

        folder_ids = set()
        for folder in raw_folders:
            if not isinstance(folder, dict):
                raise ValueError("Ein Ordner im Backup ist ungültig.")
            folder_id = folder.get("id")
            if portable and (not isinstance(folder_id, str) or not folder_id):
                raise ValueError("Ein Ordner im Komplettbackup besitzt keine ID.")
            if isinstance(folder_id, str) and folder_id:
                if folder_id in folder_ids:
                    raise ValueError("Das Backup enthält doppelte Ordner-IDs.")
                folder_ids.add(folder_id)

        list_ids = set()
        item_ids = set()
        referenced_storages = set()
        item_count = 0
        for list_entry in raw_lists:
            if not isinstance(list_entry, dict):
                raise ValueError("Eine Liste im Backup ist ungültig.")
            list_id = list_entry.get("id")
            if portable and (not isinstance(list_id, str) or not list_id):
                raise ValueError("Eine Liste im Komplettbackup besitzt keine ID.")
            if isinstance(list_id, str) and list_id:
                if list_id in list_ids:
                    raise ValueError("Das Backup enthält doppelte Listen-IDs.")
                list_ids.add(list_id)
            folder_id = list_entry.get("folder_id")
            if folder_id is not None and folder_id not in folder_ids:
                raise ValueError("Eine Liste verweist auf einen unbekannten Ordner.")
            raw_items = list_entry.get("items", [])
            if not isinstance(raw_items, list):
                raise ValueError("Das Aufgabenfeld einer Liste ist ungültig.")
            stack = [(entry, 0) for entry in reversed(raw_items)]
            while stack:
                item, depth = stack.pop()
                item_count += 1
                if item_count > self.MAX_BACKUP_ITEMS:
                    raise ValueError("Das Backup enthält zu viele Aufgaben.")
                if depth > self.MAX_ITEM_DEPTH:
                    raise ValueError("Das Backup ist zu tief verschachtelt.")
                if isinstance(item, str) and not portable:
                    continue
                if not isinstance(item, dict):
                    raise ValueError("Ein Aufgabenpunkt im Backup ist ungültig.")
                item_id = item.get("id")
                if portable and (not isinstance(item_id, str) or not item_id):
                    raise ValueError("Ein Aufgabenpunkt im Komplettbackup besitzt keine ID.")
                if isinstance(item_id, str) and item_id:
                    if item_id in item_ids:
                        raise ValueError("Das Backup enthält doppelte Aufgaben-IDs.")
                    item_ids.add(item_id)
                if portable and (not isinstance(item.get("text"), str) or not item.get("text").strip()):
                    raise ValueError("Ein Aufgabenpunkt im Komplettbackup besitzt keinen Text.")
                item_color = item.get("color")
                if portable and item_color is not None and item_color not in self.ITEM_COLOR_KEYS:
                    raise ValueError("Ein Aufgabenpunkt im Komplettbackup besitzt eine ungültige Farbe.")
                children = item.get("children", [])
                if not isinstance(children, list):
                    raise ValueError("Die Unterpunkte einer Aufgabe sind ungültig.")
                stack.extend((child, depth + 1) for child in reversed(children))
                attachments = item.get("attachments", [])
                if not isinstance(attachments, list):
                    raise ValueError("Die Anhänge einer Aufgabe sind ungültig.")
                for attachment in attachments:
                    if not isinstance(attachment, dict):
                        raise ValueError("Ein Anhang im Backup ist ungültig.")
                    storage = self.validate_attachment_storage(attachment.get("storage"))
                    referenced_storages.add(storage)

        if isinstance(data, dict):
            active_list_id = data.get("active_list_id")
            active_folder_id = data.get("active_folder_id")
            if active_list_id is not None and active_list_id not in list_ids:
                raise ValueError("Das Backup verweist auf eine unbekannte aktive Liste.")
            if active_folder_id is not None and active_folder_id not in folder_ids:
                raise ValueError("Das Backup verweist auf einen unbekannten aktiven Ordner.")
        return referenced_storages

    def normalize_lists_data(self, data):
        self.folders = []
        if isinstance(data, dict):
            if not isinstance(data.get("lists"), list):
                raise ValueError("Die Datei enthält kein gültiges Listen-Schema.")
            version = data.get("version")
            if version is not None and (not isinstance(version, int) or version < 1 or version > self.DATA_SCHEMA_VERSION):
                raise ValueError(f"Die Datenformat-Version {version!r} wird nicht unterstützt.")
            if not isinstance(data.get("folders", []), list):
                raise ValueError("Das Feld 'folders' muss eine Liste sein.")
            folder_ids = set()
            raw_folders = data.get("folders", [])
            for folder in raw_folders:
                if not isinstance(folder, dict):
                    continue
                folder_id = folder.get("id") if isinstance(folder.get("id"), str) and folder.get("id") else None
                while not folder_id or folder_id in folder_ids:
                    folder_id = uuid.uuid4().hex
                title = str(folder.get("title") or "Ordner").strip() or "Ordner"
                color = folder.get("color") if folder.get("color") in self.LIST_COLOR_KEYS else None
                note = str(folder.get("note") or "")
                self.folders.append(self.new_folder_object(title, folder_id, color, note))
                folder_ids.add(folder_id)

            lists = []
            list_ids = set()
            item_ids = set()
            item_counter = [0]
            for entry in data.get("lists", []):
                if not isinstance(entry, dict):
                    continue
                title = str(entry.get("title") or "Meine Liste").strip() or "Meine Liste"
                list_id = entry.get("id") if isinstance(entry.get("id"), str) and entry.get("id") else None
                while not list_id or list_id in list_ids:
                    list_id = uuid.uuid4().hex
                list_ids.add(list_id)
                folder_id = entry.get("folder_id") if entry.get("folder_id") in folder_ids else None
                items = self.normalize_items(entry.get("items", []), item_ids, 0, item_counter)
                color = entry.get("color") if entry.get("color") in self.LIST_COLOR_KEYS else None
                note = str(entry.get("note") or "")
                system_role = "inbox" if entry.get("system_role") == "inbox" else None
                lists.append(self.new_list_object(title, items, list_id, folder_id, color, note, system_role))
            active_id = data.get("active_list_id") if isinstance(data.get("active_list_id"), str) else None
            return lists, active_id

        # Abwärtskompatibilität: alte Speicherdatei war direkt eine Item-Liste.
        if not isinstance(data, list):
            raise ValueError("Die Datei ist weder ein Glide-Dokument noch eine alte Aufgabenliste.")
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

        self.note_preview_label = self.register_theme_widget(
            tk.Label(
                title_block,
                text="Seitennotiz hinzufügen …",
                font=("TkDefaultFont", 9, "italic"),
                bg=self.theme["bg"],
                fg=self.theme["muted"],
                anchor="w",
                justify="left",
                cursor="hand2",
            ),
            "bg",
            "muted",
        )
        self.note_preview_label.pack(anchor="w", fill="x")
        self.note_preview_label.bind("<Button-1>", self.edit_page_note)

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
            columns=("due",),
            displaycolumns=("due",),
            show="tree",
            selectmode="extended",
            style="App.Treeview",
        )
        self.tree.pack(side="left", fill="both", expand=True, padx=(14, 14), pady=14)
        self.tree.heading("#0", text="")
        self.tree.column("#0", anchor="w", stretch=True, width=360, minwidth=180)
        self.tree.column(
            "due",
            anchor="e",
            stretch=False,
            width=self.DUE_COLUMN_WIDTH,
            minwidth=self.DUE_COLUMN_WIDTH,
        )

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
        self.tree.bind("<Double-Button-1>", self.activate_tree_row)
        self.tree.bind("<Return>", self.activate_tree_row)
        self.tree.bind("<Button-3>", self.show_item_context_menu)
        self.tree.bind("<Button-2>", self.show_item_context_menu)
        self.tree.bind("<Control-Button-1>", self.show_item_context_menu)
        self.tree.bind("<Configure>", self.sync_task_tree_columns, add="+")
        self.tree.bind("<Tab>", self.toggle_indent_selected)
        self.tree.bind("<space>", self.toggle_done)
        self.bind_mousewheel(self.tree)

        self.hint_label = self.register_theme_widget(
            tk.Label(
                self.content_frame,
                text="Drag & Drop: Reihenfolge ändern · Shift + Drag: Unterpunkt · Shift + Klick: Bereich auswählen · Strg+A: alle auswählen · Tab: ein-/ausrücken · Strg+F: Suche · Rechtsklick: Details, Wichtigkeit, Fälligkeit und Farbe · Strg+T: Fälligkeit · Strg+Z: Rückgängig · Strg+C/V: Kopieren/Einfügen · F2: Bearbeiten",
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
            for sidebar_tree_name in ("inbox_listbox", "sidebar_listbox"):
                sidebar_tree = getattr(self, sidebar_tree_name, None)
                if sidebar_tree is None:
                    continue
                sidebar_tree.tag_configure("folder", foreground=self.theme["muted"])
                sidebar_tree.tag_configure("list", foreground=self.theme["text"])
                sidebar_tree.tag_configure(
                    "inbox",
                    foreground=self.theme["text"],
                    font=self.SIDEBAR_SECTION_FONT,
                )
                sidebar_tree.tag_configure("drop_target", background=self.theme["input_border"])
                for color_key in self.LIST_COLOR_KEYS:
                    sidebar_tree.tag_configure(f"listcolor_{color_key}", foreground=self.theme[color_key])

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
            self.tree.tag_configure("folder_list", foreground=self.theme["text"])
            self.tree.tag_configure("drop_target", background=self.theme["input_border"])
            for color_key in self.LIST_COLOR_KEYS:
                self.tree.tag_configure(f"listcolor_{color_key}", foreground=self.theme[color_key])
            for color_key in self.ITEM_COLOR_KEYS:
                self.tree.tag_configure(f"itemcolor_{color_key}", foreground=self.theme[color_key])

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

        for menu in getattr(self, "menus", []):
            try:
                menu.configure(
                    bg=self.theme["card"],
                    fg=self.theme["text"],
                    activebackground=self.theme["selection"],
                    activeforeground="#FFFFFF",
                    selectcolor=self.theme["accent"],
                    bd=0,
                    relief="flat",
                )
            except tk.TclError:
                pass
        for button in getattr(self, "custom_menu_buttons", []):
            try:
                button.configure(
                    bg=self.theme["bg"],
                    fg=self.theme["text"],
                    activebackground=self.theme["input"],
                    activeforeground=self.theme["text"],
                )
            except tk.TclError:
                pass

        self.refresh_tree()
        self._schedule_windows_chrome_theme(self.root)

    def _on_windows_window_map(self, event=None):
        if event is None or event.widget is self.root:
            self._schedule_windows_chrome_theme(self.root)

    def _schedule_windows_chrome_theme(self, window=None, attempt=0):
        """Wendet DWM-Farben erst nach dem Mapping mit begrenzten Retries an."""
        if os.name != "nt" or attempt >= len(self.WINDOWS_CHROME_RETRY_DELAYS_MS):
            return
        target = window or self.root

        def apply_or_retry():
            try:
                if not target.winfo_exists():
                    return
                if target.winfo_ismapped() and self._apply_windows_chrome_theme(target):
                    return
            except tk.TclError:
                return
            self._schedule_windows_chrome_theme(target, attempt + 1)

        try:
            after_id = target.after(self.WINDOWS_CHROME_RETRY_DELAYS_MS[attempt], apply_or_retry)
            self._after_ids.append(after_id)
        except tk.TclError:
            pass

    def _apply_windows_chrome_theme(self, window=None):
        """Färbt unter Windows den nativen Fensterrahmen passend zum App-Theme."""
        if os.name != "nt":
            return False
        target = window or self.root
        try:
            target.update_idletasks()
            user32 = ctypes.WinDLL("user32", use_last_error=True)
            dwmapi = ctypes.WinDLL("dwmapi", use_last_error=True)
            user32.GetParent.argtypes = [ctypes.c_void_p]
            user32.GetParent.restype = ctypes.c_void_p
            inner_hwnd = ctypes.c_void_p(target.winfo_id())
            hwnd = user32.GetParent(inner_hwnd) or inner_hwnd.value
            dark_value = ctypes.c_int(1 if self.theme_name == "dark" else 0)
            dwmapi.DwmSetWindowAttribute.argtypes = [
                ctypes.c_void_p,
                ctypes.c_uint,
                ctypes.c_void_p,
                ctypes.c_uint,
            ]
            dwmapi.DwmSetWindowAttribute.restype = ctypes.c_long
            user32.RedrawWindow.argtypes = [
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.c_uint,
            ]
            user32.RedrawWindow.restype = ctypes.c_int
            applied = False
            for attribute in (20, 19):
                result = dwmapi.DwmSetWindowAttribute(
                    ctypes.c_void_p(hwnd),
                    attribute,
                    ctypes.byref(dark_value),
                    ctypes.sizeof(dark_value),
                )
                if result == 0:
                    applied = True
                    break
            # Rahmen + Titelzeile neu zeichnen, ohne das Fenster flackern zu lassen.
            user32.RedrawWindow(
                ctypes.c_void_p(hwnd),
                None,
                None,
                0x0001 | 0x0080 | 0x0400,
            )
            return applied
        except Exception:
            # Auf älteren Windows-Versionen bleibt lediglich die native Titelleiste hell.
            return False

    def toggle_theme(self):
        self.theme_name = "dark" if self.theme_name == "light" else "light"
        self.save_theme_setting()
        self.apply_theme()

    # -----------------------------
    # Titel / Fenster
    # -----------------------------
    def edit_title(self):
        if self.view_mode == "folder" and self.active_folder_id:
            return self.edit_folder_title(self.active_folder_id)
        if self.is_inbox_list(self.current_list()):
            messagebox.showinfo("Eingang", "Der fest integrierte Eingang behält seinen Namen.")
            return "break"
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
        if new_title == self.app_title:
            return

        self.snapshot_undo()
        self.app_title = new_title
        self.current_list()["title"] = new_title
        self.title_label.configure(text=self.app_title)
        self.update_window_title()
        self.update_sidebar_list()
        self.save_items()
        self.save_settings()

    def update_page_note_preview(self):
        if not hasattr(self, "note_preview_label"):
            return
        page = self.get_active_page()
        note = str(page.get("note") or "") if page else ""
        compact = " ".join(note.split())
        if compact:
            preview = compact if len(compact) <= 110 else compact[:107].rstrip() + "…"
        else:
            preview = "Seitennotiz hinzufügen …"
        self.note_preview_label.configure(text=preview)

    def edit_page_note(self, event=None):
        page = self.get_active_page()
        if not page:
            return "break"
        page_kind = "Ordnernotiz" if self.view_mode == "folder" else "Seitennotiz"
        value = self.themed_multiline_dialog(
            page_kind,
            "Freier Bereich für längere Informationen – zählt nicht als Listenpunkt.\n"
            "Speichern: Strg+Enter",
            initial=page.get("note", ""),
        )
        if value is None:
            return "break"
        if value != page.get("note", ""):
            self.snapshot_undo()
            page["note"] = value
            self.save_items()
            self.update_page_note_preview()
        return "break"

    def update_entry_mode(self):
        if not hasattr(self, "entry"):
            return
        new_placeholder = "Neue Liste in diesem Ordner" if self.view_mode == "folder" else "Listenpunkt eingeben"
        if self.entry_placeholder_active:
            self.entry.delete(0, tk.END)
            self.entry_placeholder_text = new_placeholder
            self.entry.insert(0, new_placeholder)
        else:
            self.entry_placeholder_text = new_placeholder
        if hasattr(self, "hint_label"):
            if self.view_mode == "folder":
                self.hint_label.configure(
                    text="Doppelklick oder Enter: Liste öffnen · Eingabefeld: neue Liste in diesem Ordner anlegen · "
                    "Listenpunkte können aus einer geöffneten Liste auf ein Ziel in der Seitenleiste gezogen werden"
                )
            else:
                self.hint_label.configure(
                    text="Drag & Drop: Reihenfolge ändern · Auf eine Seitenleisten-Liste ziehen: dorthin verschieben · "
                    "Shift + Drag: Unterpunkt · Shift + Klick: Bereich auswählen · Strg+A: alle auswählen · "
                    "Tab: ein-/ausrücken · Strg+F: Suche · Strg+Shift+F/Rechtsklick: Wichtigkeit · "
                    "Strg+T: Fälligkeit · Strg+M: Seitennotiz · Strg+Z: Rückgängig · F2: Details"
                )

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
        if getattr(self, "dirty", False):
            retry = messagebox.askyesnocancel(
                "Ungespeicherte Änderungen",
                "Die letzten Änderungen konnten noch nicht gespeichert werden.\n\n"
                "Jetzt erneut speichern?",
            )
            if retry is None:
                return
            if retry:
                if not self.save_items():
                    return
            elif not messagebox.askyesno(
                "Ohne Speichern schließen",
                "Glide wirklich schließen? Die ungespeicherten Änderungen gehen verloren.",
            ):
                return
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

    def sync_task_tree_columns(self, event=None):
        """Hält die feste Fälligkeitsspalte bei jeder Treeview-Breite sichtbar rechts."""
        if not hasattr(self, "tree"):
            return
        try:
            tree_width = int(getattr(event, "width", 0) or self.tree.winfo_width())
            text_width = max(
                180,
                tree_width - self.DUE_COLUMN_WIDTH - self.TASK_TREE_EDGE_PADDING,
            )
            self.tree.column("#0", width=text_width)
            self.tree.column(
                "due",
                width=self.DUE_COLUMN_WIDTH,
                minwidth=self.DUE_COLUMN_WIDTH,
            )
        except (TypeError, ValueError, tk.TclError):
            pass

    def cancel_pending_callbacks(self):
        if not hasattr(self, "root"):
            return
        self._destroy_item_context_menu()
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

    def new_item(
        self,
        text,
        done=False,
        children=None,
        item_id=None,
        importance=0,
        due=None,
        description="",
        attachments=None,
        color=None,
    ):
        return {
            "id": item_id or uuid.uuid4().hex,
            "text": str(text),
            "done": bool(done),
            "importance": self.clamp_importance(importance),
            "due": self.normalize_due(due),
            "description": str(description or ""),
            "attachments": self.normalize_attachments(attachments),
            "color": color if color in self.ITEM_COLOR_KEYS else None,
            "children": children if isinstance(children, list) else [],
        }

    @staticmethod
    def validate_attachment_storage(storage):
        """Erlaubt ausschließlich portable, flache Pfade unter attachments/."""
        if not isinstance(storage, str):
            raise ValueError("Ungültiger Anhangspfad.")
        storage = storage.strip()
        if not storage or "\\" in storage or "\x00" in storage:
            raise ValueError("Ungültiger Anhangspfad.")
        parts = storage.split("/")
        if len(parts) != 2 or parts[0] != "attachments":
            raise ValueError("Anhänge müssen direkt im Ordner attachments liegen.")
        filename = parts[1]
        if filename in ("", ".", "..") or filename.rstrip(" .") != filename:
            raise ValueError("Ungültiger Anhangsname.")
        if any(ord(char) < 32 or char in '<>:"/\\|?*' for char in filename):
            raise ValueError("Der Anhangsname enthält unzulässige Zeichen.")
        reserved = {"CON", "PRN", "AUX", "NUL"}
        reserved.update({f"COM{number}" for number in range(1, 10)})
        reserved.update({f"LPT{number}" for number in range(1, 10)})
        if filename.split(".", 1)[0].upper() in reserved:
            raise ValueError("Der Anhangsname ist unter Windows reserviert.")
        return storage

    def normalize_attachments(self, data):
        if not isinstance(data, list):
            return []
        normalized = []
        for entry in data:
            if not isinstance(entry, dict):
                continue
            storage = entry.get("storage")
            if not isinstance(storage, str):
                continue
            try:
                storage = self.validate_attachment_storage(storage)
            except ValueError:
                continue
            name = str(entry.get("name") or os.path.basename(storage)).strip() or "Anhang"
            try:
                size = max(0, int(entry.get("size", 0)))
            except (TypeError, ValueError):
                size = 0
            normalized.append(
                {
                    "id": entry.get("id") if isinstance(entry.get("id"), str) and entry.get("id") else uuid.uuid4().hex,
                    "name": name,
                    "storage": storage,
                    "size": size,
                    "mime": str(entry.get("mime") or "application/octet-stream"),
                    "added_at": str(entry.get("added_at") or ""),
                }
            )
        return normalized

    def resolve_attachment_path(self, attachment):
        storage = attachment.get("storage") if isinstance(attachment, dict) else None
        if not isinstance(storage, str) or not storage:
            return None
        try:
            storage = self.validate_attachment_storage(storage)
        except ValueError:
            return None
        attachments_root = os.path.normcase(os.path.realpath(ATTACHMENTS_DIR))
        candidate = os.path.normcase(
            os.path.realpath(os.path.join(BASE_DIR, storage.replace("/", os.sep)))
        )
        try:
            if os.path.commonpath([candidate, attachments_root]) != attachments_root:
                return None
        except ValueError:
            return None
        return candidate

    def store_attachment(self, source_path):
        if not source_path or not os.path.isfile(source_path):
            raise OSError("Die ausgewählte Datei ist nicht mehr vorhanden.")
        original_name = os.path.basename(source_path)
        stem, extension = os.path.splitext(original_name)
        safe_stem = re.sub(r"[^\w .()-]+", "_", stem, flags=re.UNICODE).strip(" .")[:90] or "datei"
        safe_extension = re.sub(r"[^A-Za-z0-9.]", "", extension)[:16]
        attachment_id = uuid.uuid4().hex
        stored_name = f"{attachment_id}_{safe_stem}{safe_extension}"
        destination = os.path.join(ATTACHMENTS_DIR, stored_name)
        shutil.copy2(source_path, destination)
        mime, _encoding = mimetypes.guess_type(original_name)
        return {
            "id": attachment_id,
            "name": original_name,
            "storage": os.path.relpath(destination, BASE_DIR).replace("\\", "/"),
            "size": os.path.getsize(destination),
            "mime": mime or "application/octet-stream",
            "added_at": datetime.now().isoformat(timespec="seconds"),
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

    def normalize_items(self, data, seen_ids=None, depth=0, counter=None):
        if not isinstance(data, list):
            return []
        if depth > self.MAX_ITEM_DEPTH:
            raise ValueError("Die Aufgabenstruktur ist zu tief verschachtelt.")
        if seen_ids is None:
            seen_ids = set()
        if counter is None:
            counter = [0]

        normalized = []
        for entry in data:
            counter[0] += 1
            if counter[0] > self.MAX_BACKUP_ITEMS:
                raise ValueError("Die Datei enthält zu viele Aufgaben.")
            if isinstance(entry, str):
                item_id = uuid.uuid4().hex
                seen_ids.add(item_id)
                normalized.append(self.new_item(entry, False, item_id=item_id))
                continue

            if isinstance(entry, dict):
                text = str(entry.get("text", "")).strip()
                if not text:
                    continue
                item_id = entry.get("id") if isinstance(entry.get("id"), str) and entry.get("id") else None
                while not item_id or item_id in seen_ids:
                    item_id = uuid.uuid4().hex
                seen_ids.add(item_id)
                children = self.normalize_items(entry.get("children", []), seen_ids, depth + 1, counter)
                importance = entry.get("importance", entry.get("priority", 0))
                due = entry.get("due")
                description = str(entry.get("description") or "")
                attachments = self.normalize_attachments(entry.get("attachments", []))
                color = entry.get("color") if entry.get("color") in self.ITEM_COLOR_KEYS else None
                normalized.append(
                    self.new_item(
                        text,
                        entry.get("done", False),
                        children,
                        item_id,
                        importance,
                        due,
                        description,
                        attachments,
                        color,
                    )
                )
        return normalized

    def load_items(self):
        if not os.path.exists(SAVE_FILE):
            self.folders = []
            default_list = self.new_list_object(self.app_title, [])
            self.lists = [default_list]
            self.ensure_inbox_list()
            self.active_list_id = default_list["id"]
            self.active_folder_id = None
            self.view_mode = "list"
            self.items = default_list["items"]
            self.update_sidebar_list()
            self.refresh_tree()
            self.save_items()
            return
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            self.lists, active_id_from_file = self.normalize_lists_data(data)
            if not self.lists:
                self.lists = [self.new_list_object(self.app_title, [])]
            self.ensure_inbox_list()
            inbox_repaired = bool(getattr(self, "_last_inbox_repair", False))
            requested_folder_id = self.active_folder_id
            if not requested_folder_id and isinstance(data, dict):
                saved_folder = data.get("active_folder_id")
                requested_folder_id = saved_folder if isinstance(saved_folder, str) else None
            preferred_active_id = self.active_list_id or active_id_from_file
            if preferred_active_id not in [entry.get("id") for entry in self.lists]:
                existing_ids = [entry.get("id") for entry in self.lists]
                fallback = next((entry.get("id") for entry in self.lists if not self.is_inbox_list(entry)), self.lists[0]["id"])
                preferred_active_id = active_id_from_file if active_id_from_file in existing_ids else fallback
            self.active_list_id = None
            self.active_folder_id = None
            self.view_mode = "list"
            self.set_active_list(preferred_active_id, refresh=False)
            if requested_folder_id and self.get_folder(requested_folder_id):
                self.set_active_folder(requested_folder_id, refresh=False)
            self.update_sidebar_list()
            self.refresh_tree()
            if inbox_repaired:
                self.save_items()
        except (json.JSONDecodeError, ValueError, RecursionError, tk.TclError) as e:
            messagebox.showerror("Fehler", f"Die Speicherdatei ist beschädigt oder ungültig:\n{e}")
            self.folders = []
            default_list = self.new_list_object(self.app_title, [])
            self.lists = [default_list]
            self.ensure_inbox_list()
            self.active_list_id = default_list["id"]
            self.active_folder_id = None
            self.view_mode = "list"
            self.items = default_list["items"]
            self.update_sidebar_list()
            self.refresh_tree()
        except OSError as e:
            messagebox.showerror("Fehler", f"Die Speicherdatei konnte nicht gelesen werden:\n{e}")
            self.folders = []
            default_list = self.new_list_object(self.app_title, [])
            self.lists = [default_list]
            self.ensure_inbox_list()
            self.active_list_id = default_list["id"]
            self.active_folder_id = None
            self.view_mode = "list"
            self.items = default_list["items"]
            self.update_sidebar_list()
            self.refresh_tree()

    def data_payload(self, lists=None, folders=None, active_list_id=None, active_folder_id=None):
        return {
            "version": self.DATA_SCHEMA_VERSION,
            "active_list_id": self.active_list_id if active_list_id is None else active_list_id,
            "active_folder_id": (
                self.active_folder_id if self.view_mode == "folder" else None
            ) if active_folder_id is None else active_folder_id,
            "folders": self.folders if folders is None else folders,
            "lists": self.lists if lists is None else lists,
        }

    @staticmethod
    def write_json_atomic(path, payload):
        """Schreibt JSON vollständig und ersetzt die Zieldatei erst am Ende."""
        directory = os.path.dirname(os.path.abspath(path))
        os.makedirs(directory, exist_ok=True)
        fd, temp_file = tempfile.mkstemp(prefix=".glide-json-", suffix=".tmp", dir=directory)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as file:
                json.dump(payload, file, ensure_ascii=False, indent=4)
                file.flush()
                os.fsync(file.fileno())
            os.replace(temp_file, path)
            temp_file = None
        finally:
            if temp_file:
                try:
                    os.remove(temp_file)
                except OSError:
                    pass

    def save_items(self, *, show_error=True):
        self.dirty = True
        backup_warning = None
        try:
            self.sync_current_list_reference()
            if os.path.exists(SAVE_FILE):
                try:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    backup_file = os.path.join(BACKUP_DIR, f"liste_backup_{timestamp}.json")
                    shutil.copy2(SAVE_FILE, backup_file)
                    self.prune_backups()
                except OSError as exc:
                    # Ein defekter Backup-Ordner darf das Speichern der aktuellen
                    # Nutzdaten nicht verhindern. Die Warnung bleibt sichtbar.
                    backup_warning = str(exc)

            self.write_json_atomic(SAVE_FILE, self.data_payload())
            self.dirty = False
        except Exception as e:
            if show_error:
                messagebox.showerror("Fehler beim Speichern", str(e))
            return False

        try:
            self.update_sidebar_list()
        except tk.TclError:
            pass
        if backup_warning and show_error:
            messagebox.showwarning(
                "Sicherung nicht möglich",
                "Die aktuellen Daten wurden gespeichert, aber die zusätzliche automatische Sicherung "
                f"konnte nicht erstellt werden:\n{backup_warning}",
            )
        return True

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
        attachment_names = " ".join(
            str(attachment.get("name", ""))
            for attachment in item.get("attachments", [])
            if isinstance(attachment, dict)
        )
        haystack = " ".join([
            str(item.get("text", "")),
            str(item.get("description", "")),
            attachment_names,
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

    def handle_control_n(self, event=None):
        """Unterscheidet Strg+N und Strg+Shift+N anhand der echten Shift-Taste.

        Dadurch löst aktiviertes CapsLock nicht versehentlich „Neue Liste“ aus.
        """
        if event is not None and bool(event.state & 0x0001):
            return self.create_new_list(event)
        return self.focus_entry(event)

    def handle_control_f(self, event=None):
        """Unterscheidet Suche und Wichtigkeit ohne CapsLock-Nebenwirkung."""
        if event is not None and bool(event.state & 0x0001):
            return self.cycle_importance_selected(event)
        return self.focus_search(event)

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
        if self.view_mode == "folder" and self.active_folder_id:
            folder_lists = self.get_folder_lists(self.active_folder_id)
            total = done = overdue = 0
            for entry in folder_lists:
                list_total, list_done, list_overdue = self.compute_stats(entry.get("items", []))
                total += list_total
                done += list_done
                overdue += list_overdue
            list_word = "Liste" if len(folder_lists) == 1 else "Listen"
            text = f"{len(folder_lists)} {list_word} · {total} Punkte"
            if total:
                text += f" · {total - done} offen"
            if overdue:
                text += f" · {overdue} überfällig"
            try:
                self.stats_label.configure(text=text)
            except tk.TclError:
                pass
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

        if self.view_mode == "folder":
            self.refresh_folder_overview(selected_id=selected_id)
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

    def refresh_folder_overview(self, selected_id=None):
        """Zeigt die im ausgewählten Ordner enthaltenen Listen im Hauptbereich."""
        if not hasattr(self, "tree"):
            return
        self.update_stats_label()
        current_selection = selected_id or self.tree.focus()
        for row_id in self.tree.get_children(""):
            self.tree.delete(row_id)

        folder_lists = self.get_folder_lists(self.active_folder_id)
        query = self.current_search_query()
        if query:
            filtered_lists = []
            for entry in folder_lists:
                page_text = f"{entry.get('title', '')} {entry.get('note', '')}".lower()
                task_match = any(self.item_text_matches_query(item, query) for item in self.walk_items(entry.get("items", [])))
                if query in page_text or task_match:
                    filtered_lists.append(entry)
            folder_lists = filtered_lists
        if not folder_lists:
            empty_text = (
                "Keine Listen oder Inhalte passen zur aktuellen Suche."
                if query
                else "Noch keine Listen in diesem Ordner. Oben kann direkt eine neue Liste angelegt werden."
            )
            self.tree.insert(
                "",
                "end",
                iid=self.EMPTY_ROW_ID,
                text=empty_text,
                tags=("empty",),
            )
            self.schedule_scrollbar_refresh()
            return

        for entry in folder_lists:
            total, done, overdue = self.compute_stats(entry.get("items", []))
            open_count = total - done
            detail = f"{total} Punkte · {open_count} offen"
            if total:
                detail += f" · {round(done / total * 100)} % erledigt"
            if overdue:
                detail += f" · {overdue} überfällig"
            note_marker = "  📝" if str(entry.get("note") or "").strip() else ""
            row_text = f"▸  {entry.get('title', 'Liste')}   —   {detail}{note_marker}"
            iid = f"folder-list:{entry.get('id')}"
            color_key = entry.get("color") if entry.get("color") in self.LIST_COLOR_KEYS else None
            tags = (f"listcolor_{color_key}",) if color_key else ("folder_list",)
            self.tree.insert("", "end", iid=iid, text=row_text, tags=tags)

        if current_selection and self.tree.exists(current_selection):
            self.tree.selection_set(current_selection)
            self.tree.focus(current_selection)
        self.schedule_scrollbar_refresh()

    def get_selected_folder_list_id(self, event=None):
        row_id = ""
        if event is not None and self.is_mouse_event(event):
            row_id = self.tree.identify_row(event.y)
        if not row_id:
            row_id = self.tree.focus()
        prefix = "folder-list:"
        if row_id and row_id.startswith(prefix):
            return row_id[len(prefix):]
        return None

    def activate_tree_row(self, event=None):
        if self.view_mode == "folder":
            list_id = self.get_selected_folder_list_id(event)
            if list_id:
                self.set_active_list(list_id)
            return "break"
        return self.toggle_done(event)

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
            due_value = f"\U0001F4C5 {due_text}" if due_text else ""
            description_suffix = "   📝" if str(item.get("description") or "").strip() else ""
            attachment_count = len(item.get("attachments", []))
            attachment_suffix = f"   📎 {attachment_count}" if attachment_count else ""
            row_text = (
                f"{number_text}. {flag_prefix}{done_prefix}{item.get('text', '')}"
                f"{description_suffix}{attachment_suffix}"
            )
            item_id = item.get("id") or uuid.uuid4().hex
            item["id"] = item_id
            has_children = bool(item.get("children"))
            should_open = item_id in self.expanded_ids or parent_id == "" or bool(query)
            color_key = item.get("color") if item.get("color") in self.ITEM_COLOR_KEYS else None
            item["color"] = color_key
            if color_key:
                # Eine bewusst gewählte Aufgabenfarbe hat Vorrang. Status,
                # Fälligkeit und Wichtigkeit bleiben über Marker/Text sichtbar.
                tag = f"itemcolor_{color_key}"
            elif item.get("done"):
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
                values=(due_value,),
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
        if self.active_list_id and self.lists:
            self.sync_current_list_reference()
        self.undo_stack.append(
            {
                "lists": copy.deepcopy(self.lists),
                "folders": copy.deepcopy(self.folders),
                "active_list_id": self.active_list_id,
                "active_folder_id": self.active_folder_id if self.view_mode == "folder" else None,
            }
        )
        if len(self.undo_stack) > 20:
            self.undo_stack.pop(0)

    def undo_last_change(self, event=None):
        if event is not None and isinstance(self.root.focus_get(), (tk.Entry, tk.Text, ttk.Entry)):
            # In Textfeldern bleibt echtes Strg+Z eine lokale Texteingabe-Aktion.
            return None
        if not self.undo_stack:
            messagebox.showinfo("Rückgängig", "Es gibt keine Änderung zum Rückgängigmachen.")
            return "break"
        snapshot = self.undo_stack.pop()
        self.lists = copy.deepcopy(snapshot.get("lists", []))
        self.folders = copy.deepcopy(snapshot.get("folders", []))
        self.ensure_inbox_list()
        desired_list_id = snapshot.get("active_list_id")
        if desired_list_id not in [entry.get("id") for entry in self.lists]:
            desired_list_id = self.lists[0].get("id")
        desired_folder_id = snapshot.get("active_folder_id")
        self.active_list_id = None
        self.active_folder_id = None
        self.view_mode = "list"
        self.set_active_list(desired_list_id, refresh=False)
        if desired_folder_id and self.get_folder(desired_folder_id):
            self.set_active_folder(desired_folder_id, refresh=False)
        self.save_items()
        self.update_sidebar_list()
        self.refresh_tree()
        return "break"

    def format_item_lines(self, item, number_prefix, level=0):
        number_text = ".".join(str(part) for part in number_prefix)
        indent = "   " * level
        flag_prefix = self.IMPORTANCE_MARKERS.get(self.clamp_importance(item.get("importance", 0)), "")
        done_prefix = "✓ " if item.get("done") else ""
        lines = [f"{indent}{number_text}. {flag_prefix}{done_prefix}{item.get('text', '')}"]
        description = str(item.get("description") or "").strip()
        if description:
            lines.extend(f"{indent}   Beschreibung: {line}" for line in description.splitlines())
        for attachment in item.get("attachments", []):
            lines.append(f"{indent}   Anhang: {attachment.get('name', 'Datei')}")
        for index, child in enumerate(item.get("children", []), start=1):
            lines.extend(self.format_item_lines(child, number_prefix + [index], level + 1))
        return lines

    def copy_selected_to_clipboard(self, event=None):
        if self.root.focus_get() in (getattr(self, "entry", None), getattr(self, "search_entry", None)):
            return None
        if not self.require_list_view():
            return "break"
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
        if not self.require_list_view():
            return "break"

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
            noun = "Listentitel" if self.view_mode == "folder" else "Punkt"
            messagebox.showwarning("Hinweis", f"Bitte einen {noun} eingeben.")
            return
        if self.view_mode == "folder":
            self.snapshot_undo()
            new_entry = self.new_list_object(text, [], folder_id=self.active_folder_id)
            self.lists.append(new_entry)
            self.entry.delete(0, tk.END)
            self.entry_placeholder_active = False
            self.entry.configure(fg=self.theme["text"])
            self.save_items()
            self.refresh_folder_overview(selected_id=f"folder-list:{new_entry['id']}")
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
            return None
        if not self.require_list_view():
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
        if not self.require_list_view():
            return
        if messagebox.askyesno("Löschen", "Alle Punkte wirklich löschen?"):
            self.snapshot_undo()
            self.items.clear()
            self.save_items()
            self.refresh_tree()

    def edit_item(self):
        if not self.require_list_view():
            return
        item_id = self.get_selected_item_id()
        if not item_id:
            return
        found = self.find_item(item_id)
        if not found:
            return
        item, _siblings, _index, _parent_item = found
        details = self.themed_item_details_dialog(item)
        if details is None:
            return

        changed = any(
            details.get(key) != item.get(key, [] if key == "attachments" else "")
            for key in ("text", "description", "attachments")
        )
        if changed:
            self.snapshot_undo()
            item["text"] = details["text"]
            item["description"] = details["description"]
            item["attachments"] = details["attachments"]
            self.save_items()
            self.refresh_tree(selected_id=item_id)

    def _new_themed_popup_menu(self, parent=None):
        return tk.Menu(
            parent or self.root,
            tearoff=0,
            bg=self.theme["card"],
            fg=self.theme["text"],
            activebackground=self.theme["selection"],
            activeforeground="#FFFFFF",
            selectcolor=self.theme["accent"],
            bd=0,
            relief="flat",
        )

    def build_item_context_menu(self):
        """Erzeugt das Kontextmenü für die aktuelle Aufgaben-/Mehrfachauswahl."""
        item_ids = self.get_selected_item_ids()
        if not item_ids:
            return None
        selected_items = [self.find_item(item_id)[0] for item_id in item_ids if self.find_item(item_id)]
        if not selected_items:
            return None

        menu = self._new_themed_popup_menu()
        count_label = "Punktaktionen" if len(selected_items) == 1 else f"Aktionen für {len(selected_items)} Punkte"
        menu.add_command(label=count_label, state="disabled")
        menu.add_separator()
        menu.add_command(
            label=(
                "Bearbeiten (Titel, Beschreibung, Anhänge) …"
                if len(selected_items) == 1
                else "Bearbeiten … (nur einzeln)"
            ),
            command=self.edit_item,
            state="normal" if len(selected_items) == 1 else "disabled",
        )

        importance_menu = self._new_themed_popup_menu(menu)
        importance_values = {self.clamp_importance(item.get("importance", 0)) for item in selected_items}
        current_importance = next(iter(importance_values)) if len(importance_values) == 1 else None
        for value, label in ((0, "Keine"), (1, "Niedrig"), (2, "Mittel"), (3, "Hoch")):
            prefix = "✓ " if current_importance == value else "    "
            importance_menu.add_command(
                label=f"{prefix}{label}",
                command=lambda selected=value: self.set_importance_selected(selected),
            )
        menu.add_cascade(label="Wichtigkeit", menu=importance_menu)

        due_menu = self._new_themed_popup_menu(menu)
        due_values = {item.get("due") for item in selected_items}
        current_due = next(iter(due_values)) if len(due_values) == 1 else None
        today_iso = date.today().isoformat()
        tomorrow_iso = (date.today() + timedelta(days=1)).isoformat()
        due_menu.add_command(label="Datum auswählen …", command=self.set_due_date_selected)
        due_menu.add_separator()
        due_menu.add_command(
            label=f"{'✓ ' if current_due == today_iso else '    '}Heute",
            command=lambda: self.set_due_value_selected(today_iso),
        )
        due_menu.add_command(
            label=f"{'✓ ' if current_due == tomorrow_iso else '    '}Morgen",
            command=lambda: self.set_due_value_selected(tomorrow_iso),
        )
        due_menu.add_command(
            label=f"{'✓ ' if current_due is None and len(due_values) == 1 else '    '}Entfernen",
            command=lambda: self.set_due_value_selected(None),
        )
        menu.add_cascade(label="Fälligkeit", menu=due_menu)

        color_menu = self._new_themed_popup_menu(menu)
        color_values = {item.get("color") for item in selected_items}
        current_color = next(iter(color_values)) if len(color_values) == 1 else None
        for label, color_key in self.ITEM_COLOR_CHOICES:
            prefix = "✓ " if current_color == color_key else "    "
            color_menu.add_command(
                label=f"{prefix}{label}",
                foreground=self.theme[color_key],
                command=lambda selected=color_key: self.set_item_color_selected(selected),
            )
        color_menu.add_separator()
        color_menu.add_command(
            label=f"{'✓ ' if current_color is None and len(color_values) == 1 else '    '}Keine Farbe",
            command=lambda: self.set_item_color_selected(None),
        )
        menu.add_cascade(label="Aufgabenfarbe", menu=color_menu)
        menu.add_separator()
        menu.add_command(label="Entfernen", command=self.delete_item, foreground=self.theme["delete"])
        return menu

    def show_item_context_menu(self, event):
        if self.view_mode != "list":
            return "break"
        item_id = self.tree.identify_row(event.y)
        if not item_id or item_id == self.EMPTY_ROW_ID or not self.find_item(item_id):
            return "break"

        current_selection = set(self.get_selected_item_ids())
        if item_id not in current_selection:
            self.tree.selection_set(item_id)
        self.tree.focus(item_id)
        self.selection_anchor_id = item_id
        self._destroy_item_context_menu()
        menu = self.build_item_context_menu()
        if menu is None:
            return "break"
        self._item_context_menu = menu
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            try:
                menu.grab_release()
            except tk.TclError:
                pass
        return "break"

    def _destroy_item_context_menu(self):
        """Räumt ein zuvor ausgeblendetes Aufgabenmenü vor dem nächsten Öffnen auf."""
        menu = getattr(self, "_item_context_menu", None)
        self._item_context_menu = None
        if menu is None:
            return
        try:
            menu.destroy()
        except (AttributeError, tk.TclError):
            pass

    def _restore_item_selection(self, item_ids):
        for item_id in item_ids:
            if self.tree.exists(item_id):
                self.tree.selection_add(item_id)

    def set_item_color_selected(self, color_key):
        if not self.require_list_view():
            return "break"
        item_ids = self.get_selected_item_ids()
        if not item_ids:
            messagebox.showwarning("Hinweis", "Zuerst einen Punkt auswählen.")
            return "break"
        new_color = color_key if color_key in self.ITEM_COLOR_KEYS else None
        self.snapshot_undo()
        changed = False
        for item_id in item_ids:
            found = self.find_item(item_id)
            if found and found[0].get("color") != new_color:
                found[0]["color"] = new_color
                changed = True
        if not changed:
            if self.undo_stack:
                self.undo_stack.pop()
            return "break"
        self.save_items()
        self.refresh_tree(selected_id=item_ids[-1])
        self._restore_item_selection(item_ids)
        return "break"

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
        if not self.require_list_view(message=False):
            return "break"
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
    def set_importance_selected(self, value):
        if not self.require_list_view():
            return "break"
        item_ids = self.get_selected_item_ids()
        if not item_ids:
            messagebox.showwarning("Hinweis", "Zuerst einen Punkt auswählen.")
            return "break"
        new_value = self.clamp_importance(value)
        self.snapshot_undo()
        changed = False
        for item_id in item_ids:
            found = self.find_item(item_id)
            if found and self.clamp_importance(found[0].get("importance", 0)) != new_value:
                found[0]["importance"] = new_value
                changed = True
        if not changed:
            if self.undo_stack:
                self.undo_stack.pop()
            return "break"
        self.save_items()
        self.refresh_tree(selected_id=item_ids[-1])
        self._restore_item_selection(item_ids)
        return "break"

    def cycle_importance_selected(self, event=None):
        if not self.require_list_view():
            return "break"
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
        if not self.require_list_view():
            return "break"
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
        return self.set_due_value_selected(answer or None)

    def set_due_value_selected(self, due_value):
        """Setzt ein bereits bestimmtes ISO-Datum oder entfernt die Fälligkeit."""
        if not self.require_list_view():
            return "break"
        item_ids = self.get_selected_item_ids()
        if not item_ids:
            messagebox.showwarning("Hinweis", "Zuerst einen Punkt auswählen.")
            return "break"
        new_due = self.normalize_due(due_value) if due_value else None
        if due_value and new_due is None:
            messagebox.showwarning("Fälligkeit", "Das Fälligkeitsdatum ist ungültig.")
            return "break"
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
        self._restore_item_selection(item_ids)
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
        if not self.require_list_view(message=False):
            return "break"
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
        if not self.require_list_view():
            return "break"
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
        if not self.require_list_view():
            return "break"
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
        if self.view_mode != "list":
            self.drag_start_id = None
            self.drag_item_ids = []
            return
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
                    # Eine bereits bestehende Mehrfachauswahl bleibt beim Ziehen erhalten.
                    if self.drag_start_id not in self.tree.selection():
                        self.tree.selection_set(self.drag_start_id)
                    self.tree.focus(self.drag_start_id)
                    self.selection_anchor_id = self.drag_start_id
            selected = self.get_selected_item_ids()
            ordered_ids = [item_id for item_id in self.iter_tree_ids() if item_id in set(selected)]
            self.drag_item_ids = self.filter_top_level_selection(ordered_ids or [self.drag_start_id])
        return "break"

    def identify_sidebar_drop_row(self, event=None):
        if not hasattr(self, "sidebar_listbox"):
            return None, None
        try:
            pointer_x = getattr(event, "x_root", None)
            pointer_y = getattr(event, "y_root", None)
            if pointer_x is None or pointer_y is None:
                pointer_x = self.root.winfo_pointerx()
                pointer_y = self.root.winfo_pointery()
            for tree_name in ("inbox_listbox", "sidebar_listbox"):
                tree = getattr(self, tree_name, None)
                if tree is None:
                    continue
                local_x = pointer_x - tree.winfo_rootx()
                local_y = pointer_y - tree.winfo_rooty()
                if not (0 <= local_x < tree.winfo_width() and 0 <= local_y < tree.winfo_height()):
                    continue
                iid = tree.identify_row(local_y)
                return iid, self.sidebar_iid_to_row.get(iid)
            return None, None
        except tk.TclError:
            return None, None

    def pointer_is_over_widget(self, widget, event=None):
        try:
            pointer_x = getattr(event, "x_root", None)
            pointer_y = getattr(event, "y_root", None)
            if pointer_x is None or pointer_y is None:
                pointer_x = self.root.winfo_pointerx()
                pointer_y = self.root.winfo_pointery()
            local_x = pointer_x - widget.winfo_rootx()
            local_y = pointer_y - widget.winfo_rooty()
            return 0 <= local_x < widget.winfo_width() and 0 <= local_y < widget.winfo_height()
        except tk.TclError:
            return False

    def identify_tree_drop_row(self, event=None):
        """Liefert nur dann eine Task-Zeile, wenn der Zeiger wirklich über dem Task-Baum liegt."""
        if not hasattr(self, "tree"):
            return None
        try:
            pointer_x = getattr(event, "x_root", None)
            pointer_y = getattr(event, "y_root", None)
            if pointer_x is None or pointer_y is None:
                pointer_x = self.root.winfo_pointerx()
                pointer_y = self.root.winfo_pointery()
            local_x = pointer_x - self.tree.winfo_rootx()
            local_y = pointer_y - self.tree.winfo_rooty()
            if not (0 <= local_x < self.tree.winfo_width() and 0 <= local_y < self.tree.winfo_height()):
                return None
            return self.tree.identify_row(local_y)
        except tk.TclError:
            return None

    def resolve_task_drop_destination(self, sidebar_row):
        if not sidebar_row:
            return None
        row_type, row_id = sidebar_row
        if row_type == "list":
            return row_id
        if row_type != "folder":
            return None
        folder = self.get_folder(row_id)
        choices = [
            (entry.get("id"), entry.get("title", "Liste"))
            for entry in self.get_folder_lists(row_id)
            if entry.get("id") != self.active_list_id
        ]
        if not choices:
            messagebox.showinfo(
                "Kein anderes Ziel",
                "Dieser Ordner enthält keine andere Zielliste. Lege zuerst eine weitere Liste darin an.",
            )
            return None
        if len(choices) == 1:
            return choices[0][0]
        return self.themed_choice_dialog(
            "Ziel im Ordner wählen",
            f"In welche Liste von „{folder.get('title', 'Ordner')}“ soll der Punkt verschoben werden?",
            choices,
        )

    def move_items_to_list(self, item_ids, target_list_id):
        if not item_ids or not target_list_id or target_list_id == self.active_list_id:
            return False
        target = next((entry for entry in self.lists if entry.get("id") == target_list_id), None)
        if not target:
            return False
        ordered_ids = [item_id for item_id in self.iter_tree_ids() if item_id in set(item_ids)]
        ordered_ids = self.filter_top_level_selection(ordered_ids)
        moved_items = []
        self.snapshot_undo()
        for item_id in ordered_ids:
            moved = self.remove_item_by_id(item_id)
            if moved:
                moved_items.append(moved)
        if not moved_items:
            if self.undo_stack:
                self.undo_stack.pop()
            return False
        target.setdefault("items", []).extend(moved_items)
        self.save_items()
        self.refresh_tree()
        return True

    def on_drag_motion(self, event):
        if not self.drag_start_id:
            return
        if abs(event.x - self.drag_start_x) + abs(event.y - self.drag_start_y) > 6:
            self.drag_has_moved = True

        sidebar_iid, sidebar_row = self.identify_sidebar_drop_row(event)
        self.clear_drop_target_tags()
        self.clear_sidebar_drop_target_tags()
        if sidebar_iid and sidebar_row:
            try:
                target_tree = self.get_sidebar_tree_for_iid(sidebar_iid)
                if target_tree is None:
                    return
                tags = set(target_tree.item(sidebar_iid, "tags"))
                tags.add("drop_target")
                target_tree.item(sidebar_iid, tags=tuple(tags))
                if sidebar_row[0] == "folder":
                    target_tree.item(sidebar_iid, open=True)
            except tk.TclError:
                pass
            return

        target_id = self.identify_tree_drop_row(event)
        if target_id and target_id not in (self.EMPTY_ROW_ID, self.drag_start_id):
            try:
                current_tags = set(self.tree.item(target_id, "tags"))
                current_tags.add("drop_target")
                self.tree.item(target_id, tags=tuple(current_tags))
            except tk.TclError:
                pass

    def on_drag_end(self, event):
        source_id = self.drag_start_id
        dragged_ids = list(self.drag_item_ids or ([source_id] if source_id else []))
        _sidebar_iid, sidebar_row = self.identify_sidebar_drop_row(event)
        target_id = self.identify_tree_drop_row(event)
        shift_pressed = bool(event.state & 0x0001)

        self.clear_drop_target_tags()
        self.clear_sidebar_drop_target_tags()
        self.drag_start_id = None
        self.drag_item_ids = []

        if source_id and self.drag_has_moved and sidebar_row:
            destination_id = self.resolve_task_drop_destination(sidebar_row)
            if destination_id:
                self.move_items_to_list(dragged_ids, destination_id)
            return

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
        target_folder_id = self.active_folder_id if self.view_mode == "folder" else None
        for path in paths:
            try:
                with open(path, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                imported = self.parse_txt_items(lines)
                note = self.extract_txt_note(lines)
                if not imported and not note:
                    continue
                title = self.extract_txt_list_title(lines, path)
                created.append(self.new_list_object(title, imported, folder_id=target_folder_id, note=note))
            except Exception as e:
                messagebox.showerror("Fehler beim Listenimport", f"{os.path.basename(path)} konnte nicht importiert werden:\n{e}")
                return "break"
        if not created:
            messagebox.showwarning("Import", "In den ausgewählten Dateien wurden keine Aufgaben oder Notizen gefunden.")
            return "break"
        self.snapshot_undo()
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

    @staticmethod
    def extract_txt_note(lines):
        note_lines = []
        inside_note_block = False
        for raw_line in lines:
            stripped = raw_line.strip()
            if stripped == "[Seitennotiz]":
                inside_note_block = True
                continue
            if stripped == "[/Seitennotiz]":
                break
            if inside_note_block:
                note_lines.append(raw_line.rstrip("\r\n"))
        return "\n".join(note_lines).strip()

    def export_as_txt(self):
        if not self.require_list_view():
            return
        note = str(self.current_list().get("note") or "").strip()
        if not self.items and not note:
            messagebox.showwarning("Hinweis", "Keine Aufgaben oder Seitennotiz zum Exportieren.")
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
                if note:
                    file.write("[Seitennotiz]\n")
                    file.write(note + "\n")
                    file.write("[/Seitennotiz]\n\n")
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
            description = str(item.get("description") or "").strip()
            for line in description.splitlines():
                file.write(f"{indent}   Beschreibung: {line}\n")
            due_text = self.format_due_display(item.get("due"))
            if due_text:
                file.write(f"{indent}   Fällig: {due_text}\n")
            for attachment in item.get("attachments", []):
                file.write(f"{indent}   Anhang: {attachment.get('name', 'Datei')}\n")
            self.write_items_to_txt(file, item.get("children", []), current_number)

    def export_as_markdown(self):
        if not self.require_list_view():
            return
        note = str(self.current_list().get("note") or "").strip()
        if not self.items and not note:
            messagebox.showwarning("Hinweis", "Keine Aufgaben oder Seitennotiz zum Exportieren.")
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
                if note:
                    file.write(note + "\n\n")
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
            description = str(item.get("description") or "").strip()
            for line in description.splitlines():
                file.write(f"{indent}  > {line}\n")
            for attachment in item.get("attachments", []):
                file.write(f"{indent}  - Anhang: `{attachment.get('name', 'Datei')}`\n")
            self.write_items_to_markdown(file, item.get("children", []), level + 1)

    def export_as_csv(self):
        if not self.require_list_view():
            return
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
                writer.writerow(["Nummer", "Ebene", "Aufgabe", "Beschreibung", "Anhänge", "Erledigt", "Wichtigkeit", "Fällig"])
                self.write_items_to_csv(writer, self.items, [])
            messagebox.showinfo("Export erfolgreich", f"Liste exportiert nach:\n{path}")
        except Exception as e:
            messagebox.showerror("Fehler beim Export", str(e))

    @staticmethod
    def safe_csv_cell(value):
        """Verhindert, dass Nutztexte beim Öffnen in Excel als Formel starten."""
        text = str(value or "")
        if text.lstrip().startswith(("=", "+", "-", "@")):
            return "'" + text
        return text

    def write_items_to_csv(self, writer, items, number_prefix):
        for index, item in enumerate(items, start=1):
            current_number = number_prefix + [index]
            number_text = ".".join(str(part) for part in current_number)
            writer.writerow([
                number_text,
                len(current_number),
                self.safe_csv_cell(item.get("text", "")),
                self.safe_csv_cell(item.get("description", "")),
                self.safe_csv_cell(
                    " | ".join(str(attachment.get("name", "")) for attachment in item.get("attachments", []))
                ),
                "ja" if item.get("done") else "nein",
                self.IMPORTANCE_NAMES.get(self.clamp_importance(item.get("importance", 0)), "keine"),
                self.format_due_display(item.get("due")),
            ])
            self.write_items_to_csv(writer, item.get("children", []), current_number)

    def complete_backup_payload(self):
        payload = copy.deepcopy(self.data_payload())
        payload.update(
            {
                "app": APP_NAME,
                "app_version": APP_VERSION,
                "exported_at": datetime.now().isoformat(timespec="seconds"),
            }
        )
        return payload

    def collect_attachment_sources(self, lists):
        sources = {}
        total_size = 0
        for list_entry in lists:
            for item in self.walk_items(list_entry.get("items", [])):
                for attachment in item.get("attachments", []):
                    storage = self.validate_attachment_storage(attachment.get("storage"))
                    source = self.resolve_attachment_path(attachment)
                    if not source or not os.path.isfile(source):
                        raise FileNotFoundError(
                            f"Der Anhang „{attachment.get('name', storage)}“ fehlt. "
                            "Das Komplettbackup wurde nicht erstellt."
                        )
                    size = os.path.getsize(source)
                    if size > self.MAX_BACKUP_ATTACHMENT_BYTES:
                        raise ValueError(f"Der Anhang „{attachment.get('name', storage)}“ ist zu groß.")
                    if storage not in sources:
                        sources[storage] = source
                        total_size += size
        if total_size > self.MAX_BACKUP_TOTAL_BYTES:
            raise ValueError("Die Anhänge überschreiten die zulässige Gesamtgröße eines Backups.")
        return sources

    def validate_backup_target(self, path):
        target = os.path.normcase(os.path.realpath(os.path.abspath(path)))
        protected = {
            os.path.normcase(os.path.realpath(SAVE_FILE)),
            os.path.normcase(os.path.realpath(SETTINGS_FILE)),
        }
        if target in protected:
            raise ValueError("Diese Glide-Systemdatei darf nicht als Backupziel überschrieben werden.")
        attachments_root = os.path.normcase(os.path.realpath(ATTACHMENTS_DIR))
        try:
            if os.path.commonpath([target, attachments_root]) == attachments_root:
                raise ValueError("Ein Komplettbackup darf nicht im internen Anhangsordner liegen.")
        except ValueError as exc:
            if "Anhangsordner" in str(exc):
                raise
        return target

    def write_complete_backup(self, path, payload):
        """Schreibt ein vollständiges Backup atomar; fehlende Anhänge brechen ab."""
        target = self.validate_backup_target(path)
        attachment_paths = self.collect_attachment_sources(payload.get("lists", []))
        data_bytes = json.dumps(payload, ensure_ascii=False, indent=4).encode("utf-8")
        if len(data_bytes) > self.MAX_BACKUP_DATA_BYTES:
            raise ValueError("Die Glide-Daten sind für ein einzelnes Backup zu groß.")
        target_dir = os.path.dirname(target)
        os.makedirs(target_dir, exist_ok=True)
        fd, temp_path = tempfile.mkstemp(prefix=".glide-backup-", suffix=".tmp", dir=target_dir)
        os.close(fd)
        try:
            with zipfile.ZipFile(temp_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("data.json", data_bytes)
                for storage, source in sorted(attachment_paths.items()):
                    archive.write(source, arcname=storage)
            with zipfile.ZipFile(temp_path, "r") as check_archive:
                damaged = check_archive.testzip()
                if damaged:
                    raise OSError(f"Das erzeugte Backup ist bei {damaged} beschädigt.")
            with open(temp_path, "r+b") as file:
                file.flush()
                os.fsync(file.fileno())
            os.replace(temp_path, target)
            temp_path = None
            return len(attachment_paths)
        finally:
            if temp_path:
                try:
                    os.remove(temp_path)
                except OSError:
                    pass

    def inspect_backup_archive(self, archive):
        infos = archive.infolist()
        if len(infos) > self.MAX_BACKUP_MEMBERS:
            raise ValueError("Das Backup enthält zu viele Dateien.")
        seen_names = set()
        attachment_infos = {}
        data_info = None
        total_size = 0
        for info in infos:
            name = info.filename
            canonical_key = name.casefold()
            if canonical_key in seen_names:
                raise ValueError("Das Backup enthält doppelte Dateinamen.")
            seen_names.add(canonical_key)
            if info.flag_bits & 0x1:
                raise ValueError("Verschlüsselte Backup-Einträge werden nicht unterstützt.")
            unix_mode = (info.external_attr >> 16) & 0xFFFF
            if unix_mode and stat.S_ISLNK(unix_mode):
                raise ValueError("Symbolische Links sind in einem Backup nicht zulässig.")
            if info.is_dir():
                if name != "attachments/":
                    raise ValueError(f"Unbekannter Ordner im Backup: {name}")
                continue
            if name == "data.json":
                if info.file_size > self.MAX_BACKUP_DATA_BYTES:
                    raise ValueError("data.json im Backup ist zu groß.")
                data_info = info
            else:
                storage = self.validate_attachment_storage(name)
                if storage != name:
                    raise ValueError("Das Backup enthält einen nicht kanonischen Anhangspfad.")
                if info.file_size > self.MAX_BACKUP_ATTACHMENT_BYTES:
                    raise ValueError(f"Der Backup-Anhang {name} ist zu groß.")
                attachment_infos[storage] = info
            total_size += info.file_size
            if total_size > self.MAX_BACKUP_TOTAL_BYTES:
                raise ValueError("Das Backup überschreitet die zulässige Gesamtgröße.")
            if (
                info.file_size > self.BACKUP_COPY_CHUNK
                and info.compress_size > 0
                and info.file_size / info.compress_size > self.MAX_BACKUP_COMPRESSION_RATIO
            ):
                raise ValueError("Das Backup weist eine unplausibel hohe Kompressionsrate auf.")
        if data_info is None:
            raise ValueError("Im Glide-Backup fehlt data.json.")
        return data_info, attachment_infos

    def read_zip_member_limited(self, archive, info, limit):
        chunks = []
        total = 0
        with archive.open(info, "r") as source:
            while True:
                chunk = source.read(self.BACKUP_COPY_CHUNK)
                if not chunk:
                    break
                total += len(chunk)
                if total > limit:
                    raise ValueError("Ein Backup-Inhalt überschreitet die zulässige Größe.")
                chunks.append(chunk)
        if total != info.file_size:
            raise ValueError("Eine Dateigröße im Backup ist inkonsistent.")
        return b"".join(chunks)

    def copy_zip_member_limited(self, archive, info, target_path, limit):
        total = 0
        with archive.open(info, "r") as source, open(target_path, "wb") as target:
            while True:
                chunk = source.read(self.BACKUP_COPY_CHUNK)
                if not chunk:
                    break
                total += len(chunk)
                if total > limit:
                    raise ValueError("Ein Backup-Anhang überschreitet die zulässige Größe.")
                target.write(chunk)
            target.flush()
            os.fsync(target.fileno())
        if total != info.file_size:
            raise ValueError("Eine Anhangsgröße im Backup ist inkonsistent.")
        return total

    @staticmethod
    def safe_attachment_filename(original_name):
        stem, extension = os.path.splitext(os.path.basename(str(original_name or "datei")))
        safe_stem = re.sub(r"[^\w .()-]+", "_", stem, flags=re.UNICODE).strip(" .")[:90] or "datei"
        safe_extension = re.sub(r"[^A-Za-z0-9.]", "", extension)[:16]
        return f"{uuid.uuid4().hex}_{safe_stem}{safe_extension}"

    def remap_import_attachments(self, lists):
        """Gibt eingehenden Dateien neue Namen, damit Restore nie Bytes überschreibt."""
        storage_map = {}
        used_destinations = set()
        for list_entry in lists:
            for item in self.walk_items(list_entry.get("items", [])):
                for attachment in item.get("attachments", []):
                    old_storage = self.validate_attachment_storage(attachment.get("storage"))
                    if old_storage not in storage_map:
                        while True:
                            new_storage = f"attachments/{self.safe_attachment_filename(attachment.get('name'))}"
                            final_path = self.resolve_attachment_path({"storage": new_storage})
                            if new_storage not in used_destinations and final_path and not os.path.exists(final_path):
                                break
                        storage_map[old_storage] = new_storage
                        used_destinations.add(new_storage)
                    attachment["storage"] = storage_map[old_storage]
                    attachment["id"] = uuid.uuid4().hex
        return storage_map

    def ensure_inbox_in_collection(self, lists):
        inboxes = [entry for entry in lists if entry.get("system_role") == "inbox"]
        if inboxes:
            inbox = inboxes[0]
            for duplicate in inboxes[1:]:
                duplicate["system_role"] = None
        else:
            inbox = self.new_list_object("Eingang", [], system_role="inbox", color="due_action")
            lists.insert(0, inbox)
        inbox["title"] = "Eingang"
        inbox["folder_id"] = None
        return [inbox] + [entry for entry in lists if entry is not inbox]

    def export_full_backup(self):
        """Sichert Daten und alle referenzierten Anhänge gemeinsam und atomar."""
        self.sync_current_list_reference()
        default_filename = f"glide_backup_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.glidebackup"
        path = filedialog.asksaveasfilename(
            title="Komplettbackup speichern (alle Listen)",
            defaultextension=".glidebackup",
            initialfile=default_filename,
            filetypes=[("Glide-Komplettbackup", "*.glidebackup"), ("Alle Dateien", "*.*")],
        )
        if not path:
            return
        try:
            count = self.write_complete_backup(path, self.complete_backup_payload())
            attachment_word = "Anhang" if count == 1 else "Anhängen"
            messagebox.showinfo(
                "Backup erstellt",
                f"Komplettbackup mit {count} {attachment_word} gespeichert nach:\n{path}",
            )
        except Exception as e:
            messagebox.showerror("Fehler beim Backup", str(e))

    def import_full_backup(self):
        """Ersetzt den Bestand erst nach vollständiger Prüfung und Sicherung."""
        path = filedialog.askopenfilename(
            title="Komplettbackup laden (ersetzt alle Listen)",
            filetypes=[
                ("Glide-Komplettbackup", "*.glidebackup"),
                ("Frühere JSON-Backups", "*.json"),
                ("Alle Dateien", "*.*"),
            ],
        )
        if not path:
            return
        if not messagebox.askyesno(
            "Backup importieren",
            "Beim Import werden alle aktuell vorhandenen Listen ersetzt.\n\n"
            "Vom aktuellen Stand wird vorher automatisch ein vollständiges Sicherungsbackup angelegt.\n\n"
            "Fortfahren?",
        ):
            return

        archive = None
        staging_dir = None
        created_paths = []
        undo_size = len(self.undo_stack)
        committed = False
        try:
            is_portable = zipfile.is_zipfile(path)
            attachment_infos = {}
            if is_portable:
                archive = zipfile.ZipFile(path, "r")
                data_info, attachment_infos = self.inspect_backup_archive(archive)
                raw_json = self.read_zip_member_limited(archive, data_info, self.MAX_BACKUP_DATA_BYTES)
                data = json.loads(raw_json.decode("utf-8"))
            else:
                if os.path.getsize(path) > self.MAX_BACKUP_DATA_BYTES:
                    raise ValueError("Die JSON-Backupdatei ist zu groß.")
                with open(path, "rb") as file:
                    raw_json = file.read(self.MAX_BACKUP_DATA_BYTES + 1)
                if len(raw_json) > self.MAX_BACKUP_DATA_BYTES:
                    raise ValueError("Die JSON-Backupdatei ist zu groß.")
                data = json.loads(raw_json.decode("utf-8-sig"))

            referenced = self.validate_backup_schema(data, portable=is_portable)
            if is_portable and set(attachment_infos) != referenced:
                missing = sorted(referenced - set(attachment_infos))
                extra = sorted(set(attachment_infos) - referenced)
                details = []
                if missing:
                    details.append("fehlend: " + ", ".join(missing[:5]))
                if extra:
                    details.append("nicht referenziert: " + ", ".join(extra[:5]))
                raise ValueError("Die Anhänge im Backup sind unvollständig oder unerwartet (" + "; ".join(details) + ").")

            previous_folders = self.folders
            try:
                new_lists, active_from_file = self.normalize_lists_data(data)
                new_folders = self.folders
            finally:
                self.folders = previous_folders
            if not new_lists:
                raise ValueError("In der Datei wurden keine Listen gefunden.")
            new_lists = self.ensure_inbox_in_collection(new_lists)

            storage_map = {}
            staged_files = {}
            if is_portable:
                storage_map = self.remap_import_attachments(new_lists)
                staging_dir = tempfile.TemporaryDirectory(prefix=".glide-import-", dir=BASE_DIR)
                total_written = 0
                for old_storage, new_storage in storage_map.items():
                    info = attachment_infos[old_storage]
                    staged_path = os.path.join(staging_dir.name, os.path.basename(new_storage))
                    written = self.copy_zip_member_limited(
                        archive, info, staged_path, self.MAX_BACKUP_ATTACHMENT_BYTES
                    )
                    total_written += written
                    if total_written > self.MAX_BACKUP_TOTAL_BYTES:
                        raise ValueError("Die extrahierten Anhänge überschreiten die zulässige Gesamtgröße.")
                    staged_files[new_storage] = staged_path
            elif referenced:
                missing_local = [
                    storage
                    for storage in referenced
                    if not os.path.isfile(self.resolve_attachment_path({"storage": storage}) or "")
                ]
                if missing_local:
                    raise ValueError(
                        "Dieses JSON verweist auf Anhänge, enthält die Dateien aber nicht. "
                        "Bitte stattdessen das zugehörige .glidebackup verwenden."
                    )

            # Der aktuelle Zustand muss speicherbar sein, bevor er als vollständige
            # Rückfallebene gesichert und anschließend ersetzt wird.
            if not self.save_items():
                return
            pre_import_path = os.path.join(
                BACKUP_DIR,
                f"vor_import_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.glidebackup",
            )
            self.write_complete_backup(pre_import_path, self.complete_backup_payload())
            self.snapshot_undo()

            for new_storage, staged_path in staged_files.items():
                final_path = self.resolve_attachment_path({"storage": new_storage})
                if not final_path or os.path.exists(final_path):
                    raise OSError("Ein sicherer Zielpfad für einen importierten Anhang konnte nicht erstellt werden.")
                os.replace(staged_path, final_path)
                created_paths.append(final_path)

            existing_ids = [entry.get("id") for entry in new_lists]
            preferred = active_from_file if active_from_file in existing_ids else new_lists[0]["id"]
            requested_folder_id = data.get("active_folder_id") if isinstance(data, dict) else None
            folder_ids = {folder.get("id") for folder in new_folders}
            requested_folder_id = requested_folder_id if requested_folder_id in folder_ids else None
            imported_payload = {
                "version": self.DATA_SCHEMA_VERSION,
                "active_list_id": preferred,
                "active_folder_id": requested_folder_id,
                "folders": new_folders,
                "lists": new_lists,
            }
            self.write_json_atomic(SAVE_FILE, imported_payload)
            committed = True

            self.lists = new_lists
            self.folders = new_folders
            self.active_list_id = None
            self.active_folder_id = None
            self.items = []
            self.view_mode = "list"
            self.set_active_list(preferred, refresh=False)
            if requested_folder_id:
                self.set_active_folder(requested_folder_id, refresh=False)
            self.dirty = False
            self.update_sidebar_list()
            self.refresh_tree()
            self.save_settings()
            messagebox.showinfo(
                "Import erfolgreich",
                f"{len(self.lists)} Liste(n) importiert.\n\n"
                f"Sicherung des vorherigen Stands:\n{pre_import_path}",
            )
        except (json.JSONDecodeError, UnicodeDecodeError):
            messagebox.showerror("Fehler", "Die Datei ist kein gültiges Glide-Backup.")
        except Exception as e:
            if not committed:
                for created_path in reversed(created_paths):
                    try:
                        os.remove(created_path)
                    except OSError:
                        pass
                while len(self.undo_stack) > undo_size:
                    self.undo_stack.pop()
            messagebox.showerror("Fehler beim Import", str(e))
        finally:
            if archive:
                archive.close()
            if staging_dir:
                staging_dir.cleanup()

    def sort_current_list(self, key="due"):
        """Sortiert die aktive Liste rekursiv nach Fälligkeit, Wichtigkeit oder Alphabet."""
        if not self.require_list_view():
            return
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
        if not self.require_list_view():
            return
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
            note = self.extract_txt_note(lines)
            if imported or note:
                self.snapshot_undo()
                self.items.extend(imported)
                if note:
                    current_note = str(self.current_list().get("note") or "").strip()
                    self.current_list()["note"] = (
                        f"{current_note}\n\n{note}" if current_note and note != current_note else note or current_note
                    )
                self.save_items()
                self.update_page_note_preview()
                self.refresh_tree(selected_id=imported[-1]["id"] if imported else None)
                messagebox.showinfo(
                    "Import erfolgreich",
                    f"{self.count_items(imported)} Punkte und "
                    f"{'eine Seitennotiz' if note else 'keine Seitennotiz'} importiert.",
                )
            else:
                messagebox.showwarning("Import", "Die Datei enthält keine erkennbaren Aufgaben oder Seitennotiz.")
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

        inside_note_block = False
        last_item = None
        for line_index, raw_line in enumerate(lines):
            if line_index in skip_indices:
                continue
            stripped = raw_line.strip()
            if stripped == "[Seitennotiz]":
                inside_note_block = True
                continue
            if stripped == "[/Seitennotiz]":
                inside_note_block = False
                continue
            if inside_note_block:
                continue
            if stripped.startswith("Beschreibung:"):
                if last_item is not None:
                    description_line = stripped.split(":", 1)[1].lstrip()
                    previous = str(last_item.get("description") or "")
                    last_item["description"] = f"{previous}\n{description_line}".strip("\n")
                continue
            if stripped.startswith("Fällig:"):
                if last_item is not None:
                    parsed_due = self.parse_due_input(stripped.split(":", 1)[1].strip())
                    if parsed_due:
                        last_item["due"] = parsed_due
                continue
            if stripped.startswith("Anhang:"):
                # Textimporte transportieren nur den Namen, nicht die Binärdatei.
                continue
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
            last_item = new

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
        edit_menu.add_command(label="Punktdetails …", accelerator="F2", command=self.edit_item)
        edit_menu.add_command(label="Seitennotiz …", accelerator="Strg+M", command=self.edit_page_note)
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

        self.menus = [menubar, file_menu, export_menu, edit_menu, view_menu, sort_menu, help_menu]
        self.custom_menu_buttons = []
        if os.name == "nt":
            # Eine native Tk-Menüzeile bleibt unter Windows häufig weiß. Die
            # eigene schmale Menüzeile lässt sich zuverlässig mit dem Theme färben.
            self.custom_menubar = self.register_theme_widget(
                tk.Frame(self.root, bg=self.theme["bg"], height=30), "bg"
            )
            self.custom_menubar.pack(fill="x", side="top")
            self.custom_menubar.pack_propagate(False)
            menu_specs = [
                ("Datei", file_menu, "d"),
                ("Bearbeiten", edit_menu, "b"),
                ("Ansicht", view_menu, "a"),
                ("Hilfe", help_menu, "h"),
            ]
            for label, menu, mnemonic in menu_specs:
                # Ein Menubutton darf nur ein untergeordnetes Menü automatisch
                # posten. Unsere Menüs gehören aus Kompatibilitätsgründen zum
                # zentralen Menübaum; ein normaler Button mit tk_popup ist hier
                # deshalb unter Windows robuster.
                button = tk.Button(
                    self.custom_menubar,
                    text=label,
                    underline=0,
                    relief="flat",
                    bd=0,
                    highlightthickness=0,
                    padx=10,
                    pady=5,
                    font=("TkDefaultFont", 9),
                    takefocus=True,
                )
                button.configure(command=lambda b=button, m=menu: self._post_custom_menu(b, m))
                button.pack(side="left", fill="y")
                self.custom_menu_buttons.append(button)
                self.root.bind(
                    f"<Alt-{mnemonic}>",
                    lambda event, b=button, m=menu: self._post_custom_menu(b, m),
                )
        else:
            try:
                self.root.config(menu=menubar)
            except tk.TclError:
                pass
        self.menubar = menubar

    def _post_custom_menu(self, button, menu):
        previous_focus = self.root.focus_get()
        try:
            button.focus_set()
            menu.tk_popup(button.winfo_rootx(), button.winfo_rooty() + button.winfo_height())
        finally:
            try:
                menu.grab_release()
            except tk.TclError:
                pass
            try:
                if previous_focus is not None and previous_focus.winfo_exists():
                    previous_focus.focus_set()
            except tk.TclError:
                pass
        return "break"

    def open_backup_folder(self):
        self.open_external_path(BACKUP_DIR)

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
            "Rechtsklick – Details, Wichtigkeit, Fälligkeit, Farbe und Entfernen\n"
            "Strg+Shift+F – Wichtigkeit durchschalten\n"
            "Strg+T – Fälligkeitsdatum setzen oder entfernen\n"
            "F2 – Punktdetails, Beschreibung und Anhänge · F3 – Titel bearbeiten\n"
            "Strg+M – freie Seiten-/Ordnernotiz öffnen\n"
            "Rechtsklick auf Liste oder Ordner – Farbe wählen\n"
            "Ordner anklicken – enthaltene Listen im Hauptbereich anzeigen\n"
            "Auf Seitenleisten-Liste ziehen – Punkt dorthin verschieben\n"
            "Auf Ordner ziehen – enthaltene Zielliste auswählen\n"
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
