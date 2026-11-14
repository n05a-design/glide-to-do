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
- Den Fokus nach dem Schließen stellt der Aufrufer her, nicht dieses Modul.

Die Attributnamen `_glide_modal_active` und `_glide_modal_finished` bleiben
aus Kompatibilität: Einstellungsdialog und Fensterwechsel der App lesen sie.
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


def wait_modal(root, dialog, parent=None, *, log_error=None):
    """Greift, wartet und gibt frei; der vorherige Griff kehrt zurück.

    `log_error` erhält einen Text, wenn `grab_set` scheitert (etwa weil eine
    andere Anwendung den Griff hält oder das Fenster noch nicht sichtbar
    ist). Bis Glide 3.24 riss diese Ausnahme den Aufrufer mit: Der Dialog
    blieb offen, und die Anwendung wartete auf ein Fenster, das niemand
    mehr schließen konnte.
    """
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


def run_modal(root, dialog, parent=None, *, background=None,
              max_screen_share=DEFAULT_MAX_SCREEN_SHARE, log_error=None):
    """Führt einen modalen Dialog vollständig aus: vorbereiten, nach vorn holen, warten."""
    if background is not None:
        dialog.configure(bg=background)
    ensure_min_width(dialog, max_screen_share)
    bring_to_front(dialog)
    wait_modal(root, dialog, parent, log_error=log_error)
