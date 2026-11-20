# SPDX-License-Identifier: MPL-2.0
"""Modale Dialoge für Tk ohne Glide-Bezug (Shell-Paket 3a, 14.11.2026).

Der eine Warteweg für modale Dialoge, herausgelöst aus `ListApp.run_modal`
und `ListApp.modal_over`. Das Modul kennt nur Tk: Theme-Farbe,
Bildschirmanteil und Fehlerprotokoll kommen als Argumente vom Host. Es
importiert ausschließlich die Standardbibliothek und `tkinter` und ist damit
der erste Baustein der Shell (Abhängigkeitsrichtung Host → Shell → Tk).

Vertrag (festgehalten in `tests/integration/test_modalvertrag.py`):
- Während des Wartens hält der Dialog den lokalen Griff und trägt
  `_glide_modal_active = True`; danach ist der Griff frei und die Marke
  `False`, auch wenn das Warten mit einer Ausnahme endet.
- Scheitert `grab_set`, wird das gemeldet und trotzdem gewartet: ein Dialog
  ohne Griff ist unschön, ein Dialog ohne Rückweg ein Stillstand.
- Ein Dialog mit `_glide_modal_finished` (Tk-Variable) endet, sobald sie
  gesetzt wird, und bleibt bestehen; sonst endet das Warten mit dem Fenster.
- Hielt ein anderes Fenster vorher den Griff, bekommt es ihn danach zurück –
  außer es ist inzwischen verschwunden. Das Hauptfenster bekommt keinen.
- Fokusrückgabe (D87, 3.65.0): Vor dem Warten merkt sich das Modul, welches
  Widget im aufrufenden Fenster zuletzt den Fokus hatte, und gibt ihn nach dem
  Schließen dorthin zurück. Ist das Widget verschwunden, erhält das Fenster
  selbst den Fokus. Liegt der Fokus danach in einem dritten, noch offenen
  Fenster, bleibt er dort. Aufrufer, die danach selbst einen Fokus setzen,
  behalten das letzte Wort.

Die Attributnamen `_glide_modal_active` und `_glide_modal_finished` bleiben
aus Kompatibilität: Einstellungsdialog und Fensterwechsel der App lesen sie.

Dialogfabrik (R1, D94, 20.11.2026): `create_dialog` ist der gemeinsame
Erzeugungsweg für Dialogfenster. Sie legt das Fenster an, verbirgt es auf
Wunsch bis zur Platzierung, setzt Titel und Hintergrund, ordnet es dem
Besitzer zu und übernimmt Größenregeln. Farbe und Besitzer liefert der Host;
Platzieren, Themenrahmen und Warten bleiben eigene Schritte.
"""

import contextlib
import tkinter as tk

ACTIVE_ATTRIBUTE = "_glide_modal_active"
FINISHED_ATTRIBUTE = "_glide_modal_finished"
DEFAULT_MAX_SCREEN_SHARE = 0.88
MIN_WIDTH_FLOOR = 360

_WINDOWS = (tk.Toplevel, tk.Tk)


@contextlib.contextmanager
def modal_over(root, parent=None):
    """Gibt den Tastatur- und Mausgriff nach einem Unterdialog zurück.

    Ein modaler Dialog nimmt den Griff an sich. Schließt er sich, fällt der
    Griff nicht von allein an das Fenster zurück, aus dem er geöffnet wurde –
    dieses nähme dann keine Eingabe mehr an und wirkte eingefroren.

    Ohne `parent` fragt Tk selbst, wer den Griff gerade hält. Das ist der
    zuverlässigere Weg, weil kein Aufrufer sein Fenster durchreichen muss –
    und weil er auch dann greift, wenn zwischen Maske und Unterdialog noch
    ein drittes Fenster liegt. Wird das aufrufende Fenster in der
    Zwischenzeit geschlossen, bleibt der Griff aus.
    """
    owner = parent if isinstance(parent, _WINDOWS) else None
    if owner is None:
        try:
            current = root.grab_current()
        except tk.TclError:
            current = None
        owner = current if isinstance(current, _WINDOWS) else None
    had_grab = False
    if owner is not None and owner is not root:
        try:
            had_grab = bool(owner.grab_status())
        except tk.TclError:
            had_grab = False
    try:
        yield
    finally:
        if had_grab:
            try:
                if owner.winfo_exists():
                    owner.grab_set()
            except tk.TclError:
                pass


def ensure_min_width(dialog, max_screen_share=DEFAULT_MAX_SCREEN_SHARE):
    """Die Mindestbreite eines Dialogs deckt seinen Inhalt – höchstens bis zum Bildschirmanteil.

    Ein Dialog mit `_glide_layout_measured` hat sein Layout schon gemessen;
    dann entfällt das erneute `update_idletasks`.
    """
    try:
        if not getattr(dialog, "_glide_layout_measured", False):
            dialog.update_idletasks()
        breite, hoehe = dialog.minsize()
        bedarf = dialog.winfo_reqwidth()
        grenze = int(dialog.winfo_screenwidth() * max_screen_share)
        if bedarf > breite:
            dialog.minsize(min(bedarf, max(MIN_WIDTH_FLOOR, grenze)), hoehe)
    except (tk.TclError, ValueError, TypeError):
        pass


def bring_to_front(dialog):
    """Zeigt einen Dialog sichtbar über dem Hauptfenster.

    Ein Dialog, der hinter dem Hauptfenster oder minimiert entsteht, wirkt
    wie ein Klick ohne Folge.
    """
    try:
        if dialog.state() in ("withdrawn", "iconic"):
            dialog.deiconify()
        dialog.lift()
        dialog.focus_force()
    except tk.TclError:
        pass


