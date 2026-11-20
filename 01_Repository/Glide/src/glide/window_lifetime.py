# SPDX-License-Identifier: MPL-2.0
"""Zeitgeberbesitz je Fenster oder Ansicht ohne Glide-Bezug (Shell-Paket 3c, 15.11.2026).

Ein `AfterScope` gehört zu genau einem Tk-Widget – dem Hauptfenster, einem
Dialog oder einer Ansicht. Er merkt sich jeden Zeitgeber, den er anlegt, und
bricht alle ab, sobald sein Widget zerstört wird. Danach nimmt er keine neuen
Aufträge mehr an. So trifft kein später Rückruf auf ein Widget, das es nicht
mehr gibt.

Das Modul kennt weder Glide-Daten noch Glide-Module: nur Standardbibliothek
und `tkinter`. Was ein Zeitgeber tut, bestimmt allein der Aufrufer.

Vertrag: `tests/integration/test_fensterlebensdauer.py`.
"""

import tkinter as tk
import weakref

SCOPE_ATTRIBUTE = "_glide_after_scope"
PRUNE_START = 64

_SCOPES = weakref.WeakSet()


class AfterScope:
    """Besitzt die Zeitgeber eines Widgets und räumt sie mit ihm ab."""

    def __init__(self, widget, *, close_on_destroy=True):
        self.widget = widget
        self.jobs = set()
        self.closed = False
        # Wer einen Auftrag am Widget selbst abbricht (`widget.after_cancel`),
        # hinterlässt seine Kennung im Bestand. Ab dieser Größe räumt der
        # Bereich beim Planen gegen `after info` auf; die Schwelle wächst mit.
        self._prune_at = PRUNE_START
        _SCOPES.add(self)
        if close_on_destroy:
            try:
                widget.bind("<Destroy>", self._on_destroy, add="+")
            except tk.TclError:
                self.closed = True

    def _on_destroy(self, event):
        if getattr(event, "widget", None) is self.widget:
            self.close()

    def _schedule(self, starter, callback, args):
        if self.closed:
            return None
        holder = []

        def run():
            if holder:
                self.jobs.discard(holder[0])
            if self.closed:
                return
            callback(*args)

        # Tk benennt den Auftrag nach der Funktion; so bleibt er in `after info` lesbar.
        run.__name__ = getattr(callback, "__name__", "run")
        try:
            job = starter(run)
        except tk.TclError:
            return None
        holder.append(job)
        self.jobs.add(job)
        if len(self.jobs) > self._prune_at:
            self.jobs.intersection_update(self._live())
            self._prune_at = max(PRUNE_START, 2 * len(self.jobs))
        return job

    def after(self, delay_ms, callback, *args):
        """Wie `widget.after`; `None`, wenn Bereich oder Widget beendet sind."""
        return self._schedule(lambda run: self.widget.after(delay_ms, run), callback, args)

    def after_idle(self, callback, *args):
        """Wie `widget.after_idle`; `None`, wenn Bereich oder Widget beendet sind."""
        return self._schedule(lambda run: self.widget.after_idle(run), callback, args)

    def _live(self):
        try:
            return set(self.widget.tk.splitlist(self.widget.tk.call("after", "info")))
        except (tk.TclError, RuntimeError):
            return set()

    def adopt(self, job):
        """Übernimmt einen fremd angelegten Zeitgeber; gibt ihn unverändert zurück.

        Bereits gelaufene Aufträge fallen dabei aus dem Bestand, damit er bei
        lang laufenden Fenstern nicht wächst.
        """
        if job is not None:
            self.jobs.intersection_update(self._live())
            self.jobs.add(job)
        return job

    def pending(self):
        """Die noch ausstehenden eigenen Zeitgeber."""
        self.jobs.intersection_update(self._live())
        return frozenset(self.jobs)

    def cancel(self, job):
        """Bricht einen Zeitgeber ab; unbekannte und gelaufene sind kein Fehler."""
        if job is None:
            return
        self.jobs.discard(job)
        try:
            self.widget.after_cancel(job)
        except (tk.TclError, ValueError):
            pass

    def cancel_all(self):
        """Bricht alle eigenen Zeitgeber ab; der Bereich bleibt benutzbar."""
        for job in list(self.jobs):
            self.cancel(job)
        self.jobs.clear()

    def close(self):
        """Bricht alle Zeitgeber ab und nimmt keine neuen mehr an."""
        self.closed = True
        self.cancel_all()


def scope_for(widget):
    """Der Zeitgeberbereich eines Widgets; beim ersten Zugriff angelegt."""
    scope = getattr(widget, SCOPE_ATTRIBUTE, None)
    if scope is None or scope.widget is not widget:
        scope = AfterScope(widget)
        setattr(widget, SCOPE_ATTRIBUTE, scope)
    return scope


def pending_jobs(widget):
    """Alle ausstehenden Zeitgeber aller Bereiche im Interpreter von `widget`."""
    jobs = set()
    for scope in list(_SCOPES):
        if getattr(scope.widget, "tk", None) is widget.tk:
            jobs.update(scope.pending())
    return frozenset(jobs)
