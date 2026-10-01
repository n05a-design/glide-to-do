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
import subprocess
import sys
import tempfile
import time
import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk as ttk
import uuid
import zipfile
from tkinter import messagebox, filedialog
from datetime import datetime, date, timedelta

# --- Produkt-Branding -------------------------------------------------------
APP_NAME = "Glide"
APP_TAGLINE = "Aufgaben und Listen"
APP_PRODUCT_NAME = f"{APP_NAME} \u2013 {APP_TAGLINE}"
APP_VERSION = "2.7.2"
IS_MACOS = sys.platform == "darwin"
IS_WINDOWS = os.name == "nt"
# Frühere App-/Ordnernamen, aus denen bestehende Nutzerdaten automatisch
# übernommen werden, wenn im Glide-Ordner noch nichts liegt.
LEGACY_APP_NAMES = ["Lokale Listen-App"]
LEGACY_BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_app_data_dir():
    """Plattformgerechter, beschreibbarer Speicherort ohne externe Bibliotheken.

    GLIDE_DATA_DIR überschreibt den Pfad vollständig. Das ist der einzige
    plattformunabhängige Weg, Tests zu isolieren: %APPDATA% wirkt nur unter
    Windows, unter macOS und Linux würde ein Test sonst die echten Nutzerdaten
    in ~/Library/Application Support/Glide bzw. ~/.local/share/Glide benutzen.
    """
    override = os.environ.get("GLIDE_DATA_DIR")
    if override:
        path = os.path.abspath(os.path.expanduser(override))
        os.makedirs(path, exist_ok=True)
        return path
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
    if os.environ.get("GLIDE_DATA_DIR"):
        # Bei ausdrücklich gesetztem Datenordner findet keine Alt-Übernahme statt.
        return None
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
        # Dauerhafte Füllung für Schaltflächen, die einen aktiven Zustand
        # anzeigen – etwa der gewählte Kalendermodus. None bedeutet: nur beim
        # Überfahren gefüllt, wie bisher.
        self.active_fill = None
        self.active_text_color = None

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

    def set_active(self, fill=None, text_color=None):
        """Markiert die Schaltfläche dauerhaft als aktiv (oder hebt das auf)."""
        self.active_fill = fill
        self.active_text_color = text_color
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

        if self.is_hovered:
            fill = self.hover_fill
            text_color = self.hover_text_color
        elif self.active_fill:
            fill = self.active_fill
            text_color = self.active_text_color or self.hover_text_color
        else:
            fill = self.bg_color
            text_color = self.border_color
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
            # Umrandung eines Kalendertags unter dem Mauszeiger.
            "calendar_hover": "#7FB4F7",
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
            "calendar_hover": "#5AA2F0",
        },
    }

    EMPTY_ROW_ID = "__empty__"
    IN_PROGRESS_ROW_ID = "smart:in-progress"
    TRASH_ROW_ID = "smart:trash"
    # --- Automatische Sicherungen -------------------------------------------
    # Obergrenze, Mindestbestand und Höchstalter greifen gemeinsam: erst wird
    # der Mindestbestand reserviert, dann werden ältere Sicherungen nach Alter
    # entfernt, zuletzt begrenzt die Obergrenze den Rest. Dadurch bleibt immer
    # eine verlässliche Rückfallebene erhalten, ohne dass der Ordner wächst.
    MAX_BACKUPS = 40
    MIN_BACKUPS = 10
    BACKUP_MAX_AGE_MINUTES = 30
    # Frühestens nach dieser Zeit legt ein gewöhnliches Speichern eine neue
    # Sicherung an. Ohne diese Sperre entstünde bei jedem Tastendruck eine Datei.
    BACKUP_MIN_INTERVAL_SECONDS = 120
    # Zeitgesteuertes Speichern und garantierter Sicherungspunkt.
    AUTOSAVE_INTERVAL_MINUTES = 5
    DATA_SCHEMA_VERSION = 7
    MIN_PORTABLE_BACKUP_SCHEMA_VERSION = 4
    # Format 6 ergänzt die Art eines Punkts. Fehlt das Feld – also in allen
    # Beständen bis Format 5 – gilt der Punkt als gewöhnliche Aufgabe.
    ITEM_KIND_TASK = "task"
    ITEM_KIND_GROUP = "group"
    ITEM_KINDS = (ITEM_KIND_TASK, ITEM_KIND_GROUP)
    GROUP_MARKER = "\U0001F4C1 "  # Ordnersymbol vor Gruppentiteln
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
    SIDEBAR_TITLE_MAX_CHARS = 20
    SIDEBAR_ITEM_LEFT_PADDING = 8
    SYSTEM_ITEM_LEFT_PADDING = 10
    # Trennung zwischen Systembereich und Listenbereich: ein Band in der
    # Fensterfarbe, umgeben von Abstand. Keine Linie und kein zweiter Rahmen.
    SIDEBAR_DIVIDER_HEIGHT = 10
    SIDEBAR_SECTION_GAP = 12
    DUE_COLUMN_WIDTH = 132
    DUE_RIGHT_PADDING_WIDTH = 16
    TASK_TREE_EDGE_PADDING = 2
    # Einheitliche Innenabstände aller Eingabeflächen (Entry, Text, Listbox).
    # Zusammen mit der 1 px starken Feldlinie ergibt sich in jedem Dialog
    # derselbe sichtbare Textanfang; Beschriftungen stehen bündig am Rand.
    DIALOG_PAD_X = 24
    DIALOG_PAD_Y = 22
    FIELD_BORDER_WIDTH = 1
    FIELD_PAD_X = 12
    FIELD_PAD_Y = 9
    FIELD_LABEL_GAP = 5
    HEADER_TITLE_MIN_WIDTH = 140
    # Schriftfamilie der Hauptüberschrift. None bedeutet: Systemschrift der
    # Oberfläche verwenden. Für eine eigene Hausschrift genügt es, hier den
    # Familiennamen einzutragen – der Rest der Logik bleibt unverändert.
    HEADER_FONT_FAMILY = None
    HEADER_FONT_SIZE = 24
    # Schnitte, die schwerer als der reguläre Fettschnitt sind – absteigend
    # nach Strichstärke. Tk kennt für 'weight' nur normal und bold; alles
    # darüber liegt als eigene Schriftfamilie vor ("Segoe UI Black").
    # Semibold und Demibold stehen bewusst NICHT in dieser Liste: sie sind
    # leichter als Bold und würden den Titel dünner statt fetter machen.
    FONT_WEIGHT_SUFFIXES = (
        "Black",
        "Heavy",
        "ExtraBlack",
        "Extra Black",
        "UltraBlack",
        "Ultra Black",
        "ExtraBold",
        "Extra Bold",
        "UltraBold",
        "Ultra Bold",
    )
    # Diese Marker bleiben absichtlich stabil, damit TXT-Dateien auch von
    # älteren Glide-Versionen gelesen werden können. In der UI heißt der
    # Inhalt ab 2.5.4 einheitlich "Beschreibungstext".
    TXT_NOTE_BLOCK_START = "[Seitennotiz]"
    TXT_NOTE_BLOCK_END = "[/Seitennotiz]"

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

    # --- Labels --------------------------------------------------------------
    # Labels nutzen dieselbe Palette wie Listen- und Aufgabenfarben; jeder Wert
    # ist ein Theme-Schlüssel und damit in Hell und Dunkel definiert. Die
    # Labelfarbe bleibt trotzdem eine eigene Eigenschaft: sie wird getrennt von
    # der Aufgabenfarbe gespeichert und gesetzt.
    #
    # Eine ttk.Treeview kann eine einzelne Zelle nicht einfärben, deshalb steht
    # in der Labelspalte reiner Text. Farbig – und damit eindeutig – ist ein
    # Label überall dort, wo Tk es zulässt: in der Labelverwaltung, im
    # Farbauswahldialog, in den Kontextmenüs und in der Kopfzeile einer Liste
    # oder eines Ordners.
    LABEL_COLOR_CHOICES = LIST_COLOR_CHOICES
    LABEL_COLOR_KEYS = LIST_COLOR_KEYS
    LABEL_COLOR_NAMES = {key: name for name, key in LABEL_COLOR_CHOICES}
    DEFAULT_LABEL_COLOR = "accent"
    # Farbschlüssel der internen Testfassung 2.7.0 auf die endgültige Palette
    # abbilden, damit dort angelegte Labels ihre Farbe behalten.
    LEGACY_LABEL_COLOR_MAP = {
        "label_red": "delete",
        "label_orange": "flag",
        "label_yellow": "flag",
        "label_green": "export",
        "label_blue": "clear",
        "label_purple": "accent",
        "label_brown": "import",
        "label_gray": "due_action",
    }
    MAX_LABELS = 80
    MAX_LABEL_NAME_LENGTH = 40
    LABEL_COLUMN_WIDTH = 210
    LABEL_COLUMN_MAX_VISIBLE = 2
    LABEL_COLUMN_NAME_MAX_CHARS = 12
    LABEL_SEPARATOR = "  ·  "
    MAX_LABELS_PER_ITEM = 20

    # --- Papierkorb ----------------------------------------------------------
    # Gelöschte Listen und Ordner wandern vollständig in den Papierkorb und
    # bleiben wiederherstellbar. Die Obergrenze verhindert, dass die
    # Speicherdatei unbegrenzt wächst; sie ist bewusst hoch angesetzt.
    MAX_TRASH_ENTRIES = 200
    TRASH_KIND_LIST = "list"
    TRASH_KIND_FOLDER = "folder"

    # --- Kalender ------------------------------------------------------------
    CALENDAR_MODE_WEEK = "week"
    CALENDAR_MODE_MONTH = "month"
    CALENDAR_MODES = (CALENDAR_MODE_WEEK, CALENDAR_MODE_MONTH)
    # In der Monatsansicht ist eine Zelle flach, in der Wochenansicht steht die
    # volle Fensterhöhe für einen einzigen Tag zur Verfügung.
    CALENDAR_MAX_TASKS_PER_DAY = 3
    CALENDAR_MAX_TASKS_PER_WEEK_DAY = 14
    # In der flachen Monatszelle wird gekürzt, in der hohen Wochenzelle umgebrochen.
    CALENDAR_MONTH_TEXT_MAX_CHARS = 22

    WINDOWS_CHROME_RETRY_DELAYS_MS = (0, 40, 120, 300)

    def __init__(self, root):
        self.root = root
        self.root.title(APP_PRODUCT_NAME)
        self.root.geometry("1000x800")
        self.root.minsize(860, 700)

        self.items = []
        self.lists = []
        self.folders = []
        self.labels = []
        self.trash = []
        self._last_backup_monotonic = None
        self._autosave_id = None
        self.sidebar_rows = []
        self.sidebar_iid_to_row = {}
        self.sidebar_folder_open_states = {}
        self.in_progress_item_sources = {}
        self.sidebar_drag_start_iid = None
        self.sidebar_drag_start_y = 0
        self.sidebar_drag_has_moved = False
        self.active_list_id = None
        self.active_folder_id = None
        self.view_mode = "list"
        self.undo_stack = []
        self.dirty = False
        self._after_ids = set()
        self._scrollbar_refresh_id = None

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
        self.collapsed_item_ids = set()
        self._item_context_menu = None
        self._sidebar_context_menu = None

        self.theme_name = self.settings.get("theme", "light")
        if self.theme_name not in self.THEMES:
            self.theme_name = "light"
        self.active_list_id = self.settings.get("active_list_id") if isinstance(self.settings.get("active_list_id"), str) else None
        saved_folder_id = self.settings.get("active_folder_id")
        self.active_folder_id = saved_folder_id if isinstance(saved_folder_id, str) and saved_folder_id else None
        saved_view_mode = self.settings.get("view_mode")
        if self.active_folder_id:
            self.view_mode = "folder"
        elif saved_view_mode in ("in_progress", "trash"):
            self.view_mode = saved_view_mode
        else:
            self.view_mode = "list"
        self.app_title = self.settings.get("title", "Meine Liste").strip() or "Meine Liste"
        self.theme = self.THEMES[self.theme_name]
        self.theme_widgets = []
        self.rounded_containers = []
        self.buttons = []

        if IS_WINDOWS:
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
        self.schedule_autosave()

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
        if IS_MACOS:
            self.root.bind("<Command-c>", self.copy_selected_to_clipboard)
            self.root.bind("<Command-v>", self.paste_items_from_clipboard)
            self.root.bind("<Command-a>", self.select_all_items)
            self.root.bind("<Command-z>", self.undo_last_change)
            self.root.bind("<Command-f>", self.focus_search)
            self.root.bind("<Command-F>", self.handle_control_f)
            self.root.bind("<Command-t>", self.set_due_date_selected)
            self.root.bind("<Command-s>", lambda e: self.save_items())
            self.root.bind("<Command-e>", lambda e: self.export_as_txt())
            self.root.bind("<Command-i>", lambda e: self.import_from_txt())
            self.root.bind("<Command-d>", lambda e: self.toggle_theme())
            self.root.bind("<Command-g>", lambda e: self.group_selected_items())
            self.root.bind("<Command-n>", self.handle_control_n)
            self.root.bind("<Command-N>", self.handle_control_n)
            # Mac-Tastaturen besitzen meist keine Entf-Taste; Rückschritt löscht
            # den ausgewählten Punkt. In Text- und Suchfeldern bleibt sie normal.
            self.root.bind("<BackSpace>", self.delete_item)
            self.root.bind("<Command-BackSpace>", self.delete_item)
            # Cmd+Q wird von macOS abgefangen und würde WM_DELETE_WINDOW und
            # damit die Speicherabfrage überspringen.
            try:
                self.root.createcommand("::tk::mac::Quit", self.on_close)
            except tk.TclError:
                pass
        self.root.bind("<Control-n>", self.handle_control_n)
        self.root.bind("<Control-N>", self.handle_control_n)
        self.root.bind("<Control-w>", self.delete_current_list)
        self.root.bind("<Control-f>", self.handle_control_f)
        self.root.bind("<Control-F>", self.handle_control_f)
        self.root.bind("<Alt-p>", self.cycle_importance_selected)
        self.root.bind("<Control-g>", lambda e: self.group_selected_items())
        self.root.bind("<Escape>", self.handle_escape)
        self.root.bind("<F2>", lambda e: self.edit_item())
        self.root.bind("<F3>", lambda e: self.edit_title())
        self.root.bind("<Control-d>", lambda e: self.toggle_theme())
        self.root.bind("<Control-t>", self.set_due_date_selected)
        self.root.bind("<Control-m>", self.edit_page_note)
        self.root.bind("<Control-l>", self.open_label_manager)
        self.root.bind("<Control-k>", self.open_calendar_view)
        if IS_MACOS:
            self.root.bind("<Command-l>", self.open_label_manager)
            self.root.bind("<Command-k>", self.open_calendar_view)

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
        # Atomar wie die Nutzdaten: ein Absturz während des Schreibens darf die
        # bestehenden Einstellungen nicht als Rumpfdatei zurücklassen.
        try:
            self.write_json_atomic(
                SETTINGS_FILE,
                {
                    "theme": self.theme_name,
                    "title": self.app_title,
                    "hide_done": bool(self.hide_done_var.get()) if hasattr(self, "hide_done_var") else False,
                    "filter_mode": self.get_filter_mode() if hasattr(self, "hide_done_var") else "all",
                    "active_list_id": self.active_list_id,
                    "active_folder_id": self.active_folder_id if self.view_mode == "folder" else None,
                    "view_mode": self.view_mode,
                },
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
        if self.view_mode == "in_progress":
            return "In Bearbeitung"
        if self.view_mode == "trash":
            return "Papierkorb"
        if self.view_mode == "folder" and self.active_folder_id:
            folder = self.get_folder(self.active_folder_id)
            if folder:
                return str(folder.get("title") or "Ordner").strip() or "Ordner"
        return self.app_title

    def get_active_page(self):
        if self.view_mode in ("in_progress", "trash"):
            return None
        if self.view_mode == "folder" and self.active_folder_id:
            return self.get_folder(self.active_folder_id)
        return self.current_list() if self.lists else None

    def require_list_view(self, message=True):
        """Verhindert, dass Aktionen unsichtbar die zuletzt geöffnete Liste ändern."""
        if self.view_mode == "list":
            return True
        if message:
            if self.view_mode == "in_progress":
                messagebox.showinfo("In Bearbeitung", "Öffne die Aufgabe per Doppelklick in ihrer Quellliste.")
            elif self.view_mode == "trash":
                messagebox.showinfo(
                    "Papierkorb",
                    "Im Papierkorb lassen sich Einträge nur wiederherstellen oder endgültig entfernen.",
                )
            else:
                messagebox.showinfo("Ordnerübersicht", "Öffne zuerst eine Liste in diesem Ordner.")
        return False

    def ui_font_family(self):
        """Tatsächlich verwendete Familie der Oberflächenschrift."""
        family = getattr(self, "_ui_font_family", None)
        if family:
            return family
        family = "TkDefaultFont"
        try:
            actual = tkfont.nametofont("TkDefaultFont", root=self.root).actual("family")
            if actual:
                family = actual
        except (tk.TclError, RuntimeError):
            pass
        self._ui_font_family = family
        return family

    def available_font_families(self):
        families = getattr(self, "_font_families", None)
        if families is None:
            try:
                families = {name.strip() for name in tkfont.families(root=self.root)}
            except (tk.TclError, RuntimeError):
                families = set()
            self._font_families = families
        return families

    def heaviest_font(self, size, family=None):
        """Schwerster verfügbarer Schnitt der gewählten Schriftfamilie.

        Tk kennt für 'weight' nur normal und bold. Alles darüber – Semibold,
        Black, Heavy – liegt als eigene Schriftfamilie vor. Existiert eine
        solche Familie, wird sie direkt benannt und ohne zusätzliches Bold
        gesetzt, damit Tk den Schnitt nicht künstlich verdoppelt. Andernfalls
        bleibt es beim regulären Fettschnitt.
        """
        base = family or self.HEADER_FONT_FAMILY or self.ui_font_family()
        cache_key = (base, size)
        cache = getattr(self, "_heaviest_font_cache", None)
        if cache is None:
            cache = {}
            self._heaviest_font_cache = cache
        if cache_key in cache:
            return cache[cache_key]

        # Benennt HEADER_FONT_FAMILY bereits einen schweren Schnitt – etwa
        # "Inter ExtraBold" –, wird er unverändert übernommen. Ein zusätzliches
        # Bold würde Tk sonst zu einem künstlich verdoppelten Schnitt zwingen.
        base_folded = base.casefold()
        if any(base_folded.endswith(f" {suffix}".casefold()) for suffix in self.FONT_WEIGHT_SUFFIXES):
            resolved = (base, size, "normal")
            cache[cache_key] = resolved
            return resolved

        resolved = (base, size, "bold")
        families = self.available_font_families()
        if families:
            lookup = {name.casefold(): name for name in families}
            for suffix in self.FONT_WEIGHT_SUFFIXES:
                candidate = lookup.get(f"{base} {suffix}".casefold())
                if candidate:
                    # Eigene schwere Familie: ohne zusätzliches Bold setzen,
                    # sonst verdoppelt Tk den Schnitt künstlich.
                    resolved = (candidate, size, "normal")
                    break
        cache[cache_key] = resolved
        return resolved

    def header_title_font(self):
        return self.heaviest_font(self.HEADER_FONT_SIZE)

    def group_row_font(self):
        """Gruppen im Aufgabenbaum heben sich durch den Fettschnitt ab."""
        return (self.ui_font_family(), 12, "bold")

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
            # Ein Dialog darf nie außerhalb des sichtbaren Bereichs landen –
            # etwa wenn das Hauptfenster am Bildschirmrand oder auf einem
            # inzwischen abgemeldeten zweiten Monitor liegt.
            screen_w = dialog.winfo_screenwidth()
            screen_h = dialog.winfo_screenheight()
            x = max(0, min(x, max(0, screen_w - width)))
            y = max(0, min(y, max(0, screen_h - height)))
        except tk.TclError:
            x, y = 200, 150
        dialog.geometry(f"{width}x{height}+{x}+{y}")

    def _make_field(self, master):
        """Einheitlicher Feldrahmen für alle Dialoge.

        Liefert (border, field): eine 1 px starke Außenlinie in `input_border`
        und eine Innenfläche in `input`. Das eigentliche Eingabewidget wird in
        `field` mit FIELD_PAD_X/FIELD_PAD_Y gepackt, damit Entry, Text und
        Listbox app-weit denselben sichtbaren Textabstand besitzen.
        """
        border = tk.Frame(master, bg=self.theme["input_border"])
        field = tk.Frame(border, bg=self.theme["input"])
        return border, field

    def _make_field_label(self, master, text):
        """Feldbeschriftung – bündig mit der linken Feldkante."""
        return tk.Label(
            master,
            text=text,
            bg=self.theme["bg"],
            fg=self.theme["muted"],
            font=("TkDefaultFont", 9, "bold"),
            anchor="w",
            justify="left",
        )

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
        container.pack(fill="both", expand=True, padx=self.DIALOG_PAD_X, pady=self.DIALOG_PAD_Y)

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
        border, field = self._make_field(container)
        border.pack(fill="x")
        field.pack(fill="x", padx=self.FIELD_BORDER_WIDTH, pady=self.FIELD_BORDER_WIDTH)
        entry = tk.Entry(
            field,
            bg=self.theme["input"],
            fg=self.theme["text"],
            insertbackground=self.theme["text"],
            selectbackground=self.theme["selection"],
            selectforeground="#FFFFFF",
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=("TkDefaultFont", 12),
        )
        entry.pack(fill="x", padx=self.FIELD_PAD_X, pady=self.FIELD_PAD_Y)
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
        """Mehrzeiliger, themenkonformer Editor für Beschreibungs- und Aufgabentexte."""
        result = {"value": None}
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.configure(bg=self.theme["bg"])
        dialog.transient(self.root)
        dialog.minsize(560, 380)

        container = tk.Frame(dialog, bg=self.theme["bg"])
        container.pack(fill="both", expand=True, padx=self.DIALOG_PAD_X, pady=self.DIALOG_PAD_Y)
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

        border, field = self._make_field(container)
        border.pack(fill="both", expand=True)
        field.pack(fill="both", expand=True, padx=self.FIELD_BORDER_WIDTH, pady=self.FIELD_BORDER_WIDTH)
        text = tk.Text(
            field,
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
            padx=self.FIELD_PAD_X,
            pady=self.FIELD_PAD_Y,
        )
        text.pack(fill="both", expand=True)
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
        if IS_MACOS:
            dialog.bind("<Command-Return>", submit)
        dialog.bind("<Escape>", cancel)
        dialog.protocol("WM_DELETE_WINDOW", cancel)
        self._center_dialog(dialog, min_width=620)
        self._schedule_windows_chrome_theme(dialog)
        text.focus_set()
        dialog.grab_set()
        self.root.wait_window(dialog)
        return result["value"]

    def themed_page_details_dialog(self, heading, title_value, note_value, title_label="Titel", title_editable=True):
        """Titel und Beschreibungstext einer Liste oder eines Ordners in einem Fenster.

        Bewusst nach demselben Muster wie „Punktdetails“ aufgebaut: gleiche
        Feldrahmen, gleiche Abstände, gleiche Tastenbelegung. Rückgabe ist ein
        Dictionary mit ``title`` und ``note`` oder None bei Abbruch.
        """
        result = {"value": None}

        dialog = tk.Toplevel(self.root)
        dialog.title(heading)
        dialog.configure(bg=self.theme["bg"])
        dialog.transient(self.root)
        dialog.minsize(600, 460)

        container = tk.Frame(dialog, bg=self.theme["bg"])
        container.pack(fill="both", expand=True, padx=self.DIALOG_PAD_X, pady=self.DIALOG_PAD_Y)
        tk.Label(
            container,
            text=heading,
            bg=self.theme["bg"],
            fg=self.theme["text"],
            font=("TkDefaultFont", 16, "bold"),
            anchor="w",
        ).pack(anchor="w", pady=(0, 16))

        self._make_field_label(container, title_label).pack(anchor="w", pady=(0, self.FIELD_LABEL_GAP))
        title_border, title_field = self._make_field(container)
        title_border.pack(fill="x", pady=(0, 14))
        title_field.pack(fill="x", padx=self.FIELD_BORDER_WIDTH, pady=self.FIELD_BORDER_WIDTH)
        title_entry = tk.Entry(
            title_field,
            bg=self.theme["input"], fg=self.theme["text"], insertbackground=self.theme["text"],
            selectbackground=self.theme["selection"], selectforeground="#FFFFFF",
            relief="flat", bd=0, highlightthickness=0, font=("TkDefaultFont", 12),
        )
        title_entry.pack(fill="x", padx=self.FIELD_PAD_X, pady=self.FIELD_PAD_Y)
        title_entry.insert(0, str(title_value or ""))
        if not title_editable:
            # Der Eingang behält seinen Namen; sein Beschreibungstext bleibt frei.
            title_entry.configure(state="readonly", readonlybackground=self.theme["input"], fg=self.theme["muted"])

        self._make_field_label(container, "Beschreibungstext").pack(anchor="w", pady=(0, self.FIELD_LABEL_GAP))
        note_border, note_field = self._make_field(container)
        note_border.pack(fill="both", expand=True)
        note_field.pack(fill="both", expand=True, padx=self.FIELD_BORDER_WIDTH, pady=self.FIELD_BORDER_WIDTH)
        note_text = tk.Text(
            note_field,
            height=10, wrap="word", undo=True,
            bg=self.theme["input"], fg=self.theme["text"], insertbackground=self.theme["text"],
            selectbackground=self.theme["selection"], selectforeground="#FFFFFF",
            relief="flat", bd=0, highlightthickness=0, font=("TkDefaultFont", 11),
            padx=self.FIELD_PAD_X, pady=self.FIELD_PAD_Y,
        )
        note_text.pack(fill="both", expand=True)
        note_text.insert("1.0", str(note_value or ""))

        tk.Label(
            container,
            text=f"Freier Bereich für längere Informationen – zählt nicht als Listenpunkt. Speichern: {self.accel('Enter')}",
            bg=self.theme["bg"], fg=self.theme["placeholder"], font=("TkDefaultFont", 8), anchor="w",
        ).pack(anchor="w", pady=(6, 0))

        footer = tk.Frame(container, bg=self.theme["bg"])
        footer.pack(fill="x", pady=(16, 0))

        def submit(event=None):
            new_title = title_entry.get().strip() if title_editable else str(title_value or "")
            if title_editable and not new_title:
                messagebox.showwarning("Hinweis", "Bitte einen Titel eingeben.", parent=dialog)
                title_entry.focus_set()
                return "break"
            result["value"] = {"title": new_title, "note": note_text.get("1.0", "end-1c")}
            dialog.destroy()
            return "break"

        def cancel(event=None):
            dialog.destroy()
            return "break"

        self._make_dialog_button(footer, "Speichern", submit, "confirm").pack(side="right")
        self._make_dialog_button(footer, "Abbrechen", cancel, "muted").pack(side="right", padx=(0, 10))
        dialog.bind("<Control-Return>", submit)
        if IS_MACOS:
            dialog.bind("<Command-Return>", submit)
        dialog.bind("<Escape>", cancel)
        dialog.protocol("WM_DELETE_WINDOW", cancel)
        self._center_dialog(dialog, min_width=640)
        self._schedule_windows_chrome_theme(dialog)
        if title_editable:
            title_entry.focus_set()
            title_entry.select_range(0, tk.END)
        else:
            note_text.focus_set()
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

    def themed_choice_dialog(self, title, prompt, choices, item_colors=None):
        """Kleine modale Auswahl; choices enthält (Wert, sichtbarer Text).

        ``item_colors`` färbt jede Zeile einzeln ein – eine ``tk.Listbox`` kann
        das im Gegensatz zu einer ``ttk.Treeview``-Zelle. So zeigt die
        Farbauswahl jede Farbe tatsächlich in ihrer Farbe.
        """
        if not choices:
            return None
        result = {"value": None}
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.configure(bg=self.theme["bg"])
        dialog.transient(self.root)
        dialog.resizable(False, False)
        container = tk.Frame(dialog, bg=self.theme["bg"])
        container.pack(fill="both", expand=True, padx=self.DIALOG_PAD_X, pady=self.DIALOG_PAD_Y)
        tk.Label(
            container, text=title, bg=self.theme["bg"], fg=self.theme["text"],
            font=("TkDefaultFont", 15, "bold"), anchor="w",
        ).pack(anchor="w", pady=(0, 6))
        tk.Label(
            container, text=prompt, bg=self.theme["bg"], fg=self.theme["muted"],
            font=("TkDefaultFont", 10), anchor="w", justify="left",
        ).pack(anchor="w", pady=(0, 12))
        list_border, list_field = self._make_field(container)
        list_border.pack(fill="both", expand=True)
        list_field.pack(fill="both", expand=True, padx=self.FIELD_BORDER_WIDTH, pady=self.FIELD_BORDER_WIDTH)
        listbox = tk.Listbox(
            list_field,
            height=min(9, max(3, len(choices))), width=48,
            bg=self.theme["input"], fg=self.theme["text"],
            selectbackground=self.theme["selection"], selectforeground="#FFFFFF",
            activestyle="none", relief="flat", bd=0, highlightthickness=0,
            font=("TkDefaultFont", 10),
        )
        listbox.pack(fill="both", expand=True, padx=self.FIELD_PAD_X, pady=self.FIELD_PAD_Y)
        for index, (_value, label) in enumerate(choices):
            listbox.insert(tk.END, label)
            if item_colors:
                color_key = item_colors[index] if index < len(item_colors) else None
                if color_key:
                    try:
                        listbox.itemconfig(
                            index,
                            foreground=self.theme.get(color_key, color_key),
                            selectforeground="#FFFFFF",
                        )
                    except tk.TclError:
                        pass
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

    # -----------------------------
    # Labelverwaltung
    # -----------------------------
    def open_label_manager(self, event=None):
        """Zentrale Verwaltung: Labels anlegen, umbenennen, einfärben, entfernen."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Labels")
        dialog.configure(bg=self.theme["bg"])
        dialog.transient(self.root)
        dialog.minsize(560, 480)

        container = tk.Frame(dialog, bg=self.theme["bg"])
        container.pack(fill="both", expand=True, padx=self.DIALOG_PAD_X, pady=self.DIALOG_PAD_Y)
        tk.Label(
            container, text="Labels", bg=self.theme["bg"], fg=self.theme["text"],
            font=("TkDefaultFont", 16, "bold"), anchor="w",
        ).pack(anchor="w", pady=(0, 6))
        tk.Label(
            container,
            text=(
                "Labels sind unabhängig von der Aufgabenfarbe. Sie werden im Rechtsklickmenü eines Punkts "
                "zugewiesen und stehen in der Liste rechts neben der Fälligkeit."
            ),
            bg=self.theme["bg"], fg=self.theme["muted"], font=("TkDefaultFont", 10),
            anchor="w", justify="left", wraplength=520,
        ).pack(anchor="w", pady=(0, 14))

        list_border, list_field = self._make_field(container)
        list_border.pack(fill="both", expand=True)
        list_field.pack(fill="both", expand=True, padx=self.FIELD_BORDER_WIDTH, pady=self.FIELD_BORDER_WIDTH)
        listbox = tk.Listbox(
            list_field,
            height=10,
            bg=self.theme["input"], fg=self.theme["text"],
            selectbackground=self.theme["selection"], selectforeground="#FFFFFF",
            activestyle="none", relief="flat", bd=0, highlightthickness=0,
            font=("TkDefaultFont", 10),
        )
        listbox.pack(fill="both", expand=True, padx=self.FIELD_PAD_X, pady=self.FIELD_PAD_Y)

        def render(select_index=None):
            listbox.delete(0, tk.END)
            for index, label in enumerate(self.labels):
                usage = self.count_label_usage(label.get("id"))
                color_name = self.LABEL_COLOR_NAMES.get(self.label_color_key(label), "")
                listbox.insert(
                    tk.END,
                    f"{label.get('name', '')}   ·   {color_name}   ·   {usage}\u00d7 verwendet",
                )
                # Eine Listbox kann – anders als eine ttk.Treeview-Zelle – jede
                # Zeile einzeln einfärben. Die Labelfarbe ist hier deshalb auf
                # jeder Plattform sichtbar, unabhängig von der Emoji-Schrift.
                try:
                    listbox.itemconfig(
                        index,
                        foreground=self.theme[self.label_color_key(label)],
                        selectforeground="#FFFFFF",
                    )
                except tk.TclError:
                    pass
            if self.labels:
                index = min(select_index if select_index is not None else 0, len(self.labels) - 1)
                listbox.selection_set(index)
                listbox.activate(index)

        def selected_index():
            selection = listbox.curselection()
            return int(selection[0]) if selection else None

        def add_label():
            if len(self.labels) >= self.MAX_LABELS:
                messagebox.showinfo("Labels", f"Es sind höchstens {self.MAX_LABELS} Labels möglich.", parent=dialog)
                return
            name = self.themed_input_dialog("Neues Label", "Name des Labels:", ok_text="Anlegen")
            if name is None:
                return
            name = name.strip()[: self.MAX_LABEL_NAME_LENGTH]
            if not name:
                messagebox.showwarning("Hinweis", "Bitte einen Namen eingeben.", parent=dialog)
                return
            if self.get_label_by_name(name):
                messagebox.showwarning("Hinweis", "Es gibt bereits ein Label mit diesem Namen.", parent=dialog)
                return
            color = self.choose_label_color()
            self.snapshot_undo()
            self.labels.append(self.new_label_object(name, None, color))
            self.save_items()
            self.refresh_tree()
            render(len(self.labels) - 1)

        def rename_label():
            index = selected_index()
            if index is None:
                return
            label = self.labels[index]
            name = self.themed_input_dialog(
                "Label umbenennen", "Neuer Name:", initial=label.get("name", ""), ok_text="Speichern"
            )
            if name is None:
                return
            name = name.strip()[: self.MAX_LABEL_NAME_LENGTH]
            if not name:
                messagebox.showwarning("Hinweis", "Bitte einen Namen eingeben.", parent=dialog)
                return
            existing = self.get_label_by_name(name)
            if existing is not None and existing is not label:
                messagebox.showwarning("Hinweis", "Es gibt bereits ein Label mit diesem Namen.", parent=dialog)
                return
            if name == label.get("name"):
                return
            self.snapshot_undo()
            label["name"] = name
            self.save_items()
            self.refresh_tree()
            render(index)

        def recolor_label():
            index = selected_index()
            if index is None:
                return
            label = self.labels[index]
            color = self.choose_label_color(self.label_color_key(label))
            if color is None or color == self.label_color_key(label):
                return
            self.snapshot_undo()
            label["color"] = color
            self.save_items()
            self.refresh_tree()
            render(index)

        def remove_label():
            index = selected_index()
            if index is None:
                return
            label = self.labels[index]
            usage = self.count_label_usage(label.get("id"))
            if not messagebox.askyesno(
                "Label entfernen",
                f"Label '{label.get('name', '')}' entfernen?\n\n"
                f"Es wird von {usage} Punkt(en) gelöst; die Punkte selbst bleiben unverändert.",
                parent=dialog,
            ):
                return
            self.snapshot_undo()
            self.labels = [entry for entry in self.labels if entry.get("id") != label.get("id")]
            self.prune_unknown_item_labels()
            self.save_items()
            self.refresh_tree()
            render(max(0, index - 1))

        action_row = tk.Frame(container, bg=self.theme["bg"])
        action_row.pack(fill="x", pady=(10, 0))
        self._make_dialog_button(action_row, "+ Label", add_label, "confirm", width=104, height=36).pack(side="left")
        self._make_dialog_button(action_row, "Umbenennen", rename_label, "accent", width=112, height=36).pack(side="left", padx=(8, 0))
        self._make_dialog_button(action_row, "Farbe", recolor_label, "due_action", width=96, height=36).pack(side="left", padx=(8, 0))
        self._make_dialog_button(action_row, "Entfernen", remove_label, "delete", width=104, height=36).pack(side="left", padx=(8, 0))
        listbox.bind("<Double-Button-1>", lambda _event: rename_label())
        render()

        footer = tk.Frame(container, bg=self.theme["bg"])
        footer.pack(fill="x", pady=(16, 0))

        def close(event=None):
            dialog.destroy()
            return "break"

        self._make_dialog_button(footer, "Schließen", close, "muted").pack(side="right")
        dialog.bind("<Escape>", close)
        dialog.protocol("WM_DELETE_WINDOW", close)
        self._center_dialog(dialog, min_width=600)
        self._schedule_windows_chrome_theme(dialog)
        listbox.focus_set()
        dialog.grab_set()
        self.root.wait_window(dialog)
        return "break"

    def choose_label_color(self, current=None):
        """Farbauswahl eines Labels; None bedeutet Abbruch."""
        choices = [
            (key, ("\u2713  " if key == current else "     ") + name)
            for name, key in self.LABEL_COLOR_CHOICES
        ]
        return self.themed_choice_dialog(
            "Labelfarbe",
            "Welche Farbe soll das Label tragen?",
            choices,
            item_colors=[key for _name, key in self.LABEL_COLOR_CHOICES],
        )

    def toggle_label_on_selected_items(self, label_id):
        """Setzt oder entfernt ein Label für die aktuelle Auswahl im Aufgabenbaum."""
        if not self.require_list_view():
            return "break"
        label = self.get_label(label_id)
        if label is None:
            return "break"
        item_ids = self.get_selected_item_ids()
        if not item_ids:
            messagebox.showwarning("Hinweis", "Zuerst einen Punkt auswählen.")
            return "break"
        items = [self.find_item(item_id)[0] for item_id in item_ids if self.find_item(item_id)]
        # Trägt bereits jeder ausgewählte Punkt das Label, wird es entfernt.
        should_add = not all(label_id in (item.get("labels") or []) for item in items)
        self.snapshot_undo()
        changed = False
        for item in items:
            assigned = list(item.get("labels") or [])
            if should_add and label_id not in assigned:
                if len(assigned) >= self.MAX_LABELS_PER_ITEM:
                    continue
                assigned.append(label_id)
                changed = True
            elif not should_add and label_id in assigned:
                assigned = [value for value in assigned if value != label_id]
                changed = True
            item["labels"] = assigned
        if not changed:
            if self.undo_stack:
                self.undo_stack.pop()
            return "break"
        self.save_items()
        self.refresh_tree(selected_id=item_ids[-1])
        self._restore_item_selection(item_ids)
        return "break"

    def clear_labels_on_selected_items(self):
        if not self.require_list_view():
            return "break"
        item_ids = self.get_selected_item_ids()
        if not item_ids:
            return "break"
        self.snapshot_undo()
        changed = False
        for item_id in item_ids:
            found = self.find_item(item_id)
            if found and found[0].get("labels"):
                found[0]["labels"] = []
                changed = True
        if not changed:
            if self.undo_stack:
                self.undo_stack.pop()
            return "break"
        self.save_items()
        self.refresh_tree(selected_id=item_ids[-1])
        self._restore_item_selection(item_ids)
        return "break"

    def open_external_path(self, path):
        try:
            if not path or not os.path.exists(path):
                messagebox.showwarning("Datei öffnen", "Die Datei ist nicht mehr vorhanden.")
                return False
            if IS_WINDOWS:
                os.startfile(path)  # type: ignore[attr-defined]
            elif IS_MACOS:
                subprocess.Popen(["open", path])
            else:
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
        container.pack(fill="both", expand=True, padx=self.DIALOG_PAD_X, pady=self.DIALOG_PAD_Y)
        tk.Label(
            container,
            text="Punktdetails",
            bg=self.theme["bg"],
            fg=self.theme["text"],
            font=("TkDefaultFont", 16, "bold"),
            anchor="w",
        ).pack(anchor="w", pady=(0, 16))

        # Beschriftung, Feldkante und Textanfang folgen in allen drei Blöcken
        # derselben Regel: Label bündig am Container, Feldlinie bündig am
        # Container, Textanfang = Feldlinie + FIELD_PAD_X.
        self._make_field_label(container, "Titel").pack(anchor="w", pady=(0, self.FIELD_LABEL_GAP))
        title_border, title_field = self._make_field(container)
        title_border.pack(fill="x", pady=(0, 14))
        title_field.pack(fill="x", padx=self.FIELD_BORDER_WIDTH, pady=self.FIELD_BORDER_WIDTH)
        title_entry = tk.Entry(
            title_field,
            bg=self.theme["input"], fg=self.theme["text"], insertbackground=self.theme["text"],
            selectbackground=self.theme["selection"], selectforeground="#FFFFFF",
            relief="flat", bd=0, highlightthickness=0, font=("TkDefaultFont", 12),
        )
        title_entry.pack(fill="x", padx=self.FIELD_PAD_X, pady=self.FIELD_PAD_Y)
        title_entry.insert(0, item.get("text", ""))

        self._make_field_label(container, "Beschreibung").pack(anchor="w", pady=(0, self.FIELD_LABEL_GAP))
        description_border, description_field = self._make_field(container)
        description_border.pack(fill="both", expand=True, pady=(0, 14))
        description_field.pack(
            fill="both", expand=True, padx=self.FIELD_BORDER_WIDTH, pady=self.FIELD_BORDER_WIDTH
        )
        description_text = tk.Text(
            description_field,
            height=8, wrap="word", undo=True,
            bg=self.theme["input"], fg=self.theme["text"], insertbackground=self.theme["text"],
            selectbackground=self.theme["selection"], selectforeground="#FFFFFF",
            relief="flat", bd=0, highlightthickness=0, font=("TkDefaultFont", 10),
            padx=self.FIELD_PAD_X, pady=self.FIELD_PAD_Y,
        )
        description_text.pack(fill="both", expand=True)
        description_text.insert("1.0", item.get("description", ""))

        attachment_heading = tk.Frame(container, bg=self.theme["bg"])
        attachment_heading.pack(fill="x", pady=(0, self.FIELD_LABEL_GAP))
        self._make_field_label(attachment_heading, "Anhänge").pack(side="left")
        tk.Label(
            attachment_heading,
            text="Bilder und andere Dateien werden als lokale Kopie gespeichert.",
            bg=self.theme["bg"], fg=self.theme["placeholder"], font=("TkDefaultFont", 8), anchor="e",
        ).pack(side="right")

        attachment_border, attachment_field = self._make_field(container)
        attachment_border.pack(fill="x")
        attachment_field.pack(fill="x", padx=self.FIELD_BORDER_WIDTH, pady=self.FIELD_BORDER_WIDTH)
        attachment_list = tk.Listbox(
            attachment_field,
            height=5,
            bg=self.theme["input"], fg=self.theme["text"],
            selectbackground=self.theme["selection"], selectforeground="#FFFFFF",
            activestyle="none", relief="flat", bd=0, highlightthickness=0,
            font=("TkDefaultFont", 9),
        )
        attachment_list.pack(fill="x", padx=self.FIELD_PAD_X, pady=self.FIELD_PAD_Y)

        def attachment_path(entry):
            if entry.get("pending_path"):
                return entry.get("pending_path")
            return self.resolve_attachment_path(entry)

        def render_attachments(select_index=None):
            attachment_list.delete(0, tk.END)
            for attachment in attachments:
                path = attachment_path(attachment)
                exists = bool(path and os.path.isfile(path))
                if exists:
                    try:
                        size = os.path.getsize(path)
                    except OSError:
                        size = attachment.get("size", 0)
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
            # Der Grab wird für den nativen Dateidialog kurz freigegeben. Unter
            # macOS bleibt ein modaler Toplevel-Grab sonst gelegentlich stehen.
            try:
                dialog.grab_release()
            except tk.TclError:
                pass
            try:
                paths = filedialog.askopenfilenames(title="Dateien oder Bilder anhängen", parent=dialog)
            finally:
                try:
                    dialog.grab_set()
                except tk.TclError:
                    pass
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
            newly_stored_paths = []
            for attachment in attachments:
                if attachment.get("pending_path"):
                    try:
                        stored = self.store_attachment(attachment["pending_path"])
                    except Exception as exc:
                        for stored_path in newly_stored_paths:
                            try:
                                os.remove(stored_path)
                            except OSError:
                                pass
                        messagebox.showerror(
                            "Anhang speichern",
                            f"'{attachment.get('name', 'Datei')}' konnte nicht gespeichert werden:\n{exc}",
                            parent=dialog,
                        )
                        return "break"
                    stored_path = self.resolve_attachment_path(stored)
                    if stored_path:
                        newly_stored_paths.append(stored_path)
                    stored_attachments.append(stored)
                    continue
                stored = copy.deepcopy(attachment)
                stored_path = self.resolve_attachment_path(stored)
                if stored_path and os.path.isfile(stored_path):
                    try:
                        stored["size"] = os.path.getsize(stored_path)
                    except OSError:
                        pass
                stored_attachments.append(stored)
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
        if IS_MACOS:
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
    # Kalenderansicht
    # -----------------------------
    def calendar_week_start(self, reference=None):
        """Montag der Woche, in der das Referenzdatum liegt."""
        day = reference or date.today()
        return day - timedelta(days=day.weekday())

    def calendar_month_grid(self, year, month):
        """Erster und letzter Tag des montagsausgerichteten Rasters eines Monats.

        Das Raster beginnt am Montag der Woche, in der der Monatserste liegt,
        und endet am Sonntag der Woche des Monatsletzten. Für September 2026
        ergibt das genau fünf Wochen vom 31.08. bis zum 04.10.
        """
        first_of_month = date(year, month, 1)
        last_day_number = calendar.monthrange(year, month)[1]
        last_of_month = date(year, month, last_day_number)
        first_day = self.calendar_week_start(first_of_month)
        last_day = self.calendar_week_start(last_of_month) + timedelta(days=6)
        return first_day, last_day

    @staticmethod
    def shift_month(year, month, delta):
        index = (year * 12 + month - 1) + delta
        return index // 12, index % 12 + 1

    def collect_due_tasks_by_date(self, first_day, last_day):
        """Alle Aufgaben mit Fälligkeit im Zeitraum, gruppiert nach Tag.

        Rückgabe: {date: [(Aufgabe, Quellliste), …]} – sortiert nach Wichtigkeit
        (absteigend) und Titel, damit die Tageszelle stabil bleibt.
        """
        buckets = {}
        for entry in self.lists:
            for item in self.walk_items(entry.get("items", [])):
                if self.is_group_item(item):
                    continue
                iso_value = self.normalize_due(item.get("due"))
                if not iso_value:
                    continue
                try:
                    due_date = date.fromisoformat(iso_value)
                except ValueError:
                    continue
                if due_date < first_day or due_date > last_day:
                    continue
                buckets.setdefault(due_date, []).append((item, entry))
        for tasks in buckets.values():
            tasks.sort(
                key=lambda pair: (
                    1 if pair[0].get("done") else 0,
                    -self.clamp_importance(pair[0].get("importance", 0)),
                    str(pair[0].get("text", "")).lower(),
                )
            )
        return buckets

    def open_calendar_view(self, event=None):
        """Kalender mit umschaltbarer Wochen- und Monatsansicht.

        Monatsansicht: das montagsausgerichtete Raster des Referenzmonats,
        Navigation in ganzen Monaten, Tage benachbarter Monate ausgegraut.
        Wochenansicht: genau eine Woche von Montag bis Sonntag über die volle
        Höhe, damit auch viele Aufgaben an einem Tag Platz finden.
        """
        today = date.today()
        state = {
            "mode": self.CALENDAR_MODE_MONTH,
            "year": today.year,
            "month": today.month,
            "week_start": self.calendar_week_start(today),
        }
        jump_target = {"list_id": None, "item_id": None}

        dialog = tk.Toplevel(self.root)
        dialog.title("Kalender")
        dialog.configure(bg=self.theme["bg"])
        dialog.transient(self.root)
        dialog.minsize(980, 660)

        container = tk.Frame(dialog, bg=self.theme["bg"])
        container.pack(fill="both", expand=True, padx=self.DIALOG_PAD_X, pady=self.DIALOG_PAD_Y)

        header = tk.Frame(container, bg=self.theme["bg"])
        header.pack(fill="x", pady=(0, 4))
        # Statt des festen Worts "Kalender" steht hier der dargestellte Monat.
        title_label = tk.Label(
            header, text="", bg=self.theme["bg"], fg=self.theme["text"],
            font=("TkDefaultFont", 16, "bold"), anchor="w",
        )
        title_label.pack(side="left")
        range_label = tk.Label(
            header, text="", bg=self.theme["bg"], fg=self.theme["muted"],
            font=("TkDefaultFont", 10), anchor="e",
        )
        range_label.pack(side="right")

        nav = tk.Frame(container, bg=self.theme["bg"])
        nav.pack(fill="x", pady=(0, 12))

        grid_wrap = tk.Frame(container, bg=self.theme["bg"])
        grid_wrap.pack(fill="both", expand=True)
        cells = {"frame": None}
        mode_buttons = {}
        cell_bindings = []

        def restore_grab():
            """Der Kalender bleibt nach einem eingeblendeten Dialog modal."""
            try:
                dialog.grab_set()
            except tk.TclError:
                pass

        def add_task_on_day(day):
            """Doppelklick auf einen Tag: neue Aufgabe mit genau dieser Fälligkeit."""
            if self.add_task_with_due(day, parent_dialog=dialog, restore_grab=restore_grab):
                render()

        def open_task(item, source_list):
            jump_target["list_id"] = source_list.get("id")
            jump_target["item_id"] = item.get("id")
            dialog.destroy()

        def show_day(day, tasks):
            if not tasks:
                return
            choices = [
                (
                    item.get("id"),
                    f"{self.IMPORTANCE_MARKERS.get(self.clamp_importance(item.get('importance', 0)), '')}"
                    f"{'✓ ' if item.get('done') else ''}{item.get('text', '')}"
                    f"   ·   {str(source.get('title') or 'Liste')}",
                )
                for item, source in tasks
            ]
            try:
                dialog.grab_release()
            except tk.TclError:
                pass
            try:
                chosen = self.themed_choice_dialog(
                    day.strftime("%d.%m.%Y"), "Welche Aufgabe soll geöffnet werden?", choices
                )
            finally:
                restore_grab()
            if not chosen:
                return
            for item, source in tasks:
                if item.get("id") == chosen:
                    open_task(item, source)
                    return

        def current_range():
            """Zeitraum und Referenzmonat der aktuellen Ansicht."""
            if state["mode"] == self.CALENDAR_MODE_WEEK:
                first_day = state["week_start"]
                last_day = first_day + timedelta(days=6)
                # Der Donnerstag entscheidet, zu welchem Monat eine Woche zählt.
                reference = first_day + timedelta(days=3)
                return first_day, last_day, reference.year, reference.month
            first_day, last_day = self.calendar_month_grid(state["year"], state["month"])
            return first_day, last_day, state["year"], state["month"]

        def task_foreground(item, day, is_today, in_month):
            color_key = item.get("color") if item.get("color") in self.ITEM_COLOR_KEYS else None
            if item.get("done"):
                return self.theme["muted"]
            if color_key:
                return self.theme[color_key]
            if day < today:
                return self.theme["overdue"]
            if is_today:
                return self.theme["due_today"]
            return self.theme["text"] if in_month else self.theme["placeholder"]

        def build_day_cell(parent, day, tasks, reference_month, max_tasks, task_font_size):
            is_today = day == today
            in_month = day.month == reference_month
            # Tage benachbarter Monate bleiben sichtbar, treten aber zurück.
            surface = self.theme["card"] if in_month else self.theme["bg"]
            base_outline = self.theme["accent"] if is_today else self.theme["line"]
            cell = tk.Frame(
                parent,
                bg=surface,
                highlightthickness=2 if is_today else 1,
                highlightbackground=base_outline,
                highlightcolor=base_outline,
            )

            def set_outline(color):
                try:
                    cell.configure(highlightbackground=color, highlightcolor=color)
                except tk.TclError:
                    pass

            def pointer_inside():
                try:
                    pointer_x = cell.winfo_pointerx() - cell.winfo_rootx()
                    pointer_y = cell.winfo_pointery() - cell.winfo_rooty()
                except tk.TclError:
                    return False
                return 0 <= pointer_x < cell.winfo_width() and 0 <= pointer_y < cell.winfo_height()

            def on_enter(_event=None):
                set_outline(self.theme["calendar_hover"])

            def on_leave(_event=None):
                # Der Zeiger wechselt beim Überfahren zwischen Zelle und
                # Beschriftungen; ohne diese Prüfung würde die Umrandung dabei
                # flackern.
                if not pointer_inside():
                    set_outline(base_outline)

            def on_double_click(_event=None):
                add_task_on_day(day)
                return "break"

            def bind_cell_events(widget):
                widget.bind("<Enter>", on_enter, add="+")
                widget.bind("<Leave>", on_leave, add="+")
                widget.bind("<Double-Button-1>", on_double_click, add="+")

            bind_cell_events(cell)
            cell_bindings.append(bind_cell_events)
            day_row = tk.Frame(cell, bg=surface)
            day_row.pack(fill="x", padx=6, pady=(5, 2))
            bind_cell_events(day_row)
            if is_today:
                day_fg = self.theme["accent"]
            elif in_month:
                day_fg = self.theme["text"]
            else:
                day_fg = self.theme["placeholder"]
            day_number = tk.Label(
                day_row, text=str(day.day), bg=surface, fg=day_fg,
                font=("TkDefaultFont", 11, "bold"),
            )
            day_number.pack(side="left")
            bind_cell_events(day_number)
            if day.day == 1 or not in_month:
                month_hint = tk.Label(
                    day_row, text=self.MONTHS_DE[day.month - 1][:3],
                    bg=surface, fg=self.theme["placeholder"], font=("TkDefaultFont", 8),
                )
                month_hint.pack(side="right")
                bind_cell_events(month_hint)

            wrapping = state["mode"] == self.CALENDAR_MODE_WEEK
            task_labels = []
            for item, source in tasks[:max_tasks]:
                prefix = "✓ " if item.get("done") else self.IMPORTANCE_MARKERS.get(
                    self.clamp_importance(item.get("importance", 0)), ""
                )
                text = f"{prefix}{item.get('text', '')}"
                if not wrapping and len(text) > self.CALENDAR_MONTH_TEXT_MAX_CHARS:
                    text = text[: self.CALENDAR_MONTH_TEXT_MAX_CHARS - 1].rstrip() + "…"
                task_label = tk.Label(
                    cell,
                    text=text,
                    bg=surface, fg=task_foreground(item, day, is_today, in_month),
                    font=("TkDefaultFont", task_font_size), anchor="w", justify="left", cursor="hand2",
                )
                task_label.pack(fill="x", padx=6, pady=(0, 2))
                task_label.bind("<Button-1>", lambda _e, i=item, s=source: open_task(i, s))
                # Hover gilt für die ganze Zelle; der Doppelklick auf eine
                # Aufgabe legt bewusst keinen neuen Punkt an.
                task_label.bind("<Enter>", on_enter, add="+")
                task_label.bind("<Leave>", on_leave, add="+")
                task_labels.append(task_label)
            if wrapping and task_labels:
                # In der hohen Wochenzelle ist Platz für mehrere Zeilen; der
                # Umbruch richtet sich nach der tatsächlichen Zellenbreite.
                def rewrap(event, widgets=task_labels):
                    width = max(60, event.width - 16)
                    for widget in widgets:
                        try:
                            widget.configure(wraplength=width)
                        except tk.TclError:
                            pass
                cell.bind("<Configure>", rewrap, add="+")
            if len(tasks) > max_tasks:
                more = tk.Label(
                    cell, text=f"+{len(tasks) - max_tasks} weitere",
                    bg=surface, fg=self.theme["muted"],
                    font=("TkDefaultFont", task_font_size, "bold"), anchor="w", cursor="hand2",
                )
                more.pack(fill="x", padx=6)
                more.bind("<Button-1>", lambda _e, d=day, t=tasks: show_day(d, t))
                more.bind("<Enter>", on_enter, add="+")
                more.bind("<Leave>", on_leave, add="+")
            return cell

        def render():
            first_day, last_day, reference_year, reference_month = current_range()
            buckets = self.collect_due_tasks_by_date(first_day, last_day)
            total = sum(len(tasks) for tasks in buckets.values())
            title_label.configure(text=f"{self.MONTHS_DE[reference_month - 1]} {reference_year}")
            range_label.configure(
                text=f"{first_day.strftime('%d.%m.%Y')} – {last_day.strftime('%d.%m.%Y')}   ·   "
                     f"{total} Aufgabe(n) mit Fälligkeit"
            )
            for mode, button in mode_buttons.items():
                active = mode == state["mode"]
                button.set_active(self.theme["accent"] if active else None, "#FFFFFF")
            if cells["frame"] is not None:
                cells["frame"].destroy()
            frame = tk.Frame(grid_wrap, bg=self.theme["bg"])
            frame.pack(fill="both", expand=True)
            cells["frame"] = frame
            for column in range(7):
                frame.columnconfigure(column, weight=1, uniform="calendar")

            for column, name in enumerate(self.WEEKDAYS_DE):
                tk.Label(
                    frame, text=name, bg=self.theme["bg"], fg=self.theme["muted"],
                    font=("TkDefaultFont", 9, "bold"),
                ).grid(row=0, column=column, padx=2, pady=(0, 6), sticky="ew")

            week_count = ((last_day - first_day).days + 1) // 7
            for row in range(1, week_count + 1):
                frame.rowconfigure(row, weight=1, uniform="calendar_rows")
            if state["mode"] == self.CALENDAR_MODE_WEEK:
                max_tasks, task_font_size = self.CALENDAR_MAX_TASKS_PER_WEEK_DAY, 9
            else:
                max_tasks, task_font_size = self.CALENDAR_MAX_TASKS_PER_DAY, 8

            for week in range(week_count):
                for weekday in range(7):
                    day = first_day + timedelta(days=week * 7 + weekday)
                    cell = build_day_cell(
                        frame, day, buckets.get(day, []), reference_month, max_tasks, task_font_size
                    )
                    cell.grid(row=week + 1, column=weekday, padx=3, pady=3, sticky="nsew")
                    cell.grid_propagate(False)

        def shift(delta):
            if state["mode"] == self.CALENDAR_MODE_WEEK:
                state["week_start"] = state["week_start"] + timedelta(weeks=delta)
            else:
                state["year"], state["month"] = self.shift_month(state["year"], state["month"], delta)
            render()

        def set_mode(mode):
            if mode == state["mode"]:
                # Erneuter Klick springt zurück auf den heutigen Zeitraum.
                jump_to_today()
                return
            if mode == self.CALENDAR_MODE_WEEK:
                # Beim Wechsel die Woche im gerade gezeigten Monat behalten.
                first_day, _last, _y, _m = current_range()
                anchor = today if first_day <= today <= first_day + timedelta(days=41) else date(
                    state["year"], state["month"], 1
                )
                state["week_start"] = self.calendar_week_start(anchor)
            else:
                anchor = state["week_start"] + timedelta(days=3)
                state["year"], state["month"] = anchor.year, anchor.month
            state["mode"] = mode
            render()

        def jump_to_today():
            state["year"], state["month"] = today.year, today.month
            state["week_start"] = self.calendar_week_start(today)
            render()

        self._make_dialog_button(nav, "\u2039", lambda: shift(-1), "muted", width=52, height=36).pack(side="left")
        self._make_dialog_button(nav, "\u203a", lambda: shift(1), "muted", width=52, height=36).pack(side="left", padx=(8, 0))
        mode_buttons[self.CALENDAR_MODE_WEEK] = self._make_dialog_button(
            nav, "Diese Woche", lambda: set_mode(self.CALENDAR_MODE_WEEK), "accent", width=124, height=36
        )
        mode_buttons[self.CALENDAR_MODE_WEEK].pack(side="left", padx=(16, 0))
        mode_buttons[self.CALENDAR_MODE_MONTH] = self._make_dialog_button(
            nav, "Dieser Monat", lambda: set_mode(self.CALENDAR_MODE_MONTH), "accent", width=124, height=36
        )
        mode_buttons[self.CALENDAR_MODE_MONTH].pack(side="left", padx=(8, 0))
        self._make_dialog_button(nav, "Heute", jump_to_today, "confirm", width=92, height=36).pack(side="left", padx=(16, 0))
        tk.Label(
            nav,
            text="Klick auf eine Aufgabe öffnet sie in ihrer Liste · Doppelklick auf einen Tag legt dort eine Aufgabe an",
            bg=self.theme["bg"], fg=self.theme["placeholder"], font=("TkDefaultFont", 8),
        ).pack(side="right")

        render()

        footer = tk.Frame(container, bg=self.theme["bg"])
        footer.pack(fill="x", pady=(14, 0))

        def close(event=None):
            dialog.destroy()
            return "break"

        self._make_dialog_button(footer, "Schließen", close, "muted").pack(side="right")
        dialog.bind("<Escape>", close)
        dialog.bind("<Left>", lambda _e: shift(-1))
        dialog.bind("<Right>", lambda _e: shift(1))
        dialog.protocol("WM_DELETE_WINDOW", close)
        self._center_dialog(dialog, min_width=1000)
        self._schedule_windows_chrome_theme(dialog)
        dialog.grab_set()
        self.root.wait_window(dialog)

        if jump_target["list_id"]:
            self.open_task_in_source_list(jump_target["list_id"], jump_target["item_id"])
        return "break"

    def add_task_with_due(self, day, parent_dialog=None, restore_grab=None):
        """Legt eine Aufgabe mit fester Fälligkeit an; Rückgabe: wurde etwas angelegt.

        Wird vom Kalender genutzt und ist bewusst eine eigene Methode, damit der
        Weg unabhängig vom Dialog geprüft werden kann.
        """
        target = self.calendar_target_list()
        if target is None:
            messagebox.showinfo(
                "Neue Aufgabe",
                "Es gibt noch keine Liste, in der die Aufgabe angelegt werden könnte.",
            )
            return False
        title = str(target.get("title") or "Liste").strip() or "Liste"
        if parent_dialog is not None:
            try:
                parent_dialog.grab_release()
            except tk.TclError:
                pass
        try:
            text = self.themed_input_dialog(
                f"Neue Aufgabe am {day.strftime('%d.%m.%Y')}",
                f"Die Aufgabe entsteht in der Liste „{title}“ und erhält diese Fälligkeit.",
                ok_text="Anlegen",
            )
        finally:
            if callable(restore_grab):
                restore_grab()
        if text is None:
            return False
        text = text.strip()
        if not text:
            return False
        self.snapshot_undo()
        new_entry = self.new_item(text, False, due=day.isoformat())
        target.setdefault("items", []).append(new_entry)
        if target.get("id") == self.active_list_id:
            self.items = target["items"]
        self.save_items()
        self.refresh_tree()
        return True

    def calendar_target_list(self):
        """Liste, in der eine im Kalender angelegte Aufgabe entsteht.

        Das ist die geöffnete Liste; steht gerade eine Ordnerübersicht, „In
        Bearbeitung“ oder der Papierkorb im Hauptbereich, übernimmt der Eingang.
        """
        if self.view_mode == "list":
            current = next((entry for entry in self.lists if entry.get("id") == self.active_list_id), None)
            if current is not None:
                return current
        inbox = next((entry for entry in self.lists if self.is_inbox_list(entry)), None)
        if inbox is not None:
            return inbox
        return self.lists[0] if self.lists else None

    def open_task_in_source_list(self, list_id, item_id):
        """Öffnet eine Aufgabe in ihrer Quellliste und klappt den Pfad dorthin auf."""
        if not any(entry.get("id") == list_id for entry in self.lists):
            return False
        self.set_active_list(list_id, refresh=False)
        self.update_sidebar_list()
        self.refresh_tree(selected_id=item_id)
        try:
            if item_id and self.tree.exists(item_id):
                parent_id = self.tree.parent(item_id)
                while parent_id:
                    self.tree.item(parent_id, open=True)
                    self.expanded_ids.add(parent_id)
                    self.collapsed_item_ids.discard(parent_id)
                    parent_id = self.tree.parent(parent_id)
                self.tree.selection_set(item_id)
                self.tree.focus(item_id)
                self.tree.see(item_id)
        except tk.TclError:
            pass
        self.save_settings()
        return True

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
        labels=None,
    ):
        title = (title or "Neue Liste").strip() or "Neue Liste"
        return {
            "id": list_id or uuid.uuid4().hex,
            "title": title,
            "folder_id": folder_id if isinstance(folder_id, str) and folder_id else None,
            "color": color if color in self.LIST_COLOR_KEYS else None,
            "note": str(note or ""),
            "system_role": "inbox" if system_role == "inbox" else None,
            # Auch Listen und Ordner tragen Labels. Angezeigt werden sie nur in
            # der großen Darstellung im Hauptbereich, nicht in der Seitenleiste.
            "labels": self.normalize_item_labels(labels),
            "items": items if isinstance(items, list) else [],
        }

    def new_folder_object(self, title=None, folder_id=None, color=None, note="", labels=None):
        title = (title or "Neuer Ordner").strip() or "Neuer Ordner"
        return {
            "id": folder_id or uuid.uuid4().hex,
            "title": title,
            "color": color if color in self.LIST_COLOR_KEYS else None,
            "note": str(note or ""),
            "labels": self.normalize_item_labels(labels),
        }

    # -----------------------------
    # Labels
    # -----------------------------
    def new_label_object(self, name=None, label_id=None, color=None):
        clean_name = str(name or "Label").strip()[: self.MAX_LABEL_NAME_LENGTH] or "Label"
        return {
            "id": label_id or uuid.uuid4().hex,
            "name": clean_name,
            "color": self.resolve_label_color(color),
        }

    @classmethod
    def resolve_label_color(cls, color):
        """Gültiger Labelfarbschlüssel; Altwerte werden auf die Palette abgebildet."""
        if color in cls.LABEL_COLOR_KEYS:
            return color
        mapped = cls.LEGACY_LABEL_COLOR_MAP.get(color)
        if mapped in cls.LABEL_COLOR_KEYS:
            return mapped
        return cls.DEFAULT_LABEL_COLOR

    def get_label(self, label_id):
        if not isinstance(label_id, str) or not label_id:
            return None
        return next((label for label in self.labels if label.get("id") == label_id), None)

    def get_label_by_name(self, name):
        needle = str(name or "").strip().casefold()
        if not needle:
            return None
        return next(
            (label for label in self.labels if str(label.get("name") or "").strip().casefold() == needle),
            None,
        )

    def label_color_key(self, label):
        return self.resolve_label_color((label or {}).get("color"))

    def label_color(self, label):
        """Tatsächliche Farbe des Labels im aktuellen Theme."""
        return self.theme[self.label_color_key(label)]

    def item_labels(self, item):
        """Bekannte Labelobjekte eines Punkts in der Reihenfolge der Labelverwaltung.

        Funktioniert gleichermaßen für Aufgaben, Listen und Ordner, weil alle
        drei ihre Zuordnung im Feld ``labels`` führen.
        """
        assigned = item.get("labels") if isinstance(item, dict) else None
        if not isinstance(assigned, list) or not assigned:
            return []
        assigned_ids = {value for value in assigned if isinstance(value, str)}
        return [label for label in self.labels if label.get("id") in assigned_ids]

    def format_item_labels(self, item):
        """Anzeigetext der Labelspalte.

        Die Spalte hat eine feste Breite. Deshalb werden höchstens
        LABEL_COLUMN_MAX_VISIBLE Labels ausgeschrieben, der Rest als Zähler
        angehängt und lange Namen gekürzt. Der gespeicherte Name und alle
        Exporte bleiben davon unberührt.
        """
        labels = self.item_labels(item)
        if not labels:
            return ""
        visible = labels[: self.LABEL_COLUMN_MAX_VISIBLE]
        parts = []
        for label in visible:
            name = str(label.get("name", ""))
            if len(name) > self.LABEL_COLUMN_NAME_MAX_CHARS:
                name = name[: self.LABEL_COLUMN_NAME_MAX_CHARS - 1].rstrip() + "…"
            parts.append(name)
        text = self.LABEL_SEPARATOR.join(parts)
        remaining = len(labels) - len(visible)
        if remaining:
            text = f"{text}  +{remaining}"
        return text

    def format_item_label_names(self, item):
        """Reine Namen für Export und Zwischenablage."""
        return ", ".join(str(label.get("name", "")) for label in self.item_labels(item))

    def normalize_labels_data(self, data):
        """Bereinigt die Labelverwaltung: eindeutige IDs, gültige Farben, feste Obergrenze."""
        labels = []
        seen_ids = set()
        seen_names = set()
        if not isinstance(data, list):
            return labels
        for entry in data:
            if not isinstance(entry, dict):
                continue
            name = str(entry.get("name") or "").strip()[: self.MAX_LABEL_NAME_LENGTH]
            if not name:
                continue
            folded = name.casefold()
            if folded in seen_names:
                continue
            label_id = entry.get("id") if isinstance(entry.get("id"), str) and entry.get("id") else None
            while not label_id or label_id in seen_ids:
                label_id = uuid.uuid4().hex
            seen_ids.add(label_id)
            seen_names.add(folded)
            labels.append(self.new_label_object(name, label_id, entry.get("color")))
            if len(labels) >= self.MAX_LABELS:
                break
        return labels

    def normalize_item_labels(self, data, known_label_ids=None):
        """Hält nur bekannte Label-IDs, ohne Dubletten und in stabiler Reihenfolge."""
        if not isinstance(data, list):
            return []
        result = []
        for value in data:
            if not isinstance(value, str) or not value:
                continue
            if known_label_ids is not None and value not in known_label_ids:
                continue
            if value in result:
                continue
            result.append(value)
            if len(result) >= self.MAX_LABELS_PER_ITEM:
                break
        return result

    def prune_unknown_item_labels(self):
        """Entfernt Verweise auf gelöschte Labels überall im Bestand.

        Erfasst Aufgaben, Listen und Ordner – auch die Kopien im Papierkorb.
        """
        known = {label.get("id") for label in self.labels}
        changed = False

        def clean(holder):
            nonlocal changed
            assigned = holder.get("labels")
            if not isinstance(assigned, list):
                if assigned is not None:
                    holder["labels"] = []
                    changed = True
                return
            kept = [value for value in assigned if value in known]
            if kept != assigned:
                holder["labels"] = kept
                changed = True

        for holder in self.iter_label_holders():
            clean(holder)
        return changed

    def iter_all_list_objects(self):
        """Alle Listen inklusive der im Papierkorb liegenden Kopien."""
        for entry in self.lists:
            yield entry
        for trash_entry in self.trash:
            payload = trash_entry.get("list")
            if isinstance(payload, dict):
                yield payload

    def iter_all_folder_objects(self):
        """Alle Ordner inklusive der im Papierkorb liegenden Kopien."""
        for folder in self.folders:
            yield folder
        for trash_entry in self.trash:
            payload = trash_entry.get("folder")
            if isinstance(payload, dict):
                yield payload

    def iter_label_holders(self):
        """Jeder Datensatz, der Labels tragen kann: Ordner, Listen und Punkte."""
        for folder in self.iter_all_folder_objects():
            yield folder
        for entry in self.iter_all_list_objects():
            yield entry
            for item in self.walk_items(entry.get("items", [])):
                yield item

    def count_label_usage(self, label_id):
        """Wie oft ein Label vergeben ist – über Ordner, Listen und Punkte."""
        total = 0
        for holder in self.iter_label_holders():
            assigned = holder.get("labels")
            if isinstance(assigned, list) and label_id in assigned:
                total += 1
        return total

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
        self.collapsed_item_ids = set()
        self.selection_anchor_id = None
        self.update_window_title()
        self.update_header_title()
        self.update_page_note_preview()
        self.update_page_labels()
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
        self.collapsed_item_ids = set()
        self.selection_anchor_id = None
        self.update_window_title()
        self.update_header_title()
        self.update_page_note_preview()
        self.update_page_labels()
        self.update_entry_mode()
        if refresh:
            self.update_sidebar_list()
            self.refresh_tree()
            self.save_settings()

    def set_in_progress_view(self, refresh=True):
        """Öffnet die abgeleitete, datenformatfreie Ansicht aller fälligen Aufgaben."""
        self._activate_system_view("in_progress", refresh=refresh)

    def set_trash_view(self, refresh=True):
        """Öffnet den Papierkorb mit allen gelöschten Listen und Ordnern."""
        self._activate_system_view("trash", refresh=refresh)

    def _activate_system_view(self, mode, refresh=True):
        if self.active_list_id and self.lists:
            self.sync_current_list_reference()
        self.view_mode = mode
        self.active_folder_id = None
        self.expanded_ids = set()
        self.collapsed_item_ids = set()
        self.selection_anchor_id = None
        self.update_window_title()
        self.update_header_title()
        self.update_page_note_preview()
        self.update_page_labels()
        self.update_entry_mode()
        if refresh:
            self.update_sidebar_list()
            self.refresh_tree()
            self.save_settings()

    def create_list_sidebar(self):
        # Systembereich: Eingang, "In Bearbeitung" und Papierkorb sind bewusst
        # kein Bestandteil des normalen Listenbaums. Getrennt werden beide
        # Bereiche seit 2.7.2 durch ein Band in der Fensterfarbe – kein Rahmen,
        # keine Linie, sondern eine sichtbare graue Fläche mit Abstand.
        self.system_listbox = ttk.Treeview(
            self.sidebar_frame,
            show="tree",
            selectmode="browse",
            style="System.Treeview",
            takefocus=True,
            height=3,
        )
        self.system_listbox.pack(fill="x", pady=(4, 0))
        self.system_listbox.heading("#0", text="")
        self.system_listbox.column("#0", anchor="w", stretch=True, width=220)
        self.system_listbox.bind("<<TreeviewSelect>>", self.on_system_select)
        self.system_listbox.bind("<Button-3>", self.show_sidebar_context_menu)
        self.system_listbox.bind("<Button-2>", self.show_sidebar_context_menu)
        self.system_listbox.bind("<Control-Button-1>", self.show_sidebar_context_menu)
        self.system_listbox.bind("<Delete>", self.delete_selected_sidebar_entry)
        self.bind_mousewheel(self.system_listbox)

        # Das graue Band trennt Systembereich und Listenbereich sichtbar
        # voneinander; darüber und darunter bleibt zusätzlich Luft.
        self.sidebar_divider = self.register_theme_widget(
            tk.Frame(self.sidebar_frame, bg=self.theme["bg"], height=self.SIDEBAR_DIVIDER_HEIGHT),
            "bg",
        )
        self.sidebar_divider.pack(
            fill="x", pady=(self.SIDEBAR_SECTION_GAP, self.SIDEBAR_SECTION_GAP)
        )
        self.sidebar_divider.pack_propagate(False)

        title_row = self.register_theme_widget(tk.Frame(self.sidebar_frame, bg=self.theme["card"]), "card")
        title_row.pack(fill="x", pady=(0, 8))

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

        # "extended" erlaubt Shift- und Strg-Mehrfachauswahl. Alle Aktionen der
        # Seitenleiste arbeiten deshalb auf einer Auswahlmenge; bei genau einer
        # markierten Zeile bleibt das Verhalten identisch zu früheren Versionen.
        self.sidebar_listbox = ttk.Treeview(
            self.sidebar_frame,
            show="tree",
            selectmode="extended",
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
        # Gleiten statt greifen: die Auswahl lässt sich auch ohne Maus bewegen.
        self.sidebar_listbox.bind("<Alt-Up>", lambda event: self.move_sidebar_selection(-1))
        self.sidebar_listbox.bind("<Alt-Down>", lambda event: self.move_sidebar_selection(1))
        self.sidebar_listbox.bind("<Alt-Right>", self.toggle_sidebar_indent)
        self.sidebar_listbox.bind("<Alt-Left>", self.outdent_selected_sidebar_list)
        self.sidebar_listbox.bind("<Control-a>", self.select_all_sidebar_lists)
        # Entf löscht die Auswahl der Seitenleiste, nicht die des Aufgabenbaums.
        self.sidebar_listbox.bind("<Delete>", self.delete_selected_sidebar_entry)
        if IS_MACOS:
            self.sidebar_listbox.bind("<BackSpace>", self.delete_selected_sidebar_entry)
            self.system_listbox.bind("<BackSpace>", self.delete_selected_sidebar_entry)
        if IS_MACOS:
            self.bind_optional(self.sidebar_listbox, "<Command-a>", self.select_all_sidebar_lists)
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
            text="Bearbeiten",
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

    def _capture_sidebar_folder_open_states(self):
        """Merkt die Klappzustände, bevor der Seitenleistenbaum neu aufgebaut wird."""
        tree = getattr(self, "sidebar_listbox", None)
        if tree is None:
            return
        for folder in self.folders:
            folder_id = folder.get("id") if isinstance(folder, dict) else None
            iid = f"folder:{folder_id}" if folder_id else None
            try:
                if iid and tree.exists(iid):
                    self.sidebar_folder_open_states[folder_id] = bool(tree.item(iid, "open"))
            except tk.TclError:
                continue

    @classmethod
    def ellipsize_sidebar_title(cls, title):
        """Kürzt nur die Anzeige; der gespeicherte Titel bleibt vollständig erhalten."""
        clean_title = str(title or "").strip()
        if len(clean_title) <= cls.SIDEBAR_TITLE_MAX_CHARS:
            return clean_title
        return clean_title[: cls.SIDEBAR_TITLE_MAX_CHARS].rstrip() + "..."

    @classmethod
    def format_sidebar_preview(cls, title, item_count):
        return f"{cls.ellipsize_sidebar_title(title)}  ({item_count})"

    def update_sidebar_list(self):
        if not hasattr(self, "sidebar_listbox") or not hasattr(self, "system_listbox"):
            return
        self._capture_sidebar_folder_open_states()
        current_folder_ids = {
            folder.get("id")
            for folder in self.folders
            if isinstance(folder, dict) and folder.get("id")
        }
        self.sidebar_folder_open_states = {
            folder_id: self.sidebar_folder_open_states.get(folder_id, True)
            for folder_id in current_folder_ids
        }
        self._updating_sidebar = True
        try:
            self.sidebar_rows = []
            self.sidebar_iid_to_row = {}
            for row_id in self.system_listbox.get_children(""):
                self.system_listbox.delete(row_id)
            for row_id in self.sidebar_listbox.get_children(""):
                self.sidebar_listbox.delete(row_id)

            assigned_folder_ids = {folder.get("id") for folder in self.folders if isinstance(folder, dict)}

            # Der feste Eingang steht in seinem eigenen einzeiligen Feld.
            inbox = next((entry for entry in self.lists if self.is_inbox_list(entry)), None)
            if inbox:
                self._insert_sidebar_list_row(inbox, parent="", tree=self.system_listbox)
            due_count = sum(
                1
                for entry in self.lists
                for item in self.walk_items(entry.get("items", []))
                if not self.is_group_item(item) and self.normalize_due(item.get("due"))
            )
            self.system_listbox.insert(
                "",
                "end",
                iid=self.IN_PROGRESS_ROW_ID,
                text=self.format_sidebar_preview("In Bearbeitung", due_count),
                tags=("system",),
            )
            self.sidebar_rows.append(("view", "in_progress"))
            self.sidebar_iid_to_row[self.IN_PROGRESS_ROW_ID] = ("view", "in_progress")

            self.system_listbox.insert(
                "",
                "end",
                iid=self.TRASH_ROW_ID,
                text=self.format_sidebar_preview("Papierkorb", len(self.trash)),
                tags=("system",),
            )
            self.sidebar_rows.append(("view", "trash"))
            self.sidebar_iid_to_row[self.TRASH_ROW_ID] = ("view", "trash")

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
                preview = self.format_sidebar_preview(folder_title, len(child_lists))
                folder_color = folder.get("color") if folder.get("color") in self.LIST_COLOR_KEYS else None
                folder_tags = (f"listcolor_{folder_color}",) if folder_color else ("folder",)
                self.sidebar_listbox.insert(
                    "",
                    "end",
                    iid=iid,
                    text=preview,
                    open=self.sidebar_folder_open_states.get(folder_id, True),
                    tags=folder_tags,
                )
                self.sidebar_rows.append(("folder", folder_id))
                self.sidebar_iid_to_row[iid] = ("folder", folder_id)
                for entry in child_lists:
                    self._insert_sidebar_list_row(entry, parent=iid)

            inbox_selection = self.system_listbox.selection()
            if inbox_selection:
                self.system_listbox.selection_remove(*inbox_selection)
            sidebar_selection = self.sidebar_listbox.selection()
            if sidebar_selection:
                self.sidebar_listbox.selection_remove(*sidebar_selection)
            if self.view_mode == "in_progress":
                active_iid = self.IN_PROGRESS_ROW_ID
            elif self.view_mode == "trash":
                active_iid = self.TRASH_ROW_ID
            elif self.view_mode == "folder" and self.active_folder_id:
                active_iid = f"folder:{self.active_folder_id}"
            else:
                active_iid = f"list:{self.active_list_id}" if self.active_list_id else None
            if active_iid and self.system_listbox.exists(active_iid):
                self.system_listbox.selection_set(active_iid)
                self.system_listbox.focus(active_iid)
            elif active_iid and self.sidebar_listbox.exists(active_iid):
                self.sidebar_listbox.selection_set(active_iid)
                self.sidebar_listbox.focus(active_iid)
                self.sidebar_listbox.see(active_iid)
            elif self.system_listbox.get_children(""):
                first = self.system_listbox.get_children("")[0]
                self.system_listbox.selection_set(first)
                self.system_listbox.focus(first)
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
        preview = self.format_sidebar_preview(title, item_count)
        iid = f"list:{item_id}"
        if is_inbox:
            tags = ("system",)
        else:
            color_key = entry.get("color") if entry.get("color") in self.LIST_COLOR_KEYS else None
            tags = (f"listcolor_{color_key}",) if color_key else ("list",)
        target_tree.insert(parent, "end", iid=iid, text=preview, tags=tags)
        self.sidebar_rows.append(("list", item_id))
        self.sidebar_iid_to_row[iid] = ("list", item_id)

    def get_selected_sidebar_row(self):
        rows = self.get_selected_sidebar_rows()
        return rows[0] if rows else None

    def get_selected_sidebar_rows(self):
        """Alle markierten Seitenleistenzeilen in Anzeigereihenfolge.

        Der Systembereich kennt nur Einfachauswahl; der Listenbaum erlaubt seit
        2.7.0 Shift- und Strg-Mehrfachauswahl.
        """
        if not hasattr(self, "sidebar_listbox"):
            return []
        if hasattr(self, "system_listbox"):
            system_selection = self.system_listbox.selection()
            if system_selection:
                row = self.sidebar_iid_to_row.get(system_selection[0])
                return [row] if row else []
        selection = set(self.sidebar_listbox.selection())
        if not selection:
            return []
        rows = []
        for iid in self.get_sidebar_visible_iids():
            if iid in selection:
                row = self.sidebar_iid_to_row.get(iid)
                if row:
                    rows.append(row)
        if rows:
            return rows
        # Rückfallebene, falls eine markierte Zeile gerade zugeklappt ist.
        return [row for row in (self.sidebar_iid_to_row.get(iid) for iid in selection) if row]

    def get_selected_sidebar_list_ids(self, include_inbox=False):
        """IDs aller markierten Listen; Ordner und Systemzeilen bleiben außen vor."""
        ids = []
        for row_type, row_id in self.get_selected_sidebar_rows():
            if row_type != "list":
                continue
            if not include_inbox and self.is_inbox_list(row_id):
                continue
            if row_id not in ids:
                ids.append(row_id)
        return ids

    def select_all_sidebar_lists(self, event=None):
        """Markiert alle sichtbaren Zeilen des Listenbaums."""
        tree = getattr(self, "sidebar_listbox", None)
        if tree is None:
            return "break"
        visible = self.get_sidebar_visible_iids()
        if not visible:
            return "break"
        tree.selection_set(visible)
        return "break"

    def get_sidebar_iid_for_row(self, row):
        if not row:
            return None
        row_type, row_id = row
        if (row_type, row_id) == ("view", "in_progress"):
            return self.IN_PROGRESS_ROW_ID
        if (row_type, row_id) == ("view", "trash"):
            return self.TRASH_ROW_ID
        return f"{row_type}:{row_id}"

    def get_sidebar_tree_for_iid(self, iid):
        if not iid:
            return None
        for tree_name in ("system_listbox", "sidebar_listbox"):
            tree = getattr(self, tree_name, None)
            try:
                if tree is not None and tree.exists(iid):
                    return tree
            except tk.TclError:
                continue
        return None

    def on_system_select(self, event=None):
        if getattr(self, "_updating_sidebar", False):
            return
        selection = self.system_listbox.selection()
        if not selection:
            return
        sidebar_selection = self.sidebar_listbox.selection()
        if sidebar_selection:
            self.sidebar_listbox.selection_remove(*sidebar_selection)
        row = self.sidebar_iid_to_row.get(selection[0])
        if row and row[0] == "list" and (row[1] != self.active_list_id or self.view_mode != "list"):
            self.set_active_list(row[1])
        elif row == ("view", "in_progress") and self.view_mode != "in_progress":
            self.set_in_progress_view()
        elif row == ("view", "trash") and self.view_mode != "trash":
            self.set_trash_view()

    def on_sidebar_select(self, event=None):
        if getattr(self, "_updating_sidebar", False):
            return
        selection = self.sidebar_listbox.selection()
        if selection and hasattr(self, "system_listbox"):
            system_selection = self.system_listbox.selection()
            if system_selection:
                self.system_listbox.selection_remove(*system_selection)
        # Bei Mehrfachauswahl bleibt die geöffnete Seite unverändert; sonst
        # würde jede Bereichsauswahl ungewollt die Ansicht umschalten.
        if len(selection) > 1:
            return
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
        """Doppelklick und Titel-Schaltfläche öffnen den gemeinsamen Bearbeiten-Dialog."""
        row = self.get_selected_sidebar_row()
        if row and row[0] == "folder":
            return self.edit_folder_details(row[1])
        if row and row[0] == "list":
            return self.edit_list_details(row[1])
        return self.edit_title()

    def _add_color_menu(self, menu, heading, current, setter, target_id):
        """Farbauswahl als Untermenü – identisch für Listen und Ordner."""
        color_menu = self._new_themed_popup_menu(menu)
        for label, color_key in self.LIST_COLOR_CHOICES:
            prefix = "\u2713 " if current == color_key else "      "
            color_menu.add_command(
                label=f"{prefix}{label}",
                foreground=self.theme[color_key],
                command=lambda c=color_key: setter(target_id, c),
            )
        color_menu.add_separator()
        prefix = "\u2713 " if not current else "      "
        color_menu.add_command(label=f"{prefix}Keine Farbe", command=lambda: setter(target_id, None))
        menu.add_cascade(label=heading, menu=color_menu)
        return color_menu

    def _add_page_label_menu(self, menu, holder, kind):
        """Labels einer Liste oder eines Ordners zuweisen und lösen."""
        label_menu = self._new_themed_popup_menu(menu)
        assigned = list((holder or {}).get("labels") or [])
        holder_id = (holder or {}).get("id")
        if not self.labels:
            label_menu.add_command(label="Noch keine Labels angelegt", state="disabled")
        else:
            for label in self.labels:
                label_id = label.get("id")
                prefix = "\u2713 " if label_id in assigned else "     "
                label_menu.add_command(
                    label=f"{prefix}{label.get('name', '')}",
                    foreground=self.label_color(label),
                    command=lambda selected=label_id: self.toggle_page_label(kind, holder_id, selected),
                )
            label_menu.add_separator()
            label_menu.add_command(
                label="Alle Labels entfernen",
                command=lambda: self.clear_page_labels(kind, holder_id),
            )
        label_menu.add_separator()
        label_menu.add_command(label="Labels verwalten …", command=self.open_label_manager)
        menu.add_cascade(label="Labels", menu=label_menu)
        return label_menu

    def find_label_holder(self, kind, holder_id):
        collection = self.lists if kind == "list" else self.folders
        return next((entry for entry in collection if entry.get("id") == holder_id), None)

    def toggle_page_label(self, kind, holder_id, label_id):
        holder = self.find_label_holder(kind, holder_id)
        if holder is None or self.get_label(label_id) is None:
            return "break"
        assigned = list(holder.get("labels") or [])
        if label_id in assigned:
            assigned = [value for value in assigned if value != label_id]
        elif len(assigned) < self.MAX_LABELS_PER_ITEM:
            assigned.append(label_id)
        else:
            return "break"
        self.snapshot_undo()
        holder["labels"] = assigned
        self.save_items()
        self.update_page_labels()
        self.refresh_tree()
        return "break"

    def clear_page_labels(self, kind, holder_id):
        holder = self.find_label_holder(kind, holder_id)
        if holder is None or not holder.get("labels"):
            return "break"
        self.snapshot_undo()
        holder["labels"] = []
        self.save_items()
        self.update_page_labels()
        self.refresh_tree()
        return "break"

    def build_sidebar_context_menu(self, row, rows=None):
        """Vollständiges Kontextmenü für eine Liste, einen Ordner oder eine Systemzeile."""
        if rows and len(rows) > 1:
            return self.build_sidebar_multi_menu(rows)
        if not row:
            return None
        row_type, row_id = row
        if row_type == "view":
            return self.build_smart_view_menu(row_id)
        if row_type == "folder":
            return self.build_folder_menu(row_id)
        if row_type == "list":
            return self.build_list_menu(row_id)
        return None

    def build_sidebar_multi_menu(self, rows):
        """Kontextmenü für eine Mehrfachauswahl aus Listen und Ordnern."""
        list_ids = [row_id for row_type, row_id in rows if row_type == "list" and not self.is_inbox_list(row_id)]
        folder_ids = [row_id for row_type, row_id in rows if row_type == "folder"]
        menu = self._new_themed_popup_menu()
        menu.add_command(label=f"Auswahl: {len(list_ids)} Liste(n), {len(folder_ids)} Ordner", state="disabled")
        menu.add_separator()

        move_menu = self._new_themed_popup_menu(menu)
        for folder in self.folders:
            folder_id = folder.get("id")
            move_menu.add_command(
                label=str(folder.get("title") or "Ordner").strip() or "Ordner",
                command=lambda target=folder_id: self.move_selected_lists_to_folder(target),
            )
        if not self.folders:
            move_menu.add_command(label="Kein Ordner vorhanden", state="disabled")
        menu.add_cascade(
            label="In Ordner verschieben",
            menu=move_menu,
            state="normal" if list_ids and self.folders else "disabled",
        )
        menu.add_command(
            label="Aus Ordner herauslösen",
            command=lambda: self.move_selected_lists_to_folder(None),
            state="normal" if list_ids else "disabled",
        )
        menu.add_separator()

        color_menu = self._new_themed_popup_menu(menu)
        for label, color_key in self.LIST_COLOR_CHOICES:
            color_menu.add_command(
                label=label,
                foreground=self.theme[color_key],
                command=lambda selected=color_key: self.set_selected_sidebar_color(selected),
            )
        color_menu.add_separator()
        color_menu.add_command(label="Keine Farbe", command=lambda: self.set_selected_sidebar_color(None))
        menu.add_cascade(label="Farbe der Auswahl", menu=color_menu)
        menu.add_separator()
        menu.add_command(
            label="In den Papierkorb",
            command=self.trash_selected_sidebar_entries,
            foreground=self.theme["delete"],
            state="normal" if (list_ids or folder_ids) else "disabled",
        )
        return menu

    def build_list_menu(self, list_id):
        entry = next((item for item in self.lists if item.get("id") == list_id), None)
        if entry is None:
            return None
        is_inbox = self.is_inbox_list(entry)
        title = str(entry.get("title") or "Liste").strip() or "Liste"
        in_folder = bool(entry.get("folder_id"))

        menu = self._new_themed_popup_menu()
        menu.add_command(label=self.ellipsize_sidebar_title(title), state="disabled")
        menu.add_separator()
        menu.add_command(label="Öffnen", command=lambda: self.set_active_list(list_id))
        menu.add_command(
            label="Bearbeiten (Titel, Beschreibungstext) …",
            command=lambda: self.edit_list_details(list_id),
        )
        self._add_color_menu(menu, "Listenfarbe", entry.get("color"), self.set_list_color, list_id)
        self._add_page_label_menu(menu, entry, "list")
        menu.add_separator()

        create_menu = self._new_themed_popup_menu(menu)
        create_menu.add_command(label="Neue Liste …", command=self.create_new_list)
        create_menu.add_command(label="Neuer Ordner …", command=self.create_new_folder)
        menu.add_cascade(label="Neu anlegen", menu=create_menu)

        move_menu = self._new_themed_popup_menu(menu)
        move_menu.add_command(
            label="In Ordner verschieben …",
            command=lambda: self.move_list_to_folder_dialog(list_id),
            state="disabled" if is_inbox or not self.folders else "normal",
        )
        move_menu.add_command(
            label="Aus Ordner herauslösen",
            command=lambda: self.detach_list_from_folder(list_id),
            state="normal" if in_folder and not is_inbox else "disabled",
        )
        menu.add_cascade(label="Verschieben", menu=move_menu, state="disabled" if is_inbox else "normal")

        menu.add_command(
            label="Duplizieren",
            command=lambda: self.duplicate_list(list_id),
            state="disabled" if is_inbox else "normal",
        )

        export_menu = self._new_themed_popup_menu(menu)
        export_menu.add_command(label="Als TXT …", command=lambda: self.export_list_as(list_id, "txt"))
        export_menu.add_command(label="Als Markdown …", command=lambda: self.export_list_as(list_id, "md"))
        export_menu.add_command(label="Als CSV …", command=lambda: self.export_list_as(list_id, "csv"))
        menu.add_cascade(label="Exportieren", menu=export_menu)

        menu.add_separator()
        menu.add_command(
            label="Erledigte Punkte entfernen",
            command=lambda: self.remove_done_items(list_id),
        )
        menu.add_command(
            label="Liste leeren",
            command=lambda: self.clear_list_by_id(list_id),
            foreground=self.theme["delete"],
        )
        menu.add_command(
            label="In den Papierkorb",
            command=lambda: self.delete_list_by_id(list_id),
            foreground=self.theme["delete"],
            state="disabled" if is_inbox else "normal",
        )
        return menu

    def build_folder_menu(self, folder_id):
        folder = self.get_folder(folder_id)
        if folder is None:
            return None
        title = str(folder.get("title") or "Ordner").strip() or "Ordner"
        child_count = len(self.get_folder_lists(folder_id))

        menu = self._new_themed_popup_menu()
        menu.add_command(label=f"{self.ellipsize_sidebar_title(title)}  ({child_count})", state="disabled")
        menu.add_separator()
        menu.add_command(label="Öffnen", command=lambda: self.set_active_folder(folder_id))
        menu.add_command(
            label="Bearbeiten (Titel, Beschreibungstext) …",
            command=lambda: self.edit_folder_details(folder_id),
        )
        self._add_color_menu(menu, "Ordnerfarbe", folder.get("color"), self.set_folder_color, folder_id)
        self._add_page_label_menu(menu, folder, "folder")
        menu.add_separator()
        menu.add_command(
            label="Neue Liste in diesem Ordner …",
            command=lambda: self.create_list_in_folder(folder_id),
        )
        menu.add_command(label="Neuer Ordner …", command=self.create_new_folder)
        menu.add_separator()
        menu.add_command(label="Alle Listen aufklappen", command=lambda: self.set_folder_open(folder_id, True))
        menu.add_command(label="Ordner zuklappen", command=lambda: self.set_folder_open(folder_id, False))
        menu.add_separator()
        menu.add_command(
            label="Ordner auflösen (Listen bleiben)",
            command=lambda: self.delete_folder(folder_id),
            foreground=self.theme["delete"],
        )
        menu.add_command(
            label="Ordner mit Listen in den Papierkorb",
            command=lambda: self.trash_folder(folder_id),
            foreground=self.theme["delete"],
        )
        return menu

    def build_smart_view_menu(self, view_id="in_progress"):
        """Kontextmenü der Systemzeilen „In Bearbeitung“ und „Papierkorb“."""
        menu = self._new_themed_popup_menu()
        if view_id == "trash":
            menu.add_command(label=f"Papierkorb ({len(self.trash)})", state="disabled")
            menu.add_separator()
            menu.add_command(label="Öffnen", command=self.set_trash_view)
            menu.add_separator()
            menu.add_command(
                label="Papierkorb leeren",
                command=self.empty_trash,
                foreground=self.theme["delete"],
                state="normal" if self.trash else "disabled",
            )
            return menu
        menu.add_command(label="In Bearbeitung", state="disabled")
        menu.add_separator()
        menu.add_command(label="Öffnen", command=self.set_in_progress_view)
        menu.add_command(label="Kalender öffnen …", command=self.open_calendar_view)
        menu.add_separator()
        menu.add_command(
            label="Automatisch aus allen Listen erzeugt",
            state="disabled",
        )
        return menu

    def build_folder_overview_menu(self):
        """Kontextmenü für den leeren Bereich der Ordnerübersicht."""
        menu = self._new_themed_popup_menu()
        folder = self.get_folder(self.active_folder_id)
        title = str((folder or {}).get("title") or "Ordner").strip() or "Ordner"
        menu.add_command(label=self.ellipsize_sidebar_title(title), state="disabled")
        menu.add_separator()
        menu.add_command(
            label="Neue Liste in diesem Ordner …",
            command=lambda: self.create_list_in_folder(self.active_folder_id),
        )
        menu.add_command(
            label="Bearbeiten (Titel, Beschreibungstext) …",
            command=lambda: self.edit_folder_details(self.active_folder_id),
        )
        if folder:
            self._add_color_menu(
                menu, "Ordnerfarbe", folder.get("color"), self.set_folder_color, self.active_folder_id
            )
            self._add_page_label_menu(menu, folder, "folder")
        menu.add_separator()
        menu.add_command(
            label="Ordner auflösen (Listen bleiben)",
            command=lambda: self.delete_folder(self.active_folder_id),
            foreground=self.theme["delete"],
        )
        menu.add_command(
            label="Ordner mit Listen in den Papierkorb",
            command=lambda: self.trash_folder(self.active_folder_id),
            foreground=self.theme["delete"],
        )
        return menu

    def show_sidebar_context_menu(self, event):
        """Rechtsklick auf Liste/Ordner: Bearbeiten, Farbe, Verschieben, Papierkorb."""
        tree = event.widget if event.widget in (getattr(self, "system_listbox", None), self.sidebar_listbox) else self.sidebar_listbox
        iid = tree.identify_row(event.y)
        if not iid:
            return "break"
        if tree is self.system_listbox:
            sidebar_selection = self.sidebar_listbox.selection()
            if sidebar_selection:
                self.sidebar_listbox.selection_remove(*sidebar_selection)
            tree.selection_set(iid)
        else:
            system_selection = self.system_listbox.selection()
            if system_selection:
                self.system_listbox.selection_remove(*system_selection)
            # Eine bestehende Mehrfachauswahl bleibt erhalten, wenn der
            # Rechtsklick eine ihrer Zeilen trifft.
            if iid not in tree.selection():
                tree.selection_set(iid)
        tree.focus(iid)
        row = self.sidebar_iid_to_row.get(iid)
        if not row:
            return "break"
        self._destroy_sidebar_context_menu()
        menu = self.build_sidebar_context_menu(row, rows=self.get_selected_sidebar_rows())
        if menu is None:
            return "break"
        self._sidebar_context_menu = menu
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            try:
                menu.grab_release()
            except tk.TclError:
                pass
        return "break"

    def _destroy_sidebar_context_menu(self):
        menu = getattr(self, "_sidebar_context_menu", None)
        self._sidebar_context_menu = None
        if menu is None:
            return
        try:
            menu.destroy()
        except (AttributeError, tk.TclError):
            pass

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

    def edit_list_details(self, list_id):
        """Titel und Beschreibungstext einer Liste gemeinsam bearbeiten."""
        entry = next((item for item in self.lists if item.get("id") == list_id), None)
        if entry is None:
            return "break"
        is_inbox = self.is_inbox_list(entry)
        current_title = str(entry.get("title") or "Liste")
        current_note = str(entry.get("note") or "")
        details = self.themed_page_details_dialog(
            "Liste bearbeiten",
            current_title,
            current_note,
            title_label="Listentitel" if not is_inbox else "Listentitel (fester Systemname)",
            title_editable=not is_inbox,
        )
        if details is None:
            return "break"
        new_title = details["title"] if not is_inbox else current_title
        new_note = details["note"]
        if new_title == current_title and new_note == current_note:
            return "break"
        self.snapshot_undo()
        entry["title"] = new_title
        entry["note"] = new_note
        if entry.get("id") == self.active_list_id and self.view_mode == "list":
            self.app_title = new_title
            self.update_header_title()
            self.update_window_title()
            self.update_page_note_preview()
        self.update_page_labels()
        self.save_items()
        self.update_sidebar_list()
        self.refresh_tree()
        return "break"

    def edit_folder_details(self, folder_id):
        """Titel und Beschreibungstext eines Ordners gemeinsam bearbeiten."""
        folder = self.get_folder(folder_id)
        if folder is None:
            return "break"
        current_title = str(folder.get("title") or "Ordner")
        current_note = str(folder.get("note") or "")
        details = self.themed_page_details_dialog(
            "Ordner bearbeiten", current_title, current_note, title_label="Ordnertitel"
        )
        if details is None:
            return "break"
        if details["title"] == current_title and details["note"] == current_note:
            return "break"
        self.snapshot_undo()
        folder["title"] = details["title"]
        folder["note"] = details["note"]
        if self.view_mode == "folder" and self.active_folder_id == folder_id:
            self.update_header_title()
            self.update_window_title()
            self.update_page_note_preview()
        self.update_page_labels()
        self.save_items()
        self.update_sidebar_list()
        self.refresh_tree()
        return "break"

    def create_list_in_folder(self, folder_id):
        """Legt eine neue Liste direkt im gewählten Ordner an."""
        if not self.get_folder(folder_id):
            return "break"
        title = self.themed_input_dialog("Neue Liste", "Titel der neuen Liste:", ok_text="Anlegen")
        if title is None:
            return "break"
        self.snapshot_undo()
        self.sync_current_list_reference()
        new_entry = self.new_list_object(title.strip() or "Neue Liste", [], folder_id=folder_id)
        self.lists.append(new_entry)
        self.sidebar_folder_open_states[folder_id] = True
        self.set_active_list(new_entry["id"])
        self.save_items()
        return "break"

    def move_list_to_folder_dialog(self, list_id):
        """Verschiebt eine Liste über einen Auswahldialog in einen Ordner."""
        entry = next((item for item in self.lists if item.get("id") == list_id), None)
        if entry is None or self.is_inbox_list(entry):
            return "break"
        choices = [
            (folder.get("id"), str(folder.get("title") or "Ordner").strip() or "Ordner")
            for folder in self.folders
            if folder.get("id") != entry.get("folder_id")
        ]
        if not choices:
            messagebox.showinfo("Verschieben", "Es gibt keinen anderen Ordner als Ziel.")
            return "break"
        folder_id = self.themed_choice_dialog(
            "In Ordner verschieben", "In welchen Ordner soll die Liste?", choices
        )
        if not folder_id:
            return "break"
        self.snapshot_undo()
        if self.move_sidebar_list_into_folder(list_id, folder_id):
            self.sidebar_folder_open_states[folder_id] = True
            self.save_items()
            self.update_sidebar_list()
        elif self.undo_stack:
            self.undo_stack.pop()
        return "break"

    def detach_list_from_folder(self, list_id):
        """Hebt eine Liste aus ihrem Ordner auf die Hauptebene."""
        entry = next((item for item in self.lists if item.get("id") == list_id), None)
        if entry is None or self.is_inbox_list(entry) or not entry.get("folder_id"):
            return "break"
        self.snapshot_undo()
        entry["folder_id"] = None
        self.save_items()
        self.update_sidebar_list()
        return "break"

    def duplicate_list(self, list_id):
        """Legt eine unabhängige Kopie einer Liste an."""
        entry = next((item for item in self.lists if item.get("id") == list_id), None)
        if entry is None:
            return "break"
        self.snapshot_undo()
        self.sync_current_list_reference()
        copy_items = self.copy_items_with_new_ids(entry.get("items", []))
        new_entry = self.new_list_object(
            f"{str(entry.get('title') or 'Liste').strip()} (Kopie)",
            copy_items,
            folder_id=entry.get("folder_id"),
            color=entry.get("color"),
            note=str(entry.get("note") or ""),
            labels=list(entry.get("labels") or []),
        )
        index = next((i for i, item in enumerate(self.lists) if item.get("id") == list_id), len(self.lists) - 1)
        self.lists.insert(index + 1, new_entry)
        self.set_active_list(new_entry["id"])
        self.save_items()
        return "break"

    def export_list_as(self, list_id, fmt):
        """Exportiert eine beliebige Liste, ohne die Ansicht dauerhaft zu wechseln."""
        entry = next((item for item in self.lists if item.get("id") == list_id), None)
        if entry is None:
            return "break"
        previous_list_id = self.active_list_id
        previous_mode = self.view_mode
        previous_folder_id = self.active_folder_id
        try:
            self.set_active_list(list_id, refresh=False)
            if fmt == "md":
                self.export_as_markdown()
            elif fmt == "csv":
                self.export_as_csv()
            else:
                self.export_as_txt()
        finally:
            if previous_mode == "folder" and previous_folder_id:
                self.set_active_list(previous_list_id, refresh=False)
                self.set_active_folder(previous_folder_id, refresh=False)
            elif previous_mode == "in_progress":
                self.set_active_list(previous_list_id, refresh=False)
                self.set_in_progress_view(refresh=False)
            elif previous_list_id:
                self.set_active_list(previous_list_id, refresh=False)
            self.update_sidebar_list()
            self.refresh_tree()
        return "break"

    def remove_done_items(self, list_id):
        """Entfernt alle erledigten Aufgaben einer Liste; Gruppen bleiben erhalten."""
        entry = next((item for item in self.lists if item.get("id") == list_id), None)
        if entry is None:
            return "break"
        if entry.get("id") == self.active_list_id:
            self.sync_current_list_reference()

        def prune(items):
            kept = []
            removed = 0
            for item in items:
                child_kept, child_removed = prune(item.get("children", []))
                removed += child_removed
                if not self.is_group_item(item) and item.get("done") and not child_kept:
                    removed += 1
                    continue
                item["children"] = child_kept
                kept.append(item)
            return kept, removed

        pruned, removed = prune(entry.get("items", []))
        if not removed:
            messagebox.showinfo("Erledigte entfernen", "In dieser Liste ist nichts als erledigt markiert.")
            return "break"
        title = str(entry.get("title") or "Liste").strip() or "Liste"
        if not messagebox.askyesno(
            "Erledigte entfernen",
            f"{removed} erledigte Aufgabe(n) aus '{title}' entfernen?\n\n"
            "Erledigte Punkte mit noch offenen Unterpunkten bleiben erhalten.",
        ):
            return "break"
        self.snapshot_undo()
        entry["items"] = pruned
        if entry.get("id") == self.active_list_id:
            self.items = entry["items"]
        self.save_items()
        self.refresh_tree()
        return "break"

    def clear_list_by_id(self, list_id):
        """Leert eine beliebige Liste, auch wenn sie gerade nicht geöffnet ist."""
        entry = next((item for item in self.lists if item.get("id") == list_id), None)
        if entry is None:
            return "break"
        if entry.get("id") == self.active_list_id:
            self.sync_current_list_reference()
        if not entry.get("items"):
            messagebox.showinfo("Liste leeren", "Diese Liste ist bereits leer.")
            return "break"
        title = str(entry.get("title") or "Liste").strip() or "Liste"
        if not messagebox.askyesno("Liste leeren", f"Alle Punkte aus '{title}' wirklich löschen?"):
            return "break"
        self.snapshot_undo()
        entry["items"] = []
        if entry.get("id") == self.active_list_id:
            self.items = entry["items"]
        self.save_items()
        self.refresh_tree()
        return "break"

    def delete_list_by_id(self, list_id):
        """Verschiebt eine beliebige Liste in den Papierkorb."""
        entry = next((item for item in self.lists if item.get("id") == list_id), None)
        if entry is None:
            return "break"
        if self.is_inbox_list(entry):
            messagebox.showinfo("Eingang", "Der fest integrierte Eingang kann nicht gelöscht werden.")
            return "break"
        if len(self.lists) <= 1:
            messagebox.showinfo("Liste löschen", "Die letzte Liste kann nicht gelöscht werden.")
            return "break"
        title = str(entry.get("title") or "Liste").strip() or "Liste"
        if not messagebox.askyesno(
            "In den Papierkorb",
            f"Liste '{title}' in den Papierkorb verschieben?\n\n"
            "Die Liste bleibt dort vollständig erhalten und kann wiederhergestellt werden.",
        ):
            return "break"
        self.snapshot_undo()
        if not self._move_lists_to_trash([list_id]):
            if self.undo_stack:
                self.undo_stack.pop()
            return "break"
        self.save_items()
        self.update_sidebar_list()
        self.refresh_tree()
        return "break"

    # -----------------------------
    # Papierkorb
    # -----------------------------
    def new_trash_entry(self, kind, payload, origin_folder_id=None, origin_folder_title=""):
        """Ein Papierkorbeintrag hält das vollständige Original plus Herkunft."""
        entry = {
            "id": uuid.uuid4().hex,
            "kind": self.TRASH_KIND_FOLDER if kind == self.TRASH_KIND_FOLDER else self.TRASH_KIND_LIST,
            "deleted_at": datetime.now().isoformat(timespec="seconds"),
            "origin_folder_id": origin_folder_id if isinstance(origin_folder_id, str) and origin_folder_id else None,
            "origin_folder_title": str(origin_folder_title or ""),
            "list": None,
            "folder": None,
        }
        if entry["kind"] == self.TRASH_KIND_FOLDER:
            entry["folder"] = payload
        else:
            entry["list"] = payload
        return entry

    def get_trash_entry(self, trash_id):
        return next((entry for entry in self.trash if entry.get("id") == trash_id), None)

    def trash_entry_payload(self, trash_entry):
        if not isinstance(trash_entry, dict):
            return None
        if trash_entry.get("kind") == self.TRASH_KIND_FOLDER:
            return trash_entry.get("folder")
        return trash_entry.get("list")

    def trash_entry_title(self, trash_entry):
        payload = self.trash_entry_payload(trash_entry) or {}
        fallback = "Ordner" if trash_entry.get("kind") == self.TRASH_KIND_FOLDER else "Liste"
        return str(payload.get("title") or fallback).strip() or fallback

    def push_trash_entry(self, entry):
        """Neueste Einträge stehen oben; die Obergrenze schützt die Speicherdatei."""
        self.trash.insert(0, entry)
        if len(self.trash) > self.MAX_TRASH_ENTRIES:
            del self.trash[self.MAX_TRASH_ENTRIES:]

    def _move_lists_to_trash(self, list_ids):
        """Verschiebt Listen samt Inhalt in den Papierkorb. Der Eingang bleibt geschützt."""
        moved = 0
        for list_id in list_ids:
            entry = next((item for item in self.lists if item.get("id") == list_id), None)
            if entry is None or self.is_inbox_list(entry):
                continue
            if len(self.lists) <= 1:
                break
            if entry.get("id") == self.active_list_id:
                self.sync_current_list_reference()
            folder = self.get_folder(entry.get("folder_id"))
            self.lists = [item for item in self.lists if item.get("id") != list_id]
            self.push_trash_entry(
                self.new_trash_entry(
                    self.TRASH_KIND_LIST,
                    copy.deepcopy(entry),
                    origin_folder_id=entry.get("folder_id"),
                    origin_folder_title=str((folder or {}).get("title") or ""),
                )
            )
            moved += 1
            if entry.get("id") == self.active_list_id:
                self.active_list_id = None
                fallback = next((item.get("id") for item in self.lists if not self.is_inbox_list(item)), None)
                fallback = fallback or self.lists[0].get("id")
                self.set_active_list(fallback, refresh=False)
        return moved

    def trash_folder(self, folder_id):
        """Verschiebt einen Ordner gemeinsam mit seinen Listen in den Papierkorb."""
        folder = self.get_folder(folder_id)
        if not folder:
            return "break"
        title = str(folder.get("title") or "Ordner").strip() or "Ordner"
        child_lists = self.get_folder_lists(folder_id)
        if not messagebox.askyesno(
            "In den Papierkorb",
            f"Ordner '{title}' mit {len(child_lists)} Liste(n) in den Papierkorb verschieben?\n\n"
            "Ordner und Listen bleiben dort vollständig erhalten und lassen sich gemeinsam wiederherstellen.",
        ):
            return "break"
        self.snapshot_undo()
        self._move_folder_to_trash(folder_id)
        self.save_items()
        self.update_sidebar_list()
        self.refresh_tree()
        return "break"

    def _move_folder_to_trash(self, folder_id):
        folder = self.get_folder(folder_id)
        if not folder:
            return False
        child_ids = [entry.get("id") for entry in self.get_folder_lists(folder_id)]
        self._move_lists_to_trash(child_ids)
        self.folders = [entry for entry in self.folders if entry.get("id") != folder_id]
        self.push_trash_entry(self.new_trash_entry(self.TRASH_KIND_FOLDER, copy.deepcopy(folder)))
        if self.view_mode == "folder" and self.active_folder_id == folder_id:
            inbox = self.ensure_inbox_list()
            self.active_folder_id = None
            self.set_active_list(inbox.get("id"), refresh=False)
        return True

    def trash_selected_sidebar_entries(self):
        """Papierkorb-Aktion der Mehrfachauswahl: Listen zuerst, danach Ordner."""
        rows = self.get_selected_sidebar_rows()
        list_ids = [row_id for row_type, row_id in rows if row_type == "list" and not self.is_inbox_list(row_id)]
        folder_ids = [row_id for row_type, row_id in rows if row_type == "folder"]
        if not list_ids and not folder_ids:
            messagebox.showinfo("Papierkorb", "In der Auswahl steht nichts, das gelöscht werden könnte.")
            return "break"
        if not messagebox.askyesno(
            "In den Papierkorb",
            f"{len(list_ids)} Liste(n) und {len(folder_ids)} Ordner in den Papierkorb verschieben?\n\n"
            "Alles bleibt dort vollständig erhalten und kann wiederhergestellt werden.",
        ):
            return "break"
        self.snapshot_undo()
        moved = self._move_lists_to_trash(list_ids)
        for folder_id in folder_ids:
            if self._move_folder_to_trash(folder_id):
                moved += 1
        if not moved:
            if self.undo_stack:
                self.undo_stack.pop()
            return "break"
        self.save_items()
        self.update_sidebar_list()
        self.refresh_tree()
        return "break"

    def restore_trash_entry(self, trash_id, target_folder_id=None, cascade=True, save=True):
        """Holt einen Eintrag aus dem Papierkorb zurück.

        Ein Ordner nimmt seine ehemaligen Listen automatisch mit; eine Liste
        landet in ihrem Herkunftsordner, sofern dieser noch existiert.
        """
        trash_entry = self.get_trash_entry(trash_id)
        if not trash_entry:
            return False
        payload = self.trash_entry_payload(trash_entry)
        if not isinstance(payload, dict):
            self.trash = [entry for entry in self.trash if entry.get("id") != trash_id]
            return False

        restored = copy.deepcopy(payload)
        if trash_entry.get("kind") == self.TRASH_KIND_FOLDER:
            folder_id = restored.get("id")
            if not folder_id or self.get_folder(folder_id):
                folder_id = uuid.uuid4().hex
                restored["id"] = folder_id
            self.folders.append(self.new_folder_object(
                restored.get("title"), folder_id, restored.get("color"), restored.get("note"),
                restored.get("labels"),
            ))
            self.trash = [entry for entry in self.trash if entry.get("id") != trash_id]
            if cascade:
                # Die zugehörigen Listen wurden gemeinsam gelöscht und kehren
                # gemeinsam zurück. Sie tragen die alte Ordner-ID als Herkunft.
                original_id = payload.get("id")
                related = [
                    entry.get("id")
                    for entry in list(self.trash)
                    if entry.get("kind") == self.TRASH_KIND_LIST and entry.get("origin_folder_id") == original_id
                ]
                for related_id in related:
                    self.restore_trash_entry(related_id, target_folder_id=folder_id, cascade=False, save=False)
        else:
            list_id = restored.get("id")
            if not list_id or any(entry.get("id") == list_id for entry in self.lists):
                list_id = uuid.uuid4().hex
            folder_id = target_folder_id if target_folder_id is not None else trash_entry.get("origin_folder_id")
            if folder_id and not self.get_folder(folder_id):
                folder_id = None
            restored_list = self.new_list_object(
                restored.get("title"),
                self.normalize_items(restored.get("items", []), self.collect_existing_item_ids()),
                list_id,
                folder_id,
                restored.get("color"),
                restored.get("note"),
                None,  # ein wiederhergestellter Eintrag wird nie zum Systemeingang
                restored.get("labels"),
            )
            self.lists.append(restored_list)
            self.trash = [entry for entry in self.trash if entry.get("id") != trash_id]

        self.prune_unknown_item_labels()
        if save:
            self.save_items()
            self.update_sidebar_list()
            self.refresh_tree()
        return True

    def collect_existing_item_ids(self):
        """Alle bereits vergebenen Punkt-IDs – hält Wiederherstellungen kollisionsfrei."""
        seen = set()
        for entry in self.lists:
            for item in self.walk_items(entry.get("items", [])):
                item_id = item.get("id")
                if isinstance(item_id, str) and item_id:
                    seen.add(item_id)
        return seen

    def restore_selected_trash_entries(self, into_folder=False):
        trash_ids = self.get_selected_trash_ids()
        if not trash_ids:
            messagebox.showinfo("Papierkorb", "Zuerst einen Eintrag auswählen.")
            return "break"
        target_folder_id = None
        if into_folder:
            choices = [
                (folder.get("id"), str(folder.get("title") or "Ordner").strip() or "Ordner")
                for folder in self.folders
            ]
            if not choices:
                messagebox.showinfo("Wiederherstellen", "Es gibt noch keinen Ordner als Ziel.")
                return "break"
            target_folder_id = self.themed_choice_dialog(
                "In Ordner wiederherstellen", "In welchen Ordner sollen die Listen zurück?", choices
            )
            if not target_folder_id:
                return "break"
        self.snapshot_undo()
        restored = 0
        for trash_id in trash_ids:
            entry = self.get_trash_entry(trash_id)
            if entry is None:
                continue
            folder_target = target_folder_id if entry.get("kind") == self.TRASH_KIND_LIST else None
            try:
                if self.restore_trash_entry(trash_id, target_folder_id=folder_target, save=False):
                    restored += 1
            except (ValueError, RecursionError) as exc:
                # Ein manipulierter oder überdimensionierter Eintrag darf den
                # restlichen Papierkorb nicht mitreißen; er bleibt liegen.
                messagebox.showerror(
                    "Wiederherstellen",
                    f"„{self.trash_entry_title(entry)}“ konnte nicht wiederhergestellt werden:\n{exc}",
                )
        if not restored:
            if self.undo_stack:
                self.undo_stack.pop()
            return "break"
        self.save_items()
        self.update_sidebar_list()
        self.refresh_tree()
        return "break"

    def purge_selected_trash_entries(self):
        trash_ids = self.get_selected_trash_ids()
        if not trash_ids:
            messagebox.showinfo("Papierkorb", "Zuerst einen Eintrag auswählen.")
            return "break"
        if not messagebox.askyesno(
            "Endgültig entfernen",
            f"{len(trash_ids)} Eintrag/Einträge endgültig entfernen?\n\n"
            f"Nur {self.accel('Z')} innerhalb dieser Sitzung kann den Schritt noch zurücknehmen.",
        ):
            return "break"
        self.snapshot_undo()
        removed = set(trash_ids)
        self.trash = [entry for entry in self.trash if entry.get("id") not in removed]
        self.save_items()
        self.update_sidebar_list()
        self.refresh_tree()
        return "break"

    def empty_trash(self):
        if not self.trash:
            messagebox.showinfo("Papierkorb", "Der Papierkorb ist bereits leer.")
            return "break"
        if not messagebox.askyesno(
            "Papierkorb leeren",
            f"Alle {len(self.trash)} Einträge endgültig entfernen?\n\n"
            f"Nur {self.accel('Z')} innerhalb dieser Sitzung kann den Schritt noch zurücknehmen.",
        ):
            return "break"
        self.snapshot_undo()
        self.trash = []
        self.save_items()
        self.update_sidebar_list()
        self.refresh_tree()
        return "break"

    @staticmethod
    def trash_id_from_iid(row_id):
        prefix = "trash:"
        if row_id and str(row_id).startswith(prefix):
            return str(row_id)[len(prefix):]
        return None

    def get_selected_trash_ids(self):
        if self.view_mode != "trash" or not hasattr(self, "tree"):
            return []
        ids = []
        for row_id in self.tree.selection():
            trash_id = self.trash_id_from_iid(row_id)
            if trash_id and self.get_trash_entry(trash_id):
                ids.append(trash_id)
        return ids

    def set_folder_open(self, folder_id, is_open):
        """Klappt einen Seitenleistenordner gezielt auf oder zu."""
        if not self.get_folder(folder_id):
            return "break"
        self.sidebar_folder_open_states[folder_id] = bool(is_open)
        tree = getattr(self, "sidebar_listbox", None)
        iid = f"folder:{folder_id}"
        try:
            if tree is not None and tree.exists(iid):
                tree.item(iid, open=bool(is_open))
        except tk.TclError:
            pass
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
        """Entf-Taste und die Minus-Schaltfläche der Seitenleiste.

        Wirkt immer auf die Auswahl der Seitenleiste, nie auf den Aufgabenbaum.
        Der Rückgabewert „break" verhindert, dass zusätzlich die globale
        Entf-Bindung des Aufgabenbaums auslöst.
        """
        rows = self.get_selected_sidebar_rows()
        if len(rows) > 1:
            self.trash_selected_sidebar_entries()
            return "break"
        row = rows[0] if rows else None
        if row and row[0] == "view":
            messagebox.showinfo(
                "Systemansicht",
                "Eingang, „In Bearbeitung“ und Papierkorb gehören fest zur Anwendung.",
            )
            return "break"
        if row and row[0] == "folder":
            self.trash_folder(row[1])
            return "break"
        if row and row[0] == "list" and self.is_inbox_list(row[1]):
            messagebox.showinfo("Eingang", "Der fest integrierte Eingang kann nicht gelöscht werden.")
            return "break"
        if row and row[0] == "list":
            self.delete_list_by_id(row[1])
            return "break"
        self.delete_current_list(event)
        return "break"

    def move_selected_lists_to_folder(self, folder_id):
        """Verschiebt alle markierten Listen gemeinsam in einen Ordner oder heraus."""
        list_ids = self.get_selected_sidebar_list_ids()
        if not list_ids:
            messagebox.showinfo("Verschieben", "In der Auswahl steht keine verschiebbare Liste.")
            return "break"
        if folder_id is not None and not self.get_folder(folder_id):
            return "break"
        self.snapshot_undo()
        changed = False
        for list_id in list_ids:
            if folder_id is None:
                entry = next((item for item in self.lists if item.get("id") == list_id), None)
                if entry is not None and entry.get("folder_id"):
                    entry["folder_id"] = None
                    changed = True
            elif self.move_sidebar_list_into_folder(list_id, folder_id):
                changed = True
        if not changed:
            if self.undo_stack:
                self.undo_stack.pop()
            return "break"
        if folder_id:
            self.sidebar_folder_open_states[folder_id] = True
        self.save_items()
        self.update_sidebar_list()
        return "break"

    def set_selected_sidebar_color(self, color_key):
        """Färbt alle markierten Listen und Ordner in einem Schritt."""
        rows = self.get_selected_sidebar_rows()
        if not rows:
            return "break"
        new_color = color_key if color_key in self.LIST_COLOR_KEYS else None
        self.snapshot_undo()
        changed = False
        for row_type, row_id in rows:
            entries = self.lists if row_type == "list" else self.folders if row_type == "folder" else None
            if entries is None:
                continue
            entry = next((item for item in entries if item.get("id") == row_id), None)
            if entry is not None and entry.get("color") != new_color:
                entry["color"] = new_color
                changed = True
        if not changed:
            if self.undo_stack:
                self.undo_stack.pop()
            return "break"
        self.save_items()
        self.update_sidebar_list()
        return "break"

    def move_sidebar_selection(self, offset):
        """Verschiebt markierte Listen oder Ordner um eine Position nach oben/unten."""
        rows = self.get_selected_sidebar_rows()
        if not rows:
            return "break"
        moved = False
        self.snapshot_undo()
        for row_type, row_id in (rows if offset < 0 else list(reversed(rows))):
            if row_type == "list":
                collection = self.lists
                if self.is_inbox_list(row_id):
                    continue
            elif row_type == "folder":
                collection = self.folders
            else:
                continue
            index = next((i for i, entry in enumerate(collection) if entry.get("id") == row_id), None)
            if index is None:
                continue
            target = index + offset
            if target < 0 or target >= len(collection):
                continue
            if row_type == "list":
                if self.is_inbox_list(collection[target]):
                    continue
                # Beim Tausch bleibt die Ordnerzugehörigkeit der Zielposition erhalten.
                collection[index]["folder_id"] = collection[target].get("folder_id")
            collection[index], collection[target] = collection[target], collection[index]
            moved = True
        if not moved:
            if self.undo_stack:
                self.undo_stack.pop()
            return "break"
        self.save_items()
        self.update_sidebar_list()
        return "break"

    def delete_folder(self, folder_id):
        """Löst einen Ordner auf: die enthaltenen Listen bleiben auf der Hauptebene."""
        folder = next((entry for entry in self.folders if entry.get("id") == folder_id), None)
        if not folder:
            return "break"
        title = folder.get("title", "Ordner")
        if not messagebox.askyesno(
            "Ordner auflösen",
            f"Ordner '{title}' auflösen?\n\n"
            "Die enthaltenen Listen bleiben erhalten und werden auf die Hauptebene verschoben. "
            "Der leere Ordner wandert in den Papierkorb.",
        ):
            return "break"
        self.snapshot_undo()
        for entry in self.lists:
            if entry.get("folder_id") == folder_id:
                entry["folder_id"] = None
        self.folders = [entry for entry in self.folders if entry.get("id") != folder_id]
        self.push_trash_entry(self.new_trash_entry(self.TRASH_KIND_FOLDER, copy.deepcopy(folder)))
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
                try:
                    if self.sidebar_listbox.item(iid, "open"):
                        collect(iid)
                except tk.TclError:
                    continue
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
        self.sidebar_listbox.focus_set()
        iid = self.sidebar_listbox.identify_row(event.y)
        self.sidebar_drag_start_iid = iid if iid else None
        self.sidebar_drag_start_y = event.y
        self.sidebar_drag_has_moved = False
        if not iid:
            return
        # Eine bestehende Mehrfachauswahl bleibt erhalten, solange der Zug in
        # ihr beginnt. Shift und Strg sollen weiterhin die Auswahl erweitern.
        if event.state & 0x0005:  # Shift oder Control
            return
        if iid not in self.sidebar_listbox.selection():
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

        # Mehrfachauswahl: alle markierten Listen gleiten gemeinsam in den Ordner.
        selected_list_ids = self.get_selected_sidebar_list_ids()
        if (
            len(selected_list_ids) > 1
            and source_row[0] == "list"
            and source_row[1] in selected_list_ids
            and target_row
            and target_row[0] == "folder"
        ):
            self.snapshot_undo()
            changed = False
            for list_id in selected_list_ids:
                if self.move_sidebar_list_into_folder(list_id, target_row[1]):
                    changed = True
            if changed:
                self.sidebar_folder_open_states[target_row[1]] = True
                self.save_items()
                self.update_sidebar_list()
            elif self.undo_stack:
                self.undo_stack.pop()
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
        for tree_name in ("system_listbox", "sidebar_listbox"):
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
        return self.delete_list_by_id(self.current_list().get("id"))

    def validate_backup_schema(self, data, *, portable=False):
        """Prüft ein Backup strikt, ohne den aktuellen App-Zustand zu ändern.

        Alte reine JSON-Aufgabenlisten bleiben für die Migration zulässig. Ein
        portables .glidebackup muss einem ausdrücklich unterstützten Glide-
        Datenformat entsprechen; die Formate 4 bis 6 werden additiv gehoben.

        Die Prüfung erfasst zusätzlich Labels und Papierkorb: Anhänge in
        gelöschten, aber noch wiederherstellbaren Listen zählen als referenziert
        und werden deshalb mitgesichert.
        """
        trash_item_roots = []
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
            raw_labels = data.get("labels", [])
            raw_trash = data.get("trash", [])
            if not isinstance(raw_labels, list) or not isinstance(raw_trash, list):
                raise ValueError("Die Felder 'labels' und 'trash' müssen Listen sein.")
            label_ids = set()
            for label in raw_labels:
                if not isinstance(label, dict):
                    raise ValueError("Ein Label im Backup ist ungültig.")
                label_id = label.get("id")
                if portable and (not isinstance(label_id, str) or not label_id):
                    raise ValueError("Ein Label im Komplettbackup besitzt keine ID.")
                if isinstance(label_id, str) and label_id:
                    if label_id in label_ids:
                        raise ValueError("Das Backup enthält doppelte Label-IDs.")
                    label_ids.add(label_id)
                if portable and label.get("color") is not None and label.get("color") not in self.LABEL_COLOR_KEYS:
                    raise ValueError("Ein Label im Komplettbackup besitzt eine unbekannte Farbe.")
            # Gelöschte Listen bleiben vollwertige Daten: ihre Aufgaben werden
            # zusätzlich geprüft, damit auch deren Anhänge im Backup landen.
            for trash_entry in raw_trash:
                if not isinstance(trash_entry, dict):
                    raise ValueError("Ein Papierkorbeintrag im Backup ist ungültig.")
                if trash_entry.get("kind") not in (None, self.TRASH_KIND_LIST, self.TRASH_KIND_FOLDER):
                    raise ValueError("Ein Papierkorbeintrag besitzt eine unbekannte Art.")
                trashed_list = trash_entry.get("list")
                if isinstance(trashed_list, dict):
                    trashed_items = trashed_list.get("items", [])
                    if not isinstance(trashed_items, list):
                        raise ValueError("Das Aufgabenfeld einer gelöschten Liste ist ungültig.")
                    trash_item_roots.append(trashed_items)
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
            if folder.get("labels") is not None and not isinstance(folder.get("labels"), list):
                raise ValueError("Die Labels eines Ordners sind ungültig.")

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
            if list_entry.get("labels") is not None and not isinstance(list_entry.get("labels"), list):
                raise ValueError("Die Labels einer Liste sind ungültig.")
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
                item_kind = item.get("kind")
                if portable and item_kind is not None and item_kind not in self.ITEM_KINDS:
                    raise ValueError("Ein Punkt im Komplettbackup besitzt eine unbekannte Art.")
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
                item_labels = item.get("labels")
                if item_labels is not None and not isinstance(item_labels, list):
                    raise ValueError("Die Labels einer Aufgabe sind ungültig.")

        # Aufgaben aus dem Papierkorb durchlaufen dieselbe Prüfung. Ihre Anhänge
        # gehören zwingend ins Backup, sonst wäre eine Wiederherstellung
        # unvollständig.
        for trashed_items in trash_item_roots:
            stack = [(entry, 0) for entry in reversed(trashed_items)]
            while stack:
                item, depth = stack.pop()
                item_count += 1
                if item_count > self.MAX_BACKUP_ITEMS:
                    raise ValueError("Das Backup enthält zu viele Aufgaben.")
                if depth > self.MAX_ITEM_DEPTH:
                    raise ValueError("Das Backup ist zu tief verschachtelt.")
                if not isinstance(item, dict):
                    if isinstance(item, str) and not portable:
                        continue
                    raise ValueError("Ein Aufgabenpunkt im Papierkorb ist ungültig.")
                item_id = item.get("id")
                if isinstance(item_id, str) and item_id:
                    if item_id in item_ids:
                        raise ValueError("Das Backup enthält doppelte Aufgaben-IDs.")
                    item_ids.add(item_id)
                children = item.get("children", [])
                if not isinstance(children, list):
                    raise ValueError("Die Unterpunkte einer gelöschten Aufgabe sind ungültig.")
                stack.extend((child, depth + 1) for child in reversed(children))
                attachments = item.get("attachments", [])
                if not isinstance(attachments, list):
                    raise ValueError("Die Anhänge einer gelöschten Aufgabe sind ungültig.")
                for attachment in attachments:
                    if not isinstance(attachment, dict):
                        raise ValueError("Ein Anhang im Papierkorb ist ungültig.")
                    referenced_storages.add(self.validate_attachment_storage(attachment.get("storage")))

        if isinstance(data, dict):
            active_list_id = data.get("active_list_id")
            active_folder_id = data.get("active_folder_id")
            if active_list_id is not None and active_list_id not in list_ids:
                raise ValueError("Das Backup verweist auf eine unbekannte aktive Liste.")
            if active_folder_id is not None and active_folder_id not in folder_ids:
                raise ValueError("Das Backup verweist auf einen unbekannten aktiven Ordner.")
        return referenced_storages

    def normalize_lists_data(self, data):
        """Wandelt gespeicherte Daten in den geprüften Laufzeitzustand.

        Setzt neben dem Rückgabewert auch ``self.folders``, ``self.labels`` und
        ``self.trash``; der Aufrufer sichert diese Felder bei Bedarf vorher.
        """
        self.folders = []
        self.labels = []
        self.trash = []
        if isinstance(data, dict):
            if not isinstance(data.get("lists"), list):
                raise ValueError("Die Datei enthält kein gültiges Listen-Schema.")
            version = data.get("version")
            if version is not None and (not isinstance(version, int) or version < 1 or version > self.DATA_SCHEMA_VERSION):
                raise ValueError(f"Die Datenformat-Version {version!r} wird nicht unterstützt.")
            if not isinstance(data.get("folders", []), list):
                raise ValueError("Das Feld 'folders' muss eine Liste sein.")
            if not isinstance(data.get("labels", []), list):
                raise ValueError("Das Feld 'labels' muss eine Liste sein.")
            if not isinstance(data.get("trash", []), list):
                raise ValueError("Das Feld 'trash' muss eine Liste sein.")
            # Migration auf Format 7: fehlende Labels und ein fehlender
            # Papierkorb bedeuten schlicht "leer"; kein destruktiver Schritt.
            self.labels = self.normalize_labels_data(data.get("labels", []))
            known_label_ids = {label.get("id") for label in self.labels}
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
                folder_labels = self.normalize_item_labels(folder.get("labels"), known_label_ids)
                self.folders.append(self.new_folder_object(title, folder_id, color, note, folder_labels))
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
                items = self.normalize_items(entry.get("items", []), item_ids, 0, item_counter, known_label_ids)
                color = entry.get("color") if entry.get("color") in self.LIST_COLOR_KEYS else None
                note = str(entry.get("note") or "")
                system_role = "inbox" if entry.get("system_role") == "inbox" else None
                list_labels = self.normalize_item_labels(entry.get("labels"), known_label_ids)
                lists.append(
                    self.new_list_object(title, items, list_id, folder_id, color, note, system_role, list_labels)
                )

            self.trash = self.normalize_trash_data(
                data.get("trash", []), item_ids, item_counter, known_label_ids
            )
            active_id = data.get("active_list_id") if isinstance(data.get("active_list_id"), str) else None
            return lists, active_id

        # Abwärtskompatibilität: alte Speicherdatei war direkt eine Item-Liste.
        if not isinstance(data, list):
            raise ValueError("Die Datei ist weder ein Glide-Dokument noch eine alte Aufgabenliste.")
        title = self.settings.get("title", "Meine Liste") if isinstance(self.settings, dict) else "Meine Liste"
        self.folders = []
        return [self.new_list_object(str(title).strip() or "Meine Liste", self.normalize_items(data))], None

    def normalize_trash_data(self, data, item_ids=None, item_counter=None, known_label_ids=None):
        """Bereinigt den Papierkorb; unvollständige Einträge werden verworfen."""
        entries = []
        if not isinstance(data, list):
            return entries
        seen_ids = set()
        for raw in data:
            if not isinstance(raw, dict):
                continue
            kind = raw.get("kind")
            if kind not in (self.TRASH_KIND_LIST, self.TRASH_KIND_FOLDER):
                continue
            payload = raw.get("folder") if kind == self.TRASH_KIND_FOLDER else raw.get("list")
            if not isinstance(payload, dict):
                continue
            entry_id = raw.get("id") if isinstance(raw.get("id"), str) and raw.get("id") else None
            while not entry_id or entry_id in seen_ids:
                entry_id = uuid.uuid4().hex
            seen_ids.add(entry_id)
            title = str(payload.get("title") or ("Ordner" if kind == self.TRASH_KIND_FOLDER else "Liste")).strip()
            color = payload.get("color") if payload.get("color") in self.LIST_COLOR_KEYS else None
            note = str(payload.get("note") or "")
            payload_labels = self.normalize_item_labels(payload.get("labels"), known_label_ids)
            if kind == self.TRASH_KIND_FOLDER:
                stored = self.new_folder_object(title, payload.get("id"), color, note, payload_labels)
            else:
                stored = self.new_list_object(
                    title,
                    self.normalize_items(payload.get("items", []), item_ids, 0, item_counter, known_label_ids),
                    payload.get("id") if isinstance(payload.get("id"), str) else None,
                    None,
                    color,
                    note,
                    None,
                    payload_labels,
                )
            trash_entry = {
                "id": entry_id,
                "kind": kind,
                "deleted_at": str(raw.get("deleted_at") or ""),
                "origin_folder_id": raw.get("origin_folder_id")
                if isinstance(raw.get("origin_folder_id"), str) and raw.get("origin_folder_id")
                else None,
                "origin_folder_title": str(raw.get("origin_folder_title") or ""),
                "list": stored if kind == self.TRASH_KIND_LIST else None,
                "folder": stored if kind == self.TRASH_KIND_FOLDER else None,
            }
            entries.append(trash_entry)
            if len(entries) >= self.MAX_TRASH_ENTRIES:
                break
        return entries

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
        self.header_frame = top_frame
        top_frame.bind("<Configure>", self.update_header_title, add="+")

        title_block = self.register_theme_widget(tk.Frame(top_frame, bg=self.theme["bg"]), "bg")
        self.title_block = title_block
        title_block.pack(side="left", fill="x", expand=True)

        title_row = self.register_theme_widget(tk.Frame(title_block, bg=self.theme["bg"]), "bg")
        title_row.pack(anchor="w", fill="x", pady=(0, 4))

        self.title_label = self.register_theme_widget(
            tk.Label(
                title_row,
                text=self.app_title,
                font=self.header_title_font(),
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
                text="Beschreibungstext hinzufügen …",
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

        # Labels der geöffneten Liste oder des geöffneten Ordners. Eine eigene
        # Zeile aus einzelnen Labels erlaubt – anders als eine Treeview-Zelle –
        # für jedes Label seine echte Farbe. In der Seitenleiste erscheinen
        # diese Labels bewusst nicht.
        self.page_labels_frame = self.register_theme_widget(
            tk.Frame(title_block, bg=self.theme["bg"]), "bg"
        )
        self.page_label_widgets = []

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

        # Spaltenfolge: Text – Fälligkeit – Labels – rechter Innenabstand.
        # Die Labelspalte steht damit ganz rechts neben der Fälligkeit und
        # verschwindet vollständig, solange keine Labels angelegt sind.
        self.tree = ttk.Treeview(
            self.list_frame,
            columns=("due", "labels", "due_padding"),
            displaycolumns=("due", "labels", "due_padding"),
            show="tree",
            selectmode="extended",
            style="App.Treeview",
            takefocus=True,
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
        self.tree.column(
            "labels",
            anchor="e",
            stretch=False,
            width=0,
            minwidth=0,
        )
        self.tree.column(
            "due_padding",
            anchor="e",
            stretch=False,
            width=self.DUE_RIGHT_PADDING_WIDTH,
            minwidth=self.DUE_RIGHT_PADDING_WIDTH,
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
        # Verschieben ohne Maus: dieselbe Belegung wie in der Seitenleiste.
        self.tree.bind("<Alt-Up>", lambda event: self.move_selected_items(-1))
        self.tree.bind("<Alt-Down>", lambda event: self.move_selected_items(1))
        self.tree.bind("<Alt-Left>", self.outdent_selected)
        self.tree.bind("<Alt-Right>", self.indent_selected)
        self.bind_mousewheel(self.tree)

        self.hint_label = self.register_theme_widget(
            tk.Label(
                self.content_frame,
                text=(
                    "Drag & Drop: Reihenfolge ändern · Shift + Drag: Unterpunkt · "
                    "Shift + Klick: Bereich auswählen · Tab: ein-/ausrücken · "
                    "Rechtsklick: Details, Wichtigkeit, Fälligkeit, Farbe und Labels · F2: Bearbeiten"
                ),
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

        # Labels und Kalender ersetzen die früheren TXT-Schaltflächen. Import und
        # Export bleiben vollständig erreichbar: im Menü „Datei“, im
        # Kontextmenü einer Liste und über Strg+E beziehungsweise Strg+I.
        group_io = make_action_group(button_frame, 2, (0, 0), 60)
        # Die obere Reihe bleibt farblich gemischt: die beiden neuen Schaltflächen
        # übernehmen die Farben ihrer Vorgänger an derselben Stelle.
        self.labels_button = self.make_button(group_io.inner, "Labels", self.open_label_manager, "export", **top_opts)
        self.labels_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.calendar_button = self.make_button(group_io.inner, "Kalender", self.open_calendar_view, "import", **top_opts)
        self.calendar_button.grid(row=0, column=1, sticky="ew")

        # Zweite Aktionsreihe – drei gruppierte Paare:
        # Bearbeiten & Rückgängig · Kopieren & Einfügen · Aufklappen & Zuklappen.
        utility_frame = self.register_theme_widget(tk.Frame(self.content_frame, bg=self.theme["bg"]), "bg")
        # 14 px unten spiegeln den unteren Außenabstand der Seitenleisten-Box.
        # Dadurch enden linke und rechte Spalte exakt auf derselben Linie.
        utility_frame.pack(fill="x", pady=(0, 14))
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

        # Der Titelblock wird zuletzt neu gepackt. Pack vergibt den Platz in
        # Packreihenfolge; dadurch behalten Fortschrittszeile und Design-Schalter
        # ihre Breite auch dann, wenn ein Listentitel sehr lang ist.
        self.title_block.pack_forget()
        self.title_block.pack(side="left", fill="x", expand=True)
        self.update_header_title()

    def update_header_title(self, event=None):
        """Zeigt den Seitentitel und kürzt ihn nur, wenn der Platz nicht reicht.

        Gespeicherter Titel, Fenstertitel und alle Exporte bleiben vollständig.
        """
        label = getattr(self, "title_label", None)
        header = getattr(self, "header_frame", None)
        if label is None or header is None:
            return
        full_title = self.get_display_title()
        try:
            available = header.winfo_width()
            if available <= 1:
                label.configure(text=full_title)
                return
            for widget, gap in (
                (getattr(self, "stats_label", None), 16),
                (getattr(self, "theme_button", None), 12),
            ):
                if widget is not None:
                    available -= widget.winfo_reqwidth() + gap
            available = max(self.HEADER_TITLE_MIN_WIDTH, available)
            font = getattr(self, "_header_title_measure_font", None)
            if font is None:
                font = tkfont.Font(root=self.root, font=label.cget("font"))
                self._header_title_measure_font = font
            text = full_title
            if font.measure(text) > available:
                ellipsis = "…"
                while text and font.measure(text + ellipsis) > available:
                    text = text[:-1]
                text = (text.rstrip() + ellipsis) if text else ellipsis
            if label.cget("text") != text:
                label.configure(text=text)
        except tk.TclError:
            pass

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
            for style_name, surface_key in (("Sidebar.Treeview", "card"), ("System.Treeview", "card")):
                self.style.configure(
                    style_name,
                    background=self.theme[surface_key],
                    fieldbackground=self.theme[surface_key],
                    foreground=self.theme["text"],
                    borderwidth=0,
                    relief="flat",
                    rowheight=34,
                    font=("TkDefaultFont", 11),
                )
                try:
                    self.style.layout(style_name, [("Treeview.treearea", {"sticky": "nswe"})])
                except tk.TclError:
                    pass
                self.style.map(
                    style_name,
                    background=[("selected", self.theme["selection"])],
                    foreground=[("selected", "#FFFFFF")],
                )
            # Im Hauptbaum bleibt der native Klapppfeil erhalten, erhält aber
            # Luft innerhalb des Auswahlbalkens. Der Eingang braucht keinen
            # Klapppfeil und kann deshalb exakt an der 10-Pixel-Kante beginnen.
            self.style.configure(
                "Sidebar.Treeview.Item",
                padding=(self.SIDEBAR_ITEM_LEFT_PADDING, 0, 0, 0),
            )
            try:
                self.style.layout(
                    "System.Treeview.Item",
                    [
                        (
                            "Treeitem.padding",
                            {
                                "sticky": "nswe",
                                "children": [
                                    ("Treeitem.image", {"side": "left", "sticky": ""}),
                                    ("Treeitem.text", {"sticky": "nswe"}),
                                ],
                            },
                        )
                    ],
                )
                self.style.configure(
                    "System.Treeview.Item",
                    padding=(self.SYSTEM_ITEM_LEFT_PADDING, 0, 0, 0),
                )
            except tk.TclError:
                pass
            for sidebar_tree_name in ("system_listbox", "sidebar_listbox"):
                sidebar_tree = getattr(self, sidebar_tree_name, None)
                if sidebar_tree is None:
                    continue
                sidebar_tree.tag_configure("folder", foreground=self.theme["muted"])
                sidebar_tree.tag_configure("list", foreground=self.theme["text"])
                sidebar_tree.tag_configure(
                    "system",
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
        self.style.configure(
            "App.Treeview.Item",
            padding=(self.SIDEBAR_ITEM_LEFT_PADDING, 0, 0, 0),
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
            self.tree.tag_configure(
                "group_item",
                foreground=self.theme["text"],
                font=self.group_row_font(),
            )
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
        if not IS_WINDOWS or attempt >= len(self.WINDOWS_CHROME_RETRY_DELAYS_MS):
            return
        target = window or self.root

        holder = {}

        def apply_or_retry():
            self._after_ids.discard(holder.get("id"))
            try:
                if not target.winfo_exists():
                    return
                if target.winfo_ismapped() and self._apply_windows_chrome_theme(target):
                    return
            except tk.TclError:
                return
            self._schedule_windows_chrome_theme(target, attempt + 1)

        try:
            holder["id"] = self._register_after(
                target.after(self.WINDOWS_CHROME_RETRY_DELAYS_MS[attempt], apply_or_retry)
            )
        except tk.TclError:
            pass

    def _apply_windows_chrome_theme(self, window=None):
        """Färbt unter Windows den nativen Fensterrahmen passend zum App-Theme."""
        if not IS_WINDOWS:
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
        """Öffnet für die aktuelle Seite den gemeinsamen Bearbeiten-Dialog."""
        if self.view_mode == "in_progress":
            messagebox.showinfo("In Bearbeitung", "Diese automatisch erzeugte Ansicht hat einen festen Namen.")
            return "break"
        if self.view_mode == "trash":
            messagebox.showinfo("Papierkorb", "Der Papierkorb hat einen festen Namen.")
            return "break"
        if self.view_mode == "folder" and self.active_folder_id:
            return self.edit_folder_details(self.active_folder_id)
        return self.edit_list_details(self.current_list().get("id"))

    def update_page_labels(self):
        """Zeigt die Labels der geöffneten Seite farbig unter dem Titel."""
        frame = getattr(self, "page_labels_frame", None)
        if frame is None:
            return
        for widget in getattr(self, "page_label_widgets", []):
            try:
                widget.destroy()
            except tk.TclError:
                pass
        self.page_label_widgets = []
        page = self.get_active_page()
        labels = self.item_labels(page) if page else []
        if not labels:
            frame.pack_forget()
            return
        for index, label in enumerate(labels):
            chip = tk.Label(
                frame,
                text=str(label.get("name", "")),
                bg=self.theme["bg"],
                fg=self.label_color(label),
                font=("TkDefaultFont", 9, "bold"),
            )
            chip.pack(side="left", padx=(0 if index == 0 else 10, 0))
            self.page_label_widgets.append(chip)
        frame.pack(anchor="w", fill="x", pady=(3, 0))

    def update_page_note_preview(self):
        if not hasattr(self, "note_preview_label"):
            return
        if self.view_mode == "in_progress":
            self.note_preview_label.configure(text="Alle Aufgaben mit Fälligkeit · Doppelklick öffnet die Quellliste")
            return
        if self.view_mode == "trash":
            self.note_preview_label.configure(
                text="Gelöschte Listen und Ordner · Doppelklick stellt einen Eintrag wieder her"
            )
            return
        page = self.get_active_page()
        note = str(page.get("note") or "") if page else ""
        compact = " ".join(note.split())
        if compact:
            preview = compact if len(compact) <= 110 else compact[:107].rstrip() + "…"
        else:
            preview = "Beschreibungstext hinzufügen …"
        self.note_preview_label.configure(text=preview)

    def edit_page_note(self, event=None):
        """Beschreibungstext der aktuellen Seite – seit 2.7.0 im gemeinsamen Dialog."""
        if self.view_mode == "folder" and self.active_folder_id:
            return self.edit_folder_details(self.active_folder_id)
        page = self.get_active_page()
        if not page:
            return "break"
        return self.edit_list_details(page.get("id"))

    def update_entry_mode(self):
        if not hasattr(self, "entry"):
            return
        if self.view_mode == "folder":
            new_placeholder = "Neue Liste in diesem Ordner"
        elif self.view_mode == "in_progress":
            new_placeholder = "Automatische Ansicht – Aufgabe in der Quellliste anlegen"
        elif self.view_mode == "trash":
            new_placeholder = "Papierkorb – Einträge wiederherstellen oder endgültig entfernen"
        else:
            new_placeholder = "Listenpunkt eingeben"
        if self.entry_placeholder_active:
            self.entry.delete(0, tk.END)
            self.entry_placeholder_text = new_placeholder
            self.entry.insert(0, new_placeholder)
        else:
            self.entry_placeholder_text = new_placeholder
        if hasattr(self, "hint_label"):
            if self.view_mode == "in_progress":
                self.hint_label.configure(
                    text="Chronologisch nach Fälligkeit · Doppelklick oder Enter: Aufgabe in der Quellliste öffnen · "
                    f"{self.accel('K')}: Kalenderansicht · Suche und Offen-/Erledigt-Filter gelten auch hier"
                )
            elif self.view_mode == "trash":
                self.hint_label.configure(
                    text="Doppelklick oder Enter: wiederherstellen · Rechtsklick: in Ordner wiederherstellen, "
                    "endgültig entfernen, Papierkorb leeren · gelöschte Ordner nehmen ihre Listen mit"
                )
            elif self.view_mode == "folder":
                self.hint_label.configure(
                    text="Doppelklick oder Enter: Liste öffnen · Eingabefeld: neue Liste in diesem Ordner anlegen · "
                    "Drag & Drop: Listen sortieren · Auf einen Ordner links ziehen: Liste verschieben · "
                    "Labels einer Liste erscheinen rechts in dieser Übersicht"
                )
            else:
                self.hint_label.configure(
                    text="Rechtsklick: alle Aktionen inklusive Gruppen und Labels · Drag & Drop: Reihenfolge ändern · "
                    "Auf eine Seitenleisten-Liste ziehen: dorthin verschieben · Shift + Drag: Unterpunkt · "
                    f"Shift + Klick: Bereich auswählen · {self.accel('A')}: alle auswählen · "
                    "Alt+↑/↓: verschieben · Alt+←/→: aus-/einrücken · "
                    f"Tab: ein-/ausrücken · {self.accel('G')}: gruppieren · {self.accel('F')}: Suche · "
                    f"{self.accel('T')}: Fälligkeit · {self.accel('Z')}: Rückgängig · F2: Details"
                )

    @staticmethod
    def safe_filename(value):
        cleaned = "".join(char if char.isalnum() or char in (" ", "-", "_") else "_" for char in value)
        cleaned = "_".join(cleaned.strip().split())
        return cleaned.lower() or "meine_liste"

    def clamp_geometry(self, geom):
        """Hält eine gespeicherte Fenstergeometrie auf dem sichtbaren Bildschirm.

        Nach einem Monitorwechsel – etwa Notebook ohne angeschlossenes Dock –
        zeigt eine gespeicherte Position sonst auf einen Bereich, den es nicht
        mehr gibt; das Fenster wäre unsichtbar.
        """
        match = re.match(r"^(\d+)x(\d+)(?:([+-]\d+)([+-]\d+))?$", str(geom or "").strip())
        if not match:
            return None
        width = int(match.group(1))
        height = int(match.group(2))
        if match.group(3) is None:
            return f"{width}x{height}"
        x = int(match.group(3))
        y = int(match.group(4))
        try:
            screen_w = self.root.winfo_screenwidth()
            screen_h = self.root.winfo_screenheight()
        except tk.TclError:
            return f"{width}x{height}"
        # Mindestens ein sichtbarer Fensterstreifen muss auf dem Bildschirm liegen.
        visible_margin = 120
        x = max(-(width - visible_margin), min(x, screen_w - visible_margin))
        y = max(0, min(y, screen_h - visible_margin))
        return f"{width}x{height}+{x}+{y}"

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
                    safe_geometry = self.clamp_geometry(geom)
                    if width >= min_restore_width and height >= min_restore_height and safe_geometry:
                        self.root.geometry(safe_geometry)
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

    def current_focus_widget(self):
        """Fokus-Widget ohne Ausnahme.

        focus_get() wirft KeyError, sobald der Fokus auf einem Fenster liegt,
        das Tk selbst erzeugt hat (native Dialoge, gepostete Menüs).
        """
        try:
            return self.root.focus_get()
        except (KeyError, tk.TclError):
            return None

    def _register_after(self, after_id):
        if after_id is not None:
            self._after_ids.add(after_id)
        return after_id

    def schedule_scrollbar_refresh(self):
        if not hasattr(self, "root"):
            return
        # Mehrfachaufrufe innerhalb eines Leerlaufzyklus werden zusammengefasst;
        # ohne das sammelten sich pro Listenaufbau tote after-IDs an.
        if getattr(self, "_scrollbar_refresh_id", None) is not None:
            return

        def run():
            self._after_ids.discard(getattr(self, "_scrollbar_refresh_id", None))
            self._scrollbar_refresh_id = None
            self.refresh_scrollbar_state()

        try:
            self._scrollbar_refresh_id = self._register_after(self.root.after_idle(run))
        except tk.TclError:
            self._scrollbar_refresh_id = None

    def active_label_column_width(self):
        """Breite der Labelspalte.

        Sie erscheint nur dort, wo Labels tatsächlich dargestellt werden – in
        einer Liste, in „In Bearbeitung“ und in der Ordnerübersicht – und nur,
        wenn überhaupt Labels angelegt sind. Der Papierkorb behält dadurch die
        volle Textbreite.
        """
        if not self.labels or self.view_mode not in ("list", "in_progress", "folder"):
            return 0
        return self.LABEL_COLUMN_WIDTH

    def sync_task_tree_columns(self, event=None):
        """Hält Fälligkeits- und Labelspalte bei jeder Treeview-Breite sichtbar rechts."""
        if not hasattr(self, "tree"):
            return
        try:
            label_width = self.active_label_column_width()
            tree_width = int(getattr(event, "width", 0) or self.tree.winfo_width())
            text_width = max(
                180,
                tree_width
                - self.DUE_COLUMN_WIDTH
                - label_width
                - self.DUE_RIGHT_PADDING_WIDTH
                - self.TASK_TREE_EDGE_PADDING,
            )
            self.tree.column("#0", width=text_width)
            self.tree.column(
                "due",
                width=self.DUE_COLUMN_WIDTH,
                minwidth=self.DUE_COLUMN_WIDTH,
            )
            self.tree.column("labels", width=label_width, minwidth=0)
            self.tree.column(
                "due_padding",
                width=self.DUE_RIGHT_PADDING_WIDTH,
                minwidth=self.DUE_RIGHT_PADDING_WIDTH,
            )
        except (TypeError, ValueError, tk.TclError):
            pass

    def cancel_pending_callbacks(self):
        if not hasattr(self, "root"):
            return
        self._destroy_item_context_menu()
        self._destroy_sidebar_context_menu()
        for after_id in list(getattr(self, "_after_ids", ()) or ()):
            try:
                self.root.after_cancel(after_id)
            except tk.TclError:
                pass
        self._after_ids = set()
        self._scrollbar_refresh_id = None
        self._autosave_id = None

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
        kind=ITEM_KIND_TASK,
        labels=None,
    ):
        is_group = kind == self.ITEM_KIND_GROUP
        return {
            "id": item_id or uuid.uuid4().hex,
            "text": str(text),
            # Eine Gruppe ist ein reiner Behälter: kein Erledigt-Zustand, keine
            # Fälligkeit, keine Wichtigkeit. So bleibt jede Auswertung eindeutig.
            "done": False if is_group else bool(done),
            "importance": 0 if is_group else self.clamp_importance(importance),
            "due": None if is_group else self.normalize_due(due),
            "description": str(description or ""),
            "attachments": self.normalize_attachments(attachments),
            "color": color if color in self.ITEM_COLOR_KEYS else None,
            "kind": self.ITEM_KIND_GROUP if is_group else self.ITEM_KIND_TASK,
            # Format 7: Labelzuordnung als Liste von Label-IDs. Fehlt das Feld,
            # trägt der Punkt keine Labels; ältere Bestände bleiben gültig.
            "labels": self.normalize_item_labels(labels),
            "children": children if isinstance(children, list) else [],
        }

    @classmethod
    def item_kind(cls, item):
        """Liefert die Art eines Punkts; unbekannte Werte gelten als Aufgabe."""
        if isinstance(item, dict) and item.get("kind") == cls.ITEM_KIND_GROUP:
            return cls.ITEM_KIND_GROUP
        return cls.ITEM_KIND_TASK

    @classmethod
    def is_group_item(cls, item):
        return cls.item_kind(item) == cls.ITEM_KIND_GROUP

    def set_item_kind(self, item, kind):
        """Wandelt zwischen Aufgabe und Gruppe und räumt die Statusfelder auf."""
        if not isinstance(item, dict):
            return False
        new_kind = self.ITEM_KIND_GROUP if kind == self.ITEM_KIND_GROUP else self.ITEM_KIND_TASK
        if self.item_kind(item) == new_kind:
            return False
        item["kind"] = new_kind
        if new_kind == self.ITEM_KIND_GROUP:
            item["done"] = False
            item["due"] = None
            item["importance"] = 0
        return True

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
        source_size = os.path.getsize(source_path)
        if source_size > self.MAX_BACKUP_ATTACHMENT_BYTES:
            raise OSError(
                "Die Datei ist größer als 512 MB und kann deshalb nicht in ein "
                "vollständiges Glide-Backup aufgenommen werden."
            )
        original_name = os.path.basename(source_path)
        attachment_id = uuid.uuid4().hex
        # Gemeinsame, geprüfte Namensbildung mit dem Backup-Import. Der Pfad wird
        # vor dem Kopieren validiert, damit keine unauffindbare Datei entsteht.
        stored_name = self.safe_attachment_filename(original_name, attachment_id)
        storage = f"attachments/{stored_name}"
        self.validate_attachment_storage(storage)
        destination = os.path.join(ATTACHMENTS_DIR, stored_name)
        temp_path = None
        try:
            temp_handle, temp_path = tempfile.mkstemp(prefix=".attachment-", suffix=".tmp", dir=ATTACHMENTS_DIR)
            os.close(temp_handle)
            shutil.copy2(source_path, temp_path)
            copied_size = os.path.getsize(temp_path)
            if copied_size > self.MAX_BACKUP_ATTACHMENT_BYTES:
                raise OSError(
                    "Die Datei ist größer als 512 MB und kann deshalb nicht in ein "
                    "vollständiges Glide-Backup aufgenommen werden."
                )
            os.replace(temp_path, destination)
            temp_path = None
        finally:
            if temp_path:
                try:
                    os.remove(temp_path)
                except OSError:
                    pass
        mime, _encoding = mimetypes.guess_type(original_name)
        return {
            "id": attachment_id,
            "name": original_name,
            "storage": storage,
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

    def normalize_items(self, data, seen_ids=None, depth=0, counter=None, known_label_ids=None):
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
                children = self.normalize_items(
                    entry.get("children", []), seen_ids, depth + 1, counter, known_label_ids
                )
                importance = entry.get("importance", entry.get("priority", 0))
                due = entry.get("due")
                description = str(entry.get("description") or "")
                attachments = self.normalize_attachments(entry.get("attachments", []))
                color = entry.get("color") if entry.get("color") in self.ITEM_COLOR_KEYS else None
                # Migration auf Format 6: ein fehlendes oder unbekanntes 'kind'
                # bedeutet eine gewöhnliche Aufgabe. Bestehende Daten bleiben
                # dadurch unverändert gültig.
                kind = self.ITEM_KIND_GROUP if entry.get("kind") == self.ITEM_KIND_GROUP else self.ITEM_KIND_TASK
                # Migration auf Format 7: fehlende Labels bedeuten „keine Labels“.
                # Unbekannte Label-IDs werden verworfen, damit keine Zeile auf ein
                # gelöschtes Label verweist.
                labels = self.normalize_item_labels(entry.get("labels"), known_label_ids)
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
                        kind,
                        labels,
                    )
                )
        return normalized

    def load_items(self):
        if not os.path.exists(SAVE_FILE):
            self.folders = []
            self.labels = []
            self.trash = []
            default_list = self.new_list_object(self.app_title, [])
            self.lists = [default_list]
            self.ensure_inbox_list()
            self.active_list_id = default_list["id"]
            self.active_folder_id = None
            self.view_mode = "list"
            self.items = default_list["items"]
            self.update_entry_mode()
            self.update_page_note_preview()
            self.update_page_labels()
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
            requested_system_view = self.view_mode if self.view_mode in ("in_progress", "trash") else None
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
            elif requested_system_view:
                self._activate_system_view(requested_system_view, refresh=False)
            self.update_sidebar_list()
            self.refresh_tree()
            if inbox_repaired:
                self.save_items()
        except (json.JSONDecodeError, ValueError, RecursionError, tk.TclError) as e:
            messagebox.showerror("Fehler", f"Die Speicherdatei ist beschädigt oder ungültig:\n{e}")
            self.folders = []
            self.labels = []
            self.trash = []
            default_list = self.new_list_object(self.app_title, [])
            self.lists = [default_list]
            self.ensure_inbox_list()
            self.active_list_id = default_list["id"]
            self.active_folder_id = None
            self.view_mode = "list"
            self.items = default_list["items"]
            self.update_entry_mode()
            self.update_page_note_preview()
            self.update_page_labels()
            self.update_sidebar_list()
            self.refresh_tree()
        except OSError as e:
            messagebox.showerror("Fehler", f"Die Speicherdatei konnte nicht gelesen werden:\n{e}")
            self.folders = []
            self.labels = []
            self.trash = []
            default_list = self.new_list_object(self.app_title, [])
            self.lists = [default_list]
            self.ensure_inbox_list()
            self.active_list_id = default_list["id"]
            self.active_folder_id = None
            self.view_mode = "list"
            self.items = default_list["items"]
            self.update_entry_mode()
            self.update_page_note_preview()
            self.update_page_labels()
            self.update_sidebar_list()
            self.refresh_tree()

    def data_payload(self, lists=None, folders=None, active_list_id=None, active_folder_id=None,
                     labels=None, trash=None):
        return {
            "version": self.DATA_SCHEMA_VERSION,
            "active_list_id": self.active_list_id if active_list_id is None else active_list_id,
            "active_folder_id": (
                self.active_folder_id if self.view_mode == "folder" else None
            ) if active_folder_id is None else active_folder_id,
            "folders": self.folders if folders is None else folders,
            "labels": self.labels if labels is None else labels,
            "lists": self.lists if lists is None else lists,
            "trash": self.trash if trash is None else trash,
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

    def save_items(self, *, show_error=True, force_backup=False):
        self.dirty = True
        backup_warning = None
        try:
            self.sync_current_list_reference()
            backup_warning = self.write_backup_copy(force=force_backup)
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

    def write_backup_copy(self, force=False):
        """Legt eine automatische Sicherung des zuletzt gespeicherten Standes an.

        Ohne ``force`` greift eine Zeitsperre: bei jedem Tastendruck eine eigene
        Datei anzulegen würde den Ordner fluten und die tatsächlich nützlichen
        Rückfallstände verdrängen. Der zeitgesteuerte Sicherungspunkt des
        Autosave setzt die Sperre bewusst außer Kraft.

        Rückgabe: Fehlertext, falls die Sicherung nicht möglich war, sonst None.
        Ein defekter Backup-Ordner darf das Speichern der Nutzdaten nie
        verhindern.
        """
        if not os.path.exists(SAVE_FILE):
            return None
        now = self.monotonic_seconds()
        last = self._last_backup_monotonic
        if not force and last is not None and (now - last) < self.BACKUP_MIN_INTERVAL_SECONDS:
            return None
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            backup_file = os.path.join(BACKUP_DIR, f"liste_backup_{timestamp}.json")
            os.makedirs(BACKUP_DIR, exist_ok=True)
            shutil.copy2(SAVE_FILE, backup_file)
            self._last_backup_monotonic = now
            self.prune_backups()
            return None
        except OSError as exc:
            return str(exc)

    @staticmethod
    def monotonic_seconds():
        """Monotone Zeitbasis – unabhängig von Zeitzonen- und Uhrzeitkorrekturen."""
        return time.monotonic()

    def prune_backups(self):
        """Rotiert automatische Sicherungen nach Mindestbestand, Alter und Obergrenze.

        Reihenfolge und Begründung:
        1. Die neuesten MIN_BACKUPS Sicherungen bleiben immer erhalten – auch
           wenn sie älter als das Höchstalter sind. Sonst stünde nach einer
           längeren Pause keine Rückfallebene mehr bereit.
        2. Aus dem Rest verschwinden alle, die älter als BACKUP_MAX_AGE_MINUTES
           sind.
        3. Zuletzt begrenzt MAX_BACKUPS die verbleibende Menge.

        Portable Sicherungen (`vor_import_*.glidebackup`) fallen bewusst nicht
        unter diese Rotation: sie sind die Rückfallebene eines Imports.
        """
        try:
            backups = [
                os.path.join(BACKUP_DIR, name)
                for name in os.listdir(BACKUP_DIR)
                if name.startswith("liste_backup_") and name.endswith(".json")
            ]
        except OSError:
            return
        if not backups:
            return

        def mtime(path):
            try:
                return os.path.getmtime(path)
            except OSError:
                return 0.0

        backups.sort(key=mtime, reverse=True)  # neueste zuerst
        protected = backups[: self.MIN_BACKUPS]
        candidates = backups[self.MIN_BACKUPS:]
        max_age_seconds = self.BACKUP_MAX_AGE_MINUTES * 60
        now = datetime.now().timestamp()
        survivors = []
        for path in candidates:
            if now - mtime(path) > max_age_seconds:
                try:
                    os.remove(path)
                except OSError:
                    survivors.append(path)
                continue
            survivors.append(path)
        remaining = protected + survivors
        if len(remaining) > self.MAX_BACKUPS:
            for path in remaining[self.MAX_BACKUPS:]:
                try:
                    os.remove(path)
                except OSError:
                    pass

    # -----------------------------
    # Automatisches Speichern
    # -----------------------------
    def schedule_autosave(self):
        """Startet den zeitgesteuerten Speicher- und Sicherungszyklus."""
        if not hasattr(self, "root"):
            return
        interval_ms = max(1, int(self.AUTOSAVE_INTERVAL_MINUTES * 60 * 1000))
        try:
            self._autosave_id = self._register_after(self.root.after(interval_ms, self.autosave_tick))
        except tk.TclError:
            self._autosave_id = None

    def autosave_tick(self):
        """Sichert regelmäßig, ohne den Nutzer mit Dialogen zu unterbrechen.

        Ein noch nicht gespeicherter Stand wird erneut geschrieben; andernfalls
        entsteht ein garantierter Sicherungspunkt. Fehler bleiben still, weil
        ein modaler Dialog im Hintergrund die Arbeit unterbrechen würde – der
        nächste manuelle Speichervorgang meldet das Problem sichtbar.
        """
        self._after_ids.discard(self._autosave_id)
        self._autosave_id = None
        try:
            if self.dirty:
                self.save_items(show_error=False, force_backup=True)
            else:
                self.write_backup_copy(force=True)
        except Exception:
            pass
        finally:
            self.schedule_autosave()

    def walk_items(self, items=None):
        if items is None:
            items = self.items
        for item in items:
            yield item
            yield from self.walk_items(item.get("children", []))

    def find_item(self, item_id, items=None, parent_list=None, parent_item=None):
        if items is None:
            items = self.items
            parent_item = None

        for index, item in enumerate(items):
            if item.get("id") == item_id:
                return item, items, index, parent_item
            found = self.find_item(item_id, item.get("children", []), item.get("children", []), item)
            if found:
                return found
        return None

    def find_item_in_lists(self, item_id):
        """Sucht einen Punkt über alle Listen hinweg.

        Wird von der abgeleiteten Ansicht „In Bearbeitung“ benötigt, deren
        Zeilen auf Aufgaben fremder Listen verweisen.
        """
        if not item_id:
            return None
        for entry in self.lists:
            found = self.find_item(item_id, entry.get("items", []), entry.get("items", []), None)
            if found:
                return found[0], found[1], found[2], entry
        return None

    def update_in_progress_item(self, item_id, field, value):
        """Ändert eine Aufgabe direkt aus der Ansicht „In Bearbeitung“ heraus."""
        found = self.find_item_in_lists(item_id)
        if not found:
            return "break"
        item = found[0]
        if field == "due":
            new_value = self.normalize_due(value) if value else None
            if value and new_value is None:
                messagebox.showwarning("Fälligkeit", "Das Fälligkeitsdatum ist ungültig.")
                return "break"
        elif field == "importance":
            new_value = self.clamp_importance(value)
        elif field == "color":
            new_value = value if value in self.ITEM_COLOR_KEYS else None
        elif field == "done":
            new_value = bool(value)
        else:
            return "break"
        if item.get(field) == new_value:
            return "break"
        self.snapshot_undo()
        item[field] = new_value
        self.save_items()
        self.refresh_tree()
        return "break"

    def edit_in_progress_item(self, item_id):
        """Öffnet den Detaildialog für eine Aufgabe aus einer fremden Liste."""
        found = self.find_item_in_lists(item_id)
        if not found:
            return "break"
        item = found[0]
        details = self.themed_item_details_dialog(item)
        if details is None:
            return "break"
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
            self.refresh_tree()
        return "break"

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
        expanded = set(self.expanded_ids)
        collapsed = set(self.collapsed_item_ids)
        for item in self.walk_items():
            item_id = item.get("id")
            try:
                if not item_id or not self.tree.exists(item_id) or not item.get("children"):
                    continue
                if self.tree.item(item_id, "open"):
                    expanded.add(item_id)
                    collapsed.discard(item_id)
                else:
                    collapsed.add(item_id)
                    expanded.discard(item_id)
            except tk.TclError:
                pass
        self.expanded_ids = expanded
        self.collapsed_item_ids = collapsed

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
        if self.is_group_item(item):
            # Eine Gruppe hat keinen eigenen Erledigt-Zustand. Bei aktivem
            # Statusfilter bleibt sie nur sichtbar, wenn ein Unterpunkt passt –
            # das übernimmt item_visible_by_filter.
            return mode == "all"
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
            if self.current_focus_widget() != self.search_entry:
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
        focus = self.current_focus_widget()
        if focus == getattr(self, "search_entry", None) and self.search_var.get():
            self.clear_search()
        elif focus == getattr(self, "entry", None):
            if not getattr(self, "entry_placeholder_active", False):
                self.entry.delete(0, tk.END)
        else:
            self.clear_tree_selection()
        return "break"

    def compute_stats(self, items):
        """Fortschritt über echte Aufgaben; Gruppen sind reine Behälter."""
        total = 0
        done = 0
        overdue = 0
        for item in self.walk_items(items):
            if self.is_group_item(item):
                continue
            total += 1
            if item.get("done"):
                done += 1
            elif self.due_status(item) == "overdue":
                overdue += 1
        return total, done, overdue

    def _set_stats_text(self, text):
        """Setzt die Fortschrittszeile und bewertet danach die Titelbreite neu."""
        try:
            self.stats_label.configure(text=text)
        except tk.TclError:
            return
        self.update_header_title()

    def update_stats_label(self):
        if not hasattr(self, "stats_label"):
            return
        if self.view_mode == "trash":
            folders = sum(1 for entry in self.trash if entry.get("kind") == self.TRASH_KIND_FOLDER)
            lists = len(self.trash) - folders
            if not self.trash:
                self._set_stats_text("Papierkorb ist leer")
            else:
                self._set_stats_text(f"{lists} Liste(n) · {folders} Ordner im Papierkorb")
            return
        if self.view_mode == "in_progress":
            due_entries = self.get_in_progress_items(apply_filters=False)
            done = sum(1 for _due, _list_index, _item_index, _entry, item in due_entries if item.get("done"))
            overdue = sum(1 for _due, _list_index, _item_index, _entry, item in due_entries if self.due_status(item) == "overdue")
            text = f"{len(due_entries)} Aufgaben mit Fälligkeit"
            if due_entries:
                text += f" · {len(due_entries) - done} offen"
            if overdue:
                text += f" · {overdue} überfällig"
            self._set_stats_text(text)
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
            self._set_stats_text(text)
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
        self._set_stats_text(text)

    def refresh_tree(self, selected_id=None):
        if not hasattr(self, "tree"):
            return

        # Die Labelspalte erscheint erst, sobald Labels existieren.
        self.sync_task_tree_columns()

        if self.view_mode == "in_progress":
            self.refresh_in_progress_overview(selected_id=selected_id)
            return
        if self.view_mode == "trash":
            self.refresh_trash_overview(selected_id=selected_id)
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

    def get_in_progress_items(self, apply_filters=True):
        """Liefert fällige Aufgaben als abgeleitete Referenzen, ohne sie zu kopieren."""
        results = []
        query = self.current_search_query() if apply_filters else ""
        for list_index, entry in enumerate(self.lists):
            for item_index, item in enumerate(self.walk_items(entry.get("items", []))):
                if self.is_group_item(item):
                    continue
                due_value = self.normalize_due(item.get("due"))
                if not due_value:
                    continue
                if apply_filters and (
                    not self.item_text_matches_query(item, query)
                    or not self.item_matches_status_filter(item)
                ):
                    continue
                results.append((due_value, list_index, item_index, entry, item))
        results.sort(key=lambda value: (value[0], value[1], value[2]))
        return results

    def refresh_in_progress_overview(self, selected_id=None):
        """Zeigt alle fälligen Aufgaben chronologisch und navigierbar in einer flachen Ansicht."""
        if not hasattr(self, "tree"):
            return
        self.update_stats_label()
        current_selection = selected_id or self.tree.focus()
        for row_id in self.tree.get_children(""):
            self.tree.delete(row_id)
        self.in_progress_item_sources = {}

        entries = self.get_in_progress_items(apply_filters=True)
        if not entries:
            empty_text = (
                "Keine fälligen Aufgaben passen zum aktuellen Filter."
                if self.has_active_filter()
                else "Noch keine Aufgaben mit Fälligkeitsdatum vorhanden."
            )
            self.tree.insert("", "end", iid=self.EMPTY_ROW_ID, text=empty_text, tags=("empty",))
            self.schedule_scrollbar_refresh()
            return

        for due_value, _list_index, _item_index, source_list, item in entries:
            item_id = item.get("id") or uuid.uuid4().hex
            item["id"] = item_id
            list_id = source_list.get("id")
            row_id = f"in-progress:{list_id}:{item_id}"
            self.in_progress_item_sources[row_id] = (list_id, item_id)
            importance = self.clamp_importance(item.get("importance", 0))
            flag_prefix = self.IMPORTANCE_MARKERS.get(importance, "")
            done_prefix = "✓ " if item.get("done") else ""
            description_suffix = "   📝" if str(item.get("description") or "").strip() else ""
            attachment_count = len(item.get("attachments", []))
            attachment_suffix = f"   📎 {attachment_count}" if attachment_count else ""
            source_title = str(source_list.get("title") or "Liste").strip() or "Liste"
            source_folder = self.get_folder(source_list.get("folder_id"))
            if source_folder:
                folder_title = str(source_folder.get("title") or "Ordner").strip() or "Ordner"
                source_title = f"{folder_title} › {source_title}"
            number_path = self.get_item_number_path(item_id, source_list.get("items", [])) or []
            number_text = ".".join(str(part) for part in number_path)
            task_prefix = f"{number_text}. " if number_text else ""
            row_text = (
                f"{source_title}   —   {task_prefix}{flag_prefix}{done_prefix}{item.get('text', '')}"
                f"{description_suffix}{attachment_suffix}"
            )
            color_key = item.get("color") if item.get("color") in self.ITEM_COLOR_KEYS else None
            due_state = self.due_status(item)
            if color_key:
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
                "",
                "end",
                iid=row_id,
                text=row_text,
                values=(f"📅 {self.format_due_display(due_value)}", self.format_item_labels(item), ""),
                tags=(tag,),
            )

        if current_selection and self.tree.exists(current_selection):
            self.tree.selection_set(current_selection)
            self.tree.focus(current_selection)
            self.tree.see(current_selection)
        self.schedule_scrollbar_refresh()

    def refresh_trash_overview(self, selected_id=None):
        """Zeigt alle gelöschten Listen und Ordner mit Herkunft und Löschzeitpunkt."""
        if not hasattr(self, "tree"):
            return
        self.update_stats_label()
        current_selection = selected_id or self.tree.focus()
        for row_id in self.tree.get_children(""):
            self.tree.delete(row_id)

        query = self.current_search_query()
        entries = list(self.trash)
        if query:
            entries = [entry for entry in entries if query in self.trash_entry_title(entry).lower()]
        if not entries:
            empty_text = (
                "Kein Eintrag im Papierkorb passt zur aktuellen Suche."
                if query
                else "Der Papierkorb ist leer. Gelöschte Listen und Ordner landen hier und bleiben wiederherstellbar."
            )
            self.tree.insert("", "end", iid=self.EMPTY_ROW_ID, text=empty_text, tags=("empty",))
            self.schedule_scrollbar_refresh()
            return

        for entry in entries:
            payload = self.trash_entry_payload(entry) or {}
            title = self.trash_entry_title(entry)
            is_folder = entry.get("kind") == self.TRASH_KIND_FOLDER
            if is_folder:
                detail = "Ordner"
                related = sum(
                    1
                    for other in self.trash
                    if other.get("kind") == self.TRASH_KIND_LIST
                    and other.get("origin_folder_id") == payload.get("id")
                )
                if related:
                    detail += f" · {related} Liste(n) im Papierkorb"
            else:
                detail = f"Liste · {self.count_items(payload.get('items', []))} Punkte"
                origin = str(entry.get("origin_folder_title") or "").strip()
                if origin:
                    detail += f" · aus „{origin}“"
            marker = "\U0001F4C1" if is_folder else "▸"
            row_text = f"{marker}  {title}   —   {detail}"
            color_key = payload.get("color") if payload.get("color") in self.LIST_COLOR_KEYS else None
            tags = (f"listcolor_{color_key}",) if color_key else ("folder_list",)
            self.tree.insert(
                "",
                "end",
                iid=f"trash:{entry.get('id')}",
                text=row_text,
                values=(f"\U0001F5D1 {self.format_trash_timestamp(entry.get('deleted_at'))}", "", ""),
                tags=tags,
            )

        if current_selection and self.tree.exists(current_selection):
            self.tree.selection_set(current_selection)
            self.tree.focus(current_selection)
        self.schedule_scrollbar_refresh()

    @staticmethod
    def format_trash_timestamp(value, with_time=False):
        try:
            parsed = datetime.fromisoformat(str(value))
        except (TypeError, ValueError):
            return ""
        return parsed.strftime("%d.%m.%Y %H:%M" if with_time else "%d.%m.%Y")

    def build_trash_context_menu(self, row_id=None):
        """Kontextmenü des Papierkorbs – für eine Zeile oder den leeren Bereich."""
        trash_ids = self.get_selected_trash_ids()
        menu = self._new_themed_popup_menu()
        if trash_ids:
            if len(trash_ids) == 1:
                entry = self.get_trash_entry(trash_ids[0])
                menu.add_command(label=self.ellipsize_sidebar_title(self.trash_entry_title(entry)), state="disabled")
            else:
                menu.add_command(label=f"{len(trash_ids)} Einträge ausgewählt", state="disabled")
        else:
            menu.add_command(label=f"Papierkorb ({len(self.trash)})", state="disabled")
        menu.add_separator()
        menu.add_command(
            label="Wiederherstellen",
            command=lambda: self.restore_selected_trash_entries(False),
            state="normal" if trash_ids else "disabled",
        )
        menu.add_command(
            label="In Ordner wiederherstellen …",
            command=lambda: self.restore_selected_trash_entries(True),
            state="normal" if trash_ids and self.folders else "disabled",
        )
        menu.add_separator()
        menu.add_command(
            label="Endgültig entfernen",
            command=self.purge_selected_trash_entries,
            foreground=self.theme["delete"],
            state="normal" if trash_ids else "disabled",
        )
        menu.add_command(
            label="Papierkorb leeren",
            command=self.empty_trash,
            foreground=self.theme["delete"],
            state="normal" if self.trash else "disabled",
        )
        return menu

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
            # Labels einer Liste erscheinen ausschließlich in dieser großen
            # Darstellung, nicht in der Seitenleiste.
            self.tree.insert(
                "", "end", iid=iid, text=row_text,
                values=("", self.format_item_labels(entry), ""),
                tags=tags,
            )

        if current_selection and self.tree.exists(current_selection):
            self.tree.selection_set(current_selection)
            self.tree.focus(current_selection)
        self.schedule_scrollbar_refresh()

    @staticmethod
    def folder_list_id_from_iid(row_id):
        prefix = "folder-list:"
        if row_id and str(row_id).startswith(prefix):
            return str(row_id)[len(prefix):]
        return None

    def get_selected_folder_list_id(self, event=None):
        row_id = ""
        if event is not None and self.is_mouse_event(event):
            row_id = self.tree.identify_row(event.y)
        if not row_id:
            row_id = self.tree.focus()
        return self.folder_list_id_from_iid(row_id)

    def activate_tree_row(self, event=None):
        if self.view_mode == "in_progress":
            return self.open_in_progress_source_item(event)
        if self.view_mode == "trash":
            return self.restore_selected_trash_entries(False)
        if self.view_mode == "folder":
            list_id = self.get_selected_folder_list_id(event)
            if list_id:
                self.set_active_list(list_id)
            return "break"
        return self.toggle_done(event)

    def open_in_progress_source_item(self, event=None):
        """Öffnet die echte Quellliste einer Zeile aus „In Bearbeitung“."""
        row_id = ""
        if event is not None and self.is_mouse_event(event):
            row_id = self.tree.identify_row(event.y)
        if not row_id:
            row_id = self.tree.focus()
        source = self.in_progress_item_sources.get(row_id)
        if not source:
            return "break"
        list_id, item_id = source
        self.set_active_list(list_id, refresh=False)
        self.update_sidebar_list()
        self.refresh_tree(selected_id=item_id)
        if self.tree.exists(item_id):
            parent_id = self.tree.parent(item_id)
            while parent_id:
                self.tree.item(parent_id, open=True)
                self.expanded_ids.add(parent_id)
                self.collapsed_item_ids.discard(parent_id)
                parent_id = self.tree.parent(parent_id)
            self.tree.selection_set(item_id)
            self.tree.focus(item_id)
            self.tree.see(item_id)
        self.save_settings()
        return "break"

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
            is_group = self.is_group_item(item)
            importance = 0 if is_group else self.clamp_importance(item.get("importance", 0))
            item["importance"] = importance
            flag_prefix = self.IMPORTANCE_MARKERS.get(importance, "")
            done_prefix = "✓ " if item.get("done") and not is_group else ""
            due_state = "" if is_group else self.due_status(item)
            due_text = "" if is_group else self.format_due_display(item.get("due"))
            due_value = f"\U0001F4C5 {due_text}" if due_text else ""
            description_suffix = "   📝" if str(item.get("description") or "").strip() else ""
            attachment_count = len(item.get("attachments", []))
            attachment_suffix = f"   📎 {attachment_count}" if attachment_count else ""
            if is_group:
                # Eine Gruppe zeigt statt eines Status die Zahl enthaltener Aufgaben.
                contained = self.count_items(item.get("children", []))
                group_suffix = f"   ({contained})"
                row_text = (
                    f"{number_text}. {self.GROUP_MARKER}{item.get('text', '')}"
                    f"{group_suffix}{description_suffix}{attachment_suffix}"
                )
            else:
                row_text = (
                    f"{number_text}. {flag_prefix}{done_prefix}{item.get('text', '')}"
                    f"{description_suffix}{attachment_suffix}"
                )
            item_id = item.get("id") or uuid.uuid4().hex
            item["id"] = item_id
            has_children = bool(item.get("children"))
            should_open = (
                bool(query)
                or item_id in self.expanded_ids
                or (parent_id == "" and item_id not in self.collapsed_item_ids)
            )
            color_key = item.get("color") if item.get("color") in self.ITEM_COLOR_KEYS else None
            item["color"] = color_key
            if color_key:
                # Eine bewusst gewählte Aufgabenfarbe hat Vorrang. Status,
                # Fälligkeit und Wichtigkeit bleiben über Marker/Text sichtbar.
                tag = f"itemcolor_{color_key}"
            elif is_group:
                tag = "group_item"
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
                values=(due_value, self.format_item_labels(item), ""),
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
        focused = self.current_focus_widget()
        if focused is not None and focused in (getattr(self, "entry", None), getattr(self, "search_entry", None)):
            try:
                focused.selection_range(0, tk.END)
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
                "labels": copy.deepcopy(self.labels),
                "trash": copy.deepcopy(self.trash),
                "active_list_id": self.active_list_id,
                "active_folder_id": self.active_folder_id if self.view_mode == "folder" else None,
                "view_mode": self.view_mode,
            }
        )
        if len(self.undo_stack) > 20:
            self.undo_stack.pop(0)

    def undo_last_change(self, event=None):
        if event is not None and isinstance(self.current_focus_widget(), (tk.Entry, tk.Text, ttk.Entry)):
            # In Textfeldern bleibt echtes Strg+Z eine lokale Texteingabe-Aktion.
            return None
        if not self.undo_stack:
            messagebox.showinfo("Rückgängig", "Es gibt keine Änderung zum Rückgängigmachen.")
            return "break"
        snapshot = self.undo_stack.pop()
        self.lists = copy.deepcopy(snapshot.get("lists", []))
        self.folders = copy.deepcopy(snapshot.get("folders", []))
        self.labels = copy.deepcopy(snapshot.get("labels", []))
        self.trash = copy.deepcopy(snapshot.get("trash", []))
        self.ensure_inbox_list()
        desired_list_id = snapshot.get("active_list_id")
        if desired_list_id not in [entry.get("id") for entry in self.lists]:
            desired_list_id = self.lists[0].get("id")
        desired_folder_id = snapshot.get("active_folder_id")
        desired_view_mode = snapshot.get("view_mode")
        self.active_list_id = None
        self.active_folder_id = None
        self.view_mode = "list"
        self.set_active_list(desired_list_id, refresh=False)
        if desired_folder_id and self.get_folder(desired_folder_id):
            self.set_active_folder(desired_folder_id, refresh=False)
        elif desired_view_mode in ("in_progress", "trash"):
            self._activate_system_view(desired_view_mode, refresh=False)
        self.save_items()
        self.update_sidebar_list()
        self.refresh_tree()
        return "break"

    def format_item_lines(self, item, number_prefix, level=0):
        number_text = ".".join(str(part) for part in number_prefix)
        indent = "   " * level
        if self.is_group_item(item):
            flag_prefix, done_prefix = self.GROUP_MARKER, ""
        else:
            flag_prefix = self.IMPORTANCE_MARKERS.get(self.clamp_importance(item.get("importance", 0)), "")
            done_prefix = "✓ " if item.get("done") else ""
        lines = [f"{indent}{number_text}. {flag_prefix}{done_prefix}{item.get('text', '')}"]
        description = str(item.get("description") or "").strip()
        if description:
            lines.extend(f"{indent}   Beschreibung: {line}" for line in description.splitlines())
        label_names = self.format_item_label_names(item)
        if label_names:
            lines.append(f"{indent}   Labels: {label_names}")
        for attachment in item.get("attachments", []):
            lines.append(f"{indent}   Anhang: {attachment.get('name', 'Datei')}")
        for index, child in enumerate(item.get("children", []), start=1):
            lines.extend(self.format_item_lines(child, number_prefix + [index], level + 1))
        return lines

    def copy_selected_to_clipboard(self, event=None):
        if self.current_focus_widget() in (getattr(self, "entry", None), getattr(self, "search_entry", None)):
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
        if self.current_focus_widget() in (getattr(self, "entry", None), getattr(self, "search_entry", None)):
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

            kind = self.ITEM_KIND_TASK
            if text.startswith(self.GROUP_MARKER.strip()):
                kind = self.ITEM_KIND_GROUP
                text = text[len(self.GROUP_MARKER.strip()):].strip()

            for marker, marker_importance in (("🚩 ", 3), ("⚑ ", 2), ("⚐ ", 1)):
                if text.startswith(marker):
                    importance = marker_importance
                    text = text[len(marker):].strip()
                    break

            if text.startswith("✓ ") or text.startswith("✅ "):
                done = True
                text = text[2:].strip()

            if text:
                plain_items.append(self.new_item(text, done=done, importance=importance, kind=kind))

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
        if self.view_mode == "in_progress":
            messagebox.showinfo(
                "In Bearbeitung",
                "Die Ansicht wird automatisch aus den Quelllisten erzeugt. Öffne dort eine Aufgabe oder Liste.",
            )
            return
        if self.view_mode == "trash":
            messagebox.showinfo(
                "Papierkorb",
                "Im Papierkorb lassen sich Einträge nur wiederherstellen oder endgültig entfernen.",
            )
            return
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
        if event is not None and self.current_focus_widget() in (self.entry, getattr(self, "search_entry", None)):
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

    # -----------------------------
    # Aktionen der erweiterten Kontextmenüs
    # -----------------------------
    def add_child_item(self, parent_id=None):
        """Legt einen Unterpunkt unter dem gewählten Punkt an."""
        if not self.require_list_view():
            return "break"
        parent_id = parent_id or self.get_selected_item_id()
        if not parent_id:
            return "break"
        found = self.find_item(parent_id)
        if not found:
            return "break"
        title = self.themed_input_dialog("Neuer Unterpunkt", "Titel des Unterpunkts:", ok_text="Anlegen")
        if title is None:
            return "break"
        title = title.strip()
        if not title:
            messagebox.showwarning("Hinweis", "Bitte einen Titel eingeben.")
            return "break"
        self.snapshot_undo()
        child = self.new_item(title, False)
        found[0].setdefault("children", []).append(child)
        self.expanded_ids.add(parent_id)
        self.collapsed_item_ids.discard(parent_id)
        self.save_items()
        self.refresh_tree(selected_id=child["id"])
        return "break"

    def add_sibling_item(self, kind=ITEM_KIND_TASK, reference_id=None):
        """Legt einen Punkt oder eine Gruppe auf derselben Ebene an."""
        if not self.require_list_view():
            return "break"
        is_group = kind == self.ITEM_KIND_GROUP
        title = self.themed_input_dialog(
            "Neue Gruppe" if is_group else "Neuer Punkt",
            "Titel der Gruppe:" if is_group else "Titel des Punkts:",
            ok_text="Anlegen",
        )
        if title is None:
            return "break"
        title = title.strip()
        if not title:
            messagebox.showwarning("Hinweis", "Bitte einen Titel eingeben.")
            return "break"
        reference_id = reference_id or self.get_selected_item_id()
        self.snapshot_undo()
        new_entry = self.new_item(title, False, kind=kind)
        target_list = self.items
        insert_index = len(target_list)
        if reference_id:
            found = self.find_item(reference_id)
            if found:
                _item, siblings, index, _parent = found
                target_list = siblings
                insert_index = index + 1
        target_list.insert(insert_index, new_entry)
        self.save_items()
        self.refresh_tree(selected_id=new_entry["id"])
        return "break"

    def convert_selected_kind(self, kind):
        """Wandelt die Auswahl zwischen Aufgabe und Gruppe um."""
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
            if found and self.set_item_kind(found[0], kind):
                changed = True
        if not changed:
            if self.undo_stack:
                self.undo_stack.pop()
            return "break"
        self.save_items()
        self.refresh_tree(selected_id=item_ids[-1])
        self._restore_item_selection(item_ids)
        return "break"

    def group_selected_items(self):
        """Fasst die ausgewählten Punkte in einer neuen Gruppe zusammen."""
        if not self.require_list_view():
            return "break"
        item_ids = self.filter_top_level_selection(
            [item_id for item_id in self.iter_tree_ids() if item_id in set(self.get_selected_item_ids())]
        )
        if not item_ids:
            messagebox.showwarning("Hinweis", "Zuerst mindestens einen Punkt auswählen.")
            return "break"
        first_found = self.find_item(item_ids[0])
        if not first_found:
            return "break"
        # Alle Punkte müssen dieselbe Ebene teilen, sonst wäre das Ergebnis nicht vorhersehbar.
        target_siblings = first_found[1]
        for item_id in item_ids[1:]:
            found = self.find_item(item_id)
            if not found or found[1] is not target_siblings:
                messagebox.showinfo(
                    "Gruppieren",
                    "Nur Punkte derselben Ebene lassen sich gemeinsam gruppieren.",
                )
                return "break"
        title = self.themed_input_dialog("Neue Gruppe", "Titel der Gruppe:", ok_text="Gruppieren")
        if title is None:
            return "break"
        title = title.strip()
        if not title:
            messagebox.showwarning("Hinweis", "Bitte einen Titel eingeben.")
            return "break"
        insert_index = first_found[2]
        self.snapshot_undo()
        moved = []
        for item_id in item_ids:
            removed = self.remove_item_by_id(item_id)
            if removed:
                moved.append(removed)
        if not moved:
            if self.undo_stack:
                self.undo_stack.pop()
            return "break"
        group = self.new_item(title, False, children=moved, kind=self.ITEM_KIND_GROUP)
        insert_index = max(0, min(insert_index, len(target_siblings)))
        target_siblings.insert(insert_index, group)
        self.expanded_ids.add(group["id"])
        self.collapsed_item_ids.discard(group["id"])
        self.save_items()
        self.refresh_tree(selected_id=group["id"])
        return "break"

    def dissolve_selected_group(self):
        """Löst eine Gruppe auf; die Unterpunkte rücken an ihre Stelle."""
        if not self.require_list_view():
            return "break"
        item_id = self.get_selected_item_id()
        found = self.find_item(item_id) if item_id else None
        if not found or not self.is_group_item(found[0]):
            return "break"
        group, siblings, index, _parent = found
        children = list(group.get("children", []))
        self.snapshot_undo()
        siblings.pop(index)
        for offset, child in enumerate(children):
            siblings.insert(index + offset, child)
        self.save_items()
        self.refresh_tree(selected_id=children[0]["id"] if children else None)
        return "break"

    def copy_items_with_new_ids(self, items):
        """Tiefe Kopie mit frischen IDs für jeden Punkt und Anhang.

        Ohne neue IDs entstünden Dubletten: der Aufgabenbaum verweigert
        doppelte Zeilen-IDs, und listenübergreifende Suchen träfen den falschen
        Punkt. Anhänge behalten ihren Speicherpfad – die Datei wird geteilt,
        nicht kopiert.
        """
        duplicated = copy.deepcopy(items if isinstance(items, list) else [])
        stack = list(duplicated)
        while stack:
            item = stack.pop()
            if not isinstance(item, dict):
                continue
            item["id"] = uuid.uuid4().hex
            for attachment in item.get("attachments", []):
                if isinstance(attachment, dict):
                    attachment["id"] = uuid.uuid4().hex
            children = item.get("children", [])
            if isinstance(children, list):
                stack.extend(children)
        return duplicated

    def duplicate_selected_items(self):
        """Legt eine unabhängige Kopie der Auswahl direkt darunter an."""
        if not self.require_list_view():
            return "break"
        item_ids = self.filter_top_level_selection(
            [item_id for item_id in self.iter_tree_ids() if item_id in set(self.get_selected_item_ids())]
        )
        if not item_ids:
            messagebox.showwarning("Hinweis", "Zuerst einen Punkt auswählen.")
            return "break"
        self.snapshot_undo()
        created = []
        for item_id in item_ids:
            found = self.find_item(item_id)
            if not found:
                continue
            item, siblings, index, _parent = found
            copy_item = self.copy_items_with_new_ids([item])
            if not copy_item:
                continue
            siblings.insert(index + 1, copy_item[0])
            created.append(copy_item[0]["id"])
        if not created:
            if self.undo_stack:
                self.undo_stack.pop()
            return "break"
        self.save_items()
        self.refresh_tree(selected_id=created[-1])
        return "break"

    def move_selected_items(self, offset):
        """Verschiebt die Auswahl innerhalb ihrer Ebene um eine Position."""
        if not self.require_list_view():
            return "break"
        item_ids = self.filter_top_level_selection(
            [item_id for item_id in self.iter_tree_ids() if item_id in set(self.get_selected_item_ids())]
        )
        if not item_ids:
            messagebox.showwarning("Hinweis", "Zuerst einen Punkt auswählen.")
            return "break"
        ordered = item_ids if offset < 0 else list(reversed(item_ids))
        self.snapshot_undo()
        changed = False
        for item_id in ordered:
            found = self.find_item(item_id)
            if not found:
                continue
            item, siblings, index, _parent = found
            target = index + offset
            if 0 <= target < len(siblings):
                siblings.pop(index)
                siblings.insert(target, item)
                changed = True
        if not changed:
            if self.undo_stack:
                self.undo_stack.pop()
            return "break"
        self.save_items()
        self.refresh_tree(selected_id=item_ids[0])
        self._restore_item_selection(item_ids)
        return "break"

    def move_selected_to_list_dialog(self):
        """Verschiebt die Auswahl in eine per Dialog gewählte Zielliste."""
        if not self.require_list_view():
            return "break"
        item_ids = self.get_selected_item_ids()
        if not item_ids:
            messagebox.showwarning("Hinweis", "Zuerst einen Punkt auswählen.")
            return "break"
        choices = []
        for entry in self.lists:
            if entry.get("id") == self.active_list_id:
                continue
            title = str(entry.get("title") or "Liste").strip() or "Liste"
            folder = self.get_folder(entry.get("folder_id"))
            if folder:
                title = f"{str(folder.get('title') or 'Ordner').strip()} › {title}"
            choices.append((entry.get("id"), title))
        if not choices:
            messagebox.showinfo("Verschieben", "Es gibt keine andere Liste als Ziel.")
            return "break"
        target_id = self.themed_choice_dialog(
            "In Liste verschieben", "In welche Liste sollen die Punkte verschoben werden?", choices
        )
        if target_id:
            self.move_items_to_list(item_ids, target_id)
        return "break"

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

    def _add_importance_cascade(self, menu, selected_items, enabled=True):
        importance_menu = self._new_themed_popup_menu(menu)
        importance_values = {self.clamp_importance(item.get("importance", 0)) for item in selected_items}
        current_importance = next(iter(importance_values)) if len(importance_values) == 1 else None
        for value, label in ((0, "Keine"), (1, "Niedrig"), (2, "Mittel"), (3, "Hoch")):
            prefix = "✓ " if current_importance == value else "    "
            importance_menu.add_command(
                label=f"{prefix}{label}",
                command=lambda selected=value: self.set_importance_selected(selected),
            )
        menu.add_cascade(
            label="Wichtigkeit", menu=importance_menu, state="normal" if enabled else "disabled"
        )
        return importance_menu

    def _add_due_cascade(self, menu, selected_items, enabled=True):
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
        menu.add_cascade(label="Fälligkeit", menu=due_menu, state="normal" if enabled else "disabled")
        return due_menu

    def _add_color_cascade(self, menu, selected_items):
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
        return color_menu

    def _add_label_cascade(self, menu, selected_items):
        """Labels zuweisen oder lösen – Häkchen zeigt die Zuweisung der Auswahl."""
        label_menu = self._new_themed_popup_menu(menu)
        if not self.labels:
            label_menu.add_command(label="Noch keine Labels angelegt", state="disabled")
        else:
            for label in self.labels:
                label_id = label.get("id")
                assigned_count = sum(1 for item in selected_items if label_id in (item.get("labels") or []))
                if assigned_count == len(selected_items) and selected_items:
                    prefix = "✓ "
                elif assigned_count:
                    prefix = "– "  # nur ein Teil der Auswahl trägt das Label
                else:
                    prefix = "    "
                label_menu.add_command(
                    label=f"{prefix}{label.get('name', '')}",
                    foreground=self.theme[self.label_color_key(label)],
                    command=lambda selected=label_id: self.toggle_label_on_selected_items(selected),
                )
            label_menu.add_separator()
            label_menu.add_command(label="Alle Labels entfernen", command=self.clear_labels_on_selected_items)
        label_menu.add_separator()
        label_menu.add_command(label="Labels verwalten …", command=self.open_label_manager)
        menu.add_cascade(label="Labels", menu=label_menu)
        return label_menu

    def build_item_context_menu(self):
        """Vollständiges Kontextmenü für die aktuelle Aufgaben-/Mehrfachauswahl."""
        item_ids = self.get_selected_item_ids()
        if not item_ids:
            return None
        selected_items = [self.find_item(item_id)[0] for item_id in item_ids if self.find_item(item_id)]
        if not selected_items:
            return None

        single = len(selected_items) == 1
        groups = [item for item in selected_items if self.is_group_item(item)]
        tasks = [item for item in selected_items if not self.is_group_item(item)]
        only_groups = bool(groups) and not tasks
        has_tasks = bool(tasks)

        menu = self._new_themed_popup_menu()
        if single:
            header = "Gruppenaktionen" if only_groups else "Punktaktionen"
        else:
            header = f"Aktionen für {len(selected_items)} Punkte"
        menu.add_command(label=header, state="disabled")
        menu.add_separator()

        menu.add_command(
            label=(
                "Bearbeiten (Titel, Beschreibung, Anhänge) …"
                if single
                else "Bearbeiten … (nur einzeln)"
            ),
            command=self.edit_item,
            state="normal" if single else "disabled",
        )
        menu.add_command(
            label="Erledigt umschalten",
            command=self.toggle_done,
            state="normal" if has_tasks else "disabled",
        )
        menu.add_separator()

        # --- Neu anlegen ---
        create_menu = self._new_themed_popup_menu(menu)
        create_menu.add_command(
            label="Punkt darunter …",
            command=lambda: self.add_sibling_item(self.ITEM_KIND_TASK),
        )
        create_menu.add_command(
            label="Gruppe darunter …",
            command=lambda: self.add_sibling_item(self.ITEM_KIND_GROUP),
        )
        create_menu.add_command(
            label="Unterpunkt …",
            command=self.add_child_item,
            state="normal" if single else "disabled",
        )
        menu.add_cascade(label="Neu anlegen", menu=create_menu)

        # --- Gruppe ---
        group_menu = self._new_themed_popup_menu(menu)
        group_menu.add_command(
            label="Auswahl gruppieren …",
            command=self.group_selected_items,
        )
        group_menu.add_command(
            label="In Gruppe umwandeln",
            command=lambda: self.convert_selected_kind(self.ITEM_KIND_GROUP),
            state="normal" if has_tasks else "disabled",
        )
        group_menu.add_command(
            label="In Aufgabe zurückwandeln",
            command=lambda: self.convert_selected_kind(self.ITEM_KIND_TASK),
            state="normal" if groups else "disabled",
        )
        group_menu.add_separator()
        group_menu.add_command(
            label="Gruppe auflösen (Inhalt bleibt)",
            command=self.dissolve_selected_group,
            state="normal" if single and only_groups else "disabled",
        )
        menu.add_cascade(label="Gruppe", menu=group_menu)
        menu.add_separator()

        # Gruppen tragen bewusst keinen Status, keine Fälligkeit und keine Wichtigkeit.
        self._add_importance_cascade(menu, tasks or selected_items, enabled=has_tasks)
        self._add_due_cascade(menu, tasks or selected_items, enabled=has_tasks)
        self._add_color_cascade(menu, selected_items)
        self._add_label_cascade(menu, selected_items)
        menu.add_separator()

        # --- Struktur ---
        structure_menu = self._new_themed_popup_menu(menu)
        structure_menu.add_command(label="Einrücken", command=self.indent_selected)
        structure_menu.add_command(label="Ausrücken", command=self.outdent_selected)
        structure_menu.add_separator()
        structure_menu.add_command(label="Nach oben", command=lambda: self.move_selected_items(-1))
        structure_menu.add_command(label="Nach unten", command=lambda: self.move_selected_items(1))
        structure_menu.add_separator()
        structure_menu.add_command(label="In Liste verschieben …", command=self.move_selected_to_list_dialog)
        menu.add_cascade(label="Struktur", menu=structure_menu)

        # --- Zwischenablage ---
        clipboard_menu = self._new_themed_popup_menu(menu)
        clipboard_menu.add_command(label="Kopieren", command=self.copy_selected_to_clipboard)
        clipboard_menu.add_command(label="Einfügen", command=self.paste_items_from_clipboard)
        clipboard_menu.add_command(label="Duplizieren", command=self.duplicate_selected_items)
        menu.add_cascade(label="Zwischenablage", menu=clipboard_menu)

        menu.add_separator()
        menu.add_command(label="Entfernen", command=self.delete_item, foreground=self.theme["delete"])
        return menu

    def build_tree_background_menu(self):
        """Kontextmenü für den leeren Bereich der Aufgabenliste."""
        menu = self._new_themed_popup_menu()
        menu.add_command(label="Liste", state="disabled")
        menu.add_separator()
        menu.add_command(label="Neuer Punkt …", command=lambda: self.add_sibling_item(self.ITEM_KIND_TASK, None))
        menu.add_command(label="Neue Gruppe …", command=lambda: self.add_sibling_item(self.ITEM_KIND_GROUP, None))
        menu.add_command(label="Einfügen", command=self.paste_items_from_clipboard)
        menu.add_separator()
        menu.add_command(label="Alle auswählen", command=self.select_all_items)
        menu.add_command(label="Aufklappen", command=self.expand_all)
        menu.add_command(label="Zuklappen", command=self.collapse_all)
        menu.add_separator()

        sort_menu = self._new_themed_popup_menu(menu)
        sort_menu.add_command(label="Nach Fälligkeit", command=lambda: self.sort_current_list("due"))
        sort_menu.add_command(label="Nach Wichtigkeit", command=lambda: self.sort_current_list("importance"))
        sort_menu.add_command(label="Alphabetisch", command=lambda: self.sort_current_list("alpha"))
        menu.add_cascade(label="Sortieren", menu=sort_menu)

        export_menu = self._new_themed_popup_menu(menu)
        export_menu.add_command(label="Als TXT …", command=self.export_as_txt)
        export_menu.add_command(label="Als Markdown …", command=self.export_as_markdown)
        export_menu.add_command(label="Als CSV …", command=self.export_as_csv)
        menu.add_cascade(label="Liste exportieren", menu=export_menu)

        menu.add_separator()
        menu.add_command(label="Beschreibungstext …", command=self.edit_page_note)
        menu.add_command(label="Liste leeren", command=self.clear_list, foreground=self.theme["delete"])
        return menu

    def build_in_progress_context_menu(self, row_id):
        """Kontextmenü einer Zeile der abgeleiteten Ansicht „In Bearbeitung“."""
        source = self.in_progress_item_sources.get(row_id)
        if not source:
            return None
        list_id, item_id = source
        found = self.find_item_in_lists(item_id)
        if not found:
            return None
        item = found[0]

        menu = self._new_themed_popup_menu()
        source_list = next((entry for entry in self.lists if entry.get("id") == list_id), None)
        source_title = str((source_list or {}).get("title") or "Quellliste").strip() or "Quellliste"
        menu.add_command(label=f"Aus: {self.ellipsize_sidebar_title(source_title)}", state="disabled")
        menu.add_separator()
        menu.add_command(label="In Quellliste öffnen", command=self.open_in_progress_source_item)
        menu.add_command(
            label="Bearbeiten (Titel, Beschreibung, Anhänge) …",
            command=lambda: self.edit_in_progress_item(item_id),
        )
        menu.add_command(
            label=("Als offen markieren" if item.get("done") else "Als erledigt markieren"),
            command=lambda: self.update_in_progress_item(item_id, "done", not item.get("done")),
        )
        menu.add_separator()

        importance_menu = self._new_themed_popup_menu(menu)
        current_importance = self.clamp_importance(item.get("importance", 0))
        for value, label in ((0, "Keine"), (1, "Niedrig"), (2, "Mittel"), (3, "Hoch")):
            prefix = "✓ " if current_importance == value else "    "
            importance_menu.add_command(
                label=f"{prefix}{label}",
                command=lambda selected=value: self.update_in_progress_item(item_id, "importance", selected),
            )
        menu.add_cascade(label="Wichtigkeit", menu=importance_menu)

        due_menu = self._new_themed_popup_menu(menu)
        today_iso = date.today().isoformat()
        tomorrow_iso = (date.today() + timedelta(days=1)).isoformat()
        current_due = item.get("due")
        due_menu.add_command(
            label=f"{'✓ ' if current_due == today_iso else '    '}Heute",
            command=lambda: self.update_in_progress_item(item_id, "due", today_iso),
        )
        due_menu.add_command(
            label=f"{'✓ ' if current_due == tomorrow_iso else '    '}Morgen",
            command=lambda: self.update_in_progress_item(item_id, "due", tomorrow_iso),
        )
        due_menu.add_command(
            label="Fälligkeit entfernen",
            command=lambda: self.update_in_progress_item(item_id, "due", None),
        )
        menu.add_cascade(label="Fälligkeit", menu=due_menu)

        color_menu = self._new_themed_popup_menu(menu)
        current_color = item.get("color")
        for label, color_key in self.ITEM_COLOR_CHOICES:
            prefix = "✓ " if current_color == color_key else "    "
            color_menu.add_command(
                label=f"{prefix}{label}",
                foreground=self.theme[color_key],
                command=lambda selected=color_key: self.update_in_progress_item(item_id, "color", selected),
            )
        color_menu.add_separator()
        color_menu.add_command(
            label=f"{'✓ ' if current_color is None else '    '}Keine Farbe",
            command=lambda: self.update_in_progress_item(item_id, "color", None),
        )
        menu.add_cascade(label="Aufgabenfarbe", menu=color_menu)

        label_menu = self._new_themed_popup_menu(menu)
        if not self.labels:
            label_menu.add_command(label="Noch keine Labels angelegt", state="disabled")
        else:
            assigned = item.get("labels") or []
            for label in self.labels:
                label_id = label.get("id")
                prefix = "✓ " if label_id in assigned else "    "
                label_menu.add_command(
                    label=f"{prefix}{label.get('name', '')}",
                    foreground=self.theme[self.label_color_key(label)],
                    command=lambda selected=label_id: self.toggle_in_progress_label(item_id, selected),
                )
        label_menu.add_separator()
        label_menu.add_command(label="Labels verwalten …", command=self.open_label_manager)
        menu.add_cascade(label="Labels", menu=label_menu)
        return menu

    def toggle_in_progress_label(self, item_id, label_id):
        """Labelzuweisung direkt aus der Ansicht „In Bearbeitung“ heraus."""
        found = self.find_item_in_lists(item_id)
        if not found or self.get_label(label_id) is None:
            return "break"
        item = found[0]
        assigned = list(item.get("labels") or [])
        if label_id in assigned:
            assigned = [value for value in assigned if value != label_id]
        elif len(assigned) < self.MAX_LABELS_PER_ITEM:
            assigned.append(label_id)
        else:
            return "break"
        self.snapshot_undo()
        item["labels"] = assigned
        self.save_items()
        self.refresh_tree()
        return "break"

    def _popup_item_menu(self, menu, event):
        self._item_context_menu = menu
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            try:
                menu.grab_release()
            except tk.TclError:
                pass
        return "break"

    def show_item_context_menu(self, event):
        if self.view_mode == "trash":
            row_id = self.tree.identify_row(event.y)
            if row_id and self.trash_id_from_iid(row_id) and row_id not in self.tree.selection():
                self.tree.selection_set(row_id)
                self.tree.focus(row_id)
            self._destroy_item_context_menu()
            return self._popup_item_menu(self.build_trash_context_menu(row_id), event)
        if self.view_mode == "in_progress":
            row_id = self.tree.identify_row(event.y)
            if row_id not in self.in_progress_item_sources:
                return "break"
            self.tree.selection_set(row_id)
            self.tree.focus(row_id)
            self._destroy_item_context_menu()
            menu = self.build_in_progress_context_menu(row_id)
            if menu is None:
                return "break"
            return self._popup_item_menu(menu, event)
        if self.view_mode == "folder":
            row_id = self.tree.identify_row(event.y)
            list_id = self.folder_list_id_from_iid(row_id)
            self._destroy_item_context_menu()
            if list_id:
                self.tree.selection_set(row_id)
                self.tree.focus(row_id)
                menu = self.build_sidebar_context_menu(("list", list_id))
            else:
                menu = self.build_folder_overview_menu()
            if menu is None:
                return "break"
            return self._popup_item_menu(menu, event)
        if self.view_mode != "list":
            return "break"
        item_id = self.tree.identify_row(event.y)
        if not item_id or item_id == self.EMPTY_ROW_ID or not self.find_item(item_id):
            # Rechtsklick in den leeren Bereich bietet die Listenaktionen an.
            self._destroy_item_context_menu()
            return self._popup_item_menu(self.build_tree_background_menu(), event)

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
        if self.is_group_item(first_found[0]) and len(item_ids) == 1:
            # Eine Gruppe kennt keinen Erledigt-Zustand. Der gleiche Handgriff
            # klappt sie deshalb auf und zu, wie man es von einem Ordner erwartet.
            group_id = item_ids[0]
            try:
                is_open = bool(self.tree.item(group_id, "open"))
            except tk.TclError:
                return "break"
            self.tree.item(group_id, open=not is_open)
            if is_open:
                self.expanded_ids.discard(group_id)
                self.collapsed_item_ids.add(group_id)
            else:
                self.expanded_ids.add(group_id)
                self.collapsed_item_ids.discard(group_id)
            return "break"
        task_ids = [item_id for item_id in item_ids
                    if (self.find_item(item_id) or (None,))[0] is not None
                    and not self.is_group_item(self.find_item(item_id)[0])]
        if not task_ids:
            return "break"
        item_ids = task_ids
        first_found = self.find_item(item_ids[0])
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
        if event is not None and self.current_focus_widget() in (
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
            # Fallback: der Punkt landet sicher auf oberster Ebene. Da sich die
            # Daten damit geändert haben, gilt der Vorgang als erfolgreich –
            # sonst bliebe die Änderung ungespeichert und nicht rückgängig machbar.
            self.items.append(moved_item)
            return True

        target_item = target_found_after_remove[0]
        target_item.setdefault("children", []).append(moved_item)
        self.expanded_ids.add(target_id)
        self.collapsed_item_ids.discard(target_id)
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
            # Siehe make_subitem: geänderte Daten müssen gespeichert werden.
            self.items.append(moved_item)
            return True

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
                self.save_items()
                self.refresh_tree(selected_id=source_id)
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
            # Ohne echte Änderung darf kein wirkungsloser Undo-Schritt zurückbleiben.
            if self.undo_stack:
                self.undo_stack.pop()
            return "break"

        parent_found_after_remove = self.find_item(parent_id)
        if not parent_found_after_remove:
            self.items.append(moved_item)
            self.save_items()
            self.refresh_tree(selected_id=source_id)
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
        # Die eigene Drag-Auswahl beantwortet den Klick mit "break" und
        # unterdrückt damit die native Class-Bindung – einschließlich der Zeile,
        # die den Baum fokussiert. Ohne den folgenden Aufruf bliebe der Baum
        # ohne Tastaturfokus, und die Pfeiltasten würden nichts bewirken.
        self.tree.focus_set()
        if self.view_mode == "folder":
            return self.on_folder_overview_drag_start(event)
        if self.view_mode != "list":
            self.drag_start_id = None
            self.drag_item_ids = []
            return
        row_id = self.tree.identify_row(event.y)
        try:
            clicked_element = self.tree.identify_element(event.x, event.y)
        except tk.TclError:
            clicked_element = ""
        if row_id and row_id != self.EMPTY_ROW_ID and "indicator" in str(clicked_element).lower():
            # Die eigene Drag-Auswahl unterdrückt absichtlich die native Class-
            # Bindung. Klapppfeile werden daher hier explizit und zustandsfest
            # behandelt, statt den Klick als Drag-Start zu interpretieren.
            has_children = bool(self.tree.get_children(row_id))
            if has_children:
                is_open = bool(self.tree.item(row_id, "open"))
                self.tree.item(row_id, open=not is_open)
                if is_open:
                    self.expanded_ids.discard(row_id)
                    self.collapsed_item_ids.add(row_id)
                else:
                    self.expanded_ids.add(row_id)
                    self.collapsed_item_ids.discard(row_id)
            self.drag_start_id = None
            self.drag_item_ids = []
            return "break"
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

    def on_folder_overview_drag_start(self, event):
        """Startet das Sortieren/Verschieben einer Liste aus der Ordnerübersicht."""
        row_id = self.tree.identify_row(event.y)
        list_id = self.folder_list_id_from_iid(row_id)
        self.drag_start_id = None
        self.drag_item_ids = []
        self.drag_has_moved = False
        if not list_id or self.current_search_query():
            return "break"
        self.drag_start_id = list_id
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.tree.selection_set(row_id)
        self.tree.focus(row_id)
        return "break"

    def on_folder_overview_drag_motion(self, event):
        if not self.drag_start_id:
            return "break"
        if abs(event.x - self.drag_start_x) + abs(event.y - self.drag_start_y) > 6:
            self.drag_has_moved = True

        self.clear_drop_target_tags()
        self.clear_sidebar_drop_target_tags()
        sidebar_iid, sidebar_row = self.identify_sidebar_drop_row(event)
        if sidebar_iid and sidebar_row and sidebar_row[0] == "folder":
            target_tree = self.get_sidebar_tree_for_iid(sidebar_iid)
            if target_tree is not None:
                try:
                    tags = set(target_tree.item(sidebar_iid, "tags"))
                    tags.add("drop_target")
                    target_tree.item(sidebar_iid, tags=tuple(tags), open=True)
                except tk.TclError:
                    pass
            return "break"

        target_iid = self.identify_tree_drop_row(event)
        target_list_id = self.folder_list_id_from_iid(target_iid)
        if target_list_id and target_list_id != self.drag_start_id:
            try:
                tags = set(self.tree.item(target_iid, "tags"))
                tags.add("drop_target")
                self.tree.item(target_iid, tags=tuple(tags))
            except tk.TclError:
                pass
        return "break"

    def on_folder_overview_drag_end(self, event):
        source_id = self.drag_start_id
        sidebar_iid, sidebar_row = self.identify_sidebar_drop_row(event)
        target_iid = self.identify_tree_drop_row(event)
        target_list_id = self.folder_list_id_from_iid(target_iid)
        was_drag = bool(source_id and self.drag_has_moved)

        self.clear_drop_target_tags()
        self.clear_sidebar_drop_target_tags()
        self.drag_start_id = None
        self.drag_item_ids = []
        self.drag_has_moved = False
        if not was_drag:
            return "break"

        mutation = None
        if sidebar_iid and sidebar_row and sidebar_row[0] == "folder":
            mutation = ("folder", sidebar_row[1], None)
        elif target_list_id and target_list_id != source_id:
            try:
                _x, row_y, _width, row_height = self.tree.bbox(target_iid)
                place = "before" if event.y < row_y + row_height / 2 else "after"
            except (TypeError, ValueError, tk.TclError):
                place = "after"
            mutation = ("relative", target_list_id, place)
        if mutation is None:
            return "break"

        self.snapshot_undo()
        if mutation[0] == "folder":
            changed = self.move_sidebar_list_into_folder(source_id, mutation[1])
        else:
            changed = self.move_sidebar_list_relative(source_id, mutation[1], place=mutation[2])
        if not changed:
            if self.undo_stack:
                self.undo_stack.pop()
            return "break"
        self.save_items()
        self.refresh_tree(selected_id=f"folder-list:{source_id}")
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
            for tree_name in ("system_listbox", "sidebar_listbox"):
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
        if self.view_mode == "folder":
            return self.on_folder_overview_drag_motion(event)
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
        if self.view_mode == "folder":
            return self.on_folder_overview_drag_end(event)
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
        # Vor dem Auswerten sichern: beim Lesen der Labelzeilen können neue
        # Labels entstehen. Scheitert der Import, wird der Labelbestand exakt
        # zurückgesetzt und der wirkungslose Rückgängig-Schritt verworfen.
        self.snapshot_undo()
        labels_before_import = copy.deepcopy(self.labels)
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
                self.labels = labels_before_import
                if self.undo_stack:
                    self.undo_stack.pop()
                messagebox.showerror("Fehler beim Listenimport", f"{os.path.basename(path)} konnte nicht importiert werden:\n{e}")
                return "break"
        if not created:
            self.labels = labels_before_import
            if self.undo_stack:
                self.undo_stack.pop()
            messagebox.showwarning("Import", "In den ausgewählten Dateien wurden keine Aufgaben oder Beschreibungstexte gefunden.")
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

    @classmethod
    def extract_txt_note(cls, lines):
        note_lines = []
        inside_note_block = False
        for raw_line in lines:
            stripped = raw_line.strip()
            if stripped == cls.TXT_NOTE_BLOCK_START:
                inside_note_block = True
                continue
            if stripped == cls.TXT_NOTE_BLOCK_END:
                break
            if inside_note_block:
                note_lines.append(raw_line.rstrip("\r\n"))
        return "\n".join(note_lines).strip()

    def export_as_txt(self):
        if not self.require_list_view():
            return
        note = str(self.current_list().get("note") or "").strip()
        if not self.items and not note:
            messagebox.showwarning("Hinweis", "Keine Aufgaben und kein Beschreibungstext zum Exportieren.")
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
                    file.write(self.TXT_NOTE_BLOCK_START + "\n")
                    file.write(note + "\n")
                    file.write(self.TXT_NOTE_BLOCK_END + "\n\n")
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
            if self.is_group_item(item):
                # Der Gruppenmarker steht an derselben Stelle wie die
                # Wichtigkeitsmarker und wird beim Import wieder erkannt.
                file.write(f"{indent}{number_text}. {self.GROUP_MARKER}{item.get('text', '')}\n")
                description = str(item.get("description") or "").strip()
                for line in description.splitlines():
                    file.write(f"{indent}   Beschreibung: {line}\n")
                label_names = self.format_item_label_names(item)
                if label_names:
                    file.write(f"{indent}   Labels: {label_names}\n")
                for attachment in item.get("attachments", []):
                    file.write(f"{indent}   Anhang: {attachment.get('name', 'Datei')}\n")
                self.write_items_to_txt(file, item.get("children", []), current_number)
                continue
            flag_prefix = self.IMPORTANCE_MARKERS.get(self.clamp_importance(item.get("importance", 0)), "")
            done_prefix = "✓ " if item.get("done") else ""
            file.write(f"{indent}{number_text}. {flag_prefix}{done_prefix}{item.get('text', '')}\n")
            description = str(item.get("description") or "").strip()
            for line in description.splitlines():
                file.write(f"{indent}   Beschreibung: {line}\n")
            due_text = self.format_due_display(item.get("due"))
            if due_text:
                file.write(f"{indent}   Fällig: {due_text}\n")
            label_names = self.format_item_label_names(item)
            if label_names:
                file.write(f"{indent}   Labels: {label_names}\n")
            for attachment in item.get("attachments", []):
                file.write(f"{indent}   Anhang: {attachment.get('name', 'Datei')}\n")
            self.write_items_to_txt(file, item.get("children", []), current_number)

    def export_as_markdown(self):
        if not self.require_list_view():
            return
        note = str(self.current_list().get("note") or "").strip()
        if not self.items and not note:
            messagebox.showwarning("Hinweis", "Keine Aufgaben und kein Beschreibungstext zum Exportieren.")
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
            if self.is_group_item(item):
                # Gruppen sind Behälter, keine abhakbaren Aufgaben.
                file.write(f"{indent}- **{item.get('text', '')}**\n")
                description = str(item.get("description") or "").strip()
                for line in description.splitlines():
                    file.write(f"{indent}  > {line}\n")
                for attachment in item.get("attachments", []):
                    file.write(f"{indent}  - Anhang: `{attachment.get('name', 'Datei')}`\n")
                self.write_items_to_markdown(file, item.get("children", []), level + 1)
                continue
            checkbox = "[x]" if item.get("done") else "[ ]"
            flag = self.IMPORTANCE_MARKERS.get(self.clamp_importance(item.get("importance", 0)), "")
            due_text = self.format_due_display(item.get("due"))
            due_suffix = f" (f\u00e4llig {due_text})" if due_text else ""
            label_names = self.format_item_label_names(item)
            label_suffix = f" `{label_names}`" if label_names else ""
            file.write(f"{indent}- {checkbox} {flag}{item.get('text', '')}{due_suffix}{label_suffix}\n")
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
                # Neue Spalten werden ausschließlich angehängt; die Position
                # aller bisherigen Spalten bleibt dadurch stabil.
                writer.writerow([
                    "Nummer", "Ebene", "Aufgabe", "Beschreibung", "Anhänge",
                    "Erledigt", "Wichtigkeit", "Fällig", "Art", "Labels",
                ])
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
                "-" if self.is_group_item(item) else ("ja" if item.get("done") else "nein"),
                "-" if self.is_group_item(item)
                else self.IMPORTANCE_NAMES.get(self.clamp_importance(item.get("importance", 0)), "keine"),
                self.format_due_display(item.get("due")),
                "Gruppe" if self.is_group_item(item) else "Aufgabe",
                self.safe_csv_cell(self.format_item_label_names(item)),
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

    def collect_attachment_sources(self, lists, trash=None):
        """Alle Anhangsdateien, die ein Komplettbackup enthalten muss.

        Gelöschte, aber noch wiederherstellbare Listen zählen mit: ohne ihre
        Dateien wäre eine Wiederherstellung aus dem Backup unvollständig.
        """
        sources = {}
        total_size = 0
        collections = list(lists)
        for trash_entry in (trash or []):
            trashed_list = trash_entry.get("list") if isinstance(trash_entry, dict) else None
            if isinstance(trashed_list, dict):
                collections.append(trashed_list)
        for list_entry in collections:
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
        attachment_paths = self.collect_attachment_sources(
            payload.get("lists", []), payload.get("trash", [])
        )
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

    @classmethod
    def safe_attachment_filename(cls, original_name, attachment_id=None):
        """Baut einen Speichernamen, der validate_attachment_storage immer besteht.

        Kritisch sind Namen, die nach der Bereinigung auf Punkt oder Leerzeichen
        enden – etwa "report." oder eine Endung außerhalb von A-Z/0-9 wie
        ".☃". Solche Namen wären zwar schreibbar, aber nie wieder auflösbar:
        die Datei verschwände beim nächsten Start und jedes Komplettbackup
        würde daran scheitern.

        `attachment_id` hält Datensatz-ID und Dateiname nachvollziehbar gekoppelt.
        """
        prefix = attachment_id if isinstance(attachment_id, str) and attachment_id else uuid.uuid4().hex
        prefix = re.sub(r"[^A-Za-z0-9]", "", prefix)[:32] or uuid.uuid4().hex
        stem, extension = os.path.splitext(os.path.basename(str(original_name or "datei")))
        safe_stem = re.sub(r"[^\w .()-]+", "_", stem, flags=re.UNICODE).strip(" .")[:90] or "datei"
        safe_extension = re.sub(r"[^A-Za-z0-9.]", "", extension)[:16].strip(". ")
        suffix = f".{safe_extension}" if safe_extension else ""
        candidate = f"{prefix}_{safe_stem}{suffix}".rstrip(" .")
        try:
            cls.validate_attachment_storage(f"attachments/{candidate}")
        except ValueError:
            # Letzte Rückfallebene: garantiert gültig; der Anzeigename bleibt im
            # Datensatz vollständig erhalten.
            candidate = f"{prefix}.dat"
        return candidate

    def remap_import_attachments(self, lists, trash=None):
        """Gibt eingehenden Dateien neue Namen, damit Restore nie Bytes überschreibt."""
        storage_map = {}
        used_destinations = set()
        collections = list(lists)
        for trash_entry in (trash or []):
            trashed_list = trash_entry.get("list") if isinstance(trash_entry, dict) else None
            if isinstance(trashed_list, dict):
                collections.append(trashed_list)
        for list_entry in collections:
            for item in self.walk_items(list_entry.get("items", [])):
                for attachment in item.get("attachments", []):
                    old_storage = self.validate_attachment_storage(attachment.get("storage"))
                    if old_storage not in storage_map:
                        new_storage = None
                        # Begrenzte Versuche: ohne Obergrenze könnte ein Backup mit
                        # einem nicht normierbaren Anzeigenamen die App einfrieren.
                        for attempt in range(64):
                            candidate_name = (
                                self.safe_attachment_filename(attachment.get("name"))
                                if attempt < 32
                                else f"{uuid.uuid4().hex}.dat"
                            )
                            candidate = f"attachments/{candidate_name}"
                            final_path = self.resolve_attachment_path({"storage": candidate})
                            if candidate not in used_destinations and final_path and not os.path.exists(final_path):
                                new_storage = candidate
                                break
                        if new_storage is None:
                            raise OSError(
                                "Für einen Anhang aus dem Backup konnte kein freier Zielname "
                                "erzeugt werden."
                            )
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

            # normalize_lists_data setzt folders, labels und trash; der aktuelle
            # Zustand wird bis zum erfolgreichen Commit unverändert bewahrt.
            previous_folders = self.folders
            previous_labels = self.labels
            previous_trash = self.trash
            try:
                new_lists, active_from_file = self.normalize_lists_data(data)
                new_folders = self.folders
                new_labels = self.labels
                new_trash = self.trash
            finally:
                self.folders = previous_folders
                self.labels = previous_labels
                self.trash = previous_trash
            if not new_lists:
                raise ValueError("In der Datei wurden keine Listen gefunden.")
            new_lists = self.ensure_inbox_in_collection(new_lists)

            storage_map = {}
            staged_files = {}
            if is_portable:
                storage_map = self.remap_import_attachments(new_lists, new_trash)
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
                "labels": new_labels,
                "lists": new_lists,
                "trash": new_trash,
            }
            self.write_json_atomic(SAVE_FILE, imported_payload)
            committed = True

            self.lists = new_lists
            self.folders = new_folders
            self.labels = new_labels
            self.trash = new_trash
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

            # Der Schnappschuss entsteht vor dem Auswerten, weil beim Lesen der
            # Labelzeilen bereits neue Labels angelegt werden können. Rückgängig
            # nimmt dadurch auch diese Labels wieder zurück.
            self.snapshot_undo()
            labels_before_import = copy.deepcopy(self.labels)
            imported = self.parse_txt_items(lines)
            note = self.extract_txt_note(lines)
            if imported or note:
                self.items.extend(imported)
                if note:
                    current_note = str(self.current_list().get("note") or "").strip()
                    self.current_list()["note"] = (
                        f"{current_note}\n\n{note}" if current_note and note != current_note else note or current_note
                    )
                self.save_items()
                self.update_page_note_preview()
                self.update_page_labels()
                self.refresh_tree(selected_id=imported[-1]["id"] if imported else None)
                messagebox.showinfo(
                    "Import erfolgreich",
                    f"{self.count_items(imported)} Punkte und "
                    f"{'ein Beschreibungstext' if note else 'kein Beschreibungstext'} importiert.",
                )
            else:
                self.labels = labels_before_import
                if self.undo_stack:
                    self.undo_stack.pop()
                messagebox.showwarning(
                    "Import",
                    "Die Datei enthält weder erkennbare Aufgaben noch einen Beschreibungstext.",
                )
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
            if stripped == self.TXT_NOTE_BLOCK_START:
                inside_note_block = True
                continue
            if stripped == self.TXT_NOTE_BLOCK_END:
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
            if stripped.startswith("Labels:"):
                # Labels werden über den Namen aufgelöst; unbekannte Namen legen
                # ein neues Label an, solange die Obergrenze das zulässt.
                if last_item is not None:
                    for name in stripped.split(":", 1)[1].split(","):
                        label = self.ensure_label_by_name(name)
                        if label is None:
                            continue
                        assigned = last_item.setdefault("labels", [])
                        if label["id"] not in assigned and len(assigned) < self.MAX_LABELS_PER_ITEM:
                            assigned.append(label["id"])
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
            kind = self.ITEM_KIND_TASK
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

            if text.startswith(self.GROUP_MARKER.strip()):
                kind = self.ITEM_KIND_GROUP
                text = text[len(self.GROUP_MARKER.strip()):].strip()

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

            new = self.new_item(text, done, importance=importance, kind=kind)
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

    def ensure_label_by_name(self, name):
        """Vorhandenes Label mit diesem Namen oder ein neu angelegtes Label."""
        clean = str(name or "").strip()[: self.MAX_LABEL_NAME_LENGTH]
        if not clean:
            return None
        existing = self.get_label_by_name(clean)
        if existing is not None:
            return existing
        if len(self.labels) >= self.MAX_LABELS:
            return None
        # Die Farbe rotiert über die Palette, damit importierte Labels
        # unterscheidbar bleiben, ohne den Nutzer zu fragen.
        color = self.LABEL_COLOR_KEYS[len(self.labels) % len(self.LABEL_COLOR_KEYS)]
        label = self.new_label_object(clean, None, color)
        self.labels.append(label)
        return label

    def count_items(self, items, include_groups=False):
        """Zählt Punkte. Gruppen sind Behälter und zählen standardmäßig nicht mit."""
        total = 0
        for item in items:
            if include_groups or not self.is_group_item(item):
                total += 1
            total += self.count_items(item.get("children", []), include_groups)
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

    @staticmethod
    def accel(*keys):
        """Plattformgerechte Beschriftung eines Tastenkürzels.

        Unter macOS heißt der Modifikator Cmd; „Strg+E“ wäre dort schlicht falsch.
        """
        modifier = "Cmd" if IS_MACOS else "Strg"
        return "+".join([modifier] + [str(key) for key in keys])

    def create_menubar(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Neue Liste", accelerator=self.accel("Shift", "N"), command=self.create_new_list)
        file_menu.add_command(label="Neuer Ordner", command=self.create_new_folder)
        file_menu.add_separator()
        file_menu.add_command(label="TXT importieren …", accelerator=self.accel("I"), command=self.import_from_txt)
        file_menu.add_command(label="TXT als neue Liste(n) …", command=self.import_txt_as_new_lists)
        export_menu = tk.Menu(file_menu, tearoff=0)
        export_menu.add_command(label="Als TXT …", accelerator=self.accel("E"), command=self.export_as_txt)
        export_menu.add_command(label="Als Markdown …", command=self.export_as_markdown)
        export_menu.add_command(label="Als CSV …", command=self.export_as_csv)
        file_menu.add_cascade(label="Aktive Liste exportieren", menu=export_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Komplettbackup speichern …", command=self.export_full_backup)
        file_menu.add_command(label="Komplettbackup laden …", command=self.import_full_backup)
        file_menu.add_command(label="Backup-Ordner öffnen", command=self.open_backup_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Beenden", accelerator=self.accel("Q"), command=self.on_close)
        menubar.add_cascade(label="Datei", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Rückgängig", accelerator=self.accel("Z"), command=self.undo_last_change)
        edit_menu.add_separator()
        edit_menu.add_command(label="Kopieren", accelerator=self.accel("C"), command=self.copy_selected_to_clipboard)
        edit_menu.add_command(label="Einfügen", accelerator=self.accel("V"), command=self.paste_items_from_clipboard)
        edit_menu.add_command(label="Alle auswählen", accelerator=self.accel("A"), command=self.select_all_items)
        edit_menu.add_separator()
        edit_menu.add_command(label="Punktdetails …", accelerator="F2", command=self.edit_item)
        edit_menu.add_command(
            label="Auswahl gruppieren …", accelerator=self.accel("G"), command=self.group_selected_items
        )
        edit_menu.add_command(
            label="In Gruppe umwandeln", command=lambda: self.convert_selected_kind(self.ITEM_KIND_GROUP)
        )
        edit_menu.add_command(
            label="In Aufgabe zurückwandeln", command=lambda: self.convert_selected_kind(self.ITEM_KIND_TASK)
        )
        edit_menu.add_command(label="Gruppe auflösen", command=self.dissolve_selected_group)
        edit_menu.add_separator()
        edit_menu.add_command(label="Duplizieren", command=self.duplicate_selected_items)
        edit_menu.add_command(label="In Liste verschieben …", command=self.move_selected_to_list_dialog)
        edit_menu.add_command(
            label="Titel und Beschreibungstext …", accelerator=self.accel("M"), command=self.edit_page_note
        )
        edit_menu.add_command(label="Labels verwalten …", accelerator=self.accel("L"), command=self.open_label_manager)
        edit_menu.add_command(label="Wichtigkeit ändern", command=self.cycle_importance_selected)
        edit_menu.add_command(label="Fälligkeitsdatum …", accelerator=self.accel("T"), command=self.set_due_date_selected)
        edit_menu.add_command(label="Löschen", accelerator="Rückschritt" if IS_MACOS else "Entf", command=self.delete_item)
        menubar.add_cascade(label="Bearbeiten", menu=edit_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Design wechseln (Hell/Dunkel)", accelerator=self.accel("D"), command=self.toggle_theme)
        view_menu.add_separator()
        view_menu.add_command(label="Kalender …", accelerator=self.accel("K"), command=self.open_calendar_view)
        view_menu.add_command(label="In Bearbeitung", command=self.set_in_progress_view)
        view_menu.add_command(label="Papierkorb", command=self.set_trash_view)
        view_menu.add_command(label="Papierkorb leeren", command=self.empty_trash)
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
        if IS_WINDOWS:
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
        previous_focus = self.current_focus_widget()
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
        delete_key = "Rückschritt" if IS_MACOS else "Entf"
        shortcuts = (
            "Enter – Punkt hinzufügen\n"
            "Doppelklick / Leertaste – erledigt umschalten\n"
            f"{delete_key} – ausgewählte Punkte löschen\n"
            "Rechtsklick – Details, Wichtigkeit, Fälligkeit, Farbe und Entfernen\n"
            f"{self.accel('Shift', 'F')} – Wichtigkeit durchschalten\n"
            f"{self.accel('T')} – Fälligkeitsdatum setzen oder entfernen\n"
            "F2 – Punktdetails, Beschreibung und Anhänge · F3 – Titel bearbeiten\n"
            f"{self.accel('M')} – Titel und Beschreibungstext öffnen\n"
            f"{self.accel('L')} – Labels verwalten · {self.accel('K')} – Kalender öffnen\n"
            f"{self.accel('G')} – ausgewählte Punkte gruppieren\n"
            "Rechtsklick auf einen Punkt – Labels, Gruppen, Struktur, Zwischenablage und mehr\n"
            "Rechtsklick in den leeren Listenbereich – neuer Punkt, Gruppe, Sortieren, Export\n"
            "Rechtsklick auf Liste oder Ordner – bearbeiten, färben, verschieben, Papierkorb\n"
            "Alt+↑/↓ – Punkte verschieben · Alt+←/→ – aus-/einrücken\n"
            "Seitenleiste: Shift/Strg + Klick – mehrere Listen wählen · Entf – in den Papierkorb\n"
            "Seitenleiste: Alt+↑/↓ – Listen und Ordner verschieben · Alt+←/→ – aus/in Ordner\n"
            "Ordner anklicken – enthaltene Listen im Hauptbereich anzeigen\n"
            "Auf Seitenleisten-Liste ziehen – Punkt dorthin verschieben\n"
            "Auf Ordner ziehen – enthaltene Zielliste auswählen\n"
            "Tab – ein-/ausrücken · Drag & Drop – Reihenfolge ändern\n"
            "Shift+Drag – Unterpunkt · Shift+Klick – Bereich auswählen\n"
            f"{self.accel('A')} – alle auswählen · {self.accel('Z')} – rückgängig\n"
            f"{self.accel('C')} / {self.accel('V')} – kopieren / einfügen\n"
            f"{self.accel('F')} – Suche · {self.accel('E')} – Export TXT · {self.accel('I')} – Import TXT\n"
            f"{self.accel('D')} – Design wechseln · {self.accel('S')} – speichern\n"
            f"{self.accel('Shift', 'N')} – neue Liste"
            + ("" if IS_MACOS else " · Strg+W – Liste löschen")
        )
        messagebox.showinfo("Tastenkürzel", shortcuts)


if __name__ == "__main__":
    root = tk.Tk()
    app = ListApp(root)
    root.mainloop()
