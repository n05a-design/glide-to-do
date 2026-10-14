"""Native Semantik an die Lebensdauer eines Widgets binden; kein Tk-Import.

Nach Map/Fokus/Selektion setzen Klassenbindungen eigene Standardwerte.
Der nachgelagerte Auftrag ergänzt die aktuellen Fachwerte und erhält dabei
vorhandene Tastenbindungen. Native Attribute ersetzen keine Readerabnahme.
"""
from dataclasses import replace
from accessibility import Attributes, screenreader_active, set_attributes


def available(call):
    commands = ('set_acc_role', 'add_acc_object', 'emit_focus_change',
                'emit_selection_change', 'check_screenreader')
    if not all(bool(call('info', 'commands', '::tk::accessible::'+name)) for name in commands):
        return False
    # Ohne ATK registriert Tk 9.1 gleichnamige Platzhalter. Der echte native
    # Status liefert auch ohne aktiven Reader 0; Stub-Warnung/leer genügt nicht.
    return call('::tk::accessible::check_screenreader') in (0, 1, '0', '1')


class Binding:
    def __init__(self, widget, attributes, *, action=None, supported=None):
        self.widget = widget
        self.attributes = attributes
        self.action = action
        self.closed = False
        self.job = None
        self.focus_changed = self.selection_changed = False
        self.bindings = {}
        self.command = None
        self.supported = available(widget.tk.call) if supported is None else bool(supported)
        if not self.supported:
            return
        if action is not None:
            self.command = widget.register(self.invoke)
        for event, handler in (
                ('<Map>', lambda _event: self.refresh()),
                ('<FocusIn>', lambda _event: self.refresh(focus=True)),
                ('<<TreeviewSelect>>', lambda _event: self.refresh(selection=True)),
                ('<Destroy>', lambda event: self.close() if event.widget is widget else None)):
            self.bindings[event] = widget.bind(event, handler, add='+')
        self.refresh()

    def invoke(self):
        if (not self.closed and self.action is not None and
                self.widget.winfo_exists() and self.widget.winfo_ismapped()):
            current = self.attributes()
            if isinstance(current, Attributes) and current.state != 'disabled':
                return self.action()
        return 'break'

    def refresh(self, *, focus=False, selection=False):
        if self.closed or not self.supported:
            return
        self.focus_changed |= focus
        self.selection_changed |= selection
        if self.job is None:
            self.job = self.widget.after_idle(self._apply)

    def _apply(self):
        self.job = None
        if self.closed:
            return
        widget = self.widget
        focus, selection = self.focus_changed, self.selection_changed
        self.focus_changed = self.selection_changed = False
        if not widget.winfo_exists() or not widget.winfo_ismapped():
            return
        current = self.attributes()
        if current is None:
            current = Attributes('Label', 'Nicht verfügbar', state='disabled')
        if self.command is not None and self.action is not None and current.state != 'disabled':
            current = replace(current, action=(self.command,))
        set_attributes(widget.tk.call, widget, current)
        widget.tk.call('::tk::accessible::add_acc_object', str(widget))
        if (focus or selection) and screenreader_active(widget.tk.call):
            event = 'emit_focus_change' if focus else 'emit_selection_change'
            widget.tk.call('::tk::accessible::'+event, str(widget))

    def close(self):
        if self.closed:
            return
        self.closed = True
        widget = self.widget
        if self.job is not None:
            widget.after_cancel(self.job)
            self.job = None
        if widget.winfo_exists():
            for event, identity in self.bindings.items():
                widget.unbind(event, identity)
        if self.command is not None:
            widget.deletecommand(self.command)
        self.bindings.clear()
        self.command = None
        self.widget = self.attributes = self.action = None
