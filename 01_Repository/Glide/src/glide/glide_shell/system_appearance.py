# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 9: Hell/Dunkel des Systems erkennen ohne Tk-Import.

Die Erkennung deutet, was der Host abfragt: unter Windows den Registrywert
`AppsUseLightTheme` (über einen Rückruf), unter Linux die Ausgabe von
`gsettings` (color-scheme, GTK-Thema), unter macOS und Tk 9 die Antwort von
`tk::unsupported::MacWindowStyle isdark` bzw. `winfo isdark`. Jede Erkennung
darf scheitern und liefert dann None; `resolve` behält in diesem Fall das
aktuelle Design. Designnamen und -paare kennt nur der Host.
"""


def resolve(auto, system_dark, current):
    """Wirksames Design: aus dem Paar nach Systemmodus, sonst das aktuelle."""
    if not auto or system_dark is None:
        return current
    return auto["dark"] if system_dark else auto["light"]


def windows_is_dark(read_value):
    """`read_value()` liefert AppsUseLightTheme (0 = dunkel) oder wirft OSError."""
    try:
        wert = read_value()
    except (OSError, ValueError, TypeError):
        return None
    if isinstance(wert, bool) or not isinstance(wert, int):
        return None
    return wert == 0


def linux_is_dark(color_scheme=None, gtk_theme=None):
    """Ausgabe von `gsettings get …` deuten: color-scheme zuerst, dann der GTK-Name."""
    schema = str(color_scheme or "").strip().strip("'\"").lower()
    if schema == "prefer-dark":
        return True
    if schema in ("prefer-light", "default") and not gtk_theme:
        return False
    thema = str(gtk_theme or "").strip().strip("'\"").lower()
    if thema:
        return thema.endswith("-dark") or ":dark" in thema
    return False if schema else None


def tk_is_dark(answer):
    """Antwort von `tk::unsupported::MacWindowStyle isdark` oder `winfo isdark` deuten."""
    text = str(answer).strip().lower()
    if text in ("1", "true", "yes"):
        return True
    if text in ("0", "false", "no"):
        return False
    return None