def _inside(widget, window):
    """True, wenn `widget` im Fenster `window` liegt (eigene Toplevels darin zählen mit).

    Für das Hauptfenster zählt nur, was nicht in einem eigenen Toplevel liegt;
    ein reiner Namensvergleich träfe dort jedes Widget der Anwendung.
    """
    if widget is None or window is None:
        return False
    name, prefix = str(widget), str(window)
    if prefix == ".":
        try:
            return widget.winfo_toplevel() is window
        except (KeyError, tk.TclError):
            return False
    return name == prefix or name.startswith(prefix + ".")


def _focus_now(root):
    """Fokus-Widget der Anwendung oder None – auch bei Tk-eigenen Fenstern."""
    try:
        return root.focus_get()
    except (KeyError, tk.TclError):
        return None


def _origin_window(root, dialog, parent):
    """Das Fenster, aus dem der Dialog kam: `parent`, sonst der Griffhalter, sonst der Master."""
    if isinstance(parent, _WINDOWS) and parent is not dialog:
        return parent
    try:
        current = root.grab_current()
    except tk.TclError:
        current = None
    if isinstance(current, _WINDOWS) and current is not dialog:
        return current
    try:
        master = dialog.master.winfo_toplevel() if dialog.master is not None else root
    except (AttributeError, tk.TclError):
        master = root
    return master if master is not dialog else root


def remember_focus(root, dialog, parent=None):
    """Merkt sich, wohin der Fokus nach dem Dialog zurückkehrt: (Fenster, Widget).

    Gefragt wird das aufrufende Fenster nach seinem zuletzt fokussierten Widget
    (`focus_lastfor`). Das gilt auch dann, wenn ein Aufrufer vor `run_modal`
    schon ein Feld im Dialog fokussiert hat oder `bring_to_front` den Fokus
    in den Dialog gezogen hat.
    """
    window = _origin_window(root, dialog, parent)
    widget = None
    try:
        widget = window.focus_lastfor()
    except (KeyError, tk.TclError):
        widget = None
    if _inside(widget, dialog):
        widget = None
    return window, widget


def return_focus(root, dialog, remembered):
    """Gibt den gemerkten Fokus zurück; True, wenn er gesetzt wurde.

    Ist das gemerkte Widget verschwunden, erhält sein Fenster den Fokus. Liegt
    der Fokus inzwischen in einem dritten, noch offenen Fenster – etwa einem,
    das der Dialog geöffnet hat –, bleibt er dort.
    """
    window, widget = remembered if remembered else (None, None)
    try:
        if window is None or not window.winfo_exists():
            return False
        current = _focus_now(root)
        if current is not None and current.winfo_exists() and not _inside(current, dialog) \
                and not _inside(current, window):
            return False  # ein drittes Fenster behält den Fokus
        target = widget if widget is not None and widget.winfo_exists() else window
        target.focus_set()
        return True
    except (KeyError, tk.TclError):
        return False


def wait_modal(root, dialog, parent=None, *, log_error=None):
    """Greift, wartet und gibt frei; der vorherige Griff und der Fokus kehren zurück.

    `log_error` erhält einen Text, wenn `grab_set` scheitert (etwa weil eine
    andere Anwendung den Griff hält oder das Fenster noch nicht sichtbar
    ist). Bis Glide 3.24 riss diese Ausnahme den Aufrufer mit: Der Dialog
    blieb offen, und die Anwendung wartete auf ein Fenster, das niemand
    mehr schließen konnte.
    """
    remembered = remember_focus(root, dialog, parent)
    try:
        with modal_over(root, parent):
            try:
                dialog.grab_set()
            except tk.TclError as fehler:
                if log_error is not None:
                    log_error(f"grab_set fehlgeschlagen: {fehler}\n")
            setattr(dialog, ACTIVE_ATTRIBUTE, True)
            try:
                finished = getattr(dialog, FINISHED_ATTRIBUTE, None)
                if finished is None:
                    root.wait_window(dialog)
                else:
                    root.wait_variable(finished)
            finally:
                setattr(dialog, ACTIVE_ATTRIBUTE, False)
                try:
                    if dialog.winfo_exists():
                        dialog.grab_release()
                except tk.TclError:
                    pass
    finally:
        return_focus(root, dialog, remembered)


def create_dialog(parent, title, *, background=None, transient=True, withdrawn=False,
                  resizable=None, minsize=None):
    """Legt ein Dialogfenster einheitlich an und gibt es zurück.

    `resizable` und `minsize` sind Paare (Breite, Höhe). `withdrawn` hält das
    Fenster bis zur Platzierung unsichtbar; der Host zeigt es selbst an.
    """
    dialog = tk.Toplevel(parent)
    if withdrawn:
        dialog.withdraw()
    dialog.title(title)
    if background is not None:
        dialog.configure(bg=background)
    if transient:
        dialog.transient(parent)
    if resizable is not None:
        dialog.resizable(*resizable)
    if minsize is not None:
        dialog.minsize(*minsize)
    return dialog


def run_modal(root, dialog, parent=None, *, background=None,
              max_screen_share=DEFAULT_MAX_SCREEN_SHARE, log_error=None):
    """Führt einen modalen Dialog vollständig aus: vorbereiten, nach vorn holen, warten."""
    if background is not None:
        dialog.configure(bg=background)
    ensure_min_width(dialog, max_screen_share)
    bring_to_front(dialog)
    wait_modal(root, dialog, parent, log_error=log_error)
