# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 5: Aktionen, Menüs und Desktop-Adapter (D86, D88).

Plattformadapter und Menüaufbau ohne Bindung an die Glide-Anwendungsdomäne.
Erfüllt die Shell-Importregel (D86): importiert ausschließlich Standardbibliothek
und tkinter. Modulbudget (WA-50 / T322): alle Funktionen <= 50 Zeilen,
maximale Verschachtelungstiefe <= 15.
"""

import os
import subprocess
import sys
import tkinter as tk


def is_macos():
    """Prüft, ob das Betriebssystem macOS ist."""
    return sys.platform == "darwin"


def is_windows():
    """Prüft, ob das Betriebssystem Windows ist."""
    return os.name == "nt"


def is_linux():
    """Prüft, ob das Betriebssystem Linux/Unix ist."""
    return sys.platform.startswith("linux")


def platform_name():
    """Gibt den normalisierten Namen der aktuellen Plattform zurück."""
    if is_macos():
        return "macos"
    if is_windows():
        return "windows"
    return "linux"


def primary_modifier(macos_override=None, modifier_labels=None):
    """Liefert den vom Host benannten primären Modifikator."""
    mac = is_macos() if macos_override is None else macos_override
    labels = modifier_labels or {}
    name = "command" if mac else "control"
    fallback = "Cmd" if mac else "Strg"
    return labels.get(name, fallback)


def format_accelerator(*keys, macos_override=None, modifier_labels=None):
    """Plattformgerechte Textdarstellung eines Tastenkürzels."""
    mod = primary_modifier(macos_override, modifier_labels)
    return "+".join([mod] + [str(k) for k in keys])


def format_redo_accelerator(windows_override=None, macos_override=None,
                            modifier_labels=None):
    """Beschriftung für „Wiederholen“ nach Systemkonvention (Strg+Y unter Windows)."""
    win = is_windows() if windows_override is None else windows_override
    if win:
        return format_accelerator("Y", macos_override=False, modifier_labels=modifier_labels)
    labels = modifier_labels or {}
    shift = labels.get("shift", "Shift")
    return format_accelerator(shift, "Z", macos_override=macos_override,
                              modifier_labels=modifier_labels)


def _append_command_entry(menu, entry, action_resolver=None):
    """Fügt einen einzelnen Aktionsbefehl zum Menü hinzu."""
    label = entry[0]
    target = entry[1]
    accel = entry[2] if len(entry) > 2 and entry[2] else ""
    menu.add_command(label=label, command=target, accelerator=accel)
    action_id = entry[3] if len(entry) > 3 else (
        action_resolver(target) if action_resolver else None
    )
    menu._glide_action_ids[menu.index("end")] = action_id


def _append_submenu_entry(menu, entry, menus_out, attr_target, action_resolver):
    """Fügt ein Untermenü (Kaskade oder dynamisches Attribut) hinzu."""
    label, target = entry[0], entry[1]
    if isinstance(target, str):
        submenu = tk.Menu(menu, tearoff=0)
        submenu._glide_action_ids = {}
        if menus_out is not None:
            menus_out.append(submenu)
        if attr_target is not None:
            setattr(attr_target, target, submenu)
        menu.add_cascade(label=label, menu=submenu)
    elif isinstance(target, (list, tuple)):
        child = build_menu_tree(
            menu, target, menus_out=menus_out, tearoff=0,
            attr_target=attr_target, action_resolver=action_resolver
        )
        menu.add_cascade(label=label, menu=child)


def _populate_menu_entries(menu, entries, menus_out, attr_target, action_resolver):
    """Füllt ein Menü mit Einträgen, Trennlinien und Untermenüs."""
    for entry in entries:
        if entry is None:
            menu.add_separator()
            continue
        target = entry[1]
        if isinstance(target, (str, list, tuple)):
            _append_submenu_entry(menu, entry, menus_out, attr_target, action_resolver)
        else:
            _append_command_entry(menu, entry, action_resolver=action_resolver)


def build_menu_tree(parent, entries, menus_out=None, tearoff=0,
                    attr_target=None, action_resolver=None):
    """Baut rekursiv ein Menü aus deklarativen Beschreibungen auf.

    Registriert das Menü im Sammler, weist Aktions-IDs zu und
    verknüpft dynamische Attribute am Zielobjekt.
    """
    menu = tk.Menu(parent, tearoff=tearoff)
    menu._glide_action_ids = {}
    if menus_out is not None:
        menus_out.append(menu)
    _populate_menu_entries(menu, entries, menus_out, attr_target, action_resolver)
    return menu


class DesktopMenuBar:
    """Plattformspezifische Menüleisten-Erzeugung und Popup-Behandlung."""

    @staticmethod
    def create_menubar_frame(parent, bg_color):
        """Erzeugt einen Container-Rahmen für anwendungseigene Menüleisten."""
        return tk.Frame(parent, bg=bg_color)

    @staticmethod
    def post_popup_menu(button, menu, previous_focus=None, restore_cb=None):
        """Öffnet ein Menü als Popup unter einem Knopf mit sicherem Grab-Abbau."""
        try:
            button.focus_set()
            x_pos = button.winfo_rootx()
            y_pos = button.winfo_rooty() + button.winfo_height()
            menu.tk_popup(x_pos, y_pos)
        finally:
            try:
                menu.grab_release()
            except tk.TclError:
                pass
            if restore_cb is not None and previous_focus is not None:
                restore_cb(previous_focus)
        return "break"


def launch_path(path, windows_override=None, macos_override=None):
    """Öffnet einen externen Pfad oder URL mit dem System-Standardprogramm."""
    win = is_windows() if windows_override is None else windows_override
    mac = is_macos() if macos_override is None else macos_override
    if win:
        os.startfile(path)  # type: ignore[attr-defined]
    elif mac:
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])
    return True


def copy_to_clipboard(widget, text):
    """Schreibt Text in die Zwischenablage."""
    widget.clipboard_clear()
    widget.clipboard_append(text)


def read_from_clipboard(widget):
    """Liest Text aus der Zwischenablage, fängt TclError sicher ab."""
    try:
        return widget.clipboard_get()
    except (tk.TclError, Exception):
        return ""
